---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    path: ./2026-09-02-pricing-page.md
    fetched: 2026-09-02
    note: pricing page, effective 2026-09-01
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Per-million-token list prices, by the date the value was effective.

| model | input | output | as of | note |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 | unchanged from 2026-08-20 |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 | current |
| Beta 5 | $3.00 | $15.00 | 2026-08-20 | superseded 2026-09-01 |

[[prompt-caching]] multiplies the input price by 0.1 on a cache read.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5.00 in / $25.00 out per million tokens, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" body | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED |
| Beta 5 costs $2.00 in / $10.00 out per million tokens, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" body | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED |
| Beta 5 cost $3.00 in / $15.00 out per million tokens as of 2026-08-20 | https://example.test/pricing-2026-08 (fetched 2026-08-20) | prior page revision | (no verbatim quote retained at first ingest) | REPEATED |
| These prices are effective from 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | heading | "# Pricing (effective 2026-09-01)" | REPEATED |

## What it means here

Beta 5's price fell by a third on 2026-09-01; Alpha 5 did not move. This is a
supersession over time, not a contradiction between sources, so the page stays
`verified` and the old Beta 5 row is kept with its own as-of date rather than
deleted. Any cost estimate dated before 2026-09-01 that used Beta 5 at $3/$15
is still correct for its date but must be redone at $2/$10 going forward.

## What is open

- The 2026-09-02 page also states "Cache reads are billed at 10% of the input
  price; cache writes at 125%." Not taken as a claim here: [[prompt-caching]]
  owns the cache multipliers and already holds 0.1x / 1.25x, so this restates a
  value the wiki has (no material) rather than adding one.
- The 2026-08-20 Beta 5 figures predate the quote-before-write rule, so that row
  carries no verbatim quote. It is retained as the dated prior value only.
- The page gives no effective *end* date, and no prices for models other than
  Alpha 5 and Beta 5.
