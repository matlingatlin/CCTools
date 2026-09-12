# Eval: prompt-refinement

Functional regression test for the `prompt-refinement` talent. This is a *technique*
talent: given a vague/underspecified request, it should rewrite it into a precise,
testable instruction (Objective · Acceptance criteria · Constraints · Output format),
convert subjective criteria into measurable ones, ask only the minimum blocking
questions, and explicitly NOT interrogate a request that is already precise.

Method: for each scenario, reason through the likely output WITHOUT the talent
(baseline Claude) vs WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result. Adversarial, not a rubber stamp.

Date: 2026-08-27 · Talent version: SKILL.md as of this commit.

---

## Scenario 1 — Vague cleanup request (application)
**Input:** "Clean up `src/payments/charge.js`." No other detail.
**Pass criterion:** Output is a 4-part refined instruction with at least one *objectively
testable* acceptance criterion (e.g. "no behavior change: existing tests still pass"),
names a scope boundary (this file only), and asks ≤2 blocking questions OR states
vetoing assumptions. Does not silently start editing.

- **Baseline:** Likely opens the file and starts making judgment-call edits (rename vars,
  reformat, extract helpers) with an implicit, unstated definition of "clean". Risk of
  behavior changes, scope creep into other files, and an unverifiable "done".
- **With talent:** Detects gaps in goal ("clean" = readability? dead-code removal?
  perf?), scope (this file vs module), success metric (behavior preserved?). Produces:
  *Objective* — improve readability of `charge.js` with no behavior change; *AC* — (1)
  `npm test` still green, (2) no exported signature changes, (3) no new deps, (4) cyclomatic
  complexity of touched fns not increased; *Constraints* — single file, no API changes;
  *Output* — one focused diff + unchanged test suite. Asks only "readability, dead-code, or
  perf?" if it matters.
- **Verdict:** PASS. Talent converts an unbounded, unverifiable task into a bounded one
  with a pass/fail gate. Clear win over baseline's guess-and-edit.

---

