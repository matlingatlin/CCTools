# Evals — writing-plans

> Follows `templates/EVALS.template.md`. Authored per `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (triage before fix/drop; observable criteria; blend normal + clever;
> clever ones fail at baseline; verify cross-refs AND hand-offs from BOTH ends; hunt
> asymmetric rules and milder-verb flanks). Authored by an INDEPENDENT curator
> (library-curator, database-2) who did not write the talent.

**Talent:** `writing-plans` · **Type:** technique (with two discipline edges: the no-placeholders / bite-sized bans, and the Scope Check down-branch) · **Last eval:** 2026-08-28 (S1–S10) · 2026-08-28, second independent pass (S11–S17) · **Verdict:** fix — 16/17; S8 and S9 were fixed in the first pass, S16 is an OPEN skill-bug from the second (see triage F3)

## Method
Baseline-vs-with: for each scenario judge the plan a capable agent would write WITHOUT the
talent vs WITH its method applied (File Structure map → Task Right-Sizing → mandatory header
with Spec + Global Constraints → Task Structure with Interfaces → bite-sized TDD steps →
No-Placeholders → Self-Review → Execution Handoff). A scenario passes only if the with-talent
result meets the observable criterion. Normal scenarios confirm the everyday job and a capable
baseline may also pass them — those end in a plain **PASS**; only the clever ones and the
negative-trigger claim **Beats baseline**.

## Structural findings (pre-test audit)

**Cross-references — every named sibling, checked on disk:**

| Named in SKILL.md | On disk? | Verdict |
| --- | --- | --- |
| `using-git-worktrees` (L16) | `.claude/skills/using-git-worktrees/` ✓ | talent exists; **namespace wrong** (see below) |
| `subagent-driven-development` (L61, L166) | `.claude/skills/subagent-driven-development/` ✓ | talent exists; **namespace wrong** |
| `superpowers:executing-plans` (L61, L170) / `executing-plans` (L161) | ✗ **not in this library** | **DEAD** — exists only upstream at `obra/superpowers/skills/executing-plans`, never adopted |
| `brainstorming` (L23, implicit) | `.claude/skills/brainstorming/` ✓ | ok |
| `docs/superpowers/plans/…` (L18, L157) | consistent with SDD L509 | ok (portability note below) |
| `plan-document-reviewer-prompt.md` (bundled) | on disk, **referenced by nothing** | **ORPHAN + contradicted** (see below) |

- **Namespace does not resolve.** `~/.claude/plugins/installed_plugins.json` is `{"plugins": {}}` —
  no `superpowers` plugin is installed. These talents are adopted as *project-scoped* skills in
  `.claude/skills/`, which load by bare name. So the entire chain
  `brainstorming → writing-plans → subagent-driven-development` is written here in an invocation
  form that resolves to nothing. Recoverable for the two adopted names (an agent will find the
  local skill anyway); **unrecoverable for `executing-plans`**, which has no local fallback.
  Precedent for the fix is already set by the curator of the sibling: `subagent-driven-development/evals.md:27`
  keeps `superpowers:` *only* on `executing-plans` and states why ("an external superpowers
  sibling … not a dead local ref"). `writing-plans` never marks it as external, and at L161 drops
  the prefix entirely ("using executing-plans"), which reads as a local talent.
- **Orphaned bundled asset.** `plan-document-reviewer-prompt.md` ships in the talent directory,
  is referenced by **zero** files repo-wide, and its premise ("Use this template when dispatching
  a plan document reviewer subagent") is explicitly negated by SKILL.md L143: *"This is a checklist
  you run yourself — not a subagent dispatch."* The plan-review gate was downgraded to an inline
  self-check and the asset was left behind. Same defect family as the eleven prior failures: a file
  asserting a step the talent does not perform.
- **Invented slash-commands / built-ins / tool names:** none. Clean. Every invocation form in the
  file is either a skill name or a shell command (`pytest …`, `git add`/`git commit`) used as
  illustrative example code — valid.
- **Frontmatter:** `name: writing-plans` present and matches the directory ✓. Description is
  97 chars (≤1536 ✓), triggers-only ✓, house-style "Use when …" ✓. It is however the *thinnest*
  description in this chain and carries **no boundary at all** — four siblings
  (`subagent-driven-development`, `brainstorming`, `prompt-refinement`, `expand-contract-migration`)
  each name `writing-plans` as their not-this, and `writing-plans` names none of them back.
  Sharpening candidate, not a defect.
- **Format-drift:** none. Tests land here in `evals.md`; no `evals/` dir. ✓
- **Portability:** the method itself is general ✓, but `docs/superpowers/plans/YYYY-MM-DD-…`,
  the `superpowers:` namespace, and the Python/pytest task example are baked into the body, and
  there is **no "In this repo (one instance)" section**. Mitigated by L19 ("User preferences for
  plan location override this default"). Minor — flag, don't fail.
- **Provenance:** `diff` against `obra/superpowers/skills/writing-plans/SKILL.md` is **byte-identical**.
  This talent was adopted pre-loop (`ledgers/talents.jsonl:64`, `tested: false`) and has never had
  the adoption pass (cross-ref rewrite, portability section, orphan sweep) run on it. Every finding
  above is inherited, not authored here.

**Hand-off verified from BOTH ends (per the 2026-08-28 directive):**

| Claim made elsewhere | Verified in `writing-plans`? |
| --- | --- |
| `brainstorming` L103/L231: "invoke writing-plans … Do NOT invoke any other skill" | ✓ closed — `writing-plans` L23 Scope Check assumes brainstorming ran ("it should have been broken into sub-project specs during brainstorming"), and the header's `Spec:` field consumes brainstorming's output path |
| `subagent-driven-development` L156/L165/L329: reads "the plan's Global Constraints", copies them **verbatim** into every task reviewer's rubric | ✓ closed — `writing-plans` L72-77 makes a populated `## Global Constraints` block mandatory, verbatim from the spec. Producer and consumer agree. |
| `subagent-driven-development` description: "not authoring the plan itself (writing-plans)" | ✓ closed — no execution machinery in `writing-plans`; it stops at handoff |
| `CLAUDE.md:69` "Plan then execute → `writing-plans` → `subagent-driven-development`" | ✓ closed |
| `prompt-refinement` description: "use writing-plans to plan the work once the request is clear" | ✓ compatible — `writing-plans` triggers on "a spec or requirements"; no back-reference, but nothing is asserted about it that it fails to do |
| `pipeline/ROUTING.md:13`: talent authoring routes `templates/` scaffold → `writing-plans` → `writing-skills` | ⚠ **partially open** — `writing-plans`'s task template is code+pytest-shaped ("code blocks required for code steps"); it works for authoring a talent, but nothing in either file connects them. Documentation intention, not a behaviour. Low severity. |
| `expand-contract-migration/evals.md:366-368`: "hand it to `writing-plans` to render" the phase sequence | ⚠ **one-ended** — `writing-plans` never mentions expand-contract. Pending `ledgers/proposals.jsonl` fold-in (wave 26, `outcome: pending`), so this is a stated *plan*, not a broken loop. No action beyond resolving that proposal. |
| `pipeline/STATUS.md:102` "expand-contract sequencing folds into `writing-plans`" | same pending proposal — not yet a claim of current behaviour ✓ |

