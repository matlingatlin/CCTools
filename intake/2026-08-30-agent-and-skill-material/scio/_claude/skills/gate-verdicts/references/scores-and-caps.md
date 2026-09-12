# D3 · A number, or a verdict — and what caps a number

Load this when a gate is about to return a score, a rating, or a weighted composite.

## First, decide whether a number is the right return type at all

From `docs/mined/PASS2-ECC-RULES-COMMANDS.md:697`, distilled from comparing two commands in the same
repository:

> Use a **score** only where a gradient is needed — convergence, ranking, "is this getting better".
> Use a **verdict + checklist** for a decision.

A score attached to a decision has to be thresholded, and the threshold is then the real gate while
the arithmetic that produced the number is unauditable. Two of the mined repositories ship a
weighted-composite rubric; **both are left**, and one of them is contradicted by its own author's
rubric-design skill:

> *"weights guide synthesis emphasis, not a single blended score (avoid a false composite)"*
> — `benchmark-methodology`, quoted at `docs/mined/PASS2-ECC-SKILLS.md:686`

## Score caps: the arithmetic of "judgement may not overrule a check"

From `production-audit`, read at `docs/mined/PASS2-ECC-SKILLS.md:369`:

> Use scores to force prioritization, not to imply mathematical certainty. … **Cap the score at
> `69`** if any of these are true: authentication or authorization is missing on sensitive data;
> payment or fulfillment webhooks are not idempotent; required migrations cannot be run safely;
> secrets are exposed in client bundles, logs, or committed files; there is no rollback path.
> **Cap at `84`** if CI is not green or the launch-critical path was not tested end to end.

**Binary deterministic conditions set a ceiling; the judgement may only move below it.**

This is the missing arithmetic of a rule this repository already states and cannot currently
enforce: *proposals may add evidence channels; they may not convert a deterministic channel into a
judgement* (`docs/next/LAYER-E-BUILD.md` §1). Without a cap, "the model rated it 9" and "the linter
found a hardcoded secret" are two numbers in a report with no defined relationship. With one, the
secret sets the ceiling and the 9 is unreachable.

The ceiling conditions have to be **binary and deterministic** — that is what makes the cap
auditable. `app-design` §5's six deterministic checks are ready-made ceilings; so are the seven
deterministic validation agents at `validation.py:404`.

## Two anti-patterns from the same source, worth naming

- *"treating green CI as production readiness"*
- *"producing a score without naming the evidence checked"*

## Confidence, when a gate reports one

From `cso` and `review`, `docs/mined/PASS2-GSTACK-SKILLS.md:699`: one engine, two thresholds by
invocation, and a display policy in bands. The rule that matters is not the numbers:

**Low-confidence findings are labelled and demoted, never deleted.** A finding the gate is unsure
about is information; discarding it is a silent decision made by the gate on the reader's behalf.

Paired with it, from `review` / `autoplan` at `:702`: two independent gates agreeing may raise
confidence **explicitly**, and **a missing voice is N/A, never agreement**. An absent reviewer that
counts as consensus is how a two-reviewer gate quietly becomes a one-reviewer gate.

## What this does not settle

Whether *our* gates should return numbers at all. Today `checks_passed` is computed, typed,
transmitted and displayed nowhere, while the reveal shows four status lists instead
(`docs/as-built/LAYER-E-BUILD.md` §6). Either wire it or stop claiming it — and that is an ADR,
not a procedure.
