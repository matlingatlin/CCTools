---
title: Graphify — assessment for the knowledge base
sources:
  - url: https://github.com/Graphify-Labs/graphify
    fetched: 2026-08-27
  - url: https://stevescargall.com/blog/2026/05/graphify--memmachine-79-token-reduction-zero-vector-database/
    fetched: 2026-08-27
  - url: https://pypi.org/project/graphifyy/
    fetched: 2026-08-27
  - url: https://pypi.org/pypi/graphifyy/json
    fetched: 2026-09-04
    note: "0.9.53, Apache-2.0. Repo Graphify-Labs — the LIKELIER home, not a settled one: see the canonical-home paragraph below and [[graphify-features]], which holds the smaller claim"
tags: [graphify, knowledge-graph, tokens, tooling, decision]
related: ["[[graphify-features]]", "[[claude-md-and-memory]]", "[[llm-wiki-pattern]]", "[[claude-code-extension-layer]]", "[[claude-code-ecosystem-plugins]]", "[[mcp]]", "[[temporal-kg-agent-memory]]", "[[third-party-landscape]]", "[[token-economy-playbook]]", "[[harness-over-model-prime-agent]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Graphify — assessment

**Graphify** (`github.com/Graphify-Labs/graphify` — the likelier home, see below; also served at `safishamsi/graphify`;
PyPI `graphifyy`; **MIT through v7, Apache-2.0 from v8 and on the shipped
package** — the licence changed under this note, both values checked 2026-09-04, see
[[graphify-features]]; YC S26) — NOT Graphiti/Zep.
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
  `graphml`, `obsidian`, `wiki`, `neo4j`, `falkordb` (verified vs 0.9.50 from the
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
unmeasured. Same shape as the 79.6× claim graded for Graphify above — though not the same
error: **that one was mis-stated here as a PERCENTAGE, and this line was where it happened.**
Corrected 2026-09-08 against the held bytes
(`knowledge/raw/watch-2026-09-08c/stevescargall.com_graphify-memmachine.html`), which read
verbatim *"Reduction: 79.6x fewer tokens per query"* and *"We're seeing 79x token reductions"* —
a **factor**, never a percent. 496k → 6.2k is **80×, a 98.8% cut**; "79%" understates the
source's own claim by a factor of eighty and was quoted here as if the source had said it. The
origin is visible in the URL: the slug reads `graphify--memmachine-79-token-reduction`, with no
unit, and this note supplied the wrong one. The correct figure was already three sections above
in this same page (79.6×), which is the uncomfortable part — the page contradicted itself and
the wrong half wore quotation marks.

**Install and network.** `curl … install.sh | bash`: downloads the release archive and
`checksums.txt` from GitHub releases, verifies SHA-256 (integrity against a broken download,
**not** authenticity — checksum and binary come from the same channel), writes to
`~/.local/bin`, no sudo, no shell-profile edits, then hands off to the binary's own `install`
subcommand which **writes MCP client configs** unless `--skip-config`. On macOS it **strips the
quarantine attribute and ad-hoc signs the binary** — that is the installer disabling Gatekeeper
for its own artefact. **Which repo is the home — reconciled 2026-09-12, and it is still not settled.** This page said
"canonical" three times on the strength of PyPI's Homepage and Repository URLs. [[graphify-features]]
records that PyPI metadata alone is **not sufficient** — the v8 README's own self-link points at
`safishamsi/graphify`, both `main` READMEs are byte-identical, and an earlier "canonical" call here
was corrected the same day by `kb.py owners`. The word is now qualified at every occurrence, because
this page was asserting more than the evidence carries while its companion asserted less.

**New evidence, and it leans one way without closing the question.** `kb.py owners` on 2026-09-12
reports the README's `safishamsi` self-links as **0 of 1 LIVE** — a clone line and a homepage, both
inert, which the check's own verdict calls *"a leftover, not a move"*. An ownership move keeps the old
URL alive and would show live self-links; a rename that left prose behind shows exactly this. So the
evidence now favours `Graphify-Labs` as the live home while still not proving it, which is why the
word here is "likelier" and not "canonical". The check reports it as a candidate for a human, and it
stays one.

**Confirmed from the outside, 2026-09-12:** the same-channel argument above was written here from
graphify's code. Prime Intellect then published the identical reasoning about *their* installer —
*"because the inventory and archive come from the same origin, HTTPS is the authenticity boundary"* —
and pinned `--proto '=https'` to close the plaintext-redirect hole. See
[[harness-over-model-prime-agent]]: an independent vendor reaching the same conclusion is the best
evidence this page's reading was a real property and not a quibble about one project's wording.

Releases are VirusTotal-scanned per candidate (REPEATED). README: "runs
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

## The obsidian correction chain, closed (2026-09-04)

Third and final link. The chain above records two wrong answers and one right one; the right
one was right for the wrong reason. Fetching the v8 README settles it: graphify has **two
command surfaces**, and each flag belongs to exactly one. `/graphify … --obsidian` is a
**skill** flag and is documented; `graphify export obsidian` is the **CLI** subcommand and was
measured working here; `extract --obsidian` is neither, which is why it was silently ignored.
The README names the distinction itself, on the `--code-only` line. Nobody was reading a
broken tool — the pilot was reading the wrong surface. The full claim table, and the trap that
the repository's **default branch serves a v1-era README** with none of this in it, are in
[[graphify-features]]; what it means for a vault is in `knowledge/VAULT.md`.

**The lesson, sharpened.** The earlier version said "verify the exact invocation form, not just
the feature name." One pass further: verify *which surface* the form belongs to, and *which
branch* the documentation you are quoting comes from. Two of the three errors in this chain
were surface or branch errors, not feature errors.

**This tool is sold as "memory", and it is not.** [[claude-md-and-memory]] grades the social
claims made about it — "Graphify gives unlimited memory" is a video's word, not the tool's: it
builds a code graph, and what persists is `graph.json` in git. That page is where the
influencer-claim ledger lives, and it is the right neighbour for a reason this note now has
twice over — the 2026-09-04 carousel above is the second social source about graphify this
knowledge base has had to check against the source rather than believe.

**Version drift, measured within one day (2026-09-04).** The installed binary and PyPI both read
`0.9.53` in the morning; the afternoon's baseline captured `0.9.55`; the evening's watch run found
`0.9.56`. Three releases in a day. Two things follow. Any version this note or
[[graphify-features]] states is a reading, not a fact about the project — carry the timestamp or
do not carry the number. And the watch list keeps the **PyPI JSON** for this package and drops the
rendered `pypi.org/project/graphifyy/` page: same fact, and the page adds download counters that
move without the version moving. Watch the API, not the rendering — the same rule that made a
repo's README the watched form rather than its star-counting page.

**`codebase-memory-mcp` moved too**, in the direction its SANDBOX verdict cared about: for Codex,
"install keeps only a tiny managed activation pointer in global `$CODEX_HOME/AGENTS.md`; all
detailed behavior lives in the installed `codebase-memory` skill", with upgrades replacing the
legacy full managed block. That is less written into a file the user owns than the verdict was
written against. It does not overturn SANDBOX — the daemon, the config writes and the
quarantine-stripping installer are untouched — but it is movement on the specific complaint, and
it is recorded rather than left for the next reader to rediscover.

*Version note, 2026-09-11: PyPI `graphifyy` is at **0.9.58** (watched release index; was 0.9.56 when this page last measured anything). **No measurement here is re-dated by that** — every figure above names the version it was taken on, which is exactly what makes a bump cheap to absorb. What the bump does NOT settle is the open question this base still carries: whether `extract --no-viz` does anything, which needs a run and not a release number (`pipeline/reviews/2026-09-08-kb-walkthrough.md`).*
