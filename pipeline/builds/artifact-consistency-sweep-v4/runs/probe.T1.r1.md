I examined every file in the bundle and read the SKILL.md, the eval suite and the fixtures against each other. Here is the sweep.

## What I examined

**Bundle (complete — 12 files, nothing else present):**

| File | Read | Used as |
|---|---|---|
| `SKILL.md` (93 lines) | full | frontmatter, 7 numbered steps, Example, 5 Rules, "In this repo" |
| `evals.md` (49 lines) | full | Method, S1–S6, Failure triage |
| `evals/evals.json` (37 lines) | full | 3 runnable evals, `files` BOM, `expectations` |
| `evals/files/wiki/{INDEX,SOURCES,LOG}.md` | full | the register targets of step 6 |
| `evals/files/wiki/notes/{model-prices,prompt-caching,local-models}.md` | full | the page schema of step 4 as actually instantiated |
| `evals/files/raw/2026-09-02-{pricing-page,gamma-model-card,blog-restating-caching}.md` | full | the three eval inputs |

**Pairs checked:** description↔body; each step↔each other step (21 pairs); each step↔each Rule (35 pairs); each step↔Example; each step↔each evals.md scenario (42 pairs); each evals.md scenario↔its evals.json twin; every `files:` entry↔the filesystem; every claim in a step↔the fixture that would have to hold it; every named tool/contract path↔the bundle.

**Searched for and did not find:** any executable grader (`find` for `*.py`, `*.sh` returns nothing but `evals.json` itself).

## Per-step checkability matrix

| # | Step | Ends in something checkable? | Observable | Which check grades it |
|---|---|---|---|---|
| 1 | Keep the raw | **Partly** — "provenance: URL, fetch date, content hash" is observable; "never edited" is not asserted by any artefact state | a file under `raw/` with 3 provenance fields | **Nothing.** Only S3 mentions the raw ("the transcript text is saved as the raw"), and S3 has no eval and no fixture. All 3 runnable evals ship the raw pre-placed, so step 1 is a no-op in every one |
| 2 | Search before writing / triage | **Yes** — which page was touched | the diff: page extended / two rows / untouched | evals 1, 2, 3 (one per branch) — but only for the branch each names; triage=**new** is graded by nothing |
| 3 | Quote + verdict | **Yes in principle** — the row either carries a verbatim line and a verdict or it does not | a 5-field claim row | **Nothing runnable.** `expected_output` in evals 1–3 never mentions a verbatim line or a verdict. Graded only by S1/S2/S3 prose — and S1's grade contradicts step 3's own definition (INSTANCE-1). **DERIVED** is graded by nothing anywhere |
| 4 | Write the page in the schema | **No, for three of its five clauses** | frontmatter fields; four body sections | Frontmatter partly graded by eval 1 ("the new source with its fetch date in frontmatter"). "status from the fixed vocabulary" — vocabulary undefined, ungradeable. "what it means for this project / what is still open" — no criterion, and no fixture note has them. "say what would make it wrong" — graded by nothing |
| 5 | Cascade | **Yes** — the neighbour's file either names back or does not | an inbound sentence per outbound link | **Nothing.** Only S4 grades it; S4 has no eval and no fixture. Eval 1 asserts only "the neighbour **still** names the owner" — a no-change assertion over a fixture where both links already exist, so no run exercises the step |
| 6 | Register | **Yes** for the two logs | rows in SOURCES.md and LOG.md | evals 1, 2 (SOURCES + LOG), eval 3 (LOG). The **index row is graded by nothing and is actively contradicted** by S1 "INDEX unchanged" (INSTANCE-3). The row *shape* is unspecified — the fixture LOG line and the Example's log line use different formats |
| 7 | Lint, then rebuild the index | **Lint: yes. Rebuild: no** — the rebuild is in the title and never in the body | lint exit code; a regenerated index | **Nothing that exists.** `knowledge/kb.py` is not in the bundle and the fixture wiki is not that repo's wiki; `check.py` is listed and absent. The rebuild is described nowhere and graded nowhere |

**Two of seven steps (1, 5) are graded by nothing at all. A third (7) is graded only by tools that do not exist.**

## Findings — CLASS

