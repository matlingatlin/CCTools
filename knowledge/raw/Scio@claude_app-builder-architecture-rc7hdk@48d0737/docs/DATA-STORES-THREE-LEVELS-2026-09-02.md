# Data stores at three levels — what needs a database, and what does not

**Date:** 2026-09-02. **Status:** proposal; the decision is ADR-0012. This is the *data* question,
distinct from the knowledge question answered in `TALENTS-CRITICAL-SET-2026-09-02.md` §5 and
ADR-0011.

The user's question, turned round: is any particular kind of database needed **now while we
build**, **in Scio itself**, or **in the apps Scio builds**? Three different answers.

---

## 1 · While we build — a database, not a server

**Corrected 2026-09-02, later the same day.** The first version of this section said "none",
and that was the wrong word. Level 1 has a database: `scio.db`, a SQLite store with full-text
search over the corpus, plus the code graph and git. What it does not have, and does not need, is
a *server*. The knowledge the user names — how to work with Claude, our skills and agents, what we
decided — is stored; the question is whether it is stored *in one place, queryable, and current*.
Measured today, it is not, on three counts:

| What `scio.db` holds today | Count |
|---|---|
| Scio's skills (`.claude/skills`) | 555 sections, 532 KB |
| Scio's evals, mined, forward view, as-built, other docs | 1,331 sections |
| Scio's decisions | 15 sections, 7 KB |
| skills-repo's 26 verified notes on Claude Code mechanics (hooks, subagents, plugins, memory, skill anatomy, eval methodology), its BRAIN, LESSONS, CURATION-LESSONS, DATA contract and ledgers — 158 KB | **0** |
| hello-world's multi-agent branch (nine agents, 24 skills) | **0** |
| the seven documents and twelve ADRs written today | **0 until the next session start** |

Three gaps, each with a cheap fix and none needing a server:

1. **One repo of three.** The store indexes Scio only. The material most directly about "how to
   work with Claude" lives in skills-repo's `knowledge/notes/` and is unreachable from a Scio
   session except by opening files — the failure the store exists to prevent. Fix: `scio-db.py
   build` takes the three repo roots and indexes skills-repo's notes, skills, BRAIN and ledgers
   with the same section-level chunking; provenance frontmatter (`sources`, `fetched`, `status`)
   becomes columns.
2. **Rebuilt only at session start.** The graph gets a `post-commit` rebuild (ADR-0001); the store
   does not, so anything written in a session is invisible to `find` until the next session. Fix:
   the same hook rebuilds `scio.db` (measured today: the full build takes seconds and no model
   call).
3. **Nothing counts queries.** ADR-0001 names "nobody queries it" as its likeliest failure and it
   is unmeasured. Fix: `find`/`read`/`explain` append one line to a ledger; the count is read at
   `/checkpoint`.

What stays true: the store is **rebuilt from git, never a source of truth**, so a container can
be reclaimed without losing anything, and it is SQLite in a file, so there is no service to run.
Store 2 in ADR-0011 is this store; the fixes above are what "made whole" means there.

---

## 2 · In Scio — one Postgres, one object store, one git host; no vector, no graph database, no broker

Scio is multi-tenant and holds money-bearing state, so it needs a real relational database. The
predecessor's ADR-0007 chose Postgres with JSONB for the spec and pgvector for retrieval; the
as-built record shows where that went wrong, and none of it argues against Postgres:

| What the predecessor did | What the record found | What Scio does |
|---|---|---|
| `workspace_id` "everywhere" | true of 6 of 14 models; one live cross-tenant read (F-03) through an unscoped `BuildVersion` | **every table scoped or explicitly labelled unscoped; RLS on all of them** as the backstop under the application scope (`next/LAYER-G` G-3), a non-superuser application role, `SET LOCAL` inside a transaction, and a cross-tenant zero-rows test generated per policy |
| `vector` extension in migration 0001, index commented out "pending a fixed embedding dimension" | never used; vector on a deciding path rejected twice (D11, D19) | **no pgvector.** The library matches by `Contract`, exactly |
| `library_entry.contract_key` indexed on insert | the index is never queried; matching is a full-catalog scan in Python | the contract index is **the** lookup path (`contract-retrieval`: index, then verify) |
| spec as a mutable JSONB blob with `draft_*` caches | caches added because recomputing cost money on a page refresh | **event-sourced decisions, "active" computed** (A-33), versioned spec with `isLatest` and a parent chain, never a mutated assertion (A-35) |
| builds as stack frames in the API; `status = "queued"` unreachable; reaper on a heartbeat keepalives cannot advance | ADR-0020 points 2–3 unbuilt, "the largest single piece of work left" | **builds are rows in a jobs table** with a worker claiming via `SELECT … FOR UPDATE SKIP LOCKED`, heartbeat written on keepalives, a status the cancel check acts on. **No separate broker** until a measured queue depth says so |
| cost as unqualified `Decimal`, tokens nullable "because 0 would be a claim" | correct instinct, wrong types elsewhere | **append-only ledgers** per build (E-25) and per workspace, with the reduction key including the tenant (G-3), `numeric` for money, `timestamptz`, `bigint` ids (BC-A12) |
| `DATABASE_URL` unset → "running without a database" and continue | the tenant boundary's storage absent in production | fail fast in production (G-10) |

