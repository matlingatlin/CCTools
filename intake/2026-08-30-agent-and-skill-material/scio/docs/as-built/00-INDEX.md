# 00 · Index — the macro map of `hello-world`

**Status: current.** Structure measured directly; behavioural claims carried up from the
layer documents. Corrected 2026-08-26 after a blind test found two false claims here.

Measured 2026-08-26 from the repo and from `graph/graph.json` (5,173 nodes, 12,054 edges).

## The seven layers

Source only — tests and the React app are counted separately below.

| | Layer | Files | Lines | Lives in |
|---|---|---:|---:|---|
| **A** | Intake — gate 1 | 17 | 2,775 | `engine/intake`, `api/modules/{intake,spec}` |
| **B** | Understanding | 8 | 1,308 | `engine/layerb` |
| **C** | Build plan | 9 | 1,764 | `engine/layerc` |
| **D** | Component library | 31 | 4,152 | `engine/library`, `api/modules/reference` |
| **E** | Build & execution | 42 | 9,393 | `engine/{builder,execution,core}`, `api/modules/build` |
| **F** | Design window | 11 | 1,614 | `engine/design`, `api/modules/{design,deployment}` |
| **G** | Cross-cutting | 37 | 1,984 | auth, usage, project, workspace, stream, prisma, shared |
| | **Total** | **155** | **22,990** | |

**E is 41% by directory**, but `LAYER-E-BUILD.md` §6 attributes it more carefully: `execution/`
is the engine's shared model layer used by six of seven layers, and `engine.client.ts` serves
every API module. Layer E's own work is nearer **32%**. Intake — the part the product is
supposedly differentiated by — is 12%.

## How the layers actually depend on each other

Edge counts from the graph. An arrow means *references*, so it points opposite to data flow:
`B → A` is Layer B reading Layer A's output.

| Edge | Count | Reading |
|---|---:|---|
| D → E | 84 | the library is consumed by the build |
| F → G | 73 | design window leans on cross-cutting services |
| F → E | 70 | design window drives builds |
| E → C | 68 | build executes the plan |
| C → B | 66 | plan is derived from understanding |
| A → G | 62 | intake leans on cross-cutting services |
| A → E | 43 | intake uses the shared relay/provider machinery |
| C → E | 39 | plan references build primitives |
| B → A | 29 | understanding reads the spec |
| D → B | 26 | library matching consults understanding |

The declared pipeline **A → B → C → build** is visible and intact (`B→A`, `C→B`, `E→C`).

Two edges are worth a question mark, to be answered in the layer documents:

- **A → E (43).** ~~Probably cost estimation.~~ **Wrong — corrected.** `intake/` never
  mentions `estimate` at all. Every edge is `execution.provider`, `execution.relay` and
  `execution.untrusted`: the shared model-calling machinery, which six of seven layers use.
  Not a layering problem, but not the reason first given either.
- **D → B (26)** and **D → C (22).** **Answered in `LAYER-D-LIBRARY.md` §5: not an
  inversion.** All 26 B-edges land on two leaf modules importing only stdlib and pydantic;
  control flows the other way (`layerc/service.py:76` calls `match_plan`), and the chain is
  acyclic.

## Tests

**884 passed** — engine 640 passed (661 collected, 21 skipped), API 135, app 109. The two units
were previously mixed in one sentence: 640+135+109 = 884, while 661 is a collected count.

Engine tests by file, largest first:

| File | Tests | Layer |
|---|---:|---|
| `test_library` | 47 | D |
| `test_b054_real_run_hardening` | 37 | E |
| `test_intake_agent` | 37 | A |
| `test_interaction_channel` | 36 | E/F |
| `test_core_guardrails` | 30 | E |
| `test_layerb_derive` | 30 | B |
| `test_contribute_back` | 27 | D |
| `test_design_change` | 27 | F |

36 engine test files in total. Tests are named as behaviour claims
(`test_an_inference_may_not_overwrite_what_the_user_stated`), which makes them the highest-signal
description of the system — they cannot drift silently, they break.

## Verified baseline · 2026-08-26

Run in a clean container, all four green:

| Suite | Result | Exit |
|---|---|---|
| Engine | 640 passed, 21 skipped | 0 |
| API | 135 passed (12 files) | 0 |
| App | 109 passed (8 files) | 0 |
| Typecheck | clean, all workspaces | 0 |

The repo's own `/suites` records 655 passed / 6 skipped. The 15-test difference is
environment-gated, not lost tests: they need `@electric-sql/pglite`, a live `SCIO_CATALOG_DB`,
or a built Next app. **None are intake tests.** A verification environment must provide those
three things to reproduce the full number.

## The frontend, by screen

`apps/app/src/pages/` — `Projects`, `Create`, `Wizard`, `Spec`, `Build`, `Reveal`, `Design`,
`Ship`, `Involve`, `Placeholder`. The Wizard and Spec screens are Layer A's surface; Reveal is
where the build's result is shown.

## What is known to be missing

**Read this section, not `docs/STRATEGY.md`.** That file names three gaps, and its first claim
is stale:

> ~~**Intake agent (conversation → filled spec).** Designed; NOT built. `[gap]`~~

**The intake agent is built and has run for real.** `extraction.py:317` awaits `run_relay`;
`questions.py::write_question` relays for wording with a guide fallback; `service.py::run_intake_step`
orchestrates the turn and meters it. Last changed 2026-08-19 / 2026-08-22, commit *"what the
first real run surfaced"*. `StandInIntakeProvider` implements `ModelProvider` — it is a stand-in
**model** for the no-API-key path, not a stand-in agent. See `LAYER-A-INTAKE.md` §Documentation
drift found.

Genuinely missing, established by the layer documents rather than by `STRATEGY.md`:

- **Nothing reads Layer C's plan validation.** **Nine rule identifiers** run every build, emitted by
  **seven check functions** — both numbers are true of different things, and stating either alone has
  now misled a reader twice. A violation carries a `rule` name, so nine is the count that matters.
  `builder/pipeline.py`
  references the result nowhere, though ADR-0013 required validation before building (`LAYER-C` §6).
- **The library's matchable catalog is one entry.** Three of four seed entries have empty
  operations and routes and can never match (`LAYER-D` §6).
- **The build queue and worker.** `BuildJob.status = "queued"` is unreachable (`LAYER-E` §6).
- **The two most valuable gates are opt-in**, behind `SCIO_VERIFY_DATA=1` (`LAYER-E` §6).
- **No scored coverage view** — computable today from downstream tags plus field `source`
  (`LAYER-B` §6).
- **Deployment and Settings** — a 501 route table and a placeholder page (`LAYER-F` §6).

## Where to go next

One document per layer, A → G. Load only the one your question touches — they are 20–35 KB each.
`ARCHITECTURE-AS-BUILT.md` for the system as a whole. `.claude/skills/as-built/` routes it.
