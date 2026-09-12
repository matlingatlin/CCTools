**Verdict on today's batch: BLOCK = 3, WIDEN = 2.** Two separate counts — the batch is held on three rows, and two rows are contract amendments already written in.

**BLOCK — contradicts a commitment**
- **`amount`, merchant=belltower** — cents in a USD-declared column. All 440 values integer-valued (vs 0.004–0.016 elsewhere), median 32.75 → 2726.50. Rival reading "belltower moved upmarket" is beaten by: ÷100 reproduces the reference at p05/p25/p50/p75/p90/p95 and every value is exactly 2dp after the divide.
- **`settled_days`** — two encodings in one batch: 70.4% bare integers, 29.6% `"0 d"`. Suffix rate flat across every segment (0.264–0.375), so producer-side serialisation, not segment behaviour.
- **`customer_age`, channel=android** — 1.61% → 83.12% null while ios (0.0183), web (0.0180) and phone (0.0139) sit inside their own reference spread. Field went effectively absent for one client.

**WIDEN — extends a set never declared closed**
- New merchant `harborview` (240 rows) → added to the allowed set; its amount bound is **withheld, not widened** (no post-onboarding data).
- New status `chargeback` (90 rows) → added; no rate bound set on one observation.
- Channel mix (web .517→.417, ios .261→.369) contradicts nothing and extends nothing — its band is demoted to observe-only, counted in neither tally.

**Where I did not confirm the narrow story:** the belltower signature at the bound used (intfrac ≤ 0.50) separates belltower from all eight other merchants. It does **not** clear harborview — harborview sits at 0.158, its 38 integer rows are the *only* large values in the segment (non-integer rows top out at 366.80), and ÷100 puts them squarely inside the population. New-merchant-bills-round-dollars and partial-cents-leak are both still open; that is a producer question, not another statistic. Looser signatures ("p90 > 500", "above the 0.016 reference ceiling") capture both merchants and separate nothing.

**On numbers:** no harm bound exists here — no control total, bill or labelled outcome ships with this feed — so `BLOCK` means *hold and ask the producer*, not *harm proven*. All seven distributional checks are observe-only. Only two gating checks carry a number, both derived and shown: A-05's cut sits in the gap between an observed ceiling of 0.016 and the mechanical 1.0 a ×100 scale change forces; A-06's 0.10 is an absurdity floor at 3.4× the highest per-channel rate the reference ever showed, with the harm question marked `NOT DERIVED — owner: whoever consumes customer_age`. `MIN_SEGMENT_N = 100` is also `NOT DERIVED`, and its cost is that channel=phone (n=72) is untested, not passing.

**Held-out check bit:** deriving on reference rows 1–2000 and measuring on 2001–4000, **five of eight profile-derived bands failed** — `amount <= 564.33` covered 0.9990, `customer_age NOT NULL` 0.9820, and the median-amount / web-share / ios-share bands held in 1, 2 and 2 of 4 blocks. All demoted. Every exact constraint covered 1.0000, which is why the gating checks are the exact ones.

**NOT BACKTESTED — history: one prior batch.** Firings per period can't be counted, and capacity is underived. The contract does run clean on its own source batch (BLOCK 0, WIDEN 0), which shows it doesn't fire on the data it came from and nothing more.

Files in the run directory: `contract.md` (ledger, split, provenance, held-out coverage, producer questions), `assert_batch.py` (boundary assertions, exit 1 iff any BLOCK), `assertion_results.csv` / `assertion_results_reference.csv` (31 machine-readable rows each: name, segment, observed, expected, kind, side, row count, batch id).
