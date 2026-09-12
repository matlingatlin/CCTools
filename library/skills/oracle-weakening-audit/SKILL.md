---
name: oracle-weakening-audit
description: "Use when a suite went from red to green and the change landed on the CHECK rather than on the behavior — an assertion loosened from an exact value to a truthy, non-null or existence check, a numeric tolerance widened, a test deleted, skipped, xfail-ed or quarantined, an except/catch broadened, a lint or type suppression added, a snapshot or golden file re-recorded, a retry count or timeout raised until it passed, a coverage or mutation threshold lowered in config, or test data swapped for an easier case. Triggers: 'just get it green', 'CI is red before the release', 'that test was wrong', 'it's flaky, skip it', 'I relaxed the assertion', 'green build but did we weaken anything', reviewing an agent's or a colleague's red-to-green diff, auditing a suite that has 100% coverage yet catches nothing. Grades whether the surviving checks still FAIL on a deliberately broken version of the changed code. NOT for finding untested code or raising a coverage percentage (use test-coverage), NOT for the write-the-test-first ordering of new work (use test-driven-development), NOT for the duty to run the command and read real output before claiming success (use verification-before-completion — that gate is fully SATISFIED by an honestly green run of a gutted suite), and NOT for holding a stated finding that a person is pressuring you to drop (use concession-audit — that judges a position in a conversation; this judges checks in a diff)."
---

# Oracle Weakening Audit

A green suite proves the checks passed, not that the checks can still fail. This audit finds
green that was bought by weakening the oracle instead of fixing the code, and proves the
remaining suite still kills a planted defect. Language- and framework-neutral.

## When to use
- Red became green and the diff touches tests, test config, CI config, or error handling.
- Someone (you, an agent, a teammate) was told "just get it green" before a deadline.
- A suite reports high line coverage but nobody trusts it.
- Reviewing agent-written code: the model both wrote the code and owns the tests that judge it.

**When NOT to use:** you want to find code no test reaches (`test-coverage` — reachability;
a gutted assertion keeps its coverage); you are writing new code and want the test first
(`test-driven-development` — authoring order, not later erosion); you are about to claim
"done" and must run the command first (`verification-before-completion` — that duty is fully
met here, which is exactly why this audit exists); the thing under pressure is a position you
stated in a conversation rather than a check in a diff (`concession-audit` — pair them when a
weakening is being argued for: that one decides whether to hold, this one measures what the
edit costs the suite).

## Steps

1. **Diff the CONTROL SURFACE, not the code.** List every change to anything that decides
   pass/fail: test files, assertions, fixtures and test data, test config, coverage/mutation
   thresholds, lint and type-checker config and inline suppressions, CI job definitions,
   snapshots and golden files, retry/timeout settings, and the production `try/except` blocks
   that swallow errors a test used to see. Get it mechanically — `git diff <base>..HEAD --`
   over those paths — so nothing hides in a large change.

   **The rule is about the OUTCOME, not the verb.** For each control-surface change ask one
   question:

   > **Is there a defect the control would have caught before this change and does not catch after?**

   If yes, that is a weakening — whatever it was called. Deleting, skipping, xfail-ing,
   loosening, widening, re-recording, retrying, suppressing, and lowering a threshold are
   examples that happen to be common, not the definition. New verbs will keep appearing
   (a stronger check moved behind a feature flag, an assertion made conditional on the
   environment, a case removed from a parametrized list); they are covered by the same
   question. Do not audit against this list — audit against the question.

