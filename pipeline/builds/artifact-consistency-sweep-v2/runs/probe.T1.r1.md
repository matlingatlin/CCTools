Confirmed the gaps. Here are my findings.

```json
{
  "examined": {
    "artefact_root": "./artifact-A (the prompt named ./artifact; the only artefact directory present is artifact-A)",
    "files_read_in_full": [
      "SKILL.md (93 lines: frontmatter, When to use, When NOT to use, Steps 1-7, Example, 5 Rules, In this repo)",
      "evals.md (49 lines: header, Method, S1-S6, Failure triage)",
      "evals/evals.json (37 lines: 3 evals, each with prompt / expected_output / files / expectations)",
      "evals/files/raw/2026-09-02-pricing-page.md",
      "evals/files/raw/2026-09-02-gamma-model-card.md",
      "evals/files/raw/2026-09-02-blog-restating-caching.md",
      "evals/files/wiki/INDEX.md, LOG.md, SOURCES.md",
      "evals/files/wiki/notes/model-prices.md, prompt-caching.md, local-models.md"
    ],
    "pairs_swept": [
      "each of Steps 1-7 against each of the 5 Rules (35 pairs)",
      "each Step against every other Step (21 pairs)",
      "each Step against every eval expectation in evals.json (21 pairs) and every scenario in evals.md (42 pairs)",
      "frontmatter description against each body section (When to use, When NOT to use, Steps, Rules)",
      "SKILL.md Example against Steps 2/3/6 and against evals.md S1/S5 and evals.json evals 1/3",
      "evals.md scenario list against evals.json eval list (6 vs 3)",
      "every file named in evals.json 'files' arrays and in evals.md against the files actually present",
      "every eval prompt against the bundled fixture it points at (raw contents vs wiki note contents)"
    ],
    "not_present": "there is no references/ directory in this artefact, and SKILL.md never claims one — the only `references/` mention is a pointer to another skill's bundle, so this is not a missing-file finding"
  },

  "findings": [
    {
      "id": "F1",
      "level": "CLASS",
      "where": "evals/evals.json — all three evals, `files` arrays (lines 11, 22, 33)",
      "finding": "Every eval declares a checker file `evals/files/check.py` in its bill of materials. No such file exists anywhere in the artefact (only raw/ and wiki/ fixtures ship). All three evals would fail to stage.",
      "quote": "\"evals/files/check.py\"   (×3, lines 11, 22, 33)  —  ls evals/files → raw/, wiki/ only"
    },
    {
      "id": "F2",
      "level": "CLASS",
      "where": "evals/evals.json — all three evals, `expectations` field",
      "finding": "Every eval ships an empty expectations array. Nothing in the runnable suite asserts anything; the only grading text is the free-prose `expected_output`, which no mechanism consumes. Combined with F1 this means no step in SKILL.md is graded by an executable check.",
      "quote": "\"expectations\": []   (×3, lines 13, 24, 35)"
    },
    {
      "id": "F3",
      "level": "CLASS",
      "where": "evals.md line 6 (Method) vs the bundled fixture at evals/files/wiki",
      "finding": "The declared observable criterion for EVERY scenario is a lint tool that does not exist in the artefact and is not reachable from the fixture path the eval prompts use. evals.md names kb.py lint --json; evals.json names check.py; neither ships. Two rival check mechanisms, zero shipped.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\""
    },
    {
      "id": "F4",
      "level": "CLASS",
      "where": "evals.md S1-S6 vs evals/evals.json (3 evals)",
      "finding": "Six scenarios are specified; three are implemented. S3 (edge — video transcript, tests the REPEATED verdict and the `note:` source entry), S4 (pressure — the cascade, the only test of Step 5), and S6 (negative-trigger) have no eval entry and no fixture. The negative-trigger scenario — the one the standing test rule requires — is therefore unrunnable, and Step 5 is graded by nothing.",
      "quote": "evals.md: \"### S3 … · edge\", \"### S4 — the cascade under time pressure · pressure\", \"### S6 — a claim to bundle into a skill · negative-trigger\"  vs  evals.json: \"id\": 1, \"id\": 2, \"id\": 3 only"
    },
    {
      "id": "F5",
      "level": "CLASS",
      "where": "SKILL.md Step 3 (lines 48-51) vs SKILL.md Example (line 69) and evals.md S1 (line 12)",
      "finding": "Step 3 defines MEASURED as requiring a dependent variable, an effect and a sample. A vendor pricing page has none of these — by Step 3's own definition its numbers are REPEATED. Yet both the Example and S1's pass criterion require the pricing claim to be graded MEASURED. S3 then treats grading an unmeasured source MEASURED as the baseline's failure. The artefact grades the same kind of claim both ways.",
      "quote": "Step 3: \"a verdict - **MEASURED** (the source measured it: dependent variable, effect, sample), **REPEATED** (asserted, no measurement found)\"  |  Example: \"the note gets a dated row with the verbatim line and MEASURED\"  |  S1: \"the owning note gains a dated row with the verbatim line and MEASURED\"  |  S3 baseline (a failure): \"grades the on-screen numbers MEASURED\""
    },
    {
      "id": "F6",
      "level": "CLASS",
      "where": "SKILL.md Step 1 (lines 31, 33-34) vs Step 4 (lines 52-53), vs the fixture notes, vs evals.json eval 1",
      "finding": "Step 1 requires a content hash in the page's source entry. Step 4's schema for that same entry lists only url-or-path, fetch date and note — no hash field. Every fixture note's source entry has url + fetched only, and eval 1's expected_output asks for the fetch date and no hash. A step-mandated field the schema has no slot for, produced by no fixture and graded by nothing.",
      "quote": "Step 1: \"with provenance: URL or path, fetch date, and a content hash or commit\" / \"a content hash in the page's source entry\"  vs  Step 4: \"Frontmatter with title, sources (url or path, fetch date, note)\"  vs  eval 1: \"the new source with its fetch date in frontmatter\""
    },
    {
      "id": "F7",
      "level": "INSTANCE",
      "where": "SKILL.md Step 6 (line 59) vs SKILL.md Step 2 (lines 40-43), and vs evals.md S5 / evals.json eval 3",
      "finding": "Step 6 is unconditional: every ingest writes one row per source in the source log. Step 2's no-material branch says the source is not added and the operation stops after one log line. The two steps prescribe opposite treatment of SOURCES.md for the same source, and neither S5 nor eval 3 says which is graded — both are silent on SOURCES.md, so a run that adds the row and a run that omits it both pass.",
      "quote": "Step 6: \"One row in the index (map of contents), one row per source in the source log, one entry in the operation log\"  vs  Step 2: \"A corroborating source is not added to the page's source list\" / \"write one operation-log line with the URL and the reason, and stop\"  vs  eval 3: \"No page changed and no page created; one LOG line saying no material with the source URL.\""
    },
    {
      "id": "F8",
      "level": "INSTANCE",
      "where": "SKILL.md Step 6 (line 59) vs evals.md S1 (line 12)",
      "finding": "Step 6 requires an index row on every ingest with no exception for the update branch. S1's pass criterion for exactly that branch requires the index to be unchanged. A run that follows Step 6 literally fails S1.",
      "quote": "Step 6: \"**Register.** One row in the index (map of contents)\"  vs  S1: \"no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row\""
    },
    {
      "id": "F9",
      "level": "INSTANCE",
      "where": "SKILL.md Rules (line 83) vs Step 2 (line 35), Step 7 (lines 61-63), In this repo (lines 89-91), evals.md line 6",
      "finding": "A rule states the skill never runs code, while the procedure it governs requires running the wiki's lint (and, in the instance section, kb.py find / lint / build) and the eval method's only criterion is a command invocation. The rule contradicts the step it sits beside.",
      "quote": "Rule: \"This skill never installs, fetches or runs external code; it is a writing discipline.\"  vs  Step 7: \"Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches)\"  vs  In this repo: \"lint with `python3 knowledge/kb.py lint` (exit 1 on errors) and rebuild with `kb.py build`\""
    },
    {
      "id": "F10",
      "level": "INSTANCE",
      "where": "SKILL.md Step 7 heading vs Step 7 body (lines 61-63)",
      "finding": "The step is titled 'Lint, then rebuild the index' but its body only instructs the lint and the commit. The index rebuild it names is never instructed anywhere in the general procedure — it appears only in the repo-instance section. Half the step's own heading has no action and no check.",
      "quote": "\"7. **Lint, then rebuild the index.** Run the wiki's deterministic lint … and fix what it names before committing. A verified fact and its lint pass land in the same commit.\""
    },
    {
      "id": "F11",
      "level": "INSTANCE",
      "where": "SKILL.md Step 6 (line 59) vs Step 7 heading (line 61)",
      "finding": "Step 6 has the author hand-write an index row; Step 7 then rebuilds the index. If the index is generated, the hand-written row is either overwritten or duplicated. The artefact never says whether the index is authored or derived, so neither step can be checked without deciding that question.",
      "quote": "Step 6: \"One row in the index (map of contents)\"  vs  Step 7: \"Lint, then rebuild the index.\""
    },
    {
      "id": "F12",
      "level": "INSTANCE",
      "where": "SKILL.md Step 4 (line 53) vs the whole artefact",
      "finding": "Step 4 requires status to come from a 'fixed vocabulary' that the artefact never enumerates. Two values appear scattered elsewhere (`verified` in the fixtures, `disputed` in Step 2), but nothing states the closed set, so the step cannot be checked and eval 2's 'marked disputed' cannot be validated against a defined vocabulary.",
      "quote": "Step 4: \"status from the fixed vocabulary, tags, related\"  —  no list of statuses appears in SKILL.md, evals.md or evals.json"
    },
    {
      "id": "F13",
      "level": "INSTANCE",
      "where": "SKILL.md Step 2 (lines 35-40) vs evals/files/raw/2026-09-02-pricing-page.md and the fixture wiki",
      "finding": "Triage forces exactly one verdict per source, but its four definitions are all per-PAGE. The bundled eval-1 source is simultaneously an update for model-prices (Beta 5 $3/$15 → $2/$10) and no material for prompt-caching (it restates 0.1x / 1.25x, which that note already holds). The step's own structure cannot express the source it is graded on, and eval 1's expected_output never says prompt-caching must be left untouched — so the collision is also ungraded.",
      "quote": "Step 2: \"Triage into exactly one of: **new** (no page owns the topic), **update** (a page owns it…), **disputed**…, **no material** (the source adds no claim, no value and no newer date to any page).\"  vs  fixture raw: \"Cache reads are billed at 10% of the input price; cache writes at 125%.\"  vs  fixture note prompt-caching.md: \"Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\""
    },
    {
      "id": "F14",
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expected_output vs SKILL.md Steps 2 and 4",
      "finding": "Eval 1 grades 'the superseded price kept'. No step instructs this. Step 2 prescribes keeping both values only on the DISPUTED branch; the update branch says only 'extend that page, never a rival', and Step 4 says only to date what will move. An expectation with no step behind it.",
      "quote": "eval 1: \"a dated row per changed price, the superseded price kept\"  vs  Step 2 update branch: \"**update** (a page owns it: extend that page, never a rival)\""
    },
    {
      "id": "F15",
      "level": "INSTANCE",
      "where": "SKILL.md Step 2 (lines 39-41) — internal",
      "finding": "The step asserts no page is touched, then in the same breath requires writing an operation-log line. Whether LOG.md counts as 'a page' is never settled, and eval 3 repeats the same ambiguity ('No page changed … one LOG line'). The check cannot be applied without resolving it.",
      "quote": "Step 2: \"**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop.\""
    },
    {
      "id": "F16",
      "level": "INSTANCE",
      "where": "SKILL.md Rules (line 81) vs Steps 1-7 and all evals",
      "finding": "An orphan rule: no step produces a null-or-zero field, Step 4's schema has no numeric field it could apply to, and no scenario or eval mentions it. A rule that governs nothing in this artefact and is graded by nothing.",
      "quote": "Rule: \"`null` for not-fetched and not-measured; `0` only for a measured zero.\""
    },
    {
      "id": "F17",
      "level": "INSTANCE",
      "where": "SKILL.md description (line 3) vs 'When NOT to use' (lines 22-26)",
      "finding": "The description promises five boundaries; the body's NOT section states four. The deep-reading boundary — the first one the description names — appears nowhere in the body, and no scenario tests it (S6 tests only the skill-knowledge boundary).",
      "quote": "description: \"NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation)\"  vs  body: \"claims being gathered to bundle into a skill's `references/` go through `skill-knowledge` …; a fact about the agent's own task state goes to `unified-memory`; a document made false by a code change is `doc-claim-reconciliation`'s; finding what is wrong across the whole wiki is the `kb-curator` agent's job\""
    },
    {
      "id": "F18",
      "level": "INSTANCE",
      "where": "evals.md S5 (line 38) vs evals/files/raw/2026-09-02-blog-restating-caching.md and SKILL.md Example (lines 74-76)",
      "finding": "S5's input says three facts from the same sources. The bundled blog fixture restates two multipliers, under a different URL from the note's source. The SKILL.md Example describes the same scenario correctly as two multipliers. The scenario description contradicts both the fixture it grades and the Example it derives from.",
      "quote": "S5: \"a blog post restating three facts the wiki already holds with the same sources\"  vs  fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\" (source: https://example.test/blog/caching-explained; note source: https://example.test/caching)  vs  Example: \"a blog post restates two multipliers a note already carries with a dated source\""
    },
    {
      "id": "F19",
      "level": "INSTANCE",
      "where": "evals.md S1 (line 11) vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "S1's input says three per-MTok prices. The bundled fixture carries four per-MTok prices (two models × input/output) plus two cache multipliers, and only one model's prices actually changed. The scenario's description does not match the fixture the eval runs on.",
      "quote": "S1: \"a fetched vendor pricing page with three per-MTok prices\"  vs  fixture: \"Alpha 5: $5.00 … $25.00 …\" / \"Beta 5: $2.00 … $10.00 …\" / \"Cache reads … 10% … writes at 125%.\""
    },
    {
      "id": "F20",
      "level": "INSTANCE",
      "where": "evals.md Method (line 6) vs S5 (lines 37-41) and SKILL.md Step 2 (lines 44-46)",
      "finding": "The Method allows a beats-baseline claim only where the baseline plausibly fails, and S5 is labelled normal. But S5 states a failing baseline, and Step 2 cites a measurement that EVERY baseline run failed this exact scenario. S5 is the strongest beats-baseline scenario in the suite, mislabelled such that the Method forbids scoring it that way.",
      "quote": "Method: \"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\"  |  S5 header: \"### S5 — no material · normal\"  |  S5: \"**Baseline:** writes a thin note anyway.\"  |  Step 2: \"Observed 2026-09-02: without this rule, every baseline run on a restating blog post still edited the owning page\""
    },
    {
      "id": "F21",
      "level": "INSTANCE",
      "where": "evals.md S3, S5, S6 vs S1, S2, S4",
      "finding": "Three scenarios carry a 'With talent:' line stating the expected behaviour and three do not. For S3 and S6 the with-arm behaviour is therefore never stated, leaving the baseline-vs-with comparison the Method mandates with only one side defined.",
      "quote": "S1: \"- **With talent:** triage says update; the owner is extended.\"  |  S3: ends at \"- **Baseline:** cites \\\"a video\\\" with no raw and grades the on-screen numbers MEASURED.\" then \"- **Result:** pending\""
    },
    {
      "id": "F22",
      "level": "INSTANCE",
      "where": "evals.md S5 (line 39) vs SKILL.md Step 2 (line 41) and evals/evals.json eval 3",
      "finding": "S5 grades the log line on carrying a date; Step 2 requires only the URL and the reason, and eval 3 requires only the URL. A pass criterion asserting a field the step never instructs and the runnable eval never checks.",
      "quote": "S5: \"an operation-log entry says \\\"no material\\\" with the URL and date\"  vs  Step 2: \"write one operation-log line with the URL and the reason\"  vs  eval 3: \"one LOG line saying no material with the source URL\""
    },
    {
      "id": "F23",
      "level": "INSTANCE",
      "where": "evals.md S2 (line 18) vs evals/files/wiki/notes/local-models.md",
      "finding": "S2 describes the incumbent value as sourced from the vendor's README; the fixture note's frontmatter source is a model-card URL and only the body prose says README. The scenario's stated provenance is not the provenance the graded file records.",
      "quote": "S2: \"the wiki's note says 744B from the vendor's README\"  vs  local-models.md frontmatter: \"- url: https://example.test/gamma-card\" and body: \"Gamma-7 has 744B total parameters (README, 2026-08-25)\""
    },
    {
      "id": "F24",
      "level": "INSTANCE",
      "where": "SKILL.md Example (line 68) vs Rules (line 83) and the general body",
      "finding": "The Example — which sits in the general, portable half of the skill — invokes a command that is only defined in the repo-instance section, and whose execution the Rules forbid. A reader outside this repo cannot perform the Example's step, and no check exercises it.",
      "quote": "Example: \"`find \\\"pricing\\\"` shows a note that owns model prices\"  vs  Rule: \"This skill never installs, fetches or runs external code\"  vs  In this repo: \"Query with `python3 knowledge/kb.py find \\\"<terms>\\\"`\""
    },
    {
      "id": "F25",
      "level": "INSTANCE",
      "where": "SKILL.md Step 4 (lines 54-55) vs every eval and scenario",
      "finding": "Step 4 ends in two obligations with no observable form and no grader anywhere: naming what would make the claim wrong, and the body sections it lists. No expected_output, pass criterion or fixture mentions either.",
      "quote": "Step 4: \"Body: what it is, the claims graded, what it means for this project, what is still open. Date anything that will move (prices, versions, star counts) and say what would make it wrong.\""
    },
    {
      "id": "F26",
      "level": "INSTANCE",
      "where": "evals/evals.json eval 2 expected_output vs evals/files/raw/2026-09-02-gamma-model-card.md",
      "finding": "The eval-2 source carries four claims (753B total, 40B active, 1M context, 245 GB at 2-bit). The expected_output grades only the parameter counts. Two genuinely new claims — active parameters and context length — are ingested by the run and graded by nothing, so Step 3's 'locate every number' is not actually tested for completeness by the one eval that could test it.",
      "quote": "eval 2: \"Both parameter counts kept as their own dated rows with their sources, the note marked disputed at that fact, neither value overwritten; SOURCES and LOG rows.\"  vs  fixture: \"Total parameters: 753B. Active parameters: 40B. Context: 1M tokens.\""
    }
  ],

  "step_matrix": [
    {
      "step": 1,
      "title": "Keep the raw.",
      "ends_in_something_checkable": "PARTLY — 'a copy exists in raw/ with the fetch date in the filename' is checkable; 'a content hash in the page's source entry' is checkable in principle but Step 4's schema has no field for it (F6)",
      "graded_by": "NOTHING. No expected_output in evals.json mentions the raw copy or a hash. evals.md S3 is the only place the raw layer is a pass criterion, and S3 has no eval entry or fixture (F4).",
      "notes": "The three raw fixtures are inputs, not outputs — no check confirms the run copies them anywhere."
    },
    {
      "step": 2,
      "title": "Search before writing. (triage)",
      "ends_in_something_checkable": "YES for the outcome (which files changed); NO for the search act itself, which leaves no artefact",
      "graded_by": "evals.json eval 1 (update branch), eval 2 (disputed branch), eval 3 (no-material branch); evals.md S1, S2, S5. Best-graded step in the artefact.",
      "notes": "The 'new' branch is graded by nothing — no eval creates a page. The per-source/per-page collision (F13) and the SOURCES contradiction with Step 6 (F7) are both ungraded."
    },
    {
      "step": 3,
      "title": "Locate every number, date and quote … verdict.",
      "ends_in_something_checkable": "YES — the verdict token and the verbatim line are either in the note or not",
      "graded_by": "NOTHING in the runnable suite. evals.json evals 1, 2 and 3 never mention a verdict or a verbatim line. Only evals.md S1 ('MEASURED') and S3 ('REPEATED') grade it in prose, and S1's demanded verdict contradicts Step 3's own definition (F5) while S3 has no eval (F4).",
      "notes": "'every number' completeness is untested — eval 2 grades 2 of the source's 4 claims (F26)."
    },
    {
      "step": 4,
      "title": "Write the page in the schema.",
      "ends_in_something_checkable": "PARTLY — frontmatter fields are checkable; 'status from the fixed vocabulary' is NOT (the vocabulary is never given, F12); 'say what would make it wrong' is NOT (no criterion, F25)",
      "graded_by": "PARTLY — eval 1 grades one frontmatter element ('the new source with its fetch date in frontmatter'); eval 2 grades the disputed status. The body-section requirements, the hash, the vocabulary and the wrongness statement are graded by nothing.",
      "notes": ""
    },
    {
      "step": 5,
      "title": "Cascade.",
      "ends_in_something_checkable": "YES — 'the neighbour names it back with a sentence' is a concrete file state",
      "graded_by": "NOTHING. evals.md S4 is the only scenario that grades it, and S4 has no eval entry (F4). eval 1's 'the neighbour still names the owner' grades PRESERVATION of a link the fixture already has two-way, not the cascade action. Eval 2 touches local-models, whose `related:` is empty and which no note names — the one fixture where the cascade would be visible — and eval 2's expected_output says nothing about it.",
      "notes": "This is the step with the largest gap between a clear obligation and zero grading."
    },
    {
      "step": 6,
      "title": "Register.",
      "ends_in_something_checkable": "YES for SOURCES and LOG rows; the index row is checkable but contradicted (F8) and possibly overwritten by Step 7 (F11)",
      "graded_by": "evals.json eval 1 ('a SOURCES row and a LOG line'), eval 2 ('SOURCES and LOG rows'), eval 3 ('one LOG line'); evals.md S1, S5. The INDEX-row obligation is graded only NEGATIVELY, by S1 requiring INDEX unchanged.",
      "notes": "No eval or scenario ever requires an index row to be added, though Step 6 states it unconditionally."
    },
    {
      "step": 7,
      "title": "Lint, then rebuild the index.",
      "ends_in_something_checkable": "NO, as shipped — no lint tool, no index builder and no git repo exist in the fixture, and the eval prompts ask only to 'edit the wiki in place and list the files you changed', never to commit. The 'rebuild the index' half is not even instructed in the step body (F10).",
      "graded_by": "NOTHING. evals.md S1 asserts 'lint reports 0 errors' and S3 and S4 also depend on lint output, but the tool the Method names (kb.py lint --json) is absent from the artefact (F3), and the checker the evals name (check.py) does not exist (F1).",
      "notes": "The step also contradicts the Rule forbidding running code (F9)."
    }
  ],

  "summary": {
    "steps_ending_in_something_checkable": "2, 5 and 6 fully; 1, 3 and 4 partly; 7 not at all as shipped",
    "steps_graded_by_an_executable_check": "none — evals.json carries empty expectations throughout and names a checker that does not exist",
    "steps_graded_by_nothing_at_all_including_prose": "Step 5 (cascade) — the only prose grader is S4, which has no eval",
    "steps_graded_only_by_scenarios_that_were_never_implemented": "Steps 1, 3, 5 and 7",
    "highest_severity": "F1, F2 and F3 together: the suite cannot run and, if it did, would assert nothing. F5 and F6 are the sharpest internal contradictions — a verdict definition the artefact's own examples violate, and a mandatory field the schema has no slot for."
  }
}
```

**In short:** the suite is not runnable (a checker file named three times that does not exist, empty expectations everywhere, and a lint tool named as the sole criterion that is absent from the artefact), half the scenario list was never implemented, and the contradictions cluster around the verdict vocabulary (Step 3 defines MEASURED in a way the Example and S1 both violate) and the provenance schema (Step 1 mandates a content hash that Step 4's schema, every fixture and every expectation omit). Step 5, the cascade, is the only step with a clear obligation and no grader of any kind.