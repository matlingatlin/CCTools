# Layer C · Build plan & decomposition — what to build next

Forward-looking. `docs/as-built/LAYER-C-BUILD-PLAN.md` is the starting point; this is what to
do with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method note.** Every domain this layer touches was scanned before anything was proposed: work
decomposition and story splitting, dependency ordering and topological scheduling, contract-based
design, design by contract and interface segregation, monorepo build graphs (Bazel, Nx,
Turborepo), task-graph agents, acceptance-criteria formalisms, plan validation, and spec-driven
development. The rule the family of documents now runs on: **where a standard or a published
algorithm already covers something, cite and adopt it.** Four things this layer would otherwise
have invented already exist — a criteria grammar (EARS), a delta notation (OpenSpec), an
affected-set algorithm (Nx), and a modularity metric (DSM propagation cost). None needed
inventing.

This document also **depends on** two adoptions made in its siblings rather than re-proposing
them: Layer A §3.2 and Layer B §3.3 mint requirement identities in EARS, and Layer B §3.1 adopts
CodePlan and the change-impact-analysis literature. Layer C is the consumer of both.

Everything measured below was re-run against the working tree on 2026-08-26 with
`apps/engine/.venv/bin/python`. Token figures are characters ÷ 4 and are marked as such —
`messages.count_tokens` is the correct instrument and no API key was available here, so
re-measure before acting on any margin narrower than 20%.

---

## 1 · Where Layer C stands

`Architecture → BuildPlan{packages, order, graph} + PlanValidation + prompts`. Rules group
the nodes into six package kinds, Kahn's algorithm orders them, contracts are assembled, the
plan is validated, the library is matched and the build is priced — `service.py:53-96`, in
that order, and only one model call in the whole layer (`judgment.py:91`, for operations the
rules could not attach to an entity).

**Solid and not to be touched:**

- the criteria model — `produced_by` × `observed_by` (`criteria.py:67`), the strongest single
  idea in the system
- deterministic decomposition and tie-broken Kahn ordering (`decompose.py:405`, `:418`)
- `PackageInterface` — *"names and shapes, not implementations"* (`plan.py:47`); this is the
  mechanism the whole decomposition exists to produce
- the refusal discipline in `scripts.py`: no create operation, no screen, no identity ⇒ no
  script, and the criterion stays recorded-but-unjudged rather than failing every build
- the import-boundary section (`contract.py:164`), written from an observed failure

The constraint that governs every proposal below, from `judgment.py:74`:

> Never fails the plan: any error, and the deterministic grouping stands.

**Any change that lets a model decide package membership, ordering, or whether a criterion is
producible is out of scope.** Proposals may add rules; they may not move a rule into a prompt.

### 1.1 Two corrections to the as-built record

**There are nine validation rule identifiers, not seven.** `docs/as-built/LAYER-C-BUILD-PLAN.md`
says *"seven rules"*, which counts the check *functions*. `validate.py` emits nine distinct
`rule=` values (`:51, :70, :84, :102, :110, :121, :150, :166, :178, :195, :217`):
`node_covered`, `acyclic`, `dependency_exists`, `contract_complete`, `contract_testable`,
`criterion_producible`, `criterion_observable`, `order_respects_dependencies`,
`unique_package_id`. Exactly one — `criterion_observable` — can be a warning; the rest are
errors. The same undercount Layer B §1 found in its own layer, and it matters for the same
reason: the rule *identifiers* are what a gate, a delta, or a conformance check keys on.

**And one thing the as-built pass did not find, which is the largest finding in this document:
the interaction channel — the layer's best mechanism — never arms on real Layer B output.**

`derive.py:259` gives every create operation a single input:

```python
elif verb in {"create", "update"}:
    inputs = [Column(name="payload", type=FieldType.json)]
```

`_fillable` (`scripts.py:93-107`) reads `list(op.inputs) or [c for c in table.columns]`. The
`or` fallback can never fire, because `op.inputs` is never empty. `json` is not in `_SAMPLE`
(`scripts.py:62-68`), so the list comprehension filters it out and returns `[]`.
`persistence_script` then returns `None` at `scripts.py:165`, and `_it_actually_works`
(`decompose.py:207-219`) records `unobservable("'book a table' works end to end and
persists.")` instead of an interaction criterion.

Measured on the canonical booking spec through the real `derive_architecture`:

| observed_by | criteria |
|---|---:|
| `validation` | 13 |
| `unsupported` | **8** |
| `render` | 6 |
| **`interaction`** | **0** |

Zero. Thirty per cent of every plan's "done when" list is observed by nobody, and the two
criteria that two failed real runs were spent on — *"the booking persists"*, *"a guest cannot
read another guest's booking"* — are among them on every build.

`test_interaction_channel.py` passes because its `booking_architecture()` fixture
(`tests/test_interaction_channel.py:117-125`) hand-writes typed inputs — `guest_name: text`,
`party_size: integer` — that Layer B does not produce. The tests prove the derivation is
correct given a typed operation; nothing proves Layer B ever hands one over.

This is a Layer B/Layer C seam bug, not a design flaw, and it is the cheapest high-value fix
in this document (§2.1).

---

## 2 · Refining what exists

### 2.1 Arm the interaction channel — one seam, three lines

Two honest options, and they are not equivalent:

| Option | Change | Cost of being wrong |
|---|---|---|
| **A. Fix the fallback** | in `_fillable`, prefer `op.inputs` only when at least one input is a fillable type; otherwise fall through to the table's columns | a script types into a form field the operation did not declare — caught by the fill fallback (`form [name="…"]`) or by a failed assertion |
| **B. Fix the derivation** | `derive.py` emits the entity's columns as a create operation's inputs instead of an opaque `payload: json` | wider blast radius: `architecture_slice_text` (`contract.py:70`) renders inputs into every contract prompt, so every feature prompt changes |

**A is the fix for this layer; B is the right fix for the system.** A `payload: json` input is
not information — it is the absence of information rendered as a type, and it is what every
downstream consumer sees. Doing A alone leaves the contract prompt still telling the model
*"inputs: payload: json"* for the operation it is being asked to build.

Either way, the invariant to add is the one that would have caught this:

> A feature package derived from a *real* Layer B architecture with a create operation and a
> screen to drive has at least one `interaction` criterion.

Written against `derive_architecture(spec)`, not against a hand-built `Architecture`. The
existing suite is thorough and tests the wrong side of the seam.

### 2.2 Reorder the contract prompt — for the cache and for attention

