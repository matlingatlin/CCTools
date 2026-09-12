```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals.md §Method vs evals/files/check.py + evals/files/wiki/",
      "finding": "Every grading claim that rests on a lint is unbacked: the stated observable criterion is a lint run, but the bundled grader never runs a lint, and the bundled eval wiki ships no lint script (no kb.py, no lint of any kind). This invalidates the Method statement, S1's 'lint reports 0 errors', S3's INFO-vs-ERROR criterion, and step 7's grading.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "evals.md §Method vs evals/files/check.py docstring",
      "finding": "The two graders contradict each other on what grading is: evals.md admits a human reading step ('by reading the note') as part of the criterion, while the bundled code grader declares itself judgement-free. No eval says which one decides a scenario, so any expectation the code cannot express is graded by an unrecorded human read.",
      "quote": "Every check is a fact about the files; no judgement."
    },
    {
      "level": "CLASS",
      "where": "evals.md scenario pass criteria vs evals/files/check.py",
      "finding": "The pass criteria evals.md reports as measured are strictly stronger than what the executable grader checks. S1 requires the verdict MEASURED, but the grader accepts any of three verdict words; S1 requires 'INDEX unchanged', but the grader only checks that every note appears in INDEX and would pass an added row; S1 requires 'lint reports 0 errors', which nothing runs. The reported result therefore does not evidence the stated criterion.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row."
    },
    {
      "level": "CLASS",
      "where": "evals/files/check.py (T1 'neighbour names owner back'; T3 'byte-identical to the fixture') vs evals/files/wiki/",
      "finding": "Two checks are satisfied by the fixture's pre-existing state and pass without the behaviour occurring, so they grade nothing. They are the only checks covering step 5 (cascade) and the artefact's single measured win (no material).",
      "quote": "check(\"neighbour names owner back\", \"[[model-prices]]\" in notes.get(\"prompt-caching\",\"\"))"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:54 (T3) vs evals/evals.json id 3 prompt and files list",
      "finding": "The no-material byte-identity check compares the wiki against itself. check.py resolves the 'fixture' to its own sibling directory evals/files/wiki/notes — the very wiki the eval instructs the agent to edit in place, and the same path copied into the workspace — so before == after unconditionally and an edited note still passes.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json (all three entries) vs evals/files/check.py usage line",
      "finding": "Nothing invokes the grader. check.py requires a task argument (T1|T2|T3), but evals.json only lists it as a copied file, carries no command, and never mentions running it; the id-to-task mapping exists only in evals.md prose. All three evals therefore reduce to their free-text expectations.",
      "quote": "Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:26 (T1 'no rival page')",
      "finding": "The check meant to enforce step 2's 'extend it, never a rival' only rejects a new note whose filename contains the substring 'pric'. A rival page named beta-5-costs, vendor-2026-09 or model-costs passes, so the rule's central failure mode is ungraded.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/raw/",
      "finding": "Step 1 mandates a provenance manifest in the raw directory, but the bundled raw/ directory contains only the three source files and no manifest, and no eval expectation or grader check mentions one. The requirement is contradicted by the artefact's own materials and graded by nothing.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs SKILL.md steps 6 and 7",
      "finding": "The no-material branch orders a stop, while step 6 asserts the operation-log line happens 'in every branch' and step 7 is written unconditionally (lint, rebuild the index, one commit). Whether a no-material ingest gets a lint pass, an index rebuild and a commit is left contradictory, and no eval grades that branch's tail.",
      "quote": "no claim, no value, no newer date for any page: keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expectations vs SKILL.md steps 2 and 4",
      "finding": "The eval requires the superseded price to be retained as a dated row, but no step in the body says so: step 2's update branch only says extend, never a rival, and step 4 only requires an as-of date on values present. Retention of the old value is required by the body only in the disputed branch, which this scenario is not. The eval grades a rule the skill never states.",
      "quote": "the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 / step 4 vs evals/files/check.py claim-row checks",
      "finding": "The body specifies a five-field claims row under a named heading; the grader only requires a line beginning with a pipe that carries a quote and a verdict word anywhere in the note. No check requires a `## Claims` heading or a locator field, so the pre-existing price table satisfies the claims-row checks and the specified row schema is graded by nothing.",
      "quote": "a `## Claims` table with one row per claim - claim | source | locator | verbatim quote | verdict"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals/files/check.py LOG checks (T1, T2, T3)",
      "finding": "Step 6 requires the operation-log line to name three things — disposition, source URL and the pages touched — but every grader check tests only the disposition word and a source slug. 'The pages touched' is graded by nothing in any of the three executed evals.",
      "quote": "one operation-log line naming the disposition, the source URL and the pages touched, in every branch."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md opening claim vs SKILL.md Steps/Rules",
      "finding": "The rationale asserts total coverage of the body, and by its own standard the uncovered rules do not belong in the body. Several load-bearing rules have no entry: the disputed branch (two dated rows, page-level status disputed for as long as any row is), the schema and per-value as-of-date requirement of step 4, the installs-nothing/runs-only-the-wiki's-commands rule, and 'the wiki is never the only copy of a fact'.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md (no material entry) vs evals.md S5 result line",
      "finding": "The two files give different baseline denominators for the same observation. The rationale says every baseline run was 2 of 2; evals.md counts five baseline runs (without 0/1, probe 0/2, incumbent 0/2) and reports the win as 0/5. Nothing in the artefact reconciles which population 'every baseline run' names.",
      "quote": "every baseline run (2 of 2) still edited the owning page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 input vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md before/after",
      "finding": "The scenario describes a blog restating three facts; the bundled blog restates two multipliers, and the rationale's worked example also says two. The eval prose does not match the fixture it is graded on.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The scenario says three per-MTok prices; the bundled pricing page carries four (Alpha 5 input/output, Beta 5 input/output) plus two cache percentages. The scenario description does not match its own fixture.",
      "quote": "a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs evals.md S5 heading and result",
      "finding": "The method reserves the beats-baseline verdict for scenarios where the baseline plausibly fails, yet S5 is classified normal and is the only scenario awarded that verdict — and is described as the rule-driving win. Either the classification or the method rule is wrong; as written the one measured win is reported under a verdict its own method forbids for a normal scenario.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs S1/S2/S5 arm counts",
      "finding": "The header preregisters three arms at k=2, but each scenario reports four arms (with, without, probe, incumbent) and the without arm ran once, not twice. The design as stated and the results as recorded do not agree, so the repeat claim ('the T3 win survived both repeats') covers only the with arm.",
      "quote": "the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Not executed in the first build — bill of materials",
      "finding": "The evidence substituted for the missing negative-trigger eval is not in the bundle. No trigger matrix, run log or build directory ships with the artefact, so the S6 claim rests on numbers that cannot be checked from anything present, and S3/S4/S6 remain graded by nothing.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md §When to use vs SKILL.md §Steps",
      "finding": "The trigger admits a case the procedure has no branch for: step 2 forces triage into exactly one of new / update / disputed / no material, none of which is a compiled summary written back. No step, expectation or check covers the write-back path the skill invites.",
      "quote": "An existing page gains a source, or a compiled summary page is written back."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md §Rules",
      "finding": "A rule with no procedure and no observable. No numbered step produces a second copy of a fact, nothing defines what the other copy would be, and no eval expectation or grader check touches it — it cannot be violated or satisfied detectably.",
      "quote": "the wiki is never the only copy of a fact."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 3 expected_output vs its own expectations list",
      "finding": "The expected output states that nothing changes but the log line, while the expectations list for the same eval requires a SOURCES.md row (as does SKILL.md step 2's no-material branch). The eval's own summary contradicts the checks under it.",
      "quote": "No page changed and no page created; one LOG line saying no material with the source URL."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts (all three)",
      "finding": "Step 7's terminal obligation is a commit containing both the fact and the lint pass, but every eval ends at editing files in place and listing them. The step's end state is outside what any eval can observe, and the by-hand fallback ends in a self-report ('say so in the log line') that no check reads.",
      "quote": "The fact and its lint pass land in one commit."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing. No expectation in evals.json and no check in check.py looks at a raw copy, the fetch date in the file name, or the manifest row; the fixture pre-places raw/ outside the wiki so the step is never exercised, and raw/ ships without the MANIFEST the step requires."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "partially — check.py LOG-disposition checks: T1 'LOG line names the source and the disposition' (update), T2 'LOG line names the card and the disposition' (disputed) plus 'page status disputed', T3 'LOG says no material and names the source' + 'no new note'. Ungraded: the index query that precedes triage (no artefact), the 'new' branch (no eval creates a page), and 'extend, never a rival' beyond the substring-'pric' filename test."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "partially — check.py T1 'a claims-table row carries the verbatim raw quote AND a verdict word on the same line' and T2's two claims-row checks. Ungraded: 'every number, date and quote' (only one row is required in T1, and the pricing page carries four prices), and the MEASURED/REPEATED/DERIVED distinction itself, since the regex accepts any of the three where evals.md S1 says MEASURED."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "partially — check.py common check 'schema:{stem}' requires title, status, tags, related, sources on every note, in all three tasks; T1/T2 check the new source with its fetch date in frontmatter. Ungraded: the whole body contract (what it is / `## Claims` heading / what it means here / what is open), the five-field claim row including the locator column, and 'every price, version, limit, count and date in the body carries its as-of date' (dates are checked only on the two Beta 5 rows)."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "nothing that can fail. The only check is T1 'neighbour names owner back', which the fixture already satisfies before any edit; no check requires the sentence that step 5 says the edge depends on ('No true sentence, no edge'), and S4, the scenario written for this step, is pending with no executable eval."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "partially — check.py 'SOURCES row' in T1/T2/T3 and the LOG-line checks in T1/T2/T3; the common 'index:{stem}' check covers INDEX listing. Ungraded: the INDEX row for a new page (no eval creates one) and 'the pages touched' in the log line."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing. No eval runs a lint or an index rebuild, the bundled eval wiki ships no lint script, no eval reaches a commit, and the no-lint fallback resolves to a self-attestation in the log line that no check reads. evals.md's claim that every scenario is checked by kb.py lint --json is unsupported by any bundled file."
    }
  ]
}
```