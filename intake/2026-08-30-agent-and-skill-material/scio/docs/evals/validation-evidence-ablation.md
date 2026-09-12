# Ablation · `validation-evidence`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
So does `session-start-hook`. The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

**An empty violation list is the same object whether nothing was wrong or nothing was checked.**
`validate_architecture` returns `ValidationResult{valid, violations}` and records nothing about which
entity–operation pairs it walked or how many there were, so a zero-entity architecture and a fully
consistent one produce byte-identical output. The skill's rule: a checker returns a **table** — one
row per thing examined — and the verdict is derived from the table, not returned instead of it. Its
teeth are in one sentence: **no rows for a rule that declares itself applicable is a failure, not a
pass.** A genuinely inapplicable rule says so with a row of its own; *"not applicable" recorded* and
*"never ran" silent* are different states.

The obvious answer is wrong because an empty list **looks like** good news. Asked to enrich a passing
log line, the instinct is to make it *auditable* — add identity, timing, severity — all of which
answer "what run was this?" and none of which answer "did anything get examined?". Ablation 02 showed
the model fails closed on an empty *stdout*, where emptiness is visibly suspicious. A structured
`violations: []` with `valid: true` is the harder case: it is a well-formed success object, and it is
the one this skill says to distrust.

## The question

> *We run a set of rules over each project's config before we build it. Right now the build log just
> prints 'validation passed' when nothing comes back. I want to make that line more useful. What
> should it include? Four bullets maximum.*

Deliberately **not** phrased as "is an empty result a pass?" — that shape cues scepticism and is what
made ablation 02 unmeasurable. This is a log-enrichment design question, and it points toward
metadata.

## Control answer

> This is a quick design question, not something to build yet — here's my take:
>
> - **Rule count and names checked** — e.g. "12 rules evaluated" or the list of rule IDs, so a passing
>   build still shows what was actually verified.
> - **Config identity** — which project/config version (id, hash, or path) the validation ran against,
>   so the log line is traceable to a specific build.
> - **Timing** — how long validation took, useful for spotting a rule that's silently degrading.
> - **Severity breakdown** — counts of warnings/info-level notices that passed threshold but aren't
>   strictly failures (if your rules support non-blocking severities), so "passed" doesn't hide
>   near-misses.
>
> The rule-count-and-names bullet is the one I'd prioritize if you can only do one — it's what turns
> "trust me" into something someone could audit.

## Treatment answer

> Per `validation-evidence` §2.1–2.2, "validation passed" with nothing behind it is indistinguishable
> from "validation didn't run." The line should instead include:
>
> - **Which rules were applicable and how many subjects each examined** (e.g. "11 rules checked, 6
>   entities, 14 relations") — zero rows for a rule that declares itself applicable is a failure, not
>   a pass, so the count is what proves the rule actually ran.
> - **Any rule that was inapplicable, named as such** — distinguish "not applicable" (recorded) from
>   "never ran" (silent), rather than folding both into silence.
> - **The rule identifiers or names actually run**, not just a count — so a reader can tell *which*
>   eleven (Layer B) or nine (Layer C) rules this build hit, since a checker that examines the wrong
>   thing can still print "passed."
> - **A machine-checkable form** (e.g. `checked: [...]` alongside `violations: []`) so the log line is
>   a rendering of real rows, not an assertion — the same shape the skill flags Layer C as already
>   computing today and nothing downstream reads.

## Comparison

| | **Control (no project skills)** | **Treatment (`validation-evidence`)** |
|---|---|---|
| Underlying question the line answers | *"which run was this, and was it clean?"* — provenance | *"did anything actually get examined?"* — non-execution detection |
| Rule names / count | yes — bullet 1, and named as its top pick | yes — bullet 3, but explicitly *"not just a count"* |
| **Subjects examined per rule** | **absent** | the load-bearing bullet: 6 entities, 14 relations |
| Zero-subject rule | not considered | **a failure, not a pass** |
| Inapplicable vs never-ran | not distinguished | distinguished, and each recorded |
| Return-type change | none — a richer log string | `checked: [...]` alongside `violations: []` |
| Timing / config hash / severity split | three of four bullets | none — orthogonal to whether the check ran |
| Framing of "passed" | trustworthy, to be made auditable | **indistinguishable from "didn't run"** until rows exist |

**One bullet of four overlaps**, and only partly. Both arms want the rule names in the line. The
control wants them so a human can audit *which run happened*; the treatment wants them because a
checker examining the wrong thing still prints "passed" — the same artifact for a different reason,
and the treatment then adds the subject counts the control has no concept of.

The control's other three bullets are metadata about the run. None of them would change if every rule
silently examined zero subjects, which is the exact failure the skill exists to make visible.

## Verdict

**Changed the outcome**, with a partial overlap that should be recorded rather than smoothed over.

The control produced a good log line for a different problem. Its bullets make a passing build
*traceable*; they do not make a non-executing rule *detectable*. The treatment reframed the log line
as a rendering of an evidence table and made zero-subject execution a failure state — a change to the
return type, not to the string.

It is worth being precise about what the treatment did **not** supply here. §2.2's planned-count —
*"a gate must know how many units it planned to run"* — appears only implicitly as counts, and §2.3's
three-way typing of empty against missing against error was not raised at all. On a four-bullet
budget the treatment spent everything on §2.1. A longer answer might have reached the rest, or might
not have; this run does not show.

## Limits of this measurement

n=1 per arm, unblinded, one question. I wrote the question knowing the rule it was aimed at and wrote
the comparison knowing which arm was which. One run per arm cannot distinguish a skill effect from
run-to-run variance, and the partial overlap on bullet 1 is exactly the kind of result a second pair
of runs might widen or erase. Nothing here shows that a build using such a log line catches more real
defects — only that the two arms reach for different objects when asked the same question.
