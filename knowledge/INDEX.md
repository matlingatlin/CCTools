# Knowledge Index (Map of Content)

Start here. Each note is self-contained, carries its sources in frontmatter, and
links to related notes with `[[wikilinks]]` (Obsidian-compatible). Every claim
carries a source URL, a fetch date, and a status (`verified` / `unverified` /
`outdated`).

## 0. The layers, and the one index
- **`knowledge/notes/`** — the wiki layer: LLM-written, wikilinked, sourced, verdict per claim.
- **`knowledge/raw/`** — the raw layer (`MANIFEST.md`): byte-identical imports from the other
  repositories and branches with provenance, never edited; the first raw import is
  `intake/2026-08-30-agent-and-skill-material/`. Together they hold, by content hash, every
  knowledge-bearing file of Scio and hello-world on every branch as of 2026-09-02.
- **`knowledge/VAULT.md`** — open the repository root as an **Obsidian vault**; `.obsidian/` is
  committed, graph view coloured by layer, artefacts filtered out. Graphify's `export obsidian`
  is for code graphs and is documented there.
- **`knowledge/kb.py`** — the one index over all of it (notes, raw, intake, pipeline, talents):
  `build` · `find "<words>"` · `read "<heading>"` · `stale [days]` · `links` · `selftest`.
  Rebuilt from files in half a second, no model call, `kb.db` gitignored. Query it before
  opening a file: a section costs a fraction of the document it sits in.

## 0b. The summary page
- [[third-party-landscape]] — **start here for "what do we know about other people's skills,
  agents, plugins and tools".** Every third-party source in this knowledge base, what each
  yielded, the ~200 mechanisms taken grouped by theme, what was rejected and why, and what the
  harvest taught about harvesting. A compiled page; every row points at its evidence.

## 0c. The two policy pages
- [[token-economy-playbook]] — **"be as token-aware as possible — what do we know?"** Three token
  sinks, every measured number graded (graphify 79.6× with its spread and 240-query payback,
  Graft +42%, the session with zero graph queries, Scio's 65% repeated bytes, 459 < 512, 77%
  untouched files, −51% / −100%), caching mechanics per model, prices dated, and an eight-point
  policy ranked by size.
- [[model-routing-free-and-local]] — **"can we route to free or local models?"** Four arms
  (native · Anthropic-compatible hosted · free tiers through a router · Ollama), what each
  silently loses, the 50-requests-a-day arithmetic against a 29–79-call build, a jobs × arm
  matrix for building Scio, inside Scio, and in generated apps, and seven rules for any routed run.

