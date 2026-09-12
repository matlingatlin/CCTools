---
title: Long-document OCR without chunking — Baidu's Unlimited OCR (R-SWA, constant KV cache)
sources:
  - url: https://arxiv.org/abs/2606.23050
    note: "PRIMARY, read 2026-09-08 via the arXiv HTML render. 'Unlimited OCR Works', Baidu Inc., submitted 22 Jun 2026, CC BY 4.0. Named by both repo READMEs; never fetched until now. Carries Tables 1, 3 and 4 and every figure the secondaries repeat."
    fetched: 2026-09-08
  - url: https://huggingface.co/baidu/Unlimited-OCR
    note: "Model card + config.json, read 2026-09-08 at the /raw/main/ path. Licence, architecture, the 128-token window. Repo created 2026-06-19 per the HF API - three days BEFORE the paper."
    fetched: 2026-09-08
  - url: https://github.com/baidu/Unlimited-OCR
    note: "README read 2026-09-08. Carries the paper link and the inference code; carries NO benchmark number, so nothing in the numbers below could ever have been verified from the repo alone."
    fetched: 2026-09-08
  - url: https://the-decoder.com/baidus-unlimited-ocr-processes-dozens-of-document-pages-in-one-pass-by-treating-memory-like-human-forgetting/
    note: "Secondary, 2026-06. The basis for this note until 2026-09-08, together with MarkTechPost and Labellerr. Kept: two of its figures turned out to be a selective reading, and one was simply wrong."
    fetched: 2026-09-02
  - note: "12-second silent clip ('Baidu open-sourced the OCR everyone wanted') showing Figure 2 of the paper: 'Inspired by the process of humans copying books, we propose the Unlimited OCR ... a MoE-LLM decoder in which all attention mechanisms are R-SWA. The KV cache is implemented as a queue with a capacity of m+n — each time a new token is generated, the KV corresponding to the (m+1)-th token in the queue is evicted.'"
tags: [ocr, documents, pdf, long-context, vision, claims-graded]
related: ["[[long-text-comprehension]]", "[[learning-resources-agents]]"]
raw:
  - knowledge/raw/untried-surfaces-2026-09-08/arxiv.org_html_2606.23050v1.html
  - knowledge/raw/untried-surfaces-2026-09-08/arxiv.org_abs_2606.23050.html
  - knowledge/raw/untried-surfaces-2026-09-08/huggingface.co_baidu_Unlimited-OCR_raw_main_README.md
  - knowledge/raw/untried-surfaces-2026-09-08/huggingface.co_baidu_Unlimited-OCR_raw_main_config.json
  - knowledge/raw/untried-surfaces-2026-09-08/raw.githubusercontent.com_baidu_Unlimited-OCR_HEAD_README.md.md
  - "the secondary write-ups this note was FIRST written from were not kept (fetched 2026-09-02, before the raw layer); they are superseded above rather than re-fetched"
---

# Unlimited OCR

**What it claims to solve.** OCR models on long documents split pages into chunks and lose
the thread between them, because the KV cache grows with every generated token. Unlimited
OCR keeps the cache **constant**: each generated token attends to all *reference* tokens (the
image tokens and the prompt, m of them) but only to the last n = 128 *generated* tokens; the
cache is a fixed queue of m + n and the oldest output token is evicted on every step. The
paper's own analogy: a person copying a book keeps their eyes on the source and forgets what
they wrote a page ago.

That analogy is the machine-level version of a rule this base already holds at the workflow level.
[[long-text-comprehension]] reaches the same shape from session evidence rather than architecture:
work from the file rather than the accumulated transcript, and distil to a notes file *before* the
context degrades. R-SWA does by eviction what session hygiene does by hand — full attention on the
source, a fixed window of what you have already produced. Worth reading together, because the
workflow rule is usually justified by token cost and this is a second, independent reason for it.

## Read against the primary, 2026-09-08 — one figure wrong, two selectively quoted

Everything below was REPEATED for six days from three secondary write-ups, with a note saying
the HF card and the GitHub repo had not been fetched. Both answer; **both name the paper**
(arXiv 2606.23050, "Unlimited OCR Works", Baidu Inc., 22 Jun 2026, CC BY 4.0), and the paper
renders as HTML. It was one link away the whole time.

