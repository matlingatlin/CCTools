# Phase 2.2 — what the four baseline runs actually did

Four runs, no skill present, fresh sessions, opus tier, in a bare working directory
outside this repo (verified: a `claude -p` session started there lists 24 host skills and
none of this library's — `eval-set-curation` is not among them). Each was given the PATH
to a sanitised copy of the fixture and nothing pasted inline.

Task set A (Q1 pick the 200 / Q2 is 88.75% trustworthy) x 2 repeats.
Task set B (Q3 what must be removed / Q4 how many per slice) x 2 repeats.

## The prediction, and what happened to it

The package's `expected_failure` reads:

> Asked which 200 of 2000 logged cases to evaluate on, the baseline samples at random or by
> convenience, reports a single headline accuracy, and does not check whether the rare slices
> it cares about received enough examples to measure.

**REFUTED, 4 of 4.** No run sampled at random. No run reported a single headline accuracy.
Every run computed the per-slice accuracy table unprompted, and three of four computed Wilson
confidence intervals per slice and said in their own words that `adversarial` at n=22 is not
measurable. probe.B.without.r1 called it "not a measurement — it's a rumor". The package's own
note says this hypothesis has now been refuted in 3 of 3 builds; this is the fourth, and again
it was written from the solution's point of view.

What the baseline is actually bad at is narrower, and it is not what anyone predicted.

## The failures, coded from what the runs did

Quotations are verbatim from the run outputs in this directory.

### F1 — near-duplicate collapse stops at exact match. 3 of 4.

Ground truth (computed from the fixture, not from any run): the 120 rows `q0000`-`q0119`
are **60 distinct strings drawn from 6 templates** — six intents wearing sixty costumes.
Collapsing to 60 removes the exact repeats and leaves the paraphrase family intact.

- `probe.B.without.r1`: "Drop the second copy of each — **60 rows**." Frames the remainder as
  clean and moves on to the next removal.
- `probe.A.without.r2`: "dropping both copies of the 5 conflicting pairs, and **keeping one
  copy of the other 55**".
- `probe.B.without.r2`: "60 exact-duplicate query pairs (120 rows → **drop 54, quarantine 10**)".
- `probe.A.without.r1` is the exception and did the thing: "**Collapse near-duplicates, not
  just exact matches** ... 120 rows → 60 exact-distinct → **8 clusters** after normalizing ...
  They are six question templates ... filled with ten plan names. A 15:1 collapse."

Three of four stop one step early, and every one of them stops at the same step. The run that
did not stop is the only one that named the distinction out loud before doing it. Note that
even the good run over-split (8 clusters where there are 6) because of a `"the the"` artefact
in the fixture — the direction is right, the count is not exact.

### F2 — the holdout is a pool, not a seal. 3 of 4.

- `probe.A.without.r2`: "The 1699 unused rows are in `heldout_pool.csv` — **usable as a dev
  set**". A pool that may be used as a dev set is not a holdout; nothing seals it, nothing
  budgets a look, nothing logs one.
- `probe.B.without.r1` and `probe.B.without.r2` produce no dev/holdout split at all. (Their
  task set did not ask for one, so this is weak evidence from those two — recorded as such.)
- `probe.A.without.r1` again the exception: "open `eval_holdout_80.csv` **once**, to confirm a
  decision already made, and **log the date and reason. Every look burns it.**"

### F3 — the per-slice floor is a round number, not an interval. 4 of 4.

Every run computed the per-slice Wilson interval correctly. Every run then set the cut with a
number that came from nowhere in the data, and no two runs agreed:

| run | the floor it adopted | where the number came from |
|---|---|---|
| `probe.B.without.r1` | "n ≥ 100 to print a number at all", "n ≈ 200 as the build target" | asserted |
| `probe.B.without.r2` | "floor of 300–400 per slice", "don't report below n=100" | asserted |
| `probe.A.without.r1` | "the practical floor is ~30" | asserted |
| `probe.A.without.r2` | no floor stated; reports the CIs and stops | — |

Three runs, three different floors — 30, 200 and 350 — from identical data, each stated in the
run's own voice as though it were established. `probe.B.without.r2` even ran a power
calculation and then rounded its own result to "300–400". The arithmetic is not the gap. The
gap is that the cut is not sourced.

### What the baseline does NOT get wrong — recorded so nothing is written to fix it

- **Contamination.** 4 of 4 found all 37 `in_fewshot_prompt=1` rows, quantified the inflation
  (97.3% vs 88.6%) and removed rather than down-weighted them. No step needed.
- **Per-slice reporting.** 4 of 4 produced the slice table unprompted and refused the pooled
  number. `probe.A.without.r2`: "Everything that isn't simple_lookup runs at 60.5%".
- **The rare slice is not measurable.** 4 of 4 said so, in their own words, without being
  asked. `probe.B.without.r1`: "It is not a measurement — it's a rumor."
- **Stratification with deliberate over-sampling.** `probe.A.without.r1` and
  `probe.A.without.r2` both did it and both priced the trade-off in points of headline
  precision. This is the package's `expected_failure` and it did not happen once.

### A defect in the FIXTURE, not in any run. 4 of 4 flagged it.

1880 of 2000 rows carry placeholder query text of the form `simple_lookup case 970 89fcd07f`,
which contains its own slice label. Every run found it and two called for the freeze to stop
until it was resolved. `probe.B.without.r2`: "the query string *contains its own slice label*.
Any grader or model that reads it gets the answer key for free." This is a real property of
`pipeline/packages/fixtures/eval-set-curation-v2/generate.py` and it is carried into phase 7.2
as a **test bug**, not a skill bug.
