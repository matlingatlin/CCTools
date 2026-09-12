---
title: Soup — fine-tuning an 8B model on a 4 GB laptop GPU by layer streaming, and a retraction done right
sources:
  - url: https://github.com/MakazhanAlpamys/Soup
    fetched: 2026-09-02
  - note: "58-second video ('AI fine-tuning just got a lot less expensive'), transcribed locally 2026-09-02; claims graded."
status: verified
tags: [fine-tuning, ml, local, measurement, retraction, claims-graded]
related: ["[[research-methodology]]", "[[testing-skills-methodology]]", "[[model-agnostic-agent-harnesses]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[best-local-llm-2026-09]]", "[[model-routing-free-and-local]]"]
---

# Soup

MEASURED from the README unless marked.

- **What:** "Fine-tune LLMs from one YAML." Layer streaming "streams the frozen base from
  host RAM one decoder layer at a time", so the frozen base never sits in VRAM; only the
  trainable adapter and one layer do. Methods: SFT, DPO, GRPO, KTO, ORPO, SimPO, IPO, BCO.
  Apache-2.0. 4.8k stars on 2026-09-02. Author Alpamys Makazhan (the video's "Alpamees
  Makajan"; Kazakhstan per the video, not stated in the README).
- **The measurement:** RTX 3050 Laptop 4 GB, Llama-3.1-8B-Instruct + NF4, **119.6 tok/s,
  3.32 GB peak VRAM, "bit-exact against a normal resident run"**. Zenodo DOI
  10.5281/zenodo.21918325 (v3), concept DOI 10.5281/zenodo.21771064.
- **The retraction, which is the reason this note exists:** v3 (August 2026) retracts v1's
  claim that "layer streaming is bound by host-to-device transfer" — measured false; the
  bottleneck is per-layer NF4 dequantisation at ~9.8% of step cost. Earlier versions
  stay citable at their own DOIs and are not edited; "the measurement records behind
  every number ... published as written — including the failures, the assumptions that
  turned out wrong, and the numbers that were measured and then discarded" (visible in
  the video's frame of the README).

**Video claims graded** (two creators, 2026-09-02, near-identical scripts — the "85,000 users", the "PlayStation" and the "worst nightmare for AI companies" recur verbatim, which is a sign of one press kit, not two observations). "8B on a 4 GB GPU that costs less than a PlayStation" — MEASURED
(the GPU claim; the price is fluff). "Over 85,000 people are already using it" — no source,
UNVERIFIED; the README gives no user count. "Data centers / thousands of dollars" —
framing. "Democratizes AI / destroys the business model" — not a claim.

**Why keep it.** Two reasons. It is in core domain (ML tooling) and a real capability: a
fine-tune on a laptop is what makes "train a small judge on our own graded rounds"
affordable, if we ever want an `llm-judge-calibration` model rather than a prompt. And
its retraction practice is the standard this repo's CONSTANTS.md asks for — a wrong
number corrected in a new version with the old one left standing and cited — done in
public by a one-person project, which removes the excuse that it is too much overhead.

A fine-tuned local model would be arm D in [[model-routing-free-and-local]] (added 2026-09-02).
