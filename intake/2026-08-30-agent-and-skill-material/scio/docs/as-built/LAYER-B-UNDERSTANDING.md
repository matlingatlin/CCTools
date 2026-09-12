# Layer B · Understanding & architecture — as built

Spec in, three linked artifacts plus a validation result out. 8 files, 1,308 lines. Governed by **ADR-0012** and
`docs/LAYER-B.md`.

---

## 1 · Purpose

Turn Layer A's typed spec into something buildable *and* something a person can approve:
a coherent narrative they recognise, a machine-readable architecture, and the fixed house
rules every build prompt carries.

The governing method, from ADR-0012: **deterministic-first**. Rules do what rules can
guarantee; the model is used only for judgement, grounded, with additions flagged.

## 2 · Public surface

`layerb/service.py` — `AppSpec → { whole, architecture, playbook, validation }`.

Refuses to run on a spec that has not passed gate 1: `NotBuildableError`. Layer B cannot be
reached around.

## 3 · In and out

**In** — a buildable `AppSpec` from Layer A, read through its downstream tags.

**Out** — `AppSpec → { whole, architecture, playbook, validation }`. Three artifacts plus the
validation result, which is a real fourth return and is described under §4:

| Artifact | What it is | Built by |
|---|---|---|
| **The whole** | the human narrative shown at the spec gate — the frozen contract the user approves | model, grounded |
| **Architecture** | a typed, machine-readable graph — tables, columns, relations, auth, roles, permissions, operations, screens | rules |
| **Playbook** | fixed house rules: stack, folder structure, naming, secure-by-default list | constant |

`Whole` carries `narrative`, `assumptions`, `grounding`, `models_used`, `generated`.

`Architecture` is a real typed graph — `Table{columns, relations, row_level_security}`,
`AuthAccess{mode, roles, permissions}`, `Operation{verb, entity, inputs}`, screens. **Every
node records `source_field`**, so a change upstream can be traced to the parts of the
architecture it touches.

## 4 · Invariants

**Order is load-bearing.** From `service.py`: *"The deterministic backbone is derived first
and validated before the LLM is asked for anything, so a design error costs a function call
rather than a relay run."*

**Eleven rules run before any code is generated**, emitted by six check functions (`validate.py`).
Exactly one — `screen_references_operation` — is warning severity; the other ten block generation.
The rule *identifiers* are what an impact-analysis or conformance mechanism would key on:

| Check | Catches |
|---|---|
| operations hit valid entities | an action on a table that does not exist |
| permissions map to operations | a role granted something nobody can do |
| no login conflict | "no sign-in" plus per-user data or multiple roles |
| relations resolve | a foreign key pointing nowhere |
| screens reference real operations | a screen wired to nothing |
| something to build | an architecture that is empty |

`valid` is False when any error-severity rule fires.

**The whole is grounded, not free.** Its system prompt: *"Ground every sentence in the facts
listed below. Do not invent features, entities, integrations or constraints that are not
there."* And critically — **the assumed-field list comes from Layer A's metadata, not from
the model's own claim about itself.** The model cannot decide what counts as an assumption.

**Vocabulary is canonical and shared.** `vocabulary.canonical_name` is imported by Layer A
too, so both layers name things the same way.

## 5 · Dependencies

**Up:** Layer C reads the architecture graph (66 edges `C → B`); the library consults it
(26 edges `D → B`).
**Down:** Layer A's spec and gate (29 edges `B → A`).

`derive.py` is 427 lines — a third of the layer, and the largest single file. It is the
deterministic translation from tagged spec fields into the typed architecture.

## 6 · State

### Solid — carry forward unchanged

- **Deterministic-before-model ordering.** Validate the architecture with rules before
  spending a relay run. This is the cheapest quality mechanism in the whole system.
- **The eleven validation rules.** (Six counts the check *functions*; `validate.py` emits
  **eleven** distinct rule identifiers — ten error, one warning.) Each catches a class of
  incoherent app that would otherwise
  be discovered as broken generated code.
- **`source_field` on every architecture node.** Traceability from architecture back to the
  sentence the user said. This is what makes surgical change possible later.
- **Assumptions sourced from Layer A's metadata**, not from the model's self-report.
- **`NotBuildableError`.** The gate cannot be bypassed.
- **`whole.py` is the synthesis step.** *"Organise and articulate better than the user did:
  connect the scattered facts."* The "present it back better than they said it" requirement
  already exists here — it is not missing, it is Layer B's first output.

### Wrong-shaped

- **The whole is prose only.** `Whole.narrative` is text plus a flat `assumptions` list.
  There is no per-area coverage score — nothing that could render "security 86%, data 90%,
  UI 40%". The structured half of a presentation-back does not exist; only the narrative half.
- **`Whole.grounding` is `dict[str, str]`.** Loosely typed for something whose job is to prove
  each sentence traces to a fact.

### Missing

- **No scored readiness per build area.** The downstream tags already partition the spec into
  areas (`data_model`, `auth`, `access_rules`, `connectors`, `design_tokens`, `scope`), and
  every field already knows whether it was stated, derived or defaulted. A coverage score per
  area is therefore *computable today from data that already exists* — it simply is not
  computed. This is the smallest high-value gap found so far.
- **No record of whether the user accepted the whole unchanged.** The approve endpoint exists
  (`POST /spec/approve`) but nothing measures how often the narrative was right first time —
  which is the natural quality signal for both A and B.

### Obsolete

None found.

## 7 · Open questions

**a. Should the whole carry structure as well as prose?** Adding per-area scores changes what
the spec gate shows the user. It is computable from existing metadata, so the question is
product, not engineering: does a score increase trust or invite haggling?

**b. Is `derive.py` at 427 lines one responsibility or three?** It is the largest file in the
layer and the least described. Worth a closer read before any rebuild touches it.

**c. `D → B` (26 edges).** The library consults Layer B directly. Intended (matching needs the
architecture) or an inversion? Answer in `LAYER-D`.

---

*Verified 2026-08-26 against the code. Layer B has **60 tests**, not 30 — `test_layerb_derive`
(30), `test_layerb_validate` (14), `test_layerb_service` (16), all passing in 0.57s. The earlier
figure counted only the derive half, and the earlier "six rules" counted check functions rather
than the eleven rule identifiers they emit. Both corrected 2026-08-26.*
