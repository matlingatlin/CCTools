# ECC agents, commands and hooks — the orchestration question

*Read and written 2026-08-26, against `affaan-m/ECC` at commit `d8409a4` (19 Aug 2026), cloned
shallow. Every count below is counted from the files, not quoted from their README. Star count is
not evidence and is not cited anywhere in this document.*

**This document does not repeat `docs/ECC-MINED.md` §4.** That pass established the agent
frontmatter discipline (`tools:` + `model:` on 68/68), the small single-purpose file format, the
hypothesis that most agents are language variants, that the 94 commands are full prompt documents
rather than shims, and that the hook bootstrap is unmaintainable. This document tests the
hypothesis that pass left open, and asks the question it did not: **is there an orchestration
design in here, or only a roster?**

The short answer, stated up front so the rest can be evidence for it:

> ECC has **68 agents that cannot call each other** — `Task` appears in zero of the 68 `tools:`
> lines — **one** chain document, and **three** places where a typed artifact genuinely passes
> between workers. Every one of those three got its type from *outside* ECC: the OpenSpec block
> format, the unified-diff format, and a pre-created file skeleton written by a shell script. Where
> ECC invented its own handoff, it is prose, and the one handoff its own chain document names by
> name does not exist.

---

## What I read

| Path | Lines / count | Why |
|---|---|---|
| `agents/*.md` | 68 files, 9,595 lines (median 116) | the roster; frontmatter and prompt bodies |
| `commands/*.md` | 94 files, 12,349 lines | entry points; `gan-build`, `orch-*`, `multi-*`, `plan` read in full |
| `hooks/hooks.json` | 23 entries / 7 events | the installed lifecycle |
| `scripts/hooks/*.js` | `session-start-bootstrap`, `session-start`, `stop-format-typecheck`, `cost-tracker`, `evaluate-session` | what the hooks actually do |
| `skills/orch-pipeline/SKILL.md` | 121 | **the only real chain document in the repo** |
| `rules/common/agents.md` | 61 | their delegation doctrine |
| `scripts/orchestrate-worktrees.js` + `scripts/lib/tmux-worktree-orchestrator.js` | 108 + 598 | the only file-based handoff infrastructure |
| `schemas/*.json` | 11 files | checked for an agent I/O schema. There is none |

Read in full and named here so a "leave" verdict is accountable: `planner.md`, `architect.md`,
`code-reviewer.md`, `gan-planner.md`, `gan-generator.md`, `gan-evaluator.md`, `spec-miner.md`,
`agent-evaluator.md`, `silent-failure-hunter.md`, `go-build-resolver.md`, `react-build-resolver.md`,
and the six `*-reviewer.md` files used for the template diff in §1.

---

## 1 · The 68 agents, clustered honestly

### 1.1 The frontmatter cannot express a handoff

Across all 68 files there are exactly **four** frontmatter keys — `name`, `description`, `tools`,
`model` — present on 68/68, plus `color` on five. That is the whole schema.

There is no `consumes`, no `produces`, no `output_schema`, no `next`. **The file format has no slot
for a handoff.** This is the structural fact that decides §2 before any prompt body is read: a
format that cannot name its input or its output cannot describe a chain, only a worker.

Two more counts that matter more than the roster size:

- **`Task` appears in 0 of 68 `tools:` lines.** No agent can invoke another agent. Whatever chain
  exists must be driven by the main session, because the leaves have no legs.
- **One agent has an MCP tool** (`docs-lookup` → `mcp__context7__*`). The other 67 are confined to
  `Read/Write/Edit/Bash/Grep/Glob` plus `WebSearch`/`WebFetch` on two marketing agents.

Model allocation is coarse but consistent: **58 sonnet, 6 haiku, 4 opus** — opus on `architect`,
`planner`, `spec-miner` (and oddly `healthcare-reviewer`); haiku on the mechanical six
(`comment-analyzer`, `conversation-analyzer`, `doc-updater`, `docs-lookup`, the two `opensource-*`
packagers). Cheap model for mechanical work, expensive for design. Take the policy.

### 1.2 Tool signature *is* the cluster

There are 14 distinct `tools:` lines, and two of them cover 46 of 68 files:

| `tools:` line | Count | What it means |
|---|---:|---|
| `Read, Grep, Glob, Bash` | 26 | **read-only + can run diagnostics.** Every reviewer. Cannot edit |
| `Read, Write, Edit, Bash, Grep, Glob` | 20 | **can change the repo.** Every build-resolver and fixer |
| `Read, Grep, Glob` | 6 | **cannot even run a command.** `planner`, `architect`, `code-explorer` |
| all others | 16 | one-offs |

That is the most valuable single line in the roster and it is worth stating plainly: **ECC separates
"agents that may change the repo" from "agents that may only look at it" by tool grant, not by
instruction.** A reviewer physically cannot edit the code it reviews. A planner physically cannot
write a file. This is capability-based role separation and it costs one line per file. Take it.

It also cuts the other way, and §2 turns on this: `planner` and `architect` — the two agents whose
whole job is to produce a design document — **have no `Write` tool**. Their output cannot reach
disk. It exists only as text in the transcript.

### 1.3 The cluster count, and how the previous claim scores

The previous pass claimed most of the 68 are "language variants of about four jobs (reviewer,
build-resolver, architect, explorer)". Counted:

