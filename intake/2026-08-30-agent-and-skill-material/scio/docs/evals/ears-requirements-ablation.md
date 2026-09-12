# Ablation · `ears-requirements`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
So does `session-start-hook`. The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

**Two questions were run, because the first did not discriminate. Neither did the second.**

## The discriminating rule, and why the obvious answer is wrong

EARS itself — five sentence patterns from Rolls-Royce, RE'09 — is a syntax, and a syntax is a poor
ablation target: a model either knows the five keywords or it does not, and knowing them changes no
outcome. The rules worth testing are the two the skill adds *against* instinct:

1. **§5 · quality attributes are not requirements.** *"It should feel fast"* belongs in a trade-off
   discussion, **not in a SHALL sentence with an invented threshold.** Eval **E9** makes the refusal
   explicit: the skill must return *"not expressible as a criterion"* rather than inventing one, and
   calls this *"the single most likely way to misuse EARS here."* §3's assumption 1 names the failure
   mode precisely: **the syntax makes bad requirements look rigorous.**
2. **§2.4 · prose stays primary.** *"The user reads the story, not the list… showing a restaurant
   owner a numbered SHALL list is a worse product."* Eval **E7** exists, in its own words, *"because
   the most likely way to get EARS wrong here is to succeed at it and ship a worse product."*

The obvious answer is wrong in both cases in the same direction: **more rigour looks like more
quality.** Asked to make a vague criterion testable, everyone reaches for a metric and a number.
Asked how to get sign-off on a decomposed spec, everyone reaches for the itemised list.

## The questions

**Q1 (§5 / E9):**

> *A lot of our 'done when' items are things like 'the app should feel fast' and 'the code should be
> clean and well structured'. I need to rewrite them so they can actually be tested. How? Four bullets
> maximum.*

**Q2 (§2.4 / E7), run after Q1 failed to discriminate:**

> *Before we build, we want the customer — a restaurant owner, say — to confirm what we understood. We
> have the whole thing broken down into individually numbered, individually checkable statements.
> Should we just show her that list to sign off? Four bullets maximum.*

Neither names a skill, a file, or "EARS".

## Control answer

**Q1:**

> Turn each vague criterion into a threshold on something you can actually measure:
>
> - **Name the metric, not the feeling.** "Feels fast" → time-to-interactive, p95 API latency, or
>   input-to-paint delay. "Clean code" → cyclomatic complexity, duplication %, max file/function
>   length, lint error count.
> - **Attach a number and an instrument.** Every bullet needs a pass/fail number plus the tool that
>   produces it (Lighthouse score, `eslint` output, a load test harness) — if you can't name the tool,
>   the metric isn't real yet.
> - **Set the threshold from a real reference point**, not a guess: a competitor's benchmark, the old
>   hello-world system's actual numbers, or a user-perceptible constant (e.g. 100ms for "instant").
> - **Write it as a single testable sentence**: `<metric> <comparator> <value>, measured by <tool>` —
>   e.g. "p95 page load < 1.5s on 3G, measured by Lighthouse CI in the deploy pipeline."

**Q2:**

> No — a bare numbered list asks her to review a spec, which isn't her job and isn't where
> misunderstandings actually surface.
>
> - **Sign-off needs stakes, not statements**: pair each item with what it looks like in her restaurant
>   ("online orders auto-print in the kitchen") so she's confirming an outcome, not parsing our
>   phrasing back at her.
> - **Let her reject at the granularity we built it**: numbered/checkable is right for *her* to strike
>   items, not just initial the page — that's the whole point of decomposing it.
> - **Silence isn't confirmation**: for anything ambiguous or inferred (not stated by her directly),
>   flag it distinctly so agreement is active, not a rubber stamp on your assumptions.
> - **Follow it with the cheapest possible falsification** — a clickable flow or screen, even rough —
>   since owners confirm real intent by reacting to something concrete far more reliably than by
>   reading prose.

## Treatment answer

**Q1:**

> This matches the `ears-requirements` skill's territory — turning vague acceptance criteria into
> testable ones. Quick answer without invoking it, since it's a direct question:
>
> - **Replace subjective adjectives with a metric and threshold**: "feels fast" → "95th-percentile
>   response time under 200ms for action X, measured in CI/load test."
> - **Attach a measurement method to every claim**: name the tool/test that produces the number
>   (Lighthouse score, p99 latency, cyclomatic complexity, lint rule set) — if you can't name what
>   measures it, it isn't a criterion yet.
> - **Convert quality nouns into structural rules a linter or static check can enforce**: "clean and
>   well structured" → specific, checkable constraints (no function over N lines, no circular imports,
>   max nesting depth, coverage ≥ X%).
> - **Write each as EARS-style trigger→response with a pass/fail boundary**, not a feeling: "When a
>   user submits form X, the system shall respond within 200ms" — if two reviewers could disagree on
>   whether it passed, it's still not testable.

