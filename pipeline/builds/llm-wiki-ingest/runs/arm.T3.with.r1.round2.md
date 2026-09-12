**Disposition: no material.** The blog restates claims `prompt-caching` already holds and adds nothing.

Files changed:

- **`wiki/SOURCES.md`** — added the row for `https://example.test/blog/caching-explained` (2026-09-02), marked "no material" with the raw path, so a future ingest can see this source was already consulted.
- **`wiki/LOG.md`** — one operation entry: disposition, source URL, "pages touched: none", the verbatim quote with a REPEATED verdict, why no page was edited, the raw location, and the by-hand lint result (no lint script exists here).
- **`wiki/raw/2026-09-02-blog-restating-caching.md`** — new; unedited byte copy of the source so the wiki isn't relying on a file outside itself.

Deliberately unchanged:

- **`notes/prompt-caching.md`** — the two numbers (0.1x read, 1.25x write) are identical to what it already asserts, and the blog gives no measurement, so adding it as a source would inflate the evidence behind a `verified` page without adding any.
- **`INDEX.md`** — no new page, so no new row.

One thing I noticed but did not act on: `local-models` is an orphan (`related: []`, nothing links to it). That predates this ingest and is whole-wiki clean-up rather than part of it; it's recorded in the log line.