# Blind grading — data-contract-assertions-v2

## 1. Totals

**Labels re-randomise per item. The "Total" row below is an artefact of the shuffle and means nothing until the key is opened.** The per-item rows are the real output.

| Item | A | B | C | Item total |
|---|---|---|---|---|
| E1 | **7** | **7** | **5** | /7 |
| E2 | **6** | **5** | **2** | /6 |
| E3 | **1** | **2** | **6** | /6 |
| E4 | **3** | **4** | **5** | /5 |
| **Across all four (do not read as an arm score)** | **17/24 — 70.8%** | **18/24 — 75.0%** | **18/24 — 75.0%** | /24 |

The per-item cells are what recombine once the key is opened. Section 4 gives a recombination I believe is correct, and it does not look like the row above.

---

## 2. Per-expectation evidence

### E1 — derive a contract, say what today's batch does to it

| # | A | B | C |
|---|---|---|---|
| E1.1 | **MET** — "`amount` unit flip on belltower. All 440 belltower rows are in **cents**: median 2726.50" | **MET** — "B2 \| `amount` in cents while `currency`='USD' \| merchant=belltower" | **MET** — "`belltower` switched from dollars to **cents**. All 440 of its rows are whole numbers" |
| E1.2 | **MET** — "**83.1% of android rows are null** (655 of 788) vs ~1.8% on every other channel" | **MET** — "B4 \| `customer_age` presence collapse \| channel=android \| .0161 (n=806) → **.8312**" | **MET** — "`customer_age` null 1.6% → **83.1% on android alone**" |
| E1.3 | **MET** — "1,184 rows (29.6%) are `\"0 d\"`… the column no longer parses as int" | **MET** — "`settled_days` type break: `\" d\"` suffix on 1184 rows … 4000/4000 bare int → 2816 int + 1184 suffixed" | **MET (marginal)** — "`settled_days` now `\"0 d\"`/`\"1 d\"` on 29.6% of rows … it's serialization, not business". Never states 1184; 29.6% of a file it calls "Exactly 4000 rows" is exactly 1184, so it passes on arithmetic the reader has to do. |
| E1.4 | **MET** — "Four are real breaks; two are business change" … "#4 and #5 are a conversation with the vendor about the closed sets, **not a defect**" | **MET** — "WIDEN (4) … **W1** `harborview` (240 rows) and **W2** `chargeback` (90 rows) **are amendments, not failures**" | **NOT MET** — calls them "Legitimate — needs an amendment", but files both in a table headed **"Breach"** under "**Today's batch is rejected: 7 HARD breaches, 3 SOFT.** Nothing lands." They are on the side that stops the batch. |
| E1.5 | **MET** — headline is a single tally ("11 violations, 4 drift warnings") but is immediately split: "**Four are real breaks; two are business change**", with separate labelled sections "Silent corruption", "New categories — likely legitimate", "Drift, no violation" | **MET** — "## Verdict: BLOCK = 4, WIDEN = 4 … Eight differences, each on exactly one side" | **NOT MET** — "**7 HARD breaches, 3 SOFT.** Nothing lands." One whole-batch verdict; the HARD/SOFT split is severity, not block/widen, and carries no widen count. |
| E1.6 | **MET** — "**Drift, no violation:** … `channel` mix shifted … (PSI 0.06, mild)" | **MET** — filed as "**W4** channel mix" under "WIDEN (4)", i.e. not a break | **MET (marginal)** — "genuinely untriageable … I can't tell a Tuesday from a routing change with n=1". Holds rather than faults it, but does so inside a batch it has already rejected whole. |
| E1.7 | **MET (marginal)** — every number is presented as the reference profile, "From `reference.csv`:", and no tolerance band is invented. See §3(b): the profiled range "1.56–564.33" ships as contract with nothing but the file name behind it. | **MET** — "Two numbers are `NOT DERIVED` and non-gating… **`NOT BACKTESTED — history: one prior batch.`** … every distributional check is held observe-only" | **MET** — "every distributional bound is marked provisional/observe-only … I couldn't derive a row-count band at all" |

