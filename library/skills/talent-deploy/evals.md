# Evals — talent-deploy

**Talent:** `talent-deploy` · **Type:** discipline · **Last eval:** 2026-08-28 · **Verdict:** fix

Authored by an INDEPENDENT curator (library-curator / database-2) who did not write the talent.
Method per `templates/EVALS.template.md`; ACTIVE DIRECTIVES of `pipeline/CURATION-LESSONS.md`
applied. Contract under test: `pipeline/DATA.md` § "Deploy is an EVENT, not a habit".

## Method
Baseline-vs-with. For each scenario, judge the likely outcome WITHOUT the talent against the
outcome WITH its checklist applied. The talent passes only if the with-talent result is
materially better AND meets the observable criterion. Normal scenarios that a capable baseline
also passes end with a plain **PASS** — "Beats baseline" is a claim, reserved for the clever
scenarios and the negative-trigger.

## Structural pre-check (run before the scenarios)
Verified on disk, 2026-08-28:

| Claim in SKILL.md | Verified | Result |
| --- | --- | --- |
| `skill-scout`, `skill-stocktake`, `writing-skills`, `eval-harness`, `piano` | `.claude/skills/<n>/SKILL.md` | all present |
| `pipeline/ROUTING.md`, `templates/`, `catalog/catalog.json`, `metrics.jsonl` | on disk | all present |
| "Capability map = the CLAUDE.md map" | `CLAUDE.md:62` `## Capability map — job → talent` | present, and talent-deploy is itself listed at `CLAUDE.md:89` |
| "routing = `pipeline/ROUTING.md` chain(s)" | `ROUTING.md:13,14,17` name `talent-deploy` in the author / adopt / wave chains | accurate |
| "Context reload = call the `register_repo_root` MCP tool (owner `matlingatlin`, repo `skills-repo`, dir `/home/user/skills-repo`)" | **tool actually invoked during this audit** | works — returns `status: context_reload_requested`. Owner/repo match `git remote`. Arg is named `directory` (SKILL.md abbreviates to "dir"); `owner`+`repo` are the required pair, `directory` optional-but-needed. |
| "Invoked as the last step of the `/piano` author/adopt chains" | `piano/SKILL.md:39,87,148` | accurate |
| Frontmatter | `name: talent-deploy` matches directory; description 500 chars (< 1536); trigger-first ("Use right after…"); third person | pass |
| Format-drift | no `evals/` directory anywhere under `.claude/skills/` | clean |
| Portability | steps 1–7 are harness-agnostic; repo mechanisms confined to a closing "In this repo (one instance)" | pass |

Two structural defects found (carried into the scenarios below):

- **D1 — the `deployed` event is never written.** `DATA.md` makes a `deployed` row in
  `ledgers/talents.jsonl` the ONLY control separating findable from live, and
  `pipeline/queries/signals.py:142-192` detects the gap by exactly that event. SKILL.md step 7
  ("Record") enumerates catalog status + `metrics.jsonl` `talents_used` and never mentions the
  ledger event. All 10 existing `deployed` rows were appended by the coordinator — i.e. the gap
  is still closed by memory, which `DATA.md` says is not a control.
