# Layer D · The component library — what to build next

Forward-looking. `docs/as-built/LAYER-D-LIBRARY.md` is the starting point; this is what to do
with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

---

## 1 · Where Layer D stands

Assembly first, generation as the fallback. Re-verified 2026-08-26 against the code:
`test_library.py` (47) + `test_contribute_back.py` (27) + `test_catalog_store_pg.py` (3 run,
6 skipped without `SCIO_CATALOG_DB`) → **77 passed, 6 skipped in 1.72s**.

The best idea in the layer, and the one every proposal below is built around, is `Contract`
(`identity.py:140`): three sorted, de-duplicated string lists, the entity blanked out by
construction, and one test that decides everything (`identity.py:184`):

```python
set(self.operations) <= set(other.operations)
and set(self.routes)     <= set(other.routes)
and set(self.files)      == set(other.files)
```

Two subsets and an equality. No score, no threshold, no embedding. That is what makes a match
**decidable** rather than a judgement call, and it is the hardest thing here to rebuild
correctly.

### The constraint that governs everything below

From `matcher.py:217`:

> *a matcher that cannot decide generates; it never guesses*

and the asymmetry it exists to protect, from `matcher.py:1`:

> *Generating something the library already has costs money and consistency. Assembling the
> wrong thing ships code that looks reviewed and is not what the user asked for.*

**Any proposal that lets a model, a similarity score, or an embedding *decide* a match is out
of scope.** Proposals may change what is **retrieved**; they may not change what **decides**.
This is Layer D's equivalent of Layer A's gate, and §6 is written entirely inside it.

### The state, verified rather than repeated

Four claims from `as-built` were re-checked directly against `default_catalog()`:

| Entry | layer | category | offerable | contract empty | operations |
|---|---|---|---|---|---|
| `feature-booking` | feature | `booking` | yes | **no** | `cancel_entity, create_entity, list_entity` |
| `ui-button` | ui | *(none)* | yes | **yes** | — |
| `ui-empty-state` | ui | *(none)* | yes | **yes** | — |
| `ui-field` | ui | *(none)* | yes | **yes** | — |

`Contract.empty` short-circuits `satisfied_by` to `False` (`identity.py:210`). **The matchable
catalog is one entry.** Running the library's own gate over its own seeds:

```
feature-booking  accepted  []
ui-button        rejected  ['instrumented', 'tested']
ui-empty-state   rejected  ['instrumented', 'tested']
ui-field         rejected  ['instrumented', 'tested']
```

Three of four shipped entries would be refused by `review()` (`gate.py:120`) if they were
offered today. The test that would have caught it skips non-feature entries
(`test_library.py:640`).

`contribute_build` is called from exactly one place — `pipeline.py:321`, inside
`stream_full_build`. `stream_promotion` (`pipeline.py:353`), the path that delivers the app a
user shaped in the design window, never calls it and holds no `Architecture` to pass.

And the recall cost of decidability, reproduced rather than asserted:

```python
Contract.of(operations=['create_booking','cancel_booking','list_booking'], entity='booking')
Contract.of(operations=['create_appointment','cancel_appointment','list_appointment'], entity='appointment')
# → both ['cancel_entity','create_entity','list_entity']    keys equal.  This works.

Contract.of(operations=['reserve_table','release_table','list_reservations'], entity='booking')
# → ['list_reservations','release_table','reserve_table']   the project's own words, kept.
```

Generalisation is string substitution of the entity. An app whose operations do not *contain*
its entity name keeps its own vocabulary and can never equal anyone else's contract. This is
the **vocabulary problem** (Furnas, Landauer, Gomez & Dumais, CACM 1987) arriving in a system
that has no way to see it happen. Nothing measures how often it does.

---

## 2 · Refining what exists

### 2.1 The `files` equality test silently nullifies the `routes` subset test

This is the single most consequential thing found in this layer, and it is demonstrable in
four lines. Feature file plans are *derived*, not declared (`builder/file_plan.py:70–83`): six
fixed template paths plus `_route_to_page(node.name)` for every screen node. `package_routes`
reads the same screen nodes. So the screen set determines both `routes` and the variable half
of `files`.

Against the shipped booking entry:

| Package | routes | matches `feature-booking`? |
|---|---|---|
| `/booking` + `/booking/new` | 2 | **yes** |
| `/booking` only | 1 | **no** — `[]` candidates |

The second package asks for strictly *less* than the entry provides. `routes` is a subset test
and passes. `files` is an equality test and fails, because the entry would write
`app/__ENTITY__/new/page.tsx` and the plan does not ask for it. **The subset semantics on
`routes` are dead code**: files-equality upgrades routes to equality behind them.

The consequence is not a missed match, it is **catalog fragmentation**. Every distinct screen
set produces a distinct contract key, so a booking feature with one page and a booking feature
with two are two entries that never converge. That is the mechanism by which the catalog
"scatters into near-unique contracts" — as-built open question (a) — and it is structural, not
statistical.

