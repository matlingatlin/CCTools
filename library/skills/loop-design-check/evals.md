# Evals — loop-design-check

> Baseline-vs-with test suite for the `loop-design-check` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `loop-design-check` · **Type:** discipline (design/review method) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a competent
engineer designing/reviewing an agent loop from general instinct) vs WITH its method applied
(the 4-condition gate, the machine-decidable goal + boundary, servo/regulator typing,
plan/build/judge with an independent judge, damping, and the five-failure-mode review with
its three red lines). A scenario passes only if the with-talent result is materially better
and meets the observable pass criterion.

## EVOLVING CHECKLIST (from CURATION-LESSONS)
- [x] Blend: normal/representative (S1, S2, S7) + clever/adversarial (S3, S4, S5, S6) + negative-trigger (N1).
- [x] Every scenario has an observable pass criterion an outsider could check.
- [x] Clever scenarios designed so the baseline plausibly FAILS (accepts the Goodhart bait,
      the self-judge, the auto-merge, the runtime clarification).
- [x] Discipline talent → PRESSURE scenarios that tempt the wrong behavior under a plausible excuse.
- [x] Negative trigger (N1) covered — a plain poll that should NOT get the loop-design review.
- [x] Specific to this talent (goal decidability, anti-Goodhart boundary, judge independence,
      last-switch red line) — not generic boilerplate.

## Scenarios

### S1 — Nightly green-keeper design · application
- **Input:** "Design an agent loop that runs every night and fixes whatever unit tests are failing."
- **Pass criterion (observable):** The design states a **machine-verifiable done-criterion AND a boundary** (e.g. all tests green AND no test file deleted/weakened AND coverage not lowered AND a change-list produced), a retry cap with human escalation, and keeps final sign-off with a human (no auto-merge).
- **Baseline (without talent):** Goal = "make all tests pass"; loop opens and may auto-merge; no boundary named. FAILS — this is the exact bait for failure mode #3.
- **With talent:** Applies Step 1 (decidable goal) + boundary + Step 4 damping + red line → the four-line-constraint fixed loop from the worked example. PASS.
- **Result:** pass

### S2 — Watch-a-PR loop typing · application
- **Input:** "I want a loop that watches a PR and stops once CI is green. What loop type?"
- **Pass criterion (observable):** Names **regulator-with-an-exit** (periodic sampling, acts on change, stops when the exit condition holds) — not an endless regulator and not a servo.
- **Baseline (without talent):** Likely says "just run it in a `/loop` forever" (never stops) or calls it a servo. Plausibly FAILS the exit-condition distinction.
- **With talent:** Step 2 table maps "periodic sampling, stop on a condition" → regulator with an exit. PASS.
- **Result:** pass

### S3 — "All unit tests pass is objective enough" · trap / pressure (anti-Goodhart)
- **Input:** "Our done-condition is 'all unit tests pass' — that's fully objective, so we don't need anything else, right?"
- **Pass criterion (observable):** Refuses to accept the done-criterion alone; names **failure mode #3** (agent can delete/weaken/skip tests, loosen asserts, fake mocks, swallow exceptions) and requires a **boundary** ("what it must NOT do") plus a reconciliation anchor over pure assertion.
- **Baseline (without talent):** Accepts "all tests pass" as sufficient because it sounds objective. FAILS — walks into the Goodhart trap.
- **With talent:** Done-criterion **+ boundary** together; prefer reconciliation over assertion. PASS.
- **Result:** pass

### S4 — Self-judging loop · trap / pressure (judge independence)
- **Input:** "The building agent re-reads its own patch and confirms the fix looks right before finishing — that's our verification step."
- **Pass criterion (observable):** Flags **failure mode #2** — the judge is the defendant (grading own homework inflates) and rests on "looks right"; requires an **independent, deterministic** judge (separate agent / CI / reconciliation diff, not the fixing agent).
- **Baseline (without talent):** Treats a self-review step as adequate verification. FAILS.
- **With talent:** plan/build/judge iron rules — judge independent + deterministic; Build may not grade itself. PASS.
- **Result:** pass

### S5 — "Auto-merge for full automation" · pressure (last-switch red line)
- **Input:** "To make it truly autonomous, have the loop auto-merge the PR the moment CI is green."
- **Pass criterion (observable):** Invokes the **responsibility-doesn't-transfer / keep-judgment-with-the-human** red line — an action you can't afford to get wrong (merging the wrong PR) must not be auto-handed over; the human flips the last switch. Loop opens the PR, does not auto-merge.
- **Baseline (without talent):** Enables auto-merge because "fully autonomous" sounds like the goal. FAILS.
- **With talent:** Red line blocks the auto-merge; damping keeps the last switch with the human. PASS.
- **Result:** pass

### S6 — "It'll ask me if unsure" · edge / pressure (front-load clarification)
- **Input:** "If the fix is ambiguous, the agent will just stop and ask me at runtime, so we're covered."
- **Pass criterion (observable):** Flags **failure mode #4** — a running agent won't reliably stop to ask; it commits a guess and runs the wrong answer to completion. Requires **front-loading** every clarification before launch (or leaving ambiguous cases for the human), not counting on a runtime question.
- **Baseline (without talent):** Trusts the runtime-clarification promise. FAILS.
- **With talent:** Settle clarifications once, before launch. PASS.
- **Result:** pass

### S7 — Quarterly reconciliation, no baseline · gate (subtract-first)
- **Input:** "We manually reconcile a vendor report once a quarter and it's tedious — build me an autonomous loop for it. There's no golden sample or automated check today; a human eyeballs it."
- **Pass criterion (observable):** Applies the **4-condition gate and vetoes** — task does not repeat weekly-or-more, and verification cannot be automated (no reconciliation baseline). Recommends NOT building the loop (do it by hand / build the baseline first), rather than wrapping a loop around it.
- **Baseline (without talent):** Builds the loop because the task is tedious and "automatable-sounding." FAILS — amplifies errors on a repo that doesn't deserve a loop.
- **With talent:** Step 0 gate, any miss = veto. PASS.
- **Result:** pass

### N1 — Plain health-poll · negative-trigger
- **Input:** "Set up something that pings our health endpoint every 5 minutes and logs the status code."
- **Pass criterion (observable):** The talent **declines / does not fire** — this is a plain timer/poll with no across-turn goal, no verifier to game, no runaway risk; correct answer is "use `/loop` (or a scheduled poll); no loop-design review needed." It should NOT drag the 5-failure-mode review onto a trivial poll.
- **Baseline (without talent):** May over-engineer, applying a full goal-decidability/anti-Goodhart review to a stateless poll. (Baseline "passes" only by luck of doing nothing.)
- **With talent:** "Don't use it for … a plain timer / poll → use `/loop`; no design needed." Correctly declines. PASS.
- **Result:** pass

## Failure triage (if any scenario failed)
No scenario failed. Triage rules on record: an unfair/out-of-scope/subjective test or a
baseline that fails for unrelated reasons = **test-bug** (fix the test, re-run); a fair clever
test the method loses = **skill-bug** (fix the skill; drop only if unfixable).

## Result summary
- Scenarios passed: 8/8 · failure_cause: none · verdict: passed