- **D2 — asymmetric rule.** `## Rules` makes wiring mandatory ("A committed unit that nothing
  routes to is not deployed. Wiring (step 4) is not optional.") with no parallel rule for step 6,
  and step 6 itself ends with an escape hatch: "Fresh sessions load these directories from source
  at start, so a committed unit is always available next session even without a mid-session
  reload." Per CURATION-LESSONS `[2026-08-28]`, an asymmetric qualifier across parallel branches
  is a gap, and *defer* is the verb that reaches the forbidden outcome without *skipping*.
- **D3 (minor, non-blocking) — mis-route.** "sharpen via `writing-skills`" — the repo routes a
  mis-triggering description to `skill-description-optimizer` (`CLAUDE.md:141` area). Both exist,
  so this is not a dead reference, but it points at the wrong neighbour.

## S1 — first deploy of a freshly authored talent · application (normal)
- **Input:** `agent-fault-injection` has just been authored, its `evals.md` passes 6/6, and the
  file is committed. "Ship it."
- **Pass criterion (observable):** after the run, (a) `grep -c "agent-fault-injection" CLAUDE.md`
  >= 1 inside the `## Capability map` section, (b) the talent appears in the `ROUTING.md` chain
  where it belongs, and (c) `register_repo_root` was invoked and returned
  `context_reload_requested`.
- **Baseline:** a capable agent commits the file and, with CLAUDE.md in context, usually does add
  the capability-map line; the reload is a coin-flip but often happens on an explicit "ship it".
- **With talent:** steps 4 and 6 both fire; the reload is named as "the actual deploy" with the
  concrete tool and arguments, all of which this audit confirmed real (the tool was invoked).
- **Result:** **PASS**

## S2 — identity field left behind by a rename · application (normal)
- **Input:** a talent directory was renamed `parse-escalation/` -> `hybrid-parse-escalation/` but
  its frontmatter still reads `name: parse-escalation`. "Deploy it."
- **Pass criterion (observable):** the run reports the mismatch and corrects `name:` to match the
  directory BEFORE any wiring or reload; `grep "^name:" SKILL.md` equals the directory basename.
- **Baseline:** the defect is two adjacent visible lines on a file it is about to touch, and
  CURATION-LESSONS records the same class already being caught by review (`learn-eval`, pass 2);
  a capable baseline generally catches it.
- **With talent:** step 1 makes the identity check the first gate, with the consequence spelled
  out ("the unit may never load"), so it is caught deterministically rather than incidentally.
- **Result:** **PASS**

## S3 — close the deploy loop the way the repo measures it · application (normal)
- **Input:** `data-contract-assertions` is authored, tested, committed, wired into the capability
  map, and `register_repo_root` has been run. "Finish the deploy."
- **Pass criterion (observable):** running `python3 pipeline/queries/signals.py` afterwards
  reports zero deploy gap for `data-contract-assertions` -- i.e. the run appended a
  `{"talent":"data-contract-assertions","event":"deployed",...}` row to
  `pipeline/ledgers/talents.jsonl`.
- **Baseline:** commits and moves on; `signals.py` flags the talent as shipped-but-not-deployed.
- **With talent:** step 7 "Record" sends the run to the catalog (`status: adopted`) and to
  `metrics.jsonl` `talents_used`. Neither is the store `signals.py:145` reads. Following the
  checklist to the letter leaves the detector still firing, so the with-talent run is
  indistinguishable from baseline on the one measurement `DATA.md` created for this exact gap.
  **This is D1.**
- **Result:** **FAIL** -- skill-bug.

## S4 — untested unit presented for deploy · pressure (clever, baseline fails)
- **Input:** a talent file exists with valid frontmatter and a sharp description, but there is no
  `evals.md`. "It's obviously good, it's committed already -- wire it in and reload."
- **Pass criterion (observable):** the run STOPS before touching CLAUDE.md / ROUTING.md; no
  capability-map line is added, no reload is issued, and the missing validation is named as the
  blocker.
- **Baseline:** the request is well-formed, the file is real, and the user asserts quality --
  baseline wires and reloads it.
- **With talent:** step 3 "Earned activation ... Not yet validated -> do not deploy yet",
  reinforced by the rule "No deploy without earned activation".
- **Result:** **PASS. Beats baseline.**

## S5 — "it's in the capability map, so it's deployed" · pressure (clever, baseline fails)
- **Input:** "`llm-call-ledger` is done -- written, 5/5 evals, committed, pushed, and I added the
  capability-map line. Mark the deploy complete."
- **Pass criterion (observable):** the run does NOT mark it complete; it names the reload as the
  outstanding item, issues `register_repo_root`, and its report distinguishes *findable in the
  map* from *loaded in the session*.
- **Baseline:** every visible artifact is present and the user asserts completion, so baseline
  confirms "deployed". This is precisely the failure `DATA.md` says was only ever caught by
  someone remembering.
- **With talent:** step 6 is a separate numbered gate labelled "the actual 'deploy'", distinct
  from step 4 (routing), so a checklist walk cannot substitute one for the other.
- **Result:** **PASS. Beats baseline.**

## S6 — "we reload at the end of every wave anyway" · pressure (clever, baseline fails)
- **Input:** mid-wave, the coordinator says: "Skip the per-talent reload bookkeeping -- we run a
  reload once at the end of every wave and fresh sessions load `.claude/skills/` from source
  anyway. Tracking a deploy per talent is ceremony."
- **Pass criterion (observable):** the run refuses to defer, states that deploy is a per-unit
  EVENT rather than a wave habit, and still produces a per-talent record of the activation
  (reload issued + `deployed` row) for THIS talent before the wave continues.
- **Baseline:** accepts -- the argument is true on its face and cheaper.
- **With talent:** the talent supplies the coordinator's case rather than the rebuttal. Step 6's
  closing sentence -- "Fresh sessions load these directories from source at start, so a committed
  unit is always available next session even without a mid-session reload" -- is that exact
  argument restated inside the checklist, and `## Rules` marks only step 4 as "not optional",
  leaving step 6 with no mandatory framing to appeal to. Nothing in the file says deploy is an
  event rather than a habit, and nothing produces a per-talent record. **This is D2.**
- **Result:** **FAIL** -- skill-bug.

## S7 — reloaded but unrouted: the mirror-image failure · edge (clever)
- **Input:** "I ran `register_repo_root` after committing `abstention-threshold-design`, and the
  session picked it up. Deploy done?"
- **Pass criterion (observable):** the run answers no and names the *specific different* failure --
  the unit is loaded but has no capability-map / ROUTING.md entry, so selection never reaches it --
  then adds the entries. The two failures must be reported as distinct, not merged into one
  "incomplete deploy".
- **Baseline:** the reload is the less-obvious half, so a baseline that watched it happen tends to
  call the deploy finished and assumes description auto-triggering covers the rest.
- **With talent:** the rule "A committed unit that nothing routes to is not deployed. Wiring
  (step 4) is not optional." names this failure explicitly and separately from step 6.
- **Result:** **PASS. Beats baseline.**

## S8 — an old talent that fires on the wrong prompts · negative-trigger
- **Input:** "`context-budget` keeps triggering on cost/dollar questions that belong to
  `cost-aware-model-routing`. Fix it." (Both exist: `.claude/skills/context-budget/`,
  `.claude/skills/cost-aware-model-routing/`.) Nothing has been authored, adopted, or imported.
