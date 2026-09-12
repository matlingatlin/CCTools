---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; total parameter count, raw not kept
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: official model card; raw at raw/2026-09-02-gamma-model-card.md
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7 is the only model this page tiers so far. **Its total parameter count is disputed:**
two sources give different figures and neither has been reconciled against the other.

## Claims

| Claim | Source | Locator | Verbatim | Verdict | As of |
|---|---|---|---|---|---|
| Gamma-7 total parameters = 744B | https://example.test/gamma-card → README | not recorded | not recorded (raw not kept) | REPEATED | 2026-08-25 |
| Gamma-7 total parameters = 753B | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md, L5 | "Total parameters: 753B." | REPEATED | 2026-09-02 |
| Gamma-7 active parameters = 40B | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md, L5 | "Active parameters: 40B." | REPEATED | 2026-09-02 |
| Gamma-7 context = 1M tokens | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md, L5 | "Context: 1M tokens." | REPEATED | 2026-09-02 |
| 2-bit quantisation fits in 245 GB unified memory | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md, L6 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED | 2026-09-02 |

The 245 GB figure is unchanged from the 2026-08-25 ingest, so the memory tier below does not
move whichever parameter count is right.

## Memory tier

- **245 GB unified memory** — Gamma-7 at 2-bit quantisation (2026-09-02).

## The parameter dispute

- 744B, from a README fetched 2026-08-25. Its raw bytes were not kept, so the verbatim line
  cannot be re-read; the number survives only as this row.
- 753B, from the official model card fetched 2026-09-02, raw kept and hashed.

Neither source states a measurement method, so both are REPEATED — the newer one is not
promoted merely by being newer, and the model card is not promoted merely by being official.
Two readings are consistent with the evidence: the README is stale or approximate, or the two
count different things (the card separately reports 40B *active* parameters, so at least one
total/active distinction is in play). **Nothing here resolves it.**

What would settle it: the vendor's parameter table with a stated counting convention
(embeddings in or out, tied or untied), or a config/checkpoint whose tensor shapes can be
summed. Until then, quote both figures with their dates rather than picking one.

## Still open

- The 744B/753B conflict above.
- No second model is tiered yet, so "by memory tier" is a table of one.