**Proposal: route-parametric entries.** An entry declares route templates and the files each
route contributes; adapting to a package selects the routes the package asked for and *derives*
the file set. Then `routes ⊆ routes` implies `files ⊆ files`, and the equality assembly
re-check at `assembler.py:138` still holds because the derived set is the plan by construction.

The claim this rests on, and it must be checked rather than assumed: in the Next.js App Router
a `page.tsx` is an entry point and is never imported by another file, so dropping one cannot
dangle an import. The import boundary already in the build is what proves it per entry.

### 2.2 A failed assembly is terminal; an unfittable one is not

Same shape of failure, opposite treatment:

| Failure | Where | What happens |
|---|---|---|
| entry imports symbols the app does not export | `unmet_requirements`, `orchestrate.py:348` | `assemble = False` → **generate instead** |
| entry fails `verify_instrumentation` after writing | `assembler.py:172` | `needs_look` → `orchestrate.py:403` files it **broken** |

`assembler.py:82` states the principle for the first: *"knowing a component does not fit BEFORE
dropping it in means the package can simply be generated instead, which is a working app rather
than an honest report about a broken one."* The second violates it. Pick one and apply it to
both (as-built open question (b)) — and note that falling back makes the library **strictly
safe to try**, which is the property every other proposal here assumes.

The cost is that entry rot becomes invisible, which is precisely what §3.2's ledger is for.

### 2.3 `Quality.better_than` compares across two measurement worlds

`evidence()` (`entry.py:95`) is a 5-tuple mixing build-gate counts with `accessibility_score`
and `lighthouse_score`. Every contributed entry today carries `scores_measured=False` and zeros
in the last two, so comparisons are homogeneous **by accident**. When B048 lands, a Pareto
comparison between a measured and an unmeasured entry becomes meaningless and nothing in
`better_than` knows.

One line fixes it: refuse to compare when `scores_measured` differs, and fall back to the
build-gate triple. A comparison that cannot be made honestly should return `False` — "not
better" — which keeps the incumbent, which is the conservative direction.

### 2.4 The index that was built for a query nobody wrote

`library_entry_contract` is indexed on `contract_key` (`store.py:156`), written on insert
(`store.py:343`), and **queried by nothing**. `_existing_with_same_contract`
(`contribute.py:299`) is a linear Python scan over the whole catalog, and the catalog it scans
comes from `SELECT payload FROM library_entry WHERE status <> 'rejected'` (`store.py:241`) —
every entry, full JSON, into memory. This is one SQL statement pretending to be an algorithm.
See §6.

### 2.5 Delete the dead surface before anything is built on it

`gate.propose` (`gate.py:257`) is exported, uncalled, and its docstring actively lies —
*"the contribution itself … is stubbed in this slice"* (`gate.py:16`) has been false since
B061. Also uncalled: `store.next_id` (`store.py:418`), `CatalogEntry.adapted_paths` /
`adapted_ids` (`entry.py:262`, `:266`), `CatalogEntry.depends_on` (`entry.py:182`),
`Provides.capabilities` and `Provides.canonical_entities()`.

`library/verification/` (681 lines of pglite harness) is not the component library and belongs
in `builder/`. It inflates every dependency count anyone reads about this layer.

### 2.6 The three `ui` seeds: give them a mechanism or delete them

They cannot match (empty contract), cannot be reached (`Catalog.by_layer` has no production
caller), and would fail their own gate. Keeping them makes the library look four times bigger
than it is, in a document that is used to decide how much to invest here. Either the `ui` and
`pattern` layers get a matching mechanism of their own — and §4.2 argues the honest one is not
a contract — or the entries go and `Layer` shrinks to what the matcher can use.

---

## 3 · What is missing

### 3.1 Nobody consented, and nothing carries a licence

Grepped 2026-08-26 across `library/**`, ADR-0014, ADR-0016 and ADR-0019 for
`consent | opt.in | licen[cs]e`: **zero matches.**

`CatalogEntry` records `source_project` and `provenance=f"contributed:{project_id}"`
(`contribute.py:245`) — so the system knows exactly whose build it took code from — and has no
field for a licence, no record of permission, and no mechanism to withdraw. Then
`assemble_package` writes that code into a different tenant's app, which ADR-0001 says the user
**owns**.

This is not a compliance footnote. **Contribute-back is the differentiator** (§4.3), so the
thing that makes the library defensible is also the thing that has no legal basis recorded
anywhere. It cannot be retrofitted after the corpus exists, for the same reason Layer A §6
cannot: the entries already in the catalog would each need a consent that nobody asked for.

What to adopt rather than invent:

- **SPDX license expressions** ([spec 3.0.1, Annex B](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/))
  as a `license: str` field on `CatalogEntry`, parsed and compared with
  [`license-expression`](https://pypi.org/project/license-expression/) (AboutCode, bundles the
  SPDX list and the ScanCode DB). One field, one dependency, and the assembly step can then
  refuse an entry whose licence is incompatible with the target app's.
