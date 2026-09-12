# Preregistered decision rule — build `eval-set-curation-v2`

**Written 2026-09-02, at phase 2.1 while the probe was still running.** No arm output
existed when this file was written; the probe runs had not returned, the artefact had not
been started, and the expectation set did not exist. That ordering is the whole value of
this file and it is the only thing about it that cannot be reconstructed afterwards.

## Why it exists

`pipeline/build/decide.py` resolves a build's rule in three branches. This package hits the
third:

- it supplies `threshold` as prose, and
- it supplies **no** `threshold_rule`, and
- its prose is **not** the contract's `acceptance.default_rule` verbatim.

So `decide.py` will return `UNDECIDABLE` with the reason *"the preregistered threshold is
prose that is not the contract's default rule, and no threshold_rule was supplied — no code
can evaluate it. Read it yourself, and note that reading it now means reading it after the
results."*

Reading it after the results is exactly the freedom the preregistration removes. This file
does the reading **before** them.

## The two texts, side by side

Package `threshold`:

> Across k >= 2 repeats: zero regressions on correctness, no more than 20 percent worse on
> tokens or tool calls, and at least one win on correctness or shape that survives every
> repeat. A clean baseline does not stop the build; a win on shape alone satisfies the clause.

Contract `acceptance.default_rule`:

> Across k >= 2 repeats: zero regressions on correctness, no more than 20 percent worse on
> tokens or tool calls, and at least one test where the skill wins with the win surviving the
> repeat.

The clauses are the same clauses. The package's two extra sentences state, in words, the
behaviour `decide.py`'s `DEFAULTS` already implements: `win_axes` is
`["correctness", "shape"]` and the code comment on the win clause says in full why shape
alone counts ("a run where both arms are right on every test and the skill earned its place
by making the OUTPUT SHAPE right ... scored on correctness only, that run is a tie and the
skill is discarded for a reason nobody measured"). The package prose is a restatement of the
default, not a different rule.

## The rule this build is decided by

Exactly `decide.DEFAULTS`, no field altered:

```json
{
  "min_repeats": 2,
  "cost_tolerance": 0.20,
  "cost_axes": ["tokens", "tool_calls"],
  "require_win": true,
  "win_must_survive": true,
  "win_axes": ["correctness", "shape"],
  "max_repair_loops": 3
}
```

## How it is applied at 8.1

1. `decide.py <build-dir>` is run first and its refusal is recorded as an event, unedited.
   The gate is not argued with and its output is not suppressed.
2. The same file's `evaluate()` is then called on the same rows with the parameters above.
   It is the same code path the second branch of `resolve_rule` would have taken had the
   package carried a `threshold_rule` key. No judgement is inserted between the rows and the
   verdict.
3. Both results go in the record. If they disagree in any way other than
   `UNDECIDABLE` -> a decided verdict, the `UNDECIDABLE` stands.

## What this file does NOT license

It does not relax any parameter, does not add an axis, does not widen a tolerance, and does
not change what counts as a win. If the rule above returns `iterate`, the build iterates.

## The finding for the package contract

A package may preregister prose that no code can evaluate and still be ADMITTED with zero
warnings. `package_contract.py` requires `threshold` and treats `threshold_rule` as optional,
so the one field that makes the verdict machine-decidable is the one field nothing asks for.
Two builds in a row have now had to resolve this by hand. Proposed: admission emits a WARNING
when `threshold_rule` is absent and `threshold` is not the default prose verbatim — the case
where the gate is already known, at admission time, to be unable to decide later.

## Human override — 2026-09-02, AFTER the result was visible

**The registered rule refused this build.** `decide.py` returned **ITERATE**: every quality clause
passed and both cost clauses failed, at 1.84x tokens and 1.39x tool calls against a 1.20x cap.

The build's owner, having seen those numbers, decided to ship anyway on the grounds that the
quality margin justifies the cost. Recorded here rather than applied silently:

- **The verdict is not changed.** `decide.json` still reads ITERATE and is not edited. The rule was
  not reinterpreted, the threshold was not moved, and `decide.py` was not re-run against a widened
  cap. A rule rewritten after the numbers are visible is not a rule.
- **This is an override, not a pass.** The skill ships carrying a known, measured cost of roughly
  1.8x the tokens of the bare arm on every invocation.
- **Authority:** the project owner, who is the amendment authority named at registration. That is
  exactly the person this instrument exists to bind, and binding them means making the override
  visible, not preventing it.
- **What justified it:** with 93.8% of expectations met against the incumbent's 66.7% and the bare
  arm's 47.1%, wins on correctness and shape surviving every repeat, and zero regressions.

**What this costs the record:** the cost clause has now been overridden once. If it is overridden
again, it is not a threshold, it is a formality, and the honest move at that point is to raise the
cap in the contract and say why — before the next build, not after it.
