---
title: Learning resources on agents that checked out — CS329A, OpenMAIC
sources:
  - url: https://cs329a.stanford.edu/
    fetched: 2026-09-02
  - url: https://www.youtube.com/playlist?list=PL3058ht9NqT1NG6Y663elpHSDh-AW1TIr
    note: "Stanford Online playlist 'Stanford CS329A Series (Self-Improving AI Agents)'. Listing only; not watched."
    fetched: 2026-09-02
  - url: https://github.com/THU-MAIC/OpenMAIC
    fetched: 2026-09-02
  - url: https://chromewebstore.google.com/detail/notebooklm-web-importer/ijdefdijdmghafocfmmdojfghnpelnfn
    note: "Search listing only."
    fetched: 2026-09-02
  - note: "Three short videos, transcribed locally 2026-09-02; their claims graded below."
tags: [learning, courses, self-improving-agents, multi-agent, claims-graded]
related: ["[[effective-agents-anthropic]]", "[[model-agnostic-agent-harnesses]]", "[[research-methodology]]", "[[third-party-landscape]]", "[[long-document-ocr]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Learning resources that checked out

## Stanford CS329A — Self-Improving AI Agents

MEASURED from the course site: Autumn 2025, instructors Aakanksha Chowdhery and Azalia
Mirhoseini, 20 scheduled sessions. Syllabus: test-time compute scaling, robust
verification, learning from feedback with tools and code, multi-step reasoning and
planning, training-time scaling with RL, open-ended evolution of self-improving agents,
search-enhanced deep research agents, agentic frameworks for software engineering, memory
augmentation, agentic evaluations and long-horizon tasks, multimodal agents in robotics.

REPEATED (search results, Stanford Online channel): lectures uploaded publicly on
2026-08-03; the playlist has 9 parts (Part 1 course overview, 2 test-time compute, 3
robust verification, 4 learning from feedback with tools/code, 6 train-time scaling, 7
self-improvement and deep research agents, ...). Nine public videos against twenty
sessions: not everything was published.

Video claim "the skill Anthropic pays $700K for" — UNVERIFIED, no source given, and a
course is not a salary.

Why it is on our list: parts 3 (verification) and 7 (self-improvement) are the two
subjects this repo's pipeline is built on, and the reading list is the natural source for
`literature-review` runs on grader calibration and self-improvement loops.

**Practical route the video shows and which checks out in kind:** a Chrome extension
("NotebookLM Web Importer", Chrome Web Store, ~300k users per listing; third-party as far
as verified, not Google's) imports a YouTube playlist as NotebookLM sources; NotebookLM
then gives an audio/video overview, mind map, quiz, infographic. For a nine-lecture
course that is a defensible first pass before deciding which lecture to `deep-reading`.

## OpenMAIC — Open Multi-Agent Interactive Classroom

MEASURED from the repo: THU-MAIC (Tsinghua), MIT licence (two vendored packages carry
their own), 30.2k stars on 2026-09-02, v1.0.0 released 2026-08-27 ("agent workbench for
conversational course-building with durable sessions and 20 built-in skills"). Stack:
Next.js / React / TypeScript / Tailwind, orchestration in LangGraph. Paper: "From MOOC to
MAIC: Reimagine Online Teaching and Learning through LLM-driven Agents", JCST'26, DOI
10.1007/s11390-025-6000-0. Providers configurable: OpenAI, Azure OpenAI, Anthropic,
Bedrock, Gemini, DeepSeek, Qwen, Kimi, MiniMax, Grok, OpenRouter, Ollama and Lemonade
(local); model chosen via `DEFAULT_MODEL` with a provider prefix. OpenClaw integration
generates a classroom from Feishu/Slack/Discord/Telegram. No Claude Code integration.

Video claims graded: "#3 trending, ~30k stars" — consistent with 30.2k, trending rank not
checked; "only been out four or five days" — WRONG as stated: v1.0.0 was five days old,
the project and its paper predate it (JCST'26 paper, DOI year 2025).

**What "checked out" meant, and where the method lives.** Both entries were graded the way
[[research-methodology]] prescribes — the course site and the repository read directly, the
video's and the search results' version marked REPEATED beside them — and both turned up the
same class of error: a number that is roughly right (30.2k stars, nine of twenty lectures) sold
as something it is not. This page is therefore the small worked example of that workflow, on
sources that are *teaching material* rather than claims: what is checkable about a course is
its syllabus and its published lectures, not what it will teach you.

[[long-document-ocr]] is the other page in this base whose subject is a paper rather than a
tool, and it is the honest counterweight: its facts are REPEATED from the release rather than
run, so a resource being real and a resource being verified are two different findings. Read
them together before treating either as evidence for a build.

Why it is on our list: one prompt in, a whole course out, with the model swappable —
a reference implementation of a multi-agent generation pipeline with a graph
orchestrator, and a candidate source for a harvest wave (LangGraph patterns, skill
packaging in a Next.js app). Not a talent; a source.
