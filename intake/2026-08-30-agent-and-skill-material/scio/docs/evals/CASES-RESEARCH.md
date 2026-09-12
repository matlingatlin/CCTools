# Eval cases executed · the research skills

**Date:** 2026-08-26. First execution of these cases.

Twenty-two named eval cases from three research-derived skills — `change-impact-analysis` (E1–E8),
`ears-requirements` (E1–E7) and `reflexion-conformance` (E1–E7). Fifty-three cases exist across six
skills and **none had ever been run.** Today's twenty-six ablations measured whether a skill changes
what a model *says*. These cases measure something else: whether a rule, applied to a real input,
gives the right answer.

Everything below was run against real artifacts: the 5,173-node code graph at
`docs/as-built/graph/graph.json` (built at hello-world `00408d3`), the 88 Python modules of
`apps/engine/src/scio_engine/`, and a live `booking` architecture derived through
`derive_architecture` → `build_plan` → `validate_plan`. Scratch scripts are under
`/tmp/claude-0/-home-user-hello-world/cbc9c7d7-c7ee-50d4-b71d-483bd4b8b525/scratchpad/`.

---

## Summary

| | `change-impact-analysis` | `ears-requirements` | `reflexion-conformance` | **total** |
|---|---|---|---|---|
| **RUNNABLE** | 7 | 4 | 6 | **17** |
| **BLOCKED** | 0 | 3 | 0 | **3** |
| **NOT A TEST** | 1 (E3) | 0 | 1 (E3) | **2** |

Among the 17 runnable:

| Outcome | Count | Which |
|---|---|---|
| **PASS** | 6 | CIA E2, E4, E7 · EARS E4, E7 · REFL E6 |
| **FAIL** | 10 | CIA E1, E5, E8 · EARS E2, E5 · REFL E1, E2, E4, E5, E7 |
| **INCONCLUSIVE** | 1 | CIA E6 |

**Three of the six passes are vacuous** — EARS E4, EARS E7 and REFL E6 pass because nothing in the
system today could have made them fail. Counted honestly, **three cases out of twenty-two produced a
pass that a change to the code could have turned into a failure**: CIA E2, CIA E4, CIA E7.

The headline results:

- **`reflexion-conformance` failed five of its six runnable cases against our own code.** Its E2 —
  *"source that maps to no architecture node must be reported, and reported as an invariant-1
  violation"* — is the inverted-polarity rule its ablation turned on. Run for real, the system
  returns `valid = True, issues = 0`. It does not merely mis-classify unmapped source; it never
  reads it.
- **`ears-requirements` cannot be run as specified.** Three of its seven cases (E1, E3, E6) address
  fields of a requirement object that does not exist anywhere in the codebase: of the six fields
  §2.3 names — `id`, `text`, `pattern`, `grounding`, `origin`, `satisfied_by` — the live `Criterion`
  model has exactly one, `text`. Two more (E4, E7) pass vacuously. **One case, E5, found a real
  defect.** The skill's own repo records the gap: `docs/next/LAYER-A-INTAKE.md:688` lists A-8 as a
  prerequisite *"for the `grounding` field the `ears-requirements` skill already specifies"*.
- **`change-impact-analysis` is the only one of the three whose cases mostly bite**, because a real
  impact-analysis implementation exists to point them at — `graphify affected`, not Scio's own code.
  Scio has no CIA. Its E8 produced the most useful measurement of the day: a predicted impact set
  with **25% recall against a real commit**, and a structural reason for the miss.

---

## Two notes on subject before the cases

**These cases mostly do not have a subject in Scio.** `change-impact-analysis` describes an impact
analysis Scio has not built; `reflexion-conformance` describes a conformance check Scio has not
built; `ears-requirements` describes a requirement object Scio has not built. Where a nearest real
subject exists I named it and ran the case against that, saying so. Where none exists I marked the
case BLOCKED rather than inventing one.

**One factual correction to the brief.** `graphify affected "<symbol>"` does exist —

```
  affected "X"             reverse traversal to find nodes impacted by X
    --relation R            edge relation to traverse in reverse (repeatable)
    --depth N               reverse traversal depth (default 2)
```

— and it is what makes the CIA cases runnable at all. It is *graphify's* impact analysis, not
Scio's. No result below should be read as a measurement of Scio's CIA, because Scio's CIA does not
exist.

---

## `change-impact-analysis`

Subjects: **(A)** `graphify affected` over `docs/as-built/graph/graph.json` — a real forward-closure
impact analysis over 5,173 nodes / 12,054 edges of hello-world; **(B)** Scio's own only
"what-does-this-change-touch" computation, `design/markings.py:resolve_batch` → `ResolvedBatch`.

### E1 · Tiering is present and named

> *Given a design or implementation of impact analysis, assert it returns **at least two tiers**
> with distinguishable names, not a flat set. A flat set fails.*

**Classification · RUNNABLE.** **Outcome · FAIL, on both subjects.**

Subject A, real output (`graphify affected "resolve_marking" --depth 2`, 39 rows, first six):

```
Affected nodes for resolve_marking()
Relations: calls, indirect_call, references, imports, imports_from, ...
Depth: 2
- main() [calls] apps/engine/scripts/verify_core.py:L105
- directed_regenerate() [calls] apps/engine/src/scio_engine/core/regenerate.py:L185
- resolve_batch() [calls] apps/engine/src/scio_engine/design/markings.py:L124
- .test_a_good_marking_resolves_exactly() [calls] apps/engine/tests/test_core_guardrails.py:L117
- .test_a_loop_instance_resolves_via_its_pattern() [calls] apps/engine/tests/test_core_guardrails.py:L125
- .test_an_id_missing_from_the_manifest_is_drift_not_a_guess() [calls] apps/engine/tests/test_core_guardrails.py:L103
```

