# Ablation · `testing`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at account level and loads in **both** arms (as do
`session-start-hook` and `synced`). The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

Two questions were run, because the first one did not discriminate. Both are recorded.

---

## Question 1 — the stricter double · **no difference**

### The discriminating rule, and why the obvious answer is wrong

`testing` §4: **a double may be neither stricter nor weaker than the thing it doubles.** The
repository's own instance is `FakeScope` (`build.e2e.spec.ts:105-108`) applying tenant scoping to a
model that production leaves unscoped, so 44 e2e tests cannot fail on a live cross-tenant defect.

The obvious answer is that a stricter fake is a conservative fake — over-constrained at worst,
certainly not dangerous. That is the intuition the question was built to bait.

### The question

> Someone on the team wants our database test fake to be stricter than the real client — it would
> apply the tenant filter to every table, so tests can't accidentally depend on unscoped reads.
> That sounds safer to me. Any reason not to? Four bullets maximum.

### Control answer

Verbatim.

> - **Masks a real bug class**: if production code has a path that reads without setting tenant context (a missing middleware, a raw query, an admin/cross-tenant job), a fake that filters everything will silently return correct-looking scoped results in tests instead of exposing the leak — the exact bug you'd want caught.
> - **Diverges from the real client's semantics**: if the actual DB/ORM client doesn't enforce tenant scoping itself (app code is responsible for adding the filter), the fake now behaves differently from production, so tests can pass against the fake while the real client would return unscoped data.
> - **Hides missing-filter bugs in the code under test** rather than catching them: the code under test is supposed to apply the filter; if the fake applies it too, a test can't tell "app forgot the filter" from "app applied it" — both look identical.
> - **Fine if reframed as a second, opt-in fake** (e.g. `StrictTenantFake`) used deliberately for tests about the scoping layer itself, rather than replacing the default fake everywhere — that way you still have a fake that faithfully mirrors production for testing everything else.

### Treatment answer

Verbatim.

> §6.2 covers this exact case — it's already a documented failure in this repo (`FakeScope` vs `applyWorkspaceScope`).
>
> - **A fake stricter than production is not "safer," it's a different mechanism under test.** If the fake enforces tenant filtering on every table but `applyWorkspaceScope` only scopes six of fourteen models, tests pass against a system that doesn't exist — `FakeScope`/`workspace-scope.spec.ts` is the exact case where "both suites pass" and prove nothing about production.
> - **It hides the real gap instead of surfacing it.** The point of a test is to catch unscoped reads against the *actual* scoping logic; a fake that filters everything can never reproduce the live defect (`build.service.ts:517-525`) it was meant to guard against.
> - **It can only certify, never fail.** A double stricter than reality has no failure mode that maps to a real regression — see E4 in the tenant-isolation skill: diff every method the fake implements against the production function; any operation the fake refuses and production allows is a bug in the fake, not a safety net.
> - **Fix belongs upstream, not in the fake.** If you want tests to catch unscoped reads, add the missing models to `WORKSPACE_SCOPED_MODELS` (or fix `applyWorkspaceScope`) and assert against the *real* client — don't diverge the fake from what it's supposed to stand in for.

### Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| A stricter double masks the defect it was meant to catch | yes | yes |
| Test cannot distinguish "app applied the filter" from "app forgot it" | yes | yes ("can only certify, never fail") |
| The divergence is fake-versus-production semantics, not strictness per se | yes | yes |
| Repair | keep a faithful default fake; make the strict one opt-in for scoping tests | fix production's scoped-model list and assert against the real client |
| Named at `file:line` in our own code | no — reasoned generically | yes — `FakeScope`, `applyWorkspaceScope`, `WORKSPACE_SCOPED_MODELS`, `build.service.ts:517-525` |
| The conformance procedure (diff every doubled method both directions) | implied | stated as an executable check |

### Verdict — question 1

**No difference.** Same conclusion by the same reasoning. The treatment localises it to our code and
supplies a procedure, which is worth something operationally, but nothing in the *mechanism* is
supplied by the skill. The bait failed: the model does not believe a stricter fake is safer.

This is a result about the **question**, not about §4. It repeats ablation 02's lesson — the
"stricter double" framing is close enough to "the fake doesn't match production" that the model
answers it from instinct.

---

## Question 2 — the done-bar · **changed the outcome**

### The discriminating rule, and why the obvious answer is wrong

`testing` §3 Q1 and §5: **a green run is `unjudged` until the test has been shown capable of
failing** — by TDD ordering, a killed mutant, or a negative fixture. §3 Q3 and §7: *"the tests
passed"* is three claims, and a zero exit code answers none of them; the machine-readable report
gives **ran / passed / skipped** against a **planned** count, and *"27 passed, 9 skipped"* is never
*"36 tests pass."*

The obvious answer is to argue about the coverage number.

### The question

