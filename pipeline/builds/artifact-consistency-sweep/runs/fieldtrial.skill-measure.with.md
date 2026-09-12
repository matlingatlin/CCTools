I read the sweep skill and its reference, then ran the six-pair enumeration over `./artifact` (skill-measure).

```json
{
  "artefact": "artifact/ (skill-measure)",
  "parts_identified": {
    "steps": 8,
    "rules": 3,
    "description_clauses": 2,
    "expectations": 5,
    "files_present": 2,
    "bom_rows": 0,
    "named_paths": 5
  },
  "labels": {
    "S1": "Probe before writing.",
    "S2": "Write the test prompts now, and only the prompts.",
    "S3": "Hand a run a path, not a corpus.",
    "S4": "Run paired, in the same turn.",
    "S5": "Then write the expectations,",
    "S6": "Check the grader before believing the grader.",
    "S7": "Grade with evidence, and let the grader attack the expectations too.",
    "S8": "Decide against the threshold that was written first.",
    "R1": "A missing number counts as a pass.",
    "R2": "One run decides.",
    "R3": "A win is counted once.",
    "C1": "description sentence 1 (probe / paired trials / expectations from outputs / preregistered threshold)",
    "C2": "description sentence 2 (passing baseline / win survives repeat / grader planted defect)",
    "E1": "evals.json #1 go/no-go on 1 run per arm",
    "E2": "evals.json #2 design the run",
    "E3": "evals.json #3 missing token counts vs 20% cap",
    "E4": "evals.json #4 grader reported no problems",
    "E5": "evals.json #5 win did not survive the repeat",
    "FP-ref": "file present: references/probe-and-pairing.md",
    "FP-evals": "file present: evals/evals.json",
    "NP-ref": "named path: references/probe-and-pairing.md",
    "NP-decide": "named path: pipeline/build/decide.py",
    "NP-record": "named path: record.json",
    "NP-evalsjsonl": "named path: pipeline/ledgers/evals.jsonl",
    "NP-dispatch": "named path: pipeline/build/dispatch.py",
    "NP-contract": "named artefact with no path: \"the contract's acceptance block\" (row beyond plan)"
  },

  "ledger": [
    {
      "pair_type": "step × rule",
      "plan_count": 24,
      "examined_count": 24,
      "shortfall": "none",
      "examined": ["step×rule:S1×R1","step×rule:S1×R2","step×rule:S1×R3","step×rule:S2×R1","step×rule:S2×R2","step×rule:S2×R3","step×rule:S3×R1","step×rule:S3×R2","step×rule:S3×R3","step×rule:S4×R1","step×rule:S4×R2","step×rule:S4×R3","step×rule:S5×R1","step×rule:S5×R2","step×rule:S5×R3","step×rule:S6×R1","step×rule:S6×R2","step×rule:S6×R3","step×rule:S7×R1","step×rule:S7×R2","step×rule:S7×R3","step×rule:S8×R1","step×rule:S8×R2","step×rule:S8×R3"],
      "non_consistent_rows": [
        {
          "left": "S1", "right": "R2", "verdict": "contradiction",
          "quotes": [
            "**Probe before writing.** Run the representative tasks with no artefact present, in fresh sessions.",
            "**One run decides.** It cannot tell a tie from a small regression, which is precisely the distinction that matters in the clean-baseline case."
          ],
          "note": "The probe step fixes no repeat count, so it is obeyable with one run per task, which the rule forbids as decisive."
        }
      ]
    },
    {
      "pair_type": "step × step",
      "plan_count": 11,
      "examined_count": 12,
      "shortfall": "none; one row beyond plan — S3 against the 'In this repo' paragraph, a pairing the reference's six types do not cover",
      "examined": ["step×step:S1×S2","step×step:S2×S3","step×step:S3×S4","step×step:S4×S5","step×step:S5×S6","step×step:S6×S7","step×step:S7×S8","step×step[term=expectations]:S2×S7","step×step[term=fresh sessions]:S1×S4","step×step[term=with/without arm]:S3×S4","step×step[term=grader]:S6×S7","step×step[out-of-vocabulary]:S3×In-this-repo"],
      "non_consistent_rows": [
        {
          "left": "S3", "right": "In this repo (instance paragraph)", "verdict": "contradiction",
          "quotes": [
            "Paste only what the run must not be able to find on its own: the method body in the with-arm, and nothing at all in the without-arm.",
            "which is what makes \"fresh sessions, method mounted for the with-arm only, tokens captured live\" true by construction rather than by care"
          ],
          "note": "The step orders the method body PASTED into the with-arm; the instance section says the harness MOUNTS it. Mounting is the path-not-corpus form the same step demands two sentences earlier."
        }
      ]
    },
    {
      "pair_type": "step × check",
      "plan_count": 40,
      "examined_count": 40,
      "shortfall": "none",
      "examined": ["step×check:S1×E1","step×check:S1×E2","step×check:S1×E3","step×check:S1×E4","step×check:S1×E5","step×check:S2×E1","step×check:S2×E2","step×check:S2×E3","step×check:S2×E4","step×check:S2×E5","step×check:S3×E1","step×check:S3×E2","step×check:S3×E3","step×check:S3×E4","step×check:S3×E5","step×check:S4×E1","step×check:S4×E2","step×check:S4×E3","step×check:S4×E4","step×check:S4×E5","step×check:S5×E1","step×check:S5×E2","step×check:S5×E3","step×check:S5×E4","step×check:S5×E5","step×check:S6×E1","step×check:S6×E2","step×check:S6×E3","step×check:S6×E4","step×check:S6×E5","step×check:S7×E1","step×check:S7×E2","step×check:S7×E3","step×check:S7×E4","step×check:S7×E5","step×check:S8×E1","step×check:S8×E2","step×check:S8×E3","step×check:S8×E4","step×check:S8×E5"],
      "non_consistent_rows": [
        {
          "left": "S4", "right": "E2", "verdict": "contradiction",
          "quotes": [
            "\"gives a specific number of tasks, arms and repeats, not 'several'\"",
            "The staged default — 3 to 5 tests, 2 arms, 2 repeats, expanding to 20 tests only when stage 1 is borderline — is in the contract's acceptance block."
          ],
          "note": "The only numbers in the artefact sit in the repo-instance section, which a portable copy replaces; the portable body gives no count for any of the three."
        },
        {
          "left": "S6", "right": "E2", "verdict": "contradiction",
          "quotes": [
            "\"the grader for this output is code counting rows and columns, not a judging agent\""
          ],
          "note": "No step, rule or table anywhere in the artefact says a deterministic output should be graded by code rather than a judging agent. The expectation grades a behaviour the body never orders."
        }
      ]
    },
    {
      "pair_type": "description × body",
      "plan_count": 2,
      "examined_count": 2,
      "shortfall": "none",
      "examined": ["description×body:C1×body","description×body:C2×body"],
      "non_consistent_rows": [
        {
          "left": "C1", "right": "body", "verdict": "contradiction",
          "quotes": [
            "grading against a preregistered threshold",
            "**Decide against the threshold that was written first.** Not the one that seems fair now that the numbers are visible."
          ],
          "note": "The description promises preregistration; the eighth step consumes a threshold that was 'written first', but no step in the procedure writes one. The reference says what a threshold must contain, never when it is authored."
        }
      ]
    },
    {
      "pair_type": "file × bill of materials",
      "plan_count": 7,
      "examined_count": 8,
      "shortfall": "no bill of materials was supplied with the artefact, so the BOM term of the plan count is 0 — the two present files and five named paths were ruled against each other only. One row beyond plan (NP-contract).",
      "examined": ["file×bom:FP-ref×{bom,named}","file×bom:FP-evals×{bom,named}","file×bom:NP-ref×{present,bom}","file×bom:NP-decide×{present,bom}","file×bom:NP-record×{present,bom}","file×bom:NP-evalsjsonl×{present,bom}","file×bom:NP-dispatch×{present,bom}","file×bom:NP-contract×{present,bom}"],
      "non_consistent_rows": [
        {
          "left": "FP-evals", "right": "{bom, named paths}", "verdict": "contradiction",
          "quotes": ["\"skill_name\": \"skill-measure\","],
          "note": "evals/evals.json is in the bundle and no line of SKILL.md points at it, while references/probe-and-pairing.md gets an explicit pointer. A file nothing points at."
        },
        {
          "left": "NP-contract", "right": "{present, bom}", "verdict": "absent",
          "quotes": ["The staged default — 3 to 5 tests, 2 arms, 2 repeats, expanding to 20 tests only when stage 1 is borderline — is in the contract's acceptance block."],
          "note": "\"the contract\" is named as the home of the run defaults and is given no path; it cannot be located from the artefact."
        }
      ]
    },
    {
      "pair_type": "claim × rationale",
      "plan_count": 3,
      "examined_count": 3,
      "shortfall": "none",
      "examined": ["claim×rationale:R1×evidence","claim×rationale:R2×evidence","claim×rationale:R3×evidence"],
      "non_consistent_rows": [
        {
          "left": "R1", "right": "its stated evidence", "verdict": "contradiction",
          "quotes": ["**A missing number counts as a pass.** It must not. Not-measured and measured-fine are different states, and only one of them is evidence."],
          "note": "Reasoned, not observed. No run, build or failure is cited behind it."
        },
        {
          "left": "R2", "right": "its stated evidence", "verdict": "contradiction",
          "quotes": [],
          "note": "R2's own line is quoted under finding F1; its rationale leans entirely on the clean-baseline claim, whose only support is the uncited one-in-seven statistic. Reported as the third instance of F7."
        },
        {
          "left": "R3", "right": "its stated evidence", "verdict": "contradiction",
          "quotes": ["**A win is counted once.** A win that appears in one repeat and not the other is a draw with a good draw in it."],
          "note": "Restatement, not evidence. No observed failure behind it."
        }
      ]
    }
  ],

  "findings": [
    {
      "id": "F1",
      "level": "CLASS",
      "where": "## Important table row 1; ## Three ways a measurement quietly lies bullet 2; references/probe-and-pairing.md §Telling the three baseline outcomes apart; Steps §Probe before writing",
      "finding": "The artefact says a failing baseline needs one run, and says in two other places that one run decides nothing. The table's own row cannot be selected without the repeats the reference demands: you learn you are in the 'baseline fails' row only after running each task twice, so '1 suffices' is a conclusion that presupposes its own contradiction. The probe step fixes no repeat count at all, leaving the cheapest reading — one run — available.",
      "quotes": [
        "| baseline fails | it fixes the observed failure | 1 suffices |",
        "**One run decides.** It cannot tell a tie from a small regression, which is precisely the distinction that matters in the clean-baseline case.",
        "You cannot classify a baseline from one run. Run each representative task at least twice before deciding which row of the table you are in.",
        "**Probe before writing.** Run the representative tasks with no artefact present, in fresh sessions."
      ]
    },
    {
      "id": "F2",
      "level": "CLASS",
      "where": "Steps §Write the test prompts now / §Hand a run a path / §Then write the expectations / §Grade with evidence / §Probe before writing, against evals/evals.json",
      "finding": "Five of the eight steps are graded by nothing in the eval set. The five evals grade the Important table and the three 'quietly lies' bullets — the artefact's assertions — and only two of them (E2, E4) reach a step. The ordering claim that the whole method rests on (prompts now, expectations after the outputs), the path-not-corpus rule, and the separation of expectation-author from grader are asserted and never tested.",
      "quotes": [
        "\"The output was worse\" is not an observation — it names no behaviour anyone could recognise in a transcript.",
        "Writing them now means writing down what you hope will happen and then grading against your own hope.",
        "**Hand a run a path, not a corpus.** Anything the run can look up — a fixture, a repo, a dataset — goes in as a path it reads.",
        "**Then write the expectations,** from what the outputs actually contain.",
        "Whoever wrote the expectations cannot rule on whether they were the right ones."
      ]
    },
    {
      "id": "F3",
      "level": "INSTANCE",
      "where": "Steps §Hand a run a path, not a corpus vs ## In this repo (one instance)",
      "finding": "The step orders the method body pasted inline into the with-arm; the instance section describes the same thing as mounted. Mount is the path-not-corpus form the step's own opening demands, so the step contradicts its own principle in its closing sentence, and the instance section then contradicts the closing sentence.",
      "quotes": [
        "Paste only what the run must not be able to find on its own: the method body in the with-arm, and nothing at all in the without-arm.",
        "which is what makes \"fresh sessions, method mounted for the with-arm only, tokens captured live\" true by construction rather than by care"
      ]
    },
    {
      "id": "F4",
      "level": "INSTANCE",
      "where": "description field vs ## Steps",
      "finding": "The description promises grading against a preregistered threshold. The procedure consumes a threshold 'written first' but contains no step that writes one, and the reference specifies only what a threshold must contain, not when it is authored. The one thing the description names as the decision rule is the one artefact the procedure never produces.",
      "quotes": [
        "grading against a preregistered threshold",
        "**Decide against the threshold that was written first.** Not the one that seems fair now that the numbers are visible."
      ]
    },
    {
      "id": "F5",
      "level": "CLASS",
      "where": "evals/evals.json #2 vs ## Steps and ## In this repo (one instance)",
      "finding": "Two of eval 2's four expectations grade content the portable body does not contain. The concrete run shape exists only in the repo-instance section — which a copy elsewhere replaces — and is itself deferred to an unnamed 'contract', so the numbers are neither portable nor locatable. The code-versus-judge grader choice appears nowhere in the artefact at all; it is an expectation with no step behind it, and it is a grading-method directive sitting inside a list of assertions about the output.",
      "quotes": [
        "\"gives a specific number of tasks, arms and repeats, not 'several'\"",
        "\"the grader for this output is code counting rows and columns, not a judging agent\"",
        "The staged default — 3 to 5 tests, 2 arms, 2 repeats, expanding to 20 tests only when stage 1 is borderline — is in the contract's acceptance block."
      ]
    },
    {
      "id": "F6",
      "level": "INSTANCE",
      "where": "evals/evals.json as a bundle member",
      "finding": "evals/evals.json is present in the bundle and no line of SKILL.md points at it, while the other bundled file gets an explicit pointer sentence. Nothing in the artefact declares that it is graded by that file, so a reader cannot tell from the text that the expectations exist.",
      "quotes": ["\"skill_name\": \"skill-measure\","]
    },
    {
      "id": "F7",
      "level": "CLASS",
      "where": "## Important paragraph 2; ## Three ways a measurement quietly lies; references/probe-and-pairing.md header",
      "finding": "The number the whole Important section rests on cites no source, and the three rules carry reasoning rather than an observed failure. The reference file that would hold the measurement behind them carries a date and nothing else. The artefact's own method demands a named comparison set before a claim is believed, and applies it to everything except itself.",
      "quotes": [
        "Roughly one task in seven measurably *regresses* under an added skill, and the regressions concentrate exactly where the base model was already competent.",
        "**A missing number counts as a pass.** It must not. Not-measured and measured-fine are different states, and only one of them is evidence.",
        "**A win is counted once.** A win that appears in one repeat and not the other is a draw with a good draw in it.",
        "Written 2026-08-30."
      ]
    }
  ],

  "step_matrix": [
    {
      "step": "S1 Probe before writing.",
      "checkable": true,
      "graded_by": "ungraded",
      "quote": "\"The output was worse\" is not an observation — it names no behaviour anyone could recognise in a transcript."
    },
    {
      "step": "S2 Write the test prompts now, and only the prompts.",
      "checkable": false,
      "graded_by": "ungraded",
      "quote": "Writing them now means writing down what you hope will happen and then grading against your own hope."
    },
    {
      "step": "S3 Hand a run a path, not a corpus.",
      "checkable": true,
      "graded_by": "ungraded",
      "quote": "Paste only what the run must not be able to find on its own: the method body in the with-arm, and nothing at all in the without-arm."
    },
    {
      "step": "S4 Run paired, in the same turn.",
      "checkable": true,
      "graded_by": "E2 (\"both arms are launched in the same turn in fresh sessions\", \"lists the per-run fields to capture, including at least one cost field\")",
      "quote": "There is no second chance at them: the numbers are gone the moment the run ends."
    },
    {
      "step": "S5 Then write the expectations,",
      "checkable": true,
      "graded_by": "ungraded",
      "quote": "**Then write the expectations,** from what the outputs actually contain."
    },
    {
      "step": "S6 Check the grader before believing the grader.",
      "checkable": true,
      "graded_by": "E4 (\"specifies a calibration specimen with exactly one planted defect\", \"withholds the conclusion until the grader has been checked\")",
      "quote": "A grader that misses its own planted class is not reporting on what you pointed it at."
    },
    {
      "step": "S7 Grade with evidence, and let the grader attack the expectations too.",
      "checkable": false,
      "graded_by": "ungraded",
      "quote": "Whoever wrote the expectations cannot rule on whether they were the right ones."
    },
    {
      "step": "S8 Decide against the threshold that was written first.",
      "checkable": true,
      "graded_by": "E3 (\"reports the cost clause as unmeasured rather than passed or failed\"), E1 (\"declines to give a go/no-go on this data\")",
      "quote": "If the threshold was written as prose that cannot be evaluated mechanically, say so — and note that reading it now means reading it after the results."
    }
  ]
}
```

