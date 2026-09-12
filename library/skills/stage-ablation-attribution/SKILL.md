---
name: stage-ablation-attribution
description: "Use when a multi-stage AI or data pipeline underperforms end-to-end and it is unknown WHICH stage is responsible — before committing effort to optimizing any one of them. Decomposes the pipeline into stages, substitutes one stage at a time with an oracle/ground-truth (or proxy-oracle) version, measures the end-to-end score each substitution unlocks, and converts that into per-stage headroom and an error budget that ranks what is worth optimizing. Triggers on 'which stage should I fix first', 'where is the pipeline losing accuracy', 'is it the retriever or the generator', 'is it the router, the tool call, or the summarizer', 'upper bound if this step were perfect', 'ablation', 'oracle retrieval/oracle context', 'error budget', 'attribute the loss', 'is optimizing X even worth it'. Applies to RAG pipelines, multi-step agent chains, ML/ETL pipelines, extraction-then-scoring flows. NOT for testing one already-chosen hypothesis against a baseline (use measured-optimization-loop), classifying WHAT is wrong in the final outputs rather than WHERE it originated (use error-analysis-taxonomy), qualitative design review of an agent stack (use agent-architecture-audit), building the scorer/eval set itself (use eval-harness), or root-causing a single failing run (use systematic-debugging)."
---

# Stage Ablation Attribution

Find which stage of a multi-stage system is actually costing you the score, before
optimizing anything. Replace one stage at a time with a perfect (oracle) version, measure
the end-to-end ceiling each replacement unlocks, and turn those ceilings into a per-stage
headroom ranking and an error budget. The payoff: you stop tuning the stage that is easiest
to tune and start on the stage that is actually capping the system.

## When to use
- A pipeline with 2+ distinguishable stages (retrieve → rerank → generate; plan → tool-call
  → summarize; parse → normalize → classify; extract → transform → load) scores worse
  end-to-end than you want, and nobody can say which stage is to blame.
- Someone proposes "let's improve the retriever / the prompt / the reranker" and there is no
  evidence that stage is the bottleneck.
- You need to decide whether a stage is even worth engineering effort — its headroom may be
  small enough that a perfect version barely moves the end-to-end number.
- You want an error budget ("42% of the loss enters at stage 2") to defend a roadmap.

## When NOT to use
- One hypothesis, one baseline, one metric to beat → `measured-optimization-loop`.
- You need to know what KIND of thing goes wrong in the outputs, not where it originated →
  `error-analysis-taxonomy` (it pairs well: run it first if you have no idea what "wrong"
  looks like, then use this skill to locate the origin).
- You want a qualitative design critique of an agent stack → `agent-architecture-audit`.
- There is no end-to-end scorer yet — build it first (`eval-harness`, or `llm-eval-harness`
  for a shipped LLM app); ablation with no metric measures nothing.
- The system is a single indivisible step. There is nothing to attribute.
- One run failed and you want the cause of that run → `systematic-debugging`.

## Steps
1. **Fix the end-to-end metric and the eval set first.** Name ONE primary end-to-end score
   and its direction, the fixed input set (≥30 rows where possible), seed, and environment.
   Every number in this exercise is that same metric on that same set. If you cannot compute
   it today, stop and build it before continuing.
2. **Enumerate the stages and their interfaces.** List the stages in order. For each, write
   down its exact input and output type — the interface is what makes substitution possible.
   Stages you cannot cleanly cut at are not separate stages; merge them and say so. Record
   the current end-to-end score as the **baseline**.
3. **Define the oracle for each stage.** An oracle is the best-possible output of that stage
   for each eval row. Choose per stage, in preference order:
   - **Ground truth** — the labeled correct intermediate (gold passages, gold plan, gold
     parse, gold labels). Strongest.
   - **Human annotation** — a person produces the ideal intermediate for the eval rows.
     Expensive; keep the set small and record who annotated.
   - **Proxy oracle** — a much stronger/slower/more expensive model, an exhaustive or
     brute-force variant, or the stage run with information it would not have at runtime.
   - **Pairwise best-of** — for stages with no definable "correct" output (style, phrasing,
     a summary), generate several candidates and have a judge pick the best per row; that
     best-of is the oracle.
   Label each oracle **true** or **proxy**. A proxy oracle bounds the *proxy's* quality, not
   perfection: it can understate headroom (proxy is imperfect) or overstate it (proxy leaks
   information). Carry that label through every table and conclusion.
4. **Ablate one stage at a time.** For each stage: run the pipeline end-to-end with ONLY that
   stage's output replaced by its oracle, every other stage untouched and identical to
   baseline. One substitution per run — never two at once, or the result is unattributable.
   Keep the downstream stages exactly as they are; the point is to see what they do when
   handed perfect input.
5. **Compute headroom per stage.** `headroom(S) = score(oracle S) − baseline`. This is the
   **ceiling** that stage can contribute: the most you could ever gain by making S perfect.
   A near-zero headroom is the most valuable result you can get — it proves that stage is
   not worth optimizing, no matter how bad it looks in isolation.
6. **Establish the all-oracle ceiling and the residual.** Run once with EVERY stage oracled.
   That score is the system ceiling given the current architecture; `100% − ceiling` (or
   `perfect − ceiling`) is the **irreducible residual** — loss from the framing, the metric,
   ambiguous inputs, or an architecture no stage-level fix can reach. If the residual is
   large, stop optimizing stages and revisit the design.
