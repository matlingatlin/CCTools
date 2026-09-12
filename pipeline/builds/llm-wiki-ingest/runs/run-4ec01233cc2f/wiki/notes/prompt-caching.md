---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: corroborates the 0.1x read / 1.25x write multipliers; no new material
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

Re-confirmed on 2026-09-02: the price list effective 2026-09-01 states "Cache reads are
billed at 10% of the input price; cache writes at 125%."
(`raw/2026-09-02-pricing-page.md`, line 7) — REPEATED, and identical to the 2026-08-20
figures, so nothing here changed.

## Neighbours

[[model-prices]] holds the base input price these multipliers apply to, so a cached call
is only as current as that note's table; when a price there moves, cached-call cost moves
with it and this page's numbers stay the same.
