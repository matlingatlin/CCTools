# ECC's remaining rules and commands

*Mined 2026-08-26 from `affaan-m/ECC`, second pass. Covers the two surfaces the first two passes
left: the seventeen language rule directories surveyed only by heading in `ECC-RULES.md`, and the
94 command files of which `ECC-AGENTS.md` read only `gan-build`, `orch-*`, `multi-*` and `plan`.*

*The earlier verdict on the seventeen was "noise, because ADR-0011 fixes our generated stack."
Half of this document is a test of that verdict. It is **mostly right and wrong in two specific
places**, one of which is embarrassing.*

*Discipline carried over unchanged: the playbook ships in **every** package prompt (≈670 tokens ×
six packages ≈ 4,000 per build), so every candidate gets **playbook text**, **deterministic
check**, or **leave** — and the playbook ones are priced against the ~1,200-token cap.*

## Coverage

| Surface | Size | What I actually did | Coverage |
|---|---|---|---|
| 17 language dirs — **prose + headings** | 1,965 lines of 6,844 | Read every non-blank, non-fenced, non-frontmatter line, with file attribution | **100%** of prose |
| 17 language dirs — **fenced code** | 2,855 lines (41.7%) | **Not read line-by-line.** Sampled where prose flagged something | ~5% |
| 17 language dirs — blank / frontmatter | 2,024 lines (29.6%) | Counted, not read | n/a |
| Whole corpus greps | 122 rule files + 94 commands | 25 topic greps, every hit inspected | 100% |
| **Commands read in full** | 30 files, ~4,600 lines | `code-review`, `prp-{plan,prd,implement,pr,commit}`, `santa-loop`, `save-session`, `resume-session`, `aside`, `harness-audit`, `quality-gate`, `checkpoint`, `test-coverage`, `build-fix`, `refactor-clean`, `update-codemaps`, `update-docs`, `cost-report`, `security-scan`, `project-init`, `ecc-guide`, `learn`, `learn-eval`, `feature-dev`, `plan-prd`, `loop-start`, `loop-status`, `model-route`, `gan-design`, `pr`, all 7 `epic-*` | ~37% of 12,349 lines |
| **Commands read structurally** | 22 files, 4,044 lines | The `*-review` / `*-build` / `*-test` per-language family: heading skeletons diffed across all 22, two read in full (`python-review`, `go-review`) | skeleton + 2 |
| **Commands measured, not read** | remainder | Frontmatter of all 94; pairwise textual similarity of all 4,371 pairs; delegation, script-invocation and alias greps over all 94 | metadata 100% |
| Already covered by pass 1 | `gan-build`, `orch-*`, `multi-*`, `plan` — 13 files, 1,735 lines | Not re-derived | — |

**Not achieved:** I did not read the ~7,700 lines of the `*-review`/`*-build`/`*-test` bodies or
the 2,855 lines of fenced language code. I argue in §1 why that is the right cut, and I say what
it would cost to be wrong.

**The blunt number.** 6,844 lines of "noise" produced **fourteen** passages worth quoting, of
which **two** change the playbook and **three** become checks. 12,349 lines of commands produced
**twenty** mechanisms, of which **none** belong in the playbook and **most** belong to Layer C,
Layer E or the build process. The commands are worth far more than the rules, which inverts the
order the first two passes went in.

---

## 1 · The seventeen directories — was "noise" the right verdict?

**ADR-0011, verbatim from `docs/as-built/01-DECISIONS.md`:** *"Generated apps: Next.js + TS +
Tailwind + Supabase, fixed"*, with the note *"this is the **output** stack, not Scio's own."*
The register also carries **ADR-0006 — "NestJS backend + separate Python FastAPI engine"**,
Accepted, layer *all*. Both matter below.

### Where the verdict holds

The composition of the seventeen, measured rather than asserted:

| | Lines | Share |
|---|---|---|
| Fenced code (Rust, Dart, Perl, Swift, ArkTS…) | 2,855 | 41.7% |
| Blank | 1,476 | 21.6% |
| Headings | 622 | 9.1% |
| YAML frontmatter | 548 | 8.0% |
| **Prose — the only transferable surface** | **1,343** | **19.6%** |

Four-fifths of these directories cannot transfer by construction: a `#[test]` block or a
`StyleSheet.create()` example is the language, not a principle. And the prose repeats. Nine of the
seventeen `security.md` files state secret management, SQL parameterisation, input validation and
safe error responses in near-identical words; `csharp/security.md` and `fsharp/security.md` are
the same file with the type names swapped. The pass-1 count stands: **one rule in twenty-one
syntaxes.**

