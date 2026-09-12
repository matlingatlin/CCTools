---
name: ears-requirements
layer: A, C
phase: build-time
status: written
description: Write requirements as constrained natural language using EARS, so each one is addressable, testable and traceable. Use when turning a spec or a narrative into requirements, when a contract needs sentences a system can check, when something must be traceable to "an approved requirement", when writing acceptance criteria, or when reviewing vague requirement prose. Five sentence patterns from Rolls-Royce, standard in aerospace and now in AWS Kiro's spec mode.
---

# ears-requirements

A narrative cannot be traced to. **You cannot point a generated function at a paragraph.** EARS is
the smallest standard way to turn prose into sentences that have identity, a testable shape, and a
grammar a rule can check.

It is five patterns and one keyword each. That is the whole method, and its smallness is the
argument for it.

---

## 1 · Source

**EARS — Easy Approach to Requirements Syntax.** Alistair Mavin, Philip Wilkinson, Adrian Harwood
and Mark Novak, Rolls-Royce plc. First published at the **IEEE International Requirements
Engineering Conference (RE'09)**, 2009. Developed while analysing airworthiness regulations for a
jet-engine control system.

- Official guide: [alistairmavin.com/ears](https://alistairmavin.com/ears/)
- [Wikipedia: Easy Approach to Requirements Syntax](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)
- Widely used in aerospace, automotive and medical devices — domains where a requirement that
  cannot be verified is a certification failure.

**Current relevance.** AWS Kiro's spec-driven development mode uses EARS for its requirements
phase, and GitHub's Spec Kit has [an open request to adopt it](https://github.com/github/spec-kit/issues/1356).
The agent tooling world is converging on the same 2009 syntax.

---

## 2 · Method, in the form we use it

### 2.1 The general form

```
WHILE <optional precondition(s)>, WHEN <optional trigger>,
the <system name> SHALL <system response>
```

### 2.2 The five patterns

| Pattern | Keyword | Shape | Example in this domain |
|---|---|---|---|
| **Ubiquitous** | (none) | The `<system>` shall `<response>` | The app shall store a booking's party size |
| **Event-driven** | **When** | When `<trigger>`, the `<system>` shall `<response>` | When a guest submits a booking, the app shall send a confirmation |
| **State-driven** | **While** | While `<state>`, the `<system>` shall `<response>` | While a booking is held, the app shall reserve the table |
| **Unwanted behaviour** | **If … then** | If `<condition>`, then the `<system>` shall `<response>` | If the table is already booked, then the app shall reject the request and say why |
| **Optional feature** | **Where** | Where `<feature>`, the `<system>` shall `<response>` | Where payments are enabled, the app shall take a deposit at booking |

Patterns compose: a requirement may carry both a `While` precondition and a `When` trigger.

### 2.3 What each requirement carries beyond its sentence

A sentence alone is not enough for traceability. In this system a requirement is an object:

| Field | Why |
|---|---|
| `id` | the thing a generated function, a test, an architecture node and an impact set all point at. Without it, invariant 1 has no target |
| `text` | the EARS sentence |
| `pattern` | which of the five. A rule can check the sentence matches the pattern it claims |
| `grounding` | the spec field(s) the sentence is derived from — nothing may be asserted without one |
| `origin` | `requirement` / `assumption` / `necessity` — did the user say it, did we default it, or does the app kind require it |
| `satisfied_by` | architecture node references. Empty means nothing implements it; a node with no requirement means something unasked-for got built |

### 2.4 Prose stays primary

**The user reads the story, not the list.** EARS makes requirements addressable *behind* the
narrative; it does not replace it. Showing a restaurant owner a numbered SHALL list is a worse
product, and `whole.py`'s own bar — *"accurate before it is elegant"* — is not a licence to be
unreadable. Render the requirements into paragraphs; keep the ids reachable.

### 2.5 What EARS is checkable for

These are rules, not judgement, and they belong beside the other deterministic gates:

- the sentence starts with the keyword its declared pattern requires (or none, for ubiquitous)
- it contains exactly one `shall`
- the system name is the canonical vocabulary term, not a synonym
- it has at least one grounding field
- it contains no conjunction that hides two requirements in one sentence ("and then also")
- it states a response, not a design ("shall send a confirmation", not "shall call SendGrid")

---

## 3 · Limits — what the source shows versus what we would be assuming

**EARS is a syntax, not a method, and it makes no efficacy claim we can lean on.**

| Claim | Status |
|---|---|
| "EARS reduces ambiguity, vagueness and incompleteness" | The authors' stated design intent and the field's accumulated practitioner experience. **RE'09 is not a controlled trial of requirement defect rates.** Treat as convention, not measurement |
| "Standard in aerospace, automotive, medical devices" | Well supported. It is genuinely the house syntax in safety-critical requirements work |
| "AWS Kiro uses EARS" | Reported in Kiro's own documentation and secondary coverage. Not independently verified here |

**Assumptions this skill makes that EARS itself does not support:**

1. **EARS was designed for human-authored requirements about engineered systems.** Using it for
   sentences a model generates from a conversation is a transfer nobody has evaluated. The failure
   mode to watch for: a model producing syntactically valid SHALL sentences that are ungrounded —
   the syntax makes bad requirements look rigorous.
2. **EARS says nothing about traceability, ids, or provenance.** Every field in §2.3 except `text`
   and `pattern` is ours. Do not present the whole object as "the EARS format".
3. **EARS was built for systems with clear state and triggers.** A CRUD web app has weaker state
   semantics than a jet-engine controller; the `While` pattern may be used less than the others, and
   forcing it produces contortions.

**The honesty rule:** a skill may not claim more than its source shows. EARS is adopted here
because it is small, standard, checkable and free — **not** because a study showed it improves
anything about generated apps. Nobody has run that study.

---

## 4 · Eval

### E1 · Pattern conformance
Given a set of generated requirements, assert every one matches the grammar of its declared
pattern. A sentence declaring `event_driven` that does not begin with "When" fails.

### E2 · One shall
Assert exactly one `shall` per requirement. Two means two requirements.

### E3 · Grounding coverage
Assert every requirement names at least one spec field. A requirement with empty grounding is an
unsupported claim in a contract the user is about to sign — it must fail, not warn.

### E4 · Canonical vocabulary
Assert the entity nouns in each sentence are canonical terms (`booking`, not `reservation`). Round
the sentence through `vocabulary.canonical_name` and compare.

### E5 · No design in the response clause
Assert the response names an observable behaviour, not an implementation. Heuristic: reject
responses containing a library, vendor or file name. Imperfect; it catches the common case.

### E6 · Bidirectional coverage
Assert (a) every requirement has at least one `satisfied_by` node, and (b) every architecture node
traces to a requirement id or carries `origin = assumption` or `origin = necessity`. Either
direction failing is an invariant-1 violation, and they fail for different reasons: (a) means
something was promised and not built, (b) means something was built and not asked for.

### E7 · Readability is preserved
Assert the narrative shown at the spec gate is prose, not a rendered SHALL list. This eval exists
because the most likely way to get EARS wrong here is to succeed at it and ship a worse product.

---

## 5 · When this skill is the wrong tool

- **Exploratory conversation.** EARS is for the contract, not the interview. Constraining a user's
  own words into SHALL sentences mid-conversation is the opposite of momentum.
- **Non-goals.** "No payments for now" is a scope statement, not a requirement. Do not force it
  into a pattern.
- **Quality attributes.** "It should feel fast" is a quality attribute and belongs in a trade-off
  discussion (see ATAM vocabulary), not in a SHALL sentence with an invented threshold.

---

## 6 · Layer C: the same patterns as a package's acceptance criteria

Added 2026-08-26 while writing `docs/next/LAYER-C-BUILD-PLAN.md` §3.3. Everything above holds;
this section is the one place where the transfer is *tighter* than §3's caveats suggest, and it
is worth recording because it is an argument from mechanism rather than from convention.

**The clause slots map one-to-one onto machinery `layerc/scripts.py` already has.** A build
package's "done when" is checked by a deterministic script, not by reading — so:

| EARS clause | Scio mechanism today |
|---|---|
| `WHILE <precondition>` | `as_user(ALICE)` (`scripts.py:181`); `arch.auth_access.mode` |
| `WHEN <trigger>` | `fill(...)` + `click(...)` (`scripts.py:118`, `:184`) |
| `SHALL <response>` | `assert_present` / `assert_absent` / `assert_row` |
| `IF … THEN` (unwanted behaviour) | the negative assertion — the half hand-written criteria omit |
| `WHERE <feature>` | the refusal conditions: no owner column ⇒ no isolation criterion |

**A criterion in EARS is structurally closer to a `Script` than a sentence is.** That is the
adoption argument at this layer, and unlike "it reduces ambiguity" it is checkable.

**Four authoring rules on top of §2's:**

1. One `SHALL` per criterion (§4 E2 already asserts it). Two independently-failing responses are
   two criteria.
2. **Name the system as the package, not the app.** `the booking feature SHALL…`, never `the app
   SHALL…` — a criterion whose subject is the whole app cannot be owned by one package, and
   `_check_contracts` (`layerc/validate.py:94`) cannot attribute it.
3. **EARS does not replace `produced_by` and `observed_by`** (`layerc/criteria.py:67`). It
   replaces the prose. A criterion still declares which planned file makes it true and which
   channel can see it.
4. **Rewriting never changes observability.** If no channel can observe the response, the
   criterion stays `Observability.unsupported` and never gates a build. Making an unobservable
   criterion *sound* rigorous is the specific failure §3's assumption 1 warns about.

### Two more evals, for this use

**E8 · Rewriting is observability-preserving.** Take Scio's current criteria, rewrite each in
EARS, and assert `observed_by` is unchanged and `cover()` returns the same
`produced`/`observable` pair. A rewrite that turns a warning into a gate is a failure of the
skill, not a success.

**E9 · Refusal.** *"The code is clean and well structured"* has no observable response. The skill
must return **not expressible as a criterion** rather than inventing a `SHALL`. This is the
single most likely way to misuse EARS here.

---

*Scanned and written 2026-08-26. Source read at method level; no reproduction and no efficacy
study behind the adoption. §6 added while writing Layer C's document; its clause↔mechanism table
is ours, not the paper's.*
