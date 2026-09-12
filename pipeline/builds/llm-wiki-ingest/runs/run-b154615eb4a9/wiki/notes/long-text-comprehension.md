---
title: Long-text comprehension techniques
sources:
  - url: https://decodeclaude.com/ultrathink-deprecated/
    fetched: 2026-08-27
  - url: https://github.com/anthropics/claude-code/issues/19098
    fetched: 2026-08-27
  - note: user-provided tips text (unsourced), reviewed claim-by-claim 2026-08-27
status: verified
tags: [comprehension, context, tokens, reading]
related: ["[[skill-authoring-best-practices]]", "[[research-methodology]]", "[[loop-engineering-and-fable-prompting]]", "[[long-document-ocr]]"]
---

# Long-text comprehension techniques

Reviewed claims from a circulating power-user tips list, plus the techniques the
list was missing. Basis for the `deep-reading` skill.

## Verified claims

- **Work from files, not pasted walls of text.** Correct habit, wrong stated
  mechanism: total tokens are similar if the whole file is read. Real benefits:
  selective reading (line ranges, grep), persistence across `/clear` and
  compaction, re-readability, clean prompt history.
- **Session hygiene.** Context rot over long sessions is real. Distill to a
  notes/decisions file BEFORE context degrades; that file is the hand-off.
  (`/compact`, `/clear` are real; remote sessions also auto-summarize.)

## Outdated claims

- **"ultrathink allocates a ~32k thinking budget."** True in older builds
  (tiered keywords think < think hard < ultrathink). Deprecated Jan 2026:
  thinking is now on by default and adaptive. The keyword survives only as a
  per-turn "reason more deeply" nudge in current harnesses. Harmless, not a
  budget switch.
- **"Five secret codes for Claude Code: L99, /ghost, OODA, scaffold, ultrathink"** (short
  video, transcribed 2026-09-02). MEASURED against `code.claude.com/docs/en/interactive-mode`
  the same day: the built-in slash commands named there are `/btw /clear /config /effort
  /fast /help /login /model /rate-limit-options /recap /resume /status /tasks /teleport
  /theme /tui /upgrade /usage-credits`; **none of the five appears**, and the page does not
  mention ultrathink at all. The video's own frames show the words typed into a chat UI
  ("Moonlit chat", models "Opus 4.7" / "Sonnet 4.6"), not Claude Code. "OODA" and
  "scaffold" work as ordinary words in a prompt, because the model knows what they mean;
  "L99" and "/ghost" have no defined meaning anywhere and do whatever the model guesses.
  The one real lever the video gestures at is `/effort` (see
  [[loop-engineering-and-fable-prompting]]), which it does not name.

## Overstated claims

- **"Ask for restructured output to improve its logic."** Reformatting after
  the fact helps the reader and later turns; it does not retroactively improve
  comprehension. The stronger version: write structured notes WHILE reading.

## The techniques that actually produce comprehension

1. **Multi-pass reading:** structure skim (headings/TOC → outline) → deep read →
   targeted re-read of what the interrogation step exposed.
2. **Notes while reading:** per section capture claims, evidence, open
   questions, and relations to other sections. The writing is the forcing
   function, not the record.
3. **Interrogate the text:** generate questions about how parts interact;
   answer them from the text with location references; unanswerable → re-read.
4. **Concept map:** explicit entities + relations (graph-ready for a future
   knowledge-graph layer).
5. **Subagent fan-out** for very large documents: one reader per section with a
   fixed note template, then synthesis across returned notes.
6. **Self-test:** summarize from notes alone, then verify against the source;
   every mismatch marks something not yet understood — fix the notes.

## Token estimation heuristics

From ECC token-budget-advisor (heuristic, ±15%):
prose ≈ words × 1.3; code/mixed ≈ chars / 4. Useful for deciding when to
fan out subagents or split a document.

## Meta-lesson

The reviewed tips text shipped citations "[1][2][3]" with no URLs — unverifiable.
Hence the repo rule: every claim carries a source URL, fetch date, and status.
