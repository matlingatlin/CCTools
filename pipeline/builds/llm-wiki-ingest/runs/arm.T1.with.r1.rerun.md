Ingested. Triage: **update** to `model-prices` (Beta 5 changed), **no material** for `prompt-caching` (the page restates 0.1x/1.25x unchanged, so that note was left untouched and did not gain the source).

Files changed:

- **`wiki/raw/2026-09-02-pricing-page.md`** (new) — unedited copy of the source, kept so the claims can be re-derived.
- **`wiki/raw/MANIFEST.md`** (new) — provenance row: URL, fetch date 2026-09-02, sha256 `e4da3770…4353`.
- **`wiki/notes/model-prices.md`** — added the 2026-09 source to frontmatter; Beta 5 now $2/$10 as of 2026-09-02 with the old $3/$15 row kept and marked superseded; Alpha 5 $5/$25 confirmed and re-dated; new Claims table with locator, verbatim line and a verdict per claim (all REPEATED — a vendor price list asserts, it doesn't measure); a note on why this is supersession rather than `disputed`, so status stays `verified`; a "what would make this wrong" section.
- **`wiki/SOURCES.md`** — one row for the consulted source, marking prompt-caching as no material.
- **`wiki/LOG.md`** — one entry: what changed in model-prices, the no-material reason for prompt-caching, and where the raw lives.

Not changed: `wiki/notes/prompt-caching.md` (no new claim; it already names `model-prices` back with a reason, so the cascade was already closed), `wiki/INDEX.md` (no new page).

Checks: all three wikilinks resolve, no unlisted pages, the model-prices ↔ prompt-caching link is two-way with a sentence on each side. This wiki ships no lint script, so those checks were run by hand rather than by the deterministic linter the skill's step 7 expects. `local-models` is an orphan (no links in or out), pre-existing and outside this ingest.