One flat list. A depth-1 node and a depth-2 node are typographically identical; there is no
Certain / Likely / Possible, and nothing in the output says how far out a row was found. The tiering
is *available* — running `--depth 1` and `--depth 2` separately gives 13 and 38 rows — but the tool
does not return it, so a reader cannot tell the two apart.

Subject B, real output:

```
Scio's own 'what does this change touch' answer:
  ResolvedBatch.packages = ['pkg_feature_booking']
  ResolvedBatch fields   = ['outcomes', 'prompt']
  tiers                  = none — the model has one list
```

`ResolvedBatch.packages` is documented as *"The affected packages, in a stable order — these and no
others get rebuilt"* (`design/markings.py:98`). One tier, and the comment makes the flatness
load-bearing: a package outside that list is not rebuilt at all.

**This is a real failure and the case earned it.** The skill's §2.2 argument — that a flat set is
not a usable answer — is exactly what both subjects return.

### E2 · Depth is bounded and configurable

> *Assert a maximum-depth parameter exists and has a stated default. An unbounded transitive closure
> fails, and the failure message should cite the ~30% slicing result.*

**Classification · RUNNABLE.** **Outcome · PASS on subject A.**

`--depth N   reverse traversal depth (default 2)`. A stated default, exposed and tunable. §2.3's
other two knobs are half-present: `--relation R` is the dependency-type knob; there is **no**
minimum-importance flag, although every edge in the graph carries `weight` and `confidence_score`.
E2 only asserts depth, so it passes; §2.3 asks for all three and would not.

Subject B has no depth parameter because it has no walk — resolution is depth 0 by construction. It
passes E2 the way a system with no closure passes a bound on closures, which is not informative.

### E3 · Both perspectives present

> *Assert the impact set contains **both** graph-internal nodes (dependency analysis) **and** at
> least one traceability link outward — to a spec field, requirement id, package or file. One
> without the other fails.*

**Classification · NOT A TEST.** Ran it anyway; it passes.

Every row of `graphify affected` output carries a file path. Every `MarkingOutcome` carries
`package`, `file` and `line`. Both pass.

They could not have done otherwise. The outward link is a four-way disjunction whose last term is
**"file"**, and any impact analysis built on a code graph reports file paths — that is what a code
graph is made of. To fail E3 a system would have to return bare node identifiers with no location,
which no tool in this class does. The case as written cannot discriminate.

The distinction it was trying to draw is real and is lost by the disjunction: Arnold & Bohner's
traceability analysis means a link to **the requirement**, and *neither* subject has one. `NodeRef`
is `['kind', 'name']`. Tighten E3 to *"names a spec field or requirement id"* and both subjects fail
it, which is the answer §2.1 actually wants.

### E4 · Reverse attribution exists

> *Given a failure in the affected set, assert the system can name **which part of the change** is
> responsible. Forward-only fails (Chianti §2.4).*

**Classification · RUNNABLE.** **Outcome · PASS on subject A.**

Taking a test from E1's affected set and asking which change reaches it:

```
$ graphify path "test_it_touches_only_the_marked_package" "resolve_marking"
Shortest path (2 hops):
  .test_it_touches_only_the_marked_package() --calls [EXTRACTED]--> directed_regenerate() --calls [EXTRACTED]--> resolve_marking()
```

The chain is named, edge by edge, with the relation on each hop. Run once per changed symbol, this
is the affecting set for that test.

**Two qualifications the case does not make.** First, this is graphify's, not Scio's — Scio has no
reverse index. Second, Chianti's *affecting* set is a decomposition into **atomic changes**; a graph
path is a decomposition into **symbols**. Those coincide only when a change touches one symbol. The
case says "which part of the change", and a path answers "which symbol you edited reaches this",
which is weaker.

### E5 · No unearned number

> *Grep the produced text, docs, UI copy or commit messages for `95.8`, `85.7`, `99.9`, `3.95`,
> `52%` without an accompanying attribution clause naming the paper and its dataset. Any bare
> occurrence fails.*

**Classification · RUNNABLE** — it is a literal grep. **Outcome · FAIL, two occurrences, plus
four false positives the pattern itself produces.**

Twenty lines across `/home/user/scio`'s Markdown match. Eight are inside the skill file stating the
rule. Four are **false positives**: `LAYER-G-CROSS-CUTTING.md:385`, `:696` and
`tenant-isolation/SKILL.md:40`, `:339` all read `>99.999%` — Zanzibar's availability figure, an
unrelated paper — and the literal `99.9` in E5's pattern matches it. Seven of the remaining eight
name the paper, the dataset and the caveat. Two do not:

`docs/next/LAYER-B-UNDERSTANDING.md:16-17` —

> *"the biggest single finding — impact analysis — turns out to be a field with a 1993 founding
> paper, a 2004 tool with published precision numbers, a 2024 LLM system, and a 2026
> requirements-level result at 95.8% recall. None of it needed inventing."*

No paper named, no dataset named. A bare occurrence by the rule as written.

A commit message present in both repos —

> *"Chianti, CodePlan, ProReFiCIA at 95.8 percent recall."*

Names the paper; does not name the dataset. E5 requires **both**, so this fails too.

**Neither is a real over-claim, and a third of what the pattern matched is not the number at all.**
Both hits plainly attribute the figure to somebody else's work; the
honesty rule the case defends — do not sell ProReFiCIA's industrial result as ours — is not
breached. E5 is mechanical and it fires; whether either hit is a defect is a judgement a grep cannot
make. Recorded as FAIL because that is what the rule says, and flagged as the clearest example in
this document of a mechanical check that needs a human verdict on its output.

### E6 · Correct label before measurement

> *Assert the system calls its output **"may-impact"** or an equivalently hedged term until recall
> has been measured against real diffs.*

**Classification · RUNNABLE.** **Outcome · INCONCLUSIVE.**

