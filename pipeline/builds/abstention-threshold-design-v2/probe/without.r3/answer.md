## Q1

Don't pick a single global cutoff off the top of your head — calibrate it against held-out outcomes and set it by dollar risk, not by a round confidence number. Concretely:

1. **Tier by confidence, not a single line.** Use the model's confidence to route into three buckets: auto-approve (high confidence), auto-flag-for-review (low confidence), and — if the model gives you a score, not just a class — a small "toss-up" middle band that goes to review too. A single cutoff optimized for overall precision will still auto-approve some expensive mistakes.
2. **Calibrate the threshold against actual correctness, not the stated confidence value.** "1 in 20 wrong overall" is an aggregate; the error rate is not uniform across the confidence range — errors cluster at low confidence. Pull a sample of scored + labeled records (same exercise as Q2) and find the score where precision in the auto-approve bucket clears your target (I'd argue for 99%+ on invoices, since errors mean wrong payments, not just annoyance).
3. **Add a dollar-amount override regardless of confidence.** Invoice risk isn't uniform — force human review on anything above a materiality threshold (e.g., >$5–10k) even if the model is 99.9% confident. This caps your worst-case exposure independent of model quality.
4. **Do the math on team capacity.** 4,000 records/day ÷ 6 people = ~667/person/day today, which is punishing for careful review. If calibration shows ~55–65% of volume can safely auto-approve at 99%+ precision, that drops the review queue to ~1,400–1,800/day, or ~230–300/person/day — a realistic full-review workload.
5. **Roll out gradually with a monitoring loop.** Start with a conservative (high) threshold, audit-sample 5–10% of auto-approved records weekly, and only lower the threshold as observed precision confirms it holds. Re-check quarterly for drift (vendor mix, invoice format changes).

Bottom line: don't set the cutoff, build the calibration step, then set the cutoff from the data — and keep dollar-amount and audit-sampling guardrails regardless of where it lands.

## Q2

Ran the numbers on the 200 rows.

- **Overall accuracy in the sample:** 76.5% (score alone is a weak proxy without a cutoff).
- **Recommended cutoff: score ≥ 0.55.**
  - Coverage: 94/200 records (47%) auto-approved.
  - Precision in that bucket: 96.8% (3 errors out of 94), comfortably clearing the 95% target with margin.
- Why not push the threshold lower to grab more coverage? The precision curve is noisy right at the 95% boundary in this sample (0.50 → 94.7%, i.e. just under target; 0.51 → ~96%; 0.55 → 96.8%) — with only ~100 records in the bucket, that boundary has a real ±4–5% margin of sampling error. 0.55 gives you a cushion instead of sitting exactly on the line.
- **What it buys:** you cut the human-review queue roughly in half — 47% of volume goes straight through, 53% still needs eyes. At 4,000 records/day that's ~1,880 auto-approved and ~2,120 still manual, versus 4,000 manual today.
- If you want more coverage and can tolerate the added risk, 0.50 gets you to 56.5% coverage but lands right at ~95% precision with no margin — I wouldn't recommend it given the sample-size noise. If you want a stricter, near-zero-error bucket, 0.65+ gives 100% precision in this sample but only 32% coverage.

## Q3

No. Two separate reasons:

1. **A stated "90% confident" score isn't the same as 90% actual precision.** Models are frequently miscalibrated (usually overconfident), and the only way to know what a given score band actually delivers is to check it against labeled outcomes — exactly what Q2 did. In that sample, a score of ~0.5–0.55 (i.e., "more likely right than wrong") only produced ~95–97% precision, not 50-ish%; the mapping from raw score to real-world accuracy isn't linear or intuitive, so a round number picked without calibration is a guess.
2. **Even if it really were 90% precision, that's a 1-in-10 error rate on invoices flowing straight to payment with no human check** — that's materially worse than the current 1-in-20 with full review, and now with zero backstop. For AP specifically, errors have direct financial consequences (overpayment, duplicate payment, wrong vendor), so the acceptable auto-approve error rate should be closer to 1% than 10%.

Use the calibration approach from Q1/Q2 to find the score that actually delivers your target precision, and layer a dollar-amount override on top — don't auto-approve purely on a round confidence number.

## consulted
Bash (read and analyzed ./scored_predictions.csv: row count, precision/coverage at multiple score thresholds)