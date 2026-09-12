---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: "raw kept at raw/2026-09-02-pricing-page.md; prices effective 2026-09-01"
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current prices, per million tokens. Superseded rows are kept for the record, dated.

| model | input | output | as of | status |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-09-02 | current |
| Beta 5 | $2 | $10 | 2026-09-02 | current |
| Beta 5 | $3 | $15 | 2026-08-20 | superseded 2026-09-01 |

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5 in / $25 out per MTok | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md, under "Pricing (effective 2026-09-01)" | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED (vendor price list, asserted; unchanged from the 2026-08-20 page) |
| Beta 5 costs $2 in / $10 out per MTok from 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md, under "Pricing (effective 2026-09-01)" | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED (vendor price list, asserted) |
| The 2026-09 page is effective from 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md, heading | "# Pricing (effective 2026-09-01)" | REPEATED |

Not `disputed`: the two Beta 5 values come from the same publisher with an explicit
effective date, so 2026-09 supersedes 2026-08 rather than contradicting it. If a source
dated on or after 2026-09-01 still quotes $3/$15, this becomes a dispute and the page's
status changes.

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write; the
2026-09 page restates both multipliers unchanged, so that note was not edited.

## What would make this wrong
Any pricing page fetched after 2026-09-02, or an effective date later than 2026-09-01.
Alpha 5 has now held $5/$25 across two fetches; Beta 5 moved once, so treat it as the
volatile row.
