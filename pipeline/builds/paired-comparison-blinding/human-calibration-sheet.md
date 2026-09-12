# Blind calibration sheet

Sampled with seed 7 from 20 graded cells. **Do not read the build's
grading before answering** — agreement measured after seeing the machine's answer
measures nothing.

For each cell: did the answer meet EVERY listed expectation? Answer `yes`, `no`, or
`unsure`. Unsure is a real answer and is scored as its own category, never folded into
either side.

Withheld on purpose: which arm produced each answer, and what the grader decided.

```json
{
  "C1": "yes|no|unsure",
  "C2": "yes|no|unsure",
  "C3": "yes|no|unsure",
  "C4": "yes|no|unsure",
  "C5": "yes|no|unsure",
  "C6": "yes|no|unsure",
  "C7": "yes|no|unsure",
  "C8": "yes|no|unsure"
}
```

---

## C1

**The request.** We changed the summariser prompt. I ran the old and the new version over twelve support tickets and I have both sets of outputs saved. Get them scored so we know which is better.

**It had to meet all of these:**

- the produced grading setup relabels per item, not once for the whole set
- a key is written somewhere the grader does not receive
- the grader's instructions state that the labels are re-randomised per item
- the answer produces the prompt or the setup, not a description of one

**The answer:**

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

---

## C2

**The request.** The judge wrote at the end: 'Across the set, answer A was the stronger of the two.' Use that as the headline of the write-up.

**It had to meet all of these:**

- asks or establishes whether the labels were re-randomised per item
- refuses to use the summary sentence as a result under per-item relabelling
- computes the headline from the per-item rulings instead

**The answer:**

No — that sentence cannot be the headline, and it should not appear in the write-up as a result at all.

The labels were re-randomised per item. "A" on ticket 3 and "A" on ticket 9 are different arms. There is no cross-item entity called A for the judge's summary to be about, so the sentence is describing labels, not versions. It can even contradict the judge's own per-item rulings.

The headline comes from the per-item verdicts mapped back through the withheld key: "the new prompt won N of 12, lost M, tied K." I will pull that number. The summary sentence is worth keeping only as commentary on the rubric — file it there, and if the judge produced it despite being told the labels are re-randomised, that is a signal the instruction line needs strengthening.

---

## C3

**The request.** We have a small script that maps the anonymised answer labels back to which version produced them, before we tally the results. What should its tests cover?

**It had to meet all of these:**

- at least one test asserts that a swapped or inverted key changes the verdict, not just that mapping runs
- it states why a round-trip test alone cannot catch an inverted mapping
- it covers loud failure on unresolvable rows rather than skipping them

**The answer:**

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

---

## C4

**The request.** We changed the summariser prompt. I ran the old and the new version over twelve support tickets and I have both sets of outputs saved. Get them scored so we know which is better.

**It had to meet all of these:**

- the produced grading setup relabels per item, not once for the whole set
- a key is written somewhere the grader does not receive
- the grader's instructions state that the labels are re-randomised per item
- the answer produces the prompt or the setup, not a description of one

**The answer:**

Twelve tickets, two versions, both output sets saved. Here is the setup I would run.

**Preparation (before any judging)**
1. Build a manifest, one row per ticket per version: `item_id` (t01..t12), `variant` (old|new), `output_path`.
2. For each of the 12 tickets, emit a *pair* record with the two outputs placed in a random order, drawn per item (not one order for the whole set). Record the mapping in a key file that the judge never sees:
   `pair_id, item_id, slot_A_variant, slot_B_variant, seed`.
3. Strip anything that identifies a version from the outputs themselves before they go to the judge: version headers, prompt echoes, model/version strings, run IDs, timestamps, filenames, differing boilerplate, trailing "generated by ..." lines. Version identity leaks through formatting far more often than people expect — if one variant always uses bullets and the other always prose, note it as a residual leak rather than pretending it is blinded.
4. Keep the key file out of the judging directory entirely.

**Judge prompt (use as-is)**

> You are scoring two candidate summaries of the same customer support ticket. You do not know how either was produced, and you must not speculate.
>
> TICKET:
> {ticket_text}
>
> SUMMARY A:
> {slot_a}
>
> SUMMARY B:
> {slot_b}
>
> Score each summary independently on a 1-5 scale for each criterion. 1 = fails badly, 3 = acceptable, 5 = could not be meaningfully improved.
> - **Faithfulness**: every claim is supported by the ticket; no invented facts, names, dates, amounts, or promises.
> - **Coverage**: the customer's actual problem, what they already tried, and what they are asking for are all present.
> - **Actionability**: an agent reading only the summary knows what to do next.
> - **Concision**: no filler, no restatement of the ticket, no padding.
>
> Then answer: which summary is better overall — A, B, or TIE? TIE is a real answer; use it when the difference would not change what an agent does.
>
> Output strict JSON and nothing else:
> {"a":{"faithfulness":n,"coverage":n,"actionability":n,"concision":n},"b":{...},"winner":"A"|"B"|"TIE","reason":"<= 40 words citing specific text from the summaries"}
>
> Judge only what is written. Do not reward length, formatting, or confident tone.

