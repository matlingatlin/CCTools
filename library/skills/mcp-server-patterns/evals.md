# Evals — mcp-server-patterns

> Follows `templates/EVALS.template.md`. Authored against CURATION-LESSONS ACTIVE DIRECTIVES:
> blended (normal + clever), observable criteria, clever scenarios designed so the baseline
> plausibly fails, application-type scenarios (technique talent), plus a negative-trigger.

**Talent:** `mcp-server-patterns` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result is materially
better and meets the pass criterion. Be adversarial and honest.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
A good test SUITE is a BLEND — normal + clever — all specific to THIS talent:
- [x] **Mix, not only traps.** S1–S2 normal/representative; S3–S5 clever/adversarial; S6 negative-trigger.
- [x] **Specific to this talent** — every scenario about building/debugging an MCP server.
- [x] **Observable pass/fail criterion** an outsider could check.
- [x] **Clever baselines plausibly FAIL** (hardcoded SDK signature, ignored cost, SSE-by-default).
- [x] **Matches talent type** — technique → application scenarios.
- [x] **Negative trigger** — MCP *client configuration*, where this skill should NOT fire.

## Scenarios

### S1 — New tool with validation · application
- **Input:** "Add a `search_docs(query, limit)` tool to our MCP server."
- **Pass criterion (observable):** Response defines an input **schema** (Zod or SDK equivalent)
  for `query`/`limit`, registers via the SDK's tool-registration call, and returns a structured
  result/error — not a bare handler that trusts raw args or throws stack traces.
- **Baseline (without talent):** Plausibly writes a handler taking untyped args, no schema,
  errors surface as raw exceptions.
- **With talent:** Schema-first tool, validated inputs, structured error path. **PASS**
- **Result:** pass

### S2 — Transport choice for a local desktop client · application
- **Input:** "This server will run locally for Claude Desktop. Which transport?"
- **Pass criterion (observable):** Recommends **stdio** for the local client and keeps server
  logic transport-independent so HTTP can be swapped at the entrypoint.
- **Baseline (without talent):** May pick HTTP by default or couple tool logic to the transport.
- **With talent:** stdio for local; logic/transport separated. **PASS**
- **Result:** pass

### S3 — SDK signature from memory · trap
- **Input:** "Register the tool with `server.tool('name', 'desc', schema, handler)` — that's the
  API, right? Just confirm and move on."
- **Pass criterion (observable):** Does NOT blindly confirm one hardcoded signature; flags that
  the `@modelcontextprotocol/sdk` registration API has changed across versions (positional vs
  object form, `tool()` vs `registerTool()`) and says to verify against current docs/Context7
  for the pinned version.
- **Baseline (without talent):** Rubber-stamps the one signature from memory → wrong on other
  SDK versions, copy-paste error ships.
- **With talent:** Version-aware, points to verifying the current signature. **PASS**
- **Result:** pass

### S4 — Tool calling a paid external API · trap
- **Input:** "Add a tool that hits the Stripe API to create a charge on each call. Ship it."
- **Pass criterion (observable):** Raises **idempotency** (a charge tool must be retry-safe) and
  **rate/cost** concerns, and recommends documenting them in the tool description — not just a
  raw pass-through handler.
- **Baseline (without talent):** Writes a straight wrapper; retries could double-charge, no cost note.
- **With talent:** Idempotency + rate/cost surfaced and documented. **PASS**
- **Result:** pass

### S5 — "Use SSE for the new remote server" · edge/pressure
- **Input:** "Build the remote transport with HTTP+SSE — that's the standard MCP remote setup."
- **Pass criterion (observable):** Corrects the premise: **Streamable HTTP** (single endpoint) is
  the current preferred remote transport; legacy HTTP/SSE only for backward compatibility.
- **Baseline (without talent):** Accepts SSE as "standard" and builds the legacy path.
- **With talent:** Recommends Streamable HTTP, SSE only as compat. **PASS**
- **Result:** pass

### S6 — Adding an existing MCP server to a client · negative-trigger
- **Input:** "Add the GitHub MCP server to my Claude Code config so I can use its tools."
- **Pass criterion (observable):** Skill does NOT fire its server-building method; this is client
  MCP *configuration* (`claude mcp add` / settings), not authoring a server. Response routes to
  config, not to `McpServer`/Zod/transport patterns.
- **Baseline (without talent):** N/A — negative case; confirms no false trigger.
- **With talent:** Recognizes out-of-scope; declines to apply server-authoring patterns. **PASS**
- **Result:** pass

## Failure triage (if any scenario failed)
None failed. No test-bug or skill-bug surfaced.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
