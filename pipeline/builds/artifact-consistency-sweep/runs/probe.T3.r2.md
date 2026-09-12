```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — `files` array of all three evals",
      "finding": "Every eval declares a grader file that is not in the bundle. `evals/files/check.py` does not exist anywhere in the artefact, so all 23 expectations across the three evals are adjudicated by nothing. evals.md simultaneously claims the build used a 'code grader'.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs SKILL.md §In this repo and evals/files/wiki/",
      "finding": "The declared observable check is a host-repo command (`knowledge/kb.py`, named only under SKILL.md's 'In this repo' instance section). It is not in the artefact and the fixture wiki has no lint script at all — the case SKILL.md step 7 explicitly provides a fallback for. The stated grading mechanism cannot run on the bundled fixtures.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md §Rules bullet 3 vs §Steps 7",
      "finding": "The rules close the action surface to three wiki commands, but step 7 requires committing (and gating the commit on a lint fix), and step 1 requires saving fetched source bytes. A git commit is neither a query, a lint nor an index command, so the rule forbids the action a numbered step mandates.",
      "quote": "It runs the wiki's own query, lint and index commands, and nothing else."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/raw/*.md",
      "finding": "Step 1 forbids provenance inside the immutable raw file and requires a directory manifest. All three bundled raw fixtures carry `source:` and `fetched:` lines inside the file, and no manifest exists anywhere in the artefact — the bundled fixtures instantiate the shape the step rules out.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals/files/raw/2026-09-02-pricing-page.md (eval 1)",
      "finding": "Triage must yield exactly one disposition per source, but the artefact's own eval-1 raw is an 'update' for model-prices and, in the same file, restates prompt-caching's 0.1x/1.25x — 'no material' for that page. Eval 1's expectations require both dispositions at once (model-prices updated, prompt-caching untouched), which step 2 as written forbids.",
      "quote": "**Search, then triage into exactly one.**"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 3 vs SKILL.md steps 2 and 4",
      "finding": "The eval grades retention of a superseded value, but no step requires it. Only the `disputed` branch says to keep both values; the `update` branch says only 'extend it, never a rival', and step 4's schema says nothing about superseded rows. The eval tests behaviour the body never instructs.",
      "quote": "\"the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json expectations (evals 1, 2) vs evals.md S1 pass criterion vs SKILL.md step 3",
      "finding": "Step 3's three-way verdict has no decision procedure (a vendor price list asserts rather than measures, yet evals.md demands MEASURED), and evals.json resolves the ambiguity by accepting any of the three words. The distinctive output of step 3 — the correct verdict — is graded by nothing; only the presence of a token is checked.",
      "quote": "\"a claims-table row carries the verbatim raw line and a verdict word\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 2, 3, 7 vs evals.md §Method",
      "finding": "Several steps encode ordering/process ('Search, then…', 'before writing it', 'fix what the lint names before committing', 'land in one commit') while the declared criterion is end-state file content. No end-state check can distinguish a run that searched first from one that wrote first, or one commit from two — these clauses are structurally ungradable under the artefact's own method.",
      "quote": "The observable criterion for every scenario is the state of the files"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says three facts; the rationale and the bundled blog fixture both carry two multipliers (0.1x and 1.25x). The fixture cannot satisfy the input the scenario describes.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 result vs references/rationale.md 'no material' bullet",
      "finding": "Baseline-run counts for the same observation disagree: evals.md tallies five baseline runs (without 1, probe 2, incumbent 2), the rationale attributes the finding to two.",
      "quote": "**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)"
    },
    {
      "level": "CLASS",
      "where": "evals.md line 3 header vs the S1/S2/S5 scenario lines",
      "finding": "The header declares three arms at k=2; each executed scenario reports four arm labels (with, without, probe, incumbent) and the 'without' arm at k=1. The design statement and the reported runs do not describe the same experiment.",
      "quote": "three arms, k=2, code grader, blinded, preregistered rule"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md 'no material' bullet",
      "finding": "The one measured win is graded on the very source the rule was derived from — the 2026-09-02 probe blog post restating the caching multipliers is both the observation that produced step 2's no-material branch and the only eval that proves it. No held-out instance exists.",
      "quote": "the one measured win, and the rule step 2 was rewritten for"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs scenario type labels",
      "finding": "The method binds verdict wording to scenario type, but the labels invert it: S2 is typed 'trap' and returns 'PASS (no delta; baseline clean)', while S5 is typed 'normal' and is the only 'Beats baseline'. The type field grades nothing and contradicts the results it is supposed to predict.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S6 (`**Result:** pending`) vs evals.md §Not executed in the first build",
      "finding": "S6 is simultaneously reported as pending and as already carried with three measured ratios. The trigger matrix that supplies those numbers is not in the bundle, so the negative-trigger claim rests on an artefact that cannot be inspected.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 4 and step 7",
      "finding": "S3 grades against two things the body never defines: a standalone `note:` source entry (step 4's schema lists `note` as a field of a url-or-path entry, not a substitute for one) and lint severity levels INFO/ERROR (step 7 names no severities).",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening claim vs SKILL.md §Steps 2, 4 and §Rules",
      "finding": "The rationale asserts completeness it does not have. Step 4's whole schema (frontmatter fields, the four status values, as-of dates on every number), step 2's search-first clause, and both of the last two Rules ('nothing from memory', 'installs nothing') have no bullet behind them. By the file's own stated criterion those items do not belong in the body.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs references/rationale.md 'Register' bullet and SKILL.md steps 6–7",
      "finding": "The description collapses the hand-written map of contents and the generated search index into one word — the exact conflation the rationale records as caught and fixed in the body. Step 6 (a map-of-contents row) and step 7 (rebuild the search index) are distinct in the body but not in the description that selects the skill.",
      "quote": "index and log rows, lint."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs §When to use ('Not this skill')",
      "finding": "The body deliberately withholds sibling names from the portable text and defers them to the instance section; the description hard-codes the same five local unit names. The two halves of the artefact apply opposite generality policies to the same content.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    },
    {
      "level": "CLASS",
      "where": "evals.md §Scenarios (six) vs evals/evals.json (three)",
      "finding": "Half the declared blend has no executable eval — the edge (S3), the pressure (S4) and the negative-trigger (S6) scenarios. In consequence step 1's raw/manifest output, step 5's cascade and step 7's lint/commit are the steps left with no executable check, and the claim that the skill does not fire on a skill-bundle request is untested.",
      "quote": "S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 pass criterion vs SKILL.md step 6 and evals/evals.json eval 3",
      "finding": "S5's criterion requires only the operation-log line, dropping the source-log row that step 2/6 require on the no-material branch, that the rationale insists still happens, and that evals.json eval 3 actually checks. Three parts of the artefact state three different completion conditions for the same branch.",
      "quote": "**Pass criterion:** no page changed; an operation-log entry says \"no material\" with the URL and date."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/wiki/notes/*.md vs SKILL.md step 4",
      "finding": "No fixture note implements the mandated schema — none has a `## Claims` table, and prompt-caching's 0.1x/1.25x and local-models' 245 GB carry no as-of date. Eval 3 then requires those notes byte-identical, so the fixture freezes a schema violation as the pass condition and step 4's body/date clauses are never graded.",
      "quote": "\"model-prices, prompt-caching and local-models are byte-identical to the fixture\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 8 vs SKILL.md step 5",
      "finding": "The only cascade-related check tests that a pre-existing body wikilink survived. Step 5's actual deliverable — one true sentence per neighbour before the `related:` edge — appears in no expectation in any eval, and its dedicated scenario (S4) is pending.",
      "quote": "\"prompt-caching still names [[model-prices]]\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals/evals.json evals 1–3",
      "finding": "The map-of-contents clause is conditioned on a new page, but every eval either forbids a new page or is a no-material case, so that clause can never be exercised. The only INDEX check is a static invariant that holds unchanged in all three runs.",
      "quote": "A row in the hand-written map of contents for a new page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals/evals.json eval 1",
      "finding": "Two of S1's four criteria have no counterpart expectation: 'lint reports 0 errors' (no lint exists in the fixture) and 'INDEX unchanged' (evals.json checks only that every note is listed, which a spurious added row would still satisfy).",
      "quote": "no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing. No expectation in any eval mentions the raw file, its immutability, or a manifest row; the raw is handed to the run as a pre-existing file and the fixture wiki has no raw/ directory or MANIFEST.md, so neither the 'keep' nor the 'provenance in the manifest' clause can be observed."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json eval 1 \"LOG.md has a line naming the source and 'update'\" + \"model-prices is the page updated; no rival page\"; eval 2 \"LOG.md names the card and 'disputed'\" + \"a row is marked disputed and the page status is disputed\"; eval 3 \"LOG.md says no material and names the blog\" + \"no new note\". The disposition is graded in all three branches; the 'Search…' precondition and the 'exactly one' constraint are not (and eval 1's source spans two dispositions)."
    },
    {
      "step": 3,
      "checkable": false,
      "graded_by": "partially — evals.json eval 1 \"a claims-table row carries the verbatim raw line and a verdict word\" and eval 2 \"…753B, the card's verbatim line and a verdict word\" / \"…744B and a verdict word\" grade only that a verbatim quote and some verdict token are present. Whether the verdict is the RIGHT one is graded by nothing and the body supplies no decision rule (evals.md demands MEASURED for a price list; evals.json accepts any word). 'every number, date and quote' and 'before writing it' are graded by nothing."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "partially — evals.json eval 1 \"the new source with its fetch date is in model-prices' frontmatter\"; eval 2 \"the model card is in local-models' frontmatter sources\" and \"the page status is disputed\"; all three \"every note keeps its frontmatter\". Ungraded: `title`/`tags`/`related`, the `verified`/`unverified`/`outdated` status values, the four required body sections, the `## Claims` table's existence as such, and the as-of date on every price/version/limit/count — and no eval creates a page, so the schema is never graded on a new note."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "nothing. The only related check, evals.json eval 1 \"prompt-caching still names [[model-prices]]\", is a no-regression test on a link that already existed in the fixture. No eval adds a neighbour, so the 'one sentence saying why it matters' requirement and the 'no true sentence, no edge' rule are never exercised; the dedicated scenario S4 is pending."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "partially — source log: evals.json \"SOURCES.md has a row for the pricing page\" / \"…for the card\" / \"…for the blog\" (including the no-material branch); operation log: \"LOG.md has a line naming the source and 'update'\" / \"LOG.md names the card and 'disputed'\" / \"LOG.md says no material and names the blog\". Ungraded: the map-of-contents row for a new page, since no eval creates one; \"every note listed in INDEX.md\" is a static invariant that passes without any registration having occurred."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "nothing that tests the step. evals.json's \"no dangling [[link]]; every note listed in INDEX.md\" proxies a clean wiki but not that a lint was run. The grader evals.md names (`knowledge/kb.py lint --json`) is not in the artefact, `evals/files/check.py` is missing, the fixture wiki has no lint or index-build command, the eval prompts stop at 'Edit the wiki in place and list the files you changed' so no commit exists to test 'land in one commit', and no expectation looks for the fallback's required disclosure in the log line."
    }
  ]
}
```