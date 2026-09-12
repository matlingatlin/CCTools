# ADR-0001 · The code graph is standard, in every repo and every generated app

**Status:** Accepted
**Date:** 2026-08-26
**Layer:** cross-cutting
**Supersedes / relates to:** none. First decision of the rebuild.

## Context

`docs/next/` names *retrieval versus packing* as a cross-cutting axis — where a layer sends context
it could have queried instead. Until today it was a principle in prose, and prose that nobody
executes is the failure this project has documented in the predecessor five times over: an honest
signal computed and then dropped.

We were not practising it. Whole documents were read where a query would have answered better, and
the graph was queried perhaps twice across a full day of work.

Measured 2026-08-26, on the real question *what does the intake gate check, and what touches it*:

| Route | Cost |
|---|---|
| Read `LAYER-A-INTAKE.md` | ≈ **2,318 tokens** |
| `graphify explain "is_buildable"` | ≈ **546 tokens** |

Four times cheaper, and the retrieval is *better*: exact file and line, and all 26 call sites,
where the document gives prose about the same thing.

Cost of keeping the graph current, measured the same day:

| | |
|---|---|
| Full build, 5,955 files / 1.34M lines | **9.5 s** |
| Model calls | **zero** — `graphify update` is AST extraction |
| What a commit itself pays | **222 ms**, because the hook forks a background rebuild |

`graphifyy` 0.9.50 is installed; `graphify hook` exists and works, though it is absent from the
tool's own top-level help.

## Decision

**Every repo in this project carries a current code graph, and keeping it current is mechanical
rather than remembered.** Three mechanisms, in this order:

1. **`SessionStart` hook** — `scripts/ensure-graph.sh`, shipped in the plugin via
   `hooks/hooks.json`. On session start it builds the graph if absent and installs the git
   `post-commit` hook if missing. It runs outside the model's context: **zero tokens**. Every unmet
   precondition exits 0, so it can never fail a session.
2. **git `post-commit` hook** — `graphify hook install`. Keeps the graph current per commit, forked
   to the background.
3. **Generated applications get the same at scaffold time.** An app Scio produces is a repo the
   user owns and will keep working in; shipping it without a graph withholds the cheapest tool we
   have. This binds the foundation package in the build plan.

**The order is fixed and is not cosmetic.** `graphify hook` rebuilds only the files in a commit, so
installing it before a full build yields a graph of recent commits and nothing else — which looks
complete and is not. Measured: hook alone produced 3 nodes and 2 edges on a two-file repo; a full
build immediately after produced 6 and 8, the missing half being a file nobody had touched since.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| **Do nothing — keep it as a rule in the `run` skill** | It was already a rule, and we did not follow it for an entire day. A rule that depends on someone reading it is the failure mode this repo exists to document |
| **A `PostToolUse` hook on `Bash(git commit *)`** | Fires only when *Claude* commits, in-session, and misses every human commit. The git hook catches both |
| **Rebuild in the foreground for correctness** | A hook that makes every commit wait 9.5 s is disabled within a week. The background fork is why this survives contact with daily use |
| **A vector-database code search instead** | Adds a service and approximate matching to replace something exact that costs nothing. Revisit only if graph retrieval measurably fails |

## Consequences

**What this buys.** Retrieval becomes the cheap default rather than the disciplined choice. The
graph is never stale enough to mislead. Generated apps inherit it, so the ownership promise in
ADR-0001 of the predecessor extends to the tooling and not just the source.

**What it costs.** A dependency on `graphifyy` in every repo, and one more thing that can drift —
the vendored skill already drifted from the package once. Roughly 10 s once per repo, and 222 ms
per commit.

**What it forecloses.** Little. The hook is removable with `graphify hook uninstall` and the
`SessionStart` script is one file.

**Known limits, stated rather than discovered later.** `update` re-extracts **code**. Documents,
papers and images need semantic extraction, which needs a model — so this repo's own prose corpus
does **not** stay current under this hook and must be rebuilt deliberately. And the mechanisms
above keep the graph *fresh*; they cannot force a session to *query* it instead of reading files.
That half remains a rule, and it is the half we already failed once.

## How we will know it was wrong

- A session queries the graph and gets a wrong answer that a file read would have got right.
- The 222 ms commit cost grows enough that someone disables the hook.
- Graph retrieval measurably fails to answer the questions build sessions actually ask — in which
  case the vector-search alternative above comes back with evidence behind it.
- Nobody queries the graph anyway, which would mean the freshness mechanism solved the wrong half.
  **This is the most likely failure**, and it is currently unmeasured: nothing counts graph queries.
