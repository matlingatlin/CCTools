# Ablation · `contract-retrieval`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

## The discriminating rule, and why the obvious answer is wrong

§3.5. A retrieval step has **three** honest outcomes, not two:

| Outcome | Means |
|---|---|
| a candidate set | the index ran and these passed |
| `[]` | it ran, and genuinely found nothing — a real miss, worth recording |
| `null` | it did **not** run — unavailable, timed out, scope unresolvable — degrade, and never record a miss |

And a second refusal: **never widen when the scope cannot be resolved.** *"An unscoped search
pulls corpora that would be mislabeled as 'related decisions'… Widening on failure is failing
open."*

Both rules invert the instinct a competent engineer brings. The instinct is *fail open, keep the
caller simple*: return an empty list on failure so the return type never changes, and search
everything when you cannot tell what to search. Both are defensible general engineering, and both
are exactly what the skill forbids — the first makes an outage indistinguishable from a clean
miss rate forever, the second turns a narrowing stage into a source of wrong matches.

The question was written to reward that instinct: it says *"I'd rather callers didn't have to
handle special cases,"* which is a direct invitation to collapse `null` into `[]`.

## The question

> Our component lookup is getting slow so we're putting a fuzzy search step in front of it to
> narrow the candidates. Two things I'm unsure about: what it should return when the search
> service is unavailable, and what it should do when it can't work out which part of the catalog
> to search. I'd rather callers didn't have to handle special cases. Four bullets max.

No skill, no file, no term unique to the skill. "Fuzzy search", "narrow the candidates" are the
words a person would type.

## Control answer

Verbatim.

> - **Unavailable → fail open, not closed:** return the full unfiltered candidate set (or skip
>   straight to the existing slow lookup) rather than an error or empty list — callers get a
>   correct-but-slow result instead of a code path they must special-case.
> - **Ambiguous scope → same move, widen instead of narrow:** if it can't tell which part of the
>   catalog to search, treat that as "search everything" and return the broader/unfiltered set
>   rather than guessing or erroring.
> - **One contract either way:** the method's return type never changes shape (always "candidates
>   to feed the existing lookup"), so success and degraded-mode returns are indistinguishable to
>   the caller — no exceptions, no null, no separate "unavailable" flag to check.
> - **Push the cost, not the decision, downstream:** degraded cases just mean the existing lookup
>   does more work than usual; correctness is preserved and callers stay oblivious that fuzzy
>   search was skipped.

## Treatment answer

Verbatim.

> - **Unavailable service → `null`, never `[]`.** `[]` means "it ran and found nothing" (a genuine
>   miss, worth recording); `null` means "it didn't run." Conflating them makes an outage look
>   like a clean miss rate forever.
>
> - **On `null`, the caller degrades to the exact full-catalog lookup automatically** — retrieval
>   is an optimization, never a dependency, so callers don't need an unavailable-service branch at
>   all.
>
> - **Can't resolve which part of the catalog to search → refuse, don't widen.** Searching
>   unscoped when scope is unresolvable pulls in unrelated candidates that get mislabeled as
>   matches; that's failing open, not failing safe.
>
> - **A refusal also returns `null`, not `[]`**, and routes through the same fallback path as
>   "service unavailable" — so callers have exactly one special case to not-handle (fall back to
>   exact search) and it's already handled for them.

## Comparison

On mechanism, not wording.

| Mechanism | Control | Treatment |
|---|---|---|
| Return value when the service is down | full unfiltered set or empty — **explicitly "no null"** | **`null`**, typed distinctly from `[]` |
| "Ran and found nothing" vs "did not run" | **deliberately conflated** — *"indistinguishable to the caller"* is stated as the goal | **kept distinct**, with the consequence named: a miss ledger that never sees the outage |
| Unresolvable scope | **widen** — *"treat that as search everything"* | **refuse** — widening named as failing open |
| Fall back to the exact lookup | yes | yes |
| Retrieval may never decide | implied (exact lookup still runs) | implied, same |

Three of four control bullets are the prohibited answer, and the third one states the prohibition
as a design principle. The one point of agreement — fall back to the slow exact path — is real and
should be said: the control did not propose letting the approximate stage decide.

## Verdict

**Changed the outcome.** The control produced a system in which an outage is silently recorded as
a clean miss and an unresolvable scope produces wrong matches. The treatment produced the opposite
on both, by the skill's own mechanism (`null` vs `[]`; refuse vs widen), and gave the reason rather
than the rule. This is not a rewording of the same conclusion — the two answers disagree.

## Limits of this measurement

n=1 per arm, unblinded, one question, one day. No repeat runs, so run-to-run variance is unmeasured
and a single sample cannot separate the skill from sampling luck.

Two confounds, and both apply to every file in this series:

1. **`graphify` is installed at account level** (`/root/.claude/skills/graphify/`) and loads in
   both arms. "No project skills" is not "no skills"; the control also carries the user's global
   `CLAUDE.md`.
2. **The control directory is not a copy of the treatment directory minus skills.** It holds
   `CLAUDE.md` and `docs/as-built/` only; the treatment is the live `scio` repo, which also holds
   `docs/next/`, `docs/mined/`, `docs/triage/`, `scripts/` and `graphify-out/`. The treatment arm
   could in principle have read repo prose rather than the skill. Here that is weak: the
   `null`/`[]` distinction and the refuse-don't-widen rule are stated in `SKILL.md` itself, and the
   answer used the skill's own framing (*"never a dependency"*), but the confound is not eliminated
   by this design.
