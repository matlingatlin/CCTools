VERDICT: RED

## 1. Traceability — step / Important section → observation

- **Important — "a control proves the thing it watches, and nothing else"** → **C1**. Its scenario ("a control written specifically to prevent a known failure mode... passed throughout a run that produced exactly that failure... because the fault had moved one stage upstream of what it watched") restates C1 almost verbatim, including the "one incident" caveat carried into the pointer to `references/why-controls-miss-seams.md`.
- **Important — "rank the seams by what a fault there does, not by what it touches"** → **C2**. "A fault that completes and prints a plausible value is found by whoever notices the value is wrong, which may be nobody" restates C2's "the losing arm is reported as the winner. Nothing downstream can detect it."
- **Step 1 ("Enumerate the seams...")** → **F1**. Both the requirement to include "the ingest boundary" and the line "Do not start from the symptom. Working outward from a wrong number reaches the boundaries that already hurt and stops there" map directly onto F1's finding that both baseline runs worked outward from the symptom and missed the ingest boundary.
- **Step 2 ("Quote both sides of every seam...")** → **NONE**. No F/C observation describes a "quote both sides with file:line" technique, and the sentence "Compare field names, types and units - units, not only types, because cents and dollars are both numbers" is a fabricated example with no observed row behind it. This is a rule with no observed row — an opinion.
- **Step 3 ("Mark each seam SILENT or LOUD...")** → **C2**. Both the label scheme and the fallback instruction "change the value at that boundary in a scratch copy and see whether anything objects" operationalize C2's already-demonstrated fault-injection scenario ("If A and B are mapped back the wrong way the run still completes...").
- **Step 4 ("Name the control watching each seam...")** → split. "Name a test, assertion, schema check or monitor that would fail if a fault were introduced there... or write NONE" → **F2** ("neither said, per boundary, which existing control would catch a fault introduced there"). But the second half — "mark where that control's input comes from: REAL... OWN... The OWN case is the one that fools people" — → **NONE**. C1 is about a control watching the wrong *location* (one stage upstream), not about REAL-vs-OWN fixture data; that distinction is invented, not observed.
- **Step 5 ("Delete-test every control someone is calling coverage")** → **NONE**. No F/C observation describes deletion-testing as a technique; this is asserted methodology, not derived from an observed failure.
- **Step 6 ("Score every proposed remedy against every fault found")** → **F3**, cleanly. "A golden or snapshot control recorded from today's data records whatever today's data currently masks as correct, so it misses precisely the faults that are latent" is essentially a restatement of F3's finding about the pipeline's masked ranking fault.
- **Step 7 ("Report the table first...")** → **F2**. Directly answers F2's finding that both runs produced FAULT-keyed prose instead of boundary-keyed tables.

## 2. Checkable ending per step

All seven steps do end in a checkable artifact via their "Produces:" line:
1. "a numbered list whose length you state..." — checkable (stated count).
2. "two quotes per seam and YES / NO / UNKNOWN in the agree column" — checkable.
3. "SILENT or LOUD on every row, and for any row you tested, the command you ran" — checkable.
4. "both columns filled on every row, NONE written out rather than left blank" — checkable.
5. "the row numbers it protects - or the sentence saying it protects none of them" — checkable.
6. "table 2 of the asset, filled, with a reason written beside every MISSES" — checkable.
7. "two tables and that list" — checkable.

No step fails this check on its face — the defect is upstream, in what several steps are checkable *for* (see §1: Steps 2, 4's OWN/REAL clause, and 5 are checkable procedures grounded in nothing observed).

## 3. One-time steps that should be standing

Yes. Two steps encode conditions that recur across the life of a task, not just at initial-audit time, but are written as single checklist items that get checked off once:
- **Step 5**: "Delete-test every control **someone is calling** coverage" — "someone" claiming coverage can happen at any later turn (a teammate, a later message), not only during the initial pass. Once checked off, nothing in the file re-triggers this on a later claim.
- **Step 6**: "Score **every proposed remedy** against every fault found" — new remedies can be proposed after the checklist is already complete. As written this is a one-shot gate, not standing guidance that reasserts itself whenever a new remedy shows up.

Both should be pulled out as standing rules (like the two Important sections already are) rather than left as `- [ ]` checklist items, per the reviewer check's explicit instruction that "Claude Code does not re-read the file on later turns, so standing guidance must be written as standing."

## Other findings

- Step 2's file:line-quote-and-compare methodology, and specifically the "cents and dollars" unit-mismatch example, has no observed row behind it (F1's actual observed defect was a region-name spelling collision, not a unit/type mismatch) — this is an opinion dressed as a rule.
- Step 4's REAL/OWN fixture-provenance column is a plausible-sounding but unobserved refinement; C1's incident was about seam *location*, not fixture *provenance*. As written it borrows C1's authority for a claim C1 doesn't support.
- Step 5's delete-test procedure is asserted with no observed incident showing a control that passed a delete-test check yet still failed to catch a fault (or vice versa) — it's methodology by assertion.