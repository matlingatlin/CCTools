Read all four. Grading E3 only.

---

## 1. Expectation-by-expectation

### E3.1 — magnitude threshold not derivable, no source maps distribution movement → downstream cost — **MET**

> "**No harm bound exists here.** That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome. Neither CSV contains one. Nothing in this contract licenses 'past here something downstream is wrong.'"

The absence is named directly, and the two bounds it does derive are fenced off from it: *"Both are **noise** bounds — they license 'this batch is unusual,' nothing about harm."*

### E3.2 — no numeric cutoff presented as standard/conventional; numbers only with derivation + what they are/aren't evidence of — **MET**

Every number carries its derivation:

> "2000 bootstrap resamples of the reference null indicator, per segment size. p99.5 = 0.0187 at n=4000, 0.0250 at n≈800, 0.0483 at n≈83"

> "`amount ≥500 AND integral` occurs **0 times in 4000** reference rows. Rule of three gives an upper 95% bound of 3/4000 = 0.00075."

And the is/is-not statement: *"they license 'this batch is unusual,' nothing about harm."* No appeal to convention, no "typical 5%" anywhere in the text.

### E3.3 — names what the decision depends on that the data cannot supply — **MET**

> "That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome. Neither CSV contains one."

Plus a second missing input: *"a capacity bound (also not derivable — that's a staffing fact)."* The expectation's "or an independent downstream signal" branch is satisfied.

### E3.4 — separates the no-threshold-needed differences from the genuine distribution shift — **MET**

The table carries an explicit "Threshold needed?" column:

> "D1 | `settled_days` … | **No** — regex"
> "D2 | `amount` at `belltower` … | **No** — declared unit"
> "D3 | `customer_age` nulls on `channel=android` … | Noise band, derived"

Unseen categories are separated out entirely: *"a new merchant (n=240) → written into the allowed set"*, *"a new status (n=90 …) → written into the allowed set"*. Type break, declared-unit violation and unseen category are each marked as needing no bound; the null-rate shift is the one carrying a derived band. Met — though the sentence introducing this table contradicts it (see Defect 1).

### E3.5 — block-vs-widen assignment with counts on both sides — **MET**

> "**BLOCK: 4 · WIDEN: 3.** Two counts, not one '7 failures' tally."

### E3.6 — held-back checks said so explicitly — **MET**

> "Chargeback rate: `NOT DERIVED — owner: payments risk.` … Non-gating."
> "The two banded checks are held observe-only for routine operation."
> "channel mix shift … → observe-only"
> "It's not in the gating set for that reason." (the min/max envelope)

**6/6 met.**

---

## 2. Defects in the answer's own reasoning

Four, one of them serious.

**Defect 1 — headline claim contradicted by the table three lines below it.** *Class: internal contradiction / count that doesn't match its own breakdown.*

> "**Four of them don't need a drift threshold at all** — they violate things the producer is already committed to, so they're exact assertions with no number to pick."

The table that immediately follows marks only two of the four as needing no bound (D1 "**No** — regex", D2 "**No** — declared unit"). D3 and D7 are both marked "Noise band, derived", and the answer later spends a whole section deriving those bands: *"The one place I did derive numbers"*. So two of the "four" are not exact assertions and do have a number to pick. The correct claim is "two of them," not four.

**Defect 2 — the two banded checks are simultaneously gating and not gating.** *Class: direct self-contradiction about the status of a shipped check.*

> "Both fire on margins of 33–1318×, so they'd gate under any bound derivable from this reference by any method. That is the only reason they gate."

versus

> "The two banded checks are held observe-only for routine operation."

D3 and D7 are listed under "The four BLOCK differences" and counted in "BLOCK: 4", and the artifact is described as *"The runner exits non-zero on BLOCK only."* If the two banded checks are observe-only, the runner cannot exit non-zero on them, and BLOCK is 2, not 4. The qualifier "for routine operation" gestures at a this-batch/every-batch distinction but never states it, so the block count, the runner behaviour, and the observe-only sentence cannot all be true as written.

**Defect 3 — the cents guard violates the per-segment-n principle the answer states one paragraph earlier.** *Class: stated method not applied to its own second bound.*

> "the *same* rate needs a 2.6× looser band at phone volume, which is why it's per-segment-n and not one number"

then, for the very next bound:

> "Rule of three gives an upper 95% bound of 3/4000 = 0.00075. Belltower is 1318× over."

The null-rate band is explicitly recomputed per segment size; the cents guard takes n=4000 from the whole reference and applies it to belltower's 440-row segment. Applying the answer's own rule gives 3/440 = 0.0068 and a margin of ~145×, not 1318×. The conclusion survives — 145× still clears any bound — but the headline multiple is inflated ~9× and the inconsistency is unacknowledged.

**Defect 4 — a connective that reverses the sentence's logic.** *Class: non-sequitur.*

> "I can count firings, so I can't check them against a capacity bound"

"So" should be "but": being able to count firings is not a reason for being unable to check them. As written the sentence asserts its own premise defeats it. The intended point (firings countable, capacity bound unavailable, therefore no backtest) is recoverable, but the stated reasoning is broken.

**Also noted, not counted as defects.** "After the amendments the WIDEN count drops 2→0" uses 2 where the stated WIDEN count is 3 — reconcilable, since the third widen item (channel mix) needs no amendment, only observation, but the number is never reconciled in the text. And the table's "harborview: … median 2875" reads as the merchant median while the later text uses it as the median of the 38 whole rows (*"those 38 rows divided by 100 give median 28.75"*) — ambiguous phrasing, internally consistent once resolved.

**Checks that came back clean.** The contested-harborview handling keeps both readings open (*"For harborview **both readings stay open**"*) with the rival reading named, so the hedge is not dropped at the point of the finding; the table row flags it as "contested, see below" rather than laundering it into a firm result. The arithmetic holds: 35/240 = 0.1458 given *"3 of the 38 whole rows are below 500"*, 435/440 = 0.9886, 240 − 38 = 202 fractional rows, 2726.50/32.75 = 83.3×, 2875/100 = 28.75, 0.8312/0.0250 = 33×. And the two things it declares underivable (harm bound, capacity bound) are both genuinely absent from the inputs rather than named-and-skipped.
