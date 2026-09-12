# Layer D · The component library — as built

Assembly first, generation as the fallback. 31 files, 4,152 lines, 74 tests — all passing
2026-08-26.

Governed by **ADR-0014** (the library exists), **ADR-0016** (it grows from real builds) and
`docs/LIBRARY.md`.

---

## 1 · Purpose

Stop paying a model to rediscover a booking flow. Keep a catalog of curated parts, match every
build package against it, and assemble a hit instead of generating it.

ADR-0014 states the reason and the risk in the same breath:

> A part offered *instead of* generating carries authority: nobody reviews it again per
> project. Assembling the wrong thing ships code that looks reviewed and is not what the user
> asked for.

Everything in this layer is shaped by that asymmetry. `matcher.py:1` puts it as the design
rule: *"Generating something the library already has costs money and consistency. Assembling
the wrong thing ships code that looks reviewed and is not what the user asked for."*

## 2 · Public surface

The 31 files counted as Layer D are **four unrelated things**. Only the first is the library:

| Group | Files | Lines | What it is |
|---|---:|---:|---|
| Library logic (`library/*.py`) | 14 | 2,985 | the matcher, assembler, gate, contribute path, store |
| Seed catalog content (`library/catalog/**`) | 11 | 415 | the app code the library lends out |
| Data-verification harness (`library/verification/`) | 3 | 681 | pglite in-process Postgres (B060a) — **not the library** |
| `api/modules/reference/` | 3 | 71 | tagged RAG uploads, phase 4.6 — **not the library, and not built** |

**Engine, as called by other layers:**

| Entry point | Called from | Does |
|---|---|---|
| `match_plan` / `apply_matches` | `layerc/service.py:76` | decide assemble-vs-generate for every package |
| `assemble_package` / `unmet_requirements` | `builder/orchestrate.py:335` | write an entry into the app, no model |
| `contribute_build` | `builder/pipeline.py:321` | offer a finished build's work back |

**Engine, over HTTP** (`main.py:603–665`) — the curation surface:

```
GET  /library/entries?category=&status=
POST /library/entries/{id}/approve
POST /library/entries/{id}/reject
POST /library/categories
POST /library/categories/{name}/confirm
```

**API** — `apps/api/src/modules/reference/`. Registered in `app.module.ts:43`, and both service
methods throw: `throw new NotImplementedException("reference.list — phase 4.6")`
(`reference.service.ts:20`, `:29`). It is live routing to a 501.

**Frontend** — there is none for this layer. `apps/api/src/engine/engine.client.ts` contains no
`/library` call at all; nothing proxies the curation endpoints. What reaches a user is one
line on the spec gate — `SpecPage.tsx:434` renders
`` `${parts.parts_total} parts · ${parts.assembled} reused · ${parts.generated} built` `` from
`EstimateComposition`.

## 3 · In and out

**In** — a `BuildPlan` (matching), and an `app_dir` plus `PackageBuildResult`s (contributing).

**Out** — a `MatchReport` (one `Match` per package: decision, entry id, category, contract key,
reason, everything considered), files on disk, and a `ContributionReport`.

Only two package kinds are ever in play. `matcher.py:47` and `contribute.py:53` both pin it:

```python
MATCHABLE_KINDS = (PackageKind.feature, PackageKind.auth)
```

> *"The shell, the schema and the design tokens are project-shaped — their content is derived
> from THIS app's architecture, and an entry claiming to cover one would be claiming to know
> something it cannot."* — `matcher.py:50`

### Question 2 — how `Contract` is actually modelled, and why a match is decidable

ADR-0014 says entries are "contracts with files attached". As built, `Contract`
(`identity.py:140`) is three sorted, de-duplicated string lists and nothing else:

```python
class Contract(BaseModel):
    operations: list[str] = Field(default_factory=list)
    routes: list[str] = Field(default_factory=list)
    files: list[str] = Field(default_factory=list)
```

Four properties make it decidable rather than a judgement call.

