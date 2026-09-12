# Ablation · `provenance-record`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.

Two questions were run for this skill. The first discriminated weakly, the second not at all.
Both are recorded, and the verdict is taken from the pair.

## The discriminating rule, and why the obvious answer is wrong

Two candidates were tried.

**Q1 · §2 — four axes a single confidence score collapses.** `FieldMeta{value, source, confidence,
provenance}` answers *where did this come from* and leaves three questions implicit: identity over
time (which assertion is current, what it replaced), the *second* authority bit (`isStatic` — may
**time** erode this, which is orthogonal to whether it was inferred), lifecycle (when does it stop
applying, **and why**), and corroboration (how many sources). The obvious answer is one number:
reviewers ask "how much do I trust this", a scalar is what a scalar is for, and it is what almost
every extraction pipeline ships.

**Q2 · §3 — fail open on one surface, fail closed on the other.** A record with missing metadata is
**shown** on the intake surface and **withheld** on the component-offer surface. The obvious answer
is consistency: pick one policy and apply it everywhere, and a security-minded engineer picks
fail-closed. The rule says the two defaults are deliberately opposite, and that they must be
*written next to each other* or somebody eventually "fixes" one.

## The questions

> **Q1.** *Each field in our project spec stores the value plus a note of where it came from.
> Reviewers keep asking how much they should trust a given field, so we are planning to add a single
> confidence score from 0 to 1 to each one. Does that cover it? Four bullets max.*

> **Q2.** *Some of our older stored records are missing their metadata entirely — just a bare value,
> nothing saying where it came from. Two screens read those records: the review page where we show
> the user what we captured from them, and the component picker that decides which prebuilt pieces we
> offer to build with. What should the default be for a record with no metadata? Four bullets max.*

Neither names a skill, a file, or a term unique to the skill.

## Control answer

**Q1** (trimmed — closing line kept, bullet prose elided where marked):

> No — a single 0–1 score conflates several distinct things reviewers actually want to know
> separately. A few gaps:
>
> - **Source type matters more than a scalar.** "Extracted verbatim from a contract" and
>   "LLM-inferred from context" need different trust, but both can produce the same 0.73 […]
> - **Whose confidence?** A score from the extraction model, a score from a validation pass, and a
>   human override are different signals […]
> - **Calibration is unverified.** An arbitrary 0–1 float from a model is not a probability unless
>   you've checked it against outcomes […]
> - **No signal for "needs a human."** A threshold-worthy binary (verified / needs-review) is usually
>   what changes reviewer behavior […]
>
> If the goal is "reviewers know how much to trust a field," I'd lean toward pairing the score with a
> short reason code (source-type, method) rather than the float alone.

**Q2** (verbatim):

