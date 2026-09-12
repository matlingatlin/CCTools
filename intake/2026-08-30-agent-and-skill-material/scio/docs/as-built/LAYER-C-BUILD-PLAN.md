# Layer C · Build plan / decomposition — as built

Architecture in, dependency-ordered contract-bearing packages out. 9 files, 1,764 lines,
40 tests in its own two suites — all passing 2026-08-26.

Governed by **ADR-0013** and `docs/LAYER-C.md`.

---

## 1 · Purpose

Cut Layer B's architecture graph into units small enough that the model building one has
everything it needs and nothing it doesn't.

ADR-0013 states the reason: *"To build professionally (not spaghetti), the LLM must build
from small, well-bounded, well-defined packages — not 'build the whole app.'"* The same
decomposition is what makes four other things possible: marking→code mapping, directed
regeneration, cost control, and failure isolation.

`decompose.py:8` puts the granularity choice plainly: *"Per file would be too fine to stay
coherent; per app would be the huge-context failure mode Scio exists to fix."*

## 2 · Public surface

**Engine** (`apps/engine/src/scio_engine/main.py`)

| Endpoint | Does |
|---|---|
| `POST /plan` (`main.py:318`) | architecture in → validated, ordered plan with assembled prompts |
| `POST /estimate` (`main.py:302`) | the same planner, run only for the price |

**Python** — `run_layer_c()` (`service.py:43`) returns `LayerCResult{plan, validation,
grouping_advice, prompts, library, estimate}`. The build pipeline calls it directly
(`builder/pipeline.py:214`) and hands `layer_c.prompts` to the orchestrator as `contracts`
(`pipeline.py:273` → `orchestrate.py:380`).

**API** (NestJS) — one caller. `EngineClient.plan()` (`engine.client.ts:469`) is used from
`intake.service.ts:342`, and its docstring says what for: *"Layer C, for the rough part
count."* It reads `packages.length` and `estimate` and discards the rest. The API's
`EnginePlanResponse` interface (`engine.client.ts:215`) does not even model `validation`.

**Frontend** — none of its own. The plan reaches the user as a part count and a price on the
review screen.

## 3 · In and out

**In** — a Layer B `Architecture`, the approved `whole` narrative, and the `Playbook`.

**Out** — a `BuildPlan{packages, order, graph}` (`plan.py:114`) where each `BuildPackage`
(`plan.py:73`) is one contract, plus a `PlanValidation` and one assembled prompt per package.

Six package kinds, fixed (`plan.py:19`): `foundation`, `schema`, `auth`, `feature`,
`connector`, `design_tokens`. Nodes are addressed as `kind:name` — `screen:/booking`,
`table:booking` (`plan.py:28`), *"Stable, addressable identity is what makes coverage
checkable and what the marking→code coupling later hangs on."*

### How completely the "build contract" idea is implemented

ADR-0013 lists seven things each package must carry. Measured against the prompt actually
produced by `contract_prompt()` (`contract.py:140`):

| ADR-0013 clause | Where | Actually there? |
|---|---|---|
| goal | `decompose.py`, per kind | **Yes** — a template sentence filled from the architecture |
| the architecture slice it owns | `architecture_slice_text` (`contract.py:50`) | **Yes**, in full detail — columns, FKs, RLS flag, operation inputs/outputs, screen routes and roles |
| dependencies' *interfaces*, not their code | `PackageInterface` (`plan.py:47`), `dependency_interfaces` (`contract.py:37`) | **Yes**, and tested: `test_dependencies_contribute_interfaces_not_implementations` asserts `"tables: booking" in prompt` and `"CREATE TABLE" not in prompt` |
| the relevant "why" slice of the whole | `why_slice` (`contract.py:16`) | **No.** One canned sentence per `PackageKind` plus the *entire* whole, unsliced |
| house rules | `playbook.as_prompt_section()` | **Yes** — stack, folders, secure-by-default, tests, a11y, naming |
| canonical vocabulary | `dict(arch.vocabulary)` (`contract.py:135`) | **Yes** |
| scope guard | `list(arch.scope_guard)` (`contract.py:136`) | **Yes**, tested: `test_the_scope_guard_travels_into_every_package` |
| acceptance criteria | `criteria.py` | **Yes, and further than the ADR asked** — see below |

