```json
{
  "counts": {
    "inventory": "7 steps, 4 rules, ~18 description clauses, 3 evals.json entries with 30 expectations (21 of them check.py rows), 6 evals.md scenarios (3 executed), 13 bundled files, 8 rationale bullets",
    "step_x_rule": "28 planned / 28 examined",
    "step_x_step": "21 planned / 21 examined",
    "step_x_check": "210 planned (7 steps x 30 expectations) / 210 examined; plus 42 (7 x 6 evals.md scenarios) examined",
    "description_x_body": "18 planned / 18 examined",
    "file_x_bom": "19 planned / 19 examined (13 present + 6 named-not-present, both directions)",
    "claim_x_rationale": "11 planned / 11 examined (4 rules + 7 steps against 8 rationale bullets)"
  },
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md Rules bullet 4 vs steps 2 and 7 (and the description clause 'lint')",
      "finding": "A rule forbids what two steps order. The rule says the skill runs nothing, while step 7 orders running the lint and rebuilding the search index and step 2 orders querying the index (by command, per 'In this repo'). The description also promises 'lint'. Either the rule is false or steps 2 and 7 are unobeyable.",
      "quote": "\"This skill installs, fetches and runs nothing; it is a writing discipline.\" / \"**Lint, then rebuild the search index;** fix what the lint names before committing.\" / \"query the wiki's index for the title, trigger terms and URL\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules bullets 3 and 4",
      "finding": "Two rules contradict each other inside the same block: one orders looking a value up (a fetch), the other says the skill fetches nothing.",
      "quote": "\"Nothing about a tool, price, version or limit from memory: look it up and date it.\" vs \"This skill installs, fetches and runs nothing; it is a writing discipline.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules bullet 2 vs all seven steps and all 30 expectations",
      "finding": "The null/0 rule is stated nowhere a step could obey it: no step names a field that may be null or 0 (step 4's schema has no such field), and no expectation grades it. A rule that no step carries and no check reaches.",
      "quote": "\"`null` for not-fetched and not-measured; `0` only for a measured zero.\""
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening vs SKILL.md Rules",
      "finding": "rationale.md asserts every rule is present with its origin and that an unbacked rule does not belong in the body, but three of the four rules (null/0; nothing from memory; installs/fetches/runs nothing) have no entry in rationale.md. By the reference's own test those rules should not be in the body.",
      "quote": "\"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json (21 expectations across all three evals) vs the bundle",
      "finding": "The grader that 21 of the 30 expectations name — check.py — is not in the artefact. Every check.py expectation is graded by a file that does not exist, so the steps they nominally cover (2, 3, 4, 5, 6) are graded by nothing executable.",
      "quote": "\"check.py T1: no rival page\" ... \"check.py T3: SOURCES row for the consulted source\""
    },
    {
      "level": "CLASS",
      "where": "evals.md Method vs evals/evals.json expectations",
      "finding": "The two eval documents name different graders for the same scenarios: evals.md says the observable criterion for every scenario is a kb.py lint run, evals.json grades with check.py rows and contains no lint invocation at all. Neither script is bundled, and no scenario actually runs a lint.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no-material branch) vs step 7",
      "finding": "The no-material branch orders a stop after writing the source-log row and the operation-log line, but step 7 unconditionally requires a lint, an index rebuild and a single commit. The branch changes two files and then leaves the procedure before anything lints or commits them; step 6 carves out no material explicitly, step 7 does not.",
      "quote": "\"keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop\" vs \"fix what the lint names before committing. The fact and its lint pass land in one commit.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 vs step 4, and evals.md S2 vs evals/evals.json eval 2",
      "finding": "'disputed' is defined at two scopes and no check disambiguates: step 2 marks the disputed value at the contradicted line, step 4 makes `disputed` a page-level frontmatter status. evals.md grades it at line scope while the expectation is scope-free, so a page-level status alone would pass a check written for a row-level mark.",
      "quote": "\"mark the page `disputed` there\" vs \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\"; graded only by \"check.py T2: disputed marker\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs step 5",
      "finding": "Step 4 orders the `related` frontmatter written as part of the page, but step 5 says the `related:` entry follows the neighbour sentence and must be omitted when no true sentence exists. A page written to step 4 already carries edges step 5 may forbid.",
      "quote": "\"`tags`, `related`\" vs \"then the `related:` entry. If no true sentence exists, do not add the edge.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (last sentence)",
      "finding": "The step ends in an instruction that names no file, number, row or state: 'what will move' is nowhere defined and no expectation grades any dating requirement. The step's closing clause is unchecked.",
      "quote": "\"Date what will move.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 status vocabulary vs step 2's four triage branches",
      "finding": "Two of the four status values, `unverified` and `outdated`, are reachable from no step: the triage branches are new/update/disputed/no material, and nothing in the body says when a page becomes unverified or outdated. Nothing grades them either.",
      "quote": "\"`status` (`verified` / `unverified` / `disputed` / `outdated`)\" vs \"**new** ... **update** ... **disputed** ... **no material**\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5, vs evals/files/wiki/notes/model-prices.md and the eval's own expected_output",
      "finding": "The expectation labelled 'beta price updated' quotes the fixture's pre-existing, pre-update row verbatim ($3/$15, dated 2026-08-20), while the raw states Beta 5 at $2/$10 effective 2026-09-01. The check passes on the untouched fixture and contradicts the expected_output that demands a dated row per changed price; the superseded row is already covered by a separate expectation.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\" vs fixture line \"| Beta 5 | $3 | $15 | 2026-08-20 |\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 1 (step 5, cascade) and the three generic expectations in all evals, vs evals/files/wiki",
      "finding": "Checks that pass on the untouched fixture. prompt-caching.md already names [[model-prices]] in body and `related`, so 'neighbour names owner back' is true before any edit — the eval's own expected_output concedes it with 'still'. The three generic expectations (frontmatter, no dangling link, listed in INDEX) are likewise satisfied by the fixture as shipped. Step 5 therefore has no check that can fail on a cascade the agent omits.",
      "quote": "\"check.py T1: neighbour names owner back\" / \"the neighbour still names the owner\" / \"every note is listed in INDEX.md\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 vs evals/evals.json (all three) and evals/files/wiki",
      "finding": "Step 1 is graded by nothing and cannot be graded by this fixture: no expectation mentions the raw, a content hash or MANIFEST; the wiki at evals/files/wiki has no raw/ directory and no MANIFEST.md; the raws sit outside the tree the prompt tells the agent to edit. The only scenario that would grade it, S3, is pending and has no entry in evals.json.",
      "quote": "\"provenance in `raw/MANIFEST.md`\" vs \"Edit the wiki in place and list the files you changed.\" and \"S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 7 vs evals/evals.json (all three)",
      "finding": "Step 7 is graded by nothing: no expectation runs a lint, rebuilds a search index, or inspects a commit, and the eval prompts end at editing files, so the same-commit requirement is unobservable in the harness as bundled.",
      "quote": "\"**Lint, then rebuild the search index;** fix what the lint names before committing. The fact and its lint pass land in one commit.\" vs \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 'new' branch and step 6 vs evals/evals.json",
      "finding": "One of the four triage branches is exercised by no eval: T1 is update, T2 disputed, T3 no material, and no scenario creates a page. Step 6's hand-written map-of-contents row for a new page is therefore graded by nothing, and the INDEX expectation that would cover it passes on the untouched fixture.",
      "quote": "\"a row in the hand-written map of contents for a new page\" vs \"check.py T3: no new note\" / \"check.py T1: no rival page\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs references/rationale.md 'Register' bullet and steps 6-7",
      "finding": "The description re-conflates the hand-written map of contents with the generated search index, the exact conflation the rationale records as caught and fixed and which steps 6 and 7 keep apart.",
      "quote": "\"index and log rows, lint\" vs \"**Register: map of contents by hand, search index generated.** They are different things; the first draft of this skill conflated them and the whole-artefact review caught it.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "The scenario input says three facts; the bundled fixture restates two multipliers and the rationale's before/after describes two. The executed eval T3 grades the two-fact fixture, so the scenario description does not match what was run.",
      "quote": "\"**Input:** a blog post restating three facts the wiki already holds with the same sources.\" vs \"Cache reads cost a tenth of the input price and writes cost 1.25 times.\" and \"a blog post restates two multipliers a note already carries with a dated source\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header line vs the S1/S2/S5 result lines",
      "finding": "The header declares three arms at k=2; the result lines name four arms (with, without, probe, incumbent) and record the without arm at k=1. The arm count and k in the header contradict the numbers the same file reports.",
      "quote": "\"three arms, k=2, code grader, blinded, preregistered rule\" vs \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 4 schema",
      "finding": "The edge scenario expects a source that is a note-only entry, while step 4's schema requires a source to carry a url or a path. A run that satisfies S3 violates step 4 as written.",
      "quote": "\"the note's source is a `note:` entry stating that\" vs \"`sources` (url or path, fetched, note)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Not executed in the first build' vs the bundle",
      "finding": "The negative-trigger claim is handed to a trigger matrix that is not in the artefact: the three numbers are asserted with no bundled file behind them and nothing in the bundle can reproduce them.",
      "quote": "\"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4).\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing. No expectation in evals/evals.json mentions the raw, the content hash or raw/MANIFEST.md; evals.md S3 would grade it but is 'pending' with no evals.json entry, and the fixture wiki has no raw/ or MANIFEST.md to check."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "eval 1 'check.py T1: no rival page' (update branch); eval 2 'check.py T2: disputed marker' (disputed branch); eval 3 'check.py T3: no new note', 'check.py T3: prompt-caching unchanged', 'check.py T3: LOG says no material' (no-material branch). The 'new' branch is graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 'check.py T1: quote from the raw on the page' + 'check.py T1: verdict word per claim'; eval 2 'check.py T2: quote from the card on the page' + 'check.py T2: verdict word per claim'. The DERIVED verdict specifically is graded by nothing."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "partly — 'every note keeps title/status/tags/related/sources frontmatter' (all three evals) and 'check.py T1: new source in note frontmatter with fetch date'. The closing 'Date what will move.', the four required body sections and the unverified/outdated status values are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "eval 1 'check.py T1: neighbour names owner back' and 'no dangling [[link]]' — but both are already true in the untouched fixture, so in substance the cascade is graded by nothing that can fail. S4 (cascade under pressure) has no executable eval."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "eval 1/2 'check.py T1|T2: SOURCES row' and 'LOG row'; eval 3 'check.py T3: SOURCES row for the consulted source' and 'LOG says no material'. The new-page map-of-contents row is graded by nothing (no scenario creates a page; the INDEX expectation passes untouched)."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing. No expectation runs a lint, rebuilds the index, or inspects a commit; the prompts stop at editing files. evals.md claims kb.py lint --json is the criterion, but no such invocation exists in evals/evals.json and neither kb.py nor check.py is bundled."
    }
  ]
}
```