# Component Catalog

Generated 2026-08-27 · **469 components** from `obra/superpowers` + `affaan-m/ECC`, triaged into domains with a `fit` score. Machine-readable: [catalog.json](catalog.json). Schema, security flags, and the cross-project library philosophy: [README.md](README.md).

**`fit` = immediacy for building the factory now, not worth.** 3 = factory infrastructure (build now); 2 = broadly reusable; 1 = domain/vertical library (kept, pulled on demand). Nothing is rejected for being niche.

## Domain × fit

| Domain | total | fit3 | fit2 | fit1 |
| --- | --- | --- | --- | --- |
| Meta — skill / command / hook authoring | 44 | 32 | 12 | 0 |
| Agents & orchestration | 63 | 47 | 14 | 2 |
| Testing & evaluation | 41 | 14 | 7 | 20 |
| Research & web | 13 | 6 | 5 | 2 |
| Context & token management | 17 | 12 | 5 | 0 |
| Coding practices (general engineering) | 65 | 0 | 57 | 8 |
| Language / framework specific | 94 | 0 | 0 | 94 |
| DevOps & infrastructure | 28 | 0 | 4 | 24 |
| Data & ML | 16 | 0 | 0 | 16 |
| Design & UX | 20 | 0 | 0 | 20 |
| Writing & content | 12 | 0 | 1 | 11 |
| Product & strategy | 8 | 0 | 4 | 4 |
| Domain verticals (finance, health, logistics, …) | 47 | 0 | 0 | 47 |
| Other | 1 | 0 | 0 | 1 |

## Meta — skill / command / hook authoring (44)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `continuous-learning-v2` | skill | ecc | 3 | exec,network,secret-ref | Instinct-based learning evolving into skills; self-improving core |
| `conversation-analyzer` | agent | ecc | 3 | secret-ref | Mines transcripts for hookable behaviors; meta hook authoring |
| `delivery-gate` | skill | ecc | 3 | — | Stop hook enforcing quality gates; meta hook authoring |
| `dynamic-workflow-mode` | skill | ecc | 3 | exec,secret-ref | Task-local harnesses, eval gates, skill extraction; strong meta |
| `ecc-guide` | command | ecc | 3 | — | Navigates the repo's own agent/skill/command surface |
| `evolve` | command | ecc | 3 | — | Analyzes instincts and generates evolved structures |
| `gateguard` | skill | ecc | 3 | exec | Fact-forcing gate hook blocking edits; strong meta hook |
| `harness-audit` | command | ecc | 3 | exec | Audits the repo harness, prioritized scorecard |
| `hookify` | command | ecc | 3 | — | Creates hooks from conversation analysis |
| `hookify-configure` | command | ecc | 3 | — | Enables or disables hookify rules |
| `hookify-help` | command | ecc | 3 | — | Help for the hookify hook system |
| `hookify-list` | command | ecc | 3 | — | Lists configured hookify rules |
| `hookify-rules` | skill | ecc | 3 | exec,secret-ref | Create/configure hookify rules; core hook authoring |
| `instinct-export` | command | ecc | 3 | — | Exports learned instincts to file |
| `instinct-import` | command | ecc | 3 | — | Imports instincts from file or URL |
| `instinct-status` | command | ecc | 3 | — | Shows learned instincts with confidence |
| `learn` | command | ecc | 3 | secret-ref | Extracts session patterns into candidate skills |
| `learn-eval` | command | ecc | 3 | exec,secret-ref | Extracts, self-evaluates, saves skills |
| `project-init` | command | ecc | 3 | — | Detects stack, produces ECC onboarding plan |
| `projects` | command | ecc | 3 | — | Lists projects and instinct statistics |
| `promote` | command | ecc | 3 | — | Promotes project instincts to global scope |
| `prompt-optimizer` | skill | ecc | 3 | exec,secret-ref | Analyze prompts, match components, output optimized prompt; meta core |
| `prune` | command | ecc | 3 | — | Deletes stale unpromoted instincts |
| `rules-distill` | skill | ecc | 3 | exec | Distill cross-skill principles into rule files; meta core |
| `skill-comply` | skill | ecc | 3 | exec | Tests whether skills/agents are actually followed; meta core |
| `skill-create` | command | ecc | 3 | secret-ref | Generates SKILL.md from git history; core meta capability |
| `skill-health` | command | ecc | 3 | — | Skill portfolio health dashboard; directly serves skill factory |
| `skill-scout` | skill | ecc | 3 | — | Search existing skill sources before creating; meta core |
| `skill-stocktake` | skill | ecc | 3 | exec | Audit skills/commands for quality; meta core |
| `using-superpowers` | skill | superpowers | 3 | — | How to find and invoke skills; meta core |
| `workspace-surface-audit` | skill | ecc | 3 | secret-ref | Audit repo/MCP/plugins, recommend skills/hooks/agents; meta core |
| `writing-skills` | skill | superpowers | 3 | exec,network | Create, edit, verify skills; meta core |
| `add-language-rules` | command | ecc | 2 | — | Scaffolds language rule configs; meta authoring, minor |
| `agent-sort` | skill | ecc | 2 | — | Sorts skills/hooks into install buckets; ECC-specific meta |
| `config-gc` | skill | ecc | 2 | — | Garbage-collects Claude config/skills/hooks; meta cleanup |
| `configure-ecc` | skill | ecc | 2 | — | ECC install/reconfigure guide; meta but tool-specific |
| `continuous-learning` | skill | ecc | 2 | network | Deprecated v1 skill extractor; superseded by v2 |
| `ecc-guide` | skill | ecc | 2 | — | Guides ECC skills/commands/hooks surface; meta but repo-specific |
| `ecc-recipes` | skill | ecc | 2 | — | Maps workflows to command-groups; meta but ECC-specific |
| `ecc:hooks` | hook | ecc | 2 | exec,network,secret-ref | Hook config bundle; meta but opaque |
| `hermes-imports` | skill | ecc | 2 | secret-ref | Convert workflows into sanitized ECC skills; meta but niche |
| `plankton-code-quality` | skill | ecc | 2 | exec | Write-time linting/fix via edit hooks; hook authoring adjacent |
| `security-scan` | skill | ecc | 2 | network,secret-ref | Scans .claude config for vulnerabilities; meta-adjacent security |
| `superpowers:hooks` | hook | superpowers | 2 | — | Hook config bundle; meta but opaque |

