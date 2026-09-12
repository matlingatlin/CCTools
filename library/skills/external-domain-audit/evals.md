# Evals — external-domain-audit

Functional regression tests for the `external-domain-audit` talent. Each scenario states
an input, an observable pass criterion, and the reasoned baseline (no talent) vs
with-talent outcome. The talent is a **method/discipline** talent: its central claim is
that learning the external contract *before* reading the implementation catches conformance
bugs that a code-first review cannot, because a code-first reviewer anchors on the code's
own model of "correct" — and if the tests were written to match the code, both share the
same blind spot. The scenarios are built to make that claim falsifiable.

Method under test (condensed): (1) name the exact external contract/version; (2) build a
KB from the authoritative external docs BEFORE opening the code; (3) design the ideal
conformance suite BLIND from the KB; (4) only then read code + tests; (5) gap-compare in
three directions — ideal-with-no-impl (bug), ideal-with-no-test (blind spot),
code-with-no-spec (scope creep); (6) report by clause, ranked, cited. Guardrails: docs
before code; method-only (no network fetch, ask for the spec if absent); cite every claim;
existing tests are evidence never the oracle; version-pin.

Verdict summary: **PASSED** — 5/5 scenarios meet their pass criterion and the with-talent
result materially beats baseline (or correctly declines / avoids a false positive). Two
watch-items noted at the end; neither drops any scenario below baseline.

---

## Scenario A — Shared code+test blind spot (CSRF `state` not verified)
**Type:** representative task with a planted shared defect (the discriminating case).

**Input:** "Audit our OAuth 2.0 authorization-code integration against the spec (RFC 6749)."
The repo vendors RFC 6749. The implementation performs the redirect and the code→token
exchange correctly, but the callback handler never checks that the returned `state` matches
the value it sent. The one existing test drives a happy-path round trip (authorize →
callback with the *expected* state → exchange) and asserts a token comes back. It passes.

**Pass criterion:** The audit reports, as a ranked correctness finding, that the callback
does not verify `state`, cites RFC 6749 §10.12 (CSRF), gives expected-vs-actual, and names
the missing negative test ("callback with absent/mismatched state must be rejected").

**Baseline (no talent):** Reads the handler, sees a passing round-trip test, sees the
`state` param is generated and sent. A code-first pass is prone to treat the green test as
evidence of conformance and move on; §10.12 is a SHOULD-flavored security clause easy to
skip when the happy path works. Likely misses it, or mentions it only as a vague "consider
CSRF" aside without a spec cite or a concrete missing test. **Miss / weak.**

**With talent:** Step 3 enumerates conformance cases from the RFC *before* seeing the test,
so "reject callback whose `state` does not match the request" is on the frozen oracle as a
mandated negative case. Step 5(a) then finds no implementation for it → correctness gap;
5(b) finds no test → blind spot. Reported with the §10.12 cite and the exact missing test.
**Meets criterion.**

**Result: PASS.** Structural win — the blind oracle contains the case the green test hid.

---

## Scenario B — Ideal case the code never handles (S3 503 SlowDown retry)
**Type:** planted omission; discriminates the talent from test-coverage.

**Input:** "Audit our S3 client's retry logic against AWS's retry guidance" (the vendored
AWS SDK retry doc is in `docs/`). The client retries `500 InternalError` with exponential
backoff, but does **not** retry `503 SlowDown` (throttling) at all — it surfaces it as a
hard error. There is no test referencing 503.

**Pass criterion:** The audit flags that `503 SlowDown` is a retryable throttling response
per the guidance and is not retried (correctness gap) and has no test (blind spot), cited to
the retry doc, ranked above cosmetic issues.

**Baseline (no talent), esp. a test-coverage framing:** Coverage-style review fills gaps on
*code as written* — it can add a test for the 500 path, tighten backoff assertions, etc.,
but it has no reason to invent a 503 case because no 503 code path exists to cover. The
absence is invisible from the inside. **Miss.**

**With talent:** The blind suite is derived from the retry doc, which enumerates the
retryable class (500, 503 SlowDown, throttling) independent of the code. 503 is an ideal
case; step 5(a) finds no handling → gap. **Meets criterion.**

**Result: PASS.** This is the talent's sharpest structural advantage: you cannot cover a
requirement the implementation silently dropped unless your oracle came from outside the
code.

---

## Scenario C — Anti-trigger trap (internal-only diff, no external contract)
**Type:** trap; tests the description's negative triggers and the "Do NOT use" guardrail.

**Input:** "Review this diff that renames variables and extracts a helper in our internal
billing proration calculator." No protocol, RFC, public API, or vendor SDK is involved.

**Pass criterion:** The talent does **not** engage its spec-audit machinery, does not
invent or hallucinate an "external spec" to audit against, and defers to the appropriate
tool (code-review / diff review). Observable: no fabricated KB, no blind suite, an explicit
"no external contract here" statement.

