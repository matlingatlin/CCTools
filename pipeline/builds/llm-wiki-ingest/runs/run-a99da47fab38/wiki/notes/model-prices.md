---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: raw copy at raw/2026-09-02-pricing-page.md; page header says "effective 2026-09-01"
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current prices (per million tokens), as of the 2026-09-02 fetch:

| model | input | output | as of | source | verdict |
|---|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-02 | pricing-2026-09 | REPEATED |
| Beta 5 | $2.00 | $10.00 | 2026-09-02 | pricing-2026-09 | REPEATED |

Superseded rows, kept so a past invoice or estimate can still be read:

| model | input | output | as of | source | verdict |
|---|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-08-20 | pricing-2026-08 | REPEATED |
| Beta 5 | $3 | $15 | 2026-08-20 | pricing-2026-08 | REPEATED |

## Claims

- "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens."
  (pricing-2026-09, line 5) — **REPEATED**, vendor list price, no measurement.
  Unchanged from the 2026-08-20 fetch.
- "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens."
  (pricing-2026-09, line 6) — **REPEATED**. This disagrees with the 2026-08-20
  values ($3/$15), but the newer page is headed "Pricing (effective 2026-09-01)"
  from the same publisher, so this is a dated price change, not a dispute
  between two sources about the same moment. Both rows are kept above; the
  note is not marked `disputed`.
- "Cache reads are billed at 10% of the input price; cache writes at 125%."
  (pricing-2026-09, line 7) — **REPEATED**. Corroborates the multipliers already
  in [[prompt-caching]] from the 2026-08-20 caching page; no change.

## What would make this wrong

Prices move by publisher announcement, not by measurement. Any row here is wrong
the moment a newer pricing page carries a later effective date — re-fetch
https://example.test/pricing-2026-09 before quoting these in a cost estimate.

[[prompt-caching]] multiplies the input price in the current table by 0.1 on a
cache read and 1.25 on a cache write, so a Beta 5 cache read is $0.20 per MTok
after the 2026-09-01 change (was $0.30).
