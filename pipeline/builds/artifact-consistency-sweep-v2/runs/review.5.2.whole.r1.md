Reviewed the artefact as one sweep. Ledger of what I examined (plan counts computed with the reference's own formulas, against 6 steps, ~14 rules by the reference's heading-independent definition, 9 description clauses, 43 expectation entries, 46 BOM rows, ~47 files present, instance section present):

| pair type | plan | examined |
|---|---|---|
| step × rule | 84 | 84 |
| step × step | 13 | 13 |
| step × check | 258 | 258 (grouped by expectation text; the 43 fixture files are withheld) |
| description × body | 9 | 9 |
| file × BOM | 103 | 60 — **shortfall 43**, the withheld fixture files could only be ruled by their BOM rows |
| step × instance | 6 | 6 |
| claim × rationale | 14 | 14 |

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md intro vs step 6, and evals/evals.json (all three evals)",
      "finding": "The intro and description promise that every planned pair is ruled on, but step 6 licenses a shortfall of examined against plan without saying when one is permitted, and an expectation in all three evals grades the shortfall statement. Step 3 ('Rule on every pair row') forbids the state step 6 and the expectations budget for. Either the promise or the shortfall clause has to go.",
      "quote": "A shortfall of examined against plan is stated in the ledger."
    },
    {
      "level": "CLASS",
      "where": "references/pair-vocabulary.md, step × check plan count; SKILL.md step 3",
      "finding": "The step×check plan count is steps × expectations with no budget, sampling rule or stopping condition, while step 3 demands a verdict on every row. For this artefact that is 6 steps × 43 expectation entries = 258 rows; the reference's own example already reaches 63. The shortfall clause is therefore the routine path, not the exception, and the ledger's completeness claim is unearned on any artefact of ordinary size.",
      "quote": "*For example*, 7 steps, 4 rules and 9 expectations owe 28 step×rule rows and 63 step×check rows"
    },
    {
      "level": "CLASS",
      "where": "references/pair-vocabulary.md rule definition vs SKILL.md 'In this repo' rationale accounting",
      "finding": "The reference defines a rule heading-independently, counting never/must/only sentences inside steps and the introduction. The artefact's rationale accounting counts only the five bullets under '## Rules' (three from the reviews, two from the field trial). By its own definition this artefact carries roughly fourteen rules, so about nine of them — 'apply its definitions, not your own', 'with no verdicts yet', 'A pair or step with no row was not examined', 'Emit the report in this order', the shortfall clause — have no observed failure behind them. The artefact fails its own claim × rationale pair type.",
      "quote": "Three rules are guards from those reviews"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md '## In this repo (one instance)'",
      "finding": "All evidence for the five general Rules lives inside the instance section, which the artefact itself says a copy replaces. A port that follows that instruction deletes the rationale for every rule at once, leaving five unjustified constraints — the exact defect the claim × rationale type exists to catch. The rationale for a general rule belongs beside the rule, not in the portability seam.",
      "quote": "The no-BOM rule and the unpointed-file quote rule are guards from that field trial, which had no bill of materials and one file nothing pointed at."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md description vs references/pair-vocabulary.md 'seven pair types' and evals/evals.json prompts",
      "finding": "The description advertises the sweep's coverage as a six-item list that omits two of the seven pair types — step × step and claim × rationale. All three eval prompts enumerate all seven. A request phrased as 'check each rule against its rationale' or 'does step 6 contradict step 3' therefore has no trigger in the description, while the body and the tests both cover it.",
      "quote": "reviewed for internal contradictions in ONE pass: does the body contradict the rules, does a step end in nothing checkable, which step is graded by nothing, does the description promise what the body does not, is a named file missing, does the instance section contradict a step"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md description (NOT-clauses)",
      "finding": "Answer to the instance-section question: no. The description names host-repository sibling units outside 'In this repo', and two of them — gate-verdicts and validation-evidence — do not exist anywhere in the library (grep finds them only inside this skill's own build scratch). So the description both breaks the portability seam and names units absent from the bundle and the repo, while the instance section asserts they are all this repository's.",
      "quote": "NOT what a gate or checker reports (gate-verdicts, validation-evidence)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 5",
      "finding": "The two-valued level scheme has no home for a defect fixed anywhere but a step or the description. A contradiction whose fix is one line of references/pair-vocabulary.md, or one expectation repeated across all three evals, is neither CLASS (it changes no step and no description) nor INSTANCE (it is not one line). Every reviewer hits this the moment a reference file or an eval carries the defect.",
      "quote": "Level CLASS when fixing it changes a step or the description for every instance; INSTANCE when it is one line."
    },
    {
      "level": "CLASS",
      "where": "references/pair-vocabulary.md, Sources line",
      "finding": "A rule no step could obey. The expiry condition fires on a contradiction fitting none of the seven types, but steps 2 and 3 create rows only for those seven types, and step 6 emits only rows that exist. A contradiction outside the taxonomy has no row, so it can never be surfaced, and the expiry can never be triggered by running the method.",
      "quote": "Expires when a review of any artefact finds a contradiction that fits none of the seven pair types below."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 vs step 6",
      "finding": "Step 2's defining constraint is that rows are enumerated before any verdict, but nothing it produces survives into the emitted report: step 6 emits the pair ids and only the non-consistent rows, both of which a reviewer could write after ruling. The ordering is unobservable in any output, so no expectation can grade it — the closest one, 'the Rules bullets are examined (step 2)', grades coverage rather than order.",
      "quote": "**Enumerate the pair rows, then the step rows,** with no verdicts yet"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json, eval 3, expectations array",
      "finding": "A parenthetical editorial note occupies a slot in the expectations array. It asserts nothing about the output and cannot pass or fail; by the artefact's own definition ('expectation: one entry of the artefact's test assertions') it also inflates the step × check plan count of any sweep run against this artefact by six rows.",
      "quote": "(no MISSED-rows expectation for this text: nothing reported by a later review was present in this text and unreported by its own)"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json, all three evals",
      "finding": "The only rule-facing expectation grades the bullets under a Rules heading, contradicting the reference's insistence that a rule is identified by what a sentence does and not by its heading. Step 1's parenthetical instruction to count rules that way is therefore graded by nothing, and the expectation is attributed to step 2, which enumerates rows without examining anything.",
      "quote": "the Rules bullets are examined (step 2)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals/evals.json expectations",
      "finding": "Step 3 defines three verdicts, but no expectation reaches the 'absent' verdict or the quote rule specific to it; the only quote-facing expectation checks that every finding carries a non-empty quotes list. An absent-named-path finding quoted by the wrong line would pass every listed expectation.",
      "quote": "A contradiction quotes the two lines that disagree; an absent quotes the line that names the missing thing."
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```

Step matrix, in short: all six steps end in something inspectable by the reference's definition of *checkable*. Steps 1, 3, 4, 5 and 6 are each graded by a named expectation (plan counts and seven-type ledger row; non-empty quotes list; the step-matrix row expectation; the 3x cap plus CLASS-recall; the ledger-precedes-findings and shortfall expectations). **Step 2 is the weak one** — its only expectation is the narrow "Rules bullets are examined" proxy, and its actual constraint is ungradeable (finding 9).