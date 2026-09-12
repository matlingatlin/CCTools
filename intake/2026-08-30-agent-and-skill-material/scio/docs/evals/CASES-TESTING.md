# Eval cases executed · `testing`

**Date:** 2026-08-26. First execution of this skill's cases.

Sixteen named cases, `.claude/skills/testing/SKILL.md` §12. None had ever been run. Everything
below was executed against `/home/user/hello-world` (read-only) or against a copy of it under the
scratchpad. Every command and every number is real; nothing here is described rather than run.

*(The container clock reads 2026-08-27 — pytest's own JUnit stamp says
`timestamp="2026-08-27T09:07:41"`. The date above is the one the eval is filed under.)*

**What PASS means here.** A case PASSes when it was executed and its stated expected outcome was
observed. For the cases that check the repository (E9–E12, E16) a passing case means **the
repository failed the check** — the case did its job. Both are reported.

---

## Summary

| | Cases | |
|---|---|---|
| **RUNNABLE** | **9** | E1, E2, E3, E5, E9, E10, E11, E12, E16 |
| **BLOCKED** | **3** | E13, E14, E15 — all three need a gate that does not exist |
| **NOT A TEST** | **4** | E4, E6, E7, E8 |

**Among the 9 runnable: 9 PASS, 0 FAIL, 0 INCONCLUSIVE.**

That is a suspiciously clean sheet, and the reason is worth stating up front rather than buried:
**E1, E2, E3 and E5 are not predictions, they are records.** They were written *after* someone read
the files, and their "expected outcome" is the thing that was already seen there. Running them
confirms the skill's §1 is accurate — which it is, to the line, with one correction below — but a
case cannot be wrong about a fact its author copied down. The four cases that carry real risk are
E9, E10, E12 and E16, because each names a check whose result nobody had yet computed. **All four
found a live defect.** That is the result.

### What the runnable cases found in `hello-world`

| Case | Finding | Evidence |
|---|---|---|
| E9 | `AcaSandbox.start()` does not accept `env` at all — an interface violation, not a stub | 9 passed → **2 failed, 10 passed** |
| E10 | `test_no_provider_leaks_the_platforms_secrets` passes with the child process **entirely removed** | green under a mutation that deletes the mechanism |
| E12 | A four-line entry in `tenant-discipline.spec.ts`'s `ALLOWED` turns a real cross-tenant read green | **2 passed (2)** with the leak in place |
| E16 | One `**os.environ` spread into a child, plus **9** `subprocess` spawns with no `env=` at all | AST scan, both assertions red |
| E1 | The idempotency replay reads `BuildVersion` with **no tenant check at either entry point** | `build.service.ts:202` and `:518` |

---

## E1 · A double stricter than production

> Give the skill `FakeScope` (`build.e2e.spec.ts:105-108`) and `applyWorkspaceScope`
> (`workspace-scope.ts:62`). **Expected:** flags the double, names the **direction** (stricter — it
> refuses what production allows), states that no e2e assertion behind it can fail on G-F03, and
> prescribes §4 — one conformance suite over both, plus the schema-derived invariant that involves
> no double at all. **Fails if** it proposes "add another e2e test", or reports the mismatch without
> naming the direction.

**Classification: RUNNABLE.** The graded output is a model's prose, but every factual clause in the
"Expected" is executable, and the strongest of them — *no e2e assertion behind it can fail* — is a
mutation experiment. I ran the experiment instead of grading prose.

### The two sides, at source

`apps/api/test/build.e2e.spec.ts:106-110` — the double:

```ts
      buildVersion: {
        ...collection(store.buildVersions, (a, b) => b.number - a.number),
        async findFirst({ where }: any) {
          if (!owns(where.projectId)) return null;
```

`apps/api/src/auth/workspace-scope.ts:56-62` — production:

```ts
export function applyWorkspaceScope(
  model: string, operation: string, args: Record<string, any>, workspaceId: string,
): Record<string, any> {
  if (!WORKSPACE_SCOPED_MODELS.has(model)) return args;
```

`WORKSPACE_SCOPED_MODELS` holds **6** names (`Project`, `UsageEvent`, `Notification`, `AuditLog`,
`User`, `BuildJob`); `grep -c "^model " apps/api/prisma/schema.prisma` returns **14**. `BuildVersion`
is not among the six. The direction is confirmed: the double **refuses** a read production
**allows**.

### The mutation — the part nobody had run

Copied `apps/api` to the scratchpad and made the double faithful to production, deleting the one
line that refuses:

```
-          if (!owns(where.projectId)) return null;
+          // E1 MUTATION: production applyWorkspaceScope leaves BuildVersion
+          // unscoped (not in WORKSPACE_SCOPED_MODELS). Match production.
```

| | `npx vitest run test/build.e2e.spec.ts` |
|---|---|
| Unmodified double (stricter) | `Tests  44 passed (44)` |
| Double corrected to production | `Tests  44 passed (44)` |

**Not one of the 44 changes colour.** The suite cannot distinguish "BuildVersion lookups are
tenant-scoped" from "they are not", in either direction. E1's claim is not merely that the double
hides a defect — it is that the double's extra strictness is invisible to every assertion behind
it, and that is now measured rather than argued.

### Is there a live defect behind it?

Yes, and at **two** entry points, not the one the skill names. `apps/api/src/modules/build/build.service.ts`:

```ts
195:  async ensureCanStart(workspaceId, projectId, idempotencyKey?) {
202:    if (idempotencyKey && (await this.buildFor(workspaceId, projectId, idempotencyKey))) {
203:      return;                       // ← every later check skipped
...
517:    if (idempotencyKey) {
518:      const already = await this.buildFor(workspaceId, projectId, idempotencyKey);
519:      if (already) {
520:        await emit("finished", this.replayOf(workspaceId, projectId, already));
```

`buildFor` is `this.client(workspaceId).buildVersion.findFirst({ where: { projectId, idempotencyKey } })`
— and for `BuildVersion` the scoped client is the raw client. Both call sites run **before**
`this.project(workspaceId, projectId)`, which is the only thing in the path that would throw for
another tenant's project. A caller holding another workspace's `projectId` and a matching
idempotency key is replayed that workspace's build, with no tenant check anywhere in the sequence.

### The prescription, executed

§4.6 says the test that would catch this is schema-derived and involves no double. It does not
exist, so I wrote it in the copy (`test/e1-probe.spec.ts`) — enumerate `schema.prisma`, assert every
model is scoped or exempted with a reason:

