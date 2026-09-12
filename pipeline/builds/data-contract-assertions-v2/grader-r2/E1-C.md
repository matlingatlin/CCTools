The contract passes its own source file and rejects today's batch. Files: `contract.json`, `validate.py`.

## The contract (derived from yesterday, 4000 rows)

8 columns, fixed order. The parts that carry weight:

| Field | Rule |
|---|---|
| `txn_id` | `^T[0-9]{6}$`, unique, no collision across batches |
| `merchant` | closed domain, 8 values, each 12–13% |
| `channel` | closed domain: web/ios/android/phone (51.7/26.1/20.2/2.1%) |
| `amount` | USD **dollars**, 1.56–564.33, mean 41.08, ≤2dp, only ~1% whole numbers |
| `currency` | `USD` only |
| `status` | closed domain: settled/pending/refunded (86.2/10.9/2.9%) |
| `customer_age` | int 18–78, **1.4% null, and 1.2–1.6% in every channel** |
| `settled_days` | bare int 0–3, no unit suffix |

Two rules are cross-field rather than per-column, because the per-column bounds alone miss the worst failure: **no merchant may exceed 5% whole-number amounts**, and **batch total within 3× of reference**.

## What today's batch does to it: 9 blocking violations

**1. `amount` — a unit change, not a spike.** All 440 belltower rows are whole numbers (median 2729, max 20625); the reference has ~1% whole numbers and a belltower median of 32.75. Belltower switched to **cents**. Dividing those by 100 recovers min 2.39 / median 27.29 / max 206.25 — the reference shape. Confirmation: correcting belltower *and* harborview's 38 whole-number rows brings the batch total to 166,832.91 against a reference 164,315.82 — **within 1.5%**. The unit is the entire discrepancy; there is no real revenue growth here.

Belltower alone is 85.6% of today's stated revenue on 11% of rows. Any downstream sum, average, or threshold is wrong by ~12×.

**2. `customer_age` — one broken client, not general decay.** Null rate 1.4% → 17.8%. But it isn't spread: web 1.8%, ios 1.8%, phone 1.4%, **android 83.1%**. The Android integration stopped sending the field; the other three are unchanged. A batch-level null threshold alone would read this as mild degradation, which is why the contract bounds nulls per channel.

**3. `settled_days` — type break.** 1184 rows (29.6%) are now `"0 d"`, `"1 d"`, `"2 d"`, `"3 d"` instead of integers. Evenly spread across every channel, merchant, and status (~29–30% each), so it's a serializer emitting two formats non-deterministically, not a cohort. Strict integer parsers fail; lenient ones silently coerce to null.

**4. Two new enum members.** `merchant` gains `harborview` (240 rows, 6.0%) and `status` gains `chargeback` (90 rows, 2.2%). Both are plausibly legitimate business events, but they are new categories — any code with an exhaustive branch on status, or a per-merchant join, hits an unhandled case.

## Warnings, not blocks

- **Channel mix moved**: web 51.7%→41.6%, ios 26.1%→36.9% (±10pp). Large, but this is real-world drift, not malformed data.
- **`harborview` is mixed-unit** — the nastier one. 202 rows in dollars, 38 in cents, *within the same merchant*. Belltower is uniformly broken and therefore mechanically fixable; harborview needs a rule (its whole-number rows run 181–12717, and a genuine $181 charge is plausible), so a blanket "divide integers by 100" would corrupt real values.

## Recommendation

Reject the batch. Items 1 and 3 corrupt values silently rather than failing loudly, which makes them the urgent ones — a downstream job that ingests this will produce confident, wrong numbers. Items 2 and 4 need a vendor conversation: confirm `harborview`/`chargeback` are intentional additions and expand the domains, rather than patching them through.

Two caveats on what I built: the `amount` max of 850 and the categorical share tolerances are judgment calls extrapolated from a single day, so they'll need widening once you've seen a few clean batches — a one-day sample can't distinguish a true bound from the observed maximum. And the cents diagnosis is inference from distribution shape and total reconciliation, strong as that is, not from vendor documentation; worth confirming before you write a correction factor into a pipeline.
