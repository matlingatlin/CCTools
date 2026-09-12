# Talents at three levels — building Scio, inside Scio, and shipped with the app

**Date:** 2026-09-02. **Status:** proposal; filed as ADR-0008. Extends `docs/SKILLS-LIBRARY.md`
(2026-08-26), which named the three levels and is kept unchanged. What this adds: the mapping of
each predecessor mechanism onto the talent kinds the harness actually offers, measured against
Anthropic's SDK documentation fetched today, and the contents of the level-3 package.

**Talent** here means any of: skill, subagent, hook, MCP server, plugin, command. They are not
interchangeable — each has a job the others do badly — and most of this document is about which
kind goes where.

---

## 0 · What the harness can host, dated 2026-09-02

From `code.claude.com/docs/en/agent-sdk/{hooks,skills,subagents}`:

| Kind | Defined | What it is for | Limits that matter |
|---|---|---|---|
| **Hook** | in code (`options.hooks`) or settings | run *our* code at an event; `PreToolUse` can **deny, allow, ask, defer, or rewrite the input**; `PostToolUse` can append context or **replace the tool output**; `deny` beats everything | 30-odd events incl. `PostToolBatch`, `SubagentStart/Stop`, `PreCompact`, `Stop`, `InstructionsLoaded`; async hooks cannot block |
| **Skill** | files only (`.claude/skills/<name>/SKILL.md`), no programmatic API | instructions and references the model loads when relevant, or on `/<name>`; `skills: [...]` allow-lists per session | discovered via `settingSources`; a listed name must be exact; unlisted files stay readable on disk |
| **Subagent** | programmatic `AgentDefinition` (recommended) or `.claude/agents/` | a fresh context with its own prompt, a **tool subset**, its own `model`, `maxTurns`, `effort`, preloaded `skills`, its own `hooks` and `mcpServers` | receives only the Agent prompt and CLAUDE.md, never the parent's history; depth 3, 20 concurrent, `maxBudgetUsd` per query — all capped |
| **MCP server** | config | a runtime capability: a tool the model calls | the wrong shape for instructions (`TOOLING-SCAN` §3.3) |
| **Plugin** | marketplace + SHA pin | ships skills, agents, hooks and MCP config in one install, namespaced (`/scio:brainstorm`) | `claude plugin validate --strict` checks schema, not truth |

Two facts decide most placements below. **A hook runs code without the model's consent**, so a
hook is where a guarantee lives. **A subagent's context is structurally isolated**, so a subagent
is where a boundary lives. A skill is neither: it is advice the model may follow.

---

## 1 · Level 1 — building Scio (now)

Governance from Scio's 27 skills, method from skills-repo, execution by the nine unmerged agents;
see `REVIEW-FRESH-EYES-2026-09-02.md` §7 and §7.1. The only addition here is the *kind* each one
should be, because several are currently the wrong kind:

| Job | Today | Should be | Why |
|---|---|---|---|
| keep the graph fresh | `SessionStart` + `post-commit` hooks (ADR-0001) | **keep** | a guarantee, correctly a hook |
| architect may not write source | `docs-only-write.sh` PreToolUse hook on the `architect` agent | **keep** | a wall, correctly a hook |
| count agents before dispatch | a rule in `CLAUDE.md` that has failed once | `SubagentStart` hook that **denies** past the cap | the repo's own text calls it "the weakest defence"; the SDK now has the event |
| load Scio's skills into the build repo | clone-on-demand | **plugin with SHA pin** | settled in `TOOLING-SCAN` §3.1; this is the run-document answer |
| position before history | a rule | `rebuild-prospector` subagent with **no Read on the codebase** | isolation makes the rule structural |
| verify a claim at primary source | a rule | `primary-source-verifier` subagent | same |

---

## 2 · Level 2 — inside Scio, while it builds someone's app

This is the level the predecessor built by hand: relay, provider, fence, chunking, gates, critic.
Under ADR-0004 the build loop runs on the SDK, so every one of those becomes a talent of a
specific kind. The table is the migration plan for Layer C (Build) and the deterministic-first
doctrine expressed in harness terms.

### 2.1 Guarantees → hooks

