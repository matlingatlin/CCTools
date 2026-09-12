I read the file and computed everything below from it directly.

## What's actually in the file

```
2000 rows, 0 duplicate ids, no empty fields, 4 valid slice labels

slice            n      %      accuracy
simple_lookup   1647  82.3%    0.947
multi_hop        264  13.2%    0.670
ambiguous         67   3.4%    0.463
adversarial       22   1.1%    0.318
                                overall 0.888
```

---

# Q3. What has to be removed before you freeze this

Five things, in descending order of how badly they'd corrupt the score.

### 1. The 37 few-shot-contaminated rows (`in_fewshot_prompt = 1`) — remove, non-negotiable

These are items the model was shown the answer to in its own prompt. They score much higher, exactly as you'd expect:

```
                 in prompt        clean
simple_lookup    33  0.970    1614  0.947
multi_hop         3  1.000     261  0.667
ambiguous         1  1.000      66  0.455
adversarial       0     —       22  0.318
                 37  0.973    1963  0.886
```

Note where they land: 33 of 37 sit in the slice that's already 82% of the file, and one sits in `ambiguous`, where a single leaked item is 1.5% of the slice and moves that score by ~0.8pp on its own. Drop all 37 by filtering the column, then **delete the column** from the frozen file so nobody re-derives a score with them included.

### 2. 60 duplicate rows from a logging bug — remove

60 queries each appear exactly twice. This isn't real repeat traffic: **every pair has an id offset of exactly 10** (`q0009`/`q0019`, `q0054`/`q0044`, `q0100`/`q0110`, …). That's a double-write in the export, not two users asking the same thing. All 120 rows involved are in `simple_lookup`.

Drop the second copy of each — 60 rows. If you leave them, those 60 queries get double weight in the slice they're already over-representing.

### 3. 5 pairs where the duplicate rows disagree on `correct` — resolve or drop both

Of those 60 pairs, 5 have the same query text graded both 1 and 0:

```
q0054/q0044  when will the the trial refund arrive
q0031/q0021  how do i cancel the basic subscription
q0088/q0098  is our team covered by the warranty
q0100/q0110  change my billing address to premium
q0009/q0019  what is the the pro balance on my account
```

Identical input, opposite grade. Either the grader is nondeterministic or the model is — either way the label is not trustworthy for those items. **Hand-grade all 5 and keep the correct verdict.** If nobody has time, drop both copies (10 rows) rather than coin-flipping which one to keep.

That's **101 rows removed**, leaving 1899:

```
simple_lookup   1550   0.948
multi_hop        261   0.667
ambiguous         66   0.455
adversarial       22   0.318
```

### 4. `correct` is not ground truth — it must not be frozen as the label

This is the one that will quietly ruin the eval set if you skip it. `correct` is the *current* model's grade on that item. Freeze it as the answer key and every future version is scored on "did it agree with the incumbent," which caps every model at the incumbent's behavior and makes genuine improvements register as regressions.

Before freezing: each retained item needs a **reference answer written independently of what the model said**. Keep `correct` if you like, but rename it `baseline_v1_correct` and treat it as a historical result column, not a key.

### 5. 1880 of 2000 rows carry no answerable query text — this blocks the freeze

Only 120 rows are natural language. The other 1880 are template placeholders of the form `simple_lookup case 970 89fcd07f` (unique case numbers, unique hash suffixes, no collisions — machine-generated, not logged). And the split is total:

```
                 real text   placeholder
simple_lookup       120         1527
multi_hop             0          264
ambiguous             0           67
adversarial           0           22
```

**Every single non-`simple_lookup` row is a placeholder.** You cannot write a reference answer for `adversarial case 41 b2c9e10f` — there is no question in it. So after steps 1–4 the set of items you can actually freeze is: 60 unique real queries, all `simple_lookup`, and nothing else.

Either the export is broken and needs re-running, or the fixture was generated rather than sampled. Find out which before doing any of the work above, because if it's the export, steps 1–3 need redoing on the real data.

### One thing to fix that isn't a removal

Don't rebalance by deletion, but be aware: at 82% `simple_lookup`, the headline 88.8% is essentially the `simple_lookup` score wearing a disguise. Equal-weighted across the four slices the same data reads **~59.7%**. Report per-slice scores as the primary metric; if you want one number, use the slice-weighted mean with weights you chose deliberately, not the ones traffic happened to hand you.

---

# Q4. How many per slice before a per-slice score means anything

### Where you are now (Wilson 95% CIs, post-cleanup)

```
simple_lookup   n=1550  0.948  [0.936, 0.958]   ±1.1pp
multi_hop       n= 261  0.667  [0.607, 0.721]   ±5.7pp
ambiguous       n=  66  0.455  [0.340, 0.574]  ±11.7pp
adversarial     n=  22  0.318  [0.164, 0.527]  ±18.2pp
```

The adversarial score is compatible with anything from 16% to 53%. It is not a measurement — it's a rumor. Two consecutive runs of an unchanged model could plausibly print 27% and 45%.

### The thresholds I'd actually adopt

**n ≥ 100 to print a number at all.** At worst case that's ±10pp. Below 100, publish the raw fraction ("7/22") and no percentage — a percentage on n=22 invites people to compare it week over week, which is exactly the mistake.

**n ≈ 200 as the build target.** ±7pp, and it's the point where the cost per slice is still reasonable.

**Sizing for the question you're really asking** — you don't care about the absolute score, you care about catching a regression between versions. Because you run both versions on the *same* frozen set, use the paired test (McNemar), which is much cheaper than the unpaired numbers people usually quote. Assuming ~20% of items flip between versions:

```
regression to detect     paired n/slice    unpaired n/slice/arm
20pp                          40                   98
15pp                          70                  175
10pp                         157                  392
 5pp                         628                1568
```

So **n=200 per slice catches ~10pp regressions reliably**. If you want to catch 5pp you need ~600+ per slice and should say so out loud rather than pretending n=200 can do it.

### The concrete build order

Target 200 per slice, 800 total:

```
adversarial     22 → 200    author 178 new items   ← do this first
ambiguous       66 → 200    author 134 new items
multi_hop      261 → 200    downsample (random, seeded), keep the rest as holdout
simple_lookup 1550 → 200    downsample, keep the rest as holdout
```

Three things about that build:

- **The new items must be genuinely new.** Not paraphrases, not resampled from the same 60 templates. Near-duplicates inflate n without adding information — your CI narrows while your actual coverage doesn't, which is worse than a small honest set.
- **You can't source them from this file.** There are zero real `adversarial`, `ambiguous`, or `multi_hop` queries in it. This is a mining-and-authoring job against real traffic, not a curation job.
- **Freeze `simple_lookup` and `multi_hop` down to 200, don't delete the remainder** — hold them out as a refresh pool for when the frozen set gets overfit.

### Reporting rules to adopt alongside it

- Every per-slice score ships with its Wilson CI. No bare percentages.
- Version-over-version comparisons use McNemar on the paired items, not overlapping CIs by eye — overlapping CIs are not a null result.
- Never compare one slice's score to another's (`adversarial` 32% vs `multi_hop` 67% is meaningless when the intervals are ±18 and ±6).
- Re-run the contamination check (step 1) on every eval run, not once. Few-shot prompts change, and the moment someone adds an example that happens to be in the set, that slice's score silently drifts up.