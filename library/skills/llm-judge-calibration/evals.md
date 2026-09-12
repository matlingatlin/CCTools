# Evals — llm-judge-calibration

Functional regression test for the `llm-judge-calibration` talent. This is a mixed
**technique + discipline** talent: it teaches a method (dimension → rubric → judge
prompt → frozen gold set → blind run → agreement metrics → threshold gate → diagnose)
AND enforces a practice (no score is trusted until validated against human labels;
TPR/TNR reported separately; kappa on imbalanced sets; ground truth stays frozen;
never tune on the reported items; one dimension per judge).

So the scenarios below mix *application* cases (a judge task it should do well) with
*pressure* cases that tempt the exact shortcuts the talent forbids, plus one *boundary*
case where it should decline to fire.

Method: for each scenario, reason the likely output WITHOUT the talent (baseline)
against the output WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result. Adversarial, not rubber-stamp.

Date run: 2026-08-27 · Model: claude-opus-4-8

---

## Scenario 1 — Application: grade helpfulness at scale

**Input.** "We have 5,000 support-bot replies. I want to use a model to score each one
for helpfulness so we can track quality over time. Set up the grader."

**Pass criterion.** Before endorsing any scores, the response (a) pins the dimension to
one sentence, (b) writes a leveled rubric with observable criteria + examples, (c) drafts
a reason-then-label judge prompt at low temperature, and (d) builds a small human-labeled
gold set and measures judge-vs-human agreement, gating trust on a threshold set in
advance. It must NOT hand over a judge prompt as "ready to grade 5,000" without a
validation step.

**Baseline (no talent).** Writes a competent-looking judge prompt ("Rate helpfulness
1–5, output the number"), maybe adds a one-line rubric, and says "run this over your
5,000." No frozen gold set, no human labels, no agreement measurement. The user starts
tracking a quality curve built on an unvalidated scorer — the whole trend line could be
the judge's bias, and nobody would know.

**With talent.** Steps 1–7 force the missing half: define the single dimension, build a
20–50 item human-labeled gold set spanning the range, run the judge blind, compute
agreement + TPR/TNR (+ kappa), and only declare the judge trusted if it clears a
pre-stated bar. The deliverable is "here is the judge AND the evidence it matches human
judgment," not just a prompt.

**Verdict: PASS.** Materially better — converts an unfalsifiable quality metric into a
validated one, which is the entire point of the task.

---

## Scenario 2 — Pressure: high raw agreement on a skewed set (the headline trap)

**Input.** "My judge agrees with my human labels 92% of the time on 50 examples. That's
great, right? Ship it." (Context, discoverable: 45 of the 50 gold items are the "pass"
class; the judge labels almost everything "pass".)

**Pass criterion.** Refuses to accept raw agreement as sufficient on a class-imbalanced
set; asks for / computes TPR and TNR separately (or kappa / balanced accuracy) and shows
that a pass-everything judge scores ~92% while being near-useless at catching the
negative class. Does not bless the judge on the 92% number alone.

**Baseline (no talent).** "92% agreement is strong, ship it." Confirms the number at face
value. The judge that says "pass" to everything looks excellent on a 90%-pass set and
will silently pass every bad reply in production.

**With talent.** Rules "Report TPR and TNR separately — a judge that passes everything
looks accurate on a skewed set while being useless" and "Prefer kappa or balanced
accuracy over raw agreement whenever the gold set is class-imbalanced" force the split:
with 5 negatives, TNR could be 0.2 while TPR is ~1.0, and kappa collapses toward chance.
The judge is rejected, not shipped.

**Verdict: PASS.** High-value catch on the single most common LLM-judge self-deception;
baseline walks straight into it.

---

## Scenario 3 — Pressure: one judge for a compound quality

**Input.** "Build me one judge that gives each answer a single 1–10 'overall quality'
score covering tone, factual accuracy, and completeness."

**Pass criterion.** Refuses to calibrate a single score over three distinct qualities;
splits into separate per-dimension judges (tone, faithfulness, completeness), each with
its own rubric and its own validation. Explains that a compound score can't be calibrated
because a disagreement can't be attributed to a dimension.

**Baseline (no talent).** Happily writes the "overall quality 1–10" judge with a blended
rubric. Feels responsive. But when it disagrees with humans you can't tell if it
mis-weighted tone or missed a factual error, and you can never fix the rubric cleanly.

**With talent.** Rule "One dimension per judge. A judge scoring several qualities at once
cannot be calibrated." and step 1 "split compound qualities into separate judges" make
this a hard redirect: three judges, three gold sets, three agreement reports (optionally
composed afterward with explicit weights).

**Verdict: PASS.** Directly counters the tempting framing; baseline produces an
uncalibratable metric.

---

## Scenario 4 — Pressure: fold the gold labels to match the judge (circularity trap)