```
 ✓ leaves BuildVersion.findFirst completely unscoped
 × schema-derived invariant: every model is scoped or exempted with a reason
   - Array []
   + Array [ "Message", "SpecVersion", "DesignVersion", "BuildVersion",
   +         "Deployment", "ReferenceAsset", "ReferenceEmbedding" ]
 Tests  1 failed | 1 passed (2)
```

Seven unaccounted models. The invariant is nine lines and goes red on the first run — §5's `tdd`
route to promoting a green, satisfied at birth.

### Outcome — **PASS**, with one correction to the skill

The case's every clause holds. But its supporting text in §1(a) says
*"`apps/api/test/workspace-scope.spec.ts:37` asserts production **does not** scope it"* — and line 37 is:

```ts
  it("leaves non-scoped models untouched (scoped via project instead)", () => {
    const args = applyWorkspaceScope("SpecVersion", "findMany", { where: { projectId: "p1" } }, "w1");
```

That is **`SpecVersion`**, not `BuildVersion`. The "two suites assert opposite things about the same
mechanism" line is one model too generous: nothing anywhere asserts anything about `BuildVersion`'s
scoping. The real state is worse than the one described — an unasserted gap rather than a
contradiction — and the skill should say so.

---

## E2 · Skips that hide the browser path

> Give it `test_interaction_channel.py` — 36 functions, 27 passed, 9 skipped, every skip marked
> *"a browser and node with @electric-sql/pglite are both needed here"*. **Expected:** reports
> **27 ran, 27 passed, 9 skipped**, places the browser interaction path in `unjudged`, and names the
> missing capability. **Fails if** the number 36 appears anywhere as a pass count.

**Classification: RUNNABLE.** Alone among the prose-graded cases it has a fail condition a machine
can check — *the number 36 appears as a pass count* is a string match, not a judgement.

```
$ .venv/bin/python -m pytest tests/test_interaction_channel.py -q -rs
.........................sssssssss..                                     [100%]
SKIPPED [1] tests/test_interaction_channel.py:868: a browser and node with @electric-sql/pglite are both needed here
SKIPPED [1] tests/test_interaction_channel.py:876: ... (×9, :868 :876 :888 :901 :910 :920 :931 :944 :957)
27 passed, 9 skipped in 0.73s

$ grep -c "def test_" tests/test_interaction_channel.py
36
```

Every number in the case is exact: 36 functions, 27 passed, 9 skipped, the skip lines at
`:868`–`:957`, the reason string verbatim.

**The trap is live in the tooling.** The machine-readable report §3 Q3 tells you to parse says:

```xml
<testsuite name="pytest" errors="0" failures="0" skipped="9" tests="36" ...>
```

`tests="36"` — the denominator a naive harness reads is exactly the wrong number. The same holds for
`vitest --reporter=json`, whose `numTotalTests` includes pending. A gate built by reading the first
integer in the report reports 36.

**And nothing in `hello-world` reads it.** `.github/workflows/ci.yml` runs
`apps/engine/.venv/bin/python -m pytest apps/engine -q` and `pnpm --filter @scio/api test`. No
`--junitxml`, no `--reporter=json`, no skip-count gate anywhere in the repo:

```
$ grep -rn "numTotalTests\|junitxml\|reporter=json" apps/ scripts/ .github/   # (excl. node_modules)
(no output)
```

So §7 rule 5 — *CI gates on the skip count, not the pass count* — is unimplemented, and the
critical path it names ("the browser interaction channel") is one of the nine skips.

For scale, the whole engine suite: **640 passed, 21 skipped in 27.35s** — 661 collected. Nine of the
21 are this file's browser tests; four more are `test_verification_data.py` on the same pglite gap;
two are `test_preview_bridge_live.py`.

**Outcome — PASS.** The premise is exact and the fail condition is mechanical. The case tests a
reader, not the repository; the repository has no implementation for it to test, which is E13/E14's
subject.

---

## E3 · A fixture the producer never emits

> Give it the fixture at `:117-125` (`guest_name: text`, `party_size: integer`) and `derive.py:259`
> (every create/update gets `payload: json`). **Expected:** `input_provenance: hand_built`, names
> `derive_architecture` as the producer, demands the shape diff, and predicts that the channel arms
> on **0** real criteria. **Fails if** the 27 passing tests are accepted as evidence the gate works.

**Classification: RUNNABLE** — and it is the only one of E1–E3 that contains a **number nobody had
computed**, so it is the only one of the three that could have been wrong.

The fixture, `tests/test_interaction_channel.py:120-124`:

```python
                inputs=[
                    Column(name="guest_name", type=FieldType.text),
                    Column(name="party_size", type=FieldType.integer),
                ],
```

The producer, `src/scio_engine/layerb/derive.py:258-259`:

```python
        elif verb in {"create", "update"}:
            inputs = [Column(name="payload", type=FieldType.json)]
```

### The shape diff, run

`derive_architecture(make_booking_spec())`, the canonical spec from `conftest.py`:

```
op create_booking [('payload', 'json')]
op cancel_booking [('id', 'uuid')]
```

The real producer emits a single `payload: json`. The fixture's two typed columns are a shape Layer
B cannot produce. `input_provenance: hand_built`, producer `derive.py::derive_architecture`.

### The prediction, measured

`build_plan(derive_architecture(spec))`, then `interaction_criteria(pkg)` per package:

```
  pkg_foundation                 kind=foundation     criteria= 6 interaction=0
  pkg_schema                     kind=schema         criteria= 3 interaction=0
  pkg_design_tokens              kind=design_tokens  criteria= 4 interaction=0
  pkg_auth                       kind=auth           criteria= 2 interaction=0
  pkg_feature_booking            kind=feature        criteria= 8 interaction=0
booking (canonical):          packages=5 criteria=23 INTERACTION CRITERIA=0
booking (signed-in, 2 roles): packages=6 criteria=27 INTERACTION CRITERIA=0
```

**Zero, on two independent fixtures, across 50 acceptance criteria.** The prediction is exact. The
interaction channel — the thing 27 green tests are cited as covering — arms on nothing a real build
produces.

**Outcome — PASS.** The number was a prediction, and it was right.

---

## E4 · A vacuous assertion

> A test whose only assertion is on a double's configured return value. **Expected:** Q1 flags it,
> `can_fail_evidence: none`, counted `unjudged`. **Fails if** it is counted as passing.

**Classification: NOT A TEST.**

The case names **no artifact**. There is no file, no line, no fixture — only a description of a
shape, followed by the definition of that shape restated as the expected answer. *"A test whose only
assertion is on a double's configured return value"* and *"Q1 flags it"* are the same sentence
twice: Q1's own text (§3) lists *"an assertion whose subject is a double's own configured return
value"* as an automatic fail. Nothing can be brought to this case that it does not already contain,
so nothing can make it fail.