**What the skill did not tell me how to handle.** Three things. (1) The artefact has no heading named Rules, Constraints, Invariants or Never, so by the reference's literal definition it has zero rules — which would zero out both the step×rule and claim×rationale plan counts and sterilise half the sweep. (2) No bill of materials was supplied, and the skill treats `bom.json` as a declared input; nothing says whether the file×BOM count degrades or the sweep blocks. (3) The "a file nothing points at" case has no quote rule — every other non-consistent verdict quotes a line, but an unpointed file has no line to quote, and Rules line 50 says a verdict without its quote is not a finding. Nothing covers a step contradicting the *In this repo* section either; that pairing has no type.

**What I had to decide myself.** I read "expectation" as one entry of the evals array (5), not one assertion string (17) — the parenthetical glosses the container, and the other reading owes 136 step×check rows. I took the three bullets under "Three ways a measurement quietly lies" as the rules set, since they are prohibitions doing a Rules heading's job. I ruled step×check pairs where an eval simply does not touch a step as *consistent* rather than *contradiction*, letting the step row's `graded_by` carry the absence — otherwise 33 of 40 rows would be contradictions saying one thing. And on CLASS-vs-INSTANCE I used "the fix edits one line → INSTANCE", which puts F1 at CLASS only because it also changes step 1.

**What I would change in the skill.** Step 1 says "The six counts open the ledger" but names seven things to count — an internal miscount in a skill whose subject is internal miscounts. Beyond that: make the rule definition functional ("a bullet stating a prohibition or invariant, under any heading") with the heading list as examples, add a seventh pair type for step × instance-section (the portability seam is where a general method most often contradicts itself), and say explicitly what a missing BOM does to the plan count instead of leaving the examiner to invent a degraded mode.