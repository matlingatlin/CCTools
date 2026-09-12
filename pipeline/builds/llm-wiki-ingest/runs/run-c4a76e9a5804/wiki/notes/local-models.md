---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: official model card; gives 753B total, 40B active, 1M context
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7's total parameter count is **disputed**: the README says 744B (as of 2026-08-25),
the model card says 753B (as of 2026-09-02). Both values are kept below until a source
resolves which is current — the model card is newer, but neither states that it supersedes
the other, so the newer figure is not silently adopted.

Both sources agree on memory: 245 GB at 2-bit quantisation (as of 2026-09-02). The model
card adds 40B active parameters and a 1M-token context (as of 2026-09-02).

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Gamma-7 total parameters = 744B (as of 2026-08-25) | https://example.test/gamma-card | README | "744B total parameters" (as recorded in this note on 2026-08-25; raw not retained) | REPEATED — disputed |
| Gamma-7 total parameters = 753B (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md line 5 | "Total parameters: 753B." | REPEATED — disputed |
| Gamma-7 active parameters = 40B (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md line 5 | "Active parameters: 40B." | REPEATED |
| Gamma-7 context = 1M tokens (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md line 5 | "Context: 1M tokens." | REPEATED |
| 2-bit quantisation fits in 245 GB unified memory (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md line 6 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

## What it means here

For memory-tier planning nothing changes: 245 GB at 2-bit is corroborated by both sources.
The parameter-count dispute matters only for size-class comparisons, where the 1.2% gap
between 744B and 753B is below the precision such comparisons need.

## Open

- Which parameter count is current — the README may predate the card, or count differently
  (e.g. excluding embeddings). No source consulted says.
- The 2026-08-25 README was not kept as raw, so its quote cannot be re-verified from this
  wiki; only the note's own record of it survives.
