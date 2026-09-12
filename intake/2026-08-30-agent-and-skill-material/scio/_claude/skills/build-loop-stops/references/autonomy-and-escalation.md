# D3 · Rulings, escalation, and a terminal state that is not "fail"

Load this when deciding what a loop may settle by itself, and what it does when the rounds run out.

## Rulings, not stalls

From `subagent-driven-development`, read at `docs/mined/OTHERS-MINED.md:324` — the mined pass calls
it *"the most directly transferable single file in the eight repositories."*

> *"A running plan does not wait on a human. Conflicts, ambiguities, plan defects, a cap you would
> have asked to exceed — decide them… Record every decision in the ledger as
> `Ruling: <what you decided> — <why> — <what it costs if wrong>`, and keep going."*

**Four things stop it, and only four:**

1. an irreversible or destructive operation;
2. a security-sensitive action;
3. a side effect outside this work area that norms say you ask about first;
4. a plan so broken that every path forward is a guess.

The economics, quoted:

> *"A wrong ruling costs rework your human partner can see and undo; a session parked on a question
> costs their whole day and buys nothing."*

**For Scio the asymmetry is sharper, and it cuts the same way:** our user is a non-programmer who
cannot answer a mid-build architecture question at all. A build that stops to ask has not deferred
the decision, it has abandoned it.

**The `cost if wrong` field is what makes an undo mean something.** "We chose X" is a log line.
"We chose X, because Y, and if that is wrong you lose Z" is something a person can act on, and it is
the field every implementation omits.

One item on their list deserves confronting rather than inheriting: *"a cap you would have asked to
exceed"* is among the things they rule on rather than stall on. **Our spend ceiling is a hard stop.**
That is probably right for money — the user approved a number — but the difference should be a
decision, not an accident. See `spend-ceilings`, and `docs/triage/LAYER-E-TRIAGE.md`.

## What may be decided without asking

From `review/checklist.md`, `docs/mined/PASS2-GSTACK-SKILLS.md:692` — the **Fix-First heuristic**:

> **Mechanicality decides autonomy; severity biases toward asking.**

A change that is mechanical (a rename, an import, a formatting rule, a missing null check with one
obvious form) is applied. A change that is user-visible, or critical, is asked about. The two axes
are independent, and collapsing them into "severity decides" is why loops either ask about
everything or nothing.

## The escalation ladder

From the same `subagent-driven-development`, `docs/mined/OTHERS-MINED.md:324`:

| Round | What changes |
|---|---|
| 1–3 | resume the same implementer |
| **≥ 4** | **fresh implementer on a more capable model** — both the context and the model change |
| 5 | the breaker trips: adjudicate each open finding, continue unless one is load-bearing, park the rest with rulings |

Two independent details worth carrying:

- **Fresh reviewers each round**, context-isolated, with a maximum number of rounds and then an
  escalation to a human — `docs/mined/PASS2-ECC-RULES-COMMANDS.md:691`. *Take the fresh context;
  leave the dual-reviewer requirement*, which is excluded by its own source's limits section for
  tasks with deterministic verification.
- **Model selection as a routing table by role** — *"use the least powerful model that can handle
  each role"*, with reviews scaled to the diff's size and risk
  (`docs/mined/OTHERS-MINED.md:750`). This is an ADR for us, not a procedure: `matrix.yaml` already
  ranks seven tasks and three of the rankings are never routed to, including `fix` — while the
  repair path calls the `codegen` ranking directly above it (`docs/next/LAYER-E-BUILD.md` §2.6). A
  repair has a different shape from a first draft: large input, small output. That the code cannot
  express the difference is a defect; what the `fix` ranking should be is a measurement.

## A terminal state that is not "fail"

The point of the ladder is the ending. Round 5 does not throw — it **adjudicates**: each open
finding is decided, load-bearing ones block, the rest are parked with rulings.

A loop whose only ending is failure teaches its caller to ignore failures. This repository already
has the vocabulary to do better — `Remainder` with a `source`, `blocked`, `unjudged` — and already
does it in one place: hitting the spend ceiling *"is not a defect"*, it becomes a `Remainder` with
`source="budget"` and the loop stops rather than retrying, *"because a retry costs money it has
already been told it does not have"* (`loop.py:603`).

That is the shape. The gap is that it exists for exactly one stop condition out of six.
