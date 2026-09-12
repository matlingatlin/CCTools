---
name: skill-description-optimizer
description: "Use when a skill's `description` triggers wrong — it fails to auto-invoke on prompts it should own, or it mis-fires and steals prompts that belong to a sibling skill (overlapping triggers, vague wording, missing keywords). Runs when wave-reflect flags a description to `sharpen`, or when two skills fight over the same prompts. Diagnoses why the current description fires or stays silent, rewrites the trigger to be trigger-first, concrete, keyword-rich, and non-overlapping with siblings, then verifies the right skill would win on representative prompts. Tunes ONLY the description field of ONE skill, reactively; NOT the proactive job-to-owner routing table derived across a whole library and proved with negative triggers (capability-routing-table). Use writing-skills or skill-creator to author or edit a skill's body, prompt-refinement for a user's request, skill-stocktake to audit overall quality."
---

# Skill Description Optimizer

The `description` is the only thing the model reads to decide whether a skill auto-invokes. This talent tunes that one field so the right skill fires on the right prompts and no other.

## When to use
- wave-reflect flagged a skill's description to **sharpen** (overlapping or low-signal trigger).
- A skill won't fire on prompts it should own, or fires on prompts a sibling should own.
- Two or more skills have descriptions that overlap and compete for the same prompts.

**When NOT to use:** the skill's *body* or procedure is the problem (use writing-skills / skill-creator); the skill doesn't exist yet as a whole (skill-creator); a user's *request* is vague (prompt-refinement); you're auditing broad quality across many skills (skill-stocktake); you need the whole library's job-to-owner routing table derived and proved with negative triggers, rather than one field fixed (capability-routing-table).

## Steps
1. **Collect the field.** Read the target skill's `description` plus the descriptions of every sibling whose topic is adjacent. List each sibling's trigger surface (the prompts it claims).
2. **Build a prompt set.** Write 6–12 representative prompts: ones the target SHOULD own (positives), ones a sibling should own (negatives / near-misses), and phrasing variants. Draw negatives from the overlapping siblings.
3. **Diagnose current triggering.** For each prompt, judge which skill's description best matches as written. Mark false negatives (target should fire, doesn't) and false positives (target fires, sibling should own it). Name the cause: vague verb, missing keyword, topic collision with a sibling, or too-broad scope.
4. **Rewrite trigger-first.** Open with "Use when…", third person, concrete conditions and the exact keywords/filenames/phrases a matching prompt contains. Carve the boundary against each colliding sibling explicitly ("…; use X for Y instead"). Keep it under the cap your project pins (here: `pipeline/CONSTANTS.md`, 1024).
5. **Re-verify.** Re-run the prompt set against the rewrite plus the unchanged siblings. Every positive now matches the target; every negative matches its rightful sibling. If any prompt is still ambiguous, tighten the losing description's boundary and repeat.
6. **Report the diff.** Return old vs new description and the before/after verdict per prompt. Do not touch the body.

## Rules
- Change ONLY the `description` frontmatter field — never the body, name, or files.
- Method only: reason about matches yourself. No network calls, no CLI, no scripts, no auto-run hooks.
- Every rewrite must be trigger-first, third person, keyword-rich, and non-overlapping with existing siblings.
- A boundary is not sharp until a representative negative prompt clearly loses to its rightful sibling.
- Optimize for the boundary, not verbosity — cut words that don't change which skill wins.
