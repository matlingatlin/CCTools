# Ablation · `change-impact-analysis`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

Two questions were run for this skill. The first did not discriminate, and the reason is
instructive, so both are recorded. The second did.

---

## Question 1 — and why it failed

The intended rule was §2.7's **backward traceability**: forward asks *does every element of the
impact set name its reason*; backward asks *does every line in the resulting diff map to an element
of the set*. *"The backward one is the useful half and it is the one systems skip."* Plus the
corollary: *"Do not let this collapse into 'the change stayed inside the package.' Package
ownership is an allow-list, not a trace."*

> Before we let an agent make a change, we work out up front which files it should need to touch.
> Afterwards, what check tells us the change actually stayed in scope? Four bullets max.

**Control** (verbatim, trimmed to the two load-bearing bullets):

> - **File touch list diff**: `git status --porcelain` … every path listed must be inside the
>   agreed scope; anything else is a stop-and-explain.
> - **Diff-content spot check**: `git diff` read against the task description — lines that don't
>   trace to the stated goal (unrelated renames, drive-by refactors, stray formatting) are
>   out-of-scope even inside an allowed file.

**Treatment** (verbatim, same two):

> - `git diff --stat` (or `--name-only`) against the pre-task commit — every touched path must be
>   in the pre-approved file list, zero tolerance for extras.
> - Diff each file's changes against its declared purpose — an edit inside an in-scope file that
>   touches an unrelated function/concern is still drift, not just wrong files.

Both arms produced the file-list check *and* the per-line trace, and both explicitly refused to let
file-list containment stand alone. **Same conclusion, same mechanism — no difference.**

The failure is the question's. *"Afterwards, what check tells us…"* already names the backward
direction; it asks the model to design a post-hoc check, which is the answer. A question cannot
discriminate on a rule it states. This is the same defect as ablation 02, in a subtler form.

---

## Question 2 — the discriminating rule, and why the obvious answer is wrong

§2.6. **Preservation is an allowlist, not a denylist.**

```js
const PRESERVE_STATUSES   = ['done', 'in-progress', 'review', 'cancelled', …]
const REGENERATE_STATUSES = ['pending']
```

Enumerate what may be **regenerated**; everything else survives, *"including states nobody
anticipated."* A denylist — *"regenerate everything not done"* — silently regenerates every state
added after it was written, *"and the failure is invisible until someone's in-flight work is
gone."*

The obvious answer is the denylist, and it is obvious because it is how the intent is naturally
phrased: *keep what's finished, redo the rest.* That sentence is a denylist. It is also the
sentence that destroys work in any state the author did not think of on the day.

Second rule in the same section: **a delta that changes nothing returns a distinguishable no-op** —
`null` (nothing needed changing) is not `[]` (the walk ran and produced nothing).

## The question

> When a project's plan changes we regenerate the parts of it that are affected. Some pieces of
> work are already finished and some are in flight. How should the regeneration decide what to keep
> and what to redo? Four bullets max.

No skill, no file, no unique term. "Finished and in flight" hands over exactly two states, which is
the invitation to write a rule over those two and nothing else.

## Control answer

Verbatim.

> - **Downstream of a real diff, not everything touched by name**: keep work whose inputs (spec,
>   dependencies, interfaces) are unchanged even if it sits near the edited area; regenerate only
>   what consumes something that actually changed.
> - **Finished + unaffected > in-flight**: a completed artifact survives if its upstream spec still
>   holds; work still in flight gets redone rather than patched, since patching a partial result
>   usually costs more than regenerating it clean.
> - **State beats guessing** — check the actual artifact/commit against the current plan node
>   rather than inferring staleness from task status metadata, which lags reality.
> - **Write down what was kept and why** (the *keep* outcome from CLAUDE.md) so the next
>   regeneration doesn't re-examine settled ground.

## Treatment answer

Verbatim.

