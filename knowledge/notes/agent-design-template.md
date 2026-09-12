---
title: Agent design template — how to layer an agent
sources:
  - url: https://code.claude.com/docs/en/sub-agents
    note: frontmatter, what loads into a subagent, depth/concurrency limits
    fetched: 2026-08-28
  - url: https://code.claude.com/docs/en/skills
    note: skill directory anatomy, compaction re-attach budget
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/memory
    note: .claude/rules/ and paths-scoped loading
    fetched: 2026-08-27
tags: [agents, subagents, skills, rules, hooks, design, template]
related: ["[[claude-code-extension-layer]]", "[[subagents]]", "[[skill-anatomy]]", "[[claude-md-and-memory]]", "[[hooks]]", "[[dynamic-workflows]]", "[[architecture-evidence]]", "[[llm-idea-generation]]", "[[design-fixation-and-anchoring]]", "[[requirements-discovery]]", "[[agent-builder-prior-art]]", "[[api-agent-loop]]", "[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[anthropic-skill-authoring-contract]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/skills@2026-09-04.md
  - knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md
  - "partial: 2 of 3 distinct source URLs kept as raw; the rest predate the raw layer (2026-09-02)"
---

# Agent design template — how to layer an agent

The hub note [[claude-code-extension-layer]] answers *which feature to reach for*.
This note answers *how to build one agent well* and *how agents compose*. It joins
the mechanics notes to the measured evidence in [[architecture-evidence]],
[[llm-idea-generation]] and [[design-fixation-and-anchoring]].

**The organising principle: layer by WHEN something is needed, not by what it is.**
A rule, a template and a reference document may all be needed; they belong in
different tiers because they are needed at different moments.

**Why, precisely — and it is NOT that you would run out of room.** Against Opus 5's
**1,000,000-token** context (128k max output), the skill bodies in this library are a small
fraction of the window. **The three numbers that stood here — 84 skills, ~176,000 tokens, 18% —
were a running statistic pinned as constants, undated, in a page that does not own the measured
surface.** Measured 2026-09-08: **89 bodies, ~167,597 tokens, 16.8%**
(`python3 pipeline/queries/context_surface.py`, which prints "Do not copy one into a document as
a constant — cite this script"). Cite the script, not this line; the argument below survives any
of these values, which is why it was safe to pin them and wrong anyway. Room is not the binding
constraint, and an
argument built on scarcity would collapse the next time the window grows. The three
real reasons:

1. **Quality, measured.** SkillsBench: 1–3 preloaded modules ≈ **+19.0pp**, 4+ ≈
   **+10.1pp**. More performed *worse* with the window nowhere near full. This is
   about attention and dilution, not tokens — so it survives any context size.
2. **Silent truncation at compaction.** Claude Code re-attaches the most recent
   invocation of each skill at **5,000 tokens per skill against a 25,000-token
   shared budget**, most recent first. A bigger window delays compaction; it does
   not change what happens at it, and the loss is not announced.
3. **The system prompt shapes every turn.** An agent's body replaces the standard
   system prompt. Length there costs judgement, not capacity.

**Hard shared budget to design against:** the **combined descriptions of all
non-built-in subagents must stay under 15,000 tokens**, or Claude Code warns at
startup. Per-agent that is generous — a 475-character description is ~120 tokens —
but it is shared across the roster, so it bites as the roster grows rather than
when any single agent is written. There is **no documented size cap on an agent
body at all**. See [[subagents]] for the full limit table and what is explicitly
undocumented.

## The six tiers

| Tier | Loads | Price | Contents |
|---|---|---|---|
| **0 · Identity** | every invocation | paid always → keep small | who, what it may never do, **the map** of its functions |
| **1 · Functions** | full body at start | 5,000 each, 25,000 shared → **max 3** | the numbered procedures |
| **2 · Conditional rules** | when a matching file is opened | **zero until triggered** | conventions bound to certain paths |
| **3 · Knowledge** | when a step points at it | **zero until read** | principles, research, failure-mode lists — unbounded |
| **4 · Templates** | at the emit step | zero until read | the shape of what gets written |
| **5 · Walls** | never read — executed | **zero context** | what must be impossible to bypass |

Only tier 1 is expensive. Everything else can be as large as you like.

```
.claude/
  agents/architect.md              # 0: identity, boundary, the map
  rules/
    evidence-discipline.md         # 0: always on (no paths:)
    adr-conventions.md             # 2: paths: docs/decisions/*
    layer-direction.md             # 2: paths: apps/engine/**
  skills/
    _shared/failure-modes.md       # 3: shared by two functions
    architecture-decision/         # FUNCTION 1
      SKILL.md                     # 1: the procedure, preloaded
      reference/*.md               # 3
      templates/adr.md             # 4: empty fields
      antipatterns/*.md            # 3: negative examples
      evals.md                     # never loaded. The test.
    system-decomposition/          # FUNCTION 2
    architecture-review/           # FUNCTION 3
  hooks/docs-only-write.sh         # 5
```

## Where a thing belongs

| Question | Answer |
|---|---|
| Does it have numbered steps? | **skill** |
| Is it true regardless of the task? | **rule** |
| Needed only sometimes, at one step? | **reference** |
| Must it be impossible to bypass? | **hook** |
| Does the value move on its own? | **fetch it, never write it down** |

`SKILL.md` should be the **shortest complete statement of the steps**, each step
naming the file it opens — *"Step 4 · Open `_shared/failure-modes.md`. One row per
mode, including rows that say nothing-here."* This is the pattern Anthropic's own
security agent uses: a 16,300-word corpus on disk, 2,400–5,700 words loaded per
run.

**Tier 3 has a stated depth limit.** [[anthropic-skill-authoring-contract]] records
Anthropic's hard rule — keep references **one level deep** from SKILL.md — with the failure
mode named: a file reached from another referenced file may be previewed (`head -100`)
rather than read, so a nested chain of references loads incompletely and reports no error.
A step must open its reference directly, not a file that points at one.

## Rules

A file in `.claude/rules/` **without** `paths:` loads at start. **With** `paths:`
it loads only when a matching file is read — layer rules are absent from context
until someone touches the engine.

**MEASURED 2026-08-28 — `.claude/rules/` does NOT reach a subagent.** A canary
probe (unique phrase in a rule file; subagent asked to report it before touching
any tool) came back absent, for both an unconditioned rule and a `paths:`-scoped
one. Only `CLAUDE.md` was injected. See [[subagents]] for the full result and its
scope limit.

**So an agent's rules go in one of four places, never in `rules/`:**

| Rule applies to | Put it in | Tier |
|---|---|---|
| every agent in the repo | `CLAUDE.md` | 0 |
| this agent, always | the agent body — that is what a system prompt is for | 0 |
| this agent, during one procedure | the preloaded skill | 1 |
| one step of one procedure | a reference file that step opens | 3 |

`.claude/rules/` may still serve the **main session** — untested — but it is not a
delivery mechanism for agent rules. Also verified: the CLAUDE.md hierarchy *does*
reach a normal subagent, but the built-in **Explore and Plan skip it**, so project
rules do not hold there.

## Templates and examples — a measured trap

- **Template = shape. Safe and useful.** Field names, what belongs in each,
  nothing filled in. Makes output comparable.
- **A filled-in good example is a near-domain stimulus and will be copied.**
  Jansson & Smith measured subjects reproducing an example's features *even when
  the brief forbade them* — straws 1% → 17% when the brief said no straws;
  suction cups 6% → 54%. See [[design-fixation-and-anchoring]].
- **Negative examples are the safer form.** *"Here is an ADR that aged badly."*
  Surprising and negative framings measured the highest novelty and rarity.
- **If you must give a positive exemplar: one, uncommon, far-domain.** A 43-study
  meta-analysis found a single uncommon example helped most.

Format conformity is the goal for a template; content conformity is the disease.

## Composition — how agents chain

The governing mechanic: **a subagent inherits none of your context.** Not the
conversation, not auto-memory, not previously invoked skills, not prior tool
results. That sounds like a limitation. **It is the mechanism** — the handoff is
forced to be a document, which is exactly what makes independent review work (this
factory's own testers found **81 defects** because the author never wrote its own
evals). It also gives you for free what the ideation evidence demands: a generator
and an evaluator with **opposite context diets**, unable to leak into each other.

| Pattern | Verdict |
|---|---|
| **Fan-out** — parallel, independent, different quarry each | **MEASURED GOOD.** The diversity gap is *between* instances, not within one |
| **Producer → independent verifier** with a different diet and an **external** signal | **MEASURED GOOD.** 81 defects here; novelty judging 6.14 → 2.38 with retrieval |
| **Pipeline** — A's artefact is B's input | **Fine when B genuinely needs it.** The handoff is a document |
| **Round-table / debate** | **MEASURED BAD.** 12 interventions, 45 conditions, **0 of 62** comparisons significant |
| **Self-critique loop, no external signal** | **MEASURED BAD.** Every model, every benchmark, worse |

**Fan-out's "different quarry each" is not a scheduling detail — it is the finding.**
[[requirements-discovery]] measures the same shape on human reviewers: readers each following
a *different* procedure against a different fault class beat ad hoc by ~35%, while an
undifferentiated checklist measured no better than ad hoc at all. A fan-out whose workers
share one prompt is the checklist condition, and the table above should be read as saying so.

**Where the other three tiers are specified.** Tier 0 is not the only thing paid every
invocation — [[claude-md-and-memory]] holds the two memory systems that are also loaded before
the first token, and the reason the composition rule above can say a subagent inherits *no*
auto-memory. Tier 5 is [[hooks]]: a wall is a `PreToolUse` handler, which runs before every
permission check and can only tighten — the one mechanism that makes a boundary impossible
rather than stated. And when these patterns stop being a diagram and become code,
[[dynamic-workflows]] is the layer that runs them, where the concurrency ceiling below is a
number someone passes rather than a fact to design around.

### Physical ceilings to build inside

- **Depth 3**; fork cannot nest at all. **Design for two levels** — coordinator →
  workers. Level three is an emergency exit.
- **Concurrency 20** (16 inside a workflow).
- **Background subagents get a reduced built-in tool set**, silently.
- **`tools:` omitted inherits ALL, not none.** The most dangerous default here.
- **Workflow agents always run in `acceptEdits` with file edits auto-approved**,
  regardless of session permission mode → walls must be hooks, not permissions.
- **Many small agents preserve more progress than one long one** — on replay the
  cache stops at the first unfinished agent and everything after it reruns.
- **Fork** inherits the whole conversation, isolates tool calls, and **reuses the
  parent prompt cache** (cheaper). Use it when a fresh agent would need too much
  background; use a normal subagent whenever the isolation *is* the point.

## Two agents or two skills?

In this order:

1. **Opposite context diets → always two agents.** Generator starved, evaluator
   saturated. Unsolvable inside one context window.
2. **Independent quarry → two agents.** The gap is between instances.
3. **More than three functions → two agents.** The cap is not just a budget, it
   is the splitting signal.

Sequentially dependent with the *same* diet → one agent, several skills.

## Standing constraints from the evidence

- **≤3 preloaded skills.** A quality finding, not a capacity one: 1–3 modules ≈
  +19.0pp, 4+ ≈ +10.1pp, measured with the window far from full. Compaction then
  re-attaches at 5,000 tokens each against a 25,000 shared budget, so ~5 survive
  — silently.
- **No persona for correctness work.** 162 personas × 2,410 questions showed a
  "largely random" effect; a second study measured MMLU 71.6% → 66.3%.
  **But for diversity work, ordinary personas measure 2.6× more between-agent
  variation** — and *ordinary* beats *visionary* ("a support engineer who handles
  the top-20 tickets", not "Steve Jobs"). Different dependent variable, different
  answer. See [[llm-idea-generation]].
- **Separation works; costume does not.** Removing agent roles from a SWE-bench
  pipeline *lowered* the resolve rate. The mechanism is isolated context plus a
  restricted tool surface.
- **Every step must end in an artefact** — a number, a module name, a `file:line`,
  a table row. A consideration merely raised recovers a fraction of its gap.
- **A "must never" in prose is a request.** Warnings against a bias failed in
  three studies and backfired in a fourth; eight anchoring-warning variants all
  failed. Put it in a PreToolUse hook, which runs before every permission check
  including `bypassPermissions` and can only tighten. If the agent also has Bash,
  the wall is decorative.
- **The model may not rank its own output.** 22–40% agreement with experts where
  expert-expert is 60%; forced pairwise comparison inflates win rates 27.2% → 49.1%.
- **Evals ship with the skill, written by someone else, with a negative control.**
  ~15% of tasks *regress* under a skill, concentrated where the base model was
  already competent.
