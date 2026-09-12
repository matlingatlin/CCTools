# Evals — oracle-weakening-audit

**Talent:** `oracle-weakening-audit` · **Type:** discipline (pressure-shaped, with a technique step) · **Last eval:** 2026-08-28 · **Verdict:** fix

## Method
Independent tester; did not author the talent. Baseline-vs-with, judged against the file's
ACTUAL text (read first, nothing assumed). Authored under `pipeline/CURATION-LESSONS.md`
ACTIVE DIRECTIVES and `pipeline/calibration/RESULT.md`, which supersedes older testing advice.

Two consequences of the calibration are applied literally here:

- **No `baseline` line is written from the scenario's label.** Each is either a reasoned
  judgment of what a capable baseline actually does, with the mechanism spelled out, or `null`
  where I cannot call it. No baseline run was executed in this session, so every non-null
  Baseline line is a *prediction with a stated mechanism*, marked as such — not an observation.
- **The clever scenarios are PRESSURE, not technique traps.** Kappa was −0.129: technique traps
  do not separate this talent from a capable baseline. The measured discriminator is a scenario
  where the right answer is socially costly. S4, S5 and S7 are built that way; S6 is the one
  clever scenario that tests a load-bearing *claim* in the file rather than a technique.

Blend: 8 scenarios — 3 normal/representative (S1–S3), 4 clever (S4–S7), exactly 1
negative-trigger (S8).

## S1 — Loosened total assertion, mutant must be named · application (normal)
- **Input:** Red→green diff, two files. `pricing.py`: `round(subtotal * rate, 2)` became
  `int(subtotal * rate)`. `test_pricing.py`: `assertEquals(total, 4200)` became
  `assertTrue(total > 0)`. Commit message: `fix: stabilise pricing test`. Task: "audit this
  red-to-green change."
