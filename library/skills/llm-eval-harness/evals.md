# Evals — llm-eval-harness

Functional regression test for the `llm-eval-harness` talent. This is primarily a
**technique** talent (a method: locate the LLM-calling surfaces → assemble cases as data →
write deterministic assertions first → add model-graded rubrics only where determinism can't
reach → define a gate against a recorded baseline → structure a CI runner → wire it as a
required check → document) that also carries hard **discipline** rules (deterministic beats
graded; the uncalibrated grader stays advisory/non-blocking; assert on output *behavior*, not
prompt text; cases are data, not code; the baseline moves only as a reviewed act; no auto-run
hooks).

So the scenarios below mix *application* cases (the everyday suite it should build well) with
*pressure* cases that tempt the exact shortcuts the talent forbids, plus one *negative-trigger*
where a look-alike task should route it to a sibling talent instead.

Method: for each scenario, reason the likely output WITHOUT the talent (baseline) against the
output WITH the talent's method applied, and judge whether the talent produces a materially
better, criterion-meeting result. Adversarial, not rubber-stamp.

**Talent:** `llm-eval-harness` · **Type:** technique (+discipline rules) · **Last eval:** 2026-08-27 · **Verdict:** passed · Model: claude-opus-4-8

---

## Scenario 1 — Application: first eval suite for a shipped summarizer

**Input.** "Our app has a `summarizeTicket(text)` function that calls the model with a system
prompt. People keep tweaking that prompt and we only find out it got worse from customer
complaints. Set up evals so a bad prompt change can't merge."

**Pass criterion (observable).** The deliverable (a) locates the callable surface (function,
its input, its output shape) rather than testing the raw prompt string; (b) stores cases as
**data** — a JSON/YAML/table file, one row per input, not inputs hard-coded in test bodies;
(c) attaches **deterministic assertions first** (e.g. length/token budget, contains required
entities, must-not-contain PII/placeholder, JSON-parse validity); (d) adds any tone/faithfulness
check as a **model-graded rubric marked advisory/non-blocking**; (e) defines a **gate with a
recorded baseline** and (f) emits a **CI job** that runs on PRs touching the prompt/model and
exits non-zero on regression. Missing the data-file separation OR the recorded baseline OR the
CI job = fail.

**Baseline (no talent).** Writes a handful of `assert` calls inline in one test file with the
example ticket text pasted into the test body, eyeballs that the summary "looks right," and
maybe adds a single model-graded "is this a good summary? y/n" check wired as blocking. No
case-as-data file, no recorded baseline, no PR-scoped CI gate. New inputs require editing test
code; the graded check flakes and blocks unrelated PRs.

**With talent.** Steps 1–8 produce the structural pieces the baseline omits: a `evals/summarize/`
case file, deterministic checks that grade for free and never flake, the rubric kept advisory
until `llm-judge-calibration` clears it, a baseline number the gate measures regression against,
and a CI step scoped to prompt/model diffs. Done = suite + baseline + CI job + docs.

**Verdict: PASS.** Delivers the load-bearing structure (data-driven cases, recorded baseline,
regression gate) a baseline skips, which is the entire point of the task.

**Result: pass.**

---

## Scenario 2 — Application: guard a tool-calling agent's call shape

**Input.** "Our booking agent decides whether to call `create_booking` or `refund`. A prompt
edit last week made it call `refund` when it should have booked. Add an eval so that can't slip
through again."

**Pass criterion (observable).** Reaches for a **tool-call-shape deterministic assertion** —
per case, the correct tool is named, required args are present, and forbidden tools are not
called — graded deterministically. It must NOT hand this structured, exactly-checkable behavior
to a model grader.

**Baseline (no talent).** Plausibly writes a model-graded "did the agent do the right thing?"
rubric, or asserts on a fragment of the natural-language reply, rather than on the structured
tool call. Slower, costlier, and can flake on a check that is deterministic by nature.

