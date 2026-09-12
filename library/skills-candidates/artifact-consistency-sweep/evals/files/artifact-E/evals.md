# Evals — data-contract-assertions

**Talent:** `data-contract-assertions` · **Type:** technique · **Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result is materially
better and meets the pass criterion. Authored by an INDEPENDENT tester (not the skill author);
scenarios are written against the file's ACTUAL steps, tables and rules — line-cited — not
against its self-description.

**Blend:** 13 scenarios — 6 `application (normal)`, 6 clever (5 `pressure`, 1 `edge`),
1 `negative-trigger`. 46% normal, per CURATION-LESSONS ACTIVE DIRECTIVES (library was at 32%).
Normal scenarios end with a plain **PASS**: a capable baseline should often pass them, and
claiming a baseline win there is the rubber stamp these suites exist to prevent.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 6 normal / 6 clever / 1 negative-trigger.
- [x] **Specific to this talent** — every scenario cites a concrete step, table row or rule.
- [x] **Observable pass/fail criterion** — each is a checkable line, no "looks good".
- [x] **Clever scenarios designed so baseline plausibly FAILS** — S7–S12.
- [x] **Matches talent type** — technique → APPLICATION scenarios for the normals.
- [x] **Negative trigger covered** — exactly one (S13).
- [x] **Dead cross-refs / invented commands / `name:` / portability / tier-routing** — see Structural review.
- [x] **Dogfood: applied to this repo's own data** (S12) — the talent's method run against
      `pipeline/metrics.jsonl`, with the profile computed, not quoted from the talent.

## Scenarios

## S1 — Nightly vendor feed, snapshot to assertion · application (normal)
- **Input:** `vendor_orders.csv` lands nightly ~06:00 in S3; 9 columns; ~42,000 rows/night;
  90 nightly files retained. Consumers: a revenue dashboard and a monthly finance export.
  Nothing validates it today. "Set up data quality checks on this feed."
- **Pass criterion (observable):** The answer, in order: (i) writes the step-1 consumer line
  ("consumer = dashboard + finance export; a bad batch costs X; stale costs Y") BEFORE any
  check; (ii) picks a multi-period snapshot (all 90 files / ≥ 12 weeks, spanning two weekly
  cycles) rather than one night (step 2 bullet 1); (iii) profiles per column / per table /
  per batch per the step-3 table, **per period not pooled**; (iv) emits a contract split into
  HARD and SOFT (step 4); (v) asserts on the landed raw batch before any transform or write
  (step 5). Fails if a single night is profiled, if the checks are only schema/null-shaped, or
  if the assertion runs after the load merges.
- **Baseline (without talent):** Produces a reasonable but schema-heavy answer — not-null,
  type, maybe `unique(order_id)` — usually derived from one recent file, and typically placed
  in the transform layer where it runs after the merge. Volumetric and distributional checks
  are thin or absent.
- **With talent:** Step 1 fixes the stakes first. Step 2 takes 90 files. Step 3's table forces
  digit-length/quantile profiling per night, so natural variation is visible. Step 4 sorts
  `order_id` uniqueness, `qty >= 0`, required columns into HARD; row count, null rate,
  `order_total` quantiles, `payment_method` mix into SOFT. Step 5 puts all of it at the raw
  boundary with a machine-readable per-assertion result (name, status, observed, bound,
  batch id). **PASS**

## S2 — Freshness SLA that load time cannot see · application (normal)
- **Input:** Partner API sync `inventory_levels`, SLA "landed by 06:00, event time ≤ 2h old".
  On 2026-08-14 the file landed at 05:58 (SLA green) but `max(event_time)` in it was
  2026-08-12T23:00Z — 31h stale. Row count 88,400, within the normal 85k–92k band. "Our
  freshness monitor says green; the stock numbers are two days old."
