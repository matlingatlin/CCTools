# Ablation · `design-rule-hierarchy`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
So does `session-start-hook`. The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

**Two questions were run.** The first did not discriminate; the second did. Both are recorded, and the
first is the more interesting failure.

## The discriminating rule, and why the obvious answer is wrong

Two candidate rules were available, and I aimed at the weaker one first.

**Candidate A — §(d), the write-surface test.** *"Two packages may build in parallel exactly when
they are in the same antichain **and** their file plans are disjoint."* An antichain is necessary and
not sufficient. This looked like a strong trap: "no dependency edge between them, so run them
together" is the confident wrong answer, and the skill reproduces a live case —
`docs/next/LAYER-C-BUILD-PLAN.md` §2.5, two feature packages both planning `app/home/page.tsx` while
the plan reports `valid: True`. **It failed as a discriminator; see Q1.**

**Candidate B — §(c) versus §(e) and §(f), the granularity question.** *"A split that raises
propagation cost is making the plan less modular no matter how good the motivation sounds."* Eval
**D4** makes the trap explicit: the metric **must refuse to reward package count**. §(e) adds that a
splitter must be able to return *"do not decompose"* as a first-class answer with its own evidence,
and §(f) adds a second criterion that **conflicts with §(c) by design** — propagation cost can favour
splitting where a reviewer's boundary favours merging, and the skill deliberately does not resolve it.

The obvious answer is wrong because **smaller sounds more modular**, and because the natural way to
settle an architecture argument is with better judgement criteria rather than with a number computed
before the argument starts. §3's own limit is the reason the number is not a trump card either: the
graphs are 5–20 nodes, a single edge moves the value several points, and *"the direction of change is
the signal, not the absolute value."*

## The questions

**Q1 (§d):**

> *Our build plan is a graph of work packages with declared dependencies between them. I want to start
> running the independent ones at the same time to cut wall-clock time. How do I work out which ones
> are safe to batch together? Four bullets maximum.*

**Q2 (§c/§e/§f), run after Q1 failed to discriminate:**

> *We are arguing about whether to split one big work package into three smaller ones. Half the team
> says smaller is obviously more modular. How should we settle it? Four bullets maximum.*

Neither names a skill, a file, "antichain", "propagation cost", or DSM.

## Control answer

**Q1:**

> - **Compute reachability, not just declared edges**: two work packages are batchable only if neither
>   is a transitive ancestor/descendant of the other in the dependency DAG — check the full transitive
>   closure, not just direct declared deps, since a missing intermediate hop can hide a real ordering
>   constraint.
> - **Group by dependency-satisfied "ready set"**: at each round, the batch is every package whose
>   declared dependencies are already complete (or already running-and-safe, see next bullet) — a
>   classic topological-sort "wave," not everything that looks unrelated.
> - **Check for hidden shared-resource conflicts beyond the graph**: two packages with no declared edge
>   can still collide if they touch the same file/schema/API/interface contract — verify no
>   shared-write targets before batching, since the plan's declared edges are only as complete as
>   whoever wrote them.
> - **Cap batch width to actual isolation, not just graph independence**: run truly independent
>   packages in separate worktrees/branches so parallel writes can't clobber each other, and merge
>   sequentially — independence in the plan doesn't guarantee independence in the filesystem.

**Q2:**

> - "Modular" is a property of interfaces and dependencies, not package count — check whether the three
>   pieces have independent, well-defined boundaries (can each ship/test/rollback alone?) before
>   assuming smaller = better.
> - Estimate coordination cost: three packages mean three handoffs, three sets of review/merge
>   overhead, and possible sequencing/blocking dependencies — if they're tightly coupled, splitting
>   adds overhead without adding modularity.
> - Per this repo's working norm, this is a "build vs. keep" decision — write it as a one-paragraph
>   ADR-style note (options, tradeoff, decision, reason) so the debate doesn't resurface later.
> - Tiebreaker: if you can't agree on paper, timebox it — split one seam that both sides think is
>   genuinely independent, ship it, and use the actual friction (or lack of it) as evidence for the
>   other two.

## Treatment answer

**Q1:**

> - **Layer first:** run Kahn's algorithm on the dependency graph — each "ready" set (nodes whose deps
>   are all satisfied) is a batch; process layers in order, but everything within one layer is a
>   parallel-candidate.
> - **Antichain, not just "same layer":** within a layer, confirm there's no dependency path between
>   any two members at all (not just that they landed in the same topological round) — that's the
>   actual necessary condition for parallel safety.
> - **Check write-surface disjointness too** — antichain membership is necessary but not sufficient.
>   Two packages can have zero declared dependency on each other and still plan to write the same
>   file/resource; diff their planned output paths and only batch pairs with no overlap.
> - **Don't over-read modularity metrics as a benefit-of-parallelism proof:** propagation cost / DSM
>   metrics tell you how coupled the plan is, not whether parallel execution is actually cheaper —
>   repair/rework costs from conflicts are unmodeled, so treat "safe to batch" (antichain + disjoint
>   writes) and "worth batching" (net wall-clock/cost win) as separate questions.

**Q2:**

