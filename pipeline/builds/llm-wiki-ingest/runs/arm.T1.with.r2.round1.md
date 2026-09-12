Every wikilink resolves to a note, both index entries already exist (no new page, so `INDEX.md` needed no change), and the `model-prices` ↔ `prompt-caching` edge names back in both directions.

**Files changed**

- **`wiki/notes/model-prices.md`** — the update. Current table now carries the 2026-09-01 list (Alpha 5 $5.00/$25.00, Beta 5 $2.00/$10.00); the 2026-08-20 rows are kept below as dated history rather than overwritten, with a line saying Beta 5 dropped on an effective date (supersession, not a contradiction) and that pre-2026-09-01 costings used the old row. New source added to frontmatter with fetch date and the raw file's hash; claims marked REPEATED (a pricing page asserts, it doesn't measure). Added an open question: no end date, and no commitment that the cache multipliers stay tied to the input price.
- **`wiki/notes/prompt-caching.md`** — cascade. The source restates 10% / 125% verbatim, so it's added as a second corroborating source, with a sentence on why the new list matters here (multipliers are relative, so Beta 5's drop lowers its cache costs proportionally and nothing here changes).
- **`wiki/SOURCES.md`** — one row for the consulted source: date, URL, raw filename + sha256, and both notes it feeds.
- **`wiki/LOG.md`** — one operation line: update + cascade, what moved, the verdict class, and the hand-lint result (no lint script in this wiki, so links/index/orphans were checked by hand and that's stated).

Not changed: `wiki/INDEX.md` (no new page), `wiki/notes/local-models.md`, and the raw source file, which stays unedited on disk as the re-readable copy.