Directories that yielded **nothing** transferable, stated so a "leave" is accountable:
`cpp/` (229 lines — RAII, rule of five, sanitizers), `golang/` (159 — the thinnest in the corpus,
five files that mostly point at a skill), `swift/` (211), `perl/` (267 — taint mode is the one
idea and it is 1990s CGI), `fsharp/` (387 — a verbatim copy of `csharp/` plus railway-oriented
programming), `arkts/` (791 — 154 lines of "ArkTS forbids `any`, forbids destructuring, forbids
`delete`", which is a compiler manual), `java/`, `kotlin/`, `rust/`, `dart/`, `angular/`, `vue/`
patterns and testing files. That is roughly **5,900 of 6,844 lines with nothing in them for us.**

### Where the verdict is wrong — the embarrassing one

**`rules/python/fastapi.md` is a rules file for Scio's own engine.**

ADR-0011 fixes the *output* stack. The "noise" verdict was reasoned entirely from ADR-0011 and
therefore skipped `python/` — but ADR-0006 makes Scio's engine a **Python FastAPI service**, and
`python/fastapi.md` is 59 lines of FastAPI house rules that apply to the code in
`apps/engine/src/scio_engine/` today. Six of them are load-bearing and none are in our repo's
conventions:

> - Never include passwords, password hashes, access tokens, refresh tokens, or internal auth state in response models.
> - Do not call `requests`, sync SQLAlchemy sessions, or blocking file/network operations from async routes.
> - Do not combine wildcard origins with credentialed CORS.
> - Validate JWT expiry, issuer, audience, and algorithm.
> - Rate-limit auth and write-heavy endpoints.
> - Redact credentials, cookies, authorization headers, and tokens from logs.

The second is the one that bites us: an engine that orchestrates sandbox runs and relay calls from
`async def` handlers, and which does any blocking work inline, stalls its event loop under exactly
the load a build produces. That is a bug class, not a style note. The testing clauses —
*"Override the exact dependency used by `Depends`"*, *"Clear `app.dependency_overrides` after
tests"* — are the two failure modes of FastAPI test suites and cost nothing to adopt.

**This is not a playbook question at all. It is for our build process,** and it is the single
strongest argument that "screen the language directories against the output stack" was the wrong
screen. The right screen is *against both stacks*, because ADR-0006 exists.

### Where the verdict is wrong — the substantive one

**Cross-language security prose is where the corpus's rarest ideas live, precisely because the
`common/` file is generic and the language files are where someone wrote down a real incident.**
Two of them name bug classes our fixed stack has and our playbook does not: mass assignment
(§2.1) and the redirect-from-a-query-parameter (§2.2). Both were found in Ruby and PHP files —
directories with zero syntactic relevance to us. Both apply verbatim to a Supabase client call.

### What a "second reader" costs

If I am wrong about the 7,700 unread lines of `*-review`/`*-build`/`*-test` command bodies, the
loss is a per-language checklist item. If I am wrong about the 2,855 lines of fenced code, the
loss is a comment inside an example. Neither can contain a principle its own prose does not state,
because in this corpus the prose is the rule and the code is the illustration — I verified that on
the four files where a code comment looked load-bearing. **Confidence: high on the code, high on
the build/test bodies, medium on the `*-review` bodies**, which are the one place a language file
enumerates real defects (see §4.3).

---

## 2 · Principles that transcend their language

Fourteen passages survived the screen. Here they are, with the layer each attaches to and a
verdict. Four are genuinely new to us; the rest corroborate, sharpen, or fail.

### 2.1 · Mass assignment — the best find in the seventeen · **Layer B · SHIP · +48 tokens**

> `ruby/security.md` — "Use strong parameters or typed boundary objects before mass assignment."
> `php/security.md` — "Scope ORM mass-assignment carefully and whitelist writable fields."

Two directories with no syntactic bearing on our stack, naming a bug class our fixed stack has and
our playbook does not. The generated shape is:

```ts
await supabase.from('projects').update(await req.json()).eq('id', id)
```

**RLS does not stop this.** A policy of `USING (auth.uid() = owner_id)` decides *which rows* a
caller may write; it says nothing about *which columns*. A user updating their own row can set
`role`, `is_admin`, `workspace_id`, `owner_id`, `plan`, `credits` or a `created_at` — every one of
which is a field a CRUD app generated from an entity list will have. It is the column-level twin of
CVE-2025-48757, and the playbook's existing RLS sentence is read by a model as covering it.

Proposed text, deliberately naming the columns rather than the concept:

> "Never write a request body straight into an insert or update. Name the columns the caller may
> set. Ownership, tenancy, role and timestamp columns are set by the server, never by the client."

**Why prompt text and not a check:** a check would need to know which columns are privileged, which
is a property of the architecture graph, not of the file. A *Layer B* rule could assert it — that
is §5's check #2 — but the model still has to write the column list, and only the sentence makes it
do that. Ship both; they do different work.

### 2.2 · Redirect built from a query parameter · **Layer B · SHIP · +21 tokens**

> `dart/security.md` — "Sanitize deep link URLs before navigation — validate scheme, host, and path parameters. Use `Uri.tryParse` and validate before navigating."
> `react-native/security.md` — "Validate and sanitize deep links and universal links — never route or grant access based on unvalidated params."
> `kotlin/security.md`, `arkts/security.md` — the same rule, twice more.

Four independent witnesses in four mobile directories, and the web form is the one every generated
app with a login screen writes: `redirect(searchParams.get('next'))` after sign-in. That is an open
redirect and a credible phishing primitive in an app the user will hand to customers. One line,
into the `## Never` block that pass 1 already proposed:

> "Never redirect to a URL that came from a query parameter unless it begins with `/`."

Cheapest useful sentence found in either pass. **The `## Never` block goes from five lines to
seven** — this and §2.1 — for +21 and +48.

### 2.3 · Validation is bidirectional · **Layer B · SHIP · +15 tokens (amend an existing line)**

> `angular/security.md` — "Type and validate API responses — treat external data as `unknown` at the boundary."
> `kotlin/security.md` — "Validate and sanitize all server responses before use."
> `react-native/security.md` — "Validate ALL external data (API responses, deep-link params, push payloads) with Zod before use."

Three directories, one idea the `common/` file never states. Scio's playbook names the boundary and
zod for *input*. Nothing says a third-party API's response is also untrusted — and a connector
package parsing a webhook or a Stripe response is exactly where a generated app will trust JSON it
did not produce. This is **not a new rule, it is four words on the existing one**: extend the
validation line to *"…and on data coming back from any external service or webhook."*

`ruby/security.md` states the general form better than anyone:

> "Treat background jobs, webhooks, Action Cable messages, and Turbo Stream inputs as untrusted boundaries."

### 2.4 · Fail fast on missing configuration · **Layer D · library entry, 0 playbook tokens**

> `rust/security.md` — "Fail fast if required secrets are missing at startup."
> `react-native/production-readiness.md` — "Validate required config at startup and fail fast with a clear message."

Two unrelated directories, one sentence, and it is the closest thing in 6,844 lines to *what a user
sees when something fails*. A generated Next.js app with a missing `SUPABASE_URL` does not fail at
boot — it serves a 500 on the first request that touches the database, in production, to someone
who cannot read a stack trace.

**But this must not be a playbook sentence.** It is a nine-line file:

```ts
// lib/env.ts — parsed at module load, so the app refuses to start rather than 500 later
export const env = z.object({ NEXT_PUBLIC_SUPABASE_URL: z.string().url(), … }).parse(process.env)
```

That is a **Layer D library entry** under ADR-0014 — "contracts with files attached" — generated
once by the scaffold package and imported by the rest. Describing it in six prompts costs tokens
and is obeyed probabilistically; generating it costs nothing and is a fact. This is the §4 reframe
of pass 1 applied to a new rule, and it is the pattern the other three should be measured against.

### 2.5 · Logout must clear the client cache · **Layer D · library entry, 0 playbook tokens**

> `kotlin/security.md` — "Clear all auth state on logout (tokens, cached user data, cookies)."
> `dart/security.md` — "Clear auth state on logout: tokens, cached user data, cookies."

`supabase.auth.signOut()` clears the token. It does not clear a TanStack Query or SWR cache, so on
a shared browser the next person to sign in sees the previous user's rows rendered from cache
before the first refetch resolves. Two witnesses, and again the fix is **a generated helper**, not a
sentence: the library's `sign-out` part calls `queryClient.clear()` alongside `signOut()`.

### 2.6 · Timeouts on every outbound call · **Layer E · CHECK, connector packages only**

> `kotlin/security.md` — "Set timeouts on all HTTP clients — never leave defaults (which may be infinite)."
> `dart/security.md` — "Set request timeouts on all HTTP clients — never leave defaults."
> `arkts/security.md` — "Implement request timeout and retry policies."
> `golang/security.md` — "Always use `context.Context` for timeout control."

Four directories. For us the failure is not a hung phone, it is **billing**: a `fetch` with no
signal inside a route handler holds a serverless invocation until the platform's wall-clock limit
and is charged for it. It is also the one reliability rule with a clean regex: a `fetch(` in
`app/api/**` or a server action with no `signal:` / `AbortSignal.timeout` in the call. **One line in
`_QUALITY_PATTERNS`, warning severity, connector packages only** — the same scoping pass 1 gave the
SSRF rule. No playbook tokens.

### 2.7 · Sort and filter parameters need an allowlist · **Layer E · CHECK**

> `csharp/security.md` and `fsharp/security.md` — "Validate sort fields and filter operators before using dynamic query composition."

The Supabase form is `.order(searchParams.get('sort'))` on any table view with sortable columns —
a column-name injection into PostgREST, and the reason `perl/security.md`'s otherwise archaic
advice is right in general: *"Use allowlist regex for untainting — never `/(.*)/s`."* A check for a
non-literal argument to `.order(` / `.filter(` is one regex line.

### 2.8 · The production build is a different artifact · **build process · flag, no rule**

> `kotlin/security.md` — "Test release builds — obfuscation can break serialization silently."

Stated for R8, true for us: a Next.js app that works under `next dev` can fail under `next build`
on the server/client boundary, on `NEXT_PUBLIC_*` inlining, and on route-segment config. Pass 1
already found there is **no gate on the finished app** (ADR-0017 promotes the workspace and asserts
nothing about it). This is a second witness for that gap from a completely different direction, and
it sharpens it: the gate must run `next build`, not `tsc --noEmit`, because they fail differently.

### 2.9 · Six that corroborate and change nothing

| Passage | Source | Why no change |
|---|---|---|
| "Return safe client-facing messages… do not expose stack traces, SQL text, or filesystem paths in API responses" | `csharp/`, `fsharp/`, `rust/security.md` | Three more witnesses for pass 1's §3.3, already **SHIP** |
| "Regenerate session identifiers after authentication and privilege changes" | `php/`, `ruby/security.md` | Supabase rotates on sign-in; would generate redundant code |
| "Validate file uploads by content type, extension, size, and storage destination" | `ruby/security.md` | Real, but only applies to apps with Storage. **The playbook is fixed** — this argues for a conditional section, which is an open design question, not a rule |
| "Prefer `transform` and `opacity`; never animate `width`/`height`/`padding`/`margin`" | `arkts/patterns.md`, `react-native/performance.md` | Layer F. **Merge into `app-design`**, not the playbook |
| "Query by accessible role/label/text, not by `testID` — this also enforces accessibility" | `react-native/testing.md` | Consistent with pass 1: belongs in the scaffold's `test-utils.tsx`, generated once |
| "Never persist raw auth tokens to `localStorage`" | `vue/patterns.md` (+4 others) | Already line 2 of the proposed `## Never` block |

### 2.10 · Two that look good and are wrong for us

- **`vue/security.md`: "sanitize on the backend before persisting."** The modern consensus is the
  opposite — sanitize on output, store what the user typed — because a sanitiser bug becomes
  permanent data loss. Vue's own docs say this; ECC repeats it uncritically. **Leave.**
- **`csharp`/`kotlin`: "Never catch `CancellationException` — always rethrow."** The web analogue
  (do not swallow an `AbortError`) is real but so rare in generated CRUD that it fails the
  every-prompt test. **Leave.**

### 2.11 · The running total

Pass 1 proposed net **+173** tokens (668 → 841). This pass adds **+120** (§2.1 +48, §2.2 +21,
§2.3 +15, §3.2 +36) and adds **zero** through Layer D and the checks. **New total ≈ 961 tokens per package** —
cumulatively **+293 over the original playbook, ≈ +1,760 per six-package build** — still under the
~1,200 cap — but two-thirds of the remaining headroom is now spent, and
`app-design`'s sections have not landed yet. Everything after this should be a check or a
generated file.

---

## 3 · Idempotency, rollback, and failure as seen by a user

Pass 1 reported zero hits for idempotency and rollback across 9,506 lines of `rules/`. I re-ran
that over **21,855 lines** — `rules/` *and* `commands/` — with 25 terms.

| Term | Files in `rules/` | Files in `commands/` | Verdict |
|---|---|---|---|
| `idempot*` | **0** | **0** | Confirmed absent from the entire corpus |
| `exactly once`, `at-least-once`, `replay`, `compensat*`, `backoff`, `circuit break*`, `concurrent edit` | 0 | 0 | Absent |
| `dedup*` | 1 | 0 | One incidental mention |
| `rollback` (one word) | **0** | 2 | — |
| `roll back` (two words) | **3** | 0 | **Pass 1's grep missed these** |
| `reversible` | 1 | 0 | One line, and it is the important one |
| `transaction` | 3 | 0 | All three are enum variant names in example code |

**Correction to pass 1.** "Rollback: zero hits" was produced by grepping `rollback`. The corpus
says *roll back*, in three places, one of which pass 1 had already read in full (`web/patterns.md`)
without reporting it. The finding survives — there is no rollback *doctrine* — but the specific
claim was wrong and the three lines are the most useful content in this section.

### 3.1 · Idempotency: genuinely, completely absent

Zero hits in 21,855 lines. Not "thin" — **absent**. ECC has 68 agents, 23 hooks, a GAN loop that
re-runs a generator up to fifteen times, an epic system that stamps GitHub issues, and a
learning system that appends to files on every session, and no file in it contains the word.

Which makes the one place the *concept* appears without the word worth quoting in full —
`cost-report.md`, describing the cost tracker's append-only log:

> "The tracker appends one JSON object per session-stop to `~/.claude/metrics/costs.jsonl`. Each
> row is a **cumulative snapshot for that session**, so the report takes the **latest row per
> `session_id`** and sums across sessions (**summing every row would multiply-count**)."

That is the whole idea, stated correctly and only about money: **an append-only ledger with
at-least-once writes is safe only if the consumer reduces by a key, and the key must be declared.**
The producer is not idempotent; the reader is made idempotent instead.

**Scio's `G-F03` is the same shape** — a confirmed live cross-tenant idempotency replay in
metering. So the corpus's single instance of idempotent thinking is *in the same domain as our
confirmed bug*, and it is one paragraph in a reporting command. **Layer G. This is not a playbook
line and never was**; it is a property of the metering table and its reader. The transferable
sentence, for `LAYER-G` rather than for a prompt:

> Every append-only ledger declares its reduction key and its idempotency key, and the key includes
> the tenant. A consumer that sums rows without reducing by that key is a billing bug.

**Nobody has written this down in either system.** Pass 1 said that; this pass confirms it against
twice the corpus and names the one near-miss.

### 3.2 · Rollback: three lines, and only one is about software the user runs

The three, verbatim:

> `react-native/patterns.md` — "Use optimistic updates for fast interactions: **snapshot, apply,
> roll back on failure with visible feedback**."

> `web/patterns.md` — "### Optimistic Updates · Snapshot current state · Apply optimistic update ·
> **Roll back on failure** · **Emit visible error feedback when rolling back**."

> `react-native/production-readiness.md` — "Roll out gradually and **keep the ability to roll
> back**." (deployment, not runtime)

And one more, from a `hooks.md` file in a directory pass 1 classified as noise:

> `ruby/hooks.md` — "Warn when a migration changes data destructively without a **reversible path
> or documented rollout plan**."

That last line matters out of proportion to its length. Pass 1's §3.6 called migration discipline
*"the biggest genuine gap found, and it had to be written, not mined"*, on the evidence that
`grep -ril migrat rules/` returned three incidental hits. **It is in the corpus after all** — in
`ruby/hooks.md`, as a lint warning, phrased better than we phrased it: it does not ask for a
rollback, it asks for *a reversible path **or** a documented plan*, which is the honest form,
because plenty of destructive migrations are correct and only need to be deliberate.

**Verdict — Layer B, amend pass 1's migration rule at zero net cost:**

> "A migration that drops a column or a table states, in a comment on the first line, either how it
> is reversed or why it does not need to be."

That is +36 tokens and it converts an unenforceable ask into something a **check can see**: a
migration file containing `DROP` whose first line is not a comment. §5 check #4.

### 3.3 · What a user sees when an operation fails

This is the question pass 1 flagged as absent from both systems. The corpus has **four** relevant
lines and no doctrine:

> `web/patterns.md` — "Emit visible error feedback when rolling back."
> `react-native/production-readiness.md` — "Capture and surface failed network/mutation states; **do not fail silently**."
> `react-native/coding-style.md` — "**Surface user-facing errors through UI state, not console.**"
> `dart/testing.md` — "All state transitions must have tests: **loading → success, loading → error, retry**."

The last is the sharpest, because it is a *testable* statement of the same rule. And
`prp-plan.md` supplies the only enumeration of failure modes anywhere in the corpus, as a plan
template checklist:

> **Edge Cases Checklist** — Empty input · Maximum size input · Invalid types · **Concurrent
> access** · **Network failure** · **Permission denied**

Six items, three of which are the ones a generated CRUD app gets wrong, and *"concurrent access"*
is the nearest the corpus comes to naming the idempotency problem in a checklist.

**Verdict — Layer B, merge into `app-design` §4 rather than shipping separately.** Pass 1 already
routed loading/empty/error states there. Add one clause and one test rule:

- to `app-design` §4: *"An operation that fails tells the user what failed and what to do next.
  Never a blank screen, never only a console message."*
- to the playbook's existing **tests** section, replacing nothing: the test rule already says
  *happy path and main failure*; `dart/testing.md`'s **loading → success, loading → error, retry**
  is the same rule written so a reviewer can count three tests instead of arguing about two.
  **+0 tokens, better wording.**

### 3.4 · The one real rollback mechanism in the corpus is in a command

Not in `rules/` at all. `refactor-clean.md`:

> **"Never delete without running tests first. One deletion at a time — atomic changes make
> rollback easy."** · "If tests fail — **immediately revert with `git checkout -- <file>`** and
> skip this item."

Plus its safety tiers — **SAFE** (delete confidently) / **CAUTION** (verify no dynamic imports or
external consumers) / **DANGER** (investigate before touching) — and the discipline
*"Don't refactor while cleaning — separate concerns."*

**Layer E and Layer F.** This is the shape Scio's repair loop and the design window's refine step
should have and, as far as the as-built docs record, do not: *one change, verified, reverted on
failure, and the failure does not stop the run — it skips the item*. It is strictly better than a
loop that accumulates edits and then discovers the package no longer compiles. **Check/mechanism,
zero prompt tokens.** See §5.

### 3.5 · And the corpus's real answer: prevent the need to roll back

Three commands independently arrive at the same pattern, and it is the most transferable safety
idea in either half of this document:

> `project-init.md` — "**Default to dry-run.** Do not modify `CLAUDE.md`, settings files, rules,
> skills, or install state until the user approves the concrete plan… **Report exactly what would
> change before applying anything**… Never replace an existing `CLAUDE.md` without showing a diff
> and receiving approval."

> `update-codemaps.md` — "If previous codemaps exist, calculate the diff percentage. **If changes
> > 30%, show the diff and request user approval** before overwriting."

> `learn-eval.md` — "If the target already exists, **show the diff**, then prefer **Absorb**, choose
> a new name, or require explicit overwrite approval."

And the mechanism that makes regeneration survivable at all, from `update-docs.md`:

> "**Single source of truth**: always generate from code, never manually edit generated sections ·
> **Preserve manual sections**: only update generated sections; leave hand-written prose intact ·
> **Mark generated content**: use `<!-- AUTO-GENERATED -->` markers around generated sections."

**Layer F, and directly an ADR-0017 question.** ADR-0017 says "Build it" *promotes* the workspace
and never regenerates — which sidesteps this for the first build. It does not sidestep the
**second** build against an app the user has since edited, which ADR-0001's wedge ("software they
intend to run and grow") makes the normal case. The three-part answer the corpus converged on —
*dry-run by default · show the diff and get approval above a threshold · mark what is generated so
hand edits survive* — is the missing half of ADR-0017 and costs no prompt tokens at all.

---

## 4 · The 94 commands — what they actually are

### 4.1 · The taxonomy, counted

Pass 1 established they are not the compatibility shims the README claims. Measured, they are
**five** things, and only one of the five is what a slash command is usually for:

| Kind | Files | Lines | What it is |
|---|---|---|---|
| **Thin narrator over a deterministic script** | 22 | ~1,900 | Body is one `node scripts/…` or `npx` call plus how to read the output |
| **One template instantiated per language** | 22 | 4,044 | `*-review` ×9, `*-build` ×7, `*-test` ×6 — identical heading skeletons, different bodies |
| **Composed multi-phase workflow** | ~30 | ~5,100 | `prp-*`, `code-review`, `santa-loop`, `save-session`, `refactor-clean`, `orch-*`, `multi-*` |
| **A skill in the wrong folder** | ~14 | ~900 | `ecc-guide`, `model-route`, `aside`, `hookify-help`, `quality-gate`, `loop-status` — reference documents with no action |
| **Duplicate of another command** | 2 | 368 | `pr.md` / `prp-pr.md` |

Two facts about the whole set:

- **92 of 94 declare no tool restrictions.** Only `marketing-campaign.md` and `skill-create.md`
  carry `allowed_tools` (and they spell it with an underscore, unlike the agent convention).
  Exactly **one**, `security-scan.md`, binds an agent in frontmatter (`agent: ecc:security-reviewer`,
  `subtask: true`). Pass 1 praised ECC's agent frontmatter discipline; the *user-facing* entry
  points have none of it. The asymmetry is backwards — a command is what a person types.
- **Delegation is rarer than the directory implies but commoner than pass 1's count.** Pass 1 said
  "2 of 94 mention the `Task` tool" — true for that literal string (`gan-build`, `plan`). Adding
  `Agent tool` and `subagent_type` brings it to **5**: `+santa-loop`, `+multi-execute`,
  `+multi-plan`. The addition matters because `santa-loop` is the most carefully built delegation
  in the repository and pass 1 never read it (§4.4).

### 4.2 · The alias table is a lie, and it is checkable

The seven `epic-*` commands are 22–26 lines each, each one call to
`node scripts/github-coordination.js <verb>`. Each ends with a **"Compatibility aliases"** block:

| Command | Declares itself an alias of |
|---|---|
| `epic-decompose` (23 lines) | `/plan` (206), `/prp-plan` (502) |
| `epic-claim` (26) | `/orch-add-feature`, `/orch-change-feature`, `/prp-implement` (385) |
| `epic-validate` (22) | `/quality-gate` |
| `epic-review` (23) | `/review-pr`, `/code-review` (289) |
| `epic-publish` (23) | `/pr`, `/prp-pr` |
| `epic-unblock` (22) | `/loop-status` |

`/epic-decompose` stamps a GitHub issue body. `/prp-plan` runs an eight-phase codebase
investigation and writes an implementation plan. **They are declared interchangeable.** This is the
only place in ECC where the README's shim story is actually asserted inside a file, and it is
asserted between things that do unrelated work.

**For us:** an alias or "compatibility" mapping that nothing verifies is worse than none — it is a
claim of equivalence that will be believed. If Scio ever ships aliases across its own entry points,
the mapping needs a test, or it needs to not exist.

### 4.3 · The per-language family: 4,044 lines, one authored artifact

`cpp/go/kotlin/rust/react/vue/python/flutter/fastapi-review`, six `*-build`, six `*-test`. Their
first four headings are byte-identical within each family. Pairwise *textual* similarity across all
4,371 command pairs never exceeds 0.60 in this family — so they are not copy-paste; they are **one
template, filled in per language by someone who knew that language.** That is more work and more
value than a shim, and it is still 4,044 lines that exist only because ECC installs per stack.

Two things in them are worth taking, both from the review family's shared skeleton:

- **Every one ends in `## Approval Criteria`.** Pass 1 wanted the explicit approval predicate
  `common/code-review.md` lacked. It exists — 22 times, per language.
- `python-review.md` carries the only line in the corpus about **"Missing migrations for model
  changes"**, and `code-review.md`'s completeness category names *"incomplete migrations"*. Pass 1's
  claim that migrations appear three times incidentally was scoped to `rules/`; in `commands/` there
  are ten mentions.

### 4.4 · The five commands worth reading in full

**`code-review.md` (289) — the decision predicate, stated.** Its Phase 5:

> | Zero CRITICAL/HIGH, validation passes | **APPROVE** |
> | Only MEDIUM/LOW, validation passes | **APPROVE** with comments |
> | Any HIGH or validation failures | **REQUEST CHANGES** |
> | Any CRITICAL | **BLOCK** — must fix before merge |

Severity is not the output; **the decision is**, and the mapping is written down rather than left
to a reviewer's mood. `builder/validation.py` has severities and a two-value pass/fail; what it
lacks is this table. Also, Phase 3: *"Read each changed file **in full** (not just the diff
hunks — you need surrounding context)."*

