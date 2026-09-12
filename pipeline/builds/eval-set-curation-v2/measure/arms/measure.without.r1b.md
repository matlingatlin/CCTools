I read the file and computed everything below from it. Headline structure first, since all four answers depend on it:

| slice | rows | share of file | accuracy | in few-shot | exact dupes |
|---|---|---|---|---|---|
| simple_lookup | 1647 | 82.35% | 94.72% | 33 | 60 pairs |
| multi_hop | 264 | 13.20% | 67.05% | 3 | 0 |
| ambiguous | 67 | 3.35% | 46.27% | 1 | 0 |
| adversarial | 22 | 1.10% | 31.82% | 0 | 0 |
| **all** | **2000** | | **88.75%** | **37** | **60 pairs** |

After removing few-shot rows, duplicates, and contradictory pairs, the usable pool is **1900 rows**: simple_lookup 1551, multi_hop 261, ambiguous 66, adversarial 22.

---

## Q1 — The 200 rows, and what the choice costs

**Selection rule (deterministic, reproducible):** from the 1900-row clean pool (Q3), sort each slice by `md5(id)` and take the first N:

| slice | take | leaves per-slice 95% CI |
|---|---|---|
| simple_lookup | 62 | ±5.5 pp |
| multi_hop | 50 | ±13.1 pp |
| ambiguous | 66 (all of them) | ±12.0 pp |
| adversarial | 22 (all of them) | ±19.5 pp |

Score it with **traffic reweighting** — 0.8235·simple + 0.1320·multi + 0.0335·amb + 0.0110·adv. Never report the raw mean of these 200 rows; unweighted it reads ~65%, which is meaningless, because the set is deliberately not traffic-shaped.

**Why not just sample 200 rows at random.** Proportional sampling gives you 165 / 26 / 7 / 2. I simulated 2000 draws: **8.6% of the time you get zero adversarial rows, 33% of the time you get ≤1.** A two-row adversarial "score" has a 95% CI of ±65 pp. You would be shipping with no measurement at all on the slice the assistant is worst at.

**What the choice costs — three real prices:**

1. **Headline precision.** Random-200 gives a headline ±3.9 pp; my allocation gives ±4.9 pp. You pay 1 pp of headline precision to buy adversarial from ±65 pp down to ±19.5 pp and ambiguous from ±37 pp to ±12 pp. That is a good trade, but it is a trade.
2. **You give up 1700 rows for nothing.** The clean pool of 1900 scored in full gives a headline of ±1.3 pp and simple_lookup ±1.1 pp. If grading is automated, **cutting to 200 is the most expensive decision in this whole exercise** and I'd push back on it. Cap at 200 only if a human grades every row.
3. **The tails don't improve no matter what you do.** Adversarial has 22 clean rows in the entire file and ambiguous has 66. Taking 100% of both is the ceiling. ±19.5 pp on adversarial means the true accuracy is somewhere in 12%–51% — that slice cannot be measured from this file at any sample size. That's a data-collection problem, not a sampling problem.

---

## Q2 — Is 88.75% trustworthy?

**No. Don't ship on it.** Four problems, in ascending order of severity:

1. **It includes training data.** 37 rows have `in_fewshot_prompt=1` and score **97.3%** vs 88.59% for everything else. The model has literally seen these. Removing them: 88.75% → **88.59%**. Small numerically, but it means the number was never a held-out measurement.
2. **It double-counts.** 60 query strings appear twice (120 rows, ids q0000–q0119 — a natural-language block distinct from the templated rest of the file). Every duplicate is `simple_lookup`, the easiest slice, so they tilt the mix upward and they break the independence assumption behind any confidence interval you'd put on the number.
3. **The labels contradict themselves.** 5 of the 60 duplicate pairs have the *same query* graded both 1 and 0 — e.g. `q0054`/`q0044` "when will the the trial refund arrive" → 1 and 0; `q0088`/`q0098` "is our team covered by the warranty" → 0 and 1. That's an **~8% self-disagreement rate on repeated inputs**. It puts a noise floor under every number in this file, including 88.75%.
4. **The real problem: it isn't a capability number, it's a traffic-mix number.** 82% of the file is one easy slice. The per-slice reality is 94.7 / 67.1 / 46.3 / **31.8**. The assistant fails roughly a third of multi-hop, half of ambiguous, and two-thirds of adversarial queries, and the headline conceals all of it behind simple_lookup volume. It also moves without any model change: shift 10 pp of traffic from simple_lookup into the hard tails and the same model reports ~82.8%. A metric that swings 6 pp on mix drift is not a ship gate.