The hedge is used where the mechanism is described:

```
docs/next/LAYER-B-UNDERSTANDING.md:184  **may-impact** — an over-approximation that is honest about being one.
docs/next/LAYER-B-UNDERSTANDING.md:219  | **Likely** | one edge out ... | may-impact, depth 1 |
docs/next/LAYER-B-UNDERSTANDING.md:723  ... B-1 ships as a **may-impact** analysis with an ...
```

It is absent where the feature is named:

```
docs/next/LAYER-F-DESIGN-WINDOW.md:427  ### 3.4 No impact analysis before code is written — product invariant #2
docs/next/LAYER-F-DESIGN-WINDOW.md:934  | **F-6** | **Impact analysis before generation, and a change report** | ...
```

Inconclusive rather than FAIL because **the assertion has no subject**: the case is about what the
system calls *its output*, and the system produces no output. `grep -rn "impact\|affected"` over
`apps/app/src` and `apps/website` returns two hits, both in `ErrorBoundary.tsx` and unrelated. There
is no UI copy to be wrong. A backlog item title is not an output, and a product invariant is a
requirement on a feature that does not exist.

### E7 · Over-approximation smoke test

> *Construct a graph where one entity is referenced by every operation (a `user` table, typically).
> Assert that editing an unrelated field does **not** return the whole graph. This is Nx's
> documented "all projects too often affected" failure, reproduced deliberately.*

**Classification · RUNNABLE.** **Outcome · PASS, with a measurement worth keeping.**

The hubs of hello-world, by `graphify god-nodes`: `ProviderRegistry` 109 edges, `BuildPackage` 106,
`Architecture` 76. Affected-set size against 5,173 total nodes (3,628 of them code):

| Seed | d=1 | d=2 | d=3 | d=4 | d=6 | d=12 | share of code nodes at saturation |
|---|---|---|---|---|---|---|---|
| `Architecture` | 72 | 229 | 299 | 303 | 303 | 303 | **8.4%** (35 of 337 code files) |
| `ProviderRegistry` | 165 | 266 | 270 | 270 | 270 | 270 | **7.4%** |
| `BuildPackage` | — | — | — | — | 331 | 331 | **9.1%** |
| `DesignTokens` (an unrelated leaf) | 8 | 29 | 118 | 182 | — | — | 5.0% |
| `resolve_marking` | 13 | 38 | 44 | 48 | — | — | 1.3% |

The closure **saturates by depth 4** and never grows again. Editing the single most connected symbol
in the repository, with the depth bound removed entirely, reaches 9.1% of code nodes. Nx's failure
does not reproduce here.

**This also measures the skill's own caveat and confirms it.** §3 says the ~30% static-slicing figure
*"is a warning about unbounded closures in general, not a prediction of our tier sizes. Our graph is
coarser and much smaller than a statement-level PDG."* At 8–9% against 30%, the caveat was right and
the headline was not transferable. The case tests the paper's claim against our graph, and our graph
disagrees — which is the correct use of a borrowed number.

### E8 · Backward traceability

> *Given an impact set and the diff the change actually produced, assert that **every changed line
> maps to a named element of the set**. Unmapped lines are the finding, one per hunk.*

**Classification · RUNNABLE.** **Outcome · FAIL.**

Real change: hello-world `55bde65` *"feat: a directed change says whether the app still compiles"* —
a typecheck added to `apply_change`, ten files, 214 insertions.

```
$ git show --stat --format="" 55bde65
 apps/api/src/engine/engine.client.ts          |  4 ++
 apps/api/src/modules/design/design.service.ts | 16 ++++++++
 apps/api/test/design.e2e.spec.ts              | 36 +++++++++++++++++
 apps/app/src/pages/DesignPage.tsx             | 17 ++++++++
 apps/app/src/pages/design.test.tsx            | 33 ++++++++++++++++
 apps/engine/src/scio_engine/design/change.py  | 22 +++++++++++
 apps/engine/tests/test_design_change.py       | 57 +++++++++++++++++++++++++++
 packages/shared/src/dtos.ts                   |  5 +++
 (+ docs/BACKLOG.md, docs/CHANGELOG.md)
```

Predicted impact set, seeded on the edited symbol (`apply_change` is ambiguous across two files, so
the node id was used — the tool refuses to guess, which is correct):

```
$ graphify affected "apps_engine_src_scio_engine_design_change_apply_change" --depth 3
  depth=1 nodes=3   depth=2 nodes=9   depth=3 nodes=9   depth=4 nodes=9
  apps/engine/src/scio_engine/design/__init__.py
  apps/engine/src/scio_engine/main.py
  apps/engine/tests/test_api.py
  apps/engine/tests/test_design_change.py
  apps/engine/tests/test_design_restore.py
  apps/engine/tests/test_layerb_service.py
  apps/engine/tests/test_layerc_service.py
  apps/engine/tests/test_sse_heartbeat.py
```

**Recall: 2 of 8 code files** — the seed's own `change.py`, and `tests/test_design_change.py`. The
six missed files are every file outside Python: the api client, the api service, its e2e spec, the
app page, its test, and the shared DTOs.

The reason is structural, and measurable:

```
edges with both endpoints in a source file: 11268
python<->typescript edges: 0
```

**Zero of 11,268 edges cross the language boundary.** The change propagated through a serialised
contract — `DesignChangeResult` → JSON → `dtos.ts` → `DesignPage.tsx` — and the graph has no edge of
that kind, so no depth setting would ever have found it. Six unmapped files, 111 unmapped lines.

Backward traceability in the sense E8 means — every changed *line* mapped to a set element — could
not be attempted, because no mechanism produces that mapping. The skill says so itself: *"what is
missing is the mapping back."* E8 asserts a capability the skill admits does not exist; running it
confirms the admission and adds the recall figure, which the skill did not have.

---

