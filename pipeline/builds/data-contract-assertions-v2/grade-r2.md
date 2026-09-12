# Blinded grading report — data-contract-assertions-v2

**Labels re-randomise per item.** The "total" column below is therefore *not* an arm score. It is only meaningful as a bookkeeping check; the per-item cells are the recombinable unit.

## 1. Scores

| Label | E1 (/7) | E2 (/6) | E3 (/6) | E4 (/5) | Total (/24) | % |
|---|---|---|---|---|---|---|
| **A** | 6 | 6 | 1 | 4 | **17** | **70.8%** |
| **B** | 7 | 5 | 3 | 4 | **19** | **79.2%** |
| **C** | 5 | 2 | 6 | 5 | **18** | **75.0%** |

Per-item, for recombination once the key is opened:

| Item | A | B | C |
|---|---|---|---|
| E1 | 6/7 (85.7%) | 7/7 (100%) | 5/7 (71.4%) |
| E2 | 6/6 (100%) | 5/6 (83.3%) | 2/6 (33.3%) |
| E3 | 1/6 (16.7%) | 3/6 (50%) | 6/6 (100%) |
| E4 | 4/5 (80%) | 4/5 (80%) | 5/5 (100%) |

The spread within a label across items (A ranges 16.7%→100%) is larger than the spread between labels overall, which is exactly what re-randomisation should produce and is the reason the total column must not be read as a ranking.

---

## 2. Per-expectation evidence

### E1 — derive a contract, say what today's batch does to it

| # | A | B | C |
|---|---|---|---|
| E1.1 | **MET** | **MET** | **MET** |
| E1.2 | **MET** | **MET** | **MET** |
| E1.3 | **MET** | **MET** | **MET** |
| E1.4 | **MET** | **MET** | **NOT MET** |
| E1.5 | **MET** | **MET** | **NOT MET** |
| E1.6 | **MET** | **MET** | **MET** |
| E1.7 | **NOT MET** | **MET** | **MET** |

**E1.1** — A: "`amount` unit flip on belltower. All 440 belltower rows are in **cents**: median 2726.50". B: "`amount` in cents while `currency`='USD' | merchant=belltower". C: "`belltower` switched from dollars to **cents**. All 440 of its rows are whole numbers".

**E1.2** — A: "Null rate 1.4% → **17.8%**, and it is not random: **83.1% of android rows are null** (655 of 788)". B: "`customer_age` presence collapse | channel=android | .0161 (n=806) → **.8312** (n=788)". C: "`customer_age` null 1.6% → **83.1% on android alone**".

**E1.3** — A: "1,184 rows (29.6%) are `"0 d"`... the column no longer parses as int". B: "`settled_days` type break: `" d"` suffix on 1184 rows | 4000/4000 bare int → 2816 int + 1184 suffixed". C: "`settled_days` now `"0 d"`/`"1 d"` on 29.6% of rows" — C gives the share, not the count; 29.6% of the 4000 rows it states elsewhere is 1184, and the quoted string form carries the parse break. Scored MET on substance; see §3(b), this is the expectation's wording doing the work rather than C's.

**E1.4** — A: "New categories — likely legitimate... #4 and #5 are a conversation with the vendor about the closed sets, **not a defect**." B: "WIDEN (4) — extends a set the producer never closed... `harborview` (240 rows) and `chargeback` (90 rows) are **amendments, not failures**... The onboarding batch is not refused." C: **NOT MET** — C does call them "Legitimate — needs an amendment", but they sit inside a table whose column header is "Breach", under the verdict "**Today's batch is rejected: 7 HARD breaches, 3 SOFT.** Nothing lands." They are on the side that stops the batch, which the expectation explicitly excludes.

**E1.5** — A: "**11 violations, 4 drift warnings.** Four are real breaks; **two are business change**", with three separately headed lists ("Silent corruption", "New categories — likely legitimate", "Drift, no violation"). B: "**Verdict: BLOCK = 4, WIDEN = 4**". C: **NOT MET** — "7 HARD breaches, 3 SOFT" is a severity split of a single failure tally, closed by one whole-batch verdict ("Nothing lands"), not a block-vs-widen count.

