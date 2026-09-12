---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
    note: first price list; source of the 2026-08-20 rows
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: price list effective 2026-09-01; raw at raw/2026-09-02-pricing-page.md
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, as of the price list effective 2026-09-01 (fetched 2026-09-02):

| model | input | output | as of |
|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 |

Superseded rows, kept dated:

| model | input | output | as of | superseded by |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-08-20 | unchanged on 2026-09-01 |
| Beta 5 | $3 | $15 | 2026-08-20 | 2026-09-01 price list ($2 / $10) |

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5.00 in / $25.00 out per Mtok | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md line 5 | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED |
| Beta 5 costs $2.00 in / $10.00 out per Mtok | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md line 6 | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED |
| Prices above are effective 2026-09-01 | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md line 4 | "# Pricing (effective 2026-09-01)" | REPEATED |

A vendor price list asserts its prices; nothing here is measured, so every row is REPEATED.

## What it means here

Beta 5 fell from $3/$15 to $2/$10 — a 33% cut on both sides — while Alpha 5 held. Beta 5 is
now 2.5x cheaper than Alpha 5 on both input and output, where it was 1.67x. Any routing rule
tuned to the August spread should be re-checked.

This is a dated change, not a contradiction: the older figures were correct for 2026-08-20 and
the new list gives its own effective date, so both rows stand and the note stays `verified`.

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write; the
2026-09-02 list restates both multipliers unchanged.

## What is open

- Prices move. Re-check the price list before quoting these after the next vendor update; the
  as-of dates above are the only warrant they carry.
- No source yet for tiers other than Alpha 5 and Beta 5.
