---
title: LLM idea generation — diversity, selection, and what actually moves them
sources:
  - url: https://arxiv.org/abs/2409.04109
    note: Si, Yang & Hashimoto 2024/ICLR 2025, Can LLMs Generate Novel Research Ideas?
    fetched: 2026-08-28
  - url: https://arxiv.org/abs/2506.20803
    note: Si, Hashimoto & Yang 2025, The Ideation-Execution Gap
    fetched: 2026-08-28
  - url: https://doi.org/10.1126/sciadv.adn5290
    note: Doshi & Hauser 2024, Science Advances 10 eadn5290
    fetched: 2026-08-28
  - url: https://arxiv.org/abs/2605.11258
    note: Shen, Druckmann & Zou 2026, Unlocking LLM Creativity through Analogical Reasoning
    fetched: 2026-08-28
  - url: https://arxiv.org/html/2602.20408
    note: Deng, Brucks & Toubia 2026, Barriers to Diversity in LLM-Generated Ideas
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2402.01727
    note: Meincke, Mollick & Terwiesch 2024, Prompting Diverse Ideas
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2606.12071
    note: Sinhahajari, Majumder & Poria 2026, RQ-Bench, limits of LLM-as-judge for novelty
    fetched: 2026-08-28
  - url: https://arxiv.org/html/2607.01233
    note: Chen, Zhao & Cohan 2026, Measuring the Gap Between Human and LLM Research Ideas
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2310.01798
    note: Huang et al. ICLR 2024, LLMs Cannot Self-Correct Reasoning Yet
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2605.17193
    note: Kong, Lai, Piao & Evans 2026, Multi-LLM Systems Exhibit Robust Semantic Collapse
    fetched: 2026-08-28
status: verified
tags: [llm, ideation, diversity, evaluation, agents, measured-vs-repeated]
related: ["[[design-fixation-and-anchoring]]", "[[ideation-and-idea-selection]]", "[[subagents]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]"]
---

# LLM idea generation — what is measured

## The shape of the problem

A single model asked for ideas produces **a few semantic attractors dressed in
varied prose.** Si et al.: of **4,000 generated seed ideas, ~200 were unique**
after deduplication — **5%** — and the paper states plainly that *"increasing the
number of generated ideas simply leads to repeating duplicate ideas."*
Inference-time scaling of ideation is bottlenecked. **MEASURED.**

The illustration worth memorising: asked 150 times how to predict 3D protein
structure from sequence, a model's top five answers were **AlphaFold2 five
times**, differently worded.

## Novelty that does not survive execution

Si et al. (49 expert idea writers, 79 expert reviewers, 298 reviews): AI ideas
beat human experts on **novelty** (5.64 vs 4.84, p < 0.01) and on nothing else.
Feasibility was numerically lower but **p = 1.00 — not significant**, so the
popular "more novel but less feasible" overstates the second half.

The same authors' follow-up had **43 experts each spend >100 hours implementing**
an assigned idea. LLM ideas' scores dropped **significantly more** than human
ideas on every metric (p < 0.05), and on several aggregates **the ranking
flipped.** **MEASURED**, one study, one field — and the only execution-grounded
evaluation of idea quality that exists.

## Diversity collapse — the best-replicated finding here

Doshi & Hauser (preregistered, N = 293 writers + 600 evaluators): AI assistance
raised individual novelty **+5.4% / +8.1%** (one / five seed ideas) and raised
collective similarity (b = 0.871 / 0.718, p < 0.001 / 0.003). Individual up,
collective down. Replicated in direction by at least four independent groups
across fiction, essays, product ideas and consulting deliverables.

**The nuance nearly everyone drops:** the *five*-seed condition homogenised
**less** than the one-seed condition. The cause is not AI exposure; it is
**shared exposure to a narrow seed set.**

