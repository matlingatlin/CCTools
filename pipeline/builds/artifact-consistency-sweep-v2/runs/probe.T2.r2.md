I examined all 13 files: `SKILL.md` (7 numbered steps, 4 rules, description, When-to-use, In-this-repo), `references/rationale.md`, `evals.md` (S1–S6 narrative), `evals/evals.json` (3 executable evals, 31 expectations), and all 9 fixture files (3 raw sources, 3 wiki notes, INDEX/LOG/SOURCES). I checked every step against the rules, every step against every other step, every step against the eval expectations and against the fixture contents, the description against the body, the rationale against the body, and every named file against what is actually bundled.

```json
{
  "examined": {
    "files_read": ["SKILL.md", "references/rationale.md", "evals.md", "evals/evals.json", "evals/files/raw/2026-09-02-pricing-page.md", "evals/files/raw/2026-09-02-gamma-model-card.md", "evals/files/raw/2026-09-02-blog-restating-caching.md", "evals/files/wiki/INDEX.md", "evals/files/wiki/LOG.md", "evals/files/wiki/SOURCES.md", "evals/files/wiki/notes/model-prices.md", "evals/files/wiki/notes/prompt-caching.md", "evals/files/wiki/notes/local-models.md"],
    "pair_classes_swept": ["step x rule (7x4)", "step x step (21 pairs)", "step x eval expectation (7x31)", "step x fixture state", "description x body", "when-to-use x steps", "rationale x rules/steps", "evals.md x evals.json", "evals.md x fixtures", "named file x bundled file (BOM)"],
    "units": {"numbered_steps": 7, "rules": 4, "narrative_scenarios": 6, "executable_evals": 3, "expectations": 31, "fixture_files": 9}
  },

  "findings": [
    {
      "id": "C1",
      "level": "CLASS",
      "where": "SKILL.md Rules (lines 46-50) vs references/rationale.md line 3",
      "finding": "The rationale file states a contract it does not meet: it claims to hold the origin of EVERY rule, but three of the four Rules and one of the seven Steps have no entry in it at all. By the file's own stated test those rules 'do not belong in the body'. Rules 2, 3 and 4 and Step 4 are unbacked; nothing in the artefact says where they came from.",
      "quote": "rationale.md: \"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\" | Unbacked SKILL.md rules: \"`null` for not-fetched and not-measured; `0` only for a measured zero.\" / \"Nothing about a tool, price, version or limit from memory: look it up and date it.\" / \"This skill installs, fetches and runs nothing; it is a writing discipline.\" | Unbacked step: \"4. **Write the page in the schema:** frontmatter `title`, `sources` ...\""
    },
    {
      "id": "C2",
      "level": "CLASS",
      "where": "SKILL.md Rule 4 (line 50) vs Steps 2 and 7, Rule 3, the In-this-repo section, and the description",
      "finding": "Rule 4 forbids what four other parts of the same file mandate. 'Runs nothing' is contradicted by Step 7 (run the lint, rebuild the index) and Step 2 (query the wiki's index), and In-this-repo hands out the exact commands to run. 'Fetches nothing' is contradicted by Rule 3 ('look it up') and by the description's own trigger ('a fetched page'). The description also advertises 'lint' as something the skill does.",
      "quote": "Rule: \"This skill installs, fetches and runs nothing; it is a writing discipline.\" | Step 7: \"**Lint, then rebuild the search index;** fix what the lint names before committing.\" | Step 2: \"query the wiki's index for the title, trigger terms and URL\" | Rule 3: \"Nothing about a tool, price, version or limit from memory: look it up and date it.\" | In this repo: \"lint `python3 knowledge/kb.py lint`; rebuild `kb.py build`.\""
    },
    {
      "id": "C3",
      "level": "CLASS",
      "where": "All 7 steps vs evals/evals.json expectations",
      "finding": "Every step is graded on the artefact it leaves behind and on nothing else; the provenance/discipline half of each step is graded by nothing in all three evals. Ungraded across the board: the raw file, its hash and MANIFEST (1); the search that precedes the triage (2); the 'locator' field and WHICH verdict word is chosen (3); the four body sections and 'Date what will move' (4); the cascade sentence (5); the map-of-contents row (6); the lint run, the single commit, and the orphan hand-check (7).",
      "quote": "Step 1: \"with URL or path, fetch date and a content hash - in a `raw/` directory ... provenance in `raw/MANIFEST.md`\" — no expectation in evals.json mentions raw, hash or MANIFEST. Step 3: \"claim, source, locator, verbatim line, verdict\" — graded only by \"check.py T1: quote from the raw on the page\" and \"check.py T1: verdict word per claim\"."
    },
    {
      "id": "C4",
      "level": "CLASS",
      "where": "Bill of materials: evals.md line 6, evals/evals.json (21 expectations), SKILL.md step 1 — vs the bundle",
      "finding": "Three named files are absent from the artefact, and two rival graders are named for the same criterion. evals.md says the observable criterion is checked by kb.py lint --json; evals.json instead prefixes 21 of its 31 expectations with check.py. Neither script exists anywhere in the bundle (no .py file at all), so no expectation labelled 'check.py' can currently be run. raw/MANIFEST.md is likewise named by step 1 and absent from the fixture wiki.",
      "quote": "evals.md: \"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\" | evals.json: \"check.py T1: no rival page\" | SKILL.md step 1: \"provenance in `raw/MANIFEST.md`\" | bundle contains: SKILL.md, evals.md, evals/evals.json, references/rationale.md and 9 fixture .md files — zero .py files, no MANIFEST.md"
    },
    {
      "id": "C5",
      "level": "CLASS",
      "where": "evals.md scenario Inputs vs evals/files/raw/*",
      "finding": "The narrative eval descriptions do not match the fixtures they describe, in both executed non-trivial scenarios. The counts and the source identity are both wrong, so the prose spec and the runnable spec disagree about what is being tested.",
      "quote": "evals.md S1: \"a fetched vendor pricing page with three per-MTok prices\" — the fixture carries two models (\"Alpha 5: $5.00 per million input tokens, $25.00 per million output tokens. Beta 5: $2.00 ...\") plus two multipliers. | evals.md S5: \"a blog post restating three facts the wiki already holds with the same sources\" — the fixture restates two (\"Cache reads cost a tenth of the input price and writes cost 1.25 times.\") under a different URL (\"source: https://example.test/blog/caching-explained\" vs the note's \"url: https://example.test/caching\")."
    },
    {
      "id": "C6",
      "level": "CLASS",
      "where": "SKILL.md step 2 (four dispositions) vs evals/evals.json (three evals)",
      "finding": "Step 2 declares four mutually exclusive dispositions; only three are exercised. The 'new' branch is graded by nothing, and because no eval ever creates a page, everything conditioned on a new page is ungraded too: step 4's whole-page write (the generic frontmatter expectation only checks that PRE-EXISTING notes keep their fields) and step 6's map-of-contents row.",
      "quote": "Step 2: \"**new** (no page owns the topic) · **update** ... · **disputed** ... · **no material** ...\" | Step 6: \"a row in the hand-written map of contents for a new page\" | The only INDEX expectation is \"every note is listed in INDEX.md\", which the fixture satisfies before any run, and evals.md S1 confirms \"INDEX unchanged\"."
    },
    {
      "id": "C7",
      "level": "CLASS",
      "where": "evals/evals.json generic expectations vs the fixture's pre-run state",
      "finding": "Four expectations are already true of the fixture before any run, so they cannot distinguish a run that performed the step from one that did nothing. They are no-regression guards presented in the same flat list as the discriminating checks, with no marking of which is which.",
      "quote": "\"every note keeps title/status/tags/related/sources frontmatter\", \"no dangling [[link]]\", \"every note is listed in INDEX.md\", \"check.py T1: neighbour names owner back\" — the fixture already has all five frontmatter keys on all three notes, no dangling links, all three notes in INDEX.md, and prompt-caching.md already carries \"related: [\"[[model-prices]]\"]\"."
    },
    {
      "id": "I1",
      "level": "INSTANCE",
      "where": "evals/evals.json eval id 1, expectation 5, vs evals/files/wiki/notes/model-prices.md and evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The one expectation that is supposed to grade the actual update asserts the UN-updated row. The literal it looks for is the fixture's existing pre-ingest line; the raw source changes Beta 5 to $2/$10. As written, a run that changes nothing passes this check, and it collides with the separate 'old price kept' expectation, which asserts the same string for the opposite reason. No expectation anywhere grades that $2/$10 landed.",
      "quote": "expectation: \"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\" | fixture note (pre-run): \"| Beta 5 | $3 | $15 | 2026-08-20 |\" | raw source: \"Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.\" | sibling expectation: \"check.py T1: old price kept as history or superseded row\""
    },
    {
      "id": "I2",
      "level": "INSTANCE",
      "where": "SKILL.md step 3 (verdict definitions) vs evals.md S1 pass criterion",
      "finding": "The eval demands the verdict the step's own definition forbids. A vendor pricing page asserts a price, it does not measure one, so by step 3 it is REPEATED; evals.md S1 requires MEASURED. evals.json does not resolve the conflict — it only checks that a verdict word is present, never which one, so the distinction step 3 exists to enforce is graded by nothing.",
      "quote": "Step 3: \"MEASURED (the source measured it), REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters)\" | evals.md S1: \"the owning note gains a dated row with the verbatim line and MEASURED\" | evals.json: \"check.py T1: verdict word per claim\""
    },
    {
      "id": "I3",
      "level": "INSTANCE",
      "where": "SKILL.md step 2 ('no material' definition) vs evals/files/raw/2026-09-02-blog-restating-caching.md and rationale.md",
      "finding": "The graded no-material fixture does not satisfy the step's own definition of no material. The step conjoins 'no claim, no value'; the blog carries two values. The rationale states the intended test correctly ('no new claim'), so the body's wording is the drifted one — and it is the wording a reader of SKILL.md alone would apply.",
      "quote": "Step 2: \"**no material** (no claim, no value, no newer date for any page: keep the raw, write the source-log row and one operation-log line ...\" | fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times.\" | rationale.md: \"the log says `no material: <url> restates prompt-caching's 0.1x / 1.25x, no new claim`\""
    },
    {
      "id": "I4",
      "level": "INSTANCE",
      "where": "references/rationale.md lines 16-18 vs evals.md S5",
      "finding": "The two files report different baseline run counts for the same observation. The rationale says every baseline run means 2 of 2; evals.md counts five baseline runs across three arms. The rationale's parenthetical describes only the probe arm but is written as if it covered all of them.",
      "quote": "rationale.md: \"Observed 2026-09-02 in the first build's probes: on a blog post restating two multipliers a note already held, every baseline run (2 of 2) still edited the owning page\" | evals.md S5: \"with 2/2; without 0/1, probe 0/2, incumbent 0/2\" and \"PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "id": "I5",
      "level": "INSTANCE",
      "where": "evals.md line 3 (header) vs evals.md S1 and S5 arm listings",
      "finding": "The header's run design contradicts the per-scenario data it summarises. Four arms are itemised, not three, and the 'without' arm ran once, not twice, so k=2 does not hold uniformly.",
      "quote": "header: \"the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule)\" | S1: \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\" | S5: \"with 2/2; without 0/1, probe 0/2, incumbent 0/2\""
    },
    {
      "id": "I6",
      "level": "INSTANCE",
      "where": "evals.md Method (line 6) vs the S2 and S5 type labels and results",
      "finding": "The scenario type labels are inverted against the method's own rule and against the measured results. The rule ties 'Beats baseline' to scenarios where the baseline plausibly fails, yet the only scenario that beat baseline is labelled normal, and the one labelled trap showed no delta.",
      "quote": "Method: \"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\" | \"### S5 — no material · normal\" → \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\" | \"### S2 — a source that contradicts a page · trap\" → \"**Result:** PASS (no delta; baseline clean)\""
    },
    {
      "id": "I7",
      "level": "INSTANCE",
      "where": "evals.md line 6 vs evals.md S6",
      "finding": "The method claims a file-state criterion for every scenario, but the negative-trigger scenario's criterion is about which skill fires, which leaves no file state to inspect. evals.md later concedes S6 has no executable eval, contradicting the 'every scenario' claim it opened with.",
      "quote": "line 6: \"The observable criterion for every scenario is the state of the files\" | S6: \"**Pass criterion:** this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page).\" | line 49: \"S3 ..., S4 ... and S6 ... have no executable eval yet\""
    },
    {
      "id": "I8",
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs all three evals/evals.json prompts",
      "finding": "Step 7's terminal condition is a commit, but every eval prompt ends at editing files in place and never invokes git, so the clause binding the fact and its lint pass into one commit cannot be observed by any check. The alternative branch's obligation ('say so in the log line') is likewise graded by nothing.",
      "quote": "Step 7: \"fix what the lint names before committing. The fact and its lint pass land in one commit. No lint script? Hand-check dangling links, unlisted pages and orphans, and say so in the log line.\" | every eval prompt: \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "id": "I9",
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (orphans) vs evals/files/wiki/notes/local-models.md",
      "finding": "Step 7 names orphans as one of three things to hand-check, no expectation grades orphans, and the fixture ships a pre-existing orphan that no eval will ever surface. Two of the three named hand-checks have surrogate expectations; the orphan check has none.",
      "quote": "Step 7: \"Hand-check dangling links, unlisted pages and orphans\" | local-models.md frontmatter: \"related: []\" — no note links to it and it links to none. evals.json covers \"no dangling [[link]]\" and \"every note is listed in INDEX.md\" only."
    },
    {
      "id": "I10",
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals/evals.json eval id 1",
      "finding": "The only check aimed at the cascade grades a link that already exists in the fixture and points the wrong way. Step 5 requires the NEIGHBOUR to gain a sentence and a related entry; the check asks whether the neighbour still names the owner, which is true before the run. The 'one sentence' requirement is graded by nothing, and the scenario built for step 5 is not executed.",
      "quote": "Step 5: \"every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. If no true sentence exists, do not add the edge.\" | eval 1 expected_output: \"the neighbour still names the owner\" | fixture prompt-caching.md: \"related: [\"[[model-prices]]\"]\" | evals.md S4: \"**Result:** pending\""
    },
    {
      "id": "I11",
      "level": "INSTANCE",
      "where": "evals/evals.json eval id 3: expected_output vs its expectations",
      "finding": "The stated criterion is broader than the checks that grade it. 'No page changed' covers three notes; only prompt-caching is checked for being unchanged, so an edit to model-prices or local-models would pass. model-prices is the exposed one — it also carries the cache multiplier the blog restates.",
      "quote": "expected_output: \"No page changed and no page created; one LOG line saying no material with the source URL.\" | expectations: \"check.py T3: prompt-caching unchanged\", \"check.py T3: no new note\" | model-prices.md: \"[[prompt-caching]] multiplies these by 0.1 on a cache read.\""
    },
    {
      "id": "I12",
      "level": "INSTANCE",
      "where": "SKILL.md When to use (line 15) vs Steps 1-7 and the description",
      "finding": "A declared trigger has no procedure behind it. The write-back of a compiled summary page appears in When-to-use and then nowhere else — no step covers it, the description does not mention it, and no eval exercises it.",
      "quote": "\"- An existing note gains a source, or a compiled summary page is written back.\""
    },
    {
      "id": "I13",
      "level": "INSTANCE",
      "where": "SKILL.md Rule 2 (line 48) vs Steps 1-7 and evals/evals.json",
      "finding": "An orphan rule: no step produces a field where null-versus-zero can arise, the step 4 schema has no numeric field, no fixture frontmatter has one, and no expectation grades it. The rule governs nothing the artefact does.",
      "quote": "Rule: \"`null` for not-fetched and not-measured; `0` only for a measured zero.\" | Step 4 schema: \"frontmatter `title`, `sources` (url or path, fetched, note), `status` ..., `tags`, `related`\""
    },
    {
      "id": "I14",
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4",
      "finding": "The two steps place the disputed marker in different locations and neither defers to the other, so a run cannot tell whether frontmatter status must change. The eval's check is loose enough to accept either, so the ambiguity is never forced.",
      "quote": "Step 2: \"keep both values as dated rows with their sources, mark the page `disputed` there\" | Step 4: \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\" | eval 2: \"check.py T2: disputed marker\""
    },
    {
      "id": "I15",
      "level": "INSTANCE",
      "where": "SKILL.md step 2 ('stop') vs step 7",
      "finding": "The no-material branch terminates the procedure before step 7, so the lint and the single-commit rule are silently exempted for that path. Nothing states whether the exemption is intended; the log and source rows are re-specified inline in step 2, which shows the author was aware the branch skips step 6 but says nothing about 7.",
      "quote": "Step 2: \"keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop\" | Step 7: \"The fact and its lint pass land in one commit.\""
    },
    {
      "id": "I16",
      "level": "INSTANCE",
      "where": "SKILL.md line 8 (the summary line) vs the Steps section",
      "finding": "The one-line summary enumerates seven items for seven steps but skips step 4 and spends two items on step 3, so the schema step is absent from the artefact's own overview.",
      "quote": "\"Karpathy's LLM Wiki `ingest` operation made procedural: raw kept, triaged, quoted, graded, cascaded, registered, linted.\" — quoted and graded are both step 3; no item corresponds to \"4. **Write the page in the schema:**\""
    },
    {
      "id": "I17",
      "level": "INSTANCE",
      "where": "evals.md line 49",
      "finding": "A dangling cross-reference: the next iteration's item is cited by a number that appears nowhere in the artefact, and neither does the named whole-artefact review, so the gap has no traceable owner.",
      "quote": "\"The whole-artefact review named this gap; closing it is the next iteration's 2.4.\""
    },
    {
      "id": "I18",
      "level": "INSTANCE",
      "where": "evals.md (S1-S6) vs evals/evals.json (ids 1-3) vs the T1/T2/T3 labels",
      "finding": "Three parallel numbering schemes name the same tests with no mapping declared. evals.md ties S-numbers to T-numbers inline, but nothing ties T-numbers to evals.json ids; the link is only inferable from the expectation prefixes inside the JSON.",
      "quote": "evals.md: \"### S5 — no material · normal — EXECUTED as T3\" | evals.json: \"\\\"id\\\": 3\" with \"check.py T3: no new note\""
    }
  ],

  "step_matrix": [
    {
      "step": 1,
      "text": "Keep the raw (bytes, URL/path, fetch date, content hash, raw/ dir, MANIFEST.md)",
      "ends_in_something_checkable": "yes in principle — a file, a hash, a MANIFEST row are all observable",
      "graded_by": "NOTHING",
      "note": "No expectation in any of the three evals mentions the raw, the hash or MANIFEST.md. The fixture has no MANIFEST.md, so the step is also unexercisable as staged. The evals hand the raw file to the model already saved, which is the state step 1 is supposed to produce."
    },
    {
      "step": 2,
      "text": "Search, then triage into exactly one of new / update / disputed / no material",
      "ends_in_something_checkable": "yes — the disposition is readable off the resulting file state",
      "graded_by": "update: eval 1 \"check.py T1: no rival page\". disputed: eval 2 \"check.py T2: disputed marker\", \"check.py T2: both values present\". no material: eval 3 \"check.py T3: no new note\", \"check.py T3: prompt-caching unchanged\", \"check.py T3: LOG says no material\".",
      "note": "The 'new' branch is graded by nothing (C6). The search sub-step is graded by nothing — only its outcome is. The no-material fixture does not satisfy the branch's literal definition (I3)."
    },
    {
      "step": 3,
      "text": "One row per claim: claim, source, locator, verbatim line, verdict (MEASURED/REPEATED/DERIVED)",
      "ends_in_something_checkable": "partial — the quote and the presence of a verdict word are checkable; the locator and the correctness of the verdict are not checked anywhere",
      "graded_by": "eval 1 \"check.py T1: quote from the raw on the page\", \"check.py T1: verdict word per claim\"; eval 2 \"check.py T2: quote from the card on the page\", \"check.py T2: verdict word per claim\".",
      "note": "'locator' is graded by nothing. WHICH verdict is graded by nothing, and evals.md demands a verdict the step's definition forbids (I2). DERIVED is never exercised by any fixture."
    },
    {
      "step": 4,
      "text": "Write the page in the schema: five frontmatter keys; body = what it is / claims graded / what it means here / what is open; date what will move",
      "ends_in_something_checkable": "partial — frontmatter keys are checkable; the four named body sections and 'Date what will move' have no stated observable",
      "graded_by": "all three evals \"every note keeps title/status/tags/related/sources frontmatter\"; eval 1 \"check.py T1: new source in note frontmatter with fetch date\"; eval 2 \"check.py T2: model card in frontmatter sources\", \"check.py T2: both sources dated\".",
      "note": "The frontmatter expectation is a KEEPS check on pre-existing notes, not a check that a newly written page has them — and no eval writes a new page (C6, C7). The four body sections are graded by nothing."
    },
    {
      "step": 5,
      "text": "Cascade: each named neighbour gains a sentence, then the related: entry; no true sentence, no edge",
      "ends_in_something_checkable": "yes as written (a sentence and an entry are both observable), but effectively graded by nothing",
      "graded_by": "nominally eval 1 \"check.py T1: neighbour names owner back\" — but this is true of the fixture before the run and points the opposite direction from what the step requires.",
      "note": "The 'one sentence' requirement and the negative clause ('do not add the edge') are graded by nothing. The scenario designed for this step, S4, is \"**Result:** pending\" with no entry in evals.json (I10)."
    },
    {
      "step": 6,
      "text": "Register: map-of-contents row for a new page; source-log row per consulted source (also on no material); operation-log line",
      "ends_in_something_checkable": "yes — three named rows in three named files",
      "graded_by": "eval 1 \"check.py T1: SOURCES row\", \"check.py T1: LOG row\"; eval 2 \"check.py T2: SOURCES row\", \"check.py T2: LOG row\"; eval 3 \"check.py T3: LOG says no material\", \"check.py T3: SOURCES row for the consulted source\".",
      "note": "Best-graded step in the artefact, including the also-on-no-material clause. The map-of-contents clause alone is ungraded because no eval creates a page; \"every note is listed in INDEX.md\" is a pre-satisfied preservation check."
    },
    {
      "step": 7,
      "text": "Lint, rebuild the search index, fix what lint names before committing, fact + lint pass in one commit; else hand-check dangling links / unlisted pages / orphans and say so in the log line",
      "ends_in_something_checkable": "no, as staged — the named grader is not bundled, and the commit clause has no observable in any eval",
      "graded_by": "partial surrogates only: all three evals \"no dangling [[link]]\" and \"every note is listed in INDEX.md\". The lint run, the index rebuild, the single commit, the orphan check and the 'say so in the log line' clause are graded by NOTHING.",
      "note": "evals.md names kb.py lint --json and evals.json names check.py; neither exists in the bundle (C4). The eval prompts never reach a commit (I8). The fixture contains an ungraded pre-existing orphan (I9). The step also directly contradicts Rule 4 (C2)."
    }
  ],

  "summary": {
    "steps_ending_in_something_checkable": "5 of 7 fully or partly (2, 3, 4, 5, 6); step 1 is checkable in principle but has no check and no fixture support; step 7 is not checkable as staged",
    "steps_graded_by_nothing": [1, 5, 7],
    "steps_graded_only_in_part": [2, 3, 4],
    "steps_adequately_graded": [6],
    "rules_with_no_backing_and_no_check": ["null/0 rule", "no-facts-from-memory rule", "installs/fetches/runs nothing rule"],
    "direct_contradictions": ["Rule 4 vs steps 2 and 7 and Rule 3 and the description (C2)", "step 3 verdict definition vs evals.md S1 (I2)", "step 2 no-material definition vs its own graded fixture (I3)", "rationale 2-of-2 vs evals.md 0-of-5 (I4)", "header three-arms/k=2 vs S1 and S5 arm data (I5)", "method's beats-baseline rule vs S2/S5 type labels (I6)", "method's every-scenario file criterion vs S6 (I7)", "evals.md three prices / three facts vs the fixtures (C5)", "eval 1's 'beta price updated' literal vs the raw source (I1)", "step 2 disputed-at-the-line vs step 4 status frontmatter (I14)"],
    "missing_from_bill_of_materials": ["check.py (named by 21 expectations)", "knowledge/kb.py (named as the eval grader)", "raw/MANIFEST.md (named by step 1, absent from the fixture wiki)"],
    "most_consequential": "I1 — the only expectation that grades the actual price update asserts the pre-update row, so eval 1 would pass a run that changed nothing in the table; and C2 — the rule that the skill runs nothing contradicts the two steps that require running the lint and the index query."
  }
}
```

Two things worth calling out beyond the JSON. First, the rewrite that moved rationale into `references/` is where most of the drift sits: the rationale covers steps 1, 2, 3, 5, 6, 7 and the trigger, but not step 4 and not three of the four Rules — while opening with a claim that it covers every rule. That is the single edit most likely to have introduced findings C1 and C2. Second, the artefact is honest about S3/S4/S6 being unexecuted, so those are not findings against it; the ungraded steps I flagged (1, 5, 7) are ungraded *in addition* to that admitted gap — step 5 in particular is claimed to be covered by S4's future eval, but its supposed present-day check in eval 1 is a pre-satisfied backlink in the wrong direction.