## Agents & orchestration (63)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `agent-architecture-audit` | skill | ecc | 3 | — | Full-stack agent stack diagnostic; core agent domain |
| `agent-harness-construction` | skill | ecc | 3 | — | Design agent tool sets and action spaces; core |
| `agent-introspection-debugging` | skill | ecc | 3 | — | Structured agent failure debugging; core agent domain |
| `agentic-os` | skill | ecc | 3 | secret-ref | Build persistent multi-agent systems; core orchestration |
| `autonomous-agent-harness` | skill | ecc | 3 | network,secret-ref | Autonomous agent system with memory/scheduling; core |
| `blueprint` | skill | ecc | 3 | — | Construction plans for multi-agent projects; orchestration |
| `claude-devfleet` | skill | ecc | 3 | network | Orchestrate parallel agents in worktrees; core orchestration |
| `continuous-agent-loop` | skill | ecc | 3 | exec | Autonomous agent loops with eval gates; core |
| `dispatching-parallel-agents` | skill | superpowers | 3 | — | Dispatch independent parallel agent tasks; core domain |
| `dmux-workflows` | skill | ecc | 3 | — | Multi-agent parallel orchestration via dmux; core domain |
| `enterprise-agent-ops` | skill | ecc | 3 | secret-ref | Long-lived agent observability/lifecycle; core domain |
| `gan-build` | command | ecc | 3 | — | Generator/evaluator build loop with scoring |
| `gan-design` | command | ecc | 3 | exec | Generator/evaluator design loop with scoring |
| `gan-generator` | agent | ecc | 3 | network,secret-ref | Generator in iterative generate-evaluate loop; orchestration |
| `gan-style-harness` | skill | ecc | 3 | network | Generator-Evaluator autonomous agent harness; core domain |
| `harness-optimizer` | agent | ecc | 3 | secret-ref | Improves agent harness reliability/cost/throughput; orchestration meta |
| `loop-design-check` | skill | ecc | 3 | — | Design/review agent loops against failure modes; core orchestration |
| `loop-operator` | agent | ecc | 3 | exec,secret-ref | Operates autonomous agent loops, intervenes on stalls; orchestration |
| `loop-start` | command | ecc | 3 | — | Starts managed autonomous loop with stops |
| `loop-status` | command | ecc | 3 | — | Inspects active loop state and failures |
| `mcp-server-patterns` | skill | ecc | 3 | network | Building MCP servers/tools; core agents domain |
| `model-route` | command | ecc | 3 | — | Routes tasks to best model tier |
| `multi-backend` | command | ecc | 3 | — | Backend multi-model orchestration workflow |
| `multi-execute` | command | ecc | 3 | exec | Multi-model execution, Claude sole writer |
| `multi-frontend` | command | ecc | 3 | — | Frontend multi-model orchestration workflow |
| `multi-plan` | command | ecc | 3 | exec | Creates multi-model implementation plan |
| `multi-workflow` | command | ecc | 3 | exec | Full multi-model development workflow |
| `orch-add-feature` | command | ecc | 3 | — | Orchestrates end-to-end feature build |
| `orch-add-feature` | skill | ecc | 3 | — | Orchestrate feature build via agent chain; core orchestration |
| `orch-build-mvp` | command | ecc | 3 | — | Orchestrates MVP bootstrap from spec |
| `orch-change-feature` | command | ecc | 3 | — | Orchestrates altering existing feature |
| `orch-change-feature` | skill | ecc | 3 | — | Orchestrate feature change via agent pipeline; core orchestration |
| `orch-fix-defect` | command | ecc | 3 | — | Orchestrates bug fix via regression test |
| `orch-fix-defect` | skill | ecc | 3 | — | Orchestrate bug fix via agent pipeline; core orchestration |
| `orch-pipeline` | skill | ecc | 3 | secret-ref | Shared gated orchestration engine; core orchestration infrastructure |
| `orch-refine-code` | command | ecc | 3 | — | Orchestrates behavior-preserving refactor |
| `orch-refine-code` | skill | ecc | 3 | — | Orchestrate refactor via agent pipeline; core orchestration |
| `orch-review` | command | ecc | 3 | — | Orchestrated review workflow over a diff |
| `parallel-execution-optimizer` | skill | ecc | 3 | — | Concurrent agents, worktrees, verification lanes; core orchestration |
| `plan-orchestrate` | skill | ecc | 3 | secret-ref | Decompose plan into agent chains; core orchestration |
| `rag-pipeline-reviewer` | agent | ecc | 3 | exec,secret-ref | Reviews RAG retrieval/chunking/eval; core knowledge-base relevance |
| `ralphinho-rfc-pipeline` | skill | ecc | 3 | — | RFC-driven multi-agent DAG with quality gates; core orchestration |
| `santa-loop` | command | ecc | 3 | secret-ref | Adversarial dual-review convergence loop |
| `security-scan` | command | ecc | 3 | secret-ref | Scans agent/hook/MCP/secret surfaces |
| `subagent-driven-development` | skill | superpowers | 3 | exec,secret-ref | Execute plans via subagents in-session; core domain |
| `team-agent-orchestration` | skill | ecc | 3 | exec | Agent squad orchestration with Kanban and merge gates; core |
| `team-builder` | skill | ecc | 3 | — | Interactive picker for parallel agent teams; core |
| `agentic-engineering` | skill | ecc | 2 | exec | Eval-first agentic engineering operating model; broadly useful |
| `autonomous-loops` | skill | ecc | 2 | — | Deprecated autonomous loop patterns; superseded |
| `cost-aware-llm-pipeline` | skill | ecc | 2 | — | LLM cost routing and budget tracking; useful secondary |
| `council` | skill | ecc | 2 | — | Four-voice council for ambiguous decisions; multi-perspective |
| `council-multi-model` | skill | ecc | 2 | exec,secret-ref | External model critique of council decision; multi-model |
| `dev-team` | skill | ecc | 2 | secret-ref | Multi-persona role simulation; useful but secondary |
| `executing-plans` | skill | superpowers | 2 | — | Execute written plan with review checkpoints; useful |
| `gan-planner` | agent | ecc | 2 | secret-ref | Expands prompt into spec for GAN harness; orchestration |
| `opensource-pipeline` | skill | ecc | 2 | secret-ref | Multi-agent fork/sanitize/package pipeline; orchestration but niche use |
| `orch-build-mvp` | skill | ecc | 2 | — | Orchestrate MVP bootstrap from spec; orchestration, somewhat specific |
| `plan-canvas` | skill | ecc | 2 | — | Browser canvas for plan review/approval; agent workflow aid |
| `planner` | agent | ecc | 2 | secret-ref | Planning specialist for complex features; broadly useful |
| `recursive-decision-ledger` | skill | ecc | 2 | — | Recursive reasoning with evidence trail; useful secondary |
| `safety-guard` | skill | ecc | 2 | exec | Prevents destructive ops during autonomous agent runs; useful |
| `nanoclaw-repl` | skill | ecc | 1 | — | Operate specific NanoClaw REPL; niche tool-specific |
| `nasiko-control-plane` | skill | ecc | 1 | secret-ref | Specific Nasiko control plane; niche tool-specific |

