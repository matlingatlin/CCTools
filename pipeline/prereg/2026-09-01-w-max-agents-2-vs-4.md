# Preregistration — W_MAX_AGENTS: keep 2, or raise to 4

- **Registered:** 2026-09-01, before any measurement of concurrency 4 exists on this box.
- **Registered by:** the coordinator session, at the user's instruction ("mät taket, 2 mot 4, när bygget är klart").
- **Amendment authority:** the user. A change made after data has been seen creates a NEW
  registration, not a revision; this one and its result stay in the record either way.
- **Status:** OPEN — no runs executed at time of writing.

## Why this is registered rather than just measured

The three conditions the method asks for are not equally strong here, and saying so is part of
the registration:

| Condition | Holds? |
|---|---|
| (a) a specific decision the number settles | **Yes** — the value of `W_MAX_AGENTS` in `pipeline/CONSTANTS.md`. |
| (b) someone sees the result and prefers an answer | **Yes** — I do. The user asked for "smarter and faster"; I have already argued the cap is probably wrong. That is exactly the bias this instrument exists to bind. |
| (c) reversal cost above a day of work | **Weakly.** Editing a constant is cheap to reverse. But a cap set too high degrades every future run *silently*, and a cap set too low costs wall clock on every future run, also silently — neither announces itself. |

The decisive reason is the record: the current value is labelled **`measured`** in CONSTANTS.md and
its citation (STATUS:21) **does not resolve**. An unverifiable measurement is how we got here. This
registration exists so the next value does not have the same provenance.

## Primary metric

**`wall_clock_total`** — seconds from dispatch of the first run to completion of the last, for a
fixed batch of **N = 8** identical dispatched runs, at a given concurrency level.
Direction: **lower is better.** Measured by the harness clock (`started` / `ended` per run, plus a
batch-level start/stop), not estimated.

One primary. Per-run duration and failures are **guardrails**, defined below — they can only block
the change, never carry it.

## Deciding threshold

Let `W2` = median `wall_clock_total` at concurrency 2, `W4` = median at concurrency 4.

**Raise the cap to 4 only if ALL THREE hold:**

1. **Gain:** `W4 ≤ 0.70 × W2` — at least a 30% reduction in batch wall clock.
   (Ideal speedup for 4 waves → 2 waves is 2.0×, i.e. `W4 = 0.50 × W2`. Demanding 0.70 tolerates
   substantial real contention while still requiring a gain worth changing a safety constant for.)
2. **No per-run degradation:** median per-run duration at 4 ≤ **1.5 ×** median per-run duration at 2.
   (This is the contention signal. A batch that finishes sooner while each run crawls is a box
   under strain, and the next heavier workload pays for it.)
3. **No failures:** **zero** failed, truncated, or usage-less runs at concurrency 4 across all
   valid batches.

**Any one of the three fails → the cap stays 2.** "Ambiguous", "close", "probably fine" and
"no measurable difference" all resolve to **keep 2**. The status quo wins ties by construction.

**A result of `W4 > W2`** (raising the cap makes it slower) is a real and reportable finding, not a
failed experiment: it would corroborate the `min(16, cores-2)` formula on a 4-core box.

## Sample size and stopping rule

- **Fixed n.** N = 8 runs per batch; **3 batches per concurrency level**; levels **alternated**
  (2, 4, 2, 4, 2, 4) so time-of-day, proxy weather and cache state cannot land on one arm.
  Total: 48 runs. No early stop, no extension.
- **Interim looks:** I may inspect runs *only* to detect invalid runs (below) and to confirm the
  harness is recording. I may **not** stop early, add batches, or change the workload on the basis
  of a favourable or unfavourable partial result.
- If a batch is voided, it is **re-run in the same alternation position**, and both the void and
  the reason are recorded.

## Workload, population and exclusions

- **The unit:** one headless `claude -p` run from a fresh scratch directory, given a fixed prompt
  that performs **2–4 real tool calls** (grep + read + a short structured answer) over a fixed
  file in this repo. This shape is chosen to match the observed field-reader profile
  (1–12 tool calls, network-bound model call plus local tool work), not to be cheap.
