---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; total parameters 744B
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    raw: raw/2026-09-02-gamma-7-model-card.md
    sha256: 0bb6e3d47fdc31776ab0b9fb7c9906ea03ce205a4001dbad786d08397f65ecf0
    note: model card; total parameters 753B — disagrees with the README
status: disputed
tags: [models, local]
related: []
---

# Local models

Gamma-7 needs 245 GB at 2-bit. Its total parameter count is **disputed**: two sources
give two numbers and neither measures it.

## Gamma-7 claims

| claim | value | source | as of | verdict |
|---|---|---|---|---|
| Total parameters | 744B | README (gamma-card) | 2026-08-25 | REPEATED |
| Total parameters | 753B | model card (gamma-7-model-card) | 2026-09-02 | REPEATED |
| Active parameters | 40B | model card | 2026-09-02 | REPEATED |
| Context window | 1M tokens | model card | 2026-09-02 | REPEATED |
| Memory at 2-bit | 245 GB unified | README + model card (agree) | 2026-09-02 | REPEATED |

Verbatim, from `raw/2026-09-02-gamma-7-model-card.md`:

> Total parameters: 753B. Active parameters: 40B. Context: 1M tokens.

> Recommended: 2-bit quantisation fits in 245 GB of unified memory.

## The dispute

The two figures differ by 9B (~1.2%). Both are asserted, neither is accompanied by a
measurement or a method, so neither wins on evidence; the model card is the more recent
and the more authoritative document type, so **prefer 753B** while leaving 744B on the
page. Nothing here treats the newer number as verified — it is REPEATED, like the old one.

The 245 GB figure is unchanged across both sources, which is the one Gamma-7 number two
independent fetches corroborate.

## What would settle it

A parameter count read off the published weights (shard sizes or a config with layer
dimensions), or a statement from the vendor reconciling README and model card. Until then
this page stays `disputed`.
