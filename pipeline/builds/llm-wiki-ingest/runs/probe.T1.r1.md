Zero dangling links, no unindexed notes, the one cross-link is two-way with a reason on each side.

**Files changed**

- `wiki/raw/2026-09-02-pricing-page.md` — **new.** Unedited copy of the source kept so the claims can be re-derived when the URL rots (sha256 `e4da3770…4353`).
- `wiki/notes/model-prices.md` — extended, not replaced (this note already owned the topic). Current table re-dated to 2026-09-02 with both prices quoted verbatim and graded **REPEATED** — they're vendor assertions, not measurements. Beta 5's old $3/$15 moved to a new *Superseded* section rather than being deleted; Alpha 5 confirmed unchanged at $5/$25. New source added to frontmatter with its raw path.
- `wiki/notes/prompt-caching.md` — cascade. Gained the confirming source (multipliers restated unchanged at 10% / 125%) plus a sentence saying *why* it links back: the multipliers held, but the base price under them moved, so any cached-cost figure computed before 2026-09-01 is stale.
- `wiki/SOURCES.md` — one row for the new source, naming both notes it feeds and the raw copy.
- `wiki/LOG.md` — ingest entry: update (not new), what changed, the cascade, the raw hash.

`wiki/INDEX.md` is unchanged — no page was created, so there's no row to add.

One judgement call worth flagging: I treated Beta 5 as a **price change across two effective dates**, not a source contradiction, so the note stays `status: verified` rather than `disputed`. The 2026-08 page was correct for its date; both values are kept with their dates so a future reader can tell which applied when.