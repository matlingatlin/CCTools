I've read the method skill and its pair vocabulary, and swept the artefact (7 steps × 4 rules, 6 step-adjacency + 4 shared-term pairs, 7 steps × 30 evals.json expectations, 7 description clauses, 13 bundled files + 0 BOM rows + named paths, 4 rules × rationale entries).

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md — Rules bullet 4 vs step 7 and 'In this repo'",
      "finding": "A rule forbids what the last step orders. Step 7 orders 'Lint, then rebuild the search index' and the instance section supplies the commands (`python3 knowledge/kb.py lint`, `kb.py build`), which is running something; the rule says the skill runs nothing. Step 1 has the same clash on 'fetches' (it saves fetched source bytes with a fetch date). Either the rule needs a carve-out for the wiki's own lint/index tooling, or steps 1 and 7 must be phrased as hand-checks.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md — Rules bullet 3 vs Rules bullet 4",
      "finding": "One rule orders a look-up ('look it up and date it') while the next forbids fetching. No step resolves which wins when a price or limit is not already in the raw.",
      "quote": "Nothing about a tool, price, version or limit from memory: look it up and date it."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md — step 2 'no material' branch vs steps 6 and 7",
      "finding": "Step 2's branch ends in 'stop', which makes steps 6 and 7 unreachable — yet step 6 asserts the source-log row happens 'also on no material' and step 7 requires the lint pass in the same commit. The same two writes are ordered twice, by two steps, one of which cannot be reached. It is undefined whether a no-material ingest lints or commits at all.",
      "quote": "**no material** (no claim, no value, no newer date for any page: keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop)."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 'no newer date' vs evals/files/raw/2026-09-02-blog-restating-caching.md and evals.json eval 3",
      "finding": "Step 2 makes 'no newer date for any page' a condition of no material, but the eval-3 blog carries a fetch date of 2026-09-02 against prompt-caching's 2026-08-20 source. Read literally, the fixture the eval requires to be triaged 'no material' fails the test for it. The step never says whether 'date' means the fetch date or the as-of date of a value.",
      "quote": "fetched: 2026-09-02"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 4 frontmatter `status` vs step 2 'disputed' branch, and evals.json eval 2",
      "finding": "'disputed' is defined at two scopes: step 2 marks the page disputed 'there' (at the contradicted line), step 4 makes it a page-level frontmatter `status` value. Nothing says which a contradicted fact sets. Eval 2 grades an unqualified 'disputed marker', so both readings pass and neither is required.",
      "quote": "**Write the page in the schema:** frontmatter `title`, `sources` (url or path, fetched, note), `status` (`verified` / `unverified` / `disputed` / `outdated`), `tags`, `related`;"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 opening vs step 6, step 7 and references/rationale.md",
      "finding": "rationale.md warns that the hand-written map of contents and the generated search index 'are different things' and that an earlier draft conflated them — step 2 still says only 'the wiki's index', which is exactly that conflation surviving the rewrite. Separately, a search leaves no file state, so under evals.md's own file-state criterion nothing can grade that the query half of step 2 happened.",
      "quote": "**Search, then triage into exactly one:** query the wiki's index for the title, trigger terms and URL."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json (21 expectations) vs the bundle",
      "finding": "Twenty-one of the thirty expectations are delegated to `check.py` (9 in eval 1, 8 in eval 2, 4 in eval 3). No check.py exists anywhere in the bundle and no file declares where it comes from, so seven-tenths of the graded surface is graded by a program that is absent.",
      "quote": "check.py T1: no rival page"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 vs evals/files/wiki/notes/model-prices.md and evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The expectation named 'beta price updated' carries the row that is already in the fixture ($3 / $15, as of 2026-08-20). The raw page prices Beta 5 at $2.00 / $10.00, so the literal this expectation asserts is the pre-update value: it passes on a wiki nobody touched and fails if the update is performed correctly.",
      "quote": "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']"
    },
    {
      "level": "CLASS",
      "where": "bundle root — no bill of materials",
      "finding": "The bundle ships no bill of materials, so no row declares which files belong to it and no file can be found missing by declaration. Read against what the text names, three paths the tests depend on resolve to nothing shipped: check.py, `knowledge/kb.py` (evals.md's stated checker) and `pipeline/CURATION-LESSONS.md`. Only one bundled file, references/rationale.md, is pointed at by any other file; evals.md is named by nothing.",
      "quote": "test-bug → fix the test and record it in `pipeline/CURATION-LESSONS.md`; skill-bug → fix the step named; a step that cannot be fixed → drop only then."
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md preamble vs SKILL.md Rules",
      "finding": "The reference states its own completeness contract and then breaks it: of the four rules, only the first has an entry ('Raw kept, never edited'). The null/0 rule, the nothing-from-memory rule and the installs-nothing rule have no run and no source behind them — by the reference's own last clause they 'do not belong in the body'.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules bullet 2",
      "finding": "No step names `null` or `0`: step 4's frontmatter list does not say which fields may be null, step 3's verdicts are MEASURED/REPEATED/DERIVED with no null case, and no expectation in evals.json mentions either value. The rule is implemented by nothing and graded by nothing.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md preamble vs references/rationale.md organisation",
      "finding": "The body promises the reference holds the reason behind each step; the reference is organised by rule and its own preamble claims to cover rules, not steps. Step 4 ('Write the page in the schema') has no entry under either reading, so the pointer promises a rationale a reader cannot find.",
      "quote": "The reasons behind each step, with the runs they came from, are in `references/rationale.md` - open it when a step seems optional."
    },
    {
      "level": "CLASS",
      "where": "evals.md Method vs evals.md 'Not executed in the first build' and evals/evals.json",
      "finding": "The Method asserts an observable file-state criterion for every scenario checked by `kb.py lint --json`, but three of six scenarios (S3, S4, S6) have no executable eval, S6 is a negative trigger with no file state to check at all, and the executable set in evals/evals.json grades with check.py, not kb.py lint. Two different checkers are named for one criterion and neither ships.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs scenario S5",
      "finding": "The Method reserves the 'PASS. Beats baseline.' verdict for scenarios where the baseline plausibly fails, and reserves plain PASS for normal ones. S5 is labelled '· normal' and carries the beats-baseline verdict; it is also the only measured win. Either its label or the Method's rule is wrong.",
      "quote": "Baseline-vs-with per scenario; PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "S5 says the blog restates three facts with the same sources. The fixture blog restates two (0.1x read, 1.25x write) and its URL (example.test/blog/caching-explained) is not the note's source (example.test/caching); rationale.md's own before/after says two multipliers. The scenario's input description does not match the file the eval runs on.",
      "quote": "- **Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 'new' branch and step 6 vs evals/evals.json",
      "finding": "All three executable evals are update (eval 1), disputed (eval 2) and no material (eval 3). The 'new' branch — the case that creates a page and is the only one that triggers step 6's map-of-contents row — is exercised by no eval. 'every note is listed in INDEX.md' passes trivially because no run creates a note.",
      "quote": "**new** (no page owns the topic) · **update** (a page owns it: extend it, never a rival)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 closing vs evals/evals.json eval 1",
      "finding": "The branch turns on a condition no reader can inspect — the non-existence of a true sentence — and a correctly withheld edge is indistinguishable from a forgotten one. The only expectation touching the cascade, 'neighbour names owner back', is already satisfied by the untouched fixture (prompt-caching.md already lists [[model-prices]]), so it detects a regression but never requires a new edge. evals.md's cascade scenario S4 is pending.",
      "quote": "If no true sentence exists, do not add the edge."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/evals.json and evals/files/wiki",
      "finding": "Nothing grades any part of the raw discipline: no expectation mentions a saved raw, a content hash, a fetch date in a file name or raw/MANIFEST.md, and the fixture wiki contains no raw/ directory and no MANIFEST.md — the raws sit outside it, already saved by the fixture. evals.md's S3, which would cover it, is pending.",
      "quote": "Save the source bytes where the wiki can re-read them, never edited, with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts",
      "finding": "The commit clause cannot be satisfied under the evals: all three prompts say 'Edit the wiki in place and list the files you changed', the fixture is not a repository, and no expectation mentions a commit. 'rebuild the search index' is likewise graded by nothing and the fixture wiki has no generated index — only the hand-written INDEX.md. The orphan check named in the fallback is also graded by nothing.",
      "quote": "The fact and its lint pass land in one commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 closing sentence",
      "finding": "The step ends in an instruction that names no file, number, row or state: 'what will move' is never enumerated, so a reader cannot inspect whether it was done. The step's inspectable content (the frontmatter fields) is in an earlier sentence.",
      "quote": "Date what will move."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs step 1",
      "finding": "The description promises five source kinds — fetched page, paper, repo, transcript, measurement. Step 1 says what the raw is for a path/URL and for a video or image, but nothing says what the immutable raw is for a repo (a clone? a commit hash?) or a measurement produced locally, which has no URL to save. No eval covers either.",
      "quote": "A transcript or frame text is the raw for a video or image."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/wiki/LOG.md vs SKILL.md steps 2 and 6",
      "finding": "Steps 2 and 6 require an operation-log line carrying the URL and the reason. The only log line shipped as the worked example of the format carries neither — a bare source slug and a triage word. The fixture teaches a format the body forbids.",
      "quote": "- 2026-08-25 ingest: gamma-card -> local-models (new)"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 3 expectation vs its own expected_output and SKILL.md step 2",
      "finding": "The expected_output requires 'one LOG line saying no material with the source URL' and step 2 requires 'the URL and the reason', but the expectation checks only that the log says no material. A log line with no URL and no reason passes the graded check while failing the stated criterion.",
      "quote": "check.py T3: LOG says no material"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded — no expectation in evals/evals.json covers the raw, the hash, the fetch-dated filename or raw/MANIFEST.md; the fixture supplies the raws pre-saved. evals.md S3 would cover it and is pending."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "triage half only: 'check.py T1: no rival page' (update), 'check.py T2: disputed marker' (disputed), 'check.py T3: prompt-caching unchanged' + 'check.py T3: no new note' + 'check.py T3: LOG says no material' (no material). The 'new' branch and the search/query half are graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "'check.py T1: quote from the raw on the page' + 'check.py T1: verdict word per claim' (and the T2 equivalents). The locator column and the DERIVED verdict are graded by nothing."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "'every note keeps title/status/tags/related/sources frontmatter' + 'check.py T1: new source in note frontmatter with fetch date' — these grade the earlier schema sentence, not the closing 'Date what will move.'"
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "'check.py T1: neighbour names owner back' — but it is already true in the untouched fixture, so it grades only a regression; the 'no true sentence' branch is graded by nothing and evals.md S4 is pending."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "'check.py T1: SOURCES row', 'check.py T1: LOG row', 'check.py T2: SOURCES row', 'check.py T2: LOG row', 'check.py T3: SOURCES row for the consulted source'. The map-of-contents row for a new page is graded by nothing (no eval creates a page)."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "'no dangling [[link]]' + 'every note is listed in INDEX.md' + 'every note keeps title/status/tags/related/sources frontmatter' (the hand-check half only). The lint run, the index rebuild, the same-commit requirement and the orphan check are graded by nothing."
    }
  ]
}
```