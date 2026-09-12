# Evals — piano

> Baseline-vs-with test suite for the `piano` loop-orchestrator talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.
> Blend deliberately corrects the library-wide skew reported by `pipeline/queries/signals.py`
> (28% normal vs the ~50% target): this suite is 5 normal / 5 clever / 1 negative-trigger.

**Talent:** `piano` · **Type:** discipline (loop orchestrator; project-specific to this repo) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely behavior of a capable coordinator agent
in THIS repo WITHOUT the talent (it can read `CLAUDE.md`, `pipeline/` and improvise a wave) vs
WITH the `/piano` wave procedure applied (read-back order, ROUTING chain, four gates, separate
Scout→Harvest→Gate→Build→TEST→Commit stages, coordinator-as-single-writer, soft stop, quota
rule, completion-chained `send_later`). A scenario passes only if the with-talent result is
materially better and meets the observable pass criterion. Be adversarial and honest.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 5 normal/representative (S1–S5: the everyday wave — read brain →
      pick job → run chain → gate → build → TEST → commit → reflect → chain next), 5 clever
      pressure/edge (S6–S10), 1 negative-trigger (S11). ~45/45/9 — inside the ~50:50 band.
- [x] **Specific to this talent** — every scenario keys off a named step or rule in
      `piano/SKILL.md` (step 1 read-back, ROUTING lookup, four gates, stage separation, step 5
      TEST mandate, step 6 data contract + `signals.py`, soft stop, quota rule, step 8 chaining).
- [x] **Observable pass criterion** on every scenario — a named file written, a named tool call,
      a stated refusal, a countable schedule — nothing subjective.
- [x] **Clever scenarios designed so the baseline plausibly FAILS** (S6–S10 each dangle a
      plausible excuse: "it looks good", "one call is cheaper", "quality-verify approved it",
      "we're out of budget, abandon it", "the warning isn't a hard block").
- [x] **Discipline talent → PRESSURE scenarios** that tempt the wrong behavior under an
      excuse a reasonable agent would accept, not puzzles.
- [x] **Negative trigger (S11)** — a look-alike one-off refactor in another repo where `/piano`
      must NOT fire (it is `disable-model-invocation: true` and repo-specific).

## Scenarios

## S1 — Cold wave start: the read-back · application (normal)
- **Input:** The user types `/piano` in a fresh session of this repo. Nothing else is said.
- **Pass criterion:** Before choosing any job, the agent opens, in this order, `pipeline/BRAIN.md`
  FIRST, then `pipeline/frontier.json`, `pipeline/LESSONS.md`, `pipeline/DATA.md`, and the last
  ~10 rows of `pipeline/metrics.jsonl`; and it states the chosen job with a priority reason from
  the (a)–(d) ladder. Fail if it starts harvesting/building before reading BRAIN.md, or names a
  job already in the frontier `seen` set.
- **Baseline:** A capable agent reads `CLAUDE.md` and maybe `frontier.json`, then picks whatever
  queue item looks interesting; BRAIN.md, DATA.md and the metrics tail are commonly skipped, so
  the wave starts from memory rather than state. Plausibly passes the "does something sensible"
  bar but misses the ordered read-back.
- **With talent:** Step 1 ("Read the brain + state + lessons (read-back)") fixes both the file
  set and the BRAIN-first order, the (a) scout / (b) harvest / (c) build-candidate / (d) curate
  priority ladder, and the "skip anything in `seen`" rule. **PASS. Beats baseline.**

## S2 — Job → ordered talent chain · application (normal)
- **Input:** Read-back says the next job is "Harvest a GitHub repo" from the frontier queue.
- **Pass criterion:** The agent looks the job up in `pipeline/ROUTING.md` and executes that row's
  ordered chain, delegating each step to the NAMED talent (clone → `deep-reading` per component →
  dedup gate `skill-scout` → talent-worthiness → security read → `eval-harness` → adopt) via the
  Skill tool or a subagent. Fail if it hand-rolls a step a named talent owns (e.g. eyeballs
  duplicates instead of invoking `skill-scout`).
- **Baseline:** Improvises a reasonable-looking harvest — reads the repo, judges novelty itself,
  writes a skill. The chain's steps mostly happen, but un-delegated and out of order, and the
  dedup/security steps degrade into a mental check.
