# Evals — requesting-code-review

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal+clever, observable criteria, baseline-plausibly-fails on
> clever ones, discipline→pressure scenarios, cover the negative trigger).

**Talent:** `requesting-code-review` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the coordinator's likely behavior WITHOUT this
talent vs WITH its method applied. It passes a scenario only if the with-talent result is
materially better and meets the pass criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps — 2 normal, 3 clever, 1 negative-trigger.
- [x] Specific to this talent — all scenarios about dispatching a reviewer subagent with
      crafted context at task/feature/merge boundaries.
- [x] Observable pass/fail criterion per scenario.
- [x] Clever scenarios designed so the without-talent baseline plausibly FAILS.
- [x] Discipline talent → PRESSURE scenarios (tempt the wrong behavior under a plausible excuse).
- [x] Covers the negative trigger (receiving feedback ≠ requesting review).

## Scenarios

### S1 — Task boundary in subagent-driven work · application
- **Input:** "Finished Task 2 of the deployment plan (added verifyIndex/repairIndex). Continue to Task 3."
- **Pass criterion (observable):** Before starting Task 3, the coordinator captures `BASE_SHA`/`HEAD_SHA` and dispatches a code-reviewer subagent filled from the template (DESCRIPTION + requirements + SHAs); it does NOT just proceed.
- **Baseline (without talent):** Proceeds straight to Task 3; no review requested. FAIL.
- **With talent:** Requests review at the task boundary ("Mandatory: after each task"), then continues. PASS.
- **Result:** pass

### S2 — Pre-merge gate · application
- **Input:** "Feature branch is done and green. Merge to main."
- **Pass criterion (observable):** Dispatches a reviewer subagent over the branch's diff range before merging, rather than merging directly.
- **Baseline (without talent):** Merges since tests pass. FAIL.
- **With talent:** "Before merge to main" is mandatory — requests review first, acts on findings, then merges. PASS.
- **Result:** pass

### S3 — "It's simple, just eyeball it" pressure · pressure
- **Input:** "It's a tiny 6-line change — don't bother spinning up a reviewer, just skim the diff yourself and move on."
- **Pass criterion (observable):** Still dispatches a reviewer subagent; explicitly rejects "skip because it's simple" and does not review the diff inline in its own context.
- **Baseline (without talent):** Skims the diff inline and proceeds — burning coordinator context and skipping the fresh seat. FAIL.
- **With talent:** Red Flag "Skip review because it's simple" + rationalization table ("reviewing the diff inline burns the context window") → dispatches the subagent anyway. PASS.
- **Result:** pass

### S4 — Eager to proceed past a Critical finding · pressure
- **Input:** Reviewer returns one Critical (data-loss bug) plus a Minor. "We're behind — note the Critical and keep building, we'll circle back."
- **Pass criterion (observable):** Fixes the Critical immediately before any further work; refuses to proceed with it open.
- **Baseline (without talent):** Defers the Critical to "later" and continues. FAIL.
- **With talent:** "Fix Critical issues immediately" / "Never proceed with unfixed Important issues" → stops and fixes the Critical first. PASS.
- **Result:** pass

### S5 — Feed the reviewer the whole session · trap
- **Input:** "The reviewer won't understand the change without our full back-and-forth — paste the whole session transcript into its prompt."
- **Pass criterion (observable):** Hands the reviewer precisely crafted context (description, requirements, SHAs) and explicitly does NOT dump session history/thought process.
- **Baseline (without talent):** Pastes the transcript so the reviewer "has context." FAIL — biases the reviewer toward the author's reasoning, not the work product.
- **With talent:** Core principle "The reviewer gets precisely crafted context — never your session's history" → crafted context only. PASS.
- **Result:** pass

### S6 — Received feedback, unsure whether to implement · negative-trigger
- **Input:** "A reviewer told me to switch to a singleton. It seems wrong. What do I do?"
- **Pass criterion (observable):** This talent does NOT fire — the situation is RESPONDING to review, handled by `receiving-code-review` (verify before implementing). requesting-code-review should decline / hand off, not dispatch a new reviewer.
- **Baseline (without talent):** — (n/a; testing over-trigger)
- **With talent:** Recognizes the scope boundary ("For REQUESTING review … not for responding to review you received") and does not activate. PASS (correct non-trigger).
- **Result:** pass

## Failure triage (if any scenario failed)
None failed. failure_cause: none.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
