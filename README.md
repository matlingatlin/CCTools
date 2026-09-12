# CCTools — a talent library and its tooling, kept inert

Everything here comes from `matlingatlin/skills-repo`, split up on 2026-09-12. The app work went
to `matlingatlin/BusinessIdeas` and `matlingatlin/Karamellfarbrorn`; everything else came here.

**Nothing in this repository is active.** No skill loads, no agent is dispatchable, no talent
triggers, and no `CLAUDE.md` steers a session. That is deliberate and it is structural rather
than a promise: **the path `.claude/` is the activation**, and it does not exist here. A clone of
this repository adds nothing to a session's context.

```
library/skills/              89 skills          — were adopted and measured
library/agents/               3 agents          — kb-curator, rag-pipeline-reviewer, skill-builder
library/skills-candidates/    1                 — artifact-consistency-sweep, never adopted
knowledge/                   44 notes, 252 watched raw files, and the tools that check them
pipeline/                    the factory: build chain, gates, ledgers, decisions, 15 root documents
templates/                    6 authoring scaffolds
evals/                        5 routing cases — see evals/README.md, they cannot run here
catalog/ intake/ entities/   harvest records and 422 files of harvested third-party material
scio-architecture-five-layer/ 10 notes and 44 held source files, parked, not yet in the knowledge base
docs/steering/               the former CLAUDE.md and plugin manifest, archived off the live paths
```

## To put a unit back into service

Copy it under the project's own `.claude/`: a skill directory to `.claude/skills/<name>/`, an
agent file to `.claude/agents/<name>.md`. That one move is the whole of activation — which is
also why simply storing the library here cannot activate it by accident.

Read `docs/steering/CLAUDE-md-archived.md` first. It is the former always-on brief, and its
capability map is the part worth keeping: it names **79 talents** and says which one owns which
job, which sibling to prefer, and the boundary between them. Descriptions alone do not carry
that. The map's paths were rewritten to `library/…`; nothing else in it was changed.

`library/skills-candidates/artifact-consistency-sweep` is separate from the other 89 on purpose.
It was committed as a candidate and never adopted, because adoption required a measurement it
never got. Keeping it in its own directory is not bookkeeping: folding it in with the rest makes
`desc_headroom` read 98 descriptions instead of 92, because it carries five eval **fixtures**
that are each a valid `SKILL.md`, and one of them then reports as an over-target talent.

## The checks still run, and they were rewired in the same commit as the move

Four controls pointed at `.claude/`, and a path left pointing there does not fail loudly — it
reads nothing and reports success, which is the worst of the available outcomes. All four were
moved with the files:

| control | was | is |
|---|---|---|
| `knowledge/kb.py` `AREAS` | `.claude/skills/*/SKILL.md`, `.claude/agents/*.md` | `library/skills/*/SKILL.md`, `library/agents/*.md`, plus a `docs/steering/*.md` area |
| `pipeline/queries/desc_headroom.py` | `.claude/skills`, `.claude/agents` | `library/skills`, `library/agents` |
| `.github/workflows/kb-check.yml` path filter | `.claude/**` | `library/**`, `docs/**` |
| `evals/` | asserted four named skills fire | unchanged, and `evals/README.md` says why they cannot run here |

`context_surface.py`, `signals.py` and `preflight.py` followed. `kb.py`'s own selftest asserts
that every area it indexes is covered by the CI trigger, so a fifth path added later without its
filter fails the check rather than going quiet.

Measured after the move, all seven gates green and every figure matching the reading taken in
`skills-repo` before it:

```
kb.py check ........................ PASS   713 documents, 9 indexed areas, uncovered=none
watch.py --selftest ................ PASS   29 fixtures
watch.py --offline ................. PASS   96 rows, 252 raw files, 156 accounted for unwatched
pdftext.py --selftest .............. PASS   52 fixtures
pdfread.py --selftest .............. PASS   10 fixtures
desc_headroom.py --selftest ........ PASS   21 fixtures
desc_headroom.py --gate ............ PASS   92 descriptions, 5 declared above target
```

713, the same count as before the move. The root area lost `CLAUDE.md` and gained this
`README.md`, and the archived steering file is indexed under its own `docs/steering/*.md` area —
so the index is the same size by arithmetic rather than by luck, and `evals/README.md` is not in
it because no area globs `evals/`.

## `scio-architecture-five-layer/` is the one folder with work left in it

10 notes and their 44 held source files, drained from a session branch and never promoted. Its
own README states the re-entry condition per item, and that condition is now easier to meet than
it was: the notes need a `raw:` key that is reconstructible from the `Feeds` column of the four
`MANIFEST.md` files, and the raw directories need rows in `knowledge/raw/WATCH.tsv` or a
`NEVER_WATCHED` declaration — and `kb.py`, `watch.py` and `WATCH.tsv` all live in this same
repository now. Until that is done the folder is not part of the knowledge base and the checks
do not see it.
