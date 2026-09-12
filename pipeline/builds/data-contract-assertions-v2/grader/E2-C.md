`assert_batch.py` — 37 assertions in four tiers, thresholds measured from the 4,000-row reference profile. Exit 1 on any FAIL, WARNs are advisory.

**The profile I derived them from:** 8 columns, no nulls anywhere except `customer_age` (1.40%); `currency` constant USD; closed enums on channel (4) / status (3) / settled_days ({0,1,2,3}); merchant an 8-value set at ~12.5% each; `amount` a positive right-skewed decimal, median 29.84, p99 208, max 564.33; `txn_id` a dense contiguous `T\d{6}` sequence.

| Tier | Covers |
|---|---|
| **A. Structure** | exact header + order, 8 fields per row, non-empty, batch size band (warn), no untrimmed whitespace, no blanks outside `customer_age` |
| **B. Field validity** | `txn_id` format + in-batch uniqueness + contiguity + continues from previous batch; closed enums for currency/channel/status; unknown merchant (warn, escalating to fail above 5% of the batch); `amount` a bare positive ≤2dp decimal; `customer_age` blank-or-int in 18–100; `settled_days` int in {0,1,2,3} |
| **C. Distribution** | age null rate, age range, per-category mix for channel/status/settled_days/merchant, `amount` mean/median/p95/p99, tail share >250, soft max 600 (warn) and hard ceiling 2500 (fail) |
| **D. Cross-field** | per-merchant refund rate, per-channel amount median — both catch a single bad source that the batch-level aggregate hides |

Two design choices worth your sign-off:

- **Bands scale with batch size.** Mix and null-rate checks use 4σ of binomial noise plus a 0.5pp floor, computed from the actual row count; the `amount` quantile bands are 2,000-resample bootstrap intervals at n=4000, widened by √(4000/n). So a 500-row batch doesn't get flagged for sampling noise. Fixed-percent tolerances would.
- **Severity split.** Enum violations, malformed values, null-rate and amount-shape drift fail the batch. Merchant mix, age range, tail share and the per-source checks only warn — those move for legitimate business reasons.

Two things I deliberately did **not** assert: there's no `pending ⇒ settled_days == 0` rule, because the reference itself has 153 pending and 42 refunded rows with non-zero settled_days — asserting it would fire on your own baseline. And cross-batch `txn_id` uniqueness needs state the script doesn't keep; `--prev-max-id` is the cheap stand-in, and it catches both gaps and replays.

Verified both directions: clean on `reference.csv` (0 fail, 0 warn — no assertion self-fires on its own baseline), and on `current.csv` it returns 11 fails / 2 warns, catching `'1 d'` unit suffixes in settled_days (1,184 rows), a new `chargeback` status (90), an unknown `harborview` merchant (6%), the age null rate at 17.8% vs 1.4%, an iOS-ward channel shift, and amounts up to 8,206 against a profile max of 564.
