---
name: control-seam-audit
description: "Use when every component test passes but the end-to-end result is wrong: the run completed, the number looked plausible. Triggers: 'all the tests pass but the result is wrong', 'between stages', 'a seam nothing watches', 'each component is tested', 'the pipeline produced a plausible wrong answer', 'silent corruption', 'what can this suite not catch', 'we added a control, are we covered'. Tables every boundary between units, ingest and egress included: which control catches a fault there, which faults pass them all. NOT reachability inside units (test-coverage), NOT a patch's mirror sides (integration-contract-completeness), NOT which stage holds the score headroom (stage-ablation-attribution), NOT a check loosened for a green build (oracle-weakening-audit), NOT an agent's stubbed tools failing (agent-fault-injection), NOT an incoming third-party feed (data-contract-assertions), NOT where to PUT a boundary (interface-depth-design), NOT a defect with a reproducing failing test (systematic-debugging)."
---

# Auditing the boundaries a pipeline's controls do not watch

Every stage has a test suite, every suite is green, and the run produced a confidently
wrong answer. When that happens the defect is usually not inside a stage. It is at a
seam - the place where one unit hands a value to the next, where each side holds its
own idea of the contract and no control has ever seen both sides in the same run.

This audit enumerates the seams and produces one row per seam: what crosses it, what
each side believes about it, whether a fault there would complete silently or raise,
and which existing control would catch a fault introduced there. Most rows come back
NONE. NONE, written down per seam, is the deliverable - a list of the faults that would
pass every control you already have.

## When to use this

Use it when any of these is true:

- Every component test passes and the end-to-end result is wrong.
- A run completed, printed a plausible number, and someone downstream says the number
  is wrong.
- You are asked what a test suite cannot catch.
- A control was added after an incident and someone is asking whether that means you
  are now covered.
- A multi-stage pipeline whose stages were built and tested separately reaches one of
  three moments: its first unattended run, the first time its output decides something,
  or a handover to people who did not build it. An ETL or ingest chain, an eval or
  scoring harness, a retrieval chain, a multi-step agent chain, a build or release
  pipeline.

Use it when the units are ones you own and can read on both sides. If you can only see
one side of the boundary, say so per seam and write UNKNOWN; do not guess the other
side from its name.

Do not use it for a defect that already has a reproducing failing test - that is a
root-cause hunt, not a coverage question. Do not use it to decide which stage is
costing the most accuracy; that is a measurement question, answered by ablating stages,
not by reading contracts.

## Important - a control proves the thing it watches, and nothing else

The care taken over a control does not widen its scope. In the incident behind this
method, a control written specifically to prevent a known failure mode, before the
system ran on real data, passed throughout a run that produced exactly that failure -
because the fault had moved one stage upstream of what it watched. So "we added a
control after the last incident" is evidence about that incident. It is never an answer
about coverage. The answer about coverage is the table. The claim behind this is close to
a tautology - a control's scope is what it asserts - and the cited incident shows only
that careful people miss it anyway; it is not a generalisation about your pipeline, and
your own table is what settles your case.

## Important - rank the seams by what a fault there does, not by what it touches

A fault that raises is found by the next run. A fault that completes and prints a
plausible value is found by whoever notices the value is wrong, which may be nobody.
Rank on that before spending effort anywhere. `references/why-controls-miss-seams.md`
carries the evidence for both Important sections above, and their limits differ: the
first rests on one measured incident and licenses no base rate; the second rests on an
engineer's stated design rationale, which argues that silent faults are the class worth
defending and measures nothing about how often they occur.

## Important - this applies for the rest of the task, not once

Every time someone calls a control coverage, or proposes a remedy - at any point,
including long after the table is filled and the checklist is done - it goes through the
table before it is agreed. A remedy proposed in a later turn gets a CATCHES or MISSES
verdict per fault exactly like the first one did. The checklist below is worked once;
these two rules stand for the whole task.

## Steps

```
Task Progress
- [ ] 1. Enumerate the seams (N units give N+1 rows)
- [ ] 2. Quote both sides of every seam
- [ ] 3. Mark each seam SILENT or LOUD
- [ ] 4. Name the control watching each seam, and where its input comes from
- [ ] 5. Answer every coverage claim from the table, not from the control's history
- [ ] 6. Score every proposed remedy against every fault found
- [ ] 7. Report the table first
```

