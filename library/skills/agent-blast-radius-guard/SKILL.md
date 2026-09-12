---
name: agent-blast-radius-guard
description: "Use when designing, launching, or supervising an autonomous agent, loop, or wave — or the moment before any agent runs a destructive, irreversible, or outward-facing command (rm -rf, force-push, mass file/branch delete, DB drop or truncate, sending email/messages, posting to external services, or using credentials/secrets), and when granting an agent write access. Bounds the damage a run can do: enumerates its blast radius, classifies actions as reversible vs irreversible, requires a human consent gate for irreversible/outward actions, and freezes writes outside an allowed scope. This is a review method the orchestrator applies by hand — it never installs a hook or edits settings.json."
---

# Agent Blast-Radius Guard

## What & why
Autonomous agents and multi-agent waves act faster than a human can watch, so a single
bad command can be catastrophic and unrecoverable. This talent bounds the *blast radius*
before the run — the set of things the run could touch and harm — and forces the
irreversible subset through a human gate. It is the safe reimplementation of ECC's
`safety-guard`: same intent, but as a **method/checklist the orchestrator follows**, not
an auto-run `PreToolUse` hook. Our security gate forbids installed hooks, so this talent
writes nothing to `settings.json`, installs nothing, and runs no external code. It pairs
with our human-gate-proportional-to-autonomy rule and the loop-design-check.

## When to use
- Designing or launching an autonomous loop, wave, or unattended agent.
- The moment before an agent runs a destructive/irreversible or outward-facing command.
- Granting an agent (or sub-agent) write access to a repo, filesystem, or service.
- Any run whose blast radius is unclear — default to running this guard.

## Steps (the guard procedure)
1. **Enumerate the blast radius.** List everything this run could touch: local files
   and dirs, the git working tree and remote, the network, external services/APIs,
   databases, and any credentials or secrets in scope. If you cannot enumerate it, treat
   the radius as unbounded (see step 5).
2. **Classify each action reversible vs irreversible/outward.** Reversible = undoable
   from local state or git history (edit a file, add a commit, create a branch).
   Irreversible/outward = destroys data, rewrites shared history, or leaves the machine
   (see red list). When unsure, classify as irreversible.
3. **Consent gate for irreversible/outward actions** — attended vs unattended:
   - **A user's direct instruction to do a specific irreversible/outward action IS the
     per-action approval.** Don't re-gate what you were just told to do — confirm the exact
     target ("delete branch `x` on `origin` — correct?") and proceed. The gate is for actions
     the agent *chose*, not ones the user ordered.
   - **Attended, agent-chosen action:** stop, state exactly what it is and what it touches,
     ask for explicit approval. One approval = one specific action, not a standing license.
   - **Unattended run (the primary loop/wave case — no human to answer a live prompt):** a
     red-list action is **hard-disabled**, not surfaced as a prompt nobody can answer. Skip it,
     record it, and **queue it for batch human review**; the run continues on the reversible work.
4. **Scope-freeze the writes.** Define one allowed write directory (or explicit path set)
   for the run. Treat every write outside it as blocked-by-default: the agent proposes it
   and the user approves before it happens. No silent writes beyond the frozen scope —
   including config, dotfiles, and sibling repos.
5. **Default-deny on ambiguity.** If an action's reversibility, target, or scope is
   unclear, or the blast radius could not be fully enumerated, stop and ask rather than
   proceed. Ambiguity is treated as irreversible-until-proven-otherwise.

## Destructive-action red list (always gate these)
- `rm -rf`, recursive/bulk file or directory deletion, `git clean -fdx`.
- `git push --force` / `--force-with-lease`, history rewrites, tag/branch deletion on a remote.
- Mass delete of branches, files, issues, or records.
- Database `DROP`, `TRUNCATE`, unscoped `DELETE`/`UPDATE`, schema migrations against real data.
- Outward sends: email, chat/Slack, webhooks, posting or commenting on external services.
- Credential or secret use: reading, exporting, or acting with tokens, keys, or `.env` values.
- Package publish, deploy, infra apply/destroy, or anything that spends money.

## Rules
- This is a **method, not an auto-run hook**: it never installs hooks, never writes to
  `settings.json`, and never runs external code — the orchestrator applies it by hand.
- Irreversible or outward actions always ask the user first; approval is per-action.
- Writes outside the frozen scope are blocked by default.
- On any ambiguity, default-deny and ask. When unsure, classify as irreversible.
- Enumerate before you run — never launch a run whose blast radius you cannot describe.
