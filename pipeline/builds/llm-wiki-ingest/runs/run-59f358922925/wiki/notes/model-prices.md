---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: "pricing effective 2026-09-01; raw at raw/2026-09-02-pricing-2026-09.md, sha256 e4da3770460b47b55427ed1d42ecf39b14c2fdecdc531041c3be56b994743530"
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

| model | input | output | as of | verdict |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-09-01 | REPEATED |
| Beta 5 | $2 | $10 | 2026-09-01 | REPEATED |
| Beta 5 (superseded) | $3 | $15 | 2026-08-20 | REPEATED |

Current rows come from the 2026-09 pricing page (fetched 2026-09-02), effective
2026-09-01. Verbatim: `Alpha 5: $5.00 per million input tokens, $25.00 per million
output tokens.` and `Beta 5: $2.00 per million input tokens, $10.00 per million output
tokens.` Both are vendor assertions on a pricing page, not measurements — REPEATED.

Alpha 5 is unchanged from the 2026-08 page, so it carries no separate row for that
source. Beta 5 fell from $3/$15 to $2/$10; the old value is kept dated rather than
deleted, since it was correct for usage billed before 2026-09-01.

[[prompt-caching]] multiplies these by 0.1 on a cache read. The 2026-09 page restates
those multipliers unchanged, so it added nothing to that note.

**What would make this wrong:** a pricing page published after 2026-09-01, a
region- or tier-specific price list, or batch/long-context surcharges — none of which
this source covers.
