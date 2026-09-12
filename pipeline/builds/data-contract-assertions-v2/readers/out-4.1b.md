VERDICT: RED

FINDINGS:

1. Unswept overclaim, same class, relocated to SKILL.md — quote: SKILL.md:132, "A large minority of anomalies that fire at the boundary are never resolved, so an unamended widen row silently becomes a permanently red check that people learn to ignore. (C1, C2, C10)." This is the identical defect class round 1 flagged in C2's claim sentence ("and a large minority are never fixed") — a permanence claim ("never resolved") that no cited claim's quote or effect size supports. C2's own Limits paragraph in references/threshold-evidence.md warns against exactly this: "'not fixed' is not 'false alarm' — the paper's own explanations are a batch sliding out of the rolling window, and an on-call missing the alert; the fixed measurement is heuristic and the paper says it 'can miss some fixes'" — a one-month non-fix rate (28–100% fixed, by category), not "never." C1 and C10 supply no fix-rate data at all, so citing them alongside C2 spreads the same unsupported inference rather than backing it. The sweep the author ran covered only the 13 claim sentences inside references/threshold-evidence.md; this instance sits in SKILL.md's Step 4 and was not touched. I counted exactly 1 instance of this class outside the swept file — within the 13 reference claim sentences themselves I found none remaining (see per-claim check below). This fails the bundle.references agent_check ("Is every claim traceable to a source WITH A QUOTE?") for this claim as it now stands.

Per-claim check, C1–C13 (claim sentence vs. its verbatim quote, references/threshold-evidence.md):
- C1: carries — "schema evolves in most... pipelines," "hypothesis of data-schema co-evolution" support "normal state... not an incident."
- C2: carries (round-1 phrase gone from this file) — "most common anomalies are [three categories]" supports "dominated by structural surprises."
- C3: carries (reworded) — "needlessly fire an alert 7 out of 10 times... flaky" supports "false-alarmed... small perturbation"; "production volume" matches the n=100M sample given beside the quote.
- C4: carries, with a separate accuracy note — the quote measures "diagnose and fix," but the sentence and its own Limits line narrow this to "diagnosis" alone. Not an overclaim (says less than the quote, not more), so it's outside this round's target class, but it's an internal quote/Limits mismatch worth a look.
- C5: carries.
- C6: carries (changed).
- C7: carries — near-verbatim ("deliberately over-fitted").
- C8: carries — near-verbatim ("high precision but low recall").
- C9: carries (round-1 phrase gone) — "near-ceiling ROC AUC" matches the quote's 100%/92% figures.
- C10: carries.
- C11: carries.
- C12: carries — "did not move" is the underlying measurement the quote's conclusion ("not a reliable indicator") rests on, stated in the Effect size line right beside the quote.
- C13: carries — "tracks sample size more than severity" is the comparison the stated sweep (Sample: sizes 1,000–1,000,000, 100 reps) beside the quote establishes, not an added fact.

Standing questions:
- References vs. SKILL.md content: no passage is duplicated verbatim in both files (checked structural surprises / over-fitted / silenced-and-abandoned / ROC-AUC phrasing — all are short paraphrase citations in SKILL.md, the intended pattern). The one cross-file problem is Finding 1: content that reads as if it migrated from C2's claim sentence into SKILL.md picked up two extra citations (C1, C10) it isn't backed by.
- Values that move on their own: none found unflagged. The candidates that could drift — TFDV's default JS-Divergence/L-infinity (S2), the KS-test sample-size cutoff (S8), Great Expectations' Profiler defaults (S9) — each already carries its own expiry condition in the Sources section, which is the mechanism this contract calls for.
- assets/ NOT-NEEDED classification: this is a reason, not just reason-shaped, on what's visible in this bundle. Step 6 (provenance line: statistic, column/segment, row counts on each side, comparison window, kind, observed figures, owner, NOT DERIVED) and Step 9 (assertion row: name, observed value, expected bound, kind, side, row count, batch id) already name the full field list, in order, in the body. A template built to the contract's own definition of bundle.assets ("field names, order, what belongs in each. Nothing filled in.") would contain nothing beyond what Steps 6 and 9 already state in prose, so the stated reasoning is verifiably grounded rather than asserted.

WHAT YOU DID NOT CHECK:
- The actual recorded classification sentence for assets/ NOT-NEEDED: not present in this reader's bundle (no assets/ directory, no such text in SKILL.md or references/). My ruling above is reasoned from Steps 6/9's field lists, not from seeing the classification's own wording.
- whole.bom (needs the build's bill of materials — not supplied to this reader) and byte-match/fetch-date verification of the 13 quotes (per the note, already checked by script; not re-verified by eye).
- purpose.present / when.present agent checks — routed to a different field than mine.
- evals/evals.json content — withheld from this reader by design; the preflight already waives body.files-exist and ptr.resolves for it.
