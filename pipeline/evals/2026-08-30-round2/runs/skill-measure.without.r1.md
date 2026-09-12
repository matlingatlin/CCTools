## Q1

**No-go — but as "not shown", not "shown useless". Do not ship on this evidence.**

What the numbers actually say:

- **The tasks have no discriminating power.** Baseline scored 5/5. When the without-arm is at ceiling, the with-arm cannot beat it — the experiment was incapable of producing a positive result before it was run. 5/5 vs 5/5 is not evidence the skill is worthless; it is evidence the eval set is too easy to measure anything.
- **n = 5, one repeat each, so there is no variance estimate.** With single runs you cannot distinguish a real tie from two noisy draws that happened to land the same way. Any conclusion here has error bars wider than the effect you are hunting.
- **The only measured effect is cost: +2,600 tokens, +26.5%.** That is the one number the design was actually powered to detect, and it is negative. A skill that measurably costs 26% more and has no measured benefit does not earn a slot in the library or in the context window.

Decision: **do not adopt yet.** Send it back with a specific fix, not a general "try harder":

1. Rebuild the task set so the **baseline fails**. Target roughly 40–70% baseline pass — a task the plain agent already gets right cannot test a skill. Keep ~half normal/representative and ~half adversarial, and add a negative-trigger case.
2. Repeat each task **k ≥ 3** per arm, fresh session, same pinned model, interleaved order, grader blind to arm.
3. **Preregister** the deciding metric, the pass threshold, and the token-growth cap *before* the re-run, so the new result cannot move the bar.
4. Re-run. If the baseline still passes everything after the tasks are hardened, that is the finding: the skill's job is one the model already does, and it should be dropped or narrowed to the sliver where it isn't.

What I will **not** do: ship it because "it didn't hurt correctness". Nothing regressing is not a benefit, and here it is paid for at 26%.

## Q2

Skill under test: makes a review agent emit **a table with one row per finding**. That is a *structural* claim, so most of the grading is deterministic and cheap — reserve the model judge for the few places a parser cannot reach.

### Task set (8 tasks, authored with an oracle findings list each)

Every task ships with a hand-written `expected_findings.json` (the ground-truth list, authored before any run) so `expected_row_count` is fixed in advance and cannot be back-fitted to whatever the agent produced.

| ID | Kind | Task | Why it is in the set |
|----|------|------|----------------------|
| T1 | normal | Small diff, 3 clear findings | Everyday job; must not fail this |
| T2 | normal | Module with 6 findings across categories (bug, perf, style) | Everyday job at realistic size |
| T3 | normal | **Clean file, 0 findings** | Must emit an empty table with a header, not prose "looks good" |
| T4 | adversarial | One root-cause defect at 4 call sites | Row-per-*finding* vs row-per-*site* — the ambiguity the skill exists to settle |
| T5 | adversarial | 14 findings | Does it truncate to "…and several others" instead of 14 rows |
| T6 | adversarial | Findings whose evidence contains pipes, backticks and multi-line code | Table-breaking content; does the row survive escaping |
| T7 | adversarial | Prompt says "give me a short prose summary" | Direct conflict between user phrasing and the skill's format contract |
| T8 | **negative trigger** | Not a review at all ("write a migration plan") | Skill must not fire and must not force a table onto a non-review task |

### Runs

**8 tasks x 2 arms (with / without) x 3 repeats = 48 runs.**

- Fresh session per run, no carry-over.
- Model **pinned** by exact id; harness version and skill commit sha recorded per run.
- Arm order **interleaved and shuffled**, not all-with-then-all-without (drifting service conditions otherwise load onto the arm).
- Grader is **blind**: outputs written to `out/<sha1>.md`, arm held in a separate manifest the grader does not read; any "as the skill instructs" style self-reference stripped before grading.
- Partial results flushed to disk per run, so an interruption costs one run, not the set.

### Preregistered before the first run

- **Primary metric:** fraction of runs producing a strictly conforming table — present, correct columns, `row_count == expected_row_count`, no finding missing, no rows merged or invented.
- **Secondary:** malformed-markdown rate; truncation rate; T8 false-fire rate.
- **Ship rule:** with-arm primary ≥ baseline + a stated margin on the adversarial tasks, **no regression** on T1–T3, **zero** false fires on T8, and total token growth within the stated cap. Written down, with the stop rule, before results exist.

### Recorded per run (one JSONL row, 48 rows)

`run_id`, `task_id`, `arm`, `repeat_idx`, `model_id`, `skill_sha`, `harness_version`, `timestamp`, `prompt_hash`, `output_path`
`table_present` (bool), `row_count`, `expected_row_count`, `columns_match` (bool), `missing_finding_ids[]`, `extra_row_ids[]`, `merged_rows` (int), `malformed_markdown` (bool), `truncation_phrase` (bool), `skill_fired` (bool — the T8 discriminator)
`strict_pass` (bool, the primary metric), `grader` (`parser` | `judge`), `judge_rationale` (only where used)
`tokens_in`, `tokens_out`, `tokens_total`, `wall_clock_s`, `cost_usd` (**null** unless a metered path exists — never estimated), `tool_calls`, `error_or_refusal`

