# Layer G · Cross-cutting — as built

Data, auth, tenancy, cost/metering, streaming. 37 files, 1,984 lines; 38 of the API's
135 tests are owned here and the rest lean on it — all 135 passing 2026-08-26.

Governed by **ADR-0007** (Postgres), **ADR-0008** (Clerk behind an interface),
**ADR-0009** (data model), **ADR-0019** (deletion and retention — still *Proposed*),
and `docs/DATA-MODEL.md`.

---

## 1 · Purpose

Everything the other six layers assume and none of them own: who the caller is, which
tenant's rows they may touch, what their work costs, what they are allowed to spend, and
how a build that takes forty minutes reaches a browser that expects a response.

ADR-0009 states the load-bearing claim: *"**Everything is scoped by `workspace_id`** —
tenant isolation lives in the data layer and is enforced in every query and in
authorization."* Heading 4 tests that sentence; heading 6 says where it holds and where
it does not.

## 2 · Public surface

**Auth** (`apps/api/src/auth/`)

| Route | Does |
|---|---|
| `GET /auth/status` | authenticated caller's user id |
| `POST /auth/webhooks/clerk` | Clerk `user.created` / `user.deleted` — `@Public()`, 202, logs only |

Everything else is a global guard rather than a route. `AuthGuard`
(`auth/auth.guard.ts:20`) is bound as `APP_GUARD` in `modules/auth/auth.module.ts:30`:
bearer token → `IdentityVerifier.verify` → `ProvisioningService.getOrCreate` → attach
`AuthContext{userId, workspaceId, externalId, email}`. `@Public()` exempts health and the
webhook.

**Usage / metering** (`modules/usage/`)

| Route | Does |
|---|---|
| `GET /usage` | this workspace's usage events, newest first |
| `GET /usage/allowance` | `{ spent, cap, room }` for the current calendar month |

**Project CRUD** (`modules/project/`) — `GET/POST /projects`, `GET/PATCH/DELETE
/projects/:id`. The only fully-built consumer of the scoped client in this layer.

**Stubs that answer 501** — `GET /me`, `GET /workspace`, `GET /notifications`,
`PATCH /notifications/:id/read`. All four throw `NotImplementedException`
(`user.service.ts:11`, `workspace.service.ts:11`, `notification.service.ts:12,17`).

**Stream** — `GET /projects/:projectId/stream` (`modules/stream/stream.controller.ts:18`)
emits three heartbeats and completes. Its own docstring: *"Skeleton stage… The real stream
(phase 4/7) relays engine events for projects in the caller's workspace only."* The real
SSE machinery that builds actually use is `common/sse.ts`, not this controller.

All routes sit under `/v1`, `health` excluded (`main.ts:32`). Rate limiting is per
workspace, not per IP — `WorkspaceThrottlerGuard` (`common/workspace-throttler.guard.ts:18`),
120 requests/minute (`app.module.ts:29`).

## 3 · In and out

**In** — a bearer token, and a `workspaceId` the caller never supplies.

`IdentityVerifier` (`auth/identity-verifier.ts:13`) is the whole of ADR-0008's swappability:
*"Everything in the app depends on this interface — the concrete provider (Clerk today) is
an implementation detail."* Two implementations, chosen by env at module construction:

- `ClerkIdentityVerifier` — `verifyToken(token, { secretKey })` from `@clerk/backend`, with
  a fallback to `client.users.getUser(sub)` when the session token carries no email claim.
- `DevIdentityVerifier` — *"the bearer token IS the identity"*, `dev` → `dev@scio.local`,
  `dev:ada@example.com` → a second user with a second workspace. Bound only when
  `SCIO_DEV_AUTH` is set **and** `NODE_ENV !== "production"`; `devAuthEnabled` *throws*
  rather than honouring the flag in production (`dev-identity-verifier.ts:32-39`).

**Out** — a scoped Prisma client. `WorkspaceScope.forWorkspace(workspaceId)`
(`auth/workspace-scope.ts:91`) returns `prisma.$extends(...)` where
`applyWorkspaceScope(model, operation, args, workspaceId)` merges `workspaceId` into
`where` on reads and stamps it into `data` on creates.

