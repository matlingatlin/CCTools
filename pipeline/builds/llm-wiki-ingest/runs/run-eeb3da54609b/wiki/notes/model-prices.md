---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: pricing effective 2026-09-01; supersedes the 2026-08 page for Beta 5
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, as of the pricing page fetched 2026-09-02 (effective 2026-09-01):

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-02 | REPEATED (unchanged from 2026-08-20) |
| Beta 5 | $2.00 | $10.00 | 2026-09-02 | REPEATED |

Superseded rows, kept so an older quote can be dated:

| model | input | output | as of | superseded by |
|---|---|---|---|---|
| Beta 5 | $3.00 | $15.00 | 2026-08-20 | 2026-09-01 price change |

## Claims

- Alpha 5 price — https://example.test/pricing-2026-09, line 5, verbatim:
  "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens."
  Verdict: **REPEATED** (vendor assertion, no measurement). Same as the 2026-08 page.
- Beta 5 price — same source, line 6, verbatim:
  "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens."
  Verdict: **REPEATED**. Differs from the 2026-08-20 value ($3/$15). Not marked
  `disputed`: the page is headed "Pricing (effective 2026-09-01)", so this is a dated
  price change, not two sources disagreeing about the same date.
- Cache multipliers — same source, line 7, verbatim:
  "Cache reads are billed at 10% of the input price; cache writes at 125%."
  Verdict: **REPEATED**. Corroborates [[prompt-caching]] (0.1x read, 1.25x write) at a
  second date; the multipliers are owned there, not here.

## What it means here

Any cost estimate written before 2026-09-02 that used Beta 5 at $3/$15 is now 50% high.
[[prompt-caching]] multiplies the input column by 0.1 on a cache read and 1.25 on a write,
so a cached Beta 5 read is $0.20 per MTok as of 2026-09-02.

## Still open

- Whether Alpha 5 pricing is genuinely frozen or the 2026-09 page simply restated it.
- No tiered, batch or long-context pricing appears on either page; unknown whether it exists.
- Prices move. Re-fetch the pricing page before quoting these; this table is wrong the day
  a new effective date is published.
