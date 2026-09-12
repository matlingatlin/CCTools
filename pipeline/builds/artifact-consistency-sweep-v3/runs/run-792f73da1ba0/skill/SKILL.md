---
name: artifact-consistency-sweep
description: "Use when a whole artefact (artifact) that has a procedure, rules and test assertions - a skill, a spec, a runbook - has to be reviewed for internal contradictions in ONE pass: does the body contradict the rules, do two steps contradict each other, does a step end in nothing checkable, which step is graded by nothing, does the description promise more than the body, is a named file missing, does a rule have no rationale, does the repo section contradict a step. Triggers on review the whole skill, consistency sweep, did the review miss anything, the last review was red again. Ledgers every pair it ruled on, findings with quotes, a per-step matrix. NOT two adversarial reviewers converging over rounds, NOT the mirror sides of a code contract, NOT checks weakened for a green run, NOT acting on a reviewer's comments, NOT writing a skill's fields, NOT deciding what a gate may report, NOT designing what a checker returns."
---

# artifact-consistency-sweep — every pair, one pass

A review that reads an artefact as prose reports the contradictions it notices, and the next
review notices different ones. This sweep plans its pairs first and rules on each, and its
ledger shows every pair it ruled on: a contradiction missed is traceable to a pair, not
to a reader's attention. What counts as a step, a rule, a clause, an
expectation or a file, the seven pair types, the two row shapes and the plan-count formulas
are in `references/pair-vocabulary.md`, which steps 1, 2 and 4 apply.

## When to use
- An artefact with a procedure, rules and test assertions is about to be measured or
  shipped and its parts must agree.
- A previous review was red, the text was rewritten, and the question is whether anything
  was missed - "did the review miss anything", "the review is red again".

**Not this skill:** two adversarial reviewers converging over rounds; the mirror sides of a
code contract; a check loosened to make a suite green; what to do with a reviewer's
comments; writing a skill's fields; deciding what a gate or checker may report.

## Steps
1. **Read the artefact once, identify the parts by the reference's definitions, and write
   the seven plan counts.** Count the parts: steps, rules, description clauses, expectations,
   files present, bill-of-materials rows, paths the text names, and whether an instance
   section exists. Then compute one plan count per pair type with the reference's formulas.
   The part counts and then the seven plan counts open the ledger.
2. **Enumerate the rows:** one pair row per planned pair for all seven types (`type | left |
   right`, the verdict and quotes columns empty until step 3) and one step row per step
   (`step | closing sentence`, the checkable, graded_by and quote columns empty until step
   4). The pair rows are the ledger's pair list and the step rows become the matrix. A
   contradiction noticed while reading that fits no type gets a pair row of type `other`.
3. **Rule on every pair row:** consistent, contradiction, absent, or unpointed. A
   contradiction quotes the two lines that disagree; an absent quotes the line that names the
   missing thing; an unpointed (a file nothing names) quotes the sweep's own listing entry,
   written `listing: <path>`.
4. **Rule on every step row** by the reference's definition of checkable, and name the
   expectation that grades it or write ungraded; the row's quote is the closing sentence.
5. **Merge rows into findings.** Rows on one defect become one finding whose `quotes` list
   holds every quote its rows carried. Level CLASS when the fix changes what the method says
   for every artefact it is run on - a step, a rule, the description, a reference definition,
   or an expectation shared across evals; INSTANCE when the fix is local to one place. An
   `other` row becomes a finding whose `where` is the reference's pair-type table.
6. **Emit the report as one JSON object with the keys `ledger`, `findings`, `matrix`, in
   that order:** the ledger (the part counts from step 1, with a quote for each rule counted
   outside a Rules heading; then per pair type: plan count, examined count, the examined
   pairs as `type:left×right`, the rows with a non-consistent verdict, and any `other` rows),
   then the findings (`level`, `where`, `finding`, `quotes`), then the step matrix (`step`,
   `checkable`, `graded_by`, `quote`). A report whose examined counts all equal their plan
   counts is complete; any other report is marked `incomplete` and names its unruled pairs.

## Rules
- The reference's definitions decide what a step, a rule or a file is, not the reviewer's
  own - a field trial took a rule to be a bullet under a Rules heading and missed the one
  inside a step.
- The report carries the ledger of examined pairs - three reviews of one skill each reported
  findings and nothing about what they had examined, so a fourth could not tell a missed
  pair from a consistent one.
- An incomplete report (a budget, a timeout) names its unruled pairs and carries the mark
  `incomplete`; it is not a sweep - the first build's runs emitted no ledger at all, so a
  short sweep and a complete one looked the same.
- The findings count is at most the count of non-consistent pair rows plus the unchecked or
  ungraded step rows - the first build's runs emitted up to 29 findings for 7 known defects.
- A non-consistent verdict without its quoted line is not a finding - the one finding
  without a quote in those reviews could not be located afterwards.
- A defect reported twice is one finding carrying all its quotes - two rows on one defect
  went out as two findings in the first of those reviews.
- No bill of materials supplied: the BOM-row count is 0 and the ledger says `no BOM
  supplied`; files present are still paired against the paths the text names, so an absent
  named path and a file nothing names are still found. The sweep does not invent a BOM -
  the field trial had no BOM and the sweep skipped the whole pair type.
- A path named but absent is quoted by the sentence naming it; a file nothing names gets
  the verdict unpointed and the sweep's own listing entry as its quote - the field trial
  found such a file and had no line to quote for it.

## In this repo (one instance)
Built to run as the whole-artefact review (phase 5.2) of the skill-builder chain, dispatched
through `pipeline/build/dispatch.py` with the artefact and `bom.json` as its declared inputs;
not yet routed there - `evals.md` says why. Here a step is a `N. **...**` line, a rule a
bullet under `## Rules` or a binding sentence elsewhere per the reference, an expectation an
entry of `evals/evals.json`, the bill of materials the build's `bom.json`. The three reviews
the rules cite are `pipeline/builds/llm-wiki-ingest` (one skill, each review red at class
level on a different set; six of the seven pair types occurred there; `evals.md` names the
record under Origin); the field trial they cite is the first build's, recorded in `evals.md`,
on the `skill-measure` skill - the seventh pair type, step x instance section, comes from it.
The checker-design rule the reference cites lives in `validation-evidence`, a skill in the
sister repository `matlingatlin/Scio` (`.claude/skills/validation-evidence`), not in this
library. Paths in this section and in `evals.md` are host paths: a sweep of this bundle
lists them as `host:<path>`, per the reference's file definition.
