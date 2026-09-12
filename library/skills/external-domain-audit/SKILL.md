---
name: external-domain-audit
description: "Use when auditing a large feature or integration against the EXTERNAL specification of the protocol, API, RFC, or vendor SDK it implements — build a knowledge base from the upstream/official docs and design the ideal test suite BLIND (before opening the implementation), then gap-compare code and tests against that spec. Triggers: 'does our OAuth/S3/WebSocket/SMTP/gRPC/payment integration actually follow the spec', 'audit this feature against the standard', 'what conformance cases are we missing', 'independent review of a client/adapter/protocol layer', 'is our implementation faithful to the API contract'. An independent spec-conformance method that reasons from the external contract inward, distinct from diff-based code-review (reads the change), test-coverage (fills gaps on code as written), and behavioral-spec-mining (derives a spec FROM the code). NOT for reviewing a diff, measuring line coverage, or auditing internal-only logic that implements no external contract."
---

# External Domain Audit

Audit a feature against the specification of the external thing it implements — you learn
the contract from the outside world first, so implementation bugs and blind spots can't
launder themselves into your mental model of "correct."

## When to use
- A sizeable feature implements an external contract: a protocol, RFC, public API, file
  format, auth scheme, or third-party SDK, and you want an independent conformance check.
- You suspect the tests were written to match the code (confirmation-shaped), not the spec.
- Onboarding to an integration you didn't build and need to judge its faithfulness.

**Do NOT use** for reviewing a pull-request diff (use code-review), reaching a coverage
threshold on code as-written (test-coverage), recovering intent from undocumented code
(behavioral-spec-mining), or logic that implements no external contract.

## Steps
1. **Name the external contract.** Identify precisely what standard/API/version the feature
   claims to implement. Write it down. If ambiguous, stop and ask — auditing against the
   wrong spec is worse than not auditing.
2. **Build the knowledge base from external docs — BEFORE reading the implementation.**
   Read the authoritative external source (RFC, official API reference, vendor SDK docs,
   format spec) already in the repo, vendored, or provided. Extract into a KB file:
   required behaviors, MUST/SHOULD/MAY clauses, state machines, error codes, edge cases,
   versioning, auth/limits. Cite each to its source section.
3. **Design the ideal test suite BLIND.** From the KB alone — still not having read the
   code — enumerate the conformance cases a faithful implementation must pass: happy paths,
   every error/edge/timeout/retry, boundary values, and negative cases the spec forbids.
   Group by spec clause. This is the oracle; freeze it before step 4.
4. **NOW read the implementation and its tests.** Map each real code path and each existing
   test back to a KB clause and an ideal case.
5. **Gap-compare in three directions.** (a) Ideal cases with no implementation → conformance
   gaps/bugs. (b) Ideal cases with no test → coverage blind spots. (c) Code with no
   backing spec clause → scope creep, misreadings, or undocumented assumptions to flag.
6. **Report by clause, ranked.** For each finding: spec citation, expected vs. actual,
   severity, and the missing test. Rank spec-violating correctness gaps first.

## Rules
- **Docs before code, always.** If you read the implementation before finishing the KB and
  ideal suite, the audit is contaminated — restart the KB from the external source.
- **Method only.** Read docs/specs already available in the repo or handed to you; do not
  fetch over the network, install CLIs, or run auto-run hooks (security gate). Ask the user
  to supply the spec if it isn't present.
- **Cite every claim** to a spec section; an uncited "requirement" is your assumption, not
  the contract.
- **The existing tests are evidence, never the oracle** — they may encode the same bug.
- **Version-pin.** Audit against the exact spec version the feature targets; note drift.

## In this repo (one instance)
Persist the KB and blind suite as `.claude/skills/external-domain-audit/<feature>-kb.md`
before step 4; pair with `eval-harness` to turn the ideal suite into runnable evals and
`verification-before-completion` to gate the "conformant" claim.
