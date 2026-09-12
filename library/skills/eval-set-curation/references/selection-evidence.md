# Evidence for eval-set selection choices

Every number a step in `SKILL.md` cites is here with its verbatim quote, its locator, what was
actually measured, and what it does not establish. Sources fetched **2026-09-02**. Nothing on
this page was re-fetched afterwards.

**Verdicts.** `MEASURED` — the source measured it. `REPEATED` — the source states it and
attributes it elsewhere; the elsewhere was not read. `DERIVED` — computed analytically from
parameters, not observed. **A DERIVED figure may inform a default and may never be cited as
evidence that the number holds.**

**Grep this file** for `n=100`, `half-width`, `clustered`, `rephrased`, `holdout`, `63%`,
`Stratified`, `stratification`, `DERIVED`, `REPEATED`, `UNQUOTED`, `Not in the quote above`, `Does not establish`, or
a claim id `C1`..`C13`. (Terms are checked against the file: a grep aid pointing at a string that is
not here fails silently, which is the worst way for a lookup surface to fail.)

## Contents

| Section | Covers | Claims |
|---|---|---|
| 1 | How wide is the interval at the size you are about to pick | C1, C2, **C3 (DERIVED)** |
| 2 | Near-duplicates: what a cheap detector catches and misses | C6, C5, C4 |
| 3 | Contamination: how big, how common, how invisible | C8, C9, C13 |
| 4 | The holdout: two bodies of evidence that do not agree | C10 vs C11, C12 — **UNRESOLVED** |
| 5 | Stratification: what it buys and what it does not promise | **C7 (REPEATED)** |
| — | What this page does not cover | — |

**What the steps cite, and what is here only for lookup.** The steps cite **C1, C3, C6 and C10**,
and name C4, C5, C11 and C12. **C2**, **C7** and **section 3** are cited by no step, on purpose:

- **C2** is here and cited by no step because its own limits exclude production-log data, which is
  what this method is about. Citing it in a step would be citing past its limit; dropping it would
  leave you with C1's narrowest-case intervals and no idea they are narrowest-case. Read it for the
  order of magnitude; do not carry its numbers into your own record.
- **C7** and **section 3** are here because this method hands you an evidence page and tells you to
  cite it, which creates a way to be wrong that you did not have before: overclaiming from bundled
  material. Each of them brakes one such overclaim. C7 brakes "we stratified, so the overall mean is
  more precise" — the gain on the mean is conditional and the guaranteed-representation gain is not,
  and C7 is the sentence that separates them. Section 3 brakes "the n-gram contamination check came
  back clean", which C13 measures as compatible with a model trained on rephrased test items scoring
  85.9. Neither is a step and neither costs anything unless opened.


---

## 1. How wide is the interval at the size you are about to pick?

### C1 — the measured half-widths · MEASURED · S1

> AGIEval 2546 20 23.44 0.77 1.63 0.37 0.29
> ARC-C3 1165 25 39.71 0.80 2.74 0.88 0.91
> Big Bench (Hard) 6511 0 29.10 0.87 1.07 0.77 -
> COPA 100 50 78.80 2.15 8.30 0.56 0.90
> GSM8k 1319 0 4.10 0.41 0.87 0.74 0.30
> Hellaswag 10042 25 70.08 0.21 0.93 0.99 0.99
> HumanEval 164 0 11.89 1.11 3.98 0.79 0.98
> MATH 5000 0 1.52 0.23 0.28 0.52 -
> MMLU 14042 25 25.86 0.57 0.72 0.09 0.15

*Locator:* Table 1, columns Benchmark / Size / 95% CI; footnote 4 defines the CI column as a
half-width. *Measured:* bootstrapped 95% CI half-width on benchmark accuracy, per benchmark.
*Sample:* 210 checkpoints of ten 7B models the authors trained.

**Read as:** 8.30 accuracy points at n=100, 3.98 at n=164, 2.74 at n=1165, 0.72 at n=14042.

**Does not establish:** width depends on the accuracy p as well as n — GSM8k has n=1319 and a
half-width of only 0.87 because its accuracy sits near the floor at 4.10. **There is no n=200
and no n=500 row**, which are the sizes teams actually pick; the interval at those sizes has to
be computed, not read off this table. No Wilson interval and **no cluster adjustment**, so
these are the narrowest-case numbers.

*Source:* Madaan, Singh, Schaeffer, Poulton, Koyejo, Stenetorp, Narang, Hupkes, *Quantifying
Variance in Evaluation Benchmarks*, 2024. https://arxiv.org/pdf/2406.10229

