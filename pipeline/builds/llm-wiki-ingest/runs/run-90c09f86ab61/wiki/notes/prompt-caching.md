---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: restates both multipliers unchanged
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

The 2026-09-01 price list repeats both multipliers verbatim ("Cache reads are billed at 10%
of the input price; cache writes at 125%"), so the 2026-08-20 figures here are corroborated
by a second source. Because the multipliers are relative, the Beta 5 price drop in
[[model-prices]] lowers its cache costs proportionally — no change is needed here.

