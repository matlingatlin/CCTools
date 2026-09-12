---
title: Claudex Loop — a rival model attacks the plan, round after round, and never grades its own work
sources:
  - url: https://github.com/chaseai-yt/claudex-loop
    fetched: 2026-09-02
  - note: "Nine-slide carousel by Chase AI (chase.h.ai), screenshots received 2026-09-02; the run numbers below are from the README and the slides agree."
tags: [review, planning, cross-provider, convergence, codex, claude-code, claims-graded]
related: ["[[harness-over-model-prime-agent]]", "[[testing-skills-methodology]]", "[[loop-engineering-and-fable-prompting]]", "[[agent-builder-prior-art]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Claudex Loop

MEASURED from the README unless marked. MIT, **1.6k stars** (the slide says 1,270 — a few
days older). A Claude Code plugin: `/plugin marketplace add chaseai-yt/claudex-loop`,
`/plugin install claudex-loop@claudex-loop`; prerequisite Codex CLI ≥ 0.130 and
`codex login` on any ChatGPT tier, no pinned model.

**The invariant, verbatim:** "Whoever made the thing never checks the thing." Plan by Claude
→ attacked by Codex; code by Codex → reviewed by Claude; code by Claude → inspected by a
fresh Codex session. The slide's version: "The model that wrote the plan cannot be trusted
to grade it" — cross-provider so the reviewer has "nothing to defend".

**Four phases.**
0. **Recon** — Claude scouts the codebase (or prior art if greenfield) before asking
   anything; produces an *Assumptions Ledger* the user confirms in one reply. "No interview
   questions the code already answered."
1. **Interrogate** — a decision map split into *load-bearing* questions (asked one at a
   time, each with why it matters, a committed recommendation, and what breaks if guessed
   wrong) and *cosmetic* ones (batched, veto-by-exception), plus an escape hatch: "accept
   all remaining recommendations". "You enter at four points only."
2. **Review** — Codex attacks `PLAN.md` in a **read-only sandbox** (`-s read-only`, then
   `-c sandbox_mode="read-only"` on resume), **same Codex session across rounds** so it
   remembers its findings and attacks its own accepted fixes; Claude arbitrates and logs
   rejections; **`MAX_ROUNDS` = 5**, and a deadlock is flagged, "never faked".
3. **Build (optional)** — the user picks the builder; the rival grades the finished diff
   against the locked plan; the user approves the final diff.

**The one real run (README and slide agree):** 55 findings over five rounds, **26 → 15 → 12
→ 2 → 0**; one fatal ("private-schema contradiction — the access path cannot be built as
written"), ~6 data-corrupting model choices, ~7 missing subsystems; "every product decision
survived". `PLAN-REVIEW-LOG.md` keeps "the full round-by-round argument — the why".

**Claims graded.** All of the above is the author's own single run — n=1, no comparison
with a same-model reviewer, and the slide's "the plan read as completely plausible" is the
author's judgement. Nothing false was found; nothing is measured against an alternative.


**The 26 → 15 → 12 → 2 → 0 curve is the claim to check first**, and
[[testing-skills-methodology]] is where it was checked against our own runs: whole-artefact
reviews measured there did **not** converge in three rounds, three reviews came back red at
class level each time, and a round repeats because it is whack-a-mole rather than
disagreement. One author's n=1 run reaching zero, and our repeated runs not reaching it, are
not in conflict — but the curve should not be carried into a decision as if it were the
expected shape.

**Two neighbours mark the boundaries of the invariant.**
[[harness-over-model-prime-agent]] holds the opposite bet: Prime Agent's `/refine` reviews
*its own* trajectory and rewrites its own harness state, with rollback by ID as the safety
net rather than a second party. That is precisely the arrangement "whoever made the thing
never checks the thing" forbids, and neither side has measured the other — the disagreement
is real and open. [[agent-builder-prior-art]] holds the other end: of the three builders read
in full there, **not one cites a study, a benchmark, a measurement or a source**, and Claudex
is a fourth in that genre — an unusually well-specified procedure, still n=1. Its Recon phase
(scout the codebase, produce an Assumptions Ledger, "no interview questions the code already
answered") is the one thing that note records none of the builders having.

## Why this note exists

It is the closest external design to this repository's skill-builder, and it differs in
three places worth a decision each:

- **Reviewer keeps its session.** Our chain dispatches a *fresh* reader every round so it
  cannot see how the artefact was produced; Claudex keeps the *same* Codex session so it
  can attack its own accepted fixes. Both are defensible; ours pays for re-reading, theirs
  risks the reviewer defending its earlier verdicts. A same-session reviewer with a fresh
  *grader* at the end may be the cheaper shape — untested here.
- **Cross-provider by default.** Our readers and graders are Claude grading Claude with the
  arm labels blinded. Claudex's argument — same model, same blind spots — is the one
  Anthropic's own Fable 5 page half-concedes ("fresh-context verifier subagents outperform
  self-critique"). The cheap test is one build where 5.2 or 6.4 runs on Codex or GLM-5.3
  through the endpoint in [[glm-5.3-local]] and the findings are compared.
- **Convergence as the stop rule, cap 5.** Ours caps at 3 per field and escalates; theirs
  runs to zero findings or the cap and *flags* a deadlock. The 26→15→12→2→0 curve is
  exactly the shape `round_convergence.py` was written to detect, and their log format
  (finding, verdict, rejection reason, per round) is what our per-round ledger lacks.

Reuse-first: `interrogate`'s load-bearing / cosmetic split with a committed recommendation
per question is a sharper `clarifying-questions` than ours, and the Assumptions Ledger is
`requirements-discovery` in one screen. Both are worth reading before those are next
rebuilt.