Six models are scoped (`workspace-scope.ts:13-23`): `Project`, `UsageEvent`,
`Notification`, `AuditLog`, `User`, `BuildJob`. Those are exactly the six tables that
carry a `workspace_id` column. The other seven — `message`, `spec_version`,
`design_version`, `build_version`, `deployment`, `reference_asset`,
`reference_embedding` — have no such column at all and pass through untouched
(`workspace-scope.ts:62`).

**The metering ledger.** `usage_event` rows are written from four call sites, none of
them in this layer's own module:

| Site | Kind | Migration that made it expressible |
|---|---|---|
| `build.service.ts:776` (in `persist`) | `generation` | 0001 |
| `build.service.ts:305` (`meterSpend`, cancelled/failed) | `generation` | 0012 |
| `intake.service.ts:246` | `intake` | 0009 |
| `design.service.ts:151` (`meter`) | `preview` \| `design_change` | 0007 |

`UsageService` only reads them: `list`, `spentThisPeriod` (sum of `cost` since
`periodStart()` — the calendar month in UTC, `usage.service.ts:38-40`), and `allowance`.

**The cap.** `UsageService.cap()` reads `SCIO_WORKSPACE_PERIOD_CAP_USD`, defaulting to
**$50** (`usage.service.ts:32-35`). The docstring says why it is an env var rather than a
column: *"plans and pricing are an open product decision (B063), and inventing a per-plan
number here would be pretending that decision has been made. What must not wait for it is
having a ceiling at all."*

It is enforced in exactly one place — `BuildService.ensureCanStart`
(`build.service.ts:222-227`) — as a 409 naming both figures. `allowance()` returns rather
than throws, deliberately: *"the caller decides what refusing looks like, and the numbers
belong in the refusal — 'you have spent $50.12 of $50 this month' is actionable, 'over
budget' is not."*

**Streaming.** `openStream(res)` (`common/sse.ts:19`) sets the SSE headers including
`X-Accel-Buffering: no`, and writes a `: keep-alive` comment frame every 15s. The reason
is recorded rather than assumed: *"a build behind a forwarding proxy (a Codespace) died
with 'The build stopped — network error' while the build itself ran happily on."* The
interval is `unref`'d and cleared on `res.on("close")`, so a client leaving stops the
timer without stopping the build.

## 4 · Invariants

Taken from the tests. Test names are the evidence.

| Invariant | Test |
|---|---|
| A caller-supplied foreign `workspaceId` is overridden, not honoured | `overrides a caller-supplied foreign workspaceId (no cross-tenant reads)` |
| Creates are stamped, reads/updates/deletes are filtered | `stamps workspaceId into data on create` · `scopes updates and deletes too` |
| An operation the scope does not understand stops the request | `refuses upsert rather than passing it through` · `refuses createMany rather than passing it through` |
| No service reads rows through the unscoped client | `no service reads rows through the unscoped Prisma client` |
| The allow-list for that rule cannot rot | `the allow-list names files that exist` |
| A missing bearer token is 401, a `@Public()` route is not | `rejects a request without a bearer token (401)` · `lets @Public() routes through without a token` |
| First sight creates user + workspace in one transaction | `creates user + workspace in one transaction on first sight` |
| Dev auth cannot run in production | `refuses to run in production rather than accepting any token there` |
| A stale Clerk token does not silently become the dev user | `rejects a token that is not a dev token, rather than signing in as the default` |
| Cross-tenant reads/updates/deletes are 404, not 403 | `gets one project; cross-tenant reads are 404` · `soft-deletes; excluded from list; cross-tenant deletes are 404` |
| A workspace sees its own spend and nobody else's | `lists a workspace's own usage and nobody else's` |
| The period cap refuses a build before the engine is called | `refuses a build when the workspace has spent its month` (asserts `engine.seen` is empty) |
| A quiet stream is kept alive; a departed client stops the beat | `sends a comment frame while nothing else is happening` · `stops beating when the client leaves, without ending the build` |
| Every source file a clean clone needs is committed | `is committed under apps/api/src` |

Two of these deserve their mechanism written out.

**Fail-closed scoping.** `applyWorkspaceScope` ends in a `throw`, not a pass-through
(`workspace-scope.ts:76-79`). The comment records what it was fixing: `upsert` sat in
`CREATE_OPERATIONS` and *"quietly did nothing: an upsert has no top-level `data`… and it
is not a read either, so nothing was filtered."* Neither `upsert` nor `createMany` has a
caller today — *"which is exactly when to close a hole, rather than after one appears and
writes a row into the wrong tenant."*

