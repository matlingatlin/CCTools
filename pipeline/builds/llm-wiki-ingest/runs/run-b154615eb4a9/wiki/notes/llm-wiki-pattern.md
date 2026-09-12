---
title: Karpathy's LLM Wiki — raw/, wiki/, schema; ingest, query, lint
sources:
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    note: "The primary. Created 2026-04-04; 5,000+ stars and forks at fetch."
    fetched: 2026-09-02
  - note: "Surfaced by a 98-second 'build your own agentic OS' video that calls it 'Karpathy's Obsidian setup' with three folders raw/wiki/outputs; graded below."
  - path: ../raw/2026-09-02-astro-han-karpathy-llm-wiki-SKILL.md
    url: https://github.com/Astro-Han/karpathy-llm-wiki
    note: "The full SKILL.md of the 2.1k-star MIT implementation, read end to end and kept raw (md5 60184773c75ed3693ce45a30c7227645). The earlier row in the comparison table below was written from the README plus a partial read; the sections after it are quoted from this file."
    fetched: 2026-09-02
status: verified
tags: [knowledge-base, memory, obsidian, wiki, compile, method]
related: ["[[claude-md-and-memory]]", "[[graphify-assessment]]", "[[temporal-kg-agent-memory]]", "[[loop-engineering-and-fable-prompting]]", "[[research-methodology]]", "[[third-party-landscape]]"]
---

# The LLM Wiki pattern

This one *is* by Karpathy — the gist is under his own account, unlike LOOPS.md
([[loop-engineering-and-fable-prompting]]). MEASURED from the gist unless marked.

**Three layers.** `raw/` — immutable curated sources (articles, papers, images, data);
the LLM reads, never modifies. `wiki/` — LLM-generated, interlinked markdown that the
system maintains entirely: creates pages, updates them, keeps cross-references current.
**The schema** — a configuration document (CLAUDE.md for Claude Code, AGENTS.md for
Codex) that states the wiki's structure, conventions and workflows; humans and the LLM
co-evolve it.

**Three operations.** *Ingest* — read a source, extract, update entity pages, note
contradictions, strengthen synthesis; "a single source may touch 10–15 wiki pages".
*Query* — search relevant pages, synthesise; a valuable answer becomes a page, so
explorations compound. *Lint* — health-check for contradictions, stale claims, orphan
pages, missing cross-references, data gaps.

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
  batches of 2026-09-02 the raw layer was the local transcripts, and they live in a
  scratch directory that will not survive the session.
- **`lint` — two thirds now exist.** `knowledge/kb.py links` finds dangling and one-way wikilinks, `kb.py stale N` finds MEASURED notes with an old fetch date, and `kb.py selftest` proves the index can fail. What is still missing is the gist's third check: two notes asserting different values for the same named fact (contradictions). The wikilink check run by hand earlier this session (six pre-existing dangling
  links found) is the first third of a lint; contradictions and stale claims are not
  checked by anything. This is the operation that maps to our "verify before acting"
  and "re-check before it steers a decision" rules, and it has no script.
- **The schema exists** — CLAUDE.md's "verified fact lands in knowledge/notes/ the same
  turn" rule plus the MEASURED / REPEATED / DERIVED vocabulary — but it is spread across
  CLAUDE.md, `claims.contract.json` and convention, not one document.

The remaining follow-up is one subcommand, `kb.py contradictions`: two notes asserting different
values for the same named fact (star counts, prices, parameter counts) — the check that would
have caught GLM-5.3's 744B-vs-753B the day it was written.

## Three implementations compared, and what this repo took (added 2026-09-02)

Fetched 2026-09-02, READMEs and one SKILL.md; MEASURED from those pages unless marked.

| repo | shape | what it prescribes | fourth gate |
|---|---|---|---|
| `Astro-Han/karpathy-llm-wiki` — **2.1k stars, MIT**, "unofficial community implementation" | one skill + `scripts/` + `references/` + `examples/`; `npx add-skill` | `raw/<topic>/YYYY-MM-DD-slug.md`, `wiki/<topic>/<article>.md`, `wiki/index.md`, append-only `wiki/log.md`; page fields Sources, Raw, Status blocks (Outdated / Disputed with date), Updated; ingest = fetch → triage (New / Update / Disputed / No material) → compile ("Every number, date, and direct quote must be located in the raw file (grep or read) *before* it is written") → cascade → index + log; **lint in three tiers: safe fixes (index, link targets, Raw refs, See Also), mechanical reports (an evidence-checking script), judgement reports (contradictions, outdated claims, missing cross-references, orphans)**; deliberately no source-hash tracking, review dates, confidence scores, vector search or MCP: "at 50K–100K tokens of curated wiki, grep and read are more reliable" | scripts run on demand, no hook, no installer step: method taken, code not |
| `kfchou/wiki-skills` — MIT | six skills (`wiki-init`, `-ingest`, `-query`, `-lint`, `-update`, `-audit`, `-merge`) | `category` + `summary` frontmatter driving a generated index; `check-contradictions.py`, `lint-mechanical.py`; severity-tiered lint report written to `wiki/pages/lint-<date>.md`; **a tracked pre-commit hook blocks commits with an unresolved contradiction flag, missing frontmatter, a broken link or a slug collision** | the hook is exactly what the gate refuses unaudited; the contradiction script's idea is taken as the curator's judgement tier |
| `toolboxmd/karpathy-wiki` — MIT | four skills incl. a loader "auto-injected into every session", a `session-start` hook, a `bin/wiki` CLI with a scheduler, per-wiki `.ingest-runs.jsonl` / `.ingest-issues.jsonl`, per-directory `_index.md` | `type:` must match the top-level directory; pages at depth ≥ 5 rejected; "Tier-1 lint at every ingest: required frontmatter fields, link resolution, source existence, quality block ranges, type/path consistency" | auto-injected loader + session hook + CLI: sandbox or skip; the tier-1-at-every-ingest rule is taken |

