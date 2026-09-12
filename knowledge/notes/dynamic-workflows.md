---
title: Dynamic workflows
sources:
  - url: https://code.claude.com/docs/en/workflows
    fetched: 2026-08-27
tags: [claude-code, workflows, subagents, orchestration, mechanics]
related: ["[[subagents]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]"]
raw:
  - "none of the bytes this note was written from were kept (fetched before the raw layer existed, 2026-09-02)"
  - "baseline 2026-09-04, change detection only, NOT what was read: knowledge/raw/baseline-2026-09-04/code.claude.com_docs_en_workflows.md"
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

  **What actually enforces `opts.schema` (added 2026-09-11).** Claude Code checks the schema
  **before starting the subagent** and, when it can prove the schema contradicts itself, fails the
  call with the contradiction named and never spends a token — the example given is *"a `required`
  key that `additionalProperties: false` rules out"*. If output still fails validation after
  **five attempts** the call fails with the last validation failure attached; the count is
  `MAX_STRUCTURED_OUTPUT_RETRIES`. That is the same reask loop our own `structured-llm-extraction`
  talent teaches, now with a vendor default — and the first documented way a workflow agent costs
  five model calls before erroring.
`pipeline(list, fn)` (one agent per item → results array). An `agent()` call
resolves to `null` if stopped or on unrecoverable API error, and `pipeline()`
keeps the null → `.filter(Boolean)`.

  **A third way to get `null`, and it is a permission decision rather than a failure:** *"In auto
  mode, the classifier can block an `agent()` call before the subagent starts. A blocked call
  resolves to `null`."* So `.filter(Boolean)` silently turns a **blocked** agent into an absent
  one — anything counting results (our `pipeline/` harnesses, any workflow-derived metric) can
  under-report agents without a single error.

**Open question:** this page documents only `agent()` and `pipeline()` by name.
`parallel()`, `phase()`, and explicit barrier semantics are deferred to the Agent
SDK TypeScript reference (`/docs/en/agent-sdk/typescript`) — confirm there before
relying on them.

## Runtime, limits, cost

- Isolated environment; runs in background; **resumable across sessions — this note said the
  opposite and was wrong before the diff that corrected it (re-read 2026-09-11).** Results are
  saved under the session's directory in `~/.claude/projects/`, so a session reopened with
  `claude --resume` replays completed agents when you ask Claude to relaunch the workflow; a
  *fresh* session has nothing to relaunch and starts over. In a **cloud session** the results are
  saved with the conversation history and survive the VM being reclaimed. When saved results
  cannot be found at all, the relaunch fails with **`nothing to resume`** rather than silently
  restarting — the failure is explicit, which is the string a harness should match on. The real
  boundary was never "the same session": it is *the same session id with its saved results still
  present*. The held 2026-09-04 bytes already carried the `--resume` half, so this was a
  misreading on our side, not a vendor change. Replay follows start order: cached
  results stop at the first agent that didn't finish, and every agent started
  after it reruns → **many small agents preserve more progress than one long one**.
- **Concurrency cap 16 agents; hard cap 1,000 agents/run.** *The 16 is not a flat ceiling, and
  this note was written without the qualifier.* The change-detection copy this base holds
  (`knowledge/raw/baseline-2026-09-04/code.claude.com_docs_en_workflows.md:349`, and those are
  today's bytes rather than the ones this note was written from — the page has never been
  re-read since 2026-08-27) states it as: *"Up to 16 concurrent agents, **fewer when Claude Code
  has fewer CPUs available, including inside a CPU-limited container**"*. That matters here and
  not in the abstract: this repository runs on a small container, and its own `W_MAX_AGENTS` is
  **4**. The two do not conflict — 4 was measured on this box, not derived — but the direction is
  worth naming, because `pipeline/CONSTANTS.md` records that the *previous* value of 2 came from a
  CPU formula it rejected for modelling contention over a workload that is 73% API wait. The
  vendor's own page says CPU count does bound concurrency; what it does not say is where, and the
  measurement remains the only thing licensing 4. Flagged 2026-09-08 during the KB walk-through;
  a re-read of the live page is owed. No mid-run user input
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
