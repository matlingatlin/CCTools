# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: pricing-2026-09 -> model-prices (update). Raw kept at
  raw/2026-09-02-pricing-page.md (sha256 e4da3770...4353, see raw/MANIFEST.md).
  Beta 5 $3/$15 -> $2/$10 effective 2026-09-01; both rows kept dated, Alpha 5
  unchanged at $5/$25 and re-dated. Cascade: prompt-caching gained the same
  source (0.1x read / 1.25x write corroborated, unchanged) and a sentence saying
  why it names model-prices. INDEX and SOURCES rows added.
