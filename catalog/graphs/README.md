# Component graphs (Graphify code-only)

Git-persisted knowledge graphs of harvested source repos, built with Graphify
`--code-only --no-viz` (tree-sitter AST, **0 LLM tokens**). Each is a queryable map
of a repo's code — nodes (functions/classes/modules), edges (calls/imports/inherits,
tagged EXTRACTED/INFERRED), and Leiden communities (subsystems).

## Use
- Navigate an unfamiliar donor repo cheaply: `graphify explain "<name>"`,
  `graphify path "A" "B"`, or read `GRAPH_REPORT.md`.
- Refresh after the repo changes: `graphify update <repo>` (no API cost).
- `graph.json` is the queryable artifact; commit it so it survives the container.

## Graphs
- `ecc/` — affaan-m/ECC: 11,915 nodes · 24,494 edges · 606 communities (2026-08-27).

## Factory step (adopted)
Harvesting a code-heavy GitHub repo now includes: clone → `graphify extract <repo>
--code-only --no-viz` → commit `graph.json` + `GRAPH_REPORT.md` here. Pilot confirmed
Graphify runs in our environment at zero LLM cost and its file output fits git.
