# Pricing a Playbook candidate, and what is already a check

Loaded from `SKILL.md` §3 and §7 step 5. Read this when pricing a candidate; the procedure does not
require it otherwise.

All figures measured against `/home/user/hello-world` on **2026-08-26**, read-only. Token counts are
**characters ÷ 4** — `messages.count_tokens` is the correct instrument and was not available.

---

## 1 · The ledger

| Item | Tokens |
|---|---:|
| `Playbook.as_prompt_section()` today (2,671 chars) | **668** |
| × 6 package prompts on the canonical booking app | **≈ 4,008 per build** |
| Stated cap (`docs/mined/ECC-RULES.md` §43, `PASS2-ECC-RULES-COMMANDS.md:13`) | **≈ 1,200** |
| Headroom today | **≈ 532** |
| A prior mined proposal's total, both passes applied | **961** (`PASS2-ECC-RULES-COMMANDS.md:662`) |

**The cap is a discipline someone chose, not a measured degradation threshold.** Its own source
introduces it so that headroom does not read as licence. Quote it with that sentence attached.

**The 668 is not the whole prompt.** `playbook.py:118` also passes
`architecture.model_dump_json(indent=2)` — the entire architecture graph, indented — into every
package prompt, with the docstring at `:83` conceding *"for now it assembles the whole
architecture."* Any argument that the Playbook is the expensive constant should be checked against
that number first. It is not this skill's decision; it is
`docs/next/LAYER-C-BUILD-PLAN.md` §2.2's.

---

## 2 · The eleven candidates currently queued

From `docs/triage/LAYER-BC-TRIAGE.md` §2.1. Each is an **ADR row**, not an edit. They cannot all
land inside 532 tokens.

| Candidate | Tokens | Route (SKILL.md §3) |
|---|---:|---|
| No mutable module-level state in RSC/SSR | ~22 | 5 — route 4 genuinely unavailable |
| `USING ((SELECT auth.uid()) = user_id)` | ~30 | 5 |
| Idempotent retries; verify webhook signature before parse | ~34 | 5 |
| Request schemas reject unknown keys | ~20 | 5, or 2 if the emitter writes `.strict()` |
| `font-variant-numeric: tabular-nums` | ~18 | 5, **as a Revise** — net ≈ 0 |
| 40×40px hit target | ~26 | 4 first — near-computable against Tailwind output |
| `react-patterns` decision trees | unpriced | 5, and the largest of the eleven |
| `frontend-design-direction`'s three lines | unpriced | 5; one is superseded before it lands |
| Refusal message shape | unpriced | 5 |
| Hydration residue | ~30 minus the grep half | 4 + 5 split |
| `onUnhandledRequest: "error"` | ~16 | **3** — scaffold config, zero prompt tokens |

Two of the eleven are unpriced and one is a replacement. **Price before arguing.**

---

## 3 · Already a deterministic check — never restate in prose

`builder/validation.py`, verified 2026-08-26. A Playbook sentence restating any of these buys
nothing and costs tokens on every build.

**Error severity** — `check_security`, via `_SECRET_PATTERNS` and `_UNSAFE_PATTERNS`:

| Pattern | Message |
|---|---|
| `api_key`/`secret`/`password`/`token` assigned a 12+ char literal | a credential appears to be hardcoded |
| `sk-…` (16+) | a provider API key is embedded |
| `eyJ….` | a JWT is embedded |
| `dangerouslySetInnerHTML` | risks XSS |
| `eval(` | must not appear |
| `` `SELECT …${` `` | SQL built by string interpolation |

**Warning severity** — `check_code_quality`, via `_QUALITY_PATTERNS`: `TODO`/`FIXME`,
`@ts-ignore`/`@ts-nocheck`, `: any`. Plus an empty file at error severity.

**Structural checks**, each its own function: `check_tests_present` (a package with operations and
no test file), `check_contract_consistency` (an operation in the slice missing from the code; a
screen with no page file), `check_import_boundary` (an import crossing a package boundary),
`check_delivered_quality`, `check_files_complete`.

`docs/mined/ECC-RULES.md` §4 counted **eleven** of these against the mined corpus and found ECC
stating all eleven in prose as well.

---

## 4 · Lint configuration, stated as prose — the fifteen

From `docs/mined/ECC-RULES.md` §4. Each is a rule a config file asserts, which the mined corpus
also wrote out as a prompt sentence. **Scio should do only the second half.**

| Rule | Enforced by |
|---|---|
| functions < 50 lines | `max-lines-per-function` |
| files < 800 lines | `max-lines` |
| nesting depth ≤ 4 | `max-depth` |
| no `console.log` in production | `no-console` |
| avoid `any`, use `unknown` | `@typescript-eslint/no-explicit-any` + `strict` |
| rules of hooks; exhaustive deps | `eslint-plugin-react-hooks` |
| no array index as `key` | `react/no-array-index-key` |
| `target="_blank"` needs `rel` | `react/jsx-no-target-blank` |
| no `javascript:` URLs | `react/jsx-no-script-url` |
| semantic HTML, labels, ARIA correctness | `eslint-plugin-jsx-a11y` |
| 80% coverage | `vitest --coverage` thresholds |
| Core Web Vitals + bundle budgets | Lighthouse CI + `size-limit` |
| no a11y violations in components | axe assertion in the generated test setup |
| dependency CVEs | `npm audit` / `pnpm audit` in CI |
| kebab-case files, PascalCase components | ESLint + a filename check |

**Two rows of the fifteen name Scio's own Playbook as a source** — the semantic HTML / labels /
ARIA row cites `accessibility` 1–3, and the file-and-component-naming row cites `naming` 1–3. Those
lines are candidates for **deletion** under §3 route 3, not for extension. Deleting a rule runs the
same procedure as adding one: the fixture (SKILL.md §5.1) must show the config catches what the
sentence claimed, before the sentence goes.

---

## 5 · Checks worth writing that no linter ships

From `docs/mined/ECC-RULES.md` §4, ordered by value. These are **route 4** destinations for
candidates that would otherwise become prose.

| # | Check | Where |
|---|---|---|
| 1 | A policy per table per operation; reject `USING (true)` and `FOR ALL` | a Layer B rule **and** a SQL scan on generated migrations |
| 2 | `NEXT_PUBLIC_*` whose name matches `secret\|service_role\|private\|password\|token` | `_SECRET_PATTERNS`, ~3 lines |
| 3 | A migration file modified rather than added | git diff across builds |
| 4 | `localStorage.setItem` with a key matching `token\|session\|auth\|jwt` | `_UNSAFE_PATTERNS`, 1 line |
| 5 | `fetch(` inside a `useEffect(` body | `_UNSAFE_PATTERNS`, 1 multiline regex |
| 6 | `.select(` with no `.limit(`/`.range(`/`.single(` | `_QUALITY_PATTERNS`, **warning** — genuine false positives, and the one case that legitimately ships as prose too |
| 7 | A route handler building a fetch URL from a parameter | `_UNSAFE_PATTERNS`, connector packages only |

Items 2, 4, 5 and 6 are one regex line each in a tuple that already has severity semantics, the
fix-instruction loop and tests.
