# Layer A · Intake — what to build next

Forward-looking. What `docs/as-built/LAYER-A-INTAKE.md` describes is the starting point; this
is what to do with it.

Nothing here is decided. Anything that changes behaviour becomes an ADR proposal (§9).

**Method.** Every domain this layer touches was searched before anything was proposed:
requirements elicitation, dialogue state tracking, provenance, structured generation,
statecharts, survey methodology, and the app-builder field itself. Where a standard, a
benchmark or a published protocol already covers something, it is cited and adopted rather
than re-invented. The failure this rule exists to avoid is on record: the first draft of the
design skill invented a token format while the W3C DTCG module already existed. **This
document retracts two inventions from its own previous draft** — a made-up coverage formula
(§2.6) and a made-up metric set (§3.4).

---

## 1 · Where Layer A stands

Conversation → typed spec. One turn is four ordered operations: extract → detect
contradictions → ask the gate → write the next question (`intake/service.py::run_intake_step`).

**Correction to the previous draft: a turn is three model calls, not two.**
`run_intake_step` defaults to `extraction_passes=2`, and `plan_models`
(`execution/narration.py::plan_models`) with two passes returns `[models[0], models[0]]` — so
extraction is Claude Opus 5 drafting, then Claude Opus 5 reviewing its own draft, with the
*entire original prompt re-sent* alongside the first answer (`execution/relay.py::_build_messages`).
The question call is a third. Nothing measures whether pass 2 ever changes the extraction
(§7.4).

Second correction: `temperature=0.0` at `intake/extraction.py:321` is a no-op on the default
path. `execution/provider.py` deliberately does not send `temperature` to Anthropic, with the
reason in a comment — current Claude models reject sampling parameters. Determinism here comes
from the instruction, not the knob.

Solid and worth keeping: per-field provenance, the buildable-enough gate, downstream tags,
corrections, contradiction detection by rules, the WHICH/HOW split. Verified today:
`pytest -k intake` → **67 passed**.

The constraint that governs every proposal below, from `intake/questions.py`:

> The gate is *"deterministic, reproducible, free, and impossible for a model to talk its way
> past."* Only the wording goes to the relay.

**Any change that lets the model decide which required field gets asked is out of scope.**
Proposals may *add* questions; they may not let the model *skip* one.

### 1.1 What the review findings add

Five things, none of which the layer documents surfaced on their own.

**a. The fence stops at the layer boundary, and it stops inside this layer first.**
`C-F14` records *"Layer B/C tar emot spec-fältvärden ofenced"*. That chain is verifiable:
`intake/extraction.py:285` wraps the transcript in `fence('the conversation', …)` and
`EXTRACTION_SYSTEM` carries `untrusted.INSTRUCTION` — but `_field_prompt`
(`intake/questions.py:130`) and `_contradiction_prompt` (`:143`) paste
`conversation.as_prompt()` raw, and `QUESTION_SYSTEM` has no `INSTRUCTION` at all. The same
untrusted text, in the same turn, in the same layer, fenced once and not the other time. Then
`_merge_list` (`extraction.py:142`) keeps *"the user's own wording"* by design, and
`layerb/whole.py:95` interpolates those values into a prompt with no fence. There is a test
for the fenced half — `test_the_conversation_is_quoted_rather_than_pasted`
(`tests/test_prompt_injection.py:65`) — and none for the other. The review's own caveat
stands: *"Inget test bevisar att en riktig modell motstår en riktig injektion."*

**b. The reviews already graded this layer, at P1.** `PRODUCTION_READINESS_DIFF.md:110`:

> Kravinsamling · Nuläge: strukturerad intake finns · Önskat: stabil dialog som täcker
> relevanta krav utan onödig friktion · Gap: **verifiera med riktiga användare och varierade
> appar** · P1

Two words matter: *riktiga* and *varierade*. Real users, and varied apps. That is the review
pre-empting both of this document's biggest proposals — a simulated harness (§3.4) is not what
it asked for, and one app kind (§3.1) is not what it asked for.

**c. Two product invariants need something Layer A does not mint.** `DIFF` §2 invariant 1 —
*"Inget byggs utan kontrakt: varje funktion ska kunna spåras till ett godkänt krav"* — and §7's
reveal spec — *"krav uppfyllda/ej uppfyllda"* — both require a **stable requirement identity**.
Layer A produces named *fields*, not identified *requirements*. `key_actions` is one field
holding a list of five things a build can half-satisfy, and nothing downstream can say
*"requirement 3 is unmet"* because requirement 3 does not exist as an object (§3.2).

**d. The corpus is blocked, not merely unbuilt.** `C-F12 / G-F13` (deletion and retention) is
verified *partly*, and ADR-0019 which governs it is still **Proposed**. §8 cannot start.

**e. Our own baseline is one observation.** `B105` records `design.test.tsx` failing on two
consecutive runs and passing on three later ones. The 67 above is one run today. Any harness
this layer builds inherits that epistemic problem and must report variance, not a number.

---

## 2 · Refining what exists

### 2.1 Stop hand-rolling JSON extraction — the API has a grammar

`_extract_json` (`intake/extraction.py:87`) is a regex that hunts for a fenced block, falls
back to first-`{`-to-last-`}`, and gives up with `parsed: False`. `_parse`
(`intake/questions.py:76`) is the same shape again. Both exist to survive a model that
wandered outside the requested JSON.

**Claude's structured outputs remove the failure rather than handling it.** `output_config.format`
with a JSON schema compiles the schema into a formal grammar and constrains generation token by
token — the model cannot emit a character that breaks the schema
([docs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)). `AppSpec`,
`FieldMeta` and the proposal shape are already Pydantic, so the schema is already written.

