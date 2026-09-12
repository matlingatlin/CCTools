Done. Triage was **disputed** — the model card's parameter count contradicts what `local-models` held, so both values are kept as dated rows rather than one overwriting the other.

**Files changed**

- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** (new) — unedited copy of the source, sha256 `0bb6e3d4…65ecf0`.
- **`wiki/notes/local-models.md`** — status `verified` → `disputed`; model card added as a second source with fetch date, raw path and hash; prose replaced by a claims table carrying both parameter counts (744B, README, 2026-08-25 / 753B, model card, 2026-09-02) plus the new 40B active and 1M context claims, each with its verbatim line and a **REPEATED** verdict (neither source measures anything). Added what the dispute does and doesn't affect (245 GB tier unchanged; anything computed *from* the parameter count shifts ~1.2%) and what would settle it.
- **`wiki/INDEX.md`** — the `local-models` row now flags the dispute.
- **`wiki/SOURCES.md`** — row for `https://example.test/gamma-7-model-card`, 2026-09-02, feeding `local-models`.
- **`wiki/LOG.md`** — ingest entry naming the contradiction, the resolution, the new claims, the restated 245 GB figure, and the raw path + hash.

Two notes on judgement calls: the 245 GB figure is a restatement of what the note already held, so it added no new value — it appears only as the card's own quoted row, not as a revision. And I did not pick a winner on the parameter count; the note says prefer 753B if one number must be used (later, more official source) but leaves the question open, since the README hasn't been re-fetched.

No lint script ships with this wiki, so I checked by hand: every wikilink resolves, `model-prices` ↔ `prompt-caching` remain reciprocal, all three notes are indexed. `local-models` names no neighbours and the source introduced none, so there was nothing to cascade.