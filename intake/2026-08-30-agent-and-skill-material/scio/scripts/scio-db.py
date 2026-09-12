#!/usr/bin/env python3
"""The findings and skills as a queryable store, instead of regex over prose.

Why this replaces scripts/findings-index.py
-------------------------------------------
That script guessed a finding's layer with a regex over the row's text. It was wrong in
two ways at once: case-insensitively, so the English article "a" matched as layer A and
"e.g." as layer E, inflating every count reported for a day; and structurally, because a
row whose layer cell reads "Playbook" or "B, G" matches nothing. Three separate agents
had to work around it, and each re-derived its layer scope by hand.

The triage documents fixed the underlying problem without meaning to. Every row there is
`id | finding | source:line | verdict | destination`, and **the layer comes from the
filename** — `LAYER-E-TRIAGE.md` is Layer E, exactly, with nothing to infer. So the store
reads those rather than the five different table formats in docs/mined/.

SQLite, because it ships with Python and adds no dependency. The graph half stays
graphify's job: relationships across the corpus. This is the attribute half — which
layer, which verdict, which skill a finding became, and what is still undone.

Usage
  scripts/scio-db.py build            rebuild scio.db from the triage files and skills
  scripts/scio-db.py layers           findings per layer and verdict
  scripts/scio-db.py skill <name>     which findings a skill rests on
  scripts/scio-db.py adrs             decisions triaged but not yet written
  scripts/scio-db.py dupes            one finding recorded in two layers
  scripts/scio-db.py sql "<query>"    anything else
"""
import pathlib, re, sqlite3, sys

