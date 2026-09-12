---
name: as-built
layer: build-process
phase: build-time
status: written
description: Answer questions about what the predecessor system (hello-world) actually does — its layers, invariants, decisions and known defects — from the as-built documents in this repo. Use whenever a task depends on how the old system worked, before designing a replacement for any part of it, or when someone asks what is already built.
---

# as-built

Everything established about `matlingatlin/hello-world` lives in `docs/as-built/`. It was
written so this repo is sufficient on its own.

**Do not clone or open hello-world.** If you believe you need to, say why first — the answer
is almost always already here, and re-deriving it costs hours.

## Load in this order, and stop when the question is answered

1. **`00-INDEX.md`** — always first. Layer sizes, dependency edges, test counts, verified
   baseline, what is known missing. Most questions end here.
2. **`ARCHITECTURE-AS-BUILT.md`** — for anything about the system as a whole: the pipeline,
   the invariants, where trust and money live, what a rebuild must carry.
3. **`01-DECISIONS.md`** — for *why* something is shaped as it is. Check this before calling
   any design odd; several oddities are reasoned, and three ADRs are not settled.
4. **One `LAYER-*.md`** — only the layer the question touches. They are 20–35 KB each. Loading
   all seven wastes most of a context window.
5. **`graph/graph.json`** — for symbol-level lookups. Query it; do not read source.

| Question is about | Load |
|---|---|
| conversation, spec, questions, provenance, the gate | `LAYER-A-INTAKE.md` |
| the whole, architecture graph, playbook, validation rules | `LAYER-B-UNDERSTANDING.md` |
| build packages, contracts, decomposition, acceptance criteria | `LAYER-C-BUILD-PLAN.md` |
| the component library, matching, contribute-back | `LAYER-D-LIBRARY.md` |
| building, gates, sandbox, relay, spend, jobs | `LAYER-E-BUILD.md` |
| preview, markings, directed change, promotion, ship | `LAYER-F-DESIGN-WINDOW.md` |
| auth, tenancy, schema, migrations, metering, streaming | `LAYER-G-CROSS-CUTTING.md` |
| what a user actually experiences, end to end | `JOURNEY-INVOLVED-PATH.md` |
| what the old reviews say, and the MVP definition | `REVIEWS-WHAT-WE-MISSED.md` |
| whether a specific review finding still holds | `REVIEWS-FINDINGS-VERIFIED.md` |

## Querying the graph

5,173 nodes and 12,054 edges over the old repo — code by tree-sitter AST, documents extracted
semantically.

```python
import json
from networkx.readwrite import json_graph
G = json_graph.node_link_graph(
    json.load(open('docs/as-built/graph/graph.json')), edges='links')

[n for n in G.nodes if 'intake' in n.lower()]          # find symbols
list(G.neighbors('<node_id>'))                          # what it touches
G.nodes['<node_id>']                                    # source_file, label, community
```

## How to read a layer document

Seven headings, always the same. **Heading 6, State**, is the one that decides things:

- **Solid** — carry forward unchanged. Rebuilding it loses work and reintroduces closed bugs.
- **Deliberate, easy to break by accident** — reasoned trade-offs. Changing one means arguing
  against a stated reason, in an ADR, not in passing.
- **Wrong-shaped** — it works, but its form is wrong for what it is asked to do.
- **Missing** — never built.
- **Obsolete** — remove.

Each layer ends with **Documentation drift found** — places where hello-world's own docs
contradict its code. Those docs are unreliable; these documents and the code are not.

## Standing facts worth knowing before you plan anything

- The intake agent **is** built and has run for real. `STRATEGY.md` in the old repo says it is
  not; that file is stale.
- Layer C's plan validation runs on every build and **nothing reads the result**, though
  ADR-0013 required validation before building.
- The library's matchable catalog is effectively **one entry**; three of four have empty
  contracts.
- A cross-tenant idempotency replay in `BuildService.run` precedes the ownership guard, and
  the e2e doubles are stricter than production, so the suite cannot catch it.
- The Clerk webhook checks a signature's presence, never its cryptography.
- There are **35** review findings, not 34, and the most serious one (the tenancy breach) was
  found by only one of the two reviewers.
- **Five** routes are placeholders, not one — including `/live` ("Refine"), which is where
  Level 1 users were supposed to shape their app after the build.
- The baseline below is **one observation, not proof of stability**: `design.test.tsx` is
  recorded as flaky (B105).
- Verified baseline, 2026-08-26: engine 640 passed / 21 skipped, API 135, app 109, typecheck
  clean. The 15 extra skips need pglite, a live catalog DB, or a built Next app.

## Rules

**Cite where you got it.** `LAYER-E-BUILD.md §6` or `file:line`, not "the docs say".

**Do not trust a claim these documents mark unverified.** At least one exists, flagged as
such; treat it as a question, not a fact.

**When two documents disagree, stop and go to the code.** This is the one case where the
no-cloning rule yields, and it is not hypothetical: a measured ablation on 2026-08-26 had a reader
following this skill hit `00-INDEX` saying *seven rules* and `LAYER-C-BUILD-PLAN` saying *nine*,
resolve it from the graph, and **answer wrongly** — while a reader without this skill opened
`validate.py`, counted, and got it right. The graph gave seven because call edges count *functions*;
the answer was nine because violations carry *rule names*. **A graph query cannot settle a
disagreement about units.** Say which documents disagree, read the one file that decides it, and
report the number with the unit attached.

**A retrieval budget is not an accuracy budget.** This skill exists to stop hours of re-derivation,
not to make a wrong answer cheap. Cheap and wrong is the worst outcome available here.

**Say when the answer is not here.** These documents cover what was examined on 2026-08-26.
The frontend beyond the page inventory, and the two root production-readiness reviews, are
thin. Guessing to fill a gap is how a rebuild inherits a defect nobody chose.