**E1.6** — A: "**Drift, no violation:** `channel` mix shifted... (PSI 0.06, mild)". B: filed under WIDEN as "**W4** channel mix", and "The channel-mix band (0.06) is the weakest number in the file". C: "genuinely untriageable for this reason — I can't tell a Tuesday from a routing change with n=1" — not treated as a defect.

**E1.7** — A: **NOT MET.** A publishes a contract table of numeric bounds ("`amount` USD dollars, 2dp, **1.56–564.33**, median 29.84, p99 210.64"; "`customer_age` int 18–78, nullable at **1.4%**") with no derivation beyond their being reference observations, and renders drift verdicts against an unstated band — "(PSI 0.06, **mild**)", "non-harborview merchant mix (PSI 0.003)" under "Holding fine". No not-derived or non-gating marker appears anywhere in the answer. B: "Two numbers are `NOT DERIVED` and non-gating: the capacity bound... and row_count (two data points is not a range)", plus "**Profiled min/max was tested and not shipped** — `amount between [1.56, 499.68]` scores 0.9990 on held-out *clean reference data*". C: "every distributional bound is marked provisional/observe-only... I couldn't derive a row-count band at all", and the gating checks are justified as bound-free: "they trip only on power-of-ten shifts... they need no calibrated band."

### E2 — the assertions to run on every batch

| # | A | B | C |
|---|---|---|---|
| E2.1 | **MET** | **MET** | **NOT MET** |
| E2.2 | **MET** | **NOT MET** | **NOT MET** |
| E2.3 | **MET** | **MET** | **MET** |
| E2.4 | **MET** | **MET** | **NOT MET** |
| E2.5 | **MET** | **MET** | **NOT MET** |
| E2.6 | **MET** | **MET** | **MET** |

**E2.1** — A: "Row count, freshness SLA (no timestamp column exists), FK-to-merchant-master, cross-batch replay: all recorded as `NOT DERIVED`/`SKIP` with the dependency named". B: MET by absence — no row-count assertion appears anywhere in the answer. C: **NOT MET** — Tier A includes "**batch size band (warn)**" and no derivation for that band is given; the "Bands scale with batch size" paragraph explains the mix/null/quantile bands, not the batch-size band itself.

**E2.2** — A: "**WIDEN** — extends a set never committed closed: new merchant `harborview` (240 rows), new status `chargeback` (90 rows)... **On their own these ratify the batch, not refuse it** — the suite exits 0 on a widen-only batch." B: **NOT MET** — "on `current.csv` it caught **7 HARD** + 2 SOFT — a dollars→cents switch on one merchant, **two new enum values**, and a 29.6% format corruption", against a gate described as "exit 1 on HARD". C: **NOT MET** — "unknown merchant (warn, **escalating to fail above 5% of the batch**)" with harborview at 6.0%, and status under "closed enums" where "Enum violations... fail the batch"; the run reports "a new `chargeback` status (90), an unknown `harborview` merchant (6%)" among "11 fails".

**E2.3** — A: "`customer_age` null-rate 0.0161 → **0.8312 in `channel=android`** only... The check runs on channel only". B: "Only the *per-merchant* p50 caught it, at 83x". C: "**D. Cross-field** | per-merchant refund rate, per-channel amount median — both catch a single bad source that the batch-level aggregate hides".

**E2.4** — A: "each carries its derivation: **10.5x** = geometric midpoint between dollars (1.0) and cents (100)... **0.169** = `sqrt(0.0285 × 1.0)`... Everything distributional is observe-only. Capacity bound: `NOT DERIVED` — needs cadence and a named owner." B: "structural checks are binding and every `D*` bound ships **PROVISIONAL** (tickets, never pages) until real batch history accumulates", with the one HARD numeric bound sourced ("HARD is the physical [0,120]; the observed range is SOFT"). C: **NOT MET** — "soft max 600 (warn) and **hard ceiling 2500** (fail)", "tail share >250", "`customer_age` blank-or-int in **18–100**", "escalating to fail **above 5%**" all appear without derivation or marker, against a stated profile whose max is 564.33 and whose age range is 18–78.

