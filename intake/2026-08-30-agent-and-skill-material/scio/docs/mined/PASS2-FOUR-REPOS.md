# Four repositories, read properly

*Second pass, 2026-08-26. `docs/mined/OTHERS-MINED.md` covered eight repositories and read four of
them only in part; this reads those four properly. Everything already in `OTHERS-MINED.md` is out of
scope — where a finding extends one of its items the number is cited (**OM-37**) rather than restated.*

**The skip verdicts stand.** None of these four is being adopted and nothing below reopens that; this
is mining — mechanisms, numbers and failure modes out of code we will not depend on. **Every finding
names a Scio layer, or says it is for our build process:** **A** intake · **B** understanding ·
**C** build plan · **D** library · **E** build & execution · **F** design window · **G** cross-cutting.

---

## Coverage and licences, re-verified

**Licences were re-read from each repository's own `LICENSE` file on 2026-08-26**, not from the
GitHub API summary — the mistake `OTHERS-MINED.md` records having been made once already. All four
clones are the same commits `OTHERS-MINED.md` read; nothing was re-fetched, so the commit hashes
below are directly comparable.

| Repo | Commit | Commit date | `LICENSE` file says | `package.json` says | Verdict |
|---|---|---|---|---|---|
| `eyaltoledano/claude-task-master` | `c0c98d3` | 2026-04-23 | **MIT + "Commons Clause" License Condition v1.0**, 25 lines. Licensor: Eyal Toledano, Ralph Khreish | `"MIT WITH Commons-Clause"` | **confirmed.** Not free for our use |
| `zilliztech/claude-context` | `6fc318b` | 2026-07-14 | MIT, 21 lines, "Copyright (c) 2025 Zilliz" | `"MIT"` | confirmed MIT |
| `supermemoryai/supermemory` | `9652478` | 2026-08-26 | MIT, 21 lines, "Copyright (c) 2025 supermemory" | **no `license` field at all** (root `package.json` is `"private": true`) | MIT by the file; the manifest is silent |
| `yamadashy/repomix` | `f465ad9` | 2026-08-23 | MIT **text**, 7 lines, "Copyright 2024 Kazuki Yamada" — **the words "MIT License" appear nowhere in the file** | `"MIT"` | MIT by body text, not by title |

Two corrections to the licence record, both small and both the kind that compounds:

1. **`claude-task-master`'s Commons Clause is narrower and more specific than "withholds the right
   to sell."** The exact scope, from `LICENSE:19`: *"'Sell' means practicing any or all of the
   rights granted to you under the License to provide the Software to third parties, for a fee or
   other consideration (including without limitation fees for hosting or consulting/support
   services related to the Software), as part of a product or service whose value derives, entirely
   or substantially, from the functionality of the Software."* And `LICENSE:21` defines the Software
   as *"All Task Master associated files (including all files in the GitHub repository
   'claude-task-master' and in the npm package 'task-master-ai')."* **Every file in the repo,
   including the prompt JSON assets.** Scio is a hosted commercial builder whose Layer C is task
   decomposition. Nothing from this repository may be vendored, and no prompt text may be copied.
   **Everything in §1 below is an idea restated in our own words. Where an idea is close to their
   text, §1 says so at that point.**
2. **`repomix`'s `LICENSE` has no title line** — the MIT body, `Copyright 2024 Kazuki Yamada` on line
   1, and nothing naming the licence. The answer is MIT, but a tool identifying licences by heading
   returns "unknown" here: **if Layer D's library ever takes outside contributions, identify licences
   by body hash, not by title.**

### What was actually read, this pass

Reported honestly. The right-hand column is what I did **not** open, and it is not empty.

| Repo | Files (excl. `.git`, `node_modules`) | Read this pass | Not read |
|---|---:|---|---|
| `claude-task-master` | 1,254 | `tm-core/src/modules/workflow/` in full (orchestrator, state manager, validator, types); `loop/` (service, types, all 5 presets); `execution/executors/`; `dependencies/`, `reports/`, `briefs/` inspected; `scripts/modules/{scope-adjustment,find-next-task,prompt-manager,analyze-task-complexity,expand-task}.js`; `src/prompts/schemas/`; `utils/contextGatherer.js` (grepped, not line-read) | the 156 files under `tests/`, `apps/extension` and the rest of the 262 files under `apps/`, `mcp-server/` (89), `tm-profiles`, `tm-bridge`, `storage/adapters`, `auth`, `git`, `integration/export.service.ts` |
| `claude-context` | 180 | `packages/core/src/sync/` and `splitter/` line by line; `context.ts` (1,425 lines) on the index/reindex/collection paths; `packages/mcp/src/sync.ts`; `evaluation/` including the analysis script and both case-study result files | `vectordb/` (1,769 lines of Milvus client) and `embedding/` beyond their interfaces, the `vscode-extension` and `chrome-extension` packages, build config |
| `supermemory` | 1,160 | `packages/validation/schemas.ts`, `packages/memory-graph/src/` (version chain, graph-data hooks, hover popover, their tests), `packages/tools/src/claude-memory.ts`, `apps/mcp/src/server/`, `skills/supermemory/references/` | `apps/web` (the bulk of the 1,160), `browser-extension`, `raycast-extension`, `canvas/renderer.ts` in detail, the SDK middlewares, `packages/validation/api.ts` beyond grep — **and the memory engine itself, which is not in the repository** |
| `repomix` | 1,175 | `src/core/treeSitter/` line by line (`parseFile.ts`, `BaseParseStrategy.ts`, `TypeScriptParseStrategy.ts`); `src/core/metrics/tokenCountCache.ts`; `src/core/{file,output}` and `src/config/configSchema.ts` by targeted search | the other five parse strategies and the 19 query files beyond their names, `packager.ts`, `security/`, `website/`, `browser/`, `src/mcp/`, `tests/` |

**Coverage claim: high for `claude-context` (180 files, the whole engine read), good for
`supermemory`'s model and `repomix`'s core, partial for `claude-task-master`** — its 1,254 files
are mostly CLI/editor surface, and I read the domain modules and left the surface. Where a section
below is thin, it says so rather than padding.

---

## 1 · claude-task-master against Layer C

*`c0c98d3`, 2026-04-23. MIT + Commons Clause — **ideas only, no text, no code.** Where a phrase of
theirs is short and load-bearing I quote it as evidence of what their code does.*

