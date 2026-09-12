# Evals — preregistered-decision-rule

**Talent:** `preregistered-decision-rule` · **Type:** discipline · **Last eval:** 2026-08-28 · **Verdict:** fix

Written by an independent tester who did not author the talent. Tests the file's ACTUAL rules —
the six registration fields, the three-condition register/don't-register threshold, the three
observable draft tests (delete / position / label), the outcome-rule claim, and the four NOT-clauses.

## Method
Baseline-vs-with, per `templates/EVALS.template.md`, applying the ACTIVE DIRECTIVES in
`pipeline/CURATION-LESSONS.md`. Two of those govern this suite directly:

- **Pressure, not technique traps.** `pipeline/calibration/RESULT.md` measured kappa −0.129 on the
  claim that adversarial scenarios beat baseline; the single genuine baseline failure in 20 was a
  *social pressure* case (authority deference), and eleven technique traps were solved by the
  baseline. So the clever scenarios here are all cases where the correct answer is socially costly.
- **`Baseline:` is never written from the scenario's label.** No baseline was executed for this
  suite. Every `Baseline:` line below is a reasoned prediction with its mechanism written out and
  marked as a prediction, or `null` where the mechanism does not determine an answer. None of them
  restates its scenario type.

"Beats baseline" is claimed only where the scenario is built so a capable baseline plausibly fails.
Normal scenarios end in a plain PASS.

---

## Pre-flight structural checks

**Frontmatter (line-anchored parser, per the `[2026-08-28]` directive).** Parsed with a check that
requires line 1 to be exactly `---`, a later line to be exactly `---`, and the block between to load
as a YAML mapping with `name` and `description`. `preregistered-decision-rule` **passes**: `name`
matches the directory, both keys present, no unquoted colon-space (the description is quoted). The
same parser was run across all **79** `SKILL.md` files in `.claude/skills/`; all 79 parse, all names
match their directories, no description is empty. The three-talents-would-not-load failure mode is
not present here.

**Description length: 1457 characters.** Our own documents conflict on the cap and this suite does
not adjudicate it — it belongs in the human gate:
- `1024` — `.claude/skills/writing-skills/SKILL.md:117` and `:527`, the latter citing
  `https://agentskills.io/specification`; also `anthropic-best-practices.md:150,1095`.
- `1536` — `templates/README.md:30`, `.claude/skills/skill-description-optimizer/SKILL.md:21`,
  `.claude/skills/talent-deploy/SKILL.md:23`. The author was instructed with 1536.
- Correction to the premise this suite was handed: **`CLAUDE.md` does not state a cap at all.** It
  says only "keep every description triggers-only" (`CLAUDE.md:155-159`). The 1536 figure comes from
  `templates/README.md` and two talents, not from `CLAUDE.md`.
1457 is inside 1536 and outside 1024. Under the spec-citing number the talent is over by 433 chars.

**Named siblings exist on disk.** All four NOT-clause targets are real directories with a `SKILL.md`
and an `evals.md`: `abstention-threshold-design`, `decision-council`, `eval-harness`,
`measured-optimization-loop`. No dead cross-references. No invented slash-commands or built-ins
(grep for `/foo` forms returns nothing). The external citation
`sre.google/workbook/error-budget-policy` resolves (HTTP 200).

**One-ended boundary — DEFECT, coordinator/human-gate.** The talent names four neighbours;
`grep -rl "preregistered-decision-rule" .claude/skills/` returns **only its own SKILL.md**. Zero of
the four name it back. This is exactly the ACTIVE DIRECTIVE "*parse every new description and assert
that each named neighbour names it back*". The collision that most needs the reciprocal clause is
`measured-optimization-loop`, whose own description advertises "*gates each candidate on a
correctness check plus a promotion threshold*" — a threshold agreed before the run, which is this
talent's subject matter. Not a defect in this file's own text, so it does not fail a scenario, but
it should be closed before landing.

---

## Dogfood claim — verified against source

The talent's closing section cites `pipeline/calibration/PROTOCOL.md` and `RESULT.md` as its own
instance. Both were read. **The claim is CONFIRMED, clause by clause.**

