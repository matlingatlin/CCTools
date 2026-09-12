# Blinded grading report — build `data-contract-assertions-v2`, round 2

## 1. Scores

**Per label, per item** (labels re-randomise per item — these rows are not comparable across columns):

| Item | Expectations | A | B | C |
|---|---|---|---|---|
| E1 | 7 | **6/7** | **6/7** | **5/7** |
| E2 | 6 | **3/6** | **6/6** | **6/6** |
| E3 | 6 | **3/6** | **6/6** | **2/6** |
| E4 | 5 | **0/5** | **5/5** | **3/5** |
| **Total** | **24** | **12/24 — 50.0%** | **23/24 — 95.8%** | **16/24 — 66.7%** |

**These totals are close to meaningless and should not be read as arm scores.** Because labels re-randomise, the only figures that survive the key being opened are the per-item cells above. Recombine from those.

Two facts that must travel with the numbers:

- **E4-A is a single sentence.** It contains no analysis of the `amount` column at all, and scores 0/5 purely by having no text. Whatever total it lands in is dominated by what looks like a truncated or mis-captured output rather than a graded answer. Any arm total containing E4-A should be reported with and without that item.
- I found the answers separable into three consistent style families across all four items (§4). Under that grouping the recombined totals are **20/24, 18/24, 13/24** — a materially different ordering from the per-label totals above, and the 18 includes E4's zero.

---

## 2. Per-expectation evidence

### E1 — derive a contract, say what today's batch does to it

**E1.1 — names the amount unit change, locates it in belltower** [FIXTURE]

- **A: MET** — "**`belltower` switched USD → cents.** All 440/440 rows, p50 32.75 → 2,726.50 (**83x**)"
- **B: MET** — "**`amount`, merchant=belltower** — cents in a USD-declared column. All 440 values integer-valued ... median 32.75 → 2726.50"
- **C: MET** — "All 440 belltower rows are whole numbers (median 2729, max 20625) ... Belltower switched to **cents**."

**E1.2 — customer_age null collapse scoped to android, not only the whole-column figure** [FIXTURE]

- **A: MET** — "`customer_age` nulls 1.4% → 17.8%, concentrated at **83% of the android channel** (was 1.6%)"
- **B: MET** — "**`customer_age`, channel=android** — 1.61% → 83.12% null while ios (0.0183), web (0.0180) and phone (0.0139) sit inside their own reference spread"
- **C: MET** — "But it isn't spread: web 1.8%, ios 1.8%, phone 1.4%, **android 83.1%**"

**E1.3 — settled_days ceasing to parse as a number, affected row count ~1184** [FIXTURE]

- **A: MET** — "**`settled_days` gained a `\" d\"` suffix** on 1,184 rows (29.6%) ... Breaks every downstream `int()`."
- **B: NOT MET** — the type break is named: "two encodings in one batch: 70.4% bare integers, 29.6% `\"0 d\"`", but no row count appears anywhere in the answer, and no batch size is stated from which 1184 could be recovered. Fails on the count conjunct only. **I regard this as a bad judgment forced by the expectation's wording — see §3(d).**
- **C: MET** — "1184 rows (29.6%) are now `\"0 d\"`, `\"1 d\"` ... Strict integer parsers fail"

**E1.4 — harborview and chargeback assigned explicitly to the widen/ratify side, not the side that stops the batch**

