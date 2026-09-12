---
title: Claude Agent SDK (TypeScript) — the options, hooks, subagent limits and hosting rules that decide how a build loop is wired, as of 2026-09-03
sources:
  - url: https://code.claude.com/docs/en/agent-sdk/typescript
    note: "query() Options field list (names and types) read from the reference table; AgentDefinition. Raw: knowledge/raw/web-2026-09-03-sdk-and-stack/sdk-typescript-reference.html"
    fetched: 2026-09-03
  - url: https://code.claude.com/docs/en/agent-sdk/hosting
    note: "Subprocess model, session patterns, resources, cost sentence, multi-tenant isolation, known limitations. Raw: sdk-hosting.html"
    fetched: 2026-09-03
  - url: https://code.claude.com/docs/en/agent-sdk/subagents
    note: "AgentDefinition fields, what a subagent inherits, depth/concurrency/spend caps with defaults. Raw: sdk-subagents.html"
    fetched: 2026-09-03
  - url: https://code.claude.com/docs/en/agent-sdk/hooks
    note: "Hook event table (Python vs TypeScript availability), callback output fields. Raw: sdk-hooks.html"
    fetched: 2026-09-03
  - url: https://code.claude.com/docs/en/agent-sdk/skills
    note: "Skills are filesystem artefacts discovered through settingSources; the skills option scopes invocation. Raw: sdk-skills.html"
    fetched: 2026-09-03
  - note: "Package version 0.3.259 measured with npm view on 2026-09-03 (raw: npm-view-versions-2026-09-03.txt). Hosted alternative and its numbers: [[managed-agents-architecture]]."
status: verified
tags: [agent-sdk, harness, hooks, subagents, skills, hosting, multi-tenant, isolation, limits, cost, typescript, scio]
related: ["[[subagents]]", "[[hooks]]", "[[managed-agents-architecture]]", "[[agent-harness-principles-2026]]", "[[api-agent-loop]]", "[[claude-code-extension-layer]]", "[[typescript-stack-scan-2026-09]]"]
---

# Claude Agent SDK (TypeScript) — options, hooks, limits, hosting

Written 2026-09-03 for Scio's Slice 1 design, which runs its build loop on this SDK (Scio
ADR-0004). [[subagents]] and [[hooks]] hold the Claude Code feature docs; this note holds the
**SDK-specific** contract a hosting application programs against, with the version it was read
at. Everything below is the vendor's documentation, not our measurement, except the version.

## Claims