| Predecessor mechanism | Hook | Event | What it does |
|---|---|---|---|
| `verify_instrumentation` with rollback (E, Solid) | `instrumentation-guard` | `PostToolUse` on `Write\|Edit` of `*.tsx` | checks every expected `data-scio-package` id survives; on loss, **replaces the output with a rejection and reverts** |
| package stamping by the builder, not the model (E, Solid) | `package-stamp` | `PostToolUse` on `Write` | rewrites the file with the owning package's stamp; the model never asked |
| file plan ownership; two packages must not own one file (C, Missing) | `file-plan-fence` | `PreToolUse` on `Write\|Edit` | **deny** any path outside the package's plan, with the reason |
| secret sink (E-101) | `secret-sink` | `PostToolUse` on `Bash\|Write`, `Stop` | scans the exact bytes; a hit marks the build `blocked` |
| spend ceiling checked *before* the call (E, Wrong-shaped) | `spend-ceiling` | `PreToolUse` on `Agent`, plus `maxBudgetUsd` on the query | the SDK cap ends the query; ours records the overshoot the predecessor lost |
| the untrusted-text fence at the render edge (A-31, `untrusted-text-boundary`) | `render-boundary` | `UserPromptSubmit`, `PostToolUse` on `Read` of user-authored artefacts | neutralises at the boundary, never at write time |
| console classifier that publishes what it suppressed (E, Solid) | `console-classify` | `PostToolUse` on the Playwright MCP tools | appends the classified report as `additionalContext`; suppressed list included |
| stop rule (`build-loop-stops`) | `stop-rule` | `Stop`, `SubagentStop`, `PostToolBatch` | round ledger; refuses a fourth attempt at the same failure class |
| trust store for repo-declared commands (E-102) | `command-trust` | `PreToolUse` on `Bash` | deny anything not in the declared set; the generated app's `package.json` scripts are not trusted by default |

Every hook returns what it examined (`validation-evidence`): a hook that did not fire is a
missing row in the evidence report, not a pass.

### 2.2 Boundaries → subagents

| Role | Tools | Preloaded skills | Note |
|---|---|---|---|
| **package-builder** (one per package, in parallel when file plans are disjoint — E-56) | Read, Write, Edit, Bash within the sandbox | the Playbook, the stack skill for its package kind | receives the package contract and its dependencies' *interfaces*, never their code (invariant 4); `maxTurns` from the size classifier (E-11) |
| **critic** | Read, Grep only | `gate-verdicts` | cannot edit, so it cannot "fix" what it judges; verdict vocabulary enforced by a `SubagentStop` hook that rejects an unparseable verdict as failure |
| **security-reviewer** | Read, Grep only | `code-security-review`, `tenant-isolation` | model scaled to diff risk (E-28); the seven security triggers (E-12) decide whether it runs at all |
| **interaction-runner** | Playwright MCP, Read | none | drives scripts *derived* from the architecture, never authored by a model (C, Deliberate) |
| **spec-writer / whole-narrator** (Layer B) | Read | `ais-grounding`, `ears-requirements` | grounded to Layer A's metadata; a `SubagentStop` hook discards any assumption not sourced from A |

The critic and the builder are different subagents for the same reason the architect cannot write
source: separation is measured positive, self-review is measured negative (ADR-0021 of the
predecessor's multi-agent branch, citing CodeR and the GSM8K self-review decline).

### 2.3 Advice → skills, selected not constant

The Playbook is a library of one entry (`SKILLS-LIBRARY.md`). Under the SDK it becomes a
directory of skills selected per build by Layer D's `Contract` test, pointed at instructions:

| Skill | Selected when | Source |
|---|---|---|
| `playbook-core` | always | the fixed house rules, admitted through `playbook-admission` |
| `stack-nextjs-supabase` | always under predecessor ADR-0011 | BC-A1, A2, A10, A12 (the ~22–34-token lines) |
| `design-tokens` | always | `app-design` §1–4 |
| `tenancy-rls` | `users_and_roles` has more than one role | `tenant-isolation` §runtime half, BC-A13, A14 |
| `sensitive-data` | `data_ownership_sensitivity` is not `none` | BC-A13 |
| `connector-<name>` | the spec declares the integration | one per admitted connector |
| `llm-feature` | the app itself calls a model | `structured-llm-extraction`, `abstention-threshold-design`, `llm-eval-harness` — skills-repo's runtime-facing set |

The `skills: [...]` option on the query is the selection mechanism; the allow-list is computed,
never chosen by the model. Budget per `catalog-budget`: every entry's description counted, a
per-entry byte cap, a shrink floor.

### 2.4 Capabilities → MCP servers

Playwright (the interaction gates), the sandbox's own file and process tools, GitHub (repository
creation and push in D · Ship), Supabase or the database (schema apply, RLS test). Each widens
what the agent reaches, so each is added one at a time behind `command-trust`, and a subagent
gets only the servers its row above names (`mcpServers` per `AgentDefinition`).

