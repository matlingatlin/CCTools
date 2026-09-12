# Evals — agent-architecture-audit

> Follows `templates/EVALS.template.md`. Authored against the ACTIVE DIRECTIVES in
> `pipeline/CURATION-LESSONS.md`. Baseline = a competent agent debugging the same
> situation WITHOUT this talent's 12-layer stack, code-first ordering, and
> falsify-the-wrapper discipline.

**Talent:** `agent-architecture-audit` · **Type:** discipline+technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
For each scenario, judge the likely output WITHOUT the talent (blame-first, prompt-first,
current-state-only reasoning) vs WITH its method (map to the 12 layers, falsify wrapper
before blaming model, code-first fix order, severity-ranked). A scenario passes only if the
with-talent result is materially better and meets the observable pass criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** S1–S3 are the everyday job; S4–S6 are traps/edge; S7 negative-trigger.
- [x] **Specific to this talent** — every scenario maps to a named layer / anti-pattern in SKILL.md.
- [x] **Observable pass/fail criterion** — each names the layer number and the concrete fix ordering
      an outsider can check against the skill.
- [x] **Clever scenarios: baseline plausibly FAILS** — S4/S5/S6 tempt blame-the-model, clean-state,
      or prompt-first errors that the SKILL.md anti-patterns explicitly forbid.
- [x] **Matches talent type** — pressure scenarios (S4,S5) tempt the wrong behavior under a plausible
      excuse; application scenarios (S1,S2,S3,S6) exercise the method.
- [x] **Negative trigger** (S7) — a look-alike where the talent should decline.

## Scenarios

### S1 — "Must use tool" only in prompt · application
- **Input:** Agent's system prompt says "You MUST call `verify_order` before answering."
  In production the model sometimes answers order questions without calling it. Code path:
  `if model_wants_tool: run_tool()` — no enforcement that the tool ran before the final answer.
- **Pass criterion (observable):** Diagnosis names **layer 6/7 (tool selection/execution)**,
  labels it a tool-discipline failure, and the top fix is **code-gate the requirement**
  (block/reject the answer in code when the tool did not run) — NOT "make the prompt more forceful."
- **Baseline (without talent):** Suggests strengthening the prompt wording ("MUST, ALWAYS, in caps").
- **With talent:** Quick-diagnostic Q1/Q6 → "tool not code-gated"; fix #1 code-gate tool requirements.
- **Result:** pass

### S2 — Old topic bleeds into new session · application
- **Input:** User starts a fresh chat about billing; agent volunteers advice about a coding
  problem from a session three days ago. Memory retrieval returns top-k by embedding similarity
  with no session/topic scoping and no recency/correction weighting.
- **Pass criterion (observable):** Names **layer 3 (long-term memory) contamination**, traces the
  **contamination path** (retrieval admits cross-session artifacts as pseudo-facts), and recommends
  tightening memory admission / scoping — does not merely tell the model to "stay on topic."
- **Baseline (without talent):** Adds a prompt line "only discuss the current topic."
- **With talent:** Q2/Q7 → memory contamination; fix #4 tighten memory admission.
- **Result:** pass

### S3 — Correct in logs, broken in the UI · application
- **Input:** Server logs show a well-formed JSON/markdown answer, but users see truncated or
  mangled output. The final answer passes through a streaming markdown renderer that re-parses
  partial chunks.
- **Pass criterion (observable):** Names **layer 10 (platform rendering / transport mutation)**,
  locates the defect in the delivery layer NOT the model, and recommends pass-through / reduced
  rendering mutation.
- **Baseline (without talent):** Retries generation or edits the prompt to "output cleaner formatting."
- **With talent:** Q5 → rendering corruption; fix #6 reduce rendering mutation.
- **Result:** pass

### S4 — "The model got dumber" (blame trap) · pressure
- **Input:** "Our agent was great last month; now it's confidently wrong. The vendor must have
  nerfed the model — should we switch providers?" The same prompt hits the raw API correctly in a
  playground. Between then and now the team added a distillation + active-recall layer.
- **Pass criterion (observable):** REFUSES to blame the model first; explicitly **falsifies the
  wrapper regression** (playground-vs-wrapper delta points at the new layers 4/5), per the
  "Avoid blaming the model before falsifying wrapper-layer regressions" anti-pattern. Provider
  switch is not the recommended action.
- **Baseline (without talent):** Accepts the framing, benchmarks providers, may recommend switching.
- **With talent:** Wrapper-regression pattern #1 + playground-works signal → audits layers 4/5 first.
- **Result:** pass

### S5 — "Can't reproduce, all green now" (clean-state trap) · pressure
- **Input:** A serious incident was reported yesterday (agent fabricated a refund confirmation).
  Today everything works in a live run. Pressure: "It's fine now, close the ticket."
- **Pass criterion (observable):** Refuses to let the **clean current state erase the dirty
  historical incident** (named anti-pattern); insists on auditing **historical logs/traces**
  (layer 12 persistence + layer 11 repair loops) rather than declaring healthy from one live run.
- **Baseline (without talent):** "Cannot reproduce → closes as not-an-issue."
- **With talent:** Anti-pattern "Do not let a clean current state erase a dirty historical incident";
  audits traces from the incident window. Reinforced by "Design audit, not one live run."
- **Result:** pass

### S6 — Output changes between generation and delivery · edge
- **Input:** Internal generation logs an answer of "3 items match." The user receives "I found
  several items." A silent post-processor runs a second LLM pass to "polish tone" with no contract
  and no logging of its input/output diff.
- **Pass criterion (observable):** Identifies a **hidden repair/agent layer (layer 11)** running an
  undisclosed second LLM pass, flags the missing contract, and orders **narrow/remove the hidden
  repair agent** high in the fix plan (fix #2) — above prompt tweaks.
- **Baseline (without talent):** Treats the reworded output as a generation problem; tunes the prompt.
- **With talent:** Q4/hidden-agent-layers pattern → layer 11; fix #2 remove/narrow hidden repair agents.
- **Result:** pass

### S7 — Plain null-pointer crash (negative trigger) · negative-trigger
- **Input:** "My Python service throws `KeyError: 'user_id'` on line 88 of `router.py`. There's no
  LLM, memory, or agent wrapper involved — it's a dict access on a request payload."
- **Pass criterion (observable):** The talent **declines / defers** — this is ordinary code
  debugging with no agent-stack layer implicated; points to `systematic-debugging` (or
  `agent-introspection-debugging`) instead of running a 12-layer audit.
- **Baseline (without talent):** N/A — negative trigger; the point is the talent must NOT over-fire.
- **With talent:** "Do not use for: general code debugging" boundary fires → hands off.
- **Result:** pass

## Failure triage (if any scenario failed)
None failed. If S4/S5 had failed only because the baseline agent already resisted the framing
(no discrimination), that would be a **test-bug** (weak trap) → sharpen the pressure, not the skill.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
- Note: S4 and S5 are the load-bearing discriminators — they encode the two anti-patterns most
  likely to be violated without the talent (blame-the-model, clean-state-erases-history).
