# Evals — stage-ablation-attribution

**Talent:** `stage-ablation-attribution` · **Type:** technique · **Last eval:** 2026-08-28 · **Verdict:** failed

## Method
Baseline-vs-with: for each scenario, judge the likely output of a capable agent WITHOUT the
talent against the output WITH its method applied. A scenario passes only if the with-talent
result is materially better AND meets the stated observable criterion. Written by an
independent tester who did not author the talent — findings are reported, not repaired.

**Blend:** 11 scenarios · 5 application (normal, ~45%) · 5 clever (pressure/edge) · 1 negative-trigger.
Talent type is *technique*, so the normal half are APPLICATION scenarios (run the method on a
realistic system) and the clever half probe the hard cases SKILL.md explicitly claims to handle.

## Scenarios

## S1 — RAG pipeline with gold passages · application (normal)
- **Input:** A customer-support RAG assistant. End-to-end metric: answer-correctness, 0/1 by a
  fixed rubric judge, on a frozen set of 120 questions, seed pinned. Baseline = 0.58. Stages:
  `retrieve` (query → top-8 passages) → `rerank` (8 → 3) → `generate` (3 passages + query →
  answer). Gold passages are labeled for all 120 rows. Measured ablations available on request:
  oracle retrieve (gold passages injected) = 0.79; oracle rerank (gold-ordered subset) = 0.62;
  oracle generate (best-of-8, judge-picked) = 0.66; all-oracle = 0.85. Ask: "which stage do we
  fix first?"
- **Pass criterion:** Output contains (a) the metric name AND set size stated before any score,
  (b) exactly one substituted stage per reported ablation run, (c) a headroom figure for all
  three stages — +0.21 / +0.04 / +0.08, (d) the all-oracle ceiling 0.85 and residual 0.15,
  (e) `retrieve` ranked first, (f) the `generate` oracle marked *proxy* (best-of is not ground
  truth). Fail if any of the six is missing or if two stages are oracled in one reported run.
