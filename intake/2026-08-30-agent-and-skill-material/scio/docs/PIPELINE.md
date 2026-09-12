# The pipeline — from vision to a built application

**Status: proposed.** This records the stage chain, what each stage consumes and produces, and
where each artifact lives. Nothing here is decided; per `CLAUDE.md`, each stage becomes real only
when it has an ADR and a skill with an eval.

Read `OPERATING-MODEL.md` first — it holds the three-repo split and the open question of how the
build repo reads this one.

---

## The chain

| # | Stage | Consumes | Produces | Exists? |
|---|---|---|---|---|
| 0 | **Tooling** | online research + `graphify/SKILL.md` as the format bar | `brainstorm`, `architecture`, `testing`, `skill-writer` skills | 3 in progress |
| 1 | **Brainstorm** | `docs/next/` + the code graph, via retrieval | scored idea set, one shape per idea | skill in progress |
| 2 | **Validate** | the idea set | a *smaller* idea set, with reasons for every rejection | **not started** |
| 3 | **Architect** | validated ideas + settled ADRs | the architecture, plus the ADRs that record it | skill in progress |
| 4 | **Plan** | the architecture | build order, layer by layer | **not started** |
| 5 | **Code** | plan + contracts + skills | the application, in the new repo | **blocked — see §3** |
| 6 | **Test** | the code | evidence, not green ticks | skill in progress |
| 7 | **Review** | everything | contradictions and drift | running now |

Stage 0 is not preamble. Every later stage is only as good as the skill that drives it, and a skill
without an eval is an opinion in a markdown file.

---

## 1 · Where each artifact lives

The rule, stated as a test rather than a category:

> **Does this run while Scio is being built, or while a generated app is running?**
> Build-time → `scio`. Runtime → the application repo.

| Thing | Repo | Why |
|---|---|---|
| `brainstorm`, `architecture`, `testing`, `as-built`, `graph-guard` | `scio` | they run in our sessions |
| `app-design` | **both, and this is the awkward one** | §1–§4 are meant to become playbook content the product ships; §5 is a build gate we run |
| the code graph | `scio` | it describes the predecessor |
| ADRs about Scio's own architecture | `scio` | |
| ADRs about a generated app's architecture | the application repo | |
| the application | the application repo | |

`app-design` is the case that proves the rule needs care: a skill can have a build-time half and a
runtime half, and splitting it is a decision, not a formality. **Do not resolve this by copying the
file into both repos** — that is the drift hazard `SKILLS.md` already records, deliberately created.

---

## 2 · The problem the chain has, and it is not a small one

Every stage in this chain **adds**. Brainstorm adds ideas. Architecture adds structure. Only stage 2
subtracts, and it was described as *"not strict — let good ideas through"*.

`docs/next/` is already ~6,000 lines carrying roughly **90 ADR proposals**. If brainstorm adds to
that and validation filters gently, stage 3 receives an input no architect — human or otherwise —
can hold in mind at once. The result is not a bad architecture. The result is an architecture that
quietly ignores most of its input, which is worse, because nobody can tell which parts were
considered and rejected versus never read.

**So validation needs a number, not a mood.** Not "be strict" and not "let good ideas through", but
a stated output budget: *stage 3 receives at most N proposals per layer, ranked, with every
rejection carrying its reason.* Then a rejected idea is recoverable and an ignored one is
impossible. The number is a decision to make deliberately; picking it is cheap, discovering you
needed it after stage 3 is not.

This is the same failure the predecessor already has, one level up. It computed nine validation
rules and read none of them. A pipeline that generates ideas and reads a fraction of them is that
bug in process form.

---

## 3 · What cannot be decided yet, and why saying so is the right answer

**Which languages the coding agents cover.** The stack for the new build is stage 3's *output*.
Naming languages now — one agent per language, or one agent with several — would be deciding the
architecture in the staffing plan, before the architect has run.

`hello-world` is Python and TypeScript, and ADR-0011 fixes the *generated* app's stack. Neither
settles what Scio itself is written in next. It is genuinely open, and the honest move is to leave
it open until stage 3, then let the ADR record it.

---

## 4 · What "copy the good parts" means — and it is already defined

The instinct is right: where the predecessor is good, take it; elsewhere rewrite. But "good" needs
a rule, and **one already exists.** Every `docs/as-built/LAYER-*.md` has heading 6, *State*, with
five verdicts already assigned across all seven layers:

| Verdict | What stage 5 does with it |
|---|---|
| **Solid** | carry forward unchanged — rebuilding loses work and reintroduces closed bugs |
| **Deliberate, easy to break by accident** | carry forward, and changing it requires arguing against a stated reason in an ADR |
| **Wrong-shaped** | it works, but its form is wrong for the job — rewrite, keep the behaviour |
| **Missing** | build it |
| **Obsolete** | do not carry it |

That is the copy rule, written before anyone asked for one. **Do not invent a second one.** The
work at stage 5 is to follow it and to record where it was overridden.

---

## 5 · The run document

The intended end state: point a fresh session at `scio`, say *run*, and it comes up knowing the
predecessor, the forward view, the graph and the skills — then takes a vision from conversation to
a built application.

Two things decide whether that works.

**What it is.** A markdown file a human pastes, a slash command, or a plugin that installs skills,
commands and MCP config in one move. The third is the shape the intent actually describes and the
mechanism that already exists. Scan before choosing — the same rule that has already caught us
twice.

**What it must not do.** A bootstrap that loads seven as-built documents, seven forward documents
and fifteen skills has spent the context window before the user has said a word.
`.claude/skills/as-built/SKILL.md` already solved this: *load in this order, and stop when the
question is answered.* The run document inherits that discipline or it becomes the most expensive
thing in the system.

Written after stage 7 reports, because a bootstrap that points at contradictory documents
propagates the contradictions into every session that runs it.

---

*Written 2026-08-26. Proposals only.*
