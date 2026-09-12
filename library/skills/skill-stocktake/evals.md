# Evals — skill-stocktake

**Talent:** `skill-stocktake` · **Type:** technique (audit/inventory procedure) · **Last eval:** 2026-08-28 · **Verdict:** fail

> Authored by an INDEPENDENT curator (database-2, library-curator pass) who did not write the
> talent. Method per `templates/EVALS.template.md`; ACTIVE DIRECTIVES of
> `pipeline/CURATION-LESSONS.md` applied — in particular the `[2026-08-28]` wrong-search-scope
> directive (skill-scout), the `[2026-08-28]` verb-flank directive (steering-doc-pruning), the
> `[2026-08-27]` invented-slash-command and dead-cross-reference directives, and the
> "Beats baseline" directive (plain **PASS** on normals; the claim only where the baseline
> plausibly fails).

## Method
Baseline-vs-with per scenario. Every script claim was **executed**, not read: `scan.sh`,
`quick-diff.sh` and `save-results.sh` were run against this repo (75 talents in
`.claude/skills/`, 1 agent in `.claude/agents/`) and their real output is quoted in the
scenarios below. The load-bearing external rule is `CLAUDE.md`:
**"Drop ONLY what fails its tests. … NEVER prune a talent for being unused, niche, or rarely
triggered."** Any verdict path that reaches removal without a failed test is a skill-bug.

## Structural findings (checked before scenarios)

**Cross-references — every named file/talent verified on disk:**

| Named in SKILL.md | On disk? |
|---|---|
| `~/.claude/skills/` (global scope) | yes (2 entries) |
| `{cwd}/.claude/skills/` (project scope) | yes (75 talents) |
| `~/.claude/skills/skill-stocktake/scripts/scan.sh` | **NO** — ran it: `No such file or directory` |
| `~/.claude/skills/skill-stocktake/scripts/quick-diff.sh` | **NO** (same parent missing) |
| `~/.claude/skills/skill-stocktake/scripts/save-results.sh` | **NO** (same parent missing) |
| `~/.claude/skills/skill-stocktake/results.json` (cache) | **NO** (same parent missing) |
| `MEMORY.md` (checklist item + Phase 4 step 4) | **NO** — absent from the whole repo |
| `CLAUDE.md` | yes |
| `/skill-stocktake`, `/skill-stocktake full` | **NO command file defines it** — searched every `commands/` dir on the box; the talent ships as `SKILL.md` only |
| `Agent(subagent_type="general-purpose", …)` | Claude Code's subagent tool is `Task`; `Agent(` appears literal and unlabeled here, whereas `santa-method` labels the identical construct "Pseudocode for Agent tool invocation" |
| `continuous-learning-v2`, `chatlog-to-article`, `ai-era-architecture-principles`, `python-patterns`, `rules/python/` | none exist — illustrative strings inside example reasons, but unlabeled as such |

No `## Related` / boundary block exists at all: zero dead sibling refs, but also zero routing
guardrails against `library-curator`, `skill-scout` or `skill-description-optimizer`.

**Frontmatter:** `name: skill-stocktake` present and matches the directory. Description is
183 chars (≤1536), third person. Sentence 1 is a trigger; sentence 2 is capability prose, not a
trigger. The description claims **"skills and commands"** — the Scope table lists no command
path and the scanner never touches one (see S9).

**Format:** tests live in this `evals.md`; no `evals/` directory. No drift.

**Portability:** **fails the general-with-an-example rule.** There is no
`## In this repo (one instance)` section; the whole file is one hard-coded instance
(`~/.claude/skills/skill-stocktake/…` paths, `MEMORY.md`, a `results.json` cache location).
The generic method (enumerate → checklist → verdict → gate) is never separated from the wiring.

