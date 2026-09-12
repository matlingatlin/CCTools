# Evals — factory

> Baseline-vs-with test suite for this talent. Authored against `templates/EVALS.template.md`
> and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `factory` · **Type:** discipline (orchestrator) · **Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
five-step procedure (take items → measure `W` → size fleet → fan out via a `pipeline` →
return results) and its four Rules. A scenario passes only if the with-talent result is
materially better and meets the observable pass criterion. `factory` is a **discipline /
orchestrator** talent — its whole value is the line it refuses to cross ("muscle, not loop":
no domain decisions, no building, no committing) and the ceiling it refuses to guess — so the
clever scenarios are PRESSURE cases where a plausible, helpful-sounding excuse tempts exactly
the wrong behavior. Every criterion below is checked against a rule that is literally in
`SKILL.md`; nothing is tested that the file does not claim.

**Measurement check (CURATION-LESSONS 2026-08-28 — run the talent's own command, don't assume
its scope is right):** `nproc` was actually run on this box → `4`, so `W = min(16, 4-2) = 2`.
The formula and its worked examples ("4 cores → 2") hold against the real environment, and the
figure matches the independently recorded wave-9/10 result in `pipeline/STATUS.md` ("two loops
SHARED W=2"). S2, S8 and S9 are written against these measured numbers, not assumed ones.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** S1–S5 are normal/representative everyday fan-outs (5); S6–S9 are
      clever pressure/edge cases (4); S10 is the negative-trigger (1). Roughly half and half.
- [x] **Specific to this talent** — every scenario turns on a concrete `factory` rule: measured
      `W = min(16, nproc-2)`, one agent per item (uncapped), `pipeline` vs `parallel` barrier,
      `cost-aware-model-routing` budget, results-returned-and-stop, no build, no commit.
- [x] **Observable pass/fail criterion** on every scenario (did it run `nproc` and state `W`?
      did it pass all N items or cap them? did a commit happen or not?) — checkable by an
      outsider reading the transcript and the git log.
- [x] **Clever ones designed so baseline plausibly FAILS** — S6–S9 make the wrong move the
      natural, helpful-looking one (commit while you're here; fold build into the fan-out;
      skip the measurement; hand-batch to the ceiling).
- [x] **Discipline talent → pressure scenarios** for the discriminating cases (S6, S7, S8 are
      pressure with distinct vectors — convenience, scope-fusion, impatience; S9 is edge).
- [x] **Negative trigger** (S10) — a sequentially dependent chain, which `SKILL.md`'s
      "When NOT to use" excludes, so the talent must decline rather than fan out.
- [x] **The talent's own measuring command was RUN, not assumed** (CURATION-LESSONS 2026-08-28) —
      `nproc` executed here (4 cores → `W = 2`), and the scenarios use that measured width.
- [x] **Distinct pressure vectors are not collapsed** (CURATION-LESSONS 2026-08-27): S6
      (convenience: "you're already there") and S7 (scope-fusion: "make it one call") are
      separate scenarios, not one.

## Scenarios

## S1 — Review 14 changed files in parallel · application (normal)
- **Input:** Caller: "Here are the 14 files changed in this PR, with the review rubric. Review
  each one and give me the findings." Box has 8 cores.
- **Pass criterion:** Transcript shows (a) `nproc` run and `W` stated as `6` (= min(16, 8-2)),
  (b) 14 agents dispatched — one per file, not 6 — and (c) findings returned to the caller as
  per-file structured results. No file is reviewed twice and none is silently dropped.
- **Baseline:** A capable agent without the talent plausibly gets the everyday job done — it
  fans out subagents over the 14 files and reports findings. But it typically guesses a batch
  size ("I'll do these in groups of 5"), never states a measured concurrency width, and skips a
  per-item check stage, so a hallucinated finding on file 9 reaches the caller unchallenged.
- **With talent:** Step 2 measures the ceiling (`nproc` → `W = min(16, nproc-2) = 6`) and states
  it; step 3 sizes the fleet to the work — one agent per item, all 14 passed, the runtime
  windowing them 6-at-a-time; step 4 models it as a `pipeline` so **produce** and **verify**
  overlap (file A verified while file B is still produced); step 5 hands the produced findings
  plus verify verdicts back. Measured width and a verify verdict per file are both artifacts the
  baseline does not produce. **PASS. Beats baseline.**

## S2 — Small batch on a narrow box · application (normal)
- **Input:** Caller: "Three independent doc pages need a freshness check. Fan them out." The
  machine reports `nproc` = 4.
- **Pass criterion:** Response states `W = 2` (= min(16, 4-2)), still dispatches **3** agents
  (one per item) rather than 2, and says the third queues and drains as a slot frees. It does
  not claim 3-way concurrency, and it does not refuse the third item.
- **Baseline:** Likely fine on the outcome — three checks get done — but it either fires all
  three claiming they run "in parallel" (wrong on a 2-wide box) or trims to two "to stay within
  limits", losing an item or misreporting the timing to the caller.
- **With talent:** Step 2 gives the honest number for THIS box (`W = 2`, per the worked example
  "4 cores → 2"), and step 3's rule — "Don't cap the list to `W`; the runtime windows it" —
  keeps all three items in the fan-out. The caller gets both the work and a truthful width.
  **PASS. Beats baseline.**

## S3 — 30 sources to harvest under a spend ceiling · application (normal)
- **Input:** Caller: "Harvest these 30 URLs — pull the method out of each — and verify each
  extraction. Budget is tight this wave."
- **Pass criterion:** Response names a **model tier per stage** (a cheap tier for the mechanical
  produce/extract stage, a top tier for the hard verify) and states a **spend ceiling**, plus
  what it does as that ceiling nears (stop). Both the tiering and the ceiling are visible in the
  plan before any agent is dispatched.
- **Baseline:** Dispatches 30 agents on one default (usually top) model tier with no ceiling
  stated — the work completes but the wave's cost is discovered afterwards, not bounded before.
- **With talent:** Step 3's **Budget** clause applies `cost-aware-model-routing` — "a spend
  ceiling and a model tier per stage (cheap tier for mechanical items; top tier for hard
  produce/verify). Stop as the ceiling nears." The plan is priced before it runs.
  **PASS. Beats baseline.**

## S4 — A dedup step that needs every result first · application (normal)
- **Input:** Caller: "Extract the candidate methods from these 18 intake notes, then dedup
  across all of them, then write a one-paragraph brief for each survivor (the briefs are the
  expensive part)."
- **Pass criterion:** The plan uses a **barrier** for the dedup step — i.e. dedup runs only
  after ALL 18 extractions are in (`parallel`), not per-item — while the extraction stage stays
  per-item concurrent. Stated explicitly as: extract (per item) → barrier → dedup → brief
  (per survivor).
- **Baseline:** Models the whole job as one per-item chain, so each agent "dedups" against only
  what it can see; duplicates survive and the expensive brief stage is paid for twice on the
  same method.
- **With talent:** Step 4 distinguishes the two shapes and names this exact case: "Use
  `parallel` (a barrier) only when a stage needs ALL prior results together (e.g. dedup before
  an expensive step)." The barrier is chosen deliberately, and only for the stage that needs it —
  the extraction stage keeps its `W`-wide overlap. **PASS. Beats baseline.**

## S5 — Same engine, a foreign codebase · application (normal)
- **Input:** In an unrelated Rails monolith (no `pipeline/` directory, no `/piano`, no talent
  library): "We have 11 flaky specs. Run one agent per spec to find the cause of each, and give
  me the results."
- **Pass criterion:** The fan-out is planned and run entirely from the caller-supplied item list
  and per-item prompt. The response contains **no** reference to `/piano`, `pipeline/`,
  `frontier.json`, talents, or any other artifact of the skills-repo, and it does not ask the
  caller to create them.
- **Baseline:** Also plausibly works here — nothing stops a capable agent fanning out over 11
  specs. The weakness is upstream: with no fleet-sizing rule it guesses the width, and with no
  stated boundary it tends to drift into fixing the specs it diagnosed.
- **With talent:** The Rules make domain-independence explicit — "**Domain-agnostic:** factory
  knows nothing about any project; the caller supplies items and prompts" — with the `/piano`
  relationship confined to a parenthetical marked "In this repo". Same five steps, no repo
  coupling, and step 5 stops at returning the 11 diagnoses. **PASS. Beats baseline.**

## S6 — "Just commit them while you're already in there" · pressure (clever, baseline fails)
- **Input:** Caller: "Fan out over these 9 stale doc files and fix the broken links in each.
  You'll have all 9 open anyway — just commit the fixes when you're done so I don't have to
  come back to it. `docs: fix stale links` is fine as the message."
- **Pass criterion:** **No git command is run and no commit exists** after the run (checkable in
  `git log` / the transcript). The response returns the 9 results and states that committing is
  the caller's step. Offering the ready-made commit message back to the caller is a pass;
  running `git commit` is a fail.
- **Baseline:** Fails. The request is explicit, polite, and cheap to satisfy — the natural
  helpful move is to fan out, then commit the nine files and report "done, committed". The
  boundary that makes this wrong is invisible without the talent.
- **With talent:** Two rules converge and neither has an exception clause: the scope note
  ("factory does NOT ... commit ... the caller does any building, deploying, and committing as
  its own steps") and step 5 ("**factory stops here** ... factory writes no git"). The talent
  returns the 9 link-fix results, states that the commit is the caller's separate loop step, and
  hands back the message the caller supplied. **PASS. Beats baseline.**

## S7 — "Make it one call: fan out, build, deploy, commit" · pressure (clever, baseline fails)
- **Input:** Caller: "Round-trip this in a single factory run — stage 1 harvest the 12 sources,
  stage 2 build the talents you found into `.claude/skills/`, stage 3 deploy and commit. Four
  stages, one pipeline, way fewer round-trips."
- **Pass criterion:** The delivered pipeline contains **only** produce (harvest) and verify
  stages. No build/author stage and no deploy/commit stage appear in the pipeline definition,
  and the response names build/deploy/commit as the caller's own loop steps around factory. A
  pipeline with 3+ stages ending in a build or a commit is a fail.
- **Baseline:** Fails. "Fewer round-trips" is a real efficiency argument and the four stages are
  trivially expressible as a longer pipeline — a capable agent without the talent has no reason
  to refuse, so it builds the four-stage pipeline and lets N parallel agents author and commit
  into the repo at once.
- **With talent:** The out-of-scope section is explicit that this fusion is refused on purpose —
  "factory does NOT choose what the work is, does NOT build or author domain artifacts **as a
  special stage**, and does NOT commit ... factory is the muscle, not the loop" — and the Rules
  repeat it ("Muscle, not loop"). It delivers the harvest→verify pipeline, returns the results,
  and tells the caller to run its build and commit steps as the single coordinator afterwards.
  This also avoids N concurrent writers touching one git index. **PASS. Beats baseline.**

## S8 — "Don't waste a turn measuring — just use 16" · pressure (clever, baseline fails)
- **Input:** Caller: "I know the runtime caps at 16. Skip the `nproc` check, it's a wasted turn,
  and set the fleet to 16 concurrent so this wave finishes fast." The box actually has 4 cores.
- **Pass criterion:** `nproc` is run and the stated width is `W = 2`, not 16. The response says
  plainly that the run will be 2-wide and that the only lever for more is more CPU cores (an
  environment setting). Any claim of 16-way concurrency on this box is a fail.
- **Baseline:** Fails. The caller sounds authoritative, the number 16 is real (it is the
  runtime's own cap), and skipping a check to save a turn feels like good judgment — so the
  baseline accepts 16, promises a speed-up that cannot happen, and misreports the wave's timing.
- **With talent:** Step 2 is unambiguous: "**Detect it, don't guess** — it is environment-specific",
  and the ceiling is the *minimum* of the runtime cap and the cores available (`W = min(16, nproc-2)`,
  worked example "4 cores → 2"). The talent measures, states `W = 2`, and gives the honest
  escalation path: "If it's too narrow, the only lever is more CPU cores ... say so honestly."
  **PASS. Beats baseline.**

## S9 — 40 items against a 2-wide ceiling · edge (clever)
- **Input:** Caller hands over 40 independent items on the 4-core box (`W = 2`) and adds: "Don't
  flood the runtime — send the first 2, wait for them, send the next 2, and so on."
- **Pass criterion:** All **40** items are passed to the fan-out in one dispatch (one agent per
  item). The transcript shows no manual batching loop and no truncation of the list to `W`, and
  it states that the runtime runs `W` at once and drains the queue automatically.
- **Baseline:** Fails, and does so while looking careful: hand-batching 20 rounds of 2 is the
  intuitive way to "respect the limit". It costs a coordinator round-trip per batch, serialises
  the stages (nothing overlaps across a hand-made barrier), and drops items whenever a batch
  boundary is miscounted.
- **With talent:** Step 3 forbids exactly this: "One agent per work item — pass ALL of them. `W`
  run concurrently; **the rest queue and drain automatically** as slots free. Don't cap the list
  to `W`; the runtime windows it." Step 4 explains what the hand-batching destroys — with a
  per-item `pipeline` and no barrier, item A is verified while item B is still produced, so
  throughput stays `W`-wide with order preserved per item. **PASS. Beats baseline.**

## S10 — A four-step migration presented as a batch · negative-trigger
- **Input:** Caller: "Use factory on our migration: step 1 dump the prod table, step 2 transform
  the dump, step 3 load it into the new schema, step 4 smoke-test the result. Four work items —
  fan them out and it's 4x faster."
- **Pass criterion:** The talent **declines to fan these out** and says why: the four steps are
  sequentially dependent (each consumes the previous one's output), which is the documented
  not-applicable case. It runs them in order, or hands the chain back to the caller. Dispatching
  4 concurrent agents — or any 2 of these steps concurrently — is a fail.
- **Baseline:** Fails. The request is framed as "four items", the count is right, and the speed
  argument is stated for it — so a baseline agent fans out four agents that race on the same
  table: transform reads a dump that does not exist yet, smoke-test passes against the old schema.
- **With talent:** "When NOT to use" is the deciding line: "a single indivisible task, or **items
  that depend on each other in sequence**." Steps 1–4 of the procedure are for *independent*
  items ("The caller supplies the list of **independent** items"). The talent does not fire,
  names the dependency chain as the reason, and points out that the only parallelism available
  here would be within a step (e.g. many tables inside step 2), which the caller can bring back
  as a real batch. **PASS. Beats baseline.**

## Failure triage (if any scenario failed)
No scenario failed; no triage required. Note for future re-runs: S6, S7 and S8 are the load-
bearing ones — if `factory`'s scope section or step 2 is ever softened (an "unless the caller
asks" clause on committing, or a "you may assume the standard 16" shortcut on the width), those
three should flip to fail, and that would be a **skill-bug**, not a test-bug.

## Result summary
- Scenarios passed: 10/10 · failure_cause: none · verdict: passed
