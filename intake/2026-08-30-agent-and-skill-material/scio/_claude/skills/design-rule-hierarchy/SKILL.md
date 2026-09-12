---
name: design-rule-hierarchy
layer: C
phase: build-time
status: written
description: Check a decomposition against Design Rule Hierarchy and Design Structure Matrix theory — upward-only dependencies between layers, mutual independence within a layer, and propagation cost as the number a granularity change must move. Use when deciding package boundaries or granularity, when computing which packages may be built in parallel, when someone claims a decomposition is modular, or when arguing whether splitting a package is an improvement. Deterministic graph analysis; no model call.
---

# design-rule-hierarchy

## 1 · Source

Two connected bodies of work, both empirical rather than speculative.

**Design rules and modularity.** Carliss Y. Baldwin & Kim B. Clark, *Design Rules, Vol. 1: The
Power of Modularity*, MIT Press, 2000. Retrospective: *"Design rules: past and future"*,
*Industrial and Corporate Change* 32(1), 2023 —
<https://academic.oup.com/icc/article/32/1/11/6868533>

**Propagation cost, measured on real software.** Alan MacCormack, John Rusnak & Carliss Baldwin,
*Exploring the Duality Between Product and Organizational Architectures*, HBS Working Paper
08-038 — <https://www.hbs.edu/ris/download.aspx?name=08-038.pdf>; and *The Structure and Value
of Modularity in Software Design*.

