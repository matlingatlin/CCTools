# Review — the skill-builder agent and its components

**Date:** 2026-09-02. **Basis:** three measured builds. **Verdict:** builds good skills, too
slowly and too unstably, and the instability is mostly in one component that does not exist yet.

## Can it run in ten minutes?

Not as built, and not because of concurrency. The dispatch floor is **28.3 minutes at infinite
agents**: probe 5.0 + whole-artefact review 4.4 + longest arm run 7.3 + grading 6.5 + triggers
0.3, in order, each block waiting on its longest run. Raising the agent cap from 2 to 4 was
measured at 3.4 minutes; refilling slots instead of dispatching in waves at 0.7.

A single arm run takes 4–7 minutes because it is an **agent, not a prompt**: it writes Python,
runs it over 8,000 rows, iterates. A prompt-only run would be seconds and would measure who
sounds wisest rather than who finds the unit change confined to one merchant.

Ten minutes requires measuring less. That is a different product, described at the end.

## Where the time goes

`eval-set-curation-v2`, the one clean build, 79.4 minutes:

| | min | share |
|---|---|---|
| coordinator authoring | 44.6 | 56% |
| coordinator planning + reading verdicts | 27.2 | 34% |
| coordinator waiting | 7.7 | 10% |

The chain contract has **39 phases, 21 of them `model`** — coordinator turns. Those ARE the 56%.
Sixteen phases are skippable, which says half the chain is conditional.

## Where the instability is

| component | state |
|---|---|
| **dispatch harness** | **Does not exist as a stable artefact.** Rewritten ad hoc per build. All three contaminations of 2026-09-02 — shared working directory, arm name in the path, `--add-dir` to every arm — were here, and none was visible to any gate. Build 3 ran **36 arm runs for 12 valid observations** because of it. |
| gates (15 validators) | Every gate added on 2026-09-01/02 had a defect a later build found: marker string, carve-out too narrow, two rules in mutual conflict, `cost_gate` clean without tokens. Five self-inflicted, roughly seven pre-existing. |
| chain contract (39 phases, 8 rule blocks) | Internally consistent, over-built. Two rules written the same evening contradicted each other. |
| agent file (149 lines) | Grew 70 lines in one night. Read every turn. |
| measurement design | **The one component working as designed.** Three arms, repeats, blind grading, an un-blinding control that a swapped key fails by construction. It caught every contamination — by reading output, never by a check. |

## The three builds

| build | wall | runs | dispatch | arm runs | note |
|---|---|---|---|---|---|
| abstention-threshold-design-v2 | 95m | 36 | 84m | 6 | shipped |
| eval-set-curation-v2 | 79m | 32 | 99m | 8 | ITERATE, shipped on override |
| data-contract-assertions-v2 | 517m | 84 | 287m | 36 | two rate limits, three arm waves, stopped at 6.4 |

## What the measurement established that outlives the builds

- A clean probe must never stop a build: the baseline produced **opposite behaviour on an identical
  prompt**, and the skill's job turned out to be making the good run reliable, not teaching a
  method the baseline lacked.
- `expected_failure` written from the solution's viewpoint is refuted **4 of 4**.
- Expectation power: 27% → 50% → 58% discriminating across three builds. The last grader called
  42% of its instrument inert, against a set that declared 21%.
- The agent cap was never the constraint: mean concurrency 1.37 against a cap of 2.
- Rules catch what is already known to be wrong. **Reading output catches what was not known.**
  Every expensive defect in build 3 was caught by the blinding-before-expectations ordering
  forcing a read, and by nothing else.

## Recommendation

**One addition.** A dispatch script written once: isolated per-run directory carrying no arm
string, per-arm access, usage payload captured. It is the only missing component and the only
source of rework.

**Freeze everything else.** No new gates, no new rules. The contract should shrink, not grow.

**Two modes.** *Full* — current measurement, realistically ~40 minutes once the harness is
stable. *Fast* — no probe, one arm, one grader, no incumbent, ~10–12 minutes. Fast gives up the
baseline comparison, which is the thing that makes a verdict mean something; it is for iteration,
not for ship decisions.
