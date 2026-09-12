---
title: Skill anatomy
sources:
  - url: https://code.claude.com/docs/en/skills
    fetched: 2026-08-27
  - url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
    note: "The Complete Guide to Building Skills for Claude, Anthropic, 33pp, distribution section dated January 2026. Read in full 2026-08-29."
    fetched: 2026-08-29
  - url: https://code.claude.com/docs/en/skills
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/skills@2026-09-04.md
  - url: https://code.claude.com/docs/en/skills
    fetched: 2026-09-08b
    note: "re-read after watch.py reported the page changed. One sentence added, on the /skill-doctor report: 'Of the skills it tells you where to turn off, start with the ones that have the highest context cost.' Nothing else in the page moved."
tags: [claude-code, skills, mechanics]
related: ["[[skill-authoring-best-practices]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[anthropic-skill-authoring-contract]]", "[[token-economy-playbook]]", "[[claude-code-extension-layer]]", "[[plugins-and-marketplaces]]", "[[skill-authoring-eval-methodology]]", "[[subagents]]", "[[claude-md-and-memory]]", "[[hooks]]", "[[mcp]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/skills@2026-09-04.md
  - knowledge/raw/watch-2026-09-08b/skills@2026-09-08b.md
  - knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf
  - "the guide is HELD but only 17.6% EXTRACTABLE here (hex-coded CID text); knowledge/pdftext.py refuses it, so rows read from it cannot be re-verified in this environment - see pipeline/decisions/2026-09-11-stdlib-pdf-text.md"
  - "partial: 2 of 2 distinct source URLs now kept as raw"
  - "the 2026-09-08b copy is a RE-READ after watch.py reported the page changed; the 09-04 copy stays as the provenance of the rows read from it"
---

# Skill anatomy

A skill is a directory with a `SKILL.md` file: YAML frontmatter (when to load it)
plus markdown instructions (what to do when loaded). Skills follow the
[Agent Skills](https://agentskills.io) open standard; Claude Code extends it.
Custom commands (`.claude/commands/*.md`) are merged into skills — same mechanism.
Whether a job wants a skill at all is decided one level up, in
[[claude-code-extension-layer]]; this page assumes that answer was yes and describes the
shape it takes.

## Where skills live

| Level | Path | Scope |
| --- | --- | --- |
| Enterprise | managed settings dir | whole org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | all projects |
| Project | `.claude/skills/<name>/SKILL.md` | this repo |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | where plugin enabled |

Precedence on name clash: enterprise > personal > project; any level > bundled.
Plugin skills are namespaced (`/plugin:skill`) so they never clash — the plugin row of
that table is specified in [[plugins-and-marketplaces]], which also holds the trust
settings (`strictKnownMarketplaces`, reserved marketplace names) deciding whose skills can
reach the directory at all.

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

**Two changes to this field, re-read 2026-09-11.** (1) The omitted-description fallback
**changed**: it was *"uses the first paragraph of markdown content"*, it is now *"uses the first
non-empty **line** of the markdown content"* — a skill shipping without a description gets one
line as its listing text, not one paragraph. (2) The **1,536**-character combined truncation is
re-confirmed verbatim in the same rewritten row, against fresh bytes, which is the constant
`pipeline/queries/desc_headroom.py` gates on.
| **XML angle brackets `<` `>` anywhere in frontmatter** | **forbidden — a security restriction.** Verbatim: *"Frontmatter appears in Claude's system prompt. Malicious content could inject instructions."* |
| Skill names containing **"claude" or "anthropic"** | **reserved**, rejected |
| `compatibility` | 1–500 characters |
| **SKILL.md body** | **"Keep SKILL.md under 5,000 words"** — **not a constraint; see the note under this table** |
| Simultaneously enabled skills | *"Evaluate if you have more than 20–50 skills enabled simultaneously"* — **also not a constraint** |

**The last two rows are in the wrong table, and reading the guide directly on 2026-09-12 is what
showed it.** Every other row here is a hard constraint a loader enforces — a length bound, a
forbidden character, a reserved name. Those two are **remedies**, and in the guide they sit side by
side under a single `Solutions:` heading in the troubleshooting chapter, answering the symptom
*"content too large ... too many skills enabled simultaneously"*: `1. Optimize SKILL.md size - Move
detailed docs to references/ - Link to references instead of inline - Keep SKILL.md under 5,000
words 2. Reduce enabled skills - Evaluate if you have more than 20 - 50 skills enabled
simultaneously`. Nothing rejects a 6,000-word body or a 60th enabled skill; these are what to do
once something is already slow. They are kept in place rather than moved, because both figures are
cited elsewhere in this base from this table — but a reader must not plan against them the way the
rows above are planned against. *A table of constraints will absorb any number you put in it.*

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

The loop those three areas sit inside — draft, test prompts, evaluate quantitatively,
rewrite, expand the set, then a dedicated description-improver pass over triggering — is in
[[skill-authoring-eval-methodology]], read out of Anthropic's own `skill-creator`.

**Anthropic's own caveat on all of it, verbatim:** *"These are aspirational
targets - rough benchmarks rather than precise thresholds. Aim for rigor but
accept that there will be an element of vibes-based assessment. We are actively
developing more robust measurement guidance and tooling."* Worth quoting whenever
someone treats a skill's score as settled.

And on the tool: *"skill-creator helps you design and refine skills but does not
execute automated test suites or produce quantitative evaluation results."*

**That sentence is STALE, not false — resolved 2026-09-12, and the PDF's own metadata is what
settled it.** This page carried the quote above and, ~130 lines later, a description of
`skill-creator` automating baseline-vs-skill runs and emitting `pass_rate`, `tokens {mean, stddev}`
and a delta. Recorded as an internal contradiction since 2026-09-08 and marked *unresolvable*,
because the guide could not be re-extracted here. It can now be — the blocker was one poisoned
system dependency, not a missing toolchain (see `pipeline/decisions/2026-09-11-stdlib-pdf-text.md`).

Measured from the held file
(`knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf`),
33 pages, 35,765 characters extracted:

| | |
|---|---|
| the guide's `/CreationDate` | **D:20260126142224** → **2026-01-26**, Adobe InDesign 21.1 |
| `pass_rate` in the guide | **0 occurrences** |
| `quantitative` in the guide | **1** — the sentence quoted above |
| the shipped tool's metrics | read directly **2026-08-30** |

So the guide is **seven months older** than the tooling it describes, and it makes **no claim at all**
about the metrics the direct read observed — `pass_rate` is simply absent from it. The sentence was
true when written and the tool outgrew it. **Not a contradiction in this base: a dated vendor claim
the vendor's own product overtook**, and the file's creation date is what distinguishes *stale* from
*false*. Read it as scoped to January 2026; [[skill-authoring-eval-methodology]] holds what the tool
does now.

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

**All optional *to this loader* — and REQUIRED by the spec. Scope clause added 2026-09-12.** The
heading already said "(Claude Code)" and the sentence did not, so the line read as licence to ship a
skill with neither field. It is not. The Agent Skills specification —
`knowledge/raw/baseline-2026-09-04/agentskills.io_specification.html`, held since 2026-09-04 — says
verbatim *"The **required** `name` field: Must be 1-64 characters…"* and *"The **required**
`description` field: Must be 1-1024 characters…"*, and introduces `license`, `compatibility`,
`metadata` and `allowed-tools` each as *"The **optional** … field"*. Its minimal example carries
exactly `name` and `description`.

So two governing documents disagree and both are right about themselves: **the spec requires them; a
tolerant loader accepts their absence.** Omitting them is spec-violating and will still run here. See
[[skill-authoring-eval-methodology]], which states the same rule from the spec's side. *Within Claude
Code*, `description` is not merely recommended — it is what drives automatic invocation, so a skill
without one cannot be selected by the mechanism it exists for.

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

  > **`context: fork` is NOT a fork of the conversation, and Anthropic now says so explicitly
  > (2026-09-11):** *"Despite the name, a skill with `context: fork` doesn't run in a fork of the
  > current conversation, which would hand the subagent everything you've discussed so far. When
  > the task depends on that history, fork the conversation instead."* This base had **both**
  > meanings, each correct and neither aware of the other — here as "isolated context", and in
  > [[agent-design-template]] as a Fork that *"inherits the whole conversation … and reuses the
  > parent prompt cache"*. Two different features, one word, two notes that link to each other.
| `paths` | glob patterns limiting when the skill auto-activates |
| `hooks` | register hooks at invocation |
| `arguments`, `argument-hint` | named/positional args |
| `metadata`, `license`, `compatibility` | free-form / spec fields, not acted on |

Only 6 fields survive claude.ai upload / API packaging: `name`, `description`,
`license`, `compatibility`, `metadata`, `allowed-tools`. Anything else fails the
upload with a hard error (fine in Claude Code itself).

`context: fork` has an inverse: a subagent's own `skills:` field, where the agent owns the
system prompt and pulls the skill body in. [[subagents]] holds that side of the
arrangement, together with the limit a growing roster hits first — the combined
descriptions of all non-built-in subagents share a **15,000-token** budget.

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
- The always-loaded alternative is CLAUDE.md, and the trade is the whole reason skills
  exist: [[claude-md-and-memory]] records that every line of that hierarchy loads at the
  start of every session, with a target under 200 lines because adherence falls as it
  grows. Always-true rules go there; anything needed sometimes belongs in a skill body.
- Full body loads on invocation and **stays in context for the rest of the
  session** — every line is a recurring cost. Re-invocation with identical
  content adds a short "already loaded" note, not a second copy.
- On auto-compaction, the most recent invocation of each skill is re-attached:
  first 5,000 tokens per skill, 25,000-token shared budget, most recent first.

## Control & security

- A skill asks; only a hook enforces. [[hooks]] documents the mechanism a skill cannot
  supply: a `PreToolUse` hook fires **before any permission-mode check**, in every mode
  including `bypassPermissions`, and can only tighten — which is where a must-never has to
  live once `allowed-tools` has granted the tool.
- Tools reached through an MCP server are named in `allowed-tools` by their fully-qualified
  `mcp__<server>__<tool>` form; [[mcp]] holds that form and the scope precedence deciding
  which server a name resolves to.
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

## Re-read 2026-09-04b — the page moved twice in one day, and two of the changes are about us

`knowledge/watch.py`'s first run reported the `skills` page changed **hours** after the morning
fetch (16 lines). Raw: `knowledge/raw/claude-code-docs-2026-09-04b/skills@2026-09-04b.md`.
All MEASURED from that file.

| Claim | Verbatim | Verdict |
|---|---|---|
| Nested skills do NOT load at startup | "Skills in nested `.claude/skills/` directories below your starting directory don't load at startup. They load the first time Claude reads or edits a file in the subdirectory that contains them" | MEASURED |
| `/add-dir` loads them early | "To load a subdirectory's skills before Claude reads or edits a file there, run `/add-dir` with that subdirectory's path. This requires Claude Code v2.1.257 or later." | MEASURED |
| A command now measures per-skill context cost and use | "Every skill in the skill listing adds to your context on every turn, whether or not Claude ever uses it. Run `/skill-doctor` to see what each of your skills costs and how often it gets used" | MEASURED |
| It names never-invoked skills | "It flags skills in the listing that have never been invoked and says where to turn them off." | MEASURED |
| It now ranks what to turn off by context cost | "Of the skills it tells you where to turn off, start with the ones that have the highest context cost." | MEASURED |
| Large Bash output is a path, not truncation | "output past the Bash tool's inline ceiling arrives as a file path plus a short preview, not truncated text" | MEASURED |

**Why the first two matter here.** This repository keeps its talents in `.claude/skills/` at the
root, so they load at startup and the nesting rule does not bite — but any project that files
skills under a subdirectory gets them silently absent until something in that directory is
touched. A skill that "does not trigger" may simply not be loaded yet, which is a different
diagnosis from a bad description (the `skill-description-optimizer` talent treats the second, not the first).

**Why `/skill-doctor` matters more.** It measures per-skill context cost and invocation count —
the numbers `context-budget` ranks by estimate and `skill-stocktake` grades without. A first-party
measurement of "this skill has never been invoked" also lands next to this repository's standing
rule that a talent is dropped ONLY for failing its tests, never for being unused. The command
gives the number; the rule still says the number is not grounds for a drop. Both stay true, and
now the second is a deliberate choice against a measurement rather than an absence of one.

**The page moved on this exact point, and it moved against us.** Re-read 2026-09-08 (the source
changed under the row; `watch.py` reported it): the report no longer only *names* never-invoked
skills, it now tells the reader where to start — *"start with the ones that have the highest
context cost."* That is first-party guidance to act on the two numbers together, and it is the
strongest external pressure yet on the standing rule. The rule does not bend, and the reason is
narrower than "we disagree": `/skill-doctor` measures cost and use **in one developer's session**,
and this is a cross-project library whose whole premise is that a method unused in today's project
is the one a future task needs. Cost is real and is paid every turn — which is why it is measured
here per turn rather than denied ([[token-economy-playbook]] carries the figure, and
`pipeline/queries/context_surface.py` recomputes it rather than pinning it) and cut where a description can be sharpened. Use is not evidence about a library.
So: take the cost ranking, refuse the drop, and keep the removal criterion a failed test.
