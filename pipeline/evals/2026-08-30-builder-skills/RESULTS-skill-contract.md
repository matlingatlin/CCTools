# skill-contract — round 1

Run 2026-08-30. 5 questions × 2 arms × 2 repeats = 20 answers, graded blind.

## Against the preregistered rule: passes

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats per question | pass | |
| no correctness regression | pass | no question where the baseline met every expectation and the skill arm did not |
| ≥1 win surviving both repeats | pass | **Q1, Q3, Q4, Q5** won in *both* repeats; Q2 won in r2 only |
| cost | **observed, not gated** | see AMENDMENT 1 |

Score: **with 5/5 and 5/5 · without 1/5 and 0/5.**

Cost, observed: `with` averaged 64,195 tokens against `without` 61,473 — **+4.4%**, well inside
the contract's 20% tolerance. Tool calls identical at 2. The caveat from AMENDMENT 1 stands:
the `with` prompt carries ~8k characters of method the other never receives, so an unknown
part of that 4.4% is input it was handed rather than work it chose to do.

## And the measurement that produced it is weak — both graders said so, independently

This is the part that matters more than the score. The preregistered method asks each grader
to attack the expectation set, and the two attacked it the same way without seeing each other:

> *"every expectation grades declared process, and four of the five questions can be passed
> without producing the artefact they ask for … Three expectations are effectively unfailable
> given the leading framing."* — r1

> *"Of the twelve expectations, roughly half are satisfied by reciting a principle rather than
> obeying it, and several are cued directly by the question's own wording … nothing tests
> whether a remembered value was asserted as fact, so both answers state the 1,024 cap from
> memory in Q3 while both are scored as exemplary on 'does not restate rules from memory' in
> Q5."* — r2

Both also named the fix, and named it the same: the discriminating expectations are the ones
that require **a concrete artefact** or **an action at a named moment** — the bill of materials
exists, the contract was read *at write time*, the checker ran *before* the reader. The
recitable ones do not discriminate.

**Triage: test bug, not skill bug.** Nothing here says the method is wrong; it says the test
cannot tell a method being followed from a method being recited. Repairing the skill on this
would be repairing the thing that is not broken — which is why phase 7.2 exists.

## Two defects, and only one of them is expensive

| | Defect | Fix | Cost |
| --- | --- | --- | --- |
| a | expectations grade recital | rewrite them and **regrade the answers already on disk** | no new runs |
| b | questions are leading — Q3 hands over the offending number, Q5 flags itself as a trap | rewrite the prompts | new arm-runs |

## A harness finding, separate from the result

The arms are relabelled A/B **per question**, and the graders were not told that. Their
per-expectation rulings are unaffected and are all the verdict uses — but both wrote free-text
summaries treating A and B as stable identities across the set, so r1's *"split verdict, not a
sweep"* is describing labels, not arms. Unblinding it shows the same arm winning four of five.

Fix: tell the grader the labels are re-randomised per question, so it does not write a
cross-question narrative it has no basis for. **The prose overall field must not be used for
any verdict** — score.py already ignores it, which is the only reason this cost nothing.

## Status

`skill-contract` **passes its preregistered rule on a measurement its own graders call weak.**
That is not a ship. It goes back through 7.2 with the expectation set rewritten toward the
pattern both graders named, and the leading prompts replaced.
