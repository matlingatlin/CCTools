---
name: data-contract-assertions
description: "Use when data ARRIVING from an upstream source has to be checked before anything downstream trusts it — a vendor or partner feed, an API sync, a CSV/JSON/Parquet drop, a Kafka topic or event stream, a scraped dataset, a nightly ETL load, or a warehouse table someone else populates. Triggers on 'the numbers look wrong but nothing errored', 'upstream changed something and nobody told us', 'a column silently changed units/currency/scale/timezone/encoding', 'half the rows are null today', 'row count dropped or spiked', 'the feed is stale / hasn't landed', 'duplicate IDs appeared', 'a category we've never seen', 'add data quality checks or assertions at ingest', 'derive a schema or data contract from a sample', 'profile this table', 'freshness SLA', 'set a drift threshold', 'our alerts are so noisy we muted them', 'fail the pipeline or quarantine the batch', 'dbt tests / Great Expectations / Soda style checks but which ones and at what thresholds'. This is about the INCOMING dataset itself. NOT for validating an LLM's OUTPUT against a declared schema (use structured-llm-extraction), NOT for choosing which examples become an eval set (use eval-set-curation), NOT for checking that a code change covers every side of a contract (use integration-contract-completeness), NOT for reviewing ML pipeline or training code in a PR (use mlops-production-review), NOT for deterministic-then-LLM bulk field parsing (use hybrid-parse-escalation)."
---

# Data Contract Assertions

Incoming data fails quietly. Nothing throws, every type still checks out, and the wrong
numbers flow all the way to a dashboard, a bill, or a model. This is the method for
turning a known-good snapshot into an explicit contract, asserting it at the ingest
boundary, and setting thresholds that catch a broken feed without alerting on every
normal Monday.

**Core principle: type validation is the cheap half.** A column that changes *unit* —
öre to kronor, cents to dollars, ms to seconds, gross to net — passes every type,
nullability, and schema check ever written while being a hundred times wrong. Only
distributional and volumetric checks catch that. A contract without them is theatre.

## When to use
- You depend on a dataset you do not produce, and its producer can change it without telling you.
- Someone found bad numbers downstream and the question is "how long has this been wrong?"
- You are adding dbt tests / Great Expectations suites / SQL assertions and don't know which to write or where to set the bounds.
- A feed has an SLA (landed by 06:00, ≤ 2h stale) that nothing currently enforces.
- Existing data-quality alerts are noisy and people have started ignoring or muting them.

**When NOT to use:** validating a model's own output against a schema
(`structured-llm-extraction`); reviewing ML pipeline code in a diff
(`mlops-production-review`); auditing an implementation against an external API spec
(`external-domain-audit`); picking eval examples (`eval-set-curation`). This talent
inspects the *data that arrives*, not the code that consumes it.

## Steps

1. **Name the consumer and the cost of being wrong — before writing a single check.**
   Who reads this data, and what breaks if a bad batch reaches them? Billing, regulatory
   reporting, and anything that triggers irreversible side effects sit at one end; a
   dashboard, a search index, a recommendation model sit at the other. Write one line per
   dataset: *"consumer X; a bad batch costs Y; stale data costs Z."* Step 6 is decided by
   this line, and thresholds without it become arbitrary.

2. **Choose a known-good snapshot — then prove it is good, because the contract inherits
   its defects.** Deriving from one arbitrary day cements whatever was broken that day as
   the definition of correct. Do all of these:
   - Take **multiple periods**, not one — enough to span at least two full seasonal cycles
     (weekly ⇒ several weeks; if it's yearly-seasonal, a year, or accept that you can only
     derive within-week bounds).
   - **Reconcile against an independent source**: the producer's own totals, a finance
     report, a second system holding the same entities. A 3% gap is a question; a 100x gap
     is your unit bug already.
   - **Sanity-check the snapshot for defects a good snapshot cannot have**: an all-null or
     single-valued column, a supposed key that isn't unique, exactly 1000 / 10000 rows
     (a pagination or export limit, not a real count), a date range that stops short, a
     timezone that shifts mid-file.
   - **Check it against what the producer says it is** — their docs, schema registry, or
     a human. Where the data and the documentation disagree, that is a finding to raise
     now, not an expectation to encode.
   - If you cannot validate the snapshot: derive only the **structural** constraints as
     binding, and mark every distributional bound **provisional/observe-only** — logged,
     not alerting — until enough periods accumulate to set it honestly. Say so in the
     contract file.