`OTHERS-MINED.md` §3 read the task model, two prompt templates, the `tasks.json` schema and dependency
validation (OM-37…OM-42). It did not open `packages/tm-core/src/modules/` — 143 non-test TypeScript
files — where the interesting half lives. The task model is the noun; the modules are the verbs.

### 1.1 A typed state machine with five phases and no free transitions

`workflow/types.ts` declares two enumerations, and their separation is the design:
`WorkflowPhase = PREFLIGHT | BRANCH_SETUP | SUBTASK_LOOP | FINALIZE | COMPLETE` and
`TDDPhase = RED | GREEN | COMMIT`.

The outer machine has **exactly four declared transitions** (`workflow-orchestrator.ts:47-72`); an
event matching none throws *"Invalid transition: ${event.type} from ${this.currentPhase}"* (`:139`).
The inner TDD cycle is dispatched separately with from-phase assertions — `RED_PHASE_COMPLETE` from a
non-RED phase throws (`:170`). Only `ERROR`, `ABORT` and `RETRY` work in any phase, special-cased
before dispatch (`:105-124`). And `ALL_SUBTASKS_COMPLETE` reaches FINALIZE and *stops*: the comment at
`:277` is explicit that it does not auto-advance to COMPLETE, because completion requires an explicit
call.

**Layer C emits `BuildPlan{packages, order, graph}` and Layer E executes it, but there is no typed
statement of the states a package passes through, so there is nowhere to reject an out-of-order report
from an executor.** Their machine makes "green before red" unrepresentable by construction rather than
by a rule in a prompt — four rows of table and one lookup. And a terminal state you can only reach
deliberately is the right shape for "the build is done", where a wrong `done` ships an app.

Persistence uses `steno` for atomic queued writes plus a 5-deep backup ring
(`workflow-state-manager.ts:35`), and **prune failure is logged as a warning (`:251`), not raised** —
losing the ability to clean up old backups must not fail a build. Ours should choose that explicitly.

### 1.2 `TestResultValidator` — the anti-fabrication gate, and the best thing in the repo

A model reports test results; `services/test-result-validator.ts` decides whether the report is
internally coherent before anything acts on it. Six checks, all arithmetic, no second model:

| Check | Line | Why it cannot be faked |
|---|---:|---|
| `passed + failed + skipped === total` | `:59` | a fabricated summary usually gets this wrong |
| RED must have `failed >= 1` | `:85` | tests written first that already pass are not testing the new behaviour |
| RED must have `total >= 1` — *"Cannot validate empty test suite"* | `:91` | "I wrote tests", with zero tests |
| GREEN must have `failed === 0` | `:121` | — |
| GREEN must have `passed >= 1` | `:127` | zero failures is trivially true of an empty suite |
| `total < previousTestCount` ⇒ warning | `:137` | tests deleted to make the suite pass |

**Together, four integers make the two cheapest ways to fake a green build — write no tests, delete
the failing ones — detectable without reading any code.** OM-33 says an agent's success report is not
evidence; this is the cheapest instance of that principle.

It composes with Layer C's criteria model, `produced_by` × `observed_by` (`criteria.py:67`). Layer C
§1.1 measures **8 of 27 criteria `observed_by: unsupported` and 0 `interaction`** on the canonical
booking spec, and an unobserved criterion is exactly where a fabricated pass is undetectable. Their
validator does not fix that; it shows the check that becomes possible once a criterion *is* observed:
**the observation reports counts, and the counts must be consistent with the phase they claim.**

Two limits they state rather than hide: REFACTOR is validated with the GREEN rules (`:235-240`), and
`previousTestCount` is optional, so the regression check is silent unless a caller threads it through
— **a check that is off by default is off.** If we take this, that field is required.

### 1.3 "Already implemented" is a first-class outcome, not an error

`workflow-orchestrator.ts:172-206`: when RED completes with `failed === 0`, the machine does not throw
and does not proceed to GREEN. It emits `tdd:feature-already-implemented`, marks the subtask
completed, advances, and starts the next RED — or transitions to FINALIZE.

**This is OM-37 (`recommendedSubtasks: 0` — the scorer may decline to decompose) arriving at the other
end of the pipeline, and the pair is the finding.** Both are *successful* outcomes with their own
event. **Layer C should be able to emit a package whose expected outcome is "already satisfied", and
Layer E should be able to close one without change** — which is exactly what Layer D produces when a
`Contract` matches and the component is assembled rather than generated. Today that is modelled as a
match, not as a build outcome. It is one state and should be represented once.

### 1.4 The re-scope arithmetic: code decides the count, the model fills the content

`scripts/modules/task-manager/scope-adjustment.js`. `regenerateSubtasksForComplexity()` (`:169`)
computes a target subtask count in pure arithmetic from four inputs — direction (`up`/`down`), strength
(`light`/`regular`/`heavy`, validated against a three-element allowlist at `:26`), the preserved count,
and the original complexity score. Scope-up regular is `max(6, preserved + ceil(pending × 1.3))` scaled
by `(0.8 + 0.4 × complexityFactor)` where `complexityFactor = max(0.5, originalComplexity/10)`;
scope-down heavy multiplies by an `ultraAggressiveFactor` of **0.3 at `originalComplexity >= 9`, 0.5 at
`>= 7`, else 0.7**, floored at 1 (`:222-274`). Only then is the model asked for `max(1, target −
preserved)` subtasks.

**The constants are arbitrary — nothing justifies 1.3 over 1.25, and I would copy none of them. The
structure is the finding: the count is decided by code, the content by the model** — already Layer C's
governing constraint (*"Proposals may add rules; they may not move a rule into a prompt"*), here a
second independent instance. It attaches to Layer C §3.2: whatever decides how many packages a
component splits into must be a function of the architecture's own measurements.

**And the item to take outright — preservation is an allowlist, not a denylist:**

```js
const PRESERVE_STATUSES   = ['done', 'in-progress', 'review', 'cancelled', ...]  // :32
const REGENERATE_STATUSES = ['pending']                                          // :45
```

A status nobody anticipated is preserved, which is the safe direction. **Layer C §3.4's plan delta has
exactly this problem** — a new architecture must not discard packages that are built, building, or in
review — and written as "regenerate everything not done" it is a denylist. One more detail: when
`pendingSubtasks.length === 0` the function returns `regenerated: false` and touches nothing
(`:201-208`). A delta that changes nothing is a no-op with a distinguishable return.

### 1.5 The loop module — bounded iteration with a machine-readable early exit

