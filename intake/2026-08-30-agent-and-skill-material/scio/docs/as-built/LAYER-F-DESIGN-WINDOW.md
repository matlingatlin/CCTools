# Layer F · Design window — as built

Gate 2. A running preview in, a changed preview out. 11 files, 1,614 lines. 39 engine tests
— all passing 2026-08-26. A further 23 API e2e tests and 29 frontend tests read as written
but were **not run** in this pass.

Governed by **ADR-0015** (answering a conflict) and **ADR-0017** (the delivery build promotes
the design). **ADR-0018** — what Ship, Refine and Settings are — is still *Proposed*, and §6
records what that costs.

---

## 1 · Purpose

Put the user inside their app before it is delivered, let them point at things and say what
should be different, and rebuild **only the parts they touched**.

The layer's own docstring states the job and its limit in one breath
(`design/__init__.py:1-19`):

> *"Level 2 is 'show me before you build it'. The user gets a running preview, marks things in
> it, writes what they want, and presses go — and only the parts they touched are rebuilt."*
>
> *"Everything that decides anything is already-built core code. This layer's job is to take
> several markings at once and to refuse the ones it should not act on."*

That second sentence is the honest description of the whole layer: it is a **batching and
refusal** layer wrapped around Layer E's guardrails. It owns almost no mechanism of its own.

## 2 · Public surface

**Engine** (`apps/engine/src/scio_engine/design/`)

| Callable | Does |
|---|---|
| `resolve_batch(batch, manifest)` | every marking → package/file/line, one outcome each |
| `detect_conflicts(batch, arch, allowances)` | which markings argue with the approved spec |
| `apply_change(app_dir, batch, …)` | the guarded round trip; never raises for a bad marking |
| `commit_change(app_dir, description, manifest)` | one commit per batch, returns the sha |
| `restore_version(app_dir, git_sha, package_files)` | put an earlier version's code back |

**API** (NestJS, `apps/api/src/modules/design/`)

| Route | Does |
|---|---|
| `GET  /projects/:id/design` | the current preview: url, manifest, routes, whole |
| `POST /projects/:id/design/preview` | build the preview (SSE) |
| `POST /projects/:id/design/change` | apply a batch of markings |
| `GET  /projects/:id/design-versions` | the version history, newest first |
| `POST /projects/:id/design-versions/:versionId/restore` | return to a version |
| `POST /projects/:id/design-versions` | "freeze the approved design" — **no caller anywhere** (§6) |

**Deployment** (`apps/api/src/modules/deployment/`, 63 lines across three files) — registered
in `app.module.ts:42`, routed, documented in Swagger, and both methods throw:

```ts
// deployment.service.ts:46-47
// TODO(8): workspace-scoped listing.
throw new NotImplementedException("deployment.list — phase 8");
```

`NotImplementedException` is Nest's **501**. So: yes, there are stub endpoints returning 501,
and they are the whole of the deployment module.

