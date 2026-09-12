---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: price list effective 2026-09-01; Beta 5 cut, Alpha 5 unchanged
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current prices, per million tokens (MTok), from the price list effective 2026-09-01
(fetched 2026-09-02):

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-02 | REPEATED |
| Beta 5 | $2.00 | $10.00 | 2026-09-02 | REPEATED |

Verdict is REPEATED for every row: a vendor price list asserts these numbers, it does
not measure them. Nothing here was derived.

## Claim rows

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5.00 in / $25.00 out per MTok | https://example.test/pricing-2026-09 (fetched 2026-09-02) | `raw/2026-09-02-pricing-page.md`, line 5 | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED |
| Beta 5 costs $2.00 in / $10.00 out per MTok | https://example.test/pricing-2026-09 (fetched 2026-09-02) | `raw/2026-09-02-pricing-page.md`, line 6 | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED |
| The list takes effect 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | `raw/2026-09-02-pricing-page.md`, line 4 | "# Pricing (effective 2026-09-01)" | REPEATED |

## Superseded

Kept so an older figure quoted elsewhere can be dated rather than treated as a
contradiction. Alpha 5 is unchanged between the two lists (a corroboration, not a move).

| model | input | output | as of | source |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-08-20 | https://example.test/pricing-2026-08 |
| Beta 5 | $3 | $15 | 2026-08-20 | https://example.test/pricing-2026-08 |

Beta 5 fell from $3/$15 to $2/$10 with the 2026-09-01 list — a 33% cut on both sides.
This is not a dispute between sources: the later list supersedes the earlier one for
dates from 2026-09-01.

## What would make this wrong

A new price list. These numbers are dated, not durable — re-fetch
https://example.test/pricing-2026-09 before quoting them after a vendor announcement,
and check whether the effective date has moved past 2026-09-01.

## Neighbours

[[prompt-caching]] multiplies the input price in the table above by 0.1 on a cache read
and by 1.25 on a cache write, so every price change here changes cached-call cost too;
the 2026-09-02 list restates both multipliers unchanged.
