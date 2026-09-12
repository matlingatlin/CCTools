# graphify — what the tool already does, and what we therefore need not build

**Written 2026-08-26 after a full pass over the CLI. Every row below was executed, not read.**

## Why this document exists

The standing rule in this project is *never invent what already exists — go to the list and search
before proposing.* We have applied it to standards, papers and competitors. **We had not applied it
to a tool sitting in our own `PATH`.**

`graphifyy` 0.9.50 was installed all along. Across a full day of work four of its roughly twenty
commands were used — `explain`, `path`, `update`, `hook`. Several of the rest are things this repo
had written down as gaps, planned as future work, or attributed to other projects.

---

## What was missed, and what it displaces

| Command | What it does | What we were doing instead |
|---|---|---|
| **`query "<q>" --budget N`** | graph traversal answering a question under an explicit **token cap**, and it says plainly when it truncated and how many nodes were cut | The direct answer to *"don't send more context than needed"*, which is graphify's central claim. `explain` was used all day; `--budget` was never used once |
| **`benchmark`** | measures token reduction against the naive full-corpus baseline | Hand-measured with `wc -c`. The tool ships the measurement |
| **`affected "X" --depth N`** | reverse traversal: what breaks if X changes — including **which tests cover it** | `change-impact-analysis`, a whole research skill (Arnold & Bohner, Chianti, CodePlan). The tool ships a working implementation of the mechanic |
| **`save-result`** + **`reflect`** | a memory loop: outcomes tagged `useful` / `dead_end` / `corrected`, aggregated into `LESSONS.md` with **half-life decay** and a **corroboration threshold**. Deterministic, no model | Two turns before this document, `remember` and `improve` were named as stages our pipeline lacks and ECC has. **That was wrong.** We already own them |
| **`god-nodes`** | most-connected nodes — the architectural hubs | Relevant to `design-rule-hierarchy`, which reasons about exactly this structure |
| **`global add / list / remove`** | one graph spanning several repos, in `~/.graphify/global-graph.json` | `OPERATING-MODEL.md` frames three repos as a distribution problem. This makes them one queryable corpus |
| **`extract --postgres DSN`** | pulls schema, views, functions and FK relationships from a **live database** into the graph | Layer G's data model, and the generated app's schema. Column-level detail is not represented — a stated limit |
| **`check-update`** | cron-safe check for whether semantic re-extraction is pending | |
| **`tree`**, **`export callflow-html`** | collapsible D3 tree; Mermaid call-flow HTML | |
| **`extract --code-only`** | full AST index with **no API key** | The zero-cost path, distinct from `update` |

Measured on our own graph (5,173 nodes, 12,054 edges over the predecessor):

```
Corpus:          258,650 words → ~344,866 tokens (naive)
Avg query cost:  ~13,202 tokens
Reduction:       26.1x fewer tokens per query
```

That 26.1× is the tool's own measurement of the thing this project keeps calling a principle.

---

## What this changes

**`docs/ECC-MINED.md` §2 is partly superseded.** Its items 8, 9 and 10 argue for adapting ECC's
"instincts" store and building a skill-run tracker to get a `remember` stage. We have a `remember`
stage: `save-result` writes structured outcomes and `reflect` aggregates them deterministically,
with decay and corroboration already implemented. The remaining question is narrower and better —
**what should call `save-result`, and when** — not whether to build the mechanism.

**`PIPELINE.md`'s eight stages are missing `remember`, and the mechanism for it exists.** That gap
stands; the build does not.

**The retrieval half of ADR-0001 has a tool it did not name.** The ADR states that its mechanisms
keep the graph fresh but cannot make a session *query* it. `query --budget` is the query worth
making mechanical, and `benchmark` is how we would know whether it is being used.

---

## The uncomfortable part, recorded on purpose

This is the fourth time in this project that something was proposed which already existed — after a
coverage formula where ISO/IEC/IEEE 29148 existed, a design-token shape where W3C DTCG existed, and
a change-impact method where the literature had one.

The first three were caught by scanning the internet. **This one was not, because nobody thought to
run `--help` on a tool we had already installed.** The rule as written says *search the domain*. It
should also say: **read the tools you already have, in full, before designing around them.**


---

## Full pass over every command, 2026-08-26

Each row was executed against real data. Untested claims are marked as such.

