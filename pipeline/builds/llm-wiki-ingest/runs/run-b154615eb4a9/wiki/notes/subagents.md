---
title: Subagents
sources:
  - url: https://code.claude.com/docs/en/sub-agents
    fetched: 2026-08-27
status: verified
tags: [claude-code, subagents, context, mechanics]
related: ["[[skill-anatomy]]", "[[dynamic-workflows]]", "[[hooks]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[api-agent-loop]]", "[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[testing-skills-methodology]]", "[[loop-engineering-and-fable-prompting]]", "[[model-agnostic-agent-harnesses]]", "[[harness-over-model-prime-agent]]"]
---

# Subagents

Specialized assistants that run in an **isolated context window** and return only a
summary — keeping verbose work (searches, logs, file contents) out of the main
thread. Each has a custom system prompt, restricted tools, and its own context.

## Locations & precedence (highest → lowest)

1. Managed settings → 2. `--agents` CLI flag → 3. `.claude/agents/` (project) →
4. `~/.claude/agents/` (user) → 5. plugin `agents/`. Name conflicts: highest
priority wins; closest-to-cwd wins among project dirs.

## What loads into a (non-fork) subagent at startup

Custom system prompt + env details (NOT the full Claude Code prompt); the task
message Claude writes; **the whole CLAUDE.md hierarchy**; git status snapshot;
full content of skills named in `skills:`; sibling roster for `SendMessage`.
**Does NOT get:** main conversation history, main auto-memory, previously invoked
skills, prior tool results. **Exception:** built-in Explore and Plan skip CLAUDE.md
and git status (that is why they stay small).

## Frontmatter fields

`name`, `description` (required — drives delegation). Optional: `tools`
(allowlist; **omitted = inherit ALL**), `disallowedTools`, `model` (default
`inherit`; `sonnet`/`opus`/`haiku`/`fable`/full-id), `permissionMode`, `maxTurns`,
`skills` (preload full content), `mcpServers`, `hooks`, `memory`
(`user`/`project`/`local`), `background`, `effort`, `isolation: worktree`, `color`.

## Skills relationship (the key inversion)

The subagent `skills:` field is the **inverse** of a skill's `context: fork`. With
`skills:`, the subagent owns its system prompt and pulls skill content in; with
`context: fork`, a skill's content is injected into a chosen agent. A subagent can
still discover other skills via the Skill tool (unless `Skill` is removed from
`tools`); can't preload `disable-model-invocation: true` skills.

## Foreground vs background

Foreground blocks the main thread, passes permission prompts through, gets the
**full** tool set. Background runs concurrently, surfaces prompts in the main
session, and gets a **restricted** built-in tool set (Read/Grep/Glob/Bash/Edit/
Write/WebFetch/WebSearch/Skill/SendMessage/… — most others removed; MCP inherited).
In interactive sessions fork mode is on by default → spawns run in background.

## Fork

Inherits the ENTIRE conversation (system prompt, tools, model, full history) but
isolates tool calls. Use when a fresh subagent would need too much background, or
to try approaches in parallel. `/subtask <task>` (v2.1.212+). Forks reuse the
parent prompt cache (cheaper) and cannot nest.

## MEASURED: `.claude/rules/` does NOT reach a subagent

Tested 2026-08-28 with a canary probe (a rule file containing a unique phrase, a
subagent asked to report any canary in its context **before** touching any tool).

- **Result: the canary was absent.** The subagent correctly answered "no canary in
  context" rather than guessing, then read the file and confirmed the miss.
- **Only `CLAUDE.md` was injected** as a project instruction file. Also present:
  the `userEmail`/`currentDate` blocks, deferred-tool names, MCP server
  instructions, and skill **descriptions only** (names + one-liners, not bodies).
- Both an unconditioned rule and a `paths:`-scoped rule were planted; neither
  appeared.

