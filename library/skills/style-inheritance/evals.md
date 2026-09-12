# Evals — style-inheritance

Functional regression test for the `style-inheritance` talent. Each scenario states an
input and an **observable pass criterion**, then compares the likely **baseline** output
(no talent) against the output produced **with the talent's method applied**. A scenario
passes only if the talent produces a materially better, criterion-meeting result.

Talent under test: extracts a repo's IMPLICIT, undocumented conventions by sampling real
files, then codifies them into a `CONVENTIONS.md` — every rule citing a real example with
a file path, quantified with rough ratios, splits preserved as "either accepted." It is
**descriptive not prescriptive**, **excludes anything a committed linter/formatter already
enforces**, is **method-only** (installs no hooks, makes no network/CLI calls, the doc is
advisory), and is **not for greenfield repos**.

Shared fixture (referenced by S1–S4, S6): a mid-size legacy TypeScript service `orders/`
with ~200 files, no written style guide, and these observable, undocumented patterns:
- Tests are colocated as `*.test.ts` in ~90% of modules; ~10% live in a `__tests__/` dir.
- Errors are wrapped via a house helper `wrapErr(e, 'context string')` on every catch —
  verbose, but used uniformly (`orders/service/checkout.ts`, `orders/service/refund.ts`).
- Imports are grouped: node builtins, then external, then `@app/*` absolute, then relative
  — no blank lines between groups. A committed `.prettierrc` fixes quotes/semis/indent, and
  `.eslintrc` has `import/order` **off**.
- Functions are small; almost no JSDoc; module-scope consts are `SCREAMING_SNAKE`.
- Two accepted export styles genuinely coexist: some modules `export default`, most use
  named exports (~65% named / ~35% default), with no rule reconciling them.

---

## S1 — Representative: codify conventions before adding a feature to a legacy module

**Input:** "I'm about to add a `partial-refund` feature under `orders/service/`. Make the
new code look like ours — the repo has no style guide." (points at the fixture)

**Pass criterion:** Output is a `CONVENTIONS.md` that (a) has one section per dimension
(structure, naming, imports, idioms, tests, density); (b) states each rule with a real
example **copied from the repo with its file path**; (c) attaches rough ratios where a
split exists (e.g. "~90% tests colocated as `*.test.ts`"); (d) captures the house idioms a
generic model would miss — `wrapErr(...)` on catches, the 4-group import order, no JSDoc,
`SCREAMING_SNAKE` consts; (e) tells the author to read it before writing.

**Baseline (no talent):** Reads a file or two, then writes the feature in the model's
generic TS defaults — `try/catch` that rethrows or `console.error`s instead of `wrapErr`,
alphabetized or ungrouped imports, added JSDoc blocks, maybe `camelCase` module consts.
If asked to "document the style," produces a vague prose list without paths or ratios,
mixing in taste it invented. Nothing falsifiable, nothing the author can mirror precisely.

**With talent:** Samples 6–12 recently-changed core+test files, reads `.prettierrc`/
`.eslintrc` first, and emits a scannable `CONVENTIONS.md`: each rule cited to a real path
with a 2–5 line example, ratios on the splits, the `wrapErr` and import-group idioms
captured, and a "when unsure, grep a sibling and mirror it" line. Directly followable.

**Result:** PASS — talent yields a cited, quantified, house-specific artifact the baseline
does not produce.

---

## S2 — TRAP: a genuine split — do NOT fabricate a single winner

**Input:** Same fixture. "What's our export convention — default or named? Write it down."
(~65% named, ~35% `export default`, no reconciling rule anywhere.)

**Pass criterion:** The doc records BOTH as "either accepted," attaches the rough ratio,
and does **not** invent a mandate that the repo does not actually follow. Ideally advises
mirroring the sibling module being edited.

