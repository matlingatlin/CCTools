# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: https://example.test/pricing-2026-09 -> model-prices (update) — raw kept at raw/2026-09-02-pricing-page.md (sha256 e4da3770...743530); Beta 5 $3/$15 -> $2/$10 effective 2026-09-01, Alpha 5 unchanged at $5/$25; old Beta 5 row moved to Superseded, both new rows REPEATED (price list asserts, does not measure).
- 2026-09-02 no material: https://example.test/pricing-2026-09 restates prompt-caching's 0.1x cache-read / 1.25x cache-write multipliers — no new claim, prompt-caching untouched.
