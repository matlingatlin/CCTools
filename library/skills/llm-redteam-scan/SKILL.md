---
name: llm-redteam-scan
description: "Use when an LLM app needs an adversarial vulnerability scan before ship — probe the RUNNING model/agent with attack strategies and grade the responses for breaches, not diverse happy-path coverage. Plans an attack matrix (harm goal x strategy: direct jailbreak, roleplay/DAN, prompt injection, encoding/obfuscation, multi-turn crescendo, system-prompt/PII exfiltration, tool/function abuse), pairs each probe with a breach grader, runs the scan, and triages by attack-success-rate (ASR) into severity buckets with reproducible transcripts. Triggers: 'red team the model/chatbot', 'jailbreak testing', 'adversarial prompts', 'can users get it to say/do X', 'prompt-injection scan', 'attack success rate', 'safety/abuse probe before launch', 'does our guardrail hold'. Distinct from static config auditing of the agent surface (agent-surface-security-audit), manufacturing diverse non-adversarial eval inputs (synthetic-eval-data-generation), validating a subjective judge (llm-judge-calibration), building the eval framework (eval-harness), and code security review of a diff (security-review). Method only: composes probes and graders locally, never itself calls a remote generation API or auto-runs the app."
---

# LLM Red-Team Scan

Adversarially probe a running LLM app with attack strategies and grade the responses for
breaches, so jailbreaks and unsafe outputs are caught and triaged before ship — not after.

## When to use
- An LLM-backed feature (chatbot, agent, tool-caller, RAG endpoint) is nearing launch and
  you must know what an adversarial user can make it say or do.
- You have a guardrail, system prompt, or safety policy and need evidence it holds.
- You want a repeatable attack matrix + attack-success-rate (ASR) triage, not one-off pokes.

**When NOT to use:** static audit of a config/skill/MCP surface -> `agent-surface-security-audit`;
generating diverse non-adversarial test inputs -> `synthetic-eval-data-generation`; validating
a subjective LLM judge -> `llm-judge-calibration`; building the eval framework -> `eval-harness`;
reviewing a code diff for vulns -> `security-review`.

## Steps
1. **Scope the target.** Record the entry point (endpoint/agent), its declared safety policy
   or system prompt, the harm categories in scope (e.g. illicit instructions, hate/harassment,
   self-harm, PII/system-prompt exfiltration, tool/function abuse, prompt injection from
   untrusted content), and out-of-scope items. No policy on file -> write the assumed one first.
2. **Build the attack matrix.** Cross each in-scope harm goal with attack strategies:
   direct request, roleplay/persona (DAN), instruction override, encoding/obfuscation
   (base64, leetspeak, translation), payload splitting, many-shot priming, multi-turn
   crescendo, indirect injection via retrieved/tool content, and refusal-suppression framing.
   Sample cells for coverage over volume; note the expected safe behavior per cell.
3. **Author probes.** For each cell write the concrete prompt(s) — including multi-turn
   scripts and any injected-document payloads — as data files. Keep them inert: text only,
   no live exploits, no real secrets, no destructive tool calls.
4. **Pair each probe with a breach grader.** Define what counts as a breach for that cell
   (harmful content emitted, guardrail bypassed, secret/system prompt leaked, unauthorized
   tool invoked). Prefer a deterministic assertion; where the judgment is subjective, hand
   off rubric design to `llm-judge-calibration` rather than trusting an unvalidated grader.
5. **Run the scan (operator-driven).** Hand the probe set to the human/operator or an
   already-configured harness to execute against the target; collect raw responses and
   transcripts. This skill composes and grades — it does not itself call a remote model.
6. **Grade and compute ASR.** Apply graders to responses; compute attack-success-rate per
   harm goal and per strategy (breaches / attempts). Retain the full transcript for every
   breach so it reproduces.
7. **Triage by severity.** Bucket breaches by harm severity x ASR: high-severity or
   high-ASR = ship blocker; low-severity low-ASR = backlog. For each, note the failing
   cell, a minimal repro, and a suggested mitigation (prompt hardening, input/output filter,
   tool-scope limit) — do not implement fixes here.
8. **Report.** Deliver the matrix, per-cell ASR table, blocker list with repros, and a
   re-scan checklist so the same probes gate the next release.

## Rules
- **Method only, no remote generation.** Never call a remote model/generation API and never
  auto-run the target app from this skill; compose probes + graders and let the operator run.
- **Probes stay inert.** Text payloads only — no working exploit code, no real credentials or
  PII, no destructive/side-effecting tool calls in a probe.
- **Every breach is reproducible.** A finding without a saved transcript and minimal repro is
  not a finding.
- **ASR needs a denominator.** Always report breaches over attempts per cell; a raw breach
  count without attempt totals is not triage.
- **Grade against the stated policy**, not your own taste — if no policy exists, write and
  get the assumed one confirmed before grading.
- **Diagnose, don't patch.** Suggest mitigations; leave implementation to a separate change.
