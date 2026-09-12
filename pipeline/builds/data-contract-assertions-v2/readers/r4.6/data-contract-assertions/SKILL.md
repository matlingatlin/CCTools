---
name: data-contract-assertions
description: "PLACEHOLDER - the description is field 4.7 and is written last, from the finished body."
---

# Data Contract Assertions

Profile a feed that is already arriving, derive an explicit contract from that profile, and
assert it at the ingest boundary before anything downstream reads the batch. Then do the part
that decides whether the contract is usable: take every difference between the arriving batch
and the reference and **split it** — the ones that stop the batch (a silent unit change, a
null-rate collapse, a type or key break) from the ones that **widen the contract** (a new
category, a new partner, a new market the producer legitimately added). Listing the differences
is not the deliverable; assigning each one to a side is, and every difference must land on
exactly one. A batch profiled correctly and then quarantined whole has moved the problem, not
solved it — the onboarding batch is the one that gets refused. Where a bound cannot be derived
from the data in hand, name what it depends on rather than supplying a number that looks
principled.

## When to use
- You depend on a dataset you do not produce, and its producer can change it without telling you.
- A batch has landed and you have a prior batch, a sample, or a reference table to compare it to.
- Someone found bad numbers downstream and the question is "how long has this been wrong?"
- A check went red and nobody can say whether the producer broke something or changed something
  on purpose — and the batch is being held while that is argued.
- You are writing dbt tests, Great Expectations suites, Soda checks or SQL assertions over an
  incoming feed and do not know which to write or where to put the bounds.
- Someone has asked what drift threshold to set, or what number the alert should fire at.
- A feed has a stated SLA (landed by a time, no staler than some lag) that nothing enforces.
- Existing data-quality alerts are noisy enough that people mute, snooze, or ignore them.
- The producer has announced a change — a new column, a renamed field, an added category — and
  the existing checks have to survive it without being switched off.

**When NOT to use:** validating a model's own output against a declared schema
(`structured-llm-extraction`); choosing which production examples become an eval set
(`eval-set-curation`); sweeping the mirror sides of a code contract inside a patch
(`integration-contract-completeness`); reviewing training or serving code in a diff
(`mlops-production-review`); cheap bulk field parsing with an LLM on the tail
(`hybrid-parse-escalation`); auditing an implementation against an external spec
(`external-domain-audit`). This talent inspects the *data that arrives*, not the code that
produces or consumes it.

## Important — standing rules, true at every step

Claude Code does not re-read this file on later turns. These four hold for the whole task,
including after the numbered steps stop.

- **No number enters a contract without its derivation written beside it.** Asked what
  threshold to use, every baseline run supplied one anyway — drift bands, null-rate limits,
  quantile tolerances, row-count ranges, unseen-category limits — and presented them as
  engineering practice. One run of the eight flagged exactly one of its own numbers as
  underived and needing a business owner, and let its other seven through unflagged. A number
  is either derived here and shown, or written as `NOT DERIVED — owner: <name>` and left
  non-gating. A caveat added after the headline number does not count: in the run that gave
  one, the reader still leaves with the number. (OBS-1)
- **"This much drift is harmful" is not an argument you have.** No source in
  `references/threshold-evidence.md` connects how far a distribution moved to what it cost
  downstream, and the file states that absence and its consequences directly. Conventional
  bands do not repair it — they are conventions, and the same file records a hand-set
  threshold whose false positives got the alert silenced and the method abandoned. When
  asked for a threshold, say what the bound depends on (Step 5) and derive it, or say it
  cannot be derived from the data in hand and name what is missing. (OBS-1, C10, C12)
- **Every difference lands on exactly one side, BLOCK or WIDEN, and the two counts are
  reported separately** — in the finding list, in the verdict line, and in any pass/fail
  tally. (OBS-2)
