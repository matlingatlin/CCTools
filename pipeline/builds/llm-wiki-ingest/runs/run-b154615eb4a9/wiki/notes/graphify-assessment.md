---
title: Graphify — assessment for the knowledge base
sources:
  - url: https://github.com/Graphify-Labs/graphify
    fetched: 2026-08-27
  - url: https://stevescargall.com/blog/2026/05/graphify--memmachine-79-token-reduction-zero-vector-database/
    fetched: 2026-08-27
  - url: https://pypi.org/project/graphifyy/
    fetched: 2026-08-27
status: verified
tags: [graphify, knowledge-graph, tokens, tooling, decision]
related: ["[[llm-wiki-pattern]]", "[[claude-code-extension-layer]]", "[[claude-code-ecosystem-plugins]]", "[[mcp]]", "[[temporal-kg-agent-memory]]", "[[third-party-landscape]]", "[[token-economy-playbook]]"]
---

# Graphify — assessment

**Graphify** (`github.com/Graphify-Labs/graphify` — canonical, formerly `safishamsi/graphify`;
PyPI `graphifyy`, MIT; YC S26) — NOT Graphiti/Zep.
An on-device tool that turns a **codebase** into a queryable knowledge graph an agent
traverses instead of re-reading files. Decision: **pilot on harvested source repos
(code-only); do NOT point it at our own markdown/JSON KB.**

## How it works

- **Code** parsed locally and deterministically via **tree-sitter AST** (~37 grammars) —
  no LLM, nothing leaves the machine. This is the genuinely free part.
- **Docs/PDF/media** use an **LLM semantic pass** (+ Whisper for audio/video). So the
  "no-LLM/on-device" claim is **true for code only**.
- **Graph:** nodes = functions/classes/modules + "rationale nodes" (`# WHY:` comments);
  "god nodes" (most-connected) and Leiden communities. Edge types: `calls`, `imports`,
  `inherits`, `uses`, `references`, `depends_on`, each tagged **EXTRACTED** or **INFERRED**.
  **No embeddings, no vector store** — a real graph you traverse.
- **Outputs (git-friendly files):** `graph.json` (queryable graph), `GRAPH_REPORT.md`
  (highlights + suggested questions), `graph.html` (viz; unwieldy >5000 nodes). Optional
  Cypher / GraphML / **Obsidian-vault** exports.

## Running it & fit with our ephemeral + git-only model

`uv tool install graphifyy` → `graphify extract ./path [--no-viz]` → query with
`graphify query/path/explain`, or serve as an MCP stdio server, or use as a Claude
Code skill (`/graphify .`, with a git post-commit hook for incremental rebuilds).

**The standout advantage, confirmed:** the artifact is three static files with **no
database, no vector store, no per-session build**. Commit `graph.json` +
`GRAPH_REPORT.md` to git and a graph built in one container survives into the next —
exactly our constraint, and the clean win over DB-backed tools (Graphiti/Zep) that need
a running datastore an ephemeral container reclaims. Caveat: the *binary* doesn't
persist — a fresh session re-runs `uv tool install graphifyy` (fast, no LLM); the *data*
persists in git.

## Token-reduction claims (70× / 71.5× / 79×)

- **71.5×** = repo's own headline (vendor claim, no published methodology).
- **79.6×** = the one with transparent independent methodology (Scargall, on the
  MemMachine repo, 7,441 nodes): baseline naive scan ~496k tokens → graph query ~6.2k
  tokens/question. **Variance is large and honest:** local queries 227–713×, broad
  traversal only 48–62×.
- **Where it comes from:** one-time build → each question returns a scoped subgraph
  (few k tokens) instead of grepping/re-reading hundreds of files. Amortization.
- **Honest costs:** the **semantic (doc) pass** cost ~1.4M input tokens on MemMachine →
  **payback ≈240 queries**; below that it costs *more* than reading files.
  **Code-only AST extraction is ~0 LLM cost** — so run code-only to collapse break-even.
  Staleness (snapshot; doc changes need manual `--update`); "only as good as the graph"
  (weak on dynamic dispatch/metaprogramming/cross-language).

## Fit for our two use cases

**(a) Navigating harvested SOURCE repos (ECC, superpowers): strong fit — the intended
sweet spot.** Large, code-heavy, hundreds of components — exactly the 79× benchmark
shape. Useful for factory triage/discovery ("what calls what", "god nodes", Leiden
subsystems). Run **code-only** so the build is near-free; commit the graph into our repo
(`catalog/graphs/ecc/graph.json`) so it persists.

