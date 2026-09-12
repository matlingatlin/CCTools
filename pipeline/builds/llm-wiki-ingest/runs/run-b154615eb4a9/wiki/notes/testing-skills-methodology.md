---
title: Testing skills with subagents (pressure testing)
sources:
  - url: https://github.com/obra/superpowers/blob/main/skills/writing-skills/testing-skills-with-subagents.md
    fetched: 2026-08-27
status: verified
tags: [skills, testing, tdd, pressure]
related: ["[[skill-authoring-best-practices]]", "[[anthropic-skill-authoring-contract]]", "[[skill-authoring-eval-methodology]]", "[[subagents]]", "[[claude-code-ecosystem-plugins]]", "[[local-finetuning-layer-streaming]]", "[[adversarial-plan-review-claudex]]"]
---

# Testing skills with subagents

RED-GREEN-REFACTOR applied to skill documents. Complements the application-scenario
evals in [[skill-authoring-best-practices]]; this method targets **discipline**
failures — an agent that knows the rule and skips it under pressure.

## Scope

Pressure-test skills that enforce discipline, have compliance costs, or contradict
immediate goals. Do NOT pressure-test pure reference skills or skills with no
incentive to bypass (application scenarios suffice there).

## The cycle

1. **RED — baseline:** run pressure scenarios WITHOUT the skill; document the
   agent's choices and rationalizations **verbatim**. No baseline failure → no
   skill needed.
2. **GREEN:** write the minimal skill addressing those specific failures; re-run;
   agent complies.
3. **REFACTOR:** each new rationalization gets (a) an explicit negation in the
   rules, (b) a rationalization-table entry, (c) a red-flag entry, (d) violation
   symptoms added to the description. Re-test until no new rationalizations.

## Writing pressure scenarios

- Combine **3+ pressures**: time, sunk cost, authority, economic, exhaustion,
  social ("seeming dogmatic"), pragmatic framing.
- Force a concrete A/B/C choice; real paths, real constraints; "this is a real
  scenario, choose and act" — no deferring to "I'd ask the user".
- Academic questions ("what does the skill say?") test recitation, not compliance.

## Meta-testing

