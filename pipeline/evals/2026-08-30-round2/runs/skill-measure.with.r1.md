## Q1

**No-go on this evidence.** Not "it failed" — "this run cannot decide, and what it does show leans against the skill."

Two independent reasons:

1. **One run per cell cannot tell a tie from a small regression.** Five tasks x 1 repeat gives no variance at all. This is the clean-baseline case (5/5 without), which is precisely the case most likely to be made worse by an added artefact — roughly one task in seven regresses under an added skill, and regressions concentrate where the base model was already competent. A clean baseline raises the evidence bar; it does not lower it. Minimum for a ship decision here is 2 repeats, both arms of each repeat launched in the same turn.
2. **No named axis was won.** Correctness is 5/5 vs 5/5 — identical. The only axis with a difference is tokens, and the skill *loses* it: 12,400 vs 9,800 is **+26.5%**, over the usual 20% cap. So on the one measurable axis available, the result is a regression, not a win.

What has to happen before this can be re-decided:

- Name the axis the skill is supposed to win on, in writing, before the re-run (consistency? row-schema conformance? fewer missed findings on hard tasks?). "Correctness" is already saturated by the baseline and cannot show a win.
- Write the threshold with a number, a direction and a comparison set — e.g. "wins the named axis in both repeats on at least one task, loses it in none, token growth <= 20% median across paired repeats."
- Re-run 5 tasks x 2 arms x 2 repeats, paired in the same turn, fresh sessions, capturing tokens/tool calls/duration live.

If the re-run reproduces "identical correctness, +26% tokens," the answer is a permanent no-go: it is a pure cost with no measured benefit.

## Q2

Skill under test: makes a review agent emit a table with **one row per finding**.

### Stage 0 — probe, before a line of the skill is written

