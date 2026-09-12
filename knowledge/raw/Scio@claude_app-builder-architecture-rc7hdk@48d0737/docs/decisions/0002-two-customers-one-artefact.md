# ADR-0002 · Two customers, one artefact: the buyer cannot code, the judge is a developer

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** cross-cutting (governs A and the evidence surface in D/E)
**Supersedes / relates to:** relates to predecessor ADR-0001 (wedge: founders and small teams) — confirmed by the user 2026-09-02, not superseded

## Context

Predecessor ADR-0001 defined the wedge as *founders and small teams building software they intend
to run and grow* and the differentiator as *developer-grade output*. The user's brief for this
rebuild says *someone who cannot write software describes what they want*, and that the output
must be *professional enough that developers are impressed*. `docs/as-built/01-DECISIONS.md`
records that this tension sits upstream of intake: the schema asks for `entities` and
`data_ownership_sensitivity`, natural for a founder and not for a restaurant owner.

The 2026 comparisons of Lovable, Bolt, v0, Base44, Replit and Totalum judge tools on what happens
in week three: schema change, export, price. None of them is judged on evidence. The predecessor
computes more verification than any of them and renders four lists of ids
(`docs/next/LAYER-E-BUILD.md` §4.5).

## Decision

Scio has two customers and one artefact. **The buyer** is a founder or app-builder who cannot
write software but knows what an app is — the user confirmed this wedge on 2026-09-02, so
predecessor ADR-0001 stands. Their vocabulary governs intake: a question may presuppose *product*
concepts (users, roles, the things the app keeps track of, who may see what) and may never
presuppose *implementation* concepts (schema, table, row-level security, token). The predecessor's
six core fields are therefore defensible as aimed; the criticism that `entities` is mis-aimed is
withdrawn, and what remains is wording and examples. **The judge** is a developer who did not
write the code; their standard governs output, so every build ships as a repository with
structure, honest types, tests shown able to fail, a proven tenancy model, no placeholders, CI
green, and an evidence report a developer can audit. A feature that serves neither customer is
out of scope.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Widen the buyer to anyone who cannot code | Rejected by the user 2026-09-02; it would force intake to elicit a data model from someone with no product vocabulary, the hardest version of Layer A for no confirmed demand |
| Target developers directly (a Cursor-class tool) | The buyer would be able to code; the product's reason to exist disappears |
| Target non-coders only, judge output by "it runs" | That is Lovable's class and the comparisons put it in the first-48-hours category |

## Consequences

**What this buys.** A test for every scope argument: which customer does this serve, and how would
they see it. Intake and evidence get their standards from different people, which is why they
have different shapes.

**What it costs.** Intake must hold the product/implementation line in every question; the
additive app-kind detection in `docs/next/LAYER-A-INTAKE.md` still applies, but as steering, not
as a vocabulary rescue.

**What it forecloses.** A quick win by shipping a prompt box over a code generator.

## How we will know it was wrong

A developer opens three consecutive delivered repositories and rates none of them as something
they would have merged; or buyers abandon intake before the gate at a rate the replay harness
cannot bring down with vocabulary changes alone.
