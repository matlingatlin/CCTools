# ECC rules — what belongs in Scio's playbook

*Mined 2026-08-26 from `affaan-m/ECC` @ `rules/` — 122 markdown files, 9,506 lines.*
*Question: Scio's Layer B ships a `Playbook` of fixed house rules into every build prompt. ECC's `rules/` is the same artifact at fifty times the size. What is in theirs that should be in ours — and what in ours should not be prompt text at all?*

## What I read, and what the playbook is today

**Read in full:** all ten files of `rules/common/` (545 lines) and all of `rules/typescript/`
(319), `rules/react/` (878) and `rules/web/` (627) — the directories our fixed stack touches. Plus
`nuxt/security.md`, `react-native/{security,production-readiness,accessibility}.md`,
`java/security.md` and `ruby/security.md`, which cross-corpus greps flagged as the only places
certain concerns appear at all. **Surveyed by heading** across the other seventeen language
directories; five topic greps over all 122 files.

### The playbook, measured

The recorded figure — *"roughly 3,018 characters ≈ 754 tokens"* — is **exactly the byte count of
`layerb/playbook.yaml` on disk.** That is not what costs tokens. What reaches a prompt is
`Playbook.as_prompt_section()`, which drops the five-line YAML comment header and re-renders the
data as markdown:

| Object | Size |
|---|---|
| `playbook.yaml` on disk | 57 lines, **3,018 chars** |
| …minus its comment header | 2,705 chars |
| **`as_prompt_section()` — what ships** | **52 lines, 2,671 chars, 422 words ≈ 668 tokens** |

Working number: **≈ 670 tokens, not 754.** Small delta, right magnitude — but the object measured
was the file, not the prompt, and every cost argument below is against the prompt. Carried once per
package by `BuildContext.as_prompt()`; **six packages per build ≈ 4,000 tokens of playbook per
build.** Its seven sections: `stack` (ADR-0011), `folder_structure` (8 lines), `naming` (5),
`secure_by_default` (6), `tests` (3), `accessibility` (4), `quality` (4) — thirty rules, denser and
better written than most of what follows.

### One thing the cost frame gets wrong before we start

`assemble_build_context` sets `architecture=architecture.model_dump_json(indent=2)` — **the entire
architecture graph, indented, in every package's prompt.** The code admits it: *"Layer C will call
this per package; for now it assembles the whole architecture."* For any app past three tables that
JSON dwarfs the playbook. **The playbook is not the dominant term in the build prompt**, and
economising on it while a pretty-printed JSON blob rides along uncontested is misdirected.

That does not license growth. It means the discipline is a **cap** — under ~1,200 tokens, past
which an addition must displace something — not per-sentence agony.

### Volume, bluntly

9,506 lines. **2,438 blank (25.6%). 750 lines of YAML `paths:` frontmatter (7.9%). 111 `> This file
extends …` pointer lines. 47 `## Reference` sections.** Then the repetition: across the 21 language
directories the same headings recur — **Error Handling ×14, Formatting ×13, Coverage ×13,
Immutability ×12, Input Validation ×11, Secret Management ×13, SQL Injection Prevention ×5,
Repository Pattern ×6.** These are not twenty-one rules. They are one rule in twenty-one syntaxes —
correct for a repo whose install script hands a Go team the Go file, worthless to us, because
ADR-0011 fixes our output stack and it will never be Go.

**Of 9,506 lines, ~1,800 are in directories our stack touches; of those perhaps 300 lines are
content Scio does not already have, has not already made a check, and is not already covered by
`app-design`. About 25 lines are worth shipping.** §3 and §4 are those lines.

---

## 1 · common/ — the language-agnostic rules

Ten files, 545 lines — the layer ECC says to "always install", and the layer most confused about
what a rule is.

| File | Lines | What it actually is | For us |
|---|---|---|---|
| `coding-style.md` | 86 | part standards, part slogans, part linter thresholds | partly |
| `security.md` | 30 | eight-item pre-commit checklist | 2 items we lack |
| `code-review.md` | 120 | severity ladder + issue catalogue | shape + 1 passage |
| `testing.md` | 60 | 80% coverage, mandatory TDD, AAA, test naming | 1 idea |
| `patterns.md` | 36 | repository pattern, API response envelope | 1 idea |
| `development-workflow.md` | 43 | ECC's own team process | no |
| `agents.md` | 66 | Claude Code subagent orchestration | not the playbook |
| `hooks.md` | 28 | Claude Code hook types, TodoWrite advice | no |
| `git-workflow.md` | 20 | ECC's commit conventions | no |
| `performance.md` | 50 | **Claude model selection and context windows** | no |

