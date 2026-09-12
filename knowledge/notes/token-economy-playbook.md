---
title: Token economy playbook — what is measured about saving tokens, and the policy it implies
sources:
  - url: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
    note: "Minimum cacheable prefix per model, 1.25×/2× write and 0.1× (0.025× on Fable 5.1) read multipliers, four breakpoints, tools→system→messages order, entry available only after the first response begins."
    fetched: 2026-09-02
  - url: https://platform.claude.com/docs/en/about-claude/pricing
    note: "Fable 5.1 $10/$50, Opus 5 $5/$25, Sonnet 5 $2/$10, Haiku 4.5 $1/$5 per MTok; Batch 50%; 1M context at standard price; 4.7+ tokenizer ~30% more tokens on the same text."
    fetched: 2026-09-02
  - url: https://stevescargall.com/blog/2026/05/graphify--memmachine-79-token-reduction-zero-vector-database/
    note: "The one independent graphify measurement; graded in [[graphify-assessment]]."
    fetched: 2026-08-29
  - path: intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-B-UNDERSTANDING.md
    note: "§7 at line 579 — measured 2026-08-26, chars÷4, ±15%."
  - path: intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-C-BUILD-PLAN.md
    note: "§7 at line 714 — 65% repeated bytes, floor table."
  - path: intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-E-BUILD.md
    note: "§7 at line 768 — call counts, CODEGEN_SYSTEM 459 tokens, four caching blockers."
  - path: intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-F-DESIGN-WINDOW.md
    note: "§7 at line 786 — 77% untouched files, −51% and −100% scenarios."
  - path: intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-G-CROSS-CUTTING.md
    note: "§7 at line 787 — price table with the Sonnet 5 row 50% high; ledger prices cache reads at full rate."
  - path: knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0001-graph-is-standard.md
    note: "The observation appended 2026-09-02 lives in Scio at commit 0776d94; the raw copy here predates it. Quoted below."
tags: [tokens, cost, prompt-caching, retrieval, graphify, batch-api, policy, measured]
related: ["[[graphify-assessment]]", "[[claude-code-ecosystem-plugins]]", "[[graphify-features]]", "[[skill-anatomy]]", "[[claude-code-extension-layer]]", "[[model-routing-free-and-local]]", "[[third-party-landscape]]", "[[model-agnostic-agent-harnesses]]"]
raw:
  - intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-B-UNDERSTANDING.md
  - intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-C-BUILD-PLAN.md
  - intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-E-BUILD.md
  - intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-F-DESIGN-WINDOW.md
  - intake/2026-08-30-agent-and-skill-material/scio/docs/next/LAYER-G-CROSS-CUTTING.md
  - knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0001-graph-is-standard.md
---

# Token economy playbook

Written 2026-09-02 to answer one question: *be as token-aware as possible — graphify or
similar — what do we actually know?* The answer is that the knowledge base holds a dozen
**measured** numbers about where tokens go, and they do not point at graphify first. They
point at output tokens, repeated constants, and files sent that are never touched. Graphify
is fourth on the list and only for code questions. Every number below carries its
MEASURED / REPEATED / DERIVED grade; the chars÷4 estimates from Scio's layer documents are
MEASURED on real prompts but ±15% until re-run with `count_tokens`.

## 1. Where tokens go — three sinks, not one

| sink | what it is | who owns it here |
|---|---|---|
| **every-turn overhead** | CLAUDE.md, the skill listing (descriptions authored to ≤1,024 chars; **measured 2.26% of a 1M window in total, 2026-09-08** — see §1.1, and never cite a pinned share), agent descriptions (15,000-token shared budget), MCP tool schemas | `context-budget` ranks the components; `steering-doc-pruning` cuts inside one; [[skill-anatomy]] has the loading economics |
| **retrieval** | what is read to answer a question: whole files vs a section vs a graph query | `kb.py find/read` for documents; graphify for code; [[graphify-assessment]] |
| **the generation loop** | what a product's own model calls send and re-send: constants, prior answers, untouched files, repair rounds | prompt caching, Batch API, prompt ordering, deterministic edits — the Scio §7 measurements below |

