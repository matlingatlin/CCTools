# Talent templates — author every new talent from the right scaffold

A talent authored ad-hoc comes out inconsistent and mis-triggers. Every new talent starts
from one of these templates so it has the right shape, valid frontmatter, and a description
that triggers at the right time. The factory's "Author a talent" chain (`pipeline/ROUTING.md`)
copies the matching template, then `writing-skills` fills it in.

## Which template
| Talent type | File it becomes | Template | Auto-invoked? |
| --- | --- | --- | --- |
| **Technique / method skill** | `.claude/skills/<name>/SKILL.md` | `SKILL.technique.template.md` | Yes — triggers by `description` |
| **Orchestrator / discipline skill** | `.claude/skills/<name>/SKILL.md` | `SKILL.orchestrator.template.md` | No — `disable-model-invocation`, called explicitly |
| **Subagent** | `.claude/agents/<name>.md` | `AGENT.template.md` | By the Agent/Task tool |
| **Command** | `.claude/commands/<name>.md` | `COMMAND.template.md` | By `/name` |
| **Tests for a talent** | `.claude/skills/<name>/evals.md` | `EVALS.template.md` | The loop's TEST step |

`EVALS.template.md` is **self-improving**: it points authors at `pipeline/TEST-AUTHORING-LESSONS.md`
(read before authoring) and carries an EVOLVING CHECKLIST that `library-curator` keeps current
from those lessons — so the accumulated "what makes a clever, fair test" wisdom lives in the
template and every new test benefits, without editing the template by hand each time.

Hooks are NOT templated here: our security gate rejects auto-run hooks. If a hook idea is
worth it, reimplement it as a *method* skill (see `agent-blast-radius-guard`).

## The rules every template encodes
1. **Frontmatter is mandatory:** `name` (kebab-case = directory) + `description`. Missing
   `name` means the talent may not load/activate.
2. **Description discipline** (this is what makes it trigger at the *right* time):
   trigger-first ("Use when…"), third person, keyword-rich, concrete triggers, and
   NON-overlapping with existing talents (overlap → mis-trigger). Under the cap pinned in `pipeline/CONSTANTS.md` (1024 — the spec limit we author to; 1536 is a different thing, the host's listing truncation).
3. **Body is method, not prose:** what/why → when to use (+ when NOT) → numbered steps →
   rules. No filler, no dead content, no external network/CLI/hooks unless audited.
4. **General, not project-welded** (CLAUDE.md standing rule): write the method so it works
   in ANY project. Keep this repo's specific paths/names/wiring out of the steps; put them
   in a short trailing **"## In this repo (one instance)"** section as examples. The only
   exception is `/piano` (the app itself).
4. **Deploy after authoring:** run the `talent-deploy` checklist so it activates and is
   wired in — a committed file that nothing routes to never gets used.