| Option | Verdict |
|---|---|
| **Anthropic `output_config.format`** — native, no dependency, grammar-constrained | **adopt** for the Anthropic path |
| **Instructor** (~3M downloads/mo) — Pydantic + validate-and-retry, post-hoc | not needed; retries what the grammar prevents |
| **BAML** — a DSL for LLM functions, own compiler, own file type | not for this layer; a second prompt language beside the relay is a large surface for one call site |
| **Outlines / XGrammar / llguidance** — constrained decoding engines | not applicable; we do not host the decoder |

Two costs to name honestly. First-use grammar compilation adds latency, then the compiled
grammar is cached ~24h — so a schema that changes per request would pay it every time; ours
does not. And the relay is multi-vendor by construction (`matrix.yaml` ranks `gpt-5` and
`gemini-2.5-pro` behind Opus for `spec_extraction`), so the regex path stays as the fallback
for vendors without an equivalent. **This is a `RelayOptions` field, not an intake change** —
which makes it a cross-layer refinement that happens to be discovered here.

### 2.2 Effort and model routing per call type — using the real parameter

The previous draft proposed `effort: high` / `effort: low`. The actual parameter is
`output_config.effort` (`low | medium | high | xhigh | max`, default `high`), and it is
**absent from `RelayOptions` entirely** (`execution/relay.py:43`) and never sent by
`execution/provider.py`. So this is not a setting to flip; it is a knob to add.

The routing question is sharper, and it is already half-solved in the repo. Both calls pass the
task name `"spec_extraction"` (`extraction.py:317`, `questions.py:177`), whose ranking in
`matrix.yaml` is `[claude-opus-5, gpt-5, gemini-2.5-pro]`. So **a one-sentence question with a
deterministic fallback runs on the most expensive model in the matrix.** A `light_edit` task
already exists, ranked `[claude-haiku-4-5, claude-sonnet-5, claude-opus-5]`. The change at
`questions.py:177` is one string.

| Call | Job | Failure mode | Proposal |
|---|---|---|---|
| Extraction | typed extraction under grounding rules | wrong app gets built, silently | strongest model, `effort: xhigh` |
| Question wording | one sentence, guide fallback, `written_by` records which fired | visible and caught | `light_edit`, low effort |

Measured over a ten-turn conversation (§7.2): the question calls cost **$0.065 on Opus 5 and
$0.013 on Haiku 4.5**.

**The trade nobody would guess:** Claude Opus 5's minimum cacheable prefix is **512 tokens**;
Haiku 4.5's is **4,096**. Routing the question call to Haiku forecloses ever caching it. The
question prompt reaches ~830 tokens by turn 10 — comfortably cacheable on Opus, never cacheable
on Haiku. Cheaper per token, and structurally uncacheable. Sonnet 5 at 1,024 splits the
difference. **This is a decision, not an optimisation.**

### 2.3 Fence the question prompt

Two lines (`questions.py:130`, `:143`) and one string append to `QUESTION_SYSTEM`. It closes
half of `C-F14`'s Layer-A surface and costs ~87 tokens. The test that already exists for
extraction gives the exact shape of the one to write.

### 2.4 Let the extractor see its own rejections — without invalidating the cache

`ExtractionReport.rejected` is returned and discarded. Feeding last turn's rejections back —
*"you claimed X without provenance; do not repeat it"* — targets the exact failure the rules
already detect.

The obvious implementation is wrong. Appending them to `EXTRACTION_SYSTEM` changes the system
prompt every turn and destroys the cache prefix (§7.3). The right channel is a
**mid-conversation system message**: `{"role": "system", …}` appended to `messages[]`, supported
on Claude Opus 5 with no beta header, designed precisely to carry operator instructions without
touching the cached prefix. `execution/provider.py:170` currently folds every `role == "system"`
message into the top-level `system` string, so this needs a provider change, not a prompt change.

### 2.5 Make the example concrete instead of canned

Every question carries an example from a static guide (`intake/fields.py::GUIDES`). The same
example — *"Bookings, tables, guests"* — goes to a restaurant owner and to a logistics startup.
The guide was written with booking in mind, so every other app gets a mismatched example.

