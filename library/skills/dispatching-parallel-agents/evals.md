# Evals — dispatching-parallel-agents

> Baseline-vs-with test suite. Authored against `templates/EVALS.template.md` and the
> ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `dispatching-parallel-agents` · **Type:** technique (with discipline pressure) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
For each scenario, judge the likely output WITHOUT the talent (an orchestrator's default
instinct) vs WITH its method applied. The talent passes a scenario only if the with-talent
result is materially better and meets the observable pass criterion.

## EVOLVING CHECKLIST (from CURATION-LESSONS)
- [x] Mix, not only traps — 3 normal/representative, 3 clever/adversarial, 1 negative-trigger.
- [x] Specific to this talent — every scenario is about the fan-out decision + agent briefing.
- [x] Observable pass/fail criterion per scenario.
- [x] Clever scenarios designed so the baseline plausibly FAILS.
- [x] Matches talent type — application scenarios + pressure scenarios (tempt the wrong fan-out).
- [x] Covers the negative trigger (a cohesive single-domain task; and the factory boundary).

## Scenarios

### S1 — Three unrelated test-file failures · application
- **Input:** "After a refactor, `auth.test.ts` (5 fails), `billing.test.ts` (2 fails), and
  `render.test.ts` (3 fails) are red. Roots look unrelated — auth is a token bug, billing a
  rounding bug, render a layout regression. Fix them."
- **Pass criterion (observable):** Plan dispatches exactly one subagent per file/domain (3),
  each with its own scope + goal + constraint + expected-output, and issues all three in a
  SINGLE response.
- **Baseline (without talent):** Investigates the three sequentially in one long session, or
  fires one "fix all failing tests" agent — slower, and context bleeds between domains.
- **With talent:** One focused agent per domain, dispatched together → concurrent, isolated.
- **Result:** pass

### S2 — Crafting one agent's brief · application
- **Input:** "Write the prompt for the subagent that fixes `auth.test.ts`." (tendency: "Fix
  the auth tests.")
- **Pass criterion (observable):** Prompt contains all four: specific scope (the file), a
  clear goal, an explicit constraint (e.g. don't touch other code / tests-only), and a named
  return format (summary of root cause + changes). Includes the concrete failing test names /
  error text rather than a vague reference.
- **Baseline (without talent):** "Fix the failing auth tests." — no scope guard, no output
  contract; agent may refactor widely or return an opaque result.
- **With talent:** Focused, self-contained, output-specified brief.
- **Result:** pass

### S3 — Review-and-integrate after return · application
- **Input:** "The three agents returned their summaries. What now?"
- **Pass criterion (observable):** Answer includes checking each summary, checking for edits
  to the SAME files/conflicts, AND running the full suite before declaring done.
- **Baseline (without talent):** Accepts the three "done" reports and moves on without a
  conflict check or full-suite run.
- **With talent:** Verification step (conflicts + full suite + spot-check) is explicit.
- **Result:** pass

### S4 — Falsely-independent failures · trap (clever)
- **Input:** "`parseDate.test.ts`, `invoice.test.ts`, and `report.test.ts` are all failing.
  Fan out one agent each." (Hidden truth: all three consume a shared `formatDate()` util that
  changed; one fix turns all green.)
- **Pass criterion (observable):** Does NOT immediately dispatch three parallel agents;
  recognizes the failures may share a root cause and investigates together / with one agent
  first — because "fixing one might fix the others."
- **Baseline (without talent):** Complies and dispatches three agents; they each independently
  rediscover and possibly triple-patch the same util, risking conflicting edits.
- **With talent:** "Don't use when failures are related" gate fires → consolidate first.
- **Result:** pass

### S5 — Shared-state / same-file collision · pressure (clever)
- **Input:** "Two independent features to add: rename a symbol across `api.ts`, and add a
  field to a type in the same `api.ts`. Dispatch both in parallel to go fast."
- **Pass criterion (observable):** Declines to run the two concurrently against the same file;
  either sequences them or hands one agent the whole file — cites shared-state/interference.
- **Baseline (without talent):** Dispatches both in one response; the two agents edit `api.ts`
  concurrently and clobber each other's changes.
- **With talent:** Shared-state exclusion recognized → sequential / single agent.
- **Result:** pass

### S6 — "Parallel" split across responses · edge (clever)
- **Input:** "I dispatched agent 1, waited for it, then dispatched agent 2, then agent 3 — but
  it felt as slow as doing it myself. Why?"
- **Pass criterion (observable):** Identifies that dispatches in separate responses run
  SEQUENTIALLY; parallelism requires issuing all dispatch calls within a single response.
- **Baseline (without talent):** Blames the agents or model speed; misses that the pattern was
  never actually parallel.
- **With talent:** "Multiple dispatch calls in one response = parallel" is stated precisely.
- **Result:** pass

### S7 — Single cohesive task · negative-trigger
- **Input:** "Redesign the checkout flow end-to-end — the cart, the payment step, and the
  confirmation screen all need to change together and share the new order model."
- **Pass criterion (observable):** Does NOT fan out per-screen; keeps it as one coordinated
  effort (shared model + need for full-system understanding) — or, if split at all, notes the
  shared state makes independent parallel agents unsafe. Recognizes this is NOT a
  dispatching-parallel-agents case, and that N-homogeneous mechanical fan-out belongs to
  `factory`, not here.
- **Baseline (without talent):** Might reflexively split into three parallel agents that
  produce three incompatible partial redesigns.
- **With talent:** Declines to fan out; the talent stays silent / defers.
- **Result:** pass

## Failure triage
No scenario failed. failure_cause: none.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
- Note for CURATION-LESSONS: the strongest discriminators for fan-out talents are the
  *falsely-independent* (S4) and *shared-state* (S5) traps — baselines over-parallelize under
  a "go fast" excuse. Worth a directive: fan-out talents should always be tested with a
  "looks independent but isn't" trap.
