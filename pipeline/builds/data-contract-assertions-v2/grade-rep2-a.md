## 1. Totals

**Per label, per item, and overall.** Labels re-randomise per item, so only the per-item cells are recombinable.

| Label | E1 (/7) | E2 (/6) | E3 (/6) | E4 (/5) | Total (/24) | % |
|---|---|---|---|---|---|---|
| **A** | 6 | 5 | 3 | 0 | **14** | **58.3%** |
| **B** | 6 | 5 | 6 | 4 | **21** | **87.5%** |
| **C** | 4 | 6 | 2 | 3 | **15** | **62.5%** |

Column sums: E1 16/21, E2 16/18, E3 11/18, E4 7/15. E3 and E4 are where the answers actually separate; E1 and E2 are nearly saturated.

---

## 2. Per-expectation evidence

### E1 — derive a contract, say what today's batch does to it

| | A | B | C |
|---|---|---|---|
| E1.1 | MET | MET | MET |
| E1.2 | MET | MET | MET |
| E1.3 | MET | **NOT MET** | MET |
| E1.4 | **NOT MET** | MET | **NOT MET** |
| E1.5 | MET | MET | **NOT MET** |
| E1.6 | MET | MET | MET |
| E1.7 | MET | MET | **NOT MET** |

**E1.1 — amount unit change located in belltower**
- A **MET**: "**`belltower` switched USD → cents.** All 440/440 rows, p50 32.75 → 2,726.50 (**83x**)".
- B **MET**: "**`amount`, merchant=belltower** — cents in a USD-declared column. All 440 values integer-valued … median 32.75 → 2726.50".
- C **MET**: "All 440 belltower rows are whole numbers (median 2729, max 20625) … Belltower switched to **cents**."

**E1.2 — customer_age null collapse scoped to android**
- A **MET**: "**`customer_age` nulls 1.4% → 17.8%**, concentrated at **83% of the android channel** (was 1.6%)."
- B **MET**: "**`customer_age`, channel=android** — 1.61% → 83.12% null while ios (0.0183), web (0.0180) and phone (0.0139) sit inside their own reference spread."
- C **MET**: "But it isn't spread: web 1.8%, ios 1.8%, phone 1.4%, **android 83.1%**."

**E1.3 — settled_days ceases to parse as a number, ~1184 rows**
- A **MET**: "**`settled_days` gained a `" d"` suffix** on 1,184 rows (29.6%) … Breaks every downstream `int()`."
- B **NOT MET**: "two encodings in one batch: 70.4% bare integers, 29.6% `"0 d"`". The defect is named, but no row count is given and the answer never states the batch size, so 1184 is not recoverable from the text; nor does it say the column stops parsing as a number. *(Flagged in §3(b) — this is a phrasing-driven miss on substance the answer clearly has.)*
- C **MET**: "**3. `settled_days` — type break.** 1184 rows (29.6%) are now `"0 d"` … Strict integer parsers fail; lenient ones silently coerce to null."

**E1.4 — harborview and chargeback on the WIDEN side, explicitly, not the stopping side**
- A **NOT MET**: harborview is put on the blocking side by name — "**Broken feed — fix at the producer, do not widen:** #1 belltower cents, #2 the `" d"` suffix, **#4 harborview** mixed units." Only chargeback reaches the amendment side.
- B **MET**: "**WIDEN — extends a set never declared closed** — New merchant `harborview` (240 rows) → added to the allowed set … New status `chargeback` (90 rows) → added".
- C **NOT MET**: both sit inside "## What today's batch does to it: **9 blocking violations**" as "**4. Two new enum members.**", and the verdict is "Reject the batch." The vendor-conversation remark ("expand the domains") does not undo the blocking placement.

