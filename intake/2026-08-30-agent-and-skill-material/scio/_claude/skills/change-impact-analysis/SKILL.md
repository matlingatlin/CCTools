---
name: change-impact-analysis
layer: C, F
phase: build-time
status: written
description: Compute which requirements, architecture nodes, packages, files and tests a proposed change affects, before any code is written, and govern what a regeneration is then allowed to overwrite. Use when designing or reviewing impact analysis, blast radius, affected-set or "what does this change touch" logic; when scoping a surgical edit; when deciding how far a dependency walk should go; when writing a plan delta or deciding which existing work survives one; or when someone proposes inventing an impact algorithm. Also use when checking that a finished diff stayed inside the set that was predicted for it. Carries the field's real results — Arnold and Bohner, Chianti, CodePlan, ProReFiCIA — and the over-approximation failure that sinks naive versions.
---

# change-impact-analysis

Change impact analysis (CIA) is a forty-year-old field with published numbers. **Do not invent an
algorithm for it.** This skill carries what the literature establishes, in the form Scio uses it,
and the limits of each claim.

The one-line version: **a naive forward closure over a dependency graph returns roughly a third of
the system, which is useless. Everything worth knowing in this field is about how to make the
answer small without making it wrong.**

---

## 1 · Source

| Work | Who / where | What it establishes |
|---|---|---|
| *Software Change Impact Analysis* | Robert Arnold & Shawn Bohner, first framed 1993, IEEE CS Press book 1996 | Founds the field. Splits CIA into **dependency analysis** (edges in the artifact graph) and **traceability analysis** (links between requirements, design and code). Bohner (2002) names three change activities: understand, implement, retest |
| *A Review of Software Change Impact Analysis* | Steffen Lehnert, 2011, TU Ilmenau — [PDF](https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00024546/ilm1-2011200618.pdf) | Classifies **150 approaches published 1991–2011** against a taxonomy built on Arnold & Bohner, Mens & Buckley, and Kilpinen |
| *Chianti: A Tool for Change Impact Analysis of Java Programs* | Xiaoxia Ren, Fenil Shah, Frank Tip, Barbara Ryder, Ophelia Chesley — OOPSLA 2004 — [PDF](https://prolangs.cs.vt.edu/refs/docs/oopsla04.pdf) | Decomposes a version difference into **atomic changes**; reports impact as **affected tests**, and for each affected test the **affecting changes** |
| *Program slicing* | Mark Weiser, 1981, plus subsequent surveys | Forward slicing is the CIA primitive. Empirical surveys report **static slices average ~30% of program size**, dynamic ~20% |
| *CodePlan: Repository-level Coding using LLMs and Planning* | Bairi, Sonwane, Kanade, Vageesh, Iyer, Parthasarathy, Rajamani, Ashok, Shet — Microsoft Research — [arXiv 2309.12499](https://arxiv.org/abs/2309.12499), PACMSE 2024 | "A novel combination of an incremental dependency analysis, a **change may-impact analysis** and an adaptive planning algorithm" driving LLM edits across repositories |
| *LLM-Driven Cost-Effective Requirements Change Impact Analysis* (ProReFiCIA) | Romina Etezadi, Sallam Abualhaija, Chetan Arora, Lionel Briand — [arXiv 2511.00262](https://arxiv.org/abs/2511.00262), submitted Oct 2025, revised Aug 2026 | CIA at the **requirements** level with an LLM, with recall and review-cost numbers |
| *Predictive Test Selection* | Machalica, Samylkin et al., Meta — [arXiv 1810.05286](https://arxiv.org/pdf/1810.05286) | Learns test selection from historical outcomes rather than deriving it |

---

## 2 · Method, in the form we use it

### 2.1 Both perspectives, not one

Arnold & Bohner's split is the design: Scio needs **dependency analysis** (edges inside the
architecture graph) *and* **traceability analysis** (`source_field` back to the spec field the user
said, and forward to the package and file). Systems that do only the first answer "which code";
only the second answers "which requirement". The product promise needs both.

### 2.2 Tier the answer; never return a flat closure

Because static slices average ~30% of a program, a single unbounded reachability set is not a
usable answer. Return tiers with honest names:

| Tier | Rule | Name in the literature |
|---|---|---|
| **Certain** | nodes whose provenance field is the one edited; the packages owning them | the change set |
| **Likely** | one edge out — relations, operations on a changed entity, screens listing those operations, permissions naming them | **may-impact**, depth 1 |
| **Possible** | transitive closure beyond depth 1; validation rules whose subject is in the set | may-impact, unbounded |

"May-impact" is CodePlan's word and it is the right one: it declares the set an over-approximation
rather than pretending to precision it does not have.

### 2.3 Prune with the three standard knobs

The literature's pruning parameters, all three of which should be explicit and tunable:

1. **dependency type** — which edge kinds are followed
2. **minimum importance** — a weight floor on an edge
3. **maximum depth** — the hop limit

An implementation that hard-codes any of these has hidden its precision/recall trade-off.

### 2.4 The affecting direction is the useful one

Chianti's insight is easy to miss. The affected set is large (52% of tests). The *affecting* set is
tiny (3.95% of atomic changes per affected test). **When a check fails, "which of your changes did
this" is a far more actionable answer than "here is what might break."** Build the reverse index,
not only the forward one.

### 2.5 Measure recall against real diffs, or say you have not

The only honest evaluation is: compute the impact set before the change, run the change, compare
against the diff it actually produced. Report **recall** (did the set contain everything that
changed) and **review burden** (what fraction of the system the set represents). ProReFiCIA reports
both; that pairing is the template.

Until that data exists, the correct label is "may-impact analysis, unmeasured". Not "impact
analysis" without qualification.

### 2.6 Applying the delta — two rules, both about what is *not* touched

Added 2026-08-26 from `docs/mined/PASS2-FOUR-REPOS.md` §1.4 (task-master
`scope-adjustment.js:32-45`, `:201-208`). §2.1–§2.5 compute the affected set. These two govern what
happens to everything *outside* it, which is where a regeneration destroys work.

**Preservation is an allowlist, not a denylist.**

```js
const PRESERVE_STATUSES   = ['done', 'in-progress', 'review', 'cancelled', …]
const REGENERATE_STATUSES = ['pending']
```

Enumerate what may be **regenerated**; everything else is preserved, **including states nobody
anticipated**. A denylist — *"regenerate everything not done"* — silently regenerates every state
added after it was written, and the failure is invisible until someone's in-flight work is gone.

`docs/next/LAYER-C-BUILD-PLAN.md` §3.4's plan delta has exactly this shape and exactly this hazard:
an amended architecture must not discard packages that are built, building, or under review, and
the natural phrasing of that intent is a denylist. **Write the allowlist.** The safe direction is
the one where an unknown value survives.

**A delta that changes nothing returns a distinguishable no-op.**

Not an empty regeneration, and not an empty list. `null` versus `[]` is the whole mechanism, it is
free, and it lets a caller tell *"nothing needed changing"* from *"the delta computation produced
nothing."* Two callers depend on the distinction: the gate that shows the user a plan diff, which
should say *"no change"* rather than render an empty one, and the price, which is zero rather than
unknown.

This is `.claude/skills/validation-evidence` §2.3 applied to a delta, and it generalises: **an
impact set of size zero and a walk that did not run must not be the same value.** Tiering (§2.2)
makes this sharper rather than softer — an empty *Certain* tier beside a populated *Likely* tier is
a meaningful answer, and flattening the tiers loses it.

### 2.7 Every element in the set names why it is in it

*Added 2026-08-26 from `docs/mined/OTHERS-MINED.md` row 52 (karpathy-skills rule 3), triaged as
the acceptance criterion for a directed change. §2.6 governs what happens outside the set; this
governs what may be claimed about the set itself.*

An impact set with no reasons is unreviewable: a person cannot tell an edge that dragged a file
in from a file somebody added because it looked related. So each element carries the reason it
is present — the marking it resolved to, or the named edge that reached it.

The acceptance criterion on the other side of the same rule, from karpathy's rules for agentic
edits: **"every changed line should trace directly to the user's request."** Stated as a check
rather than a slogan, it is two assertions and they are different:

| Direction | Assertion | Fails when |
|---|---|---|
| **forward** | every element of the impact set names its reason | a file is in the set and nobody can say why |
| **backward** | every line in the resulting diff maps to an element of the set | the model improved something nobody asked about |

The backward one is the useful half and it is the one systems skip, because it can only be run
*after* the change — which is exactly the point: the impact set becomes a claim the diff is then
measured against, rather than an estimate nobody revisits. In Scio this is nearly free: the
isolation proof already hashes every tracked file and reports `edited_files` and
`unchanged_files`, so the diff is in hand; what is missing is the mapping back.

**Do not let this collapse into "the change stayed inside the package."** Package ownership is
an allow-list, not a trace. A model given seven files it did not need may rewrite one of them,
and a file-ownership check accepts that as inside the boundary.

---

## 3 · Limits — what the papers show versus what we would be assuming

**Read this section before quoting any number above.**

| Number | What was actually measured | What it does NOT establish |
|---|---|---|
| **52% of tests affected; 3.95% of atomic changes per affected test** (Chianti) | Java programs, Eclipse-based tooling, JUnit regression suites, 2004 | Nothing about typed architecture graphs, generated web apps, or LLM-driven edits. The ratio is suggestive, not transferable |
| **Static slices ~30% of program size** | Empirical slicing surveys across C-family programs | It is a warning about unbounded closures in general, not a prediction of our tier sizes. Our graph is coarser and much smaller than a statement-level PDG |
| **2–97 files per task; 5/6 repos pass vs 0 baselines** (CodePlan) | Two tasks — C# package migration, Python temporal code edits — on a handful of repositories | A small-n result on repository migration. It shows the *framing* works; it is not a success rate we can expect |
| **85.7% recall → 95.8% with RAG, at 3.0–3.4% review burden** (ProReFiCIA) | Requirements documents, an unnamed industrial dataset in a regulated domain, plus a benchmark dataset (93.3%) | **Measured on natural-language requirements, not on architecture graphs or code.** Our inputs are typed and much smaller. The numbers are a target to aim at, never a claim to repeat about our system |
| **>99.9% of regressions caught at ⅓ of transitively dependent tests** (Meta) | Meta's monorepo, years of historical test-outcome data | Requires a large labelled history. Unavailable to us until many real builds have run |

**Three assumptions this skill makes that no cited paper supports:**

1. That a *derived* architecture graph (nodes generated from a spec by rules) has impact
   properties comparable to a graph *extracted* from existing code. Plausible, unverified.
2. That requirement-level CIA results transfer to a system where "requirements" are generated by a
   model from a conversation rather than authored by engineers.
3. That tiering by hop distance correlates with actual change probability. It is the standard
   heuristic; it has not been validated on this shape of graph.

**§2.6 has a different evidentiary basis and should not borrow the table's authority.** The
allowlist rule and the distinguishable no-op come from one repository's source, read once
(`docs/mined/PASS2-FOUR-REPOS.md` §1.4), with no evaluation attached. They are cheap, they fail in
the safe direction, and their justification is the argument stated inline — not a measurement.
Nothing above shows that allowlist-preservation loses less work than denylist-preservation; it
shows only that the failure mode of the denylist is silent, which is the property that matters when
the cost of being wrong is someone's finished package.

**The honesty rule (`docs/next/SKILLS.md`): a skill may not claim more than its paper shows.** If
you write "impact analysis catches 95.8% of affected requirements", you are selling ProReFiCIA's
industrial-dataset result as ours. Write "ProReFiCIA reports 95.8% recall on their industrial
dataset; we have not measured ours."

---

## 4 · Eval

Runnable cases. Each states the expected outcome so the skill can be measured rather than believed.

### E1 · Tiering is present and named
Given a design or implementation of impact analysis, assert it returns **at least two tiers** with
distinguishable names, not a flat set. A flat set fails.

### E2 · Depth is bounded and configurable
Assert a maximum-depth parameter exists and has a stated default. An unbounded transitive closure
fails, and the failure message should cite the ~30% slicing result.

### E3 · Both perspectives present
Assert the impact set contains **both** graph-internal nodes (dependency analysis) **and** at least
one traceability link outward — to a spec field, requirement id, package or file. One without the
other fails.

### E4 · Reverse attribution exists
Given a failure in the affected set, assert the system can name **which part of the change** is
responsible. Forward-only fails (Chianti §2.4).

### E5 · No unearned number
Grep the produced text, docs, UI copy or commit messages for `95.8`, `85.7`, `99.9`, `3.95`, `52%`
without an accompanying attribution clause naming the paper and its dataset. Any bare occurrence
fails.

### E6 · Correct label before measurement
Assert the system calls its output **"may-impact"** or an equivalently hedged term until recall has
been measured against real diffs. Calling an unmeasured over-approximation "impact analysis" fails.

### E7 · Over-approximation smoke test
Construct a graph where one entity is referenced by every operation (a `user` table, typically).
Assert that editing an unrelated field does **not** return the whole graph. This is Nx's documented
"all projects too often affected" failure, reproduced deliberately.

---

### E8 · Backward traceability
Given an impact set and the diff the change actually produced, assert that **every changed line
maps to a named element of the set**. Unmapped lines are the finding, one per hunk. A system
that reports only forward coverage — "we predicted the files that changed" — passes E5 and fails
this, and it is the direction a user notices.

## 5 · When this skill is the wrong tool

- **Resolving a marking to a file after the fact.** That is manifest resolution, not CIA. CIA is
  the question asked *before* the change.
- **Test selection at scale.** Once outcome history exists, Meta's learned approach dominates
  static derivation. This skill is the pre-history of that.
- **Deciding whether a change is a good idea.** CIA sizes a change. It says nothing about whether
  it should happen.

---

*Scanned and written 2026-08-26. Every paper read at abstract-to-method level; none reproduced.
Numbers are the authors' own, on the authors' data.*
