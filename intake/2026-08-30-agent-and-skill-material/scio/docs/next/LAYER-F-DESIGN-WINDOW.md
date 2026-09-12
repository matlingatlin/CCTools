# Layer F · The design window — what to build next

Forward-looking. `docs/as-built/LAYER-F-DESIGN-WINDOW.md` is the starting point; this is what to
do with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method note.** Every domain this layer touches was scanned on **2026-08-26** before anything
was proposed: how Lovable, v0, Figma Make, Bolt and Replit actually implement element-level
selection and directed change; DOM→source tracing; LLM edit formats and edit-tool harnesses;
visual regression testing and affected-set snapshotting; design-token standards; deterministic
accessibility checking; change impact analysis, program slicing and test-case minimisation;
build-provenance attestation; and what users complain about in refine loops. The rule the family
of documents runs on holds here too: **where a standard, a published algorithm or a shipped
competitor mechanism already covers something, cite it and adopt it.** Six things this layer
would otherwise have invented already exist — a property-edit path that costs no model call
(Lovable, v0, Figma Make), an affected-set snapshot algorithm (Chromatic TurboSnap), a
minimality definition (ddmin), an impact-report shape (Chianti), a token format (DTCG v2025.10),
and an accessibility engine with published coverage numbers (axe-core).

This document **depends on** work proposed in its siblings rather than re-proposing it: Layer B
§3.1 adopts the change-impact-analysis literature, Layer C §3.4 turns an impact set into
packages and prices, and Layer C §2.4 computes the dependency antichain.

Everything measured below was re-run against the working tree at `00408d3` on 2026-08-26 with
`apps/engine/.venv/bin/python` and `npx vitest`. Token figures are characters ÷ 4 and are marked
as such — `messages.count_tokens` is the correct instrument and no API key was available here,
so re-measure before acting on any margin narrower than 20%.

**The frame for the whole document.** The system-wide pattern the layer documents keep hitting is
that Scio *computes an honest signal and drops it before anyone sees it*. Layer F is the only
layer whose job is seeing, and it is where every one of those dropped signals was supposed to
surface. Six are dropped inside this layer alone; they are catalogued in §1.1.

---

## 1 · Where Layer F stands

`Preview → markings → changed preview → promotion → ship`. The engine half is 848 lines across
five files (`design/{change,conflicts,markings,restore,__init__}.py`); the rest is an HTTP skin
and three React pages. Its own docstring is the honest description: *"This layer's job is to take
several markings at once and to refuse the ones it should not act on"* (`design/__init__.py:1-19`).
It owns batching, refusal, conflicts and version bookkeeping; the correctness lives one layer
down in `resolve_marking`, `directed_regenerate`, `verify_instrumentation` and `typecheck`.

**Solid and not to be touched:**

- **Per-marking honesty** (`markings.py:74-117`) — failing the batch teaches people to mark one
  thing at a time; dropping silently applies a change and never mentions the part ignored.
- **Conflicts are asked, never resolved, and cost nothing.** `detect_conflicts` runs at
  `change.py:261` *before* `_edits_for`, and is deliberately model-free (`conflicts.py:16-21`).
  `test_a_conflict_stops_the_change_before_a_token_is_spent` asserts the negative in the only way
  that counts: the registry handed in would raise if called.
- **The strict resolver.** `resolve_marking` raises rather than walking to an ancestor
  (`core/resolver.py:56`), and the error names the ancestor as evidence.
- **The bridge stays dumb.** `describe()` (`bridge.js:94`) reports the element and, separately,
  the nearest instrumented ancestor, and never substitutes one for the other. Origins pinned both
  ways.
- **A restore is a write** — manifest rebuilt, instrumentation re-verified, tree put back if it
  fails, history moved forward rather than rewritten.
- **Promotion (ADR-0017).** `stream_promotion` (`pipeline.py:353`) regenerates nothing and reads
  the plan stored beside the code. The layer's most valuable single decision.

The constraint that governs every proposal below is the same one Layer C has, stated here in
`change.py:3-11`:

> resolve strictly → detect conflicts → ask the model → guardrails.

**Any proposal that lets a model decide whether a marking is addressable, whether something is a
conflict, or whether a change stayed inside its package is out of scope.** Proposals may add
deterministic steps before the model; they may not move a guardrail into a prompt.

### 1.1 Corrections to the as-built record

Nine, and four of them change conclusions.

**(a) Five routes are placeholders, not one.** `App.tsx:16-22` lists `/live` ("Refine"),
`/versions`, `/settings`, `/states` ("Error & empty states") and `/notifications`. The as-built
named only Settings. `/live` is the one that matters — `docs/UX-FLOW.md:21-23` says Level 1
*"moves shaping to AFTER the build (on the running app) instead of BEFORE it (on a preview)"*.
§3.1 shows the situation is stranger than "unbuilt".

**(b) The change path re-runs Layer B — a model call — on every directed change, and throws the
result away.** `main.py:502`:

```python
architecture = (await run_layer_b(req.spec, registry=build_registry())).architecture
```

`run_layer_b` (`layerb/service.py:42-66`) derives the architecture with a pure function and then
calls `generate_whole(spec, registry=registry, passes=2)` — a **two-pass relay on the
`architecture` task, which ranks Opus 5 first** (`matrix.yaml`, verified: `architecture` →
`claude-opus-5` @ $5/$25 per MTok). Only `.architecture` is used. `derive_architecture(spec)` is
deterministic and free. So every marking batch pays for a narrative nobody reads, on the
interactive path, before the change starts.

**(c) The contract never reaches the change, and the system prompt says it does.**
`DesignChangeRequest` (`main.py:462-481`) has no `contracts` field; `apply_change` is called at
`main.py:507` without one; `change.py:279` therefore falls back to:

```python
(contracts or {}).get(package, f"# Package: {package}")
```

A repo-wide grep for `contracts=` finds `orchestrate.py:594`, `pipeline.py:273`,
`plan_store.py:37` and four tests — **never the design path, including its own 39 tests.**
Meanwhile `FIX_SYSTEM` (`codegen.py:118-127`) opens *"You are given the contract, the current
code, and exactly what went wrong."* In production it is given a one-line comment.

What it does not get, rendered from the real code: the canonical vocabulary, the scope guard
(*"Out of scope — do not build: no payments for now"*), the eight acceptance criteria, the import
boundary, and the whole house-rules block — including *"styling: Tailwind CSS, tokens from the
design_tokens node — no ad-hoc hex values"* and a four-line **Accessibility** section. **The one
model call in the product whose entire job is to change how the app looks is the only one told
nothing about how the app is supposed to look.**

**(d) The workspace already holds exactly what the change path is missing, and the module that
holds it says why.** `plan_store.py` writes `{plan, contracts, whole}` into `.scio/plan.json`,
with this docstring:

> *"Re-deriving them would be worse than expensive. Layers B and C are model calls: run again
> they can produce a different plan, and the app on disk would then be measured against criteria
> it was never built to meet."*

`stream_promotion` reads it (`pipeline.py:384`). `/design/change` re-runs Layer B instead. The
engine has already written down why (b) is wrong, one module over.

**(e) The label-collision wrinkle is half-fixed, and the as-built could not tell.**
`bridge.js:77-81` flips the tag below the box when there is no room above:
`tag.style.top = box.top > 22 ? "-20px" : box.height + 2 + "px"`. That handles the viewport top.
It does **not** handle the case the spike actually described — two marked elements close
together, whose labels land on each other at the same y. Half the fix landed.

**(f) `route` is captured, shown, and dropped.** `bridge.js:141` sends `route:
window.location.pathname`; `DesignPage.tsx:297` stores it on `Pending`; `:681` renders it next to
the marking. `DesignMarking` (`packages/shared/src/dtos.ts:111-120`) has no route field, and
`design.service.ts:369-380` does not send one. A feature package owns two page files on the
canonical app; the model is told which file:line, and never which screen the user was looking at.

