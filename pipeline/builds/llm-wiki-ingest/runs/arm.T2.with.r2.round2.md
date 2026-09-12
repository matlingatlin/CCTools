Lint clean: every wikilink resolves to a note, every note is in INDEX.md, no orphans.

**Triage: update + disputed** — `local-models` already owned Gamma-7, and the new card contradicts its parameter count. Both values are kept as dated claim rows rather than one overwriting the other.

Files changed:

- **`wiki/raw/2026-09-02-gamma-model-card.md`** (new) — the source bytes, copied unedited, read-only.
- **`wiki/raw/MANIFEST.md`** (new) — provenance table: source URL, fetch date, sha256, size, page it feeds. Notes that the three earlier sources' bytes were never retained.
- **`wiki/notes/local-models.md`** — `status: verified` → `disputed`; second source added to frontmatter; body rewritten with a `## Claims` table (claim | source | locator | verbatim quote | verdict). **744B (2026-08-25) and 753B (2026-09-02) both stand, both marked disputed**; new claims added for 40B active parameters and 1M context; 245 GB at 2-bit recorded as unchanged. All rows graded REPEATED — neither source describes a measurement. "What is open" records that the 744B claim can't be re-read (raw not kept) and that 245 GB didn't move despite the parameter change.
- **`wiki/notes/model-prices.md`** — cascade name-back: `[[local-models]]` added to `related`, with a sentence saying why (hosted per-token price vs memory you own).
- **`wiki/INDEX.md`** — `local-models` row flagged as disputed; pointer to `raw/`.
- **`wiki/SOURCES.md`** — row for the 2026-09-02 model card.
- **`wiki/LOG.md`** — one operation line: disposition, source URL, pages touched, raw hash, the dispute, the cascade, and the by-hand lint result.

The dispute is recorded, not resolved — 753B is newer and from a model card rather than a README, but nothing in either source explains the 9B gap. Re-fetching `https://example.test/gamma-card` is what would settle it.