**Baseline (no talent):** A diff review is exactly right and produces a fine result. Baseline
is fine here; the risk is only that the *talent* over-applies.

**With talent:** SKILL scope ("NOT for reviewing a diff ... or auditing internal-only logic
that implements no external contract") and step 1 (name the external contract; if none,
this is out of scope) cause it to decline and route to code-review rather than manufacture a
spec. **Meets criterion — the talent stays in its lane.**

**Result: PASS.** No false engagement; the guardrails hold under a tempting mislabel.

---

## Scenario D — Discipline under pressure (spec absent; do not audit from memory)
**Type:** pressure scenario; tests the method-only / cite-every-claim guardrails.

**Input:** "Audit our SMTP submission code for spec conformance." No RFC (5321/6409) is in
the repo or provided, and network fetch is disallowed.

**Pass criterion:** The audit does **not** proceed to emit "spec requirements" from the
model's memory dressed up as citations. It stops and asks the user to supply the exact
RFC/version (or an explicitly-provided authoritative source), naming what it needs. Any
interim observations are clearly labeled as unverified, not as cited contract clauses.

**Baseline (no talent):** Strong temptation to audit SMTP from memory and produce a
plausible-looking list of "MUST" claims. Some may be right, but they are uncited, possibly
version-drifted, and indistinguishable from confident guesses — the exact failure mode a
conformance audit exists to avoid. **Risky / partial.**

**With talent:** "Method only... Ask the user to supply the spec if it isn't present" and
"an uncited requirement is your assumption, not the contract" force it to request the
authoritative source before building the KB. **Meets criterion.**

**Result: PASS** (weakest discriminator — see watch-item 1: a from-memory baseline can still
surface real issues, so the win here is correctness-of-discipline, not raw find-count).

---

## Scenario E — Version-pin guards against a false positive (Stripe API version)
**Type:** trap that punishes naive auditing; tests the version-pin rule.

**Input:** "Audit our Stripe integration for API conformance." The client pins
`Stripe-Version: 2022-11-15` and uses that version's behavior/field correctly. The docs
folder happens to contain the *current* reference (a later version) in which a field was
renamed / a default changed.

**Pass criterion:** The audit checks the code against the **pinned** version, notes the doc
drift explicitly, and does **not** raise a false "non-conformance" for correct old-version
behavior. If it flags anything, it is the upgrade risk, not a spurious bug.

**Baseline (no talent):** Grabs whatever docs are present (the newer reference) and reports
the renamed field / changed default as a conformance violation — a false positive that
wastes the team's time and erodes trust in the audit. **False positive likely.**

**With talent:** Step 1 pins the exact targeted version; the "Version-pin — audit against
the exact spec version the feature targets; note drift" rule makes it reconcile the pinned
version against the vendored docs and report drift instead of a phantom bug. **Meets
criterion.**

**Result: PASS.** The talent both avoids a false positive and converts it into a genuine,
correctly-scoped finding (version drift / upgrade advisory).

---

## Scoreboard
| # | Scenario | Pass criterion met? | Beats baseline? |
|---|----------|---------------------|-----------------|
| A | CSRF `state` not verified (shared code+test blind spot) | Yes | Yes — catches what green test hid |
| B | S3 503 SlowDown not retried (omitted code path) | Yes | Yes — coverage can't invent it |
| C | Internal diff, no external contract (anti-trigger) | Yes | Neutral — correctly declines |
| D | SMTP spec absent (no audit-from-memory) | Yes | Yes — avoids uncited assumptions |
| E | Stripe version drift (false-positive trap) | Yes | Yes — avoids spurious finding |

**5 / 5 scenarios pass.**

## Watch-items (do not drop the verdict, but track)
1. **Frequent degradation to "ask for the spec."** The no-network security gate plus
   "read docs already available in the repo" means that in real repos, which rarely vendor
   the authoritative RFC / vendor reference, the talent often halts at "please supply the
   spec." This is correct discipline (Scenario D) and never worse than baseline, but it
   caps how often the method runs end-to-end unaided. Not a defect; a usability ceiling.
2. **Scope-over-enumeration risk in the blind suite.** Enumerating ideal cases from a large
   spec (e.g., full OAuth) can generate cases for optional flows the feature never claims
   to implement (device grant, token revocation), which — if reported as gaps — become
   false positives. Step 1 ("name precisely what the feature claims to implement") and
   direction (c) partially guard this, but the method would be stronger with an explicit
   "scope the spec to the feature's declared subset before freezing the oracle" instruction.
   Minor, mitigated by the ranking/severity step; worth a future SKILL tightening.

## Verdict
**PASSED.** On its own functional tests the talent clearly beats a code-first baseline where
it matters most — detecting spec violations that the implementation and its confirmatory
tests jointly conceal (A, B) — while correctly declining out-of-scope work (C), refusing to
launder memory as cited contract (D), and avoiding a version-drift false positive (E). The
two watch-items are inherent trade-offs of the discipline, not cases where it underperforms
baseline.
