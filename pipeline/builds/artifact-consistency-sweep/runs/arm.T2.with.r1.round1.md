**Plan counts (before any verdict):** step×rule 28 · step×step 13 · step×check 210 · description×body 21 · file×BOM 25 · claim×rationale 19 — total 316 rows owed. Basis: 7 numbered steps, 4 rule bullets, 21 description clauses, 30 expectations in `evals/evals.json`, 13 files present, 12 bill-of-materials rows (there is **no `bom.json` in the artefact**; the BOM was reconstructed from every file the artefact names as bundled — `references/rationale.md`, `evals/files/wiki`, the 3 `evals/files/raw/*` paths, `check.py`, `knowledge/kb.py`, the trigger matrix, `raw/MANIFEST.md`, `pipeline/CURATION-LESSONS.md`, `intake/`), 15 imperative step sentences.

**Ledger (plan / examined / non-consistent):** step×rule 28/28/2 · step×step 13/13/2 · step×check 210/210/4 · description×body 21/21/1 · file×BOM 25/25/3 · claim×rationale 19/19/1. Shortfall disclosed: step×check was ruled per step against the full 30-expectation set (7 groups), so 210 pairs were examined but only 7 step rows plus the non-consistent pairs were written out; no other type has a shortfall.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json (all 3 evals, 20 expectations) vs the bundle",
      "finding": "Every substantive expectation is delegated to a grader named check.py, and no check.py exists anywhere in the artefact (files present: SKILL.md, evals.md, evals/evals.json, references/rationale.md, 3 raw fixtures, 6 wiki fixtures). The named grader is absent, so 20 of 30 expectations grade nothing.",
      "quote": "\"check.py T1: no rival page\" ‖ \"check.py T3: SOURCES row for the consulted source\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules vs steps 2 and 7 and 'In this repo', and evals.md Method",
      "finding": "A rule forbids what two steps order. The rule says the skill runs nothing, while step 2 orders querying the index, step 7 orders running the lint and rebuilding the search index, the repo section gives the commands to run, and the eval method claims the criterion is checked by running kb.py.",
      "quote": "\"This skill installs, fetches and runs nothing; it is a writing discipline.\" ‖ \"**Lint, then rebuild the search index;** fix what the lint names before committing.\" ‖ \"lint `python3 knowledge/kb.py lint`; rebuild `kb.py build`.\""
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening vs SKILL.md ## Rules",
      "finding": "The rationale asserts it carries every rule with its evidence, but three of the four rules appear nowhere in it: the null/0 rule, the nothing-from-memory rule, and the installs/fetches/runs-nothing rule. By the rationale's own test those three 'do not belong in the body'; the rewrite moved the rationale out and left the rules behind unbacked.",
      "quote": "\"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\" ‖ \"`null` for not-fetched and not-measured; `0` only for a measured zero.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 1, 5, 7 vs evals/evals.json expectations",
      "finding": "The executed expectations grade only steps 2, 3, 4 and 6. Nothing grades step 1's content hash or raw/MANIFEST.md (the fixture wiki has no MANIFEST.md at all), nothing grades step 5's negative branch, and nothing grades step 7's index rebuild, its hand-check log line, or its one-commit requirement — the eval prompts never commit, they say to edit in place and list files.",
      "quote": "\"with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`.\" ‖ \"If no true sentence exists, do not add the edge.\" ‖ \"The fact and its lint pass land in one commit.\" ‖ \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "CLASS",
      "where": "evals.md Method and 'Not executed' section vs the bundle",
      "finding": "Three further graders/artefacts are named and none is bundled: knowledge/kb.py (claimed as the criterion for EVERY scenario, and absent from evals/files, so the stated check cannot run against the fixtures), the trigger matrix said to carry S6's claim, and pipeline/CURATION-LESSONS.md.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\" ‖ \"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5, vs evals/files/wiki/notes/model-prices.md and evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The check labelled 'beta price updated with date' asserts the literal row that is ALREADY in the untouched fixture. The raw page prices Beta 5 at $2.00/$10.00 effective 2026-09-01, so the check passes on a wiki nobody edited and fails on a correct update — it grades the opposite of its label and of S1's pass criterion.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\" ‖ \"Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules bullet 2 vs steps 1-7 and evals/evals.json",
      "finding": "A rule no step could obey and no check could grade: no step writes a field that can hold null or 0, the step 4 schema names none, and no expectation inspects a null or a zero.",
      "quote": "\"`null` for not-fetched and not-measured; `0` only for a measured zero.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 7",
      "finding": "The no-material branch orders a stop after editing the source log and the operation log, but step 7 requires the lint to pass in the same commit as any change. The branch commits two edited files with no lint, and step 7 is unreachable from it; step 6 was reconciled to the branch ('also on no material') while step 7 was not.",
      "quote": "\"keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop\" ‖ \"The fact and its lint pass land in one commit.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4",
      "finding": "The term 'disputed' is defined at two scopes and no line reconciles them: step 2 marks it at the contradicted fact, step 4 makes it one of four page-level frontmatter status values. Eval 2's 'disputed marker' expectation does not say which, and the fixture note carries status: verified.",
      "quote": "\"**disputed** (the source contradicts a page: keep both values as dated rows with their sources, mark the page `disputed` there)\" ‖ \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals/evals.json eval 3 and its fixture",
      "finding": "The no-material test as written selects the wrong branch on the fixture it is graded against: the blog is fetched 2026-09-02, newer than prompt-caching's 2026-08-20 source, so 'no newer date for any page' is false, yet eval 3 requires the no-material disposition.",
      "quote": "\"**no material** (no claim, no value, no newer date for any page\" ‖ \"No page changed and no page created; one LOG line saying no material with the source URL.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 3: expected_output vs its own expectations list",
      "finding": "The expected output describes only the LOG line and no page change, but the expectations also require a SOURCES row for the consulted source — a grader reading the expected output would mark a run correct that skipped the source-log row step 2 and step 6 both order.",
      "quote": "\"No page changed and no page created; one LOG line saying no material with the source URL.\" ‖ \"check.py T3: SOURCES row for the consulted source\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S6",
      "finding": "The method claims a file-state criterion for every scenario, but S6 is a negative trigger whose criterion is that no file is touched and a different skill fires — a criterion no file state can express.",
      "quote": "\"The observable criterion for every scenario is the state of the files\" ‖ \"this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S5 heading and result",
      "finding": "The method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails and gives normal scenarios a plain PASS, yet S5 is classified normal and carries the Beats-baseline verdict — the one measured win is recorded against the grading rule the same file sets.",
      "quote": "\"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\" ‖ \"### S5 — no material · normal\" ‖ \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs S1/S2/S5 run lines",
      "finding": "The header states three arms at k=2; every executed scenario reports four arms (with, without, probe, incumbent) and the 'without' arm ran k=1, not k=2.",
      "quote": "\"three arms, k=2, code grader, blinded, preregistered rule\" ‖ \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says the blog restates three facts held with the same sources; the rationale and the fixture both have two multipliers, and the blog's URL is a different source from the note's.",
      "quote": "\"a blog post restating three facts the wiki already holds with the same sources.\" ‖ \"on a blog post restating two multipliers a note already held\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md steps 1 and 4 and step 7",
      "finding": "S3's pass criterion depends on two things the body does not provide: a source entry with no url or path (step 4's schema requires url or path, step 1 requires URL or path for the raw), and lint severity levels INFO vs ERROR that no step, rule or reference defines.",
      "quote": "\"the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR\" ‖ \"frontmatter `title`, `sources` (url or path, fetched, note)\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs step 1",
      "finding": "The description admits a 'measurement' (and a 'repo') as an ingestible source, but the body's raw rule assumes fetched bytes with a URL or path, a fetch date and a hash, and its only widening clause covers video and image. A measurement you made yourself has no step that says what its raw is, and no eval covers one.",
      "quote": "\"Use when a fetched page, paper, repo, transcript or measurement is about to become a note\" ‖ \"A transcript or frame text is the raw for a video or image.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4, closing sentence",
      "finding": "The step closes on an instruction that names no file, row, number or state, so the step ends in nothing checkable; the schema clause before it is graded, the dating clause is not.",
      "quote": "\"Date what will move.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'In this repo (one instance)'",
      "finding": "A directory is named as part of the raw layer and nothing else in the artefact defines, uses or checks it — no step, no rule, no rationale bullet, no expectation mentions intake.",
      "quote": "\"raw `knowledge/raw/` (`MANIFEST.md`) and `intake/`\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded — no expectation names the raw, the content hash or raw/MANIFEST.md, and the fixture wiki has no MANIFEST.md; the raw files exist in the fixture before the run, so nothing observes that the step ran"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "eval 3: 'check.py T3: prompt-caching unchanged', 'check.py T3: no new note', 'check.py T3: LOG says no material', 'check.py T3: SOURCES row for the consulted source'; eval 1 'check.py T1: no rival page' (update branch); eval 2 'check.py T2: disputed marker' (disputed branch) — all four via the absent check.py"
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 and eval 2: 'check.py T1/T2: verdict word per claim' and 'quote from the raw/card on the page'; the DERIVED verdict and the locator column are graded by nothing"
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "the schema clause is graded by 'every note keeps title/status/tags/related/sources frontmatter' (all 3 evals) and 'check.py T1/T2: new source in note frontmatter with fetch date'; the closing sentence 'Date what will move.' is ungraded"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "positive branch only: eval 1 'check.py T1: neighbour names owner back' and 'no dangling [[link]]'; the closing exception (do not add an untrue edge) is ungraded, and S4 which would grade it is pending"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "eval 1/2 'check.py T1/T2: SOURCES row' and 'LOG row'; eval 3 'check.py T3: LOG says no material' and 'SOURCES row for the consulted source'; the map-of-contents row is covered only by 'every note is listed in INDEX.md'"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "ungraded — 'no dangling [[link]]' and 'every note is listed in INDEX.md' grade a lint-clean end state, but nothing grades the index rebuild, the one-commit requirement (no eval commits), or the hand-check log line, which is the live branch since no lint script is bundled"
    }
  ]
}
```