## Testing & evaluation (41)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `agent-eval` | skill | ecc | 3 | exec | Head-to-head coding agent comparison with metrics; eval |
| `agent-evaluator` | agent | ecc | 3 | network | Scores agent output on quality rubric; core eval domain |
| `agent-self-evaluation` | skill | ecc | 3 | network | Agent self-rates output on scorecard; eval domain |
| `ai-regression-testing` | skill | ecc | 3 | network | Regression testing for AI-assisted dev; testing domain |
| `eval-harness` | skill | ecc | 3 | exec,secret-ref | Formal eval-driven development framework; core high-value |
| `gan-evaluator` | agent | ecc | 3 | network,secret-ref | Evaluator agent scoring apps against rubric; eval loop |
| `pr-test-analyzer` | agent | ecc | 3 | secret-ref | Reviews PR test coverage quality; testing domain |
| `santa-method` | skill | ecc | 3 | exec,secret-ref | Multi-agent adversarial verification convergence loop; strong eval |
| `tdd-guide` | agent | ecc | 3 | secret-ref | Enforces test-first TDD methodology; core testing domain |
| `tdd-workflow` | skill | ecc | 3 | network,secret-ref | General TDD with unit/integration/E2E coverage; core, reusable |
| `test-coverage` | command | ecc | 3 | — | Coverage analysis and test generation; high-value testing domain |
| `test-driven-development` | skill | superpowers | 3 | — | General TDD before implementation; core, reusable |
| `verification-before-completion` | skill | superpowers | 3 | — | Require evidence before claiming completion; core, reusable |
| `verification-loop` | skill | ecc | 3 | secret-ref | General session-work verification before completion; core, reusable |
| `benchmark` | skill | ecc | 2 | — | Performance baselines and regression detection; useful |
| `benchmark-optimization-loop` | skill | ecc | 2 | — | Recursive optimization by measured tests; useful |
| `browser-qa` | skill | ecc | 2 | — | Browser automation visual/UI testing; useful secondary |
| `e2e-runner` | agent | ecc | 2 | network,secret-ref | E2E test runner via Playwright; testing but web-app niche |
| `e2e-testing` | skill | ecc | 2 | network | Playwright E2E patterns; useful but web-UI specific |
| `python-testing` | skill | ecc | 2 | network,secret-ref | pytest TDD/fixtures/coverage; testing domain, common language |
| `scholar-evaluation` | skill | ecc | 2 | — | Scholarly-work evaluation; useful but academic-leaning |
| `click-path-audit` | skill | ecc | 1 | — | Trace UI button state sequences for bugs; UI-specific |
| `cpp-testing` | skill | ecc | 1 | — | C++ GoogleTest/CTest testing; language-specific |
| `csharp-testing` | skill | ecc | 1 | — | C#/.NET xUnit testing patterns; language-specific |
| `django-tdd` | skill | ecc | 1 | secret-ref | Django pytest TDD; testing but framework-bound |
| `django-verification` | skill | ecc | 1 | network,secret-ref | Django verification loop; framework-bound testing |
| `fsharp-testing` | skill | ecc | 1 | — | F# xUnit/FsCheck testing; language-bound testing |
| `golang-testing` | skill | ecc | 1 | — | Go table-driven/fuzz testing; language-bound |
| `healthcare-eval-harness` | skill | ecc | 1 | exec | Patient safety eval harness; healthcare-specific |
| `kotlin-testing` | skill | ecc | 1 | secret-ref | Kotlin-specific testing; testing domain but narrow language |
| `laravel-tdd` | skill | ecc | 1 | network,secret-ref | Laravel testing; narrow framework, low relevance |
| `laravel-verification` | skill | ecc | 1 | — | Laravel verification loop; narrow framework vertical |
| `perl-testing` | skill | ecc | 1 | secret-ref | Perl testing patterns; narrow language, low relevance |
| `quarkus-tdd` | skill | ecc | 1 | — | Quarkus TDD; narrow framework, low relevance |
| `quarkus-verification` | skill | ecc | 1 | network,secret-ref | Quarkus verification loop; narrow framework vertical |
| `react-testing` | skill | ecc | 1 | — | React component testing; framework-bound, not general eval |
| `rust-testing` | skill | ecc | 1 | — | Rust test patterns; language-bound |
| `springboot-tdd` | skill | ecc | 1 | — | Spring Boot TDD; framework-bound testing |
| `springboot-verification` | skill | ecc | 1 | secret-ref | Spring Boot build/test/scan loop; framework-bound |
| `swift-protocol-di-testing` | skill | ecc | 1 | — | Swift protocol-based DI testing; language-bound |
| `windows-desktop-e2e` | skill | ecc | 1 | exec,network,secret-ref | Windows desktop E2E testing; narrow platform vertical |

## Research & web (13)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `deep-research` | skill | ecc | 3 | — | Multi-source cited web research; core high-value domain |
| `exa-search` | skill | ecc | 3 | network,secret-ref | Neural web/code/company search via Exa; core domain |
| `literature-review` | skill | ecc | 3 | — | Systematic literature review/synthesis; core research domain |
| `market-research` | skill | ecc | 3 | — | Market/competitive research with attribution; core research domain |
| `research-ops` | skill | ecc | 3 | — | Evidence-first current-state research workflow; core domain |
| `search-first` | skill | ecc | 3 | exec | Research-before-coding, invokes researcher agent; core domain |
| `competitive-platform-analysis` | skill | ecc | 2 | — | Scope competitive landscape; research but vertical |
| `data-scraper-agent` | skill | ecc | 2 | network,secret-ref | Automated scraping/data collection agent; research-web adjacent |
| `docs-lookup` | agent | ecc | 2 | secret-ref | Fetches current library docs via Context7; research-adjacent |
| `documentation-lookup` | skill | ecc | 2 | secret-ref | Up-to-date docs via Context7 MCP; research-adjacent |
| `pubmed-database` | skill | ecc | 2 | network,secret-ref | PubMed biomedical literature search; research but biomedical niche |
| `benchmark-methodology` | skill | ecc | 1 | — | Competitor scoring across dimensions; market analysis vertical |
| `competitive-report-structure` | skill | ecc | 1 | — | Assemble competitive report; narrow market-analysis step |

