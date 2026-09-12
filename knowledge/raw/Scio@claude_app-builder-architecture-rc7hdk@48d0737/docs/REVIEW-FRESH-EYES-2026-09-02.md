# Fresh eyes on the app builder — what to build, and how

**Date:** 2026-09-02. **Status:** proposal. Nothing here is decided; the decisions it argues for
are filed as ADR-0002 … ADR-0007 with status *Proposed*.

**Method.** A cold position was written first (`docs/positions/2026-09-02-cold-position-fable.md`)
with nothing read but `CLAUDE.md` and the finding counts. Only then: the as-built index, the
twenty predecessor ADRs, the whole-system as-built, the *State* heading of all seven layers, the
73 untaken decisions in the store, what the reviews missed, and a dated scan of the outside world.
Everything after the cold position is marked **informed** and should be weighed as such.

---

## 1 · The cold position, held against the history

| # | Cold position | Verdict after reading | Evidence |
|---|---|---|---|
| 1 | The product is a spec-to-*verified*-software pipeline; evidence is the surface | **Held, and it is already half-built.** The predecessor verifies more than any competitor and renders four lists of ids | `ARCHITECTURE-AS-BUILT.md` *The pattern that matters most*; `next/LAYER-E` §4.5 |
| 2 | Deterministic where possible, model only for judgement | **Held; it is the predecessor's real asset**, implemented independently in five layers | `ARCHITECTURE-AS-BUILT.md` *The one idea* |
| 3 | One opinionated output stack, deep not broad | **Held.** ADR-0011 fixed Next.js + TS + Tailwind + Supabase; Lovable ships the same family | `01-DECISIONS.md`; Lovable review 2026 |
| 4 | The spec is the contract, provenance per field | **Held, stronger than I wrote it.** `FieldMeta{value, source, confidence, provenance}`, message-id grounding, inference never overwrites a statement | `LAYER-A` §6 Solid |
| 5 | Build is a sandboxed agent loop with real tools and a written stop rule | **Held; the predecessor has the loop but not the sandbox.** `choose_sandbox()` never returns the production provider; Docker is a resource boundary, not a security one | `next/LAYER-E` §3.3 |
| 6 | Ownership means a repository with CI green | **Held; unbuilt.** Deployment is a 501 route table; nothing runs the generated app's own tests or `next build` | `LAYER-F` §6, `REVIEWS-WHAT-WE-MISSED` §3 |
| 7 | Do not rebuild the harness | **Held, with a date.** Claude Agent SDK is GA with hosting guidance for multi-tenant isolation; Managed Agents is beta (`managed-agents-2026-04-01`), not ZDR/BAA eligible | §5 below |
| 8 | Library as a curated registry, not a garden | **Revised.** The registry standard is a *distribution* format; the predecessor's `Contract` is a *matching* model with no counterpart there. Export to the standard, keep `Contract` as the deciding test | `LAYER-D` §6; RETHINK-BRIEF appendix |
| 9 | Scio's own code should be small | **Held; the count tells why it grew.** 22,990 source lines, Layer E 41% by directory, three empty library entries, five placeholder routes | `00-INDEX.md` |
| 10 | Build with the talents; governance from Scio, method from skills-repo | **Held.** 27 Scio skills, 85 skills-repo skills, and the two libraries overlap in three places | §7 below |

Two things the cold position did not see and the history did:

- **The compute-and-drop habit.** Five layers compute an honest signal and nothing consumes it:
  plan validation, `checks_passed`, `compiles`, the allowance, the curation endpoints. That is
  one habit, not five bugs, and it is the cheapest thing in the system to fix.
- **Tests that pass for the wrong reason.** Two confirmed cases. A test double stricter than
  production hid a live cross-tenant read (F-03). Any rebuild inherits this risk the moment it
  writes its first fake.

---

## 2 · What the predecessor is, in one paragraph

A pipeline — intake → understanding → plan → library match → build → design window → promote —
whose *ideas* are good and whose *seams* were never drawn. It computes provenance, validates
architecture before spending tokens, derives interaction scripts deterministically, stamps
package ownership into the DOM, and refuses to regenerate what a user shaped. It also never
reads its own plan validation, keeps its two most valuable gates opt-in, has a matchable catalog
of one entry, a queue state nothing reaches, a Python↔TypeScript seam the code graph cannot
see across, and a post-reveal half that is placeholders. It was built broadly, not carelessly.

