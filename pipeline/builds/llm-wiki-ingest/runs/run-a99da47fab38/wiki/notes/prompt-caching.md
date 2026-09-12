---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: corroborates the 0.1x read / 1.25x write multipliers; raw copy at raw/2026-09-02-pricing-page.md
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

The 2026-09-02 pricing page repeats both multipliers verbatim — "Cache reads are
billed at 10% of the input price; cache writes at 125%" (**REPEATED**) — so the
mechanics are unchanged. The multipliers are applied to whichever row of
[[model-prices]] is current, and that note's Beta 5 input price dropped $3 → $2 on
2026-09-01, which changes every cached-token cost computed from it even though
nothing here changed.
