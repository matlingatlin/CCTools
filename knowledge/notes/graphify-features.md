---
title: Graphify — full feature reference
sources:
  - url: https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md
    fetched: 2026-08-27
  - url: https://pypi.org/project/graphifyy/
    fetched: 2026-08-27
  - url: https://www.augmentcode.com/learn/graphify-knowledge-graph-codebase-skill
    fetched: 2026-08-27
  - url: https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md
    fetched: 2026-09-04
    note: re-fetched; kept at knowledge/raw/instagram-graphify-obsidian-2026-09-04/
  - url: https://raw.githubusercontent.com/safishamsi/graphify/main/README.md
    fetched: 2026-09-04
    note: the default branch serves a v1-era README
  - url: https://pypi.org/pypi/graphifyy/json
    fetched: 2026-09-04
    note: version 0.9.53, license Apache-2.0, Homepage Graphify-Labs
  - url: https://raw.githubusercontent.com/safishamsi/graphify/v8/LICENSE
    fetched: 2026-09-04
    note: "Apache-2.0. The v3, v4, v6 and v7 LICENSE files were read the same day and are MIT; one URL per branch is not listed because the claim is the CHANGE, and v8 is where it happened. An earlier version of this entry wrote all five as a brace expression, which is not a URL - curl globbed it and the baseline fetcher stored v8's file under a fabricated address."
tags: [graphify, knowledge-graph, tooling, reference]
related: ["[[graphify-assessment]]", "[[token-economy-playbook]]", "[[third-party-landscape]]", "[[model-agnostic-agent-harnesses]]"]
raw:
  - knowledge/raw/instagram-graphify-obsidian-2026-09-04/graphify-README@main@2026-09-04.md
  - knowledge/raw/instagram-graphify-obsidian-2026-09-04/graphify-README@v8@2026-09-04.md
  - "partial: 2 of 6 distinct source URLs kept as raw; the rest predate the raw layer (2026-09-02)"
---

# Graphify — full feature reference

Companion to [[graphify-assessment]] (the adopt/defer decision). This is the
complete capability inventory. **The two GitHub homes disagree, and the disagreement is the fact.** PyPI's Homepage and
Repository URLs both point at `Graphify-Labs/graphify`, while the v8 README's own self-link
points at `safishamsi/graphify`; the two `main` READMEs are byte-identical (all measured
2026-09-04). An earlier version of this line called Graphify-Labs canonical on the strength of
the PyPI metadata alone — corrected the same day by `kb.py owners`, which reads a project's own
links and found this pair. Either URL resolves; **which one is the home is not settled by the
evidence we hold**, and that is a smaller claim than the one it replaces. PyPI
**`graphifyy`**, CLI `graphify`, Python ≥3.10, **0.9.56** (PyPI, as of 2026-09-04 **evening**; it was 0.9.53 that morning and 0.9.55 that afternoon - three versions in one day, caught by `watch.py`, and the reason a calendar-based staleness rule is hopeless for this package).
**Licence, and it changed:** MIT through v7 (`LICENSE` on v3, v4, v6, v7 = "MIT License,
Copyright (c) 2026 Safi Shamsi"), **Apache-2.0 on v8 and on the shipped package** (v8 `LICENSE`
= Apache License; PyPI metadata `license: Apache-2.0`), both checked 2026-09-04; v1 and v2
carry no `LICENSE` file at all. A note that says "graphify is MIT" was right before v8 and is
wrong now. Features differ by branch (v3→v8); version-specific items
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

