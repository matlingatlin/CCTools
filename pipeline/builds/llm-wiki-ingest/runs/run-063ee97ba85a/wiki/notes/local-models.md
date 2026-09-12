---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; raw at raw/2026-09-02-gamma-7-model-card.md; source of the 753B figure
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7 is the model this page tracks for the single-machine memory tier.

## Total parameters — disputed

Two sources give different totals; both are kept until one is superseded.

| value | source | fetched | verdict |
|---|---|---|---|
| 744B | https://example.test/gamma-card (README) | 2026-08-25 | REPEATED — asserted, no measurement |
| 753B | https://example.test/gamma-7-model-card (model card) | 2026-09-02 | REPEATED — asserted, no measurement |

Verbatim, model card: "Total parameters: 753B." Neither source shows a measurement or a
parameter-count method, so the disagreement cannot be resolved from what we hold. The model
card is the later and more authoritative document, but it does not say the earlier figure was
wrong, so 744B is not retired.

## Other claims from the 2026-09-02 model card

| claim | verbatim | verdict |
|---|---|---|
| Active parameters 40B | "Active parameters: 40B." | REPEATED |
| Context 1M tokens | "Context: 1M tokens." | REPEATED |
| 2-bit quantisation fits in 245 GB of unified memory | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

The 245 GB figure is unchanged from the 2026-08-25 ingest.

## What it means here

At 2-bit, Gamma-7 sits in the 245 GB unified-memory tier — above a 128 GB machine, within a
256 GB one. The 9B-parameter disagreement (~1.2%) does not move that tier: at 2 bits, 9B extra
parameters is roughly 2 GB, inside the headroom either figure implies. Only 40B parameters are
active per token, so compute per token is far below what the total suggests, but the whole
753B (or 744B) must still be resident.

## What is open

- Which total is correct. Resolve with a source that states a counting method, or a direct
  measurement of the released weights (2026-09-02).
- Whether the 245 GB figure was recomputed for the 753B total or carried over unchanged.