## `ears-requirements`

Subject: the **23 acceptance criteria** a real `booking` spec produces, obtained by running the
actual pipeline — `booking_spec()` (`apps/engine/tests/test_builder_pipeline.py:36`) →
`derive_architecture` → `build_plan` — plus the `Criterion` model in `layerc/criteria.py` and the
11-node architecture behind them. This is Scio's nearest thing to a requirement set, and §6 of the
skill says explicitly that it is the intended target: *"the same patterns as a package's acceptance
criteria."*

**The blocking fact for three of the seven cases.** Of the six fields §2.3 says a requirement
carries, the live object has one:

```
Criterion model fields: ['observed_by', 'produced_by', 'script', 'text']
EARS object fields required by skill §2.3: id, text, pattern, grounding, origin, satisfied_by
present: ['text']
```

No `id`, no `pattern`, no `grounding`, no `origin`, no `satisfied_by`. The repo already knows:
`docs/next/LAYER-A-INTAKE.md:688` files A-8 *"Requirement identity"* as a prerequisite *"for the
`grounding` field the `ears-requirements` skill already specifies."*

### E1 · Pattern conformance

> *Given a set of generated requirements, assert every one matches the grammar of its declared
> pattern. A sentence declaring `event_driven` that does not begin with "When" fails.*

**Classification · BLOCKED.** No requirement declares a pattern, because no `pattern` field exists.

```
E1  criteria declaring which pattern they are: 0/23 (no `pattern` field exists)
E1  criteria opening with an EARS keyword (When/While/If…then/Where): 0/23
```

**Would the case be good once the field exists? Half of it.** The example E1 gives —
*"declaring `event_driven` that does not begin with When"* — is a two-line regex and is fully
mechanical. But E1 says *"matches the grammar of its declared pattern"*, and the grammar is
`WHEN <trigger>, the <system> SHALL <response>`. Checking the keyword is mechanical; checking that
what follows `When` is a **trigger** rather than a state, and that what follows `SHALL` is a
**response**, is not. Those are the parts that make an EARS sentence well-formed, and a regex cannot
see them. E1 as written mixes a mechanical check and a judged one under one name.

### E2 · One shall

> *Assert exactly one `shall` per requirement. Two means two requirements.*

**Classification · RUNNABLE** — a word count. **Outcome · FAIL, 23/23.**

```
E2  criteria containing exactly one 'shall': 0/23; containing any 'shall': 0/23
```

The finding is not that the checker is wrong; it is that **EARS has never been applied to anything
in this repository.** Every one of the 23 criteria is a declarative present-tense sentence — *"Every
table exists with its columns, keys and timestamps."*, *"Inputs are validated server-side and
invalid input is rejected clearly."* Recorded as FAIL because a conformance check on a non-conformant
corpus fails; the useful reading is that E2 measures adoption, and adoption is zero.

E2 is the one case in this skill that is unambiguously mechanical, and it is also the one that tells
you least: `count("shall") == 1` says nothing about whether the sentence is a good requirement. The
skill's own §3 names that failure mode — *"the syntax makes bad requirements look rigorous"* — and
E2 is a check that would be satisfied by exactly such a sentence.

### E3 · Grounding coverage

> *Assert every requirement names at least one spec field. A requirement with empty grounding is an
> unsupported claim in a contract the user is about to sign — it must fail, not warn.*

**Classification · BLOCKED.** There is no `grounding` field.

```
E3  criteria with a non-empty produced_by (planned FILES, not spec fields): 17/23
E3  criteria with any spec-field grounding: 0/23 — the field does not exist
```

The nearest analogue is `source_field` on the architecture objects. Running it on the live booking
architecture shows why substituting it would have produced a false pass:

```
  table booking                source_field='entities'
  table table                  source_field='entities'
  table guest                  source_field='entities'
  operation create_booking     source_field='key_actions'
  operation cancel_booking     source_field='key_actions'
  screen /                     source_field='key_actions'
```

`source_field` is a **class-level default** (`architecture.py:50`, `:110`, `:119`) — every table
says `entities`, every operation says `key_actions`. It names the *kind* of spec field a node came
from, never *which item in it*. It is non-empty on every node by construction, so an E3-shaped check
over it can never fail, and it cannot get you from `table guest` back to the thing the user said.
One node kind does default to empty — `Connector.source_field: str = ""` (`architecture.py:137`) —
so the only node type that could fail such a check fails it always.

**Would E3 be good once `grounding` exists? Yes, and it is genuinely mechanical** — non-empty, and
each named field resolves to a real key of `AppSpec`. It is the strongest of this skill's seven
cases, and it is not runnable today.

### E4 · Canonical vocabulary

> *Assert the entity nouns in each sentence are canonical terms (`booking`, not `reservation`).
> Round the sentence through `vocabulary.canonical_name` and compare.*

**Classification · RUNNABLE.** **Outcome · PASS — and vacuous.**

```
E4  entity nouns present in the 23 criteria, canonicalised:
   'operation'  -> 'operation'      'records' -> 'record'
   'screen'     -> 'screen'         'table'   -> 'table'
   'tables'     -> 'table'          'user'    -> 'user'
   non-canonical nouns found: 0
```

`canonical_name` does discriminate — it is not a no-op:

```
'reservation'  -> 'booking'      'customer' -> 'guest'
'appointment'  -> 'booking'      'member'   -> 'user'
'account'      -> 'user'         'photo'    -> 'image'
```

But **no synonym can reach these sentences.** The fixed text is written by Scio's own code in
`decompose.py`; the variable parts are interpolations of `op.name`, `op.description` and
`op.entity`, which come from an `Architecture` whose table names are already *"canonical, singular"*
(`architecture.py:44`) because `Vocabulary` canonicalised them upstream. E4 re-checks an invariant
that is enforced at construction. It passes because it cannot fail.

