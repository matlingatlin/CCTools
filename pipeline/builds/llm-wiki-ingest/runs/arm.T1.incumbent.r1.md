Lint checks pass: no dangling wikilinks, all three notes indexed, frontmatter schema intact, model-prices ↔ prompt-caching now name each other with a reason on both sides.

**Files changed**

- `wiki/raw/2026-09-02-pricing-page.md` *(new)* — unedited copy of the source, so the fact can be re-derived when the URL rots.
- `wiki/raw/MANIFEST.md` *(new)* — provenance row: URL, fetch date, sha256 `e4da3770…4353`.
- `wiki/notes/model-prices.md` — **update**, not a new page (this note owns the topic). Current table re-dated to 2026-09-02: Alpha 5 $5.00/$25.00 (unchanged), Beta 5 $2.00/$10.00. Old $3/$15 and $5/$25 rows kept in a dated "superseded" table. Added a claims section with the verbatim line and a **REPEATED** verdict per claim (vendor list prices, nothing measured), the new source in frontmatter, and a "what would make this wrong" line.
- `wiki/notes/prompt-caching.md` — cascade: same source added (it corroborates 0.1x read / 1.25x write, unchanged), plus a sentence saying *why* it names `model-prices` — the multipliers apply to whichever row is current, and Beta 5's input drop changes every cached-token cost.
- `wiki/SOURCES.md` — one row for `pricing-2026-09`, feeding both notes.
- `wiki/LOG.md` — ingest entry: triage verdict, raw location and hash, what changed, what cascaded.
- `wiki/INDEX.md` — descriptions updated to carry the as-of date and the caching relation; added a pointer to the raw layer.

One judgement call worth flagging: Beta 5's $3/$15 → $2/$10 is a **change**, not a dispute — the new page is headed "effective 2026-09-01" from the same publisher — so I kept both values as dated rows but did **not** set `status: disputed`. The reasoning is written into the note so a later reader can overturn it.