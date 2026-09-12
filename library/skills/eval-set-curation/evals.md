# Evals — eval-set-curation (candidate, build `eval-set-curation-v2`)

**Verdict: ITERATE.** These scenarios were EXECUTED, not predicted. That distinction is the
reason this build exists: the incumbent's `evals.md` recorded 11 scenarios and 11/11 passed, and
every one of those results was an agent's judgement of what a run *would* do. Nothing here is a
prediction.

## Method

Three arms, two repeats each, all at the same model tier, all fresh sessions in bare working
directories outside the repo, all given the fixture as a PATH:

| arm | what it had |
|---|---|
| **with** | this candidate's SKILL.md pasted, plus paths to its references and asset on disk |
| **incumbent** | the shipped `.claude/skills/eval-set-curation/SKILL.md` pasted |
| **without** | nothing |

Outputs were blinded and reordered under a withheld key BEFORE the judged half of the expectation
set was written. Two independent graders, neither of which saw the skill, the references, the
asset, the bill of materials or the key. Un-blinded against a control a swapped key would fail.

Two of the eight dispatched arm runs returned no answer — they invented a file-attachment
affordance — and were re-run with one added sentence about the output channel. Those two are in
`measure/void/` and are excluded; the asymmetry (two of eight saw one extra sentence) is recorded.

## Result — expectations met, by arm

| arm | repeat 1 | repeat 2 | mean |
|---|---|---|---|
| **with** | 97.4% | 90.3% | **93.8%** |
| incumbent | 66.7% | 66.7% | **66.7%** |
| without | 41.2% | 52.9% | **47.1%** |

19 expectations: 8 computed from the fixture and written before any arm output existed, 11 judged
from the blinded copies. The graders agreed on 113 of 114 cells.

## Per-scenario

| # | scenario | kind | carries | with | incumbent | without |
|---|---|---|---|---|---|---|
| E1 | Pick the 200 rows that become our eval set, and tell us what the choice costs | normal | F1 + the stratification half of F3 | 2/2 correct, 2/2 shape | 2/2 correct, **0/2 shape** | **0/2 correct**, 0/2 shape |
| E2 | Someone reports 88.75 percent accuracy and wants to ship. Is that trustworthy? | normal, **regression guard** | no failure — the baseline passes it 4 of 4 and the skill may not lose it | 2/2, 2/2 | 2/2, 2/2 | 2/2, 2/2 |
| E3 | Before we freeze this as an eval set, what has to be removed? | clever / edge | F1 alone — 3 of 4 probe runs failed it identically | 2/2 correct, 1/2 shape | 2/2 correct, **0/2 shape** | **1/2 correct**, 0/2 shape |
| E4 | How many examples per slice before a per-slice score means anything? | clever / edge | F3 | 2/2, 2/2 | 2/2, **0/2 shape** | 2/2, **0/2 shape** |
| E5 | We launch next month and have no production traffic at all yet | **negative-trigger** | must NOT route here | routed to `synthetic-eval-data-generation` | — | — |

`correct` = no fixture-computed expectation for that question graded NOT MET by either grader.
`shape_ok` = no judged expectation for that question graded NOT MET by either grader. The stricter
grader is taken on every cell, so grader generosity cannot manufacture a win.

**E2 held.** The regression guard is the only scenario all three arms pass on both axes, which is
what it is for: the skill teaches three new behaviours and did not lose a fourth that already worked.

## Routing (phase 6.5)

12/12 positives routed to `eval-set-curation` (floor 80%), **0 of 6** near misses mis-routed, and
**6 of 6** near misses reached the sibling they belong to. Near-miss queries were hand-written, one
per sibling, because an empty near-miss set makes the mis-fire rate unmeasured rather than zero.

## Why the verdict is ITERATE and not ship

Every quality clause of the preregistered rule passed — zero correctness regressions, and wins on
Q1 correctness and Q4 shape that survived every repeat. **Both cost clauses failed:** 1.84x tokens
and 1.39x tool calls against a 1.20x cap fixed before any number existed.

Triaged as a **skill bug, not a test bug**. The pasted method body accounts for about 1 percent of
the token gap; the incumbent arm carries a body of comparable size and is *cheaper* than the bare
arm (0.67x). The cost is the work the steps ask for — labelling ~50 pairs, writing a normalisation
list, inverting a tolerance and stating its p, filling a seven-section record. The method earns its
win by doing more, and the rule says it must earn it for less than 1.2x.

## What these evals do NOT test

- **F2 (a holdout that is a pool, not a seal) has no eval of its own.** The candidate's step 3 is
  the least-tested of its three steps. Nothing here observes a holdout being *reused*.
- **No real instance.** Every run was on a seeded fixture. The fixture's own near-duplicate ground
  truth turned out to be wrong under this skill's step 1, which is a warning about planted fixtures
  in general.
- **The grader was never calibrated against a planted defect.**
