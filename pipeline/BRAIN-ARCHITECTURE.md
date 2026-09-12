# The Brain — architecture from proven building blocks

Before building the self-playing piano from scratch, we mined the remaining
catalog (reuse-first) for existing components that already solve each part. The
brain below is assembled from those blocks: **adopt** = taken in as a talent as-is;
**adapt** = pattern borrowed, a generalized version authored during the build (the
source is ECC-coupled); **have** = already in `.claude/skills/`.

## Brain components → source block

| Brain component | What it does | Source block | Mode |
| --- | --- | --- | --- |
| **Pipeline engine** | gated flow: harvest → build/adopt → test → store, 2 commit gates, size-classifier, reuse-first | `orch-pipeline` | adapt |
| **Work-unit schema + merge queue** | unit = {id, depends_on, scope, acceptance, risk, rollback}; coordinator-only integration order | `ralphinho-rfc-pipeline` | adapt |
| **Talent routing** | decompose a job → ordered chain of the right talents (job X → talent Y), dedup + fallback | `plan-orchestrate` | adapt |
| **Talent team composition** | discover talents from files, compose ad-hoc team ≤N, synthesize | `team-builder` / `team-agent-orchestration` | adapt |
| **Loop safety** | decidable stop-conditions, anti-spin damping, Goodhart boundary, human gate ∝ autonomy | `loop-design-check` | **adopt** |
| **Loop recovery** | freeze → audit → reduce scope → replay; named failure modes | `continuous-agent-loop` | adapt |
| **Parallel fan-out isolation** | lane matrix: classify parallel/sequential/gated by write-surface collision before fan-out | `parallel-execution-optimizer` | **adopt** |
| **Generate→Evaluate quality loop** | ruthless evaluator (never fixes) + rubric + threshold + max-iters | `gan-style-harness` | adapt |
| **Dual-review gate** | two independent reviewers, AND-gate, fresh re-review | `santa-method` | have |
| **Two-tier DB ingestion** | Classify → Deduplicate → Store → Index; route each type to its tier (raw intake → curated talents) | `knowledge-ops` | adapt |
| **Memory / handoff + promotion gate** | `ecc.memory.v1` scoped, `trust:unreviewed`, create-only, recall-before-write → raw→tested promotion | `unified-memory` | **adopt** |
| **KB retrieval refinement** | Dispatch → Evaluate → Refine → Loop, relevance-scored, capped | `iterative-retrieval` | adapt |
| **Cold-start / git-persisted state** | self-contained step briefs + git-persisted plan files survive ephemeral containers | `blueprint`, `dynamic-workflow-mode`, `autonomous-agent-harness` | pattern |
| **Self-improvement** | promote proven harness work into a reusable talent; dogfood adopted talents on our own work | `dynamic-workflow-mode` + dogfooding | pattern |
| **Reuse-first gate** | before building, search our own catalog + talents for existing help | `skill-scout` (ours) | have |
| **Security gate** | PreToolUse hook: no third-party code adopted without review; nothing exfiltrates | our hook + `skill-comply` concept | build |

## The flow (assembled)

```
research-scout (terms/sources/entities)  ──feeds──▶  frontier queue (git-persisted)
        │                                                    │
        ▼                                                    ▼
  T4 harvester ── source-type method (pdf/docx/github/web) ──▶ INTAKE (raw, per type)
        │                                        knowledge-ops: classify→dedup→store→index
        ▼
  reuse-first gate (search our catalog) ──▶ talent-worthiness gate (fills a NEW function?)
        │ yes                                          │ no → stays a knowledge note
        ▼
  T1 factory: pipeline engine (orch) ─ route talents (plan-orch) ─ build/adopt
        │
        ▼
  gan/santa Generate→Evaluate + eval-harness + verification ──▶ TALENT LIBRARY (.claude/skills)
        │
   loop-safety (stop/anti-spin) · parallel-isolation · coordinator commits · unified-memory handoff
        │
        └──▶ findings sharpen research-scout's next terms (self-improvement)
```

Every stage uses the talents we've adopted (deep-reading, research-methodology,
skill-scout, eval-harness, santa-method, verification-before-completion,
context-budget, writing-skills, subagent-driven-development, dispatching-parallel-
agents, + the new loop-design-check, parallel-execution-optimizer, unified-memory).
New useful talents are wired into the routing table as they are adopted.
