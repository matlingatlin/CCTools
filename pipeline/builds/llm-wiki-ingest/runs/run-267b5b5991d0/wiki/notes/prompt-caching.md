---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: price list effective 2026-09-01; restates the 0.1x / 1.25x multipliers
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x. The multipliers
are unchanged between the 2026-08-20 caching page and the price list effective 2026-09-01,
which states them as 10% and 125% — the same numbers in percent form. The dollar figures they
produce did change, because Beta 5's input price fell on 2026-09-01; the multipliers apply to
whichever [[model-prices]] row is current for the date in question.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Cache reads bill at 10% of input price, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED (vendor-asserted) |
| Cache writes bill at 125% of input price, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED (vendor-asserted) |

## Open

- Neither source says whether the write multiplier is charged once per cache entry or on
  every write of the same prefix.
