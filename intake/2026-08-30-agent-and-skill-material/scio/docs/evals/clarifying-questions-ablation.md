# Ablation · `clarifying-questions`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
Every comparison below is skills-minus-`graphify` against `graphify` alone, not against nothing.

## The discriminating rule, and why the obvious answer is wrong

§4: **with 5+ real options, never drop, merge, or silently defer one to fit** the picker's cap.
Split into sequential calls instead — and *"a split chain is never auto-decide-eligible… the user's
option set is sacred."* Above six options, a meta-question first: proceed / narrow / batch.

The obvious answer is to narrow. Every UX instinct — Hick's law, choice overload, "keep it to three
or four" — says a seven-option picker is a design smell and the job is to collapse it. Merging
near-duplicates and routing the tail into *Other* is the textbook move, and it is wrong here for a
reason that is invisible in the output: **a brief showing four options when seven existed looks
exactly like a brief showing four options when four existed.** The dropped three are never
mentioned again, so the failure leaves no trace to notice.

## The question

> *We are building an onboarding wizard. One question has seven legitimate options but our picker
> only shows four, and honestly seven feels like too much to put in front of a user anyway. What is
> the best way to cut it down to four? Four bullets max.*

No skill, file or term from the skill appears. "What is the best way to cut it down" points squarely
at the wrong answer and presupposes that cutting is the task.

## Control answer

> This is a UX/product design question, not something that needs codebase digging — quick answer:
>
> - **Merge near-duplicates**: look for two of the seven that a real user would describe the same
>   way; collapsing them to one option is free simplification, no information lost.
> - **Promote the long tail to "Other"**: keep the 3-4 highest-frequency/highest-signal options as
>   bullets and route the rest into an "Other (tell us more)" free-text or follow-up — you keep
>   coverage without keeping clutter.
> - **Split into two questions**: if the seven cluster into two dimensions (e.g., "what" and "how"),
>   ask two 3-4-option questions in sequence instead of one 7-option question — often clearer than
>   cutting substance.
> - **Data-driven cut**: if you have any usage data from hello-world (check `docs/as-built/` or the
>   graph for this flow), keep the 4 most-selected and fold the rest into "Other" rather than
>   guessing which 3 to drop.
>
> My pick: try the merge first, then "Other" for whatever's left — it's the only option that doesn't
> lose information outright.

## Treatment answer

> Per the `clarifying-questions` skill (§4): with 5+ real options, the rule is **split, never drop** —
> cutting seven down to four silently loses answers nobody will ever see flagged as missing.
>
> - **Don't merge/cut to fit the picker.** A shown four looks identical whether four or seven
>   existed; the dropped three are gone with no trace.
> - **Split into sequential calls**: show the picker once per subset (e.g., 4 then 3, or however you
>   group them), each still respecting the 4-option cap, then run one final call to confirm the
>   assembled choice.
> - **Use Include/Defer/Cut/Hold buckets per split round** so the user — not you — decides which
>   options get demoted, and allow a per-option revise afterward without redoing the whole chain.
> - Since 7 exceeds 6, the skill also says to lead with a meta-question first: proceed with all seven
>   / narrow the field / batch them — let the user choose the compression, rather than you choosing
>   it for them.

## Comparison

| | **Control (no skills)** | **Treatment (`clarifying-questions`)** |
|---|---|---|
| Accepts the premise? | **Yes** — "cut it down" treated as the task | **No** — refuses the premise in the first line |
| Merge near-duplicates | recommended first | explicitly rejected: a merged four is indistinguishable from a real four |
| *Other* / free-text tail | recommended, called "coverage without clutter" | not offered; the tail is options, not clutter |
| Splitting | offered as **one of four** ideas, and only if the options happen to fall on two dimensions | the **rule**, unconditional, regardless of whether the options cluster |
| Reassembly | absent | a final validating call over the assembled set, plus a per-option revise path |
| Who chooses the compression | the builder — "keep the 4 most-selected", "guessing which 3 to drop" | the **user**, via Include/Defer/Cut/Hold and a meta-question at >6 options |
| Failure mode named | "losing information" (generic) | the *invisible* failure: a well-formed four-option brief that silently lost three |
| Final recommendation | merge, then *Other* | never drop; meta-question first |

Three of the control's four bullets are drops in different costumes. Its own closing pick — merge,
then *Other* — is the exact move the rule forbids, and it endorses it on the grounds that it
"doesn't lose information outright", which is the belief the rule exists to correct.

The one genuine overlap is that both mention splitting. But the mechanism differs: the control
offers it as a conditional stylistic alternative ("*if* the seven cluster into two dimensions"),
the treatment as the default with buckets, a validation call and a revise path attached. Same word,
different machine.

## Verdict

**Changed the outcome.** The control took the bait on the premise and on its own summary line; the
treatment inverted the question. This is a case where the skill supplies a rule the model demonstrably
does not hold — general UX instinct actively argues *against* it.

Not measured by this question: the three authority classes, the User Challenge that is never
auto-decided, the one-way door registry, and the brief format. Those are separate rules and this
result says nothing about them.

## Limits of this measurement

n=1 per arm, unblinded, one question, one day. No repeated seeds, so nothing here separates the
skill's effect from run-to-run variance; a single pair cannot. The treatment arm loaded all 27
project skills, not `clarifying-questions` alone, so strictly this measures the corpus firing on
this question — the answer cites `clarifying-questions` by name, which is evidence about which
skill fired but not proof that no other contributed. `graphify` loads in both arms. The control's
stray reference to "hello-world" is an artefact of the scratchpad path and affects nothing in the
comparison.
