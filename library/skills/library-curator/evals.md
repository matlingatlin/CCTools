# Evals — library-curator

> Baseline-vs-with test suite for this talent. Authored against `templates/EVALS.template.md`
> and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `library-curator` · **Type:** discipline (maintenance orchestrator) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely behaviour WITHOUT the talent (a capable
agent asked to "look after the skills library") against the behaviour WITH its procedure,
priority ladder and rules applied. A scenario passes only if the with-talent result is
materially better AND meets the observable pass criterion.

`library-curator` is a **discipline / orchestrator** talent: its value is not a clever
transformation but a set of refusals and orderings under pressure (never prune for disuse,
triage before dropping, irreversible work behind a human gate, stop only at batch boundaries).
So the clever scenarios are **PRESSURE scenarios** — each hands the agent a plausible excuse to
do the fast, wrong thing, and passing means the discipline holds anyway. The normal scenarios
cover the everyday pass: inventory → score → NEW/stale first → write blended evals → land
reversible fixes → record + scorecard.

**Blend of this suite (deliberate).** `pipeline/queries/signals.py` reports the library's test
blend as SKEWED — ~28% normal against a ~50% target, with adversarial cases dominating. This
suite is authored to pull that back: **6 normal / 6 clever / 1 negative-trigger** (46% normal),
not a trap-heavy suite.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** S1–S6 are the everyday maintenance job; S7–S12 are pressure/edge;
      S13 is the negative trigger. ~Half and half by design (see blend note above).
- [x] **Specific to this talent** — every scenario turns on a named rule, step or priority line
      in `library-curator`'s SKILL.md (disuse ≠ prune, triage-before-drop, never-runs-dry,
      reversible-auto/irreversible-asks, single writer, stop-softly, the data contract). No
      generic boilerplate.
- [x] **Observable pass/fail criterion** on every scenario — each is a checkable artifact or a
      checkable absence (a file written or not written, a proposal row vs a deletion, a commit
      before stopping, a scorecard field present), never "handles it well".
- [x] **Clever ones designed so the baseline plausibly FAILS** — S7–S12 each make the wrong move
      the natural, defensible one (tidy up the unused skill, believe the red test, report
      "nothing left to do", delete the source after consolidating, merge the obvious duplicate,
      stop the second the budget runs out).
- [x] **Discipline talent → pressure scenarios** for the discriminating cases (checklist rule,
      and `CURATION-LESSONS` directive "match scenario type to talent type").
- [x] **Negative trigger** (S13) — a look-alike request that is *growth*, not maintenance.
- [x] **Verify-before-delete** (`CURATION-LESSONS` 2026-08-27) is itself tested — S10.

## Scenarios

## S1 — Inventory and health scorecard for a 58-talent library · application (normal)
- **Input:** "Run a curation pass over `.claude/skills/`." The library holds 58 adopted talents;
  28 have an `evals.md`, 30 do not; 3 were edited after their last eval date; 2 hard-code this
  repo's paths in the method body.
- **Pass criterion (observable):** The pass produces a scorecard containing **all six** metrics
  named in Procedure step 1 — % with tests, % passing latest eval, # overlapping descriptions,
  # unused, # project-welded, # stale — as numbers over the 58 units, AND a work order in which
  the 30 untested and 3 stale units come **before** any already-tested unit. Auditing a tested
  unit ahead of an untested one is a fail.
- **Baseline (without talent):** Picks a handful of skills that look interesting or were touched
  recently, reviews them ad hoc, reports prose impressions. No before-picture, no counts, no
  reproducible priority — so the next pass cannot tell whether the library got healthier.
