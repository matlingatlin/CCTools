---
name: metric-driven-prompt-optimization
description: "Use when a prompt, system instruction, or agent instruction already has a labeled eval set and a trusted scorer, and it should be improved by an automated propose-evaluate-select loop rather than hand-tuning — reflective prompt evolution. The loop proposes candidate prompt variants, scores each on the eval set, reflects on the scored failures to seed the next round of candidates, and selects the best (GEPA / APE / MIPRO-style automated prompt search over the prompt text itself). Triggers on 'optimize the prompt against my eval set', 'automatic/automated prompt optimization', 'evolve or search the prompt', 'reflective prompt evolution', 'find a better prompt for these labeled examples', 'prompt candidate search', 'beat my current prompt on the metric'. NOT for sharpening a vague human request that has no eval (use prompt-refinement), tuning a skill's auto-invoke description field (use skill-description-optimizer), a general one-lever-at-a-time perf/latency/cost/code optimization (use measured-optimization-loop), building the eval harness (use eval-harness), or validating an LLM-as-judge scorer (use llm-judge-calibration) — those last two are prerequisites this loop consumes, not what it does."
---

# Metric-Driven Prompt Optimization

Improve a prompt by algorithmic search, not intuition: let a propose → evaluate → reflect → select loop mutate the prompt text and keep only variants that measurably score higher on a labeled eval set.

## When to use
- You have an instruction/prompt to improve AND a labeled eval set (inputs + expected outputs/labels) AND a scorer that returns a comparable number per example.
- Hand-tuning has plateaued, or the search space (wording, ordering, examples, constraints) is too large to explore by eye.
- You want reproducible, attributable gains — a record of which prompt won and by how much.

## When NOT to use
- No labeled set or no trusted scorer exists yet — build them first (eval-harness); validate a subjective judge first (llm-judge-calibration).
- The request itself is vague with no success metric — sharpen it (prompt-refinement).
- You are optimizing a skill's `description` for auto-invocation, not the working prompt (skill-description-optimizer).
- The target is code/perf/cost with human-formed hypotheses one at a time (measured-optimization-loop).

## Steps
1. **Fix the objective.** Name the single primary metric and direction, the eval set, and the held-out split. Reserve a validation slice never used for selection, to catch overfitting to the training slice.
2. **Baseline.** Run the current prompt over the training slice with the scorer. Record the aggregate score and per-example results. This incumbent is what every candidate must beat.
3. **Reflect.** Read the lowest-scoring examples. Write short, verbatim notes on *why* each failed (missing constraint, wrong format, ignored edge case). These failure notes — not guesses — are the raw material for proposals.
4. **Propose candidates.** Generate several distinct prompt variants, each targeting a failure pattern from step 3 (add a rule, reorder, add/remove a few-shot example, tighten output spec). Keep variants minimal and describable so a win is attributable. Vary one idea per candidate where possible.
5. **Evaluate.** Score every candidate over the same training slice, same scorer, same inputs. Rank by aggregate score; break ties by consistency (fewer catastrophic per-example failures).
6. **Select.** Promote the top candidate only if it beats the incumbent by a pre-stated margin. Ties or sub-margin gains do not promote. The promoted variant becomes the new incumbent.
7. **Guard against overfitting.** Periodically score the current incumbent on the held-out validation slice. If training score climbs while validation stalls or drops, stop — you are fitting the sample, not the task.
8. **Iterate.** Repeat 3–6 seeding proposals from the new incumbent's remaining failures, until gains fall below the margin, the budget is spent, or validation stops improving.
9. **Report.** Give baseline → final score on both slices, each promoted prompt and its delta, and the reflection that produced each win. Hand back the winning prompt verbatim.

## Rules
- Reflect before you propose: candidates must answer observed failures, not hunches.
- Select on the training slice; judge generalization on the untouched validation slice. Never tune against the validation numbers.
- State the promotion margin before evaluating — a margin chosen after seeing results proves nothing.
- Keep changes describable and minimal so each win maps to a cause; log promoted and rejected candidates alike for an auditable trail.
- Do not edit the scorer or the labels to make a candidate win — fix the prompt, not the ruler.
- A win is a margin-beating aggregate delta that holds on validation, not a prompt that merely reads better.
- Guard the held-out set from leaking into the prompt (e.g. as few-shot examples) — that inflates scores and invalidates the loop.
- Method only: this skill does not call models, run evals, or make network/CLI calls for you, and installs no auto-run hooks. You drive each round.