**With talent.** Step 3 explicitly lists tool-call shape (correct tool, required args present,
no forbidden call) among the deterministic assertions, and the rule "deterministic assertion
beats a graded one every time it can express the check" forces the right instrument. The past
incident (refund-instead-of-book) becomes a locked case with a `must-not-call: refund`
assertion.

**Verdict: PASS.** Baseline is tempted to grade a structured decision with a fuzzy judge;
the talent pins it to a stable, free, exact check.

**Result: pass.**

---

## Scenario 3 — Pressure: block the PR on an uncalibrated model grader

**Input.** "Simplest thing: have the model score each answer's correctness 1–5, average it, and
**fail the PR if the average drops**. Wire that as the required check today."

**Pass criterion (observable).** (a) Pushes the checkable part of "correctness" onto
**deterministic assertions** (exact/contains/schema/expected-key) wherever the case has a known
answer, and (b) keeps the model-graded score **advisory (reported, non-blocking)** until
`llm-judge-calibration` validates the judge — it must NOT let an uncalibrated grader be the
blocking gate. Wiring the raw 1–5 judge as the required status check = fail.

**Baseline (no talent).** Complies literally: wires the model grader as the blocking gate. The
gate now fails PRs on judge noise and drift, an unvalidated scorer decides what merges, and the
team either chases phantom regressions or disables the gate — worse than no gate.

**With talent.** Rule "Never let an uncalibrated model grader block a merge; keep it advisory
until `llm-judge-calibration` validates it" plus step 4 (`mark such assertions advisory`) refuse
the blocking wiring. Deterministic assertions on the cases with known answers become the gate
that can actually block; the graded score rides along as a reported, non-blocking signal until
calibrated.

**Verdict: PASS.** Prevents a flaky, unvalidated gate — the exact release-gate footgun the
talent's discipline exists to stop; baseline installs it by construction.

**Result: pass.**

---

## Scenario 4 — Pressure: snapshot the whole output / assert on the prompt

**Input.** "Make it bulletproof: snapshot the model's full response for each case and fail if it
changes at all, and also add a test that fails if anyone edits the system-prompt string."

**Pass criterion (observable).** Refuses whole-output exact-snapshot and prompt-text assertions;
instead asserts on **output behavior** — the summary still contains the key facts, still parses,
still names the right tool — so the suite **survives a behavior-preserving rewrite** of the
prompt or a harmless wording change in the model's phrasing. A suite that red-flags every benign
reword, or that pins the prompt string, = fail.

**Baseline (no talent).** Takes the request at face value: a full-string snapshot per case and a
`assert systemPrompt == "..."` test. Every legitimate prompt improvement and every harmless
model rephrasing turns the suite red, so people delete or `--update-snapshots` past it — the
gate stops meaning anything.

**With talent.** Rule "Assert on output behavior, not on the prompt text — the suite must survive
a rewrite that preserves behavior," backed by the deterministic-assertion menu (contains,
schema, tool shape, numeric range), redirects to behavioral checks. The system-prompt-equality
test is rejected outright; the value the user wanted (catch real regressions) is delivered
without the brittleness.

**Verdict: PASS.** Baseline builds a maximally brittle suite that gets bypassed; the talent
delivers a durable one. High-value discriminator.

**Result: pass.**

---

## Scenario 5 — Pressure: a gate that can never fail (silent baseline auto-update)

**Input.** "Have the eval **record the new pass rate as the baseline every time it runs**, so
the check is always green against the latest numbers and nobody gets blocked. Also I don't have
real example inputs yet — just make some up inside the test."

**Pass criterion (observable).** (a) Refuses to auto-rewrite the baseline each run — the baseline
moves only as an **explicit, reviewed act**, because a gate measured against a self-updating
baseline can never detect regression; and (b) on "no inputs yet," **hands off to
`synthetic-eval-data-generation`** to manufacture representative inputs rather than fabricating a
couple of throwaway cases inline in the test body. Auto-updating baseline OR inline-fabricated
cases-as-code = fail.

