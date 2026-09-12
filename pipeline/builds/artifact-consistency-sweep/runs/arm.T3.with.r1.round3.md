I read the method skill (`artifact-consistency-sweep`) and its `references/pair-vocabulary.md` first, then swept the artefact at `./artifact-C` (SKILL.md, `references/rationale.md`, `evals.md`, `evals/evals.json`, `evals/files/check.py` and the wiki/raw fixtures). Note: the bundle ships no `bom.json`, so the file×BOM type was run against the per-eval `files` arrays as the only inventory.

```json
{
  "findings": [
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py, T3 branch (lines 50-57) vs evals/evals.json eval 3 and its prompt",
      "finding": "The 'byte-identical to the fixture' check compares the wiki against itself. The prompt orders the wiki edited in place at evals/files/wiki, and the reference path is resolved from check.py's own location (evals/files/) to that same evals/files/wiki/notes, so `before` and `after` hash the identical bytes and the check can never fail. The one measured win of the build (S5/T3, no material) is therefore graded by an inert assertion, and the expectation 'model-prices, prompt-caching and local-models are byte-identical to the fixture' grades nothing.",
      "quote": "    fixture = pathlib.Path(__file__).resolve().parent / \"wiki\" / \"notes\""
    },
    {
      "level": "CLASS",
      "where": "evals.md '## Method' vs evals/evals.json and evals/files/check.py",
      "finding": "The named grader is absent from the bundle and from the fixture. evals.md says every scenario's criterion is checked by `knowledge/kb.py lint --json`, but the bundle's grader is evals/files/check.py, the fixture wiki (INDEX.md, LOG.md, SOURCES.md, notes/) contains no kb.py and no lint script, and no eval invokes a lint. Every pass criterion in evals.md that reads 'lint reports 0 errors' or 'lint reports the note-only source as INFO' is graded by a program that does not exist here.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "bundle root (no bom.json / manifest) vs the 11 files present",
      "finding": "There is no bill of materials in the artefact, so no row exists to check the bundled files against. The only inventory is the per-eval `files` array, which declares three inputs per eval and never names evals.md, references/rationale.md or the seven fixture files individually; evals.md itself is pointed at by nothing in the bundle. A named path absent from the bundle (knowledge/kb.py, the trigger matrix) cannot be detected by any list the artefact carries.",
      "quote": "   \"files\": [\n    \"evals/files/wiki\",\n    \"evals/files/raw/2026-09-02-pricing-page.md\",\n    \"evals/files/check.py\"\n   ]"
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md line 3 vs SKILL.md '## Rules' (rules 2 and 3)",
      "finding": "rationale.md asserts that every rule in SKILL.md is recorded there with its evidence, and that a rule with nothing behind it does not belong in the body. Two of the three rules have no bullet in rationale.md: 'Nothing about a tool, price, version or limit from memory' and 'This skill installs nothing and fetches no external code'. By the file's own standard those two rules do not belong in the body; either the rules or the completeness claim is false.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "CLASS",
      "where": "evals.md '## Not executed in the first build' vs SKILL.md steps 1, 5 and 7",
      "finding": "Half the procedure is graded by nothing because three of the six scenarios were never made executable. S3 is the only scenario that touches the raw (step 1), S4 the only one that touches the cascade (step 5), and no scenario exercises lint/index-rebuild/commit (step 7); none of the three evals in evals.json creates a page, saves a raw copy, or reads the log line for a hand-lint statement. The gap is disclosed but not closed in this rewrite.",
      "quote": "## Not executed in the first build"
    },
    {
      "level": "CLASS",
      "where": "evals.md S1 pass criterion vs evals/evals.json eval 1 expectations and check.py T1",
      "finding": "The artefact carries two expectation sets that disagree on the same executed scenario. evals.md S1 requires the verdict word MEASURED specifically, a lint reporting 0 errors, INDEX unchanged and SOURCES +1 row; evals.json/check.py accept any of MEASURED|REPEATED|DERIVED, run no lint, assert every note IS in INDEX (not that INDEX is unchanged), and only test that a substring appears in SOURCES.md rather than counting rows. A run can pass one set and fail the other.",
      "quote": "- **Pass criterion:** the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expectation 3 vs SKILL.md step 2 (update branch) and step 4",
      "finding": "An expectation no step produces. Keeping the superseded value as its own dated row is ordered only in the disputed branch of step 2 ('keep both values as dated claim rows'); the update branch says only 'extend it, never a rival', and step 4 requires an as-of date but never says a replaced price is retained. evals.md's S1 criterion does not require it either, yet check.py fails the run without it.",
      "quote": "the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals/evals.json eval 1 and eval 2 expectations",
      "finding": "Step 3 orders every number, date and quote in the raw to be located and graded MEASURED/REPEATED/DERIVED, but the expectations grade one row and accept any of the three verdict words. check.py matches the regex MEASURED|REPEATED|DERIVED, so a claim graded with the wrong verdict passes, and the raw's other figures (Alpha 5's $5/$25, the 10%/125% cache line) may be ungraded with the run still green. The discipline the step exists for is graded by nothing.",
      "quote": "a claims-table row carries the verbatim raw line and a verdict word"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no material branch) vs step 6",
      "finding": "Two steps own the same action, and one is unreachable. Step 2's no-material branch writes the source-log row and the operation-log line itself and then says 'stop'; step 6 says its operation-log line happens 'in every branch', which the stopped branch never reaches. Step 7's lint and index rebuild are likewise skipped in that branch while nothing says so.",
      "quote": "**no material** - no claim, no value, no newer date for any page: keep the raw, write the source-log row and the operation-log line, touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs step 6 and references/rationale.md ('Register: map of contents by hand, search index generated')",
      "finding": "'Index' names two different things across the body and collapses to one in the evals. rationale.md insists the hand-written map of contents and the generated search index are different things; step 6 writes a row in the map, step 7 rebuilds the search index, but the fixture wiki has only INDEX.md and every expectation ('every note listed in INDEX.md') grades that one file. No expectation grades a search-index rebuild, and the fixture offers no command that could perform one.",
      "quote": "**Lint, then rebuild the search index;** fix what the lint names before committing. The fact and its lint pass land in one commit."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 (fallback branch) vs the eval prompts in evals/evals.json",
      "finding": "The fixture has no lint script, so this fallback is the live branch in all three evals, yet no expectation reads LOG.md for the by-hand statement it demands (check.py's log checks grep only for the source name and the disposition word). The step's other closing requirement, that the fact and its lint pass land in one commit, cannot be checked at all: the prompts order in-place editing and a list of changed files, and the bundle contains no repository.",
      "quote": "No lint script in this wiki? Check dangling links, unlisted pages and orphans by hand and say so in the log line."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals/evals.json (all three evals) and evals.md S4",
      "finding": "The cascade is graded by nothing. No eval creates a page, so no neighbour ever needs a sentence; eval 1's only neighbour expectation ('prompt-caching still names [[model-prices]]') checks that a pre-existing edge in the fixture survived, which is a no-regression check, not the cascade. The scenario written for this step, S4, is pending with no executable eval.",
      "quote": "Every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. No true sentence, no edge."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/evals.json (all three evals) and evals/files/check.py",
      "finding": "Step 1 is graded by nothing. The raw files are supplied as fixture inputs that already exist before the run, check.py never inspects a raw copy, a fetch date in a file name, or a raw/MANIFEST.md, and the fixture wiki has no raw/ directory at all. The manifest requirement in particular is produced by no eval and checked by no expectation.",
      "quote": "Save the source bytes where the wiki can re-read them, never edited, with URL or path and fetch date."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md '## Rules' rule 1 vs the steps and the expectations",
      "finding": "A rule nothing can detect a breach of. Neither half is observable in this artefact: check.py never hashes or re-reads a raw file, so an edited raw passes every eval, and 'the wiki is never the only copy of a fact' names a state no step establishes and no expectation inspects.",
      "quote": "- The raw is never edited; the wiki is never the only copy of a fact."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description clause 1 vs step 1 and evals.md S3",
      "finding": "The description promises a source type the body cannot process and the evals never test. A measurement you made yourself, and the transcript case, have no URL and no fetch date, but step 1 requires 'URL or path and fetch date' with no branch for their absence; the only scenario for a source with no retrievable URL (S3) has no executable eval and its criterion ('the note's source is a `note:` entry') matches no step in the body.",
      "quote": "Use when a fetched page, paper, repo, transcript or measurement is about to become a note"
    },
    {
      "level": "CLASS",
      "where": "evals.md S1 and S2 — the Baseline line vs the executed result recorded in the same block",
      "finding": "Each block asserts a baseline failure mode and then records the baseline not failing. S2 states the baseline overwrites or averages, and the heading and result record 'without 1/1 ... the baseline is clean here too' with 'PASS (no delta; baseline clean)'; S1 does the same. The predicted-failure line is left standing as if it were an observation, so a reader cannot tell which scenarios actually separate the arms.",
      "quote": "- **Baseline:** overwrites with the newer number, or averages, or ignores the conflict."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header line vs the per-scenario arm counts (S1, S2, S5)",
      "finding": "The build is described as three arms with k=2, but every executed scenario records four arms — with, without, probe, incumbent — and the without arm is run once, not twice. The header's own parameters contradict the data beneath it.",
      "quote": "the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "S5's input says three facts; the fixture blog restates two (cache reads a tenth of input, writes 1.25x), and rationale.md describes the same probe as 'a blog post restating two multipliers a note already carries'. The count in the scenario matches neither the fixture nor the rationale it cites.",
      "quote": "- **Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md line 49 vs the bundle",
      "finding": "The evidence carrying S6's negative-trigger claim is a trigger matrix that is in no file of the artefact: no path names it, it is in no eval's `files` list, and its three figures cannot be traced to anything shipped. The negative-trigger requirement is asserted as covered by an artefact that is absent.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py T1 'no rival page' vs evals/evals.json eval 1 expectation 1",
      "finding": "The expectation is 'no rival page'; the check only fires when a new note's file stem contains the substring 'pric'. A rival page named e.g. 2026-09-costs or beta-5-rates satisfies the check while violating the expectation and step 2's 'extend it, never a rival'.",
      "quote": "    check(\"no rival page\", not any(s not in (\"model-prices\",\"prompt-caching\",\"local-models\") and \"pric\" in s for s in notes), str(sorted(notes)))"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 (frontmatter status values) vs step 2 and the expectations",
      "finding": "Two of the four status values are set by no step and graded by nothing. Step 2 sets only `disputed`; the fixture notes carry `verified`; nothing in the body says when a page becomes `unverified` or `outdated`, and no expectation ever inspects either value.",
      "quote": "`status` - `verified` / `unverified` / `disputed` (step 2) /"
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py line 24 vs SKILL.md step 6",
      "finding": "The grader requires a stricter form than the step states. Step 6 asks for 'a row in the hand-written map of contents' with no format given, while the check passes only if the literal wikilink [[stem]] appears in INDEX.md; a correct index row written as a plain name fails a check no step could have anticipated.",
      "quote": "    check(f\"index:{stem}\", f\"[[{stem}]]\" in index, \"not in INDEX\")"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md '**Not this skill:**' paragraph vs the frontmatter description",
      "finding": "The body says the sibling names are deferred to the In this repo section, but the description already names all five inline (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator). The body's promise about where local names live is false of the artefact that carries it.",
      "quote": "Each is its own unit - the local names are under *In this repo*."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded — no expectation inspects a saved raw, a fetch date in a filename, or raw/MANIFEST.md; the raws are fixture inputs and check.py never reads them. evals.md S3 would cover it and is pending."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "eval 3: 'no new note', 'LOG.md says no material and names the blog', 'SOURCES.md has a row for the blog' (its 'byte-identical to the fixture' expectation is inert, finding 1); eval 1: 'model-prices is the page updated; no rival page' (weak, finding 20); eval 2: 'a row is marked disputed and the page status is disputed'."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 'a claims-table row carries the verbatim raw line and a verdict word' and eval 2 'a claims row carries 753B, the card's verbatim line and a verdict word' / 'a claims row carries 744B and a verdict word' — one row only, any verdict word; correctness of MEASURED/REPEATED/DERIVED and the 'every number, date and quote' scope are ungraded."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "eval 1/2/3 'every note keeps its frontmatter' (check.py schema: title,status,tags,related,sources), eval 1 'the new source with its fetch date is in model-prices' frontmatter' and 'a Beta 5 row carries $2, $10 and a 2026-09 date' — the closing universal ('every price, version, limit, count and date carries its as-of date') is ungraded beyond that one row."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "ungraded — eval 1's 'prompt-caching still names [[model-prices]]' only checks a pre-existing fixture edge; no eval creates a page with neighbours, and evals.md S4 has no executable eval."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "eval 1 'SOURCES.md has a row for the pricing page' + 'LOG.md has a line naming the source and update'; eval 2 'SOURCES.md has a row for the card' + 'LOG.md names the card and disputed'; eval 3 'SOURCES.md has a row for the blog' + 'LOG.md says no material and names the blog'. Not graded: the map-of-contents row for a new page (no eval creates one) and 'the pages touched' in the log line."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "partly — 'every note keeps its frontmatter; no dangling [[link]]; every note listed in INDEX.md' (all three evals) grades the end state the lint would have caught. Ungraded: the by-hand check stated in the log line, the search-index rebuild, and 'the fact and its lint pass land in one commit' (no lint script, no repository in the fixture)."
    }
  ]
}
```