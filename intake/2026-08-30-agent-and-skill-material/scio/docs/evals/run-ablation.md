# Ablation · `run`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

Control arm: `/tmp/…/scratchpad/baseline` — `CLAUDE.md` byte-identical to `/home/user/scio/CLAUDE.md`,
`docs/as-built/` identical, **no `.claude/skills/`**. Treatment arm: `/home/user/scio`, all 27 skills load.

**Confound, stated up front:** `graphify` is installed at **account level** (`/root/.claude/skills/graphify/`)
and loads in **both** arms. It contributes retrieval/graph advice to control as well as treatment; nothing
in it covers the order of work, so for this skill the confound is small.

**Second confound:** the treatment directory also carries `docs/next/`, `docs/mined/`, `docs/decisions/`,
`docs/triage/`, `scripts/` and `scio.db`, which the control does not. The arms differ by the skills *and*
by the rest of the corpus. Where the treatment cites a number from that corpus, it is marked below.

## The discriminating rule, and why the obvious answer is wrong

`run` §3 fixes an order of work that inverts the standard agile loop in two places:

1. **Brainstorm happens once, over the whole system — not per layer.** *"A second brainstorm per layer"*
   is listed under **What must not happen**. The obvious answer is the opposite: ideate each layer as you
   reach it, because that is what every iterative process teaches.
2. **Architecture runs twice** — once over the whole system (fixing stack, shape, and **the layer count
   itself**), then again per layer against that fixed shape. *"Skipping step 3 because step 1 felt
   sufficient"* is also on the forbidden list. The obvious answer is one architecture pass, or per-layer
   design only.
3. **Seven layers is a description of the predecessor, not a specification.** *"Do not inherit seven by
   default."* A question that says "there are seven layers" invites the reader to treat the count as given.

A competent engineer asked "should I do each layer end to end?" answers **yes, with some up-front
groundwork** — confidently, and wrong on both counts.

## The question

> *I am starting the rebuild tomorrow and want to get the sequence right. There are seven layers. Should
> I just take each layer one at a time — think through the ideas, design it, build it, test it — or is
> there something that has to happen across the whole system first? Four bullets max.*

Names no skill, no file, no term unique to the skill. It asserts seven layers as settled, and describes
the per-layer loop *including ideation* as the default — pointing at the natural wrong answer twice.

## Control answer

> Based on your own CLAUDE.md's ordering, the sequencing question is already partly answered — 00-INDEX
> and the ADRs come before any layer work. So:
>
> - **Read 00-INDEX and 01-DECISIONS first, across all seven layers, before touching any single one** —
>   the ADRs encode cross-cutting choices (auth, data model, hosting) that constrain every layer, and
>   discovering one mid-build means rework.
> - **Resolve the stack ADR before layer 1** — your CLAUDE.md flags the stack as explicitly open; picking
>   it per-layer as you go risks silently inheriting hello-world's choices instead of deciding them.
> - **Map dependencies between layers before ordering them** — "seven layers" isn't necessarily a queue;
>   query `graph.json` for cross-layer edges so you build the layer others depend on first, not just
>   layer 1 first.
> - Within that, yes — per layer: position (cold) → scan → design → build → test → `/checkpoint`, using
>   the layer doc's "State" verdict (solid/wrong-shaped/missing/obsolete) to decide whether it's a port,
>   a rebuild, or a park.

## Treatment answer

> Yes — two whole-system passes have to happen before any layer work starts. The sequence per the `run`
> skill:
>
> - **Once, system-wide, first:** Step 0 brainstorm (once, not per layer, checked against the 249
>   already-triaged findings) → Step 1 architecture pass that fixes the stack, shape, and layer count
>   itself as ADRs. Nothing gets built until these ADRs exist in `docs/decisions/`.
> - **Then, per layer, in a loop:** read that layer's `docs/as-built/LAYER-*.md` State verdict
>   (solid/deliberate/wrong-shaped/missing/obsolete) and decide part-by-part what carries over → a
>   *second* architecture pass, this time scoped to the layer's internals against the already-fixed
>   system shape → build → test (green is `unjudged` until shown capable of failing) → record/commit.
> - Ideas and design only happen "cold" per layer at step 3, after steps 0–2 are done — not free-form
>   per layer as you described; a second brainstorm mid-layer means step 1's decision was wrong, so you
>   reopen that ADR instead of improvising.
> - Practically for tomorrow: your first session is brainstorm + architecture over the whole system
>   (deciding even whether seven layers is right), not layer 1's design — that's why "layer at a time"
>   as originally framed skips a required step.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Read cross-cutting ADRs before any layer | **yes** | implied |
| Stack decided before layer 1 | **yes** | yes |
| **Ideation once, system-wide, not per layer** | **no — endorses per-layer ideation** ("Within that, yes — per layer: position → scan → design → build → test") | **yes**, and names the failure mode: a mid-layer brainstorm means a step-1 ADR was wrong |
| **Two architecture passes** | no — one design step, per layer | **yes**, and says why the second cannot be answered before the first two |
| **Layer count is itself an open decision** | no — treats seven as given, argues only about *order* ("seven layers isn't necessarily a queue") | **yes** — "deciding even whether seven layers is right" |
| Nothing is built before step-1 ADRs exist | no | **yes** |
| The five State verdicts | four of five (drops *deliberate*) | five of five |
| Green is a claim, not a result | no | **yes** — "green is `unjudged` until shown capable of failing" |
| Cited a skill by name | none | `run`, unprompted |

Three of the four things the control said were already available to it from `CLAUDE.md` and
`docs/as-built/` — and it found them. The control's third bullet is a genuinely good point the treatment
did not make (build in dependency order, not numeric order).

**Not attributable to the skill:** the *"249 already-triaged findings"* figure comes from `scio.db` /
`docs/next/`, which the control does not have. Treat that clause as corpus, not skill.

## Verdict

**Changed the outcome.** The control endorsed the per-layer loop the question offered, which is the exact
sequence `run` forbids, and treated the layer count as settled. The treatment refused both, and gave the
reason for each — the two architecture passes answer different questions, and a mid-build idea is a signal
that an ADR is wrong rather than an invitation to improvise.

The difference is not phrasing. The control's answer, followed literally, produces per-layer brainstorms
and one architecture pass over a seven-layer shape nobody decided. That is a different project.

## Limits of this measurement

n=1 per arm, unblinded, one question, one grader — me, who wrote the question after reading the skill.
The treatment arm also carries the whole `scio` corpus the control lacks, so "skill" here means "skill
plus corpus" for anything numeric. Nothing here shows the skill's order is *correct*, only that it is
**not what the model does without it**.
