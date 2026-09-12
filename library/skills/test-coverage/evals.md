# Evals — test-coverage

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal+clever, observable criteria, baseline-fails on clever ones,
> match scenario type to talent type, cover the negative trigger).

**Talent:** `test-coverage` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a generic
"add tests until coverage hits 80%" instinct) vs WITH its method applied (detect framework →
measure → attack the *right* gaps with *meaningful* tests → re-verify). A scenario passes only
if the with-talent result is materially better and meets the observable criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps — S1/S2 are the everyday job; S3/S4/S5 are traps/edges; S6 negative.
- [x] Specific to this talent — every scenario is about measuring and closing coverage gaps.
- [x] Observable pass/fail criterion on every scenario (no "looks good").
- [x] Clever scenarios (S3–S5) designed so the without-talent baseline plausibly FAILS.
- [x] Technique talent → APPLICATION scenarios, plus one pressure/gaming trap (S3).
- [x] Negative trigger covered (S6 — TDD test-first / eval-suite request).

## Scenarios

### S1 — Detect framework and target the worst file · application (normal)
- **Input:** A Python repo with `pyproject.toml` (pytest configured), `src/validation.py` at
  32% coverage and `src/auth.py` at 45%. "Raise coverage on this module."
- **Pass criterion (observable):** Chooses `pytest --cov=src --cov-report=json` (not a jest/go
  command), lists files **worst-first** (validation.py before auth.py), and names specific
  uncovered functions/branches rather than a vague "add more tests."
- **Baseline (without talent):** Often guesses a generic `pytest` run without `--cov`, or adds
  tests to whichever file it saw first, with no worst-first ordering.
- **With talent:** Step 1 table → pytest command; Step 2 → worst-first list with named gaps.
- **Result:** pass

### S2 — Follow existing project test conventions · application (normal)
- **Input:** A TS service with Vitest, existing tests using `vi.mock()` and `expect().toBe()`,
  files named `*.test.ts` adjacent to source. `src/services/auth.ts` at 45%. "Add tests."
- **Pass criterion (observable):** New test file is `auth.test.ts` **adjacent** to source, uses
  the project's assertion lib and `vi.mock()` mocking style (not a foreign framework), and
  external deps (DB/API) are mocked — no live network/DB call in the generated tests.
- **Baseline (without talent):** May drop tests in a `__tests__/` or `/tests` dir, invent a
  Jest/chai style the repo doesn't use, or call real dependencies.
- **With talent:** "Use existing test patterns… mock external dependencies… place adjacent."
- **Result:** pass

### S3 — Refuse coverage-gaming (assertion-free line-touching) · pressure/trap
- **Input:** "We just need to hit the 80% gate to unblock the release — fastest way." The
  tempting shortcut is to `import` the module and call every function once with no assertions,
  which executes the lines and lifts the percentage.
- **Pass criterion (observable):** Every generated test contains at least one **behavioral
  assertion** on a return value / raised error / side effect. NO test that merely invokes code
  for the sole purpose of touching lines with zero `assert`/`expect`. States that coverage % is
  a proxy, not the goal.
- **Baseline (without talent):** Under the explicit "just hit 80%" pressure, plausibly emits
  smoke-only calls (`func(x)` with no assertion) — coverage rises, defects still slip.
- **With talent:** Step 3 priority is happy/error/edge/branch *behavior*; each test asserts an
  outcome, so a passing test actually pins behavior.
- **Result:** pass

### S4 — Dead code inflating the denominator · trap/edge
- **Input:** `report.py` sits at 60%. The uncovered 40% is an unreachable branch behind a
  constant `if False:` legacy flag and a private helper no caller invokes. "Get it to 80%."
- **Pass criterion (observable):** Flags the dead/unreachable code for **removal** (which raises
  coverage by shrinking the denominator) rather than fabricating contrived tests that reach an
  unreachable branch. Does not add a test that has to monkey-patch `False`→`True` to execute it.
- **Baseline (without talent):** Fixated on the number, writes convoluted tests (or edits the
  flag) to "cover" code that can never run in production.
- **With talent:** Step 2 explicitly says "Dead code that inflates the denominator" is a gap
  category — identified, not tested around.
- **Result:** pass

### S5 — Line-covered but branch-uncovered error path · trap/edge
- **Input:** `parse_amount()` shows **100% line coverage** from one happy-path test, but its
  `if amount < 0: raise ValueError` guard has never been exercised on the true side (the raise
  line is reported covered only because a different test string-formats it). "Coverage looks
  fine — anything missing?"
- **Pass criterion (observable):** Reports that the **negative/error branch is untested despite
  100% line %**, and adds a test asserting `ValueError` is raised for a negative input. Does not
  conclude "100% line = done."
- **Baseline (without talent):** Trusts the line number, declares the function fully covered,
  ships the untested error path.
- **With talent:** Step 3 "Branch coverage — each if/else… error paths" + Focus on error
  handlers distinguishes branch from line.
- **Result:** pass

### S6 — TDD / eval-suite request (should NOT fire) · negative-trigger
- **Input:** "Write the tests first for a parser that doesn't exist yet, then I'll implement it"
  (or: "Build an assertion-based eval suite that gates my prompt changes in CI").
- **Pass criterion (observable):** Declines to apply the coverage-gap method — there is no
  existing code to measure. Redirects: TDD test-first authoring is out of scope; a CI eval gate
  for an LLM app belongs to **llm-eval-harness**; scoring a Claude Code agent's own task
  completion belongs to **eval-harness**.
- **Baseline (without talent):** Might run a coverage tool on a non-existent module (0% / error)
  and flail, or conflate coverage tests with eval suites.
- **With talent:** Description scopes it to "code that exists — not TDD test-first authoring or
  building evals," so it hands off.
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. S3–S5 are the discriminators: each has an observable, outsider-checkable
criterion (presence of a behavioral assertion; dead-code-removal vs contrived test; error-branch
test despite 100% line) on which the generic "hit 80%" baseline plausibly fails while the
skill's method passes.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
