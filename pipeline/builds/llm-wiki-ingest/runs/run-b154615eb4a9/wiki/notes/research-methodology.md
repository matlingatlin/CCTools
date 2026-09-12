---
title: Multi-source research methodology
sources:
  - url: https://github.com/affaan-m/ECC/blob/main/.agents/skills/deep-research/SKILL.md
    fetched: 2026-08-27
  - url: https://github.com/affaan-m/ECC/blob/main/.agents/skills/documentation-lookup/SKILL.md
    fetched: 2026-08-27
status: verified
tags: [research, citations, phase-2]
related: ["[[long-text-comprehension]]", "[[testing-skills-methodology]]", "[[learning-resources-agents]]", "[[local-finetuning-layer-streaming]]", "[[llm-wiki-pattern]]"]
---

# Multi-source research methodology

Distilled from ECC's deep-research skill; basis for Phase 2 (research intake).

## Workflow

1. **Clarify the goal** (1–2 questions max; skip on "just research it").
2. **Decompose** the topic into 3–5 sub-questions.
3. **Multi-source search** per sub-question: 2–3 keyword variations, mix general
   and news queries, 15–30 unique sources total. Priority: academic/official >
   reputable news > blogs > forums.
4. **Deep-read 3–5 key sources in full** — never rely on search snippets alone.
   (Apply [[long-text-comprehension]] here.)
5. **Synthesize** into a cited report: executive summary, themed findings with
   inline citations, key takeaways, source list, methodology section, and an
   overall confidence rating.
6. **Parallelize** broad topics across subagents (one per sub-question cluster);
   main session synthesizes. The line runs between searching and writing:
   [[llm-wiki-pattern]]'s Astro-Han implementation states it as a rule — "Searching may run
   in parallel; compilation must not — compile one source at a time, because index.md,
   log.md, and cascade updates are shared state" (SKILL.md, fetched 2026-09-02). Every
   write target a research pass shares — an index, a log, the pages a cascade touches — is
   the reason step 6 fans out the reading and not the synthesis.

## Quality rules (adopt verbatim)

1. Every claim needs a source — no unsourced assertions.
2. Cross-reference; single-source claims are flagged unverified.
3. Prefer sources from the last 12 months.
4. Acknowledge gaps explicitly.
5. "Insufficient data found" beats guessing.
6. Separate fact from inference; label estimates and opinions.

## Live docs before training data

documentation-lookup's principle: for libraries/frameworks/APIs, fetch current
documentation instead of answering from training data (it uses the Context7 MCP;
without it, WebFetch against official docs serves the same purpose). Cap lookup
attempts (~3) and state uncertainty rather than looping. Redact secrets from
anything sent to external services.

---

## Verifying a quote: the checker is usually the defect — 2026-09-01

Three separate verification passes in one day, each reporting that an agent's quotes were
not in the source. **All three were my checker.** Corrected verdicts: 9 of 9 arXiv quotes
exact in the first case, 9 of 11 in the second with the other two explained.

The three faults, in the order they bit:

1. **Compared against `arxiv.org/abs`**, which carries only the abstract. Quotes from a
   paper's body cannot be there. Reported 6 of 6 missing.
2. **Compared against arXiv HTML when the agent extracted from the PDF.** Different
   rendering, different whitespace, different ligature handling. Matches fell from 6 to 3
   of 11 purely on rendering.
3. **No de-hyphenation across line breaks.** A PDF breaks `under-\nstanding`; a naive
   substring test then fails on any quote spanning a line end.

Two artefacts survive even a correct extraction and must be recognised rather than
counted as misquotes: **footnote markers interleaved mid-sentence** (`out of domain.5 for
example`), and **glyph decoding losses** (`cutoff` → `cuto`, an unmapped character
emitted as `cid 98`).

**The rule this yields.** Verify against the SAME rendering the quoting party used, and
normalise before comparing: case, whitespace, smart quotes, dashes, ligatures, and
hyphenation across line breaks. If a quote still fails, measure the longest common block
before concluding — 70% of a quote present with a ligature missing is an extraction
artefact; 0% present is a fabrication, and they need opposite responses.

**Why it matters more than it looks.** Every one of the three failures pointed the same
way: toward distrusting the source. That is the expensive direction. A checker biased
toward false alarms discards good evidence, and it does so while appearing rigorous.

## An out-of-sample validation ladder from quant trading (added 2026-09-02; out of core domain)

Source: a 43-second video ("four steps before you deploy an automated trading strategy"),
transcribed 2026-09-02. No primary source; the steps are standard practice in
systematic trading and are recorded as REPEATED, not verified here. Kept because the
ladder maps one-to-one onto how this repo decides whether a talent works:

1. **Parameter stability** — a heatmap over neighbouring parameter values; a single
   bright spike is overfit, a broad plateau is robust. Ours: a threshold that only holds
   at one repeat is the spike (`skill-measure`, "a win is counted once").
2. **Monte Carlo on *every* parameter set**, not the chosen one — resampling the
   winner alone is "doing it completely wrong". Ours: repeats across all tests, not
   the test that happened to win.
3. **Cluster analysis** over all results — meta-analysis of the sweep. Ours:
   `round_convergence.py` on classes rather than instances.
4. **In-sample / out-of-sample and walk-forward** — optimise on a window, test on the
   next, roll. Ours: `eval-set-curation`'s sealed holdout with a look log, and
   `preregistered-decision-rule`.

Bonus-domain scope (decision science), one video, no citation: a reminder that the
holdout-and-preregistration discipline is older than LLM evals, not a new finding.
