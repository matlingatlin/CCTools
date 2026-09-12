# as-built — what `hello-world` actually is

Written so this repo is sufficient on its own. A session working here should be able to
answer what the old system does, how its parts connect, and what state each part is in,
**without opening `matlingatlin/hello-world`**.

## How to use this directory

| Read | When |
|---|---|
| `00-INDEX.md` | Always, first. The macro map. |
| `01-DECISIONS.md` | When you need to know *why* something is shaped as it is. |
| `LAYER-*.md` | Load only the layer your task touches. |
| `graph/graph.json` | To look up a symbol, its callers, or its dependents. |
| `JOURNEY-INVOLVED-PATH.md` | To see one user's path end to end, and where intent and reality part. |

Do not read every layer document. They exist so you can load one.

## The seven headings every layer document carries

1. **Purpose** — what the layer exists to do
2. **Public surface** — what other layers touch
3. **In and out** — what it consumes, what it produces
4. **Invariants** — taken from the tests, with test names as evidence
5. **Dependencies** — up and down, from the graph
6. **State** — solid · wrong-shaped · missing · obsolete
7. **Open questions** — and what would settle them

Heading 6 is the point. The old system was built without research, skills or an architect
pass; describing it is not enough, it has to be judged.

## The graph

`graph/graph.json` — 5,173 nodes, 12,054 edges over hello-world, from
[graphify](https://github.com/Graphify-Labs/graphify). Code is tree-sitter AST (deterministic,
covering 326 source files and the 12 SQL migrations); documents were extracted semantically.

Query it rather than reading source:

```python
import json, networkx as nx
from networkx.readwrite import json_graph
G = json_graph.node_link_graph(json.load(open('docs/as-built/graph/graph.json')), edges='links')
[n for n in G.nodes if 'intake' in n.lower()]        # find
list(G.neighbors('some_node_id'))                     # what it touches
```

**One known gap.** The semantic pass covers 59 of 79 documents. The batch that failed held
the two root production-readiness reviews, the continuous-improvement runbook and the
per-workspace `CLAUDE.md` files. Those were read manually instead, so the knowledge is in the
layer documents — but they are thin in the graph.

## Status

| Phase | State |
|---|---|
| 0 · Scio skeleton, graph committed | done |
| 1 · Module map, decision register, test index | done |
| 2 · Seven layer documents | done |
| 3 · Macro synthesis | done — `ARCHITECTURE-AS-BUILT.md` |
| 4 · Navigation skill | done — `.claude/skills/as-built/` |
| 5 · Blind test with a fresh agent | done — failed on two stale claims in `00-INDEX.md`, corrected |
