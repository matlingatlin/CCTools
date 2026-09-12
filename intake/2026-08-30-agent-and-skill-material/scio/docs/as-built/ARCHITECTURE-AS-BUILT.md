# Architecture — as built

The whole of `hello-world`, composed from the seven layer documents. Every claim here is
carried up from one of them; nothing was written straight into this file.

---

## What the system is

A pipeline that turns a conversation into an application the user owns.

```
conversation ──A──▶ typed spec ──B──▶ the whole + architecture graph ──C──▶ ordered
build packages ──D──▶ matched against a library ──E──▶ built, gated, git-committed
──F──▶ shaped in a design window ──▶ promoted and delivered
```

Six gates a project passes through, each with a person or a rule at it. **A** decides when
enough has been said. **B** decides whether the architecture is coherent, before a single
token is spent on code. **C** decides what gets built in what order. **D** decides what is
assembled rather than generated. **E** decides whether what was built actually works. **F**
decides what the user changes before delivery.

## The one idea holding it together

**Deterministic first; the model only where judgement is genuinely required.**

It is not a slogan — it is implemented independently in five layers:

| Layer | Deterministic part | Model part |
|---|---|---|
| A | *which* field to ask, decided by the gate | only the *wording* of the question |
| B | architecture derived and validated by rules | only "the whole" narrative, grounded |
| C | decomposition and Kahn ordering | one optional call, for operations only |
| E | gates ordered cheap-and-certain first | codegen, and the critique |
| F | conflict detection by regex + canonical vocabulary | only the change itself |

Layer A's docstring gives the reason best: the gate is *"deterministic, reproducible, free,
and impossible for a model to talk its way past."* Layer B's gives the economics: validating
first means *"a design error costs a function call rather than a relay run."*

**This is the architecture's real asset.** Any rebuild that puts the model in charge of
sequencing, sufficiency or validation is not a refactor of this system — it is a different
and worse one.

## The five invariants the system rests on

Carried up from the layer documents, each enforced in code and covered by tests:

1. **Nothing unstated is invented.** A field claiming `stated` without real message-id
   provenance is discarded (A).
2. **An inference never overwrites what a person said**, and a hand correction cannot be
   overwritten by extraction at all (A).
3. **The architecture is validated before code is generated** — eleven rule identifiers, no relay
   spend (B).
4. **A package receives its dependencies' interfaces, never their code** — proven by a test
   asserting `"tables: booking" in prompt` and `"CREATE TABLE" not in prompt` (C).
5. **Delivery promotes, it never regenerates.** The files the user shaped are the files that
   ship, with git history intact (F, ADR-0017).

## The pattern that matters most

Across five of seven layers, the same failure recurs, and it is not five bugs — it is one
habit:

> **The system computes an honest signal, and then drops it before it reaches anyone.**

| Layer | Computed | Consumed by |
|---|---|---|
| C | `validate_plan` — **nine rule identifiers from seven check functions**, every build | **nothing**; `builder/pipeline.py` never references it |
| E | `checks_passed` — computed, typed, transmitted | **never shown** |
| F | `compiles` — carried by hand through four hops | fragile, no test |
| G | `/usage/allowance` | **nothing in the frontend**; a user learns their balance by being refused |
| D | five curation endpoints | **no human surface in front of them** |

The re-think brief's appendix argued the differentiator is *verification* — that the product
tells you honestly what works. The layer documents say that is **half-built**: the verifying
is real and careful; the telling is where it stops. `validate_plan` is the sharpest case,
because ADR-0013 explicitly rejected "no plan validation" on the grounds that design errors
would slip into code generation — and then nothing was wired to read the result.

**A rebuild that only surfaced what is already computed would deliver most of the claimed
differentiator without inventing anything.**

## The second pattern: the best mechanisms are opt-in or unreachable

- The two most valuable gates — *does it work with real data*, *can a guest read another's
  row* — run only under `SCIO_VERIFY_DATA=1`, and their proving tests skip without pglite (E).
- Three of the four library entries have empty operations and routes, so they can never
  match. The matchable catalog is **one entry** (D).
- `BuildJob.status = "queued"` is unreachable; the queue and worker are absent (E).
- Deployment is a module with a route table whose only behaviour is `501` (F).
- Settings is still a placeholder page (F).

