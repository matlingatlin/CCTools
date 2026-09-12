Done. Triaged as **disputed** (not a silent overwrite): the card's 753B and the wiki's 744B are both unmeasured assertions, so both are kept as dated rows.

**Files changed:**

- `wiki/raw/2026-09-02-gamma-7-model-card.md` — new; unedited copy of the source bytes.
- `wiki/raw/MANIFEST.md` — new; provenance row (URL, fetch date, sha256 `0bb6e3d4…`).
- `wiki/notes/local-models.md` — `status: verified` → `disputed`; second source added to frontmatter; the bare 744B sentence replaced by a graded claim table holding **744B (gamma-card, 2026-08-25)** and **753B (model card, 2026-09-02)** side by side, both REPEATED; added active params 40B and 1M context; verbatim quotes; noted 245 GB @ 2-bit is unchanged (both sources agree), so the memory tier is unaffected; open question on whether it's a revision or an error.
- `wiki/SOURCES.md` — row for `https://example.test/gamma-7-model-card`, 2026-09-02, feeds local-models.
- `wiki/LOG.md` — ingest line recording the disputed verdict, what changed, and the hand-lint (no lint script here; no dangling links, every note listed in INDEX.md).

`INDEX.md` needed no change — `local-models` is already listed and its description still fits. No `related:` edge was added, since no true sentence connects Gamma-7 to the pricing/caching pair.