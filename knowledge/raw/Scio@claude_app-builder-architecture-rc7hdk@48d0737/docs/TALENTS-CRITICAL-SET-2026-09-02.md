# The critical set — the talents Scio cannot be built or run without

**Date:** 2026-09-02. **Status:** proposal. Companion to `TALENTS-THREE-LEVELS-2026-09-02.md`
(which places talents by kind) and `REVIEW-FRESH-EYES-2026-09-02.md` §7 (the full inventory).
This document answers a narrower question: *which talents are load-bearing, at which level, what
state is each in today, and what "smart database" actually means for this project.*

The user's list, verbatim: the loops inside the app, brainstorming, planning, architecture, coding
skills, tests and verification, and a smart database. Each gets a section. The status column uses
four words: **measured** (an eval exists and was run), **written** (exists, no eval), **ungated**
(exists on an unmerged branch, none of the four gates run), **missing**.

---

## 1 · The loops inside the app — the ones that must execute correctly

Scio at runtime is five loops, and the predecessor paid for each of them with a real incident.
The talents that govern a loop are not the loop; they decide what the loop may conclude, when it
stops, and what it may touch.

| Loop | What it does | The incident it must not repeat | Governing talents | Status |
|---|---|---|---|---|
| **Intake** — ask · extract · gate | the gate picks the field, the model words it, extraction never overwrites a statement | a field claiming `stated` without a message id; an inference overwriting a correction | `ais-grounding`, `clarifying-questions`, `provenance-record`, `ontoagent-elicitation` (additive-only), `req-elicit-gym` (the replay metric) | written · **no replay harness run** (`LAYER-A` §6 Missing) |
| **Build** — generate · gate · repair | per package: instrumentation → validation → console → interaction → critique, cheap-and-certain first | a `$3.76` ceiling that licensed ~`$50` because it was per call; the ceiling checked *after* the call and the overshoot unrecorded; a 46-minute build reaped at 15 by a heartbeat that ignored keepalives | `build-loop-stops` (when to give up, what a round records), `gate-verdicts` (what a gate may say), `spend-ceilings` (fail-closed), `validation-evidence` (return what was examined); from skills-repo: `loop-design-check`, `idempotent-action-design`, `agent-fault-injection` | Scio's: written, one ablation each; skills-repo's: **measured** in their own harness, not on Scio |
| **Critique** — a reader that did not write | verdict per criterion, unparseable = failure, "pass" with unmet criteria rewritten to failure | self-review measured negative; a critic that can edit will edit | `gate-verdicts`; the critic as a **read-only subagent** (ADR-0008) | written; the subagent shape is **missing** |
| **Design change** — mark · describe · impact · regenerate · promote | only the smallest dependency-complete area changes; conflicts asked, never resolved | a design-version ref that fails to parse silently triggers a **full rebuild**, the data loss ADR-0017 exists to prevent | `change-impact-analysis`, `reflexion-conformance`, `untrusted-text-boundary`; skills-repo `agent-blast-radius-guard` | written · Slice 2 |
| **Contribution** — generalise · re-verify · admit | a finished build teaches the library; never the reason a delivery fails | `data-scio-package` leaking into entries (caught by re-verifying against an unseen entity) | `reuse-classification`, `contract-retrieval`, `catalog-budget`; skills-repo `semantic-duplicate-sweep` | written · Slice 3 |

**The one rule over all five:** a loop's stop condition, budget and allowed surface are written
*before* it runs and enforced by a **hook**, never by the model's judgement (ADR-0008). A loop
that decides for itself when it is done is the predecessor's `is_buildable()` boolean one level up.

**What is missing for Slice 1, in order:** the `stop-rule` hook (round ledger, refuse a fourth
attempt at the same failure class); the `spend-ceiling` hook checked before the call; the intake
replay harness with `req-elicit-gym`'s metrics so that any change to intake can be shown to be an
improvement; a fault-injection run of the build loop against stubbed tools before it runs
unattended.

---

## 2 · Brainstorming, planning, architecture

| Job | Governing (Scio) | Executing | Status |
|---|---|---|---|
| **Brainstorm**, once per system | `brainstorm` — parallel independent generation, check every idea against the domain before writing it down, emit a parseable idea file | `rebuild-prospector` ×N in parallel, each from its own brief, **no Read on the codebase** | skill written, one ablation; agent ungated |
| **Validate** — the subtracting stage | `PIPELINE.md` §2: a stated output budget per layer, every rejection carrying its reason | `rebuild-adjudicator` — already-built / one of the 85 proposals / new / n/a, with `file:line`, into a selection dossier | **agent ungated; the budget number undecided** |
| **Architecture**, whole system then per layer | `architecture` — fourteen patterns with what disqualifies each, ISO 25010 vocabulary, ATAM trade-offs, the deterministic-first boundary rule; `design-rule-hierarchy` — upward-only dependencies, propagation cost | `architect` — three procedures (`architecture-decision`, `system-decomposition`, `architecture-review`), docs-only by hook, no persona | skill written, ablation run; agent ungated, its own ADR-0021 sourced |
| **Model calls ruled one by one** | the deterministic-first doctrine | `llm-component-architect` — per call: deterministic alternative, cost, failure mode, what data may enter the prompt | ungated; **this is the doctrine made a checklist and should run over Slice 1's design** |
| **Plan** | `ears-requirements` (addressable, testable sentences), `change-impact-analysis` | skills-repo `writing-plans` → separately rejectable tasks with an observable success criterion each | written (both) |

