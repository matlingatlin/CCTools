# Build-now Shortlist (fit = 3)

111 components that are the factory's own infrastructure — the ones to security-read and full-evaluate now (Phase C→D). The other 358 stay in the domain library and are evaluated on demand when a matching project starts.

Ordered by domain, superpowers-origin marked. Evaluation = baseline-vs-component on a scenario matched to the component type (application vs pressure).

## Meta — skill / command / hook authoring (32)

| Name | Type | Repo | Flags | Note |
| --- | --- | --- | --- | --- |
| `continuous-learning-v2` | skill | ecc | exec,network,secret-ref | Instinct-based learning evolving into skills; self-improving core |
| `conversation-analyzer` | agent | ecc | secret-ref | Mines transcripts for hookable behaviors; meta hook authoring |
| `delivery-gate` | skill | ecc | — | Stop hook enforcing quality gates; meta hook authoring |
| `dynamic-workflow-mode` | skill | ecc | exec,secret-ref | Task-local harnesses, eval gates, skill extraction; strong meta |
| `ecc-guide` | command | ecc | — | Navigates the repo's own agent/skill/command surface |
| `evolve` | command | ecc | — | Analyzes instincts and generates evolved structures |
| `gateguard` | skill | ecc | exec | Fact-forcing gate hook blocking edits; strong meta hook |
| `harness-audit` | command | ecc | exec | Audits the repo harness, prioritized scorecard |
| `hookify` | command | ecc | — | Creates hooks from conversation analysis |
| `hookify-configure` | command | ecc | — | Enables or disables hookify rules |
| `hookify-help` | command | ecc | — | Help for the hookify hook system |
| `hookify-list` | command | ecc | — | Lists configured hookify rules |
| `hookify-rules` | skill | ecc | exec,secret-ref | Create/configure hookify rules; core hook authoring |
| `instinct-export` | command | ecc | — | Exports learned instincts to file |
| `instinct-import` | command | ecc | — | Imports instincts from file or URL |
| `instinct-status` | command | ecc | — | Shows learned instincts with confidence |
| `learn` | command | ecc | secret-ref | Extracts session patterns into candidate skills |
| `learn-eval` | command | ecc | exec,secret-ref | Extracts, self-evaluates, saves skills |
| `project-init` | command | ecc | — | Detects stack, produces ECC onboarding plan |
| `projects` | command | ecc | — | Lists projects and instinct statistics |
| `promote` | command | ecc | — | Promotes project instincts to global scope |
| `prompt-optimizer` | skill | ecc | exec,secret-ref | Analyze prompts, match components, output optimized prompt; meta core |
| `prune` | command | ecc | — | Deletes stale unpromoted instincts |
| `rules-distill` | skill | ecc | exec | Distill cross-skill principles into rule files; meta core |
| `skill-comply` | skill | ecc | exec | Tests whether skills/agents are actually followed; meta core |
| `skill-create` | command | ecc | secret-ref | Generates SKILL.md from git history; core meta capability |
| `skill-health` | command | ecc | — | Skill portfolio health dashboard; directly serves skill factory |
| `skill-scout` | skill | ecc | — | Search existing skill sources before creating; meta core |
| `skill-stocktake` | skill | ecc | exec | Audit skills/commands for quality; meta core |
| `using-superpowers` | skill | superpowers | — | How to find and invoke skills; meta core |
| `workspace-surface-audit` | skill | ecc | secret-ref | Audit repo/MCP/plugins, recommend skills/hooks/agents; meta core |
| `writing-skills` | skill | superpowers | exec,network | Create, edit, verify skills; meta core |

## Agents & orchestration (47)