Beside Postgres, two stores that are not databases:

- **Object storage** for what is large and immutable: evidence reports, build artefacts, sandbox
  snapshots, the level-3 package before it is committed. Keyed by content hash and producer
  identity (G-4).
- **A git host** for every app's repository, Scio-held by default and transferred on buy-out
  (ADR-0009). Git *is* the store for code, spec history as text, and the design window's versions
  — predecessor ADR-0009 already said "code lives in git" and ADR-0017 relies on it.

And one the harness needs: the SDK's `SessionStore` for build-session transcripts. Anthropic ships
adapters for S3, Redis and **Postgres**; Scio uses the Postgres one, so the list above does not
grow. Redis appears nowhere in the design until a measurement asks for it.

**What is explicitly not needed in Scio:** a vector database (rejected), a graph database
(graphify's files are the graph, ADR-0001; the `neo4j`/`falkordb` exports exist if a query ever
needs them and none does), an authorization service such as OpenFGA or SpiceDB (a second source of
truth for what a `WHERE` clause already says; revisit when tenancy grows a second relation —
`next/LAYER-G`), a message broker (SKIP LOCKED first).

Region (ADR-0010) applies here too: a workspace whose apps are region-bound has its Scio rows and
objects placed in that region, or the workspace is refused, not silently placed.

---

## 3 · In the apps Scio builds — Postgres with RLS, transferable with the repo

Predecessor ADR-0011 fixed the generated stack on Supabase — Postgres with row-level security and
auth. Lovable ships the same. The forward view rejects Cedar or any authorization service for the
generated app because the enforcement point is already Postgres RLS. Nothing in this review argues
against Postgres for the generated app; two things argue about *how*:

1. **The generated app has no backend today.** `grep supabase apps/api/src` returns nothing; the
   verified app runs against pglite, and the delivered app points at an unset URL. Gate 4b asserts
   row-level isolation against a database that is not the one the delivered app will talk to
   (`next/LAYER-E` §3.8). That is the gap Slice 1 closes: the interaction gates run against the
   **same database engine and the same RLS policies** the app ships with.
2. **Buy-out is a key transfer (ADR-0009), so the database must travel with the repo.** Schema
   and migrations are files in the repo already. Data is not. The app therefore talks to Postgres
   through **one client shape that works both hosted in Scio and after transfer**, and the
   transfer includes a dump-and-restore of the app's database into the customer's own Postgres or
   Supabase project, verified by running the app's own cross-tenant zero-rows test against the
   restored copy. Whether the hosted form is one Postgres per app or Supabase projects under
   Scio's organisation is a Slice 1 architecture-pass decision with a dated scan of Supabase's
   project-transfer and region options; the constraint is fixed here, the vendor is not.

Per app, the database carries what intake decided (ADR-0010): its **region**, its sensitivity
labels as `COMMENT ON COLUMN … 'PII: …'` surviving into the schema (BC-A13), and the zero-rows
test beside every policy (BC-A14). An app that stores no data gets no database, and the evidence
report says so.

Other stores appear only when the app kind needs them: file uploads → the same object store
pattern, scoped per app; search → Postgres full-text first, a search service only when measured.
Slice 1's single app kind needs relational only.

---

## 4 · In one table

| Level | Relational | Objects | Code | Vector | Graph DB | Broker |
|---|---|---|---|---|---|---|
| 1 · building | `scio.db` (SQLite, rebuilt from git, one index over three repos) | none | git | no | no (files) | no |
| 2 · Scio | one Postgres, RLS on every table, event-sourced spec, jobs via SKIP LOCKED, append-only ledgers, SDK `SessionStore` | one, content-addressed | git host, Scio-held, transferable | **no** | **no** | **not yet** |
| 3 · generated app | Postgres with RLS, region and labels from intake, dump-and-restore on buy-out | when the app kind needs it | the app's own repo | no | no (graphify files, ADR-0001) | no |

## Sources

- `docs/as-built/LAYER-G-CROSS-CUTTING.md` §6 and *The 12 migrations*; `docs/next/LAYER-G-CROSS-CUTTING.md` §3.4, G-3, G-10, the OpenFGA/Cedar rows; `docs/next/LAYER-E-BUILD.md` §3.5, §3.8; `docs/as-built/01-DECISIONS.md` (predecessor ADR-0007, 0009, 0011, 0020); findings A-33, A-35, E-25, G-3, G-4, BC-A12, BC-A13, BC-A14, D11, D19
- Agent SDK hosting (`SessionStore` adapters: S3, Redis, Postgres), fetched 2026-09-02
