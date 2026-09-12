---
name: library-curator
description: "Use to continuously test and improve a library of capabilities that is ALREADY in place (the tested/adopted tier — 'database 2') rather than to add new ones: audit every unit for test coverage, sharpen mis-triggering/overlapping descriptions, dedup/merge near-duplicates, enforce quality and portability, keep the index/capability-map accurate, and emit a health scorecard. Removal is test-validated ONLY -- never prunes a unit for being unused or niche. A recurring maintenance pass, run via parallel fan-out; the counterpart to harvest/build (which grow the library, while this one keeps it healthy). NOT for taking a one-off inventory of what the library contains (skill-stocktake)."
disable-model-invocation: true
---

# library-curator — constantly test + improve what's already in place

Adding capabilities grows a library; nothing keeps it healthy. This is the recurring
maintenance pass over the **already-adopted tier** ("database 2"): it finds what has rotted,
drifted, or was never verified, and fixes it — one auditor agent per unit, fanned out, with
the coordinator committing. It never harvests or builds new units; it improves the existing ones.

> **Invocation:** this talent carries `disable-model-invocation: true` on purpose — it is an
> orchestrator, not something a task should auto-trigger into. A caller does not "load" it;
> a caller RUNS the workflow script that makes this method executable, or follows the method
> by hand. Wording elsewhere that says "hand it to X" means running X's script.

## When to use
- Periodically between harvest/build waves (e.g. every few waves, or on a schedule), or when
  the health scorecard degrades (untested units pile up, descriptions start overlapping).

## What it checks and fixes (per unit)
1. **Test coverage — write a GOOD, BLENDED suite (specific to the unit).** Every unit must
   have persisted tests (`evals.md`) that are a MIX, all tailored to it: ~half normal/
   representative (does it do its everyday job well?) and ~half clever/adversarial (traps,
   planted defects, edge/boundary, pressure), plus a negative-trigger — then baseline-vs-with.
   Not only traps (that misses the bread-and-butter job) and not only happy-path (that misses
   where it breaks). Design the clever ones so the WITHOUT-unit baseline fails (they
   discriminate); the normal ones confirm everyday behavior. **Re-run stale tests** on change.
2. **Annotation precision.** Detect descriptions that overlap or mis-trigger (two units
   claiming one job) → sharpen with `skill-description-optimizer` so exactly one fires.
3. **Dedup / merge.** Find near-duplicate units and wrappers → propose a merge (human gate).
4. **Keep unused — do NOT prune for disuse.** A unit not used lately is NOT a prune target:
   this is a cross-project library and a niche method may be exactly what a future task needs.
   Note disuse as informational only. Never propose removal for being unused, niche, or rarely triggered.
   **Root-cause a failure before dropping (test vs skill).** When an eval fails, DO NOT
   immediately blame the unit. Triage the failure first:
   - **Test-bug** — the test was unfair, out of scope, had a wrong/subjective pass criterion,
     or the baseline would fail it for reasons unrelated to the unit → **fix the TEST**,
     re-run. A bad test must never condemn a good unit.
   - **Skill-bug** — the unit genuinely fails a fair, clever test → **fix the unit**; `drop`
     ONLY if it cannot be made to beat baseline. Dropping is the last resort after a real,
     test-validated skill failure — never a first response to a red result.
5. **Portability.** Enforce the general-with-an-example rule — a unit welded to one project
   gets generalized (method in the body, project specifics in an "In this repo" section).
6. **Freshness.** A unit referencing an external tool/version/API that has changed → re-verify
   its commands/claims against the current reality; fix or note staleness.
7. **Quality.** Re-read against the authoring conventions — kill filler/dead content, weak
   steps, missing rules; confirm valid frontmatter.
8. **Index / structure.** Keep the capability map + any `INDEX.md` accurate; cross-link the
   knowledge base to the units it explains. Re-categorize if the structure no longer fits.

## Priority — never runs dry
1. **NEW first:** units with no `evals.md` (just added/adopted) and units changed since their
   last eval (stale) — test + improve these before anything else.