**And its stated method is not mechanical.** *"Round the sentence through `canonical_name` and
compare"* — done literally, over every word of the 23 criteria, it flags 29 words:

```
['blocks','colours','columns','defaults','definitions','errors','executes','exists','families',
 'headers','inputs','keys','loads','migrations','passes','persists','policies','providers',
 'reaches','records','renders','screens','secrets','tables','timestamps','tokens','typefaces',
 'variables','works']

'renders' -> 'render'   'loads' -> 'load'   'passes' -> 'pass'   'blocks' -> 'block'
```

`canonical_name` has no notion of part of speech; it singularises verbs as happily as nouns. E4
depends on first identifying *the entity nouns*, which needs a parser or a person. As specified,
it is a check with a hand-waved first step.

### E5 · No design in the response clause

> *Assert the response names an observable behaviour, not an implementation. Heuristic: reject
> responses containing a library, vendor or file name. Imperfect; it catches the common case.*

**Classification · RUNNABLE.** **Outcome · FAIL, 2 of 23 — and this is the one case in this skill
that found something real.**

```
E5  text naming a library/vendor/file:
   (pkg_design_tokens) Tokens are defined once and consumed by the Tailwind config.
       vendor=['Tailwind']
   (pkg_design_tokens) Typefaces load via next/font, not an @import or <link> to a font CDN
                       — a third-party font request blocks the first paint.
       vendor=['CDN', 'next/font']
   total 2/23
```

Both are `decompose.py` literals (`:381`, `:396`) and both are `Observability.validation` criteria —
they gate a real build. They name a library in the response clause, which is what E5 forbids.

**The finding needs a judge, and the case says so.** Scio's stack is fixed by the playbook: Next.js
and Tailwind are not an implementation choice a criterion is smuggling in, they are the environment.
*"Typefaces load via `next/font`"* is arguably the only way to state that behaviour observably, and
the criterion even carries its own reason — *"a third-party font request blocks the first paint"* —
which is the observable behaviour E5 wants. A reviewer might rewrite it as *"no font is requested
from a third-party origin"*, or might keep it. The heuristic fires correctly; the verdict is not
mechanical. The skill labels it *"imperfect"*, which is honest, and means E5 can be a report and
never a gate.

### E6 · Bidirectional coverage

> *Assert (a) every requirement has at least one `satisfied_by` node, and (b) every architecture
> node traces to a requirement id or carries `origin = assumption` or `origin = necessity`.*

**Classification · BLOCKED, both directions.**

```
(a) requirement -> satisfied_by node : field absent, 23/23 unknowable
(b) architecture node -> requirement id : NodeRef fields = ['kind','name'] — no requirement id, no origin
```

Direction (b) has a partial analogue that does run. `_check_coverage` (`layerc/validate.py:42`)
asserts every architecture node is owned by some package:

```
$ validate_plan(plan, arch)
validate_plan -> valid = True   violations = 5   (all severity=warning, all criterion_observable)
```

Zero `node_covered` violations — all 11 architecture nodes are built by some package. But that is
**node → package**, not **node → requirement**. It answers "was it built", not "was it asked for",
and (b) is the half that catches *"something was built and not asked for"*. Nothing in the system
answers that today.

### E7 · Readability is preserved

> *Assert the narrative shown at the spec gate is prose, not a rendered SHALL list. This eval exists
> because the most likely way to get EARS wrong here is to succeed at it and ship a worse product.*

**Classification · RUNNABLE.** **Outcome · PASS — and vacuous today.**

`layerb/whole.py:22`, the prompt that produces the spec-gate narrative:

```
- Write 2-4 short paragraphs of plain prose, addressed to the user as "you". \
No headings, no bullet lists, no preamble.
- This is what the user will approve as their project's contract, so it must be \
accurate before it is elegant.
```

Prose is mandated at the point of generation. It passes — but nothing in the system produces a SHALL
list, so there is no rendered list for the gate to show by mistake. E7 is a regression guard against
a failure mode that becomes possible only once EARS is adopted, and it will be a good one then. Its
subject is also a *human* judgement — "is this prose, or is it a list wearing paragraphs" — that
happens to be decidable here only because the prompt states the rule literally.

---

## `reflexion-conformance`

Subject: the real conformance-shaped machinery in hello-world —
`core/manifest_builder.py` (the extracted source model), `core/verifier.py`
(`verify_instrumentation`, 273 lines), `core/regenerate.py` (`verify_isolation`),
`layerc/validate.py` (`validate_plan`), and the seven architecture node kinds in
`layerc/decompose.py:architecture_nodes`.

There is **no architecture-conformance check** in the system: `grep -rn
"convergence\|divergence\|absence\|reflexion\|unmapped\|conformance" apps/engine/src apps/api/src
packages` returns four hits, none of them a conformance implementation. Every case below was run
against the nearest real check and the substitution is named each time.

### E1 · Three outcomes, not two

> *Assert the conformance result distinguishes convergence, divergence and absence. A boolean, or a
> list of "violations" that merges divergence and absence, fails.*

**Classification · RUNNABLE.** **Outcome · FAIL, on both real checks.**

```python
class InstrumentationReport(BaseModel):     # core/verifier.py:41
    valid: bool
    issues: list[InstrumentationIssue] = Field(default_factory=list)
    element_count: int = 0

class PlanValidation(BaseModel):            # layerc/validate.py:34
    valid: bool
    violations: list[PlanViolation] = Field(default_factory=list)
```

Both are exactly the shape E1 forbids: **a boolean plus one flat list.** Convergence is not reported
at all — `element_count` is a raw integer, so no caller can name which elements converged, which is
the evidence §2.3 says *"the reveal is supposed to show and currently does not."*

### E2 · Unmapped source is reported

> *Construct generated source containing a component that maps to no architecture node. Assert it is
> reported, and reported as an invariant-1 violation rather than folded into "divergence".*

