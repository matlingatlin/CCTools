---
name: llm-judge-calibration
description: "Use when you need an LLM-as-judge to score a subjective or open-ended output dimension (tone, helpfulness, coherence, style, relevance, faithfulness, safety, refusal quality) and must trust its scores before relying on them — builds the judge rubric and prompt, then VALIDATES it against a small human-labeled set, measuring judge-vs-human agreement, TPR/TNR, and calibration before any score is believed. Triggers on 'LLM as judge', 'model-graded eval', 'AI grader/auto-grader', 'judge prompt', 'is my judge reliable', 'validate/calibrate the judge', 'judge agreement with humans', 'grade quality with a model'. NOT for building or running the eval harness/framework itself (use eval-harness), optimizing a target that already has a trusted scorer (use measured-optimization-loop), harvesting session lessons (use learn-eval), or objective checks a deterministic assertion can grade. NOT for reviewing a RETRIEVAL path itself (chunking, embeddings, rerank, top-k, grounding) — that is rag-pipeline-reviewer, an agent in .claude/agents/."
metadata:
  origin: ECC
tools: Read, Write, Edit, Bash, Grep, Glob
---

Build an LLM-as-judge for one subjective output dimension, then prove it matches human judgment on a small labeled set before trusting a single score.

## When to use
- You must score an output quality that no deterministic assertion captures (tone, helpfulness, faithfulness, style adherence, refusal appropriateness).
- You are about to grade many outputs with a model and need to know the grader is trustworthy first.
- An existing judge's scores are suspect and you want to measure its reliability.

## When NOT to use
- The dimension has an exact/regex/schema check — grade deterministically instead.
- You need the surrounding eval framework or a runner (eval-harness).
- You are tuning a metric that already has a trusted scorer (measured-optimization-loop).

## Steps
1. **Define the dimension.** Write one sentence naming exactly what is judged and what is out of scope. One dimension per judge; split compound qualities into separate judges.
2. **Write the rubric.** Enumerate discrete levels (e.g. pass/fail, or 1-4) with an observable criterion and a concrete example for each level. Prefer the smallest scale that carries the decision; binary is easiest to validate.
3. **Draft the judge prompt.** Instruct the model to output a fixed structure: brief reason first, then the label. Give it the rubric verbatim. Forbid it from rewarding length, fluency, or its own style. Fix temperature low for reproducibility.
4. **Build the gold set.** Sample 20-50 real outputs spanning the score range and edge cases. Have a human (or the requesting human) label each against the same rubric. Keep this set frozen and never let the judge see the labels. Hold out a few for a later re-check.
5. **Run the judge blind.** Score every gold item with the judge, no labels in context. Record label + reason per item.
6. **Measure agreement.** For binary: build the confusion matrix and compute TPR (recall on the positive/"pass" class), TNR (recall on the negative class), and raw agreement. For ordinal scales, add exact-match rate and off-by-one rate, and Cohen's kappa to discount chance agreement. State the numbers plainly.
7. **Gate on a threshold.** Decide the bar before looking (e.g. kappa ≥ 0.6, and both TPR and TNR ≥ 0.8) sized to the cost of a wrong score. If it clears, the judge is trusted for this dimension; record the metrics.
8. **Diagnose disagreements.** For each miss, read the judge's reason. Fix the rubric or prompt (ambiguous level, missing example, judge over-weighting a spurious cue) — not the gold labels. Re-run from step 5. Log what changed each round.
9. **Record the calibration.** Save rubric, judge prompt, gold set reference, final metrics, threshold, and date. A judge is trusted only for the dimension and output distribution it was validated on; re-validate when either shifts.

## Rules
- No score is trusted until the judge is validated against human labels. Agreement numbers are the deliverable, not the judge itself.
- Never tune the judge against the same items you report metrics on; keep a held-out slice for the final check.
- Report TPR and TNR separately — a judge that passes everything looks accurate on a skewed set while being useless.
- Prefer kappa or balanced accuracy over raw agreement whenever the gold set is class-imbalanced.
- Keep the gold labels fixed; iterate the rubric and prompt, never the ground truth.
- One dimension per judge. A judge scoring several qualities at once cannot be calibrated.
- Method only: no network calls, no CLI installs, no auto-run hooks. The human owns the labels.