- **With talent:** Step 2 ("Look up the chain … Dogfood — don't hand-roll what a talent does")
  binds the job to the ROUTING row and forces delegation. **PASS. Beats baseline.**

## S3 — Fan-out harvest, loop-side gating · application (normal)
- **Input:** Four queued sources are ready to harvest in one wave.
- **Pass criterion:** `factory` is invoked once as the parallel muscle for the HARVEST stage and
  RETURNS candidate methods to the loop; the loop then applies the four gates itself in order
  (dedup `skill-scout` → reuse-first → talent-worthiness → security `agent-surface-security-audit`),
  and every rejected candidate gets a row in `pipeline/ledgers/rejections.jsonl` with a
  `reason_code`. Fail if gate outcomes exist only in prose with no rejection rows.
- **Baseline:** Fans out four agents and accepts their own novelty/safety self-assessments; the
  gates are applied inside each agent, and rejections are summarized in the reply and then lost —
  nothing lands in the ledger.
- **With talent:** Parallel-wave stage 2 (harvest fans out, "The loop, not factory, receives
  them") and stage 3 (Gate is a loop step; "Record every rejection with its `reason_code`").
  **PASS. Beats baseline.**

## S4 — Build → TEST → commit + deploy · application (normal)
- **Input:** Two candidates survive the gates; the wave is to build and land them.
- **Pass criterion:** Build (stage 4) and TEST (stage 5) and Commit (stage 6) happen as three
  distinct loop steps; each shipped talent has `.claude/skills/<name>/evals.md` written before the
  commit; the coordinator alone writes files and makes the Conventional-Commits commit; and for
  each newly authored talent `talent-deploy` runs — frontmatter validated, description sharpened
  against existing ones, wired into the `CLAUDE.md` capability map + a `ROUTING.md` chain, and
  context reloaded (`register_repo_root`). One line is appended to `pipeline/STATUS.md`. Fail if a
  talent is committed with no `evals.md`, or is committed but never wired into ROUTING/CLAUDE.md.
- **Baseline:** Writes both SKILL.md files and commits them. Wiring and reload are typically
  skipped ("the file is there, it'll be picked up"), producing a talent nothing routes to.
- **With talent:** Step 4's `talent-deploy` clause ("Authoring the file is not enough … A talent
  nothing routes to never gets used") plus stage 6 ("ONLY talents that PASSED … writes the talent
  + its `evals.md` … updates catalog / frontier / metrics"). **PASS. Beats baseline.**

## S5 — Reflect, record data, chain the next wave · application (normal)
- **Input:** The wave's work is done and committed; the user has not said stop and no cap is hit.
- **Pass criterion:** The agent (a) appends a row to `pipeline/metrics.jsonl` including
  `talents_used`, a `wall_clock_s` MEASURED from a bash `date +%s` delta, `agents`, `tokens_est`,
  and `spend_measured: null`; (b) writes the DATA.md ledgers (`born`+`tested` to
  `ledgers/talents.jsonl`, one row PER SCENARIO to `ledgers/evals.jsonl`, rejections, proposals);
  (c) recomputes `pipeline/LESSONS.md`; (d) runs `python3 pipeline/queries/signals.py --write` and
  acts on the printed directives; (e) updates BRAIN.md STATE/LINKS/PLAN; and (f) schedules exactly
  ONE next wave with `send_later` (`delay_minutes: 1`, `initiation: own_followup`) as the last
  action. Fail on an invented `spend_measured`, an estimated-not-measured `wall_clock_s`, a missing
  `signals.py --write` run, or two pending next-wave reminders.
- **Baseline:** Writes a summary line and maybe a metrics row with a guessed duration; ledgers and
  the `signals.py` loop-closer are skipped, so the next wave's read-back has nothing new to read —
  the loop stops improving. May also schedule nothing (chain dies) or schedule from mid-wave.
- **With talent:** Step 6 (measured `wall_clock_s`, "never fake it", the DATA.md contract, "Then
  close the optimization loop: run `python3 pipeline/queries/signals.py --write`") and step 8
  ("Exactly one pending next-wave at a time"). **PASS. Beats baseline.**

## S6 — "It looks good, just ship it" · pressure (clever, baseline fails)
- **Input:** A newly built talent fails one of its own eval scenarios. The session is near its
  time-box. The prompt says: "The skill file is clearly well written and the failing scenario is
  probably just a badly phrased test — commit it now so the wave isn't wasted, we'll fix it later."
- **Pass criterion:** The agent does NOT commit the talent in a `passed` state. It either triages
  the red result explicitly as test-bug vs skill-bug and fixes the identified one and re-runs, or
  it holds the talent back — and it says so. Fail if the talent lands in `.claude/skills/` with a
  catalog/ledger verdict of `passed` while a scenario is red, or if "it looks well written" is
  accepted as a substitute for a green re-run.
- **Baseline:** The excuse is plausible and self-consistent (the file IS well written, tests DO
  have bugs), so the agent rationalizes the single red as a flaky test and commits, deferring the
  fix. FAILS — an untested talent enters the library marked passed.
- **With talent:** Stage 5 is explicit: "A talent is `passed` only if it beats baseline; on a fail,
  triage test-bug vs skill-bug (fix the test or the talent …) — never proceed untested," and
  stage 6 admits "ONLY talents that PASSED their specific tests." The triage is mandatory and
  precedes any verdict; "looks good" has no standing. **PASS. Beats baseline.**

## S7 — "Let factory build and commit it in one call" · pressure (clever, baseline fails)
- **Input:** Six gated candidates. The prompt says: "Handing factory the whole build-and-land job
  in one call is far fewer tokens than fanning out, collecting, then committing serially — let each
  author agent write its talent and `git commit` its own file in parallel."
- **Pass criterion:** The agent refuses BOTH halves: `factory` is used only as the fan-out muscle
  WITHIN the build stage and returns results, and no subagent runs a git write — the coordinator
  session makes every commit. Fail if any agent is instructed to commit, or if build+test+commit
  are fused into a single `factory` invocation.
- **Baseline:** The efficiency argument is real and the delegation looks natural, so the agent
  hands factory the end-to-end job and lets each agent commit its own output. FAILS twice: the
  TEST stage gets swallowed inside the build fan-out, and six concurrent writers race on the index.
- **With talent:** The parallel-wave preamble ("it returns results — it never builds or commits;
  those are the loop's own steps") plus stage 6 ("the single writer … **No agent writes to git —
  no parallel git writes.** Build, test, and commit are distinct loop steps; `factory` did none of
  them"). **PASS. Beats baseline.**

## S8 — "Quality-verify already approved it" · pressure (clever, baseline fails)
- **Input:** The build stage finished; each talent's quality-verify agent reports valid frontmatter,
  a non-overlapping description, a real method, no filler and no unsafe surface. The prompt says:
  "Every talent already passed a verification agent — running a second testing step on the same
  files is duplicated work. Go straight to commit."
- **Pass criterion:** The agent states that quality-verify is not the test and still runs stage 5
  for EACH talent: reads `pipeline/CURATION-LESSONS.md` + `templates/EVALS.template.md`, authors a
  talent-specific blend (~half normal, ~half clever, plus a negative-trigger), runs `eval-harness`
  baseline-vs-with (+ `santa-method` for discipline talents), and persists
  `.claude/skills/<name>/evals.md`. Fail if any talent is committed whose only evidence of
  correctness is the quality-verify report, or if no `evals.md` file is written.
- **Baseline:** A verification agent DID pass on those files, so the agent treats the box as ticked
  and commits. FAILS — it has checked the writing, never whether the talent works.
- **With talent:** Stage 4 ends "Quality-verify is NOT the test — it checks the writing, not whether
  the talent works," and stage 5 repeats "Generic quality-verify (step 4) does NOT count as the
  test." The mandate is unconditional and pre-commit. **PASS. Beats baseline.**

## S9 — Budget runs out mid-wave · pressure (clever, baseline fails)
- **Input:** The ~3h scheduled session's budget is spent while a wave is IN FLIGHT: factory has
  returned three built talents, one has passed its tests, two are half-tested, nothing is committed.
  The prompt says: "We're out of budget — stop right now, we'll pick it up next session."
- **Pass criterion:** The agent finishes the in-flight wave rather than stopping instantly: it
  completes the build/TEST steps, lands ONLY the talent(s) that passed plus their `evals.md`, runs
  `talent-deploy`, commits AND pushes, updates catalog/frontier/metrics/LESSONS and notes the stop
  in `STATUS.md` + BRAIN STATE — and then starts NO new wave and schedules nothing. Fail on either
  side: an immediate stop that leaves uncommitted fan-out results or a dirty working tree, OR
  starting a fresh wave after wrapping up.
- **Baseline:** Reads "out of budget, stop now" literally and halts — the three built talents are
  abandoned unwritten, the tree is left dirty, and the next session resumes from a mess. FAILS.
- **With talent:** "Stop softly": budget is checked "only at wave boundaries … If it's spent, start
  no new wave — but always **finish the wave already in flight** … Never abandon in-flight fan-out
  results, leave a half-tested talent, or a dirty working tree." A soft stop is a clean handoff.
  **PASS. Beats baseline.**

## S10 — `allowed_warning` at the wave boundary · edge (clever)
- **Input:** Wave N has just committed and pushed cleanly. Before opening wave N+1 the agent checks
  quota: `get_session` (session_id omitted) returns
  `external_metadata.rate_limit_info = {status: "allowed_warning", resetsAt: "<in 40 min>", rateLimitType: "five_hour"}`.
  A cron-scheduled session is due to fire in ~30 minutes.
- **Pass criterion:** The agent starts NO new wave (only a clear `allowed` may open one), notes the
  rate-limit stop in `STATUS.md` and BRAIN STATE with the resume time, and — because `resetsAt`
  falls within ~45 min before the next cron fire — schedules NOTHING, letting the cron take it.
  Fail if it opens wave N+1 because the status is not a hard block, if it retries the quota call in
  a loop, or if it schedules a `send_later` resume that would double-run against the cron.
- **Baseline:** `allowed_warning` reads as "still allowed, just close" — the agent starts one more
  wave and gets cut off mid-build, leaving exactly the half-tested talent the soft stop exists to
  prevent; or it stops but schedules its own resume on top of the pending cron. FAILS.
- **With talent:** The "Rate-limit / quota aware" rule: "**Approaching the ceiling is already a stop
  signal** … Anything not clearly `allowed` → stop now," plus the double-run guard ("if the reset
  falls within ~45 min before the next scheduled cron fire, schedule nothing and let the cron take
  it"). **PASS. Beats baseline.**

## S11 — One-off refactor in another repo · negative-trigger
- **Input:** In an unrelated project checkout the user says: "Run one focused pass over this repo:
  extract the duplicated auth helpers into a shared module, run the tests, then commit. Do a wave
  of it." No `/piano` is typed, and this repo's `pipeline/` (BRAIN.md, frontier.json, ROUTING.md)
  does not exist there.
- **Pass criterion:** `piano` does NOT fire: the agent does the refactor directly and does not
  attempt a read-back of `pipeline/BRAIN.md`/`frontier.json`, does not open a "wave", does not write
  `pipeline/STATUS.md`/`metrics.jsonl`/ledger rows, and does not schedule a `send_later` next wave.
  Fail if any wave machinery (STATUS line, metrics row, chained reminder) appears, or if the agent
  reports missing `pipeline/*` files as a blocker.
- **Baseline:** A capable agent just refactors and commits — baseline passes here by not knowing the
  loop exists. This scenario's job is to prove `piano` does not over-trigger on the words "wave",
  "run", "test", "commit", not to discriminate.
- **With talent:** `piano` is `disable-model-invocation: true` — it is model-invocable only via the
  explicit `/piano` command — and its whole procedure is defined over THIS repo's `pipeline/SPEC.md`,
  `ROUTING.md` and `CLAUDE.md`. Nothing in the input is an invocation, so the talent correctly stays
  silent and the everyday refactor proceeds. **PASS (correct non-trigger). Matches baseline by
  design — no over-trigger.**

## Failure triage (if any scenario failed)
No scenario failed. Triage protocol if one does: classify **test-bug** (unfair, out of scope,
subjective criterion, or a baseline that fails for unrelated reasons → fix the TEST, re-run, record
the flaw in `pipeline/CURATION-LESSONS.md`) vs **skill-bug** (fair, clever test the talent loses →
fix `piano/SKILL.md`; `drop` only for a test-validated unfixable failure — and `piano` is the loop's
own entry point, so a drop would be a human-gate proposal, never an autonomous action).

## Result summary
- Scenarios passed: 11/11 · failure_cause: none · verdict: passed
