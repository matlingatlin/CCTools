---
name: gate-verdicts
layer: E
phase: build-time
status: written
description: Decide what a gate is allowed to report and when a pass is reachable at all. Use when writing or reviewing anything that grades output - a build gate, a validation agent, a critique, a reviewer, a checklist, a linter that decides whether work is done. Use when a check could not run, when a tool returns empty or untagged output, when someone proposes a boolean pass or fail, when a number is about to be attached to a judgement, when deciding whether a gate is the real enforcement point or only a convenience, and when a status has to say what nobody actually verified. Also use when a report pads itself with things it checked but did not change, when a reviewer is about to be handed the whole build transcript, when an absent reviewer is about to be counted as agreement, or when a finding is emitted without quoting the line that caused it.
---

# gate-verdicts

A gate that cannot verify something and says PASS is worse than no gate, because the PASS is
consumed downstream as evidence. Every gate in a generated-code pipeline will eventually receive
an empty string, a timeout, an untagged body or a shape it did not expect, and **the failure mode
of every one of them is a silent PASS**.

This skill is the five decisions a gate has to answer before it returns anything. It does not
decide *which* gates exist or *what* they check — that is architecture, and it belongs in an ADR.

---

## 1 · Source

Not a paper. Twenty-five findings mined from eight external repositories on **2026-08-26** and
triaged in `docs/triage/LAYER-E-TRIAGE.md`, plus this repository's own verified defects.

| Mechanism | Where it was read |
|---|---|
| Fail-closed verdict: five ordered checks, no default branch | `docs/mined/PASS2-GSTACK-SKILLS.md:83` (`codex`) |
| Five outcome states, path-concreteness and the honesty rule | `docs/mined/PASS2-GSTACK-SKILLS.md:199` (`review`) |
| Pre-emit quote gate | `docs/mined/PASS2-GSTACK-SKILLS.md:221` (`review`) |
| Score caps — a deterministic ceiling over a judgement score | `docs/mined/PASS2-ECC-SKILLS.md:369` (`production-audit`) |
| Score only where a gradient is needed | `docs/mined/PASS2-ECC-RULES-COMMANDS.md:697` |
| *"Convenience flow, not a safety mechanism"* | `docs/mined/PASS2-GSTACK-SKILLS.md:129` (`ios-clean`) |
| Fail-closed polarity: *"a boundary that fails open is not a boundary"* | `docs/mined/PASS2-GSTACK-SKILLS.md:108` (`freeze`) |
| Reviewer sees the artefact and the question, never the transcript | `docs/mined/PASS2-ECC-SKILLS.md:428` (`council`) |
| Error contract per gate | `docs/mined/PASS2-ECC-SKILLS.md:443` (`agent-harness-construction`) |
| *What must be true to say this* as a status column | `docs/mined/PASS2-ECC-SKILLS.md:669` |
| Degraded run carries its own disclosure | `docs/mined/PASS2-GSTACK-SKILLS.md:238`, `PASS2-FOUR-REPOS.md:545` |

**Our own instances, verified at source** (`docs/next/LAYER-E-BUILD.md` §1.1, §2.4):
`check_tests_present` matching the substring `test`, so `app/latest/page.tsx` satisfies it
(`validation.py:132`); `checks_passed` computed, typed, transmitted and shown nowhere; the two
interaction gates opt-in behind `SCIO_VERIFY_DATA` with **0** `interaction` criteria to check.

---

## 2 · The five decisions

Answer them in this order. Each is checkable by reading the gate's code; none is a judgement call.

### D1 · Is PASS reachable, and only through the last check?

Write the checks as an **ordered list where the first match wins, with no default branch**. PASS is
the last entry and nothing falls through to it.

Enumerate the states in which the gate cannot know. At minimum: the process exited non-zero
(including a timeout), the output was empty or whitespace, the output was truncated, the output
carries none of the markers the gate greps for. **All of them are FAIL, and all of them are
reported as a verification failure, not as a finding count.**

> *"No `[P1]` substring and no critical findings are different claims — never infer PASS from an
> untagged body."*

The same polarity governs boundaries: a payload the check cannot parse is DENIED. **A boundary
that fails open is not a boundary.** → `references/fail-closed.md`

### D2 · What vocabulary does it return?

Not a boolean. A boolean cannot say *the gate could not run*, and that is the state that matters.
Use the outcome set the artefact actually admits, and make "nobody looked" a value in it rather
than an absence. This repository already has the vocabulary in types — `passed / needs_look /
failed / blocked`, `Remainder`, `unjudged` — and the rule is that **`unjudged` never rounds up.**

Two rules make the vocabulary bite rather than decorate: a criterion naming a concrete path must
be decided by testing that path (*"I don't want to check" is not unreachable*), and code that
*handles* a deliverable is not the deliverable. → `references/outcomes.md`

### D3 · A number, or a verdict?

**Use a score only where a gradient is needed — convergence, ranking, "is this getting better".
Use a verdict plus a checklist for a decision.** A score attached to a decision invites arithmetic
nobody can audit.

Where a score does exist beside deterministic checks, the deterministic checks set a **cap** the
judgement may not exceed. Binary conditions establish a ceiling; the score may only move below it.
That is the arithmetic of the rule that judgement may add an evidence channel and may never
overrule a deterministic one. → `references/scores-and-caps.md`

### D4 · What evidence must travel with the verdict?

- **A finding quotes the line that caused it** — file, line, and the verbatim text. If it cannot,
  the finding is unverified and is suppressed or demoted. *Inventing confidence to route around
  this defeats the gate.*
