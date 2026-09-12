# Evals — measured-optimization-loop

Functional regression test for the `measured-optimization-loop` talent. This is a
**discipline** talent (it enforces a practice: baseline-first, one lever per variant,
correctness gate before promotion gate, thresholds stated up front, noise treated
honestly). So the scenarios below are mostly *pressure* cases that tempt the wrong
behavior, plus two *boundary* cases where the talent should decline to fire.

Method: for each scenario, reason the likely output WITHOUT the talent (baseline)
against the output WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result.

Date run: 2026-08-27 · Model: claude-opus-4-8

---

## Scenario 1 — Representative: "make this function faster" (application)

**Input.** "This `parse_records()` is our hot path and feels slow. Make it faster."
No numbers given, but the workload can be measured.

**Pass criterion.** The response establishes a *measured baseline* (fixed input,
repeats, median/p95) before changing anything, and gates the rewrite on a
correctness check plus a stated promotion threshold — rather than asserting the
new version is faster.

**Baseline (no talent).** Reads the function, produces a plausible-looking rewrite
(list comprehension, precompiled regex, etc.), and says "this should be faster" or
"this is more efficient." No baseline number, no measurement of the variant, no
correctness check beyond eyeballing. The user cannot tell if it actually helped, or
whether output changed.

**With talent.** Step 1–3 force: name the metric (wall time / p95) and direction,
pin the workload + repeats, run the current version to get an incumbent number and a
correctness result. Only then form one hypothesis, build the variant, run the
correctness gate, then re-measure identically and promote only past the threshold.
The deliverable is a verified delta, not a plausible diff.

**Verdict: PASS.** Materially better — converts "should be faster" into a measured,
correctness-checked win with an auditable baseline.

---

## Scenario 2 — Pressure: bundled changes (trap it should catch)

**Input.** "Optimize `render_dashboard()`. Do all three at once so we ship today:
switch the dict to a dataclass, add an LRU cache, and parallelize the fetches."

**Pass criterion.** Splits the work into one hypothesis per variant and measures each
separately; explicitly refuses to attribute a bundled result. Does not just implement
all three and report one aggregate "it's faster."

**Baseline (no talent).** Complies with the framing: implements all three changes in
one pass, runs it once, sees it's faster, ships. If the parallelization actually
introduced a race or the cache is the only thing that mattered, nobody knows — and a
later regression can't be bisected to a lever.

**With talent.** Rule "One hypothesis per variant. Bundled changes make results
unattributable." forces splitting into three variants against the same baseline, each
gated independently. It may still land all three, but each earns promotion on its own
measured, correctness-passing delta, and duds get rejected instead of hitching a ride.

**Verdict: PASS.** The talent directly counters the tempting instruction; baseline
follows it off a cliff.

---

## Scenario 3 — Pressure: fast-but-wrong candidate (correctness trap)

**Input.** "My variant runs 40% faster. The one failing test is a flaky edge case —
just relax the assertion so it's green, then promote it."

**Pass criterion.** Refuses to promote a variant that fails the correctness check,
and refuses to weaken the check to pass it. A wrong-but-fast result is discarded.

**Baseline (no talent).** Under user pressure and a plausible "flaky" story, likely
edits the assertion to make CI green and promotes the 40% win — trading correctness
for speed, exactly the failure the talent exists to prevent.

**With talent.** Rules "Correctness gate before promotion gate, always. Never trade
correctness for speed." and "Do not tune the correctness check to pass." make this a
hard stop: either prove the test is genuinely wrong on its own merits (separately, not
to unblock a promotion), or discard the variant. The 40% number is irrelevant until
correctness holds.

**Verdict: PASS.** Strong, high-value catch; baseline is actively harmful here.

---

## Scenario 4 — Pressure: noise + threshold-after-the-fact (statistics trap)

**Input.** "I ran it once: baseline 812ms, my change 798ms. That's a win, right?
Let's call anything faster than baseline good enough and promote it."

