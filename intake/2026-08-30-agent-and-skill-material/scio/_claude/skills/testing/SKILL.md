---
name: testing
layer: C, E, build-process
phase: build-time
status: written
description: Design and audit tests so they cannot pass for the wrong reason — both for Scio itself and for the apps Scio generates. Use when writing tests, reviewing a suite, deciding whether a green run is evidence, planning what a build gate should check, or whenever someone says "the tests pass". Also use when naming a test, when a regression is found, when a build plan demands one, when a fake, stub, mock or in-memory double stands in for production, when a suite reports skipped tests, when a fixture hand-builds input the real system never produces, when a test asserts that something is absent or never happens, when a rule gains an exemption, when choosing between unit, contract, integration and browser tests, when a test is flaky, when a run exits zero and someone calls that evidence, when a model or an agent reports test counts, when a claim has to be tied to the code it was made about, or when asked about coverage targets, mutation testing, property-based or metamorphic testing, or LLM-as-judge evaluation.
---

# testing

A test that passes tells you one of two things and does not distinguish them — that the code is
right, or that the test cannot tell. This skill exists because **this repository has three
confirmed cases of the second**, all of them green, all of them cited as coverage.

A skill that only said *how to write tests* would have caught none of them. So the four questions
in §3 are the skill, and everything else supports them.

---

## 1 · The three failures this skill is built from

Verified at source in `/home/user/hello-world`, 2026-08-26.

**(a) A double stricter than production.** `FakeScope` in `apps/api/test/build.e2e.spec.ts:105-108`
calls `owns(where.projectId)` on `buildVersion.findFirst`. The real `applyWorkspaceScope`
(`apps/api/src/auth/workspace-scope.ts:62`) returns `args` unchanged for any model outside
`WORKSPACE_SCOPED_MODELS` — six names out of fourteen in `schema.prisma`, and `BuildVersion` is not
one of them. `apps/api/test/workspace-scope.spec.ts:37` asserts production *does not* scope it.
**Two suites assert opposite things about the same mechanism and both pass.** The live
cross-tenant idempotency replay (review finding G-F03) is therefore structurally invisible: 44 e2e
tests cannot fail on it, because the double refuses what production allows.

**(b) A suite whose skips are exactly the path that matters.** `test_interaction_channel.py` has 36
test functions; run here it is **27 passed, 9 skipped**. The nine at `:868`–`:957` are each marked
*"a browser and node with @electric-sql/pglite are both needed here"* — the nine that would drive a
real app are the nine that never run.

**(c) A fixture the real system never produces.** The same file's fixture (`:117-125`) hand-writes
`guest_name: text` and `party_size: integer`. The real producer, `derive.py:259`, gives **every**
create and update `inputs=[Column(name="payload", type=FieldType.json)]`. So the 27 that pass
exercise a shape Layer B cannot emit, and the channel under test never arms on a real build —
measured **0 `interaction` criteria** on the canonical spec, on two independent fixtures.

**And a fourth, in the gate rather than the suite.** `check_tests_present` (`validation.py:132`)
matches `"test" in p.lower() or "spec" in p.lower()`, so `app/latest/page.tsx` satisfies the check
that a package has a test — and there is no test runner in `DEV_DEPENDENCIES` and no `test` script
in `package_json`, so the gate could not have run anything even if it had matched correctly.

**The class.** In all four the assertion, the double or the fixture was *shaped so the real defect
could not reach it* — and each was written by someone careful. `tenant-discipline.spec.ts:15-19`
even **predicts the bug in prose**, then greps for it on the raw client while the live defect is on
the scoped one. A fence that names the failure and misses it in code is worse than no fence, because
it is counted as coverage.

---

## 2 · Source

Scanned **2026-08-26**; read at abstract-to-method level, four fetched in full (✱), none reproduced.

**Adequacy that is measured rather than believed**

