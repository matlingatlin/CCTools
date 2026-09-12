---
title: Local models by memory tier
sources:
  - url: https://example.test/gamma-card
    fetched: 2026-08-25
    note: README; source of the 744B total-parameter figure
  - url: https://example.test/gamma-7-model-card
    fetched: 2026-09-02
    raw: raw/2026-09-02-gamma-7-model-card.md
    sha256: 0bb6e3d47fdc31776ab0b9fb7c9906ea03ce205a4001dbad786d08397f65ecf0
    note: official model card; 753B total, 40B active, 1M context
status: disputed
tags: [models, local]
related: []
---

# Local models

## Gamma-7

Total parameter count is **disputed** — the two sources disagree and neither measured it.

| claim | value | source | fetched | locator | verbatim | verdict |
|---|---|---|---|---|---|---|
| Gamma-7 total parameters | 744B | https://example.test/gamma-card (README) | 2026-08-25 | README | "744B total parameters" (as recorded in this note on 2026-08-25; raw not kept) | REPEATED |
| Gamma-7 total parameters | 753B | https://example.test/gamma-7-model-card | 2026-09-02 | line 4 | "Total parameters: 753B." | REPEATED |
| Gamma-7 active parameters | 40B | https://example.test/gamma-7-model-card | 2026-09-02 | line 4 | "Active parameters: 40B." | REPEATED |
| Gamma-7 context window | 1M tokens | https://example.test/gamma-7-model-card | 2026-09-02 | line 4 | "Context: 1M tokens." | REPEATED |
| Gamma-7 memory at 2-bit | 245 GB unified memory | https://example.test/gamma-7-model-card | 2026-09-02 | line 5 | "Recommended: 2-bit quantisation fits in 245 GB of unified memory." | REPEATED |

The 245 GB figure is unchanged from the 2026-08-25 README entry; the model card restates it
rather than revising it.

### What it means here

For memory-tier planning the 245 GB 2-bit figure is the operative number and both sources
agree on it, so the parameter dispute does not move the tier. Anything that computes memory
or cost *from* the parameter count is affected: 744B vs 753B is a ~1.2% difference.

### What is still open

- Which total is correct. The model card (2026-09-02) is the later and more official of the
  two, so prefer 753B where one number must be picked, but neither source measured it and
  the README has not been re-fetched since 2026-08-25.
- This would be resolved by a re-fetch of the README showing it now says 753B (a corrected
  earlier figure), or by a config/weights manifest that can be counted directly — that would
  be MEASURED and would settle it.