Compare E1, E2, E3, E5 and E9, each of which names a file and a line. E4 is the one in that group
that forgot to.

### What I ran anyway, since the case's grep is real

§3 Q1's automatic-fails are greppable, so I ran them over the actual suites.

Python (`apps/engine/tests`, AST walk over every `test_*` function):

```
zero-assertion test bodies: 0
only assertion is `is not None`: 0
except: pass inside a test: 0
```

TypeScript — `expect(x).toBeDefined()`:

```
$ grep -rn "toBeDefined()" --include=*.spec.ts --include=*.test.ts* apps/ | grep -v node_modules | wc -l
86
```

**86 flags.** Every one I inspected is of the form
`expect(screen.getByText("0 of 3 parts done")).toBeDefined()`, where `getByText` **throws** if the
element is absent — so the assertion is redundant, not vacuous. Verified by mutation rather than by
reading: changing that string to `"0 of 4 parts done"` in a copy gives

```
TestingLibraryElementError: Unable to find an element with the text: 0 of 4 parts done
 Tests  1 failed | 25 passed (26)
```

**The rule fires 86 times and is right 0 times here.** That is a finding about §3's greppable list,
not about the suite: `toBeDefined()` is diagnostic only when the subject is a plain value, and a
testing-library query is not one. The rule needs the qualifier or it teaches people to ignore it —
which is precisely what §8 says a flaky signal does.

**Outcome — NOT A TEST.** Reported as such rather than as a pass, per §5's own logic: a case that
restates its answer cannot be evidence about anything.

---

## E5 · A substring standing in for a check

> Give it `check_tests_present` (`validation.py:132`). **Expected:** flags the substring, produces a
> **concrete false-positive path** — `app/latest/page.tsx` — and adds the second finding that no
> runner exists to run a real match. **Fails if** it fixes the pattern without noticing there is
> nothing behind it.

**Classification: RUNNABLE.** The "concrete false-positive path" is not a claim to grade, it is a
function call.

`src/scio_engine/builder/validation.py:132`:

```python
    test_files = [p for p in files if "test" in p.lower() or "spec" in p.lower()]
```

Called for real, with a package that has an operation node and one file:

```
$ .venv/bin/python e5_check.py
files given: ['app/latest/page.tsx']
findings: []
VERDICT: gate PASSED (no findings) on a package with zero tests
```

`la**test**/` matches. The gate returns an empty finding list — a clean pass — for a package
containing no test of any kind.

### The second finding, also confirmed

`src/scio_engine/builder/workspace.py:66-77`, `DEV_DEPENDENCIES`: `typescript`, `@types/node`,
`@types/react`, `@types/react-dom`, pglite, `tailwindcss`, `postcss`, `autoprefixer`. **No test
runner.** And `package_json()` at `:102-116` declares `scripts: {dev, build, start, lint}` — **no
`test` script.**

So even a correct match would have nothing to run. And a third finding the case does not mention,
found while looking: **`check_tests_present` has no test of its own** —
`grep -rn "check_tests_present" tests/` returns nothing. The check that guards "every package has a
test" is the one function in the file nobody wrote a test for.

**Outcome — PASS.** Both halves reproduce, executed. The case is well-formed because it names the
artifact and predicts a specific string, which either matches or does not.

---

## E6 · A green generated suite

> A generated app's own tests are green. **Expected:** `unjudged`, never in `checks_passed`, citing
> Lin et al. **with its scope**. A failing one is a `Remainder`. **Fails if** green raises
> `checks_passed`, or if Lin et al. is quoted without its SWE-bench scope.

**Classification: NOT A TEST.**

Two independent reasons, and the second is the more interesting.

**(1) Its premise cannot occur.** A generated app's tests are never green, because they are never
run. E5 established the workspace ships no test runner and no `test` script. The gate list is
`src/scio_engine/builder/loop.py:61`:

```python
GATES = ("instrumentation", "validation", "console", "interaction", "critique")
```

There is no test gate. `check_tests_present` lives inside `validation` and checks only that a
filename contains the letters `test`. Nothing anywhere executes a generated test, so
`checks_passed` cannot be raised by one — the failure the case forbids is unreachable, which means
the case cannot fail.

**(2) Its second fail condition is unfalsifiable as stated.** *"Fails if Lin et al. is quoted
without its SWE-bench scope"* grades whether a reader repeats a sentence that is printed twice in
the same document (§2's table and §11's limits). It measures recall of the page it is written on.

**What would make it a test.** Point it at a `PackageBuildResult` and assert
`checks_passed` is unchanged by a green generated suite — an arithmetic assertion on an object that
exists (`builder/result.py:71`). That version can fail. The version written cannot.

---

## E7 · Eight clean runs on a known flake

> B105, eight green observations. **Expected:** refuses to declare it cleared; states 3/8 = 37.5%;
> notes the independence assumption; prescribes `--repeat` with a fixed seed under CI concurrency
> plus a randomised-order job. **Fails if** it reports the flake as resolved.

**Classification: NOT A TEST — its pass condition now rewards the wrong answer.**

### First, the observations, reproduced

`docs/next/LAYER-F-DESIGN-WINDOW.md` §1.2 records `design.test.tsx` alone 5× (29 passed each) and
the full `apps/app` suite 3× (8 files, 109 passed each). Re-run today:

```
$ for i in 1 2 3 4 5; do npx vitest run src/pages/design.test.tsx; done
      Tests  29 passed (29)     ×5

$ for i in 1 2 3; do npx vitest run; done
 Test Files  8 passed (8)
      Tests  109 passed (109)   ×3
```

Identical, to the count. Eight more green observations, so **sixteen** in total, zero failures. The
rule of three now gives a 95% upper bound of **3/16 = 18.75%** — and §8's own caveat applies with
more force, not less: sixteen runs in the same order on the same idle machine sample one condition
sixteen times.

### Why the case fails as a case

`hello-world` records B105 as **done**, with the cause found:

```
docs/BACKLOG.md:156 | B105 | design.test.tsx is flaky ... | PP2 | P0 | done |

docs/CHANGELOG.md:592 — 2026-08-22 — The flaky test had two causes, and neither was the obvious one
  (B105). ... One: the page waits a real five seconds before calling a preview gone, and the test
  waited it out with an 8-second margin. ... Fake timers now advance the clock instead.
```

And the fix is in the file: `src/pages/design.test.tsx:577` `vi.useFakeTimers()`, `:581`
`vi.advanceTimersByTime(5000)`.

