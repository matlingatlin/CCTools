---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: "raw: raw/2026-09-02-gamma-7-model-card.md, sha256 0bb6e3d47fdc31776ab0b9fb7c9906ea03ce205a4001dbad786d08397f65ecf0"
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7 needs 245 GB at 2-bit quantisation. Its total parameter count is **disputed**:
the two sources below do not agree and neither was measured here.

## Claims

| claim | source | locator | verbatim | verdict |
|---|---|---|---|---|
| Gamma-7 total parameters: 744B | https://example.test/gamma-card (fetched 2026-08-25) | README | "Gamma-7 has 744B total parameters" (as recorded in this note 2026-08-25) | REPEATED |
| Gamma-7 total parameters: 753B | https://example.test/gamma-7-model-card (fetched 2026-09-02) | model card, line 4 | "Total parameters: 753B." | REPEATED |
| Gamma-7 active parameters: 40B | https://example.test/gamma-7-model-card (fetched 2026-09-02) | model card, line 4 | "Active parameters: 40B." | REPEATED |
| Gamma-7 context: 1M tokens | https://example.test/gamma-7-model-card (fetched 2026-09-02) | model card, line 4 | "Context: 1M tokens." | REPEATED |
| Gamma-7 at 2-bit fits in 245 GB unified memory | https://example.test/gamma-7-model-card (fetched 2026-09-02) | model card, line 5 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

## What this means here

The memory tier (245 GB at 2-bit) is unchanged and is the number this note is used for —
both sources agree on it, so the parameter dispute does not move any sizing decision.

## Still open

Which parameter count is right. The 2026-09-02 model card is the later and more official
source (a model card, not a README), but nothing here measured either figure, so both rows
stand until a source states the count with a measurement or the vendor corrects one.
This resolves if the README is re-fetched and now reads 753B, or a third source measures it.
