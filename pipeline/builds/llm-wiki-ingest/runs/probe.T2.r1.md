Ingested. No page was overwritten — the conflict is recorded rather than resolved, since neither source was retracted.

**Files changed**

- `wiki/notes/local-models.md` — status `verified` → `disputed`; the new model card added to `sources` (with the raw file path and fetch date). The single 744B sentence is now a claim table holding **both** parameter counts as dated rows (744B README 2026-08-25 / 753B model card 2026-09-02), each with its verbatim line and a REPEATED verdict, plus three new claims from the card (40B active, 1M context, 245 GB at 2-bit). An "open" section says what would settle it, and notes that 245 GB is asserted, not derived — 753B at 2-bit is ~188 GB, so the memory figure carries unitemised overhead.
- `wiki/SOURCES.md` — row for `https://example.test/gamma-7-model-card`, 2026-09-02, feeding local-models.
- `wiki/LOG.md` — ingest entry naming the disputed outcome, the two values, and the status change.
- `wiki/INDEX.md` — local-models entry flagged with the open dispute so a reader hits it before opening the note.

Two things I did not do: I didn't pick 753B as the winner (the later, more authoritative document, but the README was never retracted — that's a call for you or a third source), and the note names no neighbours, so there was no cascade to close. `local-models` still has an empty `related:` and nothing links to it — a pre-existing orphan I left alone as out of scope.