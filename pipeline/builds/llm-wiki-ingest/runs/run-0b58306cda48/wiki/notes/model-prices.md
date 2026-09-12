---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
    note: first pricing page; source of the 2026-08-20 values
  - url: https://example.test/pricing-2026-09
    path: ./2026-09-02-pricing-page.md
    fetched: 2026-09-02
    note: pricing effective 2026-09-01; supersedes Beta 5, restates Alpha 5
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Per-million-token list prices, each row carrying the as-of date of the *value*.

| model | input | output | as of |
|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 |

Beta 5 was $3 input / $15 output as of 2026-08-20; the 2026-09-01 page lowers it. Alpha 5
is unchanged in value, and its as-of date moves forward because the newer page states the
same figures as effective 2026-09-01.

[[prompt-caching]] multiplies these by 0.1 on a cache read and by 1.25 on a cache write.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5.00/M input, $25.00/M output, effective 2026-09-01 | https://example.test/pricing-2026-09 | "Pricing (effective 2026-09-01)", line 1 | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED |
| Beta 5 costs $2.00/M input, $10.00/M output, effective 2026-09-01 | https://example.test/pricing-2026-09 | "Pricing (effective 2026-09-01)", line 2 | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED |
| Prices above are effective 2026-09-01 | https://example.test/pricing-2026-09 | heading | "# Pricing (effective 2026-09-01)" | REPEATED |
| Beta 5 cost $3/M input, $15/M output as of 2026-08-20 (superseded) | https://example.test/pricing-2026-08 | pricing table | (earlier ingest; value carried forward from the 2026-08-20 note) | REPEATED |

## What it means here

Beta 5 is now 40% of Alpha 5's input price and 40% of its output price, so the cheap-tier
gap widened from the 2026-08-20 figures. The change is a supersession, not a contradiction:
the two sources describe different effective dates, so no claim row is `disputed` and the
page stays `verified`.

## What is open

- **Cache read at 10% of input price, cache write at 125%** — present in the 2026-09-02 raw,
  deliberately not taken here: [[prompt-caching]] already owns those multipliers and holds
  the same values (0.1x / 1.25x), so the raw adds no material to that page.
- No effective *end* date is given for these prices, and the raw lists no models other than
  Alpha 5 and Beta 5 — whether other models exist and are unpriced is unknown.
- The prices are asserted by the vendor page, not measured against a bill; verdicts are
  REPEATED, not MEASURED.
