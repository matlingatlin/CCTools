Done. Four files in `contracts/`:

| File | Role |
| --- | --- |
| `payments_txn.contract.md` | The contract artifact — tier, owner, action, derivation per assertion |
| `assert_batch.py` | The gate: 33 assertions, machine-readable output, exit 1 on HARD |
| `derive_baseline.py` | Re-derives the baseline when the contract is amended |
| `payments_txn.baseline.json` | Generated profile (never hand-edited) |

**Validation:** clean on `reference.csv` (0 HARD, 0 SOFT), and on `current.csv` it caught 7 HARD + 2 SOFT — a dollars→cents switch on one merchant, two new enum values, and a 29.6% format corruption in `settled_days`.

Three things worth your attention:

**1. The obvious unit check would have missed the unit bug.** `belltower` switched dollars→cents, but it's 11% of rows, so the global median moved 29.84 → 33.96 — **1.14x, passes cleanly**. Only the *per-merchant* p50 caught it, at 83x. When a feed is a union of independent producers, an aggregate median dilutes any single producer's fault below the noise floor. I added a second, independent signal (`U3`: cents-encoded money is integer-valued — belltower is 100% whole numbers vs a ≤1.64% baseline), which also catches the case per-merchant p50 can't: `harborview` is brand-new and has no baseline to compare against, but flagged at 15.8%.

**2. `settled_days` is the check that only a counter catches.** 1,184 rows arrived as `"1 d"`, `"0 d"`. `int()` fails, but the parseable remainder is distributionally *perfect* — min 0, max 3, p50 0, identical to baseline. A `to_numeric(errors="coerce")` would NaN them silently and every distributional check would pass. The assertion is a strict-parse failure count, never a coercion.

**3. The snapshot isn't validated, so I couldn't make the distributional bounds binding.** One file, no reconciliation, and — the real blocker — **no timestamp column anywhere**. Freshness, staleness SLA, and like-with-like period comparison are structurally impossible here; a feed that silently stops updating is currently undetectable. So structural checks are binding and every `D*` bound ships PROVISIONAL (tickets, never pages) until real batch history accumulates. I also declined to encode two tempting bounds: `settled_days <= 3` (the hard stop at 3 with no tail looks like an upstream clamp — encoding it would cement a defect as correct) and `customer_age ∈ [18,78]` (HARD is the physical [0,120]; the observed range is SOFT).

Two things I need from you: **who consumes this feed** — I assumed settlement/finance and defaulted to fail-loud, but if it drives a dashboard or ML features that should be quarantine; and note the quarantine remedies named in §6 are **unbuilt** — no reject destination, replay path, or max-age owner exists, so until they do, every HARD breach is whole-batch fail-loud.
