Every wikilink resolves, every note is indexed, `model-prices` ↔ `prompt-caching` remains mutual.

**Files changed**

- **`wiki/notes/local-models.md`** — treated as an *update-with-conflict*, not an overwrite. Status `verified` → `disputed`; new source added to frontmatter. Added a claims table with verbatim quote, locator and verdict per claim, holding **both** parameter figures as dated rows: 744B (README, 2026-08-25) and 753B (model card, 2026-09-02). Both grade **REPEATED** — neither source states a measurement method — so recency and officialness don't settle it; the note says what would (a vendor parameter table with a stated counting convention, or summed tensor shapes). New material captured: active parameters 40B, context 1M tokens. The 245 GB 2-bit memory tier is unchanged, so the tier itself doesn't move either way.
- **`wiki/raw/2026-09-02-gamma-model-card.md`** (new) — unedited copy of the source, so the quotes stay re-readable.
- **`wiki/raw/MANIFEST.md`** (new) — started the raw layer: origin URL, fetch date, sha256, target note. Records that the three earlier sources predate this layer and have no kept bytes.
- **`wiki/SOURCES.md`** — one row for the new source, pointing at its raw file.
- **`wiki/INDEX.md`** — `local-models` row flagged `status: disputed`; pointer to `raw/`.
- **`wiki/LOG.md`** — ingest entry: triage verdict, the conflict and how it was held, new material, hash, and the hand-run lint result.

Two things worth flagging: the 744B row's verbatim line can't be recovered — the earlier ingest kept no raw — so that side of the dispute rests on the row alone. And I added **no** `related:` links; `model-prices` and `prompt-caching` never mention Gamma-7, so a back-link would have been an edge nobody argued.