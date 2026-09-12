---
title: "System prompt leaks" — Anthropic publishes the claude.ai system prompt, so what a leak adds is the unpublished tool layer
sources:
  - url: https://platform.claude.com/docs/en/release-notes/system-prompts/overview
    fetched: 2026-09-02
  - url: https://platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5-1
    note: "Read in full: the September 1, 2026 entry."
    fetched: 2026-09-02
  - note: "23-second video ('system prompt leak for Fable 5 ... this is huge'), frames show Pliny the Liberator's X post ('Fable 5.1 system prompt, 270,000+ characters') and the CL4R1T4S repo file ANTHROPIC/Claude-Fable-5.1.md (2,195 lines). Transcribed 2026-09-02; graded."
status: verified
tags: [anthropic, system-prompt, transparency, security, claims-graded]
related: ["[[loop-engineering-and-fable-prompting]]", "[[claude-code-ecosystem-plugins]]"]
---

# What a "leak" of Claude's system prompt is, and is not

**MEASURED.** Anthropic publishes the claude.ai / mobile-app system prompt for every model on
its docs site — eighteen entries from Claude Haiku 3 to **Claude Fable 5.1, dated
September 1, 2026** — with the statement: "This prompt is periodically updated to improve
Claude's responses. These system prompt updates do not apply to the Claude API." The Fable 5.1
text read today is a few thousand words: product information, refusal handling (child
safety, weapons, malware, copyrighted lyrics and artwork), legal/financial caveats, tone and
formatting, wellbeing, evenhandedness, the reminder taxonomy, and a knowledge-cutoff clause
("the end of Jun 2026").

**What the video calls a leak.** Pliny's post claims "270,000+ characters" and the mirrored
file is 2,195 lines. The published prompt is far shorter, so if the mirrored text is genuine
the difference is the **unpublished operational layer** — tool definitions, artifact and
memory instructions, search and file-handling rules, per-feature blocks — which Anthropic's
page does not claim to cover. That part is UNVERIFIED here: the mirror was not read, and a
text that circulates as "leaked" can be assembled from real fragments and invention alike.

**Video claims graded.**
- "System prompts are how the thought of the LLM operates ... the actual blueprint of Fable
  5.1" — WRONG. A system prompt is instructions read at the start of a conversation; the model
  is the weights. Anthropic publishes the instructions *because* they are not the model.
- "Jailbreak comes easier, competitors now have this" — the published half was always
  public, by design; the unpublished half, if genuine, tells an attacker which tools exist,
  which is information, not a bypass. The refusal rules themselves are published.
- "Broke within one hour" — no source; it is a mirror of a text, nothing "broke".

**For us.** Two practical facts. The published prompt is the reference for what claude.ai
Claude has been told about formatting, refusals and product facts — when a behaviour in
the chat app differs from Claude Code's, this page usually says why. And the claude.ai
prompt does not apply to the API or Claude Code, so nothing in it is an instruction our
dispatched runs receive; the Claude Code system prompt is the harness's own.
