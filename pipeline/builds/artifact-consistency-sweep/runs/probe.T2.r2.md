```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json (all three evals) vs the bundled file list",
      "finding": "Every code-grader expectation delegates to a script `check.py` that is not in the artefact — 24 of the 31 expectations across evals 1-3 are graded by a file the bundle does not contain, so no step is actually graded by executable code. The bundle holds only SKILL.md, references/rationale.md, evals.md, evals/evals.json and the fixture wiki/raw.",
      "quote": "\"check.py T1: no rival page\", \"check.py T2: disputed marker\", \"check.py T3: LOG says no material\""
    },
    {
      "level": "CLASS",
      "where": "evals.md '## Method' vs evals/evals.json expectations vs evals/files/wiki/",
      "finding": "The two eval documents name two different graders and neither exists. evals.md says the observable criterion is checked by `knowledge/kb.py lint --json` — a path from SKILL.md's 'In this repo' instance, not from the fixture; the fixture wiki at evals/files/wiki contains no lint script at all, and evals.json instead grades through check.py. A scenario's criterion therefore cannot be evaluated as either document describes it.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json evals 1-3 vs SKILL.md steps 2, 4 and 6",
      "finding": "No eval exercises the 'new' branch: all three fixtures resolve to update, disputed and no material, and two expectations actively assert that no page is created. So triage's 'new' disposition, step 4's schema applied to a freshly written page, and step 6's map-of-contents row for a new page are graded by nothing. The only INDEX expectation guards notes that already exist.",
      "quote": "\"check.py T1: no rival page\" / \"check.py T3: no new note\" vs SKILL.md step 6: \"a row in the hand-written map of contents for a new page\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json expectations vs evals/files/wiki/ starting state",
      "finding": "Several expectations are already true of the fixture before any agent runs and cannot fail: 'every note is listed in INDEX.md', 'no dangling [[link]]', 'every note keeps ... frontmatter', and 'neighbour names owner back' (prompt-caching.md already carries related: [[model-prices]] and links it in the body). The cascade step is graded ONLY by such a pre-satisfied check.",
      "quote": "check.py T1: neighbour names owner back"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 vs evals/ (fixtures and expectations)",
      "finding": "Step 1 is unexercised and ungraded end to end. Each eval prompt hands the agent a raw file that is already saved, and no expectation anywhere mentions a raw/ directory, a MANIFEST row, a fetch date recorded at save time, or a content hash. rationale.md makes MANIFEST.md a hard requirement that nothing in the bundle checks.",
      "quote": "Save the source bytes where the wiki can re-read them, never edited, with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md '## Rules' vs SKILL.md step 7 and 'In this repo'",
      "finding": "The rule says the skill runs nothing, but step 7 mandates running a lint, rebuilding a search index and landing a commit, and the instance section gives the commands. Step 1's content hash is likewise a computation. The rule and the step cannot both hold.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline. / fix what the lint names before committing. The fact and its lint pass land in one commit. / lint `python3 knowledge/kb.py lint`; rebuild `kb.py build`."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expectation vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The expectation labelled 'beta price updated' quotes the PRE-INGEST row. The raw says Beta 5 is now $2/$10 effective 2026-09-01, so the literal being asserted is the value the ingest is supposed to supersede — it duplicates the separate 'old price kept as history' expectation, and the new price is graded by nothing. A run that changes nothing at all in that table passes this check.",
      "quote": "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says the blog restates three facts; the rationale and the fixture both hold two (0.1x cache read, 1.25x cache write). The 'same sources' claim also fails: the blog's URL is example.test/blog/caching-explained while prompt-caching.md's source is example.test/caching.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources. vs rationale.md: \"a blog post restates two multipliers a note already carries with a dated source\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 pass criterion vs SKILL.md step 2 and evals/evals.json eval 3",
      "finding": "Step 2's no-material branch requires three outcomes (raw kept, source-log row, operation-log line); S5's pass criterion drops the source-log row and the kept raw, so a run that skips the SOURCES row passes S5 as written while failing the step and failing eval 3's expectation. The written criterion and the executable expectation disagree.",
      "quote": "**Pass criterion:** no page changed; an operation-log entry says \"no material\" with the URL and date. vs step 2: \"keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Method' vs evals.md S5 heading and result",
      "finding": "The method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails, and S5 is tagged 'normal' — yet S5 is the one scenario awarded that verdict. Either the tag or the method sentence is wrong; as written the only measured win is recorded in violation of the stated rule.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails. vs \"### S5 — no material · normal\" ... \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs SKILL.md '## When to use' / 'Not this skill'",
      "finding": "The description excludes five siblings; the body's exclusion list carries only four — deep-reading, the nearest neighbour and the one most likely to mis-fire on 'summarise this source', is dropped from the body. No eval covers it either (the only negative trigger, S6, tests skill-knowledge and is pending).",
      "quote": "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation) vs body: \"**Not this skill:** claims bundled into a skill's `references/` (`skill-knowledge`); agent task state (`unified-memory`); a document a code change made false (`doc-claim-reconciliation`); cleaning the whole wiki (`kb-curator` agent).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 4",
      "finding": "S3 requires a source entry with no URL and no path, but step 4's schema makes url-or-path mandatory for every source. S3 also grades on a lint severity distinction (INFO vs ERROR) that no part of SKILL.md, rationale.md or the bundle defines, so the criterion is unresolvable even if a lint existed.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR vs step 4: \"frontmatter `title`, `sources` (url or path, fetched, note)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Not executed in the first build' vs evals.md S6",
      "finding": "The same paragraph says S6 has no executable eval and then reports measured numbers for the claim it makes; S6's own Result line says pending. The trigger matrix those numbers come from is not in the bundle, so the figures are unverifiable from the artefact.",
      "quote": "S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet; S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The scenario describes three per-MTok prices; the fixture page carries four (two models x input/output) plus two cache multipliers, and only one model's prices actually changed. The scenario's description of its own input does not match the input.",
      "quote": "**Input:** a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S2 vs evals/files/wiki/notes/local-models.md and evals/files/wiki/SOURCES.md",
      "finding": "S2 attributes the incumbent 744B to the vendor's README, but the fixture note's frontmatter and the SOURCES row record only example.test/gamma-card as its source. The starting state carries a claim whose cited source appears in no frontmatter and no source-log row — the exact defect step 3 and step 6 exist to prevent, inside the fixture the eval guards.",
      "quote": "the wiki's note says 744B from the vendor's README vs local-models.md: \"Gamma-7 has 744B total parameters (README, 2026-08-25)\" with \"- url: https://example.test/gamma-card\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4 vs evals/evals.json eval 2",
      "finding": "Two different places are named for the disputed marker — inline at the contested line (step 2) and the frontmatter status enum (step 4) — and the expectation that grades it names neither, while the per-eval invariant requires the frontmatter status field to survive. A run marking only one of the two locations cannot be adjudicated.",
      "quote": "mark the page `disputed` there vs step 4: \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\" vs \"check.py T2: disputed marker\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/files/wiki/ and evals/evals.json",
      "finding": "The fixture wiki has no lint script, so every eval run must take step 7's fallback branch and say so in the log line — yet no expectation checks for that statement, and evals.md's Method asserts the opposite, that a lint is run. The branch the evals actually trigger is the one branch nothing grades.",
      "quote": "No lint script? Hand-check dangling links, unlisted pages and orphans, and say so in the log line."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md '## Rules' (lines 47-48)",
      "finding": "Two rules are attached to no step and to no check. No step writes a nullable or numeric field, so the null/0 rule can never be exercised or violated; 'the wiki never the only copy of a fact' names no observable artefact at all. By rationale.md's own standard for the body, a rule with nothing behind it does not belong there.",
      "quote": "Raw never edited; the wiki never the only copy of a fact. / `null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 vs SKILL.md step 2 (no material)",
      "finding": "The T1 pricing raw also restates prompt-caching's 10%/125% multipliers verbatim — a no-material sub-case sitting inside an update case, exactly the collision the skill's hardest rule addresses. Eval 1 has no expectation that prompt-caching.md is left untouched, so the behaviour graded in T3 is ungraded in the one scenario where it competes with an update.",
      "quote": "Cache reads are billed at 10% of the input price; cache writes at 125%. vs prompt-caching.md: \"Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 3 vs the per-scenario result lines",
      "finding": "The header reports three arms; each executed scenario reports four distinct run labels (with, without, probe, incumbent), and 'without' is run at k=1 while the header states k=2. The arm count and the repeat count in the summary do not match the data below them.",
      "quote": "the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule) vs \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 3 ('Type') vs evals.md S4 and S6",
      "finding": "The talent is typed as carrying one discipline pressure test, and the method claims a preregistered, blinded measurement — but the single pressure scenario (S4) and the single negative trigger (S6) were never executed, so the type line describes coverage the eval record does not have.",
      "quote": "**Type:** technique (with one discipline pressure) ... **Verdict:** ITERATE vs \"**Result:** pending\" on S3, S4 and S6"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "Nothing. No expectation in evals/evals.json mentions raw/, MANIFEST.md, a recorded fetch date or a content hash; all three fixtures ship the raw already saved, so the step is never performed during an eval. The only written criterion for it (evals.md S3, 'the transcript text is saved as the raw') has no executable eval."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "The chosen disposition is graded indirectly: update by 'check.py T1: no rival page'; disputed by 'check.py T2: both values present' + 'disputed marker'; no material by 'check.py T3: prompt-caching unchanged' + 'no new note' + 'LOG says no material' + 'SOURCES row for the consulted source'. The 'new' disposition and the mandated index query itself are graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "'check.py T1: quote from the raw on the page' + 'check.py T1: verdict word per claim', and the T2 equivalents. The locator field, the 'every number, date and quote' completeness requirement and the DERIVED verdict are graded by nothing — no fixture contains a derived figure."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "The per-eval invariant 'every note keeps title/status/tags/related/sources frontmatter', plus 'check.py T1: new source in note frontmatter with fetch date' and 'check.py T2: model card in frontmatter sources'. The prescribed body sections (what it is / claims graded / what it means here / what is open) and 'Date what will move' are graded by nothing, and since no eval creates a page the schema is only ever checked against notes the fixture already supplied."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "Only 'check.py T1: neighbour names owner back' — a check the fixture satisfies before the run (prompt-caching.md already declares related: [[model-prices]] and links it in prose), so it cannot fail and grades nothing the agent does. S4, the scenario written for this step, has no executable eval. The clause 'If no true sentence exists, do not add the edge' is a judgement no check in the bundle can make."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "'check.py T1/T2: SOURCES row' and 'LOG row'; 'check.py T3: LOG says no material' and 'SOURCES row for the consulted source'. The first of the three registers — the hand-written map-of-contents row for a new page — is graded by nothing, because no eval creates a page; 'every note is listed in INDEX.md' only guards the pre-existing three."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "Nothing, and it cannot be. No lint script is bundled and the fixture wiki has none, so 'lint reports 0 errors' has no referent; the index rebuild has no target in the bundle; and the eval prompts end at 'list the files you changed', so the single-commit requirement is outside anything the harness can observe. evals.md's Method claims this step's checker is `knowledge/kb.py lint --json`, which is not in the artefact."
    }
  ]
}
```