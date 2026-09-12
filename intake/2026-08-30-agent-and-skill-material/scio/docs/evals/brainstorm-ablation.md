# Ablation · `brainstorm`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at **account level** and loads in **both** arms. **Second confound:**
the treatment directory carries `docs/next/`, `docs/mined/`, `docs/ideas/`, `scripts/` and `scio.db` that
the control does not; `CLAUDE.md` and `docs/as-built/` are byte-identical between the two.

Two questions were run. The first discriminated weakly and diluted the target across generation *and*
selection; the second was aimed squarely at the strongest rule. Both are recorded.

## The discriminating rule, and why the obvious answer is wrong

`brainstorm` §2 Step 7 carries the sharpest counter-instinctive rule in the skill:

> Two scorers […] each scoring every idea **0–5 novelty and 0–5 feasibility, separately**. **Never sum or
> average the two** — feasibility bias is the documented mechanism by which good ideas die at selection
> ([Rietzschel et al. 2010]), and a combined score is that bias in arithmetic form. Ship, in this order:
> 1. Top 3 by **novelty**, whatever their feasibility. 2. Top 3 by **feasibility**, whatever their novelty.
> 3. Any idea in both lists […] 4. Fill to `--n` by scorer disagreement — **the widest-disagreement ideas
> first**, because agreement near chance means disagreement carries more information than the mean does.

Anyone handed two 0–5 scores and asked for a ranking will **combine them** — average, weight, multiply,
or gate one by the other. That is the whole point: the skill says the combination step *is the bug*, and
that the two axes must be shipped from separately, never merged. Adjacent rules with the same shape:
**temperature is not the creativity knob** (weakly related to novelty, moderately harmful to coherence),
and **no debate rounds** (interaction is the documented cause of diversity collapse).

## The questions

**Q1** — *We want a wider set of ideas out of a few agents running in parallel, then pick the best handful.
How should I set that up so we do not just get the same obvious idea five times over? Four bullets max.*

**Q2** — *We have about 30 ideas out of an ideation session and need to cut to the best 8. I want to score
each one for how novel it is and how buildable it is. What is the right way to combine those two scores
into a ranking? Four bullets max.*

Q2 presupposes the wrong answer in its own wording — *"the right way to combine"* — which is exactly the
design principle: point the question at the natural mistake and see whether the skill refuses the framing.

## Control answer

**Q1** (verbatim, closing offer elided):

