---
name: artifact-consistency-sweep
description: "Use when a whole artefact - a skill, a runbook, a spec, a procedure with rules, a description and tests - has to be reviewed for internal contradictions in ONE pass: does the body contradict the rules, does a step end in nothing checkable, which step is graded by nothing, does the description promise what the body does not, is a named file missing. Triggers on review the whole skill, consistency sweep, steps vs rules vs evals, did the review miss anything, the last review was red again, unconverged review, contradictions between steps. Enumerates every pair as a row with a verdict, then emits the findings with quotes, the per-step matrix and a ledger of what was examined. NOT two adversarial reviewers converging over rounds (santa-method), NOT a code contract's mirror sides (integration-contract-completeness), NOT checks weakened to buy a green run (oracle-weakening-audit), NOT what a gate may report (gate-verdicts), NOT acting on review comments (receiving-code-review)."
---

# artifact-consistency-sweep — every pair, one pass

A review that reads an artefact as prose reports the contradictions it notices, and the next
review notices different ones. This sweep enumerates the pairs first and rules on each, so
one round reports every contradiction the text holds and says which pairs it examined.
The six pair types, the two row shapes and the plan-count formulas are in
`references/pair-vocabulary.md`; open it at step 1.

## When to use
- A whole artefact is about to be measured or shipped and its parts must agree: a skill,
  a runbook, a spec, a procedure with rules and tests.
- A previous review was red, the text was rewritten, and the question is whether anything
  was missed - "did the review miss anything", "the review is red again".

**Not this skill:** two adversarial reviewers converging over rounds; the mirror sides of a
code contract; a check loosened to make a suite green; what a gate is allowed to report;
what to do with a reviewer's comments. Each is its own unit, named in the description.

## Steps
1. **Inventory the parts and write the plan counts first.** Count the numbered steps, the
   rule bullets, the description clauses, the eval expectations, the files present and the
   bill-of-materials rows; compute the plan count per pair type with the reference's
   formulas. Write the six numbers as the first line of your report before any verdict -
   that line is what makes step 2 checkable.
2. **Enumerate the pair rows, then the step rows.** One pair row per pair (`type | left |
   right`) for all six types, one step row per numbered step (`step | last sentence`), all
   still without verdicts. A pair or step with no row was not examined.
3. **Rule on every pair row:** consistent, contradiction, or absent. A contradiction quotes
   the two lines that disagree; an absent quotes the line that names the missing thing.
4. **Rule on every step row:** checkable or unchecked (the last sentence names no file,
   number, row, artefact or state), and graded_by an expectation or ungraded. Both quote
   the step's last sentence.
5. **Merge rows into findings.** Rows on one defect become one finding carrying every
   quote its rows carried (`quotes` is a list). Level CLASS when fixing it changes a step
   or the description for every instance; INSTANCE when it is one line.
6. **Emit three things:** the findings (`level`, `where`, `finding`, `quotes`), the step
   matrix (`step`, `checkable`, `graded_by`), and the ledger (per pair type: plan count,
   examined count, rows with a non-consistent verdict). An examined count below its plan
   count is stated in the ledger, not hidden.

## Rules
- The plan counts are the first line of the report; a report that starts with a finding
  did not enumerate.
- A non-consistent verdict without its quoted line is not a finding.
- A defect reported twice is one finding with two quotes.

## In this repo (one instance)
Runs as the whole-artefact review (phase 5.2) of the skill-builder chain, dispatched through
`pipeline/build/dispatch.py` with the artefact and `bom.json` as its declared inputs. Steps
here are `N. **...**` lines, rules the bullets under `## Rules`, expectations
`evals/evals.json`, the bill of materials the build's `bom.json`; the bill lists bundled
files and not SKILL.md itself, which the checker treats as the artefact rather than a
bundled file. The record that motivated the method: `pipeline/builds/llm-wiki-ingest` -
three reviews of one skill, each red at class level on a different set; the pair types were
each seen there (the Rules line vs steps 2 and 7 in round 1; "stop" vs steps 6-7 and
"disputed" at two scopes in round 2; step 3 graded by nothing in rounds 0-1; five repo-local
names in the description in round 2; check.py named by twenty expectations and absent in
round 1; the disputed branch with no rationale in round 2). The three rules above are
guards from those reviews: r0 and r1 findings carried quotes, and the one finding without
one could not be located afterwards; two rows on one defect were reported as two findings
in r1; every review reported findings and nothing about what it had examined.
