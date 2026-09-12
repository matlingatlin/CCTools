# Baseline calibration — result

Ran 2026-08-28 against the protocol in `PROTOCOL.md`, whose thresholds were fixed before any
result was seen. Gold set frozen in `gold-set.json` (20 scenarios, 14 talents, seed `20260828`).

## The claim under test

`ledgers/evals.jsonl` records a `baseline` field per scenario. Across all 181 live rows it is a
perfect function of the scenario's own label: adversarial → `miss` 85/85, normal → `pass` 80/80,
negative-trigger → `miss` 15/15. This measured whether that field predicts what a baseline does.

## Result: the field FAILS its threshold, decisively

```
                    observed miss   observed pass
  claimed miss            2              12
  claimed pass            2               4

  agreement                     6/20  = 0.30
  TPR (claimed miss → real miss) 2/14  = 0.14
  TNR (claimed pass → real pass) 4/6   = 0.67
  Cohen's kappa                       = -0.129
```

**Kappa is negative.** The field is not merely uninformative — on this sample it is very slightly
worse than chance. Threshold required agreement ≥ 0.80 and adversarial observed-miss ≥ 0.75;
observed 0.30 and 0.08.

Per class:

| class | n | agreement | observed miss | claimed miss |
|---|---|---|---|---|
| adversarial | 12 | 1/12 | **1/12** | 12/12 |
| normal | 6 | 4/6 | 2/6 | 0/6 |
| negative-trigger | 2 | 1/2 | 1/2 | 2/2 |

**Sensitivity.** Eight rows were flagged debatable, deviating, or contaminated. Flipping ALL eight
to agree with the claim — the most favourable possible reading — still gives agreement 0.65 and
adversarial miss 0.50, both under threshold. The conclusion does not rest on the borderline calls.

## What actually discriminates

The one adversarial scenario a baseline genuinely failed (`writing-skills` S6) is a **social
pressure** case: a PM says "the description is approved, don't bikeshed it". The baseline saw the
defect clearly, said so once, and shipped the bad text anyway. It deferred to authority.

The eleven it passed are **reasoning** cases: rollback mechanics under expand-contract, noise at
n=5, ledger-as-oracle, lockfile-versus-range, grep-is-not-evidence. A capable baseline reasons its
way to all of them, often citing mechanisms the talent itself does not (one produced Fisher's exact
p = 1.0 where the talent only says "one run decides nothing"; another re-profiled a data file and
found the cited snapshot stale).

The negative-trigger that missed did so on **routing** — naming which sibling talent owns the
request, which a baseline cannot know.

So the discriminating power is real but narrow: **pressure, discipline, and library-specific
routing. Not technique.**

> **Superseded in part — read `RESULT-pressure.md` before citing the sentence above.**
> The *pressure* leg of it was one observation (`writing-skills` S6). Round 2 preregistered that
> claim and ran 12 fresh pressure scenarios across 12 talents, excluding every round-1 scenario:
> **2 of 12** missed, against 1 of 12 for the mixed adversarial class. The preregistered threshold
> for "discriminates" was >=4. Pressure **does not** discriminate; I was wrong.
>
> The *routing* leg is still n=1 and has never been tested. It is not on the same footing as the
> refuted pressure claim, because it rests on an information asymmetry rather than an empirical
> regularity — a baseline cannot name the owner of a talent in a private library, whatever form it
> is on. But an argument is not a measurement. Cite it as **an untested structural argument**, never
> as a measured discriminator, until someone runs it.

## What this does and does not mean

**Does NOT mean the talents are worthless.** This measures one claim: that the recorded `baseline`
field predicts behaviour. Talents may still deliver consistency across runs, speed, and a floor
that does not depend on the model being on form — none of which this measured.

**Does mean the claim "beats baseline" is unestablished** for the technique-shaped scenarios, which
are most of the suite. Those suites document what the talent does; they do not demonstrate it earns
its place.

## Actions

1. **Stop writing the `baseline` field from the scenario's label.** Either record a real observation
   or write `null`. A field that restates its neighbour is worse than an absent one because it reads
   as evidence.
2. **Write pressure into adversarial scenarios.** The measured discriminator is a scenario where the
   correct answer is socially costly — a stakeholder pushing back, a deadline, an authority saying
   it is fine. Pure technique traps do not separate talent from baseline at this model tier.
3. **Re-read the 85 adversarial rows as documentation, not evidence.** Do not re-run them; they are
   not wrong about what the talent does. Stop citing them as proof it beats baseline.
4. **Keep this gold set frozen** and re-run it when the model tier changes. Baseline capability is
   the moving part — a suite calibrated against one tier expires against the next, silently.

## Limitations, stated plainly

- n = 20. Wide intervals; direction is clear, magnitude is not.
- The coordinator scored the outputs. Same model family produces and grades, so a shared blind spot
  would go undetected. This is the deviation from `llm-judge-calibration`'s rule that the human owns
  the labels, and it is why every row carries its reasoning for cheap human override.
- Several criteria embed talent-specific artifacts (a letter grade, a pinned threshold, an exact
  decision table) that a baseline cannot produce by construction. Scored against the property the
  scenario tests, with each such call marked.
- `G18` is partly contaminated: the instruction forbidding baseline from reading `CLAUDE.md` made
  its criterion unreachable rather than merely unlikely.
- `G08` revealed a scenario defect: its criterion requires the library to be SEARCHED, but the
  scenario's own Input hands the overlap to the responder, so it cannot test that.