- **An explicit contribution grant**, recorded per project and per entry, with the ADR-0019
  deletion semantics attached: what happens to an entry when the project it came from is
  deleted. Today the honest answer is "nothing, and nobody decided that".

### 3.2 The match-and-miss ledger — a prerequisite, exactly as Layer A §3.3 is

Nothing measures Layer D. `matcher.py` records `considered` per package (`matcher.py:71`) and
`Outcome.reason` explains every refusal (`contribute.py:69`), and **both are thrown away**. The
best number in the repo is a test assertion pinning the canonical demo at *"1 of 5 parts from
the library, 4 generated"* — 20%, against a strategy that wants 80%.

Six numbers, all computable from data that already flows:

| Metric | From |
|---|---|
| match rate, per build and per category | `MatchReport.assembled` / `matches` |
| **near-miss distance** — how many operations/routes/files short | `contract` vs each `considered` entry |
| **vocabulary-miss rate** — packages whose operations do not contain the entity | `entity_forms` vs `package_operations`, free |
| **contract-key cardinality per category over builds** | the convergence-vs-fragmentation question, directly |
| gate refusal reasons, aggregated | `Outcome.reason`, already written |
| assembly failures per entry | `assembler.py:172`, entry rot |

The two that pull against each other, which is what makes the ledger honest: **relaxing the
contract raises match rate and raises the risk of assembling the wrong thing.** A change that
improves one while worsening the other has not improved anything, and only a ledger can show it.

`StandInIntakeProvider`'s equivalent here is the shipped seed catalog: a fixed, free baseline of
one entry. **A change to this layer that does not beat it is not an improvement, it is an
expense.**

Near-miss distance is the one to build first. It answers "what would we have to relax to double
the match rate", which is the question §2.1 is guessing at.

### 3.3 The delivery build never teaches the library

`stream_promotion` is the path with the most human attention on it — the user marked elements,
described changes, and accepted the result — and it contributes nothing. ADR-0016 documents one
exclusion (*"a preview build (Level 2) contributes nothing"*) and is silent on promotion, which
reads as oversight rather than decision.

The obstacle is real but small: `stream_promotion` loads a stored plan (`pipeline.py:384`) and
has no `Architecture`, which `_project_terms` needs (`contribute.py:110`). Two ways out —
store the architecture beside the plan, or derive project terms from the plan's own
`architecture_slice` node names, which are already `NodeRef(kind="table", name=…)`. The second
needs no migration.

### 3.4 Nothing knows whether an assembled part survived contact with the user

This is the strongest quality signal in the system and it is one field away.

The design window resolves a marking → element id → package (`BuildFinished.manifest`). A
package built by assembly carries `entry_id` on its `PackageBuildResult` (`result.py:59`). But
`BuildFinished` (`pipeline.py:63`) has no `entry_id` anywhere — not on the manifest, not on
`package_files`, not in a list. So the reveal cannot say which parts came from the library, and
**nothing can compute the rate at which assembled parts get marked and rewritten.**

An entry whose assemblies are marked-and-changed in 80% of projects is a bad entry, however
green its gates. That number is exactly what `Quality.better_than` (§2.3) is missing: real
evidence, produced by users, about entries that are already in the catalog rather than about
candidates arriving.

Note the side effect: the composition line the user reads (`SpecPage.tsx:434`,
*"5 parts · 1 reused · 4 built"*) is shown **before** the build and never again. The promise is
made at the estimate and never confirmed at the reveal.

### 3.5 The curation surface has no human in front of it

Five endpoints exist (`main.py:603–665`); `engine.client.ts` contains no `/library` call;
there is no proxy and no UI. ADR-0016 argued provisional-but-offerable *"keeps a person in the
loop without making them the bottleneck"* — with no person in the loop, `provisional` is
decoration. Build the surface or amend the ADR to say entries are auto-approved. Both are
defensible; the current state is neither.

### 3.6 Contribution spends outside the build's budget ceiling

`RelayOptions` carries `budget_usd` and `spend` (`relay.py:52–55`) — *"the build's running
total, shared across calls. This is the real ceiling."* `generalize` (`generalize.py:199`) and
`suggest_labels` (`generalize.py:265`) pass **neither**, while package builds pass
`Spend(ceiling_usd=budget_usd)` (`estimate.py`, `orchestrate.py`). A build that hits its ceiling
still runs one uncapped 16,000-token generalisation per contributable package afterwards. See
§7 for what that costs.

---

## 4 · Out of the box

### 4.1 The question asked head-on: importing a large third-party component collection

