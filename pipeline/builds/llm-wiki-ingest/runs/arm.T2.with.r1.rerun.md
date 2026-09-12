Done. Triage was **disputed**, not update — the model card's 753B and the note's 744B are both kept as dated rows rather than one overwriting the other.

**Files changed:**

- **`wiki/notes/local-models.md`** — rewritten in schema. Status `verified` → `disputed`. Second source added to frontmatter (model card, fetched 2026-09-02, pointing at its raw copy) with a note on each source saying which parameter count it gives. Body now carries a claims table: both parameter counts (744B / 753B) as separate dated rows with verbatim lines, plus three new claims from the card (40B active, 1M context, 245 GB at 2-bit). All five graded **REPEATED** — neither source measures anything, they assert. Added what it means here (245 GB is the operative planning figure; both sources agree on it, so the disagreement doesn't change which machines run it) and what's still open (which count is right; whether 245 GB was recomputed — 753B at 2 bits is ~188 GB of weights, so the figure carries unitemised overhead).
- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** (new) — unedited copy of the source, date in the filename.
- **`wiki/raw/MANIFEST.md`** (new) — provenance row: URL, fetch date, sha256, which note it feeds. The wiki had no raw layer; this creates one.
- **`wiki/SOURCES.md`** — one row for the consulted source, feeding local-models.
- **`wiki/LOG.md`** — one entry naming the URL, the `disputed` verdict, the 753B-vs-744B conflict, the new claims, and where the raw sits.
- **`wiki/INDEX.md`** — local-models line flagged with the open dispute so a reader sees it before opening the note.

No cascade edits were needed: local-models names no neighbours, and the existing `model-prices` ↔ `prompt-caching` pair is already two-way.

One deviation to flag: step 7 says run the wiki's deterministic lint, and this wiki ships none. I checked by hand instead — no dangling wikilinks, all three notes listed in INDEX, no one-way links, no orphans. That's weaker than a lint pass, so if this wiki is meant to be linted, it needs the script.