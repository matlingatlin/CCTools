---
name: expand-contract-migration
description: "Use when changing a schema or interface that live, already-running code depends on — renaming or dropping a database column or table, changing a field's type, units, or nullability, altering an API request/response field, changing a queue or event message format, renaming a config key or environment variable, changing an on-disk or object-store layout, or changing a cache key format — where old and new versions of readers and writers will be running AT THE SAME TIME during rollout, or where already-persisted data and in-flight messages are in the old shape. Triggers: 'rename this column', 'drop the old field', 'change the message format', 'zero-downtime migration', 'backward compatible change', 'rolling deploy', 'canary', 'blue-green', 'old pods crashed after deploy', 'column does not exist', 'unknown field', 'backfill', 'dual write', 'expand and contract', 'parallel change', 'deprecate this field', 'is it safe to remove yet', 'who still reads this'. Keeps old and new simultaneously valid, one deployable phase at a time. NOT for making a single side effect safe to run twice after a retry or crash (use idempotent-action-design), NOT general multi-step task planning (use writing-plans), NOT for asserting quality on incoming upstream data (use data-contract-assertions), NOT for recovering what undocumented code currently does (use behavioral-spec-mining)."
---

# Expand-Contract Migration

Changing a live interface in one commit is the classic invisible outage: the diff is clean,
the tests pass, and during the rollout window old processes ask for something that no longer
exists. **The unit of safety is not the commit, it is the instant** — at every instant of the
rollout, a mixed fleet of old and new code must both be correct against the store.

The method: never change a shape in place. Add the new shape, run both, move the data, move
the readers, and only then remove the old one — each step deployable and revertible alone.

## When to use
- A rename, type change, removal, or reshaping of anything another process reads: DB column
  or table, API field, event/message payload, config key, file layout, cache key.
- Deploys are rolling/canary/blue-green, or there is more than one deploy unit, or clients
  you do not control (mobile apps, SDK consumers, partner integrations, saved dashboards).
- Data already persisted in the old shape must survive the change.
- Someone asks "can we finally delete this field?"

**When NOT to use — running five phases where one suffices is also a defect.** Do it in one
step when *no instant of mixed old/new can exist*:
- Single deploy unit, deployed atomically (one process replaced whole), and the shape is
  purely internal to it with nothing persisted in it.
- Zero rows / zero traffic / pre-launch: the interface has no readers or data in production.
- A maintenance window is genuinely permitted and the change fits inside it.

Also not this talent: making one action safe to re-run (`idempotent-action-design` — a
perfectly idempotent migration still crashes old readers), planning generic multi-step work
(`writing-plans`), gating incoming data quality (`data-contract-assertions`).

## Steps

### 1. Inventory readers and writers before designing anything
List every process that **writes** the old shape and every one that **reads** it, plus each
one's release cadence. Include the ones that make people skip this step: batch/cron jobs,
data warehouse and ETL pipelines reading the store directly, admin and one-off scripts,
replicas and analytics copies, saved reports and dashboards, backup/restore paths, other
teams' services, and clients you cannot force-upgrade.

Record for each: **is it deployable by you?**, **does it read, write, or both?**, and **how long
until its slowest instance is upgraded?**

Keep **two** numbers, not one — a single "fleet lag" applied to every gate is the mistake that
turns a routine rename into a quarter-long project:
- **Writer lag** = the slowest *writer*'s upgrade time. It sizes the dual-write gate (step 4),
  because that gate asks "is anyone still writing old-only?" — a pure reader cannot fail it.
- **Reader lag** = the slowest *reader*'s upgrade time, including consumers you do not control.
  It sizes the switch-reads and contract gates (steps 6 and 8), which ask "is anyone still
  reading the old shape?"

The error is asymmetric in both directions, so keep them apart deliberately: using the reader
number for the writer gate is safe but can hold a two-week phase open for six weeks against a
partner that only reads; using the writer number for the contract gate is *unsafe* and breaks
that partner. When a process both reads and writes, it counts in both. A consumer you cannot
upgrade means the old shape may never be removable; decide that now, not at step 6.

### 2. Choose the shortest phase sequence that keeps both shapes valid
Full sequence: **expand → dual-write → backfill → switch reads → contract**. Drop the phases
you do not need:
- Pure addition, nothing removed → expand + switch reads.
- Removing a field nobody writes → switch reads + contract.
- No historical data (new field only meaningful going forward) → no backfill.