### The split that matters

**`performance.md` is not about performance.** It is about which Claude model to use (*"Haiku (90%
of Sonnet capability, 3x cost savings)"*), context-window management and the Option+T shortcut for
extended thinking. Zero sentences about the software produced. `agents.md`, `hooks.md`,
`git-workflow.md` and `development-workflow.md` are the same: instructions to the *agent operator*,
not rules the *artifact* obeys. **That is 207 of 545 lines — 38%, nearer 44% counting the agent
tables inside `code-review.md` and `testing.md` — of ECC's workflow conventions dressed as rules.**

The taxonomy to keep: **a playbook rule is a property of the artifact. A rule that is a property of
the process that made the artifact belongs to Scio's engine, not to the generated app's prompt.**

By that test `development-workflow.md` step 0 — *"GitHub code search first… Prefer adopting or
porting a proven approach over writing net-new code"* — is a worse version of something Scio
already built: ADR-0014's library, which matches every package against a curated catalog before
generating. ECC asks a model to search GitHub at build time; we do it deterministically against a
library grown from real builds.

### What is genuinely good in common/

**One passage** — `code-review.md`, "Common Issues to Catch → Performance":

> - N+1 queries - use JOINs or batching
> - Missing pagination - add LIMIT to queries
> - Unbounded queries - add constraints

**The only place in 9,506 lines where database performance appears**, and it lands exactly on what
Scio generates: CRUD over Supabase, where the default failure is `.select()` with no `.limit()` and
a lookup inside a `.map()`. → §3.7, §4.

**One shape** — the severity ladder: CRITICAL → **BLOCK**, HIGH → **WARN**, MEDIUM → **INFO**, LOW →
**NOTE**, with an explicit approval predicate (*"Block: CRITICAL issues found"*). Scio has the
two-value version in both `layerb/validate.py` and `builder/validation.py`. Four levels is not
obviously better; the stated predicate is the part we lack. Noted, not adopted.

**Three standards Scio already states better** — input validation (ours names the boundary *and*
zod), secrets (ours is stack-correct), and error handling — where ECC's *"Handle errors explicitly
at every level… Never silently swallow errors"* meets **nothing at all** on our side. → §3.3.

### What is worthless, and why saying so matters

`coding-style.md` opens with `## Immutability (CRITICAL)` then KISS, DRY and YAGNI as bulleted
headings. *"Prefer the simplest solution that actually works"* cannot be violated by any code a
model would write, because no model writes code it believes is needlessly complex. Tokens, no
change.

The numeric rules in the same file — *"200-400 lines typical, 800 max"*, *"Functions are small
(<50 lines)"*, *"No deep nesting (>4 levels)"* — are the opposite problem: perfectly precise, and
therefore **lint configuration that has been typed into a prompt.** ESLint has `max-lines`,
`max-lines-per-function`, `max-depth`. → §4.

And `testing.md`'s mandatory TDD loop (*"Write test first (RED)… Run test - it should FAIL"*) is
incoherent for a one-shot generator. Scio's *"Every operation gets at least one test covering its
happy path and its main failure"* is the correct translation, and already exists.

---

## 2 · The language directories, against our fixed stack

**From `docs/as-built/01-DECISIONS.md`, ADR-0011 (Accepted):** *"Generated apps: Next.js + TS +
Tailwind + Supabase, fixed"* — and the note that follows it: *"this is the **output** stack, not
Scio's own."* (Scio's own is ADR-0006 NestJS + FastAPI, ADR-0007 Postgres + pgvector — a different
question the playbook does not answer.)

| Relevance | Directories | Lines |
|---|---|---|
| **On-stack** | `typescript/`, `react/`, `web/` | 1,824 |
| **Transferable despite the label** | `nuxt/security.md`, `react-native/{security,production-readiness,accessibility}.md`, `java/security.md`, `ruby/security.md` | ~250 |
| **Noise for us** | the other 17 — angular, vue, dart, arkts, rust, golang, python, swift, php, cpp, csharp, fsharp, java, kotlin, perl, ruby, react-native | ~7,400 |

**78% is noise for us** — no criticism of ECC, whose install script exists so a Go team never sees
the Dart file. It is a statement about what can be mined.

### The hole in the middle

