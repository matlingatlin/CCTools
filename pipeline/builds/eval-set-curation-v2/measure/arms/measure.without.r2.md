Read the file and computed everything from it. Three files are attached: the eval set, the excluded rows with reasons, and the seeded build script.

**What's actually in the file** (2000 rows, all ids unique):

| slice | n | share | accuracy | in few-shot |
|---|---|---|---|---|
| simple_lookup | 1647 | 82.35% | 94.72% | 33 |
| multi_hop | 264 | 13.20% | 67.05% | 3 |
| ambiguous | 67 | 3.35% | 46.27% | 1 |
| adversarial | 22 | 1.10% | 31.82% | 0 |
| **all** | **2000** | | **88.75%** | **37** |

Two structural facts that drive every answer below: the file is 82% one easy slice, and only 1940 of the 2000 queries are distinct.

## Q1 — The 200 rows, and what the choice costs

I did not sample proportionally. Proportional-to-traffic gives you 163 / 27 / 7 / 3, which means the adversarial "score" is 3 examples — a coin flip you'd be reading as a number. I took a disproportionate stratified sample from the cleaned pool (1898 rows after the Q3 exclusions), seed 20260902:

| slice | pool | taken | acc in set | 95% CI |
|---|---|---|---|---|
| adversarial | 22 | **22** (all) | 31.8% | ±19.5pp |
| ambiguous | 66 | **66** (all) | 45.5% | ±12.0pp |
| multi_hop | 261 | **56** | 67.9% | ±12.2pp |
| simple_lookup | 1549 | **56** | 94.6% | ±5.9pp |

Within simple_lookup I also forced one row per distinct query template, so the 56 rows cover 56 different intents rather than re-sampling the same six "how do i cancel the {plan} subscription" shapes. Sampling is done blind to the `correct` column — stratifying on correctness would bake the current model's accuracy into the set.

**Ship the reweighted number, not the raw mean.** Each row carries a `slice_weight`. The unweighted mean of this 200-row set is **64.0%** — that is not a regression, it is the sampling design. Reweighted: **88.77% ±5.14pp**, which reproduces the population figure.

**What it costs, concretely:**

- **Headline precision drops ~4×.** Scoring all 1898 clean rows gives ±1.27pp; this 200-row set gives ±5.14pp. You can no longer see a 3pp overall regression. If you need that, keep scoring the full log offline and use the 200 for iteration.
- **simple_lookup goes from ±1.1pp to ±5.9pp.** On a slice sitting at 94.6%, you'll miss anything smaller than about a 7pp drop. This is the deliberate trade: I spent precision on the slice that's saturated and bought coverage on the slices that move.
- **multi_hop goes from ±5.7pp to ±12.2pp.** Real loss. If multi_hop is your active work area, take 100 there and drop simple_lookup to 12 — the pool supports it.
- **No holdout remains for ambiguous or adversarial.** I took every clean row of both. There is nothing left to detect overfitting on those two slices, and any future v3 eval set will overlap this one. Unavoidable at these pool sizes — splitting 22 adversarial into 11/11 would be worse.

## Q2 — Is 88.75% trustworthy?

The arithmetic is right and I reproduce it exactly. As a number to ship on, no, for three separate reasons.

**It's contaminated.** 37 rows are flagged `in_fewshot_prompt=1` — the model was shown these in its own prompt. They score **97.3%** vs **88.6%** for everything else. That's the model reciting, not answering. Small effect on the total (removing them moves it to 88.59%) but it's free, unearned accuracy and it will silently inflate any prompt-engineering iteration you do against this file.

**It's a traffic-mix number wearing an eval-score costume.** 88.75% is ~95% × 0.82 plus a rounding error. It is almost entirely a readout of how much of your traffic is easy lookups. Two consequences:
- The model fails **68% of adversarial**, **54% of ambiguous**, and **33% of multi_hop** queries, and none of that is visible in 88.75%.
- The number will move when traffic mix moves, with no model change at all. If simple_lookup drops from 82% to 70% of traffic, the headline falls to ~85.6% and someone will open a regression bug against a model that didn't change.

**It has no error bar, and shipping needs a threshold, not a point.** ±1.4pp on the full file — fine — but nobody has said what bar 88.75% is being compared against. "Ship on 88.75%" is only meaningful as "ship if ≥ X."

**What I'd say to the reporter:** the number is real but it isn't a quality bar. Ship criteria should be per-slice floors — e.g. simple_lookup ≥93%, multi_hop ≥65%, ambiguous and adversarial reported but not gating until we have enough data — plus the reweighted headline as a summary. And 88.75% computed on a file the model was partly prompted with should never be the ship number regardless.

