# Evals — update-codemaps

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal+clever, observable criteria, baseline-fails on clever ones,
> match talent type, cover a negative trigger).

**Talent:** `update-codemaps` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a model asked
to "document the architecture" with no method) vs WITH its 5-step method (scan → per-domain
codemaps → diff-gate → freshness metadata → diff report). Passes a scenario only if the
with-talent result is materially better and meets the observable criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1/S2 normal (everyday generate + incremental update), S3/S4/S5
      clever (diff-gate, token-budget trap, staleness edge), S6 negative-trigger.
- [x] **Specific to this talent** — every scenario keys on codemap generation mechanics
      (per-domain split, route chains, 30% diff gate, ~1000-token budget, 90-day staleness).
- [x] **Observable pass/fail** — file layout, prompt-before-overwrite, token budget, warning text.
- [x] **Baseline plausibly fails on clever ones** — S3 silent clobber, S4 budget blow-out, S5 no
      staleness signal.
- [x] **Matches talent type** — technique → application/edge scenarios (S4 is a temptation trap).
- [x] **Negative trigger** — S6: context-window-pressure ask belongs to context-budget.

## Scenarios

### S1 — Fresh monorepo, first generation · application
- **Input:** Monorepo with `packages/api` (Express routes → services → repos) and `packages/web`
  (React pages/components), no existing codemaps. "Generate architecture codemaps."
- **Pass criterion (observable):** Produces SEPARATE per-domain files under `docs/CODEMAPS/`
  (architecture / backend / frontend / data / dependencies), backend routes rendered as
  `METHOD /path → Controller → Service → Repo` arrow chains, key files listed as path + line
  count (not full code), and each file carries a `<!-- Generated: … | Files scanned: … -->`
  freshness header.
- **Baseline (without talent):** One monolithic doc (or a prose essay) with pasted code blocks,
  no per-domain split, no arrow-chain route map, no freshness header. FAIL.
- **With talent:** Domain-split, arrow-chain, header-stamped codemaps. PASS.
- **Result:** pass

### S2 — Incremental update, small diff · application
- **Input:** Codemaps already exist. One new route `POST /api/orders` and its service were added
  (~5% of the surface). "Update the codemaps."
- **Pass criterion (observable):** Updates `backend.md` IN PLACE (diff ≤ 30% → no approval
  prompt), refreshes the freshness header's date/file-count, and records the added route in
  `.reports/codemap-diff.txt` under added/modified.
- **Baseline (without talent):** Regenerates every file from scratch (clobbering any hand edits)
  or edits the route silently with no diff report and a stale header. FAIL.
- **With talent:** Targeted in-place update + refreshed header + diff-report entry. PASS.
- **Result:** pass

### S3 — Major refactor trips the diff gate · edge
- **Input:** A refactor renamed/moved ~60% of services and split a package. Existing curated
  codemaps present (with some manual annotations). "Update the codemaps."
- **Pass criterion (observable):** Detects the diff exceeds 30% and REQUESTS user approval /
  shows the diff BEFORE overwriting — does not silently replace the curated docs.
- **Baseline (without talent):** Overwrites everything unconditionally, destroying the prior
  curated content with no diff shown. FAIL.
- **With talent:** Diff computed, >30% → surfaces diff and asks before overwrite. PASS.
- **Result:** pass

### S4 — Token-lean under temptation · trap
- **Input:** `services/billing.ts` is 2,000 lines with 40 exported functions. "Add billing to the
  backend codemap."
- **Pass criterion (observable):** Keeps the entry high-level — primary flow(s), the file as
  path + line count, and only the key entry-point signatures — and stays within the ~1000-token
  per-codemap budget; does NOT inline implementation or exhaustively list all 40 signatures.
- **Baseline (without talent):** Dumps all 40 function signatures or pastes code, blowing the
  token budget and defeating the "token-lean for AI context" purpose. FAIL.
- **With talent:** Structure-only, budgeted, entry-point-focused entry. PASS.
- **Result:** pass

### S5 — Staleness detection · edge
- **Input:** `docs/CODEMAPS/data.md` header shows it was generated 120 days ago; the DB schema
  has since changed. Run an update pass.
- **Pass criterion (observable):** The `.reports/codemap-diff.txt` summary emits a staleness
  warning for `data.md` (not updated in 90+ days) AND flags the schema drift.
- **Baseline (without talent):** No staleness signal; treats the 120-day-old doc as current. FAIL.
- **With talent:** 90-day staleness warning + drift flag in the report. PASS.
- **Result:** pass

### S6 — Context-window pressure ask · negative-trigger
- **Input:** "My Claude Code session gets slow and fills up fast — what's eating my context
  window?"
- **Pass criterion (observable):** Talent does NOT fire — this is live context-window token
  auditing of loaded harness components (context-budget), not codemap generation. Correct move
  is to decline / hand off to context-budget, not to scan source and write `docs/CODEMAPS/`.
- **Baseline (without talent):** May mis-read "context" and start generating codemaps, which
  does nothing for session token pressure. FAIL (over-trigger).
- **With talent:** Recognizes the boundary, declines, points to context-budget. PASS.
- **Result:** pass

## Failure triage (if any scenario failed)
No failures. All six pass with the method applied and the three clever scenarios (S3/S4/S5)
discriminate — their baselines plausibly fail. Negative trigger S6 confirms it does not
over-fire onto context-budget's territory.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
