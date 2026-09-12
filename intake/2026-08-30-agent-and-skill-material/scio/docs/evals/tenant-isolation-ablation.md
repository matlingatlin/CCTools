# Ablation · `tenant-isolation`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

## The discriminating rule, and why the obvious answer is wrong

§5.1, *the four traps*, three of which are stated in our own
`library/verification/client.ts:18-23`:

1. **A superuser bypasses RLS entirely.** *"A naive setup would report every policy as working."*
2. **`SET LOCAL` outside a transaction is a silent no-op** — *"that is why the transaction is not
   optional."*
3. **A tight grant is not a policy.** `client.ts:76-83` grants **all** privileges to
   `authenticated` and `anon` **on purpose**: *"the POLICY decides, not the grant. A tighter grant
   looks like RLS working and is not."*

Plus §6.2: **the suite may not be stricter than production.** A test double that refuses what
production allows *"cannot fail; it can only certify."*

Trap 3 is the one where the obvious answer is not just incomplete but backwards. Every instinct
says defence in depth: lock the grants down as well as the policy. Do that in the *test harness*
and the harness stops testing RLS — the grant blocks the query, the assertion passes, and the
policy is never exercised. Deliberately granting everything to make the test real is the opposite
of what a careful engineer does by reflex.

**A note on what this skill does not contain.** The brief for this pass proposed the discriminating
rule as *RLS decides which rows, never which columns* — mass assignment, a user updating their own
row to set `role` or `owner_id`. `grep -in "mass assign|which columns|column-level|WITH CHECK"
SKILL.md` returns **nothing**. The rule is not in the skill, so an ablation on it would measure the
model, not the skill. The nearest thing present is §4.3's zero-rows assertion, which is a read-side
`SELECT` check, and `LAYER-B` §3.5's *a policy per operation, never `USING (true)`*. **That gap is
itself a finding: the column-level twin of CVE-2025-48757 is absent from the skill that carries the
CVE.** It should be added; it was not measured here.

## The question

> We've turned on Postgres row-level security so each customer only sees their own rows. I want a
> test in CI that proves the isolation actually holds. What should the test do? Four bullets max.

No skill, no file, no unique term. "Proves the isolation actually holds" is the bait: it invites a
test that asserts an outcome rather than one that first proves it is capable of failing.

## Control answer

Verbatim.

> - **Seed two (or more) tenants** with known rows via a fixture/migration, then connect as each
>   tenant's DB role (not a superuser/bypassrls role) and assert `SELECT`/`UPDATE`/`DELETE` on
>   another tenant's rows returns zero/errors while its own rows are fully visible.
> - **Enumerate every table with RLS enabled** (query `pg_tables`/`pg_policies`) and fail the test
>   if a table has RLS enabled but no policy, or has rows but RLS disabled — so a new table without
>   a policy can't silently ship exposed.
> - **Try the bypass paths**: run the same cross-tenant query as the app's connection pooling role,
>   through any views/functions (`SECURITY DEFINER` functions especially), and via raw SQL with
>   `SET ROLE`, to catch places where RLS is quietly bypassed.
> - **Assert on the query plan/policy application**, not just app-layer results — e.g. `EXPLAIN`
>   shows the RLS filter applied — so the test still fails if someone flips
>   `FORCE ROW LEVEL SECURITY` off or a superuser-owned connection accidentally skips RLS, rather
>   than only testing what your ORM happens to send.

## Treatment answer

Verbatim.

