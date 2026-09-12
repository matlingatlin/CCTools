---
name: synthetic-eval-data-generation
description: "Use when an AI feature has no production traffic yet and you must manufacture a diverse test-input set to stress it before launch — cold-start eval data via structured dimension enumeration. Enumerates input dimensions (user intent, scenario, input shape, edge/adversarial condition, persona, locale, length) into a feature x scenario grid, samples the cells for coverage over volume, and emits labeled synthetic inputs with expected-behavior notes. Triggers: 'no real data yet', 'cold start eval', 'generate test inputs/cases', 'synthetic eval set', 'stress-test the prompt before launch', 'what inputs should I try', 'seed an eval with fake but realistic queries', 'coverage of edge cases'. Produces the INPUTS (and expected behavior) an eval consumes. NOT for building or running the eval framework itself (use eval-harness), categorizing failures from EXISTING traces (use error-analysis-taxonomy), validating an LLM judge (use llm-judge-calibration), or filling code-coverage gaps with unit tests (use test-coverage)."
---

# Synthetic Eval Data Generation

Manufacture a diverse, coverage-driven set of test inputs by enumerating input dimensions into a grid and sampling it — so an AI feature can be stress-tested before any real traffic exists.

## When to use
- A new prompt, agent, or AI feature is about to ship and there is no production data to draw an eval set from.
- You need inputs that deliberately span the space (edge cases, adversarial, multilingual, malformed) rather than a handful of hand-picked happy-path examples.
- You are seeding an eval-harness and need the rows it will run over.

## When NOT to use
- You already have real traces or logs — sample and analyze those instead (error-analysis-taxonomy); synthetic data is a cold-start fallback, not a substitute.
- You need the eval runner, scorer, or pass/fail gate (use eval-harness).
- You need to trust an LLM judge's scores (use llm-judge-calibration).

## Steps
1. **State the target.** Write one sentence: what feature takes what input and must produce what. Name the unit under test and its input contract (fields, types, format).
2. **Enumerate dimensions.** List the independent axes the input varies along. Typical axes: user intent/goal, scenario/context, input shape or format, length/complexity, persona or skill level, locale/language, and an edge/adversarial axis (empty, oversized, injection, ambiguous, contradictory, out-of-scope). Aim for 4–7 axes with 3–6 values each.
3. **Build the grid.** Cross the two or three highest-signal axes into a feature x scenario table; treat the remaining axes as tags you vary within cells. The full cross-product is usually too large — the grid is a coverage map, not the output.
4. **Sample for coverage, not volume.** Select cells so every value of every axis appears at least once (pairwise-style coverage), then over-weight the edge/adversarial axis. A few hundred well-spread inputs beat thousands of near-duplicates.
5. **Instantiate each cell into a concrete input.** Write a realistic input that actually exercises that combination — real-looking phrasing, plausible data, correct format. Vary surface wording so the set does not collapse into one template.
6. **Attach an expected-behavior note.** For each input record what a correct/acceptable response looks like (or the property it must satisfy) — enough for a human or judge to grade later. Mark inputs where the right answer is "refuse", "ask for clarification", or "out of scope".
7. **Label and store.** Emit structured records (id, input, axis-tags, expected-behavior, difficulty). Keep the axis tags so results can be sliced by dimension to find which region fails.
8. **Report coverage and gaps.** Summarize which cells are covered, which axes are thin, and where real data will later be needed to replace or validate the synthetic set.

## Rules
- Coverage over volume: maximize distinct dimension combinations, not raw count. Prune near-duplicates.
- Every synthetic input MUST carry an expected-behavior note, or it cannot be graded.
- Always include an adversarial/edge axis — empty, malformed, oversized, ambiguous, injection, and out-of-scope inputs are the point of pre-launch stressing.
- Keep the axis tags on every record so failures can be attributed to a dimension.
- Synthetic data is a scaffold: label it as synthetic and plan to replace or validate it against real traffic once it exists. Never report synthetic pass rates as production quality.
- Do not fabricate real people, real PII, or real credentials as "realistic" data — synthesize plausible fictional values.
- Method only. No network calls, no CLI installs, no auto-run hooks — you enumerate, sample, and write records by hand.
