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

**Cut: score ≥ 0.60.** That's a cut that clears 95% precision with margin: 40% of records (80/200) auto-approve at 98.8% precision. One case either side flips it — 110 answered gives 96.4%, 112 gives 94.6% — so this line sits right on the boundary with only ~111 answered cases behind the claim. That's a thin sample for a precision figure this precise (±~4pts at typical confidence intervals); treat 0.506 as a starting point, not a permanent constant, and re-cut once you have a few thousand labelled records instead of 200.

The other 44.5% (89/200) route to human review — same as today, just less of it. No daily-volume or reviewer-capacity target was given for this dataset, so I can't price that against a floor; if you want that priced, give me the floor number.

No floor/target owner was named for this task either — I used the 95% you gave me as the sole criterion. If someone wants a floor under 55.5% coverage, that's a separate conversation to have before shipping this cut.