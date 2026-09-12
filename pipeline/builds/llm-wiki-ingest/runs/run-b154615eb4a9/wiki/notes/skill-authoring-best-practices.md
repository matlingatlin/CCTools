---
title: Skill authoring best practices
sources:
  - url: https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md
    fetched: 2026-08-27
  - url: https://github.com/obra/superpowers/blob/main/skills/writing-skills/anthropic-best-practices.md
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/skills
    fetched: 2026-08-27
status: verified
tags: [claude-code, skills, authoring, testing]
related: ["[[skill-anatomy]]", "[[long-text-comprehension]]", "[[anthropic-skill-authoring-contract]]", "[[testing-skills-methodology]]", "[[loop-engineering-and-fable-prompting]]", "[[prompt-patterns-kernel]]"]
---

# Skill authoring best practices

Where the three sources agree, treat these as settled rules.

## The description rule (highest-leverage finding)

The `description` must state ONLY the triggering conditions — never summarize the
skill's workflow. Superpowers' testing showed that a workflow summary in the
description becomes a shortcut: the agent follows the one-line summary and skips
the skill body (an agent did ONE review when the flowchart required TWO, purely
because the description said "code review between tasks").

- Start with "Use when …", third person, concrete symptoms/situations/keywords.
- Include terms an agent would search for: error messages, symptoms, tool names.
- The official docs phrase it as "what it does and when to use it" — the
  superpowers refinement (triggers only) is stricter and empirically motivated;
  we follow the stricter form.

## Conciseness

- Context is a public good. Only add what the agent doesn't already know;
  challenge every paragraph ("does this justify its token cost?").
- SKILL.md body under 500 lines; frequently-loaded skills far smaller
  (superpowers targets: <200 words for always-loaded, <500 for others).
- One excellent example beats many mediocre ones. No multi-language dilution.
- Move heavy reference to separate files (progressive disclosure), linked
  **one level deep** from SKILL.md only; files >100 lines get a table of contents.
- Prefer bundled scripts (executed, not read) over inline code for deterministic
  operations; document script constants (no voodoo numbers).

## Degrees of freedom

Match specificity to fragility:
- **High freedom** (prose heuristics) when many approaches are valid.
- **Medium** (templates/pseudocode) when a preferred pattern exists.
- **Low** (exact commands, "do not modify") when operations are fragile —
  narrow bridge vs open field.

## Structure that works

- Checklist workflows for multi-step tasks (agent copies checklist, ticks off).
- Feedback loops: validate → fix → re-validate; only proceed when clean.
- Conditional workflows keyed to observable predicates ("if X exists → path A").
- Consistent terminology (one term per concept, always).
- No time-sensitive phrasing; put legacy info in an "old patterns" section.
- Match the form to the failure type (superpowers): discipline failure →
  prohibition + rationalization table + red flags; wrong-shaped output →
  positive recipe (prohibitions backfire); omitted element → required slot in a
  template; conditional behavior → explicit predicate.

## Testing is not optional

- Superpowers' Iron Law: **no skill without a failing test first** — run the
  scenario without the skill (baseline), watch the failure, write the minimal
  skill that fixes it, re-run, close loopholes (RED-GREEN-REFACTOR).
- Official version: evaluation-driven development — create ≥3 eval scenarios
  BEFORE writing extensive docs; measure baseline; iterate. Format:
  `{skills, query, files, expected_behavior[]}` in `evals/evals.json`.
- Test with every model tier the skill will run on (Haiku needs more guidance,
  Opus needs less).
- The two-agent loop: Agent A helps write/refine, Agent B (fresh context) uses
  the skill on real tasks; observe B's behavior, bring findings back to A.

## Naming

- Gerund/verb-first names describe the activity: `writing-skills`,
  `condition-based-waiting`, `deep-reading`. Letters, numbers, hyphens only.
- Avoid vague names (Helper, Utils) and generic labels (step1, helper2).

## Cross-referencing

- Reference other skills by name with explicit requirement markers
  ("REQUIRED BACKGROUND: …"). Never `@`-link files from a skill — `@` force-loads
  immediately and burns context.

---

## Rebuilding an existing skill: it carries no evidence — 2026-09-01

**MEASURED on this library.** Of 69 skills sitting in `intake/`, **17 contain any URL at
all**, 21 have a `references/` directory, 12 have evals. For roughly fifty of them there is
literally nothing to cite.

That settles a design question rather than merely describing the corpus. A finished skill
decomposed into a build package produces claims with no sources — and a finished skill
**is not evidence**. It is a hypothesis someone already wrote down, with the same standing
as a one-line candidate sentence.

So its own content supplies the **scope**, the **vocabulary** and the **tasks**, and never
the claims. `claims` holds only what someone actually went and sourced.

**Demonstrated, not argued:** `abstention-threshold-design` has a 128-line body, 0
references, 0 evals, 0 URLs. Decomposed, it is REFUSED at admission — no sources, no
claims — with its 128 lines sitting right there. Rewriting an old skill means doing the
harvest nobody did the first time.

**The one thing this path gives that a fresh harvest cannot:** the trigger vocabulary. The
incumbent's description is the words someone already chose for this job, tested against
real routing or not.

**And most of our own skills cannot be EXTENDED, only rebuilt.** The extend gate refuses
to call anything a regression without a stored baseline, and an unmeasured incumbent is
UNDECIDABLE rather than no-regressions. With 12 of 69 carrying evals, that verdict applies
to most of the library.
