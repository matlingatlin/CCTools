# ADR-0007 · Evidence is the product surface: every gate on by default, every result rendered

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** C (build) and D (ship), per ADR-0005
**Supersedes / relates to:** predecessor ADR-0013 (validation before building — decided, never wired); relates to ADR-0002

## Context

Across five predecessor layers the same habit recurs: an honest signal is computed and then
dropped before it reaches anyone — `validate_plan`'s nine rule identifiers read by nothing,
`checks_passed` typed and transmitted and never rendered, `compiles` carried by hand through four
hops, `/usage/allowance` with no consumer, five curation endpoints with no surface
(`ARCHITECTURE-AS-BUILT.md` *The pattern that matters most*). The two most valuable gates — does it
work with real data, can a guest read another's row — run only under `SCIO_VERIFY_DATA=1`.
Nothing runs the generated app's own tests or `next build`. A written spec for the reveal names
nine items; the reveal shows four lists of ids (`REVIEWS-WHAT-WE-MISSED.md` §3).

Lovable's publish gate — a scan on every publish with a workspace policy to block on critical
findings — is the competitive floor (`docs/next/LAYER-E-BUILD.md` §4.5, scanned 2026-08-26).

## Decision

Every gate runs on every build; there is no opt-in verification. A gate that cannot run reports
`blocked` or `unjudged` with the reason, and never reads as clean. Plan validation is consumed: a
plan with an error-severity violation does not build. The evidence report is a first-class,
persistent artefact rendered in full: requirements met and unmet · tests and browser flows run,
including the generated app's own suite and its production build · security checks · changed
packages and files · verified-unchanged surface · model and build cost including B, C and
contribution spend · build time · remaining risks · version id and export. Findings persist as a
view the user can return to, and a workspace policy decides block / warn / allow on severity.
Status vocabulary is `passed / needs_look / failed / blocked` with `unjudged` first-class, per
`gate-verdicts`; a checker returns what it examined, per `validation-evidence`.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Keep the expensive gates opt-in to control cost | Cost is bounded by `spend-ceilings`; an opt-in gate makes the flagship claim untrue by default |
| A single score ("security 86%") instead of the nine items | A number attached to a judgement hides which check did not run; the scored view is a *summary of* the nine, never a replacement |
| Render only failures | The verified-unchanged surface and the risks that remain are what a developer reads first |

## Consequences

**What this buys.** The differentiator the predecessor half-built becomes visible: it already
verifies more than any competitor; it now also tells.

**What it costs.** Every build pays for a browser round trip and the generated app's own test run.
Slice 1 builds are slower for it, and the report says so.

**What it forecloses.** Shipping a build whose status is a green tick with nothing behind it.

## How we will know it was wrong

Users hide the evidence report, or a developer judging a delivered repository reports that the
report told them nothing they did not learn faster from the code.
