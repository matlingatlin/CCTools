# Layer E · triage of the mined findings

**Date: 2026-08-26.** Every row below was read at its source line in `docs/mined/`. Nothing here
is a summary of a summary.

Layer E is build and execution: the sandbox, the relay, the five gates, the repair loop, the
spend ceiling. The four verified defects the mining was read against — and which several
findings land on directly — are:

1. **The money is in the wrong loop.** The relay's four passes are intrinsic self-correction
   (`relay.py:148-167` gives pass *n* the prompt and pass *n−1*'s answer, no gate output at all)
   while the loop that *does* get gate feedback is capped at three
   (`docs/next/LAYER-E-BUILD.md` §2.1).
2. **Nothing runs the generated app's tests**, and `check_tests_present` matches the bare
   substring `test`, so `app/latest/page.tsx` satisfies it (`validation.py:132`, §1.1g).
3. **The two interaction gates are opt-in and have nothing to check** — measured **0**
   `interaction` criteria on the canonical spec (§1.1b).
4. **The build that hits its ceiling is the one the ledger under-reports most** — `BudgetExceeded`
   discards the whole `RelayResult` and `cost_usd` defaults to `0.0` (`loop.py:550`, §1.1c).

---

## How the scope was determined

`scripts/findings-index.py` reports Layer E at 44 findings, plus `E/F` 8, `E/G` 4 and `C/E` 6.
Its own docstring says to treat counts as a floor, and they are one: the layer regex reads the
first standalone `A`–`G` word in a row, case-insensitively, so **row 53 of `PASS2-ECC-SKILLS.md`
— score caps, marked `E, F` — is filed under layer `A`** because the phrase *"set **a** ceiling"*
matched first. Several `E · gate` and `E, with C` rows land the same way.

So the set below is the union of the index's `E`, `E/F`, `E/G`, `C/E`, `D/E`, `B/E` and `E/B`
buckets with a direct scan for rows whose *layer cell* names E, plus three rows from the
`— none —` bucket that plainly belong here (the plateau detector and two build-process
exclusions). **104 mined findings**, plus one of this repository's own verified defects (row 105)
listed because five mined rows land on it and a triage that stayed silent would be hiding the
overlap.

## Verdicts

| Verdict | Count | Means |
|---|---:|---|
| **SKILL** | 58 | a decision procedure — what exists in a domain and how to choose, or a rule for a recurring situation |
| **ADR** | 27 | a decision about what to build or change. Recorded here; it goes to `docs/decisions/` later, not into a skill |
| **FIX** | 9 | a specific defect with a specific repair |
| **DROP** | 11 | with the reason stated |

**58 SKILL rows are not 58 skills, and they are not even 58 findings.** At least nine are the same
rule arriving from a different repository — the plateau detector is in `ECC-AGENTS` and
`ECC-SKILLS` (rows 2, 8), the durable failure note is in `ECC-SKILLS` and
`PASS2-ECC-RULES-COMMANDS` (rows 10, 39), cost-ordered gates with stop-on-fail is in `ECC-SKILLS`
and `PASS2-ECC-RULES-COMMANDS` (rows 5, 41), the quote-or-suppress evidence rule is in
`ECC-AGENTS` and `PASS2-GSTACK-SKILLS` (rows 3, 62), and the three-strike stop is in
`OTHERS-MINED`, `PASS2-ECC-RULES-COMMANDS` and `PASS2-GSTACK-SKILLS` (rows 30, 43, 92). Collapsed,
they are **three new skills and one amendment**:

| Destination | Rows | What it decides |
|---|---:|---|
| `gate-verdicts` *(new)* | 25 | what a gate may report, and when PASS is reachable |
| `build-loop-stops` *(new)* | 17 | when an autonomous build or repair loop stops, and what it records |
| `testing` *(amend)* | 10 | evidence from a test run — its counts, its controls, its freshness |
| `spend-ceilings` *(new)* | 7 | caps, meters and ledgers that cannot fail open |

(25 + 17 + 10 + 7 = 59 against 58 rows: row 19 splits between two destinations.)

---

## The table

Sorted by source. `Item` is the finding as its document states it, shortened.

| # | Item | Source · line | Verdict | Destination |
|---|---|---|---|---|
| 1 | SessionStart injection budget — floor + cap + byte budget + relevance boost | `ECC-MINED.md:386` | DROP | Our session-context loading, not the product's build. Belongs to build-process triage |
| 2 | Plateau detector — stop when the finding set stops changing | `ECC-AGENTS.md:627` | SKILL | `build-loop-stops`. Our gates emit structured findings, so a repeat finding set is a **set comparison, not a judgement**. Their threshold of 15 is unbacked; take the detector, leave the number |
| 3 | `agent-evaluator`'s evidence rule — no top score without `file:line` | `ECC-AGENTS.md:626` | SKILL | `gate-verdicts`. Second statement of row 62 below, from a different repository |
| 4 | `TOTAL_BUDGET_MS` split across batches before dispatch | `ECC-AGENTS.md:629` | DROP | Our fan-out, not the product's. Build-process triage |
| 5 | Per-stack ordered gate pipeline with stop-on-fail | `ECC-SKILLS.md:647` | SKILL | `gate-verdicts`. Only the shape. Our order already exists and `docs/next` §2.3 shows the 2026 literature arrived at it independently — the rule is *do not reorder without answering `loop.py:16`* |
| 6 | `data-testid` on every interactive and list element, derived from `PackageInterface` | `ECC-SKILLS.md:648` | ADR | Playbook / emitter content. Amended by row 76; belongs to Layer B and F |
| 7 | **Fed repair loop: gate output → fresh context → fix → re-check, capped** | `ECC-SKILLS.md:651` | SKILL | `build-loop-stops`. The gate stays the oracle; its output is the repair's *input*, never a substitute |
| 8 | Plateau stop — halt when three iterations stop improving | `ECC-SKILLS.md:652` | SKILL | `build-loop-stops`. Same finding as row 2, arrived at independently |
| 9 | Completion signal with an N-consecutive threshold | `ECC-SKILLS.md:653` | SKILL | `build-loop-stops`, with the limit stated: meaningful only *alongside* gates, never instead of them |
| 10 | `SHARED_TASK_NOTES.md` — durable cross-iteration notes, as a file | `ECC-SKILLS.md:654` | SKILL | `build-loop-stops`. Must carry *what was tried and why it failed*, not a summary |
| 11 | Size classifier → gate mask (three signals, highest wins, user-overridable) | `ECC-SKILLS.md:655` | ADR | Ceremony tiers change which gates run on which build. That is a decision, not a procedure |
| 12 | The seven security triggers (authn/authz, user input, DB query, FS path, external call, crypto, secrets) | `ECC-SKILLS.md:656` | ADR | Playbook text, verbatim. Layer G's surface as much as E's |
| 13 | Rule 10 — `[revised]` protocol, re-present only changed criteria | `ECC-SKILLS.md:659` | ADR | Needs a back-edge from build failure to spec that does not exist |
| 14 | Content-hash cache keys instead of identity keys | `ECC-SKILLS.md:664` | ADR | Prompt caching is listed as missing entirely (`as-built` §6). Cache-key design is part of that decision |
| 15 | Derived eval mode per package (`playwright` / `screenshot` / `code-only`) | `ECC-SKILLS.md:666` | ADR | `code-only` is a mode Layer E does not have. Adding one is a build decision |
| 16 | TDD Evidence Report table (guarantee · test · type · result · evidence command) | `ECC-SKILLS.md:669` | SKILL | `testing` — it is an output contract, and `testing` §9 already has one to extend |
| 17 | `pass@k` vs `pass^k` | `ECC-SKILLS.md:671` | SKILL | `testing` §8. Vocabulary we do not have for flaky gates |
| 18 | Warn-only regex channel for rationalisation, unreliability stated in the file | `ECC-SKILLS.md:672` | SKILL | `gate-verdicts`. A channel that never gates must say so in the file. Layer E may add evidence channels; it may not convert deterministic ones to judgement |
| 19 | Auto-wait locators over sleeps; `retain-on-failure` traces as gate evidence | `ECC-SKILLS.md:673` | SKILL | `testing` §6 (browser level). The trace-as-evidence half is `gate-verdicts` |
| 20 | `santa-method` — dual independent reviewers, both must pass | `ECC-SKILLS.md:676` | DROP | Excluded by its own limits section: *"do not use for tasks with deterministic verification"*, which is Layer E |
| 21 | `gan-style-harness` four-criterion weighted rubric and its numbers | `ECC-SKILLS.md:677` | DROP | Unvalidated weights; `app-design` §5's six deterministic checks are the better instrument |
| 22 | `tdd-workflow` Step 0 test-runner detection matrix | `ECC-SKILLS.md:679` | DROP | Exists to cope with a repo you did not write. We write the repo |
| 23 | Scan-at-sink on the exact bytes, from the file that is passed downstream | `OTHERS-MINED.md:721` | SKILL | `gate-verdicts`. A check runs on the artefact that travels, not on an earlier copy of it |
| 24 | Cost estimator publishes its error band, its calibration corpus and its expiry condition | `OTHERS-MINED.md:727` | SKILL | `spend-ceilings`. `estimate.py` is calibrated against three real runs and says so; it does not publish an expiry, and §1.1e shows the calibration is now against a different `_cost` |
| 25 | Per-build ledger: identity first line, append-only completion lines, resume from the file | `OTHERS-MINED.md:747` | ADR | A resume mechanism. Sits squarely inside ADR-0020's queue question |
| 26 | **Rulings not stalls: closed 4-item stop list + `Ruling: what — why — cost if wrong`** | `OTHERS-MINED.md:748` | SKILL | `build-loop-stops`. The closed stop list is the autonomy boundary; the *cost-if-wrong* field is the one everyone omits |
| 27 | Fix-round circuit breaker: 5 rounds, escalate model+context at R≥4, defined terminal state | `OTHERS-MINED.md:749` | SKILL | `build-loop-stops`. Our gates retry; they neither escalate nor have a defined give-up state |
| 28 | Model selection as a routing table by role; review model scaled to diff risk | `OTHERS-MINED.md:750` | ADR | `matrix.yaml` is data, but *which* rankings exist and what routes to them is a decision (see row 51) |
| 29 | An agent's success report is not evidence; verify the artefacts it produced | `OTHERS-MINED.md:752` | SKILL | `gate-verdicts`. A report is a claim; the diff is the evidence |
| 30 | 3 failed fixes = wrong architecture, not a failed hypothesis | `OTHERS-MINED.md:753` | SKILL | `build-loop-stops` for the stop; the back-edge from build failure to architecture does not exist and is an ADR |
| 31 | Condition-based waiting: poll the condition, name it in the timeout, getter inside the loop | `OTHERS-MINED.md:754` | SKILL | `build-loop-stops`. Take as-is for sandbox and preview waits |
| 32 | Four-part agent brief: scope · goal · explicit constraints · specified output shape | `OTHERS-MINED.md:755` | ADR | Prompt composition. Pairs with row 63's constraint on `assemble_build_context` |
| 33 | `fetch(` in a route handler or server action with no `signal:` / `AbortSignal.timeout` | `PASS2-ECC-RULES-COMMANDS.md:669` | FIX | One regex into `_QUALITY_PATTERNS`, warning, connector packages only |
| 34 | An insert/update whose argument is a whole request body rather than a named object | `PASS2-ECC-RULES-COMMANDS.md:670` | FIX | One regex into `_UNSAFE_PATTERNS` |
| 35 | Non-literal argument to `.order(` / `.filter(` | `PASS2-ECC-RULES-COMMANDS.md:671` | FIX | One regex into `_QUALITY_PATTERNS` |
| 36 | A migration containing `DROP` whose first line is not a comment | `PASS2-ECC-RULES-COMMANDS.md:672` | FIX | SQL scan; joins the existing migration checks |
| 37 | Any model-chosen filename or slug: validate `[a-z0-9-]+`, resolve, assert inside root | `PASS2-ECC-RULES-COMMANDS.md:673` | FIX | The write path. `sandbox.py:125` (`_guard_path`) already does resolve-then-verify-prefix for the sandbox; this is the same rule for every other model-chosen name |
| 38 | **Predicted vs Actual** recorded per package after every build | `PASS2-ECC-RULES-COMMANDS.md:684` | ADR | Named in the source row as feeding ADR-0016 |
| 39 | A failure ledger on the build job: what was tried, why it failed, do not retry | `PASS2-ECC-RULES-COMMANDS.md:686` | SKILL | `build-loop-stops`. Same finding as row 10, from a different repository |
| 40 | Explicit decision table (APPROVE / COMMENT / REQUEST CHANGES / BLOCK), not just severities | `PASS2-ECC-RULES-COMMANDS.md:687` | SKILL | `gate-verdicts`. The outcome vocabulary is the gate's contract |
| 41 | Order validation by cost: static → unit → build → integration → edge cases, stop at first failure | `PASS2-ECC-RULES-COMMANDS.md:688` | SKILL | `gate-verdicts`. Same finding as row 5 |
| 42 | Repair loop: one change, verified, `git checkout --` on failure, skip the item; SAFE/CAUTION/DANGER tiers | `PASS2-ECC-RULES-COMMANDS.md:689` | DROP | Marked *skip* at source. Our rollback is narrower and already exists (`loop.py:_restore`); the tiers are Layer F's question |
| 43 | Non-convergence detectors: same error 3× → stop; a fix creating more errors than it resolves → stop | `PASS2-ECC-RULES-COMMANDS.md:690` | SKILL | `build-loop-stops` |
| 44 | Dual review, context-isolated, fresh reviewers each round, max 3 rounds, then escalate | `PASS2-ECC-RULES-COMMANDS.md:691` | SKILL | `build-loop-stops` — the *fresh context per round* half only. Dual review is row 20, dropped |
| 45 | **Use a score only where a gradient is needed; use a verdict + checklist for decisions** | `PASS2-ECC-RULES-COMMANDS.md:697` | SKILL | `gate-verdicts`. The rule that decides whether a gate returns a number at all |
| 46 | Unindexed-foreign-key detection over the generated migration set | `PASS2-ECC-SKILLS.md:649` | FIX | Deterministic, no model, cheap. Belongs early in `loop.py`'s gate ordering |
| 47 | `SELECT`-clause omission as a build-time check | `PASS2-ECC-SKILLS.md:651` | ADR | Needs Layer B's schema intersected with Layer C's promised fields. Cross-layer plumbing, not a patch |
| 48 | The four-fix self-review trace | `PASS2-ECC-SKILLS.md:652` | DROP | An n=1 field instance. It is a citation line beside Huang/Kamoi/Kiecker in `docs/next` §2.1, not a skill |
| 49 | Name generated tests after the failure they prevent, not the function they cover | `PASS2-ECC-SKILLS.md:653` | SKILL | `testing` |
| 50 | Six click-path bug patterns + side-effect-map-first ordering | `PASS2-ECC-SKILLS.md:654` | ADR | Deriving a side-effect map from the architecture graph is a new mechanism |
| 51 | Fact-forced repair: demand facts obtainable only by tool call | `PASS2-ECC-SKILLS.md:655` | SKILL | `build-loop-stops`. Cheaper than row 7 and complementary to it. Their evidence is n=2, self-run, unblinded — a mechanism, not a number |
| 52 | Condense repeated identical injected blocks after N occurrences | `PASS2-ECC-SKILLS.md:656` | ADR | Changes the relay. Needs an eval, not a citation |
| 53 | **Score caps: binary deterministic conditions set a ceiling a judgement score may not exceed** | `PASS2-ECC-SKILLS.md:657` | SKILL | `gate-verdicts`. The missing *arithmetic* of the rule that judgement may not overrule a deterministic check |
| 54 | Reviewer receives the artefact and the criterion only — never the build transcript | `PASS2-ECC-SKILLS.md:661` | SKILL | `gate-verdicts`. One checkable constraint on `assemble_build_context`, strictly stronger than "the reviewer is a different call" |
| 55 | Error contract per gate: root-cause hint · safe retry instruction · explicit stop condition | `PASS2-ECC-SKILLS.md:662` | SKILL | `gate-verdicts` for the contract; it is what makes rows 8 and 9 expressible *per gate* instead of globally |
| 56 | Two packages may build in parallel exactly when their file plans are disjoint | `PASS2-ECC-SKILLS.md:665` | ADR | Parallelism is deliberately deferred (`orchestrate.py:19`). The rule is computable; whether to run it is a decision |
| 57 | Cross-tenant read returning zero rows, generated beside every RLS policy | `PASS2-ECC-SKILLS.md:667` | ADR | A generation decision for Layers B and C |
| 58 | Leak vectors as greps: no identifiers in URLs, storage, logs; no `service_role` key client-side | `PASS2-ECC-SKILLS.md:668` | ADR | Playbook text; Layer G's surface |
| 59 | **Honest status gains a *what must be true to say this* column** | `PASS2-ECC-SKILLS.md:669` | SKILL | `gate-verdicts`. *"Do not treat 'present in config' as 'working'"* is our `check_tests_present` bug written as a rule by someone doing billing triage |
| 60 | Spend limits enforced outside the model; audit-log refused and halted runs, not only successful ones | `PASS2-ECC-SKILLS.md:670` | SKILL | `spend-ceilings`. Metering that counts only completed builds cannot answer a disputed bill — which is defect 4 exactly |
| 61 | `transition: all` and `will-change: all` as `_QUALITY_PATTERNS` greps | `PASS2-ECC-SKILLS.md:672` | FIX | Two regexes. Both are model defaults; a linter could have guaranteed them |
| 62 | Pre-emit gate: quote the motivating line or force confidence to 4-5 | `PASS2-GSTACK-SKILLS.md:683` | SKILL | `gate-verdicts`. No finding without a verbatim quote, and no inventing confidence to route around it |
| 63 | Hydration family as one Playbook line + one grep | `PASS2-ECC-SKILLS.md:675` | ADR | Playbook; Layer B |
| 64 | Amend: `data-testid` is Layer F's anchor, not Layer E's selector | `PASS2-ECC-SKILLS.md:679` | ADR | Generate the attribute for markings→code; generate the *test* against role and label |
| 65 | *"Omit principles you checked but did not change"* | `PASS2-ECC-SKILLS.md:680` | SKILL | `gate-verdicts`. Honest status pads with no-ops |
| 66 | `agent-self-evaluation` as a workflow | `PASS2-ECC-SKILLS.md:684` | DROP | Shipped beside `gateguard`'s *"self-evaluation doesn't work, verified experimentally"* with no cross-reference. Its Evidence Rule is row 3 |
| 67 | `gan-style-harness`'s weighted composite — second argument for leaving it | `PASS2-ECC-SKILLS.md:686` | DROP | Their own rubric-design skill forbids what their flagship harness does |
| 68 | 12-layer agent-stack diagnostic vocabulary, incl. layer 11 "hidden repair loops" | `PASS2-ECC-SKILLS.md:664` | DROP | A checklist to run over `docs/next/`, across all seven layers. It names our defect as a known class; that is a citation, not a skill |
| 69 | Package lifecycle enum + declared transition table; an unmatched status report throws | `PASS2-FOUR-REPOS.md:626` | ADR | A typed state machine is a design change to `orchestrate.py` |
| 70 | The terminal state is reachable only by an explicit call — no auto-advance into "done" | `PASS2-FOUR-REPOS.md:627` | ADR | Same ADR as row 69. A wrong `done` ships an app |
| 71 | **Arithmetic coherence gate on reported test results**: sum check, RED≥1 failure, GREEN≥1 pass, count regression | `PASS2-FOUR-REPOS.md:628` | SKILL | `testing`. Four integers make the two cheapest ways to fake a green build detectable without reading any code |
| 72 | `previousTestCount` is required, not optional | `PASS2-FOUR-REPOS.md:629` | SKILL | `testing`. *A check that is off by default is off* — the same shape as `SCIO_VERIFY_DATA` |
| 73 | "Already satisfied" is a first-class outcome at both ends | `PASS2-FOUR-REPOS.md:630` | ADR | Layer D's assembly match and this outcome are one state and are currently modelled twice |
| 74 | Closed set of sentinel completion tags with a named reason; `blocked` distinct from success and error | `PASS2-FOUR-REPOS.md:634` | SKILL | `build-loop-stops`. Four outcomes, three terminal, two carrying a reason the agent wrote — as a tag, so the harness decides |
| 75 | Finish-what-is-started before starting new work, stated as policy | `PASS2-FOUR-REPOS.md:635` | ADR | Only bites if Layer E runs packages concurrently — the same ADR as row 56 |
| 76 | `mkdir`-as-mutex, owner token recorded, 10-min stale reclaim, skip the cycle rather than queue | `PASS2-FOUR-REPOS.md:641` | ADR | A concurrency mechanism, shared with Layer D |
| 77 | Path validation is resolve-then-verify-prefix, never match-then-deny-known-bad | `PASS2-FOUR-REPOS.md:651` | DROP | Already implemented correctly for the sandbox at `sandbox.py:125`. The uncovered write paths are row 37 |
| 78 | Degrade best-effort, and publish the residual failure, its bound, and why the bound is acceptable | `PASS2-FOUR-REPOS.md:654` | SKILL | `gate-verdicts`. A degraded run must carry its own disclosure into its output |
| 79 | Never cache a failed initialisation — assign the singleton only after `init()` returns | `PASS2-FOUR-REPOS.md:655` | FIX | One retry path, no permanently-poisoned worker. **No site verified in our engine**; this is an audit to run, not a patch to apply blind |
| 80 | **Fail-closed verdict: five ordered checks, no default branch, four named unverifiable states** | `PASS2-GSTACK-SKILLS.md:679` | SKILL | `gate-verdicts`. The core of it. *"No `[P1]` substring and no critical findings are different claims"* |
| 81 | Verification modes + 5 outcome states + path-concreteness + honesty rule | `PASS2-GSTACK-SKILLS.md:682` | SKILL | `gate-verdicts`. DONE / PARTIAL / NOT DONE / CHANGED / UNVERIFIABLE. *"The gate could not run" is never DONE* |
| 82 | Fail-closed hook polarity + symlink final-component + additive-only config + narrow hard-deny | `PASS2-GSTACK-SKILLS.md:684` | SKILL | `gate-verdicts` for the polarity rule (*a boundary that fails open is not a boundary*). "Project rules may only tighten Playbook rules" is an ADR |
| 83 | WTF-likelihood thrash score + hard iteration cap | `PASS2-GSTACK-SKILLS.md:685` | SKILL | `build-loop-stops`, adapted: a thrash metric as well as a spend ceiling. Their coefficients are theirs — ours would need calibration, so the skill takes the *shape* and says so |
| 84 | *"Convenience flow, not a safety mechanism"* + "What it does NOT touch" + "Reversibility" | `PASS2-GSTACK-SKILLS.md:686` | SKILL | `gate-verdicts`. Every gate declares whether it is the enforcement point, and names the real one if not |
| 85 | Fix-First heuristic: mechanicality decides autonomy, severity biases toward asking | `PASS2-GSTACK-SKILLS.md:692` | SKILL | `build-loop-stops` (the autonomy boundary). Layer F owns the auto-apply half |
| 86 | A suppression list shipped alongside every checklist | `PASS2-GSTACK-SKILLS.md:693` | SKILL | `gate-verdicts`. *"Or the checklist is ignored within a month"* |
| 87 | Two confidence gates + 5-band display policy; low-confidence labelled and demoted, never deleted | `PASS2-GSTACK-SKILLS.md:699` | SKILL | `gate-verdicts` |
| 88 | Adaptive gating with `[NEVER_GATE]` exemptions | `PASS2-GSTACK-SKILLS.md:700` | ADR | Pruning checks on measured hit rate changes what runs, and needs a measurement first |
| 89 | Only actions are idempotent; verification always re-runs | `PASS2-GSTACK-SKILLS.md:701` | SKILL | `gate-verdicts`. Inability to prove freshness means re-run, not pass. The evidence-ledger half is row 93 |
| 90 | Fingerprint-group-boost for agreeing reviewers; **missing voice = N/A, never agreement** | `PASS2-GSTACK-SKILLS.md:702` | SKILL | `gate-verdicts`. An absent reviewer never counts as consensus |
| 91 | Adversarial prompt: authorization preamble, fixture summary-mode, format-graded `Recommendation:` line | `PASS2-GSTACK-SKILLS.md:704` | SKILL | `gate-verdicts`. *"Because it's safer" fails the format* |
| 92 | 3-strike rule, >5-file blast-radius gate, scope lock reusing the sandbox boundary | `PASS2-GSTACK-SKILLS.md:708` | SKILL | `build-loop-stops`. One boundary mechanism, two entry points |
| 93 | Positive control paired to every absence test | `PASS2-GSTACK-TESTS.md:694` | SKILL | `testing` — **already there** at §3.5, written from the same source before this triage. *"A harness that silently under-reports is worse than no harness"*. Listed so the row is not triaged twice |
| 94 | **Exit 0 is not evidence**: declared lanes + executed-unit count + no failure lines | `PASS2-GSTACK-TESTS.md:697` | SKILL | `testing`. Refuse a zero exit when fewer test files ran than planned — "invisible non-execution" |
| 95 | Evidence ledger: FRESH / STALE / MISSING bound to a working-tree hash | `PASS2-GSTACK-TESTS.md:698` | SKILL | `testing`. A claim bound to the bytes it was made about |
| 96 | Override = reason string + audited JSONL with branch and commit | `PASS2-GSTACK-TESTS.md:700` | SKILL | `spend-ceilings`. Boolean overrides get set once and never unset; a reason string in a log gets read at review |
| 97 | Relative-ratio regression **and** absolute hard cap, both present, purposes stated | `PASS2-GSTACK-TESTS.md:701` | SKILL | `spend-ceilings`. Two instruments; neither substitutes. With first-run grace, a noise floor, and same-branch-only comparison |
| 98 | Timeout derived from the plan's worst case × margin, from a live census | `PASS2-GSTACK-TESTS.md:702` | SKILL | `spend-ceilings`. Our build timeout must be `f(build plan)` or Layer C growth silently truncates builds |
| 99 | Receipt-before-send + fail-open/fail-closed polarity table asserted with exact `toEqual` | `PASS2-GSTACK-TESTS.md:704` | ADR | Requires enumerating every place bytes leave. Layer G owns the egress inventory |
| 100 | Never render a missing value as a good value: trusted / unverified / unknown / error | `PASS2-GSTACK-TESTS.md:706` | SKILL | `spend-ceilings` for meters. *A zero from a broken pipe reads as good news* — which is defect 4 |
| 101 | Secret-sink harness: 4 channels × 4 match rules, per-run `$HOME` walked post-mortem | `PASS2-GSTACK-TESTS.md:715` | ADR | Our channels differ (sandbox FS, relay, preview, logs). Building the harness is Layer G's decision; the positive-control law inside it is row 93 |
| 102 | Trust store for commands declared in repo files | `PASS2-GSTACK-TESTS.md:719` | ADR | Per-repo, per-command, recorded by a human. A new mechanism |
| 103 | Hermetic child env: no `...process.env` spread into a build child | `PASS2-GSTACK-TESTS.md:721` | SKILL | `testing`. Our *generated-code* sandbox already does this and proves it for every provider (`sandbox.py:105`); the rule generalises to any child a harness spawns |
| 104 | `estimateCost` returning 0 for an unpriced model | `PASS2-GSTACK-TESTS.md:724` | SKILL | `spend-ceilings` — **inverted**. An unpriced model must be a refusal or a pessimistic bound. As written it disables the hard cap in exactly the case the cap exists for. Our own `cost_usd=0.0` on `BudgetExceeded` is the same bug, and that half is a FIX (row 105) |
| 105 | Our own instance of row 104: `_write_attempt`'s budget branch constructs `_Written(...)` with no `cost_usd` | `docs/next/LAYER-E-BUILD.md` §1.1c | FIX | Attach the accumulated cost to `BudgetExceeded` and record it. Strictly more honest than `0.0`; no cost to being right |

*(Rows 105 and the four defects at the top are not mined findings — they are this repository's own
verified defects, listed because five mined rows land directly on them and a triage that did not
say so would be hiding the overlap.)*

---

## What did not become a skill, and why

**Eleven DROPs.** Six because the source's own limits exclude it (`santa-method`, the weighted
rubric twice, `tdd-workflow`'s runner matrix, `agent-self-evaluation`, the tiered repair loop).
One because we already do it, verified in code (path canonicalisation at `sandbox.py:125`). Two
because they are our build process rather than the product. Two because they are citations or
checklists rather than procedures.

**Twenty-seven ADRs.** Every one of them answers *what should Layer E do*, not *how should Layer E
decide*. A skill that says "run packages in parallel when their file plans are disjoint" has
decided that Layer E runs packages in parallel — which `orchestrate.py:19` deliberately has not.
That is the line: **a skill that quietly decides what to build is an architecture decision hiding
in a markdown file.** They cluster into roughly nine ADR proposals:

| Proposal | Rows |
|---|---|
| The relay's pass count and what feeds it | 14, 52, 28 |
| Package parallelism, WIP policy and the mutex | 56, 75, 76 |
| A typed package lifecycle with a deliberate terminal state | 69, 70, 73 |
| Resume, the build ledger, and the job queue (ADR-0020) | 25, 38 |
| Ceremony tiers / gate masks | 11, 88 |
| Playbook content taken from the corpus | 6, 12, 58, 63, 64, 57 |
| Cross-layer checks needing B's schema and C's fields | 47, 50 |
| Egress inventory and the secret-sink harness | 99, 101 |
| Prompt composition: the four-part brief | 32, 102 |

**Nine FIXes.** Five regexes, one FK check, one write-path validation, one singleton audit, and the
ledger repair at row 105. None needs a skill and none needs a decision; each names its site.

---

## What was written

Three skills and one amendment, all under `.claude/skills/`. Every one carries **Source · Method ·
Limits · Eval**, and every Limits section says the same uncomfortable thing: these are conventions
read in other people's repositories, and **not one of them has been measured on Scio.**

| Skill | Rows | Shape |
|---|---|---|
| `gate-verdicts` *(new)* | 25 | `SKILL.md` + four `references/` files loaded per decision — fail-closed control flow, the outcome vocabulary, scores and caps, and what a gate declares about itself |
| `build-loop-stops` *(new)* | 17 | `SKILL.md` + two `references/` files — what feeds a round, and the six ways a loop ends |
| `spend-ceilings` *(new)* | 7 | `SKILL.md` + one `references/` file — record shapes for meters, overrides and ledgers |
| `testing` *(amended)* | 10 | new §9.5 (the harness: exit codes, count arithmetic, evidence freshness, hermetic children), a sharpened Q3, four new evals E13–E16, and two vocabulary additions |

**One finding routed to `testing` was already there** — the positive-control law, row 93, written
at §3.5 from the same `gstack` file before this pass. It is listed in the table rather than dropped,
so the same row is not triaged again in six months.

**What was deliberately *not* written.** No skill decides a pass count, a parallelism policy, a
default flag, a state machine, a routing table or a Playbook line. Twenty-seven of those are ADRs
above, and the reason is the same in every case: a skill that quietly decides what to build is an
architecture decision hiding in a markdown file.

---

*Written 2026-08-26 against `docs/mined/` and `docs/as-built/LAYER-E-BUILD.md`, with the code
claims traced to `/home/user/hello-world` (read-only) through `docs/next/LAYER-E-BUILD.md`
§1–§3, which cites them at file and line.*