| # | Claim | Source | Verbatim / value | Verdict |
|---|---|---|---|---|
| 1 | Package and version | npm view, 2026-09-03 | `@anthropic-ai/claude-agent-sdk` **0.3.259** | MEASURED (as of 2026-09-03) |
| 2 | One session is one subprocess with its own shell, cwd and JSONL transcripts | hosting | "Every running agent is a long-lived process tied to local state" | REPEATED (vendor) |
| 3 | The options that wire a build loop exist by these names | typescript reference | `agents`, `hooks`, `skills` (`string[] \| 'all'`), `plugins`, `mcpServers`, `allowedTools`, `disallowedTools`, `permissionMode`, `canUseTool`, `maxTurns`, `maxBudgetUsd`, `taskBudget` (alpha, tokens), `effort` (`low\|medium\|high\|xhigh\|max`), `model`, `fallbackModel`, `settingSources`, `cwd`, `env`, `sessionStore`, `sessionStoreFlush`, `persistSession`, `resume`, `forkSession`, `sandbox` (`SandboxSettings`), `outputFormat` (`json_schema`), `systemPrompt` (string, array, or the `claude_code` preset with `append`), `enableFileCheckpointing` | REPEATED (field table) |
| 4 | Subagents are defined programmatically per query | subagents | `AgentDefinition{description, prompt, tools, disallowedTools, model, skills, memory, mcpServers, initialPrompt, maxTurns, background, effort, permissionMode}`; "Programmatically defined agents take precedence over filesystem-based agents with the same name" | REPEATED |
| 5 | A subagent starts with a fresh context; only the Agent tool's prompt crosses | subagents | "The only content you pass from parent to subagent is the Agent tool's prompt string" | REPEATED |
| 6 | Default caps: depth 3, concurrency 20, spend unlimited | subagents (SDK ≥ 0.3.219) | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` default 3 (1 = no nesting); `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` default 20; `maxBudgetUsd` "No limit. Compared against `total_cost_usd`, so subagent requests count" and at the cap "ends the query with the `error_max_budget_usd` result subtype" | REPEATED (documented defaults) |
| 7 | No session timeout; `maxTurns` is the stop; no per-subagent wall clock | hosting, known limitations | "A session does not time out on its own. Set `maxTurns`"; `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` is a stall watchdog, "not a total-runtime deadline" | REPEATED |
| 8 | Hook events available to the TypeScript SDK | hooks table | `PreToolUse` (can block or modify), `PostToolUse`, `PostToolUseFailure`, `PostToolBatch` (TS only), `UserPromptSubmit`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `PermissionRequest`, `PermissionDenied`, `SessionStart`, `SessionEnd`, `Setup`, `Notification`, `TaskCreated`, `TaskCompleted`, `InstructionsLoaded`, `FileChanged`, `CwdChanged`, `WorktreeCreate/Remove`, `ConfigChange`, `Elicitation`, `MessageDisplay`, `UserPromptExpansion`, `PreModelSwitch` (can block), `PostModelSwitch`, `TeammateIdle`, `DirectoryAdded` | REPEATED; several are TypeScript-only (the table marks Python "No") |
| 9 | A hook decides with a fixed output shape | hooks | `PreToolUse`: `permissionDecision` `allow \| deny \| ask \| defer`, `permissionDecisionReason`, `updatedInput`; `PostToolUse`: `additionalContext`, `updatedToolOutput`; `systemMessage`; "Return `{}` to allow the operation without changes" | REPEATED |
| 10 | Skills are files, never registered in code; the `skills` option only scopes | skills | "Unlike subagents… you create skills as files on disk. The SDK doesn't provide a programmatic API for registering them"; discovered through `settingSources` `user`/`project`; `skills: []` disables invocation; `/<name>` dispatch ignores the list | REPEATED |
| 11 | Multi-tenant isolation is four settings | hosting | `settingSources: []`; `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env` ("loads into the system prompt regardless of `settingSources`"); `CLAUDE_CONFIG_DIR` per tenant; `cwd` per query; plus per-tenant egress rules at the proxy. In TypeScript `env` **replaces** the subprocess environment — spread `process.env` | REPEATED |
| 12 | Resources and cost | hosting | "1 GiB RAM, 5 GiB disk, and 1 CPU per agent is a reasonable starting point"; "Anthropic token cost typically dominates container infrastructure cost by an order of magnitude or more. A minimally provisioned container runs roughly $0.05 per hour" | REPEATED (vendor figures, not ours) |
| 13 | Session persistence is a best-effort mirror | hosting | `SessionStore` mirrors transcripts only (not `CLAUDE.md` or working-directory files); a dropped batch emits `{ type: "system", subtype: "mirror_error" }` and the query continues | REPEATED |
| 14 | Subagent output is scanned for instruction-shaped patterns before the parent reads it | subagents | control-tag imitation neutralised in place, turn markers escaped, permission-config mentions kept, a `[harness: …]` marker prepended; "it never removes or rewords the subagent's text" (Claude Code ≥ 2.1.210) | REPEATED |
| 15 | The hook INPUT fields per event, as typed in the installed package | `sdk.d.ts` of 0.3.259 (raw: `knowledge/raw/web-2026-09-06-evidence-schemas/claude-agent-sdk-0.3.259-sdk.d.ts`, lines 167–181, 2438–2568, 8332–8420) | `BaseHookInput{session_id, transcript_path, cwd, prompt_id?, permission_mode?, agent_id?, agent_type?}`; `PreToolUse{tool_name, tool_input, tool_use_id}`; `PostToolUse{tool_name, tool_input, tool_response, tool_use_id, duration_ms?}`; `PostToolUseFailure{tool_name, tool_input, tool_use_id, error, is_interrupt?, duration_ms?}`; `PostToolBatch{tool_calls[]{tool_name, tool_input, tool_use_id, tool_response?}}`; `UserPromptSubmit{prompt, source?, session_title?}`; `Stop{stop_hook_active, last_assistant_message?, background_tasks?, session_crons?}`; `StopFailure{error, error_details?, last_assistant_message?}`; `SubagentStart{agent_id, agent_type}`; `SubagentStop{stop_hook_active, agent_id, agent_transcript_path, agent_type, last_assistant_message?, …}`; output: `SyncHookJSONOutput{continue?, suppressOutput?, stopReason?, decision?: approve\|block, systemMessage?, reason?, hookSpecificOutput?}`; `HookPermissionDecision = allow\|deny\|ask\|defer`; `PreToolUseHookSpecificOutput{permissionDecision?, permissionDecisionReason?, updatedInput?, additionalContext?}`; `PostToolUseHookSpecificOutput{additionalContext?, updatedToolOutput?…}` | MEASURED (read from the installed d.ts; `agent_id` is "present only when the hook fires from within a subagent", the doc comment says) |
| 16 | Permission and tool availability are two separate options, and "dontAsk" denies anything not pre-approved | `sdk.d.ts` of 0.3.259 (raw: `knowledge/raw/web-2026-09-06-evidence-schemas/sdk.d.ts`, read 2026-09-09) | `allowedTools`: "List of tool names that are auto-allowed without prompting for permission ... To restrict which tools are available, use the `tools` option instead"; `tools`: "Specify the base set of available built-in tools ... `[]` (empty array) - Disable all built-in tools"; `permissionMode` `'dontAsk'`: "Don't prompt for permissions, deny if not pre-approved"; `AgentDefinition.tools`: "Array of allowed tool names. If omitted, inherits all tools from parent" | MEASURED |
| 17 | Cost and token accounting on a result: `total_cost_usd` is an estimate and cumulative per `query()`; `usage` is the MAIN LOOP ONLY (excludes Task subagents); `modelUsage` is the per-model record with the cache fields | `sdk.d.ts` of 0.3.259 (raw: `knowledge/raw/web-2026-09-06-evidence-schemas/sdk.d.ts`, lines 1307–1316, 4897–4911, read 2026-09-09) | `total_cost_usd`: "Cumulative estimated cost in USD for this query() call … cumulative across turns in streaming-input sessions — each result carries the running total so far, so read the latest result rather than summing across results … An estimate, not a billing statement."; `usage`: "MAIN AGENT LOOP ONLY — excludes Task subagent, sidechain, and auxiliary model calls … Prefer modelUsage for token/cost accounting."; `ModelUsage = { inputTokens, outputTokens, thinkingTokens?, cacheReadInputTokens, cacheCreationInputTokens, webSearchRequests, costUSD, contextWindow, maxOutputTokens, canonicalModel?, … }` | MEASURED |

## What it means here

- **Claim 10 collides with Scio's mediation rule and resolves cleanly:** the skill *list* is still
  computed by code (`skills: [...]`), but the skill *files* must exist under a `settingSources`
  path or a plugin. With `settingSources: []` for tenant isolation (claim 11), skills must come in
  through `plugins` — the SHA-pinned plugin Scio ADR-0008 already names. The two claims together
  fix the wiring: isolation off the filesystem, skills from the plugin, list from Contract.
- **Claim 6 is the agent cap Scio wanted as a hook:** `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` in
  `env` is the mechanism, with `maxBudgetUsd` as the spend stop; a `SubagentStart` hook adds the
  evidence row, not the enforcement.
- **Claim 9 is the shape of every level-2 guarantee hook** in Scio's talent table: deny with a
  reason on `PreToolUse` (file-plan fence, command trust, spend ceiling before the call), replace
  output on `PostToolUse` (instrumentation guard, package stamp), `additionalContext` for the
  console classifier.
- **Claim 12's $0.05/hour is the vendor's container figure**; the sandbox providers' own prices
  are in [[typescript-stack-scan-2026-09]]. Claim 7 means the stop rule is Scio's to write.

## What is open

- `SandboxSettings` (claim 3) — the field exists; its contents were not read.
- The Python SDK lacks several events (claim 8); Scio is TypeScript end to end, so this does not
  bind, but a port would.
- Nothing here is measured by us: per-session RSS, real container cost and the hook latency are
  the numbers Slice 1 must record.

## Added 2026-09-06
Claim 15 pins the hook input and output field names from the installed 0.3.259 declarations, because Scio's Build layer types its eighteen hooks structurally against them (framework-free) and a renamed field must fail a test, not a build. The `last_assistant_message` on `Stop`/`SubagentStop` is what lets a verdict be parsed without reading the transcript file.

## Added 2026-09-09
Claim 16 settles a question Scio's review 15 raised: under `permissionMode: "dontAsk"` a subagent whose `tools` list names Write or Bash is still DENIED unless the session's `allowedTools` pre-approves those tools, because a subagent's list only narrows what it inherits. A session that restricts `allowedTools` to the orchestrator's four tools therefore blocks every package-builder write; the correct shape is `allowedTools` = the union every role needs, `tools` = the base set, and a hook that fences the orchestrator (Scio `packages/build/src/hooks/hooks.ts`, `orchestrator-fence`).

Claim 17 (same day) is what Scio's ADR-0019 (caching as one decision) and ADR-0021 (the ceiling covers the whole pipeline) rest on: a ledger that prices from `total_cost_usd` records an estimate that mixes the main loop and subagents and cannot be reconciled to tokens; the per-model `modelUsage` record carries `cacheReadInputTokens` and `cacheCreationInputTokens`, so a ledger row can price reads and writes at their own rates (the rates are in [[token-economy-playbook]] §2.3). Scio's producer (`packages/build/src/loop/producer.ts`) takes `costUsd` from the last result event, which is the right read of a cumulative figure, but it is the estimate, not the priced figure.

The `modelUsage` fields of claim 17 map onto the OpenTelemetry GenAI span attributes in [[otel-genai-semantic-conventions-2026-09]] (added 2026-09-09).

The network and browser boundary around a build - iframe sandboxing, frame-ancestors, an egress firewall with live updates - is in [[preview-and-sandbox-egress-boundary-2026-09]] (added 2026-09-09).