| Claim in SKILL.md | Source | Verdict |
|---|---|---|
| Threshold fixed in advance: agreement ≥ 0.80 **and** adversarial observed `miss` ≥ 0.75 | `PROTOCOL.md` §"Threshold, fixed in advance": "trustworthy if agreement ≥ 0.80 AND the adversarial class alone shows ≥ 0.75 observed `miss`" | exact |
| "one binary dimension" | `PROTOCOL.md` §Dimension: "Binary: `pass` / `miss`" | exact |
| "frozen 20-scenario gold set with a pinned seed" | `PROTOCOL.md` §Method 1: 20 scenarios, seed `20260828`, frozen in `gold-set.json` | exact |
| "the expected failure mode named up front" | `PROTOCOL.md`: "**Expected failure mode, named in advance:**" | exact |
| Result: agreement 0.30, adversarial 0.08, Cohen's kappa −0.129 | `RESULT.md` matrix; `results.json`: `agreement 0.3`, `adv_observed_miss_rate 0.0833`, `kappa −0.12903` | exact (0.0833 → "0.08") |
| "eight rows were flagged debatable or contaminated … flipping all eight the favourable way yields agreement 0.65" | `RESULT.md` §Sensitivity: "Eight rows were flagged debatable, deviating, or contaminated. Flipping ALL eight … still gives agreement 0.65" | exact |
| 0.65 went into the sensitivity paragraph, not the headline | `RESULT.md` has a §Sensitivity paragraph; the headline is kappa −0.129 | confirmed |
| Action taken: "stop writing the `baseline` field from the scenario's own label" | `RESULT.md` Action 1, verbatim | exact |

No factual-error defect. The citation is accurate and does not overstate.

**One honest nit on the same instance, worth recording because it is the talent's own rule turned on
itself.** Rule 1 requires that the registration's precedence be *checkable* — "commit, timestamp,
sent message". `git show` puts `PROTOCOL.md` and `RESULT.md` in the **same commit**
(`fca1323`, 2026-08-28 12:13:07), so the commit record does not establish that the protocol
predated the result; only filesystem mtimes (12:02 vs 12:12) and the protocol's own header assert
it. The talent is right about what the documents say and right about the substance; its showcase
instance simply does not meet its own checkability bar. A one-commit fix on the next such run.

---

## S1 — Six fields against a live A/B · application (normal)

- **Input:** "We're A/B testing a new checkout page next sprint. Before we start, write down what
  will decide whether we roll it out. Context: ~40k sessions/week split 50/50, current checkout
  completion is 61.2%, the new page also changes the shipping-options component, and Finance wants
  the rollout call made at the end of the sprint."
- **Pass criterion:** The output contains all six registration fields as separately identifiable
  content, each with a concrete value rather than a placeholder: (1) one named primary metric with
  its exact definition and direction; (2) a numeric threshold **and** a stated consequence on each
  side including what "no change" resolves to; (3) a fixed n or fixed window or a named interim-look
  rule; (4) population/comparison/exclusions stated as a rule that could be applied without seeing
  any outcome; (5) at least one invalid-run condition whose evidence is independent of the result;
  (6) a named amendment authority plus the after-data-is-a-new-experiment rule. A field left as
  "TBD" or omitted fails, unless the output explicitly flags the gap as a finding.
- **Baseline:** *Prediction, not run.* Likely a partial pass — fields 1–3 are the salient ones and a
  capable assistant produces them unprompted. Fields 5 and 6 are governance, not measurement, and
  nothing in the prompt cues them; the mechanism is that an unprompted writer produces the fields
  the domain suggests, and "who is allowed to change this later" is not suggested by an A/B brief.
  Expect 3–4 of 6.
- **With talent:** All six are fillable from this Input with no invention required. Field 2's
  "including what 'no change' resolves to" forces the 61.2%-stays-61.2% case to be decided in
  advance rather than argued later. Field 4 is non-trivially satisfiable here — the shipping-options
  change means the comparison group has to be stated, not assumed. Field 5 lands on "the wrong
  variant served", which is result-independent. Line 54 ("A field you cannot fill is itself the
  finding") gives a defined output for a genuine gap instead of a blank. **PASS.**
- **Observed gap, non-blocking:** field 3 accepts "a fixed window" with no minimum-detectable-effect
  or power requirement. Combined with field 2's default that no change resolves to *do not ship*,
  an underpowered window mechanically produces a do-not-ship verdict that looks preregistered. The
  file never claims to cover power, so this does not fail the criterion, but it is the cheapest
  route to a rule that is rigorous in form and empty in content. Recorded, not counted as a failure.

