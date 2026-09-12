---
name: cost-aware-model-routing
description: "Use when planning a multi-agent run, dispatching many subagents, picking a model tier for a task, honoring a spend budget, or when a run could get expensive. Routes each task to the cheapest model tier that can do it well, then caps spend with budget ceilings, stop-conditions, bounded fan-out, and prompt-cache reuse. Triggers on choosing a model, fanning out subagents, an expensive or long-running job, a hard cost/budget limit, or a task that mixes cheap mechanical work with a few high-stakes steps. NOT for deciding WHAT to drop when the budget will not cover the plan (use budget-cut-triage)."
---

# Cost-Aware Model Routing

## What & why
Model spend is dominated by two levers: the **tier** you pick and the **width** you
fan out to. Sending every task to the top tier, or fanning out N subagents at top tier
"to be safe," burns dollars with no quality gain on easy work. This talent picks the
cheapest tier that clears the bar, then guards the run with budgets and caching so a
routine job can't quietly become an expensive one. Complements the context-budget
talent (which governs TOKENS/context window); this one governs DOLLAR COST and tier.
Supports `COSTS.md`.

## When to use
- Planning a multi-agent run or deciding how many subagents to dispatch.
- Choosing a model for a task, or a run with a hard budget or that could be costly.
- Any batch/loop where per-item cost multiplies.

## Steps
1. **Classify task difficulty.** Mechanical/deterministic or simple lookup → cheap/small
   tier. Synthesis, ambiguous, or high-stakes (irreversible, user-facing, security) →
   top tier. Adversarial verification (checking another model's work, security review)
   → top tier even if generation was cheap. Default down, not up; escalate on evidence.
2. **Apply guardrails.** Set a **budget ceiling** for the run and a **stop-condition**
   (max steps/iterations, or "stop and ask" at X% of budget). **Cap fan-out width** to
   the smallest N that covers the work — width multiplies cost linearly. Tune
   **reasoning effort** to the task: low for easy, high only where it changes the answer.
3. **Exploit caching & reuse.** Put stable content (system prompt, shared context,
   large read-only docs) in a **stable prefix** so prompt caching amortizes it across
   calls. **Batch** similar items into one call instead of many. Reuse cached prefixes
   across subagents rather than re-sending context per agent.
4. **Measure, log, escalate on evidence.** Record spend per task class. Start cheap;
   escalate a specific item to a higher tier only when output quality demonstrably fails
   (failed verify, low confidence, retry). Log escalations so routing improves over time.

## Routing table
| Task class | Tier | Why |
|---|---|---|
| Format/transform, extract, rename, boilerplate | cheap/small | Deterministic; top tier adds cost, not quality |
| Lookup, classify, summarize short text | cheap/small | Low ambiguity; small models suffice |
| Fan-out over many similar items | cheap/small + batch | Width × price dominates; keep per-item cheap |
| Synthesis, planning, ambiguous requirements | top | Judgment and coherence pay off |
| High-stakes / irreversible / security-sensitive | top | Error cost >> model cost |
| Adversarial verify / review of other output | top | Independent check must be at least as strong |

## Levers cheat-sheet
- **Tier**: biggest per-call lever — default cheap, escalate on evidence.
- **Fan-out width**: multiplies total cost — cap N; prefer batching over more agents.
- **Reasoning effort**: raise only where it changes the answer.
- **Prompt cache**: stable prefix + batching amortizes shared context.

## Anti-patterns
- Top tier "to be safe" on mechanical work. Wide fan-out at top tier by default.
- Re-sending the same large context per subagent instead of a cached prefix.
- Escalating on a hunch instead of a failed check. No budget ceiling or stop-condition.
