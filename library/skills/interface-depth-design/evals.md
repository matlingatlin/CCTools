# Evals — interface-depth-design

**Talent:** `interface-depth-design` · **Type:** technique (with a discipline core — steps 3–4 and
the Rules forbid concluding from a single design, so the suite carries pressure scenarios too) ·
**Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its method
applied. The talent passes a scenario only if the with-talent result is materially better and meets
the pass criterion. Authored by an INDEPENDENT tester (not the skill author); every scenario is
written against the file's ACTUAL steps, table rows and Rules — cited by number — not against its
self-description.

**Blend:** 13 scenarios — 6 `application (normal)`, 6 clever (4 `pressure`, 2 `edge`),
1 `negative-trigger`. ~46% normal, per CURATION-LESSONS ACTIVE DIRECTIVES.

**Verdict phrasing:** normals end in a plain **PASS** — a capable baseline should often pass the
everyday job, and claiming a win there is the rubber stamp these suites exist to prevent
(CURATION-LESSONS `[2026-08-28]`). **PASS. Beats baseline.** appears only on the six clever
scenarios and on the negative-trigger, where over-triggering is the failure being measured.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 6 normal / 6 clever / 1 negative-trigger.
- [x] **Specific to this talent** — every scenario cites a concrete step, table row or Rule of
      `SKILL.md`; nothing is boilerplate portable to another talent.
- [x] **Observable pass/fail criterion** — each criterion names a countable or quotable artifact
      (a classification, a count of exported names, a named second implementation, a routing).
- [x] **Clever scenarios designed so baseline plausibly FAILS** — S7–S12.
- [x] **Matches talent type** — technique → application normals; the discipline core (steps 3–4,
      step 6, the rationalization table) → four pressure scenarios.
- [x] **Negative trigger covered** — exactly one (S13).
- [x] **Dead cross-refs / invented commands / `name:` / portability / non-TS example accuracy /
      seam-rule self-consistency** — checked, see Structural review.

## Scenarios

## S1 — Eleven-method ReportBuilder · application (normal)
- **Input:** "`ReportBuilder` exports 11 methods (`setRange`, `setFilters`, `addColumn`,
  `setFormat`, `setLocale`, `setTimezone`, `withHeader`, `withFooter`, `paginate`, `build`,
  `buildAsync`) plus 4 config keys. Nine call sites. Every method has at least one caller. The
  interface feels wrong but I can't say why — nothing is unused."
- **Pass criterion (observable):** The answer (i) produces a written surface inventory including
  the four config keys and any ordering constraint (`build` must follow the setters) — step 1;
  (ii) runs the deletion test per call site and classifies the module into exactly one of the
  three step-2 buckets with a stated reason; (iii) produces **three or more** candidate surfaces
  under the named conflicting constraints of step 3 (minimize surface / maximize flexibility /
  optimize the 80% caller), not one design with variations; (iv) compares them on all three step-5
  axes by name, including a *count* of files touched for two named future changes (locality);
  (v) picks a winner and names the axis each loser lost on (step 8). Fails if it returns a single
  recommended interface, however good.
- **Baseline (without talent):** A capable model handles this well — it will notice the builder is
  really "one report, many knobs", propose a single options-object or a `render(spec)` call, and
  argue it convincingly. What it usually skips is producing rival designs and the file-count
  comparison; it presents one answer as the answer.
- **With talent:** Step 5's own diagnosis is the point of leverage — "a wide interface loses only
  in comparison — every one of its eleven methods has a caller, so it is defensible one method at
  a time and indefensible against a three-method design that serves the same call sites" — which
  is why step 3 is marked mandatory. The 80%-caller constraint and the minimize-surface constraint
  land in different places (one obvious `monthlyReport(range)` call plus an escape hatch, versus a
  single `render(spec)`), so step 4's collapse check passes and the comparison is real. **PASS.**

## S2 — Ordering constraint and in-place mutation · application (normal)
- **Input:** "`SessionStore` requires callers to call `attach(conn)` before `load(id)` and to call
  `flush()` before the request ends or writes are lost. It also exposes
  `normalize_claims(claims) -> None`, which edits the caller's dict in place. Reviewers keep
  filing bugs about forgotten `flush()`. What should the surface be?"
