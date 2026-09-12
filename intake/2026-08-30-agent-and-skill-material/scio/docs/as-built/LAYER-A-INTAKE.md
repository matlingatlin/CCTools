# Layer A · Intake — as built

Gate 1. Conversation in, typed spec out. 17 files, 2,775 lines, 67 tests — all passing
2026-08-26.

Governed by **ADR-0010** and `docs/INTAKE-SCHEMA.md`.

---

## 1 · Purpose

Turn what a person says into a typed, buildable specification — and make every field
traceable to whether they *said* it, the system *inferred* it, or it was *assumed*.

ADR-0010 states the reason plainly: *"Blank-prompt builders fail because their input is an
unstructured blob; Scio's differentiator starts in the input."*

## 2 · Public surface

**Engine** (`apps/engine/src/scio_engine/main.py`)

| Endpoint | Does |
|---|---|
| `POST /intake/step` | one turn: extract → contradictions → gate → next question |
| `POST /intake/validate` | is this spec buildable |
| `POST /intake/correct` | apply one hand correction, re-run the gate |

**API** (NestJS)

| Route | Does |
|---|---|
| `GET  /projects/:id/intake` | conversation history |
| `POST /projects/:id/intake/message` | one user turn |
| `POST /projects/:id/draft-spec/field` | correct one field |
| `GET  /projects/:id/spec/versions` | spec history |
| `POST /projects/:id/spec/approve` | freeze the spec |
| `POST /projects/:id/spec/amend` | amend an approved spec (used by the design window, ADR-0015) |

**Frontend** — `WizardPage.tsx` (the conversation), `SpecPage.tsx` (review and correct).

## 3 · In and out

**In** — a conversation. Messages carry stable ids (`m1`, `m2`…) because provenance depends
on them; only user turns count as evidence.

**Out** — an `AppSpec` where every filled slot is a `FieldMeta`:

```
value · source (stated|derived|default) · confidence (low|med|high) · provenance[message ids]
```

Six core fields (`purpose`, `users_and_roles`, `entities`, `key_actions`, `sign_in`,
`data_ownership_sensitivity`), nine conditional follow-ups fired by explicit triggers,
`non_goals` always asked, and six defaulted-and-flagged slots (`platform`, `data_owner`,
`look`, `publishing`, `security_and_a11y`, `scale`).

Every field carries a **downstream tag** naming the build area it feeds — `entities →
data_model`, `sign_in → auth`, `non_goals → scope`. This is what Layers B and C consume;
without it they have prose.

## 4 · Invariants

Taken from the tests. Test names are the evidence.

| Invariant | Test |
|---|---|
| An unstated value is never invented | `test_an_unstated_value_is_not_invented` |
| Inference may not overwrite what the user stated | `test_an_inference_may_not_overwrite_what_the_user_stated` |
| An inference is never high confidence | `test_an_inference_is_never_high_confidence` |
| Extraction may not overwrite a hand correction | `test_extraction_may_not_overwrite_a_hand_correction` |
| A contradiction is asked about, not resolved | `test_a_contradiction_is_asked_about_rather_than_resolved` |
| A placeholder value counts as no answer | `test_a_placeholder_value_is_treated_as_no_answer` |
| The user's own words are kept | `test_what_it_files_is_still_the_users_own_words` |

Enforced in code, not only prompt — in `apply_extraction()` (`intake/extraction.py:160`),
*"Fold a proposal into the spec, keeping only what survives the rules"*, with `Rejection` at
`:64` and `_merge_list()` at `:142` (*"Add what is new, keeping the user's own wording"*). The
gate itself is `is_buildable()` at `intake/gate.py:62`, `triggered_conditionals()` at `:28`.
A field claiming `stated` without real message-id provenance is **discarded**. A hand correction writes the literal mark
`corrected-on-review` into provenance — deliberately not a message id, so *"a model can
never forge this mark."*

Rejections are returned, not swallowed: *"a silent drop looks identical to a model that
said nothing, and the two need different fixes."*

## 5 · Dependencies

**Up:** Layer B reads the spec (29 graph edges `B → A`).
**Down:** cross-cutting services (62 edges `A → G`), and the build layer (43 edges `A → E`).