> Four things the test must actually do (not just assert):
>
> - **Connect as the real app role, not superuser, and run genuine application queries inside a
>   transaction** — set the tenant via `SET LOCAL` (never bare `SET`, which is a silent no-op
>   outside a transaction), grant full table privileges to that role, and let the *policy* be what
>   blocks access. If the test connects as `postgres` or a role with a tightly scoped `GRANT`, it
>   can pass while RLS itself does nothing.
> - **For every tenant-scoped table, read as tenant A while `SET LOCAL` is set to tenant B's id and
>   assert zero rows returned** — one case per table, generated alongside each policy at creation
>   time rather than written later, so a new table can't ship without its own proof.
> - **Also try to write/update a cross-tenant row and assert it's rejected**, not just filtered out
>   of reads — RLS has separate `USING` and `WITH CHECK` clauses, and a policy that hides rows on
>   `SELECT` but not on `UPDATE`/`INSERT` is the exact class of bug CVE-2025-48757 was.
> - **Diff the test double against production, not the mock's own logic** — drive the assertions
>   through the actual query layer/client the app uses in production (not a hand-rolled test
>   harness that re-implements the check), so the suite can't be stricter than what's really
>   enforced. A double that refuses something production allows will pass this test and still ship
>   a leak.
>
> Bonus, cheap to add: `EXPLAIN` one of the cross-tenant queries and assert it still hits a
> tenant-leading index — proves the policy won't get disabled the first time someone complains
> about a sequential scan under load.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Do not connect as superuser / `BYPASSRLS` | **yes** — named explicitly | yes |
| Cross-tenant read returns zero rows, per table | yes | yes, **plus generated beside the policy** so a new table cannot ship without its proof |
| `SET LOCAL` must be inside a transaction; bare `SET` is a silent no-op | **absent** — the control isolates by connecting as a per-tenant role, so the GUC never arises | **present**, named as the reason the transaction is not optional |
| Grant permissively **on purpose**, so the policy is what blocks | **absent, and the harness is grant-shaped** — a per-tenant role can pass on privileges alone | **present** — *"a role with a tightly scoped `GRANT` … can pass while RLS itself does nothing"* |
| Writes tested separately from reads (`USING` vs `WITH CHECK`) | partially — asserts `UPDATE`/`DELETE` on another tenant's rows, but as a read-shaped "zero/errors" claim | **explicitly**, with the two clauses named and tied to the CVE |
| Drive production's own query layer; double must not be stricter | **absent** | **present** — §6.2, the failure mode named |
| `EXPLAIN` / plan assertion | present, aimed at *"is the RLS filter applied"* | present as a bonus, aimed at *"is a tenant-leading index used"* — a durability check, not a correctness one |
| Enumerate RLS-enabled tables with no policy | **present** | absent |
| `SECURITY DEFINER` functions, views, pooler role as bypass paths | **present** | absent |

This is a partial overlap, and it goes both ways. The control found two mechanisms the treatment
did not (the `pg_policies` census, `SECURITY DEFINER` bypasses) and independently found trap 1.

## Verdict

**Changed the outcome, narrowly** — with the overlap stated.

The decisive item is trap 3. The control's harness isolates tenants **by connecting as a per-tenant
role**. That design can pass with no working policy at all, because the role's privileges do the
blocking — precisely the *"a tighter grant looks like RLS working and is not"* failure. The control
avoided trap 1 and walked into trap 3, and trap 3 is the one that produces a green suite over an
unenforced policy. The treatment named grant-permissiveness, the transaction requirement, the
`USING`/`WITH CHECK` split, and the double-versus-production rule.

It would be dishonest to call this the clean split that `contract-retrieval` and
`reuse-classification` produced. Two of four control bullets are sound and one is a mechanism the
treatment missed. The skill's contribution here is not a different answer — it is the three
harness-invalidating traps, without which the control's otherwise reasonable test can certify
nothing.

## Limits of this measurement

n=1 per arm, unblinded, one question. No repeats; variance unmeasured. One question cannot cover a
376-line skill — §3 (Scio's own tenancy, the idempotency replay defect), §4.2 (sensitivity labels)
and §5 (choosing an enforcement point) were not reached at all, and the column-level rule the brief
asked about **is not in the skill to reach**.

The verdict rests on reading the control's harness design as grant-dependent. That is an inference
from four bullets, not from running the harness; a control asked a follow-up might have added the
permissive grant unprompted.

The two confounds that apply to every file in this series:

1. **`graphify` is installed at account level** (`/root/.claude/skills/graphify/`) and loads in
   both arms. "No project skills" is not "no skills"; the control also carries the user's global
   `CLAUDE.md`.
2. **The control directory is not the treatment directory minus skills.** It holds `CLAUDE.md` and
   `docs/as-built/` only; the treatment is the live `scio` repo, which also holds `docs/next/`,
   `docs/mined/`, `docs/triage/`, `scripts/` and `graphify-out/`.