**a. The project's own words are removed by construction.** `Contract.of` (`identity.py:152`)
takes an `entity` and blanks every spelling of it before storing anything. `entity_forms`
(`identity.py:100`) produces the raw word, its singular, the canonical singular, and their
plurals, sorted longest-first *"so replacing 'bookings' never leaves a stray 's'"*. Operation
names get the literal `entity`; paths get `__ENTITY__`, because paths must match an entry's
file templates literally (`identity.py:90`). The word boundary is hand-rolled — `(?<![A-Za-z0-9])`
rather than `\b` — with the reason written down: *"an operation is called `create_booking`, and
`\b` treats the underscore as a word character, so the obvious regex silently matches nothing
and every contract stays project-specific"* (`identity.py:116`).

**b. Sorted and de-duplicated on construction**, so *"two orderings of the same contract cannot
hash differently — the whole value of this object is that equality is decidable"*
(`identity.py:143`). `.key` is a 32-char SHA-256 of the joined lists.

**c. The match test is a set relation, not a score.** `satisfied_by` (`identity.py:184`),
called as `contract.satisfied_by(entry.effective_contract())` at `matcher.py:185`:

```python
return (
    set(self.operations) <= set(other.operations)
    and set(self.routes) <= set(other.routes)
    and set(self.files) == set(other.files)
)
```

Two subset tests and one equality test. The asymmetry is deliberate — an entry may provide
more than a package needs, never less — and the file plan must be *exact*, or the manifest's
package→file map disagrees with the disk.

**d. An empty contract never matches.** `Contract.empty` is `not self.operations`, and
`satisfied_by` returns `False` if either side is empty: *"Two empty contracts would otherwise
hash identically and every uncharacterised package would 'match' every other one"*
(`identity.py:213`).

The category (`categories.py`) only *narrows* the candidate pool, and a missing category on
either side is not disqualifying (`matcher.py:184`). The relay is asked exactly one question,
in exactly one place — `resolve_ambiguity` (`matcher.py:189`) — when two vetted entries both
pass all of the above, and *"a matcher that cannot decide generates; it never guesses"*
(`matcher.py:217`). That prompt is the one place in the engine that carries text across
tenants, and it is fenced for it (`matcher.py:199`, `fenced_lines`).

**The cost of decidability, which is real and undocumented.** Generalisation is string
substitution of the entity. A project whose operations do not *contain* the entity —
`reserve_table` for entity `booking`, `confirm_slot` for `appointment` — generalises to
`reserve_table`, keeps the project's own vocabulary in its contract, and can therefore never
equal another project's. The mechanism buys perfect precision by paying in recall, and the
size of that bill is not measured anywhere.

## 4 · Invariants

Taken from the tests. Test names are the evidence.

| Invariant | Test |
|---|---|
| An entry nobody vetted is never offered | `test_an_unvetted_entry_is_never_offered` |
| Four of five operations is not a match | `test_an_entry_missing_an_operation_is_not_a_match` |
| An entry that would write one extra file is not a match | `test_an_entry_that_would_write_the_wrong_files_is_not_a_match` |
| A tie nothing can break generates | `test_two_equal_entries_with_no_judgment_generate_rather_than_guess` |
| A synonym finds the blueprint | `test_reservations_finds_it_through_canonical_vocabulary` |
| A contributed entry is found by the next project's own word | `test_a_different_project_s_word_still_finds_it` |
| An assembled part costs no model call | `test_the_blueprint_is_assembled_with_no_model_call_for_it` |
| A catalog edited after matching fails loudly | `test_an_entry_that_drifted_from_the_file_plan_fails_loudly` |
| A missing token never ships a placeholder | `test_a_missing_token_falls_back_instead_of_shipping_a_placeholder` |
| The library never contributes its own entries back | `test_the_assembled_package_is_skipped_by_contribute` |
| A build never replaces a seed | `test_a_build_never_replaces_a_seed` |
| A duplicate that is no better is discarded | `test_a_duplicate_that_is_no_better_is_discarded` |
| The id comes from the store, not the candidate | `test_the_id_is_assigned_by_the_store_not_by_the_candidate` |
| A generalisation that breaks the code is not added | `test_an_entry_that_does_not_re_verify_is_not_added` |
| One package's refusal never stops the rest | `test_one_package_s_refusal_never_stops_the_others` |
| An unknown area is proposed, never invented | `test_an_unknown_area_is_proposed_not_invented` |

