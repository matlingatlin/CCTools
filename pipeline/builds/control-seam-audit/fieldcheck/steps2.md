VERDICT: RED

**1. Traceability — each step/Important section**

- **Important 1** ("a control proves the thing it watches, and nothing else") → **C1**. Near-verbatim paraphrase: "a control written specifically to prevent a known failure mode... passed throughout a run that produced exactly that failure - because the fault had moved one stage upstream of what it watched" mirrors C1 exactly, including the "one incident" scope, which the text correctly caveats ("one incident, one pipeline, no base rate"). Well-grounded.

- **Important 2** ("rank the seams by what a fault there does, not by what it touches") → traces loosely to **C2** ("the numbers still look plausible... Nothing downstream can detect it" ≈ "A fault that completes and prints a plausible value is found by whoever notices the value is wrong, which may be nobody"), reinforced by the shared silent-hiding trait of P1/P2/P3. But the sentence "`references/why-controls-miss-seams.md` carries the evidence for both of these Important sections and states its limits: one incident, one pipeline, no base rate" misapplies C1's "one incident" limit to a section actually resting on C2, which is annotated **REPEATED**, not "one incident." That's a provenance error, not just a stretch.

- **Important 3** ("this applies for the rest of the task, not once") → **NONE**. It's a structural rule about how guidance persists across turns, not a claim needing an observed row — not itself a finding.

- **Step 1** ("Enumerate the seams...") → **F1**. Directly answers "no boundary was enumerated... the ingest boundary... was examined by neither run" via "Include the ingest boundary... N units give N+1 boundaries."

- **Step 2** ("quote both sides of every seam") → **F2** / **P1** / **P3**. Matches "both runs DID do... find P1 and P3 by placing two lines of code side by side and reading them."

- **Step 3** ("mark each seam SILENT or LOUD") → weak, effectively **NONE**. No observation instructs classifying seams this way or mutating a scratch copy; the only support is an inference from P1/P2/P3 all being silent, which is a synthesis, not a named observed row.

- **Step 4** ("name the control watching each seam... REAL/OWN") → **F2**. Matches "every one of them exercises a stage in isolation with hand-built fixtures" and "the test's fixture and the buggy code agree with each other, not with reality."

- **Step 5** ("answer any coverage claim from the table") → **C1** / Important 1.

- **Step 6** ("score every proposed remedy against every fault") → **F3**. Matches "the remedy offered was one generic end-to-end/integration test, and neither run checked that remedy against the faults it had just found... because P3 is masked by the current data ordering."

- **Step 7** ("report the table first, the narrative second") → **NONE**. Nothing in F1–F3/C1–C2/P1–P3 concerns report ordering. This is an opinion by the contract's own test.

**2. Checkable endings**

All seven steps end in a named artifact: (1) numbered list, stated length; (2) file:line quotes + YES/NO/UNKNOWN; (3) SILENT/LOUD + command run; (4) REAL/OWN/NONE filled on every row; (5) seam numbers, or the explicit "protects none of them" sentence; (6) table 2 + a reason beside every MISSES; (7) two tables + fault list, with the empty-list-vs-skipped-audit distinction stated. No step fails the checkability test.

**3. One-time vs. standing**

Handled correctly. Important 3 explicitly promotes Steps 5/6 to standing: "Every time someone calls a control coverage, or proposes a remedy - at any point, including long after the table is filled and the checklist is done - it goes through the table before it is agreed." That satisfies the reviewer's concern about non-standing guidance.

**4. Rule the observation set supports that the text does not carry**

P2's specific mechanism — "a unit test asserts the per-record function returns None for an unpriceable currency - the drop is tested and approved - and nothing asserts the aggregate conserves rows" — supports a distinct checkable rule: **verify row/record-count conservation across each seam** (count in vs. count out, with any intentional filter explicitly asserted). Step 2 only compares "field names, types and units" (catches P1, P3) and Step 3 only tests value mutation in a scratch copy, not row disappearance. No step asks whether the count of things crossing a seam matches and whether any drop is asserted — exactly the gap that let P2 hide behind an approved per-record test. This rule is absent from all 7 steps.