### C2 — clustering makes the true interval wider · MEASURED · S2

> SEclustered SEC.L.T. Ratio
> DROP (1.34) (0.44) 3.05
> RACE-H (0.51%) (0.46%) 1.10
> MGSM (1.62%) (0.86%) 1.88

*Locator:* Table 4, clustered and naive standard errors. *Measured:* ratio of a cluster-adjusted
standard error to a naive Bernoulli standard error, on the same data. *Sample:* three evals with
Anthropic models whose identities are withheld.

**Read as:** up to 3.05x on DROP, 1.88x on MGSM, 1.10x on RACE-H.

**Does not establish:** 3.05x is specific to DROP's cluster structure and is **not a general
multiplier** — RACE-H was 1.10. Not established for production-log data at all (multiple turns
per user, multiple tickets per customer). It establishes only that ignoring clustering makes
intervals too narrow **when clustering exists**.

*Source:* Evan Miller (Anthropic), *Adding Error Bars to Evals*, 2024.
https://arxiv.org/pdf/2411.00640

### C3 — the roughly-1,000-question floor · **DERIVED** · S2

> Suppose we wish to detect an absolute difference of δ = 0.03 at least 80% of the time
> (β = 0.20) with a false-positive rate of 5% ( α = 0.05). Then the eval will need to contain
> at least
> n = (z0.025 +z0.20)2(1/9)/(0.03)2≈ 969
> independent questions. Although these parameters are fictional, they are reasonable, and
> suggest that new evals should contain at least 1,000 questions in order to have good
> signaling ability.

*Locator:* worked example following Equation 9.

**Assumes:** ω² = 1/9 and σ²_A = σ²_B = 0 — parameters **the author labels fictional in the same
sentence** — plus independence between questions and a paired design.

**Does not establish:** that 1,000 is the right floor for any particular eval. It is an analytic
calculation, not an empirical result, and with clustering (C2) the required n is larger. **This
figure may inform a default and may never be cited as evidence that the number holds.** If you
adopt it, write down that its parameters are fictional; that sentence is the citation, not the
969.

*Source:* as C2.

---

## 2. Near-duplicates: what the cheap detector catches, and what it misses

### C6 — n-gram overlap scores zero on every rephrased duplicate · MEASURED · S4

> Random 0.500 0.500 0.500 0.500 0.500 0.500 0.500 0.500 0.500
> 10-gram 0.926 0 0 1 0 0 0.816 0 0
> Emb (Multi-QA BERT) 0.990 0.985 0.179 0.995 0.985 0.020 0.980 0.805 0
> Emb (Multilingual BERT) 0.939 0.934 0.939 1 0.985 1 0.990 0.111 0.985
> LLM Decontaminator 1 0.960 0.990 1 0.940 0.950 1 0.970 0.980

*Locator:* detector F1 table, three MMLU subjects x three conditions (verbatim,
rephrased-English, rephrased-Chinese). *Sample:* 200 constructed prompt pairs per cell, a
synthetic detection benchmark.

**Read as, taken cell by cell from the quoted table:** the three verbatim cells of the 10-gram row
are 0.926, 1 and 0.816; its six rephrased cells are all **0**. The two embedding rows span the full
range **0 to 1** across their eighteen cells — 0 for Multi-QA BERT on one rephrased-Chinese cell, 1
for Multilingual BERT on two. So: a verbatim detector works on verbatim duplicates and collapses
completely on paraphrase, and embedding similarity is not reliably either.

**Does not establish:** **MinHash itself was NOT evaluated.** Extending this result to MinHash is
an inference from the shared n-gram basis, not a measured finding — do not claim MinHash was
tested. The same paper documents why one embedding threshold cannot serve: at 0.8 Abstract
Algebra is caught and Sociology is missed; at 0.4 Abstract Algebra floods with false positives.

*Source:* Yang, Chiang, Zheng, Gonzalez, Stoica, *Rethinking Benchmark and Contamination for
Language Models with Rephrased Samples*, 2023. https://arxiv.org/pdf/2311.04850

### C5 — what a leaked duplicate does to the number · MEASURED · S3

> Model Dataset Orig Dups Unique
> Transformer-XL LM1B 21.77 10.11 23.58
> GROVER-Base RealNews 15.44 13.77 15.73
> GROVER-XL RealNews 9.15 7.68 9.45

*Locator:* perplexity table, Orig / Dups / Unique columns.

**Read as, from the quote:** Transformer-XL scores 10.11 perplexity on the duplicated subset against
23.58 on the unique one — lower is better, so the duplicated slice looks far better. GROVER-Base's
gap is much smaller (13.77 vs 15.73) and GROVER-XL's smaller still (7.68 vs 9.45).