Most advice online is about the first sink. Most money in a builder like Scio is in the
third. The independent graphify figure is about the second, and only for code.

### 1.1 Our own every-turn overhead, measured — and the "~1%" it replaces

**MEASURED 2026-09-08** by `pipeline/queries/context_surface.py`, over this repository:

| component | n | bytes | ~tokens | share of 1M |
|---|---|---|---|---|
| `CLAUDE.md` | — | 22,936 | ~5,734 | 0.57% |
| skill descriptions | 89 | 66,047 | ~16,511 | **1.65%** |
| agent descriptions | 3 | 1,387 | ~346 | 0.03% |
| **total always-on** | 92 | 90,370 | **~22,592** | **2.26%** |

> **The denominator is not 1M, and the source now says so (MEASURED 2026-09-11).** `model-config`
> adds: *"Models running with a native 1M window, such as Sonnet 5, the Fable models, and Opus 4.7
> and later on the Anthropic API, compact before the window fills, at **about 967K tokens by
> default**."* The window a session actually fills is ~3.3% smaller than the one every share in
> this table is divided by, so the honest figure is **2.34%, not 2.26%** — +0.08 points.
>
> **Small, and worth recording for the shape rather than the size.** It is the same error class
> this file already tracks twice (a pinned running statistic, and a promotional price quoted as a
> standing one): a number that is *correct against the wrong reference*. Nothing here needs
> recomputing — `pipeline/queries/context_surface.py` divides by a constant, and the constant it
> should divide by is the compaction threshold for the model in play, which varies by provider
> (the same sentence continues into different behaviour on Bedrock and Google Cloud's Agent
> Platform). Recorded as a limit on the figure, not as a new figure, because a second pinned
> constant is not the fix for the first.

Tokens are `bytes ÷ 4` and are stated as an estimate: no tokenizer is available offline, and
`count_tokens` on this surface is still on the unmeasured list below.

**Two things this corrects.** The "~1% of the window" that stood in the table above, and in
CLAUDE.md itself, understated the descriptions by roughly 70% — not because it was wrong when
written, but because **it is a running statistic that was pinned as a constant** in the file every
turn reads. `pipeline/CONSTANTS.md` already states that rule, about a different value: *"a value
that moves on its own must be recorded as a finding plus a pointer to its live computation, never
as a number. A pinned number that drifts is worse than no number, because it is cited with the
authority of this file."* It had a pointer for the over-cap count and none for the share. Both
documents now cite the script instead of a figure.

**And the ranking it does not change.** 2.26% is still the *first* sink and still the smallest —
§3's ordering stands. What the measurement buys is that the number can now be re-run rather than
re-remembered, and that a future growth in the library shows up as a share rather than as a
surprise. The one figure worth watching is the descriptions': at 89 skills it is 1.65%, so the
listing costs about **0.019% of the window per talent**, and the library is the component that
grows on purpose.

**Where CLAUDE.md's own 5,734 tokens go, and the one number that changes the picture.** Measured
the same day, same script:

| section | ~tokens | share of the file |
|---|---|---|
| preamble | 212 | 3.7% |
| Standing rules (always) | 1,454 | 25.4% |
| Domain scope | 73 | 1.3% |
| **Capability map (job → talent)** | **3,886** | **67.8%** |
| Description discipline | 104 | 1.8% |

The capability map is **two-thirds of the steering file**, and it names **91 of the 92 loaded
talents** — whose own descriptions are already loaded, at 16,511 tokens. So the library carries
**two routing indexes in the always-on surface**, and the map is a ~24% surcharge on the mechanism
that actually routes. CLAUDE.md's own preamble said "this file does NOT list them all"; measured,
it lists 99% of them, and that line has been corrected.

