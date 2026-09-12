---
name: contract-retrieval
layer: D
phase: build-time
status: written
description: Find candidate catalog entries for a build package when the library is too large to scan. Use when the component library's matcher gets slow, when adding an index to the catalog store, when someone proposes embedding or fuzzy-matching components, or when deciding how a growing catalog is searched without packing it into a prompt. Also use when a matcher, lookup or optional provider has to report that it found nothing versus that it could not look. Covers index-then-verify retrieval, approximate set-containment search, the three honest outcomes a search may return, and the one rule that keeps matching decidable.
---

# contract-retrieval

Scio's library matches a build package against catalog entries with an exact set relation
(`library/identity.py:184`): operations and routes by subset, files by equality. It is
decidable, it is free, and it is the reason the layer can promise that assembly never guesses.

It is also, today, a Python loop over `SELECT payload FROM library_entry` — every entry, full
JSON, into memory, on every match (`library/store.py:241`).

That works at one entry. It does not work at ten thousand. This skill is how to scale the
*search* without touching the *decision*.

---

## 1 · Source

Two lines of work, both settled, both older than they feel.

**LSH Ensemble: Internet-Scale Domain Search** — Erkang Zhu, Fatemeh Nargesian, Ken Q. Pu,
Renée J. Miller. PVLDB 9(12), 2016. [arXiv:1603.07410](https://arxiv.org/abs/1603.07410) ·
[paper](http://www.vldb.org/pvldb/vol9/p1185-zhu.pdf) ·
implemented as `MinHashLSHEnsemble` in [datasketch](https://ekzhu.com/datasketch/lshensemble.html)
(ekzhu, MIT).

**SourcererCC: Scaling Code Clone Detection to Big Code** — Hitesh Sajnani, Vaibhav Saini,
Jeffrey Svajlenko, Chanchal K. Roy, Cristina V. Lopes. ICSE 2016. Successor for harder clones:
**Oreo** ([arXiv:1806.05837](https://arxiv.org/pdf/1806.05837)), same group.

---

## 2 · The rule that everything else obeys

> **Retrieval may narrow. Only `satisfied_by` may decide.**

An index that returns a **superset** of the true matches is safe: the exact test runs
afterwards and discards the extras. An index that returns a **subset** is unsafe: a dropped
match is silent, and nobody ever finds out.

So every retrieval stage is tuned for **recall**, never for precision, and every stage is
followed by the exact test. A retrieval layer that is allowed to say "no match" on its own has
replaced a decidable system with a probabilistic one.

If you take one thing from this skill: **you may make the search approximate; you may never
make the answer approximate.**

---

## 3 · Method, in the form we use it

### 3.1 What LSH Ensemble actually contributes

The paper's central argument is not "use MinHash". It is that **Jaccard similarity is the wrong
measure when the two sets differ greatly in size**, and that **containment** —
`|Q ∩ X| / |Q|` — is the right one for "does X cover Q".

That is exactly our asymmetry. `matcher.py` states it plainly: *an entry may provide MORE than
a package needs, never less.* A booking entry with eight operations and a package with three
have a Jaccard similarity of 0.375 and a containment of 1.0. Similarity would rank the correct
answer last. This is why a naive embedding or similarity index over the catalog would quietly
get worse as entries got richer — the better an entry is, the less similar it looks.

The paper's second contribution is **partitioning by set size**, so the index does not degrade
under skew, with a proof that equi-depth partitioning approximates the optimum for power-law
distributions. A contributed-entry catalog is power-law by construction: a few generic entries
with many operations, a long tail with three.

### 3.2 What SourcererCC contributes

The architecture, not the measure: an **inverted index over token bags, a cheap filter, then
exact verification**. SourcererCC scaled to 250M LOC on a single workstation that way. Oreo
adds an "action filter" ahead of the expensive step, purely to stop candidate explosion.

Read that as: *the expensive exact test is not the problem; running it on everything is.*

### 3.3 The three stages, as they apply to Scio

| Stage | Mechanism | Returns | Decides? |
|---|---|---|---|
| 1 · exact narrowing | one SQL query — `category = ? AND operations @> ? AND routes @> ? AND contract_key = ?`, GIN-indexed | the true candidate set | it **is** the exact test, in SQL |
| 2 · approximate narrowing | `MinHashLSHEnsemble.query(minhash, len(ops))` at a **low** containment threshold | a recall-oriented superset | **no** — stage 1 re-runs over its output |
| 3 · choose | `resolve_ambiguity`, unchanged | one entry or none | only among entries that already passed |

**Build stage 1 first and possibly only.** PostgreSQL GIN indexes support `@>` (contains) and
`<@` (contained by) on array columns natively. `contract_key` is already computed, already
stored and already indexed (`store.py:150`, `:156`) — and queried by nothing. Storing
`operations` and `routes` as `text[]` beside it makes `candidates()` one statement.

Stage 2 is for when stage 1's index selectivity measurably degrades, and for the **near-miss
ledger** — "which entries nearly matched, and by how much" — which is a ranking question and
therefore the one place approximation is the right tool.

### 3.4 Sizing rule

GIN needs a substantial row count before it beats a sequential scan. Do not add an index to a
catalog of four entries; you will measure noise and conclude the wrong thing.

Trigger: catalog > ~10³ entries, **or** `catalog()` visible in the plan step's timing.

**Two rules to build the index *with*, when it is built.** Both are one line and both are
somebody else's bug: the index's staleness snapshot is written **after** the index is durable
and **only from the set that succeeded**, so a crash lands in "still stale" rather than in
"fresh and wrong" (claude-context ships the half-fixed version); and a cache or derivation key
is `(content hash, producer identity, format version)` with the **producer in the key**, not
beside the value, so a stale entry becomes unreachable rather than mislabelled. The rest of the
index's requirements — the three-way `{added, removed, modified}` diff, keying the snapshot by
artefact identity rather than filesystem path, the rebuild mutex — belong to the ADR that
decides to build it, not here. See `docs/triage/LAYER-DFG-TRIAGE.md` §8.

---

### 3.5 What retrieval is allowed to return — and the outcome it must not conflate

Three outcomes, never two. gstack's `lib/gstack-decision-semantic.ts` makes the distinction
exactly, and it is the one Layer D's matcher does not yet make:

| Outcome | Means | The caller must |
|---|---|---|
| a candidate set | the index ran and these passed it | run `satisfied_by` over it |
| `[]` (empty) | **it ran, and genuinely found nothing** — *"also honest, and distinct"* | generate, and record a miss |
| `null` | **it did not run** — unavailable, timed out, unresolvable scope | **degrade**, and say so. Never record a miss |

**The general rule belongs to `validation-evidence`** — empty versus missing versus error, typed
three ways — and it is carried for impact sets in `change-impact-analysis` §2.6. This section is
the *retrieval* instance, and it exists because retrieval has a fourth failure the general rule
does not name: a search that widens its scope rather than refusing.

Their name for collapsing the last two is **"silent skipping"**, and the failure it produces is
a system that reports perfect precision because it never looked. `MatchReport` today can say
*no entry matched*; it has no way to say *the matcher could not look*, so a degraded run and a
genuine miss are the same row in any ledger built over it (`docs/next/LAYER-D-LIBRARY.md` §3.2).

Two rules follow, and both are refusals:

- **Never search unscoped when the intended scope cannot be resolved.** gstack refuses rather
  than widening, because *"an unscoped search pulls code/doc corpora that would be mislabeled as
  'related decisions'"* — which is precisely Layer D's failure mode, a component returned as a
  match because its prose was similar. Widening on failure is failing open.

The optional half of a retrieval path must therefore never throw and never hang — gstack's
bounds it at a 10 s timeout and returns `null` on every failure, so the deterministic path still
answers. *"Never a dependency, always an enhancement."*

**Where a question is being grounded in a match** — Layer A asking about a package, a change
prompt citing a contract — the same three outcomes apply, and the honest form of the second is
*"nothing matched"* stated out loud rather than a question asked as if nothing had been looked
for.

---

## 4 · Limits — what the papers show versus what we are assuming

- **Neither paper is about component reuse.** LSH Ensemble searches *data columns* in open-data
  portals; SourcererCC searches *code clones*. We are transferring an index structure, not a
  result. No reported number carries over.
- **Clone detection tolerates false positives. We tolerate false negatives instead.** Their
  precision/recall trade-offs are tuned in the opposite direction from ours. Take the
  architecture; discard the thresholds.
- **LSH Ensemble is approximate, with error bounds, not guarantees.** Used as stage 2 it is safe
  only because stage 1 follows it. Used alone it would silently drop matches — the exact failure
  §2 forbids.
- **The partitioning proof assumes a power-law distribution.** Our catalog's distribution is
  *assumed* to be power-law and has never been observed, because the catalog has one matchable
  entry.
- **`MinHashLSHEnsemble` in datasketch is a simplified version of the published index** — the
  library's own docs say so. Behaviour differs from the paper.
- **Do not quote claude-context's headline as "retrieval quality unchanged".** Their reported
  F1 of 0.40 → 0.40 is **end-to-end edit-localisation** — `hits` are the files the agent
  *edited*, not what retrieval returned — with dispersion computed and unpublished. It measures
  a whole agent loop, not a retriever. The honest reading is: on their benchmark their mechanism
  retrieved the *same* and *cheaper* (−39.4% tokens, 1.65×), and 0.40 is low in absolute terms
  and they do not comment on it.
- **Semantic (Type-4) matching remains unsolved**, per *Semantic Code Clone Detection: Are We
  There Yet?* ([arXiv:2606.25272](https://arxiv.org/html/2606.25272), 2026). This is evidence
  **against** ever letting a learned model decide a match here, not for it.

---

## 5 · Eval

Runnable against `apps/engine`. Each case has an expected outcome; a change that alters one has
changed behaviour, not performance.

| # | Case | Expected |
|---|---|---|
| 1 | An entry providing 8 operations, a package needing 3 of them, same routes and files | retrieval returns it; `satisfied_by` is `True`. **Similarity-ranked retrieval must not rank it below a 3-operation near-miss** |
| 2 | Stage-1 SQL result vs the current Python `candidates()` over the same catalog | **identical sets**, every time. This is the migration's only acceptance test |
| 3 | Stage-2 LSH result at threshold *t* | a **superset** of the stage-1 result for every *t* ≤ 1.0. A single missing entry fails the stage |
| 4 | Empty contract (`operations == []`) | zero candidates at every stage — `identity.py:210` must not be bypassed by an index that treats an empty query as "matches everything" |
| 5 | Two entries with equal contracts | both survive retrieval and reach `resolve_ambiguity`; retrieval must not break the tie |
| 6 | Catalog of 10⁴ synthetic entries | stage 1 latency stays flat; the current `catalog()` path is expected to degrade linearly. Measure both, record both |
| 7 | The index is unreachable — connection refused, timeout, unresolvable scope | the call returns **`null`**, the caller degrades to the exact path, and the run is **not** recorded as a miss. A run that returns `[]` here fails the case |
| 8 | The intended scope cannot be resolved | the search **refuses**. Widening to an unscoped search fails the case, whatever it returns |

Case 3 is the one that catches the dangerous mistake. Case 1 is the one that catches the
tempting mistake. Case 7 is the one that catches the *invisible* mistake: a retrieval layer
that conflates "nothing matched" with "I did not run" reports a clean miss rate forever.