Enforced in code, not only in prose: `assemble_package` re-checks file-plan equality *after*
matching, because *"a catalog edited after matching cannot quietly write somewhere else"*
(`assembler.py:139`). Generalisation output is discarded — not repaired — if the model returns
a different set of files or drops a `data-scio-id` (`generalize.py:217`, `:223`). And the
matcher's relay answer is scanned longest-id-first, because *"'feature-booking' is a prefix of
'feature-booking-twin', and a substring scan would confidently return the wrong one"*
(`matcher.py:220`).

## 5 · Dependencies

**Out:** `D → E` 84 (the largest edge in the graph), `D → B` 26, `D → C` 22.
**In:** `E → D` 23, `C → D` 9.

### Question 1 — is `D → B` (26) and `D → C` (22) a layering inversion?

**No. It is the matching design working as intended.** Four pieces of evidence.

**a. Every one of the 26 `D → B` edges points at a leaf.** They split cleanly:

| Target | Edges | Importers |
|---|---:|---|
| `layerb/vocabulary.py` — `canonical_name`, `singularize` | 17 | `categories.py`, `entry.py`, `identity.py`, `matcher.py` |
| `layerb/architecture.py` — `DesignTokens`, `Architecture` | 9 | `assembler.py`, `contribute.py` |

`vocabulary.py` imports `re` and `pydantic` and nothing else; `architecture.py` imports
`enum` and `pydantic` and nothing else. Neither references the library. These are shared
data and vocabulary modules that happen to live in `layerb/`, not Layer B's reasoning.
Layer A does the same thing — the Layer A document records it as *"the canonical vocabulary
is shared rather than duplicated"* — so this is an established pattern, not a new violation.

**b. The dependency is load-bearing and cannot be removed without losing the feature.**
The whole point of the contract is that "reservations" finds the booking blueprint. That
works only because `package_entity` canonicalises the word first (`matcher.py:110`,
`canonical_name(entity_of(package))`) and `entity_forms` canonicalises again before blanking
(`identity.py:111`). Cut the vocabulary edge and you get one entry per synonym — the exact
failure `categories.py:1` exists to prevent. `test_reservations_finds_it_through_canonical_vocabulary`
is the assertion that this edge does its job.

**c. All 22 `D → C` edges point at `layerc/plan.py`** — `BuildPackage`, `BuildPlan`,
`PackageKind`, and nothing else. `plan.py` imports only `.criteria`. There is no import
cycle: `layerc/service.py → library/matcher.py → layerc/plan.py → layerc/criteria.py` is
acyclic. `matcher.py` accounts for 13 of the 22, all of them type references on function
signatures that take a package.

**d. Control flows the other way.** The 9 `C → D` edges are `layerc/service.py` *calling*
`match_plan`, `apply_matches` and `default_store` (`service.py:76–83`). The library does not
reach into planning; planning reaches into the library and hands it a plan to look at. Same
with `E → D` (23): `orchestrate.py` calls `assemble_package`, `pipeline.py` calls
`contribute_build`.

By the index's own convention — *"an arrow means references, so it points opposite to data
flow"* — `D → B` reads exactly like `C → B` (66) and `B → A` (29): a layer referencing its
input. There is nothing to invert.

**Two caveats on the numbers themselves.** The `D → E` count of 84 is inflated: 6 of those
edges are `library/categories.py → builder/codegen.py::_normalise()`, and `categories.py`
imports nothing from `builder` — both modules define a private function called `_normalise`
and the extractor conflated them. The real `D → E` edges are the honest ones: the relay
(`generalize`, `matcher`), the build's own verifier and stamper (`assembler`, `reverify`), the
file plan, and `builder/result.py`'s result types. And `E → D` is partly an accounting
artifact too — 11 of the 23 are `pipeline.py`/`workspace.py` reaching for
`library/verification/`, the pglite harness, which is filed under Layer D only because of
where the directory sits.