**(g) A change's cost never reaches the browser.** `PackageChange.cost_usd` exists
(`change.py:57`) and `DesignChangeResult.total_cost_usd` is returned; `ApplyDesignChangeResponse`
(`dtos.ts:168-182`) has no cost field, and `design.service.ts:426-433` drops the per-package
figure. It is written to `usage_event` (`design.service.ts:141-157`) and shown to nobody.

**(h) Eight throwing 501 endpoints across six modules, not fourteen.** Fourteen is the count of
`NotImplementedException` *mentions*; six of those are imports and one
(`usage/usage.service.ts:8`) is a comment saying the method *used to* throw. The eight are
`user.me`, `workspace.current`, `notification.list`, `notification.markRead`, `reference.list`,
`reference.create`, `deployment.list`, `deployment.create`. **Four of the eight are Layer F's own
promises**: the two deployment methods are Publish, and the two reference methods are
`STRATEGY.md` §D's "reference upload" tool, scoped in its own docstring as *"Tagged RAG uploads
(4.6)"*.

**(i) There is no gate 2.** `UX-FLOW.md:93` says the design gate *"freezes 'approved design v1'
— the second contract"*, and `:135` says later changes *"are measured against the two
contracts"*. `DesignPage.tsx:556` is a plain `Build it →` navigation. The endpoint for the
missing gate exists and has no caller: `design.controller.ts:96` → `design.service.freeze:579`,
documented in Swagger as *"Freeze the approved design as a new version"*. The as-built called it
obsolete. It is not obsolete; **it is the unbuilt half of the layer's own name.** Only one of the
two contracts the product is built on exists, which is why nothing anywhere checks that the
delivered app looks like the one that was approved.

### 1.2 The baseline, honestly

`test_design_change.py` (27) and `test_design_restore.py` (12) — **39 passed in 2.72s**, re-run
2026-08-26.

**B105 records `design.test.tsx` as flaky** — two different tests failed on two consecutive runs,
cause never found. It was re-run here: `design.test.tsx` alone **5 times (29 passed each)** and
the full `apps/app` suite **3 times (8 files, 109 passed each)**. Eight green observations, no
failure.

That is much weaker evidence than it looks. With zero failures in n=8, the rule of three puts the
95% upper bound on the per-run failure rate at **3/8 = 37.5%**. Eight clean runs is consistent
with a test that fails one time in three. The correct instruments are `vitest --repeat` with a
fixed seed and recorded per-test durations, run under the concurrency CI actually uses — not more
of the same. **Do not treat the baseline as proof of stability, and do not treat this pass as
having cleared B105.**

---

## 2 · Refining what exists

### 2.1 Delete the Layer B call — one line, and it is the largest single waste in the layer

`main.py:502` needs `arch` for `detect_conflicts`. `derive_architecture(spec)` returns it, free
and deterministically. Two things `run_layer_b` also does are worth keeping, and both are free:
`is_buildable(spec)` (the gate) and `validate_architecture(architecture)`.

The cost of being wrong is nil — the whole is discarded on the next line. The gain is
$0.020 per change, two sequential Opus round trips off the interactive path, and one fewer
place where a model runs unmetered and uncapped (§7.2).

There is a second-order argument that matters more than the money. `run_layer_b` is
non-deterministic; `derive_architecture` is not. Today the conflict rules are evaluated against
an architecture re-derived on every request — which happens to be stable because the derivation
is pure, but the call site does not say so. Calling the pure function says so.

### 2.2 Give the change its contract, and read it from the workspace

`load_plan(app_dir)` returns `StoredPlan{plan, contracts, whole}`. `contracts[package]` is the
exact prompt this package's code was generated from. Two honest options:

| Option | Change | Cost of being wrong |
|---|---|---|
| **A. Read the stored contract** | `apply_change` loads `.scio/plan.json` and passes `contracts[package]` | a workspace built before plans were stored has none — `load_plan` already returns `None` for that, and the fallback is today's behaviour |
| **B. Add `contracts` to the request** | the API sends what it has | the API does not have it; it would have to re-run Layer C, which is the mistake in §2.1 wearing a different hat |

**A, and it is not close.** It is what `stream_promotion` already does, for the reason
`plan_store.py`'s docstring gives.

Two consequences to argue in the ADR rather than wave past. **Order:** put the contract first,
then the code, then the instruction — the contract is byte-identical across every round of a
refine session on that package and the code is not, so contract-first is the only order in which
anything caches at all (§7.3), and it is where attention is strongest besides. **Criteria:** a
change prompt carrying acceptance criteria is one the model can visibly violate, which is the
point, and it is the join key for the change report in §3.4.

### 2.3 Send the smallest dependency-complete file set, not the whole package

Measured on the real catalogue feature package (8 files, 11,089 chars): the file a single
marking resolves to is **22.6%** of the code listing. The other 77.4% is sent, read, priced, and
not touched.

| Option | What is sent | Failure mode |
|---|---|---|
| **A. Marked files only** | the files the resolved markings land in | the model needs a sibling it cannot see — e.g. adding a required field needs `lib/validation/booking.ts` — and either invents it or half-does the change |
| **B. Marked files + their intra-package imports** | A, plus every file inside the package that a marked file imports, transitively | over-approximates on a tightly-coupled package; on the canonical feature that is 3–4 files instead of 8 |
| **C. The whole package** | today | 77% waste, every round |

**B is the promise, made concrete.** It is a static import walk over files already on disk,
bounded by `manifest.files_for(package)` — free, deterministic, and it terminates because the
package's file list is finite and small.

The crucial property: **narrowing the prompt does not narrow the guarantee.** `verify_isolation`
(`core/regenerate.py:71`) hashes every tracked file in the app and compares; `PreparedRegenerator`
(`change.py:129-142`) already refuses files the package does not own. A model that needed a file
it was not given fails on `typecheck` or on an assertion, loudly. A model that is *given* seven
files it did not need may quietly rewrite one of them, and today the isolation proof would
accept that as "inside the package".

Honest limit: this changes the shape of failures, from "silent collateral edit inside the
package" to "incomplete edit caught by the compiler". That is the better failure, but it is a
change, and it needs measuring against §8's before/after corpus rather than asserting.

### 2.4 `/spec/amend` is protected only by the browser, and the sentences are guessable

`AmendSpecDto` (`spec.controller.ts:27-38`) has exactly three fields:

```ts
kind!: "non_goal" | "auth" | "access";   // @IsIn
specSays!: string;                        // @MaxLength(2000)
note?: string;
```

No confirmation field, no nonce, no reference to the conflict that raised the question, no
reference to the spec version it answers. `spec.service.amend` (`:181-260`) performs the whole
act on a single POST. The browser's two-step (`DesignPage.tsx:90-92`, `:744-760`) is a UI
convention.

What makes this worse than "unenforced" is that **the string an attacker needs is generated by a
template**. `detect_conflicts` filters on the exact case-folded `spec_says`
(`conflicts.py:203-206`), and `spec_says` is composed at:

- `conflicts.py:129-133` — `"sign-in via " + (arch.auth_access.provider or mode.value)`
- `conflicts.py:154` — `f"{kinds} data, with row-level security on"`

Both are derivable from the project's own visible behaviour. So one POST with
`{kind:"auth", specSays:"sign-in via supabase"}` **permanently silences every auth conflict for
that project**, never shows a second screen, and writes an `amendments[]` audit row
indistinguishable from one a human answered. `kind:"non_goal"` is worse in a different way: it
does not merely silence, it **edits the approved spec**, filtering the item out of
`spec.non_goals` and stamping provenance `"dropped in the design window: …"` (`:212-225`). The
workspace throttler (120 req/60s) does not distinguish an amendment from a page load.

Three options, and the middle one is right. **A `confirmed: true` field** is the weakest possible
fix — a second client sets it; it documents intent and enforces nothing. **A server-issued
conflict token** — opaque, short-lived, single-use, bound to `(project, spec_version, kind,
spec_says)` and required on the amendment — means the server knows the user was shown the question
it is being asked to answer. That is an ordinary intent/confirmation token, the same shape as a
CSRF intent token or a payment nonce; **do not invent a scheme.** **A pending-amendment record**
gives the same guarantee with more moving parts.