| Name | Type | Repo | Flags | Note |
| --- | --- | --- | --- | --- |
| `agent-architecture-audit` | skill | ecc | — | Full-stack agent stack diagnostic; core agent domain |
| `agent-harness-construction` | skill | ecc | — | Design agent tool sets and action spaces; core |
| `agent-introspection-debugging` | skill | ecc | — | Structured agent failure debugging; core agent domain |
| `agentic-os` | skill | ecc | secret-ref | Build persistent multi-agent systems; core orchestration |
| `autonomous-agent-harness` | skill | ecc | network,secret-ref | Autonomous agent system with memory/scheduling; core |
| `blueprint` | skill | ecc | — | Construction plans for multi-agent projects; orchestration |
| `claude-devfleet` | skill | ecc | network | Orchestrate parallel agents in worktrees; core orchestration |
| `continuous-agent-loop` | skill | ecc | exec | Autonomous agent loops with eval gates; core |
| `dispatching-parallel-agents` | skill | superpowers | — | Dispatch independent parallel agent tasks; core domain |
| `dmux-workflows` | skill | ecc | — | Multi-agent parallel orchestration via dmux; core domain |
| `enterprise-agent-ops` | skill | ecc | secret-ref | Long-lived agent observability/lifecycle; core domain |
| `gan-build` | command | ecc | — | Generator/evaluator build loop with scoring |
| `gan-design` | command | ecc | exec | Generator/evaluator design loop with scoring |
| `gan-generator` | agent | ecc | network,secret-ref | Generator in iterative generate-evaluate loop; orchestration |
| `gan-style-harness` | skill | ecc | network | Generator-Evaluator autonomous agent harness; core domain |
| `harness-optimizer` | agent | ecc | secret-ref | Improves agent harness reliability/cost/throughput; orchestration meta |
| `loop-design-check` | skill | ecc | — | Design/review agent loops against failure modes; core orchestration |
| `loop-operator` | agent | ecc | exec,secret-ref | Operates autonomous agent loops, intervenes on stalls; orchestration |
| `loop-start` | command | ecc | — | Starts managed autonomous loop with stops |
| `loop-status` | command | ecc | — | Inspects active loop state and failures |
| `mcp-server-patterns` | skill | ecc | network | Building MCP servers/tools; core agents domain |
| `model-route` | command | ecc | — | Routes tasks to best model tier |
| `multi-backend` | command | ecc | — | Backend multi-model orchestration workflow |
| `multi-execute` | command | ecc | exec | Multi-model execution, Claude sole writer |
| `multi-frontend` | command | ecc | — | Frontend multi-model orchestration workflow |
| `multi-plan` | command | ecc | exec | Creates multi-model implementation plan |
| `multi-workflow` | command | ecc | exec | Full multi-model development workflow |
| `orch-add-feature` | command | ecc | — | Orchestrates end-to-end feature build |
| `orch-add-feature` | skill | ecc | — | Orchestrate feature build via agent chain; core orchestration |
| `orch-build-mvp` | command | ecc | — | Orchestrates MVP bootstrap from spec |
| `orch-change-feature` | command | ecc | — | Orchestrates altering existing feature |
| `orch-change-feature` | skill | ecc | — | Orchestrate feature change via agent pipeline; core orchestration |
| `orch-fix-defect` | command | ecc | — | Orchestrates bug fix via regression test |
| `orch-fix-defect` | skill | ecc | — | Orchestrate bug fix via agent pipeline; core orchestration |
| `orch-pipeline` | skill | ecc | secret-ref | Shared gated orchestration engine; core orchestration infrastructure |
| `orch-refine-code` | command | ecc | — | Orchestrates behavior-preserving refactor |
| `orch-refine-code` | skill | ecc | — | Orchestrate refactor via agent pipeline; core orchestration |
| `orch-review` | command | ecc | — | Orchestrated review workflow over a diff |
| `parallel-execution-optimizer` | skill | ecc | — | Concurrent agents, worktrees, verification lanes; core orchestration |
| `plan-orchestrate` | skill | ecc | secret-ref | Decompose plan into agent chains; core orchestration |
| `rag-pipeline-reviewer` | agent | ecc | exec,secret-ref | Reviews RAG retrieval/chunking/eval; core knowledge-base relevance |
| `ralphinho-rfc-pipeline` | skill | ecc | — | RFC-driven multi-agent DAG with quality gates; core orchestration |
| `santa-loop` | command | ecc | secret-ref | Adversarial dual-review convergence loop |
| `security-scan` | command | ecc | secret-ref | Scans agent/hook/MCP/secret surfaces |
| `subagent-driven-development` | skill | superpowers | exec,secret-ref | Execute plans via subagents in-session; core domain |
| `team-agent-orchestration` | skill | ecc | exec | Agent squad orchestration with Kanban and merge gates; core |
| `team-builder` | skill | ecc | — | Interactive picker for parallel agent teams; core |