- **Identical across arms.** Same prompt, same file, same model, same scratch layout. The *only*
  thing that differs between arms is how many run at once.
- **Box state:** batches run only when the box is otherwise idle — **no build, no other loop, no
  other agents.** Load average at batch start is recorded; a batch starting above **0.50** is void.
- **Exclusion, stated before any data:** a run whose recorded token usage is absent is excluded
  from the per-run guardrail and **voids its batch for the primary** (a run that did not report is
  a run we cannot time honestly — see the `6.1 without/repeat 2` precedent, re-run for exactly this).

## Invalid-run criteria (independent of the result)

A batch is void, and re-run, if any of these is true — none of them can be judged from whether the
answer came out favourably:

- A proxy or API error (429, 5xx, TLS, connection reset) on any run in the batch.
- Any run terminated by timeout rather than completion.
- Load average at batch start > 0.50, or another agent/build observed running.
- The harness failed to record `started`/`ended` for any run.
- The model actually served differs between arms within the same alternation pair.

## What this measurement does NOT settle

Stated now so it cannot be quietly claimed later:

- **It does not measure 3, 8 or 16.** Only 2 vs 4. A win at 4 licenses 4, nothing above it.
- **It does not measure a heavier workload.** If the result is close to the 0.70 boundary in
  either direction, the honest report is that the workload was too light to decide, and the
  answer is INDETERMINATE → keep 2, not "no significant difference → raise it".
- **It does not measure write contention.** The cap also exists so parallel agents do not collide
  on git and shared files. That is a correctness constraint, not a throughput one, and no wall
  clock number can relax it. `parallel-execution-optimizer` owns that question separately.
- **It does not generalise off this box** (4 cores, this proxy, this date).

## Reporting rule

The summary opens with `W2`, `W4`, the ratio, and the verdict against the 0.70 threshold — not
with anything else. Every number not registered above is labelled **exploratory /
hypothesis-generating** in those words, in its own section. Operational findings (a bug, a
recording fault, a proxy failure) are reported plainly and acted on immediately — they are true
regardless of arm and are not hypotheses about the cap.

## Amendment 1 — 2026-09-01, before any run

The registration said an outcome "close to the 0.70 boundary in either direction" resolves to
INDETERMINATE, and did not say what close means. Left as prose, I would be choosing that number
after seeing the ratio, which is the exact failure the instrument exists to prevent. Fixed now,
while **no run has been executed on either arm**:

- **close = ratio in [0.65, 0.75]** (inclusive). A ratio in that band is reported as
  **INDETERMINATE — workload too light to decide**, and the cap stays 2.
- A ratio **> 0.75** is a clean *keep 2*. A ratio **< 0.65** clears the gain condition, and the two
  guardrails then decide.

Also fixed here, for the same reason:

- **Minimum valid batches: 3 per arm.** Fewer (after voids) → INDETERMINATE → keep 2. The
  registration set n but never said what happens if voids eat the sample.
- **Aggregation: median across valid batches** for the primary, and **median across all ok runs
  pooled within an arm** for the per-run guardrail. Stated because mean and median can straddle
  a threshold and picking between them later is bar-moving.

This is an amendment to an unstarted experiment, not a revision after data. The distinction is
the whole point, so: `pipeline/bench/runs/` is empty at the time of writing, and the commit
history shows it.

## Amendment 2 — 2026-09-01, after harness smoke, before any arm has data

A single smoke run (concurrency 1, written to `pipeline/bench/smoke/`, which `verdict.py` does not
read) found three harness defects. Recorded because two of them would have produced a **wrong
answer rather than an error**, which is the failure mode this project has hit repeatedly today:

1. **The workload did not run.** A headless run cannot read outside its own working directory, so
   it refused in ~6s having done nothing. Eight parallel refusals are almost pure dispatch
   overhead — no local work, therefore no contention — which would have read as a **large win for
   concurrency 4**. Fixed: the target file is copied into each scratch directory. A run reporting
   fewer than 2 turns is now recorded `no_work` and voids its batch.
2. **The model was not pinned.** `claude -p` served `claude-haiku-4-5`; dispatched readers do not.
   Fixed: pinned to `claude-sonnet-5` and recorded per run.