`loop/loop.service.ts` (643 lines) runs N iterations of a prompt, each a fresh `claude` process
(`spawnSync`, `maxBuffer: 50 * 1024 * 1024`, `:330-335`), optionally under `docker` when
`sandbox: true`; the config comments state that `verbose` is **not compatible with `sandbox`**. Each
iteration's outcome is decided by `parseCompletion()` (`:289-305`), 17 lines:

```
<loop-complete>REASON</loop-complete>  → 'complete'      <loop-blocked>REASON</loop-blocked> → 'blocked'
exitCode !== 0                          → 'error'         otherwise                           → 'success'
```

**Four outcomes, three terminal, two carrying a reason the agent wrote — as a sentinel tag, so the
harness decides, not a reader.** `entropy.ts:42` shows the prompt side of the contract: *"If no
significant smells remain, output: `<loop-complete>LOW_ENTROPY</loop-complete>`"* — a named reason from
a small per-preset vocabulary.

**For Layer E this completes OM-30**, which gives the five-round fix ladder but not the exit protocol
it needs. A round ending because the agent believes it is done, one ending because it is blocked, and
one ending because the process died are three different things, and Layer E's relay cannot tell the
first two apart from prose. **Take a closed set of sentinel tags with named reasons, and a `blocked`
outcome that is neither success nor error.** OM-15 is the same discipline one level down.

### 1.6 `find-next-task` — WIP preference before priority

138 lines whose docstring states the policy before the code: prefer an eligible **subtask of a parent
already `in-progress`**, falling back to top-level tasks only if none exists; within either set the sort
is **priority → fewest dependencies → parent id → sub id** (`:83-97`), a total order. Layer C already
orders by tie-broken Kahn, so the determinism is confirmation. **The finish-what-is-started preference
is not**, and Layer E should state it rather than inherit it from plan order — a builder that starts a
second package while a first is half-built holds two partial states in one repository, the merge surface
Layer E's isolation model exists to avoid.

### 1.7 The prompt registry, read properly — and two defects not to copy

OM-42 took the shape of `src/prompts/` (8 prompt assets, 3 schemas: `prompt-template` 136 lines,
`parameter` 48, `variant` 39). `scripts/modules/prompt-manager.js` (534 lines), which OM-42 did not
read, has two problems that matter to anyone building the same thing.

**Defect 1 — schema validation fails open.** `:62-71` compiles the template schema with Ajv and on any
failure sets `this.validatePrompt = () => true`, commented *"Fallback to no validation"*. Every
subsequent guard reads `if (this.validatePrompt && this.validatePrompt !== true)` (`:94`, `:138`,
`:418`), so one compile failure silently disables validation everywhere. **A gate that degrades to open
when its own schema fails to load is not a gate.** If our `Playbook` becomes a versioned schema-validated
asset, a schema that will not compile must be fatal at startup — the same fail-closed principle as OM-9.

**Defect 2 — variant conditions are JavaScript, run through `new Function`.** `evaluateCondition()`
(`:273-285`) builds `new Function(...Object.keys(context), 'return ' + condition)` and calls it.
`expand-task.json` v1.0.0 ships conditions `expansionPrompt`, `useResearch === true && !expansionPrompt`,
and none. Two consequences: **arbitrary code execution from a template file** — and Layer D's
contributed components and Layer F's user markings mean "a template with a field somebody else wrote" is
a shape we will meet — and **precedence is JSON key order**, because `selectVariant()` (`:252-266`)
returns the first non-default variant whose condition is true and nothing checks the conditions are
disjoint. Theirs are disjoint only because a human hand-wrote `&& !expansionPrompt`. **A variant
condition must be a declarative predicate over named parameters, and precedence must be an explicit
integer** — implicit precedence from file order presents as "the prompt changed when I reordered the
JSON".

The good half of OM-42 survives — semver per prompt, typed named parameters, variants as a concept,
prompts as data — and `validateAllPrompts()` (`:409`) is the right instrument. It has to be unskippable.

### 1.8 Read and left

`utils/contextGatherer.js` (973 lines) counts tokens per source class — `customContext`, `tasks`,
`files`, `projectTree` — into a breakdown with a total (`:99-224`), falling back to characters ÷ 4 when
the tokenizer throws. It is a **bill, not a budget**: nothing is dropped when the total is large.
gstack's `context-bill.ts` (OM-8) does it properly, so there is nothing to take — but it is a second
independent sighting of "measure the context you assembled, by source", which makes it a pattern.
**`dependencies/index.ts` is a stub** — eight lines and a `TODO`; the 1,860-line validator OM-38 mined
still lives in `scripts/`. `claude-executor.ts` (147 lines) wraps `spawn`. `briefs/`, `auth/`, `git/`,
`reports/`, `integration/export.service.ts` (1,645 lines), `apps/extension` and `mcp-server/` are
product and editor surface. None of it serves a layer.

---

## 2 · claude-context, past the vectors

*`6fc318b`, 2026-07-14, MIT. 180 files. Read this pass: `sync/` and `splitter/` line by line,
`context.ts` on its index/reindex paths, `mcp/src/sync.ts`, and all of `evaluation/`. The Milvus client
and the two editor extensions were not.*

The brief's framing is right: **Layer D's matching problem is not retrieval.** `Contract.satisfied_by`
(`identity.py:184`) is two subsets and an equality, and OM-43/OM-44 settled that no vector index goes
on the deciding path. What was left unread is everything that is not vector search. Read properly,
**the sync layer is weaker than OM-45 credited it with being, and the weakness is the useful part.**

### 2.1 The "Merkle DAG" is two levels deep and saves no work

`buildMerkleDAG()` (`synchronizer.ts:109-129`) sorts the file paths, concatenates every file's SHA-256
into one string as the **root** node, then adds **one flat child per file** with data `path + ":" + hash`.
That is the whole tree: a root and N leaves. No intermediate nodes, so no directory subtree to skip and
**no logarithmic diff** — `MerkleDAG.compare()` (`merkle.ts:79-89`) is a set difference over all node ids.

And `checkForChanges()` (`:138-162`) calls `generateFileHashes(this.rootDir)` first, which walks the
entire tree, `readFile`s every eligible file and SHA-256s it (`:35-43`, `:91-97`), *before* any
comparison. **The full cost is paid unconditionally on every check.** The DAG comparison is then only a
gate in front of `compareStates()` (`:164-188`), itself an O(n) diff over maps already in memory. The
Merkle structure contributes nothing but a name.

