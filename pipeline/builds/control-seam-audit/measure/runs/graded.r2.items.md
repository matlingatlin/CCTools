### ITEM Q1

#### ANSWER A

### Table 1 - seams

| # | seam | what crosses | producer says | consumer assumes | agree | fault mode | control watching this seam | control's input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | feed.csv -> extract.parse_rows | raw CSV row strings: order_id, region, currency, amount | `feed.csv` (external, no code; 12 data rows, currencies USD/EUR/JPY/GBP) | `revenue/extract.py:31-38` (`csv.DictReader` field access, one record emitted per row unconditionally) | YES (12 rows in, 12 records out, nothing dropped here) | LOUD-ish (a missing column raises `KeyError`) | `tests/test_extract.py:35-36` `test_row_count` | OWN - inline CSV literal at `tests/test_extract.py:5-9`, not `feed.csv` |
| 2 | extract.parse_rows -> transform.aggregate | `record["amount"]`: extract's docstring (`revenue/extract.py:3-4`) says **minor units (cents), int**, uniformly for every currency including JPY. Also `record["currency"]`, incl. `"GBP"`, which extract passes through untouched. | `revenue/extract.py:12-20` `_to_minor_units` - multiplies every parsed amount by 100 before rounding to int, no currency-specific exception | `revenue/transform.py:3-7` `FX_TO_USD` + `revenue/transform.py:10-15` `to_usd` - rate magnitudes (USD 1.0, EUR 1.09, JPY 0.0067) are standard USD-per-one-major-unit market rates, and `to_usd` multiplies `record["amount"]` by that rate directly with no /100 anywhere. Also: `revenue/transform.py:20` `aggregate` silently filters out any record whose currency isn't a key in `FX_TO_USD` (`GBP` isn't), with no count assertion before/after the filter. | **NO** (unit: producer emits cents, consumer's rate table expects dollars — 100x mismatch) and **NO** (count: 12 records in, 9 priced out for this feed, difference unasserted) | **SILENT** for both — run completes, prints a plausible-looking number, nothing raises | NONE for either fault. Closest are `tests/test_transform.py` and `tests/test_transform_fx.py`, but see below. | n/a (NONE) |
| 3 | transform.aggregate -> report.rank/render | `{"region_code": str, "total_usd": float}` | `revenue/transform.py:25` — returns dicts keyed `total_usd` | `revenue/report.py:16` `rank()` sorts on `r.get("total", 0)` — the *old* key. `revenue/report.py:9-11` `_amount()` (used only for the printed dollar figures) *does* check `total_usd` first. | **NO** - `rank()` reads a key `aggregate()` never emits; every row's sort key is the same default `0` | SILENT - `sorted()` with an all-equal key is a stable no-op, so "ranking" silently degrades to "whatever order `aggregate()`'s dict produced," with a plausible-looking report still printed | NONE. `tests/test_report.py` exists but see below. | n/a (NONE) |
| 4 | report.render -> stdout / Finance | Rendered text report, incl. the `"Top region: %s"` line | `revenue/report.py:19-27` `render()` | `revenue/run.py:9` writes it to stdout; a human (Finance) reads the numbers and expects them to reconcile to source data | UNKNOWN - no code-side consumer to quote; this is exactly the seam where the discrepancy was noticed, by a person, not a control | SILENT until a human happens to check | NONE - no reconciliation/golden check against an independent total | n/a (NONE) |

### Where to look, in order of what's actually driving last night's numbers

