## Q1

### Answer A

**C1** — MET. `"revenue/extract.py:12-20" ... "Real total is 32,000,000+28,500,000+1,200,000 = 61,700,000 JPY → ×0.0067 = $413,390 ... The pipeline instead multiplies the *minor-units* amount (6,170,000,000) by 0.0067 = $41,339,000.00 — exactly the number in the report, exactly 100x too high."` File:line + explicit 100x.

**C2** — MET. `"revenue/transform.py:20 aggregate silently filters out any record whose currency isn't a key in FX_TO_USD (GBP isn't)"` and `"This is why NA, which Finance says should win 'by a wide margin,' instead comes in last: its largest currency is dropped outright."`

**C3** — MET. `"rank() sorts on r.get("total", 0) — the old key ... Every row's sort key defaults to 0, so sorted() is a no-op"` — states ranking degenerates to insertion order, not revenue.

**S1** — MET. Table 1 has exactly 4 rows: `feed.csv -> extract.parse_rows`, `extract.parse_rows -> transform.aggregate`, `transform.aggregate -> report.rank/render`, `report.render -> stdout / Finance` — ingest and egress both present, count of 4 for a 3-unit pipeline.

**S2** — MET. Every row has a "control watching this seam" cell populated with a named control (`tests/test_extract.py:35-36 test_row_count`) or explicit `NONE`.

**S3** — MET. "fault mode" column: `"LOUD-ish (a missing column raises KeyError)"`, `"SILENT for both"`, `"SILENT"`, `"SILENT until a human happens to check"`.

verdict: correct=true, shape_ok=true

### Answer B

**C1** — MET. `"**2. revenue/transform.py:15 — minor units aren't converted back to major units.**" ... "Every region's total is inflated 100x."`

**C2** — MET. `"aggregate() filters None out silently (transform.py:20) ... So North America's reported total only reflects its 2 USD rows, understating it by roughly 5x"`.

**C3** — MET. `"'ranked' output is just the original list order out of aggregate() ... it has nothing to do with revenue."`

**S1** — NOT MET. No boundary enumeration exists; the answer opens "Three independent bugs, all in `revenue/transform.py` and `revenue/report.py`" and organizes entirely by bug, never naming the ingest (feed.csv→extract) or egress (report→reader) boundaries as such.

**S2** — NOT MET. No per-boundary artefact at all — organized only by fault ("1.", "2.", "3." bugs), which is the exact disqualifier S2 names: "An answer organised only by fault does not satisfy this."

**S3** — NOT MET. No systematic per-boundary fault-mode marking; "silently" appears only as an adjective inside individual bug descriptions, not as a boundary-by-boundary classification.

verdict: correct=true, shape_ok=false

## Q2

### Answer A

**C1** — MET. `"No end-to-end test. Nothing runs extract.parse_rows → transform.aggregate → report.render together, not even against feed.csv"`.

**C2** — MET. `"It builds rows as {'region_code': code, 'total': total} (test_report.py:6-7), which happens to match what rank() reads ... This is exactly what happened."`

**C3** — MET. `"Every fixture (rec(100.0), rec(1000.0, 'EUR'), etc.) passes plain float dollar amounts directly. The missing /100 conversion ... is invisible from inside transform's own tests."`

**S1** — MET (weak but sufficient). Gaps are anchored to file:line and to specific stage pairs (`test_report.py:6-7` at the transform→report seam; `rec()` fixtures at the extract→transform seam; "No golden/regression check on the actual report output" at egress), not left as bare categories.

**S2** — NOT MET. Input-source is only narratively implied for two of the controls it names (`row()`, `rec()`); it never states, for each control, whether its input was produced by the upstream stage or built by the test file — no OWN/REAL-style classification is applied uniformly, e.g. `test_expected_currencies_present` and `test_unpriceable_currency_returns_none` are critiqued on other grounds with no input-provenance statement.

verdict: correct=true, shape_ok=false

### Answer B

**C1** — MET. `"No test ever pipes extract.parse_rows()'s output into transform.aggregate(), or transform.aggregate()'s output into report.rank()/render(). Each stage is tested against numbers the test author typed in."`

**C2** — MET. `"that file's row() helper (tests/test_report.py:6-7) still builds dicts with the old key 'total' — the test suite is, right now, testing report.py against a contract transform.py no longer produces."`

**C3** — MET. `"test_transform.py's rec() and test_transform_fx.py's rec() pass plain numbers like 100.0 or 1000.0 and never ask whether that's what extract.parse_rows would actually produce for '100.00' (it produces 10000)."`

**S1** — MET. Explicitly seam-numbered throughout: `"seam 2)"`, `"Seam 4 (report output -> Finance) has no control at all"`, tying each gap to a specific boundary rather than a bare category.

**S2** — MET. `"OWN, never REAL — see column 4 of Table 1: tests/test_extract.py:5-9, tests/test_transform.py:6-8, tests/test_transform_fx.py:9-11, tests/test_report.py:6-7 all construct their own input rather than consuming the previous stage's actual output."` Classifies every named control uniformly.

verdict: correct=true, shape_ok=true

## Q3

### Answer A

**C1** — MET. `"No."`

