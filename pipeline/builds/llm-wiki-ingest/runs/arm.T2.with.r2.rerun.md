Manual lint (no lint script in this wiki): all three notes are listed in INDEX.md, the only wikilinks are the existing reciprocal `model-prices` ↔ `prompt-caching` pair, no dangling links, no orphans, frontmatter schema consistent. `local-models` names no neighbours, so there was no cascade to close — I didn't invent a `related:` edge the source doesn't support.

**Files changed**

- `wiki/raw/2026-09-02-gamma-7-model-card.md` — **new.** Unedited copy of the source, fetch date in the filename, sha256 recorded in the log.
- `wiki/notes/local-models.md` — status `verified` → **`disputed`**. The 753B and 744B totals are both kept as dated rows with their verbatim lines rather than one overwriting the other; both graded REPEATED, since neither source describes a measurement — so recency alone doesn't settle it. Added the card as a second source, plus new claims for active parameters (40B) and context (1M tokens). The 245 GB at 2-bit figure only restates what the note held, so it gained no rival row. Added an "still open" line naming the re-fetch that would resolve the dispute.
- `wiki/SOURCES.md` — one row for the consulted source (2026-09-02, feeds `local-models`).
- `wiki/LOG.md` — one entry: what was ingested, the disputed verdict, what changed on the page, and the raw's location and hash.

`wiki/INDEX.md` was left alone — `local-models` was already listed and its description still fits.