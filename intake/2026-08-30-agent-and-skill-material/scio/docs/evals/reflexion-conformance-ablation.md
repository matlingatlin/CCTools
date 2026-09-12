# Ablation · `reflexion-conformance`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at account level and loads in **both** arms (as do
`session-start-hook` and `synced`). The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

Murphy, Notkin & Sullivan (FSE'95) produce **three** outcomes, not two: convergence, divergence,
absence. The skill adds the case that matters for a generator — **source that maps to no
high-level entity at all**, the unmapped remainder, which is invariant 1's exact violation and
which a pass/fail check cannot express. §2.3 then requires the outcomes to have **different
consequences**: absence is a build gap, divergence is a *question* that escalates, unmapped source
is the one that blocks. §3 adds the refusal: structural conformance is not correctness, and the
check must not be phrased as though it were.

The obvious answer is a violations list plus a verdict — and, on the extra code specifically, the
obvious answer is the opposite of the rule: code the architecture never mentioned looks like
harmless new work, not like the thing to block on.

## The question

> After our generator produces an app, we want an automated check that the code actually matches
> the architecture we approved. What should the check output, and when should it block the build?
> Four bullets maximum.

No skill, file, paper or term unique to the skill is named. "Matches" and "block" both point at a
boolean.

## Control answer

Verbatim.

> - **Output**: a diff-shaped report — list of violations, each as `expected (per ADR/architecture doc) → actual (file:line)`, plus a single pass/fail verdict; not prose explaining the architecture.
> - **Scope of checks**: layer boundaries (e.g. no direct DB import outside the data layer), allowed dependency directions between modules, and any component the architecture doc declares mandatory (auth, logging, migration structure) — checked structurally (import graph / AST), not by naming convention alone.
> - **Block the build** only on violations that break an approved boundary or omit a mandatory component — i.e. structural drift from what was actually approved.
> - **Don't block** on drift that's merely new (a component not yet mentioned in the architecture doc) — flag it as "unreviewed" for a human decision instead of failing the build, since the check enforces approved architecture, not absence of change.

## Treatment answer

Verbatim.

> - **Three outcomes, not pass/fail:** convergence (built as agreed), divergence (source has a relation the architecture didn't declare), and absence (architecture calls for something the source lacks) — plus a fourth, unmapped source (code traceable to no architecture node at all), which is the invariant-1 violation a boolean check can't even express.
> - **Source model must be extracted, never authored** — scanned out of the generated files each build package actually produced (as `manifest_builder.py` already does), so it can't drift silently the way a hand-maintained model would.
> - **Blocking is asymmetric, not uniform:** absence and unmapped source block promotion (a gap, or code with no sanctioned reason to exist); divergence escalates to a human/architect decision rather than auto-rejecting, since it may mean the architecture was incomplete rather than the code being wrong.
> - **What it must not claim:** this is structural conformance only — it says a table/policy/route exists where expected, not that it's correct (e.g. it won't catch `USING (true)` on a wrong RLS policy) — so gate output and any UI copy should never phrase a clean run as "verified correct."

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Output shape | list of violations + **a single pass/fail verdict** | **three named outcomes**, plus convergence reported rather than implied |
| Something in the source that the model does not describe | its own bullet — **explicitly do not block**; flag as "unreviewed" for a human | its own outcome — **blocks promotion**; "code with no sanctioned reason to exist" |
| Something in the model that the source lacks | folded into "violations"; blocks if the component was mandatory | **absence**, its own outcome, blocks |
| An undeclared relation in the source | folded into "violations"; blocks if it breaks a boundary | **divergence**, escalates to a human — may mean the architecture was incomplete |
| Consequences differ by outcome | partly — a mandatory/boundary split inside one verdict | explicitly asymmetric across three outcomes |
| Where the source model comes from | an import graph / AST scan | **extracted, never authored**, stated as the anti-drift requirement, with our existing extractor named |
| What the check may claim | not addressed | must never read as "verified correct"; structural ≠ behavioural, with `USING (true)` as the counter-example |
| Checks are structural, not naming-based | **yes, and stated more concretely** (import direction, layer boundaries) | assumed, not stated |

**On the fourth case the two arms are exact opposites**, both stated with confidence: the control
says unmapped code must not fail the build because "the check enforces approved architecture, not
absence of change"; the treatment says unmapped code is the one thing that must block.

## Verdict

**Changed the outcome.** This is the cleanest discrimination in the set. The control produced the
predicted answer — a violations list under one verdict — and then took the bait on the fourth case
in the direction the skill exists to reverse. Three mechanisms appear only with the skill: the
three-way outcome vocabulary with unmapped source as a fourth, the requirement that the source model
be extracted rather than authored, and the prohibition on a structural check being reported as a
correctness claim.

Two caveats keep this honest. First, the treatment is a *paper's* method, not a measured result: the
skill's own Limits section says the paper offers no threshold, that its guarantees assume a complete
source model where ours is regex-extracted (`manifest_builder.py`'s known blind spots — ids built by
concatenation, ids passed as props, spread attributes), and that a model *derived from a spec for a
system that does not yet exist* is a direction the paper never studied. Nothing in this ablation
tests any of that; it tests only whether the skill changes what a session proposes.

Second, the control was more concrete about *what to check* — import direction, layer boundaries,
AST over naming convention — where the treatment stayed at the level of outcomes. The two are
complementary, and the skill says so itself: it does not decide what the architecture should be.

## Limits of this measurement

n=1 per arm, one question, unblinded, graded by the person who wrote it. The control's fourth bullet
carries most of the verdict, and it is one sentence from one sample. For a research skill this
matters more than usual: what was measured is that the skill changes the *proposal*, and no part of
this file is evidence that a reflexion-shaped check finds more real drift than a violations list
would. `graphify` loads in both arms and is not controlled for.