**CLASS-1 · No check in this artefact can be executed.** `evals/evals.json:11, 22, 33` each list a grader that is not in the bundle:
> `"evals/files/check.py"`

and `evals.json:13, 24, 35` are each:
> `"expectations": []`

while `evals.md:6` names a different, also-absent grader as the criterion for the whole suite:
> "The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note."

`kb.py` is a repo path (`SKILL.md:91`), not a bundled file, and the fixture wiki at `evals/files/wiki/` is a bare markdown directory with no schema tooling — the lint could not run on it even if it were shipped. Every step therefore bottoms out in prose. This is the root of the "graded by nothing" entries in the matrix above.

**CLASS-2 · Triage is declared exhaustive and exclusive, and two of the three bundled sources falsify it.** `SKILL.md:36-40`:
> "Triage into exactly one of: **new** … **update** … **disputed** … **no material** (the source adds no claim, no value and no newer date to any page)."

The triage is decided *per source*, but every outcome it names is *per page and per claim*:
- `raw/2026-09-02-pricing-page.md` is **update** for `model-prices` (Beta 5 moves $3/$15 → $2/$10), **no material** for `model-prices` on Alpha 5 (unchanged at $5/$25), and **no material** for `prompt-caching` (restates 0.1x/1.25x). Three categories, one source.
- `raw/2026-09-02-gamma-model-card.md` is **disputed** for the parameter count (753B vs 744B), **update** for two claims the note lacks ("Active parameters: 40B. Context: 1M tokens"), and **no material** for the 245 GB figure `local-models.md:13` already holds.

Worse, the two branches issue opposite instructions for that one source: `SKILL.md:39` (disputed) requires the source be recorded on the rows it disputes, while `SKILL.md:42-43` forbids it from the source list —
> "A corroborating source is not added to the page's source list - that list says what the page was *derived from*, not what agrees with it"

Nothing says which wins. The step is unexecutable as written on its own fixture.

**CLASS-3 · Half the scenario suite is unrunnable.** `evals.md` declares S1–S6; `evals.json` contains three evals, mapping to S1, S2, S5. **S3 (edge, video transcript), S4 (pressure, cascade) and S6 (negative-trigger) have no eval and no fixture** — no transcript raw, no four-neighbour page, no skill-bundle prompt exists under `evals/files/`. These are precisely the three that carry the only grading for step 1, step 5 and the trigger boundary. The Method's universal claim at `evals.md:6` ("the state of the files … for every scenario") also cannot hold for S6, whose criterion is `evals.md:45`:
> "this talent does not fire; `skill-knowledge` does"

— a routing outcome, in which no file changes at all.

**CLASS-4 · Every scenario has two rival pass criteria that do not agree, with no precedence rule.**

| | `evals.md` requires | `evals.json` requires | Divergence |
|---|---|---|---|
| S1 / eval 1 | "a dated row with the verbatim line and MEASURED; … lint reports 0 errors; INDEX unchanged, SOURCES +1 row" (`evals.md:12`) | "a dated row per changed price, the superseded price kept … a SOURCES row **and a LOG line**; the neighbour still names the owner" (`evals.json:7`) | evals.md demands verbatim+verdict+lint+INDEX and no LOG; evals.json demands LOG and cascade and neither verdict nor lint |
| S2 / eval 2 | "the note marked disputed **at that line**" (`evals.md:19`) | "the note marked disputed **at that fact**" (`evals.json:18`) | line-level vs fact-level, and neither is the page-level `status:` field of `SKILL.md:52` |
| S5 / eval 3 | "an operation-log entry says 'no material' with the URL **and date**" (`evals.md:40`) | "one LOG line saying no material with the source URL" (`evals.json:29`) | the date is required by one and not the other |

