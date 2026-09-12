# Q1 — green suite, confidently wrong number, where do we look

## ANSWER A

**C1 — MET.** `"revenue/transform.py:15 — to_usd() treats minor units as major units, inflating every priced total 100x."` Gives file:line and states the 100x consequence explicitly.

**C2 — MET.** `"revenue/transform.py:3-7 and :20 — GBP has no FX rate, so GBP rows are silently dropped."` ... `"North America (~$111.7K USD + GBP orders) clearly overtakes APAC... matching Finance's 'North America was the largest region by a wide margin.'"` Ties the drop to NA being understated.

**C3 — MET.** `"the output order is just aggregate()'s dict-insertion order... That alone reproduces 'APAC top, NA last' regardless of what the amounts are."` This is functionally "ranking is not a function of revenue," even without that exact phrase.

**S1 — NOT MET.** The answer is organized as "Three bugs... Look here, in this order" — no enumeration of pipeline boundaries as a set, no count of 4, no explicit ingest/egress framing.

**S2 — NOT MET.** No table or one-row-per-boundary structure anywhere; organized purely by fault.

**S3 — NOT MET.** No boundary-by-boundary marking of silent-vs-raise; the silent/loud language is attached to bugs, not to an enumerated boundary set.

## ANSWER B

**C1 — MET.** `"revenue/transform.py:15 (to_usd) never divides by 100... Every dollar figure that reaches the report is ~100x too large."`

**C2 — MET.** `"to_usd returns None for them... aggregate's list comprehension (transform.py:20) drops the Nones with no count check anywhere... understating it by roughly £497,800... enough on its own to flip NA from largest to smallest."`

**C3 — MET.** `"rank is not actually a function of revenue at all right now, it would misorder the moment the feed's row order changed."` Matches the expectation almost verbatim.

**S1 — NOT MET.** No boundary-set enumeration (ingest/egress included, count of 4) appears in this answer; it defers to "Q2/Table 1" rather than presenting one here.

**S2 — NOT MET.** No per-boundary table in this answer body.

**S3 — NOT MET.** No boundary-by-boundary silent/raise marking here.

# Q2 — review this test suite, what can't it catch

## ANSWER A

**C1 — MET.** Table 1 marks both critical internal seams OWN with explanations: `"never routes a real extract._to_minor_units output through to_usd"` (seam 1) and `"no test ever calls report.rank(transform.aggregate(...)) with transform's real field name"` (seam 2) — jointly this states no test carries real output forward across either internal boundary.

**C2 — MET.** `"row() helper (test_report.py:6-7) builds rows with key "total", matching rank's buggy key by construction; no test ever calls report.rank(transform.aggregate(...)) with transform's real field name."`

**C3 — MET.** `"both files' rec() helper... builds amount as an already-decimal float (100.0, 1000.0), never routes a real extract._to_minor_units output through to_usd, so the /100 mismatch is untestable by construction."`

**S1 — MET.** Every gap is filed under a numbered seam row (0–3), and "The list" restates each fault with its seam number: `"F1 (seam 1, scale...)"`, `"F3 (seam 2, report.rank...)"`.

**S2 — MET.** Table 1's `"control watching this seam | that control's input"` columns classify every named control as REAL or OWN, e.g. `"OWN — both files' rec() helper..."`.

## ANSWER B

**C1 — MET.** `"No test runs the pipeline end-to-end. Nothing calls revenue.run.main() or chains extract.parse_rows() → transform.aggregate() → report.render()."`

**C2 — MET.** `"Because the test's hand-built fixture and the production bug both use "total", the rank()/aggregate() key mismatch (Q1 bug #1) is invisible to the suite by construction."`

**C3 — MET.** `"No test feeds transform.to_usd/aggregate a value shaped like what extract actually emits, so the 100x scaling bug (Q1 bug #2) can never surface here."`

**S1 — NOT MET.** Several bullets are pure missing-test categories, not tied to a boundary: `"No invariant/property tests."`; `"Extract-level edge cases are untested: malformed/non-numeric amount, missing/unexpected region string, duplicate order_id..."`; `"Report-level edge cases beyond sorting: ties, all-zero totals..."` — exactly the "category of missing test" the expectation excludes.

**S2 — NOT MET.** The answer cites specific fixtures (`test_report.py`'s `row(code, total)`, `test_transform_fx.py`'s `rec(100.0)`) as illustrations inside gap explanations, but never systematically classifies each existing control by input provenance the way a per-control REAL/OWN pass would.

# Q3 — are we covered now (FX suite, post-March)

## ANSWER A

**C1 — MET.** `"No."`

**C2 — MET.** Names the unit-scale bug, the GBP-lock-in, and the untouched `report.py` rank bug — three of three.

**C3 — MET.** `"It actively asserts the GBP gap is correct behavior (test_unpriceable_currency_returns_none, line 49-50). Adding this suite made the silent-drop of GBP more locked-in, not less."`

