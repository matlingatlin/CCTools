Found it. **The `amount` column is in cents for some rows and dollars for the rest** — a mixed-unit column, which is why every column-level statistic passes.

## The finding

| Segment | Rows | Unit | Evidence |
|---|---|---|---|
| `belltower` | 440 (100%) | **cents** | p50 ratio vs reference = **83x**, p90 = **97x**; 100% integer-valued (0 rows with a fractional part) |
| `harborview` | 38 of 240 (16%) | **cents** | those rows are 100% integer-valued vs a ~1% natural base rate; dividing by 100 lands them exactly on harborview's own dollar distribution |
| everything else | 3,522 | dollars | p50 ratios 0.90–1.09, normal |

Dividing those rows by 100 reconciles the file:

```
sum as-is      1,989,449.64
sum repaired     166,832.91
reference        164,315.82   ← 1.5% gap, normal batch variation
repaired p50=29.63 p90=84.45  (reference p50=29.84 p90=81.23)
```

The corruption is **$1.82M of phantom volume, a 11.9x overstatement of total processed amount.**

## Why the column-level stats looked fine

`belltower` is only 11% of rows, so the pooled view is dominated by the healthy 89%:

```
           dtype     nulls   min    p25     p50     mean
reference  float64   0       1.56   17.54   29.84   41.08
current    float64   0       1.97   18.80   33.96   497.36
                                            ^^^^^   ^^^^^^
                                            1.14x   12.1x
```

Type, null rate, min, p25 and **p50 all pass any reasonable band** — the median moves 14%, well inside normal drift. Only the mean blows up, and a mean check is rarely written because it's noisy by nature. The signal lives in the tail and in the per-segment split, not in the column.

Two checks would have caught it on the first bad batch:

1. **Per-segment p50/p90 ratio vs baseline, flagged when the ratio lands near a power of ten.** Pooled it's 1.14x; grouped by merchant it's 83x on one merchant. Segmenting is what makes it visible.
2. **Digit-length distribution**, which needs no baseline grouping at all:
   ```
   reference  {1: 320, 2: 3434, 3: 246}
   current    {1: 293, 2: 2976, 3: 302, 4: 398, 5: 31}
                                        ^^^^^^^^^^^^^ 429 rows in magnitude buckets that never existed
   ```

`harborview` is the nastier half: it's a **new merchant** with no baseline to ratio against, and only 16% of its rows are affected — scattered across every channel, status and settled_days value, so no dimension isolates them. Only the integer-valued fraction (15.8% vs ~1% expected) gives it away. That pattern reads like a partially-migrated integration sending cents on one code path.

## Other contract deltas in the same file

Not what you asked about, but they're in the same batch and would fire on a proper ingest gate:

- **New category values**: merchant `harborview` (240 rows) and status `chargeback` (90 rows), neither present in reference.
- **`settled_days` changed type**: reference is a clean integer set `{0,1,2,3}`; current mixes in string values `{"0 d","1 d","2 d","3 d"}`, so it parses as a string column now and any arithmetic on it silently breaks.
- **`customer_age` null rate jumped 1.4% → 17.8%** (56 → 713 nulls).
- File is CRLF-terminated.

`txn_id` is still unique (4000/4000), and currency is uniformly `USD` — so no key or currency-mixing problem.

The immediate fix for `amount` is to reject the batch rather than patch it: a `/100` repair applied to `belltower` is safe, but the `harborview` rows can only be identified heuristically (integer-valued), and any genuine whole-dollar harborview transaction would be wrongly divided. That needs a producer conversation, not a downstream correction.

Want me to write this up as a contract file (`HARD`/`SOFT` split, bounds derived from `reference.csv`, asserted at the ingest boundary)? Worth flagging in advance: `reference.csv` is a single unreconciled snapshot, so under the method the structural checks would be binding while the distributional bounds start observe-only until more periods accumulate.
