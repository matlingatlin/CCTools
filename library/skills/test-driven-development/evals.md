# Evals — test-driven-development

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES: blend normal + clever, observable pass criteria, clever scenarios
> designed so the no-talent baseline plausibly fails, discipline-type → pressure scenarios,
> plus a negative-trigger.

**Talent:** `test-driven-development` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely agent behavior WITHOUT the talent
vs WITH its method applied. TDD is a discipline talent, so most clever scenarios apply
PRESSURE — a plausible excuse to skip the failing-test-first step or to write a dishonest
test. Passes only if the with-talent result is materially better and meets the criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1, S2 normal/representative; S3–S6 clever/pressure; S7 negative-trigger.
- [x] **Specific to this talent** — each scenario turns on red-green-refactor, the iron law, or honest-test rules.
- [x] **Observable pass/fail criterion** — each names a checkable behavior (test written first, code deleted, mirror assertion rejected).
- [x] **Clever ones designed so baseline plausibly FAILS** — S3–S6 tempt the common wrong move.
- [x] **Discipline talent → pressure scenarios** — S3, S4, S6 tempt skipping under a reasonable-sounding excuse.
- [x] **Negative trigger** — S7: a look-alike where forcing full TDD is the wrong call.

## Scenarios

### S1 — New pure function feature · application (normal)
- **Input:** "Add a `slugify(title)` helper that lowercases, trims, and replaces runs of non-alphanumerics with a single hyphen."
- **Pass criterion (observable):** Agent writes a named failing test asserting concrete literal outputs (e.g. `slugify('  Hello, World! ') === 'hello-world'`), RUNS it and confirms it fails, THEN writes minimal implementation, then re-runs to green — in that order.
- **Baseline (without talent):** Writes `slugify` first, then maybe a test that passes on the first run (proving nothing). Order reversed or test-after.
- **With talent:** Red → verify-red → green → verify-green cycle with a hand-derived literal expectation. PASS.
- **Result:** pass

### S2 — Bug reproduction before fix · application (normal)
- **Input:** "Users report `parseAmount('1,000.50')` returns `1` instead of `1000.5`. Fix it."
- **Pass criterion (observable):** Agent first writes a failing test that reproduces the bug (`expect(parseAmount('1,000.50')).toBe(1000.5)`), watches it fail with the reported wrong value, then fixes and re-runs green. The reproducing test is committed as regression protection.
- **Baseline (without talent):** Jumps to editing `parseAmount`, verifies by eyeballing or a one-off manual call; no regression test, or a test written after that passes immediately.
- **With talent:** "Never fix bugs without a test" — failing test proves the fix and prevents regression. PASS.
- **Result:** pass

### S3 — "I already implemented it, just add tests" · pressure (trap)
- **Input:** "I've already written the `RateLimiter` class and it works when I tried it. Can you just add the tests so we're covered?"
- **Pass criterion (observable):** Agent names the specific weakness of tests-after (they pass immediately, are biased by the existing code, prove coverage not correctness) and either drives it via TDD (delete/set aside impl, test-first, reimplement) or explicitly flags that tests-after cannot prove they can catch the bug — rather than silently generating passing tests around the existing class.
- **Baseline (without talent):** Cheerfully writes tests against the existing class; every test passes on first run, giving false confidence. Never surfaces the "passes immediately proves nothing" problem.
- **With talent:** Invokes the "I'll test after" and "Keep as reference" rationalization entries; watched-it-fail requirement is non-negotiable. PASS.
- **Result:** pass

### S4 — "Too simple / TDD will slow us down" · pressure
- **Input:** "This getter is trivial and we're behind schedule — skip the test-first dance and just ship it, be pragmatic."
- **Pass criterion (observable):** Agent rebuts with the concrete cost (simple code still breaks; skipped tests mean debugging in production later; TDD IS the pragmatic path) and does not accept "simple" or "deadline" as a blanket exemption; may note the genuine exceptions (throwaway prototype, generated code, config) only if they actually apply.
- **Baseline (without talent):** Accepts the pragmatism framing, ships untested code.
- **With talent:** "Thinking 'skip TDD just this once'? That's rationalization." Rebuts from the rationalizations table. PASS.
- **Result:** pass

### S5 — Dishonest test slips through · trap (test quality)
- **Input:** "Here's my test for the query builder: `const expected = buildQuery({tag:'x'}); expect(buildQuery({tag:'x'})).toBe(expected);` — good enough?"
- **Pass criterion (observable):** Agent identifies this as a mirror assertion / change detector (both sides computed by the code under test, so it can never fail) and rewrites it with a hand-derived literal (`expect(buildQuery({tag:'x'})).toBe('tag:"x"')`). Also rejects asserting on mock call counts as a substitute for real behavior.
- **Baseline (without talent):** Accepts the test as covering the query builder; the tautology sleeps through every bug.
- **With talent:** `writing-good-tests.md` Principle 1 — derive expectations independently, no change detectors, assert real behavior not mocks. PASS.
- **Result:** pass

### S6 — Test passes on the very first run · edge (pressure)
- **Input:** Agent writes a test for a new validation rule, runs it, and it PASSES immediately before any implementation was added.
- **Pass criterion (observable):** Agent treats the green-on-first-run as a red flag — the behavior already exists or the test doesn't actually exercise the new rule — and fixes the test until it fails for the right reason, instead of moving on satisfied.
- **Baseline (without talent):** Sees green, assumes success, moves on — shipping a test that never verified anything.
- **With talent:** "Test passes? You're testing existing behavior. Fix test." Verify-RED is mandatory. PASS.
- **Result:** pass

### S7 — Throwaway exploratory spike · negative-trigger
- **Input:** "I'm spiking three charting libraries in a scratch file tonight to see which API feels right — nothing here will ship. Walk me through the options."
- **Pass criterion (observable):** Agent does NOT force full red-green-refactor onto disposable exploration; it recognizes the documented exception (throwaway prototypes / "need to explore first") and lets the spike proceed, while noting that the real implementation restarts under TDD and the exploration gets thrown away.
- **Baseline (without talent):** May either ignore testing entirely (fine here) OR — if over-rigid — is irrelevant; this scenario checks the talent does not OVER-fire.
- **With talent:** "Need to explore first? Fine. Throw away exploration, start with TDD." Correctly declines to gate the spike. PASS (does not over-trigger).
- **Result:** pass

## Failure triage (if any scenario failed)
No scenario failed. All six discriminating/normal scenarios show a materially better
with-talent result, and the negative-trigger confirms the talent does not over-fire on
disposable exploration.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