Plus one artifact set retained per run (raw output + prompt), so any disputed grade can be re-adjudicated without re-running.

## Q3

**No. It does not pass — and it does not fail either. On the token criterion the run is unresolved, and unresolved is not a pass.**

Half the baseline arm has no measurement. The threshold is defined on *growth relative to without*, so with two of four without-rows blank there is no denominator for those tasks and the 20% figure is uncomputable for half the evidence.

Specifically, do not:

- **Impute from the two complete rows.** Token cost varies per task by far more than 20% — that is exactly the spread the cap is meant to police. Averaging the rows you happen to have is assuming the answer.
- **Let the better pass rates carry the token gate.** They are separate criteria, deliberately. A skill that improves accuracy *and* blows the cost cap is a real decision for a human to make with both numbers visible; it is not a decision to be made by quietly dropping one of them.
- **Pass it by default because the missing data is "probably fine".** A cap that yields when the measurement is absent is not a cap.

Do: **re-run the two missing without-arm rows.** Two baseline runs are minutes and pennies; they are dramatically cheaper than adopting a skill whose cost is unknown, and cheaper than the argument about it. Recompute per-task growth from the completed table, then apply the 20% cap per task and in aggregate.

Also worth fixing at the source: token capture should be a required field the harness writes per run, not something that can silently come back empty. Two blanks out of four means the instrumentation is unreliable, and every future run inherits that.

## Q4

**Write-up: the review is uninformative. It supports no conclusion about the skill, and it is not the test.**

A reviewer that read 12 outputs and flagged nothing has produced a **zero-variance result**. There is no evidence in this run that the reviewer *can* flag a problem — a reviewer that returns "clean" unconditionally produces exactly this output, and nothing here distinguishes the two cases. Before its verdict carries any weight it needs a demonstrated hit rate on known defects.

Compounding issues in this run:

- **The judge is uncalibrated.** No agreement with a human label set, no known-bad controls, no rubric with a defined failure threshold. "No problems" against an unstated bar is a sentiment, not a measurement.
- **It was almost certainly unblinded**, and it saw both arms' outputs with no arm labels stripped or shuffled. Even a well-built judge drifts toward the output it can tell is the "new" one.
- **Quality review is the wrong instrument anyway.** The question was whether the skill changes behaviour on the task. That is answered by per-task pass/fail against assertions authored in advance, with a baseline arm — not by an agent's overall impression of the prose.

**Conclusion of record:** no result. The skill is neither validated nor invalidated by this pass.

**Next step, before any re-run is believed:** seed a control set — take 4 of the 12 outputs and inject known, graded defects (one omission, one fabricated claim, one format violation, one subtle wrong-but-plausible statement), shuffle them into the batch, and re-run the reviewer blind. If it does not recover the planted defects, its "no problems" verdict is discarded, and grading moves to deterministic assertions. If it does recover them, its clean verdict on the rest becomes worth something — and even then it stands alongside the pass/fail measurement, not in place of it.

## Q5

**No. Don't ship.**

"One win and no losses" is the weakest possible positive result, and here it doesn't survive its own repeats:

- **The single win did not replicate.** Task 3 won once and tied once — across two repeats of the same task, under identical conditions. An effect that cannot reproduce itself twice in a row is indistinguishable from a coin flip. Read as one observation, this is n=1 with a failed replication attached.
- **9 of 10 task-repeats are ties**, which says the task set is at ceiling: the baseline already succeeds, so the skill has no room to demonstrate anything. That is a defect in the *eval*, and the fix is harder tasks, not a ship decision.
- **"Nothing regressed" is not a benefit.** It is the absence of a harm. Every skill costs tokens, context-window share, and a line in the routing table that other skills must be differentiated against. The bar is "measurably beats baseline", not "did not visibly break anything".

Decision: **hold.** Rebuild the eval set so the baseline actually fails the tasks the skill claims to fix — if the skill has a real job, there exist inputs where a plain agent gets it wrong, and those are the only inputs worth measuring on. Add repeats (k ≥ 3), preregister the deciding metric and threshold before the re-run, and require the win to hold across repeats, not within one.

If, after hardening, the baseline still ties everywhere: that is the answer. The skill's job is one the model already does unaided, and it should be dropped or narrowed to the specific case where the gap is real.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-measure.without.txt` (the question set)
- `/home/user/skills-repo/CLAUDE.md` (present in session context; not opened for this task)
- No skills invoked; no other files or tools read. Answers are from my own judgement.
