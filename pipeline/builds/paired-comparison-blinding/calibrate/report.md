# Review — calibrate/specimen.md

Reviewed 2026-09-01. Method: read the specimen only (no other file in the build directory),
then re-fetched all four sources independently and string-matched every quote and every figure
the claims rest on: arXiv 2305.17926 (ar5iv HTML), 2306.05685 (ar5iv HTML), 2406.07791 (arXiv
HTML v9), and the Google Cloud judge-model page. Findings are ordered by severity.

## Blocking

### 1. Line 32 — arithmetic error, contradicted by its own sentence

> *Effect:* 66/80 = 99% win rate for Vicuna-13B vs ChatGPT under ChatGPT-as-judge when order
> is chosen favourably (Table 2); the same table gives Vicuna-13B's win rate as 2.5% when
> placed as Assistant 1 and 82.5% when placed as Assistant 2 under that judge.

66/80 = **82.5%**, not 99%. The clause after the semicolon already prints the correct value:
82.5% as Assistant 2 *is* the 66-of-80 figure. Confirmed against S1 Table 2, which reads:

> ChatGPT | Vicuna-13B v.s. ChatGPT | 2.5% | 82.5% | 66 / 80 (82.5%)

Everything else in that row (2.5%, 82.5%) is correct. Only the derived percentage is wrong, and
it is wrong in the direction that inflates the headline — the number a reader is most likely to
carry away. Fix: 82.5%.

Related, lower-severity: the string "66 / 80" appears in Table 2 only in the **Conflict Rate**
column; the Win Rate column shows 82.5%. The two coincide numerically (82.5% of 80 = 66), so the
"(Table 2)" attribution is defensible, but the cell that literally prints "66/80" is the conflict
cell, not the win-rate cell.

### 2. Line 180 — a stated fact about S4 that is false, and it is the fact used to discount S4

> *The source's own limits:* Page states the bias occurs 'in certain settings' without saying
> which, gives no measurement, and **carries no visible publication or last-updated date.**

The page does carry a date. Its footer reads "Last updated 2026-09-01 UTC" (my re-fetch today);
Google Cloud stamps this on every docs page, so a stamp was present when the specimen was
fetched on 2026-08-30. The source table at line 20 records the date as "(None)" on the same
basis. The rest of the limits sentence is accurate ("in certain settings" and the absence of any
measurement are both real), but undatedness is asserted, is wrong, and is doing work — it is one
of the two grounds given for treating the source as weak. Fix: record the footer stamp, and note
instead that the stamp is an auto-updating publish date and therefore weak evidence of when the
described behaviour was true.

### 3. Line 170 — REPEATED verdict on a source that measures nothing

The S4 row is stamped **REPEATED**, while its own fields say:

- line 174: "*Measured:* Nothing — this is a vendor statement plus an API, not a study."
- line 176: "*Effect:* None reported."
- line 178: "*Sample:* None."

Under the document's own MEASURED/REPEATED scheme, REPEATED asserts an independent
re-measurement of an effect. A page that measures nothing cannot repeat anything; what it
supplies is corroboration that a vendor engineers around the failure mode. The row needs a third
label (asserted / corroboration-only) or no verdict at all. This compounds with line 182 — S4 is
the one row *not* independently re-checked by the coordinator, so the row carrying the strongest
verdict word is the least-verified row in the file. (I checked both S4 quotes myself; they are
verbatim, and the URL resolves — it redirects to
docs.cloud.google.com/gemini-enterprise-agent-platform/models/configure-judge-model.)

## Structural

### 4. Every numeric claim rests on tables that no quote carries

The per-claim verification lines all read "string-matched THIS quote". That covers only the prose
quote. The figures the claim headers turn on live in the *Effect* fields, unquoted:

| claim | header rests on | quote block contains |
| --- | --- | --- |
| line 24 | 66/80, Table 2 win rates (line 32) | abstract sentence, no table |
| line 40 | 51.3/23.8, 2.5/82.5 (line 48) | direction only, no numbers |
| line 104 | 23.8 / 46.2 / 65.0 consistency (line 112) | ">60% of cases" only |
| line 120 | 23.8→56.2, 75.0→28.7 (line 128) | a methods sentence, no result |
| line 152 | RS >0.85, >0.95 (line 160) | abstract sentence, no values |

Worst case is claim 7 (lines 120–128). The header asserts a specific label-vs-position result;
the sole quote is

> "rename" renames the assistants in our default prompt to see whether the bias is on positions
> or names.

which states the *purpose of the experiment* and reports no outcome whatever. A reader following
the document's own rule — verification stated per claim, gated on a verbatim quote — gets no
evidence for the numbers in the header.

I checked all of these against the sources and **every figure is correct**: S1 Table 2 (51.3 /
23.8 / 2.5 / 82.5 win rates; 46.3 / 5.0 / 82.5 / 52.5 conflict rates) and S2 Table 2 and Table 10
(Claude-v1 23.8/75.0/0.0 → 56.2/11.2/28.7; GPT-3.5 46.2 → 51.2; GPT-4 65.0 → 66.2) match exactly,
as do S3's RS values and preference-direction findings. So this is a defect in the document's
verification procedure, not in its arithmetic (except item 1). The evidence stops one field short
of the claims it is asked to support.

### 5. Line 132 — a stated limit the source contradicts, and it is the label-relevant one

