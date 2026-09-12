# The skill-builder's own three skills — acceptance run

2026-08-30. **24 agents, 1,876 s measured wall clock.** 20 arm-runs, 10 graders, two rounds.

## All three ship

| | verdict | wins surviving both repeats | tokens | tool calls |
| --- | --- | --- | --- | --- |
| `skill-knowledge` | ship | Q3, Q4, Q5 — **Q5 discounted** | 1.05× | **0.80×** |
| `skill-contract` | ship | Q1 | 1.08× | 1.00× |
| `skill-measure` | ship | Q4 only | 1.03× | 1.00× |

Every clause of the contract's default rule passes for all three, cost included. No
correctness regression anywhere across 48 paired question-repeats.

## What the run actually taught, which is not the table

**A skill's demonstrated contribution is usually one clause, not the file.** `skill-measure`
separated the arms on exactly one question — calibrating the grader against a planted defect.
Every other measurement discipline the baseline already had: refusing n=1, computing the
delta, refusing a win that did not repeat. The honest read is *the model already holds most
of this and does not calibrate its grader.* Whether the undifferentiated sections are
redundant or merely untested is **not settled** — several shared passes sit on expectations
the graders call near-unfailable, and those are different states.

**The expectations were the weakest part of the whole system, twice.** Round 1's set was
recitable and both graders said so independently; it was discarded as a verdict rather than
adjusted, and re-run. Round 2's set is far better — the baseline drops from 1/5 to 0/4 on
`skill-contract` — and still has named defects: entailed expectations that score one
competence twice, prohibitions that reward silence, and house vocabulary that scores label
matching. Every one was found by the graders, because the method requires them to attack the
set. **That instruction earned more than any other single line in this harness.**

**The sharpest criticism is one nobody has acted on yet.** For `skill-contract`: *"none of
them scores the artefact against the failure the probe documented … none asks whether the
produced file would have caught the miss."* The question supplies two observed failures and
never checks the artefact against them. That is round 3's first job.

## Harness defects found, and the one that nearly inverted a result

Three bugs, all in the artefact question, all in code written the same day. The section
parser split on the answer's own headings; fence-awareness did not fix it because the winning
answer wrote its file unfenced; and the code grader punished the more complete answer for
bundling a file the checker could not see. Before the fixes the harness scored a complete,
contract-clean SKILL.md as *nothing*.

`selftest_score.py` exists to prevent exactly an inverted conclusion, and it passed
throughout — the inversion was one stage upstream of what it watches. **A control proves the
thing it watches and nothing else.**

Caught only because a surprising per-question result was checked against the raw file before
being written down.

## What was not checked

- **The graders were never calibrated against a planted defect** (phase 6.3, v2). For
  `skill-measure` this is circular: the measurement of grader blindness was made by a grader
  whose blindness is unmeasured.
- **Trigger firing** (phase 6.5, v2). Nothing here shows these skills would be *selected*.
- **Part of every token delta is the method text the `with` arm was handed** and the other
  was not. `subagent_tokens` does not separate input from work.
- **The `without` arm had this repo's 84 existing skills available.** That is deliberate —
  the question is whether these beat what we have — but whether any fired was recorded per
  run in `## consulted` and not analysed.
- `tokens_est` in `metrics.jsonl` sums the per-run figures; `spend_measured` stays null.