Resolve first: `architecture` (the catalogue) versus the architect's three procedures. The
catalogue is the *list*; the procedures are the *steps*. The agent loads the catalogue as a
reference and does not carry a second one.

---

## 3 · Coding

The coding talents at level 1 (building Scio) and level 2 (Scio building an app) are different
sets, because the reader is different.

| | Level 1 — building Scio | Level 2 — inside a build |
|---|---|---|
| **Method** | `subagent-driven-development` (fresh implementer per task, spec + quality review, bounded fix loop), `test-driven-development`, `source-grounded-implementation` (pin the SDK version, cite its file and symbol per claim) | the `package-builder` subagent with the package contract and its dependencies' *interfaces*; `maxTurns` from the size classifier |
| **House style** | `style-inheritance` when touching ported predecessor code | the Playbook core + selected stack skills (`stack-nextjs-supabase`, `tenancy-rls`, `design-tokens`), admitted through `playbook-admission` |
| **Edits that must stay surgical** | `interface-depth-design` for the `SandboxProvider` seam | **symbol-level editing, not line-level** — see §5 on Serena |
| **What may not be written** | the architect's docs-only hook; the agent cap as a `SubagentStart` hook | the file-plan fence (`PreToolUse` deny outside the package's plan), the package stamp, the secret sink |
| **Status** | all written in skills-repo, measured there | the hooks and the subagent are **missing**; the Playbook is a library of one |

---

## 4 · Tests and verification

This project's own record: three confirmed cases of tests passing for the wrong reason, one of
which hid a live cross-tenant read. The critical set is therefore not "write tests" but *"make a
green run mean something."*

| Job | Talent | Status |
|---|---|---|
| Green is `unjudged` until the test is shown able to fail | `testing` (Scio) — doubles no stricter than production, the deletion test, `E6` a green generated suite is `unjudged` | written, ablation run |
| Claim done only with evidence | `verification-before-completion` | measured (skills-repo) |
| Was green bought by weakening the check | `oracle-weakening-audit` — mutation on the changed assertions | measured (skills-repo) |
| Tenancy proven, not asserted | `tenant-isolation` — RLS, the cross-tenant zero-rows test generated beside every policy, the four traps | written; **the zero-rows test is BC-A14 / E-57, undecided** |
| A build gate reports what it examined | `validation-evidence`, `gate-verdicts` | written |
| A talent proves it beats baseline before it ships | `skill-measure` + `paired-comparison-blinding` (skills-repo other branch) — probe first, paired arms, expectations written from *blinded* outputs, preregistered threshold | measured on three builds; **too slow (28-min floor)** per its own review |
| A generated app with a model feature | `llm-eval-harness` (assertion-based CI gate), `llm-redteam-scan` | measured (skills-repo); level 2 and 3 |
| An agent about to run unattended | `agent-fault-injection` | measured (skills-repo) |

**The order that is not negotiable** (`SKILLS-LIBRARY.md`): measure *one* talent properly before
the library gets a second entry. The measuring instrument exists on `skills-repo@claude/hej-f7k1d2`;
its dispatch harness does not, and that is the one addition its review asks for.

---

## 5 · The "smart database" — three jobs, not one product

The phrase covers three questions that need three different stores, and the project has already
answered two of them with evidence. Measured and dated below; decision in **ADR-0011**.

### 5.1 The three questions

| Question | The store that answers it | State |
|---|---|---|
| **What calls what, what breaks if this changes** — over code | **graphify**, code-only, tree-sitter, 0 LLM tokens, three static files in git, `SessionStart` + `post-commit` hooks | **decided — ADR-0001.** Limit, measured: blind across the language seam; ADR-0003 (one language) removes the seam |
| **What do we know, what did we decide, with what provenance** — over documents and findings | **`scio.db`** (SQLite FTS5 over 1,901 sections, 249 findings, 27 skills; rebuilt each session; a `read` returns 348 tokens where the file costs 3,153) plus **git-native markdown with `[[wikilinks]]`** in skills-repo (hand-curated, deterministic, zero build cost) | **in use.** The notes carry `sources`, `fetched`, `status: verified` — the provenance record `memory-provenance-separation` asks for |
| **What happened last time, what did the user correct** — session memory | Claude Code **auto memory** (built in; `MEMORY.md` 200 lines / 25 KB per repo; machine-local; not loaded into subagents) or the reference **memory MCP** (JSONL knowledge graph, MIT, eight tools) | **neither fits Scio's runtime**, see 5.3 |

### 5.2 The candidates, checked 2026-09-02

