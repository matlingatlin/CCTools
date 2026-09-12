Lint (by hand — no lint script in this wiki) passes: no dangling links, every note listed, no orphans introduced.

**Files changed**

- `wiki/notes/model-prices.md` — the owning note, rewritten in schema. Added the 2026-09 source to frontmatter; split the table into **Current (effective 2026-09-01)** (Alpha 5 $5.00/$25.00, Beta 5 $2.00/$10.00) and **Superseded** (the 2026-08-20 rows, kept with a "superseded by" column). Added a `## Claims` table with verbatim quotes, locators and REPEATED verdicts, a "what it means here" tie to `[[prompt-caching]]`, and an Open section.
- `wiki/notes/prompt-caching.md` — added the 2026-09 source, a claims table quoting the 10%/125% line, and a sentence noting the multipliers are unchanged while the dollar figures moved with Beta 5's price. Its `[[model-prices]]` edge already existed and now has a reason.
- `wiki/raw/2026-09-02-pricing-page.md` *(new)* — unedited copy of the source so the wiki can re-read it.
- `wiki/raw/MANIFEST.md` *(new)* — provenance row: source URL, fetch date, size, pages fed.
- `wiki/SOURCES.md` — one row for the consulted source, pointing at the raw file and both pages.
- `wiki/LOG.md` — one operation line: disposition, source URL, pages touched, and the hand-lint statement.

`wiki/INDEX.md` is unchanged — no new page was created.

One judgement call worth flagging: I triaged Beta 5 as **update, not disputed**. The page's row is as-of 2026-08-20 and the source is *effective 2026-09-01*, so the two state different periods rather than contradicting each other — a price change, not a conflict. I kept the old row rather than overwriting it, so past estimates remain checkable. Alpha 5's numbers are identical in both lists.

Also noted but not acted on (pre-existing, belongs to a curator pass): the 2026-08 pricing source has no raw kept, so its rows can't be re-quoted; and `local-models` is an orphan with an empty `related`.