# Eval: cost-aware-model-routing

Functional regression test for the `cost-aware-model-routing` talent. This is a
**hybrid** talent: a *technique* (route each task to the cheapest model tier that clears
the quality bar) plus a *discipline* (cap dollar spend with budget ceilings,
stop-conditions, bounded fan-out width, and prompt-cache reuse). Its sharpest,
most-differentiated behaviors are (a) defaulting DOWN a tier on mechanical/fan-out work
while (b) still escalating UP for synthesis, high-stakes, and adversarial verification,
and (c) attaching guardrails to any run that could get expensive.

Method: for each scenario, reason through the likely output WITHOUT the talent
(baseline Claude) vs WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result. Adversarial, not a rubber stamp.
Traps are included in BOTH directions — tasks that tempt over-spending (fan-out "to be
safe") and tasks that tempt under-spending (cheaping out on a high-stakes step).

Date: 2026-08-27 · Talent version: SKILL.md as of this commit.

---

## Scenario 1 — Wide fan-out over many similar items (application, core target)
**Input:** "Extract and normalize the license header in each of ~500 source files, and
report any file whose header is missing or nonstandard."
**Pass criterion:** Routes per-item work to the **cheap/small** tier, **batches** items
rather than one call per file, and **caps fan-out width** to a small N (or a single
batched pass) instead of dispatching ~500 top-tier subagents. Must NOT recommend top tier
for this deterministic work.

- **Baseline:** Plausibly does one of the two classic money-burners: fans out a subagent
  per file (or in large parallel waves) at the default/top tier "to be thorough," or sends
  every file to the top tier. 500 × top-tier calls for a find/replace-grade task — cost
  scales with width × price with zero quality gain.
- **With talent:** Step 1 classifies this as format/transform + extract → cheap/small
  (routing-table rows 1 and 3). Step 2 caps width to the smallest N and prefers batching.
  Step 3 puts the shared instruction/spec in a stable cached prefix so it amortizes across
  batches. Result: a handful of cheap batched calls, not 500 top-tier agents.
- **Verdict:** PASS. Directly attacks the tier × width cost drivers the talent names.
  Order-of-magnitude cheaper than baseline with equal output quality. Decisive win.

---

## Scenario 2 — Security-sensitive review (under-spend trap: do NOT cheap out)
**Input:** "We changed the password-reset and session-token logic. Review the diff for
security vulnerabilities before we ship."
**Pass criterion:** Routes to the **top** tier despite the talent's default-down bias,
because the task is security-sensitive AND an adversarial review. If the talent recommends
a cheap tier here to save money, it FAILS — this is the trap that a naive "always go
cheap" reading would fall into.
- **Baseline:** Typically uses a strong model for a security review anyway; fine, but with
  no explicit rationale tying tier to error-cost.
- **With talent:** Step 1 explicitly carves out high-stakes/security → top tier, and
  "adversarial verification (checking work, security review) → top tier even if generation
  was cheap." Routing-table rows 5 and 6 both point to top. The talent's *default-down*
  rule is correctly overridden by its own high-stakes and verify rules.
- **Verdict:** PASS. The talent resists its own cost-cutting pressure exactly where error
  cost >> model cost. Crucially it does NOT mis-fire the cheapness heuristic. Materially
  better than baseline because the tier choice is now principled and auditable, not habit.

---

## Scenario 3 — Adversarial verification of cheap-generated output (technique, split-tier)
**Input:** "A small/cheap model just generated 1,000 product descriptions and their SEO
metadata. Set up the check that they're accurate and on-brand before publish."
**Pass criterion:** Recommends a **split**: keep generation cheap, but run the
**verification/adjudication at the top tier** (an independent check must be at least as
strong as generation). Bonus: batch the verify pass and cache the brand/style rubric as a
stable prefix. Recommending the same cheap tier for verification = fail.
- **Baseline:** Likely verifies with whatever model is at hand — often the same cheap tier
  that generated the content, which cannot reliably catch its own class of errors; or
  swings to top tier for BOTH generation and verify, overspending on the cheap half.
- **With talent:** Step 1's adversarial-verify rule forces the checker up a tier while
  leaving generation cheap; Step 3 batches the verify and caches the rubric. This is the
  talent's most nuanced move: cost and rigor allocated independently per stage.
- **Verdict:** PASS. Split-tier routing is a behavior baseline rarely produces
  deliberately. Clear, differentiated win.

---

## Scenario 4 — Mixed batch: mostly mechanical, a few judgment calls (application)
**Input:** "Migrate 200 components from the old prop API to the new one. Most are
mechanical renames; ~5 use a deprecated pattern that needs a design decision on the
replacement."
**Pass criterion:** Routes the 195 mechanical migrations to the **cheap** tier (batched)
and escalates only the **~5 judgment-call** files to the **top** tier. A single uniform
tier for all 200 (either direction) is the failure mode. Must separate the classes.
- **Baseline:** Tends to pick one tier for the whole job — top tier "because some are
  tricky" (overpays on 195) or cheap tier throughout (the 5 design calls come out weak and
  need rework). No per-item classification.
- **With talent:** Step 1 classifies per task class, not per job: rename/boilerplate →
  cheap; ambiguous/synthesis (the design decision) → top. Step 4 says start cheap and
  escalate the specific items on evidence. Yields cheap bulk + targeted top-tier spend.