3. **The mismatch check itself was wrong.** `modelUsage` carries more than one key (the requested
   model plus an auxiliary), and the recorder read the first, reporting haiku for a run correctly
   served by the pinned model. That would have voided **every** batch on a mismatch that never
   happened. Fixed: the set is recorded and the pinned model must be a member.

**Model, and the limit it puts on the answer.** The benchmark runs on `claude-sonnet-5`, not on the
model dispatched readers actually use. The transfer is **asymmetric, and only one direction is
safe**: a cheaper model spends less time waiting on the API, so local work is a *larger* share of
each run and contention shows up *more* readily. Therefore **RAISE_TO_4 here transfers upward**
(a heavier model has strictly more waiting per unit of local CPU), while **KEEP_2 here does not
rule out a win on a heavier model** and must not be reported as if it did.

Added invalid-run criteria, before data: a run reporting `api_error_status`; a run completing in
fewer than 2 turns; a run served without the pinned model.

`pipeline/bench/runs/` is still empty. `selftest_verdict.py` is 18 checks, green, and every branch
of the rule — including each void condition — has a case that fails it.

## Amendment 3 — 2026-09-01, model changed to Opus 5, before any arm has data

**By instruction:** the benchmark runs on `claude-opus-5`, not `claude-sonnet-5`. Verified served,
not assumed: a smoke run at concurrency 1 reported `modelUsage` of
`['claude-haiku-4-5-20251001', 'claude-opus-5']` with the pinned model present.

**This retires the transfer argument in amendment 2 entirely.** Opus 5 is the model dispatched
readers actually run on, so the result needs no argument about transferring between models —
neither the safe direction nor the unsafe one. Amendment 2's asymmetry clause is void; it applied
only to the cheaper-model design it was written for. Both KEEP_2 and RAISE_TO_4 now speak directly
about the configuration the cap governs.

**One measured consequence, and it cuts against my own prior.** The API-wait share of a run's wall
clock differs sharply by model on this box:

| Model | `duration_api_ms` / `duration_ms` | Share not spent waiting on the API |
|---|---|---|
| `claude-sonnet-5` | 5079 / 10786 | ~47% local |
| `claude-opus-5` | 11917 / 15177 | ~22% local |

n=1 each, both taken under load with a build running, so both overstate the local share. Treated as
**weak, directional only**. What it says: the opus workload is *more* network-bound than the sonnet
one, so contention at concurrency 4 is **less** likely to bite — which makes a RAISE_TO_4 result
easier to obtain than under amendment 2's design. That is a reason to be *more* careful with the
result, not less, and the registered thresholds are unchanged: no number in this file moves
because of it.

**Cost, stated before the run:** the smoke run cost $0.168. 48 registered runs is roughly $8 plus
voids. Recorded so the sample size cannot later be trimmed for cost while the trim is presented as
a methodological choice.

`pipeline/bench/runs/` is still empty. `selftest_verdict.py` is 18 checks, green, with the pinned
model updated in its fixtures.

## Operational findings during the run — recorded before the verdict

Reported as operational, not exploratory: these are true regardless of which arm wins, so the
preregistration's own rule says to state them plainly and now rather than label them
hypothesis-generating.

**1. Start load is not equal across batches, and the asymmetry is structural.** A concurrency-4
batch ends the box at loadavg ~1.84; a concurrency-2 batch ends it at ~0.94. The driver waits for
loadavg <= 0.50 before each batch, which does equalise the *starting* figure — b1-c4 and b2-c2 both
began at exactly 0.481 — but it cannot equalise the decay path behind that figure, and **only the
very first batch ran from a genuinely cold box** (b1-c2 at 0.025). No concurrency-4 batch has ever
started cold.

Observed alongside it: the cold c=2 batch took 53.7s and the warm c=2 batch took 59.3s, a ~10%
spread on identical work. That is the same order as part of the effect being measured, so it is
not negligible.

**The direction of the resulting bias is not determined in advance and I am not claiming one.**
The cold batch belongs to the c=2 arm, which cuts toward that arm; every c=4 batch running warm
cuts the other way. Whether either dominates depends on which batch lands on the median, and
saying more than that after seeing the numbers would be exactly the reasoning this file exists to
prevent.

