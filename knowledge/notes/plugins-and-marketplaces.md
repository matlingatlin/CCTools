---
title: Plugins and marketplaces
sources:
  - url: https://code.claude.com/docs/en/plugins
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/plugin-marketplaces
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/plugins
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/plugins@2026-09-04.md
  - url: https://code.claude.com/docs/en/plugin-marketplaces
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/plugin-marketplaces@2026-09-04.md
tags: [claude-code, plugins, marketplaces, distribution, mechanics]
related: ["[[skill-anatomy]]", "[[subagents]]", "[[hooks]]", "[[mcp]]", "[[claude-code-extension-layer]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/plugin-marketplaces@2026-09-04.md
  - knowledge/raw/claude-code-docs-2026-09-04/plugins@2026-09-04.md
---

# Plugins and marketplaces

A plugin is a self-contained directory that bundles **skills, subagents, hooks,
MCP servers, LSP servers, monitors, executables (`bin/`), and default settings**
for sharing across projects and teams. Standalone `.claude/` (names like `/hello`)
vs plugin (namespaced `/plugin-name:hello`). Recommended: start standalone,
convert to a plugin to share.

## Structure

All component dirs sit at the **plugin root**, never inside `.claude-plugin/`
(which holds only `plugin.json`): `skills/`, `agents/`, `hooks/`, `.mcp.json`,
`.lsp.json`, `monitors/`, `bin/`, `settings.json`. `plugin.json` requires `name`
(also the skill namespace); optional `description`, `version`, `author`.
`${CLAUDE_PLUGIN_ROOT}` references bundled files; `${CLAUDE_PLUGIN_DATA}` for
state that survives updates.

## Install / test / manage

- `claude --plugin-dir ./my-plugin` — load without installing (session-only;
  overrides an installed same-name plugin except managed force-enable).
- `/plugin install name@marketplace`; `/reload-plugins` (no restart — **except for plugin MCP
  servers in a session without an interactive terminal, which wait for the next session**;
  re-read 2026-09-11, and that session class is exactly what `claude -p` is, so it covers this
  repo's own dispatch runs). The page states it from both sides: "in a session without an
  interactive terminal, plugin MCP server changes wait for your next session" and "`/reload-plugins`
  doesn't connect or disconnect plugin MCP servers; those changes take effect in your next
  session". Also new: after an install whose summary says `Run /reload-plugins to activate.`,
  Claude Code now runs that reload itself, and `/reload-plugins --force` is the escape when the
  reload warns your next message would re-read the conversation;
  `claude plugin validate ./plugin` (`--strict`).
- `claude plugin init my-tool` — scaffolds a skills-directory plugin under
  `~/.claude/skills/`, auto-loads as `my-tool@skills-dir`.
- Team enablement via settings: `extraKnownMarketplaces` (register) +
  `enabledPlugins` (enable).

## Marketplaces

Catalog for discovery, versioning, auto-updates. `.claude-plugin/marketplace.json`
requires `name`, `owner`, `plugins[]`. Plugin sources: relative path, `github`,
`url`, `git-subdir`, `npm`, `archive` (zip over HTTPS, ≤256 MiB), `command`.
`strict: true` (default) merges plugin.json + entry; `strict: false` makes the
entry the whole definition. Official: `claude-plugins-official` (Anthropic-curated);
community: `claude-community`.

## Precedence

Standalone project/user agents **override** same-named plugin agents. Skills don't
override — namespacing lets `/name` and `/plugin:name` coexist. Plugin
`settings.json` > `settings` in `plugin.json`. If `version` is set in both
plugin.json and the marketplace entry, plugin.json wins silently.

## Security (for the factory's distribution step)

Every plugin source carries trust considerations — only point at archives/repos you
control. `strictKnownMarketplaces` (managed) allowlists sources (`[]` = full
lockdown). `disableCommandPluginSources` blocks command sources. Reserved
marketplace names (impersonating official ones) are blocked. Org-distributed
plugins can't ship top-level `bin/` — use `scripts/` + `${CLAUDE_PLUGIN_ROOT}`.

## For this project

When the factory graduates a validated skill from "in this repo's `.claude/skills/`"
to "shared across repos", packaging it as a plugin in a private marketplace is the
distribution path. Until then, project skills committed here already load in cloud
sessions — no plugin needed yet.