1. **`revenue/extract.py:12-20` vs `revenue/transform.py:3-15` (seam 2, units).** Extract's own docstring (`extract.py:3-4`) says amounts are normalised to minor units (cents). Transform's `FX_TO_USD` rates are ordinary dollars-per-major-unit rates and `to_usd` never divides by 100. Every priced currency is therefore reported **100x too high**. Check it directly: APAC is pure JPY. Real total is 32,000,000+28,500,000+1,200,000 = 61,700,000 JPY → ×0.0067 = **$413,390**, which is Finance's "about $0.4M." The pipeline instead multiplies the *minor-units* amount (6,170,000,000) by 0.0067 = **$41,339,000.00** — exactly the number in the report, exactly 100x too high. Same mechanism inflates EMEA and NA's USD orders 100x too.
2. **`revenue/transform.py:20` (seam 2, silent drop).** North America's three GBP orders (497,800.25 GBP total) are silently excluded from the NA total because `"GBP"` is not a key in `FX_TO_USD` — verified above by running `to_usd` over `extract.parse_rows("feed.csv")` and inspecting what comes back `None`. `aggregate()`'s docstring even says "Rows we cannot price are not part of the total" as if this is intended, with no assertion that in-count equals priced-count and no logged warning. This is why NA, which Finance says should win "by a wide margin," instead comes in last: its largest currency is dropped outright, and what's left (USD-only, $111,750.75 real) is 100x-inflated by bug 1 to $11,175,075.00 and still loses to APAC's inflated total.
3. **`revenue/report.py:16` (seam 3, stale key).** `rank()` sorts on `r.get("total", 0)`, but `aggregate()` has emitted `total_usd` since the currency work landed (per the comment at `report.py:7-8`, which someone clearly wrote for `_amount()` but never applied to `rank()`). Every row's sort key defaults to `0`, so `sorted()` is a no-op and "Top region" is really "first region `aggregate()`'s dict happened to produce" (APAC, because it's first in `feed.csv`). This run's displayed order happens to match what a correct sort-by-`total_usd` would also produce given the *buggy* (100x, GBP-dropped) totals, so it isn't the proximate cause of APAC beating NA tonight — but it is a live, silent, currently-untested defect that will silently mis-rank the moment insertion order and true magnitude order diverge, and it should be fixed regardless.

Net effect: fix 1 and 2, and North America's real total (~$743K+ once GBP is priced at a real rate, vs APAC's ~$413K and EMEA's ~$184K) puts NA first "by a wide margin," matching Finance. Fix 3 separately, because right now it is only accidentally not the cause.

#### ANSWER B

Three independent bugs, all in `revenue/transform.py` and `revenue/report.py`. Verified by running the pipeline against `feed.csv` and inspecting intermediate values:

**1. `revenue/report.py:16` — `rank()` sorts by a field that doesn't exist.**
```python
def rank(rows):
    return sorted(rows, key=lambda r: r.get("total", 0), reverse=True)
```
`transform.aggregate()` (transform.py:25) emits rows keyed `total_usd`, not `total`. So `r.get("total", 0)` is `0` for every row, every time. `sorted()` is stable, so "ranked" output is just the original list order out of `aggregate()`, which is the order regions first appear in `feed.csv`: APAC, EMEA, North America. **That's the exact order reported** ("APAC top ... North America last") — it has nothing to do with revenue. `_amount()` (report.py:7-11) correctly reads `total_usd` for display, so the numbers printed are real, just never sorted. This is the primary cause of the wrong ranking and needs to change to `r.get("total_usd", 0)`.

