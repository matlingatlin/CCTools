---
title: Hooks
sources:
  - url: https://code.claude.com/docs/en/hooks-guide
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/hooks
    fetched: 2026-08-27
status: verified
tags: [claude-code, hooks, enforcement, security, mechanics]
related: ["[[skill-anatomy]]", "[[mcp]]", "[[subagents]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]", "[[claude-code-ecosystem-plugins]]"]
---

# Hooks

User-defined handlers that Claude Code runs at lifecycle events, giving
**deterministic control** — the action always happens, versus a skill/CLAUDE.md
instruction the model may or may not follow. This is the enforcement layer.

## Enforcement power (why hooks matter for the security gate)

A **`PreToolUse`** hook fires **before any permission-mode check**, in every mode
including `bypassPermissions` and `--dangerously-skip-permissions`. Returning
`deny` blocks the tool even in those modes. But hooks can only **tighten, never
loosen** — an `allow` doesn't override deny rules or org `ask` prompts.

## Event categories (full list on source; the load-bearing ones)

- **Tool:** `PreToolUse` (can block), `PostToolUse`, `PostToolUseFailure`,
  `PostToolBatch`, `PermissionRequest`, `PermissionDenied`.
- **Turn/session:** `UserPromptSubmit` (can block; stdout → context),
  `SessionStart` (stdout → context), `Stop`, `SessionEnd`, `Setup`.
- **Subagent/task:** `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`.
- **Context/config:** `PreCompact`, `PostCompact`, `InstructionsLoaded`,
  `ConfigChange`, `FileChanged`, `CwdChanged`, `DirectoryAdded`.
- **MCP:** `Elicitation`, `ElicitationResult`.

## Handler types

`command` (shell — most common), `http` (POST event JSON), `mcp_tool` (call a
connected MCP tool), `prompt` (single-turn LLM judgment, Haiku default), `agent`
(experimental multi-turn subagent). Matchers: exact/list (`Edit|Write`) or regex;
the `if` field filters by tool + args (`Bash(git *)`) but **fails open** — use the
permission system, not `if`, for hard enforcement.

## Control back to Claude

Exit 0 (stdout → context for UserPromptSubmit/SessionStart), exit 2 (blocking
error where supported), or structured JSON via `hookSpecificOutput`
(`permissionDecision: allow|deny|ask|defer`, `additionalContext`, `updatedInput`).
Multiple hooks run in parallel; most restrictive wins (`deny > defer > ask > allow`).

## Hooks in skill/agent frontmatter

Skills and subagents can declare a `hooks:` block. **Skill hooks** register on
invocation and persist for the session (`once: true` = once per session, skills
only). **Subagent hooks** last only while the subagent runs (a `Stop` becomes
`SubagentStop`). Project frontmatter hooks require workspace-trust acceptance.

## Relations & security

Enforcement (hooks) vs request (skills) — but a skill can *carry* hooks to register
enforcement once invoked. `allowManagedHooksOnly` and `allowedHttpHookUrls`
restrict sources. **For this project:** the factory's "never exfiltrate / never
touch credentials" rule for third-party skills belongs in a PreToolUse hook, since
that is the only mechanism a downloaded skill cannot talk its way past.
