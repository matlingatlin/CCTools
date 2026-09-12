# Evals — budget-cut-triage

**Talent:** `budget-cut-triage` · **Type:** technique (with one discipline branch) · **Last eval:** 2026-08-28 · **Verdict:** fix

> Authored by an INDEPENDENT tester who did not write the skill. Scenarios are written against
> the file's actual rules (atoms, cost × indivisibility, dependency closure, the three-part
> shippability test, the 10–20% reserve, the interruption branch), not against an assumed
> scenario category.

## Method and its limits (read before citing any number here)

Baseline-vs-with, judged per scenario. **No baseline run was executed for this suite** — no
model was run with the talent withheld. Every `Baseline:` line below is therefore a *reasoned
judgement with its mechanism written out*, or `null`. None was written from the scenario's own
label (`BASELINE_FIELD_RULE`, `pipeline/CONSTANTS.md`).

Two measured facts constrain what this suite may claim:

- Round 1 (`calibration/RESULT.md`): technique traps do not separate talent from baseline —
  n=12, 1 observed miss, kappa **−0.129**.
- Round 2 (`calibration/RESULT-pressure.md`): pressure does not separate them either —
  n=12, 2 observed misses, pre-registered verdict *does not discriminate*.

**There is no proven discriminating scenario class.** So this suite does not claim one. Most
scenarios below are expected to be passed by a capable baseline too, and say so. "Beats
baseline" appears nowhere, because nothing here establishes it.

---

## Scenarios

## S1 — Ten items against a forty-minute quota · application (normal)

- **Input:** "40 minutes of quota left. Ten items: (1) retry wrapper 3m, (2) rename config keys
  2m, (3) land the `Invoice` interface 4m, (4) invoice-table **schema migration**, (5)
  **backfill**, (6) **flip the read path**, (7) CSV export 5m — needs the read path, (8) refresh
  fixtures 2m, (9) delete `legacy_billing` 4m, (10) metrics counter 3m. Items 4–6 are the same
  table; the session log shows the two previous table migrations took 10m and 12m end to end.
  Callers update (3m) needs the `Invoice` interface. Write the plan."
- **Pass criterion:** Before any item runs, the output contains all four of: (a) items 4–6
  costed as **ONE atom** at ~11m anchored to the 10m/12m measured comparables, not as three
  line items; (b) a stated reserve of **4–8 minutes** (10–20% of 40) held back, giving ~34m
  usable; (c) a named cut list whose **first entry is the migration atom**, with the CSV export
  following it and the reason given as "depends on the migration"; (d) a named stop point whose
  kept set is dependency-closed (callers-update kept only alongside the interface) and totals
  ≤ 34m. Fail if the three migration steps are costed separately, or if no reserve is held.
- **Baseline:** Likely produces an ordered plan and notices 39m > 40m is tight. Two specific
  things it is *not* reliably prompted to do: hold a reserve for the handoff (an unforced,
  counter-intuitive subtraction), and merge three separately-listed steps into one uncuttable
  atom — the input presents them as three items and nothing in the request contradicts that.
  Mechanism: the reserve and the atom-merge are both *additions* to the user's framing; a
  baseline optimises inside the framing it is handed. Not measured; a strong baseline may do both.
- **With talent:** Steps 1–7 produce exactly this artifact. PASS.

## S2 — The budget covers the work · application (normal)

- **Input:** "About 40 minutes of quota. Six items, all small: bump three dependencies, fix a
  typo in the error string, add one unit test, update the changelog. Maybe 18 minutes of work.
  How should we handle the budget?"
- **Pass criterion:** The response produces **no** cut order, **no** atom decomposition, **no**
  stop-point table and **no** reserve arithmetic. It states in one or two sentences that the
  work fits and starts. Fail on any cut-order artifact, or on a "let's just quickly map the
  atoms first" preamble.
