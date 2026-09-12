# The pairs a sweep enumerates, the two row shapes, and the plan counts

Sources: the build record named under *In this repo* in SKILL.md (three whole-artefact reviews of
one skill, read 2026-09-03) and a checker-design rule, one row per examined pair, from a
sibling skill (read 2026-09-03). Expires when a review of any artefact finds a contradiction
that fits none of the seven pair types below.

## What counts as a step, a rule, a clause, an expectation, a file

- **step**: an item of the artefact's numbered procedure (any ordered list of actions).
- **rule**: a sentence that forbids, requires or bounds what the procedure may do, wherever it stands - a bullet under a heading named Rules, Constraints, Invariants or Never, and also a never/must/only sentence inside a step or the introduction. The heading is where rules usually live, not what makes one; a rule inside a step is counted once, as a rule.
- **description clause**: a span of the artefact's summary or description field, split at
  "NOT", semicolons and sentence ends.
- **expectation**: one entry of the artefact's test assertions (an evals file, a test list, a
  checklist the artefact says it is graded by). An artefact with no test assertions has zero
  expectations; the step×check type then has a plan count of zero and is reported as such.
- **file**: a file present in the bundle, a row of its bill of materials, or a path the
  artefact's text names. The artefact's own top-level document is the thing under review,
  not a bundled file; it is not a file×BOM row.

## seven pair types

| pair type | one row per | plan count | a contradiction looks like |
|---|---|---|---|
| **step × rule** | each step against each rule | steps × rules | a rule forbids what a step orders; a rule no step could obey |
| **step × step** | each step against the next, and against any step that uses a term it defines | (steps − 1) + one per term used by two steps, counted after reading every step | "stop" in a branch before a later step that says "in every branch"; one term defined at two scopes |
| **step × check** | each step against each expectation | steps × expectations (zero when the artefact has none) | a step no expectation grades; an expectation no step produces |
| **description × body** | each description clause against the body | clauses | the description promises what the body does not produce |
| **file × bill of materials** | each file present, each BOM row and each path the text names, against the other two sets | files present + BOM rows + named paths | a named path absent from the bundle; a file nothing points at |
| **step × instance section** | every step against the 'In this repo' section | the instance section adds a requirement the general step does not carry, or contradicts it (the portability seam) | field trial 2026-09-03: the skill under review treated a repo path as an input |
| **claim × rationale** | each rule against its stated evidence | rules | a rule with no observed failure behind it; a rationale contradicting the rule it justifies |

## Two row shapes

**Pair row** - `type | left | right | verdict | quotes`. Three verdicts: consistent,
contradiction, absent (something named that does not exist; its quote is the naming line).

**Step row** - `step | closing sentence | checkable | graded_by | quote`. *Checkable* means the
closing sentence points at something a reader could inspect: a file, a number, a row, a named
artefact or a named state; anything else is *unchecked*. *graded_by* names the expectation that
covers the step, or reads *ungraded*. The quote is the closing sentence. These rows are the
matrix the report emits.

## The plan count and the ledger

The counts follow from the formulas above once the parts are identified; two of them (shared
terms, named paths) are known only after the artefact has been read once, so the counts are
written after that first read and before any verdict. The ledger repeats them beside the
examined counts and lists the examined pairs by `type:left×right`, so a reader sees which pairs
were ruled, not only how many. *For example*, 7 steps, 4 rules and 9 expectations owe 28
step×rule rows and 63 step×check rows; 6 steps and 3 rules owe 18 step×rule rows.