**S1 — NOT MET.** The answer describes what the suite tests ("FX rate arithmetic — rate-table shape, plausible-band checks...") and what it misses, but never frames the answer through named boundary/seam rows or states explicitly which boundaries it watches/doesn't watch.

**S2 — NOT MET.** The closing line — `"'Newest and most thorough' here means thorough about FX rates specifically, not thorough about the pipeline."` — is scoped to *this* suite ("here"), not stated as a general rule.

## ANSWER B

**C1 — MET.** `"No — per the table above, test_transform_fx.py protects none of the three faults behind last night's number."`

**C2 — MET.** Names F1 (units), F2 (GBP), F3 (report.py never touched) — all three, at least two required.

**C3 — MET.** `"not against F2 in the sense that matters (it asserts GBP → None is correct, which is the current, questioned behavior, not a check that the drop is accounted for)"` — states the suite locks in the drop as correct rather than flagging it.

**S1 — MET.** `"Read its own row: it watches seam 1, and specifically the rate table's values..."` and `"Covering seam 1's units, seam 2, or seam 3 — no. It protects seam 1's rate-table sub-boundary only."` Explicitly answers via named boundary rows.

**S2 — NOT MET.** `"So: newest and most thorough by test count, yes. Covering seam 1's units, seam 2, or seam 3 — no."` This is the distinction applied to this suite, not asserted as a general principle (e.g. "recency/thoroughness never equal coverage").

## attack on the expectations

**The S-series across all three items presupposes one specific rhetorical form** — a seam/boundary table with REAL/OWN and silent/raise columns — as the definition of "correctly shaped," rather than defining the underlying analytical content independently of presentation. Both Q1 answers (A and B) got every C-expectation right, including exact file:lines and the exact 100x/GBP/key-mismatch triad, yet score 0/3 on shape purely because neither happened to render a table. For a question phrased as "where do we look" — which naturally invites a fault-first walkthrough — penalizing fault-first organization to zero on every shape axis looks less like measuring rigor and more like measuring whether the answer imitates a particular answer's format. That bias compounds in Q3's S1, which explicitly rewards an answer for saying "per the table above" — i.e., for having built the seam-table apparatus in an earlier, separately-graded item — over an answer that reasons soundly about coverage in prose. That's coupling one item's shape score to another item's stylistic choice, which is a strange thing for a "what does this answer cover" rubric to reward.

**S2 in Q2 ("classified by where its input comes from") demands an exhaustive per-control pass**, but nothing in the underlying question ("what can't this suite catch") requires enumerating controls that aren't part of the problem. An answer that correctly and specifically identifies the two fixtures that matter (test_report's `"total"` key, transform's dollar-float `rec()`) is doing the actually useful diagnostic work; requiring it to also taxonomize irrelevant controls as REAL/OWN adds bureaucratic completeness without added insight, and again matches one answer's table structure more than it matches the substance of "what can't be caught."

**Q2's S1 ("rather than being listed only as a category of missing test") actively penalizes an answer for being more thorough than the three seeded defects.** A reviewer who also flags "no invariant tests" or "no edge-case tests" is doing exactly what a real test-suite review should do, but that additional, honestly-labeled color drags the whole S1 score to NOT MET even when the three required gaps are correctly, individually boundary-tied elsewhere in the same answer. The expectation conflates "every sentence in the answer must be boundary-tied" with "the required gaps must be boundary-tied," which are different bars.

**Q1's C1 hard-codes "100x" as the required magnitude framing.** An answer that correctly identified the minor-units/major-units confusion but expressed the consequence as "two orders of magnitude" or simply "the report shows values inflated by roughly 100-fold" would presumably still pass, but a subtler answer that only demonstrated the effect numerically (e.g., matching a specific dollar figure) without using a multiplier word could be marked down for a phrasing gap rather than a substance gap — an unnecessarily narrow operationalization of "states the consequence."

**Q3's S2 and Q1/Q3's insistence on "a rule, not a remark about this one case"** is graded on a hair-trigger of phrasing ("here" vs. an unadorned general clause). Both Q3 answers clearly understand and imply the general principle that recency/thoroughness ≠ coverage — that's the entire thesis of both answers — but neither happens to detach the sentence from the concrete suite being discussed. Scoring this as binary MET/NOT MET rewards a specific sentence-level rhetorical move over the (present, in both cases) analytical insight it's supposedly checking for.

```json
{"items": [
  {"item":"Q1","A":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":3},
            "B":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":3}},
  {"item":"Q2","A":{"correct":true,"shape_ok":true,"c_met":3,"c_n":3,"s_met":2,"s_n":2},
            "B":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":2}},
  {"item":"Q3","A":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":0,"s_n":2},
            "B":{"correct":true,"shape_ok":false,"c_met":3,"c_n":3,"s_met":1,"s_n":2}}
]}
```