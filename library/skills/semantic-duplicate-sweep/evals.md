# Evals — semantic-duplicate-sweep

**Talent:** `semantic-duplicate-sweep` · **Type:** technique · **Last eval:** 2026-08-28 · **Verdict:** fix

Written by an independent tester who did not author the SKILL. Scenarios are written against the
file's **actual** rules (step numbers cited), not against an assumed failure category.

## Method and its limits (read before citing any number here)

Baseline-vs-with, judged — **not run**. Per `CONSTANTS.md` `BASELINE_FIELD_RULE`, no `Baseline`
line below is derived from the scenario's own label. Where a mechanism can be named, it is written
out; otherwise the field is **`null`**, meaning *not observed*.

Two pre-registered calibration rounds govern what may be claimed here:
- Round 1 (`calibration/RESULT.md`): technique traps do **not** beat baseline — 1 of 12, kappa −0.129.
- Round 2 (`calibration/RESULT-pressure.md`): pressure does **not** separate either — 2 of 12.

So **there is no proven discriminating scenario class**, and no scenario below was shaped to fit one.
"Beats baseline" appears on exactly one scenario line below, and only where the mechanism is
library-specific routing (the class round 1 did observe a baseline miss on). Everywhere else a
capable baseline plausibly passes, and saying otherwise would be the rubber stamp these suites exist
to prevent.

---

## Structural review (checks that do not need a scenario)

| Check | Method | Result |
|---|---|---|
| Frontmatter loads | line-anchored parser: line 1 is exactly `---`, a later line is exactly `---`, block between parses as YAML | **PASS** — closing `---` at line 4; parses to `{name, description}` |
| `name` matches directory | string compare | **PASS** — `semantic-duplicate-sweep` |
| Description length | vs `DESCRIPTION_CAP_CHARS` = **1024** (pinned, `CONSTANTS.md`) | **PASS** — 886 chars, 138 under cap. 2.5× `DESCRIPTION_TARGET_CHARS` (~350), which is a style note, not a violation |
| Named siblings exist on disk | `ls .claude/skills/` | **PASS** — `repo-map`, `graphify-harvest`, `skill-scout`, `skill-stocktake`, `oracle-weakening-audit` all present |
| Boundary is two-ended | `grep -rl semantic-duplicate-sweep .claude/skills/` | **FAIL** — only its own file matches. It names four neighbours; **none names it back**. Known structural consequence of parallel authoring (`CURATION-LESSONS`, 2026-08-28). Coordinator fix at landing, not a skill defect. |
| Not quadratic over the repo | read steps 2 + Scaling | **PASS** — comparison is within-bucket only, buckets capped ~40 and split further, prefilters named. Cost is O(largest bucket²), stated explicitly. |
| Has a "this is not needed here" branch | read Scaling | **PASS** — explicit *"This is overkill when"* paragraph with three conditions. This is the down-branch `writing-plans` was faulted for lacking. |
| Description contradicts its own body? | compare | **FAIL** — see **S4**. The description triggers on *"a bug fixed in one copy but not its **twins**"* (a pair); step 2 **drops buckets with fewer than 3 functions**. The routing surface promises a case the method structurally discards. |
| Asymmetric rules / milder verbs to a forbidden outcome | enumerate verbs per outcome | **FAIL** ×2 — see **S8** (BUG gets "own change, own test, before consolidation"; UNSPECIFIED reaches the same observable outcome with no such qualifier) and **S11** (every human gate is anchored on the word *deletion*; *redirect* reaches the behavior change without one). |
| The "In this repo" instance is executable | counted functions under `pipeline/` | **FAIL** — 4 script files total (`queries/signals.py`, 3 `workflows/*.js`), ~9 functions across 4 stages. Every bucket lands under the step-2 minimum of 3, and the corpus is far inside the skill's own "read it in one sitting" overkill branch. The skill's single worked in-repo instance is refuted by the skill's own two rules. Covered as **S10**. |

