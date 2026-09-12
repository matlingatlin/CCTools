# ADR-0006 · One vertical slice before any breadth: "just build it" ships first

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** cross-cutting (sequencing)
**Supersedes / relates to:** predecessor ADR-0017 (promotion), ADR-0018 (Ship/Refine/Settings, never settled); relates to ADR-0005

## Context

The predecessor is 22,990 source lines with five placeholder routes, one of which (`/live`,
"Refine") carries the entire value proposition of its Level 1 path — *just build it, I'll shape it
after*. Its matchable library catalog is one entry, its two most valuable gates are opt-in, nothing
runs the generated app's own tests, and deployment throws 501
(`docs/as-built/REVIEWS-WHAT-WE-MISSED.md` §1, §3). The reviews' own sentence: *"The library is an
amplifier, not the precondition for proving the core. The core loop must work well even when
everything has to be generated."* `OPERATING-MODEL.md` §4 names this: it was built broadly.

## Decision

The rebuild is sequenced as three slices and the next slice does not start until the previous one
has produced its artefact with a real user.

1. **Slice 1 — just build it.** Intake → contract → build with every gate on → evidence report →
   a complete repository with CI green, hosted and deployed in Scio's ecosystem, with the buy-out
   transfer present and tested (ADR-0009). One app kind. Everything
   generated; no library, no design window, no curation, no settings beyond the allowance.
2. **Slice 2 — shaping.** The design window as a loop over a shipped version: mark → describe →
   impact analysis → surgical regeneration → promote, carrying the predecessor's Solid F parts.
3. **Slice 3 — the library.** Contribution from every successful build including promotions,
   generalise, re-verify against an unseen entity, contract-match before generating, entries
   exported as registry-standard items with `Contract` in `meta`.

Cross-cutting concerns — tenancy, auth, tokens, spend, telemetry — are **designed** in Slice 1's
architecture pass and **built** only as far as Slice 1 exercises them; each deferral is written
into this ADR's log so it stays a decision.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Port all seven layers in parallel | The predecessor's failure mode, repeated with better tooling |
| Design window first (the "flagship loop") | It is the most code for the least validation of the core, and it needs a shipped version to loop over |
| Library first, to make builds cheap | A library of one entry made nothing cheap; contributions come from builds that do not yet exist |

## Consequences

**What this buys.** A developer can be handed a repository at the end of Slice 1 and asked the
only question that matters. Every later slice has a real artefact to measure against.

**What it costs.** Slice 1 generates everything, so its builds are slower and dearer than the
end state; the evidence report will show that honestly.

**What it forecloses.** Nothing structurally; it forecloses *starting* the amplifiers early.

## How we will know it was wrong

Slice 1 cannot reach a developer-acceptable repository without a library, which would mean
generation quality rather than sequencing is the constraint — in which case the Playbook and the
gates, not the library, are the next work.

## Deferral log

| Date | Deferred from Slice 1 | Reason | Returns in |
|---|---|---|---|
| 2026-09-02 | design window, library, curation surface, settings page | see decision | Slices 2–3 |
