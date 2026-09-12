# Ablation · `req-elicit-gym`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.

Two questions were run — one on method, one on what the research actually found, as the second is
where a research skill is most likely to hold something a model does not. Both are nulls. Both are
recorded.

## The discriminating rule, and why the obvious answer is wrong

**Q1 · §2.2 — the oracle user's three principles**, of which the second is the trap: **passive
disclosure.** The simulated stakeholder *"does not volunteer anything it was not asked for"*, and
answers **only** from the scenario's annotated implicit requirements — it may not invent one to be
helpful. *"A cooperative simulator hands over the whole spec on turn one and every interviewer scores
1.0."* The obvious answer is to make the fake user as realistic and as helpful as possible, which is
exactly what the question asks for and exactly what destroys the metric.

**Q2 · §2.4 — CoT prompting improves TKQR but not IRE.** *"Better question ordering is not more
coverage. A change that moves only TKQR has made the conversation politer, not better."* Plus §3
constraint 3: one run is one observation; report variance across seeds. The obvious answer is that
asking the important questions earlier is straightforwardly an improvement.

## The questions

> **Q1.** *We want to test our onboarding interview bot by having a second LLM play the customer. We
> want the fake customer to behave as much like a real user as possible so the score means something.
> How should we set that up? Four bullets max.*

> **Q2.** *We tweaked the prompt on our requirements interview bot. It now asks the most important
> questions much earlier in the conversation than it used to, and our ordering metric went up nicely.
> That is a real improvement, right? Four bullets max.*

Neither names a skill, file or unique term. Q1 asserts realism as the goal; Q2 asserts the
improvement and asks for agreement.

## Control answer

**Q1** (verbatim):

> - **Persona-condition, don't instruction-condition**: give the simulator LLM a rich, specific
>   persona (goals, tech-savviness, patience level, hidden constraints, mood) rather than telling it
>   to "act like a user" — vague instructions produce a cooperative, articulate fake user that's
>   easier to interview than any real one.
> - **Withhold and let it be messy**: the persona should know its own situation but not what the bot
>   needs to hear — force it to reveal info only when asked, allow contradictions, typos, one-word
>   answers, topic drift, and impatience, since a too-tidy simulated user inflates scores relative to
>   real intake calls.
> - **Sample a population, not one persona**: run many conversations across a distribution of
>   personas (varying domain knowledge, communication style, edge cases, adversarial/confused users)
>   and report score distributions, not a single transcript — one persona measures one path through
>   the bot, not the bot.
> - **Validate the simulator against real transcripts before trusting the score**: compare simulated
>   conversations (or blind human ratings of sim vs. real transcripts) to actual onboarding calls; if
>   humans/metrics can reliably tell them apart, the eval isn't measuring what you think, and the
>   persona prompts or judge rubric need fixing before you trust it as a regression gate.

**Q2** (verbatim):

> No — this is a classic Goodhart trap, not a validated improvement.
>
> - "Ordering metric" almost certainly rewards asking important questions earlier in the sequence, not
>   whether the interview actually elicits better requirements — reordering questions is the cheapest
>   possible way to move that number without improving anything real.
> - Asking high-stakes questions before rapport/context is established can hurt answer quality (users
>   under-informed or defensive early on), so the same change could be raising the metric while
>   lowering actual requirement accuracy.
> - No counter-metrics are mentioned: completion rate, answer quality/specificity, downstream rework
>   or misunderstood-requirements rate. Without at least one of these moving in the right direction
>   too, you only know the prompt got better at gaming the metric.
> - Per this repo's conventions ("Findings are claims, not facts" / verify before acting), treat this
>   as a claim to test — run an A/B or blind comparison on a quality proxy (e.g. human-rated
>   requirement completeness) before crediting the prompt change as a real win.

## Treatment answer

**Q1** (verbatim):

> - **Ground it, don't let it help you**: write scenario personas with an annotated set of implicit
>   requirements, and instruct the simulator to answer *only* from that annotated set — never invent
>   or infer a requirement to be nice.
> - **Passive disclosure is the whole trick**: it must never volunteer anything it wasn't asked about
>   (that's what makes the interviewer's score mean anything — a cooperative simulator that dumps the
>   spec on turn one makes every interviewer look perfect).
> - **Context-aware, not omniscient**: it remembers the conversation so far (no repeating itself, no
>   contradicting earlier answers) but has no access to anything outside its persona's annotated
>   requirements.
> - **Validate the simulator itself before trusting scores from it**: test that it discloses nothing
>   unprompted, discloses exactly the right thing when asked directly, and says "doesn't apply" (not a
>   fabrication) when asked about something outside its scenario — and treat resulting scores as a
>   *regression detector*, not proof the interview bot is "good" (real-user testing is still required
>   for that claim).

**Q2** (verbatim):

