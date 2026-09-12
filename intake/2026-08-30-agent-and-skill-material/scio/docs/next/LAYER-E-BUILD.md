# Layer E · Build & execution — what to build next

Forward-looking. `docs/as-built/LAYER-E-BUILD.md` is the starting point; this is what to do
with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method note.** Layer E is where the money and the risk are, so every domain it touches was
scanned before anything was proposed: sandbox isolation primitives, egress policy, agentic repair
loops and their measured returns, execution-based versus execution-free verification, test-oracle
quality, prompt-caching and batch economics, build observability conventions, build provenance
formats, and what the competitors ship. The rule this family runs on holds here too: **where a
standard, a published algorithm or a measured result already covers something, cite and adopt
it.** Five things this layer would otherwise have decided by argument already have evidence
attached — the repair-loop cap, the value of the relay's extra passes, whether running generated
tests is worth it, what a network policy for a build sandbox looks like, and what a gate result
should be called on the wire.

Everything measured below was run against the working tree on **2026-08-26** with
`apps/engine/.venv/bin/python` at `00408d3`. Token figures are characters ÷ 4 and are marked as
such — `messages.count_tokens` is the correct instrument and no API key was available here, so
re-measure before acting on any margin narrower than 20%. Research was read at
abstract-to-method level; nothing was reproduced.

---

## 1 · Where Layer E stands

`BuildPlan → running app + honest status`. Packages in dependency order into one growing
workspace; five gates per package, cheapest-and-most-certain first; one app-wide typecheck; git
history; a job row; an SSE stream. 42 files, ~9,400 lines — and the as-built is right that roughly
a third of that is filed here by directory rather than by function.

**Solid and not to be touched:** the instrumentation guardrail (`core/verifier.py:1`) — the only
gate that rolls back, written from a measured incident, and the reason the marking→code map can be
trusted; package stamping (`core/stamping.py:1`), which removes a whole class of model
non-compliance from the trust chain; the console classifier, which publishes what it suppressed;
the gate ordering argument at `loop.py:16`, which §2.3 shows the 2026 literature arrived at
independently; `Spend` as a build-scoped accumulator — one object, one enforcement point, correct
unit; the honest-status vocabulary, and `works` requiring *both* every part and nothing app-wide;
promotion refusing rather than falling back (`pipeline.py:386`); and the sandbox environment
allow-list with its conformance suite (`sandbox.py:105`).

The constraint that governs every proposal below, from the loop's own docstring:

> generate, run, look, judge, fix — capped… the whole thing is capped so a package that cannot
> be finished is *reported* rather than retried forever.

**Any change that makes a failure quieter, or lets a model's opinion stand in for a
deterministic check, is out of scope.** Proposals may add evidence channels; they may not
convert an existing deterministic one into a judgment.

### 1.1 Nine corrections to the as-built record

The as-built pass is accurate on structure. Nine things are wrong or understated, and four of
them change a conclusion.

**(a) `test_interaction_channel.py` does not have 36 passing tests.** It has 36 test functions;
run here it is **27 passed, 9 skipped in 0.26s**. The nine that skip are `:868`–`:957`, every
one of them marked *"a browser and node with @electric-sql/pglite are both needed here"* — that
is, the nine that would drive a real app are exactly the nine that do not run. The 27 that pass
test the *derivation* of scripts from a hand-built `Architecture` whose fixture
(`tests/test_interaction_channel.py:117-125`) writes typed operation inputs — `guest_name: text`,
`party_size: integer` — that Layer B never produces (§1.2). Both halves of the suite are green
for reasons unrelated to whether the gate works on a real build.

**(b) The interaction channel is empty on real Layer B output — confirmed on a second fixture.**
Layer C §1.1 found this on a six-package spec. Re-run here through
`derive_architecture(make_booking_spec()) → build_plan`, five packages:

| observed_by | criteria |
|---|---:|
| `validation` | 12 |
| `render` | 6 |
| `unsupported` | 5 |
| **`interaction`** | **0** |

Zero on both fixtures. The other three counts are fixture-dependent and should always be quoted
with the fixture named; the zero is not. Layer E's two most valuable gates are opt-in *and*
have nothing to check.

**(c) The spend-ceiling defect loses more than one pass, and the loss lands in the ledger the
user is billed against.** Verified at source. `relay.py:256` runs the completion, `:259` prices
it, `:264-268` raises, `:273` — the `spend.add(cost)` — is never reached. So:

- **lost from `Spend`:** exactly the crossing pass's cost. Bounded, as the as-built says.
- **lost from the reported ledger:** the entire `_generate` call. `BudgetExceeded` propagates
  out of `run_relay` → `_generate_chunk` → `_generate`, whose local `total_cost` accumulator
  (`loop.py:427`) dies with it, and `_write_attempt`'s budget branch (`loop.py:592-609`)
  constructs `_Written(...)` **with no `cost_usd`**, which defaults to `0.0` (`loop.py:550`).
  On a chunked feature package that discards every completed pass of every completed chunk —
  up to eight relay passes of real, paid-for work.

That zero then travels: `Attempt.cost_usd` → `PackageBuildResult.total_cost_usd` → the `package`
SSE event → `spentUsd += Number(data.total_cost_usd ?? 0)` (`build.service.ts:577`) →
`usage_event`. **The build that hit its ceiling is the one the ledger under-reports most.**

**(d) `Spend.spent_usd` — the only correct running total in the system — is never read.** Four
references repo-wide, all inside `relay.py`, one of them a string interpolation in the error
message. `AppBuildResult.total_cost_usd` recomputes the total from package results
(`orchestrate.py:434`), which is the lossy path from (c). One field on `AppBuildResult` would
fix the ledger. This is the system-wide pattern — an honest signal computed and dropped —
inside the layer that owns the money.

**(e) `estimate_plan` prices output only, and the spend ceiling inherits that.**
`cost_usd = tokens / 1_000_000 * card.cost_per_mtok` (`estimate.py`, in `estimate_plan`);
`input_cost_per_mtok` is read nowhere in that file, while `_cost` (`relay.py:169-180`) prices
both halves and its docstring says input was *"a third to a half of the real invoice"*. The
estimate is frozen onto the spec at approval, and `ceilingFor` is `estimate.cost_usd.high × 1.5`
(`build.service.ts:495-501`). So the number the user approves, the range they are shown, and the
ceiling that stops their build are all built on a model that ignores a third to a half of the
bill. `HIGH_MULTIPLIER = 2.6` may still cover it; the calibration that says so was taken when
`_cost` also priced output only, so the ratio it was tuned against is not the ratio that now
obtains.

**(f) Nobody has written down what the shipped default costs.** `_setting_from_env` returns
`MAX_SETTING = 4` when `SCIO_MODEL_PASSES` is unset (`profile.py:108-113`), so the default is
the full ranked matrix at four passes. Measured on the canonical booking plan:

```
$2.44–$9.07 · 16–61 min · 5 parts · all built   (claude-opus-5, 4 passes)
```

Ceiling: **$13.61**. The as-built quotes $1.42 and $2.69 — both from real runs at
`SCIO_MODEL_PASSES=1` on Sonnet. Nobody has priced what ships.

**(g) "Nothing runs the generated app's tests" understates it — nothing could.**
`DEV_DEPENDENCIES` (`workspace.py:66-77`) contains no test runner: no vitest, no jest, no
`@testing-library`, no playwright. `package_json` (`:103-123`) has `dev`, `build`, `start`,
`lint` and no `test` script. And `check_tests_present` (`validation.py:132`) matches
`"test" in p.lower() or "spec" in p.lower()` — so `app/latest/page.tsx` satisfies the check that
a package has a test. Meanwhile `pkg_foundation`'s interface advertises `"test runner"` to every
dependent package (`decompose.py:73`, Layer C §2.3). Three layers promising a thing that is not
installed.

**(h) G-F04 is live, verified statically here, and worse than the review recorded.** The reviews
document marked this *"taken on the brief's word, not re-checked"*. Checked now:

1. the engine emits `": keep-alive\n\n"` every `KEEPALIVE_SECONDS = 15.0` during silence
   (`main.py:696, :722`);
2. `parseFrame` accumulates only `data: ` lines and returns `null` when `raw` is empty
   (`engine.client.ts:200-213`) — a comment frame is dropped, correctly, as unreadable;
3. `streamEvents` calls `onEvent` only for non-null frames (`engine.client.ts:435-437`);
4. `heartbeatAt` is written **only** inside `relay()` (`build.service.ts:587`), i.e. only on a
   real event;
