## Q1

Don't set a single global cut yet — you don't have a validated holdout for this model, and picking a round number ("route below 0.9 to review") is exactly the trap this process exists to avoid. Here's what to actually do, in order:

1. **Lock the two numbers first, with named owners.** Propose: precision target on auto-approved invoices = **99.5%** (AP/finance-control decision — a wrong auto-post is a GL error, potential overpayment, or audit finding, so it should cost far more precision than the model's raw 95%). Coverage floor = **≥70%** auto-approved (below that, the team of 6 isn't getting real relief). Get finance to sign off on the 99.5% and ops to sign off on the 70% — both in writing, before anyone looks at the score curve.
2. **Build a 300–500 record labeled holdout** from real traffic (include the hard/ambiguous vendors, not just easy ones), score it with the model's confidence, and run the AUROC + decile check (method step 4) *before* trusting the confidence score at all. Don't assume it's calibrated just because it's a probability — see Q3/Q4 below for why that assumption fails often.
3. **Sweep coverage vs. precision on that holdout** and pick the highest-coverage cut that still clears 99.5% precision. I can't give you that exact number without your score distribution (this is the same computation I ran for Q2 below — hand me the scored holdout and I'll do it in minutes).
4. **Layer business rules on top regardless of score**: new vendor, amount over some dollar threshold, duplicate-invoice flags, and bank-detail changes should route to a human even at 100% model confidence — that's consequence gating, not accuracy gating, and it composes with the threshold rather than replacing it.
5. **Staff the exception queue deliberately.** At 4,000/day, a 70% auto-approve rate leaves ~1,200/day for 6 people (~200/person/day) — a large drop from reviewing all 4,000 (~667/person/day today), and a realistic target for a team that size. If your holdout can't hit 70% coverage at 99.5% precision, that's a real finding — escalate it (improve the model, accept lower precision with sign-off, or accept lower coverage) rather than quietly shipping whichever number the curve gives you.
6. **Monitor the auto-approve rate as a drift alarm** and re-validate on every model/prompt change.

Until step 2–3 is done, keep 100% human review — don't ship an interim guessed threshold on a decision with real financial exposure.

## Q2

Ran it. `score` is a genuinely informative signal: **AUROC = 0.889**, and accuracy rises monotonically-ish across deciles (20% in the bottom decile → 100% in the top three), so it's safe to threshold.

Sweep (selected points):

| cut | coverage | precision |
|---|---|---|
| 0.40 | 70.5% | 91.5% |
| 0.46 | 62.5% | 92.0% |
| 0.50 | 56.5% | 94.7% |
| 0.505 | 55.5% | 95.5% |
| **0.52** | **51.0%** | **97.1%** |
| 0.58 | 43.5% | 97.7% |
| 0.60 | 40.0% | 98.75% |
| 0.62 | 36.0% | 100% |

The literal highest-coverage point that clears 95% is ~0.505, but at n=200 that's only ~111 records above the cut and the precision curve is visibly noisy there (one flipped label moves it a full point) — cutting exactly on the knife-edge risks shipping something that's actually under 95% in production. I'd set the cut at **0.52**: precision **97.1%** (99/102 correct) with margin over the target, coverage **51.0%** (102/200 auto-approved).

**What it buys:** just over half the volume gets auto-approved at a precision comfortably above your 95% target; the other 49% routes to review. If that coverage is below your floor, the fix is a better score (not a lower cut) — pulling the threshold down to hit more coverage means eating into the noisy 94–96% band, which isn't a safe place to sit on a 200-row holdout.

## Q3

**No.** Two separate reasons, both from the method:

1. **"90% confidence" hasn't been validated as meaning anything.** A model's self-reported/verbalized confidence is a different kind of number than a calibrated score, and it frequently carries little to no information about actual correctness — see Q4 below, where a self-reported-confidence system in your own files scores AUROC 0.48 (chance) despite most answers being stated at 0.9+. Before threshold on *any* confidence signal you have to bucket a labeled holdout by score and check it actually separates right from wrong. Skipping that turns "auto-approve at 90%" into abstaining on a random subset — full coverage cost, zero precision gain, and you won't find out until wrong answers are already auto-approved.
2. **Even if it were validated, 90% precision is picked in a vacuum.** Nobody named the actual precision target this decision needs, so 90% is a round number that "felt safe," not a derived cut. For most auto-approve/auto-send use cases the tolerable error rate on the answered segment is much tighter than 10%.

Bottom line: get a labeled holdout, check AUROC/decile separation for whatever confidence signal you're using, and only then sweep for the cut that hits your actual (named, signed-off) precision target.

## Q4

**Can't give you a cut — the signal doesn't work.** Ran the same validation:

- **AUROC = 0.482** (coin-flip is 0.50). Stated confidence carries essentially zero information about whether the answer is actually correct.
- Decile accuracy bounces around with no trend: 65%, 75%, 70%, 65%, 75%, 55%, 60%, 85%, 65%, 60% — top decile (confidence 0.99) is *less* accurate (60%) than several middle deciles.
- Overall accuracy is 67.5%, but stated confidence clusters almost entirely between 0.79 and 0.99 — the model is uniformly overconfident regardless of whether it's right, which is exactly the classic "self-reported confidence is near-constant and near-1.0 including on wrong answers" failure mode.

Per the method: **do not threshold an uninformative measure.** Any cut you pick here (0.9, 0.95, whatever) will auto-send a segment with essentially the same ~67-68% correctness as the unfiltered pool — it looks like a quality gate but it's actually close to a random sample, so you'd be auto-sending wrong answers to customers at roughly the base error rate while telling product it's gated at "95%+ confidence."

What to do instead: go back to step 2 of the method and try a different uncertainty signal — self-consistency across a few sampled generations, a separate judge/verifier model scoring the answer, or retrieval margin if this is RAG-backed. Build the same 200+ labeled holdout, check AUROC for each candidate, and only threshold whichever one actually separates correct from incorrect. I can run that validation as soon as you have scores for a candidate signal.

## consulted
- ./scored_predictions.csv (read, analyzed with a python3 script via Bash — AUROC, decile buckets, precision/coverage sweep)
- ./selfreported_confidence.csv (same analysis)
- Bash/python3 (ad hoc, no external libraries)
- The Abstention Threshold Design method supplied in the prompt