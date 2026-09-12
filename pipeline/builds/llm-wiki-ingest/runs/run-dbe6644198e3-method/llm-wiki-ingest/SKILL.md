---
name: llm-wiki-ingest
description: "Use when a fetched page, paper, repo, transcript or measurement is about to become a note in an LLM-maintained wiki or knowledge base (Karpathy LLM Wiki: raw, notes, schema) - add this to the knowledge base, ingest this source, put this in the wiki, update the note, this contradicts the note. Raw kept, triage new/update/disputed/no material, quote before write, claim verdicts, neighbours name it back, index and log rows, lint. NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent."
---

# llm-wiki-ingest — one source, one shape, every time

Karpathy's LLM Wiki `ingest` operation made procedural: raw kept, triaged, quoted, graded,
cascaded, registered, linted. The observed failures behind each step are in
`references/rationale.md` - open it when a step seems optional.

## When to use
- A source has told you something you did not know, and you checked it - the trigger is
  the verified fact, not the end of the task.
- An existing page gains a source, or a compiled summary page is written back.

**Not this skill:** digesting a long text (a reading method); gathering claims to bundle
into another unit; an agent's own task state; a document a code change made false; a
clean-up pass over the whole wiki. Each is its own unit - the local names are under
*In this repo*.

## Steps
1. **Keep the raw.** Save the source bytes where the wiki can re-read them, never edited,
   with URL or path and fetch date. Where the wiki keeps a `raw/` directory: fetch date in
   the file name, and provenance (source, date, hash, size, which page it feeds) in the
   directory's manifest rather than inside the immutable file. A transcript or frame text
   is the raw for a video or image.
2. **Search, then triage into exactly one.** Query the wiki's own index for the title,
   trigger terms and URL. **new** - no page owns the topic. **update** - a page owns it:
   extend it, never a rival. **disputed** - the source contradicts a claim a page holds:
   keep both values as dated claim rows with their sources, mark that row `disputed`, and
   set the page's `status: disputed` for as long as any row is. **no material** - no claim,
   no value, no newer date for any page: keep the raw, write the source-log row and the
   operation-log line, touch no page, stop.
3. **Locate every number, date and quote in the raw before writing it,** and grade it:
   MEASURED (the source measured it), REPEATED (asserted, no measurement found), DERIVED
   (computed from assumed parameters). The claim rows go in the page's `## Claims` table
   (step 4) or in the wiki's claims ledger where one exists.
4. **Write the page in the schema.** Frontmatter: `title`; `sources` (url or path,
   fetched, note); `status` - `verified` / `unverified` / `disputed` (step 2) /
   `outdated`; `tags`; `related`. Body: what it is; a `## Claims` table with one row per
   claim - claim | source | locator | verbatim quote | verdict; what it means here; what is
   open. Every price, version, limit, count and date in the body carries its as-of date.
5. **Cascade.** Every neighbour the page names gets one sentence saying why it matters to
   it, then the `related:` entry. No true sentence, no edge.
6. **Register.** A row in the hand-written map of contents for a new page; a row per
   consulted source in the source log (also on no material); one operation-log line naming
   the disposition, the source URL and the pages touched, in every branch.
7. **Lint, then rebuild the search index;** fix what the lint names before committing. The
   fact and its lint pass land in one commit. No lint script in this wiki? Check dangling
   links, unlisted pages and orphans by hand and say so in the log line.

## Rules
- The raw is never edited; the wiki is never the only copy of a fact.
- Nothing about a tool, price, version or limit from memory: look it up and date it.
- This skill installs nothing and fetches no external code. It runs the wiki's own query,
  lint and index commands, and nothing else.

## In this repo (one instance)
Wiki `knowledge/notes/`, raw `knowledge/raw/` (`MANIFEST.md`) and `intake/`; schema = this
file + `CLAUDE.md`'s same-turn rule + `pipeline/contracts/claims.contract.json`, whose
convention is `null` for not-measured and `0` only for a measured zero. Query
`python3 knowledge/kb.py find "<terms>"` / `read "<heading>"`; register in
`knowledge/INDEX.md`, `knowledge/sources/SOURCES.md`, `pipeline/STATUS.md`; lint
`python3 knowledge/kb.py lint`; rebuild `kb.py build`. The neighbouring units here:
`deep-reading` (digesting), `skill-knowledge` (claims for a skill), `unified-memory` (task
state), `doc-claim-reconciliation` (docs after a code change), the `kb-curator` agent
(whole-wiki clean-up).
