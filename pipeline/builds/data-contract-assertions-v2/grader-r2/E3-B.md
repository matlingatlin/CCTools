## A drift threshold is the wrong instrument for this feed

I profiled `current.csv` against `reference.csv` (4000 rows each). There are 5 real differences. **None of them is caught by a drift band**, and a feed-level drift check would have missed the worst one outright: the 100× unit change on `belltower` moves the feed-level median only 29.84 → 33.96 (1.14×), because it's confined to 11% of rows.

**The split — 3 BLOCK, 2 WIDEN** (counts kept separate; the batch is not quarantined whole):

| | Difference | Evidence |
|---|---|---|
| **BLOCK** | `settled_days` mixed encoding | 1184/4000 rows are `"1 d"` — breaks any numeric cast |
| **BLOCK** | `belltower` amount → cents | whole-dollar share 1.0%→100%, median ratio 83.25× |
| **BLOCK** | `customer_age` null collapse | 1.40%→17.82%, uniform across all 9 merchants |
| **WIDEN** | new merchant `harborview` | 240 rows → added to the known set |
| **WIDEN** | new status `chargeback` | 90 rows, all merchants → added to the known set |

Two of the three blockers are exact assertions with no bound to tune. Only one has a number.

**The one number, and its honest limit.** `customer_age` null rate ≤ **0.0213** — the max of 10,000 bootstrap resamples (n=4000) of the reference's own null indicator. That is *within-batch* sampling variation. You have one reference batch, so between-batch spread is unmeasured and is certainly wider. It blocks this batch because 17.82% is 8.4× the entire resampling range — a gap no plausible band closes — but it is not trustworthy at the margin. Re-derive from ≥5 landed batches before treating a 3% reading as a failure.

**Two numbers I did not derive, flagged as such:** the unit-change `median_ratio ≥ 10` gate (`NOT DERIVED — owner: feed owner`; nothing in the data distinguishes anything between 1× and 100×), and the capacity bound (needs the on-call's actual read volume). The channel mix shift (web .52→.42, ios .26→.37) is logged **observe-only** — one reference batch gives no spread to derive a band from.

**Where I can't confirm the narrow story.** `harborview` is a *new* merchant with 13.8% of rows over 1000, and its large-value subset is 100% whole-dollar — the same fingerprint `belltower` carries. The signature separates them only because `harborview`'s segment is *mixed* (15.8% vs 100%); a looser signature (`max > 1000`, `p99 > 1000`) captures both. Two readings stay open: a genuine high-ticket partner, or a partial unit error in 33 rows. Nothing in these two files settles it — that needs the producer.

**No harm bound exists here.** Neither file contains a downstream signal that moves — no settlement control total, no bill, no labelled outcome. So the three blockers block because they contradict a producer commitment (declared type, declared unit, key/completeness), not because a distribution moved far enough. Nothing in this contract is licensed to say "past here, something downstream is wrong."

Recorded in the contract: **NOT BACKTESTED** (one prior batch, so firing counts can't be produced), held-out coverage measured on a within-batch split (all constraints held, which is weaker evidence than it looks), and the untested defect class — no consumer of this feed was checked against the schema, so `chargeback` may break a closed-enum assumption silently.

`assert_batch.py` runs at the boundary on the raw CSV, emits one JSONL row per assertion, exits 1 on BLOCK only. Reference against itself: 0 BLOCK, 0 WIDEN.
