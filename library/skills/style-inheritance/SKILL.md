---
name: style-inheritance
description: Use when new code will be added to an existing or legacy repo and must match its house style — before starting a feature, refactor, or large AI-generated change in an unfamiliar codebase, or when reviewers keep flagging that generated code "doesn't look like ours." Extracts the repo's IMPLICIT, undocumented conventions (file/module layout, naming casing, import ordering, error-handling and logging idioms, test structure, comment density, formatting quirks the linter doesn't cover) by sampling real files, then codifies them into a CONVENTIONS.md the author reads and follows so new code inherits the established style instead of drifting toward generic defaults. Method only — produces a reference doc; installs NO hooks and enforces nothing automatically. Not for greenfield repos with no style to inherit, not for running formatters/linters, and not for style rules already captured by an existing config (eslint, prettier, editorconfig, ruff).
---

# Style Inheritance

Extract a repo's unwritten conventions and codify them so newly added code matches what
is already there, instead of drifting to the model's generic defaults.

## When to use
- Adding non-trivial code to a legacy or unfamiliar codebase with no written style guide.
- AI-generated diffs keep getting flagged as "not our style" in review.
- Onboarding to a repo where the real conventions live only in the existing code.

Do NOT use for: greenfield repos (no style to inherit yet); rules already enforced by a
committed formatter/linter config (defer to those); or running the tools themselves.

## Steps
1. **Scope.** Pick the language/area you're about to touch. Confirm no CONVENTIONS.md
   already covers it; if one exists, refine rather than replace.
2. **Check existing config first.** Read any editorconfig, linter, or formatter config.
   Anything they already enforce is OUT of scope — codify only what they miss.
3. **Sample real files.** Read 6–12 representative, recently-changed files in that area
   (mix of core modules and their tests). Prefer files by the same team, not vendored code.
4. **Observe, per dimension.** For each, note the DOMINANT pattern and any split:
   - Structure: file/module layout, one-vs-many exports, folder grouping.
   - Naming: casing per kind (files, types, funcs, consts), abbreviations, prefixes.
   - Imports: grouping and ordering, absolute vs relative, barrel usage.
   - Idioms: error handling, logging, async style, null/optional handling, config access.
   - Tests: framework, file location/naming, arrange-act-assert shape, fixture style.
   - Density: comment frequency, docstring presence, function length, nesting depth.
5. **Quantify.** Where possible attach a rough ratio ("~90% of tests colocated as
   `*.test.ts`") so ties are visible and the rule is falsifiable, not vibes.
6. **Write CONVENTIONS.md.** One section per dimension: the rule, a one-line rationale,
   and a real 2–5 line example COPIED from the repo (with its path). Mark genuine splits
   as "either accepted" rather than inventing a winner.
7. **Add a "when unsure" line.** Tell the author to grep for a sibling of the thing they're
   writing and mirror it, rather than guessing.
8. **Place and reference it.** Save near the code it governs (e.g. area root). Point the
   author to read it before writing, and to update it when a convention genuinely shifts.

## Rules
- Descriptive, not prescriptive: report what the repo DOES; never impose outside taste.
- Every rule cites a real example with a file path — no invented conventions.
- Do not duplicate what a committed linter/formatter already enforces.
- Preserve real inconsistency as "either accepted"; don't fabricate a single answer.
- Method only: never install a PreToolUse or any auto-run hook, and make no network/CLI
  calls. The doc is advisory — the author chooses to follow it.
- Keep it short and scannable; a convention doc nobody reads inherits nothing.
