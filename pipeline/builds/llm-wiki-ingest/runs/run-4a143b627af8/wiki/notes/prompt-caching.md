---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/blog/caching-explained
    fetched: 2026-09-02
    note: corroborates the 0.1x/1.25x multipliers; no new material
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Cache read = 0.1x input price; cache write = 1.25x | https://example.test/caching (2026-08-20) | body | — | REPEATED |
| Cache read = 0.1x input price; cache write = 1.25x | https://example.test/blog/caching-explained (2026-09-02) | "Caching explained" | "Cache reads cost a tenth of the input price and writes cost 1.25 times." | REPEATED |

Both sources assert the multipliers; neither reports a measurement, so repetition does not
promote the claim. It would be wrong if a provider published per-model multipliers that
differ from the flat 0.1x/1.25x — the values in [[model-prices]] are dated for that reason.
