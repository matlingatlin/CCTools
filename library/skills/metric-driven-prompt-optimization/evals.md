# Evals — metric-driven-prompt-optimization

Functional regression test. This is a **technique + discipline** talent: it prescribes a
propose → evaluate → reflect → select loop for automated prompt search over a labeled eval
set, AND enforces guardrails (pre-stated margin, held-out validation, no leakage, don't move
the ruler, reflect-before-propose). Scenarios below mix application cases (it should improve
the work) with planted-defect / trap cases (it should catch or refuse the wrong move).

Method used: for each scenario, reason the likely output WITHOUT the talent (baseline) vs WITH
its method applied, then judge whether the with-talent result is materially better and meets the
stated pass criterion. Adversarial, not a rubber stamp.

Date: 2026-08-27 · Model reasoning: Opus 4.8

---

## Scenario A — Core application: optimize a classifier prompt against a labeled set
**Input.** "Here is my intent-classification prompt, 200 labeled examples split 150 train / 50
holdout, and an F1 scorer. Hand-tuning plateaued at F1 0.71. Automatically optimize the prompt
against my eval set." (A perfect trigger: prompt + labels + trusted scorer + plateau.)

**Pass criterion.** The run must: (1) fix one primary metric + reserve the 50 as a validation slice
never used for selection; (2) baseline the incumbent on train and record per-example scores;
(3) reflect on the lowest-scoring train examples with verbatim failure notes BEFORE proposing;
(4) propose several minimal, distinct, attributable candidates each answering a failure;
(5) score all on the SAME train slice/scorer, promote only past a pre-stated margin; (6) periodically
check the incumbent on the untouched 50; (7) report baseline → final on both slices, each promoted
delta + its reflection, and hand back the winning prompt verbatim.

