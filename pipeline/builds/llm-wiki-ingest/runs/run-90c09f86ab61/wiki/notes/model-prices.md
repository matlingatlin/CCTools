---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: pricing page, effective 2026-09-01; raw kept at 2026-09-02-pricing-page.md (sha256 e4da3770)
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Current, as of the 2026-09-01 price list (fetched 2026-09-02). All figures are vendor
assertions on a pricing page — REPEATED, not measured.

| model | input | output | as of |
|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 |

Superseded rows, kept so a dated quote can be checked against the price that was live then:

| model | input | output | as of | source |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-08-20 | pricing-2026-08 |
| Beta 5 | $3 | $15 | 2026-08-20 | pricing-2026-08 |

Alpha 5 is unchanged across the two lists. Beta 5 fell from $3/$15 to $2/$10 on 2026-09-01;
the two pages do not contradict each other — the later one carries its own effective date —
so anything costed against Beta 5 before 2026-09-01 used the old row and should be re-costed
rather than treated as wrong.

[[prompt-caching]] multiplies these by 0.1 on a cache read and 1.25 on a cache write; the
2026-09 page restates both multipliers, so the cache arithmetic carries over to the new rows
unchanged.

Open: the page gives no effective *end* date, and no vendor commitment that the multipliers
stay tied to the input price. Recheck when the next list is fetched.