**Correction to OM-45.** For Layer D's catalog-index staleness take **content hashing + a persisted
snapshot + a three-way `{added, removed, modified}` set diff**, not a Merkle tree. `compareStates` is 24
lines and is the whole idea; three categories rather than "changed", because they drive three different
index operations and collapsing them costs a rebuild. The snapshot lives at
`~/.context/merkle/<md5-of-resolved-absolute-path>.json` (`:25-33`), so **moving or re-cloning the
repository silently invalidates it** (`loadSnapshot` catches `ENOENT` at `:229` and rehashes everything):
key a staleness snapshot by the artefact's identity, not its location.

### 2.2 The snapshot is committed before the work it describes — and their fix admits it

`checkForChanges()` does this in order (`:150-157`): compute the diff, replace `fileHashes` and the DAG,
`await this.saveSnapshot()` — **the snapshot now says everything is current** — and only then return the
change list to a caller that has done none of the work. That caller is `Context.reindexByChange()`
(`context.ts:430-503`), which then deletes old chunks and re-embeds. Anything that fails in between
leaves files marked indexed that **will never be revisited until their content changes again**.

They know. The `EmbeddingError` docstring (`context.ts:39-48`) is the confession:

> *"an EmbeddingError is always re-thrown so that the entire indexing pipeline stops. This prevents
> silent partial indexing: Milvus would otherwise receive zero vectors while the snapshot marks files as
> done."*

The remedy makes one class of failure fatal and does not cover the other: the same comment says *"a
per-file read/parse error … is logged and skipped"* — and a skipped file is already in the snapshot as
current. **A permanently missing index entry, from a transient parse error, with no signal.**

**For Layer D this is a hard requirement, not a preference: the staleness snapshot is written only after
the derived artefact is durable, and from the set that actually succeeded — never the set that was
scheduled.** If an index build is interrupted, the correct state is "still stale", and that must be the
state a crash lands in. This is OM-4's audit-sink invariant pointed the other way — there a refused
input must not be persisted, here a *succeeded* marker must not be persisted ahead of the success — and
both need a named test.

### 2.3 AST chunking indexes the same code two and three times

`splitter/ast-splitter.ts`, 270 lines, `chunkSize: 2500`, `chunkOverlap: 300` (`:29-30`; the langchain
fallback defaults to 1000/200). Nine languages, with `SPLITTABLE_NODE_TYPES` (`:16-26`) listing chunkable
node kinds — for TypeScript: `function_declaration, arrow_function, class_declaration, method_definition,
export_statement, interface_declaration, type_alias_declaration`.

`extractChunks`'s `traverse` (`:118-144`) pushes a chunk on a type match **and recurses into that node's
children anyway** (`:139-141`). Those types nest. `export class Foo { bar() {} }` yields three chunks —
the `export_statement`, the `class_declaration`, the `method_definition` — so **the body of `bar` is
stored three times**, at three granularities, with three embeddings. There is no dedup pass;
`refineChunks` (`:162-175`) only splits chunks over 2500 chars further. Add 300 chars of overlap and the
index is meaningfully larger than the corpus.

Nothing here transfers to Layer D — a component with a declared `Contract` is never chunked. It
transfers to how we read their headline number: **an index storing the same code at three granularities
is one plausible mechanism behind an F1 that does not move**, and a concrete reason to distrust
"AST-aware chunking" as a phrase absent a dedup rule. §4.1 is the same problem, solved.

### 2.4 Their evaluation, read at the source rather than at the README

| Metric | Grep baseline | With claude-context | Change |
|---|---:|---:|---|
| Average F1 | 0.40 | 0.40 | comparable |
| Average tokens | 73,373 | 44,449 | −39.4% (28,924 saved/instance) |
| Average tool calls | 8.3 | 5.3 | −36.3% |

*30 SWE-bench Verified instances, 15–60 min difficulty, exactly 2 file modifications, 3 runs each
(`evaluation/README.md:13-17`), against `claude-context-mcp@0.1.0` (`:66`).* Three qualifiers, cutting
in different directions:

1. **F1 is not measuring retrieval.** `calculate_metrics(hits, oracles)`
   (`analyze_and_plot_mcp_efficiency.py:23-47`) is set precision/recall over file paths, where `hits`
   are the files the agent **edited** (`utils/format.py:25`) and `oracles` are the files in the gold
   patch (`:94`). It is end-to-end edit localisation, not index quality. **That makes the result stronger
   against them**: given the whole agent loop to help it, the index still moved nothing.
2. **The README drops a dispersion its own script computes.** `:118-119` compute `avg_f1` and `std_f1`
   and `:127` prints `±`; the published table shows only `0.40` and `0.40`. The spread is what would
   tell you whether "comparable" means equal or noise.
3. **One published baseline artefact contains a malformed hit.** `case_study/pydata_xarray_6938/grep_result.json`
   lists a third hit of `'/data2/zha...ims'` — a truncated absolute path that leaked from a log, which can
   never intersect the oracle set and so drops baseline precision from 1/3 to 1/4 in that instance. One
   case study, not the aggregate — but the extraction is fragile and the fragility runs against the baseline.

**None of this changes OM-44's verdict.** 1.65× token reduction against graphify's measured 26.1×, for
no measured quality gain, is still not a trade Layer D makes. It changes how the number should be cited:
as *their end-to-end localisation F1, dispersion unpublished*, not as "retrieval quality unchanged".

### 2.5 Two mechanisms to take that have nothing to do with search

**A `mkdir`-based global sync lock that skips rather than queues** (`packages/mcp/src/sync.ts`):
`fs.mkdirSync(lockPath)` as the mutex (atomic on POSIX; `EEXIST` means held, `:98,:107`), an `owner.json`
inside carrying `{pid, token, acquiredAt}` (`:99-103`), a **10-minute** default staleness after which the
lock is renamed aside and reclaimed with `recoveredStaleLock: true` recorded (`:12`, `:114-129`), and —
the important part — when the lock is held and fresh the cycle is **skipped, not queued**: *"Another MCP
process is already syncing. Skipping this cycle."* (`:134`). Background sync defaults to 5 minutes, floor
1 second, unparseable env falls back to the default with a warning (`:10-11`, `:42-53`).

**Layer D and Layer E both need this.** Two concurrent builds must not rebuild the catalog index at once,
and for a periodic derived-artefact rebuild the right behaviour is *skip this round* — a queue of rebuilds
is worse than a missed one. The stale-reclaim timeout and the recorded owner make the lock safe to leave
behind when a sandbox dies, which for Layer E it will.

