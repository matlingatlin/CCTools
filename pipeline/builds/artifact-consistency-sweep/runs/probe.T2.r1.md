{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json (21 of 30 expectations, across all three evals) vs the bundle contents (evals/files/ holds only raw/ and wiki/)",
      "finding": "Every substantive expectation delegates grading to `check.py`, but no check.py is bundled anywhere in the artefact, and no eval lists it in its `files:` array (T1/T2/T3 each copy only `evals/files/wiki` and one raw file). So the named grader would not even be present in the eval sandbox. Every step whose only grader is a `check.py ...` line is therefore graded by nothing — this includes the whole of step 3 (quote + verdict), the disputed branch of step 2, and the register rows of step 6. evals.md compounds this by claiming a grader that does not ship: \"code grader, blinded\".",
      "quote": "\"check.py T1: quote from the raw on the page\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json expectations vs the starting state of evals/files/wiki/",
      "finding": "A majority of expectations are invariants already true of the untouched fixture, so a run that edits nothing passes them: \"every note keeps title/status/tags/related/sources frontmatter\", \"no dangling [[link]]\" and \"every note is listed in INDEX.md\" (all three fixture notes already satisfy these) are repeated in all three evals, and T1 adds \"no rival page\" and \"neighbour names owner back\", both true before the ingest. These checks detect damage; they grade no step. For T1 that leaves only four expectations that require any action at all.",
      "quote": "\"every note is listed in INDEX.md\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules bullet 4 vs SKILL.md steps 2 and 7, the \"In this repo\" section, and evals.md Method",
      "finding": "The rule states absolutely that the skill runs nothing, but step 2 tells you to query the wiki's index, step 7 tells you to lint and rebuild the search index, the instance section supplies four commands to run (`kb.py find`, `read`, `lint`, `build`), and evals.md's sole observable criterion is a command. The same bullet says the skill \"fetches\" nothing while Rules bullet 3 says \"look it up and date it\" and the description's trigger is \"a fetched page\". The rule as written is contradicted four times inside its own file.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline."
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md line 3 vs SKILL.md ## Rules",
      "finding": "The reference asserts it carries every rule in SKILL.md and states the test that an unbacked rule must be deleted from the body. Three of the four Rules bullets have no entry in rationale.md at all: the null/zero convention, the nothing-from-memory rule, and the installs/fetches/runs-nothing rule. By the reference's own stated test those three should not be in the body — the rewrite moved the step rationale out and left the Rules section unbacked.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "CLASS",
      "where": "evals.md ## Method vs evals/files/wiki/ and vs scenarios S4 and S6",
      "finding": "The Method declares one universal observable criterion, but (a) no kb.py ships in the eval environment — evals/files/wiki has no lint script, so the criterion cannot be run on any of T1/T2/T3; (b) S6 is a negative-trigger whose criterion is which skill fires, which is not a file state and no lint can report it; (c) S4's alternative criterion is the text of a commit message, which the eval prompts (\"Edit the wiki in place and list the files you changed\") never produce. \"every scenario\" is false for at least two of the six.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 1, 5, 6, 7 vs the three bundled scenarios",
      "finding": "Whole branches of the procedure are exercised by no scenario. All three evals are update/dispute/no-material, so the 'new' triage branch of step 2 and the new-page INDEX row of step 6 never run; step 1 never runs because the fixture pre-supplies the raw; step 5's cascade sentence and step 7's index rebuild have no scenario at all. evals.md discloses the S3/S4/S6 gap but not this one: the un-run branches sit inside scenarios marked PASS.",
      "quote": "a row in the hand-written map of contents for a new page"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5, vs evals/files/raw/2026-09-02-pricing-page.md and evals/files/wiki/notes/model-prices.md",
      "finding": "The expectation named 'beta price updated with date' quotes the pre-existing row verbatim — the OLD price and the OLD date. The raw says Beta 5 is $2.00/$10.00 fetched 2026-09-02; the fixture note already reads exactly `| Beta 5 | $3 | $15 | 2026-08-20 |`. The check is satisfied by not editing the file, and it collides with the sibling expectation \"old price kept as history or superseded row\", which is what that string actually tests.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 last expectation and expected_output, vs evals/files/wiki/notes/prompt-caching.md",
      "finding": "The only check that grades step 5 (cascade) is already true before the ingest: prompt-caching.md carries `related: [\"[[model-prices]]\"]` and names [[model-prices]] in its body. The expected_output confirms this is a no-change invariant (\"the neighbour still names the owner\"), so step 5 has no check that requires the run to do anything.",
      "quote": "\"check.py T1: neighbour names owner back\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs SKILL.md step 3",
      "finding": "S1 requires the verdict MEASURED for prices taken from a vendor pricing page. Step 3 defines MEASURED as 'the source measured it' and REPEATED as 'asserted, no measurement'; a vendor asserts its prices, it does not measure them, so the skill's own taxonomy points to REPEATED. The eval expectation and the step disagree on the verdict for the artefact's headline scenario, and no check would catch it because the only grader tests that a verdict word is present, not which.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 Input vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "S5 says the blog restates three facts. The bundled raw restates two (cache reads a tenth, writes 1.25x), and rationale.md twice describes the same source as two multipliers. The one measured win in the whole artefact is documented against a source count its own fixture contradicts.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md 'No material means no page is touched' vs evals.md S5 result line",
      "finding": "rationale reports the baseline failure as 2 of 2 runs; evals.md reports the same observation as 0/5 (without 0/1 + probe 0/2 + incumbent 0/2). The evidence behind the rule step 2 was rewritten for is stated at two different sample sizes, and neither file cites the other's number.",
      "quote": "every baseline run (2 of 2) still edited the owning page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs S1/S2/S5 result lines",
      "finding": "The header describes the build as three arms at k=2. Every scenario line then reports four arm names — with, without, probe, incumbent — and 'without' is run once, not twice (1/1 or 0/1). The arm count and the k in the header cannot both describe the rows beneath them.",
      "quote": "three arms, k=2, code grader, blinded, preregistered rule"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md ## Method vs the S5 heading and S5 Result",
      "finding": "The Method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails. S5 is typed 'normal' and carries exactly that verdict — it is the only scenario the baseline fails. Conversely S2 is typed 'trap' and its baseline was clean. The scenario type labels and the Method's rule for using them are inverted on both counts.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs SKILL.md '**Not this skill:**' paragraph",
      "finding": "The description names four negative boundaries; the body's boundary list drops deep-reading (summarising a text) and keeps the other three plus kb-curator. A reader who follows the body's list has no rule separating this skill from deep-reading, which is the nearest neighbour on the ingest path.",
      "quote": "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 'no material' gloss vs references/rationale.md and vs eval 3",
      "finding": "The step defines no material as 'no claim, no value, no newer date'. The T3 blog has claims and has values — it simply adds nothing the wiki lacks, which is how rationale.md defines it ('adds no knowledge beyond what the wiki already holds'). Read literally the step's own test routes the artefact's flagship no-material fixture away from the no-material branch. The word 'new' appears to have been lost in the halving.",
      "quote": "**no material** (no claim, no value, no newer date for any page: keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals.md S5 pass criterion vs evals/evals.json eval 3",
      "finding": "Three different specifications of the same log line: the step requires the URL and the reason, evals.md requires the URL and the date, evals.json requires only the words 'no material'. A run satisfying the strictest fails none of them, but nothing grades the reason, and the date requirement exists in only one of the three documents.",
      "quote": "an operation-log entry says \"no material\" with the URL and date."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/raw/*.md and evals/files/wiki/",
      "finding": "Step 1 mandates a content hash and provenance in raw/MANIFEST.md (rationale.md dates that addition to the 2026-09-03 field trial). None of the three bundled raw files carries a hash, no MANIFEST.md exists, and the eval wiki has no raw/ directory at all — the raws live outside the wiki, in evals/files/raw/. The artefact's own fixtures model a wiki that violates step 1, and no expectation mentions the raw, the hash or the manifest.",
      "quote": "with URL or path, fetch date and a content hash - in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 body schema vs evals/files/wiki/notes/*.md and the evals.json frontmatter expectation",
      "finding": "Step 4 mandates four body sections. None of the three fixture notes has any of them — each is a title heading plus one prose line — and the only schema expectation checks frontmatter keys, never the body. The notes that define the target schema for every eval contradict the schema the step requires, and the half of step 4 that governs the body is graded by nothing.",
      "quote": "body: what it is, the claims graded, what it means here, what is open."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (disputed branch) vs step 4 (status vocabulary) vs evals.md S2 and evals.json eval 2",
      "finding": "Where 'disputed' is recorded is specified four ways: step 4 makes it a frontmatter `status` value, step 2 says mark the page disputed 'there' (at the contradicted line), evals.md says 'at that line', evals.json asks only for a 'disputed marker' anywhere. A run that sets frontmatter status only, and a run that annotates the line only, both claim conformance with a different sentence of the same file.",
      "quote": "**disputed** (the source contradicts a page: keep both values as dated rows with their sources, mark the page `disputed` there)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md '## When to use' bullet 2 vs the Steps section and all six scenarios",
      "finding": "A trigger with no procedure behind it: 'a compiled summary page is written back' appears nowhere else in the artefact — no step describes writing back a compiled summary, rationale.md does not mention it, and no scenario covers it. Similarly the description advertises 'repo' and 'measurement' as source types while step 1 gives a raw-keeping rule only for video and image.",
      "quote": "An existing note gains a source, or a compiled summary page is written back."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Not executed in the first build'",
      "finding": "The negative-trigger claim for S6 is discharged by citing a trigger matrix with three precise ratios, but no trigger matrix is bundled in the artefact and nothing in it can be re-run or inspected. The only evidence for the artefact's one boundary test is an uncheckable citation, in the same paragraph that admits S6 has no executable eval.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 second sentence",
      "finding": "The step's terminal condition is a judgement with no defined grader: whether a sentence 'says why it matters' and whether a 'true sentence exists' cannot be checked by inspection, no code grader is claimed for it, and no human or model grader is specified anywhere in evals.md. The only S4 fallback ('the commit message states which neighbours were left one-way and why') is likewise self-declared.",
      "quote": "If no true sentence exists, do not add the edge."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header verdict vs /home/user/skills-repo/CLAUDE.md capability map",
      "finding": "The artefact's own eval record returns ITERATE and holds the skill at candidate status. The repository's routing map records the same build as shipped ('measured 2026-09-03, first v3 build, ship') and lists llm-wiki-ingest as the owner of the ingest job. One of the two is wrong about whether this skill passed its gate; the artefact carries no note reconciling them.",
      "quote": "**Verdict:** ITERATE — every quality clause passed (no regression on T1/T2, the T3 win survived both repeats, tool calls 1.17x) and the token clause failed at 1.23x against a 1.20x cap. Status stays candidate."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "none. No expectation in evals.json and no pass criterion in evals.md mentions the raw file, its content hash or raw/MANIFEST.md. The fixtures pre-supply the raw outside the wiki (evals/files/raw/), carry no hash and no manifest, so the step is never executed by any of T1/T2/T3."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "partially, and only through the unbundled check.py: update branch by 'check.py T1: no rival page' (true of the untouched fixture), disputed branch by 'check.py T2: disputed marker', no-material branch by 'check.py T3: prompt-caching unchanged' + 'no new note' + 'LOG says no material'. The 'new' branch is exercised by no scenario, and the opening clause (query the index for title, trigger terms and URL) leaves no trace and is graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "nominally 'check.py T1/T2: quote from the raw|card on the page' and 'verdict word per claim' — both attributed to a grader that is not in the bundle. Even as described they test presence, not correctness: no check verifies that every number and date in the raw was located (T1 names only Beta), that the verdict assigned is the right one (see the MEASURED/REPEATED conflict), or the 'before writing it' ordering, which is unobservable in the finished files."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "the generic expectation 'every note keeps title/status/tags/related/sources frontmatter', in all three evals — frontmatter keys only, and true of the fixture before any edit. The status vocabulary (verified/unverified/disputed/outdated), the four mandated body sections and 'date what will move' are graded by nothing, and the fixture notes themselves have none of the body sections."
    },
    {
      "step": 5,
      "checkable": false,
      "graded_by": "none. The step's terminal condition ('one sentence saying why it matters', 'if no true sentence exists') is a judgement with no code, model or human grader defined anywhere in evals.md. The nearest check, 'check.py T1: neighbour names owner back', is satisfied by the untouched fixture, and evals.md S4 — the only scenario aimed at this step — is 'pending'."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "'check.py T1/T2: SOURCES row' and 'LOG row', plus 'check.py T3: SOURCES row for the consulted source' and 'LOG says no material' — all via the unbundled check.py. The map-of-contents row is never exercised: no scenario creates a page, and 'every note is listed in INDEX.md' passes on the untouched fixture."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "none. No lint script ships in evals/files/, so evals.md's stated criterion (`python3 knowledge/kb.py lint --json`) cannot run on the eval wiki; no eval rebuilds or inspects a search index; and the eval prompts stop at 'Edit the wiki in place and list the files you changed', so the one-commit clause is unobservable. The 'no lint script?' fallback resolves to a self-declaration in the log line, which nothing verifies. The three generic expectations ('no dangling [[link]]', INDEX listing, frontmatter) are hand-lint proxies that are already true before the run."
    }
  ]
}