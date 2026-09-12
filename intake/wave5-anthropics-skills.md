---
source: github anthropics/skills (official)
harvested: 2026-08-27
by: piano wave 5 (harvester, github primary-source method)
status: intake (verified — gates applied on contents)
---

# Wave 5 intake — anthropics/skills (official)

Inventory: 19 skills + `spec/` (now just a pointer to agentskills.io/specification) +
`template/SKILL.md` (minimal). Cloned, listed, gates applied.

## Talent-worthiness verdict: LIBRARY + methodology, not factory talents
- **18 vertical/library skills** — `docx`, `pdf`, `pptx`, `xlsx` (doc tooling);
  `canvas-design`, `frontend-design`, `theme-factory`, `brand-guidelines`, `algorithmic-art`,
  `web-artifacts-builder`, `slack-gif-creator` (design/artifact); `internal-comms`,
  `doc-coauthoring`, `academy-guide`, `discernment-nudge` (comms/guide); `claude-api`
  (reference); `webapp-testing` (Playwright). → **library tier**, pulled per matching project.
- **Covered (reuse-first):** `mcp-builder` ↔ our `mcp-server-patterns`; `skill-creator` ↔
  `writing-skills` + `eval-harness` (but see the two method-gaps below).

## Adopted this wave: 0 talents
Correct — official repo is polished verticals, not factory infrastructure. Security gate
also blocks adopting `skill-creator`'s bundled scripts (we take the method, not the code).

## Value extracted
- **Knowledge note:** `knowledge/notes/skill-authoring-eval-methodology.md` — the
  authoring→eval loop, plus two real gaps.
- **Build-candidate:** `skill-description-optimizer` (systematic description-triggering
  optimizer — executes wave-reflect's "sharpen" flag). Build-on-demand.
- **eval-harness upgrade (queued):** add **variance analysis** (repeat-N, report variance).
- **Template confirmation:** canonical `template/SKILL.md` is name+description+heading only
  → confirms our required-fields rule; our `templates/` are richer. No change.

## Lesson for the loop
Official-vendor repos = high-quality LIBRARY + occasional METHODOLOGY; harvest them for
knowledge notes + method gaps, expect ~0 factory talents. (Distinct from awesome-lists,
which yield neither — those stay deprioritized.)