**What a clean design would have done**, recorded so the next run is better rather than to excuse
this one: wait to a fixed low threshold (loadavg <= 0.10) before *every* batch including the
first, so all six start from the same state, and randomise the arm order rather than strictly
alternating, so residual load cannot correlate with arm at all. The current 0.50 gate was written
to catch a busy box, not to equalise two arms, and it is doing the first job and not the second.

**This does not change any threshold.** The registered rule stands as written. The per-batch
loadavg at start is recorded in every batch file, so anyone can check the association themselves
rather than take this note's word for it.

## Result

**Verdict: RAISE_TO_4.** `W2 = 59.004s`, `W4 = 32.803s`, **ratio 0.556** against the registered
threshold of 0.70 — outside the close band (0.65–0.75) and therefore decidable. All three
registered conditions hold:

| Registered condition | Required | Measured | |
|---|---|---|---|
| Gain | `W4 ≤ 0.70 × W2` | **0.556** | pass |
| No per-run degradation | ≤ 1.5× | **1.11×** | pass |
| No failures at c=4 | zero | **0** | pass |

Produced by `pipeline/bench/verdict.py`, which applies the rule and does not measure;
`concurrency_bench.py` measures and does not decide.

### The batches

| batch | c | load at start | wall clock | per-run median |
|---|---|---|---|---|
| b1 | 2 | 0.025 | 53.703s | 12.6s |
| b1 | 4 | 0.481 | 32.803s | 15.6s |
| b2 | 2 | 0.481 | 59.302s | 14.1s |
| b2 | 4 | 0.484 | 36.596s | 15.9s |
| ~~b3~~ | ~~2~~ | ~~0.504~~ | ~~54.443s~~ | **VOID** — load above the registered ceiling |
| b3 | 4 | 0.454 | 31.536s | 14.1s |
| b3r | 2 | 0.436 | 59.004s | 13.9s |

56 runs, all clean, $9.18. One batch voided on the invalid-run criteria and re-run in the same
alternation position under the identical wait rule — deliberately not a stricter one, which would
have given that batch a colder start than the other two in its own arm.

### Robustness against the confound registered before the result — EXPLORATORY

Both checks below are **exploratory and hypothesis-generating**: neither is a registered analysis.
They are reported because the confound they test was written down before the numbers existed, and
leaving it unexamined would be worse than labelling it.

- The one cold batch (b1-c2, 53.703s) is the **minimum** of its arm, not the median, so it did not
  pull the c=2 median down. Dropping it entirely gives `W2 = 59.153`, ratio **0.554** — unchanged.
- Counting the voided b3-c2 anyway gives `W2 = 56.723`, ratio **0.578** — still a clear win.

Neither the cold start nor the void manufactured the result.

### What this does and does not license

**Does:** `W_MAX_AGENTS = 4` for this workload on this box, this model, this date.

**Does not**, restated from the registration so it cannot be quietly widened later:

- **It does not measure 3, 8 or 16.** A win at 4 licenses 4 and nothing above it.
- **It does not relax write contention.** The cap also exists so parallel agents do not collide on
  shared files, which is a correctness constraint no wall-clock number can speak to. What protects
  that here is the standing rule that the coordinator commits and agents produce, not this number.
- **It does not generalise off this box** (4 cores, this proxy, this date).

### The mechanism, and what it says about the old value — EXPLORATORY

**Exploratory:** across all 56 runs the median run spent **73% of its wall clock waiting on the
API**. The `min(16, cores-2)` formula that produced the old value of 2 models CPU contention on a
4-core box. A workload that is three-quarters network wait is not what that formula describes,
which is consistent with 4 agents fitting comfortably where the formula predicted 2 would not.
Stated as a mechanism the result is consistent with, not as a measured cause: this benchmark did
not manipulate the API-wait share, so it cannot establish it.

### Amendment discipline

Three amendments were made, all **before any arm had data**: the numeric close band and minimum
sample (1), the harness fixes and model pin (2), the change to Opus 5 (3). No threshold moved
after a number existed. The load-asymmetry confound was recorded with three batches still to run.