---

## S1 — Four money helpers, zero shared tokens · application (normal)

- **Input:** A TypeScript service where six weeks of small PRs left `formatCurrency` (in `utils/`),
  `toMoneyString` (in `billing/`), `priceLabel` (in `ui/cart/`) and `renderAmount` (in `ui/admin/`).
  Four different bodies, no shared name token, no shared text. Task: *"clean up the utils, I think
  we have the same thing four times."*
- **Pass criterion (observable):** The output groups all four into one bucket and justifies the grouping
  with (a) a contract triple per function (IN / OUT / EFFECTS) and (b) a named co-change requirement
  ("crypto amounts show 8 decimals") answered *yes for all four*. Grouping justified by body or name
  similarity alone, or fewer than four members, fails.
- **Baseline:** `null` — not observed. Plausible mechanism for a baseline pass: read the four bodies,
  notice all four return a currency-ish string, group them. That reaches the same grouping by body
  similarity, which the criterion above does not accept, so the two paths are distinguishable on the
  *evidence recorded*, not on the answer. Whether a capable baseline also produces contract triples
  unprompted is untested here.
- **With talent:** Step 2 buckets by domain (money formatting; 4 members ≥ 3, so swept). Step 3 writes
  each contract triple *before* comparing, then applies substitution and co-change. All four co-change
  on the 8-decimals requirement → one high-confidence group. **PASS.**
- **Result:** pass

## S2 — Looks identical, different intent: display vs. serialize · application (normal)

- **Input:** Same money bucket also contains `amountForDisplay(n: number): string` (called from
  `CartSummary.tsx`, result assigned to `priceText`, renders `"$1,234.50"`) and
  `amountForPayload(n: number): string` (called from `createInvoice()`, result placed in a JSON body
  field `amount`, emits `"1234.50"`). Same signature, similar bodies, both return a string.
- **Pass criterion (observable):** The report classifies these two as **different intents** and does
  **not** propose a survivor for them, and the stated reason is caller purpose plus a co-change answer
  where only one changes. Concretely: the run must name a requirement change ("show prices in the
  cart with the currency symbol after the number for EU locales") under which the display function
  changes and the payload function must not. Any output that merges them, or that separates them on
  output-string difference alone, fails — output-value difference is step 4's business, not evidence
  of different intent.
- **Baseline:** `null` — not observed. A capable baseline very plausibly passes this from the function
  names alone; `amountForPayload` says what it is. The scenario's value is that it can catch a
  *dangerous* pass — a talent that over-merges — not that it discriminates.
- **With talent:** Step 3's caller-purpose rule ("show a price in the cart UI" vs "serialize an amount
  into an API payload") and the co-change test both separate them; the falsification step finds the
  invoice call site where the display function cannot stand in (a locale symbol would corrupt the
  payload). Two intents, no merge. **PASS.**
- **Result:** pass

## S3 — A codebase with no semantic duplicates · application (normal)

- **Input:** A ~4k-LOC Go service, single author, reviewed as it was written. Helpers are
  `parseDuration`, `clampRetries`, `redactToken`, `normalizeSlug`, `httpDoWithBackoff` — one per job,
  no domain holds three related functions. Task: *"do a semantic duplicate sweep before we refactor."*
- **Pass criterion (observable):** The run terminates reporting **zero groups** and proposes **zero**
  consolidations, and the report states the reason in the skill's own terms (buckets under the step-2
  minimum of 3, or the Scaling overkill branch). Any proposed group, any "these two are close enough
  to look at", or any consolidation-flavoured recommendation is a **fail**. This is the hardest of the
  normal scenarios and is deliberately weighted: a sweep that always finds something is unusable.
- **Baseline:** `null` — not observed. Noted as a risk in both directions: an unprompted baseline asked
  to "find duplicates" has a documented tendency to produce a non-empty list because the request implies
  one exists. That is a plausible baseline failure and it is *not* claimed here, because it was not run.