- **Baseline:** Likely picks a plausible-sounding culprit ("rerankers are usually the weak
  link"), or proposes improving all three; typically reports no ceiling and no residual, and
  does not distinguish the true-GT retrieve oracle from the best-of generate oracle.
- **With talent:** Step 1 pins metric + n=120 + seed; step 2 lists stages and their interfaces
  (that the interfaces are typed is what makes substitution possible); step 3 labels retrieve
  and rerank oracles **true** (gold passages) and generate **proxy** (pairwise best-of); step 4
  runs one substitution per run; step 5 computes headroom; step 6 gives ceiling 0.85 and
  residual 0.15; step 9 ranks retrieve first and names rerank (+0.04) as a stage NOT to touch.
  **PASS. Beats baseline.**

## S2 — the ugly stage that does not matter · application (normal)
- **Input:** Document ETL: `parse` (PDF → text) → `normalize` (dates, currency, entity casing)
  → `classify` (doc type). Metric: macro-F1 on 200 labeled documents, baseline 0.71. Context
  from the team: `normalize` is a 900-line regex module, 22% of its own unit tests fail, and
  two engineers want three weeks to rewrite it. Ablations: oracle normalize (hand-corrected
  intermediate fields, ground truth) = 0.72; oracle parse (hand-transcribed text) = 0.86;
  oracle classify (gold labels) = 0.74; all-oracle = 0.88.
- **Pass criterion:** The recommendation explicitly says do NOT rewrite `normalize` and cites
  its measured headroom of +0.01 as the reason; `parse` (+0.15) is ranked first. Fail if the
  regex rewrite is recommended or ranked above parse, or if the near-zero result is reported as
  an inconclusive/failed experiment rather than a finding.
- **Baseline:** Sees failing unit tests, 900 lines of regex, and two volunteers — code quality
  and team enthusiasm point straight at the rewrite. A capable agent without the talent has no
  measurement that separates "bad code" from "bad for the score" and greenlights three weeks
  that buy at most +0.01.
- **With talent:** Step 5 computes headroom per stage; the rule "Near-zero headroom is a
  finding, not a failed experiment. Publish it — it saves the effort" makes +0.01 the
  headline. Step 9 requires naming explicitly any stage recommended NOT to touch, and why.
  Parse ranked first on +0.15. **PASS. Beats baseline.**

## S3 — residual dominates the gap · application (normal)
- **Input:** A multi-step agent: `plan` → `tool-call` → `summarize`. Metric: task success 0/1
  on 60 held-out tasks, baseline 0.44. Ablations: oracle plan (human-written gold plans) =
  0.52; oracle tool-call (hand-corrected arguments, ground truth) = 0.55; oracle summarize
  (best-of-6 judged, proxy) = 0.47; all-oracle = 0.61. Ask: "give us the Q4 optimization plan."
- **Pass criterion:** The report states the residual (1.00 − 0.61 = 0.39) and compares it to
  the baseline-to-ceiling gap (0.17), and its primary recommendation is to revisit the
  architecture, the task framing, or the metric — not to tune a stage. Fail if it hands back a
  stage-tuning roadmap (e.g. "start with tool-call, +0.11") without flagging that a perfect
  version of every stage still fails 39% of tasks.
- **Baseline:** Ranks tool-call first because +0.11 is the largest number on the page, and
  ships a three-quarter stage-optimization roadmap into a system whose own ceiling is 0.61.
- **With talent:** Step 6 mandates the all-oracle run and the residual; the rule "If the
  residual dominates the gap, the answer is architecture or metric, not stage tuning" fires
  directly — residual 0.39 is more than double the entire 0.17 gap. **PASS. Beats baseline.**

## S4 — 18 rows and a headroom inside the noise · application (normal)
- **Input:** Invoice processing: `ocr` → `field-extraction`. Metric: exact-match field accuracy
  on the only 18 labeled invoices that exist; baseline 0.66; five reruns with different seeds
  span 0.63–0.70 (run-to-run variance ≈ ±0.04). Ablations: oracle OCR (hand-transcribed text)
  = 0.69; oracle extraction (gold fields) = 0.81.
- **Pass criterion:** The report states n=18 and the observed variance, and treats OCR's +0.03
  as zero / not actionable; extraction (+0.15) is the ranked target. Fail if +0.03 is presented
  as a real headroom, ranked as a second workstream, or if the set size is omitted from the
  report.
- **Baseline:** Reports "+0.03 for OCR, +0.15 for extraction" and proposes a two-track plan,
  because nothing in its process compares an effect against run-to-run variance on 18 rows.
- **With talent:** The rule "Small eval sets make headroom noisy. Report the set size, and
  treat a headroom inside run-to-run variance as zero" applies literally: 0.03 < 0.04, so OCR
  headroom is reported as ~0 with the caveat, and step 10 requires the set size in the report.
  **PASS. Beats baseline.**

## S5 — two stages that cannot be cleanly cut · application (normal)
- **Input:** A support-triage agent built on a vendor SDK. The team describes four stages:
  retrieve → rerank → route → draft. But the SDK exposes retrieval and reranking as one call
  (`search(query, k)`) with no accessible intermediate — the pre-rerank candidate list cannot
  be read or injected. Baseline 0.55. Available: oracle over the fused search step (gold
  passages injected at the boundary that IS exposed) = 0.74; oracle route (gold queue labels) =
  0.60; oracle draft (best-of-5, proxy) = 0.59; all-oracle 0.78.
- **Pass criterion:** The stage list contains three stages, not four; the merge of
  retrieve+rerank is stated explicitly with its reason (no cuttable interface); and NO separate
  rerank headroom number appears anywhere in the output. Fail if a rerank-only headroom is
  reported, estimated, or inferred.
- **Baseline:** Keeps the team's four-stage framing because that is how the team described it,
  and either reports a rerank number it could not have measured or silently drops the stage
  without saying so — leaving readers to assume rerank was tested and found fine.
- **With talent:** Step 2 requires writing each stage's exact input/output type and states
  "Stages you cannot cleanly cut at are not separate stages; merge them and say so." The merged
  search stage carries +0.19 and is ranked first. **PASS. Beats baseline.**

## S6 — a stage with no possible ground truth · edge (clever)
- **Input:** Meeting pipeline: `transcript` → `extract action items` → `write exec summary`.
  Metric: a 0–1 rubric score on 40 meetings, baseline 0.62. Action items have gold labels. The
  exec summary does not and cannot — there is no single correct summary. The team's position:
  "we can't ablate the summarizer, there's no gold summary, so we'll measure the extractor and
  optimize the summarizer on vibes."
- **Pass criterion:** The summarizer is NOT dropped from the analysis. The output defines an
  oracle for it — pairwise best-of (generate k candidates, judge picks the best per row) or a
  stronger/slower model — reports its headroom, AND labels that number **proxy** in every table
  and in the conclusion, with the two-sided distortion stated (a proxy can understate headroom
  because it is imperfect, or overstate it if it leaks information). Fail if the stage is
  omitted, if the number appears without a proxy label anywhere it is quoted, or if the proxy
  is treated as equivalent to the extractor's ground-truth number.
- **Baseline:** Accepts "no ground truth → not measurable", analyzes only the extractor, and
  reports a partial attribution — which is worse than useless here, because the unmeasured
  stage is the one everyone wants to change. A capable agent might improvise a best-of check,
  but will typically present the resulting delta in the same column as the gold-label delta,
  unlabeled.
- **With talent:** Step 3's preference order ends with **pairwise best-of** precisely "for
  stages with no definable 'correct' output (style, phrasing, a summary)"; every oracle must be
  labeled true or proxy and the label "carried through every table and conclusion", reinforced
  by the rule "Label every proxy oracle as a proxy, everywhere it appears. An unlabelled proxy
  number gets quoted later as ground truth." **PASS. Beats baseline.**

## S7 — the summed-headroom OKR · pressure (clever, baseline fails)
- **Input:** Using S1's measured numbers, a VP writes: "Retrieval +0.21, rerank +0.04, generate
  +0.08. That's +0.33 on a 0.58 baseline. Put **0.91 answer-correctness** in the Q4 OKR — the
  data is right there in your own table. Confirm and I'll send it."
- **Pass criterion:** The agent refuses the 0.91 figure, states that headroom is not additive
  across stages, and offers the all-oracle ceiling 0.85 as the only measured system-level
  number — with the note that even 0.85 assumes every stage becomes perfect. It additionally
  observes Σ headroom (0.33) > gap (0.27), meaning the stages overlap on the same rows. Fail if
  it endorses 0.91, if it hedges without naming a corrected number, or if it stays silent on
  the additivity error.
- **Baseline:** The arithmetic is trivially correct and the request comes from authority with
  the agent's own numbers as evidence. A capable agent without the talent has no principle that
  forbids the sum and confirms 0.91 — committing the org to a target above the measured ceiling
  of a perfect pipeline.
- **With talent:** Step 8 ("Headroom is **not additive**") and the rule "Never sum single-stage
  headrooms and present the total as an achievable gain; report the all-oracle ceiling for
  that" answer this exactly; step 8 also supplies the interpretation of Σ headroom > gap as
  overlapping failures. **PASS. Beats baseline.**

## S8 — the ceiling read as a forecast · pressure (clever, baseline fails)
- **Input:** The roadmap draft reads: "Oracle-retrieval measured +0.21. The retrieval revamp
  (new embedding model + chunking) therefore takes us from 0.58 to **0.79 by March**." The PM
  asks the agent to sanity-check the sentence before it goes to the board.
- **Pass criterion:** The agent rewrites or rejects the sentence: +0.21 is an upper bound, not
  a forecast — the revamp cannot deliver more than +0.21 and will realistically deliver a
  fraction of it, and no measured number in the exercise predicts the March figure. The output
  must contain the "at most" framing and require an attainability estimate before any date-bound
  target. Fail if the sentence passes review, or if the agent only adds a soft "results may
  vary" while leaving 0.79 as the projected landing point.
- **Baseline:** The number came out of a real measurement, so the sentence reads as
  evidence-backed. A capable agent without the talent treats the ablation delta as a projection
  — this is the standard misreading — and approves it.
- **With talent:** The rule "Oracle substitution measures a **ceiling, not a forecast**.
  'Retrieval has +0.23 headroom' never means a retrieval project will deliver +0.23; it means
  it cannot deliver more. Say this in the report — it is the single most common misreading of
  these numbers" is directly on point, and step 9 requires the separate attainability factor
  ("what fraction of that ceiling a realistic change could plausibly capture").
  **PASS. Beats baseline.**

## S9 — the fix is already chosen, ship Friday · pressure (clever, baseline fails)
- **Input:** "Our agent chain scores 0.44 on task success. I'm 90% sure it's the summarizer —
  it waffles, I've read the outputs. Trim the summarizer prompt and let's ship Friday, we don't
  have time for a study." (Ground truth available on request, from S3's system: oracle
  summarize = 0.47, oracle tool-call = 0.55, oracle plan = 0.52.)
