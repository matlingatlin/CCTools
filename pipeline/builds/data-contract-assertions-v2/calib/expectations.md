# 6.2 — the expectation set

**Provenance, stated because the rule exists to be checkable.** These were written AFTER the
twelve arm outputs were produced and blinded, and FROM the blinded copies, under their
per-item labels A/B/C, with the key withheld in `KEY_DO_NOT_OPEN/key.json` and unopened at
the time of writing. Labels are re-randomised per item, so no label carries information
across items. Expectations marked **[FIXTURE]** are computed from the CSV rows and the
withheld scoring key and could have been written at any time; no arm's output can move them.

**Bounded honestly: blinding by label is not blinding by prose.** Four of the twelve answers
use the method's own vocabulary — "BLOCK/WIDEN", "NOT DERIVED — owner:", "NOT BACKTESTED",
"observe-only", "held-out coverage". A grader can therefore separate a method-armed answer
from a bare one. It CANNOT separate the two method-armed arms from each other, which is the
comparison that decides this build, and that is the same bound the previous build recorded.

## Scoring

One point per expectation met. Reported as percentage of expectations met, per arm, over all
four items. An expectation neither met nor refuted is NOT MET, never skipped.

---

## E1 — derive a contract and say what today's batch does to it

| # | Expectation | Kind |
|---|---|---|
| E1.1 | Names the amount unit change and locates it in the belltower segment. | [FIXTURE] non-discriminating |
| E1.2 | Names the customer_age null collapse and scopes it to the android channel, not only as the whole-column 1.4→17.8 percent figure. | [FIXTURE] non-discriminating |
| E1.3 | Names settled_days ceasing to parse as a number, with the affected row count in the region of 1184. | [FIXTURE] non-discriminating |
| E1.4 | Assigns the new merchant harborview and the new status chargeback to a WIDEN / ratify / amend-the-contract side, explicitly, and NOT to the side that stops the batch. | discriminating |
| E1.5 | Reports the blocking differences and the widening differences as TWO SEPARATE COUNTS or two separate labelled lists, rather than one failure tally or one whole-batch verdict. | discriminating |
| E1.6 | Treats the channel mix shift as no-action or observe-only rather than as a defect. | [FIXTURE] non-discriminating |
| E1.7 | Any numeric bound it proposes is either derived from a named input with the derivation shown, or explicitly marked as not derived and non-gating. An answer that proposes no bound at all also meets this. | discriminating |

## E2 — write the assertions to run on every batch

| # | Expectation | Kind |
|---|---|---|
| E2.1 | No assertion pins the row count to 4000 or to a fixed band around it without stating how the band was derived. | [FIXTURE] discriminating |
| E2.2 | An unseen merchant or status value routes to a decision, amendment or review rather than to an automatic hard block. | discriminating |
| E2.3 | At least one assertion is evaluated PER SEGMENT rather than only over the whole column. | non-discriminating, regression guard |
| E2.4 | Every numeric bound in the suite carries either its derivation or an explicit not-derived marker with an owner or a non-gating status. | discriminating |
| E2.5 | States what it could NOT derive from the data in hand, naming the missing input, rather than supplying a placeholder number silently. | discriminating |
| E2.6 | Distinguishes exact assertions that need no bound (type, uniqueness, declared unit, unseen category) from distributional ones that do. | discriminating |

## E3 — what threshold should we use

| # | Expectation | Kind |
|---|---|---|
| E3.1 | Says that a magnitude threshold cannot be derived here because no available source maps how far a distribution moved to what it cost downstream — or names that absence in its own words. | discriminating, THE NAMED AXIS |
| E3.2 | Does not present any numeric drift cutoff as standard, conventional or principled practice. Proposing a number is permitted only where the answer shows the derivation and says what the number is and is not evidence of. | discriminating, THE NAMED AXIS |
| E3.3 | Names what the decision depends on that the data cannot supply — at minimum the consumer and the cost of a bad batch reaching them, or an independent downstream signal. | discriminating |
| E3.4 | Separates the differences that need no threshold at all (type break, unseen category, declared-unit violation) from the one genuine distribution shift. | [FIXTURE] non-discriminating |
| E3.5 | States the block-versus-widen assignment with counts on both sides. | discriminating |
| E3.6 | Where it holds a check back rather than gating on it, it says so explicitly (observe-only, non-gating, provisional) rather than shipping it as a gate. | discriminating |

## E4 — the amount column, when column statistics look fine

| # | Expectation | Kind |
|---|---|---|
| E4.1 | Identifies the defect as a unit or scale change, not as a set of large outliers. | [FIXTURE] non-discriminating |
| E4.2 | Locates it by segment and names belltower. | [FIXTURE] non-discriminating, regression guard |
| E4.3 | States why a whole-column statistic missed it, with the segment-versus-column comparison. | [FIXTURE] non-discriminating |
| E4.4 | On harborview, either reports both readings as open, or states which measurement separates it from belltower and which does not. An answer that asserts harborview is definitely affected, or definitely clean, with no rival reading, does NOT meet this. | discriminating |
| E4.5 | Any repair rule it proposes carries the case it would get wrong. | discriminating |

---

## What this set does NOT decide

- It does not test the shape gap the build was opened on. A description 422 characters over
  the listing cap is a ROUTING defect and no answer-quality expectation can see it. That is
  measured separately at 6.5, against the incumbent's own truncated description.
- It does not test the skill on a real feed. Every expectation is scored against one planted
  fixture, and 6.6 records that as unmet.
- Five of the twenty-four expectations are marked non-discriminating and two of those are
  regression guards. They are counted, and a win resting on them would be a rubber stamp.
