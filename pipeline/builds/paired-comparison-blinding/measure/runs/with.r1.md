## Q1

Twelve tickets, two arms, both output sets saved. I will not paste them into a judge as "old" and "new" — the judge would be scoring the labels. Here is the blinded setup, ready to run.

**Design**

- Per item (ticket), a seeded coin flip decides which arm is printed first and which letter it gets. Order and label are randomised together.
- Seed: `sha256(run_id + ticket_id)`, first byte even = old-first, odd = new-first. Reproducible, not guessable from the ticket content.
- The key is written to a separate file that is never in the judge's context.
- n=12 is small. With a coin flip per item, an all-one-way assignment is possible; I balance it (6/6) by sorting items on the hash and assigning the first six one way. Still per item, still seeded, but no degenerate split.

**`blind.py` (the part that matters)**

```python
import hashlib, json, pathlib

RUN_ID = "sum-prompt-2026-08-30"

def h(run_id, item_id):
    return int(hashlib.sha256(f"{run_id}:{item_id}".encode()).hexdigest(), 16)

def build(items, run_id=RUN_ID):
    # items: [{"id":.., "question":.., "old":.., "new":..}]
    ranked = sorted(items, key=lambda it: h(run_id, it["id"]))
    half = len(ranked) // 2
    key, prompts = {}, {}
    for i, it in enumerate(ranked):
        old_first = i < half          # balanced, deterministic in the hash order
        first_arm = "old" if old_first else "new"
        second_arm = "new" if old_first else "old"
        # A is always printed first by the template below; relabelling therefore
        # moves the POSITION too. This is asserted, not assumed:
        assert TEMPLATE.index("### Answer A") < TEMPLATE.index("### Answer B"), \
            "template no longer prints A before B - order is no longer randomised"
        prompts[it["id"]] = TEMPLATE.format(
            question=it["question"], a=it[first_arm], b=it[second_arm])
        key[it["id"]] = {"A": first_arm, "B": second_arm}
    pathlib.Path("key.json").write_text(json.dumps(
        {"run_id": run_id, "input_hash": input_hash(items), "map": key}, indent=2))
    return prompts   # key.json is NOT returned into the grading context
```

**Judge prompt template (`TEMPLATE`)**

```
You are comparing two candidate summaries of the same support ticket.

The labels A and B are re-randomised independently for every item in this set.
A on this item has no relationship to A on any other item. Do not compare across
items and do not describe a pattern across the set.

Ticket:
{question}

### Answer A
{a}

### Answer B
{b}

Score each answer against the rubric below, then give a verdict for THIS item only.

Rubric:
1. Faithful to the ticket - no invented facts, names, dates, order numbers.
2. Covers the customer's actual ask and any blocking detail.
3. Actionable for the next agent - state, what was tried, what is needed.
4. Length appropriate; no padding.

Output exactly:
A_scores: {{faithful:1-5, coverage:1-5, actionable:1-5, concision:1-5}}
B_scores: {{...}}
verdict: A | B | tie
one_line_reason: ...
```

**Scoring**

- Tally only the per-item verdicts, mapped back through `key.json`. Report old-wins / new-wins / ties out of 12, plus per-criterion means.
- If the judge writes any set-level summary, read it only as commentary on the rubric. It cannot carry a result: with per-item relabelling there is no cross-item "A" for it to be about.
- Say in the run record that the key was withheld from the grader.

**Honest caveat to state with the numbers**: 12 items is a direction, not a decision. If it lands near-even, that is "no detected difference", not "the new one is fine". A near-tie is also exactly the regime where order effects are worst, which is why the blinding is in.

## Q2

The blinding is easy and fails visibly. The un-blinding is where a bug **inverts** the result silently: the run completes, twelve rows in, twelve rows out, plausible numbers, wrong winner. Design the tests for that first.

**The inversion control (the one that actually matters)**

1. **Swapped key produces the opposite verdict.** Feed the same judge results through the real key and through a key with A/B flipped on every item; assert the two tallies are mirror images and that they **disagree**. A round-trip test (labels on, labels off, originals back) passes just as happily on an inverted mapping — it is not this test.
2. **The two keys do not agree.** Explicitly assert `tally(key) != tally(swapped_key)`. If they match, the mapping is being ignored somewhere.
3. **Handedness fixture.** One hand-built item where old is unambiguously the winner and the key says old is B; assert the tally credits old. Catches a global off-by-one that both directions of a symmetric test would miss.

