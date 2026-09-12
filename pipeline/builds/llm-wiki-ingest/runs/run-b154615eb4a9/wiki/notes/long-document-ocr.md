---
title: Long-document OCR without chunking — Baidu's Unlimited OCR (R-SWA, constant KV cache)
sources:
  - url: https://the-decoder.com/baidus-unlimited-ocr-processes-dozens-of-document-pages-in-one-pass-by-treating-memory-like-human-forgetting/
    note: "Secondary, 2026-06. The HF card (baidu/Unlimited-OCR) and github.com/baidu/Unlimited-OCR were NOT fetched on 2026-09-02; every figure below is REPEATED from three consistent secondary write-ups (The Decoder, MarkTechPost, Labellerr) and the paper figure visible in the video frame."
    fetched: 2026-09-02
  - note: "12-second silent clip ('Baidu open-sourced the OCR everyone wanted') showing Figure 2 of the paper: 'Inspired by the process of humans copying books, we propose the Unlimited OCR ... a MoE-LLM decoder in which all attention mechanisms are R-SWA. The KV cache is implemented as a queue with a capacity of m+n — each time a new token is generated, the KV corresponding to the (m+1)-th token in the queue is evicted.'"
status: verified
tags: [ocr, documents, pdf, long-context, vision, claims-graded]
related: ["[[long-text-comprehension]]", "[[learning-resources-agents]]"]
---

# Unlimited OCR

**What it claims to solve.** OCR models on long documents split pages into chunks and lose
the thread between them, because the KV cache grows with every generated token. Unlimited
OCR keeps the cache **constant**: each generated token attends to all *reference* tokens (the
image tokens and the prompt, m of them) but only to the last n = 128 *generated* tokens; the
cache is a fixed queue of m + n and the oldest output token is evicted on every step. The
paper's own analogy: a person copying a book keeps their eyes on the source and forgets what
they wrote a page ago.

**Facts as reported (REPEATED):** released 2026-06-22 by Baidu; 3B-parameter MoE decoder with
~500M active; DeepSeek-OCR's DeepEncoder retained (SAM-base 80M + CLIP-large 300M, 16×
compression), every decoder attention layer replaced by R-SWA; **OmniDocBench v1.6 93.92**,
reported as a new state of the art; on Baidu's own long-document set, 20 pages in one pass at
edit distance 0.057 and 40+ pages still at 0.107; **MIT weights** on Hugging Face and
inference code on GitHub.

**Video claim graded:** "the OCR everyone wanted" — marketing; the technical claim (dozens of
pages, one pass, flat memory) is what the secondaries repeat and the paper figure shows.

**For this repo.** The reading pipeline (`pdf` skill → `deep-reading`) chunks long PDFs
because the OCR step does; a 3B MIT model that reads a 40-page document in one pass is the
component that would remove that seam, and at 500M active it runs on a laptop. Before
adoption: fetch the HF card and GitHub for licence and code (not done), and run it on one of
our own long PDFs against the current `pdf` path — a measured comparison, not the benchmark.
