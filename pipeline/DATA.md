# DATA — what we collect, who writes it, when (the collection contract)

The single source of truth for the system's own telemetry. Learning is the #1 job
(`BRAIN.md` §0); learning needs data. This file says **exactly what data every run must
leave behind** so the accumulating record becomes analysis-ready. If a store below is not
updated on a run that should have touched it, that run is incomplete.

Principle that decides what we log: **capture now what cannot be reconstructed later.**
Cost, wall-clock, and longitudinal per-talent history are gone forever if a wave doesn't
tick them as it happens — so they are logged live, even though the data-science *analysis*
layer is deferred until volume exists (rule-based reflection is right until then).

## Honesty about measurement (measured vs estimated)
- **Measured** (log the real number): `wall_clock_s` (bash `date +%s` delta across the
  wave/pass), `agents` (count of agents spawned), scenario counts, gate/proposal outcomes.
- **Estimated** (honestly labelled): `tokens_est` stays an estimate. Real token spend needs
  a metered path (route the wave through the Workflow `budget.spent()` meter); until then
  `spend_measured` is `null`, never a fabricated number. Do NOT dress an estimate as measured.

## The stores

### 1. `metrics.jsonl` — one row per wave/pass (append-only)
Written by: the coordinator at wave end (piano) / pass end (curator), via `wave-reflect`.
Schema (row 0 is a `_schema` header, skipped by readers):
```
wave:INT · date · job · source · source_type · seen · adopted · adapted · library
rejected:{dedup,reuse,worthiness,security}   // counts; per-candidate reasons -> rejections.jsonl
yield_rate:FLOAT · talents_used:[..]
wall_clock_s:INT|null   // MEASURED (null only for pre-instrumentation rows 1-18)
agents:INT|null         // MEASURED count of agents spawned this wave
tokens_est:INT          // honest estimate
spend_measured:INT|null // real output tokens if routed through a meter, else null
notes:STR
```

### 2. `ledgers/talents.jsonl` — per-talent lineage (event-sourced, append-only)
Written by: piano at born/tested; curator at curated/deepened/sharpened/proposed.
One row per lifecycle EVENT (not per talent), so history accumulates:
```
ts · talent · event:(snapshot|born|tested|curated|deepened|sharpened|proposed_drop|proposed_merge)
born_wave · origin:(built|adopted-pre-loop) · wave:INT
tested:BOOL · scenarios:INT · adversarial:INT · test_verdict:(passed|failed|null)
detail
```
Answers (queryable, no prose-reading): survived N curation passes = count `curated`/`deepened`
events; last tested = max ts of `tested`/`deepened`; which source shapes yield DURABLE talents
= join `origin`/`born_wave` against survival. Seeded with a `snapshot` per on-disk talent.

### 3. `ledgers/evals.jsonl` — per-scenario eval outcome (append-only)
Written by: piano TEST step and curator, one row PER SCENARIO at author/run time.
```
ts · talent · scenario:(A|B|..) · kind:(normal|adversarial|negative-trigger)
baseline:(pass|miss) · with:(pass|catch) · result:(pass|fail) · wave · pass_criterion
```
Makes the thing that matters most — *are the tests getting more discriminating?* —
computable: scenarios/talent, adversarial share, baseline-miss rate (do the clever ones
actually break baseline?), which talent fails which scenario. History WAS backfilled from
the `evals.md` headings + `Result summary` lines (kind parsed from the heading tag; `baseline`
/`with` are `null` for backfilled rows — prose doesn't record them per-scenario, `backfill:true`
marks these); fresh rows from now on carry the full per-scenario baseline/with/result.

### 4. `ledgers/rejections.jsonl` — categorized gate rejections (append-only)
Written by: piano at the Gate step, one row per rejected candidate (going forward).
```
ts · wave · candidate · source · gate:(dedup|reuse|worthiness|security)
reason_code:(duplicate-of|already-in-library|no-baseline-gap|too-niche|covered|
             auto-run-hook|network-call|creds|installer|...) · detail
```
Turns the `rejected` COUNTS in metrics into WHY. Learn which source shapes waste the gate's
time, and which security surface recurs. Seed rows are aggregate (`candidate:"(aggregate)"`);
new rows are per-candidate.

### 5. `ledgers/proposals.jsonl` — human-gate proposal ledger (append-only)
Written by: piano/curator when raising a merge/drop/restructure proposal; the coordinator
appends the OUTCOME when the human resolves it.
```
ts · wave · type:(drop|merge|restructure|remove-legacy|remove-redundant|...)
target · proposal · rationale · outcome:(pending|approved|rejected|deferred)
resolved_ts · decided_by   // WHO made the call, not just when
```
Answers "which proposals were sound" — the human-gate's own hit rate over time.
`decided_by` was missing until 2026-08-28 and the gap was found from the outside: a new talent
required a named decider as evidence that a descope was real, and a positive control against this
very ledger showed no such field exists, so every descope we had recorded would have failed its
test. A store that records WHAT was decided and WHEN, but not by WHOM, cannot support any method
that needs to distinguish a decision from a silence.

### 6. `ledgers/defects.jsonl` — what an independent test caught, and how long it lived
Written by: the coordinator when an independent test fails a talent and the failure is triaged
as a skill-bug.
```
ts · talent · defect · lived_waves:INT|null · caught_by · triage:(skill-bug|test-bug) · fixed:BOOL
```
`lived_waves` = waves the defect was live before detection; `null` means it existed since the
talent was written (that measures "we never tested it", not detection speed — count those apart).
This is the curator's own improvement metric: **is time-to-detect falling?** A library where
defects are caught in 2 waves is healthier than one where they surface after 12, even if both
find the same number.

