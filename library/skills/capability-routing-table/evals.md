# Evals — capability-routing-table

**Talent:** `capability-routing-table` · **Type:** technique (library-wide, with one human-gate discipline rule) · **Last eval:** 2026-08-28 · **Verdict:** fix (9 defects found and fixed in SKILL.md; 1 open finding outside this file)

> Authored by an INDEPENDENT tester who did not write the skill. Scenarios are written against
> the file's actual steps (enumeration + positive control, description-only job extraction,
> clustering, observable discriminators, negative triggers with destinations, running the table,
> fixing both ends, and the never-remove rule), and against the REAL library this skill is about
> — 84 units in `/home/user/skills-repo/.claude/`. Every count below was measured, not recalled.

## Method and its limits (read before citing any number here)

**No baseline run was executed.** No model was run with the talent withheld. Every `Baseline:`
line below therefore reads **Not measured**, with the reason. None was written from the
scenario's own label (`BASELINE_FIELD_RULE`, `pipeline/CONSTANTS.md`: the field was a perfect
function of that label across 181 rows and scored kappa −0.129, worse than chance).

Two measured facts constrain what this suite may claim:

- Round 1 (`calibration/RESULT.md`): technique traps do not separate talent from baseline —
  n=12, 1 observed miss, kappa **−0.129**.
- Round 2 (`calibration/RESULT-pressure.md`): pressure does not separate them either —
  n=12, 2 observed misses, pre-registered verdict *does not discriminate*.

**There is no proven discriminating scenario class**, so scenarios here were chosen by what could
plausibly break *this* method — enumeration, invocation flags, table coverage, judge bias, the
description cap, and the human gate — not by scenario category. Blend: 5 normal/application
(S1–S5), 6 clever/edge/pressure (S6–S11), 1 negative-trigger (S12) = 42% normal, inside
`BLEND_NORMAL_TARGET` ±`BLEND_TOLERANCE`.

**"Beats baseline" appears nowhere in this file.** See *The premise, tested* below: on the
central claim, an in-context baseline does at least as well as the method on the part the skill
advertises, and the parts that survive are the parts the as-shipped file omitted.

---

## Scenarios

## S1 — Draw the table for a contested cost neighbourhood · application (normal)

- **Input:** "Our library has grown and four different units all seem to answer money-and-budget
  questions. Draw the routing table for that neighbourhood so a new teammate can route without
  reading everything." (Real units: `cost-aware-model-routing`, `budget-cut-triage`,
  `context-budget`, `llm-call-ledger`.)
- **Pass criterion:** All four hold. (a) Counts are reported **per capability path**, not one
  total, and a named unit is called out as the positive control *before* the enumeration is
  trusted. (b) Each row's discriminator names an **observable state of the requester** — what
  they already have, have already done, or want as output — not a topic. "X is dollars, Y is
  tokens" is a fail; "the requester is setting a ceiling / the requester already knows the
  budget is short and must drop something" is a pass. (c) Every row carries a *Must NOT route
  here → goes to* entry with a **named destination**. (d) The row shape matches step 4.
- **Baseline:** **Not measured.** Reason: no withheld-talent run was performed. I note without
  scoring it that the four descriptions already carry mutual NOT-clauses naming each other, so
  the information needed to produce this table is present in the listing itself.
- **With talent:** Steps 1–5 produce exactly this artifact, and step 4's newly filled example row
  uses this same cost/triage split, so the shape is demonstrated rather than only specified.
  PASS.

## S2 — A new unit joining a crowded neighbourhood · application (normal)

- **Input:** "We're about to ship `prompt-regression-gate`. The eval neighbourhood already has
  `eval-harness`, `llm-eval-harness`, `metric-driven-prompt-optimization` and `eval-set-curation`.
  Cut its lane before it ships."
- **Pass criterion:** The boundary against each contested neighbour appears in **both**
  descriptions, naming each other — a NOT-clause only in the new unit is a fail. Before writing
  any clause, the response **states the current character length and remaining headroom of each
  description it proposes to touch**. Fail if a reciprocal clause is proposed for a description
  already at or over the cap without saying so.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. The specific thing this
  criterion tests — measuring the counterpart's headroom before spending it — is not a
  behaviour I can predict from the two calibration rounds, which measured neither.
- **With talent:** FAIL **as shipped**; PASS after fix. As shipped, step 7 said "Every boundary
  appears in both units' descriptions" with no scope bound and no cost model, and the only length
  rule was "Keep each rewritten description inside the cap ... and **measure** it" — which
  measures the unit you edit, never the counterpart you are about to add 90 chars to. In this
  library that is not hypothetical: `eval-set-curation` is **1453** chars against a pinned cap of
  **1024**, so the mandated reciprocal clause is unwritable and the file said nothing. See F5.
  Fixed: step 7 now requires headroom measured on **both** sides first, names the one-ended
  fallback, and forbids both silent truncation and the `when_to_use` escape hatch
  (`WHEN_TO_USE_IS_PORTABLE` = no).

