---
name: provenance-record
layer: A
phase: build-time
status: written
description: Choose what a stored assertion carries besides its value, and where each invariant is enforced. Use when designing or reviewing a record that holds user-supplied facts over time, when a value might be silently re-derived, when deciding whether time may erode a fact, when something is superseded rather than deleted, when a decay or half-life stops surfacing something, when a version chain can branch, when a status field is about to become mutable, or when deciding whether an inferred value may be shown versus acted on. Carries the four axes a memory schema separates, the fail-open and fail-closed asymmetry between showing a fact and offering a component, the rule that monotonicity is enforced at write and never repaired at read, and two thresholds for two consequences.
---

# provenance-record

`FieldMeta{value, source, confidence, provenance}` answers *where did this come from*. Read beside
a schema built for the same job at larger scale, it turns out to answer only one of four questions
a record about a person's stated facts has to answer over time — and to leave three implicit.

This skill is the four questions and where each one is enforced. It is not a proposal to change
`FieldMeta`; every such change is an ADR.

---

## 1 · Source

Read as files on 2026-08-26, recorded in `docs/mined/`. Code, not papers — see §6.

| Source | Licence | What it contributes | Mined in |
|---|---|---|---|
| `supermemoryai/supermemory` @ `9652478` — `packages/validation/schemas.ts:242-278` (`MemoryEntrySchema`, 22 fields), `references/architecture.md:172-184`, `canvas/version-chain.ts`, `apps/mcp/src/server/format.ts:79-81` | MIT | the four axes, `isStatic`, the tri-state predicate, the version-chain defects | `OTHERS-MINED.md` §5, `PASS2-FOUR-REPOS.md` §3–§3.3 |
| `garrytan/gstack` @ `ad84005` — `plan-tune` | MIT | the display / promotion gate split | `PASS2-GSTACK-SKILLS.md` §4.6 |

**Two of the four supermemory findings are corrections of our own first pass.** `OTHERS-MINED`
took the forgetting model at face value; `PASS2-FOUR-REPOS` §3.1 opened the code and found no
engine behind it. What survives is the vocabulary, and it survives as *an idea from their schema,
not a mechanism observed working.*

---

## 2 · The four axes

Read whole, `MemoryEntrySchema` separates four things that `FieldMeta` collapses into one.

| Axis | Their fields | The question it answers | Scio today |
|---|---|---|---|
| **Identity over time** | `version`, `isLatest`, `parentMemoryId`, `rootMemoryId` | which assertion is current, and what it replaced | spec-level only (`GET /projects/:id/spec/versions`); a *field* has no history |
| **Authority** | `isInference`, `isStatic` | may this be silently re-derived; may time erode it | half — `source` answers the first, richer than their boolean. **Nothing answers the second** |
| **Lifecycle** | `forgetAfter`, `forgetReason`, `isForgotten` | when does this stop applying, and why | nothing |
| **Corroboration** | `sourceCount`, and a join carrying `relevanceScore` per source | how many sources, and which ones | `provenance` is a list of message ids, so the count exists; nothing reads it |

**Where we are already ahead, and should not trade down.** `source` is `stated | derived | default`
— three values enforced in `apply_extraction()` — against their single `isInference` boolean.
A `default` is not an inference, and losing that distinction would cost the flag that makes an
assumed value visible. Do not adopt a bit that has less information than the field it replaces.

### 2.1 `isStatic` — the second authority bit, and the one we lack

`isInference` says **where a value came from**. `isStatic` says **whether time may erode it**. They
are orthogonal, and their architecture notes define both ends:

> static — *"permanent facts that don't change… not subject to temporal updates, high priority in
> retrieval"*; dynamic — *"contextual, episodic… can be updated or superseded, time-sensitive
> relevance."*

Worked through Layer A's own vocabulary:

| Field value | `source` | Static? |
|---|---|---|
| *"the app is for booking restaurant tables"* | `stated` | **static** — a later turn does not make this less true |
| *"the user is unsure about payments"* | `stated` | **dynamic** — this is a statement about a moment |
| *"platform: web"* | `default` | dynamic; it is exactly what a later turn should be allowed to overwrite |