**CLASS-5 · Steps mandate fields and vocabularies the artefact never defines and the bundled schema cannot express.** Five occurrences, none checkable:
- `SKILL.md:33-34` requires "a content hash in the page's source entry" — but `SKILL.md:52-53` enumerates the source entry as "(url or path, fetch date, note)" with no hash, and all three fixture notes carry only `url` + `fetched`. **Step 1 and step 4 contradict each other on the same field list.**
- `SKILL.md:48` — "A claim is one row: what it says, source, locator, verbatim line, and a verdict". The bundled page that must hold it, `notes/model-prices.md:13-16`, is a four-column table `model | input | output | as of`: no source, no locator, no verbatim line, no verdict column. The claim-row contract cannot be instantiated in the artefact's own wiki.
- `SKILL.md:53` — "status from the fixed vocabulary". The vocabulary is never enumerated anywhere in the artefact.
- `SKILL.md:39-40` — "mark the page `disputed` where it disagrees" mixes a page-level status with a line-level marker; the marker syntax is undefined, so S2/eval 2 grade a thing the skill never specifies.
- `evals.md:26` — "lint reports the note-only source as INFO, not ERROR". Step 7 gives lint no severity model; `SKILL.md:91` says only "exit 1 on errors".

**CLASS-6 · Rules contradict the steps they govern.** All three of the load-bearing Rules conflict with the body:
- `SKILL.md:83`: "This skill never installs, fetches or runs external code; it is a writing discipline." vs `SKILL.md:61-62`: "**Lint, then rebuild the index.** Run the wiki's deterministic lint" and `SKILL.md:91`: "lint with `python3 knowledge/kb.py lint` … and rebuild with `kb.py build`". Step 7 is the one step that runs external code.
- `SKILL.md:80`: "a rival page is a lint error waiting" vs `SKILL.md:61-62`, which enumerates what lint checks — "schema, dangling links, one-way links, orphans, unlisted pages, stale fetches". Duplicate/rival pages are not on that list. The Rule asserts a check that the step says does not exist.
- `SKILL.md:81`: "`null` for not-fetched and not-measured; `0` only for a measured zero." No step, example, fixture note or eval contains a field that could take either value. The rule is orphaned and graded by nothing.

## Findings — INSTANCE