- **Verdict:** PASS. Per-class routing captures most of the savings while protecting the
  few high-value decisions. Baseline's uniform-tier habit loses on one axis or the other.

---

## Scenario 5 — Unbounded agent loop with a hard budget (discipline)
**Input:** "Run an agent loop that keeps trying to reproduce and fix this flaky test until
it's green. We have a $50 cap for this task."
**Pass criterion:** Attaches a **budget ceiling** ($50) AND a **stop-condition** (max
iterations, or "stop and ask at X% of budget") so the loop can't silently run away; caps
any fan-out; tunes reasoning effort. Simply starting the loop with no ceiling/stop = fail.
- **Baseline:** High risk of launching an open-ended loop with no explicit stop other than
  "until green," which on a genuinely flaky/irreproducible test can iterate indefinitely
  and blow past $50 before anyone notices — the exact "routine job quietly becomes
  expensive" failure the talent exists to prevent.
- **With talent:** Step 2 mandates a budget ceiling and a stop-condition (max
  steps/iterations or stop-and-ask at a % of budget) and caps width. The run now has a
  hard brake and a human-checkpoint before overspend.
- **Verdict:** PASS. This is the discipline half of the talent doing precisely its job.
  Baseline's missing stop-condition is a real, common, and expensive failure. Strong win.

---

## Scenario 6 — Mechanical-but-irreversible task (precedence trap / clarity gap)
**Input:** "Bulk-rename the public SDK method `getUser` → `fetchUser` across the library
and every published example and doc."
**Pass criterion:** Recognizes that although the *edit* is mechanical (a rename), the
change is **public-API / irreversible**, so the DECISION and the VERIFY step belong at the
**top** tier (or gated by a human) — not routed wholesale to cheap tier on the strength of
"it's just a rename." Routing the whole task cheap because the routing table lists
"rename → cheap/small" = fail.
- **Baseline:** Could go either way; may treat it as a simple find/replace and execute
  without flagging the breaking-change/versioning implications.
- **With talent:** Step 1 lists BOTH a "rename/boilerplate → cheap" rule (row 1) AND a
  "high-stakes/irreversible → top" rule (row 5), and says escalate on evidence. A careful
  reader resolves the conflict correctly — cheap *mechanical execution* of the rename, but
  top-tier *judgment* on whether/how to rename a public symbol and top-tier *verify* that
  nothing downstream breaks. HOWEVER, the routing table presents "rename, boilerplate →
  cheap/small" with no caveat that irreversibility/public-surface overrides mechanicalness,
  and gives no stated precedence rule when a task matches both a cheap row and the
  high-stakes row. A reader who pattern-matches on the table row alone can under-route.
- **Verdict:** WEAK / PASS-with-gap. The talent *contains* the right answer (Step 1's
  high-stakes rule), so a careful application beats baseline — but it does not *reliably*
  beat baseline here because the routing table can actively mislead toward cheap on a
  mechanical-looking-but-irreversible task. Identified GAP: no explicit precedence rule
  ("irreversible/public-surface/security overrides a mechanical classification; when a task
  matches both a cheap row and a high-stakes row, the high-stakes row wins") and no
  separation of *execution tier* from *decision/verify tier* for a single task.

---

## Summary
| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | 500-file fan-out extraction | application (core) | PASS |
| 2 | Security review | under-spend trap | PASS |
| 3 | Verify cheap-generated output | split-tier technique | PASS |
| 4 | Mixed mechanical + judgment batch | application | PASS |
| 5 | Unbounded loop with $50 cap | discipline | PASS |
| 6 | Public-API rename | precedence/clarity trap | WEAK (gap) |

**Passed: 5 / 6.**

**Overall:** The talent decisively and materially beats baseline on its core target class
— fan-out width control (S1), split-tier verify (S3), per-class routing of mixed batches
(S4), and hard budget/stop-condition guardrails on runaway loops (S5). Just as important,
it does NOT mis-fire its cheapness heuristic on high-stakes work: S2 shows the default-down
rule is correctly overridden by the high-stakes and adversarial-verify rules, so the talent
avoids the dangerous "always go cheap" failure. These are behaviors baseline produces only
sporadically and never with an auditable rationale tying tier and width to cost drivers.

**Gap (Scenario 6):** The routing table lists "rename/boilerplate → cheap" without a stated
precedence rule for tasks that are mechanical to *execute* but high-stakes to *decide/ship*
(public-API changes, irreversible migrations). Step 1 contains both rules but no explicit
tie-breaker, so a reader pattern-matching on the table alone can under-route an irreversible
task to cheap tier. This is a clarity/precedence refinement, not a defect in the talent's
core claim.

**Recommended fix (non-blocking):** Add one line to Step 1 / the routing table — "When a
task matches both a cheap row and a high-stakes row (e.g. a mechanical rename of a public
API), the high-stakes row wins: route *execution* cheap if you like, but keep the
*decision and verification* at top tier." This closes the only place the talent can be read
against its own intent.

**Verdict: PASSED** — decisive, differentiated wins across its core target domain and both
guardrail and don't-cheap-out traps handled correctly, with one non-blocking
precedence/clarity gap noted for a future edit.
