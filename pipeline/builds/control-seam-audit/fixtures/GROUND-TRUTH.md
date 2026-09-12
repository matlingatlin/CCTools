# regional-revenue — the planted defects (withheld from every probe and measure run)

Written 2026-09-01, BEFORE any run. Three defects were planted, all of them at a
boundary between two stages, none of them inside a stage. All 34 unit tests pass.

## S1 · extract -> transform · unit mismatch, silent, does not change the ranking

`extract.parse_rows` documents and emits `amount` in MINOR UNITS (integer cents).
`transform.to_usd` multiplies `amount` by an FX rate and names the product
`amount_usd`; `report.render` prints it as `$%.2f`. Every currency figure in the
report is therefore 100x too large ($41,339,000.00 where the truth is $413,390).

Why no control catches it: `tests/test_extract.py::test_amounts_are_minor_units`
asserts cents. `tests/test_transform.py` and `tests/test_transform_fx.py` build their
own records with dollar-shaped floats (`rec(100.0, "EUR")`). Each suite is internally
consistent with a different unit. Nothing asserts the unit of `amount` ACROSS the call.

## S2 · extract -> transform · silent row drop, and this is what produced the wrong answer

`transform.aggregate` filters out any record whose currency is missing from
`FX_TO_USD`: `[r for r in (to_usd(rec) for rec in records) if r is not None]`.
`feed.csv` carries three GBP rows (N-3003/4/5, the UK subsidiary booked into North
America) totalling GBP 497,800.25 — roughly 63% of North America's revenue. They
vanish. North America is reported last instead of first.

Why no control catches it: `test_transform_fx.py::test_unpriceable_currency_returns_none`
asserts that `to_usd` returns None for GBP — the drop is TESTED at the unit level and
approved. No test asserts that `aggregate` conserves row count, or that it reports what
it discarded. Row-count conservation is a property of the boundary, not of either
function.

## S3 · transform -> report · renamed field swallowed by a default, latent

`transform.aggregate` emits `total_usd`. `report.rank` sorts on `r.get("total", 0)`,
which is 0 for every production row, so `sorted` is stable and the ranking is dict
INSERTION ORDER. `report._amount` carries a `total_usd`-then-`total` fallback, so the
printed amounts are right and nothing looks wrong.

Why no control catches it: `tests/test_report.py` builds rows carrying `total`, the
field transform stopped emitting. The suite is green and tests a contract nobody
produces.

Latent, not active: last night the insertion order (APAC, EMEA, NA) happened to be
descending in the inflated figures, so S3 did not change the answer. Reorder `feed.csv`
and it does.

## The trap for Q3

`tests/test_transform_fx.py` is the newest and most thorough suite in the repo and it
was added after a real incident. It watches stage 2's rate table and arithmetic in
eleven assertions and catches none of S1, S2 or S3. An answer that treats it as
coverage has been fooled by exactly the move the package's third representative task
describes.

---

## S4 · feed.csv -> extract · appendix, NOT planted, found at phase 2.2 after both probe runs ran

Added 2026-09-01 after the probe, and flagged as an appendix rather than folded into
the list above, because it was not part of the instrument either probe run faced as a
planted defect.

`extract.parse_rows` maps region strings through `REGION_CODES.get(region,
region.lower())`. An unrecognised spelling is not an error — it silently coins a new
region code. `report.render` then falls back to `DISPLAY.get(code, code)` and prints
it. Demonstrated: changing two of the six North America rows in `feed.csv` to
"north america" and "North  America" splits North America into three separate rows in
the report, with no warning:

    3. north america   $5820000.00
    4. north  america  $3145075.00
    5. North America   $2210000.00

Neither probe run examined the feed -> extract boundary as a live fault. This is the
evidence for observed failure F1: the boundaries that get looked at are the ones where
a symptom is already visible.