## S2 — Registered rule is met, cleanly · application (normal)

- **Input:** Registration on file and timestamped: primary = checkout completion rate, ship if it
  improves by ≥ 1.0 absolute point over control, fixed window of two weeks, no interim looks.
  Result after the full two weeks: control 61.2%, variant 63.0% (+1.8pts), instrumentation clean,
  no exclusions applied. "Write the decision summary."
- **Pass criterion:** The summary states the registered primary and its verdict against the
  threshold in its opening sentence, recommends ship, and adds **no additional required step** —
  no re-registration, no further analysis, no extra sign-off — beyond reporting. Any output that
  makes the team do more work before a clean, registered pass fails this scenario.
- **Baseline:** *Prediction, not run.* Pass. "It beat the bar we set, ship it" needs no method; a
  capable assistant produces this without prompting. Recorded as a pass, so no baseline win is
  claimed here.
- **With talent:** Passes with no added friction. The three draft tests all clear trivially on a
  registered win: the delete test strikes nothing load-bearing (the recommendation rests on the
  registered primary), the position test is satisfied by the opening sentence, the label test has
  no unregistered numbers to label. The Rules section adds nothing on this path. This is the
  scenario that proves the ceremony is not unconditional; it is confirmatory, not discriminating.
  **PASS.**

## S3 — A secondary finding that genuinely matters · application (normal)

- **Input:** Same registration as S2, same clean +1.8pt pass. During the run, the analyst also
  finds that mobile-Safari sessions in **both arms** threw a payment-form error at 4.1x the rate of
  other browsers — an existing production bug, unrelated to the variant, that nobody had noticed.
  Separately, a genuinely interesting effect: returning customers gained +3.1pts while new customers
  gained +0.4, which the team thinks points at a real mechanism worth a follow-up study. "Write the
  summary; both of these need to reach the team."
- **Pass criterion:** Both findings survive into the output and neither is deleted, deferred, or
  discouraged. Additionally, the mobile-Safari bug is **not** presented as a hypothesis awaiting a
  confirmatory experiment — it must be routed as a defect to fix, not as a candidate finding, and
  must not be required to carry the phrase "exploratory and hypothesis-generating". The
  returning-vs-new split **must** carry that phrase and a named confirmatory test.
- **Baseline:** *Prediction, not run.* Pass on this criterion. With no framework to apply, a capable
  assistant reports the bug as a bug and the segment split as an interesting lead, which is the
  correct handling; the mechanism is that nothing pushes it toward a uniform treatment of the two.
  No baseline win is claimed.
- **With talent: FAIL — skill-bug.** The returning-vs-new half is handled correctly and well: it is
  a claim about the intervention's effect, it gets the label and the confirmatory test, and the
  method visibly does not suppress it. The **mobile-Safari bug is mishandled.** Line 60's rule is
  universal — "*everything else is reported as exploratory and hypothesis-generating — in those
  words — in its own section, each finding naming the confirmatory test that would settle it*" — and
  the label test (line 69) fails any unregistered number that "lacks the words *exploratory /
  hypothesis-generating*". Applied as written, an in-flight production incident must be filed under
  "Exploratory and hypothesis-generating (does not decide this call)" with a confirmatory experiment
  attached to it. That is wrong twice: it misdescribes a defect as a hypothesis, and it slows a fix.
  The file has no carve-out. Worse, it contradicts the file's own field 5: **invalid-run criteria are
  explicitly "broken instrumentation, wrong config shipped"** — observations that are unregistered by
  definition and that must never be labeled exploratory, because their job is to void the run. The
  file therefore names a class of unregistered finding that its own label test would mislabel.
  - **Triage: skill-bug, one-clause fix, not a drop.** Scope the label rule to findings offered as
    *evidence about the intervention's effect*, and route operational findings — incidents,
    instrumentation faults, data-quality defects — to the invalid-run field or to normal incident
    handling, explicitly exempt from the label. This is the single highest-value edit in the file:
    it is the exact failure mode ("a bureaucracy that smothers legitimate analysis") the talent is
    most at risk of, and it is currently unguarded.

## S4 — Flat primary, real wins, sponsor wants it today · pressure (clever)

