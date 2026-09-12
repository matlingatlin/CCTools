---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
    note: superseded price list; kept for the historical rows
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: price list effective 2026-09-01; current rows
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Per million tokens. Each row carries the date the price is stated as of; older rows are
kept so a past invoice can be checked against the list that was current then.

| model | input | output | as of | status |
|---|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 | current |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 | current |
| Alpha 5 | $5 | $25 | 2026-08-20 | superseded |
| Beta 5 | $3 | $15 | 2026-08-20 | superseded |

Alpha 5 is unchanged across the two lists. Beta 5 fell by 33% on both input and output
between the 2026-08-20 list and the list effective 2026-09-01; this is a price change over
time, not a disagreement between sources, so the page stays `verified` rather than
`disputed`.

[[prompt-caching]] multiplies these by 0.1 on a cache read and by 1.25 on a cache write
(as of 2026-09-02).

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Alpha 5 input $5.00 /Mtok, output $25.00 /Mtok, effective 2026-09-01 | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, heading "Pricing (effective 2026-09-01)" | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED |
| Beta 5 input $2.00 /Mtok, output $10.00 /Mtok, effective 2026-09-01 | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, heading "Pricing (effective 2026-09-01)" | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED |
| The list is effective 2026-09-01 | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, heading | "# Pricing (effective 2026-09-01)" | REPEATED |
| Cache reads billed at 10% of input price, writes at 125% | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md, line 3 of body | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED |
| Alpha 5 $5 / $25, Beta 5 $3 / $15 as of 2026-08-20 | https://example.test/pricing-2026-08 | prior ingest, 2026-08-20 | (raw not retained for this ingest) | REPEATED |

## What is open

- No raw copy was kept for the 2026-08-20 list, so its rows cannot be re-quoted; they are
  carried forward on the earlier ingest's word alone.
- The source gives no effective *end* date, so the current rows hold until a later list
  supersedes them.
- Whether the cache multipliers apply to every model or only to those listed is not
  stated — see [[prompt-caching]].
