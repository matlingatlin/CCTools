---
name: validation-evidence
layer: B, C
phase: build-time
status: written
description: Make a checker return what it examined, so that "found nothing" can never be mistaken for "did not run". Use when a validator, rule set, scan or conformance pass reports clean; when designing what a check returns rather than what it concludes; when a summary or signature view drops bodies, rows or steps; when an empty answer and a broken pipeline would look identical to the caller; or when a limitation is claimed without proof. Carries the one-row-per-examined-pair rule, the planned-count that makes invisible non-execution detectable, the three-way typing of empty against missing against error, and the elision marker that stops a summary from lying by omission.
---

# validation-evidence

Layer B runs **eleven rule identifiers** over every architecture (`layerb/validate.py`: six check
functions, ten error and one warning). Layer C runs **nine** over every plan (`layerc/validate.py`:
seven check functions, one of which can warn). Both return a list of violations and a boolean.

**An empty list is the same object whether nothing was wrong or nothing was checked.** That is the
subject of this skill, and it is why the mined corpus's best single sentence is a sentence about
tables:

> *"The scan's output is a table, not a verdict. One row for every pair … 'The scan is clean'
> without those rows is not a scan you ran."*
> — `docs/mined/OTHERS-MINED.md` §2.3, verdicted *"best single sentence in the eight repos"*

**The division of labour with `.claude/skills/gate-verdicts`.** That skill decides what a gate may
*conclude* — the outcome vocabulary, whether PASS is reachable, whether a score or a verdict, what
the gate says about itself. This one decides what a check must *return* so a conclusion is possible
at all. **Read `gate-verdicts` for the verdict; read this for the rows underneath it.** Where they
touch, this document calls that skill and does not restate it.

---

## 1 · Source

**The evidence table.** superpowers `subagent-driven-development`, read and verdicted in
`docs/mined/OTHERS-MINED.md` §2.3 and row 32 (`:751`), 2026-08-26.

**Exit 0 is not evidence.** `docs/mined/PASS2-GSTACK-TESTS.md` §2.1 — three test files and one
observed number: **only ~16 of 434 files ran, shell exit 0.** 96% of a suite skipped, green. The
companion file *"proves the truncated run is indistinguishable from a green one by exit code
alone."*

**Empty is not failed.** gstack `spec` 1b, `docs/mined/OTHERS-MINED.md:734` — *"'no envelope' ≠
'zero results': a failed pipeline is not an empty one."* The same rule arrived at independently in
task-master (`docs/mined/PASS2-FOUR-REPOS.md` §1.4): *a delta that changes nothing returns a
distinguishable no-op, not an empty regeneration.*

**Claimed limitations need evidence.** gstack preamble, `docs/mined/OTHERS-MINED.md:733`.

**The evidence report shape.** ECC's TDD Evidence Report, `docs/mined/ECC-SKILLS.md:669`.

**The elision marker.** repomix `parseFile.ts:36, :108, :180-213`, read in
`docs/mined/PASS2-FOUR-REPOS.md` §4.2 and row P2-28 (`:653`).

**Not sourced here, deliberately.** The five outcome states, the path-concreteness rule and the
honesty rule (`docs/mined/PASS2-GSTACK-SKILLS.md` §2.9) are carried by
`.claude/skills/gate-verdicts` D2. They are not repeated below.

**This repo.** `layerb/validate.py`, `layerc/validate.py`, `layerc/criteria.py`, `layerc/scripts.py`,
`layerc/plan.py` in `/home/user/hello-world` (read-only);
`docs/as-built/LAYER-B-UNDERSTANDING.md` §4; `docs/as-built/LAYER-C-BUILD-PLAN.md` §6.

---

## 2 · The rule — a checker returns what it examined, not only what it found

### 2.1 One row per checked pair

A checker's output is a **table**: one row per thing it looked at, carrying what it compared
against what, and what it found. The verdict is *derived from* the table; it is not the output.

**Why the shape, and not a discipline.** A model asked *"is this architecture consistent?"* will
answer *"yes"* without checking. A model required to emit one row per interface pair **cannot**. The
table is what converts a claim into work that either happened or visibly did not — and the same
argument holds for a deterministic checker, where the rows are what let a reader see that a rule
found no subjects at all.

For Scio this is concrete and unbuilt. `validate_architecture` returns
`ValidationResult{valid, violations}`. Nothing records which entity–operation pairs
`_check_operations_hit_valid_entities` walked, which relations `_check_relations_resolve` resolved,
or how many there were. **A zero-entity architecture and a fully consistent one produce the same
empty violation list** — and `_check_something_to_build` exists precisely because someone already
hit that, one rule at a time.