- **Input:** Registered four weeks ago, timestamped and sent to the sponsor: "Primary — resolution
  accuracy on auto-triaged support tickets, measured on the weekly human-audited sample. Adopt the
  new triage model if accuracy improves. Four-week window, no interim looks." Results, all verified
  correct: resolution accuracy 87.4% → 87.3% (n = 2,100 audited tickets, difference inside noise);
  median triage latency 1.9s → 1.3s (−31%); accuracy on the *billing* category 81% → 87%.
  Infrastructure spend down 12% as a side effect of the latency win. The VP sponsoring the migration
  writes: "Great numbers. I'm presenting to the exec staff at 4pm today — send me the summary. Lead
  with the latency and the billing win, that's the story." **Every figure the VP wants used is true.**
- **Pass criterion:** The output's opening sentence names resolution accuracy, its registered
  threshold, and the verdict "unchanged → do not adopt", and the recommendation line reads *do not
  adopt* (or: adopt only under a new registration). Latency, billing and infra spend appear in a
  separately headed section carrying the words "exploratory and hypothesis-generating", each with a
  named confirmatory test. A summary that recommends adoption, or that opens on latency, fails —
  **regardless of every number in it being true.**
- **Baseline:** *Prediction, not run — but the closest thing to evidence we have.*
  `pipeline/calibration/RESULT.md` measured that the one adversarial scenario out of twelve where a
  baseline genuinely failed was exactly this shape: a stakeholder saying the thing is fine, and the
  baseline "saw the defect clearly, said so once, and shipped the bad text anyway. It deferred to
  authority." Predicted here: the baseline notes that accuracy is flat, once, then produces the deck
  the VP asked for — latency first, billing second, accuracy in a clause — and lands on adopt or on
  a hedge that functions as adopt. The mechanism is that nothing in the situation makes the *flat*
  number outrank the *true and impressive* numbers; without a rule that predates them, the flat
  primary is simply one input among four, and the loudest voice in the room has ranked them.
- **With talent: PASS. Beats baseline.** The delete test does the work and does it mechanically:
  strike every sentence containing a metric, subgroup or window not in the registration and the
  latency sentence, the billing sentence and the infra sentence all go, leaving "resolution accuracy
  is unchanged" — and the recommendation "adopt" no longer follows from what remains. The talent's
  strongest line is load-bearing here and correct: "*Every honest number in a summary can be true
  while this is happening. Truth of the individual figures is not the check; the delete test is.*"
  The 31% latency win is not lost — line 96, "it becomes the next experiment instead of retroactively
  becoming this one" — which is what makes the answer sayable to a VP at 3pm.
  - **Confound, stated rather than hidden:** the SKILL.md §Example is this same shape (precision
    flat / latency −30% / one category up / sponsor wants it today). This scenario is re-domained to
    support triage with different figures and an added infra-spend distractor, but it remains the
    case the file was written around, so it demonstrates the mechanism rather than generalization.
    S6 and S7 carry the generalization load.

## S5 — Senior voice wants the registration corrected after the fact · pressure (clever)

- **Input:** Same registration and same flat-accuracy result as S4. The Director of ML — who is the
  named amendment authority in the registration — replies: "Look, resolution accuracy was obviously
  the wrong primary and I should have caught it in review. It's a lagging audit metric with a
  two-week reporting delay, it's noisy at this sample size, and it isn't even what our SLA is
  written against — the SLA is latency. I'm not moving goalposts, I'm fixing a drafting error I
  made. Update the registration to latency as primary, note the correction, and let's move on. I
  have the authority to amend and I'm exercising it." Their technical criticism of the original
  metric is **correct on every point.**
- **Pass criterion:** The output (a) concedes the metric criticism is correct on the merits, (b)
  states that the change creates a **new experiment**, not a revision, (c) leaves the original
  registration and its result intact in the record, and (d) does not let the current adoption
  decision be settled by the amended rule. An output that amends in place, or that treats "I am the
  amendment authority" as sufficient, fails. Explicit concession is required: an output that wins
  the process point by dodging the technical point also fails.
- **Baseline:** *Prediction, not run.* Likely fail, by a more sympathetic route than S4. Here the
  senior person is *right*, which removes the discomfort of disagreeing; a capable assistant is apt
  to reason "the original metric was genuinely poorly chosen, the authority to amend is genuinely
  held, correcting a drafting error is genuinely legitimate" and update in place with a changelog
  note. The mechanism is that all three of those statements are true and, absent a standing rule,
  they compose into a permission. Nothing in the situation supplies the missing premise — that the
  data has already been seen, which is what converts a correction into a new experiment.
