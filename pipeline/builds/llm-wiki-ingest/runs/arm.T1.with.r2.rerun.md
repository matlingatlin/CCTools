Ingested. The pricing page is an **update** to `model-prices` and **no material** for `prompt-caching`.

**Files changed**

- `wiki/notes/model-prices.md` — Beta 5 updated $3/$15 → $2/$10; Alpha 5 unchanged at $5/$25 with its as-of date refreshed to 2026-09-02; the old Beta 5 row kept in a "superseded" table; added a claims table with the verbatim line, locator and a **REPEATED** verdict per price (a vendor page asserts, it doesn't measure); added the new source to frontmatter with its fetch date; noted what would make the page wrong. Status stays `verified`, not `disputed` — a later effective date is a price change over time, not two sources disagreeing about the same date.
- `wiki/SOURCES.md` — row for `https://example.test/pricing-2026-09` (2026-09-02), feeding `model-prices`, with prompt-caching marked no material.
- `wiki/LOG.md` — one line for the update (what changed), one for the no-material outcome on prompt-caching.
- `wiki/raw/2026-09-02-pricing-page.md` (new) — unedited copy of the source.
- `wiki/raw/MANIFEST.md` (new) — provenance: URL, fetch date, sha256.

**Deliberately untouched:** `wiki/notes/prompt-caching.md` — the page already carries 0.1x/1.25x from a dated source; the pricing page only restates them, so it gets no "corroborating" source entry and no claims row. `INDEX.md` needed no row (no new page).

No lint script ships with this wiki, so I checked by hand instead: all wikilinks resolve, all three notes are listed in the index, `model-prices` ↔ `prompt-caching` name each other both ways with a reason. One pre-existing issue I did not touch: `local-models` has no inbound links and an empty `related:` — an orphan from an earlier ingest, not this one.