---
name: graph-guard
layer: build-process
phase: build-time
status: written
description: Keep the code graph current and catch layer-boundary drift after a commit. Use after committing code, when setting up the post-commit hook, when a cross-layer dependency needs checking, or when the architecture map has gone stale. Runs deterministic AST extraction only — no model calls, no cost.
---

# graph-guard

Structure rots quietly. A single import from the build layer into intake is one line in a
diff nobody flags, and six months later the layers are a suggestion.

This skill keeps the graph current and **fails loudly when a commit crosses a boundary it
should not**.

## The design, and why

**It guards; it does not document.** Regenerating a document on every commit produces a file
that changes constantly and is therefore never read. A guard that fires rarely gets read
every time it fires.

**It never commits the graph.** `graph.json` is ~5.5 MB and derived. Committing it per commit
turns a hundred commits into half a gigabyte of history for a file that can be rebuilt in
seconds. Regenerate on demand; commit it only at a release, or when the structure has
materially changed and someone wants the snapshot pinned.

**It runs no model.** Code goes through tree-sitter AST — deterministic, free, and it cannot
fail on a rate limit or a missing key. Semantic extraction over documents costs tokens and
belongs in CI or a manual run, never in a hook that fires on every commit.

**Cheap exit first.** No code files changed → stop before doing anything.

## What it does

### 1 · What changed

```bash
git diff --name-only HEAD~1 HEAD | grep -E '\.(py|ts|tsx|sql)$' || exit 0
```

No matches means nothing structural moved. Stop here — most commits stop here.

### 2 · Re-extract only those files

```bash
python3 -c "
from graphify.extract import extract
from pathlib import Path
import json, sys
files = [Path(p) for p in sys.argv[1:] if Path(p).exists()]
result = extract(files)
Path('.graphify_delta.json').write_text(json.dumps(result))
print(f'{len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges from {len(files)} files')
" $CHANGED_FILES
```

Incremental. A one-file commit re-parses one file.

### 3 · Diff against the previous graph

`graphify.analyze.graph_diff` gives new nodes, new edges, and a summary. That summary — not
the graph — is what a human wants after a commit.

### 4 · Check the layer rules

This is the part worth having. Declare which layer each path belongs to, and which
cross-layer edges are permitted. Anything else is a finding.

```
A intake      → may use: G, shared execution machinery
B understanding → may use: A
C build plan  → may use: B, E primitives
D library     → may use: B, C (leaf types only), E
E build       → may use: C, D
F design      → may use: E, G
G cross-cut   → may use: nothing above it
```

A new edge outside that table is reported with both endpoints and the commit that introduced
it. It is **not** auto-rejected — some are legitimate and the table is what should change.
The point is that the decision gets made by a person, once, rather than by nobody, silently.

### 5 · Report

Print to the terminal. Append one line per structural change to `docs/graph-log.md`:

```
2026-08-26  a1b2c3d  +4 nodes +6 edges   ok
2026-08-26  d4e5f6a  +1 node  +2 edges   ⚠ new edge A→E (intake/service.py → builder/loop.py)
```

An append-only log stays readable. A regenerated document does not.

## Installing the hook

Upstream ships one:

```bash
graphify hook install     # appends to any existing post-commit hook, does not replace it
graphify hook status
graphify hook uninstall
```

Use it for the AST rebuild. The layer check above runs after it.

### Run a full build first, or the graph lies

**Verified end to end on 2026-08-26; these are measured numbers, not estimates.**

The hook rebuilds **only the files in the commit**. On a fresh install that produces a graph
containing your recent commits and nothing else — which looks complete and is not. Measured on a
two-file test repo: the hook alone produced **3 nodes and 2 edges**; `graphify update .`
immediately afterwards produced **6 nodes and 8 edges**. The missing half was a whole file that
simply had not been touched since the hook went in, along with the import edge between the two.

That failure has this project's signature: a signal that looks trustworthy and is not. A partial
graph does not announce itself — every query against it returns confidently and wrongly.

**So the order is fixed:**

```bash
graphify update .          # full build, once, before anything relies on the graph
graphify hook install      # then the hook keeps it current
```

`graphify hook status` reports `post-commit`, `post-checkout` and the merge driver separately.

### What it costs, measured

| | |
|---|---|
| Full build, 2-file repo | **0.29 s** |
| Full build, **5,955 files / 1.34M lines** | **9.5 s** |
| Model calls | **zero** — `update` is AST extraction, no LLM |
| Effect on the commit itself | **222 ms**, because the hook forks a background rebuild and returns |

The background fork is the detail that decides whether this survives. A hook that made every
commit wait nine seconds would be disabled within a week; one that costs a fifth of a second and
finishes behind you will not be noticed. Do not "improve" it into a foreground job.

**One caveat the tool states itself:** `update` re-extracts *code*. Documents, papers and images
need semantic extraction, which does need a model — so a corpus of prose does not stay current
under this hook. For a documents corpus, rebuild deliberately, not on every commit.

**Post-commit cannot block a commit.** That is the right trade for a fast local loop — the
guard reports, and CI is where a boundary violation should actually fail a build. If you want
it to block locally, move it to `pre-push`, never `pre-commit`: blocking every commit on a
graph rebuild is how a guard gets disabled.

## Two things that will bite

**The vendored skill drifts from the installed package.** `.claude/skills/graphify/SKILL.md`
is a pinned copy of upstream's file. It was already found calling `check_semantic_cache`
expecting three return values against an installed version returning four. Pin the graphify
version in the setup script, and re-fetch the vendored skill deliberately rather than
assuming it matches.

**SQL needs an extra.** Plain `graphifyy` silently skips `.sql` files — the first AST pass
over hello-world dropped all twelve migrations with only a warning. Install
`graphifyy[sql]` or the data model is invisible to the graph.

## When not to use this

- Before there is code. An empty repo has no structure to guard.
- For documents. Semantic extraction costs tokens; run it deliberately, not per commit.
- As a substitute for review. This catches *structural* drift. It says nothing about whether
  the code is any good.
