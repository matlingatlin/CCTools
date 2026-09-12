# ADR-0003 · Scio is written in one language, TypeScript, end to end

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** cross-cutting
**Supersedes / relates to:** replaces predecessor ADR-0006 (NestJS backend + separate Python FastAPI engine) for the rebuild

## Context

The predecessor is a Python engine behind a TypeScript API and app, talking through serialised
DTOs. Measured 2026-08-26 on its code graph: 9,857 edges within a language and **zero** across
the seam. An impact query on a real commit predicted 2 of the 8 files that changed; the other six
propagated across the boundary (`.claude/skills/run/SKILL.md` §2). The seam is where integration
defects lived and where every retrieval tool goes blind.

The generated application stack is TypeScript (predecessor ADR-0011). The Claude Agent SDK ships
in TypeScript and Python (hosting doc fetched 2026-09-02). The Python worth keeping is small and
total: the criteria model, `Contract`, the eleven validation rules, `verify_instrumentation`, the
console classifier, the interaction-script derivation. Each ships with tests named as behaviour
claims, which are an oracle for a port.

## Decision

Scio's own code — API, engine, web app, gates, and the build-loop wrapper over the harness — is
TypeScript in one repository. The Python components carried forward are ported with their test
suites translated first and used as the acceptance oracle; a ported module is done when the
translated tests pass and one of them has been shown to fail. Framework choices inside TypeScript
are separate ADRs made in the architecture pass with a dated scan.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Keep Python engine + TypeScript API (do nothing) | Reinstates the seam the tools cannot see across and that hid the defects |
| Python end to end | The generated stack, the design window's browser bridge and the product UI are TypeScript; the port would be three times larger in the other direction |
| Keep two languages, add cross-language graph tooling | Solves observability of the seam, not the seam; a scan for such tooling can reopen this if the port proves costlier than measured |

## Consequences

**What this buys.** One code graph that sees the whole system; one test runner; one dependency
surface for `source-grounded-implementation`; shared types between generator and generated app.

**What it costs.** The port. Roughly the engine's Solid list (see `docs/REVIEW-FRESH-EYES-2026-09-02.md` §4),
which is the smallest part of 9,393 engine lines. Python-only tooling used by the predecessor
(pglite harness under `library/verification/`) is replaced, not ported.

**What it forecloses.** Reusing Python ML or data libraries inside the engine without a service
boundary.

## How we will know it was wrong

The port of any Solid component takes more than a week, or a translated test cannot be made to
fail in TypeScript for a reason that was real in Python.
