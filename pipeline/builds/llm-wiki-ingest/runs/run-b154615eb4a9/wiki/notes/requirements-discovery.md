---
title: Requirements discovery and review — what is measured in software
sources:
  - url: https://doi.org/10.1109/32.391380
    note: Porter, Votta & Basili 1995, Comparing Detection Methods for Software Requirements Inspections, IEEE TSE 21(6) 563-575
    fetched: 2026-08-28
  - url: https://arxiv.org/abs/2208.00825
    note: Ferrari, Spoletini & Debnath 2022, How Do Requirements Evolve During Elicitation?
    fetched: 2026-08-28
  - url: https://doi.org/10.1109/ICSE.2007.24
    note: Maiden, Ncube & Robertson 2007, Can Requirements Be Creative?, ICSE 2007
    fetched: 2026-08-28
  - url: https://www.cs.umd.edu/~basili/publications/journals/J81.pdf
    note: Boehm & Basili 2001, Software Defect Reduction Top 10 List, IEEE Computer 34(1)
    fetched: 2026-08-28
  - url: https://gist.github.com/Morendil/ebfa32d10528af04e2ccb8995e3cb4a7
    note: Bossavit's citation trace of the "IBM Systems Sciences Institute" 100x chart
    fetched: 2026-08-28
  - url: https://cacm.acm.org/research/the-impact-of-size-and-volatility-on-it-project-performance/
    note: Sauer, Gemino & Reich 2007, CACM 50(11) 79-84, 412 projects
    fetched: 2026-08-28
  - url: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/kim-tse-2014.pdf
    note: Kim, Zimmermann & Nagappan 2014, Refactoring at Microsoft, IEEE TSE 40(7)
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2106.09482
    note: Kneer, Kamsties & Schmid 2021, Creativity Triggers, controlled experiment
    fetched: 2026-08-28
status: verified
tags: [requirements, review, inspection, rewrite, evidence, measured-vs-repeated]
related: ["[[design-fixation-and-anchoring]]", "[[ideation-and-idea-selection]]", "[[architecture-evidence]]", "[[agent-design-template]]", "[[prompt-patterns-kernel]]", "[[production-site-checklist]]"]
---

# Requirements discovery and review — what is measured

## The best-evidenced move is differentiated perspectives, not creativity

Porter, Votta & Basili 1995, replicated experiment on requirements inspection,
three conditions — ad hoc, **checklist**, and **scenario** (each reviewer follows
a different specific procedure hunting a different fault class):

- Scenario readers outperformed ad hoc by **~35%**.
- Scenarios helped on their target fault class **without being worse elsewhere**.
- **Checklist reading was no more effective than ad hoc reading.**

Boehm & Basili's own list repeats the headline as *"perspective-based reviews
catch 35 percent more defects than nondirected reviews,"* with an across-study
range of **15–50%**.

**Design consequence:** a set of undifferentiated buckets to sort findings into
is the *checklist* condition — the one measured to buy nothing. What worked was
**different agents, different procedures, different quarry.**

Two limits that bite here. The perspective-based-reading numbers came from runs
of **12–18 volunteers**, one of which was **not significant** (21%, p = 0.21)
while the other was (30%, p = 0.0019). And **the effect was weakest on familiar
material** — no significant individual-level benefit on documents the subjects
already knew, with several reporting they *"fell back to their usual technique."*
Reviewing your own well-documented system is exactly that condition.

## The strongest measured lever for "what is missing"

Ferrari et al. 2022: 30 subjects elicited requirements by interview, then
searched **app stores for comparable existing products** and extended.

- Only **30–38%** of the post-interview content traced to the customer's original
  ideas at all.
- Up to **21%** of post-interview content was on completely novel topics.
- The comparable-products pass added **up to 42% additional feature coverage**.
- 8–17% novel *roles* discovered in that pass.

Authors' framing: requirements are *"not elicited in a strict sense, but actually
co-created."* **MEASURED**, students and a fictional customer, one domain — but
the design maps onto "we have a system, what is missing?" better than anything
else in the literature.

## Expect low novelty and high usefulness

The only study that measured whether workshop ideas survived into the delivered
specification (19 stakeholders, 145 ideas, rated 8 months later by two systems
engineers):

