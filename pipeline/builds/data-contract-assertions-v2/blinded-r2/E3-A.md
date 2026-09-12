Done. Here's the answer.

## Don't set a threshold yet — `current.csv` is already broken

You can't derive a drift band from a batch that's the anomaly. Four independent breaks are in that file right now:

**1. `amount` for `belltower` is in cents, not dollars.** All 440 belltower rows are whole numbers (the rest of the feed is 0.9% whole); p50 is 83x the baseline, p90 is 97x. `harborview` has the same bug on 38 of 240 rows. The proof: divide *only* the whole-number rows by 100 and the feed total goes from $1,989,450 to **$165,627 against the baseline's $164,316** — a 0.8% gap, i.e. normal. Every one of those rows type-checks perfectly.

**2. `settled_days` gained a unit suffix** — `"1 d"` instead of `1`, on 1,184 rows (29.6%). Still a valid string; breaks any `int()` cast.

**3. `status` gained `chargeback`** (90 rows, 2.25%) — new category, absent from baseline.

**4. `customer_age` null rate went 1.4% → 17.8%**, uniformly across all merchants, so it's a producer-side change, not merchant-specific.

## Why a single global threshold would have caught none of this

Pooled `amount` p50 ratio is **1.138**. Any sane global band passes it. The corruption is confined to one merchant out of nine, and pooling averages it into invisibility. **Thresholds have to be per-merchant, compared like-with-like.** That's the whole finding.

## The thresholds

Derived from the 7 merchants that are clean, whose observed period-over-period variation was p50 ratio **0.90–1.09** and p90 ratio **0.99–1.15**:

| Check | Bound | Tier |
|---|---|---|
| whole-number share of `amount`, per merchant | > 5% | **HARD** |
| `amount` p50 ratio vs same merchant | outside 0.75–1.33 | SOFT |
| `amount` p90 ratio vs same merchant | outside 0.70–1.43 | SOFT |
| ratio ≥ 50x or ≤ 0.02x | escalates to HARD — unit change, not drift | HARD |
| `customer_age` null rate | > 4% | SOFT |

The cheapest detector is the first one, not the quantile ratio: whole-number share is near-binary (0.4–1.6% healthy vs 100% broken), so it needs no tuning and no history.

## Three things that block making these binding

- **Both files are exactly 4000 rows.** That's an export or pagination cap, not a real batch size — so **row count is unusable as a drift signal here**, and the feed may already be truncating silently. Worth asking the producer about.
- **There is no timestamp column at all.** Freshness, staleness, and duplicate-batch detection are impossible to assert today. That's the biggest gap.
- **One reference period only.** No seasonality is observable, so every SOFT bound above is provisional/observe-only until ~6 periods accumulate. I deliberately left `channel` mix (web −10.1pp, ios +10.8pp) **unalerted** — with one period I can't distinguish drift from a real app-install trend, and a bound tight enough to catch it would be a round number pretending to be evidence.

Two files in `run-cd42511f2d/`: `CONTRACT.md` (11 HARD invariants, 8 SOFT bounds, owner and action per assertion) and `check_contract.py` (runnable, reads only, emits JSON per assertion, exits non-zero on HARD). Control run against the baseline fires nothing except the replay check — which is correct, since re-feeding an identical file *is* a replay.

One judgment call for you: the contract defaults to **fail-loud** because this data is money-shaped. If the consumer is a dashboard or a model rather than billing, quarantine is the better choice — §1 of the contract is left blank for you to fill in, and it's the line that decides it.