**Baseline (no talent).** Does exactly as asked: writes the gate to overwrite the baseline on
every run (permanently green, detects nothing) and pastes two invented strings into the test as
the "cases." The suite looks like a gate and gates nothing; a real quality drop sails through.

**With talent.** Rule "The gate measures regression against a recorded baseline; update the
baseline as an explicit, reviewed act, never silently" stops the auto-update; step 5 records a
fixed baseline the gate compares against. Step 2 ("If inputs do not exist yet, stop and hand off
to `synthetic-eval-data-generation`, then resume") plus "Cases are data, not code" route the
missing-inputs problem to the right sibling instead of hard-coding fakes.

**Verdict: PASS.** Catches two ways to build a gate that is theatre — a baseline that can't be
regressed against and cases smuggled into code — both of which baseline commits on request.

**Result: pass.**

---

## Scenario 6 — Negative-trigger: score the coding AGENT's task completion (should route away)

**Input.** "Build me an eval harness that runs my Claude Code agent over 20 tasks and scores
whether it actually completed each one, so I can tell if a change to the agent's workflow made it
worse."

**Pass criterion (observable).** Recognizes this is scoring a **Claude Code agent's / workflow's
own task completion**, not gating a shipped LLM app's product output, and **routes to
`eval-harness`** rather than building an assertion-based product-code suite. Building an
`evals/<surface>/` product suite here = fail (mis-fire).

**Baseline (no talent).** The two tasks are look-alikes ("build an eval harness"); a talent-free
response plausibly conflates them and starts building an assertion suite over the agent's
outputs, or blends the two framings, applying the wrong tool to the wrong layer.

**With talent.** The description's explicit NOT-clause and the "When NOT to use" line — "scoring
a Claude Code agent's own task completion (use `eval-harness`)" — make this a correct
non-trigger; it declines and hands to `eval-harness`.

**Verdict: PASS (correct non-trigger).** The scoping keeps it from mis-firing on the sibling's
territory; value over baseline is positive precisely because baseline is tempted to build the
wrong harness.

**Result: pass.**

---

## Failure triage

No scenario failed. No test-bug or skill-bug to root-cause; no drop considered.

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | first eval suite for a summarizer | application | PASS |
| 2 | guard a tool-calling agent's call shape | application | PASS |
| 3 | block PR on uncalibrated model grader | pressure/trap | PASS |
| 4 | snapshot whole output / assert on prompt | pressure/trap | PASS |
| 5 | gate that can never fail (auto-baseline + fake inputs) | pressure/trap | PASS |
| 6 | score the coding agent's task completion | negative-trigger | PASS |

**Scenarios passed: 6 / 6 · failure_cause: none.**

**Verdict: PASSED.** On the two application cases the talent supplies the structure a baseline
omits — cases-as-data, deterministic-first assertions (including tool-call shape), a recorded
baseline, and a PR-scoped CI gate. On the three pressure cases it refuses the exact shortcuts
that produce a gate that is worse than none: an uncalibrated judge wired as the blocking check
(S3), a brittle whole-output/prompt-text snapshot that gets bypassed (S4), and a self-updating
baseline plus fabricated inline cases that make the gate pure theatre (S5). On the negative
trigger it correctly declines and routes to `eval-harness`. In every case a talent-free baseline
is tempted into, or actively commits, the failure the talent exists to prevent.

**Minor gap (not blocking).** The talent is a method author, not a runner (its own Rules say a
human enables execution and it makes no network/CLI calls). So a lazy operator could "apply" it
in name — emit the suite and CI YAML — while never making the check *required* or ever running
it, leaving prod ungated in practice. This is the inherent limit of an authoring-only technique
talent and is disclosed in its own Rules (step 7 + "a human enables execution"); it does not
lower the verdict.
