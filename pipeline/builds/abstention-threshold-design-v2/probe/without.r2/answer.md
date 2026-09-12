## Q1

Don't set the cut from the overall 5% error rate — that number is too blunt for financial documents, and "confidently wrong" is a calibration red flag, not just an accuracy stat. Do this:

1. **Pull the confidence/correct history** (score vs. correct, like the file in Q2) and build the actual precision-vs-coverage curve. Don't guess a round number.
2. **Target ≤1% error rate in the auto-approved bucket**, not 95% precision — a wrongly auto-approved invoice is a wrong payment, not just a re-review. That's a much tighter cut than a general classification task would use, and it will likely land higher up the confidence range, automating something like 40–55% of volume rather than 90%+.
3. **Add a dollar-value guardrail on top of confidence**: anything above, say, $5k (set to your real risk tolerance), or with a vendor/duplicate-payment anomaly, always goes to a human regardless of model confidence. Confidence alone shouldn't be the only gate on money leaving the building.
4. **Audit-sample the auto-approved bucket** — pull 5–10% weekly for human spot-check to catch drift/miscalibration before it compounds.

Capacity math: at 4,000/day with 6 reviewers, 100% manual review is already ~667 records/person/day — that's why you're asking. Cutting auto-approval to conservative but real (40–55%), the queue drops to roughly 1,800–2,400/day, or 300–400/person/day, which is sustainable. Start conservative, watch the audit sample, loosen the cut over a few weeks as calibration is confirmed — not the reverse.

## Q2

Computed the precision/coverage curve directly off the 200 rows (sorted by score descending, cumulative precision from the top):

| cut (score ≥) | auto-approved | correct | precision | coverage |
|---|---|---|---|---|
| 0.55 | 94 | 91 | 96.8% | 47.0% |
| **0.51** | **106** | **102** | **96.2%** | **53.0%** |
| 0.506 | 111 | 106 | 95.5% | 55.5% |
| 0.504 | 112 | 106 | 94.6% ✗ | — |

**Recommended cut: score ≥ 0.51.**

That buys you 106 of the 200 records auto-approved (53% of volume) at 96.2% precision — comfortably clear of the 95% target, not sitting right on the boundary. Only 4 wrong predictions slip through the auto-approved bucket (1.9% error rate in that bucket, vs. the file's overall 23.5% error rate). The remaining 94 records (47%) go to review — down from reviewing all 200.

If you want to push harder, 0.506 gets you to 55.5% coverage but the precision estimate (95.5%) is right at the wire on a sample this size (only 111 approved records back it) — one more wrong record and you're under target. I'd bank the small cushion at 0.51 rather than run the exact breakeven.

## Q3

**No.**

Two reasons:

1. **A stated "90% confidence" isn't the same as 90% actual accuracy.** Models — especially ones flagged as "confidently wrong" (as in Q1) — are frequently miscalibrated in exactly this mid-high confidence band. You don't know the true precision at 0.90 until you check it against outcomes, the way Q2 did. Assuming the number means what it says is how silent errors get into production.
2. **Even if it were well-calibrated, 90% confidence implies ~1-in-10 wrong on that bucket** if taken literally — unacceptable for financial/invoice data auto-approved with zero human eyes on it. A round confidence number picked by feel isn't a risk policy; it doesn't account for dollar exposure per error either (a $50 invoice and a $50k invoice shouldn't get the same treatment at the same confidence level).

Do what Q2 did: pull the actual score-vs-correct history, compute the precision at your real target, and pick the cut empirically — then layer a dollar-value guardrail on top. Don't ship a round-number heuristic on an unvalidated assumption.

## consulted
Read tool on `./scored_predictions.csv` (all 200 rows). Bash tool attempted (sort/awk/python3) for the Q2 calculation but every non-trivial command was denied approval in this environment, so the precision/coverage curve was computed manually from the file contents and cross-checked twice (bin totals against the full 47-error/153-correct count). No skills used.