**And one thing not to copy.** `deleteFileChunks()` (`context.ts:504-521`) builds a Milvus filter by
interpolation — `` `relativePath == "${escapedPath}"` `` — escaping backslashes only, so a path containing
a double quote (legal on Linux) breaks it. Layer D will build queries from component and entity names that
trace back to a user's spec. **Identifiers derived from user text are parameters, never interpolation** —
the boundary OM-1's `datamark()` draws for prompts, drawn here for queries.

---

## 3 · supermemory's model of memory

*`9652478`, 2026-08-26, MIT (`LICENSE` re-read; the root `package.json` carries no `license` field).
Read: `packages/validation/schemas.ts`, the version-chain / graph-data / hover-popover parts of
`packages/memory-graph/src/` with their tests, `packages/tools/src/claude-memory.ts`,
`apps/mcp/src/server/`, and `skills/supermemory/references/`.*

**A coverage statement first, because it bounds everything below. There is no backend in this
repository.** `apps/` is `browser-extension`, `docs`, `mcp`, `memory-graph-playground`,
`raycast-extension`, `web` — and nothing else. The memory engine is a hosted API. What is readable is
the **model**: the schema, the client-side predicates, the renderer, and documentation of closed rules.
**The rules themselves are not here and I verified none of them.**

`MemoryEntrySchema` (`packages/validation/schemas.ts:242-278`) is 22 fields, and read whole it separates
**four axes that Scio's `FieldMeta{value, source, confidence, provenance}` collapses into one**:

| Axis | Fields | What it answers |
|---|---|---|
| **Identity over time** | `version`, `isLatest`, `parentMemoryId`, `rootMemoryId` | which assertion is current, and what it replaced |
| **Authority** | `isInference` (derived vs stated), `isStatic` (permanent vs episodic) | may this be silently re-derived; may time erode it |
| **Lifecycle** | `forgetAfter`, `forgetReason`, `isForgotten` | when does this stop applying, and why |
| **Corroboration** | `sourceCount`, and the `MemoryDocumentSource` join (`:287-294`) with `relevanceScore` | how many sources, and which ones |

OM-46…OM-50 took the first, third and fourth. **`isStatic` is what OM missed, and it is a second,
independent authority bit.** `references/architecture.md:172-184`: static is *"permanent facts that
don't change… not subject to temporal updates, high priority in retrieval"*; dynamic is *"contextual,
episodic… can be updated or superseded, time-sensitive relevance."* `isInference` says where a value came
from; `isStatic` says whether time may erode it. **Scio needs both.** "The app is for booking restaurant
tables" is static; "the user is unsure about payments" is dynamic; `FieldMeta` cannot tell them apart, so
Layer F's directed change has no principled rule for which fields a later conversation may quietly revise.

### 3.1 What decays: **nothing.** The forgetting model has no engine behind it

This corrects the tone of OM-48. `forgetAfter` is read in exactly **one place in the repository** —
`getMemoryBorderColor()` (`memory-graph/src/hooks/use-graph-data.ts:42-54`), which paints a node's border
`memBorderExpiring` when `0 < msLeft < SEVEN_DAYS_MS`. That is the whole use. Nothing schedules, nothing
sweeps, and a grep for `isForgotten` across `apps/` and `packages/` returns type declarations, mock data,
tests, two read filters and colour logic — **no writer.**

Their own test states the consequence without flinching (`__tests__/graph-data-utils.test.ts:68-73`):
*"does not treat an already-elapsed `forgetAfter` as expiring"* — a memory whose `forgetAfter` passed 60
seconds ago and which is not flagged `isForgotten` renders in the normal colour. **An expiry date that has
passed produces no state change and no signal.**

**Where ours is better, plainly: graphify's `save-result` / `reflect` gives us half-life decay and a
corroboration threshold deterministically — an engine. Supermemory has the better vocabulary and no
engine; we have the engine and no vocabulary.** The trade is one-directional: **keep graphify's decay and
add `forgetReason` as the field it must write.** A half-life that silently stops surfacing a fact cannot
answer "why doesn't my app do that any more"; a reason string turns a decay artefact into an auditable
statement, for one column. OM-48 survives — as *an idea from their schema*, not a mechanism observed
working.

### 3.2 What is retrieved: one predicate, tri-state, failing open to visible

Both retrieval paths use the same filter (`apps/mcp/src/server/format.ts:79-81`,
`tools/list-memories.ts:51`):

```ts
entry.isForgotten !== true && entry.isLatest !== false
```

Written `!== true` / `!== false` rather than `=== false` / `=== true`, so **`null` and `undefined` count
as active and visible.** For a memory store that is right: missing metadata should not hide a fact a user
gave you. It is the exact opposite of gstack's provider default (OM-9, *"callers that don't say get
`write` — fail-closed"*), and both are right because the cost of the wrong answer points the other way.
**Layer A should state the same rule: an intake field with missing or unreadable provenance is shown, not
suppressed — while Layer D's `offerable`, where a wrong "yes" ships a component, keeps failing closed.**
Write both down next to each other; they look inconsistent until the asymmetry is named.

The presentation vocabulary is three closed words — `Latest` · `Superseded` · `Forgotten`
(`node-hover-popover.tsx:598-604`) — with `forgetReason` rendered beneath as `Reason: …` when present and
a bare `Forgotten` when it is not (`:563-582`). **Layer F needs exactly this for spec fields a directed
change superseded**; what reading the component adds to OM-48 is that **the reason is optional in the type
and the UI degrades to a bare label**. Requiring a reason would mean fabricating one or blocking.

### 3.3 The version chain: cycle-guarded, repaired at read, silently linearised

`canvas/version-chain.ts`, 106 lines, does three things worth naming.

**It walks both directions with one `visited` set** (`:48-75`) — backward to the root via
`parentMemoryId`, forward via a `childrenMap` built in `rebuild()` — so a corrupted parent pointer that
forms a cycle terminates instead of hanging. OM-38's cycle check, applied to a chain.

**It repairs version numbers at read time** (`:83-89`):
`version = (Number.isFinite(m.version) && m.version > lastVersion) ? m.version : lastVersion + 1`. A
stored version that is not strictly increasing is silently renumbered for display. **Do not copy this.**
It enforces the right invariant in the wrong place: repairing it in the renderer means the stored data
stays wrong indefinitely and every other consumer sees the wrong thing.