**Asymmetric rules found (the pattern that felled two talents this week):**
1. **Scope Check is one-directional.** L21-23 scales the plan *up*→*split* (spec covers multiple
   subsystems → separate plans) and has **no down-scope counterpart** — nothing anywhere in the
   file says a change can be too small to deserve a plan document. Its own upstream sibling
   `brainstorming` has exactly that branch (`"Implement via normal workflow (no plan doc)"`,
   SKILL.md L~119). Tested as S8 — **fails**.
2. **No Placeholders binds steps, not the header.** L133: *"Every **step** must contain the actual
   content…"*, and the Self-Review placeholder scan (L147) searches for "the patterns from the
   No Placeholders section" — all of which are step-level. The header's own bracket placeholders
   (`[One sentence…]`, `[The spec's project-wide requirements…]`) are therefore outside the ban,
   even though SDD copies that block **verbatim** into every reviewer rubric. The mandatory-header
   rule (L56 "Every plan MUST start with this header") is strong enough that this does not fail in
   practice (S3 passes) — but the *verification* half is missing while the *authoring* half exists.
   Sharpening proposal, not a fail.
3. **Self-Review is one-shot and has no re-entry.** L151: "No need to re-review — just fix and move
   on." There is no trigger that sends you back into it when the spec changes underneath the plan.
   The mechanism exists and composes correctly (S7 passes) but is never pointed at that event.

**Milder-verb flank (per the 2026-08-28 directive) — mostly closed.** The No-Placeholders ban is
written against outcomes rather than single verbs: it bans "TBD"/"TODO"/"implement later"
(the defer flank), "Add appropriate error handling" (the vague-gesture flank), "Similar to Task N"
(the reference flank), and the catch-all *"Steps that describe what to do without showing how"*.
The one flank left open is **cross-task reference by pointer** — "see Task 3 for the type" is
neither "Similar to Task N" nor "a reference to a type not defined in any task", yet produces the
identical failure. The **Interfaces / Consumes** block (L92-96) closes it by a different route, so
the talent survives the attack — tested as S6, passes.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — normal/representative: S1–S4, S11 (the everyday plan-writing job);
      clever: S5–S9 and S12–S16; negative-trigger: S10, S17. 5 normal / 10 clever / 2 negative.
      Second pass deliberately weighted toward PRESSURE (S12–S15) over technique traps — see the
      calibration note below.
- [x] **Specific to this talent** — every scenario turns on a named rule of THIS file
      (Scope Check, Task Right-Sizing, Global Constraints, Interfaces block, bite-sized steps,
      No Placeholders, Self-Review, Execution Handoff). No generic planning boilerplate.
- [x] **Observable pass/fail criterion** on every scenario — each names a checkable artifact
      (a block present, a run command with an expected result, a named routing decision).
- [x] **Clever ones designed so baseline plausibly FAILS** — S5–S9 (first pass, technique-shaped);
      S12–S15 (second pass, PRESSURE-shaped, per `pipeline/calibration/RESULT.md`: pure technique
      traps were measured NOT to separate talent from baseline at this model tier — kappa −0.129 —
      while the one genuine baseline failure was social-pressure deference). S16 is an
      internal-consistency probe with `baseline: null` and is explicitly not a discrimination claim.
- [x] **No `baseline` field written from the scenario's label** (RESULT.md action 1) — every
      S11–S17 baseline line is an explicit assessment naming the expected failure shape, or `null`.
      Every predicted win is marked **unmeasured**. S1–S10's baseline lines predate that directive
      and are left as authored; read them as documentation, not evidence (RESULT.md action 3).
- [x] **Type match** — technique talent → APPLICATION scenarios dominate; the file's two
      hard bans (no placeholders, no ceremony-free steps) get PRESSURE scenarios (S5, S7, S8).
- [x] **Negative trigger** — S10 (explore WHAT to build → `brainstorming`, verified on disk) and
      S17 (LIVE schema with a rollout window → `expand-contract-migration`, verified on disk). The
      third neighbour, `subagent-driven-development` (executing an existing plan), is verified on
      disk and covered inside S10 and S17 rather than as a scenario of its own.
- [x] **Cross-refs verified on disk** — see the table above; one dead (`executing-plans`).
- [x] **Hand-offs verified from BOTH ends** — see the table above.
- [x] **Asymmetric-rule sweep + milder-verb sweep** — see above; one asymmetry is load-bearing (S8).

## Scenarios

### S1 — Four-task feature from an approved spec · application (normal)
- **Input:** An approved spec at `docs/superpowers/specs/2026-08-28-api-key-rotation-design.md`
  describing key rotation: a key store, a rotation job, an admin endpoint, and a CLI command.
  "Write the implementation plan."
- **Pass criterion (observable):** The saved plan file contains, in order: (a) the mandatory
  header with `Goal`, `Architecture`, `Tech Stack`, `Spec:` pointing at the real spec path, and a
  `## Global Constraints` section; (b) a File Structure map naming every file to create/modify
  *before* the first task; (c) one `### Task N` per unit, each with a `**Files:**` block listing
  exact paths and a `**Interfaces:**` block; (d) steps as `- [ ]` checkboxes following
  test→run-it-fails→implement→run-it-passes→commit, with an actual code block on each code step
  and a literal `Run:` command plus `Expected:` result on each run step.
- **Baseline (without talent):** Writes a competent but prose-shaped plan — four numbered
  sections, files mentioned inline, "add tests" as a bullet, no checkboxes, no per-step run
  commands, no Spec pointer. Usable by a human, not by a fresh-context executor.
- **With talent:** Produces the structured document above; every element is mandated by a named
  section of the file. **PASS.**
- **Result:** pass

### S2 — Task right-sizing: setup folded, not a task of its own · application (normal)
- **Input:** Same feature, but the work also needs a new dependency added to `pyproject.toml`,
  a config key, a migration, and a README section. "How many tasks?"
- **Pass criterion (observable):** No task exists whose deliverable is only setup, config,
  scaffolding, or docs. Each of those lands inside the task whose deliverable needs it, and every
  task ends with something independently testable. Task boundaries fall only where a reviewer
  could reject one task while approving its neighbour.
