---
name: factory
description: "Use for any task that splits into many independent work items you want done in parallel instead of one at a time — reviewing N files, harvesting N sources, researching N questions, authoring N drafts, checking N items. Measures the real concurrency width, sizes the agent fleet to the work (one agent per item), and fans them out through a produce(→verify) pipeline, returning the results to the caller. Pure parallel-execution muscle: it does NOT decide domain steps, build anything, or commit — the caller/loop does that around it. Pairs with cost-aware-model-routing, agent-blast-radius-guard, dispatching-parallel-agents."
disable-model-invocation: true
---

# factory — run many work items in parallel, return the results

A reusable parallel-execution engine for **any** project. Give it a list of independent work
items and a per-item task; it sizes the fleet to the work, fans the items out concurrently,
optionally verifies each, and **returns the results**. That is all it does.

**Out of scope — on purpose.** factory does NOT choose what the work is, does NOT build or
author domain artifacts as a special stage, and does NOT commit. Those are **separate parts
of the loop that calls it** (e.g. `/piano`): the caller decides the items and the per-item
prompt, and the caller does any building, deploying, and committing as its own steps, before
and after factory runs. factory is the muscle, not the loop.

> **Invocation:** this talent carries `disable-model-invocation: true` on purpose — it is an
> orchestrator, not something a task should auto-trigger into. A caller does not "load" it;
> a caller RUNS the workflow script that makes this method executable, or follows the method
> by hand. Wording elsewhere that says "hand it to X" means running X's script.

## When to use
- The task is a **batch of independent items** and doing them serially wastes wall-clock.
- You want throughput with control: measured width, a verify stage, results handed back.

**When NOT to use:** a single indivisible task, or items that depend on each other in sequence.

## Procedure

### 1. Take the work items from the caller
The caller supplies the list of independent items and the per-item task (review this file,
harvest this source, author this draft, check this claim). If the items must be discovered
first, that discovery is the caller's step (or a cheap producer agent) — factory just fans
out over whatever list it's given.

### 2. Measure the concurrency ceiling, then plan to it
Detect it, don't guess — it is environment-specific:
```bash
nproc 2>/dev/null || sysctl -n hw.ncpu   # CPU cores (GNU/Linux || macOS/BSD)
# nproc is coreutils-only: absent on macOS and on minimal containers. Use the fallback,
# and if BOTH are unavailable, say the width is unmeasured rather than guessing a number.

**Concurrent width `W = min(16, cores-2)`** (4 cores → 2; 8 → 6; 18+ → 16). State `W`. If it's
too narrow, the only lever is more CPU cores (an environment setting) — say so honestly.

> **`W` is GLOBAL, not per-run — shared by every concurrent fan-out on the machine.** Starting a
> second run to double throughput does NOT work: measured 2026-08-27, two factory loops shared the
> same `W=2` and gained nothing (`STATUS.md`, waves 9+10). The only lever for more width is more
> cores. Split work across runs for *organisation*, never for speed.

### 3. Size the fleet ("as many as go and are needed")
- **One agent per work item** — pass ALL of them. `W` run concurrently; the rest queue and
  drain automatically as slots free. Don't cap the list to `W`; the runtime windows it.
- **Budget:** apply `cost-aware-model-routing` — a spend ceiling and a model tier per stage
  (cheap tier for mechanical items; top tier for hard produce/verify). Stop as the ceiling nears.

### 4. Fan out via the `Workflow` tool — parallel AND sequential at once
Model the stages as a **`pipeline`** (per-item, NO barrier): it runs **parallel across items
and sequential within an item at the same time**. With width `W`, up to `W` items are in
flight at *different* stages — item A is being **verified** while item B is still being
**produced** and item C waits. Overlap is automatic, throughput = `W`-wide, order preserved
per item.
- **produce** — one agent per item does the work and RETURNS structured data (and/or writes
  to its own distinct path → no collision).
- **verify** (recommended) — one agent per produced item checks it (correctness, safety,
  quality) and returns a verdict.
Use `parallel` (a barrier) only when a stage needs ALL prior results together (e.g. dedup
before an expensive step). Pass the items as `args` to a driver script (in this repo: `pipeline/workflows/factory-wave.workflow.js` for build/harvest waves, `curate-wave.workflow.js` for curation).

### 5. Return the results to the caller
Hand back the structured results (produced data + verify verdicts). **factory stops here.**
Whatever happens next — building talents from what was found, wiring, deploying, committing —
is the **caller's** separate loop step, done by the single coordinator. factory writes no git.

## When a work item fails mid fan-out
A fan-out is not all-or-nothing. Default: a failed item **does not abort the run** — the other
items complete, and the failure is RETURNED marked-failed with its error, so the caller decides
(retry, skip, or stop). Re-dispatch only a failure with a plausible transient cause (timeout,
rate-limit), at most once, and never re-dispatch one that failed deterministically — that just
burns the width twice. Never silently drop a failed item from the results: a short result list
that looks complete is worse than an explicit failure.

## Rules
- **Muscle, not loop:** factory fans out and returns results. It never decides domain steps,
  builds/authors as a special stage, or commits — those are separate parts of the caller's loop.
- **Fleet = work, bounded:** one agent per item, capped by measured `W` + a `cost-aware-model-routing` budget.
- **Verify before returning** when correctness/safety matters — a per-item check stage.
- **Domain-agnostic:** factory knows nothing about any project; the caller supplies items and prompts.
  (In this repo, `/piano` is the caller — it composes scout/harvest/build/commit as its own
  steps and uses factory only for the parallel fan-out within a stage.)