**And it silently drops branches.** The comment is explicit (`:59-62`): *"Version chains are linear (each
memory has one parent), so we follow the first child at each step. If branching occurs, only the first
branch (by document order) is included."* Two children means one is invisible, with no marker.

**This lands on Layer F.** A branch is what two directed changes made from the same spec version produce —
the design window's ordinary concurrency case. **A version model for Layer A/F must forbid branching at
write (one latest per root, enforced) or represent it; if it linearises for display it must say so in the
display.** "First by document order" is not a merge policy.

One thing done right: a chain of length ≤ 1 returns `null`, not a one-element array (`:80-81`), because
*"a standalone v1 with no children is not useful"*. Same `null` vs `[]` discipline as OM-10, third project.

### 3.4 Read and left

`ClaudeMemoryTool` (`packages/tools/src/claude-memory.ts`, 633 lines) maps Anthropic's memory-tool
commands — `view` · `create` · `str_replace` · `insert` · `delete` · `rename` — onto document CRUD, gating
each on `isValidPath()` (`:616-622`): `path.startsWith("/memories/") || path === "/memories"`, and
`!path.includes("../") && !path.includes("..\\")`. **A prefix check plus a two-entry substring denylist**,
with no path resolution — the shape that misses encoded and trailing forms. Layer E's sandbox will expose a
file surface to a generated app; **resolve-then-verify-prefix, not match-then-deny-known-bad**. Third
instance in two passes of a denylist standing where canonicalisation belongs (OM-1 for prompts, §2.5 for
queries, this for paths).

`canvas/renderer.ts` (1,017 lines) is a hand-rolled canvas renderer, `tools/src/{openai,vercel,mastra,voltagent}/`
are SDK middlewares, and `apps/web` is the bulk of the 1,160 files. `references/architecture.md:203-244`
describes retrieval — query embedding, cosine similarity, a `chunkThreshold: 0.5` filter, relationship
expansion, then ranking by *"similarity score, recency, static vs. dynamic priority, relationship strength,
metadata matches"*. **That five-signal ranking is its only genuinely interesting claim and there is no code
here to check it against.** The LongMemEval / LoCoMo / ConvoMem numbers remain asserted and unreproduced.

---

## 4 · repomix's compression, taken seriously

*`f465ad9`, 2026-08-23. `LICENSE` is the MIT body with no title line — see the licence table. Read
line by line: `treeSitter/parseFile.ts`, `parseStrategies/{BaseParseStrategy,TypeScriptParseStrategy}.ts`,
`metrics/tokenCountCache.ts`. Searched: the rest of `treeSitter/` (1,375 lines across 11 files plus 19
query files), `src/core/{file,output}`, `src/config/configSchema.ts`.*

**The verdict is not reopened.** *"Packing, the anti-pattern with a CLI"* is correct, and the code makes
it more so: **there is no token budget anywhere in this repository.** `configSchema.ts` has
`topFilesLength` (default 5, `:140`), which only *reports* the largest files
(`outputGenerate.ts:241-246`) — and no `maxTokens`, no cap, no elision-when-over. Repomix measures the
size of the whole and never bounds it. That is the definition of packing.

But something that must summarise a repository into a budget has solved sub-problems we face, and
`--compress` solved three properly and one badly. All four are **Layer D** findings, because a
`Contract` is a signature without a body and Layer D's catalog is a signature-only view of a corpus
(OM-51).

### 4.1 The dedup pass claude-context does not have — 21 lines, and it is the whole difference

§2.3 showed claude-context indexing `export class Foo { bar() {} }` three times. Repomix hits the
identical problem — tree-sitter queries capture nested definitions — and solves it in two stages.

**Stage 1, `filterDuplicatedChunks()` (`parseFile.ts:157-178`): group captures by `startRow`, keep only
the longest content per row, re-sort by row.** Nested captures beginning on the same line are exactly the
`export_statement` / `class_declaration` collision; taking the longest keeps the outermost.

**Stage 2, content dedup.** `BaseParseStrategy.checkAndAddToProcessed()` (`:75-82`) holds a
`Set<string>` of trimmed content per file and returns `false` on a repeat.
`TypeScriptParseStrategy` adds a second key — `processedChunks.add('func:' + functionName)` (`:80-93`) —
so an overload or re-declaration of the same name is suppressed even when the text differs.

**Take the shape for Layer D's catalog index build: signature extraction over a nested AST must dedup by
containment (keep the outermost) and then by content identity, and both passes must be explicit.** That
is the entire distance between §2.3's triplicated index and a clean one — **two projects met the same
problem in the same year; one wrote the pass and one did not.**

### 4.2 The elision is marked, and that is not cosmetic

`CHUNK_SEPARATOR = '⋮----'` (`parseFile.ts:36`), joined between merged chunks (`:108`). Every place a
body was removed carries a visible marker.

**A signature-only view that does not mark its elisions is a lie to the reader**, and the reader here is a
model that would otherwise infer a class has no methods between two signatures. Layer D's catalog entries
and Layer C's `PackageInterface` (*"names and shapes, not implementations"*, `plan.py:47`) are both
signature views and neither has an elision marker in its rendered form. **One sentinel token at every
discarded body**, and an entire class of wrong inference leaves every build prompt that carries a catalog.

`mergeAdjacentChunks()` (`:180-213`) merges chunks whose rows are literally adjacent
(`endRow + 1 === current.startRow`) so consecutive signatures do not each get a separator — the marker
means "something was removed here", not "a new chunk starts". That distinction is why it is informative.

### 4.3 Best-effort degradation, with the residual failure published

`parseFile()` never throws (`:38-43`, `:110-126`): unsupported language, parse failure, or a WASM runtime
abort all return `undefined` and the caller uses uncompressed content. Two details lift this above
ordinary error handling.

**The singleton is assigned only after `init()` succeeds** (`:129-140`), with the reason written down:
*"Otherwise a failed init would leave an uninitialized parser cached for the rest of the worker's
lifetime, so every subsequent file would throw 'not initialized' and silently lose compression."*
Caching a failed initialisation is a bug Layer E meets the first time a sandbox toolchain fails to start.

**And they publish the failure they did not fix** (`:114-120`): a hard WASM abort *"can leave this
worker's shared tree-sitter runtime degraded… later files routed to the same worker may also fall back to
uncompressed output. This is bounded per worker and surfaced by the warning below. Recovering the runtime
would require recycling the worker, which is out of scope here."*

