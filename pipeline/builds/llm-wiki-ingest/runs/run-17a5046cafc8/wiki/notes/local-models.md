---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; first source for Gamma-7 parameter count
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    raw: ./2026-09-02-gamma-model-card.md
    note: model card; disagrees with the README on total parameters
status: disputed
tags: [models, local]
related: []
---

# Local models

## Gamma-7

**Disputed: total parameter count.** Two sources give different values and neither is
withdrawn; both rows are kept until a third source or a direct measurement settles it.

| claim | value | source | fetched | verbatim | verdict |
|---|---|---|---|---|---|
| total parameters | 744B | https://example.test/gamma-card (README) | 2026-08-25 | "Gamma-7 has 744B total parameters" (as recorded in this note on 2026-08-25) | REPEATED |
| total parameters | 753B | https://example.test/gamma-7-model-card (model card) | 2026-09-02 | "Total parameters: 753B." | REPEATED |
| active parameters | 40B | https://example.test/gamma-7-model-card | 2026-09-02 | "Active parameters: 40B." | REPEATED |
| context window | 1M tokens | https://example.test/gamma-7-model-card | 2026-09-02 | "Context: 1M tokens." | REPEATED |
| memory at 2-bit | 245 GB unified | https://example.test/gamma-7-model-card | 2026-09-02 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

The 245 GB figure is unchanged across both sources, so the memory tier this note exists to
record does not move with the dispute: Gamma-7 stays a 245 GB-class local model either way.

### What is still open
- Which parameter count is right. The later model card (753B) is the more authoritative
  document type and the more recent fetch, but the README was not retracted, so this note
  does not pick a winner. Resolving it: fetch the card again, or a third source, or count
  the weights.
- Neither figure is MEASURED — both are vendor assertions, and the 245 GB claim is asserted
  rather than derived from either parameter count (at 2-bit, 753B weights alone is ~188 GB,
  so the 245 GB figure carries overhead the sources do not itemise).
