The parameter count conflicts (753B on the card vs 744B in the note), so I triaged this as **disputed**, not an update: both values are kept as dated rows and nothing overwrites the old one, because the card being nine days newer is a reason to prefer it, not evidence that it's right.

Files changed:

- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** (new) — verbatim copy of the source, sha256 `0bb6e3d4…65ecf0`, so the card's lines stay re-checkable. The 2026-08-25 README has no raw, which is why its 744B line can't be re-verified now.
- **`wiki/notes/local-models.md`** — status `verified` → `disputed`; second source added; prose rewritten to say the total is contested and that no downstream number should be derived from either figure yet. Added a claims table with the verbatim line, locator and a verdict per claim (all REPEATED — the card asserts, it doesn't measure), covering 744B, 753B, active 40B, context 1M, and 245 GB at 2-bit. Added a "what is still open" section: which figure is right, whether the two describe different checkpoints, and the missing README raw.
- **`wiki/SOURCES.md`** — row for `gamma-7-model-card`, 2026-09-02, feeding local-models.
- **`wiki/LOG.md`** — one ingest line recording the contradiction, the status change, the new claims, the agreeing 245 GB, and the raw's location.
- **`wiki/INDEX.md`** — the local-models entry now flags the dispute so a reader hits it before the note.

Two things worth flagging: **245 GB is the only Gamma-7 number both sources agree on**, so it's the one safe to plan against today; and active parameters (40B) and context (1M) are new claims with a single source each, unconfirmed. This wiki has no lint script, so I checked by hand instead — no dangling wikilinks, every note listed in the index, the model-prices/prompt-caching pair still links both ways. The new content names no neighbours, so there was no cascade step to do.