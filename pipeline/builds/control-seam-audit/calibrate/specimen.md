

Seam audit of `extract → transform → report` (3 units, 4 boundaries incl. ingest and
egress). Full method: `pipeline/builds/control-seam-audit` skill.

### Table 1 — one row per seam

| # | seam | what crosses | producer says | consumer assumes | agree | fault mode | control watching this seam | that control's input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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
⁴ This is the reflex remedy flagged by the method itself: a snapshot taken from data that
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
