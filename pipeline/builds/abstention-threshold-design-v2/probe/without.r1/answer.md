## Q1

Don't use a single "trust the model" / "review everything" toggle — calibrate a confidence cut against measured precision, and back it with non-model guardrails, because this is money movement, not a low-stakes classification task.

Concretely:
- **Target precision for auto-approve should be ~99%, not 95%.** A 1-in-20 error rate is fine to *flag for review*, but far too loose to let through with zero human eyes on invoice payments.
- **Find the score threshold empirically** the same way Q2 does: score every historical prediction against ground truth, sort by confidence descending, and find the cut where cumulative precision first hits ~99%. Don't guess a round number like "90%" — model confidence and empirical accuracy are often not the same number (see Q3).
- **Add hard guardrails independent of the confidence score**: a dollar-value ceiling (e.g. auto-approve only below your low-risk materiality threshold), exclusion of new/unverified vendors and first-time payees, and duplicate/anomaly checks. Confidence score alone shouldn't clear a $50k invoice from a new payee no matter how sure the model is.
- **Audit what you automate**: randomly sample ~5% of auto-approved records weekly for manual QA, and recalibrate the threshold monthly — model drift will move the precision curve over time.
- **Expected payoff**: at 4,000 records/day and 6 reviewers, the team is currently doing ~667 reviews/person/day — reviewing everything doesn't scale. Even a threshold that only auto-clears ~50% of volume cuts that to ~330/person/day, freeing the team to spend real time on the harder, lower-confidence half instead of rubber-stamping easy ones.

## Q2

Cutoff: **score ≥ 0.506** is the highest-coverage threshold in this data that still clears 95% precision.

- Auto-approved: 108 of 200 records (54% coverage)
- Correct among those: 103 → **precision = 95.4%**
- Remaining 92 records (46%) still go to human review

For a safer operating point (small sample, some margin above the 95% floor), round the cut up to **≥0.51**: 103 of 200 auto-approved (51.5% coverage) at **96.1% precision**.

What it buys: roughly half the volume moves off human review without a human touching it, while the other half — the genuinely ambiguous, lower-confidence cases — still gets reviewed. At 4,000 records/day that's ~2,100 auto-cleared and ~1,900 still reviewed, cutting the AP team's load by about half. The cost: at 95% precision, ~5 wrong records per 108 auto-approved slip through unreviewed (~4.6% leakage) — scaled up, that's on the order of 90-100 wrong auto-approvals a day with no human check. Whether that's acceptable depends on the dollar exposure per error; if not, tighten the cut toward 0.7-0.8, where this sample shows 100% precision but only ~16-27% coverage.

Caveat: this is 200 rows, so the exact threshold has real sampling noise (precision at n≈108 has roughly a ±4-5 point confidence band). Treat 0.506 as a data-derived estimate, not a number to hard-code into prod without validating against a larger set.

## Q3

No.

Two independent reasons:
1. **A model's self-reported "90% confident" is not the same thing as 90% empirical accuracy.** Confidence scores are frequently mis-calibrated (usually overconfident), so you have to check actual precision at that score against ground truth before trusting it — you can't take the number at face value. In this sample, 0.90+ scores did show 100% precision, but on only 11 examples — nowhere near enough data to bet an unreviewed-payment policy on.
2. **Even a validated, well-calibrated 90% cut isn't a safe bar for financial approvals.** A 10% error rate on unreviewed invoice payments, at 4,000/day, means hundreds of wrong payments going out daily with nobody checking. Q1 and Q2's data both point to needing ~99% empirical precision (not 90%) before removing the human, plus guardrails like dollar caps and new-vendor exclusions that a bare confidence threshold doesn't cover.

## consulted
- Read: `scored_predictions.csv` (full 200-row file, read directly and analyzed manually after Bash script execution was blocked by the sandbox's approval gate)
- Bash: `wc -l`, `python3 --version` (sanity checks only — `python3`/`awk`/`grep`/`sort` invocations for the actual analysis were all blocked by approval, so the threshold/precision/coverage numbers in Q2 were computed by hand from the file contents, then cross-checked with an independent error-count pass for consistency)