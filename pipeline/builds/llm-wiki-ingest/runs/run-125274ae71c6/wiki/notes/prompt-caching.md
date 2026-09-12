---
title: Prompt caching mechanics
sources:
  - url: https://example.test/caching
    fetched: 2026-08-20
    note: original statement of the read/write multipliers
  - url: https://example.test/pricing-2026-09
    fetched: 2026-09-02
    note: price list effective 2026-09-01; restates both multipliers unchanged
status: verified
tags: [pricing, caching]
related: ["[[model-prices]]"]
---

# Prompt caching

Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.

The 2026-09-01 price list repeats both multipliers unchanged, so the 2026-08-20 figures still
hold as of 2026-09-02 — but they are multipliers over a base that did move: Beta 5's input
price dropped from $3 to $2, so a Beta 5 cache read went from $0.30 to $0.20 per Mtok without
this page changing at all.

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Cache reads bill at 10% of the input price; writes at 125% | https://example.test/pricing-2026-09 | raw/2026-09-02-pricing-page.md line 7 | "Cache reads are billed at 10% of the input price; cache writes at 125%." | REPEATED |
