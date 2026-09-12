---
title: Skill authoring + eval methodology (from Anthropic's official skill-creator)
sources:
  - url: https://github.com/anthropics/skills
    fetched: 2026-08-27
  - url: https://agentskills.io/specification
    note: canonical Agent Skills spec (the repo's spec/ is now just this pointer)
status: verified
tags: [skills, authoring, eval, description-triggering, methodology]
related: ["[[skill-authoring-best-practices]]", "[[testing-skills-methodology]]", "[[skill-anatomy]]", "[[anthropic-skill-authoring-contract]]"]
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

## Template confirmation
The official `template/SKILL.md` is minimal — `name` + `description` frontmatter + a body
heading, nothing more. This **confirms our required-fields rule** (name+description
mandatory) and that our `templates/` scaffolds are deliberately richer (they add the
method structure the minimal template omits). No change needed; ours are strictly better.

## Verdict (four gates)
- **Adopted as talents:** 0 (all 19 are vertical/library or covered — `mcp-builder` ↔ our
  `mcp-server-patterns`; `skill-creator` ↔ `writing-skills`+`eval-harness`).
- **Knowledge captured:** this note (authoring/eval loop + the two method gaps).
- **Build-candidate:** `skill-description-optimizer` (fills the description-sharpening gap).
- **eval-harness upgrade:** add variance analysis (repeat-N) — small, queued.
- **Library:** the 18 vertical skills, catalogued (harvest per matching project).
- Official-vendor repos ⇒ harvest for **methodology + knowledge**, expect few factory
  talents (distinct from awesome-lists, which yield neither).