`contract_prompt` (`contract.py:142-199`) emits, in order:

```
goal · architecture slice · dependency interfaces · import boundary ·
why (role sentence + THE ENTIRE WHOLE) · vocabulary · scope guard · done when · house rules
```

Two things are wrong with that order, and they are the same thing seen twice.

**Everything byte-identical across packages is at the back.** House rules (667 tokens,
measured), the whole (205 tokens on a short whole), the vocabulary and the scope guard are the
same in all six prompts. Prompt caching is a strict prefix match — render order is `tools` →
`system` → `messages`, and any byte change invalidates everything after it. Constants placed
last can never be a shared prefix. Today they are all last.

**And the whole sits exactly where a model reads worst.** The lost-in-the-middle effect is
measured across every frontier model at every input length — accuracy drops 15–20 points for
content in the middle of the context versus at either end (Hong, Troynikov & Huber, [*Context Rot*, Chroma,
2025](https://research.trychroma.com/context-rot) — 18 models, every one affected at every
input length tested; Liu et al., [*Lost in the
Middle*, 2307.03172](https://arxiv.org/abs/2307.03172)). The *"why this exists"* block is in the middle
of a ~1,300-token prompt. Its whole purpose is to survive the build.

Refinement: **constants first, then the package-specific slice, then "done when" last.**
House rules + vocabulary + scope guard + the whole is 892 tokens as a block on the fixture
(measured) — **which clears Opus 5's cache floor of 512 tokens today, without needing a design
section to grow it.** *(Corrected 2026-08-26: this sentence rested on a ~1,024-token floor that
Layer A §7.3 retracted. The floor is 512 for Opus 5 and 4,096 for Haiku 4.5. The refinement below
still stands on its own merits, and now also pays off immediately rather than after B-7.)* The slice, the interfaces and the criteria stay at
the end where attention is strongest, which is also where they belong on their merits.

This changes no words the model is asked to obey. It changes where they sit.

### 2.3 The foundation package advertises what it does not build

`decompose.py:73` exports `["app shell", "navigation", "supabase client", "test runner",
"lint config"]`. Verified by rendering the real contract prompt: every dependent package reads

```
provides: app shell, navigation, supabase client, test runner, lint config
```

Fifteen lines above that list, `decompose.py:56-60` explains that the *goal* stopped promising
lint and a test runner because *"neither of which is in its file plan"*. `planned_files`
(`file_plan.py:47`) confirms: `app/layout.tsx`, `components/site-header.tsx`,
`lib/supabase.ts`, plus shell pages. Half the fix landed. The interface is the half every
other package reads.

### 2.4 `parallelizable` is a claim, not a computation

`mark_parallelizable` (`decompose.py:442`) documents *"packages that share no dependency path
with a sibling of the same kind"* and implements `if len(group) > 1`. It is right today by
construction and nothing checks that it stays right — while `STRATEGY.md:111` already plans to
route these packages through the Batch API on the strength of the flag.

The correct computation has a name and is free. The set of packages that can run together is
the **antichain** of the dependency DAG — a set of nodes no two of which are connected by any
path — and the maximum antichain size is the DAG's *width*, the standard measure of how much
parallelism a task graph admits. Computing the antichain a package belongs to is a reachability
query over `plan.graph`, which is already materialised (`decompose.py:462`).

Do it properly and two things follow at once: the flag becomes true by construction rather
than by luck, and `topological_order` can return **levels** instead of a flat list — which is
what a scheduler and the Batch API both actually want (§7).

### 2.5 Coverage is one-directional and counts "at least once"

`_check_coverage` (`validate.py:43`) asks whether each architecture node is covered. It never
asks whether a node is covered *twice*, and never asks whether a package references a node the
architecture does not contain.

Reproduced against the real code — one screen `/home` wired to operations of two entities:

```
pkg_feature_booking  ['operation:create_booking', 'screen:/home']  ... 'app/home/page.tsx' ...
pkg_feature_menu     ['operation:list_menu',      'screen:/home']  ... 'app/home/page.tsx' ...
valid: True   errors: 0
```

Two packages own one node and both plan to write the same path. The second overwrites the
first and the manifest gets two owners for one file — which breaks the marking→code coupling
that is ADR-0013's headline consequence. `test_the_actions_file_is_not_claimed_by_two_packages`
guards `app/actions/*.ts` and nobody guards `app/*/page.tsx`.

The rule is one line — *coverage is a partition, not a cover* — and the reverse rule (a slice
entry with no architecture node) is another. `architecture_slice_text` currently skips unknown
nodes silently at `contract.py:56`, `:68`, `:78`, producing an empty *"build exactly this"*
section with no complaint anywhere.

### 2.6 Three dead arguments

`ruff check --select ARG` on the layer, run 2026-08-26:

```
ARG001 Unused function argument: `arch`  contract.py:16   (why_slice)
ARG001 Unused function argument: `plan`  contract.py:125  (assemble_contract)
ARG001 Unused function argument: `arch`  decompose.py:363 (_tokens_package)
```

`why_slice`'s unused `arch` is the interesting one: it is the signature of the function that
was *meant* to slice, kept after the slicing was abandoned. §3 argues it should be used.

---

## 3 · What is missing

### 3.1 The validation gate — decided against in the ADR, absent in the code

`validate_plan` runs seven checks emitting nine rule identifiers (§1.1) on every build. Nothing
reads the result. Verified:
`builder/pipeline.py:214` calls `run_layer_c`, `:220` takes `.plan`, `:227` saves it, `:273`
hands `.prompts` to the orchestrator; a repo-wide grep for `.validation` outside `layerc` and
its tests returns only `builder/validation.py` imports, a different module. The API's
`EnginePlanResponse` (`engine.client.ts:215`) does not model the field.

ADR-0013 lists *"No plan validation"* under **Alternatives considered — rejected; design errors
would slip into code generation."* At runtime, they still do.

**There is a well-established shape for exactly this, and it is not new.** In classical
planning, [VAL](https://github.com/KCL-Planning/VAL) (Howey, Long & Fox, ICTAI 2004) is the
standard plan validator: it checks each action's preconditions against the state, gives a
binary verdict, and — the part worth copying — **names the first action whose preconditions
fail** rather than returning a list of complaints. Recent LLM-planning work translates VAL's
unsatisfied preconditions into natural language and feeds them back as corrective input
(e.g. [Localizing and Correcting Errors for LLM-based Planners,
2602.00276](https://arxiv.org/pdf/2602.00276)).

Three things follow for Scio:

1. **Errors gate; warnings do not.** `PlanValidation.errors` already separates them
   (`validate.py:38`). The eight violations on the canonical booking plan are all
   `criterion_observable` warnings — so making errors a gate today would fail *no* current
   plan, which makes it a cheap change to land and a real one the first time a plan is wrong.
2. **The first failing rule is the message.** Not seven engineering strings.
3. **What the user sees is a product decision.** Today's messages are written for engineers:
   *"Architecture node 'screen:/x' is not built by any package."* Refuse / repair / warn is
   ADR-C-1's actual content, and it is the PM's call, not an implementation detail.

### 3.2 Size-aware granularity — and it is not an edge case

ADR-0013 fixed granularity at "per feature" and considered exactly two alternatives, per-file
and per-app. There is no notion of size anywhere in `decompose.py`.

Layer E already has one. `estimate.expected_output_tokens(package)` is *"the one place in the
engine that holds an opinion about how big a package is"* (`builder/loop.py:340`), and
`CHUNK_TOKEN_BUDGET = 11000` (`loop.py:221`) is what one codegen call may be asked for.
Measured, on plans built from real `derive_architecture` output:

| Spec | Package | expected tokens | chunks in Layer E |
|---|---|---:|---:|
| booking, 2 actions | `pkg_feature_booking` | **16,000** | 2 |
| booking, 12 actions | `pkg_feature_booking` | 23,500 | 3 |
| | `pkg_feature_general` | 21,000 | 3 |
| | `pkg_feature_table` | 18,500 | 2 |
| | `pkg_feature_guest` | 11,000 | 1 |
| any | `pkg_foundation` | 8,000 | 1 |
| any | `pkg_schema` | 4,900 | 1 |
| any | `pkg_auth` | 2,500 | 1 |

**The canonical demo app's one feature package is 45% over the budget and is split in Layer E
on every single build.** Three of four feature packages on a twelve-action app are over. This
is not a large-app edge case; it is the default path.

And the cost table in `estimate.py:44-52` — calibrated against three real runs — says the same
thing in money:

| package | observed cost |
|---|---|
| feature (2 ops, 2 screens) | **$0.857** |
| foundation | $0.168 – $0.312 |
| design_tokens | $0.094 – $0.152 |
| schema | ~$0.086 |
| auth | ~$0.080 |

The one package kind with no size limit is 5–10× every other kind and dominates the invoice.

**What the literature says to do about it.** Splitting work by size has a fifty-year answer in
software architecture and it is not "chunk it later":

- **Modularization Quality (MQ)** — Mancoridis et al.'s *Bunch* (ICSM 1998,
  [ResearchGate](https://www.researchgate.net/publication/3758763)) formulates decomposition as
  graph partitioning and scores a partition by intra-cluster cohesion against inter-cluster
  coupling. It is a single number over a graph Scio already has. It is cheap and deterministic.
- **Design Rule Hierarchy / DSM** — Baldwin & Clark's design-rule theory, made measurable by
  MacCormack, Rusnak & Baldwin's **propagation cost** ([HBS
  08-038](https://www.hbs.edu/ris/download.aspx?name=08-038.pdf)): the percentage of the system
  reachable from a change to any element. Layers whose members depend only upward, and are
  mutually independent within a layer, are a Design Rule Hierarchy — which is **exactly the
  shape `decompose.py` already produces** (§4.2).
- **Vertical vs horizontal slicing** — the agile literature's name for the split Scio already
  makes: `foundation`/`schema`/`auth`/`design_tokens` are *horizontal* (one architectural
  layer each), `feature` is *vertical* (an entity end-to-end). The known failure of horizontal
  slices is that nothing is demonstrable until every layer lands — and the census in §1 is that
  failure, quantified: every criterion outside the feature package is `validation` or
  `unsupported`, because a migration and an auth helper have nothing to look at.

**The proposal.** Split a feature package when `expected_output_tokens` exceeds the budget,
using the same function Layer E already uses, along the natural seam the architecture already
gives — operations and their screens. One package per entity *until too big*; then per
operation-group. Two consequences to argue in the ADR, not wave past:

- the marking→code map gains a level — `screen:/booking` still resolves to one package, but a
  package no longer equals an entity
- the library matcher (`match_plan`) keys on packages, so split packages change what matches

Doing this in C rather than E is what makes the split *visible in the plan the user approves*,
priced before the build, and stable across runs — three things a Layer E chunker cannot give.

### 3.3 Acceptance criteria are hard-coded English — and Layer B has already adopted the grammar

Every criterion in `decompose.py` is a template string. Nothing about *this* app's risk reaches
them. A package built entirely on Layer A defaults is held to the same "done when" as one built
on stated requirements, even though `FieldMeta.source ∈ {stated, derived, default}` records the
difference and `source_field` on every architecture node preserves the chain.

Two separate gaps, and only one of them needs a model.

**(a) The grammar. It is already decided one layer up.** Layer A §4.4 and Layer B §3.3 both land
on **EARS** — the Easy Approach to Requirements Syntax (Mavin, Wilkinson, Harwood & Novak, IEEE
RE'09; [official guide](https://alistairmavin.com/ears/)) — as the notation for identified
requirements, and Layer A states the competitive position plainly: *"EARS is table stakes, not a
differentiator"* — AWS Kiro already generates it — *"what Kiro's `requirements.md` does not have
is provenance… That is the differentiator, and it is already built."*

**Layer C's job is therefore not to choose the grammar; it is to consume it.** If Layer B emits
requirements with ids in EARS, a package's "done when" list stops being a template string and
becomes *the subset of identified requirements this package must satisfy* — which is the same
lookup that fixes `why_slice` (§6.1) and the same join key that makes the reveal's *"requirements
met and unmet"* possible at all.

The grammar itself:

```
WHILE <precondition>, WHEN <trigger>, the <system> SHALL <response>
```

Ubiquitous · Event-driven · State-driven · Unwanted-behaviour · Optional. Zero-or-many
preconditions, zero-or-one trigger, exactly one system name, one-or-many responses.

**Why the fit is unusually tight at *this* layer, which is the argument the sibling documents do
not make.** The EARS clause slots map one-to-one onto machinery `scripts.py` already has:

| EARS clause | Scio mechanism today |
|---|---|
| `WHILE <precondition>` | `as_user(ALICE)` (`scripts.py:181`); `arch.auth_access.mode` |
| `WHEN <trigger>` | `fill(...)` + `click(...)` (`scripts.py:118`, `:184`) |
| `SHALL <response>` | `assert_present` / `assert_absent` / `assert_row` |
| `IF … THEN` (unwanted) | the negative assertion — the half hand-written criteria omit |
| `WHERE <feature>` | the refusal conditions: no owner column ⇒ no isolation criterion |

**A criterion written in EARS is structurally closer to a `Script` than a sentence is.** That is
the adoption argument for Layer C specifically, and it is not popularity.

The alternative, Gherkin's Given/When/Then, is the same idea with more ceremony and a runner
attached; recent work generating it with LLMs reports 100% structural validity under
JSON-constrained decoding but only ~94% semantic coverage
([2607.01980](https://arxiv.org/abs/2607.01980)) — structure is the easy half. Scio does not need
Gherkin's runner, because `core/interaction` *is* one, so EARS's lower ceremony wins.

Also worth taking from Layer A §4.4: **Volere's *fit criterion*** — every requirement carries the
benchmark that decides whether it was met. That is `produced_by` × `observed_by` under another
name, arrived at independently, and it is the strongest evidence in this document that
`criteria.py` was built along the grain of the field rather than against it.

**(b) The risk weighting.** Lift Layer A's provenance into the contract. A package whose slice
traces mostly to `default` fields is a package built on guesses; it should carry a criterion
saying so, and the user should see which packages those are. This is free — the data is
already carried through Layer B on `source_field` and thrown away at the package boundary
(§3.5).

### 3.4 There is no plan delta — and it is the second half of Layer B's impact analysis

An amended spec re-runs the entire planner. There is no operation taking `(amended
architecture, existing plan) → delta`. Directed regeneration exists at the *code* level
(`design/change.py`); at the *plan* level, nothing.

**This is not a separate proposal from Layer B §3.1 — it is its second half, and it should not be
argued twice.** Layer B adopts the change-impact-analysis literature (Arnold & Bohner 1993;
Chianti, OOPSLA 2004; CodePlan, PACMSE 2024; ProReFiCIA 2026) and proposes a *tiered* impact set
over the architecture graph. Layer C is where that set stops being architecture nodes and becomes
**packages, files and prices** — which is the form the user and the builder can both act on.

The division of labour worth writing into the ADRs:

| Layer | Answers |
|---|---|
| **B** | which requirements and architecture nodes an edit touches, tiered certain/likely/possible |
| **C** | which packages own those nodes, what their contracts now say, what it costs, and what order to rebuild in |
| **F/E** | which files, and whether the actual diff stayed inside the set |

Layer B's own warning applies directly here and is the reason Layer C cannot just take a
transitive closure: static slices average ~30% of program size, and Nx's `affected` has a
standing discussion titled *"All projects too often affected"*. **On a six-package plan, a naive
closure from `pkg_schema` reaches every feature package — which is "the whole app" with extra
steps.** Tiering is not a refinement here; it is the difference between a useful answer and none.

Two prior arts Layer C needs that Layer B does not:

| Source | What it gives Layer C | Shape |
|---|---|---|
| **Nx / Turborepo `affected`** ([nx.dev](https://nx.dev)) | the canonical algorithm at the *package* level, which is exactly Layer C's level: diff the inputs, walk the project graph, act on the reachable set | `plan.graph` is already a project graph (`decompose.py:462`). `affected(changed_nodes)` is a reachability query over it |
| **OpenSpec** ([Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), MIT) | a *notation* for the delta: `ADDED` / `MODIFIED` / `REMOVED` sections, brownfield-first, merged into a source of truth at archive time | the vocabulary for the plan diff the user approves at the second gate. **Do not invent one.** Its explicit design goal is that a reviewer verifies intent by reading the delta rather than reverse-engineering it from generated code — which is Scio's second gate, stated by someone else |

Bazel and Nx also settle a design question Scio has never asked out loud: **dependency
granularity is a choice with a known trade-off.** Bazel and Buck2 model dependencies at
file/target level — precise, expensive, hermetic; Nx and Turborepo model them at package level —
faster to adopt, less precise, and prone to the over-approximation above. Scio is at package
level. That is defensible, and it should be an ADR line rather than an accident — particularly
because §3.2's split changes what "a package" means.

### 3.5 `source_field` stops at the package boundary

Layer B records `source_field` on every architecture node. `BuildPackage` (`plan.py:73`) does
not carry it. So an amended spec field cannot be resolved to the packages it affects without
recomputing the whole plan — which is precisely §3.4's problem, and the reason it is hard.

One field on `NodeRef` or a `dict[str, str]` on `BuildPackage`. It costs nothing and it is the
join key for the delta, for risk weighting (§3.3b), and for the failure loop Layer A §3.5 wants.

### 3.6 Nothing measures the plan

Same gap as Layer A, one layer down. Nothing records packages per app, expected-vs-actual
tokens per package kind, how many criteria ended unobservable, how often a build failure traced
to a planning decision, or whether `advise_grouping` ever moved anything useful.

Everything needed is already computed and discarded:

| Metric | Already exists at |
|---|---|
| packages per app, per kind | `plan.packages` |
| criteria by observability | `cover()` (`criteria.py:210`) — **8 unsupported out of 27 today** |
| plan validity, violations by rule | `validate_plan` |
| predicted vs actual output tokens | `expected_output_tokens` vs the build's `usage` |
| chunk splits forced in Layer E | `file_chunks` — **1 on the default app** |
| judgment consulted / applied | `GroupingAdvice` (`judgment.py:32`) |

`use_judgment=False` gives a free deterministic baseline for the whole layer, exactly as
`StandInIntakeProvider` does for Layer A. **A decomposition change that does not move these
numbers is not an improvement, it is an expense.**

### 3.7 The file plan is on the wrong side of the boundary

`validate.py:15` imports `planned_files` from `builder/file_plan.py`. Layer C asks Layer E what
a package's files are, and *that* is what makes a criterion "producible". Half of what makes a
contract checkable lives in the builder.

Three options, and the middle one is probably right:

1. **Move `file_plan.py` into Layer C.** It is a decomposition decision — which paths a package
   owns follows from which nodes it owns.
2. **Define "producible" without the file plan.** A criterion declares the *node kinds* it
   needs rather than path fragments; the builder maps those to paths. Layer C stops caring
   where a file lives.
3. **Leave it and document the exception.** Honest, and it stays a trap for the next person.

Option 1 also makes §3.2 natural: splitting a package by size needs the file plan anyway.

---

## 4 · Out of the box

### 4.1 The plan is invisible, and it is the best thing the layer produces

The plan reaches the user as **a part count and a price**. `intake.service.ts:342` calls
`EngineClient.plan()` with the docstring *"Layer C, for the rough part count"*, reads
`packages.length` and `estimate`, and discards the rest. `EnginePlanResponse` does not model
`validation`.

Meanwhile `PRODUCTION_READINESS_DIFF.md` §10's minimum product asks the user to see the
proposed architecture and its trade-offs before paying, and §7 lists nine things the reveal
should show — *changed packages and files*, *verified-unchanged surface*, *remaining risks*
among them.

The product flow is **conversation → spec the user approves → design window → regenerate →
full build → design window → approve → publish**. There is a gate between "spec approved" and
"full build" where nothing is currently shown, and Layer C already computes everything that
belongs there:

- what will be built, as parts, in order
- what each part must be true of when it is done (§3.3 makes those sentences readable)
- **which criteria nobody will check** — today 8 of 27, and the user is told none of them
- which parts come from the library and which are generated (`MatchReport`)
- the price, and now the blast radius on any later change (§3.4)

That last-but-one item is the honest one nobody ships. *"Three things in this plan cannot be
verified automatically; here they are"* is a stronger trust move than a green tick, and it costs
nothing because `scoped_out()` (`criteria.py:254`) already produces the list with reasons.

### 4.2 The layer is already a Design Rule Hierarchy — say so, and check it

`decompose.py` produces layers where members depend only upward and, within the feature layer,
are mutually independent by construction. That structure has a name — the **Design Rule
Hierarchy** (Cai et al.; grounded in Baldwin & Clark's design-rule theory) — and a measure,
MacCormack/Rusnak/Baldwin's **propagation cost**: the fraction of the system reachable from a
change to any element.

Naming it buys three concrete things:

- **`parallelizable` becomes computable** (§2.4): within-layer mutual independence *is* the DRH
  property, and the antichain is how you check it
- **propagation cost becomes the metric for a granularity change** (§3.2). Split a feature
  package and propagation cost either falls or it does not; that is an argument with a number
  in it rather than a preference
- **it is the marketing claim.** From the practitioner scan the reviews record: *"PRs containing
  AI-generated code often look perfect on the surface but are architecturally incoherent
  underneath."* A build plan that is a checked design rule hierarchy is the opposite of that,
  and Scio computes one already

### 4.3 `PackageInterface` is half a contract

Contract-based design — Benveniste, Caillaud, Nickovic et al., *Contracts for the Design of
Embedded Systems*, [Part
II](https://people.rennes.inria.fr/Albert.Benveniste/pub/ProcIEEE_contractsPart2.pdf) — defines
a component contract as an ordered pair: **assumptions** about the environment, and
**guarantees** the component provides *given* those assumptions. Refinement, composition and
compositional verification all follow from having both halves.

`PackageInterface` is guarantees only: `tables`, `operations`, `routes`, `exports`. Nothing
records what a package *assumes* — that the schema has run, that `lib/supabase.ts` exports a
configured client, that RLS is enabled before a feature relies on it. Today those assumptions
are implicit in the `dependencies` list, which says *who* but never *what*.

Adding an `assumes` field is small and it makes three current guesses checkable:

- the import boundary stops being a prose warning and becomes a derivable set
- a dependency that cannot satisfy an assumption is a plan error, found before generation —
  precisely the class `_check_criteria_are_reachable` already catches one level down
- ADR-0013's *"dependencies' interfaces, not their code"* becomes a formal claim rather than a
  convention

Honest caveat: assume/guarantee's power comes from a formal refinement calculus over behaviours,
and Scio's "behaviours" are English. What transfers is the **shape** — two-sided contracts,
checked for compatibility at composition time — not the proof theory.

### 4.4 Two package kinds are missing, and the census explains why one of them hurts

Tests are a criterion inside a feature package (`decompose.py:326`); deployment is not modelled
at all — which lines up with review finding C-F01/G-F01, no deploy or IaC anywhere.

The criteria census (§1) shows the consequence of folding tests into features: the criterion
*"Each operation has a test for its happy path and its main failure"* is `checked`, meaning a
deterministic agent reads the code — and `LAYER-E` records that **nothing runs the generated
app's own tests**. A criterion whose evidence channel does not exist is exactly what
`Observability.unsupported` is for, and this one is not marked as such.

### 4.5 The plan as a portable artifact

ADR-0001's wedge is *developer-grade output with a smooth handoff to a developer*. A build plan
— parts, order, contracts, criteria, what was assembled versus generated — is the single most
handoff-shaped thing the system produces, and it currently exists only as a `dict[str, str]` of
prompts inside a saved workspace.

The prior art here is a warning as much as an invitation: GitHub Spec Kit's
constitution → specify → plan → **tasks** → implement loop reached 111k stars by mid-2026 on
markdown templates alone, and Kiro ships the same arc with EARS. Everyone in this space now has
a plan artifact. Scio's would be different in one way that matters — **it is derived and
validated, not written** — and that difference only shows if someone can read it.

Argue the maintenance cost honestly (same caveat as Layer B §4.2's architecture language): a
bespoke format nobody else emits is a surface with no ecosystem.

---

## 5 · The means — skills, MCP, repos, research

One distinction first, per `docs/next/SKILLS.md`: a **Claude Skill** helps *us* build Scio; the
product's runtime uses relays and prompts. Nothing in this table becomes product machinery for
free.

| Means | What it gives Layer C | Verdict |
|---|---|---|
| **EARS** — Mavin et al., IEEE RE'09 · [alistairmavin.com/ears](https://alistairmavin.com/ears/) | a five-template grammar whose clause slots map one-to-one onto `Script` steps (§3.3a). Already adopted upstream in Layer A §4.4 / Layer B §3.3 | **adopt** — as the *consumer*; the choice is not Layer C's to make → skill written |
| **Design Rule Hierarchy / DSM propagation cost** — Baldwin & Clark; MacCormack, Rusnak & Baldwin, [HBS 08-038](https://www.hbs.edu/ris/download.aspx?name=08-038.pdf) | names the structure `decompose.py` already builds; gives the metric a granularity change must move | **adopt** (§2.4, §3.2, §4.2) → skill written |
| **CodePlan** — Bairi et al., MSR, PACMSE 2024, [2309.12499](https://arxiv.org/abs/2309.12499) | incremental dependency + change-may-impact + adaptive planning → plan graph. The neuro-symbolic pattern behind the plan delta | **adopt — but the skill belongs to Layer B**, which owns impact analysis (B §3.1). Writing a second one here would be inventory, not knowledge |
| **VAL** — Howey, Long & Fox, ICTAI 2004 · [KCL-Planning/VAL](https://github.com/KCL-Planning/VAL) | the validator-as-gate shape: binary verdict plus the *first* failing precondition, in words | **adopt the shape** (§3.1). Not the tool — PDDL is not our formalism |
| **Nx `affected` / project graph** — [nx.dev](https://nx.dev) | the canonical affected-set algorithm over a project graph; also the package-vs-file granularity trade-off, stated | **adopt the algorithm** (§3.4). Not the tool |
| **OpenSpec** — [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | `ADDED`/`MODIFIED`/`REMOVED` delta markers, brownfield-first. A notation we would otherwise invent | **adopt the notation** (§3.4) |
| **Modularization Quality / Bunch** — Mancoridis et al., ICSM 1998 | decomposition as graph partitioning with a single cohesion-vs-coupling score | **later** — the right metric once §3.2 gives something to optimise; premature before |
| **Agentless** — Xia et al., FSE 2025, [2407.01489](https://arxiv.org/abs/2407.01489) | hierarchical localise-then-repair beat every open-source agent on SWE-bench Lite at $0.34/issue. Empirical support for "rules first, model only where rules ran out" | **later** — it validates the existing design; it does not change it |
| **Gherkin / Cucumber** | Given/When/Then plus a runner | **not for this layer** — Scio has a runner (`core/interaction`); EARS gives the grammar without the ceremony |
| **PDDL planners** | provably valid plans over typed actions | **not for this layer** — the dependency graph is a DAG with six node kinds; Kahn is sufficient and free |
| **Bazel / Turborepo / Nx as tools** | build execution, caching, remote execution | **not for this layer** — Scio plans one app's first build, not an incremental monorepo. The *ideas* are adopted above; the tools are not |
| **MCP: dependency/code-graph servers** — [code-graph-mcp](https://github.com/sdsrss/code-graph-mcp), [dependency-mcp](https://github.com/mkearl/dependency-mcp) | tree-sitter AST graph, call-graph traversal, impact analysis over a repo | **not for this layer** — they analyse *existing* code; Layer C plans code that does not exist yet. Genuinely useful for Layer E/F verification, and for `graph-guard` on Scio's own repo |
| **GraphRAG** — Edge et al., [2404.16130](https://arxiv.org/abs/2404.16130) | local vs global search over a graph with pre-generated community summaries | **later** — the right shape for §6's `why_slice`, but the whole is a few paragraphs, not a corpus. It arrives with the spec corpus (Layer A §8) |
| **`graphify`** (ours) | corpus → queryable graph | **not for this layer today**, same reason. Note the standing drift hazard in `SKILLS.md` |
| **Batch API** — 50% cost, results by `custom_id` | the payoff for §2.4's antichain | **later** — correct `parallelizable` first; the flag is currently a guess (§7) |
| **Volere shell + fit criterion** — [volere.org](https://www.volere.org/templates/volere-requirements-specification-template/) | every requirement carries the benchmark that decides whether it was met | **already built, unknowingly** — `produced_by` × `observed_by` is a fit criterion. Adopt the *name*, so the layer's best idea has a citation |
| **ISO/IEC/IEEE 29148:2018** — [standard](https://www.iso.org/standard/72089.html) | 11 characteristics of a good requirement; Layer A §2.6 adopts the vocabulary | **later** — the natural vocabulary for what `_check_contracts` is groping at |
| **Anthropic prompt caching** — [docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) | 512-token floor on Opus 5, ~0.1× reads, 4 breakpoints | **adopt** (§7.1) — but only after §2.2 puts the constants in the prefix |
| **DSPy** | optimise prompt programs against a metric | **not for this layer** — the layer is mostly rules; there is one model call and it is bounded and grounded |

**Skills specific to Layer C**, for the build process:

- `plan-metrics` — runs §3.6's numbers with `use_judgment=False` against a fixture set and
  prints the table. Blocked on nothing; it is a script around functions that already exist.
- One new research skill, per `SKILLS.md`'s four-part format — plus one addition to an existing
  one rather than a second copy of it.

Changes made to `.claude/skills/` while writing this document:

| Skill | Change | Rests on | Used by |
|---|---|---|---|
| `design-rule-hierarchy` | **new** — layering, antichains, propagation cost, and the six evals a granularity change must pass | Baldwin & Clark; MacCormack, Rusnak & Baldwin; Cai et al.; Mancoridis et al. | C-3, C-7 |
| `ears-requirements` | **§6 appended** — the EARS-clause ↔ `Script`-step mapping, four criteria-authoring rules, and two evals (observability-preserving rewrite; refusal) | Mavin, Wilkinson, Harwood & Novak, RE'09 | C-4 |

**Two skills were deliberately *not* written**, and the reasons are the point:

- **No `ears-criteria`.** `ears-requirements` already exists and its description already covers
  writing acceptance criteria. A second EARS skill would be inventory, and two skills with
  overlapping descriptions degrade the trigger accuracy of both. The genuinely new content — the
  clause↔mechanism table, which is an argument from mechanism rather than from convention —
  belongs *inside* that skill, and that is where it went.
- **No `codeplan-impact`.** `change-impact-analysis` already exists and already carries Arnold &
  Bohner, Chianti, CodePlan and ProReFiCIA. Layer B owns that research; duplicating it here would
  be exactly the "skill for a paper nobody used" that `SKILLS.md` warns about.

Two applications of the honesty rule are worth restating, because they are the ones a reader
would otherwise get wrong:

- **Propagation cost and MQ were validated on file-level dependency graphs of shipped code.**
  Scio's graph is a *plan* of 5–20 packages that do not exist yet. The direction of change is the
  signal; the absolute number is not.
- **EARS was validated for human requirements review in safety-critical systems.** That
  structured criteria improve *generated code* is a hypothesis, unmeasured here. Neither skill
  may claim more than its source shows.

---

## 6 · Retrieval versus packing

**Where does this layer send context it could have queried?**

Two places, and one of them is the worst instance in the system.

### 6.1 `why_slice` packs the entire whole into every package

`why_slice` (`contract.py:16`) attaches one canned sentence per `PackageKind` plus the whole
narrative, unsliced, to all six packages. Its docstring defends this:

> The whole is prose, so we don't try to cut it cleverly… Wrong-but-confident slicing would be
> worse than carrying two extra paragraphs.

**That was the right call when the alternative was asking a model to cut prose**, and Layer B
§2.6 reaches the same verdict from the other side: *"The comment is not wrong; it is a consequence
of §3.3 being missing."*

It stops being the only alternative the moment the whole contains identified requirements. A
package owns `operation:create_booking` and `screen:/booking`; the requirements naming them are a
**lookup**, not a judgement. Until then, the weaker version is already available: `Whole.grounding`
maps sentences to the facts that support them (Layer B §2.1 proposes typing it), and
`arch.vocabulary` gives the canonical terms to match on — so a term-match slice with a
whole-narrative fallback is buildable today and gets strictly better when Layer B lands.

That makes the slice deterministic, cheap and wrong-in-a-recoverable-way: a sentence matched by
mistake costs a few tokens; a sentence *missed* falls back to including the whole. Keep the
fallback — the docstring's fear is correct about the failure mode, just not about the method.

And it uses the `arch` argument that `ruff` currently flags as dead (§2.6). The signature was
right; only the body gave up.

GraphRAG's local search is exactly this shape — entities as entry points, walk to neighbours —
and it is worth adopting *when there is a corpus*. There is not. A grounded lookup over one
narrative is the version that fits today.

### 6.2 The playbook is packed six times and never varies

`house_rules` is `book.as_prompt_section()` — 667 tokens, measured, byte-identical in every
package on every build for every user. It is packed six times because it is *sent* six times,
which is unavoidable; the fix is caching, not retrieval, and it needs the reordering in §2.2 to
be possible at all. This is Layer B §6's observation seen from the receiving end — it names the playbook and
`why_slice` as *"the system's worst packing violation"*, and this is where both land.

### 6.3 Where packing is correct

The architecture slice, the dependency interfaces and the criteria are per-package and all
relevant. `PackageInterface` is already the retrieval answer to *"what do my dependencies
provide"* — names and shapes instead of code, asserted by
`test_dependencies_contribute_interfaces_not_implementations`. That test is the layer's proof
that it understands the distinction; §6.1 is where it stopped applying it.

---

## 7 · Token economy

Measured 2026-08-26 against real prompts assembled from `derive_architecture(booking_spec)`,
six packages, an 822-character whole. Token figures are chars ÷ 4 unless stated; use
`messages.count_tokens` before pricing anything on them.

| Package | prompt chars | ≈ tokens | of which `why` | of which house rules | package-specific |
|---|---:|---:|---:|---:|---:|
| `pkg_foundation` | 4,971 | 1,242 | 226 | 667 | 349 |
| `pkg_design_tokens` | 5,402 | 1,350 | 224 | 667 | 459 |
| `pkg_schema` | 5,730 | 1,432 | 223 | 667 | 542 |
| `pkg_auth` | 5,336 | 1,334 | 227 | 667 | 440 |
| `pkg_connector_notifications` | 5,189 | 1,297 | 225 | 667 | 405 |
| `pkg_feature_booking` | 6,272 | 1,568 | 226 | 667 | 675 |
| **total** | **32,900** | **8,225** | | | |

**65% of Layer C's prompt output is the same bytes six times.** `why` + house rules = 5,358 of
8,225 tokens. The package-specific content — the entire reason the layer exists — is 2,870.

Three consequences, in order of size.

### 7.1 The repetition is a caching win, not a waste — but only after §2.2

These contracts are not sent once. They are the *prefix* of every codegen call in Layer E, and
a feature package alone is 2–3 chunked calls (§3.2) plus up to `max_attempts = 3` repair
rounds. The same 892-token constant block is therefore re-sent on the order of 20–30 times per
build.

Caching is a strict prefix match; cache reads cost ~0.1× and a write ~1.25×; at most four
breakpoints per request. **The minimum cacheable prefix is model-dependent and non-monotonic** —
Layer A §7.3 corrects the "~1,024 everywhere" assumption:

| Model | Minimum cacheable prefix |
|---|---:|
| **Claude Opus 5** (the default path) | **512** |
| Opus 4.8, Sonnet 5 | 1,024 |
| Opus 4.7 | 2,048 |
| Opus 4.6, **Haiku 4.5** | **4,096** |

That changes the conclusion in Layer C's favour. The 892-token constant block **clears the Opus 5
floor by 1.7×** as it stands — no design section required. Today the constants sit at the **end**
of the contract prompt (`contract.py:192-198`), so none of that is reachable. Moving them to the
front is the entire change.

Three things follow, and all three belong in the ADR:

- **a test asserting the constant prefix stays above the floor of the model it will run on.** The
  hazard is not growth, it is routing: sending codegen to Haiku 4.5 raises the floor eightfold
  and silently caches nothing
- **verify with `usage.cache_read_input_tokens`.** Zero across packages means something in the
  prefix varies — and `dict(arch.vocabulary)` (`contract.py:135`) is an ordering hazard worth
  checking first
- **the win is multiplied by re-sends, not by package count.** Layer B's **B-6** proposes caching the playbook prefix and measures it at 668 tokens —
  *"the playbook alone… will not cache"*. Combined with the whole, the vocabulary and the scope
  guard, as §2.2 arranges them, it does

### 7.2 The layer's own model call is negligible; the plan it produces is not

`advise_grouping` sends the package list and the loose operations — a few hundred tokens, at
`temperature=0.0`, one pass, and it fires **only** when `pkg_feature_general` exists
(`judgment.py:41`). On the canonical booking app it never runs.

The plan Layer C hands over, by contrast, sets the cost of the entire build:
`estimate.py`-calibrated real runs put a five-package build at **$1.42 in 14 minutes**, and a
seven-package build at **$2.69 against a $1.39 point estimate** (`estimate.py:98-104`). The
feature package at $0.857 is where the money is, and §3.2 is the only proposal here that moves
it.

### 7.3 Parallelism is worth 50%, and the flag that would unlock it is a guess

The Batch API costs 50% of standard rates. Feature and connector packages are marked
`parallelizable` — by `len(group) > 1`, not by any graph property (§2.4). `orchestrate.py:19`
acknowledges the flag is unproven; `STRATEGY.md:111` already plans to route on it.

Order matters: compute the antichain first, then batch. Batching packages that were wrongly
flagged independent produces a build where a feature is generated against an interface its
dependency had not yet declared — a failure that would surface as incoherent code rather than
as an error.

### 7.4 Effort routing

There is one model call and it is a constrained classification: *"answer only with package ids
from this list, one per line."* Its output is parsed by `_parse` (`judgment.py:57`), which drops
any line not naming both a real loose operation and a real package, and any exception at all
leaves the deterministic grouping standing.

That is the safest possible place for a cheap model: bounded output, validated parse,
deterministic fallback. Current list rates per MTok — Opus 5 $5/$25, Sonnet 5 $2/$10, Haiku 4.5
$1/$5. **Decide it with §3.6's harness, not by argument**: run both, compare how often advice is
applied and whether the resulting plans validate.

---

## 8 · Data worth owning

Layer C produces the most *structured* data in the system and keeps none of it beyond the saved
plan.

| Data | Why it is worth having |
|---|---|
| **The plan, with its validation result, keyed to the architecture that produced it** | the eval set for every decomposition change. Free — both objects already exist at `service.py:88` |
| **Predicted vs actual output tokens per package** | `estimate.py:36` says outright that the low band is optimistic and *"fixing it properly… needs a real run to calibrate against rather than a coefficient invented here (B115)."* Every build produces exactly that datum and discards it |
| **Which criteria ended `unsupported`, per package kind** | 8 of 27 today. This is the list of things Scio promises and does not check, and it is the roadmap for evidence channels in priority order |
| **Chunk splits forced in Layer E** | the direct measurement of Layer C granularity error. One on the default app |
| **Grouping advice: consulted, applied, and whether the plan still validated** | the only evidence that the layer's single model call earns its place |
| **Build failures traced back to a planning decision** | needs §3.5's `source_field` on the package. Closes Layer A §3.5's loop: intake field → architecture node → package → failed criterion |
| **Architecture shape → package shape, per app-kind** | the moat, one level down from Layer B §8. After fifty booking apps you know what a booking app's plan looks like — which makes granularity, criteria and estimates all better at once, and cannot be bought |

None of it needs new collection. It needs not throwing away what already passes through.

Same constraint as everywhere else: this is derived from user data, and ADR-0019 (deletion and
retention) is still **Proposed**. Settle what survives a project deletion before the corpus
accumulates, not after.

---

## 9 · ADR proposals

| # | Proposal | Decides |
|---|---|---|
| **C-1** | **Arm the interaction channel across the B→C seam** | whether `_fillable` falls back to table columns, or `derive.py` stops emitting `payload: json` — and adds an invariant tested against real Layer B output, not a fixture |
| **C-2** | **Plan validation becomes a gate** | errors block, warnings do not; the message is the *first* failing rule, in the user's language. What the user sees on an invalid plan — refuse, repair, or warn — is the product half |
| **C-3** | **Size-aware granularity: per entity until too big** | uses `expected_output_tokens` and `CHUNK_TOKEN_BUDGET`, which already exist. Touches the marking→code map and library matching, which is why it is an ADR and not a patch |
| **C-4** | **Acceptance criteria in EARS, weighted by provenance** | adopt Mavin et al.'s five templates rather than inventing a grammar; carry Layer A's `stated`/`derived`/`default` into the criteria |
| **C-5** | **Contract prompt reordered: constants first, criteria last** | a caching decision and an attention decision in one edit. Plus a test asserting the constant prefix stays above the ~1,024-token cache floor |
| **C-6** | **A plan delta operation** | `(amended architecture, existing plan) → ADDED/MODIFIED/REMOVED` — Nx's affected algorithm over `plan.graph`, OpenSpec's notation, tiered per Layer B §3.1. **Requires C-8 and Layer B's B-1**; it is B-1's second half, not a separate feature |
| **C-7** | **`parallelizable` computed from the dependency antichain** | before anything routes through the Batch API on the strength of the flag |
| **C-8** | **`source_field` travels into the package** | one field. The join key for C-6, for C-4's weighting, and for the failure loop |
| **C-9** | **Coverage is a partition, and it is bidirectional** | no node owned twice; no slice entry without a node. Closes a reproduced silent-overwrite path |
| **C-10** | **Who owns the file plan** | move `file_plan.py` into Layer C, or redefine "producible" without it. C-3 needs an answer |
| **C-11** | **The plan is shown at the second gate** | including which criteria nobody will check. Product decision |
| **C-12** | **Plan metrics before any decomposition change ships** | `use_judgment=False` is the free baseline, exactly as `StandInIntakeProvider` is for Layer A |

**Ordering.**

**C-1 first, and it is not close.** The layer's strongest mechanism is switched off on every
build, the fix is small, and nothing else in this document is worth more than turning it back
on.

**C-12 next**, for the same reason A-3 comes first in Layer A: it is what makes every other
proposal decidable rather than arguable. **C-5** after that — it changes no behaviour and saves
money at a multiple of package count. **C-9** and **C-8** are both one-rule-and-one-field and
unblock later work.

Then the two that change what the user experiences: **C-2** and **C-3**. C-3 needs C-10
answered first. **C-4** follows C-8 because the weighting needs the provenance.

**C-6** is the largest and it lands last — after C-8 and after Layer B's **B-1**. It is the
mechanism behind the product's central promise, and building it before the plan is measurable
(C-12) and traceable (C-8) would be shipping the interesting half of a feature whose foundations
are missing.

**One dependency across documents, stated plainly:** C-4 and C-6 both wait on Layer B. C-4 needs
identified requirements (B §3.3) before criteria can reference them; C-6 needs the tiered impact
set (B §3.1) before a plan delta can be anything but a transitive closure. Everything else in this
list — C-1, C-2, C-3, C-5, C-7, C-9, C-10, C-11, C-12 — is Layer C's alone and blocked on nothing.

**Two open questions I could not settle from the code:**

**a. Who owns library matching and pricing?** `run_layer_c` does four jobs — decompose,
library-match, validate, price — and only the first and third are decomposition. This is the
same question `00-INDEX.md` raises about `D → B` (26) and `D → C` (22), from the other side,
and the two should be answered together rather than twice.

**b. Does the plan gate exist as a moment in the product?** The flow has an approval after the
spec and an approval after the design window. Whether the plan is a third gate, a section of
the first one, or something the user never sees decides whether C-2 and C-11 are features or
plumbing — and it is a product decision.

---

*Written 2026-08-26. Every code claim carries `file:line` and was checked against the working
tree. The criteria census, the package token estimates, the contract-prompt sizes, the
double-ownership reproduction and the `ruff --select ARG` output were produced by running the real
code, not read off it. Token figures are characters ÷ 4 and inherit that estimate's error bar —
`messages.count_tokens` is the correct instrument and no API key was available. Research was read
at abstract-to-method level; nothing was reproduced. Cache floors and prices are Anthropic
first-party current values. Speculation is marked as speculation. Nothing here is implemented.*
