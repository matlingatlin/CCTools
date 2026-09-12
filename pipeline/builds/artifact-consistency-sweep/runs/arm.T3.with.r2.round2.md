Read the method skill and its `references/pair-vocabulary.md`, then swept the artefact at `./artifact-C` (SKILL.md, references/rationale.md, evals.md, evals/evals.json, evals/files/check.py and the 10 fixture files). Parts identified: 7 steps, 3 rules, 7 description clauses, 23 evals.json expectations + 6 evals.md scenarios, 13 bundled files, 0 bill-of-materials rows (none ships).

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no material branch) vs steps 6 and 7",
      "finding": "The no-material branch says 'stop' and itself performs the source-log row and the operation-log line, but step 6 says those same rows happen 'in every branch' and 'also on no material', and step 7 (lint, rebuild the index) carries no branch qualifier at all. Either the branch stops before steps 6-7 - in which case step 6's 'in every branch' and step 7 are unreachable there - or it does not, in which case step 2 duplicates step 6. Nothing in the artefact resolves which.",
      "quote": "**no material** - no claim, no value, no newer date for any page: keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (update branch) vs evals/evals.json id 1 expectation 3",
      "finding": "An expectation no step produces. The eval requires the superseded price to survive as a dated row, but the update branch orders only 'extend it, never a rival' and says nothing about retaining an overwritten value; keeping both values as dated rows is ordered only in the disputed branch, and a newer price is not a dispute. Step 4's frontmatter offers `outdated` and `unverified` as status values that no step ever assigns, for the same reason.",
      "quote": "**update** - a page owns it: extend it, never a rival."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 ('exactly one') vs step 3, and vs the bundled T2 fixture",
      "finding": "Triage is forced into exactly one disposition per source, but step 3 then grades every number in the raw separately, and the bundled gamma model card is a source whose claims fall in two branches at once: 753B contradicts the note's 744B (disputed) while 'Active parameters: 40B' and 'Context: 1M tokens' are new material for the same page. No step says which disposition wins or what happens to the claims belonging to the losing branch.",
      "quote": "**Search, then triage into exactly one.**"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md description (frontmatter) vs the body's 'Not this skill' paragraph",
      "finding": "The body withholds the sibling names on the stated ground that they live in the instance section, while the description has already named five repo-local units (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator). The description promises a portability the body asserts; one of the two must change.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Method' vs evals/evals.json and evals/files/check.py",
      "finding": "Two different graders are named for the same scenarios. evals.md says every scenario is checked by a lint command at a host path that does not ship in the bundle; evals.json instead declares evals/files/check.py as a per-task input, and check.py is the only grader present. A reader following evals.md cannot run anything.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 54 (task T3) vs evals/evals.json id 3 prompt and expectation 1",
      "finding": "The central T3 expectation is graded by a check that cannot fail. The 'fixture' it hashes against resolves to check.py's own parent directory - evals/files/wiki/notes - which is exactly the wiki the prompt tells the agent to 'Edit the wiki in place'. Before and after are read from the same files, so 'byte-identical to the fixture' passes whatever the agent wrote. Step 2's 'touch no page' is therefore graded by nothing.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 37 and evals/evals.json id 1 expectation 8 vs SKILL.md step 5",
      "finding": "The only expectation that touches the cascade is already satisfied by the untouched fixture: prompt-caching.md ships with `related: [\"[[model-prices]]\"]` and a body link. The check passes with zero cascade work, so step 5 is effectively ungraded in every executed eval, and evals.md's S4 (the cascade scenario) is pending.",
      "quote": "check(\"neighbour names owner back\", \"[[model-prices]]\" in notes.get(\"prompt-caching\",\"\"))"
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md opening vs SKILL.md rule 3",
      "finding": "A rule with no stated evidence, against a file that promises there is none such. Rule 3 ('installs nothing and fetches no external code') has no entry anywhere in rationale.md, whose bullets cover the trigger, raw, topic ownership, no material, quoting, cascade, register and lint - all steps, not rules. The file's title ('Why each step exists') and its promise ('Every rule') also disagree about what it indexes.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs step 4",
      "finding": "Two destinations for the same rows. Step 3 permits the claim rows to live in a wiki-level claims ledger instead of the page; step 4 unconditionally requires the page body to carry a `## Claims` table with one row per claim, admitting no ledger alternative. A wiki with a ledger cannot satisfy both.",
      "quote": "The claim rows go in the page's `## Claims` table (step 4) or in the wiki's claims ledger where one exists."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs the bundled fixtures evals/files/raw/*.md",
      "finding": "The step forbids provenance inside the immutable raw file and requires it in a directory manifest; all three bundled raw files carry `source:` and `fetched:` inside the file, and evals/files/raw/ contains no manifest. No expectation grades a manifest, so the bundle's own example contradicts the step it is meant to exercise.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md rule 3 vs SKILL.md step 1",
      "finding": "A rule forbidding what a step orders. Step 1 requires a hash and a size in the manifest; computing either requires running something that is not the wiki's query, lint or index command, which rule 3 closes with 'and nothing else'.",
      "quote": "It runs the wiki's own query, lint and index commands, and nothing else."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md (no material bullet) vs evals.md S5",
      "finding": "The same measurement is reported with two denominators. The rationale says every baseline run was 2 of 2; evals.md records the no-material baseline as 0/5 across without, probe and incumbent arms. The rationale's parenthetical counts only the probe arm while claiming to count every run.",
      "quote": "every baseline run (2 of 2) still edited the owning page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 input vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says three restated facts; the rationale's worked example and the actual fixture blog restate two multipliers (0.1x cache read, 1.25x cache write). The scenario description does not match the source it is run on.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Method' vs the S5 and S2 scenario labels and results",
      "finding": "The method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails, yet S5 is classified '· normal' and is the one scenario carrying that verdict, while S2 is classified '· trap' and reports a clean baseline. The classification and the verdict rule contradict each other on both scenarios.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals/evals.json id 1 expectation 4 and check.py line 32",
      "finding": "Two different bars for the same claim row. evals.md demands the verdict MEASURED specifically; the eval expectation asks only for 'a verdict word' and the grader's regex accepts MEASURED, REPEATED or DERIVED interchangeably. Step 3's three-way distinction is therefore graded by nothing that separates the three.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 26 vs evals/evals.json id 1 expectation 1",
      "finding": "The 'no rival page' expectation is graded by a substring test that only fires on a new note whose stem contains 'pric'. A rival page named beta-5-costs or september-rates passes the check, so the expectation is weaker than the sentence it claims to enforce.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description clause 1 and step 1 vs evals.md line 49",
      "finding": "The description promises transcript, video-frame, paper and repo sources, and step 1 closes on the transcript rule, but the only scenario covering it has no executable eval; the same line leaves the cascade and the negative trigger ungraded. Three description clauses are backed by no runnable check.",
      "quote": "S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts",
      "finding": "The step's commit clause is graded by nothing and cannot be: no eval commits anything - all three prompts end 'Edit the wiki in place and list the files you changed' - and no expectation checks that a lint ran, that the index was rebuilt, or that the by-hand fallback was stated in the log line.",
      "quote": "The fact and its lint pass land in one commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'In this repo' vs steps 3 and 4",
      "finding": "The instance section attaches a null-versus-zero convention to a claims contract, but no step produces any field that convention could govern: step 4's claims table columns are claim | source | locator | verbatim quote | verdict, none of them numeric-or-null. The named contract steers nothing in the body.",
      "quote": "schema = this file + `CLAUDE.md`'s same-turn rule + `pipeline/contracts/claims.contract.json`, whose convention is `null` for not-measured and `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "bundle root - file × bill of materials",
      "finding": "No bill of materials ships with the artefact. The only declaration of bundled files is each eval's files list, which names three inputs and never names evals.md, references/rationale.md or evals/evals.json itself; SKILL.md names only references/rationale.md. A file could go missing from the bundle and only a run would reveal it, which is the failure this pair type exists to catch.",
      "quote": "\"files\": [\n    \"evals/files/wiki\",\n    \"evals/files/raw/2026-09-02-pricing-page.md\",\n    \"evals/files/check.py\"\n   ]"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded - the closing sentence ('A transcript or frame text is the raw for a video or image') names an inspectable file, but no expectation in evals.json checks that a raw was kept, that a manifest row exists, or that a transcript became a raw; all three evals hand the raw in as an input. evals.md S3 is the only transcript scenario and is pending."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json id 1 expectation 1 (update), id 2 expectation 4 'a row is marked disputed and the page status is disputed' (disputed), id 3 expectations 2-3 'no new note' / 'LOG.md says no material and names the blog' (no material). The 'touch no page' clause is nominally graded by id 3 expectation 1 ('byte-identical to the fixture'), but that check compares the wiki to itself and cannot fail. The **new** branch is graded by nothing - no eval creates a page."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json id 1 expectation 4 'a claims-table row carries the verbatim raw line and a verdict word'; id 2 expectations 2-3 (753B with the card's verbatim line, and 744B, each with a verdict word), via check.py T1/T2. The MEASURED / REPEATED / DERIVED distinction itself is ungraded - the grader accepts any of the three words."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals.json id 1 expectations 2 and 5 ('a Beta 5 row carries $2, $10 and a 2026-09 date'; the new source with its fetch date in frontmatter), id 2 expectations 5-6, and the common expectation 'every note keeps its frontmatter' (check.py schema check on title/status/tags/related/sources). The closing sentence's 'every price, version, limit, count and date' is graded only on the Beta 5 row; the `outdated` and `unverified` status values are graded by nothing."
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "effectively ungraded - the closing sentence 'No true sentence, no edge' turns on whether a sentence is true, which no reader or grader can inspect. The one expectation aimed at it, id 1 'prompt-caching still names [[model-prices]]', is already satisfied by the untouched fixture; evals.md S4 is pending."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json id 1 expectations 6-7, id 2 expectations 7-8, id 3 expectations 3-4 (a SOURCES row and a LOG line naming the source and the disposition, in all three tasks). The map-of-contents clause is ungraded - no eval creates a new page, and the common expectation 'every note listed in INDEX.md' is pre-satisfied by the fixture."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "ungraded - the closing sentence names a log line, but no expectation requires a lint run, an index rebuild, a single commit, or the by-hand fallback statement. The common expectation 'no dangling [[link]]; every note listed in INDEX.md' grades the wiki's end state, not that this step ran, and passes on the untouched fixture."
    }
  ]
}
```