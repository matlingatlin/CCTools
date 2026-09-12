# abstention-threshold-design-v2 — rebuilding a skill that already existed

2026-09-01. Package origin `existing-artifact`: an incumbent at
`.claude/skills/abstention-threshold-design/` with a 128-line body, zero sources, zero URLs
and no executed evals. The package's eleven claims were fetched separately; none of them came
from it.

## Verdict: ship

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats, every test | pass | 4 tests × 2 repeats × 2 arms |
| no correctness regression | pass | none in 16 paired rows |
| tokens | pass | 353,517 vs 307,545 = **1.15×** (cap 1.20×) |
| tool calls | pass | 5.5 vs 5.0 = **1.10×** (cap 1.20×) |
| ≥1 win surviving both repeats | pass | **Q1 and Q2**, correctness, both repeats |

`chain_report`: **chain complete — every v1 phase left an event.** 36 dispatched runs, all
timed; `cost_gate` returns empty.

## What scout returned, and why

**extend.** The only unit in the library whose scope is the candidate sentence is the
incumbent: `selective` returns it alone across 90 skills, `abstention` returns it plus
`preregistered-decision-rule`, which disclaims the confidence-cut job in its own NOT-clause.
`author` would have produced a second unit owning the same six trigger terms. `reuse` asserts
the incumbent is fit as it stands — a claim about quality that nothing in the library
supported and that the package denies with `gap_kind: wrong-shaped`. One measurable fact was
already available: the incumbent's description is 1,360 characters against a 1,024 cap, so it
would fail `desc.max` today. Its own `evals.md` states that figure as 1,226.

## What the extend gate said

**1.1b: UNDECIDABLE, exit 2.**

> "no stored baseline for the incumbent, so nothing here can be called a regression. An
> unmeasured incumbent read as 'no regressions' is the flattering reading; the honest one is
> that this skill cannot be extended until its current behaviour is measured."

What was on disk was `evals.md`: eleven scenarios, every one ending *PASS. Beats baseline.*
They were **not** entered as results. The file states its own method — the tester judged *the
likely output* of an agent with and without the method; no run was executed and no output was
captured. Entering eleven predictions as eleven measurements is the substitution the gate
exists to refuse, and it would have turned them into eleven blockable regressions.

The gate names its own remedy, so the remedy was taken rather than the gate worked around:
**phase 6.1 ran the incumbent as a third arm**, same four tests, same two repeats, same
conditions. The gate was re-run on executed rows and returned **CLEAR** — 0 regressions,
0 dropped, **3 fixed**. Incumbent 5/8, rebuild 8/8.

## The probe partly refuted the package, and that is the most useful thing in this build

The package predicted a baseline that "picks a round number". It does not.

- Given a tool, 2 of 2 baseline runs computed the full precision–coverage curve correctly.
- 4 of 4 refused the round-number auto-approve, **and gave the calibration reason** rather
  than the number-too-low reason — the exact `artifact_expected` for representative task 3.
- 4 of 4 refused to cut a chance-level signal at 6.1, one of them reaching it by correlation
  rather than AUROC.

So Q3 and Q4 did not discriminate **at all**, in either the probe or the measurement. Nine of
seventeen expectations never separated the arms. The whole verdict rests on Q1 and Q2.

What the baseline does not do, in any of ten runs across probe and measurement:

| | observed |
| --- | --- |
| **F1** the recommended cut is never the maximum-coverage cut meeting the target, and the coverage given away is never priced | probe 3/4, measurement 2/2 |
| **F2** the precision target is invented in the agent's own voice; no floor, no owner | probe 4/4, measurement 2/2 |
| **F3** the score is thresholded without checking it separates | probe 4/4 |
| **F4** a coverage band is guessed when no distribution was supplied | probe 4/4, measurement 2/2 |

## Where the three arms actually differ

The fixture's maximum-coverage cut meeting 95% precision is **score ≥ 0.506** — 111 answered
of 200, 106 correct, 95.50%, 55.5% coverage.

| arm | Q2 repeat 1 | Q2 repeat 2 |
| --- | --- | --- |
| without | 0.60 (40% coverage) | 0.60 (40%) |
| incumbent | 0.52 (51%) | 0.55 (47%) |
| **with** | **0.506 (55.5%)** | **0.506 (55.5%)** |