> We want a done-bar for each generated package's tests: coverage over 80% and no failures. Is that
> a good bar, and what would you change? Four bullets maximum.

### Control answer

Verbatim.

> - **Coverage is the wrong lever**: 80% line coverage rewards trivial tests (getters, happy-path only) and says nothing about whether the *generated app's actual behavior* is correct — for an AI app builder, a broken feature with high coverage is worse than low coverage that's honest about gaps. Weight the bar toward "critical paths tested" over a blanket percentage.
> - **No-failures is necessary but not sufficient**: add a floor on test *count* or assertion density per generated unit — a package can hit 0 failures with 1 vacuous test per file.
> - **Missing: build/type-check must pass first** — coverage and pass-rate on code that doesn't compile is a meaningless bar; gate on that before either metric.
> - **Missing: flakiness signal** — since these are AI-generated packages run once and shipped to non-technical owners, a single green run isn't trustworthy; consider requiring 2-3 consecutive clean runs (or documenting that you're accepting single-run risk) before calling it "done."

### Treatment answer

Verbatim.

> No — both loaded skills refute exactly this bar (`testing` §10/§6/E8: coverage-percentage gates are marketing, not adequacy; `gate-verdicts` D2: a boolean pass/fail can't say "nobody looked"). Four changes:
>
> - **Drop coverage-% as a gate entirely.** Inozemtseva & Holmes (ICSE'14) and Zhao et al. (2026) both show coverage is weak-to-uninformative about real fault detection, and worse, uninformative specifically on *buggy* code — the exact state a gate faces. Report coverage as a map of what's untouched, never as an 80% threshold to clear.
> - **Replace it with incremental mutation on changed files as guidance, not a gate** (Stryker `--incremental`), plus the schema-derived invariant style where possible (enumerate the real artifact, assert a property of every element — no fixture to shape wrong).
> - **"No failures" needs a truncation check, not just exit code 0.** A killed shard or early `process.exit` reports 0 with a fraction of files run (`testing` §9.5a — the gstack case ran 16/434 files and exited clean). Require `ran == passed + failed + skipped` against a *planned* count, and treat skips as `unjudged`, never as passing — "27 passed, 9 skipped" is not "36 pass."
> - **A green suite in a generated package is `unjudged`, not `passed`, until it's shown capable of failing** (`testing` §5, Lin et al. ISSTA'26: 81–100% of Fail→Fail cases pass agent-run validation). Promote to evidence only via TDD-order, a killed mutant, or a negative-fixture sibling — otherwise the done-bar is measuring "a model wrote a suite that runs," not "the package works."

### Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Coverage % is a weak bar | **yes** — "rewards trivial tests" | yes, with two citations, and *drop it as a gate entirely* |
| What replaces it | "critical paths tested"; a floor on test count or assertion density | mutation on changed files as guidance; schema-derived invariants |
| A test must be **shown capable of failing** before green counts | absent | **the whole of bullet 4** — `unjudged` until a mutant is killed, TDD order, or a negative-fixture sibling |
| Exit code 0 is not proof the suite ran | absent | truncation check: `ran == passed + failed + skipped` against a **planned** count |
| Skips must not enter the denominator | absent | *"27 passed, 9 skipped" is not "36 pass"* |
| Type-check / build must pass first | **yes, and only the control** | absent |
| Repeat runs as a flakiness signal | **yes, and only the control** | absent (the skill treats a retry-masked flake as `unjudged`, not addressed here) |
| Vacuous tests | named as a risk ("1 vacuous test per file"), answered with a **count** floor | answered with a **capability-to-fail** check |

The two arms agree that coverage is weak and that vacuous tests are the danger. They then propose
**opposite kinds of remedy**: the control adds another number (test count, assertion density,
consecutive clean runs); the treatment removes the number and replaces it with a demonstration that
the test can go red. That is the discriminating difference, and it is precisely §5's rule.

### Verdict — question 2

**Changed the outcome.** Two mechanisms appear only with the skill — *green is `unjudged` until the
test is shown capable of failing*, and *a zero exit code does not establish that the planned units
ran*, with skips excluded from the denominator. Neither is in the control at any strength.

The control was better on two points the treatment dropped: gating the type-check first, and
treating a single green run as a flakiness risk. A skill that displaces a correct instinct is a cost
worth recording.

## Verdict — overall

**Changed the outcome**, on the second question. The first question found **no difference** and is
reported at equal length, because it is the more transferable finding: §4's stricter-double rule,
which the skill presents as its sharpest, is one this model already holds.

## Limits of this measurement

n=1 per arm on each question, two questions, unblinded throughout — I wrote both questions knowing
the rules, ran both arms once, and graded them myself. Question 2 was chosen *after* question 1
failed, which is one step away from fishing; it is recorded here with its predecessor precisely so
the selection is visible. Nothing here shows that a package gated the treatment's way contains fewer
defects. `graphify` loads in both arms and is not controlled for.
