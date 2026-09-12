```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals, 16 expectations",
      "finding": "Every substantive expectation is delegated to a grader script `check.py` that is not present anywhere in the artefact (bundle contains only SKILL.md, evals.md, evals/evals.json, evals/files/**, references/rationale.md). Every step-level claim these expectations are supposed to grade is therefore graded by nothing runnable.",
      "quote": "check.py T1: no rival page"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs evals/evals.json",
      "finding": "Two different and mutually inconsistent graders are named for the same scenarios: evals.md says the criterion is checked by the host repo's `kb.py lint --json`, evals.json says `check.py`. Neither exists in the artefact, and the bundled fixture wiki (evals/files/wiki) contains no lint script at all.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval id 1 vs evals/files/raw/2026-09-02-pricing-page.md and evals/files/wiki/notes/model-prices.md",
      "finding": "The expectation labelled 'beta price updated' quotes the fixture's OLD, unchanged row. The raw says 'Beta 5: $2.00 per million input tokens, $10.00 per million output tokens' effective 2026-09-01, but the asserted string is the pre-existing '| Beta 5 | $3 | $15 | 2026-08-20 |'. The check passes on a note nobody touched, so the one price change the scenario exists to test is graded by a string that is true before the ingest.",
      "quote": "check.py T1: beta price updated with date ['| Beta 5 | $3 | $15 | 2026-08-20 |']"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs SKILL.md step 3",
      "finding": "S1 requires the price claims be graded MEASURED, but step 3 defines MEASURED as 'the source measured it' and REPEATED as 'asserted, no measurement'. A vendor pricing page asserts prices; it measures nothing. The eval demands the verdict the body's own definition forbids.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 vs references/rationale.md and evals/files/raw/2026-09-02-blog-restating-caching.md",
      "finding": "The scenario says the blog restates three facts; the rationale and the actual bundled fixture both say two multipliers (0.1x cache read, 1.25x write). The fixture blog carries exactly two claims.",
      "quote": "a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "references/rationale.md 'No material' bullet vs evals.md S5",
      "finding": "The same measurement is reported with two different baseline denominators: the rationale says every baseline run, 2 of 2, edited the page; evals.md reports the same scenario as 0/5 baseline runs (without 0/1, probe 0/2, incumbent 0/2). The one measured win in the artefact is cited with contradictory counts.",
      "quote": "every baseline run (2 of 2) still edited the owning page"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md §Rules vs steps 2 and 7 and §In this repo",
      "finding": "The rule says the skill runs nothing, but step 2 orders you to query the index, step 7 orders 'Lint, then rebuild the search index', and the repo instance names the commands to run (`kb.py find`, `kb.py lint`, `kb.py build`). The rule also says it fetches nothing while the trigger, step 1 and the rule about looking things up all presuppose a fetch.",
      "quote": "This skill installs, fetches and runs nothing; it is a writing discipline."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (no material branch) vs step 7",
      "finding": "The no-material branch ends the procedure before step 7, yet step 7 declares lint mandatory before any commit and requires the fact and its lint pass to land together. The no-material path also performs step 6's registration inside step 2, so the same two registers are specified twice with different wording.",
      "quote": "touch no page, stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals/files/raw/2026-09-02-pricing-page.md (eval id 1)",
      "finding": "Triage is required to land on exactly one disposition per source, but the artefact's own eval-1 raw carries material for two notes at once: prices that update model-prices and caching multipliers ('Cache reads are billed at 10% of the input price; cache writes at 125%') that are no material for prompt-caching. No expectation in eval 1 grades what happens to prompt-caching, so the ambiguity is both unresolved by the body and ungraded.",
      "quote": "Search, then triage into exactly one:"
    },
    {
      "level": "CLASS",
      "where": "references/rationale.md preamble vs SKILL.md §Rules and steps 2/4",
      "finding": "The rationale asserts that every rule in the body appears in it, but several do not: the null/0 rule, the never-from-memory rule, the installs/fetches/runs-nothing rule, step 2's search-the-index-first clause, and step 4's whole frontmatter schema and status enum have no entry. By the rationale's own criterion those rules 'do not belong in the body'.",
      "quote": "a rule with nothing behind it does not belong in the body."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md §Rules bullet 2",
      "finding": "This rule is attached to no step (step 4's schema declares no numeric or nullable field), is absent from the rationale, and no eval expectation mentions null or zero. It is a rule with no procedure and no grader.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md §When to use bullet 2",
      "finding": "A compiled summary page written back is offered as a trigger, but step 2's triage has no branch for it (new/update/disputed/no material all assume an incoming external source), no rule covers it, the description never mentions it, and no eval exercises it.",
      "quote": "An existing note gains a source, or a compiled summary page is written back."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 4 and step 7",
      "finding": "S3 grades against two things the artefact never defines: a `note:` source entry standing in for a URL (step 4 lists 'note' as a field alongside url/path, not as a substitute for one) and lint severity levels INFO vs ERROR, which appear nowhere in SKILL.md, the rationale, or any lint the bundle ships.",
      "quote": "the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs S6",
      "finding": "The Method states the observable criterion for EVERY scenario is the state of the files, but S6's criterion is which skill fires — not a file state. The stated method cannot grade the negative-trigger scenario it claims to cover.",
      "quote": "this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page)."
    },
    {
      "level": "CLASS",
      "where": "evals.md pass criteria (S1, S2, S5) vs evals/evals.json expectations",
      "finding": "The two eval records specify different things for the same scenarios. S1 requires 'lint reports 0 errors', 'INDEX unchanged' and 'SOURCES +1 row'; evals.json id 1 has no lint check, no INDEX-unchanged check (it asserts the opposite shape, 'every note is listed in INDEX.md') and no row-count check. The prose criteria are not the criteria that run.",
      "quote": "no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval id 1 vs evals/files/wiki/notes/prompt-caching.md",
      "finding": "The only check for step 5's cascade is satisfied by the fixture's initial state: prompt-caching already carries `related: [\"[[model-prices]]\"]` and already names it in prose, and eval 1 creates no new neighbour. The check passes whether or not the cascade step is performed, and nothing anywhere grades step 5's required sentence as opposed to the bare edge.",
      "quote": "check.py T1: neighbour names owner back"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 'new' branch vs evals/evals.json (all three evals)",
      "finding": "The lead disposition of the triage — new — is exercised by no bundled eval: id 1 is an update, id 2 a disputed update, id 3 no material. Consequently step 4's schema for a freshly written page and step 6's map-of-contents row (specified only 'for a new page') are graded by nothing, while the executable expectation 'every note is listed in INDEX.md' only ever re-checks the three pre-existing fixture notes.",
      "quote": "**new** (no page owns the topic)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs evals/files/** (bill of materials)",
      "finding": "Step 1 mandates a content hash and a provenance row in `raw/MANIFEST.md`, but no MANIFEST.md exists anywhere in the artefact, the fixture wiki has no raw/ directory of its own (the raws sit outside it at evals/files/raw/), and no expectation in any eval mentions a manifest, a hash, or the raw at all. The step the description leads with ('Raw kept') is graded by nothing.",
      "quote": "provenance in `raw/MANIFEST.md`"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs step 4 vs evals/evals.json eval id 2",
      "finding": "Two incompatible placements for the disputed marker: step 2 marks the page disputed at the contested line, step 4 makes `disputed` one value of a page-level frontmatter `status`. The grading expectation is the bare phrase 'disputed marker', which cannot distinguish them, and the generic frontmatter expectation would also be satisfied by leaving `status: verified` untouched.",
      "quote": "mark the page `disputed` there"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 vs evals.md S5 vs evals/evals.json eval id 3",
      "finding": "The no-material log line is specified three different ways: the body requires the URL and the reason, S5 requires the URL and the date, evals.json expects only the source URL. No two agree on the required fields of the single artefact this branch produces.",
      "quote": "one operation-log line with the URL and the reason"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Not executed in the first build",
      "finding": "The negative-trigger claim is discharged by citing a trigger matrix with precise numbers, and a follow-up item '2.4', neither of which exists in the artefact. The only evidence offered for the one scenario that has no executable eval is unbundled.",
      "quote": "S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4)."
    },
    {
      "level": "CLASS",
      "where": "evals.md S1 and S2 — Baseline line vs measured Result line",
      "finding": "Each executed scenario asserts a baseline failure mode and then reports, in the same block, that the baseline never exhibited it ('with 2/2, without 1/1, probe 2/2, incumbent 2/2', 'PASS (no delta; baseline clean)'). The asserted failure is contradicted by the measurement printed beside it, leaving the scenario's rationale for existing unsupported.",
      "quote": "states the prices in chat, or writes a new \"pricing-2026-09\" note beside the owner."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md §Method vs S5 and S2 classifications",
      "finding": "The method reserves the 'Beats baseline' verdict for scenarios where the baseline plausibly fails, yet S5 is classified 'normal' and is the only scenario awarded that verdict, while S2 is classified 'trap' and is reported as a clean baseline. The classification and the verdict rule disagree in both directions.",
      "quote": "PASS on normal scenarios, \"PASS. Beats baseline.\" only where the baseline plausibly fails."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 vs evals/files/wiki/notes/local-models.md",
      "finding": "Step 7 makes orphans a defect to be hand-checked and reported, but the bundled fixture ships one: local-models has `related: []` and is named by no other note, so the fixture is red against the step before any ingest begins. No eval expectation covers orphans or one-way links, only 'no dangling [[link]]'.",
      "quote": "Hand-check dangling links, unlisted pages and orphans, and say so in the log line."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 vs evals.md §Method",
      "finding": "Step 3 is an ordering requirement — locate before writing — but the artefact's stated criterion is end-state file content, which cannot distinguish a claim quoted before writing from one quoted after. The required `locator` field of the claims row is likewise graded by nothing; the expectations check only a quote and a verdict word.",
      "quote": "Locate every number, date and quote in the raw before writing it."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4 second half",
      "finding": "The body shape and the dating instruction are stated without any observable form (no required headings, no definition of 'what will move'), and no expectation in any eval reads the body structure — the frontmatter expectation is the only part of step 4 that is graded.",
      "quote": "body: what it is, the claims graded, what it means here, what is open. Date what will move."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md frontmatter description vs evals/evals.json",
      "finding": "The description sells lint as part of the shape the skill guarantees, and step 7 makes it the closing gate, but no bundled eval runs a lint, the fixture wiki contains no lint script, and the eval prompts ask only to edit in place and list changed files. The promise in the description has no grader.",
      "quote": "index and log rows, lint."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs S4",
      "finding": "The talent is typed as carrying one discipline-pressure scenario, but that scenario (S4, cascade under time pressure) is marked pending and has no entry in evals.json, so the qualifier in the type line rests on nothing executed.",
      "quote": "**Type:** technique (with one discipline pressure)"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "nothing. No expectation in evals/evals.json mentions the raw, a fetch date, a content hash or raw/MANIFEST.md; the raws are supplied pre-saved outside the fixture wiki. evals.md S3 is the only place the raw is a criterion and it is marked 'pending'."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "the disposition is graded by consequence: eval 1 'check.py T1: no rival page' (update), eval 2 'check.py T2: disputed marker' (disputed), eval 3 'check.py T3: no new note' + 'check.py T3: prompt-caching unchanged' + 'check.py T3: LOG says no material' (no material). The 'new' branch and the 'query the wiki's index' clause are graded by nothing."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "eval 1 'check.py T1: quote from the raw on the page' + 'check.py T1: verdict word per claim'; eval 2 'check.py T2: quote from the card on the page' + 'check.py T2: verdict word per claim'. The 'before writing' ordering, the locator field, and the correctness of which verdict was chosen are graded by nothing (and evals.md S1 demands MEASURED where step 3's definition gives REPEATED)."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "'every note keeps title/status/tags/related/sources frontmatter' (all three evals), plus eval 1 'check.py T1: new source in note frontmatter with fetch date' and eval 2 'check.py T2: model card in frontmatter sources'. The status enum, the body sections and 'Date what will move' are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "only eval 1 'check.py T1: neighbour names owner back' and the generic 'no dangling [[link]]' — and the former is already true in the fixture before any ingest, so it grades nothing the step does. The required sentence per neighbour is graded by nothing; evals.md S4, the scenario written for this step, is pending."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "the source-log and operation-log rows are graded in all three evals ('check.py T1/T2: SOURCES row', 'LOG row', 'check.py T3: SOURCES row for the consulted source', 'check.py T3: LOG says no material'). The map-of-contents row is graded by nothing, because no eval creates a new page; 'every note is listed in INDEX.md' only re-checks the three fixture notes."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "nothing. No lint or index-build exists in the artefact or the fixture wiki; evals.md points at the host repo's kb.py while evals.json points at an absent check.py; and the commit clause cannot be observed at all — the eval prompts say only 'Edit the wiki in place and list the files you changed', with no git step in any scenario."
    }
  ]
}
```