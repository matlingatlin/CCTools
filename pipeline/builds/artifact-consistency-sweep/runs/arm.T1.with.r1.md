I read the method skill and its `references/pair-vocabulary.md`, then swept the artefact (found at `./artifact-A`: `SKILL.md`, `evals.md`, `evals/evals.json`, 9 fixture files).

**Inventory / plan counts:** 7 steps · 5 rules · 12 description clauses · 6 evals.md scenarios + 3 evals.json evals (0 `expectations` entries) · 12 files present · 5 distinct BOM-named paths.
**Rows examined:** step×rule 35/35 · step×step 21/21 · step×check 63/63 · description×body 12/12 · file×BOM 17/17 · claim×rationale 5/5 — 153/153, none below plan.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md Rules (bullet 5) vs step 7 and 'In this repo'",
      "finding": "A rule forbids exactly what a step orders: the rule says the skill runs no external code, while step 7 orders running the wiki's lint and the repo section names the command. Every run of step 7 breaks the rule.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline. || 7. **Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names before committing. || lint with `python3 knowledge/kb.py lint` (exit 1 on errors) and rebuild with `kb.py build`."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals",
      "finding": "Every eval carries an empty expectations array, so no step is graded by any machine check at all; the only grading is the prose expected_output. Nothing in the bundle can return a verdict.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json files[] vs the bundle (file × BOM)",
      "finding": "All three evals name a grader file that is not in the bundle; nothing under evals/files/ is called check.py. The declared grading path is absent for every scenario.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md Method vs the bundled fixture wiki",
      "finding": "The stated observable criterion for every scenario is a lint the bundle does not contain: evals/files/wiki holds only notes/, INDEX.md, SOURCES.md and LOG.md, and no eval's files[] includes kb.py. The grader named for all six scenarios cannot be run against the fixture.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "evals.md (S1-S6) vs evals/evals.json (evals 1-3)",
      "finding": "The two grading documents disagree on how many scenarios exist. evals.md declares six, evals.json contains three; S3 (video transcript), S4 (cascade under pressure) and S6 (negative trigger) have no eval entry and no fixture, so the raw layer, the cascade and the negative trigger are graded by nothing runnable.",
      "quote": "### S3 — a video transcript with no retrievable URL · edge || ### S4 — the cascade under time pressure · pressure || ### S6 — a claim to bundle into a skill · negative-trigger"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 vs step 4",
      "finding": "Step 1 requires a content hash inside the page's source entry; step 4's schema for that same source entry has three fields and no hash. A page written to step 4 cannot satisfy step 1, and no check covers either.",
      "quote": "the copy goes there with the fetch date in the file name and a content hash in the page's source entry. || Frontmatter with title, sources (url or path, fetch date, note), status from the fixed vocabulary, tags, related."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules (bullet 3)",
      "finding": "A rule stated nowhere a step could obey it: no step, no schema field and no claim-row field mentions null or 0, and no rationale or observed failure is given for it. It is unobeyable and ungraded.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (and step 2)",
      "finding": "The 'fixed vocabulary' of statuses is named but never given anywhere in the artefact, so no reader or grader can tell whether 'disputed' is a legal status value; the fixture uses 'status: verified' only.",
      "quote": "status from the fixed vocabulary"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4 (and evals.json eval 2 vs evals.md S2)",
      "finding": "'disputed' is defined at two scopes: step 2 marks the page disputed at the line where it disagrees, step 4 makes status a whole-page frontmatter field. The checks inherit the ambiguity ('at that line' vs 'at that fact'), so either behaviour can be graded correct.",
      "quote": "mark the page `disputed` where it disagrees || status from the fixed vocabulary || the note marked disputed at that fact"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals.md S1 pass criterion",
      "finding": "The step orders an index row on every ingest; the check for the ordinary update scenario requires the index to be unchanged. A run that obeys step 6 fails S1.",
      "quote": "One row in the index (map of contents), one row per source in the source log, one entry in the operation log saying what was ingested and what it changed. || no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs step 7",
      "finding": "Two mechanisms own the index: step 6 writes the row by hand, step 7 rebuilds the index afterwards (repo section: kb.py build), which discards or duplicates the hand-written row. Neither step says which wins.",
      "quote": "One row in the index (map of contents) || 7. **Lint, then rebuild the index.**"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 vs evals/files/wiki/notes/prompt-caching.md",
      "finding": "The only check touching the cascade passes on the untouched fixture: prompt-caching already names model-prices in its related list, so the expectation is true before the skill runs and grades step 5 vacuously.",
      "quote": "the neighbour still names the owner || related: [\"[[model-prices]]\"]"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 4",
      "finding": "The check requires a source entry with no URL or path at all; the schema requires 'url or path' in every source entry. Passing S3 means violating step 4.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR || sources (url or path, fetch date, note)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 7",
      "finding": "The check grades a lint severity distinction (INFO vs ERROR) that the artefact never defines; step 7 lists only which checks the lint runs, and the repo section says only 'exit 1 on errors'.",
      "quote": "lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules (bullet 2) vs step 7",
      "finding": "The rule justifies itself by a lint error that step 7's enumeration of lint checks does not include — there is no duplicate-topic or rival-page check in the list, so nothing catches the failure the rule names.",
      "quote": "One page owns a topic. Extending beats creating; a rival page is a lint error waiting. || (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs body 'When NOT to use'",
      "finding": "The description names a unit the body never mentions: deep-reading is excluded in the description, but the body's exclusion list covers only skill-knowledge, unified-memory, doc-claim-reconciliation and kb-curator.",
      "quote": "NOT summarising a text (deep-reading) || claims being gathered to bundle into a skill's `references/` go through `skill-knowledge` (same quote rule, different destination); a fact about the agent's own task state goes to `unified-memory`"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 6 (and the fixture INDEX.md)",
      "finding": "Step 2 orders querying the index by the source URL, but step 6 puts source URLs in the source log and the index holds only a map of contents; the fixture INDEX.md contains no URLs, so the ordered query cannot be run.",
      "quote": "Query the wiki's own index for the topic (title, trigger terms, the source URL). || One row in the index (map of contents), one row per source in the source log"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 6 / step 7",
      "finding": "The no-material branch stops before steps 6 and 7, so a source that is kept as raw gets no source-log row (step 6 orders one row per source) and no lint runs; eval 3 codifies the stop branch, leaving step 6's source-log clause and step 7 contradicted rather than scoped.",
      "quote": "keep the raw, write one operation-log line with the URL and the reason, and stop. || one row per source in the source log || No page changed and no page created; one LOG line saying no material with the source URL."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The scenario describes three per-MTok prices; the fixture carries four prices across two models plus two cache multipliers, so the input the criterion was written against is not the input that exists.",
      "quote": "a fetched vendor pricing page with three per-MTok prices || Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens. Beta 5: $2.00 per million input tokens, $10.00 per million output tokens."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 input vs evals/files/raw/2026-09-02-blog-restating-caching.md and SKILL.md Example",
      "finding": "S5 says three facts under the same sources; the fixture restates two multipliers under a different URL from the note's source, and the skill's own Example says two. The count and the 'same sources' condition contradict both the fixture and the body.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources. || a blog post restates two multipliers a note already carries with a dated source. || source: https://example.test/blog/caching-explained"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S6",
      "finding": "The Method asserts a file-state criterion for every scenario, but the negative-trigger scenario's criterion is that the talent does not fire — a routing outcome with no file state and no fixture to inspect.",
      "quote": "The observable criterion for every scenario is the state of the files || this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page)."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals/evals.json expected_outputs",
      "finding": "Step 3's central product — the claim row's verbatim line and its MEASURED/REPEATED/DERIVED verdict — appears in no evals.json expected_output; only evals.md S1/S3 mention it, and those are unrun with S3 having no fixture. The verdict vocabulary is graded by nothing.",
      "quote": "a verdict - **MEASURED** (the source measured it: dependent variable, effect, sample), **REPEATED** (asserted, no measurement found), **DERIVED** (computed from assumed parameters) || a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 and step 5 (last sentences)",
      "finding": "Both steps end in an assertion rather than an outcome: neither last sentence names a file, number, row or state that could be checked, so the steps end unchecked whatever the pairs say.",
      "quote": "A claim is not promoted by being repeated more often. || Parallel authoring produces one-way links structurally; this step is where they are closed."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header and every Result line",
      "finding": "The suite grades nothing yet by its own statement: the verdict is pending and all six scenario results are pending, so every 'graded by' in the matrix is a written criterion, not an observed one.",
      "quote": "**Last eval:** not run — suite authored 2026-09-02, status candidate until `eval-harness` baseline-vs-with has run · **Verdict:** pending"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 and S5",
      "finding": "The Method distinguishes PASS from 'PASS. Beats baseline.' per scenario, but S3 and S5 give a Baseline with no 'With talent' line, so the with-arm those scenarios are compared against is unstated.",
      "quote": "Baseline-vs-with per scenario; PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails. || - **Baseline:** writes a thin note anyway.\n- **Result:** pending"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing — the last sentence names a raw copy with the fetch date in its filename and a content hash in the source entry; no evals.json expected_output mentions the raw or a hash (all three prompts hand the raw in already), and evals.md S3, the only scenario naming the raw, has no eval entry and no fixture"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json eval 3 expected_output ('No page changed and no page created; one LOG line saying no material with the source URL') and eval 1 ('updated in place ... no new page'); evals.md S1 and S5 — prose only, since expectations is empty for all three evals"
    },
    {
      "step": 3,
      "checkable": false,
      "graded_by": "nothing for the claim row's verbatim line and verdict — no evals.json expected_output names a verdict or a quoted line; evals.md S1/S3 name MEASURED/REPEATED but are unrun and S3 has no fixture"
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals.json eval 1, partially ('the new source with its fetch date in frontmatter'); the status vocabulary, the four body sections and 'say what would make it wrong' are graded by nothing"
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "evals.json eval 1's 'the neighbour still names the owner', which is vacuous — already true in the untouched fixture; evals.md S4 is the only real cascade check and has no eval entry or fixture"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json evals 1 and 2 ('a SOURCES row and a LOG line') and eval 3 (LOG line); the index-row clause is graded by nothing and is contradicted by evals.md S1's 'INDEX unchanged'"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing — no evals.json expected_output mentions the lint or the commit; the grader named in evals.md's Method (python3 knowledge/kb.py lint --json) is outside the bundle, and evals/files/check.py does not exist"
    }
  ]
}
```