**Non-throwing metering.** Every one of the four ledger writes is inside a `try/catch`
that logs and continues. `meterSpend`'s docstring is the clearest statement:
*"Never allowed to throw. A bookkeeping failure must not be the thing that decides whether
a user can build again."* `persist`'s: *"Written after the build_version and never allowed
to fail the build: a delivered app must not be undone by a bookkeeping error."* All four
also skip the write entirely when nothing was spent — asserted by
`a build that spent nothing writes no metering row` and `writes nothing when nothing was spent`.

The invariant holds. Its cost is stated honestly nowhere: a swallowed ledger write is
*unbilled spend*, and nothing counts how often it happens.

## 5 · Dependencies

**Up:** `F → G` 73 edges, `A → G` 62, `D → G` 21 (`graph/graph.json`). **Down:** `G → D`
2 — `engine.client.ts` and the library verification client.

`E → G` shows **0** edges, which is wrong: `build.service.ts:24` imports `UsageService`
and the module imports `WorkspaceScope`. The graph's TypeScript extraction produced no
outbound edges at all from `modules/build`, so the E-side count is missing rather than
absent. Treat the 73/62/21 as a floor.

Layer G depends on nothing above it. It depends on Postgres (ADR-0007) and on Clerk only
through `IdentityVerifier`.

One dependency is **not** in the graph and not in the migrations: the Python engine opens
the same `DATABASE_URL` and issues `CREATE TABLE IF NOT EXISTS library_category` /
`library_entry` at runtime (`apps/engine/src/scio_engine/library/store.py:135,144,216`).
Those two tables are real, shared, carry no `workspace_id`, and exist in no
`schema.prisma` and no migration. Anyone rebuilding the schema from
`apps/api/prisma/migrations/` gets a database the engine will silently extend on first
connect.

## 6 · State

### Solid — carry forward unchanged

- **`applyWorkspaceScope` as a pure function.** Exported for tests, nine cases covering it,
  and it *throws* on anything it does not recognise. The strongest thing in the layer.
- **`tenant-discipline.spec.ts`.** A test that reads the source tree and fails when a
  service reaches for `this.prisma.<model>`, with a three-entry allow-list that must name
  files that exist. It is honest about what it is: *"That is a habit, not a wall… until we
  [have RLS], this test is the fence."*
- **`IdentityVerifier`.** ADR-0008's swappability is real, not aspirational — two
  implementations, one symbol, one factory. Replacing Clerk with Entra touches one file.
- **Dev auth refusing production.** `devAuthEnabled` throws rather than warns
  (`dev-identity-verifier.ts:32-39`). The flag cannot be set by accident in a deployed
  environment.
- **404 rather than 403 across tenants.** Chosen and documented — *"missing → 404, not
  403, to avoid existence leaks"* (`project.service.ts:30`) — and tested on every
  cross-tenant path in four e2e files.
- **Non-throwing metering, with the skip-if-zero rule.** Four sites, one shape, tested
  both ways.
- **The period cap.** The right unit, added because the per-build ceiling was the wrong
  one on its own: *"it bounds one build and nothing bounds the number of builds."*
- **`openStream`.** Small, tested with fake timers, and fixed a real reported failure.
- **`tracked-sources.spec.ts`.** Reads `git ls-files` rather than the disk, because an
  unanchored `.gitignore` pattern silently excluded `src/modules/build` and
  `src/modules/workspace` twice.

### Wrong-shaped

- **ADR-0009's central claim is half true, and the half that is false is not marked.**
  *"Everything is scoped by `workspace_id`"* holds for 6 of 14 models. The other seven have
  no `workspace_id` column and are protected only by the convention that a service resolves
  the project through the scoped client first. `ARCHITECTURE.md` §7 says this accurately;
  ADR-0009 and `DATA-MODEL.md` do not.

- **One verified breach of that convention.** `BuildService.buildFor`
  (`build.service.ts:365-373`) queries `buildVersion.findFirst({ where: { projectId,
  idempotencyKey } })`. `BuildVersion` is not a scoped model, so the `workspaceId` argument
  selects the client and changes nothing about the query. Both callers run it *before* any
  project ownership check: `run` (`build.service.ts:515-523`) emits
  `replayOf(...)` and returns, and `ensureCanStart` (`build.service.ts:201-204`) returns
  early. A caller who supplies another tenant's `projectId` and the matching
  `Idempotency-Key` receives that build's `git_sha`, honest-status summary,
  `total_cost_usd` and `total_tokens`. It needs a guessed UUID plus a client-chosen key,
  so it is not trivially exploitable — but it is precisely the failure
  `tenant-discipline.spec.ts:15-19` warns about, and the fence does not catch it because
  the call goes through `this.client()`, not `this.prisma`.

