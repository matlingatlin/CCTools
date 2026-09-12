# Ablation · `playbook-admission`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
So does `session-start-hook`. The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

The skill's sharpest content is not the four-part admission test. It is the **prior question in §3**,
which runs *before* the test: **could an emitter, a type, a config file the scaffold writes once, or
a deterministic check have guaranteed this instead?** If yes, prose is the wrong artifact and the
admission test never runs. Five routes, cheapest guarantee first; prompt text is route 5, the only
probabilistic one, and it costs `N tokens × 6 packages × every build`.

The obvious answer is wrong in a specific way. Asked to add a house rule, a competent engineer
evaluates **whether the rule is good** — and a line-count rule is a perfectly good rule. Having
judged it good, they word it. The question they never ask is whether it should be a *prompt sentence
at all*. `docs/mined/ECC-RULES.md` §4 counted fifteen rules in the mined corpus that are lint
configuration typed into prose, plus eleven already implemented as deterministic checks.

The skill's own eval **P1** is this exact case: *"a run that debates the number has already lost."*

## The question

> *We keep getting generated code with 300-line functions and 1200-line files. I want to add a rule
> about this to the standing instructions we send the model on every build. How should I word it?
> Four bullets maximum.*

Names no skill, no file, no term unique to the skill. "How should I word it" points hard toward the
natural wrong answer: word the prose rule.

## Control answer

> Here's a tight version for the standing build instructions:
>
> - **Hard cap:** no function exceeds 50 lines; no file exceeds 300 lines. If a change would cross
>   either limit, split it before continuing.
> - **One responsibility per unit:** if you need "and" to describe what a function or file does,
>   extract until you don't.
> - **Extract, don't inline-grow:** when adding to an existing function/file would push it over the
>   cap, pull out a new function/module for the addition rather than stretching the original.
> - **No deferred cleanup:** never generate oversized code with a plan to "refactor later" — split it
>   in the same pass it's written.

## Treatment answer

> This maps directly onto a case the `playbook-admission` skill already worked out (eval **P1**): a
> line-count rule for functions/files is refused *before* the four admission criteria even run,
> because it fails the prior question in §3 — a linter can guarantee it, so prose is the wrong
> artifact.
>
> **Don't add this to the model's standing instructions.** Instead, have the scaffold package write
> it once into the generated repo's own lint config:
>
> ```json
> // eslint.config.js — written by the scaffold package, inherited by every later package
> {
>   "rules": {
>     "max-lines-per-function": ["error", { "max": 50, "skipBlankLines": true, "skipComments": true }],
>     "max-lines": ["error", { "max": 300, "skipBlankLines": true, "skipComments": true }]
>   }
> }
> ```
>
> Why this beats a prompt bullet:
> - **Cost**: zero tokens per build, forever, vs. ~20-30 tokens × 6 package prompts × every build for
>   a prose sentence.
> - **Guarantee**: total and mechanical (CI fails on violation) vs. probabilistic (a model can just…
>   write a 300-line function anyway).
> - **Applies retroactively**: package 2 onward inherits the config package 1 wrote; a Playbook
>   sentence only ever influences the generation that reads it.
>
> If you still want a residual prompt nudge for cases the linter can't catch pre-generation (e.g.
> steering the model to decompose *before* hitting the limit, not just fail after), that's a
> different, narrower claim — say so and I'll word that specifically rather than restating the
> line-count rule in prose.

## Comparison

| | **Control (no project skills)** | **Treatment (`playbook-admission`)** |
|---|---|---|
| Artifact chosen | prompt prose, four bullets, as asked | **refuses prose**; scaffold-written `eslint.config.js` |
| Prior question asked? | no — went straight to wording | yes, and it is the whole answer |
| The numbers | invented 50 / 300 with no derivation | same numbers, but as lint config where they are enforced |
| Cost reasoning | absent | ~20-30 tokens × 6 packages × every build, versus zero |
| Guarantee reasoning | absent | total and mechanical versus probabilistic |
| Inheritance | absent | package 1 emits, every later package inherits at zero prompt tokens |
| Residue handling | n/a | offers to word **only** the part a linter cannot catch, separately |

**Zero of four control bullets survive contact with the treatment answer.** Bullets 2–4 ("one
responsibility per unit", "extract don't inline-grow", "no deferred cleanup") are additionally the
platitude shape the skill's criteria 2 and 3 exist to refuse: no named consequence, nothing that goes
wrong that can be pointed at.

## Verdict

**Changed the outcome.** The two arms disagree about *what artifact to produce*, which is upstream of
every wording question. The control produced a competent, confident, and — by this skill's rule —
wrong deliverable: four prose bullets shipped into six package prompts on every build, enforcing
probabilistically what a config file guarantees for free. The treatment produced a config file and
priced the alternative.

The mechanism is different, not the phrasing. The control never considered a non-prose artifact.

One honest note in the control's favour: it answered the question it was asked. The treatment
declined the question and answered a better one — which is the behaviour the skill is for, and is
also the behaviour that would be wrong if the prior question had come out the other way.

## Limits of this measurement

n=1 per arm, unblinded, one question, one day. I wrote both the question and the comparison, knowing
what the skill says. A single run of each arm cannot separate the skill's effect from run-to-run
variance, and the question was chosen *because* the skill's own eval P1 predicts this outcome — which
is fair as a test of the rule and unfair as an estimate of how often the rule matters. Nothing here
measures whether the resulting builds are better; it measures which artifact each arm reaches for.
