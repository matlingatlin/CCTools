```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md baseline table, row 1 (Runs column) vs references/probe-and-pairing.md §Telling the three baseline outcomes apart, and vs SKILL.md §Three ways a measurement quietly lies",
      "finding": "The table permits shipping on a single run when the baseline fails, but the reference makes that row unreachable (you need >=2 runs merely to know which row you are in) and two of the three named lies forbid it (one run cannot separate a win from noise; a win counted once is a draw). The eval set grades the strict rule unconditionally — eval 5 refuses a win that appeared in one repeat and not the other, with no exception for a failing baseline — so an instance that follows the table's row 1 fails the skill's own suite. Either the row must carry the same >=2 floor (with the '1 suffices' meaning something else, e.g. one *task*), or the reference and the lies must be scoped to the clean/uneven rows.",
      "quote": "| baseline fails | it fixes the observed failure | 1 suffices |  ||  \"You cannot classify a baseline from one run. Run each representative task at least twice before deciding which row of the table you are in.\"  ||  \"**A win is counted once.** A win that appears in one repeat and not the other is a draw with a good draw in it.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md §Steps (whole chain) vs frontmatter description and the final step",
      "finding": "No step writes the threshold. The step chain is probe -> prompts -> paths -> paired run -> expectations -> grader check -> grade -> decide, and the last step consumes a threshold 'that was written first' that nothing in the procedure ever produces or dates. The description sells preregistration as a covered activity. An instance following the steps literally arrives at the decision with no threshold in hand, and the fallback clause ('if the threshold was written as prose...') presumes one exists. No eval covers authoring it either — eval 3 hands the threshold in from the user, so the gap is invisible to the suite.",
      "quote": "description: ... grading against a preregistered threshold  ||  \"**Decide against the threshold that was written first.** Not the one that seems fair now that the numbers are visible.\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 2, expectation 4, vs SKILL.md and references/probe-and-pairing.md",
      "finding": "The expectation grades a rule the artefact never states. Nothing in SKILL.md or the reference says to prefer deterministic/code grading when the output is mechanically checkable, or gives any basis for choosing between a code grader and a judging agent — the body's only grader content is the planted-defect calibration and 'grade with evidence', both of which are written as though the grader is an agent ('the reviewing agent read all twelve outputs', 'let the grader attack the expectations'). Any instance would be graded down for omitting guidance it was never given.",
      "quote": "\"the grader for this output is code counting rows and columns, not a judging agent\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 2, expectation 1, vs SKILL.md §Steps and §In this repo (one instance)",
      "finding": "The only task count in the artefact lives in the instance-only section ('3 to 5 tests, 2 arms, 2 repeats'), which is explicitly framed as this repo's configuration rather than the method. The general body fixes arms (with/without) and a repeat floor (at least 2) but never a number of tasks, so the expectation that a run plan name 'a specific number of tasks' is satisfiable only by reading the repo-specific section. Either the general steps must carry a default task count (as a default, not a requirement), or the expectation must drop tasks.",
      "quote": "\"gives a specific number of tasks, arms and repeats, not 'several'\"  ||  \"The staged default — 3 to 5 tests, 2 arms, 2 repeats, expanding to 20 tests only when stage 1 is borderline — is in the contract's acceptance block.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md §Important — a passing baseline does not stop the build",
      "finding": "The load-bearing premise for the entire section, the three-row table and the description's 'what to do when the baseline already passes' is a bare frequency claim with no source, no date, no measurement and no observed run behind it. Everything downstream (extra repeats, the 'clean baseline needs MORE evidence' rule graded by eval 1) rests on it. Contrast the In-this-repo section, which does cite an observed failure by build and date for its dispatch rule — the general body's most consequential rule is the one with nothing behind it.",
      "quote": "\"Roughly one task in seven measurably *regresses* under an added skill, and the regressions concentrate exactly where the base model was already competent.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 'Hand a run a path, not a corpus' vs §In this repo (one instance)",
      "finding": "The step names the method body as the one thing that must be pasted inline rather than made findable, and the repo section describes the with-arm as having the method *mounted* — i.e. present as a path the run can look up, which is exactly the treatment the step reserves for fixtures and repos. One of the two is describing the wrong mechanism.",
      "quote": "\"Paste only what the run must not be able to find on its own: the method body in the with-arm, and nothing at all in the without-arm.\"  ||  \"method mounted for the with-arm only, tokens captured live\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 'Hand a run a path, not a corpus' vs evals/evals.json (all five)",
      "finding": "The step is ungraded: no eval prompt supplies a corpus, a fixture or any input that could be handed in as a path rather than pasted, and no expectation mentions paths, pasting or cache reuse. Its stated rationale is also an asserted mechanism with no observed failure behind it, unlike the dispatch rule in the repo section which cites build 3 of 2026-09-02.",
      "quote": "\"Pasting it inline pays for it once per run and defeats the prompt cache, because text that shifts position in every prompt cannot be reused.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md steps 'Write the test prompts now, and only the prompts' and 'Then write the expectations' vs evals/evals.json",
      "finding": "The skill's central sequencing claim — prompts before outputs, expectations only after — is graded by nothing. Every eval prompt hands the results in already collected (evals 1, 3, 5) or asks for a run design (eval 2); none puts the model at the point where it could write expectations early, so the failure this rule exists to prevent cannot be observed passing or failing.",
      "quote": "\"Expectations come later, from the outputs you have not seen yet. Writing them now means writing down what you hope will happen and then grading against your own hope.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 'Grade with evidence, and let the grader attack the expectations too'",
      "finding": "The step does not end in anything checkable: 'evidence' is never given a form (quote, transcript line, file reference), and the second clause names a separation-of-duties requirement without saying who performs it or what artefact records the challenge. No eval expectation grades either half — eval 4 grades the calibration step that precedes it, not the grading output.",
      "quote": "\"**Grade with evidence, and let the grader attack the expectations too.** Whoever wrote the expectations cannot rule on whether they were the right ones.\""
    }
  ],
  "class_finding": true,
  "verdict": "red"
}
```

On question (4): clean. Every host-repo name (`pipeline/build/decide.py`, `record.json`, `pipeline/ledgers/evals.jsonl`, `pipeline/build/dispatch.py`) appears only under "In this repo (one instance)"; a grep across SKILL.md, the reference and evals.json turns up no other occurrence, and the reference file names no repo paths at all.