```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals",
      "finding": "Every eval carries an empty expectations array, so nothing in the runnable suite is machine-graded. All grading rests on the prose expected_output field, which no check reads. No numbered step in SKILL.md is graded by an executable assertion.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json files lists (evals 1, 2, 3) vs the bundled tree",
      "finding": "Bill-of-materials mismatch: each eval declares a checker file that is not in the artefact. The bundle contains only evals/files/raw/ and evals/files/wiki/. The single named grading mechanism for the whole suite is absent.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S1–S6 vs evals/evals.json",
      "finding": "Six scenarios are declared, three are implemented. S3 (edge: raw for a transcript), S4 (pressure: the cascade) and S6 (negative trigger) have no runnable counterpart, so step 5 and the negative-trigger requirement are graded by prose only, and the required negative-trigger test does not exist as a run.",
      "quote": "### S3 — a video transcript with no retrievable URL · edge"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 1 and 3 vs step 4 schema, the fixtures and every expected_output",
      "finding": "Fields the steps make mandatory have no home in the schema the same file defines and are checked nowhere: step 1's content hash and step 3's locator appear in no frontmatter field list, no fixture note, and no eval expectation. Step 4's frontmatter fields are only url-or-path, fetch date and note.",
      "quote": "A claim is one row: what it says, source, locator, verbatim line, and a verdict"
    },
    {
      "level": "CLASS",
      "where": "evals.md scenario inputs vs evals/files/raw/*",
      "finding": "The scenario inputs described in evals.md do not match the bundled fixtures, so a run cannot tell which description is authoritative: S1 says three prices where the fixture states four prices plus two cache multipliers; S5 says three facts where the fixture (and SKILL.md's own Example) has two multipliers.",
      "quote": "**Input:** a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs SKILL.md Example and evals.md S1",
      "finding": "The verdict vocabulary contradicts its own use. Step 3 defines MEASURED as a source that measured something (dependent variable, effect, sample) and REPEATED as asserted with no measurement; a vendor pricing page asserts a price and measures nothing, yet both the Example and S1's pass criterion require the price row to be graded MEASURED. Under the step, that row must be REPEATED.",
      "quote": "**MEASURED** (the source measured it: dependent variable, effect, sample), **REPEATED**"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4",
      "finding": "The step ends in something uncheckable: it demands a status drawn from a fixed vocabulary that the artefact never enumerates. The fixtures use 'verified', step 2 uses 'disputed', and nothing states the legal set, so no reader or check can decide whether a written status is valid.",
      "quote": "status from the fixed vocabulary"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs step 2 and evals.md S1",
      "finding": "Step 6 is stated unconditionally, but two other places forbid what it requires: step 2's no-material branch says no page is touched and the run stops after one log line (no source-log row), and S1's pass criterion for an update requires the index to be unchanged (no index row). Step 6 carries no exception clause for either branch.",
      "quote": "One row in the index (map of contents), one row per source in the source log, one entry in the operation log saying what was ingested and what it changed."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs step 7",
      "finding": "The index is written twice by two different mechanisms in conflicting order: step 6 hand-writes a row, step 7 rebuilds the index after the lint has already run. A rebuilt index either overwrites the hand-written row or makes it redundant, and lint's 'unlisted pages' check is graded against the pre-rebuild index with no re-lint required.",
      "quote": "7. **Lint, then rebuild the index.**"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules vs step 7, 'In this repo', and evals.md Method",
      "finding": "The rule forbids running code while three other parts of the artefact mandate executing scripts (the wiki's deterministic lint, kb.py lint, kb.py build, kb.py lint --json as the grading criterion). 'External' is never defined, so the rule cannot be applied or checked.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules vs step 7's lint list",
      "finding": "The rule asserts the lint catches rival pages, but the enumerated lint checks in step 7 (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) contain no duplicate- or rival-page check. Nothing in the artefact would ever raise this error.",
      "quote": "One page owns a topic. Extending beats creating; a rival page is a lint error waiting."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules",
      "finding": "A rule graded by nothing and owned by no step: no step, no schema field, no fixture note and no eval expectation involves a null-or-zero value, so this rule has no surface on which it could pass or fail.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 4 and step 7",
      "finding": "S3 requires a source entry that is a note with no URL, contradicting step 4's schema which requires url or path; it also requires the lint to report that source at INFO rather than ERROR, but no severity levels exist anywhere in the artefact and the in-repo lint is described only as exit 1 on errors.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals.md header and Results",
      "finding": "The body cites evidence from baseline runs to justify the no-material rule, while the eval record states no eval has been run and every scenario result is pending. One of the two claims must be false; the observation is supported by nothing in the artefact.",
      "quote": "Observed 2026-09-02: without this rule, every baseline run on a restating blog post still edited the owning page (a second source plus a claims row), so \"no material\" quietly became \"update\"."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs the bundle",
      "finding": "The single stated observable criterion for every scenario is a script at a repo path that is not in the artefact; the bundled eval wiki ships no lint at all (and the failure-triage section likewise points at pipeline/CURATION-LESSONS.md, also unbundled). Every 'lint reports 0 errors' criterion is therefore unverifiable as shipped.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 vs evals/files/wiki/notes/local-models.md",
      "finding": "The pass criterion cannot be met by a correct ingest: the bundled wiki starts with local-models.md carrying related: [] and linked back by no note, which step 7's own lint list counts as an orphan/one-way link. The fixture is red before the skill runs.",
      "quote": "lint reports 0 errors; INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 vs evals.md S1",
      "finding": "The same scenario has two graders that demand different things. The JSON expects the superseded price kept and says nothing about a verbatim line, a verdict, lint or the index; S1 requires the verbatim line and MEASURED, lint 0 errors and INDEX unchanged, and says nothing about keeping the superseded price. Neither is a subset of the other.",
      "quote": "The owning note (model-prices) is updated in place: a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter; no new page; a SOURCES row and a LOG line; the neighbour still names the owner."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/raw/2026-09-02-pricing-page.md vs SKILL.md step 2 and evals/evals.json eval 1",
      "finding": "The eval-1 fixture forces two triage outcomes at once, which step 2 forbids: its price lines are an update to model-prices, while its cache lines restate the 0.1x/1.25x that prompt-caching already holds with a dated source — no material by the artefact's own definition. Eval 1's expected output covers only the price branch, so the correct handling of the cache lines is graded by nothing.",
      "quote": "Triage into exactly one of: **new** (no page owns the topic),"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2, SKILL.md Example, evals.md S5, evals/files/wiki/LOG.md",
      "finding": "The no-material log line has four incompatible shapes and no step says which passes: step 2 requires the URL and the reason, the Example shows a line with no date, S5 requires the URL and date, and the fixture log's only row uses a fourth format (date + 'ingest:' + arrow + outcome).",
      "quote": "the log says `no material: <url> restates"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S3, S5, S6",
      "finding": "The method declares a baseline-vs-with comparison for every scenario, but three scenarios ship only a baseline arm with no 'With talent' line, so there is nothing to compare the baseline against and no way to award the stated verdict.",
      "quote": "Baseline-vs-with per scenario; PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs 'When to use' and step 7",
      "finding": "The description is narrower than the body it advertises: the body triggers on a screenshot, image, video or tool output, none of which the description's source list names, and the description promises 'lint' where step 7 also requires rebuilding the index.",
      "quote": "- A fetched page, paper, repository, transcript, screenshot or tool output has told you"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts",
      "finding": "Step 7 makes a commit part of the procedure's completion condition, but no numbered step performs a commit, the eval prompts stop at editing the wiki in place, and the only place a commit is graded (S4) has no runnable eval.",
      "quote": "A verified fact and its lint pass land in the same commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'In this repo' vs step 6",
      "finding": "The instance section names three register targets but does not map them onto step 6's three registers: the index and source log are identified, the operation log is not, and pipeline/STATUS.md is listed without being said to be it. A reader cannot check step 6 in this instance.",
      "quote": "register in `knowledge/INDEX.md`, `knowledge/sources/SOURCES.md` and `pipeline/STATUS.md`;"
    },
    {
      "level": "INSTANCE",
      "where": "artefact root",
      "finding": "The artefact ships no references/ directory. Nothing in SKILL.md claims one, so no internal claim is broken, but the claim-row field contract the steps depend on is deferred to an unbundled file (pipeline/contracts/claims.contract.json), leaving step 3's row schema unresolvable from the artefact alone.",
      "quote": "`pipeline/contracts/claims.contract.json` (the claim-row fields and the three"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "none — the raw copy, its fetch date and its content hash are checked by no eval; only evals.md S3 mentions the raw, and S3 has no runnable counterpart in evals.json"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json #1 (update), #2 (disputed), #3 (no material) — prose expected_output only, expectations: [] and check.py missing; the 'new' branch is graded by nothing, and #1's fixture mixes update with no material uncovered"
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "none executable — evals.md S1 and S3 name the verbatim line and verdict in prose (S1 contradicting step 3's MEASURED definition); no evals.json expected_output mentions a quote, locator or verdict at all"
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "evals.json #1 partially (new source with fetch date in frontmatter); the status vocabulary is never enumerated and 'say what would make it wrong' has no criterion, so the step cannot be fully checked by anything"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "none — evals.md S4 grades the cascade in prose but has no runnable eval; evals.json #1's 'the neighbour still names the owner' asserts pre-existing fixture state, not a cascade the run performed"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json #1 (SOURCES row + LOG line) and #3 (LOG line), prose only; no eval checks an index row, and S1 requires the index to be unchanged, contradicting the step"
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "none — no lint ships in the bundle (check.py absent, kb.py is an unbundled repo path), the lint has no defined severity levels, the fixture wiki already violates the enumerated checks, and the commit requirement is exercised by no eval"
    }
  ]
}
```