---
name: graphify-harvest
description: "Use when exploring, onboarding to, or reviewing a code-heavy repository and you want a cheap, navigable code map instead of grepping hundreds of files — builds a Graphify code-only knowledge graph (0 LLM tokens), lets you query/explain/trace/impact-analyse it, and can merge many repos into one cross-repo graph. Best for code repos; skip for markdown-only or wiki-linked knowledge bases where a link graph already wins. NOT for detecting intent-equivalent duplicate functions (use semantic-duplicate-sweep) -- this builds a structural graph, not an intent comparison."
disable-model-invocation: true
---

# graphify-harvest — cheap code map for any code-heavy repo

Build a Graphify code graph of a code-heavy repo and use it to navigate — during
onboarding, review, refactor planning, or reuse hunts — instead of reading many files.
Tree-sitter AST, **zero LLM tokens**. The command surface below was **re-verified end-to-end
against `graphify 0.9.50`** — every export format and navigation command was actually run, not
just read from `--help` (notes call out the surprises: `svg` needs matplotlib, `neo4j`/
`falkordb` write a file unless `--push`, `--no-viz` is a `cluster-only` flag). Confirm your
installed version's help if it differs.

## When to use
- The repo has substantial CODE (not just prose/markdown). Skip markdown-only repos and
  knowledge bases whose own link structure (e.g. `[[wikilinks]]`, a docs site) is already
  the better graph.

## Steps
1. **Install if missing** (do this per fresh/ephemeral environment; free, no LLM):
   ```bash
   command -v graphify >/dev/null || pip install --quiet graphifyy
   ```
   (The PyPI package is `graphifyy` with a doubled `y`; the installed binary is `graphify`.
   This is intentional, not a typo — verified against `graphifyy 0.9.50`.)
2. **Build the graph** (code-only, no viz — fast, 0 tokens):
   ```bash
   graphify extract <repo-path> --code-only               # local AST, 0 tokens, skips doc/paper/image files
   graphify cluster-only <repo-path> --no-label --no-viz  # GRAPH_REPORT.md + communities; --no-viz skips graph.html
   ```
   NB: `--no-viz` is a **`cluster-only`** flag (it suppresses `graph.html`), NOT an `extract`
   flag — `extract … --no-viz` is silently accepted-then-ignored (extract writes no `graph.html`
   anyway; its skip-clustering equivalent is `--no-cluster`). Verified vs 0.9.50: a flag on the
   wrong subcommand is ignored, not rejected — keep each flag on the subcommand whose `--help` lists it.
3. **Triage first — find the hubs.** Read `GRAPH_REPORT.md` and run:
   ```bash
   graphify god-nodes --top 15    # most-connected nodes = real entry points / core code
   ```
   **Check the component spread before trusting a global top-N.** A repo's graph is often a
   **forest**, not one graph — a Python service and a TypeScript stack that talk over HTTP share no
   import edges, so they are separate components. A globally degree-ranked list then leans toward the
   largest one. Measured 2026-09-12 on a 4,499-node graph whose second island holds **24%** of the
   nodes: the top-15 gave it **2 slots (13%)**. Under-weighted, and **not** absent — the skew is real
   but mild, so the fix is to *read the spread*, not to distrust the list. Ask for more than you need
   and check which component each hit came from; if a subsystem you know exists has no entries, rank
   inside it rather than globally.
   Plus the Leiden communities in the report = the subsystems. This is the fast-orientation
   win: know what matters before querying, instead of reading files blind.
4. **Navigate** (graph-only, no backend, 0 tokens):
   - `graphify query "how does X connect to Y?"` → scoped subgraph (`--budget N` caps
     tokens, default 2000; `--dfs` for depth-first). The retrieval that saves reading files.
   - `graphify explain "<node-or-id>"` → degree, community, EXTRACTED/INFERRED edges.
   - `graphify path "A" "B"` → shortest connection (add `--undirected` if no directed path).
   - `graphify affected "X"` → **reverse traversal: what depends on / breaks if you touch X**
     (`--depth N`, `--relation R`). Impact analysis before adopting or changing a component.