The addition is a shape, not an algorithm: alongside `violations`, a
`checked: list[Checked{rule, subject, compared_against, outcome}]`, and —

> **no rows for a rule that declares itself applicable is a failure, not a pass.**

A rule that is genuinely inapplicable says so with a row of its own. *"Not applicable"* recorded and
*"never ran"* silent are the distinction this whole section exists to force.

### 2.2 Three numbers, and one of them must be a plan

`.claude/skills/testing` §3 Q3 already requires **ran / passed / skipped**, parsed from a
machine-readable report rather than a human summary. The mined finding adds the number those three
cannot supply:

> A gate must know **how many units it planned to run**. Without a plan count, *"invisible
> non-execution"* is undetectable.

The reference implementation refuses a zero exit when (1) failure lines were printed, (2) **fewer
units ran than were planned**, or (3) an unhandled error fired between units — and it keeps
**per-origin buffers** for stdout and stderr, because a shared buffer shears a `(fail)` line into
fragments that go uncounted, *"defeating the exit-0-with-failures backstop."*

**Declared lanes, executed-unit count against a planned count, no failure lines. All three.** This
is the parsing half of the same idea as §2.1: a count of subjects, known in advance, is the cheapest
possible evidence table.

### 2.3 Empty, missing and broken are three types

Three outcomes that must be distinguishable **in the return type**, never collapsed:

| Outcome | Means | Never rendered as |
|---|---|---|
| **a result with zero items** | the check ran and found nothing | a failure |
| **no result** | the check did not run, could not run, or produced nothing parseable | zero items |
| **an error** | the check ran and broke | either of the above |

`null` versus `[]` is the whole mechanism and it is free. Two independent repos in the mined corpus
state it: *"'no envelope' ≠ 'zero results'"*, and *a delta that changes nothing is a no-op with a
distinguishable return.*

**Where Scio already gets this right, and it is worth naming.** `layerc/scripts.py` refuses rather
than fabricating: no create operation, no screen to drive, or no identity to isolate by ⇒ **no
script**, and the criterion stays `Observability.unsupported` — recorded, unjudged, and never
failing a build. That is this rule implemented, and it is the model for the rest of the layer.

### 2.4 A claimed limitation carries its evidence

When a check reports that it *could not* do something, one of three things is attached or the claim
is an assertion wearing a result's clothes:

1. the **verbatim error**, quoted;
2. a **documented statement** that the thing is impossible, cited;
3. a **live probe** that was run, and its result.

*"It doesn't support that"* with none of the three is a guess. This is the input side of
`gate-verdicts` D2's *"'I don't want to check' is not unreachable"* — that skill governs how the
resulting state is named; this one governs what has to be in hand before it is claimed.

---

## 3 · The report a person reads

Layer C writes acceptance criteria; Layer E runs gates. **Nothing renders the join.** The mined
shape is five columns and it is enough:

| guarantee | test | type | result | evidence command |
|---|---|---|---|---|

The **evidence command** column is the load-bearing one: a reader can re-run the row. A report whose
rows cannot be re-run is a summary, and §2.1 has already said what a summary is worth.

This maps onto machinery that exists rather than needing a new model. A criterion's `produced_by`
names the file that would make it true and `observed_by` names the channel that can see it
(`layerc/criteria.py:67`); the result column is the gate's outcome, whose vocabulary is
`gate-verdicts` D2's decision, not this skill's. **It is a rendering.**

Two numbers make it worth building today. On the canonical booking spec, `cover()` reports **8 of 27
criteria unsupported** and **zero observed by interaction** — thirty per cent of every plan's "done
when" list observed by nobody, invisible because nothing renders the join
(`docs/next/LAYER-C-BUILD-PLAN.md` §1.1).

---

## 4 · A summary view marks what it removed

Distinct from §2, and easy to miss because it is not a checker at all.

> **A signature-only view that does not mark its elisions is a lie to the reader** — and the reader
> here is a model, which will otherwise infer that a class has no methods between two signatures.

The reference implementation is one constant, `⋮----`, emitted at every discarded body. And the
refinement that makes it informative: **adjacent kept items are merged**, so the marker means
*"something was removed here"* rather than *"a new chunk starts"*. Without the merge it appears
between every consecutive pair and carries no information.

**Scio has two signature views and neither marks anything.** `PackageInterface` (`plan.py:47`) —
*"names and shapes, not implementations"* — is rendered into every dependent package's contract
prompt, and Layer D's catalog entries are the same shape. The rule:

- **one sentinel token at every discarded body**, in the *rendered* form, not only in the model;
- **merge adjacent kept items**, so the sentinel means removal;
- an item omitted for a reason other than brevity — filtered, unresolvable, out of scope — carries
  that reason. *"Absent"* and *"elided"* are §2.3's distinction again, one level down.

