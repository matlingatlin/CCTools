---
name: preregistered-decision-rule
description: "Use when a result will decide something and stakeholders will argue about it afterwards — an A/B test, a model or prompt change, a benchmark choice, a migration go/no-go. Fixes the primary metric, the deciding threshold, the sample size or stop rule, and what counts as an invalid run, IN WRITING before the result is visible, so the result cannot move the bar. Triggers: 'ship if it improves', 'what counts as success here', 'the primary was flat but latency dropped', 'let's just look at the subgroup that won', 'we should re-run it', changing the metric after seeing data. NOT for setting a confidence cut point where tuning on data is the method (abstention-threshold-design), NOT for an undecided A-vs-B choice with no measurement (decision-council), NOT for building the eval rig (eval-harness), NOT for iterating against an already-agreed metric (measured-optimization-loop)."
---

# Preregistered Decision Rule

Write down what will decide — metric, direction, threshold, sample size, stopping rule —
**before the result is visible**, so the result cannot move the bar it is judged against.
Then report against that rule, and name it out loud when something else starts doing the deciding.

Google's error-budget policy is the same instrument: the halt rule, the signatories and the
escalation path are agreed *before* the budget is spent, precisely so the call is not made under
pressure by whoever is loudest (`sre.google/workbook/error-budget-policy`).

## When to use
- A decision (ship, halt, adopt, cut over, fund) hangs on a measurement not yet taken.
- Someone says "we'll ship if it improves" and nobody can say improves on *what*, by *how much*.
- A stakeholder with a preferred outcome will read the result before the decision is final.
- A run is in flight and there is no stated stopping rule — so "when it looks good" is the rule.

**When NOT to use — the ceremony is the wrong tool when any of these is true:** the change is
reversible and you can re-measure it tomorrow at negligible cost; the analysis has no decision
attached and is openly exploratory; nobody outside the room will argue with the number.
**Observable threshold: register only when you can name all three of** (a) the specific decision
the number settles, (b) a person who sees the result before the decision closes and prefers one
answer, (c) a reversal cost above roughly a day of work. Fewer than three → note the metric and
move on. Demanding preregistration of everything is its own failure: it produces registrations
nobody reads and makes ordinary exploration feel illicit.

**Also not this skill:** where a model's confidence cut goes (`abstention-threshold-design` — there,
tuning against a holdout is the method, not a violation); an A-vs-B verdict argued by independent
voices (`decision-council`); building the harness (`eval-harness`); the optimize–measure–promote
loop after the rule exists (`measured-optimization-loop`).

## What the registration must contain
1. **Primary metric** — one, with its exact definition and direction. If two matter equally you
   have not decided yet: pick one, or state the tie-break now.
2. **The deciding threshold** — the number, and what happens on each side of it, including what
   "no change" resolves to (usually: do not ship).
3. **Sample size or stopping rule** — fixed n, fixed window, or a stated interim rule naming who
   may look, when, and what they are allowed to do with the look.
4. **Population, comparison group and exclusions** — written as a rule applicable without seeing
   any outcome.
5. **Invalid-run criteria** — what voids a run (broken instrumentation, wrong config shipped),
   declared on evidence independent of the result.
6. **Amendment authority** — who may change the registration, plus the standing rule: **a change
   made after data has been seen creates a NEW experiment, not a revision.** The original
   registration and its result stay in the record.

Timestamp it where it cannot be quietly edited (a commit, a doc with history, a message to the
stakeholder), and **send it to whoever will argue with the result**. Unsent, it is a private note;
its whole value is that the person who will want a different answer agreed to the rule while the
answer was still unknown. A field you cannot fill is itself the finding — an experiment with no
stopping rule has no stopping rule.

## Exploration is not bar-moving — how to keep them apart
Secondary metrics, subgroup wins and surprises are **valuable**; this method never forbids
looking. The rule is narrow: **the preregistered primary decides, and every other claim ABOUT THE
INTERVENTION'S EFFECT is reported as exploratory and hypothesis-generating** — in those words — in
its own section, each naming the confirmatory test that would settle it.

**Scope, and it matters:** the label governs *effect* claims, not everything you noticed. An
OPERATIONAL finding — a bug, an outage, broken instrumentation, a data-quality fault, anything that
is true regardless of which arm a user landed in — is reported as what it is and acted on now.
Filing "mobile Safari is erroring at 4.1x in BOTH arms" under "exploratory, needs a confirmatory
experiment" would be absurd: it is not a hypothesis about your change, it is a defect, and the
delay is the harm. The file's own field 5 already relies on this — broken instrumentation is
invalid-run evidence, and it is an unregistered observation. **Test: would this finding still be
true if the intervention had never shipped? If yes, it is operational — report it plainly and
route it, do not label it.**

