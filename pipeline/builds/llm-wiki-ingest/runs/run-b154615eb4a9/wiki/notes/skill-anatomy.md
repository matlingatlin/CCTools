---
title: Skill anatomy
sources:
  - url: https://code.claude.com/docs/en/skills
    fetched: 2026-08-27
  - url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
    note: "The Complete Guide to Building Skills for Claude, Anthropic, 33pp, distribution section dated January 2026. Read in full 2026-08-29."
    fetched: 2026-08-29
status: verified
tags: [claude-code, skills, mechanics]
related: ["[[skill-authoring-best-practices]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[anthropic-skill-authoring-contract]]", "[[token-economy-playbook]]"]
---

# Skill anatomy

A skill is a directory with a `SKILL.md` file: YAML frontmatter (when to load it)
plus markdown instructions (what to do when loaded). Skills follow the
[Agent Skills](https://agentskills.io) open standard; Claude Code extends it.
Custom commands (`.claude/commands/*.md`) are merged into skills — same mechanism.

## Where skills live

| Level | Path | Scope |
| --- | --- | --- |
| Enterprise | managed settings dir | whole org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | all projects |
| Project | `.claude/skills/<name>/SKILL.md` | this repo |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | where plugin enabled |

Precedence on name clash: enterprise > personal > project; any level > bundled.
Plugin skills are namespaced (`/plugin:skill`) so they never clash.

**Cloud/Cowork sessions do NOT read `~/.claude/skills/` on the user's machine.**
They load (a) skills enabled on the claude.ai account and (b) project skills
committed to the cloned repo's `.claude/skills/`. → For this project, skills must
be committed to this repo to load automatically.

Live change detection: edits to SKILL.md under watched skill dirs apply within
the current session, no restart (new top-level dirs need a restart).

## Hard rules from Anthropic's own guide (read in full 2026-08-29)

These are stated as requirements, not advice. Several were not in this note.

| Rule | Value |
|---|---|
| Filename | **exactly `SKILL.md`**, case-sensitive. `SKILL.MD`, `skill.md` are rejected |
| Folder name | **kebab-case only** — no spaces, no underscores, no capitals |
| `README.md` inside a skill folder | **forbidden.** Documentation goes in SKILL.md or `references/`. A repo-level README for human visitors is separate and expected |
| `description` | **must contain BOTH what it does AND when to use it**; **under 1024 characters** |
| **XML angle brackets `<` `>` anywhere in frontmatter** | **forbidden — a security restriction.** Verbatim: *"Frontmatter appears in Claude's system prompt. Malicious content could inject instructions."* |
| Skill names containing **"claude" or "anthropic"** | **reserved**, rejected |
| `compatibility` | 1–500 characters |
| **SKILL.md body** | **"Keep SKILL.md under 5,000 words"** |
| Simultaneously enabled skills | *"Evaluate if you have more than 20–50 skills enabled simultaneously"* |

**CORRECTED 2026-08-30 — this paragraph previously called 5,000 words
"authoritative". It is one figure among four, and not the most-stated one.** A
dedicated pass over the live sources found **"under 500 lines"** in three places
(the best-practices page, `code.claude.com/docs/en/skills`, and the spec's own
checklist), **"< 5000 tokens recommended"** in the spec's progressive-disclosure
table, and **"<5k words" with a 1,500–2,000 word target** in Anthropic's
`plugin-dev/skill-development` skill. No Anthropic source reconciles them, and
none of their 11 measured shipped skills exceeds 500 lines. See
[[anthropic-skill-authoring-contract]] for the four values side by side and the
practice measurements. The mechanism to design against remains silent truncation
at compaction (5,000 *tokens* per skill against a 25,000 shared budget — see the
lifecycle section below); the word cap and the token budget are different
quantities and must not be conflated.

## What the guide says about testing

Three levels, chosen by how visible the skill is: manual in Claude.ai, scripted in
Claude Code, programmatic via the skills API.

Three areas to cover: **triggering** (fires on obvious *and* paraphrased requests,
does NOT fire on unrelated ones), **functional** (valid outputs, error handling,
edge cases), and **performance comparison** — explicitly *"Prove the skill improves
results vs. baseline"*, counting tool calls and tokens with and without.

Suggested target: *"Skill triggers on 90% of relevant queries"*, measured over
10–20 test queries.

**Anthropic's own caveat on all of it, verbatim:** *"These are aspirational
targets - rough benchmarks rather than precise thresholds. Aim for rigor but
accept that there will be an element of vibes-based assessment. We are actively
developing more robust measurement guidance and tooling."* Worth quoting whenever
someone treats a skill's score as settled.

And on the tool: *"skill-creator helps you design and refine skills but does not
execute automated test suites or produce quantitative evaluation results."*

**A method claim worth testing rather than adopting:** *"the most effective skill
creators iterate on a single challenging task until Claude succeeds, then extract
the winning approach into a skill."* Stated from experience, not measured. Note it
runs opposite to the baseline-first discipline — extract-what-worked, rather than
observe-what-fails-first. Neither is measured against the other.

## The guide's strongest corroboration of the hook rule

Verbatim, from the troubleshooting chapter: *"For critical validations, consider
bundling a script that performs the checks programmatically rather than relying on
language instructions. **Code is deterministic; language interpretation isn't.**"*

That is Anthropic saying independently what this library measured: a must-never is
a mechanism, not a sentence. See [[agent-design-template]].

**A tension to record rather than resolve.** The same chapter recommends, for
model "laziness", adding *"Take your time... Quality is more important than
speed"* — and then notes *"Adding this to user prompts is more effective than in
SKILL.md."* That prose exhortations work better in a prompt than in a skill is
consistent with the measured finding that prose warnings are weak, but the guide
offers no measurement for the technique itself.

## Distribution (guide, January 2026)

Zip the folder → Claude.ai Settings > Capabilities > Skills, or drop into the
Claude Code skills directory. Admins can deploy workspace-wide (shipped
2025-12-18) with automatic updates. Published as an **open standard**, intended to
be portable across platforms. API surface: `/v1/skills` for listing and managing,
`container.skills` on Messages API requests, **requiring the Code Execution Tool
beta**, plus version control through the Claude Console.

`allowed-tools` example given in the guide is space-separated:
`"Bash(python:*) Bash(npm:*) WebFetch"`.

## Frontmatter fields (Claude Code)

All optional; `description` recommended.

| Field | Effect |
| --- | --- |
| `name` | display name only (command name comes from the directory name; plugin skills differ) |
| `description` | drives automatic invocation; combined with `when_to_use`, truncated at 1,536 chars in the listing |
| `when_to_use` | extra trigger context, appended to description |
| `disable-model-invocation: true` | only the user can invoke; description not loaded into context |
| `user-invocable: false` | only Claude can invoke; hidden from `/` menu |
| `allowed-tools` | tools pre-approved for the invoking turn only (clears on next user message) |
| `disallowed-tools` | tools removed while skill is active |
| `model` / `effort` | per-turn model/effort override |
| `context: fork` + `agent:` | run skill body as a subagent prompt (isolated context, background by default; `background: false` to block) |
| `paths` | glob patterns limiting when the skill auto-activates |
| `hooks` | register hooks at invocation |
| `arguments`, `argument-hint` | named/positional args |
| `metadata`, `license`, `compatibility` | free-form / spec fields, not acted on |

Only 6 fields survive claude.ai upload / API packaging: `name`, `description`,
`license`, `compatibility`, `metadata`, `allowed-tools`. Anything else fails the
upload with a hard error (fine in Claude Code itself).

## Body features

- `$ARGUMENTS`, `$ARGUMENTS[N]`/`$N`, `$name` — argument substitution.
- `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}` — path/session vars;
  usable in `allowed-tools` too, enabling promptless bundled-script execution.
- `` !`command` `` and ```` ```! ```` blocks — dynamic context injection: shell runs
  BEFORE Claude sees the content; output replaces the placeholder. A failing
  command aborts the whole invocation (append `|| true` where non-zero is normal).
  Not executed for skills synced from claude.ai onto a local machine.

## Lifecycle (token economics)

- At startup only the name+description listing is in context (budget ≈ 1% of the
  context window; least-used skills lose their descriptions first).
- Full body loads on invocation and **stays in context for the rest of the
  session** — every line is a recurring cost. Re-invocation with identical
  content adds a short "already loaded" note, not a second copy.
- On auto-compaction, the most recent invocation of each skill is re-attached:
  first 5,000 tokens per skill, 25,000-token shared budget, most recent first.

## Control & security

- Permission rules: `Skill(name)` / `Skill(name *)`; deny `Skill` disables all.
- `skillOverrides` in settings: `on` / `name-only` / `user-invocable-only` / `off`.
- `allowed-tools` in a project skill applies even in untrusted folders —
  **review `allowed-tools` of any third-party skill before running it.**
- `disableSkillShellExecution: true` neutralizes `!` injection for non-bundled skills.

## Evaluation tooling

The `skill-creator` plugin (`/plugin install skill-creator@claude-plugins-official`)
automates baseline-vs-skill comparisons: eval cases in `evals/evals.json`,
isolated subagent runs, grading, benchmark (pass rate vs token overhead), blind
A/B between skill versions, and description trigger-tuning.

The loading economics above are one of three token sinks; the other two (retrieval, the generation loop) and the ranked policy are in [[token-economy-playbook]] (added 2026-09-02).
