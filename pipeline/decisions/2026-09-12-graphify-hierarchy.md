# Does `--resolution` give a HIERARCHY, or only alternative flat partitions? — preregistered 2026-09-12

**Written before graphify was installed.** The question came from a design proposal: build multi-level
graphs, each node exploded into its own graph, level after level. Answered once already from the held
READMEs — *"more, smaller communities"*, no parent/child community id documented anywhere — and that
answer was recorded as **README-grounded, not measured**. This is the measurement.

It matters because the two readings imply different designs. If communities nest, graphify already
gives you levels. If they do not, a hierarchy has to be **derived**, and the only sound way to derive
one is by intersecting partitions from a *single* extraction — re-running graphify per subtree loses
every edge crossing the boundary, which is the failure mode this base has already argued from god nodes
not respecting directory structure.

## The metric, fixed now

**Q1 — is there a declared hierarchy?**
- **REFUTED (a hierarchy exists)** if the graph artefacts carry, for communities, any of: a parent id,
  a level or depth field, a nested/tree structure, or ids that are prefixes of finer ids.
- **CONFIRMED (flat)** if community membership at each resolution is an independent flat labelling with
  no declared relationship between resolutions.

**Q2 — can a hierarchy be DERIVED, and is it sound?** Run one extraction, then cluster twice:
a coarse resolution and a fine one. For each fine community, count how many coarse communities its
members fall into.
- **DERIVABLE** if ≥90% of fine communities sit inside exactly one coarse community. Then
  coarse→fine is a real parent→child tree and nesting is safe.
- **NOT DERIVABLE** if fine communities routinely straddle coarse ones. Then "levels" are two
  incompatible cuts of the same graph and presenting one inside the other would misrepresent it.

90% is chosen before seeing any number, as the point where a tree is usable with a named exception
list rather than being a fiction. It is not tuned; if the result lands near it, the verdict is
reported at the measured value and the threshold is not moved.

## Constraints

1. **Fourth gate.** Install is `uv tool install` / venv from PyPI, **wheel only** (a `bdist_wheel`
   exists for 0.9.58, so no `setup.py` runs at install time). Core deps are `networkx`, `numpy`,
   `rapidfuzz` and tree-sitter grammars — **no credential or network libraries**; every LLM provider is
   an optional extra and none is installed. Apache-2.0. The binary's own `install` subcommand is
   **NOT** run: this base records that it writes MCP client configs unless `--skip-config`.
2. **No model calls.** Community labelling is skipped (`--no-label`); nothing here needs inference, and
   an unmetered spend would have to be recorded as `null` anyway.
3. **Read-only against the target.** The target is `/home/user/hello-world` (285 code files). Graph
   output goes outside it; the repo is not modified.
4. **Budget.** One extraction with `--no-viz` (this base records `graph.html` as slow above 5,000 nodes,
   and the ECC pilot measured 11,915 nodes on this repo), then two `cluster-only` runs — which re-run
   clustering **without re-extracting**, the one cheap thing the READMEs promise. If extraction exceeds
   ~15 minutes it is abandoned and reported as abandoned, not silently retried.

## Stop rule

One install, one extraction, two clusterings. If the extraction fails for an environmental reason
(missing grammar, a wheel that will not build), that is a **FAIL of the measurement, not of the
claim**, and the README-grounded answer stands as the best available with its provenance unchanged.
No second tool is installed to rescue the first.

## Outcome — Q1 confirmed, **Q2 FAILED and it refutes my own earlier recommendation**, Q3 answers it

Written before the result was used for anything. graphify 0.9.58 installed wheel-only into a scratch
venv with the `leiden` extra; verified afterwards that `anthropic`, `openai`, `google`, `boto3`,
`requests` and `httpx` are all **absent**, so nothing here could have made a model call. The binary's
`install` subcommand was not run. The target was a **copy** of hello-world in the scratchpad; the real
repo is untouched (`git status` clean, no `graphify-out/`).

**Extraction, measured:** `graphify extract . --code-only --no-viz` → **4,499 nodes, 11,263 edges, 189
communities** over 326 code files, no LLM. Not comparable to the ECC pilot's 11,915 nodes on the same
repo: that run included docs and semantic extraction, this one is AST-only. Two different measurements,
not a contradiction. (Also surfaced: 12 `.sql` files contributed nothing — `tree_sitter_sql` needs the
`[sql]` extra.)

### Q1 — is there a declared hierarchy? **CONFIRMED FLAT.**

