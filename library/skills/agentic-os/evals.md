# Evals — agentic-os

> Baseline-vs-with suite for the `agentic-os` talent. Authored against
> `templates/EVALS.template.md` and `pipeline/CURATION-LESSONS.md` ACTIVE DIRECTIVES.

**Talent:** `agentic-os` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result is materially
better and meets the observable pass criterion. Adversarial and honest — no rubber-stamping.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 3 normal/representative (N1–N3) + 3 clever/adversarial (C1–C3)
      + 1 negative-trigger (NT1).
- [x] **Specific to this talent** — every scenario exercises a concrete agentic-os claim
      (layered kernel/agents/commands/scripts/data, external cron, declarative routing,
      file-based data layer, non-destructive schema evolution, credential hygiene).
- [x] **Observable pass/fail criterion** on each — a checkable structural artifact, not "looks good".
- [x] **Clever ones designed so baseline plausibly FAILS** (C1–C3).
- [x] **Matches talent type:** technique → application scenarios (N1–N3) + trap/pressure (C1–C3).
- [x] **Negative trigger** (NT1): auditing a *deployed* OS should defer, not fire.

## Scenarios

### N1 — Stand up the OS structure · application
- **Input:** "Set up a personal agentic OS on Claude Code for my recurring solo work — dev, writing, research."
- **Pass criterion (observable):** Produces the layered structure — `CLAUDE.md` kernel with a
  declarative agent-registry/routing table, `agents/*.md` specialist files, `.claude/commands/*.md`,
  `scripts/` for daemons, and `data/` for JSON/markdown state — as *separate* layers, not one file.
- **Baseline (without talent):** One monolithic `CLAUDE.md` (or a single mega-prompt) that tries
  to be dev+writer+researcher, with no agent/command/data separation. FAIL.
- **With talent:** Emits the four/five-layer skeleton with a routing table and one agent file each. PASS.
- **Result:** pass

### N2 — Scheduled briefing that survives session end · application
- **Input:** "Add a daily 8am briefing that runs even when no Claude session is open."
- **Pass criterion (observable):** Recommends an OS-level scheduler (LaunchAgent / systemd timer /
  pm2 cron_restart) invoking the `/daily-sync` command, and explicitly avoids Claude Code's
  in-session cron because it dies with the session.
- **Baseline (without talent):** Suggests Claude Code's built-in scheduled task / session cron,
  which stops when the session ends — does not survive. FAIL.
- **With talent:** Wires an external systemd/launchd/pm2 job. PASS.
- **Result:** pass

### N3 — Memory across sessions · application
- **Input:** "How should each session pick up where the last one left off?"
- **Pass criterion (observable):** Reads `data/` (daily logs, project files, decisions) at session
  start and writes an append-only reflection/log at session end — no vector DB, no external store.
- **Baseline (without talent):** Treats each session as stateless / starts fresh, or reaches for a
  vector DB. FAIL on "survives across sessions" via plain files.
- **With talent:** Read-at-start / append-reflection-at-end file pattern. PASS.
- **Result:** pass

### C1 — "Just put routing in code" pressure · pressure/trap
- **Input:** "Move the intent routing into a Python function with if/else — markdown tables feel slow and hacky."
- **Pass criterion (observable):** Keeps routing declarative in `CLAUDE.md` markdown tables and
  explains why (inspectable/editable/debuggable without running code); does NOT hand back a
  code-based router as the system's routing layer.
- **Baseline (without talent):** Complies and writes an `if intent.includes('deploy')` router,
  burying routing in code — the exact anti-pattern. FAIL.
- **With talent:** Declines the code router, keeps the declarative table. PASS.
- **Result:** pass

### C2 — Postgres for a solo user · trap
- **Input:** "Set up a Postgres database to store my ~40 project records and decision logs."
- **Pass criterion (observable):** Defers the external DB; uses JSON/markdown files under `data/`,
  and states the threshold for a real DB (multiple concurrent users or GBs of data).
- **Baseline (without talent):** Provisions Postgres + schema + connection code for 40 rows. FAIL.
- **With talent:** File-based `data/` layer; DB only past the stated threshold. PASS.
- **Result:** pass

### C3 — Rename a data field · edge/trap
- **Input:** "The `priority: high` field should become a structured object with a rationale — rename it."
- **Pass criterion (observable):** Does NOT rename in place; keeps the old field (e.g. marked
  `_deprecated_priority`) and adds the new `priority_v2` object, so historical logs still read.
- **Baseline (without talent):** Renames the field across files, silently breaking older records
  that still carry the old key. FAIL.
- **With talent:** Additive, non-destructive schema evolution. PASS.
- **Result:** pass

### NT1 — Audit a deployed OS's security · negative-trigger
- **Input:** "My agentic OS is live in production — audit whether its agents' tool grants are over-scoped and could do damage."
- **Pass criterion (observable):** Does NOT fire agentic-os build guidance; recognizes this is
  operating/auditing a deployed system and defers to the security/blast-radius talents
  (agent-surface-security-audit / agent-blast-radius-guard), per its own scope clause.
- **Baseline (without talent):** N/A — this tests that agentic-os *declines*. A greedy talent that
  fired here and started re-architecting the OS would be over-triggering.
- **With talent:** Declines and points to the audit talents. PASS (correct non-fire).
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. Root-cause protocol unused this pass.

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
- Notes: C1–C3 discriminate cleanly (baseline plausibly produces the named anti-pattern each time);
  N1–N3 confirm the everyday build job; NT1 guards the "building, not auditing" scope boundary that
  keeps this talent distinct from the agent-security/blast-radius talents.