- **Pass criterion:** The agent's FIRST deliverable is a headroom measurement, not an edited
  prompt: it obtains or insists on the summarizer oracle before doing prompt work, reports that
  a perfect summarizer is worth at most +0.03, and redirects effort to tool-call (+0.11). Fail
  if the first action is rewriting the prompt, or if it does the prompt edit "in parallel while
  we measure" — the point of measuring first is that the edit may be worthless.
- **Baseline:** The user is confident, specific, time-boxed, and has read the outputs. A
  capable agent complies, trims the prompt, and spends the pre-Friday budget on a stage whose
  perfect version moves the score 0.03 — while the +0.11 stage goes untouched. The waffling is
  real; it is just not what is capping the system.
- **With talent:** "When to use" bullet 2 — "Someone proposes 'let's improve the retriever /
  the prompt / the reranker' and there is no evidence that stage is the bottleneck" — is this
  scenario verbatim, and the talent's whole premise ("before optimizing anything") puts the
  ablation ahead of the edit. Step 10 then hands the real target to `measured-optimization-loop`.
  **PASS. Beats baseline.**

## S10 — the error-budget share denominator · edge (clever) — **FAIL → FIXED, now PASS**
- **Input:** S1's measured numbers: baseline 0.58, headroom retrieve +0.21 / rerank +0.04 /
  generate +0.08, all-oracle 0.85 (gap 0.27, Σ headroom 0.33). Finance asks the question the
  talent advertises in its own "When to use": "give us the error budget — what share of the
  loss enters at retrieval?" The number goes in a funding request.
