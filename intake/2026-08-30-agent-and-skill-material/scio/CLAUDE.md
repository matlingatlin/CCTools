# Project: Scio

An AI app builder. Someone who cannot write software describes what they want, and gets
an application they own.

This repo is the **rebuild**. The working predecessor lives in `matlingatlin/hello-world`
— roughly 26,000 lines across four workspaces, built without research, skills, an architect
pass, or deliberate tooling. It works. It is not assumed correct.

## Where knowledge about the old system lives

`docs/as-built/` — everything we established about hello-world, written so this repo is
sufficient on its own.

**Read in this order. Do not open hello-world unless a document sends you there.**

1. `docs/as-built/00-INDEX.md` — the macro map. Start here, always.
2. `docs/as-built/01-DECISIONS.md` — the 20 ADRs of the old system, and what each governs.
3. `docs/as-built/LAYER-*.md` — one per layer. **Load only the layer your task touches.**
4. `docs/as-built/graph/graph.json` — 5,173 nodes, 12,054 edges over the old repo. Query it
   for symbols and dependencies instead of reading source.

Every layer document carries the same seven headings, and heading 6 (**State**) is the one
that matters: solid · wrong-shaped · missing · obsolete. A description is a manual; a
judgement is grounds for rebuilding.

## How we work

**Position before history.** Write your own position on a problem *cold* — before reading
the old code, before the reviews, before scanning what others do. A position written
afterwards is a critique of what exists, not an independent answer, and the two cannot be
told apart later. Mark any late position `informed` and weigh it less.

**Scan before building.** Every step checks what exists now: tools, skills, connectors, MCP
servers, repos, research papers, and what practitioners report. Two addressees each time —
our build process, and the product. They are rarely the same list.

**Never answer from memory** on tools, models, prices or versions. Look them up and date the
answer. A model's knowledge cutoff is months behind the present.

**Verify before acting.** A claim that will drive work is checked against primary source:
`file:line` for code, the repo's own `LICENSE` for a licence, the paper itself for a finding.
Reviews are dated and code moves under them. Findings are claims, not facts.

**Four allowed outcomes** for any question: build · complete · keep · park. *Keep* — deciding
the existing design is wiser than the new idea — is a real outcome and must be written down
with its reason, so the question does not come back.

**Budget before parallel work.** Say what a step may cost before dispatching agents. Run
deterministic passes first, model passes last and in small batches, writing partial results
to disk so an interruption costs one batch and not the run.

## Not yet decided — do not invent

The stack for this repo is **open**. hello-world's choices (NestJS, Prisma, Postgres, Clerk,
Azure) are evidence, not inheritance. Propose an ADR; do not decide silently.

## Conventions

- Commits: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:` …).
- ADRs: one decision per file in `docs/decisions/`, numbered, with status.
- Definition of done: built + tested + documented + committed. Never leave work in a session.
- `/checkpoint` documents, changelogs and commits everything outstanding.