Intake's `corrected-on-review` mark is enforced in code; this is the equivalent guarantee at the
second gate and it is not. That asymmetry is the argument.

### 2.5 The ceiling is untested and does not cover the layer's largest call

`design.service.ts:139` — `CHANGE_CEILING_USD = 2.0`, with a comment admitting it is a
placeholder. Verified: **no `budget_usd`, `ceiling` or `CHANGE_CEILING` reference exists in
`test_design_change.py`, `test_design_restore.py` or `design.e2e.spec.ts`.** Nothing asserts it
stops anything.

Worse than untested: `Spend(ceiling_usd=budget_usd)` (`change.py:250`) is threaded into
`_edits_for` and nowhere else. The Layer B call at `main.py:502` runs **outside** the ceiling and
outside `meter()`. The one model call in the change path that nobody chose to make is also the
one nobody is charged for and nobody can cap.

### 2.6 `compiles` has two owners, no test, and an unclear contract with promotion

`typecheck` is called at `change.py:330` and again at `restore.py:104`. Nothing asserts either.
The tri-state is then carried by hand through four hops with `?? null` at each.

The deliberate part is right and should stay: a change that broke the build is still committed,
because that is what makes it returnable (B048), and the window says so
(`DesignPage.tsx:821-833`). The unclear part is what happens next: `stream_promotion` delivers
the workspace as it stands. Whether a design version that does not compile can be promoted, and
what the user is told if so, is not settled anywhere. It is one line of policy and it belongs in
ADR-0017's consequences.

### 2.7 The design version `ref` is a JSON blob, and the failure mode is the expensive one

`record()` writes `JSON.stringify(ref)` (`design.service.ts:169-183`); every reader does
`JSON.parse` inside a try/catch returning `{}` (`refOf`, `:198-205`). A ref that fails to parse
degrades to "no workspace", which `build.service.designToPromote` reads as *nothing to promote*
and falls through to a full rebuild — **the exact data loss ADR-0017 exists to prevent, reached
by a different door.** The comment there is honest about preferring a rebuild to guessing at a
path; the honest options are a typed column, or `designToPromote` refusing rather than falling
through. Refusing is cheap and it is the same discipline `stream_promotion` already applies to a
workspace with no stored plan (`pipeline.py:386-392`).

---

## 3 · What is missing

### 3.0 The preview iframes have no `sandbox` attribute

*Added 2026-08-26 by the repo-wide review, and verified at source. The word `sandbox` does not
appear once in any of the seven forward documents — including this one, which owns the preview.*

Two iframes render model-generated code straight into the user's authenticated origin:

- `RevealPage.tsx:154` — `<iframe title="Your app" src={build.previewUrl} …>`
- `DesignPage.tsx:635` — `<iframe ref={frameRef} key={frameSrc} src={frameSrc} …>`

Neither carries `sandbox`. Neither carries `allow` or a referrer policy.

**Why this is Layer F's and not Layer E's.** Layer E's whole sandboxing effort — the Docker
provider, the conformance suite, the test asserting the *absence* of `ANTHROPIC_API_KEY` from the
child environment — protects the machine that *builds* the app. This is the machine that *views*
it. Generated code that is contained perfectly during the build is then rendered without
containment in the browser of the person who paid for it, and `DesignPage` additionally listens for
`postMessage` from that frame through the marking bridge.

The fix is one attribute and an origin check, and it is cheap enough that the only reason it is
absent is that nobody looked. What it is *not* is obvious: `sandbox` without `allow-scripts` breaks
every generated app, and `allow-scripts allow-same-origin` together re-grant everything the
attribute was meant to withhold. The right answer is to serve previews from a **separate origin**
and sandbox with `allow-scripts` only — which is a Layer G decision about how `previewUrl` is
issued, not a Layer F patch.

That this survived two independent reviews, seven as-built documents and seven forward documents is
the strongest argument in the repo for the cross-document pass that found it.

### 3.1 `/live` — and the real finding is not that it is missing

`UX-FLOW.md:130` is explicit: *"ONE editing model everywhere (intake gate → design markings →
live markings): mark, describe, update in a directed way, preserve the rest, verify."* So Level 1
does not need a second surface. It needs the design window pointed at the delivered app.

And that already works — by accident of ADR-0017. `RevealPage.tsx:198-205` routes "Open & refine"
to `/design`, and because promotion delivers the *same workspace*, the preview URL, manifest and
package file map on the current design version are still valid. The refine loop after a build is
live today.

**What actually blocks Level 1 is a deliberate invariant, and it is the right one.**
`pipeline.py:465` serves the promotion with `preview=False`, so the delivered app carries no
bridge — guarded by `test_a_delivery_build_never_registers_it`. Marking works after a build only
because the *preview* is still running beside the delivery, not because the delivered app is
markable. Nobody has decided which of those the user is looking at.

So the decision is not "build `/live`". It is:

| Option | What the user marks | Cost |
|---|---|---|
| **A. Re-serve the same commit in preview mode** | a preview twin of exactly the delivered code | one sandbox, no regeneration — promotion already proved a workspace can be served without rebuilding |
| **B. Ship the bridge in delivered builds, disabled** | the delivered app | breaks the spike's finding 1 (*"it never ships"* — not disabled, **absent**) and puts marking code in the user's repo |
| **C. Leave it: refine happens on the preview** | today's behaviour, undocumented | `/live` keeps claiming otherwise |

A is almost certainly right and B should be refused outright. Meanwhile `/live` should be a
redirect to `/design`, `/versions` should be the timeline `UX-FLOW.md:139-145` describes (which
`DesignPage.tsx:836-870` already renders in a side panel), and `/notifications` is step 5's
background-build notification — the one thing that makes *"you can leave"* true.

### 3.2 The nine-item reveal — and the design window already shows two of them

`PRODUCTION_READINESS_DIFF.md` §7 "Leveransbevis" lists nine things the reveal should show.
Checked against the code:

| §7 item | Computed | Reaches the user |
|---|---|---|
| requirements met / unmet | criteria in the plan; `cover()`, `scoped_out()` (Layer C) | as free-text lists in `honest_status`, not as requirements |
| tests and browser flows | `GATES` includes `interaction`; **nothing runs the generated app's own tests**; the two data gates are behind `SCIO_VERIFY_DATA=1` | no |
| security checks | RLS / auth criteria; `validate_package` | no |
| changed packages and files | `edited_files` | **design window only** (`DesignPage.tsx:800`) |
| verified-unchanged surface | `IsolationProof.unchanged_files` | **design window only** (`DesignPage.tsx:800-803`) |
| model and build cost | `build.spend`, `build.estimate` | **yes**, and well — estimate *and* actual, side by side (`RevealPage.tsx:180-193`) |
| build time | on `build_version` | ShipPage, not reveal |
| remaining risks | `honest_status.remainders` | **yes** (`RevealPage.tsx:59-67`) |
| version id and export | version + sha shown; export does not exist | half |

Three of nine. And `checks_passed` — `GATES = ("instrumentation", "validation", "console",
"interaction", "critique")`, five of them, with `loop.py:62` stating *"`checks_passed/len(GATES)`
is what the reveal shows, so the count is a real count and not a number chosen to look
reassuring"* — is computed at `loop.py:922`, typed at `packages/shared/src/intake.ts:287`,
transmitted, and appears in **no `.tsx` file anywhere**.

**The design window renders the two items the reveal does not.** That is the shape of the
problem: this layer is not short of honest data, it is short of one screen that says it.

### 3.3 There is no design gate, and therefore no second contract

Detailed in §1.1(i). What "approved design v1" would have to contain is the interesting part,
because it decides what a later change can be checked against:

- the git sha (exists — `commit_change` returns one per batch)
- the manifest at that sha (exists — stored on the ref)
- the **token set** at that sha (does not exist as an artifact; `pkg_design_tokens` owns
  `app/globals.css` and `tailwind.config.ts` and nothing extracts a token file from them)
