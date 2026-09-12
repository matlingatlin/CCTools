```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals (ids 1, 2, 3)",
      "finding": "Every eval carries an empty expectations array, so no eval in the runnable suite grades anything programmatically. The only grading content is the prose expected_output field. Combined with evals.md's \"Result: pending\" on all six scenarios, no step in the skill is graded by anything that has been or can be executed as written.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json files lists (ids 1, 2, 3) vs the shipped bill of materials",
      "finding": "All three evals declare evals/files/check.py as a bundled input file, but no check.py exists anywhere in the artefact (evals/files contains only raw/ and wiki/). The one file that would make the empty expectations executable is the one that is missing.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S1–S6 vs evals/evals.json",
      "finding": "The two eval documents define non-corresponding suites: evals.md declares six scenarios, evals/evals.json runs three (matching S1, S2, S5 only). S3 (edge, video transcript), S4 (pressure, cascade) and S6 (the required negative-trigger) exist only as prose in evals.md and have no runnable eval, so the steps they alone grade (steps 1, 3, 5) are graded by nothing runnable.",
      "quote": "### S6 — a claim to bundle into a skill · negative-trigger"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md \"Method\" vs evals/files/ and SKILL.md's portability claim",
      "finding": "The method names a repo-specific script as the observable criterion for every scenario, but no kb.py or any lint is bundled in the artefact and the fixture wiki at evals/files/wiki contains no lint tool, no schema file and no build script. The grader named for all six scenarios does not exist in the artefact, and it is a project-specific tool used to grade a talent the body presents as portable.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals.md header line",
      "finding": "Step 2 cites a measured baseline observation dated 2026-09-02 (\"every baseline run ... still edited the owning page\"), but the eval suite dated the same day states it has never been run and every scenario Result is pending. The skill asserts an experimental result its own eval file says was never produced.",
      "quote": "Observed 2026-09-02: without this rule, every baseline run on a restating blog post still edited the owning page (a second source plus a claims row), so \"no material\" quietly became \"update\"."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals.md S5 Baseline",
      "finding": "The two documents state contradictory baseline behaviour for the same restating-blog-post scenario: step 2 says the baseline edits the existing owning page (second source plus claims row), S5 says the baseline writes a new thin note. The pass criterion \"no page changed\" only distinguishes the talent from one of these two baselines.",
      "quote": "- **Baseline:** writes a thin note anyway."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals.md S1 pass criterion (and evals/evals.json id 1)",
      "finding": "Step 6 requires an index row unconditionally on every ingest, but S1 (an update-triage ingest) requires the index to be unchanged, and evals.json id 1 says only \"a SOURCES row and a LOG line\". The step and the eval demand opposite states of INDEX.md, and no eval grades the index at all.",
      "quote": "**Register.** One row in the index (map of contents), one row per source in the source log, one entry in the operation log saying what was ingested and what it changed."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs step 7 (and the \"In this repo\" instance)",
      "finding": "Step 6 has the agent hand-write a row into the index; step 7 then rebuilds the index. Whether the index is authored or generated is left contradictory, and the repo instance asserts both (\"register in `knowledge/INDEX.md`\" and \"rebuild with `kb.py build`\"). A hand-written row that a rebuild regenerates or discards cannot be checked as step 6 states it.",
      "quote": "**Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names before committing."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals.md S4 pass criterion",
      "finding": "Step 5 requires the back-link unconditionally (\"For every neighbour the page names, make the neighbour name it back\"), but S4 passes an outcome step 5 forbids: committing with one-way links as long as the commit message explains them. The eval accepts a defection the step prohibits, so step 5 is graded by a criterion weaker than itself.",
      "quote": "each neighbour gains a sentence naming the new page back before the commit, or the commit message states which neighbours were left one-way and why; lint's one-way count for the new page is 0 or explained"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S4 \"With talent\" vs SKILL.md steps 5 and 6",
      "finding": "S4 credits \"an explicit deferral in the log\" as a passing with-talent behaviour, but no step in SKILL.md defines a deferral: step 5 admits no deferral and step 6's operation-log entry is specified only as \"what was ingested and what it changed\". The eval grades against a mechanism the body never provides.",
      "quote": "- **With talent:** step 5 or an explicit deferral in the log."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 Input vs evals/files/raw/2026-09-02-blog-restating-caching.md and SKILL.md's example",
      "finding": "S5 describes the fixture as restating three facts; the actual raw file restates two (0.1x cache read, 1.25x cache write), and SKILL.md's own worked example says two multipliers. The scenario description does not match the fixture it is supposed to describe.",
      "quote": "- **Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 Input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "S1 describes three per-MTok prices; the fixture page carries four prices (Alpha 5 in/out, Beta 5 in/out) plus two cache multipliers, and only Beta's two prices actually differ from the note. The pass criterion (\"the owning note gains a dated row\", singular) does not match the fixture's changed-price count, and nothing says what must happen to Alpha's unchanged prices.",
      "quote": "- **Input:** a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json ids 1 and 2 vs SKILL.md step 2's no-material rule",
      "finding": "Both source fixtures mix new claims with claims the wiki already holds — the pricing page restates prompt-caching's 10%/125% multipliers, and the gamma model card restates local-models' 245 GB while adding untouched new claims (40B active, 1M context). Step 2 requires a no-material verdict for the already-held values and an update for the new ones from the same source, but neither expected_output says whether prompt-caching may be touched or what becomes of the unmentioned new claims. The step's hardest case is present in the fixtures and graded by nothing.",
      "quote": "Cache reads are billed at 10% of the input price; cache writes at 125%."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (\"status from the fixed vocabulary\") vs evals.md S2 / evals.json id 2 / the fixture notes",
      "finding": "The \"fixed vocabulary\" of statuses is never enumerated anywhere in the artefact — no references/ file, no schema is bundled, and the only pointer is a repo-internal contract file. The fixtures use `status: verified` and the evals require the page \"marked disputed\", but whether that is a frontmatter status value or a line-level marker is left undefined, so step 4's frontmatter cannot be checked.",
      "quote": "status from the fixed vocabulary, tags, related"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 4's source schema",
      "finding": "S3 grades on a source entry of kind `note:`, but step 4 defines a source as (url or path, fetch date, note) — where \"note\" is a descriptive field on a url/path source, not a source kind. The eval requires a source shape the schema step does not define.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 7 and the \"In this repo\" section",
      "finding": "S3 grades on lint severity levels (INFO vs ERROR) that the artefact never defines: step 7 lists the lint's checks with no severities, and the repo instance describes lint only as exiting 1 on errors. The criterion cannot be evaluated from anything the artefact ships.",
      "quote": "lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules vs step 7 and the \"In this repo\" section",
      "finding": "The rule states the skill never runs external code, while step 7 mandates running the wiki's deterministic lint and the repo instance names two commands to execute (`kb.py lint`, `kb.py build`). The security rule and the mandatory final step contradict each other.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (\"and stop\") vs step 7 and evals.md Method",
      "finding": "The no-material branch stops after the log line, skipping steps 4–7 including the lint, yet step 7 states lint accompanies every landed fact and the eval method claims the lint is the observable criterion for every scenario including S5. The no-material path is exempt from the check the method says grades it.",
      "quote": "**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts (ids 1, 2, 3)",
      "finding": "Step 7 ends in a commit-level condition, but every eval prompt asks only for in-place edits and a list of changed files, and the fixture wiki is not a repository. The final clause of the last step is unobservable in the harness that is supposed to grade it — as is S4's commit-message criterion.",
      "quote": "A verified fact and its lint pass land in the same commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md \"When to use\" second bullet vs steps 1 and 3",
      "finding": "The trigger list admits a compiled summary page written back from a query over several notes — a case with no fetched source, so step 1 (keep the raw bytes with URL/fetch date/hash) and step 3 (locate every number in the raw, no quote no finding) cannot be executed for it. The admitted case has no procedure and no eval.",
      "quote": "An existing note is being extended with a new source, or a compiled summary page is being written back from a query over several notes."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S2 Input vs evals/files/wiki/notes/local-models.md and SOURCES.md",
      "finding": "S2 says the existing 744B value comes from the vendor's README, and the note body says the same, but the note's frontmatter source and the SOURCES row both attribute it to https://example.test/gamma-card — a model card, i.e. the same kind of source as the contradicting one. The fixture contradicts itself about the provenance the disputed-rows criterion depends on.",
      "quote": "Gamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md \"In this repo (one instance)\" vs the shipped bundle (no references/)",
      "finding": "The claim-row fields the skill's step 3 and step 4 rely on are said to live in a project-internal contract file, and no references/ directory is shipped. Outside this repo the artefact carries no definition of the claim row or the page schema, so steps 3 and 4 have no checkable specification travelling with the skill.",
      "quote": "the schema is this file plus `CLAUDE.md`'s \"verified fact lands the same turn\" rule and `pipeline/contracts/claims.contract.json` (the claim-row fields and the three verdicts)"
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios S1–S6",
      "finding": "The declared baseline-vs-with method is applied unevenly across scenario entries: S1, S2 and S4 carry a \"With talent\" line, S3 and S5 carry a Baseline but no \"With talent\", and S6 carries neither. The comparison the method says every scenario runs is not written for half of them.",
      "quote": "Baseline-vs-with per scenario; PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expected_output vs SKILL.md step 3 and evals.md S1",
      "finding": "S1 grades the verbatim line and the MEASURED verdict; the corresponding runnable eval's expected_output drops both, grading only dated rows, the kept superseded price, frontmatter source, SOURCES and LOG. Step 3 — the quote-before-write rule that the description leads with — is not graded by any runnable eval.",
      "quote": "The owning note (model-prices) is updated in place: a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter; no new page; a SOURCES row and a LOG line; the neighbour still names the owner."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expected_output (\"the neighbour still names the owner\") vs SKILL.md step 5",
      "finding": "The only cascade check in the runnable suite is satisfied by the fixture before any edit is made — prompt-caching.md already carries related: [[model-prices]] and a body sentence naming it — so it passes without the agent performing step 5. Step 5's actual requirement (the neighbour gains a sentence saying why) is graded by no check that can fail.",
      "quote": "Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "Nothing runnable. No eval prompt or expected_output in evals/evals.json mentions the raw layer, and the fixture wiki has no raw/ directory, so 'the copy goes there with the fetch date in the file name and a content hash' is never exercised. evals.md S3 is the only criterion touching it and has no corresponding eval."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals/evals.json id 1 (update triage), id 2 (disputed triage), id 3 (no material) — but through prose expected_output only, since expectations is empty; evals.md S1/S2/S5, all Result: pending. The mixed-source case (a source carrying both new and already-held claims, present in fixtures 1 and 2) is graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "Nothing runnable. evals.md S1 ('the verbatim line and MEASURED') and S3 ('claims from it are REPEATED, not MEASURED') are the only criteria; the runnable evals' expected_output never mentions a verbatim line or any of the three verdicts, and S3 has no runnable eval."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "Partially: evals/evals.json id 1 ('the new source with its fetch date in frontmatter') and id 2 ('the note marked disputed at that fact'). Not checkable as written because the 'fixed vocabulary' of statuses is never enumerated in the artefact, the required body sections ('what is still open', 'say what would make it wrong') have no criterion, and no schema file is bundled."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "evals/evals.json id 1 only, as 'the neighbour still names the owner' — a condition the fixture already satisfies before any edit, so it cannot fail. evals.md S4 grades it properly but has no runnable eval and accepts an outcome (one-way links plus a commit-message explanation) that step 5 forbids."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals/evals.json id 1 and id 2 ('a SOURCES row and a LOG line'), id 3 ('one LOG line saying no material with the source URL'). The index row required by step 6 is graded by no eval and is contradicted by evals.md S1's 'INDEX unchanged'."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "Nothing. No lint or build tool is bundled and none exists in evals/files, so 'lint reports 0 errors' (S1) and the lint severity levels (S3) cannot be evaluated; the closing 'same commit' condition is unobservable because every eval prompt asks only for in-place edits and a list of changed files, and the fixture is not a repository."
    }
  ]
}
```