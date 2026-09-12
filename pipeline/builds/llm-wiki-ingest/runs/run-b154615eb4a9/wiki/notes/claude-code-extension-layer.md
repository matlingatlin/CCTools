---
title: Claude Code extension layer — choosing and combining features (general best practice)
sources:
  - url: https://code.claude.com/docs/en/features-overview
    fetched: 2026-08-27
status: verified
tags: [claude-code, best-practice, architecture, context, overview]
related: ["[[skill-anatomy]]", "[[claude-md-and-memory]]", "[[subagents]]", "[[hooks]]", "[[mcp]]", "[[plugins-and-marketplaces]]", "[[dynamic-workflows]]", "[[claude-code-ecosystem-plugins]]", "[[llm-wiki-pattern]]", "[[token-economy-playbook]]"]
---

# Claude Code extension layer

The built-in tools cover most coding tasks. The extension layer customizes what
Claude knows, connects it to services, and automates workflows. This is the hub
note: which feature to reach for, how they layer, and what each costs in context.

## The features, by role

- **CLAUDE.md** — persistent context every session ("always do X" rules). → [[claude-md-and-memory]]
- **Skills** — reusable knowledge + invocable workflows, loaded on demand. → [[skill-anatomy]]
- **Subagents** — isolated context that returns a summary. → [[subagents]]
- **Dynamic workflows** — a script running many subagents in the background. → [[dynamic-workflows]]
- **MCP** — connect to external services/tools. → [[mcp]]
- **Hooks** — run something on a lifecycle event (enforcement). → [[hooks]]
- **Plugins / marketplaces** — package and distribute all of the above. → [[plugins-and-marketplaces]]
- **Code intelligence (LSP)** — symbol navigation and live type errors.
- **Cross-session messaging / Artifacts** — pass findings between your sessions; publish output as a web page.

> **Building one agent?** [[agent-design-template]] takes over from here: the six
> loading tiers inside an agent, where rules/templates/references belong, the
> composition patterns between agents, and the measured constraints on all of it.

## Which feature when (the distinctions that matter)

- **CLAUDE.md vs skill:** always-needed rules → CLAUDE.md (keep <200 lines);
  sometimes-needed reference or a `/command` workflow → skill. Rules in
  `.claude/rules/` keep CLAUDE.md focused (path-scoped ones load only for matching
  files).
- **Skill vs subagent:** skill = reusable content added to *your* window; subagent
  = isolated worker, only its summary returns. They combine — a subagent can
  preload skills (`skills:`), a skill can run isolated (`context: fork`).
- **Subagent vs workflow:** subagent = Claude decides turn by turn; workflow =
  a script decides, at dozens–hundreds of agents. Use a workflow when the job
  outgrows a handful of subagents or you want findings cross-checked before you
  see them.
- **MCP vs skill:** MCP provides the *connection and tools*; a skill teaches
  Claude how to *use* them well. They pair.
- **Hook vs skill:** a hook *always fires* on its event (enforcement, deterministic,
  zero context cost); a skill is *interpreted* by Claude (reasoning, can vary).
  **Guardrails belong in hooks** — "never edit .env" in CLAUDE.md/a skill is a
  request; a PreToolUse hook is a guarantee.

## How features layer when defined at multiple levels

- **CLAUDE.md** — additive: all levels contribute simultaneously; conflicts
  reconciled by judgment, specific usually wins.
- **Skills / subagents** — override by name (skills: managed > user > project;
  subagents: managed > CLI flag > project > user > plugin). Plugin skills are
  namespaced.
- **MCP servers** — override by name: local > project > user.
- **Hooks** — merge: all registered hooks fire for their event, regardless of source.

## Context cost by feature

| Feature | Loads | Cost |
| --- | --- | --- |
| CLAUDE.md | full, session start | every request |
| Skills | descriptions at start, body when used | low (descriptions only) |
| MCP | tool names at start, schemas on demand | low until a tool is used |
| Code intelligence | after edits / on lookup | low; can reduce file reads |
| Subagents | isolated window when spawned | isolated from main session |
| Hooks | run externally | zero unless they return output |

Every added feature costs context and can add *noise* (skills mis-trigger, Claude
loses track of conventions), so build the setup up over time rather than up front.

## Build your setup over time (trigger → add)

- Convention wrong twice → CLAUDE.md.
- Same prompt retyped → a user-invocable skill.
- Same playbook pasted a third time → capture as a skill.
- Copying from a system Claude can't see → an MCP server.
- Many reads to find a symbol → a code-intelligence plugin.
- A side task floods the conversation → route through a subagent.
- Want it to happen every time without asking → a hook.
- A second repo needs the same setup → package as a plugin.

The same triggers say when to *update* what exists: a repeated mistake is a
CLAUDE.md edit; a workflow you keep hand-tweaking is a skill needing another
revision.

## The "agentic OS in three steps" genre (added 2026-09-02)

A 98-second video (creator sells an "AgenticOS" community; the script does not match
Charlie Automates' same-named blog post, which was checked) gives the method in one
breath, and it is worth recording because it is the same method as our `agentic-os`
skill, arrived at commercially:

1. **Architecture** — break daily and business work into *domains* (research, content,
   community…), each domain into *tasks*, each task into a *skill*, and ask per skill
   whether it can become an *automation* (scheduled or triggered). The frames show a
   "conductor" node (Claude Code) over domain columns, with an automation layer beneath.
2. **Memory** — an Obsidian vault on the LLM-wiki pattern ([[llm-wiki-pattern]]; the
   video's `outputs/` folder is its own addition), on the argument that "a true RAG
   system is overkill for most people".
3. **Observability** — every skill as a button on a dashboard non-Claude-Code users
   (team, clients) can press; usage and routines shown alongside.

Nothing is measured and nothing is claimed beyond "customizable". The corroboration is
the point: domains → skills → automations → memory → dashboard is what `agentic-os`
prescribes, and the one element we do not have is the third — a button surface over
skills for people who do not run the CLI, which is a real gap for a shared library.

Context costs across all of these, measured and ranked as a policy: [[token-economy-playbook]] (added 2026-09-02).
