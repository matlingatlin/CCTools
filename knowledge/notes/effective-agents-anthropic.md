---
title: Building effective agents — Anthropic's own patterns and cautions
sources:
  - url: https://www.anthropic.com/engineering/building-effective-agents
    note: "Anthropic engineering blog. Read in full 2026-08-29. Its empirical basis is stated as 'work with dozens of teams building LLM agents across industries' — practice, not a controlled study."
    fetched: 2026-08-29
tags: [agents, patterns, tool-design, evidence, measured-vs-repeated]
related: ["[[agent-design-template]]", "[[api-agent-loop]]", "[[agent-builder-prior-art]]", "[[subagents]]", "[[managed-agents-architecture]]", "[[loop-engineering-and-fable-prompting]]", "[[learning-resources-agents]]", "[[harness-over-model-prime-agent]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Building effective agents

The canonical Anthropic piece. Its value here is not the pattern catalogue — it is
the two places where it argues *against* building an agent, and the tool-design
section, which corroborates the hardest-won finding in [[agent-design-template]]
from an entirely different direction.

**Who needs the two arguments against.** They land on whoever is about to write the loop, and
that loop is written in three places in this base. [[api-agent-loop]] is the smallest form —
`while stop_reason == "tool_use"` is precisely "the LLM dynamically directing its own process",
so the distinction this piece draws in prose is a single line of control flow there.
[[managed-agents-architecture]] is the largest: brain, hands and session virtualised as
separate replaceable components, which is what "start simple" costs when you buy it as a
service. And [[agent-builder-prior-art]] is where this piece did its work as a *standard* —
three third-party builders were read against it, and what none of them had is the section
below on tool design.

Its taught counterpart is [[learning-resources-agents]]: Stanford CS329A covers the same
ground as a syllabus (robust verification, learning from feedback with tools, multi-step
planning) with the evidence a blog post does not carry. Where the two disagree, this piece is
the practitioner's account and the course is the literature's.

## The distinction it draws

> **"Workflows** are systems where LLMs and tools are orchestrated through
> predefined code paths. **Agents**, on the other hand, are systems where LLMs
> dynamically direct their own processes and tool usage, maintaining control over
> how they accomplish tasks."

## Six patterns

| Pattern | Use when |
|---|---|
| **Prompt chaining** — sequential steps, optional programmatic *gates* between them | the task decomposes cleanly into fixed subtasks; *"trade off latency for higher accuracy"* |
| **Routing** — classify, then send to a specialised handler | *"distinct categories that are better handled separately, and where classification can be handled accurately"* |
| **Parallelization** — *sectioning* (independent subtasks) or *voting* (same task, several times) | *"subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence"* |
| **Orchestrator-workers** — a central model decomposes and delegates dynamically | *"complex tasks where you can't predict the subtasks needed"* |
| **Evaluator-optimizer** — one generates, another critiques, in a loop | *"clear evaluation criteria"* **and** the two fit-signals below |
| **Autonomous agents** — tool use against environmental feedback | *"open-ended problems where it's difficult or impossible to predict the required number of steps"* |

**The evaluator-optimizer fit test is the useful part**, and it is sharper than
"add a critic": use it when *"LLM responses can be demonstrably improved when a
human articulates their feedback; and… the LLM can provide such feedback."* Both
conditions, not either. That is the same boundary [[llm-idea-generation]] draws
between refinement with an external signal (works) and intrinsic self-critique
(measured worse, every model, every benchmark).

## The two arguments against building one

> *"Start simple: find the simplest solution possible, and only increase
> complexity when needed. **This might mean not building agentic systems at all.**"*

> *"you should consider adding complexity only when it **demonstrably improves
> outcomes**."*

And on autonomy specifically: *"Agents' autonomy means higher costs, and the
potential for compounding errors. We recommend **extensive testing in sandboxed
environments, along with appropriate guardrails**."* Plus stopping conditions —
*"such as a maximum number of iterations"* — to keep control.

A caution about frameworks worth carrying: *"Incorrect assumptions about what's
under the hood are a common source of customer error."*

## Tool design — the strongest section, and it corroborates the wall

It coins **ACI, the agent-computer interface**, and the framing is the argument:

> *"think about how much effort goes into human-computer interfaces (HCI), and
> plan to invest just as much effort in creating good agent-computer interfaces."*

Then, from their own SWE-bench work: **"we actually spent more time optimizing our
tools than the overall prompt."** That is a direct statement, from the people who
built it, that the **tool surface is the larger lever than the wording** — which
is what [[agent-design-template]] concluded from the failure side.

**Poka-yoke — the concrete technique.** *"Change the arguments so that it is
harder to make mistakes."* Their worked example: requiring **absolute** filepaths
instead of relative ones **eliminated** a class of model error in SWE-bench.

That is the hook rule arriving from the opposite direction. We reached "a
must-never is a mechanism, not a sentence" by measuring that warnings fail.
Anthropic reaches "change the argument so the mistake is unavailable" by building.
Same conclusion, independent routes: **design the interface so the error cannot
be expressed, rather than instructing against it.**

Other tool-definition guidance, quotable:
- *"Put yourself in the model's shoes. Is it obvious how to use this tool… or
  would you need to think carefully about it?"*
- *"A good tool definition often includes example usage, edge cases, input format
  requirements, and clear boundaries from other tools."*
- *"Think of this as writing a great docstring for a junior developer on your team."*
- *"Give the model enough tokens to 'think' before it writes itself into a corner."*
- Keep formats close to what occurs naturally in internet text; avoid formatting
  overhead such as maintaining an accurate line count.
- Test by running many example inputs and iterating on the mistakes observed.

## Its three closing principles

Simplicity in design; **transparency** — *"explicitly showing the agent's planning
steps"*; and a carefully crafted ACI through tool documentation and testing.

## What its evidence actually is

Stated basis: *"work with dozens of teams building LLM agents across industries."*
Practice at scale, not a controlled comparison. Two specific claims:

- *"The most successful implementations weren't using complex frameworks or
  specialized libraries. Instead, they were building with simple, composable
  patterns."* — **REPEATED** in this note's sense: an observation across teams,
  with no counterfactual.
- Customer-support viability is argued from *"usage-based pricing models that
  charge only for successful resolutions"* — a market signal, not a measurement.

SWE-bench is cited as an existence proof (agents resolving real GitHub issues from
the PR description alone) **with no success rate given in the piece**.

Treat the patterns as a well-earned vocabulary and the tool-design section as
directly actionable. Treat "simple patterns beat frameworks" as the considered
opinion of people with unusual visibility — not as a measured result.
