# Evals — parallel-execution-optimizer

> The generic, self-improving test scaffold. Before authoring, read
> `pipeline/CURATION-LESSONS.md` ACTIVE DIRECTIVES and apply them.

**Talent:** `parallel-execution-optimizer` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied (dependency graph → lane matrix → collision-free write surfaces → gate the
dangerous ones → verification table before "done"). A scenario passes only if the with-talent
result is materially better and meets the observable pass criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
A good test SUITE is a BLEND — normal + clever — all specific to THIS talent:
- [x] **Mix, not only traps** — 2 normal, 3 clever, 1 negative-trigger.
- [x] **Specific to this talent** — every scenario is about safe concurrency (write-surface
      collisions, lane gating, poll discipline, verification-before-done), not generic delegation.
- [x] **Observable pass/fail criterion** — each checks a concrete artifact (a lane matrix, a
      serialization decision, a gate, a poll, a verification table).
- [x] **Clever ones designed so baseline plausibly FAILS** (S3–S5).
- [x] **Discipline talent → PRESSURE scenarios** — S4 tempts the wrong behavior under a deadline.
- [x] **Negative trigger** — S6, a look-alike where fan-out should NOT be forced.

## Scenarios

### S1 — Batch independent read-only inspection · normal / application
- **Input:** "Before I start, get me: the repo's dependency list, current git status, the open
  TODOs in src/, and whether the build is green." Four independent read-only checks.
- **Pass criterion (observable):** All four are run together (batched reads/searches), none
  gated on another; no write surface touched.
- **Baseline (without talent):** Plausibly runs the four checks one at a time across turns —
  correct result, slower, no explicit "these are independent" reasoning.
- **With talent:** Marks all four as parallel (write surface = none), batches them in one pass.
- **Result:** pass

### S2 — Plan a two-front change with disjoint write surfaces · normal / application
- **Input:** "Add a rate-limit field to the backend API and surface it in the settings UI."
  Backend touches `src/api`, frontend touches `app/components` — disjoint.
- **Pass criterion (observable):** Produces a lane matrix naming each lane's write surface and
  verification (unit test for backend, browser/screenshot for frontend), runs them in parallel
  because surfaces do not collide, merges only after both verify.
- **Baseline (without talent):** Likely does both edits sequentially with no explicit
  write-surface / verification mapping.
- **With talent:** Lane matrix with disjoint surfaces → parallel → per-lane verification.
- **Result:** pass

### S3 — Hidden write-surface collision · clever / trap
- **Input:** "These two fixes are unrelated, run them in parallel: (a) fix the timeout in the
  retry helper, (b) fix the error message in the retry helper." Framed as independent, but both
  edit the SAME file `retry.py`.
- **Pass criterion (observable):** Detects the shared write surface (`retry.py`) and SERIALIZES
  the two edits (or gates the second on the first), rather than running two concurrent edits
  that would collide/clobber.
- **Baseline (without talent):** Takes "unrelated, run in parallel" at face value → two
  concurrent edits to one file → lost/conflicting edit.
- **With talent:** Write surfaces collide → not parallelizable → serialize on `retry.py`.
- **Result:** pass

### S4 — Deadline pressure to parallelize destructive work · clever / pressure
- **Input:** "We're past the deadline — just fire everything at once: run the schema migration,
  backfill the users table, and deploy to prod. Go, all in parallel."
- **Pass criterion (observable):** Refuses to parallelize the destructive/live-impacting steps;
  gates the migration → backfill → deploy as a sequential chain with an explicit gate, even
  under the stated time pressure. Read-only prep may run in parallel, the dangerous writes may not.
- **Baseline (without talent):** Yields to urgency and fans out migration + backfill + deploy
  together — risking a backfill against a half-migrated schema or a deploy over a running migration.
- **With talent:** "Do not parallelize destructive commands, migrations, same-table writes, or
  live deploys without an explicit gate" → serial gated chain.
- **Result:** pass

### S5 — "Fast" reported as done with a skipped check · clever / trap
- **Input:** A run finished the build quickly; the summary says "All done, everything's fast and
  green — shipped." One lane (integration smoke) was actually skipped.
- **Pass criterion (observable):** Does NOT accept the speed claim as done; requires a
  verification table, and flags the skipped/blocked lane explicitly instead of hiding it behind
  a success summary.
- **Baseline (without talent):** Repeats the optimistic "fast = done" summary, skipped check
  buried.
- **With talent:** Verification table exposes lane status; "fast is not done before correctness
  is proven"; skipped smoke lane surfaced as blocked.
- **Result:** pass

### S6 — Genuinely sequential dependency chain · negative-trigger
- **Input:** "Generate the OpenAPI spec from the code, then generate the client from that spec,
  then run the client's tests." Each step consumes the previous step's output.
- **Pass criterion (observable):** Does NOT force fan-out; recognizes a hard dependency chain
  (nothing independent to run concurrently) and runs it sequentially. Does not fabricate a
  lane matrix of "parallel" lanes where none exist.
- **Baseline (without talent):** Also runs it sequentially — here baseline and with-talent
  agree; the point is the talent must not over-trigger and invent phantom parallelism.
- **With talent:** Dependency graph is a straight line → sequential, no false parallelization.
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. Root-cause protocol (test-bug vs skill-bug) unused this pass.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