> Four bullets, per §2.6 and §2.2 of `change-impact-analysis`:
>
> - **Compute the affected set first, tiered** — Certain (nodes whose provenance field is the one
>   edited), Likely (one edge out), Possible (transitive beyond that) — never a flat closure; the
>   depth/edge-type/weight knobs stay explicit.
> - **Preservation is an allowlist, not a denylist.** Enumerate the statuses that *may* be
>   regenerated (e.g. `pending`); everything else — `done`, `in-progress`, `review`, `cancelled`,
>   and any status added later that nobody anticipated — survives by default. A denylist
>   ("regenerate everything not done") silently destroys unknown future states; the allowlist fails
>   in the safe direction.
> - **Status alone doesn't override the affected set** — finished/in-flight work that *is* in the
>   Certain or Likely tier still gets flagged for redo or review; the allowlist only protects work
>   the delta didn't touch. Being "done" doesn't exempt a package whose spec field just changed.
> - **A no-op delta must be distinguishable from an empty regeneration** — return `null`/no-plan
>   when nothing needed changing, versus `[]` when the walk ran and found nothing to redo. Callers
>   (the diff view, the price) depend on telling "nothing changed" from "the computation produced
>   nothing."

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Direction of the preservation rule | **denylist** — *"work still in flight gets redone"*; only "finished + unaffected" is protected | **allowlist** — enumerate the regenerable statuses; everything else survives, *including states nobody anticipated* |
| In-flight work | **redone rather than patched**, on a cost argument | **preserved** unless the affected set reaches it |
| Unknown / future states | not considered | explicitly the point of the rule |
| Impact set | *"downstream of a real diff"* — a flat notion of affected | **tiered** — Certain / Likely / Possible, with depth, edge-type and weight knobs explicit |
| Status vs affected set | conflated — status *is* the decision | **separated** — the affected set decides what is at risk; status decides what is protected. Both are needed, neither substitutes |
| Nothing-to-do outcome | not addressed | `null` vs `[]`, with the two callers that depend on it named |
| Record what was kept and why | **yes** — cites `CLAUDE.md`'s *keep* outcome | not raised |

**Zero of four control bullets match a treatment bullet on mechanism**, and the control's second
bullet is the failure the skill exists to prevent, stated as a recommendation: redoing in-flight
work is the destructive direction, argued from cost rather than from what is lost.

The control's fourth bullet is worth crediting: it is `CLAUDE.md` working on the baseline, exactly
as ablation 03 found. Process discipline is not what the skill supplied.

## Verdict

**Changed the outcome**, on question 2.

The control designed a denylist and recommended discarding in-flight work. The treatment designed
an allowlist whose failure direction is safe, kept the affected set and the preservation rule as
two separate mechanisms, and added a distinguishable no-op. These are different systems, and the
control's would destroy work the first time a status was added that its author had not enumerated.

Question 1 is recorded as **no difference** and the cause is the question, not the skill. One
skill, two questions, two opposite results — which is the clearest evidence in this whole series
that these evals measure question design at least as much as they measure skills.

## Limits of this measurement

n=1 per arm, unblinded, one question per run — two questions total for this skill, and they
disagree. That is the honest headline: had only question 1 been run, this file would report a null.
Neither result is a repeat, so run-to-run variance is unmeasured, and nothing here tests the
skill's main body (§2.1–§2.5, the tiering and pruning literature, the numbers in §3).

The two confounds that apply to every file in this series:

1. **`graphify` is installed at account level** (`/root/.claude/skills/graphify/`) and loads in
   both arms. "No project skills" is not "no skills"; the control also carries the user's global
   `CLAUDE.md`.
2. **The control directory is not the treatment directory minus skills.** It holds `CLAUDE.md` and
   `docs/as-built/` only; the treatment is the live `scio` repo, which also holds `docs/next/`,
   `docs/mined/`, `docs/triage/`, `scripts/` and `graphify-out/`. The treatment's answer cites
   `§2.6` and `§2.2` by number, which is skill-internal and not reachable from repo prose.
