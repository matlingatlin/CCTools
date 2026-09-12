---
title: Supabase row-level security - where app roles live in the JWT, the to-clause, the service role, and what an enabled table with no policy allows, as fetched 2026-09-09
sources:
  - url: https://supabase.com/docs/guides/database/postgres/row-level-security
    note: "Page 'Row Level Security'. No last-updated date visible on the page. Quoted for auth.uid(), auth.jwt(), raw_app_meta_data vs raw_user_meta_data, the to clause, the secret key and bypassrls, and the no-policy default."
    fetched: 2026-09-09
status: verified
tags: [security, postgres, rls, supabase, tenancy, jwt, authorization, scio]
related: ["[[preview-and-sandbox-egress-boundary-2026-09]]", "[[production-site-checklist]]"]
---
# Supabase row-level security, as of 2026-09-09

Why this note exists: Scio renders the generated app's migration and its policies from the
architecture graph (ADR-0020), and the first rendering compared `auth.jwt() ->> 'role'` to an
app role and left a permissive policy open to every Postgres role (review 17, 2026-09-09).
Both were wrong against the vendor's own page. The facts below are what the renderer now rests on.

## Claims

| # | Claim | Source | Verbatim / value | Verdict |
|---|---|---|---|---|
| 1 | `auth.uid()` is the requesting user's id, and null without a session | Supabase RLS | "Returns the ID of the user making the request."; "When a request is made without an authenticated user (e.g., no access token is provided or the session has expired), `auth.uid()` returns `null`." | MEASURED (fetched 2026-09-09) |
| 2 | `auth.jwt()` exposes both metadata columns | Supabase RLS | "Returns the JWT of the user making the request. Anything that you store in the user's `raw_app_meta_data` column or the `raw_user_meta_data` column will be accessible using this function." | MEASURED |
| 3 | Authorization data belongs in `app_metadata`, never `user_metadata` | Supabase RLS | "raw_user_meta_data - can be updated by the authenticated user using the `supabase.auth.update()` function. It is not a good place to store authorization data."; "raw_app_meta_data - cannot be updated by the user, so it's a good place to store authorization data." | MEASURED |
| 4 | A policy on `user_metadata` is a stated security issue | Supabase RLS | "creating an RLS policy that relies on the `user_metadata` claim can create security issues in your application as this information can be modified by authenticated end users" | MEASURED |
| 5 | `authenticated` and `anon` are Postgres roles, named in a policy's `to` clause | Supabase RLS | "These are Postgres Roles. You can use these roles within your Policies using the `TO` clause" | MEASURED |
| 6 | Always name the role; `to authenticated` stops `anon` before the predicate runs | Supabase RLS | "Always name the role a policy applies to, using the `to` clause...This prevents the policy from running for any `anon` users, since the execution stops at the `to authenticated` step." | MEASURED |
| 7 | The secret key acts as `service_role`, which has `bypassrls` | Supabase RLS | "Use a secret key for administrative tasks that need to bypass RLS. A secret key authorizes access through the `service_role` Postgres role, which has the `bypassrls` attribute." | MEASURED |
| 8 | The bypass holds only when no user token rides along | Supabase RLS | "A secret key bypasses RLS only when the request carries no user access token." | MEASURED |
| 9 | RLS enabled with no policy exposes nothing through the publishable key | Supabase RLS | "Once RLS is enabled, no data is accessible through the API when using a publishable key, until you create policies." | MEASURED |

Not established here: the JSON path of the app role inside the token. The page says the
`raw_app_meta_data` column is readable through `auth.jwt()` (claim 2); the conventional path
`auth.jwt() -> 'app_metadata' ->> 'role'` follows from the column name and Supabase's custom-claims
guidance, which this note did not fetch. REPEATED until that page is read.

## What it means here

- **An app role is read from `app_metadata`, never from the top-level `role` claim** (claims 2-4):
  the top-level claim is the Postgres role (`authenticated`, `anon`), so a policy comparing it to
  `'staff'` never matches and silently denies. Scio's renderer
  (`packages/contract/src/spine/render.ts`) now compares `auth.jwt() -> 'app_metadata' ->> 'role'`.
- **Every rendered policy carries `to authenticated`** (claims 5-6). A policy with no `to` clause
  applies to `anon` as well, and the anon key ships in the browser.
- **Auth mode "none" renders no policy at all** (claims 7-9): with RLS enabled and no policy, the
  publishable key reads and writes nothing; the app's server actions use the service role and
  decide access per operation. The permissive `using (true)` policy the first rendering emitted
  would have granted the browser full read and write.
- **A worker with a user token does not bypass RLS** (claim 8): a server path that must bypass
  sends the secret key alone.
- The preview and sandbox side of the same boundary - what the generated app may reach, not what
  its database rows allow - is in [[preview-and-sandbox-egress-boundary-2026-09]]; the anon-key
  plus RLS plus server-side-auth shape a production site needs is item 3, 4 and 6 of
  [[production-site-checklist]].