| Cluster | Count | Members |
|---|---:|---|
| reviewer — language | 11 | cpp, csharp, fsharp, go, java, kotlin, php, python, rust, swift, typescript |
| reviewer — framework | 5 | django, fastapi, flutter, react, vue |
| reviewer — domain | 7 | code, database, healthcare, mle, network-config, rag-pipeline, security |
| build-resolver | 12 | generic + cpp, dart, django, go, harmonyos, java, kotlin, pytorch, react, rust, swift |
| architect | 5 | generic, code-, a11y-, homelab-, network- |
| GAN trio | 3 | planner, generator, evaluator |
| opensource | 3 | forker, packager, sanitizer |
| **singletons** | **22** | agent-evaluator, chief-of-staff, code-explorer, code-simplifier, comment-analyzer, conversation-analyzer, doc-updater, docs-lookup, e2e-runner, harness-optimizer, loop-operator, marketing-agent, network-troubleshooter, performance-optimizer, planner, pr-test-analyzer, refactor-cleaner, seo-specialist, silent-failure-hunter, spec-miner, tdd-guide, type-design-analyzer |

**Verdict on the claim: right for 59%, wrong for the rest, and the rest is where everything
interesting lives.** 40 of 68 (reviewers + build-resolvers + architects) collapse into **three**
templates, not four. But 22 singletons do not collapse at all, and they contain the only agents in
the repo with a mechanism rather than a checklist — `spec-miner`, `agent-evaluator`, and the GAN
trio. A roster audit that stops at "it's mostly variants" throws away the 32% worth reading.

### 1.4 The templates are literally templates

Diffing headings across six language reviewers (`python`, `go`, `rust`, `typescript`, `php`,
`csharp`) gives one skeleton with no structural variation:

```
## Prompt Defense Baseline → ## Review Priorities → ### CRITICAL — … → ### HIGH — …
→ ### MEDIUM — … → ## Diagnostic Commands → [## Review Output Format] → ## Approval Criteria
→ [## Framework Checks] → [## Reference]
```

The language-specific content is *what fills the severity buckets* and *which shell commands go in
`Diagnostic Commands`*. Nothing else varies. The 12 build-resolvers are the same story with a
different skeleton (`Core Responsibilities → Diagnostic Commands → Resolution Workflow → Common Fix
Patterns → <lang> Troubleshooting → Key Principles → Stop Conditions → Output Format`).

67 of 68 also open with the identical six-line "Prompt Defense Baseline" — confirming at count the
boilerplate `ECC-MINED` §5 item 5 already marked *leave, actively*.

**So the honest description of the bulk is: a severity taxonomy plus a command list, per language** —
a *rules file wearing an agent's frontmatter*. Not an orchestration design, and ECC's own `rules/`
directory already holds the same content organised better (concern × language, one home per rule).

### 1.5 What a "persona plus checklist" agent looks like, and what a designed one looks like

The parent's test — *an agent file that is a persona plus a checklist is not an orchestration
design* — separates the roster cleanly.

**`silent-failure-hunter.md`, 59 lines, in full structure:** `You have zero tolerance for silent
failures` → five "Hunt Targets" bullet lists → `## Output Format: location, severity, issue, impact,
fix recommendation`. No input contract, no stop condition, no artifact, no verification step. It is
a grep list with an attitude. Most of the 68 are this.

**`spec-miner.md`, 217 lines, opus, `tools: Read, Grep, Glob, Bash, Write` — the best agent file in
the repo**, and worth reading properly:

- **Write scope is constrained in the prompt because the frontmatter cannot do it:**
  *"`Write` may only create `openspec/specs/<capability>/spec.md`."* Plus a Bash rule rejecting any
  command that writes outside `openspec/specs/`. They found the gap in their own format and patched
  it with instructions — which is honest, and also exactly why the gap should be closed in the
  format instead.
- **The output is machine-parseable, deliberately:** only `### Requirement:` and `### Invariant:`
  blocks; `<!-- key: value -->` metadata, *one key-value per line*, explicitly "metadata, not
  documentation".
- **It is resumable.** Files it could not read are emitted as `<!-- deferred: file1.md, file2.md -->`
  at the bottom of the spec, so a later session continues rather than restarts. That is
  *"writing partial results to disk"* from `run/SKILL.md` §5 — implemented, in an agent, by them.
- **It is designed to be amended by a later pass:** *"Keep the structure flat so delta operations
  are easy"* — a later agent writes `## ADDED / MODIFIED / REMOVED Requirements` above it.
- It carries an `<!-- uncertainty: <reason> -->` key.

`agent-evaluator.md` (206 lines) is the second-best: it scores another agent's output on five axes
and is forbidden from scoring without evidence — *"DO NOT assign score 5 without citing evidence of
correctness"*, with a workflow step that greps the codebase to verify the previous agent's claims.
Its Bash grant is a read-only allowlist with a genuinely sharp hardening note: always pass
`--no-pager`, *"prefer `-c core.pager=cat` to disable pager-driven code execution via repo-local
`.git/config`"*. That is a real attack this repo's own threat work should already know about.

**The pattern across both: the two well-designed agents are the two that produce a checkable
artifact.** The other 66 produce an opinion, and their file length is spent on taxonomy.

