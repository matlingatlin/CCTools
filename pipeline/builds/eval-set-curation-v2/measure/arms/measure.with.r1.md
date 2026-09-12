I ran the method's four steps in its required order: contamination removal → cluster collapse → floor derivation → holdout. Both deliverables are attached (the filled record and the 200 ids). Answers below.

## Q1 — The 200 rows, and what the choice costs

**Order matters and changed the numbers.** Removing contamination first (2000 → 1963) meant I clustered rows I wasn't about to delete; collapsing before deriving the floor meant the floor was derived against an n that still exists. Reweighting came last, against the *original* population shares.

**The set (attached, `eval_set_200.csv`, seed 20260902):**

| Slice | Post-collapse pool | Allocated | Interval at that n (p=0.5, Wilson) | Clears the ±10 floor? |
|---|---|---|---|---|
| adversarial | 22 | **22** (census) | ±19.3 | No — never can |
| ambiguous | 66 | **66** (census) | ±11.7 | No — never can |
| multi_hop | 261 | **93** | ±9.9 | **Yes** |
| simple_lookup | 1502 | **19** | ±20.8 | No |

**What it costs, concretely:**

1. **200 rows buys exactly one gating slice.** `multi_hop` is the only one that can block a release. `simple_lookup` — 82% of your production traffic — gets 19 rows and a trend line, not a gate. That is the price of a 200 budget, not of this allocation: `93+93+66+22 = 274` is the smallest set where both large slices gate. If you can afford 274, take it; the extra 74 rows are the difference between one gated slice and two.
2. **Two slices are unfixable by sampling.** `ambiguous` (66) and `adversarial` (22) are censuses — I took every row that exists. They are 27 and 71 rows short of the floor respectively. No sampling decision closes that; you have to *collect or write* more adversarial traffic. Report them as **30/66** and **7/22**, never as 45.5% and 31.8%.
3. **Deliberate over-sampling distorts the headline.** adversarial is 1.1% of traffic and 11% of the set. So the set's raw mean is meaningless; the headline is reweighted to **88.63%** and labelled an estimate. (Stratification guarantees slice representation; it does *not* by itself make the overall mean more precise — that gain is conditional, per C7.)
4. **Every interval above is narrowest-case.** The file has no user or session id, so no cluster adjustment is possible. If your traffic has multiple turns per user, the true intervals are wider than these by an amount nothing in the evidence bundle measures for production logs. **Adding a `user_id` column is the highest-value change to this file.**

## Q2 — Is 88.75% trustworthy?

**No.** It is arithmetically correct and decision-useless, for three independent reasons — and the reasons compound in the direction of the number being *less* informative than it looks, not just noisy.

**It is a weighted average of four very different systems.** Pooling hides that:

| Slice | Clean accuracy | Share of traffic |
|---|---|---|
| simple_lookup | 94.7% | 82.4% |
| multi_hop | 66.7% | 13.2% |
| ambiguous | 45.5% | 3.4% |
| adversarial | 31.8% | 1.1% |

88.75% is essentially a report on `simple_lookup` wearing a whole-system label. Your assistant is wrong about **a third of the time** on multi-hop questions and **two-thirds of the time** on adversarial ones. Nothing about shipping should be decided on the pooled figure.

**It is inflated by contamination.** 37 rows are in the few-shot prompt. They score **97.3%** against **88.6%** on everything else. The pooled effect is small (−0.16 pts) only because they're 1.85% of the file — the per-row inflation is 8.7 points, and 33 of the 37 sit in `simple_lookup`, the slice already carrying the headline.

**It is inflated by a templated family voting 120 times.** 120 rows in `simple_lookup` are 6 intents × 10 product names × 2 exact copies (`how do i cancel the {basic|premium|the pro|student|…} subscription`). They score 94.2%. Exact dedup takes them to 60 and reads clean — that is the trap. They are **6 observations**, not 120: a 20× over-weighting inside the volume slice.

Corrected, reweighted, contamination-free: **88.63%**, and that number should still never be shipped on by itself.

## Q3 — What has to be removed before freezing

Three things, in this order — the order is not cosmetic, since clustering rows you're about to delete gives wrong cluster sizes:

1. **37 contaminated rows** (`in_fewshot_prompt == 1`). **Removed, not down-weighted.** 2000 → 1963.
2. **58 exact duplicates** after normalising case and whitespace only. 1963 → **1905 distinct strings**.
3. **54 near-duplicate members** of the templated family. 1905 → **1851 distinct clusters**, keeping one representative per cluster with its size recorded.

**Report both dedup numbers, never one: 1905 distinct strings, 1851 distinct clusters.** Stopping at 1905 is the failure — it leaves the six-intent family standing as sixty rows.

**Threshold, honestly derived:** I hand-labelled 50 pairs across the score range. Same-intent pairs scored 0.581–0.689 on 5-shingle Jaccard; different-intent pairs 0.000–0.056. The labels flip cleanly in a wide empty band, so I set the cut at 0.50.

**What I normalised, and what I deliberately did not** — this is the field that lets you check the above: case and whitespace only. I did **not** normalise the product-name slot, and I did **not** normalise the `case <N> <hex>` identifiers. Normalising either would have collapsed the family in step 1, made both dedup counts come out equal and clean, and left the failure fully intact.

**What the detector cannot see, stated rather than implied:** lexical similarity scores near zero on paraphrase sharing no character 5-grams ("cancel my subscription" vs "I'd like to stop paying"). The bundled evidence measures a 10-gram detector at F1 = **0 on all six rephrased conditions** while scoring 0.926/1/0.816 on verbatim ones. That class is assumed absent here and was **not tested**. Separately, the 1502 `simple_lookup case N <hex>` rows are opaque placeholders — no lexical detector can judge them, so **1851 is an upper bound** and the collapse must be re-run against the real query strings.

## Q4 — How many per slice

**93.** Here is where it comes from, because a round number in the analyst's own voice is not an answer.

1. **The decision it gates.** Below 93: the slice is a raw fraction on the dashboard and does **not** block a release. At or above 93: a percentage is quoted and a drop past the pre-registered threshold **blocks** the release.
2. **The tolerance, named before the arithmetic.** We will not act on a slice score we can only locate to within **10 accuracy points**, two-sided 95%. Wider than that, "shipped a regression" and "resampled the same system" are indistinguishable.
3. **The inversion, with its inputs stated.** Wilson interval at **p = 0.50, worst case** → n=93 gives ±9.9, n=92 gives ±10.1. **p was fixed at the same time as the tolerance and before any candidate score was seen** — deliberately at 0.5 rather than at each slice's incumbent accuracy, because an informed-p floor narrows precisely when the score moves, which is when you need it. (For contrast: at `simple_lookup`'s observed p=0.947 the floor would be 25, and at `multi_hop`'s 0.667 it would be 82. Those are the numbers you get by reading p after scoring; I'm flagging them rather than using them.)
4. **Variance assumption:** binomial, independent rows — **naive Wilson, no cluster adjustment**, because the file carries no user id. Treat 93 as a *lower* bound on the real requirement.
5. **Owned by:** me as analyst of record, fixed 2026-09-02, written into the attached record. It needs a countersign from whoever owns release gating — that's the one field I can't fill for you.

**Two notes on numbers you'll hear.** The widely-quoted **~1,000-question floor** is *derived*, not measured — computed from variance parameters its own author calls fictional in the same sentence. It can inform a default; it is not evidence that 1,000 holds. And the published half-widths people cite (widest: 8.30 points at n=100) have **no row at n=200 or n=500**, the sizes teams actually pick, and carry no cluster adjustment — which is why I computed 93 rather than reading a number off a table.

**The honest limit:** two of your four slices cannot reach 93 no matter how you sample, because their entire post-collapse populations are 66 and 22.

**One flag on the holdout.** I derived the split after the floor, as required — and splitting 200 into dev/holdout drops all four slices below it, so the 200-row set is the holdout in full with dev drawn from the remaining 1651. But as of this cut **nothing enforces the seal**, so the record says **UNSEALED** rather than calling the pool a holdout. Sealing it needs three concrete things (separate ACL the CI service account can read and engineers can't; aggregate-only scoring output; a CI check rejecting any commit that puts a holdout id into a prompt or fixture). Until those exist, this is a reserved sample. The look budget I've written — 1 per release candidate — is a **policy someone owns**, not an evidence-based number: the strongest result on holdout reuse is a synthetic worst case that gives no safe reuse count, and the two results pointing the other way are on rate-limited platforms with never-revealed private splits, which an internal set scored on every commit is not.