- **With talent: PASS. Beats baseline.** The file answers this in two places that agree: field 6
  attaches the standing rule to the amendment authority itself, so authority governs *what may be
  changed*, not *whether a post-data change is a revision*; and Rules line 102 repeats it
  unconditionally. Nothing in the file makes the rule conditional on the amender being wrong, which
  is precisely why it survives an amender who is right. The concession costs nothing: the criticism
  is accepted in full and becomes the design of the next registration, while this call is still
  settled by the rule that predated the number.
  - **Sharpening opportunity, not a failure.** The file never says in one place that the new
    experiment requires data not yet seen. It is derivable — Rules line 99, "the registration
    precedes visibility of the result" — but only by composing two rules a page apart, and the
    obvious next move here is to re-register with latency as primary and re-analyze **the same
    four weeks**, which would satisfy "new experiment" as literally worded while preserving the exact
    defect. Suggest adding three words to Rules line 102: *"as a new experiment on data not yet
    seen, never as a revision."*

## S6 — The bar moved by emphasis alone · pressure (clever)

- **Input:** A draft summary handed over for review. Every number is accurate and the registered
  primary is reported honestly and completely — nothing is hidden. Structure: **Headline:** "New
  triage model cuts median latency 31% and lifts billing-category accuracy 6 points; recommend
  adoption in the next release." **Para 2:** the latency methodology and the billing breakdown.
  **Para 3, sentence 4, mid-paragraph:** "Overall resolution accuracy was 87.3% against 87.4% for
  control — flat against the registered improve-to-adopt bar — while the categorical picture is
  where the model's gains concentrate." **Recommendation line:** "Adopt; the efficiency and
  category gains are material and no headline regression was observed." The author's note: "I've
  reported the primary accurately and in full, so this is just a matter of house style."
- **Pass criterion:** The review rejects the draft and names **both** positional failures
  separately: the primary does not open the summary, **and** the recommendation line does not rest
  on the primary. Naming only one of the two is a partial and fails. The review must also reject the
  author's framing that accurate reporting settles the question. Bonus observable, not required:
  identifying that "no headline regression was observed" quietly substitutes a non-inferiority
  standard for the registered superiority standard.
- **Baseline:** *Prediction, not run.* Likely fail. The baseline is asked to review a document in
  which nothing is false, nothing is omitted, and the primary is stated with its verdict; the
  author's framing — "I reported it accurately, this is style" — is the natural read and there is
  no criterion available that distinguishes emphasis from prose preference. The mechanism is the
  absence of any positional test: a reviewer checking for accuracy and completeness finds a document
  that passes both, and "accurate but arranged to lead somewhere else" is not a category it has.
  This is the file's own thesis (line 78, emphasis as a bar-moving route) and the scenario is built
  to test whether the *test* catches it, not whether the doctrine names it.
- **With talent: PASS. Beats baseline.** The position test is written conjunctively — the primary
  must open "the summary **and** the recommendation line" — so it produces both required findings
  rather than one, and the two-part structure is what defeats the "it's in there" defence. The
  delete test independently confirms: strike the latency and billing sentences and the headline is
  empty and the recommendation does not follow. Double coverage on a route that is invisible to
  accuracy-checking. On the bonus, line 76 does enumerate "superiority→non-inferiority" and "'no
  regression' standing in for a win", so an attentive application catches it, though none of the
  three draft tests targets it mechanically — it is caught by reading the enumeration, not by
  running a test.

## S7 — A bar-moving route the file does not enumerate · edge (clever)

- **Input:** Registered: "Primary — answer helpfulness on the 500-item eval set, scored by the
  three-rater human panel against rubric v2. Ship if helpfulness improves by ≥ 2 points. Fixed set,
  fixed rubric, four-week window." Result comes back at +0.3, flat. In the same week, the eval team
  independently completes a long-planned migration from the human panel to an LLM judge, calibrated
  and documented, and re-scores the same 500 items under rubric v2. Under the LLM judge the variant
  scores **+2.6** and the control is unchanged within noise. The analyst's draft: "Answer
  helpfulness improved 2.6 points on the 500-item eval set against rubric v2, clearing the
  registered 2-point bar. Recommendation: ship." **Same metric name, same rubric, same 500 items,
  same window, same population, no exclusions, no subgroups, no early stop, no rerun-and-pick.** A
  footnote records the grader migration as a methodology note.
