Found it. Correcting the identified rows reconciles the file to the reference at every quantile (sum within 1.5%, p50/p90/p99 all back in band) — that's the confirmation.

## `amount` is a mixed-unit column: 478 rows are in **cents**, the rest in dollars

| Merchant | Affected | Share | Evidence |
|---|---|---|---|
| `belltower` | 440 / 440 | **100%** | p50 ratio **83x** vs reference; 100% whole-number values |
| `harborview` | 38 / 240 | **16%** | whole-number rows p50 **2875.00** vs its own fractional rows p50 **29.41** |

Every other merchant sits at a p50 ratio of 0.90–1.09.

**Why column-level stats look clean.** The bad rows are 11.9% of the file and all land *above* the median, so the statistics people usually eyeball are untouched: p50 moves 29.84 → 33.96, p25 and min barely budge, nulls are zero, and the dtype stays `float`. The damage only shows in the tail and the total:

```
        reference    current    corrected
p50         29.84      33.96        29.63   ← looks fine
p90         81.23    1244.20        84.45   ← 15x
p99        208.35    8206.81       193.34   ← 39x
sum      164,315   1,989,450      166,833   ← 12x
```

Any downstream sum, mean, or revenue total is **inflated ~11.9x**.

**The two checks that caught it**, neither of which is a type or schema check:

1. **Per-segment p50 ratio vs baseline** — pooled, the shift hides; sliced by merchant, `belltower` lights up at 83x. The ratio sitting near a power of ten is the unit-change signature.
2. **Decimal-structure profile** — cents are whole numbers. `belltower` is 100% integer-valued and `harborview` 16%, against a ~1% baseline for legitimate round dollar amounts. This is what separated harborview's 38 contaminated rows from its 202 good ones, which no aggregate would have done.

**Two things worth flagging beyond the amount column**, both category-set deltas against the reference:

- `harborview` is a **new merchant** (240 rows, absent from reference) — it has no baseline, which is exactly why its partial contamination went unseen. A new-category check would have gated this feed before the unit bug ever mattered.
- `status` has a **new enum value** `chargeback` (90 rows).

One near-miss I checked and cleared: `northwind` has a whole-number `151.0`, but the reference contains legitimate round amounts up to `211.00`, so it's a real value, not cents.

The likely cause is a producer-side change where `belltower` moved wholesale to a minor-unit integer field, and `harborview` was onboarded with an integration that populates cents for some payment paths — the harborview split isn't by channel or status, so it's probably a per-transaction code path rather than a config flag.
