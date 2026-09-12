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
    note: "Huang et al. ICLR 2024, LLMs Cannot Self-Correct Reasoning Yet. The held copy is NOT v1 (17pp vs 19pp) and the difference runs the other way from 2605.17193's - the revision ADDED the Llama-2 GSM8K row this page cites, which v1 does not contain. Claims here were re-verified against the held copy 2026-09-11, so the unpinned URL is correct for them"
    fetched: 2026-08-28
  - url: https://arxiv.org/pdf/2605.17193v1
    note: "Kong, Lai, Piao & Evans 2026, Multi-LLM Systems Exhibit Robust Semantic Collapse. PINNED to v1 on 2026-09-12: the claims on this page were taken from v1 and match it exactly. The unpinned URL now serves an NMI Revision (93pp vs 64pp) that changes four of them - both readings are recorded in the verification section below"
    fetched: 2026-08-28
tags: [llm, ideation, diversity, evaluation, agents, measured-vs-repeated]
related: ["[[design-fixation-and-anchoring]]", "[[ideation-and-idea-selection]]", "[[subagents]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[architecture-evidence]]", "[[effective-agents-anthropic]]"]
raw:
  - knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_2310.01798.pdf
  - knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_2402.01727.pdf
  - knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_2605.17193.pdf
  - knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_2606.12071.pdf
  - knowledge/raw/pdf-sources-2026-09-12/arxiv.org_pdf_2605.17193v1.pdf
  - "all four arXiv primaries held 2026-09-11. knowledge/pdftext.py (stdlib) reads 2310.01798 and 2606.12071 at 100.0% and REFUSES 2402.01727 and 2605.17193 at 0.0% - every glyph hex-coded CID text"
  - "2026-09-12: the other two ARE now readable, by pypdf in an isolated virtualenv (see pipeline/decisions/2026-09-11-stdlib-pdf-text.md, third postscript). All four primaries have been checked against the documents; see the two verification sections below"
  - "match quotes LOOSELY against anything read by pdftext.py: it drops fi/fl/ff ligatures silently. pypdf does not"
  - "the other arXiv URLs here are UNPINNED, so they follow the latest version. 2605.17193 was revised under this note - the 09-11 copy is 93pp (NMI Revision), v1 is 64pp - and the revision changed four figures this page cites. Its citation is now pinned to v1 and BOTH readings are held; cite <id>v1 whenever a claim rests on one reading"
  - "the non-PDF sources still predate the raw layer (2026-09-02)"
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
and 22 models. **Switching model does not help.** *Provenance split 2026-09-12:* the
seven-families figure is Kong et al.'s, and only at **v1** — the revision says ten. The
**38–62%** range and the **22 models** are in neither version of that paper and belong to
another source on this page's list, an HTML render this environment does not hold. The
conclusion is unaffected: Kong et al.'s own topic-matched human baseline (Reddit
open-discussion threads) finds human within-run semantic diversity higher by
**Δ = 0.140, 95% CI [0.109, 0.160]**.

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
| **Explicit "make these more different" CoT step** | cosine **0.377 → 0.255** (human group = 0.243), but **only to ~750 ideas** | no (longer output) |
| Verbalized sampling | 1.6–2.1× diversity, +25.7% human-rated | roughly |
| Negative / surprising attribute framing | p < 10⁻⁴⁰ on novelty | yes |
| **Temperature** | raises *lexical* variety, **flat-to-negative on semantic** diversity; quality loss at 1.5–2.0 | **repeated negative** |
| **Celebrity/genius personas** | **straddles** base 0.377: best cell 0.368, worst 0.411 | mixed — see below |
| **Seeding with existing good ideas** | 0.403–0.428 vs base 0.377 — **worse**; human seeds p = .95 | **repeated negative** |
| **Closed-loop multi-agent chat** | **0 interventions** significant after Bonferroni, across **13** of them and **73 conditions** (v1: 0 of 62 comparisons, 12, 45) | measured negative |

Two operational details worth keeping: **ordinary personas beat visionary ones**
(independently found twice), and in the CoT study **~15% of runs silently skipped
the differentiation step** and declared the ideas already varied — detect and
discard those runs. Both refined against the primary on 2026-09-12, and neither
survives unqualified — see the Meincke section below: the ~15% is the *exhaustion*
experiment's removal rate, not the main comparison's, and "ordinary beats visionary"
holds in that paper only best-cell against best-cell (Creative Entrepreneur 0.348 <
Steve Jobs 0.368), while plain "Entrepreneur" at 0.406 and "Boring Person" at 0.383
are both *worse* than the base prompt.