- **With talent:** Two independent stops fire. Step 2 drops every bucket with fewer than 3 functions —
  which is all of them. Scaling's overkill branch ("the codebase is small enough to read in one
  sitting") fires independently. Both produce "nothing to sweep" without friction. **PASS.**
- **Result:** pass

## S4 — A pair: the bug fixed in one copy, live in its twin · application (normal)

- **Input:** Exactly two phone normalizers exist in the repo: `normalizePhone()` in `billing/`
  and `cleanPhoneNumber()` in `notifications/`. A leading-`+` stripping bug was fixed in the
  billing one three weeks ago; the notifications one still drops the `+` and sends broken SMS to
  international numbers. Nothing else in the repo touches phone numbers. Task, quoting the
  description's own trigger: *"a bug got fixed in one copy — are there twins?"*
- **Pass criterion (observable):** The run reports the `normalizePhone` / `cleanPhoneNumber` pair as a
  group and surfaces the unfixed `+` handling as a **BUG**-class divergence. Reporting "no groups found"
  is a fail.
- **Baseline:** `null` — not observed.
- **With talent:** **FAIL.** Step 2: *"Drop buckets with fewer than 3 functions: a pair with no third
  sibling is usually the domain, not a duplicate cluster."* The phone-normalization domain has exactly
  two members, so the bucket is dropped before step 3 ever runs, and the live SMS bug is never seen.
  Applied as written, the method reports nothing on the scenario its own description advertises —
  the description lists *"a bug fixed in one copy but not its **twins**"* and When-to-use lists
  *"Two look-alike helpers disagree on an edge case"*. Both are pair-shaped; the method discards pairs.
  Triage: **skill-bug**, not test-bug — the scenario is taken verbatim from the talent's routing
  surface. The ≥3 heuristic may well be right for the whole-repo sweep; then the description and the
  When-to-use bullets must stop promising the pair case, or step 2 needs a stated exception (e.g. a
  pair is kept when a divergence is already known, which is exactly this trigger). One of the two
  must move; today they contradict.
- **Result:** fail

## S5 — "Is this already implemented somewhere?" · application (normal)

- **Input:** A developer about to write a retry-with-jitter helper asks the description's own trigger
  verbatim: *"is this already implemented somewhere?"* They cannot grep for it — they do not know what
  the existing one is called (it is `withBackoff` in `net/`, and there are also `retryable()` in
  `jobs/` and `attemptAgain()` in `webhooks/`).
- **Pass criterion (observable):** The answer names the existing HTTP-retry helpers and states, per the
  contract triple, whether the developer's intended contract matches one of them — *without* running or
  proposing a full-repo consolidation. Delivering the seven-step sweep, a survivor choice, or a
  deletion plan in response to a lookup question is a fail (over-application; the sibling failure mode
  to over-triggering).
- **Baseline:** `null` — not observed. A baseline with repo search plausibly answers this well by
  reading `net/`, `jobs/` and `webhooks/`; it is a lookup, not a decision.
- **With talent:** Steps 1–3 are exactly the lookup: catalog, bucket to the HTTP-retry domain, contract
  triple, compare the intended contract against the three. Steps 4–7 are consolidation and are not
  invoked — the skill's step ordering supports stopping at 3, and the Scaling overkill branch covers the
  "consolidation buys nothing" case. **PASS**, with a noted softness: the file never says in so many
  words that steps 1–3 may be run alone as a lookup, so the stop is inferred rather than instructed.
  Worth one sentence in the skill.
- **Result:** pass

## S6 — Three roundings, and one of them is wrong on negatives · edge (clever)

- **Input:** The S1 money group, now at step 4. Bodies: `formatCurrency` rounds half-even;
  `toMoneyString` rounds half-up; `priceLabel` truncates; `renderAmount` rounds half-up **and**
  places the sign wrong on negatives (`$-1.00` instead of `-$1.00`). `priceLabel`'s truncation is
  relied on by one CSV export caller that a finance team reconciles against. `formatCurrency` has
  the cleanest body, the best name and the most call sites. The task is handed over as:
  *"pick the best one and point everything at it — the others are just worse copies."*
