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
tags: [harness, self-improvement, agents, swarm, benchmarks, claims-graded]
related: ["[[loop-engineering-and-fable-prompting]]", "[[effective-agents-anthropic]]", "[[subagents]]", "[[claude-code-ecosystem-plugins]]", "[[model-agnostic-agent-harnesses]]", "[[third-party-landscape]]", "[[agent-builder-prior-art]]", "[[adversarial-plan-review-claudex]]", "[[graphify-assessment]]"]
raw:
  - knowledge/raw/untried-surfaces-2026-09-08/arcprize.org_results_anthropic-claude-opus-5.html
  - knowledge/raw/watch-2026-09-11b/raw.githubusercontent.com_PrimeIntellect-ai_prime-agent_HEAD_README.md.md
  - "the rest predates the raw layer (fetched 2026-09-02); url + fetched are its only provenance"
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
  published 2026-07-24 — **MEASURED 2026-09-08 from arcprize.org itself**, which rendered on
  this attempt after refusing two fetchers on 2026-09-02. The page's verified table gives
  **30.16%** at High, which the outlets round to 30.2, and it adds three things none of them
  carried: **"Due to the short testing window, ARC-AGI-3 was evaluated only at High reasoning
  effort"** — so the ARC-AGI-3 row is blank at Max, and High was not a choice but the only run;
  Opus 5 "completed **five additional Public Demo environments** that no model had previously
  beaten"; and the neighbouring benchmarks at Max are **97.5% ARC-AGI-1 and 90.4% ARC-AGI-2
  Semi-Private**, which ARC itself calls "competitive with previous frontier leaders, though at
  slightly higher cost" — a notably flatter framing than "a new high score". The post links its median run's action
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

## The installer's own security claim was RETRACTED by its author — 2026-09-12

The watcher caught a 34-word change to the README, and it is the most interesting kind: a vendor
narrowing a security property it had previously implied.

**Was:** *"The installer downloads a versioned release, **verifies its SHA-256 checksum**, installs
the `prime-agent` command…"*

**Now:** *"The installer **requires HTTPS** for release downloads, checks the selected archive
against the release origin's SHA-256 inventory… **The checksum detects corruption or an
inconsistent transfer; because the inventory and archive come from the same origin, HTTPS is the
authenticity boundary.**"* The install line gained `--proto '=https' --proto-redir '=https'`, which
refuses a redirect to plaintext — the hole a bare `curl -fsSL … | sh` leaves open.

**This base had already written that argument, for a different project, and unprompted.**
[[graphify-assessment]] records graphify's installer as verifying SHA-256 *"(integrity against a
broken download, **not** authenticity — checksum and binary come from the same channel)"*. Same
reasoning, reached from the code rather than from a vendor's disclosure, weeks earlier. A vendor has
now published the identical distinction about its own installer, which is the strongest available
confirmation that the analysis generalises rather than being a quirk of one project.

**The transferable rule, and it belongs to the fourth gate.** A checksum served from the same origin
as the artefact it describes is an **integrity** control and not an **authenticity** one: whoever
can replace the archive can replace the inventory. Authenticity needs a second, independent channel
— a signature over a key you hold, or a transport whose identity you verify — and where the only
independent thing is TLS, *TLS is the whole boundary*, which is why forbidding a plaintext redirect
is not a cosmetic hardening. Two of the two `curl | sh` installers this base has examined make this
mistake in their wording; the second one corrected itself. **When reading an installer, do not ask
whether it verifies a checksum. Ask where the checksum came from.**
