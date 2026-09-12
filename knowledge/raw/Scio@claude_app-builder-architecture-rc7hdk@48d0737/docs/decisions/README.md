# Decisions

One architectural or product decision per file, numbered sequentially, per `CLAUDE.md`.

Copy `0000-adr-template.md`, number it, set its status.

## Where the proposals are

`docs/next/LAYER-*.md` §9 carries **85 numbered proposals** (A-n … G-n) across the seven layers.
They are *proposals*, not decisions. A proposal becomes a decision when it lands here as a numbered
ADR with a status — not when a layer document argues for it well.

`docs/as-built/01-DECISIONS.md` records the **twenty ADRs of the predecessor system**,
`hello-world`. Those are history, not our decisions. Three of them were never settled, and one
(ADR-0013, validation before building) was decided and then not implemented — which is why this
directory exists rather than being implied.

## The rule that makes this worth keeping

A settled ADR is not overturned in passing. Changing one means arguing against its stated reason,
in a new ADR that supersedes it. That is the whole mechanism: it makes a reversal visible and
costly enough to be deliberate.

## Register

| # | Decides | Status |
|---|---|---|
| 0001 | The code graph is standard, in every repo and every generated app | Accepted |
| 0002 | Two customers, one artefact: the buyer cannot code, the judge is a developer | Proposed |
| 0003 | Scio is written in one language, TypeScript, end to end | Proposed |
| 0004 | Buy the harness: Claude Agent SDK, self-hosted, one sandbox per build | Proposed |
| 0005 | Five layers, not seven, drawn along the predecessor's seams | Proposed — tested by the `architecture` pass |
| 0006 | One vertical slice before any breadth: "just build it" ships first | Proposed |
| 0007 | Evidence is the product surface: every gate on by default, every result rendered | Proposed |
| 0008 | Talents at three levels: guarantees as hooks, boundaries as subagents, advice as skills | Proposed |
| 0009 | Hosted in Scio's ecosystem by default; the code can be bought out, as a key transfer | Proposed |
| 0010 | Whether data is stored, how sensitive, and where, are asked at intake and drive the build | Proposed |
| 0011 | Three stores, not one smart database: graph for code, git-native notes for knowledge, no cross-tenant memory | Proposed |
| 0012 | Data stores per level: SQLite from git while building, one Postgres in Scio, transferable Postgres in every generated app | Proposed |
| 0013 | Commodity by reference, asset by contract: external libraries referenced through an allow-listed registry, never copied | Proposed |

0002–0007 are argued in `docs/REVIEW-FRESH-EYES-2026-09-02.md`, 0008 in
`docs/TALENTS-THREE-LEVELS-2026-09-02.md`, 0009–0010 record the user's answers of 2026-09-02, 0011 in
`docs/TALENTS-CRITICAL-SET-2026-09-02.md` §5, 0012 in `docs/DATA-STORES-THREE-LEVELS-2026-09-02.md`, 0013 in `docs/LIBRARY-SOURCES-2026-09-02.md`; the cold position they were
checked against is `docs/positions/2026-09-02-cold-position-fable.md`.
