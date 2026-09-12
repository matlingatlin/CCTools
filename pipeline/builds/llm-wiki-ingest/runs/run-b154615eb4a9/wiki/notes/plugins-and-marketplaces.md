---
title: Plugins and marketplaces
sources:
  - url: https://code.claude.com/docs/en/plugins
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/plugin-marketplaces
    fetched: 2026-08-27
status: verified
tags: [claude-code, plugins, marketplaces, distribution, mechanics]
related: ["[[skill-anatomy]]", "[[subagents]]", "[[hooks]]", "[[mcp]]", "[[claude-code-extension-layer]]"]
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
- `/plugin install name@marketplace`; `/reload-plugins` (no restart);
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