3. **Profile the snapshot — per column, per table, per batch.** Compute, don't guess:

   | Level | Measure |
   | --- | --- |
   | Column | type; null rate; distinct count (cardinality); top-k values and their share; min/max/quantiles (p1, p25, p50, p75, p99); string length distribution; **digit-length / magnitude distribution for numerics** |
   | Column | declared vs actual unit, currency, scale, timezone, encoding — record what you believe the unit to be, from documentation or reconciliation, **as a stated fact in the contract** |
   | Table | row count per batch/period; primary-key uniqueness; referential integrity against dimensions; category set per enum-ish column |
   | Batch | arrival timestamp, max event timestamp, lag to now; late-arriving and out-of-order share; duplicate-batch detection |

   Profile each measure **per period**, not pooled — you need its natural variation, and
   pooling hides it.

4. **Derive the contract, and split it in two. This split is the point of the exercise.**
   - **HARD invariants** — things that are never legitimately violated. Zero tolerance,
     one breach is a failure: PK uniqueness; a not-null column that is never null; a
     foreign key that always resolves; a sign or physical bound (age ≥ 0, quantity ≥ 0,
     end ≥ start); the declared unit/currency/timezone; the presence of required columns.
   - **SOFT distributional expectations** — things that vary legitimately and need a band,
     not an equality: row count, null rate, distinct count, quantiles, category mix,
     freshness lag. These get thresholds in step 7, and they are the ones that catch the
     unit change.
   Anything you cannot confidently place is SOFT and observe-only until evidence arrives.
   Write the contract as a file next to the pipeline, in version control, with an owner
   and a date per assertion. The expression may be dbt tests, Great Expectations, Soda,
   a pandas/Polars check, or plain SQL — those are instances; the contract is the artifact.

5. **Assert at the boundary, on every batch, before any transform or write.** Checks that
   run after the load has already merged into the target table are forensics, not a gate.
   Run against the landed raw batch; emit a machine-readable result per assertion (name,
   status, observed value, expected bound, batch id) so failures are triageable without
   rerunning anything. Include the **volumetric and distributional** checks here, not just
   the schema ones:
   - row count vs the expected band, **and** vs the same weekday/period last cycle;
   - **quantile-ratio check**: p50 (and p90) of each numeric column divided by its baseline
     — flag HARD when that ratio lands near a power of ten (100x, 0.01x) or a known
     currency/unit factor; that is the öre→kronor signature, and it is invisible to types;
   - sum/aggregate reconciliation against an upstream control total where one exists;
   - null-rate, cardinality, and category-set deltas;
   - freshness: max event time and batch arrival vs the stated SLA.

6. **Decide fail-loud vs quarantine per dataset — explicitly, and record the choice.**
   Halting the pipeline is not automatically the safe option: for a consumer that degrades
   gracefully, stale data can hurt more than slightly-off data, and a hard stop at 03:00
   trades a data problem for an availability incident. Choose per dataset, from step 1:
   - **Fail loud (stop, nothing lands)** — irreversible or externally-visible consumers:
     billing, payouts, regulatory or financial reporting, anything that writes to another
     system. Wrong is worse than late.
   - **Quarantine (bad rows or the whole batch held aside; last-good stays served)** —
     analytics, dashboards, search indexes, recommendations, ML features. Late is worse
     than slightly wrong, and partial data beats no data.
   - **Warn and pass** — allowed only for observe-only SOFT checks with no agreed bound yet.
   A quarantine is only real if it has all three: somewhere for rejected records to go, a
   **replay path** to reprocess them after the fix, and a **maximum age** with an owner.
   A quarantine nobody drains is a silent drop with extra steps. HARD invariant breaches
   fail loud regardless of the dataset's default.

7. **Set drift thresholds from the metric's own history — a contract that cries wolf gets
   muted, and a muted contract protects nothing.** For each SOFT check:
   - Derive the bound from **observed period-over-period variation** across the snapshot
     window (e.g. a band from the median ± a multiple of the historical deviation, or the
     min/max of historical change with headroom) — never from a round number that felt safe.
   - **Compare like with like**: same weekday, same hour, same segment. Most "seasonality"
     false alarms are a Monday being compared to a Sunday, or a holiday to a workday.
   - Require **persistence or magnitude** for soft checks: alert on k consecutive breaches,
     or on a single breach past a wider "this cannot be normal" bound. A one-batch wobble
     inside a two-batch pattern is noise.
   - **Backtest the proposed contract over the historical batches before enabling it.**
     Count the alerts it would have fired and read every one. More than a couple of
     unexplained firings per dataset per month means the threshold is wrong, not that the
     data is bad. State the alert budget out loud ("≤ 2/month for this feed") and tune to it.
   - Keep the two tiers distinct in routing: HARD breaches page; SOFT breaches open a
     ticket or post to a channel. Never page on a soft band.

