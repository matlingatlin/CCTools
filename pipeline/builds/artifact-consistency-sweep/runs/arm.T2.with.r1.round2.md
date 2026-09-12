I read the method skill and its `references/pair-vocabulary.md` first, then swept `./artifact-B` (the only `artifact*` directory present: `SKILL.md`, `references/rationale.md`, `evals.md`, `evals/evals.json`, `evals/files/**`).

**Ledger (plan → examined).** Parts: 7 steps · 4 rules · 7 description clauses · 30 evals.json expectations (+6 evals.md scenario criteria) · 12 bundled files besides SKILL.md · **0 bill-of-materials rows (no BOM file exists)** · ~20 named paths.
- step×rule 28 → 28 examined; 3 non-consistent.
- step×step 10 (6 adjacent + 4 shared terms: *index*, *disputed*, *source log*, *raw*) → 10; 3 non-consistent.
- step×check 210 → 210; 7 non-consistent (incl. 2 steps graded by nothing).
- description×body 7 → 7; 2 non-consistent.
- file×BOM 32 → 32; 4 absent (`check.py`, `kb.py`, `raw/MANIFEST.md`, the BOM itself).
- claim×rationale 4 → 4; 3 non-consistent.

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals; bundle root",
      "finding": "21 of the 30 expectations are delegated to a program named check.py that exists nowhere in the bundle (no .py file at all). Every T1/T2/T3 expectation — i.e. every expectation that grades skill-specific behaviour rather than generic frontmatter — is therefore ungradable, and the evals' own 'files' manifests never declare it.",
      "quote": "\"check.py T1: no rival page\" … \"check.py T2: disputed marker\" … \"check.py T3: LOG says no material\" — against \"files\": [\n    \"evals/files/wiki\",\n    \"evals/files/raw/2026-09-02-pricing-page.md\"\n   ]"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules line 4 vs step 7 and Rules line 3",
      "finding": "The rule says the skill runs and fetches nothing, but step 7 orders a lint run and a search-index rebuild (and 'In this repo' spells them as `python3 knowledge/kb.py lint` / `kb.py build`), while another rule orders 'look it up' — a fetch. The rule forbids what two other lines of the same artefact order.",
      "quote": "\"This skill installs, fetches and runs nothing; it is a writing discipline.\" || \"7. **Lint, then rebuild the search index;** fix what the lint names before committing.\" || \"Nothing about a tool, price, version or limit from memory: look it up and date it.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 vs the eval-1 raw fixture",
      "finding": "Step 2 forces exactly one disposition per source, but a source can carry two at once — and the bundle's own fixture proves it: 2026-09-02-pricing-page.md carries a changed Beta price (update) AND a restatement of the caching multipliers the prompt-caching note already holds (no material). The step gives no rule for a mixed source, and no eval-1 expectation says whether prompt-caching may be touched (only eval 3 checks it).",
      "quote": "\"2. **Search, then triage into exactly one:**\" || \"Cache reads are billed at 10% of the input price; cache writes at 125%.\""
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md opening vs SKILL.md ## Rules",
      "finding": "The rationale asserts every rule is backed there and that an unbacked rule does not belong in the body; in fact only rule 1 (raw never edited) has an entry. Rules 2 (null/0), 3 (nothing from memory) and 4 (installs/fetches/runs nothing) have no bullet at all. The rationale's bullets are mostly reasons for STEPS, not for the rules it claims to cover.",
      "quote": "\"Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (disputed branch) vs step 4 (frontmatter status)",
      "finding": "`disputed` is defined at two scopes: step 2 marks it at the contradicting line ('there'), step 4 makes it a page-level frontmatter status value. Nothing says which the eval's 'disputed marker' expectation grades, and the fixture note carries `status: verified` with no stated obligation to change it.",
      "quote": "\"**disputed** (the source contradicts a page: keep both values as dated rows with their sources, mark the page `disputed` there)\" || \"`status` (`verified` / `unverified` / `disputed` / `outdated`)\""
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 (no-material branch) vs step 6",
      "finding": "Step 2's no-material branch says stop — yet it performs step 6's work itself (source-log row + operation-log line), and step 6 declares it also applies on no material. A reader who stops at step 2 never reaches the step that claims the branch; the same two writes are ordered twice.",
      "quote": "\"**no material** (no claim, no value, no newer date for any page: keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop).\" || \"a row per consulted source in the source log (also on no material)\""
    },
    {
      "level": "CLASS",
      "where": "bundle root (no bill of materials) ",
      "finding": "The bundle declares no bill of materials of any kind — no bom.json, no manifest section in SKILL.md. The only file declarations anywhere are the per-eval 'files' arrays, which cover the fixtures only. No bundled file can be checked against a BOM row, and no absent file (check.py, a lint script) is caught by one.",
      "quote": "\"files\": [\n    \"evals/files/wiki\",\n    \"evals/files/raw/2026-09-02-blog-restating-caching.md\"\n   ]"
    },
    {
      "level": "CLASS",
      "where": "evals.md ## Method vs the bundle",
      "finding": "The stated observable criterion for EVERY scenario is a lint run via `knowledge/kb.py lint --json`, but kb.py is not in the bundle and not in the eval fixture wiki (which holds only notes/, INDEX.md, SOURCES.md, LOG.md). Step 7's own fallback ('No lint script?') concedes the script may be absent, so the criterion named for every scenario cannot be applied to any of them.",
      "quote": "\"The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5 vs eval 1 expected_output and the raw fixture",
      "finding": "The expectation labelled 'beta price updated with date' asserts the literal string of the OLD row, which is already present verbatim in the starting fixture model-prices.md. The raw page says Beta 5 is now $2.00/$10.00 effective 2026-09-01. The check passes on an untouched file, contradicts the expected_output ('a dated row per changed price'), and duplicates the separate 'old price kept' expectation.",
      "quote": "\"check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']\" || raw: \"Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expectation 12 vs evals/files/wiki/notes/prompt-caching.md",
      "finding": "The only expectation that grades step 5 (cascade) is already true in the starting fixture: prompt-caching.md carries `related: [\"[[model-prices]]\"]` and links the owner in its body before the agent acts. The check cannot fail, and eval 1's expected_output concedes it ('still names the owner'). Step 5's actual product — one sentence per neighbour saying why the new page matters — is graded by nothing.",
      "quote": "\"check.py T1: neighbour names owner back\" || \"related: [\"[[model-prices]]\"]\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs every expectation and every fixture",
      "finding": "Step 1 is graded by nothing executable. No expectation in evals.json mentions the raw, a content hash, a fetch date in the file name, or raw/MANIFEST.md; the fixture wiki has no raw/ directory and no MANIFEST.md (the raw files sit outside the wiki, as pre-existing inputs), so the step cannot even be exercised. Only pending scenario S3 would touch it.",
      "quote": "\"in a `raw/` directory when the wiki has one, fetch date in the file name, provenance in `raw/MANIFEST.md`.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules line 2",
      "finding": "A rule no step could obey and no expectation grades: no step writes a numeric or nullable field, the step-4 schema has no field where null or 0 could appear, no fixture contains one, and no expectation names either token.",
      "quote": "\"`null` for not-fetched and not-measured; `0` only for a measured zero.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs the eval prompts",
      "finding": "Step 7 makes a single commit carrying both the fact and its lint pass a requirement, but all three eval prompts instruct in-place editing with no commit, and no expectation mentions a commit. The requirement is graded by nothing and is unreachable in the harness as written.",
      "quote": "\"The fact and its lint pass land in one commit.\" || \"Edit the wiki in place and list the files you changed.\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs SKILL.md 'Not this skill' paragraph",
      "finding": "The description's first NOT clause names deep-reading; the body's boundary paragraph lists skill-knowledge, unified-memory, doc-claim-reconciliation and kb-curator and drops summarising/deep-reading entirely. The body claims each is 'named in the description' while covering only four of five.",
      "quote": "\"NOT summarising a text (deep-reading)\" || \"**Not this skill:** claims bundled into a skill's `references/` (`skill-knowledge`); agent task state (`unified-memory`); a document a code change made false (`doc-claim-reconciliation`); cleaning the whole wiki (`kb-curator` agent).\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md 'When to use' vs step 2's four dispositions",
      "finding": "A trigger the body promises has no branch and no eval: a compiled summary page written back is not new, update, disputed or no material, and no step says how to handle one. The description does not carry this trigger either.",
      "quote": "\"An existing note gains a source, or a compiled summary page is written back.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs evals/files/raw/2026-09-02-blog-restating-caching.md and references/rationale.md",
      "finding": "The scenario says the blog restates three facts; the raw fixture restates two (0.1x read, 1.25x write) and the rationale's before/after says two. The count in the eval description does not match the fixture it is executed against.",
      "quote": "\"**Input:** a blog post restating three facts the wiki already holds with the same sources.\" || \"the log says `no material: <url> restates prompt-caching's 0.1x / 1.25x, no new claim`\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md ## Method vs S2 and S5 result lines",
      "finding": "The method reserves 'Beats baseline' for scenarios where the baseline plausibly fails, and labels the rest normal. S5 is labelled normal yet is the sole measured win; S2 is labelled a trap yet reports the baseline clean. The scenario type labels contradict the measured results they carry.",
      "quote": "\"PASS on normal scenarios, \\\"PASS. Beats baseline.\\\" only where the baseline plausibly fails.\" || \"### S5 — no material · normal — EXECUTED as T3: with 2/2; without 0/1, probe 0/2, incumbent 0/2 — the one measured win\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs all 30 expectations and all fixtures",
      "finding": "Two of step 3's five row fields are graded by nothing: no expectation names the locator, and no expectation or fixture exercises DERIVED — neither raw file contains a figure computed from assumed parameters. Only 'verdict word per claim' and 'quote from the raw' are checked, and both only under the absent check.py.",
      "quote": "\"One row per claim: claim, source, locator, verbatim line, verdict - MEASURED (the source measured it), REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters).\""
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 vs all 30 expectations",
      "finding": "Only the frontmatter half of step 4 is graded. The four mandated body sections and the status vocabulary are graded by nothing, and the step's closing instruction points at no inspectable object — nothing says which dates count as 'what will move' or where a reader would look.",
      "quote": "\"body: what it is, the claims graded, what it means here, what is open. Date what will move.\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md 'Not executed in the first build' vs the bundle",
      "finding": "The negative-trigger claim is transferred to a trigger matrix cited with three precise ratios, but no file in the bundle holds that matrix — the numbers are unlocatable and the negative-trigger scenario (S6) has no executable eval, leaving the description's four NOT clauses graded by nothing.",
      "quote": "\"S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4).\""
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S2 vs evals/files/wiki/notes/local-models.md frontmatter",
      "finding": "The scenario attributes the incumbent 744B figure to the vendor's README, but the fixture note's only source is a card URL; its body says README while its frontmatter says gamma-card. The 'both sources dated' expectation therefore grades a provenance the fixture does not consistently state.",
      "quote": "\"the wiki's note says 744B from the vendor's README\" || \"  - url: https://example.test/gamma-card\""
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "ungraded — no expectation in evals.json names the raw, a hash, a dated filename or raw/MANIFEST.md; evals.md S3 would cover it but is 'pending' and has no evals.json entry, and the fixture wiki has no raw/ directory"
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals.json id 3 'check.py T3: prompt-caching unchanged' / 'no new note' / 'LOG says no material' / 'SOURCES row for the consulted source'; id 1 'check.py T1: no rival page'; id 2 'check.py T2: disputed marker' — all behind the absent check.py, and none grades a mixed-disposition source"
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "evals.json id 1/2 'check.py T#: verdict word per claim' and 'quote from the raw/card on the page' (partial — locator and DERIVED graded by nothing); behind the absent check.py"
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "partially — 'every note keeps title/status/tags/related/sources frontmatter' (ids 1-3) and 'check.py T1: new source in note frontmatter with fetch date'; the four body sections and the closing 'Date what will move.' are graded by nothing and end in nothing inspectable"
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "nominally 'check.py T1: neighbour names owner back' plus 'no dangling [[link]]' — but that expectation is already satisfied by the starting fixture, so effectively ungraded; the required sentence per neighbour is graded by nothing, and S4 (pressure) is pending"
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals.json id 1/2 'check.py T#: SOURCES row' and 'LOG row'; id 3 'check.py T3: LOG says no material' and 'SOURCES row for the consulted source' — behind the absent check.py; the map-of-contents row for a new page is graded only indirectly by 'every note is listed in INDEX.md'"
    },
    {
      "step": 7,
      "checkable": true,
      "graded_by": "partially — 'no dangling [[link]]' and 'every note is listed in INDEX.md' (ids 1-3) stand in for the lint; the search-index rebuild, the one-commit requirement and the no-lint-script fallback log line are graded by nothing, and the named grader (kb.py lint --json) is absent from the bundle"
    }
  ]
}
```