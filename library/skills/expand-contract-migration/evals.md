# Evals — expand-contract-migration

**Talent:** `expand-contract-migration` · **Type:** discipline (phase-gated method with pressure points) · **Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result meets the pass
criterion. Authored by an INDEPENDENT tester who did not write the skill; every scenario is
written against the file's ACTUAL numbered steps, gates, rules and Common-mistakes rows —
each pass criterion cites the step it tests, and every direction tested was verified present
in the file first.

**Blend:** 10 scenarios — 4 `application (normal)`, 5 clever (4 `pressure`, 1 `edge`),
1 `negative-trigger`. ~half and half, per CURATION-LESSONS ACTIVE DIRECTIVES.

**On verdict phrases:** "Beats baseline" is a claim, not a formatting rule. The normal
scenarios end in a plain **PASS** because a capable baseline plausibly passes them too — that
is what normals are for. **PASS. Beats baseline.** appears only where the baseline is designed
to fail, plus the negative-trigger where over-triggering is the measured failure. S9 (edge) is
deliberately *not* marked as beating baseline even though it is a clever scenario: see its
Baseline line for why that would be a false claim.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 4 normal / 5 clever / 1 negative-trigger.
- [x] **Specific to this talent** — every scenario cites a concrete step, gate or table row.
- [x] **Observable pass/fail criterion** — each states a checkable line; no "looks good".
- [x] **Clever scenarios designed so baseline plausibly FAILS** — S5–S8, S10.
- [x] **Matches talent type** — discipline → PRESSURE scenarios carrying a plausible excuse
      ("they're both small", "we grepped the whole codebase", "the count came back zero").
- [x] **Negative trigger covered** — exactly one (S10), neighbour verified on disk.
- [x] **Dead cross-refs / invented commands / `name:` / description bounds / portability** —
      checked, see Structural review.
- [x] **Technical claims fact-checked, hardest on DDL cost claims** — see Accuracy review.

## Scenarios

## S1 — Canonical column rename, mixed fleet · application (normal)
- **Input:** "Rename `users.name` to `users.full_name`. 40M rows, Postgres, the API runs on
  ~30 pods behind a rolling deploy that takes ~20 minutes. Give me the plan."
- **Pass criterion (observable):** The answer (i) refuses the single-commit
  `ALTER TABLE ... RENAME COLUMN` and names the specific failure — during the rollout window
  old pods execute `SELECT name` against a table where `name` no longer exists (Common-mistakes
  row 1); (ii) lays out the sequence expand → dual-write → backfill → switch reads → contract
  with **one deploy per phase** (step 2, Rules line 1); (iii) makes `full_name` nullable at
  expand (step 3); (iv) states that at no instant does either an old pod or a new pod see a
  missing column, and names the rollback for each phase. Fails if any two phases share a deploy,
  or if `full_name` is added `NOT NULL` without a default.
- **Baseline (without talent):** A capable model generally knows add-backfill-switch-drop and
  will usually produce something close to correct here — this is the textbook case and is in
  every migration blog post. Baseline typically gets phases 1–3 right; the sloppy half is
  collapsing switch-reads and drop into "then clean up later", which this criterion does not
  score.
- **With talent:** Steps 1–8 produce exactly this, and the Example section walks this precise
  rename end to end, including the old-version-pod read/write check as the step 3 gate. **PASS.**

## S2 — New required field in an API request · application (normal)
- **Input:** "Our `POST /orders` needs a new mandatory `fulfilment_channel` field. Web, an
  iOS app on a 4-week review-plus-adoption tail, and two partner integrations call it. How do
  we ship it?"
- **Pass criterion (observable):** The answer (i) applies the same phase discipline to an API,
  not a database — ship the field **optional first**, accept requests with and without it,
  migrate callers, and only then make it required (Example, "same five phases, non-SQL");
  (ii) identifies the iOS app and the partners as consumers not deployable by the team and
  derives the removal/enforcement window from **their** upgrade tail, not from the team's deploy
  time (step 1); (iii) never proposes making the field required in the same release that adds it.
  Fails if the answer is DB-specific advice, or if "required" lands before consumer adoption is
  measured.
- **Baseline (without talent):** Usually right in outline — "add it optional, then make it
  required" is common knowledge — though baseline often picks the enforcement date by feel
  ("give it a month") rather than by a measured count of requests still missing the field.
- **With talent:** Step 1's inventory column "how long until its slowest instance is upgraded"
  and step 3's "no new required field in a request" cover it directly; the method is stated over
  shapes and readers, not over tables, so nothing has to be translated. **PASS.**

