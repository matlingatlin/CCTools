# Ablation · `graph-guard`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

## The confound, and it matters most here

**`graphify` is installed at account level (`/root/.claude/skills/graphify/`) and loads in both arms.**
For every other skill in this pass that is a footnote. For `graph-guard` it is the central question,
because `graph-guard` is built *on top of* graphify's hook.

So I read the upstream skill before running anything. `/root/.claude/skills/graphify/references/hooks.md`
documents `graphify hook install` / `uninstall` / `status`, says the hook re-extracts only the files in
the commit, and says it appends to an existing post-commit hook rather than replacing it. It says
**nothing** about running a full build first, nothing about post-commit being unable to block, nothing
about pre-push versus pre-commit, nothing about a layer table, and nothing about `graphifyy[sql]`.

The confound therefore supplies **the tool** to both arms and **none of the four discriminating rules**.
That is the cleanest version of this confound available, and it still means: a positive result here shows
`graph-guard` beats *graphify-plus-general-instinct*, not that it beats nothing.

**Second confound:** the treatment directory carries `docs/next/`, `docs/mined/`, `scripts/` and `scio.db`
that the control does not; `CLAUDE.md` and `docs/as-built/` are byte-identical.

## The discriminating rule, and why the obvious answer is wrong

`graph-guard` § *Run a full build first, or the graph lies*:

> The hook rebuilds **only the files in the commit**. On a fresh install that produces a graph containing
> your recent commits and nothing else — which looks complete and is not. Measured on a two-file test repo:
> the hook alone produced **3 nodes and 2 edges**; `graphify update .` immediately afterwards produced
> **6 nodes and 8 edges**. […] A partial graph does not announce itself — every query against it returns
> confidently and wrongly.
>
> **So the order is fixed:** `graphify update .` → then `graphify hook install`.

The obvious answer is *install the hook and let it fill in as you commit*, which is how every incremental
tool is set up and is wrong here for a reason nothing in the setup reveals. Two more rules of the same
shape sit alongside it:

- **Post-commit cannot block a commit.** *"If you want it to block locally, move it to `pre-push`, never
  `pre-commit`: blocking every commit on a graph rebuild is how a guard gets disabled."* The obvious
  answer — reach for pre-commit so the violation stops the commit — is both impossible in a post-commit
  hook and wrong as a design.
- **A cross-boundary edge is reported, not rejected.** *"Some are legitimate and the table is what should
  change. The point is that the decision gets made by a person, once, rather than by nobody, silently."*

## The question

> *I want a git hook that keeps a map of our codebase up to date after each commit, so we catch imports
> that cross module boundaries we do not want crossed. What should I set up? Four bullets max.*

Names no skill, no file, no term unique to the skill. *"Keeps a map up to date after each commit"* points
straight at incremental-from-empty, which is the trap.

## Control answer

Verbatim, closing offer elided:

