I ran the sweep against the pair vocabulary. Plan counts, examined counts: **step×rule 28/28** (7 steps × 4 rules) · **step×step 21/21** (all ordered pairs; 6 handoffs + the no-material branch crossings) · **step×check 252/252** (7 steps × 30 evals.json expectations + 7 × 6 evals.md scenarios) · **description×body 17/17** clauses · **file×BOM 17/17** (13 files present, 4 named-and-absent; no `bom.json` exists in the artefact, so that direction is checkable only from the artefact's own references) · **claim×rationale 11/11** (4 rules + 7 steps against 8 rationale bullets). Examined = plan = 346.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md Rules (4th bullet) vs step 7, step 2 and 'In this repo'",
      "finding": "A rule forbids what three parts of the body order. Rule 4 declares the skill runs nothing, while step 7 orders a lint and an index rebuild, step 2 orders a query, and the instance section names the exact commands to run. Every eval prompt also has the agent edit files. Either the rule means 'this skill does not install or call out to the network' and says something else, or steps 2 and 7 are unobeyable.",
      "quote": "\"This skill installs, fetches and runs nothing; it is a writing discipline.\" vs \"7. **Lint, then rebuild the search index;** fix what the lint names before committing.\" and \"lint `python3 knowledge/kb.py lint`; rebuild `kb.py build`.\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json (all 3 evals) × bundle contents",
      "finding": "21 of the 30 expectations delegate their verdict to a grader named check.py that is not in the bundle (the artefact ships SKILL.md, evals.md, evals.json, 3 raw fixtures, 6 wiki fixtures, references/rationale.md and nothing else). No bill of materials file exists in the artefact either, so nothing declares check.py as an expected input. Every step whose only grade is a check.py line is graded by nothing runnable.",
      "quote": "\"check.py T1: no rival page\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5 vs its own expected_output and evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The expectation named 'beta price updated' pins the literal PRE-EXISTING fixture row. The raw says Beta 5 is $2.00/$10.00 as of 2026-09-01; the fixture note already holds '| Beta 5 | $3 | $15 | 2026-08-20 |'. The check therefore passes on the untouched fixture and fails a correct update, contradicting the same eval's expected_output ('a dated row per changed price') and step 3.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\" vs raw \"Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 12 vs evals/files/wiki/notes/prompt-caching.md",
      "finding": "The only check that grades step 5 (cascade) is already satisfied by the untouched fixture: the neighbour prompt-caching already carries model-prices in its related list and in its body, so the expectation passes whether or not the agent cascades anything.",
      "quote": "\"check.py T1: neighbour names owner back\" vs fixture frontmatter \"related: [\\\"[[model-prices]]\\\"]\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 2, expectations 'LOG row', 'SOURCES row', 'model card in frontmatter sources' vs the wiki fixture",
      "finding": "Three of eval 2's registration checks are satisfiable by content the fixture already contains: LOG.md already has a gamma-card ingest line, SOURCES.md already has a gamma-card row, and local-models.md frontmatter already carries a gamma-card source. Unless check.py pins the new URL (https://example.test/gamma-7-model-card), these grade step 6 vacuously — the same defect the pair record logged as 'T2 LOG row vacuous'.",
      "quote": "fixture LOG.md \"- 2026-08-25 ingest: gamma-card -> local-models (new)\" vs expectation \"check.py T2: LOG row\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no material branch) vs steps 6 and 7",
      "finding": "The no-material branch orders a full stop after two log writes, but step 6 is written as if it is still reached on that branch ('also on no material') and step 7 states the lint-and-commit unconditionally, with rationale.md repeating it for every ingest. One branch, three incompatible endpoints: a reader cannot tell whether lint runs on a no-material ingest, and eval 3 grades neither.",
      "quote": "\"**no material** (... write the source-log row and one operation-log line with the URL and the reason, touch no page, stop)\" vs \"6. **Register:** ... a row per consulted source in the source log (also on no material)\" and \"The fact and its lint pass land in one commit.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4 (and evals.json eval 2 'disputed marker')",
      "finding": "'disputed' is defined at two scopes in two steps: step 2 marks it at the contested line, step 4 makes it a page-level frontmatter status value. The eval expectation that grades the disputed branch names neither scope, so a page-level status flip and a row-level marker both pass.",
      "quote": "\"mark the page `disputed` there\" vs \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\""
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening claim vs SKILL.md Rules",
      "finding": "The reference asserts completeness it does not have. Of the four rules, only 'Raw never edited' has a bullet. There is no rationale entry for the null/0 convention, for 'the wiki never the only copy of a fact', for 'nothing from memory', or for 'installs, fetches and runs nothing' — so by the reference's own test those rules 'do not belong in the body'. The rationale was moved out of the body without carrying every claim across.",
      "quote": "\"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules, bullets 3 and 4",
      "finding": "Two rules in the same list contradict each other: one orders looking a value up rather than recalling it, the next forbids fetching. No step resolves which wins when the wiki holds a stale price.",
      "quote": "\"Nothing about a tool, price, version or limit from memory: look it up and date it.\" vs \"This skill installs, fetches and runs nothing\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/evals.json and evals/files/raw/",
      "finding": "Step 1's three concrete outputs — a content hash, the fetch date in the file name, a provenance row in raw/MANIFEST.md — are graded by no expectation in any eval, and the fixture ships no raw/MANIFEST.md for a row to be added to. All three eval prompts hand the raw in already saved, so step 1 is a no-op in every executable eval.",
      "quote": "\"with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method and S1 vs evals/evals.json and the wiki fixture",
      "finding": "The two eval records name two different graders and neither is present. evals.md says every scenario is checked by kb.py lint --json; evals.json's expectations call check.py; the fixture wiki ships neither script. S1's pass criterion 'lint reports 0 errors' is therefore ungradable as written.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "The scenario states a fixture that does not exist. The blog fixture restates two multipliers (0.1x read, 1.25x write), and rationale.md twice says two; S5 says three facts. The eval record and its own fixture disagree on what is being ingested.",
      "quote": "\"**Input:** a blog post restating three facts the wiki already holds with the same sources.\" vs raw \"Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S5 label and result",
      "finding": "S5 is typed 'normal' but carries the 'Beats baseline' grade the Method reserves for scenarios where the baseline plausibly fails — and the same line calls it the one measured win. Either the label or the grading rule is wrong; as written the scenario blend cannot be read off the labels (S2 is typed 'trap' and produced no delta).",
      "quote": "\"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\" vs \"### S5 — no material · normal ... **Result:** PASS. Beats baseline\""
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S3, S4, S6 vs evals/evals.json",
      "finding": "Half the declared scenario set has no executable eval, and they are exactly the scenarios that carry the only grade for step 1 (raw for an unretrievable source), the only pressure test of step 5, and the negative trigger. The artefact discloses the gap but the disclosure does not close it: in the executable set no step is graded adversarially and no negative trigger exists at all.",
      "quote": "\"S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals/evals.json eval 2",
      "finding": "Step 3 orders a locator column per claim and a row for every number in the raw. No expectation in any eval grades a locator, and eval 2 grades only the parameter count — the card's other numbers (40B active, 1M context, 245 GB) are graded by nothing, so a run that transcribes one claim and drops three passes.",
      "quote": "\"One row per claim: claim, source, locator, verbatim line, verdict\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4, last sentence",
      "finding": "The step ends in a directive that names no file, number, row or state, so nothing about it can be observed; and no expectation grades dating a moving value. The step's checkable half (frontmatter fields) is graded only by a generic expectation that passes on the untouched fixture.",
      "quote": "\"Date what will move.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs the eval prompts in evals/evals.json",
      "finding": "Step 7's binding outcome is a commit containing both the fact and the lint pass. Every eval prompt instructs an in-place edit and a file list, with no commit and no repository, so the same-commit rule cannot be graded by any eval in the bundle.",
      "quote": "\"The fact and its lint pass land in one commit.\" vs \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md description and 'Not this skill' vs the 'In this repo (one instance)' section",
      "finding": "The artefact declares one section as the home for repo-local wiring, then puts five repo-local unit names (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator) in the description and the body outside it. The description promises a boundary a reader outside this repo cannot resolve — the same defect the prior review record logged as 'five repo-local names in the description'.",
      "quote": "\"NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent.\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json — the 3 generic expectations repeated in every eval",
      "finding": "Nine of the thirty expectations ('every note keeps ... frontmatter', 'no dangling [[link]]', 'every note is listed in INDEX.md') are already true of the untouched fixture wiki in all three evals. They grade non-regression, not the step, so counting them as coverage overstates what any step is graded by — most visibly for steps 4, 5 and 7.",
      "quote": "\"every note is listed in INDEX.md\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing executable. No expectation in evals.json names the raw file, the content hash, the fetch date in the file name, or raw/MANIFEST.md; all three prompts pre-supply the raw. Only evals.md S3 would grade it and S3 is 'pending' with no eval in evals.json."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json #1 'check.py T1: no rival page', #2 'check.py T2: disputed marker', #3 'check.py T3: no new note' + 'LOG says no material' + 'SOURCES row for the consulted source' — all four dispositions covered, but every one of these expectations is executed by check.py, which is absent from the bundle."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json #1/#2 'quote from the raw|card on the page' and 'verdict word per claim' (grader absent). The locator column and 'every number' are graded by nothing; eval 2's non-disputed numbers are ungraded."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "last sentence 'Date what will move.' names no observable state, so the step is unchecked by the last-sentence test. Its frontmatter clause is touched only by 'every note keeps title/status/tags/related/sources frontmatter', which passes on the untouched fixture; the four prescribed body sections and the dating rule are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "evals.json #1 'check.py T1: neighbour names owner back' only — and that expectation is already satisfied by the untouched fixture, so effectively ungraded. evals.md S4, the pressure scenario for this step, is 'pending'. Evals 2 and 3 have no cascade expectation."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json #1/#2/#3 'SOURCES row' and 'LOG row' (grader absent; in eval 2 both are satisfiable by pre-existing fixture lines). The 'row in the hand-written map of contents for a new page' clause is graded by nothing — no eval creates a new page."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing. No expectation runs a lint or grades its output, the fixture ships no lint script, the hand-check fallback log line is graded by nothing, and the same-commit rule cannot be reached from prompts that ask for in-place edits. The nearest expectations, 'no dangling [[link]]' and 'every note is listed in INDEX.md', pass on the untouched fixture."
    }
  ]
}
```