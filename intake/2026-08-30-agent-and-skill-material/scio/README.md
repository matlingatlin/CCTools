# Scio

Tooling and skills for the Scio project.

## What is here

`/graphify` — point it at a folder and it returns a knowledge graph of what is in
there: an interactive `graph.html`, a queryable `graph.json`, and a `GRAPH_REPORT.md`
naming the heavily-depended-on nodes and the cross-file connections nobody would
think to ask about.

Any checkout of this repo picks the skill up automatically; there is nothing to
install first. In Claude Code (or Cursor, Codex, Gemini CLI):

```
/graphify .
```

Code is parsed locally and deterministically with tree-sitter AST. Docs, PDFs and
images go through the calling assistant's model and so cost tokens — `--no-viz` and
`--update` keep that down. Output lands in `graphify-out/`, which is gitignored.

See `.claude/skills/graphify/README.md` for provenance, the pinned sha256, the
re-fetch command, and the one behaviour worth knowing in advance: the skill
pip-installs its own package on first invocation rather than at checkout.
