I read every file in the bundle and swept each pair (step↔rule, step↔step, step↔eval expectation, description↔body, bundled files↔bill of materials). Findings below.

```json
{
  "artefact": "./artifact-C (skill: llm-wiki-ingest)",
  "examined": {
    "files_read_in_full": [
      "SKILL.md (68 lines: frontmatter description, When to use, 7 numbered steps, 3 rules, In this repo)",
      "references/rationale.md (43 lines)",
      "evals.md (52 lines: header verdict, Method, S1-S6, Not executed, Failure triage)",
      "evals/evals.json (63 lines: 3 evals, ids 1-3, with prompt/expected_output/files/expectations)",
      "evals/files/check.py (63 lines: common checks + T1/T2/T3 branches)",
      "evals/files/raw/2026-09-02-pricing-page.md",
      "evals/files/raw/2026-09-02-gamma-model-card.md",
      "evals/files/raw/2026-09-02-blog-restating-caching.md",
      "evals/files/wiki/INDEX.md, LOG.md, SOURCES.md",
      "evals/files/wiki/notes/model-prices.md, prompt-caching.md, local-models.md"
    ],
    "pairs_swept": {
      "step_vs_rule": "7 steps x 3 rules = 21 pairs",
      "step_vs_step": "21 ordered pairs",
      "step_vs_check": "7 steps x 24 check.py checks + 23 evals.json expectations",
      "step_vs_eval_md_criterion": "7 steps x 6 scenarios (S1-S6)",
      "description_vs_body": "each description clause (trigger list, pipeline nouns, NOT-list) against When-to-use, Steps, Rules",
      "eval_md_vs_evals_json_vs_check_py": "S1<->id1<->T1, S2<->id2<->T2, S5<->id3<->T3; S3/S4/S6 have no implementation",
      "fixture_vs_body": "3 raw files and 6 wiki files against step 1 (raw shape), step 4 (page schema), step 5 (cascade), step 6 (registers)",
      "bill_of_materials": "every path named in SKILL.md, evals.md, evals.json, check.py checked for presence in the bundle"
    },
    "not_examinable": "how the artefact was written, prior review rounds, the host repo's kb.py/lint (named but not bundled)"
  },

  "findings": [
    {
      "id": "F1",
      "level": "CLASS",
      "where": "evals/files/check.py T3 branch (lines 50-57) vs evals/evals.json id 3 prompt",
      "finding": "The T3 'byte-identical to the fixture' check is a tautology. The 'fixture' path resolves to check.py's own sibling directory - the very wiki the eval instructs the model to edit in place. `before` is hashed from the same file `after` is hashed from, so the check passes whatever the run did. The only scenario in the whole artefact recorded as a measured win over baseline is graded by a check that cannot fail.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\"\n        before = hashlib.sha256((fixture / f\"{stem}.md\").read_bytes()).hexdigest() if (fixture / f\"{stem}.md\").exists() else None\n        after = hashlib.sha256(notes.get(stem, \"\").encode(\"utf-8\")).hexdigest()\n        check(f\"{stem} byte-identical to the fixture\", before == after)   ||   \"prompt\": \"The wiki at evals/files/wiki ... Edit the wiki in place and list the files you changed.\""
    },
    {
      "id": "F2",
      "level": "CLASS",
      "where": "check.py common block + T1, against every fixture note",
      "finding": "A family of checks is already satisfied by the starting state, so they grade nothing about the run: `schema:{stem}` (all three fixture notes already carry title/status/tags/related/sources), `index:{stem}` (all three already listed in INDEX.md), and `neighbour names owner back` (prompt-caching.md already contains [[model-prices]] before any edit). A run that performed step 5 and a run that skipped it produce the same verdict.",
      "quote": "check(f\"index:{stem}\", f\"[[{stem}]]\" in index, \"not in INDEX\")   ||   check(\"neighbour names owner back\", \"[[model-prices]]\" in notes.get(\"prompt-caching\",\"\"))   ||   fixture prompt-caching.md: \"Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\""
    },
    {
      "id": "F3",
      "level": "INSTANCE",
      "where": "SKILL.md rule 3 (lines 56-57) vs step 7 (lines 49-51)",
      "finding": "Rule contradicts step. The rule closes the command surface to exactly three wiki commands; step 7 requires a git commit, which is none of them. Under the rule as written, step 7's terminating action is forbidden.",
      "quote": "\"This skill installs nothing and fetches no external code. It runs the wiki's own query, lint and index commands, and nothing else.\"   vs   \"fix what the lint names before committing. The fact and its lint pass land in one commit.\""
    },
    {
      "id": "F4",
      "level": "INSTANCE",
      "where": "SKILL.md rule 2 (line 55) vs rule 3 (lines 56-57)",
      "finding": "Rule contradicts rule. 'Look it up' requires a fetch or lookup action; the next rule permits only the wiki's own query, lint and index commands 'and nothing else'. Nothing in the body reconciles the two.",
      "quote": "\"Nothing about a tool, price, version or limit from memory: look it up and date it.\"   vs   \"It runs the wiki's own query, lint and index commands, and nothing else.\""
    },
    {
      "id": "F5",
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (lines 28-34) vs step 3 (lines 35-38)",
      "finding": "Step ordering contradicts step dependency. Step 2 must decide 'no claim, no value, no newer date for any page' and whether 'the source contradicts a claim a page holds' - both determinable only after step 3 has located and graded every number, date and quote. The step that carries the artefact's only measured win depends on the output of the step that follows it.",
      "quote": "\"2. **Search, then triage into exactly one.** ... **no material** - no claim, no value, no newer date for any page\"   vs   \"3. **Locate every number, date and quote in the raw before writing it,** and grade it\""
    },
    {
      "id": "F6",
      "level": "INSTANCE",
      "where": "SKILL.md step 1 (lines 23-27) vs the bundled raw fixtures",
      "finding": "Step contradicts the bundled files. Step 1 forbids provenance inside the immutable file and puts it in a directory manifest; all three bundled raw files carry `source:` and `fetched:` inside the file, and the bundle contains no manifest and no raw/ directory inside the eval wiki at all.",
      "quote": "\"provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file\"   vs   evals/files/raw/2026-09-02-pricing-page.md line 1-2: \"source: https://example.test/pricing-2026-09\\nfetched: 2026-09-02\""
    },
    {
      "id": "F7",
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (lines 39-43) vs the bundled wiki notes",
      "finding": "Step contradicts the bundled files. Step 4 mandates a body of 'what it is; a ## Claims table ...; what it means here; what is open'. None of the three fixture notes has a Claims table or any of those sections, and check.py's only schema check looks at frontmatter, so the non-conforming fixtures pass. Step 4's body schema is asserted by the skill and contradicted by the artefact's own example wiki.",
      "quote": "\"Body: what it is; a `## Claims` table with one row per claim - claim | source | locator | verbatim quote | verdict; what it means here; what is open.\"   vs   notes/local-models.md in full body: \"# Local models\\n\\nGamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit.\""
    },
    {
      "id": "F8",
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expectation 3 and check.py `beta_old`, vs SKILL.md step 2 'update' branch",
      "finding": "An eval check grades a behaviour no step requires. Both the expectation and the code demand the superseded price be retained as a dated row. SKILL.md's update branch says only 'extend it, never a rival' - retaining superseded values is specified only for the *disputed* branch. A model following the body exactly may replace the Beta 5 row and fail a check with no rule behind it.",
      "quote": "\"the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row\"   and   check(\"old price kept as a dated superseded row (Beta 5, $3, $15, 2026-08-20 on one line)\", bool(beta_old))   vs   \"**update** - a page owns it: extend it, never a rival.\""
    },
    {
      "id": "F9",
      "level": "INSTANCE",
      "where": "evals.md Method (line 6) vs the bundled grader and vs S6 (lines 43-46)",
      "finding": "The Method section contradicts itself and the bundle three ways: (a) it names a grader that is not in the bill of materials - `knowledge/kb.py` is a host-repo path, while the bundled grader is evals/files/check.py; (b) it adds 'by reading the note', a judgement, while check.py declares itself judgement-free; (c) it claims the criterion for *every* scenario is file state, but S6's criterion is a routing fact about which skill fires, which leaves no file state at all.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\"   vs   check.py: \"Every check is a fact about the files; no judgement.\"   vs   S6: \"**Pass criterion:** this talent does not fire; `skill-knowledge` does\""
    },
    {
      "id": "F10",
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion (line 12) vs evals.json id 1 expectation 4 and check.py claim_rows",
      "finding": "The written pass criterion is stricter than the implemented check on three counts, and two of the three are ungraded entirely. It demands the MEASURED verdict specifically, but the implementation accepts any of the three verdict words; it demands 'lint reports 0 errors', but no lint is run anywhere in the bundle; it demands 'INDEX unchanged', but the only INDEX check asserts presence, so an added row cannot fail.",
      "quote": "\"the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row.\"   vs   re.search(r\"MEASURED|REPEATED|DERIVED\", l)   and   \"a claims-table row carries the verbatim raw line and a verdict word\""
    },
    {
      "id": "F11",
      "level": "INSTANCE",
      "where": "evals.md S5 input (line 38) vs references/rationale.md (lines 38-41) vs the bundled blog fixture",
      "finding": "The same scenario is described with three different fact counts and two different source claims. The blog fixture states exactly two multipliers, rationale.md says two, evals.md says three. evals.md also says 'with the same sources', but the blog's URL (/blog/caching-explained) is not the note's source (/caching).",
      "quote": "S5: \"a blog post restating three facts the wiki already holds with the same sources.\"   vs   rationale.md: \"a blog post restates two multipliers a note already carries with a dated source\"   vs   fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\""
    },
    {
      "id": "F12",
      "level": "INSTANCE",
      "where": "evals.md S1 input (line 11) vs the bundled pricing fixture",
      "finding": "The scenario miscounts its own fixture. The pricing page carries four per-MTok prices (Alpha 5 input and output, Beta 5 input and output), not three.",
      "quote": "\"a fetched vendor pricing page with three per-MTok prices\"   vs   fixture: \"Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens.\\nBeta 5: $2.00 per million input tokens, $10.00 per million output tokens.\""
    },
    {
      "id": "F13",
      "level": "INSTANCE",
      "where": "evals.md S4 'With talent' (line 34) vs SKILL.md step 5 (lines 44-45)",
      "finding": "The eval will pass a behaviour the body forbids. S4 accepts an explicit deferral - committing with one-way links and explaining them - as a passing outcome. Step 5 states the cascade unconditionally and offers no deferral branch anywhere in the body.",
      "quote": "S4: \"each neighbour gains a sentence naming the new page back before the commit, or the commit message states which neighbours were left one-way and why\" / \"**With talent:** step 5 or an explicit deferral in the log.\"   vs   step 5: \"Every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. No true sentence, no edge.\""
    },
    {
      "id": "F14",
      "level": "INSTANCE",
      "where": "evals.md Method (line 6) vs S5 label and result (lines 37, 41)",
      "finding": "The document's own grading vocabulary is violated by the scenario it rests on. Method reserves 'PASS. Beats baseline.' for scenarios where the baseline plausibly fails; S5 is labelled normal and carries that verdict, while S2, labelled trap, records no delta.",
      "quote": "\"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\"   vs   \"### S5 — no material · normal\" ... \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "id": "F15",
      "level": "INSTANCE",
      "where": "references/rationale.md (lines 16-18) vs evals.md S5 (lines 37, 41)",
      "finding": "The same measurement is reported with two denominators. rationale.md cites the probe arm only and generalises it to 'every baseline run', while evals.md aggregates five baseline runs across three arms.",
      "quote": "rationale.md: \"every baseline run (2 of 2) still edited the owning page\"   vs   evals.md: \"without 0/1, probe 0/2, incumbent 0/2\" / \"0/5 baseline runs vs 2/2 with\""
    },
    {
      "id": "F16",
      "level": "INSTANCE",
      "where": "SKILL.md step 7 fallback (lines 50-51) vs the eval wiki fixture and every LOG check",
      "finding": "The branch that actually applies in the eval wiki is graded by nothing. The fixture wiki ships no lint script, so step 7's fallback governs - the log line must say the hand checks were done. No expectation in evals.json and no check in check.py looks for it, in any of the three tasks.",
      "quote": "\"No lint script in this wiki? Check dangling links, unlisted pages and orphans by hand and say so in the log line.\"   vs   check(\"LOG line names the source and the disposition\", \"pricing-2026-09\" in log and re.search(r\"update\", log, re.I) is not None)"
    },
    {
      "id": "F17",
      "level": "INSTANCE",
      "where": "SKILL.md step 6 (lines 46-48) vs all three LOG checks in check.py",
      "finding": "Step 6 requires three components in the operation-log line; the graders check two. 'The pages touched' is required in every branch and asserted by no check and no expectation.",
      "quote": "\"one operation-log line naming the disposition, the source URL and the pages touched, in every branch.\"   vs   \"LOG.md has a line naming the source and 'update'\" (evals.json id 1, and the parallel expectations in ids 2 and 3)"
    },
    {
      "id": "F18",
      "level": "INSTANCE",
      "where": "check.py T1 'no rival page' (line 26) vs the expectation it implements",
      "finding": "The check does not grade its stated expectation. It only rejects a new note whose filename stem contains the substring 'pric'; a rival page named beta-5-2026-09 or new-prices-note satisfies the check while violating the expectation.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))   vs   \"model-prices is the page updated; no rival page\""
    },
    {
      "id": "F19",
      "level": "INSTANCE",
      "where": "SKILL.md 'When to use' (line 15) vs step 1 (lines 23-27)",
      "finding": "A declared trigger has no path through step 1. A compiled summary page written back has no fetched source bytes and no fetch date, yet step 1 is stated unconditionally as the first thing every run does, and no branch in the body handles the case.",
      "quote": "\"An existing page gains a source, or a compiled summary page is written back.\"   vs   \"1. **Keep the raw.** Save the source bytes where the wiki can re-read them, never edited, with URL or path and fetch date.\""
    },
    {
      "id": "F20",
      "level": "INSTANCE",
      "where": "frontmatter description (line 3) vs SKILL.md step 2 no-material branch (lines 32-34)",
      "finding": "The description frames every invocation as a source becoming a note; the branch the artefact records as its only measured win is precisely the one where no note is written and no page is touched. The description's own clause list names the triage but the framing sentence contradicts its outcome.",
      "quote": "\"Use when a fetched page, paper, repo, transcript or measurement is about to become a note in an LLM-maintained wiki\"   vs   \"**no material** - ... keep the raw, write the source-log row and the operation-log line, touch no page, stop.\""
    },
    {
      "id": "F21",
      "level": "INSTANCE",
      "where": "evals/evals.json id 3 expected_output vs its own expectations list",
      "finding": "Within one eval entry, the expected output omits a state change the expectations require. expected_output says no page changed and names only the LOG line; expectation 4 requires SOURCES.md to gain a row, which check.py enforces.",
      "quote": "\"expected_output\": \"No page changed and no page created; one LOG line saying no material with the source URL.\"   vs   \"SOURCES.md has a row for the blog\""
    },
    {
      "id": "F22",
      "level": "INSTANCE",
      "where": "evals/evals.json vs evals/files/check.py usage",
      "finding": "The grader is unreachable from the eval spec. check.py requires a task argument T1|T2|T3; evals.json's ids are 1, 2, 3, it lists check.py as an input file but never instructs the runner to invoke it, and the id-to-task mapping exists only in evals.md's scenario headings.",
      "quote": "check.py: \"Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>\"   vs   evals.json id 1: \"files\": [\"evals/files/wiki\", \"evals/files/raw/2026-09-02-pricing-page.md\", \"evals/files/check.py\"]"
    },
    {
      "id": "F23",
      "level": "INSTANCE",
      "where": "evals.md (lines 3, 49, 52) - bill of materials",
      "finding": "Four artefacts are cited as evidence or as procedure and none is in the bundle: the build directory, the trigger matrix carrying S6's entire claim, the lessons file the failure-triage procedure writes to, and knowledge/kb.py. S6's pass criterion is therefore backed only by numbers no bundled file contains.",
      "quote": "\"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4).\"   and   \"test-bug → fix the test and record it in `pipeline/CURATION-LESSONS.md`\"   and   \"(`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule)\""
    },
    {
      "id": "F24",
      "level": "CLASS",
      "where": "SKILL.md step 3 and step 4 vs every claim-row check",
      "finding": "Universals in the body are graded by existentials in the checks. Step 3 says every number, date and quote; T1 passes on one claims row and ignores Alpha 5's two prices and both caching multipliers. Step 4 mandates a five-column claims row (claim, source, locator, verbatim quote, verdict); the checks read only the quote and the verdict from a single line, so 'locator' and 'source' are graded nowhere. The DERIVED verdict has no fixture at all - no bundled raw contains a computed figure.",
      "quote": "\"Locate every number, date and quote in the raw before writing it,\"   vs   claim_rows = [l for l in mp.splitlines() if l.strip().startswith(\"|\") and re.search(r\"MEASURED|REPEATED|DERIVED\", l) and (\"$2.00 per million input tokens\" in l or \"$10.00 per million output tokens\" in l)]"
    },
    {
      "id": "F25",
      "level": "CLASS",
      "where": "SKILL.md steps 2 (new branch), 4, 6 (index row) vs all three eval scenarios",
      "finding": "No eval exercises the 'new' triage branch. All three tasks are update, disputed and no-material, so writing a page from scratch in the schema (step 4) and adding the hand-written map-of-contents row for a new page (step 6) are never executed. The one part of step 4 that runs - the frontmatter schema check - runs only against fixture notes that already comply.",
      "quote": "\"**new** - no page owns the topic.\"   and   \"6. **Register.** A row in the hand-written map of contents for a new page\"   vs   evals.json prompts, which are Ingest ... pricing-page (update), gamma-model-card (disputed), blog-restating-caching (no material)"
    },
    {
      "id": "F26",
      "level": "INSTANCE",
      "where": "SKILL.md rule 1 (line 54) vs the eval layout",
      "finding": "A rule is structurally ungradeable in this bundle. check.py reads only the wiki directory passed as argv[1]; the raw files live outside it, in evals/files/raw/. An edited or deleted raw file cannot be detected by any check in any task.",
      "quote": "\"The raw is never edited; the wiki is never the only copy of a fact.\"   vs   wiki = pathlib.Path(sys.argv[1]); task = sys.argv[2]"
    },
    {
      "id": "F27",
      "level": "INSTANCE",
      "where": "SKILL.md rule 1, second clause",
      "finding": "The clause states an outcome with no procedure and no check anywhere in the artefact. Nothing in steps 1-7 says what action makes the wiki not the only copy, and rationale.md's raw-kept entry argues re-derivability rather than a second copy.",
      "quote": "\"the wiki is never the only copy of a fact.\""
    },
    {
      "id": "F28",
      "level": "INSTANCE",
      "where": "evals.md header (line 3) vs S4 status (line 35) and line 49",
      "finding": "The type declaration asserts a component with no executable eval. The single discipline-pressure scenario is S4, whose result is pending and which line 49 lists among those with no executable eval.",
      "quote": "\"**Type:** technique (with one discipline pressure)\"   vs   \"### S4 — the cascade under time pressure · pressure\" ... \"**Result:** pending\"   and   \"S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet\""
    },
    {
      "id": "F29",
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion (line 26) vs check.py's output vocabulary",
      "finding": "S3's criterion is unsatisfiable by the artefact's own grading machinery even once implemented: it requires a severity distinction between INFO and ERROR, and check.py emits only PASS and FAIL with no severity axis.",
      "quote": "\"lint reports the note-only source as INFO, not ERROR\"   vs   print(f\"{'PASS' if ok else 'FAIL'} {name} {detail if not ok else ''}\")"
    }
  ],

  "step_matrix": [
    {
      "step": 1,
      "name": "Keep the raw",
      "ends_in_something_checkable": "PARTLY — a saved raw file with a dated filename is checkable; the manifest row is checkable in principle but the bundle has no raw/ directory or manifest to check it in",
      "graded_by": "NOTHING. No check in check.py touches the raw path, and no expectation in evals.json mentions it. See F1's scope note, F6, F26.",
      "notes": "The raw exists in the fixture before the run, so even a check for its presence would be pre-satisfied."
    },
    {
      "step": 2,
      "name": "Search, then triage into exactly one",
      "ends_in_something_checkable": "SEARCH HALF: NO — the body never requires the search or its result to be recorded anywhere. TRIAGE HALF: YES — the disposition surfaces in the log line and the resulting file state",
      "graded_by": "T1 check 'LOG line names the source and the disposition' (/update/) + 'no rival page' (weakly, F18); T2 checks 'both values present', 'disputed marker on a row', 'page status disputed', 'LOG line names the card and the disposition'; T3 checks 'LOG says no material and names the source' + 'no new note' (the byte-identical checks are tautological, F1). The 'new' branch is graded by nothing (F25).",
      "notes": "Also depends on step 3's output despite preceding it (F5)."
    },
    {
      "step": 3,
      "name": "Locate every number, date and quote, and grade it",
      "ends_in_something_checkable": "YES — claim rows with a quote and a verdict word",
      "graded_by": "T1 'a claims-table row carries the verbatim raw quote AND a verdict word on the same line'; T2 'a claims row carries 753B, the card's verbatim line and a verdict word' and 'a claims row carries 744B and a verdict word'.",
      "notes": "Graded existentially, not universally (F24). MEASURED is demanded by evals.md S1 but not by any check (F10). DERIVED has no fixture."
    },
    {
      "step": 4,
      "name": "Write the page in the schema",
      "ends_in_something_checkable": "YES for frontmatter and claim rows; NO as written for the body sections ('what it means here', 'what is open' have no observable form specified)",
      "graded_by": "Frontmatter: common check 'schema:{stem}' — but vacuously, since the fixtures already comply and no eval writes a new page (F2, F25). Claims columns: partially, via the step-3 checks; 'locator' and 'source' columns graded by nothing (F24). As-of dates: partially, via T1's date-bearing row checks and T2 'both sources dated'. Body sections: NOTHING.",
      "notes": "Contradicted by the bundled notes, which carry none of the mandated body sections (F7)."
    },
    {
      "step": 5,
      "name": "Cascade",
      "ends_in_something_checkable": "YES in principle — a sentence in the neighbour plus a related: entry",
      "graded_by": "Only T1 'neighbour names owner back', which is pre-satisfied by the fixture and therefore grades nothing (F2). The 'one sentence saying why it matters' is graded by NOTHING in any task.",
      "notes": "Additionally contradicted by S4, which accepts deferral (F13)."
    },
    {
      "step": 6,
      "name": "Register",
      "ends_in_something_checkable": "YES — three rows in three named files",
      "graded_by": "Source-log row: GRADED in all three tasks ('SOURCES row' / 'SOURCES row for the consulted source'). Operation-log line: PARTLY — disposition and source URL graded in all three; 'the pages touched' graded by NOTHING (F17). Map-of-contents row for a new page: NOTHING (F25); the 'index:{stem}' check tests pre-existing entries only.",
      "notes": "This is the best-graded step in the artefact."
    },
    {
      "step": 7,
      "name": "Lint, then rebuild the search index",
      "ends_in_something_checkable": "YES in a real wiki — a lint exit status, a rebuilt index, a commit",
      "graded_by": "NOTHING. No lint is run by check.py; no check inspects a rebuilt index; no eval commits anything (the prompts say 'Edit the wiki in place'). The three common checks (schema, dangling links, index membership) approximate lint conditions but never verify a lint was run, and two of the three are vacuous. The fallback branch that actually applies here — say so in the log line — is graded by nothing (F16).",
      "notes": "Also contradicted by rule 3, which forbids the commit this step requires (F3)."
    }
  ],

  "rules_matrix": [
    { "rule": "The raw is never edited", "graded_by": "NOTHING — the raw lies outside the directory check.py reads (F26)" },
    { "rule": "The wiki is never the only copy of a fact", "graded_by": "NOTHING — no procedure and no check (F27)" },
    { "rule": "Nothing about a tool, price, version or limit from memory: look it up and date it", "graded_by": "INDIRECTLY ONLY — the verbatim-quote checks in T1/T2 would fail a fabricated line, but nothing grades the dating of every such value; contradicted by rule 3 (F4)" },
    { "rule": "Installs nothing, fetches no external code, runs only the wiki's query/lint/index commands", "graded_by": "NOTHING — no check inspects the commands run; contradicted by step 7 (F3) and rule 2 (F4)" }
  ],

  "summary": {
    "total_findings": 29,
    "class_level": 5,
    "instance_level": 24,
    "steps_ending_in_nothing_checkable": [2],
    "steps_graded_by_nothing": [1, 7],
    "steps_graded_only_vacuously": [4, 5],
    "steps_graded_partially": [2, 3, 6],
    "most_load_bearing": "F1 — the one scenario the artefact reports as a measured win over baseline (S5/T3, the rule step 2 was rewritten for) is graded by a hash comparison of each file against itself, which cannot fail."
  }
}
```

**What this comes to:** the artefact grades its registration step well and almost nothing else. Two of seven steps (keep the raw, lint/rebuild/commit) have no check at all, two more (write the page, cascade) are graded only by checks the fixture already satisfies before the run starts, and the single check backing the artefact's only claimed win is a tautology. On top of that, the three rules sit in direct conflict with step 7 and with each other, and evals.md's Method section disagrees with the bundled grader on what the grader even is.