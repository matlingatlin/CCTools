---
name: skill-measure
description: Use when proving a skill, prompt or agent change actually improves results - running a baseline probe before writing anything, running paired with-and-without trials, writing expectations from observed outputs, grading against a preregistered threshold. Covers what to do when the baseline already passes, why a win must survive a repeat, and why a grader is checked against a planted defect before its verdict is believed.
license: internal
---

# Showing that it works

The measurement is not the last step. It is the first one: the baseline probe runs
before a single line of the artefact is written, because everything written afterwards
is written against what the probe found.

## Important — a passing baseline does not stop the build, it raises the bar

The tempting rule is "if the baseline already does the job, don't build it". That rule
is wrong in the dangerous direction. Roughly one task in seven measurably *regresses*
under an added skill, and the regressions concentrate exactly where the base model was
already competent. So a clean baseline is not a neutral result — it is the case most
likely to be made worse, and it needs more evidence to ship, not less.

| The probe shows | What the artefact must then prove | Runs |
| --- | --- | --- |
| baseline fails | it fixes the observed failure | 1 suffices |
| baseline passes unevenly | it makes the outcome consistent | at least 2, or variance is invisible |
| baseline passes cleanly | it wins on a **named** axis and does not regress | at least 2 |

## Steps

**Probe before writing.** Run the representative tasks with no artefact present, in
fresh sessions. Then code what happened: what the runs actually did, quoted; the
consequence; and whether every run did it or only some. "The output was worse" is not
an observation — it names no behaviour anyone could recognise in a transcript.

**Write the test prompts now, and only the prompts.** Expectations come later, from the
outputs you have not seen yet. Writing them now means writing down what you hope will
happen and then grading against your own hope.

**Hand a run a path, not a corpus.** Anything the run can look up — a fixture, a repo, a
dataset — goes in as a path it reads. Pasting it inline pays for it once per run and defeats
the prompt cache, because text that shifts position in every prompt cannot be reused. Paste
only what the run must not be able to find on its own: the method body in the with-arm, and
nothing at all in the without-arm.

**Run paired, in the same turn.** With and without, fresh sessions each, both arms
launched together — a baseline collected an hour earlier is a different machine under a
different load. Capture tokens, tool calls and duration as they happen. There is no
second chance at them: the numbers are gone the moment the run ends.

**Then write the expectations,** from what the outputs actually contain.

**Check the grader before believing the grader.** Hand it a specimen carrying one
planted defect, without saying so. A grader that reports "no findings" has said one of
two things and you cannot tell which: the artefact is clean, or the grader is blind. A
grader that misses its own planted class is not reporting on what you pointed it at.

**Grade with evidence, and let the grader attack the expectations too.** Whoever wrote
the expectations cannot rule on whether they were the right ones.

**Decide against the threshold that was written first.** Not the one that seems fair
now that the numbers are visible. If the threshold was written as prose that cannot be
evaluated mechanically, say so — and note that reading it now means reading it after
the results.

## Three ways a measurement quietly lies

- **A missing number counts as a pass.** It must not. Not-measured and measured-fine
  are different states, and only one of them is evidence. Keep them apart in the data:
  null for absent, 0 for a measured zero.
- **One run decides.** It cannot tell a tie from a small regression, which is precisely
  the distinction that matters in the clean-baseline case.
- **A win is counted once.** A win that appears in one repeat and not the other is a
  draw with a good draw in it.

`references/probe-and-pairing.md` has the run shapes, what to capture per run, and how
to tell an uneven baseline from a failing one.

## In this repo (one instance)

The verdict is computed by `pipeline/build/decide.py` against the threshold recorded in
the build's `record.json`; per-scenario outcomes go to `pipeline/ledgers/evals.jsonl`.
The staged default — 3 to 5 tests, 2 arms, 2 repeats, expanding to 20 tests only when
stage 1 is borderline — is in the contract's acceptance block. Every probe, arm and grader
run is dispatched through `pipeline/build/dispatch.py`, which is what makes "fresh sessions,
method mounted for the with-arm only, tokens captured live" true by construction rather than
by care: build 3 of 2026-09-02 lost a full wave of runs to a shared directory and a mounted
method before that module existed.
