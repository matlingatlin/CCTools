---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: first Gamma-7 source; raw bytes not retained
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    note: Gamma-7 model card; raw at raw/2026-09-02-gamma-model-card.md
status: disputed
tags: [models, local]
related: ["[[model-prices]]"]
---

# Local models

Models you run on your own hardware, sized by the memory tier they fit in. Where
[[model-prices]] lists per-token prices for hosted models, the cost here is the memory
you have to own, so the deciding number is parameter count times bits per weight.

**Gamma-7** is a sparse model: two sources disagree on its total parameter count
(744B as of 2026-08-25, 753B as of 2026-09-02 — see Claims), while the deployment
number both times is 245 GB of unified memory at 2-bit quantisation. The model card
adds 40B active parameters and a 1M-token context (as of 2026-09-02).

## Claims

| claim | source | locator | verbatim quote | verdict |
|---|---|---|---|---|
| Gamma-7 total parameters = 753B (as of 2026-09-02) — **disputed** | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md, "Gamma-7 model card" | "Total parameters: 753B." | REPEATED |
| Gamma-7 total parameters = 744B (as of 2026-08-25) — **disputed** | https://example.test/gamma-card | README, per this note's 2026-08-25 revision | quote unavailable — raw bytes not retained at ingest | REPEATED |
| Gamma-7 active parameters = 40B (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md | "Active parameters: 40B." | REPEATED |
| Gamma-7 context = 1M tokens (as of 2026-09-02) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md | "Context: 1M tokens." | REPEATED |
| Gamma-7 at 2-bit fits in 245 GB unified memory (as of 2026-09-02; unchanged from 2026-08-25) | https://example.test/gamma-7-model-card | raw/2026-09-02-gamma-model-card.md | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

Every row is REPEATED: both sources assert their numbers as specifications and neither
describes a measurement.

## What it means here

For tier planning, 245 GB at 2-bit is the number to build on — it is the only figure the
two sources agree on, and it is what a machine has to provide. The parameter count is
currently unusable as a precise input: pick the larger value (753B) if you need a bound.

## What is open

- **Which total is right.** 753B is newer and comes from a model card rather than a
  README, but the 2026-08-25 raw was not kept, so the 744B claim cannot be re-read. The
  difference (9B, ~1.2%) is the size of a revision, a re-count, or a typo — nothing in
  either source says which. Resolve by re-fetching https://example.test/gamma-card.
- **Why 245 GB did not move.** The memory figure is identical across a changed parameter
  count. Either it was not recomputed, or it is not a direct function of the total (the
  model is sparse). Neither source shows the arithmetic, so the figure is carried, not
  derived.
- Only Gamma-7 is covered; the note's title promises tiers this page does not yet have.
