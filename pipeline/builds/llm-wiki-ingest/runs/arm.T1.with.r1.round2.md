Ingested per the skill. Triage was **update** (not disputed): the source carries an effective date of 2026-09-01, later than the page's 2026-08-20 rows, so it supersedes rather than contradicts.

Files changed:

- **`wiki/notes/model-prices.md`** — added the 2026-09-02 source; current rows Alpha 5 $5.00/$25.00 (unchanged) and Beta 5 $2.00/$10.00 (was $3/$15, −33% on both), with the 2026-08-20 rows kept and marked superseded; every row dated; added a `## Claims` table (claim | source | locator | verbatim quote | verdict — all REPEATED, a vendor assertion, nothing measured) and a `## What is open` section.
- **`wiki/notes/prompt-caching.md`** — cascade: the pricing page restates 10% read / 125% write unchanged, so it was added as a corroborating source with its own claims table and open questions; the sentence explaining why it matters to `model-prices` is there and both pages name each other.
- **`wiki/raw/2026-09-02-pricing-page.md`** (new) — unedited copy of the source.
- **`wiki/raw/MANIFEST.md`** (new) — provenance row: URL, fetch date, md5 `a573321c…`, 320 bytes, pages fed.
- **`wiki/SOURCES.md`** — one row for the consulted source.
- **`wiki/INDEX.md`** — pointer to `raw/`; no new note, so no new entry.
- **`wiki/LOG.md`** — one operation line naming the disposition, source and pages touched.

Two things worth flagging. No lint script exists here, so I checked by hand: no dangling wikilinks, all notes listed, no one-way links. That check did surface a pre-existing issue — `local-models` has no inbound link from any note. It is unrelated to this source, so I logged it rather than fixing it; that is a whole-wiki clean-up job. Also, no raw was retained for the 2026-08-20 lists, so the superseded rows and the earlier caching values can't be re-quoted; they're carried on the prior ingest's word, and I recorded that limitation on both pages.