Worked the file end to end. One note on ordering before the answers: the method's steps run **contamination removal → cluster collapse → floor derivation → holdout split**, and every one of those changes the next one's numbers. So Q3's answer actually ran first, and Q4's floor was derived on the collapsed set. Files are above.

## Q1 — the 200 rows, and what the choice costs

**What I did.** Deleted 37 contaminated rows (Q3), collapsed 1963 → 1851 clusters (Q2), derived the floor (Q4), *then* selected. Selecting before collapsing would have picked duplicate intents; deriving the floor before collapsing would have sized against an n that no longer exists.

Allocation, deliberately over-sampling the rare slices:

| Slice | Population share | Clusters available | **Picked** | Set share | Realized 95% CI |
|---|---|---|---|---|---|
| simple_lookup | 82.4% | 1502 | **30** | 15% | ±12.2 |
| multi_hop | 13.2% | 261 | **82** | 41% | ±10.0 |
| ambiguous | 3.4% | 66 | **66** (all) | 33% | ±11.7 |
| adversarial | 1.1% | 22 | **22** (all) | 11% | ±18.2 |

**What it costs — four things, concretely:**

1. **Two slices are exhausted, and no budget fixes them.** `ambiguous` (66 clusters) and `adversarial` (22) are taken *whole*. Reaching ±10 needs n≥92 and n≥80 respectively. The population is 26 and 58 rows short. This isn't a sampling choice — you cannot buy your way out of it with a bigger eval set, only by collecting more adversarial traffic.

2. **Only `multi_hop` actually clears the ±10 floor** in the drawn sample. `simple_lookup` at n=30 came in at ±12.2 — and that's instructive: its floor of 24 was inverted at its *observed* p=0.947, but the 30-row draw landed at p=0.867 and the interval blew out. A floor derived from a post-scoring p is fragile in exactly this way. At worst-case p=0.5 the floor is **93 per slice**, and 4×93 = 372 > 200.

3. **The 200 buys at most one robustly-measured slice.** With 88 rows forced into the two capped slices, 112 remain; a p=0.5-robust ±10 costs 93 of them. If you can move to **282** (97/97/66/22), both measurable slices clear ±10 at any p — that's the cheapest allocation that makes the gate mean something. I'd take that trade.

4. **The set is deliberately unrepresentative.** simple_lookup is 82% of traffic and 15% of the set. Any headline from this set must be reweighted to the *original* population shares, not the set's.

## Q2 — is 88.75% trustworthy?

**No.** Three separate problems, smallest first:

**It's contaminated.** 37 rows are in the few-shot prompt and score 97.3% vs 88.6% for everything else. Removing them: 88.75 → 88.59. Worth **0.16 points** — real, but the least of it.

**It's cluster-inflated.** Six templated intent families occupy 118 rows. Exact dedup finds only 60 repeats and reports 1905 "clean" rows — the families survive it completely, because one intent filled with ten product names is ten distinct strings. Collapsed properly they are **6 observations, not 118**. Two numbers, not one:

- distinct **strings** after normalised exact match: **1905**
- distinct **clusters** after near-duplicate collapse: **1851**

Normalisation was case and whitespace only. I deliberately did *not* normalise the product slot — doing so collapses the family in the wrong step and makes the two numbers come out equal and clean while the problem is still there. I also did not normalise the `case <N>` token, which looks like an ID but is 1:1 with the `id` column: normalising it would have destroyed 1845 distinct observations rather than merging repeats.

**And it's the wrong number regardless.** This is the real problem. 88.75% is a volume-weighted average that is 82% one easy slice:

| Slice | n (post-collapse) | Accuracy |
|---|---|---|
| simple_lookup | 1502 | **94.7%** |
| multi_hop | 261 | **66.7%** |
| ambiguous | 66 | **30/66** |
| adversarial | 22 | **7/22** |

Shipping on 88.75% means shipping a feature that fails a third of multi-hop queries and two-thirds of adversarial ones. Corrected stack: 88.75 → 88.59 (contamination) → 88.28 (collapse) → **88.6% reweighted**. The headline barely moves, and that is the point — **the number is roughly right and still not trustworthy**, because no single number is the trustworthy artifact here. Report per-slice or don't report.