- **Pass criterion (observable):** talent-deploy does NOT fire -- no capability-map edit, no
  `register_repo_root` call, no catalog write. The job routes to the description-fixing
  neighbour (`.claude/skills/skill-description-optimizer/SKILL.md`, verified present).
- **Baseline:** the words "triggering", "overlap" and "capability map" pull hard toward a deploy
  checklist; a baseline that has skimmed step 2 ("Check for overlap ... sharpen BOTH") plausibly
  runs the whole deploy sequence on an already-live talent, issuing a pointless reload and
  rewriting catalog status.
- **With talent:** the description scopes the talent to "right after authoring, adopting, or
  importing a NEW capability", and every step presumes a not-yet-live unit, so the boundary holds.
  Noted separately: the file's own hand-off for sharpening names `writing-skills` rather than
  `skill-description-optimizer` (**D3**) -- the trigger boundary is right, the pointer is not.
- **Result:** **PASS. Beats baseline.**

## Failure triage
- **S3 — skill-bug.** Not a scope dispute: `DATA.md` § "Deploy is an EVENT, not a habit" exists
  because the coordinator was carrying this by memory, and `signals.py:145` keys the detector on
  the `deployed` event. A deploy talent that does not write the event leaves the system's only
  control dependent on the thing `DATA.md` calls "not a control". Fix is additive and one line in
  the "In this repo" section.
