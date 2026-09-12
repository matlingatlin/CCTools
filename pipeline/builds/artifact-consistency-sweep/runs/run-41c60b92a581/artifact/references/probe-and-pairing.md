# Run shapes and what to capture

Written 2026-08-30.

## Telling the three baseline outcomes apart

You cannot classify a baseline from one run. Run each representative task at least
twice before deciding which row of the table you are in.

| Observation across runs | Classification |
| --- | --- |
| every run misses the same thing | failing |
| some runs produce the artefact, some do not | uneven |
| every run produces something acceptable, with differences of style only | clean |

The middle row is the one most often misfiled. An uneven baseline read as failing
credits the artefact with fixing something that fixed itself in half the runs; read as
clean, it hides the only benefit the artefact actually delivers, which is consistency.

## Per run, captured live

| Field | Note |
| --- | --- |
| test id, repeat, arm | the arm is `with` or `without`; both arms of a repeat are launched together |
| correct | boolean, or absent if nobody ruled — absent is not false |
| tokens, tool calls, duration | absent means not captured, and blocks the cost comparison |
| artefact | the output itself, kept, because the expectations are written from it |

## The grader's calibration specimen

Build it from a real output of the run, altered in exactly one place, in the class you
most need caught. One defect, not several: with several you learn only that the grader
found something.

## What a threshold has to contain to be checkable

A number, a direction, and a comparison set. "Better than before" has none of the
three. "No worse than 20% on tokens across at least two repeats, with at least one task
won in both" has all three and can be evaluated by something that was not present when
the results came in.
