**Today's batch is rejected: 7 HARD breaches, 3 SOFT.** Nothing lands.

## The one that matters

`belltower` switched from dollars to **cents**. All 440 of its rows are whole numbers (baseline: 5 of 479), p50 ratio 83x, p90 96.8x. Every type checks out — integer stayed numeric, no nulls, schema identical. It inflates the feed total from 164k to 1.99M.

`harborview` — a *new* merchant — has the same bug on **15.8% of its rows**. This one is nastier: its median is 35.00, perfectly normal. A p50-ratio check alone misses it entirely. Only the p90 check and the whole-number-share check see it. That's the case for running both quantiles rather than just the median.

## Everything else

| Breach | Triage |
| --- | --- |
| `settled_days` now `"0 d"`/`"1 d"` on 29.6% of rows | Broken feed — uniform across every segment, so it's serialization, not business |
| `customer_age` null 1.6% → **83.1% on android alone** | Broken feed — one client stopped sending it |
| `status` gains `chargeback` (2.2%) | Legitimate — needs an amendment |
| `merchant` gains `harborview` (6.0%) | Legitimate — but its rows are unit-corrupt |

The android null finding only names itself when the check is **per channel**. Pooled, it reads as 17.8% — a vague quality dip you'd shrug at. Segmented, it points straight at the client.

## Two things constrain how much you should trust this

**I had one reference batch.** So per the method: structural checks are binding, every distributional bound is marked provisional/observe-only, and I haven't backtested the alert budget because there's no history to backtest against. The `channel` mix shift (ios +10.8pp) is genuinely untriageable for this reason — I can't tell a Tuesday from a routing change with n=1.

**The reference itself looks synthetic.** Exactly 4000 rows, `txn_id` perfectly contiguous T000000–T003999 with zero gaps. Real daily volume doesn't land on a round number and real transaction ids have holes. That's the export-limit signature, so I couldn't derive a row-count band at all — the one number you'd most want is the one I trust least.

The unit tripwires (U1–U4) are binding *despite* that, because they trip only on power-of-ten shifts that no legitimate variation produces — they need no calibrated band. That's what saves the exercise from the one-day snapshot.

Two gaps worth closing with the vendor: there's **no timestamp column anywhere**, so staleness is undetectable — a replayed file is only caught by the id check. And no control total, so sum reconciliation can't exist. I've listed both as unimplementable rather than quietly skipping them.

I left the two legitimate changes as *proposed, unapplied* amendments — no approver, no effective date. Both arrived in the same file as the unit corruption, which is precisely when waving them through feels most reasonable.
