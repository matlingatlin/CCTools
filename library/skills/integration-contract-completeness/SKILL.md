---
name: integration-contract-completeness
description: "Use when a patch touches one side of a symmetric or multi-variant contract and you must decide whether it should cover the rest — added a parse path but not the matching dump/serialize, handled streaming but not non-streaming (or sync but not async), a new enum/field/spec variant wired through one branch only, one provider/version/format of several. Sweeps the contract's mirror sides and variant axes, then reports each as covered, missing, or deliberately-narrow with a reason. Triggers: 'did I miss the other half', 'does this need the reverse path too', 'is this change symmetric', 'audit the patch for completeness', 'what else should this touch', encode-without-decode, request-without-response, read-without-write, plus the tests/docs/prior-ADR obligations each gap implies. NOT general test-coverage thresholds (use test-coverage), NOT running commands to confirm success claims (use verification-before-completion), NOT recovering a spec from scratch (use behavioral-spec-mining)."
---

# Integration Contract Completeness

A narrow patch is right only when its silence on the other sides of the contract is deliberate. This makes that call explicit: enumerate the mirror sides and variant axes a change implies, then mark each covered, missing, or intentionally-narrow-with-a-reason — never silently skipped.

## When to use
- A patch touches one direction of a paired operation: parse/dump, encode/decode, serialize/deserialize, read/write, request/response, push/pull, migrate-up/down.
- A change lands on one of several parallel modes: streaming vs non-streaming, sync vs async, batch vs single.
- A new enum value, field, error code, or spec/format/provider/version variant is wired through some branches but maybe not all.
- Someone asks "is this complete / symmetric / did I miss anything" about a diff.

**When NOT:** measuring coverage to a percentage threshold (test-coverage); running the suite to back a "done" claim (verification-before-completion); deriving a spec where none exists (behavioral-spec-mining); pure structural mapping (update-codemaps).

## Steps
1. **Read the patch.** Identify the exact operation(s) it added or changed and the contract they belong to. Name the direction/mode/variant it lives on.
2. **Enumerate the axes.** For that contract, list every mirror side and variant that a complete change would touch:
   - Direction: does an added encode imply a decode (and a roundtrip that returns the input)?
   - Mode: streaming ↔ non-streaming, sync ↔ async, batch ↔ single.
   - Variants: every enum value, spec version, format, provider, or config branch the codebase already handles here.
   - Obligations: tests for each new path, docs/schema/changelog, and any prior ADR or decision this touches.
3. **Grep for the peers.** For each axis, search the codebase for where its siblings are handled (the existing dump next to the new parse, the other providers' branches). Absence of a peer is itself a finding.
4. **Classify each axis** as: **covered** (patch handles it), **missing** (contract demands it, patch omits it — a defect), or **deliberately-narrow** (out of scope for a stated, defensible reason).
5. **Demand a reason for every narrow.** "Not needed" is not a reason. Acceptable: the reverse path is generated, the variant is unreachable, a follow-up is tracked. Record it.
6. **Report** a table: axis → status → evidence/reason. Lead with the missing rows. If all narrows are justified, say the patch is correctly scoped and why.

## Rules
- Method only. No network or CLI side effects beyond read-only Read/Grep/Glob over the repo.
- A roundtrip is the strongest check: if the patch adds one direction, the pass is a test that goes input → new path → mirror path → equals input. Note when it is absent.
- Prefer the codebase's own precedent: the sibling branches already present define which variants a complete change must cover.
- Narrow can be the correct answer. The output is a justified decision, not a mandate to widen scope.
- Every new code path implies a test and a doc/changelog touch — count those as axes, not afterthoughts.
- Do not invent axes the contract does not have; over-widening is its own failure.