| Work | What it shows |
|---|---|
| Inozemtseva & Holmes, *Coverage Is Not Strongly Correlated with Test Suite Effectiveness*, ICSE 2014 ([summary](https://blog.acolyer.org/2014/10/21/coverage-is-not-strongly-correlated-with-test-suite-effectiveness/), [SemanticScholar](https://www.semanticscholar.org/paper/abd840dbcfd986e6de9102ab809c2c46e5ce47aa)) | five Java projects ~100 KLOC each. Once suite **size** is controlled for, coverage–effectiveness correlation is low to moderate; stronger coverage criteria add no insight |
| Papadakis, Shin, Yoo & Bae, *Are Mutation Scores Correlated with Real Fault Detection?*, ICSE 2018 ([ACM](https://dl.acm.org/doi/10.1145/3180155.3180183), [author PDF](https://coinse.github.io/publications/pdfs/Papadakis2018hi.pdf)) | the reported strong correlation is largely a **size confound**; controlled for size it is weak. But top-mutation-score suites still beat random suites of equal size — mutants **guide** improvement even where they do not **predict** |
| ✱ Zhao, Zhou & Cohen, *Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness?* (replicability), [arXiv 2607.22880](https://arxiv.org/html/2607.22880v1), 2026-07-24 | on Defects4J. Coverage vs real-bug detection **r = 0.368–0.485** on bug-free code and **uniformly weak on buggy code** — coverage measured on the buggy version *"is not informative of whether the generated tests detect that bug"*. Mutation vs detection moderate (r = 0.475–0.511). Finds **little evidence** for the size confound, contradicting Papadakis |
| Luo, Hariri, Eloussi & Marinov, *An Empirical Analysis of Flaky Tests*, FSE 2014 ([PDF](https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf)) · *Flaky Tests in JavaScript*, [arXiv 2207.01047](https://arxiv.org/pdf/2207.01047) | root causes: async wait **45%**, concurrency **20%**, order dependency **12%** — but in JS **order dependency is rare**, so the Java distribution does not transfer |
| Hanley & Lippman-Hand 1983; Jovanovic & Levy, *A Look at the Rule of Three*, The American Statistician 1997 ([PDF](http://www.nicksun.fun/assets/misc_papers/Jovanovic_1997_A_look_at_the_rule_of_three_The_American_Statistician.pdf)) | with zero events in *n* trials, **3/n** is the approximate 95% upper bound |
| pytest docs, [skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html) | first-party, and it says the quiet part — skipping lets pytest *"present a summary… while keeping the test suite green"*, and skip detail is **not shown by default** |

**Doubles, contracts and real dependencies — the section this repo needed**

| Work | What it shows |
|---|---|
| Turner-Trauring, *Fast tests for slow services — verified fakes* ([pythonspeed.com](https://pythonspeed.com/articles/verified-fakes/)) | the technique with a name. A fake becomes **verified** only by an additional suite run against **both** the fake and the real implementation |
| *Avoiding Fake Drift in Unit Tests* ([4comprehension.com](https://4comprehension.com/avoiding-fake-drift/)) | drift is the default outcome; one shared contract suite is the fix. If the real implementation changes asserted behaviour, the fake is **forced to catch up** |
| Pact / consumer-driven contract testing; bi-directional CDCT ([Pact 2026 guide](https://qaskills.sh/blog/pact-contract-testing-complete-guide-2026), [BDCT](https://qaskills.sh/blog/bidirectional-contract-testing-pact-2026)) | the industrial form for separately deployed sides. BDCT compares a consumer's used-subset against the provider's OpenAPI **statically** — cheaper, and explicitly **lower fidelity** than replaying against a running provider |
| Testcontainers ([Docker](https://www.docker.com/blog/testcontainers-testing-with-real-dependencies/), [2026 review](https://dzone.com/articles/testcontainers-explained-bringing-real-services-to)) | run the real dependency and the fidelity question disappears. Cost is boot time, a Docker dependency on every runner, and resource pressure |

**Property-based, metamorphic**

- Segura, Fraser, Sánchez & Ruiz-Cortés, *A Survey on Metamorphic Testing*, IEEE TSE 42(9) 805–824,
  2016 ([open PDF](https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf)); Chen et al.,
  *A Review of Challenges and Opportunities*, ACM CSUR 51(1), 2018 ([ACM](https://dl.acm.org/doi/10.1145/3143561)).
  MT attacks the **oracle problem** — instead of asserting one output, assert a relation between the
  outputs of related inputs. Its cost is the relations; identifying them is human work and both
  surveys name it the central open problem. *I could not extract a headline effectiveness number
  from either; do not quote one.*
- *Evaluating Shrinking*, [arXiv 2608.09935](https://arxiv.org/html/2608.09935), 2026 — shrinking is
  what turns a random failure into a debuggable counterexample, and its cost differs materially
  between frameworks. Property-based testing without good shrinking mostly produces noise.

**LLM and agent systems**

| Work | What it shows |
|---|---|
| ✱ Lin et al., *To Run or Not to Run*, ISSTA 2026, [arXiv 2606.26978](https://arxiv.org/html/2606.26978) | **the primary source.** 7,745 public traces + 3,000 controlled repair attempts over 200 SWE-bench instances (100 Lite + 100 Verified), three agents. **81–100% of Fail→Fail cases pass agent-conducted validation but fail the official evaluation** — Claude Code 81.2%, Codex 100%, OpenCode 11.1%. Prohibiting execution cost only **1.25pp** resolve rate (p>0.05) while saving **56–62%** of tokens and **48–54%** wall-clock on Claude Code. **Scope, stated by the authors:** SWE-bench-style repository bug fixing where an official suite exists; may not generalise to tasks needing dynamic analysis |
| Ahmed, Ganhotra, Shinnar & Hirzel, *Investigating Test Overfitting on SWE-bench*, [arXiv 2511.16858](https://arxiv.org/pdf/2511.16858), April 2026 | patches passing the benchmark's tests still fail broader scrutiny. Passing the available tests and being correct are different properties |
| ✱ Norman, Rivera & Hughes, *Reliability without Validity*, [arXiv 2606.19544](https://arxiv.org/pdf/2606.19544), 2026-06-19 | LLM judges show strong **inter-model agreement and self-consistency** while diverging from human judgment. Reproducible ≠ measuring the thing. Consistency is not evidence of validity |
| *Judging the Judges — position bias in LLM-as-a-Judge*, [arXiv 2406.07791](https://arxiv.org/abs/2406.07791) | 15 judges, ~40 generators, 150k+ instances. Position, verbosity and self-preference bias are systematic, not noise |

**Practice, read as files rather than published** — `garrytan/gstack` @ `ad84005` (MIT), its test
suite read on 2026-08-26 and recorded in `docs/mined/PASS2-GSTACK-TESTS.md`. It supplies §3.5 and
§9.5(a), (c) and (d). It reports no outcome measurement of its own: what it offers is a discipline
that caught two of its own false-passing tests, which those tests document.

Added 2026-08-26 from the Layer E triage (`docs/triage/LAYER-E-TRIAGE.md`), same standard —
repositories read as files, no measured outcomes claimed: `claude-task-master`'s
`TestResultValidator` (`docs/mined/PASS2-FOUR-REPOS.md` §1.2) for §9.5(b), and two vocabulary items,
`pass@k` vs `pass^k` (`docs/mined/ECC-SKILLS.md:671`) and naming a generated test after the failure
it prevents (`docs/mined/PASS2-ECC-SKILLS.md:653`).

**Generated applications, and what CI should run**

- [axe-core README](https://github.com/dequelabs/axe-core) — *"on average **57% of WCAG issues**
  automatically"*, claiming **zero false positives**, uncertain cases returned as `incomplete` for
  manual review. The vendor's own figure (§10).
- Next.js runs type checking as the **first step of `next build`**
  ([docs](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript)) — so
  `next build` strictly dominates a bare `tsc --noEmit`, and additionally resolves routes and runs
  `generateStaticParams`.
- Playwright visual comparison — cross-environment flake is **font rendering, anti-aliasing, GPU and
  browser-binary drift**, not the app. Generate baselines in the container CI runs
  ([2026 guide](https://testquality.com/playwright-visual-regression-guide/)); prefer
  `maxDiffPixelRatio` over raising `threshold`, which blunts every comparison.

---

## 3 · The four questions to ask of any test before trusting it, and a fifth for absence tests

Each is a command or a diff, not a judgement. Run all four. A test failing any one is **not
evidence**, whatever colour it is. A test that asserts an **absence** carries an extra obligation,
and it is a permanent one — §3.5.

### Q1 · Can this test fail?
**Check.** Break the thing it claims to check and re-run — negate the asserted value, delete the
line of production code the test names, or run a mutation tool over the covered lines. **The test
must go red.** If it stays green the assertion is vacuous.

**Automatic fails, greppable:** an assertion whose subject is a double's own configured return
value; `expect(x).toBeDefined()` or `assertIsNotNone` as the only assertion; `assert x == x`; a
`try/except` that swallows the failure; a test body with **zero** assertions.

### Q2 · Is the double no stricter and no weaker than production?
**Check.** §4. Both directions. A one-sided contract suite — "the fake allows what production
allows" — is exactly what `FakeScope` would pass.

### Q3 · Did it actually run — and did as much of it run as was planned?
**Check.** Parse the machine-readable report, never the human summary: `pytest --junitxml`,
`vitest --reporter=json`. Three numbers, always: **ran / passed / skipped**. §7.

**And a fourth number: how many units were *planned*.** A zero exit code is not the answer to this
question, and §9.5 is why — a truncated run is indistinguishable from a green one by exit code
alone. A claim that "the tests passed" is three claims, and all three must be checked: the lanes
that were declared ran, the executed-unit count matched the planned count, and no failure line was
printed.

### Q4 · Can the real system produce this input?
**Check.** Name the upstream producer. Run it. Diff its output against the fixture, by *shape*,
not by value. A fixture that no producer can emit tests a system that does not exist.

Scio's producers are named and callable — `derive_architecture(spec)` for `Architecture`,
`build_plan(...)` for `BuildPlan`, the Prisma schema for models — so there is no excuse for a
hand-built `Architecture` in a test of anything downstream of Layer B.


### 3.5 · If it asserts an absence, where is its permanent positive control?

Q1 is a check you run once. For a test that asserts something is **absent** — no secret in the
output, no unfenced prompt, no leaked field, no forbidden call — running it once is not enough,
because the ways an absence test rots are all silent:

- the detector broke;
- the feature it guards was deleted, so there is nothing left to find;
- the fixture never established its precondition, so nothing was ever there to leak.

All three are green. The law, from `gstack test/helpers/secret-sink-harness.ts`
(`docs/mined/PASS2-GSTACK-TESTS.md` §3.1, MIT, read 2026-08-26):

> ***"Positive-control discipline: every test suite using this harness should include one test that
> deliberately leaks a seed and asserts the harness catches it. A harness that silently
> under-reports is worse than no harness."***

**The control is a permanent test in the suite, not a manual check.** Their pairings, each one a
shape worth copying:

| Absence asserted | Its permanent control |
|---|---|
| the harness finds no leak | **six** deliberate leaks — stdout, stderr, file, telemetry, base64, 12-char prefix — each asserted caught |
| no pattern has a catastrophic-backtracking shape | a planted catastrophic pattern **is** flagged by the linter |
| a guard passes on good input | a deliberately broken input **fails** it — *"these prove a BROKEN carve fails"* |
| a component never calls the forbidden API | a second test that it **does** call the permitted one, *"so the negative test cannot pass for the wrong reason"* |
| a secret never reaches a child process | every leak test also asserts **the scrub warning fired** |

The fourth and fifth rows are the sharpest, and both are their own bug reports: a negative test that
passes because all the calls were removed, and a fixture that proved nothing because the runner
never loaded the file it was meant to leak. **They fixed the second by asserting the mechanism ran,
not that the outcome looked right.** That is the general repair.

One more move from the same file, rarer and better: a test that probes whether its fixture could
even create the condition it needs — and **skips rather than asserting a condition it could not
create**. A test that cannot establish its precondition should say so, not pass.

**Exemptions are pinned in both directions.** The same discipline applied to a rule with a carve-out
(`docs/mined/PASS2-GSTACK-TESTS.md` #16): every exemption added to a validation rule needs a test
that the rule **still fires just outside it**. An exemption with only an inside test can widen
silently — and the exemption must be pinned by the evidence that justified it, never by a shape that
happens to match today.

**Where this lands in Scio.** Layer A's gate, the prompt-fencing tests, Layer E's sandbox isolation
and Layer G's tenancy boundary are all absence assertions. `test_the_conversation_is_quoted_rather_than_pasted`
is one today, with no twin. Every eval table in `untrusted-text-boundary` depends on this section
being true.

Cost: one extra test each time, permanently. That is the whole price.

---

## 4 · The double-versus-production rule

> **A double may be neither stricter nor weaker than the thing it doubles, and the only proof is
> one conformance suite run against both.**

This is Scio's E-15, and `test_sandbox_conformance` is proof the repo already knows how — its own
docstring says *"an abstract method whose contract one implementation ignores is worse than no
abstraction."*

**Procedure.**

1. **Name the seam.** The interface, not the class. `SandboxProvider`. `WorkspaceScope`.
2. **Write one suite, parameterised over implementations.** Not two suites that agree by
   coincidence — `build.e2e.spec.ts` and `workspace-scope.spec.ts` are two suites that
   *disagree* by coincidence and both pass.
3. **Every implementation is in the parameter list.** Including ones that raise
   `NotImplementedError`. `AcaSandbox` is absent from the suite written to catch its own defect;
   adding it is one line and the test will fail. **That is the correct outcome** — it converts a
   latent runtime error into a red test.
4. **Assert both directions.** For every input: what must be **allowed** *and* what must be
   **refused**. Then add the strictness assertion explicitly: *for every refusal the double
   makes, production must refuse too.* This single line is what `FakeScope` fails.
5. **When they cannot be made to agree, stop faking.** Two honest exits, no third:
   - **run the real thing** — Testcontainers, pglite, a real browser — and accept the boot cost; or
   - **delete the double** and mark everything behind it `unjudged`.
   Keeping an unverifiable fake is the failure mode, because it certifies rather than checks.
6. **Prefer a check that does not involve the double at all.** The test that would have caught
   G-F03 is not another e2e assertion — it is **schema-derived**: *for every model in
   `schema.prisma`, either it is in `WORKSPACE_SCOPED_MODELS` or it is named in an exemption list
   with a written reason.* No fixture, no double, nothing to shape wrongly. That shape —
   *enumerate the real artifact, assert a property of every element* — is the strongest test in
   this document, and `tenant-discipline.spec.ts`'s `ALLOWED` map already demonstrates it.

**Where separate deployment makes step 2 impossible**, this is consumer-driven contract testing and
already has tools (Pact; bi-directional CDCT against OpenAPI). Adopt the shape, and record that BDCT
trades fidelity for decoupling — a static spec comparison is weaker evidence than a replayed
verification and must be labelled as such.

---

## 5 · The asymmetric rule

Carried from `docs/next/LAYER-E-BUILD.md` §3.1, which is where it was decided.

> **A failing test is evidence. A passing test is `unjudged` until it has been shown capable of
> failing.**

Red is cheap and sound — something is wrong, in the artifact or in the test, and either way it must
be resolved. Green is a claim about the *absence* of a defect, made by an instrument whose
sensitivity nobody measured.

**Promoting green to evidence.** One of these three, recorded, or it stays `unjudged`:

| Route | Evidence | Cost |
|---|---|---|
| **`tdd`** | the test was red before the fix, and the commit shows it | free, if done in that order |
| **`mutant`** | a mutant injected into the code this test covers was killed **by this test** | high — 10–100× a normal run; use incremental mode on changed files |
| **`negative_fixture`** | the suite contains a deliberately-bad sibling input that this same assertion rejects | cheap, and it is what the strictness check in §4.4 is |

**For tests a model wrote — never promote.** In a generated app, a failing test is a `Remainder`
and enters the repair loop; a passing test is `unjudged`, never a gate, never counted in
`checks_passed`. Lin et al. is why: **81–100% of failed cases passed agent-run validation.** State
its scope alongside it every time (§2) — the paper is about repository bug fixing with an official
suite, and Scio's question is dynamic. The ordering transfers; "do not execute" does not.

This costs nothing to be right about: the failures are free signal, and the passes were never
evidence.

---

## 6 · What to test at each level — with the boundary stated

The level is defined by **what is real and what is doubled**, never by the directory the file sits
in. State the boundary in the test plan (§9) or the level is unfalsifiable.

| Level | Real | Doubled | Proves | Cannot prove |
|---|---|---|---|---|
| **Derivation** | the pure function | nothing | the transformation. `applyWorkspaceScope`, `derive.py` | that anyone calls it |
| **Unit at a seam** | the caller | the seam | the caller's logic **given the seam's contract** | the seam's contract — needs the level below |
| **Conformance** | every implementation | nothing | that the implementations agree. **The level Scio is missing** | that the interface is the right one |
| **Integration, real dependency** | DB / filesystem / process | network beyond it | serialization, constraints, scoping, the things fakes get wrong | user-visible behaviour |
| **Browser** | everything | clock, network fixtures | the path a user actually takes | anything, if it is skipped (§1b) |
| **Schema-derived invariant** | the schema / source tree | nothing | a property of **every** element, with no fixture to shape wrongly | behaviour |

**At the browser level, two rules the interaction channel should be built on** — auto-waiting
locators rather than sleeps (a sleep is a guess about someone else's machine; see
`build-loop-stops` on condition-based waiting), and traces retained **on failure** so a failed
browser gate produces evidence rather than a message
(`docs/mined/ECC-SKILLS.md:673`).

**Name a generated test after the failure it prevents, not the function it covers**
(`docs/mined/PASS2-ECC-SKILLS.md:653`). A name that states the failure makes the test traceable
back to the criterion that demanded it, and makes a deleted test visible as a lost guarantee rather
than as one fewer file.

**Do not test:**

- **Framework behaviour** — Next.js routing, Prisma's query builder, React's rendering. That is
  someone else's regression suite.
- **A double's own configuration** — `mock.returns(3); expect(f()).toBe(3)` asserts the mock works.
- **Anything the compiler proves.** Prefer the deterministic gate over the test whenever one exists:
  `next build`, `tsc --noEmit`, `eslint` and `axe` have no oracle problem.
- **Appearance, via a model's opinion.** Use `toHaveScreenshot` against a container-generated
  baseline, or check nothing and say so.
- **Coverage percentage** (§10).

---

## 6a · Two rules for a test the build plan asked for

Added 2026-08-26 from `docs/mined/PASS2-ECC-SKILLS.md:653` (`ai-regression-testing`) and
`docs/mined/PASS2-GSTACK-SKILLS.md` §5.5 (`ship/sections/test-coverage.md`). Both concern tests a
Layer C acceptance criterion *demands*, rather than tests a person chose to write.

### The name is the failure it prevents

> **Name a generated test after the failure it prevents, not the function it covers.**

`test_booking_form` says which code was touched. `test_a_guest_cannot_read_another_guests_booking`
says what is guaranteed — and it survives a refactor that renames the function, moves the file or
splits the component, because the guarantee did not move.

Two consequences that make this more than style:

- **It makes a negative criterion traceable to an artifact.** A *must not* clause and a test named
  after the negation are matched by reading, with no map in between. That is the join
  `.claude/skills/validation-evidence` §3's report is built on.
- **A test nobody can name this way is probably not testing a guarantee.** *"What breaks if I delete
  this?"* has no answer for `test_it_renders`, and that is diagnostic rather than pedantic.

Scio's own suite already does this where it matters — `test_a_dropped_architecture_node_is_caught`,
`test_an_unobservable_criterion_warns_but_never_fails_the_build`,
`test_dependencies_contribute_interfaces_not_implementations`. The rule is to make it the **default
for generated tests**, where nobody is choosing.

### The regression iron rule, and the star level

> **IRON RULE:** when a regression is identified, a regression test is written immediately.
> **Nothing is asked of the user. Nothing is skipped.** When uncertain whether a change is a
> regression, err on the side of writing the test.

The asymmetry is the point: a needless regression test costs one file, a skipped one costs the
regression twice. And it is deliberately *not* a decision — making it declinable makes it a rule
about the days somebody is in a hurry.

Beside it, a quality level a criterion can carry:

| Level | What it covers |
|---|---|
| ★★★ | behaviour, edge cases **and** error paths |
| ★★ | happy path only |
| ★ | smoke test, existence check, trivial assertion — *"it renders"*, *"it doesn't throw"* |

> **A ★ test does not satisfy a contract.** A package whose acceptance criteria are all met by
> existence checks has not met them.

This is §5's asymmetric rule with a coarser dial: ★ sits close to `unjudged` by construction,
because *"it renders"* frequently cannot fail (§3 Q1). The level is a **declaration on the
criterion**, checkable by reading — it is not a measurement, and §11 says so.

The companion matrix names when a unit test is the **wrong** tool: an integration point where
mocking hides the real failure, and *"auth / payment / data-destruction flows — too important to
trust unit tests alone."* Those are §6's boundary rows arrived at from the other direction.

---

## 7 · Skipped tests

**"27 passed, 9 skipped" is never reported as "36 tests pass."** pytest's own documentation states
the purpose plainly — skipping keeps *"the test suite green"* — and skip detail is **not shown by
default**. The reporting default is what makes this failure quiet, so the reporting is what changes.

**Rules.**

1. **Three numbers or none.** `ran / passed / skipped`, from the machine-readable report. A
   summary that states one number is not a result.
2. **Every skip carries a reason, a condition and an owner.** A skip whose condition is *"a browser
   and node with @electric-sql/pglite are both needed here"* is a **statement that the browser path
   is unverified**. That belongs in `unjudged`, next to what it leaves unchecked — not in a
   denominator.
3. **A skip is a capability gap, so name the capability.** Then the fix is procurable: add pglite
   to CI, or delete the nine tests and stop implying they cover something.
4. **An unconditional skip with no owner is a deleted test with extra steps.** Delete it, or fix it.
5. **CI gates on the skip count, not on the pass count.** Fail when skips increase, and fail
   unconditionally when the skip count on a named critical path is non-zero. The critical paths here
   are tenancy, billing and the browser interaction channel.
6. **The same applies to `xfail`, `test.todo`, `it.skip`, `@pytest.mark.skipif`, and to a retry that
   masks a flake.** A test that needed three attempts is `unjudged`, not passed.

---

## 8 · Flakiness, and what B105 actually licenses

`B105` records `design.test.tsx` failing on two consecutive runs with the cause never found.
`docs/next/LAYER-F-DESIGN-WINDOW.md` §1.2 re-ran it: **8 green observations, 0 failures**, and
applied the rule of three to get a **95% upper bound of 3/8 = 37.5%** on the per-run failure rate,
concluding the baseline does not clear B105.

**That reasoning is correct, and it is weaker than it looks in one further way worth stating.** The
rule of three bounds an **independent Bernoulli** failure rate. Flakiness usually is not
independent: async-wait flakes correlate with machine load, order-dependent flakes with run order.
Eight runs in the same order on an idle machine sample **one condition eight times**, not the
condition space once. So 37.5% is the bound *under an assumption the phenomenon tends to violate* —
which strengthens rather than weakens the conclusion: do not treat the baseline as proof.

**Diagnose, do not re-run.** `vitest --repeat` with a **fixed seed** under CI's real concurrency,
recording per-test durations — duration variance is the async-wait signature. Randomise order in a
separate job (12% of flakes in Java, **rare in JavaScript**, so this is the cheap thing to rule
out here, not the likely cause). Vary resources deliberately, since no amount of repeating on an
idle machine finds load-sensitivity. For visual tests, generate the baseline **inside the CI
container** before blaming the app.

**Never fix a flake by retrying it.** Retry converts a signal into silence, and the retried pass is
`unjudged` under §5 regardless.

**Name the property you mean.** `pass@k` — it passed at least once in *k* runs — is the metric a
retry policy quietly optimises, and it is not the one a gate needs. `pass^k` — it passed *every*
one of *k* runs — is. Reporting `pass@k` where the reader assumes `pass^k` is how a flake becomes
a green build (`docs/mined/ECC-SKILLS.md:671`).

---

## 9 · The output contract

A test plan produced by this skill is machine-readable, so a build gate can consume it without
re-deriving anything.

```json
{
  "seams": [
    { "name": "WorkspaceScope",
      "real": "apps/api/src/auth/workspace-scope.ts",
      "doubles": ["apps/api/test/build.e2e.spec.ts::FakeScope"],
      "conformance_suite": null,
      "status": "unverified_double" }
  ],
  "cases": [
    { "id": "...", "level": "derivation|unit|conformance|integration|browser|invariant",
      "seam": "...", "boundary": "what is real, what is doubled",
      "input_provenance": "derived|recorded|hand_built", "producer": "derive.py::derive_architecture",
      "can_fail_evidence": "tdd|mutant|negative_fixture|none", "skip_condition": null }
  ],
  "counts":   { "ran": 27, "passed": 27, "failed": 0, "skipped": 9, "unjudged": 9 },
  "unjudged": [ { "what": "browser interaction path", "why": "9 skips need pglite + a browser" } ]
}
```

**Five rules a gate enforces, all mechanical:**

1. Every entry in `doubles` appears in exactly one `conformance_suite`, or the seam is
   `unverified_double` and **everything behind it is `unjudged`**.
2. `can_fail_evidence: none` → the case counts as `unjudged`, not `passed`.
3. `input_provenance: hand_built` on a case testing anything downstream of a real producer →
   flagged; the plan must name the `producer` and the shape diff.
4. `skipped > 0` → those cases appear in `unjudged`, never in `passed`, and never in a denominator.
5. `checks_passed` never includes an `unjudged` case. This is §5 made arithmetic.
6. `counts` must satisfy §9.5(b) — `ran == passed + failed + skipped`, and a drop against the
   previous run is flagged, not absorbed. A `counts` block that does not add up is rejected before
   any of rules 1–5 are evaluated.

**The human-readable rendering is a table with one row per guarantee**, not a summary line:
*guarantee · test · level · result · the exact command that produces the evidence*
(`docs/mined/ECC-SKILLS.md:669`). The last column is what makes the claim reproducible by someone
who was not there, and it is the column that gets dropped first.

---

## 9.5 · The harness that produces those counts

§9's contract is only as good as the numbers fed into it, and a harness has four ways to report
green while under-reporting. Each is a defect someone found in production and wrote down; each is
cheap to check for.

### (a) Exit 0 is not evidence

From `gstack`, `docs/mined/PASS2-GSTACK-TESTS.md` §2.1 (read 2026-08-26). Their runner ran every
test file in one process; a `setTimeout` armed in an `afterAll` fired mid-way through a *later*
file and killed the suite:

> *"the armed timer fires 500ms later, mid-way through a LATER test file, and kills the entire suite
> with exit code 0 and no summary. The truncated run silently masks every downstream failure
> (**observed: only ~16 of 434 files ran, shell exit 0**)."*

**96% of a suite skipped, green.** Their companion test builds real fixture suites and proves *"the
truncated run is indistinguishable from a green one by exit code alone."*

The fix refuses a zero exit when any of three hold: failure lines were printed; **fewer files ran
than were planned** — *invisible non-execution*; or an unhandled error fired between tests. Which
means **the harness must know how many units it planned to run.** Without a plan count, invisible
non-execution is undetectable, and no amount of parsing the summary recovers it.

Two implementation details with teeth, both of them bugs they hit:

- **stdout and stderr are independent pipes; keep per-origin buffers.** A single shared buffer
  glues fragments into garbled lines, *"a sheared `(fail)` line goes uncounted (defeating the
  exit-0-with-failures backstop) and a sheared summary reads as truncation."*
- **Cancellation must terminate the run, not the current child.** Installing a SIGINT/SIGTERM
  listener suppresses the default terminate-on-signal, so *"the forwarder killed the current child
  and **the parent LIVED ON — the paid worker pool kept launching API-burning shards after
  Ctrl-C**."* A ceiling that only kills the in-flight job is not a ceiling — see `spend-ceilings`.

### (b) Reported counts must be arithmetically coherent

From `claude-task-master`'s `TestResultValidator`, `docs/mined/PASS2-FOUR-REPOS.md` §1.2 — the best
item in that repository. When a *model* reports test results, six arithmetic checks decide whether
the report is internally coherent before anything acts on it. No second model, no reading of code:

| Check | Why it cannot be faked |
|---|---|
| `passed + failed + skipped == total` | a fabricated summary usually gets this wrong |
| a red phase must have `failed >= 1` | tests written first that already pass are not testing the new behaviour |
| a red phase must have `total >= 1` | *"I wrote tests"*, with zero tests |
| a green phase must have `failed == 0` | — |
| a green phase must have `passed >= 1` | zero failures is trivially true of an empty suite |
| `total < previous_total` ⇒ flagged | tests deleted to make the suite pass |

**Four integers make the two cheapest ways to fake a green build — write no tests, delete the
failing ones — detectable without reading a line of code.**

Their own stated limit is the one to correct on the way in: the previous-count field is *optional*,
so the regression check is silent unless a caller threads it through. **A check that is off by
default is off.** Make it required. (This repository has the same shape in a more expensive place:
its two most valuable gates are behind an environment flag.)

### (c) A claim is bound to the bytes it was made about

From `gstack`'s evidence ledger, `docs/mined/PASS2-GSTACK-TESTS.md` §2.2. A recorded run grades
**FRESH / STALE / MISSING**, bound not to a commit but to a fingerprint of the **working tree** —
so evidence recorded on a dirty tree stays FRESH after committing the exact tested content.
Everything else follows from binding to content:

- if the command mutates the tree mid-run, the fingerprint is **omitted** and the record grades
  STALE — *"never certifies unseen content"*;
- gitignored churn does not invalidate; a new untracked source file does;
- the record binds to the **exact command** by hash, so *"I ran the test lane"* cannot silently mean
  something narrower;
- **a recorded failing run is never FRESH**, a fabricated fingerprint degrades to STALE rather than
  crashing, and a malformed max-age is a usage error, *"never a silent fail-open"*;
- **a green lane never masks a red sibling**: every named label must be FRESH, and a label that
  never ran is MISSING;
- **ledger failure never breaks the command it observes.**

The rule this gives Scio, which nothing today provides: *acceptance criteria are written in one
layer and reported met in another, and nothing binds "met" to the bytes it was met against.*
Combined with §9's contract: **inability to prove freshness means re-run, not pass.**

### (d) The harness does not inherit the machine

No `...process.env` spread into a child a harness spawns. Build the child's environment explicitly,
from one module, and let a test assert that every runner uses it. Their comment on why it is one
module: local runs *"silently re-contaminate and nothing fails until a human notices weird results
again, **which took three burned suites last time**"*
(`docs/mined/PASS2-GSTACK-TESTS.md` §2.9).

This repository already does exactly this for the code it *generates* — the sandbox gives generated
code an allow-list rather than `os.environ`, because the child was once started with `**os.environ`
while it held the platform's API key, and a conformance suite proves it for every provider
(`sandbox.py:105`). The rule generalises to every child any harness starts, ours included.

---

## 10 · Tooling — what is worth using, and what is marketing

**Worth using**

| Tool | For | Caveat |
|---|---|---|
| [StrykerJS](https://stryker-mutator.io/docs/stryker-js/incremental/), `--incremental` | the only mechanical answer to Q1 at scale | 10–100× runtime. Incremental on PRs, full on a schedule. Treat the score as **guidance**, never a gate (Papadakis) |
| Playwright + [`@axe-core/playwright`](https://github.com/dequelabs/axe-core) | the deterministic half of accessibility | **57% is Deque's own figure in its own README**, not an independent measurement. Cite it as the vendor's claim, and never say "accessible" on the strength of it |
| [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp) | an agent driving a real browser via accessibility-tree snapshots rather than screenshots | official, Chromium/Firefox/WebKit. It is a driver, not an oracle |
| Testcontainers / pglite | replacing a fake with the real dependency — the direct fix for §1a | boot time, Docker on every runner |
| Pact / bi-directional CDCT | seams across separately deployed sides | BDCT's static comparison is **lower fidelity** than replayed verification; label it |
| `pytest --junitxml`, `vitest --reporter=json` | the only honest source of the three counts | free. Nothing else in §7 works without it |
| [`trunk-io/mcp-server`](https://github.com/trunk-io/mcp-server) | flake detection, root cause, fix suggestion over CI history | vendor product; only as good as the CI history you feed it, and it will not find a flake in a test that is skipped |

**Marketing, or actively harmful here**

- **"AI self-healing selectors."** A selector that repairs itself when the DOM changes is a test
  that **cannot fail** for a whole class of real defect. Directly against Q1. Do not adopt.
- **Coverage-percentage gates.** Inozemtseva & Holmes, plus Zhao et al. 2026 measuring coverage on
  *buggy* code as *"not informative of whether the generated tests detect that bug"* — precisely the
  situation a gate is in. Report coverage as a map of what is untouched, never as a threshold.
- **LLM-as-judge as a gate.** *Reliability without validity* — judges agree with each other and
  diverge from humans, with systematic position, verbosity and self-preference bias. A **signal**,
  never the thing that flips a build green. `critique.py`'s existing rule (*an unreadable verdict is
  a failure, never a pass*) applied to a second untrusted judge.
- **Marketplaces advertising thousands of testing skills.** `SKILLS.md` settles it — volume is not
  the gap, provenance and evals are.

---

## 11 · Limits

- **The two strongest adequacy papers disagree.** Papadakis et al. find the mutation–fault
  correlation is a test-suite-size confound; Zhao et al. (2026) find *little evidence* for that
  confound. Both are Java/Defects4J. **Neither is TypeScript, neither is generated code, neither is
  Scio.** Use them to refuse a coverage gate — which both support — not to set a mutation threshold.
- **axe-core's 57% is the vendor's own claim**, published in its own README with no method attached.
  I found no independent replication. It is quoted here because it is the number the field uses, and
  it is labelled as what it is.
- **Lin et al.'s scope is stated by its authors and matters.** SWE-bench-style repository bug fixing
  where an official suite exists; the paper says its findings may not generalise to tasks needing
  dynamic analysis — which is exactly *did the row reach the database*. The asymmetric rule survives
  the scope restriction because it is conservative in the direction the paper points. A stronger
  claim would not.
- **The 45/20/12 flake distribution is Luo et al., FSE 2014, Java-heavy and pre-2015.** The
  JavaScript study contradicts the order-dependency share directly. Do not quote the Java numbers
  about `apps/app`.
- **The rule of three assumes independent trials.** §8 says why that assumption tends to fail here.
- **§6a is two conventions and one taxonomy, none of them measured.** The naming rule and the
  regression iron rule come from two skill files read once on 2026-08-26
  (`docs/mined/PASS2-ECC-SKILLS.md:653`, `docs/mined/PASS2-GSTACK-SKILLS.md` §5.5). **Nothing shows
  that a suite named after failures catches more of them**; the argument is that the name survives
  refactoring and makes a negative criterion traceable, which is checkable by reading and is a
  weaker claim than efficacy. The ★/★★/★★★ levels are a **declaration**, self-assigned and
  therefore gameable — a ★★★ label on a ★ test is exactly the class of failure §1 is built from, so
  the level narrows a conversation and never substitutes for §3's four questions.
- **Our assumption, not the sources'.** The verified-fakes and contract-testing literature is written
  almost entirely about fakes being **weaker** than production — drift, missing constraints,
  fidelity. **I found no paper measuring the stricter direction**, which is the failure this
  repository actually had. §4's symmetric requirement is therefore *ours*, argued from `FakeScope`
  and `test_sandbox_conformance`'s own docstring, not inherited from a result.
- **§9.5 is four conventions, not four results.** Every one comes from a repository read as files
  on 2026-08-26 and recorded in `docs/mined/`. Each is quotable at a line and each names the
  production failure that motivated it — 16 of 434 files running green, three burned suites, a
  worker pool that survived Ctrl-C — but **none is a measurement that adopting it reduced false
  passes.** The one number in the group, `~16 of 434`, is their incident, not a rate.
- **The arithmetic checks in §9.5(b) detect incoherence, not dishonesty.** A model that reports
  four internally consistent integers passes all six. They raise the cost of fabrication from zero;
  they do not make a reported count evidence. §5 still governs.
- **Nothing was reproduced.** Four sources fetched in full (✱ in §2); the rest read at
  abstract-to-method level. Two ACM DL pages returned 403 and are cited from author or institutional
  copies. The four failures in §1 were verified **statically**, by reading the files named — nothing
  in §1 was executed here.

---

## 12 · Eval

Runnable cases with expected outcomes. **E1–E3 are the three real failures**; each is a case the
skill must *catch*, not merely describe.

### E1 · A double stricter than production
Give the skill `FakeScope` (`build.e2e.spec.ts:105-108`) and `applyWorkspaceScope`
(`workspace-scope.ts:62`). **Expected:** flags the double, names the **direction** (stricter — it
refuses what production allows), states that no e2e assertion behind it can fail on G-F03, and
prescribes §4 — one conformance suite over both, plus the schema-derived invariant that involves no
double at all. **Fails if** it proposes "add another e2e test", or reports the mismatch without
naming the direction.

### E2 · Skips that hide the browser path
Give it `test_interaction_channel.py` — 36 functions, 27 passed, 9 skipped, every skip marked *"a
browser and node with @electric-sql/pglite are both needed here"*. **Expected:** reports **27 ran,
27 passed, 9 skipped**, places the browser interaction path in `unjudged`, and names the missing
capability. **Fails if** the number 36 appears anywhere as a pass count.

### E3 · A fixture the producer never emits
Give it the fixture at `:117-125` (`guest_name: text`, `party_size: integer`) and `derive.py:259`
(every create/update gets `payload: json`). **Expected:** `input_provenance: hand_built`, names
`derive_architecture` as the producer, demands the shape diff, and predicts that the channel arms
on **0** real criteria. **Fails if** the 27 passing tests are accepted as evidence the gate works.

### E4 · A vacuous assertion
A test whose only assertion is on a double's configured return value. **Expected:** Q1 flags it,
`can_fail_evidence: none`, counted `unjudged`. **Fails if** it is counted as passing.

### E5 · A substring standing in for a check
Give it `check_tests_present` (`validation.py:132`). **Expected:** flags the substring, produces a
**concrete false-positive path** — `app/latest/page.tsx` — and adds the second finding that no
runner exists to run a real match. **Fails if** it fixes the pattern without noticing there is
nothing behind it.

### E6 · A green generated suite
A generated app's own tests are green. **Expected:** `unjudged`, never in `checks_passed`, citing
Lin et al. **with its scope**. A failing one is a `Remainder`. **Fails if** green raises
`checks_passed`, or if Lin et al. is quoted without its SWE-bench scope.

### E7 · Eight clean runs on a known flake
B105, eight green observations. **Expected:** refuses to declare it cleared; states 3/8 = 37.5%;
notes the independence assumption; prescribes `--repeat` with a fixed seed under CI concurrency plus
a randomised-order job. **Fails if** it reports the flake as resolved.

### E8 · A request for a coverage gate
Someone asks for an 80% line-coverage gate. **Expected:** refuses it as a gate, cites Inozemtseva &
Holmes and Zhao et al., offers incremental mutation on changed files and a coverage **map** instead.
**Fails if** the gate is set, or if a mutation-score threshold is set in its place.

### E9 · An implementation absent from its own conformance suite
`AcaSandbox` versus `test_sandbox_conformance`'s provider list. **Expected:** add it; state that the
resulting **red test is the correct outcome**; and add the rule that a provider outside the suite is
not a provider. **Fails if** the exclusion is treated as intentional.

---


### E10 · An absence test with no twin
A suite asserts a secret never reaches the logs and nothing in the suite ever puts one there.
**Not evidence.** Expected: a permanent test that seeds a leak and asserts it is caught, in the same
file. §3.5.

### E11 · A negative test that passes because the feature was deleted
Remove the call the negative test forbids, entirely. The negative test still passes; the twin that
asserts the permitted call **must** go red. If nothing goes red, the pair is missing.

### E12 · An exemption added to a rule
A carve-out lands with a test that it applies. Expected: also a test that the rule still fires just
outside the carve-out, pinned to the evidence that justified it — not to a shape.

### E13 · A truncated run reporting green
Build a suite that exits 0 after running a fraction of its files — a delayed `process.exit`, a
killed shard, a runner that stops on an unhandled error. Expected: the gate refuses the zero exit
because the executed-unit count is below the planned count, and names both numbers. A gate that
reads only the exit code, or only the printed summary, fails. §9.5(a).

### E14 · A reported summary that does not add up
Hand the gate a report where `passed + failed + skipped != total`, then one where a red phase has
zero failures, then one where the total dropped since the previous run. Expected: three rejections
and one flag, all arithmetic, no model consulted. Then remove the previous-count input and assert
the regression check still runs — an optional check is an absent check. §9.5(b).

### E15 · Evidence that outlived its subject
Record a passing run, change a source file, re-request the claim. Expected: STALE, not PASS. Then
record on a dirty tree and commit exactly that content: expected FRESH. Then name two lanes and let
one never run: expected MISSING for that lane, and the green sibling does not carry the verdict.
§9.5(c).

### E16 · A child that inherited the machine
Assert every process a harness spawns builds its environment through one explicit constructor. Grep
for a spread of the ambient environment into a child. Any occurrence fails, and the test that
asserts it must itself have a positive control that plants a variable and proves it does not arrive.
§9.5(d) and §3.5.
## 13 · When this skill is the wrong tool

- **Load, soak and concurrency behaviour.** Nothing here measures throughput or races — the repo is
  already explicit that *"everything about concurrency in this document is reasoned from code, not
  measured"*, and a suite does not change that.
- **Security review.** `check_security`, threat modelling and dependency provenance are a separate
  discipline. A green suite is not a security claim.
- **Choosing a test runner for the generated app.** ADR-0011's decision (Layer E §2.4); this skill
  says only what the runner must then report.
- **Deciding whether a feature should exist.** Tests bound risk; they do not set scope.

---

*Scanned and written 2026-08-26; amended the same day from the Layer E triage
(`docs/triage/LAYER-E-TRIAGE.md`) with §9.5, the sharpened Q3, and E13–E16. Four sources fetched in
full; the rest read at abstract-to-method level; none reproduced. Numbers are the authors' own, on
the authors' data. The four failures in §1 were verified statically against the working tree, and
nothing added in the amendment has been measured on Scio.*