- **An agent's success report is not evidence.** The claim is "completed"; the evidence is the
  diff, the artefact, the row in the database. Verify the artefact the agent produced.
- **A check runs on the bytes that travel**, not on an earlier copy of them.
- **Low confidence is labelled and demoted, never deleted.**
- **A missing voice is N/A, never agreement.** Two independent gates agreeing may raise confidence
  explicitly; an absent one never counts as consensus.
- **The status carries a *what must be true to say this* column.** *"Do not treat 'present in
  config' as 'working'"* — which is `check_tests_present` written as a rule.

### D5 · What does the gate say about itself?

Four declarations, each one line, each in the gate's own file:

1. **Enforcement point or not.** Either *"this is the enforcement point"* or *"the enforcement
   point is X"*. Ambiguity here is how a guardrail becomes a decoration.
2. **Non-scope.** What it does *not* touch, stated positively.
3. **Its error contract** — for every failure path: a root-cause hint, a safe retry instruction,
   and an explicit stop condition. A gate with no stop condition is why the stop condition ends up
   hard-coded somewhere else as a pass count.
4. **A suppression list**, shipped beside the checklist, or the checklist is ignored within a
   month. An entry that is never allowed to be suppressed is exempted **by name**.

And two rules about the report itself: **omit principles you checked but did not change** — a
report padded with no-ops trains its reader to skim; and **a degraded run carries its own
disclosure into its output**, on the same line as the result, never only in a log.
→ `references/gate-self-declaration.md`

---

## 3 · Limits — what the sources show, versus what we would be assuming

| Claim | Status |
|---|---|
| These are conventions in working repositories, read at source, quotable | Supported. Every row in §1 names a file and a line in `docs/mined/` |
| These conventions **reduce** false passes | **Not measured.** Not one of the eight repositories reports a before/after on any of them. The one self-measurement in the corpus (`gateguard`, +2.25 on a 10-point scale) is n=2, self-run and unblinded, and is worth nothing as a number |
| Our own defects are real | Supported at file and line in `docs/next/LAYER-E-BUILD.md` §1.1, which cites `/home/user/hello-world` |
| The five outcome states are the right five | **Ours to decide.** `review`'s set (DONE / PARTIAL / NOT DONE / CHANGED / UNVERIFIABLE) is one repository's answer. Scio's existing set is different and already in types |

**Four things this skill deliberately does not decide**, because each is an architecture decision
and belongs in an ADR (see `docs/triage/LAYER-E-TRIAGE.md`):

1. **Which gates exist and in what order.** Our order is argued at `loop.py:16` and independently
   supported by Lin et al. (ISSTA 2026); this skill says *do not reorder without answering that
   argument*, not what the order should be.
2. **Whether a gate runs by default.** `SCIO_VERIFY_DATA` is a product call with a measurable cost
   (`docs/next/LAYER-E-BUILD.md` §3.2).
3. **Whether checks may be pruned on measured hit rate.** Needs the measurement first.
4. **What the outcome enum's members are.** Changing a status vocabulary changes the wire format.

**The honesty rule:** this skill justifies the *shape* of a verdict — ordered checks, enumerated
unverifiable states, a vocabulary wider than two, a cap on judgement, evidence attached. It does
not justify a claim that a gate shaped this way catches more defects, because nobody measured that.

---

## 4 · Eval

Each case is a gate to construct and a property to assert. None needs a model.

**E1 · No default branch.** Give the gate a non-zero exit, an empty body, a whitespace body, and a
body with no severity markers. Assert four FAILs, each reported as a verification failure. A PASS
on any of them, or a "0 findings" phrasing on the untagged one, fails.

**E2 · PASS is last.** Read the gate's control flow. Assert exactly one path reaches PASS and it is
the final check. An `else: return PASS`, or a default parameter that is PASS, fails.

**E3 · A boolean does not carry "could not run".** Assert the return type admits at least one value
meaning *nobody looked*, and that it is not the same value as *looked and found nothing*.

**E4 · The cap binds.** Set every deterministic condition to its failing value and let the judgement
return its maximum. Assert the reported score is at or below the cap. A judgement that can exceed a
failed deterministic check fails.

**E5 · A finding without a quote is demoted.** Emit a finding with no `file:line` and no verbatim
text. Assert it is suppressed or demoted, and that no path lets a caller raise its confidence to
compensate.

**E6 · The substring test.** Feed the gate a path or a body that satisfies its check *lexically* but
not semantically — `app/latest/page.tsx` against a test-presence check is the live example. Assert
it fails. This is `validation.py:132` as an eval.

**E7 · Absence is not agreement.** Run a consensus gate with one reviewer missing. Assert the result
is N/A for that voice and that overall confidence did not rise.

**E8 · Self-declaration present.** Grep the gate's file for its enforcement-point line, its
non-scope list, and a stop condition on every error path. A missing one fails; this is a lint, not
a review.

**E9 · Degraded runs disclose.** Force a degraded path (a tool absent, a timeout, a partial parse).
Assert the disclosure appears in the *result*, not only in a log line.

---

## 5 · When this skill is the wrong tool

- **Deciding what to check.** That is Layer C's acceptance criteria and Layer B's Playbook.
- **Deciding whether a gate is worth its cost.** That needs a measurement, and then an ADR.
- **Test design.** `testing` owns whether a green run is evidence; this skill owns what the gate
  does with the answer.
- **Stopping a loop.** `build-loop-stops` owns that; this skill owns the verdict the loop reads.

---

*Written 2026-08-26 from `docs/mined/` read at source. No mechanism here has been measured on Scio.
Code claims trace to `/home/user/hello-world` through `docs/next/LAYER-E-BUILD.md` §1–§3.*