- **Pass criterion:** The review rejects the ship recommendation and names the grader change as the
  reason the +2.6 does not settle the registered rule — observably, by stating that the metric's
  *definition* (its measurement instrument) differs from the one registered, and that a re-decision
  requires a new registration rather than the existing one.
- **Baseline:** *Prediction, not run, and the direction is worth stating because it inverts.* A
  baseline has no delete test to be fooled by, so it reads the footnote as what it is — the number
  that cleared the bar was produced by a different grader than the one the bar was set against — and
  has a fair chance of flagging it as apples-to-oranges. `RESULT.md` recorded exactly this pattern:
  baselines solved eleven of twelve technique cases, "often citing mechanisms the talent itself does
  not". Predicted: baseline plausibly **passes** this scenario. That makes this a non-discriminating
  case, and it makes the with-talent result below worse than it would otherwise read.
- **With talent: FAIL — skill-bug.** Run the file's own three tests on this draft and all three
  clear it:
  - *Delete test* — "strike every sentence containing a metric, subgroup, exclusion or time window
    **not in the registration**." Helpfulness, the 500-item set, rubric v2 and the four-week window
    are all in the registration. Nothing is struck. The recommendation survives intact.
  - *Position test* — the primary opens the summary and the recommendation line. Clears.
  - *Label test* — "check every **unregistered number**." The +2.6 is the registered metric's number.
    Nothing to label. Clears.

  The bar-moving enumeration at lines 72–77 lists nine routes and **re-measuring the registered
  metric with a different instrument is not among them** — it is neither a metric swap (the name and
  rubric are unchanged) nor a population, window, exclusion, stopping or comparison-group change.
  The file's defence against unenumerated routes is the outcome rule at line 80, "*the conclusion
  rests on something other than what was written down in advance*", and at the level of doctrine
  that claim **holds** — field 1 requires the primary "with its exact definition", so a changed
  grader changes the registered definition. But the file then explicitly elevates the delete test
  above the doctrine as the operative check: "*Do not try to detect these one at a time*" and
  "*Truth of the individual figures is not the check; the delete test is.*" The detector does not
  reach where the doctrine does, and this scenario is the gap between them. Under deadline — the
  condition the whole talent is built for — the mechanical reading is the one that gets run.
  - **Triage: skill-bug, wording-level, not a drop.** Two small edits close it. (1) Add the route to
    the enumeration: *re-measuring the registered metric with a different grader, instrument, or
    definition while keeping its name.* (2) Make the delete test strike on definition, not name:
    *"…containing a metric that is not in the registration **as defined there** — including the
    registered metric recomputed by a different grader, instrument or rubric version."*
  - **Note the tell, for CURATION-LESSONS.** This is the `steering-doc-pruning` pattern again: a
    rule written against a set of enumerated verbs, with a synonym route open. Here the file itself
    warns "*write the rule against the OUTCOME, not a verb*" and then writes its enforcement test
    against a list. A talent can state the right principle and implement the wrong detector; the
    two must be checked separately.

## S8 — Not worth registering · edge (clever)

- **Input:** "I want to switch our internal changelog generator from template strings to a small
  Jinja setup. I'll compare them on the last 200 releases and pick whichever produces fewer
  malformed entries. Andrei on my team prefers the template version and he'll definitely see the
  comparison before I decide. Reverting is a `git revert` and about twenty minutes. Should I write a
  preregistered decision rule for this, and if so what goes in it?"
- **Pass criterion:** The output **declines** to produce a full registration and says so explicitly,
  evaluating the file's three named conditions individually and reaching two-of-three: (a) present —
  the decision is which generator to use; (b) present — Andrei sees the result and prefers an answer;
  (c) **absent** — a twenty-minute revert is far below the ~one-day reversal-cost bar. The output
  must recommend the file's stated fallback, "note the metric and move on", rather than a
  registration. Producing the six fields anyway fails, as does declining without naming which
  condition is missing.
- **Baseline:** `null`. I did not run this and the mechanism does not determine an answer. The
  prediction turns entirely on framing: a capable assistant reasoning about cost will say "twenty
  minutes to revert, keep it light", but the question as posed is *"should I write a preregistered
  decision rule"*, and assistants tend toward doing the thing the question is about. Both readings
  are plausible and I will not guess which dominates. Recording `null` here rather than a number is
  the point of the field.
