# ADR-0011 · Three stores, not one "smart database": a graph for code, git-native notes for knowledge, no cross-tenant memory

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** cross-cutting; level 1 and level 2 per ADR-0008
**Supersedes / relates to:** extends ADR-0001 (graph is standard); relates to ADR-0003 (one language), ADR-0004 (harness), ADR-0008 (talents at three levels)

## Context

The user asked for "some kind of smart database" and named graphify, Serena and Obsidian. The
phrase covers three questions with different answers: what calls what (code structure), what do we
know and why (knowledge with provenance), and what happened last time (session memory). The project
has already answered the first with ADR-0001 and measured it (26× fewer tokens per query; blind
across the Python↔TypeScript seam). The second is answered in practice by `scio.db` (FTS5 over
1,901 sections; a section read at a sixteenth of the file) and by skills-repo's `knowledge/notes/`
with `[[wikilinks]]`, `sources`, `fetched` and `status: verified` frontmatter.

Checked 2026-09-02: Serena (MIT, 28.7k stars) is symbol-level retrieval and editing over a
language server, not a store; its file and shell tools are disabled inside Claude Code by its own
README. Obsidian's MCP routes require the desktop app running with a REST plugin. Claude Code auto
memory is machine-local, capped at 200 lines / 25 KB, not loaded into subagents, and the SDK's
hosting guidance disables it in multi-tenant deployments because it leaks across tenants. Graphiti
needs a graph database and an LLM pass, incompatible with an ephemeral git-native model
(skills-repo note, verified 2026-08-27). Vector indexes on a deciding path were rejected in ADR-0001
and findings D11, D19.

## Decision

Three stores, each for one question, and no fourth:

1. **Code structure → graphify**, as decided in ADR-0001, code-only, in every repo including
   generated apps. ADR-0003 removes the seam it is blind across.
2. **Knowledge and decisions → git-native markdown** with `[[wikilinks]]`, indexed by `scio.db`
   at session start. Every note carries its source, fetch date, verification status, and whether
   each claim was *asserted* by a person or *observed* by the system, with an as-of stamp. A
   verified fact is written in the turn it is verified. Obsidian may open this folder as a viewer;
   nothing depends on it.
3. **Session memory → none across tenants.** Scio's build sessions run with auto memory disabled
   and no setting sources; what a build may remember of an app lives in that app's own repository
   (its `CLAUDE.md`, ADRs and evidence, per ADR-0008 level 3) and is read as files by the next
   build of the same app. At level 1, memory that is not committed does not exist.

Two additions from skills-repo's notes of 2026-09-02: the index extracts `[[wikilink]]` edges into a
table at build time with no model call (the one mechanism the gbrain note marks worth copying), so
"neighbours name each other" becomes checkable rather than a convention; and every retrieval and
every cost row treats a zero as *did not report*, never as cheap — the dispatch-harness note measured
a build whose every cost row read `tokens=None` while its cost gate returned clean.

A caution from the same notes: Graft's *controlled* result on a code graph in the agent's context was
+42% tokens and +46% tool calls over 162 runs, against a 33/50 vs 27/50 SWE-bench gain. A graph is not
free by being present; ADR-0001's unmeasured query count is now the number that decides whether store 1
earns its place.

**Serena is piloted, not adopted**: one marking from the design-change loop run through Serena's
symbol tools and through plain edits, files touched recorded for both arms, decision by that number.
Graphiti's bi-temporal rule is adopted in note frontmatter; its engine is not.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| One knowledge-graph memory server for everything (reference memory MCP, Graphiti, a hosted vendor) | Conflates three questions; needs a running store an ephemeral container reclaims; the registries' memory category carries no source, no limits, no eval (`TOOLING-SCAN`) |
| Obsidian as the store, via MCP | Makes a desktop app a runtime dependency of an agent; the format is already ours without it |
| Serena as the code graph | It answers "who references this" precisely but does not persist a graph in git, needs a language server per repo, and its memories overlap `CLAUDE.md`; it earns a pilot for *editing*, not for the graph |
| Enable auto memory for the build loop | The SDK's own hosting guidance calls this a tenant leak |

## Consequences

**What this buys.** No new infrastructure. Each store is exact, versioned in git, and already
measured. The tenant boundary for memory is structural, not a rule.

**What it costs.** A language server in the sandbox if the Serena pilot wins. The discipline of
writing notes in the turn a fact is verified, which this project has broken twice and recorded.

**What it forecloses.** Cross-app learning inside the build loop that is not routed through the
library's contribution path (ADR-0006 Slice 3), where consent and origin are recorded.

## How we will know it was wrong

A build session repeatedly re-derives something a previous build of the same app established and
the app's repo could not have carried it; or the Serena pilot touches fewer files per marking by a
margin that makes the language server worth its start-up cost; or `scio.db` returns wrong sections
often enough that a session opens files anyway, which ADR-0001 already names as the likeliest
failure and which nothing yet counts.