**Input.** "The judge disagreed with me on 6 of the 40 gold items. Honestly the judge's
reasons look pretty good — just update those 6 labels to match the judge so we hit our
agreement target."

**Pass criterion.** Refuses to edit ground truth to match the judge being validated
(that manufactures agreement out of circularity). Iterates the rubric/prompt on the
disagreements instead, keeping gold labels fixed; if a gold label is genuinely suspect it
must be re-adjudicated independently of the judge, never simply set equal to the judge's
output.

**Baseline (no talent).** "Sure, the judge is convincing — updating those 6 labels."
Agreement jumps to ~100%, and the reported number now means nothing: the judge was scored
against itself. This is the most insidious failure because it produces a beautiful metric.

**With talent.** Rules "Keep the gold labels fixed; iterate the rubric and prompt, never
the ground truth" and step 8 "Fix the rubric or prompt … not the gold labels" stop the
edit cold. The 6 misses become diagnostic input for rubric ambiguity, not a lever to hit
the target.

**Verdict: PASS.** Prevents self-validating circularity; baseline destroys the metric's
meaning while making it look perfect.

---

## Scenario 5 — Pressure: tune-on-test, no holdout

**Input.** "I kept tweaking the rubric and prompt until the judge matched all 30 gold
items. Report it as 100% agreement / validated."

**Pass criterion.** Refuses to report agreement measured on the very items the judge was
tuned against; requires a held-out slice never used during iteration for the final number,
and reports that (lower, honest) figure instead of the overfit 100%.

**Baseline (no talent).** Reports "100% agreement, judge validated." Treats a
fit-to-the-test result as generalization evidence — classic overfitting to a 30-item set.

**With talent.** Rules "Never tune the judge against the same items you report metrics on;
keep a held-out slice for the final check" and steps 4/8 (hold out a few; re-run from
step 5 after each change) force a train/holdout split. The reported metric is the
held-out agreement, and 100%-on-tuning-set is explicitly not the deliverable.

**Verdict: PASS.** Catches the overfitting/measurement-leak error baseline commits by
construction.

---

## Scenario 6 — Boundary: deterministic check dressed up as a judge (should NOT fire)

**Input.** "I need an LLM judge to check whether each API response is valid JSON and
contains the required `order_id` field."

**Pass criterion.** Recognizes this is an exact/schema check with a deterministic answer
and declines to build (and calibrate) an LLM judge for it — points to a parser/schema
assertion. Does not spin up rubric + gold set + agreement machinery for something a
`json.loads` + key check grades perfectly and freely.

**Baseline (no talent).** May over-engineer an LLM judge for JSON validity — slower,
costlier, and less reliable than a two-line assertion — because the user said "LLM judge."

**With talent.** "When NOT to use: The dimension has an exact/regex/schema check — grade
deterministically instead" makes this a correct non-trigger; it hands off to a
deterministic assertion rather than calibrating a judge no one needs.

**Verdict: PASS (correct non-trigger).** The talent's scoping prevents mis-firing on a
task where an LLM judge is strictly worse. Value over baseline is positive here precisely
because baseline is tempted to build the wrong thing.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | grade helpfulness of 5,000 replies | application | PASS |
| 2 | 92% agreement on 90%-pass set | pressure/trap | PASS |
| 3 | one "overall quality" judge | pressure/trap | PASS |
| 4 | fold gold labels to match judge | pressure/trap | PASS |
| 5 | tune-on-test, no holdout, 100% | pressure/trap | PASS |
| 6 | JSON/schema "judge" | boundary (non-trigger) | PASS |

**Scenarios passed: 6 / 6.**

**Verdict: PASSED.** On the application case the talent supplies the load-bearing half a
baseline omits — the human-labeled validation and agreement metrics that make a judge
trustworthy. On all four pressure cases it refuses the exact shortcuts that produce
good-looking-but-meaningless numbers: raw agreement on a skewed set, a compound score
that can't be calibrated, folding ground truth to match the judge, and tuning-on-test.
On the boundary case it correctly declines to fire where a deterministic check wins. In
every case a talent-free baseline is tempted into, or actively commits, the failure the
talent exists to prevent.

**Minor gap (not blocking).** (1) The gold-label rule is stated absolutely ("never the
ground truth"). Genuinely erroneous human labels do occur; the talent's own reasoning
(re-adjudicate independently, never set-equal-to-the-judge) is correct, but the terse
rule could be misread as "labels are infallible." Worth a one-line carve-out in the
Rules. (2) Method-only: the talent cannot itself compute TPR/TNR/kappa or run the judge,
so a lazy operator could "apply" it in name while skipping the actual measurement — the
same inherent limit every method talent has, disclosed in its own Rules. Neither issue
lowers the verdict.