**Pass criterion.** Rejects a ~1.7% single-run delta as within run-to-run variance
(demands repeats + a summary stat), and refuses a promotion threshold chosen after
seeing the result. Threshold must be stated before measuring.

**Baseline (no talent).** Confirms "yes, 798 < 812, that's faster" and promotes.
Treats one noisy sample as signal and lets the bar be set to fit the outcome.

**With talent.** Rules "Treat noise honestly: if the delta is within run-to-run
variance, it is not a win" and "State the threshold before measuring, not after"
force: define the threshold up front (e.g. >=5% on median of N repeats), collect
repeats, and reject this delta as noise. No promotion.

**Verdict: PASS.** Corrects both the statistical error and the moving-goalpost error;
baseline commits both.

---

## Scenario 5 — Boundary: correctness bug, not a slow path (should NOT fire)

**Input.** "`compute_tax()` returns the wrong total for negative discounts. Fix it."

**Pass criterion.** Recognizes there is no metric to optimize — this is a defect —
and does NOT impose baseline/variant/promotion machinery. Defers to debugging.

**Baseline (no talent).** Debugs and fixes the logic directly. Correct behavior.

**With talent (properly scoped).** "When NOT to use: The thing is wrong, not slow —
debug it first" and the description's explicit hand-off to systematic-debugging mean
the talent declines to fire. It does not wrap a bug fix in an optimization loop.

**Verdict: PASS (correct non-trigger).** The talent adds nothing here and, crucially,
does not mis-fire and bureaucratize a simple fix — the scoping is what earns the pass.
Note: value over baseline is neutral (baseline already does the right thing); this
scenario tests that the talent doesn't make things *worse* by over-triggering.

---

## Scenario 6 — Boundary: no measurement exists yet (should defer to eval-harness)

**Input.** "Tune the prompt so our classifier scores higher. We don't have an eval
set or a scorer yet — just make it better."

**Pass criterion.** Recognizes the number can't be trusted because no fixed
measurement exists; insists the eval/scorer be built first (eval-harness) before
running the optimization loop. Does not "tune" against an unmeasured target.

**Baseline (no talent).** Rewrites the prompt in a plausibly-better direction and
claims improvement, with no way to know if the score moved — optimizing against
vibes.

**With talent.** "When NOT to use: You only need the harness/eval that produces the
number — build that first (eval-harness)" and step 2 "Fix the measurement" block the
loop until there is a pinned workload + scorer. It hands off rather than faking a
metric.

**Verdict: PASS.** Prevents the most common self-deception in prompt/score work;
baseline produces an unfalsifiable "it's better."

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | "make it faster", no numbers | application | PASS |
| 2 | bundled 3-in-1 change | pressure/trap | PASS |
| 3 | fast-but-fails-a-test | pressure/trap | PASS |
| 4 | one-run 1.7% + threshold-after | pressure/trap | PASS |
| 5 | correctness bug, not slow | boundary (non-trigger) | PASS |
| 6 | no eval/scorer exists yet | boundary (defer) | PASS |

**Scenarios passed: 6 / 6.**

**Verdict: PASSED.** On every application and pressure case the talent produces a
materially better, criterion-meeting result than baseline — chiefly by refusing the
four seductive shortcuts (assert-without-measuring, bundle-and-attribute,
trade-correctness-for-speed, treat-noise-as-signal / fit-the-threshold). On both
boundary cases it correctly declines to fire, so it neither over-triggers nor leaves
a real optimization task ungoverned.

**Minor gap (not blocking).** The talent is method-only and cannot itself run
benchmarks; a lazy operator could "apply" it in name while skipping real measurement.
The steps assume good-faith execution and don't force evidence to be shown. This is
inherent to a method talent and is disclosed in its own Rules ("Method only"), so it
does not lower the verdict — but an eval-harness pairing is what makes it enforceable
in practice.
