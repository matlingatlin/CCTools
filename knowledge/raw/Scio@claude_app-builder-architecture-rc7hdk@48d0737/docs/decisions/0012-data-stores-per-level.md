# ADR-0012 · Data stores per level: SQLite from git while building, one Postgres in Scio, transferable Postgres in every generated app

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** E (platform) per ADR-0005; C and D for the generated app's database
**Supersedes / relates to:** replaces predecessor ADR-0007 (Postgres + JSONB + pgvector) for the rebuild; keeps predecessor ADR-0009 (code lives in git) and ADR-0011 (generated stack on Postgres/Supabase); relates to ADR-0009, ADR-0010, ADR-0011

## Context

Three levels, three different data questions (`docs/DATA-STORES-THREE-LEVELS-2026-09-02.md`).
Level 1 already runs on files in git and an index rebuilt per session. Level 2 in the predecessor
is Postgres, and its defects are all *how*, not *whether*: tenancy true of 6 of 14 models with one
live cross-tenant read; a `vector` extension installed and never used; a contract index written
and never queried; a mutable spec blob with money-saving caches bolted on; builds as stack frames
with an unreachable queue state, the largest piece of work the predecessor left. Level 3 in the
predecessor has no backend wired at all: gate 4b proves isolation against pglite while the
delivered app points at an unset Supabase URL. ADR-0009 makes buy-out a key transfer, so an
app's data must move with its repo; ADR-0010 makes region and sensitivity intake answers.

## Decision

**Level 1: a database, not a server.** `scio.db` — SQLite with full-text search, rebuilt from
the files of **all three repos** on session start and on every commit, carrying each section's
provenance (source, fetch date, verified status, asserted or observed) as columns and counting
its own queries — beside the code graph files and git. It is never a source of truth: a store not
in git does not exist. (Corrected 2026-09-02 from "no database"; measured the same day, the store
indexed one repo of three and nothing written since session start.)

**Level 2: one Postgres, one object store, one git host.** Postgres with row-level security on
every table under the application scope, a non-superuser role, `SET LOCAL` in a transaction, a
generated cross-tenant zero-rows test per policy; the spec as event-sourced decisions with
"active" computed and a versioned chain, never a mutated assertion; builds as rows claimed with
`SELECT … FOR UPDATE SKIP LOCKED`, heartbeat advanced by keepalives; append-only ledgers per build
and per workspace with the tenant in the reduction key; `numeric` money, `timestamptz`, `bigint`
ids; fail fast without a database in production; the SDK's Postgres `SessionStore`. Content-
addressed object storage for evidence, artefacts and snapshots. A Scio-held git host per app,
transferable. **No pgvector, no graph database, no authorization service, no broker** until a
measurement asks for one; region-bound workspaces placed in region or refused.

**Level 3: Postgres with RLS in every generated app that stores data**, through one client shape
that runs both hosted in Scio and after transfer; region and sensitivity labels from intake in the
schema; the zero-rows test beside every policy; the interaction gates run against the same engine
and policies the app ships with; buy-out includes dump-and-restore verified by the app's own
isolation test. Per-app Postgres versus Supabase projects under Scio's organisation is decided in
Slice 1's architecture pass with a dated scan; the transferability constraint is decided here.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Carry predecessor ADR-0007 as is | Carries pgvector nobody uses and the JSONB-blob spec the caches were bolted onto |
| A vector database for the library or the spec | Rejected three times on the same ground: `Contract` is decidable, similarity is not (ADR-0001, D11, D19) |
| A message broker for builds now | SKIP LOCKED on the jobs table is the standard first answer and adds no service; a broker returns with a measured queue depth |
| OpenFGA / SpiceDB for tenancy | A second source of truth for an answer a `WHERE` clause gives; revisit when tenancy grows a second relation (`next/LAYER-G`) |
| Schema-per-tenant or database-per-tenant in Scio | Operational weight the reviews' tenancy guidance reserves for a later stage; RLS shared-schema is the mainstream answer now |
| A NoSQL document store for the spec | The spec is exactly the thing that needs a versioned chain and provenance per field, which is relational |

## Consequences

**What this buys.** One relational engine at levels 2 and 3, so the tenancy skill, the RLS traps
and the zero-rows test are written once. Level 1 stays serverless. Buy-out is credible because the
data path is designed for transfer from the first build.

**What it costs.** RLS on every Scio table is a migration per table plus a session-variable
discipline. Dump-and-restore on transfer is a tested path, not a feature toggle. Region-aware
placement from Slice 1.

**What it forecloses.** Similarity-based matching anywhere on a deciding path; running Scio
without a database in any production-like environment.

## How we will know it was wrong

Queue depth or worker contention on the jobs table exceeds what SKIP LOCKED serves, which brings
the broker back with a number; a tenancy relation appears that RLS cannot express in a `WHERE`
clause, which brings OpenFGA back; or a buy-out's dump-and-restore fails the app's own isolation
test, which means the "one client shape" promise was not kept.