**`santa-loop.md` (175) — adversarial dual review.** Two reviewers, different model families, **no
shared context**, both must PASS. Its four load-bearing sentences:

> "You are an independent quality reviewer. You have **NOT** seen any other review. Your job is to
> find problems, not to approve."
> "**Fresh reviewers each round** prevents anchoring bias from prior findings."
> "Fix every flagged issue — **change only what was flagged, no drive-by refactors**."
> "**Maximum 3 iterations.** If still NAUGHTY after 3 rounds, stop and present remaining issues…
> Manual review required before proceeding. **Do NOT push.**"
> "**Commits happen on NAUGHTY rounds** so fixes are preserved even if the loop is interrupted."

Set that against `gan-build`, which pass 1 found instructing its generator *"If a suggestion seems
wrong, still try it — the Evaluator sees things you don't."* Same repository, opposite doctrine:
one loop removes the generator's judgement, the other removes the reviewer's memory. **The second
is right**, and its bounded-escalation-to-a-human ending is what a Layer E repair loop needs
instead of a 15-iteration budget.

**`prp-plan.md` (502) + `prp-implement.md` (385) — the package contract, and its calibration.**
Three ideas, all Layer C:

> **Golden Rule**: "If you would need to search the codebase during implementation, capture that
> knowledge **NOW** in the plan."
> **No Prior Knowledge Test**: "A developer unfamiliar with this codebase should be able to
> implement the feature using **ONLY this plan**, without searching the codebase or asking
> questions. If not, add the missing context."
> **NOT Building**: "Explicit list of what is OUT OF SCOPE (prevents scope creep during
> implementation)."