## Context & token management (17)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `aside` | command | ecc | 3 | — | Answers side question without losing task context; context management |
| `ck` | skill | ecc | 3 | — | Persistent per-project memory and context loading; core |
| `context-budget` | skill | ecc | 3 | — | Audits context window consumption; core token management |
| `iterative-retrieval` | skill | ecc | 3 | exec,network | Progressive context refinement for subagents; core context domain |
| `knowledge-ops` | skill | ecc | 3 | exec,secret-ref | Knowledge base ingest/sync/retrieval across stores; core project domain |
| `resume-session` | command | ecc | 3 | secret-ref | Resumes prior session with full context |
| `save-session` | command | ecc | 3 | secret-ref | Saves session state for later resume |
| `sessions` | command | ecc | 3 | — | Manages session history and metadata |
| `strategic-compact` | skill | ecc | 3 | network | Manual context compaction at logical intervals; core domain |
| `token-budget-advisor` | skill | ecc | 3 | — | Response depth/token budget control; core domain |
| `unified-memory` | skill | ecc | 3 | secret-ref | Durable shared context/handoffs across agents; core domain |
| `update-codemaps` | command | ecc | 3 | — | Token-lean architecture codemaps; context management |
| `cost-report` | command | ecc | 2 | — | Generates Claude Code cost report; token/cost tracking |
| `cost-tracking` | skill | ecc | 2 | — | Track Claude Code token usage and spend; useful |
| `ecc:memory-persistence` | hook | ecc | 2 | — | Memory persistence hooks; relevant to context/memory |
| `growth-log` | skill | ecc | 2 | — | Reusable-pattern learning logs; knowledge capture, secondary |
| `living-docs-governance` | skill | ecc | 2 | secret-ref | Docs-as-canonical-sources for agent harness; knowledge base adjacent |

## Coding practices (general engineering) (65)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `api-connector-builder` | skill | ecc | 2 | — | Build API connectors matching repo pattern; secondary |
| `api-design` | skill | ecc | 2 | secret-ref | REST API design patterns; general but secondary |
| `architect` | agent | ecc | 2 | secret-ref | System design specialist; useful but general engineering |
| `architecture-decision-records` | skill | ecc | 2 | secret-ref | Capture ADRs from sessions; useful general practice |
| `brainstorming` | skill | superpowers | 2 | exec,network | Explore intent/requirements before implementation; broadly useful |
| `build-error-resolver` | agent | ecc | 2 | exec,secret-ref | Fixes build/TypeScript errors quickly; general dev utility |
| `build-fix` | command | ecc | 2 | — | Detects build system, fixes errors incrementally; general |
| `checkpoint` | command | ecc | 2 | — | Creates/verifies workflow checkpoints after checks; general workflow |
| `code-architect` | agent | ecc | 2 | secret-ref | Designs feature architecture from codebase patterns; general |
| `code-explorer` | agent | ecc | 2 | secret-ref | Traces execution paths, maps architecture; deep code reading |
| `code-review` | command | ecc | 2 | exec,secret-ref | Reviews local changes or GitHub PR; broadly useful |
| `code-reviewer` | agent | ecc | 2 | secret-ref | General code review for quality/security; broadly useful |
| `code-simplifier` | agent | ecc | 2 | secret-ref | Simplifies code preserving behavior; general engineering |
| `code-tour` | skill | ecc | 2 | network | Persona-targeted code walkthroughs; comprehension-adjacent, secondary |
| `codebase-onboarding` | skill | ecc | 2 | — | Analyze codebase, generate onboarding guide; deep-reading adjacent |
| `coding-standards` | skill | ecc | 2 | network | Cross-project coding conventions; general baseline |
| `epic-claim` | command | ecc | 2 | — | Epic issue coordination, reusable across projects |
| `epic-decompose` | command | ecc | 2 | — | Breaks epics into tasks, general workflow |
| `epic-publish` | command | ecc | 2 | — | Publishes epic updates to issue tracker |
| `epic-review` | command | ecc | 2 | — | Marks epic review state, general coordination |
| `epic-sync` | command | ecc | 2 | — | Syncs epic bodies and labels from GitHub |
| `epic-unblock` | command | ecc | 2 | — | Reopens epics whose dependencies closed |
| `epic-validate` | command | ecc | 2 | — | Validates epic readiness and dependencies |
| `error-handling` | skill | ecc | 2 | network | Cross-language robust error handling; general engineering |
| `feature-dev` | command | ecc | 2 | — | Guided feature development, broadly reusable |
| `feature-development` | command | ecc | 2 | — | Feature-development workflow scaffold |
| `finishing-a-development-branch` | skill | superpowers | 2 | — | Integrate completed branch work; general engineering |
| `git-workflow` | skill | ecc | 2 | secret-ref | Git branching/commit/merge conventions; general engineering |
| `hexagonal-architecture` | skill | ecc | 2 | — | Ports & Adapters architecture; general engineering |
| `inherit-legacy-style` | skill | ecc | 2 | — | Prevent style drift onto legacy projects; general engineering |
| `intent-driven-development` | skill | ecc | 2 | secret-ref | Scoped verifiable acceptance criteria; general engineering |
| `jira` | command | ecc | 2 | network | Jira ticket integration, reusable workflow |
| `performance-optimizer` | agent | ecc | 2 | network,secret-ref | Bottleneck/perf optimization specialist; general engineering |
| `plan` | command | ecc | 2 | — | Requirements and step-by-step planning |
| `plan-canvas` | command | ecc | 2 | — | Browser annotate-and-approve plan review |
| `pr` | command | ecc | 2 | network | Creates GitHub PR from current branch |
| `prp-commit` | command | ecc | 2 | — | Natural-language targeted quick commit |
| `prp-implement` | command | ecc | 2 | network | Executes plan with validation loops |
| `prp-plan` | command | ecc | 2 | — | Feature plan with codebase analysis |
| `prp-pr` | command | ecc | 2 | network | Creates GitHub PR from current branch |
| `quality-gate` | command | ecc | 2 | — | Formatter quality gate for a file |
| `receiving-code-review` | skill | superpowers | 2 | — | Rigorously evaluate code-review feedback; broadly useful |
| `refactor-clean` | command | ecc | 2 | — | Removes dead code with verification |
| `refactor-cleaner` | agent | ecc | 2 | secret-ref | Dead code removal via knip/ts-prune; general cleanup |
| `regex-vs-llm-structured-text` | skill | ecc | 2 | — | Regex-vs-LLM parsing decision framework; broadly useful |
| `repo-scan` | skill | ecc | 2 | exec | Cross-stack source asset audit installer; secondary utility |
| `requesting-code-review` | skill | superpowers | 2 | — | Verify work meets requirements before merge; useful |
| `review-pr` | command | ecc | 2 | — | PR review using specialized agents |
| `security-review` | skill | ecc | 2 | network,secret-ref | Security checklist for auth/input/secrets; general engineering |
| `security-reviewer` | agent | ecc | 2 | network,secret-ref | Security vulnerability detection/remediation; broadly useful |
| `silent-failure-hunter` | agent | ecc | 2 | secret-ref | Finds swallowed errors/silent failures; general quality |
| `spec-miner` | agent | ecc | 2 | secret-ref | Extracts behavioral specs from codebases; comprehension-adjacent |
| `systematic-debugging` | skill | superpowers | 2 | secret-ref | Structured debugging before fixes; broadly useful |
| `type-design-analyzer` | agent | ecc | 2 | secret-ref | Analyzes type design/invariant enforcement; general engineering |
| `update-docs` | command | ecc | 2 | — | Syncs docs from source; useful but secondary |
| `using-git-worktrees` | skill | superpowers | 2 | — | Isolated worktree workspace for feature work; useful |
| `writing-plans` | skill | superpowers | 2 | — | Plan multi-step tasks before coding; broadly useful |
| `ai-first-engineering` | skill | ecc | 1 | exec | Team process for AI-written codebases; secondary |
| `codehealth-mcp` | skill | ecc | 1 | network,secret-ref | CodeScene MCP code health scoring; secondary |
| `comment-analyzer` | agent | ecc | 1 | secret-ref | Analyzes comment accuracy and rot; niche |
| `content-hash-cache-pattern` | skill | ecc | 1 | — | SHA-256 content-hash caching pattern; narrow |
| `contract-first` | skill | ecc | 1 | secret-ref | API/event schema contract governance; narrow |
| `everything-claude-code` | skill | ecc | 1 | network | Repo-specific dev conventions; narrow |
| `latency-critical-systems` | skill | ecc | 1 | secret-ref | Latency-sensitive systems; specialized infra concern |
| `security-bounty-hunter` | skill | ecc | 1 | — | Repo vulnerability hunting; security vertical, narrow |