---

## 3 · The recommendation

### 3.1 The thesis

> **Scio's output is a repository a developer would have been proud to write, delivered with
> the evidence that proves it — to a person who could not have written it.**

Two customers, one artefact. The buyer cannot code and is judged on nothing. The developer who
opens the repo is the judge, and judges on: structure, honest types, tests that can fail, a sane
schema with tenancy proven, no placeholders, CI green, and a README that says why. The
competitors listed in the 2026 comparisons are described as "excellent for the first 48 hours";
the gap they name is *week three*: does the code survive a schema change, can you leave the
platform, does the price stay sane. That gap is the product.

ADR-0001's wedge — *founders and small teams* — stands; the user confirmed it on 2026-09-02.
So the buyer is a founder who cannot code but knows what an app is, and the predecessor's intake
vocabulary is defensible as aimed. Both customers hold when assigned: the buyer's product
vocabulary governs intake, the developer's standard governs output. **ADR-0002.**

### 3.2 The shape — five layers, not seven

The missing architect pass shows at the seams, and every one of those seams sits between layers
that should have been one thing or inside a layer that should have been a step:

| Predecessor | Symptom | Proposed |
|---|---|---|
| B understanding · C plan | C repairs B's granularity in E; `run_layer_c` does four jobs; `builder/file_plan.py` is imported *upward* by C | **B · Contract** — spec → architecture → plan is one derivation, validated once, and the validation is consumed |
| D library | 26 edges into B, 22 into C, 84 into E; `library/verification/` is 681 lines of build harness filed under D | **a step inside C · Build** — match, then generate what did not match. "The library is an amplifier, not the precondition" |
| E build · F design window · deployment | F drives E (70 edges) and leans on G (73); deployment is a module that throws 501 | **D · Ship** — build result → evidence → repository → deploy → the design window as a loop *over* a shipped version |
| A intake, G platform | sound | **A · Intake**, **E · Platform**, unchanged in scope |

Five is a proposal for the `architecture` pass to test, not a number to inherit. The reason to
write it now is the rule in `run`: each layer is an ADR with its reason. **ADR-0005.**

### 3.3 One language

The predecessor is a Python engine behind a TypeScript API and app. The as-built record counts
9,857 within-language edges and **zero** across the seam, and an impact query predicted 2 of 8
files a real commit changed. The seam is where integration defects lived and where the tools go
blind. The generated stack is TypeScript. The Agent SDK is TypeScript or Python.

**Scio is written in TypeScript end to end.** The Python worth keeping — the criteria model,
`Contract`, the validators, `verify_instrumentation`, the console classifier — is small, total,
and shipped with tests named as behaviour claims; porting it is a translation with the tests as
the oracle, not a rewrite. **ADR-0003.**

### 3.4 Buy the harness

The predecessor built its own relay, provider abstraction, untrusted-text fence, chunking,
sandbox interface and job model. Measured 2026-09-02 against Anthropic's own docs:

- **Claude Agent SDK** — self-hosted; one subprocess per session; documented multi-tenant
  isolation (`settingSources: []`, `CLAUDE_CONFIG_DIR` per tenant, `cwd` per session,
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`); `SessionStore` adapters for S3/Redis/Postgres; OTEL
  out of the box; `maxTurns` as the only built-in stop. Hosting cookbook covers Docker, Modal,
  Kubernetes.
- **Managed Agents** — hosted; beta header `managed-agents-2026-04-01`; cloud or self-hosted
  sandbox; not eligible for Zero Data Retention or a HIPAA BAA while stateful; whether a browser
  runs inside the sandbox is not stated on the overview page.

**Scio runs its build loop on the Agent SDK, self-hosted, one sandbox per build**, and the
sandbox provider is chosen by the four numbers ADR-0005 (predecessor) asked for and nobody
produced: prewarm latency, concurrency limit, cost per session-hour, and **whether Playwright
runs inside the isolation boundary** — because two of the gates are a browser driving the app.
Firecracker-class providers (E2B, Vercel Sandbox, Cloudflare Sandboxes GA April 2026) are the
candidates; Azure ACA dynamic sessions remains in preview. Managed Agents is the named
alternative to re-test when it leaves beta. **ADR-0004.**

What Scio still owns on top of the harness: the spec, the gates, the evidence, the spend
ceiling checked *before* the call (the predecessor checks after and under-reports the build
that hit it), the untrusted-text boundary at the render edge, and the stop rule.

### 3.5 Evidence is the product surface

The reveal shows nine things, per the spec the reviews found and the predecessor never rendered:
requirements met and unmet · tests and browser flows run · security checks · changed packages
and files · verified-unchanged surface · model and build cost · build time · remaining risks ·
version id and export. Every gate is **on by default**; opt-in verification is not verification.
Status vocabulary stays `passed / needs_look / failed / blocked`, with `unjudged` first-class.
A gate that could not run says so; it never reads as clean. **ADR-0007.**

### 3.6 Sequence: one vertical slice before any breadth

The predecessor's failure was breadth. The rebuild proves the core loop with everything
generated, then adds the amplifiers:

1. **Slice 1 — "just build it."** Intake → contract → build with all gates on → evidence report
   → a GitHub repository the user owns with CI green. One app kind. No design window, no
   library, no curation. Level 1 of the predecessor's UX flow, which today lands on a
   placeholder.
2. **Slice 2 — shaping.** The design window as a loop over a shipped version: mark → describe →
   impact analysis → surgical regeneration → promote. Carries the predecessor's Solid parts of
   F unchanged.
3. **Slice 3 — the library.** Contribution from every successful build, generalise, re-verify,
   contract-match before generating. Export entries as registry-standard items with `Contract`
   in `meta`. Never import a block collection without a contract.

**ADR-0006.**

---

## 4 · Keep · change · park, per predecessor layer

Verdicts are the as-built *State* headings; the third column is what this proposal does with
them. Overrides of a verdict are marked and reasoned.

| Layer | Carry forward unchanged (Solid / Deliberate) | Rewrite, keep behaviour (Wrong-shaped) | Build (Missing) | Park |
|---|---|---|---|---|
| **A** | provenance model · buildable-enough gate · downstream tags · correction machinery · contradiction rules · the WHICH/HOW split (gate picks the field, model words it) · stand-in path | `is_buildable()` as a *distribution* of how much downstream must invent, not a boolean · scored coverage per area | app-kind detection, **additive-only** so no core field can be dropped (`ontoagent-elicitation`) · replay harness with published metrics (`req-elicit-gym`) · build-failure → intake-field feedback | — |
| **B+C** | eleven validation rules · `source_field` on every node · assumptions from A's metadata, never the model's · criteria model `produced_by × observed_by` · Kahn ordering · `PackageInterface` (names and shapes, never code) · deterministic interaction scripts · unsupported criteria kept | **validation is consumed**: a failing plan does not build · granularity by size, not one-per-entity · criteria carry A's provenance (a defaulted package is held to a *different* "done when") · `run_layer_c` split into its four jobs · foundation package advertises only what it builds | two packages owning one node is rejected (reproduced live 2026-08-26) · `parallelizable` computed from disjoint file plans, not asserted | `why_slice` |
| **D** | `Contract` subset-plus-equality · `entity_forms` · the seven-step refusal sequence · `reverify` against an unseen entity · model for rewriting only · `unmet_requirements` → fall back to generate | failed assembly falls back to generate, like `unmet_requirements` · indexed contract lookup instead of a full-catalog scan · `Quality.better_than` refuses to compare measured with unmeasured | promotion teaches the library · a human curation surface · Playbook version on every entry | the three empty seed entries · `library/verification/` under D · any vector index on the deciding path (DROP D11, D19) |
| **E** | `verify_instrumentation` with rollback · package stamping by the builder · console classifier that publishes what it suppressed · build-scoped `Spend` · honest-status types · promotion refuses rather than rebuilds · untrusted-text fence · cheap-and-certain gate order · truncated reply writes nothing · assembly gate set | ceiling checked **before** the call, overshoot recorded · build cost includes B, C and contribution · interaction gates **on by default** · `checks_passed` rendered · builds are jobs that survive a deploy | the generated app's own tests and `next build` run · real-data and cross-tenant gates as the default · secret-sink harness · cross-tenant zero-rows test generated beside every RLS policy | own relay/provider machinery → the harness · `AcaSandbox` · the unreachable queue state |
| **F** | per-marking outcomes · conflicts asked not resolved · the allowance sentence · restore is a write · promotion · dumb bridge · four-state preview union | change budget derived, per workspace, tested · design-version ref typed, and a bad ref **refuses** instead of rebuilding · one owner for `compiles` · deployment either works or does not exist | metering asserted in tests · the ceiling exercised · tokens, reference upload, test/interact · flagship-loop metrics · server-side second confirmation | — until Slice 2 |
| **G** | `applyWorkspaceScope` pure and throwing · the tenant-discipline test · `IdentityVerifier` behind one interface · dev auth refusing production · 404 across tenants · non-throwing metering · the period cap · `openStream` · `tracked-sources` | tenancy **proven, not asserted**: RLS in the database, every model scoped or explicitly labelled unscoped, a cross-tenant zero-rows test per policy · webhook signatures verified · `@CurrentWorkspace()` typed truthfully · enums in shared match the database | the allowance shown before the refusal · replay guarded *after* ownership (F-03) | — |

**One override.** The as-built calls `AcaSandbox` wrong-shaped; this proposal drops it
(Obsolete): the provider was never run, its `start` does not match its own interface, it is
excluded from the conformance suite, and the platform it targets is still in preview. The
`SandboxProvider` interface and its conformance test are kept.

---

## 5 · The outside world, dated 2026-09-02

- **Anthropic** ships two harness products. The Agent SDK is the self-hosted one with hosting
  guidance for isolation, session persistence and cost; Managed Agents (beta since 2026-04-08)
  is the hosted one, with cloud or self-hosted sandboxes and a durable event log. Anthropic's
  guidance is prototype on the SDK, graduate to Managed Agents.
- **Lovable** ships two-way GitHub sync, Visual Edits over database-connected content, a
  security scan on every publish with a workspace policy to block on critical findings, and
  (May 2026) parallel subagents during a build. Output stack: React + Vite + TypeScript +
  Tailwind + shadcn/ui + Supabase.
- **The comparisons** put Lovable, Bolt, v0 and Base44 in the "first 48 hours" class and name
  Totalum, Replit and Cursor as shipping production-ready output. The test they apply is
  week-three survival: schema change, export, price. None of them mentions evidence.
- **Sandboxes**: Cloudflare Sandboxes GA (April 2026), E2B and Vercel Sandbox on Firecracker,
  Modal on gVisor, Daytona closed-source since June 2026, Azure ACA custom-container sessions
  still preview.

Nothing in this scan contradicts the thesis. Everything in it says the differentiator must be
evidence and ownership, because the build itself is table stakes.

---

## 6 · What the MVP must not do

- Import a block collection. Each block arrives without a `Contract`, and the reviews are
  explicit that "we have a component library" is not a differentiator.
- Rebuild the relay, provider abstraction or job runner.
- Keep two languages.
- Put a model in charge of which question to ask, whether a plan is valid, or whether a change
  is a conflict. Each of those is a stated, tested guarantee in the predecessor.
- Ship a gate that is opt-in, or a status that can read as clean when the check did not run.
- Build the design window, the library, or curation before Slice 1 has produced a repository a
  developer has opened and not laughed at.

---

## 7 · The talents — which ones, at which step

Two libraries, one rule: **Scio's skills govern, skills-repo's skills execute.** Where both
libraries cover a job, the Scio skill decides what is allowed and the skills-repo skill does the
work under it. `skills-repo` is on branch `claude/app-builder-architecture-rc7hdk`, which is
identical to `main` (zero-line diff, measured 2026-09-02) — there is no separate talent branch.

| Step | Scio (governance) | skills-repo (method) |
|---|---|---|
| Brainstorm, once | `brainstorm` | — (`brainstorming` overlaps; Scio's is the evidenced procedure, use it) |
| Architecture, system and per layer | `architecture`, `design-rule-hierarchy` | `decision-council` for the two costly-to-reverse calls: harness and language |
| Requirements → contract | `ears-requirements`, `ais-grounding`, `clarifying-questions`, `ontoagent-elicitation`, `provenance-record` | `writing-plans` to turn the contract into rejectable tasks |
| Build Scio | `playbook-admission`, `app-design`, `catalog-budget` | `subagent-driven-development`, `test-driven-development`, `source-grounded-implementation` (pin the SDK version, cite its source), `idempotent-action-design` (builds are jobs), `interface-depth-design` (the `SandboxProvider` seam) |
| Gates and evidence | `gate-verdicts`, `validation-evidence`, `build-loop-stops`, `spend-ceilings`, `reflexion-conformance`, `change-impact-analysis` | `code-security-review` on every generated diff; `llm-eval-harness` and `llm-redteam-scan` when a generated app itself contains a model feature |
| Tenancy | `tenant-isolation`, `untrusted-text-boundary` | — |
| Testing | `testing` (green is unjudged until shown able to fail) | `verification-before-completion`, `oracle-weakening-audit`, `eval-harness` for the intake replay |
| Library | `contract-retrieval`, `reuse-classification` | `semantic-duplicate-sweep` at contribution time |
| Retrieval | `as-built`, `graph-guard`, `graphify` | `repo-map` for context selection inside a build |

### 7.1 Second inventory — the agents on the other branches (added 2026-09-02, later the same day)

The first inventory above was wrong about scope: it looked at `main` and the session branch of
`skills-repo` only. Two more bodies of talent exist, both unmerged:

**`skills-repo@claude/hej-f7k1d2`** — 40+ commits ahead of `main`, 1,081 files. Adds one agent,
`skill-builder`, and four skills it loads by phase: `skill-contract` (write a skill field by field,
description last), `skill-measure` (baseline probe, paired arms, preregistered threshold),
`skill-knowledge` (fetch only what the observed gap shows is missing, verbatim quote per claim),
`paired-comparison-blinding` (relabel per item, withhold the key). Its own review on the branch
(`pipeline/REVIEW-2026-09-02-skill-builder.md`, three measured builds) says: *builds good skills,
too slowly and too unstably*; dispatch floor 28.3 minutes at infinite agents, the coordinator's own
authoring 56% of a clean build, and all three contaminations in a dispatch harness that is
rewritten per build. Its recommendation — write the dispatch script once, freeze the gates, add a
fast mode — is the right one and is not on the Scio critical path.

**`hello-world@claude/multi-agent-system-architecture-nmn1pc`** — 41 commits, never merged into
`master`, and therefore invisible to `docs/as-built/`, which was measured on `master`. Copied
byte-identical into `skills-repo@claude/hej-f7k1d2` under
`intake/2026-08-30-agent-and-skill-material/` with `.claude/` renamed to `_claude/` and executables
disarmed, and **none of the four gates run on any of it**. It holds nine agents, 24 skills and six
`PreToolUse` hooks, and several of them are the pipeline this review performed by hand today:

| Agent | Job | Fit to the plan |
|---|---|---|
| `rebuild-prospector` | generate candidate directions from a brief, **cannot open the codebase** | the *position-before-history* step, as an agent; run several in parallel |
| `rebuild-adjudicator` | rule each candidate already-built / one of the 85 proposals / new / n/a, cite `file:line`, emit a selection dossier | the *validate* stage `PIPELINE.md` §2 says is not started — and the subtracting stage it asks for |
| `architect` · `architect-rebuild` | decide a shape question, defend seams, review a design against its claim; docs-only via a write-gate hook; loads exactly three procedures (`architecture-decision`, `system-decomposition`, `architecture-review`) | the executor of `run` steps 1 and 3 under Scio's `architecture` skill; ADR-0005 goes through it before acceptance |
| `llm-component-architect` | one row per model call: deterministic alternative, cost, failure mode, data allowed in the prompt | the deterministic-first doctrine made a checklist; run over Slice 1's design |
| `agent-builder` · `agent-fitness-review` | build an agent from an observed failure; judge an existing one fit to run | for the build repo's own runtime agents, later |
| `domain-researcher` · `primary-source-verifier` | fetch against a written commission; verify a note's citations by opening the sources | the *scan before building* and *verify before acting* rules, as agents |

The `architect` agent's ADR-0021 records the research behind its shape: personas measured
negative, separation measured positive, at most three preloaded skills, procedures rather than
principles. That matches this review's own rule that a skill is a decision procedure, not a persona.

Known problems the material records about itself and this plan inherits: evals cover 4 of the 24
skills; the ablation on the three agent-building skills returned **null** (n=1); absolute paths
to `/home/user/scio` and `/home/user/skills-repo` are hard-coded; the four gates and the security
audit of 28 executables are pending.

**Change to the talent plan.** The rows above replace "—" in the table for *Brainstorm* and
*Architecture*: `rebuild-prospector` and `rebuild-adjudicator` execute the brainstorm and the
validation stage under Scio's `brainstorm` skill; `architect` executes both architecture passes
under Scio's `architecture` skill. The overlap to resolve first is `architecture` (Scio, the
pattern catalogue) against `architecture-decision` + `system-decomposition` + `architecture-review`
(the agent's procedures): the catalogue is the *list*, the three are the *procedure*, and the
agent should load the catalogue as a reference rather than carry a second one.

**The premise, tested against the vendor (added 2026-09-02, from skills-repo's notes).** The user's
premise is that the app can be built better with talents and with Fable. Anthropic's own Fable 5
prompting page says skills written for prior models are often too prescriptive for Fable and can
degrade output. Every talent named in this section was written and measured on Opus. So "with
talents" is not a given; it is a measurement per talent, and `skill-measure`'s paired arms on Fable
are how each one earns its place or is dropped. Effort (`high` default, `xhigh` for the
capability-sensitive steps) is a routing dimension beside model, and "audit each claim against a
tool result from this session before reporting progress" goes verbatim into every subagent prompt.

Talents in skills-repo that this plan does **not** use for Scio: `piano`, `library-curator`,
`factory`, `research-scout`, `wave-reflect` and the harvest machinery — they are the talent
factory's own loop, not a build method. `agentic-os` and `enterprise-agent-ops` become
relevant at Slice 1's hosting step, not before.

The overlap to watch: `brainstorm`/`brainstorming`, `testing`/`test-driven-development`,
`eval-harness`/`llm-eval-harness`. Each pair is resolved above; the resolution should be written
into the skill descriptions so the wrong one does not trigger.

---

## 8 · What the user has to answer

1. **The wedge.** Answered 2026-09-02: founders / app-builders. Intake keeps its vocabulary;
   ADR-0002 updated accordingly.
2. **Hosting posture.** Answered 2026-09-02: the buyer is asked at intake whether data is stored,
   how sensitive it is and where it must live, and the build routes on the answers — ADR-0010.
   Delivery is hosted in Scio's ecosystem by default with buy-out as a key transfer — ADR-0009.
3. **The stray file.** `Scio/testa` holds one URL to a third-party architecture skill
   (`agentpoet/agentic-coding-system-self-improving-framework`, `.claude/skills/architecture`).
   Checked 2026-09-02: GitHub returns 404 for the repository, the raw file and the pinned commit,
   and a web search finds no repository of that name — private, renamed or deleted. It could not
   be scanned. If it is reachable to you, drop the SKILL.md into `docs/triage/` and it goes
   through the same four gates as the intake material.
4. **The unmerged agents.** Nine agents and 24 skills sit on
   `hello-world@claude/multi-agent-system-architecture-nmn1pc`, ungated, and `docs/as-built/` does
   not know they exist. Should they pass the four gates and move into Scio as the build-time
   agents (§7.1), or stay as intake until the skill-builder is stable?

---

## 9 · Sources

- Anthropic, *Claude Managed Agents overview* — platform.claude.com/docs/en/managed-agents/overview, fetched 2026-09-02
- Anthropic, *Hosting the Agent SDK* — code.claude.com/docs/en/agent-sdk/hosting, fetched 2026-09-02
- Lovable review and guides, 2026 — lovable.dev/guides, vibecoding.app/blog/lovable-review-2026
- Totalum, *Production-Ready AI App Builders in 2026*; appbuilder24, *Bolt vs Lovable vs v0 vs Base44 2026*; pasqualepillitteri.it, *AI App Builders compared 2026*
- `docs/as-built/*` (measured 2026-08-26), `docs/next/LAYER-E-BUILD.md` §3.3 and §4.5 (scanned 2026-08-26), `scio.db` (rebuilt 2026-09-02: 249 findings, 27 skills, 1,901 chunks)