> - **Compute propagation cost before and after** — build the reachability matrix over the current
>   work-package graph, get `(reachable ordered pairs)/n²` for the one-package version and for the
>   proposed three-package version. If the split doesn't lower it, "more modular" is asserted, not
>   shown (skill §2c, eval case D4/D5: more pieces isn't automatically more modular).
> - **Check the antichain, not the diagram** — the three pieces are only independent if no dependency
>   path connects any two of them post-split; if one of the three still needs to finish before another
>   starts, you haven't gained parallelism, you've added coordination overhead for nothing (§2b).
> - **Check the write surface too** — even with no declared dependency, verify the three pieces don't
>   touch the same files/interfaces. An antichain with a collision is worse than one package (§2d).
> - **Let "don't split" be a real answer** — if propagation cost is roughly flat or worse and the pieces
>   don't cleanly separate on write surface, the correct output of this argument is "keep it as one
>   package," recorded with the number that justifies it — not a compromise split to end the meeting
>   (§2e).
>
> Bottom line: don't vote on "obviously more modular" — compute the propagation-cost delta and the
> antichain/write-surface check, and let those two numbers settle it.

## Comparison

**Q1 — on mechanism. Convergent.**

| | **Control** | **Treatment** |
|---|---|---|
| Independence test | transitive closure, not declared edges | antichain — no path between members |
| Batching unit | topological "ready set" wave | Kahn levels, each `ready` set is a layer |
| **File collision beyond the graph** | **yes, bullet 3** — *"two packages with no declared edge can still collide if they touch the same file"* | yes, bullet 3 — diff planned output paths |
| Extra | worktree isolation, sequential merge | separates *safe to batch* from *worth batching*; warns propagation cost is not a parallelism proof |

The write-surface rule — the sharpest thing in §(d), and the one reproduced from a live Scio bug — was
**reached independently by the control**, in the same bullet position, for the same reason. Terminology
differs ("transitive closure" / "ready set" versus "antichain" / "Kahn levels"); the mechanism does not.
The treatment's fourth bullet is a genuine addition (do not confuse a coupling metric with a
cost-benefit argument), but it is a caution, not a different procedure.

**Q2 — on mechanism. Divergent.**

| | **Control** | **Treatment** |
|---|---|---|
| How the argument is settled | better judgement criteria, then a timeboxed experiment | **a number computed before the argument** — propagation cost before/after |
| Is "smaller = modular" rejected? | yes — *"a property of interfaces and dependencies, not package count"* | yes — *"if the split doesn't lower it, 'more modular' is asserted, not shown"* |
| Basis for the rejection | definitional / qualitative | `(reachable ordered pairs)/n²`, and D4's rule that the metric must refuse to reward package count |
| Post-split independence | *"can each ship/test/rollback alone?"* | no path between any two of the three |
| Write-surface check | absent from Q2 | present |
| **"Do not split" as a first-class output** | implied by "if tightly coupled, splitting adds overhead" | **explicit** — a recorded decision carrying the number that justifies it, *"not a compromise split to end the meeting"* |
| Tiebreaker if unresolved | split one seam and ship it, use friction as evidence | the numbers decide; no recommendation attached |
| Process | ADR note (this is `CLAUDE.md` working on the control, not the skill) | (assumed) |

**The most interesting line in the whole run is the control's first bullet.** *"Can each ship/test/
rollback alone?"* is §(f) — the review-boundary criterion, the one the skill says produces **coarser**
packages than the architectural criterion and **conflicts with §(c) by design**. The control reached
for §(f) and the treatment reached for §(c), and **neither arm named the conflict.** The skill's own
instruction — *"that conflict is real and this skill does not resolve it; name it in the ADR rather
than picking whichever number agrees with you"* — did not fire in the arm that carries it.

## Verdict

**Q1: no difference.** **Q2: changed the outcome.**

On parallel-batching safety, general engineering instinct already holds the rule the skill exists to
supply. "Two things with no declared dependency can still write the same file" is not
counter-instinctive to a model that has seen build systems; it is a known hazard with a known remedy
(worktrees), and the control produced both. That is a result about the question, and it downgrades §(d)
as a candidate for what this skill uniquely contributes — the *mechanism* was already there, and what
the skill adds is that Scio can decide it deterministically from `planned_files()`, which no question
of this shape can surface.

On granularity, the arms differ on the thing that matters: **whether the decision is a judgement or a
measurement.** The control settled a structural argument with structural taste plus an experiment; the
treatment settled it with a computable number, made "do not split" a recordable answer with evidence
attached, and refused the compromise split. Those are different procedures producing potentially
different decisions on the same plan.

The honest deduction: the treatment did not surface §(f) or its designed conflict with §(c), and picked
the number. That is precisely the failure §3 warns about — *"picking whichever number agrees with you"*
— and it went unremarked in the arm holding the warning. Changed the outcome, then; not obviously
changed it in the direction the skill intends.

## Limits of this measurement

n=1 per arm, unblinded, two questions. I wrote both questions knowing the rules they targeted, ran each
arm once, and judged the answers knowing which was which. The Q2 divergence rests on a single pair of
generations and could be run-to-run variance; the Q1 convergence could equally be. Nothing here shows a
plan built after the treatment's advice produces better code — §3 of the skill says as much on its own
account, since every empirical result behind propagation cost is measured on *shipped source*, not on a
plan of packages that do not exist yet.
