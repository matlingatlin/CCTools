# next — what to build, and why

`docs/as-built/` records what `hello-world` **is**. This directory records what to **do** with
it: refinements to what exists, functions that are missing, and the means — skills, MCP,
connectors, repos, research — that make each one decidable.

One document per layer, same nine headings. (This originally specified seven; every document
expanded where the material demanded it, and all seven now carry the same nine.)

1. Where the layer stands
2. Refining what exists
3. What is missing
4. Out of the box — the wide brainstorm
5. The means — skills, MCP, repos, research
6. Retrieval versus packing
7. Token economy
8. Data worth owning
9. ADR proposals

**Nothing here is decided.** Every behavioural change lands as an ADR proposal in §9, per
`CLAUDE.md`: propose, do not assume. **85 proposals now exist across the seven documents**, and
they land in `docs/decisions/` as ADRs before they land in code.

Two axes run through every document and exist nowhere in `as-built/`:

- **Token economy** — where tokens go per layer, and what can be cached, reused, or made
  deterministic. Measured against the real prompts, not estimated.
- **Data worth owning** — what each layer produces that is worth keeping. Most of it already
  passes through and is discarded.
- **Retrieval versus packing** — where a layer sends context it could have queried instead.
  This is graphify's principle rather than graphify the tool, and it applies to every model
  call in the system.

Cross-cutting, not per layer:

- **`SKILLS.md`** — every skill, how one is written, and the four-part format every
  research-derived skill must carry: source, method, limits, eval.
- **`.claude/skills/app-design`** — why generated apps look generated, and the token contract
  plus deterministic design gate that fixes it. Sections 1–4 are written to become Layer B
  playbook content.

| Layer | Status |
|---|---|
| A · Intake | done |
| B · Understanding | done |
| C · Build plan | done |
| D · Library | done |
| E · Build & execution | done |
| F · Design window | done |
| G · Cross-cutting | done |
