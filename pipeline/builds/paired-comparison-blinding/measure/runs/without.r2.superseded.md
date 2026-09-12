## Q1

Set it up as a blinded, randomised pairwise comparison, not a "score set A, score set B" pass.

Procedure I'd run:

1. **Build the pairing.** One row per ticket = (ticket_id, output_old, output_new). 12 rows.
2. **Randomise position per ticket.** For each ticket independently, flip a seeded coin to decide whether old or new is presented first. Do NOT use one fixed order for the whole set.
3. **Strip identifiers.** Remove anything that leaks provenance: filenames, version tags, model names, prompt-version strings, trailing whitespace/formatting tells, ordering of fields, differing markdown conventions. If the new prompt makes outputs systematically longer or bulleted and the old ones plain, note that — it is a visible tell and it will bias the judge; record it rather than pretending it is hidden.
4. **Write the key to a separate file** (`key.csv`: ticket_id, position_1_version, position_2_version, seed) and do not open it until all scores are in.
5. **Score each ticket** with the judge prompt below. Judge sees only ticket + Answer 1 + Answer 2.
6. **Counterbalance check.** Re-run each ticket with the two positions swapped (24 judgements total; it is 12 tickets, this is cheap). Any ticket where the winner follows the position rather than the content is a position-bias flip — count them and report the flip rate.
7. **Unblind and tally** with the key: wins for old, wins for new, ties, plus flips.

Judge prompt (use verbatim):

> You are comparing two candidate summaries of the same customer support ticket. You do not know how either was produced; do not speculate about it.
>
> TICKET:
> {{ticket_text}}
>
> ANSWER 1:
> {{answer_1}}
>
> ANSWER 2:
> {{answer_2}}
>
> Judge against these criteria, in this order of importance:
> 1. Factual faithfulness to the ticket — no claim that is not supported by the ticket text.
> 2. Completeness of the decision-relevant facts: the customer's actual problem, what they have already tried, what they are asking for, any deadline/account/order identifiers.
> 3. Actionability for an agent picking this up cold.
> 4. Brevity — shorter is better at equal information. Length is not merit.
>
> Output exactly this JSON and nothing else:
> {"winner": "1" | "2" | "tie", "confidence": "high" | "low", "reason": "<one sentence, citing the specific difference that decided it>", "faithfulness_errors_1": <int>, "faithfulness_errors_2": <int>}
>
> Choose "tie" if the difference is not one a support agent would notice. Do not reward length, formatting, or confident tone.

Caveat to state in the write-up up front: **n=12.** Twelve tickets can show a direction, not a reliable margin. 8–4 is not significance; report it as counts plus the judge's stated reasons, and treat anything short of ~10–2 with consistent reasons as "no clear difference, need more tickets." If you can, also have a human score 3–4 tickets blind and check they agree with the judge before you trust the judge's other 8.

## Q2

The script is the single point where the blind can silently break, so its tests matter more than its size.

Cover:

**Correctness of the mapping**
- Round-trip: for a known assignment, label → version → matches the assignment log exactly, for every row.
- Per-ticket independence: a fixture where ticket 1 has old-first and ticket 2 has new-first is mapped correctly for both. This is the test that catches the "A always means old" assumption.
- Every label in the results file resolves to exactly one version.
- Every ticket in the key appears in the results, and vice versa — no silent inner-join dropping rows.

**Failure loudly, not quietly**
- Unknown label (a "C", a typo, an empty cell) → raises, does not default to a version and does not skip the row.
- Duplicate ticket_id in the key, or in the results → raises.
- Missing key file / missing results file → raises with the path.
- Key and results disagree on the ticket set → raises and names the differing ids.
- Results file has a row count ≠ key row count → raises.
- Partial failure does not emit a tally: assert that on any error nothing is written to the output file.

