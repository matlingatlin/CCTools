---
title: The best LLM you can run locally, August–September 2026 — by hardware tier, from the model cards
sources:
  - url: https://artificialanalysis.ai/leaderboards/models
    note: "Top-15 by Intelligence Index read 2026-09-02; the page does not mark open weights, so the open/closed split below is from the model cards."
    fetched: 2026-09-02
  - url: https://huggingface.co/moonshotai/Kimi-K3
    fetched: 2026-09-02
  - url: https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE
    fetched: 2026-09-02
  - url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
    fetched: 2026-09-02
  - url: https://huggingface.co/Qwen/Qwen3.8-27B
    fetched: 2026-09-02
  - url: https://huggingface.co/unsloth/Qwen3.8-27B-GGUF
    fetched: 2026-09-02
  - url: https://huggingface.co/Qwen/Qwen3.6-27B
    fetched: 2026-09-02
  - url: https://huggingface.co/google/gemma-4-31b-it
    fetched: 2026-09-02
  - url: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
    fetched: 2026-09-02
  - note: "GLM-5.3 / 5.3-Flash figures are in [[glm-5.3-local]]. Secondary 'best local LLM' listicles were read for candidate names only; every number below is from a model card or Unsloth's memory tables."
tags: [models, open-weights, local-inference, hardware, ranking, dated]
related: ["[[glm-5.3-local]]", "[[model-agnostic-agent-harnesses]]", "[[local-finetuning-layer-streaming]]", "[[loop-engineering-and-fable-prompting]]", "[[model-routing-free-and-local]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Best local LLM, as of 2026-09-02

"Best" has no answer without a memory budget, so this is a table by tier. Every score is
**vendor-reported on its own card** unless marked; cards pick their own competitors and
their own benchmark versions (Terminal-Bench 2.0 / 2.1 / 3.0 are three different tests),
so read across rows, not down columns. This note is dated on purpose: the frontier moved
three times in August alone.

## The ceiling: what open weights score against the closed frontier

Artificial Analysis Intelligence Index, 2026-09-02 (MEASURED from the page): Claude Fable
5.1 **66**, Opus 5 **63**, GPT-5.6 Sol / Grok 4.6 **61**, then **Kimi K3 60** and **GLM-5.3
60** — the two best open-weights models sit six points under the top closed one and level
with GPT-5.6 Sol at xhigh. On LMArena text (REPEATED, search results) Kimi K3 is ~1500 Elo
and DeepSeek V4 Pro 1462, inside the frontier band. "Open weights caught the frontier" is
true to within a few points on these two boards, and false in memory: see the next table.

## By what you can fit

| tier | the pick | why, from the card | memory | licence |
|---|---|---|---|---|
| **datacentre only** (multi-GPU node) | **Kimi K3** — 2.8T total / 104B active, 1M ctx, MXFP4 weights | GPQA 93.5, Terminal-Bench 2.1 88.3, DeepSWE 67.5 vs Opus 4.8 59.0 (its own table) | 2.8T even at 4-bit is ~1.4 TB — a rack, not a workstation | custom: separate deal above $20M MaaS revenue; "Kimi K3" must be displayed above 100M MAU or $20M/month |
| | **DeepSeek V4 Pro** — 1.6T / 49B active, 1M ctx | SWE-bench Verified 80.6 (Opus 4.6 Max 80.8), LiveCodeBench 93.5 | ~0.8 TB at 4-bit | **MIT** |
| | GLM-5.3 — 744B / 40B active | Terminal-Bench 2.1 88.2, SWE-Marathon 42.5 | 2-bit needs 245 GB → 256 GB Mac Studio is the floor, at 1–2-bit quality | custom, $10B clause |
| **128–256 GB** (Mac Studio, big workstation) | **GLM-5.3-Flash** — 320B / 18B active, multimodal | "approaching Claude Opus 4.8 on coding and agentic benchmarks at one-tenth the price"; Terminal-Bench 2.1 84.3 | 3-bit on 128 GB, 4-bit on 192–256 GB (Unsloth); llama.cpp fork-only today | **MIT** |
| | DeepSeek V4 Flash — 284B / 13B active | not read; a sibling on the V4-Pro card | ~150 GB at 4-bit (DERIVED from size) | MIT |
| **24–32 GB GPU / 32–64 GB Mac** | **Qwen3.8-27B** (dense, released 2026-08-14) | SWE-bench Pro **61.7** (its table: Opus 53.4), Terminal-Bench 2.1 73.0 (Opus 4.6 Max 78.2), LiveCodeBench 90.3, GPQA 89.2, OSWorld 84.3 — native vision + video, `reasoning_effort` low/medium/xhigh, 262K ctx (1M with YaRN) | **UD-Q4_K_M 16.5 GB, Q5_K_M 19.8 GB, Q6_K 22 GB, Q8_0 29 GB** — Q4/Q5 on a 24 GB card with room for context, Q8 on 32 GB | **Apache-2.0** |
| | Gemma 4 31B (dense, 2026-07-02) — the multilingual/multimodal alternative | MMLU-Pro 85.2, LiveCodeBench 80.0, GPQA 84.3; text+image in, 256K ctx | ~18 GB at 4-bit (DERIVED from size) | **Apache-2.0** (Gemma 4 dropped the old Gemma terms) |
| **16 GB GPU / 32 GB laptop** | **Gemma 4 26B-A4B** (MoE, 3.8B active) or **Qwen3.6-35B-A3B** | NVIDIA's own controlled table (one recipe for all four): SWE-bench Verified Qwen3.6-35B-A3B **70.1**, Gemma 4 26B-A4B 57.4, gpt-oss-20b 52.4, Nemotron 3.5 Lightning 51.6; Terminal-Bench 2.1 44.4 / 37.2 / 15.2 / 24.6 | active-parameter MoEs run at small-model speed; 4-bit ~14–18 GB (REPEATED) | Apache-2.0 / Apache-2.0 |
| | Nemotron 3.5 Lightning 30B-A3B (2026-08-11) — the throughput pick, not the quality pick | loses to Qwen3.6-35B-A3B on **13 of the 14 comparable rows** of NVIDIA's own table (CORRECTED 2026-09-04: this said *every* row. It wins one — **IFBench (loose) 71.88 vs 63.71** — which is the instruction-following row, so "throughput pick, not quality pick" survives the correction and the absolute does not); 1M ctx; hybrid Mamba-2 MoE | card targets a single H100/A100 80 GB; ~25 GB at 4-bit (REPEATED) — does **not** fit 24 GB | OpenMDW-1.1 |
| **≤ 8 GB / CPU** | Gemma 4 E4B (4.5B effective) / E2B; gpt-oss-20b at 4-bit (~12 GB) | not compared here | | Apache-2.0 |

## The three sentences that matter

1. **For a coding agent on one consumer GPU, Qwen3.8-27B at Q4–Q6 is the answer this
   month** — Apache-2.0, 16.5–22 GB, a card that shows it beating Opus 4.6 on SWE-bench Pro
   (61.7 vs 53.4) and trailing it on Terminal-Bench (73.0 vs 78.2). Treat both numbers as
   Alibaba's; nobody independent has re-run them yet that this note found.
2. **For "as good as the frontier, at home", the honest floor is 128 GB** (GLM-5.3-Flash at
   3-bit, MIT) and the comfortable one is 256 GB. Below that you are choosing among 27–35B
   models, which are ~10 index points and one benchmark generation behind.
3. **The absolute best open model (Kimi K3) is not a local model** in any sense a person
   owns: 2.8T parameters. "Open weights" and "runs locally" parted company in 2026.

## Mac Studio M5 Max / M5 Ultra as the local box (added 2026-09-02)

Sources: Apple's Swedish Mac Studio page (screenshot, 2026-09-02): M5 Max 18-core CPU, up to
40-core GPU, **up to 128 GB unified memory, 614 GB/s**; M5 Ultra up to 36-core CPU, 80-core
GPU, **up to 512 GB, 1.2 TB/s**. Announced 2026-08-25, ships 2026-09-22; the 512 GB
configuration ships "late October"; M5 Ultra from 72 995 kr, a maxed one 239 395 kr
(REPEATED, Macworld.se). Measured throughput: hardware-corner.net, MLX, M5 Max 128 GB
(fetched 2026-09-02); nothing measured on an M5 Ultra was found — it is not shipping yet.

**Measured on M5 Max 128 GB (MLX, generation tok/s at 4K → 32K context):**

| model | GB | M5 Max gen | prompt (prefill) | the GPU it was compared to |
|---|---|---|---|---|
| Qwen3.5-122B-A10B 4-bit | 70 | 66 → 55 | 880–1240 t/s | RTX Pro 6000: 98 → 91 |
| gpt-oss-120b MXFP4 | 64 | 88 → 65 | 1300–2700 t/s | RTX Pro 6000: 221 → 179 |
| Qwen3-Coder-Next 8-bit | 85 | 79 → 69 (48 at 64K) | 750–1900 t/s | — |
| Qwen3.5-27B dense 6-bit | 26 | 24 → 15 | 590–810 t/s | RTX 5090: 49 → 45 |

Read: **a MoE with ~10B active runs at 55–90 tok/s on the Max, a dense 27B at 15–24** —
generation is bandwidth-bound, and 614 GB/s is a third of an RTX Pro 6000. Prefill is where
the M5 generation moved (per-core neural accelerators): 800–2,700 t/s, so a 32K-token prompt
lands in 15–40 s rather than minutes. Community figure for DeepSeek V4 Flash (284B/13B) at
2-bit on the same box: ~39 tok/s (REPEATED, single report).

**M5 Ultra 512 GB, DERIVED (nothing measured yet):** memory bandwidth doubles (1.2 TB/s), so
generation should land near **2× the Max column** for the same model, and the memory opens the
next tier — GLM-5.3-Flash at 4-bit (200 GB), DeepSeek V4 Flash at 4-bit (~150 GB), or the
GLM-5.3 flagship at 2-bit (245 GB) with room for context. At 40B active parameters the
flagship would generate at roughly a quarter of a 10B-active model's rate — call it 15–25
tok/s DERIVED — usable for an agent loop, slow for chat. Kimi K3 and DeepSeek V4 Pro still
do not fit: 1.4 TB and 0.8 TB at 4-bit.

**So, can you run local LLMs well on these?** Yes on both, with a clear split. *M5 Max 128
GB* is a strong single-user box for everything up to ~120B-A10B MoEs at 4–8-bit and dense
27–32B at 6–8-bit — i.e. Qwen3.8-27B (this note's pick) at Q8 with the whole 262K context, or
Qwen3.6-35B-A3B at silly speed; it cannot hold GLM-5.3-Flash at any quality above 3-bit.
*M5 Ultra 512 GB* is the only consumer-shaped machine that holds a near-frontier open model
(GLM-5.3-Flash 4-bit, MIT) with headroom, at 2× the Max's speed — for a price that buys
roughly 24 months of Z.ai's GLM-5.3 at heavy use. The honest comparison is not Mac vs GPU
but *own vs rent*: the Mac wins on privacy, on running all day at no marginal cost, and on
memory-per-krona; a single RTX Pro 6000 wins on speed and loses on capacity (96 GB).

## What to buy at normal prices, Sweden, 2026-09 (added 2026-09-02)

Prices are retail search results on 2026-09-02 (REPEATED; NetOnNet, Scandinavian Photo,
TeknikScout, Macworld.se, Apple SE), not quotes. Bandwidth figures from vendor pages and
Tom's Hardware / community measurements as marked. Generation speed ≈ bandwidth ÷ bytes of
active weights, so the two columns that matter are memory (what fits) and GB/s (how fast).

| box | memory for the model | bandwidth | price (SEK) | what it runs well |
|---|---|---|---|---|
| **used RTX 3090 24 GB** in an existing PC | 24 GB | 936 GB/s | ~12 200 (median of 15 sales/30 days) | Qwen3.8-27B Q4–Q5, Qwen3.6-35B-A3B, Gemma 4 26B — fast. The price floor is held up by AI buyers, not gamers |
| RTX 5070 Ti 16 GB | 16 GB | 896 GB/s | ~14 000 | the 16 GB tier: 35B-A3B / 26B-A4B MoEs, 27B only at Q3 |
| **Mac mini M5 Pro 64 GB** | 64 GB shared | M4 Pro was 273 GB/s; M5 Pro not verified | from 22 495 (24 GB); 64 GB configured higher, not priced here | 27B at Q8 with long context, 120B-A10B MoEs at 4-bit at modest speed; silent, 24/7 |
| Framework Desktop / other Strix Halo (Ryzen AI Max+ 395) 128 GB | 128 GB shared | 256 GB/s nominal, 210–215 measured | ≈ $2 200–2 300 ex VAT (~27 000 with Swedish VAT, DERIVED) | 120B-class MoEs that fit nowhere else at this price; ~100 t/s on Qwen3-30B-A3B, single-to-low-double digits on a dense 70B |
| NVIDIA DGX Spark 128 GB | 128 GB | 273 GB/s | $4 699 | same memory as Strix Halo at twice the price; CUDA is the only reason |
| **Mac Studio M5 Max 128 GB** | 128 GB shared | 614 GB/s | ~70 700 (128 GB / 1 TB); base 36 GB from 32 995 | the measured table above: 55–90 tok/s on 10B-active MoEs, 24 on a dense 27B, prefill 800–2 700 t/s |
| RTX 5090 32 GB (new) | 32 GB | 1.8 TB/s | 50 000–54 000 new, ~35 000 used — up 35% since launch | fastest 27–32B box there is; fits nothing above ~35B dense |
| Mac Studio M5 Ultra 512 GB | 512 GB | 1.2 TB/s | from 72 995 (96 GB); 512 GB well above 100 000 | GLM-5.3-Flash 4-bit; see above |

**The recommendation at normal money:**

1. **≈ 12 000 kr — a used RTX 3090** into a PC you already have. 24 GB at 936 GB/s is the
   best tok/s-per-krona on this list by a wide margin and runs this note's pick
   (Qwen3.8-27B at Q4/Q5) faster than any Mac under 100 000 kr. Costs: power (350 W),
   noise, and 24 GB is the hard ceiling.
2. **≈ 25 000–30 000 kr — Mac mini M5 Pro 64 GB or a Strix Halo 128 GB box** if the
   priority is *what fits* over *how fast*, and quiet 24/7 operation. Strix Halo holds 120B
   MoEs for the price of a 5070 Ti PC; the mini is the tidy option if 64 GB is enough.
3. **≈ 70 000 kr — Mac Studio M5 Max 128 GB** is the first machine that is both large and
   fast, and the point where a Mac beats the GPU route on capacity without losing badly on
   speed. Above that, the M5 Ultra buys memory nobody but GLM-5.3-Flash and DeepSeek V4
   Flash need.
4. **A new RTX 5090 at 50 000+ kr is the worst value here** for LLMs: 32 GB for the price of
   an M5 Max 128 GB, the price up 35% since launch. Buy it for speed on ≤32B or not at all.

DGX Spark: skip unless CUDA-only tooling is the constraint.

## For this repo

An extra arm on a 27B local model would need a machine we do not have (this box: 15 GB
RAM, no GPU). The realistic non-Claude arms remain hosted: GLM-5.3 via Z.ai's
Anthropic-compatible endpoint ([[glm-5.3-local]]) or a free rate-limited endpoint with a
logging clause ([[model-agnostic-agent-harnesses]]). Revisit this note when a build box
with ≥24 GB VRAM exists; Qwen3.8-27B is then the first candidate, and the measurement is
the same three-arm design with the model tier recorded per run.

Which jobs a local arm may take once the hardware exists, and the wiring and losses of the Ollama path: [[model-routing-free-and-local]] (added 2026-09-02).

## Verified against the cards themselves, 2026-09-04

This note carried the weakest evidence ratio in the base (6 REPEATED against 1 MEASURED), and its
sources are Hugging Face model cards that the same day's baseline batch stored locally
(`knowledge/raw/baseline-2026-09-04/`). So the table's headline numbers were read back against
the cards rather than against memory. **Caveat that decides how much this is worth:** those are
the cards as of 2026-09-04, not the bytes this note was written from, so this checks the claims
against the CURRENT cards — it cannot verify what was read at the time.

| Claim | Against the card | Verdict |
|---|---|---|
| `SWE-bench Verified Qwen3.6-35B-A3B 70.1` | NVIDIA card, benchmark table, column 2 header reads `Qwen 3.6 35B A3B`, row `SWE-bench Verified` = `70.12` | MEASURED, and correctly attributed to the column — a number without its header is not evidence |
| The designations `Gemma 4 26B-A4B` and `Qwen3.6-35B-A3B` | both are the NVIDIA card's own column headers (`Gemma 4 26B A4B`, `Qwen 3.6 35B A3B`), spaces where this note writes hyphens | MEASURED |
| Nemotron "loses on every row" | 13 of 14 comparable rows lose; **IFBench (loose) 71.88 vs 63.71 wins** | REFUTED, corrected above |
| `Qwen3.6-27B` context | its card: "262,144 natively and extensible up to" 1,010,000 tokens | MEASURED |

The lesson is the third row. An **absolute** ("every row", "always", "never") is the cheapest
claim to write and the cheapest to refute: it takes one counterexample, and a table with fourteen
rows offers fourteen chances to be wrong. The corrected sentence is longer and says less, which is
the trade.
