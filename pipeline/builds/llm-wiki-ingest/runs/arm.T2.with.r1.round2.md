Ingested as **disputed** — I did not overwrite 744B with 753B, since neither source says it supersedes the other.

Files changed:

- **`wiki/notes/local-models.md`** — `status: verified` → `disputed`; added the model card to `sources`; added a `## Claims` table carrying both parameter counts as dated rows (744B/2026-08-25 and 753B/2026-09-02, both marked disputed) plus the card's new facts (40B active, 1M context, 245 GB at 2-bit, which corroborates the existing figure); added "what it means here" and an "Open" section naming the unresolved count and the fact that the old README's raw was never kept.
- **`wiki/raw/2026-09-02-gamma-model-card.md`** *(new)* — verbatim copy of the source, unedited.
- **`wiki/raw/MANIFEST.md`** *(new)* — provenance row: URL, fetch date, SHA-256, size, page it feeds.
- **`wiki/SOURCES.md`** — one row for the consulted source (2026-09-02, gamma-7-model-card → local-models).
- **`wiki/LOG.md`** — operation line naming disposition (disputed), the URL, the page touched, and the by-hand lint result.
- **`wiki/INDEX.md`** — flagged local-models as disputed; listed the new `raw/` directory.

All claim quotes are verbatim from the raw with line locators, and each is graded REPEATED — the card asserts the numbers without showing a measurement. Manual lint (no lint script in this wiki): no dangling wikilinks, no unlisted notes, no orphans; raw byte-identical to the source. Two things worth your attention: the 744B claim's quote can't be re-verified because that README was never kept as raw, and the dispute is unresolved — if you know which source is authoritative, say so and I'll collapse it to a single verified row.