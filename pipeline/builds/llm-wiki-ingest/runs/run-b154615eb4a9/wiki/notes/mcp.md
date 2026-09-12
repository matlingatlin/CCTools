---
title: MCP (Model Context Protocol) in Claude Code
sources:
  - url: https://code.claude.com/docs/en/mcp
    fetched: 2026-08-27
status: verified
tags: [claude-code, mcp, integrations, mechanics]
related: ["[[skill-anatomy]]", "[[hooks]]", "[[plugins-and-marketplaces]]", "[[claude-code-extension-layer]]", "[[model-agnostic-agent-harnesses]]", "[[temporal-kg-agent-memory]]", "[[claude-code-ecosystem-plugins]]", "[[graphify-assessment]]", "[[third-party-landscape]]"]
---

# MCP in Claude Code

Open standard connecting Claude to external tools, databases, and APIs. Servers
expose three capability kinds: **tools** (callable actions), **prompts** (become
`/` commands), and **resources** (`@` mentions). A server can also push messages
into a session unprompted.

## Adding servers / transports

Four transports: **HTTP** (recommended remote), **SSE** (deprecated), **stdio**
(local process), **WebSocket** (persistent, for push).
- HTTP: `claude mcp add --transport http <name> <url>` (+ `--header` for bearer).
- stdio: `claude mcp add ... --transport stdio <name> -- <command> [args]` (`--`
  separates Claude's flags from the server command).
- JSON: `claude mcp add-json <name> '<json>'`. In JSON, a `url` entry needs an
  explicit `"type"` or it errors.

## Scope precedence (connects once, from highest; fields NOT merged)

Local (`~/.claude.json`, private) > Project (`.mcp.json`, committed) > User
(private, all projects) > Plugin-provided > claude.ai connectors. Default scope
is local; set with `--scope`. `.mcp.json` supports `${VAR}` / `${VAR:-default}`
expansion in command/args/env/url/headers.

## Tool search, naming, references

- **Tool search** on by default (compatible models): only tool names + server
  instructions load at start, schemas deferred → low context. `alwaysLoad: true`
  exempts a server; `ENABLE_TOOL_SEARCH` tunes it.
- **Fully-qualified name:** `mcp__<server>__<tool>` (plugins:
  `mcp__plugin_<plugin>_<server>__<tool>`). Use this exact form in permission
  rules, **skill `allowed-tools`**, **subagent `tools`**, and **hook matchers**.
- Prompts as commands: `/mcp__github__pr_review 456`. Resources: `@server:proto://path`.

## Security (the parts that matter for the factory)

- **Trust each server** — content-fetching servers create prompt-injection risk.
- Project-scoped servers still load in non-interactive/cloud runs unless
  `--strict-mcp-config`. `headersHelper` from project/plugin/managed sources runs
  behind the workspace-trust dialog and **strips credential-like env vars**
  (TOKEN, SECRET, KEY, AUTH, …) — read creds from a file/store instead.
- Server authors can force per-call approval via
  `_meta["anthropic/requiresUserInteraction"]`.
- Output: warns at 10k tokens, default max 25k (`MAX_MCP_OUTPUT_TOKENS`).

## Official reference servers (the MCP shelf)

From `modelcontextprotocol/servers` (harvested wave 6). Canonical reference
implementations — **use** as servers, not talents to adopt (0 talent surfaces):
`filesystem`, `git`, `fetch`, `memory` (KG-backed persistent memory),
`sequentialthinking` (structured multi-step reasoning), `time`, and `everything`
(a test/demo server exercising the full protocol). These are the vetted building
blocks to reach for when a project needs a standard MCP server; our
`mcp-server-patterns` talent covers authoring new ones.

## Relations

MCP provides the connection/tools; a **skill** teaches how to use them (referenced
by fully-qualified name in `allowed-tools`). A **hook** can match an MCP tool,
be implemented as one (`type: mcp_tool`), or intercept elicitation
(`Elicitation`/`ElicitationResult`). **Plugins** bundle MCP servers. Two runtimes
exist (v1/v2); v2 default on v2.1.232+.

## AXI — the case that a well-designed CLI beats an MCP server (added 2026-09-02)

Source: `https://axi.md/` fetched 2026-09-02 (Kun Chen, @kunchenguid; reference
implementations `gh-axi`, `chrome-devtools-axi`); surfaced by a 2m48s "my AI dev setup"
video. MEASURED from the page unless marked.

- **The ten principles:** token-efficient output (TOON, "~40% token savings over JSON");
  minimal default schemas (3–4 fields per list item); content truncation with size hints
  and `--full`; pre-computed aggregates; definitive empty states ("0 results"); structured
  errors, exit codes, idempotent mutations, no interactive prompts; ambient context;
  content first (no arguments shows live data, not help); contextual next-step
  suggestions; a consistent way to get help.
- **The benchmarks, as published:** browser automation, 490 runs over 14 tasks, five
  repetitions per condition, Claude Sonnet 4.6 as both agent and judge —
  `chrome-devtools-axi` 100% success at $0.074 / 4.5 turns vs `chrome-devtools-mcp` 99%
  at $0.100 / 6.2 turns. GitHub, 425 runs — AXI "100% success at $0.050/task" vs CLI
  "86% and $0.054" vs MCP "82–87% and $0.101–$0.148". The design point: the AXI browser
  tool *wraps the same MCP server* in a CLI and wins on every metric, so the difference
  is the surface, not the backend.
- **Reading the numbers:** the judge is the same model family as the agent (no human
  calibration reported — see `llm-judge-calibration`), and the tasks are the author's.
  The cost and turn-count differences do not depend on the judge and are the robust
  part; the success-rate gap is the part to hold loosely.
- **Video claim graded:** "AXI is a framework supposed to replace MCP" — AXI is ten
  design principles for CLIs plus wrappers; it does not replace MCP's transport or
  discovery, it argues agents should be handed CLIs instead of tool schemas.

**For `mcp-server-patterns`:** the ten principles are a checklist for the *output* of any
tool we expose, MCP or not — TOON-or-terse output, 3–4 fields by default, aggregates,
definitive empties, structured errors. Worth a reuse-first read before that skill is next
rebuilt.
