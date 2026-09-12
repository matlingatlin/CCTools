---
name: architecture
layer: B, build-process
phase: build-time
status: written
description: The catalogue of architecture patterns and the procedure for choosing one, so nobody proposes an architecture before searching the list. Use whenever the word architecture comes up - choosing the shape of Scio itself or of one of its seven layers, deriving an app architecture from a spec, or when someone proposes microservices, event sourcing, CQRS, hexagonal, ports and adapters, modular monolith, serverless, an event bus, or an agent orchestration pattern. Also when a quality attribute has to be named before a decision, when a tenancy isolation model is picked, when a settled ADR is about to be contradicted, or when an ADR needs its trade-offs written down. Carries fourteen patterns with what disqualifies each, the ISO 25010:2023 attribute vocabulary, the ATAM trade-off vocabulary, the deterministic-first boundary rule made operational, and the output contract the next stage needs.
---

# architecture

**The standing rule: when the word "architecture" appears, search this list before proposing.**
Proposing first and checking afterwards produces a critique of the thing you already chose. The
column that makes this a skill rather than a glossary is **"disqualified when"** — elimination is
cheaper than comparison, and it is the half of the field that blog summaries drop.

Two audiences, one procedure. **Us**, choosing the shape of Scio's seven layers. **The product**,
deriving an app's architecture from a spec — which `derive_architecture(spec)` already does as a
pure function, with `validate_architecture` running **eleven rule identifiers** over the result
(`layerb/validate.py:56,68,88,100,122,137,157,170,184,200,220,229`; ten error, one warning).

---

## 1 · Source

**Scanned 2026-08-26.** Every claim below carries its link and its date. Where a source is
paywalled or a claim is secondary, it is flagged in §9 rather than asserted.