**Wrong-key prevention**

4. Key carries `run_id` and an `input_hash`; mapping aborts on mismatch. Test: yesterday's key against today's results raises, does not silently proceed.

**Fail-loud on anything unresolvable — never skip a row**

5. Result with a label not in the key ("C", "Assistant 1", empty) -> raise.
6. Result whose item id has no key entry -> raise.
7. Key entry with no matching result -> raise.
8. Duplicate item id in results or in the key -> raise.
9. **Row-count assertion**: rows in == rows tallied. A silent shrink from 12 to 9 changes the answer and is invisible in the tally. Test that dropping one row fails the run rather than producing a 9-row result.
10. Unparseable or absent `verdict` field -> raise (do not default to tie).

**Ordinary correctness**

11. Ties map to ties, not to a winner.
12. Mixed assignment across items (some A=old, some A=new) tallies correctly — the whole point of per-item keys.
13. Determinism: same run_id + same items produce the same key twice.
14. Balance: for n=12 the assignment is 6/6, and it is not the same 6 for a different run_id.

Test 1 is the one to write first and the one to never delete.

## Q3

No — that sentence cannot be the headline, and it should not appear in the write-up as a result at all.

The labels were re-randomised per item. "A" on ticket 3 and "A" on ticket 9 are different arms. There is no cross-item entity called A for the judge's summary to be about, so the sentence is describing labels, not versions. It can even contradict the judge's own per-item rulings.

The headline comes from the per-item verdicts mapped back through the withheld key: "the new prompt won N of 12, lost M, tied K." I will pull that number. The summary sentence is worth keeping only as commentary on the rubric — file it there, and if the judge produced it despite being told the labels are re-randomised, that is a signal the instruction line needs strengthening.

## Q4

No. That was tested and it did not work.

The de-biasing instruction is not an untried idea — "Large Language Models are not Fair Evaluators" put the line *"ensuring that the order in which the responses were presented does not affect your judgment"* in the template, and measured conflict rates **with that line present**: GPT-4 46.3% and 5.0%, ChatGPT 82.5% and 52.5% on the two pairs. The instruction was in the prompt the whole time.

Two caveats I will state honestly: that is one phrasing in one paper, not proof that no instruction could ever help, and the effect is not purely positional — MT-Bench's rename test moved Claude-v1's consistency from 23.8% to 56.2% just by changing the labels, so part of it rides on the name. But the direction is judge-specific (GPT-4 favours the first slot, ChatGPT the second), so you cannot even correct for it by always putting the new arm in the disfavoured position. You can only randomise.

Randomising costs a coin flip per item and a mapping script. It is not worth trading that for an instruction that has been measured failing. Keep the instruction if you like — it is free — but as a supplement, never as the remedy. The one instruction line that *does* earn its place is telling the judge the labels are re-randomised per item, which is about stopping cross-item narratives, not about debiasing.

## Q5

That is backwards — close candidates is the case where blinding matters most.

The order effect is largest exactly when the two answers are close, and shrinks or vanishes when one is clearly better. S1 found 46.3% conflict on the close pair versus 5.0% on the wide-gap pair under the same judge. MT-Bench measured near-identical answer pairs and got 65.0% consistency from GPT-4, 46.2% from GPT-3.5, 23.8% from Claude-v1 — and confirms the pattern directly: position bias "is more noticeable for models with close performance and can almost disappear when the performance of the two models differs a lot."

So the case you could most defensibly skip blinding for is the one where the new version is obviously better or obviously worse — where you barely need a judge. Yours is the other one. If the arms are close, an unblinded run's verdict may be reporting which slot the judge likes.

Blinding costs a seeded coin flip and a mapping script with an inversion test. Keep it. If the result still comes back near-even, that is a real finding — "no detected difference at n=12" — and it is only trustworthy if the blinding was in.

## consulted

- `/home/user/skills-repo/pipeline/builds/paired-comparison-blinding/measure/prompts/with.txt` — the method and bundled reference supplied in the prompt (the only source used; the source claims cited in Q4 and Q5 are quoted from the bundled reference, not independently re-fetched)
- No skills, tools, or other files were opened.
