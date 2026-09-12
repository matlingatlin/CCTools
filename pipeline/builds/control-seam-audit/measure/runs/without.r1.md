## Q1

Three bugs, all reproducible by just running `python3 -m revenue.run feed.csv` (output matches the report exactly: APAC $41,339,000.00 top, NA $11,175,075.00 last). Look here, in this order:

**1. `revenue/report.py:16` — `rank()` sorts by the wrong key, so ranking is not actually happening.**
```python
def rank(rows):
    return sorted(rows, key=lambda r: r.get("total", 0), reverse=True)
```
`transform.aggregate()` (`revenue/transform.py:25`) emits rows with key `"total_usd"`, never `"total"`. So `r.get("total", 0)` evaluates to `0` for every row, `sorted()` becomes a no-op, and the output order is just `aggregate()`'s dict-insertion order — which follows the order regions first appear in `feed.csv`: APAC, EMEA, North America. That alone reproduces "APAC top, NA last" regardless of what the amounts are.

**2. `revenue/transform.py:15` — `to_usd()` treats minor units as major units, inflating every priced total 100x.**
```python
return {**record, "amount_usd": record["amount"] * rate}
```
`extract.py` explicitly normalizes `amount` to **minor units / cents** as an integer (see its module docstring and `_to_minor_units`, `extract.py:12-20`). `FX_TO_USD` rates (`transform.py:3-7`) are per major unit (1 JPY = 0.0067 USD). `to_usd()` never divides back by 100, so every converted total is 100x too large. Proof: APAC's JPY rows sum to 61,700,000 JPY → true value 61,700,000 × 0.0067 = **$413,390** (≈ Finance's "$0.4M"). Run it as minor units (6,170,000,000 "cents") × 0.0067 = **$41,339,000.00** — the exact number in the report.

**3. `revenue/transform.py:3-7` and `:20` — GBP has no FX rate, so GBP rows are silently dropped.**
`FX_TO_USD` has no `"GBP"` key, `to_usd()` returns `None` for it, and `aggregate()` throws those rows away ("Rows we cannot price are not part of the total"). `feed.csv` rows N-3003–N-3005 are North America's three largest orders, totalling £497,800.25, and none of it is counted. NA's reported total is just its USD rows (58,200.00 + 31,450.75 + 22,100.00 = $111,750.75 — again inflated 100x by bug #2, giving the reported $11,175,075.00). Once GBP is priced and the 100x bug is fixed, NA (~$111.7K USD + GBP orders) clearly overtakes APAC (~$413K) and EMEA (~$183.7K) — matching Finance's "North America was the largest region by a wide margin."

All three are independently sufficient to explain part of the discrepancy: #1 explains the ranking being wrong at all, #2 explains the magnitude, #3 explains why NA specifically is undercounted worst. Fix all three: change `report.rank`'s key to `"total_usd"`, divide by 100 (or keep everything in minor units end-to-end and format accordingly) in `transform.to_usd`, and add a real GBP rate to `FX_TO_USD` (plus a policy for what to do — fail loud vs. drop — when a currency truly has no rate).

## Q2

What the current 34 tests cannot catch, concretely:

- **No test runs the pipeline end-to-end.** Nothing calls `revenue.run.main()` or chains `extract.parse_rows() → transform.aggregate() → report.render()`. `tests/test_report.py:6-7` builds its own fixtures with `row(code, total)` — key `"total"` — which is *not* the key `transform.aggregate()` actually produces (`"total_usd"`). Because the test's hand-built fixture and the production bug both use `"total"`, the `rank()`/`aggregate()` key mismatch (Q1 bug #1) is invisible to the suite by construction.
- **`tests/test_transform.py` and `tests/test_transform_fx.py` never use minor-unit amounts.** They call `rec(100.0)`, `rec(1000.0, "EUR")`, etc. — plain dollar floats — even though `extract.parse_rows()` (the suite's own sibling, `test_extract.py:45-47`) proves the real contract is integer cents (`123450`, not `1234.50`). No test feeds `transform.to_usd`/`aggregate` a value shaped like what `extract` actually emits, so the 100x scaling bug (Q1 bug #2) can never surface here.
- **The FX suite hard-codes the currency gap as correct.** `test_transform_fx.py:49-50`, `test_unpriceable_currency_returns_none`, asserts GBP returns `None` — enshrining "silently drop this currency" as expected behavior rather than flagging it. There is no test anywhere asserting "every currency present in the feed has a rate" or that a dropped row is logged/counted/reconciled. A currency-completeness regression (or a future currency showing up in the feed) will pass silently forever.
</br>
- **No invariant/property tests.** Nothing checks obvious cross-stage invariants like "the top-ranked row's `total_usd` is the maximum of all rows" or "sum of rendered totals == sum of `aggregate()` totals". Either would have caught the `rank()` bug trivially without needing to know the internal key names.
- **No test exercises `feed.csv` or any multi-currency, multi-region sample file** — nothing runs the real shape of production data (mixed currencies per region, an unpriced currency mixed in with priced ones) through the full pipeline.
- **Extract-level edge cases are untested**: malformed/non-numeric amount, missing/unexpected region string, duplicate `order_id`, empty file, extra/missing CSV columns, currency in mixed case with surrounding whitespace beyond a single case.
- **Report-level edge cases beyond sorting**: ties, all-zero totals, single-currency file, very large row counts, formatting for negative (refund) grand totals.

In short: the suite is comprehensive *within* each module's own vocabulary, but every cross-module contract (units, field names, currency coverage) is asserted independently on both sides and never checked against the other side's actual output.

## Q3

No. `tests/test_transform_fx.py` is thorough about FX **rate arithmetic** — rate-table shape, plausible-band checks, linearity, zero/negative amounts, and a direct regression test for the March incident (`test_eur_regression_march_incident`, `test_transform_fx.py:33-36`). It is a good suite for what it targets. But it does not cover any of the three things that actually broke last night's run:

1. It uses the same non-minor-unit fixtures as `test_transform.py` (`rec(1000.0, "EUR")`, `rec(1000.0, "JPY")`) — never an integer-cents value like `extract.parse_rows()` really produces — so it cannot catch the 100x unit-conversion bug (Q1 #2). It tests the *rate*, never the *scale* of the input it's applied to.
2. It actively asserts the GBP gap is correct behavior (`test_unpriceable_currency_returns_none`, line 49-50). Adding this suite made the silent-drop of GBP *more* locked-in, not less — it's now a passing, named regression test for behavior that is actually the bug (Q1 #3).
3. It never touches `revenue/report.py`. The bug most directly responsible for "APAC top, NA last" — `rank()` reading `"total"` instead of `"total_usd"` — is entirely outside this suite's scope, and outside every other suite's scope too (see Q2).

So: well-covered against a repeat of the *specific* March EUR-staleness incident, not covered against unit-scale bugs, currency-completeness bugs, or cross-stage field-name bugs — which is exactly the combination that produced last night's numbers. "Newest and most thorough" here means thorough about FX rates specifically, not thorough about the pipeline.

## consulted
- regional-revenue/README.md
- regional-revenue/feed.csv
- regional-revenue/revenue/extract.py
- regional-revenue/revenue/transform.py
- regional-revenue/revenue/report.py
- regional-revenue/revenue/run.py
- regional-revenue/tests/test_extract.py
- regional-revenue/tests/test_transform.py
- regional-revenue/tests/test_report.py
- regional-revenue/tests/test_transform_fx.py
- ran `python3 -m revenue.run feed.csv` and `python3 -m unittest discover -s tests -v` in regional-revenue/