`REVIEWS-WHAT-WE-MISSED.md` §4 is the constraint. Lovable already ships versioned design
systems with adherence checks, a managed private npm registry, cross-project referencing of
components and auth flows, and templates — and [February 2026 shipped cross-project
`@`-referencing](https://training.blackbadger.biz/articles/cross-project-referencing-lovables-latest-release-feb-2026)
on top of that. *"We have a component library" is not in itself a differentiator.*

So: **if a large block collection were imported, what would have to happen to each entry before
it could match?** This is answerable exactly, because every gate is a function in the repo.
Take a shadcn `registry:block` — the richest, best-specified third-party format there is
([registry-item.json](https://ui.shadcn.com/docs/registry/registry-item-json)) — and walk it
through:

| # | What Scio requires | Where | A shadcn block has | Can it be filled? |
|---:|---|---|---|---|
| 1 | files as `path → body` | `entry.py:load` | `files[].path` + `target` | **yes**, mechanical |
| 2 | npm deps | `npm_dependencies` | `dependencies` | **yes**, mechanical |
| 3 | token bindings | `token_bindings` | `cssVars` (theme/light/dark) | **yes** — and DTCG already covers it (`app-design` §1) |
| 4 | a canonical `category` | `categories.py` | `categories[]`, free text | **maybe** — via the registry's alias resolution, else *proposed* |
| 5 | **`operations`** | `Contract.operations` | **nothing** | **no.** A block declares no operations. Inventing them is a judgement call |
| 6 | **`files` == the package's file plan** | `identity.py:184` | its own paths | **no.** `planned_files` is six derived paths plus route pages; a block's tree is never that set |
| 7 | **`__ENTITY__` in paths and bodies** | `gate._generalization_findings` | a concrete domain noun, or none | **no.** Requires knowing which noun *is* the entity |
| 8 | `data-scio-id` on every element | `gate` rule `instrumented` | none | mechanical to add, but it is a rewrite of every file |
| 9 | a shipping test file | `gate._has_tests` | none | **no.** Somebody must write it |
| 10 | `security_reviewed = True` | `gate` rule | nobody reviewed it | **no.** Requires a person or a scanner nobody has built |
| 11 | a11y + Lighthouse ≥ 85 | `MIN_ACCESSIBILITY`, `MIN_LIGHTHOUSE` | unmeasured | requires B048 |
| 12 | no leaked URLs/emails | `_LEAK_PATTERNS` | demo blocks are full of avatar URLs | fails as shipped |
| 13 | survives `reverify` against `widget` | `reverify.py:49` | untested | only after 5–8 |
| 14 | a licence and a provenance chain | **does not exist** | MIT for shadcn itself, varies per registry | §3.1 |

**Rows 5, 6 and 7 are the ones that decide matchability, and all three can only be filled by a
judgement call — which is the one thing this layer is designed never to make.** A block has no
operations because it is not a feature; it has the wrong file set because the file plan is
derived from an architecture it knows nothing about; it has no entity because it is not about
anything.

The honest conclusion: **importing a visual block collection would not add one matchable entry.**
It would add a large amount of `ui`-layer inventory of exactly the kind that already sits in the
catalog unreachable (§2.6), and it buys the half of the problem that `REVIEWS-WHAT-WE-MISSED.md`
§4 says is explicitly not the differentiator.

### 4.2 So don't build a registry — consume one

The `ui` and `pattern` layers are a real gap, and the right answer is not to copy files into our
catalog. It is to point at a registry that already exists and is already agent-addressable:

- the **shadcn registry format** is a published JSON schema with namespaces (`@acme/item`),
  `registryDependencies`, `cssVars`, and — as of
  [May 2026](https://ui.shadcn.com/docs/changelog/2026-05-registry-include) — `include` for
  composing large registries from multiple files;
- the **shadcn MCP server** ([docs](https://ui.shadcn.com/docs/mcp)) already exposes browse,
  search and install across registries to a coding agent;
- ADR-0011 already fixes the generated stack to this ecosystem, so a shadcn item is *native*
  output, not an import.

Then the `ui` layer is a **reference**, not a copy: an entry that says "this project uses
`@shadcn/button`" rather than one that carries a `button.tsx`. That removes the maintenance,
the licence question, and the gate problem in one move, and it is honest about what the layer
is for.

**The trade-off, named:** a reference means we do not control the code, cannot instrument it
until install time, and inherit upstream's breakage. A copy means we own all three problems
forever. For `ui` the reference wins because the code is commodity; for `feature` the copy wins
because the code is the asset. That line — commodity by reference, asset by contract — is the
one worth writing into an ADR.

### 4.3 The differentiator is the evidence, not the catalog

`REVIEWS-WHAT-WE-MISSED.md` §4 lists what is *not* publicly documented at Lovable: automatic
contribution from every successful build, generalisation away from project terms,
re-verification after generalisation, contract-based automatic matching before generation,
quality evidence per reused feature, Pareto replacement, assembly-first.

Every one of those is a claim about **provenance and evidence**, not about inventory. The
library's product is not "we have parts"; it is *"this part was produced by a build that passed
these gates, generalised by this method, re-verified against an unseen entity, and has been
assembled into N apps with this marking rate."*

That is a supply-chain claim, and the supply-chain world has standards for it that we should
adopt rather than invent — the same lesson as DTCG in `app-design`:

- **in-toto / SLSA provenance** — an attestation binding an artifact to the build that produced
  it. `Quality` already *is* an unsigned, ad-hoc predicate: `build_gates_passed`,
  `build_gates_total`, `test_files`, `instrumented_elements`. Re-express it as an attestation
  predicate and the format is settled.
- **Sigstore** — keyless signing. [npm provenance is now default rather than
  opt-in](https://mondoo.com/blog/npm-supply-chain-security-package-manager-defenses-2026)
  through trusted publishing, which is why signed artifacts went from rare in 2023 to common in
  2026. An unsigned quality claim in 2026 reads as untrustworthy by default.
- **SPDX / CycloneDX SBOM** — what an entry pulls in, per §3.1.

This costs a schema and a signing step, not a research programme, and it is the only part of
this layer that is genuinely hard to copy: **anybody can import a registry; nobody can import
the evidence that our builds produced.**

### 4.4 If the ledger says contracts scatter, shrink the library

The unpopular option, stated so it is available. If §3.2's contract-key cardinality shows
contributions fragmenting rather than converging, the correct response is not to relax the
contract until they converge — that trades the layer's one guarantee for a metric. It is to
freeze the catalog at hand-written seeds, keep the assembly path, and move the investment to
Layer B §4.1's **reference-architecture library**, which compounds once per app instead of once
per package and cannot be bought.

`REVIEWS-WHAT-WE-MISSED.md` §4 already says the quiet part: *"The library is an amplifier, not
the precondition for proving the core. The core loop must work well even when everything has to
be generated."*

---

## 5 · The means — skills, MCP, repos, research

Per `docs/next/SKILLS.md`, skills help **us** build Scio and are cross-cutting. Only Layer-D
specific ones are named here.

### What exists, so we build only what does not

| Thing | What it gives Layer D | Verdict |
|---|---|---|
| [**shadcn registry-item.json**](https://ui.shadcn.com/docs/registry/registry-item-json) | a published schema for a distributable component: files, targets, deps, `registryDependencies`, `cssVars`, `envVars`, namespaces | **adopt as the `ui`-layer interchange format.** Do not invent one |
| [**shadcn MCP server**](https://ui.shadcn.com/docs/mcp) | agent-side browse/search/install across registries | **adopt later**, when §4.2 is decided. It is the mechanism, not a decision |
| [**shadcn `include`** (May 2026)](https://ui.shadcn.com/docs/changelog/2026-05-registry-include) | composing one registry from many files | reference — the shape our catalog would take if it ever ships externally |
| **npm / JSR** | distribution and versioning we would otherwise write | reference. Lovable's edge here is a *managed* registry; matching it is §9's not-yet list |
| [**W3C DTCG**](https://www.designtokens.org/tr/drafts/format/) | the token format `token_bindings` reinvents in miniature | **adopt** — already argued in `.claude/skills/app-design` §1 |
| [**OpenAPI 3.2**](https://spec.openapis.org/oas/v3.2.0.html) / [**TypeSpec**](https://typespec.io/) / JSON Schema | machine-readable operation contracts; TypeSpec emits OpenAPI *and* JSON Schema from one source | **reject for the match key, adopt later for `integration`.** Our contract is a set-membership question over ~5 strings; OpenAPI is a description of HTTP surface. Using it would make matching a schema-compatibility problem, which is undecidable in the direction we need. It becomes right the day the `integration` layer holds real connectors |
| [**SPDX license expressions**](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/) + [`license-expression`](https://pypi.org/project/license-expression/) | parse, normalise and compare licences | **adopt** — §3.1. One field, one library |
| [**SLSA**](https://slsa.dev/) / **in-toto** / [**Sigstore**](https://mondoo.com/blog/npm-supply-chain-security-package-manager-defenses-2026) | signed provenance binding an artifact to the build that made it | **adopt** — §4.3. This is the differentiator's format |
| **CycloneDX / SPDX SBOM** | what an entry drags in | adopt with SLSA, same schema work |
| [**Backstage `catalog-info.yaml`**](https://backstage.io/docs/features/software-catalog/) | the incumbent shape for "a registry of components with owners and relations", in production at 3,400+ companies | reference. It catalogues *services*, not reusable code; the relation graph is the transferable idea |
| [**Open Component Model**](https://ocm.software/docs/concepts/component-identity/) | technology-agnostic component identity + transport over OCI | reference. Right shape, wrong altitude — designed for deployable compositions |
| **Postgres GIN + `@>`** ([array containment](https://www.tigerdata.com/learn/optimizing-array-queries-with-gin-indexes-in-postgresql)) | the *exact* subset test, as an indexed SQL predicate | **adopt** — §6. Removes `store.py:241` entirely |
| [**datasketch `MinHashLSHEnsemble`**](https://ekzhu.com/datasketch/lshensemble.html) | approximate **containment** search over sets, at scale | **adopt for the near-miss ledger only.** Never on the decision path |
| **graphify** (ours) | corpus → queryable graph | **later.** Same answer as Layer A: nothing to graph at one entry. It becomes right when the ledger has a corpus of contracts |
| **Context7** | live library documentation | no. Layer D matches our own parts, not third-party APIs |

### Research

| Work | What it gives Layer D | Caveat |
|---|---|---|
| **Furnas, Landauer, Gomez & Dumais** — *The Vocabulary Problem in Human-System Communication* (CACM 1987) | the name and the shape of §1's recall cost: two people spontaneously choose the same term for a thing <20% of the time | it predicts our failure; it does not predict its *size* in our data. That is §3.2's job |
| **Prieto-Díaz** — *[Implementing faceted classification for software reuse](https://dl.acm.org/doi/10.1145/103167.103176)* (CACM 1991) | the category/hashtag split in `categories.py` **is** faceted classification, rediscovered. Names the pattern and its known failure modes | 1991 libraries failed on *human* classification effort; ours is automatic, which changes the economics but not the taxonomy problem |
| **Zhu, Nargesian, Pu, Miller** — *[LSH Ensemble: Internet-Scale Domain Search](https://arxiv.org/abs/1603.07410)* (VLDB 2016) | approximate **containment** search (`\|Q∩X\|/\|Q\|`) with MinHash + domain partitioning; the paper's whole point is that Jaccard *similarity* fails across size-skewed sets, which is exactly our entry-provides-more asymmetry | approximate. Safe only as a recall-oriented **filter** in front of the exact test — see §6 |
| **Sajnani, Saini, Svajlenko, Roy, Lopes** — *SourcererCC* (ICSE 2016) and *[Oreo](https://arxiv.org/pdf/1806.05837)* | index-then-verify at 250M LOC: an inverted index over token bags plus a filtering heuristic, then exact verification. The architecture §6 proposes, in a field that has already validated it | clone detection tolerates false positives; we cannot. We take the *index*, not the similarity measure |
| *[Semantic Code Clone Detection: Are We There Yet?](https://arxiv.org/html/2606.25272)* (2026) | the honest state of Type-4 detection — learning-based methods still do not generalise | **evidence for keeping the matcher deterministic.** The field's own answer to "can a model decide two things are the same" is still "not reliably" |
| *[SkillResolve-Bench](https://arxiv.org/abs/2606.10388)* (2026) | measures exactly `resolve_ambiguity`'s failure: a retriever finds the right capability *family* and returns the wrong same-capability sibling. Reports HSR (harmful-selection rate) driven to 0 by resolving family-first, then selecting one representative | measured on agent skills, not on component catalogs. The *metric* transfers; the numbers do not |
| *[Retrieval-Augmented Code Generation: a survey](https://arxiv.org/html/2510.04905v1)* (2025) · *[ARCS](https://arxiv.org/abs/2504.20434)* | the retrieve-then-generate framing for the packages that *don't* match — a near-miss entry is the best possible context for generating the thing it nearly was | changes what generation is *given*, not what matching *decides*. Genuinely out of scope until §3.2 exists |

All read at abstract-to-method level. None reproduced.

### Skills written for this layer

Two papers are genuinely adopted, so per `SKILLS.md` each gets a skill carrying source, method,
limits and eval:

- **`.claude/skills/contract-retrieval`** — LSH Ensemble + SourcererCC's index-then-verify, in
  the one form this layer may use it: retrieval narrows, `satisfied_by` decides.
- **`.claude/skills/reuse-classification`** — Prieto-Díaz's facets and Furnas's vocabulary
  problem, as the diagnosis and the measurement for §3.2's vocabulary-miss rate.

The Layer-D-specific build skill worth writing once §3.2 exists: **`library-ledger`**, which
runs the ledger over a corpus of builds and reports the six numbers — the Layer D twin of
`intake-replay`.

---

## 6 · Retrieval versus packing

**This layer packs almost nothing into a prompt, and that is its best property. It packs
everything into memory instead, and that is the one that breaks.**

Today's model calls are small and bounded: `resolve_ambiguity` sends only the *surviving*
candidates (`matcher.py:199`, fenced), and `suggest_labels` sends four files truncated to 1,200
chars. Neither grows with the catalog.

What does grow with the catalog:

```sql
-- store.py:241, on every match, and again per assembled package via
-- default_store().catalog() at orchestrate.py:347
SELECT payload FROM library_entry WHERE status <> 'rejected'
```

Every entry, full JSON, deserialised into Pydantic, filtered in Python. `_existing_with_same_contract`
then scans the same list again. At one entry this is free. At 10,000 entries it is the whole
build's latency and it happens once per package.

**A catalog that grows cannot be packed — into a prompt, or into a process.** The retrieval
version is three stages, and the invariant that makes it safe is the one from §1:

> **Retrieval may narrow. Only `satisfied_by` may decide.**

An approximate index that returns a **superset** of the true matches is safe, because the exact
test runs afterwards and throws away the extras. One that returns a **subset** is not, because a
dropped match is invisible. So every stage below must be tuned for recall, never for precision.

| Stage | Mechanism | Returns | May it decide? |
|---|---|---|---|
| **1 · Narrow, exactly** | one SQL query: `category = ? AND operations @> ? AND routes @> ? AND contract_key = ?`, with GIN indexes on the array columns | the true candidate set, or a superset | it *is* the exact test, expressed in SQL |
| **2 · Narrow, approximately** *(only if stage 1 stops scaling)* | `MinHashLSHEnsemble` containment query at a low threshold | a recall-oriented superset | **no** — stage 1 re-runs over its output |
| **3 · Choose** | `resolve_ambiguity`, unchanged | one entry or none | only between entries that already passed stage 1 |

Stage 1 is the important one and it is not a research project: PostgreSQL's GIN indexes support
`@>` (contains) and `<@` (contained by) on arrays natively, and `contract_key` is *already*
computed, *already* stored and *already* indexed (`store.py:150`, `:156`). Storing `operations`
and `routes` as `text[]` beside it turns the entire `candidates()` function
(`matcher.py:161–187`) into one indexed statement, and `_existing_with_same_contract` into
`WHERE contract_key = %s`.

This is the same architecture the clone-detection field settled on — SourcererCC's inverted
index with an exact verification pass — and the same one LSH Ensemble formalises for
containment specifically. We are not inventing; we are catching up to 2016.

**The trigger, stated as a number rather than a feeling.** None of this is needed at one entry
and building it now would be ceremony. Build stage 1 when either the catalog crosses ~10³
entries or `catalog()` shows up in the plan step's timing. Build stage 2 only when stage 1's
index selectivity measurably degrades — GIN needs a substantial row count before it beats a
sequential scan at all.

One packing violation that *is* worth fixing now, because it is a bug rather than a scale
problem: `orchestrate.py:347` calls `default_store().catalog()` inside the per-package loop, so
a seven-package build loads the whole catalog seven times for a lookup it already has the answer
to — `match_plan` chose the entry and `apply_matches` wrote its id onto the package.

---

## 7 · Token economy

Measured 2026-08-26 against the real prompts and the real seed entry.

| Call | Where | System prompt | Payload | Cap |
|---|---|---|---|---|
| `resolve_ambiguity` | `matcher.py:189` | `AMBIGUITY_SYSTEM` 198 chars ≈ **49 tokens** | one line per candidate | `max_tokens=64` |
| `generalize` | `generalize.py:199` | `GENERALIZE_SYSTEM` 1,048 chars ≈ **262 tokens** | booking seed: 8 files, 11,089 chars ≈ **2,864 tokens** | 16,000, 300s |
| `suggest_labels` | `generalize.py:265` | `SUGGEST_SYSTEM` 421 chars ≈ **105 tokens** | ≤4 files × 1,200 chars ≈ 1,200 tokens | 400 |
| `match_plan` | `matcher.py:228` | — | — | **0 tokens** unless two entries tie |
| `assemble_package` | `assembler.py:108` | — | — | **$0.00**, `ASSEMBLE_SECONDS = 3` (`estimate.py:113`, `:222`) |

Nothing here is cacheable and nothing should be. `GENERALIZE_SYSTEM` at 262 tokens is far below
the ~1,024-token cache floor, and the bulk of its request is a file listing that is unique per
package by construction. Layer D is the one layer where caching has nothing to offer.

### The number this layer has never had: the break-even

The library's whole economic argument is "assembly is cheaper than generation", and nobody has
ever priced the *other* side of it.

**What one assembly saves.** From `estimate.py:73–89`, `:186`, a booking-shaped feature package
is `BASE 6000 + 3 operations × 2500 + 2 screens × 2500 = 18,500` output tokens per pass, plus
`CRITIQUE_OUTPUT_TOKENS = 400`. At Opus 5's $25/MTok output that is **≈ $0.47 per pass**, and
the profile may run more than one.

**What one contribution costs.** ≈2,864 input tokens ($5/MTok → $0.014) plus an output that
mirrors the input, ≈2,800 tokens ($25/MTok → $0.070) — **≈ $0.085 per contributable package**,
with the cap at 16,000 output tokens ($0.40) as the worst case.

**Ratio ≈ 5.5 : 1.** The library pays for itself if better than roughly **one in five**
contributed entries is ever matched by a later build. That single number decides whether this
layer is an asset or an expense, it is measurable the moment §3.2's ledger exists, and today
nobody knows it.

Two consequences worth acting on before then:

- **Contribution is off the critical path but not off the bill.** It runs after delivery
  (`pipeline.py:312`) and swallows its own failures (`contribute.py:415`), so a user never waits
  for it — and never sees it charged either. Whether it is billed to the project or to the
  platform is a product decision that has been made by accident.
- **It is uncapped** (§3.6). Passing the build's `Spend` into both relay calls is a one-line
  change and it is the difference between a bounded and an unbounded tail.

---

## 8 · Data worth owning

| Data | Why it is worth having |
|---|---|
| **Contract keys per category, over builds** | the convergence-vs-fragmentation answer. This is the number that decides whether to invest further in this layer at all (§4.4), and it exists nowhere |
| **Near-miss distances** — which single operation, route or file stopped a match | tells you exactly what to relax, and §2.1 predicts most of it will be one route |
| **Vocabulary-miss rate** | how often a project's operations do not contain its entity. Furnas's problem, in our data, for free |
| **Marked-after-assembly rate, per entry** | §3.4. The only user-produced evidence about entries already in the catalog, and the missing input to `better_than` |
| **Entries never matched** | dead inventory. A library with an unmeasured tail is a scrapyard with a search box |
| **Gate refusal reasons, aggregated** | every `Outcome.reason` is already written and discarded. Tells you whether the gate is protecting the library or refusing everything — which `gate.py:40` records having already happened once, when `example.com` fixtures failed the leakage rule |
| **Provenance chains** | §4.3. The asset that cannot be imported |

Note the direction, as Layer B's data improves Layer A: **Layer D's data improves Layer C.**
The contract is derived from `planned_files`, which Layer C owns. If contracts fragment on
route sets, the cause is the file plan and the fix lives in Layer C, not here.

**The constraint to design in rather than retrofit**, and it is sharper than Layer A's: this is
not the user's *data*, it is the user's *code*, copied into someone else's app. ADR-0019 is
still **Proposed**, and §3.1 shows there is no consent record and no licence field. Everything
in this table is blocked behind that, and unlike Layer A's corpus it is already accumulating.

---

## 9 · ADR proposals

| # | Proposal | Decides |
|---|---|---|
| D-1 | **Consent, licence and provenance on every contributed entry** | whether the library may legally exist as designed. SPDX expression, a recorded grant, deletion semantics. Depends on ADR-0019 |
| D-2 | **The match-and-miss ledger is a prerequisite** | no change to Layer D ships without beating the one-entry baseline on the six metrics |
| D-3 | **Contract retrieval by index, not by loading the catalog** | GIN `@>` in SQL; retrieval narrows, `satisfied_by` decides. Also removes the per-package catalog load at `orchestrate.py:347` |
| D-4 | **Route-parametric entries — files derived, not compared** | the largest behavioural change here. Ends the fragmentation §2.1 demonstrates, and requires proving pages are never imported |
| D-5 | **A failed assembly falls back to generating** | makes the library strictly safe to try; costs visibility of entry rot, which D-2 restores |
| D-6 | **The promotion build contributes** | ADR-0016 is silent on promotion. Either fix the omission or record it as deliberate |
| D-7 | **Commodity by reference, asset by contract** | the `ui`/`pattern` layers point at a shadcn-format registry; only `feature` entries are copied and contract-matched. Also settles whether the three `ui` seeds live or die |
| D-8 | **The library is an evidence store** | `Quality` becomes a signed in-toto/SLSA-style attestation. This is the differentiator, in a standard format |
| D-9 | **Curation surface, or `provisional` is decoration** | build the five endpoints a UI, or amend ADR-0016 to say entries are auto-approved |
| D-10 | **`better_than` refuses to compare across measurement worlds** | one line, before B048 makes it wrong |

**Ordering.** **D-2 first, and by a distance** — every other row on this table is currently an
argument rather than a decision, and the ledger is what makes them decidable. **D-1 runs
alongside it, not after**: entries are accumulating now, and consent cannot be obtained
retroactively. Then D-3, D-5 and D-10, which are cheap and change no promise. D-4 is the big
one and should not be attempted before D-2 can show whether it helped. D-7 and D-8 are the
strategic pair — D-7 stops us buying the non-differentiator, D-8 builds the one thing that
cannot be bought. D-6 and D-9 are corrections to ADR-0016 and should be taken together.

**Two open questions I could not settle from the code:**

1. **Does the library's own promise ever reach the user after the build?** The composition line
   is rendered at the spec gate (`SpecPage.tsx:434`) and `entry_id` never reaches
   `BuildFinished` (`pipeline.py:63`). So "assembled from curated, tested parts" is a claim made
   before the build and never confirmed at the reveal. Whether that is an oversight or a
   deliberate choice not to advertise reuse is a product question.
2. **Who is the curator?** ADR-0016 assumes a person; `main.py:603–665` assumes an operator with
   `curl`. Until somebody names the role, D-9 cannot be answered either way.

---

*Written 2026-08-26. Test counts, catalog contents, gate verdicts, contract behaviour and
prompt sizes measured against the code; research read at abstract-to-method level; prices are
list rates for the Claude API. Nothing here is implemented.*
