## Q1

Don't leave it as "review everything," but don't hand it fully to the model either. Concrete plan:

- **Auto-approve only the top confidence band, not "most" predictions.** A blanket 95%-precision cut isn't good enough for money leaving the building — a wrong auto-approved invoice can mean overpayment or fraud, not just an annoying re-review. Target ~99%+ precision for the auto-approve tier, which will be a narrower band than you'd like (probably the top 30-50% of volume, not 80%).
- **Route the rest to the 6-person team**, but reallocate their time: instead of skimming all 4,000/day (which at ~4,000/6 ≈ 667 records/person/day is already too fast to be real review — ~0.7 min/record on an 8-hour day), they spend real time on the harder, lower-confidence 50-70%.
- **Always force human review regardless of score** for: new/unverified vendors, invoices above a dollar threshold, and anything flagged for duplicate/anomaly signals — confidence score isn't a proxy for these risks.
- **Audit the auto-approved bucket** with a random 5-10% daily sample reviewed after the fact, tracked as a rolling error rate. This is your early-warning system for model/vendor-mix drift and is what actually lets you trust the cut over time.
- **Calibrate the threshold from data, don't guess it** — plot accuracy vs. confidence score on historical labeled data and pick the score where the *conditional* accuracy clears your bar, then re-check monthly.

Bottom line: tiered auto-approve (high-confidence + low-risk) + audit sampling, not a single global cutoff.

## Q2

I computed precision/coverage at every threshold in the 200-row file. The score cut is **0.52**.

- Precision at 0.52: 99/102 = **97.1%** (point estimate), comfortably clearing the 95% target
- Coverage: **51%** of records (102/200) would be auto-approved
- That leaves 98 records/day (49%) still going to human review — down from all of them

Caveat worth flagging: with only 200 labeled rows, the 95% confidence interval on that precision estimate is wide (Wilson lower bound ≈91%), so treat 0.52 as a starting point, not a permanent setting — re-derive it once you have a few thousand more labeled records, and keep sampling the auto-approved bucket to confirm it holds in production.

If you want a bigger safety margin instead of maximum coverage: 0.60 gives 98.8% precision at 40% coverage; 0.70+ gives 100% precision (on this sample) at 27% coverage.

## Q3

No.

The premise of your own question is that the model is *confidently* wrong about 1 in 20 times — meaning its stated confidence doesn't reliably track correctness. Raw score ≠ calibrated probability. A flat "auto-approve at 90%" ignores that:

1. You haven't verified what precision 0.90 actually corresponds to for your data — it could be 99% or it could be 88%, and you won't know without backtesting against labeled outcomes (see Q2's method).
2. Even where it checks out numerically, "confidently wrong" cases are exactly the ones a blanket confidence cutoff won't catch, since they're the high-score errors by definition.
3. It ignores dollar-value and vendor-risk exceptions — a 90%-confident but large/unusual invoice shouldn't skip review just because the score cleared a bar.

Do the calibration exercise from Q1/Q2 first, pick a threshold empirically against your precision target, and keep dollar/vendor overrides and an audit sample regardless of where the threshold lands.

## consulted
- Bash — read and analyzed `./scored_predictions.csv` (200 rows) via a Python script to compute precision/coverage per threshold and Wilson confidence intervals for Q2