**Export — SUBCOMMANDS, not flags** (corrected 2026-09-12; this block contradicted the
two-surface section further down in this same note, and the flag form is the exact error both
graphify notes carry as their own lesson). `graphify export <format>`, verified against 0.9.50:
`html`, `callflow-html` (Mermaid arch diagram, v8), `svg`, `graphml` (Gephi/yEd), `obsidian`
(vault), `wiki` (agent-crawlable markdown site), `neo4j`, `falkordb`. Graph-DB pushes are
`export neo4j` / `export falkordb`; `--neo4j-push bolt://…` remains a flag on that subcommand.
**`--obsidian` is a flag on the `/graphify` SKILL surface and is silently ignored on
`extract`** — see "The two flag surfaces" below, and [[graphify-assessment]] for the
correction chain (pilot claimed the flag works → curator concluded obsidian is broken → the
fresh fetch settled it: `graphify export obsidian` produced a 2,502-note vault).

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
- **README-silent:** `manifest.json` / `cost.json` are NOT verifiable by name in the
  READMEs read. Kept as its own row rather than deleted, because README silence and a runtime
  observation are different evidence bases and collapsing them loses which one supported what.
- **`manifest.json` DOES exist — now measured TWICE.** Recorded first from the ECC pilot's runtime
  observation ([[graphify-assessment]]); then directly, the same day, by a run in this environment that
  wrote `graphify-out/manifest.json` at **71,711 bytes**. Two independent evidence bases agreeing, which
  is what the README-silence row above could never have given on its own. So the row above is a fact about the
  documentation, not about the tool. `cost.json` remains unobserved by either route: cost
  tracking exists conceptually and the file has never been seen.

## Communities are a FLAT partition, not a hierarchy — checked 2026-09-12

Asked whether multi-level graphs (a node exploded into its own graph, level after level) are worth
building. Answered against the held READMEs rather than by running anything, since graphify is not
installed in this environment. Verbatim from
`knowledge/raw/watch-2026-09-11/raw.githubusercontent.com_Graphify-Labs_graphify_HEAD_README.md.md`:

- `/graphify . --cluster-only --resolution 1.5` — *"more granular communities"*; the CLI form says
  *"more, smaller communities"*. **A granularity knob over ONE partition, not a tree.** There is no
  parent/child community id documented anywhere in either README, so *different resolutions are
  alternative flat views of the same graph*, not linked levels.
- **`cluster-only` re-runs clustering WITHOUT re-extracting**, which is the cheap part and the useful
  one: several resolutions cost one extraction.
- `--exclude-hubs 99` — *"exclude p99 degree nodes from partitioning"*. Hubs distort a partition, so
  this is how a resolution produces subsystems that mean anything.
- Communities are *"The graph split into subsystems (Leiden), with LLM-free labels"* — one level, by
  the README's own wording.
- **Leiden is an optional extra and version-limited:** `uv tool install "graphifyy[leiden]"`, tagged
  *"Python < 3.13 only"*. On 3.13+ the algorithm named throughout the feature list is not installable,
  and what partitions instead is undocumented here. Worth knowing before a design leans on it.

### MEASURED 2026-09-12, and it corrected this page's own recommendation

graphify was installed and run (wheel-only, no LLM, on a scratch copy of hello-world: **4,499 nodes,
11,263 edges, 189 communities** from 326 code files). **That one run also settled two older questions
for free:** `--no-viz` is **respected**, not silently ignored — no `graph.html` was written, refuting
the worry that the 11,915-node pilot built a viz it believed suppressed — and `manifest.json` was
produced, confirming at runtime what had only been a README-silence row. Full rule and result:
`pipeline/decisions/2026-09-12-graphify-hierarchy.md`.

**Q1 confirmed from the source, not the README.** `build.py:2220` writes `data["community"] = cid` — one
integer per node — and the call is flat `gn.leiden(..., resolution=…)`. No parent, level or dendrogram
anywhere. Two corrections to the README reading above: `--resolution` and `--exclude-hubs` are **real
but absent from `--help`** (parsed at `cli.py:2034`, `cli.py:3311`), and on Python ≥3.13 graphify does
**not** break — `cluster.py` says it falls back to Louvain.

**This page previously said deriving a hierarchy by nesting resolutions was "sound". That is now
measured FALSE.** Coarse `resolution=0.5` → 55 communities, fine `resolution=2.0` → 77; of those 77,
**59 sit inside exactly one coarse community and 18 straddle**, the worst spanning **4** while holding
196 nodes. **76.6% single-parent against a 90% threshold fixed before the run — NOT DERIVABLE.** The
reason, unchecked when the claim was written: each partition call is an *independent* optimisation over
the whole graph, so a finer run is not a refinement of a coarser one and nothing makes them nest. The
edges do survive, which was the half I had right.