**Q2:**

> No — a bare numbered list asks her to review like a lawyer, and she'll rubber-stamp it.
>
> - **Group by what she'd recognize**: cluster statements under her own domain concepts (e.g. "Taking
>   Orders," "Reservations") not our internal breakdown, so she's confirming her restaurant, not
>   parsing our spec.
> - **Show consequence, not just claim**: for anything ambiguous, pair the statement with a concrete
>   example ("if two tables book the same slot, we'll do X") — she can catch a wrong assumption in a
>   scenario far more easily than in a sentence.
> - **Make disagreement cheap**: a checkbox/comment per item, not an all-or-nothing sign-off, so she
>   can flag #14 without feeling she's blocking the whole thing.
> - **Keep the numbering underneath**: fine to preserve item IDs for traceability back to the checkable
>   statements — just don't make the ID the primary thing she reads.

## Comparison

**Q1 — on mechanism:**

| | **Control** | **Treatment (`ears-requirements` loaded)** |
|---|---|---|
| Core move | metric + threshold + instrument | metric + threshold + instrument |
| "feels fast" → | p95 latency, TTI, measured by a named tool | p95 under 200ms, measured in CI/load test |
| "clean code" → | complexity, duplication, max lines, lint count | no function over N lines, no circular imports, coverage |
| Sentence form | `<metric> <comparator> <value>, measured by <tool>` | *"EARS-style trigger→response with a pass/fail boundary"* |
| **§5 · refuse to express a quality attribute** | absent | **absent** |
| **E9 · "not expressible as a criterion"** | absent | **absent** |
| Threshold provenance | *"set from a real reference point, not a guess"* — **the control was the more careful arm here** | invented 200ms with no derivation |

Same conclusion, same mechanism, four bullets to four bullets. The one visible difference is the
phrase "EARS-style" in the treatment's fourth bullet — a label on the same advice. The treatment's own
opening is the honest summary: *"Quick answer without invoking it."*

Worse: the treatment did the thing its own §3 warns about. It invented `200ms` with no reference
point, while the *control* insisted a threshold must come from a benchmark or a user-perceptible
constant rather than a guess. On the skill's stated failure mode — *the syntax makes bad requirements
look rigorous* — the unskilled arm was marginally safer.

**Q2 — on mechanism:**

| | **Control** | **Treatment** |
|---|---|---|
| Verdict on showing the list | **No** | **No** |
| Reason | *"asks her to review a spec, which isn't her job"* | *"asks her to review like a lawyer, and she'll rubber-stamp it"* |
| Fix | pair each item with what it looks like in her restaurant | group under her own domain concepts; pair with a concrete scenario |
| Keep the ids? | implied (strike items at that granularity) | explicit — *"keep the numbering underneath"* |
| Active vs passive agreement | flag inferred items so agreement is active | per-item checkbox so disagreement is cheap |

Both arms reached §2.4's conclusion — the list is not the artifact, keep the ids reachable behind
something the owner recognises — by the same reasoning. The treatment stated the id-underneath rule
more explicitly; the control added a prototype step the treatment did not. Neither difference is a
mechanism difference.

## Verdict

**No difference**, on two questions aimed at the skill's two counter-instinctive rules.

The reason is worth stating plainly, because it is not "the skill is bad". EARS is a *convention*: its
value is that a second reader can check a sentence against a named pattern, that requirements get ids
a generated function can point at, and that §2.3's object fields (`grounding`, `origin`,
`satisfied_by`) exist to be validated by rules E1–E6. **None of that is reachable by a question a
person types.** It is reachable by running the checks against a real requirement set — which is an
eval of the *rules*, not an ablation of the *skill*.

And on the one part that is a judgement call rather than a convention — refusing to invent a threshold
for a quality attribute — the loaded skill did not fire. That is a finding about the skill's
prose-to-behaviour transfer, on n=1: §5 and E9 are stated clearly in the file, the file was in context,
the answer contradicted them, and the model reported it was answering *"without invoking it."* A rule
that is in the room and does not fire is indistinguishable from a rule that is absent.

## Limits of this measurement

n=1 per arm, unblinded, two questions. I wrote the questions knowing what the skill says and judged
the answers knowing which arm was which. Two nulls do not show the skill is inert — they show these
two questions do not reach it, and a third might. In particular, nothing here tests E1–E6, which are
mechanical checks over a requirement object and are where this skill's actual content lives; nothing
here tests §6's clause↔`Script` mapping either. A null on a question that cannot reach the substance is
a weaker result than a null on one that can, and this is the weaker kind.
