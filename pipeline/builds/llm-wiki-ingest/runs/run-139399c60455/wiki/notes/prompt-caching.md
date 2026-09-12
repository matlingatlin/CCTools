---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
  - url: https://example.test/blog/caching-explained
    fetched: 2026-09-02
    raw: raw/2026-09-02-blog-restating-caching.md
    note: restates the existing multipliers, adds nothing new
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

## Claims

| claim | source | verbatim | verdict |
|---|---|---|---|
| read 0.1x input, write 1.25x | https://example.test/caching (2026-08-20) | — | REPEATED |
| read 0.1x input, write 1.25x | https://example.test/blog/caching-explained (2026-09-02) | "Cache reads cost a tenth of the input price and writes cost 1.25 times." | REPEATED |

The 2026-09-02 blog agrees with the 2026-08-20 source in words rather than in
measurement, so the multipliers stay REPEATED — a claim is not promoted by being
repeated more often. Status would move to MEASURED only on a source that states a
measured read/write price, and would move to `disputed` on a source giving different
multipliers.
