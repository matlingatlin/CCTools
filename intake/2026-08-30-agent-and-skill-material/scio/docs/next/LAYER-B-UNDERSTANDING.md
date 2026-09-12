# Layer B · Understanding & architecture — what to build next

Forward-looking. `docs/as-built/LAYER-B-UNDERSTANDING.md` is the starting point; this is what to
do with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method note.** The first draft of this document proposed a bespoke architecture language and a
bespoke impact-analysis algorithm without checking what exists. That is the same failure the
design skill made when it invented a token format while W3C DTCG already existed. This version
was written after a scan of the domains the layer touches: change impact analysis, architecture
description languages, requirements syntax, authorization languages, model-driven code
generation, provenance vocabularies, architecture conformance, and graph query standards.
**Two of the four things the first draft proposed to build already exist as standards**, and the
biggest single finding — impact analysis — turns out to be a field with a 1993 founding paper, a
2004 tool with published precision numbers, a 2024 LLM system, and a 2026 requirements-level
result at 95.8% recall. None of it needed inventing.

---

## 1 · Where Layer B stands

`AppSpec → { whole, architecture, playbook, validation }` (`layerb/service.py`). Eight files,
1,308 lines. The order is the mechanism:

```
service.py:50  gate = is_buildable(spec)          → NotBuildableError if closed
service.py:54  architecture = derive_architecture(spec)   rules, free
service.py:55  validation  = validate_architecture(arch)  rules, free
service.py:57  whole       = await generate_whole(...)    the only model call
```

Deterministic backbone derived and validated **before any model call**; only the *whole* — the
narrative the user approves — goes to the relay, grounded, with the assumed-field list taken from
Layer A's metadata rather than the model's self-report (`whole.py:125`, `whole.py:140`, `whole.py:148`).

This is the cheapest quality mechanism in the system and it should not be touched.

### Two corrections to the as-built record

**The layer has 60 tests, not 30.** `docs/as-built/LAYER-B-UNDERSTANDING.md` cites
`test_layerb_derive` (30). Measured 2026-08-26:

| File | Tests |
|---|---|
| `test_layerb_derive.py` | 30 |
| `test_layerb_validate.py` | 14 |
| `test_layerb_service.py` | 16 |

`60 passed in 0.70s`. The validation and service halves were uncounted.

**There are eleven validation rules, not six.** Six *check functions* emit **eleven distinct
`rule=` identifiers** (`validate.py:56,68,88,100,122,137,157,170,184,200,220,229`):
`action_references_entity`, `permission_maps_to_operation`, `permission_maps_to_role`,
`no_login_vs_roles`, `no_login_vs_user_specific_data`, `relation_resolves`,
`relation_column_exists`, `relation_target_column_exists`, `screen_references_operation`,
`has_entities`, `has_operations`. Exactly one of them — `screen_references_operation` — is
warning severity; the other ten block generation. "Six rules" undersells the layer's strongest
asset by nearly half, and the rule *identifiers* are what an impact-analysis or conformance
mechanism would key on.

### What the verification pass added

`PRODUCTION_READINESS_DIFF.md` §2 states five *product* invariants our analysis had no equivalent
for. Two of them are Layer B's:

> **1. Nothing is built without a contract.** Every function traceable to an approved
> requirement, a visible assumption, or a technical necessity.
>
> **2. No change without impact analysis.** Affected requirements, architecture nodes, packages,
> files and tests identified **before code is written**.

Layer B owns the architecture graph. Both belong here. **Neither exists** — `grep -rn "impact"
apps/engine/src` returns nothing, and there is no requirement identifier anywhere in the system
for invariant 1 to trace *to*.

---

## 2 · Refining what exists

### 2.1 `Whole.grounding` is `dict[str, str]`

`whole.py:42`. Loosely typed for something whose entire job is proving each sentence traces to a
fact. A sentence with no grounding entry is an unsupported claim in the contract the user signs,
and today that is a silence rather than a failure. Type it; make an ungrounded claim a validation
result. See §3.3 for the sharper version of this — grounding is per-*field*, but the thing that
needs grounding is per-*sentence*, and nothing in the code connects the two.

### 2.2 The whole carries no structure

`Whole` is `narrative: str` plus a flat `assumptions: list[str]` (`whole.py:40-41`). The scored
coverage view (Layer A §3.2) is computable today from downstream tags (`intake/gate.py:82`)
× field `source`. Layer B is where it should be assembled, because Layer B is what the user reads.

### 2.3 `derive.py` is 427 lines and twelve module-level functions

The largest file in the layer, the least described, and the one every rebuild will touch. It
derives seven distinct things — data model, auth/access, operations, screens, connectors, security
posture, design tokens. Splitting it along those seams makes each testable against its own spec
fields. Note that `derive_auth_access` already takes `operations` as an argument
(`derive.py:169`), so the seams are not clean and a split has to be designed, not just cut.

### 2.4 The playbook has no design section

It ships stack, folder structure, naming, secure-by-default, tests, accessibility and quality with
every build prompt (`layerb/playbook.yaml`). Appearance is left to the model per package, which is
why generated apps look generated. `.claude/skills/app-design` §1–§4 are written to become
playbook content, and they already resolve the format question by adopting **W3C DTCG** rather
than inventing one.

### 2.5 `Permission` is a bespoke authorization model, and better ones exist

```python
class Permission(BaseModel):           # architecture.py:78-83
    role: str
    operation: str
    scope: str = "own"                 # "own" | "all"
```

A string enum of two values is the whole access model. Meanwhile:

- **Cedar** (AWS, [OOPSLA 2024](https://www.amazon.science/publications/cedar-a-new-language-for-expressive-fast-safe-and-analyzable-authorization)) is a policy language over `principal, action, resource, context`, implemented in Rust with **properties formally verified in Lean**, and — the part that matters here — *designed for a sound and complete logical encoding so policy sets can be analysed*, e.g. to prove a refactor does not change what is authorised.
- **Zanzibar** (Google) and its open implementations **OpenFGA** and **SpiceDB** model relationship-based access, which is what `scope="own"` is groping toward.

Neither should be *shipped inside generated apps* — that would add a service the user did not ask
for, against ADR-0011's fixed stack. But `scope: "own" | "all"` should be replaced by a
Cedar-shaped triple (`principal`, `action`, `resource`, plus an ownership predicate), because that
shape is analysable and the current one is not. See §3.5 for why this is urgent rather than tidy.

### 2.6 `why_slice` refuses to slice, and says so

```python
# layerc/contract.py:16-23
"""The part of the whole this package serves.
The whole is prose, so we don't try to cut it cleverly — a package gets the
whole plus a sentence naming its part in it. Wrong-but-confident slicing
would be worse than carrying two extra paragraphs."""
```

That reasoning is correct **given prose**. It stops being correct the moment the whole has
identified requirements (§3.3): a package that owns `booking` and `create_booking` can be given
exactly the requirements naming them, and that is a lookup, not a guess. The comment is not wrong;
it is a consequence of §3.3 being missing.

---

## 3 · What is missing

### 3.1 Impact analysis — the highest value-to-effort item in the system

The product's promise, in `DIFF`'s own words:

> Only the smallest **dependency-complete and explained** area changes.

Nothing computes that area. The design window resolves markings to files through the manifest
(`core/instrumentation.py:64`, `design/markings.py:119`), which is resolution *after* the fact.
Impact analysis is the question asked *before*.

#### The field, and what it already knows

**Do not invent this.** Change impact analysis (CIA) was founded by Arnold and Bohner in 1993 and
consolidated in their 1996 book *Software Change Impact Analysis* (IEEE CS Press). Lehnert's 2011
review classifies **150 approaches published 1991–2011** against a taxonomy. Four results from
that literature bear directly on the design:

| Source | Result | What it means here |
|---|---|---|
| Arnold & Bohner | CIA splits into **dependency analysis** and **traceability analysis** | Scio needs both: dependency (graph edges) *and* traceability (`source_field` → spec) |
| Weiser 1981 → slicing surveys | **static slices average ~30% of program size**; dynamic ~20% | Forward reachability over-approximates badly. A naive closure will return "most of the app" |
| Ren, Shah, Tip, Ryder & Chesley, **Chianti**, [OOPSLA 2004](https://prolangs.cs.vt.edu/refs/docs/oopsla04.pdf) | **52% of unit tests affected**, but each affected test impacted by only **3.95% of atomic changes** | The value is not the affected set — it is the *affecting* set. Reverse attribution is the useful direction |
| Machalica et al., [Predictive Test Selection](https://arxiv.org/pdf/1810.05286) (Meta, 2018) | **catches >99.9% of regressions while running ⅓ of transitively dependent tests** | Over-approximation is fixable by learning, once you have outcome data — which is §8 |

And the failure mode is documented in the wild: Nx's `affected` graph has a standing discussion
titled ["All projects too often affected"](https://github.com/nrwl/nx/discussions/5580). Coarse
dependency edges collapse to "everything".

#### The two closest prior systems

**CodePlan** ([arXiv 2309.12499](https://arxiv.org/abs/2309.12499), Bairi et al., Microsoft
Research, PACMSE 2024) is the closest structural match: *"a novel combination of an incremental
dependency analysis, a **change may-impact analysis**, and an adaptive planning algorithm"*, used
to drive LLM edits across repositories requiring **2–97 interdependent file changes**. It got
**5/6 repositories** through validity checks where baselines got none. The term of art is
**may-impact** — an over-approximation that is honest about being one.

**ProReFiCIA** ([arXiv 2511.00262](https://arxiv.org/abs/2511.00262), Etezadi, Abualhaija, Arora &
Briand, rev. Aug 2026) is the requirements-level half:

> "ProReFiCIA achieves 85.7% recall on an unseen industrial dataset… the engineer only needs to
> review the predicted impacted requirements, which represent 3.0% of the entire set of
> requirements. Lastly, incorporating domain knowledge via RAG increases recall to 95.8% while
> slightly raising the cost to 3.4%."

That is the exact shape of the product promise: *high recall on the affected set, at a review
burden of a few percent.* It is measured on requirements documents in a regulated industrial
setting, not on generated web apps — the skill written for it must say so (§5, `SKILLS.md`).

#### What Scio already has, and what it must add

Layer B holds nearly everything:

- every architecture node records `source_field` (`architecture.py:50,93,110,119,137,152,164`) —
  though note `Connector.source_field` defaults to `""` (line 137), so one node kind is already
  untraceable and would silently fall out of any impact walk
- downstream tags map spec fields to build areas (`intake/gate.py:82`)
- Layer C's `NodeRef{kind, name}` maps packages to architecture slices (`layerc/plan.py:28-37`)
- the manifest maps `data-scio-id` → `{package, file, line}` (`core/instrumentation.py:64`)
- eleven named validation rules give each node a checkable predicate

**The chain is complete from spec field to source line, and nothing walks it.**

**Proposal, in the vocabulary of the field.** A typed forward closure over that chain, returning a
**tiered** impact set rather than a flat one — because the literature says a flat closure returns
30% of the system:

| Tier | Derived from | Honest name |
|---|---|---|
| **Certain** | nodes whose `source_field` is the edited field; the packages owning them via `NodeRef` | the change set |
| **Likely** | one edge out — relations into/out of a changed table, operations on it, screens listing those operations, permissions naming them | may-impact, depth 1 |
| **Possible** | transitive closure beyond depth 1, and any validation rule whose subject is in the set | may-impact, unbounded |

Bound the walk explicitly. The impact-analysis literature's standard pruning parameters —
*dependency type, minimum importance, maximum depth* — are exactly the three knobs to expose.

What it buys, in order:

- **The promise becomes checkable.** "Only what you marked changes" stops being a claim and
  becomes a diff that either stays inside the computed set or does not.
- **Invariant 3 — no unauthorised diff — gets its mechanism.** A file touched outside the set is
  rejected or escalated.
- **The user sees the blast radius before paying.** This is a named agent-UX pattern, and the
  guidance is specific: *concrete counts beat vague progress* — "this touches 3 packages and 11
  files" rather than a spinner.
- **Cost estimation stops being a guess.** `C-F15` (estimate low band understates cost) is
  unresolved partly because nothing sizes a change.
- **Test selection becomes possible later.** Chianti's direction — *which tests does this change
  affect* — is the same traversal with the test map attached.

**Effort: one traversal function plus a type.** It is still the highest value-to-effort item found
anywhere in this analysis. The scan did not change that conclusion; it changed the design from
"walk the graph" to "walk the graph, tier the result, bound the depth, and measure recall against
real diffs" — which is what forty years of the field says goes wrong otherwise.

### 3.2 Node-level provenance, lifted from Layer A

Invariant 1 wants every function traceable to *a requirement, a visible assumption, or a technical
necessity*. Layer A solved exactly this shape one level down: `FieldMeta.source ∈ {stated, derived,
default}` (`intake/schema.py:57`).

Lift it. Every architecture node gets `origin ∈ {requirement, assumption, necessity}` beside its
existing `source_field`. Then the whole can say *"this exists because you asked for it"* versus
*"because an app that does X needs Y"*; a node with `origin = assumption` is a candidate question
rather than a silent decision; and invariant 1 becomes a validation rule.

**Naming precedent, so the vocabulary is not ours alone.** [W3C PROV-O](https://www.w3.org/TR/prov-o/)
(Recommendation, 2013) models provenance as `Entity` / `Activity` / `Agent` with
`prov:wasDerivedFrom`, `prov:wasGeneratedBy`, `prov:used`. **Adopt the vocabulary, not the RDF
stack.** `source_field` is `wasDerivedFrom`; `origin` is the qualification. Naming our edges after
a fifteen-year-old W3C Recommendation costs nothing and means the graph can be exported to
anything that speaks PROV if it ever needs to be. Serialising to OWL/RDF and standing up a triple
store would be the wrong trade for a Pydantic graph with fifty nodes.

### 3.3 The whole has no requirements in it — which is why invariant 1 cannot be enforced

This is the finding the first draft missed, and it blocks three others.

`Whole.narrative` is one string. There is **no requirement identifier anywhere in the codebase.**
Invariant 1 says every function must be traceable to "an approved requirement" — but no approved
requirement is an addressable object. You cannot trace to a paragraph.

**EARS — Easy Approach to Requirements Syntax** — is the standard answer, and it is small enough to
adopt whole. Developed by Alistair Mavin and colleagues at Rolls-Royce while analysing
airworthiness regulations for a jet-engine control system, published at
[IEEE RE'09](https://alistairmavin.com/ears/), and now standard in aerospace, automotive and
medical devices. Five patterns, one keyword each:

| Pattern | Shape |
|---|---|
| Ubiquitous | *The `<system>` shall `<response>`* |
| Event-driven | **When** `<trigger>`, the `<system>` shall `<response>` |
| State-driven | **While** `<state>`, the `<system>` shall `<response>` |
| Unwanted behaviour | **If** `<condition>`, **then** the `<system>` shall `<response>` |
| Optional feature | **Where** `<feature>`, the `<system>` shall `<response>` |

General form: `WHILE <precondition>, WHEN <trigger>, the <system> SHALL <response>`.

The convergence is worth noting: **AWS Kiro's spec-driven mode uses EARS**, and GitHub's Spec Kit
has [an open issue asking for it](https://github.com/github/spec-kit/issues/1356). The industry is
arriving at the same place from the tooling side.

**Proposal.** `Whole` gains `requirements: list[Requirement]`, where a `Requirement` carries an id,
an EARS-shaped sentence, its `grounding` field(s), its `origin` (§3.2), and the architecture nodes
that satisfy it. `narrative` stays — it is the prose the user reads — but it becomes a *rendering
of* the requirement list rather than the only artifact.

Everything downstream unlocks at once:

- **Invariant 1 becomes checkable**: every node traces to a requirement id or a flagged assumption.
- **`why_slice` can slice** (§2.6): a package gets the requirements naming its entities.
- **Impact analysis gets its top tier**: ProReFiCIA's unit of analysis is the requirement, not the
  file. Without requirement objects, §3.1 can only ever answer at file granularity.
- **Acceptance criteria get a source**: `layerc/criteria.py` currently invents them per package.

The cost is real and should be stated: EARS constrains the prose, and *"accurate before it is
elegant"* (`whole.py:34`) is already the stated bar. Rendering EARS sentences into readable
paragraphs is an extra step, and if it is done badly the spec gate shows the user a requirements
document instead of a story. **Keep the prose primary and the requirement list addressable behind
it**; do not show a numbered list to a restaurant owner.

### 3.4 Architecture alternatives and their trade-offs

`DIFF` §10's minimum product requires the user to *"see the proposed architecture and important
trade-offs"*. Layer B produces **one** architecture, with no alternatives and no stated trade-off.

The method exists and is thirty years old: **ATAM** (SEI, Kazman et al.) — a *utility tree*
decomposing quality attributes into scenarios, evaluated to expose **risks, non-risks, sensitivity
points and trade-off points**. Full ATAM is a multi-day stakeholder workshop and is absurdly
oversized for this. What transfers is the vocabulary: a *sensitivity point* is a decision one
attribute depends on; a *trade-off point* is a decision two attributes pull against.

The choice points are enumerable from the spec, not invented: sign-in method, per-user data
isolation, media storage, synchronous versus queued work. For each, name the two options and the
attribute each favours. Where no real choice exists, say so — *"there is no meaningful choice
here"* is a strong sentence and it costs nothing.

Recent work applies LLMs to exactly this ([arXiv 2506.22688](https://arxiv.org/pdf/2506.22688),
LLM-assisted Attribute-Driven Design; [arXiv 2506.00150](https://arxiv.org/pdf/2506.00150),
LLM support for ATAM scenarios). Both are early and neither reports numbers strong enough to
build on. **Read, do not adopt.** The transferable part is the ATAM vocabulary, which is free.

### 3.5 Nothing in the architecture says what a row-level-security policy *is*

The most consequential gap found in this pass, and it is a security one.

`Table.row_level_security: bool = True` (`architecture.py:49`).
`SecurityPosture.row_level_security: bool = True` (`architecture.py:144`).
`Permission.scope: str = "own"` (`architecture.py:83`).

Three booleans and a two-valued string. **No policy is expressed anywhere in the architecture.**
The generated app's actual isolation comes from whatever SQL a model writes when the playbook says
*"Row-level security ON for every table, with explicit policies — never a blanket allow."*
(`playbook.yaml`). That instruction is a sentence in a prompt. Nothing validates the result.

This is precisely the gap that produced **CVE-2025-48757** (CVSS 9.3 Critical in the CVE record;
the reporting researcher scored it 8.26 base — see `LAYER-G-CROSS-CUTTING.md §1.5`): *insufficient database
row-level security policy in Lovable through 2025-04-15, allowing remote unauthenticated attackers
to read or write arbitrary database tables of generated sites.* Researcher Matt Palmer found
**170+ production applications with fully readable and writable databases**. One published scan
claims 10.3% of the Lovable apps it analysed had RLS effectively bypassed; treat that figure as one
scan's claim rather than an established number — the CVE and the 170+ count are the solid part.

Scio's own review set already flags the adjacent failure: `G-F03`, the cross-tenant idempotency
replay, is **confirmed live**, and `BuildVersion` has no `workspace_id` to scope on. The platform
has the same class of bug it would be generating apps to avoid.

**Proposal.** The architecture gains a typed policy per table per operation — Cedar's
`principal / action / resource` shape (§2.5), derived by rule from `Permission` and `AuthMode` —
and a twelfth validation rule: *every table with `row_level_security = True` has at least one
policy per operation reaching it, and no policy is unconditional.* Supabase's own guidance points
the same way: separate policies for select / insert / update / delete rather than `FOR ALL`, and
test through the client SDK, because the SQL editor bypasses RLS.

This is a deterministic rule, it costs one function call, and it is the difference between
Scio's security wedge being a claim and being a check. **`DIFF` §8 says a component library is not
a differentiator. A generated app that provably cannot ship the CVE that hit the market leader
is.**

### 3.6 Nothing measures whether the whole was right

`POST /spec/approve` exists. Nothing records whether the user approved it unchanged, corrected one
field, or rewrote it. That is the natural quality signal for both A and B, it needs no new model
call, and it is the metric an optimiser would target.

---

## 4 · Out of the box

### 4.1 A reference-architecture library — the component library, one level up

Layer D matches *packages* against a catalog of curated parts. The same idea at architecture level:
booking apps have a shape, marketplaces have a shape, internal tools have a shape.

An architecture pattern would carry the app-kinds it fits, the entities and operations it implies,
the auth shape it assumes, its known trade-off points (§3.4), and evidence from builds that used
it. Matched by app-kind (Layer A §3.1), it turns Layer B's first draft from *derived from six
fields* into *derived from six fields plus fifty apps that already worked*.

Two things make it stronger than the component library:

- **It compounds earlier.** An architecture is chosen once per app; components are matched per
  package.
- **It cannot be bought.** Anyone can import a component collection. A corpus of *validated
  architectures with build outcomes attached* only exists if you ran the builds.

**One caution from the scan.** A 2025 systematic mapping of LLMs in software architecture
([arXiv 2505.16697](https://arxiv.org/pdf/2505.16697)) finds retrieval-augmented generation applied
to architecture tasks **exactly once** across the surveyed literature. That is either a real
opening or a sign that nobody has made it work. Do not treat the emptiness as validation.

### 4.2 A readable architecture language — argue it against what exists, then mostly do not build it

The graph is typed Pydantic: excellent for machines, invisible to humans. The first draft proposed
a bespoke textual form. **Before proposing one, here is the field.**

| Language | What it models | Backing | Fit for Layer B |
|---|---|---|---|
| **C4 / Structurizr DSL** | systems, containers, components, relationships | Simon Brown; de facto standard for architecture-as-code; official [MCP server](https://docs.structurizr.com/ai/mcp) at `mcp.structurizr.com` | **Wrong level.** C4 models deployment topology; Layer B models entities, operations and screens *inside one container* |
| **LikeC4** ([likec4/likec4](https://github.com/likec4/likec4), MIT, ~3.8k stars) | C4 plus custom element types and arbitrary nesting | active TS project | Same level problem, but the escape hatch (custom element types) makes it survivable |
| **ArchiMate / TOGAF** | enterprise architecture layers | The Open Group | Far too heavy |
| **FINOS CALM** ([calm.finos.org](https://calm.finos.org/)) | `nodes` / `relationships` / `metadata` / **controls**, on a JSON meta-schema, with a CLI that **validates** an architecture against controls | FINOS; open-sourced by Morgan Stanley | **Closest match in spirit.** "Controls enforced continuously" is exactly `validate.py`. Level is still service/infrastructure, but the schema is extensible |
| **JHipster JDL** ([jhipster.tech/jdl](https://www.jhipster.tech/jdl/intro/)) | entities, fields, relationships, enums, validation, **and generator options**, in one readable file that a generator consumes | JHipster, ~10 years in production | **The real prior art.** JDL is precisely "readable DSL → generated app", the thing the first draft proposed |
| **DBML** ([dbml.dbdiagram.io](https://dbml.dbdiagram.io/home/)) | tables, columns, refs, enums, notes | dbdiagram.io; open DSL | **Adopt for the data half.** Terse, diffable, renders to a diagram for free |
| **Prisma schema** | models, fields, relations | Prisma | Already in this repo for the *platform*; generator-coupled, so wrong for a *rendering* |

**Verdict: do not invent a language. Render into two that exist, in one direction only.**

- **Data model → DBML.** `DataModel` is a deterministic projection into DBML. That buys a
  human-readable diff *and* a rendered ER diagram at zero cost, from a format Prisma already has a
  published generator for.
- **Auth, operations, screens → a JDL-shaped block.** JDL proves the shape works; borrow its
  grammar rather than its parser.
- **The whole graph, if it ever needs to leave the system → CALM.** JSON, schema-validated,
  extensible, with a CLI. It is the format to export to, not to model in.

**Render only. Never parse back.** The moment the textual form is an input, it is a language with a
grammar, an error-reporting story, an editor story and a versioning story — the maintenance surface
the first draft correctly flagged and then proposed to take on anyway. One-directional rendering
from a typed graph has none of that and delivers the whole benefit the argument was made for: a
diff a user can read at the second approval gate, and a developer who understands the app in a
minute (ADR-0001's wedge).

The honest residue: **nothing in the survey models entities, operations, screens and permissions
together at application level.** JDL comes closest and stops at entities plus generator options.
That gap is real, and it is an argument for a small bespoke *block* — perhaps thirty lines of
grammar for operations and permissions, sitting beside DBML — not for a bespoke *language*. Argue
that residue in the ADR; do not let it justify the whole thing.

### 4.3 Architecture as the contract, narrative as its rendering

The frozen contract today is the *whole* — a narrative. Narratives cannot be checked against an
implementation. If the architecture graph becomes the contract and the narrative becomes its
rendering, invariant 1 is enforceable: every generated function traces to a node, every node to a
requirement or a flagged assumption. The user still reads prose; the system checks the graph.

**This has a name and a 1995 paper.** Murphy, Notkin & Sullivan, *Software Reflexion Models:
Bridging the Gap Between Source and High-Level Models* (FSE'95): the engineer states a high-level
model plus a **mapping** from it to the source, and a tool computes where the model and the source
**converge, diverge, and where the source has edges absent from the model**. Three outcomes, not
pass/fail. It is the founding technique behind every architecture-conformance tool since
(ArchUnit, dependency-cruiser, Sonargraph, Lattix).

**Scio already has the mapping**, which is the part reflexion models normally require a human to
author: `NodeRef` → package (`layerc/plan.py:79`), `Manifest.packages` → files
(`core/instrumentation.py:66`), `data-scio-id` → source location. The convergence/divergence/absence
report is computable from artifacts that already exist. That is what makes B-3 a build rather than
a research project — and the three-way outcome is a better fit for this system than a boolean,
because *absence* (source with no architecture node behind it) is exactly invariant 1's violation.

### 4.4 What developers say about generated code — now with a CVSS number

From the practitioner scan: *"PRs containing AI-generated code often look perfect on the surface but
are architecturally incoherent underneath."*

That sentence is Layer B's reason for existing. It was already the strongest available public
argument. **CVE-2025-48757 makes it concrete and attributable**: the market leader shipped 170+
applications with unenforced row-level security, at CVSS 9.3 Critical, and the mechanism that would have
caught it is a deterministic rule over a typed architecture — the thing Layer B already is, minus
§3.5.

The positioning writes itself and costs nothing, *provided §3.5 ships first*. Making the claim
before the rule exists would be the same failure with our name on it.

---

## 5 · The means — skills, standards, repos, research

Verdict per row. **adopt** = use it, cite it, do not rebuild it. **later** = real, not now.
**not for this layer** = scanned, rejected, reason given.

### Standards and formats

| Thing | What it gives | Verdict |
|---|---|---|
| **EARS** (Mavin et al., RE'09) | five sentence patterns that make a requirement addressable and testable; already used by AWS Kiro | **adopt** — §3.3, the unblocker for invariant 1 |
| **W3C PROV-O** (Rec. 2013) | `wasDerivedFrom` / `wasGeneratedBy` / `used`; Entity–Activity–Agent | **adopt the vocabulary**, not the RDF stack — §3.2 |
| **DBML** | readable data-model DSL, free ER rendering, Prisma generator exists | **adopt** as a rendering target — §4.2 |
| **JHipster JDL** | proven "readable DSL → generated app" grammar for entities + options | **adopt the shape**, not the parser — §4.2 |
| **FINOS CALM** | JSON meta-schema for architecture-as-code, with controls and a validating CLI | **later** — the export format if the graph ever leaves the system |
| **Cedar** (AWS, OOPSLA 2024) | `principal/action/resource/context`, formally verified in Lean, analysable policy sets | **adopt the shape** for `Permission` — §2.5, §3.5. Do not ship the engine into generated apps |
| **Zanzibar / OpenFGA / SpiceDB** | ReBAC, relationship tuples at scale | **not for this layer** — right idea, wrong scale; adds a service ADR-0011 does not have |
| **C4 / Structurizr DSL / LikeC4 / ArchiMate** | architecture-as-code at container level | **not for this layer** — wrong abstraction level (§4.2) |
| **W3C DTCG + Style Dictionary** | the design-token standard and its transform pipeline | **adopt** — already decided in `.claude/skills/app-design`; arrives here as playbook content |
| **ISO/IEC 39075:2024 (GQL)** + openCypher | the first new ISO query-language standard since SQL in 1987; property-graph traversal | **not for this layer** — Layer B's graph has tens of nodes and lives in Pydantic. Revisit only if the reference-architecture corpus (§4.1) becomes a database |
| **MADR / Nygard ADR format** | the ADR conventions this repo already follows | already ours — `docs/decisions/0000-adr-template.md` |

### Research

All read at abstract-to-method level; none reproduced. Numbers below are the authors' on their
data, not ours.

| Work | Gives Layer B | Verdict |
|---|---|---|
| **Arnold & Bohner**, *Software Change Impact Analysis* (1993 / IEEE CS Press 1996) | the field's founding frame: dependency analysis + traceability analysis | **adopt** → skill |
| **Lehnert (2011)**, *A Review of Software Change Impact Analysis* | taxonomy over 150 approaches, 1991–2011 | **adopt** as the map → same skill |
| **Ren, Shah, Tip, Ryder & Chesley**, *Chianti* (OOPSLA 2004) | atomic changes → affected tests → **affecting changes**; 52% tests affected, 3.95% changes per affected test | **adopt** — the reverse-attribution idea is the useful half → same skill |
| **Weiser (1981)** + slicing surveys | forward slicing as the CIA primitive; static slices ~30% of program | **adopt as a warning** — bound the walk → same skill |
| **Bairi et al., CodePlan** (arXiv 2309.12499, PACMSE 2024) | incremental dependency analysis + **change may-impact analysis** + adaptive planning; 2–97 files/task; 5/6 repos pass vs 0 for baselines | **adopt the framing** → same skill |
| **Etezadi, Abualhaija, Arora & Briand, ProReFiCIA** (arXiv 2511.00262) | requirements-level CIA; **85.7% → 95.8% recall with RAG, at 3.0–3.4% review burden** | **adopt** — the target metric for §3.1 → same skill |
| **Machalica et al.**, *Predictive Test Selection* (Meta, arXiv 1810.05286) | >99.9% regressions caught running ⅓ of transitively dependent tests | **later** — the upgrade path once §8's outcome data exists |
| **Murphy, Notkin & Sullivan**, *Software Reflexion Models* (FSE'95) | model + mapping → converge / diverge / absent | **adopt** → skill, underpins B-3 |
| **Mavin et al., EARS** (RE'09) | the five requirement patterns | **adopt** → skill |
| **Cedar** (Amazon Science, OOPSLA 2024) | analysable authorization; Lean-verified | **adopt the shape** (§2.5) |
| **LLM-assisted ADD** (arXiv 2506.22688), **LLMs for ATAM scenarios** (arXiv 2506.00150) | generating architecture alternatives with stated trade-offs | **read, not adopt** — early, no numbers strong enough |
| **Software Architecture Meets LLMs** (arXiv 2505.16697) | systematic mapping; RAG applied to SA tasks exactly once | context for §4.1 — treat the gap sceptically |

### Tools, MCP and repos

| Thing | What it gives | Verdict |
|---|---|---|
| **Nx `affected`** | a production affected-graph, and a public record of its failure mode ("all projects too often affected") | **study, do not depend** — the failure mode is the design constraint for §3.1 |
| **Aider repo map** (tree-sitter + personalised PageRank into a token budget) | ranking a graph *to fit a budget* rather than sending it all | **adopt the idea** in §6; the implementation is for source trees, not our graph |
| **`code-graph-mcp`, service-graph MCP servers** | `get_impact_analysis` / blast-radius over source ASTs | **later** — they answer the Layer E/F question (which files), not the Layer B question (which requirements and nodes) |
| **Structurizr MCP** (`mcp.structurizr.com`) | DSL validation, C4 views, ADR tooling for agents | **not for this layer** — follows §4.2's level verdict |
| **`blast-radius` community Claude skill**, Blast Radius (blast-radius.dev) | affected-component lists, risk scoring, prioritised test selection as a product category | evidence the category exists — **not a dependency** |
| **Supabase RLS guidance + pgTAP helpers** | per-operation policies, multi-tenant test helpers, "test via the SDK, not the SQL editor" | **adopt** into playbook + §3.5's rule |
| **`skill-creator`** | evals and variance analysis for skills | **adopt** — required to make §5's skills measurable rather than believed |

### Skills written for this layer

Per `docs/next/SKILLS.md`, **a paper we adopt becomes a skill**, carrying source · method · limits ·
eval, and **may not claim more than its paper shows**:

- **`.claude/skills/change-impact-analysis/`** — the CIA lineage (Arnold & Bohner → Lehnert →
  Chianti → CodePlan → ProReFiCIA), in the form Layer B uses it. Underpins B-1.
- **`.claude/skills/ears-requirements/`** — the five patterns, how a `Requirement` is written and
  what makes one invalid. Underpins B-2.
- **`.claude/skills/reflexion-conformance/`** — model + mapping → converge/diverge/absent, mapped
  onto `NodeRef` and `Manifest`. Underpins B-4.

---

## 6 · Retrieval versus packing

**Where does this layer send context it could have queried?**

Layer B's own model call is well behaved. `grounding_facts()` (`whole.py:56`) builds a bounded dict
and the docstring states the guarantee: *"Nothing outside this dict reaches the model, which is
what makes 'grounded only' enforceable rather than merely requested."* That is the correct pattern
and it should be copied, not changed.

**But Layer B is where the system's worst packing violation originates.** Two constants leave this
layer and are carried into every package prompt downstream:

1. `Playbook.as_prompt_section()` (`playbook.py:46`) — byte-identical across every package, every
   build, and every user. Attached at `layerc/contract.py:134`.
2. `why_slice()` (`layerc/contract.py:16`) — sends the **entire whole** to every package, by
   deliberate choice (§2.6).

Nine packages means nine copies of both, times four codegen passes (§7).

**The architecture graph makes the retrieval version obvious**, and §3.3 makes it safe. A package
owns named entities and operations (`NodeRef`); the requirements mentioning them are a lookup, not
an inference. Layer B has the graph and never offers the query. Same shape as `validate_plan`:
built, then not consulted.

**The named prior art is Aider's repo map** — tree-sitter symbol graph, personalised PageRank,
rendered to fit an explicit `--map-tokens` budget. The transferable principle is not the algorithm
(our graph has tens of nodes, not thousands of symbols) but the *contract*: **context is selected
to fit a stated budget, ranked by relevance to the current task**, rather than concatenated and
hoped over.

One honest qualification. Layer B's graph is small — 1,659 tokens for a three-table app, 3,459 for
a six-table one (§7). Retrieval here does not solve "it does not fit". It solves "the same constant
is paid nine times, four times each". That is a caching problem at least as much as a retrieval
one, and §7 says both.

---

## 7 · Token economy — measured

Measured 2026-08-26 against the real prompts and two real derived architectures. Method: build the
spec, run `derive_architecture` → `build_plan` → `assemble_contract` → `contract_prompt` against
`hello-world`'s engine venv; count characters; estimate at 4 chars/token. **Estimates, not
`count_tokens` calls** — treat the ratios as solid and the absolute numbers as ±15%. Re-measuring
with `client.messages.count_tokens` is a twenty-minute job and should be done before any of these
figures reaches a cost model.

### Layer B in isolation

| Artifact | Chars | ≈ Tokens |
|---|---|---|
| `WHOLE_SYSTEM` | 730 | **182** |
| whole `build_prompt` (booking) | 528 | 132 |
| `Playbook.as_prompt_section()` | 2,671 | **668** |
| `Architecture` JSON, 3 tables / 2 ops | 6,635 | 1,659 |
| `Architecture` JSON, 6 tables / 6 ops | 13,837 | 3,459 |
| `BuildContext.as_prompt()` (booking) | 9,809 | 2,452 |

| Call | Cost today |
|---|---|
| Architecture derivation | **free** — rules |
| Eleven validation rules | **free** — rules |
| The whole | 2 relay passes on a ~314-token prompt |
| Playbook | constant, no model |

Layer B is close to free. **Everything expensive about Layer B happens downstream.**

### What Layer B's constants cost a real build

Marketplace app: 6 tables, 6 operations, **9 build packages**. `codegen_passes = 4` by default
(`builder/loop.py:252`), and the relay re-sends the task on every pass
(`execution/relay.py:37` — *"Below is the original task and the current best answer after review
passes"*).

| Component | ≈ Tokens, all 9 packages | ×4 codegen passes |
|---|---|---|
| `house_rules` (the playbook, identical 9×) | 6,010 | **24,040** |
| `why` (the whole, sent 9×) | 4,234 | **16,936** |
| `contract_prompt` (goal, slice, interfaces, boundary) | 15,596 | 62,384 |
| **Total contract substrate** | **25,840** | **≈ 103,400** |

At Opus 5 input pricing ($5/MTok) that is **≈ $0.52 per build in contract text alone** — before a
single line of generated code, before any repair round, before critique. The playbook and the whole
account for **≈ $0.20 of it, and both are constants.**

### The correction: the playbook cannot be cached alone

The previous draft called the playbook *"the single best caching target in the system."* Measured,
it is **668 tokens** — and the minimum cacheable prefix is **~1,024 tokens**. A breakpoint on the
playbook alone caches nothing, silently.

**What actually works.** The API renders `tools → system → messages`, and caching is a strict prefix
match. Order the package prompt **playbook first, then the architecture slice**, and put the
breakpoint after the architecture:

```
playbook (668, byte-identical everywhere)  +  architecture (1,659–3,459, identical per build)
= 2,327–4,127 tokens  →  clears the 1,024 floor with 2.3–4× margin
```

Cache reads cost ~0.1×, writes ~1.25×. Across 9 packages × 4 passes with one write and 35 reads,
the ~26k-token constant substrate costs roughly a tenth of what it costs today. Max 4 breakpoints
per request; one is enough here.

**Two things that must be true, and are not verified:**

1. The prefix must be byte-stable. `Architecture.model_dump_json(indent=2)` is deterministic for a
   fixed graph — Pydantic preserves field order — but nothing asserts it. **A test should assert
   the prefix is identical across two assemblies of the same architecture**, the same way Layer A
   §5.1 wants an assertion that `EXTRACTION_SYSTEM` stays above the floor.
2. `usage.cache_read_input_tokens` must be non-zero across packages. If it is zero, something in
   the prefix varies.

**A second, larger saving sits behind §3.3.** `why` costs 16,936 tokens per build because every
package receives the entire whole. With requirements as addressable objects, a package receives the
requirements naming its entities — plausibly a fifth of the text, and *more* relevant, not less.
`why_slice`'s comment says wrong-but-confident slicing would be worse than two extra paragraphs.
It is right. Requirement-keyed slicing is not confident guessing; it is a lookup.

### Effort

Split like Layer A's. Nothing in Layer B calls a model except the whole, and the whole is a
judgement call over a small grounded input — `output_config: {effort: "high"}` or `xhigh`, with
adaptive thinking. Everything else here is rules and should stay that way.

---

## 8 · Data worth owning

| Data | Why |
|---|---|
| **Architecture graphs by app-kind** | the input to §4.1. Fifty booking apps make the fifty-first better in a way no import can |
| **Which of the eleven rules fire, and on what** | tells you where users' specs are typically incoherent — a Layer A question answered by Layer B data |
| **Whether the whole was approved unchanged** | §3.6. The quality signal for two layers |
| **Trade-off choices users made** | when both options were offered, which was picked, per app-kind — the input to better defaults (§3.4) |
| **Impact set vs actual diff, per change** | the recall measurement for §3.1, and the *only* thing that makes B-1 improvable rather than assertable. ProReFiCIA's numbers exist because someone had ground truth; ours will not until this is stored |
| **Requirement → node → package → file chains that held, and ones that broke** | the training set for predictive impact selection (Meta's result), and the evidence base for the marketing claim in §4.4 |

Note the pattern: **Layer B's data improves Layer A.** Where specs are incoherent tells you which
questions are asked badly. Nothing currently connects those two.

Same constraint as Layer A: this is user data, and retention is governed by **ADR-0019, still
Proposed**. What survives project deletion must be settled before the corpus accumulates.

---

## 9 · ADR proposals

| # | Proposal | Decides | Rests on |
|---|---|---|---|
| **B-1** | **Impact analysis over the architecture graph** — tiered certain/likely/possible, depth-bounded, recall measured against real diffs | the mechanism behind the product's core promise, and behind invariants 2 and 3 | Arnold & Bohner; Chianti; CodePlan; ProReFiCIA |
| **B-2** | **The whole carries EARS-shaped requirements with ids**; the narrative becomes their rendering | makes invariant 1 traceable at all; unblocks B-1's top tier, B-4, and requirement-keyed `why` | Mavin et al., RE'09 |
| **B-3** | **RLS policy in the architecture, plus a twelfth validation rule** | whether Scio can ship the CVE that hit Lovable | CVE-2025-48757; Cedar's shape; Supabase guidance |
| **B-4** | **The architecture graph is the contract; the narrative is its rendering** — checked as a reflexion model (converge / diverge / absent) | what "approved" means. The largest conceptual change here | Murphy, Notkin & Sullivan, FSE'95 |
| **B-5** | **`origin ∈ {requirement, assumption, necessity}` on every node**, named after PROV-O | makes invariant 1 a validation rule rather than an aspiration | W3C PROV-O |
| **B-6** | **Cache the playbook+architecture prefix explicitly**, with a byte-stability test | free, multiplied by package count × pass count. The playbook alone is 668 rendered tokens — **which is above Opus 5's 512-token floor, so it caches on its own.** *(Corrected 2026-08-26: the original reason read "will not cache", resting on a ~1,024 floor that Layer A §7.3 retracted. The proposal is right; its stated reason was wrong, and it is now stronger — the win needs no other change first.)* And the dominant term is not the playbook at all: `playbook.py:118` passes `architecture.model_dump_json(indent=2)` — the entire graph, indented — into every package prompt, with the docstring at `:83` conceding "for now it assembles the whole architecture" | measured, §7 |
| **B-7** | **A design section in the playbook** | see `.claude/skills/app-design` §1–§4; DTCG already decided | W3C DTCG |
| **B-8** | **Architecture alternatives with stated trade-off points** | required by `DIFF` §10's minimum product | ATAM vocabulary |
| **B-9** | **Render the architecture to DBML plus a JDL-shaped block — one direction, no parser** | kills the bespoke-language proposal, keeps the benefit | DBML; JHipster JDL; §4.2's survey |
| **B-10** | **A reference-architecture library keyed by app-kind, with build outcomes** | the compounding asset. Depends on B-5 and on having run builds | §4.1 |

### Ordering, and why

1. **B-2 first**, which reverses the previous draft. Impact analysis at file granularity is
   useful; impact analysis at *requirement* granularity is the product promise, and ProReFiCIA's
   result is a requirements-level result. Without addressable requirements, B-1 can only ever
   answer "which files", never "which of the things you asked for". B-2 is also small.
2. **B-1 next**, and by a distance from everything after it. One traversal over a graph that
   already exists, with the tiering and depth bound the literature demands.
3. **B-3 in parallel with B-1** — it is independent, deterministic, cheap, and it is the only item
   here with a CVSS score attached to *not* doing it.
4. **B-6 is free** and can ship any time; it changes no behaviour, only assembly order and one
   breakpoint. Do it with the byte-stability test or not at all.
5. **B-5** is small and B-1, B-4 and B-10 all lean on it.
6. **B-4 is the one to argue about properly** before anyone builds it. Reflexion models give it a
   thirty-year foundation and a better output shape than pass/fail, but it changes what the user is
   approving.
7. **B-9 exists mainly to stop the bespoke language.** If the ADR is written and the answer is
   "render to DBML, borrow JDL's grammar, never parse", it has done its job.

**One question this pass could not settle.** Impact analysis needs ground truth to be measured, and
ground truth is *the diff a change actually produced*. That data does not exist yet and cannot be
manufactured — it accrues only from real builds. So B-1 ships as a **may-impact** analysis with an
honest name, and becomes a *measured* one later. Anyone who wants a recall number before the builds
have run is asking for a number that would be invented, which is the failure this document was
written to avoid.

---

*Written 2026-08-26. Token figures measured against the real prompts and two derived
architectures; test counts and rule counts measured by running the suite; research read at
abstract-to-method level and none reproduced; every quoted number is the source's own, on the
source's data, not ours. Nothing here is implemented.*
