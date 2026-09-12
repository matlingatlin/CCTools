# First eval wave — build-now shortlist

12 factory-infrastructure skills security-read (Phase C) and, where safe, A/B evaluated baseline-vs-with-skill on a planted-defect scenario (Phase D). Method: one runner per skill, BASELINE arm first (no skill) then WITH-SKILL arm, scored against 3 criteria from the recon design. Single-agent A/B (baseline-first, so the baseline is uncontaminated) — a screening wave, not the 5-rep full protocol.

## Adopted (9/9 evaluated → adopt)

All nine flipped every criterion (baseline 0/3 → with-skill 3/3) and are copied verbatim into `.claude/skills/` with upstream provenance preserved.

| Skill | Source | Type | Security | Baseline→With | Verdict |
| --- | --- | --- | --- | --- | --- |
| `writing-skills` | superpowers | technique | safe | 0/3 → 3/3 | adopt |
| `skill-scout` | ECC | technique | safe | 0/3 → 3/3 | adopt |
| `skill-stocktake` | ECC | technique | safe | 0/3 → 3/3 | adopt |
| `eval-harness` | ECC | reference | safe | 0/3 → 3/3 | adopt |
| `santa-method` | ECC | discipline | safe | 0/3 → 3/3 | adopt |
| `verification-before-completion` | superpowers | discipline | safe | 0/3 → 3/3 | adopt |
| `subagent-driven-development` | superpowers | technique | safe | 0/3 → 3/3 | adopt |
| `dispatching-parallel-agents` | superpowers | discipline | safe | 0/3 → 3/3 | adopt |
| `context-budget` | ECC | reference | safe | 1/3 → 3/3 | adopt |

### What each adopted skill adds

- **writing-skills** — Skill flips all three criteria; produces a materially stronger discipline skill.
- **skill-scout** — Prevents duplicate skills; enforces search-first, ranked decision table, and security vetting of external matches.
- **skill-stocktake** — Skill adds explicit path inventory, named-target merge verdicts with specific defects, and mandatory confirmation gate baseline lacked.
- **eval-harness** — Skill cleanly enforced eval-before-code, pass@k reporting, and a rerunnable artifact; caught untested edges.
- **santa-method** — Independence plus AND-gate plus fresh re-review reliably catches hallucinations single self-review rationalizes.
- **verification-before-completion** — Clear behavioral gate; converts 'should pass' into evidence-backed claims; catches hidden failures.
- **subagent-driven-development** — Independent review catches the spec trap; ledger and file handoff cut context cost.
- **dispatching-parallel-agents** — Skill turns sequential debugging into scoped parallel dispatch with real integration checks.
- **context-budget** — Skill adds rigorous quantification and ranked savings; baseline stays vague.

## Flagged by the security gate (3) — not adopted as-is

The gate did its job: three skills carry real risk and were NOT live-evaluated or installed. Their decisions:

- **`deep-research`** (ECC): **adapt** — outbound web via firecrawl/exa MCP (prompt-injection surface) and needs MCPs we lack; overlaps our `research-methodology`. Fold its cited-report rigor into our own research skill rather than adopt.
  - Security read: Makes live network calls through third-party MCP servers (firecrawl, exa) to search and scrape arbitrary URLs, then deep-reads and synthesizes untrusted web content into a report — classic prompt-injection surface from scraped pages. No sec
- **`strategic-compact`** (ECC): **adapt (hook-free)** — registers a `PreToolUse` hook running an unbundled/unauditable node script that reads the transcript, and recommends an unvetted third-party 'token-optimizer' MCP. Take only the manual-`/compact`-at-task-boundaries discipline; never the hook or the MCP.
  - Security read: The skill's mechanism is a hook (suggest-compact.js) registered on PreToolUse for Edit/Write, so it executes a node script on every edit — external code execution wired into the tool loop. The script is NOT bundled in this directory (plugin
- **`skill-comply`** (ECC): **defer (sandbox)** — spawns `claude -p` running LLM-generated commands with Bash + a pip/npm/unzip allowlist under your credentials. Valuable (automated compliance measurement) but only safe in a network-isolated, non-privileged container.
  - Security read: By-design external code execution: it spawns `claude -p` subprocesses that run LLM-generated scenario prompts with --allowedTools including Bash, and executes LLM-generated setup_commands. Mitigations are real but partial: scenarios run in 

## Notes

- `writing-skills` overlaps our existing knowledge notes on skill-authoring/testing; it is the canonical full-length skill, so it supersedes those notes as the operational reference.
- `skill-stocktake`'s eval found a real bug in an un-adopted ECC skill (`autonomous-agent-harness` references a nonexistent `claude -p --project` flag).
- Provenance: superpowers skills are MIT-licensed upstream; ECC skills retain their upstream headers. Copied verbatim; no upstream SKILL.md was modified.