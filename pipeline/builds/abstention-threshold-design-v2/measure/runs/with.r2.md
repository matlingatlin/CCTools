## Q1

No cut, because there's no scored, labelled holdout to put it on — I'm not going to hand you a coverage band that isn't backed by data (that's the failure mode this kind of question invites: a guessed "top 40%" that becomes a staffing plan with error bars drawn on).

What actually needs to happen, concretely:

1. **Pull the data**: last several weeks of production invoice extractions, each with (a) the model's confidence score per record and (b) the AP reviewer's actual correct/incorrect verdict, sampled across vendors and document types — not just the easy ones. Whoever owns the extraction pipeline logs pulls this.
2. **Get two numbers signed off before anyone looks at the data**: the precision target on auto-approved invoices (this is a payments process — wrong auto-approvals cost real money, so I'd expect AP/Finance to want something north of 98-99%, but that's their call to make, not mine) and the minimum coverage below which the feature isn't worth shipping. Name an owner for each — Finance lead or AP manager, not me.
3. **Check the confidence score actually separates right from wrong** (bucket by decile, compute AUROC) before trusting it for anything. If it's flat, no cut helps and you need a better signal (self-consistency, a second-model check, a validator on required fields) before this is worth doing at all.
4. Once that's in hand, run exactly the procedure I ran for Q2 below — that's the template.

In the meantime: keep reviewing everything. At 4,000/day and six reviewers that's ~667/person/day, which is presumably already what's happening today, so there's no forced tradeoff to make blind.

## Q2

Signal tested: `score`. It separates — AUROC 0.889 on n=200, and accuracy rises monotonically by decile (20% in the bottom decile up to 100% in the top three deciles). Passes the gate; a cut on this is meaningful.

Sweep (coverage / n answered / precision on answered):

| cut | coverage | n | precision |
|---|---|---|---|
| 0.024 | 100.0% | 200 | 76.5% |
| 0.219 | 91.0% | 182 | 82.4% |
| 0.327 | 80.0% | 160 | 88.7% |
| 0.400 | 70.5% | 141 | 91.5% |
| 0.465 | 62.0% | 124 | 91.9% |
| 0.503 | 56.5% | 113 | 94.7% |
| **0.506** | **55.5%** | **111** | **95.5%** |
| 0.525 | 51.0% | 102 | 97.1% |
| 0.595 | 41.5% | 83 | 97.6% |
| 0.642 | 33.0% | 66 | 100% |

**Cut: score ≥ 0.506.** That's the highest-coverage cut that clears 95% precision: 55.5% of records (111/200) auto-approve at 95.5% precision. One case either side flips it — 110 answered gives 96.4%, 112 gives 94.6% — so this line sits right on the boundary with only ~111 answered cases behind the claim. That's a thin sample for a precision figure this precise (±~4pts at typical confidence intervals); treat 0.506 as a starting point, not a permanent constant, and re-cut once you have a few thousand labelled records instead of 200.

The other 44.5% (89/200) route to human review — same as today, just less of it. No daily-volume or reviewer-capacity target was given for this dataset, so I can't price that against a floor; if you want that priced, give me the floor number.

No floor/target owner was named for this task either — I used the 95% you gave me as the sole criterion. If someone wants a floor under 55.5% coverage, that's a separate conversation to have before shipping this cut.

## Q3

No.

Stated/verbalized confidence is a candidate signal, never a default — it has to earn the cut like any other signal, by separating correct from incorrect on real data. It routinely doesn't: a model can be "well calibrated" in aggregate (says 90% and is right ~90% of the time overall) while having almost no ability to rank any individual right answer above any individual wrong one. Those are different properties, and only the second one licenses a threshold.

I have a direct data point for this: Q4's self-reported-confidence file is exactly this setup, and on it the signal scores AUROC 0.482 — indistinguishable from a coin flip. A 90% cut there would let through wrong answers and hold back right ones at essentially random rates. Don't assume your system's stated confidence behaves differently without testing it the same way — but assume it might not, since that's the common case.

## Q4

No cut — this signal doesn't separate correct from incorrect, so there's no auto-send/support split I can defend.

`stated_confidence` on this holdout (n=200): AUROC 0.482 (chance is 0.500). Decile buckets don't rise with the score — they bounce between 55% and 85% with no trend, and the very top decile (0.99 confidence, n=20) is actually worse than the bottom of the tested range. A direct sweep confirms it: precision on the answered set holds flat at 65-69% from the lowest cut all the way to the highest (cut ≥0.99 → 65.6% precision, n=32) — barely different from just letting everything through unfiltered (67.5% base rate). Raising the cut buys you smaller coverage and no precision, which is exactly the failure mode of thresholding a signal that hasn't been checked: it looks like a knob, but it's not connected to anything.

Whatever precision bar Product has in mind for auto-send, this signal can't carry it at any coverage. Don't ship a cut on it. If you need this capability, test a different signal on this same holdout — self-consistency across resampled answers, or a second-pass verifier/judge score — and run the same separation check before trusting a threshold on it.

## consulted
- Skill: abstention-threshold-design (`./skill/SKILL.md`), invoked via the method text provided
- `./skill/references/uncertainty-signal-evidence.md` (verbalized-confidence separation claims, cited in Q3)
- `./scored_predictions.csv` (Q2, read and analyzed — AUROC, decile buckets, precision/coverage sweep)
- `./selfreported_confidence.csv` (Q4, read and analyzed — AUROC, decile buckets, precision/coverage sweep)
- Python (stdlib `csv`) run locally to compute AUROC, deciles, and sweeps on both CSVs — no external installs or services