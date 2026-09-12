# Layer E · Build & execution — as built

Plan in, running app out — and a status you can check. 42 files, 9,393 lines, **41% of the
codebase**. 247 engine tests passing and 9 environment-skipped, plus 44 API build tests,
run 2026-08-26.

Governed by **ADR-0005** (sandbox), **ADR-0011** (generated-app stack) and **ADR-0020**
(builds as jobs, *Partly implemented*).

---

## 1 · Purpose

Take Layer C's build plan and turn it into one running, addressable, judged application —
and never claim more about it than can be evidenced.

The loop's own docstring states the method: *"generate, run, look, judge, fix — capped… the
whole thing is capped so a package that cannot be finished is *reported* rather than retried
forever"* (`builder/loop.py:1`).

Everything else in this layer exists to make that sentence true: the sandbox that runs the
code, the relay that writes it, the gates that judge it, the git history that keeps it, and
the job row that survives the process building it.

## 2 · Public surface

**Engine** (`apps/engine/src/scio_engine/main.py`)

| Endpoint | Does |
|---|---|
| `POST /build` | spec → running app, streamed as SSE (`main.py:350`) |
| `POST /build/promote` | deliver an existing design workspace *without* regenerating it (`main.py:407`) |
| `POST /workspace/discard` | delete a project's code and stop its preview (`main.py:449`) |
| `POST /estimate` | deterministic cost/time range — no model call |
| `GET /matrix/tasks` | what the relay is ranked to do |

**API** (NestJS, `modules/build/build.controller.ts`)

| Route | Does |
|---|---|
| `POST /projects/:id/build` | run a build, relay the engine's SSE unchanged |
| `DELETE /projects/:id/build` | stop the running build (a status transition) |
| `GET /projects/:id/build/job` | what is building right now |
| `GET /projects/:id/build/latest` | the reveal's payload, read back from storage |
| `GET /projects/:id/build/versions` | the version timeline |

**Frontend** — `BuildPage.tsx` (live per-part progress), `RevealPage.tsx` (the honest status).

**Internal, and used by every other layer:** `execution/relay.py` (`run_relay`,
`stream_relay`), `execution/provider.py` (`ProviderRegistry`), `execution/matrix.py`,
`execution/profile.py`. See §5 — this is not build machinery, it is the engine's model layer.

## 3 · In and out

**In** — an approved `AppSpec` (fresh build), or an existing workspace path (promotion).

**Out** — a stream of named events, and a workspace on disk with a git history.

```
started (BuildStarted)  → progress/package (per part) → [library] → finished (BuildFinished)
```

`BuildStarted` carries the real schedule — the package list and the count — *"so the build
view draws the real schedule instead of a spinner"* (`pipeline.py:52`). `BuildFinished` carries
the app URL, the git sha, the four status lists (working / needs-a-look / blocked / failed),
the remainders, the cost, the token count, the model that wrote it, the manifest, and every
route the app has.

Three things travel *with* the app rather than being remembered by a caller:

- **the manifest** (`id → package + source line`), derived from what is on disk;
- **the plan** (`.scio/plan.json`), because *"Layers B and C are model calls: run again they
  can produce a *different* plan, and the app on disk would then be measured against criteria
  it was never built to meet"* (`plan_store.py:1`);
- **the git history**, one commit per package build plus one for the assembled app.

## 4 · Invariants

### 4a · The gates — what a package must pass

```python
GATES = ("instrumentation", "validation", "console", "interaction", "critique")
```
`builder/loop.py:61`. Five per package, run cheapest-and-most-certain first, plus **one
app-wide gate** that is deliberately outside that tuple.

