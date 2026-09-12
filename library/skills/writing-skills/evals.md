# Evals — writing-skills

> Baseline-vs-with test suite for the `writing-skills` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.
> This talent AUTHORS the rest of the library, so a defect here propagates into every skill
> it writes — highest leverage in the untested backlog (used in 5 waves, previously 0 tests).

**Talent:** `writing-skills` · **Type:** technique (a skill-authoring procedure) wrapped around a
hard discipline core (the Iron Law: no skill without a failing test first) · **Last eval:** 2026-08-28 ·
**Verdict:** fix

## Method
Baseline-vs-with: for each scenario, judge the likely output of a capable agent WITHOUT the
talent's method against the output WITH it. `writing-skills` claims a concrete procedure —
RED (run pressure/baseline scenarios before writing) → GREEN (write the minimal skill: required
`name` + `description` frontmatter, "Use when…" trigger-only description, keyword coverage,
form matched to the failure type, one excellent example) → REFACTOR (rationalization table,
red-flags list, re-test) — plus gating rules on *whether* a skill should exist at all, on file
organization, and on cross-referencing. Application scenarios exercise the everyday authoring
job; clever scenarios attack the places the procedure is easiest to fake or where it is silent.
A scenario passes only if the with-talent result meets the observable criterion AND is
materially better than baseline. Two scenarios do not pass; they are triaged below rather than
rubber-stamped.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1–S4 are normal/representative (the talent's day job: author a
      skill from a stated need), S5–S8 are clever (edge + pressure), S9 is the negative trigger.
      4 normal / 4 clever / 1 negative-trigger — corrects the suite-wide 30% normal signal.
- [x] **Specific to this talent** — every scenario turns on a named section, table row, or
      checklist item of `writing-skills/SKILL.md`; no generic authoring boilerplate.
- [x] **Observable pass/fail criterion** — each names a checkable artifact or its absence
      (frontmatter fields present, description string not shipped verbatim, no `SKILL.md`
      written, prohibition count zero, baseline run recorded before the body exists).
- [x] **Clever ones designed so baseline plausibly FAILS** — S5 (a polite, reasonable request
      an untreated agent has no rule to refuse), S6 (an "already approved" description),
      S7 (a collision invisible without looking at siblings), S8 (authority + time pressure).
- [x] **Matches talent type** — technique → application scenarios dominate; the discipline core
      (Iron Law, no-batching) gets the pressure shape in S8, and S6 pressures the SDO rules.
- [x] **Covers the negative trigger** — S9 uses the two nearest look-alikes, both verified
      present in `.claude/skills/`: `skill-description-optimizer` and `skill-stocktake`.

## S1 — author a technique skill from a stated need · application (normal)
- **Input:** "Our integration tests are flaky — they `sleep` and then race the server. Write a
  skill so future agents fix this class of problem properly." Nothing else is specified.
- **Pass criterion (observable):** The deliverable is a single `<name>/SKILL.md` whose first
  lines are `---`, a `name:` using only letters/numbers/hyphens, a `description:` that begins
  "Use when", `---`. The description contains no summary of the skill's own steps (no "then
  replaces…", "walks you through…") and is under 500 characters. The body has an Overview with
  the core principle, a When-to-Use list of symptoms, a quick-reference table, and a common-
  mistakes section, with **exactly one** code example in **one** language. `wc -w SKILL.md`
  under 500. Any of: missing `name:`, a workflow-summarizing description, or the same example
  ported into a second language, is a FAIL.
- **Baseline (without talent):** Produces a genuinely useful document and will usually remember
  frontmatter — but the description lands as "Helps fix flaky tests by replacing sleeps with
  condition-based waiting", i.e. what the skill DOES, and the doc grows to 1200+ words with
  JS *and* Python variants "so it's useful to everyone". No word budget is ever checked.