- **A: NOT MET** — harborview is put on the explicit do-not-widen side: "**Broken feed — fix at the producer, do not widen:** #1 belltower cents, #2 the `\" d\"` suffix, **#4 harborview mixed units**." chargeback appears on the amendment side in triage but also stops the batch: "**New `status` value `chargeback`** ... | H9 |" under the verdict "**REJECTED — 3 HARD failures**". (See §3(d) — the harborview half of this conflicts with the FIXTURE's own protection clause.)
- **B: MET** — "**WIDEN — extends a set never declared closed** — New merchant `harborview` (240 rows) → added to the allowed set ... New status `chargeback` (90 rows) → added"; the BLOCK list contains only amount/settled_days/customer_age.
- **C: NOT MET** — "**4. Two new enum members.** `merchant` gains `harborview` ... and `status` gains `chargeback`" appears as item 4 under "**What today's batch does to it: 9 blocking violations**", closing with "Reject the batch." The amendment route is named ("expand the domains, rather than patching them through") but the assignment is to the blocking tally.

**E1.5 — two separate counts or two labelled lists, not one failure tally**

- **A: MET** — "**Broken feed — fix at the producer, do not widen:**" and "**Probably legitimate — needs an amendment with reason, approver, effective date:**" are two labelled lists.
- **B: MET** — "**Verdict on today's batch: BLOCK = 3, WIDEN = 2.** Two separate counts"
- **C: MET** — "**9 blocking violations**" section vs "**## Warnings, not blocks**" section. Structurally two labelled lists (the *contents* are wrong; that is E1.4's job, not this one).

**E1.6 — channel mix treated as no-action / observe-only, not a defect** [FIXTURE]

- **A: MET** — "Channel mix shifted 10pp ... Possibly the same release as #5", and it is triaged under "**Probably legitimate**", not under "Broken feed". (Marginal: it is still counted inside "5 SOFT breaches".)
- **B: MET** — "Channel mix ... contradicts nothing and extends nothing — its band is demoted to observe-only, counted in neither tally."
- **C: MET** — "**Channel mix moved** ... Large, but this is real-world drift, not malformed data", under "Warnings, not blocks".

**E1.7 — every numeric bound derived-and-shown, or explicitly not-derived and non-gating**

- **A: MET** — "every SOFT bound is marked **provisional/observe-only** — it tickets, it never pages"; HARD tier is enumerated as exact/structural: "10 HARD invariants (PK, no-blanks, amount > 0, declared units, closed `status` enum, replay)".
- **B: MET** — "Only two gating checks carry a number, both derived and shown: A-05's cut sits in the gap between an observed ceiling of 0.016 and the mechanical 1.0 a ×100 scale change forces; A-06's 0.10 is an absurdity floor at 3.4× the highest per-channel rate the reference ever showed ... `MIN_SEGMENT_N = 100` is also `NOT DERIVED`".
- **C: NOT MET** — two gating cross-field rules ship undeserved numbers: "**no merchant may exceed 5% whole-number amounts**, and **batch total within 3× of reference**." Neither derivation is shown and neither is marked non-gating; they are the rules the answer says catch the worst failure. The closing caveat covers different numbers only — "the `amount` max of 850 and the categorical share tolerances are judgment calls extrapolated from a single day" — and gives no non-gating status.

---

### E2 — the assertions to run on every batch

**E2.1 — no row-count pin at 4000 without stated derivation** [FIXTURE]

- **A: MET** — no row-count assertion appears; the structure tier is "schema/order, non-empty, id format + uniqueness, exact-duplicate rows", and batch size is treated as variable: "Checks that can't be evaluated at a given batch size report SKIP rather than guessing".
- **B: MET** — "That's an export cap, not a batch size — so I did not derive a row-count band, which means **a silently truncated feed is currently undetectable**."
- **C: MET** — "the row-count band and the SLA don't exist at all — the feed has no timestamp column."

**E2.2 — unseen merchant or status routes to decision/amendment/review, not automatic hard block**

- **A: NOT MET** — "**Unseen categories FAIL rather than warn.** A new merchant is a legitimate event, but joins and revenue splits are keyed on these, so it should land deliberately via a profile update." FAIL is defined as "exit 1", an automatic hard block; the profile update is remediation after the block, not a route around it.
- **B: MET** — "new merchant `harborview`, which is routine onboarding and correctly a ticket rather than a page" (SOFT tier). Passes on the merchant half; the status half goes the other way — "the gate fails loud with 8 HARD breaches: ... and a new `chargeback` status" — which the expectation's "or" permits. **See §3(b).**
- **C: MET** — "**B01–B03 open sets** — merchant/status/channel. A new value here is an **amendment**, not a failure."

**E2.3 — at least one assertion evaluated per segment**

- **A: MET** — "composition (per-category share, null rates, **null concentration by channel**); and numeric distribution (median, p99, whole-number share, **per-merchant median**, PSI)"
- **B: MET** — "Run ratio checks **per segment**, not just per column."
- **C: MET** — "android's `customer_age` null collapse 1.6%→83.1%" is a segment-scoped BLOCK row, and the band is derived per cell: "null rate 5% (largest cell at n≥200 was 1.77%)".

**E2.4 — every numeric bound carries derivation, or a not-derived marker with owner/non-gating status**

- **A: NOT MET** — the hard bounds do carry derivation ("`customer_age` and `settled_days` do get hard bounds — they sit *exactly* on their limits across all 4000 rows, which reads as an enforced clamp rather than a sampling artifact"), but the distributional tier — "numeric distribution (median, p99, whole-number share, per-merchant median, PSI)" — ships with no bound values, no derivations and no non-gating marker, and its checks are FAIL-tier: "`belltower` amounts ~83x inflated (cents) ... `E4` + `E2` + `E3`" counted among "9 FAILs".
- **B: MET** — "per the method's rule, structural checks are binding and **every distributional bound is marked provisional**", with derivations shown for the ones that matter: "real dollar amounts carry cents ~99% of the time (per-merchant baseline 0.38–1.64%) ... belltower reads 1.04% → 100.00%" and "the observed ratio was 83x, not 100x — a tight 'near a power of ten' test would have missed it, so H14 bounds on a wide `[0.125, 8]` band instead."
- **C: MET** — "**D01–D07 derived distributional** — every one ships `gating: false`", plus derivations ("`amount` p10 ratio 1.5× (largest observed split-half move was 1.30×)") plus "Two numbers are flagged `NOT DERIVED` with owners".

**E2.5 — states what it could not derive, naming the missing input**

- **A: NOT MET** — the two nearest passages fall short of naming a missing input. "**`amount` gets no upper bound.** Its reference max of 564.33 is a sample max on a heavy tail, not a cap" states a bound it declined to set and why, but names no absent source; "One thing I'd want your input on: I treated the 17.8% age-null rate as a defect, but if the android SDK genuinely stopped collecting age, that's a product change" is an interpretive question to the user, not a missing derivation input. Nothing in the answer flags the single-period limit, the absent timestamp, or the absent reconciliation source.
- **B: MET** — "there is **no timestamp column of any kind**: no freshness check is possible ... Third, one period, no reconciliation source ... so I did not derive a row-count band".
- **C: MET** — "The feed has no control total, no settlement file, no labelled outcome, so no harm bound is derivable — and no source in `threshold-evidence.md` maps drift magnitude to downstream cost."

**E2.6 — distinguishes exact assertions needing no bound from distributional ones that do**

- **A: MET (marginal)** — the check list is grouped exactly along that line ("structure (...); types and bounds (...); categorical domains (unseen values ...); and numeric distribution (...)") and the bound/no-bound question is addressed head-on: "**`amount` gets no upper bound** ... `customer_age` and `settled_days` do get hard bounds." The *rationale* (exact checks need no derivation) is never stated. **See §3(b).**
- **B: MET** — "structural checks are binding and every distributional bound is marked provisional."
- **C: MET** — "**A01–A14 exact/structural** — presence, uniqueness, `txn_id` format, `currency` as a *declared unit* ... **No bound to derive, nothing to backtest, so these gate.** ... **D01–D07 derived distributional** — every one ships `gating: false`."

---

### E3 — what threshold should we use

**E3.1 — magnitude threshold cannot be derived: no source maps distance moved to downstream cost** [NAMED AXIS]

- **A: NOT MET** — the answer refuses a threshold, but on different grounds: "You can't derive a drift band from a batch that's the anomaly." Its three stated blockers are the row-count cap, the missing timestamp and the single reference period — "**One reference period only.** No seasonality is observable" — none of which is the cost-mapping absence. It then ships bounds anyway.
- **B: MET** — "**No harm bound exists here.** Neither file contains a downstream signal that moves — no settlement control total, no bill, no labelled outcome. So the three blockers block because they contradict a producer commitment ..., not because a distribution moved far enough. Nothing in this contract is licensed to say 'past here, something downstream is wrong.'"
- **C: NOT MET** — no such absence is named anywhere; the answer proceeds to a recommended cutoff.

**E3.2 — no numeric cutoff presented as standard/conventional; numbers permitted only with derivation and a statement of what they are and are not evidence of** [NAMED AXIS]

- **A: NOT MET** — partially satisfies: the p50/p90 bands carry a derivation ("Derived from the 7 merchants that are clean, whose observed period-over-period variation was p50 ratio **0.90–1.09** and p90 ratio **0.99–1.15**") and the answer contains a strong statement of what a number would not be evidence of ("a bound tight enough to catch it would be a round number pretending to be evidence"). But two of the five shipped bounds are HARD/gating with no derivation shown: "ratio ≥ 50x or ≤ 0.02x — escalates to HARD" and "`customer_age` null rate — > 4% — SOFT". The permission clause is conjunctive; those numbers do not satisfy it.
- **B: MET** — "**The one number, and its honest limit.** `customer_age` null rate ≤ **0.0213** — the max of 10,000 bootstrap resamples (n=4000) ... That is *within-batch* sampling variation ... it is not trustworthy at the margin. Re-derive from ≥5 landed batches", plus "**Two numbers I did not derive, flagged as such:** the unit-change `median_ratio ≥ 10` gate (`NOT DERIVED — owner: feed owner`)".
- **C: NOT MET** — refuted directly: "**The standard 0.1 warn / 0.25 alert** would fire on ..." and "**Then PSI 0.1 warn / 0.25 page is fine**". A convention is named as standard and adopted as the recommendation.

**E3.3 — names what the decision depends on that the data cannot supply (consumer + cost, or an independent downstream signal)**

- **A: MET** — "One judgment call for you: the contract defaults to **fail-loud** because this data is money-shaped. If the consumer is a dashboard or a model rather than billing, quarantine is the better choice — §1 of the contract is left blank for you to fill in, and it's the line that decides it."
- **B: MET** — "Neither file contains a downstream signal that moves — no settlement control total, no bill, no labelled outcome", plus "the capacity bound (needs the on-call's actual read volume)".
- **C: NOT MET** — no consumer, no cost of a bad batch, no downstream signal is named. The closest is a producer question about one merchant — "worth confirming with whoever onboarded them" — which is not the decision input the expectation asks for, and "if that ios/web shift matters to you, it needs its own explicit rule", which defers the question without naming what it depends on.

**E3.4 — separates the differences needing no threshold from the one genuine distribution shift** [FIXTURE]

- **A: MET** — "Four independent breaks are in that file right now" (unit change, type suffix, new status, null rate) are set against the mix shift, which is held out as the one thing it will not gate: "I deliberately left `channel` mix (web −10.1pp, ios +10.8pp) **unalerted** — with one period I can't distinguish drift from a real app-install trend." The unit detector is flagged as needing no tuning: "whole-number share is near-binary ... so it needs no tuning and no history."
- **B: MET** — "Two of the three blockers are exact assertions with no bound to tune. Only one has a number", and "The channel mix shift ... is logged **observe-only**".
- **C: MET** — "**Add the guards PSI structurally can't provide:** — **Schema/format assertions** — `settled_days` matches `^\d+$` ... Catches the format bug at ingest, at full severity, instead of as a PSI score"; unseen categories are routed off the threshold ("alert on unseen categories as an info-level event instead"); and channel is identified as the genuine shift: "`channel` | 0.06 | ios +10.8pp, web −10.1pp. **The one thing here that looks like real behavioral drift.**"

**E3.5 — states the block-versus-widen assignment with counts on both sides**

- **A: NOT MET** — no widen side exists. The findings are "Four independent breaks", with `chargeback` among them; the only counts given are of assertions, not of differences — "11 HARD invariants, 8 SOFT bounds".
- **B: MET** — "**The split — 3 BLOCK, 2 WIDEN** (counts kept separate; the batch is not quarantined whole)", with both sides tabulated.
- **C: NOT MET** — no block/widen structure and no counts on two sides; the organising frame is a per-column PSI table.

**E3.6 — checks held back are said to be held back, explicitly**

- **A: MET** — "every SOFT bound above is provisional/observe-only until ~6 periods accumulate. I deliberately left `channel` mix ... **unalerted**".
- **B: MET** — "The channel mix shift ... is logged **observe-only** — one reference batch gives no spread to derive a band from."
- **C: MET** — "with `merchant` excluded from paging (new merchants are expected; alert on unseen categories as an info-level event instead)" and "One thing I'd flag rather than assert: `harborview` ...". **Passes on a demotion while the headline cutoff ships as a page — see §3(b).**

---

### E4 — the amount column, when column statistics look fine

**E4.1 — unit or scale change, not a set of large outliers** [FIXTURE]

- **A: NOT MET** — the entire answer is "`assert_batch.py` runs the assertions at the boundary on the raw batch and exits non-zero on gating failures — 3 BLOCK, 2 WIDEN, 10 observe-only firings, 12 passed." No defect is named.
- **B: MET** — "**The `amount` column is in cents for some rows and dollars for the rest** — a mixed-unit column, which is why every column-level statistic passes."
- **C: MET** — "## Found it: a unit mismatch (cents written into a dollars column), hidden inside two merchants"

**E4.2 — locates it by segment, names belltower** [FIXTURE]

- **A: NOT MET** — no segment, no merchant named.
- **B: MET** — "| `belltower` | 440 (100%) | **cents** | p50 ratio vs reference = **83x** ... 100% integer-valued"
- **C: MET** — "**`belltower` — 100% corrupted.** Every one of its 440 rows is an integer. `T004003,belltower,web,4560.0` is $45.60, not $4,560."

**E4.3 — why a whole-column statistic missed it, with the segment-versus-column comparison** [FIXTURE]

- **A: NOT MET** — absent.
- **B: MET** — "## Why the column-level stats looked fine — `belltower` is only 11% of rows, so the pooled view is dominated by the healthy 89%", with the pooled table (p50 29.84 → 33.96, "1.14x") against "grouped by merchant it's 83x on one merchant".
- **C: MET** — "**Why the column stats looked fine:** ... even a self-contained check passes: no nulls, no zeros, no negatives, valid floats throughout, and the median (33.96) barely moves because only 12% of rows are affected", against the per-merchant table showing belltower mean 3871.26 vs reference 42.04.

**E4.4 — on harborview, both readings open, or which measurement separates it from belltower and which does not**

- **A: NOT MET** — harborview is not mentioned.
- **B: MET** — states which measurement is unavailable and which identifies it: "it's a **new merchant** with no baseline to ratio against, and only 16% of its rows are affected — scattered across every channel, status and settled_days value, so **no dimension isolates them**. Only the integer-valued fraction (15.8% vs ~1% expected) gives it away." The rival reading is named as a live risk: "any **genuine whole-dollar harborview transaction** would be wrongly divided."
- **C: NOT MET** — a single reading is asserted with no rival: "**`harborview` — ~16% corrupted, interleaved.** ... it looks like one of two upstream paths for that merchant is unconverted", and the verification treats the ÷100 as settled: "dividing those 478 rows by 100 collapses every merchant onto the reference distribution — belltower mean 38.71, harborview 40.89 ... which is strong evidence the 100× factor is the entire story."

**E4.5 — any repair rule proposed carries the case it would get wrong**

- **A: NOT MET** — no repair rule and no content; nothing in the text meets or refutes it, which under the stated scoring rule is NOT MET. **This ruling turns on an ambiguity the expectation leaves open — see §3(d).**
- **B: MET** — "a `/100` repair applied to `belltower` is safe, but the `harborview` rows can only be identified heuristically (integer-valued), and any genuine whole-dollar harborview transaction would be wrongly divided. That needs a producer conversation, not a downstream correction."
- **C: NOT MET** — the one rule offered carries no failure case: "**Detection rule for the pipeline:** per-merchant rate of `amount % 1 == 0`. Alert above ~5%. That catches both cases here and any future feed that flips units." The ÷100 identification of 478 rows is applied as fact ("Nothing else needed adjusting") with no note that a genuine whole-dollar charge would be misclassified by it — the exact case another answer names.

---

## 3. Attack on the expectation set

### (a) Expectations that carried no information this round

Eight of twenty-four — a third of the set — were met by all three answers and separated nothing:

**E1.1, E1.2, E1.5, E1.6, E2.1, E2.3, E3.4, E3.6.** None was met by zero answers.

Four of those eight were *predicted* discriminating by the author and were not: **E1.5, E2.1, E3.6** are labelled "discriminating", and E1.5's failure to discriminate is structural — see (b). The set's own labelling of what would discriminate was wrong on three items. Meanwhile the two declared regression guards (E2.3, E4.2) both behaved as guards should, so the guard labelling held up where the discrimination labelling did not.

The live spread in this round rests on **11 expectations**: E1.3, E1.4, E1.7, E2.2, E2.4, E2.5, E2.6, E3.1, E3.2, E3.3, E3.5, plus E4.1–E4.5 where one answer's emptiness dominates. That is a thinner instrument than 24 points suggests.

### (b) Expectations passable on a phrase rather than substance

- **E2.2 is defeated by its own disjunction.** "An unseen merchant **or** status value routes to a decision, amendment or review" — E2-B hard-blocks the new status ("the gate fails loud with 8 HARD breaches: ... and a new `chargeback` status") while ticketing the new merchant, and scores the point. The substance the expectation wants is a *policy* for unseen categories; the wording only requires one instance. It should read "unseen categorical values route to...", tested against both.
- **E1.5 is pure form and E1.4 is its substance, so an answer can get the assignment exactly backwards and still bank E1.5.** C lists new categories under "9 blocking violations" and still scores E1.5 for having a second list headed "Warnings, not blocks". Splitting form from content across two expectations gives a half-credit that neither expectation intended.
- **E3.6 is satisfiable by one token demotion.** C passes on "One thing I'd flag rather than assert" and on excluding `merchant` from paging, while the answer's headline recommendation is a gating page threshold presented as standard. The expectation reads "where it holds a check back" — an answer that holds almost nothing back passes as long as it labels the one thing it does hold.
- **E2.6 passes on a taxonomy.** Any answer that lists its checks in the obvious groups (structure / types / categorical / distribution) satisfies "distinguishes exact from distributional" without ever asserting the point that matters — that the exact ones need no derived number and therefore need no evidence to gate on. A passes on grouping alone.
- **E1.7 and E2.4 accept the word "provisional" as a non-gating status.** Whether a check marked provisional actually gates is not visible in prose, and one answer numbers a distributional band inside its HARD series (`H14 ... [0.125, 8]`) while asserting all distributional bounds are provisional. The expectation cannot see that tension.

### (c) What the answers plainly differ on that no expectation asks — the most valuable gap

1. **Correct scoping of the null defect *on E3*.** E1.2 tests android-scoping on E1, and every answer gets it. On E3, where mis-scoping would send the user to the wrong threshold, two of three answers state it *wrongly*: "`customer_age` null rate went 1.4% → 17.8%, **uniformly across all merchants**, so it's a producer-side change, not merchant-specific" and "1.40%→17.82%, **uniform across all 9 merchants**". Both are technically true about merchants and both miss the channel concentration entirely; the third answer is the only one to localise it — "**655 of 713 nulls are `android`** — 83% of android rows." No E3 expectation looks at this. It is the clearest substantive quality difference in E3 and the set is blind to it. **This should be an expectation.**

2. **Backtest / false-positive evidence.** Three answers report calibration runs of very different weight: "181 fresh batches at n=100…2000 ... **Zero false FAILs**; 9 WARN events"; "it fired 3,258 times across 800 legitimate 500-row pseudo-batches ... After both fixes: **0 HARD and 2 SOFT across 3,401 legitimate batches**"; "deriving on reference rows 1–2000 and measuring on 2001–4000, **five of eight profile-derived bands failed**". Others report nothing. Whether the suite will be switched off in a week is decided here, and no expectation on E2 — the item that *asks for the suite* — mentions backtesting, holdout, or false-positive rate. E2 rewards saying you could not backtest, and does not reward having done so.

3. **Numerical accuracy is never checked.** Every expectation asks whether a figure is *present*, none whether it is *right*. The answers disagree with each other on figures they all claim to have computed: belltower median "2726.50" vs "2729"; current whole-column median "33.96" vs "33.95"; harborview's suspect rows "38" vs "35 of its rows ≥$500" vs "35 of 240 rows above 600"; repaired totals "$165,627", "166,832.91", "41.71 mean". At most one of each set is right. An expectation set for a data-quality skill that cannot see an arithmetic error in the answer is measuring register, not analysis.

4. **Whether the answer answers the question.** E3 asks "what threshold should we use?" Two answers decline and pivot; one gives an ordered, actionable plan ("**Fix the three defects first** ... **Then PSI 0.1 warn / 0.25 page is fine**, applied post-normalization and per-column"). Declining may well be correct — that is what E3.1/E3.2 encode — but nothing in the set credits *usable next steps*, so an answer can score 6/6 on E3 without the reader knowing what to do on Monday. This biases the item; see (d).

5. **Deliverable existence.** Most answers ship named runnable files (`assert_contract.py`, `assert_batch.py`, `validate.py`, `contract.yml`, JSONL/CSV results); two ship none. E2 asks for a suite and no expectation asks whether one exists.

6. **Whether the answer notices it is looking at the wrong thing.** One E2 answer profiled `current.csv` as the arriving batch and said so; another built purely from the reference. Same task, materially different method. Unasked.

### (d) Expectations I judge unfair, mis-weighted, or self-contradictory

- **E1.4 contradicts FIXTURE-FACTS' own protection clause.** The fixture says: "Do NOT mark an answer down for calling harborview contested, partially affected, or clean." E1.4 requires harborview on the widen side and marks down any answer that puts it elsewhere. One answer put harborview under "**do not widen**" precisely *because* it read harborview as unit-affected — a reading the fixture protects — and lost the point. I scored it NOT MET only because its `chargeback` handling independently fails ("caught by H9" inside a "REJECTED" verdict), but the conflict is real and would decide the point on a different answer. **E1.4 should be restricted to `chargeback` and the new-merchant *value*, not to any judgment about harborview's amounts.**

- **E3.1, E3.2 and E3.3 are one axis scored three times.** All three ask whether the answer names the missing cost-mapping. An answer holding that stance banks 3/6 of the item before anything else is assessed; one without it starts at 0/6 — which is the entire E3 spread (6 vs 3 vs 2). Add E3.6 and the item is two-thirds a test of a single disposition. E3 has six expectations but roughly two independent dimensions.

- **The same disposition is over-weighted set-wide.** E1.7, E2.4, E2.5, E2.6, E3.1, E3.2, E3.3, E3.6 — eight of twenty-four — all reward some form of *labelling numbers as underived, non-gating, or missing*. A set that puts a third of its mass on one habit measures adherence to a vocabulary at least as much as analytic quality, and an answer that adopts the vocabulary without doing better analysis would outscore one that does better analysis without it. Given the set's own admission that four answers use the method's vocabulary verbatim, this is the most serious structural risk in the instrument.

- **E1.3 taxes a presentation choice.** "the affected row count in the region of 1184" cost one answer a point for writing "29.6%" instead of "1,184". The information content is identical; the answer simply never states the batch size in that item. **The expectation should accept a percentage of a stated or obvious denominator.** Correct this and that answer's E1 goes 6/7 → 7/7.

- **E4.5's vacuity is unspecified, and it mattered.** E1.7 explicitly says "An answer that proposes no bound at all also meets this." E4.5 says only "Any repair rule it proposes carries the case it would get wrong", with no such clause. An answer proposing no repair is either automatically MET (vacuous truth) or automatically NOT MET (nothing decides it) depending on a reading the text does not fix. I applied the "neither met nor refuted is NOT MET" rule, which costs the empty answer a point it could equally have been handed for free. **Add E1.7's clause, or drop the expectation.**

- **E4.4 scores hedging, not correctness.** The withheld key "calls harborview purely benign"; E4.4 fails any answer that says harborview is clean *with no rival named*. So an answer that agrees with the key and says so plainly fails the expectation, while an answer that is wrong in both directions but names both passes. The fixture's contested-figure note acknowledges this and instructs the grader to protect it, which means the expectation is measuring epistemic register. That is a legitimate thing to measure — but it should be labelled as such, not as a finding about harborview.

- **E3.2's conjunction is doing two incompatible jobs.** "Does not present any numeric cutoff as standard" (a prohibition, cleanly testable) is welded to "proposing a number is permitted only where the answer shows the derivation and says what the number is and is not evidence of" (a demanding positive standard). One answer violates neither the prohibition nor the spirit — it derives its main bands from the seven clean merchants and warns that a tighter bound "would be a round number pretending to be evidence" — yet fails on two auxiliary numbers. **Split it into a prohibition and a standard, scored separately.**

- **Nothing tests E4's actual premise.** E4 says the column statistics "look fine". Only one answer challenges that framing — "they probably weren't checked against the reference — current mean is 497 vs 41" — which is a genuinely good catch about the user's own claim. No expectation rewards it.

---

## 4. Separability — the blinding did not hold

**I found the labels separable on all four items, not just some.** The twelve answers fall cleanly into three style families that are consistent across every item:

| Family | Items | Signature |
|---|---|---|
| **I** | E1-B, E2-C, E3-B, E4-A | `BLOCK`/`WIDEN` as the organising split with counts; `NOT DERIVED — owner: <name>`; `NOT BACKTESTED`; "held-out coverage"; "Where I did not confirm the narrow story"; "no harm bound exists here" |
| **II** | E1-A, E2-B, E3-A, E4-B | `HARD`/`SOFT` tiers; "per the method's rule, structural checks are binding and every distributional bound is marked provisional"; numbered step references ("step 1", "step 2", "step 8"); hashed run directories (`run-cd42511f2d/`, `run-0f506b0833/`) |
| **III** | E1-C, E2-A, E3-C, E4-C | no method vocabulary at all; PSI as the frame; "blocking violations" / "Warnings, not blocks"; conventional cutoffs cited as standard |

**What gave it away, in order of strength:**

1. **Verbatim vocabulary.** `NOT DERIVED — owner:` and `NOT BACKTESTED` appear in exactly the four Family I answers and nowhere else. "structural checks are binding ... distributional bounds ... provisional" appears near-verbatim in three of the four Family II answers. The expectation set anticipated this and bounded it as "a method-armed answer from a bare one" — but it is stronger than that admission: it separates **two method-armed families from each other**, not just method from bare. `BLOCK/WIDEN + NOT DERIVED — owner` and `HARD/SOFT + provisional/observe-only` are disjoint dialects, and no answer mixes them.
2. **Housekeeping tics.** Family II names hashed run directories; Family I names `assert_batch.py` with JSONL-per-assertion output and reports "reference against itself: 0 BLOCK, 0 WIDEN"; Family III names no artifacts in two of four items.
3. **Framing of the harborview question.** Family I treats it as two open readings requiring a producer ("Both readings are open", "Nothing in these two files settles it"); Family III asserts one reading. Family II sits between, asserting the reading but naming the repair's failure case.

**Consequence for the numbers.** Under this grouping the recombined totals are **Family II 20/24 (83.3%), Family I 18/24 (75.0%), Family III 13/24 (54.2%)** — a different ordering from the per-label totals, and Family I's figure is entirely hostage to E4-A's 0/5. Excluding E4, the three families run **18/19, 18/19, 10/19**, which flips the top two into a tie and is the honest reading of this round.

**So the blinding was worth very little here.** I graded from the expectations and quoted text, and I have not opened the key or inferred which family is which arm — but a grader who wanted to could reconstruct the arms from prose alone in under a minute, and the two method-armed families are as separable from each other as either is from the bare one. The set's stated bound ("It CANNOT separate the two method-armed arms from each other") **does not hold in this round.** If the comparison that decides the build is between those two families, the blinding did not protect it, and that should be recorded as unmet rather than carried forward from the previous build.

---

Say the word if you want this as a published page for the build record.
