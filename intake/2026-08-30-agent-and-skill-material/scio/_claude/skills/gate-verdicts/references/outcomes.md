# D2 · The outcome vocabulary

Load this when choosing what a gate returns, or when someone proposes a boolean.

## Why two values is never enough

A boolean has one bit and three things to say: *it is right*, *it is wrong*, *I could not tell*.
The third collapses into one of the other two, and it always collapses into the reassuring one.

## Two vocabularies read at source

**`review`, `docs/mined/PASS2-GSTACK-SKILLS.md:199`** — five states for "was this plan item done":

**DONE · PARTIAL · NOT DONE · CHANGED · UNVERIFIABLE**

> CHANGED is *"implemented using a different approach than the plan described, but the same goal is
> achieved"* … *"Be conservative with DONE … Be generous with CHANGED … Be honest with
> UNVERIFIABLE."*

CHANGED is the state that stops a correct build being rejected for taking a different route, and it
is the one most vocabularies omit. Beneath the five sit four *verification modes* — whether a
criterion is DIFF-VERIFIABLE, CROSS-REPO, EXTERNAL-STATE (RLS, DNS, env vars, OAuth allowlists — it
*cannot* be proven from the artefact) or CONTENT-SHAPE. **Every acceptance criterion carries how it
can be checked**, and a criterion whose mode has no channel behind it is `unsupported`, not
`checked`.

**`loop.service.ts`, `docs/mined/PASS2-FOUR-REPOS.md:169`** — four outcomes for an iteration, three
terminal, two carrying a reason the agent wrote as a sentinel tag from a small closed vocabulary:

```
<loop-complete>REASON</loop-complete>  → complete      <loop-blocked>REASON</loop-blocked> → blocked
exit code != 0                          → error         otherwise                           → success
```

**`blocked` is neither success nor error**, and that distinction is what a prose status cannot
carry. The harness parses the tag; nobody reads prose.

## Ours

Scio already has a wider-than-boolean vocabulary and it is in types, not in prose:
`passed / needs_look / failed / blocked`, `Remainder` with a `source`, `app_remainders`,
`app_unjudged`, and `works` requiring **both** every part and nothing app-wide. Two invariants are
already enforced and tested: *an unreadable verdict is a failure, never a pass* (`critique.py:134`),
and *nobody looked ≠ it passed* — recorded as `unjudged` and carried into the reveal
(`loop.py:696`).

**So the work here is not inventing a vocabulary. It is three specific gaps:**

1. `unjudged` must never be counted in a denominator that looks like coverage.
2. "Already satisfied" — a package that needed no change — is a *successful outcome with its own
   name*, not an error and not a silent skip. Today Layer D's assembly match and this outcome are
   modelled as two things (`docs/triage/LAYER-E-TRIAGE.md` row 73, an ADR).
3. Every criterion needs its verification mode recorded, or `unsupported` is indistinguishable from
   `not yet checked`.

## The two rules that make it bite

Both from `review`, quoted at `docs/mined/PASS2-GSTACK-SKILLS.md:199`:

> **Path concreteness.** If a plan item names a *concrete filesystem path* … it MUST be classified
> DONE or NOT DONE based on `[ -f <path> ]`. UNVERIFIABLE is only valid when the path is genuinely
> abstract … or the sibling root is unreachable on this machine. **"I don't want to check" is not
> unreachable.**
>
> **Honesty.** Do NOT classify an item as DONE just because related code shipped. **Code that
> *handles* a deliverable is not the deliverable.** … When in doubt between DONE and UNVERIFIABLE,
> prefer UNVERIFIABLE.

Without the first, UNVERIFIABLE becomes the lazy default. Without the second, DONE does.

## The status column everyone omits

From the eight `*-ops` skills, `docs/mined/PASS2-ECC-SKILLS.md:669`: an honest status table gains a
**what must be true to say this** column.

> *"Do not treat 'present in config' as 'working'."*

That sentence, written by someone doing billing triage in a different repository, is this
repository's `check_tests_present` bug stated as a rule.