---

## 2 · Is there a real chain, or a suggestion?

### 2.1 Where the chain is encoded — and it is none of the three places we looked

Their stated loop is *plan → test → implement → review → verify → remember → improve*. It is **not**
in `agents/` — 3 of 68 carry an explicit handoff instruction (`flutter-reviewer`, `kotlin-reviewer`,
`rag-pipeline-reviewer`, all of the form *"stop and hand off to `security-reviewer`"*, with no
mechanism behind it) and 3 more merely list neighbours under `## Related`. It is **not** in `hooks/`
(no hook sequences agents), and **not** meaningfully in `commands/` (2 of 94 mention `Task`).

It is in `skills/orch-pipeline/SKILL.md` — 121 lines, in a directory neither this brief nor the
previous pass was pointed at. That file is the real thing and it is good. It contains:

- **A size classifier (Step 0)** scoring three signals — files touched, new dependency/contract,
  design ambiguity — taking the highest tier and **selecting which phases run** via a mask:
  `trivial → 4,5,6`; `small → (1 light),4,5,6`; `standard → 1,2,4,5,6`; `large → 1,2,(3),4,5,6`.
  Tie-breaker: a security trigger or public API is *at least* standard regardless of file count.
- **Six phases** (Intake, Research & Reuse, Plan, Scaffold, Implement-TDD, Review, Commit), each
  *delegating* rather than working inline, with a **phase → agent map that has a fallback column**
  (Implement → `tdd-guide`, escalating to `build-error-resolver` on build breaks).
- **Two human gates**: GATE 1 after Plan, GATE 2 before Commit. *"This family is gated, not
  autonomous. Everything between the gates flows without stopping."*
- **A deterministic security trigger list** — authn/authz, user input, DB queries, filesystem paths,
  external API calls, cryptography, secrets — deciding whether `security-reviewer` joins.
- **A verification section auditing its own execution**: *"size tier was stated"*,
  *"`security-reviewer` ran iff a security trigger was touched"*.

This is a better-articulated build chain than anything currently written down in `scio`. Said
plainly because the brief asks for it: **on the chain document alone, theirs is better than ours.**
`PIPELINE.md` names eight stages and what each consumes and produces; it does not have a size
classifier, a phase mask, a fallback column, an escalation trigger, or a verification section that
audits its own execution. Those five things are the difference between a chain and a chart.

### 2.2 And then the handoff does not exist

`orch-pipeline/SKILL.md` has a section called **Handoff artifacts**. It reads:

> The pipeline carries no hidden state — the planning docs *are* the handoff:
> `task_list` (from Plan) drives the Implement loop.

I checked what `task_list` is. Three findings, each verified:

1. **The string `task_list` appears in zero of the 68 agent files.** The named producer — the
   `planner` agent — has never heard of it. `planner.md`'s own "Plan Format" section emits a
   markdown document with headings `## Overview / ## Requirements / ## Architecture Changes /
   ## Implementation Steps / ## Testing Strategy / ## Risks & Mitigations / ## Success Criteria`.
   No `task_list`.
2. **`planner` cannot write a file** (`tools: Read, Grep, Glob`). Its plan is transcript text; there
   is no artifact for phase 4 to open.
3. **Nothing defines its shape.** `task_list` occurs in one other substantive place —
   `rules/common/development-workflow.md:19` — as the fifth word of *"Generate planning docs before
   coding: PRD, architecture, system_design, tech_doc, task_list"*. That is the entire specification.

And the structural confirmation: **`schemas/` holds 11 JSON schemas** — for install config, hook
config, memory records, plugins, provenance, state store, package manager — **and not one for
anything an agent consumes or produces.** ECC has a validated schema for its own installer's config
file and no schema for the output of the 68 workers the installer installs.

**So: the chain is a suggestion.** The phases are real, the gates are real, the agent map is real,
and between two phases there is a model reading another model's prose out of the transcript and
re-narrating it into a fresh prompt. Each subagent starts from a prompt the orchestrator writes,
not from an artifact the previous agent produced.

### 2.3 The three exceptions, and what they have in common

Three places in ECC *do* pass a real artifact. All three are worth taking, and the reason they work
is the finding of this section.

**(a) The GAN trio — files on disk, numbered, with a schema-by-template.**
`gan-planner` (`tools: … Write`) writes `gan-harness/spec.md` **and** `gan-harness/eval-rubric.md`,
the latter explicitly *"in a format the Evaluator can consume directly"*. `gan-generator` reads
`spec.md` and `feedback/feedback-{n-1}.md`, and writes `generator-state.md`. `gan-evaluator` reads
`eval-rubric.md` + `spec.md` + `generator-state.md`, tests the **live running app**, and writes
`feedback/feedback-{n}.md`. The producer of the rubric is a *different* agent from the consumer, and
the rubric carries weights (design 0.3, originality 0.2, craft 0.3, functionality 0.2) that the
evaluator applies arithmetically. That is a genuine typed-by-template handoff.

