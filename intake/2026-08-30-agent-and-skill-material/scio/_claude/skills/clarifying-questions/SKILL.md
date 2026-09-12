---
name: clarifying-questions
layer: A
phase: build-time
status: written
description: Decide whether to ask a person at all, then shape the question so it can be answered. Use when writing or reviewing a clarifying question, when an inferred default contradicts something the user said, when a choice is irreversible, when someone proposes suppressing a question with a saved preference, when a user says "just build it", when there are more real options than a picker can show, when a reply is vague or a bare letter, or when deciding what a wizard may settle on its own. Carries the three authority classes and the one that is never auto-decided, the one-way door registry with stable option keys, six risk categories that force confirmation, the decision-brief format, the split-never-drop rule, the bounded escape hatch with an irreducible core, and a graded eval for the recommendation line.
---

# clarifying-questions

Layer A's gate decides **which** field to ask about — deterministically, and *"impossible for a
model to talk its way past"* (`intake/questions.py`). This skill is about the two decisions the
gate does not make: **whether a thing should be asked at all**, and **what shape the question
takes** once it is.

Both are recurring, both are currently improvised, and both have been written down elsewhere in
more detail than we have written them.

---

## 1 · Source

Four independent codebases, read as files on 2026-08-26 and recorded in `docs/mined/`. None of
this is a paper; all of it is shipped procedure, which is a weaker kind of evidence and is treated
as such in §7.

| Source | Licence | What it contributes | Mined in |
|---|---|---|---|
| `garrytan/gstack` @ `ad84005` — shared `AskUserQuestion` preamble (~128 lines, pasted into 40 skills), `autoplan`, `office-hours`, `plan-tune`, `scripts/question-registry.ts`, `scripts/one-way-doors.ts` | MIT | the brief format, the split rule, the three authority classes, the door registry, the escape hatch | `PASS2-GSTACK-SKILLS.md` §4–§5, `OTHERS-MINED.md` §1.3 |
| `garrytan/gstack` test suite — `test/llm-judge-recommendation.test.ts` | MIT | the graded properties and the judge that grades them | `PASS2-GSTACK-TESTS.md` §4.2 |
| `obra/superpowers` @ `b36e082` — `brainstorming` | MIT | the ambiguity rule in §6 | `OTHERS-MINED.md` §2.2 |
| `affaan-m/ECC` — `intent-driven-development` rule 5 | see repo | the six risk categories in §2.4 | `ECC-SKILLS.md` §2.3 |

---

## 2 · Whether to ask

### 2.1 Three authority classes, and the one that is never auto-decided

Every unresolved choice falls into exactly one class. The classification decides who resolves it.

| Class | What it is | How it resolves |
|---|---|---|
| **Mechanical** | one right answer given the constraints already recorded | decide silently; state it in the summary, not as a question |
| **Taste** | reasonable people differ, and nothing the user said points either way | decide **with** a recommendation, surface it at the final gate. Three named sources: close approaches, borderline scope, cross-model disagreement |
| **User Challenge** | the system's own analysis says the user's stated direction should change | **never auto-decided** |

The third class is the finding. A wizard that infers defaults will sometimes infer one that
*contradicts something the user actually said* — and that is not a Taste call with an unusual
answer, it is a different kind of event and needs its own name, its own format, and a rule that it
never resolves silently.

**The format, five lines, taken as written:**

```
What the user said:              (their original direction)
What the analysis recommends:    (the change)
Why:                             (the reasoning)
What context we might be missing: (explicit acknowledgment of blind spots)
If we're wrong, the cost is:     (what happens if the user's original direction was right)
```

> **The user's original direction is the default. The system must make the case for change, not
> the other way around.**

The last line is what turns a suggestion into a decision a person can actually make: without it
the user is choosing between two assertions, and the one with a mechanism behind it wins by
default. One carve-out in the source: if the concern is a security or feasibility risk *"not just
a preference"*, the framing says so — and *"the user still decides."*

