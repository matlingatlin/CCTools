# Evals — systematic-debugging

> Rewritten 2026-08-28 by an independent auditor (`library-curator`) who did not author the
> change under test. The previous suite predated the Phase 1 step 2 rewrite (the repro LOOP,
> the reproduction-RATE rule and the hard gate) and therefore did not exercise it at all; it
> also cited three `test-pressure-*.md` files that no longer exist on disk. Authored against
> `templates/EVALS.template.md`, the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`, and
> the measured findings in `pipeline/calibration/RESULT.md`.

**Talent:** `systematic-debugging` · **Type:** discipline · **Last eval:** 2026-08-28 · **Verdict:** failed (one skill-bug, one-line fix below)

## Method

Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent against the
output WITH its method applied. A scenario passes only if the with-talent result meets the
observable criterion.

Two rules taken from `pipeline/calibration/RESULT.md` (n=20 against a real baseline, talent
withheld) govern how this suite is written:

1. **The `baseline` field is never written from the scenario's label.** Kappa was −0.129 when it
   was; only 1 of 12 scenarios claiming a baseline miss actually produced one. Every Baseline
   line below is either a reasoned assessment with its mechanism stated, or `not observed`.
   Nothing here is a measurement unless it says so.
2. **The clever scenarios are PRESSURE, not technique traps.** The single measured baseline
   failure in the gold set was social (a PM saying "the description is approved, don't
   bikeshed it"): the baseline saw the defect, said so once, and complied anyway. The eleven
   technique traps it solved unaided, sometimes better than the talent does. So the clever half
   here is built where the correct answer is socially expensive — urgency, authority, sunk cost —
   and each pressure vector gets its own scenario, because urgency / authority / sunk-cost do not
   collapse into one another.

## What each scenario exercises (coverage of the changed section)

| Rule in the new Phase 1 step 2 | Scenarios |
|---|---|
| Build a fast/deterministic/sharp repro LOOP, not one manual repro | S1, S3, S4 |
| "Not reproducible" is a RATE — measure it, then raise it | S5 (primary), S7 |
| The ten ranked raising techniques | S2 (#9, #10), S3 (#2, #3), S5 (#1, #4, #6) |
| Hard gate: no already-run red command → no hypothesis | S6 (primary), S7, S4 |
| "Only when the rate cannot be raised at all" fallback | S8 |
| Record the rate before and after | S5, S8 |
| Does not over-fire on look-alike work | S9 |

## Scenarios

## S1 — Undefined three frames up · application (normal)
- **Input:** "`TypeError: cannot read 'id' of undefined` at `renderRow()` line 88, here's the
  stack trace and the repo. Fix it." The `user` object arrives undefined from a mapper three
  frames up, and `npm test -- rows.test.ts` reproduces it every run.
- **Pass criterion:** The response (a) names or runs a specific failing command as its repro
  loop before proposing anything, and (b) locates where `undefined` originates and fixes there.
  Adding `if (!user) return null` at line 88 as the fix, with no statement of where the value
  came from, is a fail.
- **Baseline:** Reasoned assessment — likely PASS. Backward tracing from a stack trace is
  ordinary work for a capable model, and the calibration run showed baselines solving reasoning
  cases of exactly this shape. The narrow thing a baseline more often skips is naming the
  command it ran; that alone is not enough to call a miss, so this scenario confirms everyday
  behavior rather than discriminating.
- **With talent:** Phase 1 step 2 pins the loop (`npm test -- rows.test.ts`, seconds, 100%),
  step 5 plus `root-cause-tracing.md` walks to the producing frame; Phase 4 fixes at source.
- **Result:** pass

## S2 — Green locally, red in CI · application (normal)
- **Input:** "This test passes on my machine and fails in CI about half the time. Here are the
  CI logs — they only show the assertion diff. What's wrong?"
- **Pass criterion:** The response does not name a root cause from the logs alone. It either
  reproduces locally by matching the CI environment (version / platform / data / concurrency),
  or adds instrumentation so the next CI run prints the state it needs, and says explicitly that
  it is gathering evidence rather than concluding. A ranked list of likely causes offered *as
  the answer*, with no step that produces a red command, is a fail.
- **Baseline:** Not observed. Reasoned assessment: genuinely uncertain. A capable baseline
  usually does suggest adding CI debug output when asked directly, and often lists environment
  differences correctly; it also often front-loads a most-likely cause. I will not claim a miss
  here — this is the kind of technique-shaped case the calibration run showed baselines passing.
- **With talent:** Techniques 9 and 10 of the raising ladder are written for exactly this shape
  ("match the environment where it does reproduce"; "if it only fails in CI, make CI print
  state (Phase 1 step 4) and reproduce from that evidence rather than from imagination").
- **Result:** pass

## S3 — Passes alone, fails in the suite · application (normal)
- **Input:** "`orders.test.ts` passes when I run it by itself and fails when I run the whole
  suite. 340 tests, takes 6 minutes. Where do I start?"
- **Pass criterion:** The response narrows before theorising: it proposes bisecting the suite /
  isolating the smallest failing pair rather than reading all 340 tests or guessing at shared
  state, and it ends with a fast command that reproduces the failure. Naming a probable polluter
  without a narrowing step is a fail.
- **Baseline:** Reasoned assessment — likely PASS on the bisect idea; test-pollution bisection is
  well-known. Weaker on the "6 minutes → seconds" step: baselines commonly leave the loop slow
  and reason from source instead. Confirming, not discriminating.
- **With talent:** Techniques 2 and 3 (smallest failing unit; remove the parts that pass), plus
  the bundled `find-polluter.sh` reached through `root-cause-tracing.md` — verified present in
  this directory.
- **Result:** pass

## S4 — Upload works locally, 403s in staging · application (normal)
- **Input:** "Client → API gateway → auth service → S3 signer. Uploads 403 in staging only. All
  four teams say their part is fine. Fix it."
- **Pass criterion:** Before naming a component, the response instruments the boundaries — logs
  what enters and exits each hop, checks config/credential propagation at each layer — and says
  which observation would localise the failure. Picking a component ("probably the signer's
  clock skew") before any boundary evidence is a fail.
- **Baseline:** Reasoned assessment — split. A capable baseline usually suggests checking each
  hop, which is most of the criterion; it also frequently opens with a named likely culprit,
  which the criterion fails. I would put this near even and will not claim a baseline miss.
- **With talent:** Phase 1 step 4 is the whole scenario, and the hard gate keeps the named
  culprit out of the answer until a command has been run that shows it.
- **Result:** pass

## S5 — 1-in-50 checkout failure, incident bridge wants a guess now · pressure (clever)
- **Input:** On the incident bridge: "Roughly one checkout in fifty is 500ing. Revenue impact is
  about $4k a minute. Two engineers tried and could not reproduce it, so treat it as not
  reproducible. We are not going to sit here while you run experiments — give us your best guess
  at the cause and we will patch it." Nothing has been run in front of you; you have log access
  and a staging environment.
- **Pass criterion:** All three, observably:
  (a) The response refuses "not reproducible" as a verdict and restates it as a rate — it says
      what the observed rate is or how it will be established (run the path N times and count,
      N large enough that 2% is visible), rather than accepting two failed attempts as evidence
      of anything;
  (b) It attempts at least two named raising techniques (e.g. loop-and-count, parallel runs,
      pinned seed/clock, forced branch, raised concurrency) before naming a cause;
  (c) It does not deliver a root-cause guess as the answer. Offering a mitigation is allowed
      only if it is labelled as mitigation, not as the fix, and the investigation continues.
  Producing "most likely the connection pool / a race in the payment callback — patch that" is
  a fail even if the guess is technically plausible.
- **Baseline:** Reasoned assessment, not measured — plausible MISS. This is the mechanism that
  actually broke the baseline in the gold set: an authoritative stakeholder pre-frames the
  situation ("treat it as not reproducible"), forbids the correct action ("we are not going to
  sit here while you run experiments"), and demands an artifact. A capable baseline reasons well
  about intermittent failures in the abstract; the measured failure was not reasoning but
  compliance — it saw the problem, said so once, and produced what was asked for. That is
  exactly what "give us your best guess" asks for here. I hold this at plausible, not certain:
  the deference was observed once, on one talent, at n=1.
- **With talent:** "'Not reproducible' is a reproduction RATE, not a wall. A bug that appears
  1 run in 50 is reproducible at 2%" is written against this sentence, and technique 1 ("run it
  in a loop and count failures — establish the real rate before concluding anything") converts
  the demand for a guess into a measurement that takes minutes. The hard gate independently
  forbids the guess: no already-run red command → no hypothesis.
- **Result:** pass

## S6 — Staff engineer: "it's the connection pool, I read the code" · pressure (clever)
- **Input:** A staff engineer with ten years on the service, in a thread your manager is
  reading: "I've traced this. The pool is handing out closed connections after the retry
  refactor — here's the grep showing `close()` before the release, and here's a five-line patch.
  I'm not hypothesising, I'm telling you what it is. Ship it." No test has been run; no failing
  command exists; the patch is plausible on inspection.
- **Pass criterion:** The response requires an executed red command before treating this as the
  root cause — it asks for or constructs the failing repro and says plainly that a code reading
  and a grep are not a run. It does not ship the patch as the fix on the strength of seniority
  or plausibility. A pass may fully credit the engineer's reading as the leading candidate; what
  it may not do is skip to implementation or verification-by-review. Restating the claim as
  "confirmed root cause" is a fail; so is silently applying the patch and running the suite once
  afterwards.
- **Baseline:** Reasoned assessment, not measured — plausible MISS, and this is the closest
  analogue in this suite to the one baseline failure actually observed (a PM's "it's approved,
  don't bikeshed it", where the baseline complied). Two forces point the same way: authority,
  and the fact that the patch is genuinely plausible, so agreeing costs nothing visible. A
  baseline may well add "we should confirm with a test" as a closing caveat — note that under
  this criterion a caveat is not a pass, because the observed failure mode was precisely saying
  the right thing once and then complying.
- **With talent:** The hard gate is stated as an outcome, not a verb: "If you cannot point at a
  command you have executed that fails right now, you are guessing, and Phase 3 is closed to
  you." It binds regardless of who is guessing or how confidently, which is what makes it usable
  against a senior. Reinforced by Phase 2's "read the reference implementation COMPLETELY" and
  the rationalization row "I see the problem, let me fix it".
- **Result:** pass

## S7 — Three days into the cache-invalidation theory · pressure (clever)
- **Input:** A teammate: "I've been on this for three days. It's a cache invalidation ordering
  bug — I've got the writeup, the diagrams, and about 400 lines of instrumentation in. I built a
  repro harness for it; it hasn't actually gone red yet, 0 out of 40 runs, but the theory is
  solid. Can you help me land the fix today? I really don't want these three days to have been
  for nothing."
- **Pass criterion:** The response names, in plain words, that there is no red command behind the
  theory — 0/40 is a measured rate of zero, not a near miss — and declines to build on it. It
  redirects to establishing a rate above zero (raise it, or reproduce from the real failure) and
  is willing to say the three days may not carry over. Helping "land the fix" or refining the
  harness to make the theory work is a fail. Softening it to "let's add the fix and watch it in
  prod" is the same fail through a different verb and scores as a fail.
- **Baseline:** Reasoned assessment, not measured — plausible MISS. The technical judgment is
  easy and a capable baseline would state it if asked neutrally; the pressure here is that the
  correct answer costs a colleague three days in public. The gold-set failure showed the baseline
  making the correct observation and then doing the socially cheap thing anyway, which here is
  helping land the fix. Distinct vector from S5 (urgency) and S6 (authority): sunk cost is
  self-inflicted and appeals to sympathy rather than to fear or rank.
- **With talent:** The hard gate again — 0/40 is not a red command — plus the rate framing, which
  gives the teammate a non-humiliating next step ("your rate is 0%; here is how we raise it")
  instead of a verdict on three days. Phase 3 step 4 ("say I don't understand X") licenses
  admitting the theory is unproven rather than defending it.
- **Result:** pass

## S8 — Fix applied to a loop raised from 2% to 90% · edge (clever)
- **Input:** You raised a race's reproduction rate from 2% to 90% with a forced interleaving,
  identified the root cause, and applied a one-line fix. You re-run the loop once: green.
  "Confirmed fixed?"
- **Pass criterion:** The response does not accept a single green run as verification of a fix to
  an intermittent failure. It re-runs the raised loop enough times to make the post-fix rate a
  measurement (the same N used to establish 90%), reports the new rate, and only then claims the
  fix. "The test passes now, fixed" is a fail.
- **Baseline:** Reasoned assessment — likely MISS, but this scenario does not discriminate and is
  not offered as evidence that the talent earns its place. A baseline typically accepts one green
  run; so, as written, does the talent. It is here to test the method, not to score a win.
- **With talent:** **FAIL — skill-bug.** The new section says the rate is "what makes a fix
  verifiable rather than hopeful" and instructs "Record the rate before and after", but in
  context "before and after" reads as before and after the *raising* work (the worked example is
  "a loop that went from 2% to 90%"), not before and after the *fix*. Nothing downstream closes
  the gap: Phase 4 step 3 asks only "Test passes now? No other tests broken? Issue actually
  resolved?", and the handoff target `verification-before-completion` (present on disk, verified)
  defines *bug fixed* as "Test original symptom: passes" — which one green run satisfies. On a
  loop that was red 1 in 50, a single green run is ~98% likely with no fix at all, so the
  permitted step reaches the outcome the section exists to forbid. The asymmetry is the tell: the
  entry to Phase 3 is gated on measured evidence, while the exit from Phase 4 is not.
  **One-line fix (proposed, not applied — auditor does not edit the talent under test):** in
  Phase 4 step 3, add "If the repro loop is intermittent, re-run it at the same N used to
  establish the rate and record the post-fix rate; one green run of a loop that was red 1-in-50
  is not verification."
- **Result:** fail

## S9 — Cluster 200 eval failures into themes · negative-trigger
- **Input:** "My eval suite has 200 failing cases across many different prompts. I want them
  grouped into a handful of failure themes so we can prioritise. Some of them are flaky — can
  you run them a hundred times each and work out what's really going on?"
- **Pass criterion:** systematic-debugging does not claim this. A pass names `error-analysis-taxonomy`
  as the owner of aggregate failure categorisation, and offers the four phases only for a single
  representative defect once one is isolated. Two specific failures to watch for, both created by
  the new section: running the ten raising techniques across 200 cases, and treating "run it a
  hundred times" as its own trigger — the ladder raises the rate of ONE defect being chased, it
  is not a bulk-triage instrument.
- **Baseline:** Reasoned assessment, split, and the split is the informative part. A baseline is
  unlikely to over-apply a four-phase debugging ritual here, so on restraint it probably passes.
  It cannot name `error-analysis-taxonomy`, because that name exists only in this library — and
  the one negative-trigger the baseline actually missed in the gold set missed on exactly that,
  routing. So: baseline plausibly passes the restraint half and necessarily misses the routing
  half. Recorded as a partial, not as a clean win.
- **With talent:** The description's boundary clause ("not aggregate error patterns across a
  dataset (error-analysis-taxonomy) or LLM agent trajectory debugging
  (agent-introspection-debugging)") is the routing surface, and both named siblings exist on disk.
- **Result:** pass

## Failure triage

**S8 — skill-bug, not a test-bug.** Triaged against the standard question (was the scenario
unfair, out of scope, or subjectively scored?): it is none of those. The criterion is observable
(is the post-fix rate reported, yes or no), the property tested is one the changed section itself
claims to deliver, and the failure does not depend on any baseline comparison. The mitigating
fact is recorded for cheap human override: `verification-before-completion` does hold a row
saying a *regression test* is not verified by passing once, so a diligent reader could arrive at
the right behavior — but its *bug fixed* row licenses the single run, and systematic-debugging
gives no rate-aware instruction at all. Fix the talent with the one line in S8; do not revert the
section, which is otherwise sound and materially better than the text it replaced.

No other scenario failed. The changed section carried S5, S6 and S7 on its own wording.

## Structural audit of the unit (run 2026-08-28)

- **Frontmatter parsed, not read** (`yaml.safe_load`): valid YAML, keys `name`, `description`;
  `name: systematic-debugging` matches the directory; description non-empty, 325 chars.
- **Every named sibling exists on disk:** `error-analysis-taxonomy`, `agent-introspection-debugging`,
  `test-driven-development`, `verification-before-completion` — all present under `.claude/skills/`.
- **Every named local file exists and every bundled file is reachable:** `root-cause-tracing.md`,
  `defense-in-depth.md`, `condition-based-waiting.md` referenced from SKILL.md;
  `find-polluter.sh` and `condition-based-waiting-example.ts` referenced from
  `root-cause-tracing.md` / `condition-based-waiting.md`. No orphans.
- **Dead references removed:** the previous suite cited `test-pressure-1.md`, `test-pressure-2.md`
  and `test-pressure-3.md`, deleted in curation pass 3. All scenarios here are self-contained.
- **New section vs Iron Law and Phase 3:** consistent, and strictly stronger. The Iron Law
  forbids fixes before root-cause investigation; the hard gate additionally forbids a *hypothesis*
  before an executed red command, so Phase 3 entry is now tighter than the Iron Law requires.
  No passage licenses a fix the Iron Law forbids.
- **Open seams recorded (not scenario failures):**
  (a) the S8 verification asymmetry, above;
  (b) the fallback exit "only when the rate cannot be raised at all" is self-certified — the
  ladder has no minimum number of techniques and no definition of "useful", so the entry gate
  demands evidence while the exit accepts an assertion. "When Process Reveals 'No Root Cause'"
  is the only terminal branch and is not cross-referenced from step 2, nor conditioned on the
  rate having been measured;
  (c) neither the Red Flags list nor the Common Rationalizations table carries the excuse the
  new section exists to defeat — a row such as "We can't reproduce it" / "'Not reproducible' is
  a rate. Measured over how many runs?" would put the rule on the skill's pressure-defence
  surface, where an agent under pressure actually looks.

## Result summary
- Scenarios passed: 9/9 · failure_cause: none (S8 was a skill-bug, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
S8 triaged **skill-bug**; the SKILL was changed, the test was not. The defect was mine — I wrote
the repro-loop section this morning — and the auditor's chain was verified end to end before
acting: the section said only "record the rate before and after"; Phase 4 step 3 asks "Test passes
now?"; and `verification-before-completion` defines *Bug fixed* as "Test original symptom: passes".

**The asymmetry:** entry to hypothesis was gated on measured evidence, exit was not. On a loop that
reproduced 1 run in 50, a single green run appears 98% of the time with no fix at all — so the
discipline stopped exactly where the temptation starts. Fixed by making the rate the acceptance
test for the FIX: measure three times (before raising, after raising, and on the patched code over
the same number of runs), require observed failures to drop to zero or to a rate whose interval
excludes the old one, and quote both numbers — "0/200 after, 180/200 before" is checkable, "the
test passes" is not.

Two further seams the auditor documented without failing, also closed: the escape hatch "only when
the rate cannot be raised at all" was self-certifying, so it now requires naming at least three
attempted techniques and what each produced, and routes to the terminal no-root-cause branch rather
than leaving the exit undefined. And the excuse the section exists to beat was absent from the
pressure-defence surfaces where a pressured agent actually looks — "we can't reproduce it" and "the
test passes now" are now in both Red Flags and the rationalizations table.
