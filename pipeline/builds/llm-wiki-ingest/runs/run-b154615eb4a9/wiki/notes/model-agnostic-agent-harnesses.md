---
title: Model-agnostic agent harnesses — Goose, and running Claude Code against other models
sources:
  - url: https://github.com/block/goose
    fetched: 2026-09-02
  - url: https://goose-docs.ai/docs/getting-started/providers/
    fetched: 2026-09-02
  - url: https://claude.com/customers/block
    note: "Anthropic's own Block case study; the source of the '90%' number."
    fetched: 2026-09-02
  - url: https://venturebeat.com/orchestration/jack-dorseys-block-cuts-40-of-staff-4-000-people-and-yes-its-because-of-ai
    note: "Search result only, with Fortune and SFGate corroborating the same figures."
    fetched: 2026-09-02
  - url: https://code.claude.com/docs/en/llm-gateway
    fetched: 2026-09-02
  - note: "45-second video 'The guy who built Twitter just gave everyone a million-dollar AI agent' (creator series 'Building You 100x', day 104), transcribed locally 2026-09-02. Its claims are graded, not trusted."
status: verified
tags: [agents, harness, model-routing, goose, claude-code, claims-graded]
related: ["[[subagents]]", "[[agent-builder-prior-art]]", "[[learning-resources-agents]]", "[[loop-engineering-and-fable-prompting]]", "[[mcp]]", "[[claude-code-ecosystem-plugins]]", "[[local-finetuning-layer-streaming]]", "[[harness-over-model-prime-agent]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[best-local-llm-2026-09]]", "[[model-routing-free-and-local]]", "[[token-economy-playbook]]"]
---

# Model-agnostic agent harnesses

The question underneath the video is a real one: *which harness lets me pick the model per
task, and can I keep Claude Code's workflow while doing it?* Two answers, verified.

## Goose (Block) — the harness that is model-agnostic by design

MEASURED from the README and provider docs unless marked.

- **What:** "an open source, extensible AI agent" — CLI and desktop app; reads files,
  edits, runs commands, orchestrates multi-step work; extensions via MCP (70+, REPEATED).
- **Licence and home:** Apache-2.0. "goose is part of the Agentic AI Foundation (AAIF) at
  the Linux Foundation" (contributed December 2025, REPEATED). 53.8k stars on 2026-09-02.
- **Model choice:** README says "15+ providers"; the provider docs list 60+ — Anthropic,
  OpenAI, Gemini, Azure, Groq, Mistral, DeepSeek, Bedrock, Vertex, OpenRouter, and local
  runners Ollama and LM Studio. Configured by `goose configure`, by env var
  (`ANTHROPIC_API_KEY`, ...), or **per session**: `goose run --model <model> -t "<prompt>"`.
- **Login:** most providers need an API key. Local models need none. And the reverse of
  what the video implies: via **ACP (Agent Client Protocol)** Goose can drive *Claude Code*
  or *Codex* as the model, on an existing Claude Code or ChatGPT subscription — "Claude
  ACP, Codex ACP — both require active subscriptions".

**Video claims graded**

| claim | verdict |
|---|---|
| "built by Jack Dorsey at Block" | Block's project; created by Bradley Axen (Principal Data and ML Engineer). Dorsey is CEO. MISATTRIBUTED |
| "he used it to fire 4,000 employees" | Block cut ~4,000 roles (~40%) on 2026-02-26 and Dorsey tied the cuts to AI tools (REPEATED, three outlets). Causation to Goose specifically is the creator's, not Dorsey's |
| "it now writes 90% of Block's code" | WRONG denominator. Anthropic's case study: **"90% of *my* lines of code are now written by goose" — Bradley Axen.** Block-wide figure on the same page: "75% of engineers saving 8 to 10+ hours every week"; ~4,000 of 10,000 employees use it |
| "works with any model" | MEASURED, 60+ providers, per-session switch |
| "free, open source, no logins" | free and Apache-2.0: MEASURED. "No logins": only with a local model; every hosted provider needs a key or a subscription |
| "a million-dollar AI agent" | no basis given; not a claim that can be checked |
| "ships products while you sleep" | marketing |

## Claude Code against other models — what is documented, what is community