## Language / framework specific (94)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `android-clean-architecture` | skill | ecc | 1 | network | Android/Kotlin architecture; narrow vertical |
| `angular-developer` | skill | ecc | 1 | network,secret-ref | Angular code generation; narrow vertical |
| `backend-patterns` | skill | ecc | 1 | secret-ref | Node/Express/Next backend patterns; framework-specific |
| `bun-runtime` | skill | ecc | 1 | network | Bun runtime/package manager; narrow vertical |
| `compose-multiplatform-patterns` | skill | ecc | 1 | — | Compose Multiplatform UI patterns; narrow vertical |
| `cpp-build` | command | ecc | 1 | — | Fixes C++ build errors via resolver agent; language vertical |
| `cpp-build-resolver` | agent | ecc | 1 | secret-ref | C++ build error fixer; language-specific vertical |
| `cpp-coding-standards` | skill | ecc | 1 | network | C++ Core Guidelines standards; narrow vertical |
| `cpp-review` | command | ecc | 1 | — | C++ code review command; language-specific vertical |
| `cpp-reviewer` | agent | ecc | 1 | secret-ref | C++ code reviewer; language-specific vertical |
| `cpp-test` | command | ecc | 1 | — | C++ TDD with GoogleTest; language-specific vertical |
| `csharp-reviewer` | agent | ecc | 1 | secret-ref | C# code reviewer; language-specific vertical |
| `dart-build-resolver` | agent | ecc | 1 | secret-ref | Dart/Flutter build resolver; language-specific vertical |
| `dart-flutter-patterns` | skill | ecc | 1 | network,secret-ref | Dart/Flutter production patterns; narrow vertical |
| `django-build-resolver` | agent | ecc | 1 | secret-ref | Django build error resolver; framework-specific vertical |
| `django-celery` | skill | ecc | 1 | secret-ref | Django+Celery async patterns; narrow framework |
| `django-patterns` | skill | ecc | 1 | secret-ref | Django architecture/DRF patterns; framework-specific |
| `django-reviewer` | agent | ecc | 1 | secret-ref | Django code reviewer; framework-specific vertical |
| `django-security` | skill | ecc | 1 | network,secret-ref | Django security best practices; framework-specific |
| `dotnet-patterns` | skill | ecc | 1 | — | C#/.NET idiomatic patterns; language-specific |
| `fastapi-patterns` | skill | ecc | 1 | network,secret-ref | FastAPI best practices; framework-specific |
| `fastapi-review` | command | ecc | 1 | secret-ref | FastAPI-specific review, pulled on demand |
| `fastapi-reviewer` | agent | ecc | 1 | secret-ref | FastAPI reviewer; framework-specific vertical |
| `flutter-build` | command | ecc | 1 | — | Flutter/Dart build fixes, vertical library |
| `flutter-dart-code-review` | skill | ecc | 1 | network,secret-ref | Flutter/Dart review checklist; language-specific |
| `flutter-review` | command | ecc | 1 | secret-ref | Flutter/Dart code review, language-specific |
| `flutter-reviewer` | agent | ecc | 1 | secret-ref | Flutter/Dart reviewer; framework-specific vertical |
| `flutter-test` | command | ecc | 1 | — | Flutter/Dart test runner, language-specific |
| `foundation-models-on-device` | skill | ecc | 1 | — | Apple on-device LLM framework; narrow iOS vertical |
| `frontend-patterns` | skill | ecc | 1 | network | React/Next frontend patterns; framework-specific |
| `fsharp-reviewer` | agent | ecc | 1 | secret-ref | F# code reviewer; language vertical |
| `go-build` | command | ecc | 1 | — | Go build fixes, language-specific |
| `go-build-resolver` | agent | ecc | 1 | secret-ref | Go build error resolver; language-specific vertical |
| `go-review` | command | ecc | 1 | — | Go code review, language-specific |
| `go-reviewer` | agent | ecc | 1 | secret-ref | Go code reviewer; language-specific vertical |
| `go-test` | command | ecc | 1 | — | Go TDD workflow, language-specific |
| `golang-patterns` | skill | ecc | 1 | network | Idiomatic Go patterns; language-specific |
| `gradle-build` | command | ecc | 1 | — | Gradle/Android/KMP build fixes |
| `harmonyos-app-resolver` | agent | ecc | 1 | secret-ref | HarmonyOS ArkTS specialist; narrow platform vertical |
| `java-build-resolver` | agent | ecc | 1 | exec,secret-ref | Java/Maven/Gradle build resolver; language-specific vertical |
| `java-coding-standards` | skill | ecc | 1 | — | Java Spring/Quarkus standards; language-specific |
| `java-reviewer` | agent | ecc | 1 | secret-ref | Java Spring/Quarkus reviewer; language-specific vertical |
| `jpa-patterns` | skill | ecc | 1 | — | JPA/Hibernate entity patterns; framework-specific |
| `kotlin-build` | command | ecc | 1 | — | Kotlin/Gradle build fixes, language-specific |
| `kotlin-build-resolver` | agent | ecc | 1 | exec,secret-ref | Kotlin/Gradle build resolver; language-specific vertical |
| `kotlin-coroutines-flows` | skill | ecc | 1 | network | Kotlin coroutines/Flow patterns; language-specific |
| `kotlin-exposed-patterns` | skill | ecc | 1 | secret-ref | Kotlin Exposed ORM patterns; narrow language vertical |
| `kotlin-ktor-patterns` | skill | ecc | 1 | network,secret-ref | Ktor server patterns; narrow language framework |
| `kotlin-patterns` | skill | ecc | 1 | network | Idiomatic Kotlin; language-specific, low relevance |
| `kotlin-review` | command | ecc | 1 | secret-ref | Kotlin code review, language-specific |
| `kotlin-reviewer` | agent | ecc | 1 | secret-ref | Kotlin/Android reviewer; language-specific vertical |
| `kotlin-test` | command | ecc | 1 | secret-ref | Kotlin TDD with Kotest, language-specific |
| `laravel-patterns` | skill | ecc | 1 | secret-ref | Laravel/PHP architecture; narrow framework vertical |
| `laravel-plugin-discovery` | skill | ecc | 1 | network | Laravel package discovery; narrow framework vertical |
| `laravel-security` | skill | ecc | 1 | network,secret-ref | Laravel security; narrow framework vertical |
| `nestjs-patterns` | skill | ecc | 1 | secret-ref | NestJS backend patterns; narrow framework vertical |
| `nextjs-turbopack` | skill | ecc | 1 | network | Next.js/Turbopack bundling; narrow framework vertical |
| `nuxt4-patterns` | skill | ecc | 1 | network | Nuxt 4 app patterns; narrow framework vertical |
| `perl-patterns` | skill | ecc | 1 | exec | Modern Perl idioms; narrow language vertical |
| `perl-security` | skill | ecc | 1 | exec,secret-ref | Perl security patterns; narrow language vertical |
| `php-reviewer` | agent | ecc | 1 | secret-ref | PHP code reviewer; language-specific vertical |
| `python-patterns` | skill | ecc | 1 | network | Pythonic idioms/PEP8; language vertical, low relevance |
| `python-review` | command | ecc | 1 | — | Python code review, language-specific |
| `python-reviewer` | agent | ecc | 1 | exec,secret-ref | Python code reviewer; language-specific vertical |
| `quarkus-patterns` | skill | ecc | 1 | secret-ref | Quarkus Java patterns; narrow framework vertical |
| `quarkus-security` | skill | ecc | 1 | network,secret-ref | Quarkus security; narrow framework vertical |
| `react-build` | command | ecc | 1 | — | React build fixes, framework-specific |
| `react-build-resolver` | agent | ecc | 1 | secret-ref | React build failure fixer; framework-specific vertical |
| `react-native-patterns` | skill | ecc | 1 | secret-ref | React Native/Expo patterns; narrow framework vertical |
| `react-patterns` | skill | ecc | 1 | network | React component patterns; narrow framework vertical |
| `react-performance` | skill | ecc | 1 | network | React/Next.js perf rules; framework-specific |
| `react-review` | command | ecc | 1 | network,secret-ref | React/JSX code review, framework-specific |
| `react-reviewer` | agent | ecc | 1 | secret-ref | React/JSX code reviewer; framework-specific vertical |
| `react-test` | command | ecc | 1 | — | React Testing Library TDD, framework-specific |
| `rust-build` | command | ecc | 1 | — | Rust build/borrow-checker fixes, language-specific |
| `rust-build-resolver` | agent | ecc | 1 | secret-ref | Rust build error resolver; language-specific vertical |
| `rust-patterns` | skill | ecc | 1 | — | Idiomatic Rust patterns; language vertical |
| `rust-review` | command | ecc | 1 | secret-ref | Rust code review, language-specific |
| `rust-reviewer` | agent | ecc | 1 | secret-ref | Rust code reviewer; language-specific vertical |
| `rust-test` | command | ecc | 1 | secret-ref | Rust TDD workflow, language-specific |
| `springboot-patterns` | skill | ecc | 1 | — | Spring Boot backend patterns; framework vertical |
| `springboot-security` | skill | ecc | 1 | network,secret-ref | Spring Security practices; framework vertical |
| `swift-actor-persistence` | skill | ecc | 1 | — | Swift actor persistence; language vertical |
| `swift-build-resolver` | agent | ecc | 1 | secret-ref | Swift/Xcode build resolver; language-specific vertical |
| `swift-concurrency-6-2` | skill | ecc | 1 | — | Swift 6.2 concurrency; language vertical |
| `swift-reviewer` | agent | ecc | 1 | secret-ref | Swift code reviewer; language-specific vertical |
| `swiftui-patterns` | skill | ecc | 1 | — | SwiftUI architecture patterns; language vertical |
| `tinystruct-patterns` | skill | ecc | 1 | network,secret-ref | tinystruct Java framework; narrow framework vertical |
| `typescript-reviewer` | agent | ecc | 1 | exec,secret-ref | TypeScript/JavaScript reviewer; language-specific vertical |
| `ui-to-vue` | skill | ecc | 1 | secret-ref | Screenshot-to-Vue component conversion; framework vertical |
| `vite-patterns` | skill | ecc | 1 | network,secret-ref | Vite build tool patterns; framework vertical |
| `vue-patterns` | skill | ecc | 1 | network,secret-ref | Vue 3/Nuxt/Pinia patterns; framework vertical |
| `vue-review` | command | ecc | 1 | network,secret-ref | Vue-specific code review; narrow vertical |
| `vue-reviewer` | agent | ecc | 1 | secret-ref | Vue.js code reviewer; framework-specific vertical |

