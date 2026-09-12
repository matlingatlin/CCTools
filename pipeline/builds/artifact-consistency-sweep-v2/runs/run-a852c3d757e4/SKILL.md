---
name: artifact-consistency-sweep
description: "Use when a whole artefact that has a procedure, rules and test assertions - a skill, a spec, a runbook - has to be reviewed for internal contradictions in ONE pass: does the body contradict the rules, do two steps contradict each other, does a step end in nothing checkable, which step is graded by nothing, does the description promise more than the body, is a named file missing, does a rule have no rationale, does the repo section contradict a step. Triggers on review the whole skill, consistency sweep, did the review miss anything, the last review was red again. Rules on every pair; emits the ledger of examined pairs, findings with quotes, per-step matrix. NOT two adversarial reviewers converging over rounds (santa-method), NOT a code contract's mirror sides (integration-contract-completeness), NOT checks weakened for a green run (oracle-weakening-audit), NOT acting on review comments (receiving-code-review), NOT writing a skill's fields (skill-contract), NOT deciding what a gate or checker may report."
---

# artifact-consistency-sweep — every pair, one pass

A review that reads an artefact as prose reports the contradictions it notices, and the next
review notices different ones. This sweep enumerates the pairs first and rules on each, so
one round rules on every pair it planned and says so in a ledger: a pair the ledger does not
list was not examined, and a contradiction missed there is traceable to that pair rather than
to a reader's attention. What counts as a step, a rule, a clause, an expectation or a file,
the seven pair types, the two row shapes and the plan-count formulas are in
`references/pair-vocabulary.md`; open it at step 1.

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
   files present, bill-of-materials rows, paths the text names, terms used by two steps, and
   whether an instance section exists. Then compute one plan count per pair type with the
   reference's formulas. The seven plan counts open the ledger.
2. **Enumerate the rows:** one pair row per pair for all seven types (`type | left | right`),
   one step row per step (`step | closing sentence`). These rows are the ledger's pair list:
   a pair or step with no row is not examined and cannot be ruled on. A contradiction noticed
   while reading that fits none of the seven types gets a row of type `other`.
3. **Rule on every pair row:** consistent, contradiction, or absent. A contradiction quotes
   the two lines that disagree; an absent quotes the line that names the missing thing.
4. **Rule on every step row** by the reference's definition of checkable, and name the
   expectation that grades it or write ungraded; the row's quote is the closing sentence.
5. **Merge rows into findings.** Rows on one defect become one finding whose `quotes` list
   holds every quote its rows carried. Level CLASS when the fix changes what the method says
   for every artefact it is run on - a step, a rule, the description, a reference definition,
   or an expectation every eval shares; INSTANCE when the fix is local to one place and
   changes nothing else.
6. **Emit the report in this order:** the ledger (per pair type: plan count, examined count,
   the examined pairs as `type:left×right`, the rows with a non-consistent verdict, and any
   `other` rows), then the findings (`level`, `where`, `finding`, `quotes`), then the step
   matrix (`step`, `checkable`, `graded_by`, `quote`). An examined count under its plan
   count is a defect of the sweep, not a licence: the ledger states it with its reason (a
   budget the caller set, a run cut short), so the reader knows which pairs went unruled.

## Rules
Each rule carries the observed failure behind it; a rule without one is itself a
claim × rationale finding.
- The reference's definitions decide what a step, a rule or a file is, not the reviewer's
  own - a field trial took a rule to be a bullet under a Rules heading and missed the one
  inside a step.
- The ledger is the first part of the report - three reviews of one skill each reported
  findings and nothing about what they had examined, so a fourth could not tell a missed
  pair from a consistent one.
- A non-consistent verdict without its quoted line is not a finding - the one finding
  without a quote in those reviews could not be located afterwards.
- A defect reported twice is one finding with two quotes; no two findings share a quote -
  two rows on one defect went out as two findings in the first of those reviews.
- No bill of materials supplied: the BOM-row count is 0 and the ledger says `no BOM
  supplied`; files present are still paired against the paths the text names, so an absent
  named path and a file nothing points at are still found. The sweep does not invent a
  BOM - the field trial had no BOM and the sweep skipped the whole pair type.
- A file nothing points at, or a path named but absent, is quoted by the line that lists or
  names it (the directory listing line, or the sentence naming the path) - the field trial
  found such a file and had no line to quote for it.

## In this repo (one instance)
Runs as the whole-artefact review (phase 5.2) of the skill-builder chain, dispatched through
`pipeline/build/dispatch.py` with the artefact and `bom.json` as its declared inputs. Here a
step is a `N. **...**` line, a rule a bullet under `## Rules` or a constraint sentence
elsewhere per the reference, an expectation an entry of `evals/evals.json`, the bill of
materials the build's `bom.json`. The three reviews the rules cite are
`pipeline/builds/llm-wiki-ingest` (one skill, each review red at class level on a different
set; six of the seven pair types occurred there); the field trial they cite is the first
build's, recorded in `evals.md`, on the `skill-measure` skill - the seventh pair type, step x
instance section, comes from it. The NOT-clauses of the description name this repository's
units; a copy elsewhere names its own or keeps the phrasing by job. `evals.md`, the
measurement record, is the other bundled file that names this repository's paths.
