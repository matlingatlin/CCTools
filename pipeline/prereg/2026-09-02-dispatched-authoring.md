# Preregistration — does dispatching the field WRITING cut build time?

- **Registered:** 2026-09-02, before the intervention build exists.
- **Registered by:** the coordinator, at the project owner's instruction.
- **Amendment authority:** the project owner. A change after data is seen creates a new
  registration; this one and its result stay in the record either way.
- **Status:** OPEN.

## The claim being tested

`eval-set-curation-v2` was measured at **79.4 minutes**, of which **38.2 were the coordinator
working alone** and 41.2 were dispatched runs it overlapped. Authoring alone was 44.6 minutes
across 14 turns. The dispatch floor — the sum of the longest single run in each ordered block —
is **28.3 minutes**, so scheduling and concurrency cannot explain the gap: the coordinator writes
every field itself, sequentially.

**Intervention:** the coordinator dispatches a fresh writer per field and adjudicates, instead of
authoring each field in its own turn. This is `subagent-driven-development` applied to the writing
half of a chain that already dispatches the checking half, with `writing-plans` producing the
field decomposition up front.

## Primary metric

**Wall clock minutes**, first event to last, as recorded by `record.timeline()`.
Direction: lower is better. One primary.

## Deciding threshold

**Adopt dispatched authoring only if ALL FOUR hold:**

1. **Time:** wall clock ≤ **0.75 × 79.4 = 59.6 min**.
2. **The verdict is real:** the build reaches a decision. UNDECIDABLE does not count as a result.
3. **The artefact holds:** 5.1 returns **0 errors**.
4. **The win margin holds:** the with-arm beats the incumbent by **≥ 15 points** on expectations
   met. (`eval-set-curation-v2` got 93.8 against 66.7, a 27-point margin.)

**Any one failing → keep coordinator authoring.** "Faster but the margin shrank" is a fail, not a
trade to be weighed afterwards. That is the whole reason the guardrails are numbered here rather
than judged later.

## The confound, stated before the run

**The two builds use DIFFERENT PACKAGES, and that is a real limitation, not a footnote.**
The intervention runs on `data-contract-assertions`, chosen because its profile matches the
baseline's as closely as anything in the library does:

| | eval-set-curation | data-contract-assertions |
|---|---|---|
| description | 1453 chars, cap 1024 | 1448 chars, cap 1024 |
| body | 161 lines | 187 lines |
| references / URLs / runnable evals | 0 / 0 / 0 | 0 / 0 / 0 |

They are not the same difficulty. The intervention package's body is 16% longer, its domain is
different, and nothing here controls for how hard its claims are to write.

**Therefore this is a PILOT, n=1 per arm, and its result is DIRECTIONAL.** A single build per arm
cannot separate the intervention from the package. A result inside the threshold licenses a
second, paired run on the same package — it does not license adopting the change outright.
Saying that now costs nothing; saying it after a favourable number would be worthless.

**Why not the cleaner design:** rebuilding the same package both ways is the paired comparison
that would remove the confound. It is rejected because the v2 artefact is on disk in this repo and
a fresh agent building the same skill would see it, which contaminates the arm more badly than the
package difference does.

## Invalid-run criteria

Void and re-run if any holds, on evidence independent of the result:

- Any gate is bypassed rather than satisfied (`chain_gate`, `cost_gate`, `round_gate`,
  `coordinator_gate`, `routing_gate` must all be clean).
- More than 10% of the span is unaccounted in `record.timeline()`.
- A protected run is routed to a cheaper tier than the baseline used.
- The build reads the `eval-set-curation-v2` artefact or its build record.

## What this does NOT settle

- **It does not measure quality of the writing beyond the four gates and the win margin.** A skill
  can pass all four and still be worse in ways this build cannot see.
- **It does not license dispatched authoring for the two never-batched fields** unless they were
  themselves dispatched and still passed. Which fields were dispatched is recorded per field.
- **It says nothing about the 10-minute target.** The dispatch floor is 28.3 minutes at infinite
  concurrency and this intervention does not move it. Reaching 10 requires measuring less, and the
  cost of each such cut is written down separately.

## Result

*(empty by construction at registration time)*