## DevOps & infrastructure (28)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `automation-audit-ops` | skill | ecc | 2 | — | Audits jobs/hooks/connectors inventory; ops-focused meta |
| `github-ops` | skill | ecc | 2 | secret-ref | GitHub repo/PR/CI operations via gh CLI; broadly useful |
| `pm2` | command | ecc | 2 | exec | Generates PM2 service commands |
| `terminal-ops` | skill | ecc | 2 | secret-ref | Evidence-first repo execution and CI debugging; useful secondary |
| `auto-update` | command | ecc | 1 | — | Pulls repo changes and reinstalls targets; ops utility |
| `canary-watch` | skill | ecc | 1 | network | Post-deploy URL smoke monitoring; ops vertical |
| `cisco-ios-patterns` | skill | ecc | 1 | secret-ref | Cisco IOS config review; networking vertical |
| `dashboard-builder` | skill | ecc | 1 | — | Grafana/SigNoz monitoring dashboards; ops vertical |
| `deployment-patterns` | skill | ecc | 1 | network,secret-ref | CI/CD, Docker, rollback patterns; infra vertical |
| `docker-patterns` | skill | ecc | 1 | network,secret-ref | Docker/Compose patterns; infra vertical |
| `flox-environments` | skill | ecc | 1 | exec,network,secret-ref | Nix-based reproducible dev environments; infra vertical |
| `kubernetes-patterns` | skill | ecc | 1 | network,secret-ref | Kubernetes workloads; infra vertical, low relevance |
| `netmiko-ssh-automation` | skill | ecc | 1 | secret-ref | Netmiko network automation; networking vertical |
| `network-architect` | agent | ecc | 1 | secret-ref | Enterprise network architecture; infra vertical |
| `network-bgp-diagnostics` | skill | ecc | 1 | — | BGP troubleshooting; networking vertical |
| `network-config-reviewer` | agent | ecc | 1 | secret-ref | Router/switch config reviewer; networking vertical |
| `network-config-validation` | skill | ecc | 1 | secret-ref | Router/switch config checks; networking vertical |
| `network-interface-health` | skill | ecc | 1 | — | Interface diagnostics; networking vertical |
| `network-troubleshooter` | agent | ecc | 1 | secret-ref | Network connectivity diagnostics; networking vertical |
| `opensource-forker` | agent | ecc | 1 | network,secret-ref | Forks/sanitizes projects for open-sourcing; niche pipeline |
| `opensource-packager` | agent | ecc | 1 | exec,network,secret-ref | Generates open-source packaging files; niche pipeline |
| `opensource-sanitizer` | agent | ecc | 1 | network,secret-ref | Scans forks for leaked secrets/PII; niche pipeline |
| `production-audit` | skill | ecc | 1 | secret-ref | Production readiness audit; ops vertical |
| `project-flow-ops` | skill | ecc | 1 | — | GitHub/Linear issue/PR coordination; ops vertical |
| `setup-pm` | command | ecc | 1 | — | Configures package manager; unrelated to project domains |
| `terminal-opener` | skill | ecc | 1 | exec,secret-ref | Open CLI in visible terminal; narrow ops utility |
| `uncloud` | skill | ecc | 1 | network,secret-ref | Uncloud cluster management; narrow ops vertical |
| `unified-notifications-ops` | skill | ecc | 1 | secret-ref | Notification routing across tools; ops vertical |

