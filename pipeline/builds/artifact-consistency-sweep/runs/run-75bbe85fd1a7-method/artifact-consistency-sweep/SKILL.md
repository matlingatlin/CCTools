---
name: artifact-consistency-sweep
description: "Use when a whole artefact that has a procedure, rules and test assertions - a skill, a spec with tests, a runbook with a checklist - has to be reviewed for internal contradictions in ONE pass: does the body contradict the rules, does a step end in nothing checkable, which step is graded by nothing, does the description promise what the body does not, is a named file missing. Triggers on review the whole skill, consistency sweep, steps vs rules vs evals, did the review miss anything, the last review was red again, unconverged review, contradictions between steps. Enumerates every pair as a row with a verdict, then emits the ledger of examined pairs, the findings with quotes and the per-step matrix. NOT two adversarial reviewers converging over rounds (santa-method), NOT a code contract's mirror sides (integration-contract-completeness), NOT checks weakened to buy a green run (oracle-weakening-audit), NOT acting on review comments (receiving-code-review)."
---

# artifact-consistency-sweep — every pair, one pass

A review that reads an artefact as prose reports the contradictions it notices, and the next
review notices different ones. This sweep enumerates the pairs first and rules on each, so
one round reports every contradiction the text holds and lists the pairs it examined. What
counts as a step, a rule, a clause, an expectation or a file, the six pair types, the two
row shapes and the plan-count formulas are in `references/pair-vocabulary.md`; open it at
step 1 and apply its definitions, not your own.

## When to use
- An artefact with a procedure, rules and test assertions is about to be measured or
  shipped and its parts must agree.
- A previous review was red, the text was rewritten, and the question is whether anything
  was missed - "did the review miss anything", "the review is red again".

**Not this skill:** two adversarial reviewers converging over rounds; the mirror sides of a
code contract; a check loosened to make a suite green; what to do with a reviewer's
comments. Each is its own unit, named in the description.

## Steps
1. **Read the artefact once, identify the parts by the reference's definitions, and write
   the plan counts.** Count the steps, rules, description clauses, expectations, files
   present, bill-of-materials rows and named paths; compute the plan count per pair type
   with the reference's formulas. The six counts open the ledger, before any verdict.
2. **Enumerate the pair rows, then the step rows,** with no verdicts yet: one pair row per
   pair for all six types (`type | left | right`), one step row per step (`step | closing
   sentence`). A pair or step with no row was not examined.
3. **Rule on every pair row:** consistent, contradiction, or absent. A contradiction quotes
   the two lines that disagree; an absent quotes the line that names the missing thing.
4. **Rule on every step row** by the reference's definition of checkable, and name the
   expectation that grades it or write ungraded; the row's quote is the closing sentence.
5. **Merge rows into findings.** Rows on one defect become one finding whose `quotes` list
   holds every quote its rows carried; no two findings share a quote. Level CLASS when
   fixing it changes a step or the description for every instance; INSTANCE when it is one
   line.
6. **Emit the report in this order:** the ledger (per pair type: plan count, examined
   count, the examined pairs as `type:left×right`, and the rows with a non-consistent
   verdict), then the findings (`level`, `where`, `finding`, `quotes`), then the step
   matrix (`step`, `checkable`, `graded_by`, `quote`). A shortfall of examined against
   plan is stated in the ledger.

## Rules
- The ledger is the first part of the report, so a reader sees what was examined before
  what was found.
- A non-consistent verdict without its quoted line is not a finding.
- A defect reported twice is one finding with two quotes; no two findings share a quote.

## In this repo (one instance)
Runs as the whole-artefact review (phase 5.2) of the skill-builder chain, dispatched through
`pipeline/build/dispatch.py` with the artefact and `bom.json` as its declared inputs. Here
a step is a `N. **...**` line, a rule a bullet under `## Rules`, an expectation an entry of
`evals/evals.json`, the bill of materials the build's `bom.json`. The record that motivated
the method: `pipeline/builds/llm-wiki-ingest` - three reviews of one skill, each red at class
level on a different set; each pair type was seen there (the Rules line vs steps 2 and 7 in
round 1; "stop" vs steps 6-7 and "disputed" at two scopes in round 2; step 3 graded by nothing
in rounds 0-1; five repo-local names in the description in round 2; check.py named by twenty
expectations and absent from the bundle in round 1; the disputed branch with no rationale in
round 2). The three rules are guards from those reviews: the one finding without a quote could
not be located afterwards; two rows on one defect were reported as two findings in round 1;
every review reported findings and nothing about what it had examined - which is why the
ledger comes first. The sibling units named in the description are this repository's; a copy
elsewhere replaces them with its own or phrases them by job.
