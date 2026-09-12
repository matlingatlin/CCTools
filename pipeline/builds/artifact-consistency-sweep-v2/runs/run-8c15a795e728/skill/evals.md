# Evals — artifact-consistency-sweep

**Talent:** `artifact-consistency-sweep` · **Type:** technique, shape-graded · **Last eval:** 2026-09-03, the second v3 build (`pipeline/builds/artifact-consistency-sweep`: bare-baseline probes, with/without arms, code grader against the union of three independent reviews per fixture, three repair rounds) · **Verdict:** ABANDON at the loop cap - no test cleared every grader check on both repeats; tool calls 1.21x against 1.20x. Status: candidate, not routed.

## What was measured

| fixture | baseline recall (probes) | with-arm recall, round 3 | CLASS recall with | what still failed |
|---|---|---|---|---|
| T1 (artifact-A) | 0.67 / 0.50 | **0.83 / 0.75** | 1.0 / 1.0 | the ledger check on both runs |
| T2 (artifact-B) | 0.64 / 0.64 | 0.82 / 0.64 | 0.5 / 0.5 | the ledger check; CLASS recall |
| T3 (artifact-C) | 0.29 / 0.57 | **1.00 / 0.71** | (0.67) | precision proxy and ledger; CLASS recall |

Trigger matrix PASS: 12/13 positives, 0/4 mis-fires, 4/4 near misses reached their sibling.
Field trial on the shipped `skill-measure` skill: a complete ledger (24/24 step x rule pairs), 7 findings (4 CLASS), and five gaps in the method it named itself (a rule defined by heading rather than function; no rule for a missing bill of materials; no quote rule for an unpointed file; no pair type for step x instance-section; and "six counts" naming seven things).

## Why abandon, in one line
The method lifts recall - the thing it was built for - and the grader's full bar (ledger with pair ids, precision proxy, CLASS recall 0.70 on every fixture) was not cleared on any fixture twice. Three whole-artefact reviews were red at class level with real findings each time; the convergence cap stopped a fourth.

## Scenarios (executed as T1-T3; S4-S6 not executed)
- S1 sweep a text the first review saw — with 0.83/0.75, baseline 0.67/0.50
- S2 sweep a text after its first rewrite — with 0.82/0.64, baseline 0.64/0.64
- S3 sweep a text after its second rewrite — with 1.00/0.71, baseline 0.29/0.57
- S4 a runbook without expectations · not executed (the round-2 review named this gap)
- S5 a defect reported twice · graded by the no-shared-quotes check only
- S6 negative trigger · carried by the trigger matrix (0/4 mis-fires)

## Next iteration, if taken up
The field trial's five gaps (four in the method, one miscount) first; then the ledger as a top-level key the output contract names in every prompt; then a runbook fixture.
