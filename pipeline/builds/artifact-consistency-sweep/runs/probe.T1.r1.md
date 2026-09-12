```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three evals",
      "finding": "Every eval's expectations array is empty, so no eval check grades anything. Grading rests entirely on prose expected_output; not one numbered step in SKILL.md is graded by an executable check anywhere in the artefact.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json files lists vs the bundled files (bill of materials)",
      "finding": "All three evals declare a grader file evals/files/check.py, but no such file is bundled — the artefact contains only SKILL.md, evals.md, evals/evals.json, evals/files/raw/*.md and evals/files/wiki/*. The one thing that could have made the evals checkable is missing.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md (six scenarios) vs evals/evals.json (three evals)",
      "finding": "S3 (edge), S4 (pressure) and S6 (negative-trigger) exist only as prose; the runnable suite contains no negative-trigger case, no pressure case and no edge case, so the steps those scenarios were written to grade (raw-keeping for a URL-less source, cascade, non-firing) are graded by nothing runnable.",
      "quote": "### S6 — a claim to bundle into a skill · negative-trigger"
    },
    {
      "level": "CLASS",
      "where": "evals.md \"Method\" vs evals/files/wiki/",
      "finding": "The stated universal observable criterion for every scenario is a repo-specific tool (knowledge/kb.py) that is not bundled and cannot run against the standalone fixture wiki, which is a plain directory of markdown with no lint. Every scenario therefore names a check that cannot be performed on the artefact's own fixtures.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md steps 3–4 vs evals/files/wiki/notes/*.md",
      "finding": "The mandated claim-row and page schema does not exist in the fixture notes: model-prices.md has a bare price table (no locator, no verbatim line, no verdict), local-models.md is a single prose sentence, and neither has the body sections step 4 requires. A run that follows steps 3–4 produces a page unlike the fixture; a run that matches the fixture violates steps 3–4. Nothing in the artefact says which wins.",
      "quote": "A claim is one row: what it says, source, locator, verbatim line, and a verdict"
    },
    {
      "level": "CLASS",
      "where": "evals.md header and every \"Result:\" line",
      "finding": "The suite has never been run and every scenario verdict is pending, so no step is graded by a check that has actually passed — the artefact's grading is entirely prospective.",
      "quote": "**Last eval:** not run — suite authored 2026-09-02, status candidate until `eval-harness` baseline-vs-with has run · **Verdict:** pending"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals.md S1 pass criterion",
      "finding": "Step 6 requires an index row unconditionally for every ingest; S1's pass criterion requires the index to be unchanged for exactly the update case. A run cannot satisfy both.",
      "quote": "6. **Register.** One row in the index (map of contents), one row per source in the source log, one entry in the operation log"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 3 definition of MEASURED vs SKILL.md \"Example\" and evals.md S1",
      "finding": "Step 3 defines MEASURED as requiring a dependent variable, effect and sample; a vendor price list has none of those and is an assertion (REPEATED). Yet both the Example and S1's pass criterion require the price row to be graded MEASURED. The skill's own worked example and its normal-case eval violate its verdict rule.",
      "quote": "the note gets a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (\"exactly one of\") vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "Triage is defined as exactly one bucket per source, but eval 1's own fixture is an update for model-prices AND a restatement of values prompt-caching already holds (no material). The fixture makes the step's exclusivity unsatisfiable, and nothing grades which bucket was chosen for which page.",
      "quote": "Triage into exactly one of: **new** (no page owns the topic)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 1 vs SKILL.md step 4 frontmatter schema and the fixture notes",
      "finding": "Step 1 requires a content hash in the page's source entry, but step 4's source-entry schema is url/path, fetch date and note — no hash field — and no fixture note carries one. The requirement is contradicted by the schema it must be written into and is graded by nothing.",
      "quote": "the copy goes there with the fetch date in the file name and a content hash in the page's source entry"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4",
      "finding": "The status vocabulary is called fixed but is defined nowhere in the artefact — there is no references/ directory, and the In-this-repo pointer (claims.contract.json) is said to define claim fields and the three verdicts, not statuses. The step cannot be checked: 'verified' and 'disputed' appear in fixtures with no enumeration to check against.",
      "quote": "status from the fixed vocabulary, tags, related"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7 heading vs its body, and vs step 6",
      "finding": "The heading promises a rebuild the body never describes (the body specifies only the lint and fixing what it names). A deterministic index rebuild would also overwrite or duplicate the index row step 6 requires to be hand-written, and no eval grades either half.",
      "quote": "7. **Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names before committing."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 (\"and stop\") vs steps 6 and 7 and the Rules",
      "finding": "The no-material branch stops after the log line, skipping the source-log row step 6 requires per source and the lint step 7 requires before committing. Whether a no-material ingest is exempt from the source log and the lint is left contradictory; eval 3's expected_output silently assumes the exemption.",
      "quote": "**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 observation vs evals.md status",
      "finding": "SKILL.md cites observed baseline runs dated 2026-09-02 as evidence for the no-material rule, while evals.md, dated the same day, states the suite has not been run and every result is pending. One of the two is false; no n is given for 'every baseline run'.",
      "quote": "Observed 2026-09-02: without this rule, every baseline run on a restating blog post still edited the owning page (a second source plus a claims row), so \"no material\" quietly became \"update\"."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 2 / \"No material, before and after\" example vs evals.md S5 baseline",
      "finding": "The same scenario is given two contradictory baseline failure modes: SKILL.md says the baseline edits the OWNING page (adds a corroborating source plus a claims row), evals.md S5 says the baseline writes a NEW thin note. The eval therefore grades against a failure the skill says it did not observe.",
      "quote": "- **Baseline:** writes a thin note anyway."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 input vs evals/files/raw/2026-09-02-pricing-page.md",
      "finding": "The scenario describes three per-MTok prices; the fixture page carries four (Alpha 5 input/output, Beta 5 input/output) plus two cache multipliers. The count the pass criterion is written around does not match the file.",
      "quote": "**Input:** a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S5 input vs evals/files/raw/2026-09-02-blog-restating-caching.md and SKILL.md's example",
      "finding": "S5 says three facts under the same sources; the fixture blog restates two multipliers under a different URL (blog/caching-explained vs the note's /caching), and SKILL.md's own example says two multipliers. Three descriptions of one scenario, two of them wrong about the file.",
      "quote": "**Input:** a blog post restating three facts the wiki already holds with the same sources."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S2 vs evals/files/wiki/notes/local-models.md, SOURCES.md and LOG.md",
      "finding": "S2 stakes the dispute on the existing value coming from the vendor's README, but the note's frontmatter source, the SOURCES row and the LOG line all attribute 744B to the gamma-card — and the note's own prose says README. The fixture contradicts itself and the scenario, so 'a card contradicts a README' is not the situation being graded.",
      "quote": "**Input:** a model card says 753B parameters; the wiki's note says 744B from the vendor's README."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json evals 1–3 (shared mutable fixture)",
      "finding": "All three evals edit the same wiki directory in place with no reset or per-eval copy specified. Run in sequence, eval 3's 'no page changed' criterion is confounded by evals 1 and 2 having already changed pages, and eval 1's index/SOURCES baseline no longer holds. The pass criterion is ungradeable as bundled.",
      "quote": "Edit the wiki in place and list the files you changed."
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expected_output vs SKILL.md steps 2 and 4",
      "finding": "The eval requires the superseded price to be kept, but keeping both values is instructed only for the disputed branch; the update branch says only 'extend that page' and 'date anything that will move'. The eval grades behaviour no step instructs.",
      "quote": "a dated row per changed price, the superseded price kept, the new source with its fetch date in frontmatter"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 pass criterion vs evals/evals.json eval 1 expected_output",
      "finding": "S1 requires the verbatim line and the MEASURED verdict (step 3's whole output) and lint at 0 errors; the runnable eval for the same scenario drops all three. In the only place step 3 could be graded, its criteria are absent.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 pass criterion vs SKILL.md step 7",
      "finding": "S3 grades on a lint severity distinction and a check ('note-only source') that step 7's enumerated lint checks do not contain and that the artefact defines nowhere; there is also no INFO/ERROR level anywhere in SKILL.md. The criterion cannot be evaluated.",
      "quote": "lint reports the note-only source as INFO, not ERROR; claims from it are REPEATED, not MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json eval 1 expected_output vs SKILL.md step 5",
      "finding": "Step 5 requires the neighbour to be given a sentence naming the page back; the eval only asserts a pre-existing link is still there, which any run that edits nothing in the neighbour passes. Step 5 is graded by a check that no failure mode can fail.",
      "quote": "the neighbour still names the owner"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs SKILL.md \"When NOT to use\"",
      "finding": "The description names deep-reading as the sibling for summarising a text; the body's negative-boundary paragraph lists skill-knowledge, unified-memory, doc-claim-reconciliation and kb-curator but silently drops deep-reading, so the boundary asserted to the router is not asserted in the body.",
      "quote": "NOT summarising a text (deep-reading), NOT claims for a skill bundle (skill-knowledge)"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md \"Example\" vs \"In this repo (one instance)\"",
      "finding": "The general Example is written around the repo-specific kb.py query command, which the artefact otherwise confines to the final section. A reader in another project cannot execute the example's decisive step.",
      "quote": "`find \"pricing\"` shows a note that owns model prices"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md \"Method\" vs SKILL.md \"In this repo (one instance)\"",
      "finding": "The eval invokes a --json flag the skill never documents; the skill documents the bare lint and its exit code as the contract. Nothing in the artefact establishes that the machine-readable form exists.",
      "quote": "lint with `python3 knowledge/kb.py lint` (exit 1 on errors) and rebuild with `kb.py build`"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md scenario blocks S3 and S5",
      "finding": "S1, S2 and S4 each state a 'With talent' expectation; S3 and S5 omit it, so for two of six scenarios the with-arm behaviour that the baseline is to be compared against is never written down, and the Method's PASS-vs-'beats baseline' distinction cannot be applied to them.",
      "quote": "- **Baseline:** cites \"a video\" with no raw and grades the on-screen numbers MEASURED.\n- **Result:** pending"
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "Nothing runnable. Only evals.md S3 asserts the raw is saved, and S3 has no entry in evals/evals.json and no fixture; no expected_output in the three runnable evals mentions copying the raw, its provenance, its fetch-dated filename or the content hash. The raws already sit in evals/files/raw/, so a run that copies nothing still passes."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "Partly: evals.json eval 1 (update — owner extended, no new page), eval 2 (disputed — both values kept), eval 3 (no material — no page changed, LOG line). All three by prose expected_output only, expectations empty. Ungraded within the step: the ban on adding a corroborating source, the ban on a claims row for an already-held value, and the exactly-one-bucket requirement — which eval 1's own multi-page fixture cannot satisfy."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "Nothing runnable. evals.md S1 and S3 name the verbatim line and the MEASURED/REPEATED verdict, but the corresponding runnable eval 1 omits both from its expected_output and S3 has no eval at all. DERIVED is graded by no scenario. The fixture notes carry no verdict column to write into."
    },
    {
      "step": 4,
      "checkable": false,
      "graded_by": "Not fully checkable: 'status from the fixed vocabulary' names a vocabulary the artefact never defines (no references/), and the body-section list has no acceptance criterion. Graded partly by evals.json eval 1 ('the new source with its fetch date in frontmatter'); tags, related, status, the four body sections, 'date anything that will move' and 'say what would make it wrong' are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "Nothing effective. evals.md S4 is the only real cascade check and has no runnable eval; evals.json eval 1 asserts only that a pre-existing link 'still names the owner', which passes without any cascade action. Eval 2's target note has related: [], so its disputed fact triggers no cascade check either."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "Partly: evals.json evals 1 and 2 ('a SOURCES row and a LOG line'), eval 3 ('one LOG line saying no material with the source URL'). The index row — the step's first clause — is graded by nothing and is actively contradicted by evals.md S1's 'INDEX unchanged'."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "Nothing. No lint ships with the fixture wiki, so the step cannot be executed against the artefact's own evals; evals.md's Method asserts kb.py lint --json checks every scenario but that tool is neither bundled nor reachable from evals/files/. Only evals.md S1 ('lint reports 0 errors') and S4 ('one-way count ... 0 or explained') mention lint output, and S1's runnable counterpart drops it. The 'rebuild the index' half of the step is described nowhere and graded nowhere."
    }
  ]
}
```