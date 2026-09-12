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