## 6 · State

### Solid — carry forward unchanged

- **`Contract`.** Three sorted lists, a hash, and a subset-plus-equality test. It is small,
  it is total, and it is the reason the whole layer can claim determinism. The hardest thing
  here to rebuild correctly.
- **`entity_forms` / `_blank`.** Ugly, specific, and right — the `\b`-versus-`(?<![A-Za-z0-9])`
  comment (`identity.py:116`) records a bug class that would otherwise be rediscovered.
- **The refusal sequence in `contribute.py`.** Seven ordered steps (`contribute.py:9–15`),
  each with a reason recorded on the `Outcome`. Every path says why, and `contribute_build` swallows its own exceptions because
  *"contributing is a side-effect of a finished build. It must never be the reason a user's
  app fails to be delivered"* (`contribute.py:415`).
- **`reverify`.** Adapting to `widget`, an entity the entry has never seen, rather than back
  to the project's own — *"adapting `booking` code back to `booking` would pass even if
  generalization had done nothing, which is precisely the failure being looked for"*
  (`reverify.py:49`). Caught a real bug: `strip_package_tags` exists because
  re-verification found `data-scio-package` leaking into entries (`generalize.py:130`).
- **The model is used for rewriting only.** `generalize` applies the deterministic
  substitution first and discards the model's reply wholesale on any of three failures. Nothing
  a model says decides a match, a dedup, a "better", or an admission.
- **`unmet_requirements` (B116).** A pre-write text check for the symbols an entry imports,
  with a fall back to generating (`orchestrate.py:348`). *"knowing a component does
  not fit BEFORE dropping it in means the package can simply be generated instead, which is a
  working app rather than an honest report about a broken one"* (`assembler.py:82`).
- **Cost wiring.** ADR-0014's promise that "cost becomes predictable before the build" is
  real: `estimate.py:214` prices an assembled package at `$0.00` and `ASSEMBLE_SECONDS = 3`,
  and the composition reaches the user's spec gate.

### Deliberate, and easy to break by accident

**The category and the contract do different jobs and must stay apart.** *"A wrong category
costs a missed reuse; a wrong match ships the wrong code, which is why the two jobs are kept
apart"* (`categories.py:15`). Any proposal to score, embed or fuzzy-match trades an
explainable failure for an unexplainable one; ADR-0014 and ADR-0016 each rejected it in
so many words.

**Provisional entries are offerable.** ADR-0016 argues the review queue nobody empties. That
is a defensible call — but it is only defensible while somebody can *see* the queue, and today
nobody can (below).

### Wrong-shaped

- **Three of the four seed entries can never match anything.** `ui-button`, `ui-field` and
  `ui-empty-state` declare no `operations` and no `category`, so `effective_contract().empty`
  is `True` and `satisfied_by` short-circuits to `False`. Verified directly against
  `default_catalog()`. They are reachable only through `Catalog.by_layer`, which has no
  production caller anywhere in the repo. The library's real catalog is **one entry**.
- **Those three would also fail the library's own gate.** Running `review()` over them returns
  `rejected` with `['tested', 'instrumented']` on all three — no test file ships with them,
  and they render `.tsx` while declaring `element_ids: []`. The test that would have caught
  this skips them: `test_the_shipped_seed_entries_would_all_pass_their_own_gate`
  (`test_library.py:640`) begins `if entry.layer is not Layer.feature: continue`. The library
  does not meet the bar it sets.
- **The Postgres read path does not scale to being "the nave".** `PostgresCatalogStore.catalog()`
  is `SELECT payload FROM library_entry WHERE status <> 'rejected'` (`store.py:241`) — every
  entry, full JSON, into memory, on every match, filtered in Python afterwards. `contract_key`
  is written on insert and `library_entry_contract` is indexed (`store.py:150`, `:156`), and
  **nothing ever queries either**; `_existing_with_same_contract` (`contribute.py:299`) is a
  linear scan in Python over the whole catalog. The index exists for a query that was never
  written.
