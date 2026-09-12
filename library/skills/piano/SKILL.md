---
name: piano
description: Use when the user starts or continues the self-playing piano — the autonomous talent-factory run. Invoke with /piano to run one wave, or /loop /piano to run continuously.
disable-model-invocation: true
---

# /piano — the self-playing piano orchestrator

Run ONE wave of the talent factory, then report and either continue or stop.
This is the brain's entry point. Follow `pipeline/SPEC.md`, `pipeline/ROUTING.md`,
and the standing rules in `CLAUDE.md`. You are the coordinator: track-agents produce,
you commit.

> **Invocation:** this talent carries `disable-model-invocation: true` on purpose — it is an
> orchestrator, not something a task should auto-trigger into. A caller does not "load" it;
> a caller RUNS the workflow script that makes this method executable, or follows the method
> by hand. Wording elsewhere that says "hand it to X" means running X's script.

## One wave

1. **Read the brain + state + lessons (read-back).** Open `pipeline/BRAIN.md` FIRST (the shared
   control tower — STATE/ownership, cross-agent LINKS, the PLAN, OPTIMIZE directives), then
   `pipeline/frontier.json` (queues + seen-set), `pipeline/LESSONS.md` (source-yield),
   `pipeline/DATA.md` (the data contract — what this wave must record), and the last ~10 rows
   of `pipeline/metrics.jsonl`. Apply the curator→build LINKS at the TEST step;
   at the end of the run, UPDATE BRAIN.md (STATE done, any new LINK, refresh the piano PLAN line). Pick the next job by priority — (a) research-scout if source
   queues are low, (b) harvest a queued source, (c) process a build-candidate, (d) curate —
   **but let the lessons override the raw queue order**: deprioritized source types drop
   down, seek-more shapes rise. This read-back is what makes the loop improve each wave.
   Skip anything in `seen`.

2. **Look up the chain.** Find the job in `pipeline/ROUTING.md` and run its ordered
   talent chain, delegating each step to the named talent (via the Skill tool or a
   subagent). Dogfood — don't hand-roll what a talent does.

3. **Apply the four gates** (`CLAUDE.md`) at their points: dedup → reuse-first →
   talent-worthiness → security. A candidate that fails any gate does NOT become a
   talent (it stays a knowledge note, or is skipped, with the reason logged).

4. **Coordinator commit.** Fan-out agents return data; YOU write results to the repo
   (catalog decision, new talent into `.claude/skills/`, knowledge note, or intake
   file) and commit with a Conventional-Commits message. Update the `seen` set.

   - **If this wave authored/adopted a talent → `talent-deploy`.** Authoring the file is
     not enough: validate frontmatter, sharpen its description vs existing ones, wire it
     into the CLAUDE.md capability map + ROUTING chain, and **reload context**
     (`register_repo_root`) so it activates live for the next wave. A talent nothing
     routes to never gets used.

5. **Update `pipeline/STATUS.md`** — append one line: date, wave, job, outcome
   (adopted X / cataloged Y / skipped Z + reason), and what's next.

6. **Reflect + record data (`wave-reflect` + the data contract).** Append this wave's row to
   `pipeline/metrics.jsonl` — including `talents_used`, the **measured** `wall_clock_s` (bash
   `date +%s` delta across the wave) and `agents` (count spawned), and `tokens_est` (honest
   estimate; `spend_measured` stays `null` until a metered path exists — never fake it). Then
   write the ledgers per **`pipeline/DATA.md`** (the collection contract): a `born`+`tested`
   event to `ledgers/talents.jsonl` and one per-scenario row to `ledgers/evals.jsonl` for each
   shipped talent; a per-candidate row to `ledgers/rejections.jsonl` for each gated-out
   candidate (with a `reason_code`); a row to `ledgers/proposals.jsonl` for anything raised to
   the human gate; a row to `ledgers/claims.jsonl` for every claim an agent made, written WHEN
   YOU VERIFY IT (with `verified_how` naming what you actually checked) — this is the only
   record of whether the agents grading our work are accurate, and it is gone the moment the
   wave ends; and on any `defects.jsonl` row, the `family` + `silent` fields, so defects become
   predictive rather than merely counted. Recompute `pipeline/LESSONS.md` (source-yield, prune/sharpen flags,
   diminishing-returns). Capture cost/time/history LIVE — they can't be reconstructed later.
   **Then close the optimization loop:** run `python3 pipeline/queries/signals.py --write` — it
   recomputes the objective signals FROM the ledgers and rewrites BRAIN §0, and act on the
   directives it prints (e.g. blend-skew → add normal scenarios next TEST). This is what makes
   the read-back data-driven, not from memory; it is what step 1 of the NEXT wave reads back.