Write the chosen sequence down with one deploy per phase. **Never combine two phases in one
deploy** — the combination is what removes your rollback.

### 3. Expand — add the new shape, additively, read by nobody
Add the new column/field/key alongside the old. Hard constraints that make it additive:
- **Nullable or defaulted**, never `NOT NULL` without a default; no new required field in a
  request; no removed field in a response; no narrowed enum, type, or validation.
- No rename in place, no destructive DDL, no long lock on a hot table (add the column, then
  build indexes concurrently/online as the store supports).
- Readers must tolerate the new shape being absent or unknown — old consumers must **ignore
  unknown fields**, not reject them. If a consumer's parser is strict, that parser is a
  reader you must upgrade first, and it belongs in step 1's list.

**Gate (observable, not "wait a bit"):** the change is applied on every replica/shard/region,
AND a process still running the *old* code performs its normal read and write against the
expanded store with no error. Verify that against a real old-version instance, not by
reasoning. **Rollback:** drop the addition. Nothing reads it; no data loss.

### 4. Dual-write — every writer writes both, old stays the source of truth
Every write path sets old and new in the same transaction/message/commit. The old shape
remains authoritative: reads still come from it, so a bug in the new path cannot corrupt
anything anyone is using.

- Extract the old→new transform into **one shared function** and call it from both the
  dual-write path and the backfill (step 5). Two implementations of the same transform
  produce two populations that disagree, and the disagreement surfaces months later.
- Dual-write must be idempotent per record (see `idempotent-action-design` for keying) —
  retries and redeliveries will re-run it.

**Gate:** *no writer is still writing old-only.* Measure it, do not assume: for records
created or updated after a timestamp T, the count with the new shape missing must be **0**,
sustained for longer than the **writer lag** from step 1 (not the reader lag — a reader cannot
fail this gate). Where empty is a *legal* value for the new shape, "missing" is unmeasurable as
written: count against the explicit marker step 7 requires (a `migrated_at` stamp or a
written/not-written sentinel), never against NULL. A non-zero count names your straggler —
usually a cron job, a queue consumer draining old in-flight messages, or an admin script.
For queues, remember in-flight messages already enqueued in the old format: consumers must
accept the old format for at least the queue's maximum retention plus redrive age.

**Rollback:** stop writing the new shape. Old is complete and authoritative; no data loss.

### 5. Backfill — historical records, idempotently, batched, resumable
Only start once step 4's gate is green. Backfilling while writers still write old-only is
chasing a moving target: the tail you just closed reopens behind you.

1. **Batch over a stable ordering key** (primary key range, partition, date bucket) — never
   `OFFSET`, which shifts under concurrent writes. Persist the completed watermark after each
   batch so a killed job resumes from it instead of restarting.
2. **Write conditionally, never unconditionally.** Set the new shape only where it is still
   unset (`WHERE new IS NULL`, compare-and-set on empty, create-if-absent). Live writes always
   win — see step 7.
3. **Bound the blast radius per batch:** size batches for the store's lock/latency budget,
   pause on replication lag or error-rate thresholds, and make the job resumable and
   stoppable mid-run.
4. **Verify coverage in two passes, not one.**
   - *Tail pass:* rows changed while the backfill ran (`updated_at` > job start, or the
     changelog/CDC stream over the run window; where the store has neither — object stores,
     append-only blobs — you need a listing by write time or a manifest, and if you have no
     way to enumerate the window, you cannot verify this backfill). Re-scan them; repeat until
     the pass finds zero. This is the part textbook versions skip.
     Be precise about what it catches, or you will trust it for the wrong reason: with step 4's
     gate green and writes made conditionally, rows written *during* the run are already
     dual-written, so the tail pass is not what stops them going missing. It catches the three
     things that gate does not — a straggling writer that appeared after T, a stale-over-fresh
     overwrite where the backfill clobbered a newer live write, and stores with no consistent
     snapshot, where a full scan can simply miss rows that moved beneath it.
   - *Full assertion:* count of records where the old shape is present and the new is absent
     must be **0** across the entire range — not a spot check.
5. **Presence is not correctness.** On a random sample, assert `transform(old) == new`. A
   backfill that filled every row with the wrong transform passes every null check.

**Rollback:** none needed — the backfill only fills empty slots, so a partial run is a valid
state and re-running is safe. That is exactly why step 5.2 is conditional.