**E2.5** — A: "no control total, no settlement file, no labelled outcome... all recorded as `NOT DERIVED`/`SKIP` **with the dependency named**, not filled with a plausible number". B: "One file, no reconciliation, and — the real blocker — **no timestamp column anywhere**. Freshness, staleness SLA, and like-with-like period comparison are structurally impossible here". C: **NOT MET** — the nearest is "cross-batch `txn_id` uniqueness needs state the script doesn't keep; `--prev-max-id` is the cheap stand-in", which is a script limitation it then solves; nothing in C names an input it lacked for a bound, and 2500 / 600 / 250 / 100 / 5% are supplied without provenance, which is the alternative the expectation excludes.

**E2.6** — A: "The two gating numbers are **separators between two discrete candidate states, not drift bands**... Everything distributional is observe-only" — weakest of the three, since A's gating checks all carry numbers. B: "**structural checks are binding** and every `D*` bound ships PROVISIONAL". C: the tier table separates "B. Field validity" (formats, uniqueness, closed enums) from "C. Distribution" (bands, quantiles, tail share).

### E3 — what threshold should we use

| # | A | B | C |
|---|---|---|---|
| E3.1 | **NOT MET** | **NOT MET** | **MET** |
| E3.2 | **NOT MET** | **MET** | **MET** |
| E3.3 | **NOT MET** | **MET** | **MET** |
| E3.4 | **MET** | **NOT MET** | **MET** |
| E3.5 | **NOT MET** | **NOT MET** | **MET** |
| E3.6 | **NOT MET** | **MET** | **MET** |

**E3.1** — A: **NOT MET.** The nearest text is "I only have this single reference window, so I can't separate seasonal variation from drift. The thresholds above are **calibrated to sampling noise only**" — that names an absence of *history*, not the absence of a source mapping distributional movement to downstream cost. B: **NOT MET** — "**You have one baseline period.** Natural variation is unmeasured, so any distributional threshold I gave you would be a guess with a decimal point on it" is again the noise/history absence, not the harm-map absence. C: **MET** — "**No harm bound exists here.** That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome. Neither CSV contains one. Nothing in this contract licenses 'past here something downstream is wrong.'"

**E3.2** — A: **NOT MET.** A both invokes and endorses the convention: "barely over the **conventional 0.1 'investigate' line**" and "The **familiar 0.1 / 0.25 bands are only meaningful at full file size** — there your p99 noise is 0.011, so 0.1 is a ~10× margin". Its own proposal — "**warn 0.02 / alert 0.05** at full-file size" — does not show how 0.02 and 0.05 follow from the measured p99 of 0.011. B: **MET** — the headline number carries its derivation and its limits: "Reference max per merchant is 1.64%; belltower is 100%, harborview 15.8%... That gap is ~60 sigma, **needs no history, and doesn't drift seasonally** — so unlike a distributional band, you can enable it today", and nothing is presented as convention. C: **MET** — "Both are **noise** bounds — they license 'this batch is unusual,' **nothing about harm**", with derivation: "2000 bootstrap resamples of the reference null indicator... p99.5 = 0.0187 at n=4000", "Rule of three gives an upper 95% bound of 3/4000 = 0.00075".

**E3.3** — A: **NOT MET.** A names only a data gap ("If you have several historical windows, calibrate against week-over-week PSI between clean periods instead"); no consumer, no cost, no downstream signal. B: **MET** — "**who consumes this?** I defaulted to fail-loud because `amount` looks financial, but if it feeds a dashboard rather than billing, the soft tier should quarantine instead... That's the one call in the contract I couldn't make for you." C: **MET** — "That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome", plus "`NOT DERIVED — owner: payments risk.`"

**E3.4** — A: **MET** — "**Gate 1 — schema and quality. No threshold; any occurrence pages.** - unseen categorical level... - any parse failure on a typed column", and "`channel` | 0.060 | **The only real population drift, and it's under every band.**" B: **NOT MET** — B collapses everything into "it's already broken, in five ways" and never identifies the genuine distribution shift; the channel mix does not appear in the answer at all. C: **MET** — "**Four of them don't need a drift threshold at all** — they violate things the producer is already committed to, so they're exact assertions with no number to pick", table column "Threshold needed? | **No** — regex | **No** — declared unit", with "channel mix shift... no category added or dropped → observe-only".

