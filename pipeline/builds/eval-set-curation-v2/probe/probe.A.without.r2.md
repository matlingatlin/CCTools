## What's actually in the file

| slice | rows | share | accuracy |
|---|---|---|---|
| simple_lookup | 1647 | 82.3% | 94.7% |
| multi_hop | 264 | 13.2% | 67.0% |
| ambiguous | 67 | 3.4% | 46.3% |
| adversarial | 22 | 1.1% | 31.8% |

Three defects before any sampling:

1. **37 rows have `in_fewshot_prompt=1`.** They score 97.3% vs 88.6% for everything else — the model has seen them.
2. **60 exact-duplicate query pairs** (120 rows, ids `q0000`–`q0119`, all simple_lookup). These are the only human-looking queries in the file; the other 1880 are templated `slice case N hash` strings. Duplication double-weights them.
3. **5 of those pairs carry conflicting labels** — identical query text, opposite `correct` values (e.g. `how do i cancel the basic subscription` is 1 at `q0031` and 0 at `q0021`). At least one label in each pair is wrong, and I can't tell which.

After dropping few-shot rows, dropping both copies of the 5 conflicting pairs, and keeping one copy of the other 55: **1899 eligible rows** (101 excluded, itemized in `excluded_rows.csv`).

## Q1 — the 200 rows, and what they cost

I sampled stratified with deliberate oversampling of the hard slices, seed 20260902:

| slice | sampled | of pool | per-slice 95% CI |
|---|---|---|---|
| simple_lookup | 68 | 1550 | ±5.7 pt |
| multi_hop | 60 | 261 | ±11.6 pt |
| ambiguous | 50 | 66 | ±13.3 pt |
| adversarial | 22 | 22 | ±18.2 pt |

Every row carries a `stratum_weight` column. **Never read the raw mean of this file** — it's 69.0% by construction. Reweighted it's 88.55%, which is the number comparable to production.

Why not proportional allocation? Proportional gives adversarial **2 rows** and ambiguous **7** — CIs of ±40 and ±30 points. You'd be unable to detect a 20-point regression on the slices where the model is weakest. The hybrid costs you **0.7 points of precision on the headline** (±4.4 vs ±3.8 pt) and buys usable resolution on all four slices. That trade is worth making.

The real costs, stated plainly:

- **The headline number is no longer directly readable.** Anyone who averages the `correct` column gets 69% and panics. This needs to be enforced in the harness, not documented in a README.
- **Adversarial is exhausted.** I took all 22 rows, so there is no held-out adversarial data. Any fix targeting adversarial will be validated on the same rows it was tuned against. Even at n=22 the CI is ±18 pt — this slice is *not measurable* from this file. It needs dedicated collection, ~200 rows, before it can gate anything.
- **Ambiguous is nearly exhausted** — 50 of 66, leaving 16 for future use.
- **You still can't measure real-query performance.** Only 120 rows in the entire file are natural language, all simple_lookup, and 55 survive dedup. The eval is overwhelmingly templated strings, which likely overstates performance on all four slices.
- The 1699 unused rows are in `heldout_pool.csv` — usable as a dev set, but they must stay out of few-shot prompts or you recreate defect #1.

## Q2 — is 88.75% trustworthy?

**No, but not for the reason you'd expect.** Here's the decomposition:

```
raw file (2000 rows)                88.75%
- drop few-shot contamination       88.59%
- dedup + drop conflicting labels    88.52%
```

Cleaning the data moves it **0.23 points**. So the number is arithmetically almost right — and that's exactly the trap. It's not wrong, it's *not a measurement of what they think*.

88.75% is a measurement of the traffic mix, not of the assistant. 82% of the file is one easy slice at 94.7%. **Everything that isn't simple_lookup runs at 60.5%** (n=349). The headline is a weighted average dominated by the case you already handle.

This makes it fragile in a specific way:

| traffic mix | headline |
|---|---|
| today (82/13/3/1) | 88.5% |
| hard slices 2× | 82.1% |
| hard slices 3× | 75.8% |

Per-slice accuracy unchanged — only the mix moves. A single marketing push or a support-flow change that routes more complex questions to the assistant drops the headline 6–13 points with no model regression at all. Shipping on 88.75% means shipping on an assumption about traffic composition that nobody has written down or committed to monitoring.

Two smaller points: the ±1.38 pt CI on 2000 rows captures sampling error only — the contamination and duplication biases are systematic and sit entirely outside it. And the 5 conflicting label pairs mean the ground truth itself has a nonzero error rate that nobody has quantified; 5 detectable conflicts among 60 checkable pairs is roughly 8%, and there's no reason to think the 1880 templated rows are cleaner — they're just unduplicated, so the errors are invisible.

**Recommendation:** don't ship on a single number. Gate on the four per-slice numbers with the reweighted 88.5% reported alongside as context, treat adversarial as unmeasured rather than as 31.8%, and audit a sample of templated-row labels before the next cut. If you need one number for a ship decision, use the reweighted estimate with its ±4.4 pt band and an explicit stated assumption about traffic mix.

Happy to write this up as a shareable page for the team if it needs to travel beyond this terminal.