---
name: brainstorm
layer: build-process
phase: build-time
status: written
description: Run an evidenced ideation procedure instead of free-associating. Use when someone says brainstorm, ideate, give me ideas, what else could we do here, we need options, widen the design space, what are we missing, or asks for alternatives on a layer in docs/next. Forces parallel independent generation before any sharing, checks every idea against what already exists in its domain before the idea is written down, and emits a parseable idea file a validation stage can act on. Covers what the brainstorming literature actually measured and what it disproved, LLM diversity collapse and how to counter it, retrieval-not-packing over docs/next and the code graph, and how to select ideas without collapsing to the median.
---

# brainstorm

A brainstorm here is a **procedure with an audit trail**, not a model producing plausible sentences
at temperature. It exists because the popular version of brainstorming is one of the better-disproved
ideas in applied psychology, and because a model asked to "think broadly" reaches for the median of
its training data — the same failure `app-design` names for generated UI, one level up.

Three things an unstructured prompt does not do: **independence before sharing** (parallel
generation, no cross-talk, then pooled — the one intervention the human literature supports);
**a prior-art gate that runs before an idea is written down** (this repo has twice invented
something that had a standard — a requirement-coverage percentage where ISO/IEC/IEEE 29148 existed,
`docs/next/LAYER-A-INTAKE.md:188`, and a design-token shape where W3C DTCG existed,
`.claude/skills/app-design/SKILL.md` §1); and **a parseable output** where each idea carries its
prior art and its falsifier, so the next stage tests rather than admires.

---

## Usage

```
/brainstorm --layer B                        # ideate over one layer document
/brainstorm --layer B --anchor "3.4"         # ideate over one section of it
/brainstorm "row-level security policies"    # topic-scoped, layer inferred by search
/brainstorm --layer G --n 8 --frames 5       # caps: shipped ideas (10), generator agents (5)
/brainstorm --prior-art "claim in one line"  # run only Step 2, on a single claim
/brainstorm --dry-run                        # print the retrieval plan and budget, generate nothing
```

---

## 1 · Source

Everything below was scanned **2026-08-26**. Every claim carries a link. Where a number came
from a secondary summary rather than the paper itself, it says so.

### 1.1 Group brainstorming: the claim, and 68 years of contradiction

