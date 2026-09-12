# Phase 2.2 — what the baseline runs actually did

Six runs so far, no skill present, fresh session each, clean cwd, fixture handed in by
path. Two more (E1 rep 2, E2 reps 1-2) still in flight; this file is appended to, never
rewritten.

## The classification: the baseline is CLEAN, not failing

`skill-measure`: *baseline passes cleanly -> it must win on a NAMED axis and not
regress, at least 2 runs.* That is this build's obligation. It is the harder bar, not
the easier one.

The package's `expected_failure` predicted the baseline would "compare whole-column
statistics and report the loudest distribution change, so it flags the benign
channel-mix shift and misses the unit change confined to one merchant." **REFUTED, in
every run that touched it.** This project's expected_failure has now been refuted 5 of
5, and again for the same stated reason: it was written from the solution's point of
view.

- E4 rep 1: *"only see it after grouping by `merchant`"* — found D1 unprompted.
- E4 rep 2: *"A per-merchant p99 or max check against a rolling baseline would have caught both on day one where the global stats didn't."*
- E1 rep 1: *"Profiling each metric *within* segments did ... The dimension where a break is *confined* is the one naming its cause."*
- E3 rep 1 on the benign channel shift: *"At PSI 0.06 it sits *below* a 0.1 warn line"* — it did not flag it as a defect.

Segmented reasoning is not the gap. It arrives without being asked for.

## OBS-1 — the threshold question is answered with an invented number. BOTH reps.

The package's single most useful finding is negative: no primary source publishes a
mapping from drift magnitude to expected harm (`contradictions_kept[2]`). Asked "what
threshold should we use", both baseline runs supplied one anyway and dressed it as
standard practice.

- **E3 rep 1**, first line under "Short answer": *"Use **PSI with the standard bands — warn at 0.1, page at 0.25** — computed per column, not on the file as a whole."*
- **E3 rep 2**, closing: *"If you want the number you asked for: **PSI 0.25**, applied per column"*, and earlier *"Conventional bands: PSI < 0.1 no action, 0.1–0.25 investigate, > 0.25 alert."*