**This is a finding, not a cut.** The map is not redundant text — its content is the
*cross-library discriminators* ("X → A, NOT B which does Y") that a single skill's description
structurally cannot carry, which is the job `capability-routing-table` exists for. Whether 3,886
tokens per turn is the right price for that is a judgement about the repo's steering document, and
it belongs to a human, not to a curation pass. What the measurement changes is that the question
can now be asked with a number instead of a feeling.

**And there is no slack to reclaim in the descriptions themselves — measured, negative result.**
An n-gram sweep over all 92 descriptions found **111 bytes** of phrasing repeated across four or
more of them, out of 67,434 — **0.16%**. No 5-gram or 6-gram repeats at all. So the 16,511 tokens
are 16,511 tokens of distinct content: any reduction has to cut *meaning*, which changes routing.
Recorded so nobody "optimises" the description surface on the assumption that boilerplate is
hiding in it.

**The ceiling that matters is not the cap, and three descriptions are close to it.** The 1,024
cap is what we author to (spec). The **1,536** is where Claude Code truncates `description` +
`when_to_use` combined in the listing — re-verified 2026-09-08 against the docs bytes held at
`knowledge/raw/claude-code-docs-2026-09-04b/skills@2026-09-04b.md`, unchanged. **0 of 92** units
use `when_to_use`, so the whole budget is the description's. Headroom to the wall:

| talent | chars | left |
|---|---|---|
| `data-contract-assertions` | 1,446 | **90** |
| `llm-eval-harness` | 1,445 | 91 |
| `oracle-weakening-audit` | 1,442 | 94 |

Truncation takes the **tail**, and the house style puts the NOT-clauses at the tail — so the next
disambiguator added to any of those three is the one that vanishes from the listing the model
routes on, with nothing reporting it. `pipeline/queries/preflight.py` now gates it: crossing 1,536
is a distinct, harder finding than exceeding 1,024, with a warning inside 100 characters. This is
the repo's own "a convention, not a gate" failure class, closed for this one.

**Also measured, and already known:** 13 of 92 descriptions exceed the authored 1,024-char cap
(max 1,446). That is a tracked open violation with its own live count, not a new finding — see
`pipeline/CONSTANTS.md`, which is explicit that trimming changes routing and each is an edit with
a trigger check rather than a mechanical truncation.

## 2. The numbers, graded

### 2.1 Retrieval

- **Graphify, independent (MEASURED, Scargall on MemMachine, 7,441 nodes):** naive scan
  ~496k tokens per question → graph query ~6.2k, **79.6×**, with a spread of 227–713× on
  local questions and 48–62× on broad traversals. Vendor's own 71.5× / 26.1× have no
  published method. The semantic (document) pass cost ~1.4M input tokens on that repo →
  **payback ≈240 queries**; below that the graph costs more than reading files. Code-only
  AST extraction is ~0 LLM tokens. ([[graphify-assessment]])
- **Forcing graph context into every call can cost more (MEASURED, controlled, rival tool):**
  Graft, 162 runs, +42% tokens and +46% tool calls when graph context was injected
  regardless of question ([[claude-code-ecosystem-plugins]], which holds Graft's row and the
  n=50 caveat on its SWE-bench figure). Same shape as codebase-memory-mcp's "99.2% fewer
  tokens", which is one hand-picked query against a 412k-token strawman
  ([[graphify-assessment]]). *Both halves of this sentence previously pointed at
  `graphify-assessment`, which contains no occurrence of "Graft" — a reader crossing that link
  found nothing. Corrected 2026-09-08.*
- **Zero graph queries in a real session (MEASURED, 2026-09-02, Scio ADR-0001 addendum):**
  a full working session on Scio — the fresh-eyes review, thirteen ADRs, the knowledge
  merge — ran no `graphify query/explain/path/affected` at all and about twenty-five
  section-index queries. The `SessionStart` hook did not run, no `post-commit` hook was
  installed, and graphify's "inject before every file search" mode is installed in none of
  the three repositories. The graph existed (5,173 nodes, 12,054 edges); nobody asked it
  anything, because no code was written and every question was about documents, decisions
  and talents. Quoting the ADR: *"The policy this implies is not 'graphify on every call'
  but 'graph on every code question, counted'; the counter is still the missing number."*
