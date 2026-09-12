# 01 · Decisions — the 20 ADRs of `hello-world`

Where the *why* is recorded. Read this before concluding that something in the old system is
badly shaped: several oddities are deliberate and reasoned.

Source: `docs/decisions/` in hello-world, 1,114 lines across 20 records. Statuses below are
verbatim, not paraphrased.

## The register

| # | Decides | Status | Layer |
|---|---|---|---|
| 0001 | Wedge and differentiator | Accepted | — |
| 0002 | Name: Scio, Latin *I know* | Accepted (working name, trademark pending) | — |
| 0003 | Visual identity: drafting table / blueprint | Accepted | — |
| 0004 | Cloud: Azure | Accepted | infra |
| 0005 | Sandbox: ACA dynamic sessions, behind a swappable interface | Accepted (feature in preview) | E |
| 0006 | NestJS backend + separate Python FastAPI engine | Accepted | all |
| 0007 | PostgreSQL; JSONB for spec/whole; pgvector for RAG | Accepted | G |
| 0008 | Auth: Clerk, behind own interface | Accepted (deliberate exception to Azure-native) | G |
| 0009 | Data model; everything scoped by `workspace_id`; code lives in git | Accepted | G |
| 0010 | Intake schema — six core fields, metadata, buildable-enough gate | Accepted | **A** |
| 0011 | Generated apps: Next.js + TS + Tailwind + Supabase, fixed | Accepted | E |
| 0012 | Layer B — the whole, plus a machine-readable architecture graph | Accepted | **B** |
| 0013 | Layer C — dependency-ordered, contract-bearing build packages | Accepted | **C** |
| 0014 | Component library — match every package before generating | Accepted | **D** |
| 0015 | Design conflicts answered inline; two answers only | Accepted | F |
| 0016 | Library grows from real builds; ids `category.seqno.version` | Accepted | D |
| 0017 | "Build it" **promotes** the design workspace, never regenerates | Accepted | F |
| 0018 | What Ship / Refine / Settings are | **Proposed** — needs the planning chat | F |
| 0019 | What deletion deletes | **Proposed** — retention windows unsettled | G |
| 0020 | Builds are jobs, not requests | **Partly implemented** — points 1, 4, 5 built; queue not | E |

**Three are not settled.** 0018 and 0019 are proposals awaiting a decision; 0020 is half-built.
Anything downstream of those is standing on an open question.

## The five that carry the most weight

**0013 — Layer C** is where your build contracts already exist. Each package carries *"goal;
the architecture slice it owns; dependencies (prior packages' interfaces/contracts, not their
full code); the relevant 'why' slice of the whole; house rules + canonical vocabulary."* That is
the contract-with-neighbours idea, decided and written down.

**0014 — the library** matches every package against a catalog of curated parts *between* B and
C. Entries are *"contracts with files attached."* This is what makes builds cheap, and it
explains the `D → E` edge being the heaviest in the graph.

**0017 — promotion, not regeneration.** "Build it" ships the files the user shaped, with git
history intact. No codegen, no repair loop. A strong decision and easy to break by accident.

**0009 — `workspace_id` everywhere.** Tenant isolation lives in the data layer and is enforced
in every query. Any rebuild inherits this or reintroduces a class of bug the old system closed.

**0011 — the generated stack is fixed and opinionated.** Next.js + TS + Tailwind + Supabase.
Note this is the *output* stack, not Scio's own.

## A tension worth resolving before rebuilding intake

**ADR-0001 defines the wedge as** *"founders and small teams building software they intend to
run and grow — not throwaway MVPs"*, and the differentiator as *"developer-grade output —
clean, reviewable, tested, secure-by-default, git-native code that the user owns, with a smooth
handoff to a developer."*

That is a **developer-adjacent** audience. It is not the same as "someone who cannot write
software," and the difference lands directly on Layer A.

The intake schema asks for `entities` — *"the core things the app manages"* — and for
`data_ownership_sensitivity`. For a founder who has seen a database, those are natural. For a
restaurant owner, they are not. So the schema is not obviously mis-aimed; it is aimed at
ADR-0001's wedge.

**Which means the question is upstream of intake:** is the wedge still founders and small
teams? If yes, the existing field vocabulary is defensible and the criticism of it is wrong. If
the wedge has moved toward people with no technical vocabulary at all, then ADR-0001 needs
superseding *first*, and Layer A follows from that — not the other way round.

Do not redesign intake without answering this. It decides what "asking the right question"
even means.

## Convention

One decision per file, numbered sequentially, with status. Copy `0000-adr-template.md`.
Supersede rather than edit: a changed decision gets a new number and the old one is marked.
