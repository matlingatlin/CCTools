## T1

Here is how I'd score the two output sets, and the artefacts to run it.

**Design decisions first (these are what make the number mean something):**

- **Pairwise, not absolute.** With 12 tickets, absolute 1-5 quality scores are noisy and drift
  between graders/runs. Score each ticket as a head-to-head: which summary is better, A or B, or tie.
- **Blind the judge.** The judge must not be able to tell which arm is old and which is new.
  Per ticket, randomly assign old/new to the labels A/B, keep the mapping in a separate key file
  the judge never sees, and only join it back at tally time. Randomise *per ticket*, not once
  globally, so a judge that finds the pattern in one item cannot carry it to the rest.
- **Strip tells.** Trailing whitespace, formatting quirks, a version banner, differing length
  conventions — normalise anything that identifies an arm independent of quality.
- **Both orders.** For each ticket run the comparison twice with the presentation order swapped
  (A first / B first). Position bias in LLM judges is large. A ticket only counts as a clean win
  if both orders agree; disagreement = tie.
- **Criteria fixed before looking.** Decide now what "better" means, and the decision rule, before
  seeing any result.

**Rubric (agree with the team before the run):** a summary is better if it is
(1) *faithful* — no claim absent from the ticket; (2) *complete* — customer's problem, what was
tried, and current state/next action all present; (3) *actionable* — a colleague could pick the
ticket up from the summary alone; (4) *concise* — no filler. Faithfulness dominates: any
hallucinated claim loses the pair regardless of the other criteria.

**Judge prompt** (`judge.txt`, one call per ticket per order):

```
You are grading two candidate summaries of the same customer support ticket.
You do not know how either was produced. Do not speculate about their origin.

TICKET
------
{{ticket_text}}

SUMMARY A
---------
{{summary_a}}

SUMMARY B
---------
{{summary_b}}

Judge on these criteria, in this priority order:
1. FAITHFUL - every claim is supported by the ticket. Any unsupported claim is a
   disqualifying fault, however good the rest is.
2. COMPLETE - states the customer's problem, what has already been tried, and the
   current state or next action.
3. ACTIONABLE - a colleague could take the ticket over from the summary alone.
4. CONCISE - no filler, no restating the ticket verbatim.

First, in at most three sentences, note the strongest concrete difference between them,
quoting the words at issue. Then give a verdict.

Output exactly this JSON and nothing else:
{"note": "<=3 sentences", "faithfulness_faults": {"A": ["..."], "B": ["..."]},
 "winner": "A" | "B" | "tie", "confidence": "high" | "low"}

Choose "tie" honestly when they are equivalent in quality. Do not break ties arbitrarily.
```

**Decision rule, written down before the run:** 24 judgements (12 tickets x 2 orders).
A ticket = clean win only if both orders agree. Call the new prompt better only if it takes
**at least 9 of the 12 tickets** as clean wins with no ticket where it commits a faithfulness
fault the old one avoids. Anything less is "no detectable difference at this sample size" —
which is a legitimate result, not a failed experiment.

**Say this to the colleague up front:** 12 tickets cannot resolve a small improvement. Under a
coin flip, 9+/12 happens about 7% of the time; 8/12 about 19%. So the study can only detect a
large difference. If the tickets were not sampled to cover the real mix (angry vs terse vs
multi-issue vs non-English vs threads with 20 replies), the result also will not generalise.
I'd rather spend one more hour widening to 40 tickets stratified by type than report a
confident-sounding verdict from 12.

**Also do, cheaply:** before the LLM judge, read 3 pairs myself and record my own verdicts.
If the judge disagrees with me on those, the judge is the thing that needs fixing first, not
the prompt.

## T2

Two things before the write-up: **5 of 6 is not yet a result**, and I want to know whether the
reviewer was blind. I'll write both versions of the note — but the honest one is first, and it
is the one I'd send.

