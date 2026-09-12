```json
{
  "findings": [
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:53-57 (task T3)",
      "finding": "T3's central check — that no note changed — compares the wiki against itself. check.py lives at evals/files/check.py, so its 'fixture' path resolves to evals/files/wiki/notes, which is the same directory the eval prompt tells the agent to edit in place ('The wiki at evals/files/wiki ... Edit the wiki in place'). before and after are hashes of the same bytes read microseconds apart, so the check passes no matter what the agent wrote; it can only fail if a note is deleted outright. The one scenario the artefact calls 'the one measured win' is graded by nothing.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "evals/files/check.py:37 (T1), :46 (T2) vs evals/files/wiki/notes/*.md",
      "finding": "Checks that the fixture already satisfies before the agent runs. T1's 'neighbour names owner back' is true of the untouched fixture (prompt-caching.md already reads 'in [[model-prices]]'); T2's 'both sources dated' half-passes on the fixture, which already contains 2026-08-25 in both frontmatter and body. These grade the starting state, not the work, so a step whose only grader is one of them is effectively ungraded.",
      "quote": "check(\"neighbour names owner back\", \"[[model-prices]]\" in notes.get(\"prompt-caching\",\"\"))"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals/files/check.py:32-33 and evals/evals.json id 1",
      "finding": "The eval prose demands a specific verdict (MEASURED); both executable/expectation forms accept any of the three verdict words. An agent that grades the price REPEATED passes the grader and fails the written criterion.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals.md S1 pass criterion",
      "finding": "Step 3's own definitions make a vendor pricing page REPEATED, not MEASURED — a published price is asserted, not measured by the source. S1 nonetheless requires MEASURED for exactly that input. The step and the expectation it is graded against disagree about the right answer.",
      "quote": "MEASURED (the source measured it), REPEATED (asserted, no measurement found), DERIVED\n   (computed from assumed parameters)"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:30-31 and evals/evals.json id 1 expectation 3, vs SKILL.md step 2 'update'",
      "finding": "T1 grades a behaviour no step asks for: retaining the superseded price as a dated row. Step 2's update branch says only to extend the owner; keeping two values as dated rows is the *disputed* branch's instruction. A run that followed the skill exactly — replacing the Beta 5 price and dating it — fails this check.",
      "quote": "check(\"old price kept as a dated superseded row (Beta 5, $3, $15, 2026-08-20 on one line)\", bool(beta_old))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals/files/raw/2026-09-02-pricing-page.md and check.py T1",
      "finding": "Step 2 requires triage into exactly one disposition, but the T1 source is two dispositions at once: an update for model-prices and a pure restatement of prompt-caching's 0.1x/1.25x. No T1 check forbids adding the pricing page to prompt-caching as a corroborating source — which is precisely the failure T3 exists to catch and rationale.md names as the baseline's error.",
      "quote": "Cache reads are billed at 10% of the input price; cache writes at 125%."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 ('no material') vs step 7 and the description",
      "finding": "The no-material branch ends with 'stop', which skips step 7. Step 7 states the lint and index rebuild unconditionally, and the description lists 'lint' as part of the invariant shape ('one source, one shape, every time'). check.py T3 checks no lint at all, so the contradiction is also invisible to the grader.",
      "quote": "keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 ('disputed') vs step 4 claim-row shape vs check.py:44,46",
      "finding": "Step 2 requires marking a claim row `disputed` and keeping both values as *dated* rows, but step 4 fixes the claim row at five columns with neither a status nor a date column. check.py T2 then requires 'disputed' on a table row and both dates present. The row the skill specifies cannot carry what the skill and the grader demand of it.",
      "quote": "claim | source | locator | verbatim quote | verdict"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs the shipped bundle",
      "finding": "The stated grader for every scenario is a script that is neither in the bundle nor in the eval fixture; the fixture wiki (evals/files/wiki) has no kb.py, and the grader actually shipped is evals/files/check.py. The document describes a grading path the artefact cannot execute.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json (all three ids) vs evals/files/check.py:4",
      "finding": "check.py is listed in every eval's `files` but no prompt, expected_output or expectation invokes it, and nothing anywhere maps eval id 1/2/3 to the T1|T2|T3 argument the script requires. The only deterministic grader in the bundle has no invocation contract; the expectations are prose that some unnamed reader must judge.",
      "quote": "Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>"
    },
    {
      "level": "CLASS",
      "where": "evals.md vs evals/evals.json",
      "finding": "Two rival eval specifications for one skill: evals.md holds six scenarios S1-S6 with one set of criteria, evals/evals.json holds three ids with a different set (S1 wants 'INDEX unchanged, SOURCES +1 row', id 1 asks for neither; S1 wants MEASURED, id 1 wants 'a verdict word'). Neither names the other or says which governs — the artefact does to itself what its own step 2 forbids.",
      "quote": "**update** - a page owns it: extend it, never a rival."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 3 vs the S1/S2/S5 scenario lines",
      "finding": "The header states three arms at k=2; the scenario lines report four arm labels (with, without, probe, incumbent) and k=1 for the 'without' arm. S5's '0/5 baseline runs' likewise sums three baseline arms plus the with-arm, i.e. four.",
      "quote": "with 2/2, without 1/1, probe 2/2, incumbent 2/2"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S5",
      "finding": "S5 is typed 'normal' but carries the verdict Method reserves for scenarios where the baseline plausibly fails — and it is the single result the whole ITERATE verdict rests on. Either the scenario's type or the verdict grade is wrong.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S6 Result vs 'Not executed in the first build'",
      "finding": "S6's result is 'pending' four lines above the claim that its evidence is already carried by a trigger matrix with precise counts. The matrix is cited as evidence but is not in the bundle, so its three numbers can be checked against nothing.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 ('new') and step 6 vs the executed scenarios",
      "finding": "The 'new' triage branch and step 6's 'row in the hand-written map of contents for a new page' are exercised by no executed scenario: T1 forbids a new page, T2 is an update, T3 changes nothing, and S3 — the only case that would create one — is pending. check.py's index: check only iterates notes that already exist and are already listed.",
      "quote": "**new** - no page owns the topic."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 4 vs evals/files/wiki/notes/*.md and check.py:20",
      "finding": "The schema the skill mandates is contradicted by the artefact's own fixture. No fixture note has a `## Claims` table, and check.py's schema: check passes them anyway because it tests only five frontmatter keys. T3 then requires those non-conforming notes to be preserved byte-identical, so the grader enforces the opposite of step 4 on the untouched pages.",
      "quote": "a `## Claims` table with one row per claim - claim | source | locator | verbatim quote | verdict"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs evals/files/wiki/notes/local-models.md",
      "finding": "Step 4 requires an as-of date on every limit and count in the body; the fixture note states a memory limit with none, and T3 requires that note preserved byte for byte. No check anywhere tests for as-of dates, and no check tests the 'locator' column step 4 specifies.",
      "quote": "Every price, version, limit, count and date in the body carries its as-of date."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py:26 vs :58",
      "finding": "Two different strengths for the same requirement. T3 forbids new notes by exact set equality; T1's 'no rival page' only fires on a filename containing the substring 'pric', so a rival note named beta-5-costs or 2026-09-prices-update passes T1 unnoticed.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs check.py",
      "finding": "Step 7's fallback for a wiki with no lint script ends in a log-line statement, and names orphans as one of the three things to check by hand. No check reads the log for that statement, and orphans are checked nowhere in the artefact. The 'fact and its lint pass in one commit' clause is likewise ungraded — the eval tasks edit in place and never commit.",
      "quote": "No lint script in this wiki? Check dangling links, unlisted pages and orphans by hand and say so in the log line."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/raw/ and references/rationale.md",
      "finding": "Step 1's manifest requirement, which rationale.md says a field trial added deliberately, is represented nowhere in the eval bundle: evals/files/raw/ has no MANIFEST.md, no expectation mentions provenance, and no check reads the raw directory. Step 1 is pre-satisfied by the fixture in all three tasks and graded by nothing.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals/files/raw/2026-09-02-blog-restating-caching.md (T3)",
      "finding": "Step 2 disqualifies a source from 'no material' if it carries a newer date for any page. The T3 blog is fetched 2026-09-02 against prompt-caching's 2026-08-20 source, so by the letter of the step it is not no-material — yet T3 grades any edit to prompt-caching as a failure. The step's own disqualifier contradicts the scenario the step was rewritten for.",
      "quote": "**no material** - no claim, no value, no newer date for any page"
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md",
      "finding": "The artefact's own reference file writes numbers in the shape step 3 forbids for a wiki page: counts and run tallies with no locator and no MEASURED/REPEATED/DERIVED verdict, alongside one claim that does carry a verbatim quote and a fetch date. The discipline the skill imposes on its user is applied inconsistently inside the bundle.",
      "quote": "The first lint over the host\n  repository's 44 notes found 33 one-way links and 6 dangling ones."
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S1-S6",
      "finding": "The scenario template is not held: S1, S2 and S4 carry a 'With talent' line, S3, S5 and S6 omit it — including S5, the only scenario claimed as a measured win. A reader cannot tell whether the omission means 'not specified' or 'not run'.",
      "quote": "- **Baseline:** writes a thin note anyway.\n- **Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing. No check in check.py and no expectation in evals.json inspects evals/files/raw/, a fetch date, or a manifest; all three fixtures pre-supply the raw file, so the step is satisfied before the agent starts."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "partially. The chosen disposition is graded by check.py 'LOG line names the source and the disposition' (T1 update, T2 disputed) and T3 'LOG says no material and names the source', mirrored by evals.json id1 exp 7, id2 exp 8, id3 exp 3. The 'search the index first' half, the 'exactly one' constraint, and the 'new' branch are graded by nothing; T3's no-page-touched half is the vacuous self-comparison at check.py:53-57."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "partially. check.py T1 'a claims-table row carries the verbatim raw quote AND a verdict word' and T2's 753B/744B row checks. Only one row per task is required, so 'every number, date and quote' is untested; any of the three verdict words passes, so the correctness of the verdict — the point of the step — is graded by nothing."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "partially. check.py's per-note schema:<stem> check (presence of five frontmatter keys only), plus T1 'new source in note frontmatter with fetch date' and T2 'model card in frontmatter sources'/'page status disputed'. The Claims-table heading, its five-column shape, the locator column, and the per-value as-of dates are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "nothing effective. Its only grader is check.py T1 'neighbour names owner back', which the untouched fixture already satisfies. The 'one sentence saying why it matters' requirement and the 'no true sentence, no edge' rule are untested, and S4 — the scenario written for this step — is pending with no executable eval."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "partially. check.py 'SOURCES row' and 'LOG line names the source and the disposition' in all three tasks, plus the per-note index:<stem> loop, and evals.json id1 exp 6-7, id2 exp 7-8, id3 exp 3-4. The map-of-contents row for a new page is exercised by no executed scenario, since none creates a page."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "nothing, as written. The fixture wiki ships no lint or index command, the tasks edit in place and never commit, so 'fix what the lint names before committing', 'rebuild the search index' and 'one commit' have no observable in this harness; the manual fallback's 'say so in the log line' is read by no check and orphans are checked nowhere. The only proxy is check.py's common link:<a>-><b> and index:<stem> loops, which test two of the facts a lint would report rather than the step."
    }
  ]
}
```