**Classification · RUNNABLE** — the case tells you how to construct the input.
**Outcome · FAIL, and this is the most consequential result in the document.**

Constructed exactly as specified: two instrumented components, one (`Booking.tsx`) owned by
`pkg_feature_booking`, one (`Rogue.tsx`, carrying `data-scio-id="promo-banner"`
`data-scio-package="pkg_marketing"`) belonging to no package in the plan.

```
E2  does the check see Rogue.tsx (source that maps to no architecture node)?
    verify_instrumentation -> valid = True issues = 0
    -> 'promo-banner' mentioned anywhere? False
```

**Not mis-classified — invisible.** `verify_instrumentation` iterates `manifest.all_files()`
(`verifier.py:112`), which is *"the file list per package"*. Source outside the plan is never
opened, so it cannot be reported by any rule.

The second place it could have been caught does not catch it either. `verify_isolation`
(`regenerate.py:69`) is documented as *"Compare hashes: anything changed outside the target package
is a violation"*, but its loop is:

```python
for relative, old_hash in before.items():
```

`before` is the pre-change hash of tracked files. **A file that did not exist before was never
hashed, so it is never compared, and a new unowned file is not a violation.** The isolation proof
proves that owned files did not change; it does not prove that nothing else appeared.

This is the rule whose polarity the ablation turned on — the control said *do not block on code the
architecture never mentions*, the skill said that is the one thing that blocks. Run against the real
system, the system does neither: it does not see it. The skill is right that this is the important
case and right that a boolean cannot express it; what the case reveals is that our implementation
never gets as far as needing to express it.

### E3 · Source model is extracted, never authored

> *Assert the source model's provenance field says it was scanned from the artifacts. A hand-written
> or model-written source model fails — that is the drift the technique exists to prevent.*

**Classification · NOT A TEST.** Ran it; it passes, and it would also pass on the input it is meant
to reject.

```
E3  Manifest.generated_from = 'source-scan'
E3  hand-authored Manifest().generated_from = 'source'   <- the DEFAULT, nothing checks it
E3  elements found by the scan: ['booking-root', 'booking-submit']
```

The underlying property is **true**: `build_manifest` really does scan the files, and
`manifest_builder.py:3` states the principle — *"a hand-written manifest drifts from the code, and
the drift is silent. So the manifest is an artifact of the build."*

But the *check* E3 specifies is a self-report. `generated_from: str = "source"` is a plain field
with a default (`instrumentation.py:64`). A `Manifest` typed by hand, or emitted by a model,
arrives carrying `generated_from = "source"` — a string that says it was scanned from the
artifacts — and no validator, no constructor guard and no test compares it against anything. Asking
an object whether it was extracted is not evidence that it was extracted.

A version of E3 that could fail: **re-scan the artifacts and assert the result is byte-identical to
the stored source model.** That is a real check, it is fully mechanical, and `build_manifest` is
deterministic enough to support it today.

### E4 · Extraction limits are stated

> *Assert the extractor publishes its known limits (as `manifest_builder.KNOWN_LIMITS` does) and
> that a verifier exists to catch violations of the assumptions those limits depend on.*

**Classification · RUNNABLE.** **Outcome · FAIL on the second clause.**

First clause passes. `KNOWN_LIMITS` is published verbatim:

```
Textual scanning does not see:
- ids built by string concatenation outside a template literal
- ids passed down as props from another file
- attributes assembled via spread ({...props})
The playbook forbids all three; the verifier is what catches a violation.
```

Second clause fails. The final sentence is a claim, so I tested it — one file per documented limit,
plus one legitimate element so the "nothing is instrumented at all" rule would not fire:

```
id passed down as a prop:
   manifest elements = ['ok']   patterns = []
   verifier valid = True, issues = []
id built by concatenation outside a template literal:
   manifest elements = ['ok']   patterns = []
   verifier valid = True, issues = []
attributes assembled via spread:
   manifest elements = ['ok']   patterns = []
   verifier valid = True, issues = []
```

**All three pass clean.** The verifier catches none of the three violations its own limits document
says it catches. The reason is structural: `verifier.py:20-26` imports `_ID_LITERAL`,
`_ID_TEMPLATE`, `SOURCE_SUFFIXES` and `_template_to_pattern` *from the manifest builder*. The
enforcer and the extractor share one pair of regexes, so the enforcer is blind in exactly the places
the extractor is blind. A check that inherits its subject's blind spots cannot be that subject's
guard.

This is the skill's own §3 assumption 1 — *"the source model is only as good as playbook
compliance"* — with the one mitigation it offered removed. The honest statement is: the playbook
forbids all three, and **nothing verifies that the playbook was followed.**

### E5 · Divergence escalates, absence blocks, unmapped blocks

> *Assert the three outcomes have *different* consequences. Identical handling means the distinction
> was decorative.*

**Classification · RUNNABLE.** **Outcome · FAIL.**

The two outcomes the system does distinguish, each triggered for real:

```
ABSENCE  (manifest has it, code does not): rule=manifest_consistent  severity=error  valid=False
UNMAPPED (code has it, manifest does not): rule=manifest_complete    severity=error  valid=False
```

Different rule names, different messages, **identical consequence**: both are `Severity.error`, both
set `valid = False`, and `raise_for_status` (`verifier.py:52`) raises on either without
distinguishing them. Per the case's own wording, the distinction is decorative.

There is one place in the system where the consequences genuinely differ, and it is worth crediting:
`layerc/validate.py` returned `valid = True` alongside five `criterion_observable` warnings on the
live plan, so an unobservable criterion is recorded and does not block. That is the escalate-versus-
block distinction E5 wants — implemented for observability, not for conformance.

### E6 · No correctness claim