`rules/` has **no `nextjs/`, `sql/`, `postgres/`, `supabase/` or `tailwind/` directory.** Three of
the four elements of our stack have no rules at all. `react/patterns.md` says so itself:

> Server Actions, Route Handlers, Middleware… Treated as a separate framework concern — when adding
> deep Next-specific patterns, propose a dedicated `rules/nextjs/` track. For now follow Next.js
> official docs.

**So the surface where a generated app is most likely to be insecure — RLS, migrations, server
actions, the anon-key trust model — is exactly the surface ECC leaves blank. That part cannot be
mined; it has to be written.** → §3.2, §3.6, §5.

### `react/security.md` — the best file in the repository

180 lines, the only file that reads like it was written by someone who had seen the failures.
Covers `dangerouslySetInnerHTML`, unsafe URL schemes, `target="_blank"`, server-action validation,
env-prefix leakage, session storage, CSP, prototype pollution, SSR template injection, third-party
components, production source maps. The two passages aimed straight at our stack:

> | Framework | Public prefix | Private |  ·  `// CRITICAL: secret leaked to client bundle`
> | Next.js | `NEXT_PUBLIC_*` | All others |  ·  `const apiKey = process.env.NEXT_PUBLIC_STRIPE_SECRET_KEY;`
>
> Audit on every PR that touches env vars: would this string in the public bundle be a problem?

> - Never store sessions in `localStorage` — accessible to any XSS. Use httpOnly secure cookies.
> - Never trust client-set state to gate sensitive UI. Render-gating in JSX prevents display, not
>   access — the API must enforce.

Scio has the second idea already, better phrased (*"hiding a UI control is not access control"*).
It has neither of the other two.

### `react/hooks.md`, `react/patterns.md` — good, and mostly not prompt material

The two best passages are real rules that name the banned construct and its replacement:

> `useEffect` is for synchronizing with external systems… It is **not** the right tool for: derived
> state — compute it during render… resetting state when a prop changes — use a `key`

> Default position: **do not memoize**. Add `useMemo` / `useCallback` only when… 3. The computation
> is measurably expensive (profile before assuming)

**And both are already enforced by `eslint-plugin-react-hooks`, which the same file mandates two
sections later.** ECC writes the lint config down *and* writes 187 lines asking a human to obey it.
We need one of those, and the linter is the one that cannot be ignored. → §4. Same for
`react/patterns.md`'s *"`key` must be stable across renders — never `index` for any list that can
reorder"*.

### `web/performance.md` — numbers we lack, in a medium we cannot use

LCP < 2.5s, INP < 200ms, CLS < 0.1; JS budgets 150kb landing / 300kb app / 80kb microsite,
gzipped. Scio has no performance section, so the instinct is to take it. **Resist.** A model
writing a component cannot know its LCP. Take the numbers, put them in a build gate. → §4.

### `react-native/production-readiness.md` — the shape we are missing

Nothing in `common/` corresponds to it, which is telling: the release gate exists only in the
directory whose author had shipped to an app store.

> **Pre-Release Gate** — Before shipping, all must pass: `tsc --noEmit` clean · lint clean · tests
> green, coverage ≥ 80% · critical-flow E2E pass on a real build · **no secrets in bundle** · crash
> reporting active and verified

Scio's analogue — `builder/validation.py`'s seven agents — runs *per package during* the build.
There is no gate on the **finished app**: ADR-0017 promotes the design workspace with git history
intact and asserts nothing about whether the promoted repo type-checks, tests green, or ships
without a secret. **An ADR-0017 question, not a playbook line.** → §5.

### `nuxt/` and `react-native/security.md` — right idea, wrong framework

> **SSR payload leakage** — Anything in `useState`, `useFetch`/`useAsyncData` results, or
> `runtimeConfig.public` is serialized into the client payload. Never write a secret into those.

> **SSRF on server $fetch** — Server routes run with full network egress. Never pass user-controlled
> input directly into a server-side `$fetch` URL or host. Validate the param first, allowlist the
> target… reject user-supplied absolute URLs.

Next.js server components serialise props to the client the same way; route handlers have the same
egress. Neither risk is named in Scio's playbook. The SSRF one should be scoped to connector
packages, not shipped to all six.

And the single most valuable sentence in the corpus for our stack, from `react-native/security.md`:

> Public/anon keys (e.g. Supabase anon key, Firebase config) are acceptable ONLY when protected by
> server-side rules (RLS, security rules). Enforce authorization on the backend, never in the
> client.

