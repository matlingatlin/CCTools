# Operating model — three repos, the skills that span them, and the run document

**Status: proposed, nothing decided.** Sequenced after `docs/next/` is complete for all seven
layers and the repo has been reviewed as a whole. Written now so the shape is not lost, and so the
open questions are visible before anyone starts answering them by accident.

---

## 1 · The three repos

| Repo | Holds | Written by | Read by |
|---|---|---|---|
| `hello-world` | the predecessor application, ~23,000 lines | **nobody — frozen** | nothing, directly |
| `scio` | knowledge: `as-built/`, `next/`, `decisions/`, the graph, the skills | us, in planning | the build repo, every session |
| *(new)* | the application being built, plus the skills that application uses | the build sessions | users |

The split is right, and the reason is sharper than "organisation": **the three have different
lifecycles.** `hello-world` never changes again. `scio` changes when we learn something. The build
repo changes every commit. Mixing any two of those means the fastest-moving one drags the others'
history with it.

`hello-world` is already handled — `docs/as-built/` exists so nothing has to open it, and the
`as-built` skill forbids cloning it. **That contract must survive the split unchanged**, or the
build repo will start reaching backwards.

### The unanswered question: how does the build repo read `scio`?

Four mechanisms exist and they are not equivalent. This is a decision, not a preference:

- **Claude Code plugins** — the mechanism purpose-built for distributing skills, commands, agents
  and MCP config across repos from a marketplace. If this does what it appears to, most of the
  question is already answered and we should not invent a second way.
- **Git submodule** — simple, versioned, and every developer's least favourite thing.
- **An MCP server** in front of the graph — turns `scio` into a queryable service rather than files
  on disk. Right if the graph is the main thing being read; overweight if it is the skills.
- **Clone-on-demand** — what this session does today.

**Scan before choosing.** Same rule as everywhere else in this project: the answer probably exists
and is documented, and we have already been burned twice writing something a standard covered.

### The hazard we have already met once

`SKILLS.md` records it: the vendored `graphify/SKILL.md` calls `check_semantic_cache` expecting
three return values; the installed 0.9.50 returns four. **A skill drifted from the thing it
describes.** Splitting the skills across two repos multiplies that surface. Whatever mechanism wins
above has to carry a version pin and something that fails loudly when the pin is stale — a skill
that is quietly wrong is worse than no skill, because it is trusted.

---

## 2 · The skills roster

Requested: architect, database, brainstormer, tester, test-builder, a graphify-backed check on
skill quality, and **a skill that writes new skills from research findings**.

Three things to get right before writing any of them.

### 2.1 A skill is a decision procedure, not a persona

"An architect skill" can mean two very different files. One says *think like an architect* — that
is a prompt, it will not survive contact with a real decision, and it is inventory. The other says
*here is the list of architecture patterns, here is how you choose among them for this class of
problem, here is what disqualifies each, and here are the cases that prove it* — that is a skill.

The user's own standing rule is already the test: **when a domain word appears, go to the list of
what exists in that domain and search before proposing.** A skill earns its place when it *is* that
list plus the procedure for using it. If it does not contain the list, it is a personality.

### 2.2 The skill that writes skills already partly exists

`skill-creator` exists in the Claude ecosystem and supports evals and variance analysis. **Do not
rebuild it.** What is ours is the contract it must produce, already written in `docs/next/SKILLS.md`
and non-negotiable:

1. **Source** — title, authors, link, date.
2. **Method** — how it works in the form *we* use it, not an abstract summary.
3. **Limits** — what the source actually shows versus what we are assuming. Mandatory.
4. **Eval** — runnable cases with expected outcomes.

Plus the honesty rule: **a skill may not claim more than its source shows.** OntoAgent's +33% was
measured on website applications, in their setup, against their baselines — not on us.

So the thing to build is thinner than it sounds: a **wrapper** that takes an online scan and emits
a skill in that four-part shape, refusing to emit one when §3 is empty. The refusal is the feature.

### 2.3 Graphify checks format; it cannot check truth

A graph over the skills corpus will find drift, duplication, orphans and inconsistent shape — real
value, and cheap. It will not tell you whether a skill's claim about a paper is accurate. Keep the
two apart in the design or the check will be believed for something it does not do.

### Candidate roster, with the honest verdict on each

| Skill | Verdict |
|---|---|
| `skill-writer` (wraps `skill-creator` + the four-part contract) | **strongest candidate** — it is what makes every other one trustworthy |
| `architecture-patterns` | earns it *only* as the list + selection procedure, per §2.1 |
| `data-model` | earns it — schema, migrations and tenancy are where the predecessor's worst defect lives |
| `test-design` | earns it, and it has a specific job: the predecessor has **two confirmed cases of tests passing for the wrong reason**. A skill that catches doubles stricter than production is worth more than one that writes tests |
| `graph-guard` | already written, not yet exercised |
| `app-design` | already written and scanned |
| `brainstormer` | **weakest** — this is a prompt, not a procedure, unless it carries an actual method. Park it until it has one |

Seven is already a lot. Every one of them costs maintenance and can drift.

---

## 3 · The run document

The ask: point a fresh Claude Code project at `scio`, say *run*, and it comes up with the graph,
the predecessor knowledge, the forward view, and the skills — then takes a vision from
conversation to a professional application.

**The first question is what it is, not what it says.** A markdown document a human pastes, a slash
command, or a plugin that installs skills, commands and MCP config in one move. The third is the
shape the ask actually describes, and it is the mechanism that already exists. Same rule: scan
first.

**The second question is what it must not do.** A bootstrap that loads seven layer documents, seven
as-built documents and thirteen skills into context has spent the context window before the user
has said anything. `as-built/SKILL.md` already solved this once — *load in this order, and stop when
the question is answered* — and the run document has to be built on the same principle or it will
be the most expensive thing in the system. **Retrieval, not packing.** That is graphify's principle
and it applies here more than anywhere.

---

## 4 · The tension worth naming now

The ask is an **MVP**, and simultaneously that architecture, authentication, design tokens,
component reuse, data collection and security are all considered **from the beginning**.

Those are compatible, but only under one reading, and it is worth stating the difference before
work starts:

- **Thinking about all of it from the start — right.** Every one of these is cheap to design in and
  brutally expensive to retrofit. The predecessor's tenancy breach is exactly a thing that was not
  thought about early.
- **Building all of it before an MVP — the failure we have already documented.** The predecessor is
  ~23,000 lines with a component library whose matchable catalog is effectively one entry, nine
  validation rules nobody reads, two gates that are opt-in *and* have nothing to check, and **five
  placeholder routes including the one carrying Level 1's entire value proposition.** It was not
  built carelessly. It was built broadly.

The reviews said it in one line and it should govern the build order: *"The library is an
amplifier, not the precondition for proving the core. The core loop must work well even when
everything has to be generated."*

So the working form of the instruction: **design for all of it, sequence one thing at a time, and
let the ADR record what was deliberately deferred** — so a deferral stays a decision instead of
decaying into an oversight.

---

## 5 · What is already covered, so we do not write it twice

- **Data collection and instrumentation** — every `docs/next/LAYER-*.md` carries a *Data worth
  owning* section. It does not need a new home.
- **Token economy** — same, one section per layer, measured against real prompts.
- **Design** — `.claude/skills/app-design` plus the ongoing motion scan in `docs/brand/`.
- **Authentication and tenancy** — `docs/next/LAYER-G-CROSS-CUTTING.md`.

---

*Written 2026-08-26. Proposals only. Per `CLAUDE.md`: propose, do not assume — every item above
becomes an ADR before it becomes a fact.*