**E1.5 — two separate counts or two labelled lists**
- A **MET**: two labelled lists on the block/amend axis — "**Broken feed — fix at the producer, do not widen:** …" and "**Probably legitimate — needs an amendment with reason, approver, effective date:** …". (Headline is a whole-batch verdict, but the two lists exist.)
- B **MET**: "**Verdict on today's batch: BLOCK = 3, WIDEN = 2.** Two separate counts".
- C **NOT MET**: one tally — "9 blocking violations" — plus a "## Warnings, not blocks" section that contains no widening differences (it holds channel mix and harborview's *mixed units*, a defect). The widening items are inside the 9.

**E1.6 — channel mix as no-action / observe-only**
- A **MET**: listed as SOFT, and "every SOFT bound is marked **provisional/observe-only** — it tickets, it never pages"; in triage it lands under "Probably legitimate".
- B **MET**: "Channel mix … contradicts nothing and extends nothing — its band is demoted to observe-only, counted in neither tally."
- C **MET**: under "## Warnings, not blocks" — "Large, but this is real-world drift, not malformed data."

**E1.7 — every numeric bound derived-and-shown, or marked not-derived and non-gating**
- A **MET**: "**no honest distributional band exists**. Per the method's rule, structural checks are binding and every SOFT bound is marked **provisional/observe-only** — it tickets, it never pages." HARD tier is exact (PK, no-blanks, amount > 0, declared units, closed enum, replay).
- B **MET**: "Only two gating checks carry a number, both derived and shown: A-05's cut sits in the gap between an observed ceiling of 0.016 and the mechanical 1.0 a ×100 scale change forces; A-06's 0.10 is an absurdity floor at 3.4× the highest per-channel rate the reference ever showed … `MIN_SEGMENT_N = 100` is also `NOT DERIVED`".
- C **NOT MET**: two gating cross-field rules ship bare — "**no merchant may exceed 5% whole-number amounts**, and **batch total within 3× of reference**" — with no derivation for either. The closing caveat marks "the `amount` max of 850 and the categorical share tolerances" as "judgment calls extrapolated from a single day" but leaves them blocking, and does not cover the 5% or 3×.

---

### E2 — the assertions to run on every batch

| | A | B | C |
|---|---|---|---|
| E2.1 | MET | MET | MET |
| E2.2 | **NOT MET** | **NOT MET** | MET |
| E2.3 | MET | MET | MET |
| E2.4 | MET | MET | MET |
| E2.5 | MET | MET | MET |
| E2.6 | MET | MET | MET |

**E2.1 — no undefended row-count pin**
- A **MET**: no row-count check in the suite ("structure (schema/order, non-empty, id format + uniqueness, exact-duplicate rows)"), and calibration runs "181 fresh batches at n=100…2000", so no fixed size is assumed.
- B **MET**: "That's an export cap, not a batch size — so I did not derive a row-count band, which means **a silently truncated feed is currently undetectable**."
- C **MET**: "the row-count band and the SLA don't exist at all — the feed has no timestamp column."

**E2.2 — unseen merchant/status routes to decision, amendment or review, not an automatic hard block**
- A **NOT MET**: "**Unseen categories FAIL rather than warn.**" FAIL is defined as "exit 1 — … blocks". The justification ("it should land deliberately via a profile update") does not change the routing.
- B **NOT MET**: split. New merchant is routed correctly — "new merchant `harborview`, which is routine onboarding and correctly a ticket rather than a page" — but the new status is not: "the gate fails loud with 8 HARD breaches: … and a new `chargeback` status." *(The expectation's "merchant or status" disjunction arguably licenses a pass here; see §3(b). I scored on the fixture's substance, which requires both B1 and B3 not to stop the batch.)*
- C **MET**: "**B01–B03 open sets** — merchant/status/channel. A new value here is an **amendment**, not a failure." And: "**A batch carrying only these would be ratified, not refused.**"

**E2.3 — at least one assertion per segment**
- A **MET**: "composition (per-category share, null rates, **null concentration by channel**)"; "**per-merchant median**"; "the per-merchant medians and the whole-number share (0.9% → 12.8%) are what catch it".
- B **MET**: "Run ratio checks **per segment**, not just per column."; "the per-channel split localises immediately to android at 83.1%".
- C **MET**: "null rate 5% (largest cell at n≥200 was 1.77%)"; blocks are stated per segment — "belltower's `amount` scale change; android's `customer_age` null collapse".

**E2.4 — every numeric bound derived or marked**
- A **MET**: the two hard bounds carry derivation — "`customer_age` and `settled_days` do get hard bounds — they sit *exactly* on their limits across all 4000 rows, which reads as an enforced clamp rather than a sampling artifact"; the declined one carries its reason — "Its reference max of 564.33 is a sample max on a heavy tail, not a cap"; distributional bands come from a named procedure — "split-half — profile built from a random 2000 reference rows, then 181 fresh batches". No bare number appears in the text.
- B **MET**: "every distributional bound is marked provisional"; H14's band is argued — "the observed ratio was 83x, not 100x — a tight 'near a power of ten' test would have missed it, so H14 bounds on a wide `[0.125, 8]` band instead"; per-merchant baseline named (0.38–1.64%).
- C **MET**: "The bands come from splitting the reference in half: `amount` p10 ratio 1.5× (largest observed split-half move was 1.30×), null rate 5% (largest cell at n≥200 was 1.77%)"; "Two numbers are flagged `NOT DERIVED` with owners"; "**D01–D07 derived distributional** — every one ships `gating: false`."

**E2.5 — states what it could not derive, naming the missing input**
- A **MET**, weakly: "**`amount` gets no upper bound.** Its reference max of 564.33 is a sample max on a heavy tail, not a cap", plus a named input it lacks — "if the android SDK genuinely stopped collecting age, that's a product change … Worth confirming which it is before wiring this into CI." *(Passes on the literal wording; see §3(b).)*
- B **MET**: "there is **no timestamp column of any kind**: no freshness check is possible"; "one period, no reconciliation source"; "**One thing I had to assume.** You didn't say who consumes this."
- C **MET**: "The feed has no control total, no settlement file, no labelled outcome, so no harm bound is derivable — and no source in `threshold-evidence.md` maps drift magnitude to downstream cost."

**E2.6 — exact assertions distinguished from distributional ones**
- A **MET**: five named families kept apart — "structure (…); types and bounds (…); categorical domains (…); composition (…); and numeric distribution (median, p99, whole-number share, per-merchant median, PSI)" — with the bound/no-bound call made explicitly for `amount` vs `customer_age`/`settled_days`.
- B **MET**: "structural checks are binding and every distributional bound is marked provisional"; "14 HARD / 8 SOFT / 2 observe-only / 1 blocked".
- C **MET**: "**A01–A14 exact/structural** — … No bound to derive, nothing to backtest, so these gate. **B01–B03 open sets** … **D01–D07 derived distributional** — every one ships `gating: false`."

---

### E3 — what threshold should we use

| | A | B | C |
|---|---|---|---|
| E3.1 | **NOT MET** | MET | **NOT MET** |
| E3.2 | **NOT MET** | MET | **NOT MET** |
| E3.3 | MET | MET | **NOT MET** |
| E3.4 | MET | MET | MET |
| E3.5 | **NOT MET** | MET | **NOT MET** |
| E3.6 | MET | MET | MET |

**E3.1 — no source maps distribution movement to downstream cost**
- A **NOT MET**: the three blockers it names are different absences — "Both files are exactly 4000 rows … There is no timestamp column at all … One reference period only. No seasonality is observable". Insufficient history is not the missing cost mapping; the cost link is never named.
- B **MET**: "**No harm bound exists here.** Neither file contains a downstream signal that moves — no settlement control total, no bill, no labelled outcome. … Nothing in this contract is licensed to say 'past here, something downstream is wrong.'"
- C **NOT MET**: the objection raised is contamination, not underivability — "Tuning a threshold to this file means tuning it to bugs". No absence of a cost mapping is named anywhere.

**E3.2 — no numeric cutoff presented as standard/conventional; numbers only with derivation and stated scope**
- A **NOT MET**: no appeal to convention, and a partial derivation is offered — "Derived from the 7 merchants that are clean, whose observed period-over-period variation was p50 ratio **0.90–1.09** and p90 ratio **0.99–1.15**" — but the shipped table carries numbers with no derivation shown: "ratio ≥ 50x or ≤ 0.02x → escalates to HARD" and "`customer_age` null rate > 4%". The widening from 0.90–1.09 to 0.75–1.33 is also unexplained.
- B **MET**: one number, fully defended — "≤ **0.0213** — the max of 10,000 bootstrap resamples (n=4000) of the reference's own null indicator. That is *within-batch* sampling variation. … it is not trustworthy at the margin." Plus "`NOT DERIVED — owner: feed owner`; nothing in the data distinguishes anything between 1× and 100×".
- C **NOT MET**: this is the exact failure named — "The **standard** 0.1 warn / 0.25 alert would fire on …" and "**Then PSI 0.1 warn / 0.25 page is fine**". Also "Alert at ~3× reference rate" and "alert outside 0.5–2×", both undefended.

**E3.3 — names what the decision depends on that the data cannot supply**
- A **MET**: "One judgment call for you: the contract defaults to **fail-loud** because this data is money-shaped. If the consumer is a dashboard or a model rather than billing, quarantine is the better choice — §1 of the contract is left blank for you to fill in, and **it's the line that decides it**."
- B **MET**: "no settlement control total, no bill, no labelled outcome"; "the capacity bound (needs the on-call's actual read volume)"; "no consumer of this feed was checked against the schema".
- C **NOT MET**: the only external referral is a producer question about harborview — "worth confirming with whoever onboarded them". Neither the consumer, the cost of a bad batch, nor a downstream signal is named. "if that ios/web shift matters to you" is the closest, and it names no dependency.

**E3.4 — no-threshold differences separated from the one genuine distribution shift**
- A **MET**: four named breaks vs one item held out — "I deliberately left `channel` mix (web −10.1pp, ios +10.8pp) **unalerted** — with one period I can't distinguish drift from a real app-install trend".
- B **MET**: "Two of the three blockers are exact assertions with no bound to tune. Only one has a number." Channel mix is separated as "logged **observe-only**".
- C **MET**: the PSI table does exactly this — settled_days "Format bug", merchant "Business event, not a defect", status "New category … Looks genuinely new", against channel: "**The one thing here that looks like real behavioral drift.**"

**E3.5 — block-vs-widen assignment with counts on both sides**
- A **NOT MET**: one count only — "Four independent breaks are in that file right now". No widen side and no second count; the HARD/SOFT table is a severity split, not an assignment.
- B **MET**: "**The split — 3 BLOCK, 2 WIDEN** (counts kept separate; the batch is not quarantined whole)", with a table assigning each row.
- C **NOT MET**: "**Fix the three defects first**" is the only count. The benign side is scattered across prose ("merchant excluded from paging", "Looks genuinely new") with no tally.

**E3.6 — held-back checks marked explicitly**
- A **MET**: "every SOFT bound above is provisional/observe-only until ~6 periods accumulate. I deliberately left `channel` mix … **unalerted**".
- B **MET**: "The channel mix shift … is logged **observe-only**"; "`NOT DERIVED — owner: feed owner`".
- C **MET**: "with `merchant` excluded from paging (new merchants are expected; **alert on unseen categories as an info-level event instead**)"; "**One thing I'd flag rather than assert:** `harborview` has a normal median (35.00) but …".

---

### E4 — the amount column when column statistics look fine

| | A | B | C |
|---|---|---|---|
| E4.1 | **NOT MET** | MET | MET |
| E4.2 | **NOT MET** | MET | MET |
| E4.3 | **NOT MET** | MET | MET |
| E4.4 | **NOT MET** | **NOT MET** | **NOT MET** |
| E4.5 | **NOT MET** | MET | **NOT MET** |

**A's entire answer is one sentence**: "`assert_batch.py` runs the assertions at the boundary on the raw batch and exits non-zero on gating failures — 3 BLOCK, 2 WIDEN, 10 observe-only firings, 12 passed." No column, no segment, no diagnosis, no repair. E4.1–E4.5 are all NOT MET on absence. The counts happen to match the fixture's 3-block/2-widen structure, but nothing in the text identifies `amount`, `belltower`, or a unit change, so no expectation can be scored met. See §3(c) — this single answer is the largest score swing in the set and it is a delivery failure, not an analysis failure.

**E4.1 — unit/scale change, not outliers**
- B **MET**: "**The `amount` column is in cents for some rows and dollars for the rest** — a mixed-unit column, which is why every column-level statistic passes."
- C **MET**: "## Found it: a unit mismatch (cents written into a dollars column), hidden inside two merchants".

**E4.2 — located by segment, belltower named**
- B **MET**: "| `belltower` | 440 (100%) | **cents** | p50 ratio vs reference = **83x**, p90 = **97x**; 100% integer-valued".
- C **MET**: "| belltower | 440 | **440 (100%)** | mean 3871.26 | reference mean 42.04"; "**`belltower` — 100% corrupted.** … `T004003,belltower,web,4560.0` is $45.60, not $4,560."

**E4.3 — why a whole-column statistic missed it, with the segment-vs-column comparison**
- B **MET**: "`belltower` is only 11% of rows, so the pooled view is dominated by the healthy 89%" plus the reference/current table ("p50 29.84 → 33.96, 1.14x") against "grouped by merchant it's 83x on one merchant".
- C **MET**: "the median (33.96) barely moves because only 12% of rows are affected. Only mean/std/max flag it, and a heavy-tailed transaction column is *expected* to have a big max" — set against per-merchant means of 3871.26 vs 40–44.

**E4.4 — harborview: both readings open, or which measurement separates it from belltower**
- B **NOT MET**: asserts the affected reading with no rival — the table classifies harborview's 38 rows as "**cents**", and the prose concludes "That pattern reads like a partially-migrated integration sending cents on one code path." It does say which measurement works ("no baseline to ratio against … Only the integer-valued fraction (15.8% vs ~1% expected) gives it away"), but the disqualifier clause bites. *(This expectation is internally contradictory — see §3(d).)*
- C **NOT MET**: "**`harborview` — ~16% corrupted, interleaved.** … it looks like one of two upstream paths for that merchant is unconverted." Single reading, no rival.
- A **NOT MET**: harborview not mentioned.

**E4.5 — any repair rule carries the case it would get wrong**
- B **MET**: "a `/100` repair applied to `belltower` is safe, but the `harborview` rows can only be identified heuristically (integer-valued), and **any genuine whole-dollar harborview transaction would be wrongly divided**."
- C **NOT MET**: proposes "dividing those 478 rows by 100" and a pipeline rule "per-merchant rate of `amount % 1 == 0`. Alert above ~5%", and notes genuine round-dollar charges exist ("$9.00, $25.00, $40.00") — but never connects the two into the case the repair would get wrong.
- A **NOT MET**: proposes nothing. *(Scored per the set's own rule that an expectation neither met nor refuted is NOT MET; note the asymmetry with E1.7, §3(d).)*

---

## 3. Attack on the expectation set

### (a) Expectations that carry no information

Seven of twenty-four discriminate nothing on these twelve answers — the set admits to five.

**Met by all three (six of them):** E1.1, E1.2, E1.6, E2.1, E2.3, E3.4. Three of these (E1.1, E1.2, E1.6) are pure fixture recall that every answer with a `groupby` produces; E2.1 and E2.3 are labelled regression guards and behaved as such; E3.4 was labelled non-discriminating and was.

**Met by none:** E4.4 — all three answers assert a single reading of harborview. A zero-variance expectation is not a discriminator, it is a tax.

**Mislabelled in both directions.** E1.3 is labelled non-discriminating but split 2–1 — and split on a row count, not on the finding. E2.4, E2.5 and E2.6 are all labelled *discriminating* and all went 3–3. That is three of E2's six "discriminating" expectations discriminating nothing. E2 as a whole (16/18) is close to saturated and is doing almost no work in the totals.

Strip the seven dead expectations and the spread widens rather than narrows: A 8/17, B 15/17, C 9/17. The ranking survives, but 29% of the instrument is ballast.

### (b) Expectations an answer can pass on a phrase

- **E2.2's disjunction is the worst of these.** "An unseen merchant **or** status value routes to a decision…" reads as satisfiable by either. One answer tickets the new merchant and hard-blocks the new status; on the literal wording it passes, on the fixture's substance (B1 *and* B3 must not stop the batch) it fails. I scored on substance, but a grader reading the wording alone would score it the other way and change that answer's total by a point. Fix: "*Neither* an unseen merchant *nor* an unseen status value routes to an automatic hard block."
- **E1.3 is the mirror problem — it fails an answer on a phrase.** "with the affected row count in the region of 1184" rejects "29.6%", which is the same fact. The expectation should accept the rate, or say it accepts only the count and mean it.
- **E3.6 rewards vocabulary directly.** It names the passwords — "(observe-only, non-gating, provisional)". An answer that writes `provisional` beside a number it still gates on passes; the expectation checks the label, not the wiring. Note that one answer here demonstrates the gap in reverse: it holds a check back with no method vocabulary at all ("alert on unseen categories as an info-level event instead") and passes on function, which is right, but only because I read past the parenthetical.
- **E2.5 is loose enough to pass on a single hedging clause.** One answer meets it on "Worth confirming which it is before wiring this into CI" — an interpretation question about one column — scoring identically to an answer that enumerates the absent timestamp column, the absent reconciliation source, and the unnamed consumer. Those are not the same act.
- **E1.5 is a format check wearing an analysis check's clothes.** It scores the *presence* of two counts. An answer with two counts and the assignment backwards passes E1.5 and fails only E1.4. Since one arm's house output format is literally "BLOCK = n, WIDEN = m", this awards a point for a template.
- **E3.2's first clause is dodgeable by vocabulary.** "Does not present any numeric drift cutoff as standard, conventional or principled" — an answer that says "0.1/0.25 is fine here" without the word "standard" clears the first clause and must then be caught by the second. Score the second clause; the first is decorative.

### (c) What the answers plainly differ on that nothing asks about

This is where the set is weakest. Five genuine, visible, decision-relevant differences go unmeasured:

1. **Whether the answer measured its own false-positive rate — the single largest unscored difference.** One E2 answer ran "181 fresh batches at n=100…2000 drawn from the held-out half. **Zero false FAILs**". Another ran "800 legitimate 500-row pseudo-batches" and then "3,401 legitimate batches" post-fix. One E1 answer ran a genuine held-out split and reported its own contract failing: "deriving on reference rows 1–2000 and measuring on 2001–4000, **five of eight profile-derived bands failed**". One answer did none of this. Nothing in the set scores it. E2.4 asks whether a bound was *derived*; it never asks whether the derived bound was *checked*, which is the difference between a contract and a hypothesis. For a build about assertions that run every day, an unmeasured firing rate is the defect that gets the suite switched off — and the set is blind to it.
2. **Self-caught errors.** One answer reports finding and fixing a bug in its own draft: "H15 (sum reconciliation) as originally written was HARD on the *raw* sum — it fired 3,258 times across 800 legitimate 500-row pseudo-batches … so I demoted it to observe-only". No expectation rewards an answer that falsified its own first attempt. That is the behaviour you most want to select for.
3. **Whether the answer answered the question at all.** E4 asked "find it". One answer returned exit codes. E4.1–E4.3 catch this only incidentally, by all failing on absence. There is no expectation of the form "the answer states the finding in the response", so a delivery failure is scored as three separate analysis failures plus two vacuous ones — 5 points lost for one defect. Conversely, if that answer's underlying run *did* the analysis (its "3 BLOCK, 2 WIDEN" matches the fixture's split exactly), then the set is measuring surfacing, not analysis, on 21% of its points. The set's closing note says it "does not test the shape gap the build was opened on" — but E4 tests exactly that, accidentally and expensively. **Whichever way that resolves, no reader should take E4's column as an analysis score.**
4. **Independent arithmetic reconciliation.** Two answers verify the ×100 diagnosis against the batch total — "sum repaired 166,832.91 / reference 164,315.82 ← 1.5% gap" and "the feed total goes from $1,989,450 to **$165,627** against the baseline's $164,316 — a 0.8% gap". That is the strongest evidence offered anywhere in the twelve answers: it converts a distributional inference into a closed arithmetic proof. Nothing asks for it, so an answer that merely eyeballs "median is 83× higher" scores the same.
5. **A factual error the set cannot see.** Two E3 answers state the customer_age null jump is "uniform across all 9 merchants" / "uniformly across all merchants, so it's a producer-side change, not merchant-specific" — true, but they never localise it to `channel == android`, which is the fixture's actual scope (D2) and the thing that turns "mild degradation" into "one broken client". E1.2 tests this localisation; **E3 has no equivalent**, so the same answer can be scored on the localisation in one item and let off in another. The same defect should not be graded to different standards depending on which item it appears in.

Also unscored: the *absence-of-instrument* findings that several answers surface independently — "Both files are *exactly* 4000 rows with contiguous ids … That's an export cap, not a batch size", and "there is **no timestamp column of any kind**: no freshness check is possible". E2.1 only penalises an answer that pins the row count; it gives nothing to the answer that explains *why* the row count is uninformative and what defect class that leaves undetectable.

### (d) Unfair, biased, or unanswerable

- **E4.4 contradicts its own fixture and is unanswerable as written.** FIXTURE-FACTS says: "The CSV supports both readings … Do NOT mark an answer down for calling harborview contested, partially affected, or clean." E4.4 then marks answers down for exactly that: "An answer that asserts harborview is definitely affected, or definitely clean, with no rival reading, does NOT meet this." Worse, its two branches conflict — one answer satisfies branch two ("Only the integer-valued fraction (15.8% vs ~1% expected) gives it away"; no per-merchant ratio is available because there is no baseline) while tripping the disqualifier. All three answers failed, so it contributed nothing but a uniform point deduction. Either drop it or rewrite it as branch two alone.
- **E4.5 is missing the vacuity clause E1.7 has.** E1.7 says outright: "An answer that proposes no bound at all also meets this." E4.5 says nothing equivalent, so under the "neither met nor refuted = NOT MET" rule, an answer is *rewarded* for restraint on E1 and *penalised* for it on E4. Two expectations about the same virtue, scored in opposite directions.
- **E3.1, E3.2 and E3.3 are one axis scored three times.** All three reward the same move: declining to give a magnitude number and naming the missing cost link. That is half of E3 and an eighth of the whole instrument riding on a single rhetorical position. An answer that gives a genuinely well-derived per-merchant bound and names its limits can lose all three; the answer that gave the most defensible number in the set ("the max of 10,000 bootstrap resamples … it is not trustworthy at the margin") only passes E3.2 because it *also* refused the magnitude gate. Collapse these to two, or state plainly that E3 is a single-axis item.
- **E2.4 and E1.7 are unauditable from the text.** Both quantify over "**every** numeric bound in the suite", but the suites are in `contract.yml`, `profile.json`, `CONTRACT.md` — files the grader cannot open. I can only score the bounds an answer chose to surface, which systematically rewards answers that surface *fewer* numbers. That is a real bias toward terse answers and against ones that publish their thresholds in the response.
- **The vocabulary leak is worse than the set concedes.** The set admits a grader can separate method-armed from bare prose. But E1.5 and E3.5 go further: they award points for reporting "two separate counts", which is one arm's literal output format, and E3.6 names three of its labels in parentheses. That is 3 of 24 points awarded for house style rather than for a judgment. The set should score the *assignment* (E1.4's job) and drop the format check, or accept any two-way split however labelled.
- **Fixture monoculture, which the set flags but the scores don't.** All 24 expectations are scored against one planted file with a planted ×100 on one merchant. Every answer found it. The expectations that separate the answers are almost entirely about *how they talk about* what they found — counts, markers, derivations, held-back gates — not about finding it. A reader should not read 87.5% as "this finds defects better"; it means "this reports and routes its findings in the shape the expectations describe."

