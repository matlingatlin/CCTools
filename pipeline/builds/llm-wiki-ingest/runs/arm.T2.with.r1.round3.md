Lint (by hand — this wiki has no lint script) passes: no dangling wikilinks, every note listed in INDEX.md, no orphans.

**Triage: disputed.** The card's 753B contradicts the 744B the wiki held from a different, earlier source (`gamma-card`, 2026-08-25). Both values are kept as dated claim rows rather than one overwriting the other, because neither source measured the count — both are vendor assertions (REPEATED).

Files changed:

- **`wiki/notes/local-models.md`** — `status: verified` → `disputed`; the new card added to `sources`; body rewritten to state the dispute explicitly; added a `## Claims` table with five rows (744B and 753B both marked disputed, plus 40B active, 1M context, 245 GB at 2-bit), each with a verbatim quote and verdict; added *what it means here* and *what is open*.
- **`wiki/raw/2026-09-02-gamma-7-model-card.md`** *(new)* — the source bytes, unedited.
- **`wiki/raw/MANIFEST.md`** *(new)* — provenance row: source URL, fetch date, SHA-256, size, the note it feeds.
- **`wiki/SOURCES.md`** — one row for the consulted source.
- **`wiki/LOG.md`** — one operation line: disposition, URL, page touched, what was disputed vs. added, and the by-hand lint.

Two things worth your attention. The 744B claim has **no verbatim quote** — its source predates this wiki's `raw/`, so there are no kept bytes to check it against; that gap is recorded under *what is open*. And the 245 GB figure is unchanged, so the memory tiering on that page is unaffected by the dispute — the ~1.2% parameter difference doesn't move the 2-bit footprint. No cascade edges were added: the page names no neighbours, and I had no true sentence connecting it to one.