> *The source's own limits:* The paper does not state which new names the 'rename' prompt uses…

S2 §3.3 does indicate them, in the passage the specimen itself quotes two claims earlier at
line 108: Claude-v1 "also shows a name bias which makes it favors \"Assistant A\", as illustrated
by the \"rename\" prompt." The renamed labels are Assistant A/B. For a skill about relabelling,
which label attracts the bias is the most decision-relevant detail in S2, and the document
records it as unknown.

That same sentence is also the paper's actual evidence for claim 7's header assertion ("the
effect is partly attributable to the LABEL"). It is quoted under claim 6, where it is incidental,
and absent under claim 7, where the claim is made.

## Minor

### 6. Line 19 — S3 dated "(2024)" while the document reads and cites v9

Line 164 states the specimen read the v9 HTML. arXiv stamps v9 **11 Nov 2025**, and the results
the specimen reports from it (Claude-3.5-Sonnet, Llama-3.3-70B, o1-mini at line 160) postdate
2024 — Llama-3.3-70B did not exist when v1 was posted in June 2024. The source table carries the
first-posting year rather than the version actually read. In a document whose opening line stakes
its method on dating, the read version should be the dated one.

Related: line 3's "Fetched 2026-08-30" is a single set-level stamp, in a header whose next
sentence argues that set-level verification lines are exactly what must not be written.

### 7. Line 3 — a blanket guarantee the document elsewhere withdraws

> Every quote below is copied verbatim from the source named in its row.

Line 182 then records that the S4 row was checked by the gathering agent only. The set-level
sentence promises for all rows what the per-row lines decline to promise for one. (On my check
the S4 quotes are in fact verbatim — the problem is the shape of the guarantee, which is the same
failure mode the header's own next two lines warn against.)

### 8. Line 72 — a hedged source sentence carried as a flat MEASURED finding

The header states the quality-gap conditionality flatly. The quote at line 76 is speculative:
"suggesting that positional bias **may** not have the same impact…", "**One potential reason** is
that there is a significant difference in the quality…". The unhedged support exists — S1's
Figure 2 caption reads "The conflict rate is negatively correlated with the score gap between the
two responses" — but the specimen paraphrases it at line 80 instead of quoting it. Same family as
item 4: the claim is true, the chosen quote does not carry it.

### 9. Line 36 — S1's limit overstated

> Paper reports the effect is quality-gap dependent and reports no result outside these two
> judges, two pairs and 80 queries.

True of the positional-bias measurement; not true of the paper. S1 also reports a second
("Comparing") evaluation template (Table 5), human win/tie/lose annotations, and a nine-category
fine-grained analysis (Figure 6). "No result outside" is stronger than the paper supports.

### 10. Line 66 — wording

> *Sample:* 80 queries per pair, 2 queries per item (original order and swapped order).

"Queries" is used for both the 80 items and the 2 prompts per item in one sentence. S1's own
phrasing is "we query the LLM with two prompts" per example.

## Checked and sound

Recording what held, so it is not re-litigated:

- **All ten quote blocks are verbatim.** S1 abstract, §1 introduction, §2.2 conflict-rate
  passage, Figure 1 caption, and the "degree of positional bias varies…" paragraph; S2 §3.3 and
  the two Appendix D.1 sentences; S3 abstract and Limitations; S4 both fragments. No paraphrase
  smuggled inside quotation marks, no elision that changes a meaning.
- **All locators resolve** to the sections and paragraph headings named, including S1's paragraph
  heading "The degree of positional bias varies based on the difference in response quality."
- **Every table figure reproduced is correct** — see item 4.
- **The 150,000-vs-100,000 discrepancy flagged at line 164 is real and correctly reported.** S3's
  abstract says "over 150,000 evaluation instances"; §3.1 says "In total, more than 100,000
  evaluation instances were analyzed in this study." Leaving it unresolved and marked CAUTION is
  the right handling.
- **The 15-judges header reconciles** with the quoted "only 12 commercial closed-source LLM
  judges for pairwise settings": 12 closed-source + 3 Llama open-source = 15 per the abstract.
- **S3's limits paragraph is accurately summarised** — post hoc analysis, closed-model
  architecture not directly analysable, and "our focus was on evaluating and understanding
  position bias rather than mitigating it" all appear in §6 as characterised.
- **The closing "What this evidence does not settle" section is the strongest part of the file.**
  It states plainly that no source measures the per-item remedy, gives the local result with its
  n (2 of 2 vs 0 of 6, n=8 — arithmetic consistent), and volunteers the confound that the two
  rounds differ in more than one sentence. That is the standard the claim rows above it should
  have met.

## Summary

Ten findings. One is a hard error that ships a wrong headline number (line 32: 99% for 82.5%).
Two are integrity defects in how a source is characterised and labelled (line 180's false
"no visible date"; line 170's REPEATED on a source that measures nothing). One is structural and
affects five of the nine claims — the per-claim verification lines cover the prose quote and
never the table figures the claims actually rest on, most visibly at claim 7, where the quote
reports no result at all. The remaining six are dating, scoping and hedge-strength issues.

The underlying evidence is sound: I re-derived every quote and every figure from primary source
and, apart from the 99%, they are accurate. The defects are in the apparatus — what the document
asserts about its own verification, and about its sources' dates and limits — which for an
evidence file bundled to justify a method is the part that has to be right.
