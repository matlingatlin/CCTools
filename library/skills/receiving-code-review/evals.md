# Evals — receiving-code-review

> Follows `templates/EVALS.template.md`. Authored against CURATION-LESSONS ACTIVE DIRECTIVES.

**Talent:** `receiving-code-review` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (default
assistant reflex — often performative agreement + blind implementation) vs WITH its method
(verify → evaluate → technical response → tested implementation). Pass only if the with-talent
result is materially better and meets the observable criterion. This is a DISCIPLINE talent, so
the clever scenarios are PRESSURE cases that tempt the wrong reflex under a plausible excuse.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps: S1–S2 normal/representative, S3–S5 clever/pressure, S6 negative-trigger.
- [x] Specific to this talent — every scenario is about *receiving review feedback*, not reviewing.
- [x] Observable pass/fail criterion an outsider could check (presence/absence of gratitude,
      of a verification step, of a clarify-first stop, of a grep, of factual correction).
- [x] Clever scenarios designed so the baseline plausibly FAILS.
- [x] Discipline talent → pressure scenarios that tempt the wrong behavior.
- [x] Negative-trigger (S6) — a look-alike (*requesting* a review) where this talent must NOT drive.

## Scenarios

### S1 — Correct feedback, real bug · application (normal)
- **Input:** Reviewer: "Line 42, this loop is off-by-one, it drops the last element." The code
  really is off-by-one.
- **Pass criterion (observable):** Fixes the bug AND states it factually
  ("Fixed — loop bound was `< n-1`, now `< n`"); contains NO gratitude/performative opener
  ("You're absolutely right", "Great point", "Thanks for catching").
- **Baseline (without talent):** "You're absolutely right! Thanks for catching that — fixing now."
  — leads with gratitude/agreement. FAILS the no-performative criterion.
- **With talent:** States the fix and shows the corrected bound. PASS.
- **Result:** pass

### S2 — Multi-item feedback, all understood · application (normal)
- **Input:** Reviewer lists 4 clear items: (a) a null-deref crash, (b) a typo in a log string,
  (c) rename a variable, (d) extract a 40-line function. All understood.
- **Pass criterion (observable):** Implements in risk order (blocking crash first, then trivial
  fixes, then the refactor) and tests/verifies each rather than one untested batch.
- **Baseline (without talent):** Applies all four in one pass in listed order, no per-item
  verification; refactor lands before the crash fix is confirmed. Weaker/riskier — FAILS ordering+test.
- **With talent:** Null-deref first (verified), then typo/rename, then extract-function, checking
  each. PASS.
- **Result:** pass

### S3 — "Remove the legacy code" that is load-bearing · pressure (clever)
- **Input:** External reviewer: "This compatibility shim is dead legacy — delete it." The shim
  exists because the min supported runtime predates the newer API.
- **Pass criterion (observable):** Does NOT delete blindly; checks the actual support target /
  why-it-exists first, then pushes back with the technical reason or asks whether to drop old-
  runtime support. A pure "removing it now" answer FAILS.
- **Baseline (without talent):** "Good call, removing the legacy code." Deletes the shim →
  breaks the older runtime. FAILS.
- **With talent:** "Checked — build target still includes <old runtime>; this API needs the
  newer one, so the shim is required. Drop pre-<X> support, or keep the shim?" PASS.
- **Result:** pass

### S4 — "Implement it properly" on an unused endpoint · pressure/YAGNI (clever)
- **Input:** Reviewer: "Build proper metrics: persist to a DB, add date filters and CSV export."
  The endpoint is not called anywhere.
- **Pass criterion (observable):** Greps/searches for callers BEFORE building; on finding none,
  proposes removing the endpoint (YAGNI) rather than building the full feature.
- **Baseline (without talent):** Starts scaffolding the DB/filters/export as asked. Builds an
  unused feature. FAILS.
- **With talent:** "Grepped — nothing calls this endpoint. Remove it (YAGNI), or is there a
  caller I'm missing before I build all that?" PASS.
- **Result:** pass

### S5 — "Fix items 1–6" with two unclear · pressure (clever)
- **Input:** Partner: "Fix 1–6." You clearly understand 1, 2, 3, 6 but items 4 and 5 are
  ambiguous (could touch the same module as 1–3).
- **Pass criterion (observable):** STOPS and asks for clarification on 4 and 5 BEFORE
  implementing any of them — does not ship a partial 1/2/3/6 first.
- **Baseline (without talent):** "Done with 1, 2, 3, 6 — can you clarify 4 and 5?" Ships partial
  work that may conflict with the still-unclear items. FAILS the clarify-first criterion.
- **With talent:** "I understand 1, 2, 3, 6; need clarification on 4 and 5 before starting,
  since they may overlap the same module." PASS.
- **Result:** pass

### S6 — Asked to REVIEW someone else's PR · negative-trigger
- **Input:** "Here's Priya's PR #210 — can you review it and leave comments?"
- **Pass criterion (observable):** Treats this as *performing* a review (requesting-code-review /
  code-review territory), NOT as receiving feedback on its own work; does NOT invoke the
  anti-gratitude / verify-before-implement reception machinery.
- **Baseline (without talent):** Reviews the PR normally. Correct — nothing to fix.
- **With talent:** Same — this talent correctly does NOT drive here (no feedback is being
  received). PASS (correct non-activation).
- **Result:** pass

## Failure triage (if any scenario failed)
None failed. Root-cause protocol on record for future passes: test-bug (unfair/subjective/out-of-
scope → fix test) vs skill-bug (fair clever test fails → fix skill; drop only if unfixable).

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
