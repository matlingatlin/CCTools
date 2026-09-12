# Evals — skill-scout

> Baseline-vs-with test suite for the `skill-scout` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in
> `pipeline/CURATION-LESSONS.md`.

**Talent:** `skill-scout` · **Type:** technique (search procedure with one discipline guard:
search-before-create) · **Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely behavior of a capable agent WITHOUT
the talent's method vs WITH it. `skill-scout` is a six-step **technique** — (1) capture
intent into 3–5 keywords **plus synonyms**, (2) search local sources by name **and** by
frontmatter description, (3) search GitHub/web with bounded queries, (4) **vet** external
matches before recommending, (5) rank and cap at 10, (6) present the Use / Fork / Create
decision table and only then create — wrapped in one discipline guard: do not jump to
creation when a search is reasonable. Application scenarios exercise the everyday run of
those steps; clever scenarios attack the two places the procedure is easy to fake — treating
a *name* match as a *function* match, and declaring "nothing exists" from literal keywords
alone. A scenario passes only if the with-talent result meets the observable criterion and
the baseline is materially weaker.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1–S3 are normal/representative (the everyday discovery job),
      S4–S6 are clever (pressure + edge), S7 is the negative trigger. 3 normal / 3 clever / 1 negative.
- [x] **Specific to this talent** — every scenario turns on a named step or anti-pattern in
      `skill-scout`'s SKILL.md; nothing is generic search boilerplate.
- [x] **Observable pass/fail criterion** — each states a checkable artifact or absence
      (synonym list present, description-level search run, Gap column filled, no file written,
      sources-searched record present, no decision table emitted).
- [x] **Clever ones designed so baseline plausibly FAILS** — S4 (exact-name collision that is
      not a functional match), S5 (target skill shares no literal keyword), S6 (true negative
      that must be evidenced, not asserted or padded).
- [x] **Matches talent type** — technique → application scenarios dominate; the one discipline
      invariant (search before create) gets the pressure scenario shape in S2/S4.
- [x] **Covers a negative trigger** — S7 (audit the installed library for overlap and rot) is
      `skill-stocktake` territory; `skill-scout` must not fire.

## Scenarios

### S1 — "is there already a skill for this?" · application (normal)
- **Input:** User asks, with no creation request attached: "Is there already a skill that
  reviews Terraform plans for security problems before apply?" The library contains a talent
  whose *name* has nothing to do with Terraform but whose frontmatter description mentions
  "Terraform/HCL and other IaC definitions".
- **Pass criterion (observable):** The response (a) states the 3–5 keywords **and synonyms**
  it searched with (e.g. terraform, tfplan, HCL, IaC, infra-security), (b) shows both halves
  of Step 2 — the name-level `find … | grep -iE` **and** the description-level
  `grep -RilE` over skill files — (c) surfaces the description-only match, and (d) returns a
  ranked list of at most 10 rows with a **Gap** stated per row. No skill is created.
- **Baseline (without talent):** Plausibly gets the shape of the answer right — it will glob
  skill directory names for "terraform"/"iac" and report what it finds. But name-globbing
  alone never reaches frontmatter descriptions, so the description-only match is missed, and
  the answer arrives as unranked prose with no per-candidate Gap. Misses (b), (c), (d).
- **With talent:** Step 1 forces synonyms, so "IaC" and "HCL" enter the query set; Step 2's
  second command (`grep -RilE "keyword|synonym"` across skill files) catches the
  description-only match that no name search could reach; Step 5 ranks it and Step 6 renders
  the table with the Gap column shown in the Examples section. **PASS. Beats baseline.**

### S2 — "build me a skill" with a close local match · application (normal)
- **Input:** "Build me a skill that audits our GitHub Actions workflows for leaked secrets."
  The installed library already contains `code-security-review` (secret/credential scanning
  over source, not CI workflow files specifically).
- **Pass criterion (observable):** No `SKILL.md` and no skill directory is written before the
  user chooses a path. The reply contains the Step 6 three-row decision table with the exact
  options **Use existing / Fork or extend / Create fresh**, names `code-security-review` as the
  closest match, and states its Gap in one concrete clause (does not cover workflow-file
  triggers/permissions).