**(b) Our own KB (markdown notes + JSON catalog): weak fit — skip it.** No AST here, so
Graphify falls back to the LLM pass (costs the tokens we're saving) and for ~12 notes
builds a worse graph than we already have: our **wikilinks ARE a hand-curated,
deterministic, git-native knowledge graph** — higher precision, zero build cost, already
persistent. The JSON catalog's fields are better queried with `jq`/a small index.

**Related talents (skills, not notes):** `context-budget` ranks what loads into a session; this note is about the graph.

## Recommendation

1. **Pilot (first step):** `graphify extract /path/to/ECC --no-viz` (code-only, near-free),
   commit the artifact into our repo, spend one real triage session querying it, compare
   tokens/time vs grep-and-read. Decision gate: does discovery get materially cheaper or
   reveal structure we missed?
2. **Adopt as skill/MCP** only if the pilot wins (add a session-start `uv tool install`).
3. **Defer for our own KB** — effectively "don't"; strengthen the wikilink graph instead
   (a link-linter, an auto-generated index).

**Earns its keep?** KB layer: no (too small, no code, wikilinks already better). Harvested
source layer: plausibly yes in code-only mode. 79× is credible on big code repos; just
respect the amortization.

## PILOT RESULT (2026-08-27) — DONE, adopt as a factory step

Ran the pilot for real. `graphifyy 0.9.50` installs and runs cleanly in our
environment. `graphify extract /home/user/affaan-m/ECC --code-only --no-viz`:
**791 code files → 11,915 nodes · 24,494 edges · 606 communities, 0 LLM tokens**
(94% EXTRACTED / 6% INFERRED, conf 0.87), in minutes.

**All main features exercised, all work graph-only (no LLM backend, 0 cost):**
- `query "…"` — BFS traversal returns a scoped subgraph within a ~2000-token budget
  (the token-saving retrieval; found orchestrator↔session-storage across Rust/JS/Python).
- `explain "<id>"` — node degree, community, every connection tagged EXTRACTED/INFERRED
  with file:line and edge type. `path A B` — shortest connection.
- Exports are **subcommands** `graphify export <format>`: `html`, `callflow-html`, `svg`,
  `graphml`, `obsidian`, `wiki`, `neo4j`, `falkordb` (verified vs 0.9.50 from the canonical
  `Graphify-Labs/graphify` repo). **Correction chain (worth keeping as a lesson):** the pilot
  claimed obsidian via the *flag* `extract --obsidian` (wrong — the flag is silently ignored);
  curator pass 2 then concluded "obsidian doesn't work" (also wrong); the fresh fetch settles
  it — **`graphify export obsidian` WORKS** (produced a 2502-note vault + `graph.canvas` on
  graphify's own source). Lesson: verify the exact invocation form, not just the feature name.
  New since the pilot: `export neo4j` / `export falkordb` push the graph to a graph DB.
- `manifest.json` **does** exist (corrects the earlier "unconfirmed"); SHA cache enables
  free incremental `graphify update`.

**Decision:** ADOPT as a factory step for code-heavy harvested repos —
`clone → graphify extract --code-only → query/explain to navigate → commit GRAPH_REPORT.md`.
Because extraction is free and fast, we do NOT commit the 14 MB `graph.json` (it
regenerates on demand); we commit the readable `GRAPH_REPORT.md` + callflow HTML +
a wiki index sample (see `catalog/graphs/ecc/`). The `--wiki` export is a candidate
input to our knowledge base. Still skip Graphify for our own markdown KB (wikilinks win).

## FULL COMMAND-SURFACE AUDIT (2026-08-27) — completeness re-check

Dumped the entire `graphify 0.9.50 --help` tree and compared every command against the
talent. The pilot had only exercised a subset; the following genuinely-valuable commands
were **missing and are now wired into `graphify-harvest`**:
- `god-nodes` — dedicated most-connected-hubs command (we had only the report's list).
- `affected "X"` — reverse traversal / impact analysis ("what breaks if I touch X").
- `global add|list|remove` + `extract --global --as <tag>` — a **cross-repo brain graph**
  in `~/.graphify/global-graph.json`; query/affected reason across ALL harvested repos at
  once (reuse-first at graph scale). Biggest miss — directly serves the "growing brain".
- `benchmark` — measured token reduction (ROI proof).
- `extract --postgres <DSN>` / `--cargo` — schema-from-live-DB / Rust crate deps.
- `tree` (D3 hierarchy), `diagnose multigraph` (graph QA), `save-result`+`reflect`
  (query memory → deterministic `LESSONS.md`, a self-improvement feed).

**Correctly skipped (security / cost / ephemeral-model), now documented in the talent:**
`hook install`, `watch`, `merge-driver`, `check-update` (auto-run hooks / long processes →
security gate); `label`, `add <url>`, `--mode deep` (LLM cost); `--graphml`, MCP server
mode, and all per-platform `install`/`uninstall` targets (self-writes CLAUDE.md + PreToolUse
hooks — we ship our own audited talent instead); `clone` (we git-clone ourselves).

## codebase-memory-mcp — the same job as a C daemon (looked up 2026-09-02)

Sources: `github.com/DeusData/codebase-memory-mcp` README, repo tree, `install.sh` (raw) and the
open-issues page, all fetched 2026-09-02. MEASURED from those unless marked. Looked up because
it appeared in a "four viral repos" video; graded here rather than in the plugins note
because this note owns code graphs.

**What it is.** "High-performance code intelligence MCP server. Indexes codebases into a
persistent knowledge graph." MIT. 41.9k stars, 3.4k forks, 2,677 commits, **453 open issues**,
release line v0.10.x. **Pure C**, one static binary, no runtime; `src/` holds the MCP stdio
server + CLI + a **daemon** ("per-account session coordination, IPC, lifecycle, shared
jobs/watchers"); `internal/cbm/` vendors **162 tree-sitter grammars**; storage is **SQLite**;
6,768 tests in 120 suites. So: real source, not a binary-only drop.

**Surface.** 15 MCP tools — `index_repository`, `search_graph`, `trace_path`,
`detect_changes`, `query_graph` (openCypher read subset), `get_architecture`, `search_code`,
`manage_adr`, `ingest_traces`, … — for 45 client surfaces (Claude Code, Cursor, Codex, Gemini
CLI, OpenCode, Aider, …). Numbers on the README: Linux kernel 28M LOC / 75k files indexed in
3 min; Django ~6 s; Cypher queries <1 ms; dead-code detection ~150 ms.

**The "99% fewer tokens".** Basis, verbatim: "Five structural queries consumed ~3,400 tokens
via codebase-memory-mcp versus ~412,000 tokens via file-by-file grep exploration — a 99.2%
reduction." One hand-picked comparison against a strawman (nobody greps 412k tokens on
purpose); the real number is whatever an agent *actually* spends without it, which is
unmeasured. Same shape as the "79% token reduction" claim graded for Graphify above.

**Install and network.** `curl … install.sh | bash`: downloads the release archive and
`checksums.txt` from GitHub releases, verifies SHA-256 (integrity against a broken download,
**not** authenticity — checksum and binary come from the same channel), writes to
`~/.local/bin`, no sudo, no shell-profile edits, then hands off to the binary's own `install`
subcommand which **writes MCP client configs** unless `--skip-config`. On macOS it **strips the
quarantine attribute and ad-hoc signs the binary** — that is the installer disabling Gatekeeper
for its own artefact. Releases are VirusTotal-scanned per candidate (REPEATED). README: "runs
100% locally and collects no telemetry" and "makes no network request of its own accord" —
a claim, not verified by reading the C.

**State, from the issue tracker (all dated 2026-09-01/02):** "Memory leak: RSS grows without
bound" (#2004); "Full index build allocates ~11.5 GB on a ~14k-file TypeScript monorepo"
(#1997); "search_code invents file paths and line numbers" (#2011) — a code-intelligence
tool fabricating locations is the one defect class that defeats its purpose; "one unreadable
directory aborts the whole run" (#2001); PHP symbols after inline HTML dropped (#2000); silent
Cypher failures (#1994, #1995, #2012). Issue numbers above 2,000 on a v0.10 project mean the
tracker turns over fast; 453 open is the backlog behind a 42k-star front page.

**Against what we have.**

| | Graphify (our pick) | repo-map (our skill) | codebase-memory-mcp |
|---|---|---|---|
| runtime | Python, `uv tool` | Python, tree-sitter | C daemon + SQLite |
| output | `graph.json` etc. **in git** | ranked tree in a token budget | index outside the repo, queried over MCP |
| LLM tokens to build | 0 for code | 0 | 0 |
| scale | unwieldy viz >5k nodes | budgeted by design | kernel-scale, fast |
| languages | ~37 grammars | tree-sitter set | 162 grammars |
| extras | communities, god nodes, Obsidian/Cypher export | PageRank ranking | Cypher, ADRs, trace ingest, dead code, change detection |
| footprint | files | files | background daemon, per-account sessions, config writes |

**Verdict (fourth gate): SANDBOX, not adopt.** It is the fastest and widest of the three and
the only one with a daemon, an installer that edits client configs and strips quarantine, an
unbounded-memory bug and a fabricated-locations bug open the day it was looked up. Try it in a
throwaway container on a harvested code repo when a harvest is too large for Graphify — that is
the one job the others cannot do — and read `src/` for the daemon and the `install` subcommand
before it runs anywhere with credentials. Never on our own markdown KB (same rule as Graphify).
Not a talent: infrastructure, like Graphiti; the talent that would use it is `graphify-harvest`
with a second backend, and that is not worth writing until one harvest actually needs it.

**Where this sits in the wider token picture (added 2026-09-02).** [[token-economy-playbook]] ranks the measured levers; the graph is fourth there, behind output tokens, untouched files and prompt caching, and it records the session in which a current graph was queried zero times.

The hand-curated wikilink graph this note prefers for the knowledge base is the `wiki/` layer of [[llm-wiki-pattern]], whose lint now has a script (`kb.py lint`, 2026-09-02).