- **A failed assembly is terminal.** When `verify_instrumentation` fails inside
  `assemble_package`, the package returns `needs_look` (`assembler.py:170`) and
  `orchestrate.py:404` files it under `broken`. There is no fall back to generating — unlike
  the `unmet_requirements` path, which does exactly that. The two failure modes are the same
  shape ("this entry does not fit this app") and get opposite treatment.
- **`Quality.better_than` mixes two measurement worlds.** `evidence()` is a 5-tuple that
  includes `accessibility_score` and `lighthouse_score` alongside build-gate counts. Today
  every contributed entry has `scores_measured=False` and zeros there, so comparisons are
  homogeneous by accident. When B048 lands and some contributions carry real numbers, a
  Pareto comparison between a measured and an unmeasured entry becomes meaningless — and
  nothing in `better_than` knows the difference.
- **`library/verification/` is not the component library.** 681 lines of pglite harness filed
  under Layer D purely by directory. It is good code with a clear docstring; it belongs in
  `builder/`.

### Missing

- **The delivery build never teaches the library.** `contribute_build` is called from exactly
  one place — `pipeline.py:321`, inside `stream_full_build`, guarded by `if not shell_origin`.
  `stream_promotion` (`pipeline.py:353`), the path that delivers an app the user shaped in the
  design window (ADR-0017, B070), never calls it. So a user who goes preview → design →
  promote teaches the library nothing, and the promoted app is the one with the most human
  attention on it. ADR-0016 documents only one exclusion — *"A preview build (Level 2)
  contributes nothing"* — and says nothing about promotion. This reads as an oversight, though
  a non-trivial one to fix: `stream_promotion` loads a stored plan and has no `Architecture`
  in hand, which `_project_terms` needs.
- **The curation surface has no human in front of it.** Five endpoints exist on the engine and
  are unreachable from the product: no api proxy, no client method, no UI. ADR-0016's argument
  for provisional-but-offerable was *"keeps a person in the loop without making them the
  bottleneck"* — as built there is no person in the loop, only a status field nobody sees.
  Proposed categories accumulate in `ContributionReport.proposed_categories` with no route to
  a decision.
- **The concurrency guarantee is untested by default.** The row-lock in
  `PostgresCatalogStore.add` is the load-bearing claim of ADR-0016's id design, and
  `test_eight_concurrent_contributions_get_eight_different_ids` exists — behind
  `skipif(not DSN)`. Running the suite gives `3 passed, 6 skipped`. CI without `SCIO_CATALOG_DB`
  proves nothing about the one thing a file tree could not do.
- **No measure of coverage or of what matching missed.** Nothing records how many packages
  matched, how many nearly matched, or which operation set stopped a match. `matcher.py`
  records `considered` per package but nothing aggregates it, so no change to this layer can
  be shown to be an improvement. The best number available today is a test assertion:
  `test_the_report_says_how_much_came_from_the_library` pins the canonical booking demo at
  `"1 of 5 parts from the library, 4 generated"` — 20%, against a strategy that wants 80%.
- **`api/modules/reference/` is a routed 501.** Two endpoints, both throwing, with Prisma
  models (`ReferenceAsset`, `ReferenceEmbedding` with a pgvector column) already in the
  schema. It is phase 4.6 work that no roadmap line currently tracks.

### Obsolete

- **`gate.propose`** (`gate.py:257`). Exported from `library/__init__.py`, never called from
  anywhere. Its docstring and the module header still describe the world before ADR-0016:
  *"STUB for this slice: a candidate that clears the gate is reported as accepted, not written
  to the catalog"* (`gate.py:260`) and *"The contribution itself (writing the entry into the
  catalog) is stubbed in this slice"* (`gate.py:16`). `contribute.py` has done the real thing
  since B061. The function is dead and its docstring is now actively misleading.
- **`store.next_id`** (`store.py:418`) — no callers.
- **`CatalogEntry.adapted_paths` / `adapted_ids`** (`entry.py:262`, `:266`) — no callers.
- **`CatalogEntry.depends_on`** (`entry.py:182`) — declared, never read.
- **`Provides.canonical_entities()` and `Provides.capabilities`** — the matcher stopped
  consulting entities when ADR-0016 moved identity into the contract. `canonical_entities()`
  survives only as a test assertion (`test_library.py:78`); `capabilities` is written as `[]`
  by `contribute.py:253` and read by nothing.