This is no longer only an aesthetic argument. ReqElicitGym reports that elicitation performance
**varies significantly across application domains** ([arXiv 2602.18306](https://arxiv.org/html/2602.18306)),
which is what §3.1 exists to exploit. Kept as a refinement, now with a reason.

### 2.6 Replace the boolean with a standard, not with a formula

`is_buildable()` (`intake/gate.py:62`) returns a boolean. `BuildableResult` already carries
`missing_core`, `unresolved_conditionals` and `contradictions`, so the information exists — the
*summary* is lossy.

**The previous draft proposed `area_score = (stated·1.0 + derived·0.6 + default·0.2) / n`.
Retracted.** Those weights were invented, they are unfalsifiable, and a number a user can
haggle with is worse than a list they can act on.

**ISO/IEC/IEEE 29148:2018** already defines what a good requirement is: *necessary,
implementation-free, unambiguous, consistent, complete, singular, feasible, traceable,
verifiable, affordable, bounded*
([ISO](https://www.iso.org/standard/72089.html)). Layer A currently checks exactly one of
these — *complete* — and calls the answer `buildable`. At least four more are free:

| 29148 characteristic | Already computable from |
|---|---|
| **complete** | `missing_core`, `unresolved_conditionals` — today's gate |
| **consistent** | `contradictions.detect()` — already runs, already blocks |
| **traceable** | `FieldMeta.provenance` — already enforced in code |
| **singular** | `QUESTION_SYSTEM`'s *"never two questions at once"* — enforced only by prompt today |
| **unambiguous** | the placeholder rejection in `_clean_text` is a crude first version |

Keep the boolean for the gate. Beside it, return a **29148 vector** — a named characteristic
with a named failing field, not a percentage. *"Traceable: 4 of 6 core fields cite a message"*
is actionable; *"data 90%"* is not.

---

## 3 · What is missing

### 3.1 App-kind detection — and a taxonomy that already exists

Today every app walks the same six fields in the same order. A tender platform and a restaurant
booking app are asked identical questions.

**Do not invent the taxonomy.** Two exist:

- **ReqElicitGym's ten application types** — showcase site, community platform, e-commerce,
  learning platform, entertainment app, dashboard, enterprise management, publishing platform,
  job search, productivity tool. Derived from 101 annotated elicitation scenarios, and *the
  benchmark reports results per type*, so adopting it means our numbers are comparable to a
  published baseline.
- **schema.org `applicationCategory`** — 23 values, a stable public vocabulary
  ([schema.org](https://schema.org/applicationCategory)). Wrong grain for elicitation (it
  classifies *what an app is for*, not *what it needs asked*), but the right thing to *emit*
  when a spec leaves the system.

Proposal: classify with ReqElicitGym's ten internally, map to `applicationCategory` at the
boundary. Use the class to select examples (§2.5), pre-arm conditional triggers, and later seed
defaults from the corpus (§8).

**Guarantee preserved:** kind detection may only *add* conditionals and *change wording*. It may
never remove a core field or reorder the gate. A wrong class then costs one irrelevant follow-up,
not a missing requirement.

This is where OntoAgent lands without giving the model control of sequencing: ScoreOnto /
ReRankOnto prioritise *which concerns are relevant to this domain*
([arXiv 2605.05828](https://arxiv.org/abs/2605.05828)), and here that only ever expands the
conditional set. Their GatePrune — which drops concerns — is the half we do not take.

### 3.2 Requirement identity — the smallest change with the widest reach

Invariant 1 and the reveal spec (§1.1c) both need a requirement to be a *thing*, not a field
name. Today `key_actions` is one `FieldMeta` holding *"Book a table, cancel a booking, staff see
today's list"* — three requirements in one slot, with one shared provenance list, one shared
confidence, and no id.

The minimum viable version: when a list-valued field is extracted, each item gets a stable id
and carries its own provenance. Everything downstream that currently says *"traceable to
`key_actions`"* can then say *"traceable to `A-key_actions-3`"* — which is what impact analysis
(Layer B §3.1), the reveal's met/unmet list, and the failure loop (§3.5) all need.

**A downstream consumer already exists in written form.** The `ears-requirements` skill models a
requirement as an object with `id`, `text`, `pattern`, **`grounding` — the spec field(s) the
sentence is derived from** — and `origin`. Without per-item ids, `grounding` can only ever point
at `key_actions`: one field holding three requirements, so three EARS sentences share one
citation and none of them can be individually traced, satisfied or invalidated. **A-8 is the
thing that makes that skill's `grounding` field mean something.**

**Where the standard is, and where it is not.** For the *shape* of a provenance record, the
**W3C PROV** family is the DTCG-equivalent here: `prov:Entity` / `prov:Activity` / `prov:Agent`
with `wasGeneratedBy`, `used`, `wasAttributedTo`, and a **PROV-JSONLD** serialisation
([PROV-O](https://www.w3.org/TR/prov-o/) · [PROV-JSONLD](https://www.w3.org/submissions/prov-jsonld/)).
`FieldMeta{value, source, confidence, provenance}` is a lossy special case of it — `source`
is `prov:wasAttributedTo` (the user vs. the extractor), `provenance` is `used`.

**Honest verdict: adopt the vocabulary at the export boundary, not internally.** PROV is RDF; a
Pydantic engine that swallows an OWL ontology to describe six fields has bought ceremony. But
ADR-0001 sells *code the user owns with a smooth handoff* — and a spec that exports its
provenance in a 2013 W3C Recommendation rather than our own JSON is the same argument that made
DTCG the right answer for tokens.

### 3.3 Style is structurally never elicited — and that is measured, not suspected

ReqElicitGym breaks elicitation down by requirement aspect — **Interaction, Content, Style** —
and reports a *"structural weakness: style-related requirements elicitation rate near zero"*
across every model tested.

Scio has the same hole, by construction and independently:

- `look` is **not in `EXTRACTABLE_FIELDS`** (`intake/fields.py:133`). Extraction may not fill
  it. Ever.
- It ships as a flagged default: `FieldMeta(value="Scio default", source=default)`.
- Its downstream tag is `design_tokens` — it feeds the design system, which the `app-design`
  skill argues is the difference between an app that looks designed and one that looks generated.
- Layer F's design window is where the user finally gets to say it, *after* the build.

Two independent lines of evidence converge on the same defect. The exclusion of `look` from
extraction was a *deliberate* choice — the comment says letting extraction fill a defaulted
field would erase the honest "assumed" tag — and it is right about that and wrong about the
consequence. The fix is not to let extraction overwrite it; it is to make **style a thing that
gets asked**, with its answer marked `stated` like any other.

This is the single strongest new finding in this document, and it is cheap: one field moves from
"defaulted, silent" to "defaulted, and asked once when the kind suggests it matters".

### 3.4 A replay harness — built on a published protocol, not an invented one

Nothing measures Layer A, so nothing can be shown to improve it. **The previous draft invented
five metrics.** Retracted; three published ones exist, from ReqElicitGym
([code](https://github.com/jdm4pku/ReqElicitBench)):

| Metric | Definition | Maps to |
|---|---|---|
| **IRE** — Implicit Requirements Elicitation ratio | elicited ÷ ground-truth requirements | how much Layer C has to invent |
| **ESR** — Effective Strategy Ratio | share of probe/clarify turns that elicit ≥1 requirement | wasted questions |
| **TKQR** — Turn-discounted Key Question Rate | nDCG-style; rewards asking the critical question early | *momentum over completeness*, made numeric |
| **ORA** — optimal-round assessment | in the repo, not the paper | turns-to-buildable |

The oracle-user protocol is the part worth copying exactly: responses grounded **only** in
annotated implicit requirements, **passive disclosure** unless asked, context-aware across the
dialogue. Validated against 33 real interviews at Cohen's κ = 0.73. That is a specification for
`StandInIntakeProvider`'s successor.

Three Scio-specific metrics stay, because no benchmark has them:

| Metric | From |
|---|---|
| assumed rate at the gate | `source == default` |
| misfile rate | corrections that move a value between fields |
| contradictions caught vs planted | `contradictions.detect()` |

**The baseline to beat is the published one: best model IRE = 0.32.** Not our stand-in. A
change that does not move a named metric is an expense.

**The limit, stated up front.** *"Lost in Simulation"* ([arXiv 2601.17087](https://arxiv.org/pdf/2601.17087))
argues LLM-simulated users systematically diverge from humans; the τ-bench line calls the
failure **benevolence bias** — simulators are too cooperative to be representative. `DIFF:110`
independently demands *"riktiga användare"*. So: **the harness is a regression detector, not
evidence the dialogue is good.** It answers *"did this change make it worse?"* It does not
answer *"is this good?"* Anyone who conflates the two has mis-sold it.

### 3.5 The loop back from failure

Corrections are captured at review time only. When a build fails three stages later, nothing
walks the chain back to the intake field that caused it — even though `source_field` on every
architecture node makes it traceable in principle. Cheapest first version: on a failed build
gate, record which architecture nodes were implicated and which `source_field` they trace to.
§3.2's ids are what make that a join rather than a guess. This is a dataset (§8), not yet a
feature.

### 3.6 The moment the gate opens

Still undocumented, still unsettled. Does the conversation hard-stop when `is_buildable()` turns
true, or may the user keep talking? `run_intake_step` returns `next_question: None` and
`done: True`, and what the UI does with that is not written down anywhere. It decides whether
*momentum over completeness* is a floor or a ceiling — and it is the difference between a wizard
that respects the user's time and one that cuts them off mid-thought.

---

## 4 · Out of the box — the wide brainstorm

### 4.1 Elicit by proposing, not by asking

Every question today is a blank. **GATE** — *Eliciting Human Preferences with Language Models*,
Li, Tamkin, Peng, Andreas (MIT CSAIL), ICLR 2025 —
[arXiv 2310.11589](https://arxiv.org/abs/2310.11589) — reframes elicitation as the model
*generating* candidate specifications and edge cases for the user to accept or reject, and
reports that users found this **less effortful than prompting** and that it **surfaced
considerations they had not anticipated**.

The applied form here: once §8's corpus exists, open with a draft — *"apps like yours usually
manage bookings, tables and guests, sign in by email link, and don't take payment. Correct me."*
A "no" is cheaper for a user to produce than a paragraph, and it is *more* informative per token
than a vague answer to an open question.

**This does not touch the gate.** A correction to a proposal is still evidence, still gets
`provenance`, and the gate still decides what remains unanswered. It changes the *shape of the
turn*, not who decides.

### 4.2 The conversation as a statechart — and why not yet

Named for completeness, because it is the pattern an architect would reach for. **W3C SCXML**
is a Recommendation (2015), built on Harel statecharts, and was selected by the W3C as the basis
for multimodal dialogue systems ([W3C](https://www.w3.org/TR/scxml/)); **XState** is the
JavaScript implementation, and SCXML↔XState round-tripping exists.

**Verdict: not for this layer.** Six fields walked in a fixed order is a `for` loop
(`questions.py::next_target`, twelve lines). A statechart earns its place when there are
parallel regions, history states and guarded transitions — which is a description of Layer F's
mark→regenerate→approve loop, not of a wizard. Adopting it here would be pattern-fitting.

Worth revisiting if §3.1 lands and conditionals start branching on kind.

### 4.3 Speculation: this layer is doing survey design badly

**Marked as speculation.** No evidence from our system supports it yet; it is offered because it
predicts specific, testable things.

Layer A is a questionnaire administered by an interviewer. That is a mature discipline with
sixty years of findings, and the relevant one is **satisficing** — Krosnick's model that
respondents minimise cognitive effort and give the first merely-acceptable answer, with
likelihood set by task difficulty, respondent ability and respondent motivation
([Krosnick & Presser, Handbook of Survey Research](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2010/2010%20Handbook%20of%20Survey%20Research.pdf)).
Its diagnostic signs — don't-know responses, non-differentiation, mental coin-flipping — are
exactly what a vague intake answer looks like.

Three predictions this makes, all measurable by §3.4:

1. **Answer quality decays with turn index**, independent of question difficulty. If true, the
   fixed order is costing us on whatever is asked last — and `non_goals` is asked after all six
   core fields (`next_target`, `questions.py:56`).
2. **`data_ownership_sensitivity` is the highest-difficulty question in the set** and should be
   worst-answered. It asks a non-technical person to classify data.
3. **Question-order effects are real here.** Asking `entities` before `key_actions` should
   produce different `key_actions` than the reverse.

Independent support that the *medium* is right: conversational and chatbot-administered surveys
consistently report **reduced satisficing** and more informative open-ended responses than web
forms ([AI-Assisted Conversational Interviewing, arXiv 2504.13908](https://arxiv.org/abs/2504.13908);
[CHI 2025 interview-probe comparison](https://dl.acm.org/doi/full/10.1145/3706598.3714128)). So
the conversation is the right container. What is unexamined is what we put in it.

### 4.4 EARS, Volere, and the half of Kiro not worth copying

**EARS** (Easy Approach to Requirements Syntax, Mavin et al., Rolls-Royce, RE'09) constrains a
requirement to `WHILE <precondition>, WHEN <trigger>, the <system> SHALL <response>`, in five
patterns ([alistairmavin.com/ears](https://alistairmavin.com/ears/)). **AWS Kiro already
generates `requirements.md` in EARS notation from a prompt** ([kiro.dev](https://kiro.dev/docs/specs/feature-specs/)),
and GitHub's spec-kit has an open request for it.

**So EARS is table stakes, not a differentiator** — the same lesson §8 of the review taught about
component libraries. What Kiro's `requirements.md` does *not* have is provenance: nothing in it
distinguishes what the user said from what the tool assumed. That distinction is enforced in
Scio's code, with tests. **That is the differentiator, and it is already built.**

The more interesting borrow is **Volere**'s requirement shell and its **fit criterion** — every
requirement carries the benchmark that decides whether it was met
([volere.org](https://www.volere.org/templates/volere-requirements-specification-template/)).
Pair that with §3.2's ids and the reveal's *"krav uppfyllda/ej uppfyllda"* stops being a wish:
each requirement arrives with its own test.

Speculative and mine: EARS is the right *output* format at the Layer A→B boundary and the wrong
*conversation* format. Nobody says *"WHEN a guest submits the form, the system SHALL…"* to a
chatbot. Layer A collects in the user's words and emits in EARS — which is exactly the WHICH/HOW
split applied to notation. The `ears-requirements` skill (written for the layers below this one)
reaches the same conclusion from the other end: *"prose stays primary… render the requirements
into paragraphs; keep the ids reachable."* The two documents agree, arrived at independently,
which is the closest thing to corroboration available here.

### 4.5 The corpus has a name: case-based reasoning

§8's *"apps like this one usually need X"* is not a new idea needing a new mechanism. It is
**CBR**, and Aamodt & Plaza's cycle — **Retrieve, Reuse, Revise, Retain** (1994) — maps onto it
exactly: retrieve similar past specs, reuse their field values as a draft, let the user revise
(§4.1's correction), retain the corrected spec. There is a 2025 survey of CBR for LLM agents
([arXiv 2504.06943](https://arxiv.org/html/2504.06943v2)).

Naming it matters because CBR also names the failure modes: retrieval by surface similarity when
the deep structure differs, and a case base that entrenches its own early mistakes. **A corpus
of fifty booking apps makes booking apps better and every other kind worse**, unless retrieval is
measured against IRE per app kind.

### 4.6 MCP has a capability literally called elicitation

The MCP spec defines `elicitation/create`: a server sends a **JSON Schema** describing fields it
needs, the client renders a form, the user's answer returns as structured data
([spec](https://modelcontextprotocol.io/specification/draft/client/elicitation)). The 2026-07-28
revision moves it to Multi Round-Trip Requests so it survives a stateless protocol.

**Not for this layer today** — Scio is the thing asking, not an MCP server being asked. But the
shape is the same as `FieldGuide` + `guide.shape`, and if intake is ever exposed to another agent
(*"build me an app"* from a coding assistant), this is the protocol it should speak rather than a
bespoke HTTP endpoint. Filed as *later*, with the reason.

---

## 5 · The means: what exists already

| Thing | What it gives Layer A | Verdict |
|---|---|---|
| **[Claude structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)** — `output_config.format`, schema→grammar | deletes `_extract_json`/`_parse` and the `parsed: False` path | **adopt** (§2.1) |
| **`output_config.effort`** + `matrix.yaml`'s existing `light_edit` task | per-call cost/quality routing with no new machinery | **adopt** (§2.2) |
| **[Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)** — 512-token floor on Opus 5 | −60% input tokens, no behaviour change | **adopt** (§7.3) |
| **Mid-conversation system messages** (Opus 5, no beta) | rejection feedback without breaking the cache prefix | **adopt** (§2.4) |
| **[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)** — 11 characteristics of a good requirement | the gate's richer sibling, standard-shaped | **adopt** the vocabulary (§2.6) |
| **[ReqElicitGym / ReqElicitBench](https://github.com/jdm4pku/ReqElicitBench)** — 101 scenarios, 10 app types, IRE/ESR/TKQR/ORA, validated oracle-user | the harness, the taxonomy and a published baseline (IRE 0.32) | **adopt** the protocol and metrics; **do not vendor the data — the repo has no licence file** |
| **[OntoAgent](https://arxiv.org/abs/2605.05828)** — ParseUser→ScoreOnto→ReRankOnto→GatePrune | concern-relevance per domain, in additive form only | **adopt** partially (§3.1); GatePrune refused |
| **[GATE](https://arxiv.org/abs/2310.11589)** — MIT CSAIL, ICLR 2025 | elicit by proposing; less user effort, surfaces the unanticipated | **adopt** as §4.1, after the corpus |
| **[W3C PROV-O / PROV-JSONLD](https://www.w3.org/TR/prov-o/)** | the standard vocabulary our `FieldMeta` is a special case of | **adopt at the export boundary** (§3.2); not internally |
| **[EARS](https://alistairmavin.com/ears/)** | constrained requirement syntax; Kiro ships it | **adopted already**, below this layer — see `.claude/skills/ears-requirements`. For Layer A: right for the A→B emit format, wrong for the conversation |
| **[Volere shell + fit criterion](https://www.volere.org/templates/volere-requirements-specification-template/)** | every requirement carries its own acceptance test | **later** — needs §3.2's ids first |
| **[schema.org `applicationCategory`](https://schema.org/applicationCategory)** | 23-value public vocabulary for app kind | **later** — emit at the boundary, not classify with it |
| **[AIS / AutoAIS](https://arxiv.org/abs/2112.12870)** (Rashkin et al., Google, CL 2023) | the published criterion our grounding rule already implements, plus its NLI-based automatic check | **adopt** as the harness's grounding metric (A-2) |
| **[DECODE](https://parl.ai/projects/contradiction/)** — dialogue contradiction detection | an eval set for `contradictions.detect()`'s recall | **later** — useful once the rule set grows past four rules |
| **[SGD / SGD-X](https://research.google/blog/introducing-the-schema-guided-dialogue-dataset-for-conversational-assistants/)** — schema-guided DST, 20k dialogues | zero-shot slot filling from natural-language slot descriptions; `field_catalogue()` is exactly this pattern, arrived at independently | **not for this layer** — validation that our design is standard, not a dependency |
| **[MCP elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation)** | JSON-Schema-driven structured asks, form and URL modes | **later** — only if intake is exposed to other agents |
| **[SCXML](https://www.w3.org/TR/scxml/) / XState** | statechart dialogue management, W3C Recommendation | **not for this layer** — a fixed six-field order is a for-loop |
| **Instructor / BAML / Outlines / XGrammar** | structured-output wrappers and decoders | **not for this layer** — native structured outputs cover it without a dependency |
| **DSPy** (`stanfordnlp/dspy`, MIT) | optimise question selection against a metric | **later — strictly after §3.4.** Without a metric it buys ceremony |
| **[Kiro](https://kiro.dev/docs/specs/feature-specs/) · [spec-kit](https://github.com/github/spec-kit) + its MCP servers** | competitor precedent: prompt → EARS requirements → design → tasks | **not a dependency** — competitive evidence that the *format* is commodity and the *provenance* is not |
| **Replit Agent's clarifying questions** | the only 2026 builder a reviewer says *"treated the vague description as vague"* | competitive evidence: asking is a differentiator users notice |
| **Context7** | live docs lookup to sanity-check a named integration | **later** — only once §3.1 pre-arms `integrations` |
| **graphify** | corpus → queryable graph | **later** — nothing to graph until §8 exists |

Read at abstract-to-method level unless a line says otherwise. ReqElicitBench was fetched and its
contents confirmed; nothing here was reproduced.

### 5.1 The papers that became skills, and the one that did not

`docs/next/SKILLS.md`: *"Every paper we actually adopt becomes a skill. Not every paper we read
— only the ones a design decision rests on. A skill for a paper nobody used is inventory, not
knowledge."* Applied literally:

| Skill | The proposal that rests on it |
|---|---|
| **`.claude/skills/req-elicit-gym`** | **A-2** (metrics, oracle protocol, the "regression detector not quality evidence" clause), **A-6** (the ten-type taxonomy), **A-7** (the style finding). Carries *Lost in Simulation* and benevolence bias as its Limits section, because that is what stops the numbers being over-claimed |
| **`.claude/skills/ontoagent-elicitation`** | **A-6**. Takes ScoreOnto additively, refuses ReRankOnto and GatePrune in writing, and records that **the paper never ablates ScoreOnto** — so the +33% may belong entirely to the two stages we decline |
| **`.claude/skills/ais-grounding`** | **A-2**'s grounding metric. Names the failure today's rule cannot catch: a citation that exists but does not support the claim |

**GATE (§4.1) deliberately gets no skill.** It is the best idea in §4 and no ADR proposal rests
on it — the corpus it needs is blocked behind ADR-0019. Writing one now would be inventory.
Write it the day A-10 unblocks.

**EARS gets no new skill either**, for the opposite reason: `.claude/skills/ears-requirements`
already exists, written for the layers below this one — Layer C folded its acceptance-criteria
half into that same skill (§6 there) rather than shipping a second EARS skill. A-8 is written to
feed it rather than to duplicate it.

---

## 6 · Retrieval versus packing

**Where does this layer pack context it could query instead?**

Measured, per turn (§7.2): the full transcript is packed **three times** — extraction pass 1,
extraction pass 2 (which re-sends the original prompt verbatim alongside pass 1's answer), and
the question call. On top of that, `_filled_summary` (`extraction.py:293`) re-lists every filled
field, and those values are already present in the transcript that sits above them.

**The honest answer is that packing is correct here and caching is the fix, not retrieval.** The
conversation is small (~830 tokens of transcript by turn 10), entirely relevant, and there is no
external corpus to query. Retrieval over ten messages is a lookup that costs more than the
lookup saves.

Two qualifications:

- **The duplication is measurable, so measure it before removing it.** `_filled_summary`'s
  restatement may be earning its keep as a structured anchor against a prose transcript, or it
  may be 80 wasted tokens a turn. §3.4 can tell the difference by ablation. Do not delete it on
  aesthetics.
- **Pass 2 is the largest packing decision in the layer, and it is unexamined.** It doubles
  extraction input to have Opus review Opus. That may be worth it — self-review is where
  over-eager extraction gets caught, per the docstring — but the belief is untested.

**This changes the moment §8 exists.** A corpus of past specs *is* a corpus, and *"apps like this
one usually need X"* is a retrieval question over it — CBR's Retrieve step (§4.5), which is
graphify's shape. graphify does not belong at intake **today** because there is nothing to graph;
it belongs here the day the corpus does.

---

## 7 · Token economy

### 7.1 Measured prompt sizes

Measured 2026-08-26 against the real prompts, by character count ÷ 4.

| Prompt | Size |
|---|---|
| `EXTRACTION_SYSTEM` | 4,713 chars ≈ **1,178 tokens** |
| of which `field_catalogue()` | 2,421 chars ≈ 605 |
| of which `signal_catalogue()` | 623 chars ≈ 155 |
| of which `untrusted.INSTRUCTION` | 351 chars ≈ 87 |
| `QUESTION_SYSTEM` | 564 chars ≈ **141 tokens** |
| `build_extraction_prompt`, turn 1 | 470 chars ≈ 117 |

**Method disclosure.** chars ÷ 4 is an estimate, not a measurement. The correct instrument is
`client.messages.count_tokens(model="claude-opus-5", …)`, which is model-specific and exact;
`tiktoken` is wrong for Claude by 15–20%. No API key was available in this environment, so every
figure below inherits that error bar. **Re-measure before acting on any margin narrower than
20%.**

### 7.2 A ten-turn conversation, simulated against the real prompt builders

Realistic turns (≈105-char question, ≈115-char answer), estimated input tokens per model call:

| Turn | ext pass 1 | ext pass 2 | question | total in | with caching |
|---:|---:|---:|---:|---:|---:|
| 1 | 1,348 | 1,571 | 275 | 3,195 | 3,195 |
| 3 | 1,487 | 1,710 | 398 | 3,595 | 1,143 |
| 5 | 1,653 | 1,876 | 522 | 4,050 | 1,376 |
| 10 | 2,003 | 2,226 | 832 | 5,060 | 1,828 |
| **Σ 1–10** | | | | **41,472** | **16,395** |

At Opus 5's $5/MTok input: **$0.207 today → $0.082 cached, a 60% reduction** (before the 1.25×
first-turn cache write, which is a few hundred tokens once). Add ~5,000 output tokens across ten
turns at $25/MTok ≈ $0.125, and a full intake conversation costs roughly **$0.33 today**, or
**$0.18** with §7.3 and §2.2 both applied.

Note the shape: extraction pass 2 is the single largest line in every row, and question wording
— the call running on the most expensive model — is the smallest.

### 7.3 Caching: the previous draft had the floor wrong

The previous draft said the minimum cacheable prefix is ~1,024 tokens and that
`EXTRACTION_SYSTEM` clears it *"with about 15% to spare"*. **The floor is model-dependent and
non-monotonic:**

| Model | Minimum cacheable prefix |
|---|---:|
| **Claude Opus 5** | **512** |
| Opus 4.8, Claude Sonnet 5 | 1,024 |
| Opus 4.7 | 2,048 |
| Opus 4.6, **Haiku 4.5** | **4,096** |

So on the default path (Opus 5) `EXTRACTION_SYSTEM` clears the bar by **2.3×**, not 15% — the
"one added field could drop it below the floor" worry was misplaced. The real hazard is the
opposite one, and §2.2 names it: **routing a call to a cheaper model can raise its cache floor
eightfold.**

The saving is not the system prompt anyway. **It is the conversation prefix**, which grows every
turn and is re-sent three times. A breakpoint after the last completed turn makes it O(n) instead
of O(n²)·3. Wizard turns are seconds apart, so the 5-minute TTL hits on essentially every turn
after the first. Cache reads cost ~0.1×, writes 1.25× (5-min TTL).

Two assertions worth writing as tests rather than comments:

1. `EXTRACTION_SYSTEM` is byte-identical across turns and users. Anything that varies — a
   timestamp, an unsorted dict, a regenerated id — silently zeroes the cache.
2. `usage.cache_read_input_tokens > 0` on turn 2 of a replayed conversation. That is the only
   proof the breakpoint is where we think it is.

### 7.4 Two measurable questions, not opinions

- **Does extraction pass 2 change anything?** It is ~48% of extraction input tokens. Run the
  harness at `extraction_passes=1` and `=2` and compare IRE and misfile rate. If pass 2 does not
  move them, it is the largest single saving in the layer — larger than caching.
- **Does the question model matter?** `written_by` already records when the guide fallback
  fired, so the failure is visible. Run the harness with `light_edit` routing and compare ESR.

### 7.5 One stale price in the repo

`execution/matrix.yaml:57` prices `claude-sonnet-5` at **$3 / $15** per MTok. The current list
rate is **$2 / $10** — $3/$15 is Sonnet 4.6's. Every estimate, ceiling and ledger entry that
routes through Sonnet 5 is over-stated by 50%. The file's own header says *"OPERATOR: confirm
the exact model id strings and current prices … before a real run"*, so this is the documented
maintenance step not having been run, not a design fault. Fix is one line; the layer that reads
it is G, not A.

---

## 8 · Data worth owning

Layer A generates the most defensible data in the system, and today it is kept only as project
state.

| Data | Why it is worth having |
|---|---|
| Conversation transcripts with per-field provenance | the eval set for §3.4, and the training set if elicitation is ever optimised |
| Questions that produced vague answers | which wording fails, per field and per app kind — §4.3's satisficing predictions are testable only from this |
| Fields corrected at review | a direct measurement of extraction error, already collected and already discarded |
| Assumptions the user overrode | six fields are defaulted-and-flagged; nobody knows which of them users accept |
| **App-kind → field-value distributions** | after fifty booking apps you know what a booking app's `entities` usually are |
| Which `source_field` a failed build traced back to (§3.5) | the only data that closes the loop from outcome to question |

That fifth row is the moat, and §4.5 gives it its proper name: it is a CBR case base, and the
Retain step is the only one that needs building — the other three are read paths. It makes better
defaults, better examples, and eventually §4.1's opening draft.

None of it requires new collection. It requires **not throwing away what already passes through**.

**Three constraints to design in rather than retrofit:**

1. **ADR-0019 is still Proposed.** What survives a project deletion is unanswered, and
   `C-F12 / G-F13` is verified only *partly*. This dataset must not start accumulating before
   that is settled — a corpus assembled under undefined retention is a liability, not an asset.
2. **ReqElicitBench has no licence file.** Its metrics and protocol are described in a public
   paper and may be reimplemented; **its 101 scenarios may not be vendored** without contacting
   the authors. Adopt the method, not the data.
3. **CBR's own failure mode (§4.5).** A case base entrenches its early distribution. Retrieval
   quality must be measured *per app kind*, or the corpus quietly makes every uncommon app worse
   while the aggregate number improves.

---

## 9 · ADR proposals

| # | Proposal | What it decides |
|---|---|---|
| **A-1** | **Fence the question prompt** | that `_field_prompt` and `_contradiction_prompt` wrap the transcript and `QUESTION_SYSTEM` carries `untrusted.INSTRUCTION`, with the test that already exists for extraction mirrored. Closes half of `C-F14`'s Layer-A surface |
| **A-2** | **The replay harness is a prerequisite, on published metrics** | that no change to Layer A ships without moving IRE / ESR / TKQR against a named baseline; that the oracle-user follows ReqElicitGym's three principles; that grounding is scored by **AutoAIS** rather than by our own rules marking their own homework; and that the harness is **declared a regression detector, not evidence of quality** |
| **A-3** | **Prompt-cache the conversation prefix** | where the breakpoint goes, plus two tests: prefix byte-stability, and `cache_read_input_tokens > 0` on turn 2 |
| **A-4** | **Structured outputs for both intake calls** | that `output_config.format` replaces regex JSON scraping on the Anthropic path, and that the regex survives as the other-vendor fallback. Touches `RelayOptions`, so it is cross-layer |
| **A-5** | **Model and effort routing per call type** | extraction stays strongest at high effort; question wording moves to `light_edit` — **and accepts that Haiku 4.5's 4,096-token cache floor makes that call uncacheable.** Needs A-2 to decide |
| **A-6** | **App-kind detection, additive only** | that classification uses ReqElicitGym's ten types, may steer examples, wording and conditionals, and may **never** remove a core field or reorder the gate. Emits `schema.org/applicationCategory` at the boundary |
| **A-7** | **Style becomes a question** | that `look` stops being silently defaulted and gets asked when the kind warrants it. The one finding two independent sources agree on |
| **A-8** | **Requirement identity** | that list-valued fields mint per-item ids with per-item provenance, so invariant 1 and the reveal's met/unmet list become possible. Prerequisite for Layer B's impact analysis, for §3.5, and for the `grounding` field the `ears-requirements` skill already specifies |
| **A-9** | **A 29148 vector beside the boolean** | that the gate keeps its boolean and gains a standard-named characteristic vector — **not** an invented percentage |
| **A-10** | **Retain intake data as a CBR case base** | **blocked on ADR-0019.** Also decides that retrieval quality is measured per app kind, and that ReqElicitBench's data is not vendored |

**Ordering, and why.**

1. **A-1** first — it is cheap, it closes a verified security finding, and it does not need the
   harness to justify itself.
2. **A-2** next — it is what makes A-4, A-5 and A-6 decidable rather than arguable. Everything
   below this line is an opinion until it exists.
3. **A-3** and **A-4** — both save money or delete failure modes without changing what the user
   experiences. A-4 needs A-2 only to prove it did no harm.
4. **A-7** — small, cheap, and the single strongest evidence-backed finding in this document.
5. **A-5**, **A-6**, **A-8**, **A-9** — these change what the user experiences or what
   downstream layers receive. A-8 is the one Layer B is waiting on.
6. **A-10** waits on ADR-0019, and A-6 waits on A-2 for its baseline.

**Two open questions that could not be settled from the code.**

**a. What happens the moment the gate opens** (§3.6). Hard stop or open floor. It decides whether
*momentum over completeness* is a floor or a ceiling.

**b. Whether Layer C wants a richer signal at all.** A-9 assumes it does. Nothing in `layerc/`
was read for this document, and the as-built Layer A doc flags the same uncertainty. Ask before
building the vector.

---

*Written 2026-08-26. Code claims carry `file:line` and were verified against the working tree,
with `pytest -k intake` → 67 passed. Prompt sizes are chars÷4 estimates and are marked as such —
`messages.count_tokens` is the correct instrument and no key was available. External claims carry
links; research was read at abstract-to-method level except ReqElicitGym, whose repository was
fetched. Prices are Anthropic first-party list rates. Speculation is marked as speculation.
Nothing here is implemented.*