2. **Demand a justification and evidence for each weakening.** Legitimate weakenings are
   real: a test can assert the wrong thing, a tolerance can be tighter than the system's true
   noise floor, a genuinely flaky test can need quarantine. Each one is allowed here — but it
   must carry, in the commit or PR, both a **reason** and **evidence**:

   | Claim | Evidence that makes it legitimate | The same edit without it |
   |---|---|---|
   | "The test was wrong." | The authority that says so — spec line, requirement, upstream doc, issue — AND the corrected test still asserts an EXACT expectation. A wrong oracle is replaced by a *different* oracle of equal strength, never by a weaker predicate. | An exact check replaced by a truthy/existence check. Strength dropped; nothing says the old value was wrong. |
   | "The tolerance was too tight." | The measured distribution the tolerance is derived from (N runs, spread), AND the new tolerance still fails the defect the test was written to catch — demonstrated. | A bound widened until this run fits under it. Fitted to the failure, not to the noise. |
   | "It's flaky." | Flake shown, not asserted: **at least 10 reruns** on the *unchanged* code with mixed results — pinned, for the same reason the mutant count is, because an unpinned N becomes 2 under exactly the deadline pressure this row exists to resist. Quarantine keeps the assertion intact and suspends only its gating, and carries owner + ticket + expiry. | Deleted or `skip`-ed, permanently, unowned. |

   Decisive question when the claim is unclear: **would you make this exact change if CI were
   green and there were no deadline?** No → it is fitted to the failure, not to the truth.

3. **Mutate the CHANGED code only.** Cost is the reason mutation testing gets skipped, so
   scope it: mutate the lines and functions in this diff, never the repository.
   - **With a framework**, point it at the changed files: Stryker (JS/TS, .NET, Scala),
     PIT (JVM), mutmut or cosmic-ray (Python), cargo-mutants (Rust), go-mutesting (Go),
     Infection (PHP). Run the smallest test target that covers those files.
   - **With no framework, plant mutants by hand — this is sufficient for a gate.** Five to
     eight edits on the changed lines: flip a boundary (`<` → `<=`), negate a condition,
     return a constant / empty / null instead of the computed value, off-by-one a literal,
     delete a call with a side effect, invert or swallow an error path. Apply one at a time
     in a scratch copy you delete afterwards — never the working tree, and never a commit; the same fence the LLM-generated mutants get, for the same reason: a mutant that survives into history is a defect you planted yourself; run only the tests covering that code.
   - **Semantic (LLM-generated) mutants only for high-risk changed paths** — auth, money,
     permissions, deletion, access control. Generate them from the requirement **without
     showing the model the tests**, then **apply them only to a frozen, disposable copy of
     the file — never the working tree**. Require the copy compiles, run the smallest green
     suite, then delete the copy. A mutant must never be committable.

4. **Apply the gate rule.** State it as an observable line, per mutant:

   **Before mutating anything, confirm the copy is GREEN before you mutate it.** A mutant "killed"
   by a failure that was already there is a false kill, and it makes the whole tally meaningless.
   Record per mutant: what you changed, which test failed (or none), and killed/survived.

   > **For every surviving meaningful mutant, add a test that PASSES on the original and FAILS on the mutant — and show both outputs.**

   *Meaningful* = it changes behavior a requirement cares about. **The definition decides; the
   examples below never override it.** A mutant is excluded only when you can say which requirement
   is indifferent to it — not because it falls under a convenient label.
   Usually excluded: mutants with no observable difference (equivalent), and formatting or logging
   changes where no requirement depends on the output. **But logging is exactly where this
   backfires:** deleting the `log_denied()` call on a permissions deny path is a "logging" mutant
   by label and an audit-trail defect by requirement, and Step 3 lists permissions and access
   control as high-risk for that reason. Where the log IS the requirement — audit trails, security
   events, compliance records, anything someone will later need as evidence — a surviving mutant on
   it is a finding, not a cosmetic exclusion. This file argues that weakening must be judged by
   outcome and never by a list of forbidden verbs; the same applies to its own exclusion list, and
   every
   exclusion is named with the reason, not waved through.

   **A survivor you cannot kill is a FINDING to report, not something to silence.** Do not
   delete the mutant, lower a threshold, or label it equivalent without saying what makes the
   behavior indistinguishable. "We could not kill this; here is the defect that can ship" is
   a valid, useful outcome.