- a **per-route render** at that sha (does not exist — §3.7)
- the spec version it was approved against (exists)

Three of five are already produced. The gate is mostly bookkeeping over things the layer already
has, and without it the sentence *"it looks like what you approved"* (`UX-FLOW.md:110`) has no
referent.

### 3.4 No impact analysis before code is written — product invariant #2

`PRODUCTION_READINESS_DIFF.md` §2 states five product invariants. The second is *"No change
without impact analysis"* — affected requirements, architecture nodes, packages, files and tests
identified **before code is written**. §6 writes out the pipeline:

```
User intent → selected element ids / semantic prompt → owning packages → affected contracts
→ transitive dependency closure → allowed files and operations → required tests
→ expected invariants → explicit approval if scope expands
```

Scio does steps 1–3, and step 6 only in the weak sense that the package's file list is the
allow-list. It never computes affected contracts, never a closure, never required tests, never
expected invariants, and has **no moment at which an expanded scope is put back to the user**.
Today's order is resolve → conflicts → *generate* → prove isolation: the proof arrives after the
money.

**The better promise deserves a precise definition rather than a slogan.** Not "only the marked
component changes", but *"only the smallest dependency-complete and explained area changes"* —
and each word can be made to mean something. **dependency-complete**: closed under the "this
cannot change alone" relation, which is forward slicing (Weiser, 1981), with the field's own
warning that a naive closure is useless because static slices average ~30% of program size.
**smallest**: 1-minimal in ddmin's sense (Zeller & Hildebrandt) — no element removable while the
property holds. **explained**: every file in the set names the reason it is there, a marking or
the named edge that dragged it in.

The honest limit on ddmin: it needs an oracle you can run many times, and *"does this still do
what the user asked"* is a model call. Its *minimality definition* transfers; its *search* does
not — unless the oracle is one of the deterministic gates (typecheck, instrumentation, the design
checks, the isolation proof), in which case it does.

**Chianti is the prior art Layer C did not need and Layer F does.** Ren, Shah, Tip, Ryder &
Chesley (OOPSLA 2004) decompose a version difference into *atomic changes* and report impact as
**affected tests, and for each affected test the affecting changes**. That is exactly the change
report `PRODUCTION_READINESS_DIFF.md` §6 draws by hand:

```
Ändrade filer: 5 · Verifierat oförändrade filer: 61
Kontrakt: 7/7 · Tester: 18/18 · Browserflöden: 3/3 · Säkerhetskontroller: 4/4
```

Two of those six lines already exist in `DesignChangeResult`. The rest need the impact set.

This is **the second half of Layer B's B-1 and Layer C's C-6**, and it should not be argued a
third time. The division of labour:

| Layer | Answers |
|---|---|
| **B** | which requirements and architecture nodes an edit touches, tiered |
| **C** | which packages own them, what they cost, what order to rebuild in |
| **F** | which **files**, whether the actual diff stayed inside the set, and **what the user is shown before spending** |

### 3.5 Four of the seven design-window tools

`STRATEGY.md` §D names seven: mark → describe · smart property controls · free prompt · global
style · reference upload · undo/versions · test/interact. Three exist. The four that do not are
not equally hard, and three of them are the same feature:

- **Smart property controls** — this is the deterministic edit path, and it is what every
  competitor has (§4.1). No model call, no tokens, no rollback risk.
- **Global style (edit a token for the whole project)** — the token set is the value space the
  property controls edit *within*. Same feature, one level up.
- **Test / interact** — `core/interaction` is a working browser driver used by Layer C's
  scripts and Layer E's gates. The design window does not use it, so the user cannot ask *"does
  the booking actually work"* from the place they are looking at the booking.
- **Reference upload ("like this" with an image)** — the only one with genuinely new machinery
  behind it, and it has a module: `reference.service.ts`, both methods throwing 501, scoped as
  tagged RAG (phase 4.6).

### 3.6 Nothing measures the flagship loop

No metric exists for: how often a directed change is accepted first time, how often a package is
rolled back, how often a marking is unaddressable, how many rounds a session takes, what a change
costs, or whether the conflict rules fire correctly. This is the interaction the product is
differentiated by, and **no change to it can currently be shown to be an improvement.**

Everything needed already passes through (§8). The same argument as Layer A §3.5 and Layer C
§3.6, one layer over: measure before changing, or the change is an expense.

### 3.7 Nothing verifies the isolation claim in the medium the claim is about

`verify_isolation` hashes files. The promise is about what the user *sees*. A route rendered
entirely by packages that were not touched must look identical, and nothing checks it.

The tooling exists and is unusually well-matched. **Playwright `toHaveScreenshot()`** is built in,
free, already a dependency (`apps/engine/.venv` carries the driver), and ships pinned Chromium /
Firefox / WebKit builds — which practitioners in 2026 name as the single biggest factor in
reducing visual-test flakiness. **Chromatic TurboSnap** is the affected-set idea applied to
snapshots — snapshot only the stories a change can reach, reported at **60–90% fewer snapshots**
and 50–80% less CI time. **Percy and Applitools** are the wrong shape: they keep baselines on
their servers, and Scio's baseline is a git commit it already owns.

**The fit is better than for a normal app**, because the two things VRT usually lacks are already
present: `commit_change` produces a sha for every batch, so every change has a before and an
after; and the affected-package set says which routes may legitimately differ. The snapshot set is
derivable rather than configured.

Limits, stated plainly: anti-aliasing differences register the same as a 20px shift, and
`maxDiffPixelRatio` is a blunt instrument; fonts, dates, and non-seeded data produce false
positives; and this only works if the preview renders deterministically, which needs the
verification database (`SCIO_VERIFY_DATA`) that is currently off by default.

### 3.8 The deterministic design gate does not run where the user sees the result

`.claude/skills/app-design` §5 proposes six checks — token adherence, contrast, scale adherence,
state coverage, theme completeness, focus visibility — for Layer E. Layer F is where the user
sees the result, and that has three consequences the skill does not draw:

**(a) The checks must run per *change*, not per build.** They are free. A directed change that
introduces a hex literal is the single most likely way an app drifts off its own token set,
because — per §1.1(c) — the model making that change is the only one never shown the rule
forbidding it.

**(b) Contrast is the one to build first, and it has numbers.** Deque's coverage study (2,000+
audits, 13,000+ pages, ~300,000 issues) reports axe-core catching **~57% of accessibility issues
by volume**, while only **29.5% of WCAG 2.2 success criteria are fully automatable** (10.3%
partly, 60.2% manual) — the gap explained by contrast, language-of-page and name/role/value
together being ~58.8% of real defects. Contrast is computable from the token set alone, in both
themes, before anything renders.

**(c) axe-core can run in the preview, because the preview already has an injection point.**
`bridge.js` is injected into the running app in preview mode only. Running axe there is an
existing mechanism plus a script, and the result is per-route and per-element — which the
manifest can map straight back to a package.

Two limits that must be carried into any claim: axe reports elements as **incomplete** where it
cannot be certain, and those are not passes; and the honest sentence is *"the automatable share
passed"*, never *"accessible"*. On the standard itself: **WCAG 3.0 is a Working Draft and its
contrast algorithm is explicitly undecided as of April 2026** — APCA was moved out of the draft
in July 2023 and remains exploratory. Target WCAG 2.2 AA; treat APCA as advisory.

---

## 4 · Out of the box

### 4.1 The deterministic edit path — the layer's largest missing idea, and everyone else has it

Three of the four notes the impatient user writes in `JOURNEY-INVOLVED-PATH.md` step 6 — *"too
big"*, *"move this up"*, *"this should be blue"* — are property or token changes. All three
currently cost a model rewrite of an eight-file package, and the model doing it has never been
told the token set exists.

What the field actually does, scanned 2026-08-26:

