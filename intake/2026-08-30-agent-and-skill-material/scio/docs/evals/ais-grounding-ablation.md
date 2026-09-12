# Ablation · `ais-grounding`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.

## The discriminating rule, and why the obvious answer is wrong

§2.5, the legitimacy taxonomy: **some classes of fact may never be inferred at all — and inferring
one is an error even when the inference is right.**

> *"a per-tier limit is a business rule, and no amount of correctness makes it a discovery."*

Pricing and commercial terms, data-retention and compliance obligations, prioritisation, and target
users are the four classes mapped onto Layer A. A field in a forbidden class may be `stated`, or
`default` and visibly flagged as an assumption. It **may not be `derived`**.

The obvious answer is that inference is fine as long as it is labelled. That is the entire design
philosophy of every provenance system: mark the value, show the mark, let the user correct it. It
leads to a graded rule — infer when confident, confirm when the stakes are high — and it is wrong
because the rule is **categorical, not graded**. A correctly-inferred pricing rule with a good
citation and high confidence still fails, and the eval case that proves it (E10) is designed to fail
on a *correct* inference.

## The question

> *Our intake wizard turns what a user types into a structured project spec. If someone describes a
> subscription SaaS with a free tier and a paid tier, the model can usually work out the pricing
> model and who the target users are, even when the user never spelled it out. Is it fine to fill
> those fields in automatically as long as we tag them as inferred? Four bullets max.*

It names no skill, file or unique term, and it hands the respondent the natural wrong answer already
formed: *as long as we tag them*.

## Control answer

Verbatim:

> - **Yes, but "tagged as inferred" has to mean something downstream** — the UI must visibly
>   distinguish inferred fields from user-stated ones and let the user confirm/edit each before the
>   spec is treated as final, otherwise the tag is just metadata nobody sees.
> - **Confidence-gate it**: auto-fill only when the model's inference is high-confidence and
>   low-stakes (e.g., "target users: consumers" from an obvious consumer product); for fields that
>   materially change scope, cost, or legal exposure (pricing model, data retention, payment
>   processing), surface it as a suggestion to confirm rather than a silent default.
> - **Watch for compounding inference** — if the spec generator later reasons from an inferred field
>   as if it were confirmed (e.g., picking a payment provider based on an inferred pricing tier),
>   errors stack invisibly. Either block downstream steps from consuming unconfirmed fields, or
>   propagate the "inferred" flag through anything derived from them.
> - **Log ground truth**: keep the original user text alongside the inferred field so you can audit
>   misinference later and improve the prompt — don't let the structured spec become the only record
>   of what the user actually said.

## Treatment answer

Verbatim:

> No — not for these two fields specifically. Both fall in the taxonomy of facts a model may never
> mark `derived`, even when the inference is correct:
>
> - **Pricing model** is a commercial-terms field. `intent-driven-development`'s legitimacy taxonomy
>   (mined in `docs/mined/ECC-SKILLS.md` §2.3) explicitly bars inferring pricing/business rules and
>   requires they be recorded as assumptions for confirmation, never as discovered facts — their own
>   example, a correctly-guessed tier limit, fails for exactly this reason.
> - **Target users** is one of Layer A's six core fields and sits in the same forbidden class
>   (`docs/next` mapping in the ais-grounding skill). The taxonomy's own caveat is that this one is
>   more arguable than pricing — a user describing "my customers" often does state who it's for — so
>   check whether it's actually `stated` before assuming it needs inference at all.
> - The fix isn't "tag it and move on" — it's `source = default` with a visible flag ("we assumed X,
>   confirm?"), or a follow-up question. `derived`/"inferred" specifically means "worked out from what
>   you said," and that's not an honest description of a business-rule guess; `default` is.
> - This is a taxonomy check, independent of whether the model got it right and independent of
>   citation/AIS checks — a correctly-inferred pricing rule can be perfectly well-cited and still be
>   the wrong thing to have inferred (E10 in the ais-grounding eval).

## Comparison

| | **Control (no skills)** | **Treatment (`ais-grounding`)** |
|---|---|---|
| Top-line answer | **"Yes, but"** | **"No"** |
| Governing rule | graded: confidence × stakes | **categorical**: class membership |
| Does correctness of the inference matter? | yes — auto-fill "when the inference is high-confidence" | **no** — a right inference in a forbidden class still fails |
| Pricing model | named as high-stakes → "surface as a suggestion to confirm" | forbidden class; may not be `derived` at all |
| Target users | given as the **example of a safe auto-fill**: *"target users: consumers"* | same forbidden class; check whether it is actually `stated` first |
| The tag itself | one tag, "inferred", made visible and propagated | **two different tags**: `derived` ("we worked this out") vs `default` ("we assumed this, ask us") — and only the second is honest here |
| Relation to citation checking | not distinguished | explicitly orthogonal: a value can be perfectly attributable and still illegitimate |
| Downstream propagation | **present** — compounding inference, block or propagate the flag | absent |
| Keep the original text | **present** | absent |

The control's second bullet is a genuine partial hit and should be read as one: it independently
flags pricing, retention and payment as things to confirm rather than default. What it does not have
is the reason. Its rule is *stakes*, so it lands on the same side for pricing and the **opposite**
side for target users — which it offers as the clean example of an inference that is fine to make
silently. Under the taxonomy that is the same forbidden class as pricing.

The mechanism gap is the one §2.5 predicts: a stakes-based rule is graded, so a confident,
low-perceived-stakes inference in a forbidden class passes it. The taxonomy has no such door.

Two mechanisms in the control are absent from the treatment: compounding inference through
downstream steps, and retaining the source text for audit. Both are sound, and neither is what this
question was measuring.

## Verdict

**Changed the outcome.** The two arms give opposite answers to the question as asked — *yes, with
conditions* against *no* — and the disagreement is on the governing mechanism, not on wording. On
the specific field the question was built around (target users), the control recommends exactly what
the skill forbids, and recommends it as its own worked example.

Not measured here: the AIS/AutoAIS support check (§2.1–§2.3), which is the skill's headline content,
or the user-origin gate in §2.7. This result is about §2.5.

## Limits of this measurement

n=1 per arm, unblinded, one question, one day. No repeated seeds, so nothing separates a skill effect
from run-to-run variance. The result shows the answers differ; it does not show the treatment's
answer is *right* — §3 of the skill itself says the taxonomy's transfer from code-archaeology to
conversation is unvalidated, and calls out *target users* as the most arguable class, which is the
very class this question turned on. The treatment arm loads all 27 project skills, not this one
alone. `graphify` loads in both arms.
