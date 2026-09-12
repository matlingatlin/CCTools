---
name: budget-cut-triage
description: "Use when the remaining budget — wall-clock, tokens, quota, money, context — will not cover the whole plan and something has to be dropped: deciding IN ADVANCE what gets cut so the delivered subset still hangs together and can ship, and stopping at that line instead of being killed mid-item. Triggers on 'we won't finish in time', 'quota runs out before the plan does', 'what do we drop', 'cut scope', 'partial delivery', 'ran out mid-task', 'half-applied migration', 'which items can we skip', a run throttled or shortened after the plan was written, an unattended run that may be interrupted. NOT for lowering unit cost or capping spend (cost-aware-model-routing), NOT for ordering tasks by dependency when the budget is adequate (writing-plans), NOT for defining a loop's exit condition (loop-design-check), NOT for ranking which loaded components eat the context window (context-budget). Those SET or TRACK a budget; this triages a plan against a budget already known to be short."
---

# Budget Cut Triage

When the budget will not cover the plan, the only question worth answering is **what to
drop**, and the worst moment to answer it is while the budget is draining. Decide the cut
order when you write the plan; then stop at the line you drew.

## When to use
- Estimated cost of the plan exceeds the remaining budget (time, tokens, quota, money).
- A run was throttled, shortened, or restarted with less budget than it was planned for.
- A long unattended run could be interrupted, and a half-done state would be unusable.

**When NOT to use (overkill):** either the work fits the budget with real margin — nothing has to
be dropped, so there is nothing to order — **or** every item is independent and reversible, in
which case there is no coherence to protect and nothing to
sequence. Authoring a cut order for those is ceremony. Just do the work.

## The two orders are different — this is the whole point

| | Priority order | Cut order |
|---|---|---|
| Answers | what matters most | what is dropped FIRST so the rest still ships |
| Sorted by | value to the user | cost × indivisibility, among items nothing kept depends on |
| The flagship item | first | often **first to cut** — big, indivisible, nothing kept needs it |
| A dull chore | last | **uncuttable** if item 6 needs it |

Two rules follow, and they override importance:
- **Never cut an item that something you are keeping depends on.**
- **Cut first the item with the highest cost that cannot be split**, once dependents are
  accounted for. Half of an indivisible item buys nothing.

## Is the subset shippable? (the three-part test)

A stop point is valid only if all three hold at that line:
1. **No-partial.** Every item is fully applied or not started. No half-run migration, no
   code merged against an interface that was never landed.
2. **Dependency-closed.** Everything the done items rely on is also done. Stopping after 5
   may be valid while stopping after 6 is not, if 6 needs 3 and 3 was cut.
3. **Handoff.** Someone with only the repo and your note can continue or roll back without
   reading your session. If the state lives in your head, the subset is not shippable.

Test each candidate line by asking: *if the run died exactly here, is there anything to
undo, and would anyone have to ask me a question?* Two nos = a valid stop point.

## Steps
1. **Split the plan into atoms** — the smallest unit that leaves a coherent state.
   Migration + backfill + read-switch is ONE atom, not three.
2. **Cost each atom** in the currency running out, anchored to the measured cost of the
   nearest comparable atom already done — not a hopeful guess.
3. **Map dependencies** both ways: what each atom needs, and what needs it.
4. **List the valid stop points** (the three-part test) with cumulative cost.
5. **Reserve 10–20% for stopping** — handoff, commit, close-out. A plan that spends to the
   last token gets killed while writing the handoff.
6. **Take the last stop point that fits budget minus reserve.** Everything after it is the
   cut list, in order, each with a one-line reason.
