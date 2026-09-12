# Evals — agent-harness-construction

> Baseline-vs-with test scaffold. Blend of normal + clever scenarios, all specific to
> the action-surface design method this talent teaches.

**Talent:** `agent-harness-construction` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
For each scenario, judge the likely output WITHOUT the talent vs WITH its method applied
(action-space design, granularity rules, observation contract, error-recovery contract,
context budgeting). A scenario passes only if the with-talent result is materially better
and meets the observable pass criterion. Be adversarial and honest.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps — 3 normal + 3 clever, plus 1 negative-trigger.
- [x] Specific to this talent — every scenario exercises action surface / observation /
      recovery / granularity / context-budget decisions, not generic agent advice.
- [x] Observable pass/fail criterion on every scenario.
- [x] Clever scenarios designed so the baseline plausibly FAILS.
- [x] Technique talent → APPLICATION scenarios (plus pressure on the trap ones).
- [x] Negative trigger covered (loop-diagnosis case that belongs to another talent).

## Scenarios

### S1 — Catch-all tool → typed surface · application (normal)
- **Input:** "Our agent has one `run(cmd: string)` tool that returns raw stdout. Task
  completion is low. Improve the harness."
- **Pass criterion (observable):** Recommendation replaces the catch-all with schema-first,
  narrow-input tools AND specifies a structured observation shape carrying `status`,
  `summary`, `next_actions`, and `artifacts`.
- **Baseline (without talent):** Suggests "write clearer prompts" or "parse stdout better";
  keeps the single freeform tool and prose output.
- **With talent:** Applies Action Space Design + Observation Design — typed tools, deterministic
  output shape, the four required response fields.
- **Result:** pass

### S2 — Error path has no stop condition · application (normal)
- **Input:** "A tool returns just an error string on failure and the agent retries forever.
  What should the error output contain?"
- **Pass criterion (observable):** Answer names all three Error Recovery Contract elements —
  root-cause hint, safe retry instruction, AND an explicit stop condition.
- **Baseline (without talent):** "Return a clearer error message and add a retry limit" —
  omits the explicit stop condition as part of the tool's own contract.
- **With talent:** Full recovery contract per error path.
- **Result:** pass

### S3 — Architecture pattern choice · application (normal)
- **Input:** "Task is a structured, deterministic ETL flow with a known path. ReAct or
  function-calling?"
- **Pass criterion (observable):** Recommends function-calling (typed tool execution) for the
  deterministic flow, reserving ReAct for uncertain-path exploration; may note the hybrid.
- **Baseline (without talent):** Defaults to "use ReAct, it's more capable" regardless of task shape.
- **With talent:** Matches pattern to task per Architecture Pattern Guidance.
- **Result:** pass

### S4 — "Add 20 micro-tools for flexibility" · trap (clever)
- **Input:** "Let's give the agent maximum flexibility: split read/search/edit into 20
  fine-grained tools with overlapping variants. More tools = more capable, right?"
- **Pass criterion (observable):** Pushes back — flags overlapping-semantics anti-pattern,
  prescribes medium tools for common edit/read/search loops, and reserves micro-tools for
  high-risk ops only. Does NOT endorse "more tools = more capable."
- **Baseline (without talent):** Agrees flexibility is good and adds the tools.
- **With talent:** Granularity Rules + Anti-Patterns catch the over-tooling.
- **Result:** pass

### S5 — Deploy bundled into a convenience macro-tool · edge/boundary (clever)
- **Input:** "We wrapped build+test+deploy+notify into one `ship()` macro-tool so the agent
  makes one call. Fewer round-trips, cleaner. Good?"
- **Pass criterion (observable):** Splits the irreversible deploy step into its own micro-tool
  with an explicit stop/consent condition; endorses macro-tools ONLY where round-trip overhead
  dominates AND the steps are not high-risk/irreversible. Rejects bundling deploy for convenience.
- **Baseline (without talent):** Keeps the single macro-tool because it reduces round-trips.
- **With talent:** Granularity Rules ("micro-tools for high-risk operations") override the
  round-trip argument for the deploy step.
- **Result:** pass

### S6 — "Just compact every 5k tokens" · pressure (clever)
- **Input:** "We're over context budget. Plan: bloat the system prompt with all guidance and
  force-compact every 5000 tokens. Ship it."
- **Pass criterion (observable):** Rejects the arbitrary-threshold compaction and the bloated
  invariant prompt — compact at PHASE boundaries, keep system prompt minimal/invariant, move
  large guidance into on-demand skills, prefer file references over inlining.
- **Baseline (without talent):** Complies — raises/keeps the fixed token threshold and inlines guidance.
- **With talent:** Context Budgeting rules correct all four points.
- **Result:** pass

### S7 — Loop won't terminate · negative-trigger
- **Input:** "Our agent loop keeps spinning and never terminates on this one task — diagnose
  why it won't stop."
- **Pass criterion (observable):** Declines to treat this as an action-surface redesign;
  routes to `loop-design-check` (spin/goal-decidability) or `systematic-debugging`. Does not
  start proposing new tool schemas as the fix.
- **Baseline (without talent):** May over-fire and start redesigning tools regardless.
- **With talent:** Boundary in the intro sends this to the loop/diagnosis talent.
- **Result:** pass

## Failure triage (if any scenario failed)
No failures this pass. Root-cause protocol (test-bug vs skill-bug) applies to any future red.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
