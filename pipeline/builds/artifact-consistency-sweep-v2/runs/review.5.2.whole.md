I reviewed all four bundle files plus `bom.json`, enumerated the pair types the skill itself defines, and checked each step's closing sentence against the eval expectations that would grade it.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md ## Rules, bullet 1 vs references/pair-vocabulary.md, file × bill of materials row",
      "finding": "The no-BOM rule zeroes a count the reference's formula cannot make zero. The reference computes file×BOM as 'files present + BOM rows + named paths'; with no BOM supplied, files present and named paths still exist, so the plan count is non-zero. Following the rule suppresses the whole pair type and with it the 'a named path absent from the bundle' defect the In-this-repo record cites as an actually observed failure (check.py named by twenty expectations, absent from the bundle).",
      "quote": "No bill of materials supplied: the file x BOM count is 0 and the ledger says `not applicable: no BOM`; the sweep does not invent one."
    },
    {
      "level": "CLASS",
      "where": "references/pair-vocabulary.md, 'seven pair types' table, step × instance section row",
      "finding": "The plan-count cell of the step × instance-section row holds prose describing a contradiction instead of a count formula, and the 'a contradiction looks like' cell holds a field-trial note. Step 1 orders the plan count computed 'with the reference's formulas' for every pair type, so this type's ledger row cannot be computed at all — the columns are shifted by one and the type is unenumerable.",
      "quote": "the instance section adds a requirement the general step does not carry, or contradicts it (the portability seam)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 vs references/pair-vocabulary.md, step × step formula and 'The plan count and the ledger'",
      "finding": "Step 1's list of seven counts omits the shared-term count that the step×step formula requires — '(steps − 1) + one per term used by two steps'. The reference states that 'two of them (shared terms, named paths) are known only after the artefact has been read once', but step 1 names only named paths, so a sweep that follows step 1 literally cannot compute one of the seven plan counts. The list also counts parts, while step 6's ledger is per pair type; 'the seven counts' equivocates between the two.",
      "quote": "description clauses, expectations, files present, bill-of-materials rows and named paths"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, expectations of evals 1, 2 and 3 vs SKILL.md ## Rules",
      "finding": "Every eval's rule cross-references are off by two, left over from a three-rule version. 'rule 1' is now the no-BOM rule, not the ledger-first rule (bullet 3); 'rule 3' is now the ledger-first rule, not the no-shared-quote rule (bullet 5). Any grader or reader resolving these citations lands on the wrong rule in all three eval entries.",
      "quote": "the ledger precedes the findings in the report (rule 1)"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, prompts of evals 1-3 vs references/pair-vocabulary.md 'seven pair types' and SKILL.md description",
      "finding": "The prompts enumerate five pair types. step × instance section and claim × rationale appear in no prompt, no expected_output and no expectation — two of the seven types the method requires are graded by nothing, and the description's list of what the sweep looks for ('does the body contradict the rules… is a named file missing') does not promise them either. The evals cannot detect a with-arm that silently drops both types.",
      "quote": "steps against rules, steps against each other, steps against the eval expectations, the description against the body, bundled files against the bill of materials"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json expectation 12 (all three evals) vs SKILL.md ## Rules bullet 5 and step 5",
      "finding": "The check is weaker than the rule it grades. The rule forbids any shared quote; the expectation only forbids an identical quotes SET, so two findings on one defect that share one of two quotes pass while violating the rule. evals.md records this as the only grading for that scenario ('S5 a defect reported twice · graded by the no-shared-quotes check only'), so the merge step in step 5 is effectively ungraded.",
      "quote": "no two findings share the same quotes set (rule 3)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md premise (lines 8-10) vs evals/evals.json recall expectations and evals.md verdict",
      "finding": "The body's headline promise is that one round reports every contradiction; the evals grade the same behaviour as passing at 0.60 recall (0.70 on CLASS), and evals.md's own table records with-arm recall of 0.82/0.64 on artifact-B and an ABANDON verdict. The claim the artefact is built around is contradicted by the assertions that grade it, in every instance.",
      "quote": "one round reports every contradiction the text holds and lists the pairs it examined"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6, closing sentence",
      "finding": "Step 6's closing sentence ends in something checkable but no expectation grades it: the ledger expectation asks only for 'plan and examined counts per pair type and the pair ids'. A report that omits the shortfall statement entirely passes all twelve checks.",
      "quote": "A shortfall of examined against plan is stated in the ledger."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs evals/evals.json expectation 6 and the expected_output of all three evals",
      "finding": "Step 4 and the reference's step-row shape require a quote column in the step matrix, but the expectation checks only 'checkable and graded_by', and expected_output describes the matrix as '(checkable? graded by which check?)'. The quote column of the matrix is graded by nothing.",
      "quote": "the row's quote is the closing sentence"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md ## In this repo (one instance) vs ## Rules",
      "finding": "The rationale sentence attributes three rules to the three llm-wiki-ingest reviews, but the Rules section carries five bullets. Two of them — the no-BOM rule and the unpointed-file quote rule — trace to the later skill-measure field trial recorded in evals.md ('no rule for a missing bill of materials; no quote rule for an unpointed file'), so inside SKILL.md those two rules stand with no observed failure behind them. This is the artefact's own claim × rationale defect.",
      "quote": "The three rules are guards from those reviews"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md ## In this repo (one instance), the parenthetical record",
      "finding": "The claim that every pair type was seen in that record is not supported: the parenthetical lists six occurrences for seven types, and evals.md records 'no pair type for step x instance-section' as a gap the later field trial found — so that type demonstrably was not seen in those reviews. Either description × body or step × instance section has no cited instance.",
      "quote": "each pair type was seen there"
    },
    {
      "level": "INSTANCE",
      "where": "bom.json, row for references/pair-vocabulary.md vs the file itself and SKILL.md line 11",
      "finding": "The BOM's account of the reference is stale: the file's heading reads '## seven pair types' with seven table rows and a '## Two row shapes' section, and SKILL.md says 'the seven pair types, the two row shapes'. The BOM row still describes the six-type, one-row-shape version.",
      "quote": "the six pair types with what a contradiction looks like in each, the row shape, the plan count"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json prompts 1-3 vs bom.json",
      "finding": "Every prompt names SKILL.md and references/ inside its fixture, but the BOM lists no SKILL.md row for artifact-A, artifact-B or artifact-C, and no references/ path for artifact-A at all (only artifact-B and artifact-C carry references/rationale.md). Paths the prompts name are absent from the bill of materials — the same absent-path defect the method exists to catch.",
      "quote": "Review the whole skill artefact at evals/files/artifact-A (SKILL.md, references/, evals/)"
    },
    {
      "level": "INSTANCE",
      "where": "bom.json, fixture rows",
      "finding": "A grader copy exists inside fixture C only and nothing points at it: all three evals name evals/files/check.py as the grader, and artifact-A and artifact-B have no counterpart to this nested file. It is a bundled file no prompt, expectation or expected_output references.",
      "quote": "evals/files/artifact-C/evals/files/check.py"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json, eval 3: expected_output vs expectations",
      "finding": "Eval 3's expected_output promises grading over the findings the round's own reviewer missed, but eval 3's expectation list drops the 'recall over the findings the round's own reviewer MISSED >= 0.50' check that evals 1 and 2 carry. The stated grading and the actual checks disagree within one entry, with no note explaining the asymmetry.",
      "quote": "including the ones the round's own reviewer missed"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Scenarios' vs references/pair-vocabulary.md 'expectation' definition and SKILL.md Rules bullet 1",
      "finding": "The two branches added after the field trial — an artefact with no expectations, and an artefact with no BOM — are exercised by no fixture. All three fixtures are skill bundles with evals and a BOM, so the zero-expectation plan count and the not-applicable ledger line are asserted by the reference and the rules but graded by nothing.",
      "quote": "S4 a runbook without expectations · not executed (the round-2 review named this gap)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 14 vs line 28",
      "finding": "'four gaps' is followed by five semicolon-separated gaps, and line 28 then treats the miscount as additional to the four ('The field trial's four gaps and the miscount first'). This is a recurrence of the exact defect the field trial reported — a count word naming a different number of things — now inside the record of that finding.",
      "quote": "four gaps in the method it named itself"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 3 (portability seam)",
      "finding": "In SKILL.md and references/, host-repo paths are confined to the 'In this repo (one instance)' section, and the reference defers to it rather than naming paths; the description's four sibling-unit names are the one exception and that section explicitly discloses them. evals.md is the only other bundle file naming a host path — defensible for a measurement record, but it is a second location and the instance section does not cover it.",
      "quote": "**Last eval:** 2026-09-03, the second v3 build (`pipeline/builds/artifact-consistency-sweep`"
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```

Direct answers to the four questions:

1. **Steps contradict rules and the reference in three places** — the no-BOM rule zeroes a count the reference's formula makes non-zero; step 1's seven counts omit the shared-term count step×step needs; the step×instance row has no computable plan count for step 1 to apply.
2. **All six steps close on something inspectable**, but two closing sentences are graded by nothing (step 6's shortfall statement, step 4's quote column), and two whole pair types (step×instance, claim×rationale) appear in no prompt or expectation. Grading map: step 1 → the step×rule plan-count check + ledger check (only 1 of 7 plan counts verified); step 2 → the Rules-examined check only; step 3 → the non-empty-quotes check (no check on the three-verdict vocabulary); step 4 → the matrix check, minus the quote column; step 5 → the 3x precision proxy and CLASS-recall checks, with the no-shared-quote rule graded by a weaker set-equality check; step 6 → the ledger-precedes-findings check, minus the shortfall.
3. **Yes** — within SKILL.md, Rules bullets 1 and 2 have no observed failure behind them; the rationale sentence claims three rules for five bullets, and the evidence for those two lives only in evals.md.
4. **Effectively yes** for SKILL.md and references/ — the description's sibling names are the disclosed exception, and evals.md's build path is the one uncovered mention.