Read all three files plus the BOM, identified the parts (6 steps, 3 rules, 6 pair types, 3 eval entries / 29 expectations, 3 bundle files, 41 BOM rows), and ran the pairs.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md description vs references/pair-vocabulary.md (description × body)",
      "finding": "The reference defines six pair types, but the description advertises only five (step×rule, step-checkable, step×check, description×body, file×BOM) plus 'contradictions between steps' in the triggers. The sixth type, claim × rationale — 'a rule with no observed failure behind it' — is promised nowhere in the description, so a reader routing by description never learns the sweep rules on rule-evidence, and the one output sentence that lists what is emitted does not mention it either.",
      "quote": "Enumerates every pair as a row with a verdict, then emits the ledger of examined pairs, the findings with quotes and the per-step matrix."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, prompts of evals 1, 2 and 3 vs SKILL.md step 2",
      "finding": "All three eval prompts instruct a FIVE-type sweep, enumerating the same five types the description does. Step 2 orders 'one pair row per pair for all six types'. The prompts therefore contradict the procedure they are meant to grade: an output that omits claim × rationale entirely satisfies every prompt, and no expectation names the sixth type. The skill's mandated sixth pair type is exercised by nothing.",
      "quote": "steps against rules, steps against each other, steps against the eval expectations, the description against the body, bundled files against the bill of materials."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules bullet 1 vs step 6 vs evals/evals.json expectations (step × check)",
      "finding": "Rule 1's entire content is report ORDER, and step 6 repeats it ('Emit the report in this order'). No expectation in any of the three evals grades order — they check that a ledger, a findings list and a matrix are each present, never that the ledger precedes the findings. Rules 2 and 3 are each graded ('every finding carries a verbatim quote', 'no two findings share a quote'); rule 1 is graded by nothing, and it is the rule the In-this-repo record calls the motivating failure.",
      "quote": "The ledger is the first part of the report, so a reader sees what was examined before what was found."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 vs step 5 / Rules bullet 3 (step × step, step × rule)",
      "finding": "Step 3 requires a contradiction to quote BOTH lines that disagree, so one line is quoted by every defect it participates in. Step 5 and rule 3 forbid two findings from sharing a quote. When one line takes part in two genuinely distinct defects — the common case for a step that contradicts both a rule and a later step — the rules force either merging two unrelated defects into one finding or dropping a quote step 3 requires. The expectation 'no two findings share a quote (step 5, rule 3)' grades conformance to the losing side, so the artefact pays a recall cost to satisfy a de-duplication rule written for a different situation (two rows on ONE defect).",
      "quote": "A contradiction quotes the two lines that disagree; an absent quotes the line that names the missing thing."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 and references/pair-vocabulary.md 'The plan count and the ledger' (claim × rationale)",
      "finding": "'before any verdict' is a rule with no observed failure behind it. The reference justifies writing the counts AFTER the first read (two counts are unknowable before it) but never justifies writing them BEFORE any verdict, and the In-this-repo record — which supplies an observed failure for each of the three Rules bullets — records nothing about counts written late. It is the only ordering constraint in the body that no review incident supports.",
      "quote": "The six counts open the ledger, before any verdict."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, the ledger expectation in all three evals (step × check)",
      "finding": "Step 1 orders the plan counts computed 'with the reference's formulas', and the reference gives six formulas including two derived ones (shared terms, named paths). The only expectation covering step 1 grades the PRESENCE of plan and examined counts, not their conformance to those formulas. An output that invents plan numbers, or applies steps×steps instead of (steps−1)+shared-terms, passes the expectation as written; the formulas — the reference's main contribution — are graded by nothing visible in the expectation text.",
      "quote": "a ledger with plan and examined counts per pair type and the examined pairs named (steps 1, 6)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md description vs evals/evals.json, all three eval prompts",
      "finding": "The description claims three artefact kinds; all three fixtures are the same kind (successive rewrites of one skill artefact), and each prompt hard-codes 'the whole skill artefact'. Neither non-skill kind is exercised, and the pair vocabulary is written in skill terms ('an evals file, a test list, a checklist') that the evals never test against a spec or a runbook.",
      "quote": "a skill, a spec with tests, a runbook with a checklist"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json, eval 3: expected_output vs expectations",
      "finding": "Eval 3's expected_output promises the grader measures recall 'including the ones the round's own reviewer missed', but eval 3's expectations list — unlike evals 1 and 2 — carries no 'recall over the findings the round's own reviewer MISSED' row. The stated grading and the graded expectations disagree for this entry; the expectations list is 9 rows where the others are 10.",
      "quote": "recall over the findings three independent reviewers established for this text (including the ones the round's own reviewer missed), a precision proxy, and the matrix's completeness."
    },
    {
      "level": "INSTANCE",
      "where": "references/pair-vocabulary.md, Sources line",
      "finding": "One of the reference's two sources is unnamed, so the borrowed rule that governs the ledger's row-per-examined-pair shape cannot be checked against its origin by a later reader — the same defect the skill's own rule 2 exists to prevent for findings ('a non-consistent verdict without its quoted line is not a finding').",
      "quote": "and a checker-design rule, one row per examined pair, from a sibling skill (read 2026-09-03)"
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```

**Question 4 — clean.** `## In this repo (one instance)` is the only place naming host-repo paths (`pipeline/build/dispatch.py`, `pipeline/builds/llm-wiki-ingest`, `bom.json`, `.claude`-style wiring). The body's "Not this skill" paragraph phrases the siblings by job rather than by name, and `references/pair-vocabulary.md` deliberately refers to its source as "the build record named under *In this repo* in SKILL.md" instead of the path. The only borderline case is the four sibling skill names inside the `description` field, and the section explicitly discloses and instructs on that ("a copy elsewhere replaces them with its own or phrases them by job"). No finding.

**Question 2 — every step closes on something inspectable** (counts in the ledger, rows, quoted lines, matrix quotes, level fields, emitted report), and each has at least one expectation naming it by number. The gaps are not in step *checkability* but in what the expectations actually assert: order (step 6/rule 1) and formula conformance (step 1) are named by expectations that do not test them, and INSTANCE-level labelling from step 5 is graded only through the CLASS-recall row.