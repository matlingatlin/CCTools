---
title: Software architecture — what is measured, and the gap
sources:
  - url: https://doi.org/10.1145/1368088.1368160
    note: Nagappan, Murphy & Basili ICSE 2008, The Influence of Organizational Structure on Software Quality, 3404 Windows Vista binaries
    fetched: 2026-08-27
  - url: https://www.usenix.org/conference/osdi14/technical-sessions/presentation/yuan
    note: Yuan et al. OSDI 2014, Simple Testing Can Prevent Most Critical Failures
    fetched: 2026-08-27
  - url: https://www.usenix.org/conference/osdi22/presentation/huang-lexiang
    note: Huang et al. OSDI 2022, Metastable Failures in the Wild
    fetched: 2026-08-27
  - url: https://arxiv.org/abs/2111.04362
    note: Borowa et al. 2021, cognitive bias in architectural decision-making (knowledge-transfer intervention)
    fetched: 2026-08-27
  - url: https://arxiv.org/abs/2502.04011
    note: Borowa et al. 2025 follow-up, techniques applied to the architect's own architecture
    fetched: 2026-08-27
  - url: https://insights.sei.cmu.edu/library/mission-thread-workshop-guidelines-for-preparation-and-execution/
    note: SEI CMU/SEI-2009-TR-012, Mission Thread Workshop; 57 risks of omission vs 25 of commission, kappa .82
    fetched: 2026-08-27
status: verified
tags: [architecture, evidence, failure-modes, measured-vs-repeated, gap]
related: ["[[design-fixation-and-anchoring]]", "[[requirements-discovery]]", "[[subagents]]", "[[agent-design-template]]"]
---

# Software architecture — what is measured, and the gap

Written 2026-08-28 after building an architect agent for the Scio rebuild. The
second half of this note is the more useful half.

## What is measured

### Organisation predicts defects better than code does
Eight organisational metrics against post-release failures across **3,404 Windows
Vista binaries**: **86.2% precision, 84.0% recall** — beating code churn,
complexity, coverage, dependencies and pre-release defects, all five code-metric
families. **MEASURED.**

Note the direction: organisation *predicts* defects. The **inverse Conway
manoeuvre** — reshaping the org to get the architecture — is widely repeated and,
as far as these sources go, **never measured**. Do not cite it as if it were.

### Failure modes with incidence
| Finding | Number |
|---|---|
| Catastrophic failures from **incorrect handling of explicitly signalled errors** | **92%** of 198 sampled failures in five distributed systems; **58%** catchable by simple testing of the handler |
| **Retry-induced load** as the sustaining effect in metastable failure | **>50%** of studied cases |
| Right overload signal is **request queuing time**, not CPU | ~**50%** better than CoDel, five years in production (DAGOR/WeChat) |
| Repurposed flag waking dead code | Knight Capital, 1 of 8 servers, **$460M in 45 minutes** |
| Quadratic growth in a per-peer resource | AWS Kinesis 2020, per-peer threads → OS thread limit, **~17 hours** |

These are the strongest content in an architect's toolkit, because each names a
mechanism and forces a specific artefact (the handler, the retry cap, the signal,
the grep, the growth term).

### Risk is mostly absence
SEI Mission Thread Workshop: **57 risks of omission vs 25 of commission**, two
raters, kappa **.82**. And **no relationship** between the business goals stated
up front and the risks actually discovered — a goals list will not find them.
**MEASURED.**

### Teaching an architect about bias does not debias them
A knowledge-transfer intervention on practising architects measured **no
debiasing effect**; practitioners were **more** biased than students, attributed
to attachment to systems they had built. The follow-up found the same techniques
worked when **applied as a procedure to the architecture in hand.** Knowing the
step and performing the step are different interventions. **MEASURED.**

### Two metrics that do not deliver
- **Cohesion (LCOM):** a systematic review of 106 studies concludes *"LCOM is not
  very successful in finding faults."* **MEASURED NEGATIVE.**