**Where this bites in Layer A.** `FieldMeta.source = derived` covers *"the system worked this
out"*. It does not distinguish *"the system worked this out about something the user never
mentioned"* from *"the system worked this out and it conflicts with message m4"*. Only the second
is a User Challenge. Note that this is **not** the same as `contradictions.detect()`, which fires
when the *user* contradicts the user; here the contradiction is between the user and us.

### 2.2 The door registry: one-way and two-way, keyed by option, not by label

A question is registered before it is asked, with a `door_type`:

- **`one-way`** — destructive operations, architecture or data-model forks, scope additions over a
  day, security or compliance choices. **Always asked, regardless of any stored preference.**
- **`two-way`** — suppressible by an explicit preference, because getting it wrong is cheap to
  undo.

Registry entries in the source carry a stable kebab id, the skill, a category (`approval` ·
`clarification` · `routing` · `cherry-pick` · `feedback-loop`), the `door_type`, and the option
keys. Preferences, logs and tuning all key off the registered id.

**The detail to copy verbatim, because it is the one that gets skipped:**

> *"`options` is a short list of stable option keys. UI labels can vary; keys must stay the same
> so preferences survive wording changes."*

If what gets recorded is the label the user saw, then re-wording a question orphans every prior
answer to it. Layer A's provenance has exactly this exposure: `written_by: model|guide` records
*who wrote* the wording, and the wording is re-generated per turn.

And when a one-way door overrides a stored preference, **disclose that it fired.** A suppression
that silently stops suppressing is indistinguishable from a bug.

### 2.3 The registry is primary; pattern-matching is a backstop, never the gate

The source ships a keyword matcher (`one-way-doors.ts`) *and* refuses to let it be the gate:

> *"prose-parsing is too weak to be the PRIMARY safety gate — wording can change."*

Three layers, in this order:

1. **Registry hit** → use the recorded `door_type`.
2. **No registry id** → keyword patterns, as a secondary check only.
3. **Neither** → **ask.** The default is to ask, not to assume two-way.

They wrote the weak check, said in their own review that it was weak, and then kept it as a
backstop rather than promoting it. Copy the layering, not just the list.

### 2.4 Six risk categories that force a stop, whatever the field-completeness gate says

`is_buildable()` is field-shaped: *is this slot populated*. This predicate is risk-shaped: *is what
remains unknown dangerous*. They are complementary, and the second is the one a completeness gate
structurally cannot express.

Require explicit confirmation before proceeding when an unresolved decision could create:

| # | Category |
|---|---|
| 1 | material **security exposure** |
| 2 | **data loss** |
| 3 | **irreversible migration** |
| 4 | **contractual or API breakage** |
| 5 | meaningful **cost** |
| 6 | **destructive external action** |

The condition of adoption, from the mined verdict: these six become a **computed predicate over
the typed spec**, not a line in a prompt. *"A prompt instruction here is a judgment standing in
for a gate."* Making that predicate part of `is_buildable()` changes the gate's contract and is an
ADR, not a skill's business — see `docs/triage/LAYER-A-TRIAGE.md` #32.

---

## 3 · The shape of the question, once you are asking

One question, one shape. Every constraint below is checkable by a reader or a linter, which is why
the format is worth having at all.

```
D<N> — <one-line question title>
Context:   <one short grounding sentence>
ELI10:     <plain English, 2-4 sentences, name the stakes>
Stakes if we pick wrong: <what breaks, what the user sees, what is lost>
Recommendation: <choice> because <one-line, option-specific reason>
Completeness: A=X/10, B=Y/10   (or: options differ in kind, not coverage)
Pros / cons:
  A) <option label> (recommended)
     + <pro — concrete, observable>
     - <con — honest>
  B) <option label>
     + <pro>   - <con>
Net: <one line on what is actually being traded off>
```

The rules that make it more than a template:

- **At least two pros and one con per option**, each substantive rather than a phrase. The source
  enforces ≥40 characters; the character count is a proxy for *"you did not just write 'faster'"*.
