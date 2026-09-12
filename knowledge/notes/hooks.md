---
title: Hooks
sources:
  - url: https://code.claude.com/docs/en/hooks-guide
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/hooks
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/hooks-guide
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/hooks-guide@2026-09-04.md
  - url: https://code.claude.com/docs/en/hooks
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/hooks@2026-09-04.md
tags: [claude-code, hooks, enforcement, security, mechanics]
related: ["[[skill-anatomy]]", "[[mcp]]", "[[subagents]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]", "[[claude-code-ecosystem-plugins]]", "[[claude-md-and-memory]]", "[[plugins-and-marketplaces]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/hooks-guide@2026-09-04.md
  - knowledge/raw/claude-code-docs-2026-09-04/hooks@2026-09-04.md
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

**Re-read 2026-09-11 — three behaviour changes, and all three are silent failures.**
- **`mcp_tool` hooks are SKIPPED, not errored, before MCP servers are available.** The page used
  to say such hooks *"should expect the 'not connected' error on first run"*; it now says Claude
  Code *"skips the event's `mcp_tool` hooks without calling their tools"* on `SessionStart` at
  launch, and on **`Setup` always** — *"A `type: \"mcp_tool\"` hook on `Setup` is always skipped."*
  Wiring one for session bootstrap buys silence, not an error.
- **`SessionStart` is no longer once per session.** The heading dropped the word "once": it
  re-fires on `/clear` and on compaction, runs in the background there, and **its output is
  discarded** if you `/clear` or `/resume` again while it is still running.
- **`stopReason` is now model-visible.** It read *"Not shown to Claude"*; it now reads *"It stays
  in the conversation, so Claude sees it if the conversation continues."* Anything written on the
  old assumption is now addressed to two audiences.
- **`WorktreeRemove` gained decision control**, moving from "failures logged in debug mode only"
  to *any* non-zero exit code failing the removal — so the exit-code summary's "exit 2 where
  supported" now has a second exception beside `WorktreeCreate`.
- **`SubagentStart` is no longer per-spawn**: it also runs when a subagent is resumed and *"each
  time an in-process agent team teammate handles a new message"*, with injected context
  de-duplicated so the prompt cache survives.

**Re-read again 2026-09-11 (evening) — a FOURTH silent failure, and it is the one most likely to
bite a hook author.** The page gained a troubleshooting list for *"hook prints valid JSON but the
decision doesn't take effect and no error appears"*, naming two causes:
- **A field at the wrong LEVEL is ignored without an error.** *"When your hook returns
  `permissionDecision` or `additionalContext` at the top level instead of inside
  `hookSpecificOutput`, the JSON still parses, and Claude Code ignores the misplaced fields
  without reporting an error."* So a hook that denies a tool call, written with the field one
  level too high, is **indistinguishable from a hook that allowed it** — the shape most worth
  knowing for anything in this repo's fourth gate, where a hook is the enforcement.
  The only way to see it: `claude --debug`, then search the debug log for the string
  **`Hook JSON output had unrecognized keys`**.
- **Anything on stdout before the JSON breaks it.** *"something else writes to stdout first,
  usually an unconditional `echo` in your shell profile, so the output no longer starts with `{`"*
  — a hook can therefore be broken by a change to a file the hook does not mention.

Both belong to the pattern this base keeps finding in this product's surface and now has a name
for: **the failure is not that it errors, it is that it parses.** Same shape as the description
truncation wall (the tail is dropped silently) and as `mcp_tool` hooks being skipped rather than
erroring. A hook is not verified by running it once and seeing no error; it is verified by seeing
the effect it claims.
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
enforcement once invoked. The request side is written up in [[claude-md-and-memory]]:
CLAUDE.md and auto memory both load at the start of every session and are **context, not
enforcement**, so a "never do X" written there is asked for on every turn and guaranteed on
none. Hooks also arrive by post: a plugin bundles a `hooks/` directory that registers
wherever the plugin is enabled ([[plugins-and-marketplaces]]), which is why
`allowManagedHooksOnly` and the marketplace allowlists there decide whose enforcement runs
in your session. `allowManagedHooksOnly` and `allowedHttpHookUrls`
restrict sources. **For this project:** the factory's "never exfiltrate / never
touch credentials" rule for third-party skills belongs in a PreToolUse hook, since
that is the only mechanism a downloaded skill cannot talk its way past.
