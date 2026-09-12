# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-03 ingest: https://example.test/pricing-2026-09 (raw kept unedited at ./2026-09-02-pricing-page.md, fetched 2026-09-02) -> model-prices (update: Beta 5 $3/$15 superseded by $2/$10 effective 2026-09-01, old row kept dated; Alpha 5 $5/$25 re-confirmed, as-of moved to 2026-09-01; Claims table added); prompt-caching (no material — 10%/125% restate the 0.1x/1.25x already held; cascade sentence added naming model-prices). No new page, so INDEX.md unchanged. No lint script in this wiki: checked by hand — wikilinks [[model-prices]] and [[prompt-caching]] both resolve to files in notes/, both pages name each other in related:, all three notes are listed in INDEX.md, no orphans.