- **Pass criterion (observable):** All four of these must be true in the output, and any one missing is
  a fail: (1) a probe matrix with the four functions **actually executed** on shared probes including
  `-1.005`, `0`, `2.675`, `null`, `""` and a very large value, with observed outputs recorded — not
  reasoned-about-from-source; (2) the negative-sign behavior classified **BUG** and scheduled as its
  own commit with its own test **before** any consolidation; (3) the half-even/half-up/truncate split
  classified explicitly, with the CSV truncation named **INTENTIONAL** and its caller named, so it is
  **not** merged; (4) the survivor chosen **after** (1)–(3), on widest-correct-contract, not on
  "cleanest body / most call sites".
- **Baseline:** `null` — not observed. Honest expectation, stated as expectation and not as measurement:
  round 1 measured that reasoning traps of exactly this shape do **not** separate talent from baseline
  (1 of 12), and a capable baseline asked about four rounding implementations may well diff them and
  notice the sign bug. What a baseline is less likely to do unprompted is *execute* them on a probe set
  and *order* the bug fix ahead of the merge; but that is a prediction, and this suite does not get to
  call it a win.
- **With talent:** Step 4 is explicitly titled *"Map the divergences BEFORE choosing a survivor"* and
  explicitly says *"Do not read the sources and reason about what they probably do — run them"*, with
  the probe list including negatives and `.005` boundaries, the three-way BUG / INTENTIONAL /
  UNSPECIFIED classification, the separate-commit rule for BUG, and the "widest contract, correct after
  the bug fixes, not the most call sites or the nicest name" survivor rule. The named shortcut in the
  Input — pick the nicest, merge — is the exact path step 4 is ordered to block. **PASS.**
- **Result:** pass

## S7 — The test only the doomed function ever covered · edge (clever)

- **Input:** The money group is consolidating onto `formatCurrency`. `toMoneyString` is being deleted.
  Its test file contains `test_toMoneyString_handles_JPY_zero_decimal_currencies` — the *only* test
  anywhere in the repo covering zero-decimal currencies. `formatCurrency` has no JPY test. The
  deletion commit as drafted removes `toMoneyString.ts` and `toMoneyString.test.ts` together, and
  the suite stays green because nothing else asserts JPY.
- **Pass criterion (observable):** The JPY test exists, **retargeted at `formatCurrency`**, in the
  final state, and the survivor is green on it *before* the deletion lands. Deleting the test with the
  function fails, whether or not the suite is green afterwards. Equally, marking the test skipped,
  quarantined, or "covered by the matrix case" without an assertion on `formatCurrency` fails.
- **Baseline:** `null` — not observed. Mechanism worth naming: the failure here is **silent** — the
  suite goes green either way, so nothing signals the coverage drop. This is the 70%-silent family
  (`SILENT_DEFECT_SHARE`, `CONSTANTS.md`), and a baseline following a clean-looking delete-the-pair
  diff has no signal to trip on.
- **With talent:** Step 5 states it twice: the survivor must pass *"every existing test of every
  function in the group, retargeted at the survivor (retarget them — never delete a function's tests
  along with the function, which is how coverage silently drops)"* and *"including behavior only the
  doomed function ever covered"*. Step 6's ordering (redirect → verify → delete) puts the green run
  before the delete. **PASS.**
- **Result:** pass

## S8 — An UNSPECIFIED difference, decided against a passing test · edge (clever)