- fully novel: **2 of 139**
- any novelty: **42 (30%)**
- **any impact on the delivered specification: 106 of 139 (76%)**

Authors' conclusion: the workshop was effective at *"surfacing requirements known
but not documented prior to the workshop."* For a system that already exists with
thorough documentation, that is the likely dominant yield — and it is legitimate.

**No study anywhere traces creativity-workshop ideas into a shipped product.**

## Structured prompts beat free ideation — and feel worse

Kneer et al. 2021, **n = 85**, within-subject crossover: 15 structured trigger
questions vs solo brainstorming. Trigger questions produced significantly more
requirement fragments (**p ≤ 0.0001**) in every cell — and were rated
**significantly less useful** (p = 0.0003, 3/5 vs 4/5).

The same dissociation was measured independently in security threat
identification: attack trees found more threats than misuse cases while
**participants' perceptions of the two were similar.**

**Never use "did that feel useful?" as the signal.**

## Numbers in circulation that should not be used

| Claim | Status |
|---|---|
| "Defects cost 100× more after delivery" | Boehm & Basili themselves wrote **"often"**, added **5:1 for small non-critical systems**, and noted good architecture reduces the factor even on large ones. The strong form is **REPEATED**. |
| The "IBM Systems Sciences Institute" 1:6.5:15:60–100 chart | **The study does not exist.** Traced to internal 1981 corporate training course notes from a non-research organisation. No data, no method, no sample. |
| ~2:1 for non-severe defects, 100:1 for severe | **Expert panel consensus, not a study** — and the panel says it does not apply where there is no meaningful early/late distinction. |
| Standish CHAOS, incl. "incomplete requirements = #1 cause of failure" | **REPEATED**; design and analysis critiqued as non-reproducible with selection toward failed projects. |
| "60–80% of rewrites fail"; "94 projects: 68% vs 21%"; "312 attempts across 89 organizations" | **REPEATED or FABRICATED.** The "312 attempts" figure was traced to a paper that **does not contain it**. Netscape is an anecdote. |
| Pre-mortem "increases ability to correctly identify reasons by 30%" | **REPEATED and mis-stated twice over.** The 1989 study measured explanation *length* and tense, never quality or accuracy — and found the **temporal framing had little influence**; **certainty** drove the effect. Frame it *"it failed — why?"*, not *"imagine it is the future."* |

**Measured replacements.** Across 412 projects, **total effort in person-months
was the best discriminator of underperformance** — better than budget, duration
or team size; ≤24 person-months carried ~25% risk; **67% delivered close to
target**, inverting the Standish framing. That is an argument for small
increments, not about rewriting.

## Rewrite vs refactor: the literature is empty

The one large measured study (328 Microsoft engineers + Windows 7 version
history) is **equivocal, in the inconvenient direction**: the top 5%
preferentially refactored modules **decreased post-release defects 7% *less* than
the rest**, while reducing dependencies (0.85× vs 1.10×) and increasing LOC and
crosscutting changes. Authors: the benefit "is multi-dimensional and not
consistent."

Technical-debt cost (~23–36% of development time) is **MEASURED but
self-reported counterfactual** — order of magnitude only.

**Any keep-vs-rewrite argument has to rest on something other than the
literature, because there is nothing there.**

## Measured on missing requirements as a defect source

Complete fault census of two spacecraft (87 + 122 safety-related errors):
**missing requirements were involved in nearly half** of the safety-related
errors involving requirements recognition; imprecise specifications were **>2×**
as likely to associate with safety-related functional faults; interface faults
were driven by **inter-team** communication failure. Non-safety errors
originated more in design. Domain-bound, but a real fault population.

Practitioner self-report at scale (228 companies, 10 countries): **incomplete or
hidden requirements is the most frequently reported RE problem, 48%** — but
weighted by projects that actually failed, **"moving targets" becomes the top
problem**.

## Not measured at all

Whether classifying ideas into keep / add / remove / change taxonomies improves
outcomes. Nothing found. MoSCoW, Kano and the Four Actions Framework have no
controlled outcome evaluations. Obstacle analysis / KAOS / i* finding defects
other methods miss — **the technique's own creators' 2024/25 retrospective offers
an adoption inventory and no comparative measurement.**