So: six of seven fully, one (`why`) in name only. `why_slice`'s own docstring is honest about
it — *"The whole is prose, so we don't try to cut it cleverly… Wrong-but-confident slicing
would be worse than carrying two extra paragraphs"* — but ADR-0013 and `LAYER-C.md` both say
"slice", and no reader of those documents would learn this.

The prompt also carries an eighth thing the ADR never asked for, an **import boundary**
section (`contract.py:160`), written from an observed failure: *"on the first real run the
foundation package imported `@/lib/env` and `@/types/supabase`, neither of which any package
produces."*

### Acceptance criteria — the part that went furthest

`criteria.py` is the strongest single idea in the layer. A criterion declares two things
about itself (`criteria.py:11`):

- **`produced_by`** — which of the package's planned files would make it true. A criterion
  nothing in the file plan produces *"is a contract bug, caught by `validate.py` before a
  single token is generated."*
- **`observed_by`** — which channel can check it: `render` (the vision loop), `validation`
  (a deterministic agent), `interaction` (a script that drives the app), `unsupported`
  (nobody).

An unsupported criterion is kept, not deleted, *"because deleting it would lose the intent…
What it must never do is fail a build"* (`criteria.py:21`). The whole module exists because
of a real run: the first build failed `pkg_foundation` on three criteria — a test runner,
env-only secrets, secure headers — that its own file plan could never produce.

`scripts.py` then converts a feature's architecture into an executable proof: fill the create
form, submit, **reload**, and look in both the page and the database (`persistence_script`,
`scripts.py:156`); the same twice as two users to prove row isolation (`isolation_script`,
`scripts.py:189`). Deterministic on purpose — *"asking a model to invent the steps would make
the one criterion that gates the build the least reproducible thing in the pipeline."*

## 4 · Invariants

Taken from the tests. Test names are the evidence.

| Invariant | Test |
|---|---|
| Every architecture node lands in some package | `test_every_architecture_node_lands_in_a_package` |
| A dropped node is an error, not a silent loss | `test_a_dropped_architecture_node_is_caught` |
| Every package is built after all its dependencies | `test_every_package_comes_after_all_its_dependencies` |
| An order that breaks dependencies is caught | `test_an_order_that_breaks_dependencies_is_caught` |
| The order is reproducible run to run | `test_ordering_is_reproducible` |
| A cycle is refused rather than half-built | `test_a_cycle_is_refused`, `test_a_dependency_cycle_is_caught` |
| Every package carries a testable contract | `test_every_package_carries_a_testable_contract` |
| Dependencies contribute interfaces, not implementations | `test_dependencies_contribute_interfaces_not_implementations` |
| The scope guard reaches every package | `test_the_scope_guard_travels_into_every_package` |
| Judgment is consulted only when the rules left something ambiguous | `test_judgment_is_not_consulted_when_nothing_is_ambiguous`, `test_judgment_is_consulted_when_something_is_ambiguous` |
| Judgment off ⇒ the plan is unchanged | `test_the_plan_stays_deterministic_when_judgment_is_off` |
| A criterion no file would produce is an error before generation | `test_a_criterion_no_file_would_produce_is_an_error` |
| A criterion nobody can observe warns, and never fails a build | `test_an_unobservable_criterion_warns_but_never_fails_the_build` |
| The shipped plan has no unproducible criteria | `test_the_shipped_plan_has_no_unproducible_criteria` |
| Script derivation is stable across runs | `test_derivation_is_stable_across_runs` |
| An operation with no screen to drive stays unobserved rather than failing | `test_an_operation_with_no_screen_to_drive_stays_unobserved` |
| No identity ⇒ no isolation criterion | `test_an_app_with_no_identity_gets_no_isolation_criterion`, `test_a_table_with_no_owner_column_gets_no_isolation_criterion` |
| Duplicate package ids are caught | `test_duplicate_package_ids_are_caught` |

Enforced in code, not only by prompt: the grouping model may answer only with ids from the
candidate list, and `_parse` (`judgment.py:57`) drops every line that does not name both a
real loose operation and a real package. Any exception at all and the deterministic grouping
stands (`judgment.py:90-98`): *"Never fails the plan."*

Ordering ties are broken by package id (`decompose.py:419`) — *"a plan that shuffles between
runs would make diffing builds impossible."*

## 5 · Dependencies

Edge counts from `graph/graph.json`, computed the same way as `00-INDEX.md`.