5. **Persist the readable outputs** into your repo or docs (NOT the multi-MB `graph.json`,
   which regenerates for free):
   ```bash
   mkdir -p <docs-dir>/graphs/<repo>/
   cp <repo-path>/graphify-out/GRAPH_REPORT.md <docs-dir>/graphs/<repo>/
   graphify export callflow-html                       # Mermaid architecture / call-flow
   cp <repo-path>/graphify-out/*callflow*.html <docs-dir>/graphs/<repo>/
   ```
   Gitignore `graph.json` and `graphify-out/`. The callflow HTML is the readable
   architecture map — commit it alongside the report.
6. **Merge into a cross-repo graph** (optional — every extracted repo in one queryable
   graph, 0 LLM; persists in `~/.graphify/global-graph.json`):
   ```bash
   graphify extract <repo-path> --code-only --global --as <repo>   # or: graphify global add <graph.json> --as <repo>
   graphify global list                                            # repos in the combined graph
   ```
   Then `query`/`affected` can reason **across** multiple repos at once — e.g. "does any
   of these repos already implement X?" before you build it (reuse-first, at graph scale).
   NB: the global graph lives in `~/.graphify/` — if that's ephemeral, commit a refreshed
   `GRAPH_REPORT.md` per repo and rebuild the combined graph on demand from those.
   **Store-free alternative (git-friendly):** `graphify merge-graphs <g1.json> <g2.json> …
   --out graphify-out/merged-graph.json` unions several `graph.json` into one cross-repo graph
   **without** touching `~/.graphify/` — point `query --graph merged-graph.json` at it. Prefer
   this when the global store is ephemeral or you want the combined graph tracked in git.
7. **Refresh** after the repo changes: `graphify update <repo-path>` (SHA-cache
   incremental, no API cost; `--force` after refactors that delete code).

## Exports — `graphify export <format>` (all 8 subcommands re-verified vs 0.9.50)
Exports read `graphify-out/graph.json` (run `extract` + `cluster-only` first). Each was run
end-to-end on a fresh graph; results noted so you don't hit a surprise:
| `export <fmt>` | Produces | Note |
| --- | --- | --- |
| `html` | `graph.html` | interactive, no server |
| `callflow-html` | `<repo>-callflow.html` | Mermaid architecture/call-flow — the readable map to commit |
| `svg` | `graph.svg` | **requires matplotlib** (`pip install matplotlib`); errors without it |
| `graphml` | `graph.graphml` | for Gephi / yEd |
| `obsidian` | vault (`.md` + `graph.canvas`) | verified: 2502-note vault on graphify's own source |
| `wiki` | `wiki/` articles + `index.md` | agent-crawlable markdown, 0 LLM |
| `neo4j` | `cypher.txt` | writes a file; `--push <bolt-URI> --user U` loads a LIVE DB (pw via `NEO4J_PASSWORD` env) |
| `falkordb` | `cypher.txt` | file by default; `--push falkordb://host:6379` loads live (one stmt at a time) |
NB: these are **subcommands, not `extract` flags** — `graphify extract … --obsidian` is
silently ignored; the working form is `graphify export obsidian`. Do not "correct" this back:
the tool has TWO surfaces, and `--obsidian` is real on the OTHER one — `/graphify … --obsidian`
is a documented *skill* flag (v8 README, checked 2026-09-04), which is why the flag looks valid
in the docs and dies on `extract`. This CLI table is the `graphify …` surface. `neo4j`/`falkordb` do NOT
push unless you pass `--push` — by default they just write `cypher.txt`.
**`export wiki` writes where the GRAPH is, and takes no `--dir`** (measured 0.9.53 **and re-measured on 0.9.56**, 2026-09-04 -
the package shipped three releases that day and the behaviour did not change): `--dir` is accepted without an error and silently ignored, and `wiki/` (238
articles on a 5,173-node graph) lands beside the file `--graph` points at. If that path is a
read-only import, a vendored corpus or anything you do not want 238 new files in, **copy the
graph to a scratch directory and export from there.** `export obsidian` does honour `--dir`;
they are not symmetrical.
- **Knowledge-base feed** (0 LLM): `export wiki`/`export obsidian` are the markdown/vault feeds
  in the table above. Curate a few high-signal notes into your docs; do NOT commit the whole
  set (large repos produce thousands — the graphify source yields a 2502-note vault).
