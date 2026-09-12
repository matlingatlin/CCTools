# Ablation · `ontoagent-elicitation`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.

## The discriminating rule, and why the obvious answer is wrong

§2.2: the published method has four stages — ParseUser, ScoreOnto, ReRankOnto, **GatePrune** — and
Scio adopts the scoring **additively only**. A relevance score may **turn a conditional question on.
It may never turn one off**, and it may never re-order the core fields. GatePrune is *"refused
outright"*: a model deciding a required concern is irrelevant is the precise failure the gate exists
to prevent. §2.4c adds the corollary — the ratchet is one-way; a mid-session signal may upgrade the
path and **nothing downgrades**, because a downgrade is *"GatePrune arriving through a side door."*

The obvious answer is the one the question asks for: score relevance, prune what does not apply,
shorten the interview. That is what the source paper does, it is what any product person facing a
drop-out rate would build, and it is what the skill exists to refuse in writing. The asymmetry that
justifies the refusal is the load-bearing part: *a wrong signal costs a question the user can wave
away, while a missed one costs a whole area of the app.*

## The question

> *Our setup interview asks every user the same fixed list of questions and it is too long — people
> drop out. We want to have the model work out which questions actually matter for the kind of app
> someone is describing, and skip the ones that do not apply. How should we build that? Four bullets
> max.*

No skill, file or unique term. The premise — *skip the ones that do not apply* — is the wrong answer,
handed over as a settled requirement.

## Control answer

Verbatim:

> This is exploratory — quick recommendation, not implementation:
>
> - **Model the interview as a dependency graph, not a script**: each question has a "relevance
>   predicate" (e.g. "asks about payments" → skip auth-provider questions only if no user accounts
>   are needed). Derive relevance dynamically from the user's free-text app description rather than
>   hardcoding branches per app type — the categories won't stay fixed.
> - **Two-pass, not one**: pass 1 has the model classify the description against the fixed question
>   bank (which questions are load-bearing for *this* app, which are moot) before the interview
>   starts; pass 2 lets it re-prune after each answer, since early answers often resolve later
>   questions.
> - **Always show why a question was dropped**, not just skip it silently — a one-line "skipped: no
>   user accounts needed" builds trust and gives the user an easy override if the model guessed
>   wrong.
> - **Log every skip decision with the description that triggered it** — this becomes your eval set
>   for whether the pruning is actually accurate, and it's the natural place to catch systematic
>   misses (question skipped that later turned out to matter) instead of finding out after the app is
>   built.
>
> Worth writing this as an ADR before building, since it changes the interview from deterministic to
> model-driven — a real architectural choice per your CLAUDE.md conventions.

## Treatment answer

Verbatim:

> Build it as an additive layer on top of the fixed interview, not a replacement for it:
>
> - **Keep a deterministic core, add a scoring layer on top.** Classify the app kind first (announce
>   it, let the user correct it), then use that classification only to *turn on* extra conditional
>   questions relevant to that kind — never to drop or reorder the core fields. A model deciding a
>   required question is irrelevant is the exact failure mode to avoid; letting it add relevant ones
>   is safe because the cost of a wrong guess is one skippable question, not a missing requirement.
>
> - **Never let the model skip a core field, only skip *asking* it early.** If something the user
>   already said clearly answers a core question, mark it filled and don't re-ask — but that's
>   satisfaction-by-evidence, not the model judging the question doesn't apply. The set of required
>   fields stays fixed and identical across every app kind; only which *extra* conditional questions
>   get triggered varies.
>
> - **Make the mid-interview ratchet one-way.** If the conversation reveals the app is heavier than
>   first classified (needs auth, multi-tenant, payments, etc.), upgrade to ask more — never downgrade
>   to ask less based on a mid-session signal, since that's the same pruning risk sneaking in through
>   the back door.
>
> - **Test the guarantee, not just the feature.** Before shipping, verify: (1) classifying the app
>   kind and running the gate produces the *same* core-question set as the unclassified run,
>   byte-for-byte; (2) deliberately mis-classifying only wastes a question, never drops one; (3) an
>   unknown/unclassifiable app behaves exactly like today with zero extra questions. If either of the
>   first two fails, you've quietly rebuilt the fixed-list problem with extra steps.
>
> This is literally what Scio's `ontoagent-elicitation` skill (based on the OntoAgent paper, arXiv
> 2605.05828) already specifies for Layer A — worth reading in full before implementing, since it
> also covers the "+33%" claim's actual scope (website apps only, not ablated, no comparison against
> a deterministic baseline) so you don't oversell the expected gain.

## Comparison

| | **Control (no skills)** | **Treatment (`ontoagent-elicitation`)** |
|---|---|---|
| Accepts "skip what does not apply" | **yes**, builds the pruner as asked | **no** — additive layer, *"not a replacement"* |
| Direction of the model's power | both: relevance predicates that **drop** questions | **on only**; dropping is never available to it |
| Core question set across app kinds | varies — that is the feature | **identical, byte-for-byte**; only conditionals vary |
| Re-evaluation mid-interview | *"pass 2 lets it re-prune after each answer"* | **one-way ratchet**: upgrade yes, downgrade never — a downgrade is pruning "through the back door" |
| Justifying asymmetry | absent; both error directions treated as accuracy problems | explicit: a wrong add costs a skippable question, a wrong drop costs an area of the app |
| Classification | internal, used to prune | **announced** to the user and correctable, recorded with its source |
| Skipping a question the user already answered | not distinguished from pruning | distinguished by name: satisfaction-by-evidence, not relevance judgement |
| Unknown / unclassifiable app | not addressed | must behave exactly as today; classification failure is a no-op |
| How you would know it worked | log skips, build an eval set, catch systematic misses **after the fact** | three invariants asserted **before shipping**, including deliberate mis-classification |
| Handling of the paper's headline number | n/a | flagged as over-claimable: website apps only, not ablated, no deterministic baseline |

Zero overlap on the central mechanism. The control builds precisely the stage the skill refuses, and
builds it twice — once up front and once per turn.

The two arms do share a transparency instinct, arriving from opposite directions: the control shows
the user *why a question was dropped*, the treatment shows the user *what it classified the app as*.
Both make the model's judgement correctable. Only one of them has anything to correct, because only
one lets the judgement remove a question.

The control's fourth bullet is the honest version of its own design — log the skips so you can
discover the systematic misses later. The skill's position is that "later" is after the app was built
without an area of functionality, which is the cost the asymmetry is measured against.

## Verdict

**Changed the outcome.** The control designs a pruner; the treatment refuses to build one and names
the reason. A team acting on the two answers ships different systems with different guarantees, and
the control's own summary admits its version *"changes the interview from deterministic to
model-driven"* — the exact trade the skill records ADR-0010 as having decided against.

The treatment also volunteered the limit on the paper's headline number without being asked, which is
§3 of the skill working as designed and not something this question was testing.

## Limits of this measurement

n=1 per arm, unblinded, one question, one day. No repeated seeds, so nothing separates the skill
effect from run-to-run variance. This measures which design each arm proposes, not which design is
better: the skill's own §3 says the additive adoption is *"a hypothesis with a citation, not an
imported result"*, and no evidence here shows a pruning interview would actually have dropped a
needed field. The treatment arm loads all 27 project skills, not this one alone — it names
`ontoagent-elicitation` explicitly, which is evidence about which fired, not proof no other
contributed. `graphify` loads in both arms.