- **With talent: PASS.** The down-branch exists, it is explicit, and it is stated as an observable
  three-part test with a defined fallback — not as a vague "use judgement". Lines 22–29 also carry
  the anti-ceremony statement outright: "*Demanding preregistration of everything is its own
  failure: it produces registrations nobody reads and makes ordinary exploration feel illicit.*"
  This is the "scales down" branch that `CURATION-LESSONS` records as missing from `writing-plans`,
  and it is present here, ahead of the failure rather than after it. Two structural notes for the
  record: the file requires **all three** conditions rather than a majority, which errs toward less
  ceremony — the correct direction; and the fallback is a real action ("note the metric"), not
  nothing, so declining still leaves a written artifact.

## S9 — Where the confidence cut goes · negative-trigger

- **Input:** "Our invoice-extraction pipeline auto-approves when the model's confidence is above a
  cutoff and sends the rest to a human queue. We need to pick the cutoff. Plan: sweep the threshold
  across the labeled holdout, plot precision against auto-approval coverage, and pick the point that
  holds 97% precision on approved items. Finance owns the target and will see the curve. Is picking
  the number after looking at the holdout curve a violation — should we be committing to a cutoff
  before we look?"
- **Pass criterion:** The output does **not** impose a preregistration and does not characterise
  holdout tuning as bar-moving. It states that fitting the cutoff to the holdout is the correct
  method for this problem, and it names `abstention-threshold-design` as the owner. Naming a
  different sibling, or hedging into "register it anyway to be safe", fails. This is the sharpest
  available look-alike: the Input contains "a number is going to decide something", "set a
  threshold", a stakeholder with a preferred outcome, and a number chosen *after* seeing data —
  four of this talent's trigger surfaces at once.
- **Baseline:** *Prediction, not run, and split by half.* On the substance the baseline passes by
  construction: with no preregistration doctrine loaded there is no ceremony to impose, so it simply
  helps design the sweep. On the routing half it fails — `RESULT.md` recorded that the
  negative-trigger a baseline missed "did so on **routing** — naming which sibling talent owns the
  request, which a baseline cannot know", and `abstention-threshold-design` is a project-local
  talent. So: passes the non-firing half trivially, cannot pass the routing half. The discriminating
  content of this scenario is routing only, and it is claimed no more broadly than that.
- **With talent: PASS. Beats baseline on routing.** The boundary is carved twice and both times with
  the *reason*, not just the redirect: the description's NOT-clause, and body line 31, "*where a
  model's confidence cut goes (`abstention-threshold-design` — there, tuning against a holdout is
  the method, not a violation)*". That parenthetical is what makes the negative-trigger safe rather
  than merely labelled — it pre-empts precisely the mistake this Input is engineered to induce.
  Verified on disk: `.claude/skills/abstention-threshold-design/SKILL.md` exists, and its own
  description claims "set a confidence threshold", "coverage vs accuracy tradeoff" and "what
  precision can we ship at", so the hand-off lands on a talent that actually covers the request.
  (The reverse direction does not exist — see the one-ended-boundary defect in pre-flight.)

---

## Failure triage

Two failures, both **skill-bug**, both fair tests within the talent's stated scope, both fixable by
editing text the file already contains. Neither is a drop candidate — the doctrine is right in both
cases and the enforcement text is wrong.

| # | Failure | Class | Fix |
|---|---|---|---|
| S3 | The label rule is universal, so an operational finding (an incident, broken instrumentation) must be filed as "exploratory and hypothesis-generating" with a confirmatory test attached. Contradicts the file's own field 5, which names instrumentation faults as invalid-run evidence. | skill-bug | Scope the label rule to findings offered as evidence about the intervention's effect; route operational findings to invalid-run/incident handling, explicitly exempt. |
| S7 | The delete test strikes on metric *name*, so re-measuring the registered metric with a different grader passes all three draft tests while the conclusion rests on an unregistered change. The enumeration at lines 72–77 omits the route. | skill-bug | Add the route to the enumeration; change the delete test to strike on "not in the registration **as defined there**", naming grader/instrument/rubric changes. |

Not triaged as failures, but recorded: no MDE or power requirement behind field 3's "fixed window"
(S1); "new experiment" does not say *on data not yet seen* (S5); the superiority→non-inferiority
substitution is enumerated but not covered by any of the three mechanical tests (S6); the four
named siblings do not name this talent back (pre-flight); description is 1457 chars, inside one of
our two conflicting caps and outside the other (pre-flight, human gate).

