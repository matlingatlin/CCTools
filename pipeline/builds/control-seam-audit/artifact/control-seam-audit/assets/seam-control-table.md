# Seam control table - the shape

Two tables. Copy the headers, keep the column order, fill every cell. A blank cell is a
finding, not a formatting problem: it means the audit did not reach that seam.

## Table 1 - one row per seam

| # | seam | what crosses | producer says | consumer assumes | agree | fault mode | control watching this seam | that control's input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {n} | {producer unit} -> {consumer unit} | {the object, its field names and its units} | {file:line of the line that builds it} | {file:line of the line that reads it} | {YES / NO / UNKNOWN} | {SILENT / LOUD} | {file:line of a test, or NONE} | {REAL - produced by the producer / OWN - the control builds its own / n/a} |

Column definitions, in order:

- **seam** - every boundary where a value leaves one unit and enters another. Include
  the ingest boundary (what enters the first unit, and from whom) and the egress
  boundary (what leaves the last unit, and who reads it). N units have N+1 boundaries.
- **what crosses** - the object's field names, types and units. Units, not just types:
  cents and dollars are both numbers.
- **producer says / consumer assumes** - a file:line on each side. Two quotes, not one
  description.
- **agree** - YES means the two quoted lines name the same field, the same type and the
  same unit. NO means the defect is already found and needs no run to confirm. UNKNOWN
  means one of the two sides could not be located, which is itself the finding.
- **fault mode** - SILENT if a wrong value here still completes the run and prints a
  plausible number; LOUD if it raises, crashes or fails a type check.
- **control watching this seam** - a named test, assertion, schema check or monitor.
  NONE is the expected answer for most rows and must be written, not left blank.
- **that control's input** - REAL only when the control's input is produced by the
  producing side in the same run. A control fed a fixture the test file builds itself
  proves the consumer against a contract nobody produces, and belongs in the OWN
  column even when its name says integration. Write n/a here, and only here, when the
  previous column says NONE.

## Table 2 - one row per proposed control, one column per fault

Fill this before proposing anything. Columns are the faults from Table 1 whose `agree`
is NO or UNKNOWN, plus any fault reported from outside the code - a complaint about an
output, a discrepancy someone noticed, a past incident. When the audit is proactive and
nothing has been reported, the outside column set is empty and Table 1's rows are the
whole of it.

| proposed control | {fault 1 id} | {fault 2 id} | {fault n id} | seams left unwatched |
| --- | --- | --- | --- | --- |
| {what you are proposing to add} | {CATCHES / MISSES} | {CATCHES / MISSES} | {CATCHES / MISSES} | {seam numbers from Table 1 with no control after this is added} |

A MISSES cell is the useful one. Write the reason beside it in a footnote: a control
recorded from data that currently masks a fault records the fault as correct.
