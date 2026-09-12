---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: pricing effective 2026-09-01; raw at raw/2026-09-02-pricing-page.md
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, as of the 2026-09-02 fetch of the pricing page effective 2026-09-01:

| model | input | output | as of |
|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-09-02 |
| Beta 5 | $2 | $10 | 2026-09-02 |

Superseded, kept for the record:

| model | input | output | as of | superseded by |
|---|---|---|---|---|
| Beta 5 | $3 | $15 | 2026-08-20 | 2026-09-02 pricing page |

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Alpha 5 is $5.00 in / $25.00 out per MTok | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md line 5 | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED (vendor page asserts the price; no measurement) |
| Beta 5 is $2.00 in / $10.00 out per MTok | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md line 6 | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED (vendor page asserts the price; no measurement) |
| Prices above are effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | raw/2026-09-02-pricing-page.md line 4 | "# Pricing (effective 2026-09-01)" | REPEATED |

Alpha 5 is unchanged from the 2026-08-20 fetch; only its as-of date moved. Beta 5 fell from
$3/$15 to $2/$10 — this is a price change over time, not two sources disagreeing about the
same date, so the page stays `verified` rather than `disputed` and the old row is kept above.

[[prompt-caching]] multiplies these by 0.1 on a cache read; the 2026-09-02 pricing page
restates that multiplier and the 1.25x write multiplier, adding no new claim there.

**What would make this wrong:** a pricing page with an effective date after 2026-09-01, or a
per-model or regional price the flat table above does not carry.
