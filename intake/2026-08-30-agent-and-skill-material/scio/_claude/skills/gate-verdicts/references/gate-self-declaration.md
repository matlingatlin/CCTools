# D5 · What a gate says about itself

Load this when writing a new gate, or when auditing whether an existing one is a guardrail or a
decoration.

## 1 · Enforcement point, or not

The most honest sentence in the mined corpus, from `ios-clean`
(`docs/mined/PASS2-GSTACK-SKILLS.md:129`):

> This skill is a **convenience flow**, not a safety mechanism. The structural guard against
> shipping DebugBridge in Release is in `Package.swift.template` … plus the CI invariant test that
> runs `swift build -c release` and asserts the DebugBridge symbol is absent.

**Every gate carries this line or its opposite** — either *"this is the enforcement point"* or
*"the enforcement point is X"*. Ambiguity here is exactly how a guardrail becomes a decoration:
three teams each assume one of the other two is the one that would have caught it.

This repository has one gate that already does it, in the negative:
`execution/untrusted.py` says *"the layer that matters most is not this file"*.

## 2 · Non-scope, stated positively

The same source ships two more sections worth copying as a template: **"What it does NOT touch"**
and **"Reversibility"** —

> *"Every Edit + delete is a git operation… This skill never force-pushes, never amends, never
> deletes the SPM cache — those are user choices."*

For a build gate the non-scope list is what stops a later reader assuming coverage that was never
claimed. *Nothing runs the generated app's tests* is a true sentence about this repository, and it
belongs in the gate's file, not only in a review document.

## 3 · The error contract

From `agent-harness-construction`, `docs/mined/PASS2-ECC-SKILLS.md:443`. Every response carries
`status: success|warning|error` · `summary` · `next_actions` · `artifacts`, and:

> *"for every error path, include: root cause hint · safe retry instruction · explicit stop
> condition."*

The **stop condition per gate** is the part this repository lacks and the reason it matters is
mechanical: our gates hand the repair a `problems` list with no retry instruction and no stop
condition, so the stop condition ended up hard-coded globally as a pass count. A per-gate stop
condition is what makes a plateau detector or an N-consecutive completion signal expressible at
all (see `build-loop-stops`).

## 4 · The suppression list

From `review/checklist.md`, `docs/mined/PASS2-GSTACK-SKILLS.md:693`: **a suppression list ships
alongside every checklist, or the checklist is ignored within a month.**

A checklist with no way to say "not this one, here, for this reason" gets satisfied by ritual. The
companion rule, from the adaptive-gating finding at `:700`: checks may be pruned on measured hit
rate — **except insurance checks, which are exempted by name**. Pruning without a named exemption
list deletes exactly the checks that fire rarely because they are working.

*(Whether to prune at all is an ADR: it needs the hit-rate measurement first.)*

## 5 · Reports do not pad

From `make-interfaces-feel-better`, `docs/mined/PASS2-ECC-SKILLS.md:680`:

> *"Omit principles you checked but did not change."*

A status report padded with no-ops trains its reader to skim, and a reader who skims does not see
the one line that mattered. This repository's honest status and Layer F's change reports both pad.

## 6 · A degraded run discloses, in its output

Two independent statements of the same rule:

- `retro`, `docs/mined/PASS2-GSTACK-SKILLS.md:238` — every skip path proceeds *"with the cited
  reason on a single stderr line so the narrative carries the disclosure ('offline run, window not
  freshness-verified') rather than silently misreporting."*
- `repomix`, `docs/mined/PASS2-FOUR-REPOS.md:545` — degrade best-effort, and **publish the residual
  failure, its bound, and why the bound is acceptable**.

The bound is the part that is usually missing. "Best effort" with no published residual is
indistinguishable from "worked".

## 7 · What the judge is allowed to see

From `council`, `docs/mined/PASS2-ECC-SKILLS.md:428`:

> The … external voices should be launched as fresh subagents with **only the question and relevant
> context, not the full ongoing conversation. That is the anti-anchoring mechanism.**

For a build gate: **the reviewer receives the artefact and the acceptance criterion, and nothing
else.** Not the build transcript, not the previous attempt's reasoning, not the repair's excuse. An
evaluator handed the transcript is anchored by construction, and this is one checkable constraint
on how the reviewer's context is assembled — strictly stronger than "the reviewer is a different
call".

## The audit, as a grep

All of §1–§6 are greppable. A lint over gate files that asserts each one contains an
enforcement-point line, a non-scope list, and a stop condition on every error path is a few dozen
lines and would be the first thing in this repository that checks a gate's *file* rather than its
*output*.
