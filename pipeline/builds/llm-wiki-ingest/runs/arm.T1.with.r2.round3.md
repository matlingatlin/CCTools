Done. Hand-lint passed: all three wikilinks resolve to files in `notes/`, `model-prices` and `prompt-caching` name each other, all notes appear in `INDEX.md`, no orphans. The raw source file was not edited.

**Triage: update** (not new, not disputed) — the 2026-09-01 pricing supersedes an earlier value over time rather than contradicting it, so `status` stays `verified`.

Files changed:

- **`wiki/notes/model-prices.md`** — added the 2026-09-02 source to frontmatter; Beta 5 updated to $2.00/$10.00 as of 2026-09-01 with the old $3.00/$15.00 row kept as a dated superseded row; Alpha 5 unchanged in value but its as-of moved to 2026-09-01; added a `## Claims` table (one row per figure, with verbatim quotes, all verdict REPEATED — the page asserts prices, it measures nothing), plus *what it means here* and *what is open*.
- **`wiki/notes/prompt-caching.md`** — cascade sentence: the 0.1x/1.25x multipliers are unchanged, but the base they multiply moved on 2026-09-01, so pre-dated cached-read costs are stale. The source's "10% / 125%" was **no material** for this page (it restates the values already held), so no claim was changed here.
- **`wiki/SOURCES.md`** — one row for the consulted source, with the raw path and both pages it touched.
- **`wiki/LOG.md`** — one operation line: disposition per page, source URL, raw location, and the by-hand lint result (no lint script in this wiki).

`wiki/INDEX.md` is untouched — no new page was created.

One thing worth flagging: the pre-existing Beta 5 $3/$15 row has no verbatim quote, since it predates this ingest; I retained it as a dated prior value and noted the gap under *what is open* rather than inventing a quote for it.