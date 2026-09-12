## Q1

**Verdict: NO-GO — but the no-go is on the experiment, not (yet) on the skill.**

What the numbers actually say: the task set cannot tell the two arms apart. Baseline scored 5/5.
A ceiling like that means every task was solvable without the skill, so the correctness column
carries zero information about whether the skill helps. The only thing the run measured is cost:
+2,600 tokens, +26.5%.

On the evidence in hand the decision is forced — we are being asked to pay 26.5% more tokens for
a benefit that has not been demonstrated once. Do not adopt.

Two further reasons not to read anything into this:
- n=1 per task per arm. With single runs there is no variance estimate, so even a difference would
  not be separable from run-to-run noise.
- 5 of 5 both ways is 5 ties out of 5. Zero discriminating observations.

**What has to happen before this comes back:**
1. Rebuild the task set so the baseline is expected to FAIL the tasks the skill claims to fix.
   Roughly half normal/representative (confirms it does not break the everyday job) and half
   designed to defeat baseline, plus one negative-trigger task where the skill must NOT engage.
   If we cannot write a task the baseline fails, we have not identified what the skill is for and
   should stop there.
2. Write the pass bar down before the rerun: which metric decides, what margin counts, what token
   growth is tolerable. Fix it in advance so the result cannot move the bar.
3. At least 3 repeats per task per arm, same model, same prompt scaffolding, grading by a
   deterministic script wherever the output allows.

If the rebuilt set still shows parity, the honest conclusion is that the skill costs 26% and buys
nothing — drop it. Note that "drop" would then be justified by failing its own test, not by being
unused.

## Q2

Claim under test: with the skill, a review agent emits ONE ROW PER FINDING in a table; without it,
it drifts into prose, merges findings, or emits a table whose rows do not correspond 1:1 to
findings.

**Preregistered decision rule (written before any run):**
- Primary metric: **row-to-finding fidelity** = fraction of runs where rows == ground-truth findings
  AND no fabricated rows AND no merged rows. Deterministic, scriptable.
- Secondary: required columns present in every row; findings recall vs the seeded ground truth
  (the skill must not buy structure by losing findings).
- Cost gate: median with-arm total tokens ≤ 1.20x median without-arm.
- Ship bar: fidelity with-arm ≥ 0.80 AND ≥ +0.30 absolute over without-arm, on ≥ 3 of the 6 tasks,
  no task regressing on recall, cost gate met. Anything else = no ship.
- Stop rule: 36 runs, no extension, no post-hoc metric swap.

**Tasks (6, each with a hand-written ground-truth finding list):**

| id | kind | input | seeded ground truth | why it is here |
|----|------|-------|---------------------|----------------|
| T1 | normal | diff, 4 clearly independent findings across 3 files | 4 findings | the everyday job |
| T2 | normal | diff, 2 findings, both in one function | 2 findings | tempts merging into one row |
| T3 | normal | diff, 7 findings, mixed severity | 7 findings | tests it does not truncate to a tidy 5 |
| T4 | adversarial | clean diff, no real defects | 0 findings | must emit an empty table / explicit "none", NOT invent rows to fill the format |
| T5 | adversarial | one defect that manifests at 3 call sites | 1 finding (root cause) | must not inflate to 3 rows; row count is per finding, not per symptom |
| T6 | negative trigger | "explain what this module does" — not a review | n/a | skill must NOT fire and must NOT emit a findings table |

**Arms:** `without` (identical prompt, skill unavailable) and `with` (skill available). Nothing
else differs — same model id, same temperature, same repo snapshot, same reviewer prompt text.

**Runs to launch: 6 tasks x 2 arms x 3 repeats = 36 runs.** Repeats are what make a per-task win
believable; one repeat cannot distinguish a win from a coin flip. Run them interleaved by repeat
(all 12 arm-pairs of repeat 1, then repeat 2, then 3) so a mid-session model or infra change hits
both arms equally rather than contaminating one.

**Record per run — one JSONL row, written as the run finishes, never reconstructed afterwards:**

```
run_id, task_id, arm(with|without), repeat(1..3), model_id, started_at, wall_clock_s,
tokens_in, tokens_out, tokens_total,
output_path,                      # raw output kept verbatim on disk
table_present(bool), row_count(int),
gt_finding_count(int), rows_matched(int), rows_fabricated(int), findings_missed(int),
merged_rows(int), split_rows(int),
required_columns_present(bool), columns_missing[],
fidelity_pass(bool),              # rows==gt AND fabricated==0 AND merged==0 AND split==0
skill_fired(bool),                # T6 negative trigger: must be false
grader(script|human), grader_version, notes
```

Grading is a parser script, not a model, for everything except mapping a row to a ground-truth
finding — that mapping is done by a human once per output and the mapping file is committed, so
re-grading later is reproducible. If a run's token count fails to log, that run is void and is
re-run; it is not imputed and not dropped silently.