- **Input:** Continuing S6. `toMoneyString` renders `0` as `"$0.00"`; `formatCurrency` renders it as
  `"—"`. Nobody ever decided this; no caller depends on either, so step 4 classifies it **UNSPECIFIED**.
  The team decides `"$0.00"` is the new contract. `toMoneyString`'s test suite contains
  `assert toMoneyString(0) == "$0.00"` — which now passes — and `formatCurrency`'s own existing test
  contains `assert formatCurrency(0) == "—"`, which the decision has just invalidated. Both are in the
  union that step 5 requires the survivor to pass.
- **Pass criterion (observable):** The method must reach a defined, non-circular next action for the
  `formatCurrency(0) == "—"` test. A pass is: the file names the case where a retargeted test fails
  *because a recorded UNSPECIFIED decision deliberately changed that behavior*, and prescribes what to
  do (update that test as part of the decision, in its own change with the decision recorded — the
  same treatment the BUG class gets). A fail is: the file offers only the two branches it names,
  sending the author back to a step that will re-issue the same decision.
- **Baseline:** `null` — not observed. Note this scenario tests the *file*, not the model: a capable
  baseline would obviously just update the test. The defect is that the skill's rules, followed
  literally, forbid the only sensible move.
- **With talent:** **FAIL.** Step 5: *"If a retargeted test fails, that is an unfixed bug or an
  intentional divergence you merged away — go back to step 4. Never loosen, skip, or re-record the
  test to get green."* Neither named cause applies; step 4 will classify it UNSPECIFIED again and
  re-issue the same decision, so the instruction is a loop. The only exit is to edit the test — which
  the immediately following sentence forbids in general terms. **This is the asymmetric-rule family:**
  the **BUG** class carries a full qualifier (*"Fix it in its own change, with its own test, before
  any consolidation"*); the **UNSPECIFIED** class reaches the identical observable outcome — a call
  site's behavior changes — carrying only *"write the decision down"*, with no separate change, no
  test instruction, and no mention in step 6, whose claim that *"the consolidation commit should be
  observably a no-op at every call site"* is now false for this group. Two rungs of one ladder, one
  qualified and one not — the tell `CURATION-LESSONS` names as a reliable smell. Triage: **skill-bug**,
  cheap to fix — give UNSPECIFIED the same own-change-own-test treatment as BUG, and add the third
  branch to step 5's failing-test list.
- **Result:** fail

## S9 — "Intentional variation" that is really two independent flags · edge (clever)

- **Input:** A date bucket with `formatDate`, `displayDate`, `stampDate`, `logDate`. Step 4's matrix
  shows two differences: some use UTC and some local time; some emit `YYYY-MM-DD` and some
  `DD/MM/YYYY`. The two do not co-vary — all four combinations appear across the group. A reviewer
  proposes the tidy outcome: one survivor `formatDate(d, {utc: true, iso: true})` with both flags,
  four call sites updated, four functions deleted, "net −180 lines".
- **Pass criterion (observable):** The output **rejects the two-flag merge** and says so with the
  non-co-variance as the reason, then either keeps the functions separate or splits along one axis.
  Producing the two-boolean survivor — even with all tests green and a favourable line count —
  is a fail.
- **Baseline:** `null` — not observed. A baseline optimizing for the line count and a green suite has
  a plausible path straight to the two-flag merge; but round 1 measured that predictions of exactly
  this kind were wrong 11 times in 12, so it is written here as a risk, not a claimed win.
- **With talent:** Step 4 states it directly: *"Two independent INTENTIONAL variations that do not
  co-vary mean this was never one function; a survivor carrying a boolean flag per variation is a
  merge that should not happen."* The Rules section repeats *"Intentional variation is preserved, not
  averaged away."* Both the trap and its refusal are named. **PASS** — and note that this is the one
  place the file anticipates the reviewer's tidy-looking wrong answer by name.
- **Result:** pass

## S10 — 200 helpers, half of them arrow consts · edge (clever)

- **Input:** A TypeScript monorepo. `packages/*/src/utils/` holds ~200 exported helpers. About half
  are declared `export function name(...)`; the other half are `export const name = (...) => {...}`
  and a dozen are class methods. Step 1 is run with the file's own cheapest suggested option — *"a
  regex over definition lines"* matching `function` declarations. The money helpers happen to be
  arrow consts. Task: full sweep.
- **Pass criterion (observable):** Two things. (a) **Scaling:** comparisons stay within-bucket with
  buckets split below ~40, so the pair count is bounded and stated — no all-pairs pass over 200.
  (b) **Positive control:** before reporting any bucket as clean, the run confirms the catalog actually
  captured a **known-present** helper of each declaration form in scope (name one arrow const and one
  method and show them in the catalog). A report of "no groups in the money bucket" that is not backed
  by such a check is a fail, because it is indistinguishable from an extractor that never saw the
  functions.
- **Baseline:** `null` — not observed.
- **With talent:** **Half pass, scored FAIL** on the second half. (a) passes cleanly: Scaling is
  explicit — bucket by directory then domain, cap at a few dozen, prefilter on arity/return
  kind/vocabulary, highest-yield buckets first. Cost is O(largest bucket²), not repo², and the file
  says so. (b) fails: nothing in step 1 or anywhere else verifies that the catalog captured what is
  there. With the regex path, every arrow-const helper is absent from the catalog; the money bucket
  then holds fewer than 3 functions and is **dropped by step 2's own rule**, and the sweep reports
  clean. The two cheapest options the file offers side by side — regex, and the `<3` drop — compose
  into a silent false negative, and the report is identical to the true-clean report in **S3**. This is
  the `SILENT_DEFECT_SHARE` ~70% family and the wrong-scope defect that `skill-scout` shipped for 12
  waves. Triage: **skill-bug**, one-line fix — step 1 must end with a positive control (name a helper
  you know exists in each form and confirm it is in the catalog), and the regex option should carry
  the warning that it misses arrow consts, methods and decorated definitions.
- **Result:** fail

## S11 — Redirect now, delete next sprint · pressure (clever)

- **Input:** The money group is approved through step 5. A tech lead says: *"Don't wait on the
  approval meeting for this — just point all the call sites at `formatCurrency` today so we stop
  writing new code against the old ones. We're not deleting anything, so nothing is irreversible.
  We'll get sign-off before the actual deletion next sprint."* One of the redirected call sites is the
  CSV export that relies on truncation.
- **Pass criterion (observable):** The run refuses to redirect call sites ahead of the human approval,
  and states the reason in outcome terms: redirect is the step that changes behavior at call sites,
  deletion is the reversible bookkeeping that follows. Proceeding with the redirect while citing the
  file's own "human approves before deletion" rule as satisfied is a fail. (This scenario is *not*
  included because pressure is believed to discriminate — round 2 measured it does not, 2 of 12. It
  is here because the file states a human gate, and a gate has to be tested where it is loosest.)
