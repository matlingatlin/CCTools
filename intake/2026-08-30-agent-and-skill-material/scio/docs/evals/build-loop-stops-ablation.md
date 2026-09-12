# Ablation · `build-loop-stops`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at account level and loads in **both** arms (as do
`session-start-hook` and `synced`). The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

Two rules, both in the skill's D1–D2:

1. **A plateau is a set comparison, not a judgement.** This round's *finding set* equals the
   previous round's — decided by comparing structured gate findings, not by asking whether the run
   "improved".
2. **The gate's output is the repair's input.** A round fed only the prompt and its own previous
   answer is intrinsic self-correction, which Huang et al. (ICLR 2024) and Kamoi et al. (TACL 2024)
   find does not reliably help and can degrade. That is the live defect at `relay.py:148-167`.

And D4: the stop is reported as a closed set of sentinel outcomes, where **`blocked` is neither
success nor error**.

The predicted wrong answer was a score threshold or a tuned retry count.

## The question

> Our build loop retries a failing fix up to five times before giving up, and it often burns all
> five attempts on the same error. How should it decide to stop earlier? Four bullets maximum.

No skill, file or term unique to the skill is named. "Up to five times" puts a count in front of
the reader.

## Control answer

Verbatim.

> - **Fingerprint the error before retrying** — hash the error signature (type + message + failing location); if attempt N+1 produces the same fingerprint as attempt N, stop instead of consuming another try.
> - **Require forward progress, not just a new attempt** — only continue if the diff or error output actually changed shape (fewer failures, different file/line); an unchanged or worsening signal ends the loop early.
> - **Cap retries on the same fix strategy, not on raw attempt count** — if the fix keeps touching the same code path/hypothesis, treat repeats of that strategy as one exhausted attempt and force a strategy change or escalate to a human/log after 2, not 5.
> - **Escalate with the accumulated diagnostic, don't just fail silently** — once stopped early, surface all failed attempts + fingerprints together so the next fix (human or agent) isn't starting blind.

## Treatment answer

Verbatim.

> - **Add a plateau detector**: compare this round's gate finding set to the previous round's — if identical, stop immediately rather than retrying to the cap. It's a free comparison and directly targets "burns all five on the same error."
> - **Add non-convergence detection**: stop after the same error recurs three times, or when a fix creates more new findings than it resolves — that's a distinct condition from plateau (error unchanged) and should fire before round 5, not at it.
> - **Feed each retry the failing gate's output plus a durable note of what was tried and why it failed**, not just the previous attempt — a loop retrying blind is the self-correction failure mode the literature (Huang et al. ICLR 2024, Kamoi et al. TACL 2024) shows doesn't work; without that feedback, more attempts won't help regardless of the cap.
> - **Make three failed hypotheses its own stop condition** (distinct from the count), reported as `blocked("wrong-architecture")` rather than exhausting the cap silently — three misses signals the fix approach itself is wrong, not that one more attempt will land.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Stop on a repeat rather than on the cap | **yes** — hash of `type + message + failing location`, compared round to round | yes — comparison over the **gate's finding set** |
| What is compared | the error string's fingerprint | the structured finding set the gates emit |
| A worsening fix ends the loop | **yes** — "an unchanged or worsening signal" | yes — "creates more new findings than it resolves" |
| Repeated hypothesis is its own condition | **yes** — cap per fix strategy, escalate after 2 | yes — three failed hypotheses |
| Repeated hypothesis means *wrong architecture* | no — it means try another strategy or ask a human | yes, and reported under that name |
| The retry is **fed the gate's output** | absent — diagnostics are gathered for whoever comes *after* the loop | **yes**, as the round's input, with the two papers cited |
| A durable per-round note of what was tried and why it failed | at exit only | per round, so round 3 does not repeat round 1 |
| Machine-readable terminal state; `blocked` distinct from `error` | absent — "escalate to a human/log" | `blocked("wrong-architecture")` as a sentinel |
| A tuned retry count or score threshold as the answer | **no** — the control explicitly rejects raw attempt count | no |

## Verdict

**Changed the outcome, in part — and the question's premise was wrong.** The predicted trap did not
catch the baseline at all: the control never proposed a score threshold and explicitly argued
*against* raw attempt counts, reaching a plateau detector under its own steam. Three of its four
bullets are the same conditions the skill lists, arrived at independently.

The difference that survives is **D1, the feed**: only the treatment made the failing gate's output
the repair's input and cited the reason it matters, and only the treatment kept a per-round note
whose purpose is to stop round 3 repeating round 1. The control's diagnostics are assembled at exit
for the next human — a different mechanism with a similar name. The second surviving difference is
D4's vocabulary: `blocked` as a distinct machine-readable outcome versus "escalate to a human/log".

Both differences are real and both are narrower than the skill's own framing implies. The stop
*conditions* are largely common knowledge; what the model does not hold is that a loop must be
**fed** and that its ending must be **named**.

## Limits of this measurement

n=1 per arm, one question, unblinded. I chose the question knowing the rule and graded the answers
myself. The predicted wrong answer failing to appear is itself evidence that a single sample tells
you little about what a model will do — a second run of the control might well produce the retry
count the first one refused. `graphify` loads in both arms and is not controlled for. No claim is
made that a loop built to D1 stops sooner or costs less; nobody has measured that, and the skill's
own Limits section says so.
