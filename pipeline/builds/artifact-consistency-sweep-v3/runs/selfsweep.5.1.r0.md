The artefact under review is byte-identical to the skill I was told to follow (SKILL.md and references/pair-vocabulary.md both diff clean), so this is a self-review; I applied the method as written. 228 pair rows planned, 181 ruled, 47 left unruled (the withheld fixture files), 4 `other` rows, 31 non-consistent rows, 15 findings — 10 CLASS, 5 INSTANCE.

```json
{
 "artefact": "artifact-consistency-sweep (./artifact: SKILL.md, references/pair-vocabulary.md, evals/evals.json, evals.md, bom.json)",
 "method": "artifact-consistency-sweep (mounted read-only), steps 1-6",
 "ledger": {
  "plan_counts": {
   "step × rule": 66,
   "step × step": 15,
   "step × check": 56,
   "description × body": 10,
   "file × bill of materials": 64,
   "step × instance section": 6,
   "claim × rationale": 11,
   "total_pair_rows": 228,
   "step_rows": 6
  },
  "per_pair_type": [
   {
    "pair_type": "step×rule",
    "plan_count": 66,
    "examined_count": 66,
    "examined_pairs": [
     "step×rule:S1×R1", "step×rule:S1×R2", "step×rule:S1×R3", "step×rule:S1×R4", "step×rule:S1×R5", "step×rule:S1×R6", "step×rule:S1×R7", "step×rule:S1×R8", "step×rule:S1×R9", "step×rule:S1×R10", "step×rule:S1×R11",
     "step×rule:S2×R1", "step×rule:S2×R2", "step×rule:S2×R3", "step×rule:S2×R4", "step×rule:S2×R5", "step×rule:S2×R6", "step×rule:S2×R7", "step×rule:S2×R8", "step×rule:S2×R9", "step×rule:S2×R10", "step×rule:S2×R11",
     "step×rule:S3×R1", "step×rule:S3×R2", "step×rule:S3×R3", "step×rule:S3×R4", "step×rule:S3×R5", "step×rule:S3×R6", "step×rule:S3×R7", "step×rule:S3×R8", "step×rule:S3×R9", "step×rule:S3×R10", "step×rule:S3×R11",
     "step×rule:S4×R1", "step×rule:S4×R2", "step×rule:S4×R3", "step×rule:S4×R4", "step×rule:S4×R5", "step×rule:S4×R6", "step×rule:S4×R7", "step×rule:S4×R8", "step×rule:S4×R9", "step×rule:S4×R10", "step×rule:S4×R11",
     "step×rule:S5×R1", "step×rule:S5×R2", "step×rule:S5×R3", "step×rule:S5×R4", "step×rule:S5×R5", "step×rule:S5×R6", "step×rule:S5×R7", "step×rule:S5×R8", "step×rule:S5×R9", "step×rule:S5×R10", "step×rule:S5×R11",
     "step×rule:S6×R1", "step×rule:S6×R2", "step×rule:S6×R3", "step×rule:S6×R4", "step×rule:S6×R5", "step×rule:S6×R6", "step×rule:S6×R7", "step×rule:S6×R8", "step×rule:S6×R9", "step×rule:S6×R10", "step×rule:S6×R11"
    ],
    "non_consistent_rows": [
     {"row": "step×rule:S1×R1", "verdict": "contradiction", "finding": "F2"},
     {"row": "step×rule:S6×R1", "verdict": "contradiction", "finding": "F4"},
     {"row": "step×rule:S3×R7", "verdict": "contradiction", "finding": "F5"},
     {"row": "step×rule:S3×R11", "verdict": "contradiction", "finding": "F1"},
     {"row": "step×rule:S4×R10", "verdict": "contradiction", "finding": "F6"}
    ]
   },
   {
    "pair_type": "step×step",
    "plan_count": 15,
    "examined_count": 15,
    "examined_pairs": [
     "step×step:S1×S2", "step×step:S1×S3", "step×step:S1×S4", "step×step:S1×S5", "step×step:S1×S6",
     "step×step:S2×S3", "step×step:S2×S4", "step×step:S2×S5", "step×step:S2×S6",
     "step×step:S3×S4", "step×step:S3×S5", "step×step:S3×S6",
     "step×step:S4×S5", "step×step:S4×S6", "step×step:S5×S6"
    ],
    "non_consistent_rows": [
     {"row": "step×step:S2×S6", "verdict": "contradiction", "finding": "F3"},
     {"row": "step×step:S3×S6", "verdict": "contradiction", "finding": "F1"},
     {"row": "step×step:S4×S5", "verdict": "contradiction", "finding": "F6"}
    ]
   },
   {
    "pair_type": "step×check",
    "plan_count": 56,
    "examined_count": 56,
    "examined_pairs": [
     "step×check:S1×expectations", "step×check:S2×expectations", "step×check:S3×expectations", "step×check:S4×expectations", "step×check:S5×expectations", "step×check:S6×expectations",
     "step×check:E1.1×steps", "step×check:E1.2×steps", "step×check:E1.3×steps", "step×check:E1.4×steps", "step×check:E1.5×steps", "step×check:E1.6×steps", "step×check:E1.7×steps", "step×check:E1.8×steps", "step×check:E1.9×steps", "step×check:E1.10×steps", "step×check:E1.11×steps", "step×check:E1.12×steps", "step×check:E1.13×steps", "step×check:E1.14×steps", "step×check:E1.15×steps", "step×check:E1.16×steps", "step×check:E1.17×steps",
     "step×check:E2.1×steps", "step×check:E2.2×steps", "step×check:E2.3×steps", "step×check:E2.4×steps", "step×check:E2.5×steps", "step×check:E2.6×steps", "step×check:E2.7×steps", "step×check:E2.8×steps", "step×check:E2.9×steps", "step×check:E2.10×steps", "step×check:E2.11×steps", "step×check:E2.12×steps", "step×check:E2.13×steps", "step×check:E2.14×steps", "step×check:E2.15×steps", "step×check:E2.16×steps", "step×check:E2.17×steps",
     "step×check:E3.1×steps", "step×check:E3.2×steps", "step×check:E3.3×steps", "step×check:E3.4×steps", "step×check:E3.5×steps", "step×check:E3.6×steps", "step×check:E3.7×steps", "step×check:E3.8×steps", "step×check:E3.9×steps", "step×check:E3.10×steps", "step×check:E3.11×steps", "step×check:E3.12×steps", "step×check:E3.13×steps", "step×check:E3.14×steps", "step×check:E3.15×steps", "step×check:E3.16×steps"
    ],
    "non_consistent_rows": [
     {"row": "step×check:S1×expectations", "verdict": "contradiction", "finding": "F16"},
     {"row": "step×check:S2×expectations", "verdict": "contradiction", "finding": "F9"},
     {"row": "step×check:S5×expectations", "verdict": "contradiction", "finding": "F7"},
     {"row": "step×check:S6×expectations", "verdict": "contradiction", "finding": "F1"},
     {"row": "step×check:E1.1×steps", "verdict": "contradiction", "finding": "F8"},
     {"row": "step×check:E2.1×steps", "verdict": "contradiction", "finding": "F8"},
     {"row": "step×check:E3.1×steps", "verdict": "contradiction", "finding": "F8"},
     {"row": "step×check:E1.5×steps", "verdict": "contradiction", "finding": "F7"},
     {"row": "step×check:E2.5×steps", "verdict": "contradiction", "finding": "F7"},
     {"row": "step×check:E3.5×steps", "verdict": "contradiction", "finding": "F7"},
     {"row": "step×check:E1.16×steps", "verdict": "contradiction", "finding": "F1"},
     {"row": "step×check:E2.16×steps", "verdict": "contradiction", "finding": "F1"},
     {"row": "step×check:E3.16×steps", "verdict": "contradiction", "finding": "F1"}
    ],
    "note": "Row per step = which expectation grades it; row per expectation = which step produces it. Expectation numbering follows evals/evals.json order within each eval."
   },
   {
    "pair_type": "description×body",
    "plan_count": 10,
    "examined_count": 10,
    "examined_pairs": [
     "description×body:C1×body", "description×body:C2×body", "description×body:C3×body", "description×body:C4×body", "description×body:C5×body",
     "description×body:C6×body", "description×body:C7×body", "description×body:C8×body", "description×body:C9×body", "description×body:C10×body"
    ],
    "non_consistent_rows": [
     {"row": "description×body:C1×body", "verdict": "contradiction", "finding": "F6"},
     {"row": "description×body:C3×body", "verdict": "contradiction", "finding": "F1"}
    ],
    "note": "Clauses split at NOT, semicolons and sentence ends: C1 the Use-when sentence with its eight questions, C2 the Triggers sentence, C3 'Rules on every pair...', C4 'emits its ledger...', C5-C10 the six NOT clauses."
   },
   {
    "pair_type": "file×bom",
    "plan_count": 64,
    "examined_count": 17,
    "examined_pairs": [
     "file×bom:present:references/pair-vocabulary.md×other-two-sets",
     "file×bom:present:evals/evals.json×other-two-sets",
     "file×bom:present:evals.md×other-two-sets",
     "file×bom:present:bom.json×other-two-sets",
     "file×bom:bom-row:b1 evals/evals.json×other-two-sets",
     "file×bom:bom-row:b41 references/pair-vocabulary.md×other-two-sets",
     "file×bom:bom-row:b43 evals.md×other-two-sets",
     "file×bom:named-path:p1 references/pair-vocabulary.md×other-two-sets",
     "file×bom:named-path:p2 SKILL.md×other-two-sets",
     "file×bom:named-path:p3 evals/evals.json×other-two-sets",
     "file×bom:named-path:p4 evals.md×other-two-sets",
     "file×bom:named-path:p5 bom.json×other-two-sets",
     "file×bom:named-path:p6 pipeline/build/dispatch.py×other-two-sets",
     "file×bom:named-path:p7 pipeline/builds/llm-wiki-ingest×other-two-sets",
     "file×bom:named-path:p8 pipeline/builds/artifact-consistency-sweep-v2×other-two-sets",
     "file×bom:named-path:p9 pipeline/builds/artifact-consistency-sweep×other-two-sets",
     "file×bom:named-path:p17 decide.py×other-two-sets"
    ],
    "non_consistent_rows": [
     {"row": "file×bom:bom-row:b43 evals.md×other-two-sets", "verdict": "contradiction", "finding": "F13"}
    ],
    "pairs_left_unruled": {
     "count": 47,
     "why": "The review request withholds the eval fixture files the bill of materials lists, so their presence cannot be ruled on from this bundle.",
     "bom_rows_unruled": "b2-b40 and b42 (40 rows): every evals/files/** row - the three fixture artefacts artifact-A/B/C and their nested evals, the two copies of check.py, truth-A/B/C.json",
     "named_paths_unruled": "p10-p16 (7 paths): evals/files/artifact-A, evals/files/artifact-B, evals/files/artifact-C, evals/files/truth-A.json, evals/files/truth-B.json, evals/files/truth-C.json, evals/files/check.py"
    },
    "note": "bom.json is present and named by SKILL.md ('with the artefact and `bom.json` as its declared inputs') but carries no BOM row of its own; it is the bill of materials, not an item in it - ruled consistent, not absent. The five repository paths outside the bundle (pipeline/build/dispatch.py, pipeline/builds/llm-wiki-ingest, pipeline/builds/artifact-consistency-sweep-v2, pipeline/builds/artifact-consistency-sweep, decide.py) are named by the instance section and evals.md, are out of bundle scope, and are ruled consistent."
   },
   {
    "pair_type": "step×instance section",
    "plan_count": 6,
    "examined_count": 6,
    "examined_pairs": [
     "step×instance:S1×in-this-repo", "step×instance:S2×in-this-repo", "step×instance:S3×in-this-repo",
     "step×instance:S4×in-this-repo", "step×instance:S5×in-this-repo", "step×instance:S6×in-this-repo"
    ],
    "non_consistent_rows": []
   },
   {
    "pair_type": "claim×rationale",
    "plan_count": 11,
    "examined_count": 11,
    "examined_pairs": [
     "claim×rationale:R1×its stated evidence", "claim×rationale:R2×its stated evidence", "claim×rationale:R3×its stated evidence",
     "claim×rationale:R4×its stated evidence", "claim×rationale:R5×its stated evidence", "claim×rationale:R6×its stated evidence",
     "claim×rationale:R7×its stated evidence", "claim×rationale:R8×its stated evidence", "claim×rationale:R9×its stated evidence",
     "claim×rationale:R10×its stated evidence", "claim×rationale:R11×its stated evidence"
    ],
    "non_consistent_rows": [
     {"row": "claim×rationale:R8×its stated evidence", "verdict": "absent", "finding": "F10"},
     {"row": "claim×rationale:R9×its stated evidence", "verdict": "absent", "finding": "F10"},
     {"row": "claim×rationale:R10×its stated evidence", "verdict": "absent", "finding": "F10"}
    ],
    "note": "R1-R7, the seven bullets under ## Rules, each close with the observed failure behind them and are ruled consistent. R11 is covered by the rationale of R3 (bullet 3)."
   }
  ],
  "other_rows": [
   {"row": "other:O1 evals.md open set × the bundled SKILL.md and references/pair-vocabulary.md", "verdict": "contradiction", "finding": "F12"},
   {"row": "other:O2 evals.md grader-check counts × evals/evals.json expectation counts", "verdict": "contradiction", "finding": "F14"},
   {"row": "other:O3 references/pair-vocabulary.md Sources line × the source it cites", "verdict": "absent", "finding": "F15"},
   {"row": "other:O4 SKILL.md step 1 'paths the text names' × references/pair-vocabulary.md file definition", "verdict": "contradiction", "finding": "F16"}
  ],
  "totals": {
   "pair_rows_planned": 228,
   "pair_rows_examined": 181,
   "pair_rows_unruled": 47,
   "other_rows": 4,
   "step_rows_planned": 6,
   "step_rows_examined": 6,
   "non_consistent_rows": 31,
   "findings": 15
  },
  "shortfall": "file × bill of materials: 17 examined against a plan of 64. The 47 unruled rows are named above with their reason (fixture files withheld from this review). Every other pair type's examined count equals its plan count."
 },
 "parts_identified_at_step_1": {
  "steps": 6,
  "rules": 11,
  "rules_detail": {
   "under_Rules_heading": 7,
   "binding_sentences_outside_the_heading_quoted_for_audit": [
    {"id": "R8", "where": "SKILL.md intro", "quote": "are in `references/pair-vocabulary.md`; open it at step 1."},
    {"id": "R9", "where": "SKILL.md step 2", "quote": "The ledger lists exactly these rows."},
    {"id": "R10", "where": "SKILL.md step 5", "quote": "The findings count is at most the count of non-consistent rows."},
    {"id": "R11", "where": "SKILL.md step 6", "quote": "Every examined count equals its plan count, or the ledger names the pairs left unruled and why."}
   ]
  },
  "description_clauses": 10,
  "expectations": 50,
  "expectations_detail": "evals/evals.json: eval 1 = 17, eval 2 = 17, eval 3 = 16 (eval 3 omits the MISSED-rows expectation, per its own note)",
  "files_present": 4,
  "files_present_detail": "references/pair-vocabulary.md, evals/evals.json, evals.md, bom.json. SKILL.md is the artefact under review, not a bundled file (reference, 'What counts as ... a file').",
  "bom_rows": 43,
  "paths_the_text_names": 17,
  "instance_section_exists": true
 },
 "findings": [
  {
   "id": "F1",
   "level": "CLASS",
   "where": "SKILL.md intro (lines 8-11), frontmatter description clause C3, step 3, step 6; evals/evals.json expectation 16 of all three evals",
   "finding": "The sweep's central claim - a verdict on every planned pair - is asserted in three places, cancelled by step 6, and graded by nothing. The intro and the description say the sweep rules on every pair; step 3 orders a verdict on every pair row; step 6 then licenses an examined count below the plan count with no statement of when a shortfall is permitted, and the only expectation that touches completeness is the same disjunction, so a run that plans 66 step x rule pairs, examines two, and names the other 64 in the ledger passes every expectation. Disclosure is graded; completeness is not. This is the same defect the bundled record lists as an open CLASS item from the previous round, and expectation 16 as written does not close it.",
   "quotes": [
    "This sweep enumerates the pairs first and rules on each, and its ledger shows every pair it ruled on and every pair it left: a contradiction missed is traceable to a pair, not to a reader's attention.",
    "Rules on every pair of one artefact's own parts; emits its ledger of examined pairs, findings with quotes, per-step matrix.",
    "**Rule on every pair row:** consistent, contradiction, or absent.",
    "Every examined count equals its plan count, or the ledger names the pairs left unruled and why.",
    "every pair type's examined count equals its plan count, or the ledger names the unruled pairs (step 6, rule)"
   ]
  },
  {
   "id": "F2",
   "level": "CLASS",
   "where": "references/pair-vocabulary.md, 'What counts as...' expectation definition vs the 'seven pair types' table, step x check row; against SKILL.md rule 1 and step 1",
   "finding": "The reference gives two different plan counts for the same case. Its definition section says an artefact with no test assertions has a step x check plan count of zero; its table says the plan count in that case is the step count alone, with every step row reading ungraded. For a 6-step runbook the two readings owe 0 rows and 6 rows. Rule 1 makes the reference's definitions binding on the reviewer and step 1 orders the count computed from them, so a reviewer cannot compute the count the method requires. The zero-expectation artefact is exactly the case the description advertises ('a runbook'), the When-to-use bullet conditions the skill on having test assertions, and the bundled record shows the fixture for it was never executed - so no eval can catch which reading a run took.",
   "quotes": [
    "An artefact with no test assertions has zero expectations; the step×check type then has a plan count of zero and is reported as such.",
    "steps + expectations (steps alone when the artefact has none: every step row then reads ungraded)",
    "An artefact with a procedure, rules and test assertions is about to be measured or\n  shipped and its parts must agree.",
    "- S4 a runbook without expectations · not executed (no fixture; stated gap)"
   ]
  },
  {
   "id": "F3",
   "level": "CLASS",
   "where": "SKILL.md step 2 vs step 6 (and evals/evals.json expectation 17 of all three evals)",
   "finding": "Step 2 enumerates both row shapes - pair rows and one step row per step - and then states that the ledger lists exactly these rows. Step 6 puts only pair-type material in the ledger and emits the step rows as the third and last part of the report, after the findings; the expectation grades that order. The step rows are therefore both inside the ledger and after the findings, and a reader has to guess which. The same sentence also over-claims for the pair rows: step 6 emits the pair ids and only the non-consistent rows, not the rows themselves.",
   "quotes": [
    "The ledger lists exactly these rows.",
    "**Emit the report in this order:** the ledger (per pair type: plan count, examined count,\n   the examined pairs as `type:left×right`, the rows with a non-consistent verdict, and any\n   `other` rows), then the findings (`level`, `where`, `finding`, `quotes`), then the step\n   matrix (`step`, `checkable`, `graded_by`, `quote`).",
    "the report order is ledger, then findings, then the step matrix (step 6)"
   ]
  },
  {
   "id": "F4",
   "level": "CLASS",
   "where": "references/pair-vocabulary.md, rule definition vs SKILL.md step 6 (via rule 1)",
   "finding": "The reference requires the ledger to carry each rule counted outside a Rules heading as a quote, so the rule count can be audited - the audit trail for the one count the evals grade. Step 6's enumeration of what the ledger contains has no slot for it (plan count, examined count, pair ids, non-consistent rows, other rows), and no expectation asks for it. A sweep that follows step 6 exactly produces a rule count nobody can audit, which is the failure rule 1 was written for.",
   "quotes": [
    "The ledger's rule count lists each sentence counted outside the heading by quote, so the count\n  can be audited.",
    "**Emit the report in this order:** the ledger (per pair type: plan count, examined count,\n   the examined pairs as `type:left×right`, the rows with a non-consistent verdict, and any\n   `other` rows)",
    "The reference's definitions decide what a step, a rule or a file is, not the reviewer's\n  own - a field trial took a rule to be a bullet under a Rules heading and missed the one\n  inside a step."
   ]
  },
  {
   "id": "F5",
   "level": "CLASS",
   "where": "SKILL.md step 3 vs rule 7, and references/pair-vocabulary.md file x bill of materials row",
   "finding": "Step 3 offers exactly two quoting schemes: a contradiction quotes the two lines that disagree, an absent quotes the line that names the missing thing. Neither fits 'a file nothing points at', which the reference classes as a contradiction: by definition no line names such a file, so there is no second line and no naming line. Rule 7 patches the hole by directing the reviewer to quote a directory listing line - a line that is not part of the artefact under review, cannot be located in it afterwards, and is not reproducible by the grader that expectation 15 runs. The rule's own rationale states the gap ('had no line to quote for it') and the fix moves the quote outside the artefact rather than giving the verdict vocabulary a bucket for it.",
   "quotes": [
    "A contradiction quotes the two lines that disagree; an absent quotes the line that names the missing thing.",
    "A file nothing points at, or a path named but absent, is quoted by the line that lists or\n  names it (the directory listing line, or the sentence naming the path) - the field trial\n  found such a file and had no line to quote for it.",
    "a named path absent from the bundle; a file nothing points at",
    "a finding about an absent or unpointed file quotes a line that names the path (step 3, rule: quoted by the line that names it)"
   ]
  },
  {
   "id": "F6",
   "level": "CLASS",
   "where": "SKILL.md step 5 vs step 4 and description clause C1",
   "finding": "Step 5's cap on the findings count is defined over pair-row verdicts only, but step 4 produces step rows whose vocabulary is checkable/unchecked and graded_by/ungraded - never 'non-consistent'. An artefact whose pair rows are all consistent but whose step 5 closing sentence points at nothing inspectable yields a cap of zero, so the finding the description sells in its own words ('does a step end in nothing checkable') cannot be reported without breaking the cap. The cap silently excludes one of the two row shapes the method emits.",
   "quotes": [
    "The findings count is at most the count of non-consistent rows.",
    "**Rule on every step row** by the reference's definition of checkable, and name the\n   expectation that grades it or write ungraded; the row's quote is the closing sentence.",
    "does a step end in nothing checkable, which step is graded by nothing",
    "*Checkable* means the\nclosing sentence points at something a reader could inspect: a file, a number, a row, a named\nartefact or a named state; anything else is *unchecked*."
   ]
  },
  {
   "id": "F7",
   "level": "CLASS",
   "where": "SKILL.md step 5 closing sentence vs evals/evals.json expectation 5 of all three evals",
   "finding": "Step 5 is graded by nothing on the constraint it actually states. The only expectation that cites step 5 caps findings at three times the number of known findings - a precision proxy computed from the grader's truth file - while step 5's own cap is findings at most the count of non-consistent rows, a quantity the report itself carries and no expectation ever compares. A run can report ten findings off two non-consistent rows and pass. The step's closing sentence is the ungraded one in the matrix below.",
   "quotes": [
    "The findings count is at most the count of non-consistent rows.",
    "at most 3x as many findings as known ones (step 5)"
   ]
  },
  {
   "id": "F8",
   "level": "CLASS",
   "where": "evals/evals.json expectation 1 of all three evals vs SKILL.md step 6",
   "finding": "The expectation grades an output format that no step requires. Step 6 fixes the report's parts, their order and their fields but never says the report is JSON or otherwise machine-structured; the expectation cites step 6 for a requirement step 6 does not carry. A run that obeys step 6 exactly and emits the three parts as prose tables fails expectation 1 in all three evals, and the artefact gives the reviewer nowhere to read that JSON was wanted.",
   "quotes": [
    "findings are a structured JSON list (step 6)",
    "**Emit the report in this order:** the ledger (per pair type: plan count, examined count,\n   the examined pairs as `type:left×right`, the rows with a non-consistent verdict, and any\n   `other` rows), then the findings (`level`, `where`, `finding`, `quotes`), then the step\n   matrix (`step`, `checkable`, `graded_by`, `quote`)."
   ]
  },
  {
   "id": "F9",
   "level": "CLASS",
   "where": "references/pair-vocabulary.md 'other' row provision vs SKILL.md step 2 and step 6; evals/evals.json (all three evals)",
   "finding": "The 'other' row is the method's only tripwire for its taxonomy being incomplete, and it fires into nothing. The reference says an other row is the signal that the vocabulary is incomplete and that the new type is added to the reference when one appears - an action no step in the procedure carries and no gate performs. Step 2 creates the row, step 6 emits it, and not one of the 50 expectations mentions other rows, so a sweep that files three of them and a sweep that files none are graded identically. The taxonomy can be wrong indefinitely without any part of the artefact registering it.",
   "quotes": [
    "An `other` row (SKILL.md step 2) is the signal that the taxonomy\nbelow is incomplete: the new type is added here when one appears; until then the row stands as\n`other` in the report.",
    "A contradiction noticed while reading that fits\n   no type gets a row of type `other`.",
    "the rows with a non-consistent verdict, and any\n   `other` rows"
   ]
  },
  {
   "id": "F10",
   "level": "CLASS",
   "where": "SKILL.md intro, step 2, step 5 (the binding sentences the reference counts as rules) vs references/pair-vocabulary.md claim x rationale row and description clause C1",
   "finding": "The artefact fails its own claim x rationale type. The reference defines a rule heading-independently, so three binding sentences outside ## Rules count as rules of this artefact: 'open it at step 1' (intro), 'The ledger lists exactly these rows.' (step 2) and 'The findings count is at most the count of non-consistent rows.' (step 5). Each of the seven bullets under ## Rules closes with the observed failure behind it; none of these three carries any evidence, and the description advertises 'does a rule have no rationale' as a thing this sweep finds. Three of the artefact's eleven rules are the defect its own reference tells the reviewer to look for.",
   "quotes": [
    "**rule**: a bullet under a heading named Rules, Constraints, Invariants or Never, plus any\n  sentence outside such a heading that binds a step other than the one it stands in (a never,\n  must or only about another step).",
    "a rule with no observed failure behind it; a rationale contradicting the rule it justifies",
    "does a rule have no rationale",
    "are in `references/pair-vocabulary.md`; open it at step 1.",
    "The ledger lists exactly these rows.",
    "The findings count is at most the count of non-consistent rows."
   ]
  },
  {
   "id": "F12",
   "level": "INSTANCE",
   "where": "evals.md, 'The open set: review r2's findings, verbatim' vs the bundled SKILL.md and references/pair-vocabulary.md",
   "finding": "The bundled measurement record presents its open set as verbatim quotes of the current text and as the place the next iteration starts, but the quoted lines are not in this bundle - the text was rewritten past them. The step x step formula it quotes as adjacent-pairs-only now reads steps x (steps - 1) / 2; the 'Each rule carries the observed failure behind it' rule, the reference's expiry line, the description's parenthetical sibling names and step 5's 'and changes nothing else' no longer exist. Consequently no record in the bundle measures the text that ships: every recall, baseline and cost number in evals.md was produced against a superseded artefact, and a reader taking the open set as current would re-fix items already fixed.",
   "quotes": [
    "### The open set: review r2's findings, verbatim (the next iteration starts here)",
    "*Quote:* \"each step against the next, and against any step that uses a term it defines\"",
    "| **step × step** | each step against every other step | steps × (steps − 1) / 2 |",
    "*Quote:* \"Each rule carries the observed failure behind it; a rule without one is itself a claim × rationale finding.\""
   ]
  },
  {
   "id": "F13",
   "level": "INSTANCE",
   "where": "evals.md line 3 vs its own '## Second build (v2)' heading vs bom.json, the evals.md row",
   "finding": "One measurement carries three incompatible labels. The status line calls it the third v3 build while naming the v2 build directory; the section recording it is headed 'Second build (v2)'; and the bill of materials describes evals.md as the record of the first and second builds with the third appending - but no third-build section exists in the file, although this bundle is the third build's artefact. A reader cannot tell which build produced the ABANDON verdict the instance section points at for its 'not yet routed' claim.",
   "quotes": [
    "**Status: candidate, not routed** · **Last eval:** 2026-09-03, the third v3 build (`pipeline/builds/artifact-consistency-sweep-v2`, chain contract 3.1.1: review before arms).",
    "## Second build (v2), 2026-09-03",
    "\"why\": \"the measurement record of the first and second builds, kept as history; the third build appends\""
   ]
  },
  {
   "id": "F14",
   "level": "INSTANCE",
   "where": "evals.md, 'Grader changes in this build' heading vs evals/evals.json expectation lists",
   "finding": "The record states the grader runs 13 checks on fixtures A and B and 12 on C, while evals/evals.json carries 17 expectations for evals 1 and 2 and 16 for eval 3, and each eval's expected_output says check.py is what grades it. Four expectations per eval are unaccounted for in either direction and nothing in the artefact maps expectations onto checks, so a reader cannot tell whether four expectations are graded by nothing or the record's count is stale. check.py is withheld from this review, so the mismatch cannot be resolved from the bundle.",
   "quotes": [
    "### Grader changes in this build (both copies of check.py, 13 checks on A/B, 12 on C)",
    "Graded by evals/files/check.py against evals/files/truth-A.json: recall over the findings three independent reviewers established for this text (including the ones the round's own reviewer missed), a precision proxy, and the matrix's completeness."
   ]
  },
  {
   "id": "F15",
   "level": "INSTANCE",
   "where": "references/pair-vocabulary.md, Sources line",
   "finding": "The reference sources one of its two load-bearing design rules - one row per examined pair, the rule the whole ledger rests on - to 'a sibling skill' that it does not name, while rule 1 makes this reference binding on every reviewer. The other source is named and locatable through the instance section; this one cannot be checked by any reader, which is the same defect the claim x rationale type exists to catch.",
   "quotes": [
    "Sources: the build record named under *In this repo* in SKILL.md (three whole-artefact reviews of\none skill, read 2026-09-03) and a checker-design rule, one row per examined pair, from a\nsibling skill (read 2026-09-03)."
   ]
  },
  {
   "id": "F16",
   "level": "CLASS",
   "where": "SKILL.md step 1 vs references/pair-vocabulary.md file definition and the file x bill of materials plan-count formula; evals/evals.json (all three evals)",
   "finding": "'Paths the text names' is never scoped to a document set, so one of the seven plan counts is reviewer-dependent by construction. On this artefact the count is 6 if 'the text' means SKILL.md and 17 if it means every bundled file - a plan count of 53 or 64 for the same bundle - and nothing in the artefact decides it. Only the step x rule plan count is graded (and only as a lower bound), so two sweeps of the same artefact can report different plans for file x bill of materials, both passing, while step 6 asks the reader to compare examined against plan.",
   "quotes": [
    "Count the parts: steps, rules, description clauses, expectations,\n   files present, bill-of-materials rows, paths the text names, and whether an instance\n   section exists.",
    "**file**: a file present in the bundle, a row of its bill of materials, or a path the\n  artefact's text names.",
    "| **file × bill of materials** | each file present, each BOM row and each path the text names, against the other two sets | files present + BOM rows + named paths |",
    "the ledger's step x rule plan count is at least steps x Rules bullets for this artefact (step 1)"
   ]
  }
 ],
 "step_matrix": [
  {
   "step": "1",
   "checkable": "checkable",
   "graded_by": "E1.8 / E2.8 / E3.8 (ledger with plan and examined counts per pair type and the pair ids); also E*.10 for the step x rule count and E*.13 for the seven types",
   "quote": "The seven plan counts open the ledger."
  },
  {
   "step": "2",
   "checkable": "checkable",
   "graded_by": "ungraded - E*.7 ('rows referencing the artefact's rules exist') covers the rule rows of step 2, but no expectation of any eval mentions an `other` row, which is what this closing sentence provides for (see F9)",
   "quote": "A contradiction noticed while reading that fits no type gets a row of type `other`."
  },
  {
   "step": "3",
   "checkable": "checkable",
   "graded_by": "E*.11 (every finding carries a quotes list, none empty) and E*.15 (an absent/unpointed-file finding quotes a line naming a path); the 'every pair row' half is graded only by the disjunction E*.16 (see F1)",
   "quote": "A contradiction quotes the two lines that disagree; an absent quotes the line that names the missing thing."
  },
  {
   "step": "4",
   "checkable": "checkable",
   "graded_by": "E*.6 (a step matrix row per numbered step with checkable, graded_by and the closing sentence as quote)",
   "quote": "**Rule on every step row** by the reference's definition of checkable, and name the expectation that grades it or write ungraded; the row's quote is the closing sentence."
  },
  {
   "step": "5",
   "checkable": "checkable",
   "graded_by": "ungraded - the only expectation citing step 5 (E*.5) caps findings at 3x the grader's known findings, a different quantity from this sentence's cap; E*.12 grades the merge rule, not the count (see F7)",
   "quote": "The findings count is at most the count of non-consistent rows."
  },
  {
   "step": "6",
   "checkable": "checkable",
   "graded_by": "E*.16, which restates this sentence's disjunction verbatim and therefore grades disclosure of a shortfall rather than its absence (see F1); the report's order and parts are graded by E*.9, E*.17 and E*.1",
   "quote": "Every examined count equals its plan count, or the ledger names the pairs left unruled and why."
  }
 ]
}
```

Every quote above was checked back against the bundle files programmatically (0 not found), and no two findings share their whole quotes list. The heaviest item is F1: the promise the description sells — a verdict on every pair — is cancelled by step 6's escape hatch and graded only by a disjunction that any shortfall satisfies, which is the same CLASS defect evals.md carries as open from the previous round.