| Product | Mechanism | Model call for a style change? |
|---|---|---|
| **Lovable** *Visual Edits* | a custom **Vite plugin** gives every AI-generated JSX element a stable compile-time id; the project's code is synced into the browser as an AST (Babel/SWC); edits are applied optimistically client-side and synced by HMR | **No** — styling, Tailwind class and colour changes are handled without the LLM |
| **v0** *Design Mode* | a typed properties panel (typography, colour, margin/padding, border, opacity, radius, shadow, text) applied live in the preview; on **Apply** the edits are serialised and sent to the chat | Live: no. Commit: yes |
| **Figma Make** (properties panel + annotations, 30 Jul 2026) | Figma Design's own controls over the code, a **full DOM tree** as a layers panel, **select every instance of an element at once**, and numbered annotations applied across all selected elements | Panel: no. Annotations: yes |
| **Scio today** | mark → note → whole-package model rewrite | **Always** |

Two things follow, and the second is the interesting one.

**Scio already has the hard part.** Lovable's Vite plugin exists to produce exactly what
`data-scio-id` + `Manifest` already produce — and Scio's version is *derived from source*
(`manifest_builder`), verified (`verify_instrumentation`), and resolves to `file:line`
(`SourceLocation`). The generic prior art is `@babel/plugin-transform-react-jsx-source`, which
every React dev build already runs; it gives file and line but not a stable identity across
regeneration, which is the property Scio's ids have and Babel's `__source` does not.

**So the missing piece is not instrumentation, it is a classifier and a codemod.** The proposal:

1. Classify each marking's note. A note that resolves to *(property, value-from-the-token-set)*
   is a **deterministic edit**; everything else falls through to the model.
2. Apply it as an AST codemod (ts-morph / jscodeshift / Babel) at the exact `file:line` the
   resolver returned, with the token set as the only legal value space.
3. The result costs zero model tokens, cannot lose a `data-scio-id`, and satisfies the isolation
   proof by construction.

**The classifier is the risk, and the discipline is already written down elsewhere in this
codebase.** `scripts.py` refuses to derive a script when it lacks what it needs, and
`resolve_marking` raises rather than guessing. The classifier must do the same: recognise a small,
closed set of property intents and **refuse everything else into the model path**. A classifier
that is merely usually right would silently apply the wrong edit — the exact failure
`conflicts.py:16-21` argues against for conflicts.