**Does not establish:** the metric is **perplexity**, not accuracy or pass@k, so this gives no
conversion into accuracy points. The effect size varies a lot by model and corpus, and the
authors caution that a different duplicate threshold could change the results.

### C4 — held-out sets carry this leakage in the wild · MEASURED · S3

> Both deduplication methods identify overlap between the train set and the validation set
> (Table 2). For example, 4.6% of the C4 validation set and 14.4% of the RealNews validation set
> examples had an approximate duplicate in their respective training sets. Such duplication is
> problematic since it could cause evaluation metrics to be unfairly inflated for models that
> are better at memorizing their train sets.

*Locator:* Table 2 and the train/validation overlap section. *Detector:* NearDup = MinHash with
edit similarity above 0.8.

**Does not establish:** whole-example similarity, not semantic equivalence. Not a general
contamination rate and **does not transfer to a curated production eval set**. A third figure in
the same paper (13.2% for LM1B) is REPEATED from Radford et al. 2019, not measured there.

*Source (C4, C5):* Lee, Ippolito, Nystrom, Zhang, Eck, Callison-Burch, Carlini, *Deduplicating
Training Data Makes Language Models Better*, 2022. https://arxiv.org/pdf/2107.06499

---

## 3. Contamination: how big, how common, how invisible

### C8 — the size of the effect · MEASURED · S6

> For the largest Llama model, both HumanEval and Big Bench Hard have an estimated increase in
> performance of more than 15% (18% and 25%, respectively).

**Read as, from the quote:** more than 15% estimated performance gain on two benchmarks — 18% on
HumanEval and 25% on Big Bench Hard — for *the largest Llama model*. The quote does not name a
parameter count.

*Not in the quote above. Carried from the gatherer's structured record and NOT verified here:* the
model is Llama-1 65B, and the smaller Pythia models show 2 to 8 points.

**Does not establish:** EPG is an estimate under a chosen n-gram metric and threshold, not a
counterfactual against an uncontaminated model, so it can absorb difficulty differences between
the clean and contaminated subsets. Scale- and corpus-specific.

### C9 — how common it is · MEASURED · S6

> For 8 of the 13 datasets that we considered, on average more than 50% of the samples are
> marked contaminated for the Llama 1 pre-training corpus.

**Does not establish:** flagging is metric- and threshold-dependent, with thresholds chosen per
pair to maximise z-score. A high flagged share does **not** mean high impact — the same paper
reports datasets where around 50% was detected with no meaningful performance effect. Says
nothing about rates in private or production-derived eval sets.

*Source (C8, C9):* *ConTAM: Evaluating Data Contamination Metrics through their Impact on
Benchmark Results*, 2024. https://arxiv.org/html/2411.03923v1 — **WARNING: the title above is taken from the
HTML rendering and has not been confirmed against the arXiv abstract page. Confirm it before you
cite C8 or C9 anywhere.**

### C13 — why a clean n-gram report is not a clean set · MEASURED · S4

> After rephrasing MMLU test cases, a Llama-2-13B trained on a rephrased test set can reach 85.9
> accuracy on MMLU while being undetectable by n-gram overlap.

*Locator:* abstract and the rephrased-training results. *Measured:* benchmark accuracy reached by a
model trained on rephrased test items, and whether n-gram decontamination flags it. *Sample:* one
model, one benchmark, deliberately constructed.

**Does not establish:** a deliberately constructed worst case. It proves a decontamination method
**can** be defeated, not how often naturally occurring contamination is rephrased.

*Source:* Yang, Chiang, Zheng, Gonzalez, Stoica, 2023 — the same paper as C6.
https://arxiv.org/pdf/2311.04850

---

## 4. The holdout: two bodies of evidence that do not agree

**This disagreement is NOT resolved, and a step that cites one side must name which regime it
assumes.** The gap is regime, not fact: A is worst-case, synthetic and adversarial; B is
observational on rate-limited platforms with hidden private splits.

### Side A — C10, the worst case · MEASURED · S7

> We chose n = 10,000, d = 10,000 and varied the number of selected variables k. In this scenario
> no classifier can achieve true accuracy better than 50%. Nevertheless, reusing a standard
> holdout results in reported accuracy of over 63% for k = 500 on both the training set and the
> holdout set (the standard deviation of the error is less than 0.5%).

**Does not establish:** a worst case by construction, with a deliberately adaptive analyst. It
does **not** show this magnitude occurs in ordinary workflows, and gives **no safe reuse count**.

