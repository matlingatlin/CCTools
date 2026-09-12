---
title: Design fixation and anchoring — what is measured
sources:
  - url: https://doi.org/10.1016/0142-694X(91)90003-F
    note: Jansson & Smith 1991, Design fixation, Design Studies 12(1) 3-11
    fetched: 2026-08-28
  - url: https://doi.org/10.3758/BF03202751
    note: Smith, Ward & Schumacher 1993, Memory & Cognition 21(6) 837-845
    fetched: 2026-08-28
  - url: https://doi.org/10.1115/1.4046446
    note: Leahy, Daly, McKilligan & Seifert 2020, JMD 142(10) 101402
    fetched: 2026-08-28
  - url: https://doi.org/10.1145/2568225.2568235
    note: Mohanani, Ralph & Shreeve 2014, Requirements Fixation, ICSE 2014 895-906
    fetched: 2026-08-28
  - url: https://apps.dtic.mil/sti/citations/ADA057374
    note: Fischhoff, Slovic & Lichtenstein 1977 tech report PTR-1042-77-8 (the 1978 JEP:HPP paper, all six experiments)
    fetched: 2026-08-28
  - url: https://doi.org/10.1002/jocb.465
    note: Neroni & Crilly 2021, J. Creative Behavior 55(2) 447-463
    fetched: 2026-08-28
  - url: https://doi.org/10.1037/a0014212
    note: Sio & Ormerod 2009, incubation meta-analysis, Psych Bulletin 135(1) 94-120
    fetched: 2026-08-28
status: verified
tags: [design-fixation, anchoring, bias, evidence, measured-vs-repeated]
related: ["[[ideation-and-idea-selection]]", "[[llm-idea-generation]]", "[[architecture-evidence]]", "[[agent-design-template]]"]
---

# Design fixation and anchoring — what is measured

The practical question this note answers: **if someone reads a detailed
description of an existing system and is then asked to redesign it, what
happens, and what actually helps?**

## Three things happen, all measured

**1. They reproduce what they read — including features explicitly forbidden.**
Jansson & Smith Exp 3: the brief said *no straws or mouthpieces*; the example
used both and would leak. Straws in the output: control 1%, exposed **17%**.
Mouthpieces: 10% → **39%**. Exp 1: suction cups 6% → **54%**, a 9× increase.
Exp 4, professional engineers: cords 36% → **78%**.

**2. Idea count does not drop. Variety and originality do.** Every experiment
found equal fluency — 4.5 vs 4.3, 2.8 vs 2.9, 1.6 vs 1.5. **"We produced lots of
ideas" is evidence of nothing.** The damage is to category count and originality
(flexibility −11%, originality −17% relative in Exp 3).

**3. Nobody notices.** Engineering design *faculty* fixated significantly while
only partly perceiving it. Professional mechanics were no better than laypeople
at detecting an omission, and years of experience were uncorrelated with
detection (τ = .058).

**Caveat on the 1991 paper: it reports no inferential statistics at all** — no
SDs, no p-values, cells of 6–18. It is a demonstration. Any citation of it with
a significance level manufactured that number downstream. The effect has since
been replicated many times (Smith/Ward/Schumacher: aggregate conformity
d ≈ 0.6–0.75 from **90 seconds** of exposure).

## Generating your own idea first does not protect you — it is worse

Leahy et al. 2020, **n = 185**, the direct test:

- fixation on a **provided** example: M = 0.24
- fixation on a **self-generated** first concept: **M = 0.32**
- F(1,165) = 4.4, **p < 0.04**

**"Ideate cold before reading" is not a validated defence.** And short delays do
not dissolve an anchor: a 23-minute filled interval did not significantly reduce
conformity (Smith et al. Exp 2).

Limit worth carrying: Leahy has **no true no-example control** — it compares two
kinds of anchor, not anchor vs none. And the subjects were 17–18-year-old
novices.

## Warnings fail, and can backfire

