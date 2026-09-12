---
name: repo-map
description: "Use when an LLM needs the most relevant slice of a large codebase packed into a fixed token budget — building an aider-style repository map that extracts symbol tags with tree-sitter, ranks files and definitions by PageRank over the reference graph, and emits a compact tree of the top signatures. Triggers on 'what files matter for this change', seeding an agent's context before an edit, summarizing an unfamiliar repo into a signature outline, or when full-file dumps blow the context window. NOT interactive graph querying/tracing for human onboarding (graphify-harvest), NOT measuring which loaded harness components eat context (context-budget), and NOT digesting prose documents (deep-reading) — this ranks and budget-packs code symbols to feed a model. NOT for finding functions that serve the same INTENT under different names (use semantic-duplicate-sweep)."
---

# Repo Map

Produce a token-budgeted, PageRank-ranked outline of a codebase so an LLM sees the
highest-signal files and symbols without ingesting every file.

## When to use
- Seeding an agent's context before it edits an unfamiliar or large repo.
- Answering "which files/symbols matter for task X" within a hard token budget.
- Turning a repo into a compact signature outline (defs, not bodies).

## When NOT to use
- A human wants to interactively query/trace a graph → graphify-harvest.
- You are auditing harness/context-window overhead → context-budget.
- The source is prose, not code → deep-reading.

## Steps
1. **Scope.** Collect candidate source files (respect `.gitignore`, skip vendored,
   generated, and binary files). Note the target token budget (default ~1k–8k).
2. **Tag.** Parse each file with a tree-sitter grammar for its language. Extract two
   tag kinds per symbol: `def` (function/class/method/const definitions) and `ref`
   (identifier uses). Record file, line, name, and kind.
3. **Build the graph.** Make a directed multigraph: nodes = files. For every symbol,
   add an edge from each file that *references* it to each file that *defines* it,
   weighted by reference count and by identifier rarity (rare names weigh more).
4. **Rank.** Run PageRank over the graph. **A disconnected graph does not break this — checked
   2026-09-12, and the expected failure did not occur.** A repo whose services talk over HTTP rather
   than imports yields a *forest*, and the obvious worry is that a small component gets starved of rank
   mass and vanishes from a budget-packed map. It does not: PageRank's teleport term distributes mass
   to every node regardless of connectivity, so a component's share tracks its size. Measured on a
   4,499-node graph in 48 components — the second island holds **24%** of the nodes and took
   **11 of the global top-40 (27.5%)**, slightly *over* its share. No per-component ranking needed.
   Recorded as a negative result because the concern was reasonable and the mechanism that would have
   caused it is absent by construction. Optionally bias the personalization vector
   toward files the user mentioned or files currently open/changed, so the map centers
   on the task. Distribute each file's rank across its defined symbols by inbound weight.
5. **Select within budget.** Greedily add the highest-ranked symbols, newest to a file
   creating a small header cost. Estimate tokens per added line; stop before the budget
   is exceeded. Binary-search the rank cutoff if you must hit the budget tightly.
6. **Render.** Emit a tree grouped by file path. Under each file list only the selected
   `def` signature lines (name + params/return, no bodies), with elision markers (`⋮`)
   between non-adjacent lines. Prefix with the token count used.
7. **Cache & refresh.** Key tags by file path + content hash so unchanged files reuse
   prior tags. Recompute ranks only when the file set or budget changes.

## Rules
- Method only: no network calls, no package installs, no auto-run hooks. If a
  tree-sitter grammar is unavailable, fall back to a regex/heuristic def-extractor and
  say so — never silently skip a language.
- The budget is hard. Never exceed it; prefer fewer symbols over truncated ones.
- Signatures only — never emit function bodies or file contents into the map.
- Rank is relevance, not importance-in-general: re-bias personalization per task rather
  than reusing a global ranking.
- Deterministic output: fixed tie-breaks (rank, then path, then line) so the same repo +
  budget yields the same map.
- Report what was dropped (file count, symbol count) so the caller knows the map is partial.
