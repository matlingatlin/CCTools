Manual lint: no new pages, so INDEX is unchanged and complete; `[[model-prices]]` ↔ `[[prompt-caching]]` remain mutual; no dangling links introduced.

**Triage verdict: no material.** The blog restates the multipliers `prompt-caching` already holds (0.1x read, 1.25x write) and measures nothing, so it got no page of its own — a rival page would have been a lint error, and a second assertion doesn't promote a claim.

Files changed:

- **`wiki/notes/prompt-caching.md`** — added the blog as a second source in frontmatter (fetched 2026-09-02, noted as corroboration only) and a Claims table giving both sources a row with the blog's verbatim line, each graded REPEATED, plus a line saying what would make the claim wrong. No stated value changed.
- **`wiki/SOURCES.md`** — one row: 2026-09-02, the blog URL, feeding prompt-caching, marked corroboration only.
- **`wiki/LOG.md`** — one entry recording the ingest, the "no material" verdict, the raw file's path and fetch date, and what it did and did not change.

Unchanged: `wiki/INDEX.md` (no new page to list), `model-prices.md`, `local-models.md`.

One thing I left alone: `local-models.md` has an empty `related:` and no inbound links — an orphan predating this ingest. That's a wiki-wide cleanup for `kb-curator`, not something this source touches.