## 7 · Open questions

**a. What is the library actually for, at one entry?** The economics in ADR-0014 and
`STRATEGY.md` ("~80% assembly of proven parts") assume a large catalog. The mechanism to grow
one is built and tested; what is not established is whether contributions from real builds
converge on reusable contracts or scatter into near-unique ones, because of the recall cost in
§3. That is measurable — count contract keys per category over a run of builds — and it should
be measured before more is invested here.

**b. Should assembly fall back to generation on a failed verify?** It would make the library
strictly safe to try, at the cost of hiding entry rot. The `unmet_requirements` path already
made the opposite trade in the same file. Pick one and apply it to both.

**c. Who curates, and where?** Either build the surface ADR-0016 assumes, or accept that
`provisional` is decoration and say so in the ADR.

**d. Do the three `ui` seeds have a future?** Nothing can match them and nothing can reach
them. Either the token/pattern layers get a matching mechanism of their own, or the entries
should go and `Layer` should shrink to what the matcher can use.

---

## Documentation drift found

**1. `docs/LIBRARY.md:45` — where matching happens.**

> The match happens **between Layer B and Layer C** — before the plan is built, not during the
> build.

Wrong on the second half. `match_plan` takes a `BuildPlan` and is called at
`layerc/service.py:76`, *after* `build_plan(arch)` (`:53`) and after every package's contract
has been assembled (`:64`). It has to be: `package_contract` needs `planned_files(package)`,
which needs packages. The spirit — before the *build* — is correct and is what makes the cost
estimate possible. The letter is not. The `library/matcher.py` docstring repeats the same
phrase at line 1.

**2. `docs/LIBRARY.md` "What an entry is" (lines 64–77) omits `requires`.**
`Requirement` and `CatalogEntry.requires` landed on 2026-08-22 (`e342cce`, B116, marked *done*
in `BACKLOG.md:167`); `LIBRARY.md` was last touched 2026-08-19 (`493cc41`). The doc still
describes the world where naming a package dependency was all an entry did — the exact
assumption B116 exists to correct. `requires` and `package_dependencies` should be in that
list.

**3. ADR-0014's match rule is no longer what the code does.**

> **Matching is strict and deterministic**: vetted entry, **same canonical entity**, every
> owned operation covered, and files exactly equal to the package's file plan.

The entity clause was reversed by ADR-0016 — *"The contract deliberately excludes the entity.
'Bookings' and 'appointments' produce identical contracts, which is exactly right"*
(`identity.py:24`). `candidates()` (`matcher.py:179`) filters on category and
`satisfied_by` only; there is no entity comparison anywhere in the matcher.
`test_a_different_project_s_word_still_finds_it` asserts the new behaviour. ADR-0014 is still
marked **Accepted** with no amendment note, and ADR-0016 never names it as superseded —
against `docs/decisions/README.md:8`, which says a reversing decision must mark the old one.
The honest fix is a "partially superseded by 0016" line on 0014.

**4. `docs/STRATEGY.md:69` — the contribute-back gate.**

> **Contribute-back needs a quality gate** — a newly generated component enters the library
> only after tests + **review**, or it pollutes the library and lowers every future build.

ADR-0016 explicitly rejected that: *"Contributed entries land in a review queue and are
invisible until approved. Rejected: it is the same as not growing."* As built, an entry enters
the catalog and is immediately offerable with no human review (`entry.py:209`, `offerable`
returns true for `provisional`). STRATEGY §E is a snapshot from before ADR-0016, not current
policy.

**5. `library/gate.py:16` and `:260` describe a stub that no longer exists.** See Obsolete,
above. The module docstring tells a reader that contribution is not implemented; it has been
since B061.

*Verified 2026-08-26 against the code, with `test_library.py` (47) and `test_contribute_back.py`
(27) passing — 74 total. `test_catalog_store_pg.py` runs 3 and skips 6 without a database.*
