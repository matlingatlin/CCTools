Triage: **disputed** — the model card contradicts the note's parameter count, so both values are kept as dated rows rather than one overwriting the other. No lint script exists in this wiki; I checked by hand (all three notes listed in the index, no dangling or one-way wikilinks introduced).

Files changed:

- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** (new) — unedited copy of the source, sha256 `0bb6e3d4…65ecf0`.
- **`wiki/notes/local-models.md`** — status `verified` → `disputed`; added the model card as a second source with fetch date and raw hash; replaced the prose sentence with a claims table holding both parameter counts (744B from the 2026-08-25 README, 753B from the 2026-09-02 card, both **REPEATED** — neither measured), plus new claims for 40B active parameters and 1M context; added "what this means" (245 GB tier is unchanged and agreed by both sources, so sizing is unaffected) and "still open" (which count is right, and what would resolve it).
- **`wiki/SOURCES.md`** — row for `https://example.test/gamma-7-model-card`, 2026-09-02, feeding local-models.
- **`wiki/LOG.md`** — ingest line recording the disputed verdict, the two conflicting values, the new claims, and the raw path.
- **`wiki/INDEX.md`** — local-models entry flagged as parameter count disputed as of 2026-09-02.