Without the second bit there is **no principled rule for which fields a later conversation may
quietly revise** — which is the question Layer F's directed change asks on every pass. `source`
cannot answer it: both rows one and two are `stated`, and they behave completely differently.

### 2.2 Lifecycle: a decay that cannot say *why* is unauditable

Their three lifecycle fields have no engine — `forgetAfter` is read in exactly one place, a
border-colour function, and nothing writes `isForgotten`. Their own test states the consequence:
an already-elapsed `forgetAfter` *"does not… expire"*. **An expiry date that has passed produces
no state change and no signal.**

Ours is the opposite shape: graphify's `save-result` / `reflect` gives half-life decay and a
corroboration threshold deterministically. **We have the engine and no vocabulary; they have the
vocabulary and no engine.** The trade is one-directional — keep the decay, add the reason string.

A half-life that silently stops surfacing a fact cannot answer *"why doesn't my app do that any
more?"* One column turns a decay artefact into an auditable statement.

Take the presentation vocabulary with it: three closed words — **Latest · Superseded · Forgotten**
— with the reason rendered beneath when present. Note what reading their component adds: the
reason is **optional in the type and the UI degrades to a bare label**. Requiring a reason would
mean fabricating one or blocking, and both are worse.

---

## 3 · Fail open or fail closed — decide by which wrong answer costs more

Both of their retrieval paths use one predicate:

```ts
entry.isForgotten !== true && entry.isLatest !== false
```

Written `!== true` / `!== false` rather than the positive forms, so **`null` and `undefined` count
as active and visible.** That is deliberate and it is right for a memory store: missing metadata
should not hide a fact a person gave you.

It is the **exact opposite** of the same mining pass's other default, where a caller that does not
declare an operation gets `write` — fail-closed — because a wrong permissive answer ships something.

Both are right, and they look inconsistent until the asymmetry is named:

| Situation | Unknown means | Because a wrong answer costs |
|---|---|---|
| An intake field with missing or unreadable provenance | **shown** | hiding something the user said, invisibly |
| A library component's `offerable` | **withheld** | shipping a component that should not have been offered |

**Write the two rules next to each other**, in the same document, with the asymmetry stated. Split
across two files they read as an inconsistency and somebody eventually "fixes" one of them.

---

## 4 · Enforce at write; never repair at read

Their version chain recomputes a stored version number at render time when it is not strictly
increasing. **Do not copy this.** It enforces the right invariant in the wrong place: the stored
data stays wrong indefinitely, every other consumer sees the wrong thing, and the violation becomes
unfindable because the one surface that could have shown it hides it.

The rule generalises past version numbers to every invariant over stored records:

- **Enforce at write.** A record that violates it does not get stored.
- **Detect at read**, if you must — and *report*, never silently correct.
- **A violation must stay findable.** The renderer is not the place invariants live.

Two more from the same 106-line file, both worth taking as the inverse:

- **Branching is forbidden at write or represented — never silently linearised.** Theirs follows
  *"the first child at each step… only the first branch (by document order) is included"*, so a
  second child is invisible with no marker. Two directed changes from one approved spec is what
  `POST /projects/:id/spec/amend` produces, so this is Scio's ordinary case, not an edge case. If a
  display linearises, the display must say so.
- **Do walk the chain with a `visited` set** in both directions. A corrupted parent pointer that
  forms a cycle then terminates instead of hanging — the one thing that file does unambiguously
  right.

---

## 5 · Two consequences need two thresholds

An inferred value can be **shown** to a person or **acted on**. These are different acts with
different costs, and one threshold for both is a category error.

From `plan-tune`, which built the measurement and deliberately did not ship the adaptation:

| Gate | Their bar | What it licenses |
|---|---|---|
| **Display** | sample ≥ 20, ≥ 3 contexts, ≥ 8 distinct questions, ≥ 7 days span | showing the inferred value |
| **Promotion** | 90+ days stable across 3+ contexts | letting it change behaviour |

> *"Displaying inferred values is a UI affordance; shipping behavior-adapting defaults based on the
> profile is consequential and needs a much higher bar. **Do NOT use the display gate as a green
> light.**"*