7. **Allocate the error budget.** State the denominator explicitly, then express each stage's
   headroom against it. Use the **baseline-to-ceiling gap** (`all-stages ceiling − baseline`);
   it is the loss that is actually reachable. Add the residual row. Example shape:

   | Stage | Oracle type | Score w/ oracle | Headroom | Share of gap (÷0.28) |
   | --- | --- | --- | --- | --- |
   | baseline | — | 0.61 | — | — |
   | 1 retrieve | ground truth | 0.84 | +0.23 | 82% |
   | 2 rerank | proxy (stronger model) | 0.66 | +0.05 | 18% |
   | 3 generate | pairwise best-of (proxy) | 0.69 | +0.08 | 29% |
   | all stages | mixed | 0.89 | +0.28 | gap (denominator) |
   | residual | — | — | 0.11 unreachable | outside the gap |

   **The shares sum to 129%, not 100% — and that is correct.** Overlapping headroom is the
   non-additivity of step 8 showing up in the arithmetic. A budget that sums to a tidy 100%
   has almost always been divided by Σ headroom (here 0.36) instead of the gap, which hides
   exactly the interaction you need to see. Never normalize the shares to make them sum to
   100%: state the denominator, let them overshoot, and explain why.

   **Residual** = the part of the loss no stage substitution reaches (`perfect − ceiling`,
   where "perfect" is the metric's best attainable value from step 1 — 1.0 only if the metric
   is bounded at 1.0; for an unbounded or lower-is-better metric use its own best value).

   **Metric direction.** All the arithmetic above assumes higher-is-better. For a
   lower-is-better metric (error rate, RMSE, p95 latency, cost), headroom is
   `baseline − score(oracle)` and "ceiling" is a floor. Fix the direction in step 1 and apply
   it consistently, or the ranking silently inverts and you optimize the best stage.

8. **Check for interaction before ranking.** Headroom is **not additive**: the sum of the
   single-stage headrooms will rarely equal the all-oracle gap. If `Σ headroom > gap`, the
   stages overlap — several are failing on the same rows, and fixing one moves the ceiling of
   the others. If `Σ headroom < gap`, they compound — a stage only pays off once its upstream
   is fixed (masked headroom: a reranker handed garbage cannot show its value). For the top
   2–3 stages, run the paired ablation (both oracled) to measure the interaction directly,
   and re-read the ranking in that light.
9. **Rank what to optimize.** For each stage combine: headroom (ceiling), attainability (what
   fraction of that ceiling a realistic change could plausibly capture — a proxy oracle that
   is a 50× more expensive model is not shippable), effort, and cost/latency impact. Rank by
   expected realizable gain per unit effort, not by raw headroom. Name explicitly any stage
   you are recommending NOT to touch, and why.
10. **Report, then hand off.** Deliver: the metric and eval set, the stage/interface list, the
    oracle table with true/proxy labels, the headroom table, the residual, the interaction
    finding, and the ranked recommendation. State the ceiling caveat in the report itself
    (step-6 rule). Then hand the top-ranked stage to `measured-optimization-loop` to actually
    optimize it — this skill selects the target; that one moves it.

## Example
**Before:** A RAG assistant scores 0.61 on answer correctness. The team is split between
"buy a better embedding model" and "rewrite the answer prompt"; both are weeks of work and
neither side has evidence.

**After:** Oracle-retrieval (gold passages injected, generator untouched) scores 0.84 →
retrieval headroom +0.23. Oracle-generation (best-of-8 judged, retrieval untouched) scores
0.69 → +0.08. All-oracle 0.89, so residual 0.11 is ambiguous questions and a strict metric.
Σ headroom (0.31) > gap (0.28): overlapping failures. Recommendation: retrieval first, it
caps the system; the prompt rewrite is worth at most +0.08 and less than that until retrieval
improves. The embedding-model spend is now defensible and the prompt rewrite is deferred.

## Rules
- One oracle substitution per run. Two at once (outside the deliberate paired ablation in
  step 8) makes the result unattributable.
- Same metric, same eval set, same seed, same environment for baseline and every ablation.
- Oracle substitution measures a **ceiling, not a forecast**. "Retrieval has +0.23 headroom"
  never means a retrieval project will deliver +0.23; it means it cannot deliver more.
  Say this in the report — it is the single most common misreading of these numbers.
- Headroom is **not additive** across stages. Never sum single-stage headrooms and present
  the total as an achievable gain; report the all-oracle ceiling for that.
- Label every proxy oracle as a proxy, everywhere it appears. An unlabelled proxy number
  gets quoted later as ground truth.
- A proxy oracle that leaks runtime-unavailable information inflates headroom. Check that the
  oracle only knows things a perfect version of that stage could legitimately know.
- Near-zero headroom is a finding, not a failed experiment. Publish it — it saves the effort.
- If the residual dominates the gap, the answer is architecture or metric, not stage tuning.
- Small eval sets make headroom noisy. Report the set size, and treat a headroom inside
  run-to-run variance as zero.
- Method only: no network calls, no CLI installs, no credentials, no auto-run hooks. You
  define the stages, build the oracles, and run the ablations with the project's own tooling.

## In this repo (one instance)
Examples only — the method above is the talent; nothing here is required.

- The factory's own build wave is a pipeline with stages (harvest → dedup/reuse gate →
  author → test → deploy). If wave yield disappoints, the same question applies: oracle the
  **author** stage by hand-writing one talent perfectly and re-running the downstream test
  gate, versus oracling the **harvest** stage by hand-picking known-good candidates. The
  headroom difference says whether to invest in sourcing or in authoring.
- The end-to-end metric can be the `eval-harness` baseline-vs-with pass rate on a talent's
  `evals.md`; the fixed eval set is that file's scenarios.
- Record the headroom table and the ranked recommendation where the run's other measurements
  go (e.g. the wave's `metrics.jsonl` row / `pipeline/ledgers/`) rather than only in a
  session, so a later wave can compare against it. Never write a headroom number that was
  not actually measured.