## Scenario 2 — Underspecified feature on a repo that forbids inventing (application + context trap)
**Input:** "Add auth to the app." (Repo CLAUDE.md: tech stack is explicitly UNDECIDED;
"do not invent" the stack.)
**Pass criterion:** Refined instruction surfaces the missing decisions (auth model, stack)
as blocking rather than picking them; acceptance criteria are testable; it does NOT
hard-code a framework/library choice.
- **Baseline:** High risk of jumping to a concrete implementation ("I'll add JWT +
  bcrypt + an Express middleware…"), inventing a stack the project has deliberately left
  open — directly violating the repo's do-not-invent rule.
- **With talent:** Step 1 flags unresolved *constraints* (no stack chosen) and *scope*
  (which surfaces need auth? session vs token? which users?). Step 2 asks the minimum
  blocking questions or records explicit, vetoable assumptions instead of coding. Produces
  *Objective/AC/Constraints/Output* where Constraints reads "stack undecided — must not
  pick one here" and AC are behavioral (e.g. "unauthenticated request to protected route
  returns 401"). Refines the request only; does not start work.
- **Verdict:** PASS. The talent's "ask/assume, don't guess" discipline structurally
  prevents the exact failure the repo warns about. Strong win.

---

## Scenario 3 — Subjective performance criterion (testability trap)
**Input:** "Make the search endpoint fast."
**Pass criterion:** The word "fast" must be replaced by a *measurable* target (a latency
number/percentile or a benchmark), per Step 4. If the output still contains "fast" as the
success condition, it fails.
- **Baseline:** Often accepts "fast" at face value, starts optimizing (add an index, cache)
  and later declares success subjectively, with no agreed threshold — the classic
  unverifiable-done failure.
- **With talent:** Step 4 explicitly forbids subjective adjectives and forces a measurable
  criterion, e.g. "p95 latency < 200ms at 100 rps on the seed dataset" plus a baseline
  measurement first. Constraints capture what may/may not change (no schema migration?).
- **Verdict:** PASS. This is the talent's sharpest, most differentiated behavior — the
  testability pass is something baseline routinely skips. Clear win.

---

## Scenario 4 — Already-precise request (discipline trap: do NOT interrogate)
**Input:** "In `src/utils/date.ts`, change `formatDate` to return ISO 8601 (YYYY-MM-DD)
instead of MM/DD/YYYY, and update the existing unit test to match."
**Pass criterion:** The talent recognizes the request is already precise (clear objective,
testable outcome, known scope/format) and does NOT generate clarifying questions or a
ceremony 4-part rewrite — it proceeds (or hands off to do the work). Adding interrogation
here = fail.
- **Baseline:** Proceeds to make the change. Fine.
- **With talent:** SKILL "When NOT to use" + Rule "Don't interrogate a clear request"
  explicitly gates this out; the talent should stand down and let the work happen.
- **Verdict:** PASS (no-harm). Talent matches baseline and, importantly, its explicit
  stand-down guard prevents the over-application failure mode (turning a crisp one-liner
  into a questionnaire). It neither helps nor hurts vs baseline here, which is the correct
  outcome for a trap designed to catch over-triggering.

---

## Scenario 5 — Low-stakes, reversible task (over-interrogation trap)
**Input:** "Add a .gitignore for this Node project."
**Pass criterion:** Minimal-to-zero blocking questions; the talent states a reasonable
assumption (standard Node ignores) and proceeds rather than interrogating over trivia.
Asking a batch of questions here = fail (violates "ask the fewest questions" / "when asking
isn't worthwhile, state assumptions").
- **Baseline:** Just writes a standard Node `.gitignore`. Fine.
- **With talent:** Step 2's "when asking isn't possible or worthwhile — state explicit
  assumptions" plus the "fewest questions" rule should make it assume the standard set
  (node_modules, dist, .env, logs) and proceed, noting the assumption as vetoable.
- **Verdict:** PASS (no-harm). Talent's minimal-questions rule keeps it from adding
  friction. Neutral-to-slightly-better (the explicit vetoable assumption is a small plus).

---

## Scenario 6 — Open-ended / creative request (scope-boundary trap)
**Input:** "Give me some ideas for the landing-page hero section."
**Pass criterion:** The right behavior is to produce ideas (optionally after one light
framing question), NOT to demand testable acceptance criteria or block on a formal
Objective/AC/Constraints/Format rewrite. Forcing "hero converts at X%" style testability
onto a brainstorm = fail (premature precision on an exploratory task).
- **Baseline:** Generates several hero concepts, maybe asks about product/tone. Appropriate
  for a creative ask.
- **With talent:** The description triggers on "underspecified", and a brainstorm IS
  underspecified, so the talent may pull the request toward the 4-part rewrite and the
  Step-4 testability gate — which fits engineering tasks but is awkward for ideation
  ("make 'good hero' testable"). A careful reader falls back to Step 2's "state assumptions
  and proceed," so it usually still delivers ideas, but the talent does not *clearly beat*
  baseline here and carries a real risk of over-processing an exploratory request.
- **Verdict:** WEAK / does-not-beat-baseline. Identified GAP: "When NOT to use" only
  excludes already-precise prompts, not open-ended/creative/exploratory ones where forcing
  testable acceptance criteria is counterproductive.

---

## Summary
| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | Vague cleanup | application | PASS |
| 2 | Add auth (do-not-invent) | application | PASS |
| 3 | "Make it fast" | testability trap | PASS |
| 4 | Already-precise request | over-trigger trap | PASS (no-harm) |
| 5 | Low-stakes .gitignore | over-interrogation trap | PASS (no-harm) |
| 6 | Creative brainstorm | scope-boundary trap | WEAK (gap) |

**Passed: 5 / 6.**

**Overall:** The talent clearly and materially beats baseline on its core target class —
vague, actionable engineering requests — where its structured 4-part rewrite and mandatory
testability pass turn unverifiable "done" into pass/fail gates that baseline routinely
skips. It is safe on the over-trigger/over-interrogation traps (Scenarios 4-5): its explicit
"don't interrogate a clear request" and "fewest questions" guards prevent harm.

**Gap (Scenario 6):** The "When NOT to use" section guards only against *already-precise*
prompts, not against *open-ended/creative/exploratory* requests where premature testability
is the wrong move. Recommended enhancement: add a "When NOT to use" clause — "the task is
exploratory or creative (brainstorming, ideation, options-generation) where a testable
acceptance criterion is premature; give options, don't lock a spec." This is a scope-boundary
refinement, not a defect in the talent's core claim.

**Verdict: PASSED** — decisive win on its target domain, no harm on traps, one non-blocking
scope-boundary gap noted for a future edit.
