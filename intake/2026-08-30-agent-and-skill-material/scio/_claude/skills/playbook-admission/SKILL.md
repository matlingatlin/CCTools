---
name: playbook-admission
layer: B
phase: build-time
status: written
description: Decide whether a house rule may be added to the Playbook that ships into every generated build prompt. Use before adding, editing or deleting any line of playbook.yaml, when a mined finding or a review comment is proposed as house-rule content, when someone wants to tell a model in prose something a config file or a type could have guaranteed, or when asking what a house rule costs. Carries a four-part admission test taken verbatim from its source, the prior question that redirects most candidates to a linter or an emitter, a measured token ledger against a stated cap, two wording rules learned from silent failures, and the fixtures without which "does the Playbook work" is an opinion.
---

# playbook-admission

Scio's `Playbook` is the fixed house rules carried by **every package prompt of every build**
(`layerb/playbook.yaml`, rendered by `Playbook.as_prompt_section()`). The as-built record marks it
**`constant`**: a restaurant booking app and a B2B tender platform receive byte-identical rules
(`docs/as-built/LAYER-B-UNDERSTANDING.md` §3).

Two numbers govern everything below, both measured against the working tree on 2026-08-26:

- the rendered Playbook is **668 tokens** (`len(as_prompt_section()) == 2671` chars ÷ 4)
- it enters **each** of a build's six package prompts, so it is ≈ **4,000 tokens per build** before
  a single line is added

**The failure this skill exists to prevent is not a bad rule. It is a good rule in the wrong
place.** A rule a linter can enforce costs tokens on every build and is obeyed only
probabilistically. `docs/mined/ECC-RULES.md` §4 counted the corpus: **fifteen** rules that are lint
configuration typed into prose, and **eleven more that are already deterministic checks in
`builder/validation.py`** — so any prompt sentence restating them is pure token waste.

> **The scaffold package writes the config; it does not describe the rule.**
> `docs/mined/ECC-RULES.md` §4 — *"the highest-leverage idea in this document."*

---

## 1 · Source

**The admission test.** ECC's `rules-distill` skill (265 lines plus two scan scripts), read and
verdicted in `docs/mined/ECC-SKILLS.md` §1.5, 2026-08-26: *"the single most directly reusable text
in the corpus for Layer B."* Four criteria, all required, quoted in §2 as written.

**The wording rules and the fixtures.** `docs/mined/PASS2-GSTACK-TESTS.md` §2.8, §2.4, §4.1 and §5
— a test suite of 374 files read for what it enforces rather than what it claims. Each rule below
carries the observed failure that produced it, including its issue number where the source gave one.

**The pricing.** `docs/mined/ECC-RULES.md` §4 (the fifteen lint rules and the eleven existing
checks); `docs/mined/PASS2-ECC-RULES-COMMANDS.md:274, :662-663` (the ~1,200-token cap, and a
proposal that reached 961). `docs/mined/PASS2-ECC-SKILLS.md:70` states the same cap independently.

**The self-declaration rule.** `docs/mined/OTHERS-MINED.md:772`, from karpathy-skills — *"a rules
document declares its own tradeoff and its own success criterion."*

**This repo.** `layerb/playbook.py`, `layerb/playbook.yaml`, `builder/validation.py` in
`/home/user/hello-world` (read-only); `docs/as-built/LAYER-B-UNDERSTANDING.md`;
`docs/next/LAYER-B-UNDERSTANDING.md` §2.4; `docs/triage/LAYER-BC-TRIAGE.md` §2.1, which holds the
eleven candidates currently queued behind this procedure.

**Progressive disclosure.** The measured ledger, the fifteen lint rules and the eleven existing
checks live in `references/pricing-and-existing-checks.md`. Read it when pricing a candidate; the
procedure below does not require it.

---

## 2 · The admission test — four criteria, all required

Taken verbatim. A candidate failing **any one** is refused, and the refusal is recorded with the
criterion that fired.

| # | Criterion | As written |
|---|---|---|
| 1 | **Appears in 2+ places** | a principle found in one place stays in that place |
| 2 | **Actionable behaviour change** | *"can be written as 'do X' or 'don't do Y' — not 'X is important'"* |
| 3 | **Clear violation risk** | one sentence on what goes wrong if it is ignored |
| 4 | **Not already in the rules** | including the same concept in different words |

Criteria 2 and 3 are the bar that keeps platitudes out, and the mined source gives the worked
contrast:

- *"Prefer readable code"* — **fails 2 and 3.** No behaviour changes; nothing goes wrong that can
  be named.
