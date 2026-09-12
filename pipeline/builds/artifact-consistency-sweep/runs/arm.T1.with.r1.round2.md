Note on location: there is no `./artifact` — the artefact under review is `./artifact-A` (SKILL.md, evals.md, evals/evals.json, evals/files/…); it ships **no** `references/` directory and no `bom.json`, so the file×BOM set is the 12 bundled files plus the paths the text names.

Parts identified per the method's reference: 7 steps, 5 rules, 7 description clauses, two rival expectation sets (evals.md — 6 scenarios; evals/evals.json — 3 entries), 12 bundled files.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md Rules (5th bullet) vs steps 1, 2 and 7 + In this repo + evals.md Method",
      "finding": "A rule forbids exactly what three steps order. Step 7 orders 'Run the wiki's deterministic lint', step 2 orders querying the index (the repo section spells that as python3 knowledge/kb.py find), step 1 requires computing a content hash, and the eval method grades by python3 knowledge/kb.py lint --json. Either the rule is false or the steps and the eval method are unexecutable.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no material branch) vs steps 6 and 7",
      "finding": "Step 2's no-material branch ends in 'stop', but steps 6 and 7 are written unconditionally ('One row in the index, one row per source in the source log' / 'A verified fact and its lint pass land in the same commit'). A run in the no-material branch either violates step 2 or violates steps 6-7; the artefact never says which wins. evals.json eval 3 silently sides with 'stop' by expecting only a LOG line.",
      "quote": "**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 6 vs evals/evals.json eval 1 and evals.md S1",
      "finding": "Step 6 orders an index row on every ingest, with no condition. Both expectations for the same scenario require the index to be untouched ('INDEX unchanged', 'no new page'). A run that obeys step 6 fails the eval that grades step 6.",
      "quote": "**Register.** One row in the index (map of contents), one row per source in the source log, one entry in the operation log saying what was ingested and what it changed."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (disputed branch) vs step 4 vs evals.md S2 vs evals/evals.json eval 2",
      "finding": "The term 'disputed' is used at two scopes and never reconciled: a page-level status ('mark the page disputed', and step 4's frontmatter 'status from the fixed vocabulary', the fixture using status: verified) and a line-level or fact-level mark ('where it disagrees', S2's 'marked disputed at that line', eval 2's 'marked disputed at that fact'). A run cannot tell whether to change the frontmatter status or annotate one row, and the two eval sets word it differently again.",
      "quote": "mark the page `disputed` where it disagrees"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4",
      "finding": "Step 4 defers to a 'fixed vocabulary' of statuses that nothing in the bundle defines. The fixture notes show only 'verified' and step 2 introduces 'disputed'; no file, reference or contract in the artefact lists the permitted values, so the step cannot be checked.",
      "quote": "status from the fixed vocabulary"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, files list of evals 1, 2 and 3 vs the bundle",
      "finding": "Every eval entry declares evals/files/check.py as an input file. No check.py exists anywhere in the artefact (the bundle holds 12 files: SKILL.md, evals.md, evals/evals.json, 3 raw sources, 6 wiki files). All three evals name a grader that is absent.",
      "quote": "evals/files/check.py"
    },
    {
      "level": "CLASS",
      "where": "evals.md (6 scenarios) vs evals/evals.json (3 entries) vs evals/files/",
      "finding": "The artefact ships two disjoint expectation sets and says nothing about their relationship. Only S1, S2 and S5 have a counterpart in evals.json; S3 (video transcript), S4 (cascade under pressure) and S6 (negative trigger) have no eval entry and no fixture under evals/files/, so the steps they alone grade (1 and 5) and the negative trigger are graded by nothing runnable.",
      "quote": "### S4 — the cascade under time pressure · pressure"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, expectations field of all three evals; evals.md Method",
      "finding": "Every eval entry's expectations array is empty, so the runnable suite asserts nothing mechanically; grading falls back to prose expected_output. The one checker evals.md names, python3 knowledge/kb.py lint --json, is not in the bundle and the fixture wiki contains no lint tool. Nothing in the artefact can produce a pass or fail.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals.md S1 vs evals/evals.json eval 1 (same scenario, same fixture)",
      "finding": "The two expectation sets disagree on the pass criterion for the identical ingest. S1 requires the verbatim line, the MEASURED verdict, lint reporting 0 errors and INDEX unchanged; eval 1 requires none of those and instead requires the superseded price kept and the neighbour link intact. A run can pass one and fail the other.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 1 expected_output vs SKILL.md step 2 (update branch)",
      "finding": "The expectation requires the superseded price to be kept, but no step orders keeping a superseded value. Step 2's triage keeps both values only in the disputed branch (source contradicts the page); a newer price is an update, and the update branch says only 'extend that page, never a rival'. The eval grades behaviour the procedure never produces.",
      "quote": "The owning note (model-prices) is updated in place: a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter; no new page; a SOURCES row and a LOG line; the neighbour still names the owner."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 4 vs evals/files/wiki/notes/*.md vs all expectations",
      "finding": "Step 4 mandates four named body sections, but not one of the three bundled fixture notes has them (each is a title plus a table or a sentence), and no expectation in either eval set requires them. A run that obeys step 4 restructures a note in a way eval 1's 'updated in place' does not anticipate, and a run that ignores step 4 is graded no worse.",
      "quote": "Body: what it is, the claims graded, what it means for this project, what is still open."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 vs evals/evals.json evals 1-3 and evals/files/wiki/notes/",
      "finding": "Step 3 defines a five-field claim row with one of three verdicts, but no bundled note carries any of those fields (e.g. local-models.md states '744B total parameters (README, 2026-08-25)' with no verdict), and no evals.json expected_output mentions a verdict at all. Only evals.md grades MEASURED (S1) and REPEATED (S3); DERIVED is graded by nothing anywhere.",
      "quote": "A claim is one row: what it says, source, locator, verbatim line, and a verdict -"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/wiki/notes/*.md frontmatter, evals/files/ layout and evals/evals.json eval 1",
      "finding": "Step 1 requires the fetch date in the raw file's name and a content hash in the page's source entry. The fixture note schema has only url and fetched — no hash field — and eval 1 asks only for 'the new source with its fetch date in frontmatter'. The fixture wiki also has no raw/ directory (the raws sit outside it at evals/files/raw), so the branch this sentence governs cannot be exercised and the hash is graded by nothing.",
      "quote": "When the wiki has its own `raw/` directory, the copy goes there with the fetch date in the file name and a content hash in the page's source entry."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 2, 3 and 5 (closing sentences)",
      "finding": "Three of the seven steps close on a rationale or a maxim rather than on the state the step produces: step 3 on a general principle, step 2 on a past baseline observation, step 5 on why one-way links occur. A reader following the numbered procedure reaches the end of these steps with nothing named to inspect.",
      "quote": "A claim is not promoted by being repeated more often."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (title vs body)",
      "finding": "The step's title promises two actions, lint and rebuild, but the body orders only the lint and the fix. The rebuild appears nowhere in the procedure — only in the repo-instance section as 'rebuild with kb.py build' — so 'rebuild the index' is ordered by a heading and by no sentence.",
      "quote": "**Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names before committing."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules (3rd bullet) vs the seven steps and both eval sets",
      "finding": "A rule no step could obey and no expectation grades: no step ever writes a null or a numeric zero, the step-4 frontmatter schema (title, sources, status, tags, related) has no field that could be null or 0, and neither eval set mentions either value. The rule also carries no stated evidence, unlike the ownership rule which cites the 2026-09-02 observation.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs the body's 'When NOT to use'",
      "finding": "The description names four sibling boundaries plus kb-curator; the body's NOT list carries only four of them and drops deep-reading entirely. The boundary the description promises to hold is not stated in the body, and no scenario tests it (S6 tests the skill-knowledge boundary only).",
      "quote": "**When NOT to use:** claims being gathered to bundle into a skill's `references/` go through `skill-knowledge` (same quote rule, different destination); a fact about the agent's own task state goes to `unified-memory`; a document made false by a code change is `doc-claim-reconciliation`'s; finding what is wrong across the whole wiki is the `kb-curator` agent's job, not this one's."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S3, S5 and S6",
      "finding": "The method declares a baseline-vs-with comparison for every scenario, but three of the six scenarios carry no 'With talent' line at all (S3, S5, S6) and S6 carries no baseline either. The comparison the method promises is not written down for half the suite.",
      "quote": "Baseline-vs-with per scenario; PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 7",
      "finding": "The scenario grades on a lint severity distinction (INFO versus ERROR) that the skill never defines: step 7 says only to 'fix what it names'. No lint tool, severity table or fixture exists in the bundle to produce either level, so the criterion cannot be evaluated.",
      "quote": "lint reports the note-only source as INFO, not ERROR; claims from it are REPEATED, not MEASURED."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals/evals.json evals 1-3",
      "finding": "The cascade step is graded by no runnable eval. All three eval entries extend or leave alone an existing note, and eval 1's only neighbour clause asserts an unchanged link ('the neighbour still names the owner') rather than a new back-link with a reason. local-models.md, the note eval 2 touches, has related: [] and gains no neighbour under eval 2's expectation.",
      "quote": "**Cascade.** For every neighbour the page names, make the neighbour name it back with a sentence that says *why* - a `related:` entry alone is an edge nobody argued."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (closing) vs evals/evals.json and evals/files/",
      "finding": "The step's closing state is a commit, but the fixture at evals/files is not a repository and every eval prompt asks the model to 'Edit the wiki in place and list the files you changed'. No expected_output mentions a commit or a lint run, so the step's terminal condition is graded by nothing.",
      "quote": "A verified fact and its lint pass land in the same commit."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Failure triage vs the bundle",
      "finding": "The failure-triage line routes test bugs to a file that is not in the bundle and is not scoped as a repo-local example the way SKILL.md's 'In this repo (one instance)' paths are. The named destination does not exist.",
      "quote": "test-bug → fix the test and record it in `pipeline/CURATION-LESSONS.md`; skill-bug → fix the step named; a step that cannot be fixed → drop only then."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "partially evals.md S3 ('the transcript text is saved as the raw'), which has no fixture and no evals.json counterpart; ungraded in evals/evals.json — the fetch-date filename and the content hash are graded by nothing in either set"
    },
    {
      "step": 2,
      "checkable": false,
      "graded_by": "evals/evals.json eval 3 and evals.md S5 grade the no-material branch, evals.json eval 2 and S2 the disputed branch, evals.json eval 1 and S1 the update branch; the 'new' branch is ungraded. The closing sentence is a past baseline observation, not a state the step produces"
    },
    {
      "step": 3,
      "checkable": false,
      "graded_by": "evals.md S1 (verbatim line + MEASURED) and S3 (REPEATED); no evals/evals.json expected_output mentions a verdict or a locator; DERIVED is ungraded everywhere. The closing sentence is a maxim with nothing to inspect"
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals/evals.json eval 1 ('a dated row per changed price', 'the new source with its fetch date in frontmatter') and evals.md S1; the four mandated body sections and 'say what would make it wrong' are graded by nothing in either set"
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "evals.md S4 only, which has no fixture and no evals.json entry, so it is not runnable; ungraded in evals/evals.json. The closing sentence explains why the step exists rather than naming its product"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals/evals.json evals 1, 2 and 3 (SOURCES row, LOG line) and evals.md S1 and S5 — but the index row the step orders is graded in the negative ('INDEX unchanged'), so the step is contradicted by the checks that grade it"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "ungraded — evals.md S1 asserts 'lint reports 0 errors' and the Method names python3 knowledge/kb.py lint --json, but no lint tool ships in the bundle, evals/files/check.py is absent, all expectations arrays are empty, and no expected_output mentions a lint run, an index rebuild or a commit"
    }
  ]
}
```