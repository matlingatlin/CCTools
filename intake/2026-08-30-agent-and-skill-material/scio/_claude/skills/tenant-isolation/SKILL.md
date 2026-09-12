---
name: tenant-isolation
layer: G
phase: build-time
status: written
description: Make a tenancy claim provable rather than asserted. Use when adding a model, a query or a cache path that could reach another customer's rows; when writing or reviewing row-level security policies, either ours or a generated app's; when someone says the data is scoped by workspace; when choosing between Postgres RLS and an authorization service such as OpenFGA, SpiceDB, Cedar or Oso; when a replay, idempotency or memoisation path short-circuits before an ownership check; or when a green test suite is cited as evidence of tenant safety. Covers the two authorization problems that look alike and have different answers, shared-schema RLS and its four traps, sensitivity labels that survive into the generated database, the cross-tenant zero-rows assertion, and the leak vectors that lint, typecheck and build cleanly.
---

# tenant-isolation

The load-bearing claim, from ADR-0009: *"Everything is scoped by `workspace_id` — tenant
isolation lives in the data layer and is enforced in every query and in authorization."*

Counted at source in `apps/api/prisma/schema.prisma`, 2026-08-26: it is true of **six of
fourteen models**. `WORKSPACE_SCOPED_MODELS` (`auth/workspace-scope.ts:11-23`) holds
`Project`, `User`, `UsageEvent`, `Notification`, `AuditLog`, `BuildJob`. For anything else,
`applyWorkspaceScope` returns its arguments untouched (`:62`). Seven models — including
`BuildVersion`, `SpecVersion` and `DesignVersion` — are protected by a convention kept at 26
call sites, and by nothing else.

That is what this skill is about: **a control that is believed because it is named.**

**Route to what you need:**

| You are here because | Read |
|---|---|
| adding a model, a query, or a replay/cache path | §3 |
| writing or reviewing a generated app's RLS | §4 |
| choosing an enforcement point, or someone said "let's use OpenFGA" | §5 |
| a suite or a gate is being cited as proof | §6 |
| about to quote a number or a CVE score from here | §7 |

---

## 1 · Source

