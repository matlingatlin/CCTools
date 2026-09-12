# Why a green suite and a wrong answer coexist

Two claims, both from one engineering incident, both quoted verbatim from the file named
in the row. Verification is stated PER CLAIM rather than once for the set, because a
single line pasted under every row reads as a per-claim guarantee it does not make.

## Claim 1 - a control proves the thing it watches and nothing else

**MEASURED** · local incident record, fetched 2026-08-30 · closing paragraph of the
grading write-up

> The controls that existed did not catch it: `selftest_score.py` guards the
> *un-blinding* against exactly this failure mode, and it passed throughout, because
> the inversion happened one stage upstream of what it watches.

*What was measured:* whether an existing control detected a defect in an adjacent stage.

*Effect:* 1 of 1 controls passed while the pipeline produced an inverted result.

*Sample:* one harness, one run. The same write-up gives the count in its own words, two
paragraphs above the quote:

> Three bugs, all in the same question, all in code I wrote in this session.

*The source's own limits:* a single incident in one pipeline. It establishes that the
gap can occur, not how often. Nothing here supports a base rate.

*What would make this row untrue:* nothing - it is a record of one event. What it does
NOT license is any claim about frequency.

The control in that incident was written specifically to prevent an inverted
conclusion, by someone who had the failure mode in mind, before the harness was used on
real data. It still missed, because it was pointed at a stage rather than at a boundary.
That is why the audit is keyed on boundaries: the care taken over a control does not
widen the thing it watches.

## Claim 2 - the dangerous fault completes, it does not error

**REPEATED** · module docstring of the control written in that same incident, fetched
2026-08-30

> If A and B are mapped back the wrong way the run still completes, the numbers still
> look plausible, and the losing arm is reported as the winner. Nothing downstream can
> detect it.

*What was measured:* nothing. This is the design rationale an engineer wrote into a
control, not an independent measurement, and it is recorded here as REPEATED for that
reason.

*The source's own limits:* it is one author's stated reasoning about one boundary. It
argues that silent inversion is the class worth defending against; it does not measure
how often that class occurs relative to loud failures.

*What would make this row untrue:* a downstream check that does detect the inversion -
which is exactly what the audit is looking for, per seam.

Neither claim supports the stronger statement that silent faults are more common than
loud ones. What the docstring records is one engineer's reason for defending one
boundary; the ranking it justifies is a ranking, not a frequency.

## What neither claim establishes

Neither claim says how often seam faults occur, what share of defects live at
boundaries, or that any particular remedy works. Both come from one incident in one
pipeline, and both were written by people involved in it. Anyone who wants a rate has
to measure their own.