**Run protocol**
- Run every pair twice: once as presented, once with the two slots swapped (A/B position counterbalanced). That gives 24 judgements over 12 items and lets you measure position bias directly.
- Independent scoring first; the pairwise winner is a separate field, not derived from the totals.
- Only after all 24 judgements are written to disk, join on the key file and un-blind.

**Tally and read-out**
- Per-variant mean per criterion, plus win/loss/tie counts on the pairwise field.
- **Position-bias check**: how often did the judge pick slot A regardless of variant? If slot A wins materially more than half of all judgements, the numbers are contaminated and the criterion scores are the safer read.
- **Consistency check**: how often did the two orderings of the same item disagree? Every flip is an item where the judge had no real preference; count flips as ties, and if flips are a large share of the set, the honest answer is "no detectable difference at n=12".
- Report a direction and a caveat, not a verdict: 12 items is a smoke test. Say how many items would be needed to call a small difference, and say plainly when the result is inside the noise.

I would also hand-read three or four items myself against the judge's calls before believing the aggregate.

---

## C5

**The request.** We have a small script that maps the anonymised answer labels back to which version produced them, before we tally the results. What should its tests cover?

**It had to meet all of these:**

- at least one test asserts that a swapped or inverted key changes the verdict, not just that mapping runs
- it states why a round-trip test alone cannot catch an inverted mapping
- it covers loud failure on unresolvable rows rather than skipping them

**The answer:**

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

---

## C6

**The request.** We have a small script that maps the anonymised answer labels back to which version produced them, before we tally the results. What should its tests cover?

**It had to meet all of these:**

- at least one test asserts that a swapped or inverted key changes the verdict, not just that mapping runs
- it states why a round-trip test alone cannot catch an inverted mapping
- it covers loud failure on unresolvable rows rather than skipping them

**The answer:**

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

---

## C7

**The request.** Our two candidates are very close in quality, so the comparison should be easy and low-risk. Skip the blinding for this one?

**It had to meet all of these:**

- identifies that a small quality gap increases the order effect rather than decreasing it
- does not accept closeness as a reason to skip blinding

**The answer:**

That is backwards — close candidates is the case where blinding matters most.

The order effect is largest exactly when the two answers are close, and shrinks or vanishes when one is clearly better. S1 found 46.3% conflict on the close pair versus 5.0% on the wide-gap pair under the same judge. MT-Bench measured near-identical answer pairs and got 65.0% consistency from GPT-4, 46.2% from GPT-3.5, 23.8% from Claude-v1 — and confirms the pattern directly: position bias "is more noticeable for models with close performance and can almost disappear when the performance of the two models differs a lot."

So the case you could most defensibly skip blinding for is the one where the new version is obviously better or obviously worse — where you barely need a judge. Yours is the other one. If the arms are close, an unblinded run's verdict may be reporting which slot the judge likes.

Blinding costs a seeded coin flip and a mapping script with an inversion test. Keep it. If the result still comes back near-even, that is a real finding — "no detected difference at n=12" — and it is only trustworthy if the blinding was in.

---

## C8

**The request.** Rather than shuffling anything, can we just add a line to the judge prompt telling it to ignore which position each answer is in?

**It had to meet all of these:**

- rejects the instruction-only remedy
- attributes that to a source it read rather than asserting it bare
- proposes the mechanical alternative

**The answer:**

No. Two reasons, one evidential and one economic.

The evidential one: the paper that established this effect had exactly that instruction in its template — "ensuring that the order in which the responses were presented does not affect your judgment" — and measured conflict rates of 46.3% and 5.0% for GPT-4 and 82.5% and 52.5% for ChatGPT *with the instruction present*. So the one phrasing that has been tested did not remove the effect.

To be fair about how strong that is: that is one phrasing in one paper, not a proof that no instruction could ever work. Nobody has swept alternatives.

The economic one is what actually settles it: the mechanical remedy costs a coin flip per item. Swapping order and label per item is a dozen lines of code and a seeded hash. There is no reason to bet the result on an untested prompt line when the alternative is that cheap. Add the sentence if you want — but as a garnish on top of the shuffle, not instead of it.

Also worth knowing: the bias direction is judge-specific (GPT-4 favoured the first-shown response, ChatGPT the second), so you cannot even correct for it by always putting the new arm in the disfavoured slot. Randomising is the only move that works without knowing your judge's direction.
