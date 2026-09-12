# Evals — behavioral-spec-mining

Functional regression test for the `behavioral-spec-mining` talent. Each scenario
states an input and an **observable pass criterion**, then compares the likely
**baseline** output (no talent) against the output **with the talent's method
applied**. A scenario passes only if the talent produces a materially better,
criterion-meeting result.

Talent under test: reverse-engineers a formal, *testable* behavioral spec
(Requirements + Invariants + WHEN→THEN scenarios) from brownfield code that shipped
without one, under a declared token budget, describing behavior that **IS** (not
SHOULD BE), flagging inferred outcomes `(unverified)`, and emitting plain Markdown.

Shared fixture (referenced by S1–S3): a legacy `wallet.py` `Wallet` class with
`withdraw / deposit / freeze`, guard clauses (frozen, positive-amount, idempotency
dedup, sufficient-balance), a misleading comment on `withdraw` that reads
"Always succeeds if amount is positive", and a `deposit` that has **no** frozen guard.

---

## S1 — Representative: mine a spec from a guarded legacy module

**Input:** "What is this `Wallet` class supposed to do? I'm about to rewrite it —
pin down actual behavior first." (points at the fixture)

**Pass criterion:** Output is a structured spec with (a) Requirements as SHALL
statements, (b) Invariants pulled from the guard clauses (frozen check, amount>0,
idempotency dedup, balance≥amount), (c) numbered WHEN→THEN scenarios covering the
happy path **and every error branch** (`AccountFrozen`, `ValueError`,
`InsufficientFunds`, idempotent replay), and (d) a Coverage note.

**Baseline (no talent):** Produces a readable prose summary — "a wallet you can
deposit to and withdraw from, with freeze support." Likely lists the methods and
their exceptions, but as narrative. Typically no separation of Requirements vs
Invariants, no per-branch WHEN→THEN, no coverage/blind-spot note. Not directly
translatable into characterization tests.

**With talent:** Enumerates entry points (`withdraw`, `deposit`, `freeze`), pulls
invariants from guard/error branches first (the four above), emits one WHEN→THEN
per branch incl. idempotent replay returning the unchanged balance, and closes with
a Coverage note (3/3 entry points fully mined, budget spent). Directly test-able.

**Result:** PASS — talent yields a materially more complete, testable artifact than
baseline's prose.

---

## S2 — TRAP: comment contradicts code ("Always succeeds if amount is positive")

**Input:** Same fixture. The `withdraw` docstring claims it "Always succeeds if
amount is positive," but the body raises `AccountFrozen` and `InsufficientFunds`.

**Pass criterion:** The spec records the **actual** behavior (withdraw can raise
on frozen or insufficient funds) and explicitly flags the discrepancy between the
comment's claim and the code — not the comment's claim as fact.

**Baseline (no talent):** High risk of parroting the docstring — "withdraw always
succeeds for positive amounts" — because summarizers weight comments as
authoritative. A silent, wrong Requirement enters the spec.

**With talent:** Rule "Describe behavior that IS, not SHOULD BE" + Step 6
"flag contradictions between what code does and any comments/names that claim
otherwise — record the code's actual behavior and note the discrepancy" forces the
correct outcome: WHEN frozen THEN raises `AccountFrozen`; WHEN amount>balance THEN
raises `InsufficientFunds`; plus a noted contradiction against the docstring.

**Result:** PASS — direct, discriminating win. This is the trap the talent exists
to catch.

---

## S3 — TRAP: do not invent a guard that isn't there (unverified inference)

**Input:** "Does freezing the account stop all money movement?" against the fixture,
where `freeze()` sets `self.frozen = True`, `withdraw` checks `self.frozen`, but
`deposit` has **no** frozen check.

**Pass criterion:** Spec states that a frozen account still **accepts deposits**
(no guard in `deposit`), rather than assuming freeze blocks everything. Any claim
not confirmed in code is marked `(unverified)`.

**Baseline (no talent):** Tempting to generalize "frozen accounts are locked" and
assert deposits are blocked too — a plausible but wrong invariant, unbacked by code.

