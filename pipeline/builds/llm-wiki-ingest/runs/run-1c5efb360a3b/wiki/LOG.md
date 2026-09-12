# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: https://example.test/gamma-7-model-card -> local-models (update + disputed).
  Raw kept at raw/2026-09-02-gamma-model-card.md (sha256 0bb6e3d4…, 224 B, MANIFEST.md added).
  Total parameters disputed: 744B (2026-08-25) vs 753B (2026-09-02) — both kept as dated claim
  rows, page status set to disputed. Added 40B active, 1M context; 245 GB at 2-bit unchanged.
  Cascade: local-models <-> model-prices edge added, named from both sides. Registered in
  INDEX.md and SOURCES.md. No lint script in this wiki — checked by hand: all wikilinks resolve
  ([[model-prices]], [[prompt-caching]], [[local-models]]), all three notes listed in INDEX.md,
  no orphans, frontmatter schema consistent across notes.
