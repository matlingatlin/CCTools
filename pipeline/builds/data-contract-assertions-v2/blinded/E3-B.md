## Short answer

There isn't a threshold that helps here, because `current.csv` isn't drifting — **it's already broken, in five ways.** Tuning a band until it passes would encode a 6.6x overstatement of transaction value as normal.

And the specific threshold you'd reach for first doesn't work on this data:

| Check | Value | Verdict |
|---|---|---|
| Table-level `amount` p50 ratio | **1.14x** | passes any sane band |
| Row count | 4000 vs 4000 | identical |
| Schema / types / nullability | unchanged | passes |

Every conventional drift check is green while 85% of the stated total is wrong by 100x.

## What's actually wrong

**`belltower` is reporting cents as dollars.** All 440 rows are whole numbers, p50 is 2729 vs 32.75 baseline (**83x**); divide by 100 and it lands back in band. It's 85.6% of the file's stated total on its own.

**`harborview` has the same bug on 14.6% of its rows** — 35 of 240, the other 205 are fine. This one is the reason to care about method here: harborview's median is **35.16, perfectly normal**. A per-merchant p50-ratio check passes it while 57% of its value is inflated 100x. Median-based detection assumes the whole segment moved together; partial contamination is invisible to it. Only a **sum** check or a **whole-number-fraction** check catches it.

Plus: `settled_days` gained a ` d` suffix on 29.6% of rows (producer-wide format change), `customer_age` is 83% null on android vs 1.6% baseline (SDK-side, other channels fine), and there's a new merchant and a new `chargeback` status.

Stated total **1,989,449.64** → corrected **303,128.19**.

## The threshold to actually use

**Whole-number fraction of `amount`, per merchant, ≤5% — HARD, fails the batch.**

Reference max per merchant is 1.64%; belltower is 100%, harborview 15.8%. This works because real dollar-and-cent amounts are whole ~1% of the time and integer-cents amounts are whole 100% of the time. That gap is ~60 sigma, needs no history, and doesn't drift seasonally — so unlike a distributional band, you can enable it today. Back it with a per-merchant **sum** check (±3x), which is what catches partial contamination.

## Two things that block honest bounds

**You have one baseline period.** Natural variation is unmeasured, so any distributional threshold I gave you would be a guess with a decimal point on it. I've marked those observe-only in the contract with provisional values, to be re-derived after ~6 clean periods.

**Both files are exactly 4000 rows.** A round number on both sides is the signature of a pagination or export limit, not a real volume — so don't write a row-count check until that's explained. It also means neither file may be a complete period, which undermines the sum bounds too.

One thing I need from you: **who consumes this?** I defaulted to fail-loud because `amount` looks financial, but if it feeds a dashboard rather than billing, the soft tier should quarantine instead — stale data would hurt more than slightly-off data. That's the one call in the contract I couldn't make for you.
