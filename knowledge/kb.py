#!/usr/bin/env python3
"""One index over the whole knowledge base — notes, raw imports, intake, pipeline, talents.

Why
---
On 2026-09-02 the project's knowledge lived in three repositories and was indexed in one
(Scio's scio.db, which saw one repo of three and nothing written since session start). This
file is the single index the merge asked for: every knowledge-bearing markdown file in this
repository, chunked by heading, full-text searchable, with the note frontmatter's provenance
(status, fetched dates, sources) as columns. It is rebuilt from the files and never a source
of truth: `knowledge/kb.db` is gitignored and costs seconds, no model call.

Measured on first build (2026-09-02): see the line `build` prints.

Usage
  knowledge/kb.py build                 rebuild knowledge/kb.db
  knowledge/kb.py find "<terms>"        sections matching, cheapest first (FTS5 syntax)
  knowledge/kb.py read "<heading>"      one section, and nothing else
  knowledge/kb.py stale [days]          MEASURED notes whose fetch date is older than N days
  knowledge/kb.py links                 wikilinks that point nowhere, and one-way links
  knowledge/kb.py path <a> <b>          shortest wikilink path between two notes, with the sentence each hop sits in
  knowledge/kb.py explain <note>        a note's neighbours (in and out), each with the sentence that links them
  knowledge/kb.py shared <note>         notes that cite the same source URL — related by evidence, not by link
  knowledge/kb.py cooccur "<a>" "<b>"   sections anywhere (raw, intake, skills) that mention both terms
  knowledge/kb.py check                 the whole routine, one exit code: build, lint,
                                        contradictions, selftest (this is what CI runs)
  knowledge/kb.py contradictions        two notes giving different values for the same fact
  knowledge/kb.py owners                a project whose own README names an owner we do not cite
  knowledge/kb.py sql "<query>"         anything else (tables: doc, chunk, chunk_fts, link)
  knowledge/kb.py selftest              proves the index can fail: a planted miss must miss,
                                        and a planted contradiction must be caught
"""
import collections, pathlib, re, signal, sqlite3, sys, time

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # let `| head` cut output without a traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "knowledge" / "kb.db"
AREAS = {  # kind -> glob, relative to repo root
    "note": "knowledge/notes/*.md",
    "raw": "knowledge/raw/**/*.md",
    "intake": "intake/**/*.md",
    "pipeline": "pipeline/*.md",
    # The library is INERT in this repository: nothing sits under .claude/, because that path
    # is the activation. The globs below therefore index the neutral copies, and the index is
    # the only thing that reads them - no talent here loads, triggers or routes. Moved
    # 2026-09-12; a glob left pointing at .claude/ would have indexed nothing and said nothing,
    # which is the failure mode this file already records for the CI trigger.
    "skill": "library/skills/*/SKILL.md",
    "agent": "library/agents/*.md",
    # CLAUDE.md cannot live at the root here either - a root CLAUDE.md auto-loads, and one
    # carrying a capability map over 79 talents would route on arrival. It is archived under
    # docs/steering/ and indexed from there, so it stays searchable without being steering.
    "steering": "docs/steering/*.md",
    "catalog": "catalog/**/*.md",
    "root": "*.md",
}
HEAD = re.compile(r"^(#{1,6})\s+(.*)$")
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\[\[([^\]|#]+)")


def derive_status(sources, held):
    """Can a reader re-derive this page's claims from THIS repo, or only from the open web?

    `status:` used to be asserted in every note's frontmatter and said `verified` in all 44 of
    them - a cardinality of one, which is either a redundant field or an unenforced one. On
    2026-09-12 it was measured to be the second: four notes said `verified` while the primary
    they rest on could not be opened in this container at all, so the word meant "written", not
    "checked". Derived here instead, because a value another file can falsify is a query and not
    a claim.

    `sources` is how many retrievable sources the page cites; `held` how many of them the page
    names a raw copy of. Deliberately not called verified/unverified: a page whose sources
    predate the raw layer WAS checked, just not reproducibly, and the field must not say
    otherwise.
    """
    if not sources:
        return "note-only"
    return "reproducible" if held else "cited-only"


def single_valued(values_by_field):
    """Fields whose distinct value count across the corpus is 1 - the general check that would
    have caught `status`. A field that only ever holds one value is either redundant or
    unenforced, and both are worth a line in the lint. Fields absent everywhere are not reported:
    a field nobody uses is a different finding from one everybody agrees on.
    """
    out = []
    for field, vals in sorted(values_by_field.items()):
        seen = {v for v in vals if v is not None}
        if len(seen) == 1 and len(vals) > 1:
            out.append((field, next(iter(seen)), len(vals)))
    return out


def frontmatter(text):
    m = FM.match(text)
    if not m:
        return {}, text, ""
    fm = m.group(1)
    def field(name):
        mm = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
        return mm.group(1).strip().strip('"') if mm else None
    n_src = len(re.findall(r"^\s*-\s+(url|note):", fm, re.M))
    n_held = len(re.findall(r"^\s+-\s+knowledge/raw/\S+", fm, re.M))
    return {
        "title": field("title"), "status": derive_status(n_src, n_held),
        "fetched": sorted(set(re.findall(r"fetched:\s*(\d{4}-\d{2}-\d{2})", fm))),
        "sources": n_src, "held": n_held,
    }, text[m.end():], fm


def build():
    t0 = time.time()
    if DB.exists():
        DB.unlink()
    db = sqlite3.connect(DB)
    db.executescript("""
        CREATE TABLE doc(id INTEGER PRIMARY KEY, kind TEXT, path TEXT UNIQUE, title TEXT,
          status TEXT, fetched_min TEXT, fetched_max TEXT, sources INTEGER, chars INTEGER);
        CREATE TABLE chunk(id INTEGER PRIMARY KEY, doc INTEGER, kind TEXT, path TEXT,
          heading TEXT, depth INTEGER, line INTEGER, chars INTEGER, body TEXT);
        CREATE VIRTUAL TABLE chunk_fts USING fts5(heading, body, content=chunk,
          content_rowid=id, tokenize="unicode61");
        CREATE TABLE link(src TEXT, dst TEXT, context TEXT);
        CREATE TABLE source(note TEXT, url TEXT);
        CREATE INDEX chunk_path ON chunk(path);
    """)
    seen = set()
    for kind, pattern in AREAS.items():
        for f in sorted(ROOT.glob(pattern)):
            rel = str(f.relative_to(ROOT))
            if rel in seen or "kb.db" in rel:
                continue
            seen.add(rel)
            text = f.read_text(errors="replace")
            meta, body, meta_raw = frontmatter(text)
            cur = db.execute(
                "INSERT INTO doc(kind,path,title,status,fetched_min,fetched_max,sources,chars)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (kind, rel, meta.get("title") or f.stem, meta.get("status"),
                 (meta.get("fetched") or [None])[0], (meta.get("fetched") or [None])[-1],
                 meta.get("sources"), len(text)))
            did = cur.lastrowid
            if kind == "note":
                # An edge argued in the body carries the sentence it sits in. An edge that
                # exists only in the frontmatter's related: line is asserted, not argued —
                # kept, marked, and reported by `links` as unexplained.
                seen_dst = set()
                for sent in re.split(r"(?<=[.!?])\s+|\n", body):  # a table row is its own sentence
                    for dst in LINK.findall(sent):
                        dst = dst.strip()
                        if dst not in seen_dst:
                            seen_dst.add(dst)
                            db.execute("INSERT INTO link VALUES(?,?,?)", (f.stem, dst, " ".join(sent.split())[:240]))
                # A wikilink in a source's note: field IS argued — "its rules are folded into
                # [[skill-anatomy]]" says why the edge exists. Only the bare related: line is
                # an assertion, so the two are recorded apart rather than lumped.
                rel_line = re.search(r"^related:.*$", meta_raw, re.M)
                rel_dsts = {d.strip() for d in LINK.findall(rel_line.group(0))} if rel_line else set()
                fm_dsts = {d.strip() for d in LINK.findall(meta_raw)}
                for dst in fm_dsts:
                    ctx = edge_context(dst, seen_dst, rel_dsts, fm_dsts)
                    if ctx:
                        db.execute("INSERT INTO link VALUES(?,?,?)", (f.stem, dst, ctx))
                for url in set(re.findall(r"^\s*-\s+url:\s*(\S+)", meta_raw, re.M)):
                    db.execute("INSERT INTO source VALUES(?,?)", (f.stem, url.rstrip("/")))
            heading, depth, start, buf = "(top)", 0, 1, []
            def flush(end):
                b = "\n".join(buf).strip()
                if b:
                    db.execute("INSERT INTO chunk(doc,kind,path,heading,depth,line,chars,body)"
                               " VALUES(?,?,?,?,?,?,?,?)",
                               (did, kind, rel, heading, depth, start, len(b), b))
            for i, ln in enumerate(text.splitlines(), 1):
                m = HEAD.match(ln)
                if m:
                    flush(i); heading, depth, start, buf = m.group(2).strip(), len(m.group(1)), i, []
                else:
                    buf.append(ln)
            flush(None)
    db.execute("INSERT INTO chunk_fts(rowid,heading,body) SELECT id,heading,body FROM chunk")
    db.commit()
    n_doc, n_chunk, chars = db.execute("SELECT (SELECT COUNT(*) FROM doc),(SELECT COUNT(*) FROM chunk),(SELECT SUM(chars) FROM doc)").fetchone()
    print(f"kb.db — {n_doc} documents, {n_chunk} sections, {chars:,} chars, {time.time()-t0:.1f}s, no model call")


def q(sql, args=()):
    return sqlite3.connect(DB).execute(sql, args).fetchall()


def match(terms):
    """Plain words → an FTS5 query that cannot be a syntax error.
    scio.db crashed on `find "multi-agent-system"` and `find "WHICH/HOW"`; every token is
    quoted, so punctuation is content, not an operator. Prefix the query with `fts:` to pass
    FTS5 syntax through untouched."""
    if terms.startswith("fts:"):
        return terms[4:]
    return " ".join('"' + t.replace('"', '""') + '"' for t in terms.split())



# --- contradictions -----------------------------------------------------------
# The lint's third check, the one the wiki pattern named as missing. It does not read
# prose; it compares TYPED VALUES stated about a SHARED SUBJECT. Two notes qualify as a
# pair when they cite the same source URL (the lint already emits those pairs as
# candidates); the subject anchors are the tags they share plus the words of that URL's
# path. A sentence is only read if it names an anchor, so "0.9.53" in a note about
# something else never collides with a version here. Every hit is a candidate for a human:
# a range ("MIT through v7, Apache-2.0 from v8") is a legitimate pair of values, so the
# check reports and never edits.
VALUE_RE = [
    ("licence", r"\b(MIT|Apache-2\.0|BSD-3-Clause|GPL-3\.0|AGPL-3\.0|MPL-2\.0)\b"),
    ("version", r"\bv?(\d+\.\d+\.\d+)\b"),
    ("pages",   r"(?<![\d.])(\d+)\s?(?:pp\b|pages\b)"),
    ("tokens",  r"\b(\d[\d,]*)[\s-]tokens?\b"),
    ("words",   r"\b(\d[\d,]*)[\s-]words?\b"),
    ("lines",   r"\b(\d[\d,]*)[\s-]lines?\b"),
    ("price",   r"\$([\d.]+)\b"),
]
# Anchors must SINGLE OUT a subject. A word two notes share only because both are about
# Claude Code anchors nothing, so the generic vocabulary of this domain is excluded; what
# remains is a product or document name.
STOP = {"the","and","for","docs","com","www","https","http","raw","main","md","html","json",
        "en","hubfs","pdf","claude","anthropic","skill","skills","code","github","project",
        "resources","blog","index","page","docs.claude","tooling","agent","agents"}


def anchors(url, tags_a, tags_b):
    words = {w.lower() for w in re.split(r"[^A-Za-z0-9.]+", url) if len(w) > 3 and w.lower() not in STOP}
    shared_tags = {t.lower() for t in set(tags_a) & set(tags_b)} - STOP
    return {a for a in shared_tags | words if len(a) > 3}


LIMIT_W = re.compile(r"\b(under|below|over|exceed\w*|max\w*|min\w*|cap|caps|capped|limit\w*|"
                     r"budget|recommend\w*|at most|no more than|threshold|allowed)\b", re.I)
MEAS_W = re.compile(r"\b(measured|median|mean|average|range[sd]?|actual|observed|counted|"
                    r"longest|shortest|is\b|was\b|are\b|→|->)\b", re.I)


def facet(sent, at):
    """A stated LIMIT and a MEASURED value are different claims about the same subject, and
    comparing them is the noisiest false positive this check can make. Judged on the words
    AROUND THE VALUE, not the sentence: "the licence changed under this note" is not a cap,
    and reading the whole sentence made exactly that mistake."""
    w = sent[max(0, at - 40):at + 20]
    if LIMIT_W.search(w):
        return "limit"
    return "measured" if MEAS_W.search(w) else "plain"



LIVE_LINK = re.compile(r"/(actions|releases|blob|tree|raw|issues|pull|pulls|wiki|discussions|"
                      r"commits?|compare|archive)(/|$)")


def self_link_live(url_tail):
    """Is this self-link one the maintainers must keep working, or one that can rot unnoticed?

    Measured 2026-09-08 on the two hits this check produced. graphify's single hit is a
    `git clone …/graphify.git` line the rename left behind - inert, and our citation of
    Graphify-Labs was right. goose's four are a CI workflow badge, a releases download URL
    and two blob/main doc links: those 404 at a wrong address, so a README carrying them is
    maintained THERE, and our citation of block/goose was the stale one. Same count shape,
    opposite verdicts - so the count alone was never the signal.
    """
    return bool(LIVE_LINK.search(url_tail))


def newest_per_repo(entries):
    """Pick the most recently fetched stored README per repo, from (repo, date, tag) triples.

    Nothing in the raw layer is ever deleted, so once an ownership move is settled by
    re-fetching at the new address the OLD baseline stays on disk forever. Judging both would
    report a finding that has already been acted on, every run, and a check that cannot be
    satisfied is one people learn to ignore.
    """
    best = {}
    for repo, date, tag in entries:
        k = repo.lower()
        if k not in best or date >= best[k][0]:
            best[k] = (date, tag)
    return {k: v[1] for k, v in best.items()}


def uncovered_areas(area_globs, workflow_paths):
    """Which indexed areas would a CI path filter NOT fire on?

    Measured 2026-09-08: the filter said `knowledge/**` while the index held 666 documents
    across 8 areas, only 177 of them under knowledge/. selftest asserts on intake/ content
    directly, so a change there could break this very check while CI stayed silent - and the
    failure would then surface at the next unrelated knowledge/ push, attributed to the wrong
    commit. A delayed, mis-attributed failure is worse than no check at all, which is why this
    is a fixture rather than a comment.
    """
    tops = {p.split("/")[0].split("*")[0] for p in workflow_paths if p}
    return [g for g in area_globs
            if g.split("/")[0].split("*")[0] not in tops and g not in workflow_paths]


def edge_context(dst, body_dsts, rel_dsts, fm_dsts):
    """Where is this edge argued? A wikilink in a source's note: field IS argued — "its rules
    are folded into [[skill-anatomy]]" says why the edge exists — so only a name on the bare
    related: line is an assertion. Kept as a function, not inline, because the last check whose
    predicate lived inline was contaminated by its own fixture and passed while blind."""
    if dst in body_dsts:
        return None                                    # argued in the body: the edge carries its sentence
    if dst in fm_dsts - rel_dsts:
        return "(related: explained in a source note)"
    return "(related: frontmatter only)"


def unargued(edges):
    """The asserted edges argued at NEITHER end, from (src, dst, context) triples.

    This repo REQUIRES a new note's neighbours to name it back, so the reciprocal half of an
    argued edge is asserted BY DESIGN: the sentence exists, in the note that owns the relation.
    Counting those as debt put 212 edges on one queue when 134 were the debt — the same mistake
    the REPEATED verdict made one layer up, and found the same way: by splitting the population.
    """
    argued = {(s, d) for s, d, c in edges if not c.startswith("(related:")}
    return [(s, d) for s, d, c in edges if c == "(related: frontmatter only)" and (d, s) not in argued]


def compiled_stale(page_fetched, snapshot, current):
    """A COMPILED page has no external source to watch, so nothing could tell it its INPUTS
    moved. Found 2026-09-08: the base's one compiled page declared `fetched: 2026-09-02` while
    all five notes it draws on had been rewritten since, two of them declaring later fetches.
    Every other check in this file looks outward (a URL moved) or at link structure; a page
    derived from other pages fell between them.

    Deliberately compares DECLARED dates, not git or mtime: CI checks out shallow, so `git log`
    is empty for most files there, and a fresh clone gives every file the same mtime. A content
    join key works in both places. Returns the inputs that have moved on.
    """
    moved = []
    for name, at_compile in snapshot.items():
        now = current.get(name)
        if now and now > max(at_compile, page_fetched):
            moved.append((name, at_compile, now))
    return moved


def verdict_suspect(line):
    """True when a REPEATED line gives a sample size but names no other measurer.

    The claims contract reserves REPEATED for "the source restates a finding measured by
    someone else". Four lines on 2026-09-04 used it to mean "small sample, treat with care" -
    a provenance label doing a confidence job - and the cost was a verification queue that
    ranked on the mixture and sent a reader after work that did not exist. The attribution
    words keep a SOURCE's own sample ("the paper reports n=400") from tripping this.
    """
    if "REPEATED" not in line:
        return False
    has_n = re.search(r"\bn\s*=\s*\d|\b\d+\s*(batches|occurrences|runs|trials)\b", line)
    attributed = re.search(r"source|paper|report|README|card|docs?\b|blog|search|video|"
                           r"review|press|study|vendor|their|authors?", line, re.I)
    return bool(has_n and not attributed)

def units(text):
    """One claim = one unit. A line, a markdown table row — and a whole `- url:` block in
    the frontmatter, because a source's page count sits on its `note:` line while the thing
    it names sits on the `url:` line above, and split apart neither can anchor the other."""
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm, body = text[3:end], text[end:]
        block = []
        for line in fm.splitlines():
            if re.match(r"\s*-\s", line) and block:
                yield " ".join(block); block = [line]
            else:
                block.append(line)
        if block:
            yield " ".join(block)
    for line in re.split(r"\n|(?<=[.!;])\s+", body):
        yield line


def values_about(text, anch):
    """{(anchor, kind, facet): {value: sentence}} — the anchor is part of the key, so two
    sentences are only ever compared when they name the SAME subject word."""
    out = {}
    for sent in units(text):
        low = sent.lower()
        hit = [a for a in anch if a in low]
        if not hit:
            continue
        for kind, rx in VALUE_RE:
            for m in re.finditer(rx, sent):
                f = facet(sent, m.start())
                for a in hit:
                    if a in (kind, kind.rstrip("s")):   # the unit is not the subject
                        continue
                    out.setdefault((a, kind, f), {}).setdefault(
                        m.group(1).replace(",", ""), " ".join(sent.split())[:150])
    return out


def contradictions(notes):
    """notes: {name: (text, tags, {urls})} -> candidate rows. Reports, never edits: a value
    pair can be a legitimate dated range ("MIT through v7, Apache-2.0 from v8")."""
    hits, names = [], sorted(notes)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = notes[a][2] & notes[b][2]
            if not shared:
                continue
            anch = set().union(*(anchors(u, notes[a][1], notes[b][1]) for u in shared))
            if not anch:
                continue
            va, vb = values_about(notes[a][0], anch), values_about(notes[b][0], anch)
            for key in set(va) & set(vb):
                sa, sb = set(va[key]), set(vb[key])
                if sa != sb and not (sa & sb):
                    anchor, kind, f = key
                    hits.append((kind, f, anchor, a, b, tuple(sorted(sa)), tuple(sorted(sb)),
                                 list(va[key].values())[0], list(vb[key].values())[0]))
    # the same finding surfaces once per anchor that matched; keep the most specific anchor
    best = {}
    for h in hits:
        k = (h[0], h[1], h[3], h[4], h[5], h[6])
        if k not in best or len(h[2]) > len(best[k][2]):
            best[k] = h
    return [(f"{h[0]}/{h[1]} about {h[2]!r}", h[3], h[4], list(h[5]), list(h[6]), h[7], h[8])
            for h in sorted(best.values())]


def main():
    a = sys.argv[1:]
    if not a or a[0] == "build":
        return build()
    if not DB.exists():
        build()
    cmd, rest = a[0], " ".join(a[1:])
    if cmd == "find":
        rows = q("""SELECT c.kind, c.path, c.heading, c.line, c.chars,
                    snippet(chunk_fts, 1, '>>', '<<', '…', 14)
                    FROM chunk_fts JOIN chunk c ON c.id = chunk_fts.rowid
                    WHERE chunk_fts MATCH ? ORDER BY bm25(chunk_fts) LIMIT 12""", (match(rest),))
        print(f"{len(rows)} sections match {rest!r}\n")
        for kind, path, heading, line, chars, snip in rows:
            print(f"  [{kind}] {path}:{line}  §{heading}   [{chars} chars ≈ {chars//4} tokens]")
            print(f"      {' '.join(snip.split())}\n")
    elif cmd == "read":
        rows = q("SELECT path,heading,line,chars,body FROM chunk WHERE heading LIKE ? ORDER BY chars LIMIT 1", (f"%{rest}%",))
        for path, heading, line, chars, body in rows:
            total = q("SELECT chars FROM doc WHERE path=?", (path,))[0][0]
            print(f"{path}:{line}  §{heading}\n[{chars} chars ≈ {chars//4} tokens — the whole file is {total:,} ≈ {total//4:,}, so this is {100*chars//max(total,1)}%]\n\n{body}")
        if not rows:
            print("no section with that heading")
    elif cmd == "stale":
        days = int(rest or 30)
        # No status filter: it was `status='verified'`, which all 44 notes said, so it scoped
        # nothing. A page we cannot re-derive is MORE urgent to re-read when stale, not less.
        rows = q("""SELECT path, fetched_max FROM doc WHERE kind='note'
                    AND fetched_max IS NOT NULL AND julianday('now') - julianday(fetched_max) > ?
                    ORDER BY fetched_max""", (days,))
        print(f"{len(rows)} notes with no fetch newer than {days} days")
        for p, d in rows: print(f"  {d}  {p}")
    elif cmd == "links":
        notes = {r[0] for r in q("SELECT path FROM doc WHERE kind='note'")}
        names = {pathlib.Path(p).stem for p in notes}
        dangling = q("SELECT src,dst FROM link WHERE dst NOT IN (SELECT DISTINCT src FROM link) ")
        dangling = [(s, d) for s, d in dangling if d not in names]
        oneway = q("SELECT a.src,a.dst FROM link a LEFT JOIN link b ON a.src=b.dst AND a.dst=b.src WHERE b.src IS NULL")
        oneway = [(s, d) for s, d in oneway if d in names]
        asserted = q("SELECT src,dst FROM link WHERE context='(related: frontmatter only)'")
        nowhere = unargued(q("SELECT src,dst,context FROM link"))
        reciprocal = [e for e in asserted if tuple(e) not in {tuple(x) for x in nowhere}]
        total = q("SELECT COUNT(*) FROM link")[0][0]
        print(f"{len(dangling)} dangling wikilinks; {len(oneway)} one-way links (rule: neighbours name each other); "
              f"{len(asserted)} of {total} edges are a bare related: line — {len(reciprocal)} the reciprocal half of an "
              f"edge argued at the other end, {len(nowhere)} ({len({frozenset(e) for e in nowhere})} pairs) argued at neither end")
        for s, d in sorted({tuple(sorted(e)) for e in nowhere}): print(f"  unargued  {s} <-> {d}")
        for s, d in dangling: print(f"  dangling  [[{d}]]  in {s}")
        for s, d in oneway[:40]: print(f"  one-way   {s} -> {d}")
    elif cmd == "path":
        a, b = a[1], a[2]
        edges = q("SELECT src,dst,context FROM link")
        nb = {}
        for s_, d_, c_ in edges:
            nb.setdefault(s_, []).append((d_, c_, "->")); nb.setdefault(d_, []).append((s_, c_, "<-"))
        prev = {a: None}; frontier = [a]
        while frontier and b not in prev:
            nxt = []
            for n in frontier:
                for m, c, dirn in nb.get(n, []):
                    if m not in prev:
                        prev[m] = (n, c, dirn); nxt.append(m)
            frontier = nxt
        if b not in prev:
            print(f"no wikilink path from {a} to {b} (the graph has {len(nb)} nodes); try `cooccur`")
        else:
            hops = []; n = b
            while prev[n]: p_, c, dirn = prev[n]; hops.append((p_, dirn, n, c)); n = p_
            print(f"{len(hops)} hop(s) from {a} to {b}:\n")
            for p_, dirn, n_, c in reversed(hops):
                print(f"  {p_} {dirn} {n_}\n      \"{c}\"\n")
    elif cmd == "explain":
        n = a[1]
        out = q("SELECT dst,context FROM link WHERE src=?", (n,))
        inn = q("SELECT src,context FROM link WHERE dst=?", (n,))
        print(f"{n}: {len(out)} outgoing, {len(inn)} incoming\n")
        for d, c in out: print(f"  -> {d}\n      \"{c}\"")
        for s_, c in inn: print(f"  <- {s_}\n      \"{c}\"")
    elif cmd == "shared":
        n = a[1]
        rows = q("SELECT b.note, a.url FROM source a JOIN source b ON a.url=b.url AND a.note<>b.note WHERE a.note=? ORDER BY b.note", (n,))
        print(f"{len(rows)} note(s) cite a source {n} also cites:")
        for m, u in rows: print(f"  {m}   ({u})")
    elif cmd == "cooccur":
        t1, t2 = a[1], a[2]
        rows = q("""SELECT c.kind, c.path, c.heading, c.chars FROM chunk c
                    WHERE c.id IN (SELECT rowid FROM chunk_fts WHERE chunk_fts MATCH ?)
                      AND c.id IN (SELECT rowid FROM chunk_fts WHERE chunk_fts MATCH ?)
                    ORDER BY c.chars LIMIT 20""", (match(t1), match(t2)))
        print(f"{len(rows)} section(s) mention both {t1!r} and {t2!r}:")
        for k, p_, h, ch in rows: print(f"  [{k}] {p_}  §{h}  [{ch} chars]")
    elif cmd == "lint":
        # The deterministic third of an LLM-wiki lint (Karpathy's gist: contradictions,
        # stale claims, orphan pages, missing cross-references, data gaps). What a script
        # can settle is settled here, tiered; judgement (contradictions, duplicates) is
        # the kb-curator agent's, which reads this output first. --json for the agent.
        import json as _json
        as_json = "--json" in a
        REQ = ("title", "tags", "related")
        # `status` was dropped from REQ on 2026-09-12. It was asserted in every note and said
        # `verified` in all 44 - a cardinality of one - while four of those notes rested on a
        # primary nobody could open. It is now DERIVED (see derive_status) and reported below.
        fm_values = collections.defaultdict(list)
        notes = {r[0] for r in q("SELECT path FROM doc WHERE kind='note'")}
        names = {pathlib.Path(p).stem: p for p in notes}
        index_txt = (ROOT / "knowledge" / "INDEX.md").read_text(encoding="utf-8") if (ROOT / "knowledge" / "INDEX.md").exists() else ""
        errors, warnings, info = [], [], []
        incoming = {d: 0 for d in names}
        for s_, d_ in q("SELECT src,dst FROM link"):
            if d_ in incoming: incoming[d_] += 1
        # Each note's NEWEST declared fetch, for the compiled-page check below. Built in the
        # pre-pass because a compiled page is judged against notes the per-note loop has not
        # reached yet -- computing it inside the loop would make the verdict depend on file order.
        newest_fetch = {}
        for st_, pa_ in names.items():
            d_ = re.findall(r"fetched:\s*(\d{4}-\d{2}-\d{2}[a-z]?)",
                            frontmatter(pathlib.Path(ROOT / pa_).read_text(encoding="utf-8"))[2])
            if d_: newest_fetch[st_] = max(d_)
        for stem, path in sorted(names.items()):
            text = pathlib.Path(ROOT / path).read_text(encoding="utf-8")
            meta, body, rawfm = frontmatter(text)
            if not rawfm:
                errors.append((path, "schema", "no frontmatter block")); continue
            for k in REQ:
                if not re.search(rf"^{k}:", rawfm, re.M):
                    errors.append((path, "schema", f"missing frontmatter key {k}"))
            for k_, v_ in re.findall(r"^([a-z_]+):[ \t]*(\S.*)$", rawfm, re.M):
                fm_values[k_].append(v_.strip())
            srcs = re.findall(r"^\s*-\s*(?:url|path):\s*(\S+)", rawfm, re.M)
            fetched = re.findall(r"^\s*fetched:\s*(\S+)", rawfm, re.M)
            has_note_src = bool(re.search(r"^\s*-\s*note:", rawfm, re.M))
            # unconditional since 2026-09-12: this used to be gated on `status == "verified"`,
            # which every note said, so the gate never excluded anything.
            if not srcs and not has_note_src:
                errors.append((path, "schema", "no sources block (url, path or note)"))
            elif not srcs and has_note_src:
                info.append((path, "schema", "sources are note-only: nothing retrievable to re-derive the page from"))
            # The raw JOIN KEY. Reviewed 2026-09-04: a note's frontmatter carried url and
            # fetched but never the path of the raw copy, so "keep the raw" could not be
            # checked and the raw could not be found from the note that needs it. Three
            # defensible ways to measure coverage returned 11%, 61% and 0% - the spread was
            # the finding. The field is required to be PRESENT, not to be non-empty: an
            # honest "none - fetched before the raw layer existed" is a valid answer and a
            # silent absence is not.
            # unconditional since 2026-09-12, for the same reason as the sources check above.
            if srcs and not re.search(r"^raw:", rawfm, re.M):
                errors.append((path, "raw", "no raw: key - name the raw copy's path, or say in "
                                            "one clause why none exists"))
            rawval = (re.search(r"^raw:\s*(.+)$", rawfm, re.M) or [None, ""])[1].strip()
            if rawval.startswith("knowledge/raw/") and not (ROOT / rawval.split()[0]).exists():
                errors.append((path, "raw", f"raw: points at {rawval.split()[0]} which does not exist"))
            if srcs and len(fetched) < len([u for u in srcs if u.startswith("http")]):
                warnings.append((path, "schema", f"{len(srcs)} source(s), {len(fetched)} fetched: date(s) - a URL without a fetch date cannot be judged stale"))
            # A REPEATED verdict means, per pipeline/contracts/claims.contract.json, "the source
            # restates a finding measured by someone ELSE". A line that gives a sample size but
            # names no other measurer is usually our own observation wearing a provenance label
            # for a confidence job - four such lines were found and corrected on 2026-09-04, and
            # the cost was concrete: a verification queue ranked on REPEATED counts sent a reader
            # after work that did not exist. Attribution words keep a source's OWN sample size
            # ("the paper reports n=400") from tripping this.
            for m in re.finditer(r"^.*\bREPEATED\b.*$", text, re.M):
                if verdict_suspect(m.group(0)):
                    warnings.append((path, "verdict", "REPEATED with a sample size but no other "
                                    "measurer named - is this our own measurement? (contract: "
                                    "REPEATED restates someone else's finding)"))
            for m in re.finditer(r"\[\[([^\]|#]+)", text):
                t = m.group(1).strip()
                if t not in names:
                    errors.append((path, "link", f"dangling [[{t}]]"))
            # A compiled page's inputs are other notes, so no watcher and no URL check can see
            # them move. `compiled_from:` is the join key that makes it checkable.
            if re.search(r"^compiled_from:", rawfm, re.M):
                snap = dict(re.findall(r"^\s+-\s+([a-z0-9._-]+):\s*(\d{4}-\d{2}-\d{2}[a-z]?)\s*$",
                                       rawfm.split("compiled_from:", 1)[1], re.M))
                own = (re.search(r"^fetched:\s*(\d{4}-\d{2}-\d{2}[a-z]?)", rawfm, re.M) or [None, ""])[1]
                moved = compiled_stale(own, snap, newest_fetch)
                for name, was, now in moved:
                    warnings.append((path, "compiled", f"input {name} now declares {now}, "
                                     f"was {was} when this page was compiled ({own}) - the "
                                     f"page is a view over notes that have moved on"))
            if f"[[{stem}]]" not in index_txt:
                warnings.append((path, "index", "not listed in knowledge/INDEX.md"))
            if incoming.get(stem, 0) == 0:
                warnings.append((path, "orphan", "no other note links here"))
            # Two populations were being reported as one. This repo REQUIRES a new note's
            # neighbours to name it back, so the reciprocal half of an argued edge is asserted
            # by design: the sentence exists, it just lives in the note that owns the relation.
            # Reporting both together put 212 edges on one queue when 134 were the debt — the
            # same mistake the REPEATED verdict made on 2026-09-04, one layer up.
            rel_only = q("SELECT COUNT(*) FROM link l WHERE l.src=? AND l.context='(related: frontmatter only)'"
                         " AND NOT EXISTS (SELECT 1 FROM link b WHERE b.src=l.dst AND b.dst=l.src"
                         "                 AND b.context NOT LIKE '(related:%')", (stem,))[0][0]
            if rel_only:
                info.append((path, "related-only", f"{rel_only} related: edge(s) argued at NEITHER end"))
        oneway = q("SELECT a.src,a.dst FROM link a LEFT JOIN link b ON a.src=b.dst AND a.dst=b.src WHERE b.src IS NULL")
        for s_, d_ in oneway:
            if d_ in names:
                warnings.append((names[s_] if s_ in names else s_, "one-way", f"{s_} -> {d_}: {d_} does not name {s_} back"))
        stale = q("""SELECT path, fetched_max FROM doc WHERE kind='note'
                    AND fetched_max IS NOT NULL AND julianday('now') - julianday(fetched_max) > 90""")
        for p_, d_ in stale:
            warnings.append((p_, "stale", f"no fetch newer than 90 days (last {d_})"))
        # judgement candidates: pairs the curator reads first
        pairs = q("""SELECT a.note, b.note, a.url FROM source a JOIN source b ON a.url=b.url AND a.note<b.note
                     WHERE a.url LIKE 'http%' ORDER BY a.note""")
        for f_, v_, n_ in single_valued(fm_values):
            info.append(("(all notes)", "cardinality",
                         f"frontmatter field {f_!r} holds one value ({v_!r}) across {n_} notes "
                         f"- a redundant field or an unenforced one"))
        repro = q("SELECT status, COUNT(*) FROM doc WHERE kind='note' GROUP BY status")
        info.append(("(all notes)", "derived-status",
                     " · ".join(f"{k}: {v}" for k, v in repro) +
                     " (derived from the raw layer, not asserted)"))
        report = {"notes": len(names), "errors": errors, "warnings": warnings, "info": info,
                  "contradiction_candidates": [{"a": x, "b": y, "shared_source": u} for x, y, u in pairs]}
        if as_json:
            print(_json.dumps(report, indent=1, ensure_ascii=False))
        else:
            print(f"lint over {len(names)} notes: {len(errors)} error(s), {len(warnings)} warning(s), {len(info)} info, "
                  f"{len(pairs)} note pair(s) sharing a source — run `kb.py contradictions` over them)")
            for tier, rows in (("ERROR", errors), ("WARN", warnings), ("INFO", info)):
                for p_, kind, msg in rows: print(f"  {tier:<5} {kind:<12} {p_}: {msg}")
        sys.exit(1 if errors else 0)
    elif cmd == "contradictions":
        notes = {}
        for f in sorted((ROOT / "knowledge/notes").glob("*.md")):
            t = f.read_text(encoding="utf-8", errors="replace")
            _, _, fm = frontmatter(t)
            tagline = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
            tags = [x.strip().strip("\"'") for x in tagline.group(1).split(",")] if tagline else []
            urls = {u.rstrip('.,;)"\'') for u in re.findall(r"https?://\S+", fm)}
            notes[f.stem] = (t, tags, urls)
        hits = contradictions(notes)
        print(f"{len(hits)} candidate contradiction(s) over {len(notes)} notes "
              f"(same typed value, shared source, shared subject — a human decides)")
        for kind, a, b, va, vb, qa, qb in hits:
            print(f"\n  {kind}: {a} says {va}, {b} says {vb}")
            print(f"    {a}: {' '.join(qa.split())}")
            print(f"    {b}: {' '.join(qb.split())}")
        sys.exit(0)
    elif cmd == "check":
        # The routine, as ONE command. A routine you have to remember in four parts is four
        # chances to skip one; this is what CI runs and what a curator runs before committing.
        import subprocess
        rc = 0
        for step in (["build"], ["lint"], ["contradictions"], ["owners"], ["selftest"]):
            print(f"\n=== kb.py {step[0]} " + "=" * (60 - len(step[0])))
            r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve())] + step)
            rc = rc or r.returncode
        print(f"\n=== check: {'PASS' if rc == 0 else 'FAIL'}")
        sys.exit(rc)
    elif cmd == "owners":
        # The blind spot the byte-watcher cannot see. A project that changes hands keeps its old
        # URL working - GitHub follows the transfer and serves byte-identical content - so no
        # fetch fails and no hash moves. What DOES move is the project's own links: badges, CI
        # URLs and install lines start naming the new org. This reads the READMEs already stored
        # in the raw layer and reports where a project's own links disagree with the owner we
        # cite. Offline, no API (the session's GitHub access is scoped to its own repos anyway).
        # A hit is a candidate, not a verdict: 4-of-4 links is evidence, 1-of-1 is a mention.
        base = ROOT / "knowledge" / "raw"
        # "The owner we cite" is the owner of the MOST RECENTLY fetched stored README for a
        # repo, not every one ever stored. Once a move is settled by re-fetching at the new
        # address, the old baseline stays in the raw layer forever (nothing there is deleted),
        # and judging it too would report a finding that has already been acted on - a check
        # that cannot be satisfied is one people learn to ignore. Recency comes from WATCH.tsv.
        fetched = {}
        tsv = base / "WATCH.tsv"
        if tsv.exists():
            for line in tsv.read_text().splitlines():
                c = line.split("\t")
                if len(c) >= 3:
                    fetched[c[0]] = c[2]
        entries = []
        for f in sorted(base.rglob("raw.githubusercontent.com_*README.md.md")):
            m = re.match(r"raw\.githubusercontent\.com_([^_]+)_(.+?)_HEAD_README", f.name)
            if m:
                entries.append((m.group(2), fetched.get(str(f.relative_to(ROOT)), ""), f))
        rows = []
        for f in sorted(newest_per_repo(entries).values(), key=lambda x: x.name):
            m = re.match(r"raw\.githubusercontent\.com_([^_]+)_(.+?)_HEAD_README", f.name)
            owner, repo = m.group(1), m.group(2)
            txt = f.read_text(encoding="utf-8", errors="replace")
            hits = [(o, self_link_live(tail)) for o, r, tail in
                    re.findall(r"github\.com/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)(\S*)", txt)
                    if r.rstrip(".git") == repo]
            seen = collections.Counter(o for o, _ in hits)
            live = collections.Counter(o for o, is_live in hits if is_live)
            if not seen:
                continue
            top, n = seen.most_common(1)[0]
            if top.lower() != owner.lower():
                rows.append((owner, repo, top, n, sum(seen.values()), live[top],
                             str(f.relative_to(ROOT))))
        print(f"{len(rows)} project(s) whose own README names a different owner than we cite")
        for owner, repo, top, n, tot, nlive, path in rows:
            print(f"\n  we cite {owner}/{repo}")
            print(f"    its README names {top}/{repo} in {n} of {tot} self-links, "
                  f"{nlive} of them LIVE (actions/releases/blob/... - they 404 at a wrong address)")
            verdict = ("the README is maintained THERE; our citation is the stale one" if nlive
                       else "inert links only (a clone line, a homepage): a leftover, not a move")
            print(f"    -> {verdict}")
            print(f"    baseline: {path}")
        if rows:
            print("\nA hit is a candidate for a human. An ownership move keeps the old URL alive,")
            print("so nothing fails and no hash changes - which is why this check exists at all.")
            print("The LIVE count is the discriminator: measured 2026-09-08, two hits with the same")
            print("shape (1-of-1 and 4-of-4) had OPPOSITE verdicts, decided entirely by link kind.")
        sys.exit(0)
    elif cmd == "sql":
        for r in q(rest): print("  " + " | ".join(str(x) for x in r))
    elif cmd == "selftest":
        build()
        hit = q("SELECT COUNT(*) FROM chunk_fts WHERE chunk_fts MATCH ?", (match("commodity by reference"),))[0][0]
        slash = q("SELECT COUNT(*) FROM chunk_fts WHERE chunk_fts MATCH ?", (match("WHICH/HOW split"),))[0][0]
        raw = q("SELECT COUNT(*) FROM chunk WHERE kind='raw' AND path LIKE '%0013-commodity%'")[0][0]
        intake = q("SELECT COUNT(*) FROM chunk WHERE kind='intake' AND heading LIKE '%State%'")[0][0]
        miss = q("SELECT COUNT(*) FROM chunk_fts WHERE chunk_fts MATCH ?", ('"zq7planted9nonsense"',))[0][0]
        # contradictions: a planted conflict must be CAUGHT, and two legitimate shapes must not
        fx = {
            "a": ("---\ntags: [toolx]\nsources:\n  - url: https://pypi.org/project/toolx/\n---\n"
                  "toolx is MIT.\n", ["toolx"], {"https://pypi.org/project/toolx/"}),
            "b": ("---\ntags: [toolx]\nsources:\n  - url: https://pypi.org/project/toolx/\n---\n"
                  "toolx is Apache-2.0.\n", ["toolx"], {"https://pypi.org/project/toolx/"}),
            # a dated range names BOTH values, so it must not read as a conflict
            "c": ("---\ntags: [toolx]\nsources:\n  - url: https://pypi.org/project/toolx/\n---\n"
                  "toolx was MIT through v7 and is Apache-2.0 from v8.\n", ["toolx"],
                  {"https://pypi.org/project/toolx/"}),
            # a measured value against a stated cap is not a conflict either
            "d": ("---\ntags: [toolx]\nsources:\n  - url: https://pypi.org/project/toolx/\n---\n"
                  "toolx bodies are under 500 lines.\n", ["toolx"],
                  {"https://pypi.org/project/toolx/"}),
            "e": ("---\ntags: [toolx]\nsources:\n  - url: https://pypi.org/project/toolx/\n---\n"
                  "toolx measured 485 lines.\n", ["toolx"], {"https://pypi.org/project/toolx/"}),
        }
        pairs = lambda *k: [h for h in contradictions({n: fx[n] for n in k})]
        caught = len(pairs("a", "b")) == 1
        range_ok = pairs("a", "c") == [] and pairs("b", "c") == []
        facet_ok = pairs("d", "e") == []
        v_flag = verdict_suspect("well inside the guardrail. **REPEATED**, 3 batches per arm.")
        v_flag2 = verdict_suspect("Check membership, never position. **REPEATED**, n=3, every run.")
        v_ok = not verdict_suspect("the paper reports n=400 participants. **REPEATED**.")
        v_ok2 = not verdict_suspect("MMLU-Pro 85.2 on its model card. **MEASURED**, n=3.")
        # edges: the reciprocal half of an argued edge must NOT be reported as debt, an edge
        # argued at neither end MUST be, and a source-note mention counts as argued.
        e_body = edge_context("x", {"x"}, {"x"}, {"x"}) is None
        e_note = edge_context("x", set(), set(), {"x"}) == "(related: explained in a source note)"
        e_bare = edge_context("x", set(), {"x"}, {"x"}) == "(related: frontmatter only)"
        F, B = "(related: frontmatter only)", "b argues a here"
        e_recip = unargued([("a", "b", B), ("b", "a", F)]) == []
        e_dead = unargued([("a", "b", F), ("b", "a", F)]) == [("a", "b"), ("b", "a")]
        edges_ok = e_body and e_note and e_bare and e_recip and e_dead
        # owners: a link the maintainers must keep working vs one that can rot unnoticed
        o_live = all(self_link_live(s) for s in
                     ("/actions/workflows/ci.yml", "/releases/download/stable/x.sh",
                      "/blob/main/GOVERNANCE.md", "/tree/main/crates"))
        o_inert = not any(self_link_live(s) for s in ("", ".git", "/", "#readme"))
        # and the newest stored README per repo wins: a settled move must stop being reported
        o_newest = (newest_per_repo([("goose", "2026-09-04", "old"),
                                     ("goose", "2026-09-08", "new")]) == {"goose": "new"})
        owners_ok = o_live and o_inert and o_newest
        # the check on the check: every area kb.py indexes must be a CI trigger path
        wf = ROOT / ".github" / "workflows" / "kb-check.yml"
        if wf.exists():
            block = re.search(r"push:\s*\n\s*paths: \[(.*?)\]", wf.read_text(), re.S)
            wf_paths = re.findall(r"'([^']+)'", block.group(1)) if block else []
            ci_gap = uncovered_areas(list(AREAS.values()), wf_paths)
        else:
            ci_gap, wf_paths = [], ["(no workflow)"]
        # and the predicate itself must be able to fail
        ci_ok = not ci_gap and uncovered_areas(["intake/**/*.md"], ["knowledge/**"]) == ["intake/**/*.md"]
        # derived status: held sources make a page reproducible; cited-only must NOT read as
        # reproducible, and a page with no retrievable source is neither.
        ds_repro = derive_status(3, 1) == "reproducible"
        ds_cited = derive_status(3, 0) == "cited-only"
        ds_none = derive_status(0, 0) == "note-only"
        ds_partial = derive_status(9, 1) == "reproducible"   # one held copy is enough to re-derive FROM
        status_ok = ds_repro and ds_cited and ds_none and ds_partial
        # The REGEX behind those counts needs its own fixture, because derive_status takes
        # numbers and cannot see how they were produced. A mutation loosening this pattern to
        # match any mention of the path survived the whole suite until this was added - the
        # "predicates tested, wiring untested" shape, one directive after it was written down.
        _fm_fx = ('---\ntitle: t\nsources:\n  - url: https://x/\n    fetched: 2026-09-01\n'
                  'raw:\n  - knowledge/raw/dir-2026-09-01/x.html\n'
                  '  - "baseline only, NOT what was read: knowledge/raw/other/y.html"\n'
                  '---\nbody\n')
        _fm_meta, _, _ = frontmatter(_fm_fx)
        # one real bullet, one prose line that merely NAMES a raw path: held must be 1, not 2.
        held_ok = _fm_meta["held"] == 1 and _fm_meta["status"] == "reproducible"
        # the cardinality check: a field everyone agrees on fires, a varying one does not, and
        # a field with a single NOTE is not a corpus-wide agreement.
        sv = single_valued({"status": ["verified"] * 4, "tags": ["a", "b", "a"],
                            "lang": ["sv"], "opt": [None, "x", None, "x"],
                            "ghost": [None, None, None]})
        sv_names = [f for f, _, _ in sv]
        # status (everyone agrees) and opt (everyone who sets it agrees) fire; a VARYING field,
        # a field only ONE note carries, and a field NOBODY sets must all be spared - the last
        # because "nobody uses this" is a different finding from "everybody agrees".
        card_ok = (sv_names == ["opt", "status"] and "tags" not in sv_names
                   and "lang" not in sv_names and "ghost" not in sv_names)
        ok = (hit > 0 and raw > 0 and intake > 0 and miss == 0 and slash > 0
              and caught and range_ok and facet_ok and v_flag and v_flag2 and v_ok and v_ok2
              and edges_ok and owners_ok and ci_ok and status_ok and card_ok and held_ok)
        print(f"selftest: raw ADR findable={hit>0} slash query ok={slash>0} raw chunks={raw} intake State sections={intake} planted miss={miss==0}")
        print(f"          verdict misuse: our-own-n flagged={v_flag and v_flag2} source-own-n spared={v_ok and v_ok2}")
        print(f"          edges: reciprocal spared={e_recip} argued-nowhere caught={e_dead} source-note argued={e_note}")
        print(f"          owners: live self-link detected={o_live} inert one spared={o_inert} newest fetch wins={o_newest}")
        print(f"          ci: {len(AREAS)} indexed areas, {len(wf_paths)} trigger paths, "
              f"uncovered={ci_gap or 'none'}")
        print(f"          derived status: reproducible={ds_repro} cited-only={ds_cited} "
              f"note-only={ds_none} one-held-is-enough={ds_partial} prose-mention-not-held={held_ok}")
        print(f"          cardinality: single-valued caught={card_ok} (varying field spared, "
              f"one-note field spared)")
        # compiled-page freshness. A page derived from other pages has no external source to
        # watch; these fixtures pin what "moved on" means, in both directions.
        c_moved = compiled_stale("2026-09-02", {"a": "2026-09-02"}, {"a": "2026-09-08"})
        c_same  = compiled_stale("2026-09-02", {"a": "2026-09-02"}, {"a": "2026-09-02"})
        # An input rewritten WITHOUT a newer declared fetch is not stale by this test, and
        # saying so is the honest limit: the check reads declared dates, not content.
        c_older = compiled_stale("2026-09-02", {"a": "2026-09-02"}, {"a": "2026-08-30"})
        # An input that moved but only up to the page's OWN date is not behind the page.
        c_eq    = compiled_stale("2026-09-08", {"a": "2026-09-02"}, {"a": "2026-09-08"})
        # An input named in the snapshot that no longer exists must not crash or fire.
        c_gone  = compiled_stale("2026-09-02", {"a": "2026-09-02"}, {})
        c_ok = (len(c_moved) == 1 and c_moved[0][0] == "a" and not c_same and not c_older
                and not c_eq and not c_gone)
        ok = ok and c_ok
        print(f"          compiled: input moved caught={len(c_moved)==1} unchanged spared={not c_same} "
              f"older-input spared={not c_older} at-page-date spared={not c_eq} missing-input spared={not c_gone}")
        print(f"          contradictions: planted conflict caught={caught} dated range not flagged={range_ok} limit-vs-measured not flagged={facet_ok} -> {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