The same file reports the gap between what a user *says* they want and what their answers imply, in
words rather than a number — *close* · *drift* · *mismatch* — and **never auto-applies it**: the
gap is reporting only, and the user decides which side is wrong.

For Layer A the mapping is direct: a `derived` field shown in the spec review with its tag is the
display gate; a `derived` field that silently steers what gets built is the promotion gate. Today
one mechanism does both.

---

## 6 · Limits — what the sources show versus what we would be assuming

| The source shows | We would be assuming |
|---|---|
| A **22-field schema in production** at a memory company | that a spec field is the same kind of object as a memory. A memory is one assertion retrieved by similarity; a `FieldMeta` is a typed slot in a schema that a build reads whole. The axes transfer; the retrieval reasoning does not |
| `isStatic` **declared and documented** | that it is *used* well. `PASS2-FOUR-REPOS` verified the forgetting fields had no engine; **the same audit was not run on `isStatic`.** Treat it as a well-argued distinction, not a validated one |
| Three lifecycle fields | a working forgetting model. **There is none** — one reader, no writer, and a test that documents the no-op. This is the clearest case in the corpus of a schema that describes a mechanism nobody built |
| A tri-state predicate that fails open | that fail-open is right *for us*. It is right for the same reason it is right for them — hiding a stated fact is the worse error — but the reason has to be re-checked per surface, not inherited |
| Display and promotion gates with **specific numbers** | that the numbers transfer. Their thresholds were tuned to their volume across 50+ skills. Scio has no preference profile at all, so the numbers are illustrative and only the **two-gates shape** is portable |
| Code, running, with tests | a measured outcome. **No source here reports one.** Nothing says the four axes produce better retrieval, fewer wrong revisions, or anything else measurable |

**And the standing hazard:** every axis is a column, and every column is a thing that can be wrong,
unmaintained, or quietly ignored — which is precisely what their own lifecycle fields turned out to
be. A record gains an axis when something *reads* it and changes behaviour. Adding one because the
taxonomy has four is how you end up with `forgetAfter`.

---

## 7 · Eval

| # | Case | Expected |
|---|---|---|
| E1 | A `stated` fact about what the app is, and a `stated` fact about the user's momentary uncertainty | Distinguishable. If the record cannot tell them apart, the authority axis is missing — this is the case that justifies a second bit |
| E2 | A later turn contradicting a `default` value, and a later turn contradicting a `stated` static value | The first is overwritten silently; the second is a **User Challenge** (`clarifying-questions` §2.1). The record is what makes the two distinguishable |
| E3 | A decay drops a fact | A reason is written and readable. A fact that stops applying with no reason recorded is a defect, not a tidy-up |
| E4 | A record with missing or unreadable provenance metadata, on the intake surface | **Shown.** Asserted as its own test, because it is the branch nobody exercises deliberately |
| E5 | The same missing metadata on the component-offer surface | **Withheld.** E4 and E5 must both exist in the same suite, or the asymmetry is an accident |
| E6 | A stored version number that is not strictly increasing | Rejected at write. A read that finds one **reports** it. A run where the renderer silently renumbers is the failure this section exists for |
| E7 | Two amendments made from the same approved spec version | Either refused at write, or represented as two branches. **Not** silently linearised to the first by insertion order |
| E8 | A parent pointer forming a cycle | Traversal terminates. `visited` set, both directions |
| E9 | An inferred value that clears the display bar but not the promotion bar | Shown with its tag; **does not** change what gets built. Assert the second half, since passing the first is what makes it look finished |
| E10 | Grep for a write that sets a lifecycle or authority field outside its owning module | Zero matches. An axis enforced in two places is enforced in neither |

**E4 with E5, and E2, are the load-bearing ones.** E4 alone passes trivially by showing everything;
E5 alone passes trivially by hiding everything. The pair is the test.

---

## 8 · When this skill is the wrong tool

- **Checking whether a citation supports its claim.** That is `ais-grounding`.
- **Deciding whether to ask the user about a conflict.** That is `clarifying-questions`.
- **Adding a field to `FieldMeta`.** That is a schema change to the product and needs an ADR; this
  skill supplies the argument, not the decision.
