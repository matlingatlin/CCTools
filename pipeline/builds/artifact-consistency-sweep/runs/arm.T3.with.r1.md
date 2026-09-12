I read the method skill (`artifact-consistency-sweep`) and its `references/pair-vocabulary.md` first, then swept the artefact at `./artifact-C` (the directory named `artifact` in the prompt does not exist; `artifact-C` is the only artefact present).

**Inventory and plan counts** (written before the first verdict): 7 numbered steps · 3 rule bullets · 19 description clauses · 23 `evals/evals.json` expectations + 6 `evals.md` scenarios · 13 bundled files · no `bom.json` in the bundle, so bill-of-materials pairs were resolved against every file each document names (26 references).

**Pairs owed / examined:** step×rule 21/21 · step×step 21/21 · step×check 161/161 (evals.json) + 42/42 (evals.md scenarios) · description×body 19/19 · file×BOM 39/39 · claim×rationale 10/10. **Total 313 planned, 313 examined**; no pair type fell below its plan count.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md — Rules bullet 3 vs step 7",
      "finding": "The rule closes the action set to the wiki's own query, lint and index commands, but step 7 orders a git commit and makes the commit the landing point of the whole procedure. A run that obeys the rule cannot finish step 7; a run that finishes step 7 breaks the rule.",
      "quote": "It runs the wiki's own query, lint and index commands, and nothing else. / The fact and its lint pass land in one commit."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md — step 2 (no material branch) vs step 7",
      "finding": "The no-material branch ends the procedure with 'stop'. Step 6 was reconciled with that branch explicitly ('also on no material', 'in every branch'); step 7 was not, so it still reads as unconditional. Whether the no-material disposition lints, rebuilds the index and commits is answered two ways in one file, and eval 3 grades neither answer.",
      "quote": "keep the raw, write the source-log row and the operation-log line, touch no page, stop. / Lint, then rebuild the search index; fix what the lint names before committing."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md — step 3 vs step 4",
      "finding": "Step 3 permits claim rows to live in a wiki-level claims ledger instead of the page; step 4's schema requires the Claims table in every page unconditionally. A wiki with a ledger cannot satisfy both, and no expectation covers the ledger branch.",
      "quote": "The claim rows go in the page's `## Claims` table (step 4) or in the wiki's claims ledger where one exists. / Body: what it is; a `## Claims` table with one row per claim"
    },
    {
      "level": "CLASS",
      "where": "frontmatter description vs SKILL.md 'Not this skill'",
      "finding": "The body deliberately strips repo-local unit names and defers them to the In this repo section; the description then states five of those local names itself (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator). The description promises a boundary the body says it does not state, and carries repo-specific wiring into the portable half of the artefact.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening vs SKILL.md Rules bullets 2 and 3",
      "finding": "rationale.md asserts every rule in SKILL.md has an entry with its run or source, and that a rule without one does not belong. Rule 3 (installs nothing / no external code / only the wiki's own commands) has no entry at all; rule 2's 'nothing from memory' has no entry either — the quote-before-write bullet covers quoting, not memory. By rationale.md's own test those rules do not belong in the body.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 'new' + step 4 + step 6 vs evals/evals.json",
      "finding": "The description and step 2 promise four dispositions, but all three executable evals are update, disputed and no-material. The 'new' branch — creating a page in the schema (step 4) and adding the hand-written map-of-contents row (step 6) — is exercised by no eval, and check.py T1 actively penalises creating a page, so the only executable pressure on the new branch runs against it.",
      "quote": "**new** - no page owns the topic."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py, T3 branch (line 54) vs evals/evals.json eval 3 prompt",
      "finding": "The T3 'byte-identical to the fixture' check resolves the fixture to check.py's own sibling wiki/notes — the same directory the eval prompt tells the model to edit in place. before and after are hashes of one file, so the check cannot fail whatever the run does. This is the grader for S5/T3, the artefact's only measured win over baseline.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 5 vs evals/evals.json eval 1, expectation 8",
      "finding": "The only executable check on the cascade is that prompt-caching still names [[model-prices]] — already true of the unedited fixture, which ships that link in its body and its related: list. It grades non-regression, not the step; a run that performs no cascade at all passes it. evals.md S4, the scenario written for step 5, is 'pending'.",
      "quote": "prompt-caching still names [[model-prices]]"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 vs the bundle",
      "finding": "Step 1's last sentence is a definition, not an outcome: it names no file, row or state a reader could check, so the step ends in nothing observable. Nothing grades it either — all three evals hand the raw in pre-saved under evals/files/raw/, no expectation reads that directory, no expectation checks the raw is unedited, and no manifest exists in the bundle although the step and the In this repo section both require one.",
      "quote": "A transcript or frame text is the raw for a video or image."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 7 vs evals/evals.json (all three evals)",
      "finding": "No expectation covers the lint pass, the index rebuild or the commit. The fixture wiki ships no lint script, so step 7's by-hand fallback is the branch that actually applies in every eval — and nothing checks the log line for the statement it demands. The nearest expectation ('no dangling [[link]]; every note listed in INDEX.md') grades wiki state and passes on the unedited fixture.",
      "quote": "No lint script in this wiki? Check dangling links, unlisted pages and orphans by hand and say so in the log line."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs evals/files/check.py header",
      "finding": "evals.md names kb.py lint --json plus 'reading the note' as the observable criterion for every scenario. The grader actually bundled and named by all three evals is check.py, kb.py is not in the bundle, and check.py's contract explicitly excludes the judgement half of that criterion.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals/evals.json eval 1 expectation 4 and check.py T1",
      "finding": "The scenario requires the verdict MEASURED specifically; the expectation and the grader accept any of MEASURED|REPEATED|DERIVED. A run that grades a measured price REPEATED passes the executable check and fails the written criterion.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 Input vs evals/files/raw/2026-09-02-blog-restating-caching.md and rationale.md",
      "finding": "S5 says the blog restates three facts; the fixture blog restates two (0.1x read, 1.25x write) and rationale.md's before/after entry says two. The scenario describes a fixture that is not in the bundle.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 Input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "S1 says three per-MTok prices; the fixture page carries four (Alpha 5 input/output, Beta 5 input/output) plus two cache multipliers.",
      "quote": "a fetched vendor pricing page with three per-MTok prices"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs the per-scenario results",
      "finding": "The header states three arms at k=2; every executed scenario reports four arms (with, without, probe, incumbent) and the 'without' arm runs at k=1. The design line and the results line describe different runs.",
      "quote": "three arms, k=2, code grader, blinded, preregistered rule"
    },
    {
      "level": "CLASS",
      "where": "bundle vs the files the documents name (no bom.json present)",
      "finding": "The artefact ships no bill of materials, and four artefacts named as evidence or tooling are absent from it: the trigger matrix carrying S6's entire claim, knowledge/kb.py named as the grader, the raw/MANIFEST.md step 1 requires, and pipeline/CURATION-LESSONS.md in the failure triage. evals.md itself is pointed at by nothing in the bundle. The trigger matrix is the load-bearing one — it is the sole grade on the negative trigger and cannot be inspected.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py T1 'no rival page' vs evals/evals.json eval 1 expectation 1",
      "finding": "The expectation forbids any rival page; the check only rejects a new note whose filename contains 'pric'. A rival note named beta-5-costs or 2026-09-rates passes the check the expectation was written for.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals/evals.json eval 1 expectation 7 (and evals 2, 3)",
      "finding": "Step 6 requires the operation-log line to name three things — the disposition, the source URL and the pages touched. Every expectation checks the first two only; the pages-touched clause is graded by nothing in any of the three evals.",
      "quote": "one operation-log line naming the disposition, the source URL and the pages touched, in every branch."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 status enumeration vs steps 2-7 and all evals",
      "finding": "The schema offers four status values but only `disputed` has a step that sets it (cross-referenced to step 2). No step ever sets `outdated` or moves a page from `unverified` to `verified`, and no expectation covers either value — schema values with no step behind them.",
      "quote": "`status` - `verified` / `unverified` / `disputed` (step 2) / `outdated`"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": false,
      "graded_by": "nothing. The step's last sentence is a definition naming no observable state; no expectation in any of the three evals reads evals/files/raw/, checks a raw manifest, or checks that the raw is unedited."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "update branch: eval 1 'model-prices is the page updated; no rival page' (check.py T1 no rival page). disputed branch: eval 2 'a row is marked disputed and the page status is disputed'. no-material branch: eval 3 'no new note' + 'LOG.md says no material and names the blog' + 'SOURCES.md has a row for the blog' — but its companion 'byte-identical to the fixture' check is vacuous (finding 7). new branch: nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 'a claims-table row carries the verbatim raw line and a verdict word' (check.py T1 claim_rows, requiring the verbatim price line and a verdict on one line); eval 2 'a claims row carries 753B, the card's verbatim line and a verdict word' and 'a claims row carries 744B and a verdict word'. Grades that a verdict word is present, never that the right one was chosen; the ledger alternative is graded by nothing."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "eval 1 'a Beta 5 row carries $2, $10 and a 2026-09 date', 'the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row', 'the new source with its fetch date is in model-prices' frontmatter'; check.py's common schema:<stem> check for the five required frontmatter keys; eval 2 'a row is marked disputed and the page status is disputed'. Page creation, the `outdated`/`unverified` values, and 'every price, version, limit, count and date in the body carries its as-of date' beyond the two Beta 5 rows: nothing."
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "nothing executable. The step's last sentence ('No true sentence, no edge.') names no observable outcome, and the only expectation pointed at the cascade — eval 1 'prompt-caching still names [[model-prices]]' — is already true of the unedited fixture. evals.md S4, written for this step, has Result: pending."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "eval 1 'SOURCES.md has a row for the pricing page' + 'LOG.md has a line naming the source and update'; eval 2 'SOURCES.md has a row for the card' + 'LOG.md names the card and disputed'; eval 3 'LOG.md says no material and names the blog' + 'SOURCES.md has a row for the blog'. The 'pages touched' clause and the new-page map-of-contents row: nothing."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing. No expectation covers the lint pass, the index rebuild or the commit, and no eval runs in a repository. The by-hand fallback is the branch that applies (the fixture wiki ships no lint script) and its log-line requirement is unchecked. The 'every note keeps its frontmatter; no dangling [[link]]; every note listed in INDEX.md' expectation grades wiki state, passes on the unedited fixture, and is a regression guard rather than a grade on this step."
    }
  ]
}
```