That is the conceptual half of CVE-2025-48757. → §3.2.

### One sentence from a directory we will never use

`java/security.md`: *"Never expose stack traces, internal paths, or SQL errors in API responses ·
Map exceptions to safe, generic client messages at handler boundaries · Log detailed errors
server-side; return generic messages to clients."* Scio's *"No secrets, tokens or personal data in
logs or error messages"* covers the log direction and is silent on the response direction — the one
that returns a Postgres error naming a table to a browser. → §3.3.

---

## 3 · Playbook additions, with their token cost

**Budget.** Playbook ≈ **668 tokens**, once per package, six packages ≈ **4,000 per build**. Every
100 tokens added is 600 per build. These proposals total **+329 (+49%)** — and §3.9 finds **−156**
of existing text that a linter or `file_plan.py` already guarantees, so **net +173 (+26%), ~841
tokens, ≈ +1,000 per build.** Room stays under the ~1,200 cap for the `app-design` sections already
proposed elsewhere.

### 3.1 · A `## Never` block — **SHIP · ~94 tokens**

All thirty of Scio's rules are stated positively. ECC does the same everywhere except
`react/security.md`, which switches to `// WRONG:` / `// CORRECT:` pairs — and that is the file
that reads like it works. Negative constraints are cheap, unambiguous, and are the form models
actually violate.

```yaml
never:
  - "Never put a secret behind NEXT_PUBLIC_* — that prefix ships to the browser."
  - "Never keep a session or token in localStorage — httpOnly cookies only."
  - "Never gate access by hiding UI; the server action or route handler must check."
  - "Never use an array index as a React key in a list that can reorder."
  - "Never build a URL for a server-side fetch from user input."
```

**Why not the obvious others:** `dangerouslySetInnerHTML`, `eval` and SQL interpolation are
deliberately absent — `builder/validation.py:_UNSAFE_PATTERNS` already greps for all three and
blocks the package. Restating them buys a probabilistic copy of a guarantee we hold. Line 3
overlaps the existing *"hiding a UI control is not access control"*: **move it, delete the
original.** Highest value per token in the document.

### 3.2 · The anon-key trust model — **SHIP · ~47 tokens**

> "The `NEXT_PUBLIC_SUPABASE_ANON_KEY` is public by design and safe only because RLS is on and
> every policy is explicit. The service-role key never appears in code that reaches the browser."

The playbook already says *"Row-level security ON for every table, with explicit policies — never a
blanket allow."* This adds the **reason**, which is the load-bearing part: a model that understands
the anon key is a public credential whose only protection is the policy writes the policy
carefully; a model told "turn RLS on" writes `USING (true)` and has obeyed. This is the conceptual
half of **CVE-2025-48757** (170+ Lovable apps with readable and writable databases).
`next/LAYER-B-UNDERSTANDING.md §3.5` proposes the deterministic half. **Ship both; neither
substitutes for the other** — the rule proves the architecture demands a policy, the sentence makes
the model write a good one.

### 3.3 · Error responses leak the other way — **SHIP · ~37 tokens**

> "Log the detail server-side; return a generic message to the client. Never return a stack trace,
> a database error or an internal path in a response."

From `java/security.md`. Also the **first sentence in the playbook that says anything about error
handling** — a concern with fourteen headings in ECC and zero on our side (§5).

### 3.4 · Rate limiting, narrowed — **SHIP · ~24 tokens**

> "Rate-limit sign-in, sign-up, password reset and any mutation reachable without authentication."

ECC says *"Rate limiting on all endpoints"*. **Take the concern, reject the wording** — "all
endpoints" produces middleware nobody asked for on read paths that do not need it, and violates the
scope guard. **CSRF deliberately excluded**: Next.js server actions check origin by default, so the
sentence would produce redundant hand-rolled code in every app.

### 3.5 · Loading / empty / error states — **MERGE, NOT ADD · ~0 tokens**

`react/patterns.md`: *"Every Suspense boundary needs an Error Boundary above it."*
`react-native/accessibility.md`: *"Reflect loading/error/empty states in text the reader can reach —
not just spinners or color."* `app-design/SKILL.md §4` is literally titled *"The states that are
always missing"* and is already proposed as playbook content. **Do not ship twice** — add these two
clauses to that edit when it lands.

### 3.6 · Migration discipline — **SHIP · ~62 tokens**