---

## 5 · Limits — what the sources support versus what this assumes

**Every number here is from someone else's repository.** 16-of-434 files running under exit 0 is a
real, dated observation in one test runner. **It has not been reproduced in Scio and it is not a
base rate.** The mechanism transfers; the frequency does not, and quoting the number without its
origin is selling something this repo did not earn.

**Evidence tables cost, and the cost is unmeasured.** One row per checked pair on a six-package plan
is small; on a twelve-entity architecture with relations it is not obviously so. Nothing here
establishes a break-even. Note the asymmetry that makes the rule cheap where Scio needs it most:
Layer B and Layer C both validate **deterministically, in process**, so their rows cost memory and
log volume, not model tokens. The same rule applied to a model-run scan is a much more expensive
trade and should be argued separately.

**The elision rule assumes the reader infers from adjacency.** That is the stated reason and it is
plausible. It is not measured, and no experiment here shows a contract prompt with elision markers
produces better code than one without.

**The three-way typing is a design claim, not a finding.** Two repos independently doing it is
convergent practice, which is weaker than a result and stronger than one opinion. Say which.

**This skill cannot tell you whether a check is *correct*.** It governs what a check returns and how
absence is typed. A checker that reports every row it examined while checking the wrong thing passes
every rule in this document.

**And the largest limit: none of this is enforced anywhere yet.** Layer C's nine rules already run
on every build and **nothing reads the result** — `builder/pipeline.py` goes from `run_layer_c` to
`save_plan` to the build, and the API's response type does not model the field
(`docs/as-built/LAYER-C-BUILD-PLAN.md` §6). Better rows underneath a report nobody consumes is a
smaller improvement than it looks. Whether that validation should gate is
`docs/next/LAYER-C-BUILD-PLAN.md` §3.1's ADR, not this skill's.

---

## 6 · Eval

| # | Case | Expected | What it proves |
|---|---|---|---|
| **V1** | A validator returns `violations: []` and the run reports *"the architecture is consistent."* | **Refused.** The result must name how many subjects each applicable rule examined. Zero rows for an applicable rule is a failure | §2.1. The single most likely thing to wave through |
| **V2** | A test gate reports success on exit code 0. | **Not evidence** until declared lanes, executed-unit count against a *planned* count, and absence of failure lines are all present | §2.2. A run satisfied by ran/passed/skipped alone has missed the plan count |
| **V3** | A retrieval step returns nothing and the caller renders *"0 results found."* | **Refused** unless the return type distinguishes *no envelope* from *zero results* | §2.3 |
| **V4** | A re-plan produces no changes and returns `[]`. | **Refused.** A no-op returns a distinguishable value, not an empty regeneration | §2.3, and it is the same rule the plan delta needs |
| **V5** | A check reports *"the framework doesn't support verifying this."* | **Refused** unless a verbatim error, a cited statement, or a probe result is attached. Naming the resulting state is `gate-verdicts`' job, not this skill's | §2.4, and the boundary between the two skills |
| **V6** | A `PackageInterface` renders `tables: booking` with three method bodies dropped and no marker. | **Refused.** One sentinel per discarded body, merged across adjacent kept items | §4 |
| **V7** | Asked what the acceptance criteria for the booking app achieved. | A five-column report whose rows can be re-run — not a pass count. On the canonical spec it must surface the 8-of-27 unsupported and the zero interaction criteria | §3. A run that reports a percentage fails |
| **V8** | *(negative)* *"96% of a suite can be skipped under exit 0 — that's the rate we should expect."* | **Refused.** One observation in one runner, not a base rate | §5. A skill that lends its sources' numbers to our claims has stopped being trustworthy |

**Pass condition:** V1–V7 reach the stated outcome for the stated reason; V8 fails closed.

---

## 7 · When this skill is the wrong tool

- **What a gate may conclude** — the outcome vocabulary, whether PASS is reachable, score versus
  verdict, what a gate declares about itself → `.claude/skills/gate-verdicts`. **Do not restate its
  five states here.**
- **Can this test fail? Is this double honest? Is a green run evidence?** →
  `.claude/skills/testing`, which owns the test surface and the `unjudged` vocabulary this skill
  borrows.
- **Should this rule be prose or a linter, and what does it cost?** →
  `.claude/skills/playbook-admission`.
- **How a criterion is *worded*** → `.claude/skills/ears-requirements` §6. This skill governs what
  its check returns, not its sentence.
- **Should Layer C's validation gate the build, and what does a user see when a plan is invalid?**
  → an ADR. `docs/next/LAYER-C-BUILD-PLAN.md` §3.1 states it as a product decision.
- **Which side of the rule/model boundary a check belongs on** → `.claude/skills/architecture` §4.