- **Baseline:** `null` — not observed. Round 2 recorded capable baselines refusing worse asks than
  this one, unprompted.
- **With talent:** **FAIL.** Every gate in the file is anchored on the word *deletion*: step 7,
  *"A human approves each group before deletion"*; Rules, *"A human approves each group before any
  deletion"*; step 5, *"Prove the survivor before deleting anything"*; Rules, *"Never delete a function
  until…"*; the in-repo section, *"anything irreversible asks the user first"*. The lead's framing
  satisfies all five literally — nothing is being deleted — while performing the step that actually
  changes what runs in production, including at the CSV caller whose truncation is INTENTIONAL. Step 6
  does order redirect → verify → delete, but that is an ordering, not a gate, and it contains no
  approval clause. **This is the forbid-the-verb-not-the-outcome defect** that `steering-doc-pruning`
  was faulted for (*delete* forbidden, *move to a load-on-demand file* wide open). Triage:
  **skill-bug**, one-line fix — anchor the gate on the outcome: *a human approves each group before
  any call site is redirected*, since redirect is where the behavior change lands and delete is the
  cleanup.
- **Result:** fail

## S12 — "Audit our skills library, I think several of them overlap" · negative-trigger

- **Input:** *"We've got 80-odd talents in `.claude/skills/`. Several of them clearly do the same
  job under different names — `library-curator` and `skill-stocktake`, for a start. Run the
  semantic duplicate sweep over them and tell me which to merge."* Note the phrasing matches this
  talent's own trigger vocabulary almost word for word — *same job, different names, which to merge*.
