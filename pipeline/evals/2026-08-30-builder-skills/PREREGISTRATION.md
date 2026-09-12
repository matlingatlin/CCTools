# Preregistration — the three staged builder skills

**Written 2026-08-30, before any answer file existed.** Two arms of `skill-contract`
repeat 1 were dispatched minutes earlier and had not returned. Nothing below was chosen
with a result in view; that is the only property that makes it worth writing.

## What is being tested

`skill-contract`, `skill-measure`, `skill-knowledge` — the skill-builder's own three
methods, staged in `pipeline/skills/` and not yet shipped.

## The arms

| | |
| --- | --- |
| `without` | this repo's model with the library as it stands, and no access to the staged method |
| `with` | the same, plus the method's SKILL.md body and its bundled reference, pasted into the prompt |

**The baseline is deliberately not a bare model.** It is what we already have. The
question worth answering is not "is this better than nothing" but "does adding this beat
the 84 skills already in the library", which is the reuse-first gate. A skill that only
beats an empty repo has not earned a slot in this one.

## The decision rule for this run

Across k = 2 repeats per question:

1. **No regression on correctness.** No question where the `without` arm meets every
   expectation and the `with` arm does not.
2. **At least one question won, and the win survives both repeats.** Won means: the
   `with` arm meets every expectation and the `without` arm does not.
3. **Cost: NOT MEASURED, and therefore not passed.**

## Clause 3 is a hole, and it is named here rather than quietly dropped

The default contract rule caps token and tool-call growth at 20%. **This harness cannot
measure either.** Subagent runs return no token count to the coordinator, and there is no
metered path in this repo — `DATA.md` already requires `spend_measured` to stay `null`
until one exists.

So the structured rule for this run sets `cost_axes: []`, and every build record from it
carries a `not_checked` row saying the cost axis was not established. A verdict reached
this way is **"ships on correctness, cost unknown"**, never "ships". Dropping a clause
because it cannot be measured is only honest while it is written down before the results;
dropping it afterwards is how a threshold gets moved.

This is the same weakening my own selftest uses as a negative control
(`pipeline/build/selftest_build.py`: "treat a missing measurement as a pass"). The
difference is the reason and the timing, and both are on this page.

## What a failure means

An `iterate` verdict on any of the three is the expected outcome for a first pass, not a
surprise. These are the builder's own methods, so a failure here is a finding about the
method, and it goes to triage before anything is rewritten.

## Grading

Blind. Arms are relabelled A/B per question by a seeded coin (`blind.py`); the key is
written to a file the grader is never given. The grader rules per expectation with a
quoted line as evidence, and is also asked to attack the expectation set — an
expectation both arms satisfy trivially never was a measurement.

**The grader is not calibrated against a planted defect.** That is phase 6.3 and it is
v2. A clean grader report from this run is therefore ambiguous in the way `skill-measure`
itself warns about, and that ambiguity is recorded rather than resolved.

---

## AMENDMENT 1 — the cost axis turned out to be measurable

**Written 2026-08-30, after the first two runs returned and before any of them was
read or graded.** Recorded here rather than by editing the text above, because a
preregistration that gets edited is not one.

Clause 3 said this harness cannot measure tokens or tool calls. That was wrong. The
task-completion notification for a dispatched run carries `subagent_tokens`,
`tool_uses` and `duration_ms`. They are per arm-run, not per question, and they are
MEASURED — read off the notification, not estimated. They are being logged to
`cost/measured.jsonl` from the first run onward.

**What this does and does not change for this run.**

The numbers are recorded, and they are reported as an **observation, not as a gate**.
I learned they were available after the rule was fixed, so promoting them to a clause
now would be adding a criterion with results already in existence — which is the exact
failure the preregistration exists to prevent, even though in this instance no answer
file had yet been opened.

**From the next run onward the cost clause is live**, with `cost_axes` back to tokens
and tool calls at the contract's 20% tolerance.

One caveat that must travel with the numbers: **the `with` arm's prompt is inherently
longer** — it carries the method body and its reference, several thousand characters
the `without` arm never receives. Some of the token delta is the method being present
at all, not the method causing extra work. A fair cost comparison has to say which
part of the delta is input it was handed and which is work it chose to do, and
`subagent_tokens` as reported does not separate them. That is now the open question
against this axis, and it is not resolved here.