- *"Views never query the ORM directly; a view that does will bypass the service layer's
  authorisation check"* — **passes both.** A behaviour, and a named consequence.

**Verdicts are four, not two:** `Append` · `Revise` · `New Section` · `New File`. *Revise* is the
one people skip, and it is often right — see §3's replacement rule.

**The method underneath, and it is Scio's own:** *deterministic collection, then judgement.*
Scripts collect the candidate instances exhaustively; one pass cross-reads and produces verdicts.
Do not ask a model which rules matter before something has enumerated which rules exist.

---

## 3 · The prior question — asked before the admission test, not after

**Could a linter, a type, a config file, or the generator have guaranteed this?** If yes, prose is
the wrong artifact and the admission test never runs.

Five routes, cheapest guarantee first. Take the highest one that works.

| Route | Cost per build | Guarantee | Worked example |
|---|---|---|---|
| **1. The emitter** | zero | total — the wrong output is unrepresentable | `bigint` ids, `text` not `varchar(n)`, `timestamptz`, `numeric` for money. Layer B types the schema in `derive.py` before any prompt exists, so a Playbook sentence here would ask a model for something a function already decided (`docs/mined/PASS2-ECC-SKILLS.md:648`) |
| **2. The type** | zero | total, at the boundary | minimum-substance constraints on a contract field, rather than a prose plea against placeholders (`docs/mined/OTHERS-MINED.md:760`) |
| **3. Config the scaffold writes once** | zero, after the first package | total, and inherited | `eslint.config.js`, a strict `tsconfig.json`, coverage thresholds, `onUnhandledRequest: "error"` in the test setup. Package 1 emits them; every later package inherits enforcement at **zero prompt tokens** |
| **4. A deterministic check** | CI time, not tokens | total, with an identifier a gate can key on | `builder/validation.py` already blocks hardcoded credentials, `dangerouslySetInnerHTML`, `eval(`, `${}`-built SQL, and eight more. A regex line in an existing tuple is the cheapest quality work available anywhere |
| **5. Prompt text** | **668 → N tokens × 6 packages × every build** | probabilistic | only what survives routes 1–4 |

**The test for route 4 is not "is it checkable in principle" but "is it checkable without false
positives that would block a correct build."** `docs/mined/ECC-RULES.md` §4 keeps
`.select(` with no `.limit(` at **warning** severity for exactly that reason, and ships the prompt
sentence *as well* — the one legitimate case of doing both.

**The replacement rule.** A candidate that sharpens an existing line **replaces** it. `tabular-nums`
on counters and prices is a measurable instance of a vaguer "stable dimensions" sentence already in
the Playbook, so it costs ≈ 0 net tokens rather than 18. Before pricing any addition, look for the
line it makes redundant.

---

## 4 · If it must be prose — two wording rules, both learned expensively

### 4.1 Prefer an explicit setting to a prohibition