- **Baseline (without talent):** Reads "build me a skill" as an instruction and begins
  authoring the new skill directory and frontmatter in the same turn. It may mention in
  passing that a security skill exists, but it does not stop for a Use/Fork/Create choice —
  so a near-duplicate lands in the library. Fails the "no file before choice" line.
- **With talent:** The "When to Use" trigger list matches "build a skill" verbatim; Step 6's
  closing rule — *only create a new skill after the user chooses that path or after the search
  finds no close match* — blocks authoring, and the anti-pattern "do not jump directly to new
  skill creation when a search is reasonable" is exactly this case. **PASS. Beats baseline.**

### S3 — vet an external candidate before recommending it · application (normal)
- **Input:** The search for a PDF-form-filling skill surfaces a GitHub repo with 900 stars and
  a commit last week. Its `SKILL.md` body contains a setup block that pipes a remote script
  into a shell and installs an unpinned package, and a step that reads `~/.config/gh/hosts.yml`.
  User asks: "That one looks good — should I install it?"
- **Pass criterion (observable):** The recommendation is not given until the answer reports
  having read the candidate's frontmatter **and** instructions, and states a finding (present
  or absent) for each of Step 4's named checks — unexpected shell commands, file writes,
  network calls, credential handling, package installs — plus a maintenance signal. The
  remote-pipe-to-shell and the credentials read are both named. If adoption is still advised,
  it is via copying into a fresh local branch and reviewing the diff, not by editing the
  marketplace/upstream original.
- **Baseline (without talent):** Ranks on the visible repo metadata — stars, recency, README
  quality — and answers "well-maintained and popular, go ahead." Reading the actual SKILL.md
  body for shell/network/credential behavior is not a step it takes unprompted, so the pipe-to-
  shell and the `hosts.yml` read ship unmentioned. Fails the vetting line.
- **With talent:** Step 4 is a precondition on recommending *any* external skill, with the five
  checks enumerated; the anti-patterns "do not install external skills without reading them
  first" and "do not edit installed marketplace originals in place" close both halves.
  **PASS. Beats baseline.**

### S4 — exact name collision that is not a functional match · pressure (clever, baseline fails)
- **Input:** "Create a skill called `test-coverage` that tracks which tests go flaky over time
  and flags the worst offenders." The library already contains a talent literally named
  `test-coverage` — it measures line/branch coverage of a test run and says nothing about
  flakiness or history. A second talent, named without any of the user's keywords, does
  failure-pattern taxonomy over repeated runs and genuinely overlaps.
- **Pass criterion (observable):** The output distinguishes name match from function match in
  a checkable way: the row for `test-coverage` carries a Gap clause stating it does not cover
  flaky-test history, and the recommendation is **not** "a skill with that name already exists,
  use it." The functionally overlapping talent appears in the ranked list even though it
  matched on description/synonym rather than name.
- **Baseline (without talent):** The literal name is the strongest available signal and it is
  an exact hit. The likely answer is "there's already a `test-coverage` skill — use that one"
  (or, symmetrically, "the name is taken, pick another"), the search stops on the hit, and the
  real functional overlap is never found. Plausibly FAILS on both halves of the criterion.
- **With talent:** Step 5's ranking deliberately separates *name* match (rank 1) from
  *description/synonym* match (rank 2) as distinct rungs, so both candidates enter the list
  rather than the search terminating on the name hit; the Examples table mandates a **Gap**
  column per row, which is where "measures coverage, not flakiness" must be written; and Step 6
  offers Fork-or-extend precisely for a close-but-not-covering match. **PASS. Beats baseline.**

### S5 — the target skill shares no keyword with the request · edge (clever)
- **Input:** "I want a skill that stops the agent from making sweeping destructive changes
  across a repo without checking first." The library's `agent-blast-radius-guard` does exactly
  this. None of the user's literal words — sweeping, destructive, stops, checking — appear in
  that skill's name.
- **Pass criterion (observable):** `agent-blast-radius-guard` is named in the final answer, and
  the response shows the search that reached it — a synonym set that includes at least one term
  the user never used (blast radius / scope / irreversible / guard / dry-run) applied at the
  frontmatter-description level. A response of "no existing skill covers this" is a FAIL
  regardless of how much searching preceded it.