So the skill's §8 premise — *"B105 records `design.test.tsx` failing on two consecutive runs with
the cause never found"* — is **stale**. A root cause was found and repaired, by exactly the method
§8 prescribes (diagnose, do not re-run). The correct answer today is *"B105 is resolved, and the
evidence is the root cause and its fix, not the sixteen green runs."*

E7's fail condition is *"fails if it reports the flake as resolved."* **A correct answer fails this
case, and the answer that passes it is wrong.** A case whose pass condition rewards the wrong
answer is worse than no case, and it is worth noticing that it went wrong in the one way this skill
is built to catch: the case was frozen against a state of the world, and nothing bound it to the
bytes it was written about. That is §9.5(c), applied to the eval itself.

**Outcome — NOT A TEST.** The arithmetic is sound and is preserved above; the case is not.

---

## E8 · A request for a coverage gate

> Someone asks for an 80% line-coverage gate. **Expected:** refuses it as a gate, cites Inozemtseva
> & Holmes and Zhao et al., offers incremental mutation on changed files and a coverage **map**
> instead. **Fails if** the gate is set, or if a mutation-score threshold is set in its place.

**Classification: NOT A TEST.**

There is nothing to run and nothing to check. `hello-world` has no coverage tooling at all:

```
$ grep -rn "coverage\|--coverage\|c8\|istanbul" apps/*/package.json apps/*/vitest.config.ts \
    .github/ apps/engine/pyproject.toml
(no output)
```

So the case cannot be executed against anything, and what remains is a question whose expected
answer is §10's "Marketing, or actively harmful here" bullet, restated. The two cited papers appear
in §2, §10 and §11 of the same document.

This is the ablation-02 failure mode named in `catalog-budget-ablation-03.md`: *"an eval question
must be one where the confident wrong answer is the natural one."* Refusing a coverage gate is not a
confident wrong answer anyone has to be talked out of — the control arm in
`testing-ablation.md` question 2 reached *"coverage is the wrong lever"* on its own, with no skill
loaded. E8 asks a question the baseline already answers.

---

## E9 · An implementation absent from its own conformance suite

> `AcaSandbox` versus `test_sandbox_conformance`'s provider list. **Expected:** add it; state that
> the resulting **red test is the correct outcome**; and add the rule that a provider outside the
> suite is not a provider. **Fails if** the exclusion is treated as intentional.

**Classification: RUNNABLE.** The case predicts a colour change from a one-line edit. That is a
prediction, and it is falsifiable — the test could have stayed green.

Baseline in the copy:

```
$ pytest tests/test_sandbox_conformance.py -q
.........                                                                [100%]
9 passed in 0.20s
```

`tests/test_sandbox_conformance.py:30` reads `PROVIDERS = [LocalProcessSandbox, LocalDockerSandbox]`.
`src/scio_engine/core/aca_sandbox.py:21` defines `class AcaSandbox(SandboxProvider)`. Added it:

```
PROVIDERS = [LocalProcessSandbox, LocalDockerSandbox, AcaSandbox]
```

```
$ pytest tests/test_sandbox_conformance.py -q --tb=line
E   TypeError: AcaSandbox.start() got an unexpected keyword argument 'env'
    tests/test_sandbox_conformance.py:99: TypeError
E   TypeError: AcaSandbox.start() got an unexpected keyword argument 'env'
    tests/test_sandbox_conformance.py:150: TypeError
FAILED tests/test_sandbox_conformance.py::test_every_provider_passes_the_callers_env_to_the_app[aca]
FAILED tests/test_sandbox_conformance.py::test_no_provider_leaks_the_platforms_secrets[aca]
2 failed, 10 passed in 0.21s
```

### The defect is worse than the case predicted

The case expects a red test because `AcaSandbox` raises `NotImplementedError`-shaped errors. That is
not what happened. The signatures do not match:

```python
# src/scio_engine/core/sandbox.py:46 — the interface
    def start(self, app_dir: Path, *, port: int = 0, env: dict[str, str] | None = None) -> SandboxHandle:

# src/scio_engine/core/aca_sandbox.py:63 — the implementation
    def start(self, app_dir: Path, *, port: int = 0) -> SandboxHandle:
```

`AcaSandbox.start` **does not accept `env` at all**. It fails on the call, not in the body. This is
the same defect as B107 — *"LocalDockerSandbox.start() ignores its env argument, so the marking
bridge and the verification layer are dead on any Docker host — silently"*, `docs/BACKLOG.md:158`,
marked done — reintroduced in a third provider, and invisible because that provider is not in the
suite written to catch it. The file's own docstring says it:

> *"An abstract method whose contract one implementation ignores is worse than no abstraction: every
> caller is written against the promise."*

**Outcome — PASS**, and a live defect found. Two lines, two red tests, one real interface violation
that no suite in the repository could reach. This is the strongest case in the set: it names an
artifact, predicts a colour change, and the change happened for a reason the case did not know.

---

## E10 · An absence test with no twin

> A suite asserts a secret never reaches the logs and nothing in the suite ever puts one there.
> **Not evidence.** Expected: a permanent test that seeds a leak and asserts it is caught, in the
> same file. §3.5.

## E11 · A negative test that passes because the feature was deleted

> Remove the call the negative test forbids, entirely. The negative test still passes; the twin that
> asserts the permitted call **must** go red. If nothing goes red, the pair is missing.

**Classification: both RUNNABLE.** E10 is a shape with no named artifact — on its own that would put
it with E4 — but E11 supplies the **procedure** that turns it into an experiment, and `hello-world`
supplies the subject. One mutation answers both, so they are reported together.

### The subject

`tests/test_sandbox_conformance.py:107-152`, `test_no_provider_leaks_the_platforms_secrets` — a
textbook absence test. It plants a secret and asserts it does not arrive:

```python
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret")
    ...
    provider().start(tmp_path, port=4321, env={})
    assert "ANTHROPIC_API_KEY" not in seen
    assert not any("sk-ant" in value for value in seen.values())
```

**It never asserts that `seen` is non-empty.** That is the third rot mode in §3.5 — *the fixture
never established its precondition* — and §3.5 names the repair: *"assert the mechanism ran, not
that the outcome looked right."*

### Mutation 1 — the detector still works (the control)

Added `"ANTHROPIC_API_KEY"` to `INHERITED_ENV` in `core/sandbox.py`, reintroducing the leak the
allow-list was built to stop:

```
FAILED tests/test_sandbox_conformance.py::test_no_provider_leaks_the_platforms_secrets[local-process]
FAILED tests/test_sandbox_conformance.py::test_no_provider_leaks_the_platforms_secrets[local-docker]
4 failed, 8 passed in 0.22s
```

