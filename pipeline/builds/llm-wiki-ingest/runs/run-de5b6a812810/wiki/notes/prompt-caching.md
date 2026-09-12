---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: restates both multipliers unchanged
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

The 2026-09-01 pricing page confirms both at 2026-09-02 — "Cache reads are billed at 10% of
the input price; cache writes at 125%." (REPEATED, a vendor assertion). The multipliers did
not move, but the base prices they apply to did: [[model-prices]] carries the Beta 5 drop
from $3/$15 to $2/$10, so any cached-cost figure computed before 2026-09-01 is now stale.
