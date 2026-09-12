---
title: Harness over model — Prime Agent's self-refining harness, and the swarm meta-harnesses
sources:
  - url: https://github.com/PrimeIntellect-ai/prime-agent
    fetched: 2026-09-02
  - url: https://github.com/ruvnet/claude-flow
    note: "Redirects to the project's new name, Ruflo."
    fetched: 2026-09-02
  - note: "Prime Intellect's blog post on the ARC-AGI-3 result: see the paragraph below for what was and was not retrievable on 2026-09-02."
  - note: "Two short videos ('tripled what Opus 5 scores', 'Claude Flow swarm'), transcribed locally 2026-09-02; claims graded."
status: verified
tags: [harness, self-improvement, agents, swarm, benchmarks, claims-graded]
related: ["[[loop-engineering-and-fable-prompting]]", "[[effective-agents-anthropic]]", "[[subagents]]", "[[claude-code-ecosystem-plugins]]", "[[model-agnostic-agent-harnesses]]", "[[third-party-landscape]]", "[[agent-builder-prior-art]]", "[[adversarial-plan-review-claudex]]"]
---

# Harness over model

The video's thesis — "Opus didn't get smarter last week, but the thing steering it did" —
is this repository's thesis. That is a reason to grade it harder, not softer.

## Prime Agent (Prime Intellect)

MEASURED from the README, fetched 2026-09-02, unless marked.

- "A self-improving RLM agent for coding workflows and long-running autonomous tasks."
  MIT. **19.6k stars** (the video's "13,000" is stale, not wrong). Needs an API key or a
  subscription provider via `/login`, plus a Python runtime.
- **RLM — Recursive Language Model:** context is a variable and sub-agents are function
  calls inside a persistent REPL; i.e. the model *programs over its own context* rather
  than receiving it.
- **Continual harness:** supplemental prompts, memories, skill descriptions and reusable
  sub-agent specs are durable state. The blog post, verbatim: "Rollback is supported
  through prior refinement history, allowing a bad harness update to be reverted by ID."
  And its own caveat: "currently no model has been trained around Prime Agent… we still
  notice friction when running Prime Agent with models." **`/refine`** "reviews the current trajectory and
  applies small, evidence-backed updates to supplemental harness state without
  rewriting the base system prompt", with snapshots for rollback.
- **The ARC-AGI-3 number** (MEASURED from `primeintellect.ai/blog/prime-agent`, released
  2026-08-05, fetched 2026-09-02): Opus 5 + Prime Agent **95.5% "RHAE Best@1"**, three runs
  95.0 / 95.2 / 95.5, **183/183 levels complete**, 99.97% Best@3; ARC's reported
  human-expert baseline **95.4%**. Opus 5 alone: ARC Prize's verified **30.2** at High effort,
  published 2026-07-24 (REPEATED — three outlets citing `arcprize.org/results/anthropic-
  claude-opus-5`; the leaderboard page itself did not render its numbers to two fetchers on
  2026-09-02). The post links its median run's action
  replay as an **official ARC Prize scorecard**, so the run went through ARC's own
  evaluation harness and is not a number typed into a blog — but a scorecard is not a
  leaderboard entry, and no *independent* replication is cited by anyone. The video's
  "nobody's actually replicated it" is therefore half right: unreplicated, not unrecorded.
  The post's cost graph claims fewer tokens than native harnesses at higher scores; no
  per-task cost is quantified in the text.
- The README fetched the same day does not carry the number at all; the blog does.
- Video claims graded: "tripled" — arithmetic on the self-reported number; "free" —
  MIT, yes, model calls are yours; "0.1 above human expert" — as reported, unverified.

## Ruflo, formerly claude-flow

MEASURED from the README (the GitHub URL `ruvnet/claude-flow` now redirects):

- "The original agent meta-harness." MIT, **70.2k stars** (video: "around 55,000",
  frame: 54,024 — stale). Roles: coder, tester, reviewer, architect, security; a
  "Queen-led hierarchy" with Raft / Byzantine / Gossip consensus topologies; "100+
  agents".
- **Shared memory:** AgentDB with HNSW vector index; "SONA neural patterns,
  ReasoningBank, trajectory learning"; persists across sessions in its RVF format.
- Not Claude-only: "5 providers with failover" — Claude, GPT, Gemini, Cohere, Ollama.
- The one measured claim on the page is about the vector store ("~1.9× faster at N=20k
  ... recall@10 ~0.99" vs brute force, script in repo) — a claim about its index, not
  about whether a swarm ships better code.
- Video claims graded: "same subscription, a lot more throughput" — throughput of
  *what* is never measured; "what one agent learns the next run already knows" — that
  is the memory feature, MEASURED as present, unmeasured as useful.

**A second Ruflo video (2026-09-02, "60 agents, slashes your Claude API costs by 75%, basic
tasks route to a free tier, ranked #1 with 14,000 stars"):** the README fetched the same day
states no cost percentage at all, says "100+ agents", and shows 70.2k stars. Three numbers,
three misses; the free-tier routing exists as a provider-failover feature, not as a measured
saving. Skill-library evolution as a *loop* rather than a harness is HKUDS/OpenSpace — see
[[agent-builder-prior-art]].

## What this repo should take from it

1. **`/refine` is our build loop, made a runtime command.** Prime Agent edits its
   prompts, skills and memory *during* a task from evidence in the trajectory, with
   snapshots. We do it *between* builds, with a preregistered threshold and a blind
   grader. The two are not rivals: theirs optimises one run, ours decides what ships to
   every run. The piece worth copying is the rollback snapshot per refinement — our
   `pipeline/builds/<id>/` records the verdict but not a one-command revert.
2. **The harness author ran the benchmark, on the benchmark owner's harness, and nobody
   else has yet.** That is one step better than self-grading and one step short of a
   result. It is the exact position our `skill-measure` puts a build in after the
   with-arm runs and before the blind grader: recorded, not yet believed.
3. **Swarm-with-consensus is the opposite bet to Anthropic's.** Anthropic's own guidance
   ([[effective-agents-anthropic]], the Fable 5 page in
   [[loop-engineering-and-fable-prompting]]) is few agents, explicit delegation,
   fresh-context verifiers. Ruflo bets on many agents plus a consensus protocol. Neither
   side has published a controlled comparison; we have one measurement on our own work
   (W_MAX_AGENTS 2→4, wall clock only), which says nothing about quality.
