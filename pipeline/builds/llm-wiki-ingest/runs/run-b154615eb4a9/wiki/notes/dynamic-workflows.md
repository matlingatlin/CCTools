---
title: Dynamic workflows
sources:
  - url: https://code.claude.com/docs/en/workflows
    fetched: 2026-08-27
status: verified
tags: [claude-code, workflows, subagents, orchestration, mechanics]
related: ["[[subagents]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]"]
---

# Dynamic workflows

A dynamic workflow is a **JavaScript script that orchestrates subagents at scale**,
written by Claude for the task you describe and run by a runtime **in the
background**. The distinguishing property vs subagents/skills: the **script holds
the plan** (loop, branching, intermediate results in variables), so Claude's
context receives only the final answer. Requires v2.1.154+.

## When to use vs alternatives

| | Who decides next | Intermediate results | Scale |
| --- | --- | --- | --- |
| Subagent | Claude, turn by turn | Claude's context | a few per turn |
| Skill | Claude, per prompt | context | a few |
| Agent team | lead agent | shared task list | a handful of peers |
| **Workflow** | the script | script variables | **dozens–hundreds/run** |

Reach for one when a task needs more agents than one conversation can coordinate,
or when you want the orchestration codified and rerunnable. Adds a quality
pattern, not just scale: independent agents can adversarially review each other's
findings, or draft a plan from several angles before committing.

## Triggering

- **Ask in the prompt** (natural language, or the keyword `ultracode`) — human
  input only (interactive/IDE/Remote Control/SDK stamped human); does NOT fire
  from `-p`, scheduled tasks, webhooks, or PR comments (as of v2.1.210).
- **`/effort ultracode`** = xhigh effort + automatic workflow orchestration for
  every task in the session (more tokens, slower).
- One built-in: `/deep-research <question>` (needs WebSearch) — fans out, cross-
  checks, votes on claims, returns a cited report; runs only when invoked.

## Script model

Plain JS with top-level `await`, preceded by a `meta` block (`name`,
`description`). Documented primitives on this page: `agent(prompt, opts)` (one
subagent; `opts.schema` = JSON Schema for structured output, `opts.label`) and
`pipeline(list, fn)` (one agent per item → results array). An `agent()` call
resolves to `null` if stopped or on unrecoverable API error, and `pipeline()`
keeps the null → `.filter(Boolean)`.

**Open question:** this page documents only `agent()` and `pipeline()` by name.
`parallel()`, `phase()`, and explicit barrier semantics are deferred to the Agent
SDK TypeScript reference (`/docs/en/agent-sdk/typescript`) — confirm there before
relying on them.

## Runtime, limits, cost

- Isolated environment; runs in background; resumable **within the same session
  only** (exit → next session starts fresh). Replay follows start order: cached
  results stop at the first agent that didn't finish, and every agent started
  after it reruns → **many small agents preserve more progress than one long one**.
- **Concurrency cap 16 agents; hard cap 1,000 agents/run.** No mid-run user input
  (split sign-off into per-stage workflows); no `import()` (fails before start);
  no direct FS/shell from the script (only agents act).
- Spawned agents always run in **`acceptEdits`** mode with file edits auto-
  approved, regardless of session mode; only the launch prompt honors your
  permission mode. Shell/web/non-allowlisted MCP can still prompt mid-run.
- Cost: a run can use far more tokens than doing the task inline. Gauge on a small
  slice first; `/workflows` shows live per-agent tokens. `Large workflow` warning
  at >25 agents or >1.5M projected tokens (advisory only). Size guideline
  (`workflowSizeGuideline`): small <5, medium <15 (default, v2.1.219+), large <50,
  unrestricted — advice, not a cap.

## Relation to this project

Workflows are the scale tier above the manual subagent fan-out we already use for
`deep-reading` ingestion and evals. For the factory's batch operations (auditing
many candidate skills, large research sweeps) a workflow is the right tool; for a
handful of readers, plain subagents suffice.