**The pattern catalogue.** Mark Richards, *Software Architecture Patterns*, 2nd ed., O'Reilly,
August 2022; Richards & Ford, *Fundamentals of Software Architecture*, 2nd ed., O'Reilly,
April 2025 ([publisher listing](https://www.oreilly.com/library/view/fundamentals-of-software/9781098175504/)).
Primary pattern sources: Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*,
CACM 15(12), Dec 1972 ([ACM](https://dl.acm.org/doi/10.1145/361598.361623)); Cockburn,
*Hexagonal Architecture*, v0.9 2005-09-04 ([alistair.cockburn.us](https://alistair.cockburn.us/hexagonal-architecture/));
Palermo, *The Onion Architecture*, July 2008 ([part 1](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/));
Martin, *The Clean Architecture*, 2012-08-13 ([cleancoder](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html));
Fowler, [CQRS](https://martinfowler.com/bliki/CQRS.html) (2011-07-14),
[EventSourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (2005-12-12),
[MicroservicePrerequisites](https://martinfowler.com/bliki/MicroservicePrerequisites.html) (2014-08-28),
[MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) (2015-06-03);
Simon Brown, [modular monolith](https://simonbrown.je/modular-monolith/); Hewitt et al., actor
model, 1973. Vendor "when not to use" lists, which are the most explicit disqualifiers published:
Azure Architecture Center [Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
(ms.date 2026-03-27) and [Pipes and Filters](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters)
(ms.date 2024-04-10).

**How to choose.** ISO/IEC 25010:2023, *Product quality model* — nine characteristics
([ISO](https://www.iso.org/standard/78176.html); [arc42 rendering](https://quality.arc42.org/standards/iso-25010)).
SEI ATAM and CBAM ([SEI library](https://www.sei.cmu.edu/library/integrating-the-architecture-tradeoff-analysis-method-atam-with-the-cost-benefit-analysis-method-cbam/)).
Ford/Parsons/Kua fitness functions ([Thoughtworks, 2019-01-11](https://www.thoughtworks.com/insights/articles/fitness-function-driven-development)).
[C4 model](https://docs.structurizr.com/) and [arc42](https://arc42.org/) (template v9).
[Team Topologies key concepts](https://teamtopologies.com/key-concepts) — four team types, three
interaction modes, cognitive load as a hard constraint. MADR 4.0.0, released 2024-09-17
([adr.github.io/madr](https://adr.github.io/madr/)).

**Design structure.** Already carried by `.claude/skills/design-rule-hierarchy` (Baldwin & Clark;
MacCormack propagation cost; Cai's DRH algorithm; Bunch MQ). **Do not restate it here — call it.**

**LLM and agentic systems.** Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
(2024-12-19), [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
(2025-06-13), [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
(2025-09-29). Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657),
v3 2025-10-26; NeurIPS 2025). Schmid et al., *Software Architecture Meets LLMs: A Systematic
Literature Review* ([arXiv 2505.16697](https://arxiv.org/abs/2505.16697), 2025-05-22). Hu Wei,
*Architectural Design Decisions in AI Agent Harnesses* ([arXiv 2604.18071](https://arxiv.org/abs/2604.18071),
2026-04-20). Xia et al., *Harnessing Agent Skills* ([arXiv 2606.20631](https://arxiv.org/abs/2606.20631),
2026-05-29). [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
— **checked 2026-08-26: still Development, moved out of the main semconv repo, no tagged release.**

**Multi-tenant SaaS.** AWS, [SaaS Tenant Isolation Strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-bridge-model.html)
(silo / pool / bridge). Azure, [Architectural approaches for storage and data in multitenant solutions](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data)
(ms.date 2026-08-21). [CVE-2025-48757](https://github.com/advisories/GHSA-773x-pxjg-gxgx) — insufficient
RLS in generated Lovable projects, CVSS v3.1 9.3 Critical, **disputed by the supplier**.

**This repo.** `docs/as-built/01-DECISIONS.md` (twenty ADRs), `docs/as-built/LAYER-B-UNDERSTANDING.md`,
`docs/next/LAYER-B-UNDERSTANDING.md`, `CLAUDE.md`.

---

## 2 · The list

Sections 2–8 are the **Method**. Read the disqualifier column first; read "buys" only for what
survives.

| Pattern | Buys | Costs | **Disqualified when** | Already here |
|---|---|---|---|---|
| **Layered** | one place per kind of thing; easiest onboarding; cheapest to reason about | change often cuts every layer; layers become a suggestion without enforcement | a change that is one feature routinely touches every layer (Parnas 1972: decompose by *hidden design decision*, not by processing step) | Scio's A→G layering; `graph-guard` enforces the boundaries |
| **Pipes and filters** | independent, reorderable, independently scalable steps; each testable alone | whole chain retested on any change; per-step state is expensive; duplicate delivery must be handled | steps are not independent, must commit as one transaction, the caller needs request/response, or a step needs so much context that carrying it dominates ([Azure, 2024-04-10](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters)) | **the pipeline itself** — A→B→C→D→E→F, each layer a filter with a typed contract |
| **Hexagonal / ports and adapters** | the core can be driven by a user, a test, or a batch script, and developed with no database up ([Cockburn 2005](https://alistair.cockburn.us/hexagonal-architecture/)) | an interface and an adapter per external thing; indirection that reads as ceremony when there is one adapter | there will only ever be one implementation and no test double is wanted — the port is then a synonym | ADR-0005 (sandbox behind a swappable interface) and ADR-0008 (Clerk behind our own interface) are ports-and-adapters in all but name |
| **Clean / Onion** | one rule — source dependencies point inward only ([Martin 2012](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), [Palermo 2008](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)) | mapping layers; DTO duplication; a lot of structure for a small domain | the domain is thin — a CRUD app with rules that fit on a page pays the mapping cost and gets nothing. Martin himself notes hexagonal, onion and DDD layering describe the same shape; picking all three is one decision, not three | not used explicitly; the inward-only rule is what `graph-guard` checks |
| **Microkernel / plug-in** | a stable core plus features added without touching it; third parties can extend | the plug-in contract is now public and versioned; core creep is constant pressure | the extension points cannot be enumerated up front, or you are the only author of plug-ins | Layer D's component library and connectors are plug-in shaped; Claude skills are a microkernel over the agent |
| **Modular monolith** | module boundaries with no network; one deploy; refactoring across boundaries stays cheap | boundaries hold only if a tool enforces them — Brown's failure mode is *everything public*, and the package structure becomes decoration | modules genuinely need independent deploy cadence or independent scaling, and you have the teams to own them | hello-world is one: 155 source files, 22,990 lines (`docs/as-built/00-INDEX.md`) |
| **Service-based** | 4–12 coarse-grained deployables over **one** database; most of the deploy independence, none of the distributed-data problem | one schema is a shared coupling point; a migration is still global | services would need separate data stores, or you need more than roughly a dozen | **exactly what ADR-0006 + ADR-0007 built**: NestJS API + Python FastAPI engine over one PostgreSQL |
| **Microservices** | independent deploy, scale and failure domains per bounded context | distributed transactions, network failure as a normal case, per-service ops | **Fowler's three prerequisites are absent** — rapid provisioning, basic monitoring, rapid deployment ([2014-08-28](https://martinfowler.com/bliki/MicroservicePrerequisites.html)); or the boundaries are not yet known ([MonolithFirst, 2015-06-03](https://martinfowler.com/bliki/MonolithFirst.html)); or one team owns everything | **not used, deliberately.** See eval A1 |
| **Event-driven** | producers do not know consumers; spiky load absorbs into a queue; new consumers cost nothing | no single place shows the flow; ordering, duplicates and poison messages are your problem; debugging is archaeology | you need a synchronous answer, or the "events" are really commands with one consumer — then it is a queue, not an architecture | ADR-0020 ("builds are jobs, not requests") is the shape, **partly implemented — the queue is not built** |
| **CQRS** | read and write models evolve apart; each optimised for its own load | two models, two mappings, a synchronisation story | Fowler, verbatim: *"you should be very cautious about using CQRS"* and for most systems it *"adds risky complexity"*; disqualified when read and write models overlap enough to share, and always disqualified **for a whole system** rather than one part ([2011-07-14](https://martinfowler.com/bliki/CQRS.html)) | not used. Do not introduce it to fix a query that needs an index |
| **Event sourcing** | a real audit trail; time travel; append-only writes avoid row locks | replay must reproduce past external calls; immutable events versus the right to erasure; schema evolution by upcaster; storage grows forever | straightforward CRUD; **prototypes, MVPs, or short-lived systems**; views that must be strongly consistent; static reference data; a team with no event-driven experience ([Azure, ms.date 2026-03-27](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)) | not used — and **git already is the append-only log** for generated code (ADR-0017). See eval A3 |
| **Space-based** | extreme, elastic throughput by removing the database from the request path | replicated-cache collisions under concurrent update; operational weight | caches are large, updates frequent, or replication latency times update rate puts the collision probability above what the data tolerates | no. Scio's load is per-build, not per-request |
| **Actor model** | isolated state, message passing, supervised failure — concurrency without shared locks | no ambient transactions; rollback across actors is manual compensation | the workload needs multi-entity transactions or a guaranteed global sequence — you would be rebuilding two-phase commit out of mailboxes | no |
| **Serverless** | zero idle cost; scaling is someone else's problem; ephemeral isolation per invocation | cold starts; execution ceilings; connection-pool pressure; provisioned concurrency reintroduces the fixed cost it removed | long-running or stateful work, persistent connections, or **sustained predictable load** — at which point the elasticity you are paying for is not being used | ADR-0005: ACA dynamic sessions for the build sandbox — serverless in exactly one place, for isolation, not for cost |

Generated apps are **not** an open question: ADR-0011 fixes Next.js + TS + Tailwind + Supabase.
That is the *output* stack. This table is for Scio's own shape and for the *logical* architecture
the product derives.

---

## 3 · The selection procedure

1. **Name the quality attributes before naming any pattern.** Use ISO/IEC 25010:2023's nine —
   functional suitability, performance efficiency, compatibility, interaction capability,
   reliability, security, maintainability, **flexibility**, **safety**. (2023 replaced *usability*
   with interaction capability, *portability* with flexibility, and added safety; testability
   stayed under maintainability.) **Pick at most three.** Three is the budget because everything
   after the third is what you will sacrifice.
2. **Turn each into a scenario with a response measure.** ATAM's utility tree: stimulus,
   environment, response. "Fast" is not an attribute. "A build plan for a 12-action spec derives
   in under 100 ms with no model call" is. An attribute with no measure cannot disqualify anything.
3. **Run the disqualifier column, not the buys column.** For every candidate, answer only: does a
   disqualifier fire? Write the answer down per candidate — the record of *what was eliminated and
   why* is half the ADR.
4. **Count the owners.** Team Topologies: a structure needing more independent owners than exist
   will be operated as a monolith with extra network calls. One team plus microservices is
   disqualified at this step, before any technical argument.
5. **Cost the survivors, do not rank them.** CBAM's question is benefit per unit cost, not "which
   is better". If two survivors cost the same, you have a tie, not a winner.
6. **Break the tie with evidence, in this order.** (a) A **settled ADR** — an accepted decision
   wins unless the argument engages the reason it states. (b) A number measured **in this repo**.
   (c) A published result, quoted with its scope and its date. (d) **Reversibility** — prefer the
   choice that is cheaper to undo. Fashion, star counts and blog posts break no ties.
7. **When two survive and neither is disqualified, choose the boring one.** The condition is
   precise, not a mood: no disqualifier fires for the simple option; the fancy option's advantage
   lands on an attribute outside your top three; the owner count is one; and the change is
   reversible. Fowler's observation is that *almost all* successful microservice stories began as
   a monolith that got too big, while greenfield microservices "ended up in serious trouble".
8. **Write the ADR, and name the sacrifice.** MADR 4.0.0 shape, this repo's
   `docs/decisions/0000-adr-template.md`, numbered, with status. **An ADR that names no sacrificed
   attribute is a press release.** Supersede, never edit (CLAUDE.md).
9. **Encode each structural claim as a fitness function, or write "not checkable" out loud.** An
   unchecked boundary drifts. `graph-guard` already does this for layer boundaries here.

**Four allowed outcomes**, per CLAUDE.md: build · complete · **keep** · park. *Keep* — deciding the
existing design is wiser than the new idea — is a real answer and must be written down with its
reason so the question does not come back.

---

## 4 · Deterministic-first, as an architectural principle with a boundary

This is Scio's core commitment and it is implemented independently in five layers
(`docs/as-built/ARCHITECTURE-AS-BUILT.md`). Stated as an architectural rule:

> **Rules do what rules can guarantee. The model is used only where judgement is genuinely
> required, grounded, with its additions flagged — and it runs last.**

**The ordering law.** Derive with rules → validate with rules → *then* call the model.
`layerb/service.py:50-57` is the reference implementation: gate, `derive_architecture`,
`validate_architecture`, and only then `generate_whole`. The reason is economic and is written in
the code: *"a design error costs a function call rather than a relay run."*

**Which side is a decision on? Three tests, in order.**

| Test | If yes → | Why |
|---|---|---|
| Is the answer a function of data that is already typed? | **rule** | `derive_architecture` is exactly this: tagged spec fields → typed graph, no call |
| Is the set of correct answers finite and enumerable? | **rule** | the eleven validation rules enumerate incoherence classes; a rule id is something impact analysis and conformance can key on |
| Would two competent people, given the same input, agree? | **rule** | disagreement is the definition of judgement. Agreement means you have a specification and are paying a model to run it |

**A fourth test, and it is the one that resolves the cases the first three leave ambiguous:
separate the *count* from the *content*.**

> **The code decides how many. The model fills what is in each.**

Added 2026-08-26 from `docs/mined/PASS2-FOUR-REPOS.md` §1.4 (task-master `scope-adjustment.js`),
where a target subtask count is computed in pure arithmetic from four typed inputs and only then is
the model asked for that many. **The structure is the finding; none of its constants are taken** —
nothing justifies 1.3 over 1.25, and copying an arbitrary coefficient is how a rule becomes
folklore.

It works by splitting one decision into two that fall on different sides:

| Decision | Side | Why |
|---|---|---|
| how many packages a feature splits into | **rule** | a function of the architecture's own measurements |
| what each resulting package's goal sentence says | model | prose a person will read |
| how much ceremony a build gets — which gates run | **rule** | *"a model may not set ceremony any more than it may set membership"* (`docs/mined/ECC-SKILLS.md:655`). Computed from the plan, stated aloud, user-overridable — never judged |
| which identifier a generated element carries | **rule** | an identifier a generator can derive is never model-chosen, or it inherits the non-compliance that made deriving it necessary (`docs/mined/ECC-SKILLS.md:648`) |

The failure this catches is subtler than *"the model decided something it should not have"*: it is a
prompt asking for *"an appropriate number of packages"* and getting a plausible one. Plausible is not
reproducible, and the number was computable.

Everything else is model side: **naming**, prose a person will read, resolving genuine ambiguity in
what someone said, and judging natural-language similarity.

**What a rule guarantees, and a prompt does not.** Reproducibility. Zero marginal cost. A failure
that carries an identifier. A test. And — Layer A's docstring says it best — being *"impossible for
a model to talk its way past."*

**Two boundary invariants.**

- **Additive only.** A model may *add* — a warning, a suggestion, a question. It may never *prune*
  a rule, a required field, or an error-severity check. (Same rule as
  `.claude/skills/ontoagent-elicitation`; it is what keeps the gate a gate.)
- **No model output is a gate input until a rule has checked it.** Grounding is per-fact and comes
  from Layer A's metadata, not from the model's claim about itself (`layerb/whole.py:125,140,148`).

**The architectural disqualifier this produces.** Any architecture in which the model decides
**sequencing, sufficiency, or validation** is disqualified for Scio regardless of what it buys.
That is not a refactor of this system; it is a different and worse one. Apply this at step 3 of §3,
alongside the table's disqualifiers.

**The failure mode to watch for.** The eleven rules quietly becoming eleven bullet points in a
prompt. They then stop being guarantees and start being suggestions, and nothing in the test suite
notices.

---

## 5 · Tenancy — the decision Scio makes twice

**Do not conflate them.** Scio's own tenancy and the generated app's tenancy are separate
decisions with separate blast radii.

| Model | Buys | Disqualified when |
|---|---|---|
| **Pool** — shared infrastructure, tenant key on every row | highest density, lowest cost, one thing to operate, one place to enforce | a tenant needs its own keys, its own backup policy, its own region, or its own schema; or a hard service limit is the ceiling |
| **Silo** — a full stack per tenant | strongest isolation; per-tenant compliance and recovery | you cannot automate onboarding, migration and offboarding — manual silo management stops scaling almost immediately |
| **Bridge** — pooled tier plus siloed tier | the honest answer for most real SaaS: pool by default, silo the tenants who pay for it | you have not decided which tier a new tenant lands in, or the two tiers diverge into two products |

**Scio is pool, decided.** ADR-0009 scopes everything by `workspace_id` and enforces it in every
query. Any rebuild inherits this or reopens a closed class of bug. A single-tenant request is
answered with a bridge, not a migration (eval A5).

**The generated app is where the risk actually is.** ADR-0011 fixes Supabase, so isolation lands on
PostgreSQL RLS. Azure's guidance is blunt about the cost: RLS requires the user's and tenant's
identity to be propagated into every query and is *"complex to design, implement, test, and
maintain"*, which is why many multitenant solutions skip it. Skipping it is precisely
CVE-2025-48757: insufficient RLS in generated projects, **CVSS v3.1 9.3 Critical**, supplier
disputed.

**And today Scio cannot express a policy.** `Table.row_level_security: bool` (`architecture.py:49`),
`SecurityPosture.row_level_security: bool` (`architecture.py:144`), `Permission.scope: str = "own"`
(`architecture.py:83`) — three booleans and a two-valued string. The architecture asserts isolation
and specifies none of it. That is `docs/next/LAYER-B-UNDERSTANDING.md` §3.5 / proposal **B-3**, and
it is the one item in this skill with a CVSS score attached to not doing it.

---

## 5a · When a security decision is required — the seven triggers

Added 2026-08-26. Taken verbatim from ECC's `security-review`, verdicted in
`docs/mined/ECC-SKILLS.md:656` as *"better than anything we have written down"* and *"also Layer G's
surface"*. It answers a question §5 does not: **not which isolation model, but when the question has
to be asked at all.**

If any of these appears in what is being designed or built, a security decision exists and must be
recorded. Absence of all seven is a legitimate answer and should be stated, not left silent.

| # | Trigger | Where Scio can see it without asking |
|---|---|---|
| 1 | **Authentication or authorisation** | `AuthAccess{mode, roles, permissions}`; any `Permission` in the slice |
| 2 | **User input** | any `Operation` whose `inputs` are non-empty; any screen with a create or update operation |
| 3 | **A database query** | every `Table` and every operation touching one — which is nearly every feature package |
| 4 | **A filesystem path** | storage operations; anything writing outside the package's file plan |
| 5 | **An external call** | `Connector` nodes; the connector package kind |
| 6 | **Cryptography** | rare in a derived architecture, and its rarity is the reason a rolled-your-own instance must surface |
| 7 | **Secrets** | environment variables in the file plan; anything the `_SECRET_PATTERNS` scan is aimed at |

**Why this is a skill entry and not a Playbook line.** Six of the seven are **computable from a
package's architecture slice**, so this is a routing rule for *which packages need a security
criterion and which gates must run on them* — §4's fourth test applied to ceremony. A Playbook
sentence saying "think about security" would fail
`.claude/skills/playbook-admission` §2 criteria 2 and 3 on its first reading.

**The limit.** Seven triggers is a checklist, not a threat model. It tells you a decision exists; it
does not tell you the decision. STRIDE, an attack tree, or the tenancy table above is what answers
that, and a run that treats a completed checklist as a completed review has misused this section.

---

## 6 · Architecture for LLM and agentic systems

The field where the least is settled and the most is asserted. Treat everything here as
**vocabulary**, the way ATAM is vocabulary — useful for naming a decision, not evidence for one.

**What is measured.**

- **Multi-agent cost.** Anthropic's own eval: agents use ~4× the tokens of chat, multi-agent ~15×,
  and token usage explains **80% of performance variance** ([2025-06-13](https://www.anthropic.com/engineering/multi-agent-research-system)).
  Their stated disqualifier is the useful part: multi-agent is wrong when all agents need the same
  context or the subtasks are tightly coupled — and "most coding tasks involve fewer truly
  parallelizable tasks than research."
- **Multi-agent failure.** MAST: 1,600+ annotated traces across 7 frameworks, 14 failure modes in 3
  categories — system design, inter-agent misalignment, task verification — inter-annotator
  κ = 0.88 ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657), v3 2025-10-26). Agreement on a
  taxonomy, not causation.

**What is asserted.**

- Anthropic's five workflow patterns — prompt chaining, routing, parallelisation,
  orchestrator-workers, evaluator-optimiser — plus the autonomous agent, with the rule *"add
  complexity only when it demonstrably improves outcomes"* ([2024-12-19](https://www.anthropic.com/engineering/building-effective-agents)).
  Engineering guidance, no numbers.
- Context engineering as four techniques — compaction, structured note-taking, sub-agents,
  just-in-time retrieval ([2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
  Retrieval architecture reduces to one question here: *what is the smallest set of tokens that
  makes this decision correct*, which is `docs/next/LAYER-B-UNDERSTANDING.md` §6 exactly.
- *Architectural Design Decisions in AI Agent Harnesses* ([arXiv 2604.18071](https://arxiv.org/abs/2604.18071),
  2026-04-20) reads 70 projects and reports five recurring dimensions — subagent architecture,
  context management, tool systems, safety mechanisms, orchestration — and five patterns.
  **Descriptive: it records what people built, not what worked.**
- *Harnessing Agent Skills* ([arXiv 2606.20631](https://arxiv.org/abs/2606.20631), 2026-05-29):
  ten patterns and a four-layer reference architecture — supply chain, mediation, execution
  control, evidence and feedback — instantiated across 8 systems. Relevant to `docs/next/SKILLS.md`
  because it names the supply-chain layer the vendored-`graphify` drift lives in.
- The systematic review of LLMs in software architecture found simple prompting dominant across
  18 articles, and conformance checking and architecture-to-code among the **least explored**
  ([arXiv 2505.16697](https://arxiv.org/abs/2505.16697), 2025-05-22).

**Observability is not standardised yet.** Checked 2026-08-26: OpenTelemetry's GenAI semantic
conventions are **still Development**, were moved out of the main semconv repo into
[semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai), and
that repo has no tagged release. Instrument to the attribute names by all means; **do not claim
standards compliance and do not build a contract on them.**

**Evaluation.** An LLM judge is a fragile instrument, not a neutral one — position bias,
verbosity bias and self-preference are all documented. Any agent-pipeline architecture that puts a
model judge on the *gate* rather than beside it has moved a guarantee to the model side (§4).

---

## 7 · The output contract

An architecture produced by this skill is not done until it carries all nine. Items 3, 4 and 5 are
the ones people skip, and they are the ones the next stage cannot act without.

1. **Components** — each with a one-sentence responsibility. Keep the top level to roughly a dozen;
   past that you are drawing, not deciding.
2. **Edges** — directed, each labelled with *what crosses it*. Contracts and interfaces, never
   code: invariant 4 is enforced by a test asserting `"tables: booking" in prompt` and
   `"CREATE TABLE" not in prompt`.
3. **The quality attributes it optimises** — one to three, each an ISO/IEC 25010:2023 name plus a
   scenario with a response measure.
4. **What it explicitly sacrifices** — a named attribute from the same list. Not "some complexity".
5. **The elimination record** — for each rejected candidate, the disqualifier that fired.
6. **Reversibility** — what undoing this costs, in one sentence.
7. **A fitness function per structural claim**, or the sentence "this claim is not checkable"
   written out.
8. **The ADR** — numbered, in `docs/decisions/`, with status, superseding rather than editing.
9. **For the product's derived architecture, additionally:** every node carries `source_field` so a
   change upstream traces to what it touches, and the assumption list comes from Layer A's
   metadata, never from the model's self-report.

**Render, never invent a language.** The data half projects to
[DBML](https://dbml.dbdiagram.io/home/); operations and permissions borrow
[JHipster JDL](https://www.jhipster.tech/jdl/intro/)'s grammar shape. **One direction only** — the
moment the text is an input it needs a parser, an error story, an editor story and a version story
(`docs/next/LAYER-B-UNDERSTANDING.md` §4.2, proposal B-9).

---

## 8 · What exists, so we build only what does not

| Thing | Verdict |
|---|---|
| **ISO/IEC 25010:2023** | **adopt the vocabulary.** Free, and it stops attribute names being invented per decision |
| **ATAM / CBAM** (SEI) | **adopt the vocabulary only** — utility tree, sensitivity point, trade-off point. Full ATAM is a multi-day stakeholder workshop; using three of its words is not doing an ATAM and must never be described as one |
| **arc42 v9** ([arc42.org](https://arc42.org/)) | **adopt the section skeleton** for architecture documents. Free, process-agnostic |
| **C4 / Structurizr DSL**, official MCP at `mcp.structurizr.com` ([docs](https://docs.structurizr.com/ai/mcp)) — free, open source, DSL validate/parse plus Mermaid and PlantUML export | **use for Scio's own container-level diagrams. Wrong level for the product**, which models entities, operations, screens and permissions *inside one container* |
| **MADR 4.0.0** (2024-09-17) | already effectively ours — keep this repo's template; borrow MADR's status vocabulary |
| **log4brains / adr-tools** | **skip.** Publishing ADRs as a static site is not a problem we have |
| **ArchUnit, dependency-cruiser** | **adopt when there is code** — this is how §3 step 9 gets teeth. `graph-guard` already covers layer-boundary drift in this repo |
| **`gauravs19/enterprise-architecture-skill`** (MIT, ~9 stars, C4 + ArchiMate + TOGAF ADM + arc42) | **read the Structurizr half, skip the TOGAF half.** Substantive — reference docs, templates, a linter, eval cases — but enterprise-framework shaped, and TOGAF ADM is an order of magnitude too heavy here |
| **The large skill marketplaces** (hundreds to thousands of listings) | **marketing.** `docs/next/SKILLS.md` has this right: volume is not the gap, **provenance and evals are the gap** |
| **OTel GenAI semconv** | **track, do not depend.** Still Development as of 2026-08-26 |
| **`.claude/skills/design-rule-hierarchy`** | **call it, do not restate it.** Package boundaries, antichains and propagation cost live there |
| **`.claude/skills/reflexion-conformance`** | **call it** for "does the code match the architecture" — converge / diverge / absent, not pass/fail |
| **`.claude/skills/change-impact-analysis`** | **call it** for blast radius. Do not invent an impact algorithm inside an architecture decision |

---

## 9 · Limits — what the sources support versus what this procedure assumes

**The disqualifiers are practitioner knowledge, not experiment.** No controlled trial compares
architecture styles. Richards and Ford are structured experience; the Azure "when not to use" lists
are engineering guidance from one cloud vendor with a commercial interest in its own services.
Fowler's MonolithFirst says so about itself — it generalises from *"almost all the successful
microservice stories"*, which is an observation over anecdotes. **These are strong heuristics with
known provenance. Do not cite them as measurements.**

**ISO/IEC 25010:2023 is a vocabulary, not a method.** It tells you what to name and how to
subdivide it. It does not tell you how to measure any of it, and it will not settle a tie.

**ATAM and CBAM are being used far below their design point.** They are stakeholder workshops with
elicitation and scoring steps. We take three nouns from them. That is legitimate and it is also
much less than the method.

**The LLM-architecture material is the weakest link and should be read as opinion.** The systematic
review covers 18 articles and finds mostly simple prompting; the harness study is a descriptive
reading of 70 repositories; the skills reference architecture instantiates across 8 systems. **None
of them measures whether adopting a pattern improves an outcome.** The two real numbers here —
Anthropic's token multipliers and MAST's taxonomy — are on their data, their models, their
frameworks, not ours. Anyone quoting "15×" or "80% of variance" without that sentence is selling a
number they did not earn.

**Two books are paywalled.** *Fundamentals of Software Architecture* 2nd ed. (April 2025) and
*Software Architecture Patterns* 2nd ed. (August 2022) were confirmed by publisher listing only;
the pattern-level characterisations attributed to them here (service-based at 4–12 services on one
database, space-based collision probability) come from secondary summaries and were **not verified
against the text**. Flagged rather than asserted.

**CVE-2025-48757 is disputed by the supplier**, who argues isolation is the customer's
responsibility. Cite the CVE and cite the dispute; the architectural point — that a deterministic
rule over a typed architecture would have caught it — stands either way.

**What this procedure assumes and cannot show.** That an architecture chosen this way is better
than one chosen by taste. **Unmeasured, and probably unmeasurable at our scale.** The narrower
claim, which is defensible: it produces an architecture whose disqualifiers, sacrifices, elimination
record and ADR are written down, and *that* is checkable — by eval A7 below, and by anyone reading
the ADR in a year.

---

## 10 · Eval

Runnable as prompts. **The reason is the test, not the verdict** — a run that reaches the right
answer for the wrong reason fails.

| # | Case | Expected | What it proves |
|---|---|---|---|
| **A1** | "Let's build the rebuild as microservices — one service per layer." Single-tenant, pre-revenue, one team. | **Rejected at §3 step 4** on owner count, and at step 3 on Fowler's three prerequisites. Answer: **service-based** (which ADR-0006 already is) or modular monolith. | the fashionable-pattern rejection. A run that accepts it citing "scalability" fails twice: scalability was never in the top three, and no scenario gave it a response measure |
| **A2** | "Drop Clerk for a self-hosted OIDC provider — it's cheaper and it removes a vendor." | The skill demands the argument **engage ADR-0008's stated reason** (a deliberate exception to Azure-native, behind our own interface). Cost alone does not reach it. Outcome: **keep**, recorded with its reason. | a settled ADR beats a better-looking alternative. A run that supersedes ADR-0008 without addressing why it was made fails |
| **A3** | "Event-source the build history so we can replay any build." | **Rejected.** Azure's own list disqualifies MVPs and straightforward CRUD; and **git is already the append-only log** (ADR-0017: promotion, never regeneration). The right answer names the existing mechanism instead of adding one. | the correct answer is often "we already have this". A run that designs an event store fails |
| **A4** | "Let the model decide which validation rules apply to this app — some don't fit every app kind." | **Refused.** Sufficiency and validation are rule side (§4). A model may add a warning; it may never remove one of the ten error-severity rules. | the additive-only boundary. This is the invariant most likely to be lost in a rebuild |
| **A5** | An enterprise prospect demands their data in a dedicated database. | **Bridge**: silo that tenant over the pool default. **Not** a global move to database-per-tenant. Must name the sacrifice — operational uniformity, cross-tenant reporting, and ADR-0009's single enforcement point. | tenancy is a per-tenant decision, not a platform rewrite. A run that migrates everyone fails |
| **A6** | Choosing the shape of Layer B's rebuild. | **Layered pipeline, unchanged** — derive → validate → model. If the run proposes an event bus between layers, it fails: no top-three attribute requires it, and the synchronous ordering *is* the asset (`service.py:50-57`). | "the boring one" as a real outcome, with its condition checked rather than felt |
| **A7** | Take any architecture this skill produced and check it against §7. | All nine present. **Missing item 4 — what it sacrifices — is a failure, not a nit.** | the output contract is enforceable or it is decoration |
| **A8** | *(negative)* A pattern proposed with the buys column filled in and no disqualifier check. | **Rejected before comparison begins.** | the procedure fails closed. If A8 passes, §3 has become advice |

**Pass condition:** A1–A6 reach the stated outcome *for the stated reason*; A7 and A8 fail closed.
A skill that answers A2 by agreeing with whoever asked last has stopped being this skill.

---

## 11 · When this skill is the wrong tool

- **Package boundaries, granularity, "is this decomposition modular?"** → `design-rule-hierarchy`
  (layers, antichains, propagation cost). This skill chooses a style; that one measures a structure.
- **"Does the code match the architecture?"** → `reflexion-conformance`.
- **"What does this change touch?"** → `change-impact-analysis`.
- **"How is the catalog searched?"** → `contract-retrieval`. **"Is this the same component?"** →
  `reuse-classification`.
- **"Should this rule be prose in a build prompt, and what does it cost?"** → `playbook-admission`.
  This skill decides which *side* a decision sits on; that one decides which *artifact* carries it.
- **"This validator says it is clean — is it?"** → `validation-evidence`. **"What may a gate
  conclude?"** → `gate-verdicts`.
- **How it looks** → `app-design`. **What the old system does** → `as-built`.
- **A pure product question.** Whether the wedge is founders or non-technical owners is upstream of
  every architecture decision (`01-DECISIONS.md`). Do not settle it with a pattern.