**E3.5** — A: **NOT MET** — no block/widen counts; the structure is Gate 1/2/3. B: **NOT MET** — "broken, in five ways" is a single tally; the new merchant and status appear in a trailing "Plus:" sentence with no widen side and no count. C: **MET** — "**BLOCK: 4 · WIDEN: 3.** Two counts, not one '7 failures' tally."

**E3.6** — A: **NOT MET** — all three gates are presented under "What I'd actually deploy" with no observe-only, non-gating or provisional marker on any of them. B: **MET** — "I've marked those **observe-only** in the contract with **provisional** values, to be re-derived after ~6 clean periods." C: **MET** — "**Non-gating.**", "The two banded checks are held **observe-only** for routine operation", "channel mix shift... → **observe-only**".

### E4 — the amount column, when column statistics look fine

| # | A | B | C |
|---|---|---|---|
| E4.1 | **MET** | **MET** | **MET** |
| E4.2 | **MET** | **MET** | **MET** |
| E4.3 | **MET** | **MET** | **MET** |
| E4.4 | **NOT MET** | **NOT MET** | **MET** |
| E4.5 | **MET** | **MET** | **MET** |

**E4.1** — A: "`amount` is a **mixed-unit column**: 478 rows are in **cents**, the rest in dollars". B: "two merchants have `amount` in **cents instead of dollars**". C: "`amount` is arriving in **cents** on 478 of 4000 rows".

**E4.2** — A: "| `belltower` | 440 / 440 | **100%** | p50 ratio **83x**". B: "| `belltower` | **440 / 440** (all) | every value is a whole number". C: "| belltower | 440 | **1.0000** | its own prior rate was 0.0104".

**E4.3** — A: "**Why column-level stats look clean.** The bad rows are 11.9% of the file and all land *above* the median... p50 moves 29.84 → 33.96", with a reference/current/corrected quantile table. B: "**Why the column stats pass** — Quantile checks look clean because only 478 of 4000 rows (12%) are affected and they're pushed entirely into the tail... if your monitoring uses median/IQR... it sees nothing." C: "**Why the column-level profile passed.** The defect is segment-confined, so the robust statistics barely move: median 29.84 → 33.96 (1.14x)... Only the tail gives it away — p90 15.3x".

**E4.4** — A: **NOT MET.** Harborview is asserted affected with no rival reading: "This is what **separated harborview's 38 contaminated rows** from its 202 good ones", and the causal claim "`harborview` was onboarded with an integration that populates cents for some payment paths". B: **NOT MET.** Also asserted: "| `harborview` | **38 / 240** (mixed) | integral values only, all ≥ 181; the other 202 rows are correct". B's later caveat is about the repair heuristic on individual rows ("a genuine harborview charge of exactly $181.00 would be wrongly divided"), not a rival reading of the merchant, and B never states a measurement that fails to separate harborview from belltower. C: **MET** — "**On harborview — both readings are still open.** The signature fires on belltower and harborview and separates both from the other seven, but it does **not** separate belltower from harborview... harborview has no reference batch at all, so 'a new partner whose large orders are genuinely whole-dollar' **can't be excluded from the data in hand**."

**E4.5** — A: **MET**, on the narrow reading — A surfaces the class of value that defeats its whole-number criterion and gives the boundary: "One near-miss I checked and cleared: `northwind` has a whole-number `151.0`, but the reference contains **legitimate round amounts up to `211.00`**, so it's a real value, not cents." B: **MET**, and most explicitly: "The `>= 100` guard on harborview is a heuristic, and it's the one weak point: a genuine harborview charge of exactly $181.00 would be wrongly divided, and a cents value below 100 (a sub-$1 charge) would be missed." C: **MET** — against "Dividing the flagged rows by 100 reconciles them exactly", C carries "'a new partner whose large orders are genuinely whole-dollar' can't be excluded from the data in hand."

---

## 3. Attack on the expectation set

### (a) Expectations carrying no information

Eight of twenty-four were met by all three answers and zero were met by none:

E1.1, E1.2, E1.3, E1.6, E2.3, E4.1, E4.2, E4.3.

Two further points are near-degenerate: E2.6 was met by all three, and E4.5 was met by all three. That is **ten of twenty-four points — 42% of the instrument — that separated nothing.** The effective instrument is fourteen points, and three of those fourteen (E1.4, E1.5, E3.5) test one property.