**E1: A 7/7 · B 7/7 · C 5/7**

---

### E2 — the assertions to run on every batch

| # | A | B | C |
|---|---|---|---|
| E2.1 | **MET** — "Row count, freshness SLA…: all recorded as `NOT DERIVED`/`SKIP` with the dependency named, not filled with a plausible number" | **MET (by silence)** — no row-count assertion appears anywhere in the text; nothing pins 4000 | **NOT MET** — "**A. Structure** \| … **batch size band (warn)**", and the only derivation offered ("4σ of binomial noise…computed from the actual row count") is how *other* bands scale with n, not where the batch-size band came from |
| E2.2 | **MET** — "new merchant `harborview` … new status `chargeback` … **On their own these ratify the batch, not refuse it** — the suite exits 0 on a widen-only batch" | **NOT MET** — "on `current.csv` it caught 7 HARD + 2 SOFT — … **two new enum values**", against "`assert_batch.py` \| The gate: 33 assertions … **exit 1 on HARD**" | **NOT MET** — "unknown merchant (warn, **escalating to fail above 5% of the batch**)" and harborview is 6%; result: "11 fails … a new `chargeback` status (90), an unknown `harborview` merchant (6%)" |
| E2.3 | **MET** — "`customer_age` null-rate 0.0161 → **0.8312 in `channel=android`** only … The check runs on channel only" | **MET** — "Only the *per-merchant* p50 caught it, at 83x" | **MET** — "**D. Cross-field** \| per-merchant refund rate, per-channel amount median" |
| E2.4 | **MET** — "each carries its derivation: **10.5x** = geometric midpoint between dollars (1.0) and cents (100) … **0.169** = `sqrt(0.0285 × 1.0)` … Everything distributional is observe-only. Capacity bound: `NOT DERIVED`" | **MET** — "structural checks are binding and **every `D*` bound ships PROVISIONAL** (tickets, never pages)", plus two bounds declined with reasons and the physical `[0,120]` named as such | **NOT MET** — derivations are given for the mix/quantile bands, but "tail share >250, soft max 600 (warn) and **hard ceiling 2500** (fail)", "`customer_age` … in 18–**100**" and "fail above **5%**" arrive with no derivation and no non-gating marker (2500 and 5% both gate) |
| E2.5 | **MET** — "no harm signal exists in the feed — no control total, no settlement file, no labelled outcome … Capacity bound: `NOT DERIVED` — needs cadence and a named owner" | **MET** — "the real blocker — **no timestamp column anywhere**. Freshness, staleness SLA … structurally impossible here" | **MET (marginal)** — "cross-batch `txn_id` uniqueness needs state the script doesn't keep; `--prev-max-id` is the cheap stand-in". One named gap, disclosed; meanwhile 2500/600/250/5%/100 ship silently. See §3(b). |
| E2.6 | **MET** — "The two gating numbers are **separators between two discrete candidate states, not drift bands**, and each carries its derivation… Everything distributional is observe-only" | **MET** — "**structural checks are binding** and every `D*` bound ships PROVISIONAL", plus "The assertion is a strict-parse failure count, never a coercion" | **NOT MET** — tiers A/B/C/D separate structure from distribution, but the stated axis is severity ("**Severity split.** Enum violations, malformed values, null-rate and amount-shape drift fail the batch"), which lumps bounded and unbounded checks together; and it puts a bound on an unseen category ("unknown merchant … fail above 5%"), the exact conflation the expectation tests |

**E2: A 6/6 · B 5/6 · C 2/6**

---

### E3 — what threshold should we use