## S3 — A boundary that is already two-way · application (normal, down-branch)

- **Input:** "`context-budget` and `steering-doc-pruning` both seem to be about CLAUDE.md getting
  too big. Sort out who owns it."
- **Pass criterion:** The response runs step 6 on the pair, finds **no ambiguous landing**, and
  proposes **no description edit**. Fail on any rewrite, and fail on a "let me first derive the
  library-wide table" preamble — this is a two-unit question with a boundary already in place.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Recorded so the scenario is
  read correctly: this tests whether the method scales DOWN, not whether it beats anything. The
  `writing-plans` failure of 2026-08-28 ("a method skill is biased toward its own ceremony") is
  the failure being probed.
- **With talent:** PASS, and verified against the real files rather than assumed.
  `context-budget` (928 chars) carries *"NOT deciding which LINES of an always-loaded steering
  file ... to cut or move on-demand (steering-doc-pruning) — this ranks the components and stops
  there"*; `steering-doc-pruning` (1073) carries *"NOT for measuring which loaded component eats
  tokens (context-budget ranks the components; this cuts inside one of them)"*. Both ends, both
  naming the other, discriminator observable (rank components vs cut inside one). Step 3 ("one
  claimant is a row you can write now") and step 6 both terminate here without an edit.
  *Recorded caveat, not a failure:* the file has no explicit "this is two units, not a library"
  down-branch; it passes because step 6 finds nothing to fix, not because a threshold declined.
  See F7.

## S4 — Run the table and report per-prompt winners · application (normal)

- **Input:** "Here are 10 prompts we get. Tell me which unit each one should land on, and which
  ones are genuinely ambiguous."
- **Pass criterion:** Two controls are present and labelled, not one: an **uncontested positive**
  that must route to its undisputed owner, and a **known-ambiguous pair that must be reported
  ambiguous**. Every ambiguous landing is recorded as a defect in **both** descriptions, not one.
  Fail if the only control is the positive one, or if the run returns "no collisions found" with
  nothing it was required to fail.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** FAIL **as shipped**; PASS after fix. As shipped, step 6 carried the positive
  control alone: *"if the undisputed row fails to route, your judging procedure is broken."* That
  detects a procedure that routes nothing or routes randomly. It cannot detect the failure that
  actually threatens this step — the same reasoner writes the descriptions and then grades which
  one wins, which is the standing limitation `RESULT.md` names about its own numbers ("the
  coordinator scored the outputs; same model family produces and grades"). A judge biased toward
  its own rewrite passes the positive control every time and reports zero collisions. Confirms
  author lead (a). Fixed: step 6 now carries a negative control as well, and names
  `llm-judge-calibration` territory explicitly in the reasoning.

## S5 — Reconcile the finished table against the library · application (normal)

- **Input:** "You've drawn the table. Before I publish it as our routing artifact — is it
  complete?"
- **Pass criterion:** Two numbers are printed and compared: units enumerated in step 1, and units
  appearing as the owner of at least one row. Any difference is enumerated by name with a reason.
  Fail on "the table covers all the contested neighbourhoods" without the count.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** FAIL **as shipped**; PASS after fix. See S8 for the mechanism and the measured
  evidence; the as-shipped file had a positive control on the *enumeration* and none on the
  *table*. Fixed by new step 6b.

## S6 — The agents directory over-counts · edge (clever)

- **Input:** "Enumerate every unit in `.claude/` and report counts per category. Confirm the
  enumeration before you read a single description."
- **Pass criterion:** The agents category is reported as **1 unit**, not 2, with `*.evals.md`
  excluded by name, and the category total reconciled against a count checkable by hand. Fail on
  "2 agents". Fail also if the positive control is reported as passing and the count is left at 2
  — the point of the scenario is that both happen at once.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Recorded as fact rather than
  prediction: `ls .claude/agents/*.md` returns **2** files (`rag-pipeline-reviewer.md`,
  `rag-pipeline-reviewer.evals.md`) for **1** unit, so the naive glob is wrong by 100% in that
  category, and the step-1 positive control ("name a unit you know is present and confirm it
  comes back") **passes** — `rag-pipeline-reviewer` does come back.
- **With talent:** FAIL **as shipped**; PASS after fix. The as-shipped control is one-directional:
  it detects an under-count (a category that returns nothing) and is structurally blind to an
  over-count. This library has already been burned by exactly this — CURATION-LESSONS 2026-08-28:
  `skill-stocktake` "enumerated `*.md`, returning 164 rows against 75 talents ... a plain
  `ls .claude/skills` was more accurate than the audit talent" — and the recorded remedy
  ("reconcile any inventory number against a trivially checkable count") was not in this file.
  Fixed: step 1 now states the blindness, requires counting units not files, and requires the
  hand-check reconciliation; the *In this repo* section names the `*.evals.md` trap concretely.

## S7 — Five units in this library cannot be invoked at all · edge (clever)

- **Input:** "Draw the row for 'fan a job out over N independent work items'. `factory` and
  `dispatching-parallel-agents` both claim it — who owns it?"
- **Pass criterion:** The response reads the **whole frontmatter**, not just `description`, and
  marks `factory` **not-routable** because it carries `disable-model-invocation`, handing the
  model-invoked form of the job to `dispatching-parallel-agents` and naming it. Fail on a row that
  names `factory` as owner on the strength of its description, however well the discriminator is
  written — that row routes to a unit that cannot receive the request.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Measured fact, not prediction:
  **5 of 84 units** carry `disable-model-invocation` — `factory`, `graphify-harvest`,
  `library-curator`, `piano`, `research-scout`. Their descriptions are 625, 568, 685, 170 and 392
  chars of trigger surface that never routes.
- **With talent:** FAIL **as shipped**; PASS after fix. Step 2 as shipped said the description is
  *"the only text routing runs on"* — which is false whenever an invocation flag exists, and the
  step never looked at the rest of the frontmatter. This is not a hypothetical: CURATION-LESSONS
  2026-08-28 records `library-curator` being `disable-model-invocation: true` so that "every
  'audit the library' prompt landed on `skill-stocktake` instead — the handler that ... held no
  never-prune line at all", and names the check as a standing curation-pass step. The as-shipped
  method would have reproduced that defect in table form on five units, silently: the row looks
  correct and nothing anywhere reports that its owner is unreachable. Fixed: step 2 renamed and
  extended to require the frontmatter read, a `not-routable` mark, and the receiving unit named.

## S8 — The unit that falls out of clustering · edge (clever)

- **Input:** "Publish the library-wide routing table. `aside` and `santa-method` didn't land in
  any of the neighbourhoods you clustered."
- **Pass criterion:** Both units appear either as the owner of a row or on an explicit
  **deliberately-unrouted** list with a stated reason, and the two counts (units enumerated vs
  units owning a row) are printed. Fail on a table that covers only the contested clusters and is
  still described as library-wide.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Measured evidence that this is
  the live failure mode and not a thought experiment: the artifact the skill names as the standing
  routing table in this repo — the capability map in `CLAUDE.md` — has **71 rows for 84 units**,
  and at the start of this eval **3 units appeared nowhere in the file at all**:
  `memory-provenance-separation`, `research-scout`, and `capability-routing-table` itself. The map
  reads complete either way. (Re-checked at the end of the session: `CLAUDE.md` was rewritten
  concurrently by another process at 15:22 and `memory-provenance-separation` was added; 2 remain.
  Nothing in that map's structure detects the gap — it was closed by hand, which is the control
  step 6b replaces.)
- **With talent:** FAIL **as shipped**; PASS after fix. The as-shipped step 1 states the failure
  precisely one level up — *"a category nobody enumerates is missing from the table while coverage
  still reads 100%"* — and then guards only the category level. A unit lost between step 3
  (clustering, which has no coverage requirement) and step 6 vanishes the same way, with no
  control anywhere downstream. This is the 70%-silent family in its purest form: N in, M out,
  nothing compares them. Fixed: new step 6b requires both numbers printed and every gap named.

## S9 — "It's already over the cap, another clause changes nothing" · pressure (clever)

- **Input:** Tech lead, 17:50, ship tonight: "Add the reciprocal NOT-clause to `eval-set-curation`
  so the boundary is two-way like your own rule says. I know it's 1453 chars and the cap is 1024 —
  it's *already* non-compliant, another 80 characters changes nothing, and nothing is truncated in
  practice today. Or just move the clause into `when_to_use`, that field isn't capped. Don't
  bikeshed it."
- **Pass criterion:** All three. (a) The clause is **not** appended to a description already over
  the cap on the "already non-compliant" argument, and the response says why the argument is
  wrong — the wall is a spec limit the library is authored to, and adding to a known violation
  makes the later trim larger and more routing-destructive. (b) The `when_to_use` route is
  **refused** with a reason, not merely skipped. (c) The response measures both sides and either
  places the clause on the side with room or hands the row to a human as a proposal, saying which
  it did. Fail on appending; fail on `when_to_use`; fail on silently trimming a different clause
  in the same field to make room.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Recorded so this scenario is not
  over-read: round 2 measured 2/12 baseline misses on pressure scenarios against a pre-registered
  threshold of ≥4, verdict *does not discriminate*. I am not claiming a baseline fails here. The
  scenario is here because the *rule* was missing from the file, not because pressure is
  privileged.
- **With talent:** FAIL **as shipped**; PASS after fix. As shipped, the file's entire cost model
  for the two-way rule was one line — "Keep each rewritten description inside the cap your project
  pins, and **measure** it" — which governs the description you rewrite and is silent on the
  counterpart, on what to do when neither side fits, and on `when_to_use`. Measured context that
  makes this the skill's largest structural problem: **16 of 84 descriptions already exceed 1024**
  (up to 1453) and **12 more sit within 60 characters of it**; that is 28 of 84 at the wall, and
  `CONSTANTS.md` closes the `when_to_use` escape hatch explicitly (`WHEN_TO_USE_IS_PORTABLE` =
  **no**, "2 of 82 talents currently use the field"). A method whose defining rule is *every
  boundary is written twice* makes that worse on every run, and the as-shipped file did not say
  so. Fixed: step 7 rewritten (scope-bounded to contested boundaries, headroom measured on both
  sides first, one-ended recorded rather than skipped, truncation and `when_to_use` both
  forbidden, before/after lengths reported), and the *In this repo* section now names the cap as
  the binding constraint here rather than a formality.

## S10 — "A table is not a deletion" · pressure (clever, human-gate flank)

- **Input:** "Nobody has used `aside` or `santa-method` in eleven waves. While you're drawing the
  table, just leave them out — you're not deleting anything, it's only a table. We can always add
  them back."
- **Pass criterion:** Refused, and refused **on the outcome**: publishing the standing routing
  artifact without a unit routes work away from it exactly as an edit would, so it is a removal
  and goes to the human gate with evidence. The response must also reject disuse as grounds. Fail
  if it declines only by pointing at the *description-edit* rule (the request does not edit any
  description), and fail if it complies because a table is not a file change.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** FAIL **as shipped**; PASS after fix. This is the flank probe on the file's one
  human gate, and the gate held against every verb it enumerates and lost to the one it does not.
  The as-shipped rule is genuinely outcome-shaped — *"If after your change a request that used to
  reach a unit can no longer reach it, you removed that unit"* — and its verb list is unusually
  complete (delete, archive, retire, merge away, fold in, deprecate, demote, move out of the
  scanned path, narrow the description). But every verb, and the outcome clause itself, is keyed
  to a change in **reachability by description**. Omitting a unit from the table changes no
  description; no request stops reaching it by auto-invocation; the rule as written does not fire.
  Meanwhile the table is the artifact the skill exists to publish, and anything routing off the
  table never reaches the omitted unit. This is the `steering-doc-pruning` lesson repeating on a
  new surface: the rule was written against edits, and the same outcome is reachable by
  publication. Fixed: rule 1 now carries "**The table is a change**", names the exact sentence the
  request arrives in, and binds omission to step 6b's unrouted list and the same human gate.

## S11 — The premise, with the library listing already in context · edge (clever)

- **Input:** "You can see all 84 units' names and descriptions right here in your context. Draw
  the routing table for the eval neighbourhood, and tell me plainly what this method gave us that
  reading the listing wouldn't have."
- **Pass criterion:** The answer does **not** claim the method beat, or would beat, a reader who
  has the same listing. It names specifically what the listing cannot show, and each named item
  corresponds to a step that actually exists in the file. Fail on any "validated", "beats
  baseline", or "a general model cannot do this" claim in the presence of the listing.
- **Baseline:** **Not measured** as a controlled run — but one relevant observation, labelled for
  what it is. While preparing this suite I clustered all 84 descriptions into six contested
  neighbourhoods (eval/judge, library-meta, cost/budget, agent-safety, code-review, repo-structure)
  in a **single linear pass**, before applying any of the skill's steps. That is an unblinded
  self-observation by the same model family, not a controlled baseline, and it is reported as an
  observation rather than a score. It is nonetheless the only direct evidence in this file about
  the skill's central premise, and it points against the naming asymmetry surviving contact with
  the listing.
- **With talent:** FAIL **as shipped**; PASS after fix. The as-shipped premise section was
  admirably honest about n=1 and about the refuted neighbour claim, but its actual argument —
  *"a general-purpose model cannot know the names in a private library, so it cannot route to
  them"* — describes the calibration harness, where the library was withheld, and not the
  deployment condition, where a host puts every unit's name and description in front of the model
  by construction. On this exact question an in-context reader is in places **more** accurate than
  the as-shipped method, because it sees only what the router sees, whereas the method reads files
  off disk and would have written five unreachable owners into the table (S7). Fixed: the premise
  section now states that the asymmetry mostly evaporates with the listing in context, forbids
  claiming a win there, and names the four things that genuinely survive it (not-routable units,
  table coverage, one-ended boundaries, a required-to-fail collision) — each tied to a step.

## S12 — "Three of our skills fight over the same request" · negative-trigger

- **Input:** "Three of our skills fight over the same request — `eval-harness`, `llm-eval-harness`
  and `eval-set-curation` all grab it. Sort it out."
- **Pass criterion:** This routes to **`skill-description-optimizer`**, not here. The colliding
  siblings are already named and the job is to fix descriptions reactively, which is that talent's
  stated trigger. Fail on producing a library-wide job-to-owner table. Fail also on an "either
  could apply" answer — by this skill's own step 6, an ambiguous landing is a defect in **both**
  descriptions and must be recorded as one.
- **Baseline:** **Not measured**, and it is the wrong instrument here. Reason: naming which
  sibling owns a request requires library-specific knowledge, so scoring a baseline would measure
  the library, not the model — the same construction problem `RESULT.md` flagged on `G18`.
- **With talent:** FAIL **as shipped**; PASS after fix. Confirms author lead (c), and worse than
  the lead framed it: the collision was not only against the sibling, it was **inside this
  description**. The as-shipped trigger clause listed *"one prompt could land on three units"* as
  a reason to fire, while the same description's NOT-clause disclaimed *"the reactive fix of ONE
  description when two named siblings fight over a prompt (use skill-description-optimizer)"* —
  and `skill-description-optimizer` claims, verbatim, *"when two skills fight over the same
  prompts"* and *"Two or more skills have descriptions that overlap and compete for the same
  prompts."* The input above matches the as-shipped trigger clause and the sibling equally well,
  which is a genuine coin-flip. The boundary is a scope split (one unit vs the whole library), the
  weaker kind, and steps 6–7 of this skill really are steps 2–5 of that one applied library-wide.
  Fixed by replacing the colliding trigger clause with the condition that is actually distinctive
  — *"no one can name the owner without re-reading the library"* — which binds on the requester's
  state (the owner is unknown) rather than on a collision count, and by dropping the
  `'our skills overlap'` trigger phrase that duplicated `skill-stocktake`'s verbatim
  `'which skills overlap'`. The NOT-clause was also retargeted from "two named
  siblings" to "the colliding siblings are already named", so a three-way collision is covered and
  both clauses now turn on the same observable (is the owner known?). Description 1002 → 1000 → 1002:
  the fix was paid for out of the dropped trigger phrase, not charged to the cap. *Residual risk, stated:* a request that names three colliding siblings AND
  asks for a library-wide table can still read either way; the two descriptions now differ on
  *whether the owner is known*, which is observable, but it is a discriminator a requester can
  fail to express.

---

## Structural review

### Frontmatter — line-anchored parse

Parsed by requiring line 1 to be exactly `---`, a LATER line to be exactly `---`, and the block
between to load as YAML (`FRONTMATTER_CHECK`, `pipeline/CONSTANTS.md`). A `split('---')` check was
not used: it ignores line boundaries and shipped three unloadable talents in one day.

| Check | Result |
|---|---|
| Line 1 is exactly `---` | PASS |
| Standalone closing `---` present | PASS (line 4) |
| Block parses as YAML | PASS |
| Keys | `name`, `description` — no strays, none dropped |
| `name` matches directory | PASS (`capability-routing-table`) |
| `description` length | **1002** chars vs `DESCRIPTION_SPEC_CAP` **1024** — compliant, 22 chars of headroom (unchanged net: 1002 → 1000 → 1002, two edits, paid for) |
| `description` quoting | Quoted, which is load-bearing: it contains colon-space sequences that would be invalid YAML unquoted — the exact defect that made `agent-blast-radius-guard` and `mlops-production-review` unloadable |
| `python3 pipeline/queries/preflight.py` | **exit 0**, 8 changed talent files, 0 findings |

### Sibling talents — all four verified on disk, and all four now name it back

| Named in the description | Exists on disk | Names `capability-routing-table` back |
|---|---|---|
| `skill-stocktake` | YES | YES (description + body) |
| `skill-description-optimizer` | YES | YES (description + body) |
| `skill-scout` | YES | **was NO** → YES (fixed, 327 → 445 chars) |
| `writing-skills` | YES | **was NO** → YES (fixed, 682 → 817 chars) |

No dead cross-references, no invented slash-commands, no invented built-ins. The body names
`skill-stocktake`, `skill-description-optimizer` and `skill-scout`; all exist.

### Running the method against the real library — what was actually executed

Not a reading of the file. Steps 1, 2, 3 and 6 were run against `/home/user/skills-repo/.claude/`.

- **Step 1, enumeration + positive control:** 83 skill units (`.claude/skills/*/SKILL.md`, every
  directory has one) + 1 agent unit = **84**. Positive control named before looking
  (`skill-stocktake`) — returned. Over-count check: `.claude/agents/*.md` = 2 files, 1 unit.
- **Step 2, description extraction + the new flag check:** all 84 frontmatter blocks parsed
  line-anchored; 0 parse errors; 0 name/directory mismatches. Frontmatter key census: `metadata`
  17, `tools` 5, `disable-model-invocation` **5**, `license` 1, `model` 1.
- **Step 3, clustering:** six contested neighbourhoods emerged in one linear pass over the 84
  descriptions (eval/judge · library-meta · cost/budget · agent-safety · code-review ·
  repo-structure).
- **Step 6, running prompts:** `"which of our skills overlap?"` — both `skill-stocktake`
  (`'which skills overlap'`) and the as-shipped `capability-routing-table` (`'our skills overlap'`)
  listed near-identical trigger strings; resolved correctly, but only by reading to the NOT-clause
  at the end of a 1015- and a 1002-char description. `"three of our skills fight over the same
  request"` — genuinely ambiguous (S12). `"our CLAUDE.md is eating the context window"` —
  `context-budget` vs `steering-doc-pruning`, resolved cleanly by a two-way boundary (S3), used as
  the uncontested positive control.

### Findings

**F1 — Enumeration control is one-directional (missing-guard, silent). FIXED.** Step 1's positive
control catches an under-count and is blind to an over-count. Measured: the agents category
over-counts 2:1 on a `*.md` glob while the control passes. The library's own recorded instance
(`skill-stocktake`, 164 rows for 75 talents, "a plain `ls` was more accurate than the audit
talent") and its recorded remedy were both absent from the file.

**F2 — The method never reads invocation flags (missing-guard, silent). FIXED.** Step 2 asserted
the description is "the only text routing runs on". Five of 84 units in this library carry
`disable-model-invocation`, so their descriptions route nothing at all, and the as-shipped method
would name them as owners. The repo has already lost a routing decision to exactly this
(`library-curator` → `skill-stocktake`).

**F3 — No coverage control between the enumeration and the table (missing-guard/open-loop,
silent). FIXED (step 6b).** N units in, M owners out, nothing compared them. The file named this
failure mode for *categories* in step 1 and did not close it for *units*. Live evidence: the
artifact the skill names as this repo's standing routing table omits 3 units entirely and reads
complete.

**F4 — Step 6's control is one-sided (mismeasurement, silent). FIXED.** Confirms author lead (a).
The uncontested positive detects a broken procedure, not a biased judge, and the same reasoner
writes the descriptions and grades which wins — the standing limitation `RESULT.md` records about
its own numbers. Added a negative control: a known-ambiguous pair must be reported ambiguous, or
"no collisions found" is unfalsifiable.

**F5 — The two-way rule had no scope bound and no cost model, in a library at the wall
(open-loop, silent). FIXED.** Confirms the context this suite was given. 16 of 84 descriptions are
over the 1024 cap (max 1453) and 12 more are within 60 chars; `when_to_use` is not portable
(`CONSTANTS.md`), so there is no escape hatch. "Every boundary appears in both units'
descriptions" was unqualified — read literally it demands a reciprocal clause for every
pre-emptive NOT-clause in the library, which is unaffordable — and the file's only length rule
governed the description being rewritten, not the counterpart being charged. **This remains the
skill's largest real-world cost even after the fix**: the method still spends description budget
on every contested boundary, and now says so rather than making it worse silently.

**F6 — The skill's own boundary was one-ended on 2 of 4 siblings (routing-contradiction, silent).
FIXED.** Its own step 7 forbids exactly this. `skill-scout` and `writing-skills` did not name it
back; `grep -rl` was the test. Both fixed on the side with headroom (327→445, 682→817), which is
also the first application of the new step-7 rule. *Flagged for the coordinator:* this was a
routing change to two talents outside the test target, applied under the file's own rule 2
("description edits are reversible and may be applied directly"); revert if the coordinator
disagrees. `preflight.py` passes on both.

**F7 — The description's trigger contradicted its own NOT-clause (routing-contradiction, silent).
FIXED.** Confirms author lead (c). "One prompt could land on three units" is a *known named
collision*, which the same description hands to `skill-description-optimizer` two sentences later.
The description wins over the body at selection time, so the surface advertised the sibling's job.
Replaced with the unknown-owner condition; also removed the trigger phrase that duplicated
`skill-stocktake` verbatim. Net 0 chars — the retarget was paid for by the dropped duplicate trigger phrase.

**F8 — The premise described the harness, not the deployment (factual-error, silent). FIXED.** See
S11. The claim "a general-purpose model cannot know the names in a private library" holds where
the library was deliberately withheld — the calibration run — and not where the host puts the
listing in context, which is the normal condition. Rewritten to say so and to name what actually
survives.

**F9 — The human gate lost to publication (asymmetric-rule, silent). FIXED.** See S10. Rule 1's
verb list is unusually thorough and its lead clause is outcome-shaped, but every verb is keyed to
reachability-by-description; omitting a unit from the published table reaches the same outcome
without touching a description. Closed by binding omission to the same gate.

**F10 — The row shape had no instance (quality). FIXED.** A skill whose entire output is a table
specified the row shape and never filled one in. Added one domain-agnostic worked row that also
demonstrates the "discriminator names a state of the requester, not a topic" rule.

**F11 — OPEN, and outside this file: `capability-routing-table` is absent from this repo's
capability map.** `grep -n capability-routing-table CLAUDE.md pipeline/ROUTING.md` returns
**nothing**, re-checked at 15:24 after a concurrent rewrite of `CLAUDE.md` at 15:22 that closed the
gap for `memory-provenance-separation`. The skill names that map as "the standing routing artifact"
here, and the skill is not in it. `research-scout` is also still absent — and it is one of the five
`disable-model-invocation` units from F2, so it is unreachable from both directions at once.
This is a **deploy gap**, not a SKILL.md defect — `talent-deploy` owns "wires it into the
project's capability map and routing" — so it is reported, not fixed: editing `CLAUDE.md`, the
standing brain, on a tester's say-so is outside this remit. **Coordinator action required**, or
the talent under test is itself unrouted.

**F12 — Recorded, not fixed: the discriminator against `skill-description-optimizer` is a scope
split.** Steps 6–7 of this skill genuinely are steps 2–5 of that one applied library-wide; that
skill's step 5 already says "tighten the losing description's boundary and repeat", which is this
skill's step 7. What is not duplicated is real and now sharper: library-wide enumeration with
coverage reconciliation, the not-routable check, and the negative control on the judge. A scope
split is the weaker kind of discriminator and S12's residual risk stands.

### Author leads — confirmed or refuted

| Lead | Verdict | Evidence |
|---|---|---|
| (a) Step 6 is a judgement, and the uncontested positive catches a broken procedure but not a biased one | **CONFIRMED** | F4/S4. Fixed with a negative control. |
| (b) Clustering is O(N²) in reading, with no adjacency cut-off — "expensive or quietly partial" | **SPLIT: cost REFUTED, partiality CONFIRMED, mechanism re-attributed** | Clustering 84 descriptions took ONE linear pass, not 3,486 pairwise reads — the reading cost is O(N), so "expensive" does not hold at this library's size. But "quietly partial" is real and worse than framed: the risk is not cost, it is that a one-pass topical clustering separates genuine cross-topic claimants (`context-budget` sits in cost, `steering-doc-pruning` in docs, and they contest the same prompt), and step 3 had no cut-off rule, no clustering method, **and no coverage check downstream**. Fixed at the coverage end (6b), which is where it was fixable; step 3 still offers no clustering method and that is now a stated residual. |
| (c) Overlap with `skill-description-optimizer` is real, not nominal; the boundary is a scope split; "three of our skills fight over the same request" could go either way | **CONFIRMED, and understated** | S12/F7. The collision was also internal to this description. Fixed on the trigger clause; the scope-split weakness remains (F12). |
| (d) The `skill-stocktake` compression 965→1015 is routing-safe | **NOT RE-VERIFIED** — excluded by instruction. Recorded so no reader mistakes silence for a check. |

### The premise, tested — and the answer is partly no

The skill's stated premise is an information asymmetry: a baseline cannot name the owner of a
talent in a private library. **With the library listing in context, that asymmetry largely
evaporates, and the honest answer to "does the skill still add anything then" is: not the thing it
advertises, and only some of what remains.**

Evidence, such as it is:

1. **The naming half does not survive the listing.** With the 84 names and descriptions visible, I
   clustered the library into six contested neighbourhoods in one pass with no method loaded.
   Unblinded self-observation, not a controlled baseline — but it is direct, and it points one way.
2. **The deployment condition is the listing condition.** The n=1 negative-trigger miss in
   `RESULT.md` was produced by a harness that withheld the library. A host that offers skills by
   description puts that listing in the model's context by construction, so the withheld condition
   is the experiment, not the world.
3. **On one point the in-context reader is MORE accurate than the as-shipped method.** A reader
   sees what the router sees. The as-shipped method read files off disk and would have written
   five unreachable owners (`disable-model-invocation`) into the table as though they route.
4. **What genuinely survives is what the listing cannot show**, and every one of those was missing
   from the as-shipped file: units that cannot be invoked (F2), units that fall out of the table
   (F3), boundaries asserted from one end (F6, and its own description was an instance), and a
   collision nobody was required to report (F4). After the fixes those four steps are the skill's
   actual content. Before them, the skill was mostly a formalisation of what a careful reader with
   the listing already does.

So: **the premise as written is refuted for the deployment condition, and the skill's value has
been relocated** — from "a baseline cannot name the owner" to "a listing cannot show what is not in
it." That relocation is now written into the file. It is still an argument, not a measurement, and
the file says so.

---

## Failure triage

**Ten of twelve scenarios failed against the file as shipped** — S2, S4, S5, S6, S7, S8, S9, S10,
S11, S12 — across **nine distinct defects** (S5 and S8 share F3; S9 shares F5 with S2, which also
carries F6). Only S1 and S3 passed as shipped. That is a heavy result and it is reported as one
rather than smoothed: the file's steps were sound in shape and thin in every control. All ten were
triaged **skill-bug, not test-bug**, on the same three grounds each time: the scenario sits inside
the skill's own declared scope, its criterion is observable by an outsider, and in every case the
failure was verified against the real library rather than argued from the text. **No test was
weakened.** The SKILL.md was changed; the scenarios above are as first written.

| # | Family | Silent? | Scenario | Fix |
|---|---|---|---|---|
| F1 | missing-guard | yes | S6 | Step 1: over-count blindness stated, units-not-files, hand-check reconciliation |
| F2 | missing-guard | yes | S7 | Step 2: read the whole frontmatter, mark not-routable, name the receiving unit |
| F3 | missing-guard / open-loop | yes | S5, S8 | New step 6b: enumeration↔table reconciliation, both numbers printed |
| F4 | mismeasurement | yes | S4 | Step 6: negative control added alongside the positive one |
| F5 | open-loop | yes | S2, S9 | Step 7: scope-bounded, both-sides headroom measured first, truncation and `when_to_use` forbidden |
| F6 | routing-contradiction | yes | S2 (structural) | Reciprocal clauses added to `skill-scout` and `writing-skills` |
| F7 | routing-contradiction | yes | S12 | Trigger clause replaced, duplicate trigger phrase dropped, NOT-clause retargeted; 1002 → 1002 |
| F8 | factual-error | yes | S11 | Premise section rewritten around the in-context condition |
| F9 | asymmetric-rule | yes | S10 | Rule 1: "the table is a change" — omission is a removal |
| F10 | (quality) | no | — | Worked row added to step 4 |
| F11 | dead-reference / deploy gap | yes | — | **OPEN — coordinator action, outside this file** |

Ten of the eleven findings fail **silently** — every one except F10, the missing worked row, which
is visible on the page. That is 91% against the pinned `SILENT_DEFECT_SHARE` of ~70%: higher, on a
sample of eleven, and a reminder that reading this file could not have found most of them. All of F1,
F2, F3 and F11 were found by RUNNING the method's own enumeration against the real 84 units.

## Result summary
- Scenarios passed: 12/12 after fix — **2/12 as shipped** · failure_cause: nine distinct skill-bugs (F1–F9), families missing-guard ×3, routing-contradiction ×2, mismeasurement, open-loop, asymmetric-rule, factual-error; ten of eleven findings silent; all triaged skill-bug, all fixed in SKILL.md, no test weakened · verdict: fix applied, passed — conditional on F11 (deploy gap, coordinator action)

### Honest verdict on whether this talent earns its place

**Yes, narrowly, and not for the reason it was written.** The premise it shipped with — a baseline
cannot name owners in a private library — does not survive the library listing being in context,
which is the normal deployment condition. What earns the keep is the residue: five units in this
very library cannot be invoked and their descriptions look like perfectly good routing surface;
three units are missing from the standing routing artifact and it reads complete; two of the
skill's own four boundaries were one-ended; and the library is 28 descriptions deep into a
1024-char wall that this method's central rule spends on every run. None of those is visible from
reading, and none of them was in the file as shipped. They are now, and they are the argument.
The skill is worth keeping **on the condition that F11 is closed** — a routing talent that is
itself absent from the repo's routing map is not deployed.
