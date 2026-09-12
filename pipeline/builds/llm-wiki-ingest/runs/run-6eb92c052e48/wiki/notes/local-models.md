---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; gives 744B total parameters
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; gives 753B total parameters, plus active params and context
status: disputed
tags: [models, local]
related: []
---

# Local models

## Gamma-7

**Disputed: total parameter count.** Two sources disagree; both kept, neither dropped.

| Claim | Value | Source | Fetched | Verdict |
|---|---|---|---|---|
| Total parameters | 744B | https://example.test/gamma-card (README) | 2026-08-25 | REPEATED |
| Total parameters | 753B | https://example.test/gamma-7-model-card | 2026-09-02 | REPEATED |
| Active parameters | 40B | https://example.test/gamma-7-model-card | 2026-09-02 | REPEATED |
| Context window | 1M tokens | https://example.test/gamma-7-model-card | 2026-09-02 | REPEATED |
| 2-bit quantisation footprint | 245 GB unified memory | both sources agree | 2026-09-02 | REPEATED |

Verbatim, model card (2026-09-02): "Total parameters: 753B. Active parameters: 40B.
Context: 1M tokens." / "Recommended: 2-bit quantisation fits in 245 GB of unified memory."

The model card is the later and more specific source (it also carries active-parameter and
context figures the README lacks), so 753B is the value to quote if one must be picked — but
neither source shows a measurement, so the disagreement is not resolved here.

## What it means here

Memory tier is unaffected by the dispute: both sources give 245 GB of unified memory at 2-bit,
so the machine that ran Gamma-7 before still runs it.

## Open

- Whether 744B and 753B are a revision between dates or an error in one source. Re-check when
  either page is refetched.
