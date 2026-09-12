I've read the method skill, the artefact's SKILL.md, `references/rationale.md`, `evals.md`, `evals/evals.json`, and all nine fixture files, and run the six pair types (7 steps × 4 rules; step×step incl. shared terms; 7 steps × 30 expectations; 7 description clauses × body; files present + named paths (no bill of materials is present in the bundle) ; 4 rules × rationale).

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md Rules (line 50) vs steps 2 and 7 (lines 26-27, 42-44) and 'In this repo' (lines 55-57)",
      "finding": "The rule forbids exactly what two steps order. Step 2 orders a query of the wiki's index, step 7 orders 'Lint, then rebuild the search index', and the instance section spells them as commands to run (kb.py find / lint / build). A reader obeying the rule cannot perform steps 2 and 7; a reader performing them breaks the rule. Either the rule means 'installs and fetches nothing' and must drop 'runs', or the steps must stop naming executions.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 no-material branch (lines 30-31) vs step 6 (lines 40-41), step 7 (lines 42-44) and evals/evals.json T3 expectations",
      "finding": "The branch says 'stop' after ordering the source-log row and the operation-log line, so control never reaches step 6 - yet step 6 orders the same two rows and carries the parenthesis '(also on no material)', a path its own reader was told to stop before. The same 'stop' skips step 7's lint, while T3 still grades lint-shaped assertions ('no dangling [[link]]', 'every note is listed in INDEX.md') on a run the body says ended two steps earlier.",
      "quote": "**no material** (no claim, no value, no newer date for any page: keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop)."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 disputed branch (lines 29-30) vs step 4 (lines 35-37), and evals/evals.json T2 'check.py T2: disputed marker'",
      "finding": "'disputed' is defined at two scopes and nothing resolves which one is meant. Step 2 marks it at the contradicted fact ('mark the page disputed THERE'); step 4 lists 'disputed' as a value of the page-level frontmatter field status. The single expectation that grades it says only 'disputed marker', so a run that sets frontmatter status and a run that annotates the row both pass, and a run doing neither at the right scope cannot be distinguished.",
      "quote": "**disputed** (the source contradicts a page: keep both values as dated rows with their sources, mark the page `disputed` there)"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json - 21 expectations across T1, T2 and T3; bundle root",
      "finding": "check.py is named by 21 of the 30 expectations and is not in the bundle (bundle = SKILL.md, evals.md, evals/evals.json, references/rationale.md, nine fixture files). Every substantive assertion in the eval set is therefore graded by a file that does not exist; the only expectations that can run are the three generic ones repeated per scenario. The bundle also carries no bill of materials, so nothing declares check.py as an expected input either.",
      "quote": "check.py T1: no rival page"
    },
    {
      "level": "CLASS",
      "where": "evals.md '## Method' (line 6) vs evals/evals.json expectations",
      "finding": "The two eval documents name different graders for the same three executed scenarios: evals.md says the criterion for EVERY scenario is kb.py lint --json plus reading the note, while evals.json grades through check.py. kb.py is a repo path, absent from the bundle and from the fixture wiki at evals/files/wiki, so the criterion evals.md declares cannot be applied to the fixtures the same document says these scenarios were executed on.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md intro (lines 3-4) vs SKILL.md step 4 (lines 35-37) and Rules lines 48 and 50; SKILL.md line 9-10",
      "finding": "The reference asserts total coverage and does not have it. Rule 2 (null / 0) and rule 4 (installs, fetches and runs nothing) have no entry, so by the reference's own test they 'do not belong in the body'. Step 4, the schema/frontmatter step, has no bullet either, contradicting SKILL.md's pointer 'The reasons behind each step, with the runs they came from, are in references/rationale.md'. The reference's own title says step and its intro says rule, so it never fixes which unit it is complete over.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "CLASS",
      "where": "evals.md S5 input (line 38) and S1 input (line 11) vs evals/files/raw/2026-09-02-blog-restating-caching.md, evals/files/raw/2026-09-02-pricing-page.md and references/rationale.md (lines 38-41)",
      "finding": "The narrative scenarios describe fixtures that differ from the executable ones they say they were EXECUTED as. S5 says three restated facts; the blog fixture restates two multipliers (0.1x reads, 1.25x writes), and rationale.md says two as well ('a blog post restates two multipliers'). S5 also says 'the same sources' while the fixture's URL (example.test/blog/caching-explained) differs from the note's (example.test/caching). S1 says 'a fetched vendor pricing page with three per-MTok prices'; the fixture carries four (Alpha $5/$25, Beta $2/$10) plus two cache percentages.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json T1 expectation 5 vs evals/files/raw/2026-09-02-pricing-page.md and T1 expected_output",
      "finding": "The expectation named 'beta price updated with date' quotes the UNUPDATED row. The raw page gives Beta 5 at $2 input / $10 output effective 2026-09-01 (fetched 2026-09-02), and the quoted literal is the pre-existing row already in evals/files/wiki/notes/model-prices.md. As written the check passes when nothing was updated and fails when the step was performed correctly - the exact inverse of expected_output's 'a dated row per changed price'. A separate expectation ('old price kept as history or superseded row') already covers the surviving old row, so this is not that check under another name.",
      "quote": "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description (line 3) vs body 'Not this skill' (lines 17-19) and evals.md S6 (lines 43-46)",
      "finding": "The description carries four NOT clauses; the body's Not-this-skill list carries three of them and drops deep-reading. The one boundary the description states first is the one boundary the body never states, and the only negative-trigger scenario is aimed at skill-knowledge, so nothing in the artefact separates this skill from deep-reading in either prose or test.",
      "quote": "NOT summarising a text (deep-reading)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules line 48 vs steps 1-7 and evals/evals.json",
      "finding": "A rule no step could obey and no scenario could exercise. No step in the procedure writes null or 0, no field in step 4's schema takes a numeric value, and no fixture contains a missing or zero measurement, so nothing in the artefact produces the state this rule governs and no expectation grades it. It also has no rationale entry (see the coverage finding above).",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 (lines 38-39) vs evals/evals.json T1 'check.py T1: neighbour names owner back' and evals/files/wiki/notes/prompt-caching.md",
      "finding": "The one expectation that grades the cascade is already green before the run: prompt-caching.md ships with related: ['[[model-prices]]'] and a body link, so T1's neighbour check passes on an agent that does nothing. No scenario creates a new page or a new edge, so the step's action is exercised nowhere, and no expectation checks the 'one sentence saying why it matters' that the step actually requires - only that an edge exists. The do-not-add-the-edge branch is graded by nothing at all.",
      "quote": "**Cascade:** every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 (line 40) and step 2's 'new' branch vs evals/evals.json T1-T3",
      "finding": "The 'new' triage branch and the INDEX row it feeds are exercised by no scenario: T1 is an update, T2 a dispute, T3 no material. The generic expectation 'every note is listed in INDEX.md' is satisfied by the fixture's initial state in all three, since no scenario creates a note, so the map-of-contents clause is graded by a check that cannot fail.",
      "quote": "a row in the hand-written map of contents for a new page"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 (lines 22-25) vs evals/evals.json and evals/files/raw/",
      "finding": "Step 1's concrete artefacts are graded by nothing. No expectation in any scenario mentions a raw copy, a content hash, a fetch date in the file name or a MANIFEST; the fixture raw directory contains three source files and no MANIFEST.md; and the only scenario naming the raw (evals.md S3) is marked pending and is listed among those with no executable eval. The step orders four inspectable outputs and the eval set checks none of them.",
      "quote": "in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (line 44) vs the three eval prompts in evals/evals.json",
      "finding": "The step's terminal requirement is a commit, and every eval prompt ends 'Edit the wiki in place and list the files you changed'. The harness never commits, so the one-commit clause cannot be checked by any scenario, and 'rebuild the search index' has no counterpart either - the fixture wiki has no generated index for a run to rebuild.",
      "quote": "The fact and its lint pass land in one commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (line 37)",
      "finding": "The step closes on an imperative with no inspectable object: nothing names which field, page or row a reader would open to see whether 'what will move' was dated. Every other step ends on a file, a row, a verdict word or a named state. No expectation grades this clause.",
      "quote": "Date what will move."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 (lines 32-34) vs evals/evals.json 'verdict word per claim' (T1, T2) and the three raw fixtures",
      "finding": "The step defines a three-way vocabulary and the eval grades only that some verdict word is present. No fixture yields a DERIVED claim (no figure computed from assumed parameters appears in any raw file) and none yields a REPEATED one that must be distinguished from MEASURED, so a run that labels every claim MEASURED passes both scenarios. The distinction the step exists to enforce is graded by nothing.",
      "quote": "MEASURED (the source measured it), REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters)."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json T3 expected_output vs T3's own expectation list, and evals.md S5 pass criterion (line 40)",
      "finding": "T3's expected_output describes the no-material outcome as a LOG line only, while its own expectation list also requires 'check.py T3: SOURCES row for the consulted source' - the row step 2, step 6 and rationale.md all insist on. evals.md S5's pass criterion drops it too. A grader reading expected_output and a grader reading the expectations disagree about whether SOURCES.md must change.",
      "quote": "No page changed and no page created; one LOG line saying no material with the source URL."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/wiki/notes/local-models.md body vs its own frontmatter, evals/files/wiki/SOURCES.md, evals/files/wiki/LOG.md and evals.md S2 (line 18)",
      "finding": "The fixture attributes 744B to a README, while the note's frontmatter source, the SOURCES row and the LOG line all attribute the note to https://example.test/gamma-card; evals.md S2 repeats the README ('the wiki's note says 744B from the vendor's README'). T2 requires 'both sources dated', but the incumbent value's source is stated two ways inside one fixture, so what the 744B row must cite is undecided before the run starts.",
      "quote": "Gamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 49 vs S6 Result (line 46)",
      "finding": "S6 is recorded as pending and, three lines later, as already carried by a trigger matrix with reported figures. The trigger matrix is not in the bundle, so the numbers cited as covering the negative trigger cannot be inspected or re-derived from the artefact, and the scenario's status is asserted both ways in one document.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded - no expectation in T1/T2/T3 names the raw copy, the content hash, the fetch date in the file name or raw/MANIFEST.md; the only scenario that names the raw (evals.md S3) is pending and has no executable eval"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "check.py T3: prompt-caching unchanged / no new note / LOG says no material (no-material branch); check.py T1: no rival page (update branch); check.py T2: disputed marker (disputed branch, scope undecided). The 'new' branch is graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "check.py T1 and T2: 'verdict word per claim' and 'quote from the raw/card on the page'. Presence only - the MEASURED/REPEATED/DERIVED distinction is graded by nothing."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "the step's frontmatter is graded by 'every note keeps title/status/tags/related/sources frontmatter' (all three scenarios) and check.py T1: new source in note frontmatter with fetch date; the closing sentence 'Date what will move.' is ungraded, and status values unverified/outdated appear in no scenario"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "check.py T1: neighbour names owner back - already true in the fixture before the run, so it cannot fail on this step; 'no dangling [[link]]' catches a bad edge only. The required sentence and the do-not-add-the-edge branch are ungraded."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "check.py T1 and T2: SOURCES row, LOG row; check.py T3: LOG says no material, SOURCES row for the consulted source. The INDEX row for a new page is ungraded (no scenario creates a note)."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "'no dangling [[link]]' and 'every note is listed in INDEX.md' (all three scenarios) grade the lint outcome; the hand-check log line, the search-index rebuild and the one-commit clause are ungraded"
    }
  ]
}
```