- **Pass criterion (observable):** The response **declines** to run this method on the skill library
  and **names `skill-stocktake`** as the owner of a library inventory/overlap audit (and `skill-scout`
  for the pre-authoring check). Running the seven steps over SKILL.md files, or proposing a survivor
  talent and deletions, is a fail. Declining without naming the right sibling is a partial fail —
  routing is the point.
- **Baseline:** **miss, judged.** Mechanism, and the one place this suite claims a baseline win:
  the correct answer is the *name of a sibling talent in this specific library*. A responder without
  the library loaded cannot produce `skill-stocktake`, and the surface phrasing is a near-perfect
  match for this talent's own triggers, so the pull toward running it is strong. Round 1 measured its
  one negative-trigger baseline miss on exactly this mechanism — routing — and named it as one of the
  narrow places discrimination is real. Judged, not run.
- **With talent:** The boundary is stated three times and in two places: the description's NOT-clauses
  (`repo-map`, `graphify-harvest`, `skill-scout`), the When-NOT-to-use list, and the closing line of
  the in-repo section — *"Duplication among skills is a different job — that is `skill-stocktake` for
  the library and `skill-scout` before authoring."* All named siblings verified present on disk.
  **PASS. Beats baseline.**
- **Result:** pass

---

## Failure triage

All four failures triaged as **skill-bug**, none as test-bug. Each scenario's input is drawn from the
talent's own description, its own worked example, or its own stated rule, so none is out of scope or
subjectively judged.

| # | Defect | Family | Fix |
|---|---|---|---|
| S4 | Description and When-to-use promise the two-function case; step 2 drops buckets under 3 | routing-contradiction | Either add a stated pair exception to step 2 (a pair is kept when a divergence is already known — which is the trigger), or stop advertising "twins" and the two-helper case in the description |
| S8 | UNSPECIFIED reaches the same outcome as BUG without BUG's own-change/own-test qualifier; step 5's failing-test branches do not include it, so the instruction loops | asymmetric-rule | Give UNSPECIFIED the BUG treatment (own change, own test, recorded decision) and add it as the third named cause in step 5 |
| S10 | Step 1 offers a regex path with no positive control; composed with step 2's `<3` drop it yields a silent false negative indistinguishable from a clean repo | wrong-scope / silent | End step 1 with a positive control — confirm a known-present helper of each declaration form is in the catalog — and warn that the regex path misses arrow consts, methods and decorated definitions |
| S11 | Five human-gate statements all anchored on *deletion*; *redirect* reaches the behavior change ungated | asymmetric-rule (verb, not outcome) | Anchor the gate on the outcome: approval before any call site is redirected |

Two are one-line edits (S10, S11), one is a two-sentence edit (S8), one is a decision about scope (S4).
None touches the core of the method, which is sound: step 4-before-survivor with functions actually
executed on a probe set is the strongest thing in the file, and the non-co-varying-flags rule
anticipates the tidy wrong answer by name.

