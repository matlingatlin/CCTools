Ingested as an **update** (a dated price change, not a dispute — the new list carries its own effective date, so the note stays `verified` and the old rows are kept, dated and marked superseded).

**Files changed**

- `wiki/notes/model-prices.md` — added the 2026-09-02 source; current table now Alpha 5 $5.00/$25.00 and Beta 5 $2.00/$10.00 as of 2026-09-01; old 2026-08-20 rows kept in a superseded table (Beta 5 was $3/$15, Alpha 5 unchanged); added a claims table (claim / source / locator / verbatim line / verdict — all REPEATED, a vendor list asserts rather than measures), a "what it means" section (Beta 5 down 33% both sides, now 2.5x cheaper than Alpha 5 vs 1.67x — re-check routing rules), and a "what is open" section.
- `wiki/notes/prompt-caching.md` — added the same source; the 10%/125% multipliers are reconfirmed unchanged, with the note that the base moved (a Beta 5 cache read went $0.30 → $0.20 per Mtok while this page said nothing); added its claim row with the verbatim line.
- `wiki/raw/2026-09-02-pricing-page.md` *(new)* — unedited copy of the source bytes, verified identical.
- `wiki/raw/MANIFEST.md` *(new)* — provenance: origin URL, fetch date, sha256 `e4da3770…3530`, pages fed.
- `wiki/SOURCES.md` — row: 2026-09-02, `pricing-2026-09`, feeds model-prices + prompt-caching.
- `wiki/LOG.md` — operation line recording the update, the specific price change, the raw location and hash, and the hand-lint (no lint script in this wiki).

`wiki/INDEX.md` unchanged — no new page. Hand-lint: all three wikilinks resolve, model-prices and prompt-caching name each other, all notes listed in the index. One pre-existing issue I did **not** touch: `local-models` is an orphan (`related: []`, nothing links to it) — that's a whole-wiki clean-up for `kb-curator`, not part of this ingest.