---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

These multipliers are unchanged, but the base they multiply is not: [[model-prices]]
records a Beta 5 input price cut from $3.00 to $2.00 effective 2026-09-01, so a
cached-read cost computed before that date is stale even though this page is not.
