#!/usr/bin/env python3
"""Shape grader for the llm-wiki-ingest tasks. Run over the wiki AFTER the ingest.
Every check is a fact about the files; no judgement. Prints one row per check and
exits 1 on any FAIL. Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>
"""
import re, sys, pathlib
wiki = pathlib.Path(sys.argv[1]); task = sys.argv[2]
notes = {p.stem: p.read_text(encoding="utf-8") for p in (wiki / "notes").glob("*.md")}
index = (wiki / "INDEX.md").read_text(encoding="utf-8")
log = (wiki / "LOG.md").read_text(encoding="utf-8") if (wiki / "LOG.md").exists() else ""
sources = (wiki / "SOURCES.md").read_text(encoding="utf-8")
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
if task == "T1":   # pricing page: UPDATE the owner, no rival page, dated row, quote-backed, sources+log rows
    check("no rival page", not any(s not in ("model-prices","prompt-caching","local-models") and "pric" in s for s in notes), str(sorted(notes)))
    mp = notes.get("model-prices","")
    check("beta price updated with date", re.search(r"Beta 5.*\$2(\.00)?.*\$10(\.00)?.*2026-09", mp, re.S) is not None)
    check("old price kept as history or superseded row", "$3" in mp and "$15" in mp)
    check("new source in note frontmatter with fetch date", "pricing-2026-09" in fm(mp) and "2026-09-02" in fm(mp))
    check("SOURCES row", "pricing-2026-09" in sources)
    check("LOG row", "pricing-2026-09" in log or "model-prices" in log.splitlines()[-1] if log.strip() else False)
    check("neighbour names owner back", "[[model-prices]]" in notes.get("prompt-caching",""))
elif task == "T2":  # contradiction: both values kept as rows, disputed marker, neither overwritten
    lm = notes.get("local-models","")
    check("both values present", "744B" in lm and "753B" in lm)
    check("disputed marker", re.search(r"disputed", lm, re.I) is not None)
    check("both sources dated", "2026-08-25" in lm and "2026-09-02" in lm)
    check("model card in frontmatter sources", "gamma-7-model-card" in fm(lm))
    check("SOURCES row", "gamma-7-model-card" in sources)
    check("LOG row", "gamma" in log.lower())
elif task == "T3":  # no material: nothing changed but the log
    pc = notes.get("prompt-caching","")
    check("prompt-caching unchanged", "writes 1.25x" in pc and "blog" not in fm(pc))
    check("no new note", set(notes) == {"model-prices","prompt-caching","local-models"}, str(sorted(notes)))
    check("LOG says no material", re.search(r"no material", log, re.I) is not None and "caching-explained" in log)
bad = [r for r in rows if not r[1]]
print(f"\n{len(rows)-len(bad)}/{len(rows)} checks pass")
sys.exit(1 if bad else 0)
