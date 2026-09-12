# Evals — apply-llm-edits

> Baseline-vs-with regression tests for the `apply-llm-edits` talent. Authored to the shape in
> `templates/EVALS.template.md`, applying the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `apply-llm-edits` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a naive
"find the search text and replace it" applier) vs WITH the talent's method applied (read-in-full,
format-parse, exact→whitespace→anchored-fuzzy match ladder, ambiguity stop, re-indent, verify).
A scenario passes only if the with-talent result is materially better and meets the observable
criterion. Technique talent → APPLICATION scenarios.

## Structural pre-check (CURATION-LESSONS directives)
- Frontmatter has `name:` — yes (`apply-llm-edits`).
- Tests live in `evals.md` (not an `evals/` JSON dir) — yes.
- No invented slash-commands / built-ins referenced — confirmed (method-only prose).
- No tool flag/subcommand claims to verify — talent is explicitly "method only, no shell patch
  tools"; nothing to run against a binary.
- Cross-references live, not dead — SKILL.md points to `code-review` and `simplify`; neither is a
  skills-repo sibling, but both resolve to real built-in Claude Code skills present in this
  harness, so the references resolve. Not dead. No fix needed.

## EVOLVING CHECKLIST (satisfied by this suite)
- [x] Blend: S1–S2 normal/representative, S3–S5 clever/adversarial, S6 negative-trigger.
- [x] Specific to this talent (drift, ambiguity, ordering, threshold, marker look-alike).
- [x] Every scenario has an observable pass/fail criterion.
- [x] Clever scenarios designed so the naive baseline plausibly FAILS.
- [x] Technique talent → application scenarios (not pressure).
- [x] Negative-trigger covered (git merge-conflict markers).

## Scenarios

### S1 — indentation drift on an editblock · application (normal)
- **Input:** A SEARCH/REPLACE editblock whose SEARCH body is indented with 4 spaces, but in the
  target file the identical code sits one nesting level deeper (8 spaces). All non-whitespace
  content is byte-identical.
- **Pass criterion (observable):** The replacement lands at the one correct region; the spliced
  lines carry the file's 8-space indentation (re-indented to the target, not the patch's 4);
  SEARCH text gone, REPLACE text present; no other line shifted.
- **Baseline (without talent):** Exact byte-match for the 4-space text fails → either a silent
  no-op (patch "applied" but file unchanged) or a blind paste that injects 4-space-indented lines
  into an 8-space block, producing broken indentation. FAIL.
- **With talent:** Step 4 whitespace-tolerant match (strip leading/trailing, collapse internal)
  finds the region and records its true indent; step 7 re-indents the replacement to 8 spaces;
  step 8 verifies. PASS.
- **Result:** pass

### S2 — unified diff with wrong header line numbers · application (normal)
- **Input:** A `@@ -10,4 +10,4 @@` hunk whose `-`/`+`/context lines are correct, but the matching
  content actually lives at line ~40 in the current file (the file grew above it since the model
  read it).
- **Pass criterion (observable):** Search text is reconstructed from context+`-` lines, located by
  CONTENT at line ~40, and replaced there; lines 10–13 are untouched.
- **Baseline (without talent):** A naive applier trusts the header offsets and edits lines 10–13,
  corrupting unrelated code while the real target is left stale. FAIL.
- **With talent:** Step 2/3 treat header numbers as hints only and match on reconstructed content;
  applies at line ~40. PASS.
- **Result:** pass

### S3 — ambiguous duplicate match · trap (clever)
- **Input:** SEARCH body is a short, common block (e.g. a two-line `logger.debug(...)\n  return`)
  that appears verbatim in TWO functions; the block carries no distinguishing surrounding context.
- **Pass criterion (observable):** The talent does NOT edit the file; it STOPS and reports both
  candidate locations with line numbers, asking for disambiguation.
- **Baseline (without talent):** Replaces the first occurrence (or an arbitrary one), silently
  editing the wrong site roughly half the time. FAIL.
- **With talent:** Step 6 — more than one acceptable location ⇒ STOP and report candidates; the
  rule "Never apply on an ambiguous match" holds. PASS.
- **Result:** pass

### S4 — ordered blocks that could collide on the same match · edge (clever)
- **Input:** Two SEARCH/REPLACE blocks for one file, applied top-to-bottom. The file has two
  near-identical functions `handle_v1` and `handle_v2`, each containing the same interior line.
  Block 1 targets the v1 interior; Block 2's SEARCH text also matches v1's interior (as well as
  its intended v2 site, which appears later).
- **Pass criterion (observable):** Block 1 edits the v1 site; Block 2 edits the v2 site (the
  earliest still-unconsumed match), NOT the already-consumed v1 site. Both functions end correctly
  patched; neither is double-edited.
- **Baseline (without talent):** Both blocks resolve to the first occurrence — v1 gets edited
  twice and v2 is never touched (or Block 2 no-ops). FAIL.
- **With talent:** Step 6 — for ordered blocks prefer the earliest still-unconsumed match so later
  blocks don't collide with earlier ones. PASS.
- **Result:** pass

### S5 — heavily drifted context below threshold · trap (clever)
- **Input:** A SEARCH block whose interior has drifted a lot since the model saw the file (two
  lines removed, one renamed); the best candidate region scores ~0.6 similarity. A superficially
  similar but semantically wrong region also exists.
- **Pass criterion (observable):** The talent does NOT splice into the closest region; it reports
  the block as not-found (below the ~0.85 acceptance threshold) rather than force-applying.
- **Baseline (without talent):** A fuzzy applier with no floor picks the closest-looking region
  and silently corrupts it. FAIL.
- **With talent:** Step 5 accepts only above a high similarity threshold; the rule "Never apply on
  a below-threshold match; report and stop" holds. Reports not-found. PASS.
- **Result:** pass

### S6 — git merge-conflict markers · negative-trigger
- **Input:** A file region containing `<<<<<<< HEAD … ======= … >>>>>>> feature-branch` conflict
  markers, handed over with "apply this." The markers look almost exactly like editblock markers.
- **Pass criterion (observable):** The talent recognizes these are git merge-conflict markers
  (labels are `HEAD` / a branch name, NOT `SEARCH` / `REPLACE`), declines to treat them as a
  SEARCH/REPLACE editblock, and defers to merge-conflict resolution — it does NOT rewrite the file
  as if `<<<<<<<`/`=======`/`>>>>>>>` delimited a search and a replace body.
- **Baseline (without talent):** A marker-pattern matcher keyed on `<<<<<<<`/`=======`/`>>>>>>>`
  mistakes the conflict for an editblock and mangles the file (e.g. drops one side, keeps the
  markers). FAIL / over-trigger.
- **With talent:** "Do NOT use for: git merge-conflict markers"; Format shapes require the literal
  `<<<<<<< SEARCH` / `>>>>>>> REPLACE` labels, which are absent, so the talent declines. PASS
  (correctly does not fire).
- **Result:** pass

## Failure triage
No scenario failed. failure_cause: none.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
- Notes: All three clever scenarios (S3–S5) discriminate — the naive baseline plausibly corrupts
  the file or edits the wrong site, and only the talent's ambiguity-stop / threshold-floor /
  ordered-consumption rules prevent it. The two normal scenarios (S1–S2) also beat baseline
  because whitespace/line-number drift is the everyday reason exact-match patching fails, which is
  exactly the job this talent exists for. The negative-trigger (S6) confirms it won't fire on
  merge-conflict look-alikes.