## S3 — Additive-only field, no history to fill · application (normal)
- **Input:** "We're adding `signup_source` to new accounts. It only has meaning going forward —
  there is no way to derive it for the 2M existing rows. Do we still need the whole five-phase
  ritual?"
- **Pass criterion (observable):** The answer drops the phases that do not apply and says which
  and why: no dual-write (nothing old is being replaced), **no backfill** (no historical value
  exists to compute), leaving expand + readers-tolerate-absent — and it must state that readers
  have to handle the field being NULL for old rows **permanently**, not transiently (step 2
  "No historical data → no backfill"; step 3 "readers must tolerate the new shape being absent").
  Fails if it prescribes all five phases anyway, or if it invents a backfill value.
- **Baseline (without talent):** Typically fine — baseline rarely over-ceremonies a pure
  addition. The point of scoring it is the "NULL forever, not transiently" half, which baseline
  states about half the time.
- **With talent:** Step 2 explicitly instructs dropping unneeded phases and names this exact
  case as one of the three drops. **PASS.**

## S4 — Event payload change with a queue in the middle · application (normal)
- **Input:** "Our `order.created` events carry `amount_cents`. We want to carry a
  `{amount, currency}` object instead. Producers and consumers are separate services; SQS with
  a 14-day retention sits between them. When can producers stop emitting `amount_cents`?"
- **Pass criterion (observable):** The answer (i) has producers emit **both** shapes while
  consumers read new-with-fallback-to-old (step 6.1, Example non-SQL paragraph); (ii) ties the
  earliest stop-emitting date to the **queue's retention window** for already-enqueued messages,
  not to the consumer deploy finishing (step 4, in-flight messages paragraph); (iii) requires an
  observed zero — a fallback/old-shape-consumed counter at 0 across that window — before
  producers drop the old field (step 6.2 gate). Fails if the answer is "once consumers are
  deployed, producers can stop".
- **Baseline (without talent):** Usually gets emit-both and consumer-fallback, and often
  mentions draining the queue. Baseline plausibly passes this; where it is thinner is turning
  "drained" into a measured counter rather than an assumption, and it commonly omits that
  redrive from a dead-letter queue can reintroduce messages older than the retention window —
  a point the file makes ("retention plus redrive age") but that this criterion does not require.
- **With talent:** Step 4's queue paragraph and step 6's two-sub-step read switch map onto this
  directly and supply the redrive rider as well. **PASS.**

## S5 — "The backfill is done, the count came back zero" · pressure (clever, baseline fails)
- **Input:** "Backfill finished. It ran 6h10m over 41M rows. Final verification:
  `SELECT count(*) FROM users WHERE name IS NOT NULL AND full_name IS NULL` → **0**, run right
  after the job exited. We're calling it verified and switching reads to `full_name` in
  tomorrow's release. Sign off?"
- **Pass criterion (observable):** The answer must NOT accept the single terminal count as proof,
  and must demand all four of: (1) a **tail pass** over rows changed during the 6h window
  (`updated_at > job start`, or the CDC/changelog stream over the run) **re-run until it returns
  zero** (step 5.4 "repeat until the pass finds zero"); (2) a **sampled correctness assertion**
  `transform(old) == new`, because presence is not correctness and a job that filled every row
  with the wrong transform passes every null check (step 5.5, Common-mistakes row "Non-null
  count = 0 treated as backfill correct"); (3) confirmation that the writes were **conditional**
  (`WHERE full_name IS NULL` / CAS on empty), since an unconditional backfill can have written a
  value read at 02:00 over a live write at 05:00 — stale over fresh, and invisible to any null
  count (step 5.2, step 7 bullet 1); (4) confirmation that **step 4's dual-write gate was green
  before the job started**, since otherwise an old-only writer reopened the tail behind the job
  (step 5 preamble). It must also route the residual risk to step 6.1 — deploy the **fallback
  read with a counter** rather than jumping to new-only. Fails if it signs off, or if it demands
  only the tail pass and treats the count as covering correctness.
- **Baseline (without talent):** Very likely signs off. "Zero rows where old is set and new is
  null, over the whole table" reads like an airtight proof, and it *is* airtight for one thing
  only — presence at that instant. Baseline has no reason to separate presence from correctness,
  and almost never asks whether the writes were conditional, which is where the 6-hour run
  actually hurts: the rows most likely to be wrong are the live ones the job raced.
- **With talent:** The method refuses the sign-off on three independent grounds and names the
  next observable step instead of a date. Note for the record: with a green step-4 gate and
  conditional writes, the full assertion *does* establish presence — the tail pass earns its
  place against the straggler-writer and stale-write cases, not against presence. The talent
  still gets the decision right; see Accuracy review A2 for the rationale wording.
  **PASS. Beats baseline.**

## S6 — "Ship switch-reads and stop-dual-write together, they're both small" · pressure (clever, baseline fails)
- **Input:** "Both changes are three lines. Release is Thursday, the next train is in two weeks,
  and holding a half-migrated state for another sprint is its own risk. Put the read switch and
  the removal of the old write in one PR."
- **Pass criterion (observable):** The answer refuses and names the concrete mechanism, not a
  slogan. It must state that the **rollback for switch-reads is "point reads back at the old
  shape", and that rollback is only valid while dual-write is still running** (step 6 Rollback,
  Rules line "Only because dual-write is still on"). Combining them means: from the instant the
  release lands, the old shape stops receiving writes and begins going stale, so reverting reads
  to it serves **silently outdated data** rather than failing loudly — a correctness incident,
  not an outage. It must also note that during the rollout itself the fleet is mixed, so old-code
  pods still reading the old shape see records that the new pods created and never wrote there.
  Fails if the refusal is generic ("one phase per deploy is best practice") without naming the
  destroyed rollback and the stale-read consequence.
