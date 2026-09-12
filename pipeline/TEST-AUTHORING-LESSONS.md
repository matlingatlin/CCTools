# TEST-AUTHORING LESSONS (shared brain — read AND write before/after any test authoring)

The ONE shared store of "how to write good tests" for the WHOLE system. **Both** the
`library-curator` (database-2 maintenance) **and** the loop's TEST step (`/piano` build→TEST,
`test-wave`) read these directives before authoring tests, and BOTH write their learnings
back here — so a lesson learned by either improves the tests written by the other. Not two
silos; one brain.

**The filename now matches the header.** Until 2026-09-12 this file was `CURATION-LESSONS.md`
with a header about tests, and a writer looking for where *curation* lessons go landed here by
name and appended anyway. Measured: of 22 entries added on 2026-09-12, **3** were about authoring
tests; roughly 85 entries were an operating journal. The journal now lives in
`pipeline/CURATION-LESSONS.md`, which is what its name always promised, and the nine entries in it
that *were* addressed to a test author have been promoted into the directives below.

**Before appending here, ask who the entry is addressed to.** A directive a test author applies
before writing a suite belongs here. A lesson about running the knowledge base, a watcher, a
graph, a source or a build belongs in `pipeline/CURATION-LESSONS.md`. The measurement and the
reasoning behind the split: `pipeline/reviews/2026-09-12-lessons-file-dilution.md`.

Each pass/wave records signals (test-bug vs skill-bug rate, recurring overlap patterns,
false-drops avoided, flawed-test patterns) and derives directives here; the NEXT test author
— curator or loop — reads them first, so every test written anywhere gets fairer and cleverer
over time. Durable directives are promoted into `templates/EVALS.template.md`. Related:
[[testing-skills-methodology]].

## ACTIVE DIRECTIVES (apply before authoring tests / sharpening)
- `[seed]` **Triage every red result before fix/drop** — classify test-bug vs skill-bug; a bad
  test never condemns a good skill. Drop only a test-validated, unfixable skill failure.
