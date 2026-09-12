# Layer G · Cross-cutting — what to build next

Forward-looking. `docs/as-built/LAYER-G-CROSS-CUTTING.md` is the starting point; this is what to
do with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method note.** Layer G is the layer where every word is a domain word — authentication,
authorization, multi-tenancy, migrations, metering, streaming, supply chain — and every one of
them has a standard, a paper or a running system behind it. Nothing below was designed before
that domain was scanned. Scanned 2026-08-26: Google Zanzibar and its open implementations
(OpenFGA, SpiceDB), AWS Cedar and Oso; Postgres multi-tenancy guidance (shared-schema/RLS,
schema-per-tenant, database-per-tenant) and Prisma's actual RLS story; the Standard Webhooks
specification and Clerk's use of it; usage-based billing for AI products (Orb, Metronome, Lago,
OpenMeter, Stripe); SLSA, Sigstore, dependency hashing, SBOM and the EU Cyber Resilience Act
timeline; SSE versus WebSocket and the resumable-stream work; and the public record of security
failures in AI app builders, of which the competitor's is a CVE.

**Three things this layer would otherwise have invented already exist**: a relationship
authorization model (Zanzibar), a webhook signature protocol (Standard Webhooks — and its
implementation is *already installed in the tree*, §1.1), and an RLS conformance test shape
(pgTAP / Atlas — and Scio's own version is better, and switched off, §1.6).

**One thing this layer would otherwise have bought, and should not**: a metering vendor. §7.4.

Every code claim carries `file:line` and was re-checked against the working tree on 2026-08-26.
Where a number could not be verified it is marked, not asserted.

---

## 1 · Where Layer G stands

Everything the other six layers assume and none of them own: who the caller is, which tenant's
rows they may touch, what their work costs, what they may spend, and how a forty-minute build
reaches a browser. 37 files, 1,984 lines. Governed by ADR-0007 (Postgres), ADR-0008 (Clerk
behind an interface), ADR-0009 (data model), ADR-0019 (deletion — still *Proposed*).

**Solid, and not to be touched:** `applyWorkspaceScope` as a pure exported function that
**throws** on any operation it does not recognise (`workspace-scope.ts:56-79`) — `upsert` and
`createMany` were closed *before* either had a caller, and this is the best-shaped thing in the
layer; `IdentityVerifier` (`identity-verifier.ts:13`), where ADR-0008's swappability is real
rather than aspirational; `devAuthEnabled` throwing rather than warning in production
(`dev-identity-verifier.ts:32-39`); 404 rather than 403 across tenants, chosen and documented
(`project.service.ts:30`); non-throwing metering with skip-if-zero, four sites, one shape;
the cap as a *period* cap — *"it bounds one build and nothing bounds the number of builds"*;
and `openStream` (`sse.ts:19-47`), written from a real reported failure.

**The load-bearing claim, from ADR-0009:** *"Everything is scoped by `workspace_id` — tenant
isolation lives in the data layer and is enforced in every query and in authorization."*

It is true of **6 of 14 models**. Counted at source: `schema.prisma` declares fourteen models;
`workspaceId` appears as a column on `User:113`, `Project:127`, `BuildJob:233`, `UsageEvent:356`,
`Notification:375`, `AuditLog:393`. `Workspace` is the tenant itself. The remaining seven —
`Message`, `SpecVersion`, `DesignVersion`, `BuildVersion`, `Deployment`, `ReferenceAsset`,
`ReferenceEmbedding` — have no such column, and `applyWorkspaceScope` returns their arguments
untouched at `workspace-scope.ts:62`.

### 1.1 The webhook TODO is obsolete: the verifier is already installed

This is the largest correction, because it turns a dependency decision into a two-line import.

The as-built record says *"the TODO names the library — `svix` is the library — and `svix` is
not installed."* Both halves are true and both are beside the point.

`apps/api/package.json:16` declares `@clerk/backend: ^3.16.1`. The installed package declares
**`standardwebhooks: ^1.0.0` as a direct dependency** and exports a `./webhooks` entry point
whose only public function is:

```ts
export declare function verifyWebhook(
  request: Request, options?: { signingSecret?: string }
): Promise<WebhookEvent>;
```

It reads `CLERK_WEBHOOK_SIGNING_SECRET` from the environment by default — the exact variable
`webhook.controller.ts:56` already reads. Clerk moved to [Standard
Webhooks](https://www.standardwebhooks.com/) (the specification Svix's scheme became); the
`svix-id` / `svix-timestamp` / `svix-signature` headers the controller already inspects are that
protocol's headers, and the timestamp is what makes it replay-resistant rather than merely
signed.

**The real blocker is not the library. It is the body.** `verifyWebhook` takes a Fetch
`Request` and must hash the **raw bytes**; `main.ts:23` calls `NestFactory.create(AppModule)`
with no `rawBody: true`, and `main.ts:24` installs a global `ValidationPipe`. By the time
`@Body()` reaches `handle()` at `webhook.controller.ts:26`, the bytes that were signed are gone.
So the change is: `rawBody: true` at bootstrap, a raw-body read in the controller, and the
import. No new dependency, no `svix`.

The controller's fail-closed ordering is correct and should survive unchanged — its comment
(*"the moment somebody implements `user.deleted` cleanup behind an unverified signature, an
anonymous request deletes accounts. So the refusal lands FIRST"*) is the right instinct and the
right sequence. What it does not do is verify: with a secret set, `svix-signature: anything`
passes. There is no test for this controller at all.

### 1.2 F-03 verified at source — and the fence predicted it while naming the wrong client

The most serious finding in the review corpus. Confirmed three ways, 2026-08-26:

```
build.service.ts:517   if (idempotencyKey) {
build.service.ts:518     const already = await this.buildFor(workspaceId, projectId, idempotencyKey);
build.service.ts:519     if (already) { await emit("finished", this.replayOf(...)); return; }
build.service.ts:525   const project = await this.project(workspaceId, projectId);   ← the ownership check
```

```ts
// build.service.ts:365-373
private async buildFor(workspaceId, projectId, idempotencyKey) {
  return this.client(workspaceId).buildVersion.findFirst({
    where: { projectId, idempotencyKey },
  });
}
```

`BuildVersion` carries no `workspace_id` (`schema.prisma:265`), so `WORKSPACE_SCOPED_MODELS`
does not contain it, so `applyWorkspaceScope` returns at `workspace-scope.ts:62` having changed
nothing. **The `workspaceId` argument selects the client and does not touch the query.** The same
short-circuit exists in `ensureCanStart` at `:202`, also before its `this.project()` at `:233`,
and the key is a client-supplied header (`@Headers("idempotency-key")`, `build.controller.ts:76`).
Reachability is a guessed project UUID *plus* the matching key — not trivial; what returns is the
other tenant's `git_sha`, honest-status summary, `total_cost_usd` and `total_tokens`.

**The correction to the record is about the fence, not the bug.** `tenant-discipline.spec.ts:15-19`
predicts this defect in its docstring:

> One future `buildVersion.findMany({ where: { projectId } })` **on the raw client** reads across
> tenants with nothing to stop it — an external reviewer named exactly this.

The live defect is `buildVersion.findFirst({ where: { projectId, idempotencyKey } })` on the
**scoped** client. The prediction was right about the query and wrong about the client, and the
test greps for `this.prisma.<model>` — so the shape it was written to catch is the shape it
cannot see. A fence that names the failure in prose and misses it in code is worse than no
fence, because it is cited as coverage.

### 1.3 The convention is relied on 26 times, and 24 of them honour it

Counted at source, non-test files only: **26 query call sites** on the seven unscoped models —
`build.service.ts` 9, `spec.service.ts` 7, `design.service.ts` 7, `intake.service.ts` 3. Every
public method in `spec.service.ts` and `design.service.ts` opens with
`await this.project(workspaceId, projectId)` (`spec.service.ts:49,69,186`;
`design.service.ts:211,239,329,357,510,584`). The convention is not sloppy; it is a discipline
genuinely kept, and `build.service.ts` is the sole outlier at exactly the two paths that
short-circuit before it.

That is the honest shape of the risk: **not 26 leaks, but 26 places where correctness is a habit,
and one place where the habit was skipped for a good reason** — a replay must be cheap — and
nothing noticed.

### 1.4 The test doubles are stricter than production

`FakeScope` in `build.e2e.spec.ts` enforces `owns(where.projectId)` on every child-model
operation — at `:51`, `:57`, `:64`, `:109`, `:127`, `:172`. Line 109 is
`buildVersion.findFirst`, the exact call that is unguarded in production.

`workspace-scope.spec.ts:37` asserts that production does **not** do this
(*"leaves non-scoped models untouched"*). So the two suites assert opposite things about the
same mechanism and both pass.

**Every cross-tenant e2e assertion therefore passes for two reasons at once and cannot
distinguish them.** This is the more dangerous of the two confirmed cases of tests passing for
the wrong reason, because a double that is *stricter* than reality cannot fail — it can only
certify. Any claim of tenant safety resting on `build.e2e.spec.ts` is worth less than it looks.

### 1.5 CVE-2025-48757: both scores are in the record, and they are from different authors

The competitor's failure is the strongest argument this document has, so the number has to be
right. Both circulating figures are real, and they have different authors:

| Score | Author | Where |
|---|---|---|
| **9.3** Critical, `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` | **MITRE**, as CNA | the CVE record — [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-48757), [GHSA-773x-pxjg-gxgx](https://github.com/advisories/GHSA-773x-pxjg-gxgx), published 2025-05-29/30 |
| **8.26** base, 7.58 temporal (also v3.1) | **the reporting researcher** | [mattpalmer.io, May 2025](https://mattpalmer.io/posts/2025/05/CVE-2025-48757/) |

**Cite 9.3 as the CVE record and 8.26 as the reporter's own assessment; never present one as a
correction of the other.** The description matters more than either: *"An insufficient database
Row-Level Security policy in Lovable through 2025-04-15 allows remote unauthenticated attackers
to read or write to arbitrary database tables of generated sites"* — CWE-863. Vendor
acknowledgement 2025-03-24, disclosure 2025-04-15, **"Patches and Updates: None available"** —
workarounds only, for users to apply themselves.

**Limits.** The widely repeated *"303 endpoints across 170+ apps, 10.3% of projects analysed"*
appears only in secondary coverage; the primary advisory as fetched states no scan counts, so
treat the proportion as reported rather than verified. A 2026 press report of a mass Lovable
exposure affecting projects created before November 2025
([cyberpress.org](https://cyberpress.org/lovable-ai-app-builder-reportedly-exposes-thousands-of-project-data-via-api-flaw/))
is single-source and should not be leaned on in any external claim.

### 1.6 The RLS conformance harness Scio needs already exists — and is off by default

This is the finding that makes §4 a product argument rather than hygiene.

`library/verification/client.ts` runs the generated app's own queries against an in-process
PostgreSQL (pglite), and it is faithful in exactly the way naive setups are not. From `:18-23`:

> pglite connects as `postgres`, a superuser, and superusers bypass row-level security — so a
> naive setup would report every policy as working. Every app query therefore runs inside a
> transaction as the non-superuser `authenticated` role with the JWT claim GUCs set, which is
> exactly what PostgREST does per request. **`SET LOCAL` outside a transaction is a silent
> no-op; that is why the transaction is not optional.**

It ships an `auth.uid()` / `auth.role()` / `auth.email()` shim over
`current_setting('request.jwt.claim.sub')` (`:39-58`), creates `authenticated` and `anon`, and
grants **all** privileges to both on purpose (`:76-83`) — *"the POLICY decides, not the grant. A
tighter grant looks like RLS working and is not."*

That is a more rigorous test of a generated app's row-level security than pgTAP-in-CI, because it
exercises the application's real data path rather than SQL written for the test. It is the
mechanism that would have caught CVE-2025-48757 in a generated app before delivery.

**It runs only when `SCIO_VERIFY_DATA=1`** (`verification/__init__.py:11,38`), and Layer E
records both interaction gates as opt-in behind that flag. On every default build, the strongest
security check in the system does not run.

### 1.7 The price table is wrong for exactly one model, and it is the current Sonnet

`matrix.yaml:54-60` declares `claude-sonnet-5` at `input_cost_per_mtok: 3.0` and
`cost_per_mtok: 15.0`. Current first-party list is **$2 / $10 per MTok**. Checked against the
whole table: Fable 5 ($10/$50), Opus 5 ($5/$25), Opus 4.8 ($5/$25) and Haiku 4.5 ($1/$5) are all
correct. The Sonnet 5 row carries **Sonnet 4.6's card** — $3/$15 — which is the diagnosis: the
row was not updated when the model was.

Both halves are 50% high. §7.2 traces where that goes.

### 1.8 Two smaller corrections

**Four of eight `UsageKind` values have never been written.** `schema.prisma:68-80` declares
eight; the four write sites (`build.service.ts:776`, `:305`, `intake.service.ts:246`,
`design.service.ts:151`) emit `generation`, `intake`, `preview`, `design_change`. `critique`,
`sandbox`, `storage` and `other` have no writer. Separately `packages/shared/src/entities.ts:14`
declares five, missing exactly the three that *are* written — a gap hidden by the cast at
`usage.service.ts:51`.

**`spentThisPeriod` sums in JavaScript.** `usage.service.ts:62-68` calls `findMany` for every
row of the month and reduces in Node. `aggregate` is already in `READ_OPERATIONS`
(`workspace-scope.ts:33`), so the scoped client would pass it through and the database would do
the sum. Free correctness *and* a bounded response — today a workspace with a busy month loads
its whole ledger to answer one number.

---

## 2 · Refining what exists

Small, high-value, each one a patch rather than a project.

### 2.1 Move the replay behind the ownership check — and then remove the reason it was in front

Two changes, and only doing both is a fix.

**(a) Reorder.** `this.project(workspaceId, projectId)` before `buildFor` in both `run` (`:517`)
and `ensureCanStart` (`:202`). It costs one extra indexed read on `project(workspace_id)` — an
index that exists (migration 0006, *"the lookup that happens on EVERY request"*). The comment at
`:513-516` explains why the replay is first: a client that never heard the first build finish
must not be billed twice. Nothing about that requires skipping the ownership check; it required
skipping `refuseIfAlreadyBuilding`, which is a different call.

**(b) Give `BuildVersion` a `workspace_id` and scope it.** Otherwise the reorder fixes two call
sites and leaves the model unscopeable, and the next person writes the twenty-seventh call site.
This is a migration plus one line in `WORKSPACE_SCOPED_MODELS`, and it is the same decision for
all seven child models (§3.4).

**(c) The test that would have caught it.** Not another e2e assertion against `FakeScope` —
`FakeScope` is the reason nothing caught it. It has to run `applyWorkspaceScope` itself: *for
every model in the schema, either it is in `WORKSPACE_SCOPED_MODELS` or it is named in an
exemption list with a reason.* Same shape as `tenant-discipline.spec.ts`'s allow-list, which
already works, applied to the thing that actually decides.

### 2.2 Verify the webhook with what is installed, or delete the route

Per §1.1 the cost is: `rawBody: true` at `main.ts:23`, read `req.rawBody`, call `verifyWebhook`.
The as-built record's open question — *"is the webhook worth verifying, or worth deleting?"* — is
now easy in one direction: verification is cheaper than the deliberation about it. Deleting is
also defensible (provisioning is lazy, the handler is inert); leaving a `@Public()` POST endpoint
that inspects a signature header without checking it is the worst of the three, and that is where
it sits. Add the test that does not exist — valid signature passes, tampered body fails, **stale
timestamp fails**. The third is what distinguishes Standard Webhooks from a bare HMAC.

### 2.3 Fix the Sonnet 5 row, and pin the table against drift

One-line data fix, then the thing that makes it not recur: **a test that every model entry
carries a `checked_on` date, failing when one goes stale.** CI cannot fetch prices, but
`matrix.yaml:18-23` already carries the operator instruction in prose, and a date field turns a
comment into a check. Nothing in `estimate.py` needs re-deriving — its constants are in *tokens*
(`:73-87`) and only the money moves (§7.2).

### 2.4 `@CurrentWorkspace` should refuse rather than return `undefined`

`auth-context.ts:23-25` returns `contextOf(ctx)?.workspaceId` — type `string | undefined` — while
every controller declares the parameter as `workspaceId: string`. On a `@Public()` route it is
`undefined`, and `where: { workspaceId: undefined }` in Prisma means *no filter*: an unscoped
query across every tenant. No `@Public()` route uses the decorator today, so it is latent — one
careless decorator from live, with the type system unable to object because the lie is in the
declaration.

The fix is that the decorator throws when there is no auth context. A `@Public()` route asking for
the current workspace is a programming error, and it should say so at the first request rather
than at the first breach.

### 2.5 `prisma.service.ts` should fail fast in production

`prisma.service.ts:22-24` warns *"DATABASE_URL not set — running without a database"* and returns.
The docstring's defence is right for local development — a contributor should be able to boot the
API without Postgres. In production it is a service answering requests with the tenant boundary's
storage absent.

The correct shape exists twice already in this codebase: `dev-identity-verifier.ts:32-39`
**throws** in production rather than honouring a flag, and `main.py:75-77` refuses to boot the
engine in production without `SCIO_ENGINE_TOKEN`. This is the third instance of one pattern and
the only one that got it wrong. Gate on `NODE_ENV`; keep the dev path exactly as it is.

### 2.6 Three that are one commit each

**One currency, one precision.** `build_job.cost_usd` is `Decimal(10,4)`
(`schema.prisma:246`); `build_version.cost_usd` is an unqualified `Decimal?` (`:276`), which
Prisma maps to `DECIMAL(65,30)`; `usage_event.amount` and `.cost` are unqualified (`:360-361`).
Three precisions for one currency, and the ledger — the one that decides whether a user may
build — is the one with no declared scale. `Decimal(12,6)` throughout, because a relay pass can
cost fractions of a cent and the ledger is summed, not rounded per row.

**Derive the shared enums from the schema.** `PROJECT_STATUSES` (`project.dto.ts:6`) omits
`spec_locked`, which `ProjectStatus` (`entities.ts:9`) has and migration 0002 added — and it
drives both the `@IsIn` validator and the Swagger enum (`project.controller.ts:29,86`), so
`PATCH /projects/:id` cannot set the status the spec gate uses. `UsageKind` is three values behind
(§1.8). Both are hand-copied database enums; Prisma already generates types for them, and a
generated constant cannot drift.

**Delete `modules/stream/`.** Three files, 36 lines, still mounted at `app.module.ts:46`,
exposing an authenticated route on any `projectId`, scoped to nothing. It leaks nothing *today*
precisely because it does nothing. An endpoint that looks like a feature and is a stub is an
invitation to finish it in the wrong place.

### 2.7 Count the swallowed ledger writes

All four metering sites are inside `try/catch` that logs and continues, and that invariant is
correct: *"A bookkeeping failure must not be the thing that decides whether a user can build
again."* The cost of the invariant is stated nowhere: **a swallowed write is unbilled spend, and
nothing counts how often it happens.**

A counter is not a change of policy. Increment a metric in the catch, and the cap gains an error
bar it does not currently have — because `spentThisPeriod` reports a floor, not a total, and
nobody knows how far the floor is from the truth.

---

## 3 · What is missing

### 3.1 The authorization model — and it is two models, not one

This is the largest gap in the system, and the confusion to clear first is that Layer G owns
**two** authorization problems that look alike and have different answers.

| | Scio's own tenancy | The generated app's authorization |
|---|---|---|
| Subject | a workspace | the end user of a built app |
| Enforced by | `applyWorkspaceScope`, application layer | Supabase RLS policies, generated (ADR-0011 fixes the stack) |
| Model today | a set of six model names | `row_level_security: bool = True` and `scope: "own" \| "all"` |
| Blast radius of failure | one tenant reads another's build metadata | **CVE-2025-48757** |

**What the second one is today, at source.** `architecture.py:49` and `:144`:
`row_level_security: bool = True`. Never anything else — `derive.py:384` passes `True`
unconditionally, and no code path sets it false. `architecture.py:83`:

```python
class Permission(BaseModel):
    """Who may run which operation. `operation` must name a real operation."""
    role: str
    operation: str
    scope: str = "own"  # "own" | "all"
```

The type is `str`. The enumeration is a comment. `derive.py:196` assigns it
`"all" if role.name in elevated else "own"`. That is the entire authorization model of every app
Scio builds: a boolean that is always true, and a two-valued untyped string.

**That is precisely the shape of the CVE.** Lovable's failure was not that RLS was off — it was
that *"projects were deployed with RLS policies that don't match the business logic."* A boolean
saying "RLS: on" is exactly the artefact that cannot express a mismatch. `contract.py:57` renders
it into the prompt as `table booking (row-level security: True)`; `contract.py:114` renders
`security posture: RLS=True`. The model is being told a fact with no content and asked to write
policies from it.

**What exists in the field, and what each would cost.** Scanned 2026-08-26.

| Option | What it is | Honest cost |
|---|---|---|
| **Zanzibar** — Pang et al., [USENIX ATC 2019](https://www.usenix.org/conference/atc19/presentation/pang) | Google's authorization system: object–relation–user tuples, checks and reverse queries over the graph. Trillions of ACLs, **<10 ms p95**, >99.999% | free — it is a paper, and it is the reference model to read before designing anything |
| **OpenFGA** — [openfga.dev](https://openfga.dev), CNCF Sandbox, Auth0/Okta | the most approachable Zanzibar implementation: modelling DSL, check/list/expand, runs on your existing database | a **service to run** — deploy, monitor, back up, and keep its tuple store consistent with Postgres. Two sources of truth for *"who may see this"* is a bug class we do not have today |
| **SpiceDB** — [authzed.com](https://authzed.com) | the most faithful: schema close to the paper, Watch API for cache invalidation, ZedToken consistency | as above, plus a consistency model the team must actually understand |
| **Cedar** — AWS, open source; SDKs in Rust, Java, Python, JS/TS, Go as of March 2026; [Cedar 4.5 in AVP, Aug 2025](https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-verified-permissions-cedar-4-5) | a *policy language* with a formally verified evaluator; policies as versioned, machine-analysable artefacts | a language to generate and validate. No service required if used as an artefact rather than a runtime |
| **Oso** | policy-as-library, embedded | a smaller commitment than any of the above, and a smaller answer |
| **Postgres RLS, shared schema** | policies in the database | one migration per table plus a session-variable discipline |

**The recommendation, and it is deliberately unfashionable: do not run a ReBAC service.**

For Scio's own tenancy the model is one relation deep — a row belongs to a workspace. Zanzibar
exists because Drive has sharing, groups, nested folders and inheritance. Adopting OpenFGA to
express `project.workspace_id = :ws` buys an operational dependency, a second source of truth and
a consistency window, to model what a `WHERE` clause already models. **Revisit the moment the
product grows a second relation** — team members, shared projects, an agency managing several
clients — because that is when a hand-rolled model starts accreting special cases, which is
precisely the failure Zanzibar was written about.

For the generated app, ADR-0011 fixes the stack on Supabase, so the enforcement point is Postgres
RLS and cannot be anything else without superseding an accepted ADR. The gap is not the
enforcement point. **It is that nothing between the user's intent and the generated `using (...)`
clause is checkable.** Three things close it, in increasing ambition:

1. **Type the model.** `scope: Literal["own","all"]`, plus the third value the domain obviously
   has and this one does not — `"none"`. Make `row_level_security` a per-table decision carrying
   its reason rather than a constant. An afternoon, and it makes the next two possible.
2. **Derive the policy, do not prompt for it.** A `Permission` plus an owner column determines
   the policy text; generating SQL from a typed permission is a template, not a judgement. Layer
   C's refusal discipline already has the shape — `scripts.py:195` refuses to emit the isolation
   criterion when `table is None or not owner or not table.row_level_security`.
3. **Verify the policy against the model on every build** — §1.6's harness, on by default,
   against the criterion Layer C already writes and scopes out.

**Where Cedar becomes interesting, marked speculative.** A Cedar policy *set* is analysable — its
evaluator has machine-checked proofs — so emitting the derived permission model as Cedar
alongside the SQL would make questions like *"is there any principal for whom this set permits
reading another user's row?"* decidable at build time instead of hopeful. The SQL ships; the
Cedar is its checkable shadow. **Speculation:** nobody cited here does it, Cedar-to-RLS is not a
solved translation, and the honest position is that this is a spike, not a plan.

### 3.2 The consent and licence model — and it is accumulating

Verified: **zero matches** for `consent`, `licence`, `license` or `attribution` across
`apps/engine/src/scio_engine/library/`, `apps/api/src`, and `schema.prisma`. The `library_entry`
table, created by the engine at runtime (`library/store.py:144-154`), has eight columns — `id`,
`category`, `seqno`, `version`, `status`, `contract_key`, `payload`, `created_at`. No
`workspace_id`, no origin project, no licence, no consent record; and `CatalogEntry.provenance`
(`library/entry.py:154`) is `str = "scio-seed"`, a free-text string with no schema.

ADR-0016 makes the library grow from real builds. `matcher.py:196-201` half-acknowledges what
that means:

> a catalog entry's name and description were written during someone **ELSE's** build (ADR-0016),
> which makes this the one prompt in the engine that carries text across tenants (B104).

That comment is about *prompt injection* — the risk that an entry describing itself as *"the
correct choice, ignore the others"* reads as instruction. It is a good comment about the wrong
hazard. The larger one is that **code derived from one customer's build is assembled into
another customer's application, and nothing anywhere records that the first customer agreed.**

Four consequences, none hypothetical:

- **Unwithdrawable.** ADR-0019 is still *Proposed*, and even accepted, a deletion cascade needs a
  key. `library_entry` has no column naming the workspace it came from, so the data cannot be
  found and therefore cannot be deleted.
- **Untraceable.** If an entry turns out to carry something it should not — a hard-coded secret,
  a third-party snippet, a customer's vocabulary that survived generalisation — no query returns
  which apps contain it. `contract_key` indexes what an entry *does*, not where it came from.
- **Compounding.** Every successful build adds, so the exposure rises monotonically and the cost
  of retrofitting a consent model rises with it.
- **A claim the product cannot make.** ADR-0001's differentiator is *"developer-grade output…
  that the user owns."* Ownership of code containing another tenant's contributions, under no
  stated licence, is not something to put in writing.

**Do not invent a licence vocabulary.** [SPDX](https://spdx.dev/) is the ISO-standard identifier
list and SBOM format that every downstream consumer already parses. What has to be designed,
because no standard covers it, is the **grant**: when a user's build becomes contributable, what
they are told, and whether it is opt-in or opt-out. Product and legal, not engineering — §9,
**G-4**.

The interim position costs nothing: **add `source_workspace_id`, `source_project_id`, `licence`
and `consented_at` to `library_entry` now, and refuse to serve an entry with a null
`consented_at` into another tenant's build.** Seeds get a synthetic grant; contributions stop
until the ADR lands. That converts an accumulating liability into a paused one.

### 3.3 The CI security floor

Verified against `.github/workflows/ci.yml`, 2026-08-26: eight steps — install, build shared,
install engine, typecheck, ruff, engine tests, API tests, app tests. **Zero** references to
audit, CodeQL, semgrep, trivy, gitleaks, or any secret scanner.

`apps/engine/requirements.lock` pins **52 packages with 0 hashes**. (The other half of F-16 — the
"suspicious package names" `httpx2`/`httpcore2` — is a **false positive**: both are genuine
packages published under the Pydantic organisation by httpx's author. The hash gap is the half
that stands.) `main.ts:47` mounts `SwaggerModule.setup("docs", …)` with no guard and no
environment condition.

The CI file's own reasoning is excellent and points the right way — it clones fresh, refuses to
cache, and exists because *"three of the four bugs the first Codespace run found were invisible
to every suite."* It is a hermeticity check, not a security check, and it does not claim to be.

**What 2026 practice says the floor is**, scanned 2026-08-26:

| Control | Concretely | Source |
|---|---|---|
| Hash-pinned installs | `pip install --require-hashes -r requirements.lock`; `pnpm install --frozen-lockfile` (already done) | pip's hash-checking mode; standard 2026 baseline |
| No lifecycle scripts by default | `npm ci --ignore-scripts` / pnpm equivalent | the dominant npm compromise vector |
| Dependency audit | `pnpm audit` + `pip-audit`, failing on high | — |
| Secret scanning | gitleaks or equivalent, on the diff | there is a live `ANTHROPIC_API_KEY` in this system's threat model — `sandbox.py` already closed one leak path |
| SAST | CodeQL or semgrep | — |
| SBOM | SPDX or CycloneDX, per release | [EU CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) |
| Provenance | SLSA (v1.1 stable, v1.2 in development) + [Sigstore](https://www.sigstore.dev/) — Cosign, Fulcio, Rekor | npm provenance + SLSA L2 is the stated 2026 hygiene baseline |

**And there is now a date.** The EU Cyber Resilience Act's mandatory 24-hour vulnerability and
incident reporting to ENISA begins **11 September 2026** — two weeks from this document — and
applies to products already on the market; the SBOM-in-technical-documentation obligation follows
in December 2027 with CE-marked conformity. The practical order is the reverse of the legal one:
**you cannot report within 24 hours of awareness without already knowing what is in your
software.** Whether Scio is in scope is a legal question nobody here can answer; that the
capability is needed before the deadline rather than after the first incident is not.
`--require-hashes` and `pip-audit` are two lines and should not wait for the ADR.

### 3.4 Database-level isolation, as a backstop under the application scope

`ARCHITECTURE.md` §7 already concedes it: *"Postgres RLS on our own tables is a backstop we do
not have yet."*

Current guidance for a product at this stage is unambiguous: **start shared-schema with RLS**,
and move to schema-per-tenant or database-per-tenant only for hard compliance, data-residency or
contractual isolation requirements ([PlanetScale, *Approaches to tenancy in
Postgres*](https://planetscale.com/blog/approaches-to-tenancy-in-postgres)). Schema-per-tenant
costs N migration runs and strains tooling at thousands of schemas; database-per-tenant is the
strongest isolation and the heaviest operations — worth remembering as a *paid tier* (§4.6), not
a default.

**Prisma's actual story decides the effort.** Prisma has no RLS support in its schema language;
as of 2026 the pattern is unchanged — enable RLS and write policies in raw SQL migrations, set
the tenant with `SET LOCAL app.current_workspace = …` **inside a transaction**, inject it with a
Client Extension. Two facts follow, and both are already true here:
`WorkspaceScope.forWorkspace` (`workspace-scope.ts:91`) *is* a `$extends` query extension — the
exact hook the pattern requires, so the mechanism is built and only the policy layer is missing;
and `verification/client.ts:18-23` already documents both traps in our own words (`SET LOCAL`
outside a transaction is a silent no-op; a superuser bypasses RLS entirely).

So the honest cost is: seven `workspace_id` columns and a backfill, a policy per table, a
non-superuser application role, and every scoped query wrapped in a transaction. **The last is
the real one** — it changes the connection discipline, and behind a pooler in transaction mode
`SET LOCAL` is the only safe form.

**Belt and braces, not replacement.** The application scope stays. RLS is what makes the
twenty-seventh call site safe when someone forgets, and what makes the tenancy claim provable
rather than asserted.

### 3.5 The audit log has never been written to, and nothing measures the layer

`AuditLog` exists in migration 0001, carries `workspace_id`, is in `WORKSPACE_SCOPED_MODELS`
(`workspace-scope.ts:19`), is listed under security in ADR-0009 and called the security audit
trail in `DATA-MODEL.md`. **Nothing has ever written a row.** The events that belong in it are
all already detected and discarded: a cross-tenant 404, a cap refusal, an idempotency replay, a
build cancellation, a webhook rejection, a dev-auth token used, a scoping exception thrown. Most
of those are the only evidence that would exist after a breach. Same pattern as
`/usage/allowance`: *the honest signal is computed and dropped before anyone sees it.*

Nor is there any correlation: **0** matches for opentelemetry, prom-client, `correlationId` or
`requestId` across API and engine (C-F03 / G-F05, re-verified). Observability is Layer G's to own
because it is the only layer every request passes through. Adopt OpenTelemetry rather than
inventing a logging convention, and correlate on a **build id across API, engine and stream** —
the join nobody can currently make when a user says "my build broke".

### 3.6 Streaming has no resumption, and the protocol's own mechanism is unused

SSE defines resumption: the server emits `id:` on frames, and on reconnect the client sends
`Last-Event-ID`. `openStream`'s `emit` (`sse.ts:43-45`) writes `event:` and `data:` and **no
`id:`**. And `apps/app/src/lib/api.ts:218-220` uses *"SSE over fetch, not EventSource"*, for a
correct reason — *"EventSource cannot send an Authorization header"* — which also means the
browser's automatic `Last-Event-ID` reconnect is not available even if ids were emitted.

So a 45-minute build (the longest measured, `estimate.py:100`) rides one connection with no
resume. A tab switch, a mobile backgrounding, a network change, and the stream is gone. The build
survives — deliberate and tested (*"stops beating when the client leaves, without ending the
build"*) — but the user has no way back into it.

**Prior art and its limits.** Vercel's
[`resumable-stream`](https://github.com/vercel/resumable-stream) buffers server-side under a
stream id and lets a client reattach; the AI SDK exposes it as [resumable chat
streams](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-resume-streams). The published limit is worth
quoting rather than glossing: it covers a reload on the same device reconnecting to the same
server-side buffer, and does not by itself let a client find the right session on the right
server. Durable-session vendors sell the general answer, which is a dependency.

Scio needs neither, because the state exists: `BuildJob` (migration 0011) is the durable record
and build events are already emitted in order. Persisting them against the job and serving
`GET …/build/events?after=N` is resumption built from parts already in the schema — and is also
the record §3.5 wants. **Do not adopt a transport.** WebSocket buys bidirectionality this stream
does not need, at the cost of connection management, ordering and independent scaling. The gap is
durability, not duplex.

### 3.7 `GET /me` and `GET /workspace` are 501

Re-verified: **14** `NotImplementedException` across **six** modules — user (2), workspace (2),
notification (3), reference (3), deployment (3), usage (1); wider than either root review said.
The two that matter here are the two that tell a signed-in person who they are. `MeResponse` and
`WorkspaceResponse` exist in shared and are unused. A product whose central claim is *"the user
owns this"* cannot answer *"who am I, and what is my workspace"*.

---

## 4 · Out of the box

### 4.1 The competitor has a CVE for exactly the thing Scio can already test, and does not

This is the strongest product position in the entire corpus, and it is one flag away.

The argument, in the order a buyer hears it:

1. **The category has a public, catalogued failure.** CVE-2025-48757, CWE-863, *"read or write to
   arbitrary database tables of generated sites"*, no patch — workarounds only. Not a rumour, not
   a benchmark: an entry in the National Vulnerability Database with the competitor's name on it.
2. **The failure mode is structural, not careless.** Policies that do not match business logic.
   Every builder in this category generates policies from natural language and ships them
   unverified, and a boolean saying "RLS: on" — which is what Scio's own architecture model has
   today (§3.1) — cannot express a mismatch, so it cannot detect one.
3. **Scio has the machine that detects it**, built for a different reason and stronger than
   standard practice: an in-process Postgres running the app's own queries as a non-superuser
   with real JWT claims (§1.6). pgTAP and Atlas test policies with SQL written for the test; this
   tests the policy through the code that will actually run.
4. **So the claim is falsifiable, which is what makes it worth anything**: *"every app we ship
   has been shown, by executing it, that one user cannot read another user's rows — here is the
   run."*

**What it costs:** `SCIO_VERIFY_DATA` on by default, `row_level_security` as a per-table
decision, and the result in the reveal. Nothing needs inventing — the criterion *"a guest cannot
read another guest's booking"* is already written by Layer C and already scoped out as
unobservable on every build.

**And the discipline that makes it credible rather than marketing: our own house has the same
defect.** F-03 is a cross-tenant read in Scio's own API. Shipping the claim before fixing G-1 is
the fastest way to earn the competitor's headline.

### 4.2 Tenancy as a property that is fuzzed, not asserted

A step past §2.1's static check. Generate, from `schema.prisma` itself, a suite that for every
model and every operation attempts the cross-tenant version and asserts it fails — property-based
rather than example-based, so a new model arrives with its isolation test already written and
failing until it is scoped. This is the direct answer to §1.4: the e2e suite could not catch F-03
because it tested a double, and a schema-derived suite has nothing to double.

### 4.3 The honest bill

The system computes an honest signal and drops it before anyone sees it — `/usage/allowance` with
no consumer, `checks_passed` never rendered, `PlanValidation` never read. In Layer G that pattern
has a price tag attached. What Scio could show that no competitor does, all from data that
already exists:

- **before**: the estimate with its range and *why* the range is that wide (`estimate.py:92-111`
  has the three real calibration runs and the honest admission that the low band is optimistic)
- **during**: spend against the build ceiling — `Spend` (`relay.py:96-121`) is already a shared,
  incrementing, checked object
- **after**: actual cost, tokens, model, and the difference from the estimate
- **always**: `{spent, cap, room}` — the endpoint exists and nothing calls it
- **when it fails**: what a cancelled or failed build spent. `meterSpend`
  (`build.service.ts:295-320`) already writes it. The user is billed for it and never told.

The last is the one with teeth. **A build that fails should say what it cost and offer to not
charge for it.** Nobody in this category does that, and Scio has the ledger entry to do it from.

### 4.4 Deletion as a feature, not a compliance chore

ADR-0019 is *Proposed*, every FK in migration 0001 is `ON DELETE RESTRICT`, `user.deleted` arrives
at the webhook and is logged, and the library holds derived work with no key back to its origin
(§3.2). "Delete my account" has no mechanism at all. Turned around: the wedge is *"software they
intend to run and grow"* and the differentiator is *ownership*, and a product that can show a
user everything derived from their work — and remove it — makes that claim concrete. It requires
exactly the columns §3.2 asks for, **before** the corpus grows.

### 4.5 The security reveal

`PRODUCTION_READINESS_DIFF.md` §7 lists nine things reveal should show, three of them Layer G's:
security checks performed, model and build cost, remaining risks. Today it shows a subset of one.
The version worth building is not a green tick but **what was checked, what passed, and what
could not be checked and why** — `criteria.py`'s `scoped_out()` already produces that third list
with reasons, and Layer C's census counts 8 of 27 criteria observed by nobody. *"Three things in
this app cannot be verified automatically; here they are"* is a stronger trust move than a badge,
and in a category with a CVE it is the only credible one.

### 4.6 Two worth naming and not building yet

**Isolation as a tier.** Shared-schema-plus-RLS is right for now (§3.4) and is the thing an
enterprise buyer eventually refuses. Database-per-tenant is the strongest isolation and the
heaviest operations, which makes it a bad default and a defensible *paid* tier. Worth naming now
for one reason: **the decision that forecloses it is the shape of the migration story**, not the
schema. Five of twelve migrations are hand-written idempotent SQL (`IF NOT EXISTS`) — re-runnable,
which is a virtue, and invisible to Prisma's drift detection, which is not. A migration system
that cannot be replayed deterministically across N databases cannot become database-per-tenant
later, and keeping that possible is currently free.

**An SBOM per generated app.** SPDX or CycloneDX per build satisfies the CRA-shaped obligation
the *user's* product will inherit, makes §3.2's provenance visible where it matters, and answers
*"what is in my app?"*. Marked speculative: it only differentiates if it covers the **assembled
library entries** and their licences, which requires §3.2 first. An SBOM of npm dependencies is
table stakes `npm sbom` already generates.

---

## 5 · The means — skills, MCP, repos, research

One distinction first, per `docs/next/SKILLS.md`: a **Claude Skill** helps *us* build Scio; the
product's runtime uses relays and prompts. Nothing in this table becomes product machinery for
free.

| Means | What it gives Layer G | Verdict |
|---|---|---|
| **Zanzibar** — Pang et al., [USENIX ATC 2019](https://www.usenix.org/conference/atc19/presentation/pang) | the reference model for relationship authorization; the numbers (<10 ms p95, >99.999%) that show what a dedicated service buys and therefore what we are declining | **adopt the model as reading**, not the architecture (§3.1) |
| **OpenFGA** — [openfga.dev](https://openfga.dev), CNCF Sandbox | the most approachable Zanzibar implementation; a DSL and check/list/expand over an existing database | **not yet** — revisit the moment tenancy grows a second relation (teams, sharing). Running it to express one foreign key is operational weight for nothing |
| **SpiceDB** — [authzed.com](https://authzed.com) | the most faithful implementation; Watch API, ZedToken consistency | **not yet**, same reason, more to operate |
| **Cedar** — AWS, open source, formally verified evaluator, [Cedar 4.5 in AVP Aug 2025](https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-verified-permissions-cedar-4-5) | policies as analysable artefacts — the checkable shadow of generated SQL policies | **spike, marked speculative** (§3.1). Cedar→RLS is not a solved translation |
| **Oso** | policy-as-library | **not for this layer** — smaller commitment, smaller answer than typing the model we already have |
| **Postgres RLS, shared schema** — [PlanetScale, *Approaches to tenancy in Postgres*](https://planetscale.com/blog/approaches-to-tenancy-in-postgres) | the current mainstream answer for a product at this stage, and the trade-off table for the two alternatives | **adopt** (§3.4) |
| **Prisma Client Extensions for RLS** — no native support; `SET LOCAL` inside a transaction, injected by an extension | the exact mechanism `WorkspaceScope.forWorkspace` already is | **adopt the pattern** — the hook is built, the policies are not |
| **pgTAP / [Atlas RLS testing](https://atlasgo.io/faq/testing-rls)** | CI-level proof that isolation holds; the two canonical assertions (wrong tenant returns zero rows; the plan still uses a tenant-leading index) | **adopt the assertions**, not the tools — `verification/client.ts` is a stronger harness because it drives the app's own queries (§1.6) |
| **Standard Webhooks** — [standardwebhooks.com](https://www.standardwebhooks.com/); `@clerk/backend/webhooks` → `verifyWebhook` | signature + timestamp verification, already installed via `standardwebhooks@^1.0.0` | **adopt — it is an import** (§1.1, §2.2) |
| **Clerk / WorkOS / Auth0 / Supabase Auth / Better Auth** | provider choice | **no change.** ADR-0008's `IdentityVerifier` is real swappability; the defect is the webhook, not the provider. Re-opening the provider question would be work with no finding behind it |
| **Orb · Metronome · Lago · OpenMeter · Stripe Billing** | usage-based billing for AI products. Stripe acquired Metronome (announced Jan 2026) to add real-time metering to Stripe Billing; Lago and OpenMeter are the open-source, self-hostable options | **not yet, and §7.4 argues why.** The ledger, the period cap and the four write sites are built and correct. What is missing is a *plan model* (B063), which is a product decision no vendor makes for us. Revisit when there are plans to bill, not before |
| **SLSA** (v1.1 stable, v1.2 in development) · **[Sigstore](https://www.sigstore.dev/)** (Cosign, Fulcio, Rekor) | build provenance and artefact signing | **later** — the right destination; `--require-hashes` and an audit are the two lines that matter this month (§3.3) |
| **SPDX** — [spdx.dev](https://spdx.dev/) | ISO-standard licence identifiers and SBOM format | **adopt the identifiers** for §3.2 rather than inventing a licence vocabulary |
| **EU Cyber Resilience Act** — reporting from 11 Sep 2026; SBOM in technical documentation from Dec 2027 | the date that turns §3.3 from hygiene into a schedule | **track.** Whether Scio is in scope is a legal question; the capability is required either way |
| **[vercel/resumable-stream](https://github.com/vercel/resumable-stream)** · [AI SDK resume](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-resume-streams) | the shape of stream resumption, and its published limit (same-device reload against a server-side buffer) | **adopt the shape** (§3.6). Not the package — `BuildJob` is already the durable record |
| **WebSocket / durable session vendors (Ably, Convex)** | bidirectional transport, sessions that outlive connections | **not for this layer** — the build stream is one-directional. The gap is durability, and buying a transport to get it is the wrong trade |
| **OpenTelemetry** | correlated traces across API, engine and stream | **adopt** (§3.5) rather than inventing a logging convention |
| **MCP: GitHub secret scanning** (`run_secret_scanning`, already available in this session) | secret detection on the repo | **use immediately** — it is available and §3.3 has zero coverage today |

**Skills.** `.claude/skills/` holds thirteen (counted, 2026-08-26). Read before proposing: none
covers security, authorization, tenancy or supply chain. There is genuinely a gap.

| Skill | Change | Rests on | Used by |
|---|---|---|---|
| `tenant-isolation` | **new, proposed** — the two authorization problems and why they have different answers; the Zanzibar/OpenFGA/SpiceDB/Cedar decision with its operational cost stated; Postgres RLS shared-schema versus the two alternatives; the `SET LOCAL`/superuser/pooler traps; the two canonical isolation assertions; and the F-03 shape as a worked example of a scoped client that scopes nothing | Pang et al. ATC 2019; PlanetScale tenancy guidance; Prisma Client Extensions; Atlas/pgTAP RLS testing; CVE-2025-48757 | G-1, G-2, G-5 |

Per `SKILLS.md`'s four-part format: **source** (above), **method** (the decision procedure, not
a summary), **limits** — Zanzibar's numbers are Google's at Google's scale and say nothing about
a two-model tenancy; the Postgres guidance is practitioner consensus rather than a study; the
CVE tells us a competitor failed and not that our approach succeeds — and **eval**: the F-03
reproduction, a scoped-model-completeness check against `schema.prisma`, and a `SET LOCAL`
outside-a-transaction case that must be caught.

**Three skills deliberately not written**, and the reasons are the point:

- **No `metering` or `billing` skill.** §7.4 argues against adopting a vendor; a skill for a
  decision we are declining is inventory. The one durable fact — *price the model at the rate in
  force when the tokens were spent* — belongs in an ADR, not a skill.
- **No `webhook-verification` skill.** It is a two-line import (§1.1). A skill is for something
  repeated; writing one for a single job costs more than the job.
- **No `supply-chain` skill.** The content this month is `--require-hashes`, `pip-audit`,
  `--ignore-scripts` and a secret scanner. Those are CI lines, and a skill that restates four
  flags degrades the trigger accuracy of the skills that carry real method. Revisit if SLSA
  provenance is actually adopted, which is a decision with structure in it.

---

## 6 · Retrieval versus packing

Layer G is mostly not a model layer, which makes its three instances unusually clear.

### 6.1 The one prompt that packs another tenant's text

`resolve_ambiguity` (`matcher.py:189-210`) is the single place in the engine where text written
during one tenant's build is placed into another tenant's prompt. It packs `f"- {e.id}:
{e.name} — {e.description}"` for each candidate, fenced (`fenced_lines`), and the reply is
matched only against the listed ids.

**The fencing and the bounded parse are correct and should stay.** The retrieval observation is
different: the *description* is being sent because the matcher needs a tiebreak, and a
description is the least structured thing an entry carries. The entry's `Contract` — the thing
ADR-0014 says makes matching decidable at all — is structured, comparable, and already the
basis of `satisfied_by` at `matcher.py:186`. When two entries both satisfy a contract, what
distinguishes them is a *property* (test coverage, age, how often it was replaced), not prose.

That reframes the ambiguity call: today it asks a model to read two paragraphs of somebody
else's writing; the retrieval version asks the database which of two entries has better evidence.
The second needs no prompt, carries no cross-tenant text, and is the Pareto-replacement idea
`REVIEWS-WHAT-WE-MISSED.md` §4 already names as the actual differentiator.

### 6.2 The estimate is cached because computing it was packing

Migration 0004 added `project.draft_whole` and `draft_estimate` because recomputing them *"made
`GET /intake` take 10.6s and cost money on a page refresh"*, and 0005 added
`draft_confirmation_hash` to invalidate the cache. Worth naming what that is: **a page load was
re-running a model call to answer a question whose answer had not changed.** The cache is the
retrieval answer, arrived at by pain — and it generalises to what §4.3 wants, because an
allowance, a spend, an estimate and a build's actual cost are all *queries*, and every one is
currently recomputed, dropped, or delivered once inside a stream frame and never stored.

### 6.3 The reveal packs and does not keep

`build.service.ts:760-770` assembles the finished payload — `git_sha`, honest status,
`total_cost_usd`, `total_tokens`, `standin` — and emits it into the SSE stream. The
`build_version` row keeps `cost_usd` and `tokens`; the honest-status summary and the checks are
persisted nowhere. So *"what did this build actually verify?"* has an answer for the duration of
one HTTP connection and none afterwards — which is why §4.5's security reveal cannot be built
from history and §3.6's resumption cannot replay it. One table of build events fixes all three.

---

## 7 · Token economy

Layer G spends almost nothing on tokens and decides what everything else is allowed to spend.
It owns the price table, the ceiling and the ledger, so this section is about arithmetic rather
than prompts.

### 7.1 The price table, corrected

Anthropic first-party list rates, per MTok, as of 2026-08-26:

| Model | Input | Output | `matrix.yaml` says | Status |
|---|---:|---:|---|---|
| Claude Fable 5 | $10 | $50 | 10.0 / 50.0 | correct (`:33-34`) |
| **Claude Opus 5** — the default first choice | **$5** | **$25** | 5.0 / 25.0 | correct (`:41-42`) |
| Claude Opus 4.8 | $5 | $25 | 5.0 / 25.0 | correct (`:49-50`) |
| **Claude Sonnet 5** | **$2** | **$10** | **3.0 / 15.0** | **wrong — 50% high on both halves** (`:57-58`) |
| Claude Haiku 4.5 | $1 | $5 | 1.0 / 5.0 | correct (`:65-66`) |

$3/$15 is Claude Sonnet 4.6's card. The row was not updated when the model changed.

Also in force and not modelled anywhere: **cache reads cost ~0.1×** and a cache write ~1.25×,
with a model-dependent minimum cacheable prefix (512 tokens on Opus 5); the **Batch API is 50%**.
Layer C's §7.1 and §7.3 build on both. `_cost` (`relay.py:171-184`) prices only `input_tokens`
and `output_tokens` from the card — a cached read is billed at full input rate, so any caching
Layer C lands will be invisible to the ledger and to the user until `Completion` carries
`cache_read_input_tokens` and `_cost` prices it.

### 7.2 One wrong number, seven consumers

This is why a price table is not data.

```
matrix.yaml:57-58  →  ModelCard  →  _cost (relay.py:171)
    →  RelayPass.cost                     (what one pass cost)
    →  Spend.would_exceed (relay.py:114)  (the build ceiling, checked before every call)
    →  RelayResult.total_cost_usd         (what the build cost)
    →  usage_event.cost                   (the ledger, 4 write sites)
    →  spentThisPeriod (usage.service:61) (the month's total)
    →  allowance / the $50 cap            (whether a build may start)
    →  the reveal                         (what the user is told)
```

Every Sonnet 5 pass is priced **50% above list**, on both halves of the bill, in all seven
places. The direction matters: it over-charges. A workspace hits its $50 cap after $33 of real
spend, and the reveal reports a build as costing half again what it did.

**What it does *not* invalidate.** `estimate.py`'s calibration constants are in **tokens**
(`:73-87`), and its recalibration recipe (`:57-59`) is *"read `total_cost_usd` per package off the
finished event, divide by the model's `cost_per_mtok`"* — the same wrong rate on both sides, so
the token figures cancel and survive. The **dollar** column (`:42-50`) does not: those three real
runs were on `claude-sonnet-5` at two passes, so `feature = $0.857`, `foundation =
$0.168–$0.312`, and the headline *"five-package plan… **$1.42** in 14 minutes"* are each 1.5× the
true spend. At list, the same tokens are ≈ **$0.95**.

`tests/test_estimate.py` pins $1.42 inside the band, so fixing `matrix.yaml` moves a figure the
suite asserts. That is the test doing its job — and it reveals the durable fix: **the suite's cost
assertions are pinned to a price, not to a token count.** Re-anchor them to tokens and they
survive the next rate change.

### 7.3 The allowance, and what it actually knows

`cap()` reads `SCIO_WORKSPACE_PERIOD_CAP_USD`, default **$50** (`usage.service.ts:32-35`).
`periodStart()` is the calendar month in UTC (`:38-40`). `allowance()` returns
`{spent, cap, room}` and deliberately does not throw — *"the numbers belong in the refusal —
'you have spent $50.12 of $50 this month' is actionable, 'over budget' is not."* Enforced in
exactly one place, `ensureCanStart` (`build.service.ts:222-227`), as a 409.

Arithmetic worth stating plainly, at **corrected** rates. A five-package build is ≈$0.95 and a
seven-package build was measured at $2.69 against a $1.39 point estimate (`estimate.py:98-104`) —
call it ≈$1.79 corrected. So $50 buys somewhere between **18 and 50 builds a month**, before
intake, previews and design changes, which are metered too and are not in that figure. That is
the number a plan has to be built on, and nobody has stated it.

Four things the cap does not currently know:

- **It is a floor, not a total.** Swallowed ledger writes are uncounted (§2.7).
- **It is not atomic.** F-09 / G-F09: read-then-decide, with the build starting after. Two
  concurrent starts both see room. Not verifiable statically; the fix is a conditional write or
  an advisory lock, and it is small.
- **It cannot be re-priced.** `usage_event` stores `model` and `cost` but not the *rate* in force
  when the tokens were spent. When `matrix.yaml:57` is corrected, no historical row can be
  restated — which is the direct consequence of §7.2 and the argument for §8's rate column.
- **It cannot be shown.** `/usage/allowance` has no caller anywhere in `apps/app/src` (verified:
  zero matches for `/usage`). A user learns their balance by being refused.

### 7.4 What an honest cost estimate to the user would require — and why not to buy one

Five things, in order of how much they change the number:

1. **Correct rates**, with a date, per model (§7.1). Everything else is noise until this holds.
2. **Predicted input tokens.** `estimate.py:25-33` admits the gap: the relay now prices input,
   which was *"a third to a half of the real invoice"*, but the heuristic predicts output only,
   so the point estimate is knowingly low and rescued by `HIGH_MULTIPLIER = 2.6`.
3. **Cache reads at 0.1×.** Layer C's §7.1 puts ~892 constant tokens in front of 20–30 re-sends
   per build. Priced at full rate today; the ledger cannot see the saving.
4. **Batch at 50%**, once `parallelizable` is computed rather than guessed (Layer C §2.4).
5. **The range, and why it is that wide.** `LOW_MULTIPLIER = 0.7` / `HIGH_MULTIPLIER = 2.6`, and
   the honesty that produced them (`estimate.py:97-107`): the old high of 1.8 excluded both
   figures later measured — *"a range whose top the real world walks past is not a range, it is
   an underestimate with error bars."* That sentence is the product's voice. Show the range and
   the reason for it.

**And then do not buy a metering vendor.** Orb, Metronome (acquired by Stripe, announced January
2026), Lago and OpenMeter all solve event ingestion → aggregation → invoice. Scio has ingestion
(four correct, non-throwing, skip-if-zero write sites), aggregation and a ceiling. What it does
not have is a **plan model** — B063, an open product decision, deliberately deferred
(`usage.service.ts:27-30`) — and no vendor supplies that; they all require it as input. Adopting
one now means modelling plans in a third-party system before deciding what plans are. Revisit
when the plan model exists and invoicing is the bottleneck; that day is real, and it is not
today.

---

## 8 · Data worth owning

Layer G touches every request and keeps almost none of what passes through.

| Data | Why it is worth having | Where it already exists |
|---|---|---|
| **The tenancy denial record** — every cross-tenant 404, cap refusal, scoping exception, rejected webhook, dev-auth use | after an incident this is the only evidence there is; before one, it is the measurement that says whether the fence is load-bearing or decorative. `AuditLog` exists, is scoped, and has never been written to (§3.5) | detected at `project.service.ts:30`, `workspace-scope.ts:76`, `build.service.ts:222` |
| **Every ledger row with the rate in force** | §7.2's whole problem. `usage_event` has `model` and `cost` and no rate, so a corrected price table cannot restate history. One column, added before the corpus grows | `usage_event`, four write sites |
| **Swallowed ledger writes** | unbilled spend is currently invisible; the cap reports a floor and nobody knows the gap | the four `catch` blocks |
| **Predicted versus actual cost and tokens, per package kind** | `estimate.py:57-59` asks for exactly this and says it *"needs a real run to calibrate against rather than a coefficient invented here (B115)"*. Every build produces it and discards it | `expected_output_tokens` vs the finished event |
| **Build events, persisted against the job** | one table serves three needs at once: stream resumption (§3.6), the security reveal (§4.5), and the answer to *"what did this build verify?"* which currently lives for one HTTP connection (§6.3) | already emitted in order; `BuildJob` is already the durable row |
| **Consent grants and entry provenance** | without `source_workspace_id` / `licence` / `consented_at`, contributed library entries cannot be withdrawn, traced, or licensed — and the exposure grows with every build (§3.2) | nowhere. This is the one item on this list that has to be *created* |
| **Cap-hit and near-cap events** | the only signal that says whether $50 is the right number, and the input to whatever B063 decides plans are | `ensureCanStart` throws and forgets |
| **Stream disconnects mid-build** | the measurement behind §3.6. How often does a user actually lose the stream? Nobody knows, and the resumption work should be sized on the answer | `res.on("close")` fires and is used only to clear a timer |

Two constraints run under all of it. **ADR-0019 is still *Proposed*** — every row above is
derived from user data, every FK in migration 0001 is `ON DELETE RESTRICT`, and a hard delete
therefore needs an ordered cascade that does not exist. Settle what survives a project deletion
**before** the corpus accumulates, which is the sentence Layer C's §8 also ends on and is more
urgent here, because §3.2's liability is the one that cannot be un-accumulated.

**And the audit log is this document's one exception to "collect less".** Everywhere else the
advice is to stop discarding what already exists; here it is to start writing rows that were
never written, because a security audit trail that begins on the day of the incident is not a
trail.

---

## 9 · ADR proposals

| # | Proposal | Decides |
|---|---|---|
| **G-1** | **Close the cross-tenant idempotency replay** | ownership check before replay in both `run` and `ensureCanStart`; `workspace_id` on `BuildVersion`; and a schema-derived completeness test that does not run against `FakeScope` |
| **G-2** | **The authorization model** | the full one, below |
| **G-3** | **Postgres RLS as the backstop under the application scope** | shared-schema RLS on all fourteen models; a non-superuser application role; `SET LOCAL` inside a transaction via the existing `$extends` hook. Keeps `applyWorkspaceScope`; does not replace it |
| **G-4** | **Consent, licence and provenance for contributed library entries** | `source_workspace_id`, `source_project_id`, SPDX `licence`, `consented_at`; refuse to serve an unconsented entry cross-tenant; whether the grant is opt-in or opt-out. **Product and legal, not engineering** |
| **G-5** | **Verify the Clerk webhook with `@clerk/backend/webhooks`, or delete the route** | `rawBody: true`, `verifyWebhook`, three tests (valid, tampered, stale). No new dependency. The alternative — deleting the route — is also acceptable; leaving it as-is is not |
| **G-6** | **The CI security floor** | `--require-hashes`, `--ignore-scripts`, `pnpm audit` + `pip-audit`, secret scanning, SAST, and a guard on `/docs`. SLSA and Sigstore named as the destination, not this increment |
| **G-7** | **The price table is dated data with a test** | fix Sonnet 5 to $2/$10; add a `checked_on` per model and a staleness check; re-anchor `test_estimate.py`'s cost assertions to token counts rather than dollars |
| **G-8** | **`usage_event` records the rate in force** | one column, and it is the difference between a ledger that can be restated and one that cannot |
| **G-9** | **The allowance is shown, not only enforced** | `/usage/allowance` gets a consumer; the estimate, live spend, actual cost and the failed-build refund question (§4.3) are one product decision, not four |
| **G-10** | **Fail fast in production without a database** | gate `prisma.service.ts:22-24` on `NODE_ENV`, matching `dev-identity-verifier.ts:32-39` and `main.py:75-77`. Keeps the local-dev path unchanged |
| **G-11** | **The audit log gets its first writer** | which events, what retention, and how it interacts with ADR-0019. Blocked on nothing except deciding |
| **G-12** | **Build events are persisted; the stream is resumable** | `GET …/build/events?after=N` from a durable event table. Not a transport change — SSE stays. Serves §3.6, §4.5 and §6.3 together |
| **G-13** | **Observability: OpenTelemetry, correlated on build id** | across API, engine and stream. Adopt rather than invent a logging convention |
| **G-14** | **Housekeeping with security consequences** | `@CurrentWorkspace` throws rather than returning `undefined`; one decimal precision for currency; shared enums generated from the schema; `modules/stream/` deleted; swallowed ledger writes counted |

### G-2 in full — the authorization model

**Decision statement.** Scio adopts *two distinct authorization models for two distinct problems,
and runs no relationship-authorization service for either.*

*For Scio's own tenancy:* `workspace_id` on every model, enforced at the application layer by
`applyWorkspaceScope` (unchanged) **and** at the database layer by Postgres row-level security
(G-3). The model is one relation deep and is expressed as a column and a policy.

*For the generated app:* the architecture's authorization model becomes typed and per-table
rather than a constant boolean and an untyped string — `row_level_security` a per-table decision
carrying its reason, `Permission.scope` a closed enumeration including `"none"`. Policies are
**derived** from that model rather than prompted for, and **verified by execution** on every
build using the existing pglite harness with `SCIO_VERIFY_DATA` on by default.

**Alternatives considered.**

| Alternative | Why not |
|---|---|
| **Adopt OpenFGA or SpiceDB now** | both are excellent and both are a service to run, monitor, back up and keep consistent with Postgres. To express *"a row belongs to a workspace"* that is a second source of truth for an answer a `WHERE` clause already gives. Zanzibar was written for Drive's sharing graph; we do not have one. **Revisit the moment tenancy grows a second relation** — teams, shared projects, an agency with several clients — and revisit it *then* rather than growing special cases first |
| **Cedar as the generated app's runtime authorization** | ADR-0011 fixes the generated stack on Supabase; the enforcement point is Postgres RLS and changing it supersedes an accepted ADR for no user-visible gain |
| **Cedar as an analysable shadow of the generated policies** | genuinely interesting and genuinely unproven (§3.1). **Spike, not decision.** Cedar→RLS is not a solved translation and nobody cited here does it |
| **Schema-per-tenant or database-per-tenant for Scio's own data** | strongest isolation, heaviest operations; current guidance reserves both for hard compliance, residency or contractual isolation requirements. Worth keeping *possible* as a paid tier (§4.6), which mainly constrains the migration story, not the schema |
| **Leave the application scope as the only control** | it is one careless call site from a leak, and F-03 is the proof that "one careless call site" is not hypothetical. `tenant-discipline.spec.ts` is honest about being *"a habit, not a wall"* |
| **Leave `row_level_security: bool = True`** | it is the exact artefact that cannot express the failure CVE-2025-48757 describes: policies that do not match the business logic. A constant cannot mismatch, so it cannot be checked |

**Consequences.**

- Every service still uses the scoped client; RLS is belt-and-braces, and the seven unscoped
  models stop being a class of latent bug (§1.3's 26 call sites become safe by construction).
- The application connects as a non-superuser role and scoped queries run inside transactions.
  With a pooler in transaction mode, `SET LOCAL` is the only safe form — and
  `verification/client.ts:18-23` already documents both traps, in this repository, in our own
  words.
- The generated app's authorization becomes a derivation rather than a generation, which is one
  fewer place a model's judgement decides a security property — the same principle Layer C
  states as *"proposals may add rules; they may not move a rule into a prompt."*
- `SCIO_VERIFY_DATA` on by default makes builds slower and more expensive. That is the price of
  the claim in §4.1, and the claim is worth more than the minutes.
- Two criteria Layer C currently scopes out as unobservable — *"the booking persists"* and
  *"a guest cannot read another guest's booking"* — become observable, which closes a gap Layer
  C's census counts on every single build.

### Ordering

**G-1 first, and it is not close.** A live cross-tenant read in our own product, three lines plus
a migration, and every security claim this document makes is void until it is closed.

**G-5 and G-6 next**, because both are hours rather than days — an import that already exists,
and four CI lines — and because G-6 has a date attached (11 September 2026) that nothing else
here does. **G-14 and G-7** follow: housekeeping and one wrong number, both cheap, both with
consequences out of proportion to their size, and G-7 unblocks any honest statement about cost.

**G-4 must be raised before the next contributed entry**, even though answering it is slower than
the rest: the columns can land immediately and the grant question can take as long as it needs,
but the corpus must not grow while both are open.

Then the two that change what the user experiences — **G-9** (the allowance and the honest bill)
and **G-2/G-3** (the authorization model and its backstop); G-3 is the largest engineering item
here and depends on G-1 having settled the child-table question. **G-12 and G-13** last and
together: the same table and the same correlation key seen from two directions.

### Three open questions this document could not settle

**a. Is the library's cross-tenant contribution model a product decision that has been made?**
ADR-0016 decides the library grows from real builds. Nothing decides that one tenant's build may
supply another tenant's app. Those are different decisions and only the first is written down.
Until the second is answered, §3.2's exposure grows on every build and G-4 cannot be drafted.

**b. What is the cap actually for?** $50/month/workspace, env-configurable, hard-refusing. At
corrected rates that is 18–50 builds (§7.3). Whether it becomes a per-plan column (B063) or stays
a platform-wide circuit breaker with plans layered above decides whether G-9 shows a *balance*
or a *safety limit* — and those read completely differently to a user.

**c. Does the security reveal exist as a moment in the product?** §4.5 and §4.1 both assume the
user is shown what was checked and what could not be. Whether that is part of the existing reveal,
a separate artefact, or something only exported with the code is a product decision, and it
decides whether G-2's verification work is user-visible or merely true.

---

*Written 2026-08-26. Every code claim carries `file:line` and was checked against the working
tree; the model count (14), the scoped-model count (6), the unscoped child-model call-site count
(26), the `NotImplementedException` count (14 across 6 modules), the lockfile figures (52 pinned,
0 hashes), the `UsageKind` gap and the `@clerk/backend` dependency and export surface were
produced by reading the tree, not recalled. Research was scanned 2026-08-26 at
abstract-and-documentation level; nothing was reproduced or benchmarked. CVE scores are quoted
with their authors because two differ. Prices are Anthropic first-party list rates and the cost
arithmetic in §7 is arithmetic on them, not a measurement. Speculation — Cedar as a policy IR,
the per-tenant tier, the SBOM differentiator — is marked as speculation. Nothing here is
implemented.*