**Do not carry the persona row into a job graded on being right.**
[[architecture-evidence]] holds the other dependent variable: persona framing measured
MMLU **71.6% → 66.3%**, with no improvement across 162 personas × 2,410 questions. Ordinary
personas buy between-agent variation; they do not buy accuracy, and an architect agent
built on this table would inherit the wrong half.

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

## Re-verified against the held primaries, 2026-09-11 — 5 of 5 confirmed, 2 unverifiable HERE

Four arXiv primaries are now held. Two read at 100.0% via `knowledge/pdftext.py`; the claims this
page takes from them were checked against the documents rather than against the note's memory of
them, matching ligature-tolerantly. **Every one held**, verbatim:

| claim | the primary says | verdict |
|---|---|---|
| GPT-4 GSM8K **95.5 → 91.5 → 89.0** | Table 4, exactly those cells | **MEASURED** |
| GPT-3.5 CommonSenseQA **75.8 → 38.1** | same table, exactly | **MEASURED** |
| Llama-2 GSM8K **62.0 → 36.5** | `62.0 → 43.5 → 36.5`; the page quotes start and end | **MEASURED** |
| the confound: **81.8 → 75.1** | *"Standard Prompting (ours) 1 81.8 · Self-Correct 7 75.1"*, beneath Madaan's own `44.0* → 67.0*` | **MEASURED** |
| RQ-Bench **27.2% → 49.1%** on ties | *"the strict win rate for gpt-5.5 on non-obviousness jumps from 27.2% in standalone scoring to 49.1% in comparative scoring"* | **MEASURED** |
| expert agreement **22–40%** vs **60%** | Table 5a: Expert-Expert 60%, human-vs-LLM 22/28/34/40, *"agreement between humans and LLMs dropped to as low as 22%"* | **MEASURED** |
| and in *opposite directions* | *"Domain experts, however, reach the opposite conclusion"*; *"LLM judges exhibit the opposite tendency"* | **MEASURED** |

**One precision the table forces.** "Every model, every benchmark, accuracy drops" is true of every
model×benchmark *by the end of the loop*, but one cell is a tie rather than a fall: GPT-4 on
HotpotQA is **49.0 → 49.0** at round 1 before dropping to 43.0 at round 2. The sentence stands; the
tie is recorded so nobody re-derives it as a contradiction.

**Two figures on this page were NOT verifiable here — and on 2026-09-12 the search narrowed.** The
`3.73/4` vs `1.00/4` novelty-vs-quality pair and the `6.14` vs `2.38` retrieval pair appear nowhere
in either primary `pdftext.py` can read. `arXiv 2605.17193` was one of the two that **refused at
0.0%**; it is now readable (pypdf, isolated virtualenv) and has been searched in **both** its
versions — the figures are **absent from it too**. That does not refute them; it removes the last
*held* candidate, leaving only the HTML renders this environment does not hold. Absence from the
documents that were searched is still not evidence against them — recorded so the next reader goes
after the unheld sources instead of repeating this search.

## The other two primaries, read 2026-09-12 — and a paper that moved under this note

The two arXiv PDFs `pdftext.py` refuses at 0.0% are readable by `pypdf` in an isolated
virtualenv. Both were searched; every figure this page takes from them was checked against the
document rather than against the note's memory of it.

**Meincke, Mollick & Terwiesch 2024 (`2402.01727`) — 4 of 5 confirmed, 1 wrong in SIGN.**

| claim on this page | the primary says | verdict |
|---|---|---|
| CoT **0.377 → 0.255**, human group **0.243** | Table 2: Group of Students 0.243 · Chain Of Thought 0.255 · Base Prompt 0.377 | **MEASURED** |
| seeding **0.403–0.428** vs base — worse | Previous Top Ideas 0.403 · Girota et al. Seeded GPT-4 0.428 | **MEASURED** |
| **~15%** of CoT runs skipped the step | *"the model did not properly follow the second step and deemed the ideas bold enough without modification. These runs have been removed from the final aggregation (around ~15% of all runs)"* | **MEASURED**, but see the scope below |
| human pool more diverse than any GPT-4 pool | *"Cosine similarity for ideas generated by groups of humans is around 0.243 compared to 0.255 - 0.432 for GPT-4 generated ideas"* | **MEASURED** |
| celebrity personas **worse** | *"instructing GPT-4 to think like Steve Jobs is effective in **increasing the diversity** of the resulting ideas (0.368 cosine similarity versus the baseline of 0.377)"* | **WRONG SIGN — corrected above** |

