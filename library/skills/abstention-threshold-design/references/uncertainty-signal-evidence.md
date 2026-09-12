# What is measured about confidence signals, thresholds and coverage

Eleven claims, five sources, all fetched 2026-09-01. Every row carries the locator and a
verbatim quote. Read this when a stakeholder disputes a step in SKILL.md, when you need a
number to argue with, or when you are about to threshold a signal nobody has validated.

## Contents

- [How to read a verdict](#how-to-read-a-verdict)
- [1. Abstaining buys accuracy, and the price is coverage](#1-abstaining-buys-accuracy-and-the-price-is-coverage) - C1, C2
- [2. The threshold can be chosen with a guarantee](#2-the-threshold-can-be-chosen-with-a-guarantee) - C3, C10
- [3. A confidence number does not mean what it says](#3-a-confidence-number-does-not-mean-what-it-says) - C4, C5, C8
- [4. Calibration is not separation, and the difference is the whole step](#4-calibration-is-not-separation-and-the-difference-is-the-whole-step) - C9
- [5. What signal you threshold changes what you can ship](#5-what-signal-you-threshold-changes-what-you-can-ship) - C7
- [6. A threshold is valid only for the distribution it was fitted on](#6-a-threshold-is-valid-only-for-the-distribution-it-was-fitted-on) - C6, C11
- [Sources](#sources)
- [What would make these rows untrue](#what-would-make-these-rows-untrue)

## How to read a verdict

`MEASURED` - the source reports the number from its own experiment.
`REPEATED` - the finding is corroborated across several datasets or models within the source.

**These two tags arrive with the claims, from the package this skill was built from, and this
build did not re-verify any of them.** Three rows carry `MEASURED` while their own Limits line
says no number is reported: C5 is a definition, C10 is a guarantee with its empirical result
delegated to a figure, and C11 is an impossibility statement with a constructed illustration.
An independent reader of this file objected to all three, and the objection looks right. The
tags are not rewritten here, because the verdicts were set by whoever read the five PDFs, and
overruling one from a reading of the summary is the same substitution this file exists to
prevent. Read C5, C10 and C11 as definitions and guarantees carrying no effect size; the tag on
those three rows is not load-bearing.

Every quote below is verbatim from the source named. The coordinator who assembled the
package re-fetched all five PDFs and re-extracted them with pdfminer; 9 of 11 quotes matched
character for character after de-hyphenation, and the other 2 differ only by a footnote
marker and a lost `ff` ligature in the extraction. This build did not repeat that check.

## 1. Abstaining buys accuracy, and the price is coverage

**C1 · MEASURED · S1, Abstract; Sec 1; Sec 5.3, Table 6**

> "For example, using our method an unprecedented 2% error in top-5 ImageNet classification
> can be guaranteed with probability 99.9%, and almost 60% test coverage."

ImageNet top-5, RESNET-50, target risk r\*=0.02: test risk 0.0189 at test coverage 0.5935.
VGG-16 same setting: 0.0179 at 0.5351. Sample: ImageNet ILSVRC2014, validation set split
into ~25,000 calibration and ~25,000 test, delta = 0.001.
**NOT QUOTED, and marked so deliberately:** the full-coverage top-5 error for these models is
not stated in the text or in any table - it appears only as the coverage=1.0 end of the
risk-coverage curve in Figure 2c, roughly 8-10% by eye. The "error falls 4-5x" reading that
follows from it is therefore an inference off a figure, not a reported result. C2's
equivalent multiple rests on a stated baseline number instead of a figure reading.
**Limits:** 0/1 loss only; the paper says it does not "fully control false-positive and
false-negative rates". All guarantees assume calibration and test data are i.i.d. from the
same distribution.

**C2 · MEASURED · S1, Sec 5.1, text following Table 1**

> "Finally, we see that it is possible to guarantee with this method amazingly small 1%
> error while covering more than 78% of the domain."

CIFAR-10, VGG-16. r\*=0.01 gives test risk 0.0092 at coverage 0.7856 against a base model at
93.54% accuracy, so error on the accepted set falls about 7x for about 21 points of coverage.
The rest of the sweep is the row that matters when someone wants a cushion:
r\*=0.02 -> 0.0149 risk / 0.8466 coverage; 0.03 -> 0.0261 / 0.8966; 0.04 -> 0.0380 / 0.9318;
0.05 -> 0.0486 / 0.9596; 0.06 -> 0.0572 / 0.9784. Six points of coverage between the first
two rows, for six tenths of a point of risk.
**Limits:** the 93.54% baseline is a validation accuracy reported in prose, not a matched
full-coverage row of the same table. No Bonferroni correction was applied across the
target-risk rows, which the paper states outright: "With this small delta, and small number of
reported experiments (6-7 lines in each table) we did not perform a Bonferroni correction
(which can be easily added)".

## 2. The threshold can be chosen with a guarantee

**C3 · MEASURED · S1, Sec 5.1; Algorithm 1 (SGR) and Sec 3**

> "Observing the results in Table 1, we see that the risk bound, b\*, is always very close to
> the the target risk, r\*. Moreover, the test risk is always bounded above by the bound b\*,
> as required."

Every reported row satisfies test risk <= b\*, across 6-7 target levels x 6 tables
(CIFAR-10, CIFAR-100, ImageNet top-1 and top-5 for VGG-16 and RESNET-50). CIFAR-100 r\*=0.05:
b\*=0.0499, test risk 0.0413 at coverage 0.4450.
**Limits:** a high-probability statement over an i.i.d. calibration draw, not a per-input
guarantee. The paper does not claim the rejection mechanism is optimal: "it might be possible
to identify superior mechanisms for a given classifier f".

**C10 · MEASURED (tag disputed) · S5, Sec 5.5, Eq (15) and Proposition 4**

> "This is called a selective accuracy guarantee, because the accuracy is only computed over
> a subset of high-confidence predictions. This quantity cannot be controlled with techniques
> we've seen so far, since we are not guaranteed that model accuracy is monotone in the cutoff
> λ. Nonetheless, it can be handled with Learn then Test - a framework for controlling
> arbitrary risks."

The guarantee, verbatim, and the sentence that fixes alpha as an input rather than a result:

> "Proposition 4. Assume the {(Xi, Yi)}n i=1 and (Xtest, Ytest) are i.i.d. and lambda-hat is
> chosen as above. Then (15) is satisfied with probability 1 - delta."

One thing here is quoted and one is not, and they are marked apart.
QUOTED: the clause people skip in the first quote - **accuracy is not guaranteed to be
monotone in the cutoff**. "Higher cut, higher precision" is a property of a particular sweep,
not a law.
**NOT QUOTED:** that alpha is fixed before the cutoff is scanned rather than read off the
result. Proposition 4 says only that lambda-hat is "chosen as above"; neither quote held here
shows alpha entering the selection step, and the section's display equations were not
extracted. The reading is consistent with Eq (15), which states the target as 1 - alpha, but
it is an inference from the structure of the proposition, not a reported sentence.
**Limits:** the guarantee is MARGINAL, not per-input, and requires exchangeable calibration
and test data. The paper reports no in-text numeric effect size for this section - it points
to a figure - and none is invented here.

## 3. A confidence number does not mean what it says

**C4 · REPEATED · S2, Sec 1 and Figure 1; Sec 5.2 / Table 1**

> "While neural networks today are undoubtedly more accurate than they were a decade ago, we
> discover with great surprise that modern neural networks are no longer well-calibrated."

Uncalibrated ECE (15 equal-width bins): CIFAR-100 ResNet-110 **16.53%**, falling to 1.26%
under temperature scaling; CIFAR-100 Wide ResNet 32 15.0%; DenseNet 40 10.37%; Birds/ResNet-50
9.19%; ImageNet DenseNet 161 6.28%, ResNet 152 5.48%; CIFAR-10 ResNet 110 4.6%. 19
dataset-model rows across 8 datasets, vision and NLP.
**Limits:** the paper does not explain the mechanism - "It remains future work to understand
why these trends affect calibration while improving accuracy" - and flags that its own numbers
may be "affected by dataset split or by the particular binning scheme". One dataset (Reuters)
was already well calibrated (ECE at or under 1%) and temperature scaling did not help there -
**NOT QUOTED**, read off Table 1 rather than from a sentence. No abstention experiment is run.

**C5 · MEASURED (tag disputed) · S2, Sec 2, around Eq (1)**

> "We would like the confidence estimate P to be calibrated, which intuitively means that P
> represents a true probability. For example, given 100 predictions, each with confidence of
> 0.8, we expect that 80 should be correctly classified."

This is the source's own definition of what a stated confidence claims. From the same
paragraph: "In all practical settings, achieving perfect calibration is impossible."
**Limits:** definitional, not an experiment. The quantity "cannot be computed using finitely
many samples", so every calibration number anywhere is a binned estimate.

**C8 · REPEATED · S4, Sec 5.1, Figure 2 caption and Table 2**

> "the confidence levels primarily range between 80% and 100%, often in multiples of 5; 2) the
> accuracy within each bin is much lower than its corresponding confidence, indicating
> significant overconfidence."

Average ECE above 0.377 for GPT-3, GPT-3.5 and Vicuna against the paper's own 0.25 threshold
for significant deviation. GPT-4's average AUROC for separating its own correct from incorrect
answers is **62.7%**, against 50% for a coin. Five LLMs x eight datasets across five task types.
**Limits:** fixed-form and free-form QA with a unique ground-truth answer only - the paper
excludes summarization and open-ended QA. Black-box setting by choice. White-box logit methods scored better in the
paper's own comparison, AUROC 0.605 against 0.522 - **NOT QUOTED**, two figures lifted from a
comparison rather than from a sentence. Tied to 2023-era model snapshots and to their
elicitation prompts.

## 4. Calibration is not separation, and the difference is the whole step

**C9 · MEASURED · S4, Sec 5.2**

> "For example, with the CoT prompting on the GSM8K dataset, GPT-4 with 93.6% accuracy
> achieves a near-optimal ECE 0.064 by assigning 100% confidence to all samples. However,
> since all samples receive the same confidence, it is challenging to distinguish between
> correct and incorrect samples based on the verbalized confidence."

A signal can score beautifully on calibration and carry **zero** ability to rank a right
answer above a wrong one. There is no threshold on a constant. The paper's own instruction:
"The reliability of the given confidence must be assessed by considering multiple metrics,
such as both ECE and AUROC."
**Limits:** the degenerate case is shown on one model-dataset pairing and the paper does not
quantify how often it occurs. No coverage/risk abstention experiment is run.

## 5. What signal you threshold changes what you can ship

**C7 · MEASURED · S3, Abstract; Sec 1; Sec 5.2 and Table 1**

> "On average, the trained calibrator achieves 56.1% coverage (i.e., the system answers 56.1%
> of test questions) while maintaining 80% accuracy on answered questions, outperforming
> MaxProb with the same QA model (48.2% coverage at 80% accuracy)"

The unit of result throughout S3 is **coverage at a fixed accuracy target** (Cov@Acc), not
accuracy alone.
Cov@Acc=80%: MaxProb 48.23 -> calibrator 56.06 (+7.8 points). Cov@Acc=90%: 21.07 -> 29.42
(+8.4). Risk-coverage AUC 20.54 -> 18.47, 95% CI on the gap to the stronger baseline
[1.01, 1.69] by paired bootstrap over 1000 samples. Swapping the signal, not moving the cut,
bought the coverage.
**Limits:** a large residual gap to the oracle remains - "Best possible" is 74.92 Cov@Acc=80%
against 56.06 achieved, and the paper adds "achieving this bound may not be realistic". The
result is conditional on not having samples of the real test-time distribution, in the paper's
own words: "We note that our findings do not hold in the alternate setting where we have access
to samples from q_unk (instead of q_known)." And the accuracy figures are a lower bound, because
"62% of overconfidence errors are due to the model predicting valid alternate answers, or span
mismatches".

## 6. A threshold is valid only for the distribution it was fitted on

**C6 · REPEATED · S3, Sec 5.3, Figures 3a-3d**

> "Figure 3b shows that MaxProb is not well calibrated: it is underconfident in-domain, and
> overconfident out-of-domain. For example, for a MaxProb of 0.6, the model is about 80%
> likely to get the question correct if it came from SQuAD (in-domain), and 45% likely to get
> the question correct if it was OOD."

**A 35-point spread in true correctness at one identical stated confidence.** The number on
the score did not move; what it was worth did. Downstream: MaxProb yields 48.23% coverage at
an 80% accuracy target and 21.07% at 90% on the mixed stream.
**Limits:** the paper attributes the in-domain underconfidence to SQuAD's single-answer
training against multi-answer evaluation, and reports that removing the multiple answers
leaves MaxProb well calibrated in-domain while it "stays overconfident out-of-domain". Only
the five quoted words are verbatim; **NOT QUOTED** is the attribution sentence itself, which
is a paraphrase of the surrounding paragraph and not extracted as a line. The paper draws its
own boundary: "miscalibration out-of-domain does not imply poor selective
prediction on OOD data, but does imply poor selective prediction in our mixture setting."
Single model family, single task type.

**C11 · MEASURED (tag disputed, see How to read a verdict) · S5, Sec 3, around Eq (7) and Figure 10**

> "This is a stronger property than the marginal coverage property in (1) that conformal
> prediction is guaranteed to achieve - indeed, in the most general case, conditional coverage
> is impossible to achieve [14]. In other words, conformal procedures are not guaranteed to
> satisfy (7), so we must check how close our procedure comes to approximating it."

A global guarantee permits every error to land in one slice.
**NOT QUOTED**, both of the following being paraphrase rather than extracted lines: the source
illustrates the point with two groups at 90% and 10% frequency, covered always in the large one
and never in the small one, which still satisfies 90% marginal coverage; and what it offers in
place of a guarantee are two diagnostics, feature-stratified and size-stratified coverage, each
measuring realised coverage within a stratum against 1 - alpha.
**Limits:** the tutorial does not measure how large a real slice-level violation gets for the
selective-classification procedure, and reports no value for either diagnostic. Its `MEASURED`
tag is one of the three disputed under How to read a verdict above; this row carries a
definition, an impossibility statement and a constructed illustration, and no effect size.

## Sources

| id | title | authors | venue / year | url | fetched | read |
|---|---|---|---|---|---|---|
| S1 | Selective Classification for Deep Neural Networks | Geifman, El-Yaniv (Technion) | NeurIPS 2017 | https://arxiv.org/abs/1705.08500 | 2026-09-01 | full PDF, all 12 pages incl. every results table, cross-checked against ar5iv |
| S2 | On Calibration of Modern Neural Networks | Guo, Pleiss, Sun, Weinberger (Cornell) | ICML 2017 | https://arxiv.org/abs/1706.04599 | 2026-09-01 | full main body incl. Table 1; supplementary tables skimmed |
| S3 | Selective Question Answering under Domain Shift | Kamath, Jia, Liang (Stanford) | ACL 2020, 5684-5696 | https://arxiv.org/abs/2006.09462 | 2026-09-01 | full main body incl. Tables 1-2, Sec 5.3, Discussion; appendices skimmed |
| S4 | Can LLMs Express Their Uncertainty? | Xiong, Hu, Lu, Li, Fu, He, Hooi (NUS/EPFL/HKUST) | ICLR 2024 | https://arxiv.org/abs/2306.13063 | 2026-09-01 | full main body incl. Sec 5.1-5.2, Table 2, Limitations; appendix skimmed |
| S5 | A Gentle Introduction to Conformal Prediction | Angelopoulos, Bates (UC Berkeley) | arXiv monograph, v6 2022 | https://arxiv.org/abs/2107.07511 | 2026-09-01 | **PARTIAL** - full text held; Sec 1, 3, 5.5 read closely, the rest searched not read |

## What would make these rows untrue

- **C4, C8, C9 name specific model generations.** C8 and C9 measure GPT-3, GPT-3.5, GPT-4,
  Vicuna and LLaMA-2 as they were in 2023; C4 measures 2017 vision architectures. A later
  model may be better calibrated, and the model-specific figures are the perishable part.
  What none of these sources measures, at any date, is whether a given signal separates on a
  given system: that is a property of a deployment, not of the literature, and no future
  number here can settle it either way.
- **C1, C2, C3, C10 assume i.i.d. calibration and test data.** Every guarantee in them is
  void under distribution shift, which is not a caveat but the normal condition of a
  production stream. C6 is the measurement of what that costs.
- **Nothing here is about LLM agent tool-calling confidence**, and no source measures it.
  Extending these rows to an agent's self-reported certainty about an action is an
  extrapolation from C8, not a measurement held here.
- **No source here measures a modern reasoning model's token-level logprobs.** If your signal
  is one of those, no row here reports a value for it.