- **Pass criterion (observable):** The contract carries **two** freshness assertions — batch
  arrival vs 06:00 and `max(event_time)` lag vs now — and the answer states that arrival time
  alone cannot detect this (step 5 final bullet; hard-cases row "Backfill replays yesterday's
  file → freshness on **event** time, not load time"). It also adds batch-id/duplicate-batch
  detection (step 3 Batch row). Fails if only one freshness check is proposed, or if it is
  keyed on load/ingest timestamp.
- **Baseline (without talent):** Often adds a freshness check, but keyed on the landing
  timestamp or `_loaded_at` — which is exactly the signal that was already green. Roughly even
  odds it reaches event-time lag unprompted.
- **With talent:** Step 3's Batch row profiles arrival timestamp, max event timestamp and lag
  to now as three separate measures; step 5 asserts both. The duplicate-batch detector catches
  the replayed file independently of the lag. **PASS**

## S3 — A seventh payment method appears · application (normal)
- **Input:** `payment_method` has held exactly 6 values across 90 days. Today's batch contains
  a 7th, `wallet_kr`, on 1,290 of 41,700 rows (3.1%). All rows are otherwise valid. The
  partner's release notes (found after asking) confirm a new wallet launched Monday.
- **Pass criterion (observable):** The category-set delta fires (step 5, "category-set deltas";
  hard-cases row "Producer starts sending a new enum value"), and the response then runs step 8
  triage explicitly: classified **legitimate change**, contract amended with reason, approver
  and effective date, and the new bounds for `payment_method` mix derived from data **after**
  the change rather than from the firing batch alone. Fails if the fix is "widen the accepted
  values list" with no recorded reason/approver/effective date.
- **Baseline (without talent):** Detects it if an `accepted_values` test happens to exist; the
  usual remedy is to append the value to the list and move on, with no amendment record and no
  re-derived mix bounds.
- **With talent:** Step 4 put the known category set in the contract with an owner and date;
  step 8 forces the broken-feed vs legitimate-change classification and the amendment record.
  **PASS**

## S4 — A join key stops being unique · application (normal)
- **Input:** `order_id` was unique in every one of 90 snapshot batches. Tonight: 41,802 rows,
  41,110 distinct `order_id` — 692 duplicates (1.65%). Upstream changed a join. The dataset's
  default disposition (step 6) is **quarantine**, because the consumer is a dashboard.
- **Pass criterion (observable):** PK uniqueness is placed in HARD (step 4; hard-cases row
  "A join key stops being unique"), asserted **per batch** at the boundary, and the breach
  **fails loud despite the dataset's quarantine default** — the answer must cite that HARD
  invariant breaches override the per-dataset default (step 6 final line). Fails if the answer
  quarantines the 692 rows and lets the rest land, or treats 1.65% as within tolerance.
- **Baseline (without talent):** Usually catches the duplicates (a `unique` test is the most
  common test written), but frequently proposes de-duplicating on the fly or dropping the
  extra rows — a silent drop that the Rules forbid ("No silent drops").
- **With talent:** Tier is HARD → zero tolerance, one breach is a failure → fail loud
  regardless of default; nothing lands; rejected records are countable, not filtered away.
  **PASS**

## S5 — "Which dbt tests, and at what thresholds?" · application (normal)
- **Input:** `fct_subscriptions` in the warehouse is populated nightly by another team. Our
  team owns three dashboards on it. A ticket says: "add dbt tests to fct_subscriptions."
  30 days of history available; the team uses dbt, not Great Expectations.
- **Pass criterion (observable):** The answer (i) treats dbt as the *expression* and the
  contract file as the artifact — the deliverable is a version-controlled contract next to the
  pipeline, with owner + date per assertion, that happens to be expressed as dbt tests (step 4
  final sentence); (ii) goes beyond dbt's four generic tests (`unique`, `not_null`,
  `accepted_values`, `relationships`) by adding row-count band, null-rate delta, quantile and
  freshness checks, since the generics are all HARD-shaped and catch none of step 5's
  distributional cases; (iii) tags every assertion with tier + owner + action on breach
  (Rules line 2). Fails if the output is only the four generics, or if it presumes a tool the
  team does not use.
