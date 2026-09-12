## Found it: `amount` is arriving in **cents** on 478 of 4000 rows (11.9%)

**Why the column-level profile passed.** The defect is segment-confined, so the robust statistics barely move: median 29.84 → 33.96 (1.14x), p25 1.07x, p75 1.38x, zero nulls, type clean, currency still `USD`. Only the tail gives it away — p90 15.3x, mean 12.1x, `sum(amount)` 12.1x.

**Where it lives.**

| merchant | n | integer-share | vs reference |
|---|---|---|---|
| belltower | 440 | **1.0000** | its own prior rate was 0.0104 |
| harborview | 240 | **0.1583** (38 rows) | no reference — new merchant |
| other 7 | 3320 | 0.0041–0.0148 | all inside the reference spread |

Cent values are whole integers; dollar values aren't. Reference int-share is 0.0095 across 4000 rows. Dividing the flagged rows by 100 reconciles them exactly — belltower `/100` against the reference gives KS D=0.045 (p=0.39), and correcting all 478 rows brings the whole batch to D=0.016 (p=0.68) and the control total to 1.015x reference, from 12.11x.

**On harborview — both readings are still open.** The signature fires on belltower and harborview and separates both from the other seven, but it does **not** separate belltower from harborview. Two measurements favour the defect reading without closing it: the 38 integers aren't round-number billing (last digits are near-uniform, only 5% divisible by 100 — values like 871, 1619, 4093), and comparing harborview *only to itself*, its integer rows vs its own non-integer rows go from KS D=0.985 raw to D=0.085 (p=0.97) after `/100`. But harborview has no reference batch at all, so "a new partner whose large orders are genuinely whole-dollar" can't be excluded from the data in hand. It blocks either way — the exact unit assertion fails under both readings. One confirmed-clean harborview batch resolves it.

**No drift threshold is involved in the block.** `currency = USD` is a commitment to major units, so E7 is an exact assertion with no bound to derive. That matters, because of the four distributional bounds I derived, held-out coverage killed three: amount-KS 0.750, null-rate 0.250, channel-mix untestable. Only the integer-share bound survived at 1.000. There's also no harm bound available anywhere in this data — it would need a reconcilable control total (processor remittance, GL figure), which isn't here.

**Ledger — BLOCK 4, WIDEN 3.** Alongside the amount defect: `settled_days` gained a `" d"` suffix on 1184 rows (type break, blocks) and `customer_age` nulls went 1.4% → 17.8% uniformly across all nine merchants (blocks, but observe-only — its bound failed held-out coverage). Widening: new merchant `harborview`, new status `chargeback` (90 rows, spread across all merchants), and a re-derived channel-mix bound. **The batch is not quarantined whole** — harborview's 202 dollar-denominated rows reconcile cleanly (D=0.037) and are accepted.

Two caveats worth your attention: the contract is `NOT BACKTESTED` — one prior batch can't produce firing counts, so every derived distributional check is held non-gating. And the new `chargeback` value is exactly the class of change a schema check can't see: if a downstream `status` mapping has an `else` branch, chargebacks may be landing in it silently right now.
