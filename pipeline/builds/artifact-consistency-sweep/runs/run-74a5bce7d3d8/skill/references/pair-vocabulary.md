# The pairs a sweep enumerates, the two row shapes, and the plan counts

Sources: the build record named under *In this repo* in SKILL.md (three whole-artefact reviews of
one skill, read 2026-09-03) and a checker-design rule, one row per examined pair, from a
sibling skill (read 2026-09-03). Expires when a review of any artefact finds a contradiction
that fits none of the six pair types below.

## Six pair types

| pair type | one row per | plan count | a contradiction looks like |
|---|---|---|---|
| **step × rule** | each numbered step against each rule bullet | steps × rules | a rule forbids what a step orders; a rule no step could obey |
| **step × step** | each step against the step(s) it hands off to, and against any step that names the same term | (steps − 1) + one per shared term | "stop" in a branch before a later step that says "in every branch"; one term defined at two scopes |
| **step × check** | each step against each eval expectation | steps × expectations | a step no expectation grades; an expectation no step produces; a check that passes on the untouched fixture |
| **description × body** | each description clause (split at "NOT", commas and semicolons) against the body | clauses | the description promises what the body does not produce; a trigger the body cannot serve |
| **file × bill of materials** | each file present against the BOM and each BOM row against the files | files present + BOM rows | a named grader absent from the bundle; a file nothing points at |
| **claim × rationale** | each rule bullet and each imperative step sentence against its stated evidence | rules + imperative sentences | a rule with no observed failure behind it; a rationale contradicting the rule it justifies |

Each was seen at least once in the record that motivated this skill; the *In this repo* section
of SKILL.md says where.

## Two row shapes

**Pair row** - `type | left | right | verdict | quotes`. Three verdicts: consistent,
contradiction, absent (something named that does not exist; its quote is the naming line).

**Step row** - `step | last sentence | checkable | graded_by`. Checkable means the closing
sentence points at something observable; graded_by names the expectation that covers the step,
or reads ungraded. Its quote is that closing sentence. These rows form the matrix.

## The plan count

The formulas above give the numbers SKILL.md step 1 asks for; the ledger repeats them beside
the examined counts. *For example*, an artefact with 7 steps, 4 rules and 9
expectations owes 28 step×rule rows, at least 6 step×step rows and 63 step×check rows; an
artefact with 6 steps and 3 rules owes 18 step×rule rows. A shortfall of examined against owed rows for any type belongs in the ledger; no ledger, no
enumeration.