**What I'd report instead:** "88.6% on traffic mix (95% CI ±1.3 on the full clean pool), composed of 94.8 / 66.7 / 45.5 / 31.8 across simple_lookup / multi_hop / ambiguous / adversarial, with adversarial and ambiguous under-powered." Then let the team decide whether 31.8% adversarial is shippable. My read: it isn't.

---

## Q3 — What has to be removed before freezing

**Hard removals — 100 rows, 2000 → 1900:**

1. **All 37 `in_fewshot_prompt=1` rows.** Non-negotiable train/test leakage. Also make this a permanent invariant: any row that ever enters the prompt is permanently evicted from the eval set, and CI should assert `sum(in_fewshot_prompt) == 0` on the frozen file.
2. **58 duplicate rows** — 60 dup groups, keep one member each (55 groups after step 3), drop the rest. Dedupe on normalized query text, not on `id` (all 2000 ids are unique, so id-dedup catches nothing).
3. **All 10 rows in the 5 contradictory-label pairs.** Drop both members, not one — you don't know which label is right. Fix the grader before deciding they're recoverable, then re-adjudicate.

**Blockers that aren't a row filter — these are why I wouldn't freeze it yet:**

4. **There is no expected-output column.** `correct` is a stored verdict about one model run, not ground truth. As-is, this file can only rescore the exact system that produced it; the moment you change the model, prompt, or retrieval, every label is stale and the file scores nothing. **An eval set needs the gold answer.** This is the single biggest gap.
5. **Provenance of the q0000–q0119 block.** 120 rows in natural-language form (with template artifacts like "the the"), all simple_lookup, all perfect duplicate pairs — unlike the other 1880 templated rows. That's an injected batch from a different source. Confirm where it came from before keeping any of it.
6. **No timestamp column**, so you cannot check whether this is one week of traffic or a year, and you cannot detect the mix drift described in Q2. Add it.
7. **PII scan.** These queries are synthetic, but the shapes ("change my billing address to…", "reset the password for…") are exactly where real logged traffic carries account data. If any of this touches production logs, scrub before freezing a file that will be committed and shared.

---

## Q4 — How many examples per slice before a per-slice score means anything?

Depends on the question you're asking of it. Two different bars:

**Bar A — reporting an absolute per-slice number.** Rows needed for a 95% CI at the observed accuracies:

| slice | ±10 pp | ±7 pp | ±5 pp |
|---|---|---|---|
| simple_lookup (~95%) | 19 | 39 | 76 |
| multi_hop (~67%) | 86 | 175 | 342 |
| ambiguous (~46%) | 96 | 195 | 382 |
| adversarial (~32%) | 84 | 171 | 334 |

Accuracy near 50% is the expensive regime; simple_lookup is cheap only because it's near the ceiling.

**Bar B — detecting a regression between two builds.** This is what you actually do week to week, and it's far cheaper if you run both builds on the *same* items and use McNemar on the discordant pairs. At 80% power / 95%:

| discordance rate | detect 15 pp | 10 pp | 5 pp |
|---|---|---|---|
| 10% of items flip | 35 | 79 | 314 |
| 20% flip | 70 | 157 | 628 |

(Unpaired comparison of two independent samples needs ~300–400 *per arm* for a 10 pp shift on the hard slices — 4× worse. Always pair.)

**Concrete recommendation:**

- **n < 30 per slice: don't publish a number.** Show the raw fraction ("7/22 adversarial") and no percentage. At n=22 the CI is ±19.5 pp — 12% to 51% — which is compatible with both "badly broken" and "merely bad."
- **100 per slice** is my minimum for a slice that gates a release: ±9 pp absolute, ~10 pp paired regression detection. Good enough for go/no-go.
- **300+ per slice** if you want ±5 pp absolute or to catch 5 pp regressions.

**Against this file:** simple_lookup (1551) and multi_hop (261) clear the 100 bar. **Ambiguous (66) and adversarial (22) do not, and no sampling scheme fixes that** — the rows don't exist. Before per-slice scores on those two mean anything, someone has to write or collect roughly **80 more ambiguous and 280 more adversarial cases with gold answers**. Given that those are the two slices where the assistant is at 46% and 32%, that authoring work is the highest-value thing on this list — and it's the reason I'd hold the freeze rather than lock in a set that can't see the failures.