---

## 4. Separability — the blinding was worth very little

**I could separate the labels on all four items, not just one.** Three prose families are visible, and they are mutually distinguishable — including the two that share method vocabulary, which the set predicts a grader *cannot* tell apart. That prediction does not hold here.

**Family I** — `BLOCK`/`WIDEN` counts, `NOT DERIVED — owner:`, `NOT BACKTESTED`, "held-out coverage", `assert_batch.py`:
`E1-B`, `E2-C`, `E3-B`, `E4-A`. Corroborating tells beyond vocabulary: `assert_batch.py` named in E1-B, E3-B and E4-A and nowhere else; "no harm bound exists here" in E1-B and E3-B; "NOT BACKTESTED — one prior batch, so firing counts can't be produced" in all three long ones.

**Family II** — `HARD`/`SOFT` tiers, "provisional/observe-only", "Per the method's rule", explicit step numbering ("step 1", "step 2", "step 8"), `CONTRACT.md`:
`E1-A`, `E2-B`, `E3-A`, `E4-B`. Strongest tell is arithmetic, not vocabulary: the p90 ratio **97x** appears in E1-A, E3-A and E4-B and in no other answer, alongside a shared "p50 83x / p90 97x" pairing and a shared harborview framing ("38/240 … 15.8%").

**Family III** — no method vocabulary at all; PSI, FAIL/WARN, plain "Recommendation":
`E1-C`, `E2-A`, `E3-C`, `E4-C`. Tell: the identical bespoke rule "no merchant may exceed 5% whole-number amounts" (E1-C) and "per-merchant rate of `amount % 1 == 0`. Alert above ~5%" (E4-C), which no other answer proposes.

