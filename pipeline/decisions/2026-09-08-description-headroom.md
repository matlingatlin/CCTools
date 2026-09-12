# Preregistered rule — trimming descriptions for truncation headroom

**Written 2026-09-08, before any candidate description was opened.** The point of writing it
first is that the result must not be allowed to move the bar; this repo has a talent for exactly
that failure (`preregistered-decision-rule`).

## The problem, already measured

`DESCRIPTION_LISTING_TRUNCATION` is **1,536** characters — the host's silent wall, not our
authored cap. Truncation takes the **tail**, and this library's house style puts the NOT-clauses
at the tail. So the next disambiguator added to a near-wall description is *removed by the act of
adding it*, with nothing reporting it. Three descriptions sit 90–94 characters under the wall.

## The target, and why this number

Not "as short as possible", and not the authored 1,024 cap either — that would be a 29% cut on
the largest, which cannot be meaning-preserving. The target is **headroom for one more
NOT-clause**, sized from the ones this library actually writes:

- 69 NOT-clauses across 62 of 92 descriptions.
- min 41 · **median 189** · mean 219 · **p75 306** · p90 405 · max 537.

**Target: ≤ 1,230 characters** (1,536 − 306, the p75 clause). Median headroom would leave half of
the library's own clause-writing habits unaccommodated; p90 would force cuts that lose meaning.
p75 is the defensible middle, and it is chosen from the distribution **before** any candidate was
read.

## Constraints — a cut that violates any of these is not made

1. **Zero distinct trigger tokens lost.** Measured mechanically: the set of content words
   (lowercased, stopwords and punctuation removed) present before must be present after.
2. **Zero NOT-clauses lost.** Counted with the same regex that produced the distribution above.
3. **The `Use when…` opening is preserved.**

## Stop rule

A description that cannot reach 1,230 without violating 1–3 is **reported as uncuttable**, and
left alone. That is a finding about the library, not a failed pass — and it is the outcome this
rule exists to make sayable.

## What would falsify the whole exercise

If every candidate turns out uncuttable, the conclusion is that the wall must be respected by
*splitting* a talent or by shortening the NOT-clause being added — not by trimming. Recording
that in advance is the point.

---

## Outcome, same day — and the rule was NOT executed

Stated plainly, because a preregistration that quietly reports a different experiment is worse
than none: **no description was trimmed.** The rule above was written to govern a trimming pass,
and the trimming pass did not happen. What follows is what happened instead and why.

**Feasibility was measured, and my first reading of it was wrong.** Counting only *duplicate*
content words gave 97–187 recoverable bytes against a 66–216 need, which reads as "three of five
are impossible". That ignored stopwords, punctuation and connective prose, which are the bulk. The
real floor — every distinct content word present exactly once, single-spaced — is **867–1,011
characters**, leaving **429–488 bytes of slack** against the 66–216 needed. All five are trimmable
in principle, comfortably.

**So the blocker was never feasibility.** A description edit changes *routing*, and this library's
own standing rule is that such a change is proven against a baseline (`skill-measure`) — which
needs a run, not an opinion. Trimming five dense descriptions on my own judgement, unmeasured,
in the same pass that built the rule, would have been the thing the rule was written to stop.

**What was built instead: a gate, because the failure is silent.** The risk is not that these five
are long; it is that the *next* NOT-clause added to one of them is deleted by the act of adding it,
with nothing reporting it. `pipeline/queries/desc_headroom.py --gate` fails when a description
crosses the wall, when an undeclared one crosses the target, and — the part that matters — when a
**declared one grows by a single character**. The five are named in `GRANDFATHERED` with the length
each had today. That is not an amnesty: it covers exactly the failure mode, for all 92, from now.

**The live proof found what the fixtures could not.** With the target recomputed from the current
p75, padding a description during the test moved the target from 1,230 to 1,231 — *a threshold
derived from the population it judges can be raised by the very edit it should refuse.* The target
is now frozen in `CONSTANTS.md` as `DESCRIPTION_HEADROOM_TARGET`, with today's p75 printed beside
it so drift stays visible without being automatic. Eleven fixtures, six mutations, all caught;
two live proofs (a grandfathered description growing by one character, and an under-target one
crossing) both fail the gate and were reverted.

**Still open, and owned by this document:** trimming the five. It needs a paired trigger
measurement, not a session of judgement. Deleting a name from `GRANDFATHERED` is the finished job.