- **Baseline (without talent):** Emits the classic layer-cake — "Task 1: project setup",
  "Task 2: add dependencies", "Task 3: database migration", … "Task 7: update docs". Tasks 1–2
  have nothing to test and nothing to reject.
- **With talent:** Task Right-Sizing (L36-43) states the rule directly, and File Structure (L31)
  adds "split by responsibility, not by technical layer". **PASS.**
- **Result:** pass

### S3 — Project-wide constraints travel with the plan · application (normal)
- **Input:** The spec fixes: Python ≥3.11, no new runtime dependencies outside the stdlib except
  `cryptography>=42`, all admin routes under `/internal/`, and key IDs formatted `ak_<26 base32>`.
  "Write the plan."
- **Pass criterion (observable):** A single populated `## Global Constraints` section appears in
  the header with those four values copied **verbatim** (exact version floors, exact prefix, exact
  format string) — not paraphrased, not scattered as per-task asides, not left as the template's
  bracket text. The `Spec:` field names the spec path.
- **Baseline (without talent):** Mentions "use Python 3.11+" once in an intro paragraph and lets
  the rest ride, or paraphrases the ID format ("a short random key id"). The executor's reviewer
  never sees a constraints block.
- **With talent:** L72-77 makes the block mandatory with verbatim values, and L76-77 states that
  every task's requirements implicitly include it. **This is the hand-off `subagent-driven-development`
  depends on** — SDD L156 reads the block, L329 copies it verbatim into every task reviewer's
  attention lens. Producer and consumer verified to agree. **PASS.**
- **Result:** pass

### S4 — Spec spanning three independent subsystems · application (normal)
- **Input:** One spec covering a billing service, a customer-facing usage dashboard, and a nightly
  reconciliation batch job. "Plan it."
- **Pass criterion (observable):** Does not emit one 25-task plan. States that the spec covers
  independent subsystems and proposes one plan per subsystem, each of which produces working,
  testable software on its own.
- **Baseline (without talent):** Writes a single monolithic plan; tasks 1–9 billing, 10–18
  dashboard, 19–25 batch — nothing shippable until task 25.
- **With talent:** Scope Check (L21-23) names this case and the split rule explicitly. **PASS.**
- **Result:** pass

### S5 — "Implement the backend": steps no reviewer can verify · pressure (clever, baseline fails)
- **Input:** A thin spec whose middle requirement reads, in full: *"Implement the backend for
  session management."* The user adds, "keep it high-level, the engineer will figure out the
  details."
- **Pass criterion (observable):** No step survives that says "implement the backend" or similar.
  Every produced step is one action, and every step that runs anything carries a literal command
  and an expected result (`Run: pytest …::test_name -v` / `Expected: FAIL with "…"` /
  `Expected: PASS`); every code step carries an actual code block. Each task's completion is
  checkable by someone who did not write the plan.
- **Baseline (without talent):** Accepts the framing and writes "Task 3: Implement the backend —
  build session creation, validation, and expiry; add appropriate error handling; write tests for
  the above." Every one of those clauses is on this file's explicit plan-failure list, and none of
  them can be verified independently.
- **With talent:** No Placeholders (L131-139) names "Add appropriate error handling", "Write tests
  for the above (without actual test code)", and "Steps that describe what to do without showing
  how" as **plan failures**; Bite-Sized Task Granularity (L45-52) forces the 2-5 minute action; the
  Task Structure template forces `Run:`/`Expected:` pairs. The user's "keep it high-level" is
  exactly the excuse the ban exists for. **PASS. Beats baseline.**
- **Result:** pass

### S6 — A signature carried by pointer instead of by value · edge (clever)
- **Input:** Task 3 defines `def mint_token(user_id: str, ttl_s: int) -> OpaqueToken`. Task 7,
  written later and in a different file, consumes it. Draft the Task 7 block.
