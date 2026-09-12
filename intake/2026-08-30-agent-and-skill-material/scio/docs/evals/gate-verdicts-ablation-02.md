# Ablation 02 · `gate-verdicts` — it fired, and it changed nothing

**Date:** 2026-08-26. Two questions were being asked: do the skills load and fire automatically,
and have they been tested. Both now have answers, and the second one is worse than the first.

## Do they load?

**Yes, verified.** A session started in `/home/user/scio` lists all 27 project skills. A session
started in `/home/user/hello-world` lists none of them — skills load from the project directory, so
a session in the wrong repo has none of this available. That is the mechanism, not a defect.

All 27 descriptions carry a when-clause, which is the necessary condition for a skill to fire from
context rather than only from an explicit invocation. It is necessary and not sufficient.

## Does one fire unprompted?

**Yes.** Asked *"A gate in our build ran and returned empty output. Is that a pass?"* — a person's
phrasing, no skill named — the session answered and cited `gate-verdicts` without being told it
existed.

## Did it change the answer?

**No.** The same question, run from a directory where the skills are not loaded:

| | With `gate-verdicts` | Without any skill |
|---|---|---|
| Verdict | not a pass | not a pass |
| Reason | empty means it found nothing **or did not run**, and those must be distinguished | fail closed on empty output; it usually means the check did not run |
| Skill cited | `gate-verdicts` | none — *"a general CI/build-hygiene judgment"* |

Two independent runs, same conclusion, same reasoning. **The skill fired and added nothing**, because
the model already holds the instinct.

## What this actually measures, and what it does not

It does **not** show `gate-verdicts` is worthless. It shows this *question* does not discriminate.
The skill's substance is the five ordered checks with no default branch, the outcome vocabulary, and
the rule that *"no P1 substring" and "no critical findings" are different claims* — none of which
this question reaches.

**It shows the eval was badly designed, and that is the transferable finding.** A question the model
answers correctly without the skill measures nothing, however sensible the answer. The discriminating
question is one where general instinct gives the *wrong* answer for our system — and writing those is
harder than writing skills.

`obra/superpowers` states the rule this pass rediscovered the expensive way: **watch an agent fail
without the skill first.** Had that been done here, this question would never have been chosen.

## Where this leaves the 27

| | |
|---|---|
| Load in a session in `scio` | **27 of 27**, verified |
| Descriptions capable of firing | **27 of 27** |
| Observed firing unprompted | **1** |
| Measured against a no-skill baseline | **2** |
| Shown to change an outcome | **0** |
| Shown to make an outcome *worse* | **1** — `as-built`, ablation 01 |

Two measurements exist. One skill made an answer worse; one made no difference. That is the whole
evidence base for twenty-seven skills, and it is not an argument for deleting them — it is an
argument that **nobody knows**, which is a different and more uncomfortable position.

`claude plugin eval --ablation with-without` automates exactly this comparison and is early-access
gated on this account. Until it opens, the comparison has to be run by hand, and the hard part is
not running it — it is choosing a question that can fail.
