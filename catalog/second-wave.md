# Second eval wave — reuse-first scan for building the brain

Before building the self-playing piano, we scanned the remaining shortlist for
components that help *build it* (architecture, code, subagent/loop/memory patterns).
17 candidates were pattern-mined; 8 with distinct brain-functions were security-read
and A/B evaluated. **All 8 safe, all fill a distinct function.**

| Skill | Brain function | Security | Verdict |
| --- | --- | --- | --- |
| `loop-design-check` | autonomous-loop safety (stop-conditions, anti-spin, human gate) | safe | **adopt** |
| `parallel-execution-optimizer` | parallel fan-out with write-collision gating | safe | **adopt** |
| `unified-memory` | scoped trust-tagged memory/handoff + raw→tested promotion | safe | **adopt** |
| `orch-pipeline` | gated harvest→build→test→store pipeline engine | safe | adapt |
| `plan-orchestrate` | talent routing (job → talent chain) | safe | adapt |
| `knowledge-ops` | two-tier DB ingestion (classify→dedup→store→index) | safe | adapt |
| `gan-style-harness` | generator→evaluator build loop (evaluator never fixes) | safe | adapt |
| `iterative-retrieval` | relevance-scored KB retrieval refinement loop | safe | adapt |

**adopt (3)** — taken in verbatim as talents (in `.claude/skills/`).
**adapt (5)** — pattern is valuable but ECC-coupled (hardcoded catalogue/command,
Playwright/app-build, 6 stack-specific layers, ECC pseudocode). We borrow the
pattern and author a generalized version during the brain build; recorded in
`pipeline/BRAIN-ARCHITECTURE.md`.

Pattern-mined but not separately evaluated (folded into the architecture as
patterns): `ralphinho-rfc-pipeline` (unit schema + merge queue), `blueprint`
(cold-start briefs), `dynamic-workflow-mode` (checkpoint state + skill-extraction),
`continuous-agent-loop` (recovery), `autonomous-agent-harness` (persistence/heartbeat),
`team-agent-orchestration`/`team-builder` (composition), `claude-devfleet`/`dmux-workflows`
(inspiration; external-tool-dependent).

Not taken: duplicate `orch-*` wrappers (one engine, not every wrapper); GAN
sub-agents and extra review loops (overlap `santa-method`); tmux-manager-dependent
team tools (external software we lack). Nothing taken merely for existing — only
if it fills a function we don't already cover (talent-worthiness gate).
