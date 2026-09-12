# paired-comparison-blinding — the first end-to-end chain run

2026-08-30 to 09-01. Phases 0 through 9, one package, one skill.

## Verdict: ship

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats | pass | |
| no correctness regression | pass | none in 20 paired question-repeats |
| tokens | pass | 70,356 vs 62,169 = **1.13×** (cap 1.20×) |
| tool calls | pass | 2.0 vs 2.0 |
| ≥1 win surviving both repeats | pass | **Q1, Q2, Q4, Q5** — all four in *both* |

Q3 tied in both repeats. Nothing regressed anywhere.

## What actually separated the arms — and it is not what the skill is about

Both graders, blind and independent, found the same thing:

> *"Every expectation about mechanism — relabel per item, withhold the key, raise on
> unresolvable rows, refuse the label-summary headline, refuse the instruction-only fix,
> propose the shuffle — was met by both answers in all five questions; not one of those
> twelve rulings discriminated."* — r2

The baseline already knows the mechanics. What it does not do:

> *"in each the losing answer failed the same kind of expectation: making the design
> legible to the party that has to act on it, or attaching a claim to something read
> rather than asserting it."* — r2

Concretely: a judge prompt that randomises per item but never **tells the judge so**; a
test list containing a round-trip without noting that a round-trip is **exactly** the test
an inverted map survives; a correct refusal of the instruction-only fix **with no source**.

So the skill's demonstrated value is not the procedure. It is *stating the thing that makes
the procedure work to whoever has to act on it, and sourcing the claim that rules out the
cheap alternative.* That is narrower than the skill's own description implies, and it is
recorded here rather than smoothed over.

## The expectation set is weak, again, and the graders said so

> *"four of their five expectations are satisfied by any answer that says no and gestures
> at per-item labels"* — r1, on Q3 and Q5

Same disease as both earlier rounds. Twelve of sixteen r2 rulings did not discriminate.
The four that did are the ones naming a **specific failable thing**. Round 3's rewrite
should keep only that shape.

Q5 still produced a surviving win, so the verdict holds on the discriminating expectations
rather than on the free ones.

## What was not checked

- **The graders were not calibrated against a planted defect** (6.3, still v2).
- **Trigger firing** (6.5, v2) — nothing shows this skill would be *selected*.
- **The expectations were written at phase 4, before any output existed.** The chain orders
  them written after. Preregistered means they cannot be shaped to the results; it also
  means nobody knew what would vary. Both halves are in the build record.
- **The body's rules trace to the claim set, not to observed failures.** The probe found no
  gap on four runs across two task sets, so phase 4.5's warrant was unavailable. This is
  the deviation the whole build rests on, and the measurement is what redeems it.
- **Part of the 1.13× token delta is the method text the `with` arm was handed** and the
  other was not. `subagent_tokens` does not separate input from work.
