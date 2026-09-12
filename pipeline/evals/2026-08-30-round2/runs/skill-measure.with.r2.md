## Q1

**No-go on this evidence.** Not "the skill is bad" — the run cannot support a decision either way, and it costs 27% more tokens to not support it.

Two things are wrong with it:

1. **One run per cell.** With n=1 per arm I cannot tell which baseline I am looking at. 5/5 in a single pass is equally consistent with a clean baseline and with an uneven one that happened to land well this time — and the uneven case is the one where the skill's only real benefit (consistency) lives. One run also cannot separate a tie from a small regression, which is exactly the distinction in play here. Correctness is 5/5 vs 5/5: that is a tie in the data, not a win.
2. **The baseline passed, so the bar goes up, not down.** A clean baseline is the case most likely to be made worse by an added skill, so the artefact now has to prove two things it has not proved: a win on a *named* axis (name it before the re-run — row-completeness? consistency across repeats? something specific), and no regression. Neither is demonstrated. What *is* demonstrated is 12,400 vs 9,800 = **+26.5% tokens**, i.e. the only measured difference between the arms is that the skill is more expensive. If our standing cap is 20% token growth, that alone fails.

**Decision: do not ship. Re-run before deciding.** Minimum to reopen: ≥2 repeats per task per arm, both arms of each repeat launched in the same turn, tokens/tool-calls/duration captured live per run, and the named win axis and threshold written down *before* the numbers come back. If after that it is still 5/5 vs 5/5 with +26% tokens and no named axis won in both repeats, the answer is a permanent no-go, and that is a fine outcome — it means the base model already does this job.

One caveat on my own verdict: I am reading a threshold ("cap token growth") after seeing +26.5%. If no threshold was written before this run, then there was no threshold — record that as a process defect of this build, not as a number the skill failed.

## Q2

Skill under test: makes a review agent emit **one row per finding** in a table.

### Phase 0 — probe, before a line of the skill is written

8 runs, no artefact present, fresh session each, tasks run twice so the baseline can be classified:

| run | task | repeat | arm |
| --- | --- | --- | --- |
| P1–P2 | T1 dirty diff, 3 findings of different severity | 1,2 | without |
| P3–P4 | T2 file with exactly one finding | 1,2 | without |
| P5–P6 | T3 clean file, zero findings | 1,2 | without |
| P7–P8 | T4 large diff, ~12 findings incl. two sharing a root cause | 1,2 | without |

Then code what happened, in quotes, per run: did it produce a table at all; did it produce prose with bullets; did it merge two findings into one row; did it emit a row for a non-finding; on T3 did it emit an empty table, "no issues found", or nothing. Then classify: **every run misses it → failing; some runs table, some prose → uneven; every run acceptable, differing only in column names → clean.** That classification sets how many wins the skill has to show later, so it is not optional.

### Phase 1 — write the test prompts, and only the prompts

The five prompts (T1–T4 above plus **T5, negative trigger**: "explain what this module does" — no review requested; the skill must not impose a finding table). No expectations yet — they get written in phase 3 from outputs I have not seen.

### Phase 2 — the paired run

5 tasks x 2 arms x 2 repeats = **20 runs**. Both arms of a given (task, repeat) launched together in the same turn, fresh session each; nothing reused from the probe, because a baseline collected an hour ago is a different machine.

| runs | task | repeats | arms |
| --- | --- | --- | --- |
| R1–R4 | T1 three findings, mixed severity | 1,2 | with + without |
| R5–R8 | T2 exactly one finding | 1,2 | with + without |
| R9–R12 | T3 clean file, zero findings | 1,2 | with + without |
| R13–R16 | T4 twelve findings, two share a root cause | 1,2 | with + without |
| R17–R20 | T5 negative trigger, not a review | 1,2 | with + without |

### Recorded per run, captured live

