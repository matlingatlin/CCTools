I read every file in the artefact and swept it pair by pair. Here is the report.

## What I examined

`SKILL.md` (7 numbered steps, 4 Rules bullets, description, When-to-use, In-this-repo), `references/rationale.md` (8 bullets + a before/after block), `evals.md` (6 scenarios, 3 executed), `evals/evals.json` (3 evals, 30 expectation strings of which 21 are `check.py T*:` calls), and all 9 bundled fixture files — 3 raw sources, 3 notes, INDEX.md, SOURCES.md, LOG.md. No `bom.json` is supplied, so the file×BOM row resolves every path the artefact's own text names instead.

## Headline

The artefact is internally honest about its *pending* scenarios but not about its *executed* ones. Four expectations shared by all three evals are already true of the fixture before an agent touches it — which is exactly why evals.md records "no delta; baseline clean" on two of three executed scenarios. Separately, T1's only substantive assertion quotes the row it is supposed to prove was replaced, and neither grader named anywhere in the artefact (`check.py`, `knowledge/kb.py`) is bundled with it. Every one of the 7 steps has at least one clause graded by nothing.

Quotes below are verbatim except that `**` bold markers are dropped.

```json
{
  "ledger": {
    "bom": "no bom.json in the artefact - no BOM supplied; the file x BOM row resolves every path the artefact's own text names instead",
    "part_counts": {
      "steps": 7,
      "rules": 4,
      "checks": 30,
      "check_py_expectations": 21,
      "shared_prose_expectations_distinct": 3,
      "evals_md_scenarios": 6,
      "notes_bundled": 3,
      "raws_bundled": 3,
      "rules_outside_the_rules_heading": {
        "when-to-use trigger": "A source has told you something you did not know, and you checked it - the trigger is the verified fact, not the end of the task.",
        "not-this-skill line": "claims bundled into a skill's references/ (skill-knowledge); agent task state (unified-memory)",
        "step 1 immutability": "Save the source bytes where the wiki can re-read them, never edited",
        "step 5 negative rule": "If no true sentence exists, do not add the edge.",
        "evals.md method line": "The observable criterion for every scenario is the state of the files, checked by python3 knowledge/kb.py lint --json and by reading the note."
      }
    },
    "step_x_rule": {
      "plan": 28, "examined": 28, "non_consistent": 2,
      "pairs": ["S1xR1","S1xR2","S1xR3","S1xR4","S2xR1","S2xR2","S2xR3","S2xR4","S3xR1","S3xR2","S3xR3","S3xR4","S4xR1","S4xR2","S4xR3","S4xR4","S5xR1","S5xR2","S5xR3","S5xR4","S6xR1","S6xR2","S6xR3","S6xR4","S7xR1","S7xR2","S7xR3","S7xR4"]
    },
    "step_x_step": {
      "plan": 21, "examined": 21, "non_consistent": 3,
      "pairs": ["S1xS2","S1xS3","S1xS4","S1xS5","S1xS6","S1xS7","S2xS3","S2xS4","S2xS5","S2xS6","S2xS7","S3xS4","S3xS5","S3xS6","S3xS7","S4xS5","S4xS6","S4xS7","S5xS6","S5xS7","S6xS7"]
    },
    "step_x_check": {
      "plan": 63, "examined": 63, "non_consistent": 8,
      "note": "each of the 7 steps against 9 check units - evals.json T1, T2, T3 and evals.md S1..S6; pairs listed per step in compact form",
      "pairs": ["S1 x T1,T2,T3,S1..S6","S2 x T1,T2,T3,S1..S6","S3 x T1,T2,T3,S1..S6","S4 x T1,T2,T3,S1..S6","S5 x T1,T2,T3,S1..S6","S6 x T1,T2,T3,S1..S6","S7 x T1,T2,T3,S1..S6"]
    },
    "description_x_body": {
      "plan": 12, "examined": 12, "non_consistent": 2,
      "pairs": ["trigger-list","karpathy-wiki-naming","natural-language-triggers","raw-kept","triage-four-way","quote-before-write","claim-verdicts","neighbours-name-it-back","index-and-log-rows","lint","not-list-five-siblings","name-field-vs-h1"]
    },
    "file_x_bom": {
      "plan": 14, "examined": 14, "non_consistent": 3,
      "pairs": ["references/rationale.md RESOLVES","check.py x21 MISSING","knowledge/kb.py MISSING","bom.json ABSENT","evals/files/wiki/notes/model-prices.md RESOLVES","evals/files/wiki/notes/prompt-caching.md RESOLVES","evals/files/wiki/notes/local-models.md RESOLVES","evals/files/wiki/INDEX.md RESOLVES","evals/files/wiki/SOURCES.md RESOLVES","evals/files/wiki/LOG.md RESOLVES","evals/files/raw/2026-09-02-pricing-page.md RESOLVES","evals/files/raw/2026-09-02-gamma-model-card.md RESOLVES","evals/files/raw/2026-09-02-blog-restating-caching.md RESOLVES","raw/MANIFEST.md ABSENT-IN-FIXTURE"]
    },
    "step_x_instance": {
      "plan": 11, "examined": 11, "non_consistent": 2,
      "pairs": ["S1xInRepo","S2xInRepo","S3xInRepo","S4xInRepo","S5xInRepo","S6xInRepo","S7xInRepo","R1xInRepo","R2xInRepo","R3xInRepo","R4xInRepo"]
    },
    "claim_x_rationale": {
      "plan": 20, "examined": 20, "non_consistent": 1,
      "pairs": ["S1xRat","S2xRat","S3xRat","S4xRat","S5xRat","S6xRat","S7xRat","R1xRat","R2xRat","R3xRat","R4xRat","Rat1xBody","Rat2xBody","Rat3xBody","Rat4xBody","Rat5xBody","Rat6xBody","Rat7xBody","Rat8xBody","RatBeforeAfterxBody"]
    },
    "other": [
      "evals.md header vs its own scenario arithmetic - check x check, a pair type the seven-type table does not carry",
      "evals.md S5 input description vs rationale.md vs the bundled raw - check x instance",
      "fixture-internal provenance disagreement inside evals/files/wiki - instance x instance"
    ],
    "totals": { "non_consistent_rows": 24, "findings": 15, "steps_with_an_ungraded_clause": 7 }
  },

  "findings": [
    {
      "id": "F1",
      "level": "CLASS",
      "where": "evals/evals.json - the four expectations shared by evals 1, 2 and 3, against evals/files/wiki",
      "what": "Four expectations are already satisfied by the fixture before the agent edits anything, so they cannot separate the with arm from the baseline. All three notes already carry title/status/tags/related/sources. INDEX.md already lists all three notes, and no eval creates a note (T1 asserts no rival page, T3 asserts no new note), so the listing check can never fail. No dangling link exists in the fixture. And model-prices.md and prompt-caching.md already name each other in related:, so 'neighbour names owner back' is a preservation check - evals.json says so itself with the word 'still'. This is the mechanism behind evals.md's own 'PASS (no delta; baseline clean)' on S1 and S2: two of the three executed scenarios are graded largely by checks that pass on an untouched tree.",
      "quote": "check.py T1: neighbour names owner back",
      "quotes": [
        "check.py T1: neighbour names owner back",
        "the neighbour still names the owner",
        "every note is listed in INDEX.md",
        "related: [\"[[prompt-caching]]\"]",
        "related: [\"[[model-prices]]\"]",
        "Result: PASS (no delta; baseline clean)"
      ]
    },
    {
      "id": "F2",
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1, expectation 5, against evals/files/raw/2026-09-02-pricing-page.md and notes/model-prices.md",
      "what": "The expectation named for the update quotes the superseded row, not the new one. The raw prices Beta 5 at $2.00 input and $10.00 output; the string the expectation carries is the row already sitting in model-prices.md at $3 / $15 dated 2026-08-20. Read as a required substring it asserts the old row under a name saying updated, and duplicates the very next expectation; read as a forbidden substring it contradicts that next expectation outright. Either way no expectation anywhere in evals.json names $2 or $10, so the one price the source actually changes - the entire substance of T1 - is graded by nothing.",
      "quote": "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']",
      "quotes": [
        "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']",
        "Beta 5: $2.00 per million input tokens, $10.00 per million output tokens.",
        "check.py T1: old price kept as history or superseded row"
      ]
    },
    {
      "id": "F3",
      "level": "CLASS",
      "where": "file x BOM - evals/evals.json (21 expectations) and evals.md Method line, against the artefact's file list",
      "what": "Every grader the artefact names is absent from it. 21 of the 30 expectation strings are calls to check.py; there is no check.py anywhere under the artefact. evals.md's Method names kb.py lint --json as the observable criterion for every scenario; there is no kb.py in the artefact and the bundled wiki has no lint of any kind - it is a plain directory of markdown. There is no bom.json. So as shipped, not one expectation in evals.json is executable from the artefact, and the three shared prose expectations are the only checks a reader can apply by hand.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by python3 knowledge/kb.py lint --json and by reading the note.",
      "quotes": [
        "The observable criterion for every scenario is the state of the files, checked by python3 knowledge/kb.py lint --json and by reading the note.",
        "check.py T3: SOURCES row for the consulted source",
        "The wiki at evals/files/wiki has notes/, INDEX.md, SOURCES.md and LOG.md."
      ]
    },
    {
      "id": "F4",
      "level": "INSTANCE",
      "where": "step x rule and rule x instance - SKILL.md Rules bullet 4 against step 7, step 2 and the In this repo section",
      "what": "Rule 4 says the skill runs nothing, and three other places in the same file instruct runs. Step 7 orders a lint and an index rebuild. Step 2 orders a query of the wiki's index. The In this repo section spells all three out as shell commands. evals.md's Method adds a fourth. The rule is true only of installs and fetches; as written it contradicts the steps it sits under.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline.",
      "quotes": [
        "This skill installs, fetches and runs nothing; it is a writing discipline.",
        "Lint, then rebuild the search index; fix what the lint names before committing.",
        "python3 knowledge/kb.py find \"<terms>\" / read \"<heading>\"",
        "lint python3 knowledge/kb.py lint; rebuild kb.py build"
      ]
    },
    {
      "id": "F5",
      "level": "INSTANCE",
      "where": "step x step - SKILL.md step 2 against steps 6 and 7, and the description's index clause",
      "what": "Step 2 sends the triage to 'the wiki's index', which steps 6 and 7 split into two different artefacts - a hand-written map of contents and a generated search index. rationale.md records that this exact conflation was already found and fixed once. The fix landed in steps 6 and 7 and in the rationale; step 2 and the description still carry the old singular. It also leaves a circularity: the index step 2 must query is only guaranteed fresh by step 7 of a previous run, and in the bundled fixture the only index that exists is INDEX.md, which step 7 does not rebuild.",
      "quote": "Search, then triage into exactly one: query the wiki's index for the title, trigger terms and URL.",
      "quotes": [
        "Search, then triage into exactly one: query the wiki's index for the title, trigger terms and URL.",
        "a row in the hand-written map of contents for a new page",
        "Register: map of contents by hand, search index generated. They are different things; the first draft of this skill conflated them and the whole-artefact review caught it.",
        "index and log rows, lint"
      ]
    },
    {
      "id": "F6",
      "level": "INSTANCE",
      "where": "step x check - SKILL.md step 1 against evals/evals.json and evals/files/wiki",
      "what": "Step 1 is graded by nothing and cannot be performed on the fixture. It demands a raw/ directory, the fetch date in the file name, a content hash and a provenance row in raw/MANIFEST.md. No expectation in evals.json mentions raw, MANIFEST or a hash. The bundled wiki has notes/, INDEX.md, SOURCES.md and LOG.md - each eval prompt enumerates exactly those four - and no raw/ and no MANIFEST.md; the raw files sit outside the wiki, already saved, so the step is pre-satisfied by the harness. S3, the only scenario stating a raw criterion, is pending.",
      "quote": "Save the source bytes where the wiki can re-read them, never edited, with URL or path, fetch date and a content hash - in a raw/ directory when the wiki has one, fetch date in the file name, provenance in raw/MANIFEST.md.",
      "quotes": [
        "Save the source bytes where the wiki can re-read them, never edited, with URL or path, fetch date and a content hash - in a raw/ directory when the wiki has one, fetch date in the file name, provenance in raw/MANIFEST.md.",
        "the transcript text is saved as the raw",
        "Result: pending"
      ]
    },
    {
      "id": "F7",
      "level": "INSTANCE",
      "where": "step x check - SKILL.md step 5 against evals/evals.json evals 1-3 and evals.md S4",
      "what": "The cascade is graded by nothing executable. Step 5 requires a sentence per neighbour and only then the related: entry, plus a negative rule against adding an unargued edge. The single related expectation, in T1, is pre-satisfied (F1) and tests a link, not a sentence. T2 and T3 carry no cascade expectation at all - and T2 is the one that edits local-models.md, the only note whose related: is empty, so the step's live case is the one left unchecked. S4 is the cascade scenario and its Result is pending, which also means the one discipline pressure the evals.md header claims for this talent is the scenario never run.",
      "quote": "every neighbour the page names gets one sentence saying why it matters to it, then the related: entry. If no true sentence exists, do not add the edge.",
      "quotes": [
        "every neighbour the page names gets one sentence saying why it matters to it, then the related: entry. If no true sentence exists, do not add the edge.",
        "Type: technique (with one discipline pressure)",
        "related: []"
      ]
    },
    {
      "id": "F8",
      "level": "INSTANCE",
      "where": "step x check - SKILL.md step 3 against evals/evals.json expectations for T1 and T2",
      "what": "Step 3's three-way verdict collapses to a single gradeable token. The only check is that a verdict word is present per claim, which any of the three words satisfies, so a run that labels the model card's asserted 753B as MEASURED passes identically to one that labels it REPEATED. DERIVED appears in no bundled raw, so it is unexercised; REPEATED is exercised only by S3, which is pending. The claim row also mandates a locator column, named by no check at all. evals.md S1 states the stricter criterion - the verbatim line and MEASURED specifically - but that strictness is not carried into evals.json.",
      "quote": "One row per claim: claim, source, locator, verbatim line, verdict - MEASURED (the source measured it), REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters).",
      "quotes": [
        "One row per claim: claim, source, locator, verbatim line, verdict - MEASURED (the source measured it), REPEATED (asserted, no measurement), DERIVED (computed from assumed parameters).",
        "check.py T2: verdict word per claim",
        "the owning note gains a dated row with the verbatim line and MEASURED"
      ]
    },
    {
      "id": "F9",
      "level": "INSTANCE",
      "where": "step x check - SKILL.md step 2's new branch and step 6's map-of-contents clause, against evals.json and evals.md",
      "what": "One of step 2's four dispositions is exercised by nothing, and it takes a clause of step 6 down with it. T1 is update, T2 is disputed, T3 is no material; no eval and no evals.md scenario presents a source no page owns. Because nothing creates a page, step 6's INDEX row for a new page is never written, while the shared expectation that every note is listed in INDEX.md passes on the untouched fixture (F1) - so the registration rule looks covered and is not.",
      "quote": "new (no page owns the topic) - update (a page owns it: extend it, never a rival)",
      "quotes": [
        "new (no page owns the topic) - update (a page owns it: extend it, never a rival)",
        "a row in the hand-written map of contents for a new page; a row per consulted source in the source log (also on no material); an operation-log line."
      ]
    },
    {
      "id": "F10",
      "level": "INSTANCE",
      "where": "claim x rationale - references/rationale.md opening claim against SKILL.md Rules bullets 2, 3 and 4",
      "what": "rationale.md asserts completeness over SKILL.md and delivers it only for the Steps. Its eight bullets map to the seven steps and the trigger. Three of the four Rules bullets have no entry - the null-versus-zero rule, the nothing-from-memory rule, and the runs-nothing rule. By rationale.md's own stated test those three do not belong in the body; none of the three is graded by any check either, so they are asserted, unjustified and unmeasured at once.",
      "quote": "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.",
      "quotes": [
        "Every rule in SKILL.md is here with the run or the source it came from; a rule with nothing behind it does not belong in the body.",
        "null for not-fetched and not-measured; 0 only for a measured zero.",
        "Nothing about a tool, price, version or limit from memory: look it up and date it."
      ]
    },
    {
      "id": "F11",
      "level": "INSTANCE",
      "where": "step x instance - SKILL.md step 4's body schema against all three notes in evals/files/wiki/notes",
      "what": "The page schema step 4 mandates is violated by every note the artefact ships and asserted by no check. All three notes are a heading plus one table or one sentence - no what-it-is section, no claims graded, no what-it-means-here, no what-is-open, and no verdict word anywhere. The only schema check lists five frontmatter keys and stops. So a with-arm run that actually restructures a note to step 4 earns nothing, and one that ignores step 4 loses nothing. Two of the four status values, unverified and outdated, appear in no fixture and no check.",
      "quote": "body: what it is, the claims graded, what it means here, what is open. Date what will move.",
      "quotes": [
        "body: what it is, the claims graded, what it means here, what is open. Date what will move.",
        "[[prompt-caching]] multiplies these by 0.1 on a cache read.",
        "Cache reads cost 0.1x of the input price in [[model-prices]]; writes 1.25x.",
        "every note keeps title/status/tags/related/sources frontmatter"
      ]
    },
    {
      "id": "F12",
      "level": "INSTANCE",
      "where": "description x body - SKILL.md frontmatter description against the When to use and Not this skill sections",
      "what": "The two boundary lists disagree in length. The description names five siblings; the body's Not this skill line names four, dropping deep-reading - the one sibling most likely to be confused with this skill, since summarising a fetched page is the nearest neighbouring job. In the other direction, the body carries a second trigger, a compiled summary page written back, which appears in no step, no rule, no scenario and no expectation.",
      "quote": "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation)",
      "quotes": [
        "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge), NOT agent memory (unified-memory), NOT docs broken by code (doc-claim-reconciliation)",
        "Not this skill: claims bundled into a skill's references/ (skill-knowledge); agent task state (unified-memory); a document a code change made false (doc-claim-reconciliation); cleaning the whole wiki (kb-curator agent).",
        "An existing note gains a source, or a compiled summary page is written back."
      ]
    },
    {
      "id": "F13",
      "level": "INSTANCE",
      "where": "other row in the pair-type table - check x check, evals.md header line against its own S1 and S5 scenario lines",
      "what": "The header's arm count and repeat count are both contradicted by the numbers underneath it. The header says three arms at k=2; every executed scenario names four arm labels - with, without, probe, incumbent - and puts one of them at k=1. S5's arithmetic only closes on four: without 0/1 plus probe 0/2 plus incumbent 0/2 is the 0/5 baseline it reports, which requires three baseline arms alongside the with arm. This is a pair type the seven-type table has no row for, so it is reported as an other row.",
      "quote": "three arms, k=2, code grader, blinded, preregistered rule",
      "quotes": [
        "three arms, k=2, code grader, blinded, preregistered rule",
        "with 2/2, without 1/1, probe 2/2, incumbent 2/2",
        "PASS. Beats baseline (0/5 baseline runs vs 2/2 with)"
      ]
    },
    {
      "id": "F14",
      "level": "INSTANCE",
      "where": "other row in the pair-type table - evals.md S5 against references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "what": "The no-material fixture is described with two different claim counts and one false attribution. evals.md S5 calls it three facts; rationale.md calls it two multipliers, twice, and names them; the bundled raw carries two. S5 also says the restated facts come with the same sources, but the blog's source URL is the caching-explained blog while prompt-caching.md's recorded source is a different URL, so the sources are not the same - and this matters, because sameness of source is what would make the no-material triage obvious rather than a judgement call.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources",
      "quotes": [
        "a blog post restating three facts the wiki already holds with the same sources",
        "a blog post restates two multipliers a note already carries with a dated source",
        "Cache reads cost a tenth of the input price and writes cost 1.25 times. That is all.",
        "source: https://example.test/blog/caching-explained"
      ]
    },
    {
      "id": "F15",
      "level": "INSTANCE",
      "where": "other row in the pair-type table - evals/files/wiki/notes/local-models.md body against its own frontmatter, SOURCES.md and LOG.md",
      "what": "The fixture for T2 disagrees with itself about where its incumbent value came from, on the axis the eval grades. The note body attributes 744B to a README dated 2026-08-25, while the same note's frontmatter, the SOURCES row and the LOG line all record the gamma-card URL for that same date. Step 4 makes frontmatter sources the place provenance lives, so the body's parenthetical is an unsourced second provenance record. T2's expectation that both sources are dated therefore grades a disputed pair whose first side has two conflicting origins - and the incoming URL, gamma-7-model-card, differs from the incumbent gamma-card by two characters, so a substring test cannot reliably tell them apart.",
      "quote": "Gamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit.",
      "quotes": [
        "Gamma-7 has 744B total parameters (README, 2026-08-25) and needs 245 GB at 2-bit.",
        "url: https://example.test/gamma-card",
        "| 2026-08-25 | https://example.test/gamma-card | local-models |",
        "check.py T2: both sources dated"
      ]
    }
  ],

  "matrix": [
    {
      "step": 1,
      "title": "Keep the raw",
      "quote": "A transcript or frame text is the raw for a video or image.",
      "checkable": true,
      "checkable_because": "the closing state is a file on disk with a dated name, a hash and a MANIFEST row - all observable",
      "graded_by": "ungraded - no expectation in evals.json names raw, MANIFEST or a hash; the fixture wiki has no raw/ so the step cannot be performed there; evals.md S3 is the only scenario stating a raw criterion and its Result is pending",
      "findings": ["F6"]
    },
    {
      "step": 2,
      "title": "Search, then triage into exactly one",
      "quote": "keep the raw, write the source-log row and one operation-log line with the URL and the reason, touch no page, stop.",
      "checkable": true,
      "checkable_because": "the disposition is exactly one of four and each has a distinct observable file outcome",
      "graded_by": "update by check.py T1 no rival page; disputed by check.py T2 disputed marker; no material by check.py T3 prompt-caching unchanged, no new note and LOG says no material. The new branch is ungraded - no eval or scenario presents a source no page owns. The step also names 'the wiki's index', which steps 6 and 7 hold to be two different things",
      "findings": ["F5", "F9"]
    },
    {
      "step": 3,
      "title": "Locate every number, date and quote in the raw before writing it",
      "quote": "DERIVED (computed from assumed parameters).",
      "checkable": true,
      "checkable_because": "the closing state is a claims table whose columns and verdict tokens are readable off the page",
      "graded_by": "partly - check.py T1 and T2 quote from the raw on the page, and verdict word per claim. Which verdict is chosen is ungraded, the locator column is ungraded, and DERIVED is exercised by no bundled raw",
      "findings": ["F8"]
    },
    {
      "step": 4,
      "title": "Write the page in the schema",
      "quote": "Date what will move.",
      "checkable": true,
      "checkable_because": "frontmatter keys, status value and body sections are all readable off the file",
      "graded_by": "partly - the frontmatter key list on all three evals, check.py T2 disputed marker, check.py T1 new source in note frontmatter with fetch date. The four body sections are ungraded and absent from all three bundled notes; the unverified and outdated status values are ungraded; the sources sub-fields 'path' and 'note' are ungraded (S3 pending)",
      "findings": ["F11"]
    },
    {
      "step": 5,
      "title": "Cascade",
      "quote": "If no true sentence exists, do not add the edge.",
      "checkable": true,
      "checkable_because": "a sentence in the neighbour and a related: entry are both observable, and their absence is too",
      "graded_by": "ungraded - the only related expectation, check.py T1 neighbour names owner back, is satisfied by the fixture before any edit and tests a link rather than a sentence; T2 and T3 carry no cascade expectation; evals.md S4 is pending",
      "findings": ["F1", "F7"]
    },
    {
      "step": 6,
      "title": "Register",
      "quote": "an operation-log line.",
      "checkable": true,
      "checkable_because": "three named files either gain a row or do not",
      "graded_by": "partly - check.py SOURCES row and LOG row on all three evals, including T3's SOURCES row for the consulted source. The map-of-contents row for a new page is ungraded, because no eval creates a page and the shared INDEX expectation passes on the untouched fixture",
      "findings": ["F9"]
    },
    {
      "step": 7,
      "title": "Lint, then rebuild the search index",
      "quote": "No lint script? Hand-check dangling links, unlisted pages and orphans, and say so in the log line.",
      "checkable": true,
      "checkable_because": "a lint verdict, a rebuilt index and a commit containing both are all observable",
      "graded_by": "partly - the three shared prose expectations stand in for a lint, but they are pre-satisfied by the fixture. The index rebuild is ungraded and unperformable (no index builder is bundled); the same-commit clause is ungraded, since every eval prompt asks only to edit in place and list the files changed; the no-lint-script fallback that the fixture actually triggers is ungraded",
      "findings": ["F1", "F3"]
    }
  ]
}
```

## The three things I would fix first

1. **F2** — T1's substantive expectation quotes the row it should prove was replaced. Nothing in the suite asserts `$2` / `$10` landed, so the update scenario's whole point is ungraded.
2. **F1/F3** — the four shared expectations pass on an untouched tree, and neither named grader is bundled, so "no delta; baseline clean" on S1 and S2 is a property of the checks, not of the baseline.
3. **F5/F10** — the index conflation `rationale.md` says was already caught survives in step 2 and the description, and three of four Rules bullets fail `rationale.md`'s own belongs-in-the-body test.

One thing out of scope but worth naming: `evals.md` records **ITERATE — Status stays candidate**, while this repo's `CLAUDE.md` capability map lists `llm-wiki-ingest` as *measured 2026-09-03, first v3 build, ship*. That is artefact-versus-repo, not internal, so I did not file it as a finding.