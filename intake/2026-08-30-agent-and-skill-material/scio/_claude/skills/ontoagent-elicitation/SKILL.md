---
name: ontoagent-elicitation
layer: A
phase: build-time
status: written
description: Decide which requirement concerns are relevant to the kind of app a user is describing, without letting a model choose which required question gets skipped. Use when adding app-kind detection to intake, when pre-arming conditional follow-up questions, when someone proposes making question selection adaptive or scored, when a request seems to describe several apps at once, when deciding what to classify a request as before asking anything, when a mid-session signal suggests the job is bigger than it looked, when a design rests on OntoAgent's reported 33 percent improvement, or when reviewing whether a change to the wizard gives up the deterministic gate. Carries the four-stage method, the additive-only rule that keeps Scio's gate guarantee intact, the exact scope of the published numbers, and the eval that proves no core field can be dropped.
---

# ontoagent-elicitation

An interview agent that knows *what a booking app usually needs asked* will ask better
questions than one walking a fixed list. That is the promise. The danger is the mechanism:
the published method scores and prunes concerns, and pruning is exactly the guarantee Scio
refuses to give up.

This skill exists to take the first half and refuse the second, on purpose, in writing.

---

## 1 · Source

**From Chat to Interview: Agentic Requirements Elicitation with an Experience Ontology.**
Dongming Jin, Zhi Jin, Yaotian Yang, Linyu Li, Zheng Fang, Yuanpeng He, Wenchun Jing,
Xiaohong Chen. Submitted 7 May 2026. [arXiv 2605.05828](https://arxiv.org/abs/2605.05828)

Same research group as ReqElicitGym (see the `req-elicit-gym` skill), which is where its
metrics come from. Read the two together; the numbers below are ReqElicitGym's metrics.

---

## 2 · Method, in the form we use it

### 2.1 What the paper does

OntoAgent automatically analyses domain-specific requirements descriptions to construct an
**experience ontology** — requirements *concerns* organised by domain — and then runs four
sequential operations per turn:

| Stage | What it does |
|---|---|
| **ParseUser** | read the user's turn into the ontology's vocabulary |
| **ScoreOnto** | score which concerns are relevant to what has been said |
| **ReRankOnto** | order them, so the important question comes first |
| **GatePrune** | drop concerns judged irrelevant, and stop |

The claimed effect: interviews that are *systematic and explainable* rather than improvised.

### 2.2 What Scio takes, and what it refuses

**Scio's gate is deterministic by decision, not by accident.** `intake/questions.py`:

> WHICH field to ask about is decided by the gate — deterministic, reproducible, free, and
> impossible for a model to talk its way past. Only the WORDING goes to the relay.

So the adoption is **additive only**:

| Stage | Scio's use |
|---|---|
| ParseUser | already exists — this is `extract()` |
| **ScoreOnto** | **adopt, additively.** A concern scored relevant for this app kind *turns on a conditional trigger*. It may add a question |
| ReRankOnto | **refuse.** Core order is fixed in `CORE_FIELDS` and walked by `next_target()`. Re-ranking is the thing being given up, and it is not free |
| **GatePrune** | **refuse outright.** A model deciding a required concern is irrelevant is precisely the failure mode `is_buildable()` exists to prevent |

**The asymmetry that makes this safe** is already written into `_apply_signals`
(`intake/extraction.py`): a signal is only ever turned *on*, because *"a wrong one costs a
question the user can wave away, while a missed one costs a whole area of the app."* Concern
scoring inherits that asymmetry exactly — a wrong app-kind classification costs one irrelevant
follow-up, never a missing requirement.

### 2.3 The concrete shape

1. Classify the app kind (ReqElicitGym's ten types — see the `req-elicit-gym` skill).
2. Look up the concerns that kind usually raises.
3. **Turn on** the matching entries in `TriggerSignals`. Never off.
4. `triggered_conditionals()` and `is_buildable()` are untouched. They still decide everything.

The ontology is a lookup table keyed by app kind, not a live model call. Deterministic first,
same as every other quality mechanism in this system.


### 2.4 Classify out loud — and the five rules that make a classifier safe

The paper supplies *what to classify by*. Two codebases, read as files on 2026-08-26, supply the
procedure around it — and they reached the same first move independently of each other and of the
paper.

| Source | Licence | Mined in |
|---|---|---|
| `obra/superpowers` @ `b36e082` — `brainstorming` | MIT | `docs/mined/OTHERS-MINED.md` §2.2 |
| `garrytan/gstack` @ `ad84005` — `office-hours`, `spec` | MIT | `docs/mined/PASS2-GSTACK-SKILLS.md` §4.1, §4.4 |

**a. Classify before the first content question, and say it out loud.** `brainstorming` splits
three ways — *Spike* (the output is an answer, not code), *Bounded* (a scoped change to something
that already exists — *"Bounded measures the repo, not your familiarity"*), *Architectural*.
`office-hours` does the same before any content question.

The reason is not accuracy, it is **provenance**: announcing a classification the user can correct
puts the single biggest assumption on the record before anything is built on it. A classification
made silently is an assumption; the same classification stated is a decision the user has ratified
or corrected. Record it exactly as `_apply_signals` records a signal — with its source.

**b. Two classifiers, orthogonal, not one.** `office-hours` runs *what kind of thing* and *how far
along* separately, and the pair selects the question set — not a subset of one classifier's
branches. Layer A today has neither: every app walks the same six fields in the same order, and the
only variation is how many get filled. Kind × stage is strictly more information than kind, and it
costs one more announced assumption.

They are genuinely different procedures rather than tone variants, and they are **revisable
mid-session**: *"if the user starts in builder mode but says 'actually I think this could be a real
company'… upgrade… naturally."* Which leads directly to:

**c. The ratchet is one-way.**

> *"When in doubt between two paths, take the heavier one. The ratchet is one-way: hidden
> complexity discovered mid-task upgrades the path — stop, say so, and step up. **Nothing
> downgrades mid-task.**"*

This is the same asymmetry §2.2 already relies on, applied to the classifier rather than to a
signal: a wrong-heavy classification costs questions the user can wave away; a wrong-light one
costs an area of the app. An app builder discovers mid-build that a "simple" app needs auth,
tenancy or a migration constantly, so the upgrade path is the normal case and needs to exist. A
*downgrade* path would let a mid-session signal undo a decision the gate already relied on, and
that is GatePrune arriving through a side door.

**d. Decompose before interrogating.**

> *"If the request describes multiple independent subsystems… flag this immediately. Don't spend
> questions refining details of a project that needs to be decomposed first."*

A check that runs *before* field-filling, not a conditional inside it. For a builder aimed at
people who are not programmers this is among the most common intake failures — three apps described
as one — and there is no such check today. Its output feeds Layer C, which is where decomposition
actually happens; Layer A's job is only to notice and say so.

**e. Ground the question, or say that you could not.** `spec` makes this mandatory before its
technique questions: read at least one piece of real evidence first, *"and if you genuinely cannot
find any related evidence, say so explicitly."*

Scio is greenfield, so the analogue is the **library**: before asking, search Layer D for a
`Contract` that covers the concern, and either ground the question in what exists — *"you have a
booking flow already; does this reuse it?"* — or state that nothing matched.

**Both branches produce provenance**, and that is the point. *"Matched nothing"* and *"did not
look"* are different facts, and only one of them is evidence. Layer D has the same requirement from
a second source — `docs/mined/ECC-SKILLS.md` #19, *"Layer D must distinguish matched nothing from
could not look"*, whose author's name for the failure is **silent skipping**.

Two constraints on all five, inherited from §2.2 and not negotiable: a classifier may only turn
conditionals **on**, and no classification may change `CORE_FIELDS` or its order. E1 and E4 below
test exactly that, and they apply to these five rules as written.

---

## 3 · Limits — what the paper shows versus what we are assuming

**The number everyone repeats: +33% IRE, +21% TKQR.** The sentence that must travel with it:

> Measured on **website applications**, in the authors' setup, against **their** baselines,
> with **their** ontology and **their** interviewer wrapper. Not on Scio, not on Scio's
> schema, not on Scio's users.

A skill that repeats "+33%" without that sentence is selling a number it did not earn.

| The paper shows | We would be assuming |
|---|---|
| Gains for the **whole** four-stage pipeline | that ScoreOnto alone carries the gain. **The paper does not ablate it.** Some or all of the improvement may come from ReRankOnto and GatePrune — the two stages we refuse |
| An ontology **constructed automatically** from domain requirements descriptions | that we can build one by hand, or from a corpus we do not yet have. Untested either way |
| Results in the website domain | transfer to tender platforms, internal tools, logistics. Unknown |
| Improvement over baselines that ask worse questions | improvement over a *deterministic fixed-order* gate. **The paper never compares against that**, because nobody else has one |

**The honest reading: this is a hypothesis with a citation, not an imported result.** Adopting
ScoreOnto additively is cheap and safe; claiming it will produce +33% is neither. Only the
harness (`req-elicit-gym`) can say whether it did anything at all.

**§2.4's sources carry a weaker warrant than the paper**, and it points the other way. They are
shipped procedure with no reported outcome — no measurement that announcing a classification
improves anything, and no ablation of the two-classifier split against one. What they have that the
paper does not is survival in daily use. Treat §2.4 as craft with a citation: cheap, plausible,
and unmeasured until the harness says otherwise. The one claim in §2.4 that does **not** rest on
their evidence is the one-way ratchet, which follows from `_apply_signals`'s own asymmetry and
holds regardless.

**And one open risk of our own:** if the concern table is built from Scio's own corpus, it
inherits case-based reasoning's entrenchment failure — fifty booking apps make booking apps
better and every uncommon app worse. Measure per app kind or do not measure.

---

## 4 · Eval

| # | Case | Expected |
|---|---|---|
| E1 | Classify an app kind, then run the gate | The set of core fields is **identical** to the unclassified run. Byte-for-byte. This is the guarantee; it is a test, not a promise |
| E2 | Deliberately mis-classify (a tender platform as a restaurant booking app) | Extra, irrelevant conditionals fire. **No core field disappears, no order changes.** The failure is a wasted question |
| E3 | A concern scored *irrelevant* for the kind, but the user's own words trigger it | The conditional still fires. Scoring may add; the user's evidence always wins |
| E4 | Every one of the ten app kinds, gate run to completion | `CORE_FIELDS` asked in `CORE_FIELDS` order in all ten. Any deviation is a GatePrune leak |
| E5 | Concern lookup with an unknown / unclassifiable app | Behaves exactly as today: no extra conditionals, gate unchanged. Classification failure must be a no-op, never an error |
| E6 | Harness run with and without concern pre-arming | Report IRE, ESR, TKQR and **turns-to-buildable** for both. Pre-arming that lifts IRE while inflating turns has traded one metric for another — that is the whole point of measuring both |
| E7 | Grep the implementation for any write that sets a `TriggerSignals` field to `False` | Zero matches. `_apply_signals`'s one-way rule is the mechanism; a test asserting the absence is how it stays that way |
| E8 | A classification made, then a mid-session signal pointing to a heavier one | Upgrades, and says so. **The reverse signal changes nothing.** Both directions asserted in the same test, or the ratchet is a comment |
| E9 | A request naming three independent subsystems | Flagged before the first field question, not after six of them |
| E10 | A question asked where a matching `Contract` exists, and one where none does | Both record which happened. *"Nothing matched"* is written down; it is never indistinguishable from not having looked |
| E11 | Every classification the system makes | Present in the record with its source, and correctable by the user. An unannounced classification fails this whatever it decided |

**E1 and E4 are the load-bearing ones.** If either fails, the adoption stopped being additive
and became the thing ADR-0010 decided against.
