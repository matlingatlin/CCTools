---
name: eval-set-curation
description: "Use when production data already exists in volume and the question is WHICH of it becomes the eval set - logged traces, queries, tickets, documents, transactions. Covers near-duplicate and templated family collapse, a per-slice reporting floor, and a sealed holdout with a look log. Triggers on 'we have 40k logs, which 200 do I evaluate on', 'is my eval set representative', 'dedupe the eval set', 'near-duplicate test cases', 'effective N', 'how many examples per slice', 'minimum sample size per segment', 'what error bar can I live with per slice', 'test-set contamination', 'frozen holdout', 'per-slice accuracy'. NOT for manufacturing inputs when there is no production data yet (synthetic-eval-data-generation), scoring or CI-gating a set that already exists (eval-harness, llm-eval-harness), a high score you suspect is the SCORER not the set (llm-judge-calibration), or clustering traces to find WHAT is going wrong rather than which ones to keep (error-analysis-taxonomy)."
---

# Eval Set Curation

Three checks on an eval set drawn from data you already have, and the record they fill in. The
population is real traffic — logged traces, queries, tickets, documents, transactions — and this
method does not run the whole selection: it runs the three parts of it that a competent analysis
gets wrong. What you get out is a filled `assets/eval-set-record.md` carrying **two** de-duplication
counts rather than one, a per-slice reporting floor derived from a tolerance somebody owns, and a
holdout that is either sealed with a look log or marked UNSEALED.

## When to use

- You are selecting a fixed evaluation subset from production history, and want the three parts of
  that job that go wrong checked.
- You have a candidate set already and need to know whether a templated family or a paraphrase
  cluster is inflating it — whether its effective N is the N you think it is.
- Someone has asked how many examples a slice needs before its score can be quoted, and the answer
  so far is a round number nobody can source.
- You have a pool of unused rows that people call the holdout, and nobody can say what seals it.
- Your holdout *is* sealed and you have to decide how often it may be opened, with no evidence-based
  number available to point at.

