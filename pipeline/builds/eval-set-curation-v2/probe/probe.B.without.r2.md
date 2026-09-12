I read the file and computed everything below from it. Two findings dominate, and one of them is bigger than the question anticipated.

## Q3 — What has to be removed before you freeze this

**a) 37 rows that were in the few-shot prompt (`in_fewshot_prompt=1`).** Non-negotiable. The model saw these at inference time, so they measure memorization, not capability. They score 97.3% vs 88.6% for everything else. They're also spread unevenly — 33 of 37 land in `simple_lookup`, so they inflate your strongest slice and make the aggregate look better than it is.

**b) 60 exact-duplicate query pairs (120 rows → drop 54, quarantine 10).** Every natural-language query in the file appears exactly twice. Duplicates silently double-weight whatever they test. Worse: **5 of the 60 pairs carry contradictory labels** — same query string, one row marked correct and one incorrect:

```
q0054/q0044  "when will the the trial refund arrive"      1 / 0
q0031/q0021  "how do i cancel the basic subscription"     1 / 0
q0088/q0098  "is our team covered by the warranty"        0 / 1
q0100/q0110  "change my billing address to premium"       1 / 0
q0009/q0019  "what is the the pro balance on my account"  1 / 0
```

Don't just dedupe these — that picks a label by coin flip. Quarantine all 10 rows and have a human adjudicate. Either your grader is nondeterministic or the label is judgment-dependent, and you want to know which before freezing.

**c) 12 malformed utterances ("the the trial refund", "what is the the pro balance").** Template-generation artifacts. Repair the text or drop them; don't freeze a broken string as ground truth.

**d) The big one: 1,880 of 2,000 rows (94%) have no real query text.** They read `simple_lookup case 970 89fcd07f`, `multi_hop case 1248 …` — the slice name, an index, and a random hash. Every one is unique, so this isn't a duplicate artifact. Two things follow:

- These rows cannot be re-run against a model. There's no question to ask. Whatever `correct` says, you can't reproduce or debug it.
- The query string *contains its own slice label*. Any grader or model that reads it gets the answer key for free.

Real natural-language text exists only in `q0000`–`q0119` — the first 120 rows. That pattern says **export bug, not synthetic data**: the query column stopped being populated after the first 120 records and fell back to a placeholder. So the fix is almost certainly **re-export from the source logs, not delete**. If you delete, the file goes from 2,000 rows to 44 usable ones, all `simple_lookup`, and you have no eval set at all.

**What I'd actually do:** stop the freeze, confirm with whoever owns the logging pipeline whether `query` is recoverable for `q0120`+. Everything else is downstream of that answer. I've written `curate.py` (plus `eval_set.csv` / `quarantine.csv` with per-row `drop_reason`) in the scratchpad — it applies a–d in order and is what you run *after* the re-export, not now.

## Q4 — How many per slice

Right now the per-slice numbers are this shaky (Wilson 95% CI, after removing contamination and dupes):

| slice | n | acc | 95% CI | width | 1 example = |
|---|---|---|---|---|---|
| simple_lookup | 1551 | 94.8% | 93.6–95.8 | 2.2 pts | 0.06 pts |
| multi_hop | 261 | 66.7% | 60.7–72.1 | 11.4 pts | 0.38 pts |
| ambiguous | 66 | 45.5% | 34.0–57.4 | **23.4 pts** | 1.49 pts |
| adversarial | 22 | 31.8% | 16.4–52.7 | **36.3 pts** | **4.55 pts** |

`adversarial` is unusable — one example flipping moves the score 4.5 points, and the true value is somewhere between "terrible" and "coin flip." `ambiguous` is nearly as bad.

The number depends on what you want the score to *do*:

- **Rank slices / find the weak one:** ~100 per slice (±10 pts). Enough to see 32% vs 67% is real.
- **Track a slice across releases and catch a meaningful regression:** **~350 per slice.** At p≈0.70 that gives 80% power to detect a 10-point drop. This is the number I'd budget for.
- **Catch a 5-point regression:** ~1,375 per slice. Usually not worth it — buy a better grader instead.

**Concrete recommendation: floor of 300–400 per slice, and don't report a per-slice score below n=100 at all** — emit "insufficient n" instead of a number, because a printed 31.8% will get quoted in a deck. That means sourcing roughly **340 more `adversarial` and 300 more `ambiguous`** examples. Those are your rare, high-value slices; oversample them deliberately rather than waiting for traffic to produce them.

One more thing you'll want to fix at the same time: `simple_lookup` is 82% of rows, so your headline accuracy of **88.7%** is really just the easy slice. The unweighted average across the four slices is **60.0%**. Report macro-average alongside per-slice, and keep traffic-weighted as a separate production-health metric — don't let one number serve both jobs.