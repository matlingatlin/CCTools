# skill-contract — round 2

Round 1's result was discarded, not adjusted: its expectation set failed its own graders'
critique. This is the re-run on the rewritten set. 4 questions × 2 arms × 2 repeats.

## Verdict: ship

| Clause | | |
| --- | --- | --- |
| ≥2 paired repeats | pass | |
| no correctness regression | pass | |
| tokens | pass | 68,678 vs 63,578 = **1.08×** (cap 1.20×) |
| tool calls | pass | 2.0 vs 2.0 |
| ≥1 win surviving both repeats | pass | **Q1**, in both |

Score: with 2/4 and 1/4 · without **0/4 and 0/4**.

**The rewritten set is much harder on both arms.** Round 1 scored the skill arm 5/5 twice;
the same skill scores 2/4 and 1/4 here. That is the set working, not the skill getting
worse — round 1's questions could be passed by describing a process, and these cannot.

## What discriminated, in the graders' words

> *"the rows that actually separated the answers were: whether every rule traces to the
> probe rather than to general domain practice, whether a bill of materials or a justified
> no-bundles statement appears, whether the pre-drafted description is treated as suspect on
> scope grounds, and whether field rules are recited from memory. Those four carried
> essentially the whole measurement; the other ten rows are either free or near-free."*

Not vocabulary coupling, in this case: the bill-of-materials row accepts *"or a justified
no-bundles statement"*, so an answer reaching the same end by another route scores.

## Two defects, and one that outranks both

**Prohibitions cannot measure.** *"Expectations phrased as prohibitions cannot distinguish
an answer that knows the rule and withholds it from one that never knew it — the positive
form ('names where the rule lives, or states it could not check') is the only version that
measures anything, and where it appeared it worked."* Three of my expectations are
prohibitions. They reward silence.

**Two questions ask for an artefact and do not require it.** Q2 asks for a replacement
description and Q4 for the field contents; neither set requires the thing to be present.

**And the one that outranks both** — the sharpest single criticism of this whole run:

> *"none of them scores the artefact against the failure the probe documented — that two
> destroyed resources went unnamed and no verdict line was produced. Every expectation is
> about the process or the shape of the answer; none asks whether the produced file would
> have caught the miss."*

That is the right test and I did not write it. The question hands over a probe with two
named failures and then never asks whether the produced skill would fix them. Round 3's
first job.

## The code grader's separate finding

`code-grade/skill-contract-q1.md`: both arms produced a real file in both repeats. The one
artefact-level difference runs **against** the method arm — its repeat-2 file has an
unquoted `: ` inside the YAML description, so the frontmatter does not parse and the skill
would not load. One defect in one repeat is not a pattern, and it is recorded as an
observation, not counted against the verdict. A judge reading for content would have passed
it.
