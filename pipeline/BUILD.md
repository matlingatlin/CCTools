# Build & run spec — how to start the piano

How to start a new Claude Code project where all talents load and the piano runs.
Read with `SPEC.md` (the full system), `BRAIN-ARCHITECTURE.md` (the blocks), and
`ROUTING.md` (job → talent chains).

## 1. Start the project (talents auto-load)
1. In Claude Code (web), create a **new session with `matlingatlin/skills-repo` as the
   source repo** (not hello-world). Cloud sessions load the repo's `.claude/skills/`,
   `.claude/agents/`, and `CLAUDE.md` automatically.
2. Confirm: type `/` — you should see the 34 talents (deep-reading, eval-harness,
   skill-scout, …) and be able to invoke any with `/name`.
3. `CLAUDE.md` (standing rules + capability map) and `pipeline/frontier.json`
   (git-persisted state) are loaded — the brain has its rules and its queue.

To try it inside THIS hello-world session instead: `/add-dir /home/user/skills-repo`
(loads its skills/agents), though a fresh session from the repo is the clean path.

## 2. What runs today vs what to build
**Runs today (the 34 adopted talents + the gates):** you can already, by hand or via
`/piano`, harvest a repo/paper, deep-read it, run the four gates, eval a candidate,
and adopt winners — using the talents we have. The catalog (469) + frontier tell the
piano what's left.

**Still to author (the generalized brain-talents — the adapt patterns):** these were
pattern-borrowed but not yet written as runnable talents. Build them in this order:

1. **`research-scout`** — generate search terms + sources + entities (core domains AI/
   ML/data/IT/SE/NLP by default; psychology/cognition/design as bonus). Feeds frontier.
2. **`source-methods`** — one method per source type (github/pdf/profile/top-10/docx),
   each routing to the right talent (`pdf`, `deep-reading`, Graphify code-only).
3. **`intake-db`** — two-tier store: Classify→Deduplicate→Store→Index (generalize
   `knowledge-ops`); raw `intake/` → tested `.claude/skills/`.
4. **`dedup-guardian`** — prospective gate (new candidate vs whole library) +
   retroactive audit (cluster near-duplicates, propose merges).
5. **`library-curator`** — the librarian: re-test, sharpen descriptions, cluster,
   sort, update the map (we ran its description pass manually — package it).
6. **`pipeline-engine`** — generalize `orch-pipeline`: gated harvest→build→test→store.
7. **`talent-router`** — generalize `plan-orchestrate`: job → ordered talent chain
   (backed by `ROUTING.md`).
8. **`piano` orchestrator** — the entry point (scaffolded here): read frontier → pick
   job → run chain → gates → coordinator-commit → update STATUS → loop safely.

Each new talent is itself built through the factory (reuse-first → author →
eval-harness + santa-method → verification-before-completion → adopt) and wired into
`CLAUDE.md` + `ROUTING.md`.

## 3. How the autonomous run works
- **Entry point:** `/piano` runs one wave (see `.claude/skills/piano/SKILL.md`).
- **Keep it running — completion-chained (default):** each wave, as its last step,
  schedules the NEXT wave with a one-shot `send_later` (re-delivering `/piano` into the
  same session) — but only if it finished cleanly and no stop-condition hit. Wave N+1
  cannot start until wave N completes and schedules it: sequential, never overlapping.
  The `send_later` reminder is durable, so the chain survives container reclaim; git
  state means each wave resumes from the frontier. A fixed-interval cron is deliberately
  NOT used (it would fire regardless of the previous wave's state). `/loop /piano`
  remains for self-paced runs inside an interactive session.
- **Cadence:** producer→consumer — research-scout feeds the frontier, harvester
  consumes it, the factory consumes candidates. Always something to consume.
- **Loop safety (`loop-design-check`):** decidable stop-condition, anti-spin damping,
  and a human gate before anything irreversible.
- **Stop:** you say stop (or a wave-budget cap). State is in git, so it resumes.

## 4. Human control (non-negotiable)
- Auto-allowed: harvest, deep-read, eval, adopt-into-library, sharpen descriptions,
  commit — all reversible via git.
- Ask the user first: merge/delete a talent, push anything outward, or any
  irreversible step. (`loop-design-check`: the more autonomous, the stricter the gate.)

## 5. The very first run
In the new session, once talents load:
```
/piano
```
It will report the next job from the frontier and run it. To let it run continuously:
```
/loop /piano
```
Watch `pipeline/STATUS.md` for a one-line-per-wave record of what happened.