> "A schema change is a new file in `supabase/migrations/`, never an edit to an existing one."
> "A migration that creates a table creates its RLS policies in the same file, one policy per
> operation — never `USING (true)`, never `FOR ALL`."

**ECC contributes nothing.** `grep -ril migrat` over all 122 files returns three hits, all
incidental. In 9,506 lines about how software should be built, migration discipline does not
appear. Scio names the folder and attaches no rule to it — on the riskiest surface of the fixed
stack, in a product whose wedge (ADR-0001) is *"software they intend to run and grow"*, where a
second build against an existing database is the normal case. The second clause is the cheapest
available guard against §3.2's failure: policies written in the same file as the table mean the
table cannot ship without one. **Biggest genuine gap found, and it had to be written, not mined.**

### 3.7 · Query shape — **SHIP · ~27 tokens**

> "Every list query has an explicit limit or range. Never query inside a loop over rows — fetch
> once and join."

From `common/code-review.md` — the corpus's only DB-performance content. Both failures are the
default output of a model writing Supabase client code screen by screen, and **no linter catches
either**, because `.select()` and `.map()` are legitimate in isolation. That is the test for prompt
text over a check, passed. A heuristic warning-level check is still worth adding (§4).

### 3.8 · Dependency policy — **SHIP · ~38 tokens**

> "Add a dependency only when it replaces code you would otherwise write and maintain. Pin the
> exact version. Nothing new for what the stack already does."

