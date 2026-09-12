Lint (manual — this wiki has no lint script): no dangling links, all three notes indexed, the one existing link pair (`model-prices` ↔ `prompt-caching`) is mutual. `local-models` names no neighbours, so no cascade was owed.

**Files changed**

- **`wiki/notes/local-models.md`** — triaged as **disputed**, not a new page. Status `verified` → `disputed`; the new source added to `sources`. The parameter conflict is kept as two dated claim rows (744B, README, 2026-08-25 / 753B, model card, 2026-09-02) rather than overwriting — the newer number is not promoted just for being newer. Added rows for active parameters (40B), context (1M tokens) and the 245 GB 2-bit figure, which corroborates what the note already held. Each row carries its verbatim line and a verdict (all **REPEATED** — the card asserts, it measures nothing). Added "what it means here" (use 245 GB; don't derive memory from a disputed count) and "still open" (which total is right, how to settle it, what would make the note wrong).
- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** *(new)* — unedited copy of the source.
- **`wiki/raw/MANIFEST.md`** *(new)* — raw-layer row: source URL, fetch date, sha256, destination note.
- **`wiki/INDEX.md`** — `local-models` entry annotated with the open dispute.
- **`wiki/SOURCES.md`** — row for `https://example.test/gamma-7-model-card`, 2026-09-02 → local-models.
- **`wiki/LOG.md`** — ingest entry recording the disputed verdict, the raw path and hash, and what changed.

One caveat worth flagging: the 2026-08-25 raw was never kept, so the 744B verbatim line can only be quoted as this note recorded it — I marked that in the row. Settling the dispute needs the README re-fetched.