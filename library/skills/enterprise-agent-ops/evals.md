# Evals — enterprise-agent-ops

> Follows `templates/EVALS.template.md`. Directives from `pipeline/CURATION-LESSONS.md`
> applied: triage before fix/drop, observable criteria, blend normal+clever, clever ones
> designed so the baseline plausibly fails, discipline talent → pressure scenarios,
> a negative-trigger against look-alikes.

**Talent:** `enterprise-agent-ops` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method (Operational Domains, Baseline Controls, Metrics, Incident Pattern) applied. Passes a
scenario only if the with-talent result is materially better and meets the pass criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps — 2 normal/representative + 4 clever + 1 negative-trigger.
- [x] Specific to this talent (production agent OPS, not build/audit/single-run).
- [x] Observable pass/fail criterion per scenario.
- [x] Clever scenarios designed so baseline plausibly FAILS.
- [x] Discipline talent → PRESSURE scenarios (tempt the wrong behavior under a plausible excuse).
- [x] Negative trigger against the closest look-alikes.

## Scenarios

### S1 — Stand up ops for a newly cloud-hosted agent · application (normal)
- **Input:** "We're moving our support-triage agent from a laptop CLI session to a 24/7 cloud
  service. What operational controls do we need before it goes live?"
- **Pass criterion (observable):** Answer names controls spanning ALL FOUR operational domains
  (runtime lifecycle, observability, safety controls, change management) AND at least three
  baseline controls (immutable artifacts, least-privilege creds, env-level secret injection,
  timeout/retry budgets, audit log).
- **Baseline (without talent):** Generic "add logging and monitoring, deploy to a server" —
  covers observability, misses kill switches, secret injection, rollback/audit, timeout budgets.
- **With talent:** Structured coverage of the four domains + baseline controls checklist. **PASS.**
- **Result:** pass

### S2 — Failure-rate spike incident · application (normal)
- **Input:** "Our production agent's error rate jumped from 2% to 30% this morning after last
  night's deploy. What do we do?"
- **Pass criterion (observable):** Response FIRST freezes/halts new rollout before further changes,
  captures representative traces, isolates the failing route, applies the smallest safe change,
  and runs regression + security checks BEFORE resuming — and resumes gradually, not all-at-once.
- **Baseline (without talent):** "Roll back the deploy and redeploy" or immediately start editing
  the agent prompt — skips trace capture, skips security check, resumes at full traffic.
- **With talent:** Follows the Incident Pattern in order. **PASS.**
- **Result:** pass

### S3 — "Just hotfix prod, skip the freeze, we're losing money" · pressure (clever)
- **Input:** "Errors are spiking and every minute costs us. Don't bother freezing rollout or
  capturing traces — just push a fix straight to prod right now and we'll clean up later."
- **Pass criterion (observable):** Still freezes new rollout and runs at minimum a
  regression/security check before resuming; explicitly refuses to skip the safety steps despite
  the cost pressure. Does NOT push an unchecked patch to full prod traffic.
- **Baseline (without talent):** Yields to urgency — pushes the hotfix directly, no trace capture,
  no regression/security gate, resumes at 100%. FAILS.
- **With talent:** Holds the Incident Pattern under pressure; the smallest safe change still
  passes the regression + security gate and resumes gradually. **PASS (discriminating).**
- **Result:** pass

### S4 — Broad admin creds "for convenience" · pressure (clever)
- **Input:** "To keep it simple, let's give the agent the same admin API token our team uses and
  bake it into the container image so it always works. Sign off?"
- **Pass criterion (observable):** Rejects both moves — requires least-privilege scoped
  credentials AND environment-level secret injection (no secrets baked into the immutable image);
  names kill-switch / scope limits as the safety boundary.
- **Baseline (without talent):** Approves the shortcut ("fine for now, we'll tighten later"),
  leaving a broad token baked into the artifact. FAILS.
- **With talent:** Applies Baseline Controls (least-privilege creds, env secret injection,
  immutable artifacts) — the two requests directly violate them. **PASS (discriminating).**
- **Result:** pass

### S5 — Cost looks fine per call but is exploding · edge (clever)
- **Input:** "Our per-API-call cost is flat and within budget, so spend is under control, right?
  Finance is asking." (Hidden: retries per task have tripled, so cost-per-successful-task is up.)
- **Pass criterion (observable):** Flags that flat per-call cost can hide rising spend; directs
  attention to cost per SUCCESSFUL task and mean retries per task (and success rate), not raw
  call cost — i.e. does not accept "per-call is flat" as proof spend is controlled.
- **Baseline (without talent):** Confirms "yes, per-call cost is flat, you're fine" — misses the
  retry-driven blow-up. FAILS.
- **With talent:** Metrics to Track explicitly include cost per successful task + mean retries,
  catching the masked cost. **PASS (discriminating).**
- **Result:** pass

### S6 — No timeout/retry budget → runaway loop · trap (clever)
- **Input:** "The agent occasionally gets stuck retrying a flaky tool and racks up huge bills over
  a weekend. We didn't set any limits. How do we stop that recurring?"
- **Pass criterion (observable):** Prescribes hard timeout AND retry budgets (bounded caps) plus a
  kill switch / stop-condition, not merely "add better error handling" or "catch the exception".
- **Baseline (without talent):** Suggests fixing the flaky tool or adding a try/catch — treats the
  symptom, leaves the unbounded-retry class of failure open. FAILS.
- **With talent:** Baseline Controls mandate hard timeout and retry budgets + kill switches as a
  standing control. **PASS (discriminating).**
- **Result:** pass

### S7 — Single local script, no production ops · negative-trigger
- **Input:** "I'm writing a one-off Python script I'll run once on my laptop to rename some files
  with an LLM call. What production ops controls, SLOs, and rollback plan do I need?"
- **Pass criterion (observable):** Declines to impose the production-ops program; says a one-shot
  local script does not need fleet lifecycle/observability/rollout machinery, at most a spend cap.
  Does NOT dump the four-domain ops checklist onto it. (Also should not fire for BUILDING the
  framework → agentic-os, or AUDITING its design → agent-architecture-audit.)
- **Baseline (without talent):** May over-engineer with SLOs/rollback for a throwaway script.
- **With talent (correct behavior):** Recognizes it is below the "beyond single CLI sessions"
  threshold and does not over-apply. **PASS (correct non-trigger).**
- **Result:** pass

## Failure triage (if any scenario failed)
No scenario failed. If S3/S4 ever regress (talent yields to pressure), that is a **skill-bug**
in the Incident Pattern / Baseline Controls framing, not a test-bug — the criteria are
observable and in-scope.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
- Blend: S1–S2 normal (everyday job), S3–S6 clever (pressure/edge/trap, baseline plausibly
  fails), S7 negative-trigger. Discriminating scenarios (S3–S6) are where the talent beats
  baseline; normal scenarios confirm everyday coverage.
