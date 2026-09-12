I read all 13 files in the bundle end to end. Here are the findings.

```json
{
  "examined": {
    "artefact_path": "./artifact-B (the directory in the working tree is named artifact-B, not artifact)",
    "files_read_in_full": [
      "SKILL.md (57 lines: frontmatter, intro, When to use, Not this skill, Steps 1-7, Rules 1-4, In this repo)",
      "references/rationale.md (41 lines: 8 rationale bullets + a before/after worked example)",
      "evals.md (52 lines: header verdict, Method, S1-S6, Not-executed note, Failure triage)",
      "evals/evals.json (67 lines: 3 evals, 30 expectation strings)",
      "evals/files/raw/2026-09-02-pricing-page.md",
      "evals/files/raw/2026-09-02-gamma-model-card.md",
      "evals/files/raw/2026-09-02-blog-restating-caching.md",
      "evals/files/wiki/INDEX.md",
      "evals/files/wiki/LOG.md",
      "evals/files/wiki/SOURCES.md",
      "evals/files/wiki/notes/model-prices.md",
      "evals/files/wiki/notes/prompt-caching.md",
      "evals/files/wiki/notes/local-models.md"
    ],
    "pair_classes_swept": [
      "step x rule (7 steps x 4 rules = 28 pairs)",
      "step x step (21 ordered pairs, plus the branch/rejoin question for step 2's stop)",
      "step x eval expectation (7 steps x 30 expectations, rolled up per step)",
      "step x eval fixture (can the bundled wiki+raw even satisfy the step)",
      "description x body (5 promised exclusions, 8 promised mechanics, 5 promised source types)",
      "SKILL.md x references/rationale.md (rationale's own completeness claim x every rule and step)",
      "evals.md x evals/evals.json (6 scenarios x 3 executed evals: grader, pass criterion, arm counts)",
      "evals.md x evals.md (Method rule x each scenario's type and result line)",
      "bill of materials: every path named anywhere x what is on disk"
    ],
    "bill_of_materials_result": "references/rationale.md exists as named. evals/files/wiki and the three raw files exist as named in evals.json. check.py does NOT exist anywhere in the bundle. raw/MANIFEST.md does not exist. No lint script and no search index exist in the fixture wiki. The knowledge/*, pipeline/* and .claude/agents/* paths are the 'In this repo' instance section and are correctly outside the bundle.",
    "counts": {
      "files": 13,
      "numbered_steps": 7,
      "rules": 4,
      "scenarios_in_evals_md": 6,
      "executable_evals": 3,
      "expectation_strings": 30,
      "expectations_naming_a_missing_grader": 21,
      "description_length_chars": 650
    }
  },

  "findings": [
    {
      "id": "C1",
      "level": "CLASS",
      "where": "evals/evals.json:16-24, 39-46, 61-64 (21 of 30 expectations) vs the whole bundle",
      "finding": "Every substantive expectation delegates to a grader named check.py that is not in the artefact. Nothing else in the bundle defines what 'no rival page', 'disputed marker', 'verdict word per claim' or 'LOG says no material' mean operationally. Every step-specific grade in the artefact therefore rests on a file that is not present, and evals.md asserts that grader was run.",
      "quote": "\"check.py T1: no rival page\" ... \"check.py T2: disputed marker\" ... \"check.py T3: LOG says no material\"  |  evals.md:3 \"three arms, k=2, code grader, blinded, preregistered rule\""
    },
    {
      "id": "C2",
      "level": "CLASS",
      "where": "SKILL.md:47-50 (Rules) vs Steps 1-7 and all 30 expectations",
      "finding": "Orphan rules: three of the four rules are implemented by no step and graded by no check. The null/0 rule governs a field that the step-4 schema never introduces; 'never the only copy of a fact' has no step that verifies a second copy; 'runs nothing' is not only ungraded but contradicted (see I9).",
      "quote": "\"- `null` for not-fetched and not-measured; `0` only for a measured zero.\" / \"- Raw never edited; the wiki never the only copy of a fact.\" / \"- This skill installs, fetches and runs nothing; it is a writing discipline.\""
    },
    {
      "id": "C3",
      "level": "CLASS",
      "where": "references/rationale.md:3-4 vs SKILL.md:35-37 and :47-50",
      "finding": "The reference states a completeness invariant about itself that its own contents falsify. Step 4 (write the page in the schema) has no rationale bullet, and three of the four rules have none: the null/0 rule, 'the wiki never the only copy of a fact', and 'installs, fetches and runs nothing'. By the reference's own stated test those rules 'do not belong in the body' - yet they are in the body.",
      "quote": "\"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\""
    },
    {
      "id": "C4",
      "level": "CLASS",
      "where": "SKILL.md:29-31 vs evals.md:39 vs evals/evals.json:52 and :63",
      "finding": "The no-material operation-log line is specified three incompatible ways. The step requires URL + reason; evals.md requires URL + date; evals.json requires the words 'no material' + URL. No two agree, so an output satisfying the step can fail the eval and vice versa.",
      "quote": "SKILL.md: \"write the source-log row and one operation-log line with the URL and the reason\"  |  evals.md S5: \"an operation-log entry says \\\"no material\\\" with the URL and date\"  |  evals.json: \"one LOG line saying no material with the source URL\" / \"check.py T3: LOG says no material\""
    },
    {
      "id": "C5",
      "level": "CLASS",
      "where": "SKILL.md:26-31 (step 2) vs SKILL.md:32 (step 3) vs all three raw fixtures",
      "finding": "Step 2 demands a single disposition per source, but every bundled fixture carries several at once, so the artefact's own test data cannot be triaged as the step instructs. The pricing page is 'update' for model-prices and 'no material' for prompt-caching (it restates 10%/125%). The gamma card is 'disputed' for the parameter count, 'update' for the 40B active / 1M context claims, and 'no material' for the 245 GB figure the note already holds. Step 3's 'every number' then contradicts step 2 directly: the single-disposition rule discards claims step 3 requires be located and rowed.",
      "quote": "step 2: \"Search, then triage into exactly one:\"  |  step 3: \"Locate every number, date and quote in the raw before writing it.\"  |  raw pricing page: \"Cache reads are billed at 10% of the input price; cache writes at 125%.\"  |  raw model card: \"Total parameters: 753B. Active parameters: 40B. Context: 1M tokens.\""
    },
    {
      "id": "C6",
      "level": "CLASS",
      "where": "evals/evals.json:14, 24, 58, 60 vs evals/files/wiki/notes/*.md and INDEX.md",
      "finding": "Several checks are already satisfied by the starting fixture and so grade nothing an agent does. 'neighbour names owner back' is the only grade on step 5, yet prompt-caching.md already names [[model-prices]] in both body and frontmatter before the run. 'every note is listed in INDEX.md' is pre-satisfied because no eval creates a note. These checks pass on a wiki where the agent did literally nothing.",
      "quote": "expectation: \"check.py T1: neighbour names owner back\"  |  fixture prompt-caching.md, unmodified: \"related: [\\\"[[model-prices]]\\\"]\" and \"Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\""
    },
    {
      "id": "C7",
      "level": "CLASS",
      "where": "SKILL.md:22-24, :42-43 vs evals/evals.json prompts and evals/files/",
      "finding": "Steps whose outputs have no home in the eval environment, so they can neither be performed nor graded. There is no raw/ directory inside the fixture wiki (raws sit outside it at evals/files/raw/), no MANIFEST.md, no content hash, no search index to rebuild, and the prompts stop at editing files, never committing - while step 7 makes the commit the unit of the requirement.",
      "quote": "step 1: \"provenance in `raw/MANIFEST.md`\"  |  step 7: \"Lint, then rebuild the search index ... The fact and its lint pass land in one commit.\"  |  every eval prompt: \"Edit the wiki in place and list the files you changed.\""
    },

    {
      "id": "I1",
      "level": "INSTANCE",
      "where": "evals/evals.json:17 vs evals/files/raw/2026-09-02-pricing-page.md and evals/files/wiki/notes/model-prices.md",
      "finding": "The check named 'beta price updated' asserts the presence of the UNCHANGED, pre-existing row. The raw page prices Beta 5 at $2/$10 as of 2026-09-01; the literal the check looks for is the fixture's old 2026-08-20 row of $3/$15. As written the check passes when nothing was updated and would fail an agent that correctly replaced the row - it is either inverted or a duplicate of the 'old price kept' check two lines below.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\"  |  raw: \"Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.\"  |  fixture note: \"| Beta 5 | $3 | $15 | 2026-08-20 |\""
    },
    {
      "id": "I2",
      "level": "INSTANCE",
      "where": "evals.md:38 vs references/rationale.md:16-18, :38-41 and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The S5 input says three restated facts; the rationale and the actual fixture both have two. The blog states exactly two values (a tenth, 1.25x).",
      "quote": "evals.md: \"**Input:** a blog post restating three facts the wiki already holds with the same sources.\"  |  rationale.md: \"on a blog post restating two multipliers a note already held\"  |  fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\""
    },
    {
      "id": "I3",
      "level": "INSTANCE",
      "where": "evals.md:3 vs evals.md:10, :17, :37",
      "finding": "The header says three arms; every executed scenario reports four (with / without / probe / incumbent).",
      "quote": "header: \"the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule)\"  |  S1: \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "id": "I4",
      "level": "INSTANCE",
      "where": "evals.md:6 vs evals.md:37, :41",
      "finding": "The Method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails, and S5 is typed 'normal' - yet S5 carries exactly that verdict, and is the artefact's single measured win. Either the scenario type or the method rule is wrong.",
      "quote": "Method: \"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\"  |  \"### S5 — no material · normal\" ... \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "id": "I5",
      "level": "INSTANCE",
      "where": "evals.md:46 vs evals.md:49",
      "finding": "S6's result is recorded as pending, and three lines later the same document reports its numbers.",
      "quote": "\"**Result:** pending\"  |  \"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)\""
    },
    {
      "id": "I6",
      "level": "INSTANCE",
      "where": "evals.md:6 vs evals.md:43-45",
      "finding": "The Method claims a file-state criterion for every scenario; S6 is a negative-trigger whose criterion is that no files are touched by this skill at all and a sibling fires instead. A universal quantifier the document's own scenario list breaks.",
      "quote": "\"The observable criterion for every scenario is the state of the files\"  |  S6: \"**Pass criterion:** this talent does not fire; `skill-knowledge` does\""
    },
    {
      "id": "I7",
      "level": "INSTANCE",
      "where": "SKILL.md:3 vs SKILL.md:17-19",
      "finding": "The description advertises five exclusions; the body's 'Not this skill' paragraph carries four. deep-reading - the nearest and most confusable sibling, since summarising a text is what a careless reader will do with a fetched page - is promised by the description and absent from the body.",
      "quote": "description: \"NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation)\"  |  body: \"**Not this skill:** claims bundled into a skill's `references/` (`skill-knowledge`); agent task state (`unified-memory`); a document a code change made false (`doc-claim-reconciliation`); cleaning the whole wiki (`kb-curator` agent).\""
    },
    {
      "id": "I8",
      "level": "INSTANCE",
      "where": "SKILL.md:3 vs SKILL.md:22-24",
      "finding": "The description admits a 'measurement' as an ingestible source, but step 1 defines the raw as source bytes with a URL or path, a fetch date and a hash. A measurement you produced has no fetched bytes and no URL, and no step says what stands in for them. Step 1 makes an explicit accommodation for video and image but none for the measurement case the description sells.",
      "quote": "description: \"a fetched page, paper, repo, transcript or measurement is about to become a note\"  |  step 1: \"Save the source bytes where the wiki can re-read them, never edited, with URL or path, fetch date and a content hash\""
    },
    {
      "id": "I9",
      "level": "INSTANCE",
      "where": "SKILL.md:50 vs SKILL.md:26, :42, :56-57",
      "finding": "Rule 4 says the skill runs nothing; step 2 requires querying the index, step 7 requires running the lint and rebuilding the index, and the instance section gives the four commands to run. The rule is contradicted by two of the seven steps and by the artefact's own worked instance.",
      "quote": "rule: \"This skill installs, fetches and runs nothing; it is a writing discipline.\"  |  step 7: \"**Lint, then rebuild the search index;** fix what the lint names before committing.\"  |  In this repo: \"lint `python3 knowledge/kb.py lint`; rebuild `kb.py build`.\""
    },
    {
      "id": "I10",
      "level": "INSTANCE",
      "where": "SKILL.md:31 vs SKILL.md:41 and :42-44",
      "finding": "Step 2's no-material branch terminates the procedure, but step 6 then legislates for that same branch and step 7's lint-and-commit rule is unconditional. Whether the no-material path reaches steps 6 and 7 is answered both ways inside one seven-step list.",
      "quote": "step 2: \"touch no page, stop.\"  |  step 6: \"a row per consulted source in the source log (also on no material); an operation-log line.\"  |  step 7: \"The fact and its lint pass land in one commit.\""
    },
    {
      "id": "I11",
      "level": "INSTANCE",
      "where": "SKILL.md:30 vs references/rationale.md:16-22 and the S5 fixture",
      "finding": "Step 2 defines no material as the absence of any claim or value, which excludes the canonical no-material case the skill was rewritten around: the blog does state values, they are simply already held. The rationale gives the correct test ('adds no knowledge beyond what the wiki already holds') and the step does not.",
      "quote": "step 2: \"**no material** (no claim, no value, no newer date for any page...)\"  |  rationale.md: \"No material — adds no knowledge beyond what the wiki already holds.\"  |  fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times.\""
    },
    {
      "id": "I12",
      "level": "INSTANCE",
      "where": "SKILL.md:36 (step 4) vs SKILL.md:29 (step 2) vs evals.md:19 vs evals/evals.json:40",
      "finding": "Two different places to record a dispute and no rule for which. Step 4's schema has a frontmatter status value 'disputed' for the whole page; step 2 says to mark it at the contradicted line. The eval expectation says only 'disputed marker', so it cannot discriminate, and evals.md commits to the line-level reading without amending the schema.",
      "quote": "step 4: \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\"  |  step 2: \"mark the page `disputed` there\"  |  evals.md S2: \"the note marked disputed at that line\"  |  expectation: \"check.py T2: disputed marker\""
    },
    {
      "id": "I13",
      "level": "INSTANCE",
      "where": "SKILL.md:37 vs evals/files/wiki/notes/model-prices.md, prompt-caching.md, local-models.md",
      "finding": "Step 4 mandates a four-part body and not one of the three fixture notes has any of it - they are a heading plus a table or a sentence. The fixture is therefore a wiki the skill declares non-conformant, and an agent updating in place must either violate step 4 or restructure notes the evals expect to be otherwise untouched. No expectation grades the body structure, only the frontmatter.",
      "quote": "step 4: \"body: what it is, the claims graded, what it means here, what is open.\"  |  fixture note in full body: \"# Prompt caching\\n\\nCache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\"  |  expectation: \"every note keeps title/status/tags/related/sources frontmatter\""
    },
    {
      "id": "I14",
      "level": "INSTANCE",
      "where": "SKILL.md:22-24 vs evals/files/raw/*.md (all three)",
      "finding": "Step 1's own required artefacts are absent from the artefact's own raw files: no content hash on any of the three, and no MANIFEST.md anywhere in the bundle. The bundled raws satisfy only the two loosest clauses (a source line and the fetch date in the file name).",
      "quote": "step 1: \"with URL or path, fetch date and a content hash ... provenance in `raw/MANIFEST.md`\"  |  raw file in full header: \"source: https://example.test/pricing-2026-09\\nfetched: 2026-09-02\""
    },
    {
      "id": "I15",
      "level": "INSTANCE",
      "where": "evals.md:6 vs evals/evals.json:16 etc. vs evals/files/wiki/",
      "finding": "Two documents name two different graders for the same three runs, and the fixture wiki contains neither. evals.md commits to the repo's kb.py, which cannot run against a standalone fixture directory that has no kb.py, no INDEX schema it knows and no built index.",
      "quote": "evals.md: \"checked by `python3 knowledge/kb.py lint --json` and by reading the note\"  |  evals.json: \"check.py T1: ...\" (21 times)"
    },
    {
      "id": "I16",
      "level": "INSTANCE",
      "where": "evals.md:12 vs evals/evals.json:7, 20, 23",
      "finding": "S1's pass criterion and eval 1's expectations are not the same test. evals.md omits the LOG row and the superseded-price requirement that evals.json grades; evals.json omits the 'lint reports 0 errors' and 'INDEX unchanged' that evals.md requires. A run can pass either document and fail the other.",
      "quote": "evals.md S1: \"the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row.\"  |  evals.json: \"check.py T1: old price kept as history or superseded row\", \"check.py T1: LOG row\""
    },
    {
      "id": "I17",
      "level": "INSTANCE",
      "where": "evals.md:12 vs SKILL.md:33-34 and evals.md:26",
      "finding": "S1 requires the verdict MEASURED for prices taken off a vendor pricing page. Step 3 reserves MEASURED for a source that measured the thing and gives REPEATED for an assertion; a price list asserts. The artefact applies its own verdict ladder inconsistently - S3 correctly demands REPEATED for numbers merely displayed.",
      "quote": "step 3: \"MEASURED (the source measured it), REPEATED (asserted, no measurement)\"  |  S1: \"the owning note gains a dated row with the verbatim line and MEASURED\"  |  S3: \"claims from it are REPEATED, not MEASURED\""
    },
    {
      "id": "I18",
      "level": "INSTANCE",
      "where": "SKILL.md:8-9 vs SKILL.md:35-37",
      "finding": "The intro summarises the procedure as seven verbs against seven steps, but step 3 takes two of them (quoted, graded) and step 4 - actually writing the page, the point of the whole skill - gets none. The reader's index of the procedure silently omits its central act.",
      "quote": "\"Karpathy's LLM Wiki `ingest` operation made procedural: raw kept, triaged, quoted, graded, cascaded, registered, linted.\""
    },
    {
      "id": "I19",
      "level": "INSTANCE",
      "where": "SKILL.md:15 vs SKILL.md:21-44",
      "finding": "The second trigger promises a case no step handles. Writing back a compiled summary page is not an ingest of a source: it has no raw to keep (step 1), nothing to triage (step 2), no verbatim line to quote (step 3). The trigger admits work the procedure cannot process.",
      "quote": "\"- An existing note gains a source, or a compiled summary page is written back.\""
    },
    {
      "id": "I20",
      "level": "INSTANCE",
      "where": "evals/files/wiki/LOG.md:3 vs SKILL.md:31, :41 and evals/evals.json:63",
      "finding": "The fixture's only log line - the sole worked example of the format an agent will imitate - carries no URL, which both the step and the eval expectation require. The fixture teaches the format the grader rejects.",
      "quote": "LOG.md: \"- 2026-08-25 ingest: gamma-card -> local-models (new)\"  |  step 2: \"one operation-log line with the URL and the reason\"  |  expectation: \"check.py T3: LOG says no material\" / expected_output: \"one LOG line saying no material with the source URL\""
    },
    {
      "id": "I21",
      "level": "INSTANCE",
      "where": "evals/files/raw/2026-09-02-gamma-model-card.md vs evals/evals.json:30, 35-47",
      "finding": "Eval 2's source carries two claims the note does not hold - 40B active parameters and a 1M context - and neither the expected_output nor any of the eight expectations mentions them. Step 3 requires every number be located and rowed; nothing grades whether they were, and a run that drops them scores full marks.",
      "quote": "raw: \"Total parameters: 753B. Active parameters: 40B. Context: 1M tokens.\"  |  expected_output: \"Both parameter counts kept as their own dated rows with their sources, the note marked disputed at that fact, neither value overwritten; SOURCES and LOG rows.\""
    },
    {
      "id": "I22",
      "level": "INSTANCE",
      "where": "evals/files/wiki/SOURCES.md:1 vs evals/evals.json:64 and SKILL.md:41",
      "finding": "Eval 3 requires a SOURCES row for a source that by definition feeds into nothing, but the fixture's source-log schema has a mandatory 'Feeds into' column and no convention for the empty case. The required row cannot be written in the fixture's own format.",
      "quote": "SOURCES.md header: \"| Date | Source | Feeds into |\"  |  expectation: \"check.py T3: SOURCES row for the consulted source\"  |  step 6: \"a row per consulted source in the source log (also on no material)\""
    },
    {
      "id": "I23",
      "level": "INSTANCE",
      "where": "evals.md:38-41 vs evals/files/raw/2026-09-02-blog-restating-caching.md and evals/files/wiki/notes/prompt-caching.md",
      "finding": "S5 says the restated facts come with the same sources; the blog's source URL is not the note's. Small, but it is the fact that makes the scenario a no-material rather than a corroboration case, and the fixture does not have it.",
      "quote": "evals.md: \"a blog post restating three facts the wiki already holds with the same sources\"  |  blog raw: \"source: https://example.test/blog/caching-explained\"  |  prompt-caching.md: \"url: https://example.test/caching\""
    }
  ],

  "step_matrix": [
    {
      "step": 1,
      "text": "Keep the raw.",
      "ends_in_something_checkable": "partially - 'a file exists in raw/ with the fetch date in its name' is checkable; 'a content hash' and 'provenance in raw/MANIFEST.md' are checkable but no such artefact exists to check",
      "graded_by": "NOTHING. No expectation in any of the three evals reads evals/files/raw/, checks a hash, checks a MANIFEST, or checks that the raw was left unedited. The only pass criterion that would grade it is evals.md S3 ('the transcript text is saved as the raw'), and S3 has no executable eval.",
      "related_findings": ["C7", "I14", "C2"]
    },
    {
      "step": 2,
      "text": "Search, then triage into exactly one.",
      "ends_in_something_checkable": "the disposition itself is NOT checkable - no step requires the chosen label be written down anywhere. Only its downstream consequences are observable.",
      "graded_by": "PARTIALLY, by consequence only: eval 1 'check.py T1: no rival page' (the update branch); eval 2 'check.py T2: disputed marker' (the disputed branch); eval 3 'check.py T3: prompt-caching unchanged' + 'no new note' + 'LOG says no material' (the no-material branch). The 'new' branch is graded by nothing - no eval ingests a source no page owns. The 'exactly one' constraint is graded by nothing and is falsified by all three fixtures (C5).",
      "related_findings": ["C4", "C5", "I10", "I11"]
    },
    {
      "step": 3,
      "text": "Locate every number, date and quote in the raw before writing it. One row per claim: claim, source, locator, verbatim line, verdict.",
      "ends_in_something_checkable": "partially - 'verbatim line' and 'verdict' are checkable; 'locator' and the completeness of 'every number' are not checked anywhere; the step also never says where the claim rows live",
      "graded_by": "PARTIALLY: eval 1 'check.py T1: quote from the raw on the page' + 'verdict word per claim'; eval 2 'check.py T2: quote from the card on the page' + 'verdict word per claim'. Eval 3 grades neither (correctly - nothing is written). The 'locator' column is graded by nothing. Completeness is graded by nothing and eval 2 demonstrates the hole (I21). Which verdict is correct is graded inconsistently (I17).",
      "related_findings": ["I17", "I21", "C5"]
    },
    {
      "step": 4,
      "text": "Write the page in the schema (frontmatter + four-part body).",
      "ends_in_something_checkable": "yes for the frontmatter; the four-part body is checkable in principle but the fixture notes violate it from the start",
      "graded_by": "PARTIALLY: 'every note keeps title/status/tags/related/sources frontmatter' (all three evals) grades the frontmatter key set; eval 1 'new source in note frontmatter with fetch date' and eval 2 'model card in frontmatter sources' grade the sources entry. The body structure ('what it is, the claims graded, what it means here, what is open') is graded by NOTHING. The status enum is graded by nothing, and the disputed value is ambiguous between step 4 and step 2 (I12). 'Date what will move' is graded indirectly by 'both sources dated' / 'updated with date'.",
      "related_findings": ["I12", "I13", "I18", "C3"]
    },
    {
      "step": 5,
      "text": "Cascade: every neighbour gets one sentence, then the related: entry.",
      "ends_in_something_checkable": "yes - the neighbour's file either gains a sentence naming the page or it does not",
      "graded_by": "EFFECTIVELY NOTHING. The single check, eval 1 'check.py T1: neighbour names owner back', is already true of the untouched fixture (prompt-caching.md names [[model-prices]] in body and frontmatter before the run), so it passes without the agent cascading. Eval 2 has no cascade check at all, although local-models.md carries related: [] and gains a disputed fact. Eval 3 correctly has none. The 'one sentence, not just an edge' requirement - the thing rationale.md argues hardest for - is graded by nothing. evals.md S4 is the scenario that would grade it and it has no executable eval.",
      "related_findings": ["C6"]
    },
    {
      "step": 6,
      "text": "Register: INDEX row for a new page, source-log row, operation-log line.",
      "ends_in_something_checkable": "yes",
      "graded_by": "PARTIALLY: source-log row graded in all three evals ('check.py T1/T2: SOURCES row', 'T3: SOURCES row for the consulted source'); operation-log line graded in all three ('T1/T2: LOG row', 'T3: LOG says no material'). The INDEX-row-for-a-new-page clause is graded by NOTHING - no eval creates a page, and 'every note is listed in INDEX.md' is pre-satisfied by the fixture. The required content of the log line is specified three incompatible ways (C4), and the fixture's own example line does not meet it (I20).",
      "related_findings": ["C4", "C6", "I20", "I22"]
    },
    {
      "step": 7,
      "text": "Lint, then rebuild the search index; fix what the lint names before committing; fact and lint pass in one commit; hand-check fallback if no lint script.",
      "ends_in_something_checkable": "the lint result is checkable; 'rebuild the search index' and 'one commit' are checkable in a repo but not in this eval environment",
      "graded_by": "PARTIALLY and by proxy only: 'no dangling [[link]]' and 'every note is listed in INDEX.md' (all three evals) stand in for the lint - they have real bite only against an agent that breaks something, since the fixture starts clean. 'rebuild the search index' is graded by NOTHING and is unperformable (no index exists in the fixture). 'The fact and its lint pass land in one commit' is graded by NOTHING - no eval prompt commits. The 'no lint script? hand-check and say so in the log line' fallback is the branch that actually applies to this fixture, and it is graded by NOTHING; worse, eval 3's expected LOG content leaves no room for it.",
      "related_findings": ["C1", "C7", "I9", "I15"]
    }
  ],

  "summary": {
    "steps_ending_in_something_checkable": "7 of 7 in principle; 0 of 7 fully graded",
    "steps_graded_by_nothing_at_all": [1, 5],
    "steps_graded_only_in_part": [2, 3, 4, 6, 7],
    "rules_graded_by_nothing": ["Raw never edited / never the only copy", "null vs 0", "installs, fetches and runs nothing"],
    "rules_contradicted_by_a_step": ["installs, fetches and runs nothing (steps 2 and 7, and the In this repo section)"],
    "checks_that_cannot_run": "21 of 30 expectations name check.py, which is not in the bundle",
    "checks_that_pass_without_the_agent_acting": ["check.py T1: neighbour names owner back", "every note is listed in INDEX.md (x3)"],
    "checks_that_appear_inverted": ["check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']"],
    "named_files_missing_from_the_bundle": ["check.py", "raw/MANIFEST.md", "a lint script or search index inside evals/files/wiki"]
  }
}
```

Two things worth pulling out of the JSON, because they change what the eval numbers mean rather than just tidying the text:

- **`check.py` does not exist**, yet `evals.md` reports the build as run with a "code grader, blinded". 21 of 30 expectations resolve to nothing on disk. Every per-step grade in the artefact rests on it.
- **`check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']`** asserts the *old* row. The raw prices Beta 5 at $2/$10; the fixture holds $3/$15. That check passes on a wiki nobody touched and fails a correct update.

The rewrite also left a seam at the halving: rules 1, 2 and 4 survived into the body while their justifications did not follow them into `references/rationale.md`, and the reference asserts the opposite — "a rule with nothing behind it does not belong in the body."