ECC's only real statement is `ruby/security.md`: *"Review new gems for maintainer activity, native
extension risk, transitive dependencies, and whether the same behavior can be implemented with
Rails core."* — the last clause is the transferable one. Scio has nothing, and should, for three
reasons: **cost** (install time on every build and sandbox run, ADR-0005); **Layer D** (a model
reaching for a new npm package for something the library already has defeats ADR-0014's match); and
**supply chain** (`ECC-MINED.md §4` already records ECC's own `npx -y` contradiction — pinning is
the lesson, this is where it lands in the output).

### 3.9 · What pays for it — **TRIM · −156 tokens**

**`folder_structure`, ~125 tokens.** `builder/file_plan.py` already computes each package's files.
Its docstring: *"That decision is deterministic and lives here, following the playbook's folder
structure — **not left to the model**, because the manifest's package→file map depends on it and a
model that renames a folder would silently break the marking→code coupling."* The model is handed
its paths. Not *fully* redundant — the same docstring records a real failure where a model invented
`@/lib/validation/booking` because the plan gave it nowhere to live — so **trim, don't delete**:
keep the two lines carrying a rule (`lib/db/ — no raw SQL in components`, and the migrations line
now expanded by §3.6), drop the six that only name folders. **−90.**

**`naming` lines 1–3, ~31 tokens.** kebab-case files, PascalCase components, camelCase functions —
mechanically checkable, belongs in the scaffold's ESLint config. **Keep lines 4–5** (`database:
snake_case, singular…` and `operations: verb_entity`) because those bind to the architecture
graph's canonical vocabulary and are semantic, not syntactic. **−31.**

**`quality` line 1, ~35 tokens.** *"No dead code, no commented-out blocks, no TODOs left behind."*
`_QUALITY_PATTERNS` already greps `TODO|FIXME`; `no-unused-vars` covers the rest. **−35.**

**Net +173 tokens.** Small enough that the decision is not really about cost — it is about whether
each sentence changes what gets generated. Seven of the eight do. The discipline is not "add
nothing"; it is **"add nothing a linter could have guaranteed"**, which is §4.

---

## 4 · Rules that should be deterministic checks, not prompt text

The brief calls this the more valuable outcome, and it is. Scio's stated method (ADR-0012) is
*rules do what rules can guarantee; the model is used only for judgement*, and
`builder/validation.py` opens by saying it out loud:

> "Deterministic on purpose. Asking a model whether the code it just wrote is secure gets you an
> opinion; grepping for a hardcoded key gets you a fact."

**The reframe.** ECC writes 9,506 lines telling a developer to obey rules that its own
`hooks.md` files then wire to a linter. It does the work twice and ships the weaker copy in prose.
For Scio the equivalent mistake would be a playbook sentence for anything the generated repo's own
toolchain can assert — so the instruction is: **the scaffold package writes the config; it does not
describe the rule.** Package 1 emits `eslint.config.js`, a strict `tsconfig.json`, a
`vitest.config.ts` with coverage thresholds and a CI workflow **once**, and all five later packages
inherit enforcement at **zero prompt tokens**. That is the highest-leverage idea in this document.

### Two different places a check can live

1. **On the architecture, before generation** — Layer B's 11 rules, Layer C's 9. Cost: one function
   call. Catches design incoherence before a relay run is spent.
2. **On the generated code, after** — `builder/validation.py`'s 7 agents, plus the generated repo's
   own eslint / tsc / vitest / lighthouse / gitleaks. Cost: CI time in a sandbox.

Everything below belongs to (2) unless marked.

### Already a check — do not add prompt text

`builder/validation.py` already blocks on all of these, so any playbook sentence restating them is
pure token waste: hardcoded credential / `sk-…` key / embedded JWT, `dangerouslySetInnerHTML`,
`eval(`, SQL built by `${}` interpolation (`security` agent); `TODO`/`FIXME`, `@ts-ignore`,
`: any` (`code_quality`, warning) and an empty file (`code_quality`, error); an operation in the slice missing from the code and
a screen with no page file (`contract_consistency`); a package with operations and no test file
(`tests_present`); an import crossing a package boundary (`import_boundary`).

### ECC rules that are lint config, stated as prose

| ECC rule | Source | Enforced by |
|---|---|---|
| functions < 50 lines | `common/coding-style.md`, `common/code-review.md` | `max-lines-per-function` |
| files < 800 lines (200–400 typical) | same | `max-lines`; ECC also ships a PreToolUse hook for it |
| nesting depth ≤ 4 | same | `max-depth` |
| no `console.log` in production | `typescript/coding-style.md` | `no-console` |
| avoid `any`, use `unknown` | `typescript/coding-style.md` | `@typescript-eslint/no-explicit-any` + `strict` |
| rules of hooks; exhaustive deps | `react/hooks.md` — *which mandates the plugin itself* | `eslint-plugin-react-hooks` |
| no array index as `key` | `react/patterns.md` | `react/no-array-index-key` |
| `target="_blank"` needs `rel` | `react/security.md` | `react/jsx-no-target-blank` |
| no `javascript:` URLs | `react/security.md` | `react/jsx-no-script-url` |
| semantic HTML, labels on inputs, ARIA correctness | `web/coding-style.md`, Scio playbook `accessibility` 1–3 | `eslint-plugin-jsx-a11y` |
| 80% coverage | `common/testing.md` | `vitest --coverage` thresholds |
| Core Web Vitals + bundle budgets | `web/performance.md` | Lighthouse CI + `size-limit` |
| no a11y violations in components | `react/testing.md` (`vitest-axe`) | axe assertion in the generated test setup |
| dependency CVEs | `java/`, `ruby/`, `rust/security.md` | `npm audit` / `pnpm audit` in CI |
| kebab-case files, PascalCase components | Scio playbook `naming` 1–3 | ESLint + a filename check |

**Fifteen rules, none of which should ever be a sentence in a build prompt.** ECC states all of
them in prose and additionally configures most of them; we should do only the second half.

### Checks worth writing that do not exist off the shelf

Ordered by value. The first three are the ones that matter.

| # | Check | Where | Why no linter has it |
|---|---|---|---|
| 1 | **A policy per table per operation; no unconditional policy.** Reject `USING (true)` and `FOR ALL` in `supabase/migrations/*.sql` | Layer B rule 12 (architecture) **and** a SQL scan on generated migrations | Already proposed in `next/LAYER-B-UNDERSTANDING.md §3.5`; this adds the code-side half. This is CVE-2025-48757 made impossible rather than discouraged. |
| 2 | **`NEXT_PUBLIC_*` whose name matches `secret\|service_role\|private\|password\|token`** | `_SECRET_PATTERNS`, ~3 lines of regex | The existing patterns catch a hardcoded key; they do not catch a real key correctly loaded from a fatally-named env var |
| 3 | **A migration file modified rather than added** | git diff over `supabase/migrations/` between builds | Requires build-to-build state; nothing in a linter has it. Enforces §3.6 |
| 4 | `localStorage.setItem` with a name matching `token\|session\|auth\|jwt` | `_UNSAFE_PATTERNS`, 1 line | Storing to localStorage is legitimate; storing *credentials* is not, and only the key name distinguishes them |
| 5 | `fetch(` inside a `useEffect(` body | `_UNSAFE_PATTERNS`, 1 multiline regex | `react-hooks` does not flag it; it is a design rule, not a hook rule |
| 6 | `.select(` with no `.limit(` / `.range(` / `.single(` in the chain | `_QUALITY_PATTERNS`, **warning severity** | Genuine false positives on single-row lookups — hence warning, and hence §3.7 also ships as prompt text |
| 7 | A route handler or server action that builds a fetch URL from a parameter | `_UNSAFE_PATTERNS`, connector packages only | The SSRF rule from `nuxt/security.md`, scoped so it does not fire on five packages that make no external call |

Seven checks. Items 2, 4, 5 and 6 are one regex line each in an existing tuple, in a file that
already has the severity semantics, the fix-instruction loop and the tests. **That is the cheapest
quality work available anywhere in this document** — cheaper than any playbook edit, and it is a
guarantee rather than a probability.

---

## 5 · What a generated app needs that neither playbook has

| Concern | ECC | Scio playbook | Verdict |
|---|---|---|---|
| **Error handling** | 14 headings, all language-idiom (`Result`, `Optional`, `try/catch`) | nothing | §3.3 covers the leak direction. **Still missing: what the user sees when an operation fails.** A generated CRUD app with no defined failure path is not shippable. Candidate: *"Every operation has a visible failure path — a message the user can act on, never a blank screen."* |
| **Logging** | *"no `console.log`, use a logging library"* and nothing else, in 15 files | *"no secrets… in logs"* | Neither says **what to log**. A generated app with no request log cannot be debugged by the developer it was handed to (ADR-0001's handoff). Genuine open question — flag, do not invent |
| **Input validation** | 11 headings | names the boundary and zod | **Ours is better.** No change |
| **Secrets** | 13 headings, all "use env vars" | stronger, stack-correct | Ours, plus §3.2 |
| **Dependency policy** | 3 language-local mentions | nothing | §3.8 |
| **Migration discipline** | **3 incidental hits in 9,506 lines** | a folder name | §3.6. **Biggest gap; had to be written, not mined** |
| **Accessibility beyond design** | `react-native/accessibility.md` is the corpus's best a11y file | 4 good lines | Ours is missing: state announcement (`aria-live` for async errors), focus moved to new content on modal/route change and restored on close, and the WCAG AA numbers (4.5:1 body, 3:1 large). The first two are not lintable and are worth ~30 tokens; the third is an axe check |
| **Performance budgets** | good numbers, wrong medium | nothing | §4 — a check, never prompt text |
| **Observability / error reporting** | one paragraph, RN only (`@sentry/react-native`) | nothing | **A product decision, not a playbook line.** An app "they intend to run and grow" with no error reporting is not runnable, but adding Sentry means adding a service the user did not ask for. Belongs in an ADR |
| **Idempotency** | **zero hits in 9,506 lines** | nothing | Scio's own `G-F03` is a *confirmed live* cross-tenant idempotency replay. Nobody has written this down anywhere, in either system |
| **Rollback / backup** | **zero hits** | nothing | Out of scope for a generated app's prompt; belongs to ADR-0019 (Proposed) |
| **What not to do** | only `react/security.md` uses the negative form | none — all thirty rules are positive | §3.1. The cheapest structural improvement to the playbook |
| **A gate on the finished app** | `react-native/production-readiness.md` — the only release checklist in the corpus | 7 per-package agents, nothing on the promoted repo | ADR-0017 promotes the workspace with git history intact and asserts nothing about it. **Not a playbook line — an ADR-0017 question**, and the sharpest thing §2 surfaced |
| **Data deletion / retention** | none | none | ADR-0019 is Proposed. When it settles, the generated app needs a rule for what "delete" means |

Three of these — **idempotency, rollback, and what the user sees when an operation fails** — are
absent from *both* 9,506 lines of ECC and 30 lines of Scio. That is the answer to "what is the
playbook missing that nobody has ever asked": not more rules of the kind either system has, but
the runtime behaviours that only appear once an app has been running for a week.

---

## 6 · Verdict table

| # | Rule / cluster | Source | Verdict | Tokens |
|---|---|---|---|---|
| 3.1 | `## Never` block, 5 lines | `react/security.md`, `nuxt/security.md`, `react/patterns.md` | **SHIP** | +94 |
| 3.2 | Anon key is public; safe only because RLS is explicit | `react-native/security.md` | **SHIP** | +47 |
| 3.3 | Generic message out, detail to the log | `java/security.md` | **SHIP** | +37 |
| 3.4 | Rate-limit auth surfaces and unauthenticated mutations | `common/security.md`, narrowed | **SHIP** | +24 |
| 3.6 | Migration discipline + policies in the same file | **written; ECC has none** | **SHIP** | +62 |
| 3.7 | Explicit limit; no query in a loop | `common/code-review.md` | **SHIP** | +27 |
| 3.8 | Dependency policy | `ruby/security.md`, generalised | **SHIP** | +38 |
| 3.5 | Loading / empty / error states | `react/patterns.md`, `react-native/accessibility.md` | **MERGE into `app-design` §4** | 0 |
| 5 | Focus management + `aria-live` on async errors | `react-native/accessibility.md` | **SHIP with the a11y edit** | +30 |
| 3.9 | `folder_structure` lines 1–3, 5–8 | Scio playbook | **TRIM** — `file_plan.py` owns it | −90 |
| 3.9 | `naming` lines 1–3 | Scio playbook | **TRIM** — ESLint owns it | −31 |
| 3.9 | `quality` line 1 (dead code, TODOs) | Scio playbook | **TRIM** — already a check | −35 |
| 4 | RLS policy per table per operation | `next/§3.5` + a SQL scan | **CHECK** | 0 |
| 4 | `NEXT_PUBLIC_*` named like a secret | new | **CHECK** — 3 regex lines | 0 |
| 4 | Migration edited rather than added | new | **CHECK** — git diff | 0 |
| 4 | Credentials in `localStorage`; `fetch` in `useEffect`; unbounded `.select()`; SSRF in connectors | `react/security.md`, `react/hooks.md`, `common/code-review.md`, `nuxt/security.md` | **CHECK** — 1 regex line each | 0 |
| 4 | 15 lint-config rules (function length, file length, nesting, `no-console`, `any`, hooks rules, `key`, `rel`, `javascript:`, jsx-a11y, coverage %, CWV, axe, `npm audit`, filename case) | `common/`, `typescript/`, `react/`, `web/` | **CHECK — scaffold config, not prose** | 0 |
| — | CSRF tokens | `common/security.md`, `react/security.md` | **LEAVE** — Next.js server actions check origin; would produce redundant code | — |
| — | KISS / DRY / YAGNI / "immutability (CRITICAL)" | `common/coding-style.md` | **LEAVE** — unfalsifiable slogans | — |
| — | Mandatory TDD red-green loop | `common/testing.md` | **LEAVE** — incoherent for one-shot generation; our "happy path + main failure" is the right translation |
| — | Repository pattern, API response envelope | `common/patterns.md`, `typescript/patterns.md` | **LEAVE** — architectural taste, and Layer D's library already fixes the shapes it cares about |
| — | Container/presentational split, compound components, state decision tree | `react/patterns.md`, `web/patterns.md` | **LEAVE** — good advice, ~400 tokens, changes nothing a reviewer would fail |
| — | RTL query priority, MSW, `userEvent` over `fireEvent`, coverage-by-layer table | `react/testing.md` (208 lines) | **LEAVE from the playbook** — belongs in the scaffold's `test-utils.tsx` and the Layer D library entry, generated once |
| — | Model selection, context windows, extended thinking | `common/performance.md` | **LEAVE** — not about the generated app at all |
| — | `agents.md`, `hooks.md`, `git-workflow.md`, `development-workflow.md` | `common/` | **LEAVE** — ECC's process, not the artifact's properties |
| — | 17 language directories, ~7,400 lines | `rules/` | **LEAVE** — ADR-0011 fixes the output stack |
| — | Observability / error reporting; idempotency; rollback; deletion semantics | mostly absent from both | **ADR, not playbook** — §5 |

**Net playbook change: +173 tokens (668 → 841, +26%), ≈ +1,000 tokens per build.**
**Net check change: 7 new deterministic checks, 4 of them a single regex line in a file that
already has the loop, the severity model and the tests.**

The ratio is the point. Seven sentences and seven checks came out of 9,506 lines, and the checks
are worth more than the sentences.

---

*Mined 2026-08-26 against `affaan-m/ECC` @ `rules/` (122 files, 9,506 lines) and
`apps/engine/src/scio_engine/layerb/playbook.{py,yaml}`, `builder/validation.py`,
`builder/file_plan.py`, `layerc/contract.py`. Structure of `rules/` already covered in
`docs/ECC-MINED.md §4`; design content deliberately out of scope per
`.claude/skills/app-design/SKILL.md`.*
