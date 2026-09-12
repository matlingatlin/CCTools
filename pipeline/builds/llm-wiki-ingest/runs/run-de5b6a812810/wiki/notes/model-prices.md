---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: pricing effective 2026-09-01; Beta 5 dropped, Alpha 5 unchanged
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, from the pricing page effective 2026-09-01 (fetched 2026-09-02):

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-02 | REPEATED |
| Beta 5 | $2.00 | $10.00 | 2026-09-02 | REPEATED |

Verbatim, from `raw/2026-09-02-pricing-page.md`:

> Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens.
> Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.

Both are vendor assertions on a pricing page, not measurements — REPEATED, not MEASURED.
They are wrong the moment the vendor publishes a new effective date; re-fetch the pricing
page before quoting them in a cost estimate.

## Superseded

| model | input | output | as of | superseded by |
|---|---|---|---|---|
| Beta 5 | $3 | $15 | 2026-08-20 | 2026-09-01 pricing page |

Alpha 5 was $5/$25 on 2026-08-20 and is unchanged. Beta 5 fell from $3/$15 to $2/$10.
This is a price change across two effective dates, not a contradiction between sources —
the note is not `disputed`.

## Cache multipliers

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write; the
2026-09-02 page restates both ("Cache reads are billed at 10% of the input price; cache
writes at 125%."), so the multipliers are confirmed by a second source at that date.
