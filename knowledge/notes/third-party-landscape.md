---
title: The third-party landscape — every skill, agent, plugin, tool, tip and trick in this knowledge base, summarised
sources:
  - path: knowledge/notes/agent-builder-prior-art.md
  - path: knowledge/notes/claude-code-ecosystem-plugins.md
  - path: knowledge/notes/model-agnostic-agent-harnesses.md
  - path: knowledge/notes/harness-over-model-prime-agent.md
  - path: knowledge/notes/graphify-assessment.md
  - note: "A compiled page (llm-wiki query written back as a note): every row points at the note that holds the evidence; the paths above are the five it draws on most. Added by the kb-curator's first pass, 2026-09-02, to satisfy the schema."
fetched: 2026-09-02
tags: [summary, landscape, skills, agents, plugins, tools, harvest, claims-graded]
related: ["[[agent-builder-prior-art]]", "[[claude-code-ecosystem-plugins]]", "[[model-agnostic-agent-harnesses]]", "[[harness-over-model-prime-agent]]", "[[graphify-assessment]]", "[[temporal-kg-agent-memory]]", "[[llm-wiki-pattern]]", "[[loop-engineering-and-fable-prompting]]", "[[production-site-checklist]]", "[[learning-resources-agents]]", "[[local-finetuning-layer-streaming]]", "[[prompt-patterns-kernel]]", "[[claude-md-and-memory]]", "[[mcp]]", "[[model-routing-free-and-local]]", "[[token-economy-playbook]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
compiled_from:
  # A compiled page has no external source to watch, so nothing could tell it its INPUTS had
  # moved. This is the join key that makes it checkable: each input note's newest declared
  # `fetched:` at the moment this page was compiled. `kb.py lint` warns when an input's current
  # value is later than this page's own `fetched:`. Recorded 2026-09-08, after the page was
  # found stale against all five of its inputs.
  - agent-builder-prior-art: 2026-08-29
  - claude-code-ecosystem-plugins: 2026-09-02
  - model-agnostic-agent-harnesses: 2026-09-08
  - harness-over-model-prime-agent: 2026-09-02
  - graphify-assessment: 2026-09-04
  # Re-reconciled 2026-09-12 against the two inputs the join key flagged as moved. NOT a full
  # recompile: the check names WHICH inputs moved, so only the rows drawn from those two were
  # re-read. graphify's obsidian chain was already carried here (the page says "settled
  # 2026-09-04"); the Ornith row was stale on a PROVENANCE label - MIT had been upgraded from
  # REPEATED to MEASURED, and the ownership claim both secondaries agreed on was refuted. A
  # compiled page rots one row at a time, and the join key is what makes that affordable.
  #
  # The snapshot records each input's OWN declared fetch (09-08, 09-04), not the date of this
  # reconcile - a snapshot saying 09-12 would claim the input declared something it never did,
  # and the whole value of the key is that both sides of the comparison are the input's words.
  #
  # KNOWN LIMIT, stated where it can be acted on: this key is SELF-REPORTED. Bumping these two
  # dates clears the warning whether or not a single row was re-read. The check says WHEN to
  # look, never THAT you looked, and no script can close that gap - the reconcile is prose work.
  # What it does buy is the narrowing: it names which inputs moved, so this pass re-read two
  # notes instead of five and touched one row instead of a 31 KB page.
---

# The third-party landscape, summarised

**What this is.** A compiled page — the `query` operation of [[llm-wiki-pattern]] written back
as a note — over everything in this knowledge base that came from *outside Anthropic*: GitHub
repositories, practitioner profiles, papers, videos and vendor pages, harvested between
2026-08-26 and 2026-09-02. Anthropic's own documentation and repositories are excluded by the
question; where a third-party claim was graded *against* an Anthropic page, that is said.
Every row points at the note or mined document that holds the evidence; nothing here is new.

**The scale, as of compiling (2026-09-02).** 469 components catalogued from two repositories
(`catalog/catalog.json`, 2026-08-27), 44 adopted as talents; ten mined documents over six more
repositories with verdict tables (in `intake/…/scio/docs/mined/`); **36 notes**; ~35 short
videos graded against primary sources in five batches on 2026-09-02; roughly 80 named projects
in total.

> **The note count is a LIVE number and was pinned here as a fixed one.** It was 36 at
> compiling and is not 36 now; read it from the base (`ls knowledge/notes/*.md | wc -l`), never
> from this line. Kept as written, dated, because it is what this page was compiled over — the
> rows below are true of those 36 — but a reader must not carry the figure forward. The same
> caution applies to "44 adopted as talents": that is the catalog's `adopted` count on
> 2026-08-27, cited again with its source further down, and it is not the size of the talent
> library today. This is the repository's own standing rule about running statistics, and this
> page had broken it: *a value that moves on its own is recorded as a finding plus a pointer to
> its live computation, never as a number.*

---

## 1 · The sources, and what each yielded

| Source | What it is | What came out | Where |
|---|---|---|---|
| **obra/superpowers** (MIT, 277,967★ on 2026-08-26) | 14 workflow skills | **12 adopted verbatim** after A/B (writing-skills, TDD, verification-before-completion, subagent-driven-development, dispatching-parallel-agents, writing-plans, brainstorming, systematic-debugging, using-git-worktrees, finishing-a-development-branch, requesting/receiving-code-review). Its `writing-skills` rule — *if you didn't watch an agent fail without the skill you don't know what it teaches* — is the library's own test discipline | `catalog/first-wave.md`, `OTHERS-MINED` §2 |
| **affaan-m/ECC** (MIT, 243,420★) | 286 skills · 68 agents · 94 commands · 23 hooks · 122 rule files | **32 adopted or adapted** (eval-harness, santa-method, skill-scout, skill-stocktake, context-budget, loop-design-check, parallel-execution-optimizer, unified-memory, agent-architecture-audit, agentic-os, mcp-server-patterns, literature-review, market-research, enterprise-agent-ops …). Mined in four passes: 18 + 19 + 45 + 60 verdict rows. The recurring finding: **its plumbing is worth taking, its roster is not** — "their chain document is better than ours, and their chain is worse" | `ECC-MINED`, `ECC-AGENTS`, `ECC-RULES`, `ECC-SKILLS`, `PASS2-ECC-*` |
| **garrytan/gstack** (MIT) | 61 skills, a TypeScript codebase with 554 test files | Skipped as a dependency, **mined as the richest single source of mechanisms**: 33 + 32 verdict rows, almost all "take" — see §3 | `OTHERS-MINED` §1, `PASS2-GSTACK-SKILLS`, `PASS2-GSTACK-TESTS` |
| **Practitioner repos** — stanfordnlp/dspy, dottxt-ai/outlines, simonw/llm, pydantic/pydantic-ai, hamelsmu | frameworks and a profile | Frameworks not adopted; **7 methods built** from them: llm-judge-calibration, error-analysis-taxonomy, synthetic-eval-data-generation (hamelsmu), llm-call-ledger (simonw), external-domain-audit, integration-contract-completeness (pydantic-ai), metric-driven-prompt-optimization (dspy). Highest method yield of any source type | `intake/wave9-two-loops.md`, `pipeline/LESSONS.md` |
| **eyaltoledano/claude-task-master** | task pipeline; **MIT + Commons Clause** (withholds the right to sell) | Not vendored (licence); 12 mechanisms taken as ideas, best: the arithmetic coherence gate on reported test results, "already implemented" as a first-class outcome, user-owned fields absent from the model's output schema | `PASS2-FOUR-REPOS` §1 |
| **zilliztech/claude-context** | semantic code search MCP over a vector DB | Vector-on-the-deciding-path rejected, three times; its own eval shows F1 0.40 → 0.40; three-way content-hash diff taken | `PASS2-FOUR-REPOS` §2 |
| **supermemoryai/supermemory** | hosted memory | Service rejected; the *schema* mined: versioned assertions with `isLatest`, `isInference`, `isStatic`, forget-with-reason — and the finding that its forgetting has no engine | `PASS2-FOUR-REPOS` §3 |
| **yamadashy/repomix** | packs a repo into one file | The anti-pattern with a CLI (packing, not retrieval); its dedup and elision-marker code taken | `PASS2-FOUR-REPOS` §4 |
| **rohitg00/awesome-claude-code-toolkit** | 40 skills · 138 agents · 262 commands · 21 hooks | 0 factory talents; library tier (vertical: WCAG, AWS, k8s, Rust …) | `intake/wave3` |
| **ComposioHQ/awesome-claude-skills**, **hesreallyhim/awesome-claude-code**, the MCP registries | curated lists | Indexes, not sources: read only to extract repo paths | `LESSONS`, `TOOLING-SCAN` |
| **addyosmani/agent-skills** (MIT, 91.6k★) | 25 engineering skills, 4 personas, 8 commands | Reuse-first source; ≥9 name collisions with our talents; `shipping-and-launch` twins the site checklist | [[agent-builder-prior-art]] |
| **skills.sh / find-skills** (Vercel, 1.29M installs) | a skills registry and the skill that searches it | A *source*; its vetting is installs + stars + an org whitelist, weaker than our four gates | [[agent-builder-prior-art]] |
| **keysersoose/claude-agent-builder**, **FrancyJGLisboa/agent-skill-creator** | agent/skill builders | Three builders solve three problems under one name; none tests against a baseline; one has lifecycle governance we lack | [[agent-builder-prior-art]] |
| **Graphify-Labs/graphify** (Apache-2.0 since v8; MIT through v7 — checked 2026-09-04) | code → knowledge graph, AST, no LLM for code | **Adopted** as the code-graph tool: 0-token extraction, `query/explain/path`, `export obsidian`; blind across a language seam; not for markdown corpora | [[graphify-assessment]], [[graphify-features]] |
| **getzep/graphiti** | temporal knowledge graph | Reference only (needs a graph DB + LLM); its bi-temporal rule adopted in note frontmatter | [[temporal-kg-agent-memory]] |
| **garrytan/gbrain** (MIT) | markdown-in-git brain with PGLite, typed edges, nightly consolidation | Not installed; zero-LLM typed-edge extraction copied into the KB index | [[temporal-kg-agent-memory]] |
| **Karpathy's LLM Wiki gist** | raw/ · wiki/ · schema; ingest, query, lint | Adopted as this KB's shape; `knowledge/raw/` and `kb.py` follow it | [[llm-wiki-pattern]] |
| **The plugin stack the videos sell** — OmniRoute (MIT 60k★), claude-mem (Apache 93k★), Headroom (Apache 68k★), unlazy (MIT 3k★), Graft (MIT 5k★), codebase-memory-mcp (MIT 42k★), OpenMontage (**AGPL** 55k★), agency-agents (MIT 150k★), task-observer, BASE (**PolyForm Noncommercial**) | routers, memory, compression, gates, personas | Each real, each mis-described by its video; **none adopted**; unlazy's gates-file shape and Graft's controlled +42%-tokens figure are the two things kept | [[claude-code-ecosystem-plugins]], [[claude-md-and-memory]] |
| **Harnesses** — Goose (Apache, Linux Foundation, 60+ providers), Pi (MIT, minimal), Herdr (multiplexer), Ruflo ex Claude Flow (MIT 70k★, swarm + AgentDB), Prime Agent (MIT 19.7k★, self-refining) | alternatives to Claude Code | Goose is the honest "any model per task" harness; Ruflo's shared memory is a multi-tenant hazard; Prime Agent's 95.5% ARC-AGI-3 is self-reported against a verified 30.2% for the model alone and is the author-grades-own-work shape our gates refuse | [[model-agnostic-agent-harnesses]], [[harness-over-model-prime-agent]] |
| **Gateways and free models** — free-claude-code (MIT 52.8k★), claude-code-router, LiteLLM, Nemotron 3 Ultra free endpoints, the 260-free-APIs list (CC0), Ornith-1.5 (open weights; **MIT MEASURED** from the model card's own frontmatter 2026-09-08, and the weights are under **`ornith-ai`, not `deepreinforce-ai`** as both secondaries said — plus three sizes that are all **vision-language** at **256K** context, which no write-up mentioned) | run Claude Code on non-Claude models | Anthropic's page: unsupported for non-Claude models; with a gateway credential the subscription is unused. "Free forever" = the CLI on free tiers with logging and trial terms. Usable only as a *non-comparable extra arm* in a measurement | [[model-agnostic-agent-harnesses]] |
| **Design and components** — shadcn registries (Magic UI MIT, Kibo, Aceternity, Origin→coss.com/ui **MIT/AGPL mixed**), registry.directory (82 registries), Supabase UI Library, tweakcn, UI UX Pro Max (MIT 124k★), 21st.dev, W3C DTCG, Style Dictionary, Tokens Studio, Figma MCP | component and token ecosystems | Reference commodity parts through an allow-listed registry, never copy; tokens in DTCG; the Supabase library is the one feature-shaped source | [[production-site-checklist]], Scio `LIBRARY-SOURCES-2026-09-02` |
| **Infrastructure** — E2B, Modal, Cloudflare Sandboxes, Vercel Sandbox, Daytona; OpenFGA, SpiceDB, Cedar, Oso; SLSA/in-toto/Sigstore, SPDX, CycloneDX; datasketch MinHash; Backstage, OCM; Context7; chrome-devtools-mcp, playwright-mcp, Sentry, Prisma MCP, crystaldba/postgres-mcp; Serena (MIT 28.7k★); Obsidian | sandboxes, authz, supply chain, retrieval, editors | Firecracker-class sandboxes are the field consensus; authz services rejected until tenancy grows a second relation; signed provenance is "the differentiator's format"; Serena piloted for symbol-level edits; Obsidian a viewer, never a store | Scio `next/LAYER-E` §3.3, `next/LAYER-G`, `next/LAYER-D` §5, ADR-0011, ADR-0013 |
| **Learning and papers** — Stanford CS329A, OpenMAIC (MIT 30k★), ICM (arXiv 2603.16021), Soup (Apache), AXI, LOOPS.md, KERNEL | courses, methods, memes | CS329A parts 3 and 7 are reading for verification and self-improvement; ICM states no token number; Soup's public retraction is the standard we ask of ourselves; AXI's CLI-beats-MCP benchmarks have the agent model as judge; LOOPS.md's attribution is unverified; KERNEL's numbers are unsupported | [[learning-resources-agents]], [[claude-md-and-memory]], [[local-finetuning-layer-streaming]], [[mcp]], [[loop-engineering-and-fable-prompting]], [[prompt-patterns-kernel]] |

Excluded by the question: `anthropics/skills`, `skill-creator`, `plugin-dev`, `claude-code-setup`
and the official plugins — recorded in `intake/wave5` and `TOOLING-SCAN` as library and
methodology, not as third-party.

---

## 2 · What became talents

**44 adopted in the catalog** (`catalog.json`, status `adopted`): 12 from superpowers, 32 from
ECC, of which 11 are *adapted* — rebuilt as safe, general versions when the original carried a
hook, an installer or a network call (`safety-guard` → `agent-blast-radius-guard`,
`security-scan` → `agent-surface-security-audit`, `council` → `decision-council`,
`model-route` + `cost-aware-llm-pipeline` → `cost-aware-model-routing`,
`regex-vs-llm-structured-text` → `hybrid-parse-escalation`, `inherit-legacy-style` →
`style-inheritance`, `spec-miner` → `behavioral-spec-mining`, `benchmark-optimization-loop` →
`measured-optimization-loop`, `mle-reviewer` → `mlops-production-review`). Plus the seven
practitioner methods above, and the talents the loop built itself. **Every adopted skill was
measured baseline-versus-with on a planted-defect scenario** before it entered
`.claude/skills/`; the first wave flipped 0/3 → 3/3 on all nine.

**Flagged by the security gate and not adopted as-is:** `deep-research` (outbound web through
third-party MCPs — prompt-injection surface), `strategic-compact` (an unbundled node hook on
every edit), `skill-comply` (spawns `claude -p` running LLM-generated commands under your
credentials — valuable, only in a sandbox).

---

## 3 · The tips, tricks and mechanisms taken — by theme

Condensed from ~200 "take" rows. Each is a method someone else wrote down and we verified
against their code; the layer it serves in Scio is in the source document.

**Gates and verdicts**
- A gate enumerates its unverifiable states; empty, errored, truncated and untagged output is a
  *verification failure*, never "0 findings" (gstack `codex`).
- Five outcome states — DONE / PARTIAL / NOT DONE / CHANGED / UNVERIFIABLE; "the gate could not
  run" is never DONE (gstack `review`).
- No finding reaches a person without a verbatim quote of the line that caused it (gstack).
- Validators emit one evidence row per checked pair; no rows means no scan (superpowers).
- "No issues found" needs what-was-examined; "skipped" is never valid (gstack `autoplan`).
- Exit 0 is not evidence: declare lanes, count executed units, check for failure lines
  (gstack tests). Arithmetic coherence on reported test counts: sum, RED ≥ 1 failure, GREEN ≥ 1
  pass, regression warning (task-master).
- Score caps: a binary deterministic condition sets a ceiling a judgement score may not exceed
  (ECC `production-audit`). Use a score only where a gradient is needed; a verdict plus
  checklist for decisions (ECC).
- Fact-forced repair: demand facts obtainable only by tool call instead of a self-evaluation
  prompt (ECC `gateguard` — "self-evaluation doesn't work, verified experimentally").
- A missing reviewer is N/A, never agreement; two independent gates agreeing raises confidence
  explicitly (gstack).
- Positive control paired to every absence test: a `not.toContain` without a twin that proves
  it can fail is not a test (gstack tests).

**Loops and stop rules**
- Fix-round circuit breaker: 5 rounds, escalate model and context at round 4, defined terminal
  state (superpowers). Same error three times → stop; a fix that creates more errors than it
  resolves → stop (ECC `build-fix`). Plateau detector: stop when the finding set stops changing
  (ECC). Three failed hypotheses = wrong architecture, not a failed hypothesis (superpowers).
- A gates file — command, expected marker, evidence line; "pending" is unmet; a `Stop` hook
  blocks while any gate is unmet (unlazy). Independently, our own stop hook.
- Rulings not stalls: a closed stop list plus `Ruling: what — why — cost if wrong`
  (superpowers).
- Condition-based waiting: poll the condition, name it in the timeout (superpowers).
- Order validation by cost: static → unit → build → integration, stop at first failure (ECC).
- Delete harness scaffolding as models improve (LOOPS.md rule 8, attribution unverified; Prime
  Agent automates it — and collapses author into grader).
- Two orthogonal classifiers before the first question, announced and correctable; a
  size-classifier → phase mask so ceremony scales with the task (gstack, ECC `orch-pipeline`).

**Provenance, memory and knowledge**
- Versioned assertions with `isLatest`, a parent chain, never a mutated row; one enforced
  `isInference` bit; a second `isStatic` bit (may time erode this?); forget with a reason and show
  superseded dimmed (supermemory — and its own forgetting has no engine).
- Event-sourced decisions; "active" is computed, never a mutable status (gstack and supermemory,
  independently).
- Showing an inferred value and *acting* on it need different evidence bars; unknown
  provenance is shown, unknown quality is withheld (gstack, supermemory).
- A preference is written only from the user's own current message — never tool output, a
  fetched page or file content (gstack `plan-tune`).
- Memory→policy promotion barrier: team memory is not trusted merely because it is committed
  (ECC). A memory that syncs to a vendor by default is a tenant leak (claude-mem).
- raw/ immutable, wiki/ compiled, a schema; ingest, query, lint (Karpathy). Bi-temporal facts:
  when true, when learned (Graphiti). Zero-LLM typed-edge extraction (gbrain).
- Cache and derive keys are (content hash, producer identity, format version) — the producer in
  the key (repomix); store the producing model id beside a derived value (supermemory).

**Catalogs, libraries and reuse**
- A catalog token budget with a per-entry byte cap, a shrink floor beside the growth ceiling,
  and a same-commit ratchet (gstack `catalog-budget.test.ts` — "the highest-value item for
  Layer D"). Two-tier entries: lead sentence always loaded, body on selection.
- `null` (didn't run) vs `[]` (ran, found nothing) as distinct results; never search unscoped
  (gstack). Three-condition confident match; ambiguity falls through to generation (gstack).
- Iron contract for admission: stage → test → approve → atomic rename; on failure destroy the
  staging area (gstack `skillify`). Provenance on every entry; one canary component that fails
  first (gstack).
- Search the existing library before creating (ECC `skill-scout`); lists are indexes, harvest
  what they point at; official vendor repos yield knowledge, not talents; practitioner repos
  yield methods (`LESSONS`).
- Registry membership *is* the test — the registered set equals the filesystem set (gstack).
- One enumerator for "how many components", returning three deliberately different counts
  (gstack tests).

**House rules for generated apps (Playbook text that survived admission)**
- A `## Never` block; anon key is public and safe only because RLS is explicit; generic error
  out, detail to the log; rate-limit auth and unauthenticated mutations; migration discipline
  with policies in the same file; explicit query limits; a dependency policy (ECC rules, ~+173
  tokens). Never write a request body into an insert; never redirect to a URL from a query
  parameter; validate what comes *back* from external services; a destructive migration states
  its reverse (ECC pass 2, +120 tokens).
- Every `"use server"` function is a public endpoint; no mutable module-level state in RSC/SSR;
  `USING ((SELECT auth.uid()) = user_id)` so RLS evaluates once; schema types `bigint`, `text`,
  `timestamptz`, `numeric`; `onUnhandledRequest: "error"` (Vercel Labs `react-performance`,
  Supabase `postgres-patterns`, ECC).
- Sensitivity labels that survive into the database as `COMMENT ON COLUMN … 'PII: …'`, and a
  cross-tenant zero-rows test generated beside every RLS policy (ECC `healthcare-phi-compliance`).
- The seven security triggers: authn/authz, user input, DB query, FS path, external call,
  crypto, secrets (ECC). Six click-path bug patterns (ECC). 40×40 px hit targets;
  `tabular-nums` on counters; the hydration family as one line and one grep; a motion admission
  test (ECC `make-interfaces-feel-better`, `motion-foundations`).
- `rules-distill`'s four admission criteria for promoting a principle to a rule — the bloat
  control every playbook needs (ECC). Every playbook line carries the pinned version it was
  verified against (Vercel Labs).
- Most ECC rules are lint config stated as prose: 7 sentences and 7 deterministic checks came out
  of 9,506 lines, and the checks are worth more than the sentences.

**Requirements and intake**
- Classify the request (spike / bounded / architectural) before the first question, out loud;
  one-way ratchet — hidden complexity upgrades the path, nothing downgrades (superpowers
  `brainstorming`). Decompose before interrogating when several subsystems are named.
- One-way / two-way door registry with stable option keys; registry primary, keyword patterns
  fallback, default to asking (gstack). The decision-brief format: ELI10, stakes, ≥2 pros / ≥1
  con, exactly one `(recommended)` (gstack).
- Split, don't drop: a UI cap on options must never become a product decision — a real
  transcript shows an agent trimming the user's fifth option to fit a four-option picker
  (gstack tests, row 19).
- User-owned fields are absent from the model's output schema, not merely protected by a rule
  (task-master). `datamark()` — neutralise stored user text at the render boundary, because a
  write-time denylist cannot (gstack). Scan at the sink on the exact bytes; a three-tier gate
  whose top tier no flag can skip; the audit-sink invariant as a named test.
- Session-kind classification before asking: spawned auto-chooses, headless blocks, interactive
  falls back to prose (gstack tests).

**Plans, packages and agents**
- `Consumes` / `Produces` on every package with a bipartite completeness check; global
  constraints copied verbatim into every package prompt; a package boundary is the smallest unit a
  gate could independently reject; a `No Placeholders` rejection list (superpowers
  `writing-plans`). Every package carries a "NOT building" list; a Parallel/Depends column; the
  No-Prior-Knowledge test as the contract's acceptance criterion (ECC `prp-*`).
- Capability separation by tool grant — reviewers get no Write, planners no Bash; a lint that
  greps an agent body for tools absent from `tools:` (ECC agents — ECC needs it and lacks it).
- Delegation Completion Contract; a pre-created handoff skeleton with fixed headings filled
  `Pending`; four-part agent brief — scope, goal, explicit constraints, output shape (ECC,
  superpowers). The reviewer receives the artefact and the criterion only, never the build
  transcript (ECC `council`).
- Two packages may build in parallel exactly when their file plans are disjoint (ECC). Package
  lifecycle as a declared transition table; the terminal state reachable only by an explicit
  call; "already satisfied" as a first-class outcome (task-master).
- Ship the architecture to each package as a token-lean codemap, not a JSON dump (ECC
  `update-codemaps`). Content-hash cache keys instead of identity keys (ECC).
- Personas measure negative; separation measures positive; at most three preloaded skills;
  procedures not principles (the architect-agent ADR's sources, corroborated by ECC's 68
  agents being three templates over a severity taxonomy).

**Budgets, timeouts and meters**
- A relative-ratio regression *and* an absolute hard cap, both present; overrides are a reason
  string in an audited log, never a boolean; a timeout derived from the plan's worst case times a
  margin, from a live census (gstack tests). An unpriced model must be a refusal or a pessimistic
  bound, never $0 (gstack's own defect, inverted).
- Never render a missing value as a good value: trusted / unverified / unknown / error; a zero
  from a broken pipe reads as good news (gstack). Spend limits enforced outside the model;
  audit-log refused and halted runs, not only successful ones (ECC `llm-trading-agent-security`).
- Receipt before send, and a fail-open/fail-closed polarity table asserted exactly; hermetic
  child environments with no `...process.env` spread (gstack tests — "three burned suites").
- The harness is part of the instrument: a shared working directory, an arm name in the path, a
  method mounted for every arm, and a usage payload never captured each poisoned a paired
  comparison here, on 2026-09-02 (our own measurement, [[subagents]]).

**Context and tokens**
- Retrieval, not packing: a code graph answers "what calls what" for a few thousand tokens where
  a scan costs hundreds of thousands — measured 79.6× on one code repo with a 48–713× spread,
  0 LLM tokens when code-only, and a ~240-query payback if the semantic pass is used (Graphify,
  Scargall). Forcing graph context into every call can cost more: Graft's controlled +42% tokens
  over 162 runs. Ours, observed: a full session with zero graph queries and ~25 section-index
  queries, because the questions were about documents.
- Progressive disclosure: a description in the always-loaded index, the body on demand; ECC
  has none and pays a 190-line median per skill. Path-scoped rules over one big steering file
  (BASE's idea, Claude Code's built-in mechanism). Condense repeated identical injected blocks
  after N occurrences (ECC `gateguard`, needs an eval).
- Compression tools (Headroom, OmniRoute's Caveman) change what the model sees; never in a
  measured path. AXI's ten CLI-output principles — terse output, 3–4 fields by default,
  definitive empties, structured errors — are a checklist for any tool we expose.

---

## 4 · What was rejected, and the reasons that recur

| Reason | Instances |
|---|---|
| **Licence** | claude-task-master (MIT + Commons Clause, no right to sell); `multica-ai/andrej-karpathy-skills` (207k★, **no LICENSE file**, not by Karpathy); BASE (PolyForm Noncommercial); OpenMontage (AGPL); Origin UI → coss.com/ui (MIT/AGPL by directory); Nemotron free endpoints (logged, trial terms) |
| **Archived or dead** | `gsd-build/get-shit-done` (archived, now a redirect); `steipete/claude-code-mcp` (archived); crystaldba/postgres-mcp (no commit since Jan 2026) |
| **Personas without evals** | agency-agents (230 prompt files, 150k★), gstack's `plan-*-review` family (8,100 lines of taste), 40 of ECC's 68 agents (three templates), task-observer and `claude-code-setup` as *described* by their videos |
| **A vector index on a deciding path** | claude-context; pgvector in the predecessor; Ruflo's AgentDB *as a product component*; Pinecone on a starter list |
| **Hosted memory** | claude-mem (syncs to cmem.ai by default), supermemory the service, the MCP registry's memory servers ("every one puts our knowledge base on someone else's server to solve a problem a local file already solves") |
| **Packing** | repomix — "the anti-pattern with a CLI" |
| **Self-grading** | ECC `agent-self-evaluation` (shipped beside `gateguard`'s proof that it does not work); Prime Agent's `/refine` as a harness; ECC `gan-style-harness`'s weighted composite (its own rubric skill forbids it) |
| **A whole competing harness** | ECC and gstack as installs, Goose and Ruflo and Prime Agent as the build loop — mined, never adopted wholesale; "adopting it means adopting its opinions wholesale, which is the opposite of the ADR discipline" |
| **Unsupported routing** | every gateway to non-Claude models, by Anthropic's own page; usable only as a non-comparable arm |
| **Installers and auto-run** | `npx skills add`, `llm install`, hamelsmu's evals pack, hooks that run unbundled scripts on every edit — the fourth gate reads code first, always |
| **Star counts and listicles as evidence** | superpowers reported at "94,000+" against 277,967; a repo slug that does not exist recommended in three lists; the same script travelling between creators in the Nemotron and find-skills pairs |

---

## 5 · What the harvest taught about harvesting

From `pipeline/LESSONS.md` and the STATUS log, all measured on this repository's own waves:

- **Practitioner and framework repos beat vendor repos beat lists.** Wave 9 over five
  practitioner sources: 10 candidate methods, 7 built. Vendor repos: polished verticals, ~0
  talents, one knowledge note. Awesome-lists: 277 seen, yield 0.00 — they are indexes.
- **Building in the loop beats harvesting more.** One parallel build wave: yield 1.0 against
  harvest waves' ~0.
- **Deep re-read beats description-only triage.** A re-audit that opened files found 10 validated
  talents where surface triage found 0; the eight-repo pass was 8-for-8 on adoption verdicts
  and **0-for-8 on mineable content, because nobody opened the files** — the single most useful
  item in that pass sat in a test file of a repository dismissed for its marketing copy.
- **Measure a producer by its own output.** `adopted/seen` scored the best harvest source at
  0.00 because adoption happens in a later wave; a metric that contradicts a trusted lesson is
  the thing to suspect.
- **Verify the invocation form, and which SURFACE it belongs to.** A pilot wrote
  `graphify extract … --obsidian`, which is ignored; a curator pass concluded "doesn't work";
  `graphify export obsidian` works. Settled 2026-09-04 against the v8 README: the tool has two
  surfaces, and `/graphify … --obsidian` **is** documented — as a *skill* flag, not an `extract`
  flag ([[graphify-features]]). Three passes, and two of the three errors were about the surface
  or the branch of the documentation, not the feature.
- **Read the number's denominator.** "90% of Block's code" was one engineer's own lines;
  "99% fewer tokens" was five structural queries against a grep nobody runs; "4× cheaper" was a
  best case against a controlled +42%; "F1 unchanged" measured edit localisation, not retrieval.

---

## 6 · Where the detail lives

`knowledge/notes/` (the wikilinked pages above) · `intake/2026-08-30-agent-and-skill-material/scio/docs/{ECC-MINED,TOOLING-SCAN,SKILLS-LIBRARY}.md` and `docs/mined/*` (ten verdict tables, ~250 rows) · `catalog/{catalog.json,CATALOG.md,SHORTLIST.md,first-wave.md,second-wave.md}` · `pipeline/{LESSONS,CURATION-LESSONS,STATUS}.md` · `intake/wave*.md` and `intake/ecc-reaudit.md`. Query with `knowledge/kb.py find "<name>"`.

Two policy pages compiled from this landscape on 2026-09-02: [[token-economy-playbook]] (what is measured about saving tokens, ranked) and [[model-routing-free-and-local]] (which jobs may leave Claude, and the mechanics per arm).