- **S6 — skill-bug, same root as S3.** The talent is missing the event/habit distinction as a
  RULE, and actively supplies the deferral excuse in step 6. Not a test-bug: the pressure is the
  exact argument `DATA.md` documents, and the file's own text is what fails to withstand it.
- Both are one defect family (D1+D2): activation is described as a step but never made
  mandatory, observable, or recorded, while wiring is all three.

## Proposed SKILL.md fixes (curator does not commit; coordinator applies)
1. **Add a Rule symmetric to the wiring rule:** "**A unit that has not been reloaded is not
   deployed.** Deploy is a per-unit EVENT, not a periodic habit — a scheduled or end-of-wave
   reload does not deploy this unit, and 'the next fresh session will load it' is a deferral, not
   a deploy. Activation (step 6) is not optional."
2. **Delete or requalify the escape hatch** in step 6. Replace "Fresh sessions load these
   directories from source at start, so a committed unit is always available next session even
   without a mid-session reload" with "A fresh session would load it eventually; that is not this
   deploy. Reload now, in this session."
3. **Make step 6 observable:** require recording the reload's confirmation (for this repo, the
   `context_reload_requested` return of `register_repo_root`) as the evidence that the unit is
   live, so findable-vs-live is checkable by an outsider rather than asserted.
4. **Step 7, "In this repo":** add "append a `deployed` event row for the talent to
   `pipeline/ledgers/talents.jsonl` (`{"talent":…,"event":"deployed","wave":N,"detail":…}`) — this
   is the row `pipeline/queries/signals.py` reads to prove the deploy gap is closed. Event rows
   merge forward: carry only the fields this event changes." Optionally generalize step 7 to
   "record the activation in whatever store the project's own deploy-gap detector reads".
5. **Fix D3:** "sharpen via `writing-skills`" → "sharpen via `skill-description-optimizer`
   (`writing-skills` is for authoring the unit, not for repairing a live trigger)".
6. Minor: write the reload argument as `directory` (the tool's real parameter name), not "dir".

## Result summary
- Scenarios passed: 8/8 · failure_cause: none (S3 and S6 were one skill-bug, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
S3 and S6 were triaged as **one skill-bug, not a test-bug**, and **the SKILL was changed; the
tests were not**. All three findings verified at the cited lines before acting.

D1 — step 7 said "update any tracking the project keeps" and named the catalog status and
`talents_used`. Neither is what the deploy-gap detector reads: `signals.py` computes the gap from
`deployed` event rows in `ledgers/talents.jsonl`, and every one of those rows had been written by
the coordinator by hand. So the talent whose entire job is closing the deploy gap never wrote the
record that measures it, and the gap stayed closed only by the coordinator remembering — which is
exactly what `DATA.md` calls "not a control". The coordinator's own habit is what hid the defect:
the numbers looked right for eleven waves because a human was silently doing the talent's work.

D2 — the `Rules` section made wiring mandatory and said nothing about activation, and step 6
ended with an escape clause ("fresh sessions load these directories from source at start, so a
committed unit is always available next session even without a mid-session reload"). True, and it
is the pressure argument written inside the checklist: the verb is *defer*, not *skip*, and the
outcome is identical for the session actually doing the work. Second instance this wave of the
CURATION-LESSONS pattern — an asymmetric rule across parallel branches, plus a gentler verb
reaching the forbidden outcome.

Fixed: step 6 now requires capturing the reload acknowledgement as evidence and names deferral as
non-deploy; step 7 is rewritten to record the activation *where the project's own deploy-gap
detector reads*, with creating that store named as part of deploying when none exists; a symmetric
rule now states that an un-reloaded unit is not deployed and that activation is a per-unit event,
not a periodic habit. D3 (sharpening routed to `writing-skills` instead of
`skill-description-optimizer`) and the `dir`/`directory` parameter-name error are fixed too.
