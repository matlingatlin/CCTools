# Ablation 03 · `catalog-budget` — the first measured difference

**Date:** 2026-08-26. Third measurement, and the first where a skill changed the outcome.

Ablations 01 and 02 both failed to measure anything: one skill made an answer *worse*, one made
**no** difference. Both failures were the eval's fault, not the skill's — the questions were ones a
model answers correctly from general instinct. This one was designed the other way round: **pick a
rule where the obvious answer is wrong.**

## The question

> *We are adding a CI check so our component catalog entries do not bloat. What should the check
> assert? Be specific, four bullets maximum.*

Nothing names a skill, a budget, or a floor. "Do not bloat" points at a ceiling, which is the trap:
almost anyone designing this check thinks about growth and not about collapse.

Run twice — once from `/home/user/scio`, where the 27 skills load, once from a directory where none
do.

## The two answers

| | **Without skills** | **With `catalog-budget`** |
|---|---|---|
| 1 | max entries per file or category | aggregate ceiling over the always-loaded surface, with the constant and its dated derivation updated **in the same commit** |
| 2 | field/prop budget per component | per-entry cap on the **discovery-time description**, not the body — *"anything longer is content, not a routing decision"* |
| 3 | no duplicate or near-duplicate names | **two floors, not just ceilings** — non-empty required, plus a shrink floor against a frozen baseline |
| 4 | staleness: fail on zero references | three-count census, `addressable ≤ physical`, every addressable entry resolving to a real file |

**Zero of four bullets overlap on mechanism.**

## What the skill added that instinct did not

**The shrink floor, and its reason.** A check that only caps growth passes an entry that collapses
to nothing — *"a silently emptied summary short-circuits matching"* — and the skilled answer cites
`identity.py:210`, our own code, which the baseline could not have known.

**The right subject.** The baseline capped *components*; the skill capped **the always-loaded
surface**, which is what actually costs tokens. Those are different checks with the same name.

**The ratchet.** A constant and its derivation moving together, so a budget cannot be raised
silently. The baseline had no notion that the budget itself needs guarding.

## What both got right

Both flagged that the catalog format is not yet decided and that this belongs in an ADR rather than
an ad-hoc CI script. That is `CLAUDE.md` working on the baseline too, and it is worth saying: the
*process* discipline is not what the skill supplied. The mechanism is.

The skilled answer also closed with the limit its own Limits section demands: *"Constants are
gstack's, not ours — measure our own corpus before picking values, and write the derivation as an
ADR."* A skill that hands over borrowed numbers without saying they are borrowed would have failed
this eval differently.

## Where this leaves the 27

| | |
|---|---|
| Measured against a no-skill baseline | **3** |
| Changed the outcome | **1** — `catalog-budget` |
| Made no difference | **1** — `gate-verdicts` |
| Made the outcome worse | **1** — `as-built`, and the cause was our own contradictory documents |

Still 3 of 27. But the method now works, and the transferable part is the question design:
**an eval question must be one where the confident wrong answer is the natural one.** Ablation 02's
question could not fail; this one could, and the baseline took the bait on all four bullets.