- **The test doubles are stricter than production, which is why the suite missed it.**
  `FakeScope.forWorkspace` in `build.e2e.spec.ts` enforces `owns(where.projectId)` on
  every child-model operation (`build.e2e.spec.ts:51, 57, 64, 109, 172`). The
  real `WorkspaceScope` does not, and `workspace-scope.spec.ts:37` asserts that it does not
  (`leaves non-scoped models untouched`). So every cross-tenant e2e test passes for two
  reasons at once and cannot tell them apart. **The e2e suite cannot detect an unguarded
  child-row read.** Any future claim of tenant safety based on these tests is worth less
  than it looks.

- **Clerk webhook signatures are checked for presence, not verified.** The handler is a
  stub that logs (`webhook.controller.ts:20-62`). It refuses an unsigned POST when a
  secret is configured, and refuses everything in production when one is not — the comment
  explains the ordering: *"the moment somebody implements `user.deleted` cleanup behind an
  unverified signature, an anonymous request deletes accounts. So the refusal lands
  FIRST."* That reasoning is right, and the result is still not verification: with a secret
  set, `svix-signature: anything` passes. The TODO names the library —
  *"`svix` is the library"* — and **`svix` is not installed** (absent from
  `apps/api/package.json`; only `@clerk/backend` is there). There is no test for this
  controller.

- **`@CurrentWorkspace()` is typed `string` and returns `string | undefined`.**
  `auth-context.ts:24` returns `contextOf(ctx)?.workspaceId`; every controller declares
  `workspaceId: string`. On a `@Public()` route it would be `undefined`, and
  `where: { workspaceId: undefined }` is "no filter" in Prisma — an unscoped query. No
  `@Public()` route uses the decorator today, so this is latent, not live. It is one
  careless `@Public()` from being live, and the type system will not object.

- **`PROJECT_STATUSES` omits `spec_locked`** (`packages/shared/src/project.dto.ts:6`)
  while `ProjectStatus` includes it (`entities.ts:9`, schema enum, migration 0002). It
  drives both the `@IsIn` validator and the Swagger enum
  (`project.controller.ts:29,86`), so `PATCH /projects/:id` cannot set the status the spec
  gate actually uses.

- **`UsageKind` in shared is three values behind the database.**
  `entities.ts:14` has `generation | critique | sandbox | storage | other`; the Prisma enum
  also has `intake`, `preview`, `design_change`, all three actively written. The gap is
  hidden by a cast in `usage.service.ts:51`.

- **`/usage/allowance` has no consumer.** Nothing in `apps/app/src` calls `/usage` or
  `/usage/allowance`. `ARCHITECTURE.md` §7 promises *"estimate at the spec gate + live
  counter + pause at the cap"*; the pause exists, the counter is an endpoint nobody reads.
  A user learns their balance by being refused.

- **`build_version.cost_usd` is `DECIMAL(65,30)`** (migration 0005) while
  `build_job.cost_usd` is `DECIMAL(10,4)` (migration 0012) and `usage_event.amount`/`cost`
  are unqualified `Decimal`. Three precisions for one currency.

### Missing

- **Database-level tenant isolation.** No RLS on any of our own tables, acknowledged as
  such: *"Postgres RLS on our own tables is a backstop we do not have yet"*
  (`ARCHITECTURE.md` §7). Consequently no `workspace_id` on the seven child tables either.
- **A test that a cross-tenant child-row read is impossible** — as opposed to a test that
  the services currently don't attempt one.
- **`GET /me` and `GET /workspace`.** The two endpoints that tell a signed-in person who
  they are both 501. `MeResponse` and `WorkspaceResponse` exist in shared and are unused.
- **Five tables with no reader and no writer anywhere in the API**: `notification`,
  `audit_log`, `deployment`, `reference_asset`, `reference_embedding`. `audit_log` is the
  notable one — ADR-0009 lists it under security, `DATA-MODEL.md` calls it the security
  audit trail, and nothing has ever written a row.
