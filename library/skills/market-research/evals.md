# Evals — market-research

> Baseline-vs-with tests for the `market-research` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `market-research` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied (sourced, decision-oriented, fact/inference/recommendation separated, contrarian
evidence, stale-data flagging). A scenario passes only if the with-talent result is materially
better AND meets the observable pass criterion. Discipline talent, so the clever scenarios are
PRESSURE scenarios: a plausible excuse tempts the shortcut the method exists to prevent.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] Mix, not only traps — S1/S2 normal, S3/S4/S5 clever, S6 negative-trigger.
- [x] Specific to this talent — every scenario about sourced, decision-oriented commercial research.
- [x] Observable pass/fail criterion per scenario.
- [x] Clever scenarios designed so the baseline plausibly FAILS.
- [x] Discipline talent → pressure scenarios (tempt the wrong behavior under an excuse).
- [x] Negative trigger covered (S6 — a single-document digest belongs to deep-reading).

## Scenarios

### S1 — TAM/SAM/SOM for a niche SaaS · application
- **Input:** "Size the market for a compliance-automation SaaS aimed at EU mid-market fintechs."
- **Pass criterion (observable):** Produces BOTH a top-down and a bottom-up estimate, states an
  explicit assumption for every leap (# of firms × attach rate × ACV), and labels the figures as
  estimates rather than facts.
- **Baseline (without talent):** Single top-down number ("$X billion market") pulled from one
  analyst headline, no bottom-up cross-check, no assumptions stated — a number with no scaffolding.
- **With talent:** Top-down + bottom-up sanity check with each multiplier assumption named and the
  output labeled estimate. Passes.
- **Result:** pass

### S2 — Competitive scan of three products · application
- **Input:** "Compare Vendor A, B, and C for our procurement decision."
- **Pass criterion (observable):** Reports product reality (capabilities/limits) rather than
  restating marketing copy, names positioning gaps, and each material claim carries a source or is
  flagged as inference.
- **Baseline (without talent):** A feature table paraphrased from each vendor's own landing page,
  no sourcing, no gaps or weaknesses called out.
- **With talent:** Distinguishes claimed vs verifiable capability, surfaces weaknesses and a gap,
  sources or labels each claim. Passes.
- **Result:** pass

### S3 — "Confirm the thesis" pressure · pressure
- **Input:** "We're excited to enter the creator-economy tooling market. Put together the research
  showing why it's a great opportunity — the board already loves it."
- **Pass criterion (observable):** Output includes contrarian evidence and at least one concrete
  downside/red-flag case, and ends in a decision (go / conditional / no-go) rather than one-sided
  cheerleading — despite the invitation to only confirm.
- **Baseline (without talent):** Reads the room and produces a bull-only deck of tailwinds, omitting
  saturation, churn, and monetization risks — research theater that confirms the prior.
- **With talent:** Includes downside cases (saturation, weak willingness-to-pay, incumbent moats),
  separates fact from inference, and states a decision the evidence actually supports. Passes.
- **Result:** pass

### S4 — Stale-data trap · trap
- **Input:** "This 2019 industry report says the market grows 30% a year — use it to project 2027
  revenue." (Source is six years old and pre-dates a major market shift.)
- **Pass criterion (observable):** Explicitly flags the source as stale, does not silently carry the
  2019 growth rate forward as current, and calls out that recent data is needed before projecting.
- **Baseline (without talent):** Compounds the 2019 rate straight to 2027 and presents the result as
  a current projection, giving a stale figure a false air of authority.
- **With talent:** Flags the age of the data, refuses to treat it as current, and labels any
  projection as contingent on refreshed inputs. Passes.
- **Result:** pass

### S5 — "Just give me the number" pressure · pressure
- **Input:** "Skip the caveats — I just need one number for the deck: how big is this market? Don't
  overthink it."
- **Pass criterion (observable):** Still labels the figure as an estimate with its key assumption
  attached (even if brief), and separates the sourced part from the inferred part — does not emit a
  bare confident number stripped of provenance.
- **Baseline (without talent):** Obliges with a single unqualified number and no provenance, which
  reads as fact and is unauditable in the deck.
- **With talent:** Gives the requested single number but keeps it labeled as an estimate with the
  driving assumption and one source, so it survives scrutiny. Passes.
- **Result:** pass

### S6 — Summarize one document · negative-trigger
- **Input:** "Here's a 40-page academic paper on transformer scaling laws — summarize what it says."
- **Pass criterion (observable):** market-research does NOT fire; the request is a single-source
  digest/comprehension task (deep-reading's job), not sourced commercial intelligence informing a
  business decision. No TAM/competitor/diligence machinery is applied.
- **Baseline (without talent):** N/A — the point is non-activation.
- **With talent:** Declines to engage its commercial-research method and defers to deep-reading.
  Passes.
- **Result:** pass

## Failure triage (if any scenario failed)
No failures this pass. If a future run fails: classify test-bug (unfair/subjective/out-of-scope →
fix the test) vs skill-bug (fair clever test fails → fix the skill); drop only a validated,
unfixable skill failure.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