> Given this repo already has graphify producing `docs/as-built/graph/graph.json`, the hook should just
> reuse that pipeline rather than invent a new grapher:
>
> - **post-commit hook** (`.git/hooks/post-commit`, or better, a tracked script wired via
>   `core.hooksPath`/husky so it's shared) that re-runs the graphify skill's generator against the changed
>   paths and rewrites `graph.json`.
> - **A boundary rules file** (e.g. `docs/decisions/module-boundaries.json` or an ADR) listing forbidden
>   import edges between modules/layers — this is the part you have to author by hand, since no tool can
>   infer "we don't want" from the graph alone.
> - **A checker script** that diffs the fresh graph's import edges against that rules file and exits
>   non-zero on a violation, so the hook can fail the commit (or just warn — decide which).
> - **Fast-path guard**: skip/only-run on files touched in the commit (via `git diff --cached --name-only`
>   pre-commit, or `git diff HEAD~1` post-commit) so the hook stays fast; full-graph rebuilds belong in CI,
>   not every commit.

## Treatment answer

Verbatim:

> Here's the setup, per the graph-guard skill already in this repo:
>
> - **Full build first**: `graphify update .` once, before the hook exists — the hook only rebuilds files
>   touched by each commit, so without a baseline the graph looks complete while missing everything
>   untouched since install.
> - **Install the hook**: `graphify hook install` (appends a post-commit hook, forks the rebuild to
>   background — ~220ms added to the commit, not the 9.5s of a full build). Post-commit can't block a
>   commit, which is correct here: block on `pre-push` instead if you want boundary violations to actually
>   stop something locally; never on `pre-commit`.
> - **Declare the layer table and diff against it**: define which layer each path belongs to and which
>   cross-layer imports are allowed (e.g. `A intake → may use G`), then after each incremental re-extract,
>   diff new edges against that table. A disallowed edge isn't auto-rejected — it's reported with both
>   endpoints and the commit, appended to `docs/graph-log.md`, so a person decides once instead of nobody
>   deciding ever.
> - **Watch two gotchas**: install `graphifyy[sql]` or migrations get silently dropped from the graph, and
>   this only handles code (AST, zero model calls) — a docs/papers corpus needs deliberate semantic
>   rebuilds, not this hook.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Reuse graphify rather than write a grapher | **yes** | yes |
| Uses the shipped `graphify hook install` | **no** — hand-rolls `.git/hooks/post-commit` + husky | **yes** |
| **Full build before the hook exists** | **no — and argues the opposite**: "full-graph rebuilds belong in CI, not every commit" | **yes**, with the failure it prevents: "looks complete while missing everything untouched since install" |
| Hand-authored boundary/layer table | **yes**, and makes the good point that no tool can infer intent | yes, with the concrete A→G table |
| Diff new edges against the table | yes | yes |
| **Post-commit cannot fail a commit** | **no — asserts it can**: "exits non-zero on a violation, so the hook can fail the commit" | **yes**, and gives the correct escalation: `pre-push`, never `pre-commit` |
| **Report, do not auto-reject** | **no** — offers "fail the commit (or just warn — decide which)" | **yes**, with the reason: legitimate edges exist and the table is what should change |
| Append-only log rather than a regenerated document | no | **yes** — `docs/graph-log.md` |
| Cost is stated and measured | no | **yes** — 222 ms on the commit, 9.5 s full build |
| **`graphifyy[sql]` or migrations vanish silently** | **no** | **yes** |
| Documents need semantic extraction, not this hook | no | **yes** |

## Verdict

**Changed the outcome**, and it is the strongest of the five in this pass.

Two of the control's four bullets are wrong in ways that would ship:

1. *"Full-graph rebuilds belong in CI, not every commit"* is correct about steady state and skips the
   one-time full build entirely. Following it produces a graph that contains only what has been committed
   since install — the exact failure `graph-guard` measured (3 nodes/2 edges versus 6 nodes/8 edges on a
   two-file repo). It looks complete. Every boundary query against it then returns confidently and wrongly,
   which is the same failure signature as this project's other measured defects.
2. *"exits non-zero on a violation, so the hook can fail the commit"* is not possible. A post-commit hook's
   exit status does not affect the commit; it has already happened. The control proposed a guard that
   silently does nothing, and offered no alternative escalation.

The treatment got both right, added the report-don't-reject design with its reason, the append-only log,
the measured cost that decides whether the hook survives contact with a developer, and the `graphifyy[sql]`
extra without which the twelve migrations in the predecessor were invisible to the first AST pass.

**Reading it against the confound:** the control had `graphify` loaded and still hand-rolled a hook rather
than reaching for `graphify hook install`, so the shared skill did not fire in the control arm on this
question. The delta measured here is therefore mostly attributable to `graph-guard` itself — but the honest
statement is that this compares *`graph-guard` present* against *`graphify` present and not firing*, not
against a bare model.

## Limits of this measurement

n=1 per arm, unblinded, one question, one grader who wrote the question after reading the skill. The
treatment arm carries the whole `scio` corpus as well as the 27 skills. The two control errors are graded
against `graph-guard`'s own measurements — I re-derived the post-commit-cannot-block claim from git's
documented behaviour, but I did **not** re-run the 3-nodes-versus-6-nodes experiment, so that number is
this skill's claim about itself and is inherited here rather than verified. A rerun could land differently;
one observation is one observation.
