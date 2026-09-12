```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "SKILL.md frontmatter description vs SKILL.md body 'Not this skill'",
      "finding": "The body states that the local sibling names are kept out of the general text and live under 'In this repo', but the description itself carries five repo-local unit names (deep-reading, skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator). The two parts assert opposite placements for the same names.",
      "quote": "body: \"Each is its own unit - the local names are under *In this repo*.\" || description: \"NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation); whole-wiki clean-up is the kb-curator agent.\""
    },
    {
      "level": "CLASS",
      "where": "evals.md '## Method' vs evals/files/check.py (file x bill of materials)",
      "finding": "evals.md declares one grader for every scenario - knowledge/kb.py lint --json - which is not in the bundle (the bundled fixture wiki has no kb.py and no lint script at all). The grader that actually exists and is copied into every eval run, evals/files/check.py, is named nowhere in evals.md. Every scenario's stated observable criterion therefore rests on an absent file.",
      "quote": "evals.md: \"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\" || evals.json: \"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 'new' branch and step 6 vs evals.md scenarios and evals/evals.json",
      "finding": "Triage has four branches; the evals exercise three (update = eval 1, disputed = eval 2, no material = eval 3). No scenario in evals.md and no eval in evals.json creates a new page, so the 'new' branch is graded by nothing - and with it step 6's new-page map-of-contents row and step 5's cascade for a new page. evals.md's 'Not executed in the first build' paragraph lists S3/S4/S6 as the gap and does not admit this one.",
      "quote": "SKILL.md: \"**new** - no page owns the topic.\" || SKILL.md: \"A row in the hand-written map of contents for a new page\" || evals.md: \"S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet\""
    },
    {
      "level": "CLASS",
      "where": "evals.md scenario results S1/S2 vs the eval set as a whole",
      "finding": "Of the three executed scenarios, two record no difference between arms (baseline 5/5 clean), including the one labelled 'trap'. A trap whose baseline passes every run grades nothing about the skill; only T3 discriminates, which is also what the recorded verdict rests on.",
      "quote": "\"### S2 — a source that contradicts a page · trap — EXECUTED as T2: with 2/2, without 1/1, probe 2/2, incumbent 2/2 (the baseline is clean here too)\" || \"**Result:** PASS (no delta; baseline clean)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/files/check.py T3 branch vs the eval 3 prompt",
      "finding": "The T3 'byte-identical to the fixture' check computes the reference hash from check.py's own sibling directory - the very wiki the prompt tells the agent to edit in place - so before and after are the same bytes and the check cannot fail. The central expectation of the only scenario that beat baseline is graded by a comparison of a file with itself.",
      "quote": "check.py: \"fixture = pathlib.Path(__file__).resolve().parent / \\\"wiki\\\" / \\\"notes\\\"\" || evals.json: \"model-prices, prompt-caching and local-models are byte-identical to the fixture\" || prompt: \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 5 vs evals.json eval 1 expectation 8 / check.py 'neighbour names owner back'",
      "finding": "The only expectation offered for the cascade step asserts a link that already exists in the untouched fixture (prompt-caching's body and frontmatter both name [[model-prices]] before any ingest). The check passes on the unmodified wiki, so step 5 - the sentence-per-neighbour requirement - is graded by nothing.",
      "quote": "SKILL.md: \"Every neighbour the page names gets one sentence saying why it matters to it, then the `related:` entry. No true sentence, no edge.\" || evals.json: \"prompt-caching still names [[model-prices]]\" (fixture already reads: \"Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.\")"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs the eval fixture layout and every expectation",
      "finding": "Step 1 orders a raw directory manifest carrying source, date, hash, size and target page, and orders the raw be saved where the wiki can re-read it. In the bundle the raw sits outside the wiki (evals/files/raw/ beside evals/files/wiki/), there is no manifest, and no expectation in any of the three evals mentions the raw or the manifest at all.",
      "quote": "SKILL.md: \"provenance (source, date, hash, size, which page it feeds) in the directory's manifest rather than inside the immutable file\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md rule 3 vs step 1 and step 7",
      "finding": "Rule 3 confines execution to the wiki's own query, lint and index commands 'and nothing else', while step 1 orders a hash to be recorded (obtainable from none of those three) and step 7's fallback orders dangling-link, unlisted-page and orphan checks in a wiki that has no lint script. A rule no step could obey as written.",
      "quote": "\"This skill installs nothing and fetches no external code. It runs the wiki's own query, lint and index commands, and nothing else.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no-material 'stop') vs step 7",
      "finding": "Step 2's no-material branch ends in 'stop', while step 7 orders lint, index rebuild and a single commit unconditionally, with no branch qualifier. Nothing in the artefact says whether step 7 runs after a no-material stop, and eval 3 requires none of it, so the disagreement is never forced to resolve.",
      "quote": "step 2: \"keep the raw, write the source-log row and the operation-log line, touch no page, stop.\" || step 7: \"Lint, then rebuild the search index; fix what the lint names before committing.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs all three eval prompts",
      "finding": "Step 7's terminal requirement is a commit containing both the fact and its lint pass. No eval commits anything - every prompt ends at editing in place and listing changed files - and no expectation mentions a commit or a lint run, so the closing requirement of the last step is graded by nothing and cannot be graded by this harness.",
      "quote": "SKILL.md: \"The fact and its lint pass land in one commit.\" || evals.json: \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md opening claim vs SKILL.md rules 1 and 3 and step 4",
      "finding": "rationale.md asserts that every rule in SKILL.md appears there with its evidence. Rule 3 (installs nothing / runs only the wiki's own commands) has no entry, rule 1's second clause ('the wiki is never the only copy of a fact') has no entry, and step 4's schema has no entry - although the file's own title promises the failure behind each step.",
      "quote": "rationale.md: \"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 input vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "S5 describes the fixture as restating three facts held with the same sources. The fixture blog restates two multipliers, and it carries a new URL (blog/caching-explained) that prompt-caching does not hold (its source is example.test/caching) - which is why eval 3 requires a new SOURCES row for it. rationale.md describes the same case as two multipliers.",
      "quote": "evals.md: \"a blog post restating three facts the wiki already holds with the same sources\" || fixture: \"Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.\" || rationale.md: \"a blog post restates two multipliers a note already carries with a dated source\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals.json eval 1 expectation 4 and check.py T1",
      "finding": "The scenario's pass criterion demands the verdict MEASURED specifically; the executed expectation and the grader accept any of the three verdict words, so a run grading the price REPEATED passes the check while failing the documented criterion.",
      "quote": "evals.md: \"the owning note gains a dated row with the verbatim line and MEASURED\" || check.py: \"re.search(r\\\"MEASURED|REPEATED|DERIVED\\\", l)\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs the bundled grader",
      "finding": "Two of S1's four stated criteria are graded by nothing: no lint exists in the bundle to report 0 errors, and check.py never tests that INDEX is unchanged - its INDEX check asserts the opposite kind of fact (that every note, including any new one, is listed).",
      "quote": "evals.md: \"lint reports 0 errors; INDEX unchanged, SOURCES +1 row\" || check.py: \"check(f\\\"index:{stem}\\\", f\\\"[[{stem}]]\\\" in index, \\\"not in INDEX\\\")\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S6 'Result' vs evals.md 'Not executed in the first build'",
      "finding": "S6 is recorded as pending and simultaneously as carried by a trigger matrix. The trigger matrix and the three numbers quoted from it exist in no bundled file, so the substitute grader for the negative trigger is itself absent from the artefact.",
      "quote": "\"**Result:** pending\" || \"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header line vs the S1/S2/S5 arm counts",
      "finding": "The header records three arms at k=2; the scenario lines record four arms (with, without, probe, incumbent) and k=1 for the 'without' arm in all three executed scenarios.",
      "quote": "header: \"three arms, k=2, code grader, blinded, preregistered rule\" || S1: \"with 2/2, without 1/1, probe 2/2, incumbent 2/2\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs evals.json expectations and check.py",
      "finding": "Step 4 specifies a five-column Claims table and four named body sections. The grader accepts any line beginning with a pipe that contains the quote and a verdict word; the locator column, the '## Claims' heading, and 'what it is / what it means here / what is open' are graded by nothing.",
      "quote": "SKILL.md: \"a `## Claims` table with one row per claim - claim | source | locator | verbatim quote | verdict; what it means here; what is open\" || check.py: \"claim_rows = [l for l in mp.splitlines() if l.strip().startswith(\\\"|\\\") ...]\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.json eval 1 expectation 1 vs check.py T1 'no rival page'",
      "finding": "The expectation forbids any rival page; the check only detects a rival whose file stem contains the substring 'pric', so a rival note named e.g. model-costs-2026-09 satisfies the grader while violating the expectation and step 2's 'extend, never a rival'.",
      "quote": "check.py: \"check(\\\"no rival page\\\", not any(s not in (\\\"model-prices\\\",\\\"prompt-caching\\\",\\\"local-models\\\") and \\\"pric\\\" in s for s in notes), str(sorted(notes)))\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals.json expectations and check.py",
      "finding": "Step 3 permits claim rows to live either in the page's Claims table or in a wiki-level claims ledger. Every expectation and every grader row requires them inside the note, so a run taking the permitted second branch fails the eval that is supposed to grade the step.",
      "quote": "SKILL.md: \"The claim rows go in the page's `## Claims` table (step 4) or in the wiki's claims ledger where one exists.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs the steps and the eval set",
      "finding": "The description names five source kinds. Step 1 handles a page, a transcript and frame text; nothing in the body or in any scenario says how a repo or a bare measurement becomes raw, is quoted verbatim, or is graded. All three fixtures are markdown pages.",
      "quote": "description: \"Use when a fetched page, paper, repo, transcript or measurement is about to become a note\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": false,
      "graded_by": "ungraded — its closing sentence is a definition ('A transcript or frame text is the raw for a video or image.') that ends in no file, number or state; no expectation in evals.json touches the raw or the manifest, and the fixture raw/ has no manifest"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "partly graded — update: evals.json #1 'model-prices is the page updated; no rival page'; disputed: #2 'a row is marked disputed and the page status is disputed'; no material: #3 'no new note' and 'LOG.md says no material and names the blog'. The 'new' branch: ungraded"
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json #1 'a claims-table row carries the verbatim raw line and a verdict word'; #2 'a claims row carries 753B, the card's verbatim line and a verdict word' and 'a claims row carries 744B and a verdict word'. The MEASURED/REPEATED/DERIVED distinction itself is ungraded — any verdict word passes"
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "partly graded — evals.json #1 'a Beta 5 row carries $2, $10 and a 2026-09 date' and 'the new source with its fetch date is in model-prices' frontmatter'; #2 'both sources dated 2026-08-25 and 2026-09-02'; check.py's schema row grades the five frontmatter keys. The locator column and the four body sections: ungraded"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "ungraded — the only candidate, evals.json #1 'prompt-caching still names [[model-prices]]', is already true in the untouched fixture; no expectation requires a neighbour to gain a sentence naming the new or updated page"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "partly graded — evals.json #1 'SOURCES.md has a row for the pricing page' and 'LOG.md has a line naming the source and update'; #2 'SOURCES.md has a row for the card' and 'LOG.md names the card and disputed'; #3 'SOURCES.md has a row for the blog'. The map-of-contents row for a new page and 'the pages touched' in the log line: ungraded"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "ungraded as written — the fixture wiki has no lint script and no index builder, and no expectation requires the log line to say the by-hand checks were done, nor the single commit. Only the resulting state is touched, by evals.json's common 'every note keeps its frontmatter; no dangling [[link]]; every note listed in INDEX.md', which passes on the untouched fixture"
    }
  ]
}
```