Red for both real providers. The test does have detection power against a widened allow-list. So
far, so good.

### Mutation 2 — E11's procedure, run literally

Remove the mechanism entirely. `LocalProcessSandbox.start` returns before it ever spawns a child:

```python
        app_dir = app_dir.resolve()
        # E10 MUTATION B: a plausible regression — reuse a live preview and
        # never spawn. The child is never started, so nothing can leak into it.
        if True:
            return SandboxHandle(url="http://127.0.0.1:0", workdir=app_dir, kind=self.name)
```

```
$ pytest tests/test_sandbox_conformance.py::test_no_provider_leaks_the_platforms_secrets \
         tests/test_sandbox_conformance.py::test_every_provider_passes_the_callers_env_to_the_app -q --tb=line
E   AssertionError: the marking bridge arrives only through env — a provider that drops it
    produces a preview where clicking does nothing, and says nothing
    assert None == '1'
     +  where None = {}.get('SCIO_PREVIEW_MODE')
FAILED tests/test_sandbox_conformance.py::test_every_provider_passes_the_callers_env_to_the_app[local-process]
1 failed, 3 passed in 0.19s
```

**Two tests, one fixture, one mutation, opposite verdicts:**

| Test | Shape | Under a mutation that deletes the child process |
|---|---|---|
| `test_every_provider_passes_the_callers_env_to_the_app` | asserts a **presence** — `seen.get("SCIO_PREVIEW_MODE") == "1"` | **RED** |
| `test_no_provider_leaks_the_platforms_secrets` | asserts an **absence** | **GREEN** |

The leak test is green while the code it tests does nothing at all. Its `seen` dict is `{}`, and
`"ANTHROPIC_API_KEY" not in {}` is true for the least interesting reason there is.

### Outcomes

**E10 — PASS, and it caught a live one.** `hello-world` has exactly the test E10 describes: an
absence assertion that passes when the mechanism is removed. The repair is one line inside the
existing test — `assert seen`, or better `assert seen.get("SCIO_PREVIEW_MODE") == "1"` — which
would have made mutation 2 red.

**E11 — PASS, as a procedure.** Its prediction held precisely: the negative test stayed green, the
twin went red, and the pair is therefore *not* missing here — the file happens to contain both. But
the guarantee does not transfer, because they are two independent test functions. Delete or skip
`test_every_provider_passes_the_callers_env_to_the_app` and the leak test is left certifying
nothing, with no signal that anything changed. §3.5's law says the control belongs *in the same
test*, and this file has it in the same *file*. That distinction is the difference between a
guarantee and a coincidence.

### Where E11 finds no pair at all

Applied to `apps/api/test/tenant-discipline.spec.ts` — a negative test that greps the source for a
forbidden call — the answer is the other one. There is **no twin asserting the permitted call**
(`scope.forWorkspace`) anywhere in the API suite. Planting a violator proves the rule fires:

```
$ npx vitest run test/tenant-discipline.spec.ts     # after adding src/evil/leak.service.ts
AssertionError: these read rows without workspace scoping — use scope.forWorkspace(workspaceId),
or add the file to ALLOWED with the reason it is safe: expected [ 'evil/leak.service.ts' ] to deeply equal []
 Tests  1 failed | 1 passed (2)
```

— but see E12 for what happens next.

---

## E12 · An exemption added to a rule

> A carve-out lands with a test that it applies. Expected: also a test that the rule still fires
> just outside the carve-out, pinned to the evidence that justified it — not to a shape.

**Classification: RUNNABLE.** `hello-world` has a real exemption list, so the case has a subject.

`apps/api/test/tenant-discipline.spec.ts:25-37` — three carve-outs from *"no service reads rows
through the unscoped Prisma client"*:

```ts
const ALLOWED = new Map<string, string>([
  [join("auth", "provisioning.service.ts"), "runs BEFORE any workspace context exists — it is what creates one"],
  [join("auth", "workspace-scope.ts"),      "is the scoping client itself"],
  [join("prisma", "prisma.service.ts"),     "is the client"],
]);
```

The file has two tests: the rule itself, and *"the allow-list names files that exist"* — a drift
check, described in its own comment as *"an allow-list that has drifted is a hole with a comment
over it."* Neither is the test E12 demands. There is **no assertion that the rule still fires just
outside the carve-out**, and the exemptions are pinned to nothing but a prose reason no test reads.

### The experiment

Continuing from E11: `src/evil/leak.service.ts` contains
`this.prisma.buildVersion.findMany({ where: { projectId: "p1" } })` — a genuine unscoped
cross-tenant read, and the rule catches it (output above). Now add four lines to `ALLOWED`:

```ts
  [
    join("evil", "leak.service.ts"),
    "E12: a carve-out with a reason nobody checked",
  ],
```

```
$ npx vitest run test/tenant-discipline.spec.ts
 Test Files  1 passed (1)
      Tests  2 passed (2)
```

**Green, with the cross-tenant read still in the source.** Both tests pass — the rule because the
file is exempted, the drift check because the file exists. The exemption is validated by the
existence of the thing it exempts.

**Outcome — PASS, and the repository fails the check.** A four-line diff to a *test* file, needing
no change to production code and no reviewer's attention on a `.ts` under `test/`, silently converts
a tenancy violation into a green suite. The reason string is decoration: nothing reads it, nothing
checks it, and nothing binds it to the evidence that would justify it. §3.5's phrasing — *"an
exemption with only an inside test can widen silently"* — understates it. This one widens on a line
of its own choosing.

The repair E12 names is checkable: a permanent fixture outside the carve-out that the rule must
flag, in the same file, so that a widened `ALLOWED` cannot also silence the control.

---

## E13 · A truncated run reporting green

> Build a suite that exits 0 after running a fraction of its files — a delayed `process.exit`, a
> killed shard, a runner that stops on an unhandled error. Expected: the gate refuses the zero exit
> because the executed-unit count is below the planned count, and names both numbers. A gate that
> reads only the exit code, or only the printed summary, fails. §9.5(a).

**Classification: BLOCKED.** The gate the case grades does not exist — anywhere. The whole of
`hello-world`'s test gating is `.github/workflows/ci.yml`:

```yaml
      - name: Engine tests
        run: apps/engine/.venv/bin/python -m pytest apps/engine -q
      - name: API tests
        run: pnpm --filter @scio/api test
      - name: App tests
        run: pnpm --filter @scio/app test
```

Three exit codes. No planned count, no executed count, no report parsed. There is nothing to run the
case against.

