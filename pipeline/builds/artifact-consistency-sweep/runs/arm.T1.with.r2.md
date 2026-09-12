Sweep of `./artifact-A` (the mounted skill has no `references/` in the artefact under review; nothing in the artefact names one, so that is not a defect).

**Plan counts, written before the first verdict:** 7 steps · 5 rules · 9 checks (3 entries in `evals/evals.json` + 6 scenarios in `evals.md`) · 9 description clauses · 12 bundled files + 1 named-but-absent · 7 rationale-bearing claims.
**Examined:** step×rule 35/35 · step×step 8/6 (6 handoffs + the two branch escapes 2→6, 2→7) · step×check 63/63 · description×body 9/9 · file×BOM 13/13 · claim×rationale 7/7. **Total 135 rows examined, 135 owed.**

```json
{
  "findings": [
    {
      "level": "CLASS",
      "where": "evals/evals.json — all three entries",
      "finding": "Every eval declares an empty expectations array, so no step of the skill is graded by any mechanical check at all. The only graders in the artefact are the prose expected_output strings and the evals.md pass criteria, neither of which the harness can evaluate. The whole step×check axis is ungraded by construction.",
      "quote": "\"expectations\": []"
    },
    {
      "level": "CLASS",
      "where": "evals/evals.json files lists (ids 1, 2, 3) vs the bundle",
      "finding": "All three evals declare evals/files/check.py as an input file. No such file exists anywhere in the bundle (evals/files/ contains only raw/ and wiki/). The named grader is absent, which is also why every expectations array can be empty without anything noticing.",
      "quote": "\"evals/files/check.py\""
    },
    {
      "level": "CLASS",
      "where": "evals.md scenarios vs evals/evals.json",
      "finding": "The artefact ships two rival eval documents that disagree on how many scenarios exist: evals.md declares six (S1-S6), evals/evals.json implements three. S3 (URL-less source / raw for a transcript), S4 (cascade under time pressure) and S6 (negative trigger) have no runnable eval and no fixture, so step 1's video/image clause, step 5 in full, and the negative trigger are graded by nothing executable. Nothing in evals.json or SKILL.md points at evals.md.",
      "quote": "### S6 — a claim to bundle into a skill · negative-trigger"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md Rules bullet 5 vs steps 2 and 7 (and 'In this repo')",
      "finding": "A rule forbids what two steps order. The rule says the skill runs no code; step 2 orders querying the wiki's own index, step 7 orders running the deterministic lint, and 'In this repo' spells that out as `python3 knowledge/kb.py lint`. No step can obey the rule as written and still be performed.",
      "quote": "This skill never installs, fetches or runs external code; it is a writing discipline."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 vs steps 6 and 7 (and the rule under step 7)",
      "finding": "The no-material branch says 'stop' before steps 6 and 7, which are written unconditionally. Step 6 orders one row per source in the source log — step 2's stop skips it, and step 2's exemption is only about the page's own source list, leaving SOURCES.md undecided; evals.json id 3 expects a LOG line and nothing else, so the two readings are graded differently. Step 7's 'lint pass in the same commit' is likewise unreachable on this branch.",
      "quote": "**No material means no page is touched**: keep the raw, write one operation-log line with the URL and the reason, and stop."
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 2 vs step 4 vs evals/evals.json id 2",
      "finding": "'disputed' is defined at two scopes and nothing reconciles them. Step 2 marks it at line scope ('where it disagrees'), step 4 makes status a frontmatter field 'from the fixed vocabulary' (page scope), and eval 2 expects it at fact scope ('marked disputed at that fact'). A run cannot tell which one the check will read.",
      "quote": "mark the page `disputed` where it disagrees"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 vs 'In this repo' vs pipeline/contracts/claims.contract.json",
      "finding": "The artefact names its own authority and then contradicts it. Step 3 defines three verdicts (MEASURED, REPEATED, DERIVED) and 'In this repo' cites the claims contract as the source of 'the three verdicts'; that contract's cl.verdict rule is 'every claim verdict is MEASURED or REPEATED', severity error. A DERIVED row would fail the very check cited as its schema.",
      "quote": "and `pipeline/contracts/claims.contract.json` (the claim-row fields and the three verdicts)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 3 vs the Example vs evals.md S1",
      "finding": "MEASURED is defined as requiring a dependent variable, an effect and a sample, then applied to a vendor pricing page, which asserts a price and measures nothing. The Example and S1 both make MEASURED the passing verdict for exactly that input, so the definition and its only two uses disagree.",
      "quote": "**MEASURED** (the source measured it: dependent variable, effect, sample)"
    },
    {
      "level": "CLASS",
      "where": "SKILL.md step 1 and Rules bullet 1 vs evals/evals.json ids 1-3",
      "finding": "Step 1 is graded by a check that passes on the untouched fixture. All three fixtures already ship raw/ files with source and fetched headers, no expected_output mentions the raw layer, a fetch date in a filename, or a content hash, and nothing verifies raw/ was left unedited. A run that skips step 1 entirely passes all three evals.",
      "quote": "the copy goes there with the fetch date in the file name and a content hash in the page's source entry"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expected_output vs SKILL.md step 5",
      "finding": "The only check on the cascade is vacuous: prompt-caching.md already carries related: [\"[[model-prices]]\"] in the untouched fixture, so the clause is true before the run starts. Step 5's actual requirement — the neighbour gains a sentence saying why — is graded by nothing.",
      "quote": "the neighbour still names the owner"
    },
    {
      "level": "INSTANCE",
      "where": "evals/evals.json id 1 expected_output vs SKILL.md steps 2 and 4",
      "finding": "An expectation grades behaviour the body never orders. Keeping a superseded value is defined only in the disputed branch ('keep both values as their own rows'); the update branch says to extend the page and date what moves, and the Example shows only a new dated row. A compliant run may overwrite Beta 5's $3/$15 and fail id 1.",
      "quote": "the superseded price kept"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 6 vs evals.md S1",
      "finding": "Step 6 orders an index row unconditionally for every ingest; S1's pass criterion for the update branch requires the index to be untouched. One of the two must be wrong, and evals.json id 1 ('no new page') silently sides with S1.",
      "quote": "INDEX unchanged, SOURCES +1 row"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 7, heading vs body",
      "finding": "The step's heading orders two actions and its body describes one: the index rebuild appears in the title and in 'In this repo' (kb.py build) but nowhere in the step's instructions, and no expectation mentions it. It also collides with step 6, which writes the index row by hand.",
      "quote": "**Lint, then rebuild the index.** Run the wiki's deterministic lint (schema, dangling links, one-way links, orphans, unlisted pages, stale fetches) and fix what it names before committing."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md step 4",
      "finding": "'The fixed vocabulary' is named but listed nowhere in the artefact. Fixtures use status: verified, step 2 introduces disputed, and no third value is defined; nothing can check a status against a vocabulary the artefact does not contain.",
      "quote": "status from the fixed vocabulary"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md Rules bullet 3",
      "finding": "A rule stated nowhere a step could obey it: no step, no schema field in step 4, no fixture and no expectation ever writes null or 0. The rule cannot be violated or satisfied by anything the procedure produces.",
      "quote": "`null` for not-fetched and not-measured; `0` only for a measured zero."
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md description vs the 'When NOT to use' paragraph",
      "finding": "The description promises a boundary the body does not draw: four of the five sibling exclusions (skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator) are argued in the body; deep-reading appears only in the description and is never distinguished anywhere in the body.",
      "quote": "NOT summarising a text (deep-reading)"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md header vs SKILL.md step 2",
      "finding": "The body cites a baseline result the eval record says was never produced. Step 2's rationale reports what 'every baseline run' did on 2026-09-02, while evals.md dates the suite to the same day, states it has not been run, and marks every scenario's Result as pending.",
      "quote": "**Last eval:** not run — suite authored 2026-09-02"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md Method vs the bundle and evals/evals.json",
      "finding": "The declared observable criterion for every scenario is a repo-local script that is not in the bundle, is absent from evals/files/wiki, and is never invoked by any eval prompt or expectation. As written, no scenario's stated criterion can be executed against the shipped fixture.",
      "quote": "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 7",
      "finding": "S3 grades on a lint severity distinction the artefact never defines, and step 7 says the opposite: it orders fixing everything the lint names, with no INFO tier that may be left standing.",
      "quote": "lint reports the note-only source as INFO, not ERROR"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S3 vs SKILL.md step 4 schema",
      "finding": "S3 requires a source entry that is a `note:` kind with no URL; step 4 lists note as a field alongside 'url or path', which every fixture treats as required (all three notes carry url + fetched and no note field). The two readings of the sources schema are not reconciled and no fixture demonstrates the URL-less form.",
      "quote": "the note's source is a `note:` entry stating that"
    },
    {
      "level": "INSTANCE",
      "where": "evals.md S1 vs evals/evals.json id 1",
      "finding": "The two eval documents grade the same scenario differently: S1 makes the verbatim line and the MEASURED verdict decisive, and the runnable eval drops both, so step 3 — the quote-before-write gate the description leads with — is graded by nothing executable.",
      "quote": "the owning note gains a dated row with the verbatim line and MEASURED"
    },
    {
      "level": "INSTANCE",
      "where": "SKILL.md intro paragraph (claim × rationale)",
      "finding": "The procedure's stated provenance carries no locator: the gist is named with no URL, no fetch date and no quote, and 'what broke here' is evidenced only by step 2's single undated-by-source observation — while the skill's own rule 4 forbids writing an unlooked-up, undated claim about a tool.",
      "quote": "This is Karpathy's LLM Wiki `ingest` operation made procedural, with the parts his gist leaves to the reader filled in from what broke here."
    }
  ],
  "steps": [
    {
      "step": 1,
      "checkable": true,
      "graded_by": "none. No expectation in evals/evals.json names raw/, a fetch date in a filename, or a content hash, and all three fixtures ship raw/ pre-populated, so the check passes untouched. evals.md S3 is the only stated grader and has no runnable eval."
    },
    {
      "step": 2,
      "checkable": true,
      "graded_by": "evals/evals.json id 3 + evals.md S5 (no-material branch); id 1 + S1 (update branch); id 2 + S2 (disputed branch). The 'new' branch is graded by nothing, and the branch's SOURCES-row question is graded inconsistently against step 6."
    },
    {
      "step": 3,
      "checkable": true,
      "graded_by": "none runnable. evals.md S1 ('the verbatim line and MEASURED') and S3 ('REPEATED, not MEASURED') only; no expected_output in evals/evals.json mentions a quote, a locator or a verdict, and DERIVED is graded nowhere at all."
    },
    {
      "step": 4,
      "checkable": true,
      "graded_by": "evals/evals.json id 1, partially ('a dated row per changed price ... the new source with its fetch date in frontmatter'). The status vocabulary, the body sections, and 'say what would make it wrong' are graded by nothing."
    },
    {
      "step": 5,
      "checkable": true,
      "graded_by": "evals/evals.json id 1's 'the neighbour still names the owner' — vacuous, already true in the untouched fixture. evals.md S4 is the only real grader and has no runnable eval. Effectively ungraded."
    },
    {
      "step": 6,
      "checkable": true,
      "graded_by": "evals/evals.json ids 1-2 ('a SOURCES row and a LOG line') and id 3 (one LOG line). The index row it orders is graded by nothing and is contradicted by evals.md S1's 'INDEX unchanged'."
    },
    {
      "step": 7,
      "checkable": false,
      "graded_by": "none. The step ends in 'a verified fact and its lint pass land in the same commit', but the bundle ships no lint, no check.py and no commit stage — the eval prompts only say to edit the wiki in place and list changed files — so neither the lint pass nor the commit is a state anything in the artefact can produce or inspect."
    }
  ]
}
```