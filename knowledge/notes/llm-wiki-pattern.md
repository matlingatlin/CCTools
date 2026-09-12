---
title: Karpathy's LLM Wiki — raw/, wiki/, schema; ingest, query, lint
sources:
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    note: "The primary. Created 2026-04-04; 5,000+ stars and forks at fetch."
    fetched: 2026-09-02
  - note: "Surfaced by a 98-second 'build your own agentic OS' video that calls it 'Karpathy's Obsidian setup' with three folders raw/wiki/outputs; graded below."
tags: [knowledge-base, memory, obsidian, wiki, compile, method]
related: ["[[claude-md-and-memory]]", "[[graphify-assessment]]", "[[temporal-kg-agent-memory]]", "[[loop-engineering-and-fable-prompting]]", "[[research-methodology]]", "[[third-party-landscape]]", "[[claude-code-extension-layer]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# The LLM Wiki pattern

This one *is* by Karpathy — the gist is under his own account, unlike LOOPS.md
([[loop-engineering-and-fable-prompting]]). MEASURED from the gist unless marked.

**Three layers.** `raw/` — immutable curated sources (articles, papers, images, data);
the LLM reads, never modifies. `wiki/` — LLM-generated, interlinked markdown that the
system maintains entirely: creates pages, updates them, keeps cross-references current.
**The schema** — a configuration document (CLAUDE.md for Claude Code, AGENTS.md for
Codex) that states the wiki's structure, conventions and workflows; humans and the LLM
co-evolve it. That third layer is not a new mechanism: it is the file
[[claude-md-and-memory]] specifies, loaded before the first token of every session and paid
every turn, which is why a schema that grows without being cut is a running cost rather than
a document.

**Three operations.** *Ingest* — read a source, extract, update entity pages, note
contradictions, strengthen synthesis; "a single source may touch 10–15 wiki pages".
*Query* — search relevant pages, synthesise; a valuable answer becomes a page, so
explorations compound. *Lint* — health-check for contradictions, stale claims, orphan
pages, missing cross-references, data gaps.

Ingest is where this pattern and [[research-methodology]] are the same rule stated twice: "every
number, date, and direct quote must be located in the raw file before it is written" is the
wiki's phrasing of *deep-read the primary, never a search snippet*. The difference is only that
the wiki makes it checkable — the raw file is on disk, so the requirement has an address.

[[temporal-kg-agent-memory]] is the road not taken. Graphiti answers the same
compounding-knowledge problem with a bi-temporal graph database and an LLM call per write; this
pattern answers it with markdown that `grep` can read. Its concepts crossed over anyway, into
`unified-memory` rather than into this pattern. The bi-temporal half is worth naming as a gap:
frontmatter records `fetched:` — when *we* learned a fact — and has no field for when the fact
held in the world, so a dated range survives only as prose in the body ("MIT through v7,
Apache-2.0 from v8"). That is why `kb.py contradictions` has to detect such a range by reading
the sentence, and why it needed a rule not to call one a conflict.

**The principle.** The wiki is a persistent, compounding artefact: instead of retrieving
raw documents at query time (RAG), the LLM incrementally *compiles* structured knowledge
that gets richer per source and per question, and connections are not re-derived. Obsidian
is the browser (graph view, backlinks), not the engine.

## Video claims graded

- "Karpathy's Obsidian setup, vault divided into three subfolders: raw, wiki, outputs" —
  raw and wiki are the gist's; **"outputs" is the creator's addition**, not in the gist,
  which names the schema as the third layer. Not wrong as practice; wrong as attribution.
- "A true RAG system is overkill for most people" — the gist argues this on the merits
  (compile once vs retrieve each time); as stated in the video it is opinion.

That video is graded as a genre in [[claude-code-extension-layer]], whose "agentic OS in
three steps" section places this pattern as the *memory* step, between an architecture of
domains → tasks → skills → automations and a dashboard over them — useful here because it
shows what the pattern is being sold as, and that the vault is only one third of the pitch.

A second video (66 s, "massive overhaul of my Claude Code second brain") uses the gist by
name ("this document from Karpathy — LLM Wiki") as step one, then adds a **self-learning
skill** that "goes through your brain, finds gaps, and researches YouTube or Google to fill
them" on demand or weekly. That is the gist's *lint* ("data gaps") wired to *ingest* — the
loop the gist describes but does not automate — and the honest caveat in the video is the
right one: "build your own, because you are connected to your own sources".

## Where this repo already is, and is not, an LLM wiki

`knowledge/notes/` is the `wiki/` layer: LLM-written, wikilinked, with frontmatter that
names sources and a per-claim verdict. What we lack is stated exactly by the gist:

- **`raw/` — now exists, since the evening of 2026-09-02.** `knowledge/raw/MANIFEST.md` holds byte-identical imports from the other repositories (a second session's work), and `knowledge/raw/video-transcripts-2026-09-02/` holds the verbatim whisper transcripts every video-derived note in this base cites, with md5 per source video. Before that, our sources were URLs with a fetch date. The gist keeps the source text
  itself, immutable, so a page can be re-derived when the URL rots. For the video
  batches of 2026-09-02 the raw layer was the local transcripts — written when they sat in a
  scratch directory; they are committed at `knowledge/raw/video-transcripts-2026-09-02/` and
  the sentence above is the reason the clause about not surviving the session is now struck.
- **`lint` — two thirds now exist.** `knowledge/kb.py links` finds dangling and one-way wikilinks, `kb.py stale N` finds MEASURED notes with an old fetch date, and `kb.py selftest` proves the index can fail. What is still missing is the gist's third check: two notes asserting different values for the same named fact (contradictions). The wikilink check run by hand earlier this session (six pre-existing dangling
  links found) was the first third of a lint; **stale claims are now checked** (`kb.py stale`,
  and the lint's 90-day rule), so what is unchecked is contradictions alone — and the lint
  emits shared-source pairs as candidates for them, which is a prompt to look, not a check. This is the operation that maps to our "verify before acting"
  and "re-check before it steers a decision" rules, and it has no script.
- **The schema exists** — CLAUDE.md's "verified fact lands in knowledge/notes/ the same
  turn" rule plus the MEASURED / REPEATED / DERIVED vocabulary — but it is spread across
  CLAUDE.md, `claims.contract.json` and convention, not one document.

The remaining follow-up is one subcommand, `kb.py contradictions`: two notes asserting different
values for the same named fact (star counts, prices, parameter counts) — the check that would
have caught GLM-5.3's 744B-vs-753B the day it was written. **Both now exist, and the pair is settled** (2026-09-04): `kb.py contradictions` is written and tested, and the GLM figures turned out not to be a contradiction at all - a count from the shipped `config.json` lands at ~754B, so `744B-A40B` reads as a rounded product label against a ~753B weight count ([[glm-5.3-local]]). The check would have flagged the pair for a human; only the primary data could resolve it.

## Three implementations compared, and what this repo took (added 2026-09-02)

Fetched 2026-09-02, READMEs and one SKILL.md; MEASURED from those pages unless marked.

| repo | shape | what it prescribes | fourth gate |
|---|---|---|---|
| `Astro-Han/karpathy-llm-wiki` — **2.1k stars, MIT**, "unofficial community implementation" | one skill + `scripts/` + `references/` + `examples/`; `npx add-skill` | `raw/<topic>/YYYY-MM-DD-slug.md`, `wiki/<topic>/<article>.md`, `wiki/index.md`, append-only `wiki/log.md`; page fields Sources, Raw, Status blocks (Outdated / Disputed with date), Updated; ingest = fetch → triage (New / Update / Disputed / No material) → compile ("every number, date, and direct quote must be located in the raw file before it is written") → cascade → index + log; **lint in three tiers: safe fixes (index, link targets, Raw refs, See Also), mechanical reports (an evidence-checking script), judgement reports (contradictions, outdated claims, missing cross-references, orphans)**; deliberately no source-hash tracking, review dates, confidence scores, vector search or MCP (README, not the SKILL.md): "at 50K–100K tokens of curated wiki, grep and read are more reliable" (README) | scripts run on demand, no hook, no installer step: method taken, code not |
| `kfchou/wiki-skills` — MIT | six skills (`wiki-init`, `-ingest`, `-query`, `-lint`, `-update`, `-audit`, `-merge`) | `category` + `summary` frontmatter driving a generated index; `check-contradictions.py`, `lint-mechanical.py`; severity-tiered lint report written to `wiki/pages/lint-<date>.md`; **a tracked pre-commit hook blocks commits with an unresolved contradiction flag, missing frontmatter, a broken link or a slug collision** | the hook is exactly what the gate refuses unaudited; the contradiction script's idea is taken as the curator's judgement tier |
| `toolboxmd/karpathy-wiki` — MIT | four skills incl. a loader "auto-injected into every session", a `session-start` hook, a `bin/wiki` CLI with a scheduler, per-wiki `.ingest-runs.jsonl` / `.ingest-issues.jsonl`, per-directory `_index.md` | `type:` must match the top-level directory; pages at depth ≥ 5 rejected; "Tier-1 lint at every ingest: required frontmatter fields, link resolution, source existence, quality block ranges, type/path consistency" | auto-injected loader + session hook + CLI: sandbox or skip; the tier-1-at-every-ingest rule is taken |

**What landed here the same day.** `llm-wiki-ingest` (skill: the seven-step ingest with this
repo's claim verdicts and the cascade rule), `kb-curator` (agent: lint first, safe tier only,
judgement as data, merges and deletions as proposals) and `kb.py lint` (schema, dangling,
one-way, orphan, unlisted, stale, related-only, and the shared-source pairs as contradiction
candidates; `--json` for the agent; exit 1 on errors). Its first run found 9 errors and 51
warnings on 44 notes and the safe tier closed the errors. The `kb.py contradictions` follow-up
named above is now the curator's step 4 over the pairs the lint emits. **Written 2026-09-04**
(`kb.py contradictions`), after a day in which three value conflicts — a licence, a version and
a page count — were all caught by hand or by an agent reading pairs, which is exactly the labour
the check exists to remove. It compares TYPED values (licence, version, pages, tokens, words,
lines, price) stated about a SHARED subject, where a pair qualifies by citing the same source
URL and the subject is a tag or URL word both sentences name. Three rules keep it quiet, each
one earned by a false positive it produced first: a stated LIMIT is never compared with a
MEASURED value, judged on the words around the number rather than the sentence (reading the
sentence made "the licence changed *under* this note" a cap); an anchor equal to the value's own
unit is circular and dropped ("tokens" near a token count anchors nothing); and a note naming
BOTH values is a dated range, not a conflict. `kb.py selftest` now carries the fixtures: a
planted conflict must be caught, a dated range and a limit-vs-measured pair must not be. Over
the corrected knowledge base it reports zero; over a copy with the page count put back to its
wrong value it reports the pair.

**Attribution corrected 2026-09-03** by the first v3 build's field trial (a with-arm run of `llm-wiki-ingest` over a copy of this knowledge base): the "grep and read are more reliable" and "no source hashes / vector search / MCP" lines above are README claims, not SKILL.md text - `grep` over the raw kept at fetch confirms neither string is in the SKILL.md. The SKILL.md itself carries six mechanisms this note does not yet hold (the Grounding Invariant, written-form fidelity, the no-material log heading as an inventory key, parallel search / serial compile, cascade must not trust the index, archive never cascades); they are in the run's output at `pipeline/builds/llm-wiki-ingest/runs/fieldtrial.astro-han.with.md` and are the next ingest for this page.

## A generated page's provenance has to be reachable from the page (added 2026-09-04)

A machine-generated wiki makes the raw-layer argument concrete. Graphify's Obsidian export
writes one note per graph node with `source_file: <path>` in frontmatter and a `## Connections`
list — measured at 29 notes here on 2026-09-02, and seen at scale in an outside user's 657-note
build on 2026-09-04 (`knowledge/raw/instagram-graphify-obsidian-2026-09-04/`, graded in
`knowledge/VAULT.md`), where one note came to **15 words and 143 characters**. The frontmatter
path is a citation; it is not a *reachable* one, because the document it names is not in the
vault. Their repair was to copy the corpus in and add a "Source doc" callout per note — which
is this pattern's `raw/` layer, arrived at from the other direction and after the fact.
The rule the two runs agree on: **a page whose source cannot be opened from the page is a stub
with a footnote**, and a wiki of them is navigable without being readable. This repository pays
that cost up front — `raw/` first, then the page that cites it, which is step 1 of
`llm-wiki-ingest` and not an optional one.
