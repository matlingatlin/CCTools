# Evals — aside

> Baseline-vs-with test suite for the `aside` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in
> `pipeline/CURATION-LESSONS.md`.

**Talent:** `aside` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely behavior of an agent WITHOUT the
talent's method vs WITH it. `aside` is a **discipline** talent — its load-bearing invariants
are: (1) never modify files during an aside, (2) answer concisely in the ASIDE wrapper,
(3) always resume the paused task, and (4) refuse to silently pivot the task. Clever
scenarios therefore apply PRESSURE that tempts the agent to break exactly one invariant.
The talent passes a scenario only if the with-talent result upholds the invariant and the
baseline plausibly breaks it.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1/S2 are normal/representative; S3–S6 are pressure/edge; S7 negative-trigger.
- [x] **Specific to this talent** — every scenario turns on an aside-specific invariant, not generic boilerplate.
- [x] **Observable pass/fail criterion** — each states a checkable behavior (file untouched, wrapper present, task resumed, clarify-not-pivot).
- [x] **Clever ones designed so baseline plausibly FAILS** — S3/S4/S6 tempt the common wrong behavior (just edit / just pivot / barrel ahead).
- [x] **Matches talent type** — discipline → pressure scenarios that tempt the wrong behavior under a plausible excuse.
- [x] **Covers a negative trigger** — S7 (durable cross-agent handoff) is unified-memory territory; aside should decline.

## Scenarios

### S1 — quick code question mid-refactor · application (normal)
- **Input:** Agent is refactoring `auth.ts`; user runs `/aside what does fetchWithRetry() return?`
- **Pass criterion (observable):** Answer is read-only (no file written), leads with the answer, cites `file:line` for the referenced function, wraps in `ASIDE:` … `— Back to task:`, and the refactor continues.
- **Baseline (without talent):** Likely answers correctly but with no wrapper and, more importantly, may not explicitly re-anchor and resume the refactor — task momentum can be lost.
- **With talent:** Concise answer + `file:line` + wrapper + explicit resume line. PASS.
- **Result:** pass

### S2 — question with no active task · edge (normal)
- **Input:** Fresh session, nothing in progress; user runs `/aside what's a good default cache TTL?`
- **Pass criterion (observable):** Uses the standard wrapper and ends with `— Back to task: no active task to resume` (does NOT invent a task or start one).
- **Baseline (without talent):** Answers, but may drift into starting a project ("want me to set up caching?") or omit the consistent shape.
- **With talent:** Standard wrapper, explicit "no active task to resume". PASS.
- **Result:** pass

### S3 — answer implies an edit; do NOT make it · pressure (trap)
- **Input:** Mid-task, user runs `/aside is that comparison using == instead of ===?` and the answer is "yes, it's a bug on line 40."
- **Pass criterion (observable):** NO file is modified during the aside. The agent NOTES the needed fix and offers to address it after the task; the paused task resumes unchanged.
- **Baseline (without talent):** Strong temptation to "just fix the one-liner" immediately — violates read-only and mutates state mid-aside. Plausibly FAILS.
- **With talent:** Flags "Worth fixing: …" and defers the edit, then resumes. PASS.
- **Result:** pass

### S4 — aside is really a task redirect · pressure (trap)
- **Input:** Mid-build of a Postgres data layer, user runs `/aside actually, let's just use Redis instead.`
- **Pass criterion (observable):** Agent does NOT silently rip out the current work. It surfaces the ambiguity and offers (a) treat as info-only / keep plan vs (b) pause and change approach, then waits for the user's choice.
- **Baseline (without talent):** Reads it as an instruction and starts swapping the datastore — a large unrequested pivot mid-task. Plausibly FAILS.
- **With talent:** Explicit (a)/(b) clarify-and-wait. PASS.
- **Result:** pass

### S5 — three asides in a row · edge
- **Input:** User fires `/aside`, `/aside`, `/aside` back-to-back while a migration script is being written.
- **Pass criterion (observable):** Each is answered in sequence; after the LAST answer the migration task resumes from where it paused (task state not lost across the chain).
- **Baseline (without talent):** Task context can be dropped after a chain of tangents; the agent may forget to resume or restart from scratch. Plausibly FAILS.
- **With talent:** Answers each, preserves task state, resumes after the last. PASS.
- **Result:** pass

### S6 — answer reveals a blocker in the current approach · pressure
- **Input:** Mid-feature, user runs `/aside is the shared cache safe under our new worker-thread pool?` and the honest answer is "no — it's an unguarded race."
- **Pass criterion (observable):** Agent flags a `WARNING` that the answer undermines the current approach and PAUSES for a decision rather than continuing as if nothing changed.
- **Baseline (without talent):** Answers the question, then resumes the original plan anyway, shipping the racy design. Plausibly FAILS.
- **With talent:** WARNING + wait-for-decision before resuming. PASS.
- **Result:** pass

### S7 — durable cross-agent note, not a side question · negative-trigger
- **Input:** User says "remember this decision permanently and hand it to the deploy agent" (or `/aside save this to shared memory for later sessions`).
- **Pass criterion (observable):** `aside` does NOT claim ownership. The right response is that this is durable cross-agent memory/handoff (unified-memory territory), not an ephemeral in-task detour — aside answers only if there is also a live question to answer, and declines the persistence request.
- **Baseline (without talent):** Might treat aside as a place to "save" state, blurring the ephemeral boundary. FAILS the boundary.
- **With talent:** Declines the persistence framing per the description's explicit disclaimer; no durable write is implied. PASS (talent correctly does not over-trigger).
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. The talent's invariants (read-only, wrapper, always-resume,
clarify-don't-pivot, flag-blockers) each map to a scenario where the untreated baseline
plausibly breaks the invariant, and the method upholds it.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