- **Pass criterion (observable):** The answer (i) lists the ordering constraints as part of the
  SURFACE, not as documentation — step 1 names ORDERING explicitly as a thing the caller must
  learn; (ii) applies step 7's second heuristic to `normalize_claims`, recommending a return value
  instead of in-place mutation, with the reason given as *ordering and aliasing become part of the
  contract*; (iii) treats "forgot to `flush()`" as evidence for the step-2 *relocated complexity*
  bucket — the lifecycle did not vanish, it was spread over the callers as plumbing. Fails if the
  fix offered is better documentation, a runtime warning, or a lint rule rather than a shape change.
- **Baseline (without talent):** Usually good on the mutation half (return a new dict is standard
  advice) and often reaches "use a context manager / scoped handle" for the lifecycle. It tends to
  offer the doc/lint mitigation alongside as an equally-weighted option.
- **With talent:** Step 1's inclusion of ordering constraints in the inventory forces the lifecycle
  into the surface count, and step 2's third bucket names this exact failure — "the complexity does
  not vanish but simply MOVES … spread over the callers as extra plumbing, wiring, and knowledge of
  ordering … This is the failure mode that looks like success." A doc fix cannot change the ratio in
  step 2's closing line, so it is not a candidate. **PASS.**

## S3 — A module that is genuinely deep · application (normal)
- **Input:** "`RateLimiter` has 2 public methods but ~700 lines inside: a sliding window, clock-skew
  tolerance, a Redis fallback to local counters on outage, and jitter. A new tech lead wants it
  split into `WindowCalculator`, `RedisCounter`, `LocalCounter` and `JitterPolicy` 'so each piece is
  testable'. Is the current interface wrong?"
- **Pass criterion (observable):** The answer runs the deletion test and lands in the *deep* bucket
  — the fallback and skew decisions would reappear in every caller — and therefore recommends
  keeping the 2-method surface, explicitly stating that "keep it as-is" is a legitimate winner
  (step 8). It must also distinguish internal decomposition (private collaborators, no new public
  surface) from moving the split onto the public interface, and note that the proposed 4-part split
  would make callers wire them. Fails if it endorses exposing the four pieces because "smaller
  units are more testable".
- **Baseline (without talent):** Split-into-small-units is a strong prior; the baseline frequently
  agrees with the tech lead, or hedges without a criterion for deciding. It has no vocabulary for
  "this is a good wide-inside/narrow-outside module".
- **With talent:** Step 2's second bucket is exactly this shape ("the same non-obvious decision,
  edge case, or state machine reappears in every caller → the module is deep: it concentrates
  complexity. Keep it."), and the step-2 ratio — hidden complexity over exposed surface — is
  maximal here: two names hide four decisions. Step 8 licenses the no-change verdict. **PASS.**