Lower cosine similarity means *more* diverse, and the page had that right everywhere else (it
reads 0.255 as better than 0.377 two rows up). The celebrity row inverted it anyway, and the
range `0.368–0.411` was the tell: it **straddles** the 0.377 baseline, so no single verdict can
be true of the whole family. The paper's own abstract picks the low end out as a success.

**Two scope limits the primary states and this page did not carry.**

1. **The ~15% removal is the exhaustion experiment's**, not the main comparison's. It appears in
   the 1,200-ideas-in-one-session run; the paper does not report a skip rate for the Table 2
   runs. The operational advice (detect and discard) stands; the number is one experiment's.
2. **CoT's advantage has a horizon.** *"the difference in cosine similarity persists from the
   start up until around 750 ideas when the difference becomes negligible. It is strongest
   between 100 - 500 ideas."* Past ~750–800 the strategy *"starts to deplete the pool of ideas
   it can generate from ... there are fewer and fewer fish in the pond and the strategy does not
   matter any more."* This is an independent second measurement of the ceiling this page opens
   with — Si et al. got there by deduplication (4,000 → ~200), Meincke et al. by depletion — and
   it is the sharper operational form: **a diversity prompt buys you the first few hundred ideas,
   not more of them.**

And the caution the paper puts on its own table, which a ranked list of techniques needs most:
*"Our results should hence not be interpreted as a blanket endorsement of one strategy"*, because
*"the inherent characteristics of cosine similarity complicate the interpretation of
statistically significant results"* and *"prompt crafting does not always have a significant
effect on the outcome."* It also names the limit that matters for ideation specifically: cosine
similarity *"does not consider the similarity to ideas that already exist in the world"*, and
*"it is not clear how it empirically links to human scored measures of similarity."* Read the
table above as an ordering of candidates to test, never as settled effect sizes.

**Kong, Lai, Piao & Evans (`2605.17193`) — the note was right and the PAPER MOVED.**

Three figures on this page did not match the held document. Every one of them matched
`arxiv.org/pdf/2605.17193v1` exactly.

| this page | v1 (64 pp) | held copy (93 pp, titled *"(NMI Revision)"*) |
|---|---|---|
| 12 interventions | *"twelve intervention strategies"* | *"thirteen intervention strategies"* |
| 45 conditions | *"Across a total of 45 tested conditions"* | *"Across 73 tested conditions"* |
| 0 of **62 comparisons** | *"Across 62 baseline comparisons, no intervention yields a positive and statistically significant effect ... after Bonferroni correction"* | *"Across all baseline comparisons, no intervention yields a positive and significant effect ... (all adj. p > 0.05)"* — **the count is gone** |
| 7 families | *"across seven foundation models"* | *"across 10 foundation models"* |

**The finding is not that the note was stale. It is that the URL was never pinned.** An arXiv
*version id* is immutable; `arxiv.org/pdf/<id>` **without** one resolves to the latest version.
All five arXiv PDFs in this repo's raw layer are stored under that unpinned form, and
`knowledge/watch.py` excluded them from watching on the stated ground that *"arXiv version ids
are immutable, so the URL cannot change under us."* That reason was false, and it was refuted by
one of the files it excluded — 64 pages became 93, and four figures changed. The exclusion
itself still holds (a PDF has no visible-text fallback, so a row could only cry wolf), but the
reason in the code has been corrected, and the fix lives at the citation: **pin the version when
a claim rests on one reading.**

The conclusion is untouched, and is now stronger in the revision: more models, more conditions,
more interventions, and still nothing that significantly restores semantic diversity.

**The sweep that followed:** all five held arXiv PDFs were re-fetched at `<id>v1` and hashed.
**Two of the five are not v1.** The other is Huang et al. (`2310.01798`), and it drifted the other
way — its revision *added* the Llama-2 GSM8K row this page cites, which v1 does not contain, so
that note's claim is true of the held copy and false of v1. The full table is in
`knowledge/raw/pdf-sources-2026-09-12/README.md`.

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

Anthropic draws the same line from the design side. [[effective-agents-anthropic]] gates
its evaluator-optimizer pattern on **both** conditions holding — a human can articulate the
feedback, *and* the model can supply that feedback — which is a demand for an external
signal, exactly the ingredient that separates the loop above that loses accuracy on every
model and benchmark from the oracle-label version that gains 8.4 points.

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