- **`(recommended)` on exactly one option, even when neutral.** If it is a taste call, say so in
  the reason — *"this is a taste call, no strong preference"* — and still mark one. An unmarked
  brief hands the work back.
- **Completeness scored, or explicitly declined**: 10 = complete, 7 = happy path, 3 = shortcut —
  or a note that the options differ in kind so a score would be false precision.
- **Effort on two scales** where they differ: *"(human: ~2 days / CC: ~15 min)"*. This makes
  compression visible at decision time rather than after.
- **A vague reply is re-asked, never interpreted.** Treat silence, *"ok"* or *"sure"* without an
  explicit choice as not-yet-answered. For anything irreversible, require the choice typed out.
- **A bare letter maps to the single most recent unanswered brief.** If more than one is open, do
  not guess — ask which one it answers.

---

## 4 · Five or more options: split, never drop

Any picker has a cap; the source's is four options per call. The rule for what happens when a real
decision has more:

> **With 5+ real options, NEVER drop, merge, or silently defer one to fit.** Split per-option —
> fire N sequential calls, one per option. **Default to this when unsure.**

Mechanics, in the source and worth taking whole:

- Four buckets per split call: **Include · Defer · Cut · Hold** — where *Hold* stops the chain.
- A final call validating the assembled set, and a per-option revise path so one answer can change
  without re-running the chain.
- Above six options, a meta-question first: proceed / narrow / batch.
- **A split chain is never auto-decide-eligible.** Their runtime checker refuses `never-ask` on any
  split id, for a stated reason: **the user's option set is sacred.**

The failure this prevents is invisible in the output. A brief showing four options when five
existed looks exactly like a brief showing four options when four existed, and the dropped one is
never mentioned again. That is why §8 puts a **floor** on the count and not only a ceiling.

---

## 5 · The escape hatch, as a bounded negotiation

An impatient user is the normal case, not the edge case, and *"skip the questions"* is a request
that a gate must survive without either ignoring the person or collapsing.

The procedure, from `office-hours`:

1. **Push once, and say why.** Name the value being skipped rather than asserting the rule.
2. **Concede a bounded amount** — ask the *two* most critical remaining questions, chosen by the
   classifier (see `ontoagent-elicitation` §2.4), then proceed.
3. **If they push back a second time, respect it.** Proceed immediately. Do not ask a third time.
4. **A full skip requires evidence**, not impatience — a formed plan with specifics.
5. **Even then, the irreducible core still runs.** In the source, two named phases survive every
   skip. In Layer A the analogue is the set of fields without which a build is guessing, and it
   must be named in advance rather than negotiated in the moment.

The shape is the finding: **one push, a bounded concession, then unconditional compliance, around
a core that is not on the table.** Written down, it is auditable; improvised, it is whatever the
model feels like that turn.

---

## 6 · When the answer is to resolve, not to ask

Not every unknown deserves a question. The distinction, which is easy to lose:

| Situation | What it is | What to do |
|---|---|---|
| Two things the user said clash | a **contradiction** | **ask.** Layer A already enforces this: `test_a_contradiction_is_asked_about_rather_than_resolved` |
| One thing the user said has two readings | an **ambiguity** | **resolve it, and record the resolution** |

> *"Could any requirement be interpreted two different ways? If so, pick one and make it
> explicit."*

Resolving beats flagging because it produces a field with a value and a note saying it was
disambiguated, rather than a blank field with a warning attached — and a recorded interpretation is
something a person can correct on review, which a warning is not. The recorded resolution is
`derived`, never `stated`; `ais-grounding` §2.5 governs which kinds of fact may be resolved this
way at all.

**Do not collapse the two rows.** Resolving a contradiction silently is the failure Layer A
already has a test against.

---

## 7 · Limits — what the sources show versus what we would be assuming