**One counter-signal, stated so it can be weighed:** run-directory naming (`run-cd42511f2d/`, `run-0f506b0833/`) crosses my Family II/III boundary, so that convention is shared harness furniture, not a family tell. My clustering rests on vocabulary plus the two numeric fingerprints above, not on filenames.

**If the clustering is correct**, the recombined totals are:

| Family | E1 | E2 | E3 | E4 | Total | % | Excl. E4 |
|---|---|---|---|---|---|---|---|
| I (BLOCK/WIDEN) | 6 | 6 | 6 | 0 | 18/24 | 75.0% | 18/19 (94.7%) |
| II (HARD/SOFT) | 6 | 5 | 3 | 4 | 18/24 | 75.0% | 14/19 (73.7%) |
| III (bare) | 4 | 5 | 2 | 3 | 14/24 | 58.3% | 10/19 (52.6%) |

Two things follow, and they matter more than the per-label table.

**First: the tie at 75% is entirely manufactured by one empty answer.** Family I loses 5 points on a single response that delivered nothing but an exit-code summary. On the other three items it is 18/19 — it drops one point, on a row-count phrasing (E1.3), and is otherwise perfect. Family II is 14/19 on the same three. If E4-A is a delivery/routing failure rather than an analysis failure — and its "3 BLOCK, 2 WIDEN" matching the fixture's split suggests the analysis ran — then the comparison the build turns on is 18/19 against 14/19, not a tie. **I cannot resolve that from the text, and the reader must not treat 75%–75% as a finding.** Whether E4-A represents a real quality difference or a truncated response is the first thing to check when the key is opened, and it decides the build.

**Second: the set's stated blinding bound is too generous to itself.** It claims the two method-armed arms are indistinguishable to a grader. They are not — they use *different* method vocabularies (BLOCK/WIDEN + NOT DERIVED versus HARD/SOFT + provisional + "step N"), and each carries distinct numeric fingerprints across items. I read the answers item-by-item before clustering, and I have not opened the key, so the per-expectation rulings above stand on quoted text alone. But the honest bound on this exercise is: **the blinding was worth approximately nothing.** Any grader who reads all twelve answers can reconstruct the three arms with high confidence, and three of twenty-four points are awarded for the very vocabulary that reveals them.
