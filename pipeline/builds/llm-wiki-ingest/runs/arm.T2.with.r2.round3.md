Done. The parameter conflict was a genuine contradiction between two asserting sources, so I took the **disputed** branch rather than overwriting 744B with 753B.

Files changed:

- **`wiki/notes/local-models.md`** — rewritten into the schema. `status: verified` → `disputed`; the new model card added to `sources`. Body now states the dispute plainly and carries a `## Claims` table (one row per claim: claim | source | locator | verbatim quote | verdict) with both parameter figures kept as dated rows marked disputed, plus 40B active, 1M context, and 245 GB at 2-bit. All five figures graded REPEATED — neither source shows a measurement. Added *what it means here* (245 GB is the figure that decides the memory tier, and both sources agree on it; the 1.2% parameter gap changes no tier) and *what is open* (which count is right; the 245 GB figure exceeds the ~188 GB of 2-bit weights by unexplained overhead; nothing from the raw left untaken).
- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** (new) — unedited copy of the source, made read-only.
- **`wiki/raw/MANIFEST.md`** (new) — provenance row: source URL, fetch date, size, page it feeds.
- **`wiki/SOURCES.md`** — one row for the consulted source, feeding `local-models`.
- **`wiki/INDEX.md`** — the `local-models` entry now flags its disputed status.
- **`wiki/LOG.md`** — operation line naming the disposition (disputed), the source URL, the pages touched, and the by-hand lint.

Two things I deliberately did not do: no cascade edits, because `local-models` names no neighbours and I could write no true sentence linking it to `model-prices` or `prompt-caching` — an invented edge is worse than none. And there's no lint script here, so I checked by hand (no dangling wikilinks, all three notes listed in INDEX). `local-models` is an orphan, but it was one before this ingest; that's a whole-wiki matter for `kb-curator`, noted in the log.