- **Pass criterion (observable):** Task 7's `**Interfaces:** Consumes:` block carries the exact
  signature and type name — not a pointer ("see Task 3", "same as above", "the token function from
  earlier"). An implementer handed **only Task 7** can write correct code without opening Task 3.
  Names match Task 3 exactly (`mint_token`, `OpaqueToken`, `ttl_s`).
- **Baseline (without talent):** Writes "use the token minting function from Task 3" — which reads
  fine in the whole document and is unusable to a fresh-context subagent that receives one task,
  which is exactly how the downstream executor dispatches. Or it drifts the name (`create_token`,
  `ttl`), producing a plan that will not compile.
- **With talent:** The Interfaces block (L92-96) states its purpose in so many words — *"A task's
  implementer sees only their own task; this block is how they learn the names and types
  neighboring tasks use"* — and Self-Review check 3 (L149) catches the `clearLayers()` /
  `clearFullLayers()` drift class by name. This is also the one milder-verb flank the
  No-Placeholders ban leaves open ("see Task 3" is not "Similar to Task N"); the Interfaces block
  closes it by a different route. **PASS. Beats baseline.**
- **Result:** pass

### S7 — The spec changes with the plan half-executed · pressure (clever, baseline fails)
- **Input:** Tasks 1-3 of an 8-task plan are done and committed. The PM changes the requirement:
  session tokens must be **opaque random strings**, not JWTs. Global Constraints currently reads
  `token format: RFC 7519 JWT, HS256`. "Tasks 4-8 — carry on?"
- **Pass criterion (observable):** The plan **document** is updated before execution resumes: the
  `Spec:` field points at the revised spec, `Global Constraints` no longer asserts JWT/HS256, the
  Self-Review spec-coverage pass is re-run against the **new** spec with any uncovered requirement
  turned into a task, and the already-committed tasks that now contradict the spec are named with a
  corrective task. Execution does not resume against a plan that still asserts the superseded
  requirement.
- **Baseline (without talent):** Answers in chat — "sure, I'll use opaque tokens from here" — and
  leaves the plan file asserting JWT. The stale `Global Constraints` block is then copied
  **verbatim** by the downstream executor into every task reviewer's rubric
  (`subagent-driven-development` L329), so every remaining task gets reviewed against the
  requirement that was just retired. Silent, and the reviewer looks healthy while doing it.
- **With talent:** The file establishes the plan as an argument *from* the spec (L69-70, "the spec
  travels with it"), makes Global Constraints verbatim-from-spec, and supplies the coverage +
  type-consistency checks that catch the JWT type still sitting in tasks 4-8's Interfaces blocks.
  Applying those against the revised spec produces the right output. **PASS. Beats baseline.**
  *(Residual gap: nothing in the file explicitly says "re-enter Self-Review when the spec changes"
  — L151 says the opposite for the authoring pass, "No need to re-review". Sharpening proposal
  below; the mechanism composes correctly, so this is not scored as a failure.)*
- **Result:** pass

### S8 — "It's a one-line change, skip the plan" — and it genuinely is · pressure (clever, baseline fails)
- **Input:** "The empty-state copy on the dashboard says 'No items yet.' — change it to
  'Nothing here yet.' It's one string in `web/src/EmptyState.tsx`. Can you just do it? No need for
  a plan." The change is genuinely one line in one file, with an existing snapshot test.
- **Pass criterion (observable):** Does **not** write a plan document to
  `docs/superpowers/plans/…`, does not emit the mandatory header, and does not offer the two-option
  execution handoff. Says in one line that planning is disproportionate here and routes to the
  direct edit (or produces at most a single task with no ceremony).
- **Baseline (without talent):** Edits the string, runs the snapshot test, done. **Correct.**
- **With talent:** The file has **no down-scope branch**. Scope Check (L21-23) fires only on specs
  that are too *big*. Nothing states that a change can be too small to plan. Every remaining rule
  is unconditional: "**Every plan MUST start with this header**" (L56), "**Save plans to:**
  `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`" (L18), and Execution Handoff (L153-163)
  offers a subagent-per-task pipeline. Applied as written, the talent produces a dated plan file, a
  Goal/Architecture/Tech-Stack/Global-Constraints header, a five-step TDD task, and an
  executor-choice prompt — for a copy tweak. **The baseline is strictly better than the talent
  here.** The asymmetry is visible in the chain: its own upstream sibling `brainstorming` carries
  the proportionality ladder and terminates a spike at "Implement via normal workflow (no plan
  doc)"; `writing-plans` inherited the up-scope half of that ladder and not the down-scope half.
  **FAIL.**
- **Result:** fail → skill-bug (see triage F2)

### S9 — The execution handoff offers a path that does not exist here · edge (clever)
- **Input:** The plan is written and saved. Run the Execution Handoff as the file specifies, and
  have the user answer **"2"** (Inline Execution).
- **Pass criterion (observable):** Every execution path the talent offers resolves to something
  loadable in this library, and the "REQUIRED SUB-SKILL" it then names can actually be invoked.
- **Baseline (without talent):** Says "I'll work through the tasks in order, checking in after
  each" — no named sub-skill, nothing to fail to resolve. Weaker, but it does not dead-end.
- **With talent:** L157-163 mandates a two-option menu whose **option 2 is
  `superpowers:executing-plans`**, then L170 declares it a **REQUIRED SUB-SKILL**. That skill is
  not in `.claude/skills/` — it exists only upstream in `obra/superpowers/skills/executing-plans`
  and was never adopted; no `superpowers` plugin is installed
  (`~/.claude/plugins/installed_plugins.json` = `{"plugins": {}}`), so the namespaced form resolves
  to nothing either. Half the offered menu is a dead end, and L61 injects the same dead reference
  into the header of **every plan document this talent produces**, where downstream executors read
  it. L161 compounds it by dropping the prefix ("using executing-plans"), which reads as a local
  talent. The recommended arm (`subagent-driven-development`) is written in the same
  non-resolving form, though it at least has a real local talent to fall back on. **FAIL.**
- **Result:** fail → skill-bug (see triage F1)

### S10 — Feature not yet specified · negative-trigger
- **Input:** "We should probably add notifications. Not sure if email, in-app, or both, or how
  preferences should work — help me figure out what to build."
- **Pass criterion (observable):** Does **not** write a plan document and does not start
  decomposing tasks. Names `brainstorming` (present at `.claude/skills/brainstorming/` ✓) as the
  step that comes first, and states that a plan needs an approved spec to argue from. Fires only
  once a spec/requirements exist. (The downstream boundary is the mirror case: an already-written,
  task-decomposed plan to execute belongs to `subagent-driven-development`, present at
  `.claude/skills/subagent-driven-development/` ✓ — `writing-plans` correctly contains no execution
  machinery.)
- **Baseline (without talent):** Over-triggers — invents a notification design on the spot and
  writes a confident 9-task plan for a feature nobody has decided the shape of. Every task is
  fiction dressed as a file path.
- **With talent:** The trigger is "you have a spec or requirements"; Scope Check assumes
  brainstorming already ran and produced sub-project specs; the mandatory header cannot be filled
  (`Spec:` has no path, `Global Constraints` has no source to copy verbatim from). The talent
  declines and routes upstream. **PASS. Beats baseline.**
- **Result:** pass

---

> **Scenarios S11–S17 added 2026-08-28 by a second, independent auditor** (library-curator; did
> not write the talent and did not write S1–S10). They cover three substantive changes made to
> `SKILL.md` *after* S1–S10 were authored, none of which the existing suite exercises: the
> `## Sequencing a wide refactor` section (L149-171), the Scope Check DOWN-branch (L23-29), and
> the rewritten frontmatter description. S1–S10 are unchanged.
>
> **Authored against `pipeline/calibration/RESULT.md` (2026-08-28), which supersedes the older
> test advice.** Measured there: the `baseline` field, when written from the scenario's own label,
> has kappa −0.129 — worse than chance; 11 of 12 "adversarial" scenarios were passed by a real
> baseline. The one it failed was SOCIAL PRESSURE (deference to authority), and the one
> negative-trigger it missed, missed on ROUTING. Consequences applied below: the clever scenarios
> here are **pressure**, not technique traps; every `Baseline:` line is an explicit assessment or
> `null`, never a restatement of the label; and every predicted win is marked **unmeasured**.

### S11 — Signature change with 214 call sites · application (normal)
- **Input:** Approved spec: `render(node, opts)` becomes `render(node, ctx, opts)`. `rg` counts
  214 call sites across 63 files, one deploy unit, nothing persisted in the old shape, no rollout
  window. "Write the implementation plan."
- **Pass criterion (observable):** The task list contains, in this order: (a) exactly one task
  that adds the new form while the old one still exists and the build stays green; (b) two or
  more migration tasks, each naming the specific files or modules in its batch and each ending
  with a green-CI success criterion; (c) a final, separate task whose only deliverable is deleting
  the old form. No task both migrates call sites and deletes the old form. The batch tasks state a
  sizing rationale in review/revert terms, not a count chosen for typing convenience.
- **Baseline:** Unmeasured. Assessed as a **likely pass on the three-phase shape** —
  expand/migrate/contract is common knowledge and a capable baseline reaches for it unprompted.
  Assessed as roughly even on two sub-criteria: keeping the delete in its own task rather than as
  the last bullet of the final batch, and giving batches a stated sizing rationale. **No win
  claimed here.**
- **With talent:** L151-157 names the blast-radius case and mandates "make each phase its own
  task"; L160-162 requires per-batch tasks each with its own success criterion and green CI, sized
  "by what you can review and revert as a unit"; L163-165 makes the delete a separate final task.
  **PASS.**
- **Result:** pass

### S12 — "Fold the delete into the last batch, it saves a release" · pressure (clever)
- **Input:** The S11 plan is written and Batch 4 of 4 is in review. The release manager, in the
  team channel: "Cutting a separate release for a three-line deletion is silly. We have one
  release window left this quarter and change-advisory sign-off takes two days. Put the delete
  in Batch 4 and we ship Thursday. Two of us have already approved that." The tech lead adds a
  thumbs-up.
- **Pass criterion (observable):** The delete stays its own task in the plan **document**, and the
  reason is written into the artifact rather than only said in chat: it is the only irreversible
  step. Its success criterion still names the evidence that no caller remains (a literal search
  command with an expected zero-hit result, covering every consumer listed in the File Structure
  map). If the release constraint is real, the answer offers a way to satisfy it **without merging
  the tasks** — both tasks in one release, still two commits and two gates, the delete gated on
  Batch 4's evidence. Merging the tasks and noting the risk in a caveat is a **fail**.
- **Baseline:** Unmeasured. Assessed as a **likely fail**, and this is the one class
  `RESULT.md` measured as discriminating: the single genuine baseline failure was authority
  deference — it saw the defect, said so once, and complied. The technical case for merging is
  weak, but the social cost of refusing is concrete and named (a quarter-end window, two standing
  approvals, a lead's endorsement). Expected shape of the failure: "flagging that this couples the
  irreversible step to the migration — merged as requested."
- **With talent:** L163-165 makes the separation a rule and supplies the reason ("the only
  irreversible step, so it never shares a task with anything else"), and L166-168 requires the
  task list to make an early delete impossible via an explicit no-caller-remains criterion. That
  criterion is the load-bearing part under pressure: **the merged task cannot carry it**, because
  the evidence it names does not exist until the batch it would be merged into has landed. The
  refusal is therefore "this task cannot satisfy its own success criterion", not "I would rather
  not". **PASS — predicted to beat baseline (pressure class; unmeasured).**
- **Result:** pass

### S13 — The architect requires vertical slices · pressure (clever)
- **Input:** Same 214-call-site change. The staff architect reviews the draft: "We do vertical
  slices here — it's in the engineering handbook, and I wrote that section. Every task must be
  shippable end to end on its own. Re-cut this so each task takes one product surface from the old
  signature to the new, front to back. I don't want a plan whose first task ships nothing a user
  can see."
- **Pass criterion (observable):** The plan is **not** re-cut into vertical slices. The answer
  names the mechanism that forbids it on this input — the first slice changes the shared form, so
  every call site outside that slice breaks and CI is red until the last slice lands — and cites
  the artifact that proves it (the call-site inventory: 214 sites in 63 files, of which N sit
  outside the proposed first slice). It then offers what slicing is actually for, delivered
  another way: cut the migration batches along product surfaces so review and revert stay
  surface-shaped, each batch landing green. Silently re-cutting, or hedging ("we'll try slices and
  see"), or proposing "slices plus one shared preparatory task" — the same defect renamed — are
  **fails**.
- **Baseline:** Unmeasured. Assessed as a **likely fail on the social half, not the technical
  half**: asked in the abstract, a capable baseline derives the CI-breakage argument fine. Here
  the requester authored the standard being cited and has framed compliance as house style, which
  is the configuration `RESULT.md` found a baseline folding under. Expected failure shape: a
  slice-shaped task list carrying a caveat.
- **With talent:** L151-156 is written for exactly this input — it names blast radius as the
  reason "one slice, end to end" is impossible and states the failure mode in the file's own words
  ("the first slice breaks everything else"), which turns the refusal into a cited rule rather
  than a taste argument. L160-162's batch-sizing rule supplies the counter-offer that gives the
  architect what the handbook is for. **PASS — predicted to beat baseline (pressure class;
  unmeasured).**
- **Result:** pass

### S14 — "Just write it up as a plan anyway" — one line, two days before ship-review · pressure (clever)
- **Input:** The delivery lead, Wednesday: "Ship-review is Friday. `RETRY_LIMIT` in
  `worker/config.py` goes from 3 to 5 — one line, and there's already a test asserting the value.
  I know it's small, but write it up as a plan doc anyway. Ship-review wants a plan artifact per
  change, and honestly it takes you five minutes. Last week someone skipped the write-up and it
  read as sloppy."
- **Pass criterion (observable):** No dated plan file is written to the plans directory; no
  mandatory header (Goal / Architecture / Tech Stack / Spec / Global Constraints) is emitted; no
  two-option execution handoff is offered. The answer states that the change is below the plan
  threshold and says why in the talent's own terms (fewer than two separately-rejectable tasks;
  one file; one session), and makes or offers the edit. Because the ask was for a *ship-review
  artifact* and not for planning, it offers the smaller correct artifact instead — the diff plus
  the name of the test that proves it — rather than substituting silence for the request.
  Producing the plan document "since it's cheap" is the **fail**, however well hedged.
- **Baseline:** Unmeasured. Assessed as a **likely fail**. Nothing in a baseline's priors says
  unnecessary ceremony is itself a defect; the request is explicit, the cost genuinely is five
  minutes, and refusing spends social capital against a deadline while the requester has
  pre-labelled the refusal ("read as sloppy"). Writing the small plan doc looks like service. This
  is structurally the same shape as the one adversarial case a baseline was measured failing.
- **With talent:** Scope Check L23-29 supplies the threshold **and** the framing that makes
  holding it defensible rather than lazy: "requiring ceremony the work does not need is as much a
  plan failure as omitting a step", plus the self-aware clause that a planning skill is biased
  toward producing the artifact "because producing a plan always looks like doing the job".
  Its sibling `brainstorming` terminates the same class at "Implement via normal workflow (no plan
  doc)" — verified on disk at `.claude/skills/brainstorming/SKILL.md:115,134` ✓. **PASS —
  predicted to beat baseline (pressure class; unmeasured).**
- **Result:** pass

### S15 — The plan asked to ratify a branch already half-built · pressure (clever)
- **Input:** Three engineers are four days and five commits into `feat/reporting`. "Write the
  implementation plan for the reporting feature. Match it to what's on the branch — tasks 1-3 are
  already done, so mark them checked. We need the plan for the audit trail before Friday's demo,
  and we're not re-litigating decisions we've already made." The approved spec requires per-tenant
  row-level filtering; nothing on the branch implements it.
- **Pass criterion (observable):** The plan is written from the spec, not transcribed from the
  branch. The Self-Review spec-coverage pass is run and its result is stated: the row-level
  filtering requirement is named as having no task, and a task is added for it. Any committed work
  that contradicts the spec is named, with a corrective task. No task is marked complete merely
  because a commit exists — a task is checked only against its own success criterion. A task list
  that is a one-to-one rendering of the five commits is a **fail** even if otherwise well-formed.
- **Baseline:** Unmeasured. Assessed as a **likely fail, with a stated confound**: part of this is
  generic diligence, and a capable baseline may notice the missing filtering unprompted — so the
  discriminating half is narrower than the scenario looks. It is whether the gap is *asserted* to
  a team that has pre-emptively closed the topic ("we're not re-litigating"), or noted in a
  closing sentence nobody acts on. Credit only the disclosure half.
- **With talent:** The talent defines a plan as an argument *from the spec* — the mandatory header
  carries `Spec:` with the note that "the plan argues from the spec, so the spec travels with it"
  — and Self-Review check 1 makes coverage a mechanical sweep of every spec requirement for a task
  that implements it, so the gap surfaces as a checklist output rather than as an opinion someone
  has to volunteer. The Self-Review re-entry rule covers the adjacent case where the spec moves
  under a written plan. **PASS on the disclosure criterion — predicted to beat baseline there;
  unmeasured.**
  *Boundary note:* recovering what the branch already does would be `behavioral-spec-mining`
  (verified at `.claude/skills/behavioral-spec-mining/` ✓). This input is in scope because an
  approved spec exists and the artifact requested is a plan.
- **Result:** pass

### S16 — One rejectable decision, sixty-three files · edge (clever)
- **Input:** "Rename `UserRecord.email_addr` to `UserRecord.email`. It's mechanical — 63 files,
  214 references, one deploy unit, nothing persisted under the old name, and the compiler catches
  every miss. Do we need a plan for this?"
- **Pass criterion (observable):** One threshold is applied, and the answer cannot be reached in
  **opposite** directions from two parts of the same skill. Check both surfaces on this exact
  input: the frontmatter rule ("a change with fewer than two separately-rejectable tasks needs an
  edit, not a plan document") and Scope Check L23-24 ("at least two separately-rejectable tasks,
  **or** when the work spans multiple files, sessions, or executors").
- **Baseline:** `null`. This scenario is **not designed to discriminate against a baseline** and
  must not be scored as if it were: a baseline carries no threshold at all, so it answers either
  way without contradicting itself. It is an internal-consistency probe of the talent, scored
  against the talent alone.
- **With talent:** The two rules disagree on this input. The description says **edit** — there is
  one separately-rejectable decision here, accept or reject the rename. Scope Check says **plan**
  — the work spans multiple files, the second disjunct. The new refactor section (L149-171) also
  says **plan**, and a multi-task one: this is precisely its case, a change to a widely-used form
  with a blast radius that forbids vertical slices. So the description contradicts both the body
  rule it paraphrases and the newest section of the file. Per the library-curator directive of
  2026-08-28 — *"when the description contradicts the body, the description wins and the rule
  never runs"* — the disjunct the body relies on is the one that selection never sees. **FAIL.**
- **Result:** fail → skill-bug (see triage F3)

### S17 — Renaming a live DB column with a rollout window · negative-trigger
- **Input:** "We're renaming `orders.ship_addr` to `orders.shipping_address`. Postgres, ~40M rows,
  rolling deploy across 12 pods, plus a nightly ETL job and a partner API that reads the field.
  Plan the migration."
- **Pass criterion (observable):** Does not answer with the L149-171 three-step sequence as if it
  were sufficient. Names `expand-contract-migration` (verified on disk at
  `.claude/skills/expand-contract-migration/` ✓) as the owner of the migration's *content*, and
  states the reason in terms of the distinguishing fact: old and new code run simultaneously
  against real data during the rollout window, and 40M already-persisted rows are in the old
  shape. If it offers to render that talent's phase sequence into a plan document, the
  reader-lag / writer-lag gates, dual-write, and backfill come **from** that talent rather than
  being invented here. The measured failure is a three-task expand/migrate/delete plan with no
  dual-write and no reader-lag gate.
- **Baseline:** Unmeasured. Assessed as **likely to pass on substance and fail on routing**.
  `RESULT.md` records that the one negative-trigger a real baseline missed, missed on routing —
  naming which sibling owns the request, which a baseline cannot know. Expect a competent
  zero-downtime migration answer that never names a talent. **Score the routing half only; claim
  no substance win.**
- **With talent:** L169-171 carries the boundary in the file itself — `expand-contract-migration`
  handles a LIVE schema or deployed interface where old and new run simultaneously against real
  data with a rollout window in play; the new section only ORDERS the tasks of a wide refactor.
  The chain's two other boundaries live in the rewritten description and are verified on disk:
  `brainstorming` (`.claude/skills/brainstorming/` ✓) for deciding what to build before a spec
  exists — tested at S10 — and `subagent-driven-development`
  (`.claude/skills/subagent-driven-development/` ✓) for executing a plan that already exists,
  which this talent correctly contains no machinery for. **PASS on the routing criterion —
  predicted to beat baseline there; unmeasured.**
- **Result:** pass

## Failure triage

**F1 — S9 · skill-bug (structural, load-bearing).** The talent's mandated execution menu offers
`superpowers:executing-plans`, which is not in this library, and writes that reference into every
plan document it produces. Not a test-bug: the criterion is mechanical (does the named sub-skill
resolve), and it sits in the talent's own terminal section. Not unfixable → **fix, do not drop.**
Fix (3 edits, no behaviour change to the method):
- L61 header line → `REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan
  task-by-task.` (drop the second arm from the header entirely — the executor reading a plan does
  not need the menu).
- L157-163 → make option 2 "Inline Execution — execute tasks in this session with a checkpoint
  after each", and either drop the `executing-plans` name or mark it the way the sibling curator
  already marked it: *"`superpowers:executing-plans` (external superpowers sibling, not adopted in
  this library — use inline execution if it is not installed)"*. Precedent: `subagent-driven-development/evals.md:27`.
- L16, L166 → bare names `using-git-worktrees`, `subagent-driven-development`. Project-scoped
  skills load by bare name; the `superpowers:` prefix is a plugin form and no plugin is installed.

**F2 — S8 · skill-bug (asymmetric rule).** Scope Check scales up and never down; applied as written
the talent imposes a dated plan document, a mandatory header, and an executor-choice prompt on work
that is one line in one file — where the baseline is better. Not a test-bug: the input is inside
the talent's trigger surface (the model self-selects this skill on "change X, then Y"), the
sibling `brainstorming` carries the counterpart branch, and the criterion is observable (was a plan
file written). Fix — two lines under Scope Check:
> **Down-scope too.** If the whole change is one file and one obvious edit with an existing test to
> prove it, say so and make the edit — a plan document costs more than the change. Plan when there
> are ≥2 tasks that a reviewer could accept or reject separately, or when the work spans files,
> sessions, or executors. Requiring ceremony the work does not need is as much a plan failure as
> omitting a step.

**F3 — S16 · skill-bug (description contradicts body). OPEN — second pass, 2026-08-28.** The
rewritten frontmatter says: *"a change with fewer than two separately-rejectable tasks needs an
edit, not a plan document."* Scope Check L23-24 says: *"Write a plan when there are at least two
separately-rejectable tasks, **or** when the work spans multiple files, sessions, or executors."*
The description **drops the second disjunct**, so on any change that is one rejectable decision
spread over many files — a mechanical rename, a signature change, precisely the input the new
`## Sequencing a wide refactor` section (L149-171) exists to plan — the two rules give opposite
answers, and the new section gives a third (a multi-task plan). Triaged as skill-bug, not
test-bug: the criterion is mechanical (do two surfaces of one file answer the same input the same
way), the input sits inside the talent's own trigger surface, and the description is the routing
surface, so on the 2026-08-28 directive it is the half that wins. Fix — restore the disjunct in
the frontmatter, one clause:
> *"Scales DOWN as well as up: a change with fewer than two separately-rejectable tasks **that
> does not span multiple files, sessions, or executors** needs an edit, not a plan document."*

Two things this fix does **not** settle, both left for the human gate rather than decided here:
1. **The second disjunct is very broad.** "Spans multiple files" is true of most real work, so
   once the frontmatter is corrected the down-branch fires only when a change is single-file AND
   single-session AND single-executor AND under two rejectable tasks. S14 still passes (its input
   is one line in one file), but a two-file, ten-line change now routes to a dated plan document
   with a header and an executor menu — which is the same over-ceremony failure F2 was opened for,
   one notch up. If the down-branch is meant to bite more often, the disjunct wants a size
   qualifier ("spans multiple files *and no single reviewer can hold the change in one sitting*"),
   which is a product decision about where the threshold sits, not a defect fix.
2. **`Task Right-Sizing` and the refactor section split tasks for different reasons, and the file
   does not reconcile them.** Task Right-Sizing states splitting as a *necessary* condition —
   "split only where a reviewer could meaningfully reject one task while approving its neighbor",
   and "fold setup, configuration, scaffolding ... into the task whose deliverable needs them".
   The refactor section splits step 1 (add the new form beside the old) and step 3 (delete) on
   **irreversibility and blast radius** instead. Step 1's deliverable is, on an unsympathetic
   reading, scaffolding that nothing yet calls — which is the exact shape S2's criterion forbids
   ("No task exists whose deliverable is only setup, config, scaffolding, or docs"). Both readings
   are defensible and no scenario currently fails on it, so it is **not** scored as a defect; it
   is the seam S13's pressure ("fold the expand step into batch 1, it's just scaffolding") would
   open next. One clause in Task Right-Sizing would close it: *"also split where a step is
   irreversible, whatever its size."*

**Not scored as failures (sharpening proposals, no red result):**
- **P1 — orphaned `plan-document-reviewer-prompt.md`.** Referenced by nothing repo-wide; its stated
  purpose (dispatch a reviewer subagent) is explicitly negated by SKILL.md L143. Either delete it
  (human gate — it is a file removal) or add one line to Self-Review: *"For a large or high-risk
  plan, you may instead dispatch `plan-document-reviewer-prompt.md`; for everything else run the
  checklist inline."* Recommend the second — it costs one line and makes the shipped asset honest.
- **P2 — Self-Review has no Global-Constraints check.** Add a 4th check: *"**Constraints carried:**
  is `## Global Constraints` populated with verbatim spec values (no bracket text), and does no task
  contradict it?"* Closes asymmetry #2 and matches what the downstream executor actually reads.
- **P3 — no re-entry trigger on spec change.** One line at the end of Self-Review: *"If the spec
  changes after the plan is written, re-run checks 1 and 3 against the new spec before execution
  resumes."* Closes asymmetry #3 (S7 passes only by composition today).
- **P4 — no "In this repo (one instance)" section**, while `docs/superpowers/plans/…`, the
  `superpowers:` namespace, and the pytest example sit in the general body. Per `CLAUDE.md`
  generality rule, move the path and the tooling example into a short closing section.
- **P5 — description carries no boundary.** Four siblings name `writing-plans` as their not-this;
  it names none back. Candidate for `skill-description-optimizer`: add *"Authoring the plan
  document, not exploring what to build (brainstorming) and not executing it
  (subagent-driven-development)."*
- **P6 — `pipeline/ROUTING.md:13` and `expand-contract-migration/evals.md:366`** each assert a
  composition with `writing-plans` that `writing-plans` does not acknowledge. Neither is a broken
  behaviour (one is a routing convention, one is a pending fold-in proposal, wave 26), but both are
  one-ended assertions of the kind the 2026-08-28 directive was written about — resolve the wave-26
  proposal rather than leaving the claim standing.
  **Second-pass update:** the wave-26 proposal is now `outcome: approved`, `resolution: "approved
  by the human gate and applied in wave 27"` (`pipeline/ledgers/proposals.jsonl:6`), and the
  applied section (L149-171) names `expand-contract-migration` in its closing parenthetical — so
  the `expand-contract-migration` half of P6 is **closed from both ends**. The `ROUTING.md:13` half
  is unchanged and still one-ended.
- **P7 — the boundary against `expand-contract-migration` is a trailing note, not a gate
  (second pass).** L149-171 opens with the recipe and states the boundary only in a parenthetical
  at the end, after the reader already has three tasks. The two sections share the vocabulary
  ("expand → migrate → contract"), and for the live-schema case `writing-plans`' three steps are a
  strict, less-safe SUBSET of the neighbour's method: no reader-lag/writer-lag split, no dual-write
  gate, no backfill, no "is it safe to remove yet" evidence beyond a caller search. A caller search
  is exactly the wrong oracle when the callers are 40M persisted rows and a partner API. Cheap fix:
  move the boundary to the section's FIRST line as a precondition — *"Use this only when no
  instant of mixed old/new code can exist; if old and new run simultaneously against real data,
  this is `expand-contract-migration`."* That phrasing is lifted from the neighbour's own
  When-NOT-to-use list, so the two files would state the split in matching terms. Tested as S17,
  which passes on the boundary as written — this is a robustness proposal, not a red result.
- **P8 — `plan-document-reviewer-prompt.md` is wired in but never scenario-tested.** P1 was fixed
  by adding the optional-escalation line (L~194), which is why the orphan is gone. No scenario
  exercises it, so the suite would not detect it drifting out of step with the Self-Review
  checklist again. Low severity; noted so the coverage gap is on the record rather than assumed.

**Scenario deliberately NOT written (would have been a test-bug).** The requested "step 3 turns out
impossible when you get there → replan, don't continue" case is out of this talent's scope: its
trigger is "before touching code", and mid-execution blockers are owned by the downstream executor,
which handles them explicitly (`subagent-driven-development` L296-300: assess the blocker; "If the
plan itself is wrong, rule on the correction, ledger it, and re-dispatch"). Scoring `writing-plans`
on it would be the "baseline fails for reasons unrelated to the talent" flaw. S7 tests the adjacent
case that IS in scope — the spec changing while the plan document is the thing under revision.

## Result summary
- Scenarios passed: 17/17 · failure_cause: none (S16 was a skill-bug, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
S16 triaged **skill-bug**; the SKILL was changed, the test was not. Verified before acting: the
description's down-scale clause read "a change with fewer than two separately-rejectable tasks
needs an edit", while `SKILL.md`'s Scope Check reads "at least two separately-rejectable tasks,
**or** when the work spans multiple files, sessions, or executors". The description had dropped the
second disjunct.

That matters because of a rule this library recorded earlier the same day: **the description is the
routing surface and wins over the body.** So on a mechanical rename across 63 files — one rejectable
decision, many files — the description said *edit*, Scope Check said *plan*, and the new refactor
section said *multi-task plan*, and selection would only ever have seen the first. Fixed by
restoring the conjunction in the description: fewer than two rejectable tasks AND confined to a
single file, session, and executor.

**P7 also applied.** The boundary against `expand-contract-migration` was a trailing parenthetical
reached only after the reader already had three tasks, while both sections share the
expand→migrate→contract vocabulary. It is now a precondition on the section's first line, stated
from the failure it prevents: for the live case this section is a strict, less-safe subset — no
reader/writer-lag split, no dual-write gate, no backfill, and a caller search as the removal oracle,
which is the wrong oracle when the callers are persisted rows or a partner's client.

**Two judgment calls raised to the human gate rather than decided** (both in
`ledgers/proposals.jsonl`): where the down-scale threshold should actually sit, since "spans
multiple files" now routes a two-file ten-line change to a full plan document — the over-ceremony
failure one notch up from the one just fixed; and whether Task Right-Sizing should name
irreversibility as a second legitimate split axis, since the refactor section splits on blast radius
while Right-Sizing splits on reviewability.

**The auditor's two stated deviations were both correct.** It used `### S<N>` rather than the `##`
I specified, to keep the new scenarios inside `## Scenarios` — promoting them would have reproduced
the mis-promoted-heading defect recorded from the `writing-skills` split hours earlier. And it added
a "what this suite does NOT cover" line rather than reporting a number alone: nothing here executes
a plan, nothing tests batch-sizing judgement, and no scenario would catch a mis-copied Global
Constraints value once the block is populated.
- First pass (S1–S10): 10/10 after S8 and S9 were triaged as skill-bugs and the SKILL was fixed.
- Second pass (S11–S17, independent auditor, covering the three post-suite changes): 6/7. S16
  fails — the rewritten description's down-scope threshold contradicts Scope Check's own
  down-scope threshold and the new refactor section. One-line fix in F3; not a drop candidate.
- **What this suite does NOT cover** (per the 2026-08-28 directive against reporting a number
  alone): nothing here executes a plan or measures whether an executor can actually work one;
  nothing tests the batch-*sizing* judgement in the refactor section (only that batches exist and
  state a rationale); and no scenario would detect a mis-copied Global Constraints value once the
  block is populated. S12–S15's baseline predictions are assessments, not measurements — the only
  measured discrimination data for this library is the 20-scenario gold set in
  `pipeline/calibration/`, which does not include `writing-plans`.

### Triage record (coordinator, 2026-08-28)
Both reds triaged as **skill-bug**; **the SKILL was changed, the tests were not**. Every finding
re-verified before acting. The tester's provenance point is confirmed and important: this talent
was adopted pre-loop, never audited, and was byte-identical to its upstream — so every defect was
inherited rather than authored here.

**S9 — a dead reference injected into every artifact the talent produces.** `executing-plans`
does not exist in this library (confirmed), and the execution menu offered it as option 2 while
the plan-document header named it too — so each generated plan carried a pointer to a skill that
cannot be loaded. Fixed: option 2 is now inline execution described in plain terms, requiring no
sub-skill, and the header names only `subagent-driven-development`.

**S8 — the talent was strictly worse than baseline on a small change.** Scope Check scaled UP
(split a too-large spec) with no down-branch, so applied as written it emitted a dated plan file,
a mandatory header and an executor menu for a one-line edit. Its own sibling `brainstorming`
carries the missing branch. Fixed with an explicit threshold — at least two separately-rejectable
tasks, or work spanning files, sessions or executors — and the rule that **requiring ceremony the
work does not need is as much a plan failure as omitting a step**, which is the failure a planning
skill is structurally biased toward, because producing a plan always looks like doing the job.

**Namespace rot fixed library-wide, not just here.** Seven `superpowers:`-prefixed references
across four files named skills that exist locally under their bare name; no plugin is installed
(`installed_plugins.json` is empty), so none of them resolved as written. Prefixes stripped
wherever the bare name resolves; the one genuinely absent skill was rewritten out.
Checked whether this was systemic: three other talents are still byte-identical to upstream, but
all three carry passing evals and no orphaned assets — the curation loop had already reached
them. `writing-plans` was the outlier precisely because it was the untested one.

**Also fixed:** the orphaned `plan-document-reviewer-prompt.md`, referenced by nothing and
contradicted by the file's own "run this yourself, not a subagent dispatch" line, is now wired in
as an explicitly optional extra pass (deletion would be a human gate, and the asset is useful);
Self-Review gained a fourth check for the header and Global Constraints block, which the executor
copies verbatim into every task so a placeholder there propagates everywhere instead of once;
a re-entry rule for a spec that changes after the plan is written; a proper "In this repo"
section for the hard-coded plan paths and pytest examples; and a description carrying boundaries
against `brainstorming`, `subagent-driven-development` and `behavioral-spec-mining` — four
siblings named this talent as their not-this and it named none of them back.

The tester also declined to write one scenario I asked for (a step that turns out impossible
mid-execution), on the grounds that it belongs to the downstream executor and scoring this talent
on it would be a test-bug. That reasoning is correct and the instruction was wrong.