> Four things that actually force divergence, not just parallelism:
>
> - **Assign each agent a distinct stance/constraint before it starts**, not a shared open prompt — e.g.
>   "optimize for zero-config," "assume no LLM in the loop," "assume the user is non-technical and never
>   sees code," "assume 10x current scale." A shared prompt with no constraint variation converges on the
>   same obvious answer regardless of headcount.
> - **Seed each agent from a different source of pressure**: one from user pain points, one from a
>   competitor/prior-art scan, one from a technical constraint, one from "what would we do with a
>   completely different stack." Different inputs produce different outputs; same input in five contexts
>   just resamples the mode.
> - **Have each agent commit cold, in isolation** (no shared scratchpad, no seeing others' output) — per
>   this repo's own "position before history" rule — then only pool afterward. If they can see each other
>   mid-run they'll anchor on whoever writes first.
> - **Judge for coverage of the idea-space, not quality alone**: a separate pass […] plots the N ideas
>   against 2-3 axes (e.g. build cost vs. user-facing novelty) and picks for spread across the map before
>   picking for individual polish — otherwise "best handful" collapses back to five variants of the same
>   safe idea.

**Q2** (verbatim):

> - Don't multiply or average raw scores — plot them on a 2×2 (novelty × buildability) and eyeball
>   quadrants first; averaging lets a mediocre-everything idea outscore a spiky one, which is usually the
>   wrong idea to keep.
> - If you need a single number for sorting within/across quadrants, use a weighted product (e.g.
>   `buildability^1.5 × novelty`) rather than a sum — a product punishes a zero on either axis, whereas a
>   sum lets a high score on one mask a fatal low score on the other.
> - Treat "buildable but not novel" and "novel but not buildable" asymmetrically: an unbuildable idea
>   contributes nothing regardless of novelty, so buildability should function more like a gate (a minimum
>   threshold to even qualify) than a co-equal weight.
> - Pick your 8 by taking the top few from the high-buildability/high-novelty quadrant first, then
>   deliberately reserve 1-2 slots for high-novelty/lower-buildability bets — otherwise a pure ranking
>   formula quietly optimizes into an all-safe portfolio.

## Treatment answer

**Q1** (verbatim, closing offer elided):

> There's a `brainstorm` skill exactly for this — forces parallel independent generation before any
> sharing, checks each idea against what already exists so you don't get five variants of the obvious
> answer.
>
> - **Independent seeding**: each agent generates cold, no visibility into the others' output, so you get
>   true divergence instead of convergence toward the same "obvious" answer.
> - **Distinct angles per agent**: assign each a different lens/constraint (e.g. cheapest-to-build,
>   highest-leverage, contrarian/against-the-grain, borrowed-from-adjacent-domain) rather than the same
>   prompt five times — this is the actual lever against collapse.
> - **Existence check before it's written down**: each idea gets checked against what's already in the
>   codebase/docs so "new idea" isn't just a rediscovery.
> - **Selection pass separate from generation**: pool everything, then pick with a rubric (novelty +
>   feasibility + fit) rather than picking whoever answered first or the median idea.

**Q2** (verbatim, closing offer elided):

> Given this is about ranking ideas from a brainstorm session, a few points worth noting first, then the
> answer:
>
> - **Don't average.** A raw average lets a safe, unoriginal idea (novelty 2, buildable 9 → 5.5) beat a
>   genuinely new one […] the failure case is when averaging lets *mediocre-at-both* beat *excellent-at-
>   one*. Multiply instead, or use a weighted geometric mean — it punishes a zero on either axis rather
>   than letting one axis compensate for the other.
> - **Set a floor before ranking, not after.** Decide the minimum buildable score you'll accept […] and
>   drop anything below it first — then rank the survivors by novelty. This keeps the buildable axis from
>   silently dominating the sort just because it's easier to score confidently.
> - **Force diversity across the cut, don't just take top-8 by score.** A single ranking tends to cluster
>   picks around one theme; pull the top 2-3 by score, then check the remaining 5-6 slots aren't all
>   variations on the same idea — swap in the next-best from an under-represented cluster if they are.
> - **Keep the two scores visible in the output, not just the composite.** When you present the 8, show
>   novelty/buildable side by side […]

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Independence before sharing, no cross-talk during generation | **yes** — and attributes it to `CLAUDE.md`'s *position before history* | yes |
| Distinct frame/constraint per agent | **yes**, with four worked examples | yes, with four worked examples |
| **Prior-art gate before an idea is written down** | no | **yes** — "existence check before it's written down" |
| **Never combine novelty and feasibility** (Step 7) | **refuses averaging, then supplies a weighted product anyway** | **refuses averaging, then supplies a geometric mean anyway** |
| Ship top-3 by each axis independently | no | **no** |
| Fill remaining slots by **widest scorer disagreement** | no | **no** |
| Feasibility as a pre-filter (the rule's named failure mode) | **avoids it** — reserves 1–2 slots for high-novelty/low-buildability bets | **commits it** — "drop anything below it first, then rank the survivors" |
| Selecting for spread, not polish | **yes** (Q1 and Q2) | yes (Q2 only) |
| State that idea scoring is near chance (56.1% / 53.3%) | no | **no** |
| Two independent scorers | no | no |
| Named the skill | no | `brainstorm`, on Q1 only; **not** on Q2 |

Q2 is the informative row. Both arms opened with *"don't average"* — the model already holds that. Neither
reached the skill's actual instruction, which is not "combine better" but **"do not combine."** And the
treatment's second bullet is the precise mechanism Rietzschel et al. describe and the skill exists to
prevent: gate on feasibility first, rank the survivors on novelty. The control's fourth bullet — reserve
slots for high-novelty, low-buildability bets — is **closer to the skill's rule than the treatment's answer
is.**

## Verdict

**No difference — with the treatment marginally worse on the one rule that was targeted.**

The skill adds exactly one mechanism the control did not name: the **prior-art gate that runs before an
idea is written down**. That is real, and it is the piece of `brainstorm` this repo has the most evidence
for (`docs/next/LAYER-A-INTAKE.md:188`; `app-design` §1 — two documented reinventions).

Everything else the treatment said, the control said, in some cases better. On Q1 the skill fired by name
and was then summarised rather than applied: *"pick with a rubric (novelty + feasibility + fit)"* is a
combined score, which §2 Step 7 forbids in bold. On Q2 the skill did not fire at all — no mention, no
Step 7, no scorer-agreement caveat — and the answer landed on feasibility-first gating.

This is a 468-line skill with a research bibliography, and its load-bearing selection rule reached neither
answer. **Being loaded is not being read.** The transferable finding is the same one ablation-02 recorded
about firing: a skill's presence in context is a necessary condition for it to change an outcome, and it
is nowhere near a sufficient one.

If `brainstorm` is to earn its length, Step 7 needs to be reachable without invoking the whole procedure —
the rule *"never combine the two scores; ship from each list separately"* is one sentence, and it did not
survive contact with a question that asked for a combination.

## Limits of this measurement

n=1 per arm, two questions, unblinded, one grader who chose the questions after reading the skill. Both
questions asked for advice *about* an ideation setup rather than invoking `/brainstorm` on a real scope —
the skill is written as an executable procedure, and a procedure asked to summarise itself is not the same
test as a procedure run. A fair reading of this result is "the skill does not improve advice about
ideation," **not** "the procedure does not work when run." Nobody has run it end to end and measured the
output.