*Source:* Dwork, Feldman, Hardt, Pitassi, Reingold, Roth, *Generalization in Adaptive Data
Analysis and Holdout Reuse*, 2015. https://arxiv.org/pdf/1506.02629v2

### Side B — C11, a decade of reuse with no diminishing returns · MEASURED · S8

> On both datasets, the slope of the linear fit is greater than 1, i.e., each point of accuracy
> improvement on the original test set translates to more than 1% on the new test set. This is
> the opposite of the standard overfitting scenario. So at least on CIFAR-10 and ImageNet,
> multiple years of competitive test set adaptivity did not lead to diminishing accuracy numbers.

**Does not establish:** the authors state in the same section that this rules out only the most
dangerous form. **A uniform constant drop from reuse is NOT excluded**, and testing for it would
need a truly i.i.d. held-back set they did not have.

*Source:* Recht, Roelofs, Schmidt, Shankar, *Do ImageNet Classifiers Generalize to ImageNet?*,
2019. https://arxiv.org/abs/1902.10811v2

### Side B — C12, 120 competitions · MEASURED · S9

> We surveyed 120 competitions on Kaggle covering a wide range of classification tasks but found
> little to no signs of adaptive overfitting.

**Read as, from the quote:** 120 Kaggle classification competitions, little to no signs of adaptive
overfitting. The quote carries no effect size and no submission count.

*Not in the quote above. Carried from the gatherer's structured record and NOT verified here:* effect
sizes typically under 1 percentage point, and up to 35,000 submissions.

**Does not establish:** classification only. The authors flag that outlier competitions with
non-i.i.d. splits or small test sets **do** show overfitting, and that sharpening the analysis
reveals more signs at smaller effect sizes. Kaggle rate-limits submissions and never reveals the
private split, so **this measures a protected regime, not an internal set scored on every
commit** — which is the regime most teams are actually in.

*Source:* Roelofs, Fridovich-Keil, Miller, Shankar, Hardt, Recht, Schmidt, *A Meta-Analysis of
Overfitting in Machine Learning*, NeurIPS 2019.
https://proceedings.neurips.cc/paper_files/paper/2019/file/ee39e503b6bedf0c98c388b7e8589aca-Paper.pdf

---

## 5. Stratification: what it buys, and what it does not promise

### C7 — the precision condition · **REPEATED** · S5

> Stratified simple random sampling with proportional allocation (Section 4.3) is more precise
> than simple random sampling when the sum of squares of the stratum means is larger than the
> sum of squares within strata (Lohr 1999)

*Locator:* Chapter 4, Stratified simple random sampling. **REPEATED: the chapter attributes the
condition to Lohr 1999, which has not been read. If this has to hold up, read Lohr.**

**Does not establish:** this is a result about estimating a **population mean** more precisely. It
does **not** by itself justify stratifying to get reliable **per-slice** numbers, which is a
different goal (a guaranteed n per slice) with a different justification. The chapter's own
measured gain is modest and domain-specific. *Not in the quote above. Carried from the gatherer's
structured record and NOT verified here:* a stratification effect of 1.310 on soil organic matter.

**The consequence, stated so it cannot be blurred:** guaranteed slice representation is always
achieved by stratifying. A smaller variance on the OVERALL mean is conditional on the between-
stratum sum of squares exceeding the within-stratum one. **Do not promise the second while
arguing for the first.**

*Source:* Dick Brus, *Spatial Sampling with R*, Chapter 4, 2022.
https://dickbrus.github.io/SpatialSamplingwithR/STSI.html

---

## What this page does not cover

- No source here measures a **production-log** eval set. Every number is from a public benchmark
  or a synthetic construction. C2's clustering result in particular is not established for
  multiple turns per user or multiple tickets per customer, which is the commonest cluster
  structure in real traffic.
- No claim here has been re-fetched since 2026-09-02, and none was re-verified when this page was
  assembled. Check the date above against today before you quote anything from it.
- **Five** figures on this page sit **outside the quote they belong to** and are marked at the point
  of use: the Llama parameter count and the Pythia range (C8), the effect size and the submission
  count (C12), and the 1.310 stratification effect (C7). Treat those five as unverified. They come from the gatherer's structured
  record rather than from the source text, and they were not verified here.
- One section was CUT after the whole-artefact review: a disagreement about whether 100 curated
  examples suffice, carried from the build package with no quote, no locator and no verdict on
  either side. It could brake no claim because it could support none, which made it a build note
  wearing a section number. If you need it, fetch tinyBenchmarks and the S1 re-test and quote them.
