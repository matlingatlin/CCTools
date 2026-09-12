---
title: Graphify — full feature reference
sources:
  - url: https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md
    fetched: 2026-08-27
  - url: https://pypi.org/project/graphifyy/
    fetched: 2026-08-27
  - url: https://www.augmentcode.com/learn/graphify-knowledge-graph-codebase-skill
    fetched: 2026-08-27
status: verified
tags: [graphify, knowledge-graph, tooling, reference]
related: ["[[graphify-assessment]]", "[[token-economy-playbook]]"]
---

# Graphify — full feature reference

Companion to [[graphify-assessment]] (the adopt/defer decision). This is the
complete capability inventory. `github.com/safishamsi/graphify` (mirror
`Graphify-Labs/graphify`), PyPI **`graphifyy`**, CLI `graphify`, Apache-2.0,
Python ≥3.10, v0.9.50. Features differ by branch (v3→v8); version-specific items
flagged. Two surfaces: the `/graphify` assistant skill and the `graphify` shell CLI.

## Contents
- CLI commands · Language/format support · Graph model · Outputs · Integration ·
  Query · Configuration · Version diffs · Limitations

## CLI commands

**Build:** `/graphify .` or `graphify extract ./path`. Flags: `--update`
(incremental, changed files only), `--mode deep` (richer inference), `--code-only`
(AST only, **0 API calls**), `--cluster-only`, `--directed`, `--watch` (live rebuild
on save), `--force`, `--allow-partial`, `check-update`/`update` (staleness).

**Query:** `graphify query "…"` (NL → subgraph; `--budget N` caps tokens; `--dfs`
path trace v3/v4; `--graph file` other graph), `graphify path "A" "B"` (shortest
path), `graphify explain "X"` (degree, community, rationale).

**Add content:** `graphify add <url>` — arXiv papers, YouTube/video (download +
transcribe), tweets (v3/v4); `--author`/`--contributor` provenance tags.

**Export:** `export callflow-html` (Mermaid arch diagram, v8), `--svg`, `--graphml`
(Gephi/yEd), `--neo4j` (Cypher file) / `--neo4j-push bolt://…`, `--falkordb-push`
(v8), `--obsidian` (vault), `--wiki` (agent-crawlable markdown site).

**Install/integrate:** `graphify install [--platform]`; per-assistant
`graphify claude|codex|cursor|gemini|copilot|aider|… install|uninstall`
(`claude install` = CLAUDE.md instruction + PreToolUse hook).

**Ops:** `hook install|uninstall|status` (git post-commit/checkout auto-rebuild),
`merge-graphs a.json b.json`, `clone` (v6), `global add … --as name` (v8),
`prs` / `prs --triage` (PR impact dashboard, v8),
`python -m graphify.serve graph.json` (MCP server).

Other flags: `--no-viz`, `--max-workers N`, `--token-budget N`, `--max-concurrency N`,
`--api-timeout S` (600s), `--dedup-llm`, `--no-cluster`, `--no-label`,
`--resolution N` (Leiden granularity), `--exclude-hubs N`, `--backend <name>`,
`--postgres "…"`, `--no-gitignore`.

## Language & format support

**Code = 100% local tree-sitter AST** (deterministic, no LLM). Grammar count grew:
v3 = 20 languages; v4/v6 ≈ 25 (+Verilog/SystemVerilog/Vue/Svelte/Dart);
**v8 = "37+ grammars / ~40"** (+ Astro, Groovy, Fortran, Pascal, Bash, JSON, SQL,
DreamMaker, Salesforce Apex, Terraform/HCL, OCaml). Some ship as optional extras
(DreamMaker, Terraform, Pascal, OCaml, Common Lisp).

**Non-code semantic pipeline (needs LLM backend unless noted):** markdown/HTML/RST/
YAML; Office `.docx/.xlsx`; Google Workspace (v8, env-gated); PDF (citation mining);
images (vision model); **video/audio = local faster-whisper transcription** + `yt-dlp`,
concept extraction via LLM; config manifests (`pyproject.toml`, `go.mod`, `pom.xml`,
MCP configs — local); SQL schema / live `--postgres` introspection.
**Privacy split:** code + audio local; docs/PDF/images go to the LLM backend.

## Graph model

**Nodes:** functions/classes/modules/variables/types/imports; concepts (from docs);
**rationale nodes** (`# NOTE:`/`# WHY:`/`# HACK:` + docstrings + ADR/RFC citations,
linked `rationale_for`); **god nodes** (highest-degree); **communities** (Leiden);
hyperedges (3+ nodes, v3/v4); media content nodes; SQL/IaC entities (v8).

**Edges:** `calls`, `imports`, `inherits`, `mixes_in`, `references`, `uses`,
`implements`, `depends_on`, `cites`, `semantically_similar_to` (always INFERRED).

**Confidence tag on every edge:** `EXTRACTED` (explicit, 1.0) / `INFERRED`
(reasoned, 0.0–1.0 score) / `AMBIGUOUS` (v3/v4; de-emphasized in v8).