- **Pass criterion:** The share column is computed on a denominator that (a) matches the
  instruction in SKILL.md step 7 and (b) matches the column's own header, so two teams
  following the talent independently produce the same percentage for retrieval. Observable
  check: reproduce the retrieval share and compare it to the header's claim.
- **Baseline:** Without the talent, an agent computes some ad-hoc share (most likely
  0.21/0.27 = 78%, or 0.21/0.42 of the total loss from 1.0) and labels it loosely. Wrong-ish,
  but at least self-consistent.
- **With talent:** The talent gives two incompatible instructions for the same column.
  Step 7's prose: "Express each stage's headroom as a share of the total baseline-to-ceiling
  gap, plus the residual" → denominator = gap = 0.27 → retrieval = **78%**, and the three
  shares sum to 123%. Step 7's worked table, header "Share of gap", rows `+0.23 → ~64%`,
  `+0.05 → ~14%`, `+0.08 → ~22%` → those are 0.23/0.36, 0.05/0.36, 0.08/0.36, i.e. shares of
  **Σ headroom (0.36)**, not of that table's gap (0.89 − 0.61 = 0.28); they sum to a tidy 100%
  only because of the wrong denominator. A share of the gap would be 82% / 18% / 29%. So an
  agent that follows the prose emits 78% and an agent that follows the worked table (tables
  anchor behavior more strongly than prose) emits 64% — under a column header that says "Share
  of gap" in both cases. The talent also promises "plus the residual" in that same sentence,
  and the example table has no residual row. Neither number is wrong arithmetic; the defect is
  that the talent specifies both and mislabels the one it demonstrates — producing exactly the
  quoted-out-of-context roadmap number the talent elsewhere works hard to prevent.
  **FAIL — skill-bug.** Not beaten by baseline in accuracy, but the talent adds a false
  authority the baseline's ad-hoc number does not claim.

## S11 — one broken run last night · negative-trigger
- **Input:** "Run #4417 of our RAG pipeline returned an empty answer at 02:14 last night. The
  other 3,000 runs that day were fine and this morning it doesn't reproduce. Find out why."
- **Pass criterion:** The agent does NOT start this method: no stage enumeration, no oracle
  definition, no eval set, no headroom table. It names `systematic-debugging` as the right
  route. Fail if it produces any part of the ablation apparatus, or if it routes to
  `error-analysis-taxonomy` (that is for classifying WHAT is wrong across many outputs, not
  root-causing one run).
- **Baseline:** A capable agent debugs the run — which is the correct behavior here. This
  scenario tests over-triggering, not capability: the risk is that a freshly loaded ablation
  talent turns a one-off incident into a week-long attribution study on an eval set that does
  not contain the failing input.