**What landed here the same day.** `llm-wiki-ingest` (skill: the seven-step ingest with this
repo's claim verdicts and the cascade rule), `kb-curator` (agent: lint first, safe tier only,
judgement as data, merges and deletions as proposals) and `kb.py lint` (schema, dangling,
one-way, orphan, unlisted, stale, related-only, and the shared-source pairs as contradiction
candidates; `--json` for the agent; exit 1 on errors). Its first run found 9 errors and 51
warnings on 44 notes and the safe tier closed the errors. The `kb.py contradictions` follow-up
named above is now the curator's step 4 over the pairs the lint emits; a script that compares
values is still not written.

## The Astro-Han SKILL.md read in full — six mechanisms the summary above missed

Source: [the SKILL.md itself](../raw/2026-09-02-astro-han-karpathy-llm-wiki-SKILL.md), kept
raw (fetched 2026-09-02). The table row above was written from the README plus a partial
read, so two of its quotes — the "50K–100K tokens of curated wiki, grep and read are more
reliable" line and the list of deliberate omissions (source hashes, review dates, confidence
scores, vector search, MCP) — are **README claims, not in this file**; checked by grep on
2026-09-02. Everything below is quoted from the raw. All **REPEATED**: this is a method
document, and it asserts its design without measuring any of it — no benchmark, no sample,
no before-and-after anywhere in its 233 lines.

- **The Grounding Invariant, named as an invariant with an owner per phase.** "Every
  load-bearing fact in wiki/ — numbers, dates, direct quotes — exists verbatim in the raw/
  files linked by that article's Raw field. Compile *establishes* this invariant (locate
  before you write); lint *verifies* it". The verifier is a grep over "the high-signal
  literals — suffixed or large numbers, decimals, ISO dates, longer quotes"; the rest is
  covered only by the compile-time rule, which the file admits. **Why it is cheap:**
  "Because raw/ is immutable, a verified article stays verified; the script re-checks the
  whole wiki in seconds, so there is no incremental state to maintain." That is the argument
  our own `raw/` layer has been missing: immutability is not archival piety, it is what lets
  the checker be stateless.
- **Fidelity is about the written form, not just the value.** "write the value exactly as
  found — if the source says 42K, write 42K, not 42,000", and a derived value "must show
  their components so each component is findable in raw". Unlocatable value → "drop it or
  state it without precision". Stronger than our DERIVED verdict, which records that a value
  was computed but does not require the components to be greppable.
- **The no-material log heading is a machine-readable key.** The exact form
  `## [YYYY-MM-DD] ingest | no material: <path>` is required because "The exact no-material
  heading is the machine-readable inventory key"; the lint's "Unreferenced raw files" report
  excludes files logged that way. So no-material is not a dead end — it is what stops a kept
  raw from being reported forever as unfinished work. Our LOG.md has no such key.
- **Parallel search, serial compile.** "Searching may run in parallel; compilation must not —
  compile one source at a time, because index.md, log.md, and cascade updates are shared
  state." The same conclusion [[research-methodology]] reaches for multi-source work, from
  the write side rather than the citation side.
- **Cascade must not trust the index.** "Do not rely on the index alone: search the full wiki
  for the source's key entities, aliases, and the claims it touches" — an index is a summary
  and a summary is exactly where a materially affected page hides. Superseded claims are
  kept with a Status block: "Never silently rewrite history."
- **Two carve-outs we do not have.** Archive pages — a query answer written back as a page —
  "are never cascade-updated (they are point-in-time snapshots)"; and the wiki "supports one
  level of topic subdirectories only. No deeper nesting." Both are cheap rules that remove a
  whole class of lint finding rather than reporting it.

**Two lint dispositions worth copying**, both from the safe-fix tier, both resolving the same
question — *is a broken link data, or damage?* — in opposite directions on purpose: an index entry
pointing at a missing file is marked `[MISSING]` — "Do not delete the entry; let the user
decide" — while a See Also link with zero matches is simply removed, "a dead cross-reference
is not load-bearing". The index is a record; a cross-reference is only an edge.

**What this does not settle.** Nothing in the file is measured, so none of it is evidence
that the method works — only that a 2.1k-star implementation chose it. The grounding grep is
a *literal* check: a sentence that misstates what a source argues, in no numbers, passes it.

