## Q1

Don't pick a confidence cut yet — pick a process, then let a calibration check set the number.

"Confidently wrong" is the tell: if the model is overconfident on its errors, raw score isn't a trustworthy proxy for correctness (see Q4 below — that's exactly what a miscalibrated confidence signal looks like). Cutting at an arbitrary score like 0.90 could wave through a disproportionate share of the 5% error rate.

What to actually do:
1. **Calibrate first.** Pull ~500–1,000 recently-reviewed records with human-verified labels, plot precision vs. score exactly like Q2. Takes a day, not a quarter.
2. **Set the bar higher than 95% precision for auto-approve.** Invoices move money — target ≥99% precision on the auto-approved bucket, not 95%. A 1-in-20 error rate sitting inside auto-approved-and-unreviewed is not acceptable for AP.
3. **Cap the blast radius regardless of score:** hard-block auto-approval above a dollar threshold (e.g. $2,500), for new vendors, first invoice from a vendor, or any PO/amount mismatch — no confidence score overrides these.
4. **Never let auto-approve go dark:** pull a random 5–10% audit sample from the auto-approved bucket weekly and re-check precision. Recalibrate the cut monthly — model and vendor mix both drift.
5. **Redeploy the 6 FTE, don't cut them.** If calibration clears ~50% of volume at ≥99% precision (a realistic shape based on curves like this), manual review load drops from 4,000/day to ~2,000/day. Use the freed capacity for deeper review of the flagged/high-risk half and the audit sample — not headcount reduction, since the humans are your drift detector.

Bottom line: no cut goes live until step 1 produces a real precision curve on this model. Everything else in this list is the guardrail structure around whatever number that curve gives you.

## Q2

Cut: **score ≥ 0.60**.

The raw crossing point where precision first reaches 95% is score ≥ 0.506 (111/200 kept, 95.5% precision) — but with only 200 labeled points, that boundary is noisy (Wilson 95% lower bound on it is only ~90%). Building in margin:

- **Cut at 0.60:** 80 of 200 records auto-approved (40% coverage), precision 98.75% (Wilson lower bound 93.3%).
- Below 0.60: 120 records (60%) still go to human review.

What it buys: **40% of volume moves to auto-approve at ~99% observed precision**, cutting manual review load by roughly two-fifths while keeping a real safety margin under the 95% target given the sample size. Revisit the cut once you have more labeled data — 200 points is enough to set a first threshold, not enough to trust the exact boundary to the third decimal.

## Q3

**No.**

"90% confident" only means something if that number is calibrated — and confidence scores aren't calibrated by default. The two files in this batch are a clean before/after of exactly this: in `scored_predictions.csv`, score ≥ 0.90 does hold up (100% precision, though only n=11). In `selfreported_confidence.csv`, an LLM's *stated* confidence ≥ 0.90 is basically worthless — 66% precision, barely above the 67.5% base rate, because stated confidence there is uncorrelated with correctness (r = -0.03).

Don't set a 90% cutoff on faith. Check precision-at-that-cut against held-out labels first (the Q2 exercise). If it holds, fine — but verify per-model, per-deployment; calibration isn't a property of "AI confidence" in general, it has to be earned by each system.

## Q4

**Do not launch this on stated_confidence — no cut clears the target.**

Stated confidence in this file ranges only 0.79–0.99 (never expresses doubt below "fairly sure"), and it's uncorrelated with actual correctness (r = -0.03). Precision by threshold:

| cut | coverage | precision |
|---|---|---|
| ≥0.80 | 98.5% | 68.0% |
| ≥0.90 | 68.0% | 66.2% |
| ≥0.95 | 34.0% | 69.1% |

Even at the highest stated-confidence band (≥0.95), precision tops out at 69% — nowhere near the 95% bar Product wants, and it doesn't even trend upward with higher stated confidence. Overall accuracy is 67.5%, so this "confidence" score is functionally noise; auto-sending on it would send wrong answers to customers about a third of the time no matter where the cut is set.

What I'd tell Product: the LLM's self-reported confidence isn't usable as a routing signal for this system. Options: (a) route everything to support until a real calibrated confidence estimator is built (e.g. a separate scoring model trained against labeled correctness, the way `scored_predictions.csv` was), or (b) route by other signals (query type, retrieval match quality, historical accuracy by category) instead of the model's own stated certainty. Don't ship a threshold on this column.

## consulted
Bash (python3) — computed precision/coverage tables and Wilson confidence intervals over `./scored_predictions.csv` and `./selfreported_confidence.csv`. No skills or other files used.