**Design Rule Hierarchy (DRH) as an algorithm.** Yuanfang Cai and colleagues' work clustering
files into a layered hierarchy where lower layers depend only on higher ones and same-layer
modules are mutually independent — see *Recovery of Architecture Module Views using an Optimized
Algorithm Based on Design Structure Matrices*,
[1709.07538](https://arxiv.org/pdf/1709.07538), and *A Longitudinal Study of Identifying and
Paying Down Architectural Debt*, [1811.12904](https://arxiv.org/pdf/1811.12904).

**Related, for the granularity score:** Spiros Mancoridis et al., *Using Automatic Clustering to
Produce High-Level System Organizations of Source Code* (Bunch / Modularization Quality), ICSM
1998.

Read at abstract-to-method level. Not reproduced.

## 2 · Method, in the form we use it

**The claim.** A decomposition is a Design Rule Hierarchy when:

1. it can be partitioned into ordered **layers**;
2. every dependency points **upward only** (a lower layer may depend on a higher one, never the
   reverse, and never sideways within a layer);
3. within a layer, modules are **mutually independent**.

Property 3 is what makes a layer's members substitutable, independently testable, and — the
part Scio cares about — **safely buildable in parallel**.

**Scio already produces this shape.** `layerc/decompose.py` emits foundation → schema/tokens →
auth → features/connectors, with dependencies declared per package. What it does not do is
*check* it. Three deterministic computations over `BuildPlan.graph`, all free:

### (a) Layering — the topological levels

Not a flat order. Kahn's algorithm already computes `ready = sorted(pid for pid, deps in
remaining.items() if not deps)` at `decompose.py:429` and then flattens it. Each `ready` set
**is** a layer. Return the levels.

### (b) Within-layer independence — the antichain

A set of nodes is an **antichain** when no path connects any two of them. The maximum antichain
size is the DAG's **width** — the standard measure of how much parallelism a task graph admits.

`parallelizable` should mean *"in an antichain with at least one sibling"*, computed by
reachability over `plan.graph`. Today `mark_parallelizable` (`decompose.py:442`) checks
`len(group) > 1` and flags everything — right by construction, unverified, and about to be
routed on.

### (c) Propagation cost — the number a granularity change must move

Build the boolean reachability matrix over `plan.graph` (transitive closure; for a plan of
5–20 packages, Warshall is instant). Then:

```
propagation_cost = (number of reachable ordered pairs) / n²
```

MacCormack et al.'s definition: the fraction of the system that can be affected by a change to
any element. Lower is more modular.

**How to use it.** When someone proposes changing granularity — splitting a feature package
(Layer C §3.2), merging connectors, adding a test package — compute propagation cost before and
after. A split that raises it is making the plan *less* modular no matter how good the
motivation sounds. This turns "is this decomposition better?" from an opinion into a number.

**Modularization Quality (MQ)** is the alternative score: intra-cluster cohesion minus
inter-cluster coupling, one number over a partition, from Bunch. Use it when comparing two
*different partitions of the same graph*; use propagation cost when comparing the *same
partition before and after a structural change*. They answer different questions and the wrong
one is easy to reach for.

### (d) The write-surface test — what makes (b) operational

Added 2026-08-26 from `docs/mined/PASS2-ECC-SKILLS.md` §2.9 (`parallel-execution-optimizer`):

> *"Only run lanes in parallel when their write surfaces do not collide."*

An antichain is **necessary** for two packages to build together and it is not **sufficient** — two
packages with no dependency path between them can still plan to write the same file. Scio can decide
the sufficient half deterministically, because `planned_files()` (`builder/file_plan.py:42`) computes
each package's paths:

> **Two packages may build in parallel exactly when they are in the same antichain *and* their file
> plans are disjoint.**

This is not hypothetical here. `docs/next/LAYER-C-BUILD-PLAN.md` §2.5 reproduces two feature packages
that both plan to write `app/home/page.tsx` while the plan reports `valid: True` — an antichain pair
with a colliding write surface. **The same disjointness test is also the missing coverage rule:** a
decomposition where two packages own one node is not a partition, and a plan whose file plans
intersect is not parallelisable regardless of its width.

Two failure modes the source names that this test does *not* cover, stated so nobody reads it as more
than it is: *"treating 'fast' as done before correctness is proven"*, and *"hiding skipped checks
behind a success summary"* — the second is `.claude/skills/validation-evidence` §2.2.

### (e) A splitter must be allowed to decline

Added 2026-08-26 from `docs/mined/OTHERS-MINED.md:756` (task-master `analyze-complexity`): score
first, expand second, and **the scorer may return "do not decompose."**

A decomposition step whose only outputs are *n ≥ 2* parts will always find a seam, because it was
asked to. *"This is already the right size"* must be a reachable, first-class return — not the
absence of a result, and not a part count of one, which reads as a degenerate split rather than a
decision.

Two corollaries when applying this to Layer C's granularity question:

- **The declining answer carries its own evidence.** *"Not split, because `expected_output_tokens`
  is under the chunk budget"* is a decision; *"not split"* alone is silence
  (`.claude/skills/validation-evidence` §2.3).
- **The score is a rule, not a judgement** — §(c)'s propagation cost, or the architecture's own
  measurements, per `.claude/skills/architecture` §4's fourth test. The scoring *mechanism* for
  Layer C is `docs/next/LAYER-C-BUILD-PLAN.md` §3.2 and needs an ADR; this section only says the
  mechanism must be able to say no.

### (f) A boundary a gate cannot independently reject is not a boundary

Added 2026-08-26 from `docs/mined/OTHERS-MINED.md` §2.1 (superpowers `writing-plans`):

> *"A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's
> gate… split only where a reviewer could meaningfully reject one task while approving its
> neighbor."*

**A second, independent criterion, and it produces coarser packages than the architectural one.**
Layer C decomposes by architectural boundary — entity, screen, connector. This asks a different
question: could a gate accept package A and reject package B, and would that mean anything? Where
the answer is no, the two are one unit however cleanly the architecture separates them.

Apply it **after** §(a)–(c), as a check on the result rather than as the partitioning rule. It
matters most for Layer E, because a package is what a gate accepts or rejects — and it is the
criterion that argues *against* over-splitting where §(c) alone would argue for it.

**The mined verdict was *"take as a validation rule"*, and this section is deliberately not that.**
As a criterion for judging a decomposition it is a skill; as a rule identifier in
`layerc/validate.py` it decides what Scio builds and needs an ADR of its own —
`docs/triage/LAYER-BC-TRIAGE.md` records the finding and deliberately does not open one.

## 3 · Limits — what the sources show versus what we assume

**What is actually shown:**

- Propagation cost is defined and computed over **file-level dependency matrices of existing
  code**, across large real systems (Mozilla, Linux and others in the MacCormack line of work),
  and correlates with organisational structure and with later maintenance cost.
- DRH clustering algorithms are validated on **recovered architectures of existing repositories**,
  where the ground truth is what the code does.
- Bunch's MQ is validated as a **clustering objective**, not as a predictor of build quality.

**What we are assuming, and must not claim:**

- **Scio's graph is a plan, not code.** Nodes are packages that do not exist yet; edges are
  declared intentions. Every empirical result above is about dependencies *observed* in shipped
  source. That a low propagation cost in the plan produces better generated code is our
  hypothesis and is unmeasured.
- **The graphs are tiny.** 5–20 packages, versus thousands of files. Metrics designed to
  discriminate between large architectures may be noisy at this size; a single edge can move
  propagation cost by several points. Treat the *direction* of change as the signal, not the
  absolute value.
- **Parallel-safe is a stronger claim than antichain.** Two packages in an antichain declare no
  dependency on each other. They can still collide on a *file* — reproduced in Layer C §2.5,
  where two feature packages both plan `app/home/page.tsx` with no declared edge between them.
  **The antichain is necessary, not sufficient. Check the file plan too before batching.**
- **No claim about cost saving.** The Batch API's 50% discount is real; that a parallel build is
  cheaper end-to-end depends on repair rounds, which are not modelled here.
- **§(d), §(e) and §(f) are practitioner findings, not results.** Added 2026-08-26 from mined
  skills and command files, each read once, none with an evaluation attached. The write-surface
  test is *derivable* — it follows from what a file collision does — and is the strongest of the
  three. The review-boundary criterion in §(f) is a heuristic from one plan-writing skill and
  **conflicts with §(c) by design**: propagation cost can favour splitting where a reviewer's
  boundary favours merging. That conflict is real and this skill does not resolve it; name it in
  the ADR rather than picking whichever number agrees with you.

## 4 · Eval

Runnable against `apps/engine` in `hello-world`, using `build_plan(derive_architecture(spec))`.

| # | Case | Expected | Why it is the right test |
|---|---|---|---|
| D1 | canonical booking plan, levels from Kahn | `[pkg_foundation]`, then `{pkg_design_tokens, pkg_schema}`, then `pkg_auth`, then `{pkg_feature_*, pkg_connector_*}` | the layering is the claim; if it does not come out layered, the DRH framing is wrong for Scio and this skill should be dropped |
| D2 | `parallelizable` recomputed as antichain membership | identical result to `len(group) > 1` on **every current fixture** | proves the rewrite is behaviour-preserving today — which is exactly why it is safe to land before it is needed |
| D3 | construct a plan where one feature package depends on another | antichain method flags them **not** parallelizable; `len(group) > 1` flags them parallelizable | the failing case the current implementation cannot see. If this does not diverge, the antichain buys nothing |
| D4 | propagation cost, 2-action booking plan vs 12-action plan | 12-action plan is **not** lower despite having more packages | more packages is not more modular; the metric must refuse to reward package count |
| D5 | split `pkg_feature_booking` into two per-operation packages (Layer C §3.2) | report propagation cost before and after | this is the decision C-3 turns on. **No expected value** — the point of the eval is that the number is produced *before* the ADR is argued, not after |
| D6 (negative) | two packages in the same antichain that plan the same file path | flagged as a conflict, not as parallelizable | the reproduced double-ownership bug. An antichain check that passes this case is unsafe to batch on |

**Pass condition:** D1–D4 and D6 behave as stated; D5 produces a number and is reported without
a recommendation attached. A skill that answers D5 with a preference rather than a measurement
has stopped being this skill.
