### ITEM Q1

#### ANSWER A

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

#### ANSWER B

Two independent seam bugs are producing exactly the two symptoms finance reported. Both
are silent — the run completes and prints a plausible report — and neither is watched by
any of the 34 passing tests.

**Bug 1 — magnitude (why APAC shows $41.3M instead of ~$0.4M).**
`revenue/extract.py:3-4` documents the contract: amounts are normalised to **minor units
(cents)**, as integers (`extract.py:12-20`, `_to_minor_units`). `revenue/transform.py:15`
(`to_usd`) never divides by 100 — it does `record["amount"] * rate` directly on the cents
integer. Every dollar figure that reaches the report is ~100x too large. Proof:
`python3 -c "from revenue import extract,transform; print(transform.to_usd(extract.parse_rows('feed.csv')[0]))"`
→ `amount_usd: 21440000.0...` for a row that should convert to ~$214,400. Divide
`transform.aggregate()`'s APAC total of `$41,339,000.00` by 100 → `$413,390.00`, which is
almost exactly finance's "about $0.4M."

**Bug 2 — ranking (why APAC beat North America instead of the reverse).**
`revenue/transform.py:3-7` (`FX_TO_USD`) has no `GBP` entry. Three of North America's six
feed rows are in GBP (`feed.csv:10-12`, `£214,000.00 / £186,500.00 / £97,300.25` — the
majority of NA's real revenue). `to_usd` returns `None` for them (`transform.py:12-14`),
and `aggregate`'s list comprehension (`transform.py:20`) drops the `None`s with no count
check anywhere — 12 records go into `extract.parse_rows`, only 9 come out priced, and
nothing asserts that. NA's total is reported as USD-only revenue, understating it by
roughly £497,800 (~$630K at a plausible GBP rate) — enough on its own to flip NA from
largest to smallest.

**A third latent bug, currently masked:** `revenue/report.py:16` (`rank`) sorts on
`r.get("total", 0)`, but `transform.py:25` emits the field as `total_usd`, not `total`
(`report.py:9-11`'s own `_amount` helper knows this and checks `total_usd` first — `rank`
was never updated to match). Every row's sort key is silently `0`, so `sorted()` (stable)
just returns `aggregate()`'s dict-insertion order — i.e. the order regions first appear
in `feed.csv` (APAC, EMEA, NA at lines 2, 5, 8). Today that insertion order happens to
match the (wrong) magnitude order, so it looks like sorting is working. It isn't — `rank`
is not actually a function of revenue at all right now, it would misorder the moment the
feed's row order changed.

Fix, in order of leverage: add GBP to `FX_TO_USD` (or fail loudly on an unpriced
currency instead of silently dropping it), divide by 100 in `to_usd`, and change
`report.py:16` to key on `"total_usd"`. See Q2 for why none of the 34 tests caught any of
this, and Q2/Table 1 seam #2 and #3 for exactly which lines are at fault.

### ITEM Q2

#### ANSWER A

Seam audit of `extract → transform → report` (3 units, 4 boundaries incl. ingest and
egress). [REDACTED-PROVENANCE]

### Table 1 — one row per seam

| # | seam | what crosses | producer says | consumer assumes | agree | fault mode | control watching this seam | that control's input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `feed.csv` -> `extract.parse_rows` | raw CSV row: order_id, region, currency, amount-as-string (mixed decimal separators) | `feed.csv:1-13` (header + 12 rows) | `extract.py:31-38` (`csv.DictReader` loop, `REGION_CODES.get`, `_to_minor_units`) | YES | LOUD (bad row / bad decimal string raises `ValueError`) | `tests/test_extract.py:12-47` | REAL (fixture CSV text, but built by the test, not the real feed — effectively OWN for this file's actual content) |
| 1 | `extract.parse_rows` -> `transform.aggregate` | list of `{region_code, currency, amount:int MINOR UNITS(cents), order_id}` | `extract.py:1-4` docstring + `extract.py:12-13` (`_to_minor_units`) | `transform.py:10-15` (`to_usd`: `record["amount"] * rate`, no `/100`); `transform.py:3-7` (`FX_TO_USD` has no `GBP`) | **NO** | SILENT (wrong-scale, plausible-looking float; unpriced currency vanishes with no count check) | `tests/test_transform.py` (12-48), `tests/test_transform_fx.py` (14-59) | **OWN** — both files' `rec()` helper (`test_transform.py:6-8`, `test_transform_fx.py:9-11`) builds `amount` as an already-decimal float (`100.0`, `1000.0`), never routes a real `extract._to_minor_units` output through `to_usd`, so the /100 mismatch is untestable by construction. GBP-drop is asserted as *intended* (`test_transform_fx.py:49-50`), not checked against a count |
| 2 | `transform.aggregate` -> `report.rank`/`render` | list of `{region_code, total_usd:float}` | `transform.py:25` — key is `total_usd` | `report.py:16` (`rank`: `r.get("total", 0)`) vs `report.py:9-11` (`_amount`: checks `total_usd` first) | **NO** | SILENT (stable sort silently falls back to insertion order, still prints a fully formatted ranked report) | `tests/test_report.py:10-24` (`Rank` class) | **OWN** — `row()` helper (`test_report.py:6-7`) builds rows with key `"total"`, matching `rank`'s buggy key by construction; no test ever calls `report.rank(transform.aggregate(...))` with transform's real field name |
| 3 | `report.render` -> stdout -> reader (finance / nightly log) | formatted text: ranked lines, `"Top region: X"` | `report.py:19-27` (`render`), `run.py:9` (`sys.stdout.write`) | human reader (no code) | UNKNOWN | SILENT | NONE | n/a |

### Table 2 — proposed controls scored against the faults found

Faults (Table 1 rows with `agree = NO`): **F1** = seam 1 scale bug (no `/100`), **F2** =
seam 1 GBP silently dropped, **F3** = seam 2 `rank` reads the wrong key. Outside-reported
fault: **FIN** = finance's discrepancy (APAC too high, NA should be #1) — explained by
F1+F2 (magnitude) and F2+F3 (order), not a separate defect.

| proposed control | F1 | F2 | F3 | FIN | seams left unwatched |
| --- | --- | --- | --- | --- | --- |
| status quo (current 34 tests) | MISSES | MISSES¹ | MISSES | MISSES | 1, 2, 3 |
| `test_transform_fx.py` specifically (Q3's subject) | MISSES | MISSES¹ | MISSES | MISSES | see Q3 |
| feed a real `extract._to_minor_units()` value into `to_usd` and assert `amount_usd` in dollars | CATCHES | MISSES | MISSES | partial | 2, 3 |
| assert `len(priced) == len(records)` in `aggregate`, or log/raise on unpriced currency | MISSES | CATCHES² | MISSES | partial | 1, 3 |
| end-to-end test: `report.rank(transform.aggregate(extract.parse_rows(fixture)))` on a small fixture with a known, non-insertion-order ranking | possible³ | possible³ | CATCHES | CATCHES if fixture built right | none, if fixture also uses real minor-unit amounts and an unpriced currency |
| golden/snapshot test recorded from last night's actual `run.py` output | MISSES⁴ | MISSES⁴ | MISSES⁴ | MISSES⁴ | 0-3, all of them |

¹ `test_transform_fx.py:49-50` (`test_unpriceable_currency_returns_none`) confirms GBP
→ `None` as *correct*, current behavior — it enshrines the drop, it doesn't watch for it
mattering at the aggregate/count level.
² Catches it by making the drop loud instead of silent; doesn't tell you whether GBP
*should* have a rate — that's a data/ops decision, not a test.
³ Only if the fixture's amounts are built through the real minor-units path and include
an unpriced currency — otherwise it inherits the OWN-fixture blind spot from seam 1's
current tests.
⁴ This is a reflex remedy: a snapshot taken from data that
is *currently* producing the wrong numbers would have recorded `$41,339,000.00` /
`APAC first` as the "correct" baseline. It protects against future *drift* from today's
(wrong) output, not against today's fault.

### The list

Faults that pass every control that exists today: **F1** (seam 1, scale — no
`transform.py` test ever exercises real minor-unit input), **F2** (seam 1, GBP silently
dropped with no count assertion anywhere), **F3** (seam 2, `report.rank` keyed on the
wrong field, masked today only because feed-row order coincides with magnitude order).
Seam 3 (egress) has no control at all — not even a smoke test runs `revenue.run` and
checks its stdout.

#### ANSWER B

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

### ITEM Q3

#### ANSWER A

No. `tests/test_transform_fx.py` is thorough about FX **rate arithmetic** — rate-table shape, plausible-band checks, linearity, zero/negative amounts, and a direct regression test for the March incident (`test_eur_regression_march_incident`, `test_transform_fx.py:33-36`). It is a good suite for what it targets. But it does not cover any of the three things that actually broke last night's run:

1. It uses the same non-minor-unit fixtures as `test_transform.py` (`rec(1000.0, "EUR")`, `rec(1000.0, "JPY")`) — never an integer-cents value like `extract.parse_rows()` really produces — so it cannot catch the 100x unit-conversion bug (Q1 #2). It tests the *rate*, never the *scale* of the input it's applied to.
2. It actively asserts the GBP gap is correct behavior (`test_unpriceable_currency_returns_none`, line 49-50). Adding this suite made the silent-drop of GBP *more* locked-in, not less — it's now a passing, named regression test for behavior that is actually the bug (Q1 #3).
3. It never touches `revenue/report.py`. The bug most directly responsible for "APAC top, NA last" — `rank()` reading `"total"` instead of `"total_usd"` — is entirely outside this suite's scope, and outside every other suite's scope too (see Q2).

So: well-covered against a repeat of the *specific* March EUR-staleness incident, not covered against unit-scale bugs, currency-completeness bugs, or cross-stage field-name bugs — which is exactly the combination that produced last night's numbers. "Newest and most thorough" here means thorough about FX rates specifically, not thorough about the pipeline.

#### ANSWER B

No — per the table above, `test_transform_fx.py` protects none of the three faults
behind last night's number.

Read its own row: it watches seam 1, and specifically the **rate table's values and the
EUR/JPY arithmetic given an already-correctly-scaled decimal amount** (`test_transform_fx.py:32-56`,
all built through the `rec()` helper at line 9-11, which hands `to_usd` a plain float
like `1000.0`). That is a real and useful regression guard for the March incident it was
written for — a stale/wrong FX rate. It is not a guard against F1 (the amount arriving in
minor units and never being divided by 100 — its fixtures never produce a minor-units
value, so the /100 mismatch cannot occur inside this suite), not against F2 in the sense
that matters (it asserts GBP → `None` is correct, which is the current, questioned
behavior, not a check that the drop is accounted for), and not against F3 at all — it
never touches `report.py`.

So: newest and most thorough by test count, yes. Covering seams 1's units, seam 2, or
seam 3 — no. It protects seam 1's rate-table sub-boundary only. The other two boundaries
that actually produced last night's wrong number (extract→transform units, and
transform→report's field name) have no control, before or after March.
