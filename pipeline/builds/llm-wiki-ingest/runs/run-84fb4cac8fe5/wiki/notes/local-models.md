---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: official model card; 753B total, 40B active, 1M context
status: disputed
tags: [models, local]
related: []
---

# Local models

## Gamma-7

Total parameter count is **disputed** between two sources. Both rows are kept; neither
is promoted by repetition.

| Claim | Value | Source | Fetched | Verbatim | Verdict |
|---|---|---|---|---|---|
| Total parameters | 744B | https://example.test/gamma-card (README) | 2026-08-25 | "Gamma-7 has 744B total parameters" (as recorded in this note on 2026-08-25; raw not kept) | REPEATED |
| Total parameters | 753B | https://example.test/gamma-7-model-card | 2026-09-02 | "Total parameters: 753B." | REPEATED |
| Active parameters | 40B | https://example.test/gamma-7-model-card | 2026-09-02 | "Active parameters: 40B." | REPEATED |
| Context window | 1M tokens | https://example.test/gamma-7-model-card | 2026-09-02 | "Context: 1M tokens." | REPEATED |
| Memory at 2-bit | 245 GB unified memory | https://example.test/gamma-7-model-card | 2026-09-02 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

The 245 GB figure agrees with what this note already held, so the memory tier is unaffected
by the parameter dispute.

### What it means here

For memory-tier planning, use 245 GB at 2-bit — that number is stated directly and is not in
dispute. Do not derive a memory figure from the parameter count until the count is settled.

### Still open

- Which total is right: 744B (README, older) or 753B (model card, newer and more official)?
  The two differ by 9B, ~1.2%. Plausible causes: embedding/tied-weight accounting, a
  checkpoint revision between the two dates, or a README that was never updated.
- Resolving it needs the README re-fetched at its current state and compared to the model
  card, or a config/weight-index count. The 2026-08-25 raw was not kept, so the older
  verbatim line cannot be re-read.
- This note would be wrong if the README now also says 753B (then the dispute is stale and
  the row should be retired) or if either source restates the figure with a different basis.
