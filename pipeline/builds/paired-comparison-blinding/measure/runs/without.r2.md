## Q1

Setup I'd actually run over the 12 tickets (pairwise, blinded, order-counterbalanced):

1. Build the comparison file. For each ticket i, load `old[i]` and `new[i]`. Draw a coin per ticket: if heads, slot_A = old, slot_B = new; else slot_A = new, slot_B = old. Write a key file `key.csv` with `ticket_id,slot_A_version,slot_B_version` and keep it OUT of the judging directory. The judge sees only ticket text + Answer A + Answer B, never version names, filenames, or ordering hints. Strip anything version-identifying from the outputs themselves (prompt-version headers, model names, trailing formatting tells).
2. Run each ticket TWICE with the slots swapped (both orders), so position bias cancels within-ticket rather than only across the set. That's 24 judgements over 12 tickets. A ticket where the judge picks slot A both times is a position-flip and counts as a tie, not a win.
3. Judge prompt (use as-is):

```
You are comparing two candidate summaries of the same customer support ticket.

TICKET
{{ticket_text}}

ANSWER A
{{answer_a}}

ANSWER B
{{answer_b}}

Judge on these criteria, in this order of importance:
1. Factual faithfulness to the ticket — no invented details, no dropped commitments, dates, order numbers or amounts.
2. Coverage of the customer's actual ask and the current state of the issue.
3. Actionability for the next agent — what has been done, what is outstanding.
4. Brevity and clarity. Length is not a merit in itself.

Do not consider which answer appears first, which is longer, or which sounds
more confident, except where those bear on the criteria above.

Output JSON only:
{"reasoning": "<=80 words citing concrete differences",
 "verdict": "A" | "B" | "tie",
 "margin": "clear" | "slight"}
```

4. Tally by joining verdicts to `key.csv` — the join is the only place slot letters become version names. Report: wins for old, wins for new, ties, position-flip count, and how many wins were "clear". With n=12 a 7-5 split is noise; I'd treat anything under roughly 9-3 (with consistent order-swapped agreement) as "no detectable difference" rather than a win.
5. Before trusting the judge, spot-check it: label 3-4 tickets yourself and check the judge agrees. If it doesn't, fix the rubric before running the other 12.

Two things I need from you: the tickets themselves (the judge must see the source, not just the two summaries), and whether "better" means faithfulness-first as above or something else (e.g. shortest acceptable summary).

## Q2

This script is the one place where the blind is broken, so its tests are load-bearing — a silent inversion here flips the headline of the whole study and nothing downstream will notice.

Normal cases:
1. Straight round-trip: label a known set, unmap it, assert every item recovers its original version.
2. Both assignment orders present in the input (some tickets A=old, some A=new) — assert per-ticket mapping, not a single global rule.
3. Ties / no-verdict rows pass through as ties and are not silently assigned to a version.
4. Tally arithmetic: wins + losses + ties == number of judgements; counts match a hand-computed fixture.

Adversarial / edge cases:
5. **Inversion detection.** Feed a key deliberately swapped for one ticket and assert the output differs — i.e. write at least one test that FAILS if the mapping is reversed. A symmetric fixture (6 old-first, 6 new-first, balanced verdicts) will pass under an inverted map; make sure your fixtures are asymmetric enough to catch it.
6. Unknown or unexpected label ('C', 'a' lowercase, 'Answer A', empty, null) → raises, never defaults to a version.
7. Ticket id in verdicts but missing from the key, and vice versa → raises; no silent drop. Assert the count of joined rows equals expected.
8. Duplicate ticket ids in the key (e.g. both order-swapped runs) → handled explicitly, either keyed by run id or rejected. This is the likeliest real bug once you counterbalance.
9. Type/whitespace robustness: ids as `"7"` vs `7`, trailing whitespace, BOM in the CSV.
10. The key file is never written by the same process that produced the anonymised outputs in the same pass without a checksum — test that a mismatched key (wrong run, stale file) is detected, e.g. by comparing a run id or hash stored in both files.

Negative: it should not "correct" or reinterpret verdicts, only map them. A test that the function is a pure relabelling — same multiset of verdict strengths in and out.

## Q3

No. "Answer A" is a slot label, not a version — it means nothing until it's joined to the key, and with counterbalanced order there is no single "A" across the set. Using it as a headline is exactly the error the anonymisation exists to prevent, and it's a coin-flip whether it names the right version.

Also: the judge's own closing sentence is a summary of its per-item verdicts, not an independent result. The headline should come from the tally: e.g. "New prompt won 8 of 12, old won 2, 2 ties; margin clear on 5." If the judge's global remark disagrees with the tally, the tally wins and the disagreement is worth reporting.

Additionally, in a two-order run "A was stronger" across the set is a symptom to check, not a finding — it's the signature of position bias.

## Q4

No — that doesn't work and it costs you the only real defence.

An instruction to ignore position is a statement about the judge's intent; position bias is a property of how the model actually attends to the sequence, and it survives being told not to. Empirically judges asked to ignore order still show first- or last-position preference, and now you have no way to measure it, because with a fixed order the bias is perfectly confounded with the result.

Randomising (better: running both orders per item) is cheap — it's a coin flip in the harness — and it turns position bias from an invisible confound into a number you can report: how often the judge picked the same slot regardless of content. Keep the instruction if you like, it's harmless, but it is not a substitute. If you want evidence for your own setup, run the 12 tickets with A and B swapped and count the flips; if it's near zero you've proven the point, and if it isn't you've just saved the study.

## Q5

No — that's backwards. Blinding matters most precisely when the candidates are close.

When one version is obviously better, the effect is large enough to survive a biased procedure. When they're near-identical, the true difference is smaller than the bias, so whatever tilt exists — position, verbosity, the judge or the human knowing which is "the new one" — becomes the deciding vote. An unblinded close comparison doesn't produce a weak result; it produces a confident result that measures your expectations.

"Low-risk" is also doing some work here. The risk isn't in the comparison, it's in what you do next: you'll ship the winner and treat the question as settled. A wrong close call is more durable than a wrong obvious one, because nobody re-runs it.

Blinding costs a shuffle and a join. Keep it. If anything, for close candidates add the order swap and more items, since n=12 with a small effect can't distinguish the two anyway — the honest outcome may well be "no detectable difference, pick on cost/latency".

## consulted

none — answered from my own judgement. Files touched: read `pipeline/builds/paired-comparison-blinding/measure/prompts/without.txt` (the prompt itself), wrote this file.