**(b) The `multi-*` family — the unified diff as the contract.** `multi-execute.md` states an
invariant it calls **Code Sovereignty**: *"External models have zero filesystem write access, all
modifications by Claude"*, and every external call ends `OUTPUT: Unified Diff Patch ONLY. Strictly
prohibit any actual modifications.` A unified diff is a real type: it applies or it does not, and
the check is `git apply --check`, not a judgment. One writer, N proposers, machine-verifiable
handoff. (Caveat, stated because it matters: this family depends on an external `ccg-workflow`
runtime that *"is not part of the base ECC install"* — so it is a design one can read, not a thing
one can run.)

**(c) The worktree orchestrator — a pre-created artifact skeleton.**
`scripts/lib/tmux-worktree-orchestrator.js` creates, *before any worker starts*, three files per
worker in a coordination directory: `task.md`, `handoff.md`, `status.md`. `handoff.md` is written
out with its sections already present and every one filled with `- Pending`:

```
# Handoff: <worker>
## Summary            - Pending
## Files Changed      - Pending
## Tests / Verification - Pending
## Follow-ups         - Pending
```

The consumer knows the shape before the producer runs, and an unfilled section reads as `Pending`
rather than being silently absent. `status.md` carries `- State:` in a **separate file from the
result**, so "is it done" and "what did it produce" are different channels. This is the cheapest
real handoff mechanism I found anywhere, it is ~30 lines of JavaScript, and it needs no schema
language.

**What the three have in common: not one of them invented its own type.** OpenSpec supplied
`spec-miner`'s block format; the unified-diff format supplied `multi-execute`'s; a shell script
supplied the worktree skeleton; and the GAN rubric is a template one agent wrote for another because
a *command* forced them into a loop. **Where ECC had to invent a handoff itself — `task_list` — it
produced a word.** That is the lesson to carry into §5: a handoff exists when something outside the
prompt defines its shape, and does not exist when a prompt merely names it.

Against our own: `Contract` and `BuildPackage` are typed handoffs in code, produced and consumed by
programs, validated at the boundary. **ECC has no equivalent.** Its nearest approach is (c), a
markdown skeleton with four fixed headings — and honestly, (c) is the right *cheap* answer for a
build-process chain where the producer and consumer are both models and no runtime exists yet.

---

## 3 · Delegation mechanics and cost control

### 3.1 How a subagent is actually invoked

There is exactly one mechanism and one honest description of it.

**Invocation is by `description` match, from the main session.** The `description` field is the
dispatch key, written as an imperative aimed at the orchestrator: `code-reviewer` says *"Use
immediately after writing or modifying code. MUST BE USED for all code changes."* Capitalised urgency
is the entire routing logic — there is no router, no scorer, no registry. `rules/common/agents.md`
supplies a hand-written table of agents to use unprompted, and **that table lists 11 of the 68.**

**The context a subagent gets** is whatever the orchestrator types into the `Task` call, plus its tool
grant; the return channel is stated bluntly and correctly as **"Your final message IS the
deliverable."** Prose in, prose out.

**Depth is capped by instruction in one place** — the worktree task file's *"Do not spawn subagents or
external agents for this task."* Redundant with the harder fact that no agent has `Task` at all. The
two give an effective **maximum delegation depth of 1**: sound, arrived at half by intent and half by
omission.

### 3.2 The Delegation Completion Contract — the best 200 words in ECC

`rules/common/agents.md` closes with three rules that *"apply to every agent at every depth"*:

1. **"Your final message IS the deliverable.** Never end your turn with 'waiting for background
   agents' — a spawned task is not a completed task. Ending your turn while children are running
   orphans their results."
2. **"If you delegate, you own collection.** Wait for results, integrate them, then return.
   Fire-and-forget delegation is forbidden."
3. **"Decompose only when the work cannot fit in one context. Do not re-delegate a task already
   sized for a single agent — depth is an outcome, not a plan."**

And then the rationale, which is why this is worth taking:

> Observed failure mode — research agents followed "Parallel Task Execution" above, spawned children,
> and returned "waiting" as their final answer. All children completed successfully but their results
> were orphaned. **The parallel rule without a completion contract produces zombie tasks.**

This is a rule written from a measured incident — the same provenance that makes Layer E's
instrumentation guardrail trustworthy — and it identifies a failure our own rule does not cover.
`run/SKILL.md` §5 says *"budget before parallel work, deterministic passes first, model passes last
and in small batches, writing partial results to disk"*. Every clause is about **dispatch**. Not one
is about **collection**. Rule 3 is also sharper than anything we have written on depth: *depth is an
outcome, not a plan* is the correct answer to the temptation to draw an org chart of agents.

**Verdict: take the mechanism, all three rules, verbatim in substance.** What would have to be true:
nothing. It is prose, it costs nothing, and it patches a real gap in `run/SKILL.md` §5.

### 3.3 Cost control: they measure and never enforce; we enforce and never measure

The contrast is exact, and both halves are useful.

**ECC has no cost enforcement of any kind** — no budget, no ceiling, no refusal, no fan-out cap,
anywhere in the 68 agents, 94 commands or 23 hooks. What exists is `scripts/hooks/cost-tracker.js`
(239 lines, on `Stop`): one JSONL row per session to `~/.claude/metrics/costs.jsonl`, preferring the
harness's `cost.total_cost_usd` and falling back to a token-priced estimate, under its own contract
comment *"Non-blocking — never fail the Stop hook."* An odometer with no brake.

Worse, the doctrine pushes the other way: **"ALWAYS use parallel Task execution for independent
operations"**, illustrated with a three-agent fan-out marked `# GOOD`, with no number, cap or cost
statement anywhere near it. Our §5 rule *budget before parallel work* is the direct contradiction,
and ours is right — "ALWAYS parallelise" without a budget is how one diff becomes five model calls.

