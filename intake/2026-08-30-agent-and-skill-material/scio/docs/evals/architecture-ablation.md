# Ablation · `architecture`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at **account level** and loads in **both** arms. **Second confound:**
the treatment directory carries `docs/next/`, `docs/mined/`, `docs/decisions/`, `scripts/` and `scio.db`
that the control does not; `CLAUDE.md` and `docs/as-built/` are byte-identical. Q1's treatment answer cites
a live reproduction from that corpus — see the note in the comparison.

Two questions were run. Neither discriminated. Both are recorded.

## The discriminating rule, and why the obvious answer is wrong

`architecture` §4 draws the deterministic-first boundary and then sharpens it with a fourth test:

> **The code decides how many. The model fills what is in each.**

and its worked example:

| Decision | Side |
|---|---|
| how many packages a feature splits into | **rule** — a function of the architecture's own measurements |
| what each resulting package's goal sentence says | model — prose a person will read |

> The failure this catches is subtler than *"the model decided something it should not have"*: it is a
> prompt asking for *"an appropriate number of packages"* and getting a plausible one. **Plausible is not
> reproducible, and the number was computable.**

The obvious answer, when a model-chosen count comes out different every run, is **prompt engineering**:
tighten the instruction, drop the temperature, pin a seed, enforce a JSON schema. A competent engineer
reaches for those first and confidently. The skill's answer is that the count is not a generation problem
at all — it is a computation that was handed to a generator.

Runners-up considered and not used: **pick at most three quality attributes** ("three is the budget because
everything after the third is what you will sacrifice"); **run the disqualifier column, not the buys
column**; **cost the survivors, do not rank them — a tie is a tie, not a winner**; **count the owners
before any technical argument**.

## The questions

**Q1** — *We have a step where the model looks at a feature and decides how many work packages to split it
into, then writes a one-line goal for each. Anything wrong with that? Four bullets max.*

**Q2** (the sharper retry) — *Our planner asks the model for an appropriate number of subtasks for each
feature, and the model also names each one. We keep getting a different number for the same input. Should
I just fix that with a stricter prompt and a lower temperature? Four bullets max.*

Q2 names the natural wrong answer in the question itself and invites agreement.

## Control answer

**Q1** (verbatim):

> - **Sizing has no ground truth to check against**: the model is grading its own split, so it can produce
>   3 packages or 12 for the same feature with no way to tell which is right — unless something external
>   (team velocity, a rubric, dependency structure) constrains the count.
> - **A one-line goal hides coupling**: work packages that share a data model, an API contract, or a
>   migration will get independent one-liners that read as clean but conflict at merge time […]
> - **Vague features get vague packages**: if the input feature description is underspecified, the model
>   will confidently fabricate scope boundaries rather than flagging "this needs clarification before
>   splitting" […]
> - **No idempotency/stability**: re-running on a lightly edited feature description can reshuffle the
>   whole breakdown (different count, different boundaries) […] worth pinning or diffing against the prior
>   split rather than regenerating from scratch.

**Q2** (verbatim):

> No — nondeterministic subtask counts are a symptom worth diagnosing before you patch it, not a
> prompt-wording problem by default. Four bullets:
>
> - **Temperature=0 doesn't guarantee determinism** on most providers (batching/MoE nondeterminism,
>   floating-point non-associativity across calls) […] treat it as a small nudge, not a fix.
> - **The real fix is usually structural**: force the count via a schema […] or an explicit "return exactly
>   N items" derived from a separate, deterministic sizing step — rather than hoping free-text generation
>   lands on the same number twice.
> - **Split "how many" from "what are they"** — one call decides subtask count from measurable features of
>   the feature description (word count, number of nouns/verbs, explicit heuristics), then a second call
>   names exactly that many. This turns an open-ended judgment call into two smaller, more constrained
>   ones.
> - **If variance is actually desirable** […] the bug isn't variance itself but *unrepeatability for
>   identical input* — worth checking whether your test is truly holding input constant […]

## Treatment answer

**Q1** (verbatim):

> - **No decline path**: a step whose only outputs are *n ≥ 2* packages will always find a seam because it
>   was asked to — "this feature is already one unit" needs to be a first-class, evidenced answer, not
>   something that only happens by returning n=1.
> - **No modularity check on the split**: the model can produce more packages without producing a *more
>   modular* plan — nothing here computes propagation cost before/after, so "split into 4" could raise the
>   fraction of the plan a future change touches versus splitting into 2.
> - **One-line goals don't establish independence or disjoint write-surfaces**: packages with no declared
>   dependency can still collide on the same file (reproduced live in this repo — two feature packages
>   both plan `app/home/page.tsx`, reported `valid: True`). A goal-per-package doesn't surface that.
> - **No gate-boundary check**: splitting by architectural seam (screen/entity/connector) can produce
>   packages too fine for a reviewer to meaningfully accept one and reject its neighbor — that's a second,
>   independent criterion this step isn't applying, and it can conflict with the modularity number rather
>   than agree with it.

