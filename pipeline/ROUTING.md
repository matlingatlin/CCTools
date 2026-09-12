# Routing table — deterministic job → talent chains

Auto-invocation by description handles single-talent picks. This table is for the
orchestrator's **multi-step jobs**, where the brain deterministically chains talents
(the `plan-orchestrate` pattern). Each row: a job the piano runs, and the ordered
chain of talents. New talents are wired in here as they are adopted.

| Job | Ordered talent chain |
| --- | --- |
| **Harvest a GitHub repo** | clone → (code-heavy? `graphify-harvest` to build+query a code map instead of reading files) → `deep-reading` per component → dedup gate (`skill-scout`) → talent-worthiness gate → security read → `eval-harness` → adopt |
| **Ingest a research paper (PDF)** | `pdf` (extract) → `deep-reading` (abstract→method→results→limits) → `research-methodology` (cite, cross-check) → talent-worthiness gate → knowledge note or author talent |
| **Process a "top 10" list / web page** | WebFetch/Playwright → credibility filter → `deep-reading` → dedup gate → sort into intake |
| **Author a new talent from an insight** | reuse-first (`skill-scout`) → copy the matching `templates/` scaffold → `writing-plans` → `writing-skills` → `eval-harness` + `santa-method` → `verification-before-completion` → `talent-deploy` (wire + reload) |
| **Adopt an existing talent from a repo** | `agent-surface-security-audit` (PASS/SANDBOX/REJECT) → dedup gate → talent-worthiness gate → `eval-harness` (baseline-vs-with) → `talent-deploy` (wire + reload) + catalog decision |
| **Curate the library (database 2)** | `library-curator` (score → fan out one auditor per talent by RUNNING `pipeline/workflows/curate-wave.workflow.js` (the `factory` method made executable): test-coverage/description/quality/portability/freshness, apply reversible fixes + write missing `evals.md`, propose merge/prune) → coordinator commits + surfaces proposals (human gate) + appends health scorecard |
| **Generate search terms / sources / entities** | `research-scout` (core domains default; bonus areas when they yield a talent) → write to `frontier.json` |
| **Settle which unit owns a contested job (whole library)** | `capability-routing-table` (enumerate every category → claimed job from each description → cluster contested jobs → discriminator + negative triggers naming a destination → fix BOTH ends) → proposals to a human for any removal |
| **Reconcile docs after a change merges** | `doc-claim-reconciliation` (extract falsifiable claims from the diff → search every doc across D1-D5 with a positive control per dimension → disposition per (claim x document): fix / supersede / propose / out-of-scope → ledger artifact proving each step RAN) → ADRs are superseded, never edited |
| **Run a maximally-parallel wave** | `/piano` plans the work (scout/harvest/build items from frontier+LESSONS) → runs `pipeline/workflows/factory-wave.workflow.js` (the `factory` method made executable: size fleet → fan out) → coordinator commits + `talent-deploy` + `wave-reflect` |
| **Run a wave safely** | `loop-design-check` (stop-condition + anti-spin) → `agent-blast-radius-guard` (bound damage, gate irreversible ops) → `cost-aware-model-routing` (tier + budget ceiling) → `parallel-execution-optimizer` (lane matrix) → `dispatching-parallel-agents` → coordinator merge/commit → recovery on stall |
| **Learn from a wave (self-improve)** | `wave-reflect` (append `metrics.jsonl` → recompute `LESSONS.md`: source-yield, prune/sharpen flags) — read back at next wave's step 1; feed source-yield to `research-scout`; hand each **sharpen** flag to `skill-description-optimizer` |
| **Sharpen a vague request before acting** | `prompt-refinement` (objective + acceptance criteria + constraints + format) → then `writing-plans` to plan the now-clear work |
| **Make a consequential go/no-go or A-vs-B decision** | `decision-council` (frame criteria → N blind lenses → synthesize + keep dissent) → record ADR in `docs/decisions/` |
| **Ingest a verified source into the knowledge base** | `llm-wiki-ingest` (raw → triage via `kb.py find` → quote → page in schema → cascade → INDEX/SOURCES/STATUS → `kb.py check`) → coordinator commits |
| **Clean the knowledge base** | `kb-curator` agent (`kb.py lint --json` + `contradictions` → safe fixes → one-way links closed with a sentence → contradictions/duplicates as proposals) → human gate on merges/deletes → coordinator commits |
| **Verify before shipping anything** | `verification-before-completion` → `santa-method` (adversarial) |

## How the brain uses this
1. Read `frontier.json` (queues + seen-set) → pick the next job.
2. Look up the job here → run the ordered chain, each step delegating to a talent.
3. Apply the four gates (CLAUDE.md) at the marked points.
4. Coordinator commits results; log to `STATUS.md`; feed findings back to `research-scout`.

## Maintenance
When a new talent is adopted, add/replace it in the relevant chain and in the
CLAUDE.md capability map. When two talents overlap, the librarian differentiates
their descriptions so only one triggers per job.
