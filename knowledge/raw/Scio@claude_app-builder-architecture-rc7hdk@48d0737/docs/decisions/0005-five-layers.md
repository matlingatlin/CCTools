# ADR-0005 · Five layers, not seven — drawn along the seams the predecessor accreted across

**Status:** Proposed — to be tested by the `architecture` pass before acceptance
**Date:** 2026-09-02
**Layer:** cross-cutting
**Supersedes / relates to:** predecessor ADR-0012, ADR-0013, ADR-0014 (layer boundaries); relates to ADR-0004

## Context

The predecessor has seven layers because it has seven directories. `ARCHITECTURE-AS-BUILT.md`
*Where the missing architect pass shows* lists the seams: granularity fixed in C and repaired by
chunking in E; `builder/file_plan.py` defining "producible" and imported upward by C's validator;
`library/verification/` filed under D though it is build harness; `run_layer_c` doing four jobs;
deployment a module whose only behaviour is 501. The edge counts agree: D → E is the heaviest
edge in the graph (84), F → E (70) and F → G (73) show the design window as a client of build and
platform rather than a peer.

`run` §3 says the count is not to be inherited and not to be changed casually.

## Decision

The rebuild has five layers, each an ADR with its reason:

| Layer | Owns | Predecessor material |
|---|---|---|
| **A · Intake** | conversation → typed, provenance-bearing spec; the buildable-enough gate | A, unchanged in scope |
| **B · Contract** | spec → architecture → ordered, contract-bearing packages, as **one derivation validated once**, whose validation is consumed | B + C |
| **C · Build** | match against the library, generate what did not match, gate, produce evidence | E, with D as a step inside it |
| **D · Ship** | evidence report → repository the user owns → deploy → the design window as a loop over a shipped version → promote | F + deployment + reveal |
| **E · Platform** | tenancy proven by RLS, identity behind one interface, spend and allowance, streams, jobs | G |

The `design-rule-hierarchy` test applies: dependencies point upward only, A ← B ← C ← D, all on E.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Inherit seven | Inherits the seams listed above, which is where the predecessor's defects sit |
| Four (fold Ship into Build) | Building and shipping have different stop rules and different customers; the evidence report is a product surface, not a build artefact |
| Keep D as a layer | The library is "an amplifier, not the precondition" (reviews); a layer whose matchable catalog is one entry should not gate the shape of the system |

## Consequences

**What this buys.** Validation has one owner and a consumer. Granularity is decided where the
file plan is known. The library cannot be built before the core loop, because it is not a layer
until Slice 3.

**What it costs.** B is the largest layer and needs the second architecture pass (`run` step 3)
most; the contract-bearing package model of predecessor ADR-0013 must survive the merge intact.

**What it forecloses.** Selling the library as a separate product; it is a step.

## How we will know it was wrong

B's internal design cannot be drawn without a seam that looks exactly like the old B/C boundary,
or the reflexion model shows Build reaching into Contract for anything but interfaces.
