---
title: GLM-5.3 and GLM-5.3-Flash — what "run it locally" actually costs, and the Claude Code path
sources:
  - url: https://huggingface.co/zai-org/GLM-5.3
    fetched: 2026-09-02
  - url: https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE
    fetched: 2026-09-02
  - url: https://huggingface.co/zai-org/GLM-5.3-Flash
    fetched: 2026-09-02
  - url: https://github.com/zai-org/GLM-5
    fetched: 2026-09-02
  - url: https://unsloth.ai/docs/models/glm-5.3
    fetched: 2026-09-02
  - url: https://unsloth.ai/docs/models/glm-5.3-flash
    fetched: 2026-09-02
  - url: https://docs.z.ai/guides/overview/pricing
    fetched: 2026-09-02
  - url: https://docs.z.ai/devpack/tool/claude
    fetched: 2026-09-02
  - note: "Release dates come from search-result snippets (REPEATED): z.ai's blog post did not render on fetch and the GitHub README carries no dates. Coding Plan tier prices were not retrievable (z.ai/subscribe renders client-side)."
status: verified
tags: [models, open-weights, local-inference, glm, claude-code, pricing, claims-graded]
related: ["[[model-agnostic-agent-harnesses]]", "[[local-finetuning-layer-streaming]]", "[[claude-code-ecosystem-plugins]]", "[[loop-engineering-and-fable-prompting]]", "[[best-local-llm-2026-09]]", "[[model-routing-free-and-local]]"]
---

# GLM-5.3 locally

Looked up on request, 2026-09-02. Two models share the name and most write-ups blur them;
the search snippets did too ("320B/18B, MIT" is the **Flash**, not the flagship).

## The two models (MEASURED)

| | GLM-5.3 | GLM-5.3-Flash |
|---|---|---|
| size | **744B total / 40B active** (GitHub README "744B-A40B"; the HF card says 753B — the two Z.ai sources disagree by 9B) | **320B / 18B active** |
| architecture | GLM MoE with "DSA" (dynamic sparse attention) | same family; "first natively multimodal model in the GLM-5 series" |
| context | 1M, 128K max output (docs.z.ai) | evaluation notes cite 300K |
| licence | **custom "GLM-5.3 License"** — MIT-shaped permissions plus one clause: a "Model as a Service" business with >$10B revenue over any 12 months must pass Z.AI's security review first; end-user products and API relays are excluded from that definition | **MIT** |
| release | API 2026-08-14, weights on HF ~2026-08-26/28 after a stated two-week "safety evaluation and hardening" hold — REPEATED, not read on a Z.ai page | same window, REPEATED |
| API price / MTok | $1.40 in · $0.26 cached · $4.40 out | $0.075 in · $0.015 cached · $0.25 out (50% launch discount; list $0.15/$0.03/$0.50) |

HF card benchmarks for the flagship, with the listed competitors: Terminal-Bench 2.1
**88.2** (Kimi K3 88.3, GPT-5.6 Sol 88.8); Terminal-Bench 3.0 **28.3** (Fable 5 33.7,
GPT-5.6 Sol 34.6); DeepSWE v1.1 **66.9** (Fable 5 69.7); SWE-Marathon v1.1 **42.5**
(Kimi K3 48.1); Agents' Last Exam CLI **28.5**. All vendor-reported; Z.ai's own "50% over
GLM-5.2 on Z.ai Code Bench" is on Z.ai's own bench. Flash: Terminal-Bench 2.1 84.3,
"approaching Claude Opus 4.8 on coding and agentic benchmarks at one-tenth the price".

## What "local" means in memory (MEASURED, Unsloth)

| | RAM + VRAM needed | disk |
|---|---|---|
| GLM-5.3 1-bit | 223 GB | |
| GLM-5.3 2-bit (UD-IQ2_M) | 245 GB — "works on 256 GB RAM devices" | 239 GB |
| GLM-5.3 3-bit | 290–360 GB | |
| GLM-5.3 4-bit | 372–475 GB | |
| GLM-5.3 8-bit | 810 GB | |
| Flash 1-bit (UD-IQ1_S) | ~100 GB | 93 GB |
| Flash 3-bit (UD-IQ3_XXS) | 128 GB | 120 GB |
| Flash 4-bit (UD-Q4_K_XL) | 192–256 GB | 200 GB |

Unsloth's quantisation table for the flagship shows top-1 accuracy from 96.6% down to
72.6% across the variants — the 1- and 2-bit files that fit a 256 GB box are the bottom
of that range, and no tokens/second is published for any consumer hardware. **llama.cpp
support is fork-only** as of the Flash page ("our specific PR"; the `glm5_next`
architecture is not in mainline); the flagship page points at mainline without saying a
version. Server paths: SGLang, vLLM, TokenSpeed, KTransformers, Transformers; no minimum
GPU count stated on either card.

**So:** the flagship is not a laptop model in any sense — a 256 GB Mac Studio at 2-bit is the
floor, at quality Unsloth's own table puts well below the BF16 numbers the benchmarks were
run at. Flash at 3-bit is the first configuration that fits a 128 GB machine. This
session's box (4 cores, 15 GB) cannot run either at any quantisation.

## The Claude Code path (MEASURED, docs.z.ai)

Z.ai serves an **Anthropic-compatible endpoint**, so no gateway is needed:

```
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ANTHROPIC_AUTH_TOKEN=<Z.ai key>
API_TIMEOUT_MS=3000000
```

Coding Plan mapping: opus → `glm-5.3`, sonnet → `glm-5.3`, haiku → `glm-5.3-flash`.
Installers: `npx @z_ai/coding-helper` or `curl -O https://cdn.bigmodel.cn/install/claude_code_zai_env.sh && bash …` — both are the fourth gate's "external installer"; set the
three variables by hand instead. The older scenario page still maps to GLM-4.7 / 4.5-Air;
the devpack page is the current one. Coding Plan tier prices: not retrieved (page is
client-rendered); the plan page names GLM-5.3, 5.3-Flash, 5.2 and 5-Turbo as included.
Anthropic's own position on pointing Claude Code at a non-Claude model is unchanged:
unsupported ([[model-agnostic-agent-harnesses]]).

## For this repo

- **Cheapest possible non-Claude arm.** Through `dispatch.py` the with-arm is `claude -p`;
  with the three env vars set for that run only, the same prompt, fixture and isolation
  hit GLM-5.3 at $1.40/$4.40 (or Flash at 7.5 cents in) — no gateway, no OpenRouter
  logging clause. It needs: a `TIERS` entry marked *non-comparable on cost*, `usage`
  fields checked against what Z.ai's endpoint actually returns, and Z.ai's data-use terms
  read first (not done here). This is the experiment the Nemotron note wanted, at a
  fraction of the friction.
- **"Local" is not on the table for us**, and it is not what the Coding Plan users in the
  videos mean either — they mean *Z.ai-hosted behind Claude Code*.
- The custom licence's $10B clause is irrelevant to us; Flash being MIT matters only if
  weights are ever fine-tuned ([[local-finetuning-layer-streaming]] — an 8B fits a laptop;
  a 320B does not).

Arm B in the routing matrix, and the terms-read that still blocks it on private work: [[model-routing-free-and-local]] (added 2026-09-02).
