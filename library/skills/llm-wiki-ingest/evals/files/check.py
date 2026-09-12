#!/usr/bin/env python3
"""Shape grader for the llm-wiki-ingest tasks. Run over the wiki AFTER the ingest.
Every check is a fact about the files; no judgement. Prints one row per check and
exits 1 on any FAIL. Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>
"""
import re, sys, pathlib, json
wiki = pathlib.Path(sys.argv[1]); task = sys.argv[2]
notes = {p.stem: p.read_text(encoding="utf-8") for p in (wiki / "notes").glob("*.md")}
def _read(p): return p.read_text(encoding="utf-8") if p.exists() else ""
index = _read(wiki / "INDEX.md"); log = _read(wiki / "LOG.md"); sources = _read(wiki / "SOURCES.md")
rows = []
def check(name, ok, detail=""):
    rows.append((name, ok, detail)); print(f"{'PASS' if ok else 'FAIL'} {name} {detail if not ok else ''}")
def fm(t):
    m = re.match(r"---\n(.*?)\n---", t, re.S); return m.group(1) if m else ""
# common: schema on every note, no dangling links, every note in index
for stem, t in notes.items():
    f = fm(t)
    check(f"schema:{stem}", all(re.search(rf"^{k}:", f, re.M) for k in ("title","status","tags","related","sources")),
          "missing a required frontmatter key")
    for m in re.finditer(r"\[\[([^\]|#]+)", t):
        check(f"link:{stem}->{m.group(1)}", m.group(1).strip() in notes, "dangling")
    check(f"index:{stem}", f"[[{stem}]]" in index, "not in INDEX")
if task == "T1":   # pricing page: UPDATE the owner, no rival page, dated rows, quote+verdict on one claims row, sources+log rows
    check("no rival page (the note set is unchanged)", set(notes) == {"model-prices","prompt-caching","local-models"}, str(sorted(notes)))
    check("INDEX unchanged (no new row)", index.count("[[") == 3)
    mp = notes.get("model-prices","")
    beta_new = [l for l in mp.splitlines() if "Beta 5" in l and re.search(r"\$2(\.00)?\b", l) and re.search(r"\$10(\.00)?\b", l) and "2026-09" in l]
    check("beta price updated with date (a Beta 5 row carrying $2, $10 and a 2026-09 date)", bool(beta_new))
    beta_old = [l for l in mp.splitlines() if "Beta 5" in l and "$3" in l and "$15" in l and "2026-08-20" in l]
    check("old price kept as a dated superseded row (Beta 5, $3, $15, 2026-08-20 on one line)", bool(beta_old))
    check("and that row or its section is MARKED superseded/history/outdated", any(re.search(r"supersed|history|outdated|previous|old", l, re.I) for l in mp.splitlines() if "$3" in l and "$15" in l) or re.search(r"(supersed|history|outdated)[^\n]*\n(?:[^\n]*\n){0,6}[^\n]*Beta 5[^\n]*\$3", mp, re.I) is not None)
    claim_rows = [l for l in mp.splitlines() if l.strip().startswith("|") and re.search(r"MEASURED|REPEATED|DERIVED", l) and ("$2.00 per million input tokens" in l or "$10.00 per million output tokens" in l)]
    check("a claims-table row carries the verbatim raw quote AND a verdict word on the same line", bool(claim_rows))
    check("new source in note frontmatter with fetch date", "pricing-2026-09" in fm(mp) and "2026-09-02" in fm(mp))
    check("SOURCES row", "pricing-2026-09" in sources)
    check("LOG line names the source and the disposition", "pricing-2026-09" in log and re.search(r"update", log, re.I) is not None)
    check("neighbour names owner back", "[[model-prices]]" in notes.get("prompt-caching",""))
elif task == "T2":  # contradiction: both values as dated claim rows, disputed on the row and the page, neither overwritten
    lm = notes.get("local-models","")
    check("both values present", "744B" in lm and "753B" in lm)
    rows_ = [l for l in lm.splitlines() if l.strip().startswith("|")]
    check("a claims row carries 753B, the card's verbatim line and a verdict word", any("753B" in l and "Total parameters: 753B" in l and re.search(r"MEASURED|REPEATED|DERIVED", l) for l in rows_))
    check("a claims row carries 744B and a verdict word", any("744B" in l and re.search(r"MEASURED|REPEATED|DERIVED", l) for l in rows_))
    check("disputed marker on a row", any("disputed" in l.lower() for l in rows_))
    check("page status disputed", re.search(r"^status:\s*disputed", fm(lm), re.M) is not None)
    check("both sources dated", "2026-08-25" in lm and "2026-09-02" in lm)
    check("model card in frontmatter sources", "gamma-7-model-card" in fm(lm))
    check("SOURCES row", "gamma-7-model-card" in sources)
    check("LOG line names the card and the disposition", "gamma-7-model-card" in log and re.search(r"disputed", log, re.I) is not None)
elif task == "T3":  # no material: no page changed (hash of every note against the fixture), no page created, log and source-log rows
    import hashlib
    pristine = json.loads((pathlib.Path(__file__).resolve().parent / "pristine.sha256.json").read_text())
    for stem, before in pristine.items():
        after = hashlib.sha256(notes.get(stem, "").encode("utf-8")).hexdigest()
        check(f"{stem} byte-identical to the pristine hash shipped beside the grader", before == after)
    check("no new note", set(notes) == {"model-prices","prompt-caching","local-models"}, str(sorted(notes)))
    check("LOG says no material and names the source", re.search(r"no material", log, re.I) is not None and "caching-explained" in log)
    check("SOURCES row for the consulted source", "caching-explained" in sources)
bad = [r for r in rows if not r[1]]
print(f"\n{len(rows)-len(bad)}/{len(rows)} checks pass")
sys.exit(1 if bad else 0)