## 0d. Added 2026-09-02 from lookups, video batches and the day's questions
(listed by the kb-curator's first lint pass; each line is the note's own title)
- [[adversarial-plan-review-claudex]] — Claudex Loop — a rival model attacks the plan, round after round, and never grades its own work
- [[best-local-llm-2026-09]] — The best LLM you can run locally, August–September 2026 — by hardware tier, from the model cards
- [[claude-code-ecosystem-plugins]] — The Claude Code plugin stack the videos sell — what each one actually is
- [[glm-5.3-local]] — GLM-5.3 and GLM-5.3-Flash — what "run it locally" actually costs, and the Claude Code path
- [[harness-over-model-prime-agent]] — Harness over model — Prime Agent's self-refining harness, and the swarm meta-harnesses
- [[learning-resources-agents]] — Learning resources on agents that checked out — CS329A, OpenMAIC
- [[llm-wiki-pattern]] — Karpathy's LLM Wiki — raw/, wiki/, schema; ingest, query, lint
- [[local-finetuning-layer-streaming]] — Soup — fine-tuning an 8B model on a 4 GB laptop GPU by layer streaming, and a retraction done right
- [[long-document-ocr]] — Long-document OCR without chunking — Baidu's Unlimited OCR (R-SWA, constant KV cache)
- [[loop-engineering-and-fable-prompting]] — Loop engineering (LOOPS.md) and Anthropic's own Fable 5 prompting rules
- [[model-agnostic-agent-harnesses]] — Model-agnostic agent harnesses — Goose, and running Claude Code against other models
- [[production-site-checklist]] — What a vibe-coded site is missing — a 19-item production checklist
- [[prompt-patterns-kernel]] — The KERNEL prompt pattern — what it says, and what its numbers are worth
- [[skill-authoring-eval-methodology]] — Skill authoring + eval methodology (from Anthropic's official skill-creator)
- [[system-prompt-transparency]] — "System prompt leaks" — Anthropic publishes the claude.ai system prompt, so what a leak adds is the unpublished tool layer
- [[temporal-kg-agent-memory]] — Temporal knowledge-graph agent memory (Graphiti/Zep)

## 0e. Added 2026-09-04 — one source, and what running it settled
No new page: a forwarded Instagram carousel on graphify → Obsidian was triaged as an **update**
and extended four existing pages instead of starting a rival. What it settled, and where:
- the tool has **two command surfaces** — `/graphify … --obsidian` (skill) vs `graphify export
  obsidian` (CLI) — which closes a three-pass correction chain → [[graphify-features]],
  [[graphify-assessment]]
- the repository's **default branch serves a v1-era README**; this KB is written against v8 →
  [[graphify-features]]
- the **licence changed**: MIT through v7, Apache-2.0 on v8 and on PyPI 0.9.53 →
  [[graphify-features]], [[third-party-landscape]]
- the vault's on-demand export was **run rather than quoted**: 5,401 notes in 2.4 s, node notes
  median 42 words, and 1 of 380 `source_file` paths resolves in the repo the vault sits in →
  `knowledge/VAULT.md`
- `graphify export wiki` **ignores `--dir`** and writes beside the graph — into `intake/`, here
  → [[graphify-features]], `.claude/skills/graphify-harvest/SKILL.md`
- a generated page whose source cannot be opened from the page is a stub with a footnote →
  [[llm-wiki-pattern]]
- raw kept at `knowledge/raw/instagram-graphify-obsidian-2026-09-04/` (frame text, both READMEs)

## 1. Orientation — general best practice
- [[claude-code-extension-layer]] — **hub note.** Which feature to use when, how
  they layer, context costs, "build your setup over time". Read this first.

## 2. Claude Code mechanics (one note per feature)
- [[claude-md-and-memory]] — CLAUDE.md, `.claude/rules/`, auto memory
- [[skill-anatomy]] — SKILL.md format, frontmatter, where skills live, loading & token economics
- [[subagents]] — isolated workers, frontmatter, fork, foreground/background, **documented limits** (15,000-token shared description budget, depth 3, 20 concurrent — and what is explicitly undocumented)
- [[dynamic-workflows]] — scripts that orchestrate many subagents at scale
- [[mcp]] — connecting external tools/services (transports, scope, tool search, security)
- [[hooks]] — deterministic lifecycle automation and the enforcement layer
- [[plugins-and-marketplaces]] — packaging and distributing all of the above

## 2b. Building an agent
- [[agent-design-template]] — **the shape.** Six loading tiers inside one agent
  (identity / functions / conditional rules / knowledge / templates / walls), where
  rules, templates and references belong, the composition patterns between agents
  with verdicts, and the measured constraints on all of it. Read with
  [[claude-code-extension-layer]], which decides *which feature*; this decides *how to
  layer one*.

## 2d. Building agents against the API (a different craft)
- [[api-agent-loop]] — the Messages-API agent loop: `stop_reason` control flow, the
  parallel-tool rule, tool schemas, and — more useful — the seven things Anthropic's
  own tutorial does **not** cover (error contract, budgets, testing, approval gates).
  Plus Tool Runner, and why it is not the Claude Agent SDK.

## 2e. Anthropic's own agent writing
- [[effective-agents-anthropic]] — the six patterns, the two arguments against
  building an agent at all, and the tool-design section: **"we actually spent more
  time optimizing our tools than the overall prompt"**, plus poka-yoke — change the
  argument so the mistake cannot be made.
- [[managed-agents-architecture]] — brain / hands / session decoupling; the
  credential pattern where **the token is never reachable from the sandbox**; and a
  measured case of a harness workaround outliving the model behaviour it fixed.

## 2c. Prior art — what other people built
- [[agent-builder-prior-art]] — three third-party agent/skill builders read in full
  against Anthropic's own guide. They solve three different problems under one name;
  none cites evidence or tests against a baseline; one has **lifecycle governance**
  (versioning, rollback, quarantine, expert-vs-operator separation of duties) that we
  do not.

## 3. Authoring & quality (how to build well)
- [[anthropic-skill-authoring-contract]] — **Anthropic-only.** What they STATE about the
  body, bundled files, evals and baseline, separated from what they DO — with 11 shipped
  skills measured. Carries the 13 confirmed gaps where Anthropic says nothing, and the
  four unreconciled body-length figures. Read before authoring or gating a skill.
- [[skill-authoring-best-practices]] — conciseness, the description rule, progressive disclosure, testing
- [[testing-skills-methodology]] — pressure-testing skills with subagents (RED-GREEN-REFACTOR)

## 3b. Domain evidence — what is measured vs merely repeated
Added 2026-08-28. Every claim in these five carries **MEASURED** (a study with numbers,
read) or **REPEATED** (widely asserted, no measurement found). Written because the
knowledge base held only Claude Code mechanics and no domain knowledge at all, which is
why an architect agent had to be written from recall.
- [[ideation-and-idea-selection]] — brainstorming's founding claim is unmeasured; the
  chain breaks at **selection**, not generation
- [[design-fixation-and-anchoring]] — reading the existing system reproduces it; warnings
  fail and can backfire; **self-generated first ideas anchor harder than provided ones**
- [[llm-idea-generation]] — diversity collapse, the model cannot rank its own ideas,
  starve the generator / saturate the evaluator
- [[requirements-discovery]] — differentiated perspectives beat undirected review by
  ~35%; **generic checklists buy nothing**; the rewrite literature is empty
- [[architecture-evidence]] — the measured failure modes, and the design literature we
  are missing

## 4. Tooling decisions
- [[graphify-assessment]] — Graphify (codebase→graph): pilot on harvested repos code-only; skip for our KB; the obsidian correction chain, closed
- [[graphify-features]] — full Graphify capability reference (CLI, exports, integrations, versions); the two command surfaces, the default-branch README trap, and the MIT→Apache-2.0 licence change

## 5. Working methods
- [[long-text-comprehension]] — genuinely understanding long documents (basis for the deep-reading skill)
- [[research-methodology]] — multi-source research workflow with citations (basis for Phase 2)

## Built / adopted skills (`.claude/skills/`)
- `deep-reading` — multi-pass comprehension skill (built here, v2, evaluated)
- Adopted from source repos (first eval wave, 9/9 passed — see [catalog/first-wave.md](../catalog/first-wave.md)):
  `writing-skills`, `skill-scout`, `skill-stocktake`, `eval-harness`, `santa-method`,
  `verification-before-completion`, `subagent-driven-development`,
  `dispatching-parallel-agents`, `context-budget`
- Adopted second wave (brain-building blocks — see [catalog/second-wave.md](../catalog/second-wave.md)):
  `loop-design-check`, `parallel-execution-optimizer`, `unified-memory`

## The brain (self-playing piano)
- [pipeline/BRAIN-ARCHITECTURE.md](../pipeline/BRAIN-ARCHITECTURE.md) — architecture assembled from proven catalog blocks
- [pipeline/frontier.json](../pipeline/frontier.json) — git-persisted shared state (queues + seen-set)

## Component catalog
- [catalog/CATALOG.md](../catalog/CATALOG.md) — all 469 harvested components, by domain + fit
- [catalog/SHORTLIST.md](../catalog/SHORTLIST.md) — the 111 build-now components
- [catalog/first-wave.md](../catalog/first-wave.md) — first eval wave results + security gate outcomes

## Source log
- [sources/SOURCES.md](sources/SOURCES.md) — every source consulted, with date and verdict