## Q3 — what has to be removed before freezing

**37 rows where `in_fewshot_prompt = 1`** — removed, not down-weighted. They score 97.3% against 88.6%, and they're concentrated in simple_lookup (33 of 37), so they inflate the slice that already dominates the pooled mean. This must happen **before** clustering, or you cluster rows you're about to delete and every cluster size is wrong.

**112 near-duplicate rows** get collapsed (not deleted) to 6 representatives, with cluster sizes recorded so reweighting stays possible.

**What I could not check, and you should not treat as clean:** the file supports exactly one contamination channel. Four others are **UNKNOWN** — fine-tune/training data, retrieval index, public benchmarks, and hard-fixed debug traces. No manifests were supplied. The one channel that *was* checkable turned out contaminated, which is not evidence the other four are clean. Close them before this gates a release.

**What the detector cannot see.** Shingle Jaccard is a surface-form detector; it catches the templated head and **no paraphrase at all** — `cancel my plan` vs `how do i cancel the basic subscription` scores near zero and survives as two clusters. C6 measures the neighbouring case: a 10-gram detector scored 0.926/1/0.816 on verbatim conditions and **0 on all six rephrased ones**, with embedding detectors spanning the full 0-to-1 range. MinHash was *not* evaluated there and I'm not claiming it was. This corpus is synthetic and contains no paraphrases, so this run tells you nothing about the paraphrase rate in real traffic — 1851 is an upper bound on effective N, not a measurement of it.

## Q4 — how many per slice

**The floor is not a number you can look up; it's the output of a tolerance somebody owns.** So, stated in order:

**The decision it gates:** below the floor, a slice is reported as a raw fraction, never a percentage, and does not block a release. Above it, the slice is quoted with its interval and a 10-point drop blocks the ship.

**The tolerance:** largest half-width we'll act on is **10 accuracy points**. Reason: the ship conversation turns on roughly-fine vs roughly-broken, and a score locatable only to ±15 can't separate 60% from 75%.

**The inversion, and the p it needs:**

| Inverted at | Floor | Use when |
|---|---|---|
| **worst-case p = 0.50** | **n ≥ 93** | the floor must survive whatever the model does next — **quote this one** |
| observed p (simple_lookup 0.947) | 24 | only valid while p holds there |
| observed p (multi_hop 0.667) | 82 | |
| observed p (ambiguous 0.455) | 92 | |
| observed p (adversarial 0.318) | 80 | |

**So: ~93 per slice**, and the observed-p floors are optimistic because **p was fixed after scoring** — the `correct` column was already in the file. Q1's simple_lookup result is the live demonstration: its p=0.947 floor of 24 failed on a real 30-row draw.

**Two caveats that make 93 a floor, not a ceiling.** The intervals are **naive Wilson with no cluster adjustment** — the file has no user or session column, so clustering can't be measured. Real support traffic has several tickets per customer, and C2 measured cluster-adjusted standard errors up to 3.05× naive (but 1.10× on another eval, and its own limits exclude production logs — so no multiplier is carried into the floors). The true intervals are wider by an amount **nothing in the evidence measures for production data**.

And if anyone reaches for the ~1,000-question floor: it's **DERIVED** from ω²=1/9 and σ²=0, parameters the author calls fictional in the same sentence that states the 1,000. It can inform a default. It is not evidence, and it is not a tolerance.

**The two gaps in this record, stated rather than papered over:** the ±10 tolerance has **no named owner** and was fixed **after the first score was seen**. Both need fixing before these floors are quoted as a standard. And the 112-row reserve pool is marked **UNSEALED** — separate storage is a filename, not a mechanism; it becomes a holdout when the scorer can't read those ids without a named approval. `ambiguous` and `adversarial` are consumed whole by the eval set and have **no holdout at all**, so nothing about this assistant's adversarial behaviour can be described as confirmed on held-out data.