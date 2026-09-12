# Evals — skill-description-optimizer

Functional regression tests. This is a **technique talent**: it takes a skill
`description` that mis-triggers and rewrites it to be trigger-first, concrete,
keyword-rich, and non-overlapping with siblings, verifying against a prompt set.
So each scenario is an *application* case (a broken description to fix) or a
*trap* case (a temptation to do the wrong thing). Pass = applying the talent's
method yields a materially better, criterion-meeting result than a baseline
model without it.

Sibling landscape used (real descriptions in this repo):
- `writing-skills` — create/edit/verify a skill (incl. its body).
- `skill-stocktake` — audit skill quality across many skills.
- `skill-scout` — find/discover/fork an existing skill.
- `prompt-refinement` — sharpen a vague *user request*.
- `wave-reflect` — flags descriptions to `sharpen`; upstream trigger.
- `test-driven-development` / `test-coverage` — used in Scenario A's boundary.

Baseline = a competent model asked to "fix a skill description that
mis-triggers," WITHOUT this talent's method.

---

## Scenario A — False negative: a silent skill (representative)
**Input.** Target `test-coverage` has `description: "Improves testing."` It never
auto-fires. Prompt it should own: *"add tests for the untested error paths in
payment.ts"*.
**Pass criterion.** Rewrite is trigger-first ("Use when…"), contains the concrete
keywords a matching prompt carries (coverage / untested / uncovered branches /
add tests), AND carves the boundary against the adjacent sibling
`test-driven-development` (write-test-first) so "add tests to existing code" wins
`test-coverage` while "TDD this new feature" wins TDD.

- **Baseline.** Likely produces "Use when adding or improving tests." Better than
  "Improves testing," but generic; typically does NOT discover the TDD collision,
  so "add tests" and "write the test first" stay ambiguous between the two.
- **With talent.** Step 1 forces listing adjacent siblings → surfaces TDD. Step 4
  yields e.g. *"Use when existing code has untested paths / low coverage — add
  tests for uncovered branches, error paths, edge cases in code that already
  works; use test-driven-development to write tests before the code exists."*
  Trigger-first, keyword-rich, boundary carved.
- **Verdict: PASS** (moderate margin). The boundary carve is the material win;
  on pure keywording alone the gap over baseline is smaller.

---

## Scenario B — False positive: an over-broad skill steals a sibling's prompts
**Input.** A skill `skill-doctor` with `description: "Use when a skill isn't
working right — fix its triggering, its body, or its overall quality."` Negative
prompt that belongs to `writing-skills`: *"rewrite the procedure steps in my pdf
skill's body."* Also negative for `skill-stocktake`: *"audit all our skills for
quality."*
**Pass criterion.** After rewrite, the body-editing prompt clearly loses to
`writing-skills` and the audit prompt clearly loses to `skill-stocktake`; the
rewrite scopes the skill to description-only triggering.

- **Baseline.** Often keeps the broad "triggering, body, or quality" scope
  because the user only complained about triggering; the two negatives keep
  matching `skill-doctor`. Over-fires exactly as before.
- **With talent.** Rule "change ONLY the description field" + "boundary not sharp
  until the negative loses to its rightful sibling" force narrowing to
  auto-invocation only, with explicit `use writing-skills for the body; use
  skill-stocktake to audit quality` clauses. Both negatives now lose correctly.
- **Verdict: PASS** (clear margin). This is the talent's core competency.

---