The No-Prior-Knowledge Test is a **falsifiable acceptance criterion for an ADR-0013 build package**,
which currently has a good list of contents and no test of sufficiency. "NOT Building" appears
three times across `prp-plan`, `prp-prd` and `plan-prd` — the most-repeated idea in the commands
corpus — and it is a per-package field, not a playbook sentence, so it costs the prompt nothing
beyond the two or three lines it contains.

And from `prp-implement`, the best single idea in the 12,349 lines:

> **Assessment vs Reality** — | Metric | Predicted (Plan) | Actual | — for complexity, confidence,
> and files changed.

The plan writes down what it expects; the report scores it. Scio has Layer C predicting packages
and Layer E building them and, per the as-built docs, **nothing that compares the two afterwards**.
That table is the measurement ADR-0016's library needs in order to grow from real builds rather
than from whatever was generated last.

**`save-session.md` (275) + `resume-session.md` (156) — the failure ledger.**

> "## What Did NOT Work (and why) — **This is the most important section.** List every approach
> tried that failed. For each failure write the EXACT reason **so the next session doesn't retry
> it**. Be specific: 'threw X error because Y' is useful. 'didn't work' is not."
> "## What WORKED (with evidence) … **Without evidence, move it to 'Not Tried Yet' instead.**"
> "Write every section honestly… **An incomplete file is worse than an honest empty section.**"