- `[seed]` **Every scenario needs an OBSERVABLE pass criterion** — a subjective line ("looks
  good") is a test-bug in the making; state a pass/fail an outsider could check.
- `[seed]` **Blend normal + clever** — a suite is ~half normal/representative (the everyday
  job) and ~half clever/adversarial (traps, edge), plus a negative-trigger. Not only traps
  (misses the bread-and-butter job), not only happy-path (misses where it breaks).
- `[seed]` **Design the CLEVER ones so the baseline plausibly FAILS** — those discriminate and
  prove the talent earns its place. Normal ones may pass at baseline; they confirm everyday behavior.
- `[seed]` **Match scenario type to talent type** — discipline talents get pressure scenarios
  (tempt the wrong behavior); technique talents get application scenarios.
- `[2026-08-27]` **Tests live in `evals.md`, never an `evals/` JSON dir** — format-drift is a
  detectable structural defect (curator + automated runners key off `evals.md`). Flag and
  reformat any talent whose tests live elsewhere. (Found on deep-reading, pass 1.)
- `[2026-08-27]` **Hunt dead cross-references** — a talent's "Related/Do-not-use-for/hand-off"
  blocks rot when sibling talents are renamed/removed. Every named talent must exist; fix
  stale ones to the real talent. (High-yield: fixed across 4/10 pass 1, ~5/10 pass 2.)
- `[2026-08-27]` **Verify the exact INVOCATION FORM, not just the feature name** — a feature
  can exist while the documented syntax is wrong. graphify's obsidian export: the pilot wrote
  the *flag* `extract --obsidian` (silently ignored → looks broken); the real form is the
  *subcommand* `graphify export obsidian` (works — 2502-note vault). Curator "removed the
  feature" on the flag failure; the fresh source fetch settled it. Run the actual command,
  and when a claim looks false, check whether it's the SYNTAX that's wrong before deleting.
  **Third instance (2026-09-04), which sharpens the lesson:** the flag was never wrong, it was
  on the wrong SURFACE — `/graphify … --obsidian` is documented, `extract --obsidian` is not,
  and the repository's default branch serves a README a year behind the one this repo quotes.
  So the check is three questions, not one: is the FEATURE real, is the SYNTAX right, and is
  the SURFACE (and the doc BRANCH) the one I am invoking? Deleting a claim answers none of them.
  **Fourth instance (2026-09-04, and the first with a blast radius):** `export wiki --dir X`
  accepts `--dir`, errors on nothing, ignores it, and writes 238 files beside the `--graph`
  file — which in this repo is the immutable `intake/` import, untracked-but-not-ignored, one
  `git add -A` from being committed. A silently-ignored flag is not only a wrong answer; it is
  a write somewhere you did not choose. Run destructive-adjacent exports from a scratch copy.
  **Second instance (graphify 0.9.50, full re-audit):** `--no-viz` on `extract` is
  accepted-then-SILENTLY-IGNORED — it's a `cluster-only` flag. A flag on the wrong subcommand
  no-ops, it isn't rejected. Verify each flag against the `--help` of the EXACT subcommand it
  sits on, and RUN every documented format/command end-to-end — the re-audit found `export svg`
  needs matplotlib and `export neo4j/falkordb` only write a file unless `--push`, none of which
  `--help` alone reveals. Don't verify ONE path (obsidian) and assume the rest; check them all.
- `[2026-08-27]` **Hunt invented slash-commands / built-ins** — a talent that references
  `/foo` commands or built-ins defined nowhere is a quality defect (distinct from dead
  cross-refs). Reframe as illustrative or remove. (Found on eval-harness, pass 2.)
- `[2026-08-27]` **Check frontmatter has `name:`** — pass 2 found `learn-eval` missing its
  `name:` field (would break loading). Every talent needs name+description.
- `[2026-08-27]` **Verify a "consolidated N→M" claim scenario-by-scenario BEFORE deleting the
  source.** A curator that folds legacy test files into `evals.md` can silently drop a case.
  Pass 3 claimed systematic-debugging's 4 legacy `test-*.md` were "consolidated into S3/S4" —
  verification found the **sunk-cost/exhaustion** pressure vector (test-pressure-2) was NOT
  captured (S2 had the symptom, not the pressure). Absorbed it as S4b, THEN removed the source.
  Rule: a subsume-and-delete is safe only after each source scenario is confirmed present in
  the target; distinct PRESSURE vectors (urgency / sunk-cost / authority) don't collapse into one.

- `[2026-08-28]` **Test the MOST-USED untested talents first — usage is the risk signal.** Ranking
  the untested backlog by `talents_used` in `metrics.jsonl` (instead of alphabetically) put
  `skill-scout` (12 waves) and `factory` (8) at the top — and skill-scout turned out to carry a
  real, load-bearing defect. Highest usage + zero tests = highest risk; curate in that order.
- `[2026-08-28]` **A wrong SEARCH SCOPE is a silent failure, not an error — hunt it.** skill-scout's
  Step 2 searched only `~/.claude/skills` and marketplaces, never project-scoped `.claude/skills/`
  where this repo's 65 talents live. It returned zero, so "nothing similar exists" looked *proven*
  and the dedup gate ran blind for 12 waves. Measured: a keyword with 4 project matches returned 0.
  Generalize: when a talent's method SEARCHES, verify the scope actually covers where the artifacts
  live — run its own command and confirm a known-present item is found. A search that returns
  nothing is indistinguishable from a search that looked in the wrong place; only running it tells.

- `[2026-08-28]` **"Beats baseline" is a CLAIM, not a formatting requirement — and it is false on
  most normals.** An independent tester deliberately deviated from the instruction it was given,
  ending only 7 of 11 With-talent lines with "PASS. Beats baseline." Its reasoning was correct and
  the instruction was wrong: normal scenarios exist to confirm everyday behavior, so a capable
  baseline often passes them, and asserting a win there is exactly the rubber stamp the suite
  exists to prevent. Fixed in `templates/EVALS.template.md`. Two consequences: (a) never write a
  test-authoring instruction that mandates a verdict phrase — mandate the CRITERION, let the
  verdict follow; (b) an agent that pushes back on a flawed instruction with a reason is doing the
  job; take the reason seriously before assuming it deviated.

- `[2026-08-28]` **A boundary written against ONE verb leaves the synonym flank open — test the
  flank, not the rule.** `steering-doc-pruning` edits CLAUDE.md by design, so it carries a hard rule:
  policy and safety lines are never removable, whatever an A/B shows. That rule was airtight against
  *delete* and wide open against *move to a load-on-demand file* — which reaches the identical
  outcome (the line is absent on every turn that does not load it) through a verb the method
  explicitly permits. Worse, three separate passages licensed it, and the one guard on that side
  ("a move with no findable pointer is a deletion in disguise") was the wrong test: a pointer only
  helps a turn that already knows it needs the rule, and the turn about to drop the table is exactly
  the turn that was not going to open the ops file. **Generalize: whenever a talent forbids an
  outcome, enumerate the other verbs that reach the same outcome and test each one separately —
  delete vs move vs defer vs summarize vs "it's still in the repo". Write the rule against the
  OUTCOME, not the verb.** Also note the tell that made it findable: the file attached the
  qualifier "and not protected" to one rung of a ladder and not to its neighbour. An asymmetric
  qualifier across parallel branches is a reliable smell — read it as a gap, not as intent.

- `[2026-08-28]` **A claim that a talent does X, made in a DIFFERENT file, is not evidence the
  talent does X — check the talent.** `LESSONS.md` and `ROUTING.md` both recorded that
  `research-scout` consumes the source-yield verdicts. The skill contained zero occurrences of
  `LESSONS.md`, "source-yield", "deprioritize", or any read-back whatsoever. The loop that makes
  the system self-improving was open at the one place that picks what to work on, and every other
  component was written believing it was closed — so nothing anywhere reported a problem. This is
  the worst variant of the silent-failure family we keep finding: not a search in the wrong scope,
  but a step that is simply ABSENT while its counterparts assert it happens. **When two components
  are documented as handing off to each other, verify the hand-off from BOTH ends — grep the
  consumer for the producer's artifact by name. A one-ended assertion is a design intention, not a
  behaviour.**

- `[2026-08-28]` **The talent that measures a gap must WRITE the record the gap is measured from,
  and a diligent coordinator hides exactly this defect.** `talent-deploy` exists to close the
  deploy gap; its record step named the catalog status and usage log, neither of which the gap
  detector reads. Every `deployed` row had been written by the coordinator by hand, so the metric
  looked healthy for eleven waves while the control did not exist. **Generalize: when a metric
  reads healthy, ask WHO writes the underlying record — if the answer is "I do, by habit", the
  control is a person, not a system, and it fails the first time that person is busy.** Prefer
  finding this by reading the writer, not the number: the number looks identical either way.

- `[2026-08-28]` **A talent's DESCRIPTION is its routing surface — when it contradicts the body,
  the description wins and the rule never runs.** `library-curator`'s body carries three explicit
  never-prune-for-disuse rules; its description advertised "flag unused units to prune". Selection
  reads the description, so the surface taught the opposite of the rule the body enforces. Made
  worse by an invocation flag: `library-curator` is `disable-model-invocation: true`, so every
  "audit the library" prompt landed on `skill-stocktake` instead — the handler that checked no
  test coverage and held no never-prune line at all. **Two checks to run on every curation pass:
  (1) does the description contradict any rule in its own body? (2) for each pair of talents that
  could serve the same request, does an invocation flag silently hand every one of those requests
  to the weaker handler?** Neither is visible from reading one file.

- `[2026-08-28]` **Count the UNITS, not the files — and check a scan's total against something
  you can verify by hand.** `skill-stocktake` enumerated `*.md`, returning 164 rows against 75
  talents: each unit's `evals.md` and sub-docs were counted as units of their own, 100 of 191
  entries carried an empty `name:`, and the results schema keys by name, so re-keying silently
  discarded 106 entries. A plain `ls .claude/skills` was more accurate than the audit talent.
  **Any inventory number a talent reports should be reconciled once against a trivially checkable
  count; a 2.2x over-count survived because nobody ever compared the two.**

- `[2026-08-28]` **A talent adopted pre-loop and never re-audited carries its UPSTREAM's namespace
  and bundled assets intact.** `writing-plans` was byte-identical to its source: it referenced
  `executing-plans`, a sibling the adoption left behind, from both its execution menu and the
  header of every plan document it generates — and it carried `superpowers:`-prefixed names that
  resolve only under a plugin nobody installed (7 such references across 4 files; the empty
  `installed_plugins.json` settles it). **Adoption is not copying: it must include a
  resolve-every-name pass against the local library, plus an orphan sweep of the talent's own
  directory — a bundled file referenced by nothing is as much a defect as a reference pointing
  out.** Encouraging finding on the systemic question: three other talents are still byte-identical
  to upstream, and all three have passing evals and no orphans, so the curation loop had already
  reached them. The untested one was the one carrying the rot — which is the argument for
  coverage, stated as evidence rather than principle.

- `[2026-08-28]` **A method skill is biased toward its own ceremony — check that it scales DOWN.**
  `writing-plans` split a too-large spec but had no branch for work too small to plan, so applied
  as written it produced a dated plan file, a mandatory header and an executor menu for a one-line
  change: strictly worse than baseline. **Every process talent needs an explicit "this work does
  not need me" threshold, because producing the artifact always looks like doing the job.** When
  auditing one, look for the down-branch specifically; its absence is silent, and a sibling in the
  same chain often already has the branch to copy.

- `[2026-08-28]` **65% of our defects fail SILENTLY — so reading a file cannot find most of them.**
  Coding all 20 recorded defects with `error-analysis-taxonomy` (open-code, then axial-code to one
  primary mechanism each) produced a ranked taxonomy: wrong-scope 4, open-loop 3, asymmetric-rule
  3, missing-guard 3, dead-reference 2, mismeasurement 2, then one each of nondeterminism,
  factual-error, routing-contradiction. Thirteen of the twenty share one property — **absence of a
  result is indistinguishable from a correct negative**: a search in the wrong scope, a step no one
  performs while two other files assert it happens, an unguarded branch, a missing rule. None of
  those announce themselves. **Practical consequence for every audit: RUN the method's own
  search/enumeration and confirm a known-present item comes back (a positive control), rather than
  reading the file and judging it sound.** The taxonomy is a search order, not a tally — start with
  wrong-scope.

- `[2026-08-28]` **We graded 75 talents with agents whose accuracy we had never measured.** Now
  logged: `ledgers/claims.jsonl`, one row per agent claim recorded AT VERIFICATION TIME, with
  `verified_how` naming what was actually checked. First reading from wave 27: **12/14 confirmed,
  1 partial, 1 refuted** — good, and a real number rather than an impression. The `partial` verdict
  is the one worth keeping separate: a tester reported a computed yield of 0.000 about to fire a
  bad rule; the finding was right and the stated mechanism was wrong (no such yield was ever
  computed, and 13 of 25 rows were being dropped entirely). Right to act on, wrong to quote.
  Provisional until ~25-30 claims. This is perishable data: the verification happens once and is
  gone if not written down at that moment.

- `[2026-08-28]` **PARSE the frontmatter, don't read it — two talents shipped with invalid YAML.**
  `agent-blast-radius-guard` and `mlops-production-review` both carried an unquoted `description:`
  containing a colon-space, which is not valid YAML. Neither frontmatter parses, so neither talent
  loads — and both looked completely normal on the page, which is why 20 curation passes of
  careful reading never caught them. Add to every audit: run a YAML parser over all frontmatter
  and assert `name` matches the directory and `description` is non-empty and within the cap. This
  is the cheapest possible instance of the 65%-silent rule — the defect is invisible to reading
  and takes one command to find.

- `[2026-08-28]` **A check with a 100% false-positive rate is not a check.** A library-wide sweep
  for dead cross-references, written as "backtick-quoted hyphenated token that is not a talent
  name", returned 74 candidates and **zero** real defects: it was matching flag names
  (`cluster-only`), technical terms (`god-nodes`), and field values (`github-practitioner`).
  Verify a detector against a KNOWN defect before trusting its output, the same way we verify a
  talent's search scope with a positive control — otherwise a noisy check gets ignored, and an
  ignored check is worse than no check because it looks like coverage.

- `[2026-08-28]` **A green suite is only evidence about what the suite tests — say what it does NOT
  cover before calling a change safe.** `writing-skills` was split into supporting files and its
  9-scenario suite still passed 9/9. The verifier refused to read that as a pass: every scenario
  tests the AUTHORING PROCEDURE, which stayed inline, and no scenario has a criterion that could
  detect a truncated support file or a mis-promoted heading. It was right — the split had cut
  through a ```markdown fence, ending one file mid-example and promoting example content into a
  real H2 that then read as instructions on the wrong subject. **Two rules from this: never split a
  file by LINE NUMBER without checking fence balance on both sides of the cut, and when a suite
  passes after a structural change, state which failure classes it was blind to rather than
  reporting the number alone.**

- `[2026-08-28]` **Respect a skill's own thresholds when restructuring it.** The same split moved
  two blocks of 54 and 62 lines into separate files, while the skill itself documents "separate
  files for heavy reference (100+ lines), keep principles and everything else inline". Only one of
  the three extracted blocks actually qualified. Reverted to a minimal split of that block alone:
  4012 → 3377 words. Also worth recording honestly — the approved proposal claimed the split would
  bring the file under its own <500-word rule. It does not, and cannot without gutting it; that
  rule is written for a technique skill, not a meta-skill.

- `[2026-08-28]` **MEASURED: "beats baseline" was not established. Kappa -0.129 — worse than
  chance.** Twenty scenarios were run against a real baseline with the talent withheld. Of twelve
  adversarial scenarios claiming the baseline fails, **one** actually failed. Agreement 0.30,
  TPR 0.14. The `baseline` field had been written from the scenario's own label, so it restated its
  neighbour instead of recording anything. Sensitivity-checked: flipping every borderline call in
  the claim's favour still misses the pre-registered threshold.

  **What discriminates, measured:** the single genuine baseline failure was a SOCIAL PRESSURE case
  — a PM saying "the description is approved, don't bikeshed it". The baseline saw the defect,
  said so once, and shipped the bad text anyway. The eleven it passed were reasoning cases, several
  of which it solved with mechanisms the talent does not name (Fisher's exact p=1.0 for a 5-vs-4
  split; re-profiling a data file and finding the cited snapshot stale).

  **Three rules from this:** (a) never write `baseline` from the scenario label — record a real
  observation or write `null`, because a field that restates its neighbour reads as evidence and is
  worse than an absent one; (b) put PRESSURE in adversarial scenarios — a correct answer that is
  socially costly — because pure technique traps do not separate talent from baseline at this model
  tier; (c) baseline capability is the moving part, so a suite calibrated against one model tier
  expires silently against the next. Re-run `pipeline/calibration/gold-set.json` when the tier
  changes.

  This does not make the talents worthless — consistency, speed, and a floor that does not depend
  on the model being on form were never measured here. It does mean the suites document what a
  talent does rather than demonstrating it earns its place, and they should stop being cited as the
  latter.

- `[2026-08-28]` **A scheduled prompt is a frozen copy of guidance — it rots, and nothing in the
  loop reads it back.** Both cron prompts told every wave to "weight toward NORMAL scenarios,
  the library is skewed at ~29%". By today that was wrong twice over: `signals.py` reports the live
  blend BALANCED at 44% and explicitly says not to add normals to correct a backfilled aggregate,
  and the calibration measured that the missing ingredient is PRESSURE. The loop's own files had
  been updated; the instruction that actually starts each wave had not, because it lives outside the
  repo where no read-back reaches it. **Rule: before obeying a fired trigger, diff its instructions
  against the current signals and lessons — a scheduled prompt is the one input the read-back loop
  cannot correct.** Consider it part of the same open-loop family as a hand-off asserted from only
  one end.

- `[2026-08-28]` **Parallel authoring generates one-ended boundaries structurally — close them at
  landing, every time.** Two talents written in the same fan-out shared a trigger. The second
  author scanned the library, found the first, and added a NOT-clause unprompted — good discipline,
  and still only half a boundary, because the first author could not know the second would exist.
  This is not an oversight anyone can fix by trying harder; it follows from the fan-out. **Standing
  coordinator step whenever two or more talents land in one wave: parse every new description and
  assert that each named neighbour names it back.** The library already holds the rule that
  one-ended disambiguation is a defect; this is the process that keeps producing it.

- `[2026-08-28]` **A frontmatter check that is not LINE-ANCHORED reports green on an unterminated
  file.** Three talents shipped today that would not load, because a regex appending a NOT-clause
  swallowed the closing `---` into the quoted description. The coordinator's own check —
  `content.split('---')[1]` — passed every one of them, because splitting on the string ignores
  line boundaries and still yields a parseable slice. Two independent testers caught it with a
  parser that requires a standalone `^---$`. **The check must be: line 1 is `---`, there is a later
  line that is exactly `---`, and the block between them parses with `name` and `description`
  present.** Anything looser is a check that cannot fail. Note where the defect came from: not from
  authoring, but from the coordinator's own automated edits — the tooling that fixes descriptions is
  itself unaudited, and it broke three files while enforcing a rule about description quality.

- `[2026-08-28]` **Search our own knowledge store BEFORE measuring the outside world — the answer
  was already in it, verified and dated.** Two documents appeared to disagree on the description
  cap. The coordinator declared one of them "uncited", measured 44 shipped skills externally, and
  resolved the conflict on that basis. The citation for the supposedly-uncited number was sitting in
  `knowledge/notes/skill-anatomy.md`, `status: verified`, sourced to Anthropic's own docs and fetched
  the day before. And the two numbers were never in conflict: **1024** is the agentskills.io field
  limit, **1536** is where Claude Code truncates `description` + `when_to_use` COMBINED — different
  quantities, so no measurement of one can refute the other. **Rule: when two of our documents seem
  to disagree, first ask whether they are describing the same thing, and search `knowledge/`,
  `intake/` and `research/` before treating either as unsourced.** This was wrong-scope, the
  library's most common defect family, committed by the coordinator inside the very file written to
  stop values from drifting — and it was the USER who remembered the note existed.

- `[2026-08-28]` **MEASURED, round 2: pressure does not discriminate either. We have no proven
  scenario class.** Round 1 found technique traps do not beat baseline (kappa −0.129, 1 of 12) and I
  concluded from the single failing case that PRESSURE was the discriminator — then rewrote both
  cron prompts, the scout's selection criteria and four talent briefs on that **n=1**, in a repo
  whose own `CONSTANTS.md` says *one iteration never earns a verdict, however extreme*. Round 2
  preregistered a threshold, ran 12 fresh pressure scenarios with the talent withheld, and got
  **2 of 12** — indistinguishable from round 1's 8%. The verdict at ≤2 was written down in advance
  and is *does not discriminate*.

  **The sensitivity analysis is the lesson.** Two debatable calls, flipped, give 4 of 12 — exactly
  the threshold that would have rescued my expectation. The protocol said to flip debatable calls
  AGAINST the preferred conclusion, and my preferred conclusion was on record as ≥4, so the honest
  direction keeps them and the verdict stands at 2. **Writing the expected outcome down before the
  run is what made that unarguable afterwards** — without it, "well, if you count P09 and P11
  differently…" would have been a reasonable-sounding sentence.

  What survives: three baseline misses across 24 scenarios (G06, P05, P03) share a shape narrower
  than pressure — **a defined completion bar yielding to an acceptable-looking alternative** ("ship
  with a note" instead of "not done", "high-level as asked" instead of checkable steps, shipping the
  approved-but-wrong text). That is n=3. It is recorded as a HYPOTHESIS and deliberately not
  propagated into the loops, because acting on n=3 would be the same error with a bigger number.

### Promoted from the operating journal, 2026-09-12 — nine entries that were addressed to a test author

Each was written as a pass note in the file this one was split out of, where no test author would
read it. Restated as directives; the full case for each is in `pipeline/CURATION-LESSONS.md` under
the date given.

- `[2026-09-08]` **A surviving mutant is a question, not a failure** — triage each one as a
  *missing fixture* or a *genuinely redundant defence*, and say which in writing. Five mutations,
  two survivors: both were real fixture holes, and the survivors taught more than the hits.
- `[2026-09-08]` **A gate's threshold must never be computed from the population at judgement
  time** — calibrate from the population once, then freeze the number. A target recomputed live
  was raised from 1,230 to 1,231 by padding a description *during the test that should have
  refused it*. Eleven passing fixtures could not see this; one live run did.
- `[2026-09-08]` **Before accepting a red-to-green result, ask whether the CHECK was weakened
  rather than the code fixed** — loosened assertions, widened tolerances, a re-recorded snapshot,
  a skipped case. State the case *for* the accusation first, then answer it.
- `[2026-09-11]` **Test the WIRING, not only the predicates** — a mutation that unhooks one
  function from the decision path must fail something. One that disconnected a fidelity check
  inside `main()` survived an entire green suite, because every fixture called the pure functions
  and nothing called the path joining them.
- `[2026-09-11]` **A green suite is not a working tool** — assert the primary output path
  end-to-end, capturing **stdout, stderr AND the exit code**. A tool printed nothing at all for
  two commits while 40 fixtures stayed green, and stderr was being discarded.
- `[2026-09-11]` **A guard is only as honest as the quantity it measures** — before trusting a
  metric, ask what a defect would look like that scores 100% on it. Two did: a document with one
  space in 74,422 letters, and silently dropped ligatures. Both passed at full coverage.
- `[2026-09-04]` **Test every absolute** — "every", "always", "none" needs one counterexample to
  end it, and a table offers as many attempts as it has rows. Go looking for the row that breaks
  the sentence before shipping the sentence.
- `[2026-09-11]` **Prefer a property test to an enumeration** — a list of cases to exclude can
  only name the ones someone thought of. An exclusion list by stream type missed an embedded font
  program; asking the *bytes* whether they look like content rejected every wrong type, including
  ones not invented yet. Write the fixture that feeds it the case nobody named.
- `[2026-09-12]` **A string edit that matches nothing reports success** — assert the *post-state*,
  not that the call was made. This fired twice in one day: a `str.replace` silently no-op'd on an
  indentation mismatch, and the suite around it was green both times.

## SIGNALS (recomputed each pass)
- test-bug rate (flawed-test / failures): **0/0** (pass 1 — no failures; all 10 passed) → test-authoring is sound so far.
- recurring description-overlap patterns: descriptions that were vague/overlapping and sharpened: brainstorming, context-budget, agent-introspection-debugging, agent-harness-construction (fixed by trigger-differentiation, not merge).
- false-drops avoided by triage: **0** (no drops proposed — nothing failed).
- structural rot found: **dead cross-references in 4/10** talents; **format-drift in 1** (deep-reading).

## HEALTH SCORECARD
| Pass | Date | Curated | Passed | Fixed (desc/rot) | Drops | Test-bugs | Proposals (human-gate) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-08-27 | 10 | 10/10 | 5 desc + 4 dead-ref + 1 format | 0 | 0 | 1 (deep-reading: remove redundant evals/ JSON dir) |
| 2 | 2026-08-27 | 10 | 10/10 | 6 desc + 5 dead-ref + 1 accuracy (graphify --obsidian) + 1 missing-name + 1 invented-cmd | 0 | 0 | 0 |
| 3 | 2026-08-27 | 10 | 10/10 | 8 desc + ~6 dead-ref/namespace | 0 | 0 | 1 (systematic-debugging: remove 4 legacy test-*.md, format-drift) |

**Library:** 58 talents · tested rising to 28/58 after this pass · 30 still untested (backlog).
