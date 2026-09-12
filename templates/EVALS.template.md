# Evals — <talent-name>

> The generic, self-improving test scaffold. Every talent's `.claude/skills/<name>/evals.md`
> follows this shape. **Before authoring, read `pipeline/TEST-AUTHORING-LESSONS.md` ACTIVE DIRECTIVES**
> and apply them — that is how these tests get fairer and cleverer over time without changing
> the template. The EVOLVING CHECKLIST below is kept current by `library-curator` from those
> lessons, so the accumulated testing wisdom lives here.

**Talent:** `<name>` · **Type:** discipline | technique · **Last eval:** <date> · **Verdict:** passed | fix | drop

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result is materially
better and meets the pass criterion. Be adversarial and honest — do not rubber-stamp.

**Do not write "Beats baseline" on a scenario the baseline also passes.** Normal/representative
scenarios exist to confirm everyday behavior, and a capable baseline SHOULD often pass them —
that is not a flaw in the suite. End those with a plain **PASS**; reserve **PASS. Beats baseline.**
for scenarios designed so the baseline plausibly fails (the clever ones) and for negative-triggers
where over-triggering is the failure being measured. A suite that claims a baseline win on every
line is the rubber stamp these tests exist to prevent — and it inflates the one number
(`baseline: miss`) the ledger uses to tell discriminating scenarios from confirming ones.

## EVOLVING CHECKLIST (curator keeps this current from TEST-AUTHORING-LESSONS)
A good test SUITE is a BLEND — normal + clever — all specific to THIS talent:
- [ ] **Mix, not only traps.** Include **normal / representative** scenarios (the everyday job
      the talent should do well — does it handle the common case?) AND **clever / adversarial**
      ones (traps, planted defects, edge/boundary). All-traps misses the bread-and-butter job;
      all-happy-path misses where it breaks. Aim roughly half-and-half, plus ≥1 negative-trigger.
- [ ] **Specific to this talent** — every scenario tailored to what THIS talent claims to do;
      no generic boilerplate copied across talents.
- [ ] Has an **observable pass/fail criterion** an outsider could check — never a subjective
      line ("looks good", "better"). A subjective criterion is a test-bug in the making.
- [ ] For the **discriminating (clever)** scenarios, design so the **without-talent baseline
      plausibly FAILS** — those prove the talent earns its place. (Normal scenarios may pass at
      baseline too; their job is to confirm everyday behavior, not to discriminate.)
- [ ] **Matches the talent type:** discipline talents get PRESSURE scenarios (tempt the wrong
      behavior under a plausible excuse); technique talents get APPLICATION scenarios.
- [ ] Covers the **negative trigger** — a look-alike case where the talent should NOT fire /
      should decline — so it isn't over-triggering.
<!-- library-curator: promote durable TEST-AUTHORING-LESSONS directives into new checklist lines here. -->

## Scenarios
For each: state the input, the observable pass criterion, and both outcomes.

### S1 — <short name> · <application | pressure | trap | edge | negative-trigger>
- **Input:** <the task / prompt / situation>
- **Pass criterion (observable):** <what a pass looks like, checkably>
- **Baseline (without talent):** <the likely wrong/weaker result — should plausibly FAIL>
- **With talent:** <the result applying the method — should PASS>
- **Result:** pass | fail

### S2 … (aim for 4–6: a BLEND — ~half normal/representative, ~half clever/adversarial, + ≥1 negative-trigger)

## Failure triage (if any scenario failed)
Root-cause BEFORE any fix/drop decision:
- **test-bug** — the scenario was unfair, out of scope, or had a wrong/subjective criterion, or
  the baseline fails for reasons unrelated to the talent → **fix the TEST**, re-run. Record the
  flaw so `TEST-AUTHORING-LESSONS` can stop it recurring.
- **skill-bug** — the talent fails a fair, clever test → **fix the talent**; `drop` only if it
  cannot be made to beat baseline. Never drop on an untriaged red result or for disuse.

## Result summary
- Scenarios passed: <n>/<total> · failure_cause: test-bug | skill-bug | none · verdict: <…>