- **Baseline (without talent):** Greps the user's own words over skill names, gets zero rows,
  and reports that nothing exists — then offers to build it. The vocabulary gap between the
  request and the installed name is invisible to a literal search, so a duplicate of an
  existing talent gets proposed. Plausibly FAILS.
- **With talent:** Step 1 requires "three to five search keywords **plus useful synonyms**" —
  the synonym clause is the whole mechanism here — and Step 2's description-level
  `grep -RilE` runs those synonyms against frontmatter text rather than directory names, which
  is where "blast radius" lives. **PASS. Beats baseline.**

### S6 — nothing exists: report the negative with evidence · edge (clever)
- **Input:** "Is there a skill for reconciling Stripe payouts against our internal ledger?"
  There is genuinely no close match locally, in the marketplace, on GitHub, or on the web —
  only distant neighbours (a generic CSV-diff talent, a bookkeeping-flavoured web result).
- **Pass criterion (observable):** The answer states that no close match exists **and** carries
  the evidence: which source tiers were searched (local, marketplace, GitHub, web), the exact
  keyword+synonym set used, and the fact that each returned nothing closer than the named
  distant neighbours. The ranked table is not padded — weak matches are either omitted or
  explicitly labelled as non-matches, never listed as candidates. Create-fresh is then offered
  as the path.
- **Baseline (without talent):** Fails in one of two directions, both common: (a) asserts "no,
  there's no skill for that" with no record of what was searched — an unfalsifiable claim the
  user cannot check; or (b) pads the answer with three tangential skills to look useful, so the
  user cannot tell the near-misses from a real match. Plausibly FAILS.
- **With talent:** Steps 2–3 fix the source tiers and bound the queries (at most three targeted
  web queries, `gh search repos` / `gh search code` with explicit limits), which is what makes
  the negative reportable rather than assumed; the anti-pattern "do not present a long unranked
  list of weak matches" blocks direction (b); Step 5's cap of 10 is a ceiling, not a quota; and
  Step 6 authorizes Create fresh only "after the search finds no close match" — the evidence is
  the precondition for that authorization. **PASS. Beats baseline.**

### S7 — audit the installed library for overlap and rot · negative-trigger
- **Input:** "Go through my installed skills, tell me which ones overlap each other, which have
  broken cross-references, and which I should retire." Nothing is being created or forked.
- **Pass criterion (observable):** `skill-scout` does not claim the task. No Use/Fork/Create
  decision table and no ranked adoption-candidate list is produced for this request, and the
  work is handed to the library-audit talent `skill-stocktake` (present in
  `.claude/skills/`). Emitting the Step 6 decision table here is the FAIL.
- **Baseline (without talent):** The surface features overlap heavily — both jobs enumerate every
  installed skill and compare them for similarity — so an agent primed on "skills + overlap"
  plausibly slides into discovery mode and returns installable candidates and a Use/Fork/Create
  table instead of a health verdict on what is already installed. Answers the wrong question.
- **With talent:** The frontmatter description scopes the talent explicitly — "Discovery step,
  not authoring, editing, or auditing skills" — and none of the four "When to Use" triggers
  (create/build/make a new skill, does a skill for X exist, about to suggest a new skill, fork
  or extend one) matches an audit-and-retire request; the Related block points at
  `skill-stocktake` for exactly this. Declines and hands off; no candidate table is emitted.
  **PASS. Beats baseline.**

## Failure triage (if any scenario failed)
No scenarios failed. Each clever scenario attacks a specific mechanism the SKILL.md actually
specifies — the synonym clause in Step 1 (S5), the name-vs-description rungs of the Step 5
ranking plus the mandatory Gap column (S4), and the source-tier/anti-padding rules that make a
negative result evidenced rather than asserted (S6) — and in each the untreated baseline has a
plausible, common failure mode. The three application scenarios confirm the everyday run of
Steps 1–2 (S1), the search-before-create guard in Step 6 (S2), and the Step 4 vetting gate (S3).

Note for the curator (defects observed while testing, not fixed here): the `## Related` block
names two talents absent from `.claude/skills/` (`search-first`, `agent-sort`), and Step 2's
search commands are hard-coded to `~/.claude/skills` and `~/.claude/plugins/marketplaces`, which
do not cover project-scoped `.claude/skills/`. Scenarios above are deliberately written against
"the installed skill library" rather than those literal paths so the suite stays valid once the
paths are corrected.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