Claude Code itself selects among *Claude* models (`/model`, `ANTHROPIC_MODEL`). Pointing it
elsewhere works because everything goes through one variable:

- **`ANTHROPIC_BASE_URL`** — MEASURED from `code.claude.com/docs/en/llm-gateway`
  (2026-09-02): "the variable that points Claude Code at the gateway". "Any gateway that
  exposes a supported API format works." And the sentence that settles the question:
  **"Anthropic doesn't endorse, maintain, or audit third-party gateway products, and
  doesn't support routing Claude Code to non-Claude models through any gateway."** So
  the mechanism exists and is documented; using it for GPT/Gemini/local models is
  community territory, unsupported, and each Claude Code release can break a gateway
  that does not forward the new capabilities. Two more facts from the page: with a
  gateway credential active the claude.ai subscription is *not* used (billed per token to
  the credential's owner); with only the base URL set, the subscription login stays the
  active credential and its limits still apply.
- **Community routers** (REPEATED, search results 2026-09-02, none read in full):
  `claude-code-router` (`ccr code` instead of `claude`; intercepts the Anthropic-format
  request and rewrites it for DeepSeek, Qwen, GLM, MiniMax, Gemini, OpenRouter or a local
  model, with a routing rule per request type), a LiteLLM proxy (translates provider
  formats behind an Anthropic-shaped endpoint), `1rgs/claude-code-proxy` (OpenAI models),
  and Ollama / LM Studio, which "serve Anthropic-compatible endpoints" so Claude Code can
  point at them directly.

What this buys and costs, for us: our measurement design fixes the model tier per run
(`pipeline/build/dispatch.py`, `TIERS`), and a gateway would let the same harness dispatch a
run on a non-Claude model with the *same* prompt and isolation — a real experiment
("does this skill help GPT-x too?"). It also breaks the cost row: a gateway's `usage`
payload is whatever the gateway chooses to report, so `tokens` from a routed run is not
comparable to a native one unless the gateway is checked first.

## free-claude-code — the "Claude Code free forever" repo, named (added 2026-09-02)

Source: `https://github.com/Alishahryar1/free-claude-code` README fetched 2026-09-02; a
four-slide carousel (bestapps.ai; slide 2/4 shows the repo page) supplied in two parts, md5
8ca9ec1b… (cover) and 5a6bcbc7… (repo slide). MEASURED from the README unless marked.

- **What:** "Independent open-source project. Not affiliated with or endorsed by Anthropic."
  MIT, **52.8k stars**. "50 ToS-friendly providers. 1.3B+ free tokens every month"; "10
  coding agents" behind one model catalogue — Claude Code, Codex, Pi, OpenCode, Cline,
  Hermes, DeepSeek Harness, Grok Build, Muse Code, Aider; failover to the next configured
  model after retries; "Up to 90% fewer terminal-output tokens" via optional RTK filtering.
- **How it hooks in:** `ANTHROPIC_BASE_URL=http://localhost:8082` and
  `ANTHROPIC_AUTH_TOKEN=freecc`, plus `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` and
  `CLAUDE_CODE_AUTO_COMPACT_WINDOW`. The cover's screenshot shows Claude Code v2.1.126's
  `/model` picker listing `open_router/google/gemma-3-4b-it:free` … `gemma-4-26b…:free`
  — that is, **Gemma through OpenRouter's free tier**, presented inside Claude Code's UI.
- **Its own terms claim:** "FCC follows provider terms and removes integrations if they
  stop being allowed." The 1.3B figure is, as with OmniRoute's 1.51B, a pool of other
  providers' free tiers, each with its own rate limit, logging and trial clause.

**Claims graded.** "Use Claude Code for free forever" — WRONG as worded: what runs for free
is the *Claude Code CLI* driving non-Claude free models; no Claude model is involved, and
with a gateway credential active the claude.ai subscription is not used at all (Anthropic's
gateway page, re-read 2026-09-02). "Already has 51k stars" — 52.8k, MEASURED. "50 other AI
backends" — the README says 50 providers, MEASURED. "Forever" — each free tier is a
provider's promise, revocable; the README's own line about removing integrations concedes
it. Anthropic's position, unchanged: "doesn't support routing Claude Code to non-Claude
models through any gateway."

**For us.** Same verdict as OmniRoute and the community routers above: a *source* for a
non-comparable extra arm on a public fixture, never in `dispatch.py`'s measured path, and
the four gates before it runs anywhere. One thing it does better than the others: a
per-provider ToS stance stated up front.

## Free frontier-class weights as an extra arm — Nemotron 3 Ultra via OpenCode Zen / OpenRouter (added 2026-09-02)

Sources: `https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free` and
`https://opencode.ai/docs/zen/` fetched 2026-09-02; a 35-second video graded below.

- **The model (MEASURED, OpenRouter page):** NVIDIA Nemotron 3 Ultra, **550B total / 55B
  active** parameters, hybrid Transformer-Mamba mixture-of-experts, 1M context, 65,536 max
  output, released 2026-06-04. Free variant at $0/$0, "free endpoints are rate limited",
  data policy in full: "do not upload any confidential information or personal data...
  Your use is logged for security purposes and to improve NVIDIA products and services."
  Paid variant $0.50 / $2.20 per MTok (REPEATED, search result).
- **OpenCode Zen (MEASURED):** "a list of tested and verified models provided by the
  OpenCode team"; Nemotron 3 Ultra Free is listed among several free models "for a
  limited time"; an account **is** required ("sign in to OpenCode Zen, add your billing
  details, and copy your API key"); the Nemotron entry repeats NVIDIA's trial-only,
  logged-use terms.
- **Video claims graded:** "NVIDIA just killed Claude Code" — hype, no comparison shown;
  "55 billion parameter model" (spoken) vs "550B" (title) — both true, active vs total;
  "free to use" — true on the free endpoints, with rate limits, logging and a trial
  clause the video never mentions; "two ways, OpenCode or an OpenRouter key" — MEASURED.

**For us.** A free, logged, rate-limited endpoint is unusable for the measurement itself
(cost rows not comparable; the fixture leaves our hands) but exactly right for an *extra
arm* on a public fixture: "does the skill help a non-Claude model at all?" is a question
we have never been able to afford to ask. Through `dispatch.py` it needs a gateway (above)
and a `TIERS` entry marked non-comparable on cost.

## Ornith-1.5 — open weights "built to improve itself", and what that phrase means (added 2026-09-02)

Sources: `https://ornith.ai/ornith_1_5.html` fetched 2026-09-02 (primary for the training
method and the benchmark table); Hugging Face model card returned 401 to the fetcher, so
the licence is REPEATED (llm-releases and testingcatalog: MIT, weights on HF under
`deepreinforce-ai`; Ornith-1.0 is MIT on HF, MEASURED via search listing). An Instagram
carousel (askgpts, slide 2/3, md5 4b59e388…) supplied 2026-09-02.

- **What (MEASURED from the blog):** three models — 397B MoE, 35B MoE "activating only 3B
  parameters per token", 9B dense — released August 2026 (2026-08-19, REPEATED). Team named
  only as "Ornith Team" on the page; DeepReinforce per HF and press (REPEATED).
- **"Self-improving" is a training-time loop, not a deployed behaviour.** Three stages,
  verbatim: "the model proposes new tasks" progressing "toward harder tasks that go beyond
  what the model has already solved"; "the model then generates or refines a task-specific
  scaffold — the instructions, tools, decomposition strategy"; "the policy produces a
  solution rollout. Reward from the rollout is propagated across all three stages" (GRPO).
  Nothing on the page says the shipped weights change themselves at inference.
- **The benchmark table, versus Claude Opus 4.8** — the *previous* generation; not Opus 5,
  not Fable 5; "all results reported for Ornith-1.5 are averaged over five independent
  runs"; who ran the Opus 4.8 numbers is not stated:

  | Benchmark | Ornith-1.5-397B | Opus 4.8 |
  |---|---|---|
  | Terminal-Bench 2.1 | 86.1 | 85.0 |
  | SWE-bench Verified | 86 | 85.8 |
  | WideSearch | 80.8 | 72.9 |
  | BrowseComp | 86.6 | 84.3 |
  | DeepSWE | 56 | 59 |
  | Frontier-Bench v0.1 | 13.5 | 21.1 |
  | GPQA Diamond | 92.8 | 93.6 |
  | HLE (with tools) | 56.1 | 57.9 |

  Four wins by 0.2–8 points, four losses, one of them (Frontier-Bench) by a third. "Comparable
  to Claude Opus" is a fair one-line reading of that table *for Opus 4.8*.

**Carousel claims graded.** "Open-source AI built to improve itself" — MEASURED as a training
method, MISLEADING as a product property. "Trains itself on increasingly difficult coding
tasks" — MEASURED (task proposal stage). "Generates its own tools and task scaffolds" —
MEASURED (scaffold stage). "Available in 9B, 35B, 397B" — MEASURED. The chart is the blog's
own, reproduced faithfully.

**For us.** The same slot as Nemotron: an MIT open-weights candidate for the *non-Claude
arm* of a skill measurement, on a public fixture, cost row marked non-comparable. Two
cautions specific to it: the comparison baseline is one generation behind the models we
measure on, and "self-improving" in the headline is the same word Prime Agent uses for a
different mechanism (runtime harness edits, [[harness-over-model-prime-agent]]) — the two
should not be filed together.

## "260 free LLM APIs" — the list behind the video (added 2026-09-02)

Source: `https://github.com/mnfst/awesome-free-llm-apis` fetched 2026-09-02 (the video's
frames show this repo: "LLM APIs with permanent free tiers for text inference",
manifest.build banner, CC0-1.0); a 30-second video graded below.

- MEASURED: CC0-1.0; 7.3k stars; "All endpoints are OpenAI SDK-compatible unless noted";
  permanent free tiers only, no trial credits; 6 provider APIs + 11 inference providers
  (Cohere, Google Gemini, Cloudflare Workers AI, GLM-4.x Flash ... visible in the frames);
  `data.json` + GitHub Actions refresh; maintained by the manifest.build company, which is
  the commercial interest behind a free list.
- "260" — UNVERIFIED as a count: the README does not state a total; ~100+ model rows
  visible; 260 is plausibly the repo's own title figure counting model variants. "Use
  forever" — the list is of *permanent* tiers, but each tier is the provider's promise,
  not the list's, and the frames show rate limits of 20 requests/minute and
  1,000 calls/month on the first rows.
- The better-known sibling `cheahjs/free-llm-api-resources` (26+ providers, includes
  trial credits, mintlify docs) covers the same ground; neither is a talent, both are
  sources for a `cost-aware-model-routing` fallback tier.

## Pi and Herdr — a minimal harness and a multiplexer (added 2026-09-02)

Sources: `https://pi.dev/` and `https://herdr.dev/docs/agents/` fetched 2026-09-02; a
2m48s "23-year-old AI engineer in big tech" setup video (Pi + ChatGPT $20 subscription +
Herdr + a terminal; AXI skills — see [[mcp]]).

- **Pi** (MEASURED): "a minimal agent harness" by Earendil Inc. and contributors, MIT.
  Agent runtime, tool runtime, unified API over 15+ providers (Anthropic, OpenAI, Google,
  Azure, Bedrock, Mistral, Groq, Cerebras, xAI, Hugging Face, NVIDIA, OpenRouter, Ollama…),
  auth by API key or OAuth; four modes (interactive, print/JSON, RPC, SDK); deliberately
  ships without sub-agents and plan mode, which are extensions. The video's "ChatGPT $20
  subscription as provider" is not on the page (UNVERIFIED for Pi; OAuth is). The
  "toggle skills" extension (which skills are agent-invocable vs manual) is a
  third-party extension by another author — the same knob as our
  `disable-model-invocation`.
- **Herdr** (MEASURED): terminal multiplexer for coding agents — "each agent stays in a
  real terminal pane with its shell, logs, prompts, and running processes intact",
  20+ agents auto-detected, sidebar state idle / working / blocked. Licence and price not
  on the docs page.
- **OmniRoute**, the gateway both plugin videos lead with, is written up in
  [[claude-code-ecosystem-plugins]]: MIT, 352 providers, "~1.51B free tokens / month"
  pooled from other providers' free tiers.

## Agent TARS / UI-TARS-desktop — a computer-use agent stack (added 2026-09-02)

Source: `https://github.com/bytedance/UI-TARS-desktop` fetched 2026-09-02; a 27-second video
("a skill that kills your mouse and keyboard"). MEASURED from the README unless marked.

- **What:** ByteDance's "general multimodal AI Agent stack" — Agent TARS (CLI + Web UI +
  headless server; hybrid browser agent choosing GUI, DOM or both; protocol-driven event
  stream; kernel built on MCP) and UI-TARS-desktop (a native GUI agent "driven by UI-TARS and
  Seed-1.5-VL/1.6 series models" with screen, mouse and keyboard control). **Apache-2.0,
  38.8k stars.** Install `npx @agent-tars/cli@latest`.
- **Model:** needs a vision-language model — Volcengine (Doubao) or Anthropic are the
  documented providers, with an API key; local deployment is mentioned. The video's "you
  can even add your own LLM" is true in that sense.
- **Video claims graded:** "a skill" — it is a stack of two applications, not a SKILL.md;
  "kills your mouse and keyboard" — it *drives* them, which is the point and the risk;
  "books hotels, scrapes the web, turns data into graphics" — the README's demo videos
  (`agent-tars-book-hotel.mp4`) show the first; the rest is generic.

**For us.** A computer-use agent is the maximal blast radius: it does whatever a prompt or
a page it reads tells it to, with the user's mouse. `agent-blast-radius-guard` and
`untrusted-text-boundary` are the two talents that must run before it does; the harness
is also a candidate *subject* for `agent-fault-injection`. Not a talent; infrastructure.

## Switchyard — NVIDIA's routing proxy, and the 74% number (added 2026-09-02)

Sources: search results and NVIDIA / LangChain blog snippets (REPEATED — the README at
`github.com/NVIDIA-NeMo/Switchyard` was not fetched); a 13-slide carousel (@buildwithneej).

- **What:** a Rust proxy and library that routes LLM traffic across providers while
  translating between OpenAI Chat, OpenAI Responses and Anthropic Messages formats, records
  metrics, and ships typed routing strategies — `classifier`, `stage`, `escalation`,
  `prefill`, `random`, `passthrough`. Apache-2.0, ~2,000 stars (slide: 2,038, +932 that
  week), `cargo install --locked switchyard-server`, one `routes.toml`.
- **The 74%:** LangChain's benchmark, 145 multi-turn tasks (support, incident
  investigation, automation), escalation router between Nemotron 3.5 Lightning and Claude
  Opus 4.8, five runs: **74% cheaper than frontier-only with 7% of calls escalated**. The
  slide's "NVIDIA's own eval" is wrong in one word — the eval was LangChain's, the router
  NVIDIA's — and the number is a *cost* number; the quality delta against frontier-only is
  in the LangChain post and was not read here.
