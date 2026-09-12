---
name: spend-ceilings
layer: E
phase: build-time
status: written
description: Design a cost cap, a timeout or a usage meter so it cannot quietly fail open. Use when adding or reviewing a spend limit, a token budget, a rate cap, a build timeout, a monthly allowance, or anything that bills a user. Use when a price is unknown for a model, when a run is cancelled or dies partway and someone has to be charged for what was actually used, when a limit needs an escape valve, when picking a timeout number, when a meter can show zero for two different reasons, and when deciding whether a cap should stop the work or merely warn. Also use when a cap is checked after the call it was meant to prevent, when an estimate is about to be frozen and shown to someone as a price, or when a dashboard would render a missing measurement as a good one.
---

# spend-ceilings

A cap that returns zero for the case it does not understand is not a cap. A meter that shows zero
when the pipe broke is worse than a blank. And a ledger that loses the run that hit its ceiling
under-reports exactly the bill somebody will dispute.

This skill is five decisions for any limit or meter. It does not decide what our ceiling should be
— that number is the user's approved estimate, and changing how it is derived is an ADR.

---

## 1 · Source

Seven findings mined on **2026-08-26** and triaged in `docs/triage/LAYER-E-TRIAGE.md`, plus this
repository's own verified defects, which are the sharper teachers.

| Mechanism | Where it was read |
|---|---|
| An unpriced model returns `0` — *the fail-open in the spend ceiling* | `docs/mined/PASS2-GSTACK-TESTS.md:133` (**inverted**: leave the behaviour, take the warning) |
| Override is a reason string landing in an audited JSONL with branch and commit | `docs/mined/PASS2-GSTACK-TESTS.md:95` |
| A relative-ratio regression **and** an absolute hard cap, both, purposes stated | `docs/mined/PASS2-GSTACK-TESTS.md:112` |
| A timeout floor derived from a live census, margin itemised | `docs/mined/PASS2-GSTACK-TESTS.md:146` |
| Never render a missing value as a good value | `docs/mined/PASS2-GSTACK-TESTS.md:706` |
| Limits enforced outside the model; audit refused and halted runs, not only successful ones | `docs/mined/PASS2-ECC-SKILLS.md:670` |
| A cost estimator publishes its error band, its calibration corpus and its expiry condition | `docs/mined/OTHERS-MINED.md:727` |

**Ours, verified at file and line** (`docs/as-built/LAYER-E-BUILD.md` §4b, §6;
`docs/next/LAYER-E-BUILD.md` §1.1c–f, §2.2):

- The good part: `Spend` is one build-scoped accumulator, enforced at **one** place
  (`relay.py:264`), computed from the estimate the user actually approved —
  `ceilingFor(spec) = estimate.cost_usd.high × 1.5` (`build.service.ts:495`) — and *"a spec with no
  estimate gets none: a ceiling invented here would be a number nobody agreed to."*
- **It is checked after the call it should have stopped.** `:256` runs the completion, `:259` prices
  it, `:264` raises. `Spend`'s own docstring says *"checked before each one"*, which the code does
  not do.
- **The build that hits its ceiling is the one the ledger under-reports most.** `BudgetExceeded`
  skips `spend.add(cost)` and unwinds past `_generate`'s local accumulator; `_write_attempt`'s budget
  branch builds `_Written(...)` with no `cost_usd`, which defaults to `0.0` (`loop.py:550`). That
  zero travels to the `package` event, to `spentUsd +=`, and into `usage_event`.
- **`Spend.spent_usd` — the only correct running total in the system — is never read.** Four
  references repo-wide, all inside `relay.py`.
- **The estimate prices output only** (`input_cost_per_mtok` is unread in `estimate_plan`) while the
  relay prices both halves, and input was *"a third to a half of the real invoice"*. The number the
  user approves, the range they see, and the ceiling that stops their build all rest on that model.

---

## 2 · The five decisions

### D1 · Where is it enforced, and when?

**Outside the model, in one place, before the spend happens.**