7. **Write the cut order into the plan before item 1 runs**, marking each stop point as a
   checkpoint.

   **Two different things get called "mid-run", and only one of them is forbidden.** The test is
   what the order is deciding about:
   - **Rationalisation — forbidden.** You are deciding that what you have ALREADY spent was the
     right subset. The sunk cost is doing the choosing, the boundary lands wherever you happen to
     be, and the order is written to justify it. This is what the rule above rules out.
   - **Re-planning — required, not forbidden.** The budget changed under you: a quota warning
     landed, the window shortened, the run restarted with less. The remaining work is a NEW plan
     whose item 1 has not started, and it gets a cut order the same way the original did. Refusing
     to re-plan here is how you end up killed mid-item with nothing to hand over — the exact
     failure this method exists to prevent.

   The line between them: **draw the cut order over work not yet begun.** If every item it ranks
   is still unstarted, it is a plan. If it ranks items you have already finished, it is a story.
   This repo's own case is re-planning, not rationalisation — see the instance below.

## If you get interrupted mid-item anyway
1. **Stop. Start nothing new**, including "one quick fix".
2. **Restore coherence toward the nearest stop point:** revert the partial if it is
   revertible; if it is not (a half-applied migration), spend what is left finishing the
   smallest atom that closes it, or writing the exact rollback recipe.
3. **Write the handoff in three named parts:** *Done* (verifiable — commits, passing
   tests), *Not done* (every remaining item named — silence reads as done), *Next step*
   (one action, with the file or command).
4. **Leave the state in the repo, not the session.**

## Example
**Before:** 40 minutes of quota, a 10-item plan, no cut order. The agent starts at item 1
and works down. Killed mid-item 6: half-applied migration, no coherent line, a handoff
nobody can act on.

**After (decided before item 1):** costs 4/3/6/5/4/12/3/3/8/6 min = 54 against 40; reserve
6, so 34 usable. Item 6 is the flagship — migration + backfill + read-switch, indivisible,
12 min — and 9 and 10 depend on it; 7 and 8 depend only on 3. Cut list in the plan header:
**6 first** (largest indivisible, and the most important item in the plan), then 9 and 10,
which fall with it by closure. Kept 1–5, 7, 8 = 28 ≤ 34; the stop point after 8 is
dependency-closed with nothing to undo. Delivered: 7 of 10 items whole, plus a handoff
naming 6, 9, 10 as not started and the migration as the next step.

## Rules
  This rule maximises WHOLE ATOMS DELIVERED, not value delivered — say that out loud when you apply it. Where one item's value genuinely dwarfs several others combined, override the rule deliberately and record that you did; do not let the arithmetic make a value judgement it cannot see.
- **The cut order is written before the first item runs.** Whoever is mid-run with the
  quota draining is the worst-placed to choose what to sacrifice — which is why the choice
  is pre-agreed (SRE error-budget policy: the consequence is signed before it is needed, so
  it is not decided under pressure by whoever argues loudest).
- **Never stop inside an atom.** Stop at a stop point or restore one.
- **An unnamed unfinished item is read as done.** Name every one.
- Budget the stop, not just the work.
- Method only: your own planning and estimation. No external CLI installs, no credentials.

## The nearest boundary, spelled out

`loop-design-check` is the closest neighbour and the description cannot carry the distinction
inside the 1024-char cap, so it lives here. That talent already owns two rules this one brushes:
*do not start an iteration you cannot finish*, and *record what backlog remains*. Both are about
WHEN a loop stops and how it damps against quota.

This method answers a different question: given a plan that will not fit, **which items are
dropped and in what order**, so the part that ships is coherent. Concretely — `loop-design-check`
tells the wave not to begin item 7; this tells you that item 7 should be item 10 in the cut order
because item 4 depends on it, and that stopping after item 5 leaves a state someone can pick up.
Use both: one decides that you stop, the other decides what you stop with.

## In this repo (one instance)
Real case, `pipeline/STATUS.md` waves 20–22: a weekly-quota warning throttled the loops
from a 4h to an 8h cadence and that shortened window **cost an entire overnight build
wave**. The budget shrank after the plan was set and no cut order existed, so a whole wave
was lost instead of a chosen part of it. Per-wave fix: cost each queued talent in
`pipeline/frontier.json`; treat build → TEST → commit as ONE atom (an untested talent is a
half-applied change under the standing "test before commit" rule); record the cut order in
`pipeline/BRAIN.md` at the start of the wave, not at the throttle.
