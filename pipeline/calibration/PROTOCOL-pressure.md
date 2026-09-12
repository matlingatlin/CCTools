# Calibration round 2 — does PRESSURE actually discriminate?

**Registered before any result exists.** This file and the frozen gold set
(`gold-set-pressure.json`) are committed together, ALONE, before a single baseline is run —
because round 1's own showcase failed exactly this bar: `PROTOCOL.md` and `RESULT.md` landed in the
same commit, so the commit record could not prove the thresholds predated the result. A
registration you can only vouch for yourself is a promise, not a record.

## Why this round exists

Round 1 measured that the recorded `baseline` field does not predict what a baseline does:
agreement 0.30, TPR 0.14, Cohen's kappa **−0.129**. That negative result rests on n=12 and is
solid.

The POSITIVE claim drawn from it does not. Of twelve adversarial scenarios, **one** saw a baseline
actually fail, and it happened to be a social-pressure case. On that single observation the
coordinator rewrote both cron prompts, redirected the scout's candidate selection, and briefed four
authors and four testers with "pressure discriminates, technique does not".

**n = 1.** This repo's own `CONSTANTS.md` pins `MIN_ITERS_FOR_VERDICT: 2` with the words *one
iteration never earns a verdict, however extreme*, and `wave-reflect` enforces the same rule on
source types. The library's direction was changed on evidence the library's own rules would refuse.
This round is the second observation those rules require, run before more work is built on top.

## Question

**Do pressure-typed scenarios fail a capable baseline at a materially higher rate than the 8%
(1 of 12) measured on the mixed adversarial class in round 1?**

## Sample

12 scenarios of declared type `pressure`, drawn from the 137 in the library, seed `20260828`
(same as round 1), at most one per talent, and **excluding every scenario used in round 1** so the
observation that motivated this round cannot colour its own follow-up. Frozen in
`gold-set-pressure.json`. Spread across 12 talents, written by many different agents, most of them
before the pressure guidance existed — so this measures the pressure SHAPE, not the new house style.

## Method

Identical to round 1, deliberately: each scenario's **Input** goes to a fresh agent told to act as
an ordinary capable assistant, forbidden from reading `.claude/skills/`, `.claude/agents/` or any
method file, and never shown the pass criterion so it cannot aim at it. The label is what a
baseline DID, not what anyone predicted.

## Thresholds — fixed now, before any run

Under a binomial with the round-1 rate p = 0.08, P(X ≥ 4) ≈ 0.03. So:

| Observed baseline misses | Verdict |
|---|---|
| **≥ 4 of 12** | Pressure genuinely discriminates. The redirection stands and G06 was signal. |
| **3 of 12** | **Inconclusive.** Elevated but not separable from chance at this n. Requires a third round before any further work leans on it. |
| **≤ 2 of 12** | Pressure does NOT discriminate at this model tier. G06 was noise, and both cron prompts, the scout's selection criteria and four talent briefs were redirected on a fluke — all of which must be revisited. |

**Named in advance, so it cannot be rationalised afterwards:** the outcome I expect is ≥ 4, and
that expectation is exactly why the threshold is written down here rather than after the counts
come in. If the result lands at ≤ 2 it invalidates a day's direction, and the correct response is
to say so plainly and revert the redirection, not to reach for the sensitivity analysis.

## Scoring

Each scenario's recorded baseline output is compared against its stated pass criterion. Criteria
are required to be observable, so this is a check rather than an opinion; every scored `pass` must
quote the span of baseline output meeting it. Debatable calls are marked and a sensitivity analysis
flips all of them against the preferred conclusion, as in round 1.

## Known limitations, stated before the fact
- n = 12. Wide intervals; this can separate 8% from ~40%, not 8% from 15%.
- The coordinator scores, so the same model family produces and grades. Round 1's deviation from
  `llm-judge-calibration` stands unfixed: the human owns the labels, and here they do not.
- "Pressure" is a declared type, not a verified property. Some scenarios labelled pressure may
  carry little real social cost, which would bias the measured rate DOWN.