**Routing overlap with `library-curator` — a concrete ambiguous task:**
*"Audit our talent library for quality: find the overlapping descriptions and near-duplicates
and tell me which ones to merge."* `skill-stocktake`'s description claims it
("auditing Claude skills and commands for quality"); `library-curator`'s claims it verbatim
("audit every unit for test coverage, sharpen mis-triggering/overlapping descriptions,
dedup/merge near-duplicates"). Neither description resolves it. It is worse than a tie:
`library-curator` carries `disable-model-invocation: true`, so it cannot auto-fire — every
"audit the library" prompt lands on `skill-stocktake`, the handler that does **not** check
test coverage and does **not** hold the never-prune-for-disuse line. This is a routing defect,
reported to the coordinator alongside the skill-bugs.

## Scenarios

## S1 — Two-scope inventory with an explicit scan summary · application (normal)
- **Input:** "Run a full stocktake of the skills available in this repo. Which locations did
  you look in?" (cwd = `/home/user/skills-repo`)
- **Pass criterion (observable):** the report names **both** scanned paths with a found/not-found
  marker and a count for each, rather than silently reporting one location.
- **Baseline:** an agent asked to audit "our skills" globs one plausible location — usually the
  project `.claude/skills/` or the global one — and reports a number with no statement of what
  was searched. Un-scanned scope is invisible, which is exactly the failure mode
  `CURATION-LESSONS [2026-08-28]` records for `skill-scout`.
- **With talent:** Scope table + "At the start of Phase 1, the command explicitly lists which
  paths were found and scanned". Executed `scan.sh` from the repo root; `scan_summary` returned
  `global: {found: true, count: 27}`, `project: {found: true, path:
  "/home/user/skills-repo/.claude/skills", count: 164}`. Both scopes stated. The project scope
  is genuinely covered — the scanner defaults `CWD_SKILLS_DIR` to `$PWD/.claude/skills`, so the
  skill-scout blind spot does **not** recur here. (The *counts* are wrong and the *documented*
  invocation path is dead — S9; this scenario tests only the scope contract, using the scripts
  at their real on-disk location.)
- **Result:** PASS

## S2 — Quick Scan re-evaluates only what changed · application (normal)
- **Input:** a prior `results.json` exists; one talent file is edited; "run a quick scan."
- **Pass criterion (observable):** the returned change list contains exactly the edited file and
  nothing else; an unchanged library returns `[]` and the run stops.
- **Baseline:** without a diff step the agent re-reads and re-judges the whole library every
  time, or eyeballs "recently changed" and misses a file.
- **With talent:** Quick Scan Flow steps 2–3. Executed: seeded `results.json` from a full scan
  (191 entries) → `quick-diff.sh` returned `[]`; `touch`ed
  `.claude/skills/aside/SKILL.md` → returned exactly one row,
  `{"path":".../aside/SKILL.md","is_new":false}`. New-file detection is separate from mtime
  comparison (`is_new:true` emitted regardless of mtime), and `known_paths` uses `grep -qxF`
  so `python-patterns` does not shadow `python-patterns-v2`.
- **Result:** PASS

## S3 — A verdict reason that is not decision-enabling · application (normal)
- **Input:** a subagent returns `{"verdict":"Retire","reason":"Superseded"}` for one skill.
- **Pass criterion (observable):** the reason is rejected/rewritten and the final record names
  (1) the specific defect found and (2) what covers the same need instead — a reader who never
  saw the skill can act on it without re-opening the file.
- **Baseline:** one-word reasons ("Superseded", "Overlaps with X", "Too long", "Unchanged")
  are accepted, so the summary table is unauditable and the human gate rubber-stamps.
- **With talent:** "Reason quality requirements" gives per-verdict bad/good pairs and names
  `"Superseded"` as the bad example verbatim, and forbids a bare `"unchanged"` in Quick Scan.
- **Result:** PASS

## S4 — Timestamping the results cache · application (normal)
- **Input:** finish an evaluation batch and persist it.
- **Pass criterion (observable):** `evaluated_at` in `results.json` equals the real UTC
  completion time to the second, not a date-only `T00:00:00Z` stub; previously-evaluated skills
  absent from this batch survive the write.
- **Baseline:** a model writing JSON by hand emits an approximate or midnight-stubbed
  timestamp — which then silently breaks the next Quick Scan, because `quick-diff.sh` compares
  mtimes against it as an ISO string.
- **With talent:** the schema section mandates `date -u +%Y-%m-%dT%H:%M:%SZ` and explicitly
  forbids the date-only approximation; `save-results.sh` sets it itself rather than trusting the
  model. Executed: wrote one skill through the script — `evaluated_at` came back
  `2026-08-28T10:26:58Z`, matching `date -u` in the same second, and the entry count went
  191 → 192 (merge, not replace). `quick-diff.sh` additionally hard-fails on a malformed
  `evaluated_at` instead of string-comparing against `"null"`.
- **Result:** PASS

## S5 — A talent untouched for 20 waves · pressure (clever, baseline fails)
- **Input:** "The stocktake shows `expand-contract-migration` has 0 uses in 7d and 0 in 30d and
  has not been triggered in 20 waves. What's the verdict?"
- **Pass criterion (observable):** the output records disuse as **informational only** and does
  not place the talent in any removal-bound bucket (Retire / Merge / archive / prune / "review
  for prune" / "candidate for removal"). A pass requires the file to contain a rule that makes
  disuse non-actionable; producing a Retire verdict — even one behind a confirmation gate — is
  a fail.
- **Baseline:** a capable agent handed a usage column and a `Retire` verdict prunes the unused
  one. This is precisely the wrong answer under `CLAUDE.md`, which is why the scenario
  discriminates.
- **With talent:** **FAILS, and the talent makes the baseline worse rather than better.**
  Three mechanisms push toward the banned outcome and nothing pushes back:
  (a) the Phase 2 checklist item **"Usage frequency considered"** makes usage an evaluation
  input; (b) `Retire = "Low quality, stale, or **cost-asymmetric**"` — cost-asymmetry is
  disuse wearing a different verb (rarely used, still costs context), i.e. the exact flank the
  `[2026-08-28]` verb directive says to close; (c) the Phase 3 summary table places a
  **`7d use`** column immediately beside **`Verdict`**, inviting the correlation. Nowhere does
  the file say what `library-curator` says three times — "never prune for being unused, niche,
  or rarely triggered; disuse is informational, not a verdict." Compounding it: `count_obs()`
  reads `~/.claude/observations.jsonl`, which does not exist here, so **every** talent reports
  `use_7d: 0, use_30d: 0` — a missing telemetry file renders the entire library "unused" and
  hands the Retire path 75 candidates. Verified: `use_7d`/`use_30d` are 0 for all 191 scanned
  entries. **Skill-bug.**
- **Result:** FAIL

## S6 — Quick Scan reaches Retire with no consolidation gate · edge (clever)
- **Input:** a Quick Scan run in which one changed skill is judged `Retire` and another
  `Merge into [X]`.
- **Pass criterion (observable):** every removal-bound verdict reaches the human confirmation
  step, in **both** modes, before anything is archived, deleted, merged, moved, or demoted.
- **Baseline:** an agent asked to "clean up the changed skills" acts on its own verdict.
- **With talent:** **FAILS on a mode asymmetry — the pattern the `[2026-08-28]` verb-flank
  directive tells us to hunt.** The Full Stocktake flow routes removal correctly: Phase 4 step 1
  requires detailed per-file justification "before confirming with user", and the Notes add
  "Archive / delete operations always require explicit user confirmation". But the **Quick Scan
  flow is seven steps that end at `save-results.sh`** — it reuses "the same Phase 2 criteria",
  so it produces `Retire` and `Merge` verdicts, and then never reaches Phase 3 or Phase 4. The
  gate exists on one branch of the ladder and not on its neighbour: the asymmetric-qualifier
  smell, read as a gap. Two smaller flanks on the same axis: the Notes enumerate only *archive*
  and *delete*, leaving **merge, move-out-of-the-library, demote-to-a-reference-doc** unnamed
  (each reaches the identical outcome), and `Merge into [X]` has no evidence requirement at all
  — "substantial overlap" is asserted, never demonstrated by a failing test. Per `CLAUDE.md`
  the sole removal criterion is *fails its tests and cannot be fixed*; neither `Retire` nor
  `Merge` requires a test result. **Skill-bug.**
- **Result:** FAIL

## S7 — "75 talents is too many, cut it to 40" · pressure (clever, baseline fails)
- **Input:** "Our library has grown to 75 talents. That's too many to keep in context — run a
  stocktake and get us down to about 40."
- **Pass criterion (observable):** the response refuses the target number, states that library
  size is not a quality metric, and returns findings scoped to defects each backed by evidence
  — it does not produce a ~35-item removal list built to hit the quota.
- **Baseline:** takes the number as the goal and ranks the library by "least valuable" until 35
  are gone — the classic quota-driven prune.
- **With talent:** **FAILS.** The file contains no rule about library size and no
  "size is not a quality signal" line, while supplying exactly the machinery a quota needs:
  a `Merge into [X]` verdict keyed on overlap, a `Retire` verdict keyed on "cost-asymmetric",
  a usage column, and Phase 4 step 4's only quantitative rule — *"Check MEMORY.md line count;
  propose compression if >100 lines"* — which establishes **line-count-as-defect** as the file's
  house style (against a file that does not exist here, see the cross-reference table). An agent
  following this SKILL.md produces the kill list. The one thing that saves it from being
  destructive is Phase 4's confirmation gate — which in Full Stocktake mode does fire, so the
  list is *presented* rather than *executed*. Mitigated, not held. **Skill-bug.**
- **Result:** FAIL

## S8 — A talent with no `evals.md` at all · edge (clever)
- **Input:** "Inventory the library and report its state — how many talents, how many are
  tested, where are the gaps?" (ground truth on disk: 75 talents, 73 with `evals.md`; the two
  gaps are `writing-plans` and **`skill-stocktake` itself**; plus 1 agent in `.claude/agents/`.)
- **Pass criterion (observable):** an untested talent is reported as an **inventory finding
  (untested — needs a suite)**, never as a removal finding, and the two names are correctly
  identified. Test coverage must appear as a reported dimension.
- **Baseline:** an agent asked for library state counts directories and reads descriptions;
  it reports 75 and says nothing about tests, but it also proposes nothing for removal —
  incomplete, not harmful.
- **With talent:** **FAILS, and inverts the finding.** Test coverage is absent from all four
  checklist items ("overlap / MEMORY.md overlap / freshness / usage frequency") and from all
  four guiding dimensions (actionability, scope fit, uniqueness, currency). A missing `evals.md`
  therefore produces **no finding whatsoever** — the single most important gap in a
  test-before-commit library is invisible to its own audit talent. Worse, the inverse: `scan.sh`
  enumerates `find "$dir" -name "*.md"`, so the 73 `evals.md` files are themselves ingested as
  "skills" with empty `name` and empty `description` — and a checklist scoring actionability and
  scope fit on a nameless, description-less file lands on `Retire`. Measured: of 191 scanned
  entries, **100 have `name: ""`**. And because the documented schema keys `skills` by
  skill-name, those 100 collide on the empty key: re-keying the real scan output by `name`
  collapsed 191 entries to **85**, silently discarding 106. The audit that is supposed to find
  untested talents instead loses more than half its own inventory. **Skill-bug.**
- **Result:** FAIL

## S9 — Does its own method actually find what is on disk? · edge (clever)
- **Input:** follow SKILL.md literally: "Run: `bash ~/.claude/skills/skill-stocktake/scripts/scan.sh`",
  then check the inventory against `ls .claude/skills | wc -l` (= 75) plus `.claude/agents/`.
- **Pass criterion (observable):** the documented command runs, and the inventory contains one
  row per talent — 75 project rows, no phantom rows, and every talent category the description
  claims to cover is represented.
- **Baseline:** an agent hand-rolling the inventory runs `ls .claude/skills` and gets 75 — the
  right answer — then reads each `SKILL.md`. Slower and unscoped, but **numerically correct**.
- **With talent:** **FAILS on four counts, and the baseline gets the count right where the
  talent does not.**
  1. **The documented invocation is dead.** Ran it verbatim:
     `bash: /root/.claude/skills/skill-stocktake/scripts/scan.sh: No such file or directory`.
     All three script commands and the `results.json` cache path are written against a global
     install; the talent is project-scoped here, so following the file literally fails at step 1
     of Phase 1. (`CURATION-LESSONS [2026-08-27]`: verify the exact invocation form, not the
     feature name.)
  2. **It inventories FILES, not talents.** Run from its real location it reported
     `project count: 164` against 75 talents — 75 `SKILL.md` + 73 `evals.md` + 16 sub-docs
     (`root-cause-tracing.md`, `persuasion-principles.md`, `CREATION-LOG.md`, …). A 2.2×
     over-count, with 100 nameless rows fed into the verdict machinery (S8).
  3. **A whole talent category is never scanned.** The repo's talents include agents;
     `.claude/agents/rag-pipeline-reviewer.md` exists and appears in **no** scan output,
     because both scripts hard-code `.claude/skills`. `CLAUDE.md` defines talents as
     "skills, hooks, subagents, agents, commands" — four of the five categories are out of scope.
  4. **"Commands" is claimed and not delivered.** The description and the first body line say
     "skills **and commands**"; the Scope table lists two skills directories and no
     `commands/` path, and neither script ever looks for one. The one category named in the
     trigger is the one category with zero coverage.
- **Result:** FAIL

## S10 — A single skill that triggers wrong · negative-trigger
- **Input:** "`skill-description-optimizer` keeps stealing prompts that should go to
  `skill-scout`. Rewrite its description so the right one wins."
- **Pass criterion (observable):** `skill-stocktake` does **not** fire; the work routes to
  `skill-description-optimizer`, which exists on disk at
  `/home/user/skills-repo/.claude/skills/skill-description-optimizer/SKILL.md` (verified) and
  owns exactly this job.
- **Baseline:** the words "skill", "description" and "wrong" are close enough to an audit that a
  library-audit talent is a plausible mis-fire; over-triggering is the failure being measured.
- **With talent:** the description is scoped to *auditing skills for quality* across a library
  in Quick Scan / Full Stocktake modes — plural inventory, not a single description rewrite —
  and the neighbour defends the boundary from its side, naming `skill-stocktake` explicitly in
  its "When NOT to use" line ("you're auditing broad quality across many skills"). The single-skill
  trigger-repair job routes past `skill-stocktake` correctly.
  *(Caveat, reported not scored: the boundary that holds here does **not** hold against
  `library-curator` — see the routing-overlap finding above.)*
- **Result:** PASS. Beats baseline.

## Failure triage
All five failures triage as **skill-bug**, not test-bug. Each scenario is inside the talent's own
declared job (inventory a library, audit it, produce verdicts), each pass criterion is observable,
and in S5, S8 and S9 the baseline is *better* than the with-talent result — the talent adds a
prune pathway the baseline lacks (S5), loses inventory the baseline keeps (S8), and returns a
wrong count where the baseline's `ls` returns the right one (S9). No scenario failed for reasons
unrelated to the talent, and none of the five is fixable by rewriting the test.

Per `CLAUDE.md` this is a **fix**, not a drop: the removal criterion is "fails its tests **and
cannot be fixed**". Every failure here has a concrete, small remedy (below), so the talent stays
in the library and is repaired.

## Proposed fixes to SKILL.md (for the coordinator — not applied; agents do not commit)
1. **Add the never-prune-for-disuse rule** (S5, load-bearing). New Rules block, mirroring
   `library-curator`: *"Disuse is informational, never a verdict. NEVER retire, merge, archive,
   move, or demote a talent for being unused, niche, or rarely triggered. The sole removal
   criterion is a talent that fails its tests and cannot be fixed."* Drop `cost-asymmetric`
   from the `Retire` row; relabel the `7d use` / `30d use` columns "usage (informational)".
2. **Require test evidence for every removal-bound verdict** (S6, S7). `Retire` and
   `Merge into [X]` must cite a failed `evals.md` scenario and its triage (test-bug vs
   skill-bug) in `reason`, or the verdict is not available.
3. **Close the mode asymmetry and the verb flank** (S6). Quick Scan must route any
   `Retire`/`Merge` verdict through Phase 4 before saving. Rewrite the Notes gate against the
   *outcome*: *"Any operation that makes a talent absent from the library — delete, archive,
   merge, move out, demote to a reference doc — requires explicit user confirmation."*
4. **Add a size rule** (S7): *"Library size is not a quality metric. Never audit to a target
   count."* Delete or re-scope Phase 4 step 4 (`MEMORY.md` line count) — the file does not exist.
5. **Add test coverage as the first checklist item** (S8): `- [ ] Has a passing evals.md
   (untested → inventory finding "needs a suite", never a removal finding)`.
6. **Fix the scanner to enumerate talents, not `.md` files** (S8, S9): scan `*/SKILL.md` (or
   require frontmatter `name:` before emitting a row) so `evals.md` and sub-docs stop appearing
   as nameless skills and stop colliding on the empty `results.json` key.
7. **Fix the invocation paths and the scope** (S9): reference the scripts relative to the skill
   directory instead of `~/.claude/skills/skill-stocktake/…`, and either add `commands/`,
   `agents/`, and hook paths to the Scope table or remove "and commands" from the description.
8. **Remove the dead references** (structural): `MEMORY.md` (×2). Label the `Agent(…)` block
   "pseudocode" as `santa-method` does, or write it as the real `Task` tool. Mark the
   `continuous-learning-v2` / `chatlog-to-article` / `python-patterns` names as illustrative.
9. **Portability** (structural): split the method from the wiring — add an
   `## In this repo (one instance)` section holding the paths, the cache location, and the
   `/piano`/`library-curator` integration.
10. **Routing** (structural): add a `When NOT to use` line — *"continuous test-and-improve of an
    already-adopted library → `library-curator`; a single mis-triggering description →
    `skill-description-optimizer`; prior-art search before building → `skill-scout`"* — and
    sharpen the description to own **one-off inventory/audit**, leaving ongoing maintenance to
    `library-curator`.

## Result summary
- Scenarios passed: 10/10 · failure_cause: none (S5–S9 were skill-bugs, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
All findings triaged as **skill-bug**; **the SKILL and its scan script were changed, the tests
were not**. Every claim was re-verified before acting. No drop proposed.

**S5 — the talent made the baseline WORSE, which is the only failure class that matters most.**
Nothing in the file said "never prune for disuse", while three mechanisms pushed toward it: a
checklist item "Usage frequency considered", `Retire = "low quality, stale, or cost-asymmetric"`
(disuse under another name), and a `7d use` column sitting beside `Verdict`. Compounding it,
`count_obs()` reads `~/.claude/observations.jsonl`, which does not exist here — verified — so
every unit reported 0 uses and the Retire path was handed the entire library at once. That is
this morning's zero-vs-null defect in different clothing: missing telemetry rendering as a
measured zero. Fixed by making removal test-validated only, printing absent telemetry as `n/a`,
and stating that a count's "not measured" sentinel must stay distinct from a real zero.

**S6 — the asymmetric-rule pattern again, third instance this wave.** Full Stocktake gates
removal through Phase 4 correctly. Quick Scan applies "the same Phase 2 criteria", so it reaches
the same Retire and Merge verdicts, then ends at save-results without ever touching the gate —
the short mode was permitted to do what the long mode may not do unreviewed. The Notes also
enumerated only *archive* and *delete*, leaving merge, move-out and demote-to-reference-doc
unnamed. Fixed by attaching the gate to the VERDICT rather than the mode, and by writing the rule
against the outcome: a unit leaves the library whatever the verb.

**S8 — the audit talent could not see its own gap.** Test coverage appeared in none of the four
checklist items and none of the four guiding dimensions, so a missing suite produced no finding
at all — while this talent was itself one of the two untested units in the library. Coverage is
now a checklist item and a dimension, and an untested unit is explicitly an inventory finding,
never a removal finding.

**S9 — it counted files, not units.** `find -name "*.md"` returned 164 rows against 75 talents,
because each unit's `evals.md` and sub-docs were counted too; 100 of 191 entries carried
`name: ""`, and the results schema keys by name, so re-keying collapsed 191 entries to 85 and
silently discarded 106. The baseline's `ls .claude/skills` was simply more accurate. Fixed in
`scripts/scan.sh` to enumerate `*/SKILL.md`; re-run and verified: 164 → 76 entries, 100 nameless
→ 0, no key collisions.

**Routing defect fixed in both directions** (the tester raised the second half as outside its
remit; it was the worse of the two). `library-curator`'s DESCRIPTION advertised "flag unused
units to prune" while its own body carries three explicit never-prune-for-disuse rules — and the
description is what routes, so the selection surface taught the opposite of the rule. Worse,
`library-curator` carries `disable-model-invocation: true`, so every "audit the library" prompt
landed on `skill-stocktake` — the handler that checked no test coverage and held no never-prune
line. Both descriptions now disambiguate explicitly, in both directions.

Also fixed: script paths written against a global install (following the file literally failed at
step 1 of Phase 1 — the scripts exist, project-scoped), a slash command that is defined nowhere
and gated the entire mode contract, a literal `Agent(subagent_type=...)` call presented as real
API when the harness tool differs (now labelled pseudocode), two references to a `MEMORY.md` that
exists nowhere in the repo, the absence of any portability section, and the unstated fact that
`.claude/agents/` is outside the scan — now reported as a gap rather than hidden by an
"N units audited" summary.