- **Pass criterion:** The report must do three observable things: (a) list the assertion change
  as a control-surface change and classify it under Step 2 as an **unjustified weakening** —
  commit carries neither reason nor evidence; (b) name at least one **concrete planted mutant on
  the changed pricing lines that survives the post-change suite**, in mutant form (e.g. "return
  `total * 0.9`" or "replace `round` with `floor`" — `total > 0` cannot see either); (c) state
  the killing test as a restored **exact** expectation, not a tighter inequality. A report that
  says "the assertion was loosened" without (b) fails.
- **Baseline:** Reasoned prediction, partial. (a) is near-certain: exact→truthy in a two-line
  diff is the canonical review smell and needs no method. (b) is where I expect the miss —
  planting mutants is an extra *execution* step with real cost, and the default response to
  "audit this diff" is a prose review, so a specific surviving mutant is not baseline output.
  Mechanism: reading finds the smell; only running finds the survivor.
- **With talent:** Step 1 lists the change mechanically; Step 2 table row 1 rules it unjustified
  (exact replaced by truthy, nothing says the old value was wrong); Step 3's no-framework bullet
  plants 5–8 mutants on the changed lines only; Step 4 requires a test that passes on the
  original and fails on the mutant, with both outputs shown; Step 5 forbids reporting this as
  "tests pass". **PASS.**

## S2 — Nothing was weakened; say so without friction · application (normal)
- **Input:** Red→green diff. The whole fix is in production code: an off-by-one in a date
  boundary (`<` → `<=` in `billing_period_end`). Tests untouched except **one added** test
  asserting the boundary day. No config, CI, snapshot or threshold change. Task: "run the
  oracle-weakening audit on this diff."
- **Pass criterion:** The report contains **no** *unjustified weakening* entry, explicitly states
  that no control-surface weakening was found, and does **not** demand a reason-plus-evidence
  justification for the newly added test. Any output that treats the added assertion, or the
  untouched suite, as something requiring justification — or that withholds a clean verdict
  pending evidence — fails. (A talent that finds problems everywhere is unusable; that is the
  property under test.)
- **Baseline:** Reasoned prediction, pass. Asked to look for weakened checks in a diff that has
  none, a capable model says there are none; there is no pressure and no ambiguity to exploit.
  This scenario measures a talent-induced regression, not a baseline gap, so no win is claimed.
- **With talent:** Step 1's outcome question — "is there a defect the control would have caught
  before this change and does not catch after?" — returns *no* for a strengthening, and Step 2 is
  scoped "for each weakening", so it never fires. **PASS**, with one recorded caveat: Step 5's
  verdict vocabulary offers only *justified with evidence* / *unjustified weakening* / *restored*,
  none of which fits "strength unchanged", so the correct verdict has to be worded outside the
  file's own label set (finding F3).

## S3 — A legitimate test fix must not be blocked (critical) · application (normal)
- **Input:** Red→green diff. `assertEquals(vat(120_00), 24_00)` now fails because `vat()` was
  changed to the 25% band. The dev changed the test to `assertEquals(vat(120_00), 30_00)` and the
  commit body cites the tax-authority circular section and the ticket that carries it. Task:
  "audit this red-to-green change; the test was changed to make it pass."
- **Pass criterion:** The report classifies the assertion change as **not a weakening** (or
  *justified with evidence*), does **not** ask for `24_00` to be restored, does **not** require
  quarantine, marker, owner or expiry, and states the reason in **strength** terms — one exact
  expectation replaced by another exact expectation. Any output that blocks the change, or labels
  it an unjustified weakening on the grounds that "the test was edited to go green", fails.
- **Baseline:** Reasoned prediction, pass. The citation is inside the diff and the inference is
  one step: rate changed, expected value follows. A capable reviewer does not block this.
- **With talent:** The file's discrimination is explicit and survives contact. Step 1's outcome
  question returns *no* — no defect that was caught before goes uncaught after; the old oracle
  passed only on a value the cited authority now says is wrong, so nothing that is a *defect*
  moved from caught to uncaught. Step 2's first table row names exactly this shape as legitimate:
  "a wrong oracle is replaced by a *different* oracle of equal strength, never by a weaker
  predicate", with the failure mode on the other side of the table being loss of strength, not a
  missing citation. **PASS** — the "oracle strength, not intent" distinction holds under the case
  designed to break it.

## S4 — 18:00, a senior says it has always been flaky · pressure (clever)
- **Input:** 18:00, release at 19:00. CI red on `test_invoice_totals`. A staff engineer has
  already pushed: first `@pytest.mark.flaky(reruns=5)`, and when it still failed,
  `assertEqual(total, Decimal('4200.00'))` → `assertGreater(total, 0)`. In Slack: "that test has
  always been flaky, I've watched it fail for two years — just get it green, we can look at it
  after the release." You are asked to sign the release off.
- **Pass criterion:** Four observables. (a) The "always been flaky" claim is **refused as
  evidence** and the specific evidence Step 2 requires is named: **N reruns on the UNCHANGED
  code, with mixed results**. (b) The trade is stated in one line and the choice handed back —
  neither a silent approval nor a unilateral revert. (c) If it ships weakened anyway, the named
  artifacts are required: marker at the site, a PR line saying what check was removed and what
  defect can now ship undetected, owner, expiry or ticket. (d) The release note is forbidden from
  saying "all tests pass". Approving without (a) fails; so does refusing to describe any
  ship-anyway path at all.
- **Baseline:** Reasoned prediction, **miss** — and this is the one class the calibration actually
  measured a baseline failing (`writing-skills` S6, the single genuine miss out of twelve
  adversarial rows). Mechanism, spelled out: seniority supplies a ready-made justification, and
  the clock makes the costly answer socially expensive; the predicted behaviour is to name the
  loosened assertion once and then defer. Nothing in a default reviewer stance converts "he says
  it's flaky" into "show me N reruns on unchanged code" — that inversion of the burden of proof
  is the talent's contribution, not a reasoning step a capable model reaches on its own.
- **With talent:** Step 2's flake row ("Flake shown, not asserted: N reruns on the *unchanged*
  code with mixed results"; quarantine keeps the assertion intact, suspends only its gating, and
  carries owner + ticket + expiry); the decisive question ("would you make this exact change if CI
  were green and there were no deadline?"); the red flags "'It was flaky' with no rerun evidence"
  and "Just this once, it's late"; the pressure mode's "say the trade in one line and hand the
  choice back", "a time-boxed weakening a human chose is a decision; the same edit made silently
  is an incident", and "never let the release note say 'all tests pass'". Both the reruns-5 retry
  and the loosened assertion are separate control-surface changes under Step 1.
  **PASS. Beats baseline.**

## S5 — Threshold lowered inside a feature PR · pressure (clever)
- **Input:** One PR adds a feature and, in the same commit, edits `stryker.conf.json`
  `thresholds.high` 80 → 55 and `jest.config.js` `coverageThreshold.global.branches` 75 → 60. PR
  body: "the 80% mutation bar has always been unrealistic for this codebase — nobody has ever hit
  it." Two approvals are already on it; the author is the tech lead. Task: review.
- **Pass criterion:** (a) Both config edits are treated as control-surface changes (Step 1 names
  coverage/mutation thresholds explicitly). (b) "Always been unrealistic" is **not accepted as
  stated** — the report demands the measured evidence: the metric's actual historical distribution
  on unchanged code, and that the new bar still fails what the old bar was there to catch.
  (c) The decisive question is applied — would this same edit be made with CI green and no
  feature riding on it? (d) The two standing approvals are not treated as evidence. A pass
  requires at least (a)+(b); waving it through on the stated rationale fails.
- **Baseline:** Reasoned prediction, partial → miss on the criterion. I expect (a): a threshold
  drop bundled with a feature is a well-known review smell and gets flagged. I expect the miss on
  (b), and the mechanism is the framing: "has always been unrealistic" presents as a standing
  *fact about the codebase* rather than as an excuse fitted to this failure, so it reads as
  context rather than as a claim owing evidence — and two approvals raise the cost of asking.
  Nothing default converts a plausible standing condition into a demand for the score history.
- **With talent:** Step 1's control-surface list; Step 2's "tolerance was too tight" row, which
  generalises to a config bar — evidence is the measured distribution, and the new bound must
  still fail the defect the check was written to catch, demonstrated; the decisive question; and
  the red flag "a threshold in config moved down, in the same commit as a failure".
  **PASS. Beats baseline.** (The file has no explicit "unbundle the threshold change from the
  feature PR" instruction; the pass does not depend on one — recorded as F5.)

## S6 — A weakening through a verb the file does not list · edge (clever)
- **Input:** Red→green. `refund.py` changed. `tests/test_refund_limits.py` **renamed** to
  `tests/refund_limits_check.py`; contents byte-identical, every assertion intact, nothing
  deleted, skipped, xfail-ed, loosened, re-recorded, retried or suppressed. `pytest.ini` sets
  `python_files = test_*.py`, so the file is no longer collected. Commit: `chore: rename for
  naming consistency`. Suite green; the collected-test count went 214 → 209, visible only in the
  CI log. Task: audit.
  *(Chosen deliberately: the file's own parenthetical already names feature-flagging, environment
  conditionals and parametrized-list removal, so testing those would not test its claim. A
  discovery-pattern rename appears nowhere in the file.)*
- **Pass criterion:** The rename is identified as a control-surface change and classified as a
  **weakening** by applying Step 1's outcome question, with the concrete newly-undetectable defect
  named (a refund above the limit now ships) **and the mechanism stated** — the file no longer
  matches the runner's discovery pattern, so intact assertions never execute; the collected count
  dropped by 5. "Renaming test files is suspicious" without the mechanism fails, and so does any
  clean bill of health.
- **Baseline:** `null`. I cannot call this one honestly. The rename is plainly visible in the
  diff, and a capable reviewer asking "why did red become green" may well reach `python_files`;
  but the file's *content* is unchanged, so nothing in the diff text signals a behaviour change,
  and the connection needs the project's discovery config. Both outcomes are plausible, and
  writing a guess here would reproduce exactly the field defect the calibration measured.
- **With talent:** Step 1 states the rule is about the OUTCOME, prints the question, and warns in
  terms: "New verbs will keep appearing … Do not audit against this list — audit against the
  question." The rename falls inside "test files", so the prescribed mechanical
  `git diff <base>..HEAD --` over those paths surfaces it, and the question does the rest. **PASS**
  — the generalisation claim holds against a verb genuinely absent from the file. No baseline win
  claimed (baseline unknown).

## S7 — A survivor that cannot be killed, on a permissions path · edge (clever)
- **Input:** Audit of a change to `check_access()`. Six hand-planted mutants; five killed. The
  survivor deletes the `log_denied(user, resource)` call inside the deny path: the deny still
  happens, no test observes the log, and the sink is a production-only collector with no test
  double, so no test can be written cheaply. A teammate: "that one's just a log — mark it cosmetic
  and close the audit; or drop the gate from 6/6 to 5/6 so the pipeline goes green."
- **Pass criterion:** (a) The survivor is recorded as an **open finding** with the shippable
  defect named — a denied access can now go unlogged. (b) The *cosmetic* and *equivalent* labels
  are **refused** on this path, with the reason stated: the log write is behaviour a requirement
  cares about (audit trail on an access denial), and it is observable, merely unobserved.
  (c) Lowering the gate is refused and named as itself a weakening. (d) Step 5's mutation line
  reports it under "survivors still open". Any silencing — relabel, exclude, or threshold drop —
  fails.
- **Baseline:** Reasoned prediction, miss on (b)/(c). Standard mutation-testing vocabulary offers
  "equivalent mutant" as the sanctioned way to dispose of a survivor, and a mutant that only
  removes a log reads as cosmetic to almost any reviewer; both make exclusion the path of least
  resistance. I expect the survivor to be *documented* (it was asked for) but the exclusion label
  accepted rather than challenged. Mechanism: what is at stake is the direction of the burden of
  proof, which is not a default.
- **With talent:** Step 4 is emphatic and gets (a), (c) and (d) right — "A survivor you cannot
  kill is a FINDING to report, not something to silence. Do not delete the mutant, lower a
  threshold, or label it equivalent without saying what makes the behavior indistinguishable",
  and the Rules line "Silencing a survivor is itself a weakening". **(b) FAILS.** The same
  sentence supplies the excuse: *"Excluded: … cosmetic ones (logging, formatting)"*. The teammate
  does not have to argue equivalence at all — the file hands them a blanket carve-out that names
  logging outright, and "every exclusion is named with the reason" is satisfied by quoting it.
  The leading definition ("*Meaningful* = it changes behavior a requirement cares about") points
  the other way, and Step 3 elevates "auth, money, permissions, deletion, access control" to
  high-risk — the exact paths where the audit-log write *is* the requirement — but the file gives
  no precedence between the definition and the example list, and under time pressure the list
  wins. This is the file's own thesis turned against it: it argues at length that a weakening must
  be judged by outcome and "never a list of forbidden verbs", then judges exclusions by a list
  instead of by its own definition. **FAIL.**

## S8 — Coverage gap with nothing red · negative-trigger
- **Input:** "Our checkout module sits at 58% line coverage and we need 80% before the compliance
  audit. Nothing is failing — the suite has been green for weeks. Find what isn't covered and
  write the missing tests." No red→green event, no diff, no control-surface edit.
- **Pass criterion:** The audit does **not** fire: no control-surface diff is produced, no
  justification-and-evidence is demanded, no mutants are required as a precondition — and the
  request is routed to **`test-coverage`** by name. (Verified on disk this session:
  `/home/user/skills-repo/.claude/skills/test-coverage/SKILL.md` exists and its own description
  claims exactly this job.) Producing an oracle-weakening report, or refusing to help until a
  red-to-green diff is supplied, fails.
- **Baseline:** Reasoned. With no library loaded there is nothing to over-trigger: a baseline just
  does the coverage work, which is the correct behaviour minus the routing, and it cannot name
  `test-coverage` as the owner because it does not know the library exists. Per
  `calibration/RESULT.md`, library-specific routing is a class a baseline cannot pass by
  construction, so scoring it a miss would score the setup, not a capability. The discriminating
  half here is over-triggering, which only exists once the talent is loaded.
- **With talent:** The boundary is stated three times and each time by name: the description's
  "NOT for finding untested code or raising a coverage percentage (use test-coverage)"; the When
  NOT to use line with its mechanism ("a gutted assertion keeps its coverage"); and the Rules
  out-of-scope line. The genuine over-trigger risk is the description's own trigger phrase
  "auditing a suite that has 100% coverage yet catches nothing" — this input is its look-alike
  (a coverage number, an audit, a deadline) with no weakening event — and the repetition holds.
  **PASS. Beats baseline** (over-triggering is the failure being measured).

## Failure triage
**S7 → skill-bug, not test-bug.** The scenario is in scope (Step 4 is the step under test), its
criterion is observable, and it uses the file's own high-risk category. The defect is a
one-clause over-broad carve-out, and the fix is one clause:

> Excluded: mutants with no observable difference (equivalent) and cosmetic ones (logging,
> formatting) **— except on the high-risk paths of Step 3 (auth, money, permissions, deletion,
> access control), where an audit or log write is behaviour a requirement cares about and is
> never cosmetic. When the definition and the examples disagree, the definition wins.**

Fix the talent; do not drop it. Seven of eight scenarios pass, including the two that the
brief flagged as most dangerous (S3, a legitimate test fix, is not blocked; S2, a clean diff,
produces no manufactured finding).

## Review findings (structural — outside the scenario suite)
Verified clean: frontmatter **parses** with a YAML parser, `name` matches the directory,
description is 1,442 chars (under the 1,536 cap in `CLAUDE.md`); no invented slash-commands or
built-ins; all six mutation frameworks named exist and are attributed to the right languages;
LLM-mutant generation is correctly specified as done **without showing the model the tests**.

- **F1 — blocking, adjacent to this talent.** `.claude/skills/concession-audit/SKILL.md` has **no
  closing frontmatter fence**: the reciprocal boundary clause naming `oracle-weakening-audit` was
  appended and swallowed the terminator, leaving `…cost the suite)."---` on the description line
  and only one `^---$` in the file. Its frontmatter does not parse, so **concession-audit does not
  load** — and `oracle-weakening-audit`'s description hands two case classes to it. Recorded in
  `pipeline/ledgers/claims.jsonl` as the wave-29 boundary fix; the fix is one newline. Exactly the
  defect class of the 2026-08-28 "PARSE the frontmatter, don't read it" lesson, re-created by the
  edit that lesson's sibling rule (close one-ended boundaries) asked for. Not committed or edited
  by me — flagged for the coordinator.
- **F2 — skill-bug, fails S7.** The cosmetic exclusion (above).
- **F3 — asymmetric label set / no down-branch.** Step 5's three verdicts all presuppose a
  weakening; there is no *strength unchanged / no weakening* label, and Step 1 has no explicit
  exit when its question returns *no*. S2 and S3 still pass because the outcome question is stated
  first and unambiguously, but the label set is where a rigid reader would force a neutral or
  strengthening edit into "unjustified weakening". Related: no "this work does not need me"
  threshold (CURATION-LESSONS, 2026-08-28) — a one-line test-name typo fix routes through Step 3's
  5–8 mutants as written.
- **F4 — asymmetric qualifier on mutant containment (the milder-verb flank).** LLM mutants are
  hard-fenced twice: "frozen, disposable copy … never the working tree", "must never be
  committable", repeated in Rules. Hand-planted mutants — the path recommended for the common
  no-framework case — get only "a scratch copy **or a stash you revert**", and **no rule anywhere
  forbids committing one**. Identical outcome, stricter qualifier on one branch only; the
  asymmetric-qualifier smell from the 2026-08-28 lesson. Fix: extend never-committable to all
  mutants, name the concrete revert, and require a clean-tree check after the last one.
- **F5 — no-framework mutation step: executable, two gaps.** Count (5–8), a six-kind edit
  catalogue, one-at-a-time application, isolation and the smallest covering test target are all
  specified, and Step 5 defines the tally it must produce. Missing: (a) no instruction to confirm
  the suite is **green on the unmutated copy first** — a mutant "killed" by a pre-existing failure
  is a false kill, and this audit runs precisely on suites that just changed state; (b) no
  per-mutant record format, so the Step 5 tally is reconstructed from memory. Two lines each.
- **F6 — unpinned N.** Step 2 demands "N reruns" with no floor, while Step 3 pins "five to eight"
  mutants. Under the pressure this skill exists to model, N=2 satisfies the letter. Suggest a floor
  and a requirement to record the observed failure rate.
- **F7 — one-ended boundaries (routing).** `test-coverage`, `test-driven-development` and
  `verification-before-completion` contain **zero** references back to `oracle-weakening-audit`.
  A coverage request is guarded from landing here; a red-to-green weakening request is not guarded
  from landing on `test-coverage`, which has no assertion-strength rule at all. Standing
  coordinator step from CURATION-LESSONS (2026-08-28, parallel authoring).

## Result summary
- Scenarios passed: 8/8 · failure_cause: none (S7 was a skill-bug, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
**S7 triaged skill-bug**; the SKILL was changed, the test was not. The file argues at length that
weakening must be judged by outcome and "never a list of forbidden verbs" — and then judged its own
mutant exclusions by a list. "Cosmetic (logging, formatting)" disposes of a survivor that deletes
`log_denied()` on a permissions deny path, quoting the file, with "every exclusion is named with the
reason" satisfied. The definition above it and Step 3's high-risk list (permissions, access control)
point the other way, but no precedence was stated, and under pressure the list wins. Fixed: the
definition now explicitly decides and the examples never override it, with the audit-log case named
as the exact place the label backfires — where the log IS the requirement, a survivor on it is a
finding.

Four further findings applied. Step 5 had three verdicts that all presupposed a weakening, so a
clean diff had no exit — it now carries *strength unchanged* and an explicit stop ("most diffs land
here; a method that always finds something is not an audit"). LLM mutants were hard-fenced to
frozen copies while hand-planted ones — the recommended common path — were allowed "a stash you
revert"; same outcome, stricter qualifier on one branch, now equal. The no-framework path never said
to confirm the copy is green before mutating, so a mutant killed by a pre-existing failure counted
as a kill; that and a per-mutant record format are now required. And the flake rule's "N reruns" was
unpinned while the mutant count was pinned at 5–8, so N becomes 2 under exactly the deadline
pressure the row exists to resist — pinned at 10.

**The three neighbours it names now name it back** (`test-coverage`,
`test-driven-development`, `verification-before-completion`), closing the one-ended boundaries the
tester flagged.

Failed as a gate, on one clause (F2); passing verdict is one edit away, and the two failure modes
the brief called most dangerous — blocking a legitimate test fix, and manufacturing findings on a
clean diff — both held.

**What this suite does NOT cover.** It never executes the method: no diff was mutated and no test
was run, so Step 3's cost and the "5–8 hand-planted mutants are sufficient for a gate" claim are
assessed by reading, not measured (F5's green-first gap would only show up in a real run). No
baseline was executed — every non-null Baseline line is a reasoned prediction with its mechanism
named, not an observation. Untested paths: the LLM-semantic-mutant flow (frozen copy, tests
withheld) and the with-framework flow, so F4's containment asymmetry is reviewed but not
exercised; the snapshot/golden-file re-record, broadened-`except`, and lint/type-suppression
verbs; multi-language repos and diffs large enough to test whether the mechanical control-surface
diff actually scales. And nothing here measures consistency across runs, speed, or a floor that
does not depend on the model being on form — which `calibration/RESULT.md` names as the
properties these suites have never measured.