- **Profiling, per-column typing and per-segment comparison are assumed, not taught here.**
  Every isolated baseline run found all three planted defects — including the one confined to
  a single merchant — with no skill present. The work this skill adds is the split and the
  provenance of numbers, not the detection. (observed-failures, "What the baseline is NOT
  failing at")

## Steps

```
Task Progress
[ ] 1. Difference ledger built — one row per difference, with n on both sides
[ ] 2. Every row assigned BLOCK or WIDEN; counts reported separately
[ ] 3. Each BLOCK row carries the rival benign reading and what separates it
[ ] 4. Each WIDEN row carries its contract amendment
[ ] 5. Every bound labelled noise / capacity / harm — or observe-only
[ ] 6. Provenance line written for every number
[ ] 7. Derived constraints measured on held-out reference data
[ ] 8. Contract backtested; firings counted and labelled
[ ] 9. Assertions run at the boundary; per-assertion rows emitted
```

**1. Build the difference ledger before judging anything.** One row per difference between
the arriving batch and the reference: what changed, where (column, and the segment if the
change is confined to one), the measurement on each side, and **the row count each side was
computed over**. The row count is not decoration — a statistic's firing behaviour is driven
by how many rows it sees, so a difference recorded without its n cannot be compared to the
same difference on another column or another day. Nothing is labelled a defect in this step.
(C3, C11, C13)

**2. Assign every row to BLOCK or WIDEN. This is the deliverable, not the list.** The
discriminator: does the difference contradict something the producer is committed to — a
declared unit, currency, scale or timezone; a key that is unique; a column that is never
null; a foreign key that resolves; a required column that is present — or does it *extend* a
set the producer never committed to keeping closed (a new category, a new partner or market,
a new column)? Schema change is the normal state of a production feed, and new columns and
unexpected string values are the commonest thing to fire at an ingest boundary, so a contract
with no WIDEN side is mis-specified. Write the two counts as two counts; a widen row folded
into a FAIL tally is the observed failure this step exists to prevent. A batch whose only
differences are widen rows is **ratified, not refused** — refusing the onboarding batch moves
the problem rather than solving it.
*(OBS-2: uneven, not absent — E1 rep 2 made this split cleanly and unprompted; E1 rep 1 filed
two benign category additions inside its FAIL count and verdicted "quarantine it". The step
exists to make the behaviour consistent, not to introduce it. C1, C2)*

**3. For each BLOCK row, write the rival benign reading and the measurement that beats it.**
A signature chosen to catch a defect will often also capture a segment with an innocent
explanation — a genuinely new partner with different pricing, a different mix, a different
volume. Record, per segment, the figure your signature produced, and state which segments
it separates and which it does not. If the signature captures a segment you believe benign,
it is not yet evidence: tighten it and record the separation you actually observed, or report
both readings. Do not report a defect as segment-exclusive when the data supports a second
reading. (OBS-3)

**4. For each WIDEN row, write what the contract becomes.** An amendment carries reason,
approver, effective date, and — where it changes a bound — a bound re-derived from data
gathered *after* the change, never from the firing batch alone. A large minority of anomalies
that fire at the boundary are never resolved, so an unamended widen row silently becomes a
permanently red check that people learn to ignore. (C1, C2, C10)

**5. Before writing any bound, say which of three kinds it is. Record the kind per check.**

| Kind | Derived from | What it licenses you to say |
| --- | --- | --- |
| **Noise** | the observed spread of that statistic across the reference periods, same weekday/hour/segment on both sides | "this batch is unusual" — nothing about harm |
| **Capacity** | how many firings the named owner will actually read per period, against the number of checks × batches per period | "we can afford to look at this many" |
| **Harm** | an independent downstream signal that moves — a control total that must reconcile, a bill, a labelled outcome — with the bound set at the smallest deviation observed to move it | "past here, something downstream is wrong" |

A harm bound is the only kind that answers "should this block", and it exists only where such
a signal exists. Aggregate model performance is not one unless you have measured it moving:
the reference records a study where it failed to move under real drift. A check that fits
none of the three is **observe-only** — logged, not gating — and the contract file names it
as such and states what would promote it. (OBS-1, C10, C12)

**6. Write a provenance line for every number that survives.** Fields, all of them:
statistic; the column and segment it runs on; the row count on each side; the comparison
window (which period, which weekday, which segment); the kind from Step 5; the observed
figures it was derived from; the owner; and `NOT DERIVED` where it came from outside the
data. Keep the exact and the distributional assertions visibly apart — a uniqueness, presence,
not-null, FK or declared-unit assertion has no bound to derive and no provenance line to
write, and mixing it with a banded check hides which of the two you actually justified. A
distributional number does not transfer to another column, feed or sample size: the reference
holds one measured case of a negligible perturbation over-firing at very large n and another
of a large perturbation going undetected at small n. Read
`references/threshold-evidence.md` before defending or reusing any bound. (OBS-1, C3, C11, C13)

**7. Measure the derived constraints on held-out reference data before any of them gate.**
Split the reference; derive on one part; report **coverage per constraint** on the part you
held out. Constraints auto-derived from a sample have been measured not all holding on the
remainder of the same dataset, and at least one profiler generates its expectations
deliberately over-fitted to the sample by design — so a generated suite is a starting draft,
never a shipped contract. Any constraint that does not hold on held-out data is observe-only
until re-derived or re-scoped, and the coverage figure stays in the contract file next to it.
If the plan is "switch on the tool's default configuration", record what share of historical
batches were actually bad: default configurations have been measured both over-alerting and
under-alerting, the disagreement is unresolved in the reference, and which one you get
depends on that base rate. (C6, C7, C8, C9)

**8. Backtest the proposed contract over the historical batches, then count and label.**
Per check: how many times it would have fired, and for each firing a label — defect,
legitimate change, or noise. The counted, labelled list is the artefact; a backtest whose
firings were not read has not been done. Where the total exceeds the capacity bound from
Step 5, re-derive or demote the check *before* enabling it. Muting is the terminal failure
here: once alerts are silenced, the method goes with them. (C10, C2)

**9. Assert at the boundary, on the landed raw batch, before any transform or write.** Emit
one machine-readable row per assertion: name, observed value, expected bound, kind, side
(BLOCK/WIDEN), row count, batch id — so a reader can tell which failures stop the batch and
which amend the contract without rerunning anything. Boundary validation is what turns a
silent format change from a months-long diagnosis into a short one. Note in the contract file
which consuming code was **not** exercised: a schema-level check leaves a defect class
visible only when the consumer's own assumptions are tested against the schema, and that
class does not appear in the data. (C4, C5, OBS-2)

## Bundled files

- `references/threshold-evidence.md` — **READ**, whenever a bound is being set, defended,
  reused, or challenged, and always when someone asks what threshold to use or cites standard
  bands. Holds the sources behind the threshold question with a verbatim quote, effect size,
  sample and limits per claim, plus the disagreements left unresolved and the statement of
  why no cutoff is given. Cite the claim id when you use one.
- `evals/evals.json` — **RUN** through the eval harness, not by hand; the two fixture CSVs it
  names are its inputs. Read it only when changing this skill's steps, to see which scenarios
  the wording is answerable against — it is the measurement, not the method.
