---
name: talent-deploy
description: "Use right after authoring, adopting, or importing a new capability (skill, agent, command, or other reusable unit) to actually DEPLOY it — make it activate and get used at the right moment, not just sit as a committed file. Validates frontmatter, enforces a non-overlapping description so it triggers correctly, wires it into the project's capability map and routing, commits, and reloads the session context so it goes live immediately. The last step of every author/adopt/import job in any project."
---

# talent-deploy — make an added capability live and routable

Adding a file to a skills/agents/commands directory is NOT deploying it. A capability only
gets used if it (1) loads, (2) has a description sharp and distinct enough to trigger at the
right moment, and (3) is wired into whatever routes the project follows to select capabilities.
This is the checklist that closes that gap. It applies to any project that installs reusable
units, whatever they are called locally.

## When to use
- Immediately after authoring a new capability, or after adopting/importing one from another
  source — the final step of any "author a capability" or "adopt a capability" workflow.

## Deploy checklist (all must pass)
1. **Frontmatter valid.** Required identity field (e.g. `name:`, kebab-case, matching the
   directory) AND `description:` present. A missing/mismatched identity → the unit may never
   load. Authored from the correct scaffold/template for its type.
2. **Description will trigger at the right time.** Trigger-first ("Use when…"), third person,
   keyword-rich, concrete triggers, under the cap the project pins (here: `pipeline/CONSTANTS.md`). **Check for overlap** with the
   descriptions of existing units: if two units could both claim the same job, sharpen BOTH
   so exactly one triggers. Overlap = mis-trigger.
3. **Earned activation.** The unit has been validated by whatever bar the project sets before
   activation (e.g. an eval, a test, a review, a demonstrated improvement over baseline). Deploy
   what demonstrably helps, not what merely exists. Not yet validated → do not deploy yet.
4. **Wire the routes** (so selection USES it, not just relies on auto-trigger):
   - Add an entry to the project's **capability map** (job → unit), wherever that lives
     (e.g. a CLAUDE.md table, a README index, a registry file).
   - Add/insert it into the relevant **routing chain(s)** the project uses to sequence work.
   - If the unit does not auto-trigger (e.g. it is marked for explicit invocation only), name
     its explicit call site.
5. **Persist.** Commit (Conventional Commits) and push — so the deploy survives fresh checkouts
   and environment resets.
6. **Activate live in-session (the actual "deploy").** Newly committed units are typically not
   picked up mid-session automatically. Trigger a **context reload** so the running session sees
   the unit immediately, using whatever mechanism the harness/environment provides for
   re-scanning the capability directory. **Capture the reload's acknowledgement** — whatever the
   mechanism returns to confirm it ran — as the evidence this step happened; an activation that
   leaves no trace is indistinguishable from one that was skipped.
   "A fresh session will load it anyway" is a DEFERRAL, not a deploy: it is true and it does not
   help the work in front of you, which is running in this session against a capability the
   session cannot see. Deferring activation to the next session is the same outcome as skipping
   it, reached through a gentler verb.
7. **Record the activation where the project's own deploy-gap detector reads.** Update the
   catalog/registry status (and note its source if it was adapted from one) and log first use
   wherever usage is tracked — but neither of those is the deploy record. Find what the project
   uses to answer *"which units are wired but never activated?"* and write THIS unit's activation
   into that store, as a per-unit event with a timestamp. If the project has no such store,
   creating one is part of deploying: an unmeasured step reverts to being remembered, and memory
   is not a control.

## Rules
- **A committed unit that nothing routes to is not deployed.** Wiring (step 4) is not optional.
- **A unit that has not been reloaded is not deployed either.** Activation (step 6) is not
  optional, and it is a per-unit EVENT, not a periodic habit — "we reload at the end of every
  batch anyway" leaves each unit's activation unowned and unrecorded, so a miss looks exactly
  like a success. Routing makes a unit FINDABLE; only the reload makes it LIVE. Two different
  failures, each needing its own evidence.
- **No deploy without earned activation** — activation is earned by evidence it helps (step 3).
- Reversible: deploy adds and wires; it never deletes or overwrites another unit (human gate).
- After deploy, the next unit of work can immediately route to the new capability.

## In this repo (one instance of the general method)
- Units are "talents" (skills, agents, commands) under `.claude/skills/`.
- Overlap check uses `skill-scout` / `skill-stocktake`; sharpen a mis-triggering description
  via `skill-description-optimizer` (`writing-skills` authors one from blank).
- Earned activation = passing `eval-harness` (baseline-vs-with).
- Capability map = the CLAUDE.md map; routing = `pipeline/ROUTING.md` chain(s).
- Context reload = call the `register_repo_root` MCP tool for this repo (owner `matlingatlin`,
  repo `skills-repo`, `directory` `/home/user/skills-repo`); it acknowledges with
  `status: context_reload_requested` — that acknowledgement is step 6's evidence.
- Record = append a `deployed` event row for the talent to `pipeline/ledgers/talents.jsonl`
  (this is the row `pipeline/queries/signals.py` reads to compute the deploy gap — the catalog
  status and `talents_used` are NOT read by it), then set the catalog entry `status: adopted`
  (+ `adapted_into` if built from a source) and log the talent in this wave's `metrics.jsonl`
  `talents_used` on first run. See `pipeline/DATA.md`, "Deploy is an EVENT, not a habit".
- Invoked as the last step of the `/piano` author/adopt chains.
