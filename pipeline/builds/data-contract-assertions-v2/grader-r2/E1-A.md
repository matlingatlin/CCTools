Contract passes cleanly on the snapshot it came from (21/21, no false positives) and rejects today's batch. Files: `CONTRACT.md`, `assert_contract.py`.

## The contract

**Consumer assumption (step 1) — please confirm.** No consumer was named. The columns are settlement data, so I wrote it for the money path: *consumer = revenue/payout reporting; a bad batch costs mis-stated revenue, externally visible* ⇒ **fail loud**. If it actually feeds a dashboard or ML features, the SOFT tier should quarantine instead; the HARD tier fails loud either way.

**Snapshot caveat (step 2) — this limits everything.** `reference.csv` is *one* batch. No period-over-period variation is observable, so **no honest distributional band exists**. Per the method's rule, structural checks are binding and every SOFT bound is marked **provisional/observe-only** — it tickets, it never pages. Also found, and worth raising with the producer before trusting any of it:

- `currency` is single-valued `USD` — it carries no information, and critically it did **not** move when belltower's *scale* changed. The unit is not in the data.
- Exactly **4000 rows** both days. Cannot distinguish "vendor sends 4000/day" from "export capped at 4000."
- **No date/timestamp column at all** — event-time freshness is unassertable. I substituted H10 (`min(txn_id) > last batch's max`) for replay detection.
- No upstream control total to reconcile against, so S4's sum check is the weak baseline-relative form.

10 HARD invariants (PK, no-blanks, amount > 0, declared units, closed `status` enum, replay), 10 SOFT provisional bands.

## What today's batch does to it: **REJECTED — 3 HARD failures, 5 SOFT breaches**

| # | Finding | Caught by |
|---|---|---|
| 1 | **`belltower` switched USD → cents.** All 440/440 rows, p50 32.75 → 2,726.50 (**83x**), p90 **97x**. Divide by 100 and it lands back on baseline (p90 76.58 vs 79.14). | **S2e/S3e** (power-of-ten escalation) + S5 |
| 2 | **`settled_days` gained a `" d"` suffix** on 1,184 rows (29.6%), spread evenly across all merchants — a producer formatting change. Breaks every downstream `int()`. | H8 |
| 3 | **New `status` value `chargeback`** (90 rows, 2.25%) — an unmapped revenue treatment. | H9 |
| 4 | **`harborview` is a new merchant with *mixed* units** — 38/240 rows (15.8%) are whole numbers vs a 0.95% baseline; those 33 ≥1000 divided by 100 sit right on the family median. | S5 |
| 5 | **`customer_age` nulls 1.4% → 17.8%**, concentrated at **83% of the android channel** (was 1.6%). | S6 |
| 6 | Channel mix shifted 10pp: web 51.7%→41.7%, ios 26.1%→36.9%. Possibly the same release as #5. | S7 |

**The point the method is making, live in this batch:** `amount` passed *every* type and format check, including H5 (≤2 decimal places — `4560.0` is fine) and H6 (`currency == USD` — unchanged). Nothing structural noticed that a merchant's numbers were 100x wrong. Only the p50/p90 **ratio** check caught it. Likewise, the status-mix band (S8) passed at 2.25pp while the closed-enum invariant caught `chargeback`; the merchant-volume band (S9) passed at 6% while the cents-rate check caught harborview.

## Triage before you touch a threshold (step 8)

- **Broken feed — fix at the producer, do not widen:** #1 belltower cents, #2 the `" d"` suffix, #4 harborview mixed units. #4 is the nastiest: it's *within* one new merchant, so no per-merchant median would ever have flagged it.
- **Probably legitimate — needs an amendment with reason, approver, effective date:** #3 `chargeback` (make the revenue-treatment decision first, then amend the H9 set), and #5/#6 if the android null spike is a consent/tracking change rather than a broken field mapping. New bounds must come from batches *after* the change, not from this one.

Two things I could not do and you should know are missing: no backtest of the alert budget (one historical batch can't be backtested — retune once ~8 batches exist), and no landing-time SLA check because no SLA was stated.
