---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: pricing page effective 2026-09-01; Beta 5 cut, Alpha 5 unchanged
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, per million tokens, from the pricing page effective 2026-09-01
(fetched 2026-09-02):

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 | REPEATED |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 | REPEATED |

Superseded:

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Beta 5 | $3 | $15 | 2026-08-20 | REPEATED |

Alpha 5 carried $5 / $25 on 2026-08-20 as well; the 2026-09 page restates it, so the
row is the same value on a newer date, not a change.

Claim rows:

- Alpha 5 $5.00 in / $25.00 out — https://example.test/pricing-2026-09, fetched
  2026-09-02, raw `raw/2026-09-02-pricing-page.md`, line "Alpha 5: $5.00 per million
  input tokens, $25.00 per million output tokens." — **REPEATED** (vendor assertion, no
  measurement).
- Beta 5 $2.00 in / $10.00 out — same source, line "Beta 5: $2.00 per million input
  tokens, $10.00 per million output tokens." — **REPEATED**. Down from $3 / $15
  (2026-08-20 page).

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write;
the 2026-09 page restates both multipliers unchanged, so that note was not touched.

These are vendor list prices and will move. Wrong if the vendor publishes a page with a
later effective date, or if a discount/tier not shown on this page applies.