| # | A | B | C |
|---|---|---|---|
| E3.1 | **NOT MET** — the only absence named is history: "I only have this single reference window, so I can't separate seasonal variation from drift". No source mapping distance-moved to downstream cost is mentioned, and a cutoff is shipped anyway. | **NOT MET** — un-derivability is tied to variation, not harm: "**You have one baseline period.** Natural variation is unmeasured, so any distributional threshold I gave you would be a guess with a decimal point on it." Closest is "who consumes this?", which it attaches to tier *action* (fail-loud vs quarantine), not to a magnitude. | **MET** — "**No harm bound exists here.** That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome. Neither CSV contains one." |
| E3.2 | **NOT MET** — ships undreived cutoffs as deployables: "**Gate 2** … Alert when the rate changes by **>2×** *and* **>1pp** absolute", and the step from a measured p99 noise of 0.011 to "**warn 0.02 / alert 0.05**" is never shown. (It does *not* endorse the conventional bands — "Applying 0.1/0.25 per merchant would give you pure false positives" — so it fails on the second clause, not the first.) | **NOT MET** — the headline 5% is fully derived ("Reference max per merchant is 1.64% … That gap is ~60 sigma, needs no history"), but "Back it with a per-merchant **sum** check (**±3x**)" is a distributional cutoff with no derivation and no scope statement | **MET** — "**Cents guard**: `amount ≥500 AND integral` occurs **0 times in 4000** reference rows. Rule of three gives an upper 95% bound of 3/4000 = 0.00075", and what they are/aren't evidence of: "Both are **noise** bounds — they license 'this batch is unusual,' nothing about harm" |
| E3.3 | **NOT MET** — the only dependency named is more of the same data: "If you have several historical windows, calibrate against week-over-week PSI between clean periods instead" | **MET** — "**who consumes this?** I defaulted to fail-loud because `amount` looks financial, but if it feeds a dashboard rather than billing, the soft tier should quarantine instead — stale data would hurt more than slightly-off data" | **MET** — "That needs an independent downstream signal that moves — a control total that reconciles, a bill, a labelled outcome" |
| E3.4 | **MET** — "**Gate 1 — schema and quality. No threshold; any occurrence pages.** - unseen categorical level … - any parse failure on a typed column", and "`channel` … **The only real population drift, and it's under every band**" | **NOT MET** — the channel mix shift is never mentioned at all, so the one genuine distribution shift is not separated from anything; type break and new enums are listed ("Plus: `settled_days` gained a ` d` suffix … there's a new merchant and a new `chargeback` status") without being classed as needing no threshold | **MET** — "**Four of them don't need a drift threshold at all** — they violate things the producer is already committed to, so they're exact assertions with no number to pick", with a "Threshold needed? **No — regex** / **No — declared unit**" column, against "channel mix shift … → observe-only" |
| E3.5 | **NOT MET** — no block/widen assignment and no counts; the structure is Gate 1/2/3 | **NOT MET** — "it's already broken, in five ways" is one tally; no widen side and no counts | **MET** — "**BLOCK: 4 · WIDEN: 3.** Two counts, not one '7 failures' tally" |
| E3.6 | **NOT MET** — all three gates are presented as deployable ("What I'd actually deploy"); nothing is marked observe-only, non-gating or provisional | **MET** — "I've marked those **observe-only** in the contract with **provisional** values, to be re-derived after ~6 clean periods" | **MET** — "The two banded checks are held **observe-only** for routine operation"; "Chargeback rate: `NOT DERIVED — owner: payments risk` … **Non-gating**" |

**E3: A 1/6 · B 2/6 · C 6/6**

---

### E4 — the amount column when column stats look fine