**WRONG: the benchmark is OmniDocBench v1.5, not v1.6.** The paper's Table 1 and its own
summary sentence both say v1.5. A version number is exactly the kind of detail a secondary
mis-transcribes and nobody re-reads.

**MISLEADING: "a new state of the art" is a 0.02-point lead.** Table 1 puts Unlimited-OCR
3B-A0.5B at **93.92** with **Qianfan-OCR 4B at 93.90** on the row above, and Logics-Parsing-v2
at 93.33. The paper's own claim is the modest one — "**93% on OmniDocBench v1.5, outperforming
the DeepSeek OCR baseline by 6%**", i.e. against its own baseline, not against the field.

**SELECTIVE: the long-horizon numbers are the two friendliest points of a non-monotonic row.**
Table 3, edit distance by page count:

| pages | 2 | 5 | 10 | 15 | 20 | 40+ |
|---|---|---|---|---|---|---|
| Edit distance ↓ | 0.0362 | 0.0452 | 0.0526 | **0.0787** | 0.0572 | 0.1069 |
| Distinct-35 ↑ | 99.87% | 99.98% | 99.83% | 99.99% | 99.89% | 96.90% |

**15 pages is worse than 20.** The secondaries' "20 pages at 0.057, 40+ at 0.107" is a clean
degradation curve that the table does not show, and the paper's own sentence is the vaguer
"at 40+ pages, the edit distance remains below 0.11".

**MEASURED, upgraded from REPEATED** — verbatim from the paper unless marked:

- "**3B total and 500M activated parameters**", DeepSeek OCR as the baseline, DeepEncoder
  retained. Derivation from the shipped `config.json` agrees: 12 layers, hidden 1280, 64 routed
  experts + 2 shared, 6 routed per token ≈ 2.9B.
- "we replace **all** attention layers in the decoder" with R-SWA, and each generated token
  attends to every reference token plus "**the preceding n output tokens (128 by default)**" —
  and the shipped config carries `sliding_window_size: 128`, so the paper's default is the
  weights' default.
- "**dozens of pages … in a single forward pass under a standard maximum length of 32K**" —
  `max_position_embeddings: 32768` in the config.
- **MIT**, from the model card's own frontmatter (`license: mit`), with `vision-language` and
  `image-text-to-text` tags.
- The DeepEncoder is **SAM ViT-B + CLIP-L/14-224**, read straight out of `vision_config`
  (`sam_vit_b`: 12 layers, width 768; `clip-l-14-224`: 24 layers, width 1024) — the "SAM-base +
  CLIP-large" the secondaries name, now from the artefact.

**NEW — nothing said any of this:**

- **The decoder is DeepseekV2**, not a generic MoE: `auto_map` points at
  `configuration_deepseekv2.DeepseekV2Config`. The model is DeepSeek's decoder with its
  attention layers swapped, which is a much more specific claim than "a 3B MoE decoder".
- **The HF repo was created 2026-06-19, three days before the paper was submitted.** The
  "released 2026-06-22" every secondary carries is the *paper* date.
- **The speed claim is a theoretical ceiling, not a measurement.** Table 4 is headed
  "Theoretical inference performance ceiling comparison", prefill is fixed at **10** tokens, and
  the 35% lead is at 6,144 output tokens (Unlimited 7,847.71 TPS vs DeepSeek 5,822.87). At 256
  tokens the two are level. Nothing here is a document-OCR throughput number.
- **The paper names its own failure mode**, and it is not R-SWA: repeated errors "occur where
  small text in the PDF is difficult to discern, primarily due to the use of DeepEncoder's
  'Base' mode (1024 × 1024 resolution) under multi-page conditions". `candidate_resolutions`
  in the config holds exactly one entry, 1024 × 1024, so that is the shipped setting.
- **R-SWA is claimed general-purpose** — "equally applicable to tasks such as ASR, translation"
  — with no experiment in the paper. REPEATED, and by the authors about their own work.
- **Neither README carries a single benchmark number.** Anyone checking these figures against
  the repo alone would have found nothing to check them against.

**Video claim graded:** "the OCR everyone wanted" — marketing; the technical claim (dozens of
pages, one pass, flat memory) is what the secondaries repeat and the paper figure shows.

