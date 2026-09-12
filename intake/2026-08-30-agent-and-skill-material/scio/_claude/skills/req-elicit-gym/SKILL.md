---
name: req-elicit-gym
layer: A
phase: build-time
status: written
description: Measure a requirements-elicitation conversation with published metrics instead of invented ones. Use when building or running Layer A's replay harness, when choosing metrics for an intake or interview agent, when writing a simulated stakeholder or oracle user, when someone asks "did this change make the wizard better", when classifying what kind of app a user is describing, or when a claim rests on a number like "IRE" or "turns to buildable". Carries the IRE / ESR / TKQR / ORA definitions, the validated oracle-user protocol, the ten-application-type taxonomy, the published baseline to beat, and the reasons a simulated user cannot tell you whether a dialogue is good.
---

# req-elicit-gym

Layer A had no metric, and the first draft of its design document invented five. This skill
exists so that never happens again: a published, reproducible metric set for conversational
requirements elicitation, with the baseline it was measured against and the limits it carries.

---

## 1 · Source

**ReqElicitGym: An Evaluation Environment for Interview Competence in Conversational
Requirements Elicitation.**
Dongming Jin, Zhi Jin (corresponding), Zheng Fang, Linyu Li, XiaoTian Yang, Yuanpeng He,
Xiaohong Chen — Peking University, Wuhan University, Beijing Forestry University, East China
Normal University. 20 February 2026.