Osborn's *Applied Imagination* (1953) proposed four rules — defer judgment, go for quantity,
build on others' ideas, encourage wild ideas — and the claim that interacting groups produce
far more ideas than the same people alone.
[history](https://www.regent.edu/journal/journal-of-transformative-innovation/the-history-of-brainstorming-alex-osborn/)
**Not verified against the book itself; the "twice as many" figure is repeated everywhere and
sourced nowhere I could open.**

The first controlled test found the opposite and it has not been overturned:

| Study | Design | Result |
|---|---|---|
| [Taylor, Berry & Block 1958](https://www.jstor.org/stable/2390603), *Admin. Sci. Q.* 3(1):23-47 | 12 real groups of 4 vs 48 individuals recombined into 12 **nominal** groups, same rules, same 3 problems | real groups "markedly inferior" on total ideas, unique ideas, and three quality-weighted measures |
| [Diehl & Stroebe 1987](https://www.uni-muenster.de/imperia/md/content/psyifp/aeechterhoff/wintersemester2011-12/seminarthemenfelderdersozialpsychologie/08_diehl_stoebe_productivityloss-brainstorming_jpsp1987.pdf), *JPSP* 53(3):497-509 | 4 experiments isolating free riding, evaluation apprehension, production blocking | **production blocking** — waiting your turn — accounts for most of the loss |
| [Mullen, Johnson & Salas 1991](https://www.tandfonline.com/doi/abs/10.1207/s15324834basp1201_1), *BASP* 12:3-23 | meta-analysis, face-to-face vs nominal, 1958–1990 | nominal wins on quantity **and** quality; effect sizes reported as r ≈ .57 / .56 (figures via secondary summaries, not the PDF) |
| [DeRosa, Smith & Hantula 2007](https://www.sciencedirect.com/science/article/abs/pii/S0747563205000506), *Comp. Hum. Behav.* 23:1549-1581 | meta-analysis of electronic brainstorming | the loss is **medium- and size-dependent**: large electronic groups beat nominal; nominal wins below ~8 members |

**The mechanism transfers, not the ritual.** Production blocking is a channel problem, and agents
writing in parallel to separate files have no channel to block — which is why this procedure looks
like *brainwriting* ([6-3-5](https://en.wikipedia.org/wiki/6-3-5_Brainwriting), Rohrbach 1968) and
the [Nominal Group Technique](https://gwern.net/doc/statistics/prediction/2001-rowe.pdf), not a meeting.

**Delphi**: [Rowe & Wright 1999](https://www.sciencedirect.com/science/article/abs/pii/S0169207099000187)
report it beating unstructured interaction 5 studies to 1 (3 to 1 excluding non-accuracy tasks),
but with **no clear advantage over other structured procedures** including NGT. Structure beats no
structure; which structure is unsettled. Do not sell a ritual.

**TRIZ, morphological analysis and SCAMPER** have thinner evidence than their popularity implies.
The best TRIZ result I found is a multi-institution student experiment reporting improved novelty
and variety with slightly reduced quantity
([ASEE PEER](https://peer.asee.org/experimental-assessment-of-triz-effectiveness-in-idea-generation.pdf)),
whose own framing is that TRIZ "has not been conclusively demonstrated"; SCAMPER's are classroom
pre/post designs on students
([e.g.](https://www.sciencedirect.com/science/article/abs/pii/S1871187123000524)). **This skill
uses them as frame labels only and claims no effect size for any of them.**

**Analogy and fixation** are the two findings with direct operational consequences:

- [Jansson & Smith 1991](https://www.sciencedirect.com/science/article/abs/pii/0142694X9190003F) —
  showing designers an example solution, *even one whose flaws are pointed out*, makes their
  designs share features with it. **Design fixation is real and survives being warned.**
- [Chan, Fu, Schunn et al.](https://www.designsociety.org/download-publication/30665/on_the_effective_use_of_design-by-analogy_the_influences_of_analogical_distance_and_commonness_of_analogous_designs_on_ideation_performance) —
  far-field, *less-common* analogies help; near-field common ones fixate. Findings are partly
  non-intuitive ([AI EDAM](https://www.cambridge.org/core/journals/ai-edam/article/abs/overcoming-design-fixation-design-by-analogy-studies-and-nonintuitive-findings/038760839BBBEFC08F146457A77BBE51)).

Consequence: **the layer document is itself a fixation source.** Reading §2 before generating
produces restatements of §2, so Step 3 forbids it.

### 1.2 LLM-specific, 2024–2026

| Finding | What was actually measured | Link |
|---|---|---|
| LLM ideas judged **more novel** than expert ideas, feasibility not significantly worse | 49 expert idea writers, 79 reviewers, 298 reviews, 3 conditions, Welch's t-test with Bonferroni. Novelty: human 4.84 vs AI 5.64 (p<0.01) vs AI+human-rerank 5.81 (p<0.001). Feasibility 6.61 / 6.34 / 6.44, both p=1.00 | [Si, Yang & Hashimoto, arXiv:2409.04109](https://arxiv.org/abs/2409.04109) |
| Same paper, two harder findings: **volume is mostly duplication** — 4,000 seed ideas per topic collapsed to ~200 after dedup, a **5% survival rate**; and **judging is near chance** — reviewer-vs-reviewer balanced accuracy 56.1% (vs 71.9% for ICLR 2024 papers), Claude-3.5 as pairwise judge 53.3% | their own pipeline and review data | [ibid.](https://arxiv.org/html/2409.04109v1) |
| Alignment causes **mode collapse** via typicality bias in preference data; **Verbalized Sampling** (ask for k responses *with their probabilities*) recovers 1.6–2.1× diversity in creative writing, training-free | creative writing, dialogue simulation, open-ended QA, synthetic data; more capable models benefit more | [Zhang et al., arXiv:2510.01171](https://arxiv.org/abs/2510.01171) (Oct 2025, rev. Jul 2026) |
| **Temperature is not the creativity knob.** Weakly correlated with novelty, moderately *negatively* with coherence, no relation to cohesion or typicality | narrative generation, fixed context/model/prompt, ICCC'24 best student paper | [Peeperkorn et al., arXiv:2405.00492](https://arxiv.org/abs/2405.00492) |
| Generative AI **raises individual creativity and lowers collective diversity** — AI-assisted stories are more similar to each other | online experiment, short stories, *Science Advances* 2024 | [Doshi & Hauser](https://www.science.org/doi/10.1126/sciadv.adn5290) |
| **Multi-agent debate is mostly majority voting.** Under equal compute, self-consistency matches or beats debate | several 2025 analyses | [Stop Overvaluing Multi-Agent Debate, arXiv:2502.08788](https://arxiv.org/pdf/2502.08788); [problem drift, arXiv:2502.19559](https://arxiv.org/pdf/2502.19559) |
| **Diversity collapse in multi-agent LLM ideation** — interaction itself converges outputs (Vendi-score based) | Chen et al., 2026-04-22 | [arXiv:2604.18005](https://arxiv.org/pdf/2604.18005) — **abstract-level only; I did not verify its effect sizes** |
| A contrary 2026 claim: multi-agent systems **outperform human teams** on creativity | Hu et al., 2026-05-19 | [arXiv:2605.17885](https://arxiv.org/pdf/2605.17885) — **could not extract its numbers; treat as unverified and unresolved against the row above** |

Two of these fight each other. That is the honest state of the 2026 literature and the reason
this procedure keeps agents independent by default: the failure mode is documented, the
benefit of interaction is contested.

### 1.3 Ideation for architecture, specifically

The architecture field is rich in **evaluation** and poor in **generation**.
[ATAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) is
nine steps for evaluating an architecture you already have — utility trees, scenarios,
sensitivity points, trade-off points, risks and non-risks — with CBAM adding the economics.
Neither generates candidates.

What it contributes is the **shape of a good idea record**: an idea naming its trade-off point and
the quality attribute it costs is reviewable; one that does not is a wish. The closest measured
generation work is program-level, not architecture-level —
[Beyond Code Generation](https://arxiv.org/abs/2503.06911) (CHI 2025), an IDE surfacing alternative
problem framings and tracking decisions.

### 1.4 Selection — the stage that destroys the work

[Rietzschel, Nijstad & Stroebe 2010](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1348/000712609X414204),
*Br. J. Psychol.*: after generating, people **select feasible and desirable ideas at the cost of
originality**. Generating well and selecting badly nets zero — see also Groningen's review,
[Why Great Ideas Are Often Overlooked](https://research.rug.nl/en/publications/why-great-ideas-are-often-overlooked-a-review-and-theoretical-ana/).

The standard ideation metric set is
[Shah, Vargas-Hernandez & Smith 2003](https://www.researchgate.net/publication/222672623_Metrics_for_measuring_ideation_effectiveness):
**novelty, variety, quantity, quality** — built for engineering design studies, widely reused,
adapted here rather than adopted whole.

For novelty checking against prior work there is now tooling worth copying the *method* from:
[Literature-Grounded Novelty Assessment](https://arxiv.org/abs/2506.22026) (Shahid et al., 2025) —
keyword + snippet retrieval, embedding filter, **facet-based LLM re-rank**, ~13% higher agreement
than prior approaches, with the re-ranker as the load-bearing part.

### 1.5 Tooling that exists — what to use and what is marketing

| Thing | Verdict |
|---|---|
| [Sequential Thinking MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | real, official, **wrong shape** — it serialises one chain of thought; this needs parallel independent chains. Skip. Same for [mcp-structured-thinking](https://github.com/Promptly-Technologies-LLC/mcp-structured-thinking): a markdown file under `docs/next/ideas/` is a better state store, and it diffs |
| Marketplace brainstorming skills ([obra/superpowers](https://claudemarketplaces.com/skills/obra/superpowers/brainstorming), [mcpmarket listings](https://mcpmarket.com/tools/skills/brainstorming-ideation)) | one is a useful *gate* (blocks implementation until options exist). The ones advertising "30+ research-validated prompt patterns from 14 authoritative research sources" list SCAMPER among them — **that phrase is marketing; the patterns are not validated in the sense the word implies.** Copy the gate idea, not the claim |
| [ResearchStudio-Idea](https://arxiv.org/pdf/2607.04439) (skill suite from ML conference outcomes, 2026-07) | closest published relative of this skill. **Read before extending this one**; I verified its existence and framing only |
| [AI Idea Bench 2025](https://arxiv.org/pdf/2504.14191) / [IdeaBench](https://arxiv.org/abs/2411.02429) | source of the **non-duplicate ratio** metric used in Step 4 |
| `graphify` (this repo) | the retrieval principle and the graph. Use it. Do not re-read source files |

---

## 2 · Method

### Step 0 — Scope and budget, printed before anything runs

Resolve scope to exactly one of: a layer letter, a layer plus section anchor, or a topic string.
Then print, and do not exceed:

```
Scope:      LAYER-B-UNDERSTANDING.md §3.4
Retrieval:  <= 400 lines of layer text, <= 4,000 tokens total
Generators: 5 frames x 6 ideas = 30 raw
Prior art:  <= 3 domain words x 2 searches = <= 6 web calls
Ship:       <= 10 ideas, written to docs/next/ideas/YYYY-MM-DD-<scope>.md
```

Why so small: `docs/next/LAYER-*.md` is **6,007 lines / 413 KB ≈ 103,000 tokens** and
`docs/as-built/graph/graph.json` is **5.5 MB ≈ 1.37M tokens** (measured 2026-08-26). A brainstorm
that packs either has spent its budget before having an idea.

### Step 1 — Retrieve, do not pack

Never `cat` a layer document. Never load `graph.json`. Three queries, in order:

```bash
# 1a. Heading index for the scoped layer only (~40 lines, ~600 tokens)
rg -n '^#{2,3} ' docs/next/LAYER-B-UNDERSTANDING.md

# 1b. The scoped section only, by line range from 1a
sed -n '310,330p' docs/next/LAYER-B-UNDERSTANDING.md

# 1c. What is already claimed anywhere, for the 3-6 key terms of the scope
rg -n -i --max-count 3 -C1 'impact analysis|blast radius' docs/next/*.md docs/as-built/00-INDEX.md
```

For anything about existing code, query the graph — do not open source. Symbols, then their edges:

```bash
G=docs/as-built/graph/graph.json
jq -r '.nodes[] | select(.norm_label|test("permission")) | "\(.label)  \(.source_file):\(.source_location)"' $G | head -20
jq -r --arg n 'apps_engine_src_scio_engine_layerb_architecture_permission' \
  '.links[] | select(.source==$n or .target==$n) | "\(.source) -\(.relation)-> \(.target)"' $G | head -20
```

**Record the retrieval transcript** — the exact commands and line counts — into the run file's
header. Eval case E3 checks it.

### Step 2 — The prior-art gate, before an idea exists

This is the project-wide standing rule made mechanical. It runs **before** Step 3 for the scope,
and again **per idea** in Step 6. An idea that has not passed it may not be written down.

Extract the **domain words** from the scope (at most 3). For each, in this order:
(1) the layer's own `## 5 · The means` section — every layer document has one and it is this repo's
list of what exists in that domain (`rg -n '^## 5 · ' docs/next/LAYER-*.md`); (2) the registry below,
then a web search:

| Domain word | Go here first |
|---|---|
| requirements, spec, acceptance | ISO/IEC/IEEE 29148; EARS (`.claude/skills/ears-requirements`) |
| architecture, structure, decision | ISO/IEC/IEEE 42010, arc42, C4, MADR/ADR, SEI ATAM + CBAM |
| design, tokens, UI, theme | W3C DTCG, WCAG, `.claude/skills/app-design` §1 and §6b |
| auth, permissions, roles, tenancy | OAuth 2.1 / OIDC RFCs, OpenFGA / Zanzibar, Cedar, OWASP ASVS, Postgres RLS |
| database, schema, migration | SQL standard, Postgres docs, Prisma/Drizzle migration semantics |
| testing, coverage, quality gate | ISO/IEC/IEEE 29119, ISTQB glossary, property-based testing |
| observability, tracing, cost | OpenTelemetry semantic conventions |
| code, package, dependency, licence | SPDX, the language's own registry (PyPI/npm), GitHub search |
| graph, retrieval, memory | `.claude/skills/graphify`, GraphRAG |

(3) **two** web searches — *"is there a standard for X"* and *"X existing implementation 2026"*.
Never one: the first returns the thing you already thought of.

Record per domain word: the standard or tool found, its link, and one of
**adopt · extend · differs · reinvents**. `reinvents` is a hard stop for any idea resting on it.

### Step 3 — Independent parallel generation

**Dispatch all generator agents in a single message.** Sequential dispatch leaks earlier output
into later prompts and destroys the independence the whole design rests on.

Each agent receives the Step-1 §-extract, the Step-2 prior-art table, **one frame**, and nothing
else — no other agent's prompt or output, and no layer prose beyond the scoped extract, which is the
fixation source (§1.1, Jansson & Smith). Five default frames, deliberately unlike each other:

| # | Frame | Instruction given to that agent |
|---|---|---|
| 1 | **Constraint inversion** | assume the single most load-bearing constraint in the extract is false. What becomes possible? |
| 2 | **Far analogy** | take the mechanism from a *distant, uncommon* domain — biology, logistics, compilers, aviation safety — and map it. Name the source explicitly |
| 3 | **Deletion** | which component could be removed entirely, and what would have to be true for the system to survive that? |
| 4 | **Cost inversion** | the cheapest possible version, and the version that assumes cost is not a constraint. Two ideas, both extremes, no middle |
| 5 | **Failure-first** | start from how this layer will fail in production, and generate what prevents that class |

Every agent uses **Verbalized Sampling**: *"Produce 6 candidate ideas, each with an explicit
probability reflecting how typical it is; mark the two highest-probability ones `MEDIAN`."* Keep all
six — the median stays **visible and labelled** rather than shipped by accident
([arXiv:2510.01171](https://arxiv.org/abs/2510.01171)). **Leave temperature at default**: it is
weakly related to novelty and moderately harmful to coherence
([arXiv:2405.00492](https://arxiv.org/abs/2405.00492)). Diversity comes from frames, not the sampler.

### Step 4 — Pool, dedup, and measure the pool before touching it

Pool the 30. Deduplicate by claim, not by wording. Then compute and print:

```
Raw: 30   Unique: 17   Non-duplicate ratio: 0.57
Frames represented after dedup: 5/5
MEDIAN-labelled share: 4/17
```

Rules that fire on these numbers:

- **Non-duplicate ratio < 0.50** → mode collapse. Discard the pool, change at least three frames,
  rerun Step 3 **once**; if it fails again, report the failure rather than ship a collapsed pool.
- **Fewer than 4 of 5 frames surviving** → one frame dominated. Name it in the run file.
- Reference point, not target: Si et al.'s pipeline survived dedup at ~5%
  ([arXiv:2409.04109](https://arxiv.org/html/2409.04109v1)). A ratio of 1.00 means the frames were
  not exploring the same problem.

### Step 5 — One cross-read pass, additive only

Only now may agents see each other's output — **one pass, and it may only add**. It may not edit,
merge, rank, or delete another agent's idea. No debate rounds: under equal compute, debate is
approximately majority voting ([arXiv:2502.08788](https://arxiv.org/pdf/2502.08788)), it drifts
([arXiv:2502.19559](https://arxiv.org/pdf/2502.19559)), and interaction is the documented cause of
diversity collapse ([arXiv:2604.18005](https://arxiv.org/pdf/2604.18005)).

Ideas born here are tagged `generation: cross-read`, are the only permitted combinations, and are capped at 5.

### Step 6 — Per-idea prior-art gate, then record

For **each surviving idea**, rerun Step 2's search on that idea's own domain words, then apply the
[Idea Novelty Checker](https://arxiv.org/abs/2506.22026) shape by hand: retrieve broadly, re-rank on
the *facet the idea claims*, not on topic similarity. Two ideas about "permissions" are not prior
art for each other if one claims a policy language and the other a storage model.

- **reinvents** → `status: rejected-reinvents`, kept in the file with its link. Not deleted: the
  rejection is the evidence the gate ran.
- **extend / differs** → shippable; the record must say *how* it differs, in one sentence.
- **adopt** → not an idea but a dependency proposal. Record it as `adopt` and move on.

### Step 7 — Select without collapsing to the median

Two scorers (subagents, independent, single dispatch), each scoring every idea **0–5 novelty and
0–5 feasibility, separately**. **Never sum or average the two** — feasibility bias is the documented
mechanism by which good ideas die at selection
([Rietzschel et al. 2010](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1348/000712609X414204)),
and a combined score is that bias in arithmetic form. Ship, in this order:
1. Top 3 by **novelty**, whatever their feasibility.
2. Top 3 by **feasibility**, whatever their novelty.
3. Any idea in both lists, marked `both`.
4. Fill to `--n` by scorer disagreement — **the widest-disagreement ideas first**, because
   agreement near chance means disagreement carries more information than the mean does.

Print the two scorers' agreement rate and this sentence verbatim in the run file:

> Idea scoring is near chance. Human expert reviewers agreed 56.1% and an LLM judge 53.3% in the
> only head-to-head measurement we have ([arXiv:2409.04109](https://arxiv.org/html/2409.04109v1)).
> These scores order the file. They do not decide anything.

Decisions come from Step 8's falsifiers, tested downstream — not from the scores.

### Step 8 — Write the run file, then stop

Write `docs/next/ideas/YYYY-MM-DD-<scope>.md` in the §3 contract. **Do not commit** — `/checkpoint`
owns that — and do not open an ADR. Ideas that survive validation become proposals in the layer
document's `## 9 · ADR proposals`, which is where this repo already puts them.

---

## 3 · Output contract

One header block, then one section per idea. Fixed keys, in this order, so a validation stage can
parse it with `rg` and a fixed grammar.

```markdown
# Brainstorm — LAYER-B §3.4 — 2026-08-26

retrieval:  rg headings (39 lines) + sed 310-330 (21 lines) + rg terms (14 lines) = 74 lines
frames:     5 | raw 30 | unique 17 | non-duplicate-ratio 0.57 | cross-read +3
scoring:    2 scorers, agreement 0.61 — near chance, ordering only
shipped:    9 | rejected-reinvents 2 | adopt 1

## B34-01 · Impact set as a build-plan input, not a review output
- claim: the impact set computed from the graph becomes an input to Layer C's plan, so the planner
  sizes packages by blast radius rather than by file count.
- replaces_or_adds: adds to LAYER-B §3.1 (impact analysis exists there as a review artefact only)
- prior_art:
  - [SEI ATAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) — sensitivity/tradeoff points, evaluation-time only — **differs** (ours is plan-time, computed)
  - `.claude/skills/change-impact-analysis` — **extend**
- would_have_to_be_true:
  - graph edges predict change fan-out better than file adjacency, over >= 20 real commits
  - computing the impact set costs < 2s on 5,173 nodes
- costs: plan latency, to buy rework rate
- frame: 3 (deletion) | generation: independent | median: no
- novelty: 4, 3 | feasibility: 3, 4 | disagreement: 1
- status: proposed

## B34-07 · A requirement-completeness percentage
- claim: score each requirement 0-100% for completeness, gate the build on the mean.
- prior_art: [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) — 11 named characteristics of a good requirement — **reinvents**
- status: rejected-reinvents · note: this repo made this exact mistake once, `docs/next/LAYER-A-INTAKE.md:188`
```

Required keys per idea: `claim`, `prior_art` (>= 1 entry, each with a link and a verdict),
`status`. Required unless `status: rejected-*`: `replaces_or_adds`, `would_have_to_be_true`
(>= 2, each falsifiable), `frame`, `generation`, `novelty`, `feasibility`.

A `would_have_to_be_true` entry that cannot be tested by a command, a measurement, or a document
lookup is not one. "It would have to be a good idea" fails.

---

## 4 · Failure modes and their countermeasures

| Failure | Looks like | Countermeasure, and where it lives |
|---|---|---|
| **Converging on the median** | five ideas that are one idea in five registers; everything sounds reasonable | Verbalized Sampling with explicit `MEDIAN` labelling (Step 3); non-duplicate ratio gate < 0.50 (Step 4); five deliberately unlike frames |
| **Restating the document** | an idea whose key phrase already appears in `docs/next` | design fixation, Jansson & Smith 1991. Generators never see §2/§4 prose (Step 3); eval E6 greps every claim's key phrase against `docs/next/*.md` |
| **Reinventing a standard** | a coverage percentage; a bespoke token shape; a hand-rolled policy language | the Step-2 gate before generation and the Step-6 gate per idea; `reinvents` is a hard stop; rejected ideas stay in the file as proof the gate ran |
| **Volume instead of signal** | 40 ideas, no falsifiers | hard cap `--n 10`; every shipped idea needs >= 2 testable `would_have_to_be_true` entries; unfalsifiable ideas are dropped, not padded |
| **Collapse at selection** | only feasible ideas survive | novelty and feasibility never combined; top-3-by-novelty ships regardless of feasibility (Step 7) |
| **Interaction eating diversity** | agents agreeing after a debate round | no debate; one additive-only cross-read pass (Step 5) |
| **Budget burned on context** | the run reads 6,000 lines and then thinks | Step 0 caps and Step 1 commands; the retrieval transcript is written into the file and checked by E3 |
| **Confusing a scan for a source** | citing a marketplace blurb as evidence | §1.5 verdicts; anything unverified is labelled unverified, per `docs/next/SKILLS.md` |

---

## 5 · Limits

**Mandatory reading before trusting anything above.**

- **The human evidence is about humans.** Production blocking, evaluation apprehension and social
  loafing are properties of people in rooms. That parallel independent agents avoid the same
  losses is an **assumption**, supported only indirectly by the multi-agent diversity-collapse
  result ([arXiv:2604.18005](https://arxiv.org/pdf/2604.18005)), whose effect sizes I did not verify.
- **The 2026 literature contradicts itself** on whether multi-agent systems help creativity
  ([arXiv:2605.17885](https://arxiv.org/pdf/2605.17885) vs the above). This procedure takes the
  conservative branch. It could be the wrong branch.
- **Si et al. measured NLP research ideas judged by NLP researchers**, not architecture proposals.
  Their novelty result does not transfer; the dedup and judge-agreement numbers are about pipelines,
  and are the parts this skill leans on.
- **Verbalized Sampling's 1.6–2.1×** is creative writing. There is **no measurement of VS on
  architecture ideation**. It is used here because it is training-free and cheap to abandon.
- **Shah et al.'s novelty/variety metrics** were built for engineering design sketches; Step 4's
  non-duplicate ratio is borrowed from [AI Idea Bench 2025](https://arxiv.org/pdf/2504.14191) and is
  not a validated instrument.
- **TRIZ, SCAMPER and morphological analysis appear here as frame labels only.** No effect size
  is claimed for any of them, and the frames in Step 3 are not any of those methods.
- **The thresholds are conventions, not findings.** 0.50 non-duplicate ratio, 5 frames, 6 ideas,
  cap of 10, 400 lines of retrieval — chosen for budget, not measured.
- **This procedure has never been run.** It has no eval results yet. §6 says how to get them.

---

## 6 · Eval

Runnable cases. Each states its check. Cases E1 and E2 are designed to **fail an idea** — a run
that ships them is broken.

**E1 — must reject: design tokens.**
`/brainstorm --prior-art "give each generated app a JSON file mapping semantic colour names to hex values"`
→ Expected: `status: rejected-reinvents`, prior art
[W3C DTCG](https://www.designtokens.org/tr/drafts/format/), and a pointer to
`.claude/skills/app-design` §1. **Shipping this as a novel idea is a hard failure.**

**E2 — must reject: a coverage percentage.**
`/brainstorm --prior-art "score every requirement 0-100% for completeness and gate on the mean"`
→ Expected: `rejected-reinvents`, prior art
[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html), note citing
`docs/next/LAYER-A-INTAKE.md:188`.

**E3 — retrieval budget.** `/brainstorm --layer G --dry-run`
→ Check: the plan reads ≤ 400 lines; the transcript contains no `cat` of a `LAYER-*.md` and no read
of `graph.json`.

**E4 — independence.** `/brainstorm --layer B --anchor 3.4`
→ Check: 5 generator agents dispatched in one message; no generator prompt contains another
generator's output; ≥ 5 shipped ideas tagged `generation: independent`.

**E5 — diversity floor.** Same run.
→ Check: `non-duplicate-ratio ≥ 0.50` in the header and ≥ 4 of 5 frames among shipped ideas. Below
the floor the expected behaviour is **one reframe and rerun, then an honest failure report** — not
a shipped pool.

**E6 — no restatement.** For each shipped `claim`, take its most distinctive 4-word phrase and run
`rg -i -c "<phrase>" docs/next/*.md`. Expected: 0 hits. A hit means the idea was retrieved, not
generated; status must become `restatement` and it must not ship.

**E7 — selection does not collapse, and ideas are falsifiable.** The shipped set contains ≥ 1 idea
with feasibility ≤ 2 and novelty ≥ 4 (if every shipped idea is feasible, Step 7 was skipped), and
every shipped idea has ≥ 2 `would_have_to_be_true` entries each naming a command, a number, or a
document.

Record results in the run file header as `eval: E1 pass … E7 pass`. An unrecorded eval line means an
unmeasured run.

---

## Sources

All scanned **2026-08-26**; every link is inline above, at the claim it supports. The load-bearing
ones are Taylor/Berry/Block 1958, Diehl & Stroebe 1987, Mullen et al. 1991 and DeRosa et al. 2007
(nominal vs interacting); Jansson & Smith 1991 and Chan/Fu/Schunn (fixation and analogy);
Rietzschel et al. 2010 and Shah et al. 2003 (selection and metrics);
[arXiv:2409.04109](https://arxiv.org/abs/2409.04109) (the dedup and judge-agreement numbers);
[arXiv:2510.01171](https://arxiv.org/abs/2510.01171) and
[arXiv:2405.00492](https://arxiv.org/abs/2405.00492) (sampling and temperature);
[SEI ATAM/CBAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/);
[arXiv:2506.22026](https://arxiv.org/abs/2506.22026) and
[arXiv:2504.14191](https://arxiv.org/pdf/2504.14191) (novelty checking, non-duplicate ratio).

**Not verified:** Osborn's original quantitative claim (book not opened); the Mullen et al. effect
sizes (secondary summaries only); the effect sizes in [arXiv:2604.18005](https://arxiv.org/pdf/2604.18005)
and [arXiv:2605.17885](https://arxiv.org/pdf/2605.17885) (abstract and metadata only);
[arXiv:2607.04439](https://arxiv.org/pdf/2607.04439) beyond its framing; Heslin 2009 and
Paulus & Yang 2000 on brainwriting, which reached me only through vendor summaries and are
therefore **not cited above as evidence**.