and `resume-session` renders it back under the heading **"WHAT NOT TO RETRY"**.

**Layer E, and an ADR-0020 question.** Builds are jobs; a job that failed a package one way and is
retried has no record that says which way. ADR-0016 grows the library from what *worked*; nothing
in Scio records what failed and why, so every repair loop is free to repeat the previous one's
mistake. A negative ledger is cheap — it is a JSONB column on the build job.

### 4.5 · Two commands that state our own doctrine better than we do

`harness-audit.md`, on a scoring command that wraps a script:

> "This script is the **source of truth** for scoring and checks. **Do not invent additional
> dimensions or ad-hoc points.**" · "Use script output directly; **do not rescore manually**." ·
> "Rubric version: `2026-05-19`." · "`max_score` depends on which categories are applicable to the
> target; **never assume a fixed total**."

`security-scan.md`, on a security command that wraps a scanner:

> "**Do not invent findings.** Use AgentShield output as the source of truth and **separate scanner
> facts from follow-up judgment**." · "Re-run the scan after fixes and report the **before/after**
> score."

That is ADR-0012 — *rules do what rules can guarantee; the model is used only for judgement* —
written as an operating instruction for a prompt, plus two things we do not have: a **versioned
rubric** and a **variable denominator**. Both matter for the design window's scoring and for any
build quality score we report to a user: a score whose rubric is unversioned cannot be compared
across builds, and a fixed denominator lies when a category does not apply.

