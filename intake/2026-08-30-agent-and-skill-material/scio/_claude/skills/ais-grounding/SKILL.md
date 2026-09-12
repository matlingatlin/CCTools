---
name: ais-grounding
layer: A
phase: build-time
status: written
description: Check that every value a model claims a person stated is actually supported by what they said, using a published criterion rather than our own rules marking their own homework. Use when writing or reviewing extraction grounding, when scoring an intake replay harness, when someone proposes relaxing the provenance rule, when a field is claimed as stated without a message id, when deciding whether a spec field is evidence or invention, when a value could be inferred but perhaps should not be, when a pasted document or tool output is about to become the source of a fact, or when deciding whether to forbid a field in the schema rather than in a rule. Carries the AIS definition, how AutoAIS automates it, why an id check and an entailment check catch different failures, the taxonomy of facts that may never be inferred at all, and the limits of using an NLI model as a judge.
---

# ais-grounding

Scio's strongest invariant is that an unstated value is never invented. It is enforced in code
(`intake/extraction.py::apply_extraction`), not only in a prompt, and a field claiming `stated`
without a real message id is discarded.

That rule checks **that a citation exists**. It does not check **that the citation supports the
claim**. Those are different failures, and there is a published framework for the second one.

---

## 1 · Source

**Measuring Attribution in Natural Language Generation Models** — the **AIS** framework
(*Attributable to Identified Sources*).
Hannah Rashkin, Vitaly Nikolaev, Matthew Lamm, Lora Aroyo, Michael Collins, Dipanjan Das,
Slav Petrov, Gaurav Singh Tomar, Iulia Turc, David Reitter — Google Research.
*Computational Linguistics* 49(4), 2023.