**Up:** `E → C` 68 (the build executes the plan), `D → C` 22 (library matching reads the
plan). Tests contribute a further ~200 edges, the largest being
`test_b054_real_run_hardening` (51), `test_layerc_service` (48) and `test_layerc_decompose`
(30).

**Down:** `C → B` 66, `C → E` 39, `C → D` 9, `C → G` 4.

The `C → E` edges are not one thing:

| From | To | Edges | Reading |
|---|---|---:|---|
| `scripts.py` | `core/interaction.py` | 22 | the script vocabulary — fine, `core` is shared |
| `judgment.py` | `execution/relay.py`, `provider.py` | 8 | the one model call — fine |
| `service.py` | `estimate.py` | 4 | Layer C prices the plan |
| `validate.py` | `builder/file_plan.py` | 3 | **Layer C asks Layer E what a package's files are** |

The last row is the one to look at. `planned_files()` (`builder/file_plan.py:42`) decides
which paths each package owns — and *that* is what makes a criterion "producible". Half of
what makes a contract checkable therefore lives in the builder, not in Layer C, and the
validator imports upward to reach it.

`C → D` (9) is `service.py:75-83` calling `match_plan` and `apply_matches`: the library is
consulted during planning, deliberately — *"knowing which parts are assembled is what makes a
build's cost and quality predictable rather than discovered."* It is also why `BuildPackage`
carries `source` and `catalog_entry` (`plan.py:89-95`), library concepts in a Layer C model.

## 6 · State

### Solid — carry forward unchanged

- **The criteria model** (`criteria.py`). `produced_by` × `observed_by`, with `judgeable()`,
  `interacting()` and `scoped_out()` deriving what each channel may be asked. This is the
  hardest-won and least reproducible thing in the layer; two failed real runs paid for it.
- **Deterministic decomposition and Kahn ordering** (`decompose.py:405`, `:418`). Free,
  reproducible, tie-broken by id, cycle-refusing.
- **Grounded, optional judgment** (`judgment.py`). One model call, only for operations the
  rules could not attach, answers restricted to existing package ids, failure falls back to
  rules. `use_judgment=False` makes the whole layer deterministic and is used by `/estimate`.
- **`PackageInterface`** (`plan.py:47`) — *"names and shapes, not implementations."* The
  single mechanism that keeps context tight, and the thing the whole decomposition is for.
- **Deterministic interaction scripts** (`scripts.py`), including their refusal discipline:
  no create operation, no screen to drive, or no identity to isolate by ⇒ no script, and the
  criterion stays recorded-but-unjudged rather than failing every build.
- **The import-boundary section** in the contract prompt (`contract.py:160`).
- **The marking→code consequence is real**, not aspirational. `data-scio-package` carries the
  owning package into the DOM (`core/instrumentation.py:25`), the manifest maps id → package
  → files, and `design/change.py` regenerates only affected packages. ADR-0013's headline
  consequence is actually delivered.

### Deliberate, and easy to break by accident

- **Deterministic-first ordering** in `run_layer_c` (`service.py:3`): *"Deterministic
  decomposition first, LLM judgment only for what the rules left ambiguous, then contracts,
  then validation — in that order, so a plan error is caught before the builder ever runs."*
- **The unsliced `why`.** Argued, with a reason (see §3). Reopening it means arguing that a
  confident wrong slice beats two extra paragraphs — a real trade, not a free improvement.
- **Unsupported criteria are kept, never deleted.** Deleting them would lose intent; failing
  on them would fail builds for things nobody looked at.

### Wrong-shaped

- **Validation is a report, nothing consumes it.** `validate_plan` runs **seven check functions**
  emitting **nine distinct `rule` identifiers** (`unique_package_id`, `node_covered`, `acyclic`,
  `dependency_exists`, `contract_complete`, `contract_testable`, `criterion_producible`,
  `criterion_observable`, `order_respects_dependencies`; `criterion_observable` is the only one that
  can be a warning). Counting call edges in the graph gives seven and is the wrong unit. Nine good
  rules, and `LayerCResult.validation` is returned by `/plan` — but no runtime caller reads
  it. `pipeline.py` goes straight from `run_layer_c` (`:214`) to `save_plan` (`:227`) to the
  build, and the API's response type does not model the field. A grep for `.validation` finds
  only `layerc` itself and tests. The only enforcement that exists is a pytest assertion
  (`test_the_shipped_plan_has_no_unproducible_criteria`) — i.e. it protects *the developers'*
  architecture fixtures, not a user's app. ADR-0013 explicitly rejected "no plan validation"
  because *"design errors would slip into code generation."* At runtime, they still can.
