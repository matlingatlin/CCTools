No lint script ships with this wiki, so I checked by hand: all three wikilink targets resolve to existing notes, all three are listed in INDEX.md, and `model-prices` ↔ `prompt-caching` name each other. Nothing new introduced, since no note was edited.

**Files changed**

- `wiki/raw/2026-09-02-example.test-blog-caching-explained.md` — **new**. Unedited copy of the source with its `source:`/`fetched:` provenance lines, fetch date in the filename, sha256 `1b2deb2c…`.
- `wiki/SOURCES.md` — one row: `2026-09-02 | https://example.test/blog/caching-explained | (no material — restates prompt-caching)`. The source was consulted, so it gets a row even though it fed no page.
- `wiki/LOG.md` — one operation line recording the `no material` verdict, the reason, and the raw path.

**Files deliberately not changed**

- `wiki/notes/prompt-caching.md` — the blog's two values (0.1x read, 1.25x write) are already there with a dated source. It is not added as a "corroborating" source: that list says what the page was derived from, not what agrees with it. No claims row either, since no new value.
- `wiki/notes/model-prices.md`, `wiki/notes/local-models.md`, `wiki/INDEX.md` — untouched; no new page, no cascade.

One pre-existing issue I noticed but left alone: `local-models` is an orphan — nothing links to it and its `related` is empty. That's whole-wiki cleanup (kb-curator's job), not part of this ingest.