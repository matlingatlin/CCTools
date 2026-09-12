---
source: ECC (affaan-m/ECC) — targeted deep re-audit of description-only triage
harvested: 2026-08-27
by: piano re-audit (4 parallel reviewers, coordinator-commit)
status: intake (verified — files opened, gates applied on contents)
---

# ECC re-audit — closing the description-only triage gap

**Why:** the Graphify miss (features skipped because judged on the surface) exposed the
same risk in the ECC harvest: **349 of 454 components were triaged from their one-line
description without opening the file.** This audit opened the high-value tiers and judged
on actual contents. Four reviewers ran in parallel; the coordinator committed.

## Coverage check (trust, with evidence)
- **superpowers: complete** — clone has 14 `SKILL.md`; catalog has 14 skills + 1 hook. Nothing skipped.
- **ECC "898 skills" scare: resolved** — 519 were i18n doc mirrors (ja/zh/tr/es/ko),
  93 were other-tool mirrors (.kiro/.agents/.cursor); canonical `skills/` = 286 = catalog's
  287. No canonical components were skipped; the mirror-dedup held.

## Results
| Tier | Sampled/read | Correct as-was | Under-scored (adopt/promote) | Security-flag |
| --- | --- | --- | --- | --- |
| fit=1 (spot-check of 249) | 30 | 29 (97%) | 1 (`mle-reviewer`) | 0 |
| fit=2 (all) | 100 | 87 | 9 | 4 |
| adapt (all) | 27 | — (collapse to 3 builds) | 3 new | several noted |

**fit=1 error rate 3.3% → a full re-read of the 249 is NOT warranted** (diminishing
returns; ~8 core-domain items might be mildly under-scored, none critical).

## 10 validated new talents (deduped across all reviewers)
Each fills a function NOT covered by our 36 talents (reuse-first applied). Priority:
factory-cross-cutting first, then domain techniques.

**Cross-cutting (improve the factory itself):**
1. `prompt-refinement` — diagnose + rewrite underspecified prompts. Safe. (adapt-ranked HIGH)
2. `agent-surface-security-audit` — static audit of CLAUDE.md/settings/MCP/hooks for
   injection, permissive allowlists, supply-chain. **SAFE reimpl** of ECC `security-scan`
   (which drives `npx ecc-agentshield` + auto-`--fix`): Read/Grep only, no external CLI/
   Action, no auto-fix, never prints secret values. (HIGH — serves our own security gate)
3. `cost-aware-model-routing` — pick model tier by task complexity + budget guardrails +
   prompt-cache discipline; supports `COSTS.md`. Merges `cost-aware-llm-pipeline` +
   `model-route`. (MEDIUM)
4. `decision-council` — adversarial multi-voice go/no-go with fresh-subagent anti-anchoring
   (from `council`). `brainstorming` generates ideas; this one decides. (MEDIUM)
5. `agent-blast-radius-guard` — guardrails for autonomous agents (flag destructive commands,
   freeze writes to a directory). **SAFE reimpl** of `safety-guard` (no PreToolUse hook —
   a checklist/consent method). (MEDIUM — matches our autonomy-safety ethos)

**Domain techniques (build on first matching task — dogfood-on-demand):**
6. `behavioral-spec-mining` — reverse-engineer specs/invariants from brownfield code
   (from `spec-miner`; keep the sample-and-expand token strategy, drop OpenSpec format).
7. `measured-optimization-loop` — baseline → one-hypothesis variants → correctness gate →
   promotion gate (from `benchmark-optimization-loop`). Perf work by measurement.
8. `style-inheritance` — extract implicit code conventions and codify them to stop AI
   style-drift on legacy repos (from `inherit-legacy-style`; SAFE ver, no enforcement hook).
9. `hybrid-parse-escalation` — deterministic parse first, confidence-gated escalation to a
   cheap LLM only on edge cases (from `regex-vs-llm-structured-text`).
10. `mlops-production-review` — production-ML review method: data-contract/leakage checks,
    training reproducibility, fail-closed promotion gates, serving/rollback, monitoring
    (from `mle-reviewer`, promoted from fit=1).

Deduped OUT: `intent-driven-development` → overlaps `writing-plans` (library, not built).

## Security — correctly kept OUT (never adopt as-is)
`ecc:hooks`, `ecc:memory-persistence`, `plankton-code-quality`, `repo-scan`, `plan-canvas`
(auto-run hooks / external-code install / loopback server); `council-multi-model` (external
codex + OpenAI send); `deep-research`/`exa-search`/`autonomous-agent-harness`/`delivery-gate`/
`strategic-compact` (paid MCPs + API keys / auto-run hooks — the previously-gated family).
Where the *idea* is worth it (config-guard, blast-radius), we build a SAFE reimplementation
— never the auto-run/external-install source.

## Verdict
The description-only triage was ~97% sound on fit=1 and mostly sound on fit=2 (87/100), but
it DID miss 10 real cross-project talents — confirming the concern that surfaced from
Graphify. Those 10 are now validated (files read, gates applied) and queued to build;
security items are rejected with reasons. Catalog decisions updated; `catalog.json.reaudit`
records the run.
