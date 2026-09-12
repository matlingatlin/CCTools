# skill-measure — round 2

5 questions × 2 arms × 2 repeats = 20 answers, graded blind, expectation set rewritten
after round 1. **The cost clause is live this round.**

## Verdict: ship — against the full default rule, cost included

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats | pass | |
| no correctness regression | pass | |
| tokens | pass | 66,724 vs 64,874 = **1.03×** (cap 1.20×) |
| tool calls | pass | 2.0 vs 2.0 = 1.00× |
| ≥1 win surviving both repeats | pass | **Q4**, in both |

Score: with 4/5 and 3/5 · without 3/5 and 2/5. Nothing regressed in either repeat.

## The result is real and it is narrow: one clause is doing all the work

Q4 is the grader-calibration question, and it is the only thing that separated the arms
in either repeat. Both graders located the same discriminator independently:

> *"only three items separated them at all — same-turn paired launch and a deterministic
> row/column grader in question 2, and a single-defect calibration specimen in question
> 4."* — r1

> *"one answer specified a single specimen altered in exactly one place while the other
> seeded several defects across three or four outputs, which cannot isolate the defect
> class."* — r2

Everything else the baseline already had: refusing to decide on n=1, computing the delta
rather than calling it "higher", refusing to let a pass-rate win discharge a cost clause,
refusing a win that did not repeat. **17 of 20 ruling-pairs in r1 came back met for both
arms.**

So the honest headline is not "skill-measure works". It is: **the model already holds most
of measurement discipline, and does not spontaneously calibrate its grader.** That one gap
is worth a skill. The rest of the file has not been shown to add anything.

What that does *not* establish: whether the undifferentiated parts are redundant or merely
untested by these expectations. Several of the shared passes sit on expectations the
graders call near-unfailable, so "both arms met it" is not evidence the baseline knows it.
Those are two different states and this run cannot separate them.

**Recommendation: ship, then cut to what earned its place — and re-measure the cut.**
A skill whose demonstrated contribution is one clause should not carry five sections of
context on every invocation. Shortening it is a change to the artefact, so it goes back
through the same rule rather than being trimmed on judgement.

## The expectation set is better than round 1's and still has two defects

Round 1's disease — expectations satisfiable by recital — is largely gone. Two new ones,
both mine, both found by the graders:

**Paraphrase pairs.** Several questions contain two expectations that cannot be satisfied
independently: *"does not treat missing as a pass"* and *"reports it as unmeasured"* are
one behaviour scored twice. The effective number of independent measurements in r2 is
about **nine, not fifteen** — so a single competence counts twice and a single failure
fails twice, which distorts a per-question all-or-nothing score in both directions.

**One expectation in tension with its own question.** Q1's *"declines to give a go/no-go"*
is unusable as written: the question asks for the go/no-go, both answers open with
"No-go", and both then say the data cannot decide. It is met and contradicted inside the
same answer. What I meant was *"does not treat the data as sufficient"*, and that is what
it should say.

The graders also named what to copy: the items with **a specific failable quantity or
mechanism** — "exactly one planted defect", "same turn, fresh sessions", "the grader is a
script counting rows". Those are the three that discriminated.

## What was not checked

The grader was **not calibrated against a planted defect** — phase 6.3, still v2. Which is
precisely the gap Q4 measures. The measurement of grader blindness was made by a grader
whose own blindness is unmeasured, and that circularity is not resolved here.

Part of the +2.8% token delta is the method text the `with` arm was handed and the other
was not; `subagent_tokens` does not separate input from work.