- **Information hiding:** measured only through a proxy — propagation cost fell
  from 17.35% to 2.78% across one redesign, with **no downstream defect or
  delivery outcome measured**. Treat it as a design discipline producing a
  testable claim, not as a proven predictor.

### Stable-dependencies
Depend in the direction of stability is **REPEATED** — widely taught, no outcome
measurement found. The mechanical *direction check* is still worth running
because it is cheap and deterministic, not because the principle is proven. On
this codebase it found **6 layer-direction violations in 12,054 links** across
276 files, in exactly the two places an independent human review had named.

## The gap — what an architect built from the above does not know

The list above is almost entirely **post-mortem empiricism**: how systems and
architects fail. It is strong on death and empty on design. The following are
absent, and this section is a **research target, not verified content** — it is
recalled, not sourced, and nothing here should enter a skill before it is checked
the way the rows above were.

| The job | The gap |
|---|---|
| Where the boundary goes | Parnas's actual criterion — decompose on **decisions likely to change**, not on processing steps. We hold the proxy and not the source. Bounded context and ubiquitous language — the most-used decomposition primitive in practice — appear nowhere. Cognitive load as a boundary criterion. |
| What "simple" means | The **simple / easy** distinction (un-braided vs near-at-hand). Most architectural debt is choosing "easy" and calling it "simple"; without the distinction the failure cannot be named. Essential vs accidental complexity. Conceptual integrity. |
| What architecture *is* | Architecture as **the decisions that are hard to change** — we hold reversibility as one row of a table rather than as the definition. Architecture as buying options; the trade-off as the deliverable. |
| Surviving operations | The stability pattern language (circuit breaker, bulkhead, timeout) and its antipatterns. **Static stability** — the data plane keeps working when the control plane is down. Blast radius and cell-based isolation, decided before building. Idempotency and identity across boundaries. |
| Data | The whole data discipline. CAP as refined rather than as quoted. |
| Method | **Quality-attribute scenarios** (source, stimulus, artefact, environment, response, **response measure**) — an artefact-forcing procedure of exactly the shape that works here, and we reinvented a worse version. A diagram convention for the decomposition document. |
| Counter-rules | Postel's robustness principle has been **formally retracted** — a counter-rule with a named mechanism, which is the shape measured to discriminate. Hyrum's law: with enough users, every observable behaviour is depended upon. |
| **Measured outcomes** | **DORA / Accelerate** — the largest-N measurement linking architectural properties (loose coupling, team autonomy) to delivery outcomes. **The biggest omission by this note's own criterion:** we demanded measured evidence and missed the most measured source about architecture that exists. |

## Practical notes for building an architect agent

- **Preload at most three skills.** Focused skills of ≤3 modules measured
  +19.0pp vs +10.1pp for 4+; and preloaded skills are re-attached on compaction
  at up to 5,000 tokens each against a 25,000-token shared budget.
- **No persona.** Persona framing measured MMLU 71.6% → 66.3% and no improvement
  across 162 personas × 2,410 questions. *But see*
  [[llm-idea-generation]] — for **diversity** rather than correctness, ordinary
  personas measure 2.6× more between-agent variation. Different dependent
  variable, different answer. Do not carry one conclusion into the other job.
- **Separation works, costume does not.** Removing agent roles from a SWE-bench
  pipeline *lowered* the resolve rate. The mechanism is a separate context and a
  restricted tool surface.
- **Reference corpora on disk, not preloaded.** A skill is a directory; SKILL.md
  can point at sibling files read only when a step calls for them. The ≤3 cap is
  on *preloaded* modules, not on available material. This is the pattern
  Anthropic's own security agent uses: thin identity, fat on-demand procedures
  addressed by path.
- **A boundary that a prompt states is a convention.** A PreToolUse hook runs
  before every permission check, including bypassPermissions, and can only
  tighten. If the agent also has Bash, the wall is decorative.
