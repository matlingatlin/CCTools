## Q1

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

## Q2

What the current suite (34 tests across `test_extract.py`, `test_transform.py`, `test_transform_fx.py`, `test_report.py`) structurally cannot catch:

- **No end-to-end test.** Nothing runs `extract.parse_rows` → `transform.aggregate` → `report.render` together, not even against `feed.csv`, which ships in the repo. Every one of the three bugs above only exists at a *seam* between stages, and every seam is untested.
- **`test_report.py`'s `row()` fixture hides the `total` vs `total_usd` mismatch.** It builds rows as `{"region_code": code, "total": total}` (test_report.py:6-7), which happens to match what `rank()` reads. It never uses the shape `transform.aggregate()` actually produces (`total_usd`), so a test suite that is 100% green can coexist with `rank()` silently sorting nothing. This is exactly what happened.
- **`test_transform.py` / `test_transform_fx.py` never feed `to_usd()` the minor-unit integers `extract.py` actually produces.** Every fixture (`rec(100.0)`, `rec(1000.0, "EUR")`, etc.) passes plain float dollar amounts directly. The missing `/100` conversion from cents to dollars is invisible from inside `transform`'s own tests — it's only observable once you compose it with `extract`'s output, which nothing does.
- **Currency-completeness is tested against itself, not against reality.** `test_expected_currencies_present` (test_transform_fx.py:22-23) asserts `set(FX_TO_USD) == {"USD","EUR","JPY"}` — it enshrines whatever the table already contains rather than checking it against currencies that actually occur in the feed or in the business. A missing currency can never fail this test; it would need to be added to the assertion by the same person who forgot to add the rate.
- **Silently-dropped revenue is treated as correct, not flagged.** `test_unpriceable_currency_returns_none` (test_transform_fx.py:49-50) confirms `to_usd(GBP) -> None` is *expected* behavior, and nothing checks what `aggregate()` does with that `None` (i.e., that it disappears with no count, log, or total-reconciliation check). There's no invariant test like "priced rows + dropped rows == input rows" or "dropped currency volume is reported somewhere."
- **No golden/regression check on the actual report output.** No test asserts on `revenue.run.main`'s or `report.render`'s output for a known input, so a wrong "Top region" line or wrong dollar figure in the real report has no test to break.

## Q3

No. `test_transform_fx.py` is thorough *within* `transform.py`, but the incident it prevents (a stale rate silently drifting, caught by `test_eur_rate_in_plausible_band`, `test_jpy_rate_in_plausible_band`, and the explicit `test_eur_regression_march_incident`) is a different failure mode from what happened here.

Specifically, it does not cover any of the three bugs in Q1:
- It never touches `report.py`, so it cannot catch the `rank()` reading a nonexistent `total` field — the bug actually responsible for "APAC top, North America last."
- Its `rec()` helper (test_transform_fx.py:9-11) passes plain decimal amounts straight into `to_usd()`, the same way `test_transform.py` does, so it cannot see the missing minor-units-to-dollars division — the bug responsible for the 100x-inflated figures.
- It does test GBP (`test_unpriceable_currency_returns_none`) but only to confirm the *current* (incomplete) behavior is what happens — it has no assertion that GBP volume matters or should be added, and no way to know from inside `transform.py`'s tests that GBP is actually present in production feeds and material to North America's total.

It's a good regression guard for "rate value quietly changes" — the March incident — but it's scoped to one function's arithmetic. It gives no coverage of the extract→transform unit mismatch or the transform→report field-name mismatch, which is where this run's actual error lived. Being "newest and most thorough" describes depth on `to_usd`/`FX_TO_USD`, not breadth across the pipeline; an integration test against `feed.csv` (or any fixture CSV) checking the final rendered output would have caught all three bugs immediately, and none of the four existing suites, `test_transform_fx.py` included, do that.

## consulted
- regional-revenue/README.md
- regional-revenue/revenue/extract.py
- regional-revenue/revenue/transform.py
- regional-revenue/revenue/report.py
- regional-revenue/revenue/run.py
- regional-revenue/feed.csv
- regional-revenue/tests/test_extract.py
- regional-revenue/tests/test_transform.py
- regional-revenue/tests/test_transform_fx.py
- regional-revenue/tests/test_report.py
- ran `python3 -m revenue.run feed.csv` and a small inline script calling `extract.parse_rows`/`transform.aggregate` to inspect intermediate values