| Command | Result |
|---|---|
| `query --budget N` | **works.** Caps output at a token budget and states how many nodes it cut |
| `explain "X"` | works |
| `path "A" "B"` | works **only with `--undirected`** on our graph. `diagnose` reports `effective_directed: False`, so the directed default finds nothing and says to retry |
| `affected "X" --depth N` | **works.** Reverse traversal, and it names the tests that cover the symbol |
| `god-nodes` | works. Top hubs on our graph: `ProviderRegistry` 109 edges, `BuildPackage` 106, `derive_architecture()` 89 |
| `benchmark` | **works.** 26.1× fewer tokens per query on our graph, measured by the tool |
| `save-result` / `reflect` | **works.** Outcomes tagged `useful`/`dead_end`/`corrected` → `LESSONS.md`, deterministic, no model |
| `diagnose multigraph` | **works, and our graph is clean**: 12,054 edges, zero dangling, zero self-loops, zero duplicates, zero collapsed |
| `update` | works. 5,955 files / 1.34M lines in 9.5 s, no model |
| `extract --code-only --no-cluster` | works. Full AST, no API key. Reports files it skipped and why |
| `cluster-only --no-label` | works. Deterministic re-clustering, **warns when saved labels no longer match the communities**, and backs up the curated graph first |
| `hook install/status/uninstall` | works. Absent from the top-level `--help` |
| `global add/list/path` | **works.** Merged 5,173 + 2 nodes into one cross-repo graph and queried across both. This is the three-repo question answered |
| `merge-graphs` | works. 5,175 nodes, 12,055 edges |
| `tree` | works. 372 KB collapsible D3 tree |
| `export callflow-html` | works. 16 Mermaid diagrams, 15 call tables, written to `docs/as-built/graph/graph-callflow.html` |
| `check-update` | works. Silent when nothing is pending, as documented |
| `install --platform claude` | **works, and it mattered** — see below. Side effect: also creates `~/.claude/CLAUDE.md` if absent |
| `add <url>` | **broken for our use.** See below |
| `label`, `watch`, `clone`, `merge-driver`, `extract --postgres/--cargo/--mode deep`, exports `--wiki/--neo4j/--falkordb/--svg/--graphml/--mcp` | **not tested.** `label` needs an LLM backend; `--postgres` needs a live database; `merge-driver` was registered by `hook install` but never exercised on a real conflict |

### `add` reports success and saves nothing — traced to source

`graphify add https://arxiv.org/abs/2501.07857` printed `Saved arxiv:` and wrote a **302-byte
stub**: title set to the bare ID, authors empty, abstract empty, no body. Both URL forms.

**Two causes, and only one is graphify's fault.** *(This corrects an earlier version of this
section, which said the paper was reachable and implied the parser had broken. The parser is never
reached.)*

1. **Environmental.** `ingest.py` fetches with a bare `urlopen` and no proxy handling; `security.py`
   then rejects the resolved address — `SSRF blocked: IP 127.0.0.1 … is private/reserved`. This
   environment routes outbound HTTPS through a local proxy, so the guard resolves the *proxy* rather
   than the target and the fetch can never succeed. There is no escape hatch:
   `GRAPHIFY_ALLOW_LOCAL_PROVIDERS` gates LLM providers, not ingestion. **`graphify add` cannot work
   here at all.**

2. **A real defect, and it is not ours.** `_fetch_arxiv` at `ingest.py:165` wraps the fetch in a
   bare `except Exception:` and falls back to
   `title, abstract, paper_authors = arxiv_id.group(1), "", ""` — after which the caller prints
   success. Any transient failure, anywhere, silently produces a file that looks like a saved paper
   and contains nothing. Worth reporting upstream; it is a few lines.

**Where the fix goes matters more than that it works.** Four options, in order:

| Where | Verdict |
|---|---|
| **Upstream** | the durable fix for cause 2. Report it |
| **Beside the vendored file, in something of ours** | where cause 1's workaround belongs — it cannot drift, because it is ours |
| **Patched into the vendored `SKILL.md`** | **no.** This is the drift we just spent a pass removing |
| **A fork of the package** | last resort, and it inherits every future upgrade as a merge |

So: `scripts/fetch-paper.py`. It uses `curl`, which honours `HTTPS_PROXY`, and — the part graphify
omits — **it refuses to write when extraction comes back empty**, exiting non-zero with the reason
rather than saving a stub. Verified: a real paper writes **1,820 bytes** with title, authors and a
1,349-character abstract; a 404 exits 1 and writes nothing.

A corpus that looks populated and is empty is worse than one that is short. That is the same
failure signature as the partial graph above, twice in one tool, and the general rule it teaches is:
**check what a tool wrote, not what it printed.**

### `install` is how the vendored drift gets fixed

Our vendored `graphify/SKILL.md` was **1,208 lines and wrong**: it unpacked three return values from
`check_semantic_cache`; the package returns four and takes two more arguments. 1,153 lines differed
from what 0.9.50 ships.

`graphify install --platform claude` writes the package's own copy — **713 lines plus a
`references/` directory of eight files**. Two conclusions elsewhere in this repo were wrong because
of the stale copy:

- `REVIEW-WHOLE.md` concluded that re-fetching **could not** fix the drift because the vendored
  sha matched its pin. Re-fetching fixed it; the vendored copy simply predated the package.
- The same review found *"zero use of progressive disclosure"* across our skills and cited
  graphify's 1,204 lines. **Upstream uses it** — `SKILL.md` loads a `references/*.md` only when its
  step is reached. We vendored a monolithic older version, then criticised it for being monolithic.

Ours is now the package's copy, recorded in `.claude/skills/graphify/VENDORED.md`.