5. `HEARTBEAT_GRACE_MS = 15 * 60 * 1000` (`:382`), and `reapStaleJobs` (`:429`) is called from
   `:205`, `:269` and `:399` — request-triggered, and the app polls `/projects/:id/build/job`
   (`api.ts:196`).

So the screen that shows progress is what fires the reaper. And one codegen relay **pass** may
take `CODEGEN_TIMEOUT_S = 900.0` (`loop.py:241`) with `codegen_passes = 4` (`loop.py:252`): a
single package may legitimately be silent for **up to 60 minutes, four times the grace**.

The consequence is worse than a wrong status. `reapStaleJobs` sets `status: "failed"`; the
in-flight cancel check reads `job?.status === "cancelled"` (`:451-454`). A reaped job therefore
does **not** stop the engine. The user is told the build stopped reporting, and the build keeps
running and keeps spending against a job row that has already been closed.

**(i) F-03 is Layer G's to fix, but the reason the tests cannot see it lives here.**
`BuildService.run` replays on the idempotency key at `:518-522` — `buildVersion.findFirst({ where:
{ projectId, idempotencyKey } })` and `emit("finished", ...)` — *before* `this.project(workspaceId,
projectId)` at `:525`. `WORKSPACE_SCOPED_MODELS` (`auth/workspace-scope.ts:13-22`) holds six
names — `Project`, `UsageEvent`, `Notification`, `AuditLog`, `User`, `BuildJob` — out of 14
models in `schema.prisma`. **`BuildVersion` is not one of them**, and carries no `workspace_id`
column. The only thing between a caller and another tenant's finished-build payload is knowing
`(projectId, idempotencyKey)`.

The 44 build e2e tests cannot catch this, and the reason is precise:
`FakeScope.buildVersion.findFirst` calls `owns(where.projectId)` before returning
(`test/build.e2e.spec.ts:105-108`). **The double is stricter than the thing it doubles.** That is
the third confirmed instance in this repository of a suite passing for the wrong reason, after
`test_interaction_channel.py` (§1.1a) and the Layer C seam it sits on. Worth naming as a class,
because the fix is a policy — *a double must be provably no stricter than production, proved by
running the same conformance suite against both* — which is exactly what
`test_sandbox_conformance` does for `SandboxProvider`, and what §2.5 shows it stopped doing for
one provider.

---

## 2 · Refining what exists

### 2.1 The relay's four passes are intrinsic self-correction, and that is the largest cost lever in the system

`stream_relay` runs `passes` model calls in sequence. `_build_messages` (`relay.py:148-167`)
gives pass *n* exactly two things: the original prompt and pass *n−1*'s answer, prefixed by
`REVIEW_INSTRUCTION` or `FINAL_INSTRUCTION`. **No gate output. No compiler. No browser. No test.
No external signal of any kind.** The build's real feedback — validation findings, console errors,
interaction failures, typecheck errors — enters through a different door entirely:
`_write_attempt`'s `problems` list, on the *next attempt*, capped at `max_attempts = 3`.

Scio runs two loops and spends its money on the wrong one:

| Loop | Feedback | Cap | Default |
|---|---|---:|---|
| relay passes | none — the model's own previous answer | `MAX_PASSES = 4` | **4** |
| repair attempts | seven validation agents, console classifier, interaction runner, critique | `max_attempts` | 3 |

The literature on which of these works is unusually clear, and it is not new:

- Huang, Chen, Mishra, Zheng, Yu, Song & Zhou, [*Large Language Models Cannot Self-Correct
  Reasoning Yet*, ICLR 2024](https://arxiv.org/abs/2310.01798) — *"LLMs struggle to self-correct
  their responses without external feedback, and at times, their performance even degrades after
  self-correction."*
- Kamoi, Zhang, Zhang, Han & Zhang, [*When Can LLMs Actually Correct Their Own Mistakes? A
  Critical Survey*, TACL 2024](https://arxiv.org/abs/2406.01297) — three findings, and the middle
  one is the design rule: *"no prior work demonstrates successful self-correction with feedback
  from prompted LLMs"*; *"self-correction works well in tasks that can use reliable external
  feedback"*.
- Kiecker, Reichmann, Kang, An & Grunske, [*Is Three the Magic Number? An Empirical Evaluation of
  LLM-Based Repair Loops*, July 2026](https://arxiv.org/html/2607.05197v1) — 0–10 repair steps
  across six tool/dataset combinations; the first 3–4 iterations capture the vast majority of the
  achievable gain, and by step 3 the increment is *"single digit percentages or below"*. The
  answer to the title is yes.

**`max_attempts = 3` is exactly right and now has a citation. `codegen_passes = 4` is the one
without evidence behind it**, and it is a straight 4× multiplier on the most expensive call in
the build.

The honest complications, both of which belong in the ADR:

1. **Scio's passes are not strictly *self*-correction.** `plan_models` walks the matrix ranking,
   so pass 2 and 3 may be different models (`matrix.yaml` ranks `codegen` as Opus 5 → Sonnet 5 →
   GPT-5). Cross-model review is a different and better-supported thing than a model reviewing
   itself. The surveys above measure self-correction; they do not measure a three-vendor relay.
   **That is a hypothesis, and it is measurable** — the whole point of the profile knob.
2. **The two-pass floor is deliberate and should stay.** `relay_passes(1) → 2` because
   `plan_models` puts the best model first and last, so "one model, generate then self-review"
   is the minimum the product's own language promises (`profile.py:40-49`).

The proposal is therefore not "turn passes off". It is: **default the shipped profile to
`SCIO_MODEL_PASSES=1` (two relay passes), spend the difference on the loop that has feedback,
and settle the question with a measurement rather than a preference.** By the estimate's own
arithmetic — `expected_output_tokens(package) * passes` — that halves the canonical app's
default estimate from $2.44–$9.07 to roughly $1.22–$4.54, and the three real runs the estimate is
calibrated against were all taken at that setting.

### 2.2 The ceiling is checked after the call, and two different fixes are needed

`Spend`'s docstring claims it is *"incremented by every call, checked before each one"*. It is
checked after (§1.1c). Two fixes, and doing either alone leaves half the defect:

| Fix | What it closes | Cost of being wrong |
|---|---|---|
| **Check before.** `messages.count_tokens` on the assembled prompt, plus `max_tokens` × the card's output rate, gives a hard upper bound on the call. Refuse if that bound crosses the ceiling | the overshoot — the vendor is never billed for a call the ceiling would have stopped | over-refusal: a call whose real output is short is blocked by its worst case. Mitigable by pricing the bound at, say, the observed output ratio rather than `max_tokens` |
| **Preserve the partial.** Attach the accumulated cost to `BudgetExceeded` and record it in `_write_attempt`'s budget branch | the ledger — the user is billed for what was actually spent | none; it is strictly more honest than `0.0` |

`count_tokens` is the correct instrument and it is free of charge on the Messages API. It also
gives Layer E the input-side prediction `estimate.py`'s docstring says it needs and *"needs a
real run to calibrate against rather than a coefficient invented here (B115)"* — except it does
not need a real run, because the prompt is fully assembled before the call.

### 2.3 The gate order is right, and the 2026 evidence says so — do not reorder it

Worth recording rather than changing, because `loop.py:16`'s argument is now supported from
outside. Lin, Zhu, Zhou, Wang, Sun, Yang, Lo & Li, [*To Run or Not to Run: Analyzing the
Cost-Effectiveness of Code Execution in LLM-Based Program Repair*, ISSTA
2026](https://arxiv.org/html/2606.26978) prohibits execution for a repair agent and measures the
difference: a resolve-rate gap of **1.25pp** on commercial agents and ≈0pp on open-source models,
neither significant, while prohibiting execution **saves 56–62% of tokens and 48–54% of
wall-clock** for Claude Code; localisation stays above 95% either way. That is *"a model asked to
judge a page we already know is broken costs a relay and tells us what a regex told us for free"*
from the other direction. Its limits matter equally: the paper is scoped to SWE-bench-style
repository bug fixing, where a test suite exists, and says its findings may not generalise to
tasks needing dynamic analysis — which is exactly what *"did the row reach the database"* is. The
ordering transfers; the conclusion "do not execute" does not.

### 2.4 `check_tests_present` checks a substring, and there is nothing behind it

Three separate defects stacked (§1.1g), and they should be fixed in this order, because each one
makes the next meaningful:

1. **the substring.** `"test" in path.lower()` matches `latest`, `greatest`, `contest`. Match on
   a real convention — `*.test.ts`, `*.test.tsx`, `*.spec.ts`, or a `__tests__/` segment.
2. **the runner.** Add vitest (or the runner ADR-0011 chooses) to `DEV_DEPENDENCIES` and a `test`
   script to `package_json`, so the promise `pkg_foundation` already makes to every dependent
   package (`decompose.py:73`) is true.
3. **running them** — §3.1, which is a design question, not a patch.

### 2.5 `AcaSandbox` does not implement its own interface, and the suite written to prevent that excludes it

`SandboxProvider.start(app_dir, *, port=0, env=None)` (`sandbox.py:43-53`) versus
`AcaSandbox.start(app_dir, *, port=0)` (`aca_sandbox.py:63`). It would `TypeError` on the first
call the builder makes, before reaching the `raise SandboxError("… not implemented")` one line
below. And it is absent from `test_sandbox_conformance`'s provider list — the suite whose own
docstring says *"An abstract method whose contract one implementation ignores is worse than no
abstraction."*

Adding it to that list is one line, and the test will fail. **That is the correct outcome**: it
converts a latent runtime error into a red test, which is what the suite is for. This is the same
policy §1.1i argues for on the API side.

### 2.6 Three matrix rankings are unused, and one of them is the repair path

`matrix.yaml` ranks seven tasks. `run_relay` is called with four: `spec_extraction`,
`architecture`, `codegen`, `review`. `fix`, `design` and `light_edit` are never routed to — while
the repair path calls `run_relay("codegen", fix_prompt(...))` (`loop.py:401`) with a `fix`
ranking sitting unused directly above it.

This is not tidiness. A repair is a different task with a different shape: the input is large
(every file in the package, verbatim) and the output is small (the files that changed). Routing it
as `codegen` prices it, ranks it and caps it as if it were a first draft. Whether the `fix`
ranking should differ from `codegen` is a measurement (§8); that the code cannot express the
difference is a defect.

Two smaller ones in the same family: `clamp_passes(requested, available_models)` ignores its
second argument entirely (`relay.py:132-136`), and `RelayOptions.budget_usd` /
`BuildOptions.budget_usd` are superseded by `Spend` and survive as a footgun with a warning
label. `BuildJob.status = "queued"` is a schema default no code path can produce
(`schema.prisma:235` vs `openJob` writing `"running"` at `build.service.ts:415`) — it becomes
reachable when, and only when, ADR-0020's queue lands.

### 2.7 Rate limiting: the as-built is half right, and the half it misses matters

`grep -rn "429\|rate_limit"` over the engine returns nothing, which is true. But
`AnthropicProvider._complete` constructs `AsyncAnthropic(api_key=..., timeout=timeout_s)`
(`provider.py:169`) without overriding `max_retries`, and the SDK's default is **2 retries on
408/409/429/5xx with `Retry-After` honoured**. The Anthropic path does have rate-limit handling;
it is inherited, invisible and untested. What is genuinely absent is the same guarantee for the
OpenAI and Google providers — which the matrix ranks second and third for `codegen` and **first**
for `review` — any surfacing of a 429 into the narration, so throttled looks identical to slow,
and admission control, which is what ADR-0020's queue exists to provide. The engine's own
`_complete_with_retry` (one retry, `0.2 × (attempt+1)` linear sleep) then sits *on top* of the
SDK's, so a hard 429 costs up to six attempts with no jitter. Say what the layer relies on, or
stop relying on it.

---

## 3 · What is missing

### 3.1 Nothing runs the generated app's tests or `next build` — and the two are not the same proposal

`PRODUCTION_READINESS_DIFF.md` §7 requires unit, component, integration **and** browser tests,
and requires central flows to have been run in a browser. Layer E has the browser half, opt-in
(§3.2), and none of the rest. But "run the tests" and "run the build" have opposite evidence
profiles, and collapsing them is how this gets built wrong.

**`next build` is a deterministic gate with no oracle problem. Add it first.** The typecheck gate
runs the app's own `tsc --noEmit`; the sandbox runs `next dev`. Neither is a production build.
Next.js runs type checking as the first step of `next build` and fails on type errors
([TypeScript config](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript)),
so the overlap with `typecheck.py` is real — but the build also resolves routes, runs static
analysis and executes `generateStaticParams`, which is where a route that works in dev and dies in
production shows up. One subprocess, already in `package.json` (`workspace.py:113`), compiler
output, nothing to judge.

**Running the generated app's tests is a weaker signal than it looks, and the honest design says
so in its types.** Three measured results:

- Lin et al. (ISSTA 2026, above): **81–100% of failed cases pass agent-executed validation but
  fail the official evaluation.** The agent runs the tests, sees green, and is wrong.
- Ahmed, Ganhotra, Shinnar & Hirzel, [*Investigating Test Overfitting on SWE-bench*, arXiv
  2511.16858v3, April 2026](https://arxiv.org/pdf/2511.16858) — patches that pass the benchmark's
  tests still fail under broader scrutiny; passing the available tests and being correct are
  different properties.
- The test-oracle literature generally: LLM-written oracles capture substantial intended behaviour
  but *"unit test generators prioritize coverage and regression, producing tests optimized for
  passing rather than bug exposure"* — the weak-oracle problem
  ([2601.05542](https://arxiv.org/abs/2601.05542),
  [TOGLL](https://arxiv.org/pdf/2405.03786)).

**So the design rule is asymmetry**, and Scio already has the vocabulary for it:

> A failing generated test is a **`Remainder`** and enters the repair loop. A passing generated
> test is **`unjudged`** — never a gate, never counted in `checks_passed`.

That is not a compromise; it is the rule `critique.py` already enforces (*"an unreadable verdict
is a failure, never a pass"*) applied to a second untrusted judge — and it costs nothing to be
right about, because the failures are free signal and the passes were never evidence. Layer C's
criterion *"Each operation has a test for its happy path and its main failure"* is currently
`checked` when its evidence channel does not exist (Layer C §4.4 spotted this); under this
proposal it becomes `checked` for existence and `unsupported` for correctness, which is true.

### 3.2 `SCIO_VERIFY_DATA` should default on, and Layer E owns half the fix

Layer C's **C-1** fixes the supply side — a create operation declaring typed inputs instead of
`payload: json`, so `persistence_script` stops returning `None`. Layer E's half is the demand
side: defaulting the flag on costs a pglite boot, one browser round trip per feature package, and
~40MB of dev dependency. The argument for opt-in is speed; the argument against is that
`works == True` currently means *"five deterministic checks passed and a model agreed"*, and the
product's claim is that the status is honest — which `PRODUCTION_READINESS_DIFF.md` §7 already
decided on the product side. The measurement that settles it is one run each way on the same
plan, comparing wall-clock and cost. Both are instrumented. This should not be argued.

### 3.3 There is no isolating production sandbox, and ADR-0005's choice needs re-deciding with numbers

`choose_sandbox()` never returns `AcaSandbox`; its three methods raise; its own banner says *"NOT
RUN HERE… treat every line as unverified"*. The mitigation is real — the process provider refuses
under `SCIO_ENV=production` (`sandbox.py:406-414`), so the failure mode is *cannot serve*, not
*serves unsafely* — and `LocalDockerSandbox` with `CONTAINER_LIMITS` is a genuine development
boundary.

**What the isolation field settled while ADR-0005 sat unbuilt.** Scanned 2026-08-26:

| Primitive | Boot | Overhead | What it gives up |
|---|---|---|---|
| Docker / runc | ms | minimal | shared host kernel; a kernel exploit is a host escape. [Northflank, Feb 2026](https://northflank.com/blog/how-to-sandbox-ai-agents): consensus is explicit that this is not enough for AI-generated code |
| **gVisor** (Modal) | ms | 10–30% on I/O-heavy work | a user-space kernel (Sentry) intercepting syscalls — much smaller attack surface than runc, weaker than a VM |
| **Firecracker microVM** (E2B, Vercel Sandbox) | ~125ms | <5 MiB/VM | hardware-enforced isolation, dedicated kernel per workload; slightly longer boot |
| Kata Containers | ~200ms | — | VM isolation with Kubernetes-native workflow |

E2B is purpose-built for untrusted agent code on Firecracker with ~150ms cold starts; Modal runs
gVisor and is the only one where a sandbox can hold a GPU; **Cloudflare Sandboxes reached GA in
April 2026** on Cloudflare Containers with a TypeScript API for commands, files, background
processes and public service URLs ([InfoQ, April
2026](https://www.infoq.com/news/2026/04/cloudflare-sandboxes-ga/),
[cloudflare/sandbox-sdk](https://github.com/cloudflare/sandbox-sdk)); Daytona moved its production
codebase closed-source in June 2026, citing security. Azure Container Apps dynamic sessions with
custom containers — ADR-0005's choice — [remains in
preview](https://learn.microsoft.com/en-us/azure/container-apps/sessions-custom-container), billed
on the Dedicated plan on E16 instances.

**What Scio's Docker provider gives up by not using any of them** is one kernel. That is the
entire answer, and it is not small: `CONTAINER_LIMITS` bounds memory, swap, CPU and PIDs with
`no-new-privileges`, which is a resource boundary, not a security boundary.

**What ADR-0005 got right and should keep is the interface.** `SandboxProvider` plus
`test_sandbox_conformance` is precisely the structure that makes this a binding change rather
than a rewrite. The decision to re-take is which provider, with four numbers ADR-0005 flagged and
nobody has produced: prewarm latency, concurrency limit, cost per session-hour, and whether
Playwright runs inside the session or beside it. That last one is not optional — gates 4 and 4b
are a browser driving the app, and a sandbox that cannot host a browser moves the interaction
runner outside the isolation boundary.

### 3.4 There is no network policy, and the objection in `sandbox.py:267` has a published answer

The code is honest about this: *"Not a network policy: the preview has to reach npm and the
verification database, and cutting it off breaks the product rather than the attack. That is a
real remaining gap (B118)."*

The objection is correct and the conclusion no longer follows, because the shape that resolves it
ships in a product. [Vercel Sandbox's
firewall](https://vercel.com/docs/sandbox/concepts/firewall) (docs updated 2026-08-04) defines
three modes — `allow-all` (default), `deny-all`, and user-defined (deny by default, allowlist by
SNI domain and CIDR) — and **policies can be updated on a running sandbox without restarting the
process**. Their stated use case is Scio's problem verbatim: *"Start with Internet access, get
required data, lock access and start untrusted process."* That is the two-phase policy Scio needs:
install with egress to the registry, then narrow to the verification database and the app's own
origin before generated code runs. It also names **credentials brokering** — injecting a
credential at egress so the secret never enters the sandbox. Scio's env allow-list
(`sandbox.py:105`) solves that by omission; brokering solves it for credentials the app needs.

**The limits, which must be stated with the adoption:**

- domain rules match the **SNI only**, so domain fronting can reach a different virtual host
  behind an allowed endpoint; plain HTTP cannot be filtered by domain at all;
- `subnets.allow` leaves DNS unrestricted, and DNS is itself an exfiltration channel;
- an allowlist does not stop exfiltration *through* an allowed destination — an injected prompt
  can use free-form fields of a permitted API as a covert channel
  ([Safeguard, 2026](https://safeguard.sh/resources/blog/agent-runtime-egress-controls-2026)).

None of that makes the policy not worth having. It makes "we have an egress allowlist" a
statement about accidents and broad classes of attack, not about a determined adversary — which
is exactly how `execution/untrusted.py` already talks about its own fence.

### 3.5 The API still owns a forty-minute unit of work

ADR-0020 points 2 and 3 are unbuilt: the engine has no concept of a job id, and there is no
queue, no worker, no `SELECT … FOR UPDATE SKIP LOCKED`, no broker. The ADR is explicit that 1–5
are not separable — *"Restart-safety, cancellation and admission control all follow from (1) and
(3)"* — and calls it the largest single piece of work left.

§1.1h is the cost of not having it, and it is not the cost the ADR predicted. The ADR warns that
*"the current design does not survive a deploy"*; what happens first is smaller and stranger — a
quiet build marked failed by a reaper that cannot stop it, on the strength of a heartbeat a
keepalive cannot advance. Two of those three things are one-line fixes inside the current design:
write `heartbeatAt` on a keepalive too, and give the reaper a status the cancel check acts on.
**Fix those first; they are not a reason to defer the queue, and the queue is not a reason to
leave them.**

### 3.6 There is no observability, and the convention to adopt is not stable yet

Zero matches for `opentelemetry`, `prom-client`, `correlationId` or `requestId` across API and
engine; one logging reference in the whole builder. C-F03 / G-F05, still true.

**The convention exists and its honest status is "Development".** In `semantic-conventions`
v1.42.0 (June 2026) all GenAI conventions were deprecated in the main repo and moved to
`open-telemetry/semantic-conventions-genai`, which as of July 2026 has **no tagged release**;
every `gen_ai.*` attribute, span, metric and event still carries the Development badge ([state of
the conventions, July 2026](https://john-hodge.com/blog/opentelemetry-genai-semantic-conventions/)).
Adopt the **names**, pin v1.42.0, claim no conformance:

| Scio has | OTel GenAI name |
|---|---|
| `Completion.vendor` | `gen_ai.provider.name` (replaced `gen_ai.system` in v1.37.0) |
| `Completion.input_tokens` / `output_tokens` | `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` |
| — (does not exist yet, §7) | cache-token attributes, added v1.40.0 |
| `CriterionVerdict` from `critique.py` | **`gen_ai.evaluation.result`** event (v1.38.0): `evaluation.name`, `score.value`, `score.label`, `explanation` |

The last row is the one to stop on. Scio's per-criterion critique verdict — a name, a pass/fail
and a reason — **is** `gen_ai.evaluation.result`, field for field, and the five deterministic
gates fit the same event. Do not invent a gate-result schema. `Remainder.source` is already the
`evaluation.name` namespace. The one thing OTel does not name: **a build id on every span, event
and log line.** `BuildJob.id` exists (`schema.prisma:229`) and the engine has never heard of it —
that is ADR-0020 point 2, and it is the same gap.

### 3.7 No prompt caching, no batch, and no way to measure either if they landed

`grep -rn "cache_control\|ephemeral"` over the engine returns nothing. `STRATEGY.md` §G lists
caching under *"Adopt now (clear wins, low risk)"* and calls it *"our single biggest cost lever"*.
§7 shows why it is not a one-line change and what the real prerequisite is.

### 3.8 The generated app has no backend

ADR-0011 makes Supabase the generated app's backend; `grep -rn supabase apps/api/src` returns
nothing. Verified apps run against pglite; delivered apps get a client pointing at an unset
`NEXT_PUBLIC_SUPABASE_URL`. This belongs beside ADR-0018 (what Publish is) rather than in this
layer's backlog — but Layer E is where it becomes visible, because gate 4b asserts row-level
isolation against a database that will not be the one the delivered app talks to.

### 3.9 The reveal shows a fraction of what the build already knows

`PRODUCTION_READINESS_DIFF.md` §7 lists nine things the reveal should show. Checked against
`RevealPage.tsx` and `BuildFinished` (`pipeline.py:63-103`):

| §7 requires | Shown | Computed |
|---|---|---|
| requirements met and unmet | no | per-criterion, in `CritiqueResult` — discarded at the package boundary |
| tests and browser flows | no | interaction outcomes exist, opt-in |
| security checks | no | `check_security` runs on every package; only failures survive, as prose |
| changed packages and files | no | `BuildFinished.files`, `package_files`, `manifest` — all transmitted, none rendered |
| verified-unchanged surface | no | not computed |
| model and build cost | cost only | `BuildFinished.model` is transmitted and not rendered |
| build time | no | not computed — `BuildFinished` has no duration field |
| remaining risks | partly | `remainders` are rendered, `unjudged` are not surfaced as a category |
| version id and export | yes | version + git sha |

Two and a half of nine. And `checks_passed` — whose docstring says *"`checks_passed/len(GATES)` is
what the reveal shows, so the count is a real count and not a number chosen to look reassuring"* —
appears in `packages/shared/src/intake.ts:287` and in **no** `.tsx` file. **A rebuild that only
rendered what this layer already computes would deliver most of §7 without generating a single new
fact.**

---

## 4 · Out of the box

### 4.1 The build produces an attestation and throws it away — and the format already exists

Every build produces: the spec it was approved against, the plan, the pinned stack, which parts
came from the library and which were generated, the model that wrote each one, seven validation
agents' findings, a console classification, browser interaction outcomes, a critique verdict per
criterion, an app-wide typecheck, a git sha, a manifest, and a cost. That is the most complete
evidence trail in the product, and it survives as four lists of package ids and a number.

**Do not invent a format for it.** [SLSA Build
Provenance](https://slsa.dev/spec/draft/build-provenance) as an
[in-toto attestation](https://github.com/in-toto/attestation/blob/main/spec/predicates/provenance.md)
(`predicateType: https://slsa.dev/provenance/v1`) is the standard shape, and the mapping is
uncomfortably direct:

| SLSA field | Scio |
|---|---|
| `subject` | the git sha of the delivered workspace, plus per-file digests from the manifest |
| `buildDefinition.buildType` | Scio's pipeline version |
| `buildDefinition.externalParameters` | the approved `AppSpec` and the `BuildPlan` |
| `buildDefinition.resolvedDependencies` | pinned `DEPENDENCIES`/`DEV_DEPENDENCIES` **and the library entries assembled**, by `category.seqno.version` (ADR-0016) |
| `runDetails.builder.id` | the model ids that actually ran, plus the matrix version |
| `runDetails.metadata` | `invocationId` = `BuildJob.id`, `startedOn`/`finishedOn` |
| `runDetails.byproducts` | every gate report |

**The limits, plainly.** SLSA is about the *integrity of the build process* — that the artifact
came from the sources and the builder it claims. It says nothing about whether the software meets
its requirements. It gives Scio the envelope and the vocabulary, not the verdict; the verdict is
`produced_by × observed_by`, which is Scio's own and better. Claiming a SLSA *level* needs things
Scio does not have (a hosted non-falsifiable builder, signing), so the honest adoption is *"we
emit SLSA-shaped provenance"*. The payoff is ADR-0001's wedge: a repository plus a statement of
what built it, from what, and what checked it, is a handoff. Four status lists on a web page is
not.

### 4.2 The gates are a reflexion model, and Scio already has the skill for it

`.claude/skills/reflexion-conformance` carries the software reflexion model — a high-level model
plus a mapping, producing **convergences, divergences and absences** rather than pass/fail. Layer
E already emits exactly three categories: `passed`, `failed`, `unjudged`. The third is what makes
the honesty claim work and no competitor has it. Naming it buys one concrete thing: **absence
becomes a first-class output of the build rather than a footnote.** *"Three things in this app
nobody checked, and here they are"* is Layer C §4.1's move at the plan gate, and Layer E is where
the list is produced — `gate.unjudged`, `app_unjudged`, `Observability.unsupported`, and the 5 of
23 criteria this layer's own plan records as observed by nobody.

### 4.3 The deterministic packages should stop being model calls at all

The most reliable way to reduce token spend is not to route it more cleverly. Look at what the
default plan actually buys:

| package | expected output tokens | what it is |
|---|---:|---|
| `pkg_auth` | 2,500 | one helper and a test |
| `pkg_design_tokens` | 3,000 | a CSS file and a Tailwind config |
| `pkg_schema` | 4,900 | a migration and generated types |
| `pkg_foundation` | 8,000 | layout, header, supabase client, shell pages |
| `pkg_feature_booking` | 16,000 | the app |

Four of five packages are **near-deterministic transformations of the architecture graph**. A
migration renders `data_model`. Design tokens render `DesignTokens` — which
`.claude/skills/app-design` already proposes to make a W3C DTCG document. An auth helper for a
fixed stack with a fixed posture is a template with a variable in it. `builder/standin.py` already
proves a keyless path through the pipeline exists.

The proposal — and it is ambitious, so mark it as such: **codegen becomes a feature-package
activity.** The horizontal packages are produced by the library (ADR-0014: *"match every package
before generating"*, exactly this) or by deterministic templates, and the model is spent only where
the work is genuinely open. On the canonical plan that is ~18,400 of 34,400 expected output tokens
— **more than half the build**, and the half with the least variance and the fewest interesting
failures.

What it breaks, honestly: the library's contribution loop learns from generated packages, so
templating them removes the input that makes ADR-0016 work for those categories; and a template
that drifts from ADR-0011's stack is a silent failure that a model would have adapted to. The
second is the real risk and it is the one `test_sandbox_conformance`-shaped thinking answers —
the template's output goes through the same gates as generated code, so drift fails a build rather
than shipping.

### 4.4 The preview's unit is wrong

A preview is one `next dev` per project, in one container, for one person, held for a session, and
session cooldown is the only cost lever anybody has reached for. Three speculative directions:
**build once and serve statically** — if E-5 lands, its artifact *is* a production build, at the
price of the hot reload the design window depends on (a two-mode question, not a replacement);
**one sandbox per build rather than per project**, since the verification app and the
marking-bridge app are different apps with different flags (`workspace.py:142`) sharing one
lifecycle; and **the verification database as a service**, since pglite is a 40MB devDependency
shipped inside the delivered artifact so `assert_row` can run through the app's own process.

### 4.5 The competitive floor: Scio verifies more than anyone and shows less

Scanned 2026-08-26.

| | Verification shipped |
|---|---|
| **Lovable** | a basic security scan on every publish (~10–15s: database configuration, RLS rules, cloud project settings, known misconfiguration patterns), an on-demand deep agentic code review (~3 min: access control, unprotected endpoints, exposed secrets, unsafe input handling), continuous dependency checks, optional Wiz and Aikido connectors, agent auto-fix for non-breaking findings, and a workspace setting to **block publishing on critical findings** ([docs](https://docs.lovable.dev/features/security-view)) |
| **Bolt** | in-browser test execution and vendor-claimed automatic testing and iteration |
| **Replit Agent** | builds and verifies before handing over, checkpoints to roll back to, provisions databases and ships to a public URL |
| **v0** | frontend components; no backend |

**Lovable's publish gate is the competitive floor, and Scio does not have one.** Scio runs seven
deterministic validation agents — including a secret scanner, an `eval`/`dangerouslySetInnerHTML`/
interpolated-SQL check and an import-boundary check — plus a console classifier, a browser
interaction gate asserting row-level isolation with two users, a model critique per criterion, and
an app-wide typecheck, **per package** rather than once at publish. That is more verification than
anything above, and the reveal renders four lists of ids. *The differentiator is built and
unrendered.*

Two things Lovable has that Scio has not, both cheap: **findings that persist as a view you can
return to** rather than remainders attached to one build, and **a gate with a workspace policy** —
block, warn, allow. `check_security` produces the findings; `Severity` separates error from
warning; nothing turns that into a decision anyone configured.

### 4.6 `Script` is already a small language — decide whether it is one

`core/interaction.py` defines a step vocabulary — `as_user`, `fill`, `click`, `reload`,
`assert_present`, `assert_absent`, `assert_row` — derived from the architecture rather than
authored by a model (`layerc/scripts.py:1`). That is a DSL with a compiler (`scripts.py`) and a
runtime (`interaction_runner.py`), and nobody has called it one. Layer C §3.3 maps EARS clause
slots one-to-one onto these steps; if that lands, `Script` becomes the executable form of an
acceptance criterion — what Gherkin exists to be, without its ceremony, and with the property
Gherkin lacks: **it is derived, not written.** The counter-argument applies to every bespoke
notation — no ecosystem, permanent maintenance. The counter to that is seven verbs that already
exist. Keep it small or do not keep it.

---

## 5 · The means — skills, MCP, repos, research

Per `docs/next/SKILLS.md`: a **Claude Skill** helps *us* build Scio; the product's runtime uses
relays and prompts. Nothing in this table becomes product machinery for free.

| Means | What it gives Layer E | Verdict |
|---|---|---|
| **Huang et al., ICLR 2024** ([2310.01798](https://arxiv.org/abs/2310.01798)) · **Kamoi et al., TACL 2024** ([2406.01297](https://arxiv.org/abs/2406.01297)) | intrinsic self-correction does not reliably help and can degrade; external feedback is what works | **adopt** (§2.1) — it decides the default profile → skill written |
| **Kiecker et al., July 2026** ([2607.05197](https://arxiv.org/html/2607.05197v1)) | the diminishing-returns curve: 3–4 iterations capture the vast majority of the gain | **adopt** — it *validates* `max_attempts = 3` → in the same skill |
| **Lin et al., ISSTA 2026** ([2606.26978](https://arxiv.org/html/2606.26978)) | execution feedback buys 1.25pp and costs 56–62% of tokens on SWE-bench-style repair; 81–100% of failed cases pass agent-run validation | **adopt with its scope stated** (§2.3, §3.1) → in the same skill |
| **Ahmed et al., April 2026** ([2511.16858](https://arxiv.org/pdf/2511.16858)) | test overfitting: passing the available tests ≠ correct | **adopt** — it is why §3.1 is asymmetric |
| **Firecracker** (Agache et al., NSDI 2020) · **gVisor** · [Northflank, Feb 2026](https://northflank.com/blog/how-to-sandbox-ai-agents) | the isolation ladder with numbers: ~125ms boot, <5 MiB/VM, gVisor 10–30% I/O overhead | **adopt the framing** (§3.3) → skill written |
| **Vercel Sandbox firewall** ([docs, 2026-08-04](https://vercel.com/docs/sandbox/concepts/firewall)) | three policy modes, **live policy updates on a running sandbox**, credentials brokering, and an explicit statement of SNI/DNS limits | **adopt the pattern** (§3.4) — not the product → in the same skill |
| **Anthropic prompt caching** ([docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)) | 512-token floor on Opus 5, 4096 on Haiku 4.5; reads ~0.1×, writes 1.25× (5m) / 2× (1h); 4 breakpoints; 20-block lookback; concurrent requests cannot read each other's writes | **adopt** (§7) — after the three structural blockers |
| **OTel GenAI semantic conventions** ([state, July 2026](https://john-hodge.com/blog/opentelemetry-genai-semantic-conventions/)) | attribute and event names, including `gen_ai.evaluation.result` | **adopt the names, pin v1.42.0, claim nothing** (§3.6) |
| **SLSA / in-toto provenance** ([slsa.dev](https://slsa.dev/spec/draft/build-provenance)) | the envelope for a build attestation | **adopt the shape** (§4.1). Not the level |
| **E2B / Modal / Cloudflare Sandboxes / Vercel Sandbox as products** | managed isolated runtimes | **evaluate, do not assume** (§3.3). ADR-0005 is Azure-committed via ADR-0004; the four unanswered numbers decide it |
| **Batch API** — 50% of standard rates, results keyed by `custom_id` | the payoff for a scheduler | **later** (§7.4) — it needs Layer C's antichain (C-7) and it trades the live progress the build screen is built on |
| **`fix` matrix ranking** (ours, unused) | a repair is a different task shape from a first draft | **wire it** (§2.6); decide the ranking with §8's data |
| **MCP: code-graph / dependency servers** | AST and call-graph traversal over code on disk | **genuinely useful here**, unlike Layer C — but the candidate use, slicing the repair prompt (§6.1), is already answered for free by `Finding.file`. A later refinement, not a dependency |
| **Agentless** ([2407.01489](https://arxiv.org/abs/2407.01489)) · **DSPy** | localise-then-repair at $0.34/issue; prompt-program optimisation | **later** — the first supports the existing design without changing it; the second needs a metric (§8) |

**Skills specific to Layer E**, for the build process. Two written, and the reasons two others were
not are part of the answer.

| Skill | Change | Rests on | Used by |
|---|---|---|---|
| `execution-feedback-economics` | **new** — the two-loop distinction, the diminishing-returns curve, the asymmetric rule for model-written tests, and four evals a change to `codegen_passes` or `max_attempts` must pass | Huang et al.; Kamoi et al.; Kiecker et al.; Lin et al.; Ahmed et al. | E-1, E-6 |
| `sandbox-isolation` | **new** — the isolation ladder with measured numbers, the two-phase egress policy, credentials brokering, and the three limits an allowlist does not cover | Firecracker NSDI'20; gVisor; Vercel Sandbox firewall docs; Northflank Feb 2026 | E-8, E-9 |

**Two skills deliberately not written:**

- **No `prompt-caching` skill.** The bundled `claude-api` skill already carries the per-model
  floors, the multipliers, the breakpoint rules, the 20-block lookback and the silent-invalidator
  table, first-party and current. A second copy would be inventory that goes stale, and
  `SKILLS.md` warns about exactly this.
- **No `otel-genai` skill.** The conventions are in Development with no tagged release (§3.6).
  A skill encoding a moving target teaches drift. Revisit when the dedicated repository cuts one.

**Two applications of the honesty rule**, because a reader would otherwise get them wrong:
Kiecker et al. tested Gemma-4 31B, Qwen3.5 27B and gpt-4o-mini and state their results *"may not
generalize to larger, newer LLMs"* — the 3–4 iteration curve is the direction to trust, not the
constant, and Scio runs Opus 5. And Lin et al. is scoped to repository bug fixing where a test
suite exists and localisation is the hard part; Scio writes code from nothing, and reading that
paper as licence to skip the browser would be exactly backwards.

---

## 6 · Retrieval versus packing

**Where does this layer send context it could have queried instead?**

Layer E packs more tokens than every other layer combined, and three of the four places are fixable
with data the layer already computes.

### 6.1 The repair prompt sends every file when the findings already name one

`fix_prompt` (`codegen.py`) interpolates `current_files` verbatim, and `_write_attempt` builds
that from `_files_on_disk(app_dir, allowed)` (`loop.py:582`) — **every file the package owns**. On
a feature package that is eight files, ~16,000 tokens, re-sent on every repair attempt and again
on every relay pass within it.

The findings that triggered the repair already know which file. `Finding.file`
(`validation.py:42`) carries it; `TypeProblem.file` carries it with a line number;
`Remainder.where` is populated from `f.file or package.id` (`loop.py:687`). And `gate.problems` —
the list that actually reaches `fix_prompt` — is `list[str]`: `report.instructions()` flattens the
structure into prose and the file identity is lost between `:687` and `:401`. **The layer's own
instance of the system-wide pattern**: the join key is computed, used once for a `Remainder`
nobody renders, and dropped before the one consumer that would save money with it.

The refinement: make `problems` carry `(file, message)`, slice `current_files` to the files named,
and keep a whole-package fallback for findings with no file (`check_files_complete`, console
errors, critique verdicts) — the same shape as Layer C §6.1's grounded slice with a narrative
fallback, for the same reason.

### 6.2 Every relay pass re-sends the previous pass's entire output

`_build_messages` (`relay.py:148-167`) builds pass *n*'s user turn as `instruction + ORIGINAL TASK
+ PREVIOUS ANSWER` — for a feature chunk, ~8,000 tokens of code re-sent on passes 2, 3 and 4. This
is **not** a packing violation; it is what a review pass is, and `fix_prompt`'s docstring already
records why (*"A model asked to fix code it cannot see invents a plausible replacement, which is
how ids get lost"*). The answer is caching (§7), not retrieval — and §7.2 shows why the current
message construction makes even that impossible. If §2.1 lands and the default drops to two
passes, this cost falls by two thirds with nobody touching the mechanism.

### 6.3 Chunked packages pack every earlier chunk's full body into every later chunk

`build_prompt`'s `already_written` (`codegen.py`) sends earlier chunks verbatim *"so imports and
names line up across a package that was written in pieces."* Correct today. But what the later
chunk needs is what the earlier one **exports** — names and signatures, not bodies. That is
`PackageInterface`'s distinction one level down, and Layer C already asserts it in
`test_dependencies_contribute_interfaces_not_implementations`. `tsc --declaration
--emitDeclarationOnly`, run with the app's own compiler exactly as `typecheck.py:83` argues for,
produces it deterministically. Speculative, and bounded: only feature packages chunk, and only
into two or three, and a `.d.ts` may omit something the model needed. Do it after §7's caching, so
it can be measured against a stable baseline rather than confused with it.

### 6.4 Where packing is correct

The contract, the file listing, `INSTRUMENTATION_RULES` and `FILE_FORMAT_RULES` are all
per-call-relevant and none is queryable: the contract is Layer C's product and arrives whole, the
file list is short, and the rules are the format the reply must satisfy. Leave them.

---

## 7 · Token economy

Measured 2026-08-26 against the real prompts assembled from `derive_architecture(make_booking_spec())`,
five packages. Token figures are chars ÷ 4 unless stated.

### 7.1 What a default build actually sends

**The constants, measured:**

| Block | chars | ≈ tokens |
|---|---:|---:|
| `CODEGEN_SYSTEM` | 1,836 | **459** |
| `FIX_SYSTEM` | 1,465 | 366 |
| (of which `INSTRUMENTATION_RULES`, in both) | 806 | 201 |
| `REVIEW_INSTRUCTION` | 204 | 51 |
| `FINAL_INSTRUCTION` | 192 | 48 |

**The per-package prompts, measured:**

| Package | `contract_prompt` | `build_prompt` | files | chunks |
|---|---:|---:|---:|---:|
| `pkg_foundation` | 1,078 | 1,125 | 4 | 1 |
| `pkg_schema` | 1,268 | 1,308 | 2 | 1 |
| `pkg_design_tokens` | 1,186 | 1,223 | 2 | 1 |
| `pkg_auth` | 1,112 | 1,146 | 2 | 1 |
| `pkg_feature_booking` | 1,359 | 1,439 | 8 | **2** |

**The call count**, at the shipped default (`codegen_passes = 4`, `critique_passes = 1`,
`max_attempts = 3`):

| | relay calls |
|---|---:|
| every package passes attempt 1 | (1+1+1+1+2 chunks) × 4 passes + 5 critiques = **29** |
| every package needs three attempts | 24 + (5 pkgs × 2 repair attempts × 4 passes) + up to 15 critiques = **79** |

The repair path is not chunked (`_generate` takes the `if problems:` branch at `loop.py:399`), so
a repair is one relay of four passes carrying the entire package.

**Input, per relay:**

- codegen pass 1 ≈ 459 (system) + 1,125–1,439 (user) ≈ **1,600–1,900**
- codegen passes 2–4 ≈ the above + the previous answer, which for a feature chunk is ~8,000
  tokens of code ≈ **10,000 each**
- a repair pass 1 ≈ 459 + 1,439 + ~16,000 (every file in the package) ≈ **18,000**
- repair passes 2–4 ≈ 18,000 + ~8,000 ≈ **26,000 each**

At Opus 5 list ($5 in / $25 out): one repair round of a feature package is ≈96k input and ≈32k
output → **$0.48 input, $0.80 output — input is 37% of that call's bill.** That is the *"a third
to a half"* the `_cost` docstring records, reproduced from the prompt shapes rather than taken on
trust. It is also, precisely, the fraction `estimate_plan` does not price (§1.1e).

### 7.2 Caching is blocked by four things, and only one of them is "nobody wrote `cache_control`"

**1. The system prompt has no place to put a breakpoint.** `AnthropicProvider._complete` joins
every `role="system"` message into a single **string** and passes `{"system": system}`
(`provider.py:170, :178`). `cache_control` goes on a content *block*; a string has none. The
change is to send `system=[{"type": "text", "text": ..., "cache_control": {...}}]`.

**2. The only constant in the path is 459 tokens, and the Opus 5 floor is 512.** Verified against
the first-party table:

| Model | Minimum cacheable prefix |
|---|---:|
| **Claude Opus 5**, Fable 5 | **512** |
| Opus 4.8, **Sonnet 5**, Sonnet 4.6 | 1,024 |
| Opus 4.7 | 2,048 |
| Opus 4.6, **Haiku 4.5** | **4,096** |

`CODEGEN_SYSTEM` is ~53 tokens short. Below the floor there is no error — just
`cache_creation_input_tokens: 0`. Adding `cache_control` today would do nothing and report nothing.

**3. The varying instruction is at the front of the user turn, and draft and repair use different
system prompts.** `_build_messages` builds pass 2+ as `instruction + "\n\n--- ORIGINAL TASK ---\n"
+ prompt + "\n\n--- PREVIOUS ANSWER ---\n" + previous`. Because the instruction is *first*, pass
1's user content is not a byte prefix of pass 2's, so nothing shared between the passes of a
single relay can cache. Reordering to `prompt` → `previous answer` → `instruction` makes pass 1's
content an exact prefix of pass 2's. And `CODEGEN_SYSTEM` ≠ `FIX_SYSTEM`, so a draft and its
repairs cannot share a prefix at all.

**4. And the one that makes this dangerous to ship as a one-liner.** `Completion`
(`provider.py:31-39`) has `input_tokens` and `output_tokens` and no cache fields, and `_cost`
prices every input token at `card.input_cost_per_mtok`. If caching started working tomorrow, the
ledger, the ceiling and the reveal would all **over-report by up to 10× on the cached portion** —
and `Spend.would_exceed` would stop builds that were well inside their budget. The cache-token
attributes OTel added in v1.40.0 (§3.6) are the names to use.

### 7.3 What a correct fix is worth

Put the breakpoint at the end of the **contract**, not the end of the system prompt. That makes
the cacheable prefix ≈ 459 + 1,078–1,359 = **1,540–1,820 tokens**, which clears the Opus 5 floor by
3×, and it is re-read on every pass and every attempt of that package: up to 12 codegen calls.

Per package, with the 5-minute TTL (write 1.25×, read 0.1×):

```
uncached:  12 × 1,700 = 20,400 tokens at $5/MTok  = $0.102
cached:    (1.25 + 11 × 0.1) × 1,700 = 4,000      = $0.020
saving per package ≈ $0.082
```

Five packages ≈ **$0.41 on a build estimated at $2.44–$9.07** — 4.5–17%, and larger the more repairs
happen, which is when it matters most. Modest, real, and it grows with the playbook: Layer C §7.1
measures a further 892 tokens of constants that would join the same prefix.

**And the routing check that has to accompany it.** A 1,700-token prefix caches on Opus 5 (512) and on
Sonnet 5 (1,024). It **does not cache on Haiku 4.5 (4,096)**. `matrix.yaml` ranks Haiku first for
`light_edit`, and §2.6 proposes wiring the unused `fix` ranking — so any proposal that routes
repairs to Haiku to save on the per-token rate would silently lose caching on the single largest
prefix in the system. That trade has to be priced, not assumed. The test that prevents it is one
assertion: **the constant prefix must exceed the floor of the model it will run on.**

Two more first-party facts that constrain any scheduler:

- **A cache entry is readable only after the first response begins streaming.** N parallel
  requests with identical prefixes all pay full price. A parallel Layer E scheduler must fire one
  call, await its first token, then fan out — or it converts the caching win into N cache writes.
- **Max 4 breakpoints per request, and a 20-block lookback.** Both are comfortably above what
  Layer E needs today; both become live constraints if `already_written` (§6.3) becomes many
  blocks.

### 7.4 The Batch API is 50%, and it is third in line

Batch runs asynchronously at 50% of standard rates, with results keyed by `custom_id` and returned
in any order. `orchestrate.py:19` says MVP is sequential and `parallelizable` is recorded but
unscheduled; `BACKLOG.md:18` correctly reframes batching as a product call, because it trades the
live per-part progress the build screen is built on (`BuildPage.tsx:102`).

Order matters and it is not the order the strategy doc implies:

1. **Layer C's C-7** — compute `parallelizable` from the dependency antichain instead of
   `len(group) > 1`. Batching packages that were wrongly flagged independent produces code
   generated against an interface its dependency had not declared, which surfaces as incoherence
   rather than as an error.
2. **Caching** (§7.2), because batching before caching means every batched request is a cache miss
   (see the concurrency rule above).
3. **Batch**, if the product accepts losing live progress — and the honest framing is that it
   probably should not for the first build, and probably should for a re-verification sweep of the
   library (`library/reverify.py`), which nobody is watching.

### 7.5 The lever that dwarfs all of the above

Caching saves 4.5–17%. Batching saves up to 50% of what remains, at a product cost. **Dropping
`codegen_passes` from 4 to 2 saves 50% outright, needs no new mechanism, and is the change the
literature supports** (§2.1). The order to do things in is: measure (§8), then passes, then
caching, then parallelism, then batch.

---

## 8 · Data worth owning

Layer E produces more measurable fact per build than the rest of the system together, and keeps
almost none of it past the reveal.

| Data | Why it is worth having | Already computed at |
|---|---|---|
| **Predicted vs actual output tokens, per package kind** | `estimate.py` says outright that it *"needs a real run to calibrate against rather than a coefficient invented here (B115)."* Every build produces exactly that datum | `expected_output_tokens` vs `PackageBuildResult.total_tokens` |
| **Predicted vs actual *input* tokens** | the third to a half of the invoice `estimate_plan` does not model at all (§1.1e). `count_tokens` gives the prediction for free | absent — needs §2.2 |
| **Attempts to green, per package kind** | the direct test of `max_attempts = 3` against Kiecker et al.'s curve on *our* task, with *our* model | `PackageBuildResult.attempts` |
| **Which gate failed first, per attempt** | the priority order for evidence channels, and the only honest way to argue about gate ordering | `_Gate` — discarded after the decision |
| **Whether pass *n* changed anything** | the measurement that settles §2.1. Diff pass *n*'s output against pass *n−1*'s; a relay whose later passes reproduce the earlier one is a relay that should be shorter | `RelayResult.passes[*].text` — all four are held and thrown away |
| **The true build spend** | `Spend.spent_usd` is correct and unread (§1.1d) | `relay.py:112` |
| **`cache_read_input_tokens` per call** | the only way to know caching works, and the thing that makes the ledger right (§7.2) | absent — needs a field on `Completion` |
| **Criteria ending `unjudged`, per package kind** | 5 of 23 on the canonical app. This is the list of things Scio promises and does not check, in priority order | `gate.unjudged`, `app_unjudged` |
| **Console lines suppressed, by origin; validation findings by agent, and which repaired** | `ConsoleReport.suppressed` exists so the filter stays auditable and nothing audits it; and which of the seven agents earn their place | `core/console.py`, `ValidationReport.findings` |
| **Sandbox boot time, install cache hit rate, preview uptime** | most of what ADR-0005 needs and nobody has (§3.3) | `InstallReport`, `SandboxHandle.uptime_s` |
| **Build shape → outcome, per app kind** | after fifty booking apps you know which packages fail, how often, and at which gate. This is the moat, one layer down from Layer C §8, and it cannot be bought | everything above, joined |

None of this needs new collection. It needs a `build-metrics` harness and not throwing away what
already passes through — the same argument Layer A makes for `StandInIntakeProvider` and Layer C
for `use_judgment=False`. **Layer E's free deterministic baseline already exists**:
`builder/standin.py` runs the entire pipeline with no API key, and its 315 lines are currently
filed as a footgun rather than as the control arm of every experiment in this document.

Same constraint as everywhere else: this is derived from user data, and ADR-0019 is still
**Proposed**. Settle what survives a project deletion before the corpus accumulates.

---

## 9 · ADR proposals

| # | Proposal | Decides |
|---|---|---|
| **E-1** | **The shipped default becomes `SCIO_MODEL_PASSES=1`** (two relay passes) | halves the default build cost. Alternatives: keep 4, or vary by package kind. Evidence: unfed passes do not reliably help (Huang, Kamoi) while fed repair rounds do (Kiecker); counter-evidence: Scio's passes may be cross-model rather than self-review. **Decide with E-2, not by argument** |
| **E-2** | **A build-metrics harness before any tuning ships** | `standin.py` is the free baseline; §8 is the table. Nothing else here is decidable without it, exactly as A-3 and C-12 are for their layers |
| **E-3** | **The ceiling is checked before the call, and the partial spend is never lost** | `count_tokens` + `max_tokens` × output rate as the pre-call bound; `BudgetExceeded` carries the accumulated cost. Two fixes, both needed. Consequence: over-refusal on a call whose real output is short — the price of the ceiling meaning what it says |
| **E-4** | **`Spend.spent_usd` is the reported build cost** | one field on `AppBuildResult`; the reveal's number becomes larger and correct. Also decides whether Layers B and C come inside the ceiling — today they are outside it *and* outside the estimate, which is coherent, but the workspace ledger under-reports either way |
| **E-5** | **`next build` becomes an app-wide gate** | deterministic, no oracle problem, catches what `tsc --noEmit` cannot. Alternatives: replace the typecheck gate, or run both. Consequence: build time, and a real chance today's apps fail it |
| **E-6** | **Generated tests run, and a pass is never evidence** | a failing test is a `Remainder` in the repair loop; a passing one is `unjudged` and never counts toward `checks_passed`. Needs a runner in the scaffold and a real filename convention (§2.4). The asymmetry is the decision; Lin et al. and Ahmed et al. are why |
| **E-7** | **`SCIO_VERIFY_DATA` defaults on** | the honesty claim versus a pglite boot and one browser round trip per feature. Blocked on Layer C's **C-1**, without which there is nothing to drive. Measurable; should not be argued |
| **E-8** | **Re-decide or re-affirm ADR-0005 with the four numbers** | prewarm latency, concurrency limit, cost per session-hour, whether Playwright runs inside the session. ACA custom-container sessions are still in preview; Firecracker (E2B, Vercel), gVisor (Modal) and Cloudflare Sandboxes (GA April 2026) are the field. **ADR-0004 commits to Azure, so this is a tension between two ADRs and must be written as one.** Either way ADR-0005 needs an implementation-status line — it reads as decided and has never run |
| **E-9** | **A two-phase egress policy on the sandbox** | install with egress, then narrow before untrusted code runs — Vercel Sandbox's live-update pattern. Consequence: stated per provider, with the limits (SNI-only matching, DNS, exfiltration through allowed destinations) documented rather than implied. Closes B118 honestly, not completely |
| **E-10** | **The reveal renders what the build already computed** | `checks_passed`, the model, per-criterion verdicts, changed files, the `unjudged` list — two and a half of the readiness diff's nine. Product decision, no new engine. **The cheapest large win here** |
| **E-11** | **A publish gate with a workspace policy** | block / warn / allow on critical findings — the floor Lovable ships. `check_security` produces the findings; `Severity` separates error from warning; nothing makes it a decision. Blocked on ADR-0018 |
| **E-12** | **Prompt caching, in the right order** | (a) `system` as a content-block list; (b) `_build_messages` puts the instruction last; (c) breakpoint at the end of the contract; (d) cache fields on `Completion` and in `_cost`. **(d) is not optional** — without it a working cache breaks the ledger and the ceiling. Plus a test asserting the prefix clears the floor of the model it runs on |
| **E-13** | **The build emits SLSA-shaped provenance** | subject, buildDefinition, runDetails, byproducts. A claim about *shape*, never about a level. ADR-0001's handoff promise, made into an artifact |
| **E-14** | **Observability on OTel GenAI names, pinned and unclaimed** | `gen_ai.provider.name`, `gen_ai.usage.*`, cache tokens, `gen_ai.evaluation.result` per gate verdict. Pin v1.42.0. Requires ADR-0020 point 2 — the engine must know the job id |
| **E-15** | **A test double may be no stricter than production** | `FakeScope` is stricter than `WorkspaceScope` (§1.1i); `AcaSandbox` is absent from the suite written to catch its defect (§2.5). One policy: doubles are proved against the same conformance suite as the real thing, and a provider outside that suite is not a provider |

**Ordering.** **E-2 first, and it is not close** — four proposals here (E-1, E-6, E-7, E-12) are
arguments about magnitudes nobody has measured, and `standin.py` makes the baseline free. **Then
the honesty fixes that are small and unblocked**: E-4 (one field), E-15 (one line and one red
test), and the two one-line heartbeat fixes from §3.5 that stop the reaper marking live builds
failed — none changes what the product does, all change whether what it says is true. **Then
E-1**, which is the money, and **E-3**, which is the ceiling meaning what it says. **Then the two
the user sees**: E-10, which needs no engine work and delivers most of §7 of the readiness diff,
and E-5, which is one subprocess and will fail some builds — the point. **Then E-7** (blocked on
C-1), **E-6**, **E-12**, and **E-11** (blocked on ADR-0018).

**E-8 and E-9 sit outside that order**: they are sequenced not by cost but by whether Scio is
serving real users. Neither matters in development; both are prerequisites for production traffic
alongside ADR-0020's queue. **E-13 and E-14 land last, deliberately** — both record what a build
did, and recording it before E-2 defines what is worth recording would build the wrong schema
well.

**Three dependencies across documents, stated plainly:**

- **E-7 needs Layer C's C-1.** Turning the interaction gates on before the interaction channel
  produces criteria would change nothing except the build time. This is the strongest cross-layer
  dependency in the family and both halves are small.
- **E-12 compounds with Layer C's C-5.** Layer C moves the constants to the front of the contract;
  Layer E puts the breakpoint at the end of it. Either alone is worth less than half of both.
- **§7.4's batching needs Layer C's C-7.** `parallelizable` is currently `len(group) > 1`, and
  `STRATEGY.md:111` already plans to route on it.

**Two open questions I could not settle from the code:**

**a. Does the build's cost include Layers B and C?** `run_layer_b` and `run_layer_c` take no
`spend` parameter, so the narrative relay (up to two passes) and the grouping judgment are outside
the ceiling and outside the estimate. That is *coherent* — the ceiling matches what the user
approved — and it means the workspace ledger understates what the workspace spent. Whether the
ceiling should cover the whole pipeline or only the packages is a product decision about what
"this build costs" means, and it decides E-3 and E-4 together.

**b. Is `works` a claim or a summary?** Today `AppBuildResult.works` requires every part to pass
*and* nothing app-wide, which is a strong and honest definition — while five of twenty-three
criteria on the canonical app are observed by nobody and are not part of it. Adding
`next build` (E-5), the generated tests (E-6) and data verification (E-7) each raise the bar and
each will turn some currently-green builds red. Whether that is a feature or a regression is the
product's call, and it should be made once, in advance, rather than three times in a row when each
gate lands.

---

*Written 2026-08-26 against the working tree at `00408d3`. Every code claim carries `file:line`
and was checked. The criteria census, the package sizing, the default estimate, the prompt-token
measurements, the interaction-suite run and the keepalive/reaper trace were produced by running the
real code, not read off it. Token figures are characters ÷ 4 and inherit that estimate's error bar
— `messages.count_tokens` is the correct instrument and no API key was available. Prices and cache
floors are Anthropic first-party current values. Web research was scanned 2026-08-26 and every
source carries its date; nothing was reproduced. Speculation is marked as speculation. Nothing here
is implemented.*