- **Account deletion.** ADR-0019 is *Proposed*; `user.deleted` arrives at the webhook and
  is logged (`webhook.controller.ts:54-57`). Every foreign key in migration 0001 is
  `ON DELETE RESTRICT`, so a hard delete would need an explicit ordered cascade that does
  not exist.
- **Any count of swallowed ledger writes.** The catches log; nothing aggregates. Unbilled
  spend is invisible.
- **`library_category` / `library_entry` in the migration history.** See §5.

### Obsolete

- **`modules/stream/`** (3 files, 36 lines). The build stream it was a placeholder for was
  built elsewhere — `common/sse.ts` plus `build.controller.ts`, *"written by hand rather
  than through Nest's `@Sse` decorator"*. `StreamController` is still mounted
  (`app.module.ts:46`) and still exposes an authenticated route on any `projectId`,
  scoped to nothing, that emits `{ projectId, heartbeat, note: "stub stream" }`. It leaks
  nothing today because it echoes only what the caller sent. It should be deleted, not
  finished.
- **`AuthStatusResponse`'s comment** — *"auth (stub — real Clerk integration is phase 3.3)"*
  (`dtos.ts:42`). Phase 3.3 happened.

## 7 · Open questions

**a. RLS, or better fences?** The convention (resolve the project through the scoped
client, then use `projectId`) is one unguarded call away from a leak, and one has now been
found. Two answers: add `workspace_id` to the seven child tables and scope them like the
rest, or put RLS under all of it. The first is a migration and a set-membership change; the
second is a bigger commitment and makes the application layer a convenience rather than the
control. Either needs an ADR. Doing neither leaves `tenant-discipline.spec.ts` as the only
fence, and that test does not read query arguments.

**b. What is the cap actually for?** $50/month/workspace, env-configurable, hard-refusing.
That is a bill guard. It is not a plan, and ADR-0009 defers billing tables to Phase 12. The
open question is whether the cap becomes a per-plan column (B063) or stays a platform-wide
circuit breaker with plans layered above it — and until it is answered, nobody can show a
user their balance in a way that means anything.

**c. Is the webhook worth verifying, or worth deleting?** Provisioning is lazy and the
handler is inert, so the endpoint currently earns nothing. Either install `svix` and verify,
or remove the route until `user.deleted` has work to do. Leaving a `@Public()` POST endpoint
that looks like it authenticates is the worst of the three.

**d. Does ADR-0019 survive contact with `ON DELETE RESTRICT`?** Its proposal (3) —
*"Account deletion cascades to projects and stops there"* — has no mechanism in the schema.
Whoever accepts the ADR is also choosing an ordered-delete routine or a schema change.

---

## Documentation drift found

**1. `docs/COSTS.md` is a 13-line skeleton describing work that is done.** It still reads
*"Status: skeleton. Modelled in **Phase 2**; enforced in **Phase 6**"* with three empty
sections, one of which is *"Pricing & limits — Plans, credits/quotas, iteration caps,
guardrails against runaway cost. (Phase 2)"*. Built since: a metering ledger with six
`UsageKind` values and four write sites, a per-period cap (`usage.service.ts:32`), a
per-build ceiling in the engine relay (`engine/builder/loop.py:256-262`), and
`GET /usage/allowance`. Last touched 2026-08-19; the enforcement landed 2026-08-22 in
`4746757 fix: bill what a cancelled build spent, cap the period…`. **This is the largest
drift in the layer.**