### 6. Switch reads — in two sub-steps, never one
1. **Fallback read:** readers use *new if present, else old*, and **increment a counter every
   time the fallback fires**. Deploy. The fallback counter is your live proof of residual
   gaps that the step-5 assertions missed.
2. **New-only read:** once the fallback counter is 0 across a window longer than the fleet
   lag *and* longer than the slowest periodic job's period (a quarterly report reads once a
   quarter), remove the fallback. Deploy.

**Gate:** fallback-hit count = 0 over that window; error rates and the relevant business
metrics unchanged after each sub-step.
**Rollback:** point reads back at the old shape. This is safe **only because dual-write is
still on** — which is why "switch reads" and "stop writing old" must never ship together.

### 7. When dual-write and backfill disagree
During the transition, **exactly one side is the source of truth: the old shape, until reads
switch.** Resolve conflicts by that rule, not by last-writer-wins.

- The backfill reads a record, computes, and writes seconds or minutes later; a live write may
  have landed in between. An unconditional write puts *stale* data over *fresh*. Always
  condition the write on the target still being empty, or on the record's version/`updated_at`
  not having moved since the batch read it. If it moved, skip the row — dual-write already
  handled it correctly.
- If empty is a legitimate value a live write can set, nullness is not a usable sentinel. Use
  an explicit marker instead — a `migrated_at` stamp or schema-version field on the record.
- If old and new disagree on a record after both are populated, treat it as a **conflict, not
  a merge**: log it with the record id, do not overwrite, and fix the transform. Divergence
  found before the read switch is cheap; found after, it is a data-correctness incident.
- Non-invertible transforms (splitting one field into two, merging two into one, lossy type
  narrowing) deserve an explicit written decision on which direction is authoritative in each
  phase — this is where "both are the source of truth" quietly becomes "neither is".

### 8. Contract — the phase everyone forgets, and the only one-way door
Removal has two steps, and only the second is irreversible.

**8a. Stop writing the old shape.** Deploy. Reversible *when a new→old transform exists*: turn
dual-write back on, then backfill the *old* shape for records created in the meantime. For a
lossy or non-invertible change (one field split into two, a narrowed type) that transform may
not exist, and 8a is then effectively one-way for anything written after it — check this before
you ship 8a, not while rolling back, and if it is one-way, hold the old shape's last known
values (an export, or keep writing them) for the length of the reader lag.

**8b. Remove the old shape.** Drop the column, delete the field, delete the key. **This is the
one-way phase** — after it, recovery requires a restore from backup. Ship it alone, separated
in time from every other phase, and never bundled with a feature change.

**What counts as proof that no reader remains — "we grepped the code" does not.** Grep misses
dynamic field access (`row[name]`), `SELECT *`, reflection and generic serializers, ORM
lazy-loads, third-party and mobile clients, saved queries, dashboards, notebooks, ETL jobs,
and anything outside the repo you searched. Required evidence, all of it:
1. **Measured reads of the old shape = 0** from instrumentation on the access path (a counter
   tagged by caller/service/client version), sustained over a window **longer than the longest
   consumer's release cycle** and longer than the slowest periodic job's period. For clients
   you do not control, that window is the client's own upgrade tail — possibly unbounded, in
   which case you version the interface or publish a hard sunset date and accept breakage
   knowingly.
2. **Zero grants/permissions** left to the old shape, or the read permission revoked first and
   nothing broke.
3. **A dark-removal rehearsal:** behind a flag you can flip back in seconds, make the old shape
   unavailable (return empty/error, revoke access, rename the flag-guarded path) for a bounded
   period in production, watching error rates. Something breaking here is the whole point —
   discovering it now costs a flag flip; discovering it after 8b costs a restore.
Only after 1–3 do you run 8b.

### 9. Record the phase state where the next person will find it
The migration outlives your session and usually your attention. Keep a short, updated record
of: current phase, the gate evidence for each completed phase, the straggler list from step 1,
and the earliest date 8b may run. A half-finished expand-contract that nobody remembers is
permanent dual-write cost plus a field everyone is afraid to delete.

## Example
**Before:** rename `users.name` → `users.full_name`. One PR: `ALTER TABLE ... RENAME COLUMN`,
every call site updated, tests green. During the rolling deploy the old pods run
`SELECT name FROM users` against a table where `name` no longer exists. Nothing in the diff
or the test suite shows it.

