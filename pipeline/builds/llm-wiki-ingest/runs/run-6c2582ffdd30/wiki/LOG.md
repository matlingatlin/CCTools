# Operation log

- 2026-08-25 ingest: gamma-card -> local-models (new)
- 2026-09-02 ingest: gamma-7-model-card -> local-models (update + disputed). Raw kept at
  raw/2026-09-02-gamma-7-model-card.md (sha256 0bb6e3d4…). Total parameters 753B contradicts
  the 744B the note held from the README; both rows kept with dates, status verified ->
  disputed, prefer 753B (newer, model card) but neither is measured. New claims added:
  active parameters 40B, context 1M tokens. 245 GB at 2-bit corroborated by both sources.
  No cascade: the note names no neighbours and the source introduced none.
