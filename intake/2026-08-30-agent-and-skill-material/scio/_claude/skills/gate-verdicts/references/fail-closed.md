# D1 · Fail closed, in order, with no default branch

Load this when writing the control flow of a gate that grades output it did not produce.

## The pattern, quoted

From `codex`, read at `docs/mined/PASS2-GSTACK-SKILLS.md:83`. It is the strongest refusal in the
mined corpus and it is nineteen lines:

> **The gate FAILS CLOSED** — a run that cannot be verified is a FAIL, never a PASS. Work through
> these checks IN ORDER; the first match wins:
>
> 1. exit code is non-zero (including 124) → **FAIL** (fail-closed: the review did not complete, so
>    there is no verified result). Expired auth, a bad flag, a timeout, or a model-entitlement 400
>    all land here instead of masquerading as a clean pass.
> 2. captured output is empty or whitespace-only → **FAIL** (nothing was reviewed).
> 3. output contains `[P0]` or `[P1]` → **FAIL** (N critical findings).
> 4. output contains **no** `[P0]`, `[P1]` or `[P2]` tag anywhere → **FAIL** (fail-closed: untagged
>    output — the severity markers this gate greps for are absent, so "no critical findings" cannot
>    be verified mechanically; a human must read the verbatim output and judge).
> 5. severity tags are present and none is P0/P1 → **PASS**.
>
> There is no default branch: PASS is only reachable through check 5.

The sentence to carry over verbatim:

> **"No `[P1]` substring" and "no critical findings" are different claims — never infer PASS from
> an untagged body.**

And its companion, from `review` in the same document: *"A timed-out pass is MISSING COVERAGE, not
a clean bill — say so explicitly rather than continuing as if it had reviewed."*

## The four unverifiable states, generalised

Every gate that reads another process's or another model's output has these four. Name them in the
gate, do not discover them in production.

| State | Cause | Reported as |
|---|---|---|
| **errored** | non-zero exit, exception, auth failure, entitlement error | verification failure |
| **empty** | no output, whitespace only | verification failure |
| **truncated** | output cut mid-structure; a parse that consumed part of it | verification failure |
| **untagged** | output present and readable, but carries none of the markers the gate greps for | verification failure |

A fifth is worth adding for a gate that drives something: **not driven** — the tool was not
available, the flag was off, the browser was absent. This repository already produces it honestly
(*"the app was not running with data, so nobody drove it"*, `loop.py:523`) and the discipline is to
keep it a value rather than let it collapse into a pass.

## Polarity, for boundaries rather than graders

From `freeze`, `docs/mined/PASS2-GSTACK-SKILLS.md:108`:

> Polarity is fail-closed: a tool payload the hook cannot parse is DENIED, not allowed — **a
> boundary that fails open is not a boundary.** A payload that parses but has no `file_path` (a
> non-file tool) is allowed. Symlinks are resolved through their FINAL component, so an in-boundary
> symlink pointing outside the boundary is checked against its target.

Two details worth taking with it:

- **The hard-deny tier is deliberately narrow.** They deny exactly two shapes, and only for simple
  commands with no `;`, `&&`, `||`, `|` or newline; compound shapes fall through to a softer ask.
  *A narrow provably-correct deny list beats a broad guessable one.*
- **Resolve, then verify the prefix.** Never match-then-deny-known-bad. This repository already
  does it for the sandbox (`_guard_path`, `sandbox.py:125`); the finding at
  `docs/mined/PASS2-FOUR-REPOS.md:651` is the third instance in two mining passes of a denylist
  standing where canonicalisation belongs.

## What this does not cover

A gate can be perfectly fail-closed and still check the wrong thing. `check_tests_present` fails
closed on a missing file and still passes `app/latest/page.tsx`, because its predicate is a
substring. Fail-closed is about the *control flow*; the predicate is a separate review.
