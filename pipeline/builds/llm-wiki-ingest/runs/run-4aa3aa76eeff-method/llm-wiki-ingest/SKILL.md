---
name: llm-wiki-ingest
description: "Use when a fetched page, paper, repo, transcript or measurement is about to become a note in an LLM-maintained wiki or knowledge base (Karpathy LLM Wiki: raw, notes, schema) - add this to the knowledge base, ingest this source, put this in the wiki, update the note, this contradicts the note. Raw kept, triage new/update/disputed/no material, quote before write, claim verdicts, neighbours name it back, index and log rows, lint. NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent."
---

# llm-wiki-ingest — one source, one shape, every time

Karpathy's LLM Wiki `ingest` operation made procedural: raw kept, triaged, quoted, graded,
cascaded, registered, linted. The reasons behind each step, with the runs they came from, are
in `references/rationale.md` - open it when a step seems optional.

## When to use
- A source has told you something you did not know, and you checked it - the trigger is
  the verified fact, not the end of the task.
- An existing note gains a source, or a compiled summary page is written back.

**Not this skill:** claims bundled into a skill's `references/` (`skill-knowledge`); agent
task state (`unified-memory`); a document a code change made false
(`doc-claim-reconciliation`); cleaning the whole wiki (`kb-curator` agent).

## Steps
1. **Keep the raw.** Save the source bytes where the wiki can re-read them, never edited,
   with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has
   one, fetch date in the file name, provenance in `raw/MANIFEST.md`. A transcript or frame
   text is the raw for a video or image.
2. **Search, then triage into exactly one:** query the wiki's index for the title, trigger
   terms and URL. **new** (no page owns the topic) · **update** (a page owns it: extend it,
   never a rival) · **disputed** (the source contradicts a page: keep both values as dated
   rows with their sources, mark the page `disputed` there) · **no material** (no claim, no
   value, no newer date for any page: keep the raw, write the source-log row and one
   operation-log line with the URL and the reason, touch no page, stop).
3. **Locate every number, date and quote in the raw before writing it.** One row per claim:
   claim, source, locator, verbatim line, verdict - MEASURED (the source measured it),
   REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters).
4. **Write the page in the schema:** frontmatter `title`, `sources` (url or path, fetched,
   note), `status` (`verified` / `unverified` / `disputed` / `outdated`), `tags`, `related`;
   body: what it is, the claims graded, what it means here, what is open. Date what will move.
5. **Cascade:** every neighbour the page names gets one sentence saying why it matters to it,
   then the `related:` entry. If no true sentence exists, do not add the edge.
6. **Register:** a row in the hand-written map of contents for a new page; a row per
   consulted source in the source log (also on no material); an operation-log line.
7. **Lint, then rebuild the search index;** fix what the lint names before committing. The
   fact and its lint pass land in one commit. No lint script? Hand-check dangling links,
   unlisted pages and orphans, and say so in the log line.

## Rules
- Raw never edited; the wiki never the only copy of a fact.
- `null` for not-fetched and not-measured; `0` only for a measured zero.
- Nothing about a tool, price, version or limit from memory: look it up and date it.
- This skill installs, fetches and runs nothing; it is a writing discipline.

## In this repo (one instance)
Wiki `knowledge/notes/`, raw `knowledge/raw/` (`MANIFEST.md`) and `intake/`; schema =
this file + `CLAUDE.md`'s same-turn rule + `pipeline/contracts/claims.contract.json`. Query
`python3 knowledge/kb.py find "<terms>"` / `read "<heading>"`; register in
`knowledge/INDEX.md`, `knowledge/sources/SOURCES.md`, `pipeline/STATUS.md`; lint
`python3 knowledge/kb.py lint`; rebuild `kb.py build`. Clean-up: `.claude/agents/kb-curator.md`.