The user named **graphify, Serena and Obsidian**. Graphify is already decided (ADR-0001) and is
row one of §5.1; the two others follow. Graphiti/Zep was **not** named by the user — it appears
here only because skills-repo's verified note compares it to graphify, and the two names are
easy to confuse in writing. They are unrelated projects.

**Serena** (`oraios/serena`, MIT, 28.7k stars, 40+ languages via language servers). It is not a
database. It is an MCP server exposing **symbol-level** retrieval and editing over a running
language server: find a symbol, find everything that references it, replace a symbol's body,
insert after a symbol. Where graphify's graph is tree-sitter and *approximately* right (INFERRED
edges tagged as such), Serena's answers are the compiler's. Its own README says that inside Claude
Code its file/search/shell tools are disabled by default because the harness already has them;
what survives is the semantic layer. It also ships a "memories" feature — markdown files per
project — which overlaps with `CLAUDE.md` and is declined.

Fit: **level 2, the design-change loop.** "Only the smallest dependency-complete area changes"
(the reviews' precisification of the surgical-change promise) is exactly `find_referencing_symbols`
followed by `replace_symbol_body`. Level 1 gains less: the TypeScript LSP plugin already gives
Claude Code diagnostics, and graphify gives impact. Cost: a language server per sandbox (TypeScript
only under ADR-0011 of the predecessor), started per build. **Pilot, measure, then decide**: does
a design change through Serena touch fewer files than the same change through Edit, on the same
marking?

**Obsidian.** A viewer over markdown with `[[wikilinks]]` — the format skills-repo's knowledge base
already uses, and the format graphify exports (`graphify export obsidian`, verified 2026-08-27
after a correction chain). The MCP routes into it (`mcp-obsidian`, `obsidian-mcp-plugin`) require
Obsidian to be *running* with a REST plugin, which makes a desktop app a runtime dependency of an
agent. Fit: **level 1 only, as a human window onto the notes and the graph. Never a store, never
a runtime dependency.** The notes stay in git; Obsidian opens the folder.

**Graphiti / Zep** (temporal knowledge graph, bi-temporal facts, provenance, incremental update;
not on the user's list, see above). The most capable *idea* among memory tools, and skills-repo's verified note already ruled: needs a graph
database and an LLM for extraction, so it cannot live in an ephemeral, git-native model. Kept as a
**reference**; its bi-temporal rule — record when a fact was true and when we learned it — is
adopted in the notes' frontmatter, not its engine.

### 5.3 Why session memory is a hazard at level 2, not a feature

The SDK's hosting guidance for multi-tenant deployments says to set
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and `settingSources: []`, because memory files load into the
system prompt regardless and "can leak one tenant's context into another tenant's session."
A build for tenant A must not remember tenant B. So **Scio's build loop has no cross-build agent
memory at all.** What a build is allowed to remember lives in the app's own repository — its
`CLAUDE.md`, its ADRs, its evidence report (ADR-0008 level 3) — which is per tenant by
construction, and which the next build of the *same* app reads as files. Auto memory is also
machine-local and not loaded into subagents, so in a reclaimed container it is lost anyway.

At level 1 the same applies for a different reason: this project runs in ephemeral containers,
so a memory that is not committed is a memory that is gone. The rule already in skills-repo's
`CLAUDE.md` — a verified fact lands in `knowledge/notes/` in the same turn it is verified —
is the memory system, and it is the right one.

### 5.4 The decision, in one line each

- Code → graphify (decided). One language makes it whole.
- Knowledge and decisions → git-native markdown with wikilinks, indexed by `scio.db`; every note
  carries source, fetch date, verified status, and asserted/observed origin.
- Session memory → none across tenants; per app, the app's own repo.
- Serena → pilot for the design-change loop, measured on files touched per marking.
- Obsidian → a viewer for humans, optional, never a dependency.
- Graphiti → a reference for the bi-temporal rule, not a component.
- A vector index anywhere on a deciding path → still rejected (DROP D11, D19, ADR-0001).

---

## 6 · What this asks of the next session

1. Run the four gates over the nine agents and the four new skills; the `architect`,
   `rebuild-adjudicator` and `llm-component-architect` first, because §2 needs them.
2. Write the two hooks §1 names as missing for Slice 1 and test each with a case that must be
   denied.
3. Pilot Serena on one marking against the predecessor's canonical booking spec; record files
   touched, both arms.
4. Take `skill-builder`'s own recommendation: one dispatch script, freeze the gates, then measure
   one talent end to end.

## Sources

- oraios/serena README, fetched 2026-09-02; code.claude.com/docs/en/memory, fetched 2026-09-02;
  modelcontextprotocol/servers `src/memory`, fetched 2026-09-02; Agent SDK hosting, fetched 2026-09-02
- skills-repo `knowledge/notes/{graphify-assessment,temporal-kg-agent-memory,claude-md-and-memory}.md`, verified 2026-08-27
- `docs/TOOLING-SCAN.md` §"The five that actually matter" (2026-08-26); `docs/SKILLS-LIBRARY.md`; ADR-0001
