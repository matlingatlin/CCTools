---
name: llm-eval-harness
description: "Use when a generated LLM app needs an assertion-based eval suite that gates prompt or model changes in CI — writes eval cases as code-level tests where each recorded input carries explicit assertions (exact/contains/regex/JSON-schema/tool-call-shape deterministic checks plus model-graded rubric assertions), organizes them into a versioned suite, and wires it as a CI gate that fails the PR when a prompt edit or model swap drops pass rate below threshold. Triggers on 'eval suite for my app', 'test my prompt', 'gate prompt/model changes in CI', 'assertion-based / model-graded evals', 'promptfoo/Braintrust-style eval', 'regression-test the LLM output', 'stop a prompt change from breaking prod'. Builds the shipped app's eval suite as a release gate. NOT for the eval-driven-development harness that scores a Claude Code agent or workflow's own task completion (use eval-harness), validating or calibrating an LLM-as-judge before its scores are trusted (use llm-judge-calibration), manufacturing the test inputs a suite consumes (use synthetic-eval-data-generation), categorizing existing failure traces (use error-analysis-taxonomy), automated prompt search against a labeled set (use metric-driven-prompt-optimization), or filling code-coverage gaps with unit tests (use test-coverage). NOT for reviewing a RETRIEVAL path itself (chunking, embeddings, rerank, top-k, grounding) — that is rag-pipeline-reviewer, an agent in .claude/agents/."
metadata:
  origin: ai-app-builder
tools: Read, Write, Edit, Bash, Grep, Glob
---

# LLM Eval Harness

Author an assertion-based eval suite for a generated LLM app's product code — deterministic checks plus model-graded rubrics — and wire it as a CI gate so a prompt edit or model swap cannot regress output quality unnoticed.

## When to use

- An LLM app ships prompts, system instructions, or a chosen model, and changes to any of them currently merge with no automated quality check.
- You want a versioned suite of input→assertion cases that runs on every PR and fails the build on regression.
- You are adding a CI gate that blocks a prompt/model diff when pass rate falls below a threshold.

**When NOT to use:** scoring a Claude Code agent's own task completion (use `eval-harness`); deciding whether a model judge can be trusted (use `llm-judge-calibration`); creating the inputs the suite runs on (use `synthetic-eval-data-generation`); grouping raw failure traces (use `error-analysis-taxonomy`); searching for a better prompt against a labeled set (use `metric-driven-prompt-optimization`); ordinary code unit-test coverage (use `test-coverage`).

## Steps

1. **Locate the units under test.** Grep the app for prompt strings, system messages, model ids, and the functions that call the LLM. List each callable surface (function name, its inputs, its output shape) the suite must exercise.
2. **Assemble a case set.** Gather real or representative inputs — happy path, edge, adversarial, and each past incident. If inputs do not exist yet, stop and hand off to `synthetic-eval-data-generation`, then resume. Store cases as data (JSON/YAML/table), one row per input, never hard-coded in test bodies.
3. **Write deterministic assertions first.** For each case attach the checks a machine can grade with certainty: exact match, contains/not-contains, regex, JSON-schema/parse validity, numeric range, latency/token budget, and tool-call shape (correct tool, required args present, no forbidden call). Prefer these — they are cheap, stable, and never flaky.
4. **Add model-graded rubric assertions only where determinism cannot reach.** For open-ended dimensions (tone, faithfulness, helpfulness) write a rubric assertion that names the dimension, the pass bar, and a 1–5 or pass/fail scale. Treat the judge as unvalidated until `llm-judge-calibration` clears it; mark such assertions `advisory` (reported, non-blocking) until then.
5. **Define the gate.** Set a threshold per suite (e.g. deterministic assertions must be 100%; graded pass rate ≥ target). Compute pass@1 for reliability and pass^k where stability matters. Record the current baseline so the gate measures regression, not an absolute.
6. **Structure the suite for CI.** Emit a runner (in the app's own test framework) that reads the case file, executes each callable, applies its assertions, and exits non-zero when the gate fails. Store under `evals/<surface>/` beside the code, versioned with it. Print a per-case PASS/FAIL table and the aggregate against baseline.
7. **Wire it as a required check.** Add the suite to the existing CI workflow as a step that runs on PRs touching prompts, model ids, or LLM-calling code. The human configures it as a required status check — this skill writes the job definition and describes the setting; it does not install hooks or auto-run anything.
8. **Document and hand back.** Record the suite location, cases covered, gate thresholds, and baseline in the app's docs so the next prompt/model change updates the baseline deliberately.

## Rules

- Cases are data, not code. New inputs must be addable without editing test logic.
- Deterministic assertion beats a graded one every time it can express the check — reach for the judge last.
- Never let an uncalibrated model grader block a merge; keep it advisory until `llm-judge-calibration` validates it.
- A flaky assertion in a release gate is a bug — fix or quarantine it, never leave it to fail intermittently.
- The gate measures regression against a recorded baseline; update the baseline as an explicit, reviewed act, never silently.
- Assert on output behavior, not on the prompt text — the suite must survive a rewrite that preserves behavior.
- No external network or CLI calls and no auto-run hooks: this skill authors suite and CI definitions; a human enables execution.
- Definition of done = suite written + baseline recorded + CI job defined + documented.
