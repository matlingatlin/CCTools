---
name: decision-council
description: "Use when a high-stakes go/no-go or either-or DECISION needs a second, independent look before committing — an architecture or adopt-this-library/framework choice, a ship/don't-ship gate, a hard either-or with real tradeoffs, or any consequential and costly-to-reverse call. Convenes an adversarial council of fresh, independent subagents with distinct lenses (proponent, skeptic, cost, user, long-term-maintenance) that each score a verdict against explicit criteria, then synthesizes a decision and records the rationale plus the strongest dissent. DECIDES between options — distinct from brainstorming (which GENERATES options) and santa-method (which VERIFIES one finding). NOT for committing to a metric and threshold before a MEASUREMENT lands (use preregistered-decision-rule)."
---

# Decision Council

Make a consequential decision — go/no-go, or A-vs-B — by putting it before a council of
fresh, independent subagents, each arguing a distinct lens, then synthesizing a verdict
that keeps the dissent instead of smoothing it over.

## Overview

A single agent deciding alone anchors on its first framing and rationalizes toward it.
Even a self-review shares that agent's blind spots. A council breaks this: several
subagents, each **blind to the others** and each assigned a different lens, evaluate the
same options against the same criteria. Because none sees another's draft, they cannot
converge prematurely — disagreement is signal, not noise. You (the coordinator) never
vote; you frame the question and synthesize the result.

This is the DECIDE tool. It is distinct from its neighbors:
- `brainstorming` GENERATES options — use it first if the options aren't yet clear.
- `santa-method` VERIFIES one finding against adversarial reviewers.
- `dispatching-parallel-agents` is the raw mechanism (fan-out); this adds the protocol.

## When to Use

Use when the decision is **consequential and not cheaply reversible**, and a second
independent look is worth the tokens:
- Architecture or design commitments (a pattern, a data model, a boundary).
- Adopt-or-not: a library, framework, vendor, or protocol you'll build on.
- Ship / don't-ship or launch gates.
- A hard either-or where both options have real, non-obvious tradeoffs.

**Do NOT use when** the call is trivial, cheap to reverse, or already clear — a rename, a
one-line config, an easily-undone experiment. A council there is waste and false ceremony.
If the options themselves don't exist yet, brainstorm first; if you're checking one claim,
use santa-method.

## Steps

### 1. Frame the decision
Write, explicitly and in one place:
- **The question** as a clean choice: "Adopt X or not?" / "A or B?" — not open-ended.
- **The options** (2+), each stated fairly, with its known context and constraints.
- **The decision criteria** — the 3-6 dimensions that actually matter here (e.g. cost,
  reversibility, security, time-to-ship, maintenance load, user impact) and, if they
  differ in weight, how. This is the rubric every voice scores against; get it right,
  because a council on the wrong criteria decides the wrong thing.

### 1b. Red-team the rubric BEFORE fan-out (the frame is a single point of failure)
Identical criteria handed to every voice means a skewed frame becomes *amplified* false
consensus, not a corrected error. So first attack the rubric itself: one pass (a lens, or
your own) asks "what decision-relevant axis is missing or over-weighted here?" Fold any real
omission in before spawning voices. AND relax the no-freelancing rule (step 3): any voice that
spots a decision-relevant axis the rubric omits MUST flag it; when one does, add the axis and
re-run. A rubric no one is allowed to challenge is how a council launders a biased frame.

### 2. Spawn N fresh, independent voices
Dispatch N subagents (typically 3-5), each with a **distinct lens/role** and each given
ONLY the frame from step 1 — never another voice's output, never a shared running draft,
never your leaning. Suggested lenses (pick those that fit the decision):
- **Proponent** — strongest honest case FOR the leading option.
- **Skeptic** — strongest honest case AGAINST; failure modes, what breaks.
- **Cost** — money, tokens, time, opportunity cost over the realistic horizon.
- **User** — impact on the end user / consumer of the thing.
- **Long-term maintenance** — who lives with this in 12-24 months; lock-in, exit cost.
Anti-anchoring is the whole point: separate subagents, identical inputs, no cross-talk.
Do not paraphrase one voice into another's prompt.

### 3. Each returns a scored verdict
Instruct every voice to return, against the step-1 criteria:
- a **recommendation** (which option, or go/no-go),
- a **score per criterion** (e.g. 1-5) with one line of reasoning each,
- its **single biggest risk** and what would change its mind.
Structured returns make step 4 a synthesis, not a vibe.

### 4. Synthesize, decide, record
- Tally by a stated rule: **majority** across voices, overridden by **severity** — a
  credible fatal objection (security hole, one-way door, cost blowout) outweighs a
  numeric majority. Say which rule decided it.
- **Surface the strongest dissent** verbatim, even when overruled. Do not average it away.
- State the **decision** and the **rationale** tied to the criteria.
- Record it: for an architectural or product call, write an ADR (in this repo,
  `docs/decisions/`); otherwise note the decision, the rule, and the kept dissent where
  the work lives.

## Rules
- The coordinator frames and synthesizes; the coordinator does not cast a vote.
- Voices are blind to each other and to your leaning — fresh subagents, no shared draft.
- Every voice scores against the SAME step-1 criteria — but the rubric is red-teamed first
  (step 1b) and any voice MUST flag a decision-relevant axis it omits; don't freelance scores,
  do challenge the frame.
- **Unanimity is a flag, not a comfort** — if every voice agrees, check the frame before
  trusting the consensus; identical inputs can manufacture agreement a biased rubric caused.
- Dissent is preserved, attributed, and recorded — never smoothed over or averaged out.
- Severity can override majority; when it does, say so explicitly.
- Match council size to stakes: 3 for most, 5 for the genuinely load-bearing. Skip it
  entirely for trivial or cheaply-reversible calls.
- The decision isn't done until it's written down with its rationale and its dissent.