**What actually produces levels — and graphify already ships the dependency.**
`graspologic.partition` exposes **`hierarchical_leiden`** beside the flat `leiden` graphify calls. On
the same graph's largest connected component (3,182 nodes): **level 0 = 21 clusters, level 1 = 132, and
132 of 132 have exactly one parent — 100.0%.** Levels by construction, because each level *is* a
refinement of the one above. **Caveat, and it is structural rather than fringe:** `hierarchical_leiden` needs a connected graph, and
**1,317 of 4,499 nodes (29%) sit outside the giant component**. Measured further: **48 components**, and
only **8** of those 1,317 nodes are lone nodes. The second component holds **1,089 nodes** — from
`source_file`, `apps/engine` (2,818) dominates the giant one while `apps/api`/`apps/app`/
`packages/shared` make up the second. **The Python engine and the TypeScript stack are two islands**,
disconnected because they talk over HTTP and a queue rather than importing each other. So the tree must
be built **per component** — a forest, one tree per subsystem — or it silently omits a quarter of the
graph.

**Which hands you level 0 for free.** Connected component ≈ language/workspace boundary, computed with
no algorithm and no parameter, and more meaningful than any Leiden level; Leiden then refines *inside*
each island. Discovered by asking how many components there were, which cost one line and was not asked
for two days. **A tool that assumes "the graph" is one connected structure is wrong about this repo.**

**Checked against Scio's held graph too, 2026-09-12 — same shape, larger fraction.**
`Scio/docs/as-built/graph/graph.json` (5,173 nodes, 12,054 links, read-only) is a **77-component
forest**: giant **3,201 (61.9%)**, **1,972 nodes outside it**, and only **25** lone nodes — so again the
outside is structure, not dust. The same two islands (`apps/engine` 2,790 vs `apps/api`/`apps/app`/
`packages/shared`), plus a **third island of 279 documentation nodes** (`docs/decisions`,
`docs/UX-FLOW.md`, `docs/STRATEGY.md`) which is most of the gap between that graph's 5,173 nodes and
the 4,499 of the `--code-only` run here. Consistent, not contradictory: different extraction modes.

**Why this is worth carrying in this note.** Scio's own steering file instructs readers to *"Query it
for symbols and dependencies instead of reading source."* A reader following that instruction and
treating the result as one connected structure silently misses **38% of the graph** — the entire
TypeScript stack and all of the documentation nodes. The fix is a sentence in Scio's own docs, which is
a separate repo and a separate decision; recorded here because this note is where the measurement
lives.

Re-running `graphify` per subtree remains the worst option: each edge leaving the subtree is silently
lost, so the sub-graph understates exactly the coupling that was the reason to look — and this base
already measured why the tempting boundary is wrong, since **god nodes are the highest-degree nodes and
do not respect directory structure.**

For descent on demand rather than pre-built levels, `graphify query "<question>" --budget N` already
returns a token-bounded scoped subgraph, which addresses the real constraint (context budget) without
any levels at all. Pre-built nesting earns its place when the artefact must be browsable without the
tool — the `obsidian` and `wiki` exports, where nesting is presentation over one graph and therefore
safe.

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

## The two flag surfaces, and which README you are reading (checked 2026-09-04)

An Instagram carousel on graphify → Obsidian (`knowledge/VAULT.md`) sent this page back to the source.
Raw: `knowledge/raw/instagram-graphify-obsidian-2026-09-04/`. It settles the `--obsidian`
question the pilot got wrong twice: **there are two command surfaces, and a flag belongs to
one of them.** `/graphify …` is the *skill*; `graphify extract …` / `graphify export …` is the
*CLI*. `--obsidian` is a skill flag. `--code-only` is an extract flag. Neither is a bug in the
other's surface — and the README says so in its own command reference.

