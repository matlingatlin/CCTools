**Triage verdict: no material.** The blog asserts exactly the multipliers `prompt-caching.md` already holds (0.1× read, 1.25× write), so no new page was created and nothing was added to the index — a restating source is recorded, not promoted.

Files changed:

- **`wiki/raw/2026-09-02-blog-restating-caching.md`** (new) — unedited copy of the source kept so the claim can be re-read after the URL rots.
- **`wiki/notes/prompt-caching.md`** — added the blog to `sources:` (url, fetched 2026-09-02, raw path, note that it restates); added a Claims table with the verbatim line `"Cache reads cost a tenth of the input price and writes cost 1.25 times."` graded **REPEATED**, alongside the existing source's row, and a sentence saying the values stay REPEATED because a claim isn't promoted by repetition, plus what would move it to MEASURED or to `disputed`. Values and `status: verified` unchanged.
- **`wiki/SOURCES.md`** — one row: `2026-09-02 | https://example.test/blog/caching-explained | prompt-caching (no material — corroborates only)`.
- **`wiki/LOG.md`** — entry recording the ingest as no-material, what was skipped (new page, index row, value/status change) and what was kept.

Unchanged: `wiki/INDEX.md` (no new page), `wiki/notes/model-prices.md` (the `prompt-caching` ↔ `model-prices` cascade is already two-way with a reason on each side). No lint script exists in this wiki; I checked by hand that every wikilink resolves, all three notes are listed in the index, and no orphan or rival page was introduced.