| # | A | B | C |
|---|---|---|---|
| E4.1 | **MET** — "`amount` is a mixed-unit column: 478 rows are in **cents**, the rest in dollars" | **MET** — "**two merchants have `amount` in cents instead of dollars**" | **MET** — "`amount` is arriving in **cents** on 478 of 4000 rows (11.9%)" |
| E4.2 | **MET** — "`belltower` \| 440 / 440 \| **100%** \| p50 ratio **83x**" | **MET** — "`belltower` \| **440 / 440** (all) \| every value is a whole number ending `.0`" | **MET** — "belltower \| 440 \| **1.0000** \| its own prior rate was 0.0104" |
| E4.3 | **MET** — "**Why column-level stats look clean.** The bad rows are 11.9% of the file and all land *above* the median … p50 moves 29.84 → 33.96 … p90 81.23 → 1244.20" | **MET** — "**Why the column stats pass** … only 478 of 4000 rows (12%) are affected and they're pushed entirely into the tail … if your monitoring uses median/IQR … it sees nothing" | **MET** — "**Why the column-level profile passed.** The defect is segment-confined, so the robust statistics barely move: median 29.84 → 33.96 (1.14x) … Only the tail gives it away" |
| E4.4 | **NOT MET** — asserts one reading and explains it: "`harborview` was onboarded with an integration that populates cents for some payment paths". No rival reading for harborview; the one rival it does entertain is for a different merchant ("`northwind` has a whole-number `151.0` … so it's a real value, not cents") | **NOT MET** — asserts affected ("`harborview` \| **38 / 240** (mixed)… Harborview is the worse case: it's a *partial* corruption"). The nearest rival — "a genuine harborview charge of exactly $181.00 would be wrongly divided" — is a failure mode of the repair heuristic, not a rival reading of the merchant, and the separating/non-separating measurement pair is never stated as such. **This is the closest call in the whole set — see §3(b).** | **MET** — "**On harborview — both readings are still open.** The signature fires on belltower and harborview and separates both from the other seven, but it does **not** separate belltower from harborview … harborview has no reference batch at all, so 'a new partner whose large orders are genuinely whole-dollar' can't be excluded from the data in hand" |
| E4.5 | **NOT MET** — proposes the correction ("Correcting the identified rows reconciles the file to the reference at every quantile") but names no case it would get wrong; the northwind note is a case it says it got *right* ("One near-miss I checked and **cleared**") | **MET** — "The `>= 100` guard on harborview is a heuristic, and it's the one weak point: a genuine harborview charge of exactly $181.00 would be wrongly divided, and a cents value below 100 (a sub-$1 charge) would be missed" | **MET** — ships no repair rule ("It blocks either way … One confirmed-clean harborview batch resolves it") and states the case a /100 repair would get wrong: "'a new partner whose large orders are genuinely whole-dollar' can't be excluded" |

**E4: A 3/5 · B 4/5 · C 5/5**

---

## 3. Attack on the expectation set

### (a) Expectations that carried no information in this run

Ten of twenty-four were met by all three answers and discriminated nothing:

**E1.1, E1.2, E1.3, E1.6, E1.7, E2.3, E2.5, E4.1, E4.2, E4.3.**

The set declares five as non-discriminating. In practice it is ten — 42% of the instrument is inert. Two of the ten (**E1.7** and **E2.5**) are declared *discriminating* and were not; both are discussed below, and both fail for the same reason — they can be satisfied by a phrase.

Note also what the ten have in common: E1.1/E1.2/E1.3 and E4.1/E4.2/E4.3 are six points for **finding the planted bugs**, which every answer did. E4 in particular pays three separate points for one finding — belltower, cents, hidden by pooling — so a correct answer banks 3/5 before the two expectations that actually ask anything. E1 pays four (E1.1–E1.3, E1.6) out of seven the same way. The set is weighted heavily toward re-describing the fixture.

**E1.6 is met by inaction.** An answer that never mentions the channel mix at all meets it identically to one that reasons about why it should not gate. E3-B, in fact, omits the channel shift entirely and would have met E1.6 had it been asked there — the same silence costs it E3.4. The set punishes and rewards the same omission depending on which item it lands in.

**E2.1 also rewards silence.** It is a negative expectation, so any answer that simply never proposes a row-count check passes. E2-B met it by not raising the topic; E2-A met it by explicitly recording row count as `NOT DERIVED` with the dependency named. Identical credit for very unequal work.

### (b) Wording that lets an answer pass on a phrase rather than substance

