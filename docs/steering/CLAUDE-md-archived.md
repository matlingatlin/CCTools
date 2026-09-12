> **ARCHIVED, AND NOT STEERING.** This was `CLAUDE.md` at the root of `matlingatlin/skills-repo`,
> where it loaded every turn. It is kept here, off the root, because a root `CLAUDE.md` auto-loads
> and this repository is deliberately inert: nothing in `library/` is installed, so no talent
> loads, triggers or routes, and the capability map below routes nothing on arrival.
>
> **What is still true:** every rule, discriminator and boundary. The map says which unit owns
> which job, and that does not depend on where the files sit. It names **79 talents** — measured
> 2026-09-12 by resolving each backticked name against the library, not counted by hand.
>
> **What is no longer true, and was corrected rather than deleted:** the activation paths. The
> library moved from `.claude/skills/`, `.claude/agents/` and `.claude/skills-candidates/` to
> `library/skills/`, `library/agents/` and `library/skills-candidates/`. Every such path below
> has been rewritten to where the file actually is. To put a unit back into service, copy it
> under a project's own `.claude/` — see this repository's README.
>
> The talent-factory loops it describes (`/piano`, `library-curator`) do not run here; the
> pipeline that drove them travelled with it and is in `pipeline/`.

# skills-repo — the self-playing piano

A self-improving **talent factory**. Talents = skills, hooks, subagents, agents,
commands. See `pipeline/SPEC.md` for the full system and `pipeline/BRAIN-ARCHITECTURE.md`
for the build. This file is the standing brain: rules that always apply + a capability map.
Talents auto-load by their own `description` **once installed** — not in this repository, where
nothing is — so the map is a **second routing index, paid every
turn** wherever the library is live — it earns that only through the cross-library discriminators a single description cannot
carry. Cost: `python3 pipeline/queries/context_surface.py`.

