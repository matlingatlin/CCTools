---
name: mlops-production-review
description: "Use when reviewing production machine-learning code before it ships or promotes — training pipelines, feature engineering, model serving/inference endpoints, batch scoring jobs, or a model-promotion PR. Applies an MLOps review method: hunt train/serve skew and data leakage, check data contracts and label integrity, verify training reproducibility (seeds, pinned data/deps, versioned artifacts), demand fail-closed promotion gates (eval thresholds, no silent fallback), and confirm serving rollback and drift/monitoring hooks. Triggers on model.fit/predict, feature stores, checkpoints, sklearn/xgboost/torch training loops, model registries, inference handlers, \"deploy the model\", \"promote to prod\", \"eval gate\", \"train-serve\", \"data leakage\", \"model rollback\". NOT for generic app code review (use code-review), test authoring (use test-coverage/test-driven-development), or LLM/agent eval design (use eval-harness/learn-eval) — this is classical/deep-learning ML in production. NOT for reviewing a RETRIEVAL path itself (chunking, embeddings, rerank, top-k, grounding) — that is rag-pipeline-reviewer, an agent in .claude/agents/."
---
# MLOps Production Review

Review production ML code the way outages actually happen: bad data, leaked labels, unreproducible training, silent promotions, and un-rollback-able serving. Method only — you read and reason; you do not run training, deploy, or call networks.

## When to use
- A PR that trains, evaluates, promotes, or serves a model reaches production.
- Someone asks "is this model code safe to ship / promote / deploy?"
- You are auditing an existing pipeline for skew, leakage, or missing gates.

**When NOT:** generic backend/app code (code-review), writing tests (test-coverage, test-driven-development), or LLM/agent/prompt eval design (eval-harness, learn-eval). This covers classical and deep-learning models in production, not chat/agent behavior.

## Steps
1. **Map the pipeline.** Identify each stage — data source -> features -> train -> eval -> registry/promote -> serve -> monitor — and note which stages the diff touches. Review only real, reachable code.
2. **Data contract & label integrity.** Check inputs have a validated schema/types/ranges; nulls and out-of-range handled explicitly; labels defined once and not derived differently in train vs serve; no PII leaking into features.
3. **Leakage hunt.** Look for target-derived features, future/look-ahead data, fit-before-split (scalers/encoders/imputers fit on full data), group/time leakage across split boundaries, and duplicate rows spanning train/test.
4. **Train/serve skew.** Confirm the same feature transforms run at train and serve time (shared code or a feature store), same defaults, same category encodings, same units/ordering.
5. **Reproducibility.** Require pinned/versioned training data, pinned deps, a fixed seed, and versioned output artifacts (model + preprocessing + metadata). Flag anything that makes a run non-reproducible.
6. **Promotion gate (fail-closed).** The gate must block on eval thresholds against a held-out or time-based set, compare to the current prod model, and error/stop on missing metrics — never promote on exception, empty eval, or silent fallback.
7. **Serving & rollback safety.** Check input validation at the endpoint, versioned model loading, a defined rollback/previous-version path, timeouts/resource bounds, and safe behavior on load failure (fail closed, not serve-garbage).
8. **Monitoring.** Confirm prediction/input logging, drift and performance signals, and alert hooks exist for the promoted model.
9. **Report.** List findings ordered by blast radius: silent-wrong-prediction and leakage first, then reproducibility and gates, then monitoring gaps. Give each a concrete failure scenario and the smallest fix.

## Rules
- Silent wrong predictions outrank crashes — a model that serves confidently wrong output is worse than one that errors.
- Leakage is a blocker, not a nit: inflated offline metrics hide it until production.
- A promotion gate that can be skipped, defaulted, or excepted past is no gate — treat fail-open as a blocking finding.
- No transform may exist only on the training path; train/serve parity is mandatory.
- Every promoted model needs a rollback path before it needs praise.
- Method only: never run training/deploy, never call external networks or CLIs, never add auto-run hooks. Read, reason, report.
- Reproducibility means another engineer reruns and gets the same artifact — unpinned data, deps, or seed fails this.
