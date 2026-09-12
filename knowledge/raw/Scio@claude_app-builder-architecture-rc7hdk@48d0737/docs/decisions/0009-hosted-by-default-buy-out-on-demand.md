# ADR-0009 · Hosted in Scio's ecosystem by default; the code can be bought out, as a key transfer

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** D (ship) per ADR-0005; commercial model
**Supersedes / relates to:** amends ADR-0006 (Slice 1's delivery); relates to ADR-0002; predecessor ADR-0009 (code lives in git) and ADR-0018 (Ship, never settled)

## Context

The user's stated plan (2026-09-02): a customer can stay entirely inside Scio's ecosystem — hosting,
domain, backend, operations — and can also *buy out* the code. The reviews recorded what Lovable is
far ahead on and said not to chase parity first: hosting and custom domains, managed backend, GitHub
sync, payments, connectors (`REVIEWS-WHAT-WE-MISSED.md` §5). The 2026 comparisons' test for a
production-ready builder is *can you export it and keep building without the platform*
(`REVIEW-FRESH-EYES-2026-09-02.md` §5). Predecessor ADR-0009 already puts every app's code in git.

The tension: a hosted-first product is tempted to make export a migration project, which is what
makes "you own it" untrue in week three. A repo-first product is tempted to skip hosting, which is
the buyer's default need.

## Decision

Every build produces a complete git repository from the first build, held in Scio's ecosystem by
default and deployed there. **Buy-out is a key transfer, not a migration**: the repository, its
history, its evidence and its level-3 talents (ADR-0008) move to the customer's own GitHub and
infrastructure as they are, and the deploy is re-pointed. Nothing in the repository depends on
Scio at runtime; anything that would — a Scio SDK, a Scio-hosted service the app calls — is a
build-time refusal, not a later cleanup. Slice 1 (ADR-0006) delivers the hosted form with the
transfer button present and tested; custom domains, managed backend operations and the rest of the
parity list come in later slices, in the order the deferral log records.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Repo in the customer's GitHub from build one (this review's cold position 6) | Right about the artefact, wrong about the default: the buyer confirmed as a founder wants it hosted first and owned when it matters |
| Hosted only, export later "when asked" | Export becomes a migration and the ownership promise fails the week-three test |
| Two code shapes, a hosted one and an exportable one | Two shapes drift; the buy-out then buys the worse one |

## Consequences

**What this buys.** One artefact, one shape, two commercial doors. The buy-out is credible because
it is mechanically trivial, and that credibility is the differentiator against the tools whose
export exists but does not survive.

**What it costs.** Scio runs hosting and operations from Slice 1; the parity list is real work and
is sequenced, not skipped. A build-time check that the app has no runtime dependency on Scio.

**What it forecloses.** Lock-in by dependency. Revenue from the hosted tier has to come from
operating the app well, not from making leaving expensive.

## How we will know it was wrong

A buy-out takes more than a working day of anyone's time, or a transferred app stops working because
of something it needed from Scio; or hosted customers churn to self-hosting at a rate that says the
hosted tier delivers nothing over the repository.
