# Ablation · `gate-verdicts`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

Ablation 02 measured this skill and found nothing, because its question — *is empty gate output a
pass?* — is one the model answers correctly from instinct. This run targets the skill's structural
substance instead: **ordered checks with no default branch**, and the rule that *"no `[P1]`
substring" and "no critical findings" are different claims*.

**Confound, stated once and true of every file in this series:** `graphify` is installed at account
level and loads in **both** arms (as do `session-start-hook` and `synced`). The arms differ only by
the 27 project skills in `/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

`gate-verdicts` D1: write a gate's checks as an **ordered list where the first match wins, with no
default branch**; PASS is the last entry and nothing falls through to it. Every state in which the
gate cannot know — non-zero exit, empty body, truncated body, a body carrying none of the markers
it greps for — is FAIL, **reported as a verification failure, not as a finding count**. D3 adds:
a decision takes a verdict, not a number. D4 adds: a finding that cannot quote its `file:line` is
demoted.

The obvious answer is `if "[P1]" in output: fail else: pass` — a boolean with a default-pass branch,
usually improved by adding a count threshold for the lower severities. Both moves are wrong in the
skill's terms: the default branch is how an unparseable body becomes green, and the threshold
attaches arithmetic to a decision.

## The question

> Our code review step prints its findings into a text blob with severity tags like [P1]. We're
> wiring it into CI so it can block a merge. What should the pass rule be? Be specific, four
> bullets maximum.

No skill, file or term unique to the skill is named. "What should the pass rule be" points at the
substring test.

## Control answer

Verbatim.

> - **Block on any [P1] finding**: zero tolerance — one or more P1s in the output fails the check.
> - **Allow [P2]/[P3] through with a count threshold** (e.g. fail if P2 count > N), so minor findings don't stall merges but can't accumulate silently either — start N at 0 and loosen only if false-positive rate demands it.
> - **Fail closed on absence of a parseable severity tag** — if the blob doesn't contain the expected `[P#]` markers at all (empty output, crashed run, malformed format), treat it as a failure, not a pass, since silence shouldn't be mistaken for a clean review.
> - **Fail closed on the reviewer step itself erroring or timing out** — a non-zero exit or timeout from the review tool is a gate failure, not a skip.

## Treatment answer

Verbatim.

> Applying the gate's D1/D2 rules to a text-blob output:
>
> - **Fail on any `[P1]` tag, no other tagged severity blocks the merge.** Grep for the exact markers you emit (`[P1]`, `[P2]`, …); this is a decision, not a score, so don't sum or weight severities.
> - **Fail closed on anything that isn't a clean, taggable body**: non-zero exit, empty/whitespace output, truncated output, or output with zero recognized severity tags at all. Report each as a *verification failure*, distinct from "0 P1s found" — an untagged blob is not evidence of a clean pass.
> - **PASS is reached only by the last check in an ordered list** (no `[P1]` found *and* the body parsed cleanly) — never a default/`else` branch, so a shape you didn't anticipate can't fall through to green.
> - **Every P1 finding must carry `file:line` + verbatim quoted text to count** — a P1 without a locatable quote is demoted (doesn't block) rather than trusted at face value, since an unverifiable finding is exactly the shape that should not silently pass either.

The treatment names the skill's own decision numbers unprompted ("the gate's D1/D2 rules"), so the
skill fired from context.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Block on `[P1]` | yes | yes |
| Empty / crashed / malformed output is FAIL | **yes** — "silence shouldn't be mistaken for a clean review" | yes |
| Non-zero exit or timeout is FAIL, not skip | **yes** | yes |
| Truncated output enumerated as its own unknowable state | no | yes |
| *Verification failure* reported as distinct from "0 findings" | no — fails, but does not separate the two claims | **yes**, stated as the distinction |
| PASS reachable only through the last check, **no default branch** | absent | **yes**, as a control-flow requirement |
| Verdict, not a score | **inverted** — proposes a P2 count threshold `N` | explicit: "this is a decision, not a score, so don't sum or weight severities" |
| Finding must quote `file:line` or be demoted | absent | yes |

**Two of four control bullets converge on the treatment's mechanism, not merely its conclusion.**
The fail-closed-on-empty instinct is the model's own, exactly as ablation 02 found — and it reaches
further than ablation 02 credited, since the control also covers a *malformed* body with no markers.

## Verdict

**Changed the outcome, in part.** Three mechanisms appear only with the skill: the ordered-checks
control-flow requirement with no default branch, the *verification failure* vocabulary that keeps
"could not tell" separate from "found nothing", and the quote-or-demote rule on findings. One
control bullet runs the other way — a count threshold on P2, which D3 forbids for a decision.

What it did **not** show is that the skill supplies fail-closed polarity. The control had that, and
had it in the untagged case too. If the skill is justified, it is justified by the structure it
imposes on the check list and by what travels with a finding, not by the instinct to distrust
silence.

## Limits of this measurement

n=1 per arm, one question, unblinded — I wrote the question knowing the rule, ran both arms, and
judged the difference. No mutation of the question, no repeated sampling, no second grader. A
single re-run could move the P2-threshold bullet, which is the one carrying most of the verdict's
weight. `graphify` loads in both arms and is not controlled for.
