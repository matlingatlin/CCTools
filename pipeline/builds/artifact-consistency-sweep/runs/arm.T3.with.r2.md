Read the method skill and its pair vocabulary, then swept `./artifact-C` (SKILL.md, references/rationale.md, evals.md, evals/evals.json, evals/files/check.py + 9 fixture files).

**Plan counts written before judging, and examined:** step×rule 7×3 = 21/21 · step×step 9/9 (6 adjacent + 3 branch-crossing: 2→6, 2→7, 3→4) · step×check 7×29 = 203/203 (23 evals.json expectations + 6 evals.md pass criteria) · description×body 9/9 clauses · file×BOM 20/20 (14 present, 6 named) · claim×rationale 11/11 (3 rules + 8 rationale bullets). Examined count equals plan count.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/files/check.py, T3 branch (lines 50-57) vs evals/evals.json eval 3, expectation 1",
      "finding": "The 'no page changed' check compares the wiki against itself. `fixture` resolves to check.py's own sibling directory `wiki/notes`, which is the same directory the prompt tells the model to edit in place, so `before` and `after` hash the same bytes read after the ingest. The check passes whatever the model wrote, and T3 - the one scenario evals.md calls 'the one measured win' - is graded by nothing.",
      "quote": "fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, all three prompts vs evals/files/wiki/",
      "finding": "All three evals mutate one shared fixture wiki in place, with no copy or restore step anywhere in the artefact. Eval 1 and eval 2 leave the notes, SOURCES.md and LOG.md changed, so eval 2 and eval 3 run against a wiki an earlier eval already rewrote, and the 'fixture' eval 3 claims byte-identity against no longer exists in its original state.",
      "quote": "Edit the wiki in place and list the files you changed."
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json, `files` list of evals 1, 2 and 3 vs evals/files/check.py",
      "finding": "The grader is shipped into the workspace of the model being graded. check.py is listed among the files handed to every task, and it contains the literal strings the expectations look for ('$2.00 per million input tokens', '2026-08-20', 'gamma-7-model-card', 'no material'), so the artefact under test can read its own answer key. In the other direction, no expectation invokes check.py: the expectations are prose, and nothing in the artefact says which of the two grades a run.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 7 vs SKILL.md Rules, third bullet",
      "finding": "The rule closes the skill's command surface to three commands; step 7 (and rationale.md's 'Lint in the same commit') orders a commit, which is none of them. A step orders what a rule forbids.",
      "quote": "It runs the wiki's own query, lint and index commands, and nothing else."
    },
    {
      "level": "CLASS",
      "where": "evals.md ## Method vs evals/files/ (whole bundle)",
      "finding": "The evals declare a grader that is not in the bundle and cannot run on the fixture. `knowledge/kb.py` is a host-repo path; the fixture wiki has no lint script, no kb.py and no index builder, and the only executable grader present is check.py, which evals.md never names. Every scenario's stated observable criterion therefore rests on a file that does not exist here.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals/evals.json eval 1, expectation 8 (check.py T1 'neighbour names owner back')",
      "finding": "Step 5's cascade is graded by a check that is already true of the untouched fixture: prompt-caching.md ships containing [[model-prices]]. The check cannot fail as a result of anything the ingest does, and the part step 5 actually requires - one true sentence per neighbour before the edge - is graded by no expectation at all (evals.md's S4 is 'pending').",
      "quote": "prompt-caching still names [[model-prices]]"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/evals.json, all three prompts and their expectations",
      "finding": "Step 1 is unperformable and ungraded in every eval. The fixture wiki has no raw/ directory and no manifest, no prompt asks for the raw to be saved into the wiki, and none of the 23 expectations mentions a raw copy, a fetch date on it, or a manifest row. The step's whole first clause and its provenance requirement are checked by nothing.",
      "quote": "The wiki at evals/files/wiki has notes/, INDEX.md, SOURCES.md and LOG.md."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs SKILL.md step 3 and check.py T1 claim_rows",
      "finding": "Three parts disagree on the verdict word. Step 3 defines MEASURED as 'the source measured it', and a vendor price list asserts prices rather than measuring them, which makes the correct verdict REPEATED by the skill's own definition; evals.md demands MEASURED; the grader accepts any of the three words. A run that follows step 3 fails evals.md's criterion and passes check.py.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 3 vs SKILL.md step 2, update branch",
      "finding": "An expectation with no step behind it. Keeping the superseded value as its own dated row is required by the eval and enforced by check.py's 'old price kept as a dated superseded row', but the update branch says only to extend the page; keeping both values is written only into the *disputed* branch. Nothing in the procedure tells the reader to preserve a price the source replaces.",
      "quote": "**update** - a page owns it: extend it, never a rival."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 Input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The scenario miscounts its own fixture: the pricing page carries four per-MTok prices (Alpha 5 input and output, Beta 5 input and output) plus two cache multipliers, not three.",
      "quote": "a fetched vendor pricing page with three per-MTok prices"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 Input vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "S5 says three facts; the fixture blog restates two multipliers, and rationale.md's own before/after record of the same scenario says two. The eval's input description contradicts both the file it runs on and the rationale it was written from.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header line vs S1, S2 and S5 arm counts",
      "finding": "The header's description of the run contradicts the per-scenario numbers: four arms are reported per scenario (with, without, probe, incumbent), not three, and the baseline arm ran once (1/1) where the header declares k=2.",
      "quote": "three arms, k=2, code grader, blinded, preregistered rule"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md frontmatter description vs SKILL.md 'Not this skill' paragraph",
      "finding": "The body deliberately strips the sibling names out of the general text and sends the reader to the repo-local section, but the description states five of those local unit names outright. The description promises a boundary in names the body says do not belong outside 'In this repo'.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md opening claim vs SKILL.md Rules, third bullet",
      "finding": "The rationale asserts complete coverage of the rules and does not cover them. The 'installs nothing, fetches no external code, runs only the wiki's own commands' rule has no entry and no observed failure behind it, and by the file's own test it 'does not belong in the body'.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2, no-material branch vs steps 6 and 7",
      "finding": "The branch stops before steps 3-7, and only step 6's log line is declared to hold 'in every branch'. Step 7 states the lint, the index rebuild and the one-commit rule unconditionally, so whether a no-material ingest is linted or committed at all is left undecided by two steps that disagree in scope.",
      "quote": "keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4, last sentence vs check.py common schema check and the 23 expectations",
      "finding": "The as-of-date requirement is graded by nothing. check.py only tests that five frontmatter keys are present - which is already true of all three fixture notes before any ingest - and the only date assertion anywhere is the single Beta 5 row in T1. No check reads any other price, version, limit or count in a body for its date.",
      "quote": "Every price, version, limit, count and date in the body carries its as-of date."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py, T1 'no rival page' vs SKILL.md step 2",
      "finding": "The rival-page check only fires on a note whose filename contains 'pric'. It catches the one baseline filename evals.md happens to quote and passes a rival called model-costs, 2026-09-rates or beta-5. Step 2's 'never a rival' is asserted against a single hard-coded substring.",
      "quote": "check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md ## Method vs evals.md S6 and S3 pass criteria",
      "finding": "The method states one criterion type for every scenario, then two scenarios are graded by something else: S6 by which skill fires, which is not a file state, and S3 by a lint severity level (INFO vs ERROR) that no grader in the bundle produces - check.py emits only PASS and FAIL.",
      "quote": "lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'In this repo (one instance)'",
      "finding": "Two things are named here that nothing in the procedure uses or can check: an `intake/` directory that appears nowhere else in the artefact, and a null-versus-zero contract convention that no step, rule, expectation or grader mentions. Named material with no step behind it.",
      "quote": "Wiki `knowledge/notes/`, raw `knowledge/raw/` (`MANIFEST.md`) and `intake/`; schema = this file + `CLAUDE.md`'s same-turn rule + `pipeline/contracts/claims.contract.json`, whose convention is `null` for not-measured and `0` only for a measured zero."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing - no expectation in evals.json and no check in check.py touches the raw copy, its fetch date or a manifest row; the fixture wiki has no raw/ directory, so the step cannot be exercised at all"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json e1 'LOG.md has a line naming the source and update', e2 'LOG.md names the card and disputed', e3 'LOG.md says no material and names the blog' + 'no new note' (check.py T1 'no rival page' - weak, substring-only; T2 'page status disputed'; T3 'no new note'). The no-page-changed half of the no-material branch is graded only by the self-comparing T3 hash check, i.e. by nothing"
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json e1 'a claims-table row carries the verbatim raw line and a verdict word' and e2's two claims-row expectations (check.py T1 claim_rows, T2 rows_). Grades one row per task; the step's 'every number, date and quote' and the locator column are graded by nothing, and the MEASURED/REPEATED/DERIVED distinction is graded by nothing - the regex accepts any of the three"
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals.json e1/e2/e3 'every note keeps its frontmatter; no dangling [[link]]; every note listed in INDEX.md' (check.py common loop) - a check already true of the untouched fixture. The Claims-table column shape, the status vocabulary beyond 'disputed', and the as-of date on every body value are graded by nothing"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "nothing that can fail - the only expectation is e1 'prompt-caching still names [[model-prices]]', which the fixture already satisfies before any ingest; the required sentence per neighbour is graded by no expectation, and evals.md's S4 for it is 'pending'"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json e1 'SOURCES.md has a row for the pricing page' + 'LOG.md has a line naming the source and update', e2 'SOURCES.md has a row for the card' + 'LOG.md names the card and disputed', e3 'SOURCES.md has a row for the blog' (check.py T1/T2/T3 SOURCES and LOG checks). The map-of-contents row for a *new* page is graded by nothing - no eval creates a page, and 'every note listed in INDEX.md' passes on the fixture"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "nothing - no expectation runs a lint, rebuilds an index, or inspects a commit; the fixture wiki contains no lint or index command, and evals.md's named grader for it (knowledge/kb.py lint --json) is absent from the bundle"
    }
  ]
}
```