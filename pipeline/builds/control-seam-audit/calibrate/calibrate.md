## Ruling

**S1 — NOT MET**

The header claims a complete 4-boundary set: *"Seam audit of `extract → transform → report` (3 units, 4 boundaries incl. ingest and egress)."* But Table 1 only ever enumerates three rows, starting at:

> `| 1 | \`extract.parse_rows\` -> \`transform.aggregate\` | ... |`

There is no row for the feed file entering `extract.parse_rows` — the first row already assumes data is inside the pipeline. The egress boundary is present (row 3: `report.render -> stdout -> reader`), but the ingest boundary is asserted in prose ("4 boundaries incl. ingest") and then never actually appears in the enumerated set. The set delivered has 3 members, not 4, and is missing ingest specifically.

**S2 — NOT MET**

Of the three boundaries that *are* listed, each does carry a named control or NONE (`tests/test_transform.py (12-48), tests/test_transform_fx.py (14-59)`; `tests/test_report.py:10-24`; and row 3's `NONE`). But since the ingest boundary required by S1 is never listed as a row, it never receives a control designation or an explicit NONE anywhere in the answer — there is no text of the form "ingest: NONE" or "ingest: <control>". A boundary that isn't enumerated cannot satisfy "carries a named control or NONE."

**S3 — NOT MET**

Same gap as S2: the three enumerated rows are each marked `SILENT` (e.g. row 1: *"fault mode ... SILENT (wrong-scale, plausible-looking float...)"*), satisfying the letter of S3 for those three. But the ingest boundary has no row and therefore no fault-mode marking at all — it is not marked "complete silently" or "raise" anywhere in the text.

**C1 — MET**

Row 1: *"never routes a real `extract._to_minor_units` output through `to_usd`, so the /100 mismatch is untestable by construction."* Row 2: *"no test ever calls `report.rank(transform.aggregate(...))` with transform's real field name."* Both explicitly state that no test chains one stage's real output into the next stage's input.

**C2 — MET**

Row 2: *"`row()` helper (`test_report.py:6-7`) builds rows with key `\"total\"`, matching `rank`'s buggy key by construction."* This directly identifies that the report test's own fixtures use the same (wrong) key `"total"` that `rank` erroneously reads, rather than the real `total_usd` key transform produces.

**C3 — MET**

Row 1: *"both files' `rec()` helper (`test_transform.py:6-8`, `test_transform_fx.py:9-11`) builds `amount` as an already-decimal float (`100.0`, `1000.0`)"* — contrasted against the producer contract *"`{region_code, currency, amount:int MINOR UNITS(cents), order_id}`"*. This identifies the transform fixtures as decimal/dollar-scaled floats rather than the integer minor units extract actually emits.

## anything else

- **Boundary-count contradiction**: The title claims *"4 boundaries incl. ingest and egress"* but Table 1 has exactly 3 rows, and every downstream artifact (Table 2's "seams left unwatched" column, "The list" section) is computed against a 3-seam model. The claimed count and the delivered enumeration don't match.
- **Phantom "seam 0"**: The golden/snapshot row in Table 2 lists "seams left unwatched" as *"0-3, all of them"* — but Table 1 only ever defines seams numbered 1, 2, 3. Seam "0" is never introduced, defined, given a producer/consumer/control, or assigned a fault mode anywhere in the answer. This looks like an unacknowledged nod to the missing ingest boundary from S1, but it's never formalized as a row, so it just reads as a number that doesn't add up against the rest of the document.
- **Unsupported statistic**: Table 2's first row cites *"status quo (current 34 tests)"*. No other part of the answer derives, counts, or references "34" anywhere (no test-count arithmetic, no file-by-file tally). It's asserted with no supporting evidence in the answer's own content.
- **Unexplained module-name switch**: "The list" section states *"not even a smoke test runs `revenue.run` and checks its stdout"* — but everywhere else in the answer (Table 1 row 3, footnotes) the same module is called `run.py` (e.g. *"`run.py:9` (`sys.stdout.write`)"*), with no prior mention of a `revenue` package/prefix. This is an inconsistent identifier for what appears to be the same file, introduced without explanation.
- **Conflated cell in Table 1, row 1**: The "consumer assumes" column bundles two distinct faults (the missing `/100` scale conversion and the missing `GBP` rate) into a single cell, even though Table 2 correctly treats them as separate faults F1/F2. Not fatal since Table 2 disambiguates them, but the seam table itself doesn't cleanly separate the two claims where they're first introduced.