### But the case's first sentence is buildable, so I built it

Five files, ten tests. The first file arms a timer in the gstack shape; four of the ten assertions
are deliberate failures.

```python
def test_arms_a_timer_in_teardown():
    # The gstack shape: a timer armed here fires mid-way through a LATER file.
    threading.Timer(0.4, lambda: os._exit(0)).start()
```

```
$ pytest . -q --collect-only  |  tail -1
10 tests collected in 0.01s

$ pytest . -q > out.txt 2>&1 ; echo "EXIT: $?"
EXIT: 0
$ cat out.txt
...
```

**Three of ten units executed. Exit code 0. No summary line at all** — the output is literally three
dots. The four planted failures never printed. Disarming the timer:

```
$ pytest . -q > out2.txt 2>&1 ; echo "EXIT: $?"
EXIT: 1
4 failed, 6 passed in 2.43s
```

§9.5(a)'s claim — *"the truncated run is indistinguishable from a green one by exit code alone"* —
is reproduced exactly, on the same runner `hello-world` gates on. A CI step whose only signal is
`$?` would report this build green.

*(A methodological note, because this eval nearly made the mistake it is auditing: my first
measurement read `$?` after a pipe into `tail`, which returns `tail`'s status and is always 0. The
numbers above are from a redirect, not a pipe. An exit code read through a pipeline is not evidence
either.)*

### What must be built

A harness that (i) knows a **planned** unit count before it runs — `--collect-only` for pytest,
`vitest list` for vitest — (ii) records the **executed** count from the machine-readable report, and
(iii) refuses a zero exit when executed < planned, naming both integers. §9.5(a)'s two
implementation details apply on the way in: per-origin stdout/stderr buffers, and a signal handler
that terminates the run rather than the current child.

**Would E13 then be a good test of it?** Yes — it is one of the best-specified cases in the set. It
names three distinct truncation mechanisms, states the numeric condition, and specifies two ways to
fail it (reads only the exit code; reads only the summary). The fixture above is a working red input
for it today.

---

## E14 · A reported summary that does not add up

> Hand the gate a report where `passed + failed + skipped != total`, then one where a red phase has
> zero failures, then one where the total dropped since the previous run. Expected: three rejections
> and one flag, all arithmetic, no model consulted. Then remove the previous-count input and assert
> the regression check still runs — an optional check is an absent check. §9.5(b).

**Classification: BLOCKED.** No such validator exists, and nothing in the repository reads a test
count at all:

```
$ grep -rn "numTotalTests\|junitxml\|reporter=json\|passed + failed\|previous_total\|TestResultValidator" \
    apps/ scripts/ .github/          # (excl. node_modules, .venv)
(no output)
```

**What must be built.** The six checks of §9.5(b) over four integers plus a previous total, with the
previous-count field **required** rather than optional. §9's rule 6 already specifies where it sits:
*"a `counts` block that does not add up is rejected before any of rules 1–5 are evaluated."*

**Would E14 then be a good test of it?** Yes, and it is the best-constructed case in the whole set —
the only one that specifies its **inputs** rather than its subject. Three malformed reports and one
regression case, each with a stated verdict, all decidable by arithmetic with no model in the loop.
It is also the only case that tests its own gate for the defect its source disclosed: *"remove the
previous-count input and assert the regression check still runs."* That final clause is a
positive-control in §3.5's sense, applied to a validator, and it is what stops the check being
switched off by omission.

One ambiguity to resolve before building: the case says *"three rejections and one flag"* for four
inputs, and §9.5(b)'s table marks only `total < previous_total` as *flagged* while the rest are
hard failures. That reading is consistent, but the case does not say which of the four is the flag —
it must be stated, or the implementer will pick the reading that passes.

---

## E15 · Evidence that outlived its subject

> Record a passing run, change a source file, re-request the claim. Expected: STALE, not PASS. Then
> record on a dirty tree and commit exactly that content: expected FRESH. Then name two lanes and
> let one never run: expected MISSING for that lane, and the green sibling does not carry the
> verdict. §9.5(c).

**Classification: BLOCKED.** There is no evidence ledger, no working-tree fingerprint, and no
FRESH/STALE/MISSING vocabulary anywhere in `hello-world`:

```
$ grep -rn "STALE\|FRESH\|fingerprint\|evidence ledger" apps/engine/src apps/api/src scripts
apps/api/src/modules/intake/intake.service.ts:379:/** A stable fingerprint of a spec.
```

One hit, and it is a spec hash, unrelated.

**What must be built.** A record binding a run to (a) a content fingerprint of the working tree, not
a commit; (b) the exact command by hash; (c) a named lane. Grading FRESH / STALE / MISSING, with:
mutation mid-run ⇒ omit the fingerprint and grade STALE; gitignored churn does not invalidate but a
new untracked source file does; a recorded failing run is never FRESH; a fabricated fingerprint
degrades to STALE rather than crashing; every named lane must be FRESH or the claim does not stand.

**Would E15 then be a good test of it?** Mostly. Its three sub-cases are precise and each has a
stated expected grade, including the counter-intuitive one (dirty-tree record → commit → still
FRESH), which is exactly the shape a good case has: **the obvious answer is that committing
invalidates the record, and it does not.**

Its weakness is the third clause. *"The green sibling does not carry the verdict"* is a claim about
a composite verdict the case never defines — is the overall grade MISSING, or is it a per-lane
report with no overall grade at all? Two readings, different implementations, and the case chooses
neither. State it before building, rather than after.

**And E15 has already caught something, without being implemented.** E7 above is a claim recorded
against a state of the world (*"B105 … cause never found"*) that a later commit invalidated, and
nothing anywhere noticed. That is precisely the failure E15 exists to prevent, occurring inside the
skill that defines it.

---

## E16 · A child that inherited the machine

> Assert every process a harness spawns builds its environment through one explicit constructor.
> Grep for a spread of the ambient environment into a child. Any occurrence fails, and the test that
> asserts it must itself have a positive control that plants a variable and proves it does not
> arrive. §9.5(d) and §3.5.

**Classification: RUNNABLE.** Unlike E13–E15 this one needs no gate — it is a source-tree invariant,
and §6's own table calls that shape *"the strongest test in this document."* I wrote it and ran it.

`tests/test_e16_harness_env.py`, three tests: the literal grep, a stronger AST form, and the
positive control §3.5 demands.

