Done — a runnable suite in `run-0f506b0833/`:

```bash
python3 build_profile.py reference.csv profile.json   # once, + on intentional changes
python3 assertions.py profile.json batch.csv --quiet  # every batch; exit 1 blocks
```

`profile.json` is the contract derived from the reference; `assertions.py` holds no feed-specific facts, so retuning is a reviewable diff of the profile rather than an edit to the checks.

**Two tiers:** FAIL (exit 1 — the data isn't what the contract says, something downstream will silently compute a wrong number) and WARN (differently shaped, possibly a real business change — alert, don't stop the pipeline).

**The checks:** structure (schema/order, non-empty, id format + uniqueness, exact-duplicate rows); types and bounds (numeric parse, integrality, ≤2dp, positive amounts, `customer_age` ∈ [18,78], `settled_days` ∈ [0,3]); categorical domains (unseen values, plus case/whitespace variants as a separate cheaper bug); composition (per-category share, null rates, null concentration by channel); and numeric distribution (median, p99, whole-number share, per-merchant median, PSI).

Two design calls worth flagging:

- **`amount` gets no upper bound.** Its reference max of 564.33 is a sample max on a heavy tail, not a cap, so a hard ceiling would fire on legitimate large transactions. It's policed by scale checks instead. `customer_age` and `settled_days` do get hard bounds — they sit *exactly* on their limits across all 4000 rows, which reads as an enforced clamp rather than a sampling artifact.
- **Unseen categories FAIL rather than warn.** A new merchant is a legitimate event, but joins and revenue splits are keyed on these, so it should land deliberately via a profile update.

**Calibration** (this is the part that decides whether anyone keeps the suite switched on): split-half — profile built from a random 2000 reference rows, then 181 fresh batches at n=100…2000 drawn from the held-out half. **Zero false FAILs**; 9 WARN events total, all mix/null-rate at small n. Checks that can't be evaluated at a given batch size report SKIP rather than guessing, so rare values (`phone` ~2%, `refunded` ~3%) vanishing from a small batch doesn't fire.

I also ran it against the `current.csv` sitting next to your reference. It is **not** a clean batch — 9 FAILs, six distinct defects:

| Defect | Caught by |
|---|---|
| `settled_days` has a unit suffix — 1184 rows `"0 d"`, `"1 d"` | `B_settled_days_parses` |
| New merchant `harborview` (240 rows) | `C2_merchant_domain` |
| New status `chargeback` (90 rows) | `C2_status_domain` |
| `customer_age` nulls 1.4% → 17.8%, **83% of android rows** | `D2` + `D3` |
| `belltower` amounts ~83x inflated (cents), 429/440 rows | `E4` + `E2` + `E3` |
| Channel mix: ios 26% → 37% | `D1_channel_mix` |

The belltower one is the reason `E4` and `E3` exist. Overall median only moves 29.84 → 33.95 because just one partner is affected, so a median check alone passes it — the per-merchant medians and the whole-number share (0.9% → 12.8%) are what catch it, and `E4` names the partner.

One thing I'd want your input on: I treated the 17.8% age-null rate as a defect, but if the android SDK genuinely stopped collecting age, that's a product change and `D3` will fail every batch until the profile is refreshed. Worth confirming which it is before wiring this into CI.