**Where ECC is nonetheless ahead of us, and Layer E §3.6 already concedes it:** they have telemetry.
`costs.jsonl` per session, `skill-runs.jsonl` per skill invocation (`ECC-MINED` §5 item 10 already
took this), and an `evaluate-session.js` on `Stop`. Scio has `Spend` — a build-scoped accumulator
with one enforcement point and a real ceiling that refuses — and **no persisted record of what any
build actually cost.** So:

| | Enforcement | Telemetry |
|---|---|---|
| **Scio** | `Spend`, one accumulator, refuses (checked after the call — Layer E §2.2) | none — Layer E §3.6 |
| **ECC** | none, anywhere | `costs.jsonl` + `skill-runs.jsonl`, per session, zero tokens |

Neither is complete, and the missing halves are different. Take their JSONL-append-on-`Stop` shape
for the build-process chain — identifiers and numbers only, no model call, no tokens — because it
answers *"what did that pipeline run cost"*, which we currently cannot answer at all.

### 3.4 The one genuine budget mechanism, and it is in a hook

`scripts/hooks/stop-format-typecheck.js` is the only place in ECC where a total budget is divided
*before* work is dispatched: `TOTAL_BUDGET_MS = 270_000` inside a 300s hook timeout, then
`perBatchMs = floor(TOTAL_BUDGET_MS / totalBatches)`, with files grouped by project root and by
`tsconfig` directory so each batch gets its slice — *"so the cumulative total stays within the Stop
hook wall-clock limit even in large monorepos."* That is *"budget before parallel work"* in eleven
lines, for a deterministic pass, with a hard outer bound. The idea transfers directly. What the file
does with the result does not — §4.3.

### 3.5 Right-sizing as cost control — the best cost idea in the repo, and it is not about cost

`orch-pipeline`'s Step 0 size classifier (§2.1) is the strongest cost mechanism in ECC precisely
because it is not framed as one. *"Ceremony scales to blast radius."* A trivial change runs phases
4→5→6 and skips Research and Plan entirely; a large one runs all six. The classifier is three
signals and a max, it is stated in one line so the user can override, and it decides **which agents
are never invoked**.

Not spending is cheaper than spending carefully. Our §5 rule optimises *how* to dispatch; theirs
decides *whether*. Both are needed, and we do not have theirs.

**Take the mechanism.** What would have to be true for it to work here: our stages have to be
skippable, and `PIPELINE.md`'s eight stages are currently written as though all eight always run.
For a one-line doc fix, stages 1–4 are ceremony. A phase mask keyed to a stated tier is the fix,
and it is also a partial answer to `PIPELINE.md` §2's real problem — a pipeline where *every stage
adds* is affordable only if most requests skip most stages.

---

## 4 · Commands and hooks

### 4.1 The 94 commands are entry points, and ECC says so out loud

They are not shims (`ECC-MINED` §4 established that) and they are not compositions either.
Counted: **2 of 94** mention the `Task` tool (`gan-build`, `plan`); **13 of 94** name any agent from
`agents/`. The other 81 are standalone prompt documents averaging 131 lines that do the work inline.

And the decisive line is in `plan.md`, one of the two: *"Run inline by default. **Do not call the
Task tool or any subagent by default.** This keeps `/plan` usable from plugin installs that ship
commands without agent files."* The decoupling is deliberate and its reason is packaging — a command
that delegates breaks when the agents are absent. So `plan.md` duplicates inline the work the
`planner` agent also does: **two implementations of one job that can drift, with nothing able to
detect it.**

That leaves `gan-build.md` as the *only* command that composes agents into a workflow (§4.2). The
`orch-*` commands (36–39 lines) are wrappers invoking an `orch-*` **skill**, which delegates to
`orch-pipeline` — the composition lives two layers below the command, which is the right layering and
the opposite of what the directory listing suggests.

**Take:** the layering — thin command → skill that holds the pipeline → agents. **Leave:** 94 entry
points. **Take the warning:** an inline duplicate of a delegated job is drift with no detector.

### 4.2 `gan-build` — the loop, and its stop conditions

103 lines of prose pseudocode that the main session interprets. Nothing compiles it; the `while` loop
is a model reading a code block and choosing to obey it. Defaults: `--max-iterations 15`,
`--pass-threshold 7.0`, `--eval-mode playwright`. Phase 1 launches `gan-planner` via Task and *waits
for the files*; Phase 2 alternates generator and evaluator, each launched via Task, each reading and
writing numbered files; after each round the orchestrator **reads `feedback-{n}.md` and parses the
weighted total** to decide whether to continue.

Two stop conditions, and the second is the valuable one:

```
if score >= pass_threshold: break
if iteration >= 3 and score has not improved in last 2 iterations:
    Log "PLATEAU detected — stopping early"; break
```

A **plateau detector**: an adaptive stop that ends the loop when the *signal* stops improving, rather
than when a counter runs out. Carried forward to §6.

Two defects worth recording so the mechanism is taken cleanly:

