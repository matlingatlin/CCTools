Two notes on the brief before the findings: the directory is `./artifact-A`, not `./artifact`, and there is **no `references/` directory** — the artefact never claims one, so that's a mismatch in the brief rather than a missing bundled file. The one file it *does* claim and lack is `evals/files/check.py`.

```json
{
  "artefact": "artifact-A (llm-wiki-ingest)",

  "examined": {
    "files_read_in_full": [
      "artifact-A/SKILL.md (93 lines: frontmatter, When to use, When NOT to use, Steps 1-7, Example, Rules, In this repo)",
      "artifact-A/evals.md (49 lines: header, Method, S1-S6, Failure triage)",
      "artifact-A/evals/evals.json (3 eval entries)",
      "artifact-A/evals/files/raw/2026-09-02-pricing-page.md",
      "artifact-A/evals/files/raw/2026-09-02-gamma-model-card.md",
      "artifact-A/evals/files/raw/2026-09-02-blog-restating-caching.md",
      "artifact-A/evals/files/wiki/INDEX.md",
      "artifact-A/evals/files/wiki/LOG.md",
      "artifact-A/evals/files/wiki/SOURCES.md",
      "artifact-A/evals/files/wiki/notes/model-prices.md",
      "artifact-A/evals/files/wiki/notes/prompt-caching.md",
      "artifact-A/evals/files/wiki/notes/local-models.md"
    ],
    "pair_classes_swept": [
      "step x rule (7 steps x 5 rules = 35 pairs)",
      "step x step (21 ordered pairs)",
      "step x eval expectation (7 steps x 6 prose scenarios + 3 json evals)",
      "description x body (each description clause traced to a step)",
      "When-to-use / When-NOT-to-use x steps",
      "Example x steps, Example x rules, Example x S1/S5",
      "evals.md scenario x evals.json entry (6 vs 3)",
      "evals.json `files` bill-of-materials x files actually present",
      "raw fixture content x eval expected_output x scenario pass criterion",
      "wiki fixture schema x step 3 claim-row fields x step 4 frontmatter schema",
      "'In this repo' paths x the real repository (all 10 resolve)"
    ],
    "bill_of_materials_check": "12 files present. 1 file named by the artefact and absent: evals/files/check.py, listed in the `files` array of all three evals.json entries. `find` over the artefact returns zero .py files. No references/ directory exists and none is claimed."
  },

  "findings": [
    {
      "id": "F1",
      "level": "CLASS",
      "where": "SKILL.md Rules (l.83) vs Steps 2 and 7 (l.35, l.61-62) vs 'In this repo' (l.89-91) vs evals.md Method (l.6)",
      "finding": "The closing rule forbids running external code, while two numbered steps, the repo instance section and the eval grading method all require running a script. Every step-7 completion and the entire eval oracle violate the rule as written.",
      "quote": "- This skill never installs, fetches or runs external code; it is a writing discipline.\n7. **Lint, then rebuild the index.** Run the wiki's deterministic lint\nQuery with `python3 knowledge/kb.py find \"<terms>\"` and `read \"<heading>\"`\nlint with `python3 knowledge/kb.py lint` (exit 1 on errors) and rebuild with `kb.py build`\nchecked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "id": "F2",
      "level": "CLASS",
      "where": "SKILL.md step 3 (l.48-51) vs SKILL.md Example (l.69) vs evals.md S1 pass criterion (l.12)",
      "finding": "Step 3 defines MEASURED as requiring a dependent variable, an effect and a sample. A vendor pricing page announcing a price has none of the three, so by step 3's own definition it is REPEATED. Both the Example and S1's pass criterion nevertheless grade exactly that pricing page MEASURED. The rule that defines the verdict and the two places that apply it disagree, so a run graded against S1 is rewarded for breaking step 3.",
      "quote": "a verdict -\n   **MEASURED** (the source measured it: dependent variable, effect, sample), **REPEATED**\n   (asserted, no measurement found)\nthe note gets a dated row with the verbatim line and MEASURED\nthe owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "id": "F3",
      "level": "CLASS",
      "where": "SKILL.md step 2 (l.36-37) vs the eval-1 fixture (raw/2026-09-02-pricing-page.md l.7) vs the wiki fixture (notes/prompt-caching.md l.13)",
      "finding": "Step 2 requires exactly one triage label per source, but the eval-1 source triages differently per page: its Beta 5 prices are an 'update' to model-prices while its cache multipliers ('10%' / '125%') restate values prompt-caching already holds, which is 'no material'. A source touching two pages with two verdicts has no defined handling, and no step, expectation or check says whether prompt-caching may be touched.",
      "quote": "Triage into exactly one of: **new** (no page owns the topic),\n   **update** ..., **disputed** ..., **no material**\nCache reads are billed at 10% of the input price; cache writes at 125%.\nCache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x."
    },
    {
      "id": "F4",
      "level": "CLASS",
      "where": "artifact-A/evals.md S1-S6 vs artifact-A/evals/evals.json",
      "finding": "evals.md declares six scenarios; evals.json implements three (S1, S2, S5). S3 (edge, raw-less transcript), S4 (pressure, cascade) and S6 (negative trigger) have no runnable entry and no fixture — there is no video-transcript raw file and no negative-trigger prompt. Consequently step 5 (cascade), the REPEATED half of step 3, and the whole no-fire boundary in the description are graded only by prose that cannot execute.",
      "quote": "### S3 — a video transcript with no retrievable URL · edge\n### S4 — the cascade under time pressure · pressure\n### S6 — a claim to bundle into a skill · negative-trigger\n \"skill_name\": \"llm-wiki-ingest\",\n \"evals\": [\n  {\n   \"id\": 1,"
    },
    {
      "id": "F5",
      "level": "INSTANCE",
      "where": "artifact-A/evals/evals.json, `files` array of evals 1, 2 and 3 vs the bundle",
      "finding": "All three evals declare evals/files/check.py in their bill of materials. No such file exists; the artefact contains no .py file at all. The only named programmatic grader in the suite is missing, so nothing mechanical grades any eval.",
      "quote": "   \"files\": [\n    \"evals/files/wiki\",\n    \"evals/files/raw/2026-09-02-pricing-page.md\",\n    \"evals/files/check.py\"\n   ],"
    },
    {
      "id": "F6",
      "level": "CLASS",
      "where": "artifact-A/evals/evals.json, evals 1, 2 and 3",
      "finding": "Every eval's `expectations` array is empty. Combined with the missing check.py, the suite carries zero machine-checkable assertions — grading rests entirely on the prose `expected_output`, which no component in the artefact consumes.",
      "quote": "   \"expectations\": []"
    },
    {
      "id": "F7",
      "level": "INSTANCE",
      "where": "evals.md Method (l.6) vs evals.json prompts (l.6, 17, 28)",
      "finding": "The Method names the grader as a lint over `knowledge/`, but every eval prompt operates on the fixture wiki at evals/files/wiki, and no kb.py is bundled. The stated observable criterion for every scenario cannot be produced for any scenario. S1, S2, S3 and S4 pass criteria all depend on this lint's output.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\nThe wiki at evals/files/wiki has notes/, INDEX.md, SOURCES.md and LOG.md."
    },
    {
      "id": "F8",
      "level": "CLASS",
      "where": "SKILL.md step 6 (l.59-60) vs step 2 update branch (l.36-37) vs evals.md S1 (l.12) vs SKILL.md Example (l.70-71)",
      "finding": "Step 6 requires an index row unconditionally, but step 2's 'update' branch extends an existing page that already has an index row, and S1 makes 'INDEX unchanged' a pass criterion. The Example sides with step 6 ('the index ... gain a row') for the same pricing-page case S1 covers. An update run cannot satisfy step 6 and S1 at once.",
      "quote": "6. **Register.** One row in the index (map of contents), one row per source in the source\n   log, one entry in the operation log\n**update** (a page owns it: extend that page, never a rival)\nno new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row.\nthe index and source log gain a row"
    },
    {
      "id": "F9",
      "level": "CLASS",
      "where": "SKILL.md step 2 no-material branch (l.40-42) vs step 6 (l.59-60)",
      "finding": "Step 2 halts the procedure after a single operation-log line for 'no material'; step 6 unconditionally demands three registrations including a source-log row. Step 2 also explicitly forbids the source row. The two steps give opposite instructions for the same run, and eval 3's expectation is silent on whether SOURCES may gain a row, so a run that adds one is neither clearly passing nor clearly failing.",
      "quote": "**No material means no page is touched**: keep the raw, write\n   one operation-log line with the URL and the reason, and stop. A corroborating source is\n   not added to the page's source list\nOne row in the index (map of contents), one row per source in the source\n   log, one entry in the operation log"
    },
    {
      "id": "F10",
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (l.41) vs SKILL.md Example (l.75-76) vs evals.md S5 (l.40) vs evals.json eval 3 (l.29)",
      "finding": "Four statements of what the no-material log line must contain, no two identical: URL + reason; URL + reason with no date; URL + date with no reason; URL only. A run cannot be graded because the required content is not fixed.",
      "quote": "one operation-log line with the URL and the reason, and stop.\nthe log says `no material: <url> restates\nprompt-caching's 0.1x / 1.25x, no new claim`\nan operation-log entry says \"no material\" with the URL and date.\nNo page changed and no page created; one LOG line saying no material with the source URL."
    },
    {
      "id": "F11",
      "level": "INSTANCE",
      "where": "evals.md S5 Input (l.38) vs the fixture raw/2026-09-02-blog-restating-caching.md vs SKILL.md Example (l.73-74)",
      "finding": "S5 describes a fixture that does not exist: it says three facts with the same sources; the bundled blog restates two multipliers and carries a different source URL (blog/caching-explained) from the note's source (example.test/caching). SKILL.md's own Example describes the same case correctly as two multipliers, so the scenario contradicts both the fixture and the body.",
      "quote": "- **Input:** a blog post restating three facts the wiki already holds with the same sources.\nCache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\na blog post restates two multipliers a note already\ncarries with a dated source."
    },
    {
      "id": "F12",
      "level": "CLASS",
      "where": "SKILL.md step 3 (l.48-49) vs step 4 (l.52-54) vs notes/model-prices.md (l.13-16) and notes/local-models.md (l.13)",
      "finding": "Step 3 specifies a five-field claim row (what it says, source, locator, verbatim line, verdict). Step 4's schema defines only frontmatter and four prose body sections — it provides no place for that row. Neither does any bundled note: model-prices' table has four columns and no source, locator, quote or verdict, and local-models states its claim as a sentence. The artefact's own schema and its own fixtures cannot hold the output step 3 mandates, so step 3 is unsatisfiable against the material shipped to test it.",
      "quote": "A claim is one row: what it says, source, locator, verbatim line, and a verdict\nBody: what it is, the claims\n   graded, what it means for this project, what is still open.\n| model | input | output | as of |\nGamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit."
    },
    {
      "id": "F13",
      "level": "INSTANCE",
      "where": "SKILL.md step 1 (l.29-34) vs step 4 (l.52-53) vs all three fixture notes' frontmatter",
      "finding": "Step 1 requires a content hash in the page's source entry. Step 4's frontmatter schema lists url-or-path, fetch date and note — no hash field. No fixture note carries a hash, and no expectation or pass criterion mentions one. The requirement has nowhere to be written and nothing that checks it.",
      "quote": "with provenance: URL or path, fetch date, and a\n   content hash or commit.\na content\n   hash in the page's source entry.\nFrontmatter with title, sources (url or path, fetch\n   date, note), status from the fixed vocabulary, tags, related."
    },
    {
      "id": "F14",
      "level": "CLASS",
      "where": "SKILL.md step 2 (l.35-43) vs step 3 (l.47-51)",
      "finding": "Ordering contradiction: step 2 assigns the triage label, and its 'no material' branch stops the run before step 3 ever executes. But deciding that a source 'adds no claim, no value and no newer date' requires having located and compared every number and date in the raw — which is step 3's work. Step 2 depends on an output produced by a step it precedes and can prevent from running.",
      "quote": "2. **Search before writing.** ... **no material** (the source adds no claim, no value and\n   no newer date to any page).\n3. **Locate every number, date and quote in the raw before it is written.**"
    },
    {
      "id": "F15",
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (l.53)",
      "finding": "Step 4 requires a status drawn from 'the fixed vocabulary', but no vocabulary is stated anywhere in the artefact. Two values appear incidentally — `verified` in all three fixtures and `disputed` in step 2 — with no statement that these are the whole set. The step cannot be checked because the legal values are never enumerated.",
      "quote": "status from the fixed vocabulary, tags, related."
    },
    {
      "id": "F16",
      "level": "CLASS",
      "where": "SKILL.md step 2 (l.39) vs evals.md S2 (l.19) vs evals.json eval 2 (l.18)",
      "finding": "Three incompatible granularities for the disputed mark: step 2 marks the page, S2 marks a line, eval 2 marks a fact. Step 4 treats status as page-level frontmatter, so a line-level or fact-level mark has no defined syntax anywhere in the artefact. A grader cannot tell what output passes.",
      "quote": "mark the page\n   `disputed` where it disagrees\nthe note marked disputed at that line\nthe note marked disputed at that fact"
    },
    {
      "id": "F17",
      "level": "CLASS",
      "where": "SKILL.md step 4 (l.53-55) vs all three fixture notes vs evals.json eval 1 (l.7)",
      "finding": "Step 4's four mandatory body sections appear in none of the three bundled notes, which the artefact presents as valid wiki pages. Eval 1 further expects an in-place row addition, not the restructuring step 4 would force on an updated page. The schema the step teaches and the schema the fixtures and expectations enforce are different schemas.",
      "quote": "Body: what it is, the claims\n   graded, what it means for this project, what is still open.\nThe owning note (model-prices) is updated in place: a dated row per changed price"
    },
    {
      "id": "F18",
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion (l.12) vs evals.json eval 1 expected_output (l.7)",
      "finding": "The two statements of what eval 1 must produce disagree in five places. S1 requires the verbatim line, the MEASURED verdict and INDEX unchanged, none of which eval 1 mentions; eval 1 requires a LOG line, the superseded price kept and the neighbour link, none of which S1 mentions. A run can pass either and fail the other.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row.\nThe owning note (model-prices) is updated in place: a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter; no new page; a SOURCES row and a LOG line; the neighbour still names the owner."
    },
    {
      "id": "F19",
      "level": "INSTANCE",
      "where": "SKILL.md step 5 (l.56-58) vs evals.json eval 1 (l.7) and the fixture notes' `related:` fields",
      "finding": "Step 5 is graded by nothing that can fail. Eval 1's only cascade clause checks that a link already present in the fixture is still present, which passes if the agent does nothing. model-prices and prompt-caching already name each other, and local-models (eval 2) names no neighbour at all, so no runnable eval ever presents a one-way link for step 5 to close. Only S4, which has no runnable entry, tests the step.",
      "quote": "5. **Cascade.** For every neighbour the page names, make the neighbour name it back with a\n   sentence that says *why*\nthe neighbour still names the owner.\nrelated: [\"[[prompt-caching]]\"]\nrelated: []"
    },
    {
      "id": "F20",
      "level": "INSTANCE",
      "where": "SKILL.md step 7 heading vs step 7 body (l.61-63)",
      "finding": "The step's title names two actions; the body describes only the first. Rebuilding the index is never explained, never given an observable outcome, and is checked by no scenario or expectation. It also duplicates step 6's hand-written index row with a generated one, with no statement of which wins.",
      "quote": "7. **Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling\n   links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names\n   before committing."
    },
    {
      "id": "F21",
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (l.62-63) vs evals.md S4 pass criterion (l.32)",
      "finding": "The commit is the terminal observable of the procedure and a graded object in S4, but no numbered step tells the operator to commit or what the message must contain. S4 can pass on a commit message that step 7 never asks anyone to write, and eval prompts instruct the agent to 'Edit the wiki in place and list the files you changed' — no commit occurs in any runnable eval at all.",
      "quote": "before committing. A verified fact and its lint pass land in the same commit.\nor the commit message states which neighbours were left one-way and why\nEdit the wiki in place and list the files you changed."
    },
    {
      "id": "F22",
      "level": "CLASS",
      "where": "SKILL.md 'When to use' second bullet (l.19-20) vs Steps 1-7 vs the whole eval suite",
      "finding": "The skill claims a second trigger — a compiled summary page written back from a query over several notes — that the procedure cannot serve. Step 1 presupposes source bytes with a URL and fetch date; a compiled page has no external source and no raw. No step covers it, no scenario tests it, and the description never mentions it either.",
      "quote": "- An existing note is being extended with a new source, or a compiled summary page is being\n  written back from a query over several notes."
    },
    {
      "id": "F23",
      "level": "INSTANCE",
      "where": "SKILL.md Rules (l.81)",
      "finding": "An orphan rule. No step, no schema field, no fixture and no expectation involves a null or zero value anywhere in the artefact; step 4's frontmatter has no field this could govern. The rule constrains nothing the procedure produces and is graded by nothing.",
      "quote": "- `null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "id": "F24",
      "level": "INSTANCE",
      "where": "SKILL.md Example (l.66-71) vs the wiki fixture vs evals.md S1",
      "finding": "The Example is internally inconsistent and inconsistent with its fixture. It describes an update to the existing owner, then has neighbours 'name the pricing note back' as though a new page had been created; it asserts two notes quote the old price when only prompt-caching does; and it has the index gain a row, which S1 forbids for this exact case.",
      "quote": "`find \"pricing\"` shows a note that owns\nmodel prices; the note gets a dated row with the verbatim line and MEASURED; the two notes\nthat quote the old price name the pricing note back with a sentence; the index and source\nlog gain a row"
    },
    {
      "id": "F25",
      "level": "INSTANCE",
      "where": "evals.json eval 2 expected_output (l.18) vs SKILL.md step 3 (l.47) vs raw/2026-09-02-gamma-model-card.md (l.5)",
      "finding": "Step 3 demands every number in the raw be located and written. The gamma model card carries two numbers beyond the disputed parameter count — 40B active parameters and a 1M-token context — and eval 2's expectation requires neither. An agent that captures only the dispute passes eval 2 while breaking step 3, so the eval cannot detect the step's most common failure mode.",
      "quote": "Total parameters: 753B. Active parameters: 40B. Context: 1M tokens.\nBoth parameter counts kept as their own dated rows with their sources, the note marked disputed at that fact, neither value overwritten; SOURCES and LOG rows."
    },
    {
      "id": "F26",
      "level": "INSTANCE",
      "where": "SKILL.md step 6 (l.59-60) vs 'In this repo' (l.90) vs the eval fixture wiki",
      "finding": "Step 6 names three registers — index, source log, operation log. The repo instance section maps them onto INDEX.md, SOURCES.md and pipeline/STATUS.md, but a status file is not an operation log, and no operation-log path is given for this repo. The eval fixture meanwhile ships LOG.md as the operation log, so the artefact's two instantiations of step 6 do not agree on where the third row goes.",
      "quote": "register in `knowledge/INDEX.md`, `knowledge/sources/SOURCES.md` and `pipeline/STATUS.md`;\nOne row in the index (map of contents), one row per source in the source\n   log, one entry in the operation log"
    },
    {
      "id": "F27",
      "level": "INSTANCE",
      "where": "evals.md S5 label (l.37) and Method (l.6) vs SKILL.md step 2 (l.44-46)",
      "finding": "S5 is classified 'normal', but step 2 records that the baseline fails this exact scenario every time. The Method reserves the beats-baseline verdict for scenarios where the baseline plausibly fails, so the artefact's own measurement disqualifies its own classification and the scenario is scored under the weaker rubric.",
      "quote": "### S5 — no material · normal\nObserved 2026-09-02: without this rule, every baseline run on a restating blog post still\n   edited the owning page (a second source plus a claims row), so \"no material\" quietly\n   became \"update\".\nPASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "id": "F28",
      "level": "INSTANCE",
      "where": "evals.md S3 (l.24-28), S5 (l.37-41), S6 (l.43-46) vs S1, S2, S4",
      "finding": "Schema drift inside the scenario list: S1, S2 and S4 carry a 'With talent' line stating the expected mechanism; S3, S5 and S6 omit it. For those three, nothing states which step of the skill is supposed to produce the passing behaviour, so a pass cannot be attributed to the artefact.",
      "quote": "- **With talent:** triage says update; the owner is extended.\n- **Baseline:** cites \"a video\" with no raw and grades the on-screen numbers MEASURED.\n- **Result:** pending"
    }
  ],

  "per_step_matrix": [
    {
      "step": 1,
      "title": "Keep the raw.",
      "ends_in_something_checkable": "PARTLY. 'a copy exists in raw/ with the fetch date in the file name' is observable; the required content hash is not, because step 4's schema has no field for it and no fixture carries one (F13).",
      "graded_by": "NOTHING RUNNABLE. No evals.json expectation inspects a raw copy — all three prompts pre-place the raw and ask only that the wiki be edited. Only S3's prose ('the transcript text is saved as the raw') touches it, and S3 has no runnable entry (F4)."
    },
    {
      "step": 2,
      "title": "Search before writing.",
      "ends_in_something_checkable": "PARTLY. The triage label is never recorded as an artefact except, in one branch, as a log line; it is inferred from the resulting file state. The 'no material' branch is checkable but its required log content is stated four incompatible ways (F10).",
      "graded_by": "update branch → evals.json eval 1 + S1. disputed branch → eval 2 + S2. no-material branch → eval 3 + S5. The 'new' branch is graded by NOTHING — no eval presents a topic no page owns. Mixed-triage sources are graded by nothing and undefined (F3)."
    },
    {
      "step": 3,
      "title": "Locate every number, date and quote in the raw before it is written.",
      "ends_in_something_checkable": "NO, as written. The mandated claim row (what it says, source, locator, verbatim line, verdict) has no home in step 4's schema or in any bundled note (F12), and the MEASURED criterion contradicts the two places that apply it (F2).",
      "graded_by": "NOTHING RUNNABLE. No evals.json expected_output requires a verbatim line or a verdict; eval 2 does not even require the numbers the raw contains (F25). Only S1 and S3 prose mention verdicts, and S3 has no runnable entry."
    },
    {
      "step": 4,
      "title": "Write the page in the schema.",
      "ends_in_something_checkable": "PARTLY. Frontmatter fields are checkable. 'status from the fixed vocabulary' is not — no vocabulary is given (F15). The four body sections are checkable in principle but contradicted by every fixture and by eval 1's in-place expectation (F17).",
      "graded_by": "PARTIALLY by evals.json eval 1 ('the new source with its fetch date in frontmatter'). Status, tags, related and all four body sections are graded by NOTHING."
    },
    {
      "step": 5,
      "title": "Cascade.",
      "ends_in_something_checkable": "YES. 'the neighbour names it back with a sentence that says why' is directly observable in the neighbour file.",
      "graded_by": "NOTHING THAT CAN FAIL. Eval 1's clause checks a link the fixture already contains, so it passes on an unchanged tree; eval 2's page names no neighbour. The only real test is S4, which has no runnable entry (F19, F4)."
    },
    {
      "step": 6,
      "title": "Register.",
      "ends_in_something_checkable": "PARTLY. Source-log and operation-log rows are checkable. The index row is not consistently checkable: the step demands it unconditionally while S1 requires INDEX unchanged for the same run (F8), and the repo instance section names no operation-log file (F26).",
      "graded_by": "SOURCES + LOG rows → evals.json evals 1, 2 and 3, and S1/S5. The index row is graded by NOTHING positive — the only check touching INDEX (S1) asserts the opposite."
    },
    {
      "step": 7,
      "title": "Lint, then rebuild the index.",
      "ends_in_something_checkable": "NO. Both halves fail. The lint has no implementation in the bundle (no kb.py, no check.py — F5, F7), and 'rebuild the index' is named in the heading but never described, so it has no defined outcome at all (F20). The terminal commit is required by S4 but produced by no step and by no eval prompt (F21).",
      "graded_by": "NOTHING. S1, S2, S3 and S4 all condition on lint output that cannot be produced in this bundle; no evals.json entry mentions lint."
    }
  ],

  "summary": {
    "findings_total": 28,
    "class_level": 12,
    "instance_level": 16,
    "steps_ending_in_something_checkable": "1 of 7 fully (step 5); 5 partly (steps 1, 2, 4, 6 and — only in principle — 3); 1 not at all (step 7)",
    "steps_graded_by_a_runnable_check": "steps 2, 4 and 6 only, and each only in part; steps 1, 3, 5 and 7 are graded by nothing that can execute",
    "sharpest_single_defect": "F2 — step 3's definition of MEASURED excludes the vendor pricing page that both the Example and S1 grade MEASURED, so the eval rewards violating the rule it is meant to enforce."
  }
}
```

The three that would change the artefact most: **F2** (the verdict rule and every place applying it disagree), **F1** (the "never runs external code" rule forbids the lint that step 7 and the whole eval oracle depend on), and **F4/F5/F6 together** (half the declared scenarios have no runnable entry, the one named grader `check.py` is absent, and every `expectations` array is empty — so the suite currently grades nothing mechanically).