2. **When the new/stale queue is empty, deepen the OLD:** author FRESH, ADDITIONAL test
   scenarios for already-tested units — new adversarial cases, edge cases, and pressure
   scenarios the current suite doesn't cover (guided by the latest `TEST-AUTHORING-LESSONS`), not a
   re-run of the same evals. Coverage and rigor keep rising over passes; the library is never
   "done" being hardened. Rotate so the oldest-tested / weakest-suite units come up again.

## Procedure (fan out, coordinator commits)
0. **Read the brain.** Open `pipeline/BRAIN.md` (shared control tower) + `TEST-AUTHORING-LESSONS.md`
   (the directives to apply) + `CURATION-LESSONS.md` (this loop's own operating journal)
   + `templates/EVALS.template.md` + `pipeline/DATA.md` (the data contract — what to record) first. Respect STATE ownership (curator owns existing
   talents' evals/fixes; never curate a talent piano is building this cycle). At the end,
   UPDATE BRAIN.md (STATE, any new cross-agent LINK, refresh the curator PLAN line).
1. **Inventory + score.** List every adopted unit; apply the priority above; compute the
   **health scorecard**:
   % with tests, % passing latest eval, # overlapping descriptions, # unused, # project-welded,
   # stale. This is the before-picture and the priority signal.
2. **Fan out (run `pipeline/workflows/curate-wave.workflow.js`, the `factory` method made
   executable):** one auditor agent per unit (or per worst-N first),
   each running the checks above and RETURNING proposed fixes + any test it wrote. Reversible
   fixes (write a missing eval, sharpen a description, delete filler) are auto; irreversible
   ones (merge, delete/prune) are **proposals only**.
3. **Coordinator applies + commits (single writer):** land the reversible fixes and the new
   `evals.md`, run `talent-deploy` for anything whose wiring changed, update the scorecard,
   and commit. Surface merge/prune proposals to the human — do NOT act on them autonomously.
4. **Record (the data contract — see `pipeline/DATA.md`).** Append the scorecard + this pass's
   `metrics.jsonl` row with **measured** `wall_clock_s` and `agents`. Then write the ledgers:
   a `curated`/`deepened` event (and `sharpened` when a description changed) per unit to
   `ledgers/talents.jsonl`; one row PER SCENARIO to `ledgers/evals.jsonl` (with the triage
   result — test-bug vs skill-bug — in `detail`); a `proposals.jsonl` row for any merge/prune
   raised to the human gate; a `claims.jsonl` row for EVERY claim an auditor made, written at the
   moment you verify it and before you act on it, with `verified_how` naming what you actually
   checked — you already verify auditor claims before fixing (the rule is above); this records
   the outcome instead of discarding it, and it is the only measure of whether the auditors are
   accurate; and `family` + `silent` on every `defects.jsonl` row. Capture history/cost/time LIVE (unreconstructable later). **Then
   run `python3 pipeline/queries/signals.py --write`** to recompute the objective signals from
   the ledgers into BRAIN §0 (closes the loop), and act on its directives. Note the pass in the
   status log so the trend (is the library getting healthier?) is visible.

## Self-improvement — the curator gets better at testing over time
The curator applies `wave-reflect`'s measure→reflect→learn→read-back loop TO ITSELF, so its
tests and audits sharpen each pass:
- **Measure:** each pass records, to a curation ledger, per-unit signals — was a failure a
  test-bug or a skill-bug (the triage above)? how many tests turned out flawed on triage? which
  description-overlap patterns recurred? how many false-drops were avoided by triage?
- **Reflect:** derive `TEST-AUTHORING-LESSONS` directives from those signals (and this pass's operating lessons into `CURATION-LESSONS`) — e.g. "discipline-talent tests
  kept mis-scoring on X → author them as pressure scenarios, not application ones", "tests that
  asserted a subjective criterion were the flawed ones → always state an observable pass line",
  "domain-Y descriptions kept overlapping on keyword Z → differentiate on trigger, not topic".
- **Read back:** the NEXT pass reads `TEST-AUTHORING-LESSONS` before authoring tests or sharpening,
  so it stops repeating the mistakes — better, fairer, cleverer tests each cycle.
- **Promote into the generic test template:** when a CURATION-LESSON proves durable (recurs
  across passes), fold it into the EVOLVING CHECKLIST of `templates/EVALS.template.md` — a
  reversible edit. That way the accumulated testing wisdom lives in the one generic template
  every future test is authored from, and improves it over time without touching each talent.
A high test-bug rate is itself a signal: the test-authoring needs work, not the library. Track
it; when it drops, the curator has learned to write fairer tests.

## Stop softly (graceful shutdown)
A bounded pass (time budget or a stop signal) must stop **between batches, never mid-unit**:
- Check the budget **only at batch boundaries.** If it's spent, do NOT start a new batch —
  but always **finish the batch already in flight**: let its auditor agents complete, land
  their `evals.md` + reversible fixes, and **commit**. Never abandon in-flight results or
  leave a half-written eval or a dirty working tree.
- End on a **consistent, committed state**: everything done is committed and pushed, the
  scorecard reflects exactly what was processed, and the frontier shows the remaining backlog
  — so the next firing resumes cleanly from a clean line, not a mess.
- A soft stop is a clean handoff, not an interrupt. If asked to stop early, the same applies:
  wrap up the current unit/batch, commit, then stop.
- **Quota-aware stopping (a resetting rate limit is a budget too).** When the run is bounded by
  a quota that refills on a clock (an API rate-limit window, a token/spend cap), check it at the
  SAME batch boundaries as the time budget — never mid-unit. Approaching the ceiling is already
  a stop signal: do NOT start a batch you cannot finish, because being cut off mid-unit is what
  produces the half-written state a soft stop exists to prevent. On stop: finish the in-flight
  unit, commit+push, record WHY and what backlog remains, then **schedule the resume for just
  after the quota resets** (exactly one; and if the reset lands close before an already-scheduled
  run, schedule nothing and let that run take it — never queue two). A quota stop is a pause with
  a known wake-up time, not a failure.
  **Check WHICH window is warning** — several quotas are usually enforced at once and the
  binding one changes as windows reset. A SHORT window (minutes/hours) → pause and resume, as
  above. A LONG window (days/weekly) → do NOT pause: waiting days is an outage, not a pause.
  THROTTLE instead — smaller batches, less fan-out, longer gaps — and surface it to the human,
  whose budget it is.

## Rules
- **Improve, don't grow:** this pass never harvests or builds new units — only tests + improves existing ones.
- **Stop softly:** budget/stop is checked between batches; the in-flight batch always finishes and commits before stopping — never a half-done unit or an uncommitted tree.
- **Triage before dropping:** a failed eval is root-caused (test-bug vs skill-bug); fix the test
  when the test was wrong, fix the skill when the skill was wrong, drop only a genuinely broken,
  unfixable skill. Never drop on a red result alone.
- **Drop ONLY what fails its tests.** A failing test (doesn't beat baseline, can't be fixed) is
  the sole removal criterion. Never prune a unit for being unused, niche, or rarely triggered —
  a cross-project library keeps methods a future task may need. Disuse is informational, not a verdict.
- **Tests must be clever, not rote.** Continuously author good, adversarial tests (traps, planted
  defects, edge cases) — a test everything passes measures nothing.
- **Reversible auto, irreversible asks:** writing tests / sharpening / de-fillering is auto;
  merge, delete, and re-structure are proposals behind the human gate.
- **Single writer:** auditor agents return proposals/drafts; the coordinator commits.
- **Measure the library, not just the units:** every pass emits a health scorecard so decay is caught early.

## In this repo (one instance)
"Database 2" = the adopted talents in `.claude/skills/`. Tests live at
`.claude/skills/<name>/evals.md`; the usage ledger is `pipeline/metrics.jsonl` (`talents_used`);
overlap/sharpen uses `skill-scout`/`skill-stocktake` + `skill-description-optimizer`; the
capability map is the `CLAUDE.md` "Capability map" list; the scorecard is appended to `pipeline/metrics.jsonl`
and summarized in `pipeline/STATUS.md`. `/piano` runs a curation pass as a periodic maintenance
stage between harvest/build waves, using `factory` for the fan-out.
