# Evals — subagent-driven-development

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (triage-before-drop, observable criteria, normal+clever blend, baseline-fails
> on clever ones, discipline→pressure scenarios, negative-trigger, verify cross-refs/tool claims).

**Talent:** `subagent-driven-development` · **Type:** discipline (orchestration) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely controller behavior WITHOUT this talent
(default "just execute the plan yourself / dispatch loosely") vs WITH its method applied. A
scenario passes only if the with-talent result is materially better and meets the observable
criterion. This is a discipline talent, so the clever scenarios are PRESSURE cases: a plausible
excuse tempts the wrong behavior, and the method must hold the line.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1–S2 normal/representative (the everyday execute-a-plan job),
      S3–S6 clever/adversarial (pressure + a planted diff-range trap), S7 negative-trigger.
- [x] **Specific to this talent** — every scenario turns on SDD's own mechanics (per-task
      review gate, ledger recovery, controller-never-fixes, 5-round breaker, plan-mandated-defect
      ruling, recorded BASE, sequential dispatch), not generic subagent boilerplate.
- [x] **Observable pass/fail criterion** on every scenario — an outsider can check it.
- [x] **Baseline plausibly FAILS** on the clever scenarios (S3–S6).
- [x] **Discipline → pressure scenarios** — S3, S4, S6 tempt the wrong behavior under a real excuse.
- [x] **Negative trigger** — S7 (no task-decomposed plan yet, or tightly-coupled tasks).
- [x] **Cross-refs verified** — `using-git-worktrees`, `finishing-a-development-branch`,
      `requesting-code-review` (+ `code-reviewer.md`) all exist in-repo; `executing-plans` is an
      external superpowers sibling, now prefixed `superpowers:` to mark it as such (not a dead
      local ref). Scripts `sdd-workspace`/`task-brief`/`review-package` are pure git+awk+local FS.

## Scenarios

### S1 — Execute a 4-task plan in-session · application (normal)
- **Input:** "Here's `plan.md` with Tasks 1–4, mostly independent. Execute it; stay in this chat."
- **Pass criterion (observable):** Runs the loop — one fresh implementer subagent per task with a
  freshly-built brief (not session history), a task review (spec compliance AND code quality)
  after EACH task, completion lines appended to a ledger file, and ONE whole-branch review at the
  end before finishing. Never implements a task itself in the controller.
- **Baseline (without talent):** Controller implements the tasks directly, or dispatches workers
  with no per-task review gate and no ledger; quality varies and nothing verifies each task.
- **With talent:** Per-task dispatch→review→complete cycle with ledger + final review. **PASS.**
- **Result:** pass

### S2 — Resume after compaction · application (normal, recovery)
- **Input:** Session resumes. Ledger `progress.md` first line names this plan; it has
  `Task 1: complete (...)` and a `Task 2: fix round 2/5 (...)` line as its last entry.
- **Pass criterion (observable):** Reads the ledger, does NOT re-dispatch Task 1 (already
  complete), and resumes Task 2 at fix round 3 — trusting the ledger + `git log` over its own
  (absent) memory. Does not restart the plan from Task 1.
- **Baseline (without talent):** No ledger discipline → re-dispatches completed tasks from
  scratch (the single most expensive observed failure) or loses its place entirely.
- **With talent:** Ledger-driven recovery skips done tasks and resumes the mid-loop task. **PASS.**
- **Result:** pass

### S3 — "I'll just fix the Critical myself" · pressure (clever)
- **Input:** Task 3's review returns a Critical finding. It's late; fixing it inline in the
  controller looks faster than re-dispatching a subagent.
- **Pass criterion (observable):** Does NOT edit code in the controller. Enters the fix loop
  (rounds 1–3 resume the original implementer with the findings verbatim), and every round ends
  with a SCOPED re-review before the task can complete. Controller context stays coordination-only.
- **Baseline (without talent):** Controller patches the file itself and moves on — the fix skips
  review and pollutes the controller's context.
- **With talent:** Fix routed to a subagent + scoped re-review; controller never fixes. **PASS.**
- **Result:** pass

### S4 — Round 5 still has an open finding · pressure (clever, breaker)
- **Input:** Task 5's fix loop reached round 5 and the re-review still reports one Important
  finding open. "One more round will surely converge."
- **Pass criterion (observable):** Stops dispatching at the cap (no round 6). Adjudicates the
  finding: park-with-ruling if contestable or non-load-bearing, or rule-on-the-smallest-unblock
  and carry it forward if load-bearing — and writes a `Ruling:`/`parked` LEDGER line either way.
  No silent drop; no infinite loop.
- **Baseline (without talent):** Either loops indefinitely chasing convergence, or silently drops
  the finding to move on — both hide a decision from the human.
- **With talent:** Breaker trips, adjudicate + ledger, continue or stop only if every path is a
  guess. **PASS.**
- **Result:** pass

### S5 — Plan mandates what the rubric flags as a defect · trap (clever)
- **Input:** Task brief explicitly says "duplicate the validation block verbatim into both
  handlers." The task reviewer flags the verbatim duplication as an Important quality defect.
- **Pass criterion (observable):** Treats it as a plan-vs-rubric conflict and RULES on it with
  the spec as binding authority, recording a `Ruling:` ledger line — does NOT auto-dismiss the
  finding merely because the plan mandated it, and does NOT dispatch a fix contradicting the plan
  without a recorded ruling.
- **Baseline (without talent):** Blindly obeys the plan (finding vanishes, no record) or blindly
  obeys the reviewer (silently overrides the plan) — no adjudication trail either way.
- **With talent:** Conflict adjudicated against the spec, ruling ledgered. **PASS.**
- **Result:** pass

### S6 — Multi-commit task, computing the review diff · pressure (clever, planted trap)
- **Input:** Task 2's implementer made 4 commits. Controller needs to package the diff for the
  task reviewer; `HEAD~1` is right there and tempting.
- **Pass criterion (observable):** Uses the BASE it recorded (`git rev-parse HEAD`) BEFORE
  dispatching the implementer as the diff range floor — via `scripts/review-package PLAN BASE HEAD`
  — NOT `HEAD~1`. Reviewer sees all 4 commits, not just the last one.
- **Baseline (without talent):** Reaches for `git diff HEAD~1`, silently reviewing only the final
  commit and letting 3 commits' worth of change go unreviewed.
- **With talent:** Recorded BASE → full multi-commit diff reviewed. **PASS.**
- **Result:** pass

### S7 — No task-decomposed plan yet · negative-trigger
- **Input:** "I want to build a notifications feature — can you get started?" No written plan, no
  task breakdown; OR a plan whose tasks are tightly coupled (each needs the previous half-built).
- **Pass criterion (observable):** Does NOT start the SDD loop. Routes first to `writing-plans`
  (or brainstorming) to produce a task-decomposed plan when none exists; for tightly-coupled
  tasks, routes to manual execution / `superpowers:executing-plans` rather than fanning subagents
  at interdependent work. SDD fires only once mostly-independent tasks exist.
- **Baseline (without talent):** Might immediately spin up subagents against an undecomposed or
  coupled problem, producing conflicting half-work.
- **With talent:** Declines to loop; sends the work upstream to planning first. **PASS.**
- **Result:** pass

## Failure triage (if any scenario failed)
No scenario failed. If one had: **test-bug** = unfair/out-of-scope/subjective criterion or
baseline failing for unrelated reasons → fix the test and re-run; **skill-bug** = fails a fair
clever test → fix the skill, drop only if unfixable. Triage before any fix/drop.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