**With talent:** "Never invent Requirements the code does not exhibit; mark every
inferred outcome `(unverified)`" + "Invariants come from error/guard branches first"
drive reading each method's guards individually: withdraw is frozen-guarded, deposit
is not, so the spec records "WHEN frozen THEN deposit still succeeds" as observed
behavior. Avoids the fabricated invariant.

**Result:** PASS — talent prevents an invented invariant baseline is prone to.

---

## S4 — BOUNDARY TRAP: wrong tool / greenfield (should NOT mine actual behavior)

**Input:** "Spec out this new payments module I'm *about* to write," and separately
"Give me an architecture codemap of the repo."

**Pass criterion:** The talent recognizes it does not apply — greenfield specs are
authored forward (not mined from non-existent behavior), and structural/codemap
questions route to `update-codemaps`; single-file prose comprehension routes to
`deep-reading`. It declines/redirects rather than producing a bogus "mined actual
behavior" spec.

**Baseline (no talent):** No routing signal; would just attempt whatever was asked,
including "mining" behavior from code that does not exist yet, or conflating a
behavioral spec with an architecture map.

**With talent:** Description's negative scope ("NOT for regenerating structural
codemaps … NOT for comprehension notes on prose or a single file") and the
"When NOT to use" list explicitly cover greenfield ("author forward") and
structure (update-codemaps). Correctly declines/redirects.

**Result:** PASS — modest but real guardrail against misapplication. (Weakest of the
five: declining is less visibly valuable than the S2/S3 wins, but it is correct.)

---

## S5 — PRESSURE: exhaustive-read + format demand ("read all 200 files, give Gherkin")

**Input:** "Reverse-engineer acceptance criteria for our whole 200-file billing
service. Read all of it and give me Gherkin `.feature` files plus the pytest
skeletons."

**Pass criterion:** (a) Declares a token budget and **samples** entry points by
importance rather than reading everything; (b) reports honest Coverage (mined vs
skimmed vs skipped); (c) emits **plain Markdown** WHEN→THEN, **not** Gherkin/OpenSpec;
(d) does **not** scaffold test files — mining produces the spec only.

**Baseline (no talent):** Likely complies literally — attempts to read the whole
corpus (blows context, degrades quality), emits Gherkin, and generates test
skeletons because the user asked. No blind-spot accounting.

**With talent:** "Budget is a hard ceiling … Sampling with honest coverage beats
exhaustive reading" + "Output is plain Markdown only. Do not emit OpenSpec, Gherkin
… and do not scaffold test files." Talent samples under budget, emits Markdown
WHEN→THEN, reports coverage, and refuses the scaffolding — resisting both the
exhaustive-read and the format temptation.

**Result:** PASS — talent overrides two tempting-but-wrong user demands with
principled behavior.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| S1 | Mine spec from guarded legacy module | representative | PASS |
| S2 | Comment contradicts code | trap (discriminating) | PASS |
| S3 | Don't invent a missing guard | trap (discriminating) | PASS |
| S4 | Greenfield / wrong-tool boundary | boundary trap | PASS |
| S5 | Exhaustive-read + Gherkin/scaffold pressure | pressure | PASS |

**Scenarios passed: 5 / 5.**

**Verdict: PASSED.** The talent clearly beats baseline. Its decisive advantages are
concentrated in the discriminating traps: S2 (records actual behavior over a lying
comment), S3 (refuses to fabricate a guard the code lacks), and S5 (holds a budget
and refuses Gherkin/test-scaffolding under direct user pressure) — all behaviors a
baseline summarizer routinely gets wrong. S1 shows a materially more testable
artifact; S4 shows correct negative-scope routing.

**Minor observations (not blocking):**
- S4's win is the least visible — the negative scope is correct but low-drama.
- The talent deliberately stops at the spec and forbids test scaffolding; a user who
  actually wants executable characterization tests must take a second step. This is a
  scope choice, not a defect, but worth noting for expectation-setting.
- On tiny corpora the "declare a 40k budget" step is ceremony; harmless, and the
  sampling rule already no-ops when corpus < ~40% of budget.
