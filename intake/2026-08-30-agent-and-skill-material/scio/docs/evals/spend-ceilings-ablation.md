# Ablation · `spend-ceilings`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

**Confound:** `graphify` is installed at account level and loads in **both** arms (as do
`session-start-hook` and `synced`). The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

## The discriminating rule, and why the obvious answer is wrong

`spend-ceilings` D2: **an unpriced model is a refusal or a pessimistic bound, never zero.** A zero
disables the cap in exactly the condition the cap exists for — a new model id, a price change, a
provider not yet carded. This is the defect the rule was mined from, inverted.

D1 carries the second half: the check happens **before the call**, computed from a bound over the
assembled prompt. A check after the call has already paid for the call — our own `relay.py:264`
raising after `:256` has run the completion.

D5 carries the third: a run killed at its ceiling must record the cost it actually accumulated.
`loop.py:550` records `0.0`, and that zero travels into the usage event, so **the build that hits
its ceiling is the one the ledger under-reports most.**

The question's premise is written as the wrong answer: look the price up *after* the call, add,
abort if over.

## The question

> We're adding a spend cap to our build pipeline: after each model call we look the model's rate up
> in our price table, add the cost to a running total, and abort the build if it goes over the
> user's approved budget. What do we need to get right here? Four bullets maximum.

No skill, file or term unique to the skill is named. The described design contains two of the three
defects; a reader who accepts the premise will spend all four bullets on token accounting.

## Control answer

Verbatim.

> - **Match the price table key to the actual billed SKU** — model version/snapshot, region, and whether it's a cached-read/cache-write/batch rate, not just the model family name. A stale or mismatched lookup (e.g. pricing a `-latest` alias as its old snapshot) silently under- or over-charges every call.
> - **Cost the whole call, not just the visible tokens** — input, output, cache writes and cache reads are usually priced differently, and reasoning/thinking tokens count too. If the running total only sums prompt+completion tokens it will systematically undercount and let real spend blow past the cap.
> - **Handle the check-then-spend race** — if calls can run concurrently, "read total, compare to budget, add cost" is a TOCTOU bug: two calls can both pass the check before either updates the total. Either serialize the accounting or reserve/estimate cost before dispatch and reconcile after.
> - **Decide what "abort" means for a call already in flight or already billed** — you can't refund a completed API call, so the cap has to stop the *next* call, not claw back the one that pushed you over; also treat a failed price lookup as fail-closed (abort) rather than silently treating the call as free.

## Treatment answer

Verbatim.

> Four things to get right:
>
> - **Check before, not after** — the call you're describing (call → look up price → add → abort) checks the ceiling *after* paying for the call that broke it. Compute a pessimistic bound (prompt tokens + output cap × rate) before issuing the call, and refuse if the bound would cross the ceiling. This is our own repo's verified defect (`relay.py:264` checks after `:256` already ran the completion).
>
> - **Never let an unpriced model resolve to zero.** A lookup miss on a new model id or a price-table gap must refuse the call or use a pessimistic bound — not fall through to `0`, which silently disables the cap exactly when it's needed most.
>
> - **Record the partial, not zero, on abort.** When a build is killed mid-way for hitting the ceiling, attach the cost actually accumulated so far to that failure — don't let the exception path skip the running total and report `cost_usd: 0.0` for a build that clearly spent something.
>
> - **Meter every outcome, including the abort itself.** Refused and killed builds need a usage record same as successful ones, or the ledger under-reports the exact runs a spend dispute would be about.
>
> One more worth flagging even though it's not in your four: consider whether you want a relative check (this build vs. comparable past builds) alongside the absolute ceiling — an absolute cap alone never catches a cost regression that stays under it.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Unpriced model must not be treated as free | **yes** — trailing clause of bullet 4: "treat a failed price lookup as fail-closed (abort) rather than silently treating the call as free" | yes — its own bullet, refuse **or pessimistic bound** |
| Where the ceiling is checked | **inverted** — "the cap has to stop the *next* call, not claw back the one that pushed you over" | before the call, on a computed bound over the assembled prompt |
| Cost recorded when a run is killed at the ceiling | absent | the accumulated partial, never `0.0` |
| Refused / cancelled / failed runs are metered | absent | yes — "the ledger under-reports the exact runs a spend dispute would be about" |
| Relative instrument beside the absolute cap | absent | raised, explicitly outside the four |
| Price-table key correctness (snapshot, region, cache/batch tier) | **yes, and only the control** | absent |
| Pricing both halves plus cache and reasoning tokens | **yes, and only the control** | absent |
| Concurrency / TOCTOU on the running total | **yes, and only the control** | absent |

## Verdict

**Changed the outcome, on different ground than predicted.** The rule the ablation was designed to
test — *unknown price is never zero* — **the control also produced**, unprompted, without the skill.
It arrives as a subordinate clause rather than a headline, and it offers only refusal where the
skill also allows a pessimistic bound, but the mechanism is the same and it must be scored as a
convergence. The defect this rule was mined from is not one this model walks into when asked.

Where the arms genuinely disagree is **enforcement point**. The control states, as settled
engineering, that a cap can only stop the *next* call. The skill says the bound is computable before
the call and must be — and its own Limits section concedes the trade the control is implicitly
making ("not free… it trades a bounded overshoot for a risk of over-refusal"). This is a real
mechanism conflict, confidently stated on both sides, and the treatment names our own `relay.py`
line as the live instance.

The second difference is the **ledger**: recording a partial rather than `0.0`, and metering
refused and killed runs. Neither appears in the control at all, and the skill's Limits section
flags this as the half of the fix with no downside.

The control was better than the treatment on three things the skill does not cover: SKU/snapshot
keying, cache and reasoning token tiers, and the TOCTOU race on a shared total. That is worth
recording as a gap in the skill, not as noise.

## Limits of this measurement

n=1 per arm, one question, unblinded, graded by the person who wrote the question. The control's
unpriced-model clause is one sentence and a re-run might drop it, which would flip the headline of
this file — a strong argument for not believing any single-sample ablation, including this one.
`graphify` loads in both arms and is not controlled for. Nothing here measures whether a limit
shaped to the skill actually saves money; the skill states plainly that nobody has measured that.