**The set miscounts itself.** The closing note says "Five of the twenty-four expectations are marked non-discriminating." The table marks **nine**: E1.1, E1.2, E1.3, E1.6, E2.3, E3.4, E4.1, E4.2, E4.3. The declared non-discriminating share is 37.5%, not 21%. Whoever writes the build report will draw the wrong conclusion about how much of the margin rests on live expectations if they take the footer at face value.

**The kind labels are wrong in both directions.** E3.4 is marked "non-discriminating" and was the only E3 expectation that B failed — it discriminated. E2.6, E4.1, E4.2, E4.3 and E4.5 are the reverse: E4.5 is marked "discriminating" and discriminated nothing.

### (b) Wording that lets an answer pass on a phrase

1. **E1.7 is defeated by a profile dump.** "Derived from a named input with the derivation shown" is satisfied by "From `reference.csv`:" followed by observed min/max. That is precisely the un-tested envelope that two other answers demonstrate fails on clean data (`amount between [1.56, 499.68]` at 0.9990 held-out; the min/max envelope at 0.9950). The expectation cannot tell "derived" from "observed once and asserted". I scored A NOT MET on this only because of its unbanded PSI verdicts ("PSI 0.06, mild"; "PSI 0.003" filed under "Holding fine"), not because of the contract table — a different grader would rule the other way on the same text, which means E1.7 is not reliably scoreable.

2. **E1.3 never requires the count it names.** "Row count in the region of 1184" is satisfied by "29.6% of rows" in a file the answer elsewhere states has 4000 rows. The expectation asks for a number and accepts a ratio.

3. **E2.4, E3.6, E1.7 and E2.5 are keyword detectors.** E3.6 literally enumerates the passing tokens — "observe-only, non-gating, provisional". An answer that achieves the identical restraint in other words fails: A's "The thresholds above are calibrated to sampling noise only" is a non-gating disclosure and scores zero. This matters more than usual here because **the set's own preamble names those same tokens as the marker that identifies a method-armed arm.** Four expectations therefore award points for the vocabulary the preamble concedes is a tell. That is not measurement, it is a marker check.

4. **E2.1 rewards silence.** B meets it by never mentioning row count at all. An answer that thought about row count and declined to bound it, and one that never considered it, score the same.

5. **E2.4 and E2.5 are close to the same point twice.** Every answer that failed one failed the other; no answer split them. Likewise E3.1/E3.2/E3.3 are three phrasings of "did you say a magnitude threshold can't be sourced from this feed", and E1.5/E3.5 are the same block-vs-widen-counts test asked in two items. Roughly five of the fourteen live points are duplicates, which means a single behaviour moves the total by up to 21 percentage points.

### (c) What the answers plainly differ on that nothing asks about — the most valuable gap

1. **Whether the suite was run against its own baseline.** Some answers report a self-firing test — "clean on `reference.csv` (0 fail, 0 warn — **no assertion self-fires on its own baseline**)", "the runner... **fires 0 times on `reference.csv`**", "held-out coverage (derived on reference rows 1–2000, measured on 2001–4000)" — and some report nothing of the kind. A contract suite that fires on its own reference is worthless, and this is the cheapest possible check. **No expectation asks.** This is the single biggest omission in the set; it is objective, binary, and readable from every answer.

