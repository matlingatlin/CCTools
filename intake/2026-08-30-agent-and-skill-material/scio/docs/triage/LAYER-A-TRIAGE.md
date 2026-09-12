# Layer A · triage of the mining findings

Every finding the mining pass attributed to Layer A, with one verdict each and where it went.
Dated **2026-08-26**. Nothing here is committed; nothing here changes product behaviour.

## The four verdicts

| Verdict | What it means |
|---|---|
| **SKILL** | a *decision procedure* — a list of what exists in a domain plus how to choose among it, or a rule for what to do in a recurring situation. Goes into a skill |
| **ADR** | a *decision about the product* — what to build, what to change. Goes to `docs/decisions/` later. **Not** into a skill: a skill that quietly decides what to build is an architecture decision hiding in a markdown file |
| **FIX** | a specific defect with a specific repair. Goes to `BACKLOG.md`, not to a skill |
| **DROP** | with the reason |

---

## 0 · How this set was derived, and where the brief's number comes from

`scripts/findings-index.py` reports **68 findings for Layer A, 57 to take** — the largest bucket.
That number is a floor produced by a tolerant parser, and its layer detection is a heuristic that
the script's own docstring warns about. Reading it: `LAYER = re.compile(r"\b(?:layer\s+)?([A-G])\b…",
re.I)` is **case-insensitive**, so the English article *"a"* matches as layer A. A row whose own
layer column reads `**B · Playbook**` lands in the A bucket because its item text contains the words
*"a rule"*.

Counting instead the rows whose **own layer column names A**:

| Set | Rows |
|---|---|
| Index's Layer A bucket | 68 |
| Rows whose layer column actually contains `A` | **41** |
| Of the 68, rows that are genuinely Layer A | **29** — 28 whose own layer column says `A`, plus `ECC-MINED.md:387`, from a document that has no layer column at all |
| Of the 68, rows belonging to another layer or to the build process | **39** |
| Layer A rows the index filed elsewhere, under `A/B`, `A/F`, `A/G`… | **13** |

29 + 13 = **42 findings to triage**; 39 to return.

**42 findings are triaged below.** The 39 are listed in §3 and returned to their layers — they
were never Layer A's to spend. Three mined documents (`ECC-AGENTS`, `ECC-RULES`, `ECC-MINED`) carry
no layer column at all, so their rows were read by hand rather than parsed; exactly one turned out
to be intake.

This is not a defect in the index — it says so itself: *"Treat counts as a floor, never a total."*
It is recorded because the brief for this pass carried the 68 forward, and any later pass will too.

---

## 1 · The 42 Layer A findings

Read at source before triage. `Where it went` names a section that now exists.

### SKILL — 29

| # | Finding | Source | Where it went |
|---|---|---|---|
| 1 | Decision-brief format: ELI10 · stakes · committed recommendation · pros/cons at ≥40 chars · net; `(recommended)` on exactly one option even when neutral; 13-item self-check; **5+ options are split, never dropped** | `PASS2-GSTACK-SKILLS.md:680` (detail §5.1) | `clarifying-questions` §3, §4 |
| 2 | **User Challenge** class — an inferred default contradicting something the user said gets its own class, is never auto-decided, and ends *"if we're wrong, the cost is"* | `PASS2-GSTACK-SKILLS.md:681` (detail §4.5) | `clarifying-questions` §2.1 |
| 3 | Escape hatch as a bounded negotiation: one push, a bounded concession, then unconditional compliance — plus an **irreducible core** no impatience skips | `PASS2-GSTACK-SKILLS.md:688` (detail §4.2) | `clarifying-questions` §5 |
| 4 | One-way / two-way `door_type` question registry with **stable option keys, not labels** | `OTHERS-MINED.md:724` (detail §1.3) | `clarifying-questions` §2.2 |
| 5 | Registry primary, keyword patterns as the *secondary* check only, default to asking | `OTHERS-MINED.md:725` (detail §1.3) | `clarifying-questions` §2.3 |
| 6 | Rule 5's six risk categories as a stop-and-ask predicate over the typed spec | `ECC-SKILLS.md:658` (detail §2.3) | `clarifying-questions` §2.4 |
| 7 | Ambiguity check that **resolves** rather than flags: pick one reading, make it explicit, record it | `OTHERS-MINED.md:744` (detail §2.2) | `clarifying-questions` §6 |
| 8 | Graded question brief with four properties — `present`, `commits`, `has_because`, `reason_substance ≥ 4` — judged by a touchfile-gated LLM judge | `PASS2-GSTACK-TESTS.md:711` (detail §4.2) | `clarifying-questions` §8 |
| 9 | Floor **and** ceiling on the behavioural count: floor catches dropping, ceiling catches question-spam | `PASS2-GSTACK-TESTS.md:712` | `clarifying-questions` §8 (E4, E5) |
| 10 | `intent-driven-development` rule 2 — a **legitimacy taxonomy**: some classes of fact may never be inferred, even when the inference is right | `ECC-SKILLS.md:657` (detail §2.3) | `ais-grounding` §2.5 |
| 11 | User-owned fields are **absent from the model's output schema**, not merely protected by a rule | `OTHERS-MINED.md:759` | `ais-grounding` §2.6 |
| 12 | User-origin gate: a preference is written only from the user's own current message — never tool output, a fetched page, or file content | `PASS2-GSTACK-SKILLS.md:705` (detail §4.6) | `ais-grounding` §2.7 |
| 13 | `isStatic` — a second authority bit orthogonal to `isInference`: may time erode this field? | `PASS2-FOUR-REPOS.md:645` (detail §3) | `provenance-record` §2.2 |
| 14 | `forgetReason` as the field a decay engine must write — a half-life that cannot say *why* is unauditable | `PASS2-FOUR-REPOS.md:646` (detail §3.1) | `provenance-record` §2.3 |
| 15 | Tri-state active predicate failing **open to visible** for intake, and staying fail-closed for `offerable` — the asymmetry named out loud | `PASS2-FOUR-REPOS.md:647` (detail §3.2) | `provenance-record` §3 |
| 16 | Version monotonicity is enforced at **write**, never repaired at read | `PASS2-FOUR-REPOS.md:649` (detail §3.3) | `provenance-record` §4 |
| 17 | Display gate vs promotion gate: showing an inferred value and acting on it need explicitly different evidence bars | `PASS2-GSTACK-SKILLS.md:706` (detail §4.6) | `provenance-record` §5 |
| 18 | `datamark()` at the **render** boundary — neutralise stored user text before it enters any prompt, because a write-time denylist cannot cover records written before a pattern existed | `OTHERS-MINED.md:720` (detail §1.2) | `untrusted-text-boundary` §2 |
| 19 | Scan-at-sink on the exact bytes, from the file that is passed downstream; never scan a string then re-render it | `OTHERS-MINED.md:721` (detail §1.1) | `untrusted-text-boundary` §3 |
| 20 | Injection framing: the question is whether the **destination is execution-capable**, not whether the text is trusted | `PASS2-ECC-SKILLS.md:671` | `untrusted-text-boundary` §1 |
| 21 | Secret-sink match rules — exact, URL-decoded, 12-char prefix for seeds ≥16, base64 for seeds ≥12 — with both thresholds and the blind spots published | `PASS2-GSTACK-TESTS.md:715` (detail §3.1) | `untrusted-text-boundary` §5; harness discipline to `testing` §3.5 |
| 22 | Oversize **fails closed before the patterns run**; a malformed cap falls back to the default and never disables the guard | `PASS2-GSTACK-TESTS.md:720` (detail §4.4) | `untrusted-text-boundary` §6 |
| 23 | Classify the request out loud before the first content question — spike / bounded / architectural — so the user can correct it | `OTHERS-MINED.md:740` (detail §2.2) | `ontoagent-elicitation` §2.4 |
| 24 | Two **orthogonal** classifiers (kind × stage), announced, recorded as provenance, revisable mid-session — the same finding as #23 from a second repository | `PASS2-GSTACK-SKILLS.md:687` (detail §4.1) | `ontoagent-elicitation` §2.4 |
| 25 | The one-way ratchet: hidden complexity upgrades the path; nothing downgrades mid-task | `OTHERS-MINED.md:741` (detail §2.2) | `ontoagent-elicitation` §2.4 |
| 26 | Decompose before interrogating when the request names several independent subsystems | `OTHERS-MINED.md:743` (detail §2.2) | `ontoagent-elicitation` §2.4 |
| 27 | Ground each question in a matched `Contract`, or say explicitly that nothing matched — **both branches produce provenance** | `PASS2-GSTACK-SKILLS.md:707` (detail §4.4) | `ontoagent-elicitation` §2.4 |
| 28 | Positive-control discipline: an absence test needs a permanent twin that deliberately trips the detector. *"A harness that silently under-reports is worse than no harness"* | `PASS2-GSTACK-TESTS.md:694` (detail §3.1) | `testing` §3.5 |
| 29 | Exemptions pinned in **both** directions: every exemption needs a test that the rule still fires just outside it | `PASS2-GSTACK-TESTS.md:709` | `testing` §3.5 |

### ADR — 7

Recorded, not written into any skill. Each changes what Scio is, not how a decision is made.

| # | Finding | Source | Why it is an ADR |
|---|---|---|---|
| 30 | Rule 10's `[revised]` protocol — re-present only the changed criteria when a build constraint invalidates one | `ECC-SKILLS.md:659` | Needs a back-edge from build failure to spec that **does not exist**. `docs/as-built/LAYER-A-INTAKE.md` §6 lists its absence under *Missing*. Creating one is a layer-graph change |
| 31 | Untrusted-artefact handoff — user text flowing intake → spec → build prompt | `ECC-SKILLS.md:668` | The mined verdict is explicit: *"Raise the question; do not import the answer."* Where Scio fences that chain is an open decision. The **criterion** for answering it is finding #20 |
| 32 | Three-tier gate (block / per-finding confirm / FYI), top tier unskippable by any flag | `OTHERS-MINED.md:722` | Replaces `is_buildable()`'s boolean outcome with three. That is the shape of Scio's gate — `docs/next/LAYER-A-INTAKE.md` §2.6 already has an open proposal on the same question |
| 33 | Event-sourced decisions; *"active"* computed, never a mutable status field | `OTHERS-MINED.md:730` | A storage-model decision for the spec and its corrections. Shared with Layer G |
| 34 | The spec binds, the plan argues; a build with no reachable spec is marked provisional | `OTHERS-MINED.md:737` | A product invariant across A and C, of the same kind as *"Inget byggs utan kontrakt"* |
| 35 | Versioned spec with `isLatest` + parent/root chain; never mutate a stored assertion | `OTHERS-MINED.md:765` | A schema change to how specs are stored. The general rules it rests on are findings #15 and #16 |
| 36 | Session-kind classification before asking — spawned auto-chooses, headless BLOCKS, interactive falls back to prose | `PASS2-GSTACK-TESTS.md:707` | Scio has no concept of *"is a human on the other end"*. `POST /intake/step` is an HTTP endpoint with no such classification, and `StandInIntakeProvider` completes gate 1 with no key. Inventing the taxonomy is a decision, not a procedure |

### FIX — 1

| # | Finding | Source | The repair |
|---|---|---|---|
| 37 | Audit-sink invariant as a named test: when the gate blocks, the raw spec is in **no store, no log, no prompt** | `OTHERS-MINED.md:723` (detail §1.1) | The mined text states the gap exactly: *"We have written the rule and not the test."* One test, named after the invariant, in `BACKLOG.md` — not a decision to make. The invariant it asserts, and the four sinks to check, are stated in `untrusted-text-boundary` §4 so the test has something to be named after |

### DROP — 5

| # | Finding | Source | Reason |
|---|---|---|---|
| 38 | `isInference` — provenance reduced to one enforced bit | `OTHERS-MINED.md:766` | We already have strictly more. `FieldMeta.source` is `stated \| derived \| default` — three values where theirs has two — and it is enforced in `apply_extraction()`, not merely declared. Adopting a bit would be a downgrade |
| 39 | `forgetAfter` + `forgetReason` + `isForgotten` as a forgetting mechanism | `OTHERS-MINED.md:767` | **Retracted by the second pass of our own mining.** `PASS2-FOUR-REPOS.md` §3.1 found `forgetAfter` is read in exactly one place — a border-colour function — and nothing writes `isForgotten`. The vocabulary survives as finding #14; the mechanism was never observed working |
| 40 | Instincts as a store — adopt the record shape, reject the self-reported confidence | `ECC-MINED.md:387` | Both halves are already held. The record shape *is* `FieldMeta`, and the confidence half is already written up, with sources, in `ais-grounding` §3 hazard 3 (*"verbalised confidence is not calibration"*). Nothing new to carry |
| 41 | Preference provenance allowlist, unknown source rejected, exit 2 ≠ exit 1 | `PASS2-GSTACK-TESTS.md:708` | The same finding as #12, stated in a second document — exactly the cross-document duplication `findings-index.py` was built to surface. The one part not in #12 is the exit-code split, which is CLI-shaped; Scio's intake is HTTP and has no exit code to split |
| 42 | *"What scales with simplicity is the artifact, never the approval"* | `OTHERS-MINED.md:742` | True, and already unconditionally true of us: `is_buildable()` has no size exemption and no small-app path. A sentence with no procedure attached, restating an invariant already enforced in code |

---

## 2 · Counts

| Verdict | Count | Share of the 42 |
|---|---|---|
| SKILL | 29 | 69% |
| ADR | 7 | 17% |
| FIX | 1 | 2% |
| DROP | 5 | 12% |

Against the 81 rows actually examined (42 Layer A + 39 mis-bucketed), **36% became skill content**.

The SKILL share of the Layer A set is high, and that is worth saying plainly rather than
presenting as a result: this set was pre-filtered twice before reaching triage — a miner tagged
each row `A` and marked it `take` — so it is a shortlist, not a population. The honest claim is
that 13 of 42 were held back, and that the seven ADRs are the ones a permissive pass would have
smuggled into markdown.

**Six skills carry the 29:** three new (`clarifying-questions`, `provenance-record`,
`untrusted-text-boundary`) and three amended (`ais-grounding`, `ontoagent-elicitation`, `testing`).

---

## 3 · The 39 rows the index attributed to Layer A that belong elsewhere

Not triaged here. Listed so the next pass over each layer finds them rather than re-deriving them.

| Layer | Rows |
|---|---|
| **B / Playbook** | `ECC-SKILLS.md:644`, `ECC-SKILLS.md:646` (with G), `PASS2-ECC-SKILLS.md:644`, `:646`, `:682`, `:683`, `PASS2-GSTACK-SKILLS.md:694`, `ECC-RULES.md:449`, `ECC-RULES.md:513` |
| **C** | `PASS2-GSTACK-TESTS.md:698` (with E), `:699` |
| **D** | `ECC-SKILLS.md:675`, `PASS2-FOUR-REPOS.md:643`, `:656`, `PASS2-GSTACK-SKILLS.md:691`, `PASS2-GSTACK-TESTS.md:718` (with B) |
| **E** | `ECC-AGENTS.md:636`, `:637`, `ECC-SKILLS.md:654`, `PASS2-ECC-RULES-COMMANDS.md:686`, `PASS2-ECC-SKILLS.md:651`, `:655`, `:684`, `PASS2-FOUR-REPOS.md:634`, `PASS2-GSTACK-SKILLS.md:686` (with F), `:702`, `PASS2-GSTACK-TESTS.md:702`, `:721` |
| **F** | `PASS2-GSTACK-SKILLS.md:709`, `:710` |
| **G** | `PASS2-ECC-SKILLS.md:659` (with F), `:669` (with E), `PASS2-GSTACK-TESTS.md:706` (with E) |
| **build process / all seven** | `ECC-MINED.md:383`, `:385`, `:395`, `:397`, `ECC-SKILLS.md:667`, `PASS2-ECC-SKILLS.md:657` (E, F) |

One of these is worth flagging upward rather than filing: `ECC-SKILLS.md:667` — *"every harness
component encodes an assumption about what the model can't do alone; re-test when models
improve"* — is tagged **all seven** and nothing in `docs/next/` says which parts of Scio are 2026
workarounds. It is not Layer A's to spend, and it should not be lost in a per-layer file.
