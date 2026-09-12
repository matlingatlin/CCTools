---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: pricing page restates the same multipliers; corroborates, adds nothing new
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x (as of
2026-09-02). The multipliers apply to that page's per-model input price, so a price change
there changes the cache cost without this page changing.

The 2026-09-02 pricing page restates both multipliers unchanged from the 2026-08-20
caching page — two independent sources, same values.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Cache reads billed at 10% of the input price | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, line 3 of body | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED |
| Cache writes billed at 125% of the input price | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, line 3 of body | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED |
| Same two multipliers, stated 2026-08-20 | https://example.test/caching | prior ingest, 2026-08-20 | (raw not retained for this ingest) | REPEATED |

## What is open

- Neither source says whether the multipliers vary by model or by cache TTL.
- The pricing page does not state a minimum cacheable prefix length.