**The living brain is `pipeline/BRAIN.md`** — the shared control tower BOTH loops
(`/piano` build/harvest + `library-curator` db2) read at the start of a run and update at the
end. It **connects** their learnings (a lesson by one → an action for the other), **syncs**
their work (ownership so they don't collide), **plans** each loop's next action, and
**optimizes** the whole. Always read it before running either loop.

## Standing rules (always)
- **Count before you fan out.** `W_MAX_AGENTS` in `pipeline/CONSTANTS.md` is GLOBAL and shared
  across loops. It is **4** as of 2026-09-01, measured against a threshold fixed before any number
  existed; the earlier value of 2 came from a CPU formula over a workload that turned out to be
  73% API wait, and its own citation did not resolve. Four is what was measured — 8 and 16 were
  not. Before dispatching agents, call `TaskList` and count what is already running; dispatch only
  up to the cap. This rule exists because on 2026-08-28 the coordinator launched three authors
  against a cap of two, in the same session that built CONSTANTS.md to prevent that drift and
  minutes after reading the file. The cap was not forgotten — it was never CHECKED at the moment
  of dispatch. **This is a convention, not a gate:** no code enforces it, because dispatch has no
  script hook. It is therefore the weakest defence in this repo, and the one most likely to fail
  again. Treat a `TaskList` call as part of dispatching, not as an optional precaution.
- **Four gates before anything becomes a talent:** dedup (not a copy) → reuse-first
  (search our own library first) → talent-worthiness (fills a function we lack) →
  security (read the code; no auto-run/unaudited hooks, no external-CLI installs, no
  credential/network calls). Unsafe → sandbox or skip.
- **Generality (every talent is portable):** a talent MUST be a general, domain-agnostic
  method usable in ANY project — never welded to this repo. Write the method generally;
  put any project-specific paths, names, or wiring (e.g. `pipeline/frontier.json`,
  `register_repo_root`, `library/skills/`) in a short **"In this repo (one instance)"**
  section at the end, as examples, not requirements. The ONLY deliberately project-specific
  talent is `/piano` (it is the app, not a method). Authoring goes through the `templates/`
  scaffolds + `factory`, both of which produce general-with-an-example talents by default.
- **Dogfood:** use our own talents on our own work (map below). Don't hand-roll what
  a talent already does.
- **Coordinator commits; agents produce.** No parallel git writes to this repo.
- **A verified fact lands in `knowledge/notes/` in the same turn it is verified —
  not when someone asks.** This rule exists because it was broken twice in one session:
  documented limits and research findings were reported in chat and left there, and the
  user had to ask both times. The trigger is not "the work is finished"; it is
  **"I now know something I did not know, and I checked it."** Fetched a doc page,
  read a paper, measured the repo, got a number back from a tool → note it, with the
  source, the fetch date, and a per-claim **MEASURED / REPEATED** verdict. A finding
  that lives only in a chat message is lost at the next compaction, and it is lost
  silently. Reuse-first applies: check whether an existing note owns the topic and
  extend it rather than adding a rival, and when a new note names neighbours, make each
  neighbour name back — parallel authoring produces one-sided links structurally.
- **Human gate ∝ autonomy:** auto-sharpen descriptions is fine; merge/delete/anything
  irreversible asks the user first.
- **Test before adoption (definition of done = built + TESTED + documented + committed):** a
  talent is COMMITTED as a candidate in `library/skills-candidates/` (never loaded, so it cannot
  trigger) once it is filled, code-checked and reviewed once (chain 4.0.0, candidate mode); it is
  ADOPTED into `library/skills/` only after the promote build measures it. Measured 2026-09-03:
  the reviewer is red on every text including adopted ones, and the arms are the cost - so the
  cheap checks gate the commit and the measurement gates the adoption. No talent is adopted until SPECIFIC tests for it are authored and pass — a BLEND, all
  tailored to that talent: ~half normal/representative (the everyday job) and ~half clever/
  adversarial (traps, planted-defect/pressure, edge), plus a negative-trigger. Run
  `eval-harness` baseline-vs-with (the clever ones designed so the baseline fails; the normal
  ones confirm everyday behavior), persisted as `library/skills/<name>/evals.md`. Not only
  traps, not only happy-path. Quality-review is not the test. Untested → not shipped.
- **Drop ONLY what fails its tests.** The sole removal criterion is a talent that doesn't beat
  baseline and can't be fixed. NEVER prune a talent for being unused, niche, or rarely
  triggered — this is a cross-project library; a method unused today may be exactly what a
  future task needs. Keep it; test it; only a broken talent is dropped.
- **Everything commits to git.** State lives in `pipeline/frontier.json`, not in a session.
- **Never put backticks in a `git commit -m` string.** Bash executes them: the words vanish
  from the message and the commit lands quietly mangled. This has now happened twice (1b58352,
  90cb4f1). Write commit bodies to a file and use `git commit -F`, or quote with single quotes
  and name fields in plain words ("the adopted field"), never `` `adopted` ``. Do NOT rewrite
  pushed history to fix a cosmetic message — the blemish costs less than a force-push.
- **Collect the data the purpose needs (`pipeline/DATA.md` is the contract).** Learning is #1;
  learning needs data. Every wave/pass records its `metrics.jsonl` row with MEASURED
  `wall_clock_s` + `agents`, and ticks the ledgers (`pipeline/ledgers/`: talent lineage,
  per-scenario evals, categorized rejections, human-gate proposals). Capture cost, time, and
  lineage LIVE — they cannot be reconstructed later. Never fake a measurement: `spend_measured`
  stays `null` until a metered path exists. The analysis layer is deferred; the collection is not.

## Domain scope
- **Core (default, always):** AI, ML, LLMs, agents/orchestration, software engineering,
  data, IT/infra, tooling, developer workflows, NLP, prompt engineering.
- **Bonus/connected (when it yields a real talent):** psychology, cognition,
  linguistics, design, decision science.

## Capability map — the DISCRIMINATORS, not an index (dogfood these)
Not a list of what exists: the descriptions above are that. A line earns its tokens only by naming
what one description cannot — which sibling owns a job, a boundary, a chain. **Absence here means
"no discriminator needed", never "no talent for this."** Test + the 25 lines cut 2026-09-12:
`pipeline/decisions/2026-09-12-capability-map-earns-its-tokens.md`.
- Understand a long doc/paper/repo → `deep-reading` (PDF via the `pdf` skill first)
- Research a topic with citations → `literature-review`, `market-research`, `research-methodology` (note)
- Find prior art before building → `skill-scout` (+ reuse-first gate)
- Test a talent / feature → `eval-harness`; adversarial verify → `santa-method`
- Plan then execute → `writing-plans` → `subagent-driven-development`
- Fan out work → `dispatching-parallel-agents`; avoid write collisions → `parallel-execution-optimizer`
- Debug a failure → `systematic-debugging`; agent-run failure → `agent-introspection-debugging`
- Watch the context budget → `context-budget`; token-lean codemaps → `update-codemaps`
- Navigate a code-heavy harvested repo cheaply → `graphify-harvest` (code-only graph, 0 LLM tokens; skip for markdown-only repos and our own KB)
- Select the most relevant files/symbols within a token budget for an LLM → `repo-map` (PageRank-ranked; context selection, vs graphify-harvest's navigable graph)
- Find functions that serve the SAME INTENT under different names → `semantic-duplicate-sweep` (intent comparison; `repo-map`/`graphify-harvest` build structure, they do not compare meaning)
- Robustly apply model-produced code edits (fuzzy search/replace, diff formats) → `apply-llm-edits`
- Put a verified source into the knowledge base in the one shape every page has (raw kept, triage,
  quote before write, verdict, cascade, index + log, lint) → `llm-wiki-ingest` (measured 2026-09-03, first v3
  build, ship; `skill-knowledge` is for claims bundled INTO a skill)
- Walk the knowledge base and fix what rotted - dangling/one-way links, unlisted pages, schema drift,
  stale fetches, contradictions and duplicates as proposals → `kb-curator` — **an AGENT at
  `library/agents/`** (candidate; runs `knowledge/kb.py lint --json` first; `library-curator` is for
  the talent library, not the wiki)
- Review a whole artefact for internal contradictions in ONE pass - every step-rule, step-step, step-check,
  description-body, file-BOM and claim-rationale pair as a row → `artifact-consistency-sweep`
  (**candidate in `library/skills-candidates/`, NOT adopted — it does not load and cannot trigger**;
  `santa-method` is two reviewers converging. Its build history and open findings: its own `evals.md`)
- Decide whether a remembered fact can still be BELIEVED — user-asserted vs system-observed, stamped as-of, re-checked before it steers a decision → `memory-provenance-separation` (governs a row's origin and freshness, not its storage; the two compose — `unified-memory` writes the row, this one says what it means)
- Audit the talent library → `skill-stocktake` (reports THAT units overlap and grades them)
- After a diff merges, find every doc still asserting the OLD behaviour and gate completion on reconciling them → `doc-claim-reconciliation` (works per claim x document, not per file; `update-codemaps` regenerates GENERATED maps, `steering-doc-pruning` cuts what a steering file has not earned, `verification-before-completion` checks the work rather than the docs about it)
- Decide WHO OWNS each job across a whole library, and prove it with negative triggers → `capability-routing-table` (finds what a listing cannot show: units that cannot be invoked at all, units that fell out of the table, boundaries asserted from only one end. Its unvalidated premise is stated in its own premise section)
- Generate search terms / sources / entities for a harvest wave → `research-scout` (`disable-model-invocation`, so it will NOT auto-trigger — invoke by name; chains in `pipeline/ROUTING.md`)
- Build an MCP server / agent harness → `mcp-server-patterns`, `agent-harness-construction`
- Security-audit a talent/config before adopting (the 4th gate) → `agent-surface-security-audit`
- Bound an autonomous run's damage → `agent-blast-radius-guard` (pairs with `loop-design-check`)
- Before an agent runs unattended, inject tool/infra faults and grade whether it degrades HONESTLY → `agent-fault-injection` (stubs only, never live endpoints; `agent-introspection-debugging` is for after a real run failed)
- Make each real-world side effect safe to re-run after a crash/retry/resume (idempotency keys, plan-then-apply, action ledger) → `idempotent-action-design` (blast-radius-guard says whether it MAY run; this says what happens when it runs twice)
- Pick the cheapest model tier + cap spend → `cost-aware-model-routing` (dollars; tokens → `context-budget`)
- Decide WHAT to drop when a budget will not cover the plan → `budget-cut-triage` (consumes a budget already known short; `cost-aware-model-routing` sets one, `context-budget` ranks components)
- Author a talent from the right scaffold → `templates/` (technique/orchestrator/agent/command)
- Deploy an added talent so it activates + is routed → `talent-deploy` (wire + `register_repo_root` reload)
- Run ANY task as a parallel fan-out (one agent per work item, capped) → `factory` (domain-agnostic; `/piano` drives the talent-factory wave through it)
- Improve perf/cost/score by measurement, not guessing → `measured-optimization-loop`
- Find WHICH stage of a multi-step pipeline costs the score, before optimizing any of them (oracle-substitute each stage, rank by headroom) → `stage-ablation-attribution` (localize first; `measured-optimization-loop` then tests the chosen fix)
- Catch silent quality drift in INCOMING data at the boundary (profile, derive contract, assert at ingest, drift thresholds) → `data-contract-assertions` (the dataset arriving; `structured-llm-extraction` validates a model's output)
- Build + validate an LLM-as-judge before trusting its scores → `llm-judge-calibration`
- Choose WHICH production examples become the eval set — collapse templated near-duplicate FAMILIES rather than exact matches, set a per-slice reporting floor so a rare slice is not reported at an interval it cannot support, and seal the holdout with a look log → `eval-set-curation` (you have too much data; `synthetic-eval-data-generation` is for having none, `error-analysis-taxonomy` clusters traces to find WHAT went wrong rather than which to keep)
- Decide when a feature should DECLINE/escalate instead of answering — and prove the confidence signal SEPARATES right from wrong (AUROC or decile buckets) before any cut is trusted, then set the cut against a precision target and a coverage floor agreed first → `abstention-threshold-design` (uncertainty-driven; `hybrid-parse-escalation` escalates on parse failure for cost, `llm-judge-calibration` validates a judge against humans)
- Check a patch covers the full symmetric/multi-variant contract → `integration-contract-completeness`
- Gate a GENERATED LLM app's prompt/model changes with assertion-based CI evals → `llm-eval-harness` (distinct from `eval-harness`, which tests our own talents)
- Adversarially scan a GENERATED LLM app for vulnerabilities before ship → `llm-redteam-scan`
- Extract typed, schema-validated data from an LLM (validation-retry / reask loop) → `structured-llm-extraction`
- Explore intent + design BEFORE implementing any feature/change → `brainstorming`
- Integrate a finished feature branch (retest → merge/PR menu) → `finishing-a-development-branch`
- Request a code review via a fresh reviewer subagent → `requesting-code-review`; act on review feedback (verify before implementing) → `receiving-code-review`
- Build a persistent file-based multi-agent OS on Claude Code → `agentic-os`; run the OPS around a long-lived hosted agent system (lifecycle/observability) → `enterprise-agent-ops`
- Fix the deciding metric, threshold and stop rule IN WRITING before a result is visible, so the
  result cannot move the bar → `preregistered-decision-rule` (`decision-council` is for an
  undecided A-vs-B with no measurement; `measured-optimization-loop` iterates against a metric
  already agreed)
- Diff an inherited handoff brief against the ORIGINAL request, hunting requirements it has gone
  SILENT about → `inherited-context-drift-audit` (`unified-memory` stores state and trusts it;
  `agent-introspection-debugging` diagnoses a run that already visibly failed)
- Hold a correct technical position when a person pushes back with authority, a deadline or
  prior approval rather than evidence → `concession-audit` (decides whether to concede, and
  records the finding as standing when only pressure was offered; `receiving-code-review` is
  for evaluating an incoming reviewer change, `verification-before-completion` for your own claims)
- Audit whether a red-to-green result was bought by WEAKENING the check rather than fixing the
  code (loosened assertions, skipped tests, widened tolerances, suppressions, re-recorded
  snapshots) → `oracle-weakening-audit` (grades assertion STRENGTH via mutation on changed code;
  `test-coverage` measures reachability and stays green when an assertion is gutted)
- Review a RETRIEVAL path end-to-end before trusting its answers (raw top-k reaching the LLM,
  whether the rerank/filter actually reorders or is a pass-through, embedding model+version
  matched at index and query time, insufficient-context fallback, citations bound to retrieved
  chunks, retrieval-metric coverage) → `rag-pipeline-reviewer` — **an AGENT, at
  `library/agents/`, not `library/skills/`.** The retrieval path itself; `mlops-production-review`
  for training/serving code, `llm-eval-harness` for the CI gate mechanism, `llm-judge-calibration`
  to validate the judge producing the faithfulness numbers, `eval-set-curation` to choose the
  queries it runs on
- Change a LIVE schema or deployed interface while two versions of the code run at once
  (expand → dual-write → backfill → switch reads → contract, each phase independently deployable)
  → `expand-contract-migration` (`idempotent-action-design` answers "what if it runs twice";
  this answers "what if two VERSIONS run at once")
- Trim or write a doc an AGENT reads EVERY turn (CLAUDE.md/AGENTS.md/system prompt) → `steering-doc-pruning`
  (no-op test, cache-aware edit cadence, progressive exposure; `context-budget` ranks WHICH component
  eats tokens, this cuts inside one; `writing-skills` authors a load-on-demand SKILL.md)
- Implement against a library/API you must not guess at — pin the exact resolved version, read THAT version's
  source/docs, cite the file+symbol per claim → `source-grounded-implementation` (verifies what the dependency
  actually does; `deep-reading` is for understanding a doc, `external-domain-audit` for auditing against a spec)
- Write or rewrite the FIELDS of a Claude Code skill against a field contract (order, per-field
  inputs, code check then independent reader, description last) → `skill-contract`
  (`writing-skills` authors a skill from scratch; this governs which field is written when, on
  what evidence, and what checks it before the next one starts)
- Prove a skill, prompt or agent change beats baseline (probe first, paired with/without in the
  same turn, expectations written from observed outputs, verdict against a preregistered
  threshold) → `skill-measure` (`eval-harness` runs a suite; this decides what the run must show
  and refuses to move the bar afterwards)
- Decide whether an artefact needs knowledge fetched, then gather, quote, verify and reconcile it
  before bundling → `skill-knowledge` (`literature-review` surveys a field; this asks the narrower
  question of what the OBSERVED gap shows is missing, and gates on a verbatim quote per claim)
- Turn an admitted build package into a tested skill, end to end → `skill-builder` — **an AGENT,
  at `library/agents/`.** It orchestrates the three above and stops at the code gates
  (`pipeline/validate/package_contract.py`, `skill_contract.py`, `pipeline/build/decide.py`).
  Every run it dispatches goes through `pipeline/build/dispatch.py`; two modes — `full` (the
  only one that ships, ~40 min) and `fast` (with-arm only, ceiling `fast_pass`, for iterating)
- Blind a PAIRED comparison so one grader cannot tell which arm produced which answer -
  relabel and reorder per item, withhold the key, tell the grader the labels re-randomise, and
  control the un-blinding with a test a swapped key would FAIL → `paired-comparison-blinding`
  (`llm-judge-calibration` blinds the judge to the GOLD LABEL and validates its scores against
  humans; `oracle-weakening-audit` finds checks loosened to buy a green build)
- Fix the SHAPE of a module/interface that already exists (deletion test, three-way fan-out, is the seam real) →
  `interface-depth-design` (existing surface feels wrong / single-adapter port / leaky abstraction; `brainstorming`
  is for what to build before it exists, `behavioral-spec-mining` for recovering what code does)

For deterministic multi-step chaining see `pipeline/ROUTING.md`.

## Description discipline (why the right talent triggers)
Talents are selected by their `description`. Keep every description: triggers-only
("Use when…"), keyword-rich, third person, and short (cap in `pipeline/CONSTANTS.md`:
`cited`+`decided`, not measured). Its context share moves on its own, so it is not pinned here —
`python3 pipeline/queries/context_surface.py`. Overlapping descriptions cause mis-triggering.