- Paper: [arXiv 2602.18306](https://arxiv.org/html/2602.18306)
- Code and data: [github.com/jdm4pku/ReqElicitBench](https://github.com/jdm4pku/ReqElicitBench)

**Paired with**, because it is what stops the metrics being over-claimed:

- *Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic
  Evaluations* — Seshadri, Cahyawijaya, Odumakinde, Singh, Goldfarb-Tarrant —
  [arXiv 2601.17087](https://arxiv.org/pdf/2601.17087)
- τ-bench / τ²-bench (Yao et al. 2024; Barres et al. 2025), whose community named the
  **benevolence bias** — simulated users are too cooperative to be representative.

---

## 2 · Method, in the form we use it

### 2.1 The three metrics

| Metric | Definition | What it catches in Scio |
|---|---|---|
| **IRE** — Implicit Requirements Elicitation ratio | elicited requirements ÷ ground-truth requirements | how much Layer C will have to invent |
| **ESR** — Effective Strategy Ratio | share of probe/clarify turns that elicit at least one implicit requirement | questions that cost a turn and returned nothing |
| **TKQR** — Turn-discounted Key Question Rate | nDCG-style: rewards asking a critical question early, penalises asking it late | *momentum over completeness*, made numeric |

`ORA` (optimal-round assessment) appears in the repository but not the paper; treat it as
"turns to buildable" and cite the repo, not the paper, when using it.

The repository also breaks elicitation down **by requirement aspect — Interaction, Content,
Style** — and **by action type — probe, clarify, finish.** Both breakdowns are more useful to
Scio than the aggregates, because they say *which kind* of requirement is being missed.

### 2.2 The oracle user

The part worth copying exactly. An LLM stakeholder under three controlled principles:

1. **Grounded** — responses come only from the scenario's annotated implicit requirements.
   It may not invent a requirement to be helpful.
2. **Passive disclosure** — it does not volunteer anything it was not asked for.
3. **Context-aware** — it remembers the dialogue and does not repeat itself.

Principle 2 is the one that makes the metric mean anything. A cooperative simulator hands over
the whole spec on turn one and every interviewer scores 1.0.

### 2.3 The taxonomy

Ten application types, from 101 annotated scenarios: showcase websites · community platforms ·
e-commerce · learning platforms · entertainment apps · dashboards · enterprise management ·
publishing platforms · job search platforms · productivity tools.

Use these as Scio's internal app-kind classes (`docs/next/LAYER-A-INTAKE.md` §3.1). Map to
[`schema.org/applicationCategory`](https://schema.org/applicationCategory) only when a spec
leaves the system.

### 2.4 The baseline

**Best model measured: IRE = 0.32.** That is the number to beat, and it is a low bar reported
honestly by the authors: current LLMs show *"limited interview competence"*.

Two findings that should change what Scio builds, not just how it measures:

- **Style-aspect elicitation is near zero across every model tested.** Scio has the same hole
  independently: `look` is excluded from `EXTRACTABLE_FIELDS`. Two unrelated lines of evidence,
  one defect.
- **CoT prompting improves TKQR but not IRE.** Better question *ordering* is not more
  *coverage*. A change that moves only TKQR has made the conversation politer, not better.
- **Performance varies significantly by application domain** — which is the empirical case for
  app-kind detection at all.

---

## 3 · Limits — what the paper shows versus what we are assuming

**This section is mandatory and it is the reason to trust the rest.**

| The paper shows | We would be assuming |
|---|---|
| Results on **website** requirements scenarios, in the authors' setup | that they transfer to Scio's app types, its schema, and its users. Untested |
| An oracle user validated at **Cohen's κ = 0.73** against 33 real interviews | that κ=0.73 is close enough for our purposes. It is substantial agreement, not equivalence |
| IRE = 0.32 for the best model **they** tested, with **their** interviewer wrapper | that our number is comparable to theirs. It is not, unless we run their harness on their data — which the licence does not clearly permit |
| Metrics computed against **annotated ground truth** | that Scio has ground truth. We do not, until scenarios are written and annotated by hand |

**Three hard constraints:**

1. **The repository has no licence file.** The metrics and the protocol are described in a
   public paper and may be reimplemented. **The 101 scenarios may not be vendored.** Contact
   the authors, or write our own scenarios and say so.
2. **A simulated user cannot tell you the dialogue is good.** *Lost in Simulation* finds
   systematic divergence from human behaviour; the τ-bench line names benevolence bias.
   `PRODUCTION_READINESS_DIFF.md:110` independently demands verification *"med riktiga
   användare och varierade appar"*. **This harness is a regression detector.** It answers *"did
   this change make it worse?"* It does not answer *"is this good?"* Any claim of the second
   kind from these numbers is a mis-sale.
3. **One run is one observation.** `B105` records a flaky test in this repo that passed three
   runs and failed two. Report variance across seeds, not a single figure.

**Never write "+X% on IRE" without the sentence that says whose IRE, on what scenarios.**

---

## 4 · Eval

Runnable cases with expected outcomes, so the skill can be measured rather than believed.
Each assumes Scio's own scenario set, not ReqElicitBench's data.

| # | Case | Expected |
|---|---|---|
| E1 | Oracle user, asked nothing, produces a turn | Discloses **no** requirement. A simulator that volunteers fails principle 2 and invalidates every downstream number |
| E2 | Oracle user asked directly about an annotated requirement | Discloses exactly that requirement, in the persona's own words, and no other |
| E3 | Oracle user asked about a requirement **not** in the scenario | Says it does not apply. Does **not** invent one — this is the grounding check on the simulator itself |
| E4 | A deliberately terrible interviewer (asks "tell me more" every turn) | IRE near the floor, ESR near zero. If it scores well, the metric is broken, not the interviewer |
| E5 | The `StandInIntakeProvider` path, replayed | Produces a number, deterministically, with no API key. This is the free baseline every change must beat |
| E6 | The same scenario run five times with different seeds | Report mean **and** spread. A change inside the spread is not a change |
| E7 | Per-aspect breakdown on any scenario with a style requirement | Style elicitation ≈ 0 **before** `look` becomes a question, and > 0 after. This is the acceptance test for proposal A-7 |
| E8 | Ablate `extraction_passes` 2 → 1 | IRE and misfile rate reported for both. Whichever way it comes out, ~48% of extraction input tokens stops being an untested belief |

**Failing E1 or E3 stops everything.** A simulator that is not grounded and passive makes every
other number in this file meaningless.