## Data & ML (16)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `clickhouse-io` | skill | ecc | 1 | network,secret-ref | ClickHouse query optimization; database vertical |
| `data-throughput-accelerator` | skill | ecc | 1 | — | Speed up ETL/ingestion/backfill; data vertical |
| `database-migration` | command | ecc | 1 | — | Database migration workflow scaffold; database vertical |
| `database-migrations` | skill | ecc | 1 | — | DB schema/data migration best practices; narrow infra vertical |
| `database-reviewer` | agent | ecc | 1 | secret-ref | PostgreSQL query/schema specialist; narrow database vertical |
| `ml-adoption-playbook` | skill | ecc | 1 | — | Adding ML to codebases; ML vertical, low relevance |
| `mle-reviewer` | agent | ecc | 1 | exec,secret-ref | ML engineering pipeline reviewer; MLOps vertical |
| `mle-workflow` | skill | ecc | 1 | exec,secret-ref | ML engineering workflow; ML vertical, low relevance |
| `mysql-patterns` | skill | ecc | 1 | secret-ref | MySQL schema/query patterns; database vertical |
| `postgres-patterns` | skill | ecc | 1 | — | PostgreSQL schema/query/RLS patterns; database vertical |
| `prisma-patterns` | skill | ecc | 1 | secret-ref | Prisma ORM patterns; database vertical |
| `pytorch-build-resolver` | agent | ecc | 1 | network,secret-ref | PyTorch training error resolver; ML vertical |
| `pytorch-patterns` | skill | ecc | 1 | exec | PyTorch training patterns; ML vertical |
| `recsys-pipeline-architect` | skill | ecc | 1 | exec | Recommendation pipeline design; narrow ML vertical |
| `redis-patterns` | skill | ecc | 1 | — | Redis caching/locks; infra vertical, low relevance |
| `videodb` | skill | ecc | 1 | network,secret-ref | Video/audio ingest, indexing, search; media data vertical |

## Design & UX (20)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `a11y-architect` | agent | ecc | 1 | secret-ref | WCAG accessibility architect; UI vertical, low project relevance |
| `accessibility` | skill | ecc | 1 | network | WCAG accessibility auditing; UI vertical, low relevance |
| `design-system` | skill | ecc | 1 | network | Generate/audit design systems; UX not core |
| `fal-ai-media` | skill | ecc | 1 | network,secret-ref | AI image/video/audio generation; media vertical |
| `frontend-a11y` | skill | ecc | 1 | secret-ref | React/Next accessibility patterns; UX vertical |
| `frontend-design-direction` | skill | ecc | 1 | — | ECC frontend design direction; UX vertical |
| `frontend-slides` | skill | ecc | 1 | exec,network | HTML presentation builder; design vertical |
| `ios-icon-gen` | skill | ecc | 1 | network | iOS app icon generation; narrow media vertical |
| `liquid-glass-design` | skill | ecc | 1 | — | iOS Liquid Glass UI; narrow platform design |
| `make-interfaces-feel-better` | skill | ecc | 1 | — | UI polish details; design vertical, low relevance |
| `manim-video` | skill | ecc | 1 | — | Manim animated explainers; media production vertical |
| `motion-advanced` | skill | ecc | 1 | — | Advanced React motion; design vertical |
| `motion-foundations` | skill | ecc | 1 | — | React motion foundations; design vertical |
| `motion-patterns` | skill | ecc | 1 | — | React UI animation patterns; design vertical |
| `motion-ui` | skill | ecc | 1 | — | React motion system; design vertical |
| `remotion-video-creation` | skill | ecc | 1 | network | React video creation; narrow media vertical |
| `taste` | skill | ecc | 1 | — | Creative direction for music videos; narrow media vertical |
| `tasteforge-video` | skill | ecc | 1 | — | Multimodal asset discovery/taste workflows; media vertical |
| `ui-demo` | skill | ecc | 1 | network | Playwright UI demo video recording; media vertical |
| `video-editing` | skill | ecc | 1 | network,secret-ref | AI video editing pipeline; media vertical |

## Writing & content (12)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `doc-updater` | agent | ecc | 2 | secret-ref | Updates codemaps and docs; useful for knowledge base |
| `article-writing` | skill | ecc | 1 | — | Long-form article writing; content vertical |
| `brand-voice` | skill | ecc | 1 | — | Source-derived writing style profile; content vertical |
| `connections-optimizer` | skill | ecc | 1 | — | X/LinkedIn network pruning and outreach; social vertical |
| `content-engine` | skill | ecc | 1 | — | Platform-native content systems; content vertical |
| `crosspost` | skill | ecc | 1 | — | Multi-platform content distribution; social vertical |
| `marketing-agent` | agent | ecc | 1 | secret-ref | Marketing strategist/copywriter; content vertical |
| `marketing-campaign` | command | ecc | 1 | — | Marketing copy/campaign, vertical library |
| `marketing-campaign` | skill | ecc | 1 | — | Multi-channel marketing campaigns; content/GTM vertical |
| `seo` | skill | ecc | 1 | network | SEO audit and remediation; marketing vertical |
| `seo-specialist` | agent | ecc | 1 | secret-ref | Technical SEO audits; marketing vertical |
| `social-publisher` | skill | ecc | 1 | network,secret-ref | Multi-platform social posting; content vertical |

