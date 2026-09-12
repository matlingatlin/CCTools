---
title: Soup — fine-tuning an 8B model on a 4 GB laptop GPU by layer streaming, and a retraction done right
sources:
  - url: https://github.com/MakazhanAlpamys/Soup
    fetched: 2026-09-02
  - note: "58-second video ('AI fine-tuning just got a lot less expensive'), transcribed locally 2026-09-02; claims graded."
tags: [fine-tuning, ml, local, measurement, retraction, claims-graded]
related: ["[[research-methodology]]", "[[claude-code-ecosystem-plugins]]", "[[testing-skills-methodology]]", "[[model-agnostic-agent-harnesses]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[best-local-llm-2026-09]]", "[[model-routing-free-and-local]]"]
raw:
  - knowledge/raw/watch-2026-09-08/raw.githubusercontent.com_MakazhanAlpamys_Soup_HEAD_README.md.md
  - "the 2026-09-02 read predates the raw layer; url + fetched are its only provenance"
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

## Two releases read in at once, 2026-09-12 — and three instances of ONE failure shape

The watcher reported this README changed; the diff replaced the **v0.74.0** release block with
**v0.75.0**, so v0.74's figures were in the raw layer from 2026-09-11 and never read into this note.
Both are recorded here. Verbatim from the README unless marked.

**v0.75.0 fixes, in one release, three separate cases of a setting being ACCEPTED and then
silently ignored.** That is the failure shape this base keeps finding in other people's surfaces —
*the failure is not that it errors, it is that it parses* — and it is worth having a vendor's own
worked example of fixing all three at once:

1. **An unknown config key now refuses the load.** *"A typo like `quantizaton`, or a key that only
   exists on a newer Soup, used to be dropped while the run proceeded with the setting not
   applied"* — now exit 1 on the CLI and `ValueError` in the API, naming the field you probably
   meant. **Breaking, and deliberately telegraphed:** *"v0.74 warned and named this release as the
   deadline."* A silent-drop deprecated through one release with a named end date is the honest way
   to do it.
2. **MLX honoured a config it had accepted.** Six options — `train_on_responses_only`,
   `warmup_ratio`/`scheduler`/`weight_decay`/`optimizer`, `max_grad_norm`,
   `gradient_accumulation_steps`, `gradient_checkpointing` — were *"each validated and then dropped
   on `backend: mlx`"*. So the same `soup.yaml` trained **a different recipe on MLX than on
   transformers, silently**. And the sharpest detail: *"Only 8 of the 32 optimizer names have an MLX
   equivalent; the other 24 are refused by name instead of silently becoming AdamW."* Refusing by
   name rather than falling back to a default is the same choice `knowledge/pdftext.py` makes about
   an unreadable PDF.
3. **Validation loss existed nowhere.** *"It was computed on every backend and thrown away: no
   metrics column, no event field, nothing on the panel."* An honest signal computed and then
   dropped — which is, word for word, the failure Scio's ADR-0001 says that project documented in
   its predecessor five times over. Three independent projects, one shape.

Also in v0.75.0: `grpo_variant: gspo` is now the published sequence-level objective
(arXiv:2507.18071), *"replacing a column-centering heuristic in which a padding token also shifted
the gradient of every row sharing its column"* — **existing gspo configs will not reproduce prior
runs**, which is a reproducibility break stated plainly. Web UI read endpoints and SSE now require
auth with short-lived single-use tickets instead of a token in a query string. `torch>=2.6.0`.
**All 60 pull requests came from outside the maintainer, by 22 people.** Python **3.10–3.12** only.

**v0.74.0, read from the 2026-09-11 baseline and now superseded — kept because its numbers are the
measured ones.** *"The frozen base was being loaded in fp32 the whole time."* Every SFT load
upcast a base that never receives an optimizer step, on all three load paths. Measured on an H100
with Llama-3.1-8B + LoRA: **48,241 MiB → 18,658 MiB peak, 2.59×, 28.9 GB**, byte-identical across
three repeats. Also: the free Colab/Kaggle tier *"could not stream at all"* (T4/P100/V100/GTX 16xx),
because peft creates LoRA adapters in the checkpoint's dtype while the fp16 GradScaler needs fp32
gradients. **Four SSRF bypasses of the same shape** — abbreviated, decimal, hex and octal IPv4
spellings (`127.1`, `2130706433`, `0x7f000001`, `0177.0.0.1`) reached the telemetry and webhook
guard *"and, through a path the first fix never touched, the OTLP tracing validator"*. `soup serve`
became exit 2 when bound to a non-loopback host without `--tool-auth-token`. **116 of 120 PRs from
outside the maintainer, by 25 people.**

**The v0.74 → v0.75 arc is itself the lesson.** v0.74 shipped a known limitation in its own release
notes — *"the declared `torch>=2.5.0` floor does not work with `trl>=0.29`"*, at which point every
preference trainer was dead — and v0.75 closes it by raising the floor. A project that publishes the
limitation it shipped with, names the release that will end a deprecation, and states which configs
will stop reproducing, is one whose README can be trusted as a source. That is worth recording
about a source, not just from it.

**Added since we read it — caught by the watcher, 2026-09-08.** The first CHANGED row this
watcher has produced that was worth acting on. The README gained a **`## Web UI`** section:
`soup ui` "serves a local dashboard for experiments, training setup, live metrics, dataset
exploration and model chat", installed as `pip install "soup-cli[ui]"` and served at
`http://127.0.0.1:7860`. Nothing about the layer-streaming claims below changed. Recorded because
it moves the project out of CLI-only, which is the kind of scope growth a note written from one
README silently goes stale on.

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
The base it would be trained from is picked in [[best-local-llm-2026-09]] — which is a table by
memory tier precisely because 4 GB is the constraint this project removes, so the two pages
answer one question from opposite ends: what fits, and what stops having to fit. Whatever comes
out still needs a harness to run under, and [[model-agnostic-agent-harnesses]] is where that
choice is recorded, including Anthropic stating that pointing Claude Code at a non-Claude model
is unsupported. An adapter trained here is therefore a supported *tool* and an unsupported
*agent* — worth keeping straight before anyone plans on it.

**Its retraction practice is a method, not a courtesy**, and two of our own pages set the bar
it clears. [[research-methodology]] requires the primary to be read rather than the summary,
and this note is the case where the primary changed under a claim: v1's bottleneck was
measured false in v3, so anyone citing the video's version is citing a retracted number.
[[testing-skills-methodology]] holds the same discipline turned inward — a wrong number
corrected in a new version, the old one left standing and cited, is exactly what a measured
build is asked to do here. A one-person project doing it in public is the evidence that the
overhead is affordable — and it is no longer the only instance. `code-review-graph`, graded in
[[claude-code-ecosystem-plugins]], re-captured its benchmark on 2026-08-02, published numbers
**lower** than the capture they replaced, and gave the reason. Two unrelated single-author
projects doing this makes it a practice rather than an anecdote.