8. **Maintain the contract as reality legitimately changes.** Upstream *will* add a
   category, launch a market, and triple in volume for good reasons. When a check fires:
   triage to **broken feed** or **legitimate change**, and record which. A legitimate
   change amends the contract with a reason, an approver, and an effective date — new
   bounds derived from data *after* the change, not from the failing batch alone. Never
   widen a bound just to make red go green without that record; that is how a contract
   decays into a rubber stamp. Re-derive bounds on a schedule (e.g. quarterly) so slow,
   real growth doesn't accumulate into a permanent yellow. Where checks keep firing for
   the same upstream reason, the fix is a conversation with the producer, not a wider band.

## The hard cases, in one table

| Symptom | Why types miss it | The check that catches it |
| --- | --- | --- |
| Currency column switches öre → kronor (or cents → dollars, ms → s) | integer stays integer, nulls unchanged, schema identical | p50/p90 **ratio** vs baseline near a power of ten; sum vs an upstream control total; digit-length distribution shift |
| Feed silently truncated (half a day's rows) | every present row is valid | row count vs same-period band; max event time vs SLA |
| Producer starts sending a new enum value | it's a valid string | category-set delta against the contract's known set |
| A join key stops being unique | duplicates are type-correct | PK uniqueness as a HARD invariant, asserted per batch |
| Backfill replays yesterday's file | data is real, just old | batch-id/duplicate detection + freshness on **event** time, not load time |
| Alerts fire every Monday | threshold set on pooled data | like-with-like comparison + persistence rule (step 7) |

## Rules
- **Never derive a binding threshold from a snapshot you have not reconciled** (step 2).
  Unvalidated snapshot ⇒ structural checks binding, distributional checks observe-only.
- **Every assertion carries: tier (HARD/SOFT), owner, action on breach.** An assertion
  with no named action is a log line, so label it observe-only and stop calling it a gate.
- **Assertions read data; they never mutate the source.** No credential-fetching, no
  external CLI installs, no calls outside the data access the project already has.
- **No silent drops.** Rejected records are quarantined and countable, or the batch fails.
  "Filter out the weird rows" without a counter is how a 40% loss goes unnoticed.
- **The contract lives in version control beside the pipeline**, and every amendment
  records reason + approver + effective date.
- This talent stops at the ingest boundary: it does not review the consuming code
  (`mlops-production-review`), and it does not diagnose *why* a specific batch broke once
  detection has fired (`systematic-debugging`).

## In this repo (one instance)
`pipeline/metrics.jsonl` and `pipeline/ledgers/*.jsonl` are exactly this problem: append-only
feeds written by many different agents, consumed by `wave-reflect`, with the stated contract
already written down in `pipeline/DATA.md`. Applying the method here:
- **Snapshot caveat (step 2):** early rows are pre-instrumentation — `wall_clock_s` and
  `agents` are legitimately `null` for waves 1–18. Profiling naively would encode "≈74% null (17 of 23 data rows — counted, not estimated)"
   Two precision points this instance turns on: the fields are **omitted, not set to `null`** —
   which matters because step 4 lists *presence of required columns* as a HARD invariant, so a
   contract asserting key presence would fail-loud on 17 of 23 historical rows and needs step 8's
   amendment with an effective date (the instrumentation boundary at wave 19). And the trap column
   itself, `wall_clock_s`, belongs in the HARD list (declared unit: seconds) — a value written in
   milliseconds type-checks perfectly.
  as normal. Split the snapshot at the instrumentation boundary and derive from rows after it.
- **HARD:** one row per wave, `wave` an integer that never repeats, ISO `date`, every row
  parses as JSON, `spend_measured` is null-or-integer (`DATA.md`: never a fabricated number).
- **SOFT:** `agents` per wave, `yield_rate` range, `tokens_est` magnitude, rows-appended per pass.
- **Unit trap, live:** `wall_clock_s` written in milliseconds by one agent type-checks
  perfectly and silently inflates every duration ~1000x — caught only by the p50-ratio check.
- **Consumer (step 6):** `wave-reflect` learns longitudinally, so a bad row poisons the record
  permanently and cannot be un-learned ⇒ **fail loud** at append time, not quarantine.
