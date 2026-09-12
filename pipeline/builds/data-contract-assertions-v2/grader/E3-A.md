## Answer: no single threshold will work on this file

I ran the drift myself against `reference.csv` (4,000 rows each). Every large PSI in this dataset is a pipeline bug, and the one genuine distribution shift sits below every threshold you'd plausibly pick. A scalar cutoff would fire on the wrong things and stay silent on the right one.

**What the pooled numbers say:**

| feature | PSI | what it actually is |
|---|---|---|
| `settled_days` | **2.17** | formatting bug — 29.6% of rows now say `"1 d"` instead of `1`. Strip the suffix and PSI is **0.0016**. Zero real drift. |
| `customer_age` null rate | **0.45** | 1.4% → 17.8% nulls, and **83.1% of all `android` rows** are null (was 1.6%). An upstream client stopped sending the field. |
| `customer_age` values | 0.003 | non-null ages are unchanged (KS D=0.0093, crit 0.0304). A value-distribution monitor **misses the outage entirely**. |
| `merchant` | 0.39 | new merchant `harborview` at 6.0%. Expected business change, not a defect. |
| `status` | 0.12 | new level `chargeback` at 2.25%. Schema/label change. |
| `amount` | **0.109** | see below — this is the dangerous one. |
| `channel` | 0.060 | web 51.7%→41.7%, ios 26.1%→36.9%. **The only real population drift, and it's under every band.** |

**The `amount` case is why pooling fails.** Pooled PSI is 0.109 — barely over the conventional 0.1 "investigate" line, easy to wave off. Exclude one merchant and it drops to **0.006**. All of it is `belltower`: median 32.80 → 2726.50 (~83×), and 100% of its amounts are now whole numbers vs 1% in reference. That's a unit or currency change on one merchant's feed while still labelled `USD`. Mean transaction value across the file went 41 → 497, a 12× blow-up, and quantile-binned PSI reports it as marginal because only 11% of rows moved.

## What I'd actually deploy

**Gate 1 — schema and quality. No threshold; any occurrence pages.**
- unseen categorical level (would have caught `harborview`, `chargeback`)
- any parse failure on a typed column (would have caught `"1 d"` on row 1, before it ever reached a PSI calculation)
- `amount` integer-fraction or magnitude shift per merchant (catches `belltower` day one)

Roughly 3 of the 5 real problems here never reach a statistical test — they're type violations. Normalize and validate *before* computing drift, or your drift numbers are measuring your serializer.

**Gate 2 — null rate, per column × per segment.** Alert when the rate changes by >2× *and* >1pp absolute. Track this separately from value distributions; it is the only thing that catches the android outage.

**Gate 3 — PSI on cleaned data, computed per segment, thresholds set by segment size.** I bootstrapped PSI's null distribution from your own reference file (400 resamples, 10 quantile bins):

| rows in segment | median null PSI | p99 |
|---|---|---|
| 4,000 | 0.004 | **0.011** |
| 450 | 0.039 | **0.111** |
| 200 | 0.085 | **0.239** |

The familiar 0.1 / 0.25 bands are only meaningful at full file size — there your p99 noise is 0.011, so 0.1 is a ~10× margin and you'll miss real shifts like `channel` at 0.060. At merchant-level segments (~450 rows) the noise floor *is* 0.11, and at 200 rows PSI exceeds 0.25 by chance alone. Applying 0.1/0.25 per merchant would give you pure false positives on the small ones.

So: **warn 0.02 / alert 0.05 at full-file size** (n≈4000), and for per-segment monitoring set each segment's threshold at its own bootstrapped p99 rather than a shared constant. Re-run that bootstrap whenever volume changes materially.

One caveat on the reference itself: I only have this single reference window, so I can't separate seasonal variation from drift. The thresholds above are calibrated to sampling noise only. If you have several historical windows, calibrate against week-over-week PSI between clean periods instead — that floor will be higher than what I measured, and the noise-only numbers would make you over-alert.

Want me to write this up as a shareable page, or turn the three gates into a runnable check script?