> - Your "ordering metric" is TKQR (turn-discounted key question rate) — it rewards asking critical
>   questions *early*, not asking *more* of them. The paper's own finding: **CoT prompting improved
>   TKQR but not IRE** (coverage). Better ordering ≠ better elicitation.
>
> - So the honest read is: the conversation got politer, not necessarily better. Check IRE (elicited ÷
>   ground-truth requirements) and ESR (probes that actually surfaced something) before calling this
>   an improvement — TKQR moving alone is consistent with the bot asking the same questions, just
>   resequenced.
>
> - Watch for a specific failure mode: if reordering pushed "important" questions to the front, it may
>   have shortened turns spent on later probes, which could *drop* IRE even while TKQR rises. A single
>   number going up can hide a real regression elsewhere.
>
> - One run is one observation — report IRE/ESR/TKQR across seeds, not a single before/after diff, and
>   say explicitly whose metric on what scenarios (per req-elicit-gym skill: never write "+X%" without
>   that qualifier).

## Comparison

**Q1 — the trap was refused by both arms.**

| Mechanism | **Control** | **Treatment** |
|---|---|---|
| Accepts "as realistic as possible" | **no** — rich persona, but reveal only when asked | **no** — grounded and passive |
| Passive disclosure | **present**, in its own words: *"force it to reveal info only when asked"* | present, called *"the whole trick"* |
| Cooperative simulator inflates the score | **present**: *"a too-tidy simulated user inflates scores"* | present: *"dumps the spec on turn one makes every interviewer look perfect"* |
| Answers only from an **annotated** requirement set | **absent** — persona has a "situation", not annotated ground truth | present, and it is what makes a coverage ratio computable at all |
| Simulator must not invent a requirement | implied by the persona | stated as its own rule, with a test for it |
| Context-aware / no self-contradiction | present (allows contradictions deliberately) | present (forbids them) — a genuine disagreement, on a minor point |
| Validate the simulator before trusting scores | **present**, against real transcripts | present, as three self-tests on the simulator's behaviour |
| Score is a regression gate, not a quality verdict | **present** — *"before you trust it as a regression gate"* | present — *"a regression detector, not proof the interview bot is 'good'"* |
| Population / variance across runs | **present** — distributions, not one transcript | absent from this answer |
| Named metrics (IRE / ESR / TKQR), the 0.32 baseline | absent | **absent** — the skill's headline content did not surface here either |

**Q2 — same verdict, and substantially the same argument.**

| | **Control** | **Treatment** |
|---|---|---|
| Verdict | **No** | **No** |
| Core argument | ordering is the cheapest way to move that number without improving anything | ordering ≠ coverage; the conversation got politer |
| Names the thing to check instead | quality proxy: completion rate, answer specificity, downstream rework, human-rated completeness | **coverage**: IRE, and ESR for wasted probes |
| Cites the published finding | no | **yes** — CoT improved TKQR but not IRE |
| Reordering could *reduce* coverage | implied via "lowering actual requirement accuracy" | stated as a mechanism: front-loading eats turns from later probes |
| Variance / seeds | absent | present |
| Frames it as a claim to verify | **yes**, quoting repo convention | implicitly |

## Verdict

**No difference** — on both questions.

On Q1 the control reached passive disclosure, benevolence bias and the regression-gate framing on its
own, in the same breath and for the same reason. On Q2 both arms rejected the premise and both located
the fault in the same place: a proxy moved, coverage is the thing to check. The treatment names the
proxy (TKQR), the coverage metric (IRE), and the published result; the control calls it a Goodhart
trap and asks for a quality counter-metric. **That is the same reasoning with different vocabulary,
which this eval counts as no difference.**

What the treatment did add, and it is worth recording precisely because it did not change the verdict:
an **annotated ground-truth requirement set**, without which no coverage ratio exists — the control's
design produces realistic conversations and no computable IRE; a **citation** rather than an intuition;
and the **variance-across-seeds** rule on Q2. What the control added: a persona population, completion
rate, and validation against real transcripts, none of which appeared in the treatment answers.

Also worth recording as a negative: on neither question did the treatment surface the skill's own
headline numbers — **IRE = 0.32 as the published baseline**, the near-zero style-aspect elicitation, or
the κ = 0.73 oracle validation. Those are the parts a general model could not know, and they are the
parts that did not fire. This is a result about which content of a skill reaches an answer, and it is
the more useful half of a null.

## Limits of this measurement

n=1 per arm, unblinded, two questions, one day. No repeated seeds — which is the exact discipline the
skill itself demands and this eval does not meet. A null here is weak evidence: it shows the skill did
not change *these two* answers, not that it holds nothing the model lacks, and the unfired numeric
content above is direct evidence that a different question could land differently. The treatment arm
loads all 27 project skills, not this one alone. `graphify` loads in both arms.
