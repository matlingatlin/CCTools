## The contract

Both files are 4,000 rows, 8 columns, same header. From `reference.csv`:

| Column | Contract |
|---|---|
| `txn_id` | `^T\d{6}$`, unique, not null, disjoint across batches |
| `merchant` | closed set of 8, near-uniform (~12.5% each) |
| `channel` | closed set of 4 — web 52%, ios 26%, android 20%, phone 2% |
| `amount` | USD **dollars**, 2dp, 1.56–564.33, median 29.84, p99 210.64. Only 0.95% whole numbers |
| `currency` | `USD` only |
| `status` | `settled` 86.2% / `pending` 10.9% / `refunded` 2.9% |
| `customer_age` | int 18–78, nullable at **1.4%**, nulls spread evenly (≤1.6% in every channel) |
| `settled_days` | int in {0,1,2,3}, **bare digits, no unit** |

## What today's batch does to it

**11 violations, 4 drift warnings.** Four are real breaks; two are business change.

**Silent corruption — these produce wrong numbers, not errors:**

1. **`amount` unit flip on belltower.** All 440 belltower rows are in **cents**: median 2726.50, max 20625.00, and 100% are whole numbers written `4560.0`, `676.0`. Divide by 100 and it lands right back on the reference (median 27.27 vs 32.75, mean 38.71 vs 42.04). Also **38 harborview rows** are cents-encoded (35 of them >600). Restate just those 478 rows and the whole column reverts to contract: median 29.63 vs 29.84, mean 41.96 vs 41.08. Untouched, this inflates total volume by ~12x.

2. **`settled_days` type break.** 1,184 rows (29.6%) are `"0 d"`, `"1 d"`, `"2 d"`, `"3 d"` — the column no longer parses as int. Affects every merchant and channel at a uniform ~30%, so it's a formatter change, not a data change. Strip the suffix and the value distribution matches reference. The two `settled_days` drift warnings are just this artifact, not independent drift.

3. **`customer_age` collection failure on android.** Null rate 1.4% → **17.8%**, and it is not random: **83.1% of android rows are null** (655 of 788) vs ~1.8% on every other channel, essentially unchanged from reference. Something in the android path stopped sending age. Any age-based aggregate is now silently android-blind.

**New categories — likely legitimate, but they break a closed set:**

4. **`merchant`: new value `harborview`**, 240 rows (6.0%). Its channel/status mix matches the rest of the file, so it looks like a genuine onboarding — but 38 of its rows carry the cents bug.
5. **`status`: new value `chargeback`**, 90 rows (2.25%), spread across all merchants. Reads as a real new lifecycle state. Note it's drawn from `settled`, which fell 86.2% → 83.8%.

**Drift, no violation:**

6. **`channel` mix shifted** — web 51.7% → 41.7%, ios 26.1% → 36.9% (PSI 0.06, mild). Present in harborview and non-harborview rows alike, so it isn't the new merchant pulling the mix.

**Holding fine:** row count, header and column order, `txn_id` format/uniqueness (T004000–T007999, zero overlap with yesterday), `currency`, `customer_age` range, no malformed rows, non-harborview merchant mix (PSI 0.003).

The ordering I'd suggest: #1 and #3 corrupt numbers without failing anything downstream, so they're the urgent ones — #2 will at least throw on ingest. #4 and #5 are a conversation with the vendor about the closed sets, not a defect.