## Q3 — What must be removed before freezing

102 rows, listed with reasons in `excluded_rows.csv`. Four categories, in priority order:

1. **37 few-shot-contaminated rows** (`in_fewshot_prompt=1`). Non-negotiable — these are in the model's prompt. Delete, don't just down-weight.
2. **4 untagged twins of few-shot rows.** Two duplicate pairs contain a flagged row and an unflagged one with identical text (`q0001`/`q0011`, `q0067`/`q0077`). The flag is per-row, so the twin is contaminated but unmarked. Anything text-identical to a prompt example has to go, whatever its flag says. **This means the `in_fewshot_prompt` column undercounts contamination — dedupe first, then re-derive the flag by text match against the actual prompt.**
3. **10 rows in 5 duplicate pairs with conflicting labels** — same query, opposite `correct`. Examples: `q0009`/`q0019` "what is the the pro balance on my account" (1 vs 0), `q0031`/`q0021` "how do i cancel the basic subscription" (1 vs 0). One label in each pair is wrong and I can't tell which from the file. Pull all 10 for human adjudication rather than guessing; they'll be worth re-adding once labeled.
4. **55 exact-duplicate rows** (60 duplicate groups total, all simple_lookup, all size 2, minus the 5 conflicting pairs already handled). Duplicates silently double-weight whatever they contain.

**Two more things I'd fix before freezing, that aren't row deletions:**

- **1880 of 2000 queries have no content.** They read `simple_lookup case 970 89fcd07f` — placeholder text, not queries. Only 120 rows contain anything a model could actually answer. If this is fixture data standing in for real logs, fine, but this file cannot be frozen as an eval set: there is nothing to evaluate. Confirm before proceeding.
- **Those 120 real rows are 6 intents, not 120 examples.** They decompose exactly as 6 templates × 10 plan slots × 2 copies: *cancel subscription*, *reset password*, *refund timing*, *change billing address*, *warranty coverage*, *account balance*. Several also carry a duplicated-article typo ("the the"). Treat these as ~6 test cases with paraphrase variants — scoring them as 120 independent trials overstates your evidence by roughly 20×.

## Q4 — How many per slice before a per-slice score means anything

Depends on what you're asking the score to do. Three different bars:

**To read a level** (95% CI, binomial):

| target | p≈0.5 | p≈0.7 | p≈0.9 | p≈0.95 |
|---|---|---|---|---|
| ±10pp | 97 | 81 | 35 | 19 |
| ±7.5pp | 171 | 144 | 62 | 33 |
| ±5pp | 385 | 323 | 139 | 73 |

Note the asymmetry: a saturated slice is cheap to measure, a coin-flip slice is expensive. adversarial at ~32% is the worst case in this file.

**To detect a regression between two model versions** — this is what an eval set is actually for, and it's much cheaper because it's paired. You score both versions on the same rows and only the rows where they *disagree* carry information. With ~20% discordance: **~157 per slice to catch a 10pp shift**, ~628 for 5pp, ~1743 for 3pp. Discordance rate is the lever — measure yours from your first two runs rather than assuming 20%.

**Working thresholds I'd adopt:**

| n per slice | what it's good for |
|---|---|
| < 30 | smoke test only. Report "3/22 failed," never a percentage. |
| 30–100 | directional. ±10–20pp. Catches catastrophes, not regressions. |
| 100–300 | a real per-slice metric. ±5–10pp; can gate a release. |
| 300+ | fine-grained. ±3–5pp; can arbitrate close A/B calls. |

**Against those thresholds, this file supports exactly one gating slice.** multi_hop (261 clean) qualifies. simple_lookup (1549) is over-supplied and I'd cap it at ~150 and spend nothing more. ambiguous (66) is directional at best. adversarial (22) is a smoke test — 22 rows on a 32%-accuracy slice gives ±19.5pp, so it cannot distinguish 32% from 50%, and reporting "31.8% on adversarial" implies a precision that isn't there.

**Concrete ask:** to make ambiguous and adversarial gate-able at ±10pp you need roughly **100 ambiguous** and **100 adversarial** examples, i.e. ~35 and ~80 net new ones. Adversarial is 1.1% of logged traffic, so you will not get 80 more by waiting — they need to be written or adversarially mined, which is a labeling project, not a sampling one. That is the single highest-leverage thing on this list: the slices where the assistant fails two-thirds of the time are the ones you currently cannot measure.