- **Granularity is fixed at one package per entity, with no notion of size.** A feature with
  one operation and a feature with twelve are both one package. Layer E patches this
  afterwards by chunking a package that will not fit in one reply
  (`test_a_package_too_big_for_one_reply_is_asked_for_in_chunks`) — a Layer C decision being
  repaired in Layer E, which is exactly what a missing architect pass looks like.
- **Acceptance criteria are hard-coded English, per package kind.** Everything in
  `decompose.py` is a template; nothing about *this* app's risk reaches the criteria. Layer
  A's provenance — which fields were assumed, which were stated — does not survive into a
  package contract, so a package built entirely on defaults is held to the same "done when"
  as one built on stated requirements.
- **`run_layer_c` does four jobs**: decompose, library-match, validate, price. Only the first
  and third are decomposition. This is why `/estimate` must run the entire planner to return
  a number, and why the library and cost models reach into `plan.py`.
- **`why_slice` is not a slice** (see §3), and takes an `arch` parameter it never uses.
- **The foundation package advertises what it does not build.** Its interface exports
  `"test runner"` and `"lint config"` (`decompose.py:73`) — while the comment 15 lines above
  says those were removed from its *goal* precisely because *"neither of which is in its file
  plan."* Verified: every dependent package's contract prompt reads `provides: app shell,
  navigation, supabase client, test runner, lint config`. Half the fix landed.
- **`parallelizable` is not computed.** The docstring says *"Flag packages that share no
  dependency path with a sibling of the same kind"*; the body flags every member of a group
  when `len(group) > 1` (`decompose.py:448`). It happens to be right today, because feature
  packages never depend on each other by construction — but nothing checks that, and
  `STRATEGY.md` line 111 already plans to route these packages through the Batch API on the
  strength of the flag.
- **Three unused function arguments** (`ruff --select ARG`): `contract.py:16`,
  `contract.py:125`, `decompose.py:363`. Small, but `CLAUDE.md` says "no dead code".

### Missing

- **No check that two packages don't own the same node — and it is reachable.** Reproduced
  against the real code on 2026-08-26: an architecture with one screen `/home` wired to
  operations of two entities produces

  ```
  pkg_feature_booking  ['operation:create_booking', 'screen:/home']  [... 'app/home/page.tsx' ...]
  pkg_feature_menu     ['operation:list_menu',      'screen:/home']  [... 'app/home/page.tsx' ...]
  valid: True
  ```

  Two packages own one node and both plan to write the same file. The second overwrites the
  first, and the manifest gets two owners for one path — the exact condition
  `test_the_actions_file_is_not_claimed_by_two_packages` guards for `app/actions/*.ts` and
  nobody guards for `app/*/page.tsx`. `_check_coverage` (`validate.py:43`) only asks whether
  each node is covered at least once, never at most once.
- **Coverage is one-directional.** A package may reference a node the architecture does not
  contain; `architecture_slice_text` silently skips it (`contract.py:56`, `:68`, `:78`…) and
  no rule fires. A phantom slice entry becomes an empty "build exactly this" section.
- **No metric on the plan.** Nothing records packages per app, repair rounds per package
  kind, how many criteria ended up unobservable, or how often a build failure traced back to
  a planning decision. So no change to decomposition can be shown to be an improvement — the
  same gap Layer A has.
- **No spec-field traceability in the contract.** Layer B records `source_field` on every
  architecture node, but a `BuildPackage` does not carry it forward. An amended spec cannot
  be resolved to the packages it affects without recomputing the whole plan.
- **No re-plan / plan diff.** There is no operation taking an amended architecture and an
  existing plan and returning a delta. Directed regeneration exists at the *code* level
  (`design/change.py`); at the *plan* level, an amendment re-runs everything.
- **No package kind for tests or deployment.** Tests are a criterion inside a feature
  package; deployment is not modelled at all.

### Obsolete

None found. `mark_parallelizable` produces information nothing consumes yet, but it is
recorded deliberately (*"this is the information a later scheduler needs, recorded now while
the graph is in hand"*) and `orchestrate.py:19` acknowledges it — unproven, not dead.

## 7 · Open questions

**a. Should validation be a gate?** Today it is advisory and unread. Making it a gate raises
the next question immediately: what should a user see when their plan is invalid, given the
violations are written for engineers (*"Architecture node 'screen:/x' is not built by any
package"*)? Refuse, repair, or warn — that is a product decision, not an engineering one.

**b. Is per-entity the right granularity, or should it be per-entity-until-too-big?** The
chunker in Layer E is evidence that the fixed rule already fails on large features. Changing
it touches the marking→code map, so it needs an ADR, not a patch.

**c. Who owns library matching and pricing — C, or D and E?** `run_layer_c` currently owns
both. This is the same question `00-INDEX.md` raises about `D → B` (26) and `D → C` (22),
seen from the other side, and the two should be answered together.

**d. Who owns the file plan?** `builder/file_plan.py` decides what a package may write, which
decides what its criteria can claim. Either it belongs in Layer C, or "producible" needs a
definition that does not require an upward import.

---

## Documentation drift found

**1. `docs/STRATEGY.md` §A.5 is stale.**

> **Planner (Layer B -> C).** Built — but must be extended for the library (library matching
> BEFORE the build plan).

The extension is done. `service.py:75-83` reads the catalog from the store, calls
`match_plan`, and applies the matches *before* validation and pricing, with the reason in
comment: *"The library is asked before the build, not during it."* `BuildPackage.assembled`
(`plan.py:97`) and `LayerCResult.library` exist and are tested (`test_library.py`, 15 edges
into `layerc`). §B.2's *"it must exist BEFORE the build plan"* is likewise satisfied.

**2. ADR-0013 and `docs/LAYER-C.md` claim a validated-before-building plan.**

ADR-0013: *"the plan is validated (full coverage, acyclic, valid contracts) before building"*,
with *"No plan validation — rejected; design errors would slip into code generation"* under
alternatives. `LAYER-C.md` §"Validate the plan before building" repeats it.

The validation runs. Nothing acts on it. `builder/pipeline.py:214-227` calls `run_layer_c`
and proceeds to `save_plan` and the build without reading `layer_c.validation`; a repo-wide
grep for `.validation` outside `layerc` and its tests returns nothing. The documents describe
a gate; the code has a report.

**3. ADR-0013 and `docs/LAYER-C.md` claim a "why" slice.**

ADR-0013: *"the relevant 'why' slice of the whole"*. `LAYER-C.md`: *"why — the relevant slice
of the whole"*. `why_slice` (`contract.py:16`) attaches the entire whole plus one of six
canned sentences keyed on `PackageKind`. The code's own docstring says so; the documents do
not.

**4. Internal drift — `decompose.py:442`.**

> *"Flag packages that share no dependency path with a sibling of the same kind."*

The implementation checks `len(group) > 1` and flags everything in the group. No dependency
path is examined.

**5. Internal drift — `contract.py:168`.**

The contract prompt says *"You may import ONLY from: files this package writes (listed
below)"*. No list follows — verified by rendering a real contract. The file list is appended
later by `codegen.build_prompt` (`builder/codegen.py:149`), so the reference resolves only
because Layer E happens to complete the prompt. Anything reading `/plan`'s `prompts` or the
saved plan sees a dangling forward reference.

**6. `docs/BACKLOG.md` carries the same item twice** — B030 and B035 are both *"Layer C:
build plan / decomposition (design)"*, both P0, both done. Bookkeeping only.

---

*Verified 2026-08-26 against the working tree (`hello-world` at `00408d3`; the layer itself
last changed in `f6d5ad0`, 2026-08-20). `test_layerc_decompose` (20) and
`test_layerc_service` (20) pass; `test_b054_real_run_hardening` (37) and
`test_interaction_channel` (36), which cover `criteria.py` and `scripts.py` alongside builder
machinery, pass 64 with 9 skipped (skips require Playwright). `ruff check` is clean on the
layer at its configured rule set.*

*One observation the numbers do not carry: every strong piece of this layer names the real
run that produced it — B054 in `criteria.py`, B060 in `scripts.py`, B071–B078 in
`decompose.py` and `file_plan.py`. The layer was debugged into shape rather than designed
into it. That produced unusually honest code, and it also left the seams an architect pass
would have caught: validation computed but unwired, the file plan on the wrong side of a
layer boundary, and granularity fixed in C but repaired in E.*