Speculative extension, flagged as such: once the classifier exists, a **property panel** is the
same feature with a UI, and *"select every instance"* (Figma Make's move) is a manifest query —
`bridge.js:167-178` already sends every id on the route.

### 4.2 The visual isolation proof

Today the layer proves *"61 other files are byte-identical"*. What the user cares about is
*"every other screen looks the same"*. Render the affected and unaffected routes at the previous
commit and at the new one; routes whose owning packages were untouched must match. That converts
the layer's central claim from an assertion about bytes into evidence about pixels, in the medium
the promise is made in — and TurboSnap's 60–90% reduction is the argument that scoping it to the
affected set makes it affordable.

Flag as **conditional**: it depends on deterministic rendering, which depends on the
verification database currently behind `SCIO_VERIFY_DATA=1`.

### 4.3 Make the missing states markable

`app-design` §4: empty, loading, error, **partial** — the four states generators skip. The design
window can only mark what is on screen, so the states nobody builds are also the states nobody
can complain about. `core/interaction` can already drive the app; the routes list already exists.
A control that puts a screen into its empty / loading / failing state turns a documented quality
gap into a thing the user can point at.

Partial state is the one worth being ambitious about: `unjudged` and `needs_look` are already
this system's house vocabulary, and nothing in the generated UI speaks it.

### 4.4 The change report as an artifact, not a paragraph

`PRODUCTION_READINESS_DIFF.md` §6 already drew it. Make it the thing the design gate approves and
the thing that travels in the repo — the *"living spec/architecture doc that travels with the
code"* `UX-FLOW.md:154-156` asks for.

Prior art worth naming and worth **not** overclaiming: build provenance has a standard shape —
an **in-toto attestation** carrying a **SLSA provenance v1.1** predicate, DSSE-signed, with
GitHub's `actions/attest-build-provenance` as a working reference implementation, and
CycloneDX/SPDX for the dependency half. The *shape* transfers: a signed, machine-readable
statement about how an artifact came to be, attached to its digest. The *predicate* does not —
SLSA answers "who built this from what source", not "what was this change allowed to touch".
**Do not claim SLSA conformance for a change report.**

### 4.5 Explain the change that nobody asked for

`ref.change` is `batch.described()` — the raw note list. `UX-FLOW.md:138` asks for *"you asked for
X → I changed Y"*. The half genuinely missing is the reverse: **why a file changed that nobody
marked.** That sentence is exactly what an impact set with named edges produces, and it is the
difference between a diff and an explanation. The same applies to refusals: `unaddressable`
markings carry a reason written for a human (`resolver.py:63-77`), while a rejected *package*
gets `f"{type(exc).__name__}: {exc}"`.

### 4.6 The allowance ledger should read like the security artifact it is

An allowance is a permanent, exact-string silencer carried forward through every subsequent spec
version by `allowancesOf(spec.assumptions)`. Speculative but worth an argument: one granted
against spec v3 should not silently survive into v9, and the set should be re-shown at the design
gate rather than living only in `assumptions`. The mechanism is right — the *lifetime* is what
nobody has decided.

### 4.7 Quote the change before it is made

The loudest complaint in the 2026 practitioner writing about these tools is not quality, it is
**not knowing what an edit will cost before submitting it** — debugging loops that consume credits,
sessions that end with more broken than they started with. Scio can quote a directed change
*deterministically*: the input files are on disk and countable, the output is bounded by their
size, and `estimate.py` already does exactly this trick for a build. No competitor can, because
none of them has a file plan.

That also replaces the flat `$2.00` with a number derived from the work, which is what
`design.service.ts:139`'s own comment asks for.

### 4.8 Run independent packages concurrently — speculative, and blocked

`apply_change` loops `for package in resolved.packages` and awaits each. Packages with no
dependency edge between them could run together, halving wall-clock on the one interaction the
user is actually watching. **Blocked on Layer C's C-7**: `parallelizable` is currently
`len(group) > 1`, not a graph property, and batching wrongly-flagged packages produces a feature
generated against an interface its dependency had not yet declared.

---

## 5 · The means — skills, MCP, repos, research

One distinction first, per `docs/next/SKILLS.md`: a **Claude Skill** helps *us* build Scio; the
product's runtime uses relays, prompts and code. Nothing in this table becomes product machinery
for free.

| Means | What it gives Layer F | Verdict |
|---|---|---|
| **Lovable Visual Edits** — [how we built it](https://lovable.dev/blog/visual-edits), [docs](https://docs.lovable.dev/features/preview-toolbar) | proof that stable compile-time element ids + a client-side AST make style edits cost **no model call**; and that a Vite plugin is how a competitor gets what `data-scio-id` already gives us | **adopt the pattern** (§4.1). Not the implementation — theirs is a browser-side AST of the whole project; ours can be a server-side codemod at a known `file:line` |
| **v0 Design Mode** — [docs](https://v0.app/docs/design-mode), [design systems](https://v0.app/docs/design-systems-2) | the exact property set a panel needs to expose, from someone who shipped it; and the live-preview / apply-to-code split | **adopt the property list** (§4.1). Note the limit v0 states: panel for styles, natural language for structural change |
| **Figma Make properties panel + annotations** — [blog, 30 Jul 2026](https://www.figma.com/blog/properties-panel-and-annotations-now-in-figma-make/) | numbered annotations applied across selected elements (Scio's model, arrived at independently), plus two things Scio lacks: a DOM-tree layers panel and *select every instance* | **adopt the two** (§4.1). The inventory the bridge already sends is the index for both |
| **`@babel/plugin-transform-react-jsx-source`** — [babel](https://babeljs.io/docs/babel-plugin-transform-react-jsx-source) | the standard DOM→source mechanism every React dev build already runs | **already superseded by ours** — `__source` gives file:line but no identity stable across regeneration. Worth citing so nobody re-invents `data-scio-id` as a novelty |
| **Playwright visual comparisons** — `toHaveScreenshot()` | per-route before/after rendering with pinned browser builds; already a dependency | **adopt** (§3.7, §4.2) |
| **Chromatic TurboSnap** — [docs](https://www.chromatic.com/docs/turbosnap/setup/) | the affected-set snapshot algorithm; 60–90% fewer snapshots, 50–80% less CI time | **adopt the algorithm** (§3.7). Not the service — the baseline is our git commit |
| **axe-core** — [dequelabs/axe-core](https://github.com/dequelabs/axe-core), [coverage report](https://www.deque.com/automated-accessibility-coverage-report/) | ~57% of real issues by volume, with a documented false-positive discipline and an explicit *incomplete* verdict; runs in-page, where the bridge already is | **adopt** (§3.8) → skill worth writing, carrying the 57% / 29.5% distinction as its Limits section |
| **W3C DTCG Format Module v2025.10** — [spec](https://www.designtokens.org/tr/drafts/format/), [announcement, 28 Oct 2025](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) | the token interchange format the "global style" tool edits. Re-verified 2026-08-26: **still the current stable version**; the CG's most recent post (17 Jun 2026) celebrates adoption, announces no successor | **adopt** — already the `app-design` skill's position. **Not a W3C Standard and not on the Standards Track** — say so |
| **Style Dictionary** — [DTCG support](https://styledictionary.com/info/dtcg/) | DTCG → CSS variables / Tailwind config, which is precisely `pkg_design_tokens`' two files | **adopt, and pin.** v4 has first-class DTCG; **full v2025.10 support is still landing in v5** (dimension objects and 14 colour spaces done, rest in progress). Verify rather than assume |
| **Figma MCP** · **Playwright MCP** · **Chrome DevTools MCP** | reading an existing design system; accessibility snapshots, console, network and Core Web Vitals traces for an agent | **build process, not product.** Figma MCP earns its place only when a user brings a Figma system; the product's runtime already drives a browser through `core/interaction` |
| **Chianti** — Ren, Shah, Tip, Ryder & Chesley, OOPSLA 2004 — [PDF](https://prolangs.cs.vt.edu/refs/docs/oopsla04.pdf) | impact reported as *affected tests, and for each test the affecting changes* — the change report's published shape | **adopt the shape** (§3.4). Already carried by the `change-impact-analysis` skill; **do not write a second one** |
| **ddmin** — Zeller & Hildebrandt, [*Simplifying and Isolating Failure-Inducing Input*](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf) — and **program slicing**, Weiser 1981 | the definition of *smallest* (1-minimal, no element removable) and of *dependency-complete* (closed under the forward-slice relation), plus the warning that static slices average ~30% of the program | **adopt the definitions** (§3.4) → append to `change-impact-analysis`, don't fork it. ddmin's search needs a cheap oracle; ours are the deterministic gates |
| **Edit formats: aider's benchmarks** — [unified diffs](https://aider.chat/docs/unified-diffs.html), [edit formats](https://aider.chat/docs/more/edit-formats.html) | whole-file vs search/replace vs udiff, measured. GPT-4 Turbo: 20% → 61% on a refactor suite when the format changed | **evidence, not adoption** — the numbers are model-specific and from 2024. What transfers is that **the edit format is a variable worth measuring**, not a given |
| **"The Harness Problem"** — Can Bölük, Feb 2026 — [post](https://x.com/_can1357/status/2021828033640911196) | 180 tasks × 16 models × 3 edit formats: changing only the edit tool moved 15 models by **5–14 points** and cut output tokens ~20% | **the argument for §7.4.** A blog benchmark, not peer-reviewed — cite it as motivation to run our own, never as our number |
| **Anthropic text editor tool** (`text_editor_20250728` / `str_replace_based_edit_tool`) — [docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) | a first-party `view` / `str_replace` / `insert` / `create` contract, so we do not design an edit format | **candidate** (§7.4). Limit: str_replace requires the model to reproduce whitespace exactly, and a failed match is a wasted round trip |
| **in-toto / SLSA v1.1 provenance** — [slsa.dev](https://slsa.dev/spec/v1.1/faq) | the shape of a signed machine-readable statement about how an artifact came to be | **adopt the shape only** (§4.4). The predicate answers a different question |
| **`change-impact-analysis`** (ours) | Arnold & Bohner, Lehnert's 150-approach survey, Chianti, CodePlan, ProReFiCIA, the ~30% over-approximation result | **already written — use it.** F-6 rests on it |
| **`app-design`** (ours) | the token contract, the six-check gate, the "AI design slop" cluster | **already written.** §5 of it is what F-8 proposes to run *per change*, not only per build |

**Skills specific to Layer F**, for the build process:

- **`design-window-metrics`** — runs §3.6's numbers against a fixture workspace with a stand-in
  registry and prints the table. Blocked on nothing; it is a script around functions that exist.
- **`accessibility-gate`** — new, and it earns its place: axe-core's coverage numbers, the
  automatable-vs-detected distinction, the *incomplete* verdict, WCAG 2.2 AA as the target and
  WCAG 3.0/APCA's actual status, plus contrast-from-tokens as a runnable eval. Nothing we have
  carries this and §3.8 rests on it.

**Two skills deliberately *not* written**, and the reasons are the point:

- **No `visual-regression`.** It would be one paragraph of method and a tool list. The decision it
  supports (§4.2) is an ADR, and a skill that encodes a decision is an architecture decision
  hiding in markdown — `SKILLS.md`'s own warning.
- **No `slicing-minimality`.** `change-impact-analysis` already carries the literature; ddmin's
  minimality definition is three sentences and belongs *inside* it. Two skills with overlapping
  descriptions degrade the trigger accuracy of both.

**Two applications of the honesty rule worth restating:**

- **axe-core's 57% is issues by volume across a real audit corpus, not per-page confidence.** It
  says nothing about whether *this* app is accessible, and it may not generalise to
  machine-generated UI, which is not the population Deque sampled.
- **TurboSnap's 60–90% is measured on Storybook component graphs**, where the affected set is
  computed from a build-time dependency graph of stories. Scio's graph is six packages and a
  route list. The direction is the signal; the number is not ours.

---

## 6 · Retrieval versus packing

**Where does this layer send context it could have queried instead?**

This is the layer with the worst ratio in the system, and the reason is unusual: it is not that
retrieval is hard here. It is that the answers are already sitting in the workspace, on disk,
next to the code.

### 6.1 The change packs a whole package and retrieves nothing

`change_prompt` (`change.py:145-176`) inlines every file the package owns, verbatim:

```python
listing = "\n\n".join(f"FILE: {path}\n```\n{content}```" for path, content in sorted(current.items()))
```

Measured: **77.4%** of that listing is files no marking pointed at. The manifest resolved the
marking to `file:line`; `instruction_for` (`markings.py:118-127`) renders that line into the
instruction — and then the prompt ignores it and sends everything. §2.3 is the fix.

### 6.2 The architecture is re-derived with a model call instead of being read

§1.1(b). And `.scio/plan.json` — written by the build, read by the promotion — holds the plan, the
contracts and the whole. **The change path is the only consumer of this workspace that does not
read the file the workspace keeps for exactly this purpose.**

### 6.3 The bridge sends an index and the window throws it away

`inventory()` (`bridge.js:167-178`) returns every `data-scio-id` on the current route, and it is
sent on `ready` and on `ping`. That is a per-route retrieval index for free. It is what a layers
panel, a *select every instance* control, and an "is this element even addressable before you
click it" affordance are all built on. Nothing reads it.

### 6.4 Where packing is correct, and must stay

The marked file's source goes in verbatim, and `change_prompt`'s docstring is right about why:
*"A model asked to change code it cannot see invents a plausible replacement, which is how ids get
lost — and a lost id is a failed build (B039)."* That is packing, it is deliberate, and it is
correct. The argument in §2.3 is about *which* files, never about summarising them.

Likewise `fence('the markings', instruction)` (`change.py:171`) — the instruction is assembled
from what the user typed *and* text scraped out of the running page, and fencing it as untrusted
data rather than instruction is right (B104). Any retrieval added here inherits that boundary.

---

## 7 · Token economy

Measured 2026-08-26 against the real `change_prompt`, the real `contract_prompt`, and the real
catalogue feature package (`library/catalog/booking-feature/files`, 8 files, 11,089 chars). Token
figures are chars ÷ 4 unless stated. Prices from `execution/matrix.yaml` as loaded: `architecture`
and `codegen` both rank **claude-opus-5 first at $5 / $25 per MTok**.

**A directed change should be the cheapest model call in the system.** It edits code that already
exists, at a location already resolved, behind a guardrail that can roll it back. Here is why it
currently is not.

### 7.1 One marking, one package, today

| Call | Site | in ≈tok | out ≈tok | ≈cost |
|---|---|---:|---:|---:|
| whole, pass 1 | `main.py:502` → `whole.py:132` | 314 | 300 | $0.0091 |
| whole, pass 2 | same relay | 614 | 300 | $0.0106 |
| the change | `change.py:194` | 2,999 + 366 system | 627 | $0.0325 |
| **total** | | | | **$0.052** |

Two readings, and the second is the one that matters:

- **38% of a directed change buys a narrative that is discarded on the next line** (§1.1(b)).
- **77% of the change call's input is files that will not be touched** — 2,321 of 2,999 tokens.

The catalogue package is *small*, because library entries are compact by construction. A
generated feature package is not: `expected_output_tokens(pkg_feature_booking) = 16,000` for one
pass, which is roughly what its source weighs. Re-run on that basis:

| Scenario | in ≈tok | out ≈tok | ≈cost | vs today |
|---|---:|---:|---:|---|
| **today** — whole package, no contract, + the Layer B call | 16,400 | 2,000 | **$0.152** | — |
| §2.1 alone — drop the Layer B call | 16,400 | 2,000 | $0.132 | −13% |
| §2.1 + §2.2 — add the contract (1,310) | 17,710 | 2,000 | $0.139 | −9% |
| §2.1 + §2.2 + §2.3 — dependency-complete file set (~3 of 8 files) | 5,010 | 2,000 | **$0.075** | **−51%** |
| §4.1 — deterministic property edit | 0 | 0 | **$0.000** | −100% |

Adding the contract costs $0.007 and buys the token rules, the accessibility rules, the scope
guard, the vocabulary and the acceptance criteria. Scoping the file set pays for it eighteen
times over.

### 7.2 The ceiling covers the wrong half

`CHANGE_CEILING_USD = 2.0` is threaded into `_edits_for` and nowhere else. At $0.15 a change that
is ~13 changes in a batch — generous, as intended. But the Layer B call at `main.py:502` is
**outside** the ceiling and **outside** `meter()`. The one call nobody chose to make is the one
nobody is charged for and nobody can cap. Nothing tests the ceiling at all (§2.5).

And `passes` is a request field defaulting to 1 (`main.py:471`) that the API never sets. Raising
it to 4 multiplies the change call and the ceiling is the only thing between that and the invoice.

### 7.3 There is nothing to cache, and there is an easy way to fix that

Anthropic prompt caching is a strict prefix match; reads cost ~0.1×, a write ~1.25×; at most four
breakpoints; the minimum cacheable prefix is **512 tokens on Opus 5** (1,024 on Sonnet 5 and Opus
4.8; 4,096 on Haiku 4.5 — Layer A §7.3 has the table, and the non-monotonicity is a routing
hazard, not a growth one).

Today the change prompt opens with `# Package: pkg_feature_booking` and goes straight into the
code, which changes every round. **The cacheable prefix is zero tokens.**

With §2.2's contract-first ordering, the constant prefix is contract (1,310) + `FIX_SYSTEM` (366)
= **1,676 tokens**, byte-identical across every round of a refine session on that package — 3.3×
the Opus 5 floor. A five-round session on one package:

| | tokens billed at full rate | tokens billed at cache-read rate | ≈cost of the prefix |
|---|---:|---:|---:|
| today | 5 × 1,676 = 8,380 | 0 | $0.042 |
| contract-first, cached | 1,676 × 1.25 = 2,095 | 4 × 1,676 → 670 effective | $0.014 |

Three caveats belong in the ADR. **The default cache TTL is five minutes** — a user thinking
between rounds misses it, and the one-hour TTL is the right lever only *if* §8 shows sessions run
long, which is a measurement rather than a guess. **Verify with `usage.cache_read_input_tokens`**:
zero across rounds means something in the prefix varies. And **the win multiplies by rounds, not
by markings** — a single-round change gains nothing.

### 7.4 Effort routing — and the edit format is the bigger variable

The change call is a bounded edit on files that already exist, validated by `extract_files` with
an allow-list, guarded by `directed_regenerate`, and rolled back on failure. That is the safest
place in the system for a cheaper model — the same argument Layer C §7.4 makes about
`advise_grouping`, with a stronger guardrail behind it.

But the harness evidence says the **edit format** is worth more than the model choice. `_edits_for`
requires the model to return *complete files* (`change.py:174`), which is the format aider's
benchmarks call `whole`: easiest for a model, heaviest in tokens. On a 2,000-token file, changing
one Tailwind class costs 2,000 output tokens. The alternatives are a first-party contract
(`str_replace_based_edit_tool`) or a search/replace block, and the published claims — 5–14 points
across 15 models and ~20% fewer output tokens from changing only the edit tool; 20% → 61% on
aider's refactor suite from switching format — are large enough to be worth measuring and too
model-specific to adopt on faith.

**Decide both with the harness in §3.6, not by argument.** The eval set is free: §8's before/after
corpus is every change ever made.

### 7.5 Latency, which the user experiences and nothing measures

The interactive path today is: two sequential Opus passes for a discarded narrative → one codegen
call → `build_manifest` → `verify_instrumentation` → `typecheck` (a real `tsc` run over the app) →
`git add`/`commit`. §2.1 removes two round trips. §4.1 removes all of them for the most common
kind of change. §4.8 could halve the rest. Nothing currently records how long any of it takes.

---

## 8 · Data worth owning

**Markings, rejections and re-prompts are the highest-signal data the product ever sees, and all
three are discarded.** Every other layer's data is about what Scio did. This layer's data is about
what a human thought was wrong with what Scio did, pointed at the exact element, in their own
words. Nothing else in the system produces a supervised pair.

| Data | Why it is worth having | Where it already exists |
|---|---|---|
| **The marking** — id, tag, on-screen text, **route**, note, resolved package/file/line | *(generated UI, human's objection)*, localised to a line. The training and eval set for the classifier in §4.1, and the only direct evidence of what generated apps get wrong | `MarkingOutcome` has all of it except `route`, which the bridge sends and the DTO drops (§1.1(f)) |
| **Unaddressable markings** | a direct measurement of instrumentation coverage: which element kinds, in which package kinds, users try to mark and cannot. This is the priority list for `stamp_files` | `resolved.unaddressable`, returned and shown, never stored |
| **Re-prompts** — a second batch touching the same `scio_id` in one session | the definition of a failed change, and the only honest success metric this layer has | derivable today from `design_version.ref.change` + the manifest; nobody derives it |
| **Rounds per session, and where a session stops** | whether people iterate to satisfaction or give up. The impatient user in `JOURNEY-INVOLVED-PATH.md` step 8 does not do a second round — is that typical? | design version numbers per project |
| **Conflicts raised, and which answer** | keep-as-is vs change-the-plan, per kind. The only evidence that the regex rules are neither too tight nor too loose. **The false-negative rate needs a different instrument** — a conflict never raised is invisible, and that is the failure that matters for ADR-0001's wedge | `Conflict` objects, returned and discarded |
| **Allowances granted, per kind, per spec version** | a security ledger. `assumptions.amendments` already records kind, sentence, note and timestamp — it is written and never read back | `spec.service.amend:234-242` |
| **Rollbacks and rejections, per package kind** | how often the guardrails fire, which is how you tell a tightening from a regression | `PackageChange.rolled_back`, `.rejection` |
| **Cost per change, predicted vs actual** | nothing predicts a change (§4.7) and the actual is dropped before the browser (§1.1(g)) | `total_cost_usd`, `usage_event` |
| **The before/after pair, per commit** | **the eval corpus for every prompt, edit-format and model change in this layer, and it is already produced.** `commit_change` returns a sha per batch and the manifest travels in the same commit | git, today |
| **Per-route renders at each design version** | the baseline §4.2 needs, and the artifact §3.3's design gate would freeze | does not exist |
| **Which notes were deterministic-eligible** | §4.1's classifier training set. Bootstrap by labelling the existing note corpus | does not exist |

Aggregate, the moat one level down from Layer C §8: after fifty booking apps you know which
elements get marked first, which notes recur, what *"too big"* means in this app kind, and which
package kinds produce unmarkable UI. That makes instrumentation, the classifier, the token
defaults and the estimate all better at once, and it cannot be bought.

**None of this needs new collection.** It needs not throwing away what already passes through —
plus one field (`route`) that is computed, displayed and dropped between the browser and the DTO.

Same constraint as everywhere else: this is derived from user data, some of it is *what a person
disliked about their own project*, and **ADR-0019 (deletion and retention) is still Proposed.**
Settle what survives a project deletion before the corpus accumulates, not after.

---

## 9 · ADR proposals

| # | Proposal | Decides |
|---|---|---|
| **F-1** | **The change path stops re-running Layer B** | `derive_architecture(spec)` directly, keeping `is_buildable`; deletes a two-pass Opus call, $0.020 and two round trips from every change |
| **F-2** | **The change is given its contract, read from the workspace, and placed first** | `load_plan(app_dir).contracts[package]`, contract before code. Fixes the token, accessibility, vocabulary and scope rules never reaching the one call that changes how the app looks — and creates the only cacheable prefix this layer can have |
| **F-3** | **The prompt is scoped to the smallest dependency-complete file set** | marked files plus their intra-package imports. The isolation proof keeps allowing the whole package, so the guarantee does not narrow — only the bill and the blast radius of a careless model |
| **F-4** | **A security amendment is enforced server-side** | a server-issued, single-use conflict token bound to `(project, spec_version, kind, spec_says)` — not a `confirmed` boolean. Today one POST with a template-derivable sentence silences a protection forever |
| **F-5** | **A deterministic edit path for property and token changes** | classify, codemod at `file:line`, no model call. The classifier **refuses into the model path** rather than guessing. This is what every competitor ships and Scio has better inputs for |
| **F-6** | **Impact analysis before generation, and a change report** | product invariant #2. `PRODUCTION_READINESS_DIFF.md` §6's pipeline; Chianti's report shape; ddmin's minimality; tiered per Layer B **B-1** and Layer C **C-6**. Includes the "scope expanded — approve?" moment that does not exist |
| **F-7** | **The design gate exists, and freezes a second contract** | what "approved design v1" contains — sha, manifest, token set, per-route render, spec version — or `freeze` is deleted. Without it, *"it looks like what you approved"* has no referent |
| **F-8** | **The deterministic design gate runs on every change, not only every build** | `app-design` §5's six checks on changed files; contrast from the token set; axe-core in the preview, where the bridge already is. The claim is *"the automatable share passed"*, never *"accessible"* |
| **F-9** | **The visual isolation proof** | per-route screenshots at the previous commit vs the new one, scoped to the affected set (TurboSnap's algorithm over `plan.graph`). Conditional on deterministic rendering |
| **F-10** | **The reveal shows its nine items** | product decision. `checks_passed` is the free first one — computed, typed, transmitted, rendered nowhere. The design window already shows two of the nine that the reveal does not |
| **F-11** | **A change is quoted before it is made and priced after** | replaces the flat `$2.00`; covers every model call in the change path, not only codegen; and answers the loudest complaint users have about this category of product |
| **F-12** | **`/live`, `/versions`, `/notifications`** | the real question is whether a delivered app is refined on a preview twin of the same commit (A), by shipping a disabled bridge (B — refuse), or on the design preview as today (C, undocumented). `/live` is a redirect either way |
| **F-13** | **Design-window telemetry before any change to the loop ships** | the Layer C **C-12** argument one layer over: this is the interaction the product is differentiated by and no change to it can currently be shown to be an improvement |
| **F-14** | **`route` travels with the marking** | one field. Prerequisite for F-9's per-route baseline and for F-6's report, and the highest-signal column in §8's corpus |

**Ordering.**

**F-1 and F-2 first, and neither is close.** Both are small, both remove a wrong default rather
than adding a feature, and F-2 fixes the fact that the model changing the app's appearance has
never been told the app has a design system. Together they are perhaps forty lines.

**F-13 and F-14 next**, for the same reason A-3 comes first in Layer A and C-12 in Layer C: they
make everything after them decidable rather than arguable. **F-4 next** — small, security, and
the only finding here an attacker can use today. Then **F-3** and **F-11**, both cheap and both
measurable against F-13's baseline.

Then **F-5**, the largest single win in the layer and the thing the competition already has. It
needs F-14, and it should not ship before F-13 can show it did not make refusals worse. **F-8**
and **F-9** follow in that order: the design gate is free and runs on files; the visual proof
needs rendering and is conditional on the verification database.

**F-6** is the biggest and lands last — after Layer B's **B-1** and Layer C's **C-6**, because a
plan-level impact set is its input and a naive closure over six packages is "the whole app with
extra steps". Building the interesting half first is how this layer ends up with a change report
nobody can trust.

**F-7, F-10 and F-12 are product decisions** and belong in the planning chat rather than an
implementation queue. F-7 in particular is not an omission — it is the second of the two contracts
the product's own flow document is built on, and it has never been decided.

**Dependencies across documents, stated plainly:** F-6 waits on B-1 and C-6. F-9's affected-set
scoping wants C-7's real antichain, and §4.8's concurrency is blocked on it outright. Everything
else — F-1, F-2, F-3, F-4, F-5, F-7, F-8, F-10, F-11, F-12, F-13, F-14 — is Layer F's alone and
blocked on nothing.

**Four open questions I could not settle from the code:**

**a. Can a design version that does not compile be promoted?** `stream_promotion` delivers the
workspace as it stands; `compiles` is advisory and the version is committed either way, for a good
reason (B048). Whether the delivery build refuses, warns, or proceeds is policy nobody has
written, and it belongs in ADR-0017's consequences.

**b. Is the "approved design" a version or a moment?** F-7 assumes a frozen artifact. It could
instead be a property of the current design version. That decides whether the timeline has
approved and unapproved entries, which decides what `/versions` shows.

**c. What is a directed change worth?** `CHANGE_CEILING_USD` is a placeholder with a comment
saying so, B063 (customer-facing pricing) is still `todo`, and F-11 produces a number without
deciding what to charge for it. That is a business decision upstream of this layer.

**d. Does ADR-0018 get accepted, amended, or overtaken?** The reveal already behaves as if §1 and
§2 were accepted while the ADR stays *Proposed*, which means a future reader cannot tell which
parts were decided and which were drifted into. F-10 and F-12 both touch it. It should be marked
Accepted or rewritten to match what was built — the as-built pass raised this and nothing has
moved.

---

*Written 2026-08-26. Every code claim carries `file:line` and was checked against the working
tree at `00408d3`. The change-prompt sizes, the contract-prompt render, the package file counts,
the 22.6% marked-file share, the model matrix prices, the `contracts=` grep and the test runs
(39 engine design tests; `design.test.tsx` 5×; the full `apps/app` suite 3×) were produced by
running the real code, not read off it. Token figures are characters ÷ 4 and inherit that
estimate's error bar — `messages.count_tokens` is the correct instrument and no API key was
available. Competitor mechanisms are from vendor documentation and engineering posts read
2026-08-26 and are described as those documents describe them; nothing was reproduced. axe-core,
TurboSnap and edit-format figures are the publishers' own and their sampling limits are stated
where they are used. Speculation is marked as speculation. Nothing here is implemented, and
nothing in `hello-world` was modified.*