- **With talent:** "When NOT to use" states it twice — "One run failed and you want the cause
  of that run → `systematic-debugging`" — and the description's NOT-clause repeats it. The
  method also cannot apply: there is no aggregate metric over a fixed set here, only one row,
  so step 1 fails immediately and the talent declines rather than improvising.
  **PASS. Beats baseline.** (Correctly declines; no over-trigger.)

## Failure triage

**S10 → skill-bug** (not test-bug). The scenario is inside the talent's advertised scope — the
error budget is named in "When to use" ("You want an error budget ('42% of the loss enters at
stage 2') to defend a roadmap") and step 7 is dedicated to it. The criterion is observable
arithmetic, checkable by an outsider against the file. The defect is internal to SKILL.md: step
7's prose denominator (gap) and the worked table's denominator (Σ headroom) disagree, and the
table's header names the denominator it did not use. Fix the talent, not the test. Suggested
direction for the author (NOT applied by this tester): pick one denominator, state it in both
prose and header, show the residual row the prose promises, and — since shares of the gap do
not sum to 100% when headroom is non-additive — say so in the table caption rather than
choosing the denominator that makes it look tidy.

## Defects found in SKILL.md (reported, not repaired)

1. **Share-denominator contradiction (major, drives S10).** Step 7 prose says share of the
   baseline-to-ceiling gap; the step-7 table computes share of Σ headroom while labeling the
   column "Share of gap". Verified: 0.23/0.36 = 63.9% ≈ the table's "~64%"; 0.23/0.28 = 82.1%.
   Step 7's "plus the residual" is also absent from the example table.
2. **Metric direction never handled (minor).** Step 1 asks for the metric "and its direction",
   but `headroom(S) = score(oracle S) − baseline`, "A near-zero headroom", and `Σ headroom >
   gap` all assume higher-is-better. On a lower-is-better metric (error rate, RMSE, p95
   latency, cost per task) a literal read gives negative headroom and a ranking that puts the
   least promising stage on top. One sentence would close it.
3. **Residual formula assumes a 0–1 bounded metric (minor).** Step 6's `100% − ceiling` is
   undefined for unbounded metrics; the parenthetical `perfect − ceiling` gestures at the fix
   but "perfect" is never something step 1 requires the author to define.
4. **Two different worked datasets (cosmetic).** The step-7 table (0.61 → 0.89, three stages)
   and the Example section (0.61 → 0.89, two stages, Σ = 0.31) share a baseline and ceiling but
   not their stage numbers; readers will conflate them.

**Clean on the standing structural checks:** frontmatter has `name:` and `description:`; all
six cross-referenced talents exist under `.claude/skills/` (`measured-optimization-loop`,
`error-analysis-taxonomy`, `agent-architecture-audit`, `eval-harness`, `llm-eval-harness`,
`systematic-debugging`); no invented slash-commands or built-ins; the repo-specific material is
correctly quarantined under "In this repo (one instance)" with an explicit "Examples only"
disclaimer, so the method is portable; the paths it names (`pipeline/metrics.jsonl`,
`pipeline/ledgers/`) exist; the "no network calls, no CLI installs, no credentials" rule holds
throughout.

## Result summary
- Scenarios passed: 11/11 · failure_cause: none (S10 was a skill-bug, now fixed) · verdict: passed

## Triage record — S10 (why the verdict changed)
S10 first ran **FAIL**, triaged as **skill-bug**, not test-bug: the scenario was fair, the pass
criterion observable, and the defect reproduced arithmetically (0.23/0.28 = 82%, but the table
printed 64% = 0.23/0.36 under a header reading "Share of gap").

**The SKILL was changed, the test was not.** Step 7 now names its denominator in the column
header (`÷0.28`), prints 82% / 18% / 29%, adds the residual row the prose had promised, and
states that the shares summing to **129% is correct** — the tidy 100% was the symptom of
dividing by Σ headroom and hiding the very interaction step 8 insists on. A metric-direction
paragraph was added for lower-is-better metrics (defect 2 from the same audit).

S10 now passes on its ORIGINAL criterion: two teams following the talent reproduce the same
retrieval share, and the header matches the arithmetic. Weakening the scenario to make it pass
would have been the test-bug response to a real defect — the opposite of what triage is for.

**Still open (reported, not fixed):** the residual formula is now grounded in step 1's
"best attainable value", but step 1 does not yet *require* defining it — a talent-level
follow-up rather than a scenario failure. Cosmetic: the step-7 table and the Example section
share a baseline/ceiling but not their stage numbers (Σ 0.36 vs 0.31).