### 7. `ledgers/claims.jsonl` — what an agent CLAIMED, and what verification found
Written by: the coordinator, one row per claim an independent agent made, at the moment it is
verified — before acting on it.
```
ts · wave · agent_role:(tester|curator|author|harvester) · target · claim
verdict:(confirmed|refuted|partial) · verified_how · acted:BOOL
```
`partial` = the finding was real but the stated MECHANISM was wrong. Both halves matter: the
claim earned its keep, and citing it verbatim would have propagated an error. (Real instance: a
tester reported that a yield of 0.000 was computed and would soon fire a deprioritize; the true
mechanism was that no such yield was ever computed at all, and 13 of 25 rows were being dropped
from the table. Right to act on, wrong to quote.)

**Why this store exists: we measure the talents but never measured the instrument.** Every
verdict in `evals.jsonl` comes from an agent whose accuracy we had never quantified. This makes
"is the tester trustworthy?" a number instead of an impression, and it is PERISHABLE — the
verification happens once, in the moment, and is gone if not written down.

**Rule: verify before you act, and record the verification, not just the outcome.** `verified_how`
must name what was actually checked (a file read, a command re-run, a count compared) — "looked
correct" is not a verification.

### Defects carry a FAMILY, not just a description
`defects.jsonl` rows carry `family` (one of: `wrong-scope`, `asymmetric-rule`, `open-loop`,
`mismeasurement`, `missing-guard`, `dead-reference`, `factual-error`, `nondeterminism`,
`routing-contradiction`) and `silent:BOOL`. The taxonomy was derived from the first 20 defects
via `error-analysis-taxonomy` (open-code → axial-code → one primary mechanism per row), not
invented up front; extend it the same way rather than by adding a category ad hoc.

Families make defects PREDICTIVE instead of merely counted: the ranked distribution says where to
look next. The first ranking put `wrong-scope` at 20% and, more importantly, showed that
**13 of 20 defects (65%) are SILENT** — absence of a result is indistinguishable from a correct
negative. That is the class an audit cannot find by reading; it needs a positive control.

### Deploy is an EVENT, not a habit
`talents.jsonl` carries a `deployed` event per talent. Routing coverage says a talent is
**findable** in the capability map; only a context reload makes it **live**. Those are different
failures and only one of them was measured — the gap was being closed by the coordinator
remembering, which is not a control. `signals.py` now emits a directive for any shipped talent
with no `deployed` event.

**Event rows MERGE forward.** A later event carries only the fields it changes, so readers must
merge non-null values rather than taking the last row wholesale — otherwise a `deployed` event
silently un-tests a talent. (Introduced and caught within one run of `signals.py`.)

## Also feeding the brain (existing, unchanged)
`LESSONS.md` (source-yield) · `TEST-AUTHORING-LESSONS.md` (test-authoring directives) ·
`CURATION-LESSONS.md` (the operating journal) · `frontier.json`
(queues/seen/schedules) · `catalog/catalog.json` (469 labelled components) · `STATUS.md`
(human log) · `BRAIN.md` (§0 improvement-signals, now sourced from these ledgers).

## The contract (enforced by the skills)
- **piano** every wave: metrics row (with `wall_clock_s`+`agents`); a `born`+`tested`
  talent event and per-scenario `evals` rows for each shipped talent; a `rejections` row per
  gated-out candidate; a `proposals` row for anything raised to the human gate; a `claims` row
  per claim any agent made, recorded WHEN VERIFIED; `family` + `silent` on every `defects` row.
- **library-curator** every pass: metrics row; a `curated`/`deepened` (and `sharpened` when a
  description changes) talent event + per-scenario `evals` rows per unit; `proposals` for
  merges/prunes; triage (test-bug vs skill-bug) recorded in the eval row's detail; a `claims`
  row per auditor claim with how it was verified; `family` + `silent` on every `defects` row.
- **both, at end:** refresh `BRAIN.md` §0 improvement-signals FROM the ledgers (not by memory).
- **Reconstructable-only backfill:** past waves (1–18) are seeded from `metrics.jsonl` +
  on-disk `evals.md`; their cost/time are `null` (unmeasured then) — never faked.

## Analysis layer (deferred, on purpose)
No dashboards or ML yet — the ledgers are append-only JSONL precisely so a data-science pass
can consume them later without migration. `pipeline/queries/` (future) will hold read-only
scripts (survival curves, test-discrimination trend, gate-waste by source). Until volume
justifies it, `wave-reflect`'s deterministic rules + BRAIN §0 remain the reflection engine.

### 8. `ledgers/builds.jsonl` — one row per skill-builder build (append-only)
Written by: `pipeline/build/record.py` at 8.2, **whatever the verdict**. An abandoned build
is a row, not a silence — the abandon rate and its shapes are what the loop learns from.
```
ts · build · verdict:(ship|iterate|abandon|undecidable) · reason
failure_kind · content_kind · verifiable
phases_run:[..] · phases_skipped:[{phase,function,reason}] · not_checked:[{what,why}] · events:INT
```
`phases_skipped` carries the REASON because a phase skipped deliberately and a phase never
reached are the same absence in a record that logs only what ran. `not_checked` exists because
a build record listing only what was verified reads as though everything else was fine.

### 9. `ledgers/fields.jsonl` — one row per contract field per build (append-only)
Written by: `pipeline/build/record.py` at each 4.x field completion.
```
ts · build · field · red_code:[rule ids] · red_agent:[..] · n_red_code · n_red_agent · rewrites:INT
```
**This is what makes the builder measurable on itself.** Without it we learn only that a skill
came out good or bad; with it we learn WHERE in the chain it did — which contract field costs
the most rework, and therefore which part of the method to fix next.
