Here's what the file actually contains, and what follows from it.

**The population (2,000 rows), measured before sampling:**

| slice | n | share | accuracy | in few-shot |
|---|---|---|---|---|
| simple_lookup | 1,647 | 82.35% | 94.72% | 33 |
| multi_hop | 264 | 13.20% | 67.05% | 3 |
| ambiguous | 67 | 3.35% | 46.27% | 1 |
| adversarial | 22 | 1.10% | 31.82% | 0 |

## Q1

Files are attached: **119 dev + 81 frozen holdout** (60/40 within each cell; the 120/80 split lands at 119/81 after per-cell rounding). Seed 20260902, sampled from the 1,963 uncontaminated rows only, with `cluster`, `cluster_size`, `why_included`, `seed` columns so it rebuilds.

Allocation — floor of 30 per cell, remainder pushed toward error variance, not toward traffic:

| slice | clean pop | allocated | NL | templated | floor 30 |
|---|---|---|---|---|---|
| simple_lookup | 1,614 | 64 | 18 | 46 | ok |
| multi_hop | 261 | 64 | 0 | 64 | ok |
| ambiguous | 66 | 50 | 0 | 50 | ok |
| adversarial | 22 | **22** | 0 | 22 | **exhausted** |

simple_lookup is 82% of traffic and gets 32% of the set — deliberate. It scores 94.7% with variance 0.050; ambiguous carries variance 0.249. Spending the budget proportionally would buy precision where nothing is failing.

**What the choice costs — four things, concretely:**

1. **adversarial cannot reach the floor.** There are only 22 such rows in the entire file. I took all of them; the cell is genuinely exhausted, not under-sampled. At n=22 its score is 31.8% **±19.5%** — that CI spans 12% to 51%, so this cell cannot detect anything short of a total regression. It's an anecdote and must be labeled one on every report. Fixing it means logging more adversarial traffic or generating synthetic cases; it cannot be fixed by resampling this file.
2. **ambiguous is 50 of 66 available.** Taking most of the cell leaves only 16 rows in reserve, so the next refresh has almost no unseen ambiguous data to draw anchors from.
3. **Precision is capped at roughly ±6pp per slice** even where I spent generously. multi_hop at n=64 is ±11.4%. A prompt change worth 5pp will not be visible in a single slice on this set.
4. **The 200 lose the head's raw volume.** Any absolute pooled number computed on them is meaningless without reweighting — see Q2.

## Q2

**No — but not for the reason you'd expect, and the usual objection doesn't apply here.**

Worth being precise: this file *is* the population, not a sample of it, so 88.75% is already correctly traffic-weighted. Removing the 37 contaminated rows moves it only to **88.63%**. Weighting is not the defect.

The defects are:

**It's one pooled number hiding a 63-point spread.** 94.7% / 66.7% / 45.5% / 31.8%. The head slice is 82% of traffic, so it sets the headline almost single-handedly. Every one of your hard slices is failing and the number reads as healthy.

**It moves on traffic mix with the model frozen.** Holding per-slice accuracy exactly constant and only shifting the mix:

- simple_lookup 82% → 90%: pooled **91.1%**
- simple_lookup 82% → 70%: pooled **84.3%**

That's a 6.8-point swing from zero quality change. A marketing push that drives easy lookups would "improve" your model by 2.5 points. This number tracks your traffic distribution, not your assistant.

**The n=2,000 confidence is fictitious.** 1,880 of 2,000 rows have query text of the form `simple_lookup case 970 89fcd07f` — a placeholder with no semantic content, so variety among them is unverifiable. The 120 real natural-language rows collapse to **6 intent clusters** (refund timing, billing address, cancellation, password reset, warranty, balance), each appearing 20 times as 10 product-slot variants × 2 exact copies. Effective N on the verifiable portion is 6, not 2,000.

**The 37 contaminated rows score 97.3%** vs 88.6% for everything else — they are measuring prompt recall, and they bias upward exactly as expected.

Report instead: **per-slice first**, then "≈88% (population-weighted estimate)" with the label attached. On the curated 200 that estimate is **88.1% ±5.1%**. Note the raw stratified mean of the 200 is **66.5%** — correct arithmetic, and completely wrong as a quality claim. It must never be reported.

## Q3

Four removals, in order:

1. **The 37 `in_fewshot_prompt=1` rows.** Disqualifying, not a caveat — 33 simple_lookup, 3 multi_hop, 1 ambiguous, 0 adversarial. They score 97.3%. Delete them, don't down-weight. Re-run this check after any prompt or few-shot edit; a set that's clean today is contaminated by tomorrow's prompt change.
2. **The near-duplicate collapse.** 120 NL rows → 60 exact strings → 6 intents. I kept ≤1 per exact string and ≤3 per intent (18 rows), recording cluster size 20 on each. Without this, "password reset" phrasings would be ~17% of the eval set and would silently drive your score.
3. **The 1,880 placeholder rows have to be replaced with real query text before you freeze anything.** This is the blocking item. As written they can't be deduped, can't be inspected for contamination beyond the flag column, and can't be error-analyzed. They pass through my sampler flagged `variety UNVERIFIABLE`, which is honest but not shippable. If these stand in for real logged queries, join the real text back in and re-run steps 5–6a — the multi_hop and ambiguous cells in particular may collapse the way the NL rows did, and if they do, those cells are far smaller than 64 and 50.
4. **PII.** The NL queries reference accounts, balances, and billing addresses. Redact or pseudonymize at selection time, before the set is stored anywhere.

After removals, re-check every floor and top up from each cell's untouched population — that's why simple_lookup's 46 templated draws were taken *after* the NL dedup, not before. Sample to a post-dedup target. And once frozen: the holdout is opened once per release, logged with date and reason. Never delete a case because it fails.

## Q4

**Floor of 30 per acted-on cell; below ~10 it's an anecdote and must be labeled as one.**

The reason, at the accuracies actually in this file — 95% CI half-widths:

| slice | acc | n=10 | n=30 | n=50 | n=100 |
|---|---|---|---|---|---|
| simple_lookup | 94.7% | ±13.9% | ±8.0% | ±6.2% | ±4.4% |
| multi_hop | 66.7% | ±29.2% | ±16.9% | ±13.1% | ±9.2% |
| ambiguous | 45.5% | ±30.9% | ±17.8% | ±13.8% | ±9.8% |
| adversarial | 31.8% | ±28.9% | ±16.7% | ±12.9% | ±9.1% |

At n=10, ambiguous reads 45% ±31% — that interval contains both "coin flip" and "nearly fine." You cannot act on it. At n=30 it's ±18%: enough to tell a broken slice from a working one, which is the decision the floor exists to serve. At n=50 you get ±14%, which is roughly where a 15-point regression becomes detectable.

So: **30 to notice a slice is broken. ~100 to measure a change within it.** Note none of these n's detect a 5-point improvement — that needs n≈400 per slice, which this file cannot supply for anything but simple_lookup. Size the cell to the decision: floors for triage, and if you need to A/B a prompt tweak on multi_hop specifically, that's a purpose-built larger draw, not this set.

Two consequences for you: adversarial at 22 will never clear the floor from this data — treat its number as directional only until you log more. And the floor is what makes the budget non-proportional; matching traffic share would have given ambiguous 7 rows and adversarial 2, which is how the previous number stayed at 88.75% with three slices failing underneath it.