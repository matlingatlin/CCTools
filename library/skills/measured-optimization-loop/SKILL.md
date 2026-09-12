---
name: measured-optimization-loop
description: "Use when improving performance, latency, throughput, cost, token usage, or an eval/benchmark score and you want measured gains instead of guessed ones — establishes a baseline, tries one hypothesis at a time, and gates each candidate on a correctness check plus a promotion threshold before keeping it. Triggers on \"make it faster\", \"optimize\", \"reduce latency/cost\", \"speed up the hot path\", \"beat the baseline\", \"tune the prompt/config for a higher score\", A/B or variant comparison, and profiling-then-improving loops. Not for finding why something is broken (use systematic-debugging), for one-shot code cleanup with no metric (use simplify), or for designing the eval/benchmark itself (use eval-harness). NOT for fixing the deciding metric, threshold and stop rule in writing BEFORE the result is visible (use preregistered-decision-rule)."
---

Improve a measurable target by disciplined experiment: baseline first, one hypothesis per variant, and two gates (correctness, then promotion) so only real, verified wins survive.

## When to use
- You have (or can define) a single numeric metric and want it better: runtime, p95 latency, memory, cost per call, tokens, an eval score.
- Regressions are unacceptable, so every change must prove it beats what came before.

## When NOT to use
- The thing is wrong, not slow — debug it first.
- No metric exists and none can be defined — you are guessing, not optimizing.
- You only need the harness/eval that produces the number — build that first (eval-harness).
- The change is a pure readability cleanup with no metric to move (simplify).

## Steps
1. **Define the target.** Name one primary metric and its direction (lower/higher is better). State the promotion threshold up front (e.g. "must beat baseline by >=5% on the metric, with correctness unchanged"). Note secondary metrics that must not regress.
2. **Fix the measurement.** Pin the workload, inputs, seed, and environment so runs are comparable. Decide how many repeats and which summary (median/p95, not a single noisy run).
3. **Establish the baseline.** Run the current version under the fixed measurement. Record the number and the correctness result. This is the incumbent that every candidate must beat.
4. **Form one hypothesis.** Write a single specific change and why it should move the metric ("cache X to cut repeat computes"). One lever per variant — never bundle changes, or you cannot attribute the result.
5. **Build the variant.** Implement only that change against the baseline.
6. **Correctness gate.** Run the correctness check (tests / eval oracle). If it fails, discard the variant — a wrong-but-fast result is not a win. Do not tune the correctness check to pass.
7. **Promotion gate.** Measure the variant the same way as the baseline. Promote only if it clears the threshold AND no secondary metric regresses. Ties and sub-threshold gains stay unpromoted.
8. **Promote or discard.** If promoted, the variant becomes the new baseline; record the delta and the hypothesis that worked. If discarded, record why so it is not retried.
9. **Repeat** from step 4 with the next hypothesis until gains fall below the threshold or the budget is spent.
10. **Report.** Summarize baseline -> final metric, each promoted step and its delta, and what was tried and rejected.

## Rules
- One hypothesis per variant. Bundled changes make results unattributable.
- Correctness gate before promotion gate, always. Never trade correctness for speed.
- Compare like with like: same inputs, seed, repeats, and environment as the baseline run.
- A win is a threshold-beating, correctness-passing, non-regressing measured delta — not a plausible-looking diff.
- Keep the incumbent baseline; only a promoted variant replaces it.
- Record every attempt (promoted and rejected) with its number, so the loop is auditable and reruns are reproducible.
- Treat noise honestly: if the delta is within run-to-run variance, it is not a win — increase repeats or reject.
- State the threshold before measuring, not after — a threshold chosen to fit the result proves nothing.
- Method only: this skill does not run benchmarks, install profilers, or make network/CLI calls for you, and installs no auto-run hooks.
