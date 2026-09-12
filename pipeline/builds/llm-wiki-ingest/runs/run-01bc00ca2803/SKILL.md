---
name: llm-wiki-ingest
description: "Use when a fetched page, paper, repo, transcript or measurement is about to become a note in an LLM-maintained wiki or knowledge base (Karpathy LLM Wiki: raw, notes, schema) - add this to the knowledge base, ingest this source, put this in the wiki, update the note, this contradicts the note. Raw kept, triage new/update/disputed/no material, quote before write, claim verdicts, neighbours name it back, index and log rows, lint. NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent."
---

# llm-wiki-ingest — one source, one shape, every time

An LLM-maintained wiki compounds only if every page lands the same way: the source kept
where it can be re-read, the claim quoted before it is written, the verdict on the claim
stated, the neighbours told, the index and the log updated, the lint run. Skip one step and
the page is a chat message with a filename. This is Karpathy's LLM Wiki `ingest` operation
made procedural, with the parts his gist leaves to the reader filled in from what broke here.

## When to use
- A fetched page, paper, repository, transcript, screenshot or tool output has told you
  something you did not know, and you checked it. The trigger is *"I now know something and
  I verified it"*, not *"the task is finished"* - a finding that lives only in the conversation
  is lost at the next compaction, silently.
- An existing note is being extended with a new source, or a compiled summary page is being
  written back from a query over several notes.

**When NOT to use:** claims being gathered to bundle into a skill's `references/` go through
`skill-knowledge` (same quote rule, different destination); a fact about the agent's own
task state goes to `unified-memory`; a document made false by a code change is
`doc-claim-reconciliation`'s; finding what is wrong across the whole wiki is the
`kb-curator` agent's job, not this one's.

## Steps
1. **Keep the raw.** Save the source bytes where the wiki can re-read them (a `raw/` layer
   or an intake directory), never edited, with provenance: URL or path, fetch date, and a
   content hash or commit. A page whose raw is gone cannot be re-derived when the URL rots.
   For a video or image, the transcript or frame text is the raw. When the wiki has its own
   `raw/` directory, the copy goes there with the fetch date in the file name and a content
   hash in the page's source entry.
2. **Search before writing.** Query the wiki's own index for the topic (title, trigger
   terms, the source URL). Triage into exactly one of: **new** (no page owns the topic),
   **update** (a page owns it: extend that page, never a rival), **disputed** (the source
   contradicts a page: keep both values as their own rows with dates, mark the page
   `disputed` where it disagrees), **no material** (the source adds no claim, no value and
   no newer date to any page). **No material means no page is touched**: keep the raw, write
   one operation-log line with the URL and the reason, and stop. A corroborating source is
   not added to the page's source list - that list says what the page was *derived from*,
   not what agrees with it - and no claims row is added for a value the page already holds.
   Observed 2026-09-02: without this rule, every baseline run on a restating blog post still
   edited the owning page (a second source plus a claims row), so "no material" quietly
   became "update".
3. **Locate every number, date and quote in the raw before it is written.** No quote, no
   finding. A claim is one row: what it says, source, locator, verbatim line, and a verdict -
   **MEASURED** (the source measured it: dependent variable, effect, sample), **REPEATED**
   (asserted, no measurement found), **DERIVED** (computed from assumed parameters). A
   claim is not promoted by being repeated more often.
4. **Write the page in the schema.** Frontmatter with title, sources (url or path, fetch
   date, note), status from the fixed vocabulary, tags, related. Body: what it is, the claims
   graded, what it means for this project, what is still open. Date anything that will move
   (prices, versions, star counts) and say what would make it wrong.
5. **Cascade.** For every neighbour the page names, make the neighbour name it back with a
   sentence that says *why* - a `related:` entry alone is an edge nobody argued. Parallel
   authoring produces one-way links structurally; this step is where they are closed.
6. **Register.** One row in the index (map of contents), one row per source in the source
   log, one entry in the operation log saying what was ingested and what it changed.
7. **Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling
   links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names
   before committing. A verified fact and its lint pass land in the same commit.

## Example
**Before:** a fetched pricing page says a model costs $2/$10 per MTok; the fact is stated in
chat and the session moves on.
**After:** the page is saved raw with the fetch date; `find "pricing"` shows a note that owns
model prices; the note gets a dated row with the verbatim line and MEASURED; the two notes
that quote the old price name the pricing note back with a sentence; the index and source
log gain a row; lint reports zero errors; one commit carries all of it.

**No material, before and after:** a blog post restates two multipliers a note already
carries with a dated source. *Before:* the note gains the blog as a "corroborating" source and
a claims row. *After:* the note is untouched; the log says `no material: <url> restates
prompt-caching's 0.1x / 1.25x, no new claim`; the raw is kept.

## Rules
- The raw layer is never edited; the wiki layer is never the only copy of a fact.
- One page owns a topic. Extending beats creating; a rival page is a lint error waiting.
- `null` for not-fetched and not-measured; `0` only for a measured zero.
- No page is written from memory about a tool, price, version or limit; look it up and date it.
- This skill never installs, fetches or runs external code; it is a writing discipline.

## In this repo (one instance)
The wiki is `knowledge/notes/`, the raw layer `knowledge/raw/` (`MANIFEST.md`) and
`intake/`, the schema is this file plus `CLAUDE.md`'s "verified fact lands the same turn"
rule and `pipeline/contracts/claims.contract.json` (the claim-row fields and the three
verdicts). Query with `python3 knowledge/kb.py find "<terms>"` and `read "<heading>"`;
register in `knowledge/INDEX.md`, `knowledge/sources/SOURCES.md` and `pipeline/STATUS.md`;
lint with `python3 knowledge/kb.py lint` (exit 1 on errors) and rebuild with `kb.py build`.
Obsidian opens the repository root as the vault (`knowledge/VAULT.md`). The periodic
clean-up is `.claude/agents/kb-curator.md`.