- **Multimodal corpus (beyond code — verified):** without `--code-only`, `extract` also indexes
  **docs, papers, images, and videos** into the same graph — but these need an **LLM backend**
  (`--backend gemini|claude|openai|kimi|deepseek|ollama` + the matching API key) and **cost
  tokens**. Verified: a corpus with a non-code file errors with "no LLM API key found … or pass
  `--code-only`". So code-only stays the 0-token default; reach for the semantic pass only when a
  specific doc/paper/image graph is worth the spend. `--google-workspace` first exports
  `.gdoc/.gsheet/.gslides` shortcuts; `.graphifyignore` (+ `--no-gitignore`) scopes what's indexed.
- **Prove the ROI:** `graphify benchmark` → measured token reduction vs a naive full scan
  (verified: prints corpus tokens vs avg per-query cost).
- **Schema-heavy projects:** `graphify extract <path> --postgres <DSN>` maps tables/views/
  functions + FK relationships from a live Postgres DB (column detail not represented).
  `--cargo` does the same for Rust crate→crate deps.
- **Extra views:** `graphify tree` → D3 collapsible-tree HTML (hierarchy view alongside
  callflow). `graphify diagnose multigraph` → QA on edge-collapse risk in a graph.
- **Query memory / learning loop:** `graphify save-result …` records a Q&A outcome
  (useful/dead_end/corrected); `graphify reflect` aggregates them into a deterministic
  lessons file. A self-improvement feed — adopt only if you drive many graph queries.

## Deliberately NOT used by default (considered, skipped with reason)
- `hook install` / `watch` / `merge-driver` / `check-update` — auto-run git hooks and
  long-running watchers. Avoid unaudited auto-run, and an ephemeral or git-only workflow
  has no persistent process to host them. Re-extract on demand instead.
- `label` / `add <url>` / `extract` semantic mode (`--mode deep`, doc/PDF pass) — these
  invoke the **LLM backend and cost the tokens you're saving**. Only for a specific
  document graph that's worth it; never by default. `--no-label` keeps community naming free.
- `graphify export graphml` — only if you need an external graph app (Gephi/yEd); otherwise
  navigate in-session.
- **MCP stdio server mode** + the ~20 per-platform `install`/`uninstall` targets (claude,
  cursor, codex, opencode, aider, gemini, kilo, **copilot**, **vscode**, claw, droid, trae,
  antigravity, hermes, kiro, pi, devin …) — integration installers that write to config files
  (e.g. a CLAUDE.md/AGENTS.md section) and add PreToolUse/BeforeTool hooks. Prefer invoking
  Graphify explicitly rather than letting it self-install into your tooling.
- `clone <github-url>` / `add <url>` — clone/fetch with your own tools to keep the checkout
  under your control (`add` also invokes the LLM backend on the fetched content).
- `save-result` / `reflect` — a per-graph Q&A memory→lessons loop; adopt only if you drive
  many graph queries and want graphify's own retrieval to self-improve (separate from our brain).

## Rules
- Code-only by default (0 LLM). Run the semantic/doc pass only when a specific document
  graph is worth it.
- Commit the readable outputs (report + callflow HTML), gitignore `graph.json`; extraction
  is cheap, storage isn't.
- Treat every install/hook subcommand as a security decision — don't let Graphify write
  hooks or config sections into your repo; invoke it explicitly from this method.

## In this repo (one concrete instance)
This method is domain-agnostic. As an example of wiring it into a specific project, a
harvesting/curation repo might: persist reports under a `catalog/graphs/<repo>/` tree,
treat its own wiki-linked markdown knowledge base as the case to *skip* (link graph wins
there), and feed the combined graph into a reuse-check step before building new code. Any
repo-local index/registration step (e.g. registering the extracted repo root with your
harness) is glue around this method, not part of it.
