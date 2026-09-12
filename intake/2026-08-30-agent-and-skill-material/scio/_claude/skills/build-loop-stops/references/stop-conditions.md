# D1 and D2 · What feeds a round, and the six ways a loop ends

Load this when implementing a stop condition or the feed into a repair round.

## The feed

### The fed repair loop

From `ECC-SKILLS`, `docs/mined/ECC-SKILLS.md:270`. Their Continuous Claude loop, described as
working: on a failed check, fetch the run id, spawn a **fresh** process with the failure as input,
read the logs, fix, push, re-wait — bounded by an explicit retry maximum.

> Our relay's four passes get the model's own previous answer and nothing else.

The mined document's own summary of the asymmetry is worth keeping: *"We have the citations and they
have the mechanism."*

The governing constraint on taking it: **none of it may convert a deterministic gate into a
judgement. The gate output is the *input* to the repair, never a replacement for it.**

### Fact-forced repair — cheaper than the above, and complementary

From `gateguard`, `docs/mined/PASS2-ECC-SKILLS.md:339`:

> **LLM self-evaluation doesn't work.** Ask "did you violate any policies?" and the answer is always
> "no." … But asking **"list every file that imports this module"** forces the LLM to run Grep and
> Read. **The investigation itself creates context that changes the output.**

Three stages, `DENY → FORCE → ALLOW`, where the FORCE payload is concrete facts the model cannot
produce from memory. For a build repair the four write themselves:

1. the unsatisfied acceptance criterion, quoted verbatim from the plan;
2. which gate emitted which line;
3. which files the failing package's file plan owns;
4. the contracts of that package's dependents.

**Their evidence is n=2, self-run and unblinded (9.0 gated vs 6.75 ungated). Take the mechanism;
the number is worth nothing.**

### Do not re-inject an identical block

Same source, and it is directly our problem:

> Only the first 3 fact-force denials emit the full four-fact block; later denials are condensed to a
> single line carrying the denial ordinal, **so near-identical blocks cannot accumulate in the
> context window and amplify model repetition loops.**

Our relay repeats a `problems` list into a growing context. If that claim holds, repeated identical
injections are not merely uninformative — they are degrading. **It needs an eval, not a citation**,
and changing the relay to condense them is an ADR (`docs/triage/LAYER-E-TRIAGE.md` row 52).

### The durable note

Two independent statements: `SHARED_TASK_NOTES.md` read at iteration start and written at iteration
end *"to bridge the context gap between independent invocations"* (`docs/mined/ECC-SKILLS.md:285`),
and a failure ledger on the build job — *what was tried, why it failed, do not retry*
(`docs/mined/PASS2-ECC-RULES-COMMANDS.md:686`).

The rule is the content, not the file: **a note that carries a summary instead of the failure is
tokens for nothing.** What stops round 3 repeating round 1 is knowing what round 1 tried.

---

## The six stops

### 1 · Success — every gate green

Nothing to say, except that "green" must mean what `gate-verdicts` D1 says it means.

### 2 · Plateau

From `gan-style-harness` via `docs/mined/ECC-SKILLS.md:291`: *"if the generator can't improve past a
score plateau after 3 iterations, stop and flag for human review."* And, independently, from
`ECC-AGENTS`, `docs/mined/ECC-AGENTS.md:430`:

```
if score >= pass_threshold: break
if iteration >= 3 and score has not improved in last 2 iterations:
    Log "PLATEAU detected — stopping early"; break
```

**Their version needs a score. Ours does not, and that is the improvement**
(`docs/mined/ECC-AGENTS.md:578`):

> Scio is unusually well placed to make that adaptive, because its gates already emit structured
> findings: **a repair attempt returning the same finding set as the previous attempt is a plateau,
> and that is a set comparison, not a judgment.** Cheaper than tuning the cap, deterministic, and it
> composes with the existing cap rather than replacing it.

Implementation notes: compare the *finding set*, normalised — gate name, rule id, file, and the
identifying part of the message — not raw text, and not the generated code. A single changed line
number should not defeat it, and a genuinely different failure should.

### 3 · Non-convergence

From `build-fix`, `docs/mined/PASS2-ECC-RULES-COMMANDS.md:690`: **the same error three times → stop;
a fix that creates more errors than it resolves → stop.**

The second is the one a cap cannot express: a loop that is actively making things worse still has
attempts left. It requires counting findings before and after, which the plateau comparison already
gives for free.

### 4 · Three failed hypotheses means the architecture is wrong

From `systematic-debugging` (`docs/mined/OTHERS-MINED.md:396`) and `investigate`
(`docs/mined/PASS2-GSTACK-SKILLS.md:188`), independently:

> *"Each fix reveals new shared state/coupling/problem in a different place… This is NOT a failed
> hypothesis — this is a wrong architecture."*

`investigate` states it as a numeric gate: three failed hypotheses → STOP and ask, with three
options (continue / escalate / instrument-and-wait). Its Iron Law above it: *"NO FIXES WITHOUT ROOT
CAUSE INVESTIGATION FIRST."*

**For us this stop has nowhere to go.** There is no back-edge from a build failure to the
architecture. Building one is an ADR; until then the honest terminal state is "stopped, and the
reason is architectural", not a fourth attempt.

### 5 · Blast radius and scope lock

From `investigate`: a fix touching **more than five files** → ask (proceed / split / rethink). And
the scope lock writes the narrowest containing directory into **the same file the freeze hook
reads** — *one mechanism, two entry points* — with an explicit escape: *"If the bug spans the entire
repo… skip the lock and note why."*

The reusable part is the second sentence: a boundary that already exists (for us, the sandbox
workspace guard at `sandbox.py:125`) should serve both the safety check and the scope check rather
than growing a parallel implementation.

### 6 · The hard cap, and the two adaptive metrics that need calibration

The cap is justified: Kiecker et al. put the achievable gain in the first 3–4 iterations, with the
increment by step 3 in *"single digit percentages or below"*. `max_attempts = 3` has a citation.

Two further instruments are worth the shape and not the numbers:

- **A thrash score** (`docs/mined/PASS2-GSTACK-SKILLS.md:255`) — a churn metric alongside the hard
  cap, so a loop that is oscillating stops before the counter runs out. **Their coefficients are
  theirs.** Ours would need calibration on real runs, with test commits excluded, and the hard cap
  stays regardless.
- **An N-consecutive completion signal** (`docs/mined/ECC-SKILLS.md:288`) — three consecutive
  iterations declaring done. A stop condition that is neither "N attempts" nor "gates green", and
  **only meaningful alongside gates, never instead of them.**

---

## Waiting, which is not a stop but is where loops rot

From `condition-based-waiting`, `docs/mined/OTHERS-MINED.md:396`: **poll the condition, name the
condition in the timeout message, and re-read the subject inside the loop.** A fixed sleep is a
guess about someone else's machine; a getter hoisted outside the loop polls a stale value forever.

This applies directly to sandbox start-up and preview readiness. It is also why a timeout should be
derived rather than chosen — see `spend-ceilings`.
