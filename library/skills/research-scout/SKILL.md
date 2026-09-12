---
name: research-scout
description: Use when a research effort needs fuel — deriving what to search for and where to look next for any topic or goal. Generates ranked search terms, sources, and entities (people, companies, institutes, universities, communities) for a subject and records them to a research queue or backlog. The query engine that keeps any harvesting, literature review, competitive scan, or discovery loop fed.
disable-model-invocation: true
---

# research-scout — the query engine

Given a research goal (a topic, question, or an existing body of knowledge), produce
the next batch of **search terms**, **sources**, and **entities** to investigate, and
record them wherever the project tracks its research frontier (a queue file, a backlog,
an issue list, or a plain note). This is the producer that keeps any downstream
consumer — a harvester, a reviewer, or yourself — supplied with concrete leads
(producer→consumer cadence).

## Domain scope
Scope is defined by the research goal, not by this skill. Before generating terms,
fix the scope explicitly:
- **Core (default, always):** the domains the goal directly names or requires.
- **Bonus / connected (only when it plausibly serves the goal):** adjacent fields that
  can surface non-obvious leads. Include an adjacent term only when you can name why it
  connects to the goal.

State the core and bonus domains once at the top of a run so the batch stays on-target.

## Steps

1. **Set the frontier — and read back what the last loop learned.** Two inputs, both mandatory.

   **(a) The seen set is a UNION, under a canonical key.** Most projects keep "already seen"
   in several disjoint places — a seen list, a done list, the queue of things not yet
   consumed, what a previous run already emitted, and the catalog of what was ingested. A
   source absent from one and present in another is still seen. Take the union of all of
   them, and normalize every entry to a **canonical key** before comparing (for repos:
   `host:owner/name`, lowercased, with renames and known aliases resolved to one identity).
   Without a canonical key the same source re-enters under a second spelling and nothing
   catches it. A suspected duplicate is resolved HERE and dropped; never queue it with a note
   asking the consumer to dedup it — that hands your own gate downstream, where it is cheaper
   to skip than to run.

   **(b) Read the loop's own lessons before generating anything.** If the project records
   what its past passes learned — yield per source type, active directives, verdicts like
   *seek-more* or *deprioritize* — read that FIRST and let it constrain this batch. A source
   type carrying a *deprioritize* verdict is not re-emitted unless you state why this instance
   is different. This step is what makes the loop self-improving rather than merely repeating;
   skipping it is invisible, because a batch generated without the lessons looks exactly like
   one generated with them.
2. **Search terms.** For each core domain, generate 3–6 terms of three kinds:
   (a) academic/technical (precise field vocabulary, method names),
   (b) practitioner/"top-N" ("best X frameworks 2026", "top X tools"),
   (c) failure/symptom ("why X breaks", "X pitfalls", "X limits"). Add bonus-area terms
   only when they connect to the goal.
3. **Sources, ranked.** For each term, name where to look, best-first:
   primary (original papers/preprints, official docs, source repos, standards, filings) >
   reputable labs/companies/institutions > known practitioner profiles >
   secondary commentary/blogs. Open access only; no paywalled/pirated content.

   **A curated list is not a source — it is an INDEX, and it never enters the queue itself.**
   "Awesome-X", top-N roundups, and link collections are read only to extract the concrete
   paths they point at; each of those is then deduped and judged on its own. Queueing the list
   hands the consumer a hop instead of a lead, and the list's own top ranks are reliably the
   sources you already hold — prominence and your prior search agree on what is prominent.
4. **Entities.** List people / companies / institutes / universities / communities worth
   tracking, each with a **credibility tier** (primary / reputable / community) and a
   one-line why.
5. **Dedup + write, and record the COUNT you handed on.** Drop anything already seen (step 1's
   union, canonical key). Record the search terms, entities, and the concrete source URLs/repos
   to wherever the project keeps them (queue, backlog, notes, or issues), and update the "seen"
   record. Keep the storage location a project choice — this skill just defines what to write,
   not one fixed file. Then write down **how many candidates this pass emitted**, in whatever
   the project measures passes with. That number is this pass's output; see the Rules.
6. **Declare the scope you searched, and prove a hit before reporting none.** Name which
   places you actually looked in. Before reporting "nothing new", run a **positive control**:
   query for something you KNOW is present and confirm it comes back. A search that returns
   nothing is indistinguishable from a search that looked in the wrong place, and only the
   control tells them apart. Distinguish the two conclusions explicitly in what you report:
   *"this channel is exhausted"* (drop rate approaching 100% on a channel you proved you can
   search) is a reason to change channel; *"the frontier is exhausted"* is a much larger claim
   and needs more than one channel's silence behind it.

7. **Self-improve.** After the consumer returns findings, re-run with those findings as
   input so the next batch of terms is sharper (feedback loop), and write back what this pass
   learned about which source shapes paid — that is the record step 1(b) reads next time.

## Rules
- Prefer recency (last ~12 months) and primary sources; flag single-source claims.
- Never emit a source that violates ToS/paywall; store distilled notes + citation, not
  wholesale copyrighted content.
- Keep batches bounded (one wave-worth), so the consumer always has something to work on
  but the queue doesn't explode.
- **This method is a PRODUCER and is measured on the candidates it emitted — never on what a
  later consumer eventually kept.** Adoption happens in a downstream pass, often much later,
  so scoring a scouting pass by adoptions reads as zero for work that was excellent, and an
  automated rule will then deprioritize the engine that feeds the whole loop. Record
  `candidates` on every pass. If a computed verdict about this method's yield contradicts what
  the passes plainly produced, suspect the measurement before obeying it.

## Hand-off and boundaries
This method produces leads and hands them to a consumer — a harvester, a reviewer, a build
pass — which is a different job with a different measure (see the Rules). Neighbours it is
easy to confuse it with: `market-research` answers a market/competitive question and ends in a
finding, not a queue; `literature-review` reads a body of work and synthesises it with
citations; `skill-scout` searches an existing local library for prior art rather than the
outside world for new leads.

## In this repo (one instance)
As one concrete instance, a talent-discovery pipeline uses this method to keep a harvester
fed: core domains are AI/ML/LLMs, agents & orchestration, software engineering, data,
IT/infra, developer tooling, NLP, prompt engineering; bonus domains (psychology, cognition,
linguistics, design, decision science) count only when they plausibly yield a talent.
There, "record to the frontier" means appending terms to a `catalog/` search-terms file,
entities to an entities file, and pushing source URLs to the harvester queue in a
`pipeline/frontier.json` track, then updating its `seen` set. The seen UNION here is
`frontier.json` tracks' `seen` + `done_sources` + `queue_sources` + what earlier passes already
emitted + `catalog/catalog.json`; five disjoint registers, so step 1(a)'s canonical key is not
optional. Step 1(b) reads `pipeline/LESSONS.md` — its ACTIVE DIRECTIVES and the source-yield
table — and honours the verdicts there; `pipeline/ROUTING.md` records that this hand-off is
expected in both directions. Step 5's count is the `candidates` field on this wave's
`pipeline/metrics.jsonl` row. Those paths are examples of step 5's "wherever the project tracks
its frontier", not a requirement of the method.
