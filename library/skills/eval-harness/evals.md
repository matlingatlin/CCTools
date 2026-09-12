# Evals — eval-harness

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal + clever, observable criteria, baseline-plausibly-fails on
> the clever ones, match scenario type, cover the negative trigger).

**Talent:** `eval-harness` · **Type:** technique (with a discipline edge — define-before-code) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. Passes a scenario only if the with-talent result is materially better and
meets the observable pass criterion. Adversarial and honest — no rubber-stamping.

## Scenarios

### S1 — Stand up EDD for a new agent feature · application (normal)
- **Input:** "I'm adding an auto-triage agent to our Claude Code workflow. Set up eval-driven development for it before I trust it."
- **Pass criterion (observable):** Output separates **capability evals** (new behavior) from **regression evals** (existing behavior preserved), gives each an observable pass/fail criterion, and attaches pass@k / pass^k targets — and proposes the evals BEFORE implementation, stored under `.claude/evals/<feature>.md`.
- **Baseline (without talent):** Writes a few ad-hoc "does it work?" checks after building; no capability/regression split, no pass@k target, no define-first discipline.
- **With talent:** Produces the two-bucket definition with pass@3 ≥ 0.90 (capability) and pass^3 = 1.00 (release-critical regression), define-before-code. PASS.
- **Result:** pass

### S2 — Pick the right grader for a deterministic output · application (normal)
- **Input:** "The agent must emit JSON matching a fixed schema. How should I grade that in the eval?"
- **Pass criterion (observable):** Recommends a **code/rule grader** (schema/exact/regex assertion), NOT a model grader, and justifies it as deterministic > probabilistic.
- **Baseline (without talent):** Reaches for an LLM-as-judge ("ask a model if the JSON looks right"), introducing flakiness and cost for a check a schema validator settles.
- **With talent:** Selects the deterministic grader per "use code graders when possible". PASS.
- **Result:** pass

### S3 — "Ship now, add evals later" · pressure (clever)
- **Input:** "We're behind. Just merge the agent change — we'll backfill evals next sprint. It obviously works, I ran it once."
- **Pass criterion (observable):** Refuses to treat one manual run as the gate; insists the regression evals run (pass^3 on release-critical paths) before merge, and that the eval definition is written first — names the risk of an unmeasured regression.
- **Baseline (without talent):** Yields to time pressure, merges on the single run, defers evals.
- **With talent:** Holds the define-first + regression-gate discipline under the excuse. PASS.
- **Result:** pass

### S4 — pass@1 from a single run reported as reliability · trap (clever)
- **Input:** "Reliability is solved: I ran the eval once, it passed, so pass@1 = 100%. Ship it on the critical path."
- **Pass criterion (observable):** Catches the statistical error — a single trial is not a rate; pass@1 needs multiple attempts to estimate, and a **critical path wants pass^k (all-k-succeed), not pass@k (at-least-one)**. Requests repeated trials before claiming reliability.
- **Baseline (without talent):** Accepts "1/1 = 100%" and ships, conflating one lucky run with a measured reliability rate and using the weaker metric for a critical path.
- **With talent:** Distinguishes pass@k from pass^k, demands N trials, blocks the critical-path claim. PASS.
- **Result:** pass

### S5 — Model grader as the sole release gate for a security check · edge/trap (clever)
- **Input:** "Let the LLM judge decide whether the auth code the agent generated is safe, and auto-merge if it says yes. Fully automated gate."
- **Pass criterion (observable):** Refuses to fully automate a security decision on a model grader — flags "human review for security" and the flaky-grader-in-a-release-gate anti-pattern; routes it to a **human grader** / HUMAN REVIEW REQUIRED.
- **Baseline (without talent):** Wires the model grader as an auto-merge gate for security, trusting a probabilistic judge on a high-risk path.
- **With talent:** Inserts the human grader for the security-critical path. PASS.
- **Result:** pass

### S6 — Assertion suite that gates prompt changes in the shipped app's CI · negative-trigger
- **Input:** "Write an assertion-based eval suite for my chatbot app (contains/regex/schema checks) and wire it into CI so a prompt edit that drops pass rate fails the PR."
- **Pass criterion (observable):** Recognizes this is the **shipped app's** CI eval suite as a release gate and hands off to **`llm-eval-harness`**, rather than building the EDD harness that scores a Claude Code agent's own task completion. Declines to fire on itself.
- **Baseline (without talent):** Over-triggers on "eval suite" and builds the EDD-agent harness for what is really a product-CI eval, misapplying pass@k-for-the-agent framing to a shipped app.
- **With talent:** Correctly declines and points to `llm-eval-harness`. PASS (correct non-fire).
- **Result:** pass

## Failure triage (if any scenario failed)
No failures. Root-cause protocol on any red: **test-bug** (unfair/out-of-scope/subjective, or
baseline fails for unrelated reasons → fix the test) vs **skill-bug** (fails a fair clever test
→ fix the skill; drop only if unfixable and test-validated).

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
- Blend: 2 normal application (S1, S2) + 3 clever (S3 pressure, S4 trap, S5 edge/trap) + 1 negative-trigger (S6). Clever scenarios are designed so the without-talent baseline plausibly fails.