- **E1.7 — "derived from a named input with the derivation shown"**, plus the free pass "An answer that proposes no bound at all also meets this." E1-A ships a profiled min/max as contract (`amount … 1.56–564.33`) under the header "From `reference.csv`:" and passes, because the input is named. But two other items in this very set (E2-A, E3-C, E4-C) demonstrate that a profiled envelope fails held-out coverage — "the obvious auto-derived `amount` min/max envelope covered only **0.9950** — it would have failed 0.5% of a clean batch". E1.7 therefore certifies as "derived" the exact practice E2.4 and E3.2 exist to catch. Naming a file is not showing a derivation, and the expectation should say so.
- **E2.5 — "States what it could NOT derive … naming the missing input."** One instance suffices, and it need not be a number. E2-C passes on a remark about cross-batch `txn_id` state while shipping 2500, 600, 250, 5% and 100 with no provenance — precisely the "supplying a placeholder number silently" the expectation's own second clause names. The expectation should be scoped to the numbers in the suite, or read as universal ("*every* undreived number is marked") rather than existential.
- **E1.3 — "row count in the region of 1184."** E1-C passes on "29.6% of rows" without ever stating a count. If a percentage counts, say so; if it doesn't, E1-C should fail.
- **E1.5 and E3.5 reward a format, not a judgment.** Both are satisfied by a header line ("BLOCK = 4, WIDEN = 4"). E1-A does the same *reasoning* — "Four are real breaks; two are business change", with three separately labelled lists — and passes only because that sentence exists; delete it and an answer with identical content fails on presentation. E3.5 is worse: it asks for block/widen counts in response to a task that asked "what threshold should we use?", so an answer that engages the actual question is docked for not emitting a different deliverable.
- **E4.4's last sentence contradicts its own disjunction.** The requirement is "either reports both readings as open, **or** states which measurement separates it from belltower and which does not." The exclusion then reads as though naming *any* rival reading is enough. E4-B names a rival ("a genuine harborview charge of exactly $181.00 would be wrongly divided") while concluding the merchant is definitely affected. I ruled it NOT MET on the disjunction; under the exclusion sentence read literally it is MET. **This single ambiguity is worth a point on the item with the fewest expectations**, and the expectation should be rewritten to pick one test.
- **E3.2's "only where" clause is absolute and catches good answers.** A single unexplained secondary number sinks it: E3-B's headline threshold is derived to ~60 sigma and it still fails on a parenthetical "±3x"; E3-A's bootstrap is the most serious quantitative work in the twelve answers and it still fails on ">2× and >1pp". Both rulings are correct against the text as written, and both are arguably not what the expectation is *for*. A looser reading flips two verdicts and moves E3 by two points — a third of the item.

### (c) What the answers plainly differ on that nothing asks about — the most valuable findings

