# The pairs a sweep enumerates, the two row shapes, and the plan counts

Sources (provenance; a copy keeps this line as history): three whole-artefact reviews of one
skill in the host repository's build record (read 2026-09-03) and the checker-design rule 'one
row per examined pair' from a checker-design skill in the host's sister repository (read
2026-09-03). SKILL.md's instance section names both and gives their host paths. An `other` row (SKILL.md step 2) is the signal that the taxonomy
below is incomplete: the report carries it as a finding against this table, and whoever
maintains the reference adds the type.

## What counts as a step, a rule, a clause, an expectation, a file

- **step**: an item of the artefact's numbered procedure (any ordered list of actions).
- **rule**: a bullet under a heading named Rules, Constraints, Invariants or Never. A sentence
  outside such a heading that binds a step other than the one it stands in (a never, must or
  only about another step) is counted as a rule for the step × rule pairs and listed by quote
  in the ledger's part counts; it is not a claim × rationale row, because the artefact does
  not present it as a rule with evidence - its lack of a heading is itself reported once, as
  a step × rule finding. A step's own imperative is the step, not a rule.
- **description clause**: a span of the artefact's summary or description field, split at
  "NOT", semicolons and sentence ends.
- **expectation**: one entry of the artefact's test assertions (an evals file, a test list, a
  checklist the artefact says it is graded by). An artefact with no test assertions has zero
  expectations; the step×check plan count is then the step count and every step row reads
  ungraded.
- **file**: a file present in the bundle, a row of its bill of materials, or a path named by
  any bundled document other than a test fixture (paths inside fixtures belong to the fixture
  artefacts). A path under the artefact's instance section, or a path into the host repository
  that a bundled record cites, is a host path: the ledger lists it as `host:<path>` and it is
  not a file × bill of materials row. The artefact's own top-level document is the thing under review,
  not a bundled file; it is not a file×BOM row.

## seven pair types

A pair row pairs one part with another part, or one part with a set of parts (a step with the
expectations, a clause with the body); the plan-count column says which.

| pair type | one row per | plan count | a contradiction looks like |
|---|---|---|---|
| **step × rule** | each step against each rule | steps × rules | a rule forbids what a step orders; a rule no step could obey |
| **step × step** | each step against every other step | steps × (steps − 1) / 2 | "stop" in a branch before a later step that says "in every branch"; one term defined at two scopes; a row shape declared twice |
| **step × check** | each expectation against the set of steps (which step produces what it grades); the step row of the matrix answers the converse, which expectation grades each step | expectations (0 when the artefact has none: the matrix then reads ungraded on every step) | an expectation no step produces; a step no expectation grades (from the matrix) |
| **description × body** | each description clause against the body | clauses | the description promises what the body does not produce |
| **file × bill of materials** | each file present, each BOM row and each path the text names, against the other two sets | files present + BOM rows + named paths | a named path absent from the bundle; a file nothing points at |
| **step × instance section** | every step against the 'In this repo' section | steps, when the artefact has an instance section; 0 otherwise | the instance section adds a requirement the general step does not carry, or contradicts it (the portability seam) - a repository path treated as an input, an artefact-specific tool a step assumes |
| **claim × rationale** | each rule under a Rules heading against its stated evidence | rules under the heading | a rule with no observed failure behind it; a rationale contradicting the rule it justifies |

## Two row shapes

**Pair row** - `type | left | right | verdict | quotes`. Four verdicts: consistent,
contradiction, absent (something named that does not exist; its quote is the naming line),
unpointed (a file present that nothing names; its quote is the sweep's own listing entry,
`listing: <path>`).

**Step row** - `step | quote | checkable | graded_by`. The quote is the step's deliverable
sentence: the sentence that states what the step produces, which is the closing sentence unless
the step ends in an aside. *Checkable* means that sentence points at something a reader could
inspect: a file, a number, a row, a named artefact or a named state; anything else is
*unchecked*. *graded_by* names the expectation that covers the step, or reads *ungraded*. These
rows are the matrix the report emits.

## The plan count and the ledger

The counts follow from the formulas above once the parts are identified; two of the parts
(paths the text names, whether an instance section exists) are known only after the artefact
has been read once, so the seven counts are written after that first read and before any
verdict. The ledger repeats them beside the
examined counts and lists the examined pairs by `type:left×right`, so a reader sees which pairs
were ruled, not only how many. *For example*, 7 steps, 4 rules and 9 expectations owe 28
step×rule rows, 21 step×step rows and 9 step×check rows; 6 steps and 3 rules owe 18 step×rule
rows and 15 step×step rows.
