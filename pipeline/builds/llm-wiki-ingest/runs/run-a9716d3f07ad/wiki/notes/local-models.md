---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: official model card; raw at raw/2026-09-02-gamma-7-model-card.md
status: disputed
tags: [models, local]
related: []
---

# Local models

## Gamma-7

Two sources give different total parameter counts. Both are kept; neither is retracted.

| claim | value | source | fetched | verbatim | verdict |
|---|---|---|---|---|---|
| total parameters | 744B | README (gamma-card) | 2026-08-25 | "Gamma-7 has 744B total parameters" (as recorded in this note on 2026-08-25) | REPEATED |
| total parameters | 753B | model card | 2026-09-02 | "Total parameters: 753B." | REPEATED |
| active parameters | 40B | model card | 2026-09-02 | "Active parameters: 40B." | REPEATED |
| context window | 1M tokens | model card | 2026-09-02 | "Context: 1M tokens." | REPEATED |
| memory at 2-bit | 245 GB unified memory | model card | 2026-09-02 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

**Disputed — total parameters.** The later model card (2026-09-02) says 753B; the earlier
README (2026-08-25) says 744B. Neither source describes a measurement, so both are REPEATED
and recency alone does not settle it. The 9B gap is the size of a plausible embedding- or
head-counting convention difference, but no source in the wiki says so.

The 245 GB at 2-bit figure is unchanged across both sources, so the memory tier this note
places Gamma-7 in does not move while the parameter count is disputed.

**Still open:** which counting convention each source uses (does 744B exclude embeddings or
a shared expert?), and whether the README has since been updated to 753B. Re-fetch
https://example.test/gamma-card to check; if it now reads 753B, this dispute resolves to 753B
and the 744B row becomes outdated rather than rival.