7. **Loop-safety check (`loop-design-check`).** Decide continue or stop:
   - STOP if: the user said stop, a wave-budget cap is hit, the last 2 waves added
     nothing new (diminishing returns — `wave-reflect` writes this to LESSONS), a wave
     errored, or something irreversible needs the user's approval.
   - **Human gate:** before anything irreversible (merge/delete a talent, push outward,
     destructive change) — ask the user first. Everything else (harvest, eval,
     adopt-into-library, sharpen descriptions, commit) is auto-allowed and reversible.

8. **Chain the next wave (completion-triggered).** THIS is how the loop advances — not a
   fixed clock. As the LAST action of the wave:
   - **If continuing:** schedule exactly one next wave with `send_later`
     (`delay_minutes: 1`, `initiation: own_followup`, message = the `/piano` wave prompt).
     The next wave fires only because this one finished — sequential, never overlapping.
   - **If stopping:** do NOT schedule anything. State the stop reason. If it's a human
     gate or an error, surface it to the user; if diminishing returns, say the loop is
     paused and can be resumed with `/piano`.
   - **Exactly one** pending next-wave at a time. Before scheduling, if a next-wave
     reminder is already pending, do not add a second (no fan-out of waves).

## Stop softly (graceful shutdown — bounded/scheduled runs)
When a run is time-boxed (e.g. the ~3h scheduled session) or a stop condition hits, stop
**between waves, never mid-wave**:
- Check the budget **only at wave boundaries.** If it's spent, start no new wave — but always
  **finish the wave already in flight**: complete its build/TEST steps, land only the talents
  that PASSED their tests plus their `evals.md`, `talent-deploy` them, and **commit + push**.
  Never abandon in-flight fan-out results, leave a half-tested talent, or a dirty working tree.
- End on a **consistent, committed, pushed state** with catalog/frontier/metrics/LESSONS
  updated, so the next scheduled session resumes from a clean line — not a mess.
- A soft stop is a clean handoff, not an interrupt. Same if asked to stop early: wrap up the
  current wave, commit, then stop.
- **Rate-limit / quota aware (checked at the wave boundary, like the time budget).** Before
  starting a NEW wave, read the run's quota state (in this harness: `get_session` with
  `session_id` omitted → `external_metadata.rate_limit_info` = `{status, resetsAt, rateLimitType}`).
  `allowed` → run the next wave. **Approaching the ceiling is already a stop signal** — start no
  new wave, because being cut off mid-wave leaves the half-tested talent a soft stop exists to
  prevent. Anything not clearly `allowed` → stop now. If a call is rate-limited mid-work, treat
  it as the stop signal; never retry in a loop. On a quota stop: finish the in-flight unit,
  commit+push, note in `STATUS.md` + BRAIN STATE that it stopped on rate-limit and when it
  resumes, then **schedule exactly ONE resume just after `resetsAt`** (`send_later`). Guard
  against double-runs: if the reset falls within ~45 min before the next scheduled cron fire,
  schedule nothing and let the cron take it. A quota stop is a pause with a known wake-up.
  **Check WHICH window is warning** (`rateLimitType`) — several are enforced at once and the
  binding one changes as windows reset. A SHORT window (minutes/hours) → pause and resume after
  `resetsAt`, as above. A LONG window (days/weekly) → do NOT pause: waiting days is an outage,
  not a pause. Instead THROTTLE — smaller waves, less fan-out, longer gaps — so the remaining
  budget lasts to the distant reset, and SURFACE it to the user: spending the rest of a weekly
  budget overnight is their call, not the loop's.