Run the five tasks below with **no artefact present**, fresh session each, **2 repeats** — 10 runs. Two repeats is the minimum that separates *failing* (every run misses the same thing) from *uneven* (some runs produce the table, some don't) from *clean* (every run acceptable, differences of style only). The middle case is the one that gets misfiled, and here it is the likely one — a review agent sometimes tabulates on its own.

Code each probe run as: the behaviour quoted from the transcript ("returned three prose paragraphs, no table"), the consequence ("findings cannot be counted or diffed"), and whether every run did it or only some. Nothing gets written into the skill until this coding exists.

### The five test prompts (prompts only — no expectations yet)

| id | prompt shape | why it is in the set |
| --- | --- | --- |
| T1 | review a ~60-line diff containing 3 clear defects | everyday / representative |
| T2 | review a file containing exactly **1** defect | does a one-row table survive, or does it collapse to prose |
| T3 | review a **clean** file, 0 defects | measured zero vs no table at all — the 0-vs-null trap in the artefact itself |
| T4 | review a ~400-line multi-file diff with ~12 defects, 3 of them near-duplicates | adversarial: does row-per-finding hold at volume, or do rows get merged/summarised |
| T5 | "explain what this module does" (no review asked for) | **negative trigger** — the skill must NOT impose a table |

Expectations are written **after** stage 1 outputs exist, from what the outputs actually contain.

### Stage 1 — the paired runs

**5 tests x 2 arms (with / without) x 2 repeats = 20 runs.** Both arms of a repeat launched **together, in the same turn**, fresh sessions. A baseline collected an hour earlier is a different machine under a different load and does not pair.

Per run, captured live (there is no second chance at these):

| field | note |
| --- | --- |
| test_id, repeat, arm | arm is with / without |
| artefact | the full output, kept verbatim — the expectations get written from it |
| tokens, tool_calls, duration_s | **null if not captured** — never 0, and never treated as fine |
| table_present | bool |
| row_count | integer; **0 is a measured zero** (T3), null if no table at all |
| finding_count | findings the grader counts in the prose/output, independent of rows |
| rows_equals_findings | bool — the actual claim of the skill |
| schema_ok | required columns present, one finding per row, no merged rows |
| correct | bool, or **absent if nobody ruled** — absent is not false |

### Stage 2 — only if stage 1 is borderline

Expand to 20 tests, same 2 arms / 2 repeats. Do not expand a clear result.

### The grader, checked before it is believed

Build one calibration specimen from a **real** T4 with-arm output, altered in exactly **one** place, in the class most needing to be caught: take a correct 12-row table and **merge two findings into a single row** (row_count 11, finding_count 12). One defect, not several — with several you learn only that the grader found *something*. Hand it to the grader blind, mixed into the batch. If the grader returns "no findings" on the specimen it is blind to its own planted class, and its verdicts on the other 20 runs are discarded until it is fixed. The grader is also asked to attack the expectations themselves — whoever wrote them cannot rule on whether they were the right ones.

### The threshold, written now, before any result is visible

> rows_equals_findings true in **both** repeats for T1, T2 and T4 in the with-arm, and true in **strictly fewer** without-arm runs; T3 yields a table with row_count = 0 (not a null and not prose) in both with-arm repeats; T5 yields **no** table in both with-arm repeats; median token growth with-vs-without **<= 20%** across the paired repeats; zero tasks where the with-arm is correct in fewer repeats than the without-arm.

Number, direction, comparison set — evaluable by something that was not in the room when the results came in. A win that shows up in one repeat and not the other counts as a draw.

## Q3

**No — it does not pass. It is not measured.**

The token cap is a numeric threshold over a *comparison set*, and half the baseline comparison set is missing. Two null token cells are not two cells that were fine; not-measured and measured-fine are different states, and only one of them is evidence. Reading "the other two rows are within 20%" as satisfying the cap is exactly the failure where a missing number quietly counts as a pass.

Concretely: with 2 of 4 without-arm rows null, there is no denominator for those pairs, so no growth figure exists for them, so the clause "caps token growth at 20 percent" is **undecided**, not met. Undecided fails a gate; gates are not passed by default.

The better pass rates do not discharge it. They are a different axis, and the threshold as written has a token clause; if that clause can be dropped because another axis looks good, the threshold was never a threshold.

Fix (and it cannot be backfilled): re-run the two affected repeats with **both arms launched together** and instrumentation on. A without-arm token count collected now against a with-arm count collected earlier is not a pair. Until then record tokens as `null`, verdict as "token clause not evaluated", and do not ship on the pass-rate result alone.

## Q4

**Conclusion: no conclusion. The reviewer's clean sweep is not yet evidence.**

Write-up as it should go into the record:

> **Result.** Reviewing agent read 12/12 outputs, reported 0 problems.
>
> **Status: uninformative, pending grader calibration.** A grader that reports "no findings" has said one of two things and we cannot tell which: (a) the twelve outputs are clean, or (b) the grader is blind to the class we pointed it at. Twelve consecutive clean readings do not distinguish these — they are equally consistent with a grader that would report nothing whatever it was handed. Recording this as "12/12 clean" would be recording the ambiguity as a pass.
>
> **Next step, blocking.** Take one of the twelve real outputs and alter it in exactly one place, in the defect class we most need caught. One planted defect, not several — several teaches only that the grader found something. Submit it blind, mixed into a re-read.
>
> - Grader catches the planted defect -> the 12 clean readings stand as evidence of clean outputs, and are then also put to the grader as an attack on the *expectations* (whoever wrote the expectations cannot rule on whether they were the right ones — a grader can be sound and still have been pointed at the wrong thing).
> - Grader misses it -> the 12 readings are discarded, not re-interpreted. Fix the grader (its instructions, its inputs, or its model), re-run all twelve.
>
> **Also note.** 12 outputs with no problems in any is itself the clean-baseline shape: if the without-arm outputs are among these twelve and are also clean, the artefact must win on a *named* axis rather than on correctness, which is already saturated.

## Q5

**Don't ship.**

The record is **zero wins and zero losses**, not one win.

Task 3 won in repeat 1 and tied in repeat 2. A win that appears in one repeat and not the other is a draw with a good draw in it — the two repeats are the same test under the same conditions, so the disagreement is the variance of the task, not an effect of the skill. Counting it once is counting noise as signal. Tasks 1, 2, 4, 5 tied in both. Nothing regressed, which is good news and is not a result: "did not make things worse" is the *precondition* for shipping, not the case for it.

This is the clean-baseline row of the table: the baseline is doing the job, so the artefact must win on a **named** axis *and* not regress. It has not won an axis. Not regressing alone would justify shipping any no-op.

Check it against the threshold as written first, not one that seems fair now the numbers are visible: a threshold of the standard form ("at least one task won in both repeats") is explicitly failed by this data. If the threshold was prose that cannot be evaluated mechanically, say so out loud — and note that we are now reading it after the results, which is the moment it stops being a threshold.

What would settle it, in order:

1. Stage 1 is borderline, so expand: more repeats on Task 3 specifically (4-6), same pairing discipline. If the win reproduces in most repeats, it is real and Task 3 names the axis.
2. If it does not reproduce, the skill is a measured no-op that still costs tokens and context — and a no-op is a no-go, because the token cost is certain and the benefit is not.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-measure.with.txt` (the prompt, its embedded method, and the bundled `probe-and-pairing.md` reference)
- `/home/user/skills-repo/CLAUDE.md` (present in session context; not opened for this task)
- No other files, skills or tools were read.