**Step 1 - enumerate the seams before examining any of them.** List every boundary
where a value leaves one unit and enters another, in pipeline order, before looking for
anything wrong. Include the ingest boundary - what enters the first unit, and from whom
- and the egress boundary - what leaves the last unit, and who reads it. N units give
N+1 boundaries. Produces: a numbered list whose length you state, each row naming the
producing side, the consuming side, and the object that crosses.

Do not start from the symptom. Working outward from a wrong number reaches the
boundaries that already hurt and stops there, and the boundaries with no symptom yet are
the ones this list exists to reach.

**Step 2 - quote both sides of every seam.** For each row, find the line that BUILDS the
object and the line that READS it, and quote both with file:line. Compare field names,
types and units. Units, not only types: the asset's `what crosses` column definition says
why that distinction is the one that hides.
Compare the COUNT as well: how many things does the producer emit, how many does the
consumer receive, and is any difference asserted anywhere? A filter that quietly drops
what it cannot handle passes every test written about the dropped item in isolation,
because dropping it is the tested and approved behaviour of that one function; nothing
tests the total. Produces: two quotes per seam, a count-in and count-out or the note
that they are not counted, and YES / NO / UNKNOWN in the agree column. A NO is a defect
found by reading and needs no run to confirm. An UNKNOWN - a side you could not locate -
is a finding, not a blank.

**Step 3 - mark each seam SILENT or LOUD.** Ask what a wrong value at this seam does:
does the run raise, or does it complete and emit something plausible? If you cannot answer from the
code, change the value at that boundary in a throwaway copy - never the working tree -
and see whether anything objects. Produces: SILENT or LOUD on every row, and for any row you
tested, the command you ran.

**Step 4 - name the control watching each seam, and where its input comes from.** For
each seam name a test, assertion, schema check or monitor that would fail if a fault
were introduced there, with its file:line - or write NONE. Then mark where that
control's input comes from: REAL if the producing side produced it in the same run, OWN
if the control built its own fixture. The OWN case is the one that fools people, and the
column definition in `assets/seam-control-table.md` says why. Produces: both columns
filled on every row, NONE written out rather than left blank.

**Step 5 - answer any coverage claim from the table, never from the control's history.**
When someone offers a control as coverage - it is the newest, it is the most thorough,
it was written after the last incident - do not weigh those facts. Read its row. Name
the seam numbers whose control column holds this control, and if that set is empty say
so plainly: it protects none of the rows on this table, whatever its name and however
recently it was added. Produces: per control claimed as coverage, the seam numbers it
protects, or the sentence saying it protects none of them.

**Step 6 - score every proposed remedy against every fault found.** Do not propose a
control without a row per fault reading CATCHES or MISSES. One end-to-end test is the
reflex remedy and it is a partial one: a golden or snapshot control recorded from
today's data records whatever today's data currently masks as correct, so it misses
precisely the faults that are latent. Produces: table 2 of the asset, filled, with a
reason written beside every MISSES.

**Step 7 - report the table first, the narrative second.** The failure this fixes is
specific: an answer organised by fault reads as complete while leaving whole boundaries
unmentioned, because a boundary with no fault found produces no paragraph. A row keyed
by boundary cannot go missing - it comes back NONE instead. So lead with the two tables,
then the list of faults that would pass every control that exists today, each tied to
the seam number it enters at. Produces: two tables and that list. An empty list under a
filled table is a result; an empty list with no filled table is a skipped audit.

## Bundled files

- `references/why-controls-miss-seams.md` - READ it before relying on either Important
  section above, and again when someone argues an existing control already covers a
  boundary or that a fault there would have surfaced by now. Two claims with their
  verbatim quotes, fetch dates, and what each one does and does not license.
- `assets/seam-control-table.md` - COPY it into your answer at step 1 and fill it as you
  go. The two table shapes and a definition of every column. Not reading material; it is
  the output format.

## In this repo (one instance)

The grading harness under `pipeline/evals/harness/` is a three-unit pipeline -
`blind.py` relabels, the graded run scores, `score.py` maps the labels back - and
`selftest_score.py` is the control that watches the un-blinding seam and nothing else.
Anywhere else, the units are whatever your pipeline calls its stages.