## Where trust is won or lost

Three moments, all built, all careful:

1. **The spec gate** — Layer B's *whole*, the narrative the user approves. Grounded, and its
   assumed-list comes from Layer A's metadata rather than the model's own claim.
2. **The reveal** — the honest-status vocabulary `passed / needs_look / failed / blocked`,
   with `unjudged` as a first-class value.
3. **The design window** — per-marking outcomes, and conflicts *asked* rather than resolved.

The missing fourth is a **scored** view: nothing renders "security 86%, data 90%". The
downstream tags already partition the spec into build areas and every field already records
whether it was stated, derived or defaulted — **so this is computable today from data that
exists**. It is the smallest high-value gap in the system.

## Where the money is

- The **period cap** ($50/month, `SCIO_WORKSPACE_PERIOD_CAP_USD`) works, enforced once, as a
  409 naming both figures (G).
- **Metering is non-throwing** — a failed ledger write is logged, never raised into a build (G).
- The **per-build ceiling** is checked *after* the call that crosses it, and the raise discards
  the whole `RelayResult` — so not just the crossing call but every completed pass in that
  attempt goes unrecorded, and `_write_attempt` returns `cost_usd=0.0`. The ledger under-reports
  precisely the build that hit its ceiling. The code's own comment argues the opposite: *"the
  model has already been paid for the tokens either way"* (E §6).
- **The reported build cost is not the build's cost.** Layers B and C and the library
  contribution run with no spend tracking; the figure is packages-only (E).

## The most dangerous single finding

**Tests that pass for the wrong reason.**

**Two confirmed instances, not one.**

`FakeScope` in the API e2e suite enforces `owns(projectId)` on child models. The real
`WorkspaceScope` deliberately does not — only six of fourteen tables carry `workspace_id`.
So every cross-tenant test passes for two different reasons and cannot distinguish them.

And `test_interaction_channel.py` — 36 test functions, of which **27 run and 9 skip**, and the nine
that skip are exactly the ones that would drive a real browser — hand-writes typed operation inputs that Layer B
never produces. `derive.py:259` gives every create and update a single `payload: json`;
`_fillable` prefers declared inputs and `json` cannot be typed into a form, so
`persistence_script` returns `None` on every real build. Measured on the canonical booking
spec: 13 `validation` criteria, 8 `unsupported`, 6 `render`, **0 `interaction`**. The channel
the two most valuable gates depend on never arms — and the suite proving it works is green.

That is what let a real breach survive: `BuildService.run` replays a build by
`{projectId, idempotencyKey}` **before** the project ownership guard, and `BuildVersion` has
no `workspace_id` column to scope on. This is GPT review finding **F-03**, still live
(G, verified 2026-08-26).

A green suite is only evidence if the doubles are no stricter than production.

## What a rebuild must carry

**Non-negotiable — expensive to rediscover, invisible in the shape of the code:**

- Deterministic-first sequencing, in all five places it appears
- Per-field provenance with `source`, `confidence` and message-id grounding
- The buildable-enough gate, and *momentum over completeness*
- Downstream tags — without them B and C have prose
- `source_field` on every architecture node
- The `Contract` subset-plus-equality test that makes library matching decidable
- The honest-status vocabulary, `unjudged` included
- Build-scoped rather than per-call spend
- Promotion over regeneration

**Safe to drop or redo:**

- `why_slice`, which does not slice
- `mark_parallelizable`, which does not compute
- The unreachable queue state
- The three empty library entries
- `library/verification/` — 681 lines of pglite harness filed under the library, which is not
  the library

## Where the missing architect pass shows

Not in the ideas, which are good. In the seams:

- Granularity is fixed in C and then repaired by chunking in E
- `builder/file_plan.py` defines what "producible" means and is imported *upward* by C's
  validator
- `library/verification/` sits under the wrong layer entirely
- `run_layer_c` does four jobs; only the first is in its name
- A boolean `is_buildable()` where the downstream question is *how much will be invented*

Each is small. Together they are the difference between a system that was drawn and one that
accreted.

---

*Composed 2026-08-26 from LAYER-A through LAYER-G. Every claim traces to a layer document;
each layer document traces to `file:line` or a test name.*