- *Outside the model*: a limit expressed as prompt text is a request. A limit in the caller is a
  limit.
- *One place*: our single enforcement point is the reason a seven-package build no longer authorises
  the ceiling fourteen times over. Keep it.
- *Before*: a check after the call has already paid for the call. The bound is computable before —
  token-count the assembled prompt, add the output cap at the card's rate, refuse if the bound
  crosses the ceiling. Price the bound at an observed output ratio rather than the theoretical
  maximum, or short calls get refused by their worst case. Counting tokens is free on the Messages
  API; the prompt is fully assembled before the call.

### D2 · What happens when the price is unknown?

**Refuse, or bound pessimistically. Never zero.**

A zero for an unpriced model disables the cap in exactly the condition the cap exists for — a new
model id, a price change, a provider we have not carded. Take the mined source's `as_of` stamp per
row and its warn-once; leave its `return 0`.

The same rule generalises: **an unknown is not a good value.** A meter has four states, not one —
`trusted / unverified / unknown / error` — and *a zero from a broken pipe reads as good news*. Our
`cost_usd = 0.0` on the budget branch is this bug in our own code.

### D3 · Two instruments, or one?

**Both, and say what each is for.**

| Instrument | Catches | Set it |
|---|---|---|
| **Relative** — this run against the last comparable one | drift, a slow regression, a prompt that grew | with a noise floor, first-run grace, and same-branch-only comparison |
| **Absolute** — a hard ceiling | runaway: an infinite retry, a price change, a prompt-blowup bug | high enough that legitimate growth never trips it. *"NOT to gate legitimate scope growth"* |

Neither substitutes for the other. A relative check alone ratchets a bug into the baseline; an
absolute cap alone never notices a doubling that stays under it.

The same shape applies in the other direction — **a floor as well as a ceiling.** A measurement that
collapses to near-zero is a broken producer, not a saving, and only a floor catches it.

### D4 · Where does a timeout come from?

**Derive it. Never choose it.**

A timeout must be a function of the work planned — the plan's worst case × a margin, computed from a
live census, with the margin itemised rather than rounded. A constant goes stale silently every time
upstream grows, and a watchdog set below the real worst case *"kills a healthy run mid-flight and
the tail shards report never-started"* — truncation by configuration, paid for.

Two of our own numbers show what a chosen timeout does. One codegen pass may take
`CODEGEN_TIMEOUT_S = 900.0` with four passes, so a package may legitimately be silent for **up to
sixty minutes** — against a heartbeat grace of **fifteen**. And the reaper sets `status: "failed"`
while the in-flight cancel check reads `"cancelled"`, so **a reaped job does not stop the engine**:
the user is told the build stopped reporting, and it keeps running and keeps spending
(`docs/next/LAYER-E-BUILD.md` §1.1h). A derived timeout would not have produced that pair.

### D5 · What is recorded, and what may override it?

- **Every run is metered — refused, cancelled and failed, not only successful.** Metering that counts
  completed builds cannot answer a disputed bill. We already do this on the API side
  (`meterSpend` on cancellation and failure); the engine-side gap is D2's zero.
- **A partial is recorded as a partial.** Attach the accumulated cost to the exception. It is
  strictly more honest than zero and costs nothing to be right about.
- **An override is a reason string, not a boolean**, and it lands in an append-only log with
  provenance — timestamp, scope, reason, branch, commit. *"A hard cap with no escape valve becomes
  operationally hostile. An escape valve with no audit becomes 'everyone overrides everything and we
  lose the gate.'"* Booleans get set once and never unset; a reason gets read at review.
- **The audit write is best-effort.** An observability layer must not be able to fail what it
  observes.
- **An estimator publishes its error band, its calibration corpus, and the condition under which the
  calibration expires.** Ours is calibrated against three real runs and says so — but those runs
  predate the change that made the relay price both halves of the bill, so the ratio it was tuned
  against is not the ratio that now obtains. **That expiry condition is exactly the thing to publish
  and did not exist to be checked.**

