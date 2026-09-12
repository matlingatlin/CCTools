# Skills — cross-cutting

Skills are not a per-layer concern. They help **us** build Scio; they do not belong to a layer
of the product. This document holds all of them, so the layer documents do not each grow a
padded section answering a question that has one answer.

---

## The distinction that is easy to blur

A **Claude Skill** is instructions a coding agent loads. It runs in *our* build process.

The **product's runtime** uses relays and prompts — different mechanism, different lifecycle,
different cost model.

One bridge exists: the Messages API can attach Agent Skills to a container
(`container.skills` alongside code execution). So a skill *could* become a product mechanism.
That is a separate decision with its own cost, not a free consequence of having written one.

Until that decision is made, assume: **skills are for building, not for running.**

---

## How a skill is written

The format is small on purpose. One file, `SKILL.md`, YAML frontmatter then Markdown.

**Two required fields.** `name` and `description`. Everything else is optional and
spec-compliant runtimes ignore keys they do not recognise.

- `name` — lowercase, digits and hyphens, ≤64 chars, **must match the folder name exactly** or
  it will not load.
- `description` — ≤1,024 chars, and it is the load-bearing field. It decides *when* the agent
  loads the skill, so it must say what the skill does **and when to use it**, in words a person
  would actually type.

**No angle brackets anywhere in the frontmatter** — they can inject into the system prompt.

A description that says only what a skill does will never fire. `graph-guard`'s says *"Use
after committing code, when setting up the post-commit hook, when a cross-layer dependency
needs checking, or when the architecture map has gone stale"* — those are the sentences a
person types.

---

## Ours today

**Sixteen exist.** Five documents previously gave four different counts; this table is the one to
trust, and it is dated.

| Skill | Does | State |
|---|---|---|
| `as-built` | routes questions about hello-world to the right document; forbids opening the old repo | in use, blind-tested |
| `graph-guard` | keeps the code graph current after a commit and catches layer-boundary drift | written, not yet exercised — no code in this repo |
| `graphify` | vendored upstream, turns a corpus into a queryable graph | vendored; **drifts from the installed package**, and its frontmatter was corrected locally so it can fire from context at all |
| `app-design` | the token contract, the design gate, and the defaults that make generated apps recognisable | written; §1–§4 proposed as playbook content (**B-7**) |
| `brainstorm` | the ideation procedure — parallel independent generation, existence check before an idea is written | new, unexercised |
| `architecture` | the pattern catalogue with a disqualified-when column, plus the selection procedure | new, unexercised |
| `testing` | how to tell a green run from evidence; built from this repo's three real cases of tests passing for the wrong reason | new, unexercised |
| `ais-grounding` · `change-impact-analysis` · `contract-retrieval` · `design-rule-hierarchy` · `ears-requirements` · `ontoagent-elicitation` · `reflexion-conformance` · `req-elicit-gym` · `reuse-classification` | the research skills, one per adopted paper | written |

**None of the sixteen has an `evals/` directory.** `claude plugin eval` exists and its default
ablation runs a no-plugin baseline arm and reports the delta — which is the fourth part of the
contract below, and the part we have never actually been able to measure. See
`docs/TOOLING-SCAN.md` §3.2.

**The drift is a standing hazard, not a one-off.** The vendored `graphify/SKILL.md` calls
`check_semantic_cache` expecting three return values; the installed 0.9.50 returns four. Pin
the package version and re-fetch the vendored file deliberately.

---

## Proposed

### For the build process

| Skill | Why it earns its place |
|---|---|
| `intake-replay` | runs Layer A's replay harness and reports the five metrics, so measuring is one command instead of a procedure. **Blocked on the harness existing** |
| `layer-audit` | given a layer, re-runs the as-built seven headings against current code and reports what changed. Keeps `docs/as-built/` from going stale the way `STRATEGY.md` did |
| `adr-propose` | drafts an ADR from a decision under discussion, in the repo's format, with status `Proposed`. Cheap, and it is what `CLAUDE.md` already demands |

`layer-audit` is the one that pays for itself. Every stale claim we found — `STRATEGY.md`
saying the intake agent was not built, `DATA-MODEL.md` predating five migrations, `COSTS.md`
describing a system that shipped — existed because nothing re-checked documents against code.

### Research skills

**Every paper we actually adopt becomes a skill.** Not every paper we read — only the ones a
design decision rests on. A skill for a paper nobody used is inventory, not knowledge.

Each carries four things:

1. **Source** — title, authors, link, date. Who did this and where it is published.
2. **Method** — how it works, in the form *we* use it, not a summary of the abstract.
3. **Limits** — what the paper actually shows, versus what we are assuming. This section is
   mandatory and it is the one that makes the skill trustworthy.
4. **Eval** — runnable cases with expected outcomes, so the skill can be measured rather than
   believed. `skill-creator` supports evals and variance analysis.

**The honesty rule: a skill may not claim more than its paper shows.** OntoAgent reports +33%
on implicit requirements elicitation — measured on website applications, in their setup, against
their baselines. Not on us. A skill that repeats "+33%" without that sentence is selling a
number it did not earn.

Candidates, in the order the layer documents will need them:

| Paper | For | Status |
|---|---|---|
| OntoAgent — *From Chat to Interview* | Layer A, app-kind detection and question prioritisation | abstract-to-method; not reproduced |
| LLMREI | Layer A, the interviewer-error metric | abstract only — **read in full before writing the skill** |
| ClarifySTL | Layer A, why vague clarification questions backfire | abstract only |
| DSPy — Stanford NLP, MIT licence | optimising elicitation once a metric exists | deferred by design, not by oversight |
| Hierarchical summarisation | the method behind `docs/as-built/` itself | already used; skill would document what we did |

---

## The bigger idea, noted and parked

If research reliably converts into tested, sourced, evaluated skills, then the pipeline itself
is a product: a place where people find skills that carry their provenance and their limits,
rather than a directory of unsourced markdown.

The existing marketplaces are large and unfiltered — one lists 23,600 Claude Code skills,
another claims 2 million scraped from public repos. Volume is not the gap. **Provenance and
evals are the gap**, and that is exactly what the four-part format above produces as a
by-product of using it honestly.

Parked deliberately. It is a second product, and Scio is not finished.

---

## When a skill is the wrong tool

- **A one-off task.** A skill is for something repeated. Writing one for a single job costs
  more than doing the job.
- **Anything needing a runtime.** Skills are instructions. A thing that must execute is a
  script, an MCP server, or product code.
- **Encoding a decision that belongs in an ADR.** A skill describing *how* we do something is
  fine; a skill that quietly decides *what* we do is an architecture decision hiding in a
  markdown file.
