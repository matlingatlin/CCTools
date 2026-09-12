# D5 · Record shapes — what a meter, an override and a ledger actually contain

Load this when writing the record, not when deciding the policy.

## The four meter states

From `docs/mined/PASS2-GSTACK-TESTS.md:706`: **never render a missing value as a good value.**

| State | Means | Renders as |
|---|---|---|
| `trusted` | measured, by the instrument that owns it | the number |
| `unverified` | measured, but by a path that cannot prove freshness | the number, marked |
| `unknown` | not measured — the flag was off, the tool absent, the run cut short | *not measured*, never `0` |
| `error` | the measurement itself failed | *measurement failed*, with the reason |

Applies to **every** meter, not only money: spend, tokens, tests passing, components reused, parts
that work. *A zero from a broken pipe reads as good news.*

Our live instance is `cost_usd = 0.0` on the budget branch (`loop.py:550`): the same zero means
*this call was free*, *this call's cost was lost*, and *nobody priced it*. Three claims, one value.

## The override record

From `docs/mined/PASS2-GSTACK-TESTS.md:95`. The argument, quoted in full because it is the whole
design:

> *"a hard cap with no escape valve becomes operationally hostile (legit price changes, longer
> transcripts, new required evals can all blow the cap). An escape valve with no audit becomes
> 'everyone overrides everything and we lose the gate.' This module is the audit half."*

The record: `timestamp · scope · reason · details`, **plus provenance** — CI flag, runner, branch,
commit (8 chars). The environment variable that carries it is a *reason string*, not a boolean:
`..._OVERRIDE_REASON="why this is OK"`.

Two properties:

- **A boolean override is set once and never unset.** A reason string is read at review, and a bad
  reason is visible as a bad reason.
- **The write is best-effort** — *"don't fail the test on audit-write errors."* An observability
  layer must not be able to fail what it observes.

## The usage record: every run, not every successful run

From `docs/mined/PASS2-ECC-SKILLS.md:670`: spend limits enforced **outside the model**, and the
audit log records **refused and halted runs, not only successful ones**.

> Metering that counts only completed builds cannot answer a disputed bill.

This repository already gets half of it right, deliberately: `meterSpend` writes `usage_event` on
success, on cancellation *and* on failure, because *"a cancellation that quietly forgave the cost
would be a hole, and an exploitable one"* (`build.service.ts:296`). The remaining hole is not on
that side — it is that the number handed to it is the lossy one from D2.

Two further gaps worth naming rather than assuming:

- **`Spend.spent_usd` is the only correct running total in the system and is never read.** Four
  references repo-wide, all inside `relay.py`, one of them a string interpolation in an error
  message. The reported total is recomputed from package results instead, which is the lossy path.
  One field on the build result would close it.
- **The reported build cost is not the build's cost.** Layers B and C run model calls inside the
  same stream and track no cost at all, and they take no spend parameter, so they are outside the
  ceiling as well as outside the ledger. This is *coherent* with the estimate, which also prices
  packages only — so the ceiling is not wrong relative to what the user approved — but the ledger
  and the reveal both understate what the workspace really spent
  (`docs/as-built/LAYER-E-BUILD.md` §6).

## The estimate's own record

From `docs/mined/OTHERS-MINED.md:727`: an estimator publishes **its error band, its calibration
corpus, and its expiry condition.**

The third is the one nobody writes. Ours is calibrated against three real runs and says so; what it
does not say is *what would invalidate that calibration*. Something did: the relay changed to price
input as well as output, and the three runs were taken when it did not — so the multiplier that was
tuned against one ratio now covers a different one, and the estimate itself still prices output only
(`docs/next/LAYER-E-BUILD.md` §1.1e).

A publishable expiry condition for a cost model is a short list, and every item is mechanical:

1. the pricing path changes (which halves of the bill are counted);
2. a card's rate changes, or a model id enters the ranking without one;
3. the default pass count or profile changes;
4. the corpus is older than N months.

Any one of them fires a re-calibration, and the estimate says so on its face rather than being
quietly trusted for another year.

## The ratchet, for any constant this skill produces

From `docs/mined/PASS2-GSTACK-TESTS.md:161`, printed inside the failure message rather than kept in
a wiki: when a limit is raised, **update the constant and its derivation comment — reference, date,
value, and what moved it — in the same commit.** The header above their constant reads *"Budget
derivation (re-derive it, do not trust the number)."*

That is the difference between a number with a story and a number someone typed.
