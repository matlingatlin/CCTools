---
name: build-loop-stops
layer: E
phase: build-time
status: written
description: Decide when an autonomous build or repair loop stops, what feeds each round, and what it records when it gives up. Use when writing or reviewing a loop that retries, regenerates, repairs or reviews until something is good enough. Use when picking an iteration cap, when a loop keeps producing the same failure, when a fix creates more errors than it resolves, when deciding whether a loop should ask a human or decide for itself, when a retry needs a different model or a fresh context, when a loop has no defined way to give up, when someone proposes more self-review passes, or when a run has to wait for a sandbox or a preview to become ready. Also use when deciding what a round writes down so the next round does not repeat it.
---

# build-loop-stops

A loop that retries until a counter runs out spends its last attempt whether or not the previous
one moved anything. A loop with no defined terminal state reports "failed" for four different
situations that need four different responses. And a loop whose extra rounds get no external
feedback is paying for self-correction, which the literature says does not work.

This skill is the four decisions a loop has to answer: **what feeds a round, when it stops, what
happens at the boundary, and how the stop is reported.** It does not decide how many rounds our
loop should run — that is an ADR with a measurement behind it.

---

## 1 · Source

Two kinds, kept apart on purpose.

**Measured results, on repair loops** — already sited in `docs/next/LAYER-E-BUILD.md` §2.1:

- Huang, Chen, Mishra, Zheng, Yu, Song & Zhou, [*Large Language Models Cannot Self-Correct Reasoning
  Yet*, ICLR 2024](https://arxiv.org/abs/2310.01798) — *"LLMs struggle to self-correct their
  responses without external feedback, and at times, their performance even degrades after
  self-correction."*
- Kamoi, Zhang, Zhang, Han & Zhang, [*When Can LLMs Actually Correct Their Own Mistakes? A Critical
  Survey*, TACL 2024](https://arxiv.org/abs/2406.01297) — *"no prior work demonstrates successful
  self-correction with feedback from prompted LLMs"*; *"self-correction works well in tasks that can
  use reliable external feedback."*
- Kiecker, Reichmann, Kang, An & Grunske, [*Is Three the Magic Number? An Empirical Evaluation of
  LLM-Based Repair Loops*, July 2026](https://arxiv.org/html/2607.05197v1) — 0–10 repair steps across
  six tool/dataset combinations; the first 3–4 iterations capture the vast majority of the achievable
  gain, and by step 3 the increment is *"single digit percentages or below"*.

**Conventions, mined from eight repositories on 2026-08-26** and triaged in
`docs/triage/LAYER-E-TRIAGE.md`: the fed repair loop and plateau stop (`docs/mined/ECC-SKILLS.md:270`,
`ECC-AGENTS.md:430`), rulings-not-stalls and the fix-round circuit breaker
(`OTHERS-MINED.md:324`), non-convergence detectors (`PASS2-ECC-RULES-COMMANDS.md:690`), the
three-strike and blast-radius gates (`PASS2-GSTACK-SKILLS.md:188`), the thrash score
(`PASS2-GSTACK-SKILLS.md:255`), sentinel completion tags (`PASS2-FOUR-REPOS.md:169`), fact-forced
repair (`PASS2-ECC-SKILLS.md:339`), and condition-based waiting (`OTHERS-MINED.md:396`).

**The defect this repository already has, verified at file and line**
(`docs/next/LAYER-E-BUILD.md` §2.1): two loops, and the money is in the wrong one.

| Loop | Feedback it receives | Cap | Default |
|---|---|---:|---|
| relay passes (`relay.py:148-167`) | none — only the prompt and its own previous answer | `MAX_PASSES = 4` | **4** |
| repair attempts (`loop.py`) | seven validation agents, console classifier, interaction runner, critique | `max_attempts` | 3 |

`max_attempts = 3` is exactly right and now has a citation. `codegen_passes = 4` is the one without
evidence behind it, and it multiplies the most expensive call in the build.

---

## 2 · The four decisions

### D1 · What feeds the round?

**The gate's output is the repair's input, never a substitute for it.** A round that receives only
the previous round's answer is intrinsic self-correction and the three papers above are about
exactly that. A round that receives the failing gate's output is a different mechanism with
different evidence behind it.

Four rules for the feed:

1. **Fresh context per round**, carrying the gate output rather than the transcript. The reviewer
   sees the artefact and the criterion only (`gate-verdicts` → `references/gate-self-declaration.md` §7).
2. **Demand facts the model must use a tool to obtain**, rather than asking it to evaluate itself.
   The four write themselves here: the unsatisfied criterion quoted verbatim, the gate line that
   emitted the failure, the files the failing package's file plan owns, and the contracts of its
   dependents. None is available from the model's own previous answer.
3. **A durable note per unit of work, carrying what was tried and why it failed** — not a summary.
   That is what stops round 3 repeating round 1. A summary is tokens for nothing.
4. **Do not re-inject an identical block.** If the same payload has already gone in N times,
   condense it to a line. → `references/stop-conditions.md`

### D2 · When does it stop?

Six conditions, and a loop should be able to name which one fired. Check them in this order —
cheapest and most certain first, the same argument that orders the gates:

| # | Condition | How it is decided |
|---|---|---|
| 1 | **Success** | every gate green |
| 2 | **Plateau** | this round's *finding set* equals the previous round's. Our gates emit structured findings, so this is a **set comparison, not a judgement** |
| 3 | **Non-convergence** | the same error three times, or a fix that creates more errors than it resolves |
| 4 | **Wrong architecture** | three failed hypotheses. *"This is NOT a failed hypothesis — this is a wrong architecture"* |
| 5 | **Blast radius** | the fix crosses a file-count threshold, or leaves the scope lock |
| 6 | **Hard cap** | rounds exhausted, spend ceiling reached (`spend-ceilings`), or the derived timeout hit |

**The plateau detector is the one worth building first**, because it is free: a repeat finding set
costs a comparison and saves a whole round. It *composes with* the hard cap rather than replacing
it. Their threshold of fifteen iterations is unbacked — take the detector, leave the number.

Two more that need calibration before use, not adoption on trust: a **thrash score** over churn,
and an **N-consecutive completion signal**. The second is only meaningful alongside gates, never
instead of them. → `references/stop-conditions.md`

### D3 · What happens at the boundary — rule, or ask?

A running loop does not wait on a human for everything, and it does not decide everything either.
Make the stop list **closed**, and record the decisions it did make:

> Record every decision as `Ruling: <what you decided> — <why> — <what it costs if wrong>`, and
> keep going.

Four things stop it and only four: an irreversible or destructive operation; a security-sensitive
action; a side effect outside the work area; and a plan so broken that every path forward is a
guess. **The `cost-if-wrong` field is the one everyone omits, and it is the field that makes an
undo mean something.**

When rounds are exhausted, escalate before giving up: at the second-to-last round, change *both*
the context and the model; at the last, adjudicate each open finding and park the rest with
rulings. **A terminal state that is not "fail"** is the point — a loop whose only ending is failure
teaches its caller to ignore failures. → `references/autonomy-and-escalation.md`

### D4 · How is the stop reported?

A closed set of sentinel outcomes, each carrying a named reason from a small per-loop vocabulary,
emitted as a tag the harness parses — **nobody reads prose**:

```
complete(reason) · blocked(reason) · error(reason) · success
```

**`blocked` is neither success nor error.** A round that ended because the work is done, one that
ended because it cannot proceed, and one that ended because the process died are three different
things, and a `problems` list cannot tell the first two apart.

The stop must also be *legible per gate*: a gate with no stop condition of its own forces the loop
to hard-code one globally, which is how a pass count ends up standing in for a stop condition
(`gate-verdicts` → `references/gate-self-declaration.md` §3).

---

## 3 · Limits

| Claim | Status |
|---|---|
| 3–4 repair iterations capture most of the achievable gain | Supported — Kiecker et al., six tool/dataset combinations, July 2026 |
| Self-correction without external feedback does not reliably help and can degrade | Supported — Huang (ICLR 2024), Kamoi (TACL 2024) |
| **Therefore our four relay passes are waste** | **Not shown.** `plan_models` walks the matrix ranking, so passes 2 and 3 may be *different models*. Cross-model review is a different and better-supported thing than a model reviewing itself. The surveys measure self-correction; they do not measure a three-vendor relay. That is a hypothesis, and it is measurable |
| A plateau detector saves rounds | **Not measured, by us or by them.** The mechanism is sound and cheap; the saving is a guess until instrumented |
| The circuit-breaker ladder, the thrash coefficients, the blast-radius threshold | **Their numbers, from their workloads.** Take the shapes; a number copied without its calibration is a guess someone typed |
| The three-strike rule points at architecture | Stated in two independent repositories. Neither measured it. **And we have no back-edge from build failure to architecture** — building one is an ADR |

**What this skill does not decide**, because each is an architecture decision
(`docs/triage/LAYER-E-TRIAGE.md`): the default pass count; whether repair rounds escalate to a
different model; whether the loop keeps a resumable ledger file; whether packages run in parallel;
whether the loop may exceed a spend ceiling by ruling rather than stopping. The last one deserves
naming — our ceiling is a hard stop and theirs is a decision with a recorded cost. Ours is probably
right for money, but the reasoning is worth confronting rather than inheriting.

**The honesty rule:** the citations justify the *cap*, and only the cap. Everything else here is a
convention read in someone else's repository, and this skill says so at each one.

---

## 4 · Eval

**E1 · The loop names its stop.** Run to each of the six conditions. Assert the result carries a
distinct machine-readable reason for each. Two conditions sharing one reason fails.

**E2 · Plateau fires before the cap.** Construct a repair whose gate output is byte-identical two
rounds running, with the cap set higher. Assert the loop stops at the repeat and that the
comparison is over the *finding set*, not over the generated text.

**E3 · Blocked is not failed.** Give the loop a blocking condition it cannot act on. Assert the
outcome is `blocked` with a reason, and that no caller path maps it to `error`.

**E4 · The round is fed.** Assert the repair prompt contains the failing gate's output. A prompt
containing only the original request and the previous answer fails — that is the defect at
`relay.py:148-167` reproduced.

**E5 · The note carries the failure, not a summary.** Assert the cross-round note names what was
tried and why it failed. A note that would let round 3 repeat round 1 fails.

**E6 · Rulings are recorded with their cost.** Force an autonomous decision. Assert a record exists
with all three fields, `what`, `why`, and `cost if wrong`. Two of three fails.

**E7 · The stop list is closed.** Assert the loop's ask-a-human conditions are enumerated in one
place. A loop that can ask about anything will, and one that can ask about nothing will not stop
for a destructive operation.

**E8 · The terminal state is not only failure.** Assert at least one exhaustion path produces a
reported, non-failure terminal state with open findings adjudicated.

**E9 · Waits are conditions, not sleeps.** Grep the loop and its helpers for fixed sleeps used as
readiness waits. Each one must instead poll a named condition, re-read its subject inside the loop,
and name that condition in the timeout message.

---

## 5 · When this skill is the wrong tool

- **Deciding what a gate returns.** `gate-verdicts` owns that; this skill reads it.
- **Deciding whether a green run is evidence.** `testing`.
- **Setting a budget.** `spend-ceilings` owns caps, meters and what happens when one is hit.
- **Choosing the number of rounds for our loop.** That is an ADR with a measurement attached, and
  §3 says why the obvious answer is not yet earned.

---

*Written 2026-08-26. Papers read at abstract-to-method level, not reproduced. Mined conventions read
at source in `docs/mined/`. Code claims trace to `/home/user/hello-world` through
`docs/next/LAYER-E-BUILD.md` §1–§3.*