**For this repo.** The reading pipeline (`pdf` skill → `deep-reading`) chunks long PDFs
because the OCR step does; a 3B MIT model that reads a 40-page document in one pass is the
component that would remove that seam, and at 500M active it runs on a laptop. The first half
of the adoption gate is now closed — licence MIT, code and weights read, architecture known.
**What remains is the half that matters:** run it on one of our own long PDFs against the
current `pdf` path. Table 3 makes that more necessary, not less — a metric that is worse at 15
pages than at 20 is not a curve you can extrapolate to your own documents, and the paper's
stated failure mode (small text at 1024×1024) is exactly what a dense technical PDF has.

## That run is BLOCKED, not pending — measured 2026-09-11

The item stood as "the single highest-value open item, and it is a measurement" for three days.
It was never attempted, so nobody had checked whether it *could* be. It cannot, and the reason
is the one nobody looks for: **the baseline arm is missing too.** A comparison needs three
things, and this environment has none of them.

MEASURED here on 2026-09-11, in this container:

| precondition | state |
|---|---|
| a long PDF of our own | **0** `.pdf` files in the repo — *met later the same day: 3 held* |
| the baseline (`pdf` skill) path | **7 of its 8 scripts fail at import**; `pdftotext`, `pdftoppm`, `pdfinfo`, `qpdf`, `mutool`, `gs`, `tesseract` all absent |
| the Unlimited-OCR arm | no GPU; `torch` and `transformers` not installed; 15.7 GiB RAM, 29 G free disk |

The baseline failure is worth stating exactly, because "not installed" was the wrong diagnosis
the first time. `pdfplumber`, `pdf2image`, `PIL` and `reportlab` are genuinely **not installed**.
`pypdf` **is** installed (`/usr/local/lib/python3.11/dist-packages/pypdf`, imported by five of the
eight scripts) and is **broken**: it reaches `cryptography.hazmat.bindings._rust`, which needs
`_cffi_backend`, which is absent — and the failure surfaces as a Rust `PanicException`, not an
`ImportError`, so pypdf's own crypto-provider fallback does not catch it. An installed package
that panics is a different problem from a missing one, and only the second is fixed by a wheel.

**What this makes false elsewhere.** `CLAUDE.md` routes "Understand a long doc/paper/repo →
`deep-reading` (PDF via the `pdf` skill first)". In this environment that first hop does not
execute. The routing line is not wrong as a method — it is unexecutable here, which a capability
map cannot show, because a map lists what *exists*, never what *runs*.

**And it is not one skill but two.** The first pass checked `/mnt/skills/public/pdf/` and stopped;
there is also a separate `/mnt/skills/public/pdf-reading/`, which is the one a *reading* task
actually wants. It does not help: its documented first move is `pdfinfo` + `pdffonts` +
`pdftotext` + `pdfimages` + `pdfdetach`, and **all five are absent** — the whole poppler set —
with `pypdf` as its Python path, broken as above. So both PDF skills are unexecutable here, which
makes the finding stronger than first written, and the first write-up wrong in the narrow sense
that it named one skill where the evidence covers two.

Two of their own descriptions overlap on the contested job: `pdf` claims "reading or extracting
text/tables from PDFs", while `pdf-reading` claims the same and cedes only creation and form-filling
back. That is a live instance of what this repo's own description discipline warns about —
overlapping descriptions cause mis-triggering — observed in a skill set we did not write, and it is
why our routing line names the weaker of the two without being wrong by either description.

**Update, same day — precondition (1) is now met, and it sharpened the rest.** Three PDFs are held
in `knowledge/raw/pdf-sources-2026-09-11/`, and a stdlib-only reader, `knowledge/pdftext.py`, was
built and measured against them. It reads the two academic papers at **100.0%** and the 33-page
Anthropic guide at **17.6%** — the guide is CID-encoded, so its text needs ToUnicode CMaps that
nothing here can parse. That is the document an OCR comparison would want, and it is the one that
does not come out. So the baseline arm is now *partly* alive: a text-layer PDF can be read here with
no install at all, and a CID-encoded one cannot. Full argument and the preregistered rule it failed:
`pipeline/decisions/2026-09-11-stdlib-pdf-text.md`.

