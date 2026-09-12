---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: earlier README; gives 744B total parameters
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    raw: raw/2026-09-02-gamma-7-model-card.md
    note: official model card; gives 753B total parameters
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7's total parameter count is **disputed**: two sources, two values, both kept
below. The 245 GB memory figure is unchanged between them.

## Claims

| Claim | Source | Locator | Verbatim | As of | Verdict |
|---|---|---|---|---|---|
| Gamma-7 total parameters = 744B | https://example.test/gamma-card | README | "Gamma-7 has 744B total parameters" (as recorded in this note on 2026-08-25) | 2026-08-25 | REPEATED |
| Gamma-7 total parameters = 753B | https://example.test/gamma-7-model-card | model card, line 5 | "Total parameters: 753B." | 2026-09-02 | REPEATED |
| Gamma-7 active parameters = 40B | https://example.test/gamma-7-model-card | model card, line 5 | "Active parameters: 40B." | 2026-09-02 | REPEATED |
| Gamma-7 context = 1M tokens | https://example.test/gamma-7-model-card | model card, line 5 | "Context: 1M tokens." | 2026-09-02 | REPEATED |
| Gamma-7 at 2-bit fits in 245 GB unified memory | https://example.test/gamma-7-model-card | model card, line 6 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | 2026-09-02 | REPEATED |

Neither parameter count is measured: both are asserted by their source. The 2026-09-02
model card is the later and the more authoritative of the two (a model card rather than a
README), but the earlier value is kept rather than overwritten, per the disputed rule.

## What this means here

For memory-tier planning the operative figure is still 245 GB of unified memory at 2-bit —
both sources agree on it, so the 9B-parameter disagreement does not change which machines
can run Gamma-7. It does change any per-parameter arithmetic (bytes/param, active-vs-total
ratio: 40B active on 753B total is 5.3%, on 744B it is 5.4%).

## Still open

- Which count is right. Resolving it needs a third source, or a measured parameter count
  from the released weights (that would be MEASURED and would settle this).
- Whether 245 GB was recomputed against 753B or carried over unchanged. 753B at 2 bits is
  roughly 188 GB of weights, so the 245 GB figure carries overhead the card does not
  itemise — it is not a straight function of the parameter count either way.

## Sources kept raw

- `raw/2026-09-02-gamma-7-model-card.md` (sha256 `0bb6e3d4…65ecf0`, fetched 2026-09-02)