**C2** — MET. `"It never touches report.py, so it cannot catch the rank() reading a nonexistent total field"` (rank defect) and `"it cannot see the missing minor-units-to-dollars division"` (units defect) — at least two named.

**C3** — MET. `"It does test GBP ... but only to confirm the current (incomplete) behavior is what happens — it has no assertion that GBP volume matters or should be added."`

**S1** — NOT MET. No reference to a boundary artefact/table at all in this answer's text; it argues purely from the suite's subject matter ("scoped to one function's arithmetic," "depth on to_usd/FX_TO_USD, not breadth") rather than naming boundary rows or stating explicitly it watches none of them.

**S2** — NOT MET. The recency/thoroughness point is stated only as a remark tied to this suite: `"Being 'newest and most thorough' describes depth on to_usd/FX_TO_USD, not breadth across the pipeline"` — phrased about this specific suite's functions, never generalized into a rule.

verdict: correct=true, shape_ok=false

### Answer B

**C1** — MET. `"No."`

**C2** — MET. Table: `"F1 (units mismatch) MISSES¹ ... F2 (GBP silently dropped) MISSES² ... F3 (rank() stale key) MISSES³"` — all three named.

**C3** — MET. `"test_unpriceable_currency_returns_none asserts the drop as correct, expected, tested behavior for a single record ... because that's what it's designed to confirm, not to challenge."`

**S1** — MET. `"Table 1's control column names ... none of them is actually listed as the watching control for any seam ... Seam numbers it protects: none of the four rows in Table 1."` Explicitly answers from the boundary artefact and states it watches none of the rows.

**S2** — MET. `"Read test_transform_fx.py's row, don't weigh its recency or thoroughness."` plus `"This is a familiar shape: a control written specifically after a named incident ... 'Newest and most thorough' describes effort spent on the rate table specifically."` — stated as a general pattern/rule, not only a remark about this suite.

verdict: correct=true, shape_ok=true

## attack on the expectations

**Format-fidelity masquerading as substance (Q1 S1–S3, Q2 S2, Q3 S1).** These criteria don't test whether the answer understands the pipeline's boundary structure — they test whether the answer happened to adopt a specific audit-table scaffold (a table with a named "seam," "fault mode," and "control" column, tagged OWN/REAL/NONE). An answer that discusses ingress, egress, silent-vs-raising failure, and self-built-vs-piped fixtures entirely in prose, with equivalent or greater precision, is marked NOT MET purely for lacking the artefact shape. S2's own text makes this explicit — "An answer organised only by fault does not satisfy this" — which is a stylistic gate, not a correctness one. This systematically privileges whichever answer in a pair happens to default to tabular/columnar exposition.

**The "count of 4" heuristic (Q1 S1) is gameable and brittle.** Counting rows rewards padding (add a trivial 4th "boundary" to hit the number) and punishes substantively complete answers that fold the ingest boundary into the extract-stage discussion without a discrete numbered row. It measures a surface statistic, not whether ingress and egress were actually reasoned about.

**Q3 S1 imports a Q1-specific artefact into a differently-scoped question.** The question in Q3 is "are we covered now?" — answerable correctly and completely by naming the three defects and explaining why the March-incident suite doesn't touch them. Requiring the answer to "answer from the boundary artefact" or "name the boundary rows" makes S1 really a test of whether the same author's Q1 answer used a table, not a test of Q3 reasoning quality. Since the two items are graded independently (per the re-randomization instruction), this creates an odd dependency: an answer can be maximally correct and clear on Q3 and still fail S1 solely because it chose not to reuse a tabular format.

**Q3 S2's "rule vs. remark" distinction is subjective and hard to apply by exact-quote grading.** Nothing in the expectation specifies what linguistic marker separates a generalized rule from a suite-specific remark; two graders could reasonably disagree on whether "read this suite's row, don't weigh its recency or thoroughness" counts as a rule versus just another comment about this suite. This ambiguity lets the grading swing on phrasing rather than the underlying claim (which both answers in this item actually make in substance).

**Q3 C2's "at least two of three" bar sits oddly next to the rubric's otherwise strict, exhaustive style.** Q1's S1 wants all boundaries (with a hard count check), Q2's C1–C3 want specific named items — but Q3 C2 explicitly tolerates skipping one whole defect class. This inconsistency in strictness across the three items makes the overall rubric's rigor uneven rather than principled.

**Q1 C3 is nearly automatic once the key-mismatch is found.** Once an answer identifies that `rank()` reads a key `aggregate()` never emits and that `sorted()` degenerates to a no-op, "the ranking is not a function of revenue" follows immediately and almost tautologically — this criterion adds little discriminating power beyond restating C3's first clause, so it inflates the apparent size of the correctness rubric without testing a distinct insight.

```json
{"items": [
  {"item":"Q1","A":{"correct":true,"shape_ok":true,"c_met":3,"c_n":3,"s_met":3,"s_n":3},
            "B":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":3}},
  {"item":"Q2","A":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":1,"s_n":2},
            "B":{"correct":true,"shape_ok":true,"c_met":3,"c_n":3,"s_met":2,"s_n":2}},
  {"item":"Q3","A":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":2},
            "B":{"correct":true,"shape_ok":true,"c_met":3,"c_n":3,"s_met":2,"s_n":2}}
]}
```