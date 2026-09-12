# skill-knowledge — round 2

5 questions × 2 arms × 2 repeats = 20 answers, graded blind, cost clause live.

## Verdict: ship

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats | pass | |
| no correctness regression | pass | |
| tokens | pass | 66,910 vs 63,758 = **1.05×** (cap 1.20×) |
| tool calls | pass | 2.0 vs 2.5 = **0.80×** — the skill arm used *fewer* |
| ≥1 win surviving both repeats | pass | **Q3, Q4, Q5** |

Score: with 4/5 and 5/5 · without 1/5 and 0/5. The widest gap of the three skills.

## What actually separated the arms

Both graders named the same axis, and it is the one round 2 was rewritten to test:

> *"The recurring separator across the set is production versus description — per-failure
> coverage outcomes, a verbatim quote field, a reached-how field distinct from
> read-how-much, an enumerated verifier return vocabulary — and rulings turned on whether
> those existed in the answer or were only promised."* — r2

The baseline consistently explained what it would do; the skill arm produced the row.

## One win is inflated and is discounted here

The r2 grader found a confound in my own expectation set, and it is the sharpest criticism
of this run:

> *"house-vocabulary coupling: question 1 scores the literal word `repeated` and question 5
> scores knowledge of one specific verification protocol, so a substantively correct answer
> using different labels or a different sound procedure is marked wrong, while a compliant
> answer with weak reasoning passes."*

That is a real threat to Q5's win: only the `with` arm was handed our vocabulary, so part
of what looks like competence is label matching. **Q5 is discounted.**

The verdict survives the discount. **Q3 and Q4 still win in both repeats**, and neither is
vocabulary-coupled — Q3 is refusing a measured verdict from an abstract while keeping
*reached* and *read* apart, Q4 is keeping a contradiction as two rows instead of resolving
it by preference. Both are substantive. The same grader called Q1 and Q3 the healthiest
sets, *"each carrying at least one item that a plausible wrong answer genuinely fails."*

## Two defects in the set, carried forward

**Entailed expectations, again.** Same disease as `skill-measure`: *"in questions 2, 4 and
5 two or three expectations are entailed by one another, so a set that looks like three
measurements delivers one or two, and scores are correspondingly inflated or crushed as a
block."* An all-or-nothing per-question score amplifies this in both directions.

**No negative items.** Nothing in the set punishes inventing a field that was not in the
source, restating a hedged figure as a number, or failing to deliver the artefact at all —
and the grader caught a live instance: *"one answer here that is truncated mid-deliverable
and lost no points for it."* Every set needs at least one expectation a *plausible wrong
answer* fails, not only one a lazy answer fails.

## What was not checked

The grader was not calibrated against a planted defect (phase 6.3, v2). Part of the +5%
token delta is the method text the `with` arm was handed. The `without` arm had this
repo's 84 existing skills available; whether any fired is recorded in each run's
`## consulted` section and was not analysed.

---

## Harness defects found while grading the artefact question, and what they nearly cost

Three bugs, all in the same question, all in code I wrote in this session. The artefact
question exercises the harness harder than any judgement question does, and it found what
the others could not.

**1 · The section parser broke on the answer's own headings.** It split on any `## ` line.
An answer that produces a SKILL.md contains `## Steps` inside it, so the parser cut the
artefact in half and the code grader reported *no file produced*.

**2 · Fence-awareness was not enough.** The winning answer had written the file **unfenced**,
as an indented walkthrough. That is a presentation choice, not a failure to deliver, and
the fixed parser still scored it as nothing. The rule is now inverted: **the harness
recognises its own markers (`## Qn`, `## consulted`) and nothing else.** An answer cannot
collide with a marker it was told to write.

**3 · The code grader punished the more complete answer.** It runs the contract checker on
the extracted SKILL.md alone, so a skill that correctly bundles an asset and points at it
fails `body.files-exist` and `ptr.resolves` — for a reason that is the checker's *context*,
not a defect in the artefact. Those rules and 22 others are now reported as
**not-decidable-here** rather than counted, using the same rule the rest of the system uses:
a check that could not run is not a failure and is not a pass.

**What it nearly cost.** Before the fixes the harness scored the arm that produced a
complete, contract-clean SKILL.md as having produced nothing, and the arm that produced a
simpler one as the winner. That is the inverted-conclusion class — the run completes, the
numbers look plausible, and the loser is reported as the winner. It was caught only because
a surprising per-question result was checked against the raw file before being written down.

The controls that existed did not catch it: `selftest_score.py` guards the *un-blinding*
against exactly this failure mode, and it passed throughout, because the inversion happened
one stage upstream of what it watches. **A control proves the thing it watches, and nothing
else** — the extractor now has 6 controls of its own, including both presentation forms.