- **Why it matters for this repo:** it is a first-party answer to the gateway question in
  the section above — an Anthropic-format endpoint in front of any model, with escalation
  as a *strategy* rather than a hand-written rule. It is also `cost-aware-model-routing`
  as software. For `dispatch.py` it is the same caveat as every gateway: the `usage` a
  routed run reports is the proxy's, and Anthropic does not support non-Claude backends.

## OpenMAIC, for completeness

A third model-agnostic harness seen the same day (13 providers, `DEFAULT_MODEL` with a
provider prefix) is a *course generator*, not a coding agent; it is written up in
[[learning-resources-agents]].

## Verdict summary

Goose is the real thing the video is pointing at, and the only wrong parts of the video
are the numbers and the attribution. For "run my Claude Code workflow on another model",
the documented lever is `ANTHROPIC_BASE_URL` and a gateway — and Anthropic states in the
same document that routing to non-Claude models is unsupported. The routers are community
software and get the four gates before any of them runs here. If the goal is "one harness,
any model, per task", Goose is the tool built for that; Claude Code is not.

**The decision, not the landscape (added 2026-09-02).** Which of our jobs may run on a routed arm, what silently breaks per arm (Ollama drops caching, count_tokens, tool_choice and Batch), and why a 50-request-a-day free tier cannot carry one Scio build: [[model-routing-free-and-local]]. The token levers a routed arm forfeits are ranked in [[token-economy-playbook]].
