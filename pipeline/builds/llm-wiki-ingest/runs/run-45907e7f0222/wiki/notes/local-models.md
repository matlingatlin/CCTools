---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; 753B total, 40B active, 1M context, 245 GB at 2-bit
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7's total parameter count is **disputed**: the 2026-08-25 README says 744B, the
2026-09-02 model card says 753B. Neither source shows a measurement, and neither
supersedes the other on its face, so both are kept as dated rows below rather than one
overwriting the other.

Undisputed: Gamma-7 activates 40B parameters per token, takes 1M tokens of context, and
at 2-bit quantisation fits in 245 GB of unified memory (as of 2026-09-02) — the memory
figure is unchanged from the 2026-08-25 reading.

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Gamma-7 total parameters = 744B (as of 2026-08-25) — **disputed** | https://example.test/gamma-card | README, via note body 2026-08-25 | "Gamma-7 has 744B total parameters" | REPEATED |
| Gamma-7 total parameters = 753B (as of 2026-09-02) — **disputed** | https://example.test/gamma-7-model-card | Gamma-7 model card, line 2 | "Total parameters: 753B." | REPEATED |
| Gamma-7 active parameters = 40B (as of 2026-09-02) | https://example.test/gamma-7-model-card | Gamma-7 model card, line 2 | "Active parameters: 40B." | REPEATED |
| Gamma-7 context window = 1M tokens (as of 2026-09-02) | https://example.test/gamma-7-model-card | Gamma-7 model card, line 2 | "Context: 1M tokens." | REPEATED |
| Gamma-7 at 2-bit fits in 245 GB unified memory (as of 2026-09-02) | https://example.test/gamma-7-model-card | Gamma-7 model card, line 3 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

## What it means here

For memory-tier planning the 245 GB figure is the one that decides, and it is agreed by
both sources; the parameter-count dispute does not move it. The 9B gap between 744B and
753B is under 1.2% and does not change which tier Gamma-7 lands in, so the dispute is
recorded rather than blocking.

## What is open

- Which total-parameter figure is correct. Neither source measured it; a weights manifest
  or a config file would settle it. The page stays `status: disputed` until one does.
- The 2-bit 245 GB figure is asserted, not measured, in both sources — 753B at 2 bits is
  ~188 GB of weights, so the 245 GB includes unstated overhead the sources do not break
  down.
- Untaken from the raw: nothing. Every figure in the model card (753B, 40B, 1M, 2-bit,
  245 GB) is in the claims table above.