**2. `revenue/transform.py:15` — minor units aren't converted back to major units.**
```python
return {**record, "amount_usd": record["amount"] * rate}
```
`record["amount"]` is cents (extract.py's `_to_minor_units`), but this multiplies cents by the FX rate and calls the result `amount_usd` — i.e. dollars. Every region's total is inflated 100x. Proof: APAC is 3 JPY rows summing to 61,700,000 JPY → `61700000 * 0.0067 = 413,390` USD, i.e. ≈ **$0.4M**, matching Finance exactly. The pipeline instead reports $41,339,000.00 — 100x too high. Needs `record["amount"] / 100 * rate`.

**3. `revenue/transform.py:3-7` — `FX_TO_USD` has no GBP entry.**
`feed.csv` has 6 North America rows; 3 are GBP (214000.00 + 186500.00 + 97300.25 = 497,800.25 GBP). `to_usd()` returns `None` for GBP, and `aggregate()` filters `None` out silently (transform.py:20) — no warning, no error, no line in the report. So North America's reported total only reflects its 2 USD rows, understating it by roughly 5x in volume of GBP revenue alone. This is why "North America last" looked plausible instead of obviously broken — the number itself was quietly wrong, not absent.

Net effect: bug 3 makes North America's true total too low to begin with; bug 2 scales every region's total by the same wrong factor (so it doesn't itself change the ranking); bug 1 means the ranking was never actually computed at all, so it defaulted to feed order and put APAC on top regardless of any of the above.

Fix all three: `report.rank` key → `total_usd`; `transform.to_usd` → divide `amount` by 100 before applying the rate; add GBP (and audit for any other live currencies) to `FX_TO_USD`, and make `aggregate()` surface dropped/unpriced volume instead of silently discarding it.

### ITEM Q2

#### ANSWER A

What the current suite (34 tests across `test_extract.py`, `test_transform.py`, `test_transform_fx.py`, `test_report.py`) structurally cannot catch:

- **No end-to-end test.** Nothing runs `extract.parse_rows` → `transform.aggregate` → `report.render` together, not even against `feed.csv`, which ships in the repo. Every one of the three bugs above only exists at a *seam* between stages, and every seam is untested.
- **`test_report.py`'s `row()` fixture hides the `total` vs `total_usd` mismatch.** It builds rows as `{"region_code": code, "total": total}` (test_report.py:6-7), which happens to match what `rank()` reads. It never uses the shape `transform.aggregate()` actually produces (`total_usd`), so a test suite that is 100% green can coexist with `rank()` silently sorting nothing. This is exactly what happened.
- **`test_transform.py` / `test_transform_fx.py` never feed `to_usd()` the minor-unit integers `extract.py` actually produces.** Every fixture (`rec(100.0)`, `rec(1000.0, "EUR")`, etc.) passes plain float dollar amounts directly. The missing `/100` conversion from cents to dollars is invisible from inside `transform`'s own tests — it's only observable once you compose it with `extract`'s output, which nothing does.
- **Currency-completeness is tested against itself, not against reality.** `test_expected_currencies_present` (test_transform_fx.py:22-23) asserts `set(FX_TO_USD) == {"USD","EUR","JPY"}` — it enshrines whatever the table already contains rather than checking it against currencies that actually occur in the feed or in the business. A missing currency can never fail this test; it would need to be added to the assertion by the same person who forgot to add the rate.
- **Silently-dropped revenue is treated as correct, not flagged.** `test_unpriceable_currency_returns_none` (test_transform_fx.py:49-50) confirms `to_usd(GBP) -> None` is *expected* behavior, and nothing checks what `aggregate()` does with that `None` (i.e., that it disappears with no count, log, or total-reconciliation check). There's no invariant test like "priced rows + dropped rows == input rows" or "dropped currency volume is reported somewhere."
- **No golden/regression check on the actual report output.** No test asserts on `revenue.run.main`'s or `report.render`'s output for a known input, so a wrong "Top region" line or wrong dollar figure in the real report has no test to break.

#### ANSWER B

What the 34-test suite cannot catch, read off Table 1's control column: **every one of the four seams is NONE.** All 34 tests are unit tests of a single function called with a hand-built dict or an inline CSV literal the test file writes itself (OWN, never REAL — see column 4 of Table 1: `tests/test_extract.py:5-9`, `tests/test_transform.py:6-8`, `tests/test_transform_fx.py:9-11`, `tests/test_report.py:6-7` all construct their own input rather than consuming the previous stage's actual output). Concretely, the suite cannot catch:

- **A unit mismatch between any two adjacent stages.** No test ever pipes `extract.parse_rows()`'s output into `transform.aggregate()`, or `transform.aggregate()`'s output into `report.rank()`/`render()`. Each stage is tested against numbers the test author typed in, which are only as correct as the author's assumption about what the previous stage emits. This is precisely how the cents-vs-dollars mismatch (seam 2) survives: `test_transform.py`'s `rec()` and `test_transform_fx.py`'s `rec()` pass plain numbers like `100.0` or `1000.0` and never ask whether that's what `extract.parse_rows` would actually produce for "100.00" (it produces `10000`).
- **A currency present in the feed but absent from `FX_TO_USD`.** `test_unpriceable_currency_returns_none` (`tests/test_transform_fx.py:49-50`) tests exactly one record and asserts `None` — that's the *designed* per-record behavior, correctly tested. Nothing tests the aggregate-level consequence: that an entire region's dominant currency can vanish from its total with no error, no warning, and no assertion that `len(input) == len(priced) + len(dropped)`, or `sum(logged as dropped) == 0`.
- **A field-name drift between what a producer emits and what a consumer reads.** `report.py:16`'s `rank()` reading `"total"` while `transform.py:25` emits `"total_usd"` is invisible to `tests/test_report.py` because that file's `row()` helper (`tests/test_report.py:6-7`) still builds dicts with the *old* key `"total"` — the test suite is, right now, testing report.py against a contract transform.py no longer produces.
- **Any end-to-end / golden check.** There is no test that runs `revenue.run.main()` (or the three stages in sequence) over a known feed and asserts on the final ranking or a known-correct dollar figure. Seam 4 (report output -> Finance) has no control at all; the only "control" that exists there is a human reading the report, which is what actually caught last night's bug.
- **Record-count conservation anywhere in the pipeline.** No test anywhere asserts that the number of records/rows entering a stage equals (or accounts for) the number leaving it. That is exactly the class of defect - a filter silently dropping what it can't handle - that produced bug 2.

None of this is a criticism of the 34 tests on their own terms: each one is a correct, passing test of the function it targets in isolation. The gap is structural — every test's input is OWN, not REAL, so a contract drift between two stages that both individually pass their own tests is invisible by construction.

### ITEM Q3

#### ANSWER A

No. `test_transform_fx.py` is thorough *within* `transform.py`, but the incident it prevents (a stale rate silently drifting, caught by `test_eur_rate_in_plausible_band`, `test_jpy_rate_in_plausible_band`, and the explicit `test_eur_regression_march_incident`) is a different failure mode from what happened here.

Specifically, it does not cover any of the three bugs in Q1:
- It never touches `report.py`, so it cannot catch the `rank()` reading a nonexistent `total` field — the bug actually responsible for "APAC top, North America last."
- Its `rec()` helper (test_transform_fx.py:9-11) passes plain decimal amounts straight into `to_usd()`, the same way `test_transform.py` does, so it cannot see the missing minor-units-to-dollars division — the bug responsible for the 100x-inflated figures.
- It does test GBP (`test_unpriceable_currency_returns_none`) but only to confirm the *current* (incomplete) behavior is what happens — it has no assertion that GBP volume matters or should be added, and no way to know from inside `transform.py`'s tests that GBP is actually present in production feeds and material to North America's total.

It's a good regression guard for "rate value quietly changes" — the March incident — but it's scoped to one function's arithmetic. It gives no coverage of the extract→transform unit mismatch or the transform→report field-name mismatch, which is where this run's actual error lived. Being "newest and most thorough" describes depth on `to_usd`/`FX_TO_USD`, not breadth across the pipeline; an integration test against `feed.csv` (or any fixture CSV) checking the final rendered output would have caught all three bugs immediately, and none of the four existing suites, `test_transform_fx.py` included, do that.

#### ANSWER B

No. Table 1's control column names `tests/test_extract.py`, `tests/test_transform.py`/`tests/test_transform_fx.py`, and `tests/test_report.py` as the closest existing controls to seams 1, 2 and 3 respectively — and none of them is actually listed as the watching control for any seam, because each is OWN-input (column 4: OWN, not REAL) and none crosses a boundary. Read `test_transform_fx.py`'s row, don't weigh its recency or thoroughness. Its 10 tests all call `transform.to_usd()` / read `transform.FX_TO_USD` directly, using its own `rec()` helper (`tests/test_transform_fx.py:9-11`) with arbitrary numbers (`1000.0`, `0.0`, `-100.0`) that never pass through `extract.parse_rows`. It protects the arithmetic *inside* `transform.py` — that the rate table has the right keys, the right sign, the right ballpark, and multiplies correctly. It does not protect, and was never pointed at, the boundary where `extract.py`'s minor-units output meets `transform.py`'s major-units-shaped rate table. **Seam numbers it protects: none of the four rows in Table 1.**

Scored against the three faults from Q1 (F1 = units mismatch, F2 = GBP silently dropped, F3 = `rank()` reads stale key):

| proposed control | F1 (units mismatch) | F2 (GBP silently dropped) | F3 (rank() stale key) | seams left unwatched |
| --- | --- | --- | --- | --- |
| `tests/test_transform_fx.py` (existing) | MISSES¹ | MISSES² | MISSES³ | 1, 2, 3, 4 (all of them) |

¹ Its fixture amounts are hand-picked numbers, never `extract.parse_rows` output, so a 100x unit error between the two stages cannot appear in any assertion.
² `test_unpriceable_currency_returns_none` asserts the drop *as correct, expected, tested behavior* for a single record — it cannot flag that this same behavior silently guts a whole region's total, because that's what it's designed to confirm, not to challenge.
³ It never imports or calls anything in `report.py`.

This is a familiar shape: a control written specifically after a named incident (the March stale-FX week, per `README.md:15-17` and the docstring at `tests/test_transform_fx.py:1-3`), aimed carefully at the failure mode it was built for (a wrong *rate*), passing throughout a run whose defect sits one seam upstream (a wrong *unit* feeding a correct rate) and one seam downstream (a stale *key* reading a correctly-computed total). "Newest and most thorough" describes effort spent on the rate table specifically; it says nothing about the three other seams in Table 1, all four of which remain NONE after this suite runs. Being covered would mean a row in Table 1 naming it with REAL input; no such row exists.
