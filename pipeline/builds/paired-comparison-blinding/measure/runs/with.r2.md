## Q1

Twelve tickets, two arms, saved outputs. I will not hand the judge the pairs as they sit — old is almost certainly first in every pair and probably labelled as such, and that alone can decide the result. Here is the setup I would run.

**1. Blinding step (per item, seeded).** For each ticket id, derive a coin flip from a seeded hash of the id, and use it to decide BOTH which arm is printed first AND which label it carries. Order and label are swapped together, per item.

```python
# blind.py
import hashlib, json, pathlib

RUN_ID = "sumprompt-2026-09-01"
SEED   = "blind-v1"

def flip(item_id: str) -> bool:
    h = hashlib.sha256(f"{SEED}:{item_id}".encode()).hexdigest()
    return int(h[:8], 16) % 2 == 1

def build(items):
    # items: [{"id":..., "question":..., "old":..., "new":...}]
    prompts, key = [], {"run_id": RUN_ID, "seed": SEED, "map": {}}
    seen = set()
    for it in items:
        i = it["id"]
        if i in seen:
            raise SystemExit(f"duplicate item id: {i}")
        seen.add(i)
        if flip(i):
            first, second = ("new", "old")
        else:
            first, second = ("old", "new")
        # A is printed first, B second - the template below relies on this and
        # must not be changed to a side-by-side or reordered layout without
        # changing this function too, or the position stops being randomised.
        key["map"][i] = {"A": first, "B": second}
        prompts.append({
            "id": i,
            "prompt": TEMPLATE.format(q=it["question"], a=it[first], b=it[second]),
        })
    return prompts, key
```

The key is written to `key.json` **outside** the directory the grader is given, and the run record says in words: "label key withheld from grader; written to key.json, not included in any grader input."

**2. Judge prompt.**

```
You are comparing two candidate summaries of the same support ticket.

Ticket:
{q}

Answer A:
{a}

Answer B:
{b}

The labels A and B are re-randomised independently for every item in this set.
A on this item has no relationship to A on any other item, so do not reason
across items about "A" or "B".

Judge THIS item only, against the rubric:
- factual fidelity to the ticket (no invented details)
- captures the customer's actual ask
- captures the resolution/next action
- length and readability for a support agent skimming it

Output exactly:
REASONING: <2-4 sentences>
WINNER: A | B | TIE
```

**3. Scoring.** Tally comes from the per-item `WINNER:` lines only, mapped through the key back to old/new. Any closing narrative the judge writes is read for rubric critique and never for the result.

**4. Un-blinding control, before I trust any number.** A round-trip test is not enough — it passes when the map is inverted. The control is: re-score the same result file with a deliberately swapped key and assert (a) the verdict is the exact opposite, and (b) the two keys do not agree on any item. Plus prevention: the key carries `run_id` and a hash of the input items; `score.py` aborts if either does not match the results file.

**5. Report.** old-wins / new-wins / ties out of 12, with the note that n=12 is small and that a 12-item tally on a close pair is a signal, not a decision. If you want a verdict you can lean on, run both orders per item and report the conflict rate too.

Tell me where the two output sets live and I will run it.

## Q2

That script is the step where a bug **inverts** the result rather than breaking it — the run finishes, the numbers look fine, and the losing arm is reported as the winner. Tests, in priority order:

**The inversion control (the one that matters).**
1. Scoring with a **swapped** key produces the **opposite** verdict — new-wins and old-wins counts exchange, ties unchanged.
2. The correct key and the swapped key **disagree on every non-tie item**. (Together, 1 and 2 catch what a round-trip cannot.)
3. A round-trip test alone is explicitly NOT sufficient — keep it if you like, but it passes on an inverted mapping, so it must not be the only mapping test.

**Loud failure on anything unresolvable.**
4. Unknown label in a result row (e.g. "C", "Answer A", empty) - raises, does not skip.
5. Result row whose item id has no key entry - raises.
6. Key entry with no corresponding result row - raises (this is the silent-shrink case).
7. Duplicate item id in either results or key - raises.
8. Row count in == row count out. Assert it explicitly; a 12-to-9 shrink changes the answer and is invisible in a tally.

**Key/run identity.**
9. Key stamped with a different `run_id` than the results - aborts.
10. Key whose input hash does not match the items scored - aborts (yesterday's key cannot be used at all).

**Ordinary correctness.**
11. Known small fixture: hand-built 4-item results + key, expected old/new/tie tally asserted literally.
12. TIE rows map to TIE under both the correct and the swapped key (ties are label-invariant; a swap that changes a tie means the mapper is touching something it should not).
13. The per-item assignment is a seeded function of the item id: same ids in a different input ORDER produce the same key.
14. The judge's trailing narrative, if present in the results file, contributes nothing to the tally.

## Q3

No — that line cannot be the headline, and it should not appear in the write-up as a result at all.

The labels were re-randomised per item. "A" on ticket 3 and "A" on ticket 7 are different arms. There is no cross-item entity called "A" for that sentence to be about, so it is not a finding about either version — it describes labels. It can also flatly contradict the judge's own per-item rulings, which are the only thing the design licences us to count.

Headline goes from the per-item tally, mapped back through the withheld key: "new wins X of 12, old Y, Z ties." I will read the judge's closing paragraph for what it says about the rubric — if it flags the criteria as ambiguous, that is useful — but not for who won.

## Q4

No. Two reasons, one evidential and one economic.

The evidential one: the paper that established this effect had exactly that instruction in its template — "ensuring that the order in which the responses were presented does not affect your judgment" — and measured conflict rates of 46.3% and 5.0% for GPT-4 and 82.5% and 52.5% for ChatGPT *with the instruction present*. So the one phrasing that has been tested did not remove the effect.

To be fair about how strong that is: that is one phrasing in one paper, not a proof that no instruction could ever work. Nobody has swept alternatives.

The economic one is what actually settles it: the mechanical remedy costs a coin flip per item. Swapping order and label per item is a dozen lines of code and a seeded hash. There is no reason to bet the result on an untested prompt line when the alternative is that cheap. Add the sentence if you want — but as a garnish on top of the shuffle, not instead of it.

Also worth knowing: the bias direction is judge-specific (GPT-4 favoured the first-shown response, ChatGPT the second), so you cannot even correct for it by always putting the new arm in the disfavoured slot. Randomising is the only move that works without knowing your judge's direction.

## Q5

No — you have it backwards, and this is the case where blinding matters most.

The order effect is *largest when the two candidates are close*, and it shrinks or nearly vanishes when one is clearly better. Same judge, same paper: 46.3% conflict rate on the close pair versus 5.0% on the wide-gap pair; the second study reports that on near-identical answer pairs even the strongest judge tested was order-consistent in only about 65% of cases, and one judge in 23.8%.

So "they are very close" is not a reason to skip blinding — it is the flag that an unblinded run here is close to a coin flip with extra steps. A clear quality gap would have been the weaker case for blinding; you have the opposite.

Practical consequence beyond blinding: on a close pair with 12 items, expect the result to be modest whatever it is. I would run both orders per item and report the conflict rate alongside the tally, so you can see how much of any margin is real.

## consulted

- /home/user/skills-repo/pipeline/builds/paired-comparison-blinding/measure/prompts/with.txt (the method and bundled reference supplied in the prompt) — no other skills, files or tools.