- **`gan-evaluator` is instructed to use tools it was not granted.** Its body says *"Use Playwright
  MCP"* and lists `mcp__playwright__navigate/click/fill/screenshot`; its frontmatter is
  `tools: Read, Write, Bash, Grep, Glob` — **no MCP tool at all.** The MCP path is dead; only the
  `npx playwright` Bash fallback runs. This is the frontmatter discipline `ECC-MINED` §4 praised,
  undermined from the other side: declaring tools is worth little if nothing checks the prompt
  against the declaration. **A lint greping agent bodies for tool names absent from `tools:` is ~20
  lines and would have caught it.**
- **`gan-generator` is told not to disagree:** *"If a suggestion seems wrong, still try it — the
  Evaluator sees things you don't."* That converts a reviewer's opinion into a command and removes
  the only check on an evaluator that hallucinates a defect. Leave, actively.

### 4.3 The 23 hooks, and what they do about agents

23 entries across 7 events: **PreToolUse 8, Stop 7, SessionStart 2, PostToolUse 2, PostToolUseFailure
2, PreCompact 1, SessionEnd 1.**

**Nothing coordinates agents.** No hook launches, sequences, budgets or routes a subagent. The
closest is `PostToolUseFailure` on matcher `Skill` → `skill-run-tracker.js`, which is observation, and
which `ECC-MINED` §5 item 10 already took.

**`SessionStart` (2 entries)** — an 85-line shim resolving the plugin root, delegating to
`session-start.js` (798 lines) whose injection budget `ECC-MINED` §5 item 7 already took. **Nothing
about agents is injected.** One part not yet taken: the shim passes a **hook profile** gate
(`minimal,standard,strict`), so every hook is tagged with the profiles it runs under and a user on
`minimal` gets a different lifecycle without editing `hooks.json`. Install-time selection applied to
hooks — the same shape as their `rules/` matrix, and the right answer to "23 hooks is too many".

**`Stop` (7 entries) — and only one of them gates.** Exactly one emits
`{ decision: 'block', reason }`: `plan-canvas-pending.js`. The other six always exit 0. The important
one is `stop-format-typecheck.js`: it spends up to **270 seconds** running formatters and `tsc` in
budgeted batches (§3.4) — and then:

```js
function run(rawInput) { try { main(); } catch (err) { … } return rawInput; }
```

**The typecheck result is returned nowhere and shown to nobody.** The hook exists to auto-format as a
side effect; the type errors it just spent four and a half minutes computing are discarded. It is not
a gate, and the file name says it is.

That is `LAYER-E-BUILD.md` §2.6's *"three matrix rankings are unused"* in a different repo: work
computed and then not read. The lesson is ours as much as theirs — **a check that runs and is not
read is worse than one that does not run, because its presence in the file listing is taken as
coverage.** Their `Stop` array looks like a seven-gate quality bar; it is one gate and six observers.

---

## 5 · What our build agents should be, as files

Every agent that has built this repo so far was a one-off prompt written from scratch. The fix is not
68 files. It is **seven**, plus three mechanisms that make them a chain rather than a roster.

### 5.1 The three mechanisms first — they matter more than the roster

**(1) The handoff is a file that exists before the producer runs** — from
`tmux-worktree-orchestrator.js` (§2.3c), not from anything in `agents/`. Before stage *n* dispatches,
the orchestrator creates `pipeline/<run-id>/<stage>.md` with its headings present and each filled
`- Pending`. The producer fills it; the consumer opens that path, not the transcript. This gives us
`task_list`'s intent without its fate: **the shape is defined outside the prompt, so it cannot be a
word nobody implemented.** Two fields on every handoff, from `spec-miner`: `<!-- deferred: … -->` and
`<!-- uncertainty: … -->`, one key per line, greppable. It is the cheap stand-in for
`Contract`/`BuildPackage` — markdown, not a type — and should be replaced by a real schema the moment
stage 3 gives us one.

**(2) Capability separation by tool grant, not by instruction** — ECC's single best structural habit
(§1.2): three grants only — analyst (`Read, Grep, Glob`), evidence-gatherer (`+ Bash`, no write),
and coder (`Read, Write, Edit, Bash, Grep, Glob`) — as applied in the table below, plus `Write`
narrowed by prompt to one path
prefix (`spec-miner`-style) on every agent whose only output is its handoff file. **A reviewer that
physically cannot edit the code it reviews is worth more than a reviewer told not to.**

**(3) `Task` on no agent. Depth 1, and the Delegation Completion Contract in the run skill.** §3.2's
three rules go into `run/SKILL.md` §5 next to *budget before parallel work*, because that rule
governs dispatch and says nothing about collection — and ECC's incident report says collection is
where it breaks.

### 5.2 The seven files

Language-neutral, per `PIPELINE.md` §3 — the stack is stage 3's output and naming languages now
would staff a decision the architect has not made.

