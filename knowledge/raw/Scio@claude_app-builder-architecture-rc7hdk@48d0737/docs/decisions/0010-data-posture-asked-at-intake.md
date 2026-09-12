# ADR-0010 · Whether data is stored, how sensitive it is, and where, are asked at intake and drive the build

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** A (intake), C (build), D (ship), E (platform)
**Supersedes / relates to:** extends predecessor ADR-0010 (six core fields incl. `data_ownership_sensitivity`); constrains ADR-0004 (sandbox provider) and ADR-0008 (skill selection)

## Context

The user's instruction (2026-09-02): in the chat, the buyer is asked whether the app stores data, at
what sensitivity level, and in which region, and the build makes choices from those answers. The
predecessor's intake already carries `data_ownership_sensitivity` as a core field and `tenant-isolation`
carries sensitivity labels that survive into the generated database (BC-A13). Region and *whether to
store at all* are not asked. This review's earlier question — whether ZDR or data residency applies to
Scio — was the wrong question: it applies per app, and the buyer answers it.

## Decision

Intake asks three questions in the buyer's product vocabulary (ADR-0002): **does the app keep any
data about people or business**, **how sensitive is it** (a closed scale with examples, never a
compliance term the buyer must know), and **where must it live** (a region list, with "no
preference" allowed and recorded as such). The answers are core fields with provenance, and each
downstream layer consumes them deterministically: skill selection (`sensitive-data`, `tenancy-rls`
per ADR-0008), the generated database's region and its sensitivity labels, the hosted deployment's
region (ADR-0009), and **the build sandbox's region and retention** — a build for a region-bound app
runs in that region or is refused with the reason. Region availability therefore joins ADR-0004's
four numbers as the fifth the sandbox provider must answer. A build whose region cannot be honoured
is `blocked`, never silently placed elsewhere.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| One global posture for Scio (ZDR on or off, one region) | Forces every buyer into the strictest or the loosest setting; wrong for most |
| Ask after the build, at ship time | The sandbox, the schema and the skill set have already been chosen without it |
| Infer sensitivity from the entities | Inference may be *shown* but never *acted on* (`provenance-record`); this drives placement |

## Consequences

**What this buys.** Compliance-shaped questions become product questions the buyer can answer, and
their answers become checkable build inputs. Managed Agents' ZDR ineligibility stops being a
platform verdict and becomes a per-build routing rule.

**What it costs.** Region-aware infrastructure from Slice 1 for the sandbox, the database and the
deploy; a refusal path when a region cannot be served.

**What it forecloses.** A single-region launch that quietly serves region-bound apps elsewhere.

## How we will know it was wrong

Buyers answer "no preference" so uniformly that the question is noise; or a region answer is
recorded and a build still places data outside it, which the cross-region assertion in the
evidence report must catch.