### 2.5 What stays code, not talent

Intake's gate (`is_buildable`), the eleven validation rules, Kahn ordering, `Contract` matching,
the criteria model, the size classifier, the evidence report. None of these is a talent. They are
deterministic functions the harness calls before or between model turns. Putting any of them in a
skill would hand a guarantee to advice.

---

## 3 · Level 3 — shipped with the generated app

The delivered repository is the product (ADR-0002). A developer opens it and, increasingly, opens
it *with an agent*. Handing over the code without the instructions for working on it is half a
handover (`SKILLS-LIBRARY.md`). The level-3 package, generated by the foundation package in
Layer B's plan:

| Artefact | Contents | Already decided? |
|---|---|---|
| **code graph + hooks** | `graphify` build, `SessionStart` and `post-commit` hooks | **yes — ADR-0001** |
| **`CLAUDE.md`** | the app's own architecture in words: the *whole* from Layer B, the package map, the invariants the build enforced, what `unjudged` in the evidence report means | no |
| **`docs/decisions/`** | the ADRs the build made for *this* app (stack, tenancy, each connector), with the user's stated requirements as their context | no |
| **`docs/evidence/`** | the evidence report as delivered, plus the criteria — so a later change can be checked against the same bar | no |
| **stack skill** | the same `stack-nextjs-supabase` and `tenancy-rls` skills level 2 used, so the developer's agent writes in the same house style Scio did | no |
| **test and lint hooks** | `PostToolUse` running typecheck and the affected tests, the secret-sink hook, the file-plan fence relaxed to a warning | no |
| **`evals/`** | for an app with a model feature: the `llm-eval-harness` suite and the red-team scan config, wired as CI | no |
| **a `/extend` command** | the smallest Scio loop as a command: spec delta → impact analysis → surgical change → evidence — for the developer working without Scio | no, and this is the one with a business shape |

Level 3 is deliberately **last** in `SKILLS-LIBRARY.md`'s order, and this document keeps that:
it needs levels 1 and 2 to be worth shipping. What changes is only that Slice 1 (ADR-0006) ships
the first four rows anyway, because they are outputs Scio already computes and the graph is
already decided.

---

## 4 · What is settled, what this proposes, what stays parked

| | Outcome | Reason |
|---|---|---|
| Three levels, not two | **keep** (`SKILLS-LIBRARY.md`) | levels 2 and 3 have different readers and different lifecycles |
| Order: measure one skill → split the Playbook → second entry → consent → level 3 | **keep** | scaling an unmeasured thing multiplies it |
| Guarantees as hooks, boundaries as subagents, advice as skills | **build** (ADR-0008) | the SDK now has the events and the isolation; the predecessor hand-built both |
| The nine agents on the multi-agent branch | **complete** through the four gates | they exist, ungated |
| A skills marketplace as a second product | **park** (`next/SKILLS.md`) | Scio is not finished |
| A vector index anywhere on the selection path | **keep the rejection** (DROP D11, D19) | `Contract` is decidable; embeddings are not |

---

## Sources

- Anthropic, *Intercept and control agent behavior with hooks*, *Extend agents with skills*,
  *Subagents in the SDK* — code.claude.com/docs/en/agent-sdk/, fetched 2026-09-02
- `docs/SKILLS-LIBRARY.md` (2026-08-26); `docs/TOOLING-SCAN.md` §3.1, §3.3, §3.4; `docs/next/SKILLS.md`
- `docs/as-built/LAYER-C`, `LAYER-E` §6; `scio.db` findings E-11, E-12, E-28, E-56, E-101, E-102, A-31, BC-A1…A14
