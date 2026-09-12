---
title: Model prices per million tokens
sources:
  - url: https://example.test/pricing-2026-08
    fetched: 2026-08-20
    note: prior price list; Alpha 5 and Beta 5 rows as of 2026-08-20
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: price list effective 2026-09-01; supersedes the Beta 5 row, restates Alpha 5
status: verified
tags: [pricing, models]
related: ["[[prompt-caching]]"]
---

# Model prices

Per million tokens. Every row carries the date it is true as of; a later row supersedes an
earlier one for the same model rather than replacing it, so an old invoice can still be
checked against the price that was current when it was issued.

## Current (effective 2026-09-01)

| model | input | output | as of |
|---|---|---|---|
| Alpha 5 | $5.00 | $25.00 | 2026-09-01 |
| Beta 5 | $2.00 | $10.00 | 2026-09-01 |

## Superseded

| model | input | output | as of | superseded by |
|---|---|---|---|---|
| Alpha 5 | $5 | $25 | 2026-08-20 | unchanged at 2026-09-01 |
| Beta 5 | $3 | $15 | 2026-08-20 | 2026-09-01 ($2 / $10) |

Beta 5 fell from $3/$15 to $2/$10 between the two lists — a price change across dates, not a
conflict between sources: each list states what it was true of at its own effective date, so
neither row is disputed.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Alpha 5 costs $5.00 in / $25.00 out per Mtok, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" | "Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens." | REPEATED (vendor-asserted list price) |
| Beta 5 costs $2.00 in / $10.00 out per Mtok, effective 2026-09-01 | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" | "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens." | REPEATED (vendor-asserted list price) |
| Cache reads bill at 10% of the input price above; writes at 125% | https://example.test/pricing-2026-09 (fetched 2026-09-02) | "Pricing (effective 2026-09-01)" | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED (vendor-asserted; owned by [[prompt-caching]]) |
| Beta 5 cost $3 in / $15 out per Mtok as of 2026-08-20 | https://example.test/pricing-2026-08 (fetched 2026-08-20) | prior price list | (no verbatim quote retained at ingest; raw not kept for this source) | REPEATED |

## What it means here

[[prompt-caching]] multiplies the input column by 0.1 on a cache read and 1.25 on a cache
write, so the current cheapest cached read is Beta 5 at $0.20 per Mtok (as of 2026-09-01).
Any cost estimate has to say which effective date's row it used.

## Open

- The 2026-08 list's raw was not kept, so its rows cannot be re-quoted; they are retained
  here on the earlier ingest's word only.
- No effective end-date is given for the 2026-09-01 list.
