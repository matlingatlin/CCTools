# Untried surfaces, 2026-09-08

Every file here answers a question a note had already recorded as unanswerable — and in each
case the note said so honestly, naming the surface it had not tried. That was the selection
rule for this batch: not "which claim is weakest", but **"which claim has a surface nobody
opened"**.

## Baidu Unlimited-OCR — the whole of `long-document-ocr` was REPEATED

The note's own source line said the HF card and the GitHub repo "were NOT fetched". Both
answer, and **both name the paper** — arXiv 2606.23050, which renders as HTML.

| Stored | Bytes | What it settles |
|---|---|---|
| `arxiv.org_html_2606.23050v1.html` | 228,197 | PRIMARY. Tables 1, 3, 4; the R-SWA definition; "3B total and 500M activated" verbatim |
| `arxiv.org_abs_2606.23050.html` | 43,505 | Abstract, submission date 22 Jun 2026, CC BY 4.0 |
| `huggingface.co_baidu_Unlimited-OCR_raw_main_README.md` | 11,108 | `license: mit`; vision-language tags |
| `huggingface.co_baidu_Unlimited-OCR_raw_main_config.json` | 2,881 | DeepseekV2 decoder, `sliding_window_size: 128`, 32K positions, SAM ViT-B + CLIP-L/14 |
| `raw.githubusercontent.com_baidu_Unlimited-OCR_HEAD_README.md.md` | 11,585 | The paper link and the inference code — and **no benchmark number at all** |

The arXiv files are **not watched**: a published paper does not change under its identifier.
The HF card and the GitHub README are.

## Three plugin READMEs `claude-code-ecosystem-plugins` marked "READMEs not fetched"

`mksglu/context-mode`, `alexgreensh/token-optimizer`, `tirth8205/code-review-graph` — the
section header said the batch was REPEATED because nobody had opened them. All three answer.

Nothing here was edited after fetching; every file is stored as received.

## Graphiti — the maturity claim was filed under the wrong project

`temporal-kg-agent-memory` carried "v0.30 with frequent breaking changes (REPEATED,
vectorize.io review)" as a bullet about **gbrain**. The registries settle both halves:

| Stored | Bytes | What it settles |
|---|---|---|
| `pypi.org_pypi_graphiti-core_json.json` | 338,234 | `graphiti-core` **0.30.1**, Apache-2.0, uploaded 2026-09-01; 193 releases across 30 minor versions since 2024-08-27 |
| `raw.githubusercontent.com_getzep_graphiti_HEAD_README.md.md` | 28,280 | Requirements verbatim: Neo4j 5.26 / FalkorDB / Neptune+OpenSearch / Kuzu (deprecated), **plus an OpenAI API key**; the structured-output warning |

"v0.30" is graphiti-core's version; gbrain ships on npm at 1.3.1, so the bullet was
mis-filed. And "frequent breaking changes" no longer describes the project: the cadence went
10 releases in January 2026 → 6 in February → **one a month**, with **two in the last ninety
days**. A review accurate when written now reads as a warning about a project that has settled.

Note what the raw layer alone could not have told us. A README is a snapshot; **a release index
is a time series**, and the claim here was about change over time. Fetch the index, not the page,
when the claim is a rate.

## GLM-5.3 — the weights date, and one file deliberately NOT watched

`huggingface.co_api_models_author-zai-org.json` (40,755 B) settles a date every secondary
carries as "~2026-08-26/28": all four GLM-5.3 repositories carry `createdAt` **2026-08-25**.

**This file is deliberately absent from WATCH.tsv.** It is a listing whose payload includes
download counters, so it changes every day and would report CHANGED forever, teaching the
reader to ignore the column — the same reasoning that keeps the KB watching a model *card*
rather than a model *page*. What the file is kept for is provenance of a date, and a date
does not move. `createdAt` bounds the release from below; it does not prove the announcement
day, because a repository can be created private.

## ICM / MWP — "the 28-page paper not read"

`arxiv.org_html_2603.16021v1.html` (264,676 B). The note's source line named the untried
surface in as many words. The paper renders as HTML, and reading it corrected four things:

- **The layer token figures are Figure 1 of the paper**, not a secondary write-up. The
  REPEATED verdict was right that they are absent from the abstract and wrong to conclude
  where they came from. Five layers, not four, and a sum the note never had: **"Layers 0
  through 2 together contribute roughly 1,300 to 1,600 tokens."**
- **The method is called Model Workspace Protocol (MWP)** — 77 uses, against the title's ICM.
- **The author is Jake Van Clief** (with David McDermott). The video's "Jay Van Cleef" is
  wrong on both names.
- **The paper is not data-free**, which an abstract-only read implied: Figure 5 reports human
  edit frequency at each stage boundary from **33 practitioners** (92% / 30% / 78%,
  self-reported, values labelled approximate, with a Threats to Validity section).

Its own "no token-reduction number" is confirmed against the full text: the one reduction
figure in the paper is a *citation* to Jiang et al., used to argue the opposite point.

Not watched — a published paper does not change under its identifier.

## ARC Prize — the page that would not render, two attempts later

`arcprize.org_results_anthropic-claude-opus-5.html` (573,378 B). On 2026-09-02 this page
"did not render its numbers to two fetchers", so the Opus 5 ARC-AGI-3 score was REPEATED
from three outlets. It renders now. Three details the outlets did not carry:

- The verified table says **30.16%** at High; 30.2 is the rounding.
- **"Due to the short testing window, ARC-AGI-3 was evaluated only at High reasoning effort."**
  The Max row is blank — High was not a chosen operating point, it was the only run.
- ARC's own framing of the neighbouring results is flat: 97.5% ARC-AGI-1 and 90.4% ARC-AGI-2
  Semi-Private at Max are "competitive with previous frontier leaders, though at slightly
  higher cost".

The lesson generalises past this page: **a failed render is a dated observation, not a
property of the source.** Three of this batch's five findings came from re-trying a surface a
note had written off — a 401, a page that would not render, and a paper nobody opened.

## Second batch, same day — and one of them caught an error I had just made

Five more files, same selection rule.

| Stored | Bytes | What it settled |
|---|---|---|
| `raw.githubusercontent.com_NVIDIA-NeMo_Switchyard_HEAD_README.md.md` | 16,055 | The route types (no `prefill`; three routes the note was missing), Apache 2.0, and **NVIDIA's own Terminal-Bench 2.1 table** |
| `raw.githubusercontent.com_garrytan_gbrain_HEAD_README.md.md` | 76,781 | "100+ operations as MCP tools" verbatim; the LongMemEval numbers; **no release date at all** |
| `raw.githubusercontent.com_musistudio_claude-code-router_HEAD_README.md.md` | 24,253 | v3.0.22 with desktop installers and a `ccr ui` dashboard — well past the CLI the note describes |
| `raw.githubusercontent.com_1rgs_claude-code-proxy_HEAD_README.md.md` | 8,175 | Now dominated by Gemini, not the "OpenAI models" summary |

**The gbrain README caught a mistake made hours earlier in this same session.** The Graphiti
maturity correction had cited "gbrain ships on npm at 1.3.1" as half its evidence. The npm
package `gbrain` is `stormcolor/gbrain`, *"GPU Javascript Library for Machine Learning"*, created
2018-04-02 and last published 2018-11-15 — a different project. This project's README carries a
warning about exactly that collision: *"GBrain is NOT distributed on npm … it can shadow the real
binary on your PATH."* The conclusion held on graphiti-core's own version, but one leg of it was
borrowed from a name that happened to match. **A registry hit on a matching name is not an
identity check** — read the repository field and the publish dates before treating it as the
same project.

**And Switchyard's numbers are two different claims wearing one badge.** The "74% cheaper" that
travels on carousels is LangChain's 145-task suite. NVIDIA's own README reports Terminal-Bench 2.1
against a $98.06 / 76.0% Opus 4.8 baseline: **13-30% cheaper at 71-76% accuracy** — and the
cheapest route is the least accurate while the most accurate is the least cheap. A straight trade,
stated by the vendor, which is more useful than the number that travels.