## Testing & evaluation (14)

| Name | Type | Repo | Flags | Note |
| --- | --- | --- | --- | --- |
| `agent-eval` | skill | ecc | exec | Head-to-head coding agent comparison with metrics; eval |
| `agent-evaluator` | agent | ecc | network | Scores agent output on quality rubric; core eval domain |
| `agent-self-evaluation` | skill | ecc | network | Agent self-rates output on scorecard; eval domain |
| `ai-regression-testing` | skill | ecc | network | Regression testing for AI-assisted dev; testing domain |
| `eval-harness` | skill | ecc | exec,secret-ref | Formal eval-driven development framework; core high-value |
| `gan-evaluator` | agent | ecc | network,secret-ref | Evaluator agent scoring apps against rubric; eval loop |
| `pr-test-analyzer` | agent | ecc | secret-ref | Reviews PR test coverage quality; testing domain |
| `santa-method` | skill | ecc | exec,secret-ref | Multi-agent adversarial verification convergence loop; strong eval |
| `tdd-guide` | agent | ecc | secret-ref | Enforces test-first TDD methodology; core testing domain |
| `tdd-workflow` | skill | ecc | network,secret-ref | General TDD with unit/integration/E2E coverage; core, reusable |
| `test-coverage` | command | ecc | — | Coverage analysis and test generation; high-value testing domain |
| `test-driven-development` | skill | superpowers | — | General TDD before implementation; core, reusable |
| `verification-before-completion` | skill | superpowers | — | Require evidence before claiming completion; core, reusable |
| `verification-loop` | skill | ecc | secret-ref | General session-work verification before completion; core, reusable |

## Research & web (6)

| Name | Type | Repo | Flags | Note |
| --- | --- | --- | --- | --- |
| `deep-research` | skill | ecc | — | Multi-source cited web research; core high-value domain |
| `exa-search` | skill | ecc | network,secret-ref | Neural web/code/company search via Exa; core domain |
| `literature-review` | skill | ecc | — | Systematic literature review/synthesis; core research domain |
| `market-research` | skill | ecc | — | Market/competitive research with attribution; core research domain |
| `research-ops` | skill | ecc | — | Evidence-first current-state research workflow; core domain |
| `search-first` | skill | ecc | exec | Research-before-coding, invokes researcher agent; core domain |

## Context & token management (12)

| Name | Type | Repo | Flags | Note |
| --- | --- | --- | --- | --- |
| `aside` | command | ecc | — | Answers side question without losing task context; context management |
| `ck` | skill | ecc | — | Persistent per-project memory and context loading; core |
| `context-budget` | skill | ecc | — | Audits context window consumption; core token management |
| `iterative-retrieval` | skill | ecc | exec,network | Progressive context refinement for subagents; core context domain |
| `knowledge-ops` | skill | ecc | exec,secret-ref | Knowledge base ingest/sync/retrieval across stores; core project domain |
| `resume-session` | command | ecc | secret-ref | Resumes prior session with full context |
| `save-session` | command | ecc | secret-ref | Saves session state for later resume |
| `sessions` | command | ecc | — | Manages session history and metadata |
| `strategic-compact` | skill | ecc | network | Manual context compaction at logical intervals; core domain |
| `token-budget-advisor` | skill | ecc | — | Response depth/token budget control; core domain |
| `unified-memory` | skill | ecc | secret-ref | Durable shared context/handoffs across agents; core domain |
| `update-codemaps` | command | ecc | — | Token-lean architecture codemaps; context management |