From the installed source, not the README. `build.py:2220` writes `data["community"] = cid` — a single
integer per node. `cluster.py`'s own docstring: *"Uses Leiden (graspologic) if available, falls back to
Louvain (networkx). Splits oversized communities."* The call is `gn.leiden(..., resolution=resolution)`,
the **flat** variant. No parent id, no level field, no dendrogram anywhere in the package.

Two corrections to the README-grounded answer this replaces:
- **`--resolution` and `--exclude-hubs` are real but UNDOCUMENTED in `--help`.** They are parsed at
  `cli.py:2034` and `cli.py:3311`. The README shows them; the CLI's own help does not. The earlier note
  was right about the flags and would have looked wrong to anyone who checked `--help` instead.
- **On Python ≥3.13 it does not break — it falls back to Louvain.** The earlier note said what
  partitions instead was "undocumented"; `cluster.py` documents it in its first line.

### Q2 — can a hierarchy be DERIVED by intersecting resolutions? **NOT DERIVABLE. 76.6% against 90%.**

Coarse (`resolution=0.5`) → 55 communities. Fine (`resolution=2.0`) → 77. Of those 77 fine
communities, **59 sit inside exactly one coarse community and 18 straddle**, the worst spanning **4**
coarse communities while holding 196 nodes. **76.6%**, against a threshold of 90% fixed before any
number existed. The verdict is FAIL and the threshold is not moved.

**This refutes what I recommended to the user an hour earlier**, in `graphify-features` and in chat:
*"nesting a fine partition inside a coarse one — both from the same extraction — gives parent/child
levels with every edge intact."* The edges survive, which was the point I was defending; **the tree
does not**. The reason is now obvious and was not checked: each `_partition` call is an *independent*
optimisation over the whole graph, so a finer run is not a refinement of a coarser one. Nothing
constrains them to nest, and measurement says they do not. The note has been corrected.

### Q3 — the mechanism that does work, and graphify already ships it

A separate question, asked after Q2's verdict was recorded, and it cannot rescue it: `graspologic.partition`
exposes **`hierarchical_leiden`** beside the flat `leiden` graphify calls. On the same graph's largest
connected component (3,182 nodes, 8,745 edges): **level 0 = 21 clusters, level 1 = 132 clusters, and
132 of 132 have exactly one parent — 100.0%.** Levels by construction, because each level *is* a
refinement of the one above.

**Caveat, measured:** it needs a connected graph. 1,317 of 4,499 nodes (**29%**) lie outside the giant
component and get no place in the hierarchy at all. A design that presents the tree as complete would
be hiding almost a third of the graph.

**So the design answer is: the levels are real and one function call away, in a dependency graphify
already installs for its `leiden` extra — but they must come from `hierarchical_leiden`, not from
re-running extraction per subtree (loses cross-boundary edges) and not from intersecting resolutions
(measured at 76.6% single-parent, which is not a tree).**

## Postscript — the 29% caveat is not noise, and it hands you level 0 for free

The Q3 caveat was recorded as "1,317 of 4,499 nodes lie outside the giant component". Left there it
reads as fringe. Measured properly:

| | |
|---|---|
| components | **48** |
| giant | 3,182 nodes (70.7%) |
| **second** | **1,089 nodes** |
| isolated single nodes | **8** — i.e. **0.6%** of what is "outside" |

So the outside is not dust: 1,309 of those 1,317 nodes sit in **real components**, and the second
largest is a 1,089-node subsystem with **no edge at all** to the first. Identified from
`source_file`:

- **Component 0 (3,182)** — `apps/engine` 2,818, plus the marking spikes. **The Python engine.**
- **Component 1 (1,089)** — `apps/api` 435, `apps/app` 241, `packages/shared` 121. **The TypeScript
  stack: NestJS API, the frontend, the shared package.**

They are disconnected because they do not import each other — they talk over HTTP and a queue. Nothing
is wrong with the graph; the repo genuinely has two islands.

**Two consequences, and the second is the useful one.**

1. **`hierarchical_leiden` on the giant component alone would silently omit the entire TypeScript
   stack** — 24% of the graph, and the half a web developer would be looking for. The Q3 result stands
   but its construction must be **per component**, yielding a *forest* with one tree per subsystem.
2. **The top level of the hierarchy comes free from connectivity, and it is more meaningful than any
   Leiden level.** Level 0 = connected component ≈ language/workspace boundary, computed with no
   algorithm and no parameter. Leiden then refines *inside* each island. That is the principled version
   of the multi-level design, and it needed no clustering to discover — only asking how many components
   there were.

**And a caution for anything reasoning over "the graph":** a tool that assumes one connected structure
is wrong about this repo. Scio's held graph (`docs/as-built/graph/graph.json`, 5,173 nodes / 12,054
edges) describes the same codebase; whether it is also a forest is unchecked here.