→ `references/meters-and-ledgers.md` for the record shapes and the four meter states.

---

## 3 · Limits

| Claim | Status |
|---|---|
| These record shapes exist and are quotable | Supported — each row in §1 names a file and a line in `docs/mined/` |
| The mined caps' *numbers* transfer | **No.** `$200` / `$500` / `2×` / `5-call noise floor` are their workloads. The source itself publishes the history of every constant precisely so it can be argued with; copying the value and dropping the derivation is the error it warns against |
| Our defects are real | Supported at file and line, `docs/next/LAYER-E-BUILD.md` §1.1c–f |
| Checking before the call is strictly better | **Not free.** It trades a bounded overshoot for a risk of over-refusal, and it needs a token count on an assembled prompt. The two fixes are separable and the ledger fix has no downside at all; the check-before fix has one |
| A pessimistic bound is safe | **Only as a stop.** A pessimistic bound shown to a user as a price is a different and worse error. Bound the *cap*, not the *quote* |

**What this skill does not decide:** what our ceiling multiplier should be; whether the estimate
should price input; whether a workspace allowance is the right second instrument; whether the engine
should ever exceed a ceiling by ruling rather than stopping (see `build-loop-stops` D3). Each is an
ADR — `docs/triage/LAYER-E-TRIAGE.md`.

**The honesty rule:** this skill justifies the *shape* of a limit — enforced outside the model, once,
before the spend, with no zero-valued unknown, two instruments, a derived timeout, and an audited
override. It does not justify any particular number, and nobody has measured that a limit shaped
this way saves money.

---

## 4 · Eval

**E1 · The unpriced model.** Price a call with a model id absent from the table. Assert the result is
a refusal or a pessimistic upper bound. A zero, or a silent pass, fails. This is the mined finding
inverted and it is the single most important case here.

**E2 · The ceiling stops the call that would cross it.** Assert no completion is issued once the
computed bound crosses the ceiling. A test that only asserts the *next* call is blocked passes
today's code and misses the defect.

**E3 · The partial survives.** Drive a run to its ceiling mid-way through a multi-part unit. Assert
the recorded cost equals the work actually completed. A recorded `0.0` fails. This is
`loop.py:550` as an eval.

**E4 · Four meter states.** Assert a meter can distinguish *measured zero*, *not measured*, *unknown*
and *error*, and that a display path exists for each. One zero for all four fails.

**E5 · Refused and cancelled runs are metered.** Cancel a run and refuse a run. Assert both produce a
usage record.

**E6 · The override is auditable.** Set an override. Assert the log line carries a reason string,
branch and commit, and that no boolean path can raise the cap without one. Then make the log
unwritable and assert the run still succeeds.

**E7 · The timeout is derived.** Assert the timeout is computed from the current plan and that
growing the plan grows it. A constant fails. Assert the derived value is at or above the plan's worst
case, with the margin named.

**E8 · Both instruments present.** Assert a relative check and an absolute cap both exist, each with
a one-line statement of what it is for, and that the relative one has a noise floor and first-run
grace so a first run cannot pass vacuously.

**E9 · The estimator publishes its expiry.** Grep the estimator for its calibration corpus and the
condition that invalidates it. Assert a change to the pricing path is one of them.

---

## 5 · When this skill is the wrong tool

- **Deciding when a loop stops for reasons other than money.** `build-loop-stops`.
- **Deciding what a gate reports.** `gate-verdicts` — though D2's *never render a missing value as a
  good value* is the same rule seen from the meter's side.
- **Choosing a pricing strategy or what to charge.** That is a product decision.
- **Optimising cost.** Prompt caching, batching and pass counts are ADRs with measurements attached,
  not limits.

---

*Written 2026-08-26 from `docs/mined/` read at source. No mechanism here has been measured on Scio.
Code claims trace to `/home/user/hello-world` through `docs/as-built/LAYER-E-BUILD.md` §4b and
`docs/next/LAYER-E-BUILD.md` §1.1 and §2.2, which cite them at file and line.*