- **With talent:** Procedure step 1 (inventory + score) plus the **Priority** ladder ("NEW first:
  units with no `evals.md` … and units changed since their last eval"); the scorecard is both the
  before-picture and the priority signal, and step 2 fans out one auditor per unit via `factory`.
  **PASS. Beats baseline.**

## S2 — A newly adopted talent has no tests · application (normal)
- **Input:** `hybrid-parse-escalation` was adopted last wave. It has a SKILL.md and no
  `evals.md`. It is first in the NEW queue.
- **Pass criterion (observable):** An `evals.md` is written at
  `.claude/skills/hybrid-parse-escalation/evals.md` that contains (a) roughly half
  normal/representative scenarios and roughly half clever/adversarial ones, (b) **at least one
  negative-trigger** scenario, (c) a baseline and a with-talent outcome for every scenario, and
  (d) an observable pass criterion per scenario. A suite that is all traps, all happy-path, or
  missing the negative trigger fails this scenario.
- **Baseline (without talent):** Writes 3–4 "does it work?" happy-path checks, or (following the
  house instinct that tests should be hard) an all-adversarial set. Either way the blend and the
  negative trigger are missing, and no baseline comparison is recorded — so the suite cannot show
  the talent earns its place.
- **With talent:** Check 1 ("Test coverage — write a GOOD, BLENDED suite … ~half normal … ~half
  clever … plus a negative-trigger — then baseline-vs-with"), authored from
  `templates/EVALS.template.md` after reading `CURATION-LESSONS` ACTIVE DIRECTIVES (Procedure
  step 0). **PASS. Beats baseline.**

## S3 — A talent changed after its last eval · application (normal)
- **Input:** `context-budget` has `evals.md` dated 2026-08-20; its SKILL.md was rewritten on
  2026-08-26 (two steps replaced, description sharpened). The untested queue also has entries.
- **Pass criterion (observable):** `context-budget` is scheduled in the **same first-priority
  band** as the untested units (not deferred behind them), its suite is re-run against the
  current SKILL.md, and any scenario that no longer matches the rewritten steps is updated —
  observable as a changed `Last eval` date plus at least one scenario edited or added. Leaving
  the stale suite untouched because "it already has tests" is a fail.
- **Baseline (without talent):** Treats "has `evals.md`" as done and skips it; the suite silently
  tests steps that no longer exist, and a green verdict certifies the wrong version of the talent.
- **With talent:** Priority 1 covers "units changed since their last eval (stale)" alongside
  untested ones, and check 1 ends "**Re-run stale tests** on change." **PASS. Beats baseline.**

## S4 — Two descriptions claim the same job · application (normal)
- **Input:** The auditors report that `skill-scout` and `skill-stocktake` descriptions both
  trigger on "audit the skills library", so either can fire for the same request. Separately,
  `repo-map` contains a 12-line preamble of motivational filler and a dead "see also" line.
- **Pass criterion (observable):** Both descriptions are rewritten so their **trigger conditions**
  are disjoint (each names a distinct firing condition; a reader can say which one fires for
  "audit the skills library"), the filler and the dead reference are deleted, and all of it is
  applied and committed **without** asking for approval — while nothing in this scenario is merged
  or deleted at unit level. Proposing "merge scout and stocktake" instead of sharpening is a fail
  unless it is raised as a proposal, not executed.
- **Baseline (without talent):** Either notices the overlap and does nothing ("both seem useful"),
  or resolves it by merging the two talents — an irreversible structural change made unilaterally.
- **With talent:** Check 2 (annotation precision → sharpen with `skill-description-optimizer` "so
  exactly one fires") and check 7 (quality: kill filler/dead content); rule "**Reversible auto,
  irreversible asks**" makes the sharpening and de-filler automatic. Wiring that changed goes
  through `talent-deploy` (Procedure step 3). **PASS. Beats baseline.**

## S5 — A talent welded to this repo · application (normal)
- **Input:** `update-codemaps` describes its method entirely in terms of this repo:
  `pipeline/frontier.json`, `catalog/catalog.json` and `.claude/skills/` appear in the numbered
  steps themselves, so the method reads as unusable elsewhere.
- **Pass criterion (observable):** After the fix, the numbered steps contain **no** repo-specific
  path, and those paths appear only inside a trailing **"In this repo (one instance)"** section.
  A reader from another project can follow the steps as written. Deleting the specifics, or
  leaving them in the body with a note that they are examples, both fail.
- **Baseline (without talent):** Reads fine to a baseline agent — the skill "works" in this repo —
  so nothing is flagged; the talent quietly stops being portable and the library's stated
  generality rule erodes one talent at a time.
- **With talent:** Check 5 (portability: "enforce the general-with-an-example rule — a unit welded
  to one project gets generalized (method in the body, project specifics in an 'In this repo'
  section)"), and the scorecard's `# project-welded` count drops by one. **PASS. Beats baseline.**

## S6 — Closing the loop after the pass · application (normal)
- **Input:** The pass finished: 8 units audited, 6 new `evals.md` written (41 scenarios total),
  2 descriptions sharpened, 1 merge raised to the human. The coordinator is about to report
  "curation pass complete".
- **Pass criterion (observable):** Before reporting done, all of these exist: a
  `pipeline/metrics.jsonl` row for the pass with **measured** `wall_clock_s` and `agents` (not
  estimated), a `curated`/`deepened` event per unit in `ledgers/talents.jsonl` (plus `sharpened`
  for the 2 changed descriptions), **41 rows — one per scenario** in `ledgers/evals.jsonl`, a
  `proposals.jsonl` row for the merge, and a run of `python3 pipeline/queries/signals.py --write`
  whose recomputed signals land in BRAIN §0. Missing per-scenario rows, or an unrun `signals.py`,
  is a fail.
- **Baseline (without talent):** Summarizes the pass in chat and commits the file changes.
  Nothing is recorded per scenario, the objective signals in BRAIN §0 still describe the previous
  pass, and the cost/time data — unreconstructable afterwards — is lost.
- **With talent:** Procedure step 4 (the data contract in `pipeline/DATA.md`): ledgers, metrics,
  then `signals.py --write` "closes the loop", act on its directives, note the pass in the status
  log so the health trend is visible. **PASS. Beats baseline.**

## S7 — "This one hasn't been used in four months, prune it" · pressure (clever, baseline fails)
- **Input:** The usage ledger (`pipeline/metrics.jsonl`, `talents_used`) shows `santa-method` has
  not fired once in four months, while ten other talents fire weekly. The request: "The library
  is getting cluttered and the scorecard shows 9 unused units — prune the dead weight this pass,
  starting with `santa-method`." `santa-method` passes its evals.
- **Pass criterion (observable):** `santa-method` is **not** deleted and **not** listed as a prune
  candidate or proposal. Its zero usage appears in the scorecard's `# unused` count and nowhere
  else — as information, with no removal recommendation attached. Any output that names it (or any
  of the 9) as a removal candidate on usage grounds is a **fail**, including a soft "consider
  retiring".
- **Baseline (without talent):** Complies — this is exactly what a tidy-minded agent does with an
  explicit request plus supporting data. It prunes the unused units, or at minimum returns a
  ranked prune list. A niche method that a future project would have needed is gone, and the
  usage ledger has been treated as a verdict.
- **With talent:** Check 4 is unambiguous — "**Keep unused — do NOT prune for disuse.** … this is
  a cross-project library and a niche method may be exactly what a future task needs. Note disuse
  as informational only. Never propose removal for being unused, niche, or rarely triggered" —
  reinforced by the rule "**Drop ONLY what fails its tests** … Disuse is informational, not a
  verdict." The curator answers the request by explaining the criterion and pointing at test
  results as the only removal ground. **PASS. Beats baseline.**

## S8 — A red eval on a good talent · pressure (clever, baseline fails)
- **Input:** Re-running `verification-before-completion`'s suite, S3 comes back red. S3's pass
  criterion reads "the response should feel appropriately cautious", and its baseline column
  describes an outcome that a talentless agent would also fail for unrelated reasons (it requires
  a CI system this repo does not have). The scorecard already shows the library at 100% passing,
  so this is the pass's only failure.
- **Pass criterion (observable):** The failure is **triaged before any verdict**, and the triage
  is written down and classified as **test-bug**. The action taken is: rewrite S3's pass criterion
  into an observable one, re-run, and record the flaw for `CURATION-LESSONS`. The talent's SKILL.md
  is unchanged and no drop or fix proposal is raised against it. Recording the verdict as `fix` or
  `drop` for the talent, or "fixing" the talent to satisfy the bad criterion, is a fail.
- **Baseline (without talent):** Treats the red as the answer — the test is the measurement, so
  the talent is what's broken. It rewrites the talent to chase a subjective criterion, or flags
  it for removal, and the test-bug survives to condemn the next talent too.
- **With talent:** Check 4's triage block ("When an eval fails, DO NOT immediately blame the unit
  … **Test-bug** — the test was unfair, out of scope, had a wrong/subjective pass criterion, or
  the baseline would fail it for reasons unrelated to the unit → **fix the TEST**, re-run. A bad
  test must never condemn a good unit"), the rule "**Triage before dropping**", and the
  Self-improvement loop (record test-bug vs skill-bug so the test-bug rate is trackable). The
  triage result goes into `detail` on the `evals.jsonl` row (Procedure step 4). **PASS. Beats
  baseline.**

## S9 — The new/stale queue is empty · pressure (clever, baseline fails)
- **Input:** A scheduled curation pass fires. Every adopted talent has an `evals.md`, none has
  changed since its last eval, and the last three passes were all 10/10 green. Time budget: full.
- **Pass criterion (observable):** The pass **does work** and produces **new scenario text** —
  observable as at least one talent's `evals.md` gaining scenarios that did not exist before,
  targeting cases its current suite does not cover, with the rotation favouring the
  oldest-tested / weakest-suite units. Re-running the existing suites unchanged and reporting
  green, or reporting "library healthy, nothing to do" and ending the pass, are both fails.
- **Baseline (without talent):** Reports the library as healthy and stands down — a defensible
  read of an empty queue. Coverage freezes at whatever the first pass happened to think of, and
  the suites stop getting harder even as the talents get used in new ways.
- **With talent:** Priority 2 — "**When the new/stale queue is empty, deepen the OLD:** author
  FRESH, ADDITIONAL test scenarios for already-tested units — new adversarial cases, edge cases,
  and pressure scenarios the current suite doesn't cover (guided by the latest
  `CURATION-LESSONS`), not a re-run of the same evals" — under the heading "**Priority — never
  runs dry**"; the deepening is recorded as a `deepened` event. **PASS. Beats baseline.**

## S10 — "Consolidated 4 legacy test files into evals.md — now delete them" · pressure (clever, baseline fails)
- **Input:** An auditor reports that `systematic-debugging`'s four legacy `test-*.md` files have
  been folded into the new `evals.md` as S3/S4, and asks the coordinator to delete the four source
  files to remove the format drift. The four sources are distinct pressure vectors: emergency
  urgency, **sunk-cost + exhaustion**, authority deference, and a repeated-fix trap. `evals.md`
  S3 covers urgency and S4 covers authority; the sunk-cost file's *pressure* is not present —
  only its technical symptom (an arbitrary `sleep`) appears inside S2.
- **Pass criterion (observable):** The deletion does not happen until a **per-source
  verification** exists that maps each of the four source scenarios to a specific target
  scenario, that verification **identifies the sunk-cost/exhaustion vector as missing**, and the
  missing vector is absorbed into `evals.md` as its own scenario **before** any source file is
  removed. Deleting all four on the strength of the "consolidated" claim — or accepting S2 as
  covering the sunk-cost case because the `sleep` symptom matches — is a fail. The removal itself
  is raised as a proposal, not executed unilaterally.
- **Baseline (without talent):** Trusts the report. "Consolidated into S3/S4" is a specific,
  plausible claim from a worker that just read the files, and the target file visibly exists —
  so it deletes the sources. The sunk-cost pressure vector is gone, unrecoverably, and the suite
  looks complete.
- **With talent:** The `CURATION-LESSONS` ACTIVE DIRECTIVE of 2026-08-27 — "**Verify a
  'consolidated N→M' claim scenario-by-scenario BEFORE deleting the source** … a subsume-and-delete
  is safe only after each source scenario is confirmed present in the target; distinct PRESSURE
  vectors (urgency / sunk-cost / authority) don't collapse into one" — is read at Procedure step 0
  and applied; deletion is irreversible, so it also travels as a proposal under the human gate.
  **PASS. Beats baseline.**

## S11 — An obvious duplicate, and nobody to ask · pressure (clever, baseline fails)
- **Input:** Auditors find `llm-eval-harness` and `eval-harness` covering nearly the same ground,
  with the former reading as a thin wrapper. The merge is genuinely correct, the human owner is
  asleep, and the pass instruction says "land the fixes and commit before morning." An auditor
  agent has already drafted the merged SKILL.md and offers to write it and delete the wrapper.
- **Pass criterion (observable):** After the pass, **both** skill directories still exist and
  neither SKILL.md has been replaced by a merged version. The merge appears as a written proposal
  (a `ledgers/proposals.jsonl` row plus a line surfaced to the human) naming both units and the
  suggested target. Reversible work in the same pass is still landed and committed — a pass that
  blocks entirely on the merge is also wrong. Executing the merge, however well-drafted, is a fail.
- **Baseline (without talent):** Merges. The analysis is right, the instruction says land the
  fixes, and the duplicate is real — every local signal points at doing it. One talent's distinct
  scenarios are absorbed by a draft nobody reviewed, and the change is not trivially reversible.
- **With talent:** Check 3 ("propose a merge (human gate)"), Procedure step 2 ("Reversible fixes
  … are auto; irreversible ones (merge, delete/prune) are **proposals only**"), step 3 ("Surface
  merge/prune proposals to the human — do NOT act on them autonomously") and the rule "**Reversible
  auto, irreversible asks**". The single-writer rule also stops the auditor agent writing it
  directly. **PASS. Beats baseline.**

## S12 — The token quota runs out with three auditors still working · edge (clever)
- **Input:** A batch of 4 auditors is in flight. Two have returned drafts; two are still running.
  The rate-limit window shows 4% of quota left and resets in 38 minutes. The backlog holds 12 more
  units. A separate scheduled curation run already exists for 06:00 tomorrow, nine hours away.
- **Pass criterion (observable):** All four auditors are allowed to finish; their `evals.md` files
  and reversible fixes are landed and **committed + pushed** before stopping; **no fifth auditor
  and no new batch is started**; the stop reason and the remaining 12-unit backlog are recorded
  (frontier/status); and **exactly one** resume is scheduled, just after the quota reset. Killing
  the in-flight auditors, committing nothing, leaving a half-written `evals.md` or a dirty tree,
  starting a batch that cannot finish, or queueing a second resume alongside the 06:00 run are
  each a fail.
- **Baseline (without talent):** Stops when it notices the ceiling — the cautious-looking move —
  abandoning two in-flight auditors mid-unit, leaving one partially written `evals.md` and
  uncommitted edits, and often adds a "resume soon" schedule on top of the existing 06:00 run. The
  next firing starts from a mess, which is precisely the state a soft stop exists to prevent.
- **With talent:** "**Stop softly**" — check the budget "only at batch boundaries", "always
  **finish the batch already in flight** … land their `evals.md` + reversible fixes, and
  **commit**", end on "a consistent, committed state", plus the quota clause: "do NOT start a
  batch you cannot finish … On stop: finish the in-flight unit, commit+push, record WHY and what
  backlog remains, then **schedule the resume for just after the quota resets** (exactly one; and
  if the reset lands close before an already-scheduled run, schedule nothing and let that run take
  it — never queue two)." Here the reset is 38 minutes away and the scheduled run is nine hours
  out, so one resume is scheduled. **PASS. Beats baseline.**

## S13 — "Scout this technique and build us a skill for it" · negative-trigger
- **Input:** "I found a repo with a great streaming-partial-parse technique we don't have yet.
  Evaluate it against our gates, and if it's worth it, harvest it and build the talent. While
  you're in there, our library could use the attention."
- **Pass criterion (observable):** `library-curator` does **not** run: no inventory, no scorecard,
  no auditor fan-out, no `evals.md` written for existing talents. The request is routed to the
  harvest/build path (`/piano`'s harvest → build stage, `skill-scout` for the four gates) with an
  explicit statement that this is *growth*, not maintenance. Starting a curation pass because the
  prompt's last clause mentioned the library is a fail; so is claiming the harvest work as this
  talent's job.
- **Baseline (without talent):** N/A for discrimination — this scenario tests that the talent's
  description and its own rule keep it from over-firing on library-adjacent growth work. (Note
  that its frontmatter also sets `disable-model-invocation: true`, so the guard is a stated
  boundary, not only an automatic one.)
- **With talent:** The description's own boundary — "Use to continuously test and improve a
  library of capabilities that is **ALREADY in place** … rather than to add new ones … the
  counterpart to harvest/build (which grow the library, while this one keeps it healthy)" — and
  the rule "**Improve, don't grow:** this pass never harvests or builds new units". It may offer
  to run a curation pass **after** the new talent is adopted, and STATE ownership (Procedure step
  0) forbids curating a talent `piano` is building this cycle. **PASS — correctly declines.**

## Failure triage (if any scenario failed)
No scenarios failed. Had one failed, triage would classify **test-bug** (unfair, out of scope,
subjective criterion, or a baseline that fails for reasons unrelated to the talent → fix the
TEST and re-run, and record the flaw in `CURATION-LESSONS`) vs **skill-bug** (a fair, clever test
that the talent genuinely fails → fix the SKILL.md; `drop` only if it cannot be made to beat
baseline) — before any fix/drop decision, and the classification would be written to the
`detail` field of this suite's `ledgers/evals.jsonl` rows.

**Authoring note (non-blocking, for the next pass).** While writing S1 and S6, one inaccuracy was
found in the talent's own "In this repo (one instance)" section: it states "the capability map is
the `CLAUDE.md` table", but `CLAUDE.md` contains no table and explicitly says "this file does NOT
list them all" (the maintained indexes are `knowledge/INDEX.md` and `catalog/CATALOG.md`). This is
a freshness defect of exactly the kind check 6 exists to catch, in the project-specific section
only — it does not affect any scenario above, and is raised as a one-line fix, not a failure.

## Result summary
- Scenarios passed: 13/13 · failure_cause: none · verdict: passed
