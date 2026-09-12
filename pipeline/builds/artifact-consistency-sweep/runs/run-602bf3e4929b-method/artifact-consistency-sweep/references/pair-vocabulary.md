# The pairs a sweep enumerates, and what a contradiction looks like in each

Sources: this repository's build record `pipeline/builds/llm-wiki-ingest` (three whole-artefact
reviews, read 2026-09-03) and Scio's `validation-evidence` skill (the one-row-per-examined-pair rule,
read 2026-09-03). Expires when a fourth review of that artefact finds a pair type not listed here.

The report of a sweep says what was examined, not only what was found. Six pair types cover a skill-shaped artefact (a
procedure with rules, a description, bundled files and evals); the same six apply to any
document that has steps, constraints, a summary and tests.

| pair type | one row per | a contradiction looks like | seen in the record |
|---|---|---|---|
| **step × rule** | every numbered step against every rule bullet | a rule forbids what a step orders ("runs nothing" vs "run the lint"); a rule is stated nowhere a step could obey it | llm-wiki-ingest r1: Rules line vs steps 2, 7 |
| **step × step** | every step against the ones it hands off to | a branch that says "stop" before a later step that says "in every branch"; two steps defining one term at two scopes | r2: step 2 "stop" vs steps 6-7; "disputed" at row scope and page scope |
| **step × check** | every step against every eval expectation | a step graded by no expectation; an expectation with no step behind it; a check that passes on the untouched fixture | r0/r1: step 3 graded by nothing; T2 LOG row vacuous |
| **description × body** | every clause of the description against the body | the description names units the body does not; a trigger the body cannot serve | r2: five repo-local names in the description |
| **bundled file × bill of materials** | every file listed against every file present, both directions | a grader the expectations name that is not in the bundle; a file present that nothing points at | r1: check.py named by 20 expectations, absent |
| **claim × rationale** | every body rule against its stated evidence | a rule with no observed failure behind it; a rationale that contradicts the rule it justifies | r2: disputed branch with no rationale entry |

## The row

`pair | left | right | verdict | quote | level`. Verdict is one of **consistent** ·
**contradiction** · **unchecked** (the step ends in nothing observable) · **ungraded** (no
check covers it) · **absent** (a named thing does not exist). Level: CLASS or INSTANCE, as SKILL.md step 5
defines them. Any verdict other than consistent is accompanied by the deciding line, quoted.

## Why the count matters

The pair count is the plan count: with 7 steps, 4 rules and 9 expectations the sweep owes
28 step×rule rows, 6 step×step rows and 63 step×check rows before it says anything. A
report with 11 findings and no row count cannot be told apart from a report that examined
11 pairs. That is the one-row-per-examined-pair rule from checker design, applied to a
review.