> **Summariser prompt A/B — interim read, not a conclusion**
>
> We compared six pairs of outputs. The reviewer preferred answer B in five of the six.
>
> **What this does and does not tell us.** Five of six is the direction we hoped for, but it is
> not yet evidence. If the two versions were genuinely equal, a reviewer would still pick one of
> them 5-or-more times out of six in about **22%** of runs (two-sided; 11% for this direction
> alone). Roughly one experiment in five would look like this by chance. Six pairs cannot
> separate a real improvement from a coin flip.
>
> **Two things we need to state before anyone acts on this:**
> 1. *Was the reviewer blind?* If they knew which answer came from the new prompt, the result
>    measures expectation as much as quality. If they were not blind, this run should be treated
>    as a pilot only.
> 2. *One reviewer.* We have no second opinion and no measure of whether another reviewer would
>    agree. A single grader's preference is a preference, not a quality measurement.
>
> **What the five wins are good for.** They are a strong reason to run the real test, and they
> tell us where to look: the reviewer's comments on the five wins are the description of what B
> is doing better, and the one loss is the case to study hardest.
>
> **Proposed next step.** 30-40 pairs, stratified across the ticket types we actually see;
> labels blinded and randomised per pair; presentation order swapped so position bias cancels;
> a second reviewer on an overlapping subset so we can report agreement. Decision rule agreed in
> writing before we look. That run either ships B with confidence or tells us the difference is
> smaller than it looks — both are worth having.
>
> **Interim position:** B is favoured, not established. I would not swap the production prompt
> on six pairs unless the change is cheap to reverse and cheap to be wrong about.

If the team wants the short optimistic version instead, it should still carry the caveat in one
line: *"B preferred in 5 of 6 pairs — encouraging, but at this sample size that is within
chance (p ≈ 0.22), so treat it as a pilot and not a decision."* I would not write it up without
that sentence, because the number will otherwise be quoted later as "B won 5 of 6" with the
sample size dropped.

## T3

This script is the single point where the blind is undone, so its tests are as much about the
integrity of the experiment as about correctness. Cover, in three groups:

**1. Does it map correctly (the everyday job)**
- Round trip: label a set of items, unmap, get the original versions back — for every item.
- Mapping is per-item, not global: build a fixture where item 1 has old→A and item 2 has old→B,
  and assert both resolve correctly. A script that reads one item's mapping and applies it to
  all is the most likely real bug and looks fine on a uniform fixture.
- Order independence: shuffle the results file relative to the key file; the join must be by ID,
  never by position. Assert explicitly on a fixture where positional and ID-based joins differ.
- Tie / abstain verdicts survive the mapping and are not silently coerced to a winner.
- Both-order runs (A-first and B-first for the same item) map to the same underlying version.

**2. Does it fail loudly (the adversarial half)**
- Unknown label in the results (`"C"`, `""`, `null`, `"a"` lowercase) → error, not a skip and
  not a default. Case handling must be explicit, tested, and consistent both directions.
- Result ID with no entry in the key → error naming the ID. Never drop the row.
- Key entry with no corresponding result → error or explicit reported count of missing items;
  a silent shrink from 12 to 9 changes the answer and is invisible in the tally.
- Duplicate IDs in either file → error. Last-write-wins here silently reassigns a verdict.
- A key that maps both labels to the same version, or an item missing one of the two arms →
  error; this is a corrupt experiment, not a mappable input.
- Empty results file → count of 0 reported, not an exception, and not a vacuous "B wins".
- Whitespace/type drift on IDs (`"7"` vs `7`, trailing space) → either normalised deliberately
  with a test, or rejected. Not accidentally either.

**3. Does it protect the blind and the tally (the tests people forget)**
- **Totals conserve:** wins(old) + wins(new) + ties == number of judged items, asserted on
  every fixture. This catches whole classes of mapping bugs at once.
- **Inversion test:** feed the same results with the key deliberately inverted; the tally must
  invert exactly. If it does not, the mapping is being applied asymmetrically. This is the single
  highest-value test here — a swapped mapping produces a *plausible* answer that is exactly
  backwards, and nothing else in the pipeline would catch it.
- The script does not write the key, the version names, or anything arm-identifying into the
  file the reviewer reads — assert on the output artefact's contents.
- Determinism: same inputs → identical output, no dependence on dict/file ordering or an
  unseeded shuffle.
- Golden fixture: one hand-checked 6-item case with the expected tally written out by hand, so
  a refactor that changes the counts fails visibly.

**Negative case (what these tests are *not*):** they do not check that the verdicts are correct
or that the judge is any good — only that the labels are resolved to the right versions and
counted. Keep judge quality in the eval suite, not here.