- **Baseline (without talent):** Often agrees, and the excuse is a good one — both diffs really
  are small and the two-week train is a real cost. Baseline reasons about diff size and test
  coverage, which are both fine here; the failure is invisible at review time because nothing
  breaks *unless* you need to roll back. Some baselines will say "do them separately" as a
  general instinct but cannot say what specifically breaks, which this criterion requires.
- **With talent:** The dependency is stated as a rule and repeated in Common mistakes ("Switch
  reads and stop dual-write in the same deploy → reads cannot be rolled back; the old shape is
  now stale"), and step 8a gives the honest alternative — ship the read switch Thursday, stop
  writing old on the next train, since 8a is itself reversible. **PASS. Beats baseline.**

## S7 — "We grepped the whole codebase, nothing reads it" · pressure (clever, baseline fails)
- **Input:** "`rg 'legacy_status'` across all 6 repos → 0 hits outside the migration itself.
  The field is dead. Dropping the column in tomorrow's deploy."
- **Pass criterion (observable):** The answer rejects grep as evidence and must (i) name the
  concrete classes of reader grep cannot see — `SELECT *`, dynamic/attribute access (`row[name]`),
  ORM lazy-loads, reflection and generic serializers, saved queries, dashboards and notebooks,
  ETL/warehouse jobs, and clients outside the repos searched (step 8, Common-mistakes row
  "Grep proves no readers"); (ii) require **measured reads of the old shape at 0**, from
  instrumentation on the access path tagged by caller, sustained over a window **longer than the
  longest consumer's release cycle and longer than the slowest periodic job's period** — the
  quarterly-report case (step 8 evidence 1); (iii) require the remaining two evidence items —
  permissions/grants revoked with nothing breaking, and a **dark-removal rehearsal** behind a
  flippable flag before the real drop (step 8 evidence 2–3); (iv) treat 8b as the one-way door
  shipped alone. Fails if it accepts grep plus a short soak, or omits the window-sizing rule.
- **Baseline (without talent):** Commonly accepts it, or hedges to "wait a couple of weeks and
  add logging" — which is the right shape with the wrong sizing. The specific failure baseline
  makes is a window sized by deploy cadence (days) against consumers whose cadence is a quarter,
  and it rarely proposes a rehearsal that can be undone in seconds.
- **With talent:** Step 8 makes all three evidence items mandatory and pre-empts the "possibly
  unbounded" client tail with an explicit fork — version the interface, or publish a hard sunset
  and accept breakage knowingly. **PASS. Beats baseline.**

## S8 — Non-invertible split: `name` → `{first_name, last_name}` · pressure (clever, baseline fails)
- **Input:** "Same migration, but we're splitting into `first_name` and `last_name`. We're in
  dual-write. New code writes the two fields natively from the signup form; old code still writes
  `name`. QA found 300 records where `first || ' ' || last != name`. Which one is right, and how
  do we resolve them?"
- **Pass criterion (observable):** The answer must (i) give the single-source-of-truth rule
  explicitly — **the old shape is authoritative until reads switch**, so during this phase `name`
  wins and the split fields are derived (step 7 opening); (ii) refuse last-writer-wins and refuse
  an automatic merge — the 300 records are **logged as conflicts with record ids, not overwritten**,
  and the transform gets fixed (step 7 bullet 3); (iii) recognise the transform is non-invertible
  and demand an explicit written decision on the authoritative direction **per phase**, because
  new code writing the pair natively means the pair now carries information `name` cannot
  represent (step 7 bullet 4, "where 'both are the source of truth' quietly becomes 'neither is'");
  (iv) state that divergence caught before the read switch is cheap and after it is a
  data-correctness incident. Fails if it picks a winner heuristically ("prefer the split fields,
  they're newer"), or silently rewrites `name` from the pair.
- **Baseline (without talent):** Typically produces a plausible reconciliation heuristic —
  split on the last space, prefer the newer row, backfill the disagreements — which is exactly
  the failure. It resolves 300 visible conflicts by writing over data, and it does not notice
  that letting new code write the pair natively while `name` is still authoritative means the two
  populations will keep diverging for as long as dual-write runs.
- **With talent:** Step 7 answers the question asked ("who is source of truth") with a rule
  rather than a heuristic, and forbids the merge. Gap noted for sharpening: step 8a's
  reversibility ("backfill the *old* shape for records created in the meantime") silently assumes
  a defined new→old transform, which for a lossy split is exactly the thing that does not exist —
  see Accuracy review A4. That does not change this scenario's outcome. **PASS. Beats baseline.**

## S9 — Five phases where none are needed · edge (clever)
- **Input:** "I'm renaming a struct field `retryCnt` → `retryCount` in our worker. It's an
  in-memory field on a single binary, deployed as one unit — the old process is stopped and the
  new one started, never both. It is never serialised, never persisted, and nothing outside the
  process reads it. Walk me through expand-contract."
- **Pass criterion (observable):** The answer must **decline the ceremony** and say so plainly:
  rename it in one commit. It must justify the decline against the file's own condition — no
  instant of mixed old/new can exist, single deploy unit replaced whole, nothing persisted in
  that shape (step "When NOT to use", bullet 1) — and it should name the cost of doing it anyway
  (Common-mistakes last row: weeks of double bookkeeping and a permanent half-migrated field for
  no exposure). Fails if it produces a five-phase plan, or hedges into "you could do a
  lightweight version of expand-contract".
- **Baseline (without talent):** Baseline also passes this — asked to rename a private in-memory
  field, a capable model renames it. Claiming a baseline win here would be false. What this
  scenario measures is the talent's own failure mode: a phase-gated discipline invoked by name
  ("walk me through expand-contract") pulling a five-phase plan onto a change with zero exposure.
  The talent must not make the answer *worse* than baseline, and it does not.
- **With talent:** The file gates itself before step 1, listing three explicit not-this cases and
  restating the discipline in Rules ("Prefer fewer phases when no mixed-fleet instant can exist —
  but decide it from step 1's inventory, not from optimism"), so the decline is derived from the
  inventory rather than asserted. **PASS.**

## S10 — Retried payment capture runs twice · negative-trigger
- **Input:** "During yesterday's canary rollout our payment worker timed out and the queue
  redelivered the message; the customer was charged twice. Two in-flight messages hit two
  different worker versions. How do we make sure a capture that runs a second time doesn't
  double-charge? Nothing about the message format or the DB schema is changing."
- **Pass criterion (observable):** The talent does NOT fire. The answer must decline to open the
  expand/dual-write/backfill/contract sequence and must route to **`idempotent-action-design`**,
  naming it. Fails if it starts a reader/writer inventory or proposes dual-writing anything —
  there is no old and new shape here, only one shape and two executions.
- **Baseline (without talent):** Not a capability discriminator — this scenario measures
  over-triggering, not skill.
- **With talent:** The bait is deliberate and dense: "canary", "rolling deploy", "in-flight
  messages", "two worker versions", "the queue redelivered" are all live trigger phrases in this
  talent's description, and the mixed-version fleet is genuinely present. The routing survives it
  because the discriminator is a *shape change*, and there is none. Both the description's
  NOT-clause ("NOT for making a single side effect safe to run twice after a retry or crash —
  use idempotent-action-design") and the When-NOT-to-use block state the hand-off, with the sharp
  line "a perfectly idempotent migration still crashes old readers" marking the boundary from the
  other side. Neighbour verified present on disk at
  `/home/user/skills-repo/.claude/skills/idempotent-action-design/SKILL.md`, and its own
  description carries the matching triggers ('double-charged', 'at-least-once', 'is this safe to
  re-run'). **PASS. Beats baseline.**

## Accuracy review (a) — technical claims, fact-checked
Verified claim by claim against the file. **No factual error found.** Four sharpening notes,
all non-blocking:

- **DDL / locking claims — checked hardest, and they hold.** The file never asserts that any DDL
  operation is universally cheap. Step 3 states a *directive* ("no long lock on a hot table") and
  hedges the index build as "concurrently/online **as the store supports**" — correct, since
  `CREATE INDEX CONCURRENTLY` (Postgres) cannot run inside a transaction block and can leave an
  INVALID index on failure, MySQL 8.0 online DDL has its own algorithm matrix, and SQLite has
  neither. Nothing is claimed about those specifics, so nothing is wrong.
  `DROP COLUMN` being a one-way door recoverable only from backup (step 8b) is correct in the
  operational sense that matters, including on Postgres where the drop is metadata-only but the
  data becomes inaccessible. The `OFFSET` warning (step 5.1) is correct — offset pagination shifts
  under concurrent inserts/deletes and degrades quadratically; keyset/watermark ranging is the
  right fix. Queue handling (step 4) is correct, including the rider that consumers must accept
  the old format for **retention plus redrive age**, which is the part people miss: a DLQ redrive
  can reintroduce a message far older than the nominal retention window. Conditional writes
  (`WHERE new IS NULL` / CAS-on-empty) with a version-or-`updated_at` guard, and the explicit
  `migrated_at` sentinel for when empty is a legitimate value (step 7 bullet 2), are correct and
  unusually well-specified.
  *Rider worth adding (A5):* "nullable **or defaulted**" is correct as a *compatibility* rule
  (old writers omit the column, the default fills it), and readers may over-read it as also being
  the *cheap* option. Adding a defaulted column is metadata-only on PG ≥ 11 and MySQL 8.0
  `ALGORITHM=INSTANT`, but rewrites the whole table under an exclusive lock on PG ≤ 10. One clause
  — "defaulted is free on modern engines, a full rewrite on older ones; check yours" — would close
  the only place a reader could infer a cost claim the file does not make.
- **A1 — `fleet lag` as one number applied to every gate is overgeneralized.** Step 1 defines it
  as the max over *all* processes and says it "sets every gate window below". But the relevant
  population differs per gate: the dual-write gate (step 4) is bounded by the **writer** fleet's
  rollout, while the read-switch (step 6) and contract (step 8) gates are bounded by the
  **reader/consumer** tail. The Example bakes the conflation in — it holds the dual-write gate at
  zero for six weeks because a *partner integration* releases every six weeks, even though the
  partner writes through an API the team itself deploys. The error direction is conservative
  (safe but expensive), and it can inflate a routine rename into a quarter-long project. Suggested
  fix: "fleet lag is per gate — take the max over the processes that gate actually depends on."
- **A2 — the stated rationale for the tail pass is slightly over-claimed.** Common-mistakes row
  "Verifying coverage with one pass → rows written during the run are missed" is not strictly true
  for *presence*: if step 4's gate is green (no writer writes old-only) and step 5.2 writes
  conditionally, rows written during the run already carry both shapes, and a single full
  assertion on an MVCC snapshot does establish presence. What the tail pass genuinely catches is
  (i) a straggler writer that step 4's gate missed, (ii) rows where the backfill's stale read lost
  a race and wrote an outdated value — presence intact, correctness gone — and (iii) stores with
  no consistent snapshot for a long scan (sharded/eventually-consistent, or a count run against a
  lagging replica). The prescription is right and cheap; only the "why" is imprecise. Sharpening
  the reason would make the rule harder to argue away.
- **A3 — step 4's gate metric is unsatisfiable for a legitimately-empty value.** "Count with the
  new shape missing must be 0" assumes NULL means unmigrated. Step 7 bullet 2 already supplies the
  fix (`migrated_at` stamp or schema-version field) but only in the backfill context; step 4's
  gate does not point at it, so a team whose transform can legitimately produce NULL will chase a
  count that never reaches zero.
- **A4 — step 8a's reversibility claim needs a rider for non-invertible transforms.** "Reversible:
  turn dual-write back on, then backfill the *old* shape" presumes a defined new→old transform.
  For the lossy directions step 7 itself names (splitting one field into two, type narrowing),
  that inverse may not exist or is lossy — `first + ' ' + last` does not round-trip
  "Mary Anne van der Berg". 8a is still *more* reversible than 8b; the claim just is not
  unconditional. See S8.

## Structural review (b)
- **Frontmatter:** `name: expand-contract-migration` present and **matches the directory**
  `.claude/skills/expand-contract-migration/`. `description:` present. OK.
- **Description bounds:** 1374 characters — under the 1536 limit. Triggers-only and third
  person throughout ("Use when…", "Keeps old and new simultaneously valid…"); no second-person
  address, no method exposition. Carries four explicit NOT-routings. OK.
- **Dead cross-references — every named sibling verified on disk:**
  `idempotent-action-design` ✓, `writing-plans` ✓, `data-contract-assertions` ✓,
  `behavioral-spec-mining` ✓, `integration-contract-completeness` ✓, `library-curator` ✓
  (named in the repo section). Six for six, no rot.
- **Invented slash-commands / built-ins:** none. A grep for `/<word>` tokens returns nothing;
  the file's only commands are illustrative SQL fragments, and it says so explicitly
  ("Every command in the example is illustrative, not prescribed").
- **Format drift:** tests live in this `evals.md`; no `evals/` directory. OK.
- **Repo-instance paths verified:** `pipeline/frontier.json` ✓, `pipeline/metrics.jsonl` ✓,
  `pipeline/ledgers/` ✓ (5 ledgers). The claim that both loops read/write them checks out —
  `frontier.json` is referenced from `pipeline/BUILD.md`, `BRAIN.md`, `ROUTING.md`, `DATA.md`
  and root `CLAUDE.md`. The frontmatter claim (`name`/`description` read by the runtime loader,
  so an added field must be ignorable first) is correct and is a real instance of step 3's
  unknown-field rule.

## Portability (c)
Domain-agnostic in its bones: the method is stated over "shapes", readers, writers and deploy
units, and the Example closes with an explicit non-SQL pass (API required field, event payload,
config key) — S2, S3 and S4 confirm it transfers without translation. The repo-specific content
is fenced in one clearly-labelled section at the end, not smuggled into the steps.
One genuine lean: **step 5 is the SQL-flavoured section.** Batching, watermarks and conditional
writes each carry a non-SQL gloss ("compare-and-set on empty, create-if-absent"), but the *tail
pass* is defined only via `updated_at` or a CDC stream — neither of which exists for an object
store or a flat file layout, where the equivalent is a listing diff by `LastModified` over the
run window. One clause would close it. Not a portability failure; a polish note.

## Overlap (d)
**A concrete task whose right handler is genuinely ambiguous exists — one, and it is with
`idempotent-action-design`:**

> "Make our nightly backfill job safe to kill and restart mid-run."

Both talents claim it, and neither routes it. `expand-contract-migration` step 5.1–5.3 owns it
directly (persisted watermark, conditional writes, resumable and stoppable mid-run).
`idempotent-action-design` owns it just as directly — its description triggers on 'resume from
where it stopped', 'the job died mid-write', 'half-applied batches', and its step 8 is
"Reconcile after any interruption, before resuming anything". The hand-off is **one-directional
and partial**: expand-contract defers to the neighbour only for *dual-write* keying ("Dual-write
must be idempotent per record — see `idempotent-action-design` for keying"), never for the
backfill job; and `idempotent-action-design`'s NOT-list does not mention expand-contract at all.
Suggested fix (cheap, no merge): add one clause to expand-contract step 5 — "for the job's own
crash-safety and reconciliation, `idempotent-action-design`; this step owns only what the
migration requires of it" — and a matching NOT-clause on the neighbour.

**No overlap with the other two.** `writing-plans` produces a plan *document* for an engineer
with no context; expand-contract supplies the *content* of one particular plan. The two compose
(write the phase sequence, then hand it to `writing-plans` to render) rather than compete, and no
task I could construct has an ambiguous owner. `data-contract-assertions` is cleanly on the other
side of the boundary: it gates data *arriving from someone else*, while expand-contract changes
a shape *you own*; both files state the split, and expand-contract's Complements line points at
the correct sequencing (assert the new shape's quality once it is authoritative).

## Failure triage (if any scenario failed)
No scenario failed; no triage required. The four Accuracy-review notes (A1–A4) plus the DDL
rider (A5), the step-5 portability clause and the overlap clause are **sharpening items, not
failures**: none of them makes the talent wrong, and none makes it net-negative against
baseline on any scenario in this suite. Recommend routing them to the author as polish.

## Result summary
- Scenarios passed: 10/10 · failure_cause: none · verdict: passed
