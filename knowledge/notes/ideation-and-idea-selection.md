---
title: Ideation and idea selection — what is measured
sources:
  - url: https://doi.org/10.1037/0022-3514.53.3.497
    note: Diehl & Stroebe 1987, Productivity Loss in Brainstorming Groups, JPSP 53(3) 497-509
    fetched: 2026-08-28
  - url: https://doi.org/10.1207/s15324834basp1201_1
    note: Mullen, Johnson & Salas 1991, meta-analytic integration, BASP 12(1) 3-23
    fetched: 2026-08-28
  - url: https://doi.org/10.1016/j.jesp.2005.04.005
    note: Rietzschel, Nijstad & Stroebe 2006, Productivity is not enough, JESP 42(2) 244-251
    fetched: 2026-08-28
  - url: https://doi.org/10.1287/orsc.2020.1420
    note: Curhan, Labuzova & Mehta 2021, Cooperative Criticism, Organization Science 32(5)
    fetched: 2026-08-28
  - url: https://doi.org/10.1002/ejsp.210
    note: Nemeth, Personnaz, Personnaz & Goncalo 2004, EJSP 34(4) 365-374
    fetched: 2026-08-28
  - url: https://doi.org/10.1177/001698620504900405
    note: Isaksen & Gaulin 2005, Gifted Child Quarterly 49(4) 315-329
    fetched: 2026-08-28
tags: [ideation, brainstorming, decision-making, evidence, measured-vs-repeated]
related: ["[[design-fixation-and-anchoring]]", "[[llm-idea-generation]]", "[[requirements-discovery]]", "[[agent-builder-prior-art]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Ideation and idea selection — what is measured

House rule for this note and its three siblings: every row carries **MEASURED** (a
study with numbers exists and was read) or **REPEATED** (widely asserted, no
measurement found). The distinction is the content; the summary is not.

**The three siblings, and the stage each owns.** [[llm-idea-generation]] owns *generation*:
what comes out when the generator is a model rather than a room — 4,000 seed ideas
deduplicating to ~200, so the fluency this page finds unreliable in humans is worse, not
better, when automated. [[design-fixation-and-anchoring]] owns *exposure*: what reading a
prior design does to whatever is produced next, which is the failure mode that makes idea
*count* actively misleading — fluency held equal in every experiment while variety collapsed.
[[requirements-discovery]] owns *review*: the one intervention in this family with a
replicated effect size, and the finding that differentiated perspectives are what carries it,
not creativity or a checklist. Read together they say the same thing at four stages —
**count is not the measure**, and the studies that report only a count are the ones this
house rule marks REPEATED.

## The founding claim is unmeasured

Osborn (1953, p. 229) claimed "the average person can think up twice as many ideas
when working with a group than when working alone." Basis: observation at his own
advertising agency. No control condition, no alone-comparison, no randomisation.
**REPEATED.** Seventy years of measurement since has pointed the other way.

## What is solid

| Claim | Verdict | Number |
|---|---|---|
| Individuals working alone, pooled, beat the same people interacting | **MEASURED** | d = 1.395, k = 34, N = 2,577 |
| The loss grows with group size | **MEASURED** | r = .606 |
| The loss vanishes at group size 2 | **MEASURED** | all 4 null results in Diehl & Stroebe's Table 1 were 2-person |
| The loss vanishes for non-standard formats | **MEASURED** | d = 0.202, ns |
| Cause is verbal turn-taking | **MEASURED, contested** | 96% of between-condition variance — but from n = 15 units, and Mullen et al. rank it *secondary* |

The two most-cited primary sources **contradict each other on mechanism** and
almost no secondary account says so. Mullen et al., verbatim: their results
"contradict the interpretation of productivity loss suggested by Diehl and
Stroebe (1987)."

Free riding and evaluation apprehension are **MEASURED AND LARGELY REFUTED** as
major causes — 7.75% of variance vs 83.46% for session type; the critical
session × apprehension interaction was non-significant.

## Quantity does not breed quality — the useful half is false

- More ideas → more good ideas: **MEASURED**, r = .69–.82. Near-tautological; a
  fixed hit rate over a larger pool.
- More ideas → a better *best* idea or better *average*: **REFUTED.**
  Manipulations that moved idea count by a factor of 2.6 produced **no
  significant effect on average originality or feasibility.**
- Originality and feasibility are **negatively correlated, r = −0.71**. A single
  "quality" score is therefore incoherent; score the two separately.

## The chain breaks at selection, and that is where the value is

Rietzschel et al. 2006: groups that generated more and more original ideas
**did not select better ideas — selection was not significantly better than
chance.** People systematically pick the conventional: correlation between
"picking the best" and "picking the original" was **−0.40**. Instructing them to
select ideas that are both original and feasible **did not improve selection at
all.**

**This is the single most actionable finding in the literature.** The bottleneck
is not generation.

## Deferring judgment

- "No criticism increases output": **CONTESTED**, and barely tested at all.
  Litchfield's observation that this central rule has almost never been isolated
  experimentally is still accurate.
- Permitting criticism: **MEASURED, CONDITIONAL.** Nemeth found +25–35% more
  ideas. Curhan et al., better powered (N = 422 real stakeholders, preregistered
  stopping rule), found **no main effect at all** (F = 0.01) and a significant
  interaction: **+16% under shared goals, −16% under competing goals.**
- Nemeth's traditional brainstorming instructions were only **marginally** better
  than saying nothing (p < .06). The four rules' value over "come up with as many
  good solutions as you can" is close to undetectable.

## Quotas act as ceilings

Isaksen & Gaulin: told "generate 5–7 ideas" → produced 7. Told "at least 20" →
21. Told nothing → 29. **MEASURED**, though from a study with one group per
condition whose authors disown its rigour. Direction is worth respecting;
percentages from that paper are not.

## Do not trust secondary writing on this topic

An article encountered during this research attributed to Diehl & Stroebe a
finding that does not exist in their paper, and attributed to Mullen et al. the
exact opposite of their conclusion — three fabrications in one short text, each
attached to a real citation. Go to the primary source or do not cite.

The same failure shape recurs far outside this literature: [[agent-builder-prior-art]]
records a practitioner post stating "73% of tickets" and two further percentages with no
method, no logs and no product they map to. **A percentage with no method behind it is
decoration**, wherever it appears — which is why that note reads practitioner writing for
failure reports and never carries a number out of one.

## What could not be found measured

Osborn's rules 2 (free-wheeling) and 4 (combination) in isolation. The 6-3-5
brainwriting protocol specifically — its famous "108 ideas in 30 minutes" is
6 × 3 × 6, arithmetic presented as a result. Optimal group size derived from
data. Session duration, room setup, sticky-note colour. All **REPEATED**.