**This is OM-8's standard — publish your error band — met for a degradation path**, and the second
sighting of a mechanism that states its residual failure, its bound, and why the bound is acceptable.
**Layer E's relay should degrade and document the same way**: degrade the package, name what is now
unreliable, bound the blast radius — rather than failing the build or pretending nothing happened.

### 4.4 The signature boundary is found with string arithmetic — and it is measurably wrong

The one part done badly, and the part Layer D would be copying. `TypeScriptParseStrategy` has the capture
node — with `startPosition`, `endPosition` and every child range tree-sitter provides — and then locates
the end of a function signature by **scanning lines for one containing `)` that ends with `{`, `=>` or
`;`** (`findSignatureEnd`, `:99-107`; falls back to `startRow` alone if none matches), and truncates that
line at **`indexOf('{')` or `indexOf('=>')`** (`cleanFunctionSignature`, `:109-122`). `indexOf` — not the
last, not the balanced one.

I re-implemented both functions exactly and ran four realistic TypeScript signatures through them:

| Input first line | Extracted "signature" |
|---|---|
| `export function pick<T extends { a: number }>(x: T): number {` | `export function pick<T extends` |
| `function f(opts = { retries: 3 }): void {` | `function f(opts =` |
| `export const g = (a: number): number => {` | `export const g = (a: number): number =>` ✓ |
| `function h(` ⏎ `  a: number,` ⏎ `  b: string` ⏎ `): void {` | full signature ✓ |

**A generic constraint containing a brace, and a default parameter containing an object literal, both lose
the entire parameter list and the return type.** Two of four common shapes silently produce a signature
with no parameters — which in a signature-only view is not a degraded answer but a wrong one.

**The rule for Layer D: a signature view is cut at the parse tree's own child boundaries — the node range
of the body — never by string-searching the source line.** They had the AST in hand and used `indexOf`.
Whatever produces a catalog entry from a component's source takes ranges from the parser, and there is a
test with a brace inside a type.

### 4.5 One mechanism for Layer G, from the token cache

`src/core/metrics/tokenCountCache.ts`. The cache key is `` `${encoding}:${byteLength}:${md5_16}` ``
(`:327-331`) — **the tokenizer identity is part of the key** — with the byte length included because it
*"makes the key tolerant to MD5 collisions on differently-sized inputs and keeps the digest portion short
(16 hex chars / 64 bits)"*. There is a `CACHE_VERSION = 1` (`:11`) to bump *"when the on-disk format
changes incompatibly so stale caches are discarded silently"*, a `MAX_CACHE_ENTRIES = 100_000` FIFO cap
applied **both on insert and again on save** — *"defence in depth — the file cannot exceed the cap even if
the eviction logic ever breaks"* (`:13-21`) — and a monotonic `revision` counter snapshotted before a save
so that *"`setCached` calls that ran during an in-flight save"* do not lose their persistence guarantee
(`:44-50`).

**Two things follow.** The `revision` counter is precisely the durability discipline §2.2 found
claude-context getting wrong — writes landing during an in-flight persist must not be marked clean. Same
bug class, correct here and incorrect there, in the same month.