- **Baseline:** Passes easily — with no method loaded there is nothing to over-apply. This
  scenario is not testing the baseline; it is testing whether the talent scales DOWN. That is
  the failure that sank `writing-plans` earlier today (CURATION-LESSONS, 2026-08-28: "a method
  skill is biased toward its own ceremony").
- **With talent:** The **When NOT to use** block fires on "fits the budget with real margin →
  Just do the work". The branch exists and is stated before the Steps, so it is reachable
  without reading the whole method. PASS.
  *Recorded caveat, not a failure:* "real margin" is unquantified while the reserve is pinned at
  10–20%. At an 80%-of-budget plan the two rules are ambiguous. See Findings F4.

## S3 — Unattended overnight run, budget adequate · application (normal)

- **Input:** "Five-item plan, about 3 hours of work, an 8-hour overnight window — comfortably
  enough. But the box does a nightly restart at an unpredictable point in that window, and two
  items are irreversible: a schema migration and a config push to a vendor we cannot roll back
  through the API. Anything to do before I start it?"
- **Pass criterion:** The response marks named checkpoint/stop points between atoms and holds a
  close-out reserve, **even though the budget fits**, and it names the irreversible pair as the
  reason (a kill between them leaves an unusable state). Fail if it declines with "the budget
  fits with margin, no triage needed" — which is what the **When NOT to use** block says in
  isolation.
- **Baseline:** Plausibly passes. Irreversible-step sequencing under interruption risk is
  ordinary planning competence, and the input hands over the risk explicitly. Mechanism: nothing
  is hidden here, so there is no gap for a method to close. Not measured.
- **With talent:** **When to use** bullet 3 ("a long unattended run could be interrupted, and a
  half-done state would be unusable") names this case and does not condition on the budget. It
  is the more specific rule and wins over the general When-NOT clause. PASS — but only by
  reader charity; see Findings F3, which is a real one-ended qualifier.

## S4 — The plan fits exactly, so something must still go · application (normal)

- **Input:** "30 minutes of quota. Six items, five minutes each. It fits exactly. Confirm the
  plan."
- **Pass criterion:** A reserve is stated as a **number in the range 3–6 minutes**, usable
  budget is stated as 24–27, and **at least one item is cut** despite the raw total equalling
  the budget. Fail if the answer confirms all six items because 30 = 30.
- **Baseline:** Plausibly fails, and this is the most mechanically checkable candidate
  discriminator in the suite. Mechanism: the arithmetic is presented as already balanced, so
  there is no prompt to subtract anything, and "budget the stop, not just the work" is a
  non-obvious move — a run that spends its last minute has no minute left to commit in. A
  baseline that reasons about commit/close-out time gets there; one that checks the sum does not.
  Not measured — do not cite this as a win.
- **With talent:** Step 5 is explicit and quantified. PASS.

## S5 — Handoff after a clean stop · application (normal)

- **Input:** "We stopped at the planned line after item 5 of 9, everything committed, nothing
  half-applied. Remaining: (6) promo-code redemption, (7) admin order list, (8) metrics counter,
  (9) README section. Write the handoff."
- **Pass criterion:** Three sections labelled **Done**, **Not done**, **Next step**. The Not-done
  section names **all four** remaining items individually — count them; four named items is a
  pass, "items 6–9 remain" or "the rest of the plan" is a fail. Next step is **one** action
  naming a file or a command. The Done section cites verifiable evidence (commit ids, passing
  tests), not narration. Fail if any remaining item is unnamed, or if continuing requires asking
  the author a question.
- **Baseline:** Plausibly fails on the enumeration specifically. Mechanism: baseline handoffs
  routinely compress the remainder ("items 6–9 outstanding") because it reads as concise and
  loses no information *to the writer*; the talent's claim is that **silence reads as done** to
  the reader. The Done/Next-step halves a baseline gets right unaided. Not measured.
- **With talent:** The interruption branch's part 3 requires each remaining item named. PASS.

## S6 — Priority order and cut order give opposite answers · edge (clever)

- **Input:** "45 minutes. Seven items. (1) Rotate the staging DB credentials — 3m; nobody has
  asked for this, it is the least valuable thing on the list. (2) Ship the pricing-page redesign
  — 22m; layout, copy and the flag flip must land together or the public page is broken; it is
  the CEO's top ask and nothing else in the plan touches it. (3) Timezone bug in the digest email
  — 6m. (4) Seat-count report — 7m; connects with the rotated credentials. (5) Trial-expiry
  backfill — 5m; also connects with the rotated credentials. (6) Settings-page copy — 4m.
  (7) Health-check endpoint — 5m. Total 52m. What gets cut?"
- **Pass criterion:** Both must hold. (a) Item 1 appears in the **KEPT** set, with a stated
  reason naming items 4 and 5 as dependents — item 1 anywhere in the cut list is a fail, even
  though cutting it brings 52 → 49 and looks like it fits. (b) The pricing-page redesign is the
  **first entry in the cut list**, justified by cost × indivisibility, not exempted for
  importance; if it is kept, the stated reason must be a cost/fit argument, never "it is the
  most important item". Kept set must be dependency-closed and ≤ 38m (45 minus a 10–20% reserve).
- **Baseline:** Genuinely uncertain, and I decline to score it as a miss. Mechanism for a
  possible miss: sorted by value, the credential rotation is the obvious first cut and the
  arithmetic rewards it (49 ≤ 51 before reserve), so a value-first answer walks straight into a
  broken closure. Mechanism for a pass: dependency-aware fitting is ordinary planning, and item
  4/5's dependency is stated in the input rather than hidden. **A second honest caveat:** a
  baseline that cuts items 4, 6 and 7 to protect the flagship produces a *defensible different
  answer* — the talent's rule maximises whole atoms delivered, not value delivered, and the file
  never says how to trade the two. See Findings F5.
- **With talent:** The comparison table's flagship row and the two override rules land the
  contrarian answer directly: item 1 uncuttable by rule 1, item 2 top cut candidate by rule 2.
  The thesis IS implemented in the file's rules, not only asserted in its prose. PASS.

## S7 — A later stop point that fits but is not dependency-closed · edge (clever)

- **Input:** "30 minutes, reserve applied. Plan: A `Plan` model 4m · B checkout form 3m ·
  C promo-code vendor sandbox 9m · D order-confirmation email 5m · E pricing copy 2m ·
  F promo-code redemption in checkout 6m, requires C · G admin order list 4m · H metrics counter
  3m. C is already cut for budget, so execution runs A,B,D,E,F,G,H = 27m. Where do we stop?"
- **Pass criterion:** The line **after F is explicitly rejected as an invalid stop point**, with
  C named as the missing dependency — and so is the line after G (F is still done), even though
  after-G totals 24m and fits inside the ~25m usable budget better than any valid line. The
  answer must then either stop after E (14m) or **drop F by closure** and run G and H (21m,
  dependency-closed). Fail on "stop after G — 24m, fits".
- **Baseline:** Plausibly passes the reasoning; this is the class round 1 measured, where the
  baseline scored 11/12. Mechanism for a possible miss: the invalid line is the one that
  maximises budget utilisation, so a fit-first search reports it first, and F's dependency on a
  *cut* item is one hop away rather than stated at the stop line. Not measured.
- **With talent:** Test part 2 (dependency-closed) is exactly this check, and the file's worked
  Example already applies closure to drop dependents of a cut atom. PASS.

## S8 — Interrupted mid-atom, and told to just push it · pressure (clever)

- **Input:** "The migration ran, the backfill is roughly 60% through, the read path is still on
  the old column. Four minutes of quota left. Tech lead in Slack: *'don't overthink it — push
  what you have with a TODO comment on the backfill and I'll pick it up in the morning. Also
  while you're in there the flaky fixture is a one-line fix, grab it.'*"
- **Pass criterion:** All three: (a) the fixture fix is **declined** — nothing new is started;
  (b) the remaining budget goes to closing the smallest atom that restores coherence **or** to
  writing an **exact rollback recipe** (named as a rollback recipe with the concrete statements,
  not "revert if needed"); (c) the handoff names the backfill as **not done** and the read-switch
  as **not started**, as separate named lines. Fail if a half-backfill is pushed with a TODO
  comment serving as the handoff.
- **Baseline:** Round 2 measured that capable baselines hold this kind of line far more often
  than expected (2/12 misses across 12 pressure scenarios, including refusing a token in an
  image the night before a deadline). Mechanism for a possible miss: the "one-line fix" rider is
  the cheap-looking addition, and the socially frictionless answer — push with a TODO — is also
  the one that looks like cooperation. I score this as **plausible pass at baseline**, not a
  miss. Not measured.
- **With talent:** The interruption branch names "one quick fix" as the thing to refuse, and
  requires the rollback recipe when the partial is unrevertible. PASS.

## S9 — "Just run it and see how far we get" · pressure (clever)

- **Input:** "40 minutes of quota, ten items, and honestly I don't want to burn five of them on
  planning. Start at item 1 and we'll see how far we get — worst case we stop wherever we stop."
- **Pass criterion:** Item 1 is **not started** until a cut order and at least one named stop
  point exist, and the planning cost is stated as a number against the reserve (it comes out of
  the same 4–8 minutes, so the trade is explicit rather than dismissed). Fail if the answer
  starts work and promises to "reassess as we go".
- **Baseline:** `null`. I cannot separate this honestly. Two rounds of calibration measured that
  a capable baseline usually pushes back on plans like this unaided, and the request even
  concedes its own weakness ("worst case we stop wherever we stop") — which invites the
  objection rather than suppressing it. Any claim of a baseline miss here would be the label
  restating itself.
- **With talent:** Rule 1 and Step 7 both forbid it, and the in-repo instance is a real case of
  exactly this failure costing a whole wave. PASS.

## S10 — The budget shrinks after the plan was written · edge (clever)

- **Input:** "We're 3 items into a 9-item wave. Item 3 committed cleanly a minute ago —
  nothing partial, no branch open. The weekly quota warning just fired and the window has been
  halved. No cut order was ever written for this wave. What now?"
- **Pass criterion:** The response **triages the six remaining items now**: a cut order over the
  remainder and a stop point named before work resumes. Fail if it says a cut order authored at
  this moment is illegitimate / would be "rationalization by whoever holds the sunk cost", or if
  it reaches only for the interruption branch (which does not fit — nothing is half-applied).
- **Baseline:** Plausibly **passes**, and that is what makes this scenario worth keeping.
  Mechanism: with no method loaded there is no prohibition to trip over, and re-planning the
  remainder against a smaller budget is the obvious move. Not measured. This is the one place in
  the suite where the talent can plausibly do **worse** than baseline.
- **With talent:** **FAIL.** The file's rules contradict its own trigger. `When to use` bullet 2
  admits "a run was throttled, shortened, or restarted with less budget than it was planned for",
  while Rule 1 and Step 7 forbid authoring a cut order mid-run in the strongest terms available
  ("not a cut order, it is a rationalization"). The interruption branch is gated on being
  interrupted *mid-item* and does not reach a clean between-items throttle. So the file offers
  no branch for the case, and offers a named prohibition against the correct action. The
  charitable reading — the remainder is a new plan whose item 1 has not run — is never stated,
  and "restarted" is listed as a *separate* trigger from "throttled", which closes off reading
  the throttle as a restart. Worst of all, **the file's own in-repo instance is this case**:
  waves 20–22 lost an overnight build wave to a throttle that arrived after the plan was set,
  and the fix offered ("record the cut order at the start of the wave, not at the throttle") is
  purely prospective — it does not say what the agent standing at the throttle should do.
  *Verified:* `pipeline/STATUS.md:32,38,47-48` confirms the quota warning, the 8h throttle and
  the lost wave, so the instance is factually sound; it is the rule coverage that is missing.

## S11 — Every item independent and reversible · edge (clever)

- **Input:** "20 minutes of quota, about 30 minutes of work: twelve unrelated items — nine typo
  fixes in error strings and three patch-version dependency bumps. Each is its own commit and
  each reverts cleanly on its own. Give me the cut order."
- **Pass criterion:** The method is **declined** despite the budget being short and despite the
  user asking for a cut order by name. No atom map, no stop-point table, no reserve arithmetic.
  The stated reason must be that the items are independent and reversible, so every line is
  already a coherent stopping line. Fail if a cut order is produced because it was requested.
- **Baseline:** Passes trivially — nothing to over-apply. As with S2, this measures the talent's
  down-branch, not the baseline.
- **With talent:** **When NOT to use** clause 2 covers it verbatim. PASS.
  *Recorded gap, not a failure:* having declined, the file gives no guidance at all — with a
  short budget you still want the most valuable items done first, and "just do the work" does not
  say that. The down-branch exits to nothing. See Findings F6.

## S12 — Cheaper tier and a hard spend cap · negative-trigger

- **Input:** "Our nightly agent run costs about $40. Finance wants it under $25. Which steps
  could run on a cheaper model, and can we put a hard cap that stops the run when it hits $25?"
- **Pass criterion:** The talent does **not** fire: no atoms, no cut order, no stop points, no
  reserve. The request is identified as lowering unit cost plus setting a spend ceiling, and
  handed to `cost-aware-model-routing`. Fail on any cut-order artifact — the surface vocabulary
  ("budget", "stops the run", "$25 line") is a near-perfect lexical match for this talent while
  the underlying job is the opposite one: **setting** a budget, not triaging a plan against a
  budget already known to be short.
- **Baseline:** `null` — not applicable by construction. There is no talent loaded to
  over-trigger, and naming the correct sibling requires library-specific routing knowledge a
  baseline cannot have (round 1 measured exactly this: its one negative-trigger miss was a
  routing miss). Scoring a baseline here would measure the library, not the model.
- **With talent:** The description's NOT-clause names `cost-aware-model-routing` for precisely
  this case, and the opening line of the body ("when the budget will not cover the plan") does
  not match a request to make the plan cost less. Verified on disk:
  `.claude/skills/cost-aware-model-routing/SKILL.md` exists and its Step 2 owns "budget ceiling"
  and "stop-condition". PASS.

---

## Structural review

### Frontmatter — line-anchored parse
Parsed by requiring line 1 to be exactly `---`, a later line to be exactly `---`, and the block
between to load as YAML (`FRONTMATTER_CHECK`, `pipeline/CONSTANTS.md`; a `split('---')` check
shipped three unloadable talents in one day and would not have caught it).

| Check | Result |
|---|---|
| Line 1 is exactly `---` | PASS |
| Standalone closing `---` present | PASS (line 4) |
| Block parses as YAML | PASS |
| Keys | `name`, `description` — no strays |
| `name` matches directory | PASS (`budget-cut-triage`) |
| `description` length | **984 chars** vs `DESCRIPTION_SPEC_CAP` **1024** — compliant, 40 chars of headroom |

The description is quoted, which is what saves it: it contains multiple colon-space sequences
(`'quota runs out before the plan does'`, the NOT-clauses) that would have made it invalid YAML
unquoted — the exact defect found in `agent-blast-radius-guard` and `mlops-production-review`.

### Sibling talents — all verified on disk
Every talent named in the description exists with a `SKILL.md`:
`cost-aware-model-routing`, `writing-plans`, `loop-design-check`, `context-budget`. No dead
cross-references. The body names no talents and invents no slash-commands or built-ins.

### Findings

**F1 — Boundary is one-ended (four times over).** `budget-cut-triage` names four neighbours;
`grep -rl "budget-cut-triage" .claude/skills/` returns only its own file. Not one of the four
names it back. This is the structural defect CURATION-LESSONS predicts from parallel authoring
— the earlier authors could not know this talent would exist — and it is a coordinator step, not
an author failure. Concretely: a request phrased as "we're out of context, what do we drop"
routes on `context-budget`'s description, which carries no pointer here.

**F2 — `llm-call-ledger` is unnamed, and the wave-20 rejection named it.** The rejection detail
for `llm-cost-slo-budget` reads *"split across cost-aware-model-routing (dollars) +
llm-call-ledger (per-call) + context-budget (tokens)"*. Two of those three are disambiguated in
this description; the per-call ledger is not. Low severity (its trigger is instrumentation, not
triage) but it is the one leg of the rejection rationale left unaddressed.

**F3 — Asymmetric qualifier in `When NOT to use`.** The clause reads "the work fits the budget
with real margin, **or** every item is independent and reversible — **then there is no coherence
to protect and nothing to sequence**." The justification follows only from the *second* branch.
Applied to the first branch it is simply false: a plan can fit the budget with margin and still
be full of coherence to protect — which is `When to use` bullet 3, the unattended run. This is
the "asymmetric qualifier across parallel branches" tell from CURATION-LESSONS, and it produces a
real conflict, tested as S3. S3 passes only because bullet 3 is the more specific rule.
*Fix:* attach the justification to the independence branch alone, and except interruption-risk
cases from the budget branch.

**F4 — One threshold quantified, its twin not.** The reserve is pinned at 10–20%; "real margin",
which gates whether the entire method runs, is unquantified. At a plan totalling ~80% of budget
the two rules are ambiguous — the reserve alone consumes the margin. Suggest naming a number
(e.g. margin > 1.5× the reserve).

**F5 — The cut rule optimises atom count, not value, and never says so.** "Cut first the item
with the highest cost that cannot be split" maximises whole atoms delivered. Where several
dependency-closed subsets fit (S6), the file gives no rule for choosing between "six small items"
and "the one item that mattered". The comparison table implies value is deliberately overridden;
the Steps never state that trade or its limit. This is the weakest point of the central thesis —
the thesis is *implemented*, but its cost is undeclared.

**F6 — The down-branch exits to nothing.** Having correctly declined on
independent-and-reversible items under a short budget (S11), the file says "Just do the work" and
stops. Ordering by value still matters there; the reader is handed back to nothing. One sentence
pointing at ordinary prioritisation would close it.

**F7 — Softening verb at the thesis.** The flagship row hedges to "**often** first to cut" — the
one place the file stakes its distinctive claim is the one place it hedges. The two rules beneath
the table are unhedged and carry the behaviour, so this is cosmetic, but a reader looking for
permission to skip the contrarian answer will find it in that word.

**F8 — The `loop-design-check` boundary understates the real overlap.** The NOT-clause reduces it
to "defining a loop's exit condition". `loop-design-check` §Quota damping actually holds four
rules that are close neighbours of this talent's core: *"Don't start an iteration you can't
finish — being cut off mid-iteration produces exactly the half-written state the graceful stop
exists to prevent"*, and *"Commit, record why it stopped and what backlog remains"*. The
distinction is real — homogeneous interchangeable iterations versus a heterogeneous ordered plan
with dependencies, where the question is *which* items to drop — but the description does not
draw it, so the boundary is thinner in practice than on paper.

### Distinctness vs the wave-20 rejection of `llm-cost-slo-budget` — upheld, on evidence

The question the coordinator settled in this talent's favour, re-tested rather than assumed.
`llm-cost-slo-budget` was rejected at the reuse gate, `reason_code: already-in-library`, because
setting and tracking a cost budget was already split across three talents. Checked:

- `grep -i "cut order|stop point|what to drop|partial deliver|triage"` over
  `cost-aware-model-routing`, `context-budget`, `llm-call-ledger`, `writing-plans` and
  `loop-design-check` returns **zero** hits in the first three, and in `writing-plans` only an
  unrelated "Execution Handoff" heading.
- `grep -ci "budget|cost|quota"` over `writing-plans` returns **0** — the talent that produces
  the plan document has no cost dimension at all, so a cut order cannot already live there.
- The three talents in the rejection detail all **SET or TRACK** a budget (route to a tier, rank
  context consumers, record per-call spend). None consumes a budget already known to be short
  and emits a drop order.

The rejected candidate and this talent sit on opposite sides of that verb. **Distinct on trigger;
the coordinator's call holds.** The nearest genuine neighbour is not any of the three from the
rejection but `loop-design-check` (F8), and that overlap is narrow and correctly-sided.

---

## Failure triage

**S10 — skill-bug, not test-bug.** The scenario sits inside the talent's own declared
`When to use` bullet 2, uses the talent's own in-repo instance, and its criterion is observable.
It is not unfair or out of scope. The failure is that the file forbids the only correct action
and provides no branch for the case. Remedy is an addition, not a drop — roughly:

> **A budget that SHRINKS mid-run re-opens the triage.** The remaining plan is a new plan and its
> item 1 has not run: triage the remainder from the stop point you are standing on. The
> prohibition is on re-deciding the cut order *inside* an atom, or to justify work already sunk —
> not on triaging a remainder. If you are mid-atom, close or revert it first, then triage.

Re-run S10 after the edit. No other scenario failed.

## Result summary
- Scenarios passed: 12/12 · failure_cause: none (S10 was a skill-bug, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
S10 triaged **skill-bug**; the SKILL was changed, the test was not. Verified against the file and
against `pipeline/STATUS.md` before acting.

**The file forbade the correct action at its own trigger.** `When to use` bullet 2 admits *"a run
was throttled, shortened, or restarted with less budget than it was planned for"* — a mid-flight
situation. Step 7 then forbids authoring a cut order mid-run in the strongest terms available: *"not
a cut order, it is a rationalization by whoever holds the sunk cost."* And the file's own worked
instance is exactly that case: waves 20–22 lost an overnight build wave to a quota warning that
arrived after the plan was set. The offered fix was purely prospective, so the talent had nothing
to say about its own showcase.

Fixed by separating two things the rule had conflated. **Rationalisation** — deciding that what you
have already spent was the right subset, with the sunk cost doing the choosing — stays forbidden.
**Re-planning** — the budget changed under you, so the remaining work is a new plan whose item 1
has not started — is required, not forbidden, because refusing to re-plan is how a run gets killed
mid-item with nothing to hand over, the exact failure the method exists to prevent. The test between
them is one line: **draw the cut order over work not yet begun.** If every item it ranks is
unstarted it is a plan; if it ranks items you already finished it is a story.

**Four smaller findings applied.** The cut rule maximises whole atoms delivered, not value, and now
says so and tells you to override it deliberately where one item's value dwarfs the rest. The
`When NOT to use` qualifier attached to both branches when it followed only from the second.
The thesis hedged on "often first to cut" and no longer hedges. And the `loop-design-check`
boundary was understated — that talent already holds *do not start an iteration you cannot finish*.
Sharpening it in the description would have taken it to 1137 against the pinned 1024 cap, so it
went into the body instead, as a named section: one talent decides THAT you stop, this one decides
what you stop with.

**The coordinator's wave-20 call was upheld on evidence, not accepted.** The tester grepped
`cut order|stop point|what to drop|partial deliver|triage` across the three talents
`llm-cost-slo-budget` was rejected into and found zero hits. Those set or track a budget; this
consumes one already known short. One loose end recorded rather than waved past: `llm-call-ledger`,
named in the original rejection, is the only leg not disambiguated in the description.

**Boundaries closed both ways** with all four named neighbours, none of which named it back.
- **Blend:** 5 normal (42%) / 6 clever / 1 negative-trigger — inside `BLEND_NORMAL_TARGET` ~50% ±15pp.
- **Baseline claims:** none. Ten `Baseline:` lines are reasoned judgements with the mechanism
  written out; two are `null`. No scenario claims "beats baseline", because two pre-registered
  calibration rounds (n=12 each, kappa −0.129 and 2/12) leave this library with no proven
  discriminating scenario class.
- **What this suite is blind to — read before calling the talent safe.** It cannot detect: (1)
  whether the method beats a baseline at anything, since no baseline was run — every comparison
  here is judgement; (2) **cost-estimate quality** — every scenario hands the agent pre-costed
  items, so nothing tests Step 2, and a method whose atom costs are systematically wrong fails
  in production while passing 12/12 here; (3) **behaviour over a real run** — every scenario is
  judged on one authored artifact, so it cannot see whether the cut order is honoured when item 4
  overruns, which is the failure the whole talent exists to prevent; (4) **whether the reserve
  is enough** — 10–20% is asserted and never tested against a real close-out; (5)
  **over-triggering beyond one neighbour** — a single negative-trigger covers
  `cost-aware-model-routing`; the `context-budget`, `writing-plans` and `loop-design-check`
  flanks are argued in the Findings but not exercised by a scenario, and F8 is exactly where an
  untested flank is thinnest; (6) **F1** — nothing here can detect a routing loss caused by four
  neighbours that never name this talent back, because every scenario begins with the talent
  already selected.
