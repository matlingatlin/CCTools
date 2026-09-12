Ingested. Triage was **update** — `model-prices` already owned the topic, so it was extended, not rivaled.

**Files changed**

- `wiki/raw/2026-09-02-pricing-page.md` *(new)* — unedited copy of the source, kept so the page can be re-derived when the URL rots.
- `wiki/raw/MANIFEST.md` *(new)* — provenance row: source URL, fetch date 2026-09-02, sha256 `e4da3770…3530`.
- `wiki/notes/model-prices.md` — current table now Alpha 5 $5.00/$25.00 and Beta 5 $2.00/$10.00 as of 2026-09-02; added a claim-row table (verbatim line + locator + verdict **REPEATED** for each — a price list asserts, it does not measure); the old $3/$15 Beta 5 and $5/$25 Alpha 5 rows moved to a dated **Superseded** section rather than deleted; added "what would make this wrong" and a neighbour paragraph; new source entry in frontmatter.
- `wiki/notes/prompt-caching.md` — no material change (10% read / 125% write restated identically), recorded as a dated re-confirmation with the verbatim line, source row added, and the back-link to `[[model-prices]]` now carries a sentence saying *why* rather than a bare `related:` edge.
- `wiki/INDEX.md` — split into Notes / Raw layer; `model-prices` entry now says "current as of 2026-09-02"; manifest listed.
- `wiki/SOURCES.md` — one row for the new source, feeding model-prices and prompt-caching.
- `wiki/LOG.md` — two entries: the update to model-prices (with the Beta 5 delta and the cascade) and the explicit no-material skip for prompt-caching.

The wiki ships no lint script, so I ran the equivalent checks by hand (frontmatter keys, dangling links, one-way links, unlisted pages): 0 errors. Beta 5's drop is a supersession, not a dispute — the later list is effective 2026-09-01 — so the note is `verified`, not `disputed`. `local-models` quotes no prices, so nothing cascaded there.