| The source shows | We would be assuming |
|---|---|
| Procedures **shipped and used** in a large skill corpus, with tests for some of them | that they work. **No source here reports an outcome measurement.** There is no A/B, no user study, and no baseline. This is craft that survived contact with users, which is real evidence and is not the same as a result |
| A format for a **CLI agent's** question to a developer | that it transfers to Scio's wizard, whose user is a founder answering in a browser and whose questions are one sentence with an example. The brief is heavier than what `write_question` emits today, and heavier is not automatically better |
| The 5+ split rule solving a **4-option UI cap** | that Scio has the same cap. It does not today — `next_question` returns one question with one example. The rule matters the moment a picker with a cap exists, and the principle (*never silently drop an option*) applies before that |
| The six risk categories as **prompt text** in their repo | that they can be computed. The mined verdict says they must be, and nothing has yet mapped them onto the typed spec's field kinds |
| `door_type` as a **hand-maintained registry** of 56 entries | that the registry stays current. An unregistered question defaults to asking, which is safe, but a registry nobody updates degrades to the keyword backstop they themselves called too weak |
| A judge scoring recommendation quality at **~$0.04/run** on their fixtures | that the threshold transfers. `reason_substance >= 4` was tuned against their rubric and their fixtures; ours would need re-anchoring on hand-graded examples before the number means anything |

**The one thing not to take:** none of this may make question *selection* adaptive. `is_buildable()`
decides which required field is unanswered; everything here operates on questions the gate has
already decided to ask, or on choices the gate never covered. A brief that argues its way out of
asking a core field has inverted the layer.

---

## 8 · Eval

| # | Case | Expected |
|---|---|---|
| E1 | An inferred default that conflicts with a user message | Classified **User Challenge**. Emits all five lines, including *"if we're wrong, the cost is"*. Never resolved silently, and never counted as `derived` without the conflict recorded |
| E2 | An inferred default about something the user never mentioned | **Not** a User Challenge. Taste or Mechanical. Distinguishing E1 from E2 is the whole classification |
| E3 | A one-way question with a stored preference that would suppress it | Asked anyway, **and** the override is disclosed in the output |
| E4 | A decision with six real options | Six appear across a split chain. **Count them.** A run that emits four is a failure even though every visible brief is well-formed |
| E5 | A decision with two real options | Exactly two. The ceiling catches question-spam; the floor (E4) catches silent dropping. Both, or neither is a test |
| E6 | A brief with `(recommended)` absent, or on two options | Rejected. Neutrality is expressed in the reason, not by declining to mark one |
| E7 | A brief whose recommendation reads *"because it's safer"* | Fails `reason_substance`. A passing reason is option-specific and contrasts a named alternative |
| E8 | Reply is *"ok"* to a one-way question | Treated as not-yet-answered and re-asked. Asserted as an absence — **no** recorded answer — with a positive control that a proper reply does record one (`testing` §3.5) |
| E9 | Reply is a bare *"B"* with two briefs open | The system asks which brief it answers. It does not pick the most recent |
| E10 | User says *"just build it"* twice | One push, a bounded concession of two questions, then compliance. **A third push is a defect.** The named core fields are still filled |
| E11 | A question with no registry id and no keyword match | Asked. Default-to-ask is asserted directly, because it is the branch that never fires in normal operation and so is never exercised by accident |
| E12 | Rubric or threshold changed | The judge re-runs against hand-graded fixtures, gated on the rubric file so it fires on rubric changes and not on every test run. Report agreement with the hand grades **before** reporting any score |

**E1 vs E2 and E4 vs E5 are the load-bearing pairs.** Each is a floor and a ceiling on the same
mechanism, and a suite with only one half of either passes while the mechanism is broken.

---

## 9 · When this skill is the wrong tool

- **Deciding which field to ask about.** That is `is_buildable()` and `next_target()`, and it is
  deterministic on purpose. Nothing here may touch it.
- **Deciding which *concerns* matter for this kind of app.** That is `ontoagent-elicitation`.
- **Deciding whether an extracted value is legitimately grounded.** That is `ais-grounding`.
- **Adopting any of this into the product.** Each adoption changes Layer A's behaviour and is an
  ADR. This skill carries the option space and the choice rules; it does not decide that Scio
  ships them.
