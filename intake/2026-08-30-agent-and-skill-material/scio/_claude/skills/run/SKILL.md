---
name: run
layer: build-process
phase: build-time
status: written
description: Bootstrap a Scio build session, and answer anything about this corpus by querying it rather than opening files. Use when someone says run, start the project, set up the new repo, or begin the build - and whenever you are about to read a document to find a fact, because scripts/scio-db.py find and read return the one section instead, at a sixteenth the size. Establishes the three repos and which is writable, the store that holds findings, skills and content, the order of work - brainstorm and architect each layer before building it - and the rule for deciding what to keep, adjust, replace or build new from the predecessor. Read this before proposing anything.
---

# run

You are starting work on **Scio** — an AI app builder. Someone who cannot write software describes
what they want and gets an application they own.

Read this file to the end before opening anything else. It is short on purpose.

---

## 1 · Three repos. Know which one you are in.

| Repo | What it is | Your access |
|---|---|---|
| `hello-world` | the working predecessor, ~23,000 lines. It works; it is not assumed correct | **read-only, and normally never opened** |
| `scio` | the knowledge: what the predecessor is, the forward view per layer, the skills, the code graph | **read.** Write here only when recording a decision or updating knowledge |
| the build repo | where the new application is written | **write here** |

**Do not clone or open `hello-world`.** `docs/as-built/` was written so this repo is sufficient on
its own. If you believe you need the old source, say why first — the answer is almost always
already written down, and re-deriving it costs hours.

**Where a skill lives follows one test:** does it run while Scio is being *built*, or while a
generated app is *running*? Build-time → `scio`. Runtime → the build repo.

---

## 2 · Load by retrieval, not by packing

There are 40+ documents and 27 skills here — roughly **1.9 million characters**. Loading even a
handful spends the context window before the user has said anything, and it is the single most
expensive mistake available in this session.

**Do not open a file to find out what is in it. Query the store.**

### The store answers three different questions

`scio.db` is built by the `SessionStart` hook and rebuilt with `scripts/scio-db.py build`. It holds
the corpus three ways, because a question needs one of three things and rarely all three:

```bash
scripts/scio-db.py find "plateau"        # content — which section says this, and what it costs
scripts/scio-db.py read "when does it stop"   # that section, and nothing else
scripts/scio-db.py layers                # 249 findings by layer and verdict
scripts/scio-db.py skill gate-verdicts   # which findings a skill rests on, traced to source line
scripts/scio-db.py adrs                  # decisions triaged and still unwritten
scripts/scio-db.py sql "SELECT …"        # anything else; the schema is in the script's docstring
```

**Measured, not asserted.** The average section is **1,274 characters** against an average file of
**20,397** — sixteen times smaller. Asked *when does the build loop stop*, `read` returns **348
tokens** where opening the file costs **3,153**, and the answer is complete in itself. `read` prints
that fraction every time, so the saving stays visible.

### Then, and only for what the store cannot answer

1. **`scripts/scio-db.py find`** — start here for anything factual.
2. `docs/as-built/00-INDEX.md` — the macro map, when you need orientation rather than a fact.
3. `docs/as-built/01-DECISIONS.md` — for *why* something is shaped as it is. Check before calling
   any design odd; several oddities are reasoned.
4. **One** `docs/as-built/LAYER-*.md` or `docs/next/LAYER-*.md` — only when you need a whole layer's
   argument, not a fact from it. They are 20–70 KB each.
5. **The code graph**, for symbol-level lookups over the predecessor. Query it; never read old
   source:
   ```bash
   graphify explain "is_buildable" --graph docs/as-built/graph/graph.json
   graphify query "what does the intake gate check" --graph <path> --budget 600
   graphify affected "is_buildable" --graph <path>     # what breaks if this changes
   ```
   Measured on this graph: **26× fewer tokens per query** than the naive corpus, by the tool's own
   `benchmark`. `--budget` caps the answer and says how many nodes it cut.

   **The graph stops at the language boundary, and this is not a small caveat.** Counted
   2026-08-26: **9,857 edges within a language, zero between Python and TypeScript.** The
   predecessor is a Python engine plus a TypeScript API and app that talk through serialised DTOs,
   so the graph is blind to precisely the seam where integration defects live. Measured against a
   real commit, an impact query predicted **2 of the 8 files that actually changed** — the rest
   propagated across that boundary. Use the graph for structure *within* a language; for anything
   crossing the seam, read the DTO and follow it by hand.

**The failure this prevents is specific and has happened here.** An ablation on 2026-08-26 had an
agent answer a question wrongly because two documents disagreed and it resolved the conflict from
the graph — which counts call edges, not rule identifiers. **When two sources disagree, go to the
code.** A retrieval budget is not an accuracy budget.

The `as-built` skill routes a question to the right document. Use it rather than guessing.

---

## 3 · The order of work

Two passes happen **once, over the whole system**. Then a loop runs **once per layer**. Nothing is
written into the build repo before step 2 is recorded as an ADR.

### Once, before any layer

**Step 0 · Brainstorm — once, not per layer.** Invoke `brainstorm`. It is a procedure, not an
invitation to free-associate: it forces independent generation before any sharing, and checks every
idea against what already exists in its domain *before* the idea is written down. Feed it from the
store, not from open files:

```bash
scripts/scio-db.py layers                    # what is already found, per layer
scripts/scio-db.py sql "SELECT layer,row_no,text FROM finding WHERE verdict='ADR'"
```

**249 findings are already triaged and 73 are decisions nobody has taken.** Brainstorming past them
without reading them produces a 250th.

**Step 1 · Architecture, the whole shape.** Invoke `architecture`. This pass decides what nothing
downstream may re-open: the stack, the shape, and **the layer count**.

The predecessor has seven — intake · understanding · build plan · component library · build &
execution · design window · cross-cutting. **That is a description of what exists, not a
specification of what to build.** Six may be better; ten may be better; the forward documents argue
at least one seam sits in the wrong place. Do not inherit seven by default, and do not change it
casually: each is an ADR with its reason.

Output: ADRs in `docs/decisions/`. **Until they exist, step 2 has nothing to build against.**

### Then, once per layer

**Step 2 · Read the predecessor for this layer — and decide part by part.** Every
`docs/as-built/LAYER-*.md` has a **State** heading carrying one of five verdicts, already assigned
across the whole system. That is the keep-or-rebuild rule and it was written before anyone asked
for one. **Do not invent a second one.**

| Verdict | What you do |
|---|---|
| **Solid** | carry forward unchanged. Rebuilding loses work and reintroduces closed bugs |
| **Deliberate, easy to break by accident** | carry forward. Changing it means arguing against a stated reason, in an ADR |
| **Wrong-shaped** | it works, but its form is wrong for the job. Rewrite; keep the behaviour |
| **Missing** | build it |
| **Obsolete** | do not carry it |

Where you override a verdict, record why. An override that is not written down becomes an accident
in six weeks.

**Step 3 · Architecture again — this layer, before any code.** Invoke `architecture` a second time.
Step 1 fixed the system's shape; this fixes *this layer's* internal design against it, now that
step 2 has told you what is being carried forward and what is being written fresh. **These are
different questions and the second cannot be answered before the first two.**

Both architecture passes go through the skill, never from memory. Its *disqualified-when* column is
the point: elimination is cheaper than comparison.

**Step 4 · Build.** Now, and not before. Use the layer's own skills — query rather than guess which:

```bash
scripts/scio-db.py sql "SELECT name FROM skill WHERE layer LIKE '%E%'"
scripts/scio-db.py skill gate-verdicts       # what a skill rests on, traced to source
```

`playbook-admission` before anything enters the Playbook. `app-design` for anything a user sees.

**Step 5 · Test, and treat green as a claim.** Invoke `testing`. This system has **three confirmed
cases of tests passing for the wrong reason**, and its own rule: *red is evidence; green is
`unjudged` until the test is shown to be capable of failing.* `gate-verdicts` decides what a gate
may conclude; `build-loop-stops` decides when to stop trying.

**Step 6 · Record and commit.** ADRs for what was decided, `/checkpoint` for the rest. The graph and
the store refresh themselves — the commit pays 222 ms and no model call.

### What must not happen

- **Building before step 1's ADRs exist.** That is how the predecessor became 23,000 lines with five
  placeholder routes: built broadly rather than carelessly.
- **A second brainstorm per layer.** Step 0 happens once. A layer that needs new ideas mid-build has
  found a step 1 decision that was wrong — reopen the ADR, do not improvise.
- **Skipping step 3 because step 1 felt sufficient.** The whole shape does not settle a layer's
  internals, and code written without step 3 is where the shape quietly stops being true.

---

## 4 · The rules that make the work trustworthy

These do not travel in a `CLAUDE.md` — a plugin cannot ship one — so they are here.

**Position before history.** Write your own position on a problem *cold*, before reading the old
code or the reviews. A position written afterwards is a critique of what exists, not an independent
answer, and later nobody can tell the two apart. Mark a late position `informed` and weigh it less.

**Scan before building.** Every step checks what exists now — tools, skills, MCP servers, repos,
papers, what practitioners report. When a domain word appears — architecture, database,
authentication, design, testing, code — go to the list of what exists in that domain and search
before proposing. **This project has invented something a standard already covered twice**, and
both times the standard was one search away.

**Never answer from memory** about a tool, a model, a price or a version. Look it up and date it.

**Verify before acting.** A claim that will drive work is checked at primary source: `file:line`
for code, the paper itself for a finding, the repo's own `LICENSE` for a licence. Findings are
claims, not facts. Numbers in these documents have been wrong before and were corrected only
because someone counted.

**Four allowed outcomes** for any question: **build · complete · keep · park.** *Keep* — deciding
the existing design is wiser than the new idea — is a real outcome, and it must be written down
with its reason so the question does not come back.

**Budget before parallel work.** Say what a step may cost before dispatching agents. Deterministic
passes first, model passes last and in small batches, **writing partial results to disk** so an
interruption costs one batch rather than the run.

---

## 5 · Nothing is decided yet

`docs/next/LAYER-*.md` §9 carries roughly **85 numbered proposals**. They are proposals. A proposal
becomes a decision when it lands in `docs/decisions/` as a numbered ADR with a status — not when a
document argues for it well.

The stack for the new build is **open**. The predecessor's choices are evidence, not inheritance.

**Propose; do not decide silently.**

---

## 6 · Before you finish

Definition of done: built + tested + documented + committed. `/checkpoint` documents, changelogs
and commits everything outstanding. Never leave work in a session.