| Agent file | Stage | Tool grant | Consumes | Produces |
|---|---|---|---|---|
| `scan-agent` | 0 Tooling | `Read, Grep, Glob, WebSearch, WebFetch` | a domain word | `scan/<topic>.md` — catalogue with descriptions + dates, per `ECC-MINED` §4's `mcp-configs` shape |
| `idea-miner` | 1 Brainstorm | `Read, Grep, Glob` | `docs/next/` **by retrieval**, code graph | `ideas.md` — one shape per idea, scored |
| `idea-validator` | 2 Validate | `Read, Grep, Glob` + scoped `Write` | `ideas.md` | `validated.md` — **at most N per layer**, every rejection carrying its reason |
| `architect-agent` | 3 Architect | `Read, Grep, Glob` + `Write` scoped to `docs/decisions/` | `validated.md`, settled ADRs | ADR drafts, one decision per file |
| `build-planner` | 4 Plan | `Read, Grep, Glob` + scoped `Write` | the architecture | `plan.md` — thin vertical slices, ordered, each with its `State` verdict from `PIPELINE.md` §4 |
| `slice-coder` | 5 Code | `Read, Write, Edit, Bash, Grep, Glob` | **one** slice from `plan.md` | code + `handoff-<slice>.md` (Summary / Files Changed / Tests / Follow-ups) |
| `evidence-auditor` | 6 Test + 7 Review | `Read, Grep, Glob, Bash` | any agent's handoff | `findings.md` — every claim marked verified / unverified with `file:line` |

Notes that are load-bearing:

- **`idea-validator` exists to subtract, and its output cap is its whole point.** `PIPELINE.md` §2
  already says validation needs *"a number, not a mood"*. An agent file is where that number gets
  written down and where a run can be checked against it.
- **`evidence-auditor` covers two stages deliberately**, and is modelled on ECC's `agent-evaluator`
  (§1.5): it may not mark a claim verified without citing `file:line`, and its Bash grant is
  read-only with the `--no-pager` hardening. It is the enforcement arm of `run/SKILL.md` §5's
  *"findings are claims, not facts"* — which today is a rule with nobody assigned to it.
- **`slice-coder` takes one slice, never a plan.** *Decompose only when the work cannot fit in one
  context* (§3.2 rule 3). The orchestrator loops; the coder does not.
- **Do not write a `planner` and a `/plan` that both plan** (§4.1). One implementation per job.

### 5.3 The two things wrapped around the seven

**A size classifier at the front, with a phase mask** — `orch-pipeline` Step 0 (§3.5) adapted to
eight stages: score files touched, whether a new contract or dependency appears, and design
ambiguity; take the highest tier; state it in one line so it can be overridden; run only the stages
the mask names. A typo fix runs 5 and 7; a new layer runs all eight. This is the cost lever, and
`PIPELINE.md` §2's every-stage-adds problem is unaffordable without it.

**Two human gates, not autonomy** — GATE 1 after stage 4, GATE 2 before commit. Already how this
project works; writing it into the chain makes it checkable.

**A `Stop` hook appending one JSONL row per run** — run id, stages executed, tier, agents dispatched,
wall clock, cost if the harness exposes it. Identifiers and numbers, zero tokens (§3.3). It answers
*"what did that run cost, and which of the seven agents ever fire"* — the question
`skill-runs.jsonl` answers for skills, which we already decided to take.

---

## 6 · What this says about the product's chain

Layer E's verified defect: **four relay passes with no external feedback, capped at 4 by default,
next to a repair loop that has seven validation agents, a console classifier and an interaction
runner behind it, capped at 3.** The money is in the loop without the signal.

**Does ECC suggest a better shape? On three narrow points, yes. On the whole, no — their chain is
looser than ours, and by a wide margin.**

The three points, in order of value:

**(1) The plateau detector is the one mechanism worth importing (§4.2).** Scio's caps are both
static: `MAX_PASSES = 4`, `max_attempts = 3`. Kiecker et al. (July 2026) justifies **3** as a fixed
cap and Layer E §2.1 is right to cite it — but a fixed cap spends the third attempt whether or not
the second moved anything. Scio is unusually well placed to make that adaptive, because its gates
already emit structured findings: **a repair attempt returning the same finding set as the previous
attempt is a plateau, and that is a set comparison, not a judgment.** Cheaper than tuning the cap,
deterministic, and it composes with the existing cap rather than replacing it. Their threshold of 15
iterations is unbacked — take the detector, leave the number.

**(2) Role separation as an argument for keeping the relay's *last* pass, not its middle ones.**
`gan-generator` is told *"Don't self-evaluate — your job is to build, not to judge. The Evaluator
judges"*, and the Evaluator is a different agent with `Bash`, a rubric it did not write, and a live
app to test. That is the structural version of Layer E §2.1's finding: ECC did not make Scio's
mistake, because it never gave the generator a review pass at all — it gave the *reviewer* execution
and made it a separate worker. It supports `SCIO_MODEL_PASSES=1` (two passes: generate, then a
final) and it supports spending the difference on the loop that has gates. It does **not** rescue
passes 2 and 3.

**(3) One caution that cuts against ECC and toward us.** `gan-generator` is also told *"If a
suggestion seems wrong, still try it — the Evaluator sees things you don't."* Layer E's constraint —
*a model's opinion may not stand in for a deterministic check* — is the opposite instruction, and
ours is right. If Scio ever adds a critique channel that the repair loop must obey, that sentence is
the failure mode to design against.

**What ECC has nothing to offer on.** Their evaluator's feedback is a model scoring a rubric 1–10
and writing prose; Scio's is seven validation agents, a console classifier, an interaction runner and
a typecheck. Their loop has no budget, no ceiling and no refusal; Scio has `Spend`. Their handoff is
markdown; ours is `Contract` and `BuildPackage`, validated in code. Their gates do not roll back;
`core/verifier.py` does. **On the product chain, we are ahead everywhere except the stop condition.**

