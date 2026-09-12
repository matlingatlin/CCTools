Done. Three files in `run-317a875bf5/`: `contract.py` (constants + derivations), `assert_batch.py` (runnable, emits JSONL per assertion), `contract.md` (ledger, split, provenance).

## The split — 3 BLOCK, 4 WIDEN (two counts, never summed)

**BLOCK** — contradicts a producer commitment:
- **L1** `belltower` amounts are 91x the pooled median, 440/440 whole-valued, min 239 — cents where `currency=USD` declares dollars.
- **L2** `settled_days` carries a ` d` suffix on 1184/4000 rows — type break, uniform across every segment.
- **L3** `customer_age` null-rate 0.0161 → **0.8312 in `channel=android`** only.

**WIDEN** — extends a set never committed closed: new merchant `harborview` (240 rows), new status `chargeback` (90 rows), harborview's wider amount range, and the ios/web mix shift. **On their own these ratify the batch, not refuse it** — the suite exits 0 on a widen-only batch. `harborview` is not what stops this one.

## The two BLOCK signatures, and what they don't separate

The obvious belltower signatures — share of rows >200, share whole-valued — **also flag harborview** (0.163 / 0.158 vs 0.004–0.016 for reference merchants). They were rejected for that; `share_whole_valued` is logged as corroborating-only, marked never-gating in code. What gates is median ratio: belltower **91.4**, harborview **1.17**, reference merchants 0.88–1.08.

For L3 the same test cuts the other way: **by channel it separates cleanly** (android 0.831 vs 0.018/0.018/0.014); **by merchant it separates nothing** — all nine merchants sit at 0.142–0.200, harborview included, because every merchant carries android rows. The check runs on channel only, and no merchant-level claim is made.

Left open: harborview's 39 rows >200, of which 37 are whole-valued and whose /100 median (27.37) lands squarely in the reference range. That reads equally as a new partner's large tickets or a partial cents corruption inside the new merchant. The data does not decide it; it's filed WIDEN with the rival reading recorded and the bound observe-only.

## On thresholds

**No drift threshold is in this contract**, because no harm signal exists in the feed — no control total, no settlement file, no labelled outcome. The two gating numbers are separators between two discrete candidate states, not drift bands, and each carries its derivation: **10.5x** = geometric midpoint between dollars (1.0) and cents (100), given observed across-merchant spread of 1.098 — 9.6x margin each side; **0.169** = `sqrt(0.0285 × 1.0)` between the reference per-channel ceiling and total absence — 5.9x each side. Gating them is a **named deviation** from the method's three kinds, flagged so you can reject it.

Everything distributional is observe-only. Capacity bound: `NOT DERIVED` — needs cadence and a named owner. Row count, freshness SLA (no timestamp column exists), FK-to-merchant-master, cross-batch replay: all recorded as `NOT DERIVED`/`SKIP` with the dependency named, not filled with a plausible number.

Held-out check (derive on ref rows 0–1999, measure on 2000–3999) put `amount <= max` at **0.9990** — it would have failed 2 of 2000 clean rows, so it is non-gating by design. `NOT BACKTESTED — history: one reference batch.`