**Design consequence: an agent's rules cannot live in `.claude/rules/`.** They must
go where a subagent actually loads from — `CLAUDE.md` (repo-wide, so every agent
gets every rule), the agent body itself (tier 0, which is what a system prompt is
for), a preloaded skill (tier 1), or a reference file the procedure opens (tier 3).

**Scope limit, stated by the probe itself:** this tests the *subagent* path only.
Whether the main session loads `.claude/rules/` is NOT established here — the probe
file was created mid-session, and rules load at session start, so the parent's
failure to see it proves nothing. Do not generalise this to the main session.

## Documented limits (re-verified 2026-08-28)

| Limit | Value |
|---|---|
| **Combined descriptions of all non-built-in subagents** | **15,000 tokens.** Claude Code shows a startup warning with the total when exceeded. A **shared** budget across the whole roster — it bites as the roster grows, not per agent |
| Nesting depth | **3** (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` disables nesting). At the depth limit Claude Code **withholds the `Agent` tool from every subagent except a fork** |
| Concurrent subagents | **20** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) |
| `MEMORY.md` in the subagent system prompt | first **200 lines or 25 KB**, whichever comes first |
| Transcript retention | `cleanupPeriodDays`, default 30 |
| `maxTurns` | field exists; **no default or maximum documented** |

**Explicitly NOT documented:** maximum size of the agent definition file; maximum
system-prompt length; context window (inherits from the model); total subagents
over a session's lifetime; truncation behaviour for oversized inputs.

So **there is no size cap on an agent body.** Against Opus 5's 1M-token context an
agent file is a rounding error. Keeping it short is a *quality* argument — the body
becomes the system prompt and shapes every turn — not a mechanical one. Say it that
way; do not dress it as a limit.

## Limits & gotchas

Transcripts at
`~/.claude/projects/{project}/{sessionId}/subagents/agent-{id}.jsonl`, survive
compaction, deleted after `cleanupPeriodDays` (30). Explore/Plan can't be resumed
(one-shot). Easy to get wrong: `tools` omitted inherits all (not none); background
silently drops non-listed built-ins.

## For this project

Subagents are the fan-out engine behind `deep-reading` ingestion and the eval
harness. Note for the factory: a normal subagent DOES load this repo's CLAUDE.md
(so doc-driven rules apply), but Explore/Plan do not — pick `general-purpose` when
the rules must hold.

---

## A subagent has no Task tool here — MEASURED 2026-09-01

Running the `skill-builder` agent unaided on a full build surfaced a limit nothing in
our design had accounted for: **the agent could not dispatch subagents.** No `Task` tool
was available to it.

It worked around this by driving the headless CLI — `claude -p` — from fresh scratch
directories outside the repo, so none of the library's 88 skills loaded into the runs it
started. Never more than two concurrent. It captured cost per run.

**Verdict MEASURED**, n=1 agent, one environment. What it establishes is that the
capability cannot be *assumed*; it does not establish the rule for every host.

**Why it matters beyond the workaround.** Every orchestrating talent we own — `factory`,
`dispatching-parallel-agents`, `subagent-driven-development`, the `skill-builder` agent
itself — is written as though an agent can fan out. One level down, in this environment,
it cannot. An orchestrator that assumes it will either stop or improvise, and improvising
is what happened here.

Two consequences worth carrying:

- **A dispatching talent should state what it needs and check for it**, rather than
  discovering the absence mid-run.
- **The workaround is better than it looks.** Fresh scratch directories mean the runs
  loaded no skills at all, which is a *cleaner* baseline than our own harness produces —
  ours runs the without-arm inside a repo where 88 descriptions are in the listing. Worth
  copying deliberately rather than inheriting by accident.

## What a dispatched chain actually costs — MEASURED 2026-09-01

One agent, one full 38-phase build, 55 minutes wall clock. The distribution is not where
I predicted, and the prediction is worth recording alongside the number because it was
wrong in an instructive way.

| | |
| --- | --- |
| total wall clock | 55 min |
| logged run time | 15 min, 18 dispatched runs |
| **coordinator's own turns** | **roughly half the wall clock** |
| total tokens | 3.58M |
| **share in 6 probe/arm runs** | **82%**, at 420–570k each |

**The first diagnosis was wrong.** From my own earlier build I concluded the wall clock
was the cold sessions. It was not: in that build I was the coordinator and my turns never
appeared in any measurement. When the coordinator is an agent, its turns become visible
and they are half the cost. A cost model built from a run where you were the orchestrator
will systematically under-count orchestration.

**Why the six runs dominate the tokens:** each pasted the same fixture and the same method
body inline. Four runs over one fixture pay for it four times, and text that shifts
position in every prompt cannot be served from the prompt cache. Hand a run a PATH to
anything it can look up; paste only what it must not be able to find.

**And 12 of the 18 runs logged no duration at all** — only tokens. Two thirds of the run
was invisible to anyone trying to make it faster. Same class of loss as an unrecorded
spend: available at the moment, unrecoverable afterwards.

## The headless run's observable surface — MEASURED 2026-09-01

Measured directly by running `claude -p "<prompt>" --output-format json` from a fresh scratch
directory on this box (CLI 2.1.257), n=3 runs. Recorded because a benchmark that reads this
payload wrongly produces a **wrong number, not an error** — and did, twice, before it was fixed
(`pipeline/bench/`, prereg amendment 2).

**Top-level keys of the JSON result** (verbatim from a run):
`api_error_status`, `duration_api_ms`, `duration_ms`, `fast_mode_disabled_reason`,
`fast_mode_state`, `is_error`, `modelUsage`, `num_turns`, `permission_denials`,
`queued_turn_count`, `result`, `session_id`, `stop_reason`, `subagent_stats`, `subtype`,
`terminal_reason`, `time_origin_ms`, `time_to_request_from_spawn_ms`, `time_to_request_ms`,
`total_cost_usd`, `ttft_ms`, `type`, `usage`, `uuid`, `warm_spare_claimed`.

Three findings, each of which cost a defect to learn:

1. **A headless run cannot read outside its own working directory.** Given an absolute path into
   another tree it does not error — it *declines*, in prose, in about 6 seconds, and exits 0 with
   a well-formed JSON result. Any harness that times such runs is timing a refusal. Copy the
   inputs into the run's cwd. **MEASURED**, n=1, reproduced by the fix.
2. **`modelUsage` has MORE THAN ONE key.** A run pinned with `--model claude-sonnet-5` reported
   `['claude-haiku-4-5-20251001', 'claude-sonnet-5']` — the requested model plus an auxiliary the
   CLI uses internally. Reading `list(modelUsage)[0]` therefore reports the *auxiliary* model for
   a correctly-served run. Check membership, never position. **REPEATED**, n=3, every run.
3. **`--model` does take effect** in a headless run; the apparent mismatch in (2) was entirely the
   reader's. **REPEATED**, n=3.

**`duration_api_ms` vs `duration_ms` splits waiting-on-the-API from local work** — the quantity
that decides whether a dispatch cap is protecting against real contention. It varies sharply by
model on the same box and the same prompt:

| Model | `duration_api_ms` / `duration_ms` | Share NOT spent waiting on the API |
|---|---|---|
| `claude-sonnet-5` | 5079 / 10786 | ~47% local |
| `claude-opus-5` | 11917 / 15177 | ~22% local |

**Weak: n=1 each, both taken under load with a build running**, which inflates the local share in
both rows. Directional only. What it does establish is that **"is this workload network-bound?"
has no model-independent answer** — the heavier model spends proportionally more of its wall clock
waiting, so a dispatch cap tuned on one model is not evidence about another. A benchmark of
concurrency must therefore pin the model it is answering for. The clean version is the registered
benchmark at `pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md`, pinned to Opus 5, which has not
run.

## Dispatch concurrency 2 vs 4 on a 4-core box — MEASURED 2026-09-01

Preregistered before any number existed (`pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md`),
rows in `pipeline/bench/runs/`. 56 headless `claude -p` runs on `claude-opus-5`, 8 per batch,
3 valid batches per arm, arms alternated, $9.18.

| | concurrency 2 | concurrency 4 |
|---|---|---|
| Batch wall clock, median of 3 | 59.0s | **32.8s** |
| Per-run duration, median | 13.6s | 15.1s |
| Failed runs | 0 | 0 |

**Ratio 0.556** against a threshold of 0.70 fixed in advance. Per-run cost of the higher
concurrency is **1.11x**, well inside the 1.5x guardrail. **REPEATED**, 3 batches per arm.

**The thing worth carrying to another project:** the prior value came from `min(16, cores-2)`,
a formula that models **CPU** contention. The median run here spent **73% of its wall clock
waiting on the API** (`duration_api_ms` over `duration_ms`, 56 runs). A core-count formula does
not describe a workload that is three-quarters network wait, and four agents fitted comfortably
where it predicted two would not. Before accepting a concurrency cap derived from cores, measure
the API-wait share of one run — it is one field in `--output-format json` and it decides whether
the formula applies at all.

**Bounds, stated because a measurement widens quietly otherwise:** this licenses 4, not 8 or 16,
which were not run. It is silent on write collisions between parallel agents, which is a
correctness constraint no wall-clock number can speak to. It is one box, one model, one date.

**One instrument fault, recorded before the verdict and unresolved by it.** A concurrency-4 batch
leaves the box at loadavg ~1.84 and a concurrency-2 batch at ~0.94, while the driver only waited
for 0.50 — so only the first batch ever started cold, and no concurrency-4 batch did. Cold and
warm batches of identical work differed ~10%. Two post-hoc checks (dropping the cold batch;
counting the voided one) moved the ratio to 0.554 and 0.578, so the win survives either way, but
both are **exploratory**. A cleaner design waits to a fixed low load before *every* batch and
randomises arm order rather than alternating.

## Three ways an ad hoc dispatch script poisons a paired comparison — MEASURED 2026-09-02

Source: build `data-contract-assertions-v2` (`pipeline/builds/data-contract-assertions-v2/`,
36 arm runs for 12 valid observations), read from the run outputs, not from any gate. All
three faults were in shell written for that build and none was visible to a check.

- **A shared working directory.** MEASURED: a later run in the same directory read the
  earlier run's answer file and continued from it. Fix that generalises: one fresh directory
  per run, created `exist_ok=False`, named by a hash of label plus nonce.
- **The arm name in the path.** MEASURED: six of twelve answers wrote their own working
  directory into their text ("artefacts are in `.../with-arm/`"), so a grader handed the
  relabelled files could still read the arm off the prose. Blinding by label does not blind
  by content. Fix: the path carries no arm string, and every output is regex-scanned for the
  arm vocabulary before it reaches a grader (`arm_leak`).
- **The method mounted for every arm.** MEASURED: `--add-dir <skill>` was passed to all three
  arms, so the bare baseline cited the skill's own reference material. Fix: the mount is a
  parameter that raises for any arm but `with`.
- **The usage payload was never captured.** MEASURED: every cost row of that build had
  `tokens=None`, and the cost gate returned clean, so the cost clauses of the verdict had
  nothing to judge. `--output-format json` carries `usage` and `modelUsage`; sum the
  `*_tokens` fields and treat a zero as a run that did not report, not as a cheap run.

The generalisable lesson: the harness is part of the instrument, and a harness rewritten per
experiment cannot be trusted by the experiment that uses it. In this repo the four fixes are
`pipeline/build/dispatch.py`, with each fault reconstructed as a positive control in
`selftest_dispatch.py`. Neighbour: `testing-skills-methodology.md` (mutation-testing the
controls that guard this).