2. **Numerical accuracy and self-consistency are entirely unscored.** The answers disagree with each other and, in one case, with themselves, on the fixture's own facts:
   - harborview affected rows: "38 / 240" (five answers) vs "**35 of 240**, 14.6%" (E3-B) vs "39 rows >200, of which 37 are whole-valued" (E2-A).
   - harborview median: "35.00" (E1-C) vs "**35.16**" (E3-B) vs 29.41 / 29.68 (its fractional subset, elsewhere).
   - belltower current median: 2726.50 (key: 2726.5) vs "**2729**" (E3-B) vs "32.80 → 2726.50" (E3-A, which also misstates the reference segment median as 32.80 against the key's 32.75).
   - Overstatement factor: "~12x" / "12.1x" / "inflated ~11.9x" across most answers, but E3-B says "a **6.6x** overstatement of transaction value" while its own figures — stated 1,989,449.64 → corrected 303,128.19 — give 6.56x against its *corrected* total and 12.1x against the reference total of 164,315. The answer contains both framings and reconciles neither.
   - E4-C states "`customer_age` nulls went 1.4% → 17.8% **uniformly across all nine merchants**" — true per merchant, but in an answer that never mentions the android channel, a reader would take the defect as unsegmented, which is the opposite of the finding.
   
   An answer can score 100% on this instrument while being wrong about the numbers. That is the failure mode the instrument most needs to catch and does not.

3. **Which segmentation is the *wrong* one.** Two answers volunteer that the merchant cut is a trap for the null-rate finding — "viewed per *merchant*, B4 shows all nine merchants elevated (.1416–.2004). **The merchant cut is the wrong segmentation** and would have produced nine findings instead of one"; "by merchant it separates nothing — all nine merchants sit at 0.142–0.200". E2.3 only asks that *some* per-segment check exist, which all three answers pass trivially. Naming the segmentation that produces nine spurious findings is a strictly harder and more useful behaviour, and it is invisible to the set.

4. **The fixture's synthetic signature.** Two answers refuse a row-count bound because "Exactly 4000 rows, `txn_id` perfectly contiguous T000000–T003999 with zero gaps... That's the **export-limit signature**" and "A round number on both sides is the signature of a pagination or export limit, not a real volume". Others silently ship or omit a batch-size band. Nothing asks — and E2.1 half-credits the outcome without noticing the reasoning.

5. **Structurally impossible checks.** "**No timestamp column anywhere**, so staleness is undetectable — a replayed file is only caught by the id check" appears in three answers and is arguably the largest standing hole in any contract built here. No expectation touches freshness, staleness, or replay.

6. **Consumer-side breakage that no assertion can see.** "nothing in the batch is wrong about `chargeback`, but a consumer whose revenue sum has no chargeback branch is now wrong, and no assertion here can see it"; "if a downstream `status` mapping has an `else` branch, chargebacks may be landing in it silently right now." This is the only place any answer reasons past the file to the consumer of the file. E3.3 rewards it in E3 alone; in E1, E2 and E4 it is free.

7. **Bounds declined because they would cement a defect.** "`settled_days <= 3` (the hard stop at 3 with no tail looks like an **upstream clamp** — encoding it would cement a defect as correct)" and "there's no `pending ⇒ settled_days == 0` rule, because the reference itself has 153 pending and 42 refunded rows with non-zero settled_days — asserting it would fire on your own baseline." Two different, genuinely sophisticated reasons for *not* writing an assertion. Neither is scoreable anywhere in the set.

### (d) Unfair, biased, or unanswerable

1. **Five of twenty-four points ride on one output format.** E1.4, E1.5, E2.2, E2.6 and E3.5 all reward a two-sided BLOCK/WIDEN ledger with counts on both sides. An answer that reaches the identical triage in prose is penalised: C's E1 says "Legitimate — needs an amendment" and "I left the two legitimate changes as *proposed, unapplied* amendments — no approver, no effective date", which is substantively the correct disposition, and loses two points because the disposition sits inside a "Breach" table under a whole-batch reject. That may be the right call — a reject is a reject — but E1.5 in particular scores presentation, not judgment, and it is the presentation the preamble identifies as the method's own. **21% of the instrument is a house-style check.**

2. **E4.5 has no null case; E1.7 does.** E1.7 says "An answer that proposes no bound at all also meets this." E4.5 has no equivalent, so an answer that correctly declines to repair — "It **blocks either way**... One confirmed-clean harborview batch resolves it" — is left to the grader's discretion. I ruled it MET; the text does not say I should have.

3. **E3.1 is not reliably decidable.** "Or names that absence in its own words" required me to rule on whether "calibrated to sampling noise only" and "any distributional threshold I gave you would be a guess with a decimal point on it" name the *harm-map* absence or merely a *history* absence. I ruled they do not, because the expectation specifies which absence. Two competent graders will split on this, and it is one of the two points labelled "THE NAMED AXIS" — the least robust wording sits on the most load-bearing point.

4. **E2.1 and E2.4 are unanswerable from the text.** They quantify over "the suite" and "every numeric bound in the suite", but the artefacts are 33, 34 and 37 assertions living in files the grader cannot see. I scored summaries. An answer is rewarded for describing fewer of its own bounds, which is a perverse incentive: the most transparent answer exposes the most surface to E2.4.

5. **The fixture note protects harborview in E4 and nowhere else.** FIXTURE-FACTS forbids scoring the harborview reading and E4.4 correctly converts that into a test of *handling*. But the answers reason about harborview in E1, E2 and E3 as well — "The harborview verdict is decided by where the bound is put, not by the data", "it's filed WIDEN with the rival reading recorded and the bound observe-only", "I held the 38 rows, not the merchant" — and in those three items the same behaviour earns nothing. The set's best-designed expectation is applied to a quarter of the evidence for it.

---

## 4. Separability — where the blinding failed

**The blinding failed in all four items, and it failed further than the preamble concedes.**

The preamble's bound is: four of twelve answers carry the method's vocabulary, so a grader can separate method-armed from bare, but cannot separate the two method-armed arms from each other. The first half is correct and understates the problem; the second half I believe is **false**, and that is the finding that matters.

**Cluster α — full ledger vocabulary.** E1-B, E2-A, E3-C, E4-C. Markers: an explicit "BLOCK n · WIDEN n" headline with the phrase "two counts, not one tally"; `NOT DERIVED — owner:`; `NOT BACKTESTED — history: one reference batch`; "held-out coverage" on a 50/50 reference split with a coverage figure to four decimals (0.9990, 0.9950, 1.0000); and a signature move of holding a rival reading open in place ("both readings stay open", "I held the 38 rows, not the merchant", "the bound's value is not load-bearing"). Exactly one per item. Unmistakable.

**Cluster β — tiered contract, second consistent style.** E1-C, E2-B, E3-B, and most likely E4-B. Markers, all recurring and none shared with α: HARD/SOFT severity tiers with "exit 1 on HARD"; the word PROVISIONAL rather than observe-only-plus-NOT-DERIVED; a closing request to the reader phrased as "**who consumes this feed / who consumes this?**" with the same fail-loud-versus-quarantine reasoning verbatim across E2 and E3; "**no timestamp column anywhere**" as a named structural blocker; and the "**exactly 4000 rows on both sides is a pagination or export-limit signature**" observation, which appears in E1-C and E3-B in nearly the same words and in no α or γ answer. E4-B is the weakest assignment — E4 gives this style nothing to hang a contract on — but its "If the source system has a per-row timestamp or ingestion batch id, keying off that would be exact" carries the same timestamp preoccupation.

**Cluster γ — analyst prose, no contract vocabulary.** E1-A, E2-C, E3-A, and by elimination E4-A. Markers: PSI and quantile tables with a "corrected" column; bootstrap resampling presented as the answer's own methodological contribution; profile tables presented directly as "the contract"; explicit invocation of conventional bands ("the conventional 0.1 'investigate' line", "the familiar 0.1 / 0.25 bands"); and a closing offer of further work ("Want me to write this up as a shareable page, or turn the three gates into a runnable check script?").

**What gave it away, ranked by strength:** (1) the recurring reader-question "who consumes this feed", identical in framing across β's E2 and E3; (2) the export-limit observation about 4000 rows, a distinctive and non-obvious remark repeated across β's E1 and E3; (3) `NOT DERIVED — owner:` and `NOT BACKTESTED — history:` as literal tokens in α; (4) held-out coverage reported as a four-decimal figure, α only; (5) the HARD/SOFT versus BLOCK/WIDEN axis, which cleanly splits β from α.

**Consequence.** I could assign 11 of 12 answers to a consistent source cluster, and the twelfth (the E4 α-versus-β-versus-γ split) only because E4 strips the answers of their contract scaffolding. If β is the second method-armed arm, the preamble's central claim — that the comparison deciding this build is blind — does not hold: β's markers are as distinctive as α's, just different. If β is not a method arm, then three of the twelve answers I read carry a coherent house style that the preamble does not account for at all. Either way, the label re-randomisation is doing almost no work; the prose is the key.

For the record on my own grading: I graded each item in file order, A then B then C, against the expectation text, and the resulting per-item scores do not follow the clusters monotonically — α scores 7/7, 6/6, 6/6, 5/5 across the four items and β scores 5/7, 5/6, 3/6, 4/5, but γ beats β in E2 by four points and loses to it in E1 and E3. If I were scoring the clusters rather than the text, that pattern would be smoother than it is.