**Reported at the end:** the 36-row table, per-task fidelity with/without and the delta, median
token ratio, and the verdict read straight off the preregistered bar. Plus the T6 result stated
separately — a skill that fires on a non-review is a defect even if every other number is good.

## Q3

**It does not pass. It does not fail either — it is undetermined, and undetermined is not a pass.**

Token growth is a ratio, and half the denominators are missing. With two of four baseline token
counts absent there is no defensible way to compute growth against the 20% cap:
- Averaging the two known baselines and applying that to the missing rows assumes the missing rows
  behaved like the present ones, which is exactly the thing we do not know.
- Dropping the two incomplete pairs and judging on the remaining two silently changes the test to
  a different, weaker one — and the rows most likely to fail to log are the long, expensive runs,
  so the surviving subset is biased cheap.

The better pass rates do not help. Correctness and cost are separate gates; a skill can improve
accuracy and still be rejected on cost. Passing one gate does not license waiving the other.

**Do this:** re-run the two missing without-arm rows under the same conditions and recompute the
ratio on all four pairs.

**And treat the gap itself as a finding.** Two of four rows lost their token count, which means the
measurement pipeline drops data without erroring. Until we know why, the token numbers that DID
land are of unknown reliability, and so are the pass-rate rows recorded by the same harness. Fix
the logging so a missing metric voids and re-runs its own row, rather than producing a table that
looks complete enough to reason over.

## Q4

**Conclusion recorded: none. The review is uninformative and no quality claim is entered.**

A reviewer that reports no problems across twelve outputs has told us one of two things and we
cannot distinguish them: either the outputs are clean, or the reviewer does not detect problems.
There was no positive control in this review — nothing was planted that the reviewer was required
to catch — so the instrument is uncalibrated and its clean report has no evidential weight. A
zero-defect result from an unvalidated detector is the single most common way a check gets
silently gutted while still looking green.

Before this result can be cited:
1. **Calibrate.** Seed known defects of the kind the review is supposed to find into 3-4 of the
   twelve outputs (or into copies), shuffle, and re-run the same reviewer blind. If it catches them,
   its clean verdict on the rest becomes meaningful. If it misses them, this review is void and its
   output should be deleted rather than filed.
2. **Record the calibration alongside the verdict** — reviewer, prompt version, seeded defect list,
   catch rate, date. A verdict without its detector's sensitivity is not a measurement.

Separately, and independently of calibration: **this review is not the skill's test.** It grades the
outputs' quality; it does not compare with-arm against without-arm, so even a perfectly calibrated
clean sweep would not tell us the skill did anything. The adoption decision still needs the paired
baseline-vs-with run against the preregistered bar. Quality review and effect measurement are two
different jobs and neither substitutes for the other.

## Q5

**No. Do not ship.**

Ten paired observations (5 tasks x 2 repeats): one win, zero losses, nine ties. Run that through a
sign test and it is a single discordant pair — p = 0.5. That is precisely the result you would
expect from a skill that does nothing at all. "Nothing regressed" is not a signal; with nine ties,
the experiment had almost no opportunity to show a regression either.

The one win is also the weakest possible kind. Task 3 won in repeat 1 and tied in repeat 2 — the
skill did not reproduce its own only success. An effect that appears in one of its two attempts on
the same task, with everything else held fixed, is indistinguishable from run-to-run variance. If
anything the repeat is evidence against the win, not support for it.

The deeper problem is the task set, not the tally: 9 of 10 ties means the tasks are at ceiling and
cannot detect this skill's contribution regardless of how many times we rerun them. More repeats on
these five tasks will buy tighter confidence intervals around zero.

Also missing from the summary: cost. No token comparison was cited. A skill with no demonstrated
benefit and any nonzero token overhead is net negative, so absent that column the decision defaults
to no.

**What to do instead:**
1. Rewrite the task set so the baseline is expected to fail where the skill claims to help. Keep the
   normal tasks as a no-harm check, but the deciding tasks must be ones baseline loses.
2. Write the ship bar down before rerunning — e.g. wins on ≥ 3 of 6 tasks, reproduced in every
   repeat of those tasks, zero regressions, ≤ 1.20x tokens.
3. Rerun with ≥ 3 repeats per arm and decide off that bar.

If the rebuilt set still returns ties everywhere, that is the answer: the skill does not earn its
place, and it should be dropped for failing its test.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-measure.without.txt` (the prompt itself)
- `/home/user/skills-repo/CLAUDE.md` (auto-loaded into context by the harness, not opened deliberately)

No skills were invoked and no files under `pipeline/skills/`, `pipeline/contracts/` or
`pipeline/build/` were read. Answers are from general knowledge and judgement.