```
$ pytest tests/test_e16_harness_env.py -q --tb=short
FF.                                                                      [100%]

_________ test_no_source_spreads_the_ambient_environment_into_a_child __________
E   AssertionError: builder/workspace.py:350: env={**os.environ, "NEXT_TELEMETRY_DISABLED": "1", "CI": "1"},
E     core/sandbox.py:94: # It used to see everything: the child was started with `**os.environ`, which at

__________ test_every_child_process_names_its_environment_explicitly ___________
E   AssertionError: builder/persistence.py:26: subprocess.run(...) with no env=
E     builder/typecheck.py:101: subprocess.run(...) with no env=
E     core/sandbox.py:294: subprocess.run(...) with no env=
E     core/sandbox.py:321: subprocess.run(...) with no env=
E     core/sandbox.py:343: subprocess.run(...) with no env=
E     core/sandbox.py:429: subprocess.run(...) with no env=
E     core/sandbox.py:377: subprocess.run(...) with no env=
E     core/sandbox.py:390: subprocess.run(...) with no env=
E     core/sandbox.py:459: subprocess.run(...) with no env=

2 failed, 1 passed in 0.36s
```

### What the two failures mean

**The literal grep finds a real one.** `src/scio_engine/builder/workspace.py:343-350`:

```python
        result = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund", "--loglevel=error"],
            cwd=scratch, ... 
            env={**os.environ, "NEXT_TELEMETRY_DISABLED": "1", "CI": "1"},
        )
```

`npm install` — a process that fetches and executes third-party install scripts from the network —
is handed the platform's entire environment, which at that moment holds `ANTHROPIC_API_KEY` and
`SCIO_CATALOG_DB` (a database URL with credentials). §9.5(d)'s incident report is thirty lines away
in the same repository, at `core/sandbox.py:94`:

> *"It used to see everything: the child was started with `**os.environ`, which at that moment holds
> ANTHROPIC_API_KEY and SCIO_CATALOG_DB — a database URL with credentials."*

The lesson was written down, an allow-list (`INHERITED_ENV`, `child_environment()`) was built for
the *generated app's* process, and the harness's own `npm install` was left inheriting everything.