1. **Whether the suite false-fires on its own baseline.** Three answers report validating against the reference — "clean on `reference.csv` (0 fail, 0 warn — **no assertion self-fires on its own baseline**)", "clean on `reference.csv` (0 HARD, 0 SOFT)", "fires 0 times on `reference.csv`" — and one reports held-out coverage split across reference halves, catching a check that would fail 2 of 2000 clean rows. Others report nothing of the kind. This is the single most basic quality property of an assertion suite, it is plainly visible in the text, the answers differ on it, and **no expectation asks**. It should be an expectation on E2 and E3.
2. **Whether the whole batch is refused.** "**Nothing lands.**" versus "**The batch is not quarantined whole** — harborview's 202 dollar-denominated rows reconcile cleanly and are accepted." This is the most consequential operational difference between the twelve answers. It is touched only obliquely by E1.4/E1.5, and only on E1 — E3 and E4 answers that refuse everything pay nothing for it.
3. **Internal numerical consistency, and agreement with the file.** On harborview's contaminated rows the answers say 38/240 (15.8%), 38/240 (16%), 38 (0.1583), 39 rows >200, and — in one case — "**35 of 240, 14.6%**" with a median of "35.16" where a sibling answer says 38 and 29.41. FIXTURE-FACTS says 38. Nothing in the set penalises getting a checkable number wrong, and **there is no expectation anywhere that penalises a false claim.** An answer could invent a statistic wholesale and lose zero points. That is the largest hole in the instrument.
4. **False-positive economics.** One answer alone measures PSI's null distribution by segment size and shows that a shared constant is pure noise on small segments — "at merchant-level segments (~450 rows) the noise floor *is* 0.11, and at 200 rows PSI exceeds 0.25 by chance alone." That is real, correct, operationally load-bearing work, and it scores **1/6** on its item because the item's expectations are about a different vocabulary. Whatever the set is measuring, it is not measuring whether the alerting would be usable.
5. **Detection-method critique.** "harborview's median is **35.16, perfectly normal**. A per-merchant p50-ratio check **passes it** while 57% of its value is inflated 100x. Median-based detection assumes the whole segment moved together; partial contamination is invisible to it." Also: "The obvious belltower signatures … **also flag harborview** … They were rejected for that". These are the sharpest analytic moves in the twelve answers. Nothing scores them.
6. **Declining to encode a bound because it would ratify a defect.** "I also declined to encode … `settled_days <= 3` (the hard stop at 3 with no tail looks like an **upstream clamp** — encoding it would **cement a defect as correct**)." One answer, one sentence, and it is the best judgment in the set. Unscored, and E2.4 as written does not reach it.
7. **Whether the answer says what to do next.** "ask the vendor two questions … A per-merchant settlement total from the remittance file is the single artefact that would convert B2/B3 from 'unusual' to 'off by 100× against money actually moved'." Some answers end with a named next action and the artefact that would resolve the open question; others end with a table. Unscored.
8. **Naming what is structurally undetectable.** "**no timestamp column anywhere** … a feed that silently stops updating is currently undetectable"; "there's **no timestamp column anywhere**, so staleness is undetectable — a replayed file is only caught by the id check." Two answers surface a whole class of undetectable failure that the fixture does not plant. E2.5 half-reaches this, but only as "name one missing input", so the answer that names three gets the same point as the answer that names one.

### (d) Unfair, biased, or unanswerable

- **E3 is written in one method's vocabulary and effectively scores conformance to it.** E3.1 ("no available source maps how far a distribution moved to what it cost downstream"), E3.5 ("block-versus-widen assignment with counts"), E3.6 ("observe-only, non-gating, provisional") are not independent tests of answer quality — they are a checklist of one output shape. One answer per item matches that shape almost verbatim, and the set's own preamble concedes the vocabulary is legible to a grader. E3.5 in particular is off-task: the user asked for a threshold, and the expectation requires a block/widen ledger.
- **E2.4 is partly unanswerable from the text.** It says "**Every** numeric bound **in the suite**", but the suites are files I was not given ("33 assertions", "37 assertions", `contract.py`, `assert_batch.py`). I can only score the prose summary. An answer that summarises tersely and an answer that enumerates every bound in the reply are scored on how much they chose to paste, not on what the suite contains. The same objection applies more weakly to E2.1 and E2.6.
- **E1.7's escape hatch is a bias toward brevity.** "An answer that proposes no bound at all also meets this" means the safest way to pass is to say less. Combined with the fact that E1 has no expectation rewarding a usable contract, the item pays for restraint and not for utility.
- **E4.4 was demonstrably written with the answers in view.** Its exclusion clause and the FIXTURE-FACTS' §"A contested figure you must not score against an answer" both read as patches applied after a disagreement the answers themselves surfaced. The provenance note discloses that the expectations were written from the blinded outputs, so this is honest rather than concealed — but it means E4.4 is not independent of the answers it scores, and it is the only expectation on E4 that any answer failed *for a reason other than finding the bug*. E4 is thus one real discriminator plus one ambiguous one, wrapped in three freebies.
- **The [FIXTURE] items are not doing the work the label implies.** They are described as immune to arm output because they come from the CSV. That is true of their *content* but not of their *selection*: choosing to award three separate points for belltower/cents/pooling, and none for false-fire rate or numerical accuracy, is a choice about what matters, and it is the choice that determines the score.