Every arm computed the curve correctly. Every arm named the crossing row. Two of the three
then recommended a cushion above it and priced nothing. The incumbent does this **in direct
contradiction of its own step 6**, which says to take the highest-coverage row — a rule
written and not obeyed, 2 of 2. That is the finding this build exists to have produced, and it
was not visible from reading either file.

On Q1 the with-arm refuses to state a coverage figure 2 of 2 and marks its own proposed
numbers unagreed: *"Both numbers above are proposed by me, unagreed — needs an owner and a
date before they're binding."* The baseline gives a band 2 of 2.

## The grader was checked before it was believed

A real with-arm Q2 answer with exactly one change — the recommended cut moved off the
maximum-coverage row — went into both grading packets unlabelled. Both graders ruled it
INCORRECT and both named Q2 E2, at different positions in a per-question reshuffle. **CAUGHT,
twice.** It is believed on that class and no other.

`calibrate.py` was not used: all five of its defect kinds mutate a *skill artefact*
(frontmatter, fetch dates, block quotes, percentages, NOT-clauses) and none applies to an
answer transcript. Recorded as a deviation.

## Two reds that were the TEST, not the skill

Triaged at 7.2 before anything was repaired, because the default without that step is that
the skill is what gets fixed.

1. The first steps reader reported **every bundled file missing**. It had been given
   `SKILL.md` copied alone into a scratch directory; `body.files-exist` and `ptr.resolves`
   both passed on the same artefact in the same minute.
2. `triggers.py` first scored **0 of 12 positives as no-fires**. It defaults the target to the
   *package* id (`…-v2`) and the router had chosen `abstention-threshold-design` every time.
   Taken at face value this reports a unit that cannot be reached at all, and the repair would
   have been aimed at a description that was working.

## The reader loop cost six rounds to buy one sweep

The references file took six rewrites to reach 0 red. Every round from 1 to 6 found a **new
instance of the same two defect classes in a different entry**, because each prompt named what
the last round found and the reader spot-checked that. Round 6 asked for an entry-by-entry
sweep of all eleven claims against both classes; round 7 — the first prompt to say *a review
that must find something is not a review* — returned 0 red. Both changes are worth carrying
into the next build.

Rewrite counts: bill of materials 4, references 6, steps 3, description 2, pointers 1, whole
artefact 2. Name, what-and-when and frontmatter: 0.

## What is NOT settled

- **`desc.target` is left red.** 1,006 characters against a 500 target — a warning, not an
  error, and the incumbent's 1,360 is an error. The reader proposed cutting two package
  trigger terms; six siblings need NOT-clauses and those alone are 344 characters. 6.5 then
  showed the cut that *was* made cost nothing: the query *selective prediction* still routed
  here after the phrase was removed from the description.
- **The eleven claims were not re-verified** by this build. 3.4 was skipped because 3.3
  gathered nothing. The package carries per-claim quotes and a `verified_by` line; if a quote
  there is wrong, the same quote is wrong in `references/`.
- **Three claim verdicts are disputed and left disputed.** C5, C10 and C11 carry `MEASURED`
  while their own Limits lines say no number is reported. The dispute is written into the
  reference file's *How to read a verdict* rather than settled by overruling a verdict this
  build did not earn the right to overrule.
- **No field trial.** 6.6 was skipped: no instance of this job exists outside the eval set
  here. Both fixtures are synthetic, seeded, and built by this build — so the cut the with-arm
  is measured on finding is a cut this build placed there.
- **Stage 2 was not run.** Nothing was borderline, so 4 tests stand rather than 20.
- **Not deployed.** Reserved by the coordinator. `.claude/skills/` was not touched.

## What deployment still owes

- The capability-map entry in `CLAUDE.md` still describes the incumbent.
- `pipeline/ROUTING.md` was not checked for chains naming this skill.
- The incumbent's `evals.md` — eleven authored predictions with no executed run behind them —
  would sit beside a new `evals/evals.json` unless it is removed. The executed replacement is
  `pipeline/builds/abstention-threshold-design-v2/measure/rows.json`.