5. **Report the verdict.** Per control-surface change: *strength unchanged* / *justified with
   evidence* / *unjustified weakening* / *restored*.
   **If step 1's question returns "no" for every change, stop here and say so in one line** — the
   controls are as strong as they were, no mutation run is needed, and this method is done. Most
   diffs land here. A method that always finds something is not an audit; running the ceremony on
   a diff that weakened nothing costs time and trains people to ignore the result. Plus the mutation line: mutants planted, killed,
   survived, survivors killed by new tests, survivors still open. Never describe a run as
   "tests pass" when a check was relaxed in the same change — the honest phrasing names the
   relaxation: "passes after loosening the total assertion."

## The pressure mode — name it out loud

Calibration of this library measured one thing that reliably beats a capable reviewer:
**social pressure.** Not missing technique. "Just get it green before the release" *is* that
pressure, and under it the cheapest green is always a control-surface edit — one that then
passes every other checklist honestly, because the suite really was run and the output really
was green.

When you are the one under it:
- **Say the trade in one line and hand the choice back.** "This goes green in two minutes by
  loosening the total assertion; that removes the check for wrong totals. Fixing the code is
  ~40 minutes. Which do you want?" Stating the trade needs no permission.
- **A time-boxed weakening a human chose is a decision; the same edit made silently is an
  incident.** If it ships weakened, it carries a marker at the site and a line in the PR:
  what check was removed, what defect can now ship undetected, owner, and expiry or ticket.
- **Never let the release note say "all tests pass"** when the honest sentence is "all tests
  pass after we stopped checking the total."

## Red flags — stop and run this audit
- The only edits that turned red into green are in test or config files.
- An assertion lost an exact expected value.
- "It was flaky" with no rerun evidence.
- A threshold in config moved down, in the same commit as a failure.
- A `catch`/`except` got wider next to a failing test.
- A snapshot was re-recorded without anyone reading the diff.
- Retries or timeout raised until the run stayed green.
- "Just this once, it's late."

## Example
**Before:** 18:00, release at 19:00. `assertEquals(total, 4200)` fails and looks flaky. The
instruction is "just get it green." It becomes `assertTrue(total > 0)`, a neighbouring test is
`@Skip`-ed, the build is green, and every completion checklist is satisfied.

**After:** Step 1 flags two control-surface changes with no evidence — an exact oracle replaced
by a truthy one, and a skip with no rerun log. Step 3 plants four mutants on the changed
pricing lines; the one returning `total * 0.9` **survives** — `total > 0` cannot see it. Step 4
requires a test that passes on the original and fails on that mutant, which restores the exact
`4200` expectation. Root cause: a rounding change, one line, twelve minutes. Reported as: "the
assertion was hiding a real 10% pricing defect," not as "flaky test fixed."

## Rules
- Judge the outcome (a defect that now goes undetected), never a list of forbidden verbs.
- A weakening is allowed only with a stated reason AND evidence; a correction preserves oracle
  strength, it does not trade it away.
- Mutate only changed code. LLM-generated mutants touch frozen disposable copies only — never
  the working tree, never a commit.
- Every surviving meaningful mutant is killed by a new test or reported as an open finding.
  Silencing a survivor is itself a weakening.
- This audit reads a diff, plants local edits, and runs the project's own test command. It
  installs nothing, needs no credentials, and makes no network calls.
- Out of scope: which code lacks tests (`test-coverage`), the order in which new tests are
  written (`test-driven-development`), and whether the run was actually executed
  (`verification-before-completion`).

## In this repo (one instance)
A talent's `evals.md` is its oracle. The same audit applies: a scenario whose criterion is
softened from a specific required artifact to "mentions the topic" is a weakened assertion that
keeps its row count, and a scenario deleted because the talent failed it is a skip. The
mutant here is a deliberately degraded talent output — the eval must fail on it.
