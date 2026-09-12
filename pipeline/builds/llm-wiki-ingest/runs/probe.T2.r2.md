Manual lint (no `kb.py` in this wiki): all three notes are listed in INDEX, every wikilink resolves, `model-prices` ↔ `prompt-caching` remains two-way, `local-models` names no neighbour so there is no one-way edge to close.

**Files changed**

- `wiki/raw/2026-09-02-gamma-7-model-card.md` — **new.** Unedited copy of the source, with its own `source:`/`fetched:` header; sha256 `0bb6e3d4…` recorded in the note and log.
- `wiki/notes/local-models.md` — extended, not replaced (this note already owned Gamma-7). Second source added to frontmatter; `status: verified` → `disputed`. Claims table now carries both parameter counts as dated rows (744B README 2026-08-25, 753B model card 2026-09-02), plus two new claims from this source — 40B active parameters, 1M context. Both verbatim lines quoted. Added a "dispute" section and a "what would settle it" section.
- `wiki/SOURCES.md` — one row for the new source, pointing at the raw file.
- `wiki/LOG.md` — ingest entry: update + disputed, what changed, and why no cascade was needed.
- `wiki/INDEX.md` — the `local-models` row now flags the dispute so a reader hits it before the note.

On the number itself: **neither figure is measured.** Both are bare assertions, 9B apart (~1.2%). I kept both and marked the page `disputed` rather than overwriting 744B — the model card is newer and the more authoritative document type, so the note says prefer 753B, but it's graded REPEATED exactly like the old one. The 245 GB at 2-bit is the one Gamma-7 figure both sources agree on.