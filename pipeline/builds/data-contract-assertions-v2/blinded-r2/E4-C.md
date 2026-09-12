## Found it: a unit mismatch (cents written into a dollars column), hidden inside two merchants

The column-level stats mask it because the bad rows are a *minority mixed into a majority* — but `merchant` splits it wide open.

**The tell:** 513 rows have an integer-valued `amount` (`x % 1 == 0`). The natural base rate for round-dollar charges is ~1.3% (2–7 rows per merchant, all small: `$9.00`, `$25.00`, `$40.00`). Two merchants blow past it:

| merchant | rows | integer-valued | mean amount | reference mean |
|---|---|---|---|---|
| belltower | 440 | **440 (100%)** | 3871.26 | 42.04 |
| harborview | 240 | **38 (16%)** | 608.79 | *(absent)* |
| all others | ~470 ea | 2–7 (~1.3%) | 40–44 | 39–43 |

**Two distinct defects:**

1. **`belltower` — 100% corrupted.** Every one of its 440 rows is an integer. `T004003,belltower,web,4560.0` is $45.60, not $4,560. The whole merchant feed is emitting cents.

2. **`harborview` — ~16% corrupted, interleaved.** This is the nasty one. It's a **new merchant** (not present in `reference.csv` at all), and only *some* of its rows are in cents — `454.0`, `12671.0`, `871.0` sit right next to correct values like `20.63`, `8.2`, `51.69`. The bad rows are scattered evenly across the whole file (~16% in every 500-row bucket, indices 279→3904), so it isn't a time window or a bad batch — it looks like one of two upstream paths for that merchant is unconverted.

**Verification:** dividing those 478 rows by 100 collapses every merchant onto the reference distribution — belltower mean 38.71, harborview 40.89, against a reference range of 39.2–42.6. Overall mean goes 497.36 → 41.71 (reference: 41.08); max goes 20,625 → 678.79. Nothing else needed adjusting, which is strong evidence the 100× factor is the entire story.

**Why the column stats looked fine:** they probably weren't checked against the reference — current mean is 497 vs 41. But even a self-contained check passes: no nulls, no zeros, no negatives, valid floats throughout, and the median (33.96) barely moves because only 12% of rows are affected. Only mean/std/max flag it, and a heavy-tailed transaction column is *expected* to have a big max.

**Detection rule for the pipeline:** per-merchant rate of `amount % 1 == 0`. Alert above ~5%. That catches both cases here and any future feed that flips units.

---

Side note, unrelated to `amount`: `settled_days` is a string column with mixed formats — `"0"`/`"1"` and `"0 d"`/`"1 d"` (1,184 rows carry the `" d"` suffix), so it parses as text rather than numeric.
