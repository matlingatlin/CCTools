> **SUPERSEDED 2026-09-12, and kept as the record.** This describes the step BEFORE this one:
> three session branches drained into three folders at the root of `matlingatlin/skills-repo`,
> parked outside every check. That repository has since been split three ways —
> `ai-startup-ideas-low-budget/` to `matlingatlin/BusinessIdeas`,
> `godisbutik-app-hemsida/karamellfarbrorn/` to `matlingatlin/Karamellfarbrorn` (with its history,
> via `git subtree split`), and everything else to this repository. Two of the three folders
> therefore no longer exist; `scio-architecture-five-layer/` is here, still parked, still with the
> re-entry condition its own README states.
>
> The CI paragraph below is about `skills-repo`'s workflow and no longer describes this one — the
> trigger filter here covers `library/**` and `docs/**` instead of `.claude/**`. Everything else,
> in particular what was verified about each branch before it was drained, stands as written.

# Branch consolidation — three folders on main, not part of the knowledge base yet

**What this is.** Three folders at the repo root — `scio-architecture-five-layer/`, `ai-startup-ideas-low-budget/`, `godisbutik-app-hemsida/`, one per session branch. Everything here was written on a session branch, is real work, and
would have been lost when the branch was deleted — so it lives on `main` now. **None of it is
indexed, linted, watched or accounted for yet**, and that is deliberate rather than an oversight.

**Why it is not just moved into place.** `knowledge/kb.py` indexes `knowledge/notes/*.md`
(non-recursive) and `knowledge/raw/**/*.md`, and the checks over those paths now require things the
parked material predates — a `raw:` join key in every note's frontmatter, and every raw file
accounted for in `WATCH.tsv` or declared in `watch.py`'s `NEVER_WATCHED`. Dropping the files
straight in would have produced lint errors and a failing `watch.py --offline`, on `main`, which is
the default branch and the only one CI's `schedule:` runs on. **A staging area that is obviously
outside the checks is safer than content that is silently inside them and failing.**

**What absence from this list means.** Only that a branch's content has not been brought over
*yet* — never that the branch was empty. The table below says what is still outstanding and why.

| branch | last commit | brought over | why / why not |
|---|---|---|---|
| `claude/scio-architecture-five-layer-t8t9mp` | 2026-09-11 14:49Z | **yes, verified complete** → `scio-architecture-five-layer/` | idle ~23 h, so a copy cannot go stale under us. **Drained and checked:** all 54 files it added are here and **byte-identical** to the branch, all 30 it modified are covered by the patch, and it added nothing outside `notes/` and `raw/`. Deleting the branch now loses nothing |
| `claude/ai-startup-ideas-low-budget-kmmwty` | 2026-09-12 13:18Z | **yes, verified complete** → `ai-startup-ideas-low-budget/` | brought over on the user's decision after the staleness risk was raised. **Snapshot pinned at `8e6ec9a`**; all 111 added files byte-identical, 7 modified covered by the patch |
| `claude/godisbutik-app-hemsida-s7fkas` | 2026-09-12 12:25Z | **yes, verified complete** → `godisbutik-app-hemsida/` | same. **Snapshot pinned at `9894ff3`**; all 67 added files byte-identical, 1 modified covered by the patch |
| `claude/hej-f7k1d2` | — | **nothing to bring** | 0 commits outside `main`: provably contained, safe to delete |
| `claude/kunskapen-db-tm243q` | merged as PR #1 | **all of it, in `main` proper** | 0 commits outside `main` after the merge, safe to delete |

**Two of the three were copied while they might still be live, and that is a decision rather than an
oversight.** The risk was raised — copying a branch that is still being written to creates a second,
stale version of it, which is the duplicate this consolidation exists to prevent — and the answer was
to bring them over anyway. The mitigation is that **each folder pins the head SHA it was taken from**,
so "is this snapshot current?" is one `git rev-parse` away instead of a worry. Neither branch had moved
between first measuring it and copying it.

**The three folders are not equally ready, and the difference is evidence.**
`scio-architecture-five-layer` holds 44 source files with per-file URL, sha256 and fetch date, and its
notes are missing only the pointer to them — reconstructible mechanically.
`ai-startup-ideas-low-budget` adds **nothing** under `knowledge/raw/`, so its 5 notes are missing the
evidence itself and promoting them means re-fetching sources that are now a week older than the claims
written from them. `godisbutik-app-hemsida` touches the knowledge base not at all. Read each folder's
own README before moving anything.

**Branch deletion is not something this session can do.** A delete-ref push returns **HTTP 403** —
the session's git credential may write commits and not remove refs, and there is no delete-branch
tool in the GitHub MCP server. The two branches marked safe above have to be deleted by a human,
from the PR page or the repository's Branches page.

**A push touching only the three folders runs no CI, and that is correct.** `kb-check.yml`'s path
filter covers the areas `kb.py` indexes — `knowledge/`, `intake/`, `pipeline/`, `.claude/`,
`catalog/` and root `*.md` — and none of the three folders is any of them. Recorded because this
repo has already been bitten by the opposite mistake, where the tell that a check's trigger did not
cover its own input was **a missing run count**. Here the missing run is the design: there is
nothing indexed to check. When material moves out of a folder and into place, the push that moves
it touches `knowledge/` and is checked then.

**This file is the exception, and it is worth being exact about.** It sits at the repo root, so it
matches the filter's `*.md` and `kb.py` indexes it as one of three root documents — a push editing
only `CONSOLIDATION.md` *does* run CI. It is not linted as a note (the lint walks `kind='note'`), so
it carries no frontmatter contract. The first version of this paragraph said no CI runs, which
stopped being true the moment the file moved from `incoming/README.md` to the root.
