---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; raw at raw/2026-09-02-gamma-7-model-card.md, sha256 0bb6e3d47fdc31776ab0b9fb7c9906ea03ce205a4001dbad786d08397f65ecf0
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7 needs 245 GB of unified memory at 2-bit quantisation. Its **total parameter
count is disputed**: the README (2026-08-25) and the model card (2026-09-02) give
different figures, and nothing seen so far reconciles them. Both rows are kept below;
neither has been superseded, so no downstream number should be derived from either
until the conflict is resolved.

## Claims

| claim | source | locator | verbatim | verdict | as of |
|---|---|---|---|---|---|
| Total parameters: 744B — **disputed** | https://example.test/gamma-card | README | "Gamma-7 has 744B total parameters" (as recorded on ingest 2026-08-25; raw not kept) | REPEATED | 2026-08-25 |
| Total parameters: 753B — **disputed** | https://example.test/gamma-7-model-card | line 5 | "Total parameters: 753B." | REPEATED | 2026-09-02 |
| Active parameters: 40B | https://example.test/gamma-7-model-card | line 5 | "Active parameters: 40B." | REPEATED | 2026-09-02 |
| Context window: 1M tokens | https://example.test/gamma-7-model-card | line 5 | "Context: 1M tokens." | REPEATED | 2026-09-02 |
| 2-bit quantisation fits in 245 GB unified memory | https://example.test/gamma-7-model-card | line 6 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED | 2026-09-02 |

The 245 GB figure is the one value the two sources agree on (the 2026-08-25 ingest
recorded the same number), so it is the only Gamma-7 number here that is safe to plan
against today.

## What is still open

- Which total-parameter figure is right. The model card is nine days newer, which is a
  reason to prefer it but not evidence: a card can restate a stale README, and the
  difference (9B, ~1.2%) is the size of a rounding or a revision, not an obvious typo.
  Resolving it needs a third source that states the count with a date, or a weight-file
  measurement — not another restatement.
- Whether 744B and 753B describe the same release. If the README predates a checkpoint
  revision, both may be correct for different versions, and the page should split rather
  than pick a winner.
- The raw of the 2026-08-25 README was not kept, so its verbatim line above is the value
  as transcribed at ingest and cannot be re-checked against the source. This is why the
  raw layer exists.
