Found it: **two merchants have `amount` in cents instead of dollars.**

## The bug

| Merchant | Rows in cents | Detection |
|---|---|---|
| `belltower` | **440 / 440** (all) | every value is a whole number ending `.0`, median 2726 → $27.26 |
| `harborview` | **38 / 240** (mixed) | integral values only, all ≥ 181; the other 202 rows are correct |

The giveaway is that these are the *only* integral-valued amounts above ~151 in the file. Every other merchant has integral amounts too (35 of them — legitimate round-dollar charges like `13.0`, `40.0`), but they max out at `151.0`. Harborview's integral rows start at `181.0` and run to `12717.0`, and dividing them by 100 gives a median of $28.75 — matching harborview's own non-corrupted median of $29.41.

Harborview is the worse case: it's a *partial* corruption, scattered across the file (rows 279–3904, all four channels, all statuses), so there's no contiguous bad batch to slice out. Note harborview also doesn't appear in `reference.csv` at all — it's a new merchant, which is likely why its integration shipped with an inconsistent unit.

## Why the column stats pass

Quantile checks look clean because only 478 of 4000 rows (12%) are affected and they're pushed entirely into the tail:

| | reference | current | corrected |
|---|---|---|---|
| median | 29.84 | 33.96 | 29.63 |
| p25 / p75 | 17.5 / 51.2 | 18.8 / 70.8 | 17.3 / 51.3 |
| mean | 41.08 | **497.36** | 41.71 |
| max | 564.33 | **20625.00** | 678.79 |

Min, null rate, dtype, and the quartiles all pass. Only mean and max actually move — and if your monitoring uses median/IQR (as robust checks usually do, precisely to resist outliers), it sees nothing.

## Fix

```python
cents = (df.merchant == 'belltower') | ((df.merchant == 'harborview') & (df.amount % 1 == 0) & (df.amount >= 100))
df.loc[cents, 'amount'] /= 100
```

That restores mean 41.71 / median 29.63 / max 678.79 against the reference's 41.08 / 29.84 / 564.33.

The `>= 100` guard on harborview is a heuristic, and it's the one weak point: a genuine harborview charge of exactly $181.00 would be wrongly divided, and a cents value below 100 (a sub-$1 charge) would be missed. If the source system has a per-row timestamp or ingestion batch id, keying off that would be exact — worth checking before running this on the real table.

One unrelated thing I noticed while parsing: row `T004001` has `settled_days` of `"1 d"` rather than a number, so that column isn't cleanly numeric either. Separate issue, not chased down.