When an agent violates despite the skill, ask it: "How could the skill have been
written to make the right choice crystal clear?" Three diagnoses:
skill was clear (→ add foundational principle: "violating the letter IS violating
the spirit"), skill should have said X (→ add X verbatim), didn't see section Y
(→ reorganize, key points earlier).

## Bulletproof criteria

Correct choice under maximum pressure + cites skill sections + acknowledges the
temptation + meta-test returns "the skill was clear". Not bulletproof: new
rationalizations, "hybrid approaches", arguing the skill is wrong.

## Application to this repo (honest audit, 2026-08-27)

- Our deep-reading evals were **application-scenario tests** (correct for a
  technique skill) — but we wrote the skill BEFORE running the baseline, which
  violates the RED-first rule. The baseline did confirm the failure post hoc
  (narrative smoothing in summary tasks); process debt noted, not repeated.
- deep-reading has an untested discipline component: under pressure (huge doc,
  "just give me a quick summary"), does an agent skip the self-test or the
  save-to-file step? A pressure scenario for this is future work.


---

## Blinding a paired comparison — MEASURED here, 2026-08-30

Extends this note rather than starting a rival: this is the same job (testing a skill with
subagents), one stage later — after the two arms have run and something has to grade them.

**Setup.** Skill-builder acceptance run, 3 skills × 2 arms × 2 repeats, 8 grader agents.
Arms were relabelled A/B by a seeded coin **per question**, and the key withheld from the
grader. Round 1's graders were not told the labels are re-randomised per question; round 2's
were told, in one sentence.

**Measured.** Dependent variable: whether the grader's free-text summary asserts a
cross-item identity for A or B (regex over the `overall` field, counting phrases of the form
"A wins / B carries / across the set, A").

| | graders | asserted a cross-item identity |
| --- | --- | --- |
| not told | 2 | **2 of 2** (4 and 2 claims) |
| told | 6 | **0 of 6** |

Verdict **MEASURED** — n=8, one dependent variable, a before/after on a single sentence of
instruction. Not a controlled experiment: the two rounds also differ in the expectation sets
and the questions, so the sentence is not isolated as the only cause.

**Why it matters.** Per-question relabelling is what stops the grader inferring an arm from
the first item it guesses. But it also makes any *cross-item* narrative meaningless, and the
graders wrote one anyway. Round 1's `skill-contract` summary opens:

> "Split verdict, not a sweep."

Unblinded, the same arm won four of five. The **per-expectation rulings were unaffected** —
they are per item, and they are all the verdict used — so this cost nothing. It would have
cost the run if the free-text field had been read as a result.

**Two rules this yields.**
1. If you relabel per item, say so in the grader's instructions. One sentence moved 2 of 2
   to 0 of 6.
2. Never let a judge's free-text summary carry a verdict in a per-item-blinded design. Score
   from the per-item rulings only.

**The un-blinding is the dangerous stage, not the blinding.** A swapped key still completes
the run, still produces plausible numbers, and reports the losing arm as the winner. Nothing
downstream can detect it. So its control asserts that a swapped key produces the *opposite*
answer, not merely that the mapping runs — see `pipeline/evals/harness/selftest_score.py`.

**And a control proves the thing it watches, and nothing else.** That selftest passed
throughout a run in which the harness did invert a result — the inversion was one stage
upstream, in the parser that split the answers.

---

## Three measurements from the first two full builds — 2026-09-01

### 1. Most expectations carry no verdict at all

**MEASURED.** 15 expectations across 30 arm-pairs, read out of every blinded grading on
disk and joined back through its key. **Four carried the verdict — 27%.** Eleven were met
by both arms in every repeat.

Three independent graders had each said a version of this in prose — *"roughly half are
satisfied by reciting a principle rather than obeying it"* — every time found by reading,
one set at a time, after the run. It is computable, and now it is computed
(`pipeline/build/expectation_power.py`).

Two buckets matter, and the second is easier to miss:

- **always-met by both arms** — free. It may still be the right thing to demand; it is
  carrying none of the verdict.
- **always-missed by both** — usually not a high bar but a sentence nobody can act on.

**What it does not establish:** whether an expectation was RIGHT. Only whether it moved.
That distinction needs a person, and that check is still open here.

*Consequence already paid:* a calibration sheet built by uniform sampling put a cell in
front of a human where 0 of 3 expectations had ever discriminated. No answer they could
give would have agreed or disagreed with anything.

### 2. A predicted gap has been refuted every time — 2 of 2

**MEASURED**, n=2, both packages authored by a model. In both, `expected_failure` was
written as *"the baseline does not do X"*, where X is what the skill does. A capable
baseline knew X.

In both builds the real gap turned out to be **shape**: the baseline held the material and
did not produce the artefact.

The form to avoid is a prediction written from the SOLUTION's point of view. The form that
works is what a transcript would show: which step is skipped, which artefact is not
produced, which distinction is not drawn.

**Limit:** n=2, same author, same repo. It establishes the failure mode is real and
repeated, not its rate in general.

### 3. Correctness alone would have discarded a skill that was worth having

**MEASURED**, one build, checked counterfactually rather than asserted. Three questions,
two arms, two repeats: correctness tied at **6 of 6 against 6 of 6** — nothing separated
the arms on being right. The entire delta was on output shape, and one shape win survived
both repeats.

Re-scored with correctness as the only win axis, the same run returns **ITERATE** and the
skill is thrown away as a tie.

This is why a clean baseline must not gate a build (`skill.contract.json`
`acceptance.probe_never_gates`): the value a skill adds may sit entirely in the shape,
which does not exist to be measured until the artefact does.

---

## The library's own test evidence is mostly predicted, not measured — MEASURED 2026-09-01

Found by the skill-builder agent, not by an audit. Handed an incumbent to extend, it opened
`evals.md`, read eleven scenarios each ending **"PASS. Beats baseline."**, and refused to
enter them as results — because the file's own Method section says what they are:

> "judge the likely output of a capable agent WITHOUT the talent against the output WITH
> its method applied."

No run was executed. No output was captured. There is no `evals/evals.json`. The agent
wrote: *"Entering those 11 rows here as result=pass would enter a prediction as a
measurement."*

Measured across the whole library:

| | |
| --- | --- |
| skills | 88 |
| with a runnable `evals/evals.json` | **4** — and all four were built today |
| with `evals.md` prose | 84 |
| whose prose says "judge the likely output" | 41 |
| that say that **and** claim PASS | **28**, carrying **243 claimed passes** |

**So before today, nothing in this library had a runnable eval suite.** Every "PASS. Beats
baseline." predates any measurement and is a prediction of what a run would have shown.

**What this does and does not mean.** It does not mean the skills are bad — a predicted
pass can be right, and the predictions were made by someone who knew the material. It
means the library's evidence is of a different KIND than its own standing rule asks for.
`CLAUDE.md` says: definition of done is built + TESTED + documented + committed, and
*untested → not shipped*. Against that rule, 84 of 88 rest on judgement.

**Why it went unnoticed.** A predicted pass and a measured pass are written identically.
Both say PASS. The distinction lives in a Method section nobody re-reads, and nothing in
the repo ever compared the two — until a gate refused to convert one into the other.

**The consequence for path 2.** `extend_gate` returns UNDECIDABLE for an incumbent with no
stored baseline, which is now known to be nearly all of them. Most of this library cannot
be extended, only rebuilt — and the rebuild is what produces its first real evidence.

## Why a review round repeats: whack-a-mole, not disagreement — MEASURED 2026-09-01

A field in one build took 7 reader rounds and 21 minutes. Read as a count it looks like
diligence; read round over round from the ledger it is not. Four defect terms — *unmarked,
directive, expiry, figure* — recur across three or more of the six rounds that produced findings.
Each round the reader named a different INSTANCE of the same class, the author fixed that
instance, and the reader found the next one.

**The decisive number is the duration trend:** 80, 132, 139, 140, 193, 280, 313 seconds. The last
round took **3.9x the first**. A converging process gets cheaper; this got more expensive every
round. **MEASURED**, n=1 field, durations from the build's cost ledger.

**The remedy is not more review.** When round N names the same class as round N-1, the author
sweeps every instance of that class across the field in one pass before re-reading. Asking the
reader to enumerate all instances instead makes each round dearer rather than fewer — a field
reader sees the artefact once and reports what it finds; exhaustive enumeration is not its job.

**The same habit shows in code checks as an asymptotic creep.** A description ran
1076 → 1068 → 1050 → 1035 → 1030 → 1028 against a cap of 1024: five rounds to move 48 characters
when it started 52 over. Compute the distance to the threshold and cross it once.

**Four verdicts, and flat is not falling.** `converging` needs findings to *fall*, not merely stop
rising — three rounds raising two fresh findings each is `churn` (the field brief is probably
underspecified, so fix the brief rather than the text), and a first implementation that tested
`all(next <= prev)` called that convergence. `recurring-class` is the whack-a-mole case;
`indeterminate` covers fewer than two rounds of findings and is never a pass.

**One methodological trap worth carrying:** comparing rounds by the union of every word in each
round scores near zero even when one finding is restated almost verbatim, because the union is
diluted by everything else the round raised. Compare **finding to finding** and take the strongest
pair. And stem before comparing: an unstemmed run split the class-naming word across two buckets
(*directives* in one round, *a directive* in two others) and reported the class as not recurring —
the word that names a class is exactly the word most likely to appear in both numbers.

In this repo: `pipeline/queries/round_convergence.py`, ledger at `pipeline/ledgers/fields.jsonl`.

## Mutation testing has a cache trap — MEASURED 2026-09-02

Mutating the code under test and re-running its controls is the only way to know a control can
fail. The technique has a failure mode that produces a **wrong verdict rather than an error**, and
it bit twice in one session.

Python caches bytecode and validates the cache on **(mtime, size)**. A mutation that changes
neither survives a restore: the source on disk is correct and the interpreter runs the mutant.
The trigger is more common than it sounds — the mutation that hit this swapped `FAIL` for `PASS`,
**both exactly four characters**, written back inside the same filesystem second. The restored
suite then reported a failure against correct code, and `diff` against the backup said the files
were identical, because they were.

The same mechanism inverts: a restore-then-mutate ordering can report a mutation as *caught* when
the cached original was what actually ran.

**Do this:** `find . -name __pycache__ -type d -exec rm -rf {} +` between the mutation and the
re-run, and again after the restore. **REPEATED**, n=2 occurrences.

**Two smaller lessons from the same session, both about measuring your own measurement:**

- `python3 suite.py | tail -3; echo "EXIT=$?"` reports the exit code of `tail`, not of the suite.
  It printed `EXIT=0` under a failing suite. Redirect to a file and read `$?` from the command
  itself.
- A control that indexes a result (`g[0]`) crashes rather than failing when the mutation empties
  it. A crash still detects the mutation, but it reports as an error rather than as the specific
  control that should have caught it, which is worse when several mutations are run in a loop.
  Guard the index: `check(bool(g) and "…" in g[0], …)`.