The `A → E` edges are **not** cost estimation — `intake/` never mentions `estimate`. They are
`execution.provider`, `execution.relay` and `execution.untrusted`: the shared model-calling
machinery six of seven layers use. Intake is metered per exchange (`cost_usd` on both extraction
and question). Not a layering problem. *(Corrected 2026-08-26; the first reading was wrong.)*

Intake also imports `layerb.vocabulary.canonical_name`, so the canonical vocabulary is
shared rather than duplicated.

## 6 · State

### Solid — carry forward unchanged

- **Provenance model.** `FieldMeta{value, source, confidence, provenance}` with enforcement
  in code. This is the strongest thing in the layer and the hardest to rebuild correctly.
- **The buildable-enough gate.** `is_buildable()` — core answered or flagged, triggered
  conditionals resolved, no open contradictions. *Momentum over completeness*, decided in
  ADR-0010 and testable rather than a vibe.
- **Downstream tags.** The mechanism that makes B and C possible at all.
- **Correction machinery.** Typed, shape-checked, cannot be overwritten by extraction.
- **Contradiction detection** by rules, not judgement, with resolutions carried forward.
- **The stand-in path.** `StandInIntakeProvider` completes gate 1 with no API key, so the
  free path finishes and tests run deterministically.

### Deliberate, and easy to break by accident

**The WHICH/HOW split.** Which field to ask is decided by the gate — deterministic, free,
and per the docstring *"impossible for a model to talk its way past."* Only the **wording**
goes to the model. Every question returns `{question, example}`, falls back to the schema's
own wording on any failure, and records `written_by: model|guide`.

One relay pass per question, on purpose: *"a question is a sentence, and running the full
relay on every turn of the wizard would multiply the cheapest part of the build."*

Any proposal to make question selection adaptive (scoring, re-ranking) trades this guarantee
for adaptivity. That is a real trade, not a free improvement, and must be argued explicitly.

### Wrong-shaped

- **`is_buildable()` returns a boolean.** Buildability is really a distribution over how much
  the downstream must invent. A boolean cannot express *"buildable, but Layer C will be
  guessing about six things."*
- **No scored view of coverage.** The spec gate shows assumed tags, but nothing summarises
  *how well understood* an area is — no per-area readiness figure to show the user.
- **No app-kind detection.** The schema is per-type (`app`), but nothing classifies *what kind
  of app* early and uses that to steer the questions. Every app walks the same six fields in
  the same order.

### Missing

- **No feedback loop from build failure back to the intake field that caused it.** Corrections
  are captured at review time only, so intake cannot learn from what went wrong later.
- **No replay harness or metric.** Nothing measures turns-to-buildable, assumed-rate at the
  gate, misfile rate, or contradiction catch rate — so no change to this layer can be shown
  to be an improvement.

### Obsolete

None found.

## 7 · Open questions

**a. Which wedge does this serve?** ADR-0001 says *founders and small teams*, with
developer-grade output. The schema's vocabulary (`entities`, `data_ownership_sensitivity`)
fits that audience. If the wedge moves toward people with no technical vocabulary, ADR-0001
must be superseded **before** Layer A is redesigned — it decides what "the right question"
means. See `01-DECISIONS.md`.

**b. Fixed order versus scored selection.** Settled deliberately in favour of fixed order for
a stated reason. Reopening it requires an ADR that addresses the guarantee being given up.

**c. What replaces the boolean gate**, if anything, and whether Layer C actually wants a
richer signal or is happy with the flag list.

---

## Documentation drift found

`docs/STRATEGY.md` §A line 12 states:

> **Intake agent (conversation → filled spec).** Designed; NOT built. `[gap]`

**This is stale.** The agent is built and has been run for real:

- `extraction.py:317` — `await run_relay(...)`
- `questions.py::write_question` — relays for wording, falls back to the guide
- `service.py::run_intake_step` — orchestrates the full turn, metered per exchange
- Last changed 2026-08-19 / 2026-08-22, commit *"what the first real run surfaced"*

`STRATEGY.md` was last touched 2026-08-19 and the code moved past it. Treat §A as a
historical snapshot, not current status.

*Verified 2026-08-26 against the code, with all 67 intake tests passing.*
