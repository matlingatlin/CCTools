I read the method skill (`artifact-consistency-sweep`) and its `references/pair-vocabulary.md`, then swept the artefact at `./artifact-C` (SKILL.md, references/rationale.md, evals.md, evals/evals.json, evals/files/check.py + fixtures; no `bom.json` is present, so the bill of materials is the `files` arrays in evals.json plus the files SKILL.md names).

Plan counts enumerated first — 7 steps, 3 rules, ~24 description clauses, 23 evals.json expectations, 13 files present, 10 BOM rows → step×rule 21, step×step ≥13, step×check 161, description×body ~24, file×BOM 23, claim×rationale ~28.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md description vs SKILL.md body, 'Not this skill' paragraph",
      "finding": "The body promises that the sibling units are named only in the local section, but the description carries all five repo-local names itself. Fixing it rewrites the description, not one line.",
      "quote": "body: \"Each is its own unit - the local names are under *In this repo*.\" || description: \"NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent.\""
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md vs SKILL.md '## Rules'",
      "finding": "rationale.md states as an invariant that every rule is backed by a run or a source, and that an unbacked rule does not belong in the body. Rule 2 (nothing from memory) and rule 3 (installs nothing, fetches no external code) have no bullet in rationale.md at all, and rule 1's second clause ('never the only copy') is unbacked — the 'Raw kept, never edited' bullet covers only its first clause.",
      "quote": "rationale.md: \"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\" || SKILL.md: \"Nothing about a tool, price, version or limit from memory: look it up and date it.\" || SKILL.md: \"This skill installs nothing and fetches no external code.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md '## Rules' vs evals/evals.json (all 23 expectations) and evals/files/check.py",
      "finding": "Not one of the three rules is graded by any expectation or any check. No expectation reads a raw file (rule 1), asks where a figure came from (rule 2), or observes which commands ran (rule 3); check.py never hashes or opens evals/files/raw/.",
      "quote": "SKILL.md: \"The raw is never edited; the wiki is never the only copy of a fact.\" || check.py: \"notes = {p.stem: p.read_text(encoding=\\\"utf-8\\\") for p in (wiki / \\\"notes\\\").glob(\\\"*.md\\\")}\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md rule 3 vs step 7",
      "finding": "Rule 3 closes the allowed command set to the wiki's own query, lint and index commands 'and nothing else'; step 7 orders a commit, which is none of the three. A step orders what a rule forbids.",
      "quote": "rule: \"It runs the wiki's own query, lint and index commands, and nothing else.\" || step 7: \"The fact and its lint pass land in one commit.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md rule 1 (second clause) vs step 1",
      "finding": "Rule 1 forbids the wiki being the only copy of a fact, but the only copy-keeping step puts the raw inside the wiki's own raw/ directory. No step produces a copy outside the wiki, so the rule is one no step could obey.",
      "quote": "rule: \"the wiki is never the only copy of a fact.\" || step 1: \"Where the wiki keeps a `raw/` directory: fetch date in the file name, and provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no material branch) vs steps 6 and 7",
      "finding": "Step 2's branch stops before steps 3-7, yet step 6 asserts its operation-log line happens 'in every branch' and step 7 makes the lint pass and the commit unconditional. In the no-material branch the log and source rows step 2 writes are never linted or committed, and step 6's clause is unreachable.",
      "quote": "step 2: \"keep the raw, write the source-log row and the operation-log line, touch no page, stop.\" || step 6: \"one operation-log line naming the disposition, the source URL and the pages touched, in every branch.\" || step 7: \"The fact and its lint pass land in one commit.\""
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json eval 1 expectation 3 (and check.py T1 'beta_old') vs SKILL.md step 2 update branch",
      "finding": "The eval requires a superseded value to be preserved as a dated row on an ordinary update, and check.py hard-fails without it. No step orders this: only the disputed branch says to keep both values, and the update branch says only to extend. An expectation no step produces.",
      "quote": "evals.json: \"the 2026-08-20 Beta 5 row ($3, $15) is kept as a dated superseded row\" || SKILL.md step 2: \"**update** - a page owns it: extend it, never a rival.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py, T3 branch (lines 51-57) vs evals.json eval 3 expectation 1",
      "finding": "The 'byte-identical to the fixture' check resolves the fixture to check.py's own sibling directory — evals/files/wiki/notes — which is the very directory the eval prompt tells the agent to edit in place. before and after hash the same file, so the check cannot fail. The single measured win of this skill (the no-material branch) is graded by a vacuous check.",
      "quote": "check.py: \"fixture = pathlib.Path(__file__).resolve().parent / \\\"wiki\\\" / \\\"notes\\\"\" and \"check(f\\\"{stem} byte-identical to the fixture\\\", before == after)\" || evals.json prompt: \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "CLASS",
      "where": "evals/files/check.py T1 and T2 vs evals/files/wiki fixture",
      "finding": "Two further checks pass on the untouched fixture. prompt-caching already carries [[model-prices]] in its frontmatter, so the T1 neighbour check is satisfied before any ingest; local-models already contains 2026-08-25, so half of T2's 'both sources dated' is satisfied before any ingest.",
      "quote": "check.py: \"check(\\\"neighbour names owner back\\\", \\\"[[model-prices]]\\\" in notes.get(\\\"prompt-caching\\\",\\\"\\\"))\" || fixture prompt-caching.md: \"related: [\\\"[[model-prices]]\\\"]\" || check.py: \"check(\\\"both sources dated\\\", \\\"2026-08-25\\\" in lm and \\\"2026-09-02\\\" in lm)\" || fixture local-models.md: \"fetched: 2026-08-25\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/evals.json and evals/files/raw/",
      "finding": "Step 1 is graded by nothing. No expectation and no check.py check inspects a raw file, a fetch date in a file name, or a manifest; and the bundled raw fixture contains no manifest, so the artefact the step names is absent from the bundle it ships.",
      "quote": "step 1: \"provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals/evals.json eval 1 expectation 8 and evals.md S4",
      "finding": "The cascade step is graded by nothing executable. None of the three evals creates a page, so no neighbour sentence is ever demanded; the one expectation that names a neighbour is satisfied by the untouched fixture, and the scenario written for this step is unexecuted.",
      "quote": "step 5: \"Every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. No true sentence, no edge.\" || evals.json: \"prompt-caching still names [[model-prices]]\" || evals.md S4: \"**Result:** pending\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/evals.json prompts and expectations",
      "finding": "Step 7 is graded by nothing, and its commit clause is contradicted by the harness: every eval prompt ends at editing files in place and listing them, so no lint run, no index rebuild, no commit and no by-hand say-so line can be observed.",
      "quote": "step 7: \"Lint, then rebuild the search index;\" and \"The fact and its lint pass land in one commit.\" || evals.json prompt: \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Method' vs evals/files/check.py and the bundle",
      "finding": "evals.md names a grader that is not in the bundle and does not exist in the fixture wiki, and never names the grader that is bundled. The bill of materials and the stated grading method disagree about what grades the scenarios.",
      "quote": "evals.md: \"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\" || check.py: \"Shape grader for the llm-wiki-ingest tasks. Run over the wiki AFTER the ingest.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says three restated facts; the rationale and the actual bundled fixture carry two multipliers.",
      "quote": "evals.md S5: \"**Input:** a blog post restating three facts the wiki already holds with the same sources.\" || rationale.md: \"a blog post restates two multipliers a note already carries with a dated source.\" || fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times.\""
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md 'No material means no page is touched' vs evals.md S5",
      "finding": "The rationale counts two baseline runs on the no-material probe; evals.md counts five. The evidence behind the step's rewrite is stated at two different sizes.",
      "quote": "rationale.md: \"every baseline run (2 of 2) still edited the owning page\" || evals.md: \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs evals.md S1/S2/S5 arm lines",
      "finding": "The header declares three arms at k=2; the scenario lines name four arms (with, without, probe, incumbent) and one of them ran at k=1.",
      "quote": "evals.md: \"three arms, k=2, code grader, blinded, preregistered rule\" || evals.md S1: \"EXECUTED as T1: with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Method' vs evals.md S6",
      "finding": "The method claims file state is the observable criterion for every scenario, but the negative-trigger scenario's criterion is which talent fires, which no file state records.",
      "quote": "evals.md: \"The observable criterion for every scenario is the state of the files\" || evals.md S6: \"**Pass criterion:** this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md '## Method' vs evals.md S5 heading and result",
      "finding": "The method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails, yet the scenario carrying that verdict is classed normal.",
      "quote": "evals.md: \"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\" || evals.md: \"### S5 — no material · normal\" ... \"**Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 6 and evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "Step 2 forces exactly one disposition per source, but the bundled eval-1 source is an update for model-prices and no material for prompt-caching (whose 0.1x/1.25x it merely restates). Step 6 then speaks of 'the pages touched' in the plural. The two steps disagree on whether a disposition is per source or per page, and no expectation says what should happen to prompt-caching.",
      "quote": "step 2: \"Search, then triage into exactly one.\" || step 6: \"one operation-log line naming the disposition, the source URL and the pages touched, in every branch.\" || fixture raw: \"Cache reads are billed at 10% of the input price; cache writes at 125%.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py T1 vs evals/evals.json eval 1 expectation 1",
      "finding": "The expectation forbids any rival page; the code only rejects a new note whose stem contains the substring 'pric'. A rival named e.g. 2026-09-model-costs passes the check the expectation was written to fail.",
      "quote": "check.py: \"check(\\\"no rival page\\\", not any(s not in (\\\"model-prices\\\",\\\"prompt-caching\\\",\\\"local-models\\\") and \\\"pric\\\" in s for s in notes), str(sorted(notes)))\" || evals.json: \"model-prices is the page updated; no rival page\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py usage line vs evals/evals.json",
      "finding": "check.py requires a task argument T1|T2|T3, but evals.json identifies its cases as 1, 2, 3 and lists check.py only as a file with no invocation. Nothing in the eval definition binds an eval id to a grader branch; the T1/T2/T3 labels exist only in evals.md and in the code.",
      "quote": "check.py: \"Usage: python3 check.py <wiki_dir> <task: T1|T2|T3>\" || evals.json: \"\\\"id\\\": 1,\" with \"\\\"files\\\": [ ... \\\"evals/files/check.py\\\" ]\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals/evals.json eval 1 expectation 7, eval 2 expectation 8, eval 3 expectation 3",
      "finding": "Step 6 requires the operation-log line to name three things; every expectation checks only two of them. The pages touched are graded by nothing, and check.py's log checks likewise test only the source and the disposition word.",
      "quote": "step 6: \"one operation-log line naming the disposition, the source URL and the pages touched, in every branch.\" || evals.json: \"LOG.md has a line naming the source and 'update'\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md steps 6 and 7 and references/rationale.md vs evals/files/wiki fixture",
      "finding": "The artefact insists the hand-written map of contents and the generated search index are different things, but the bundled wiki contains only INDEX.md and no generated index and no lint script. The distinction the rationale says a review already caught once cannot be exercised by any eval, and step 7's no-lint-script fallback is the branch that always applies while being graded by nothing.",
      "quote": "step 7: \"Lint, then rebuild the search index;\" || rationale.md: \"**Register: map of contents by hand, search index generated.** They are different things; the first draft of this skill conflated them and the whole-artefact review caught it.\" || step 7: \"No lint script in this wiki? Check dangling links, unlisted pages and orphans by hand and say so in the log line.\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "none — no expectation in evals.json and no check in check.py reads evals/files/raw/ at all; evals.md S3 is the only scenario covering the raw and its Result is 'pending'. The manifest the step names is absent from the bundled fixture."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "eval 1 exp 1 ('model-prices is the page updated; no rival page'), eval 2 exp 4 ('a row is marked disputed and the page status is disputed') and exp 8, eval 3 exps 2-4 ('no new note', 'LOG.md says no material and names the blog', 'SOURCES.md has a row for the blog'). Note eval 3 exp 1 ('byte-identical to the fixture') is vacuous per the check.py finding, and the no-rival check is substring-weak."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 exp 4 ('a claims-table row carries the verbatim raw line and a verdict word'); eval 2 exps 2 and 3 (753B and 744B rows with a verdict word). The three verdict words are graded only as a regex alternation, so choosing the wrong one of the three is not graded."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "eval 1 exps 2, 3, 5 and 9; eval 2 exps 4, 6 and 9 (frontmatter keys, status disputed, dated rows). The 'note' subfield of a sources entry and the four-value status vocabulary are not graded."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "none in effect — the only expectation naming a neighbour is eval 1 exp 8 ('prompt-caching still names [[model-prices]]'), which passes on the untouched fixture; no eval creates a page, so no neighbour sentence is ever demanded; evals.md S4 is 'pending'."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "eval 1 exps 6-7, eval 2 exps 7-8, eval 3 exps 3-4 (SOURCES row and LOG line). Two sub-clauses ungraded: the map-of-contents row for a new page (no eval creates one) and 'the pages touched' in the log line."
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "none for the step's own actions — nothing observes a lint run, an index rebuild, a single commit, or the by-hand say-so log line, and the eval prompts end at editing in place. Only the subject matter is indirectly touched by eval 1/2 exp 9 and eval 3 exp 5 ('no dangling [[link]]; every note listed in INDEX.md'), which pass on the untouched fixture."
    }
  ]
}
```