| field | note |
| --- | --- |
| test id / repeat / arm | arm is `with` or `without`; pair id ties the two arms launched together |
| correct | boolean, or **absent if nobody ruled** — absent is not false |
| tokens / tool calls / duration | captured at the run, not reconstructed; `null` if genuinely not captured, never 0 |
| artefact | the full output, kept — the expectations are written from these |
| rows emitted | integer |
| findings present in the source | integer, from the task's own key |
| rows-merged count | findings collapsed into a shared row (T4's planted pair is the probe for this) |
| phantom rows | rows with no corresponding finding |
| table emitted at all | boolean (T5: emitting one is the failure) |

### Phase 3 — expectations, from the outputs

Written after reading all 20 artefacts, describing behaviour visible in transcripts ("T4 without-arm collapsed the two null-check findings into a single row in both repeats"), never "the output was worse".

### Phase 4 — calibrate the grader before believing it

Take one real with-arm T4 table, alter it in **exactly one place** — merge two findings into one row, the class I most need caught — and hand it to the grader with no hint. If it comes back "no findings", the grader is blind to the only class this skill exists to fix, and every clean verdict it has given so far is uninterpretable. Fix the grader, then re-grade. Let the grader also attack the expectations; I wrote them, so I cannot rule on whether they were the right ones.

### Phase 5 — pre-registered threshold (written now, before results)

> rows == findings on T1, T2, T4 in **both** repeats of the with arm; zero rows-merged and zero phantom rows in the with arm across both repeats; T3 yields an explicit zero-finding statement in both repeats; T5 yields no table in either repeat; token growth ≤ 20% on the median across T1–T4; and at least one task where the with arm beats the without arm **in both repeats** (a win in one repeat only is a draw).

A number, a direction, a comparison set — checkable by someone who was not in the room when the results landed.

## Q3

**No. It does not pass — the token clause is unevaluable, and unevaluable is not a pass.**

The comparison the threshold asks for is with-arm tokens against without-arm tokens. Two of the four without-arm rows have no token count. That is a *null*, not a zero and not a fine result: nobody measured them, so half the baseline is missing and there is no denominator to compute 20% against. Quietly averaging the two rows that do have counts, or scoring the missing pair as "no growth observed", is the classic way a measurement lies — the missing number silently counting as a pass.

So the verdict splits:

- **Correctness clause: passes** (pass rates better with the skill) — assuming those rows were actually ruled and not merely unruled.
- **Token clause: NOT MEASURED.** Record it as `null`, not as met.
- **Overall: no pass.** A threshold with an unmet-because-unmeasured clause is not satisfied.

To close it: re-run the two without-arm cells that lack counts — freshly, paired against their with-arm partners in the same turn, because tokens from a solo re-run an hour later are not comparable to the with-arm numbers already in the table. Then evaluate the 20% cap on complete data. If those two cells cannot be re-run, the honest write-up is "token cap not evaluated", and the build ships or doesn't on the correctness clause alone, with that gap stated on the record.

## Q4

**Conclusion: no conclusion. The review is uninterpretable until the grader is calibrated.**

"No problems in any of twelve" is exactly the result that carries no information, because it has two indistinguishable causes: the twelve outputs really are clean, or the reviewing agent cannot see the defect class we pointed it at. Nothing in a uniformly clean report tells the two apart, and the second is common — a grader given a vague brief tends to converge on "looks fine" across everything it is shown.

Write-up as it should go into the record:

> **Grader result:** 12/12 outputs reported clean by the reviewing agent. **Status: NOT EVIDENCE.** The grader was not calibrated before the pass, so a clean report cannot be distinguished from a blind grader. No quality claim about the twelve outputs is supported at this time.
>
> **Action before this becomes a result:** build a calibration specimen — take one of the twelve real outputs, alter it in exactly one place, in the defect class we most need caught (one defect, not several; several teaches only that the grader found *something*) — and hand it to the same grader with the same brief and no hint that it is planted. Two outcomes:
> - grader flags the planted defect → the 12/12 clean verdict becomes believable evidence, and is recorded as such with the calibration noted.
> - grader misses it → the grader is not reporting on what we pointed it at. The 12/12 result is discarded, not downgraded. Fix the brief or the grader, re-run all twelve, and re-calibrate.
>
> Additionally: the grader should be asked to attack the **expectations** as well as the outputs. Whoever wrote the expectations cannot rule on whether they were the right ones, and a clean sweep is as easily explained by expectations that ask for nothing as by outputs that satisfy them.

Suspicion worth stating out loud in the record: twelve for twelve, with no partial or borderline calls anywhere, is itself the shape of a grader that is not discriminating. Perfect uniformity is a symptom, not a reassurance.

## Q5

**Not yet — that is a draw, not a win.**

Task 3 was won in repeat 1 and tied in repeat 2. A win that appears in one repeat and not the other is a draw with a good draw in it: it is what a small random advantage looks like, and with n=2 there is nothing to distinguish the two. So the scoreboard is not "one win, no losses" — it is **five ties and no losses**, with one repeat that went nicely.

That would be a weak-but-arguable case if the baseline had been failing. It is not the case here: everything tying in both repeats means the baseline is doing the job, i.e. we are in the clean-baseline row — the row where an added skill is most likely to make things quietly worse, and where the artefact must prove a win on a **named** axis *and* no regression. It has proved no regression. It has not proved a win: an axis that wins in one repeat out of two has not been named and demonstrated, it has been observed once.

**Decision: do not ship on this. Two ways forward, pick one.**

1. **Name the axis and re-run task 3 specifically**, ≥3 repeats per arm, paired, launched together. If the win reproduces in the majority of repeats on a stated axis, ship. If it alternates, it was noise and the answer is no.
2. **Accept the honest outcome:** the base model already does these five tasks, and this skill has no measured benefit. Don't ship it. That is a real result and it is cheap — a skill that adds tokens for a coin-flip advantage is a net loss, and the regression risk is concentrated exactly in this situation.

And check the pre-registered threshold before choosing: if it said "at least one task won in both repeats", this fails it outright and there is nothing to weigh. If no threshold was written before the numbers, say so plainly — a bar chosen now is a bar chosen after seeing the results.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-measure.with.txt` — the prompt, the supplied method ("Showing that it works") and its bundled reference `probe-and-pairing.md`.
- No other files, skills or tools were read.
