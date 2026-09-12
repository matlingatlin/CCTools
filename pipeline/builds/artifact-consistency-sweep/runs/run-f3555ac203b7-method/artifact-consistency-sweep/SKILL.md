---
name: artifact-consistency-sweep
description: "Use when a whole artefact - a skill, a runbook, a spec, a procedure with rules, a description and tests - has to be reviewed for internal contradictions in ONE pass: does the body contradict the rules, does a step end in nothing checkable, which step is graded by nothing, does the description promise what the body does not, is a named file missing. Triggers on review the whole skill, consistency sweep, steps vs rules vs evals, did the review miss anything, the last review was red again, unconverged review, contradictions between steps. Enumerates every step-rule, step-step, step-check, description-body, file-BOM and claim-rationale pair as a row with a verdict and a quote, then emits the findings list and the per-step matrix. NOT two adversarial reviewers converging over rounds (santa-method), NOT the mirror sides of a CODE contract (integration-contract-completeness), NOT checks weakened to buy a green run (oracle-weakening-audit), NOT acting on a reviewer's comments (receiving-code-review)."
---

# artifact-consistency-sweep — every pair, one pass

A review that reads an artefact as prose reports the contradictions it notices, and the next
review notices different ones. This sweep enumerates the pairs first and rules on each, so
one round reports every contradiction the text holds and says which pairs it examined.
The pair types, the row shape and the count are in `references/pair-vocabulary.md`.

## When to use
- A whole artefact is about to be measured or shipped and its parts must agree: a skill,
  a runbook, a spec, a procedure with rules and tests.
- A previous review was red, the text was rewritten, and the question is whether anything
  was missed - "did the review miss anything", "the review is red again".

**Not this skill:** two adversarial reviewers converging over rounds; the mirror sides of a
code contract; a check loosened to make a suite green; deciding what to do with a reviewer's
comments. Each is its own unit (`santa-method`, `integration-contract-completeness`,
`oracle-weakening-audit`, `receiving-code-review`).

## Steps
1. **Inventory the parts, and count them.** List every numbered step, every rule bullet,
   every description clause, every eval expectation, every bundled file and every file the
   bill of materials names. Write the counts down first: they are the plan count the report
   is checked against (7 steps × 4 rules = 28 step×rule rows owed).
2. **Enumerate the pairs, one row each, before judging any.** The six pair types and the
   row shape are in `references/pair-vocabulary.md`; open it now and write the rows for
   every type. The rows exist before the verdicts do; a pair with no row was not examined.
3. **Rule on every row** with one of the reference's five verdicts. Every verdict other
   than consistent carries a verbatim quote of the line that decides it. A row with no
   quote is not returned.
4. **Read each step's last sentence for an observable outcome.** If the sentence names no
   file, number, row, artefact or state that could be checked, the step's row is *unchecked*
   whatever the pairs said. Then find the expectation that grades it; none is *ungraded*.
5. **Classify each finding.** CLASS when fixing it changes a step or the description for
   every instance; INSTANCE when it is one line. Two rows on the same defect are one
   finding with two quotes, not two findings.
6. **Emit two things and nothing else:** the findings list (`level`, `where`, `finding`,
   `quote`) and the step matrix (`step`, `checkable`, `graded_by`) with the examined-pair
   counts per type beside the plan counts from step 1. A report whose examined count is
   below its plan count says so on its face.

## Rules
- Enumerate before judging: the plan count is written before the first verdict.
- No quote, no finding.
- Say what was examined, not only what was found: the counts go in the report.

## In this repo (one instance)
Runs as the whole-artefact review (phase 5.2) of the skill-builder chain, dispatched through
`pipeline/build/dispatch.py` with the artefact and `bom.json` as its declared inputs. The
record that motivated it: `pipeline/builds/llm-wiki-ingest` - three reviews of one skill,
each red at class level on a different set, two findings verbatim in a text the earlier
review passed. Steps are numbered `N. **...**` in this repository's skills, rules are the
bullets under `## Rules`, expectations live in `evals/evals.json`, the bill of materials in
the build's `bom.json`.
