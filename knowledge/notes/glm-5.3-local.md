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
  - note: "Release dates came from search-result snippets; the HF weights date is now MEASURED from the HF API (2026-09-08) and was one to three days off. z.ai's blog post did not render on fetch and the GitHub README carries no dates. Coding Plan tier prices were not retrievable (z.ai/subscribe renders client-side)."
tags: [models, open-weights, local-inference, glm, claude-code, pricing, claims-graded]
related: ["[[model-agnostic-agent-harnesses]]", "[[local-finetuning-layer-streaming]]", "[[claude-code-ecosystem-plugins]]", "[[loop-engineering-and-fable-prompting]]", "[[best-local-llm-2026-09]]", "[[model-routing-free-and-local]]", "[[adversarial-plan-review-claudex]]"]
raw:
  - knowledge/raw/untried-surfaces-2026-09-08/huggingface.co_api_models_author-zai-org.json
  - "the rest predates the raw layer (fetched 2026-09-02); url + fetched are its only provenance"
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
| release | API 2026-08-14 (REPEATED). Weights on HF **2026-08-25 — MEASURED 2026-09-08** from the HF API: all four repos (GLM-5.3, -BF16, -Flash, -Flash-BF16) carry `createdAt` 2026-08-25, so the "~2026-08-26/28" every secondary repeats is one to three days late. The limit worth stating: `createdAt` is when the repository was created, which can precede public visibility if it was private first — it bounds the release from below, it does not prove the announcement date. The two-week "safety evaluation and hardening" hold is still REPEATED, not read on a Z.ai page | same window, REPEATED |
| API price / MTok | $1.40 in · $0.26 cached · $4.40 out | **$0.15 in · $0.03 cached · $0.50 out** — the list price, in force since **2026-09-09** | 

> **The launch discount expired, and this row had the right shape to survive it.** Until 2026-09-09 Flash was $0.075/$0.015/$0.25 under a 50% launch discount; this table recorded the discount *and* the list price beside it, so the correction was a deletion rather than a re-derivation. [[model-routing-free-and-local]] cited only the discounted pair and was therefore 2× wrong the moment the promotion lapsed — the same fact, two notes, and the one that wrote down *why* the number was low is the one that did not rot. Verified 2026-09-11 against the page itself, which had said *"The promotion ends at 24:00 on September 9, 2026 (UTC+8, Singapore time)"* and now shows the single list column. GLM-5.3 and GLM-5.2 are unchanged at $1.4 / $0.26 / $4.4.

HF card benchmarks for the flagship, with the listed competitors: Terminal-Bench 2.1
**88.2** (Kimi K3 88.3, GPT-5.6 Sol 88.8); Terminal-Bench 3.0 **28.3** (Fable 5 33.7,
GPT-5.6 Sol 34.6); DeepSWE v1.1 **66.9** (Fable 5 69.7); SWE-Marathon v1.1 **42.5**
(Kimi K3 48.1); Agents' Last Exam CLI **28.5**. All vendor-reported; Z.ai's own "50% over
GLM-5.2 on Z.ai Code Bench" is on Z.ai's own bench. Flash: Terminal-Bench 2.1 84.3,
"approaching Claude Opus 4.8 on coding and agentic benchmarks at one-tenth the price".

**The two Unsloth pages are KNOWN-NOISY watch rows (2026-09-08).** They are GitBook-hosted, and
their deploy id, asset hashes and even bundler chunk numbers churn on every republish — so the
watcher reports CHANGED with **zero words changed**. Measured that day: a narrow normaliser for
the deploy id (681 occurrences per page) did not close the gap and was deleted rather than
widened. The rows are kept because the table below is a claim we cite; they are annotated in
`WATCH.tsv`, and a CHANGED on either one means *read the diff*, not *the numbers moved*.

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
  fraction of the friction. The concrete job waiting for that arm is the cross-provider
  review in [[adversarial-plan-review-claudex]], whose whole design turns on the reviewer
  not sharing the author's model — this endpoint is the cheapest way to give it one.
- **"Local" is not on the table for us**, and it is not what the Coding Plan users in the
  videos mean either — they mean *Z.ai-hosted behind Claude Code*.
- The custom licence's $10B clause is irrelevant to us; Flash being MIT matters only if
  weights are ever fine-tuned ([[local-finetuning-layer-streaming]] — an 8B fits a laptop;
  a 320B does not).

Arm B in the routing matrix, and the terms-read that still blocks it on private work: [[model-routing-free-and-local]] (added 2026-09-02).

## The 744B-vs-753B disagreement, settled 2026-09-04

[[llm-wiki-pattern]] named this as the contradiction a value-comparing check would have caught
"the day it was written". It was never resolved, so it was resolved here — from the weights'
own configuration rather than from either page's prose.

**What the sources say today.** The GitHub README (`zai-org/GLM-5`, fetched 2026-09-04) still
reads **`744B-A40B`** — MEASURED. The Hugging Face card
(`knowledge/raw/baseline-2026-09-04/huggingface.co_zai-org_GLM-5.3_raw_main_README.md.md`)
**states no parameter count at all** — so the note's claim that "the HF card says 753B" cannot be
checked against the card as it now stands. Whether the card dropped the figure or the figure was
misattributed cannot be settled: the bytes that would decide it were never kept, because this note
predates the raw layer. That is this base's own failure mode, demonstrated on itself.

**What the architecture says.** From `config.json` (fetched 2026-09-04), which is primary data
rather than prose: 78 layers, `first_k_dense_replace: 3`, hidden 6144, 256 routed + 1 shared
experts, `moe_intermediate_size` 2048, dense `intermediate_size` 12288, 64 heads and 64 KV heads
at head_dim 192, vocab 154,880, embeddings untied.

| Component | Arithmetic | Params |
|---|---|---|
| One MoE layer's experts | 257 × 3 × 6144 × 2048 | 9.70 B |
| 75 MoE layers | 75 × 9.70 B | 727.3 B |
| Attention, all 78 layers | 78 × (Q + K + V + O) = 78 × 302 M | 23.6 B |
| 3 dense FFN layers | 3 × 3 × 6144 × 12288 | 0.68 B |
| Embeddings (untied, ×2) | 2 × 154,880 × 6144 | 1.9 B |
| **Total** | | **≈ 754 B** |

**Verdict: DERIVED, and it favours the larger figure.** An independent count from the shipped
configuration lands at ~754 B, one billion from the 753 B the note attributes to the card and ten
billion above the vendor's `744B` label. The most economical reading is that **744B-A40B is a
rounded product label and ~753 B is the weight count** — the two are not a contradiction about
the same quantity, which is why neither source was ever going to correct the other.

**One figure this does NOT settle.** A rough active-parameter count by the same method
(attention + 1 shared + 8 routed experts per layer) lands near **50 B**, not the label's
**A40B**. The gap is real and unexplained here; candidates are that the label counts FFN experts
only, or a different top-k accounting. Recorded as open rather than resolved, because a
derivation that reproduces one number and not its sibling has not earned the second.
