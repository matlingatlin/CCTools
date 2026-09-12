**Triage: no material** — the blog restates exactly what `prompt-caching` already holds ("a tenth of the input price" = 0.1x, "1.25 times" = 1.25x), from a dated source (2026-08-20). It adds no claim and no new value, so per the skill no page is touched and it is *not* added as a corroborating source.

Files changed:

- `wiki/raw/2026-09-02-caching-explained.md` — new; verbatim copy of the source, never to be edited
- `wiki/raw/MANIFEST.md` — new; provenance row (URL, fetch date 2026-09-02, SHA-256 `1b2deb2c…`)
- `wiki/SOURCES.md` — new row: source consulted, feeds into `(none — no material)`
- `wiki/LOG.md` — new entry recording the no-material verdict with the URL and reason

Deliberately **not** changed: `wiki/notes/prompt-caching.md`, `wiki/notes/model-prices.md` (no second source, no claims row), and `wiki/INDEX.md` (no new page).

Lint: this wiki ships no lint script, so I checked by hand — INDEX still lists all three notes, `prompt-caching` ↔ `model-prices` link both ways, no dangling links. One pre-existing issue I left alone since it's outside this ingest: `local-models` has `related: []` and nothing links to it (an orphan) — that's a `kb-curator` item.