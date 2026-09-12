---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: "raw at raw/2026-09-02-pricing-page.md, sha256 e4da3770460b47b55427ed1d42ecf39b14c2fdecdc531041c3be56b994743530; prices effective 2026-09-01"
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, as of the 2026-09-01 price list (fetched 2026-09-02):

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 | REPEATED |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 | REPEATED |

Verbatim, https://example.test/pricing-2026-09 (fetched 2026-09-02), under
"Pricing (effective 2026-09-01)":

> Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens.
> Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.

Both rows are REPEATED: a vendor price list asserts the numbers, it does not measure them.

## Superseded

| model | input | output | as of | source |
|---|---|---|---|---|
| Beta 5 | $3 | $15 | 2026-08-20 | https://example.test/pricing-2026-08 |

Beta 5 fell from $3/$15 to $2/$10 between the two lists. This is a price *change* across
two dated lists, not a contradiction — the older list is not marked disputed, it is marked
superseded. Alpha 5 is unchanged at $5/$25 across both.

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write; the
2026-09-02 page restates those same multipliers, so that note keeps its own source.

**What would make this wrong:** a price list dated after 2026-09-01, or a per-model or
regional price the flat table above cannot express.