DB = pathlib.Path("scio.db")
ROW = re.compile(r"^\|\s*\**([A-G]?\d+)\**\s*\|(.+?)\|(.+?)\|\s*\**(SKILL|ADR|FIX|DROP)\b.*?\|(.*)\|\s*$")
SRC = re.compile(r"`?([A-Za-z0-9._-]+\.md):(\d+)`?")


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*`]", "", s)).strip()


def build() -> None:
    if DB.exists():
        DB.unlink()
    db = sqlite3.connect(DB)
    db.executescript("""
        CREATE TABLE finding(
          id INTEGER PRIMARY KEY, layer TEXT NOT NULL, row_no TEXT,
          text TEXT NOT NULL, src_doc TEXT, src_line INTEGER,
          verdict TEXT NOT NULL, destination TEXT, triage_file TEXT);
        CREATE TABLE skill(
          name TEXT PRIMARY KEY, layer TEXT, phase TEXT, status TEXT,
          desc_chars INTEGER, body_bytes INTEGER);
        CREATE INDEX finding_layer ON finding(layer);
        CREATE INDEX finding_verdict ON finding(verdict);

        -- The content half. graphify holds relationships and `finding` holds attributes;
        -- neither holds the text, so reading anything still meant opening a 50 KB file.
        -- A chunk is one heading-delimited section: the granularity a question is
        -- actually answered at, and the granularity retrieval should cost.
        CREATE TABLE chunk(
          id INTEGER PRIMARY KEY, kind TEXT, source TEXT, heading TEXT,
          depth INTEGER, line INTEGER, chars INTEGER, body TEXT);
        CREATE VIRTUAL TABLE chunk_fts USING fts5(
          heading, body, content=chunk, content_rowid=id, tokenize="unicode61");
        CREATE INDEX chunk_source ON chunk(source);
    """)

    # Four agents were given one instruction and produced four schemas. Two put the verdict
    # in a column; two put it in a section heading. That is the argument for this file
    # existing: prose does not carry structure reliably, even when structure is asked for.
    HEADING = re.compile(r"^#{2,4}\s.*\b(SKILL|ADR|FIX|DROP)\b")
    ROW4 = re.compile(r"^\|\s*\**([A-G]?\d+)\**\s*\|(.+?)\|(.+?)\|(.*)\|\s*$")

    for f in sorted(pathlib.Path("docs/triage").glob("LAYER-*-TRIAGE.md")):
        # The layer is the filename. Nothing is inferred from prose.
        layers = re.match(r"LAYER-([A-G]+)-TRIAGE", f.name).group(1)
        section = None
        for line in f.read_text(errors="ignore").splitlines():
            h = HEADING.match(line)
            if h:
                section = h.group(1)
                continue
            m, verdict, dest = ROW.match(line), None, None
            if m:
                verdict, src_cell, dest = m.group(4), m.group(3), m.group(5)
            else:
                m = ROW4.match(line)
                # A four-column row only counts inside a verdict section, and only when it
                # cites a source. Summary tables have neither.
                if not m or not section or not SRC.search(m.group(3)):
                    continue
                verdict, src_cell, dest = section, m.group(3), m.group(4)
            src = SRC.search(src_cell)
            db.execute(
                "INSERT INTO finding(layer,row_no,text,src_doc,src_line,verdict,destination,triage_file)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (layers, m.group(1), clean(m.group(2)),
                 src.group(1) if src else None, int(src.group(2)) if src else None,
                 verdict, clean(dest), f.name))

    for d in sorted(pathlib.Path(".claude/skills").iterdir()):
        sf = d / "SKILL.md"
        if not sf.is_file():
            continue
        t = sf.read_text(errors="ignore")
        fm = re.match(r"---\n(.*?)\n---", t, re.S)
        g = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm.group(1), re.M).group(1).strip()
                       if fm and re.search(rf"^{k}:\s*(.*)$", fm.group(1), re.M) else None)
        dm = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:|\n---)", t, re.S | re.M)
        db.execute("INSERT INTO skill VALUES (?,?,?,?,?,?)",
                   (d.name, g("layer"), g("phase"), g("status"),
                    len(clean(dm.group(1))) if dm else 0,
                    sum(p.stat().st_size for p in d.rglob("*.md"))))
    # --- content, chunked by heading -------------------------------------------------
    HEAD = re.compile(r"^(#{1,4})\s+(.*\S)\s*$")
    corpus = [("skill", p) for p in sorted(pathlib.Path(".claude/skills").rglob("*.md"))]
    corpus += [("doc", p) for p in sorted(pathlib.Path("docs").rglob("*.md"))]
    for kind, path in corpus:
        lines = path.read_text(errors="ignore").splitlines()
        head, depth, start, buf = "(frontmatter)", 0, 1, []
        def flush(end_line):
            text = "\n".join(buf).strip()
            if text:
                db.execute(
                    "INSERT INTO chunk(kind,source,heading,depth,line,chars,body)"
                    " VALUES (?,?,?,?,?,?,?)",
                    (kind, str(path), head, depth, start, len(text), text))
        for i, line in enumerate(lines, 1):
            h = HEAD.match(line)
            if h:
                flush(i)
                head, depth, start, buf = h.group(2), len(h.group(1)), i, []
            else:
                buf.append(line)
        flush(len(lines))
    db.execute("INSERT INTO chunk_fts(rowid,heading,body) SELECT id,heading,body FROM chunk")

    db.commit()
    n = db.execute("SELECT count(*) FROM finding").fetchone()[0]
    k = db.execute("SELECT count(*) FROM skill").fetchone()[0]
    c, ch = db.execute("SELECT count(*), sum(chars) FROM chunk").fetchone()
    print(f"scio.db — {n} findings, {k} skills, {c} chunks ({ch:,} chars searchable)")
    db.close()


def q(sql: str, args=()) -> list:
    return sqlite3.connect(DB).execute(sql, args).fetchall()


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "layers"
    if cmd == "build":
        return build()
    if not DB.exists():
        sys.exit("no scio.db — run: scripts/scio-db.py build")

    if cmd == "layers":
        print(f"{'layer':<8}{'SKILL':>7}{'ADR':>6}{'FIX':>6}{'DROP':>6}{'total':>7}")
        for r in q("""SELECT layer,
                        sum(verdict='SKILL'), sum(verdict='ADR'),
                        sum(verdict='FIX'), sum(verdict='DROP'), count(*)
                      FROM finding GROUP BY layer ORDER BY layer"""):
            print(f"{r[0]:<8}{r[1]:>7}{r[2]:>6}{r[3]:>6}{r[4]:>6}{r[5]:>7}")
        t = q("SELECT sum(verdict='SKILL'),sum(verdict='ADR'),sum(verdict='FIX'),"
              "sum(verdict='DROP'),count(*) FROM finding")[0]
        print(f"{'ALL':<8}{t[0]:>7}{t[1]:>6}{t[2]:>6}{t[3]:>6}{t[4]:>7}")

    elif cmd == "skill":
        name = sys.argv[2]
        rows = q("SELECT layer,row_no,text,src_doc,src_line FROM finding "
                 "WHERE verdict='SKILL' AND destination LIKE ? ORDER BY layer,row_no",
                 (f"%{name}%",))
        print(f"{name} rests on {len(rows)} findings\n")
        for layer, n, text, doc, line in rows:
            print(f"  {layer}-{n:<4} {text[:72]}")
            print(f"          {doc}:{line}")

    elif cmd == "adrs":
        rows = q("SELECT layer,row_no,text,src_doc,src_line FROM finding "
                 "WHERE verdict='ADR' ORDER BY layer,row_no")
        print(f"{len(rows)} decisions triaged, and docs/decisions/ holds one ADR\n")
        for layer, n, text, doc, line in rows[:20]:
            print(f"  {layer}-{n:<4} {text[:74]}")
        if len(rows) > 20:
            print(f"  … {len(rows)-20} more")

    elif cmd == "dupes":
        rows = q("""SELECT src_doc, src_line, count(DISTINCT layer) c,
                           group_concat(layer||'-'||row_no, '  '), min(text)
                    FROM finding WHERE src_doc IS NOT NULL
                    GROUP BY src_doc, src_line HAVING c > 1 ORDER BY c DESC""")
        print(f"{len(rows)} source rows triaged by more than one layer\n")
        for doc, line, c, where, text in rows:
            print(f"  {doc}:{line}   {where}")
            print(f"      {text[:76]}")

    elif cmd == "find":
        # Content search. Returns the section, not the file.
        term = " ".join(sys.argv[2:])
        rows = q("""SELECT c.source, c.heading, c.line, c.chars,
                           snippet(chunk_fts, 1, '>>', '<<', ' … ', 14)
                    FROM chunk_fts f JOIN chunk c ON c.id = f.rowid
                    WHERE chunk_fts MATCH ? ORDER BY rank LIMIT 8""", (term,))
        print(f"{len(rows)} sections match {term!r}\n")
        for src, head, line, chars, snip in rows:
            print(f"  {src}:{line}  §{head}   [{chars} chars ≈ {chars//4} tokens]")
            print(f"      {re.sub(chr(10), ' ', snip)}\n")

    elif cmd == "read":
        # Fetch one section by heading. This is the retrieval the corpus was missing.
        rows = q("SELECT source,heading,line,chars,body FROM chunk WHERE heading LIKE ? "
                 "ORDER BY chars DESC LIMIT 1", (f"%{' '.join(sys.argv[2:])}%",))
        if not rows:
            sys.exit("no section matched")
        src, head, line, chars, body = rows[0]
        whole = q("SELECT sum(chars) FROM chunk WHERE source=?", (src,))[0][0]
        print(f"{src}:{line}  §{head}")
        print(f"[{chars} chars ≈ {chars//4} tokens — the whole file is {whole:,} "
              f"≈ {whole//4:,}, so this is {chars*100//whole}%]\n")
        print(body)

    elif cmd == "sql":
        for r in q(sys.argv[2]):
            print("  " + " | ".join(str(x) for x in r))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