**2. `docs/SECURITY.md`'s "Controls" section is empty** — *"How each threat above is
mitigated. (Phase 2/6)"* — directly under a threat list whose first entry is *"Tenant
isolation (one user's app/data must never reach another)"*. The controls exist:
`workspace-scope.ts`, `tenant-discipline.spec.ts`, `WorkspaceThrottlerGuard`, the period
cap, the CORS allow-list (`main.ts:15`). The prompt-injection section appended below it
(B104, 2026-08-22) is excellent and current; the skeleton above it is not.

**3. `docs/DATA-MODEL.md` predates five migrations.** It has no `build_job` entity
(migrations 0011, 0012); `project` lacks `draft_spec`, `draft_whole`, `draft_estimate`,
`draft_confirmation_hash`, `preview_url` (0002–0005); `build_version` lacks `cost_usd`,
`tokens`, `idempotency_key` (0005, 0010); `project.status` is listed as
`draft | building | ready | error`, missing `spec_locked` (0002). Last touched 2026-08-19.

**4. ADR-0009's scoping claim overstates what is enforced.** *"Everything is scoped by
`workspace_id` — tenant isolation lives in the data layer and is enforced in every query"*
(ADR-0009:15-16). Six of fourteen models are scoped in the data layer; seven have no
`workspace_id` column. `ARCHITECTURE.md` §7 describes the real arrangement correctly and
should be treated as the accurate account; ADR-0009 should be amended or superseded rather
than left as the citation people reach for. `schema.prisma:2-3` repeats the same claim.

**5. ADR-0019 cites a column that does not exist.** *"`user.deleted` is still a column
nothing writes to"* (ADR-0019:65-66). The `User` model has `id`, `clerkUserId`, `email`,
`workspaceId`, `role`, `createdAt`, `updatedAt` — no deletion column, in schema or in any
migration. The Clerk *event* named `user.deleted` exists; the column does not.

**6. ADR-0008's consequence about the engine was not what was built.** *"Backend verifies
Clerk JWTs; the Python engine can validate the same tokens"* (ADR-0008:20). The backend
half is true (`clerk-identity-verifier.ts:27`). The engine half is not: the engine
authenticates the API with a shared secret, `SCIO_ENGINE_TOKEN`
(`apps/engine/src/scio_engine/main.py:97`), and refuses to boot in production without it.
Not a defect — a consequence that was superseded by a better decision and never written
back.

**7. The schema history is incomplete for a rebuild.** `library_category` and
`library_entry` are created by the engine at runtime
(`apps/engine/src/scio_engine/library/store.py:135,144,216`) in the same database, and
appear in no migration and no `schema.prisma`.

### The 12 migrations, in order

| # | Migration | What it added |
|---|---|---|
| 0001 | `init` | The whole schema: `vector` extension, 10 enums, 13 tables (`workspace` → `audit_log`), all FKs `ON DELETE RESTRICT`; the pgvector index left commented out pending a fixed embedding dimension. |
| 0002 | `gate1_spec_lock` | `ProjectStatus.spec_locked` and `project.draft_spec` (jsonb) — gate 1's working spec. |
| 0003 | `build_preview_url` | `project.preview_url` — where the current build is being served. |
| 0004 | `draft_whole_and_estimate` | `project.draft_whole`, `draft_estimate` — cached because recomputing them made `GET /intake` take 10.6s *and cost money on a page refresh*. |
| 0005 | `build_cost_and_cache_key` | `build_version.cost_usd`, `tokens` (nullable: *"0 would be a claim rather than an absence"*), and `project.draft_confirmation_hash` to invalidate 0004's cache. |
| 0006 | `indexes_and_one_current` | 15 FK indexes Prisma does not create on Postgres — including `project(workspace_id)`, *"the lookup that happens on EVERY request"* — plus three partial unique indexes making "exactly one current version" a database rule instead of four hopeful code paths. |
| 0007 | `usage_kinds_for_the_design_window` | `UsageKind += preview, design_change` — the design window's spend was real and had nowhere to go but `generation`. |
| 0008 | `usage_by_period` | `usage_event(workspace_id, created_at)` — *"Every billing question is 'spend in a period', and nothing indexed the period."* |
| 0009 | `usage_kind_intake` | `UsageKind += intake` — the wizard's one relay call per message, *"the only spend in the product the ledger could not see at all."* |
| 0010 | `build_idempotency` | `build_version.idempotency_key` plus a **partial** unique index on `(project_id, idempotency_key)` so pre-existing NULLs do not collide. A retry must not be a second bill. |
| 0011 | `build_jobs` | The `build_job` table, two indexes, and a partial unique index enforcing one live build per project. ADR-0020's first slice: a build you can find after a restart, and one you can stop. |
| 0012 | `job_spend` | `build_job.cost_usd`, `tokens` — because `persist()` only runs on `finished`, so *"cancel a second before the end and the ledger stayed at zero."* |

0006, 0008, 0010, 0011 and 0012 are hand-written idempotent SQL (`IF NOT EXISTS`) rather
than Prisma-generated. Re-runnable, which is a virtue; also invisible to Prisma's drift
detection, which is not.

*Verified 2026-08-26 against the code, with all 135 API tests passing
(`cd apps/api && npx vitest run` → 12 files, 135 passed).*