## Scenario C — Overlap: two siblings fight for the same prompts (core case)
**Input.** `skill-stocktake`'s description has drifted to *"Use when working with
skill quality — find, audit, or improve skills."* It now collides with
`skill-scout` (discover/fork). Prompt set: positives for stocktake ("audit the
changed skills," "run a full quality stocktake"); negatives owned by scout ("find
a skill that parses PDFs," "is there an existing skill for X I can fork?").
**Pass criterion.** After rewrite, every "find/discover/fork" prompt routes to
`skill-scout`; every "audit/quality" prompt routes to `skill-stocktake`; the word
"find" is removed from stocktake's trigger surface.

- **Baseline.** May sharpen wording but frequently leaves "find" in, or fixes
  stocktake without touching scout's side of the boundary, leaving "find a skill"
  ambiguous.
- **With talent.** Step 2 draws negatives *from the overlapping sibling*; step 5
  re-runs the set against BOTH the rewrite and the unchanged sibling and requires
  each negative to lose to its rightful owner — pinning the boundary from both
  sides. Result strips discovery language and adds `use skill-scout to find or
  fork an existing skill`.
- **Verdict: PASS** (clear margin). The bidirectional prompt-set check is a real
  method advantage baseline lacks.

---

## Scenario D — TRAP: the real problem is the BODY, not the description
**Input.** *"My `pdf` skill auto-fires on the right prompts, but its steps produce
broken output — fix it."* The talent is invoked, but the description is fine.
**Pass criterion (guardrail).** The talent must DECLINE to churn the description
and route to `writing-skills`/`skill-creator` (its explicit "When NOT to use"),
not fabricate a description problem.

- **Baseline.** Prompted to "optimize the description," a baseline model often
  edits the description anyway — motion without effect, leaving the actual body
  bug untouched.
- **With talent.** "When NOT to use: the skill's body/procedure is the problem →
  writing-skills / skill-creator." Correctly no-ops on the description and
  redirects.
- **Verdict: PASS.** Guardrail prevents the wrong action baseline takes.

---

## Scenario E — TRAP: keyword-stuffing to force a fire
**Input.** A skill won't fire on *"containerize the service."* Tempting fix: pad
the description with every deploy/infra keyword. Doing so makes it steal prompts
that belong to sibling infra skills (over-firing).
**Pass criterion.** The rewrite adds a *boundary carve* and the minimal
distinguishing keywords, NOT a keyword dump — and a representative negative
("write a Dockerfile from scratch," owned by a sibling) still loses after the
rewrite.
- **Baseline.** Commonly stuffs keywords ("docker, k8s, compose, deploy, build,
  ship, infra…") to guarantee firing → the target now over-fires on sibling
  prompts. Fixes the false negative by creating false positives.
- **With talent.** Rules "optimize for the boundary, not verbosity — cut words
  that don't change which skill wins" and "a boundary is not sharp until a
  representative negative loses to its rightful sibling" directly forbid this.
  The negative-must-lose check catches the over-fire the stuffed version would
  cause.
- **Verdict: PASS.** Anti-verbosity + negative-loses rule block the failure mode.

---

## Scenario F — Phrasing variants (representative robustness)
**Input.** Target should own a concept expressed many ways: *"tighten this
description," "why won't my skill trigger," "this skill keeps hijacking prompts
meant for another."* A single-example fix might satisfy one phrasing and miss the
others.
**Pass criterion.** The rewrite matches all three positive phrasings (silent
skill, mis-fire, overlap) — the talent's own three documented "when to use"
cases.
- **Baseline.** Tends to optimize against the one example prompt given; a
  differently-phrased positive can still miss.
- **With talent.** Step 2 mandates "phrasing variants" and covers positives +
  negatives + near-misses, so all three intake shapes are exercised before
  finalizing.
- **Verdict: PASS** (moderate margin).

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| A | Silent skill (false negative) | application | PASS (moderate) |
| B | Over-broad steals sibling | application | PASS (clear) |
| C | Two siblings overlap | application | PASS (clear) |
| D | Body problem, not description | trap/guardrail | PASS |
| E | Keyword-stuffing temptation | trap/guardrail | PASS |
| F | Phrasing variants | robustness | PASS (moderate) |

**6 / 6 pass.** The talent clearly beats baseline on the cases that define its
job: the bidirectional prompt-set verification and the "negative must lose to its
rightful sibling" stop-condition produce sharper, non-overlapping boundaries than
a baseline rewrite, and the explicit "when NOT to use" guardrail prevents the
wrong-target churn (D) and keyword-stuffing over-fire (E) that baseline falls
into. On pure false-negative keywording with no sibling collision (A, F) the
margin is smaller but still positive.

### Known limitation (non-blocking)
- **Verification is self-judged.** The method reasons about description matching
  in-model ("reason about matches yourself; no scripts") — it cannot ground-truth
  actual auto-invocation. This is inherent to description optimization (baseline
  can't test it either) and does not stop the talent from beating baseline, but
  the "verified" verdicts are predictions, not measurements.
- **Sibling discovery vs the "no CLI" rule.** Step 1 depends on enumerating
  adjacent siblings, yet the Rules say "no CLI, no scripts." Intent is clearly to
  ban *simulating invocation*, not to ban `ls`/Read for finding sibling skills —
  worth one clarifying clause so the rule doesn't read as forbidding the discovery
  the method requires.

**Verdict: PASSED.**