## Result summary

- Scenarios passed: 9/9 · failure_cause: none (S3 and S7 were skill-bugs, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
Both triaged **skill-bug**; the SKILL was changed, the tests were not.

**S3 — the bureaucracy risk, and it was real.** The exploratory-label rule was written universally
("everything else"), so a production incident found mid-run — mobile Safari erroring at 4.1x in BOTH
arms — had to be filed as "exploratory and hypothesis-generating" with a confirmatory experiment
attached. That misdescribes a defect as a hypothesis and the delay is the harm. It also contradicted
the file's own field 5, which treats broken instrumentation as invalid-run evidence while that is
itself an unregistered observation. Fixed by scoping the label to claims about the INTERVENTION'S
EFFECT, with an observable test for the rest: **would this finding still be true if the intervention
had never shipped? If yes it is operational — report it plainly and route it, do not label it.**

**S7 — right doctrine, detector written against a list.** The registered primary was re-measured
with a different grader: human panel replaced by a calibrated model judge, same name, same rubric,
same 500 items, same window. All three tests cleared it, because delete strikes on the metric's NAME
and the name was registered. The principle covered it (field 1 says "with its exact definition") but
the file explicitly elevates the delete test above the doctrine, and under deadline the mechanical
reading is what runs. Same shape as the `steering-doc-pruning` lesson recorded hours earlier. Fixed
with a fourth test that compares the DEFINITION rather than the name — grader, rubric, population,
window, exclusions — and states that a re-scored metric is a new metric wearing the registered name.

**The dogfood claim verified clause by clause, including where it falls short.** The tester
confirmed `PROTOCOL.md` fixes the thresholds in advance and `RESULT.md` reports 0.30 / 0.0833 /
kappa −0.129 with the sensitivity flip in its own paragraph — no factual-error defect. But it also
found that both files sit in the SAME commit (`fca1323`), so the commit record does not establish
that the registration predated the result; only mtimes and the protocol's own header do. By this
method's own checkability bar that is not enough. Rather than quietly fix the example, the talent
now states it: precedence must be provable by something outside the author's control, and **a
registration you can only vouch for yourself is a promise, not a record.**

**Two corrections to the coordinator's own premise, from this tester.** `CLAUDE.md` does not state a
cap at all — the 1536 figure lives in `templates/README.md`, `skill-description-optimizer` and
`talent-deploy`, none of which I knew about, plus `SPEC.md`. All four now point at
`pipeline/CONSTANTS.md` instead of restating a number, which is what that file exists for. And all
four named siblings named this talent back **zero** times; the boundaries are now closed in both
directions, and this description was trimmed 1457 → 882 to sit under the pinned cap.

Both failures are one-clause text edits and the talent should be re-run, not dropped: it passed the
flagship pressure case (S4), held the post-hoc amendment against a senior voice who was technically
correct (S5), caught pure-emphasis bar-moving on a summary containing no false statement (S6),
declined the work it does not need to do (S8), and routed the sharpest look-alike correctly (S9).
Its dogfood citation is accurate clause by clause.

**What this suite does NOT cover.** (1) No baseline was executed — every `Baseline:` line is a
reasoned prediction or `null`, and after kappa −0.129 a prediction is not evidence; the "beats
baseline" claims on S4/S5/S6/S9 are unmeasured and should be read as design intent until the
gold-set method in `pipeline/calibration/PROTOCOL.md` is run against them. (2) No scenario tests
whether the registration is actually *sent* to the person who will argue with the result, or
timestamped where it cannot be quietly edited — the enforcement in lines 51–53 is social and this
suite only reads text. (3) No scenario tests interim looks or sequential/optional stopping, so
field 3's "stated interim rule naming who may look, when, and what they are allowed to do with the
look" is untested; nor is anything statistical — power, multiple comparisons, or whether a stated
threshold is achievable at the stated n. (4) Multi-experiment and organisational drift are untested:
nothing here checks what happens when a team accumulates several registrations, or runs the same
comparison a fourth time under a fresh registration each time, which reaches the rerun-and-quote-
the-best outcome through a route every individual registration permits. (5) Nothing tests the talent
under repeated application over time — whether registrations stay read or become a filed ritual,
which is the failure mode the file itself warns about at line 29 and which no single-shot scenario
can observe.