**Frontend** — `DesignPage.tsx` (883 lines, the window itself), `ShipPage.tsx` (131, "get the
code"), `RevealPage.tsx` (228, the trust receipt and the three actions).

## 3 · In and out

**In** — a `ChangeBatch`: a list of `Marking`s plus one batch-wide `prompt`
(`markings.py:52-72`). Each marking mirrors what the in-preview bridge sends — `scio_id`,
`scio_package`, `tag`, `text`, and separately `ancestor_id` / `ancestor_package` /
`ancestor_distance`. The ancestor's purpose is stated and bounded:

> *"including the ancestor — which exists so a refusal can name it, and for no other reason.
> Nothing here may be substituted for `scio_id`."* — `markings.py:32-35`

**Out** — a `DesignChangeResult` (`change.py:66-135`): `applied`, `conflicts[]`, `packages[]`
(with `edited_files`, `unchanged_files`, `isolated`, `accepted`, `rejection`, `rolled_back`),
`unaddressable[]`, the moved-on `manifest`, `total_cost_usd`, `compiles`, `type_problems[]`,
and `git_sha`.

Two fields carry the layer's honesty in their own descriptions:

- `git_sha` — *"Empty means it could not be committed, and therefore cannot be returned to."*
- `compiles` — *"None means nobody asked… finding out three changes later that the first one
  broke the build is the expensive version of this answer."*

**The order is the design** (`change.py:3-11`): resolve strictly → detect conflicts → ask the
model per affected package → Layer E's isolation + instrumentation guardrails. Conflicts are
checked at `change.py:261`, *before* `_edits_for` is ever called — so a conflict costs nothing.

## 4 · Invariants

Taken from the tests. Test names are the evidence. Engine tests were run
(`test_design_change.py` 27 passed, `test_design_restore.py` 12 passed).

| Invariant | Test |
|---|---|
| One bad marking never spoils the others | `test_one_unaddressable_marking_does_not_spoil_the_others` |
| An unaddressable marking is reported, not dropped | `test_an_unaddressable_marking_is_reported_and_skipped` |
| Only the marked packages are rebuilt | `test_a_batch_changes_only_the_packages_it_touches` |
| A conflict costs nothing — no tokens spent | `test_a_conflict_stops_the_change_before_a_token_is_spent` |
| A change that loses a `data-scio-id` is rolled back | `test_a_change_that_loses_an_id_is_rolled_back` |
| A package cannot edit files it does not own | `test_a_model_that_edits_a_file_the_package_does_not_own_is_refused` |
| The manifest moves on so the next marking resolves | `test_the_manifest_comes_back_so_the_next_marking_resolves` |
| Conflicts match the project's vocabulary, not strings | `test_it_matches_the_projects_own_vocabulary_not_the_literal_string` |
| The batch-wide prompt is checked for conflicts too | `test_the_batch_prompt_counts_too` |
| An applied change is a commit you can return to | `test_an_applied_change_is_a_commit` |
| Returning does not lose what came after | `test_returning_puts_the_old_code_back_without_losing_the_new` |
| A version that no longer verifies is refused *and undone* | `test_a_version_that_no_longer_verifies_is_refused_and_undone` |
| An allowance silences exactly one question | `test_the_exact_sentence_the_question_quoted_silences_it` / `test_a_different_allowance_does_not` |
| The bridge is absent from a delivery build | `test_a_delivery_build_never_registers_it` |
| The bridge reports the ancestor, never substitutes it | `test_the_bridge_reports_the_ancestor_but_never_substitutes_it` |
| A promotion delivers the files that are there | `test_a_promotion_delivers_the_files_that_are_there` |
| A promotion keeps the git history | `test_the_delivered_app_keeps_the_history_it_was_built_with` |
| A workspace with no plan is refused, not rebuilt | `test_a_workspace_with_no_plan_is_refused_rather_than_rebuilt` |

The strongest of these is the conflict test, because it asserts a negative in the only way that
counts — the registry handed in *would raise if it were ever called*
(`test_design_change.py:378-380`), and the file on disk is compared byte-for-byte before and
after.

### ADR-0017 — verified

**Claim:** "Build it" promotes the design workspace, regenerates nothing, keeps git history.

**Verified, in three places.**

1. `build.service.ts:614-635` branches once. `designToPromote()` (`:691-712`) reads the current
   design version's `ref.workspace`; if there is one, the API calls `engine.promoteBuild(…)`
   instead of `engine.streamBuild(…)`. The comment states the stake: *"Rebuilding it from the
   spec would regenerate every file the user spent the session shaping — and, on the way,
   delete the workspace the design history points at (B070)."*
2. `pipeline.py:353-473` — `stream_promotion` calls `load_plan(workspace)` (`:384`), then goes
   straight to `stream_verification`. There is **no** `prepare_workspace`, no `codegen`, no
   repair loop in the function. It serves with `preview=False` (`:465`), so the delivered app
   carries no bridge. A workspace with no stored plan raises `WorkspaceUnavailable` (`:390`)
   rather than silently rebuilding.
3. `workspace.py:390-395` — the destructive path is annotated at the site of the danger:
   *"This deletes history… Any new caller that might run against an existing project must
   promote (`stream_promotion`) rather than come through here."*

The provenance link is real too: `build.service.ts:655` writes `designVersionId: design?.id`
onto the build version. And `RevealPage.tsx:198-205` routes "Open & refine" to `/design` on
exactly this reasoning.

One thing the ADR does not say and the code confirms: a promotion re-judges with the **stand-in
registry** when the real one is fake (`pipeline.py:404`), because otherwise a free-path
promotion downgraded parts that had passed minutes earlier. Evidence:
`test_a_promotion_does_not_downgrade_what_the_build_passed`.

### ADR-0015 — verified

**Claim:** conflicts are answered inline, with exactly two answers; "Change the plan" amends
the spec; security conflicts get a second confirmation and an allowance rather than a rewrite.

**Verified.** `DesignPage.tsx:762-778` renders exactly two buttons per conflict — *"Keep it
as-is"* and *"Change the plan"* — with no third path and no link back to the wizard.

- `keepAsIs()` (`:402-411`) drops only the marking that raised the question; the rest stay.
  Where the conflict came from the free prompt (`scioId` empty) it clears the prompt instead.
- `changeThePlan()` (`:413-430`) calls `POST /projects/:id/spec/amend`, then re-runs the batch.
- `isSecurity()` (`:90-92`) routes `auth`/`access` through `setConfirming` — a second panel
  naming the protection verbatim, with *"Yes, allow it"* / *"Cancel"* (`:744-760`).
- `spec.service.amend` (`:181-245`) does the two different acts the ADR demands: `non_goal`
  filters the item out of `spec.non_goals` and stamps provenance `"dropped in the design
  window: …"`; anything else appends to `assumptions.allowances` and **leaves the posture
  alone**. Both write an `amendments[]` audit row with kind, sentence, note and timestamp.
- `allowancesOf(spec.assumptions)` is passed back into the engine on the next change
  (`design.service.ts:393`), and `detect_conflicts` filters on the exact case-folded
  `spec_says` string (`conflicts.py:206`).

Tests: `it("'Change the plan' amends the spec, then applies")`, `it("asks a second time before
dropping a protection, and names it")`, `it("records a security decision as an ALLOWANCE,
leaving the posture alone")`, `it("does not fail when the same conflict is answered twice")`.

**One gap worth naming.** The second confirmation is **browser-only**. `AmendSpecDto`
(`spec.controller.ts:27-30`) has no `confirmed` field, and `spec.service.amend` performs an
`auth`/`access` allowance on a single POST. The two-step is a UI convention, not an enforced
invariant — unlike intake's `corrected-on-review` mark, which is enforced in code.

## 5 · Dependencies

Recomputed from `graph/graph.json` and reproduced exactly: **F → G = 73**, **F → E = 70**
(assigning `apps/api/src/engine/engine.client.ts` to E and `apps/api/src/common` to G, which is
the only split that yields the index's figures).

**F → G (73) is almost entirely type imports.**

| Target | Edges |
|---|---:|
| `packages/shared/src/{dtos,intake,index,entities}.ts` | **51** |
| `apps/api/src/auth/{auth-context,workspace-scope}.ts` | **16** |
| `apps/api/src/common/sse.ts` | 3 |
| `apps/api/src/prisma/prisma.service.ts` | 3 |

`dtos.ts` alone is 40 edges. `CurrentWorkspace` is the single most-referenced symbol (10). So
the largest edge count in the whole graph after `D → E` is **request/response DTOs and the
tenancy decorator** — plumbing, not coupling. It says the layer is a thin HTTP skin over the
engine, which is what it claims to be.

**F → E (70) is where the real weight is**, and it is *reuse of Layer E's guardrails*:

| Target | Edges | What is borrowed |
|---|---:|---|
| `builder/persistence.py` | 10 | `git()`, `ensure_repo()` — versioning is git, not a table |
| `execution/relay.py` | 8 | `run_relay`, `RelayOptions`, `Spend` |
| `builder/typecheck.py` | 6 | "does it still compile" after a change and after a restore |
| `api/src/engine/engine.client.ts` | 6 | every engine call the API makes |
| `core/instrumentation.py` | 6 | `Manifest` |
| `core/regenerate.py` | 5 | **`directed_regenerate`** — the isolation proof |
| `builder/codegen.py` | 5 | `FIX_SYSTEM`, `extract_files` |
| `core/resolver.py` | 5 | **`resolve_marking`** — the strict resolver |
| `execution/provider.py` | 4 | `ProviderRegistry` |
| `core/{persistence,stamping,manifest_builder,verifier}.py`, `execution/untrusted.py` | 12 | `ManifestStore`, `stamp_files`, `build_manifest`, `verify_instrumentation`, `fence` |

**Answer to "what is the design window leaning on so heavily":** it leans on **git and on
Layer E's four guardrails** — `resolve_marking` (strict resolution), `directed_regenerate`
(isolation + rollback), `verify_instrumentation` (a restore is a write), and `typecheck`. It
originates none of them. The 1,614 lines are the batching, the conflict rules, the version
bookkeeping and the HTTP surface; the correctness lives one layer down. `change.py:12-14` says
so outright: *"The last step is the core's `directed_regenerate`, unchanged."*

Two smaller edges are worth naming: **F → B (13)** — `layerb/architecture.py` (10) and
`layerb/vocabulary.py` (3), because conflict detection reads the derived architecture and
canonicalises through the same vocabulary Layer A shares; and **F → A (3)** —
`spec.service.ts`, for `allowancesOf`. Both are legitimate: they are how a conflict is decided
in the user's own words rather than by string match.

## 6 · State

### Solid — carry forward unchanged

- **Per-marking honesty.** `ResolvedBatch` gives every marking its own outcome
  (`markings.py:74-117`). The reasoning is written down and is right: *"Failing the whole batch
  would teach people to mark one thing at a time; silently dropping it would apply a change
  they asked for and never mention that one part was ignored."*
- **Conflicts are asked, never resolved.** Deterministic, narrow, and deliberately model-free:
  *"It never asks a model whether something is a contradiction, because a model that is merely
  usually right here would sometimes block a legitimate change and sometimes wave through the
  one thing the user asked us not to do."* (`conflicts.py:16-21`) Checked before any spend.
- **The allowance mechanism.** One frozen sentence silences one question and nothing else. It
  is the only way a conflict stops being one (`conflicts.py:193-206`), and it leaves the
  security posture intact. This is the wedge from ADR-0001 defended in the one place a side
  panel could quietly undo it.
- **A restore is a write.** `restore.py` rebuilds the manifest from the restored source,
  re-verifies instrumentation, and rolls the working tree back if it fails. History moves
  forward — `read-tree -u --reset` then commit on top of HEAD — so *"the version you came from
  is still a commit."*
- **Promotion (ADR-0017).** Verified above. This is the layer's most valuable single decision:
  it made a delivery cheap and made the user's work survive it.
- **The bridge boundary.** The spike's finding 2 — *"the bridge must stay dumb"* — is honoured:
  `describe()` reports the ancestor separately and Python decides. `test_the_bridge_reports_
  the_ancestor_but_never_substitutes_it` guards it.
- **Preview lifecycle as a four-state union** (`DesignPage.tsx:39-56`). Replaced six booleans
  and 2^6 reachable combinations for four real states.

### Deliberate, and easy to break by accident

**Conflict detection is regex + canonical vocabulary, not judgement.** `_WANTS` / `_REMOVES` /
`_AUTH_WORDS` / `_ACCESS_WORDS` (`conflicts.py:35-58`) are word lists — including Swedish
(`lägg till`, `ta bort`, `inloggning`, `öppen`). It will miss conflicts phrased unusually. That
is the accepted cost of never having a model block a legitimate change, and the docstring
states what is deliberately out of scope: *"anything requiring judgment. A note that quietly
widens scope, or that is a bad idea, is not this function's business."* Any proposal to make
detection smarter trades a guarantee for coverage and needs an ADR.

**The change relay gets one accumulator for the whole batch** (`change.py:251`, `:206`).
`Spend` is shared and mutable on purpose (`relay.py:96-109`) — a per-call ceiling authorised
the ceiling once per call, which is how a "$3.76 build ceiling" licensed ~$50. Reverting to a
per-call budget here would silently reopen that.

**A rejected package does not stop the others** (`change.py:290-322`), for the same reason a
bad marking does not fail the batch.

### Wrong-shaped

- **The change budget is a hard-coded constant in the API.**
  `design.service.ts:139` — `private static readonly CHANGE_CEILING_USD = 2.0`. The comment
  admits it is a placeholder: *"Flat rather than derived from the estimate: the estimate prices
  a BUILD, and a change is a different unit of work that nobody has quoted."* It is not
  configurable, not per-workspace, not per-plan, and no test asserts it stops anything.
- **The design version's `ref` is a JSON blob in a text column.** `record()` writes
  `JSON.stringify(ref)` (`:169-183`) and every reader does `JSON.parse` inside a try/catch that
  returns `{}` on failure (`refOf`, `:198-205`). A ref that fails to parse degrades to "no
  workspace", which in `build.service.designToPromote` silently means **a full rebuild** —
  precisely the data loss ADR-0017 exists to prevent, reached by a different door. The comment
  there is honest about the choice (*"Fall through to a full build rather than guessing at a
  path"*) but the failure mode is the expensive one.
- **`compiles` is a tri-state carried by hand through four hops** (engine result → API DTO →
  page state → notice string), with `?? null` at each. The typing is fine; the fact that the
  same question is answered independently after a change (`change.py:330`) and after a restore
  (`restore.py:104`) means the answer has two owners.
- **Deployment is a module, not a stub.** Three files, a Swagger tag, a route table and a
  DI-wired service, all so that two methods can throw 501. It is shaped like something that
  works. A single `NotImplementedException` in the controller, or no module at all, would
  mislead less.

### Missing

- **No test asserts the layer's own metering.** `meter()` (`design.service.ts:141-157`) writes
  `usage_event` rows of kind `preview` and `design_change`, and its docstring says the ledger
  *"billing will rest on"* could not previously see the interaction people spend most of their
  time in. `design.e2e.spec.ts` builds a `usageEvents` store (`:42`, `:91-93`) and **never
  asserts on it**. The most commercially load-bearing write in the layer is untested.
- **No test exercises the `$2.00` ceiling.** No `budget_usd` or `ceiling` reference exists in
  either engine design test file.
- **Most of the promised toolset.** `STRATEGY.md` §D names seven design-window tools; the code
  has three — mark→describe, free prompt, undo/versions. **Smart property controls, global
  style tokens, reference upload ("like this" with an image), and test/interact are absent
  from the codebase.** Nothing in `DesignPage.tsx` reads a design token or accepts an upload.
- **No metric for the flagship loop.** Nothing measures how often a directed change is accepted
  first time, how often a package is rolled back, how often a marking is unaddressable, or what
  a change costs on average. This is the interaction the product is differentiated by, and no
  change to it can be shown to be an improvement.
- **The second security confirmation is not enforced server-side** (§4).
- **Marking in a scrolled or responsive frame** — explicitly left unsettled by the spike
  (*"Everything was above the fold at one viewport"*) and still unaddressed.
- **The label-collision wrinkle** the spike asked gate 2 to fix (*"labels collide when two
  marked elements are close together. Offset or flip them"*) — I could not verify either way
  from `DesignPage.tsx`, because the marker is drawn inside the preview by the bridge, which is
  outside this layer's files.

### Obsolete

- **`POST /projects/:id/design-versions` — "Freeze the approved design as a new version"**
  (`design.controller.ts:94-102`, `design.service.freeze` `:579-590`). Grepped across
  `apps/app`, `apps/api`, `packages/shared` and both test suites: **nothing calls it**. The API
  client (`apps/app/src/lib/api.ts:178-181`) exposes list and restore only. It writes a design
  version with `{approved: true, ref: body.ref}` — a shape no reader understands, since every
  other reader expects `workspace` / `previewUrl` / `manifest` / `packageFiles`. If it were
  ever called it would create a *current* design version with no workspace, which
  `designToPromote` would then read as "nothing to promote" and rebuild from scratch. Dead, and
  dangerous if revived.
- **The `/live` "Refine" placeholder route** (`App.tsx:17`). ADR-0018 records that this needed
  no decision and is already wired — the reveal's "Open & refine" goes to `/design`
  (`RevealPage.tsx:203`). The `/live` route still renders `PlaceholderPage` with *"This screen
  is being ported from the prototype next."* Nothing links to it; it should be deleted or
  redirected.

### What Ship and Settings actually do today (ADR-0018 is only Proposed)

- **"Open & refine"** — real. Routes to the design window. Needed no decision (ADR-0018 §1).
- **"Get the code"** — `ShipPage.tsx` is a real screen, not a placeholder. It shows version,
  commit sha, build time and honest status, then a "Not built yet" block naming three things
  individually: downloading the repository, pushing to your own remote, publishing
  (`:104-122`). **No download and no push exist** — there is no endpoint for either. The screen
  is honest rather than functional, which is what the ADR proposed and is the correct
  intermediate state.
- **"Publish"** — not built. `RevealPage.tsx:218-222` says so in one sentence on the screen.
  The backing module is the 501 stub described above.
- **"Settings"** — **still a placeholder.** `App.tsx:19` maps `/settings` to `PlaceholderPage`,
  which renders *"This screen is being ported from the prototype next."* (`PlaceholderPage.tsx:13`).
  Nothing from ADR-0018 §3 — spend, what is running, how to stop it — exists. `SCIO_MODEL_PASSES`
  remains an operator env var, as the ADR predicted.

So: of the reveal's three actions, two are real and one is named-as-unbuilt. Settings is
unchanged since before the ADR. ADR-0018's *consequences* are already visible in the product
even though the ADR has not been accepted — which means the code is running ahead of its own
governance, not behind it.

## 7 · Open questions

**a. Does ADR-0018 get accepted, amended, or overtaken?** The reveal already behaves as if §1
and §2 were accepted (ship screen written, publish named as unbuilt). Only §3 (Settings) is
untouched. Leaving the ADR *Proposed* while shipping two-thirds of it means a future reader
cannot tell which parts were decided and which were drifted into. It should be taken to the
planning chat and marked Accepted or rewritten to match what was built.

**b. What is a directed change worth, and who quotes it?** `CHANGE_CEILING_USD = 2.0` is a
placeholder with a comment saying so, and B063 (customer-facing pricing) is still `todo`. Until
that lands the flagship loop has a made-up ceiling and no price.

**c. Does the toolset in `STRATEGY.md` §D still describe the product?** Four of its seven items
have no code. Either they are the roadmap for gate 2b and belong in `BACKLOG.md` with ids, or
the strategy has moved and §D should be trimmed. Right now it reads as a description of
something that exists.

**d. Should the security confirmation be enforced by the API?** Today it is a browser
convention. Intake's equivalent guarantee is enforced in code. If a second client is ever
written, the two-step disappears.

**e. What owns the workspace lifecycle?** ADR-0017 flagged it (*"the design version and the
build version now point at the same workspace, so the workspace lifecycle belongs to the
project rather than to a single build. Deleting it (B100) has to account for both"*). B100 is
`in progress`. The unresolved half is here.

---

## Documentation drift found

**1. `docs/STRATEGY.md` §A item 9 is stale.**

> 9. **Finish -> full build -> back in the design window.** Designed.

This is built. `stream_promotion` (`pipeline.py:353`) delivers the design workspace, the build
records `designVersionId` (`build.service.ts:655`), and `RevealPage.tsx:203` routes "Open &
refine" back into the design window. Decided in ADR-0017 on 2026-08-22; `STRATEGY.md` was last
committed **2026-08-19** (`fix: B071-B074 — what the first real run surfaced`), three days
earlier. Item 8's *"Toolset to complete"* is still accurate.

**2. `docs/STRATEGY.md` §E contradicts ADR-0018 §3.**

> **Model passes are a Settings control (and a test lever).** Expose the relay's configurable
> pass-count in Settings.

ADR-0018 §3 proposes the opposite — *"the model profile does not go in it yet"*, because
exposing "how hard should Scio work" needs the pricing decision (B063) first. Both documents
are current. One of them is wrong, and which one is a product decision that has not been made.

**3. `docs/STRATEGY.md` §D describes a toolset that is four-sevenths unbuilt.** Listed: mark →
describe, smart property controls, free prompt, global style, reference upload, undo/versions,
test/interact. Present in code: mark → describe, free prompt, undo/versions. No design-token
editing, no property panel and no image upload appear anywhere in `DesignPage.tsx` or the
design modules. §D is written as description, not as plan.

**4. A dead endpoint is documented in Swagger.** `POST /projects/:projectId/design-versions`
carries `@ApiOperation({ summary: "Freeze the approved design as a new version" })` and has no
caller. The generated API docs promise a capability the product does not use.

**5. `docs/BACKLOG.md` B022 and B084 are accurate.** Both read *"in progress"* with the right
detail (*"ship done; live/versions/settings/notifications need ADR-0018"*, *"refine + ship
wired; publish/settings need ADR-0018"*). No drift. `docs/ROADMAP.md:30` correctly names 0018
as one of three Proposed ADRs.

---

## A note on the test scope given

`tests/test_interaction_channel.py` (36 collected; 27 passed, 9 skipped — the live browser and
pglite tests skip when the sandbox lacks them) is **not a Layer F suite.** Its own docstring:
*"The interaction channel (B060b): 'it works' as something a build passes or fails."* It tests
Layer C's script derivation and Layer E's verification loop. One class touches this layer
obliquely — `TestTheVocabulary::test_a_loop_rendered_id_is_still_addressable` guards the
`data-scio-id` vocabulary that marking depends on.

The design window's own suites are `test_design_change.py` (27) and `test_design_restore.py`
(12), which together with the API e2e (23) and frontend (29) tests make 91 tests over 1,614
lines. I ran the 39 engine tests; the 52 TypeScript tests I read but did not execute.

*Verified 2026-08-26 against the code, with all 39 engine design tests passing. Graph figures
recomputed from `graph/graph.json` (5,173 nodes, 12,054 edges) and reproduce the index's 73 and
70 exactly.*
