---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: earlier Gamma-7 README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; 753B total / 40B active / 1M context; raw at raw/2026-09-02-gamma-7-model-card.md
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7's total parameter count is **disputed**: the 2026-08-25 README says 744B, the
2026-09-02 model card says 753B. Both are kept below; neither has been retired. The model
card additionally gives 40B active parameters and a 1M-token context (as of 2026-09-02).
At 2-bit quantisation Gamma-7 needs 245 GB of unified memory (as of 2026-09-02) — the
value this page already held, restated by the model card.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Gamma-7 total parameters = 744B (as of 2026-08-25) — **disputed** | https://example.test/gamma-card | README, per this page's 2026-08-25 entry | *(not available — this source predates `raw/`; no kept bytes to quote)* | REPEATED |
| Gamma-7 total parameters = 753B (as of 2026-09-02) — **disputed** | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-7-model-card.md, body line 1 | "Total parameters: 753B." | REPEATED |
| Gamma-7 active parameters = 40B (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-7-model-card.md, body line 1 | "Active parameters: 40B." | REPEATED |
| Gamma-7 context = 1M tokens (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-7-model-card.md, body line 1 | "Context: 1M tokens." | REPEATED |
| Gamma-7 at 2-bit quantisation fits in 245 GB unified memory (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-7-model-card.md, body line 2 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

## What it means here

Memory tiering for Gamma-7 is unaffected by the dispute: 245 GB at 2-bit is unchanged, and
a 9B difference in total parameters (~1.2%) does not move the 2-bit footprint across a tier
boundary. The dispute matters for anything quoting the headline size, not for capacity
planning. 40B active parameters mark this as a sparse/MoE-style model, so throughput should
be estimated from the active count, not the total.

## What is open

- Which total-parameter figure is correct. Neither source shows a measurement; both are
  vendor assertions, so REPEATED is as high as either can grade. Resolving it needs a source
  that counts (weights manifest, config, or a third-party audit).
- The 744B claim has no kept raw and therefore no verbatim quote — it cannot be re-checked
  against its own bytes.
- Whether 245 GB was re-measured for the model card or carried over from the README.
- Not taken from the raw: nothing. Every figure the card states (753B, 40B, 1M, 245 GB, and
  the 2-bit recommendation) has a row above.
