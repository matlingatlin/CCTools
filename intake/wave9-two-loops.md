---
source: two concurrent factory loops (practitioner/framework repos)
harvested: 2026-08-27
by: factory ×2 (parallel harvest loops, coordinator-merged)
status: intake (verified — gates applied on contents)
---

# Wave 9 intake — two concurrent factory loops

First run of TWO factory loops at once, splitting the queue 3+3 (both produced data;
coordinator merged + committed — single-writer preserved). Practitioner/framework repos,
per the LESSONS pivot away from lists.

## Sources harvested
- **Loop A:** stanfordnlp/dspy, dottxt-ai/outlines, simonw/llm
- **Loop B:** pydantic/pydantic-ai, hamelsmu (profile), outlines-dev/outlines (dup of outlines → 0)

## Talent-worthiness verdict: practitioner repos yield real methods
Unlike vendor/reference repos (0 talents), practitioner/framework repos yielded **10
candidate methods**, 7 of which pass the gate (a general method we lack). Frameworks
themselves (dspy, outlines, pydantic-ai) are libraries → not adopted; their *methods* are.

### BUILD (7 — validated, queued)
- **llm-judge-calibration** (hamelsmu) — build an LLM-as-judge for a subjective dimension, then validate it against a small human-labeled set (agreement/TPR/TNR) before trusting it.
- **error-analysis-taxonomy** (hamelsmu) — open/axial-code a batch of AI traces into a frequency-ranked failure taxonomy → an actionable improvement backlog.
- **synthetic-eval-data-generation** (hamelsmu) — generate diverse test inputs via dimension grids (feature × scenario) to stress-test a feature before real traffic.
- **llm-call-ledger** (simonw/llm) — log every model call (prompt/response/model/params/tokens/cost/ts) to a queryable ledger for replay + `COSTS.md` metering.
- **external-domain-audit** (pydantic-ai) — build a KB from an API/protocol's external docs + design the ideal test suite BEFORE reading the impl, then gap-compare (distinct from diff-based code-review).
- **integration-contract-completeness** (pydantic-ai) — check a narrow patch covers the full contract (roundtrip, streaming/non-streaming, sync/async, all variants, tests, docs) or justify staying narrow.
- **metric-driven-prompt-optimization** (dspy) — optimize a prompt/instruction against a labeled eval set via propose-evaluate-select (distinct from skill-description-optimizer/prompt-refinement).

### DEFER (3 — borderline / lower priority)
- concise-schema-extract (simonw) — terse schema DSL → JSON schema; overlaps general structured-output.
- content-addressed-fragments (simonw) — SHA256 prompt fragments for dedup/cache; overlaps cost-aware-model-routing caching.
- record-replay-http-testing (pydantic-ai) — VCR/cassette for deterministic LLM tests; tooling-specific.

## Security notes (kept OUT / flagged)
- hamelsmu's `evals-skills` installs via `npx skills add …` (external installer, arbitrary
  code) → we build the METHODS ourselves, never install the pack.
- simonw/llm plugins (`llm install`) = pip of arbitrary code; fragments fetch arbitrary URLs
  (SSRF). pydantic-ai ships `.github` agentic CI + a pre-commit that fetches external hooks.
  None auto-run from a clone; we take methods, not their auto-run/installer machinery.

## Concurrency finding (two loops vs one)
Both 3-agent loops finished in ~106–113 s **together**. At the measured cap W=2 (4 cores),
one 6-agent loop would also take ~120 s. So the two loops **shared the ~2 concurrency slots
— running two did NOT increase throughput** on this box; the cap is effectively global, not
per-loop. Two loops buy organization (separate concerns), not speed. The real throughput
lever stays: **more CPU cores** (W = min(16, cores−2)). Prefer ONE loop with more items
(and more cores) over N loops for raw speed.