> *Grep the produced text, UI copy and docs for phrasing that turns structural conformance into a
> behavioural guarantee ("verified correct", "matches the approved design" without qualification).
> Any occurrence fails.*

**Classification · RUNNABLE.** **Outcome · PASS — and vacuous.**

```
### hello-world (product code + UI copy) ###
(no matches)

### scio docs+skills ###
./docs/evals/reflexion-conformance-ablation.md:48  ... should never phrase a clean run as "verified correct."
./.claude/skills/reflexion-conformance/SKILL.md:98  | "This proves generated code matches the approved architecture" | **Not supported.** ...
```

The only occurrences are the prohibition stating itself. Zero in product code, zero in UI copy, zero
in the layer documents.

Vacuous for the same reason CIA E6 was inconclusive: **the surface where the violation would appear
does not exist.** There is no conformance gate, so there is no clean run to phrase, so there is
nothing to over-claim about. E6 becomes a real check the day the gate ships and not before.

### E7 · Mapping completeness

> *Assert every architecture node kind has a mapping rule to source. A node kind with no mapping is
> invisible to the check and will silently always converge.*

**Classification · RUNNABLE.** **Outcome · FAIL, with a named instance.**

`architecture_nodes` defines seven kinds: `table`, `operation`, `screen`, `connector`, `auth`,
`tokens`, `security`. `planned_files` (`builder/file_plan.py:43`) is the only mapping from
architecture to source paths — and it branches on **`PackageKind`, not node kind.** Run on the live
booking plan:

```
pkg_foundation  (kind=foundation)
   planned files: ['app/layout.tsx', 'app/page.tsx', 'components/site-header.tsx', 'lib/supabase.ts']
   slice nodes  : ["kind='security' name='security_posture'", "kind='screen' name='/'"]

pkg_schema  (kind=schema)
   planned files: ['supabase/migrations/0001_init.sql', 'types/database.ts']
   slice nodes  : ["kind='table' name='booking'", "kind='table' name='table'", "kind='table' name='guest'"]

pkg_feature_booking  (kind=feature)
   planned files: ['app/actions/booking.ts', 'app/booking/new/page.tsx', ..., 'tests/booking.test.ts']
   slice nodes  : ["kind='operation' name='create_booking'", "kind='operation' name='cancel_booking'", ...]
```

| Node kind | Mapping rule to source | Verdict |
|---|---|---|
| `screen` | `_route_to_page(node.name)` — per node | ✅ |
| `auth` | `lib/auth.ts` — singleton kind, so effectively per node | ✅ |
| `tokens` | `app/globals.css`, `tailwind.config.ts` — singleton | ✅ |
| `connector` | `lib/connectors/{name}.ts` — one connector per package | ✅ |
| `table` | 3 nodes → one package's 2 files. No per-node rule | ⚠️ package granularity only |
| `operation` | 2 nodes → one package's 8 files. No per-node rule | ⚠️ package granularity only |
| `security` | **none** | ❌ |

`security:security_posture` sits in `pkg_foundation`, whose planned files are `layout.tsx`,
`page.tsx`, `site-header.tsx` and `lib/supabase.ts` — **not one of which is a security artifact.**
There is no rule that maps a security node to any source file, which is precisely E7's predicted
consequence: invisible to the check, silently always converging.

The skill's §3 assumption 4 anticipated the adjacent problem — *"a reflexion model would report that
a table exists and a policy file exists. It would not report that the policy is `USING (true)`."*
The measured situation is a step worse: at Layer C there is no policy file in the mapping at all.

---

## Are these cases mechanical, or do they need a judge?

Every case in all three skills is written in the imperative of a deterministic check — *"assert"*,
*"grep"*, *"construct"*. Running them, **nine of the twenty-two are decidable by a script
without a person reading the output — and two of those nine only once a missing field exists.**

| | Cases | |
|---|---|---|
| **Fully mechanical** — a script decides pass/fail | CIA E1, E2, E4 · EARS E2, E3\*, E6\* · REFL E1, E4, E5 | 9 |
| **Mechanical shell, judged verdict** — the check fires deterministically; whether a hit is a defect is a human call | CIA E5, E6, E7, E8 · EARS E1, E5 · REFL E2, E7 | 8 |
| **Needs a judge** — no deterministic form exists | EARS E4, E7 · REFL E6 | 3 |
| **Unfalsifiable as written** | CIA E3 · REFL E3 | 2 |

\* EARS E3 and E6 are mechanical *once the `grounding` / `satisfied_by` fields exist*. Today: seven.

The boundary runs through the middle of individual cases, not between them, and that is the finding
that matters:

- **EARS E1** bundles two checks under one name. *"A sentence declaring `event_driven` that does not
  begin with When fails"* is a regex. *"Matches the grammar of its declared pattern"* requires
  deciding that what follows `When` is a **trigger** and what follows `SHALL` is a **response** —
  which is the entire content of an EARS sentence being well-formed, and is not decidable by
  pattern. **This is the question the brief asked.** The answer: E1–E6 are described as mechanical
  checks over a requirement object, and E2, E3 and E6 genuinely are; E1 and E4 are not; E5 is a
  mechanical filter with a judged verdict. So the skill **can** be measured — but only three of its
  six named "mechanical" cases can gate, and none of the three is runnable until the requirement
  object exists.

- **EARS E4** is the sharpest example. *"Round the sentence through `canonical_name` and compare"*
  reads mechanical and is not: applied literally it flags `renders`, `loads`, `passes` and `blocks`,
  because `canonical_name` singularises without knowing a noun from a verb. The check's first step —
  *identify the entity nouns* — is doing the work and is not specified.

- **CIA E5 and REFL E6** are greps, and greps always fire mechanically. Both need a person to read
  the hit: *"an accompanying attribution clause naming the paper and its dataset"* and *"without
  qualification"* are not regex predicates. CIA E5's two hits are, on reading, both harmless.