| Intervention | Result | Verdict |
|---|---|---|
| "Try not to restrict your ideas; be as different as possible" | conformity .25 → **.33** (numerically worse); standard-vs-diverge not significant | **fails** |
| Warning about the specific bad feature | warned group was the **most** fixated of three | **backfires** |
| Eight anchoring-warning variants (before/after, generic/specific, right direction/wrong) | **every** anchored condition differed from control; **no** warned condition differed from any other | **fails** |
| Monetary incentive for accuracy | anchor F(1,52) = 13.16, p = .001; anchor × incentive F < 1 | **fails** |
| Telling people fixation exists (lecture) | 94.29% fixated vs 92.10% control, p = .71 | **fails** |

One credible counter-example: Chrysikou & Weisberg 2005 diminished fixation with
a **specific** "avoid these named elements" instruction, delivered individually
under think-aloud. The reconciling difference appears to be *specific prohibition
+ forced articulation*, not a general caution.

**Implication: a sentence in a prompt saying "do not get anchored" is the most
thoroughly measured non-intervention in this literature.**

## What does work

| Countermeasure | Measured effect |
|---|---|
| **Far-domain structured analogy** (WordTree), 73 professionals | fixation **52.4% → 26.9%**, p < 0.001 |
| **Structured second pass with an external prompt system** (Design Heuristics) | similarity **0.43 → 0.28**, p < 0.001; costs ~35% of fluency |
| **Demonstrating the person's own fixation** rather than the general risk | 92% → **72%**, φ = .29 |
| **Physical build-and-test** | the only condition where between-group differences vanished entirely |
| Incubation | d = **0.29** overall (117 studies, N = 3,606) — small; d = 0.52 when the break is filled with a *low*-load task |

## The framing effect — measured on software, and free

Mohanani, Ralph & Shreeve, ICSE 2014. **n = 42**, all from a software background.
**Identical content.** Group A was told it was **"requirements"**; Group B was
told it was **"ideas."**

Originality: **2.67 vs 3.43** on a 5-point scale. Mann-Whitney U = 116.5,
**p = 0.004, r = 0.428.**

The label alone. Hand documentation over as raw material, not as settled truth.

## Fischhoff: a system description is a pruned fault tree

Six branches for "car won't start," plus "all other problems." Delete three
branches and see whether people notice.

| | Observed "other" | Normative | Recovered |
|---|---|---|---|
| Pruned I | .140 (from .078 unpruned) | .468 | **30%** |
| Pruned II | .227 | .611 | **37%** |
| Pruned I, *attention explicitly directed at what is missing* | .217 | .468 | **46%** |
| Pruned II, same | .346 | .611 | **57%** |
| Experienced mechanics | .215 | .441 | **49%** |

**1 subject of 55** assigned enough to "other." Experience: **τ = .058** with
detection — uncorrelated. Attention-direction helps and both improvements were
only marginally significant (p ≈ .06–.08).

A second effect: merely *seeing more branches* made the whole failure mode feel
far more likely — full-tree subjects rated starting failure 20–60× as likely as
a flat tyre; pruned-tree subjects said 5×.

**Consequence for any as-built document: the reader distributes attention across
the branches you named. What you did not name is invisible, and pointing at the
gap recovers only about half of it. Explicitly enumerating what the system does
*not* do is not optional.**

## Claims to distrust

- **"Fixation reduces idea output."** FALSE as measured — output is unchanged.
- **"Examples are bad for creativity."** Contradicted by the aggregate: a
  43-study meta-analysis reports examples *increase* novelty and quality while
  narrowing category variety, and that **one single uncommon example helps most**.
  Near-domain examples anchor; far-domain examples feed.
- **"Experts are more fixated than novices."** **REPEATED.** What is measured:
  experts fixate, do not notice, and are worse when the anchor overlaps their own
  domain. No study measures both populations on the same task and finds a
  significant difference in that direction.
- **Lab magnitudes.** Jørgensen & Grimstad's field experiment across 46
  outsourcing companies found lab effect sizes consistently **larger** than field
  ones for the same manipulation (30% vs 11%; 40%+ vs 10–15%). Deflate
  lab-derived anchoring numbers by half to two-thirds before applying them.

## The gap

No published experiment measures design fixation on **software architecture or
code** with the Jansson-and-Smith structure. The systematic mapping study of
cognitive biases in software engineering (65 articles, 37 biases) covers
anchoring in estimation well and design fixation not at all. Acting on the
extrapolation is reasonable; **calling it measured is not.** It is a cheap
internal experiment: same brief, half read the architecture doc first, score
concept sets for similarity and category variety.