Contested by Ashkinaze et al. (CI 2025, N = 844): in an *iterated* setting AI
exposure **increased** global diversity (Cliff's δ = 0.31) by breaking human
herding. Controlling variable: whether the AI is the shared source or the
perturbation.

Model-level: LLM semantic variability is **38–62% below human** across 7 families
and 22 models. **Switching model does not help.**

## LLMs have a measurable idea *shape*

Chen, Zhao & Cohan: **11,683 papers**, 9 LLM configurations, identical context.

| Opportunity framing | Humans | LLMs |
|---|---|---|
| "Bridge two disconnected things" | **12.1%** | **47.1–64.2%** |
| "Synthesise / unify" | **5.1%** | **22.5–38.7%** |
| Normalised entropy | 0.926 | 0.550–0.758 |

**4–5× over-concentration.** For a software rebuild this becomes *"combine your
X with modern Y," "unify these three subsystems under Z," "add a layer bridging
A and B."* Individually each reads fine; in aggregate the distribution is
grossly narrow. **MEASURED.**

## What moves diversity, ranked by evidence

| Technique | Measured effect | Compute-matched? |
|---|---|---|
| **Cross-domain structural analogy** | diversity **+90–173%**; novel-solution rate **1.6% → 50.4%**; 78% human preference; validated by real implementations | **yes** |
| **Ordinary personas** | **2.6×** between-agent variation; recovers ~90% of the human gap | yes |
| **Explicit "make these more different" CoT step** | cosine **0.377 → 0.255** (human group = 0.243) | no (longer output) |
| Verbalized sampling | 1.6–2.1× diversity, +25.7% human-rated | roughly |
| Negative / surprising attribute framing | p < 10⁻⁴⁰ on novelty | yes |
| **Temperature** | raises *lexical* variety, **flat-to-negative on semantic** diversity; quality loss at 1.5–2.0 | **repeated negative** |
| **Celebrity/genius personas** | 0.368–0.411 vs base 0.377 — **worse** | repeated negative |
| **Seeding with existing good ideas** | 0.403–0.428 vs base 0.377 — **worse**; human seeds p = .95 | **repeated negative** |
| **Closed-loop multi-agent chat** | **0 of 62 comparisons** significant after correction, across 12 interventions and 45 conditions | measured negative |

Two operational details worth keeping: **ordinary personas beat visionary ones**
(independently found twice), and in the CoT study **~15% of runs silently skipped
the differentiation step** and declared the ideas already varied — detect and
discard those runs.

## The model cannot rank its own ideas

| Evaluator | Agreement with expert ranking |
|---|---|
| Human inter-reviewer | **56.1%** |
| Best LLM (pairwise) | 53.3% |
| GPT-4o | 45.0% |
| A published "AI reviewer" | 43.3% |
| Random | 50.0% |

Two of them below chance. In 2026, RQ-Bench measured expert-vs-LLM agreement on
non-obviousness at **22–40%**, against expert-expert at 60% — and found they
disagree in *opposite directions*, not merely noisily.

**Forced pairwise comparison inflates scores by construction:** the same model's
win rate went **27.2% → 49.1%** purely because ties had to be broken.

**Novelty scoring rewards vagueness.** In one 2026 study the **worst** system
scored **highest** on novelty (3.73/4) and last on quality (1.00/4) — a vague,
topic-agnostic template *"has no precise prior art to collide with, so it scores
as novel."* Only the quality × novelty plane separates it.

**Embedding similarity does not detect restatement.** Human-written reference
questions were *more* similar to their source material than the model outputs,
while being *less* narrow. The pathology is structural, not lexical.

## The context rule

Five independent measurements converge:

> **Starve the generator of the existing system's solution vocabulary. Saturate
> the evaluator with it.**

Generator side: seeding hurts (above); models given background material produce
outputs experts call *"narrow and too tied to the background"* (narrowness 1.00–
1.55 vs human 0.47); and for **well-known problem types** models produce *more*
ideas with *lower* novelty, diversity and rarity.

Evaluator side: judging already-published (therefore non-novel) ideas, a model
scored novelty **6.14/10 without retrieval and 2.38/10 with it.** Without the
existing reality in front of it, a novelty judgment is inflated ~2.6×.

**Cross-domain context is the exception — it expands.** But vague instruction to
"look elsewhere" is not enough; the measured gain came from an **explicit
relational mapping**.

## Self-critique

Huang et al., intrinsic self-correction with no external signal: **every model,
every benchmark, accuracy drops.** GPT-4 GSM8K 95.5 → 91.5 → 89.0. GPT-3.5
CommonSenseQA 75.8 → **38.1**. Llama-2 GSM8K 62.0 → 36.5. With **oracle** labels
the same loop *gains* 8.4 points — the signal does the work, not the loop.

Their exposed confound is one to check in our own work: a reported
self-refinement gain of 44.0 → 67.0 became, with a properly informative initial
prompt, a **baseline of 81.8 that self-refinement then degraded to 75.1.** *If a
refinement step uses criteria the generation prompt lacked, put them in the
generation prompt and re-measure.*

No measured evidence exists that an LLM critiquing its own proposals with no
external input improves them.

## Multi-agent

"Multi-agent ideation beats compute-matched single-model sampling" is **NOT
MEASURED.** Every affirmative claim found — including a widely-publicised
co-scientist system — lacks a matched-budget baseline. Where matched baselines
exist in adjacent tasks they go the other way: majority-vote self-consistency
beat debate at every matched budget (85.3 vs 83.2 at 6 calls; 88.2 vs 83.0 at 9),
and independent k-shot sampling beat agentic pipelines at every cost threshold on
216 Codeforces problems.

Scope limit worth respecting: the self-consistency result is a *verifiable-answer*
task with majority voting, which is meaningless for ideation — you want the tail,
not the mode. What transfers is the methodological demand: **any multi-agent
ideation claim without a matched single-model baseline is uninterpretable.**

## Thin spots

The analogical-reasoning result is one paper, one domain, not replicated —
despite being the strongest positive finding. Verbalized sampling has no
independent replication. RQ-Bench's headline rests on 50 samples and 2 experts.
And **almost all 2025–2026 ideation benchmarks score with LLM judges**, which the
judge literature says over-reward vague novelty language — so leaderboard
positions measure *appeal to an LLM judge*, not idea quality.