**Normalisation**
- Case and surrounding whitespace on labels (`" a "`, `"A"`, `"a"`) map identically — or are rejected consistently. Pick one and test it.
- Ties / abstentions / "no winner" pass through as a distinct category and are not silently counted as a loss for either side.

**Tally arithmetic**
- wins_old + wins_new + ties == number of tickets.
- A hand-computed fixture: 12 rows with a known 7/4/1 outcome produces exactly 7/4/1.
- Swap the key (invert every assignment) and assert the tally inverts exactly — this catches an off-by-one or a reversed lookup that a symmetric fixture would hide.
- All-old-wins and all-new-wins fixtures produce 12/0/0 and 0/12/0.

**Determinism / order independence**
- Shuffling the row order of the results file does not change the tally.
- Same inputs → byte-identical output, run twice.
- Property test: generate a random assignment and random winners, apply the script, and assert the recovered per-version win counts equal the ones you generated.

**Process guard (worth an assertion even though it feels procedural)**
- If the script is also the thing that generated the key, assert it refuses to run unblinding while any result row is still missing a verdict — so nobody unblinds half a set, sees the direction, and then scores the rest.

## Q3

No — don't use it, and don't paraphrase it either. Send it back.

"Answer A" is a **position label, not a version.** If positions were randomised per ticket (they should have been), then "A" is the old prompt on some tickets and the new prompt on others, so "answer A was stronger across the set" is not a statement about either version — it is closer to a statement that the judge preferred whatever it read first, which is the position bias we blind against, not a result.

What to do instead:
- Take the judge's **per-ticket** verdicts, map each through the key, and compute the headline from the tally.
- If the judge only produced this aggregate sentence and no per-ticket verdicts, the run has no usable result — rescore with a per-item output format (the JSON in Q1).
- If, on inspection, positions were *not* randomised and A was always the old version, then the sentence is about the old version — but in that case the result is confounded by position and should be re-run, not headlined.

The write-up headline should name versions, not letters: e.g. "Old prompt preferred on 7 of 12 tickets, new on 4, 1 tie (n=12, blinded, 2 position flips)."

## Q4

No. That instruction does not work and, worse, it makes the bias unmeasurable.

- Position/primacy bias in LLM judges is a property of how the model attends to the inputs, not a stated preference it can switch off on request. Asking it to ignore position gets you compliance in the text, not in the scores.
- Even if it partly worked, you have no way to check. Randomisation gives you a check for free: swap the order and see whether the verdict follows the content or the slot.
- It also does nothing about the other leak — provenance tells in the text itself (length, formatting, model-specific phrasing). Randomising positions plus stripping identifiers addresses both; a prompt line addresses neither.

Randomising is one line of code and a key file. Keep the instruction if you like — it costs nothing — but keep it *in addition to* randomisation, never instead of it. And run the swapped duplicate on all 12; the flip rate is your evidence that the blinding did something.

## Q5

No. Close candidates are the case where blinding matters **most**, not least.

Bias is roughly a fixed-size thumb on the scale. When the true quality gap is large, that thumb doesn't change the winner. When the two candidates are near-identical, the thumb *is* the result — you will get a clean-looking verdict that is measuring presentation order rather than quality, and it will be indistinguishable from a real finding.

Also, "we already know they're close" is itself a prior you'd be feeding into an unblinded comparison — exactly the thing blinding exists to keep out.

And the risk framing is backwards: low-stakes means a wrong answer is cheap, not that a wrong answer is unlikely. Blinding here costs a shuffle, a key file, and a few minutes. Keep it. If the budget is genuinely the issue, cut the counterbalanced second pass before you cut the blinding — and if the two really are that close, the honest outcome is likely "no measurable difference," which is a useful result you can only report if the comparison was clean.

## consulted

- /home/user/skills-repo/pipeline/builds/paired-comparison-blinding/measure/prompts/without.txt (the task prompt itself)
- No skills, tools, or other repo files consulted. Answers are from my own judgement.
