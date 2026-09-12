---
name: behavioral-spec-mining
description: "Use when reverse-engineering a formal behavioral spec from existing or brownfield code that shipped without one — extracting Requirements, Invariants, and WHEN→THEN scenarios (happy path, edge cases, error handling) before a refactor, rewrite, migration, or characterization-test suite. Triggers: 'what is this code supposed to do', 'mine/recover/reconstruct the spec', 'document actual behavior', 'derive acceptance criteria from legacy code', 'spec out this module before I change it'. Mines behavior by sampling entry points and expanding under a token budget. NOT for regenerating structural codemaps (use update-codemaps) and NOT for comprehension notes on prose or a single file (use deep-reading)."
---

# Behavioral Spec Mining

Recover a formal, testable spec from code that never had one — Requirements and
Invariants plus WHEN→THEN scenarios — so a refactor, rewrite, or test suite has a
target. Method comes from sampling representative code, then expanding, within a
declared token budget. The spec captures *actual* behavior, not intended behavior.

## When to use

Use for brownfield/legacy code slated for change where no spec exists and behavior
must be pinned down first. Use NOT when: structure/architecture is the question
(update-codemaps); you only need reading comprehension of one file or a document
(deep-reading); the code is greenfield and the spec should be authored forward.

## Steps

1. **Set the budget and scope.** Name the target (module/service/dir) and a token
   budget for the mining pass (e.g. 40k). Estimate corpus size (code ≈ chars/4). If
   the corpus exceeds ~40% of budget, you MUST sample — do not read everything.

2. **Enumerate entry points.** List the surfaces where behavior is observable:
   public functions, API routes, event handlers, CLI commands, exported classes.
   These become the units you mine. Rank by apparent importance and branching.

3. **Sample, don't exhaust.** Read the top-ranked entry points in full plus their
   immediate callees. For the rest, read signatures and skim bodies. Track spent
   budget; stop reading when the sample stops yielding new behaviors.

4. **Extract Requirements and Invariants.** For each sampled unit, write:
   - **Requirements** — capabilities the code provides ("The system SHALL …").
   - **Invariants** — conditions always held (validation, ordering, idempotency,
     auth checks, conservation of a quantity). Pull these from guard clauses,
     asserts, and error branches — they are the richest invariant source.

5. **Expand into WHEN→THEN scenarios.** For each Requirement, derive scenarios:
   `WHEN <precondition/input> THEN <observable outcome>`. Cover the happy path,
   at least one edge case, and each error/exception branch you saw. Mark any THEN
   you inferred but did not confirm in code as `(unverified)`.

6. **Cross-check and dedupe.** Merge overlapping scenarios; flag contradictions
   between what code does and any comments/names that claim otherwise — record the
   code's actual behavior and note the discrepancy.

7. **Emit the spec.** Output plain Markdown: one section per entry point with its
   Requirements, Invariants, and a numbered WHEN→THEN list. Close with a **Coverage**
   note — what fraction of entry points were fully mined vs. skimmed vs. skipped, and
   the budget spent — so the reader knows the blind spots.

## Rules

- Budget is a hard ceiling. Declare it up front; report spend at the end. Sampling
  with honest coverage beats exhaustive reading that blows the budget.
- Describe behavior that IS, not behavior that SHOULD BE. Never invent Requirements
  the code does not exhibit; mark every inferred outcome `(unverified)`.
- Invariants come from error/guard branches first — that is where real contracts hide.
- Every Requirement gets at least one WHEN→THEN, including its failure mode.
- Output is plain Markdown only. Do not emit OpenSpec, Gherkin, or any tool-specific
  format, and do not scaffold test files — mining produces the spec, nothing else.
- Method only: no network calls, no CLI invocation, no auto-run hooks. Read and reason.
