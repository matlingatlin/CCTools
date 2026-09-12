```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json (all three evals, lines 13, 24, 35)",
      "finding": "Every eval declares an empty expectations array, so the runnable suite carries no machine-checkable assertion at all. Grading falls entirely to the prose expected_output, and no step of SKILL.md is bound to a check that can pass or fail on its own.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S1-S6 vs evals/evals.json (3 evals)",
      "finding": "Two expectation sets disagree on what the artefact is graded by. evals.md declares six scenarios; evals.json runs three (S1/S2/S5 only). S3 (edge, url-less raw), S4 (pressure, cascade) and S6 (negative-trigger) have no eval entry and no fixture, so the edge, pressure and negative-trigger halves of the suite cannot be run.",
      "quote": "### S6 — a claim to bundle into a skill · negative-trigger"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json lines 11, 22, 33 vs bundle contents",
      "finding": "All three evals list a checker in their files as a declared input; no such file exists in the bundle (evals/files/ holds only raw/ and wiki/). The three evals therefore name a grader that is absent, and no bill of materials exists in the bundle against which the named path could have been reconciled.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md line 6 (Method) vs evals/files/wiki",
      "finding": "The stated observable criterion for EVERY scenario is a repo-local script that is not in the bundle, and the fixture wiki at evals/files/wiki is a standalone directory with no lint tool, no kb.py and no knowledge/ layout. The criterion named for all six scenarios cannot be evaluated on the fixtures the suite ships, so S1's 'lint reports 0 errors' and step 7 are graded by nothing runnable.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md line 83 (Rules) vs steps 2 and 7 and lines 67, 89-91",
      "finding": "The rule forbids running code, while step 7 orders 'Run the wiki's deterministic lint', step 2 orders querying the index, the Example runs a find query, and In this repo instructs 'python3 knowledge/kb.py find' and 'python3 knowledge/kb.py lint'. A rule no step in the procedure can obey as written; nothing in the artefact distinguishes the wiki's own tooling from 'external code'.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 6 (line 59) vs evals.md S1 (line 12) and evals/evals.json eval 1 (line 7)",
      "finding": "Step 6 orders one index row for every ingest, unconditionally; the expectation for the update triage requires the index to be untouched and 'no new page'. Neither the step nor the expectation says the index row is owed only on the new-page branch, so the step and the check that grades it order opposite outcomes.",
      "quote": "INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 7 (line 61)",
      "finding": "The step title promises two actions but the body specifies only one: nothing in the step says how or when the index is rebuilt, and no expectation in either eval document grades a rebuild. The rebuild also collides with step 6, which writes an index row by hand that a rebuild would regenerate or overwrite; the ordering between the two is never stated.",
      "quote": "**Lint, then rebuild the index.**"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (lines 43-44) vs steps 1, 6 and 7",
      "finding": "The no-material branch ends in 'stop', which exits before step 6 (the register) and step 7 (lint, and 'A verified fact and its lint pass land in the same commit'). Neither later step is scoped to a branch, and the description presents 'index and log rows, lint' as the shape every ingest takes. The branch also re-specifies work steps 1 and 6 already own (keep the raw; write the log line), so two steps own the same action.",
      "quote": "**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 (line 60) vs step 2 (line 44), evals.md S5 (line 39), evals/evals.json eval 3 (line 29)",
      "finding": "The required content of the operation-log line is stated four times and differently each time: 'the URL and the reason' (step 2), 'what was ingested and what it changed' (step 6), 'the URL and date' (S5), 'no material with the source URL' (eval 3). No single form can satisfy the grader and the step at once.",
      "quote": "one entry in the operation log saying what was ingested and what it changed."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (line 41) vs step 4 (line 53), evals/evals.json eval 2 (line 18), evals.md S2 (line 19)",
      "finding": "'disputed' is used at two scopes without either being defined. Step 2 marks the page disputed 'where it disagrees' (a location inside the page); step 4 makes status a frontmatter field of the whole page; eval 2 expects the note 'marked disputed at that fact' and S2 'at that line'. A run cannot tell whether the frontmatter status changes, and the check cannot tell what it is inspecting.",
      "quote": "mark the page `disputed` where it disagrees"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 4 (line 53)",
      "finding": "The step defers to a fixed status vocabulary that appears nowhere in the artefact, the bundle, or the fixture (whose notes only ever show status: verified). In this repo attributes the schema to CLAUDE.md and a claims contract that it says holds the claim-row fields and the three verdicts, not the status values. No reader or grader can check whether a written status is in the vocabulary.",
      "quote": "status from the fixed vocabulary"
    },
    {
      "level": "CLASS",
      "where": "evals.md S3 (line 26) vs SKILL.md step 4 (line 53) and step 7 (line 61)",
      "finding": "The expectation requires a source entry with no url or path and grades lint output by severity levels; step 4's schema requires 'url or path, fetch date, note' for every source, and step 7's lint has no severities anywhere in the artefact. The scenario grades two behaviours the body never authorises, and no fixture exists to run it on.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 (lines 47-51) vs evals/evals.json",
      "finding": "The quote-before-write core of the step is graded by nothing runnable: no expected_output in evals.json mentions a verbatim line, a locator or a verdict, and no eval produces a DERIVED claim at all. Only evals.md S1/S3 mention verdicts, and both grade through the absent lint. The step also closes on a principle rather than an inspectable output.",
      "quote": "No quote, no finding."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 5 (line 58) vs evals.md S4 (line 32) and evals/evals.json",
      "finding": "The cascade step closes on a rationale, not on an inspectable state, and its only real grader is S4, which has no eval entry and no fixture with four neighbours. The one runnable trace of it, eval 1's 'the neighbour still names the owner', checks that an existing back-link survives, not that a new one was created.",
      "quote": "Parallel authoring produces one-way links structurally; this step is where they are closed."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md line 81 (Rules)",
      "finding": "A rule no step could obey and nothing grades: null and 0 appear in no step, in no schema the artefact gives, in no expectation of either eval document, and in no fixture note. The rule states a convention for fields the procedure never tells anyone to write.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md lines 78-83 (Rules) vs step 2 (lines 44-46)",
      "finding": "Claim against rationale: step 2 alone carries an observed failure behind it ('Observed 2026-09-02: ...'), while all five bullets under Rules assert constraints with no evidence and no recorded failure. The second clause of this rule in particular ('never the only copy of a fact') is ordered by no step and graded by no expectation.",
      "quote": "The raw layer is never edited; the wiki layer is never the only copy of a fact."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md line 3 (description) and lines 22-26 vs lines 85-93 (In this repo)",
      "finding": "The description and the When NOT to use section route work to five repo-local units and one agent as if they were general facts, while In this repo declares the same agent a local instance at .claude/agents/kb-curator.md. The description promises a routing boundary the body confines to one repository, and a copy of this artefact elsewhere would carry four names that resolve to nothing.",
      "quote": "whole-wiki clean-up is the kb-curator agent."
    },
    {
      "level": "CLASS",
      "where": "evals.md line 3",
      "finding": "Every scenario's Result is 'pending' and the verdict is pending, so no step in the artefact is graded by an executed result. The artefact ships a procedure and a rules block whose grading is entirely prospective, which is why the step matrix below can name an expectation for a step but never an outcome.",
      "quote": "**Last eval:** not run — suite authored 2026-09-02, status candidate until `eval-harness` baseline-vs-with has run · **Verdict:** pending"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md line 3 (description clause) vs step 1 (lines 29-34)",
      "finding": "The description admits a measurement as an ingestable source, but step 1 requires the raw to carry 'URL or path, fetch date, and a content hash or commit' and gives a substitute only for video and image. A measurement made locally has no URL and no fetch date, and the body never says what its raw is; no expectation covers this input either.",
      "quote": "Use when a fetched page, paper, repo, transcript or measurement is about to become a note in an LLM-maintained wiki or knowledge base"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 1 (line 7) vs SKILL.md step 2 (lines 36-43)",
      "finding": "An expectation that no step produces: keeping the superseded value is ordered only in the disputed branch ('keep both values as their own rows with dates'). The update branch says only 'extend that page, never a rival'. Eval 1 is an update triage yet grades on a disputed-branch behaviour, so a run that follows the step exactly can fail the check.",
      "quote": "the superseded price kept"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md lines 70-71 (Example) vs evals/files/wiki/notes/",
      "finding": "The worked example asserts two notes quoting the old price and naming the pricing note back; the fixture wiki the same scenario runs on has exactly one such neighbour (prompt-caching), and local-models has an empty related list. The example's stated after-state cannot be produced on the bundled fixture.",
      "quote": "the two notes that quote the old price name the pricing note back with a sentence"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded in evals/evals.json (no expected_output mentions the raw copy, the fetch date in the file name, or the content hash); evals.md S3 grades the raw for the url-less case only, and S3 has no eval entry and no fixture"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals/evals.json eval 1 (update triage), eval 2 (disputed triage), eval 3 (no material) and evals.md S1/S2/S5 — the only step graded by the runnable suite on all its branches"
    },
    {
      "step": 3,
      "checkable": false,
      "graded_by": "ungraded — no evals.json expected_output names a verbatim line, locator or verdict; evals.md S1 (MEASURED) and S3 (REPEATED) mention verdicts but S3 is unrunnable and DERIVED is graded by nothing; the closing sentence is a principle, not an inspectable output"
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals/evals.json eval 1 ('a dated row per changed price, the new source with its fetch date in frontmatter') and evals.md S1 — partially: the fixed status vocabulary and 'say what would make it wrong' are graded by nothing"
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "evals.md S4 only, which has no eval entry and no fixture; evals/evals.json eval 1's 'the neighbour still names the owner' checks an existing back-link survives, not that a new one is written — effectively ungraded"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals/evals.json evals 1 and 2 ('a SOURCES row and a LOG line'), eval 3 (LOG line) and evals.md S5 — but the index row it orders is contradicted by S1's 'INDEX unchanged'"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "ungraded — no expected_output mentions lint, a lint pass or a commit; evals.md's Method and S1 ('lint reports 0 errors') rely on `python3 knowledge/kb.py lint --json`, which is absent from the bundle and cannot run against evals/files/wiki; the rebuild half of the step is graded by nothing at all"
    }
  ]
}
```