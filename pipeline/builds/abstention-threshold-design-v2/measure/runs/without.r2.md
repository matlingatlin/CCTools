## Q1

Set the auto-approve bar much higher than the "95% precision" instinct — this is money leaving the building, not a content-moderation queue. Target **≥99.5% precision on the auto-approved bucket** (i.e., ≤1 error in 200 auto-approved invoices), not 95%. A model that's "confidently wrong" 1 in 20 overall can still hit that bar on its high-confidence subset — but you have to derive the actual score cutoff from your own precision/recall curve on held-out labeled data (same method I used in Q2), because it depends on your model's calibration, not a rule of thumb.

Practical rollout:
- **Phase 1:** pick the score cutoff that empirically clears 99.5% precision on a validation set. Expect that to cover somewhere around 40–60% of volume for a model this error-prone (a well-calibrated model with a 5% overall error rate typically needs to give up a lot of coverage to buy that much precision — see Q2's curve for the shape of that tradeoff).
- Route everything below the cutoff to full human review, same as today.
- **Audit, don't trust blindly:** pull a random 5% of auto-approved records daily for human spot-check, and track precision on that sample weekly. If it drifts below 99.5%, raise the cutoff back up.
- Capacity math: at 4,000/day fully reviewed, your 6-person team is doing ~667/person/day. If the cutoff clears 50% of volume, review load drops to ~2,000/day (~333/person/day) — that's what actually buys headroom, not the raw precision number.
- Expand the auto-approve share only as audit data accumulates confidence in the calibration — don't jump straight to a high coverage target on day one.

## Q2

Read `scored_predictions.csv` (200 rows) and swept every threshold. The lowest cut that clears 95% precision on point estimate is **t ≈ 0.53** (99 auto-approved, 49.5% coverage, precision 96.97%, 3 errors).

But with only 200 rows, that point estimate is noisy — the 95% Wilson lower bound at t=0.53 is only 91.5%, meaning the true precision could plausibly be below your 95% target. If you want a cut that's actually defensible at 95% with margin, use **t ≈ 0.60**: 80 auto-approved (40% coverage), precision 98.75%, Wilson lower bound 93.3%, only 1 error in the sample.

What it buys: at t=0.60, you auto-approve 40% of volume and send the other 60% to review — cutting review load by 40% while keeping the error rate on auto-approved records to roughly 1-2%. Recommend re-running this on a larger sample (200 rows is thin for a precision claim you're going to act on) before locking the number in production.

## Q3

No. Two separate problems: first, a flat "model says 90%" cutoff still means roughly 1 error in every 10 auto-approved records if that confidence is well-calibrated — worse than the 1-in-20 error rate you're currently catching with full human review, except now nobody catches it. Second, "90% sure" as stated by a model is frequently not well-calibrated to begin with (see Q4 — in that dataset, stated confidence had essentially zero correlation with actual correctness, r ≈ -0.03). You'd be trusting a number that may not mean anything. Don't gate auto-approval on a round-number confidence claim — derive the cutoff empirically from a precision curve against labeled outcomes (Q2's method), target ≥99%+ precision for anything unreviewed, and re-validate periodically since calibration drifts.

## Q4

There is no cut that works here — don't ship this. I checked `selfreported_confidence.csv`: stated confidence ranges only from 0.79 to 0.99 (the model never says it's unsure), overall accuracy is 67.5%, and accuracy is flat across confidence bins regardless of threshold:

| stated conf ≥ | coverage | accuracy |
|---|---|---|
| 0.79 | 100% | 67.5% |
| 0.85 | 89% | 67.4% |
| 0.90 | 68% | 66.2% |
| 0.95 | 34% | 69.1% |
| 0.99 | 16% | 65.6% |

Correlation between stated confidence and correctness is essentially zero (-0.03). Raising the cutoff buys you nothing — accuracy at the top confidence band (≥0.99) is actually the same or worse than at the bottom. This LLM's self-reported confidence is not a signal of correctness at all; it's clustered near the top regardless of whether the answer is right. Auto-sending on any cut of this number means auto-sending wrong answers to customers at roughly the same ~30-35% error rate no matter where you draw the line.

Recommendation: don't gate on `stated_confidence`. If you need an auto-send/route-to-support split, build a real calibrated confidence signal (e.g., a small classifier trained on features of the response, or consistency-based self-check sampling) and validate it the way I did in Q2 before trusting a threshold.

## consulted
- Read: `./scored_predictions.csv`, `./selfreported_confidence.csv`
- Bash: `python3` (csv, statistics, Wilson confidence interval calculations) to compute precision/coverage sweeps and calibration bins on both files