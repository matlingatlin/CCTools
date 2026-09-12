---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    raw: raw/2026-09-02-pricing-page.md
    note: corroborates the read/write multipliers
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

Corroborated 2026-09-02 by the pricing page, verbatim: "Cache reads are billed at 10% of
the input price; cache writes at 125%." Verdict: **REPEATED** — two vendor pages assert it,
neither measures it.

The multipliers apply to whatever the input column of [[model-prices]] says at the time; that
column changed on 2026-09-01 (Beta 5 $3 -> $2 per MTok), so the derived cached-read price
moved with it even though these multipliers did not.