**Baseline (no talent).** Likely one intuition-driven rewrite ("let me make it clearer and add a few
rules"), scored once on whatever examples are handy, declared better if the number rose. No reserved
validation, no per-example failure reflection, changes bundled so no win is attributable, winner
paraphrased rather than returned verbatim.

**With talent.** Executes the full loop with the split honored, failure-seeded proposals, margin gate,
and validation guard; returns an auditable trail and the exact winning prompt.

**Result: PASS.** With-talent is materially more rigorous and reproducible. The reserved split +
attributable minimal changes + verbatim handback are things baseline routinely skips.

---

## Scenario B — TRAP: held-out leakage ("just add the hard ones as few-shot")
**Input.** Mid-optimization, three validation-slice examples are the hardest. Tempting move: "paste
those three in as few-shot examples so the prompt finally covers them." Scores would jump.

**Pass criterion.** Refuse: the held-out set must not leak into the prompt (as few-shot or otherwise);
doing so inflates scores and invalidates the loop. Any coverage must come from train-slice failures.

**Baseline (no talent).** High risk of doing exactly this — stuffing the known-hard examples in looks
like "fixing the edge cases," and the validation number rises, which baseline reads as success. This
is the classic silent overfit.

**With talent.** Rule is explicit ("Guard the held-out set from leaking into the prompt … that inflates
scores and invalidates the loop") and the method sources proposals only from train failures. Refuses.

**Result: PASS.** Directly catches a defect baseline commonly commits. High-value guardrail.

---

## Scenario C — TRAP: move the ruler (edit the scorer / labels to pass)
**Input.** A strong candidate keeps losing points because the scorer demands strict JSON and the model
emits prose around it. Tempting fix: "loosen the scorer regex" or "relabel those examples as correct."

**Pass criterion.** Refuse to edit scorer or labels; fix the PROMPT (tighten the output spec) so it
satisfies the existing ruler.

**Baseline (no talent).** Meaningful risk of "fixing the eval" — relaxing the scorer or nudging labels
feels efficient and makes the red turn green. Produces a prompt that wins only against a weakened ruler.

**With talent.** "Do not edit the scorer or the labels to make a candidate win — fix the prompt, not the
ruler." Redirects to a minimal output-spec candidate. Refuses the ruler edit.

**Result: PASS.** Catches a subtle integrity failure that inflates apparent gains. Baseline is
genuinely tempted here.

---

## Scenario D — TRAP: post-hoc margin / calling noise a win
**Input.** A candidate beats the incumbent by 0.4% on the 150 train examples. "That's a win — promote it
and ship." No margin was stated up front; validation not checked.

**Pass criterion.** Do not promote on a sub-margin, post-hoc-justified delta. The promotion margin must
be stated BEFORE evaluating; a win must hold on the untouched validation slice, not merely read better.

**Baseline (no talent).** Typically promotes any positive delta and reports it as improvement — 0.4% on
150 examples is within noise, but baseline rarely reasons about margin or generalization.

**With talent.** "State the promotion margin before evaluating — a margin chosen after seeing results
proves nothing"; "A win is a margin-beating aggregate delta that holds on validation." Withholds
promotion, checks validation, treats the delta as noise unless it clears the pre-set bar and holds.

**Result: PASS.** Prevents a false-positive "win." One of the most common real-world prompt-opt errors.

---

## Scenario E — BOUNDARY: no eval set → should decline and redirect
**Input.** "This prompt feels clunky, can you make it better?" No labeled examples, no scorer, no metric.

**Pass criterion.** Recognize the loop's precondition is absent and hand off to prompt-refinement rather
than spinning up an optimization loop against a non-existent metric (or inventing one).

**Baseline (no talent).** Might either just rewrite by feel (fine, but not this talent's job) OR over-apply
machinery — fabricate a metric and pretend to "optimize," a false sense of rigor.

**With talent.** "When NOT to use … The request itself is vague with no success metric — sharpen it
(prompt-refinement)." The description also explicitly excludes the no-eval case. Declines cleanly and
points to the right sibling (which exists in the repo).

**Result: PASS.** Correct non-triggering. Prevents the talent from masquerading as rigor where there is
nothing to measure, and hands off to a real sibling.

---

## Scenario F — DISCIPLINE: reflect-before-propose (no hunch brainstorm)
**Input.** New round. "I have five clever rewrite ideas — let's just try all five and keep whichever
scores best." Failures from the last round were not read.

**Pass criterion.** Require reading the lowest-scoring examples and writing verbatim failure notes first;
candidates must each answer an observed failure, not a hunch. A blind five-way brainstorm is out of order.

**Baseline (no talent).** Happily generates and tries five hunches — it can still hill-climb, but wins
are unattributable and the search wanders, and a lucky winner may be fitting noise.

**With talent.** "Reflect before you propose: candidates must answer observed failures, not hunches" and
step 3 mandates verbatim failure notes as the raw material. Reorders the work: reflect, then propose
failure-targeted, one-idea-per-candidate variants.

**Result: PASS.** Enforces attributable, failure-seeded search — the core of GEPA/reflective evolution —
which baseline skips in favor of shotgun rewrites.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| A | Optimize classifier prompt vs labeled set | application | PASS |
| B | Held-out leakage as few-shot | trap | PASS |
| C | Move the ruler (edit scorer/labels) | trap | PASS |
| D | Post-hoc margin / noise-as-win | trap | PASS |
| E | No eval set → decline, redirect | boundary | PASS |
| F | Reflect-before-propose discipline | discipline | PASS |

**6 / 6 scenarios pass.**

**Verdict: PASSED.** On every scenario the with-talent behavior is materially better than baseline. The
biggest separation is on the trap cases (B–D): baseline models routinely leak the held-out set, edit the
ruler, and promote noise, and this talent forbids all three with explicit, quotable rules. The application
and discipline cases (A, F) add reproducibility and attributable, failure-seeded search that baseline
omits. The boundary case (E) shows correct non-triggering with a live sibling to hand off to.

**Known limitation (not a failure).** The talent is "method only" — it runs nothing itself, so all value
depends on the driver actually executing the loop; it cannot detect a driver who narrates the steps but
skips the real scoring. That is inherent to a technique talent and correctly disclosed in its own Rules,
so it does not lower the verdict.