**RETIRED 2026-09-12: the block was a poisoned dependency, and the baseline arm is alive.** The
system `pypdf` is **6.17.0** — not missing, not old. It panics because the *system* `cryptography`
41.0.7 reaches a Rust binding needing an absent `_cffi_backend`. In an isolated virtualenv **the
same version — 6.17.0 — reads the Anthropic guide: 33 pages, 35,733 characters** (35,765 if the
pages are newline-joined), including the exact sentence this base quotes from it. The first
demonstration used 6.18.1, which left a version bump as an untested confound; the control is the
same version isolated, so the only variable is whether `site-packages` can reach the broken
`cryptography`. Nothing was installed system-wide. See
`pipeline/decisions/2026-09-11-stdlib-pdf-text.md`, third postscript and the positive control after it.
**And it is reproducible from this repo now:** `knowledge/pdfread.py` builds that isolated reader
with no network and no package manager - `python3 -m venv` plus a copy of the system `pypdf` that
is already on disk - and `--report` reads all nine held PDFs. The recipe had lived in `/tmp` through
three verification passes, which meant nothing here could reproduce any of them.

**The regression reading below was still correct and is kept, because it is how the block was
diagnosed.** `anthropic-skill-authoring-contract` records
its own source as extracted with **pdfminer.six**, page-counted with **pypdf**, on 2026-09-04.
Measured today: `pdfminer` is not installed and `pypdf` panics on import. The inference drawn from
that — *"this environment had a working PDF reader eight days ago and lost it"* — was **wrong, and
wrong in the safe-looking direction.** Nothing was lost: `pypdf` is present at the version it has
always been, and the 2026-09-04 extraction was done in a venv, exactly as it is done now. There was
no regression to explain, and the question the inference posed to the human — *"should we restore a
toolchain the base's provenance depends on"* — **is withdrawn rather than answered.** The reasoning
is kept because it is what drove the probe; the conclusion it reached is not.

**How much of the `pdf` skill the isolation alone recovers — measured 2026-09-12.** The claim above
and in `BRAIN.md` is *"7 of the 8 scripts in the public `pdf` skill fail at import"*, measured with
real imports on the system interpreter and correct there. Re-run under a virtualenv holding nothing
but `pypdf`, **5 of 8 pass**:

| script | system `python3` | isolated venv |
|---|---|---|
| `check_bounding_boxes.py` | OK | OK |
| `check_fillable_fields.py` | `pypdf(PanicException)` | **OK** |
| `extract_form_field_info.py` | `pypdf(PanicException)` | **OK** |
| `fill_fillable_fields.py` | `pypdf(PanicException)` | **OK** |
| `fill_pdf_form_with_annotations.py` | `pypdf(PanicException)` | **OK** |
| `convert_pdf_to_images.py` | `pdf2image` absent | `pdf2image` absent |
| `create_validation_image.py` | `PIL` absent | `PIL` absent |
| `extract_form_structure.py` | `pdfplumber` absent | `pdfplumber` absent |

So **the 7 failures were 4 parts poison and 3 parts genuinely missing**, and isolation with no
install at all takes the skill from 1 of 8 to 5 of 8. The conclusion that *"the dead route is one we
point at and do not own"* survives — but the dead route was overstated by four scripts, and the
difference is the same confusion that produced the original PDF block: **an import that raises is
not evidence that a package is absent.** It is worth noting *which* four: every one of them is a
form-filling script, so what isolation recovers is the half of the skill our routing line does not
want, and the reading half still needs `pdfplumber` or poppler.

**What would unblock the OCR comparison**, in the order that costs least: (1) ~~a long PDF in the
repo~~ — **done**; nine are held, and eight of the nine are fully readable; (2) ~~a working
`pypdf`~~ — **done**, at zero install cost, by isolation; (3) the rest of the `pdf` toolchain —
`poppler-utils`, `pdfplumber`, `pdf2image`, `Pillow`; (4) the OCR arm — `torch` plus ~3B of weights,
~6 GB at bf16, which the RAM allows and the absent GPU makes slow rather than impossible. Only (3)
and (4) are package installs and therefore the **fourth gate's** business. The baseline arm is alive;
what remains standing for the human is the OCR arm and the poppler half of the baseline, which is a
narrower question than the one this note opened with.
