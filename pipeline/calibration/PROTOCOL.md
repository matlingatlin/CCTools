# Baseline calibration — protocol

Written BEFORE any result was seen. Thresholds set in advance; changing them after looking at
the numbers would make this an exercise in confirming what we already believed.

Follows `llm-judge-calibration`, with one deliberate deviation recorded at the bottom.

## The claim under test

`ledgers/evals.jsonl` carries a `baseline` field per scenario. Across all 181 live rows it is a
**perfect function of the scenario's own label**: adversarial → `miss` in 85/85, normal → `pass`
in 80/80, negative-trigger → `miss` in 15/15. Zero exceptions.

A field that reproduces the label beside it carries no independent information. So the library's
central quality claim — *the clever scenarios beat baseline, therefore the talent earns its
place* — currently rests on an author's expectation, never on an observation. This measures how
often that expectation is right.

## Dimension (one, per the talent's rule)

**Does a capable assistant WITHOUT the talent meet this scenario's stated pass criterion?**
Binary: `pass` / `miss`. Out of scope: whether the talent is good, whether the scenario is
well-written, whether the criterion is the right one.

## Method

1. **Gold set** — 20 scenarios sampled from the 180 with an extractable Input and Pass criterion:
   12 adversarial, 6 normal, 2 negative-trigger, at most 2 per talent, across 14 talents.
   Seed pinned (`20260828`) so the sample is reproducible. Frozen in `gold-set.json`.
2. **Observation, not judgment** — each scenario's **Input** is handed to a fresh agent that is
   told to solve it as an ordinary capable assistant, and is explicitly forbidden from reading
   `.claude/skills/`, `.claude/agents/`, or any method file. It never sees the pass criterion, so
   it cannot aim at it. This is the step that breaks the circularity: the label is what a baseline
   DID, not what anyone predicted it would do.
3. **Scoring** — the recorded output is compared against the scenario's pass criterion. The
   criterion is required to be observable, so scoring is a check, not an opinion. Every scored
   `pass` must quote the span of baseline output that meets it.
4. **Agreement** — confusion matrix of claimed vs observed, with TPR/TNR reported separately per
   the talent's rule, plus Cohen's kappa (the set is class-imbalanced by construction).

## Threshold, fixed in advance

The claimed `baseline` field is **trustworthy** if agreement ≥ 0.80 AND the adversarial class
alone shows ≥ 0.75 observed `miss`.

Below that, the field is decoration and the honest options are to run real baselines going
forward or to stop making the claim. Between 0.60 and 0.80, it is usable only with the measured
error rate always stated beside it.

**Expected failure mode, named in advance:** adversarial scenarios where a capable baseline
happens to pass. Those are not scenario bugs — they mean the talent's edge is smaller than the
suite asserts on that case.

## Deviation from `llm-judge-calibration`, stated plainly

Step 4 of that talent requires a HUMAN to label the gold set, and its rules say the human owns the
labels. Here the labels are produced by running baselines instead. That is weaker than human
ground truth in one specific way: the same model family both produces and scores the baseline
output, so a blind spot shared across both would go undetected.

It is stronger than the alternative actually on offer — the coordinator hand-labelling from
opinion — because each label is an experiment whose inputs and outputs are recorded and can be
re-run or overruled. The gold set is built so a human can spot-check any row cheaply: read the
Input, read what baseline produced, read the criterion, disagree if warranted. Human overrides
take precedence and are recorded in `observed_by`.
