# What's actually in the file

```
slice            rows    share    accuracy
simple_lookup    1647    82.35%     94.7%
multi_hop         264    13.20%     67.0%
ambiguous          67     3.35%     46.3%
adversarial        22     1.10%     31.8%
                 ─────
                 2000              88.75%   ← the reported number, exactly
```

Also: **37 rows are flagged `in_fewshot_prompt=1`** (they score 97.3%), and **60 query strings appear twice**.

---

# Q1 — The 200 rows

**Selection rule** (in `curate.py`, seed 20260902, rebuilds byte-identically):

1. **Drop all 37 contaminated rows.** These are the prompt's own few-shot examples. They measure recall of the prompt, not capability. Removed, not down-weighted.
2. **Collapse near-duplicates, not just exact matches.** 1880 rows carry opaque placeholder text (`simple_lookup case 970 89fcd07f`) — each is its own cluster, nothing to compare. The other 120 rows carry real query text, and they collapse hard: 120 rows → 60 exact-distinct → **8 clusters** after normalizing (`"the the"` → `"the"`) and blanking the plan-name slot. They are six question templates — cancel / refund / balance / billing address / password reset / warranty — filled with ten plan names. A 15:1 collapse.
3. **Stratify to a post-dedup target, sample within cell, 60/40 dev/holdout.**

| slice | pop | eligible clusters | drawn | dev | holdout | acc | 95% CI |
|---|---|---|---|---|---|---|---|
| simple_lookup | 1647 | 1502 | 57 | 34 | 23 | 94.7% | 85.6–98.2 |
| multi_hop | 264 | 261 | 55 | 33 | 22 | 70.9% | 57.9–81.2 |
| ambiguous | 67 | 66 | **66 (all)** | 40 | 26 | 45.5% | 34.0–57.4 |
| adversarial | 22 | 22 | **22 (all)** | 13 | 9 | 31.8% | 16.4–52.7 |

I took **every** eligible ambiguous and adversarial row. At n=22 you cannot afford to leave any behind. The remaining 112 went to the two slices carrying the real error mass — simple_lookup and multi_hop each account for ~44% of total production error (0.8235×0.053 vs 0.132×0.330).

**Report per-slice first.** If you need one number: reweighted by true traffic shares, **89.3% ±2.6pp, labeled an estimate**. Never the raw mean of the 200, which is 65% — stratification deliberately over-samples the rare slices.

## What the choice costs

- **Adversarial can't clear the floor.** 22 examples exist in the entire log; the practical floor is ~30. This cell is **genuinely exhausted, not under-sampled** — that is a finding, not a defect. Its holdout is 9 rows, which is an anecdote, not a measurement. Adversarial should be judged on the 13 dev rows, and the holdout adversarial number should not be quoted.
- **No reserve in the rare slices.** Taking all 66 ambiguous and all 22 adversarial means there is nothing left to top up from or to cut a fresh holdout when this one wears out. You are dependent on new traffic accruing.
- **Coarse resolution where you most need it.** Smallest change these n's can reliably detect: simple_lookup ±12pp, multi_hop ±25pp, ambiguous ±24pp, **adversarial ±39pp**. A prompt change that moves adversarial from 32% to 60% will not register as significant. Budget more traffic collection before you promise to measure adversarial improvement.
- **1800 rows discarded (90%).** That is the intended outcome, not waste — but it means anyone expecting "we evaluate on all our data" needs to be told why.
- **The simple_lookup variety number is unknown.** Only 120 of 1647 rows have inspectable text, and those collapse 15:1. If the other 1527 look like that sample, simple_lookup's true distinct-variant count is far below 1502 and the set over-represents this slice's diversity. **Get real query text logged for that slice and re-run step 2** — this is the one open risk in the selection.

---

# Q2 — Is 88.75% trustworthy?

**No — but not because it's biased.** That's the part worth being precise about, because the obvious critique is wrong.

88.75% is the exact mean of all 2000 rows. Since the log *is* the production population, it's a fair estimate of the population mean. Removing contamination and dupes barely moves it: 88.75% → 88.59% → 88.50%. Anyone who argues "it's inflated by leakage" is arguing about 0.25pp.

It's untrustworthy for four other reasons:

1. **It is an in-sample number with zero holdout.** Nothing was withheld. If anyone tuned prompts or fixed bugs against this traffic — and the 37 few-shot rows prove at least some of it fed the prompt — the number is contaminated at the *process* level even after those 37 rows are dropped. There is currently no honest final number available for this system at all.
2. **It averages away the slices you'd act on.** Behind 88.75% sit **adversarial at 31.8% and ambiguous at 46.3%**. Those two are 4.5% of traffic and invisible in the headline. Shipping on 88.75% means shipping without knowing that two-thirds of adversarial inputs fail.
3. **It's hostage to traffic mix, not quality.** Holding per-slice accuracy *completely fixed*, if adversarial+ambiguous grow from 4.5% to 12.3% of traffic, the headline falls to 85.0%; at 18.9%, to 81.8%. An 7pp "regression" with zero change in the system. Conversely, more easy lookups make it rise. The number moves for reasons unrelated to quality — the exact failure mode an eval set is supposed to prevent.
4. **The precision is fictional.** Four significant figures on a number whose actionable components have ±23pp and ±36pp confidence intervals. And the system is nondeterministic: of the 60 query strings logged twice, **5 got different outcomes on identical text**. Re-running the suite gives a different number.

**Recommendation: don't ship on it.** Concretely:

- Replace the single number with the per-slice table as the gate. Set thresholds per slice, not on the pooled mean.
- If a headline is required for reporting, use the reweighted estimate (**89.3% ±2.6pp**) and label it an estimate with its weighting written down.
- Run the release decision on `eval_dev_120.csv`; open `eval_holdout_80.csv` **once**, to confirm a decision already made, and log the date and reason. Every look burns it.
- Treat adversarial as **not yet measurable**. Before you can gate on it, collect adversarial traffic to n≥60 — that's the single highest-value data-collection task here.
- Re-run contamination checks after any prompt or few-shot edit. Today's clean set is contaminated by tomorrow's prompt change.