Rep 1 does add a caveat — *"0.1/0.25 are convention, not derived from your data"* — but
it arrives after the headline number, and its remedy is a VARIANCE argument (*"run it in
shadow mode ... set the line above observed quiet-period variance"*), not a harm
argument. Neither run says the mapping from magnitude to harm does not exist in any
source. Neither says what the threshold depends on that the data cannot supply.

**Consequence.** The person leaves with 0.1/0.25 and a false belief that it is
principled. C10 in the claim set is the same story ending badly at Meta: a single
hand-set threshold produced so many false positives that engineers silenced the alert.
C3, C11 and C13 together say sensitivity is governed by sample size and the statistic,
not by how damaging the corruption is — so the number transfers to nothing.

**Every run did it, not some.** 2 of 2.

## OBS-2 — the block/widen SPLIT is not made as a decision. Rep 1 of E1.

The fixture's whole point is that three differences must block and three must widen the
contract. E1 rep 1 identified all six correctly on the facts and then did not split
them:

- Verdict: *"Quarantine it. Every row is hit by at least one break"* — a whole-batch
  refusal.
- On the two benign category additions: *"**Two closed domains opened.** `merchant` +=
  `harborview` (240 rows, PSI 0.667), `status` += `chargeback` (90 rows, PSI 0.226). Not
  defects, but they break enum joins."* Filed under the "22 FAIL" count, and the reader
  is not told which of the six are contract-widening events and which are producer
  breaks.
- E3 rep 1 reaches the right frame only as an afterthought, at the very end:
  *"`harborview` and `chargeback` are probably intended changes. Reference needs to be
  updated to include them, otherwise you're calibrating a threshold against a baseline
  you already know is stale."*

**Consequence.** A suite built from that answer refuses the onboarding batch. The
fixture's own note: *"A contract that blocks all six has not solved the problem, it has
moved it."*

**Strength of the observation: 1 of 1 so far on E1.** E1 rep 2 and both E2 runs are
still in flight and will settle whether this is systematic or a draw. Marked provisional
until they land.

## OBS-3 — a fixture wrinkle, found by the runs, not by us

Every E4 run reports that `harborview` ALSO carries the cents bug (~38 of 240 rows).
`ground_truth.json` does not: D1 is belltower-only and harborview is B1, benign. The
data supports the runs: whole-number `amount` rates are belltower 440/440, harborview
38/240 (15.8%), every other merchant 2-7 of ~470 (0.4-1.5%). So harborview's elevated
whole-number rate is real in the CSV and is almost certainly a generator artefact rather
than a planted defect. Recorded, and carried to `not_checked`: an expectation keyed on
"names belltower and only belltower" would punish a correct reading of the data.

---

# APPENDED after the contamination re-run (see the `harness_defect` event)

The four second-rep runs above were discarded: they executed in a working directory
holding another run's `contract.py`, `contract.json`, `feed_profile.json` and
`report.html`, and one of them read them. Re-run with a per-run isolated cwd. Everything
below is from the isolated runs. Wave 1 (E1/E3/E4 rep 1) is kept — see the event for why.

## OBS-1 CONFIRMED, and it is wider than the threshold question. 4 of 4 isolated runs.

Asked what threshold to use, and asked to write assertions, the baseline supplies numeric
bands it cannot derive and presents them as engineering practice.

- **E3 rep 2 (isolated)**: *"PSI on the parsed, validated data ... Warn at **0.10**, alert at **0.25**"*, plus *"Unparseable rate per column > 0.5%"*, *"Null rate exceeding reference by >2pp absolute *or* 3× relative"*, *"Values outside reference [min, max] > 1% of rows"*, *"Unseen categorical level > 0.5% of rows"*.
- **E3 rep 1**: *"Use **PSI with the standard bands — warn at 0.1, page at 0.25**"*.
- **E2 rep 1 (isolated)**: *"mean ±25%, median ±20%, p99 ±40% (ERROR)"*, *"Row count vs reference ±50%"*, *"NULL rate ≤3%"*, *"tolerance max(3pp, 4σ binomial)"*.

E3 rep 2 does try to justify one of its numbers: *"the other seven merchants sit between
0.014 and 0.052, which is your real noise floor and is what justifies 0.10 as a warn
line."* That is a VARIANCE argument. It says the number sits above the quiet-period
spread. It does not say the batches above the line are the harmful ones, and nothing in
the file lets it. The claim set says why no such argument is available: C3 (a 0.01
percent perturbation fired 7 of 10 times at n=100M), C11 (a 10 percent perturbation
largely undetected), C13 (the KS test flags a 0.5 percent shift once n exceeds ~100,000)
— sensitivity is governed by sample size and the statistic, not by how damaging the
corruption is. C10 is where it ends: one hand-set non-null-fraction threshold produced so
many false positives at Meta that engineers silenced the alert.

E2 rep 1 is the honest version of the same failure and shows what "good" looks like from
the baseline's own mouth: *"`AMOUNT_HARD_MAX = 2000` is the one threshold not derived
from the data. It's a placeholder at ~3.5× the reference max and needs a business owner's
sign-off."* It flags ONE of its numbers and lets seven others through unflagged.

**Nothing in any of the eight runs says the mapping from drift magnitude to harm does not
exist in the literature.** That is the sentence the skill has to carry.

## OBS-2 DOWNGRADED to UNEVEN, not failing. 1 of 2.

E1 rep 2 (isolated) makes the split cleanly and unprompted: *"Findings 1–3 are defects to
fix before this batch is used ... Findings 4–5 are changes to ratify, not bugs."* E1 rep
1 did not: it filed the two benign category additions inside a "22 FAIL" count and
verdicted *"Quarantine it."*

So the split is a behaviour the baseline HAS and does not reliably reach. Per
`skill-measure`, an uneven baseline needs the artefact to make the outcome CONSISTENT,
and needs at least two runs to see it at all. This is the second axis, and it is a
consistency claim, not a capability claim.

## OBS-3 CONFIRMED and it is a fixture defect, not a run defect. 3 of 3.

Every isolated E4/E1/E3 run reports harborview also carrying cents rows (35-38 of 240).
`ground_truth.json` calls harborview purely benign (B1). E2 rep 1 tested it and came to
the ground truth's answer by a different route: *"My first pass set that threshold at
15%, which flagged `harborview` too. That was a false positive — it's a genuinely new
merchant with chunkier round pricing, not a cents bug. 50% separates the real defect
cleanly."* The CSV supports both readings. No expectation may be keyed on "names
belltower and only belltower".

## What the baseline is NOT failing at

Segmented reasoning, per-column typing, null-rate-by-segment, and the arithmetic. Every
isolated run found D1, D2 and D3. No step may be written teaching those, because no run
failed at them.
