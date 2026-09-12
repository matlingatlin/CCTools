# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: https://example.test/pricing-2026-09 -> model-prices (update). Beta 5
  $3/$15 -> $2/$10 effective 2026-09-01, old row kept as superseded; Alpha 5 $5/$25
  unchanged, fetch date refreshed; claims rows added with verbatim lines and verdicts.
  no material: the same page restates prompt-caching's 0.1x / 1.25x multipliers, so that
  note was not touched and did not gain the page as a source. Raw kept at
  wiki/raw/2026-09-02-pricing-page.md (sha256 e4da3770...4353), listed in raw/MANIFEST.md.