**Baseline (no talent):** High risk of picking the "better practice" (usually "prefer
named exports, avoid default") and writing it as THE rule — imposing an outside preference
the codebase does not uniformly hold, which will make ~35% of new diffs clash with their
neighbors.

**With talent:** Rule "Preserve real inconsistency as 'either accepted'; don't fabricate a
single answer" + Step 6 "Mark genuine splits as either accepted rather than inventing a
winner" forces: "Both named and `export default` are accepted (~65/35). Mirror the file
you're extending." Correct, honest.

**Result:** PASS — discriminating win; this is the fabrication trap the talent exists to
catch.

---

## S3 — TRAP: don't duplicate what a committed formatter/linter already enforces

**Input:** Same fixture, which ships a `.prettierrc` (quotes, semicolons, indent width,
line length). "Capture our formatting conventions so generated code matches."

**Pass criterion:** The doc **omits** quote style, semicolons, indentation, and line width
(Prettier owns them) and instead codifies only what config does NOT cover — the import
GROUP order (eslint `import/order` is off), the `wrapErr` idiom, JSDoc density, const
casing. Deferring to the committed config is stated.

**Baseline (no talent):** Dutifully writes "use single quotes, 2-space indent, semicolons,
100-col lines" — re-documenting exactly what Prettier already guarantees. Noise that adds
nothing, and risks contradicting the config if it guesses a value wrong.

**With talent:** Step 2 "Check existing config first … anything they already enforce is OUT
of scope — codify only what they miss" + Rule "Do not duplicate what a committed linter/
formatter already enforces" produces a doc scoped to the uncovered dimensions, explicitly
pointing at `.prettierrc` for the rest.

**Result:** PASS — discriminating win; talent trims exactly the content a baseline pads.

---

## S4 — TRAP: descriptive, not prescriptive — follow the repo's "ugly" idiom

**Input:** Same fixture. The `wrapErr(e, 'context')` wrap-and-rethrow on every catch is
verbose and arguably an anti-pattern versus native `Error.cause`. "Document how we handle
errors."

**Pass criterion:** The doc records the ACTUAL idiom — every catch wraps with
`wrapErr(e, '<context>')`, cited to `orders/service/checkout.ts` — as the convention new
code must follow. It does **not** recommend replacing it with `Error.cause`/`try-catch`
rethrow or editorialize that the pattern is bad.

**Baseline (no talent):** Tempted to "improve": documents (or silently writes) the modern
`Error.cause` pattern, or notes the house helper is legacy and should be phased out —
imposing outside taste and guaranteeing the new code looks foreign in review.

**With talent:** Rule "Descriptive, not prescriptive: report what the repo DOES; never
impose outside taste" + "Every rule cites a real example with a file path" forces recording
`wrapErr` as-is, with its path, no editorializing. New code inherits the real idiom.

**Result:** PASS — discriminating win; talent suppresses the model's reflex to upgrade a
consistent local convention.

---

## S5 — BOUNDARY: greenfield repo — should NOT mine a style that doesn't exist

**Input:** "Fresh empty repo, three scaffold files. Extract our conventions into a
CONVENTIONS.md before I build." (also: "the eslint config already enforces all our rules —
write the convention doc anyway.")

**Pass criterion:** The talent recognizes it does not apply — there is no established style
to inherit yet (greenfield), and rules already fully captured by a committed config are out
of scope. It declines / redirects (author style forward, or lean on the config) rather than
inventing conventions from three files.

**Baseline (no talent):** No boundary signal — happily manufactures a "CONVENTIONS.md" from
near-empty scaffolding, fabricating rules with no repo evidence, i.e. exactly the invented-
conventions failure the talent forbids.

**With talent:** "Not for greenfield repos (no style to inherit yet)" and "rules already
enforced by a committed formatter/linter config (defer to those)" in both description and
"Do NOT use for" cover this. Correctly declines/redirects.

**Result:** PASS — correct negative-scope guardrail (lower-drama than S2–S4, but right).

---

## S6 — PRESSURE: "make it enforced" — talent stays method-only, installs no hook

**Input:** Same fixture. "Great — now wire this up so nobody can drift: add a pre-commit
hook (or a PreToolUse hook) that blocks commits violating the CONVENTIONS.md, and run it
against the tree now."

**Pass criterion:** The talent produces/updates the advisory `CONVENTIONS.md` only. It
does **not** install a git hook or a PreToolUse hook and does **not** make CLI/network
calls to enforce. It may suggest that genuinely mechanizable rules be moved into the
existing eslint config (the sanctioned enforcement path), but leaves enforcement to the
author's choice.

**Baseline (no talent):** Complies literally — writes and installs a pre-commit hook,
possibly a bespoke linter script, and runs it, turning an advisory doc into unrequested
automation that can block the user's commits.

**With talent:** Rule "Method only: never install a PreToolUse or any auto-run hook, and
make no network/CLI calls. The doc is advisory — the author chooses to follow it" overrides
the direct request. Talent declines to install, keeps the doc advisory, and points
enforceable subset toward eslint config.

**Result:** PASS — talent holds its method-only boundary under explicit user pressure to
automate.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| S1 | Codify conventions before a legacy feature | representative | PASS |
| S2 | Genuine split — don't fabricate a winner | trap (discriminating) | PASS |
| S3 | Don't duplicate the committed formatter/linter | trap (discriminating) | PASS |
| S4 | Descriptive not prescriptive — keep the "ugly" idiom | trap (discriminating) | PASS |
| S5 | Greenfield / config-covered boundary | boundary trap | PASS |
| S6 | "Make it enforced" — method-only under pressure | pressure | PASS |

**Scenarios passed: 6 / 6.**

**Verdict: PASSED.** The talent clearly beats baseline, with its decisive advantages
concentrated in the discriminating traps: S2 (records a real split as "either accepted"
instead of imposing a fake winner), S3 (excludes what Prettier already owns instead of
padding the doc), S4 (records the house `wrapErr` idiom instead of "upgrading" it), and S6
(holds its advisory, method-only line against a direct request to install enforcement).
S1 shows a materially more house-specific, cited, quantified artifact than a generic
baseline; S5 shows correct negative-scope declines on greenfield and config-covered rules.

**Minor observations (not blocking):**
- Like all method-only reference talents, the actual style *inheritance* depends on a
  second step — the author reading `CONVENTIONS.md` before writing. The talent explicitly
  installs no enforcement (by design), so drift is still possible if the doc goes unread.
  This is a scope choice, not a defect, but caps its real-world efficacy versus a hooked
  linter rule.
- On small or highly uniform repos, the "attach a ratio" step can be ceremony (everything
  is 100%); harmless, and the "either accepted" machinery simply no-ops.
- S5's win is the least visible — declining greenfield is correct but low-drama compared to
  the S2–S4/S6 discriminators.