- **REFL E2 and CIA E7** are the two best-designed cases in the set, and the reason is the same in
  both: **they name the input to build.** *"Construct generated source containing a component that
  maps to no architecture node"* and *"construct a graph where one entity is referenced by every
  operation"* remove the ambiguity about what is being tested. Both ran first time, both produced a
  quotable number or verdict, and one of them found the most serious defect in this document.

**What follows for how these cases should be used.** A case needing a human judge is not worthless —
EARS E5's two hits are worth a reviewer's minute — **but it cannot be a gate**, and none of the
three skills says which of its cases can be. Each skill presents its Eval section as a uniform list
of *"runnable cases"* with no distinction between *fail the build*, *raise a finding*, and *ask
someone*. That distinction is the same three-way split `reflexion-conformance` §2.3 argues for in
its own subject matter — block, escalate, report — and none of the three skills applies it to its
own evals.

---

## What the cases reveal about the skills that wrote them

**1 · A skill that describes a system nobody has built writes specifications, not tests.**
Four cases open in the literal conditional — *"Given a design or implementation of impact
analysis…"*, *"Given a failure in the affected set…"*, *"Given an impact set and the diff…"*,
*"Given a set of generated requirements…"* — and **eighteen of the twenty-two presuppose an artifact
Scio has not built**: an impact analysis (CIA E1–E4, E6–E8), a requirement object (EARS E1–E6), a
conformance check (REFL E1–E3, E5, E7). Only four — CIA E5, EARS E7, REFL E4, REFL E6 — address
something that exists today. Three cases are BLOCKED outright on a single missing object: EARS §2.3's requirement, of whose six fields the live `Criterion` has one. The cases read as
tests and behave as a design document — a statement of what the thing should do when it exists.
That is a legitimate artifact. It is not a measurement, and labelling it *"Runnable cases. Each
states the expected outcome so the skill can be measured rather than believed"* (CIA §4) overstates
it.

**2 · Both NOT A TEST cases are self-report checks, and that is a hazard specific to research
skills.** CIA E3 asks whether the impact set *names* a file. REFL E3 asks whether the source model
*says* it was scanned. Neither asks whether the thing is true. A paper describes properties of an
artifact, and the cheapest way to turn a described property into an assertion is to have the
artifact assert it about itself — which is how `generated_from: str = "source"` ends up as the
evidence that a manifest was extracted, when it is a defaulted string no validator reads. The
replacement for both is the same move: **check the property, not the claim.** Re-scan and diff for
REFL E3; require a spec-field or requirement id, not "or a file", for CIA E3.

**3 · The Limits sections govern the *sources* and leave the *evals* ungoverned.** CIA §3 said
plainly that the ~30% static-slicing figure was *"a warning about unbounded closures in general, not
a prediction of our tier sizes"* — and measurement agrees: an unbounded closure from the most
connected symbol in hello-world reaches **8.4–9.1% of code nodes**, not 30%. The honesty rule
worked. But no Limits section anywhere in the three skills says *this case cannot fail*, *this case
has no subject*, or *this case needs a human*. §3 disciplines what the skill may claim about its
paper; nothing disciplines what the skill may claim about its own evals, and that is where two of
the twenty-two went wrong.

**4 · `reflexion-conformance` was right and our code is wrong — which is the best outcome an eval
can produce, and the opposite of what a failing score usually means.** Five of six runnable cases
failed. Not one failure was the skill misapplying its paper:

- E1 — our conformance results are `valid: bool` + a flat list, which the paper's three-way answer
  exists to replace.
- E2 — source that maps to nothing is not mis-classified, it is **never read**: `valid = True,
  issues = 0`, and `verify_isolation`'s `for relative, old_hash in before.items()` cannot see a file
  that did not exist before.
- E4 — `KNOWN_LIMITS` ends *"the verifier is what catches a violation"*, and the verifier catches
  none of the three, because it imports the extractor's own regexes and inherits its blind spots.
- E5 — absence and unmapped both return `severity=error`, `valid=False`.
- E7 — the `security` node kind maps to no source artifact at all.

The skill's ablation showed it inverting an outcome on a question. The cases show it identifying
five real defects in code that predates it. That is a stronger result than the ablation, and it
argues these cases belong in `docs/BACKLOG.md`, not in CI.

**5 · `ears-requirements` now has a measured value, and it is one finding.** Its ablation was a
double null and closed by saying the substance *"is reachable by running the checks against a real
requirement set — which is an eval of the rules, not an ablation of the skill."* The checks have now
been run against the only real requirement-shaped set that exists. Three cases had no subject, two
passed vacuously, one failed for want of adoption, and **one — E5 — found two live gating criteria
that name a library in their response clause**, and needs a reviewer to say whether that is a defect
given a fixed stack. The skill's honest position is stronger than its Eval section implies: E3 is an
excellent mechanical check and is blocked on A-8, and saying so is more useful than listing seven
cases as if they were equally ready.

**6 · The one unsupported claim I found is not a number, and no honesty rule caught it.** All three
Limits sections handle their borrowed figures correctly — every occurrence of `95.8`, `85.7`,
`3.95`, `52%` inside a `SKILL.md` carries its paper and its dataset, and CIA §3 states outright that
ProReFiCIA's numbers are *"a target to aim at, never a claim to repeat about our system"*. The claim
that failed was prose: *"the verifier is what catches a violation."* It is hello-world's sentence,
`reflexion-conformance` E4 quotes it approvingly as the thing to assert, and it is false for all
three limits it covers. **A skill may not claim more than its source shows — and the source here was
our own code comment, which nobody had tested either.**

---

*Executed 2026-08-26 against hello-world at `00408d3` and the code graph built from it. No file in
`/home/user/scio/.claude/skills/` or `/home/user/hello-world` was modified. Nothing committed.*
