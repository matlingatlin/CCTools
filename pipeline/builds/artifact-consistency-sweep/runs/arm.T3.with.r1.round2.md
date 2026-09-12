```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json id 1 expectations vs SKILL.md steps 2 and 4",
      "finding": "The update path is graded for behaviour no step orders. Nothing in the procedure says an update must keep the superseded value as its own dated row (only the disputed branch of step 2 says 'keep both values'), and nothing says an existing note that has no '## Claims' table must be retro-fitted into step 4's schema — yet both are required expectations. A run that follows every step as written can fail eval 1.",
      "quote": "the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 1, 5, 7 vs evals/evals.json (all 23 expectations)",
      "finding": "The executable eval set covers only the middle of the procedure (steps 2, 3, 4, 6). No expectation touches the raw layer or its manifest (step 1 — the fixture wiki has no raw/ directory and the raw files sit outside the wiki), the cascade (step 5 — none of the three tasks creates a page), or the lint/index-rebuild/commit (step 7). evals.md's own S3/S4 would cover steps 1 and 5 and are 'pending'.",
      "quote": "provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no material branch) vs step 7",
      "finding": "Step 2's no-material branch orders 'stop' before step 7 is reached, so lint, index rebuild and the commit rule never run on that branch. Step 6 was given an 'in every branch' clause to survive the stop; step 7 was not.",
      "quote": "keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs the three prompts in evals/evals.json",
      "finding": "Step 7's closing obligation is a commit, but every eval prompt says 'Edit the wiki in place and list the files you changed' and the fixture is not a git repository. The step's deciding condition cannot be produced, let alone checked, in the environment that grades the skill.",
      "quote": "The fact and its lint pass land in one commit."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 54 (task T3) vs evals/evals.json id 3, expectation 1",
      "finding": "The T3 'before' hashes are read from check.py's own sibling directory — which is the same evals/files/wiki the prompt tells the agent to edit in place. The fixture is therefore compared with itself and the byte-identical check can never fail, so the central expectation of the one scenario that measured a win is graded by nothing.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json id 1 expectation 8 and id 2 expectation 5, against evals/files/wiki fixture",
      "finding": "Several expectations are already true of the untouched fixture and so cannot separate a run that did the step from a run that did nothing: prompt-caching.md already contains '[[model-prices]]', and local-models.md already contains '2026-08-25'. These are the only expectations that touch step 5 and half of eval 2's date check.",
      "quote": "prompt-caching still names [[model-prices]]"
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md opening vs SKILL.md rule 3",
      "finding": "rationale.md states that every rule in SKILL.md appears there with its evidence, and that a rule with nothing behind it does not belong in the body. Rule 3 ('installs nothing and fetches no external code…and nothing else') has no bullet, no run and no source anywhere in rationale.md. By the file's own test the rule should not be in the body.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs evals/files/check.py",
      "finding": "evals.md names a grader that neither exists in the bundle nor is the one used: there is no knowledge/kb.py in the fixture wiki, the actual grader is evals/files/check.py, and that grader's contract explicitly excludes 'reading the note' ('Every check is a fact about the files; no judgement.').",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs the executed lines of S1, S2 and S5",
      "finding": "The header declares three arms at k=2, but the scenario lines name four arms (with, without, probe, incumbent) and the 'without' arm is run once, not twice ('without 1/1', 'without 0/1'). The header's design and the reported runs cannot both be true.",
      "quote": "three arms, k=2"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs S5 heading and result",
      "finding": "The Method reserves 'PASS. Beats baseline.' for scenarios where the baseline plausibly fails, and S5 is tagged '· normal' — yet S5 is the only scenario reported as beating baseline, while the scenario tagged 'trap' (S2) is reported as 'no delta; baseline clean'. The normal/trap labels are inverted relative to the results they carry.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 Input vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "S5 says three restated facts; the bundled raw carries two multipliers (0.1x read, 1.25x write) and rationale.md describes the same scenario as 'two multipliers'. Three sources of the same fixture give two different counts.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources"
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md (no material bullet) vs evals.md S5 result line",
      "finding": "rationale.md says every baseline run of the no-material probe was 2 of 2; evals.md reports five baseline runs for the same scenario ('without 0/1, probe 0/2, incumbent 0/2' and '0/5 baseline runs'). The evidence behind the rule cites a denominator the eval record contradicts.",
      "quote": "every baseline run (2 of 2) still edited the owning page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Not executed in the first build'",
      "finding": "The negative-trigger claim is delegated to a 'trigger matrix' with three precise ratios, but no trigger matrix exists in the bundle and no other file names one. The one artefact carrying S6's evidence is absent, so S6 is graded by nothing that can be inspected.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs the 'Not this skill' paragraph",
      "finding": "The body says the local sibling names are kept under 'In this repo', but the description hard-codes five of them (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator). The description contradicts the containment the body claims for it.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'When to use' second bullet vs steps 1, 2 and 6",
      "finding": "A compiled summary page written back is offered as a trigger, but step 2's triage admits exactly one of four dispositions, all of which are about an incoming source; and a written-back summary has no source bytes, no URL and no fetch date, which steps 1 and 6 require in every branch. The trigger has no path through the procedure.",
      "quote": "An existing page gains a source, or a compiled summary page is written back."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no material test) vs evals/evals.json id 3",
      "finding": "The no-material test includes 'no newer date for any page', and the blog raw carries fetched: 2026-09-02 against prompt-caching's 2026-08-20 — by the literal test the eval-3 source is not no material, yet no material is the required disposition. The artefact uses two kinds of date (fetch date in step 1, as-of date in step 4) and never says which this test means.",
      "quote": "**no material** - no claim, no value, no newer date for any page"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 26 vs evals/evals.json id 1 expectation 1",
      "finding": "The expectation has two halves — 'model-prices is the page updated' and 'no rival page' — and the check grades only the second, by a substring test that fires only if a new note's filename contains 'pric'. A rival page named e.g. beta-costs, and an update written to the wrong note, both pass.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 3",
      "finding": "S3 requires the verdict to turn on the creator being unidentified, but step 3 defines the three verdicts solely by whether the source measured, asserted or computed the value — an on-screen number the clip itself measured is MEASURED under step 3. The expectation grades a rule the procedure does not contain.",
      "quote": "claims from it are REPEATED, not MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs evals/evals.json (all expectations)",
      "finding": "The Claims table is specified with five columns including 'locator', a term the artefact defines nowhere and no expectation grades; the graders only look for the quote and the verdict word on one line. Two of the five prescribed columns end in nothing checkable.",
      "quote": "a `## Claims` table with one row per claim - claim | source | locator | verbatim quote | verdict"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S2 vs evals/evals.json id 2 expectation 4",
      "finding": "The bundle carries two eval documents and never says which one grades. Where they describe the same scenario they differ: S2's pass criterion stops at the row, while evals.json also requires the page-level status that step 2 mandates ('set the page's status: disputed'). A run graded by evals.md and one graded by evals.json can disagree.",
      "quote": "both values kept as separate rows with their sources and dates; the note marked disputed at that line; neither value silently overwritten"
    },
    {
      "level": "INSTANCE",
      "where": "bundle contents vs SKILL.md (only bundled path it names)",
      "finding": "There is no bill of materials in the artefact; evals.json's per-eval 'files' arrays are the only manifest, and they cover the fixtures alone. SKILL.md names exactly one bundled path — references/rationale.md — so evals.md, evals/evals.json and evals/files/* are present and pointed at by nothing in the artefact's own text.",
      "quote": "The observed failures behind each step are in `references/rationale.md` - open it when a step seems optional."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded — no expectation in evals/evals.json mentions the raw, its fetch-date filename or a manifest; the fixture wiki has no raw/ directory, so the manifest clause is never triggered. evals.md S3 would cover it and is 'pending'."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json e1 'LOG.md has a line naming the source and \\'update\\''; e2 'a row is marked disputed and the page status is disputed'; e3 'LOG.md says no material and names the blog' + 'no new note'. The 'never a rival' clause is graded only by check.py's 'pric'-substring test (see finding 17)."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json e1 'a claims-table row carries the verbatim raw line and a verdict word'; e2 'a claims row carries 753B, the card's verbatim line and a verdict word' + 'a claims row carries 744B and a verdict word'. Which of the three verdict words is correct is not graded — check.py accepts any of MEASURED|REPEATED|DERIVED."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals.json e1 'a Beta 5 row carries $2, $10 and a 2026-09 date' and 'the new source with its fetch date is in model-prices' frontmatter'; e2 'both sources dated 2026-08-25 and 2026-09-02' (half pre-satisfied by the fixture); e1/e2/e3 'every note keeps its frontmatter'. The Claims-table columns source and locator are ungraded."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "ungraded — the only expectation that touches it, e1 'prompt-caching still names [[model-prices]]', is already true of the untouched fixture, and no eval task creates a page with new neighbours. evals.md S4 is 'pending'."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json e1 'SOURCES.md has a row for the pricing page' + 'LOG.md has a line naming the source and \\'update\\''; e2 'SOURCES.md has a row for the card' + 'LOG.md names the card and \\'disputed\\''; e3 'SOURCES.md has a row for the blog'. The map-of-contents row for a new page, the source URL and 'the pages touched' in the log line are ungraded (no task creates a page; check.py greps for a slug only)."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "partially — e1/e2/e3 'every note keeps its frontmatter; no dangling [[link]]; every note listed in INDEX.md' grades the lint-clean end state, but that is the grader performing the lint. Nothing grades the lint run, the index rebuild, the one-commit rule (impossible in the fixture, finding 4), or the by-hand fallback's log line."
    }
  ]
}
```