| # | Gate | What it actually checks | Where | Evidence |
|---|---|---|---|---|
| 1 | **Instrumentation verifier** | duplicate ids; source↔manifest both ways; every element names a *known* package; **both** attributes present, not just the id; loop patterns both ways; **ids lost since before this write**; nothing instrumented at all | `core/verifier.py:97` | `test_a_lost_id_fails_the_build`, `test_a_duplicate_id_fails`, `test_an_element_without_a_package_fails_the_verifier` |
| 2 | **Validation agents** (7, deterministic) | hardcoded secrets / `sk-…` / JWTs; `eval`, `dangerouslySetInnerHTML`, interpolated SQL; empty files; a test file exists for a package with operations; every planned file written and non-empty; each slice operation and screen present; **imports stay inside the package's declared dependencies**; no third-party web font | `builder/validation.py:404` | `test_the_exact_imports_the_real_run_invented_are_caught`, `test_a_missing_file_is_named_not_shrugged_at`, `test_an_imported_web_font_fails_the_package` |
| 3 | **Console classifier** | classifies each console line by *origin* before anyone judges it — browser noise (favicon), framework chatter, third-party host, or the app itself. Only app-origin errors and uncaught page errors fail | `core/console.py:186` | `test_the_favicon_404_the_spike_hit_does_not_fail_a_build`, `test_the_identical_message_from_an_app_route_does_fail`, `test_a_font_cdn_the_sandbox_cannot_reach_is_not_the_apps_fault` |
| 4 | **Interaction** — *does it work with real data* | drives the app in a real browser: fill → click → **real navigation** → assert on the page **and** in the database (`assert_row` through the app's own process) | `core/interaction_runner.py:28`, scripts derived in `layerc/scripts.py` | `test_a_correct_feature_passes_the_persistence_criterion`, `test_an_insert_that_silently_does_nothing_fails_it` |
| 4b | **Interaction** — *can a guest read another's row* | the same, twice, as two users (`as_user`), asserting each sees their **own** row and **not** the other's — *"because 'nobody can see anything' is not isolation, it is a broken list"* (`layerc/scripts.py:15`) | `layerc/scripts.py:189` | `test_a_guest_cannot_read_another_guests_booking`, `test_without_an_isolating_policy_it_fails` |
| 5 | **Critique** (the one model judgment) | per-criterion verdict against the package's *judgeable* acceptance criteria only, on fenced evidence | `builder/critique.py:208` | `test_an_unparseable_critique_is_never_a_pass`, `test_a_pass_with_an_unmet_criterion_is_rewritten_to_a_failure` |
| — | **App-wide typecheck** | the app's **own** `tsc --noEmit`, once, after everything is in place; errors blamed onto the owning package, unowned files blamed on the app | `builder/typecheck.py:79`, wired at `orchestrate.py:225` | `test_a_build_that_does_not_compile_does_not_say_it_works`, `test_the_part_that_owns_the_broken_file_is_the_part_named` |

The **order is an argument, not an accident**: *"a model asked to judge a page we already know
is broken costs a relay and tells us what a regex told us for free — and the same argument puts
the interaction channel ahead of it, because a browser round trip is cheaper than a relay and
answers the harder question"* (`loop.py:16`). The critique runs only when gates 1–4 are clean
(`loop.py:715`), and `test_the_critique_is_not_paid_for_when_the_app_does_not_work` pins it.

Four invariants hold across all of them:

| Invariant | Where | Test |
|---|---|---|
| A lost id fails the build **and the write is rolled back** | `loop.py:_attempt_package` → `_restore` | `test_a_regeneration_that_drops_an_id_is_rejected_and_rolled_back` |
| An unreadable verdict is a **failure**, never a pass | `critique.py:134` | `test_a_verdict_that_cannot_be_read_is_a_failure` |
| Nobody looked ≠ it passed — recorded as `unjudged` and carried into the reveal | `loop.py:696`, `typecheck.py:64` | `test_no_compiler_is_unjudged_and_never_a_pass`, `test_a_preview_that_cannot_drive_reports_it_rather_than_passing` |
| The app-wide gate can override a per-part "works" | `AppBuildResult.works` requires `not self.app_remainders` (`orchestrate.py:111`) | `test_a_build_that_does_not_compile_does_not_say_it_works` |

The typecheck's existence is documented as a confession: *"a build that had just reported
**"5 of 5 parts work"** shipped a `lib/db/booking.ts` importing `getSupabaseClient` from a
`lib/supabase.ts` that exports one boolean. Every existing gate passed it honestly… Every one
of those is per-package. The failure is *between* packages"* (`typecheck.py:1`).

**Two caveats, verified.** Gates 4 and 4b run only when `SCIO_VERIFY_DATA=1`
(`library/verification/__init__.py:62`); without the flag `preview.interact()` returns `None`
and the criteria are recorded as *"the app was not running with data, so nobody drove it"*
(`loop.py:523`). And `TestDrivenForReal` — the nine tests that prove gates 4/4b against a
real running app — **skipped in this environment**: *"a browser and node with
@electric-sql/pglite are both needed here."* I could not verify them here; the index records
the same environment gate.

### 4b · The money — how a model call is made, metered and capped

Every model call in the engine goes through one path: `run_relay(task, prompt, registry, options)`.

- **Which models**: `matrix.top_n(task, n=3)` off `execution/matrix.yaml` — data, not code.
  `plan_models` runs best-first, down the ranking, then **back to the best for the final pass**.
- **How many passes**: `MAX_PASSES = 4`, hard. `clamp_passes` enforces it (`relay.py:132`).
  The run profile (`SCIO_MODEL_PASSES`) is the user-facing knob, and `1` means *one model, run
  twice* — generate, then self-review (`profile.py:40`).
- **What a pass costs**: `_cost` prices **both halves** of the bill. The docstring records why
  that was not always true: *"a repair attempt re-sends every file it is fixing, so a codegen
  call routinely carries several times more input than it returns, and input was a third to a
  half of the real invoice. Every figure downstream… was quietly low"* (`relay.py:171`).
  Pinned by `test_a_pass_is_priced_on_its_input_as_well_as_its_output`.
- **Providers**: `ModelProvider` per vendor (Anthropic / OpenAI / Google), SDKs imported lazily,
  plus `FakeProvider` (deterministic digests) and `ScriptedProvider` (real text) for tests.

**Where the per-build ceiling is enforced — precisely.**

`Spend` is a mutable dataclass, one instance per build, shared by every call in it
(`relay.py:96`). The API computes it from the estimate the user actually approved against:

```
ceilingFor(spec) = spec.assumptions.estimate.cost_usd.high × 1.5   (build.service.ts:495)
```

*"A spec with no estimate gets none: a ceiling invented here would be a number nobody agreed
to."* It travels `build.service.ts:628 → EngineBuildRequest.budget_usd → pipeline.py:286
Spend(ceiling_usd=budget_usd) → BuildOptions.spend → RelayOptions.spend`, and is enforced at
**`relay.py:264`** — one place, for every codegen and every critique in the build.

The `Spend` docstring is a bug report against the previous design: *"Handing the same number to
every codegen and every critique therefore authorised it once per call — a seven-package build
makes at least fourteen, so a $3.76 'build ceiling' licensed something closer to $50."* Pinned
by `test_a_ceiling_reached_in_an_earlier_call_stops_a_later_one`.

Hitting it is not a defect: `BudgetExceeded` unwinds to `loop.py:_write_attempt`, becomes a
`Remainder` with `source="budget"` — *"stopped at the cost ceiling you approved"* — and the
loop **stops rather than retrying**, *"because a retry costs money it has already been told it
does not have"* (`loop.py:603`).

**A second, coarser ceiling** sits above it: a workspace's monthly allowance, checked before
the stream opens (`build.service.ts:222`, default $50 via `SCIO_WORKSPACE_PERIOD_CAP_USD`).
Its own docstring names why the per-build one is insufficient alone: *"it bounds one build and
says nothing about how many."*

**Metering.** Spend accumulates on the job row from every `package` event
(`build.service.ts:577`), and is written to `usage_event` on success (`persist`), on
cancellation and on failure (`meterSpend`, `build.service.ts:296`) — *"a cancellation that
quietly forgave the cost would be a hole, and an exploitable one."* Pinned by
`records the spend of a build that failed` and `keeps the running total on the job as the
parts finish`.

Cost containment is also structural, not only fiscal: codegen is chunked to fit
(`CHUNK_TOKEN_BUDGET = 11000`), a chunk that will not fit is **halved rather than re-asked**
— *"Eight files of real code do not become five files of real code because the prompt asked
nicely"* (`loop.py:222`) — and codegen gets a 900s timeout because the relay's 120s default
*"made every real pass time out — twice, silently"* (`loop.py:241`).

### 4c · Builds as jobs — ADR-0020, verified

ADR-0020's status says points 1, 4 and 5 are built and the queue and worker (2 and 3) are not.
**That is accurate.** Checked against the code:

| ADR-0020 point | Status | Evidence |
|---|---|---|
| 1. `build_job` row created before any work starts | **Built** | `openJob` at `build.service.ts:393`, called at `:550` *before* the engine call at `:628`. `BuildJob` model at `prisma/schema.prisma:229`. Test: `opens a job before any work starts` |
| 4. Cancellation is a status transition, checked between packages | **Built** | `cancel()` at `:247`; checked in `relay` at `:595` on every event; `BuildCancelled` closes the engine stream at a package boundary. Tests: `marks the live job cancelled`, `it("cannot stop another workspace's build")` |
| 5. Stale-heartbeat jobs are reaped | **Built** | `reapStaleJobs` at `:429`, 15-minute grace at `:382`. Test: `takes a job whose process died rather than locking the project forever` |
| 2. The engine takes a job id and reports against it | **NOT built** | `EngineBuildRequest` (`engine.client.ts:115`) carries `spec, project_id, build_version, max_attempts, shell_origin, budget_usd` — **no job id**. The engine has no concept of a job |
| 3. A worker takes jobs off a queue | **NOT built** | No `SELECT … FOR UPDATE SKIP LOCKED`, no broker, no worker process anywhere in the repo. `BuildJob.status` defaults to `"queued"` (schema:235) but `openJob` writes `"running"` directly (`:415`) — **the queued state is dead** |
| "The old project-status lock should be deleted when this lands" | **Still there, deliberately** | `refuseIfAlreadyBuilding` + `BUILD_LOCK_MS = 90 min` at `:175`/`:470`, kept for pre-jobs projects, exactly as the ADR says |

Consequence, exactly as the ADR states: the API still owns the forty-minute unit of work, and
streaming is a **live relay**, not a read of the job's event log — so a reconnect re-reads the
result rather than rejoining the build. Confirmed at `engine.client.ts:403`
(`streamEvents` reads the engine's response body straight through to `onEvent`).

### 4d · What the sandbox is allowed to be

- Generated code sees an **allow-list** of environment variables, not `os.environ`
  (`sandbox.py:105`). The comment names the incident it prevents: *"the child was started with
  `**os.environ`, which at that moment holds ANTHROPIC_API_KEY and SCIO_CATALOG_DB… an app that
  merely logged its own environment would have put the platform's key in a log the user can
  read."* Pinned across **every** provider by `test_no_provider_leaks_the_platforms_secrets`.
- Writes cannot escape the workspace (`_guard_path`, `sandbox.py:125`).
- A model-written `Dockerfile` never wins (`test_a_generated_dockerfile_never_wins`).
- Containers are bounded on memory, swap, CPU and PIDs, with `no-new-privileges`
  (`CONTAINER_LIMITS`, `sandbox.py:242`).
- `choose_sandbox()` **refuses to run** the non-isolating process provider when
  `SCIO_ENV=production` (`sandbox.py:406`).

## 5 · Dependencies

**Down:** `E → C` (68 edges) — the build executes Layer C's plan; `C → E` (39) — the plan
imports build primitives (`core.interaction` for scripts, `estimate` for sizing).

**Up:** `D → E` (84) — the library is consumed by the build; `F → E` (70) — the design window
drives builds; `A → E` (43).

**The `A → E` edges are not what the index guessed.** `00-INDEX.md` and `LAYER-A-INTAKE.md`
both attribute them partly to cost estimation. Verified: `grep -rn "estimate" intake/` returns
**nothing**, and `estimate.py` is imported only by `main.py`, `layerc/service.py` and
`builder/loop.py`. Every `A → E` edge is intake importing `execution.provider` /
`execution.relay` — the shared model machinery, not the builder.

### Is 41% proportionate?

Partly. Roughly a third of this layer is not build machinery at all — it is filed here because
of where the directories sit.

| Group | Lines | Who actually uses it |
|---|---:|---|
| `builder/` (loop, orchestrate, pipeline, codegen, validation, critique, typecheck, workspace, …) | 4,455 | Layer E — genuinely the build |
| `core/` (sandbox, verifier, console, instrumentation, manifest, stamping, interaction) | 2,491 | mostly E; parts shared with D and F |
| `execution/` (relay, provider, matrix, profile, narration, untrusted) | 1,037 | **A, B, C, D, E, F and `main.py`** |
| `api/modules/build` | 919 | Layer E |
| `api/engine` (`engine.client.ts`) | 491 | **every API module that talks to the engine** — intake, spec, design, build |

Three specific misfilings, each verified by import:

- **`execution/` (1,037 lines) is cross-cutting, not build.** It is the engine's model layer.
  Filed under G it would move ~4.5 points of the codebase out of E.
- **`core/resolver.py` (119) and `core/regenerate.py` (261) belong to Layer F.** Their only
  importers outside `core/` are `design/markings.py` and `design/change.py` respectively. Guardrail
  2 (*"a marking resolves exactly, or errors"*) is a design-window guarantee living in the build
  layer's directory. `builder/preview_bridge.py` (104) is the same story from the other side.
- **`engine.client.ts` (491) is not the build's client.** It carries intake, correction,
  architecture, plan, design change, design restore and workspace discard. It is the API's single
  door to the engine.

Adjusted, Layer E's own work is closer to **~7,400 lines (32%)** — still the largest layer, and
defensibly so: it holds a sandbox, a browser driver, a repair loop, seven validation agents, a
typechecker, git persistence, and a job lifecycle. But the headline 41% overstates it, and the
`A → E`, `C → E` and `F → E` edge counts are largely an artifact of the same filing.

One thing genuinely *is* in the wrong place and is not a filing question:
**`builder/standin.py` (315 lines)** is test scaffolding shipped in `src/`. It is honest about
itself — *"It is NOT a model and its output is NOT real app code"* — and it is load-bearing for
the key-less path, but it is 3% of the layer.

## 6 · State

### Solid — carry forward unchanged

- **The instrumentation guardrail.** `verify_instrumentation` with `expected_ids` is the single
  hardest-won thing here, and the only gate that triggers a **rollback**. Its rationale is a
  measured incident, not a theory: *"losing an id does not fail loudly on its own: the app still
  renders, the click still resolves, and it resolves to the wrong package"* (`verifier.py:1`).
- **Package stamping.** `data-scio-package` is written by the builder, not requested from the
  model — *"the model supplies the thing only it can… and the builder supplies the thing it
  already knows"* (`stamping.py:1`). This removes a whole class of model non-compliance from
  the trust chain.
- **The console classifier.** Small, auditable, and it publishes what it suppressed
  (`ConsoleReport.suppressed`) *"so the filter stays auditable rather than becoming a place
  failures go to hide."*
- **`Spend` as a build-scoped accumulator.** One object, one enforcement point, correct unit.
- **The honest-status vocabulary.** `passed / needs_look / failed / blocked`, `Remainder`,
  `app_remainders`, `app_unjudged` — and `works` requiring *both* every part and nothing
  app-wide. This is the layer's product promise, expressed in types.
- **Promotion.** `stream_promotion` regenerates nothing and refuses rather than falling back:
  *"Never silently fall back to a rebuild: that is the data loss this exists to prevent, and it
  would be invisible to the person it happens to"* (`pipeline.py:386`).
- **The untrusted-text fence.** `execution/untrusted.py` is honest about being the cheap half —
  *"the layer that matters most is not this file"* — and the expensive half (unparseable verdict
  = failure; "pass" with unmet criteria rewritten to failure) is real and tested.
- **Sandbox environment hygiene**, proved once for every provider by a conformance suite whose
  own docstring explains why: *"An abstract method whose contract one implementation ignores is
  worse than no abstraction: every caller is written against the promise."*

### Deliberate, and easy to break by accident

**Cheap-and-certain first.** Instrumentation (free) → validation (free) → console (a page load)
→ interaction (a browser round trip) → critique (a relay). Reordering this — or making the
critique run unconditionally — silently multiplies build cost with no gain in signal. The
argument is written down in `loop.py:16`; any change to it needs to answer that argument.

**Deterministic where determinism is possible.** The interaction scripts are *derived from the
architecture*, not authored by a model: *"asking a model to invent the steps would make the one
criterion that gates the build the least reproducible thing in the pipeline"*
(`layerc/scripts.py:1`). `test_derivation_is_stable_across_runs` pins it. Likewise the file
plan, the manifest and the package stamp.

**A truncated reply writes nothing.** *"Writing what arrived would put half a component on
disk"* (`loop.py:614`). And a chunk that will not fit is split, never re-asked at the same size
— `test_a_chunk_that_will_not_fit_is_halved_not_repeated`.

**Assembled parts are judged on a shorter gate set** (`ASSEMBLY_GATES`), because holding a
curated library part to *this* app's operation names produced a preview saying "5 of 5 parts
work" and a delivery of the same files saying "4 of 5" (`loop.py:970`). Removing this
distinction reintroduces that.

### Wrong-shaped

- **The ceiling is checked *after* the call it should have stopped.** `relay.py:256` runs the
  completion, `:259` prices it, `:264` raises. The vendor has already billed those tokens. The
  overshoot is bounded (one pass) but it is **unrecorded**: the raise skips `spend.add(cost)`
  *and* discards the whole `RelayResult`, so `_write_attempt` returns `cost_usd=0.0` and the
  package event carries none of that call's spend — including passes 1..k-1 that *did* complete.
  The ledger therefore under-reports precisely the build that hit its ceiling. `Spend`'s own
  docstring says *"checked before each one"*, which the code does not do.
- **The reported build cost is not the build's cost.** `AppBuildResult.total_cost_usd` sums
  package results only (`orchestrate.py:434`). Layer B's narrative relay (`layerb/whole.py:133`,
  up to 2 passes), Layer C's grouping judgment (`layerc/judgment.py:92`) and the library
  contribution (`library/contribute.py`) all run inside `stream_full_build` and **track no cost
  at all** — `grep -n cost layerb/service.py layerb/whole.py layerc/service.py` returns nothing
  about spend. Those calls are also outside the ceiling: `run_layer_b` and `run_layer_c` take
  no `spend` parameter. This is coherent with the *estimate* (which also prices packages only),
  so the ceiling is not wrong relative to what the user approved — but the ledger and the
  reveal both understate what the workspace really spent.
- **The interaction gates — the two most valuable checks in the layer — are off by default.**
  Everything that makes "it works" mean *saved to a database* and "it is private" mean *RLS
  actually isolates* hangs on `SCIO_VERIFY_DATA=1`. Without it those criteria come back as
  "nobody drove it", which is honest but means the flagship gate is opt-in. The runbook
  documents this plainly, so it is a shape problem, not a drift problem.
- **`checks_passed` is computed, typed, transmitted and never shown.** `GATES`' docstring
  claims *"`checks_passed/len(GATES)` is what the reveal shows, so the count is a real count
  and not a number chosen to look reassuring"* — but the field appears in
  `packages/shared/src/intake.ts:287` and in **no** `.tsx` file. The reveal shows the four
  status lists instead. Either wire it or stop claiming it.
- **The API owns a forty-minute unit of work.** ADR-0020's own consequence section: *"the
  current design does not survive a deploy."* Everything downstream of that — resume, admission
  control, rejoining a stream — is shaped around a stack frame.
- **`AcaSandbox.start` does not match its own interface.** `SandboxProvider.start(app_dir, *,
  port, env)` vs `AcaSandbox.start(app_dir, *, port)` (`aca_sandbox.py:63`). It would `TypeError`
  on the first call the builder makes. It is also excluded from `test_sandbox_conformance`'s
  `PROVIDERS` list — the suite written specifically to stop this.

### Missing

- **Nothing runs the generated app's tests.** `check_tests_present` verifies a test file
  *exists* and is non-empty (`validation.py:123`); no gate executes it. `grep -rn
  "vitest\|jest\|npm test"` across the engine returns nothing. A generated app can ship a
  test file that fails.
- **Nothing runs `next build`.** The typecheck gate runs `tsc --noEmit`; the sandbox runs
  `next dev`. A production build failure (a route that only breaks under static analysis, a
  bad `generateStaticParams`) is never seen.
- **No prompt caching.** `grep -rn "cache_control"` returns nothing. `STRATEGY.md` §G lists it
  under **"Adopt now (clear wins, low risk)"** and calls it *"our single biggest cost lever…
  Use it on the STATIC prefix of every build-package prompt."* The static prefix exists (the
  playbook, house rules, architecture slice) and is re-sent on every call.
- **No Batch API**, likewise listed under "Adopt now". `BACKLOG.md:18` reframes it as a
  product call (it trades the live progress the build screen is built on), which is a fair
  answer — but the strategy doc still says adopt.
- **No rate-limit handling.** `_complete_with_retry` retries once with a 0.2s linear sleep and
  has no 429 branch (`relay.py:187`). `grep -rn "429\|rate_limit"` returns nothing. A real
  seven-package build makes dozens of large calls.
- **No parallelism.** `orchestrate.py:19`: *"MVP is sequential. `parallelizable` is already
  recorded on the packages by Layer C; a scheduler is a later optimisation."* True, and the
  cost is wall-clock: the slowest measured build was 46 minutes (`build.service.ts:172`).
- **No Supabase project is ever provisioned.** ADR-0011 makes Supabase the generated app's
  backend, and the scaffold pins `@supabase/supabase-js` (`workspace.py:58`) and writes
  `supabase/migrations/`. Nothing in the engine or the API creates a project, applies the
  migrations to a real instance, or provides keys — `grep -rn supabase apps/api/src` returns
  **nothing**. Verified apps run against pglite; delivered apps get a client pointing at an
  unset `NEXT_PUBLIC_SUPABASE_URL`.
- **No network policy on the sandbox.** Named honestly in the code itself: *"Not a network
  policy: the preview has to reach npm and the verification database… That is a real remaining
  gap"* (`sandbox.py:267`, B118).
- **No isolating production sandbox.** ADR-0005's provider is three `raise SandboxError("…not
  implemented")` methods and `choose_sandbox()` never returns one. Mitigated, not solved: the
  process provider refuses to run under `SCIO_ENV=production`, so the failure mode is *cannot
  serve*, not *serves unsafely*.
- **No observability.** No build id in logs, no metrics, no aggregation of honest statuses.
  `BACKLOG.md:36` (B123) names it and correctly ties it to the job.

### Obsolete

- **`RelayOptions.budget_usd` / `BuildOptions.budget_usd`.** Superseded by `Spend`. In the
  production path `BuildOptions.budget_usd` is never set — `grep -rn "budget_usd="` shows the
  only assignments are `main.py` (→ `Spend`), `loop.py` (reading the unset field) and **two
  tests**. It survives as a footgun with a warning label: *"A ceiling on ONE relay call. Rarely
  what you want."*
- **`clamp_passes(requested, available_models)`** ignores `available_models` entirely
  (`relay.py:132`). Dead parameter, still in the signature and still passed.
- **Three of seven matrix task rankings are never used.** `matrix.yaml` defines `fix`, `design`
  and `light_edit`; the only tasks any `run_relay` call site passes are `spec_extraction`,
  `architecture`, `codegen` and `review`. Notably the repair path calls `run_relay("codegen",
  fix_prompt(...))` (`loop.py:401`) while a `fix` ranking sits unused.
- **`BuildJob.status = "queued"`** is a schema default that no code path can produce.

## 7 · Open questions

**a. Does the queue land, or does the API keep the long work?** ADR-0020 is explicit that
points 1–5 are not separable — *"Restart-safety, cancellation and admission control all follow
from (1) and (3)"* — and calls the queue *"the largest single piece of work left in the
backlog… a prerequisite for anything resembling production traffic."* Everything in §6's
Missing list about resume, admission control and observability is downstream of this one
decision. It needs the planning chat, not an engineer.

**b. Should `SCIO_VERIFY_DATA` become the default?** It is what makes "5 of 5 parts work" mean
something, and it costs a pglite boot, a browser round trip per feature and ~40MB. The
argument for opt-in is speed; the argument against is that the product's whole claim is that
the status is honest. This is a product call with a measurable cost.

**c. Where does `execution/` live?** It is the engine's model layer, used by six of seven
layers. Leaving it under "build" is why every layer appears to depend on the build. Moving it
is a directory change, not a redesign — but it changes what the layer map means.

**d. What is the production sandbox?** ADR-0005 chose ACA dynamic sessions in August 2026,
noting it was in preview and flagging four open questions (prewarm latency, concurrency limits,
cost per session-hour, whether Playwright runs inside the session). None of the four has been
answered, and the implementation has never run. Re-decide or re-affirm before the deploy;
either way ADR-0005 needs a status that says so.

**e. Does the generated app get a real backend?** ADR-0011's Supabase choice is what makes the
"secure-by-default, minimal LLM-generated security code" argument work. Until provisioning
exists, a delivered app is code the user owns with nothing behind it. That is a scope question
about what "delivered" means, and it belongs beside ADR-0018 (what Publish is).

---

## Documentation drift found

**1. `docs/STRATEGY.md` §A is stale in three places** (last touched 2026-08-19; the code moved
on 2026-08-22):

> 4. **Review screen**… The cost calculation is unresolved. `[gap]`

`estimate.py` exists, is calibrated against three real runs, is exposed at `POST /estimate`,
is frozen onto the spec at approval, and is the source of the build's spend ceiling
(`build.service.ts:497`). `tests/test_estimate.py` asserts the range still contains the one
real invoice.

> 6. **Build (package-by-package + vision loop).** Built (fake-driven).

Not fake-driven. The layer's largest test file is named for what a real model did:
`test_b054_real_run_hardening.py` — *"The three defects the first real build against Claude
exposed."* `matrix.yaml` and `file_plan.py` both carry comments about *"the second real run"*.
`validation.py:336` records a measured 12.7-second font stall from a real sandbox.

> 7. **Build view**… the live tick-off + the time estimate aren't wired.

Wired. `BuildProgress` → SSE → `BuildPage.tsx:102` renders `"{done} of {total} parts done"`,
and its own comment says *"there is no timer and no fake bar."*

**2. `docs/STRATEGY.md` §G lists prompt caching and the Batch API under "Adopt now (clear wins,
low risk)".** Neither is adopted: `grep -rn "cache_control\|ephemeral"` over the engine returns
nothing, and `BACKLOG.md:18` has since reclassified Batch as an open product call. §G should be
read as a 2026-08-19 evaluation, not a statement of what is in.

**3. ADR-0005 carries no implementation status.** Its status is *"Accepted (with a spike;
feature is in preview)"* and it reads as decided. The code it describes has never executed —
`aca_sandbox.py:3` says so in a warning banner (*"⚠️ NOT RUN HERE… treat every line as
unverified"*), and `BACKLOG.md:27` (B122) says so plainly. The ADR itself does not. Anyone
reading the decisions folder alone would conclude Scio has an isolating production sandbox.

**4. In-code drift, three instances, each small and each a claim about behaviour:**

- `builder/loop.py:61` — *"`checks_passed/len(GATES)` is what the reveal shows"*. It is not
  shown anywhere in `apps/app/src`.
- `execution/relay.py:107` — `Spend` is *"incremented by every call, checked before each one"*.
  It is checked after the call that crosses it (§6, Wrong-shaped).
- `library/assembler.py:40` — ASSEMBLY_GATES are *"Fewer than a generated package's four"*.
  `GATES` has five.

**5. This repository's own `00-INDEX.md` and `LAYER-A-INTAKE.md`** both explain the 43 `A → E`
edges as *"cost estimation and the shared relay/provider machinery."* The cost-estimation half
is wrong: `grep -rn "estimate" apps/engine/src/scio_engine/intake/` returns nothing, and
`estimate.py` has exactly three importers, none of them in intake. Every `A → E` edge is
`execution.provider` / `execution.relay`.

*Verified 2026-08-26 against the code. Layer E tests run here: 247 passed, 9 skipped across
`test_core_guardrails` (30), `test_b054_real_run_hardening` (37), `test_interaction_channel`
(36 — 9 skipped, needing a browser and pglite), `test_builder_orchestrate` (21),
`test_relay` (21), `test_builder_pipeline` (18), `test_builder_loop` (16),
`test_builder_workspace` (16), `test_run_profile` (14), `test_matrix` (11),
`test_prompt_injection` (10), `test_typecheck_gate` (7), `test_sandbox_conformance` (6),
`test_preview_without_playwright` (6); plus `apps/api/test/build.e2e.spec.ts` — 44 passed.*
