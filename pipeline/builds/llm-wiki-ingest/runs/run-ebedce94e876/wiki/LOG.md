# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: gamma-7-model-card -> local-models (disputed). Raw kept at
  raw/2026-09-02-gamma-model-card.md (sha256 0bb6e3d4...5ecf0) and raw/MANIFEST.md started.
  Total parameters 753B contradicts the 744B held from the 2026-08-25 README; both rows kept
  with dates and the page marked disputed, neither figure dropped — both are REPEATED, so
  recency does not decide. New material added: active parameters 40B, context 1M tokens. The
  245 GB 2-bit memory figure is unchanged. No cascade: the page names no neighbours and none
  of model-prices/prompt-caching mentions Gamma-7, so no back-links were invented.
  Lint (by hand — this wiki has no lint script): no dangling wikilinks, every note listed in
  INDEX.md, no one-way links, frontmatter schema intact.