- Paper: [arXiv 2112.12870](https://arxiv.org/abs/2112.12870) ·
  [ACL Anthology](https://aclanthology.org/2023.cl-4.2/)
- Evaluation resources: [github.com/google-research-datasets/AIS](https://github.com/google-research-datasets/AIS)

Related, for the automated variant and its difficulty:
[AttributionBench](https://aclanthology.org/2024.findings-acl.886.pdf) (Li et al., ACL Findings
2024).

**Three further sources, for §2.5–§2.7 only.** These are shipped code and shipped procedure read on
2026-08-26, not research, and §3 treats them accordingly.

| Source | Licence | Contributes | Mined in |
|---|---|---|---|
| `affaan-m/ECC` — `intent-driven-development` rule 2 | see repo | the legitimacy taxonomy (§2.5) | `docs/mined/ECC-SKILLS.md` §2.3 |
| `eyaltoledano/claude-task-master` @ `c0c98d3` — `base-schemas.js` | NOASSERTION — **read for the idea only, no text or code taken** | schema-level exclusion (§2.6) | `docs/mined/OTHERS-MINED.md` #40 |
| `garrytan/gstack` @ `ad84005` — `plan-tune`, `test/gstack-question-preference.test.ts` | MIT | the user-origin gate (§2.7) | `docs/mined/PASS2-GSTACK-SKILLS.md` §4.6, `PASS2-GSTACK-TESTS.md` §2.7 |

---

## 2 · Method, in the form we use it

### 2.1 The criterion

A statement is **attributable to identified sources** if a generic listener would affirm:

> *"According to [source], [statement]."*

Two steps, and the first is the one people skip:

1. **Interpretability** — the statement must be turned into a standalone proposition, with
   pronouns and context resolved, so it can be judged at all.
2. **Support** — the proposition must be verifiable from the cited source alone.

**AutoAIS** is the automated version: an NLI/entailment model asked whether the source entails
the proposition. It is a proxy for the human judgement, and the paper treats it as such.

### 2.2 Applied to Layer A

Scio's spec is a set of claims about the external world (the user's world), each carrying a
citation (`FieldMeta.provenance`, a list of message ids). That is the exact shape AIS was
written for, with the user's own turns as the source document.

| Layer A concept | AIS concept |
|---|---|
| `FieldMeta.value` with `source = stated` | the statement to be attributed |
| `provenance: ["m2", "m5"]` | the identified source |
| the grounding rule in `apply_extraction` | a **presence** check on the citation |
| **missing today** | the **support** check — does m2 actually say this? |

**The two failures are genuinely different.** Today's rule catches a model citing nothing. It
does not catch a model citing `m2` for a value `m2` does not support — which is the more
plausible failure once a model knows the rule exists, because a valid-looking id is free to
produce. `_merge_list` keeping the user's own wording makes support *usually* hold; nothing
makes it hold.

### 2.3 Where it goes

**In the harness, not in the request path.** Running an entailment check on every field on every
turn adds latency and cost to the wizard's hot loop for a failure that is rare. Running it
across a replayed corpus gives a single number — **grounding precision** — that says whether
extraction's citations mean anything.

Two AIS-derived metrics for `req-elicit-gym`'s harness:

- **Attribution precision** — of fields marked `stated`, the share whose cited messages entail
  the value.
- **Interpretability rate** — the share of extracted values that are standalone propositions at
  all. A field holding *"yes, that one"* is unjudgeable, and unjudgeable is a defect in its own
  right.

### 2.4 The rule this does not replace

`CORRECTION_MARK = "corrected-on-review"` is deliberately not a message id, so a model can never
forge it. That is a **security** property and AIS has nothing to say about it. Keep the id check.
AIS is added beside it, never instead of it.


### 2.5 What may be inferred **at all** — a legitimacy taxonomy

AIS asks whether a citation supports a claim. This asks something prior: **was the claim ever ours
to make?**

From ECC's `intent-driven-development` rule 2 (`docs/mined/ECC-SKILLS.md` §2.3), the only skill in
286 that carried method, limits *and* an eval:

> Do not infer product or business constraints from code. Business rules, compliance obligations,
> contractual SLAs, pricing, data-retention policy, prioritization, and target users cannot be read
> from a repository. Record them as **assumptions flagged for confirmation, never as discovered
> facts.** The repository tells you how the system behaves today, not what the business requires it
> to do.

Their own pass/fail example is exact: *"Users on the free tier are limited to 100 exports per
month"* filed under **discovered facts** fails — because a per-tier limit is a business rule, and
no amount of correctness makes it a discovery.

`FieldMeta` records **where** a value came from. It does not record **which classes of fact may be
inferred at all** — and inferring one of the forbidden classes is an error *even when the inference
is right*. That is the part a grounding check cannot catch: a correctly-inferred pricing rule is
perfectly attributable to nothing.

Their direction is code → requirements and ours is conversation → spec, so the source differs while
the classes do not:

| Class | Layer A's exposure |
|---|---|
| pricing and commercial terms | inferable from any e-commerce-shaped description |
| data-retention policy, compliance obligations | `data_ownership_sensitivity` is a compliance-shaped field with a defaulted value |
| target users | `users_and_roles`, one of the six core fields |
| prioritisation | which of `key_actions` matters most is never stated and is always tempting |

**The rule this yields:** a field in a forbidden class may be `stated`, or `default` and visibly
flagged as an assumption. It may not be `derived`. The difference between `derived` and `default`
is precisely the difference between *"we worked this out"* and *"we assumed this, ask us about
it"*, and for these classes only the second is honest.

### 2.6 The strongest form of the rule is a schema, not a rule

From task-master's `base-schemas.js` (`docs/mined/OTHERS-MINED.md` #40), recorded there as the
strongest idea in that repository: **user-owned fields are absent from the model's output schema,
not merely protected by a rule.**

A rule the model is asked to follow can be broken, and then has to be caught. A field that does not
exist in the schema the model emits into **cannot be emitted**, and nothing has to catch anything.
With grammar-constrained structured outputs (`docs/next/LAYER-A-INTAKE.md` §2.1) the exclusion is
enforced by the decoder rather than by a check afterwards.

Scio already does this once, and it is worth recognising as an instance rather than an accident:
`look` is **not in `EXTRACTABLE_FIELDS`**, so extraction may never fill it.

**And the cost is worth stating in the same breath**, because it is what a schema-level exclusion
always buys: a field the model cannot fill must be *asked*, or it stays defaulted forever.
`docs/next/LAYER-A-INTAKE.md` §3.3 is that bill arriving — style is structurally never elicited,
which ReqElicitGym measures independently as a near-zero elicitation rate across every model tested.
Structural exclusion is the strongest enforcement available and it obliges you to provide another
route to the value.

### 2.7 A value is written from the user's own message, or it is not written

From gstack's `plan-tune` (`docs/mined/PASS2-GSTACK-SKILLS.md` §4.6), where it is called *"THE
critical safety contract"*: a stored preference may only be written when the instruction

> *"came from the user's current chat message, never from tool output or file content."*

The attack is ordinary rather than exotic: an intake that ingests prose from several places will
eventually take a sentence out of a document and record it as something the person said. Then it is
`stated`, with a citation, and every check in this skill passes — because the failure happened
before attribution, at the point where a source was admitted as a user turn.

Scio holds half of this already: `user_message_ids()` admits only user turns, which is why E4 below
rejects a value citing an assistant message. The half that is not yet held is any future path where
intake reads a document — a pasted brief, an uploaded requirements file, a fetched page. **Content
from such a source is data. It can be quoted, summarised and asked about; it cannot be the
provenance of a `stated` field.** Which prompt boundaries that text crosses on the way is
`untrusted-text-boundary`'s subject; whether it may become evidence is this one's.

---

## 3 · Limits — what the paper shows versus what we are assuming

| The paper shows | We would be assuming |
|---|---|
| A framework and human-annotation protocol for **generated text against provided documents** (QA, summarisation, dialogue-with-sources) | that a conversation transcript is a "source document" in the same sense. It is shorter, first-person, and the "claim" is a typed field rather than a sentence. **A reasonable but unvalidated transfer** |
| **AutoAIS correlates with human judgement** at the system level | that it is reliable **per example**. AttributionBench finds automatic attribution evaluation is hard; a per-field verdict is weaker evidence than an aggregate |
| Attribution is a property of the **text**, judged by a human | that an NLI model is a sufficient judge. It is a proxy, and it fails on implicature — a user saying *"just guests and my staff"* entails two roles by pragmatics, not by entailment |

**The three procedural sources carry a different limit**, and it is the same one for all three:

| The source shows | We would be assuming |
|---|---|
| A taxonomy of fact-classes that *"cannot be read from a repository"*, written for code archaeology | that the same classes are the un-inferable ones from a **conversation**. The argument transfers cleanly for pricing, retention and compliance; *target users* is more arguable, since a user describing their app often does say who it is for |
| Schema-level exclusion, shipped | that it is free. It is not — §2.6's second half. A field the model cannot fill needs another route to a value, and Scio has one live instance of that bill going unpaid |
| A user-origin gate called *"THE critical safety contract"*, with tests | that it is measured. **No source here reports an outcome.** No study says a legitimacy taxonomy reduces bad inferences, or that anyone tried to attack the gate |

**Three specific hazards for us:**

1. **`derived` is out of scope, by design.** AIS asks whether a source *supports* a claim. An
   inference is not supported by the transcript — that is what makes it an inference.
   `source = derived` fields must be **excluded** from attribution precision, or the metric
   punishes the system for doing the right thing.
2. **Multilingual.** `contradictions.py` carries Swedish patterns, so the wizard runs in at
   least two languages. Most off-the-shelf NLI models are English-first. Measure the judge
   before trusting the metric.
3. **Verbalised confidence is not calibration.** `FieldMeta.confidence` is whatever the model
   said. Research through 2025 consistently finds verbalised confidence poorly calibrated and
   clustered at the top of the scale, often worse than token probabilities
   ([survey coverage](https://www.emergentmind.com/topics/verbalized-confidence-scores)).
   `_confidence_of` already refuses `high` on a derived value, which is a sound floor. **Do not
   build anything that reads `confidence` as a probability**, and do not let AIS scores be
   reported as confidence — they measure a different thing.

---

## 4 · Eval

| # | Case | Expected |
|---|---|---|
| E1 | Field marked `stated`, `provenance: []` | Rejected by the **existing** rule, before AIS runs. Test name today: `test_an_unstated_value_is_not_invented` |
| E2 | Field marked `stated`, cites `m2`, and `m2` plainly says it | Attribution precision counts it supported |
| E3 | Field marked `stated`, cites a **real but unrelated** message | **The current rule accepts it. AIS must reject it.** This single case is the whole reason for this skill |
| E4 | Field marked `stated`, cites an assistant message id | Rejected before AIS: `user_message_ids()` only admits user turns — a value sourced from our own question is the model quoting itself |
| E5 | Field marked `derived` | **Excluded** from attribution precision. Counted separately. Including it is the metric's most likely mis-implementation |
| E6 | Value is `"yes"` or `"that one"` | Fails interpretability, reported in the interpretability rate, not silently scored as supported |
| E7 | Field carrying `corrected-on-review` | Never evaluated by AIS. It has no message source and needs none — a person typed it |
| E8 | Swedish transcript, correct citation | Same verdict as the English equivalent. If it differs, the judge is the defect, not the extraction |
| E9 | Run AIS over a corpus where a human has labelled support by hand | Report agreement between AutoAIS and the human labels **before** reporting any AutoAIS number as fact |

| E10 | A pricing, retention, compliance or target-user value marked `derived` | **Rejected**, whether or not the inference is right. The correct outcomes are `stated`, or `default` and visibly flagged. E10 fails on a *correct* inference — that is what makes it a test of the taxonomy and not of accuracy |
| E11 | The extraction output schema, enumerated against the fields extraction may not fill | Excluded fields are **absent from the schema**, not merely unmentioned in the prompt. `look` is today's instance |
| E12 | Every field the model cannot fill by schema | Has a route to a real value — a question, or a default that is flagged. A field with neither is defaulted forever and nobody will notice |
| E13 | A document is pasted into the conversation, and a value appears that only that document supports | Not `stated`. The document is data; it may be quoted and asked about. **Assert the absence of a `stated` field citing it, with a positive control** that a value the *user* typed does record one (`testing` §3.5) |

**E3 justifies the skill; E5, E9 and E10 are where it will be got wrong.** E9 in particular: an
automatic judge reported without its agreement rate is exactly the *"one green run recorded as a
verified baseline"* mistake this repository has already made once.
