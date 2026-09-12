Done. Triage was **update** — `model-prices` already owned the topic, so it was extended rather than a rival page created.

**Changed files**

- **`wiki/notes/model-prices.md`** — added the 2026-09 pricing page as a second source (with raw path and note). Beta 5 updated to $2.00 / $10.00 as of 2026-09-01, with the old $3 / $15 row kept as superseded; Alpha 5 stays $5.00 / $25.00, re-dated since the new page restates it. Added claim rows with the verbatim source lines and a **REPEATED** verdict each (vendor assertion, nothing measured), plus a note on what would make the prices wrong.
- **`wiki/raw/2026-09-02-pricing-page.md`** *(new)* — unedited copy of the source.
- **`wiki/raw/MANIFEST.md`** *(new)* — provenance row: URL, fetch date, sha256 `e4da3770…743530`.
- **`wiki/SOURCES.md`** — one row for the new source, feeding `model-prices`.
- **`wiki/LOG.md`** — one ingest line (what changed in the note) and one `no material` line for the caching multipliers.

**Not changed, deliberately:** `wiki/notes/prompt-caching.md` — the source's "10% of input / 125%" restates the 0.1x / 1.25x that note already carries with a dated source, so it's no material: no corroborating source entry, no claims row. `wiki/INDEX.md` is unchanged since no page was created. The existing `model-prices` ↔ `prompt-caching` back-link already carries a reason sentence on both ends, so the cascade step had nothing to close.

No lint script ships with this wiki; I checked by hand — no dangling or one-way links, all three notes listed in the index, frontmatter schema consistent.