- **Section index vs file (MEASURED on Scio, 2026-09-02):** the ADR addendum measured the
  section index answering "at a sixteenth of the file" for the questions that session
  asked. Retrieval by heading, no model call, rebuilt in half a second
  (`knowledge/kb.py`, `knowledge/VAULT.md`).

### 2.2 The generation loop — Scio's own measurements (2026-08-26, chars÷4)

| finding | number | where |
|---|---|---|
| Layer C sends the same bytes six times: `why` + house rules | **5,358 of 8,225 tokens = 65%**; the package-specific content is 2,870 | LAYER-C §7 |
| Contract text alone per marketplace build (9 packages × 4 passes) | **≈103,400 tokens ≈ $0.52** at Opus 5; the two constants (playbook + whole) ≈ $0.20 of it | LAYER-B §7 |
| The playbook alone cannot cache | 668 tokens, under every floor except Opus 5/Fable's 512 | LAYER-B §7 |
| `CODEGEN_SYSTEM` is under the Opus 5 floor | **459 tokens vs 512** — `cache_control` would report nothing and cache nothing | LAYER-E §7.2 |
| System prompt sent as a string | no content block → nowhere to put a breakpoint (`provider.py:170,178`) | LAYER-E §7.2 |
| Instruction-first ordering | the varying instruction opens the user turn, so the constant prefix is broken on pass 2+ | LAYER-E §7.2 |
| Constants at the end of the contract prompt | `contract.py:192-198` — none of the constant block is a prefix today | LAYER-C §7.1 |
| Repair round of one feature package | ≈96k in / ≈32k out → **$0.48 in, $0.80 out**; input is 37% of that call | LAYER-E §7.1 |
| Relay calls per build | **29** if every package passes first time, **79** if every package needs three attempts | LAYER-E §7.1 |
| Directed change: files that will not be touched | **77% of input** (2,321 of 2,999 tokens) | LAYER-F §7.1 |
| Directed change scenarios | drop Layer B call −13%; + contract −9%; + dependency-complete file set **−51%**; deterministic property edit **−100%** | LAYER-F §7.1 |
| Ledger prices cache reads at full input rate | `_cost` reads only `input_tokens`/`output_tokens`; any caching would be invisible to the ledger and over-reported ~10× | LAYER-G §7.1 |
| Price table wrong for Sonnet 5 | $3/$15 (Sonnet 4.6's card) vs $2/$10 list — over-charges 50% in seven places | LAYER-G §7.1–7.2 |

The order of magnitude: the whole caching fix is worth ≈ $0.41 per build (4.5–17% depending
on repair rounds); the file-set fix on directed changes is worth 51% of that call; a
deterministic edit is worth 100% of it; and one repair round's *output* costs more than
all the contract text in the build.

### 2.3 The mechanics that decide whether caching works (MEASURED, platform docs 2026-09-02)

| fact | value |
|---|---|
| minimum cacheable prefix | **Fable 5.1 / Opus 5: 512** · Opus 4.8, Sonnet 5, Sonnet 4.6: 1,024 · Opus 4.7: 2,048 · Opus 4.6, **Haiku 4.5: 4,096** |
| cache write | 1.25× input (5-minute TTL), 2× (1-hour) |
| cache read | 0.1× input; **0.025× on Fable 5.1** — a cached Fable read is $0.25/MTok, cheaper than a fresh Haiku token |
| breakpoints | at most 4 per request |
| prefix order | `tools → system → messages`; a change at one level invalidates it and everything after |
| availability | a cache entry exists only **after the first response begins** — parallel calls sent at once all miss; warm once, then fan out |
| below the floor | no error; `cache_creation_input_tokens: 0` |

The floor is **non-monotonic across models**, so it is a *routing* hazard: sending a call
that caches on Opus 5 to Haiku 4.5 raises the floor eightfold and silently caches nothing.

### 2.4 Prices (MEASURED, pricing page 2026-09-02, per MTok)

Fable 5.1 $10 / $50 · Opus 5 $5 / $25 · Sonnet 5 $2 / $10 · Haiku 4.5 $1 / $5 · Batch API
50% off · 1M context at standard price · the 4.7+ tokenizer yields ~30% more tokens on the
same text than the older one. Output is five times input on every card, which is why
"fewer passes" beats "shorter prompts" whenever both are available.

## 3. The policy, ranked by measured size

1. **Cut output before input.** Every card prices output at 5× input, and a repair round's
   output ($0.80) exceeds its input ($0.48) and the whole build's contract text ($0.52).
   Measure `codegen_passes = 4` against 2; stop a pass when the review says nothing changed;
   make the deterministic edit (−100%) the first branch, the model call the fallback.
2. **Send only what the call can touch.** Dependency-complete file set instead of the whole
   package (−51% on a directed change, 77% of that input was dead weight). The contract
   costs $0.007 and buys the rules; the file scoping pays for it eighteen times.
3. **Cache the constant prefix — properly.** Constants first, breakpoint after them;
   `system` as content blocks, never a string; a test that asserts the constant prefix is
   above the floor *of the model the call is routed to*; verify with
   `usage.cache_read_input_tokens` (zero means something in the prefix varies — dictionary
   ordering is the first suspect); the ledger must price cache-read and cache-write tokens
   at their own rates or it lies in both directions; warm the cache with one call before a
   parallel fan-out.
4. **Batch API for anything not latency-bound.** 50% off. In a builder that is the
   antichain of independent packages, every eval run, every harvest grading pass, and the
   whole `library-curator` loop.
5. **Retrieve, do not pack.** Documents: a section from the index, never the file. Code:
   graph query for *what calls what / what breaks if this changes*, code-only extraction so
   the build is free, and a **query counter** — the number this repository still does not
   have. Never inject graph context into every call (Graft, +42%;
   [[claude-code-ecosystem-plugins]]). Graphify is not a token
   saver for a markdown knowledge base; the wikilinks and the section index already are the
   graph there.
6. **Trim the every-turn overhead once, then on a cadence.** `context-budget` to rank,
   `steering-doc-pruning` to cut; keep descriptions triggers-only and short; edit CLAUDE.md
   in batches, because every edit invalidates the cached prefix of every subsequent turn.
7. **Route constrained calls down a tier, with the floor in mind.** Classification,
   grouping and yes/no judgements at temperature 0 belong on Haiku 4.5 or Sonnet 5 with
   low effort — but a Haiku call caches nothing under 4,096 tokens, so a small routed call
   never expects a cache hit. Generation that the product's promise rests on stays on the
   model the skills were measured on ([[model-routing-free-and-local]]).
8. **Count tokens before pricing anything.** chars÷4 is ±15%; `count_tokens` is a
   twenty-minute job; the Scio price table was wrong by 50% for a whole model and nothing
   noticed because the ledger consumed the table rather than the API.

## 4. What is still unmeasured

- The graph **query count** per session — the only number that would settle "graph on
  every code question" against "graph never asked".
- Real `count_tokens` on the Scio prompts, and `cache_read_input_tokens` after the reorder.
- Real `count_tokens` on **our own always-on surface** (§1.1): the 2.26% is bytes÷4, and the
  bound that matters is whether markdown with heavy punctuation runs above or below 4 B/token.
- Cache hit rates inside a Claude Code session (not observable from the CLI; the
  Agent SDK's `usage` is).
- Every skill re-measured on Fable 5.1 (Scio ADR-0008): a skill that saved tokens on Opus
  may add tokens on a model that already does the thing.