**Zanzibar: Google's Consistent, Global Authorization System** — Pang et al.,
[USENIX ATC 2019](https://www.usenix.org/conference/atc19/presentation/pang). Object–relation–user
tuples, checks and reverse queries over the relation graph; trillions of ACLs, **<10 ms p95,
>99.999% availability**. The reference model, and the thing we are declining (§5).

**CVE-2025-48757 — Lovable.** *"An insufficient database Row-Level Security policy in Lovable
through 2025-04-15 allows remote unauthenticated attackers to read or write to arbitrary
database tables of generated sites."* CWE-863. Two scores exist and they have **different
authors**: **9.3** Critical (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N`) from **MITRE as
CNA**, in the CVE record and [GHSA-773x-pxjg-gxgx](https://github.com/advisories/GHSA-773x-pxjg-gxgx);
**8.26** base / 7.58 temporal from the **reporting researcher**. Vendor acknowledgement
2025-03-24, disclosure 2025-04-15, *"Patches and Updates: None available."*

**Practitioner guidance:** [PlanetScale, *Approaches to tenancy in Postgres*](https://planetscale.com/blog/approaches-to-tenancy-in-postgres);
[Atlas, *Testing RLS*](https://atlasgo.io/faq/testing-rls) and pgTAP for the two canonical
assertions; Prisma Client Extensions, because Prisma has no RLS support in its schema language.

**Mined:** `docs/mined/PASS2-ECC-SKILLS.md` rows 41, 62, 63 (ECC `healthcare-phi-compliance`,
`react-performance`); `docs/mined/PASS2-FOUR-REPOS.md` P2-17 (claude-context `context.ts:504-521`,
a live defect); `docs/mined/PASS2-GSTACK-TESTS.md` §3.4; `docs/mined/PASS2-GSTACK-SKILLS.md`
row 8; `docs/mined/PASS2-ECC-RULES-COMMANDS.md` M15.

**Ours, and it is the strongest instrument here:** `library/verification/client.ts`, which runs
a generated app's own queries against in-process PostgreSQL with RLS actually in force.

---

## 2 · Two problems that look alike and have different answers

Confuse them and every argument that follows is about the wrong thing.

| | **Scio's own tenancy** | **The generated app's authorization** |
|---|---|---|
| Subject | a workspace | the end user of a built app |
| Enforced by | `applyWorkspaceScope`, in the application layer | Supabase RLS policies, generated (ADR-0011 fixes the stack) |
| Model today | a set of six model names | `row_level_security: bool = True` and `scope: str` |
| Blast radius | one tenant reads another's build metadata | **CVE-2025-48757** |

They share one discipline — an isolation claim must be provable — and almost nothing else.
§3 is the first; §4 is the second.

---

## 3 · Scio's own tenancy

### 3.1 The ordering rule: nothing may short-circuit before the ownership check

The live defect, verified at `apps/api/src/modules/build/build.service.ts:517-525`:

```ts
if (idempotencyKey) {
  const already = await this.buildFor(workspaceId, projectId, idempotencyKey);
  if (already) { await emit("finished", this.replayOf(...)); return; }   // ← returns here
}
const project = await this.project(workspaceId, projectId);              // ← the ownership check
```

`buildFor` queries `buildVersion.findFirst({ where: { projectId, idempotencyKey } })` on the
**scoped** client. `BuildVersion` is not in `WORKSPACE_SCOPED_MODELS`, so the scope is a no-op
and **the `workspaceId` argument selects the client without touching the query.** The
idempotency key is a client-supplied header (`build.controller.ts:76`). The same shape exists
in `ensureCanStart` (`:202`, ownership at `:233`).

**The rule, stated so it is checkable:** *every* early return — replay, idempotency, cache hit,
memoised result, "already running" — is an authorization decision, and must come **after** the
ownership check, not before it. A path added because it must be cheap is exactly the path that
skips the expensive thing.

**A scoped client that scopes nothing is worse than a raw one**, because the argument reads as
the control. If a model is outside the scoped set, the query has to carry the tenant itself.

### 3.2 The reduction key of an append-only ledger includes the tenant, and the database reduces

`usage.service.ts:62-68` answers *"what has this workspace spent this period"* by calling
`findMany` for every row of the month and reducing in Node. `aggregate` is already in
`READ_OPERATIONS` (`workspace-scope.ts:33`), so the scoped client would pass it through.

Two failures in one shape. **Correctness:** a ledger whose reduction key is applied by the
consumer is a ledger that can be reduced with the wrong key. **Bounded response:** a busy month
loads its whole ledger to answer one number. Declare the reduction key — `(workspace_id,
period)` — with the ledger, and let the database apply it.

### 3.3 Identifiers derived from user text are query parameters, never interpolated

claude-context interpolates a user-derived identifier into a query at `context.ts:504-521`.
This is the same boundary `untrusted-text-boundary` draws for prompts, drawn for queries — and
for filesystem paths. That skill owns the prompt side; the query side is here because the consequence
is tenancy, not injection alone.
Under RLS it is worse than ordinary injection, because a successful injection runs *as the
session*, and the session is what the policy trusts.

### 3.4 Cross-tenant responses: 404, not 403

Chosen and documented at `project.service.ts:30`. A 403 confirms the resource exists. Keep it.

---

## 4 · The generated app

### 4.1 Type the model before anything else

At source: `architecture.py:49` and `:144` declare `row_level_security: bool = True`, and
`derive.py:384` passes `True` unconditionally — no code path sets it false.
`architecture.py:83` declares `scope: str = "own"` with the enumeration **in a comment**.
`contract.py:57` renders this into the build prompt as `table booking (row-level security:
True)`; `contract.py:114` as `security posture: RLS=True`.

**That is the artefact that cannot express Lovable's failure.** The CVE was not RLS being off;
it was *"projects deployed with RLS policies that don't match the business logic."* A boolean
that is always true has no content, and a model asked to write policies from it is guessing.

Three steps, in order, each making the next possible:

1. **Type it.** `scope: Literal["own","all","none"]` — the third value the domain obviously has
   and this one does not. `row_level_security` becomes a per-table decision carrying its reason.
2. **Derive the policy; do not prompt for it.** A `Permission` plus an owner column determines
   the policy text. Generating SQL from a typed permission is a template, not a judgement.
   Layer C's refusal discipline already has the shape: `scripts.py:195` refuses to emit the
   isolation criterion when `table is None or not owner or not table.row_level_security`.
3. **Verify the policy against the model on every build** — §6.

### 4.2 Sensitivity labels that survive into the database

From ECC's `healthcare-phi-compliance`, and it is the mechanism, not the domain:

```sql
COMMENT ON COLUMN patients.name IS 'PHI: patient_name';
COMMENT ON COLUMN doctor_payouts.amount IS 'PII: financial';
```

Layer B already types every field. Emitting the classification as a column comment makes it
**survive into the generated database**, which turns four leak rules from name heuristics into
decidable checks: *is a labelled column named in a route path, in a `console.log`, in a
`localStorage.setItem`, in a client component's props?* Neither Scio's `Playbook` nor ECC's has
any notion of a labelled column, and without one every leak rule is a regex over identifiers.

The five prose rules the labels make checkable — never put identifying data in errors thrown to
the client, in logs, in URL parameters, in browser storage; never use the `service_role` key in
client-side code — are worth carrying verbatim; they apply to any generated app with a users
table.

### 4.3 The zero-rows assertion, written beside the policy

```sql
CREATE POLICY "facility_isolation" ON patients FOR SELECT TO authenticated
  USING (facility_id IN (SELECT facility_id FROM staff_assignments WHERE user_id = auth.uid()));
-- Test: login as doctor-facility-a, query facility-b patients — Expected: 0 rows returned
```

`LAYER-B` §3.5 already proposes the deterministic half — a policy per operation, never
`USING (true)`. **The half nobody holds is evidence that the policy isolates**, and the shape is
one line: for each tenant-scoped table, a cross-tenant read that must return zero rows. It is a
derivable acceptance criterion, and it is the surface where CVE-2025-48757 actually landed.

pgTAP and Atlas add the second canonical assertion: **the query plan still uses a
tenant-leading index.** A policy that is correct and unindexed becomes a policy somebody turns
off under load.

### 4.4 Leak vectors that lint, typecheck and build cleanly

- **Mutable module-level state in RSC/SSR.** *"Module state is shared across all requests."* In
  a server-rendered generated app this is a cross-tenant leak that passes every gate Scio has,
  including `_UNSAFE_PATTERNS`. ~22 tokens of `Playbook` text; nothing else catches it.
- **An unscoped search or query when the intended scope could not be resolved.** gstack refuses
  rather than widening, because *"an unscoped search pulls corpora that would be mislabeled."*
  Widening on failure is failing open.

---

## 4b · RLS decides which rows, never which columns

*Added 2026-08-26 after an ablation found this skill cites CVE-2025-48757 three times and never
names its column-level twin.*

A row-level policy answers *may this user touch this row*. It has no opinion about **which fields
of that row they may set**. So a handler that writes a payload straight into an update lets a user
change their own row's `role`, `owner_id` or `workspace_id` — and every policy passes, because the
row was always theirs.

```python
# The row check succeeds. The privilege escalation succeeds with it.
await db.update(table="member", where={"id": me}, values=await request.json())
```

That is **mass assignment**, and it is the same failure as the CVE at a different granularity: the
CVE is *no policy*; this is *a correct policy asked the wrong question*.

**Two mechanisms, and you need both.**

1. **An explicit writable-column allowlist per operation**, derived from the architecture rather
   than hand-maintained. A field absent from the allowlist is dropped, not rejected — rejecting
   tells an attacker the field exists.
2. **`WITH CHECK`, but not for the reason this section first gave.**

   > **Corrected 2026-08-26, measured.** This section originally claimed a policy with `USING`
   > alone lets a user update a row out of their own tenant. **That is false.** When `WITH CHECK`
   > is omitted, Postgres applies `USING` to the *new* row as well, so the hop is already refused.
   > Verified on Postgres 18.3 via pglite: `USING (tenant = 'A')` with no `WITH CHECK`, then
   > `UPDATE … SET tenant='B'` → `new row violates row-level security policy`. The error was
   > written into this skill hours after an ablation found the section missing — a gap closed with
   > a defect.

   `WITH CHECK` earns its place only when the write rule must be **narrower than the read rule**.
   `USING` alone means *whatever you may read, you may write*. A policy that lets a member read
   every row in their workspace but write only their own needs the two clauses to differ, and that
   is the case worth stating — not a tenant hop, which the default already refuses.

   **And `WITH CHECK` does not stop the mass assignment above.** It validates the resulting row
   against a predicate; it has no opinion about which columns the caller supplied. Only the
   allowlist closes that.

**The assertion that catches the real failure:**

> As tenant A, update your own row setting a field the allowlist does not contain — `role`, or
> `owner_id`. **The write must drop the field**, and a read must show it unchanged.

A tenant-hop assertion passes on a correct *and* an incorrect policy here, so it tests nothing;
this one fails whenever the allowlist is absent.

**Limit:** this is a mechanism, not a measurement. Nothing here shows how often generated apps
carry the defect; the CVE shows only that the row-level half was missing in 170+ published apps.

## 5 · Choosing an enforcement point

| Option | What it is | Honest cost |
|---|---|---|
| **Zanzibar** (paper) | the reference model: tuples, checks, reverse queries | free — read it before designing anything |
| **OpenFGA** — CNCF Sandbox, Auth0/Okta | the most approachable implementation; DSL, check/list/expand over your database | **a service to run**, plus a tuple store to keep consistent with Postgres. Two sources of truth for *who may see this* is a bug class we do not have |
| **SpiceDB** — Authzed | the most faithful; Watch API, ZedToken consistency | as above, plus a consistency model the team must understand |
| **Cedar** — AWS, formally verified evaluator | policies as versioned, machine-analysable artefacts | a language to generate and validate; **no service required if used as an artefact rather than a runtime** |
| **Oso** | policy-as-library, embedded | a smaller commitment and a smaller answer |
| **Postgres RLS, shared schema** | policies in the database | one migration per table, a non-superuser role, and a session-variable discipline |

**The recommendation, and it is deliberately unfashionable: do not run a ReBAC service for a
one-relation model.** Zanzibar exists because Drive has sharing, groups, nested folders and
inheritance. Adopting OpenFGA to express `project.workspace_id = :ws` buys an operational
dependency, a second source of truth and a consistency window to model what a `WHERE` clause
already models. **Revisit the moment a second relation appears** — team members, shared
projects, an agency managing several clients — because that is when a hand-rolled model starts
accreting special cases, which is the failure Zanzibar was written about.

For the generated app, ADR-0011 fixes the stack, so the enforcement point is Postgres RLS and
cannot be anything else without superseding an accepted ADR.

### 5.1 The four traps, all of which are already documented in our own code

`library/verification/client.ts:18-23` states three of them in our words:

1. **A superuser bypasses RLS entirely.** pglite connects as `postgres`. *"A naive setup would
   report every policy as working."*
2. **`SET LOCAL` outside a transaction is a silent no-op** — *"that is why the transaction is
   not optional."* Behind a pooler in transaction mode, `SET LOCAL` is the only safe form.
3. **A tight grant is not a policy.** `:76-83` grants **all** privileges to `authenticated` and
   `anon` on purpose: *"the POLICY decides, not the grant. A tighter grant looks like RLS
   working and is not."*
4. **Prisma has no RLS in its schema language.** Policies live in raw SQL migrations; the tenant
   is set with `SET LOCAL` inside a transaction, injected by a Client Extension —
   and `WorkspaceScope.forWorkspace` (`workspace-scope.ts:91`) already *is* a `$extends` query
   extension. **The hook is built; only the policy layer is missing.**

**Belt and braces, not replacement.** The application scope stays. RLS is what makes the
twenty-seventh call site safe when someone forgets.

---

## 6 · Proving it

### 6.1 A control declares whether it is the enforcement point

**The rule itself belongs to `gate-verdicts`** — *every gate declares whether it is the
enforcement point, and names the real one if it is not*, from gstack's egress test
(*"THREAT MODEL: … it records ATTEMPTED egress so accidents are auditable; **it is not an
exfiltration control**"*). Read it there. What is here is why a tenancy control fails this rule
in a particular way: an isolation control that is *not* the enforcement point is usually cited
as though it were, because its name says what it does and not where it stops.

Scio's positive instance: `.github/workflows/ci.yml` is a hermeticity check, not a security
check, and does not claim to be. Scio's negative instance: `tenant-discipline.spec.ts:15-19`
predicts this exact defect **in prose**, then greps for `this.prisma.<model>` — the raw client —
while the live defect is on the scoped one. **A fence that names the failure and misses it in
code is worse than no fence, because it is counted as coverage.**

The companion rule, also `gate-verdicts`': every destructive action ships a **non-scope list** —
what it does *not* touch — and an undo.

### 6.2 The suite may not be stricter than production

`FakeScope` in `build.e2e.spec.ts:105-108` enforces `owns(where.projectId)` on
`buildVersion.findFirst` — the exact call that is unguarded in production — while
`workspace-scope.spec.ts:37` asserts that production *does not*. **Two suites assert opposite
things about the same mechanism and both pass**, so every cross-tenant e2e assertion passes for
two reasons at once and cannot distinguish them. A double stricter than reality cannot fail; it
can only certify. See `testing` §1(a) and §4, where this case is the worked example.

### 6.3 Three layers for one privacy promise

For every sentence put in front of a user about what does not leave their machine or their
tenant, gstack asserts three things, and any one alone is theatre:

1. **Coverage** — every place the thing could leave is enumerated, with no unexplained
   exemption bucket.
2. **Behaviour of the actual filter** — the real function, on real input, not a re-implementation
   written for the test.
3. **A floor** — the promise still holds at the boundary case where the mechanism degrades.

`verification/client.ts` is layer 2 for RLS and it is stronger than pgTAP-in-CI, because it
drives the application's own queries rather than SQL written for the test. **It runs only when
`SCIO_VERIFY_DATA=1`** (`verification/__init__.py:11,38`), so on every default build the
strongest security check in the system does not run. A control that is off by default is layer
1 at best.

---

## 7 · Limits — what the sources show versus what we would be assuming

- **Zanzibar's numbers are Google's, at Google's scale, for Google's relation graph.** <10 ms p95
  and >99.999% say what a dedicated service can achieve; they say nothing about a two-model
  tenancy, and they are not an argument for adopting one. They are the measure of what is being
  declined.
- **The tenancy guidance is practitioner consensus, not a study.** PlanetScale's shared-schema
  recommendation has no controlled comparison behind it. It is the current mainstream answer and
  should be cited as that.
- **The CVE tells us a competitor failed. It does not tell us we succeed.** Cite **9.3 as the
  CVE record and 8.26 as the reporter's own assessment; never present one as a correction of the
  other.** The widely repeated *"303 endpoints across 170+ apps, 10.3% of projects analysed"*
  appears only in secondary coverage — the primary advisory states no scan counts. A 2026 press
  report of a mass Lovable exposure is single-source and must not be leaned on externally.
- **The sensitivity-label mechanism is ECC playbook prose, not a measured control.** Nobody has
  shown it reduces leaks. What it does, demonstrably, is turn four regex-over-identifier rules
  into queries against a labelled schema — which is a change in kind, not a measured effect.
- **Cedar-to-RLS is not a solved translation.** Emitting the permission model as an analysable
  Cedar policy set beside the SQL is a **spike**, not a plan. Nobody cited here does it.
- **Scio's own tenancy has never been fuzzed.** Every claim in §3 rests on reading 26 call sites
  once, on one date. Reading is not a property test.
- **This skill has no measured effect on anything.** `status: written`. It carries verified code
  positions and published sources; it carries no evidence that using it changes an outcome.

---

## 8 · Eval

### E1 · The replay reproduction
Two workspaces, one project UUID and one idempotency key. Call the build endpoint from the
wrong workspace with the matching key. **Expected: 404.** Today it returns the other tenant's
`git_sha`, honest-status summary, `total_cost_usd` and `total_tokens`. A fix that moves the
ownership check above the replay must make this case fail loudly, and it must fail against
**production code**, not against a double (E4).

### E2 · Scoped-model completeness
Enumerate every model in `schema.prisma` and every model named in `WORKSPACE_SCOPED_MODELS`.
For each model in neither set, report every non-test query site that touches it. **Expected
today: eight models unscoped, 26 call sites, 24 of which open with an ownership check.** The
two that do not are E1. This case is the map, and it must be re-run whenever a model is added.

### E3 · `SET LOCAL` outside a transaction
Set the tenant GUC outside a transaction, then run a scoped query. **Expected: the query
returns rows it must not**, and the harness must detect it rather than pass. A test that cannot
produce this failure is not testing RLS.

### E4 · A double stricter than production
Diff every method a test double implements against the production function it stands in for.
**Any operation the double refuses and production allows fails the case.** `FakeScope` versus
`applyWorkspaceScope` is the reference instance.

### E5 · Zero rows, per tenant-scoped table
For every table with a tenant column, a cross-tenant read as `authenticated` inside a
transaction with the other tenant's claims. **Expected: 0 rows, every table, no exceptions.**
Generated beside the policy, not written later.

### E6 · The plan still uses a tenant-leading index
`EXPLAIN` the same query. **Expected: an index scan on a tenant-leading index.** A policy that
forces a sequential scan is a policy with an expiry date.

### E7 · A labelled column in a leaky place
Label one column `'PII: …'`. Grep the generated app for that column name in a route path, a
`console.log`, a `localStorage.setItem`, and a client component's props. **Expected: each hit
is a finding with a file and a line.** With no label, the same search is a name heuristic and
this case cannot be written.

### E8 · The gate declares its own scope
For each security-relevant gate, assert its file states whether it is the enforcement point.
**`ci.yml` passes. `tenant-discipline.spec.ts` fails** — it claims a boundary it does not check.

---

## 9 · When this skill is the wrong tool

- **Feature authorization inside one tenant** — roles, sharing, approval chains. That is the
  second relation, and §5's answer changes the moment it exists.
- **Deciding what Scio actually adopts.** The enforcement point, the seven missing
  `workspace_id` columns, the consent model for `library_entry`, whether `SCIO_VERIFY_DATA`
  becomes the default: each is a decision with a cost and belongs in an ADR. This skill says how
  to argue them and what to assert afterwards.