**After:** *(1)* readers/writers inventoried — the API, a nightly export job, and a partner
integration on a 6-week release cycle → fleet lag 6 weeks. *(2)* full five-phase sequence.
*(3)* add nullable `full_name`; verify an old-version pod still reads/writes fine. *(4)* all
writers set both via one shared transform; gate when rows created after T with
`full_name IS NULL` stays at 0 for 6 weeks — which surfaces the export job nobody listed.
*(5)* backfill batched by id range with a persisted watermark, `WHERE full_name IS NULL`, then
a tail pass over `updated_at > start` until it returns zero, then the full assertion and a
sampled `name == full_name`. *(6)* fallback reads with a counter; when it holds at 0, new-only
reads. *(8a)* stop writing `name`. *(8b)* six weeks of measured zero reads plus a dark-removal
day behind a flag, then `DROP COLUMN` alone in its own deploy.

**The same five phases, non-SQL:** adding a required API request field → ship it optional,
accept both, migrate callers, then require it. Changing an event payload → producers emit both
shapes, consumers prefer new with fallback, drain the queue's retention window, then stop
emitting old. Renaming a config key → read new-then-old with a deprecation warning on the old
path, and remove only when the warning stops firing.

## Rules
- **One phase per deploy.** Combining phases is what destroys rollback.
- Every gate is an **observable measurement over a window ≥ fleet lag** — a count, a counter at
  zero, a live old-version process succeeding. Never "wait a bit" or "should be fine by now".
- Additive only during expand: nullable/defaulted, no narrowed types, no new required fields,
  unknown fields ignored rather than rejected. That is a COMPATIBILITY rule, not a cost claim —
  whether adding a defaulted column is instant or rewrites the whole table depends on the engine
  and its version (recent PostgreSQL and MySQL do it in metadata; older ones rewrite). Check
  your own engine before sizing the window.
- Backfill writes conditionally and resumes from a persisted watermark; verify with a tail pass
  plus a full assertion plus a sampled correctness check.
- **The old shape is the source of truth until reads switch.** Conflicts stop and get logged;
  they are never merged or last-writer-wins.
- Only 8b (actual removal) is irreversible. Ship it alone, late, and never with a feature.
- "We grepped for it" is not evidence of no readers. Measured reads plus a dark-removal
  rehearsal are.
- Prefer fewer phases when no mixed-fleet instant can exist — but decide it from step 1's
  inventory, not from optimism.
- Design method applied by hand: no auto-run hooks, no credential or network calls, no tool
  installs. Every command in the example is illustrative, not prescribed.
- Complements: `idempotent-action-design` (the dual-write and backfill steps must be safe to
  re-run), `integration-contract-completeness` (did the change cover every mirror side),
  `data-contract-assertions` (assert the new shape's quality once it is authoritative).

## Common mistakes
| Mistake | What actually happens |
|---|---|
| Rename in one commit, "the deploy is fast" | Old pods query a column that no longer exists for the whole rollout window |
| Backfill started before dual-write is fully rolled out | The historical tail reopens behind the job; coverage never reaches 100% |
| Backfill writes unconditionally | Stale computed values overwrite fresh live writes |
| Verifying coverage with one pass | Rows written during the run are missed — the exact rows that are live |
| Non-null count = 0 treated as "backfill correct" | Every row filled with the wrong transform passes a null check |
| Switch reads and stop dual-write in the same deploy | Reads cannot be rolled back; the old shape is now stale |
| Grep proves no readers | Dynamic access, `SELECT *`, dashboards, ETL, and clients you don't own are invisible to grep |
| Removal window sized by deploy time | A quarterly job or a 6-week mobile release reads it after your two-day window closed |
| Two copies of the old→new transform | Two populations that disagree, discovered long after both are authoritative |
| Five phases for a field inside one atomic deploy unit | Weeks of double bookkeeping and a permanent half-migrated field, for no exposure |

## In this repo (one instance)
`pipeline/frontier.json`, `pipeline/metrics.jsonl`, and the `pipeline/ledgers/` rows are live
interfaces: both loops (the build/harvest wave and `library-curator`) read and write them, and
older runs may still be in flight. Renaming a key there is the same five phases — add the new
key alongside, have both loops write both, backfill existing rows conditionally on the new key
being absent, switch readers to new-with-fallback, and only drop the old key once no run has
read it for longer than a full loop cycle. `.claude/skills/<name>/SKILL.md` frontmatter is the
same story: `name` and `description` are read by the runtime loader, so an added field must be
ignorable by it before anything depends on it.