A rule phrased as *"do NOT use X"* inverts itself the day a host default flips, and **nothing
fails.** The observed case: guidance written as *"do NOT use `run_in_background`"* stopped producing
a foreground run when a platform version made background the default; specialists silently launched
in the background and were merged before they completed. The only wording that survived was the
positive setting, `run_in_background: false`
(`docs/mined/PASS2-GSTACK-TESTS.md` §2.8, issues #2440 / #497).

Write the state you want, not the state you forbid. Where the Playbook must forbid — *"never a
blanket allow"* — pair it with the positive form it is the negation of.

### 4.2 Every path interpolated into a prompt is absolute and host-resolved

**The failure mode of a broken path in a prompt is not an error — it is fabrication.** A relative
`scripts/question-registry.ts` never resolved from a user's project directory, the lookup failed
silently, and agents invented identifiers from a fallback: **21 of 21 unregistered in one observed
session** (`docs/mined/PASS2-GSTACK-TESTS.md` §2.8, issue #2489).

Scio's Playbook interpolates no paths today. It names folders (`app/`, `lib/db/`,
`supabase/migrations/`), which are relative on purpose and are the generated repo's own. The rule
binds the moment a rule points at a file **we** own.

---

## 5 · What must exist before a rule counts as enforced

A rule in `playbook.yaml` is a *declaration*. Whether it changes an artifact is a separate
question, and four mechanisms answer it. Without them, *"does the Playbook work"* is an opinion —
which is what the mined source says of its own corpus, and of ours: **we have rules and no seeds**
(`docs/mined/PASS2-GSTACK-TESTS.md` §4.1).

### 5.1 One canonical violating fixture per rule family

Each fixture is *"pre-loaded with one obvious finding the matching skill cannot honestly miss"* —
the operational definition of what the rule is for. Four seeds, one per Playbook section family
(secure-by-default · tests · accessibility · quality), is the minimum.

A rule with no fixture is `unjudged`, in exactly the sense `.claude/skills/testing` §5 gives the
word.

### 5.2 The inert-declaration cross-check

**A fact declared in one place and enforced in another needs a test that the two agree.** The
observed case: a registry demoted a test to `periodic` while the file still self-gated on `gate`,
so the demotion was *"inert for months"* and they kept paying for tests they believed removed
(`docs/mined/PASS2-GSTACK-TESTS.md` §2.4).

**Scio has this shape twice.** The Playbook is declared in `playbook.yaml` and enforced in a build
prompt elsewhere. Acceptance criteria are declared in a package and checked by a gate elsewhere.

Two refinements to copy rather than reinvent:

- **The cross-check's own matcher must be fail-closed.** Enumerate the shapes it accepts and
  **report zero-match files** — a mechanical refactor must not silently drop a rule from the
  invariant that exists to police it.
- **"Reported, not asserted."** Cases the check can *see* but not *arbitrate* are printed as a
  list, not failed and not dropped. A third channel between fail and ignore, and it is what keeps
  the check honest enough to leave switched on.

### 5.3 Exemptions are pinned in both directions

Every exemption carved into a rule needs a test that the rule **still fires just outside it**. An
exemption tested only from the inside is indistinguishable from a deleted rule.

This binds hardest on Layer B's eleven validation rule identifiers (`layerb/validate.py`), because
each is the checkable form of something the Playbook otherwise has to ask for in prose. Pin the
exemption on **evidence**, never on **shape**: *"this table is exempt because it has no owner
column"* is evidence; *"this table is exempt because its name matches `_public`"* is shape, and
shape is what a rename defeats.

### 5.4 Prose-regex invariants — free, and never behavioural coverage

A regex asserting a sentence still appears in a prompt template catches **deletion and drift**,
which is real: §4.1's inverted prohibition is exactly that class. It catches **nothing about
whether the prose works.**

Keep them. Never count them toward whether a rule is enforced. In the mined corpus **76 of 374
files (20%)** were this shape, and the source's own verdict is the one to carry: *"Free, worth
keeping, never behavioural coverage."*

---

## 6 · The Playbook declares its own trade-off and its own success criterion

From karpathy-skills, `docs/mined/OTHERS-MINED.md:772`. A rules document that states neither cannot
be argued with, only obeyed or ignored.

`playbook.yaml` states neither today. Its header says what it is for — *"turns 'build X' into 'build
X the Scio way'"* — and nothing about what that costs or how anyone would know it worked. Two lines
at the top of the file:

- **Trade-off** — every line here is resident in every package prompt of every build, and is obeyed
  probabilistically. It buys consistency across apps that a per-package prompt cannot.
- **Success criterion** — a rule is working when its canonical violating fixture (§5.1) is caught
  and a build with the rule removed produces the violation. Anything else is a claim.

**Write both before the file grows, not after.** They are the sentences that make §2's criterion 4
answerable by someone who did not write the rule.

---

## 7 · The procedure, end to end

1. **Enumerate, do not judge.** Collect every instance of the candidate principle across the
   sources. Criterion 1 is a count, not an impression.
2. **Ask the prior question (§3).** Route 1–4 if any of them work. Most candidates stop here.
3. **Run the four criteria (§2).** Record the verdict and, on a refusal, the criterion that fired.
4. **Look for the line it replaces (§3).** Price the *delta*, not the addition.
5. **Price it.** Tokens × 6 packages × every build, against the ~1,200-token cap. Current spend and
   remaining headroom: `references/pricing-and-existing-checks.md`.
6. **Write it as a setting, not a prohibition (§4).**
7. **Ship the fixture with the rule (§5.1).** Not afterwards.
8. **Add the cross-check if the rule is declared in one place and enforced in another (§5.2).**

A candidate that clears all eight is still an **ADR**, not an edit. It decides what every generated
app contains, in every app, indefinitely — which is the definition `docs/next/SKILLS.md` gives of a
decision that must not hide in a markdown file.

---

## 8 · Limits — what the sources support versus what this assumes

**The four criteria are one team's practice, not a result.** `rules-distill` ships no evaluation
and reports no number. Nothing shows a corpus filtered this way produces better generated apps than
one filtered by taste. What is defensible is narrower and still worth having: the criteria are
*checkable by a second reader*, and refusals become recorded rather than felt.

**The ~1,200-token cap is a stated discipline, not a measured threshold.** `docs/mined/ECC-RULES.md`
§43 introduces it as a cap precisely so headroom does not read as licence. **No experiment in this
repo shows quality degrading past 1,200 tokens of house rules**, and none shows it holding either.
Treat the cap as a budget someone chose, and say so when quoting it.

**The token figures are characters ÷ 4.** `messages.count_tokens` is the correct instrument and was
not available when these were measured. The 668 is stable enough to compare candidates against; do
not act on any margin narrower than 20% without re-measuring.

**The wording rules generalise from one observation each.** 21/21 fabricated identifiers and one
inverted prohibition are real, dated, and attributed to issue numbers — and they are *n = 1* per
rule, from a different codebase, with a different host. The mechanism transfers; the frequency does
not.

**The fixture discipline is untested here.** Scio has no Playbook fixtures at all, so §5.1 is a
proposal with a rationale, not a practice with a result. The honest statement is that we cannot
currently tell a Playbook line that works from one that does not.

**This skill cannot tell you whether a rule is *correct*.** It tells you whether a rule belongs in
prose, what it costs, and what would have to exist for anyone to find out. Correctness is a
security, accessibility or performance question, and the four criteria are silent on all three.

---

## 9 · Eval

Runnable as prompts against this skill. **The reason is the test, not the verdict.**

| # | Case | Expected | What it proves |
|---|---|---|---|
| **P1** | *"Add to the Playbook: functions should be under 50 lines and files under 800."* | **Refused at §3, route 4** — `max-lines-per-function` and `max-lines` are ESLint rules the scaffold config sets once. Never reaches §2 | the prior question runs first. A run that debates the number has already lost |
| **P2** | *"Add: prefer readable, maintainable code."* | **Refused at §2, criteria 2 and 3**, both named. No behaviour changes; no consequence can be stated | the platitude filter, which is the whole reason the criteria were taken |
| **P3** | *"Add: never read `window` or `navigator` at module level."* | **Split.** The greppable half goes to `_UNSAFE_PATTERNS` (route 4); only a residue no grep catches may be prose, and it must be priced | one finding, two artifacts. A run that adds the whole sentence to the Playbook fails |
| **P4** | *"Add: no mutable module-level state in RSC/SSR."* | **Admitted to the ADR queue** — passes all four criteria, and route 4 is genuinely unavailable: it lints, typechecks, builds and passes `_UNSAFE_PATTERNS`. Priced at ~22 tokens, ≈132 per build | the procedure admits things. A skill that refuses everything is not a filter, it is a wall |
| **P5** | *"Add: use `font-variant-numeric: tabular-nums` on counters and prices."* | **`Revise`, not `Append`** — it supersedes the existing vaguer stable-dimensions line. Net cost ≈ 0 | the replacement rule (§3). A run that prices it at +18 tokens has skipped step 4 |
| **P6** | *"Add: do NOT let the model use inline styles."* | Admitted only after rewriting as the positive setting (§4.1), or refused. The prohibition form is the defect | the wording rule fires on our own text, not only on the mined example |
| **P7** | *(negative)* A rule is added with no fixture and no cross-check. | **The rule is `unjudged`**, and saying "the Playbook now covers X" is refused | §5 has teeth or it is decoration |
| **P8** | *"The Playbook is 668 tokens and the cap is 1,200, so we have 532 tokens of room."* | Accepted **only** with the cap's provenance attached: a stated discipline, unmeasured, and the 668 is chars ÷ 4 | §8. A run quoting either number bare fails |

**Pass condition:** P1–P6 reach the stated outcome for the stated reason; P7 and P8 fail closed.

---

## 10 · When this skill is the wrong tool

- **Whether a check should exist at all in `builder/validation.py`** → that is a Layer E gate
  decision. This skill only says the rule does not belong in prose.
- **Whether a validator's *output* is trustworthy** → `.claude/skills/validation-evidence`.
- **Whether a test can fail, or a double is honest** → `.claude/skills/testing`.
- **What the app should look like** → `.claude/skills/app-design`, which owns the design surface
  and is where §1–§4 of it are proposed as Playbook content.
- **Which side of the rule/model boundary a *decision* sits on** → `.claude/skills/architecture` §4.
  This skill assumes that answer and asks the narrower question of artifact.
- **A rule for one app.** The Playbook is `constant` by design. A rule that should apply to a
  booking app and not to a tender platform is not a Playbook rule, and admitting it there is how
  the constant stops being one.