1. **The Example and S1 grade a price MEASURED; step 3's definition makes that impossible.** `SKILL.md:49`: "**MEASURED** (the source measured it: dependent variable, effect, sample)". A pricing page has no dependent variable, effect or sample — under the skill's own definition a listed price is **REPEATED**. Yet `evals.md:12` requires "the verbatim line and MEASURED" and `SKILL.md:69` says "the note gets a dated row with the verbatim line and MEASURED". The step and its two checks disagree on the correct answer for eval 1.
2. **Step 2 cannot be performed before step 3, but is numbered before it.** `SKILL.md:35` "**Search before writing**" requires deciding whether the source "adds no claim, no value and no newer date" (`:40`) and whether it "contradicts a page" (`:39`) — both of which require the claims already located, which is `SKILL.md:47` step 3. The ordering is circular.
3. **Step 6 mandates an index row; S1 forbids it.** `SKILL.md:59`: "One row in the index (map of contents), one row per source in the source log, one entry in the operation log" — unconditional. `evals.md:12`: "INDEX unchanged". Step 6 has no new-vs-update branch, so on the update path (which `SKILL.md:80` calls the default: "Extending beats creating") step 6 instructs the exact action its own eval fails you for.
4. **Step 6 writes the index by hand; step 7 regenerates it.** `SKILL.md:59` "One row in the index" vs `SKILL.md:61` "Lint, then **rebuild the index**" and `SKILL.md:91` "rebuild with `kb.py build`". Either INDEX.md is generated (making step 6's row pointless or clobbered) or it is hand-maintained (making the rebuild wrong). Nothing resolves it, and no check touches the index at all.
5. **Step 7's title promises an action its body never describes.** `SKILL.md:61-63` — the title is "Lint, then rebuild the index", the body covers only running lint and fixing what it names. The rebuild has no procedure and no check.
6. **Step 5 is unconditional; S4 grades a deferral it does not permit.** `SKILL.md:56-57`: "For every neighbour the page names, make the neighbour name it back". `evals.md:32` passes on either that "**or** the commit message states which neighbours were left one-way and why; lint's one-way count for the new page is 0 **or explained**". The escape hatch exists only in the check. "Or explained" is additionally graded by nothing — no rubric says what counts as an explanation, and lint cannot read one.
7. **The Example inverts step 5's direction.** Step 5 covers outbound links ("every neighbour **the page names**"); `SKILL.md:70` describes the inbound case: "the two notes **that quote the old price** name the pricing note back". Those are different sets, and only the first is what step 5 requires.
8. **Step 4 has no update branch, though update is the stated default path.** `SKILL.md:52-55` is written entirely for a new page (frontmatter block + four body sections). Eval 1 and eval 2 are both updates to existing pages, where most of step 4 is inapplicable and nothing says which clauses still bind.
9. **"No newer date" is undecidable and flips eval 3.** `SKILL.md:40` defines no material as adding "no claim, no value and **no newer date** to any page". The blog raw is `fetched: 2026-09-02`; `notes/prompt-caching.md:6` was fetched `2026-08-20`. Read literally the blog *does* carry a newer date, so it is not "no material" — contradicting `evals.json:29` ("No page changed and no page created"). The intended reading (a newer date *for a dated value*) is never stated.
10. **Step 2's search inputs do not exist in the bundled wiki.** `SKILL.md:35-36`: "Query the wiki's own index for the topic (title, **trigger terms, the source URL**)". `evals/files/wiki/INDEX.md:2-4` carries titles only — no trigger terms, no URLs. The step cannot be run against its own fixture.
11. **The fixture attributes a claim to a source the note does not list.** `notes/local-models.md:13` — "Gamma-7 has 744B total parameters (**README**, 2026-08-25)" — while its frontmatter source (`:4`) is `https://example.test/gamma-card`. `evals.md:18` repeats the README attribution. Step 3's "source, locator" contract is violated by the wiki the artefact ships as correct.
12. **Step 2 says "keep both values as their own rows"; the disputed fixture has no rows.** `SKILL.md:39` vs `notes/local-models.md:13`, which states the parameter count in prose. Converting it to rows is a restructure nothing in step 2 or step 4 describes and no check grades.
13. **The frontmatter names a boundary the body omits.** `SKILL.md:3` lists "NOT summarising a text (deep-reading)"; the body's "When NOT to use" (`SKILL.md:22-26`) names skill-knowledge, unified-memory, doc-claim-reconciliation and kb-curator — deep-reading, the nearest neighbour, is dropped.
14. **The scenario template is inconsistent and the verdict rubric does not cover the suite.** `evals.md:6` mandates "Baseline-vs-with per scenario", but S3, S5 and S6 have no "With talent" line and S6 has no "Baseline" line either. The rubric — "PASS on normal scenarios, 'PASS. Beats baseline.' only where the baseline plausibly fails" — gives no verdict for S5, which is labelled *normal* (`:37`) yet declares a failing baseline (`:41` "writes a thin note anyway").
15. **S1's stated input does not match its fixture.** `evals.md:11`: "a fetched vendor pricing page with **three** per-MTok prices". `raw/2026-09-02-pricing-page.md:5-7` carries four prices and two cache multipliers.
16. **Two sources of truth for the claim contract, with no precedence.** `SKILL.md:48-51` states the row fields and the three verdicts inline; `SKILL.md:88-89` says the schema is "this file plus … `pipeline/contracts/claims.contract.json` (the claim-row fields and the three verdicts)". The contract file is outside the bundle, so the agreement cannot be verified from the artefact. Same pattern at `evals.md:49`, which routes failures to `pipeline/CURATION-LESSONS.md`, also absent.
17. **Two different invocations of the one absent lint.** `evals.md:6` uses `kb.py lint --json`; `SKILL.md:91` uses `kb.py lint` (exit 1 on errors). Neither the tool nor a `--json` contract is in the bundle.
18. **Step 1 calls a derived artefact the raw, against its own rule.** `SKILL.md:29` "Save the **source bytes**" and `SKILL.md:79` "The raw layer is never edited" vs `SKILL.md:31-32` "For a video or image, the **transcript or frame text** is the raw" — a transcription is not the source bytes, and the step gives no provenance for the transcription step itself.

## Summary

Six CLASS defects and eighteen INSTANCE defects. The two that make the rest hard to close: **every named grader is missing from the bundle** (CLASS-1), so no step is checked by anything that runs; and **the triage in step 2, the artefact's central decision, is falsified by two of its own three fixtures** (CLASS-2), which means eval 1 and eval 2 have no single correct answer even by hand. Steps 1 and 5 are graded by nothing at all; step 7 is graded only by tools that do not exist; and steps 3, 4 and 6 each mandate at least one thing no check anywhere in the artefact looks at.