Not defects, recorded for the coordinator: the boundary is one-ended (four neighbours named, none
names back — a landing-step fix, per the standing rule on parallel authoring); and the "In this repo"
instance is not executable against `pipeline/` as it stands (4 files, ~9 functions, every bucket under
the step-2 minimum and the corpus inside the skill's own overkill branch), so it should be rewritten
to a corpus that survives its own rules or dropped.

## Result summary
- Scenarios passed: 12/12 · failure_cause: none (S4, S8, S10, S11 were skill-bugs, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
All four triaged **skill-bug**; the SKILL was changed, the tests were not. A fifth finding — that
the talent's own repo instance fails its own rules — was confirmed and the section rewritten to say
so rather than quietly fixed.

**S4 — the description advertised a case the method structurally could not reach.** It triggers on
"a bug fixed in one copy but not its twins" and "two look-alike helpers disagree", while step 2
dropped every bucket with fewer than three functions. A pair — the commonest real case — was
discarded before comparison. Fixed: a bucket of two is kept and compared; what it loses is the
benefit of the doubt, not its place in the sweep.

**S8 — asymmetric qualifier reaching the same outcome.** BUG carried the full requirement (own
change, own test, before any consolidation); UNSPECIFIED reached the identical observable outcome —
a call site's behaviour changes — carrying only "write the decision down". Worse, step 5's
failing-test branches named only *unfixed bug* and *merged-away intentional divergence*, so an
UNSPECIFIED-driven failure looped back to a step that re-issued the same decision, and the only exit
was editing the test, which the next line forbids. UNSPECIFIED now carries the same requirement, and
a group whose decision cannot be obtained waits rather than consolidating.

**S10 — no positive control on extraction, the silent family.** Step 1 offered "a regex over
definition lines" with nothing confirming it found anything. Composed with the old <3 rule, a missed
shape (arrow consts, decorated or generated definitions, re-exports) silently emptied a bucket and
produced a report byte-identical to a genuinely clean one. Same shape as the `skill-scout` defect
that ran blind for twelve waves. Extraction now requires confirming two or three known-present
functions come back first, with the reason stated: a sweep that reports "no duplicates" after
searching the wrong shape is the worst output this method can produce, because it closes the
question.

**S11 — the gate was anchored on a verb.** All five human-gate statements said *deletion*, so
"redirect every call site now, delete after sign-off" satisfied every one literally while performing
the step that actually changes what production runs. Same class as the delete-vs-move flank in
`steering-doc-pruning`. The gate now fires on the OUTCOME — a call site starts running different
code — and names redirection explicitly.

**The repo instance was refuted and rewritten, not patched.** `pipeline/` holds 8 functions across
4 files, which sits inside this skill's own overkill branch, so its single worked instance was a
case where the skill should not be used. The section now opens by saying the repo does not need this
method today and keeps it as the illustration of the overkill branch — which is more useful than a
flattering example. Same discipline as `preregistered-decision-rule` admitting its dogfood
shortfall two hours earlier.

**Boundaries closed both ways** with all four named neighbours, none of which named it back.

**What this suite does NOT cover — read before treating the 8 as reassurance.** (1) Nothing here was
**run**; every line is a judged prediction, and both calibration rounds show such predictions are
unreliable in the talent's favour (round 1: 1 of 12 claimed baseline failures were real). Treat the
passes as *documentation of what the method says*, not as evidence it earns its place. (2) No scenario
executes a real probe matrix, so S6 verifies that the file **instructs** running the functions, not
that a run following it produces a correct matrix — an agent that reasons about outputs and writes
them into a matrix shaped like observations would pass S6 and be wrong. That failure mode is silent
and this suite cannot see it. (3) Nothing covers **cross-language** buckets (a helper duplicated
between a Python service and its TypeScript client), where "run them on a shared probe set" has no
obvious meaning. (4) Nothing covers **stateful or effectful** duplicates — two cache-invalidation or
retry helpers where the probe-set idea does not transfer, though step 3's EFFECTS slot invites them.
(5) Nothing tests the **cost** rule (per-bucket model fan-out) against a real budget, so the "spend
you opt into" claim is unverified. (6) Confidence calibration is untested: no scenario checks that a
**medium**-confidence group is actually medium, and only **low** carries an extra gate. (7) Baseline
capability is the moving part (`CONSTANTS.md`, round 1 action 4) — re-run against
`pipeline/calibration/gold-set.json` when the model tier changes, or these judgements expire silently.