The honest summary: **ECC contributes one loop mechanism to Layer E and nothing else.** The relay
question stays where §2.1 left it — a default change and a measurement — and nothing in 68 agents,
94 commands or 23 hooks argues otherwise.

---

## 7 · Verdict table

Numbering continues from `ECC-MINED` §5 (which ended at 18) so the two tables compose.

| # | Item | Verdict | What would have to be true |
|---|---|---|---|
| 19 | **Capability separation by tool grant** — reviewers get no `Write`, planners get no `Bash` (§1.2) | **take the mechanism** | Three grants, applied when we define the seven agents. Costs one line per file |
| 20 | **`orch-pipeline`'s size classifier + phase mask** (§2.1, §3.5) | **take the mechanism** | `PIPELINE.md`'s eight stages must become skippable and the tier must be stated aloud. This is the cost lever |
| 21 | **The two human gates** — after Plan, before Commit (§2.1) | **take** | Nothing. It is how we already work; writing it down makes it checkable |
| 22 | **Delegation Completion Contract**, all three rules (§3.2) | **take the mechanism** | Goes into `run/SKILL.md` §5, which covers dispatch and not collection |
| 23 | **Pre-created handoff skeleton** — `handoff.md` with fixed headings, filled `Pending` (§2.3c) | **take the mechanism** | The orchestrator creates the file before dispatching. Replace with a real schema once stage 3 exists |
| 24 | **`spec-miner`'s `<!-- deferred: -->` / `<!-- uncertainty: -->` keys** (§1.5) | **take** | One key-value per line, greppable. Implements `run/SKILL.md` §5's partial-results rule |
| 25 | **`agent-evaluator`'s evidence rule** — no top score without `file:line` (§1.5) | **take the idea** | Becomes `evidence-auditor`. Its read-only Bash allowlist and `--no-pager` hardening come with it |
| 26 | **Plateau detector** — stop when the finding set stops changing (§4.2, §6) | **take the mechanism** | Scio's gates already emit structured findings; a repeat finding set is a set comparison. Take the detector, leave their 15 |
| 27 | **Unified diff as the inter-model contract** (`multi-execute` Code Sovereignty, §2.3b) | **take the idea** | Only if we ever run a non-Claude proposer. One writer, N proposers, `git apply --check` as the gate |
| 28 | **`TOTAL_BUDGET_MS` split across batches before dispatch** (§3.4) | **take the idea** | Eleven lines. Applies to any deterministic fan-out we run |
| 29 | **JSONL append on `Stop`** for pipeline runs (§3.3) | **take** | Identifiers and numbers only. We have enforcement and no telemetry; this is the missing half |
| 30 | **Hook profile gating** (`minimal,standard,strict`) (§4.3) | **take the shape** | Only once we have more than a couple of hooks. Install-time selection, same shape as their `rules/` matrix |
| 31 | **Lint that greps an agent body for tools absent from `tools:`** (§4.2) | **take — and it is ours to invent** | ~20 lines. ECC needs it and does not have it; `gan-evaluator` is the proof |
| 32 | `task_list` and the "planning docs are the handoff" claim (§2.2) | **leave — and learn from it** | Zero occurrences in 68 agent files; producer has no `Write`; no schema. A named handoff nobody implemented |
| 33 | The 68-agent roster, the reviewer/build-resolver templates (§1.3, §1.4) | **leave** | 40 of 68 are three templates over a severity taxonomy. That content belongs in `rules/`, which they already have |
| 34 | "ALWAYS use parallel Task execution" (§3.3) | **leave, actively** | Directly contradicts `run/SKILL.md` §5. Ours is right |
| 35 | "If a suggestion seems wrong, still try it" (`gan-generator`, §4.2, §6) | **leave, actively** | Inverts Layer E's constraint that a model's opinion may not override a deterministic check |
| 36 | `stop-format-typecheck` as a quality gate (§4.3) | **leave** | Spends 270s and returns `rawInput` unchanged. Take the budget split (#28), not the hook |
| 37 | Commands as compositions (§4.1) | **leave** | 2 of 94 delegate; `plan.md` forbids delegation by design. Take the layering — thin command → skill → agents |

**Nine takes, five ideas, one shape, six leaves.** The concentration is telling: every "take" is a
*mechanism for controlling a chain* — grants, gates, budgets, stop conditions, handoff skeletons —
and every "leave" is *content*. ECC is worth reading for its plumbing, not its roster: the same
verdict `ECC-MINED` reached about its skills, arrived at from a different direction.

The one sentence that survives everything: **their chain document is better than ours, and their
chain is worse.** `orch-pipeline/SKILL.md` has a classifier, a phase mask, an escalation column and
a self-audit that `PIPELINE.md` should have; underneath it, agents hand each other prose out of a
transcript and the one artifact it names does not exist. We have the opposite problem — real typed
handoffs in `Contract` and `BuildPackage`, and eight stages with no way to skip any.

---

*All findings above come from files read on 2026-08-26 at commit `d8409a4`. Counts in tables were
counted, not quoted. Where a claim rests on a single file it is named with its path in the text.*
