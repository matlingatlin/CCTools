Three files, plus the run output. `current.csv` was sitting next to the reference, so I profiled it as the arriving batch — that's what makes the assertions concrete rather than a schema sketch.

## What ships

**24 assertions in `contract.yml`**, in three tiers that are kept visibly apart:

- **A01–A14 exact/structural** — presence, uniqueness, `txn_id` format, `currency` as a *declared unit*, `amount` parses positive ≤2dp, `settled_days` is a bare integer. No bound to derive, nothing to backtest, so these gate.
- **B01–B03 open sets** — merchant/status/channel. A new value here is an **amendment**, not a failure.
- **D01–D07 derived distributional** — every one ships `gating: false`.

## The split on this batch: BLOCK 4 · WIDEN 4

**BLOCK** — belltower's `amount` scale change; android's `customer_age` null collapse 1.6%→83.1%; `settled_days` gaining a ` d` suffix on 1,184 rows; plus one unresolved row (below).

**WIDEN** — new merchant `harborview` (240 rows); new status `chargeback` (90 rows); channel mix shift; harborview's bands having no prior. **A batch carrying only these would be ratified, not refused.**

Only 1 of the 4 BLOCK rows actually gates: `settled_days`. The other three are held observe-only because there's one prior batch, so no firing count exists — `NOT BACKTESTED` is written into the contract. The *assignment* stands either way; gating is about automating the refusal.

## Two things worth arguing with

**harborview is not settled, and I didn't settle it.** Its median is $35 and its small rows look normal, but all 35 of its rows ≥$500 are whole-dollar — belltower's exact signature. Reference large amounts aren't rounder than small ones (2.5% vs 0.9% whole-dollar), so "big tickets are round" isn't a convention of this feed. But harborview is a *new partner* with no prior, and a new partner is entitled to its own invoicing convention. Both readings are open; resolving it needs producer confirmation or two more batches. If someone asks "so it's just belltower?" — no, and the ledger says why.

**Every bound here is a noise bound.** They license "this batch is unusual" and nothing about cost. The feed has no control total, no settlement file, no labelled outcome, so no harm bound is derivable — and no source in `threshold-evidence.md` maps drift magnitude to downstream cost. The bands come from splitting the reference in half: `amount` p10 ratio 1.5× (largest observed split-half move was 1.30×), null rate 5% (largest cell at n≥200 was 1.77%). That's a *within-batch* spread standing in for a *between-batch* one, so it's a lower bound that will over-fire. Two numbers are flagged `NOT DERIVED` with owners: `customer_age` range [13,120] is a business rule, not a profile result; the row-count band and the SLA don't exist at all — the feed has no timestamp column.

The `amount` min/max constraint a profiler hands you failed its own holdout (0.9992) and is kept in the contract as an explicitly rejected candidate so nobody re-proposes it.

Highest-value change available, worth more than every band above: get the acquirer's per-merchant daily settlement total. That turns the amount checks into harm-kind gates and retires D02/D03.