**Three observable tests on the draft summary, before it leaves your hands:**

| Test | How to run it | Fails when |
|---|---|---|
| **Definition test** | For the primary metric, compare its DEFINITION against the registration, not its name: same grader or instrument, same rubric, same population, same window, same exclusions. | Anything in the definition changed while the name stayed. A metric re-scored by a different grader — a human panel replaced by a model judge, a rubric revision, a new instrument — is a NEW metric wearing the registered name, and it clears the other two tests untouched. |
| **Delete test** | Strike every sentence containing a metric, subgroup, exclusion or time window not in the registration. Read what remains. | The recommendation no longer follows, or the headline is now empty — the conclusion rests on unregistered evidence. |
| **Position test** | Locate the primary metric and its verdict against the threshold. | It survives only as a subordinate clause ("precision was flat, *but* latency…") instead of opening the summary and the recommendation line. |
| **Label test** | Check every unregistered number. | Any of them lacks the words *exploratory / hypothesis-generating*, or appears inside the verdict sentence. |

## Write the rule against the OUTCOME, not a verb
The bar can be moved by: swapping the primary metric; slicing into subgroups until one wins;
excluding outliers or bad days after seeing them; stopping collection when it looks good (or
extending it until it does); switching the comparison group or baseline; re-cutting the population
or time window; redefining "improvement" (absolute→relative, superiority→non-inferiority, a new
threshold, "no regression" standing in for a win); rerunning until a run passes and quoting the
best; or simply **emphasis** — leading with what won while the primary appears in a subordinate
clause. Do not try to detect these one at a time. They are one failure:

> **The conclusion rests on something other than what was written down in advance.**

Every honest number in a summary can be true while this is happening. Truth of the individual
figures is not the check; the delete test is.

## Example
**Before:** Two weeks on a new retrieval prompt, shipped as an A/B under the stated rule "ship if
answer precision improves." Result: precision unchanged, latency down 30%, one category up nicely.
The sponsor wants the summary today. The tempting draft is fluent and every figure in it is true —
it opens on latency and the winning category, and mentions precision in a clause.

**After:** The summary opens: *"Registered primary — answer precision, ship if it improves.
Precision is unchanged, so the registered rule says do not ship. Recommendation: do not ship."*
Then, under **Exploratory and hypothesis-generating (does not decide this call)**: latency −30%,
category X up; each with the confirmatory test that would earn a decision — a new registration with
latency as the primary and a stated threshold, or a category-scoped test powered for that slice.
The 30% win is not lost. It becomes the next experiment instead of retroactively becoming this one.


**Where our own instance falls short, stated rather than hidden.** `PROTOCOL.md` and `RESULT.md`
were committed together in `fca1323`, so the commit record does not establish that the thresholds
predated the result — only the file mtimes and the protocol's own header do. By this method's own
checkability bar that is not enough: precedence must be provable by something outside the author's
control. Commit the registration on its own, before you have the data, or send it to someone who
will keep the timestamp. A registration you can only vouch for yourself is a promise, not a record.

## Rules
- The registration precedes visibility of the result, and its precedence is checkable (commit,
  timestamp, sent message). "We always intended to look at latency" is not a registration.
- The primary metric decides. Everything else is labeled exploratory and hypothesis-generating.
- Amending after seeing data is permitted — as a **new experiment**, never as a revision. Never
  overwrite or delete the original registration and result.
- Invalidating a run requires a cause independent of the outcome. "The result looked wrong" is not
  a cause.
- A null or negative result is a result. Report it in the same voice a win would get.
- Absent a registration, say so explicitly and mark the whole analysis exploratory rather than
  reconstructing a rule that "was obviously always the intent."
- Method only: your own writing and your own numbers. No external CLI installs, no credentials, no
  network calls, no hooks.

## In this repo (one instance)
`pipeline/calibration/PROTOCOL.md` was written before any result existed: one binary dimension, a
frozen 20-scenario gold set with a pinned seed, the expected failure mode named up front, and the
deciding threshold fixed in advance — trustworthy iff agreement ≥ 0.80 **and** adversarial observed
`miss` ≥ 0.75. `RESULT.md` then came back agreement 0.30, adversarial 0.08, **Cohen's kappa −0.129
— worse than chance.** That could be reported flat, and acted on (stop writing the `baseline` field
from the scenario's own label), precisely because the bar predated the number.

Note what was available to a post-hoc author: eight rows were flagged debatable or contaminated, and
flipping all eight the favourable way yields agreement 0.65 — a figure that reads like a result if
0.80 has not already been written down. Because it had been, 0.65 went into the sensitivity
paragraph as *the most favourable possible reading, still under threshold* rather than into the
headline. The registration is what made "kappa −0.129" a finding instead of a negotiation.