**Clustering:** Leiden over **edge density / topology — no embeddings, no vector
store**. `--resolution` tunes granularity, `--exclude-hubs` suppresses hubs.
Centrality = degree + community. Communities drive PR impact analysis.

## Outputs (`graphify-out/`)

- `graph.json` — full queryable graph (commit this; single source of truth).
- `GRAPH_REPORT.md` — god nodes, surprising connections, 4–5 suggested questions.
- `graph.html` — interactive force-directed viz (slow >5000 nodes → `--no-viz`).
- `cache/` — SHA256 cache; re-runs process only changed files.
- Export artifacts: callflow HTML/SVG, GraphML, Cypher (Neo4j/FalkorDB), Obsidian
  vault, markdown wiki.
- **Unconfirmed:** `manifest.json` / `cost.json` were NOT verifiable by name in the
  READMEs read — treat as unverified (cost tracking exists conceptually; the file
  does not verify).

## Integration modes

- **Assistant skill + hook** (context injected before file searches): Claude Code
  (CLAUDE.md + PreToolUse hook), Codex, OpenCode, Cursor, Gemini, Copilot, Aider,
  OpenClaw, Trae, … — **20+ assistants** (v8). Hookless assistants run sequential.
- **MCP server:** `python -m graphify.serve graph.json` (stdio) or `--transport http
  --host --port` (v8). Tools: `query_graph`, `get_node`, `get_neighbors`,
  `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.
- **Git hook:** post-commit/checkout AST-only rebuild (no API cost).
- **CI/headless:** `graphify extract --backend … --code-only`.

## Query capabilities

NL query → scoped subgraph (token-bounded); path-finding; explain-a-concept;
auto-suggested questions; callflow tracing; GraphRAG-style retrieval substrate
(positioning, not a named feature); agent access via MCP tools or reading
`graph.json`; PR intelligence (`prs --triage`, shared-community merge-risk, v8).

## Configuration

**Backends (default Gemini):** Gemini, Claude (`--backend claude` / `claude-cli`
subscription), OpenAI (+`OPENAI_BASE_URL` for local servers), DeepSeek, Kimi/Moonshot,
Ollama (local, no key), Bedrock, Azure, Anthropic-compatible gateways.
`--code-only` = 0 credits.

**Incremental/staleness:** `--update`, SHA256 cache, `--watch`, `check-update`/
`update`, git hook. Partial extractions refuse to overwrite unless `--allow-partial`/
`--force`.

**Limits/env:** viz slow >5000 nodes; graph cap 512 MiB (`GRAPHIFY_MAX_GRAPH_BYTES`);
`.graphifyignore` (gitignore syntax) + auto-merge `.gitignore`; env vars
`GRAPHIFY_MAX_WORKERS/_MAX_OUTPUT_TOKENS/_API_TIMEOUT/_FORCE/_GOOGLE_WORKSPACE/
_TRIAGE_BACKEND/_OLLAMA_NUM_CTX/_QUERY_LOG_ENABLE`.

**Extras:** `graphifyy[pdf,office,google,video,mcp,neo4j,falkordb,svg,leiden,ollama,
openai,gemini,anthropic,bedrock,azure,sql,postgres,dm,terraform,pascal,ocaml,
commonlisp,chinese,all]`. **Leiden extra needs Python <3.13.**
Install: `uv tool install graphifyy` / `pipx` / `pip`.

## Version diffs (v3→v8)

v8 adds vs earlier: ~40 languages, multi-backend matrix, full headless `extract`
+ `--postgres`, PR tooling (`prs`/`--triage`), `export callflow-html`, MCP HTTP
transport + 7 tools, FalkorDB export, `global add`, `--resolution`/`--exclude-hubs`,
Graphify-Labs mirror. AMBIGUOUS confidence tier de-emphasized in v8.

## Limitations (stated)

Viz >5000 nodes; 512 MiB graph cap; Ollama VRAM tuning; LLM output truncation
(auto-recovers via chunk bisection); partial extractions on very large corpora;
ghost duplicates fixed in v0.8.33+ (re-extract old graphs); community naming needs a
backend; Codex needs `multi_agent=true` for parallel; **no embeddings/vector DB**
(topology-only similarity, a deliberate recall limit).

**Independent benchmarks:** LOCOMO recall@10 0.497 (high), but LOCOMO QA 45.3%
(*lower* than supermemory 49.7% despite far higher recall); LongMemEval-S QA 76%
(tied with dense RAG); graph build 0 LLM credits. Token claims: 71.5× on a 52-file
mixed corpus, ~1× on tiny corpora (below the graph inflection point).

## Ambiguities
`manifest.json`/`cost.json` unverified by name; "GraphRAG" is inferred positioning;
HTTP-MCP API-key auth implied not documented; grammar count quoted 36 vs 37+.
`BENCHMARKS.md` / `ARCHITECTURE.md` exist upstream but were not fetched.

Policy for when to query the graph at all, and the measured cost of forcing it into every call: [[token-economy-playbook]] (added 2026-09-02).