**The stronger form finds nine more, and they are the quieter half.** `subprocess.run` with no
`env=` inherits the full parent environment by default — the same leak, with nothing to grep for.
Two of the nine are the ones that matter: `builder/persistence.py:26` (`git`, run inside the
generated app's directory) and `builder/typecheck.py:101` (`tsc`, ditto). The seven under
`core/sandbox.py` are `docker` CLI invocations, where the parent's environment reaches the docker
client rather than the container, so they are the weaker finding — but they are indistinguishable
from the other two by the grep E16 prescribes, which is the point.

**The grep as written also produces one false positive:** `core/sandbox.py:94` is a *comment*
describing the historical bug. A text grep over source cannot tell the incident report from the
incident. The AST form has no such problem, and E16 should specify it.

### The positive control passes

```python
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-planted")
    monkeypatch.setenv("SCIO_CATALOG_DB", "postgres://u:p@host/db")
    env = child_environment(port=4321)
    assert "ANTHROPIC_API_KEY" not in env
    assert "SCIO_CATALOG_DB" not in env
    assert env["PORT"] == "4321"        # and the constructor really ran
```

Green. The allow-list does what it claims, and — note the last line, which is exactly what E10's
subject is missing — the test proves the mechanism ran rather than that the outcome looked right.

**Outcome — PASS, and the repository fails the check.** E16 is, with E9 and E14, one of the three
best cases in the set: it states a mechanical procedure, a threshold (*any* occurrence), and its own
positive-control obligation. It found one explicit leak and nine implicit ones on first execution.

---

## What the cases reveal about the skill that wrote them

### The single strongest predictor of whether a case is a test is whether it names a file

| Names an artifact at `file:line` | Cases | Result |
|---|---|---|
| **Yes** | E1, E2, E3, E5, E9, E12*, E16* | all runnable; 4 found live defects |
| **No** | E4, E6, E7, E8, E10*, E11*, E13, E14, E15 | 4 NOT A TEST, 3 BLOCKED, 2 rescued |

\* E12 and E16 name a *rule* rather than a file, and the repository supplied the subject. E10 and
E11 name neither, and were only runnable because E11's **procedure** could be pointed at a subject
E10 lacked — they rescue each other, and neither would have been runnable alone.

Every case that failed to be a test failed the same way: it described a shape and then restated the
description as the expected answer. E4 is the clearest — *"a test whose only assertion is on a
double's configured return value"* / *"Q1 flags it"* — and Q1's own text already lists that shape as
an automatic fail. Nothing external is consulted, so nothing can make it fail. **A case that cannot
fail is the exact defect this skill exists to catch in other people's work, and four of its own
sixteen are it.**

### The skill's own asymmetric rule, turned on the eval set

§5: *a passing test is `unjudged` until it has been shown capable of failing.* Applied to the
sixteen cases, the honest ledger is not 9 PASS. It is:

| | |
|---|---|
| Shown capable of failing, by a colour change I observed | **E9, E10, E11, E12, E16** — 5 |
| Made a numeric prediction that could have been wrong | **E3** (0 interaction criteria), **E1** (44 → 44) — 2 |
| Confirmed a fact its author had already read | **E2, E5** — 2 |
| Cannot fail | **E4, E6, E7, E8** — 4 |
| No implementation to run against | **E13, E14, E15** — 3 |

**Seven of sixteen carry real information.** E1–E3 are labelled in the skill as *"the three real
failures … each is a case the skill must catch, not merely describe"*, and two of the three are
records of a reading rather than checks that could have gone either way. E3 is the exception, and
it is the exception precisely because it contains a number — `0` — that had to be computed.

### The rules the skill is sharpest about are the ones its own cases honour least

- **"Green is `unjudged` until the test is shown capable of failing."** Of the nine runnable cases,
  five demonstrate a test going red and four do not. E2 and E5 assert a state without ever showing
  the assertion could have come out otherwise — E5 in particular reports *"the gate passed"* with no
  companion showing what makes it fail. Neither case is wrong; both are `unjudged` by their own
  standard.
- **"A double stricter than production hides a defect."** True here, and now measured: the double is
  stricter, and its strictness is invisible to all 44 assertions behind it. But the supporting text
  overstates the evidence — see E1's correction. `workspace-scope.spec.ts:37` is about `SpecVersion`;
  nothing anywhere asserts anything about `BuildVersion`. "Two suites assert opposite things" is a
  better story than "one gap nobody asserted", and the worse story is the true one.
- **"'27 passed, 9 skipped' must never be reported as '36 tests pass.'"** Verified to the integer,
  and the trap is confirmed live in the tooling: pytest's own JUnit XML reports `tests="36"`. The
  rule holds. Nothing in the repository implements it.
- **"Exit 0 is not evidence."** Reproduced: 3 of 10 units, exit 0, no summary. The repository's CI
  gates on exactly the three exit codes this defeats.

### Three findings the cases did not anticipate, which is the best sign they were worth running

1. **`AcaSandbox.start()` does not accept `env`.** E9 predicted a red test from a stub raising an
   error. The actual failure is a signature mismatch — a reintroduction of B107, closed weeks ago
   in a different provider, and invisible because the new provider is not in the suite written to
   catch B107.
2. **The idempotency replay has no tenant check at either entry point**, not one — `ensureCanStart`
   at `:202` short-circuits before every subsequent check, as well as `run` at `:518`.
3. **`check_tests_present` has no test of its own.** The function that enforces "every package has a
   test" is the one in its file that nobody wrote a test for.

### One case is actively wrong, and it broke in the skill's own blind spot

E7's premise — *B105, cause never found* — was true when written and is not true now:
`docs/BACKLOG.md:156` marks it **done**, `docs/CHANGELOG.md:592` names the two causes, and
`design.test.tsx:577` contains the fix. E7 fails an answer that says the flake is resolved. The
resolved answer is the correct one. **A case whose pass condition rewards a wrong answer is worse
than no case** — and the mechanism of the rot is §9.5(c), a claim not bound to the bytes it was made
about, occurring in the document that defines the rule.

### What a rewrite would change

1. **Every case names an artifact at `file:line`, or it is deleted.** That single rule reclassifies
   E4, E6 and E8, and it is the difference between the seven cases that worked and the nine that
   did not.
2. **Every case states its inputs, not its subject.** E14 is the model: three malformed reports and
   one regression case, each with a stated verdict. Compare E4's *"a test whose only assertion…"*.
3. **Every case states what a wrong answer looks like, concretely.** E2's *"fails if the number 36
   appears anywhere as a pass count"* is a string match. E8's *"fails if the gate is set"* names no
   artifact that could hold a gate.
4. **A case that grades prose is labelled as such and expected to survive an ablation.** E7's
   expected answer is §8 recited; E6's second clause grades whether a reader repeats a scope
   sentence printed twice on the same page. `catalog-budget-ablation-03.md`'s standard applies:
   *an eval question must be one where the confident wrong answer is the natural one.*
5. **E1–E3 stop being described as cases the skill "must catch."** They are the three findings the
   skill was built from. Calling a record a test is the category error the skill spends §5 on.

---

## What must exist before the blocked cases can run

All three blocked cases need the same thing that does not exist: **a harness that produces and
checks numbers, rather than a shell that reads exit codes.** Today the entire test gate is three
lines of `.github/workflows/ci.yml` and three `$?` values.

### 1 · A planned-count-aware runner — unblocks E13

- Compute a **planned** unit count before the run: `pytest --collect-only -q` (returns
  `10 tests collected` on the E13 fixture), `vitest list` for the two TypeScript suites.
- Run with a machine-readable reporter: `pytest --junitxml`, `vitest --reporter=json`. Note the
  denominator trap E2 confirmed — JUnit's `tests=` and vitest's `numTotalTests` **include skips**;
  the executed count is `tests - skipped`.
- Refuse a zero exit when executed < planned, **naming both integers**.
- Per-origin stdout/stderr buffers; a signal handler that terminates the run, not the current child.

The E13 fixture in the scratchpad is a working red input: 10 planned, 3 executed, exit 0.
**E13 would then be a good test of it** — it names three truncation mechanisms and two distinct ways
for the gate to fail.

### 2 · An arithmetic report validator — unblocks E14

The six checks of §9.5(b) over `{total, passed, failed, skipped, previous_total}`, with
`previous_total` **required**. Placed as §9 rule 6 specifies: before rules 1–5.

**E14 would then be a very good test of it** — it is the only case in the set that specifies its
inputs rather than its subject, and its last clause tests the validator's own off-by-default
failure mode. **Resolve one ambiguity first:** the case says "three rejections and one flag" without
saying which of the four inputs is the flag. §9.5(b)'s table implies it is `total < previous_total`.
Write that down, or an implementer will choose the reading that passes.

### 3 · An evidence ledger — unblocks E15

Content-fingerprinted records binding a claim to a working tree, a command hash and a named lane,
grading FRESH / STALE / MISSING, with the sub-rules in E15's entry above.

**E15 would then be a good test of it**, with one clause to sharpen: *"the green sibling does not
carry the verdict"* does not say whether the composite grade is MISSING or whether there is no
composite grade at all.

### And two repairs the runnable cases have already earned

Neither is blocked on anything; both are small, and both close a defect this eval measured.

| | Fix | Effect |
|---|---|---|
| **E9** | Add `AcaSandbox` to `PROVIDERS` (`test_sandbox_conformance.py:30`) and give `start` the `env` parameter the interface declares | Converts a latent runtime error into a red test today; the red is the correct outcome |
| **E10** | Add `assert seen.get("SCIO_PREVIEW_MODE") == "1"` inside `test_no_provider_leaks_the_platforms_secrets` | Makes the absence test go red when the mechanism is removed — it currently does not |
| **E16** | Route `workspace.py:350` and the `git`/`tsc` spawns through `child_environment()`; land the AST assertion as a permanent test | Stops `npm install` receiving `ANTHROPIC_API_KEY` |
| **E12** | Add a permanent fixture outside `ALLOWED` that the rule must flag | Stops a four-line carve-out silencing the tenancy fence |
| **E1** | Land the schema-derived invariant (nine lines, red on the first run) and close the `BuildVersion` gap at `build.service.ts:202` and `:518` | The only check in §4 that involves no double at all |

---

## Method, and what was touched

- `/home/user/hello-world` was **not modified**. `git status --porcelain` is clean of any change of
  mine before and after; pytest ran with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`.
  *(One untracked file, `apps/api/test/zz-e4-double-vs-production.spec.ts`, appeared in the tree
  mid-session and was gone by the end. It was not mine — its header read `SCRATCH —
  tenant-isolation E4` — and I left it alone. The tree is clean at the time of writing.)*
- Every mutation ran against copies under the session scratchpad: `engine/` (src + tests, venv
  reused by absolute path), `api/` and `app/` (source copied, `node_modules` symlinked), and a
  standalone `e13/` fixture suite.
- Baselines, for anyone re-running: engine **640 passed, 21 skipped in 27.35s**; api **135 passed,
  0 failed, 0 skipped** across 12 files (`build.e2e.spec.ts` = 44); app **8 files, 109 passed**.
- Nothing in this document is a described result. Where a command produced no output, that is stated
  and the command is shown.