## Parallel wave (fan-out) — the loop owns the stages; `factory` is the muscle
A wave is NOT one agent doing steps serially, but it is also NOT one monolithic `factory`
call. **The loop (this skill) owns the stages and runs them as SEPARATE parts; `factory` is
used only as the parallel fan-out muscle WITHIN a stage** (it returns results — it never
builds or commits; those are the loop's own steps). Stages, in order:
1. **Scout (producer):** `research-scout` generates sources/terms → the frontier never dries up.
2. **Harvest (fan-out by running `pipeline/workflows/factory-wave.workflow.js`):** give the
   script the queued sources; it fans out one
   agent per source (clone/inventory) and RETURNS candidate methods. The loop, not factory,
   receives them.
3. **Gate (loop step):** the loop applies the four gates to the returned candidates —
   dedup (`skill-scout`) → reuse-first → talent-worthiness → security
   (`agent-surface-security-audit`). Only survivors proceed. **Record every rejection** with
   its `reason_code` to `ledgers/rejections.jsonl` (per `DATA.md`) — the WHY behind the counts.
4. **Build (SEPARATE loop step, fan-out by running `pipeline/workflows/factory-wave.workflow.js`):**
   give the script the gated candidates;
   it fans out one author agent per talent (`writing-skills` + the right `templates/` scaffold)
   then a **quality-verify** agent each (valid frontmatter, non-overlapping description, method,
   no filler, no unsafe surface). Quality-verify is NOT the test — it checks the writing, not
   whether the talent works.
5. **TEST (SEPARATE loop step — MANDATORY, before any commit):** first **read the shared
   test-authoring brain** — `pipeline/TEST-AUTHORING-LESSONS.md` (ACTIVE DIRECTIVES) +
   `templates/EVALS.template.md` — and apply them, so the loop writes tests as well as the
   curator has learned to. Then for EACH built/adopted talent, **create SPECIFIC tests for it**
   — a BLEND tailored to what it claims to do: ~half normal/representative (does it do its
   everyday job?) and ~half clever/adversarial (traps, planted defects, edge), plus a
   negative-trigger (discipline talents get pressure scenarios; technique talents get
   application scenarios). Run `eval-harness` **baseline-vs-with-talent** (+ `santa-method` for
   discipline talents). **Persist** as `.claude/skills/<name>/evals.md`. A talent is `passed`
   only if it beats baseline; on a fail, **triage test-bug vs skill-bug** (fix the test or the
   talent; drop only a test-validated unfixable skill) — never proceed untested. **Write back:**
   fold any test-authoring lesson this wave surfaced (a flawed-test pattern, a recurring
   overlap) into `pipeline/TEST-AUTHORING-LESSONS.md` so the curator and future waves share it — one
   brain, not two silos. Generic quality-verify (step 4) does NOT count as the test. **Emit the
   data:** one row PER SCENARIO to `ledgers/evals.jsonl` (kind normal/adversarial/negative,
   baseline pass|miss, with pass|catch, result) and a `tested` event to `ledgers/talents.jsonl`
   (scenarios, adversarial count, verdict) — per `DATA.md`, so test-discrimination is queryable.
6. **Commit + deploy (SEPARATE loop step — the single writer):** ONLY talents that PASSED their
   specific tests. The coordinator (this session) writes the talent + its `evals.md`, runs
   `talent-deploy` (wire + reload), updates catalog (`test: passed`) / frontier / metrics, and
   makes the commit(s). **No agent writes to git — no parallel git writes.** Build, test, and
   commit are distinct loop steps; `factory` did none of them.

The security gate runs on every candidate; a `cost-aware-model-routing` budget bounds the
fleet; irreversible actions hit the human gate. Because harvest and build are separate loop
steps (not fused inside factory), the loop is free to harvest one wave and build the next, or
do both in one wave — its choice, not factory's.

## Maintenance (curation) — improve what's already in place, not just grow
Growing the library (harvest/build) is only half the loop; the other half is keeping the
adopted tier healthy. Every few waves (or when the health scorecard degrades), run a
**curation pass** via `library-curator`: it fans out one auditor per adopted talent
(test-coverage → write missing `evals.md`; sharpen overlapping descriptions; cut filler;
enforce portability; check freshness), applies the reversible fixes, and proposes merges/prunes
for the human gate — then the coordinator commits and appends a health scorecard. Interleave
curation with harvest/build so the library is constantly tested and improved, not just added to.

## Continuous run — completion-chained (default)
Each wave triggers the next **only when it completes**, via a one-shot `send_later` that
re-delivers `/piano` into this same session (step 8). This is sequential by construction:
wave N+1 cannot start until wave N has finished and scheduled it. State persists in git,
so each wave resumes from the frontier; the chain survives container reclaim because the
`send_later` reminder is durable. To STOP the chain: tell the piano to stop, or delete the
pending next-wave reminder — no wave reschedules on a stop condition. (A fixed-interval
cron is deliberately NOT used: it would fire regardless of whether the previous wave
finished, risking overlap.) `/loop /piano` remains available for self-paced runs inside an
interactive session.

## First-run note
`research-scout` and `library-curator` are BUILT and adopted (they have their own ROUTING
chains — use them). Three brain-talents remain on the build backlog in `pipeline/BUILD.md`:
`dedup-guardian`, `pipeline-engine`, `talent-router`. Until those exist, run waves with the
talents we have (harvest → deep-reading → gates → eval-harness → adopt) over the remaining
catalog, and author the missing ones through the factory as their own jobs (reuse-first →
writing-skills → eval → adopt).