- **Baseline (without talent):** Reliably emits the four generic dbt tests on plausible columns.
  Thresholds, if any, are round numbers. Distributional coverage is usually missing entirely,
  and the answer is a set of YAML blocks rather than a contract with owners.
- **With talent:** The HARD/SOFT split (step 4) makes the gap explicit — the dbt generics
  populate the HARD half and leave the SOFT half empty, which is the half that catches a unit
  change. Portability holds: the file names dbt, Great Expectations, Soda, pandas/Polars and
  plain SQL as interchangeable instances. **PASS**

## S6 — Half a day of rows quietly missing · application (normal)
- **Input:** Feed averages 1.10M rows/night (Tue–Thu band 1.04M–1.16M). Tonight: 612,000 rows.
  Every present row is valid; nulls, types and schema unchanged. `max(event_time)` is 13:04
  instead of the usual 23:5x.
- **Pass criterion (observable):** The contract has a row-count check compared against the
  **same weekday/period** band, not a global one (step 5 bullet 1; step 7 "compare like with
  like"), plus the max-event-time check, and both fire. Fails if row count is compared to a
  pooled all-days average or to a fixed round floor picked by feel.
- **Baseline (without talent):** Often adds a row-count check, but as a pooled minimum
  ("alert if < 500k") which this batch would pass at 612k. Weekday-matched comparison is the
  part usually missing.
- **With talent:** Step 3 profiles row count per period; step 7 derives the band from observed
  period-over-period variation and compares same-weekday. 612k sits far below the Tue–Thu band
  and the truncated max event time corroborates it. **PASS**

## S7 — A currency column changes unit, nothing else moves · pressure (clever, baseline fails)
- **Input:** `order_total` is a `bigint` in **öre**. 90-day baseline: p50 = 24,900, p90 = 89,900,
  modal digit length 5. Tonight: p50 = 249, p90 = 899, modal digit length 3. Row count 41,300
  (band 39k–44k). Null rate 0.0%, as always. Schema byte-identical. The vendor's own daily
  control total for the day says 10.4M kr; summing our batch gives 104,000 kr. Downstream is a
  monthly invoicing run. Every type, nullability, schema and freshness check is green.
- **Pass criterion (observable):** The batch is **stopped before anything lands**, on at least
  one of: the p50/p90 **ratio** vs baseline landing at 0.01x — a power of ten — flagged hard
  (step 5 bullet 2); the sum vs the upstream control total off by 100x (step 5 bullet 3); the
  digit-length distribution shift (step 3 Column row). The answer must also record the declared
  unit as a stated fact in the contract and treat a unit change as a **HARD** invariant breach
  (step 4 HARD list: "the declared unit/currency/timezone"), so the invoicing consumer fails
  loud (step 6, irreversible/externally-visible). Fails if the answer only reports "values look
  smaller" without a ratio/control-total test, or if it lets the batch land with a warning.
- **Baseline (without talent):** Every check a capable agent normally writes — types, nulls,
  uniqueness, accepted values, row count, freshness — passes. The batch ships and invoices go
  out at 1/100 of the correct amount. A baseline may notice the values look small if it happens
  to eyeball the data, but it has no test that fires; it has no baseline quantiles to compare
  against because it profiled one day, and no control-total reconciliation because step 2's
  independent-source rule is what introduced one.
- **With talent:** The quantile-ratio check exists *only* because step 3 profiled p1/p25/p50/
  p75/p99 and digit-length per period, and step 5 turns it into a per-batch ratio assertion with
  a power-of-ten trip. The öre→kronor signature is named explicitly in the file's core principle
  and in the hard-cases table. Routing is complete: declared unit = HARD (step 4) → step 6 fails
  loud regardless of the dataset default → step 7 pages. **PASS. Beats baseline.**

## S8 — The contract cried wolf and the team muted it · pressure (clever, baseline fails)
- **Input:** A contract shipped six weeks ago fires on row count every Monday (Mondays run
  ~2.1x Sunday) and on `null_rate(promo_code)` at every month end. 34 alerts in 6 weeks, 31 of
  them normal seasonality. Slack channel is muted; two weeks ago a genuinely truncated feed
  fired and nobody looked. "Should we just raise the thresholds until it stops?"
- **Pass criterion (observable):** The answer refuses the blanket widen and instead: (i) states
  an explicit **alert budget** out loud (e.g. "≤ 2/month for this feed"); (ii) **backtests the
  proposed thresholds over the historical batches before re-enabling**, counts the alerts it
  would have fired, and reads every one; (iii) switches the comparison to like-with-like
  (Monday vs Monday, month-end vs month-end) rather than raising the band; (iv) adds a
  persistence/magnitude rule (k consecutive breaches, or one breach past a wider
  "cannot be normal" bound); (v) keeps routing split — SOFT to a ticket/channel, never a page.
  Crucially, the backtest must **classify** each historical firing, so the one real truncation
  is preserved as a true positive rather than tuned away. Fails if thresholds are widened to
  silence the alerts without a backtest, or if the real truncation is absorbed into the new band.
- **Baseline (without talent):** Sympathetic and wrong in the usual way — widens the bands
  ("use 3 sigma", "set the floor at 60% of average") so the Monday firings stop. That also
  swallows the truncation event, because the widened band was fitted to noisy history that
  contained it. No budget is named, and nothing is backtested before re-enabling.
- **With talent:** Step 7 is the whole scenario: derive from observed variation, compare like
  with like, require persistence or magnitude, backtest against a stated budget before enabling,
  and keep tier routing distinct. Step 8 supplies the classification discipline that stops the
  tune-to-budget rule from laundering a real incident ("triage to broken feed or legitimate
  change"; "never widen a bound just to make red go green"). **PASS. Beats baseline.**

## S9 — The known-good snapshot is itself broken · pressure (clever, baseline fails)
- **Input:** You are handed one export to derive the contract from: `partner_customers.csv`,
  **exactly 1,000 rows**, 14 columns. `region` is 100% null. `signup_ts` spans 2026-06-01 to
  2026-06-30 and stops. `customer_id` has 4 repeats. The partner's docs say the table holds
  ~380,000 customers and that `region` is mandatory. "Derive our data contract from this."
- **Pass criterion (observable):** The answer **refuses to derive binding bounds from this file**
  and names at least three specific defects using step 2 bullet 3's list: exactly 1,000 rows =
  a pagination/export limit not a real count; an all-null column; a supposed key that is not
  unique; a date range that stops short. It must also run step 2 bullet 4 (check against what
  the producer says it is) and surface the 1,000-vs-380,000 and mandatory-`region` conflicts as
  **findings to raise with the producer now, not expectations to encode**. Consequence must be
  stated: structural constraints binding, all distributional bounds observe-only until real
  periods accumulate (step 2 bullet 5 + Rules line 1). Fails if a contract is derived that
  encodes `row_count ≈ 1000`, `region` as always-null/droppable, or `customer_id` as
  non-unique.
- **Baseline (without talent):** Profiles what it was given and produces a confident contract:
  row-count band around 1,000, `region` dropped or marked nullable, `customer_id` demoted from
  key because "it isn't unique in the data", `signup_ts` bounded to June. Every one of those
  cements a defect as the definition of correct — and the `customer_id` demotion permanently
  disables the check that would have caught the duplicate-key case in S4.
- **With talent:** Step 2 is explicitly "choose a known-good snapshot — **then prove it is
  good, because the contract inherits its defects**", and its sanity-check bullet names the
  1000-row pagination artefact and the all-null column by name. The producer-doc cross-check
  turns the disagreement into a finding. **PASS. Beats baseline.**

## S10 — Fail-loud stops a consumer that would rather have the junk · pressure (clever, baseline fails)
- **Input:** One contract, two consumers on the same feed. (a) A billing run that emits
  invoices to customers. (b) A merchandising dashboard whose team says explicitly: "if 2% of
  rows are dodgy we still want the other 98% at 07:00 — a blank dashboard costs us more than
  slightly wrong numbers." Last night a SOFT null-rate breach (4.1% vs a 0.5–1.5% band)
  halted the shared pipeline at 03:12; nothing landed for anyone; the on-call was woken and
  the dashboard was empty all morning. "Turn the checks off."
- **Pass criterion (observable):** The answer neither turns checks off nor keeps one global
  fail-loud. It forces an **explicit, recorded per-dataset (per-consumer) disposition** (step 6):
  billing → fail loud (irreversible, externally visible, "wrong is worse than late");
  dashboard → quarantine with last-good still served ("late is worse than slightly wrong").
  It must also state that this is decided from the step-1 consumer/cost line, and that the
  3am hard stop traded a data problem for an availability incident — the file's own words.
  Fails if the answer keeps a single global disposition for both consumers, or if it relaxes
  the HARD tier to reduce stoppages.
- **Baseline (without talent):** Treats fail-loud as the responsible default and defends it
  ("better no data than bad data"), or capitulates and downgrades the checks to warnings for
  everyone — which silently removes the gate protecting billing. Both answers are one global
  choice, which is the actual defect.
- **With talent:** Step 6 exists precisely to make this a deliberate per-dataset decision and
  says out loud that halting is not automatically the safe option. Step 1's consumer/cost line
  is what decides it, and step 6's last line keeps the HARD tier intact for billing regardless.
  **PASS. Beats baseline.**

## S11 — The quarantine nobody drains · edge (clever)
- **Input:** A quarantine has been running 5 months. `quarantine/` holds 1.94M rows across 147
  daily partitions. There is no replay job; no owner; the count is not on any dashboard. The
  ingest is green every night. Someone asks "our totals are ~3% light versus the partner's
  invoice — where is it going?"
- **Pass criterion (observable):** The answer identifies the quarantine itself as the leak and
  applies step 6's three-part test — a quarantine is only real if it has (1) somewhere for
  rejected records to go, (2) a **replay path** to reprocess after the fix, and (3) a
  **maximum age with an owner** — finding (2) and (3) missing. It must name the failure mode in
  the file's terms: a quarantine nobody drains is a **silent drop with extra steps**, and the
  rejected count must be countable/alarmed (Rules: "No silent drops … or the batch fails").
  Fails if the answer only proposes to "look at the quarantine folder" without adding a replay
  path, an owner and a max age, or if it treats a green ingest as evidence of no loss.
- **Baseline (without talent):** Quarantine is the answer a capable baseline recommends
  enthusiastically at design time; five months later it usually investigates the 3% gap
  downstream (joins, filters, timezone) before suspecting the reject path, because ingest is
  green. When it does find it, the fix is typically "reprocess those files once" with no
  standing owner, max age or counter — so the leak reopens.
- **With talent:** Step 6's three-condition rule turns "we quarantine" from a claim into a
  checklist, and the Rules make the reject count a first-class number. **PASS. Beats baseline.**

## S12 — Dogfood: profiling this repo's own `pipeline/metrics.jsonl` · pressure (clever, baseline fails)
- **Input:** Apply the method to `/home/user/skills-repo/pipeline/metrics.jsonl`, treating the
  file on disk today as the "known-good snapshot". Verified profile (computed, not quoted):
  24 lines, line 1 is a `_schema` header ⇒ **23 data rows** (waves 2–24). `wall_clock_s` is
  present on **6** rows only — waves 19–24, values 480, 320, 524, 1226, 1022, 798 — and the key
  is **absent** (not JSON `null`) on the other **17** rows ⇒ **74% missing** (17/23 = 73.9%).
  `agents` has the identical 6/17 pattern. `spend_measured` is null on all 24. Question:
  "derive the contract for this feed and set its thresholds."
- **Pass criterion (observable):** The method must **not** cement 74% missing measurements as
  normal. Specifically: (i) step 2 must reject this as a validated snapshot — the derivable
  slice after splitting at the instrumentation boundary is **6 rows**, which cannot span "at
  least two full seasonal cycles" and cannot be reconciled against an independent source;
  (ii) consequently, per step 2's final bullet and Rules line 1, `wall_clock_s`/`agents`
  distributional bounds are **observe-only / provisional — logged, not alerting** — while the
  structural constraints (`wave` integer and never repeating, one row per wave, ISO `date`,
  every line parses as JSON, `spend_measured` null-or-integer) stay binding; (iii) step 6 must
  route observe-only SOFT checks to "warn and pass", never to a gate. It fails if a p50 band
  for `wall_clock_s` is derived as *binding* from n=6, or if "74% null" is encoded as the
  expected null rate.
- **Baseline (without talent):** Profiles the file as given and reports "`wall_clock_s` null
  rate 74%" as a fact about the feed, then either sets `not_null` (which would fail 17 of 23
  historical rows and get relaxed away on the first run) or, more often, encodes the observed
  74% as the expected null rate — permanently normalising the missing measurements the repo is
  actively trying to fix. With n=6 it will happily quote a median (~502s) as a baseline.
- **With talent:** Step 2's split-then-prove sequence produces the right answer for the right
  reason — the boundary split leaves 6 rows, 6 rows fails bullet 1, failing bullet 1 triggers
  bullet 5's observe-only route. Step 2 bullet 4 (check against what the producer says it is)
  resolves the null pattern rather than encoding it: `pipeline/DATA.md` documents
  `wall_clock_s:INT|null // MEASURED (null only for pre-instrumentation rows 1-18)`, so the
  gap is explained, not a defect — and `spend_measured` is null "never a fabricated number"
  by design, i.e. a HARD null-or-integer rule, not a SOFT null-rate band. The file's own
  "In this repo" section reaches the same prescription (split at the instrumentation boundary).
  **PASS. Beats baseline.**
- **Two defects found while running this scenario** (recorded, non-blocking to the criterion
  above — the routing is correct regardless, because the post-split slice is 6 rows either way):
  1. **Wrong number, in the section that tells you to compute.** SKILL.md line 178 states
     profiling naively "would encode `≈30% null` as normal". The measured value is **74%**
     (17 of 23 data rows). The talent's own step 3 says "Compute, don't guess"; this is the
     one figure in the file a reader can check, and it is off by 2.4x. It also understates the
     danger the section is warning about. Fix: `≈74% null (17 of 23 rows)`.
  2. **`null` vs `absent` conflated.** The same section says the fields "are legitimately
     `null` for waves 1–18". In the file the keys are **omitted**, not set to `null`, and the
     first data row is wave 2, not wave 1. This matters to the method, not just to prose:
     step 4 lists "the presence of required columns" as a **HARD** invariant, so a contract
     asserting key presence would fail loud on 17 of 23 historical rows. A JSONL profiler must
     distinguish missing-key from null-value, and the amendment needs step 8's **effective
     date** (the wave-19 instrumentation boundary) for the presence rule to be assertable at
     all. Also: `wall_clock_s` is the subject of the section's unit trap yet appears in neither
     the HARD nor the SOFT list on lines 178–180.

## S13 — "Validate that the model's JSON matches our schema" · negative-trigger
- **Input:** "Our extraction agent returns JSON for each invoice — `invoice_no`, `total`,
  `line_items[]`. About 6% of responses come back with a missing field or a total as a string.
  We want assertions so bad records don't reach the database. Can you set up data contract
  checks?" The word "contract", the word "assertions", a 6% failure rate and a downstream
  database are all present.
- **Pass criterion (observable):** The talent **declines to be the method here** and routes to
  `structured-llm-extraction`, on the stated ground that this is a model's **own output**, not
  a dataset arriving from an upstream producer — the file's "When NOT to use" first item and
  its closing "This talent inspects the *data that arrives*, not the code that consumes it".
  Fails if it derives a snapshot/profile/threshold plan for the LLM's output as if it were a
  vendor feed. (Adjacent second look-alike, same routing rule: "review this PR's data handling
  in our training pipeline" → `mlops-production-review`, which the file also names.)
- **Baseline (without talent):** Over-triggers happily — "contract" plus "assertions" plus a
  6% bad-record rate reads as a data-quality task, and a baseline will start profiling the
  6% and proposing null-rate thresholds. That is the wrong instrument: an LLM's output
  distribution is fixed by prompt/schema/decoding, not by an upstream producer you negotiate
  with, so a drift band over it measures your own model version, not a feed.
- **With talent:** The description's explicit NOT-list and the "When NOT to use" block route it
  in one step, and the boundary rule ("data ARRIVING from an upstream source") is the
  discriminator, not the vocabulary in the request. Over-triggering is the failure this
  scenario measures, and the file does not. **PASS. Beats baseline.**

## Structural review (independent checks demanded by CURATION-LESSONS)
- **`name:` frontmatter:** present (`name: data-contract-assertions`, line 2) with a
  description. Loads correctly.
- **Dead cross-references:** all 8 named talents exist on disk — `structured-llm-extraction`,
  `eval-set-curation`, `integration-contract-completeness`, `mlops-production-review`,
  `hybrid-parse-escalation`, `external-domain-audit`, `systematic-debugging`, and `wave-reflect`
  (named as the consumer in the repo section). No rot.
- **Invented slash-commands / built-ins:** none. Grep for `/foo`-shaped references returns only
  the literal `≤ 2/month` alert budget. Clean.
- **Portability (dbt / Great Expectations as EXAMPLES, not requirements):** holds. Line 85–86
  is explicit — "may be dbt tests, Great Expectations, Soda, a pandas/Polars check, or plain
  SQL — those are instances; the contract is the artifact." No tool is required anywhere, no
  installs are prescribed, and the Rules forbid external CLI installs and credential fetching.
- **HARD-vs-SOFT split carried through steps 4 → 5 → 6 → 7 (the check specifically demanded):**
  **consistent, and the routing is two-axis, not one.** Verified chain:
  - step 4 defines the tiers and puts "the declared unit/currency/timezone" in **HARD**;
  - step 5's quantile-ratio bullet says "**flag hard** when that ratio lands near a power of
    ten" — this reads as tier HARD, not a stray adverb, because the invariant it evidences is
    the declared unit from step 4. The ratio is the *detector*; the tier belongs to the unit;
  - step 6 routes on tier: per-dataset default governs the pipeline **action**, observe-only
    SOFT gets "warn and pass", and "HARD invariant breaches fail loud regardless of the
    dataset's default" overrides;
  - step 7 routes on tier again for **notification**: "HARD breaches page; SOFT breaches open a
    ticket … Never page on a soft band";
  - Rules line 2 makes tier a required field on every assertion ("tier (HARD/SOFT), owner,
    action on breach"), so the split is enforced at authoring time, not just described.
    The two axes (action = dataset default + HARD override; channel = tier) compose without
    contradiction on every combination I enumerated. No inconsistency found. Note for a future
    sharpening pass, not a defect: "flag hard" (line 96) is the only lowercase use of the tier
    word in the file — capitalising it to **HARD** would remove the one ambiguity.
- **Defects found:** the two recorded under S12 — the `≈30% null` figure (measured: 74%) and
  the `null`-vs-absent conflation, both in the "In this repo" section, lines 176–184. Both are
  accuracy defects in the worked instance; neither changes what the method prescribes, since
  the observe-only route is triggered by the 6-row post-split sample size, not by the null
  rate. Recommended patch, not a fail.

## Failure triage (if any scenario failed)
No scenario failed; no triage required. The two S12 defects are accuracy corrections to the
repo-instance section, triaged as **skill-doc inaccuracy, non-blocking** — the prescribed
action (split at the instrumentation boundary; observe-only bounds) is unchanged whether the
figure reads 30% or 74%. They are logged here so the next pass patches them rather than
inheriting them.

## Result summary
- Scenarios passed: 13/13 · failure_cause: none · verdict: passed
