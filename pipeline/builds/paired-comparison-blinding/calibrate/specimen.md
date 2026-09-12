# Why blinding a paired comparison has to be mechanical

Fetched 2026-08-30. Every quote below is copied verbatim from the source named in its row.
Verification is stated PER CLAIM, not once for the set: a single line pasted under every row
reads as a per-claim guarantee it does not make.

## Contents

- [Sources](#sources)
- [Claims](#claims)
- [What this evidence does not settle](#what-this-evidence-does-not-settle)

## Sources

| id | source | read | url |
| --- | --- | --- | --- |
| S1 | Large Language Models are not Fair Evaluators (2023) | full | https://arxiv.org/abs/2305.17926 |
| S2 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023) | full | https://arxiv.org/abs/2306.05685 |
| S3 | Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge (2024) | full | https://arxiv.org/abs/2406.07791 |
| S4 | Configure a judge model | Gemini Enterprise Agent Platform | Google Cloud Documentation (None) | full | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/configure-judge-model |

## Claims

### Swapping only the ORDER of two candidate responses reverses the judge's verdict often enough to invert a whole model-vs-model comparison; the paper's headline demonstration is that Vicuna-13B beats ChatGPT on 66 of 80 queries under ChatGPT-as-judge when the order is chosen adversarially.

**MEASURED** · Large Language Models are not Fair Evaluators · Abstract

> We find that the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. This manipulation allows us to skew the evaluation result, making one model appear considerably superior to the other, e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator.

*Measured:* Win rate of one candidate model over another, as a function of which slot (Assistant 1 vs Assistant 2) that candidate's response was placed in.

*Effect:* 66/80 = 99% win rate for Vicuna-13B vs ChatGPT under ChatGPT-as-judge when order is chosen favourably (Table 2); the same table gives Vicuna-13B's win rate as 2.5% when placed as Assistant 1 and 82.5% when placed as Assistant 2 under that judge.

*Sample:* 80 tested queries, two candidate pairs (Vicuna-13B vs ChatGPT; Vicuna-13B vs Alpaca-13B), two judges (GPT-4, ChatGPT).

*The source's own limits:* Paper reports the effect is quality-gap dependent and reports no result outside these two judges, two pairs and 80 queries.

*Verification:* coordinator re-fetched S1 independently and string-matched THIS quote against the full text

### The direction of the order effect is judge-specific, not universal: GPT-4 favours the FIRST-displayed response and ChatGPT the SECOND, on the identical template.

**MEASURED** · Large Language Models are not Fair Evaluators · Section 1 (Introduction); corroborated in Section 2.2

> Specifically, we demonstrate that GPT-4 exhibits a preference for the first displayed candidate response by consistently assigning it higher scores, even when the order of candidates is subtly altered. As illustrated in Figure 1 , merely swapping the presentation order can reverse evaluation outcomes. This bias is also present in ChatGPT, which typically favors the second response.

*Measured:* Which slot the judge's higher score goes to, holding the two responses fixed and swapping only their positions.

*Effect:* Direction only in this passage; the accompanying Table 2 shows Vicuna-13B win rate 51.3% as Assistant 1 vs 23.8% as Assistant 2 under GPT-4, and 2.5% vs 82.5% under ChatGPT, on the same pair.

*Sample:* Same 80-query setup, judges GPT-4 and ChatGPT.

*The source's own limits:* Two judge models only; the paper does not claim the direction generalises to other models.

*Verification:* coordinator re-fetched S1 independently and string-matched THIS quote against the full text

### Order sensitivity is quantified as a conflict rate: the share of items where the same judge, on the same two responses, returns contradictory verdicts before and after a swap. Rates ranged from 5.0% to 82.5% depending on judge and candidate pair.

**MEASURED** · Large Language Models are not Fair Evaluators · Section 2.2 (Revealing the Positional Bias)

> We found that GPT-4 exhibited conflict rates of 46.3% and 5.0%, respectively. In contrast, ChatGPT displayed considerably higher conflict rates, with figures of 82.5% and 52.5%, respectively. These findings indicate that LLMs can be self-conflicting due to the sensitivity of the response order in the template, with stronger models being less influenced by the placement of responses.

*Measured:* Conflict Rate = proportion of items on which the judge's winner changes when only the two responses' positions are swapped.

*Effect:* GPT-4: 46.3% (Vicuna-13B vs ChatGPT) and 5.0% (Vicuna-13B vs Alpaca-13B). ChatGPT: 82.5% and 52.5% on the same two pairs.

*Sample:* 80 queries per pair, 2 queries per item (original order and swapped order).

*The source's own limits:* The paper states the rate depends heavily on how far apart the two responses are in quality (see next claim).

*Verification:* coordinator re-fetched S1 independently and string-matched THIS quote against the full text

### The size of the order effect is conditional on the quality gap between the two candidates: it is large when the candidates are close and small when one is clearly better. This is the source's own stated boundary on its finding.

**MEASURED** · Large Language Models are not Fair Evaluators · Section 2.2, paragraph 'The degree of positional bias varies based on the difference in response quality.'

> We notice that the conflict rate of “Vicuna-13B v.s. Alpaca-13B” is much lower than that of “Vicuna-13B v.s. ChatGPT”, suggesting that positional bias may not have the same impact on the assessment of different responses. One potential reason is that there is a significant difference in the quality of responses between Alpaca models and Vicuna models, and positional bias is not strong enough to change the judgment in such a situation.

*Measured:* Conflict rate grouped by the score difference between the two responses (Figure 2).

*Effect:* 5.0% conflict rate for the wide-gap pair vs 46.3% for the close pair under GPT-4 (Table 2). Figure 2 reports conflict rate negatively correlated with score gap; the exact per-bin values are in a figure, not in the text.

*Sample:* Same 80-query, two-pair setup.

*The source's own limits:* This IS the limit the source states on its own headline finding.

*Verification:* coordinator re-fetched S1 independently and string-matched THIS quote against the full text

### Instructing the judge in the prompt to ignore order does not remove the order effect.

**MEASURED** · Large Language Models are not Fair Evaluators · Figure 1 caption (also Table 1 caption)

> Simply changing the order of candidate responses leads to overturned comparison results, even though we add the command “ensuring that the order in which the responses were presented does not affect your judgment” into the prompt.

*Measured:* Verdict flip under swap, with an explicit de-biasing instruction present in the evaluation template.

*Effect:* Not quantified in this caption; the quantification is the conflict rates above, which were produced with that instruction in the template (Table 1).

*Sample:* Same setup; the template carrying the instruction is reproduced as Table 1.

*The source's own limits:* Single de-biasing phrasing tested; the paper does not sweep alternative instructions.

*Verification:* coordinator re-fetched S1 independently and string-matched THIS quote against the full text

### Position bias is named and measured as a first-class limitation of LLM-as-a-judge: on near-identical answer pairs, even the strongest judge tested was order-consistent in only ~65% of cases, and the weaker judges far less.

**MEASURED** · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena · Section 3.3 (Limitations of LLM-as-a-Judge) and Table 2

> As in Table 2 , we found all of them exhibit strong position bias. Most LLM judges favor the first position. Claude-v1 also shows a name bias which makes it favors "Assistant A", as illustrated by the "rename" prompt. The position bias can be very significant. Only GPT-4 outputs consistent results in more than 60% of cases.

*Measured:* Consistency = percentage of cases where the judge gives the same result when the order of the two assistants is swapped; plus 'biased toward first' / 'biased toward second' shares.

*Effect:* Table 2, default prompt: Claude-v1 consistency 23.8% (biased toward first 75.0%, toward second 0.0%); GPT-3.5 46.2% (50.0% / 1.2%); GPT-4 65.0% (30.0% / 5.0%).

*Sample:* Two similar answers per MT-bench first-turn question (80 questions), judged in both orders, by 3 judges x 2 prompts.

*The source's own limits:* The source flags this as a hard case and says the effect is smaller elsewhere: 'Note that this test is challenging because the answers are very similar and occasionally indistinguishable even to humans. We will show that position bias is less prominent in some cases in Section D.1 .'

*Verification:* coordinator re-fetched S2 independently and string-matched THIS quote against the full text

### The effect is partly attributable to the LABEL, not only the slot: renaming the assistants in the prompt changed Claude-v1 from 75.0% first-preferring to 28.7% second-preferring and raised its order-consistency from 23.8% to 56.2%. This is the direct label-vs-position test.

**MEASURED** · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena · Section 3.3, description of the 'rename' prompt, and Table 2 / Table 10

> “rename” renames the assistants in our default prompt to see whether the bias is on positions or names.

*Measured:* Consistency under swap, and direction of preference, with the assistants' labels changed and everything else held fixed.

*Effect:* Claude-v1 default -> rename: consistency 23.8% -> 56.2%; biased toward first 75.0% -> 11.2%; biased toward second 0.0% -> 28.7%. GPT-3.5: 46.2% -> 51.2% consistency. GPT-4: 65.0% -> 66.2% (little change).

*Sample:* Same 80 MT-bench first-turn questions, near-identical GPT-3.5 answer pairs, both orders.

*The source's own limits:* The paper does not state which new names the 'rename' prompt uses, and reports the name effect for one judge (Claude-v1) only; the two other judges showed small changes. Cause is explicitly left open: the paper says it suspects the training data or the left-to-right causal-transformer architecture but 'leave a deeper study as future work'.

*Verification:* coordinator re-fetched S2 independently and string-matched THIS quote against the full text

### The order effect shrinks or vanishes as the two candidates' quality diverges, and is largest on open-ended tasks — the source's own stated scope limit, and an independent replication of S1's quality-gap finding.

**REPEATED** · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena · Appendix D.1 (Position bias), discussion of Tables 11 and 12

> Finally, we study how the model pairs influence position bias by using GPT-4 and the default prompt to judge three different model pairs. As shown in Table 12 , the position bias is more noticeable for models with close performance and can almost disappear when the performance of the two models differs a lot.

*Measured:* Consistency under swap, broken out by task category (Table 11) and by candidate model pair (Table 12).

*Effect:* Direction reported in prose; per-cell values are in Tables 11 and 12. Prose also states position bias 'is more noticeable on open questions like writing and stem/humanity knowledge questions.'

*Sample:* MT-bench first-turn questions; three model pairs; GPT-4 judge with the default prompt.

*The source's own limits:* This IS the source's stated limit on the headline number.

*Verification:* coordinator re-fetched S2 independently and string-matched THIS quote against the full text

### At scale — 15 judges, 2 benchmarks, 22 tasks, ~40 candidate models — position bias is confirmed to be systematic rather than sampling noise, and to vary strongly by judge and by task.

**MEASURED** · Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge · Abstract; Section 4 (Main Findings), 'Position Bias of Capable Judges are not Mere Random Variations'

> The findings confirm that position bias is not due to random chance and varies significantly across judges and tasks. While position bias is weakly influenced by the length of prompt components, it is strongly affected by the quality gap between solutions.

*Measured:* Three metrics: Repetition Stability (same judge, same prompt, repeated trials), Position Consistency (same winner after permuting order), Preference Fairness (direction and degree of primacy vs recency preference).

*Effect:* Repetition Stability generally above 0.85, and over 0.95 for Claude-3.5-Sonnet, GPT-4 and Llama-3.3-70B — i.e. repeated runs agree, so the swap-induced disagreement is not run-to-run noise. Per-judge Position Consistency and Preference Fairness values are in Table 2 (not reproduced here). GPT-4 and GPT-3.5-Turbo flip preference direction across datasets (recency-preferred on MTBench, primacy-preferred on DevBench); Claude-3.5-Sonnet is near preference-fair on MTBench but strongly recency-preferred on DevBench.

*Sample:* 15 LLM judges across MTBench and DevBench, 22 tasks, ~40 solution-generating models; abstract states 'over 150,000 evaluation instances'.

*The source's own limits:* Source states its own limits: 'First, we evaluated only 12 commercial closed-source LLM judges for pairwise settings and 4 for list-wise paradigms across two benchmarks, limiting the list-wise comparisons to three-candidate lists.' It also notes the analysis was post hoc, that closed-model architecture/size could not be analysed directly, and that the study measures rather than mitigates the bias. CAUTION, discrepancy noted at fetch time: the abstract says 'over 150,000 evaluation instances' while Section 3.1 of the same v9 HTML says 'In total, more than 100,000 evaluation instances were analyzed in this study.' Both figures are in the source; I did not resolve which is correct.

*Verification:* coordinator re-fetched S3 independently and string-matched THIS quote against the abstract, as its locator states

### A production evaluation vendor documents the same failure mode for its own pairwise judge and ships an order-swapping mitigation as a configuration flag.

**REPEATED** · Configure a judge model | Gemini Enterprise Agent Platform | Google Cloud Documentation · Section 'Response flipping'

> For PairwiseMetrics, the Gen AI evaluation service takes in responses for the baseline model and the candidate model. The judge model evaluates which response better aligns with the criteria in the metric_prompt_template. However, the judge model may be biased toward the baseline or candidate model in certain settings.

*Measured:* Nothing — this is a vendor statement plus an API, not a study. The mitigation offered: 'To reduce bias in the evaluation results, you can enable response flipping, where half of the calls to the judge model flips the baseline model and candidate model response using the Vertex AI SDK:' (AutoraterConfig(flip_enabled=True)).

*Effect:* None reported. The page gives no numbers, no residual-bias figure, and no evidence that flipping fully removes the effect.

*Sample:* None.

*The source's own limits:* Page states the bias occurs 'in certain settings' without saying which, gives no measurement, and carries no visible publication or last-updated date. Treat as corroboration that the effect is real enough to engineer around, not as evidence of its size.

*Verification:* gathering agent only - NOT independently re-checked by the coordinator

## What this evidence does not settle

**None of these sources measures whether per-ITEM relabelling beats a single fixed
assignment.** They establish that order and label move a judge's verdict. The per-item
remedy is this repo's own, and its only measurement is local: 2 of 2 graders not told about
re-randomisation asserted a cross-item identity, against 0 of 6 told. n=8, and the two rounds
differ in more than that one sentence.

**Nor does any of it measure the un-blinding control.** The inversion test is a design
argument, not a finding.
