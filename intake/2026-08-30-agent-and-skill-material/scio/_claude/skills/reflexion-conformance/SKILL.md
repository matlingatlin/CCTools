---
name: reflexion-conformance
layer: E
phase: build-time
status: written
description: Check generated or existing code against a stated architecture using a software reflexion model — a high-level model plus a mapping, producing convergences, divergences and absences rather than pass/fail. Use when deciding whether the architecture graph is the contract, when checking whether a build matches what was approved, when designing architecture conformance or drift detection, or when someone proposes a boolean "does the code match the design" check.
---

# reflexion-conformance

Checking code against an architecture is not a boolean. The founding paper says so, and its
three-way answer is a better fit for a system that generates code than pass/fail is — because the
interesting failure is **source with no architecture behind it**, and a boolean cannot express
that.

---

## 1 · Source

**Software Reflexion Models: Bridging the Gap Between Source and High-Level Models.**
Gail C. Murphy, David Notkin, Kevin Sullivan. Proceedings of the 3rd ACM SIGSOFT Symposium on the
Foundations of Software Engineering (**FSE'95**), October 1995.

- [ACM DL](https://dl.acm.org/doi/10.1145/222124.222136) ·
  [Author page](https://www.cs.ubc.ca/~murphy/papers/rm/fse95.html)
- Extended as *Software Reflexion Models: Bridging the Gap between Design and Implementation*
  (IEEE TSE, 2001).

It is the technique underneath every architecture-conformance tool since — ArchUnit,
dependency-cruiser, Sonargraph, Lattix, Structure101 — and behind later work such as ReflexML
(UML-based architecture-to-code traceability) and CATMA (microservice conformance).

---

## 2 · Method, in the form we use it

### 2.1 The three inputs

A reflexion model needs exactly three things:

1. **A high-level model** — entities and the relations expected between them.
2. **A source model** — extracted from the actual artifacts, not authored.
3. **A mapping** — which source artifacts belong to which high-level entity.

In the original the engineer writes all three. **The mapping is normally the expensive part**, and
it is the part Scio already has for free:

| Reflexion input | What Scio already holds |
|---|---|
| high-level model | `Architecture` — tables, relations, operations, screens, permissions, each with `source_field` |
| mapping | `NodeRef{kind, name}` → build package (`layerc/plan.py`), `Manifest.packages` → files, `data-scio-id` → `{package, file, line}` (`core/instrumentation.py`) |
| source model | scanned out of generated source by `core/manifest_builder.py` — *"the manifest is an artifact of the build, scanned out of the files each package actually produced, never authored beside them"* |

That comment in `manifest_builder.py` is, without naming it, the reflexion principle: an authored
source model drifts silently, so extract it.

### 2.2 The three outputs — and why three matters

| Outcome | Meaning | What it means here |
|---|---|---|
| **Convergence** | the model says it, the source has it | the node was built as agreed |
| **Divergence** | the source has a relation the model does not | code reaching across a boundary the architecture did not declare — an unauthorised edge |
| **Absence** | the model says it, the source lacks it | something approved was not built |

**A fourth case is the one that matters most for a generator**, and it is absence read in the
other direction: **source artifacts that map to no high-level entity at all.** That is invariant
1's exact violation — a function traceable to no requirement, no visible assumption, no technical
necessity. A pass/fail conformance check cannot report it; a reflexion model reports it as the
unmapped remainder.

### 2.3 How to use the outcomes

Each outcome is a different conversation, and collapsing them loses that:

- **Absence** → a build gap. Report it, name the requirement, do not promote.
- **Divergence** → either the code is wrong or the architecture was incomplete. It is a *question*,
  and the original paper is explicit that a reflexion model is a lens for the engineer's
  understanding, not an oracle. In a generated system it should be a gate that escalates rather
  than a silent rejection.
- **Unmapped source** → the invariant-1 violation. This is the one that should block.
- **Convergence** → the evidence the reveal is supposed to show and currently does not.

### 2.4 Iterate the mapping, do not perfect it first

The paper's working method is iterative: state a rough model and mapping, compute, look at the
divergences, refine. In a generated system the mapping is derived rather than authored, so the
iteration target is different — divergences point at gaps in the *architecture schema*, i.e.
concepts the generated code needs that `Architecture` has no node kind for.

---

## 3 · Limits — what the paper shows versus what we would be assuming

| Claim | Status |
|---|---|
| Reflexion models are a durable technique | Very well supported. Thirty years, an entire tool category, continuous citation |
| They produce convergence / divergence / absence | Exactly what the paper defines |
| "This proves generated code matches the approved architecture" | **Not supported.** A reflexion model compares *structure*. It says nothing about whether behaviour is correct |

**Assumptions this skill makes that FSE'95 does not support:**

1. **The source model is extracted by regex, not by parsing.** `manifest_builder.py` records its
   own limits: ids built by concatenation outside a template literal, ids passed as props, and
   spread attributes are all invisible to it. The playbook forbids all three, so the source model
   is only as good as playbook compliance. **An AST parse is the honest upgrade**, and the paper's
   guarantees assume a source model that is actually complete.
2. **The paper assumes a human-authored high-level model of an existing system.** Ours is
   *derived* from a spec and describes a system that does not exist yet. Whether divergence rates
   behave similarly in that direction is unstudied.
3. **The paper offers no threshold.** How many divergences make a build unacceptable is a product
   decision, not a result. Any number chosen here is ours.
4. **Structural conformance is not security conformance.** A reflexion model would report that a
   table exists and a policy file exists. It would not report that the policy is `USING (true)`.
   Row-level-security correctness needs its own rule.

**The honesty rule:** this skill justifies the *shape* of the check — three outcomes, extracted
source model, explicit mapping. It does not justify a claim that conformance implies correctness.

---

## 4 · Eval

### E1 · Three outcomes, not two
Assert the conformance result distinguishes convergence, divergence and absence. A boolean, or a
list of "violations" that merges divergence and absence, fails.

### E2 · Unmapped source is reported
Construct generated source containing a component that maps to no architecture node. Assert it is
reported, and reported as an invariant-1 violation rather than folded into "divergence".

### E3 · Source model is extracted, never authored
Assert the source model's provenance field says it was scanned from the artifacts. A hand-written
or model-written source model fails — that is the drift the technique exists to prevent.

### E4 · Extraction limits are stated
Assert the extractor publishes its known limits (as `manifest_builder.KNOWN_LIMITS` does) and that
a verifier exists to catch violations of the assumptions those limits depend on.

### E5 · Divergence escalates, absence blocks, unmapped blocks
Assert the three outcomes have *different* consequences. Identical handling means the distinction
was decorative.

### E6 · No correctness claim
Grep the produced text, UI copy and docs for phrasing that turns structural conformance into a
behavioural guarantee ("verified correct", "matches the approved design" without qualification).
Any occurrence fails.

### E7 · Mapping completeness
Assert every architecture node kind has a mapping rule to source. A node kind with no mapping is
invisible to the check and will silently always converge.

---

## 5 · When this skill is the wrong tool

- **Behavioural verification.** Tests, browser flows and the vision loop do that. Reflexion is
  structure only.
- **Ranking or prioritising context.** That is a retrieval problem, not a conformance one.
- **Deciding what the architecture should be.** Reflexion checks against a stated model; it does
  not propose one.

---

*Scanned and written 2026-08-26. Source read at method level; not reproduced. The mapping-already-
exists claim is verified against `layerc/plan.py` and `core/instrumentation.py` in hello-world.*
