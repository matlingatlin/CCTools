Ingested. Triage said **update**, not new: `model-prices` already owns the topic, so it was extended rather than given a rival page.

**Files changed**

- **`wiki/notes/model-prices.md`** — Beta 5 updated to $2.00/$10.00 (was $3/$15), Alpha 5 confirmed at $5.00/$25.00. Old Beta 5 row kept in a "superseded" table so pre-2026-09 quotes can still be dated. Added a Claims section with the verbatim line, locator and verdict per claim (all **REPEATED** — vendor assertion, nothing measured), a "what it means here" note (old Beta 5 estimates run 50% high; cached Beta 5 read is now $0.20/MTok), and a "still open" section. New source added to frontmatter with fetch date and raw path.
- **`wiki/notes/prompt-caching.md`** — cascade: the source also states the 10%/125% multipliers, so this note gains the corroborating quote at a second date, the new source in frontmatter, and a sentence that the multipliers are unchanged but the price they multiply moved on 2026-09-01. Links with `model-prices` were already two-way; both now carry a *reason*, not just a `related:` entry.
- **`wiki/raw/2026-09-02-pricing-page.md`** (new) — unedited copy of the source.
- **`wiki/raw/MANIFEST.md`** (new) — provenance row: URL, fetch date, sha256 `e4da3770…`, which notes it feeds.
- **`wiki/SOURCES.md`** — row for `pricing-2026-09` → model-prices, prompt-caching.
- **`wiki/LOG.md`** — ingest entry recording the price change, the superseded row, the cascade and the raw hash.
- **`wiki/INDEX.md`** — pointer to the raw layer (no new note row, since no new page was created).

One judgement call worth flagging: I did **not** mark the note `disputed` for Beta 5. The page is headed "Pricing (effective 2026-09-01)", so the two values are a dated price change, not two sources disagreeing about the same date — the reasoning is written into the note so it isn't re-litigated later.

Lint checks (manual — this wiki has no lint script): zero dangling wikilinks, every note listed in the index, the model-prices ↔ prompt-caching link two-way, raw byte-identical to the source. Pre-existing and untouched: `local-models` has `related: []` and is linked by nothing — an orphan that predates this ingest.