| Claim | Source | Locator | Verbatim | Verdict |
|---|---|---|---|---|
| `--obsidian` is documented on the **skill** surface | README v8 | `Full command reference`, l.678 | `/graphify ./raw --obsidian         # generate Obsidian vault` | MEASURED |
| It can write into an **existing** vault without clobbering it | README v8 | l.679 | `/graphify ./raw --obsidian --obsidian-dir ~/vault  # write into an existing vault (never overwrites your own notes or .obsidian config)` | MEASURED (vendor assertion about its own behaviour; not run here) |
| The README itself separates the two surfaces | README v8 | l.671 | `graphify extract ./raw --code-only # index code only — local AST, no API key (skips docs/PDFs/images); an `extract` flag, not a skill flag` | MEASURED |
| The auto-sync flag is `--watch` | README v8 | l.686 | `/graphify ./raw --watch            # auto-sync as files change` | MEASURED (the carousel frame reads `--match`; the frame is wrong) |
| `main` is **not** the v8 line | README `main` | whole file, 7,106 B vs v8's 62,662 B | `**A Claude Code skill.** Type `/graphify` in Claude Code` | MEASURED |
| `main` documents no Obsidian mode at all | README `main` | grep | (no `--obsidian`, no `export` subcommand; `obsidian/` appears only as an output directory: `obsidian/        open as Obsidian vault`) | MEASURED |
| v8 is the newest branch line | branch fetch | `v1`…`v8` → 200, `v9`, `v10` → 404 | — | MEASURED |
| `Graphify-Labs` and `safishamsi` serve the same `main` | branch fetch | byte comparison | both 7,106 B, sha256 `86382f46b8ebc269` | MEASURED |

**Why this matters for anyone reading this page.** The version diffs above are written against
the **v8** branch README. A reader who fetches the default branch gets a **v1-era** document
(7 KB, no exports, no MCP, no PR tooling) and will conclude this page invented features. Fetch
`.../graphify/v8/README.md`, not `.../main/README.md`.

**`export wiki` and `export obsidian` are not symmetrical (MEASURED 2026-09-04, 0.9.53).**
`export obsidian --dir X` writes to X. `export wiki --dir X` **accepts `--dir`, returns no
error, and ignores it** — the 238 articles land in `wiki/` beside the file `--graph` points at.
Re-measured on **0.9.56** the same evening, after the package shipped three releases in a day: unchanged. Found the way such things are found: by running it, at which point it wrote 238 files into this
repository's immutable `intake/` import, which is not gitignored and would have been committed.
Third instance of this repository's accepted-then-silently-ignored flag class (after
`extract --obsidian` and `extract --no-viz`), and the first with a blast radius.

**Still open.** `--obsidian-dir`'s "never overwrites" was not exercised here — the safe path
stays the one `knowledge/VAULT.md` takes (build a separate vault, move it in yourself). The v8 branch
README is a branch, not a release tag; which PyPI version ships which surface is not measured.

Where this tool sits against every other one the harvest graded, and the one-line reason it was
adopted while its neighbours were not: [[third-party-landscape]], whose invocation-form lesson
this page's claim table is the evidence for.

**The same move, twice in one day.** [[model-agnostic-agent-harnesses]] found goose's repository
transferred from `block/goose` to the `aaif-goose` org while its note still cited the old path -
byte-identical README on both, so nothing broke to announce it. That is this page's
`safishamsi` → `Graphify-Labs` finding in another project, and two instances in one day is the
argument for checking ownership at ingest rather than when something fails: **a project that
changes hands keeps its old URL working, which is precisely why the citation goes stale silently.**


*Version note, 2026-09-11: PyPI `graphifyy` is at **0.9.58** (watched release index; was 0.9.56 when this page last measured anything). **No measurement here is re-dated by that** — every figure above names the version it was taken on, which is exactly what makes a bump cheap to absorb. What the bump does NOT settle is the open question this base still carries: whether `extract --no-viz` does anything, which needs a run and not a release number (`pipeline/reviews/2026-09-08-kb-walkthrough.md`).*
