VERDICT: RED

F1. Cell: assets/seam-control-table.md, Table 2 instructions — "Columns are the faults from Table 1 whose `agree` is NO or UNKNOWN, plus any fault the incident raised."
Why wrong: "the incident" has no antecedent inside this file and is only meaningful if the audit happens to be triggered by a known prior incident. The skill's own "When to use this" list includes proactive triggers with no incident at all ("its first unattended run," "a handover to people who did not build it"), so this instruction is undefined/inapplicable in those cases — a domain-specific residue leaking into what is billed as the generic output-format template.
Severe: severe (breaks the output-format asset in a stated in-scope use case).

F2. Sentence: SKILL.md, "Important" sections ("a control proves the thing it watches, and nothing else" / "rank the seams by what a fault there does") plus their sourcing note — "`references/why-controls-miss-seams.md` carries the evidence for both Important sections above."
Why wrong: these two rules are declared binding "for the rest of the task" on every invocation of a supposedly general, domain-agnostic method, yet their entire evidentiary basis is one incident from one specific grading-harness repo (blind.py/score.py/selftest_score.py) — the same repo used as the "In this repo (one instance)" example. That makes project-specific material a load-bearing requirement rather than an illustrative example confined to the closing section, contradicting the stated library rule.
Severe: severe.

F3. File: evals/evals.json, the 7 evals as a set.
Why wrong: the eval contract requires "at least one case where the right outcome is NO finding." None of the 7 cases is a correctly-executed audit that lands on an adequately-covered pipeline (full table, empty fault list). Eval 7 tests scope refusal (wrong tool for a reproducing bug), not a legitimate empty-result run of the method itself — so the "empty list under a filled table is a result" case that SKILL.md itself describes as valid is never exercised.
Severe: severe (leaves a stated contract requirement unmet).

F4. Sentence: evals/evals.json, eval 3 expected_output — "the suite is delete-tested against the table, and the rows it protects are named."
Why wrong: "delete-tested" is not defined or used anywhere else in SKILL.md, the reference file, or the asset file. A grader has no way to verify this expectation against the method as written, since the method never produces or names a "delete-tested" artifact.
Severe: cosmetic/moderate (unverifiable eval wording, but doesn't break the method itself).

F5. Sentence: SKILL.md Step 2 — "Units, not only types, because cents and dollars are both numbers" — duplicated verbatim in assets/seam-control-table.md's "what crosses" column definition — "Units, not just types: cents and dollars are both numbers."
Why wrong: same claim stated in two places nearly word-for-word, one of the exact failure modes the review rule calls out.
Severe: cosmetic.

F6. Sentence: SKILL.md "Bundled files" — "READ it when someone argues an existing control already covers a boundary, or that a fault there would have surfaced by now" (describing references/why-controls-miss-seams.md).
Why wrong: this narrows the file's trigger to a rebuttal scenario, but the "Important" sections earlier in the same document say this file "carries the evidence for both Important sections above" — rules that apply to the whole task, not just to rebutting a coverage claim. The stated read-trigger and the file's actual justificatory role disagree.
Severe: cosmetic.

F7. Sentence: evals/evals.json, "_note" — "the expectations array is filled once the first paired outputs exist."
Why wrong: no eval object in the file contains an "expectations" field at all (only "expected_output" strings), so the artifact as delivered cannot yet be used for automated grading described by its own note — a declared but unfilled structural piece shipped as if the file were complete.
Severe: cosmetic (self-acknowledged, but leaves the deliverable partially unusable as-is).