## Product & strategy (8)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `plan-prd` | command | ecc | 2 | — | Generates lean PRD, hands off to plan |
| `product-capability` | skill | ecc | 2 | — | PRD-to-SRS capability planning; product domain, secondary |
| `product-lens` | skill | ecc | 2 | — | Validate product why; product diagnostics, secondary |
| `prp-prd` | command | ecc | 2 | — | Interactive problem-first PRD generator |
| `brand-discovery` | skill | ecc | 1 | — | Brand identity interviews; strategy vertical |
| `investor-materials` | skill | ecc | 1 | — | Pitch decks/investor memos; narrow strategy vertical |
| `investor-outreach` | skill | ecc | 1 | — | Investor cold emails/follow-ups; narrow strategy vertical |
| `lead-intelligence` | skill | ecc | 1 | secret-ref | Sales lead/outreach pipeline; GTM vertical |

## Domain verticals (finance, health, logistics, …) (47)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `agent-payment-x402` | skill | ecc | 1 | exec,network,secret-ref | Crypto payment execution for agents; narrow vertical |
| `blender-motion-state-inspection` | skill | ecc | 1 | — | Blender rig/animation inspection; narrow vertical |
| `carrier-relationship-management` | skill | ecc | 1 | — | Freight carrier portfolio management; narrow vertical |
| `customer-billing-ops` | skill | ecc | 1 | secret-ref | Customer billing/subscription operations; narrow vertical |
| `customs-trade-compliance` | skill | ecc | 1 | network | Customs/tariff trade compliance; narrow vertical |
| `defi-amm-security` | skill | ecc | 1 | secret-ref | Solidity AMM security audit; narrow finance vertical |
| `ecc-tools-cost-audit` | skill | ecc | 1 | secret-ref | ECC billing/burn audit; narrow repo-specific vertical |
| `email-ops` | skill | ecc | 1 | secret-ref | Mailbox triage/drafting workflow; narrow vertical |
| `energy-procurement` | skill | ecc | 1 | — | Electricity/gas procurement expertise; narrow vertical |
| `evm-token-decimals` | skill | ecc | 1 | — | EVM token decimal bug prevention; narrow crypto vertical |
| `finance-billing-ops` | skill | ecc | 1 | — | Revenue/billing/refunds workflow; narrow finance vertical |
| `generating-python-installer` | skill | ecc | 1 | network | Windows Python installer packaging; narrow vertical |
| `gget` | skill | ecc | 1 | network | Bioinformatics genomic query CLI; narrow vertical |
| `google-workspace-ops` | skill | ecc | 1 | — | Google Drive/Docs/Sheets/Slides ops; narrow vertical |
| `healthcare-cdss-patterns` | skill | ecc | 1 | — | Clinical decision support patterns; narrow healthcare vertical |
| `healthcare-emr-patterns` | skill | ecc | 1 | — | EMR/EHR development patterns; narrow healthcare vertical |
| `healthcare-phi-compliance` | skill | ecc | 1 | — | PHI/PII compliance patterns; narrow healthcare vertical |
| `healthcare-reviewer` | agent | ecc | 1 | secret-ref | Clinical safety/PHI reviewer; healthcare vertical |
| `hipaa-compliance` | skill | ecc | 1 | secret-ref | HIPAA healthcare compliance entrypoint; narrow vertical |
| `homelab-architect` | agent | ecc | 1 | secret-ref | Home network planning; homelab vertical |
| `homelab-network-readiness` | skill | ecc | 1 | — | Homelab VLAN/DNS/VPN readiness; narrow vertical |
| `homelab-network-setup` | skill | ecc | 1 | — | Home network planning; narrow homelab vertical |
| `homelab-pihole-dns` | skill | ecc | 1 | exec,network,secret-ref | Pi-hole DNS setup; narrow homelab vertical |
| `homelab-vlan-segmentation` | skill | ecc | 1 | secret-ref | Home VLAN segmentation; narrow homelab vertical |
| `homelab-wireguard-vpn` | skill | ecc | 1 | exec,network,secret-ref | WireGuard VPN setup; narrow homelab vertical |
| `inventory-demand-planning` | skill | ecc | 1 | — | Retail demand forecasting; narrow vertical |
| `ito-baskets` | skill | ecc | 1 | exec,network,secret-ref | Prediction-market basket data; narrow finance vertical |
| `ito-compute` | skill | ecc | 1 | secret-ref | GPU RFQ/procurement CLI; narrow vertical |
| `ito-inference` | skill | ecc | 1 | secret-ref | Model serving handoff on Itô booking; narrow vertical |
| `ito-training` | skill | ecc | 1 | exec,secret-ref | ML training handoff on Itô booking; narrow vertical |
| `jira-integration` | skill | ecc | 1 | network,secret-ref | Jira ticket ops via MCP/REST; narrow vertical |
| `llm-trading-agent-security` | skill | ecc | 1 | network,secret-ref | Trading agent wallet security; finance vertical |
| `logistics-exception-management` | skill | ecc | 1 | — | Freight exception handling; logistics vertical |
| `mailtrap-email-integration` | skill | ecc | 1 | network,secret-ref | Transactional email API integration; narrow vendor vertical |
| `messages-ops` | skill | ecc | 1 | exec | Live messaging/DM inspection workflow; narrow vertical |
| `nodejs-keccak256` | skill | ecc | 1 | — | Ethereum hashing bug prevention; crypto vertical |
| `nutrient-document-processing` | skill | ecc | 1 | network,secret-ref | Document processing via Nutrient API; vendor vertical |
| `openclaw-persona-forge` | skill | ecc | 1 | secret-ref | OpenClaw persona/character creation; niche gaming vertical |
| `prediction-market-oracle-research` | skill | ecc | 1 | — | Prediction market oracle research; finance vertical |
| `prediction-market-risk-review` | skill | ecc | 1 | secret-ref | Trading workflow risk review; finance vertical |
| `production-scheduling` | skill | ecc | 1 | — | Manufacturing scheduling; industrial vertical |
| `quality-nonconformance` | skill | ecc | 1 | network | Manufacturing quality/NCR; industrial vertical |
| `returns-reverse-logistics` | skill | ecc | 1 | secret-ref | Returns/warranty operations; narrow vertical |
| `social-graph-ranker` | skill | ecc | 1 | — | Social-graph ranking for warm intros; narrow vertical |
| `uspto-database` | skill | ecc | 1 | exec,network,secret-ref | USPTO patent/trademark lookup; narrow legal vertical |
| `visa-doc-translate` | skill | ecc | 1 | — | Visa document translation to bilingual PDF; narrow vertical |
| `x-api` | skill | ecc | 1 | network,secret-ref | X/Twitter API integration; social vertical |

## Other (1)

| Name | Type | Repo | Fit | Flags | Note |
| --- | --- | --- | --- | --- | --- |
| `chief-of-staff` | agent | ecc | 1 | network,secret-ref | Multi-channel comms triage; unrelated to project |
