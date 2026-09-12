# Threshold Evidence

Evidence gathered on two questions this skill has to answer for an arriving batch:
which differences must WIDEN the contract instead of blocking it, and what drift
threshold should be used to block one. Nine sources, thirteen claims bearing on
schema evolution, boundary anomalies, detection thresholds, and their relationship to
harm, and three unresolved contradictions. This file does not answer the threshold
question with a number. Section [The central finding](#the-central-finding) says why
no number is here for that question.

## Table of contents

- [The central finding](#the-central-finding)
- [Sources](#sources)
- [Claims](#claims)
  - [Is schema change normal, and what fires at the boundary?](#is-schema-change-normal-and-what-fires-at-the-boundary)
  - [Do default/automated tools over-alert or under-alert?](#do-defaultautomated-tools-over-alert-or-under-alert)
  - [How small a corruption is detectable?](#how-small-a-corruption-is-detectable)
  - [Is detected drift a usable proxy for harm?](#is-detected-drift-a-usable-proxy-for-harm)
  - [Are profile-derived constraints reliable as thresholds?](#are-profile-derived-constraints-reliable-as-thresholds)
- [Contradictions kept (unresolved)](#contradictions-kept-unresolved)

## The central finding

Across the nine sources gathered for this question, none publishes a mapping from
drift magnitude to expected harm — no source ties "the distribution moved by X" to
"the downstream cost was Y." What the sources do publish is evidence that a
detector's alert behavior is driven by sample size and by which statistical test is
used, largely independent of whether the underlying change matters (see
[How small a corruption is detectable?](#how-small-a-corruption-is-detectable)), and
at least one source's own measurement is that aggregate performance — the thing a
threshold is usually meant to protect — does not move in step with drift that is
present (see [Is detected drift a usable proxy for harm?](#is-detected-drift-a-usable-proxy-for-harm)).
This absence is recorded as the third row of
[Contradictions kept](#contradictions-kept-unresolved) and is the reason this file
carries claims, limits, and unresolved disagreements instead of a cutoff.

## Sources

Fetch date for every source below: **2026-09-02**.

### S1 — Data Validation for Machine Learning
Breck, Polyzotis, Roy, Whang, Zinkevich, 2019. Paper (MLSys). Read in full: PDF
downloaded and text-extracted locally, cross-checked with a second extractor.
**Expiry condition:** untrue if a later measurement over the same or a larger Google
pipeline population revises the schema-revision counts, the anomaly-category
fix rates, or the chi-square false-alarm demonstration reported here, or if TFDV's
default statistics/tests change from what is described.

### S2 — Auto-Validate by-History
Tu, He, Cui, Ge, Zhang, Shi, Zhang, Chaudhuri, 2023. Paper (arXiv). Read in full.
**Expiry condition:** untrue if Deequ or TFDV change their default configuration
(JS-Divergence, L-infinity) away from what this evaluation measured, or if a later
benchmark against a different or larger incident set reports different
precision/recall for the same tools in default configuration.

### S3 — Automating Data Quality Validation for Dynamic Data Ingestion
Redyuk, Kaoudi, Markl, Schelter, 2021. Paper (EDBT). Read in full.
**Expiry condition:** untrue if the hand-tuned Deequ ROC AUC figures are revised in a
later version of this work, or if a later evaluation removes the ground-truth-visibility
advantage given to the hand-tuned arm and the gap to automated methods changes.

### S4 — Moving Fast With Broken Data
Shankar, Fawaz, Gyllstrom, Parameswaran (Meta / UC Berkeley), 2023. Paper (arXiv).
Read in full. **Expiry condition:** untrue if the 30%-null-fraction abandonment
anecdote is quantified in a later revision of this work, or if the described
tens-of-thousands-of-columns scale is no longer representative of the pipelines this
skill is applied to.

### S5 — Automating Large-Scale Data Quality Verification
Schelter et al., 2018. Paper (VLDB). Read in full.
**Expiry condition:** untrue if a later Deequ release changes the constraint-suggestion
algorithm from what Table 3 measured, so that the 63.6%-coverage result no longer
reflects current Deequ behavior.

### S6 — Empirical data drift detection experiments on real-world medical imaging data
Authors not recorded by the gatherer, 2024. Paper (Nature Communications). Read in
full (HTML). **Expiry condition:** untrue if a later study on a different modality or
dataset finds aggregate performance IS a reliable drift indicator, narrowing this
result to the specific imaging/COVID-19 case studied here.

### S7 — Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift
Rabanser, Gunnemann, Lipton, 2019. Paper (arXiv). Read in full.
**Expiry condition:** untrue if a later evaluation extends the same shift-detection
tests to tabular, schema, or categorical drift and finds the 10%-undetectable result
does not hold outside the image-classification benchmarks used here.

### S8 — Which test is the best? We compared 5 methods to detect data drift on large datasets
Evidently AI, 2023. **VENDOR ENGINEERING POST** — the post argues for the author's own
product's defaults; the measurements may be sound but the framing is not neutral.
Read in full (HTML). **Expiry condition:** untrue if Evidently AI revises its
recommended sample-size cutoff for the KS test, or if an independent (non-vendor)
replication contradicts the sample-size-driven alert behavior reported here.

### S9 — How to create and edit Expectations with the User Configurable Profiler
Great Expectations, 2022. **VENDOR DOCUMENTATION** — a stated design property, not an
experiment. Read in full (HTML, after a summariser had paraphrased the passage — the
raw HTML was read to correct for that). **Expiry condition:** untrue if a Great
Expectations release changes the User Configurable Profiler's default suite-generation
behavior away from the deliberately-over-fitted min/max shown here; this is legacy
documentation for 0.14.13.

## Claims

Each claim below carries its source, its verbatim quote, what was measured, the
effect size as reported, the sample, its limits, and its verdict (MEASURED = the
source ran or reports an experiment; REPEATED = the source states it without
quantifying it).

### Is schema change normal, and what fires at the boundary?

The threshold sections below assume a difference has already been sorted into "block"
or "widen." These four claims, all from S1, are the evidence a split is possible at
all: schema change is not an anomaly to eliminate, boundary anomalies are dominated by
a specific, recognizable set of structural surprises, a boundary check pays for itself
against diagnosing a silent failure downstream, and a schema-only check still misses a
defect class that only shows up against the training code.

**C1 — S1 — MEASURED.** Schema change is the normal state of a production feed, not an incident.
> "The graph illustrates that the schema evolves in most of the examined pipelines, in line with our hypothesis of data-schema co-evolution. The majority of cases have up to five schema revisions, with the distribution tapering off after that point."
What was measured: number of manual schema revisions per pipeline. Effect size: most
pipelines revised, majority up to five. Sample: more than 700 Google ML pipelines
already using data validation. Limits: counts manual edits by pipeline owners, not
producer changes directly, and the histogram is not given as numbers — "most" and "up
to five" are the authors' reading of their own figure; the population is self-selected
for teams already validating; this conflates "the data legitimately changed" with "the
initial inference was wrong."

**C2 — S1 — MEASURED.** Ingest-boundary anomalies are dominated by structural surprises.
> "As shown, the most common anomalies are new feature columns, unexpected string values, and missing feature columns. The first two are unsurprising: even in a healthy pipeline, there will be new values for fields such as "postal code", and new feature columns are constantly being created by feature engineers. Missing features and missing data are more cause for concern."
What was measured: share of pipelines on which each anomaly category fired in 30 days,
and the share of firings subsequently fixed. Effect size: fixed-given-fired ranges 28
to 100 percent by category; new feature column 65, out-of-domain values 66, missing
column 53. Sample: one month of production telemetry across the same pipeline
population. Limits: "not fixed" is not "false alarm" — the paper's own explanations
are a batch sliding out of the rolling window, and an on-call missing the alert; the
fixed measurement is heuristic and the paper says it "can miss some fixes"; table
values transcribed from a PDF table, not quoted.

**C4 — S1 — MEASURED.** Boundary validation collapsed diagnosis time on one production incident.
> "The total time to diagnose and fix the problem was two days, whereas similar issues have taken months to resolve."
What was measured: wall-clock time to diagnose and fix one incident. Effect size: two
days against an unquantified "months." Sample: one incident, n=1. Limits: a single
case study reported by the team that built the tool, with an uncontrolled comparison —
"months" is a recollection of unspecified issues, not a matched baseline; it measures
time-to-diagnose, not time-to-detect: how long the silent drop ran before validation
was switched on is not stated.

**C5 — S1 — MEASURED.** Unit-testing the training code against the schema catches a defect class the data alone cannot show.
> "Specifically, more than 70% of pipelines had at least one model unit test defined. Based on analysis of test logs over a period of one month, we determined that these tests were executed more than 80K times (including runs executed as part of continuous test framework). Of all of these executions 6% had failures indicating that either the training code had incorrect assumptions about the data or the schema itself was under specified."
What was measured: adoption and failure rate of schema-driven fuzz tests over the
training code. Effect size: 6 percent of 80K+ executions failed. Sample: one month
across the same pipeline population. Limits: 6 percent is a rate over executions, not
distinct defects — repeated runs of one unfixed defect inflate it, and CI reruns are
included; it is ambiguous by construction between a wrong code assumption and an
under-specified schema; adoption is confounded by the test shipping in standard
templates; the authors call the method "obviously not fool-proof."

### Do default/automated tools over-alert or under-alert?

**C8 — S2 — MEASURED.** High precision, low recall from static default configuration.
> "Commercial data-validation solutions like Amazon Deequ and Google TFDV have high precision but low recall, because they use predefined and static configurations (e.g., JS-Divergence and L-infinity are the default for TFDV), which lack the ability adapt to different pipelines, and thus the low recall."
What was measured: precision/recall of default-configured validation tools against
production column histories. Effect size: reported only as plot positions; "high" and
"low" are the authors' words. Sample: 2000 Microsoft production pipelines. Limits: run
in DEFAULT configuration only, so this measures out-of-the-box behavior, not the
frameworks' ceiling; recall was measured against substitute columns and synthetic
issue types, not logged incidents, because the authors say few documented incidents
exist to test against; this is a competing method's paper reporting on its rivals.

**C9 — S3 — MEASURED.** Automated configurations false-alarm in the majority of cases;
hand-tuned reaches near-ceiling ROC AUC.
> "The results indicate that our approach outperforms other automated baseline solutions and reaches the predictive performance of hand-tuned baselines (ROC AUC score of 95%, whereas the hand-tuned Deequ solution reaches 100% and 92% on the Flights and FBPosts datasets, respectively). Other automated solutions tend to produce false alarms in the majority of cases."
What was measured: ROC AUC of automated and hand-tuned validation configurations.
Effect size: hand-tuned Deequ 100% and 92%; the authors' own method 95%. Sample: two
labelled datasets with hand-labelled dirty counterparts. Limits: positive base rate is
50% by construction, far above production where corrupted batches are rare, inflating
apparent precision for every method; the hand-tuned arm was tuned WITH sight of the
ground-truth clean data, an optimistic bias the authors state directly; the automated
arms were frozen after inference and never revised. **DIRECTLY CONTRADICTS C8** — see
[Contradictions kept](#contradictions-kept-unresolved).

**C10 — S4 — REPEATED.** A single hand-set null-fraction threshold produced enough
false positives that engineers silenced, then abandoned it.
> "However, this method produced too many false positive alerts, and ML engineers thus silenced them. Some ML engineers discovered an increase in precision when manually tuning the threshold, but this approach required significant effort. Eventually, ML engineers abandoned this data validation method."
What was measured: not quantified in the source. Effect size: not quantified. Sample:
not quantified — a narrative from the authors' own organization. Limits: the
false-positive volume is never given a number and "abandoned" is a recollection, not a
measurement; the mechanism behind it IS quantified elsewhere in the same paper — with
more than 10,000 features, most had at least one anomalous statistic — so this is
scoped to feature tables with tens of thousands of columns, not a small ingest table.

**C13 — S8 — MEASURED — VENDOR EXPERIMENT.** The KS test's alert behavior tracks
sample size more than severity.
> "It raises flags even for a minor change of 0.5%, as soon as we have more than 100,000 objects in a dataset."
What was measured: share of runs in which the test reported drift, by sample size and
injected shift. Effect size: 0.5% shift flagged above roughly 100,000 observations.
Sample: sizes swept 1,000 to 1,000,000, 100 repetitions per configuration, alpha=0.05.
Limits: argues for the vendor's own product defaults; this is a small REAL shift being
flagged, not a null-true false positive — the complaint is that the alert is not
actionable at that volume; the vendor's own recommendation is to use KS under roughly
1,000 observations.

### How small a corruption is detectable?

**C3 — S1 — MEASURED.** A goodness-of-fit test false-alarmed on a small perturbation
at production volume.
> "As shown, this method would needlessly fire an alert 7 out of 10 times and would most likely be considered a flaky detection method."
What was measured: alert rate of a chi-square goodness-of-fit test under a
deliberately negligible perturbation. Effect size: 7 of 10 trials fired. Sample: 100M
points from N(0,1), 10k replaced from N(0,2), alpha=0.01, 10 trials. Limits: n=10, one
synthetic setup, one test, one batch size — a point estimate with a wide interval, not
a calibrated false-positive rate; that the injected 0.01% is harmless is asserted, not
shown; the authors report repeating on real product data with "qualitatively the same
results" but give no numbers, and this does not establish their replacement metric has
a lower false-alarm rate.

**C11 — S7 — MEASURED.** Corruption confined to a minority of rows is near-blind to
distribution-shift monitors; the same corruption at majority scale is not.
> "Moreover, the results in Table 2b show that while target data exhibiting only 10% anomalous samples are hard to detect, suggesting that this setting might be better addressed via outlier detection, perturbation percentages 50% and 100% can already be detected with better than chance accuracy using 50 samples."
What was measured: shift-detection accuracy as a function of the fraction of
perturbed samples. Effect size: 10% hard to detect; 50% and 100% detectable above
chance at n=50. Sample: image benchmarks with synthetic perturbations, 5 random
splits, alpha=0.05. Limits: image classification only — does NOT cover tabular
ingest, schema changes, null-rate spikes, unit changes, or categorical drift, which
are the failure modes an ingest contract mostly guards; the figures are detection
accuracy over a shift battery, not a per-detector false-negative rate on a real
pipeline.

See also C13 above (S8): the same detector class flags a 0.5% shift once sample size
exceeds ~100,000. Read together with C3 and C11, alert behavior in these three sources
is explained by sample size and test choice at least as much as by how much the data
actually moved — see [Contradiction 2](#contradictions-kept-unresolved).

### Is detected drift a usable proxy for harm?

**C12 — S6 — MEASURED.** Aggregate model performance did not move under real and
synthetic drift.
> "This lends credence to our observation that aggregate model performance is not a reliable indicator of data drift (despite widespread use)."
What was measured: movement of aggregate performance metrics under known input drift.
Effect size: triple-aggregated metrics did not move; per-class metrics were more
sensitive but the authors describe them as noisy. Sample: chest X-ray classifiers;
COVID-19 emergence plus synthetic shifts. Limits: says nothing about whether the
undetected drift was harmful — only that performance metrics did not reveal it; one
modality only.

### Are profile-derived constraints reliable as thresholds?

**C6 — S5 — MEASURED.** Constraints auto-suggested from a sample did not all hold on
the held-out remainder.
> "However, the system also suggests two constraints which do not hold for the data."
What was measured: coverage on held-out data of constraints derived from a sample
profile. Effect size: isInRange on "lang" covers 0.991; isUnique on "statuses count"
covers 0.636; on a second, structurally simpler dataset every suggested constraint
covered 1.0. Sample: two datasets, one split each. Limits: the failure rate is a
property of the data's messiness as much as of the method; the authors frame
suggestion as human-in-the-loop and say suggestions "might not necessarily hold for
future data."

**C7 — S9 — REPEATED — VENDOR DOCUMENTATION.** Profiler-generated expectations are
deliberately over-fitted to the sample by design.
> "These Expectations are deliberately over-fitted on your data e.g. if your table has 10,000 rows, the Profiler will produce an Expectation with the following config:"
What was measured: not applicable — a stated design property, not an experiment.
Effect size: not applicable. Sample: not applicable. Limits: documents one legacy
suite-generation path in one tool, not every Great Expectations path and not an
experiment; the same source page continues that the resulting suite "is not
specifically intended to be used as is."

## Contradictions kept (unresolved)

Three disagreements found across these sources are kept unresolved rather than
adjudicated. Each bounds what any threshold advice can claim; none is resolved here.

### 1. Do default-configured validation tools over-alert or under-alert?
- **a (C9):** automated Deequ and TFDV "produce false alarms in the majority of
  cases" on a balanced benchmark.
- **b (C8):** the same two tools show "high precision but low recall" across 2000
  production pipelines.
- **Status: NOT RESOLVED.** Opposite verdicts on the same tools. The likely split is
  base rate — a balanced clean/corrupted benchmark against production batches that
  are almost all clean — and whether the derived suite is ever revised. A skill
  citing only one gives exactly the wrong advice in the other regime.

### 2. How small a corruption is detectable?
- **a (C3):** a 0.01% perturbation over-detected, firing 7 of 10 times at n=100M.
- **b (C11):** a 10% perturbation largely undetected by two-sample tests.
- **Status: NOT RESOLVED.** Sensitivity is dominated by sample size and the
  statistic, not by how damaging the corruption is. The consequence is that "will my
  monitor fire" is a poor proxy for "is this batch bad" in both directions.

### 3. Is detected drift a usable proxy for harm?
- **a (C12):** aggregate performance failed to move under real drift, so drift
  detection is the only available signal when labels are absent.
- **b (C13 and the gatherer's own finding):** no primary source publishes a mapping
  from drift magnitude to expected performance loss.
- **Status: NOT RESOLVED, and it bounds this file.** "Is this drift worth blocking"
  has no answer independent of whether a performance signal exists. Nobody in these
  nine sources publishes drift-magnitude-to-harm, which is exactly what a blocking
  decision needs.
