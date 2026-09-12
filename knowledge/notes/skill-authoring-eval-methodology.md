---
title: Skill authoring + eval methodology (from Anthropic's official skill-creator)
sources:
  - url: https://github.com/anthropics/skills
    fetched: 2026-08-27
  - url: https://agentskills.io/specification
    note: "canonical Agent Skills spec (the repo's spec/ is now just this pointer). Fetch date not recorded at write time and not recoverable from SOURCES.md or this note - null rather than invented. anthropic-skill-authoring-contract fetched the same URL on 2026-08-30; that is that note's read, not this one's."
    fetched: null
tags: [skills, authoring, eval, description-triggering, methodology]
related: ["[[skill-authoring-best-practices]]", "[[testing-skills-methodology]]", "[[skill-anatomy]]", "[[anthropic-skill-authoring-contract]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Skill authoring + eval methodology — from the official `skill-creator`

Harvested from `anthropics/skills` (wave 5). The repo is mostly high-quality **vertical
library** skills (docx, pdf, pptx, xlsx, canvas/frontend/theme design, internal-comms,
slack-gif, web-artifacts, webapp-testing) — polished, but not factory infrastructure.
The factory-relevant value is the **method** inside `skill-creator`.

## The authoring→eval loop (canonical)
1. Decide what the skill does and roughly how.
2. Write a draft.
3. Write a few **test prompts**; run *Claude-with-the-skill* on them.
4. Evaluate qualitatively AND **quantitatively** — draft quantitative evals if none exist;
   view results, look at metrics.
5. Rewrite from the eval feedback (and any glaring benchmark flaws).
6. Repeat; then **expand the test set and re-run at larger scale**.
7. Run the **description-improver** to optimize triggering accuracy.

## Two things this adds over our current talents
**And that sentence is the resolution to a standing contradiction (2026-09-12).**
[[anthropic-skill-authoring-contract]] quotes best-practices as *"Create evaluations BEFORE writing
extensive documentation"*, with its own steps running **without-skill baseline → minimal
instructions**. The loop above opens at *"write a draft"* and has **no without-skill step at all**, so
the two were recorded as opposite orderings. They are not: they differ on **whether a baseline is
taken before anything is written**, and the contract's deferral is of *extensive* documentation, not
of all writing. The contract's claim that this note "confirmed" its ordering has been retracted there
— a loop cannot confirm an ordering whose first step it omits.

Our `writing-skills` covers authoring and `eval-harness` covers baseline-vs-with. Two
methods here fill real gaps:

- **Description-triggering optimizer.** A dedicated pass that optimizes a skill's
  `description` for *when it fires* — precisely the "sharpen overlapping descriptions"
  flag `wave-reflect` produces but has no method to execute. GAP → candidate talent
  `skill-description-optimizer` (build-on-demand; a METHOD, we do not adopt the repo's
  script — security gate).
- **Variance analysis.** Run the benchmark **multiple times** and measure variance, not a
  single pass — so a skill isn't judged on one lucky/unlucky run. `eval-harness` should
  gain a "repeat N times, report variance" option. Low-effort rigor upgrade.

## What running this loop then measured

Everything above is the loop **as prescribed**. [[testing-skills-methodology]] is the same loop
**as run here**, and it is where the two diverge — the variance point above turned out to be the
smaller half of the problem. Measured there: most expectations in this library carry no verdict
at all, a predicted gap was refuted 2 of 2 times, correctness alone would have discarded a skill
worth keeping, and a review round repeats because it is whack-a-mole rather than disagreement.
Read step 4's "evaluate qualitatively AND quantitatively" against those, and the missing
instruction is visible: the loop says nothing about who writes the expectations, or when a
failing one means the *expectation* was wrong.

## Template confirmation
The official `template/SKILL.md` is minimal — `name` + `description` frontmatter + a body
heading, nothing more. This **confirms our required-fields rule** (name+description
mandatory) and that our `templates/` scaffolds are deliberately richer (they add the
method structure the minimal template omits). No change needed; ours are strictly better.

**Upgraded from inference to verbatim, 2026-09-12.** "Mandatory" was read off the minimal template's
*shape*; the specification says it outright. From the copy held since 2026-09-04
(`knowledge/raw/baseline-2026-09-04/agentskills.io_specification.html`): *"The **required** `name`
field"*, *"The **required** `description` field: Must be **1-1024 characters**"*, against *"The
**optional**"* for `license`, `compatibility`, `metadata` and `allowed-tools`. **MEASURED**, not
inferred.

This also resolves a standing contradiction with [[skill-anatomy]], which says the fields are "all
optional". Both hold: that page describes what *Claude Code's loader* tolerates, this one what the
*spec* requires, and neither carried the scope clause until now. Omitting them is spec-violating and
still runs.

**And the 1,024 is a limit, not a style note.** `DESCRIPTION_CAP_CHARS` in `pipeline/CONSTANTS.md` had
been marked `cited`+`decided`; it is now sourced to this sentence. Measured the same day: **13** units
in this library have descriptions longer than 1,024 characters, from 1,037 to 1,446 — and the
`desc_headroom` gate sees only 5 of them, because its target answers a *different* constraint (the
host's silent 1,536-character truncation wall). Trimming changes routing, which this library's own rule
says must be proven against a baseline, so this is a finding for the human and not a fix to apply.

## Verdict (four gates)
- **Adopted as talents:** 0 (all 19 are vertical/library or covered — `mcp-builder` ↔ our
  `mcp-server-patterns`; `skill-creator` ↔ `writing-skills`+`eval-harness`).
- **Knowledge captured:** this note (authoring/eval loop + the two method gaps).
- **Build-candidate:** `skill-description-optimizer` (fills the description-sharpening gap).
- **eval-harness upgrade:** add variance analysis (repeat-N) — small, queued.
- **Library:** the 18 vertical skills, catalogued (harvest per matching project).
- Official-vendor repos ⇒ harvest for **methodology + knowledge**, expect few factory
  talents (distinct from awesome-lists, which yield neither).