---

## 4. Separability of the labels

**I found the labels separable on all four items — and, worse for the blinding, separable into three clusters that are stable across items.** The set's preamble bounds this as "four of the twelve answers use the method's own vocabulary … A grader can therefore separate a method-armed answer from a bare one." That bound is too generous to the blinding. The twelve answers sort into three groups of four, one per label per item, on prose fingerprints that have nothing to do with the vocabulary disclaimer:

**Cluster α — full method vocabulary: E1-B, E2-A, E3-C, E4-C.** `BLOCK = n / WIDEN = n` as a headline, `NOT DERIVED — owner:`, `NOT BACKTESTED — history: one reference batch`, "held-out coverage", "noise bound … licenses 'this batch is unusual', nothing about harm", explicit rival-reading bookkeeping on harborview. Three of the four also cite the same held-out finding (profiled min/max at 0.9950 / 0.9990 coverage, tested and not shipped).

**Cluster β — partial vocabulary, plus three recurring obsessions: E1-C, E2-B, E3-B, E4-B.** Every one of the four raises at least one of: (i) *no timestamp column* — "no timestamp column anywhere, so staleness is undetectable" / "the real blocker — no timestamp column anywhere" / "If the source system has a per-row timestamp or ingestion batch id"; (ii) *exactly 4000 rows is an export-limit signature* — "Real daily volume doesn't land on a round number" / "the signature of a pagination or export limit"; (iii) *who consumes this?* — "Two things I need from you: who consumes this feed" / "One thing I need from you: who consumes this?", both followed by the same fail-loud-vs-quarantine framing. Uses "PROVISIONAL"/"observe-only" but never the block/widen ledger.

**Cluster γ — no method vocabulary, statistical machinery instead: E1-A, E2-C, E3-A, E4-A.** PSI tables, bootstrap resampling, KS statistics, σ-based bands, dense before/after quantile tables, and a closing offer of further work ("Want me to write this up as a shareable page, or turn the three gates into a runnable check script?", "Two design choices worth your sign-off"). Distinctive tic: an explicitly checked-and-cleared near-miss ("One near-miss I checked and cleared: `northwind` has a whole-number `151.0`").

Recombining my per-item scores by cluster:

| Cluster | E1 | E2 | E3 | E4 | Total |
|---|---|---|---|---|---|
| α | 7/7 | 6/6 | 6/6 | 5/5 | **24/24 — 100%** |
| β | 5/7 | 5/6 | 2/6 | 4/5 | **16/24 — 66.7%** |
| γ | 7/7 | 2/6 | 1/6 | 3/5 | **13/24 — 54.2%** |

I am not going to guess which cluster is which arm, and the mapping above is my clustering, not the key. But two things follow regardless of how the key reads.

First, **the blinding bought less than the preamble claims.** The disclaimer covers vocabulary; the separation I got came mostly from non-vocabulary habits — the timestamp remark, the 4000-rows remark, the "who consumes this" ask, the offer of follow-up work. Any grader reading four items in sequence will cluster these, and the per-item re-randomisation does not prevent it, because the clustering is done on prose and then applied across items.

Second, **a cluster scoring 24/24 against an expectation set written in that cluster's own vocabulary is not a measurement, it is a mirror.** Four expectations (E1.5, E3.1, E3.5, E3.6) can be met by reproducing a specific output shape, and one cluster reproduces it every time. Before treating 100% as a result, I would want the E3 block rewritten in neutral terms — ask what the answer *establishes* about the threshold question, not whether it emitted a block/widen ledger — and I would want the four unscored differences in §3(c), especially **does the suite false-fire on its own baseline** and **are the stated numbers actually right**, added as expectations. On the current instrument, an answer can score 24/24 while never once being checked for being correct.