> Default should differ by screen, since "unknown" means different things to a user vs. a builder:
>
> - **Review page: label it "Source unknown" (or similar), never guess a provenance.** The user is
>   checking what was captured from them — silently attributing it to a plausible source (e.g. "from
>   your input") would misrepresent what actually happened and erode trust in every other label on
>   the page.
> - **Component picker: treat as the most restrictive/least-capable category, not as "no
>   constraint."** Missing metadata should never accidentally unlock prebuilt pieces that assume a
>   known, trusted origin — a permissive default there is a silent capability leak, not a
>   convenience.
> - **Both screens should make the absence visible, not paper over it** — this is a data-quality
>   signal (old records predating metadata capture), and hiding it removes the incentive to ever
>   backfill or migrate those records.
> - Don't invent a third, shared "default value" for the missing field itself (e.g. `source:
>   "unknown"` vs `source: "user"`) without an ADR — that's a schema/behavior decision, not a UI copy
>   decision, and belongs in `docs/decisions/` per the project's conventions.

## Treatment answer

**Q1** (trimmed, bullet headings and key clauses kept):

> No — a single scalar collapses questions that need to stay separate:
>
> - **Confidence isn't authority.** A number can't distinguish "the user said this and it may still
>   be true later" from "the user said this about a fleeting state" — you also need the `source`
>   tri-state (stated/derived/default) you already have, plus a static/dynamic bit for whether time
>   may erode it […]
> - **Confidence isn't corroboration.** A 0.9 from one message and a 0.9 from three converging
>   messages should not look the same to a reviewer — count/list the sources (you already store
>   `provenance` as message ids; a scalar throws that structure away into one number).
> - **A score can't say why it's low**, and a low score with no reason is unauditable […] If
>   confidence is meant to ever decay over time, it needs a reason string, not just a recomputed
>   number (see provenance-record §2.2 — a decay that can't say why is a documented failure mode
>   elsewhere).
> - **Decide what a score is allowed to do**, not just how it's computed: showing a low-confidence
>   field in a review UI is a different bar than letting a low-confidence field silently drive a
>   build decision. One threshold for both is a category error (§5) […]

**Q2** (verbatim):

> - **Review page: show it.** Missing provenance means unknown, not untrustworthy — treat the record
>   like `source ∈ {stated, derived, default}` all pass a fail-open check (`!== withheld`), so a
>   record with no metadata renders rather than vanishing. Hiding a fact the user actually gave you
>   is the worse error here.
>
> - **Component picker: withhold it.** Same missing metadata, opposite default — an `offerable`-style
>   check should fail-closed, since shipping a component built on an assumption with unknown origin
>   costs more than declining to offer one.
>
> - **Same reason, different verdict — write both rules in one place.** The asymmetry (display vs.
>   act-on) is what makes the two defaults consistent rather than contradictory; splitting them into
>   separate docs invites someone to "fix" one to match the other.
>
> - **Tag it, don't backfill it.** Render the review-page value labeled as "unknown source" (or
>   similar) rather than inventing a `source` value to fill the gap — a fabricated provenance is worse
>   than an honest gap, and it keeps the missing-metadata case findable instead of silently laundered
>   into `stated`/`default`.

## Comparison

**Q1 — same verdict, partly different axes.**

| Axis in §2 | **Control** | **Treatment** |
|---|---|---|
| Verdict on the single score | **No** | **No** |
| Authority — was it inferred | yes: "source type matters more than a scalar" | yes: the `source` tri-state |
| Authority — may **time** erode it (`isStatic`) | **absent** | named: static/dynamic bit, with the fleeting-vs-durable example |
| Corroboration count | **absent** | named: one message at 0.9 ≠ three at 0.9 |
| Lifecycle: a decay needs a **reason** | **absent** | named |
| Identity over time (version, supersession) | **absent** in both | **absent** in both |
| Two thresholds, display vs act | "needs a human" binary with an agreed cutoff — **one** threshold | **two** gates, and *"one threshold for both is a category error"* |
| Calibration is unverified | **named** — the treatment missed this | absent |
| Closing recommendation | score + a reason code | separate axes + two gates |

**Q2 — same conclusion, same reasoning.**

| | **Control** | **Treatment** |
|---|---|---|
| Review page | show, labelled "source unknown" | show, labelled "unknown source" |
| Component picker | most restrictive category; a permissive default is *"a silent capability leak"* | withhold; fail-closed because shipping on an unknown origin costs more |
| Asymmetry recognised | **yes** — *"Default should differ by screen"*, opening line | yes |
| Don't fabricate the missing value | yes | yes |
| Keep both rules in one document | **absent** | present |
| ADR discipline | present | absent (that is `CLAUDE.md` firing on the control) |

The control reached the asymmetry unprompted and gave the same reason for each half. On the rule
this question was designed to test, there is **nothing between the arms**.

## Verdict

**No difference.** Q2 was the sharper question and it is a clean null: the control opened by
rejecting the premise of a single default and derived both halves of the asymmetry itself.

Q1 is a weaker result in the same direction — identical verdict (*reject the single score*),
reached by a different route. The treatment supplied three axes the control did not have
(time-erosion, corroboration count, decay-with-a-reason) and the display/promotion split; the
control supplied one the treatment did not (calibration). A person acting on either answer stops
shipping the single float. **The decision does not move**, which is the standard this eval uses.

Worth recording rather than hiding: the control's Q1 answer is *good*. The instinct that a scalar
conflates source, judge and calibration is apparently already held. What the skill adds on this
question is a **more complete enumeration**, not a corrected conclusion — and a more complete
enumeration is a real thing to want, but it is not what an ablation of this shape can score.

## Limits of this measurement

n=1 per arm, unblinded, two questions, one day. No repeated seeds, so run-to-run variance is
unmeasured and a single pair cannot separate it from a skill effect. Neither question reaches §4
(enforce at write, never repair at read; branching never silently linearised) or the version-chain
rules, which are the parts of this skill most likely to be counter-instinctive and are simply
untested here — this verdict is about two rules, not about the skill. The treatment arm loads all 27
project skills, not `provenance-record` alone. `graphify` loads in both arms.