**Not this:** there is no production data yet (`synthetic-eval-data-generation`); the set exists and
needs scoring or wiring into CI (`eval-harness` for an agent's own task completion,
`llm-eval-harness` for a shipped app's CI gate); you have failure traces and need them categorised
(`error-analysis-taxonomy`); **the set looks fine and you suspect the SCORER instead** — a set that
scores high while users complain is as often a miscalibrated judge as a badly chosen set, and that
is `llm-judge-calibration`; **two teams cannot agree on the tolerance itself** rather than on the
floor that follows from it, which is `preregistered-decision-rule`.

## Important — what this is for, and what it deliberately leaves out

This method was rebuilt against four measured baseline runs on the same task. Those runs, with no
method loaded at all, **already did** the following, every time, unprompted:

- computed the population count and accuracy per slice, and refused to report the pooled number;
- found every contaminated row, quantified the inflation, and removed rather than down-weighted;
- said in their own words that the rare slice could not be measured at its n;
- stratified with deliberate over-sampling of the rare slices and priced the trade-off.

**None of that is taught here**, because teaching it costs context on every invocation and buys a
behaviour that is already reliable. Do those four things; they are the floor, not the method.

Three things the same runs got wrong, and those are the three steps below. On two of them the runs
disagreed **with each other on identical input**, which is the shape this method exists to fix: the
good answer is available, it is just not the reliable one.

## Steps

### 1. Collapse to clusters, not to distinct strings

Exact-match dedup produces a *distinct-string* count. That is not the number you want. A templated
family — one intent, filled with ten product names — survives exact dedup completely, and every
member of it votes.

Three of four baseline runs removed the exact repeats, reported the remainder as clean, and left a
six-intent family standing as sixty rows.

1. Normalise first — case, whitespace, IDs, timestamps, and **only slots you can enumerate before
   looking at the clusters** (an order number, a date, a customer name). Exact-match on the
   normalised text. That is the *distinct-string* count. **Write down what you normalised.** If you
   normalise the varying slot of a templated family here, the family collapses in step 1 and step 4's
   two numbers come out equal and clean while the family is still standing — the normalisation list is what
   lets someone else see that happened.
2. Then cluster on similarity. Take a sample of ~50 pairs spanning the score range, label each
   yourself as same-intent or not, and set the threshold where your labels flip. Record the pairs
   you looked at. **If your labels do not flip cleanly** — same-intent and not-same-intent
   interleave across a wide band — there is no single threshold and saying so is the finding. (C6
   establishes the weaker, related point that one threshold does not transfer across domains: at 0.8
   one MMLU subject is caught and another missed, at 0.4 the first floods with false positives. It
   does not establish that your own hand-labelled pairs will interleave; this clause stands on the
   fallback, not on the citation.) Report the band, collapse only inside its confident end, and
   hand the interleaved pairs to a person.
3. Keep one representative per cluster and **record the cluster size**. A cluster of forty
   paraphrases is one observation, not forty.
4. Report **two numbers, separately**: distinct strings after step 1, distinct clusters after step
   2, **and the normalisation list from step 1 beside them**. If the two numbers are equal, that
   claim is read against the list: equal numbers after normalising a template slot is not the same
   finding as equal numbers after normalising whitespace.

**State what your detector cannot see.** In one measured comparison a 10-gram overlap detector
scored 0.926, 1 and 0.816 on the three verbatim conditions and **0 on all six rephrased ones**;
two embedding detectors spanned the whole range from 0 to 1 across the same cells
(`references/selection-evidence.md`, C6). So write down the paraphrase class you are not catching
rather than implying you caught it. MinHash itself was **not** evaluated in that experiment; do not
claim it was.

**Why the evidence page does not settle this step, and what does.** No claim in the evidence bundled
here measures within-set near-duplicate over-weighting. C4 and C5 measure *train-to-eval leakage*,
which is a different mechanism and one the baseline already handles. The argument for this step is
arithmetic, not empirical: a cluster of forty identical-intent rows contributes forty votes to a
mean that should have received one. It needs no citation and it does not have one.

### 2. Derive the floor from a tolerance you name first

Every baseline run computed the per-slice confidence interval correctly. Three then set the
reporting floor with a round number of their own invention — **30**, **200** and **350**, three
different floors from identical data, each stated as though established.

The arithmetic is not the gap, and a "source" column is not enough either: an interval reports the
width **at** an n, it does not select one. What turns evidence into a cut is a tolerance, and the
tolerance has to be named before the number.

1. **Name the decision the floor gates, and the action on each side of it.** "Below the floor we
   do not block a release on this slice; above it we do." This is the part someone else can check
   against what you actually did, and it is what makes the next clause a decision rather than a
   preference.
2. **Name what the number has to do**, in one of two forms, written down before computing
   anything: the largest half-width you can act on ("I will not act on a slice score I can only
   locate to within 10 points"), or the difference the gate must detect ("this must catch a
   10-point regression between releases, at 80% power").
3. **Invert it, and name the inputs the inversion needs.** A half-width depends on the accuracy p
   as well as on n, so state which p you inverted at and why — the slice's current estimate, a
   worst-case p=0.5, or a target. A power calculation needs a variance assumption, so state it and
   where it came from. Two people who agree on a 10-point tolerance and disagree on p get
   materially different floors, and that disagreement should be visible as a disagreement about p.
4. **Fix p at the same time as the tolerance**, or record that p was chosen after scoring and from
   which score. Two floors can differ on nothing but when p was read, and without this both look
   compliant.
5. **Say who owns the tolerance and when it was fixed.** If that is one person, it is one name —
   what matters is that the tolerance was written down before the first score, not that a committee
   met. A tolerance chosen after seeing the scores is the same failure one level up, and saying so
   is better than pretending otherwise.

The anchors you may cite, with what they do not establish, are in
`references/selection-evidence.md`: measured 95% CI half-widths across nine benchmarks, the widest
of them **8.30 accuracy points at n=100** (C1) — with no row at the sizes teams actually pick, so
yours has to be computed rather than read off, and with **no cluster adjustment**, so those figures
are narrowest-case and not a conservative ceiling. If your examples arrive in groups — several turns
per user, several tickets per customer — the true interval is wider than anything on that table by
an amount **nothing in this bundle measures for production logs**. The one claim that sizes the
effect at all does so on public evals and says in its own limits that it is not established for
production data, so it is on the evidence page and no step cites it: read it if you want the order
of magnitude, and do not carry its numbers into your own record as a multiplier. And the
widely-quoted **floor of roughly 1,000
questions** (C3), which is **DERIVED** from variance parameters its own author calls fictional in
the same sentence. It may inform a default. It may not be cited as evidence that 1,000 holds, and
it is not a substitute for clause 1 above.

**What this step closes, and what it does not.** It does not make two teams agree. A team that can
act on a 5-point half-width and a team that can act on 18 will derive floors three-fold apart from
identical data, and both will have followed every clause — that divergence is legitimate, because the
floor is a consequence of what each team can act on. **That is not the divergence that was
observed.** The observed case was one task, one dataset, four runs, and floors of 30, 200 and 350
with no tolerance stated at all and no differing action threshold behind them — divergence with
nothing underneath it. This step is claimed to close that kind and only that kind: it removes the
floor stated in the analyst's own voice as though it were established. If two teams need to
converge, the tolerance is the thing to negotiate, and that negotiation belongs in `preregistered-decision-rule`, not here.

### 3. Seal the holdout, or do not call it one

A pool of unused rows that "can also be used as a dev set" is not a holdout. Three of four baseline
runs produced exactly that and named it a holdout.

1. Split dev and holdout. Dev is worked against freely — that is its job.
2. **Seal the holdout**: stored separately, never read example by example, never used to choose
   between variants, opened only to confirm a decision already made on dev. Write down what
   enforces that, not what you intend.
3. **Log every look** — date, who, reason, and the decision it confirmed. This is the half that
   fixes the failure: an empty log under a stated seal means no look yet; an empty log with nothing
   sealing it means there is no holdout, and the record says so instead of implying otherwise.
4. **A look budget is a policy, and it is written down as one.** There is no evidence-based number
   here and this method does not invent one. The strongest result on holdout reuse is a synthetic
   worst case that explicitly gives no safe reuse count (`references/selection-evidence.md`, C10).
   The two results on the other side differ from each other and neither transfers cleanly: C12 found
   little to no adaptive overfitting across 120 Kaggle competitions, on a platform that rate-limits
   submissions and never reveals the private split — a protection an internal set scored on every
   commit does not have; C11 found the opposite of overfitting over a decade of competitive
   CIFAR/ImageNet reuse, and says in the same section that a uniform constant drop is **not**
   excluded. Nothing in the bundle says whether that reuse was rate-limited; do not assume either
   way from the C12 contrast. Read section 4 of the evidence page, name whoever owns the choice,
   and record the number as a policy rather than as a finding.

## The order these run in, because every ordering changes the numbers

The three steps are not independent and this is the one thing a cold reader cannot work out from
them. **Contamination removal, then step 1, then step 2, then step 3.**

- **Contamination first.** It is not taught here (see Important, above) but it must happen before
  step 1, or you cluster rows you are about to delete and the cluster sizes are wrong.
- **Step 1 before step 2.** Collapsing clusters shrinks every slice, so a floor derived first is a
  floor derived against an n that no longer exists. The two steps genuinely fight: aggressive
  collapse is the correct answer to step 1 and directly shrinks the n step 2's floor gates. **Step 1
  wins, and step 2 is re-derived on the collapsed set.** Record both n's — pre-collapse and
  post-collapse — because the difference is the finding, not an accounting detail.
- **Step 2 before step 3.** Splitting a slice into dev and holdout halves its n, so a slice that
  clears its floor whole may not clear it split. Derive the floor first, then decide whether the
  slice can afford a holdout at all.
- **Reweighting comes last, and against the ORIGINAL population shares.** Collapse changes the
  set's composition; it does not change what production sends you.

## Output

Fill in `assets/eval-set-record.md`. Sections 3, 5 and 6 there are the enforced ones and carry stop
clauses, one per step above; the fields are chosen so that skipping a step leaves a visible empty
entry rather than an unremarkable silence — the two-number near-duplicate row, the *tolerance*
column that a floor with no origin cannot be written into, and the look log under a Sealed field.

## Rules

- **Report the two dedup numbers separately.** Distinct strings is not distinct clusters.
- **Every floor is the output of a named tolerance.** A number that appears nowhere else is an
  invention with a table around it, and a citation is not a tolerance.
- **A DERIVED figure informs a default and never proves one.** If you cite the ~1,000-question
  floor, cite the sentence saying its parameters are fictional too.
- **A sealed holdout is a mechanism, not an intention.** If nothing enforces it, write UNSEALED.
- Method only: no external CLI installs, no credentials, no network calls beyond the data store you
  already have.

## Common mistakes

| Mistake | What it costs |
| --- | --- |
| Dedup to distinct strings and call it deduplicated | A templated family votes as many; effective N is a fiction |
| A floor with a source but no tolerance | A citation is not a decision; nothing says what the floor gates |
| "Held-out pool, also usable as a dev set" | There is no honest final number left and nobody notices |
| Citing the ~1,000-question floor as a finding | It is DERIVED from parameters its author calls fictional |
| A look budget presented as an evidence-based number | The evidence gives no safe reuse count; the budget is a policy |

## Related

`synthetic-eval-data-generation` fills the cells this method finds empty. `eval-harness` and
`llm-eval-harness` consume the curated set and score it. `error-analysis-taxonomy` categorises
failures across the sampled examples. `llm-judge-calibration` validates the scorer — go there
first if you suspect the number rather than the set. `abstention-threshold-design` sets a decline
cut once the set exists. `preregistered-decision-rule` fixes the threshold this set will be judged
against, which is also where step 2's tolerance belongs if the decision is contested.

## In this repo (one instance)

Applied here, the population is the run history in `pipeline/ledgers/` and the `metrics.jsonl`
rows; the slices are talent type x scenario kind (representative / adversarial /
negative-trigger); and the curated result is what a talent's `evals.md` scenarios are drawn from.
That is an example of applying the method, not part of it.