### 4.6 · The contradiction inside the learning system, which is our question too

`learn-eval.md` documents *removing* a numeric rubric:

> "This version replaces the previous 5-dimension numeric scoring rubric… **forcing rich
> qualitative signals into numeric scores loses nuance and can produce misleading totals.** The
> holistic approach lets the model weigh all factors naturally… while the explicit checklist
> ensures no critical check is skipped."

Meanwhile `gan-build` gates its loop on a **parsed weighted total**, and `gan-design` ships
weights `0.35 / 0.30 / 0.25 / 0.10`. Two positions, one directory, neither aware of the other.

Both are right about different jobs, and the distinction is worth stating because Scio has both
jobs: **a score is required when you need a gradient** (convergence, plateau detection — `gan-build`),
and **a verdict plus a checklist is better when you need a decision** (save/drop, approve/block —
`learn-eval`, `code-review`). Scio's design window and `builder/validation.py` are the second kind.

Also from `learn-eval`, two mechanisms:

- **Four verdicts, not two: Save · Improve then Save · Absorb into [X] · Drop** — with a mandatory
  duplicate check first (*"Grep existing skills by keyword to check for content overlap… consider
  whether appending to an existing skill would suffice"*). **Layer D.** ADR-0016 grows the library
  from real builds with ids `category.seqno.version`; without an **Absorb** verdict and a
  pre-creation overlap check, it accumulates near-duplicate parts and ADR-0014's match degrades
  exactly as the library gets bigger.
- The corpus's only **write-side injection defence**: *"Treat session-derived content as
  untrusted… Validate `pattern-name` as a lowercase hyphenated slug. **Reject path separators and
  path traversal, resolve the target, and confirm it remains inside the approved root.** If the
  target already exists, show the diff… **Never replace an existing skill silently.**"*
  **Layer E, security.** `builder/file_plan.py` computes paths deterministically, which is why this
  has not bitten us — but anywhere a model names a file or a slug from user text, this is the check.

### 4.7 · Leave, with reasons

`gan-design.md` tells its generator *"A stunning half-finished app beats a functional ugly one."*
That is the correct instruction for a design experiment and the **wrong** one for ADR-0001's
promise of developer-grade output. **Leave, actively** — as pass 1 said of `gan-generator`.
`marketing-campaign`, `jira`, `pm2`, `setup-pm`, `hookify-*`, `instinct-*`, `projects`, `promote`,
`prune`, `skill-health`, `evolve`, `auto-update`, `ecc-guide`, `plan-canvas`, `aside`,
`model-route`: ECC's own operations. Nothing for us.

---

## 5 · Verdict table

**Playbook text** — the only three that earn a sentence in every package prompt.

| # | Item | Layer | Source | Verdict | Tokens |
|---|---|---|---|---|---|
| 2.1 | Never write a request body into an insert/update; name the writable columns | **B** | `ruby/`, `php/security.md` | **SHIP** | **+48** |
| 2.2 | Never redirect to a URL from a query parameter unless it starts with `/` (into the `## Never` block) | **B** | `dart/`, `react-native/`, `kotlin/`, `arkts/security.md` | **SHIP** | **+21** |
| 2.3 | Extend the existing zod line: also validate data coming back from any external service or webhook | **B** | `angular/`, `kotlin/`, `react-native/security.md` | **SHIP** (amend) | **+15** |
| 3.2 | A destructive migration states how it is reversed, or why it need not be | **B** | `ruby/hooks.md` | **SHIP** (amend pass 1 §3.6) | **+36** |
| 3.3 | "loading → success, loading → error, retry" as the wording of the existing test rule | **B** | `dart/testing.md` | **REWORD** | **±0** |
| 3.3 | "An operation that fails tells the user what failed and what to do next" | **B/F** | `web/patterns.md`, `react-native/*` | **MERGE into `app-design` §4** | 0 |
| 2.9 | Animate `transform`/`opacity` only | **F** | `arkts/`, `react-native/` | **MERGE into `app-design`** | 0 |

**Running total: pass 1 +173, this pass +120 → 961 tokens per package (668 → 961, +44%);
≈ +1,760 added per six-package build, ≈ 5,770 total playbook cost per build.** Under the ~1,200 cap, with roughly 240 tokens left for `app-design`. Nothing else here spends any.

**Deterministic checks** — cheaper than every sentence above, and guarantees rather than probabilities.

| # | Check | Layer | Where it goes | Source |
|---|---|---|---|---|
| 1 | `fetch(` in a route handler or server action with no `signal:` / `AbortSignal.timeout` | E | `_QUALITY_PATTERNS`, warning, connector packages only | `kotlin/`, `dart/`, `arkts/`, `golang/security.md` |
| 2 | An insert/update whose argument is a whole request body (`req.json()`, `formData`) rather than a named object | E | `_UNSAFE_PATTERNS`, 1 regex | §2.1 |
| 3 | Non-literal argument to `.order(` / `.filter(` | E | `_QUALITY_PATTERNS`, 1 regex | `csharp/`, `fsharp/security.md` |
| 4 | A migration containing `DROP` whose first line is not a comment | E | SQL scan, joins pass 1's migration checks | `ruby/hooks.md` |
| 5 | Any model-chosen filename or slug: validate as `[a-z0-9-]+`, resolve, assert inside root, never overwrite silently | E | write path | `learn-eval.md` |
| 6 | Privileged columns (`role`, `owner_id`, `workspace_id`, `*_at`) declared in the architecture graph, so #2 can name them | **B** | Layer B rule, on the graph | §2.1 |

**Mechanisms** — no tokens, no regex; these are changes to how the engine runs.

| # | Mechanism | Layer | Source |
|---|---|---|---|
| M1 | Ship the architecture to each package as a **token-lean codemap** (`POST /api/x → handler → service → table`, capped ~1,000 tokens) instead of `architecture.model_dump_json(indent=2)` | **C** | `update-codemaps.md` |
| M2 | Every package carries a **"NOT building"** list | **C** | `prp-plan`, `prp-prd`, `plan-prd` |
| M3 | **No-Prior-Knowledge Test** as the acceptance criterion for a package contract | **C** | `prp-plan.md` |
| M4 | A **`Parallel` / `Depends`** column on the package table, not just dependency order | **C** | `prp-prd.md` |
| M5 | **Predicted vs Actual** recorded per package after every build; feeds ADR-0016 | **D/E** | `prp-implement.md` |
| M6 | **Absorb** as a fourth library verdict, with an overlap check before any new entry | **D** | `learn-eval.md` |
| M7 | A **failure ledger** on the build job: what was tried, why it failed, do not retry | **E** | `save-session`, `resume-session` |
| M8 | An explicit **decision table** (APPROVE / COMMENT / REQUEST CHANGES / BLOCK) in `validation.py`, not just severities | **E** | `code-review.md` |
| M9 | Order validation **by cost**: static → unit → build → integration → edge cases, stop at the first failure | **E** | `prp-implement.md` |
| M10 | Repair loop: **one change, verified, `git checkout --` on failure, skip the item**; SAFE/CAUTION/DANGER tiers | **E/F** | `refactor-clean.md` |
| M11 | Non-convergence detectors: same error 3× → stop; a fix that creates more errors than it resolves → stop | **E** | `build-fix.md` |
| M12 | Dual review, context-isolated, **fresh reviewers each round**, max 3 rounds, then escalate to a human and do not ship | **E** | `santa-loop.md` |
| M13 | Second builds: **dry-run by default · diff above a threshold · `<!-- AUTO-GENERATED -->` markers so hand edits survive** | **F** | `project-init`, `update-codemaps`, `update-docs` |
| M14 | Gate the **promoted repo** on `next build`, not `tsc --noEmit` — they fail differently | **F** | `kotlin/security.md` + pass 1's ADR-0017 gap |
| M15 | Append-only ledgers declare a **reduction key including the tenant**; the consumer reduces | **G** | `cost-report.md` — and `G-F03` |
| M16 | Apply `python/fastapi.md`'s six rules to the engine (no blocking calls in async routes; no auth state in response models; JWT aud/iss/exp/alg; no wildcard CORS with credentials; redact auth headers; clear `dependency_overrides`) | **build process** | `python/fastapi.md`, ADR-0006 |
| M17 | Any scoring surface: **version the rubric**, let the denominator vary, and separate "scanner facts" from "follow-up judgment" | **build process** | `harness-audit`, `security-scan` |
| M18 | Use a **score** only where a gradient is needed (convergence); use a **verdict + checklist** for decisions | **E/F** | `learn-eval` vs `gan-build` |

**Leave.**

| Item | Source | Why |
|---|---|---|
| ~5,900 lines across `cpp`, `golang`, `swift`, `perl`, `fsharp`, `arkts`, `java`, `kotlin`, `rust`, `dart`, `angular`, `vue` patterns/testing | the seventeen | ADR-0011 fixes the output stack; nothing transferable found |
| 4,044 lines of `*-review` / `*-build` / `*-test` | commands | One template per language; ECC installs per stack, we do not |
| Session rotation after sign-in; sanitize-before-persist; `:style` injection; `CancellationException` | `php`, `ruby`, `vue`, `kotlin` | Handled by Supabase, contested, or too rare for every prompt |
| RTL/test-id query priority | `react-native/testing.md` | Scaffold `test-utils.tsx`, as pass 1 concluded |
| File-upload validation | `ruby/security.md` | Real, but conditional on the app having Storage — the fixed playbook cannot express it. **Open question, not a rule** |
| `gan-design`'s "a stunning half-finished app beats a functional ugly one" | `gan-design.md` | Contradicts ADR-0001's developer-grade promise |
| `epic-*` compatibility aliases | commands | An unverified equivalence claim between a 23-line script wrapper and a 502-line workflow |
| `marketing-campaign`, `jira`, `pm2`, `hookify-*`, `instinct-*`, `evolve`, `skill-health`, `auto-update`, `ecc-guide`, `aside`, `model-route` | commands | ECC's own operations |

---

### The ratio, stated plainly

**6,844 lines of "noise" → 4 playbook sentences (+120 tokens), 4 checks, 2 build-process items.**
The verdict was right about volume and wrong about method: it screened against ADR-0011 alone,
which is why it missed `python/fastapi.md` (ADR-0006) and why two Ruby/PHP security lines naming a
live Supabase bug class went unread.

**12,349 lines of commands → 0 playbook sentences and 18 mechanisms**, most of them for Layers C
and E. The commands are worth more than the rules, and none of what they are worth is prompt text —
which is the same finding pass 1 reached from the other direction, arrived at independently.

*Mined 2026-08-26 against `affaan-m/ECC` @ `rules/` (122 files, 9,506 lines) and `commands/`
(94 files, 12,349 lines), read alongside `docs/as-built/01-DECISIONS.md`,
`docs/mined/ECC-RULES.md` and `docs/mined/ECC-AGENTS.md`. Two claims in pass 1 are corrected here:
the rollback grep (§3) and the delegation count (§4.1). Nothing else in either prior document is
re-derived.*
