# Review — paired-comparison-blinding

Reviewer: independent read of `SKILL.md`, `references/position-bias-evidence.md`,
`evals/evals.json`. 16 findings. Most serious: **F1**.

One line of credit before the findings: the artefact tells you where it stops. The body's
"What none of it establishes is that per-**item** relabelling beats a single fixed
assignment" and the reference's `*Verification:* gathering agent only - NOT independently
re-checked by the coordinator` are the kind of disclosure most skills omit. The findings
below are about what happens between those two honest sentences.

---

## 1. What / when / how — and what a reader still has to guess

The what and the when are unambiguous. The description carries the trigger set ("A/B prompt
tests, with-and-without skill runs, model bake-offs") and the body opens with the mechanism
("A judge that can tell which side is the new one is not scoring the answers"). The how is
six imperative steps, which is the right shape.

Five things a reader must supply themselves.

**F7 — Neither bundled file has a read instruction.** The reference is named once:

> `references/position-bias-evidence.md` carries the sources and their verbatim lines.

That is a mention, not a load rule. Nothing says when a reader should open it, what it
would change if they did, or that it holds the boundary conditions (judge-specificity,
quality-gap dependence) the body does not carry. `evals/evals.json` is bundled and never
appears in the body at all. The BOM justifies both files; the body accounts for neither.

**F8a — "Relabel" to what?** The body never names the labels. It says:

> **Relabel per item, not per run.**

The reference indicts specific label strings — Claude-v1 "shows a name bias which makes it
favors 'Assistant A'". So the reader is left to guess whether A/B is acceptable, and the
obvious default is the one label pair the evidence names as biased. The repo instance uses
A/B. Nothing in the method says whether that is a considered choice or a leftover.

**F8b — What is the seed, and what stops the grader reading the key?** The body says:

> Write the key to a file the grader is never given,

with no mechanism. In the repo instance (`pipeline/evals/harness/blind.py:107-108`) the key
lands in the same `runs/` directory as the grader prompt; the only thing withholding it is
which path a human pastes. For an agent grader holding a Read tool that is not a control at
all. The method should say the key must live outside the grader's reachable scope, or that
the grader must have no filesystem access — it says neither.

**F8c — "seeded function of the item id" leaves the seed unspecified.** Reproducible across
what — reruns of the same comparison, or across comparisons? The instance seeds on
`skill|repeat|qid`; the body does not say the run identity must be in the seed, and later
asks you to "stamp the key with a run id or input hash," which is a different mechanism for
an adjacent problem. A reader has to reconstruct the relationship.

---

## 2. Rules that do not end in something checkable

Four of six steps land on an artefact you could assert against. Named for credit: the key
file, the one sentence in the grader prompt, the inversion control, and the four
unresolvable-row conditions ("An unknown label, a result with no key entry, a key entry
with no result, a duplicate id") — that last is the most testable line in the file.

**F9a —**

> so the assignment is reproducible without being predictable from the data.

"Not predictable from the data" names no test that could fail. There is no threshold, no
adversary model, no check. A `qid % 2` assignment is reproducible and trivially predictable;
nothing in the rule rejects it.

**F9b —**

> Read it for its critique of the rubric, never for its result.

A reading habit with no artefact. Contrast the same step's first half, which is checkable
(the tally derives only from per-item rows).

**F9c —**

> Design the control for that first.

An ordering instruction with nothing that records whether it was obeyed.

---

## 3. Opinions stated without warrant

**F3 — The framing claim of the whole skill has no warrant anywhere in the artefact.**

> ## Important — the danger is at the un-blinding, not the blinding
> Getting the labels on is easy and visibly wrong when it fails. Getting them back off is the
> step where a bug **inverts** the result

This is a claim about relative failure rates of two steps. No measurement, no incident, no
source. The reference contains nothing about un-blinding bugs — all four sources are about
judge behaviour, none about mapping code. It may well be true; it is asserted.

**F2 — The load-bearing step is unwarranted, and the artefact says so itself.** Step one is
"Relabel per item, not per run," and its rationale —

> One fixed assignment across the whole set gives the judge an answer to work from after the
> first item it guesses.

— has no evidence behind it. No cited source tests whether a judge infers a fixed assignment
across items. The artefact concedes this in its own words:

> What none of it establishes is that per-**item** relabelling beats a single fixed
> assignment. That remedy is not measured in the literature cited, and the only measurement
> behind it is local and small.

Disclosed is better than hidden. But the disclosure sits 30 lines below the imperative, and
the imperative is what a reader executes. The skill's primary instruction rests on a
plausible mechanism story, and the reader has to reach the last section to learn it.

**F10 — The "one sentence" rule states a causal claim whose only warrant is confounded, and
the body drops the confound.** Body:

> Without it the grader writes a cross-item narrative — "A was consistently stronger" — that
> describes labels rather than arms

Reference:

> 2 of 2 graders not told about re-randomisation asserted a cross-item identity, against 0 of
> 6 told. n=8, and the two rounds differ in more than that one sentence.

"The two rounds differ in more than that one sentence" is an admission that the comparison is
confounded. The body states the effect as if it were isolated. This is a small n=8 result
carrying a flat causal sentence.

---

## 4. Does the evidence support the rules? (the important one)

### F1 — The evidence measures ORDER. The method changes LABELS. The steps never mention position at all.

This is the finding. Nearly every claim in the reference is a position claim:

> We find that the quality ranking of candidate responses can be easily hacked by simply
> altering their **order of appearance** in the context.

> *Measured:* Conflict Rate = proportion of items on which the judge's winner changes when
> only the two responses' **positions** are swapped.

> *Measured:* Consistency = percentage of cases where the judge gives the same result when the
> **order** of the two assistants is swapped

And the one production mitigation documented is an order mitigation:

> 'you can enable response flipping, where half of the calls to the judge model flips the
> baseline model and candidate model response'

Exactly one claim addresses the label channel — the MT-Bench `rename` prompt — and its own
row limits it hard:

> *The source's own limits:* The paper does not state which new names the 'rename' prompt
> uses, and reports the name effect for one judge (Claude-v1) only; the two other judges
> showed small changes.

Now the method. Every step is about labels: "Relabel per item"; "Write the key"; "Tell the
grader the labels are re-randomised"; "a swapped **key** produces the opposite verdict"; "An
unknown **label**". The word slot appears once in the whole body, and only in the evidence
summary, never in an instruction:

> the effect sits partly on the **label** and not only the slot

The body knows the slot channel exists, correctly reports that the evidence puts most of the
mass there, and then issues a procedure that does not address it. A reader who follows these
six steps literally — randomise which label each arm gets, per item, print the new arm second
every time — has preserved intact the 5.0%–82.5% conflict rate the reference documents, and
has mitigated only the channel measured for one judge in one table.

The repo instance escapes this by accident, not by instruction: in `blind.py`, `A` is always
printed first, so flipping the label necessarily flips the slot. That coupling is a property
of the print layout. Nothing in the method requires it, states it, or warns that decoupling
label from position guts the technique. **The method must say the arms' positions are
randomised, not only their names — or say explicitly that the label must be bound to the
slot.** As written it is silent on the one variable every source manipulates.

### F4 — "tens of percent" drops the low end of the measured range.

Body:

> swapping only the order of two candidates reverses a judge's verdict often enough to be
> measured in the tens of percent

Reference:

> Rates ranged from **5.0%** to 82.5% depending on judge and candidate pair.

5.0% is not tens of percent. The dropped low end is the wide-quality-gap case, which is
precisely the condition the body invokes two clauses later. The body compresses a 16-fold
range into one phrase and loses the conditional it then relies on.

### F5 — "does not work" is stated absolutely; the source tested one phrasing.

Body:

> telling the judge to ignore that does not work.

and

> instructing the judge to ignore order does not remove it.

Reference:

> *The source's own limits:* **Single de-biasing phrasing tested**; the paper does not sweep
> alternative instructions.

The claim "instructions do not remove it" is warranted. The claim as a general fact about
instruction-based remedies is not, and the body states the general version twice. This
matters because eval 4 tests exactly this rule.

### F6 — Judge-specificity is documented in the reference and absent from the body.

The reference is emphatic that the magnitude and even the direction are judge-dependent:

> GPT-4 exhibits a preference for the first displayed candidate response ... This bias is also
> present in ChatGPT, which typically favors the second response.

> Claude-v1 consistency 23.8% ... GPT-3.5 46.2% ... GPT-4 65.0%

> *Effect:* ... GPT-4 and GPT-3.5-Turbo flip preference direction across datasets

The body carries none of this. It prescribes one uniform procedure and never tells a reader
that the cost/benefit varies by a factor of three across judges, nor suggests measuring their
own. A reader cannot tell from the body whether this is worth doing for the judge they have.

### F16 — Reference-internal: the verification line is pasted identically under all nine claims and is wrong for most of them.

Every claim ends with the same string, including S1 and S2 rows whose locators are sections
and figure captions:

> *Verification:* coordinator re-fetched the full text independently and string-matched this
> quote; 9 of 9 arXiv quotes matched (S3 against the abstract, as its locator states)

The parenthetical is a global note about S3 reproduced under S1 and S2 claims where it makes
no sense. It is boilerplate, and boilerplate in a per-claim verification field is the
mechanism by which verification stops being per-claim. Fix: one global verification note, or
a genuinely per-row line.

---

## 5. Do the evals test the teaching, or recall of it?

Two of five discriminate. Three are gradeable by paraphrase of the body.

**F11 — Eval 1's first three expectations restate the body's first three steps.** They are:

> "the produced grading setup relabels per item, not once for the whole set"
> "a key is written somewhere the grader does not receive"
> "the grader's instructions state that the labels are re-randomised per item"

Against the SKILL.md, these are recall. Worse, they are gradeable on assertion: an answer
that emits one fixed A/B mapping for all twelve tickets while *saying* it relabels per item
satisfies expectation 1 as written, because nothing requires the twelve differing assignments
to be exhibited. The only expectation doing work is the fourth —

> "the answer produces the prompt or the setup, not a description of one"

— and that is a format check, not a correctness one. Missing from eval 1: any check that the
twelve assignments actually differ; any check that the grader prompt is free of arm-revealing
wording; and, per F1, any check on position.

**F12 — Eval 3's third expectation cannot fail.**

> "computes the headline from the per-item rulings instead"

The prompt supplies no per-item rulings. No answer can compute anything; an answer that
promises to compute passes identically to one that does. Expectations 1 and 2 of that eval
are good — "asks or establishes whether the labels were re-randomised" is a real conditional.

**F13 — Eval 4 passes on a bare citation.**

> "attributes that to a source it read rather than asserting it bare"

"Research shows instructions don't fix this" or a naked "Wang et al. 2023" satisfies this. A
wrong answer citing the right paper for the wrong finding passes. The discriminating version
would require the specific fact: that the de-biasing instruction *was already in the template*
that produced the 46.3%/82.5% conflict rates.

**Eval 5 is one sentence of recall** of body line 53 ("it is largest when the two candidates
are close"). Fine as a pressure trap, but a model holding the body passes without
understanding.

**Eval 2 is the good one.** "at least one test asserts that a swapped or inverted key changes
the verdict, not just that mapping runs" is a genuine discriminator that a baseline plausibly
fails, and expectation 3 is the only place the loud-failure rule is tested at all.

**F14 — Three gaps in the suite.**
- **No negative-trigger case.** The house standard requires one. Nothing tests that this skill
  declines a judge-vs-human-labels calibration request, a single-arm quality review, or an
  ordinary code review. Given `llm-judge-calibration` exists in the same library, this is the
  omission with a named victim.
- **No eval on the artefact's own honesty boundary.** The highest-value eval available is:
  "is per-item relabelling proven better than a fixed assignment?" — where the correct answer
  is *no, our own reference says that is unmeasured.* An artefact that discloses a limit and
  never tests whether a reader carries the limit forward has documented it, not taught it.
- **No eval on order/position**, mirroring the body's silence (F1), and none on the run-id /
  input-hash stamping rule.

---

## 6. Collisions

**`llm-judge-calibration` — real collision, and this description does nothing about it.** Both
units answer some form of "can I trust this judge's verdict". A user typing "our judge's
scores seem unreliable" or "the judge disagrees with itself" could route to either. The
description here ends without a single NOT-clause — unusual in this library, where the
neighbouring entries all carry explicit "NOT for X (use Y)" boundaries.

Routing a reader should get, and does not: **pick `paired-comparison-blinding` when the
question is how to present two arms to one grader and map the labels back afterwards — a
protocol question, answered before any grading happens. Pick `llm-judge-calibration` when the
question is whether the judge's scores track human judgement at all — a validity question,
answered on labelled data.** They compose in that order: blind the protocol, then calibrate
the judge inside it. Calibrating an unblinded judge measures the judge plus the position
artefact and cannot separate them.

**`oracle-weakening-audit` — narrow overlap, low risk, worth a cross-reference.** The
overlap is a single idea, and this body states it well:

> A round-trip test — map the labels on, map them off, get the originals back — passes just as
> happily when the mapping is inverted.

That is a weak-oracle finding in `oracle-weakening-audit`'s own idiom. The units divide
cleanly on time and target: **`oracle-weakening-audit` is retrospective and runs on production
code whose suite went suspiciously green, grading assertion strength by mutation.
`paired-comparison-blinding` is prospective and designs one control in an eval harness before
the comparison runs.** No overlap in trigger, so no mis-fire expected; a mutual "see also"
would serve a reader who arrives from the wrong side.

**F15 — the unlisted neighbour: `skill-measure`.** It also owns paired with/without runs in
the same turn against a preregistered threshold. This skill is the blinding sub-protocol
inside that; nothing in either description says so. Worth resolving before this ships into
the routing table.

---

## What would change the verdict

In priority order: state the position/slot requirement in the steps (F1); either measure the
per-item rule or demote it from an imperative to a stated preference (F2); add the negative
trigger and the honesty-boundary eval (F14); add the NOT-clause naming `llm-judge-calibration`
(F15); carry the judge-specificity boundary into the body (F6).