- **With talent:** The `SKILL.md Structure` block supplies the exact frontmatter contract (two
  required fields, `name` charset, description third-person, "Use when…", <500 chars); SDO §1's
  ❌/✅ pairs rule out the DOES-form; SDO §4 sets the <500-word target and prescribes the
  `wc -w skills/path/SKILL.md` verification; `Code Examples` ("One excellent example beats many
  mediocre ones", "Don't: implement in 5+ languages") caps it at one. **PASS. Beats baseline.**

## S2 — author a discipline skill, RED before GREEN · application (normal)
- **Input:** "People keep marking work done without running the suite. Author a skill that
  stops it."
- **Pass criterion (observable):** Baseline scenarios are run WITHOUT the skill and their
  results recorded BEFORE any `SKILL.md` body text exists, and the finished artifact contains
  (a) 3+ combined-pressure scenarios, (b) a rationalization table whose left column holds
  excuses captured verbatim from those baseline runs, and (c) a red-flags list. Writing the
  skill body first — or inventing a rationalization table from imagination — is a FAIL.
- **Baseline (without talent):** Writes the skill immediately; it is a documentation task and
  there is no obvious reason to run experiments first. Any "common excuses" table is invented
  rather than observed, so it counters excuses agents don't actually make and misses the ones
  they do.
- **With talent:** `The Iron Law` ("NO SKILL WITHOUT A FAILING TEST FIRST") plus `RED: Write
  Failing Test (Baseline)` ("you must see what agents naturally do before writing the skill",
  document rationalizations verbatim); `Testing All Skill Types → Discipline-Enforcing Skills`
  selects pressure scenarios with combined pressures; `Bulletproofing → Build Rationalization
  Table` / `Create Red Flags List` supply (b) and (c); the `Skill Creation Checklist` orders
  RED before GREEN and instructs a todo per item. **PASS. Beats baseline.**

## S3 — heavy reference and a reusable tool · application (normal)
- **Input:** "Here are 600 lines of vendor API notes and a 40-line helper script we keep
  re-pasting. Turn it into a skill."
- **Pass criterion (observable):** The 600 lines end up in a **separate** file inside the skill
  directory and the script in its own file; `SKILL.md` keeps only overview + workflows and stays
  under the word target; the reference is linked by plain relative filename. Inlining the 600
  lines into `SKILL.md`, or linking with `@skills/...`, is a FAIL.
- **Baseline (without talent):** Produces one enormous `SKILL.md` with the API dump inlined —
  "it's all one topic" — or splits it but links with `@path` syntax, which force-loads the file
  into context on every invocation.
- **With talent:** `Directory Structure → Separate files for: 1. Heavy reference (100+ lines)
  … 2. Reusable tools`; `File Organization → Skill with Heavy Reference` gives the worked
  layout (`pptx/` with `pptxgenjs.md`, `ooxml.md`, `scripts/`); SDO §5 forbids `@` links
  explicitly with the reason ("force-loads files immediately, consuming 200k+ context").
  **PASS. Beats baseline.**

## S4 — match the form to the failure · application (normal)
- **Input:** Baseline runs are in hand and they show *compliance* with the rule but the wrong
  output shape: agents dispatching subagents restate the entire spec inside the dispatch prompt.
  Write the guidance that fixes it.
- **Pass criterion (observable):** The authored guidance is a positive recipe/contract that
  names the output's parts in order, and contains **zero** prohibition clauses about the
  unwanted content ("don't restate", "never narrate") and **zero** nuance clauses of the form
  "unless it matters". A prohibition list, or a recipe with a nuance clause appended, is a FAIL.
- **Baseline (without talent):** Reaches straight for the intuitive fix — "Never restate the
  spec; don't narrate the plan" — and softens it with "unless the subagent genuinely needs it".
  This is the documented backfire: under the competing "make the prompt self-contained"
  incentive, the prohibition arm produced *more* of the unwanted content than the recipe arm and
  trended worse than the no-guidance control.
- **With talent:** `Match the Form to the Failure` row 2 keys on the observed failure ("Complies,
  but output has the wrong shape … restated spec") and prescribes "Positive recipe or contract:
  state what the output IS — its parts, in order", naming the prohibition list as the wrong
  form; `Rules for whichever form you pick → No nuance clauses` blocks the softener; the GREEN
  checklist has the item "Guidance form matches the failure type". **PASS. Beats baseline.**

## S5 — a one-off job dressed up as a skill request · edge (clever)
- **Input:** "Write a skill documenting how we migrated staging to Postgres 16 last Tuesday —
  the ordered steps, our connection string, and the two flags we had to pass." The work is done,
  it is specific to this repo's staging box, and it will not recur.
- **Pass criterion (observable):** No `<name>/SKILL.md` is authored. The response declines and
  names the disqualifying reason (one-off / project-specific / narrative), and redirects the
  content to the project's instructions file or a runbook. Emitting a SKILL.md — especially one
  containing the connection string — is the FAIL.
- **Baseline (without talent):** Complies. The request is explicit, polite and well-formed, and
  an untreated agent has no rule authorizing a refusal; it writes a tidy narrative SKILL.md
  ("In the 2026-08-25 migration we…") with the environment specifics baked in. The library gains
  a permanently non-reusable, non-portable entry.
- **With talent:** `When to Create a Skill → Don't create for:` lists "One-off solutions" and
  "Project-specific conventions (put in your instructions file)" — two independent hits;
  `What is a Skill?` states "Skills are NOT: Narratives about how you solved a problem once";
  `Anti-Patterns → ❌ Narrative Example` names this exact shape and its reason ("Too specific,
  not reusable"). The talent declines and redirects. **PASS. Beats baseline.**

## S6 — an "already approved" description that names the topic, not the trigger · pressure (clever, baseline fails)
- **Input:** The PM hands over a finished description and says use it verbatim, it is already
  approved, don't bikeshed:
  `description: Comprehensive guide to caching strategies — covers TTLs, invalidation and
  stampede protection, then walks you through picking one for your workload.`
- **Pass criterion (observable):** The shipped frontmatter `description:` is **not** that
  string. What ships begins with "Use when", is third person, states triggering conditions or
  symptoms (e.g. repeated identical expensive calls, thundering-herd on cache expiry, stale
  reads after writes), and contains no summary of the skill's own steps ("walks you through
  picking one"). Shipping the supplied text — or a lightly reworded version that still leads
  with the topic — is the FAIL.
- **Baseline (without talent):** Ships it. The string is grammatical, informative and
  explicitly blessed by a stakeholder; there is no articulated rule that a description must be
  a trigger rather than a topic, and pushing back looks like bikeshedding on approved copy.
  This is the single most common quality defect in the library, and baseline reproduces it.
- **With talent:** SDO §1's `CRITICAL: Description = When to Use, NOT What the Skill Does`
  makes the rewrite non-negotiable and supplies the evidence to hand the PM — a
  workflow-summarizing description caused an agent to perform ONE review when the skill's
  flowchart specified two, and removing the summary fixed it; the "trap" paragraph names the
  mechanism ("the skill body becomes documentation agents skip"); `Content` repeats "Write in
  third person" and "NEVER summarize the skill's process or workflow", and the GREEN checklist
  re-checks both. **PASS. Beats baseline.**

## S7 — a new skill that collides with an existing one · edge (clever)
- **Input:** The library already ships `skill-description-optimizer` (frontmatter: "Use when a
  skill's `description` triggers wrong — it fails to auto-invoke … or it mis-fires and steals
  prompts that belong to a sibling skill"). The user says: "Author a new skill called
  `trigger-tuning` that makes skills fire on the right prompts."
- **Pass criterion (observable):** Before the new skill is written, the installed library is
  searched for a skill with overlapping triggers (e.g. a `grep -Ril` over
  `.claude/skills/*/SKILL.md` descriptions), and the deliverable is either (a) a decline plus a
  hand-off to the existing `skill-description-optimizer`, or (b) a new skill whose description
  states its boundary against that sibling. Shipping a second skill whose description claims
  the same prompts, with no boundary clause and no record of a sibling search, is the FAIL.
- **Baseline (without talent):** Authors `trigger-tuning` from a blank page. It never enumerates
  the installed library, so the collision is invisible; two skills now compete for every
  "my skill isn't triggering" prompt and the loader picks arbitrarily.
- **With talent:** **No improvement.** `SKILL.md` contains no step for this. `When to Create a
  Skill` lists exactly four don't-create conditions (one-off, standard practice, project-
  specific, mechanically enforceable) — "one already exists" is not among them. The entire SDO
  section optimizes a description **in isolation**: keyword coverage, verb-first naming,
  "Use when…" phrasing — with no instruction to compare against sibling descriptions, and the
  GREEN checklist has no dedup item. `Discovery Workflow` even describes future agents grepping
  descriptions, without drawing the conclusion that two skills must not answer the same grep.
  Nothing hands off to `skill-scout` (search-before-create) or `skill-description-optimizer`,
  both present in `.claude/skills/`. The with-talent output is a better-formatted, keyword-rich
  description that collides head-on — arguably *worse*, because richer keywords widen the
  collision. **FAIL — failure_cause: skill-bug.**

## S8 — "just write it fast, we'll fix the details later" · pressure (clever, baseline fails)
- **Input:** Ten minutes before the demo, the lead says: "We need this skill in the repo now —
  skip the frontmatter and the test scenarios, just drop the body in as a markdown note, we'll
  clean it up next week. And do the other two skills in the same pass, we're out of time."
- **Pass criterion (observable):** What lands in the repo either (a) has YAML frontmatter with
  both `name:` and `description:` and had its baseline scenarios run, or (b) is not placed in
  the skills directory at all. Any shipped `SKILL.md` missing `name:` or `description:`, or more
  than one skill created in the pass without each being tested, is a FAIL.
- **Baseline (without talent):** Complies with the deadline and the authority: a headerless
  markdown note under `skills/<name>/SKILL.md` — which does not load at all — plus the two
  batched siblings, all untested, with a sincere intent to fix it next week. This is not
  hypothetical: pass 2 of the curation loop found `learn-eval` shipped missing its `name:`.
- **With talent:** `The Iron Law` extends to edits and enumerates the exceptions as void ("Not
  for 'simple additions' … Don't keep untested changes as 'reference'"); `Common
  Rationalizations for Skipping Testing` answers this excuse by name ("No time to test" →
  "Deploying untested skill wastes more time fixing it later"; "I'll test if problems emerge");
  `STOP: Before Moving to Next Skill` forbids the batching directly ("Do NOT: Create multiple
  skills in batch without testing each … Skip testing because 'batching is more efficient'");
  the GREEN checklist makes `name` + `description` a required, non-skippable item. The talent
  ships one properly-headed, tested skill or ships nothing. **PASS. Beats baseline.**

## S9 — sharpen an existing skill's triggering / audit the library · negative-trigger
- **Input:** Two look-alike requests, neither asking for a skill to be authored or its body
  rewritten. (1) "`context-budget` isn't firing when it should and it keeps stealing prompts
  that belong to `repo-map` — fix its triggering." (2) "Go through all the installed talents
  and tell me which are stale, which overlap, and which I should retire."
- **Pass criterion (observable):** `writing-skills` claims neither request. Request (1) is
  handed to `skill-description-optimizer` and request (2) to `skill-stocktake` — both verified
  present in `.claude/skills/`. Rewriting `context-budget`'s description under this talent's own
  SDO procedure, or producing a library-wide quality audit, is the FAIL.
- **Baseline (without talent):** Not the discriminator here — an untreated agent would simply
  do both jobs by hand. The question a negative trigger asks is whether the talent
  over-triggers, and the with-talent column answers it.
- **With talent:** **No improvement — the talent fires on both.** Its own frontmatter reads
  "Use when creating new skills, **editing existing skills**, or **verifying skills work before
  deployment**": request (1) is editing an existing skill and request (2) is verifying skills,
  so both match the trigger literally. The body never scopes itself out — there is no "When NOT
  to use" block, no Related/hand-off block, and neither `skill-description-optimizer` nor
  `skill-stocktake` is named anywhere in `SKILL.md`. Worse, SDO §1 is a *complete*
  description-rewriting method, so a with-talent agent is fully equipped to take request (1)
  itself, and `Testing All Skill Types` plus the deployment checklist invite it to take (2).
  Contrast the house standard set by `skill-scout`, whose description scopes it explicitly
  ("Discovery step, not authoring, editing, or auditing skills") and whose Related block hands
  off — which is exactly why its negative-trigger scenario passes. **FAIL — failure_cause:
  skill-bug.**

## Failure triage (if any scenario failed)
Two failures, S7 and S9. Both triage to **skill-bug**, and both reduce to one root cause:
`writing-skills` authors and scopes each skill **in isolation**, with no awareness of the
library it is writing into.

Why not **test-bug** in either case:
- Both scenarios sit squarely inside what the talent's own frontmatter claims ("creating new
  skills, editing existing skills, verifying skills work"); neither invents a capability.
- Both criteria are observable by an outsider (was a sibling search run? does a second skill
  ship with an unbounded overlapping description? was the request handed off?).
- The standard applied is the library's own, already met by a sibling talent (`skill-scout`
  passes the equivalent negative trigger because its description scopes itself and its Related
  block hands off), so the bar is neither novel nor unfair to this talent alone.
- The baseline in S7 fails too — but a talent that does not beat baseline on a fair, in-scope
  criterion has not earned the scenario, and this is the talent that seeds the defect into every
  skill it writes, which is what makes it load-bearing rather than cosmetic.

Not a drop candidate: seven of nine scenarios pass decisively, several of them (S4, S5, S6, S8)
against baselines that fail in ways this library has actually observed. The fix is additive.
**Recommended (for the curator to apply — not applied here):** (i) add a dedup / search-before-
create step to the GREEN phase and the checklist, handing off to `skill-scout`, and require the
new description to state its boundary against the nearest sibling; (ii) add a "When NOT to use"
/ hand-off block naming `skill-description-optimizer` (description-only tuning) and
`skill-stocktake` (library-wide audit); (iii) sharpen this talent's own description so
"editing existing skills" does not swallow both siblings' jobs. Re-run S7 and S9 after.

Note for the curator (further defects observed while testing, not fixed here):
1. **Dead cross-references** — `SKILL.md:12` links `../using-superpowers/references/codex-tools.md`
   and `../using-superpowers/references/gemini-tools.md`; there is no `using-superpowers`
   directory in `.claude/skills/` (66 talent dirs checked). Both links are broken.
2. **Namespace drift on load-bearing references** — `test-driven-development`
   (`SKILL.md:18`, `:393`) and `systematic-debugging` (`:284`); the real talents are
   `test-driven-development` and `systematic-debugging`, with no `superpowers:` prefix anywhere
   in this library. Lines 18 and 393 are REQUIRED-BACKGROUND directives, so they resolve to
   nothing. Lines 283–284 are style examples, but they teach the bad prefix to every skill this
   talent writes — which is plausibly the origin of the namespace drift seen elsewhere.
   `testing-skills-with-subagents.md:13` carries the same broken prefix.
3. **Its own description is topic-shaped and unbounded** — the defect S6 and S9 test for
   (see the recommended fix above).
4. **Self-violation of its own token budget** — `wc -w SKILL.md` = **3730 words** against the
   "<500 words (still be concise)" target it sets for other skills in SDO §4, complete with the
   `wc -w` verification snippet. Defensible for an authoring reference, but it should either
   claim the reference exemption explicitly or move sections out to the supporting files that
   already exist beside it; as written, the skill that teaches the budget breaks it 7x.
5. **Frontmatter example seeds a non-conforming name** — the template block at `SKILL.md:105-108` (`name:` on line 107)
   shows `name: Skill-Name-With-Hyphens` (capitalized), while every talent in this library and
   this skill's own SDO §3 naming guidance use lowercase gerund/verb-first names. An authoring
   skill that seeds a capitalized name into every new skill is a portability risk.
6. **Clean on two checks:** no invented slash-commands or built-ins are referenced (the only
   command forms are `wc -w` and the real, present `./render-graphs.js`), and all four
   in-directory supporting files it names — `anthropic-best-practices.md`,
   `graphviz-conventions.dot`, `persuasion-principles.md`, `testing-skills-with-subagents.md` —
   exist. Minor: `render-graphs.js` is documented only as a bare relative invocation
   (`./render-graphs.js ../some-skill`), which works only from inside the skill directory and
   needs node + graphviz.

## Result summary
- Scenarios passed: 9/9 · failure_cause: none (S7+S9 were skill-bugs, now fixed) · verdict: passed

## Triage record — S7 and S9 (why the verdict changed)
Both first ran **FAIL**, triaged as **skill-bug**, not test-bug: both sit inside what the
frontmatter claims, both criteria are outsider-checkable, and the bar was the library's own —
already met by a sibling (`skill-scout` passes the equivalent scope test).

Root cause was one thing, and it was systemic: **`writing-skills` authored in isolation, with
zero awareness of the library it writes into.** Verified: the file contained 0 mentions of
`skill-scout`, dedup, or "already exists", and its only "When NOT to use" was inside a TEMPLATE
it teaches others to write, not a section it had itself.

**The SKILL was changed, the tests were not:**
- **S7** → added a mandatory **Step 0: search the library before authoring** (run `skill-scout`
  over project + user + marketplace scopes with synonyms; then use / extend / differentiate on
  TRIGGER; "I found nothing" counts only if you can say where you looked).
- **S9** → its description was topic-shaped and unbounded ("creating new skills, editing
  existing skills, or verifying skills work"), which literally claimed two siblings' jobs.
  Rewritten trigger-shaped with explicit NOT-clauses routing to `skill-description-optimizer`,
  `skill-stocktake`, `skill-scout`, and `eval-harness`.

Also fixed from the same audit: 4 `superpowers:`-prefixed refs that resolve to nothing (and were
taught as ✅ examples, making this talent a plausible ORIGIN of namespace drift elsewhere in the
library); a dead `../using-superpowers/references/` link; and a frontmatter example seeding a
capitalized `Skill-Name-With-Hyphens` into every skill authored from it.

**Still open — raised to the human gate, not fixed:** the talent is 3730 words against the
"<500 words" budget it sets for others, complete with the `wc -w` check it never runs on itself.
Cutting it is a restructure, not a repair.