## S4 — The test that has to patch a private method · application (normal)
- **Input:** "Our test for `UploadQueue` retry behavior does `monkeypatch.setattr(q, '_attempt',
  failing_stub)`. It breaks every time we touch internals. Is the test wrong or is the interface
  wrong?"
- **Pass criterion (observable):** The answer treats the internal-mock requirement as a SURFACE
  signal (it is in "When to use": "A test can only reach the behavior by patching, stubbing, or
  subclassing internals"), not as a testing-hygiene problem; and it names step 8's verification
  condition as the acceptance test for whatever it proposes — "confirm the test that previously
  needed internal mocks can now reach the behavior through the public surface". Fails if the whole
  answer is "make `_attempt` public" or "use a better mocking library" with no surface change and no
  stated verification.
- **Baseline (without talent):** Often diagnoses it correctly as a design smell, but the remedy is
  frequently the cheap one — rename the private method, or extract an interface for the transport
  and mock that (which S7 shows is the wrong move when nothing varies) — and it rarely states a
  checkable after-condition.
- **With talent:** The trigger is listed in "When to use", so the skill fires; step 1 records what
  the test needs to control (failure injection, clock) as part of the surface question; step 8 makes
  the previously-internal test passing through the public surface the explicit verification, so the
  proposal is falsifiable rather than plausible. **PASS.**

## S5 — A boundary that is not a class · application (normal)
- **Input:** "Our public REST endpoint `GET /v2/search` takes 9 query params, and clients must first
  call `POST /v2/search/session` and pass the returned cursor. Third-party integrators keep getting
  the sequence wrong. This is an HTTP boundary, not a module — does interface work even apply?"
- **Pass criterion (observable):** The answer applies the method without conversion — the surface
  inventory covers query params, status codes, error bodies and the two-call ORDERING; the deletion
  test is run against real integrator call sites; at least three rival endpoint shapes are produced
  under the step-3 constraints. It must not decline for being non-object-oriented. Fails if it
  answers with generic REST style advice (naming, versioning, pagination conventions) instead of a
  depth comparison.
- **Baseline (without talent):** Gives competent API-design advice and will likely suggest folding
  the session call in. Its failure mode is drifting into convention advice — the very thing the
  skill routes to `style-inheritance` — and stopping at one proposal.
- **With talent:** The opening scope line is explicit — "Language-neutral: applies to a class,
  package, module, HTTP endpoint, or CLI boundary in any ecosystem" — so nothing needs translating,
  and the "When NOT to use" clause keeps naming/idiom advice out of the answer. **PASS.**

## S6 — A module that builds its own S3 client · application (normal)
- **Input:** "`ingest.py` does `client = boto3.client('s3')` at module import and reads
  `os.environ['BUCKET']` inside `run()`. Tests need `moto` plus a patched environment. How should
  the surface look?"
- **Pass criterion (observable):** The answer applies step 7's first heuristic and takes the client
  and the bucket in as an argument/field, stating the reason as *credentials, region and network
  reachability are currently part of the contract without being listed*. It must accept the
  **concrete** client — it must NOT introduce a `StorageProvider`/`ObjectStore` interface, because
  no second backend is named (step 6). Fails if the recommendation is a new port/protocol/ABC.
- **Baseline (without talent):** Reliably says "inject the client" — this is standard DI advice, and
  the baseline passes the first half easily. It quite often goes one step too far and wraps the
  client in a `StorageProvider` protocol "for testability", adding an interface with one
  implementation.
- **With talent:** Step 7's heuristic supplies the injection, and its own closing rider settles the
  overreach: "But if nothing varies, injecting may only widen the surface — this heuristic answers
  to step 6, not the reverse." Injecting a concrete collaborator and introducing an abstraction over
  it are separated correctly. **PASS.**

## S7 — The single-adapter port, defended as dependency injection · pressure (clever, baseline fails)
- **Input:** "Review our storage layer. `StoragePort` is an interface with 6 methods; `S3Adapter` is
  its only implementation and has been for two years. Four call sites take the port by constructor
  injection; `main.py` wires the adapter in; tests pass a `FakeStorage`. The team is proud of it —
  it's dependency-injected, decoupled and testable, and it passed review twice. Anything wrong?"
- **Pass criterion (observable):** The answer must (i) run the deletion test and conclude that
  deleting the port and adapter leaves callers talking to one real implementation, so **nothing was
  hidden**; (ii) state that the surface got *wider*, and count the added pieces — interface +
  implementation + wiring site (≥3 artifacts, 6 methods of surface); (iii) rebut "it's
  dependency-injected" specifically, on the grounds that injection with one implementation decouples
  from nothing and coupling is measured by what changes together; (iv) rule on the test argument
  against the step-6 exemption list rather than accepting it in general terms. Fails if the verdict
  is "this is fine, it's a clean hexagonal architecture" or if the only criticism offered is that
  6 methods is a lot.
- **Baseline (without talent):** Plausibly fails. Ports-and-adapters with constructor injection and
  a test fake is a textbook-clean pattern; a reviewer without a depth criterion approves it, praises
  the decoupling, and at most suggests trimming a method. The prompt is deliberately loaded with the
  approving vocabulary ("decoupled", "testable", "passed review twice") the baseline pattern-matches.
- **With talent:** This is the file's named hard case, and every clause is load-bearing here. The
  section states the deletion-test outcome directly ("delete the port and the adapter and the
  callers talk to the one real implementation directly — nothing was hidden, and the surface got
  wider by an interface plus an implementation plus a wiring site"), the table rebuts the exact
  rationalization in the prompt ("Injection with one implementation decouples from nothing"), and
  Rule 3 ("One adapter is not a seam. Two are.") makes the verdict non-negotiable. The test defence
  is adjudicated, not waved through: S3 is network, which IS on step 6's exemption list — but the
  exemption licenses a substitutable *client*, not a 6-method port, and S6's separation of injection
  from abstraction is what keeps the two answers consistent. **PASS. Beats baseline.**

## S8 — A fan-out that only looks like a fan-out · pressure (clever, baseline fails)
- **Input:** The engineer reports back from step 3 with three designs for a `PricingEngine` surface:
  (A) `quote(cart, customer) -> Quote`; (B) `getQuote(cart, customer) -> Quote` "with the discount
  rules kept internal"; (C) `priceCart(cart, customer) -> Quote` "optimised for the checkout path".
  "All three converged on the same shape — that's strong evidence it's right. Can we proceed to
  implementation?"
- **Pass criterion (observable):** The answer must REJECT the convergence-as-confirmation reading and
  re-run at least one constraint, giving the reason that the three differ in neither the count of
  exported names (all 1) nor where the seam sits (all at the same boundary). It must name which
  constraint collapsed and re-run it — a checkable action, not a caution. Fails if it accepts the
  convergence as evidence, or merely notes the similarity and proceeds.
- **Baseline (without talent):** Plausibly fails, and fails attractively: three independent designs
  agreeing IS normally strong evidence, and the baseline has no way to see that all three are the
  same design under different verbs. It proceeds to implementation with false confidence.
- **With talent:** Step 4 exists solely for this and gives a mechanical test rather than a judgement
  call: "If all designs expose roughly the same names in the same places, you designed once and
  paraphrased. They must differ in at least the count of exported names OR where the seam sits.
  Re-run the constraint that collapsed." Applied here: name count 1/1/1, seam identical → collapse
  confirmed. The maximize-flexibility constraint is the one that produced no divergence and is the
  one re-run. Step 3's framing ("One design you then defend is not design, it is rationalization")
  supplies the why. **PASS. Beats baseline.**

## S9 — "We'll swap the vendor one day" · pressure (clever, baseline fails)
- **Input:** "We're keeping `EmailProviderInterface` even though SendGrid is the only implementation.
  Leadership has said we may move off SendGrid eventually — pricing keeps changing — and rewriting
  every call site later would be brutal. Surely the optionality is worth one interface?"
- **Pass criterion (observable):** The answer must demand a **named second implementation and a
  date/ship condition** as the price of keeping the seam, and must state the second, less obvious
  half of the objection: a port shaped by one backend usually does not fit the second when it
  arrives. Fails if it accepts unspecified future optionality, or if it rejects the interface without
  offering that name-and-date test as the way to settle it.
- **Baseline (without talent):** Plausibly fails. "Avoid vendor lock-in" is a strong, respectable
  prior with real cases behind it; the baseline typically endorses keeping the interface, and it
  almost never raises the point that the one-backend-shaped port will need rewriting anyway.
- **With talent:** Step 6 states the test as an obligation — "To claim a seam with one adapter, name
  the second implementation and say when it ships" — and the table row supplies the rebuttal in full:
  "Name it and date it. An unnamed second adapter is surface charged today for optionality that may
  never arrive — and the port shaped by one backend usually cannot fit the second anyway." The rule
  is not a blanket ban: a named, dated second provider converts the seam to real, at which point
  step 6's second half (intersection, not union — see S12) governs its shape. **PASS. Beats baseline.**

## S10 — "The interface is wrong but the refactor is too big" · pressure (clever, baseline fails)
- **Input:** "You're right that `JobRunner`'s 14-method surface is wrong. But it has 60 call sites
  across 4 services, we're two weeks from a launch, and the team that owns two of those services is
  offshore. Let's just leave it and note it as tech debt — running your process would burn days we
  don't have."
- **Pass criterion (observable):** The answer must separate the two questions and say so explicitly:
  the deletion test is a thought experiment run *before* pricing the refactor, so the shape question
  can be answered now at low cost, while the migration is scheduled separately. Concretely it should
  still produce the recorded decision (step 8: chosen surface + rejected candidates written to a
  design note/ADR/PR description) even when nothing is migrated this quarter. Fails if it accepts the
  deferral wholesale and produces no analysis, and also fails if it insists the refactor happen
  before launch.
- **Baseline (without talent):** Plausibly fails, in the agreeable direction: the constraints are
  real and sympathetic (launch, 60 call sites, cross-team), so the baseline concedes, files a
  tech-debt note, and produces nothing — which is indistinguishable from never having looked.
- **With talent:** The last table row is written for this excuse: "The deletion test is a thought
  experiment; run it before pricing the refactor. Cost of change is a separate decision from whether
  the shape is right." Step 8 makes the deliverable a written decision including rejected candidates
  — "the record is what stops the next author re-litigating it" — which is precisely the artifact
  that survives a deferred migration, and it explicitly hands the diff to
  `test-driven-development` rather than doing it here. **PASS. Beats baseline.**

## S11 — The complexity vanishes entirely · edge (clever)
- **Input:** "`UserFormatter` wraps our user record: `formatName(u)` returns
  `u.first + ' ' + u.last`, `formatEmail(u)` returns `u.email.toLowerCase()`, `formatId(u)` returns
  `String(u.id)`. Twelve call sites. It's imported everywhere, it's covered by tests, and it gives
  us a place to put formatting later. How should we reshape its interface?"
- **Pass criterion (observable):** The answer must conclude that the module should be **removed**,
  not reshaped — the deletion test's first bucket: callers do the obvious thing directly and nothing
  is duplicated. It must carry "no module at all" as a genuine candidate through the comparison
  (step 3's optional fourth constraint) rather than only reshaping, and must reject "a place to put
  formatting later" on the same name-it-and-date-it grounds as S9. Fails if it returns a tidier
  3-method or 1-method surface for a module that should not exist.
- **Baseline (without talent):** Plausibly fails by answering the question as asked. Given "how
  should we reshape its interface", the baseline reshapes: it proposes `format(u, field)` or a
  `UserView` type, and the existing test coverage plus twelve importers read as evidence the module
  earns its keep. Recommending deletion is not the shape of the question.
- **With talent:** Step 2's first bucket names the outcome ("the callers just do the obvious thing
  directly, and nothing is duplicated → the module is shallow: it added surface and hid nothing.
  Candidate for inlining"), and step 3's fourth constraint — "no module at all — the deletion-test
  outcome as a real candidate" — is what puts deletion on the comparison table where it can win on
  step 5's leverage axis (zero decisions removed ÷ three names exposed). Test coverage of a shallow
  module is coverage of surface, not evidence of depth. **PASS. Beats baseline.**

## S12 — Two real adapters: intersection, not union · edge (clever)
- **Input:** "We now genuinely have two: `PostgresEventStore` (live) and `DynamoEventStore` (ships
  next month, contract signed). The proposed `EventStore` interface has 9 methods — the 5 both
  support, plus `beginTransaction`/`commit`/`rollback` (Postgres only, no-ops on Dynamo) and
  `queryByGsi` (Dynamo only, throws on Postgres). Two call sites use transactions today. Sign off?"
- **Pass criterion (observable):** The answer must (i) confirm the seam is now REAL — two
  implementations, one named and dated — rather than repeating the one-adapter objection; (ii)
  reject the 9-method union and require the INTERSECTION of what both genuinely need; (iii) refuse
  the no-op and throwing methods by name, because a method that no-ops on one backend puts a
  correctness rule back into every caller (step 2's relocated-complexity bucket); (iv) resolve the
  two transaction call sites explicitly — either the seam is misplaced or transactions stay outside
  the port — instead of silently dropping a capability a real caller depends on (step 3's
  minimize-surface constraint still must "serve every real call site"). Fails if it signs off on the
  union, or if it prescribes a bare intersection without saying what happens to the two transactional
  callers.
- **Baseline (without talent):** Plausibly fails on (ii)–(iv). The union is how this is normally
  built, and no-op/throwing methods on an interface are so common they read as ordinary. The baseline
  typically approves with a note to document which backends support which methods — which is exactly
  the ordering/capability knowledge being pushed back onto callers.
- **With talent:** Step 6 supplies both halves in one sentence — "TWO adapters make the seam real —
  and the interface should then be the INTERSECTION of what both genuinely need, not the union" — so
  the two-implementation fact changes the verdict on the seam without changing the verdict on the
  width. Step 5's seam-placement axis ("does anything real vary across this boundary today?") is what
  exposes `queryByGsi` and the transaction trio as things that do NOT vary across the boundary but
  across one side of it. **PASS. Beats baseline.**

## S13 — A payments service that does not exist yet · negative-trigger
- **Input:** "I'm going to build a new payments service for our marketplace — split payouts, refunds,
  chargebacks, multi-currency. How should it look? What should its interface be?"
- **Pass criterion (observable):** The talent must DECLINE and route to `brainstorming`. Observable:
  the response does not run a surface inventory, a deletion test or a fan-out, and it names
  `brainstorming` as the right next step. Fails if it starts designing candidate surfaces for a
  module that has no call sites.
- **Baseline (without talent):** Not a capability discriminator — the failure being measured is
  over-triggering. An agent cued only by the talent's topic ("interface", "how should it look",
  "what should its surface be") reads this as squarely in scope and starts step 3, producing three
  rival surfaces for a service whose behavior nobody has decided. That output is unfalsifiable by
  this method: steps 2 and 5 both measure against a real call-site inventory, and there are no call
  sites, so leverage and locality cannot be computed at all.
- **With talent:** Both gates catch it independently. The `description` opens with the precondition —
  "Use when a module, class, or package ALREADY EXISTS" — and its NOT-clause routes this case by
  name ("NOT for exploring what to build before it exists (use brainstorming)"); "When NOT to use"
  repeats it. The bait is deliberate: the prompt uses the talent's own trigger words ("how should it
  look", "interface"), and the discriminator is not vocabulary but the existence of call sites.
  **PASS. Beats baseline.**

## Structural review (independent checks demanded by CURATION-LESSONS)
- **Frontmatter:** `name: interface-depth-design` present and matches the directory;
  `description:` present, with an explicit precondition and four NOT-clauses. OK.
- **Dead cross-references:** all five named siblings exist under `.claude/skills/` —
  `brainstorming`, `decision-council`, `behavioral-spec-mining`, `style-inheritance`,
  `test-driven-development`. No rot. (Verified by directory listing, not by memory.)
- **Invented slash-commands / built-ins:** none. A grep for `/token` patterns over the file returns
  zero hits; the only backticked identifiers are the five sibling talents plus `open`/`read` used as
  illustrative method names in step 1.
- **Format drift:** tests live in this `evals.md`; the talent directory contains only `SKILL.md` and
  this file — no `evals/` JSON directory. OK.
- **Portability:** no hooks, no credentials, no CLI or package install — stated in Rules and true of
  the content. Step 3 dispatches read-only design subagents but Rule 4 scopes that to "ordinary
  delegation", and the load-bearing requirement is three *conflicting* designs, which a single agent
  can produce sequentially; the delegation is a mechanism, not a dependency. The "In this repo"
  section names no file paths, so it cannot rot. OK.

### (a) Seam-rule self-consistency — is "one adapter = hypothetical, two = real" contradicted by the injection heuristic?
Checked all six sites where the rule or the injection heuristic appears (description; step 5 axis 3;
step 6; step 7 heuristic 1; hard-case section + table rows 1 and 3; Rule 3). **Consistent — and the
one place it could have gone wrong is explicitly handled.** Step 7's "take dependencies in; do not
construct them" is the classic route to accidentally re-deriving a port ("inject it, so abstract
it"), and the file closes that route in the heuristic's own last sentence: *"But if nothing varies,
injecting may only widen the surface — this heuristic answers to step 6, not the reverse."* The
distinction it relies on — injecting a **concrete** collaborator versus introducing an
**abstraction** over it — is what makes S6 and S7 come out differently, and it holds under both.
The table row "Injection with one implementation decouples from nothing" restates the same
subordination. No contradiction found. *Polish note (non-blocking):* the concrete-vs-abstract
distinction is what does the work but is never named in those words; a reader could take "accepting
the client as a field/argument" to mean "accept an interface". One clause would remove the ambiguity.

### (b) Non-TS examples — counted through, one at a time
- **Python, `client = boto3.client("s3")` at import time → credentials, region and network
  reachability become part of the contract.** **Correct as a contract claim.** Any caller or test of
  the module must now supply AWS credentials, a region and network access, and cannot substitute
  them, because the module resolves all three itself. *Precision footnote (not an error):* of the
  three, only region is enforced at construction — `boto3.client("s3")` with no region configured
  raises `NoRegionError` immediately, whereas credentials are resolved lazily at request-signing
  time and no network call occurs at client construction. The file does not claim import-time
  failure, so the sentence stands as written.
- **Go, a function reaching for `http.DefaultClient` and `os.Getenv` internally.** **Correct.**
  Both are real: `http.DefaultClient` is a package-level `*http.Client` in `net/http` and
  `os.Getenv` is the standard env accessor; both are process-global reach-ins that weld transport
  policy and environment into the function's contract. The example is if anything understated —
  `http.DefaultClient` carries no timeout, so its policy is inherited invisibly too.
- **Go/C, `Parse(in, out *Doc) error` versus `Parse(in) (Doc, error)`.** **Correct.** The
  multi-return form is valid Go and is the idiomatic value-returning shape; the out-pointer form is
  valid Go and the ordinary C idiom, and it is the one that makes aliasing and initialization state
  the caller's problem. Signature sketches omit parameter types, which is consistent with the file's
  "illustrations only" framing.
- **Python, `normalize(records) -> None` mutating in place versus returning a new list.**
  **Correct.** Valid annotation syntax, and `-> None` is exactly the signal that the effect is
  invisible in the return type — the point being made.
- **Rust `&mut` as a case where in-place mutation is the ecosystem's idiom and ownership/aliasing
  become part of the contract.** **Correct.** `&mut T` is an exclusive borrow, so mutation is
  expressed in the type and exclusivity is guaranteed. *Precision footnote (not an error):* in Rust
  that contract is compiler-**enforced** rather than merely documented, which is a stronger claim
  than the file makes, not a weaker one; the cost the file says to "pay deliberately" — the
  contract's complexity — still applies. The pairing with "numeric buffers" is apt.
  **No incorrect example found in any of the five.**

### Other findings
- **Worked Example, non-blocking imprecision.** The Example collapses a 7-method `NotificationPort`
  over a single `EmailAdapter` and verifies with "Retry is now testable through the public call with
  an injected clock". The clock covers backoff timing but not *failure injection*: to test retry the
  transport must be made to fail, and email delivery is network, which is on step 6's own exemption
  list. The rules reach the right answer — inject the concrete transport (step 7a), do not resurrect
  a 7-method port (step 6) — but the Example names only the clock, so read literally it under-delivers
  on step 8's verification requirement. One extra clause ("with an injected clock and transport")
  would close it. Recorded as polish, not a defect: no rule is contradicted.
- **Intersection rule, missing rider.** Step 6's "the interface should then be the INTERSECTION of
  what both genuinely need" is stated without saying what to do when a real call site needs a
  capability only one implementation has (S12's transactional callers). Step 3's minimize-surface
  constraint ("that still serve every real call site") supplies the answer to a careful applier — the
  seam is misplaced, or the capability stays outside the port — but the rider is not local to the
  rule. Recorded as polish; S12 passes because the two steps compose.

## Failure triage (if any scenario failed)
No scenario failed; no triage required. The two polish notes above and the concrete-vs-abstract
naming gap in (a) are wording improvements, not skill-bugs: in each case the file's rules, applied
as written, produce the correct answer.

## Result summary
- Scenarios passed: 13/13 · failure_cause: none · verdict: passed
