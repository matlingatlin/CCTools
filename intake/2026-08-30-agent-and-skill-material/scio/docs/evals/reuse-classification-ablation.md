# Ablation · `reuse-classification`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

## The discriminating rule, and why the obvious answer is wrong

Identity is split across three mechanisms and only one of them decides
(`library/categories.py`, `library/identity.py`):

- **category** — narrows the search. **Never decides.**
- **hashtags** — labels for a person browsing. **Never a match key.**
- **contract** — operations, routes and files with the project's own entity words removed.
  **Decides**, by exact set relation.

The consequence, stated in the skill's Eval case 2: a project that names its operations
`reserve_table` / `release_table` keeps its own vocabulary and **the miss stays visible**. *"Any
change that makes this silently match is wrong."* The temptation, once the miss rate is known, is
to make the generalisation cleverer until the miss disappears — *"which trades a visible miss for
an invisible wrong match."*

The obvious answer is similarity scoring: fuzzy-match names, compare prop signatures, diff rendered
output, weight the signals, rank the candidates. Every one of those is a competent instinct for
"are these the same component", and every one of them makes identity probabilistic — which is the
one property this library is built to refuse. The question was written so that "near-duplicates"
and "really the same" both point at a threshold.

## The question

> Our shared component library is filling up with near-duplicates. I want a script that flags when
> two entries are really the same component, so we can merge them. How should it decide that two
> entries are the same? Four bullets max.

No skill, no file, no unique term. "Near-duplicates" is the bait.

## Control answer

Verbatim, including the closing recommendation.

> This is exploratory — here's my take, not a build:
>
> - **Structural fingerprint**: normalize and diff the prop/API surface (names, types,
>   required/optional) — two entries with near-identical prop signatures are the strongest signal,
>   since UI components converge in behavior before they converge in name.
> - **Rendered/visual output**: for components with stories or snapshots, compare rendered DOM or a
>   visual diff at matching prop values — same markup/style output despite different code is a hard
>   tell.
> - **Name and usage-site similarity**: fuzzy-match names/aliases and cross-reference where each is
>   imported — components serving the same call sites in the codebase are candidates even if their
>   code differs.
> - **Source similarity as a tiebreaker only**: token/AST similarity on implementation catches
>   copy-paste forks, but rank it last — it's the noisiest signal (two components can look similar
>   in code and behave differently, or vice versa).
>
> Recommendation: weight structural + usage-site signals highest and treat visual/source similarity
> as supporting evidence, then have the script output a ranked candidate list for human merge
> decisions rather than auto-merging.

## Treatment answer

Verbatim.

> Based on Scio's own identity model (`library/identity.py`, `categories.py`) and the
> faceted-classification lineage it descends from:
>
> - **Match on contract, not on category or hashtags.** Category only narrows the search space and
>   hashtags are free-text for browsing — neither is a reliable identity key. Compute
>   `Contract.key` for each entry (operations, routes, files with the project's own entity words
>   substituted out) and compare *that*.
> - **Generalize entity names before comparing, but only entity names.** `bookings`/`appointments`
>   should collapse to one contract if their operations, routes, and files otherwise match. Don't
>   let the substitution reach further than the entity form — that's where false merges hide.
> - **Treat a near-exact contract as a flagged near-miss, never an auto-merge.** If
>   operations/routes/files differ by a small set-distance (e.g. `reserve_table` vs `book_table`
>   under the same entity), surface it for a human to confirm — silently "fixing" the mismatch
>   trades a visible miss for an invisible wrong merge, which defeats the point of the check.
> - **Log what didn't match and why**, so you can tell scattering (same category, ever-growing
>   distinct contract keys, low vocabulary-miss — a schema problem) apart from a vocabulary gap
>   (high vocabulary-miss rate — an aliasing problem). Those need opposite fixes, and conflating
>   them will misdirect the cleanup.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| What decides identity | **a weighted blend of four similarity signals** | **exact equality of one derived key** (`Contract.key`) |
| Names | fuzzy-matched, a ranked signal | substituted out — entity forms only, and *"don't let the substitution reach further"* |
| Rendered output / visual diff | *"a hard tell"* | absent — not an identity mechanism |
| Prop/API signature | the strongest signal | absent as such; operations/routes/files are the key |
| Near-miss | folded into the score, moves an entry up or down the ranking | **a separate, named outcome** — flagged, never merged; the visible miss is the point |
| Diagnosis of *why* the library is duplicating | none | two numbers that separate a too-fine contract from unaliased naming — *"these need opposite work"* |
| Human confirms the merge | yes | yes |

**Zero of four control bullets overlap on mechanism.** The single agreement is procedural — both
refuse to auto-merge and hand the decision to a person — and that is `CLAUDE.md`'s caution showing
up in the control too, not the skill's contribution.

The sharpest split is what a near-miss *is*. For the control it is a low score, which is a
quantity. For the treatment it is a distinct outcome that must stay visible, because the failure
being guarded against is not a missed merge — it is a wrong one that nobody can see afterwards.

## Verdict

**Changed the outcome.** The control designed exactly the similarity scorer the skill exists to
refuse, and its top-ranked signal (prop-signature similarity) is one the skill excludes from
identity entirely. The treatment produced a decidable rule plus a diagnostic that tells you which
of two opposite fixes the library actually needs. Different mechanism, different artefact, not a
rephrasing.

## Limits of this measurement

n=1 per arm, unblinded, one question. No repeats, so variance is unmeasured.

One asymmetry worth naming beyond the shared confounds: the control was not told the library is
Scio's, so it reasonably assumed a React component library and answered for that. Some of the gap
is domain knowledge the skill carries, not judgement the skill supplies — though the identity
principle (exact key, never a score) is domain-independent and the control did not reach for it.

The two confounds that apply to every file in this series:

1. **`graphify` is installed at account level** (`/root/.claude/skills/graphify/`) and loads in
   both arms. "No project skills" is not "no skills"; the control also carries the user's global
   `CLAUDE.md`.
2. **The control directory is not the treatment directory minus skills.** It holds `CLAUDE.md` and
   `docs/as-built/` only; the treatment is the live `scio` repo, which also holds `docs/next/`,
   `docs/mined/`, `docs/triage/`, `scripts/` and `graphify-out/`.