And the key **sharpens OM-50**: supermemory keeps the producing model *beside* the value
(`memoryEmbeddingModel`, plus a second column to migrate through); repomix puts the producing tokenizer
*in the key*. **In the key is strictly better** — a stale entry becomes unreachable rather than
mislabelled, no migration column is needed, and two generations coexist without a schema change.
**Layer G's rule: every cached or derived value is keyed by `(content hash, producer identity, format
version)`, not merely annotated with them.** One line, and supermemory's migration problem stops existing.

---

## 5 · Verdict table — item, layer, take/adapt/leave, what must be true

Numbered `P2-n` to distinguish them from `OTHERS-MINED.md`'s OM-1…OM-55, which stand unchanged
except where a row below says otherwise. "What must be true" is the condition that makes the item
worth doing — the thing to check before opening a PR, not after.

| # | Item | Source | Layer | Verdict | What must be true |
|---|---|---|---|---|---|
| P2-1 | Package lifecycle enum + declared transition table; a status report that matches no transition **throws** | task-master `workflow-orchestrator.ts:47-72,:139` | **E** | **take** | the executor reports transitions, not states; the table is data, not `if`s |
| P2-2 | The terminal state is reachable only by an explicit call — no auto-advance into "done" | same, `:277` | **E** | **take** | there is exactly one call site that can mark a build complete |
| P2-3 | Arithmetic coherence gate on reported test results: sum check, RED≥1 failure, GREEN≥1 pass, count-regression warning | task-master `test-result-validator.ts:59,:85,:91,:121,:127,:137` | **E**, with **C** | **take — best item in that repo** | the criterion is `observed_by` something that reports counts; today 8/27 criteria are `unsupported` and 0 are `interaction` (Layer C §1.1) |
| P2-4 | `previousTestCount` is **required**, not optional | same, `:132-140` | **E** | **adapt** | a check that is off by default is off |
| P2-5 | "Already satisfied" is a first-class outcome at both ends — C may emit a no-build package, E may close one without change | task-master `:172-206` + OM-37 | **C, E** | **take** | Layer D's assembly match and this outcome are unified as one state, not two |
| P2-6 | The count is computed by code; the model fills the content | task-master `scope-adjustment.js:210-274` | **C** | **take the structure, none of the constants** | the inputs are the architecture's own measurements — attaches to Layer C §3.2 |
| P2-7 | Preservation is an **allowlist** — only `pending` regenerates; unknown statuses are preserved | same, `:32-45` | **C** | **take** | Layer C §3.4's plan delta names the statuses it *will* discard, never the ones it won't |
| P2-8 | A delta that changes nothing is a no-op with a distinguishable return, not an empty regeneration | same, `:201-208` | **C** | **take** | same `null` vs `[]` discipline as OM-10 |
| P2-9 | Closed set of sentinel completion tags with a named reason; `blocked` distinct from success and from error | task-master `loop.service.ts:289-305`, `entropy.ts:42` | **E** | **take** | the vocabulary of reasons is enumerated per loop kind; the harness parses, no one reads prose. Completes OM-30 |
| P2-10 | Finish-what-is-started before starting new work, stated as policy | task-master `find-next-task.js:52-97` | **E** | **adapt** | only if Layer E ever runs packages concurrently; state the WIP rule rather than inheriting it from plan order |
| P2-11 | A prompt/`Playbook` registry whose schema fails to compile must be **fatal at startup** | task-master `prompt-manager.js:62-71` — *defect* | build process | **take the inverse** | no `validatePrompt = () => true` fallback path exists anywhere |
| P2-12 | Variant conditions are declarative predicates with explicit integer precedence — never `new Function`, never file order | task-master `prompt-manager.js:252-285` — *defect* | build process, **B** | **take the inverse** | conditions are provably disjoint or precedence is a field. Qualifies OM-42 |
| P2-13 | Content hash + persisted snapshot + **three-way** `{added, removed, modified}` set diff | claude-context `synchronizer.ts:164-188` | **D** | **take** | the three categories drive three different index operations. **Corrects OM-45: take the diff, not the Merkle DAG — it is two levels deep and saves nothing** |
| P2-14 | The staleness snapshot is keyed by the artefact's identity, not its filesystem path | claude-context `:25-33` | **D** | **take** | relocating the library does not force a full rebuild |
| P2-15 | The snapshot is written **after** the derived artefact is durable, and from the set that **succeeded** | claude-context `:150-157` + `context.ts:39-48` — *their own bug, half-fixed* | **D** | **take — hard requirement** | a crash lands in "still stale"; there is a named test, as OM-4 has for the other direction |
| P2-16 | `mkdir`-as-mutex, owner token recorded, 10-min stale reclaim, **skip the cycle rather than queue** | claude-context `mcp/src/sync.ts:98-134` | **D, E** | **take** | the rebuild is periodic, so a missed round is cheaper than a queue of rounds |
| P2-17 | Identifiers derived from user text are query **parameters**, never interpolated | claude-context `context.ts:504-521` — *defect* | **D, G** | **take the inverse** | the same boundary OM-1 draws for prompts, drawn for queries and (§3.4) for paths |
| P2-18 | A vector index anywhere on the `Contract` deciding path | claude-context, whole | **D** | **leave — reaffirmed** | nothing changed; `satisfied_by` stays two subsets and an equality |
| P2-19 | How to cite their headline number | claude-context `evaluation/` | **D** | **record** | it is *end-to-end edit-localisation F1 (0.40 → 0.40), dispersion computed but unpublished*, not "retrieval quality unchanged" |
| P2-20 | `isStatic` — a second authority bit, orthogonal to `isInference`: may time erode this field? | supermemory `schemas.ts:264`, `architecture.md:172-184` | **A** | **take** | `FieldMeta` gains one boolean; Layer F consults it before revising a field |
| P2-21 | `forgetReason` as a field graphify's half-life decay must write | supermemory `schemas.ts:266` | **A, F** | **adapt — ours is the engine** | **their forgetting has no engine: `forgetAfter` is read by exactly one border-colour function and nothing sets `isForgotten`.** Keep our decay, take their vocabulary |
| P2-22 | Tri-state "active" predicate that fails **open to visible** for intake — and stays fail-closed for `offerable` | supermemory `format.ts:79-81` vs gstack OM-9 | **A, D** | **take both, written next to each other** | the asymmetry is named: unknown provenance is shown, unknown quality is withheld |
| P2-23 | Closed three-word status vocabulary — Latest · Superseded · Forgotten — with an **optional** reason and graceful bare label | supermemory `node-hover-popover.tsx:563-604` | **F** | **take** | never block or fabricate to satisfy a reason field. Completes OM-48 |
| P2-24 | Version monotonicity is enforced at **write**, never repaired at read | supermemory `version-chain.ts:83-89` — *defect* | **A, G** | **take the inverse** | a violation is findable; the renderer is not the place invariants live |
| P2-25 | Branching in a version chain is either forbidden at write or represented — never silently linearised to "first child by document order" | supermemory `version-chain.ts:59-62` — *defect* | **F** | **take the inverse** | two directed changes from one spec version is the design window's normal case, not an edge case |
| P2-26 | Path validation is resolve-then-verify-prefix, never match-then-deny-known-bad | supermemory `claude-memory.ts:616-622` — *defect* | **E** | **take the inverse** | third denylist-where-canonicalisation-belongs in two passes |
| P2-27 | Signature extraction dedups twice: by containment (keep outermost per start row), then by content identity | repomix `parseFile.ts:157-178`, `BaseParseStrategy.ts:75-82` | **D** | **take** | 21 lines; it is the entire difference between §2.3's triplicated index and a clean one |
| P2-28 | Every discarded body leaves a visible elision sentinel; adjacent signatures are merged so the marker means "removed", not "next chunk" | repomix `parseFile.ts:36,:108,:180-213` | **C, D** | **take** | `PackageInterface` and catalog entries both render one. A signature view without it misleads by omission |
| P2-29 | Degrade best-effort, and publish the residual failure, its bound, and why the bound is acceptable | repomix `parseFile.ts:38-43,:110-126` | **E** | **take** | second instance of OM-8's standard; applies to the relay and every sandbox tool |
| P2-30 | Never cache a failed initialisation — assign the singleton only after `init()` returns | repomix `parseFile.ts:129-140` | **E** | **take** | one retry path, no permanently-poisoned worker |
| P2-31 | Cut a signature at the parse tree's own child ranges, never by `indexOf` on the source line | repomix `TypeScriptParseStrategy.ts:99-122` — *defect, reproduced* | **D** | **take the inverse** | two of four common TypeScript shapes lose their whole parameter list (§4.4 table). There is a test with a brace inside a type |
| P2-32 | Cache/derive keys are `(content hash, producer identity, format version)` — the producer is **in the key**, not beside the value | repomix `tokenCountCache.ts:11,:327-331` | **G** | **take — sharpens OM-50** | stale entries become unreachable rather than mislabelled; supermemory's dual-column migration stops being necessary |
| P2-33 | The four repositories as dependencies: repomix as a tool, task-master's code or prompt text (Commons Clause), supermemory the service, claude-context the MCP | all four | — | **leave, as decided** | unchanged by this pass |

**Three items are corrections to `OTHERS-MINED.md` rather than additions**, and they are the ones to
carry forward: **P2-13** (OM-45 credited a Merkle DAG that does no work), **P2-21** (OM-48 credited a
forgetting mechanism that does not exist in the repository), and **P2-19** (OM-44's F1 figure needs
its real definition attached). None of them changes a verdict; all three change what we would be
claiming if we cited these repositories to justify a decision.
