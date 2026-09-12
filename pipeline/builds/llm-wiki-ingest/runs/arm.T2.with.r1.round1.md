Done. Triage was **disputed** — the model card's 753B contradicts the wiki's 744B, so both values are kept as dated rows rather than one overwriting the other.

**Files changed**

- `wiki/notes/local-models.md` — status `verified` → `disputed`; the new model card added to `sources` with its fetch date and raw path; the parameter conflict written as a two-row dated table (744B README 2026-08-25 vs 753B model card 2026-09-02, both graded REPEATED — neither source measured); new claims from this card added with verbatim quotes (active 40B, 1M context, 245 GB at 2-bit, unchanged); "what it means here" notes the ~1.2% disagreement doesn't change the memory tier; open questions record what would resolve it.
- `wiki/raw/2026-09-02-gamma-7-model-card.md` — new, unedited copy of the source.
- `wiki/raw/MANIFEST.md` — new; provenance row with URL, fetch date, sha256.
- `wiki/SOURCES.md` — row for `https://example.test/gamma-7-model-card`, feeds into local-models.
- `wiki/LOG.md` — ingest line recording the disputed verdict, what was added, the raw hash, and the hand lint (no lint script here).

`wiki/INDEX.md` unchanged — no new page, and local-models was already listed.

Not resolved, deliberately: which parameter count is correct. Neither source states a counting method or a measurement, so picking one would be a guess; the page says what evidence would settle it.