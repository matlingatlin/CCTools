---
name: paired-comparison-blinding
description: "Use when one grader or judge has to score two arms of a comparison side by side - A/B prompt tests, with-and-without skill runs, model bake-offs, before-and-after evals - and the verdict must not turn on which side was shown first or what the labels were called. Covers relabelling per item rather than per run, withholding the key, what the grader must be told, and why the un-blinding step needs a control that a swapped key would fail."
license: internal
---

# Blinding a paired comparison

A judge that can tell which side is the new one is not scoring the answers. Even when it
cannot, the position and the label still move the verdict on their own — and telling the
judge to ignore that does not work. So blinding is mechanical, or it is decoration.

## Important — the danger is at the un-blinding, not the blinding

Getting the labels on is easy and visibly wrong when it fails. Getting them back off is the
step where a bug **inverts** the result instead of breaking it: the run completes, the
numbers look plausible, and the losing arm is reported as the winner. Nothing downstream
can tell. Design the control for that first.

## Steps

**Randomise the ORDER, not only the label.** The measured effect is on the position a
candidate is shown in; the label carries part of it but is not all of it. Swap which arm is
printed first, per item, and relabel it at the same time. If your template prints the labels
in a fixed order — A first, then B — then relabelling moves the position too, but say so in
the code rather than relying on it: a template that later prints them in a different order,
or side by side, silently unwelds the two and leaves the position fixed.

**Do it per item, not per run.** One fixed assignment across the whole set gives the judge an
answer to work from after the first item it guesses. Use a seeded function of the item id so
the assignment is reproducible without being predictable from the data.

**Write the key to a file the grader is never given,** and say in the run's own record that
it was withheld. A key that lives in the same prompt is not withheld.

**Tell the grader the labels are re-randomised per item.** One sentence. Without it the
grader writes a cross-item narrative — "A was consistently stronger" — that describes labels
rather than arms and can contradict its own per-item rulings.

**Score from the per-item rulings only.** In a per-item-blinded design a judge's overall
summary cannot carry a verdict, because no cross-item identity exists for it to be about.
Read it for its critique of the rubric, never for its result.

**Control the un-blinding by inversion, not by round-trip.** A round-trip test — map the
labels on, map them off, get the originals back — passes just as happily when the mapping is
inverted. The control that catches it asserts that **a swapped key produces the opposite
verdict**, and that the two keys do not agree. Add the cheaper prevention too: stamp the key
with a run id or input hash and abort on a mismatch, so yesterday's key cannot be used at
all.

**Fail loudly on anything the mapping cannot resolve.** An unknown label, a result with no
key entry, a key entry with no result, a duplicate id. Never skip a row: a silent shrink
from twelve rows to nine changes the answer and is invisible in the tally.

## What the evidence supports, and where it stops

`references/position-bias-evidence.md` carries the sources and their verbatim lines. In
short:

- Swapping only the order of two candidates reverses a judge's verdict at rates the sources
  report **from 5.0% to 82.5% depending on the judge and the pair** — not a single headline
  number, and quoting only the high end oversells it.
- The effect sits partly on the **label** and not only on the slot, which is why relabelling
  helps at all — but only partly, which is why it is not sufficient on its own.
- It is **largest when the two candidates are close**, which is exactly the case a judge is
  needed for.
- Its **direction is judge-specific**: one model favours the first-shown candidate, another
  the second. So you cannot correct for it by always presenting the new arm in the
  disfavoured slot; you can only randomise.
- **One tested phrasing** of "ignore the order" did not remove the effect. That is one
  prompt in one paper, not a proof that no instruction could ever work — it is enough
  reason not to rely on an instruction when a mechanical remedy costs a coin flip.

What none of it establishes is that per-**item** relabelling beats a single fixed
assignment. That remedy is not measured in the literature cited, and the only measurement
behind it is local and small.

## In this repo (one instance)

`pipeline/evals/harness/blind.py` builds the relabelled prompt and the key;
`score.py` maps back; `selftest_score.py` holds the inversion control.
