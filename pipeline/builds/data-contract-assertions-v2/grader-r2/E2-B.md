Two files in `contracts/`: the contract of record (YAML) and the boundary gate that runs it. 14 HARD / 8 SOFT / 2 observe-only / 1 blocked.

**Three things about the snapshot you should know before trusting any bound.**

Both files are *exactly* 4000 rows with contiguous ids (T000000–T003999, T004000–T007999). That's an export cap, not a batch size — so I did not derive a row-count band, which means **a silently truncated feed is currently undetectable**. Second, there is **no timestamp column of any kind**: no freshness check is possible, and no like-with-like comparison, so every band is pooled. Third, one period, no reconciliation source — so per the method's rule, structural checks are binding and every distributional bound is marked provisional.

**The unit trap here breaks the method's own headline check.** Whole-feed `amount` p50 ratio is 1.14 — the p50-ratio check passes clean. The conversion is per-merchant: belltower is 100% cents-encoded, harborview 16%, diluted to invisibility across nine merchants. Two corrections went into the contract:

- Run ratio checks **per segment**, not just per column.
- The sharper detector is **zero-fraction share**: real dollar amounts carry cents ~99% of the time (per-merchant baseline 0.38–1.64%), cents-encoded integers are 100%. belltower reads 1.04% → 100.00%. Unlike a quantile, it's independent of volume mix. And the observed ratio was 83x, not 100x — a tight "near a power of ten" test would have missed it, so H14 bounds on a wide `[0.125, 8]` band instead.

**Backtest found a bug in my first draft.** H15 (sum reconciliation) as originally written was HARD on the *raw* sum — it fired 3,258 times across 800 legitimate 500-row pseudo-batches, because sums scale with row count and any batch smaller than baseline breaches on every merchant at once. Normalising fixes it, but then it's just the mean, which H14 already covers, so I demoted it to observe-only with an explicit upgrade path. A rare-category share bug (`phone` at n=200) cost 45 more. After both fixes: **0 HARD and 2 SOFT across 3,401 legitimate batches**. Caveat stated in the file — resampling one snapshot measures sampling noise only, so the real false-positive rate is higher than 0.06% and still unknown.

On `current.csv` the gate fails loud with 8 HARD breaches: cents conversion (belltower + harborview), `settled_days` arriving as `"0 d"` in 29.6% of rows, and a new `chargeback` status. Plus 5 SOFT tickets — `customer_age` nulls 1.4% → 17.8%, which the per-channel split localises immediately to android at 83.1% (broken collector, not a data change), and new merchant `harborview`, which is routine onboarding and correctly a ticket rather than a page.

**One thing I had to assume.** You didn't say who consumes this. The column shape is a payments ledger, so I assumed settlement/finance and set routing to fail-loud on HARD. That assumption is written at the top of the contract with an `ACTION_REQUIRED` — if the real consumer is a dashboard or feature store, flip it to quarantine (the block is defined but needs a drain owner) and the bands should loosen. The assertions themselves don't change; only the routing does.