**Q2** (verbatim):

> No — nondeterministic subtask counts are a symptom of an underdetermined decomposition, and clamping
> temperature just papers over it while leaving the real issue in place. Quick take:
>
> - **Root cause first**: if the model isn't given a fixed decomposition rule (e.g., "one subtask per
>   acceptance criterion" or "one per architectural component touched"), count variance is expected
>   regardless of temperature […]
> - **Lower temperature helps marginally, doesn't fix it**: it reduces sampling noise but won't eliminate
>   real decision boundaries (e.g., "is auth one subtask or two?") that flip with irrelevant wording
>   changes in the prompt.
> - **Better fix**: make the count *derived*, not *decided* — have the model first extract a structured
>   list of atomic requirements/criteria (via EARS-style requirements or similar), then subtasks fall out
>   as one-per-item deterministically, rather than asking "how many subtasks and what are they" as a single
>   freeform judgment call.
> - Since this is subtask decomposition for feature planning, this is squarely what the
>   **change-impact-analysis** and **ears-requirements** skills in this repo cover […]

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Q2 · refuses "stricter prompt + lower temperature" as the fix | **yes**, opens with "No" | **yes**, opens with "No" |
| Q2 · **count must be derived, not generated** | **yes** — "Split 'how many' from 'what are they' […] decides subtask count from measurable features […] then a second call names exactly that many" | **yes** — "make the count *derived*, not *decided*" |
| Q2 · the model keeps the prose, loses the count | **yes** | **yes** |
| Q2 · temperature is not the lever | **yes**, with a stronger technical reason (provider nondeterminism, FP non-associativity) | yes |
| Q2 · plausible ≠ reproducible, stated as the principle | implied | implied |
| Q2 · §3 selection procedure, ≤3 quality attributes, disqualifiers | no | **no** |
| Q2 · the two boundary invariants (additive-only; no model output is a gate input) | no | **no** |
| Q2 · routed to other skills | none | `change-impact-analysis`, `ears-requirements` |
| Q1 · overlapping mechanisms | — | **zero of four overlap**, but in different directions, not better ones |
| Q1 · no ground truth / no idempotency | **yes** | no |
| Q1 · decline path, propagation cost, write-surface collision, reviewer granularity | no | **yes** |
| Either question · `architecture` skill named | — | **never** |

**Not attributable to the skill:** Q1's treatment bullet 3 cites *"reproduced live in this repo — two
feature packages both plan `app/home/page.tsx`, reported `valid: True`"*. That comes from the corpus the
control does not have, not from `architecture`. The propagation-cost framing is `design-rule-hierarchy`
territory, which `architecture` explicitly delegates to.

## Verdict

**No difference.** Two questions, and on the rule that was actually targeted the two arms converged.

Q2 was designed so that agreeing with the questioner was the easy path, and **both arms refused it and both
arrived at the count/content split** — the skill's §4 fourth test, reached without the skill. The control
even gave a better reason for the temperature half (provider-level nondeterminism means temperature=0 is
not determinism at all), which `architecture` does not say.

Q1 produced four different bullets per arm with no mechanism overlap, but "different" is not "better": the
control's *no ground truth* and *no idempotency* are the same concern as the skill's *plausible is not
reproducible*, and the treatment's four bullets are about split *quality*, not about which side of the
deterministic boundary the decision sits on. The skill's own framing did not appear in either arm.

The `architecture` skill was **never named in either question**, in a directory where it loads. Its
description explicitly says *"Use whenever the word architecture comes up"* — and neither question used
that word, which is a fair description of how a person would actually ask. A skill that only fires on its
own vocabulary is a skill that fires when it is least needed.

Recorded as a null. The §3 selection procedure — ≤3 attributes, disqualifiers before buys, count the
owners, a tie is not a winner — remains **unmeasured**; a question that reaches it would have to be about
choosing between candidate shapes, and would not have been answerable in four bullets.

## Limits of this measurement

n=1 per arm, two questions, unblinded, one grader who wrote the questions after reading the skill. Both
questions probe §4, roughly one page of a 458-line skill; §§2, 3, 5, 5a and the fourteen-pattern
disqualifier table are untouched by this result and nothing here says anything about them. The treatment
arm carries the rest of the `scio` corpus as well as the 27 skills, so a difference in either direction
could be corpus rather than skill — and on Q1, at least one of the treatment's specifics demonstrably was.
