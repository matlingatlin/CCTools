# The skipped repositories — what a real pass finds

*Written 2026-08-26. Eight repositories cloned to disk and read as files. All metadata below
came from the GitHub API on 2026-08-26 — stars, archived flag, last push and licence — not from
the earlier scan, which was right about three of them and wrong about one in a way that matters.*

`docs/TOOLING-SCAN.md` §1 gave each of these one line and a **skip**. Those verdicts were about
*adoption*: whether to take the whole thing as a dependency. On that question they hold, and
nothing here reverses one. **This document does not re-decide adoption.** It does the pass that
was never done — opening the files and taking the mechanisms.

---

## What I read, and what the original one-line verdicts got right

| Repo | Cloned at | Last push | Archived | Licence | What I actually read |
|---|---|---|---|---|---|
| `garrytan/gstack` | `ad84005` | 2026-08-26 | no | MIT | 61 `SKILL.md` (62,872 lines), `lib/` (8,612 lines of TS), `scripts/question-registry.ts`, `scripts/one-way-doors.ts`, 8 of 374 test files |
| `obra/superpowers` | `b36e082` | 2026-08-19 | no | MIT | all 14 `SKILL.md`, `skills/*/` references, `hooks/`, `.claude-plugin/` |
| `eyaltoledano/claude-task-master` | `c0c98d3` | 2026-04-28 | no | **NOASSERTION** | `apps/`/`packages/` task model, the `parse-prd` and `expand-task` prompt templates, `tasks.json` schema, dependency validation |
| `zilliztech/claude-context` | `6fc318b` | 2026-07-14 | no | MIT | splitter, merkle sync, hybrid-search path, MCP tool surface, `evaluation/` |
| `supermemoryai/supermemory` | `9652478` | 2026-08-26 | no | MIT | memory schema, forgetting/decay path, container model, `skills/` |
| `yamadashy/repomix` | `f465ad9` | 2026-08-23 | no | MIT | `src/core/`, compress/tree-sitter path, output styles |
| `multica-ai/andrej-karpathy-skills` | `2c60614` | 2026-04-20 | no | **none in repo** | every file — there are 9 |
| `gsd-build/get-shit-done` | `bdcaab2` | 2026-05-31 | **yes** | MIT | `README.md`, `agents/`, `hooks/`, phase files |

**Star counts, for the record and for nothing else:** gstack 129,823 · superpowers 278,002 ·
karpathy-skills 207,634 · get-shit-done 64,638 · supermemory 29,083 · repomix 28,070 ·
task-master 28,022 · claude-context 12,446. Not one of these numbers appears as evidence below.

### The scorecard on the original verdicts

- **`repomix` — right, and right for the stated reason.** §6 confirms it in a paragraph.
- **`get-shit-done` — right.** Archived is archived. §6.
- **`andrej-karpathy-skills` — right, and the file is even thinner than reported.** §6.
- **`supermemory` — right as an adoption call, incomplete as a reading.** Its *model* of memory
  has two ideas we don't have. §5.
- **`claude-context` — right that it duplicates graphify for *code*. Wrong to stop there**, because
  Layer D does not search code, it matches `Contract`s, and the interesting part of claude-context
  is not the vectors. §4.
- **`claude-task-master` — right for stage 4 of our build process, and the wrong question.** Read
  against Layer C it has one schema decision and two prompt artefacts worth taking. §3.
- **`superpowers` — the verdict was right and the reading was 1/14th complete.** §2.
- **`gstack` — the verdict is defensible, the reason given is false.** "Personas, not decision
  procedures" does not survive contact with the files. §1.

---

## 1 · gstack

**The one-line reason was wrong, and it is worth being precise about how.** `TOOLING-SCAN.md` says
*"23 tools cast as CEO, Designer, Eng Manager, QA — personas, not decision procedures."* On disk
there are **61 skills, not 23**; the persona framing belongs to about six of them (the
`plan-*-review` family, `cso`, `office-hours`); and underneath sits **8,612 lines of TypeScript in
`lib/` and 374 test files** implementing things this project has been designing from scratch. The
strategic call — do not adopt a competing harness — stands, for the reason ECC was refused. The
stated reason was a description of the README.

Every `SKILL.md` is generated from `SKILL.md.tmpl`, which injects ~865 lines of shared preamble into
all 61, so a 1,646-line `spec/SKILL.md` is ~780 lines of actual procedure. Persona words live in the
*description*; the body is phases, gates, exit codes and refusals.

### 1.1 The deterministic gate, done at the sink — Layer A, and Layer E

`spec/SKILL.md` Phase 4.5b is the closest thing I have read to what Layer A's gate must be, and it
beats our specification on three points.

**Scan the bytes that will actually be sent, from the file that will actually be sent:**
*"Scan-at-sink on the EXACT bytes that will be sent: write to a temp file, scan that file, pass the
SAME file downstream. Never scan a string then re-render it."* Our gate validates a `Spec` object; a
later stage renders a prompt from it. The serialisation between them is unchecked. One `mktemp`,
scanned and passed, closes that by construction.

**Three tiers, distinct outcomes, no override on the top one.** Exit 3 (HIGH — credentials) blocks,
does not dispatch, and *does not persist the body anywhere*. Exit 2 (MEDIUM — PII, legal, internal)
asks per finding, with sterner wording and no batch-acknowledge when the repo is public. Exit 0
surfaces LOW as a non-blocking FYI. And *"`--no-gate` skips the codex score only; redaction always
runs, no flag disables it."* Ours is binary; a middle tier that asks per finding is more usable and
no less strict, provided the top tier is unskippable. Their visibility resolution has the same shape
— `local config → gh → glab → unknown` — and **`unknown` is treated as public-strict**: unknown
means strictest.

**The audit-sink invariant is a named test:** *"when the scan BLOCKS (exit 3), the raw spec must NOT
be persisted anywhere downstream — no archive write, no transcript log, no codex dispatch.
`spec-quality-gate-secret-sink.test.ts` enforces this."* A blocking gate that logs its rejected
input has leaked. We have written the rule and not the test.

### 1.2 `datamark()` — the render boundary, and the strongest single finding here

`lib/gstack-decision.ts` stores decisions as free text and passes every read through `datamark()`
before it reaches a model: strip C0/C1 and U+0085/2028/2029, neutralise markdown code fences and
`---` banner sentinels, and insert a zero-width space inside `<|` / `|>`, inside
`<system>`/`<user>`/`<assistant>`/`<tool>`, and inside `Human:`/`Assistant:`/`System:`/`User:`. The
commentary is the finding: *"Write-time `hasInjection` is a denylist; this is the render-boundary
defense-in-depth that also covers `--all`/snapshot reads and records written before a pattern
existed."*

**This is exactly Scio's shape and we have no such boundary.** Layer A stores user prose with
provenance. Layer B interpolates a `Playbook` into every build prompt. Layer F turns free-text
markings on a preview into directed change. All three store text a person wrote and re-render it
*into a prompt*; our defence is write-time validation, which is a denylist, and denylists do not
cover records written before a pattern existed. Ten lines, applied at every such point. The
write-time counterpart is worth taking too: free text is injection-checked **and** redact-scanned on
write, with HIGH-tier secrets rejected — a user pasting an API key into an intake answer is not
hypothetical for an app builder.

### 1.3 The one-way door registry — Layer A

`scripts/question-registry.ts` is 56 typed entries: stable kebab id, skill, category (`approval` ·
`clarification` · `routing` · `cherry-pick` · `feedback-loop`), **`door_type`**, stable option keys,
optional signal key. `one-way` = destructive ops, architecture/data-model forks, scope adds over a
day, security or compliance choices — **always asked, regardless of any user preference**. `two-way`
= suppressible by explicit preference. Preferences, logs and tuning all key off the registered id.

Two details to steal verbatim. *"`options` is a short list of stable option keys. UI labels can vary;
keys must stay the same so preferences survive wording changes"* — if Layer A's provenance records
the label the user saw, re-wording a question orphans every prior answer. And
`scripts/one-way-doors.ts` is only the *secondary* check, a keyword regex used when a question has no
registry id, because *"prose-parsing is too weak to be the PRIMARY safety gate — wording can
change."* Their own review said the prose check was weak; they kept it as a backstop rather than
promoting it. Copy the layering, not just the list.

### 1.4 The catalog budget — Layer D, where we are currently worst

`test/catalog-budget.test.ts` solves the exact problem the brief names. gstack's discovery surface is
the sum of every skill's frontmatter `name` + `description` — what every host loads every session:

- Budget **1,150 token-equivalents**; measured 2026-08-12 at **4,420 bytes / 1,105
  token-equivalents** over 53 skills plus the router alias. Headroom ~4%. Dominant entry named.
- Per-entry cap **260 bytes**, with the rule that makes it stick: *"A description that needs more
  than 260 bytes is a body paragraph, not a catalog entry."*
- A **ratchet protocol** printed in the failure message: re-measure, update the constant *and* the
  derivation comment — ref, date, value, which entry moved it — **in the same commit**.
- *"Import-free by design… this test must survive generator refactors."*

A component's catalog entry is its `Contract` summary; the whole catalog is what a build prompt
carries when matching. Today that is unbounded and grows with every component, so **Layer D gets more
expensive as it gets more useful** — the wrong gradient. Take all four parts; the same-commit ratchet
is the one most teams skip and the one that stops a budget being raised silently.

`lib/context-bill.ts` (1,017 lines) is the instrument: per-content-class byte-per-token divisors
(`frontmatter` 3.99, `skillmd` 4.21, `reference` 4.15, `artifact` 3.67, `legacy` 3.47) fitted to real
`count_tokens` calls, because *"measured bytes-per-token spans 2.36 to 4.72 and the spread is largely
structural"* — one divisor charges some ledgers ~19% under. Classes cut mean per-file error 11.1% →
7.4%. They also publish what classes do **not** fix (worst case near 40% on heterogeneous files, so
*"use `--exact` when a single file's number has to be right"*) and that the divisors are
tokenizer-specific and expire on the next model. **A cost estimator that publishes its own error band
and its expiry condition is the standard Layer E's spend ceiling should meet**; ours reports a number
with neither. The `--exact` path adds one more rule: it writes an egress receipt *before* the POSTs,
and if the receipt cannot be written it **degrades to the offline estimate with a warning rather than
sending unrecorded**.

### 1.5 The provider contract — Layer D and Layer G

`lib/code-intelligence/contract.ts`, 201 lines, answers "how do we depend on an optional external
retriever" — which Layer D faces the moment the component library outgrows a file.

Four **required** capabilities (`register_source`, `refresh`, `search`, `status`), three **optional**
ones a provider advertises (`add`, `delete`, `export`); deliberately repo-oriented because *"a
document-CRUD-required contract would misrepresent whole-repo code-search and code-graph tools."*
Ops are classed `read` or `write` for a per-remote trust-tier veto, and **"callers that don't say get
`write` — fail-closed."** `local: true` means no content leaves the machine and is a property of the
provider, not a config flag; non-local providers need explicit per-repo `consented` on
`register_source`/`refresh`/`add` **and on `search`** — *"the search query text is repo-derived
content."* That last clause is the one people forget. The whole contract is optional:
`resolveCodeProvider()` returns `null` and callers degrade to grep. *"Never a dependency, always an
enhancement."*

`lib/gstack-decision-semantic.ts` applies the same policy to memory — the reliable core has zero
imports of the optional engine, the optional module never throws and never hangs (10 s timeout), and
every failure returns `null` so the caller shows deterministic file results. The `null` vs `[]`
distinction is exact and worth copying: `null` = the engine was unavailable, **degrade**; `[]` = it
ran and genuinely found nothing, *"also honest, and distinct"*. Layer D's matcher needs the same
split between "no component matched" and "the matcher didn't run". They also refuse to search
unscoped when the curated source cannot be resolved, because *"an unscoped search pulls code/doc
corpora that would be mislabeled as 'related decisions'"* — precisely Layer D's failure mode, a
component returned as a `Contract` match because its prose was similar.

### 1.6 Two mechanisms for our build process, and three rules for the `Playbook`

**Tiered, cost-scoped tests over model behaviour.** `test/helpers/e2e-gate.ts` defines one predicate
(`EVALS=1 && EVALS_TIER === tier`) for `gate` (free, per-PR, structural) versus `periodic` (paid,
runs a real agent and asserts what it *did*). `carve-section-loading.test.ts` is *"the behavioural
proof that a REAL agent actually Reads each carved skill's required sections at runtime — not just
that the skeleton structure looks right."* One `test()` per skill so a hung run fails one case, and
`GSTACK_CARVE_SKILL=<name>` scopes the paid run to the changed skill — the answer to "behavioural
evals are too expensive to run per PR" is: don't run all of them.

**Registry membership *is* the test.** `test/helpers/carve-guards.ts` is a pure data module with no
runtime imports, consumed by five test files, one of which asserts the registry set **equals the
filesystem set**. "Registered ⇒ asserted" becomes structural — a carved skill cannot exist
unguarded. `docs/next/SKILLS.md` worries about skills shipping without evals; this makes that state
unrepresentable, for one data file plus one equality test.

Three preamble rules are refusals rather than encouragements and belong in our `Playbook` verbatim.
**Claimed limitations need evidence:** *"State one only with the verbatim error, the documented
statement, or a live probe in hand… When a cheap probe settles the question, run it BEFORE asking the
user anything or declaring a step blocked"* — Layer E will generate "this can't be done" a hundred
times a day. **The pipeline-failure distinction:** an envelope reading "(empty body)" means zero
matches; **no envelope at all means the pipeline failed — that is not "0 matches"**, with five named
failure modes and the exact message for each. That is `GRAPHIFY-SURFACE.md`'s *"check what a tool
wrote, not what it printed"* written as a procedure a model can follow. **The confusion protocol:**
for high-stakes ambiguity only — architecture, data model, destructive scope — STOP, name it in one
sentence, offer 2–3 options, ask; explicitly *not* for routine work, so it cannot become a stall.

### 1.7 What I read and am leaving

The `plan-*-review` family (4,700 lines across four files) — here the original verdict holds. The
four-mode structure of `plan-ceo-review` (SCOPE EXPANSION / SELECTIVE EXPANSION / HOLD SCOPE / SCOPE
REDUCTION) is a real decision procedure, but for *a human's product plan*, and its content is taste.
`OPERATING-MODEL.md` §2.1 rejects this shape and should keep rejecting it.

The `gbrain:` frontmatter block — declarative context queries (`kind: filesystem`, `glob`, `sort`,
`limit`, `render_as`) that pre-load context before the model runs — is a good idea I am recording and
not taking: it is coupled to their hosted brain, and Layer B's `Playbook` is static by design.

The 865-line generated preamble in all 61 skills is the anti-pattern their own `context-bill` exists
to measure. Both are true at once, and the second is the interesting one: they built the instrument
that indicts the design.

---

## 2 · superpowers, past `writing-skills`

*MIT, v6.3.0, 278,002★, pushed 2026-08-19, cloned at `b36e082`. 14 skills, 7,539 lines of markdown.
Its entire runtime footprint is one hook: `SessionStart` on `startup|clear|compact`, synchronous.
A 278k-star project ships one hook — worth noting on its own.*

`TOOLING-SCAN.md` §4 read one skill of fourteen and got the right answer from it: take the
baseline-first method, do not install the plugin, because `brainstorming`, `test-driven-development`
and `writing-plans` collide with skills we already have. **That call stands.** What it missed is that
the three "colliding" skills are the three most useful to *read*, precisely because they collide:
they are another attempt at problems we have already specified, and on several points theirs is
better.

### 2.1 `writing-plans` is a Layer C specification, and it has our contract block

Layer C turns architecture into packages with contracts and acceptance criteria. Their task template
carries this:

```
**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]
```

The *rationale* is what to take. The contract exists because the implementer is context-isolated —
derived from the execution model, not from style. Our contracts are justified as "what a package
promises"; theirs as "the only channel through which a package learns its neighbours' names". The
second is stronger, and it implies a validation rule we lack: **every `Produces` must be `Consumed`
by some package and every `Consumes` must be `Produced` by one** — a bipartite completeness check.
Their `Self-Review` does it by eye (*"A function called `clearLayers()` in Task 3 but
`clearFullLayers()` in Task 7 is a bug"*); Layer C can do it mechanically.

**`## Global Constraints` in the plan header** — the spec's project-wide requirements (version
floors, dependency limits, naming and copy rules, platform requirements) copied **verbatim** into one
section, with the rule *"Every task's requirements implicitly include this section."* We have a
`Playbook` of house rules in every build prompt. We do not have the per-build equivalent: the
constraints that came from *this spec* and must reach *every* package prompt. Verbatim matters —
paraphrasing a version floor is how a version floor gets lost.

**The spec travels with the plan.** *"the plan argues from the spec, so the spec travels with it;
executors read both"*, and *"conflicts inside the plan resolve against it. A plan with no reachable
spec gets a ledger note saying so — rulings made without one are provisional."* That is a
conflict-resolution *order*, which Scio needs when a package contract disagrees with the Layer A
spec, and the corollary is the useful part: a build executing without a reachable spec is **marked
provisional**, not merely allowed.

**Task right-sizing by review boundary, not by size:** *"A task is the smallest unit that carries its
own test cycle and is worth a fresh reviewer's gate… split only where a reviewer could meaningfully
reject one task while approving its neighbor."* Layer C decomposes by architectural boundary; this is
a second, independent criterion producing coarser packages, and it is the one that matters for Layer
E, because a package is what a gate accepts or rejects. **A package boundary no gate can
independently reject is not a boundary.**

**The `No Placeholders` rejection list**, of which two entries we would not have written: *"'Similar
to Task N' (repeat the code — the engineer may be reading tasks out of order)"* and *"References to
types, functions, or methods not defined in any task"*. The first follows directly from isolated
execution; the second is the dangling half of the bipartite check. Both are mechanically checkable.

### 2.2 `brainstorming` — a better shape for Layer A's gate than ours

**Classify before the first question, and say the classification out loud so the human can override
it.** Three paths: *Spike* (a feasibility answer; the output is not code), *Bounded* (a scoped change
to a flow that **already exists in this repo** — *"Bounded measures the repo, not your
familiarity"*), *Architectural*. Layer A treats every request as one shape and varies only how many
fields get filled. Announcing a classification the user can correct is cheap provenance: it puts the
single biggest assumption on the record before anything is built on it.

**The one-way ratchet:** *"When in doubt between two paths, take the heavier one. The ratchet is
one-way: hidden complexity discovered mid-task upgrades the path — stop, say so, and step up. Nothing
downgrades mid-task."* An app builder discovers mid-build that a "simple" app needs auth, tenancy or
a migration constantly. One sentence of policy.

**The rule the gate turns on:** *"What scales with simplicity is the artifact, never the approval."*
Our gate is unconditional, which is right; the pressure we will actually face is to skip it for a
trivially small app. gstack reaches the same answer independently (§1.1).

**Decompose before interrogating:** *"if the request describes multiple independent subsystems…flag
this immediately. Don't spend questions refining details of a project that needs to be decomposed
first."* For a builder aimed at non-programmers this is the most common intake failure, and we have
no such check. It belongs in Layer A before field-filling and it feeds Layer C.

**The spec self-review, as four named scans** — placeholder · internal consistency · scope ·
**ambiguity: *"Could any requirement be interpreted two different ways? If so, pick one and make it
explicit."*** That last converts ambiguity into a recorded decision rather than a flag, which is
exactly what our provenance model wants: a field with a value and a note saying it was disambiguated,
not a blank field with a warning.

**The red-flag table is a distinct device** — not rules but *self-rationalizations* paired with
rebuttals ("I'll call it bounded and skip the spec" → "Reaching for a label to skip work IS the
doubt"). gstack has it, `verification-before-completion` has it, `systematic-debugging` has it: four
independent instances across two repositories is a genre. Our `Playbook` is all rules and no excuses.

**And for Layer F, unexpectedly:** the visual-companion rules. Offer it *just-in-time*, never upfront,
only the first time a question would genuinely be clearer shown than told; the offer **must be its own
message**; after acceptance decide **per question** on the test *"would the user understand this
better by seeing it than reading it?"*, with the corollary that *"a question about a UI topic is not
automatically a visual question."* Layer F is a design window and the live question is when a
conversation should move into it. That is the test, already written.

### 2.3 `subagent-driven-development` — Layer E's execution and recovery model

568 lines, and the most directly transferable single file in the eight repositories.

**The ledger, and the failure that motivates it:** *"Conversation memory does not survive compaction.
In real sessions, controllers that lost their place have re-dispatched entire completed task
sequences — the single most expensive failure observed. Track progress in a ledger file, not only in
todos."* The design: one git-ignored workspace per plan; *"Another plan's directory is never yours to
read or write"*; the ledger's **first line is its identity**; a task with a `Task <N>: complete` line
is never re-dispatched; a task whose last line is a fix round resumes at the next round; a ledger
naming a different plan is left alone; and *"After compaction, trust the ledger and `git log` over
your own recollection."* Layer E's relay has this exact bug if its state lives in the orchestrating
context, and re-running completed packages does not merely waste time — it burns the spend ceiling
and can re-emit side effects. The identity line is what makes a stale ledger safe.

**"Rulings, not stalls" — the autonomy boundary as a closed list.** *"A running plan does not wait on
a human. Conflicts, ambiguities, plan defects, a cap you would have asked to exceed — decide them…
Record every decision in the ledger as `Ruling: <what you decided> — <why> — <what it costs if wrong>`,
and keep going."* Four things stop it, and only four: an irreversible or destructive operation; a
security-sensitive action; a side effect outside this worktree that norms say you ask about first; and
a plan so broken that every path forward is a guess. The economics: *"A wrong ruling costs rework your
human partner can see and undo; a session parked on a question costs their whole day and buys
nothing."* For us the asymmetry is sharper — our user is a non-programmer who cannot answer a mid-build
architecture question at all. Take the closed stop-list and the ruling record; **the *cost-if-wrong*
field is what lets Layer F offer an undo that means something**, and it is the field everyone omits.
Note that *"a cap you would have asked to exceed"* is among the things to rule on rather than stall on.
Our spend ceiling is a hard stop; theirs is a decision with a recorded cost. Ours is probably right for
money, but the reasoning deserves confronting rather than inheriting.

**The fix-round circuit breaker.** Rounds 1–5. R ≤ 3: resume the same implementer. **R ≥ 4: fresh
implementer on a more capable model.** R = 5: the breaker trips — adjudicate each open finding, continue
unless one is load-bearing, park the rest in the ledger with rulings. A complete retry policy: bounded
rounds, an escalation ladder that changes both context and model, and a terminal state that is not
"fail". Our gates retry; they neither escalate nor have a defined give-up state.

**Model selection as a routing table.** *"Use the least powerful model that can handle each role."*
Mechanical implementation (isolated functions, clear spec, 1–2 files) → fast and cheap, and they assert
most tasks are mechanical *when the plan is well-specified* — which is the argument for investing in
Layer C. Integration/judgment → standard. Architecture and the final whole-branch review → most
capable, *"not the session default."* Reviews scaled to the diff's size, complexity and risk.

**The pre-flight scan whose output is a table, not a verdict** — the best sentence in the repository
for us:

> *"The scan's output is a table, not a verdict. One row for every pair of tasks that share a file or
> an interface: the two tasks, what one produces against what the other consumes, and what you found.
> One row for every task: whether its own text agrees with itself… 'The scan is clean' without those
> rows is not a scan you ran."*

Layer B has 11 validation rules that return pass/fail. A model asked "is this architecture
consistent?" will answer "yes" without checking. A model required to emit one row per interface pair
cannot. **Layer B's and Layer C's validators should emit an evidence table, and the absence of rows
should be a failure, not a pass.** It costs tokens and buys the only thing that makes a validation
rule real.

### 2.4 `verification-before-completion` — one row aimed straight at Layer E

The skill is an Iron Law plus a five-step gate plus two rationalization tables, and most of it
restates our `testing` skill. Two rows do not:

| Claim | Requires | Not sufficient |
|---|---|---|
| **Agent completed** | **VCS diff shows changes** | **Agent reports "success"** |
| Regression test works | Red-green cycle verified | Test passes once |

The first is Layer E's relay exactly. Our gates consume a build agent's report; a report is a claim,
the diff is the evidence. `dispatching-parallel-agents` closes on the same note — *"Spot check —
agents can make systematic errors"*. That is the third independent statement of `GRAPHIFY-SURFACE.md`'s
*"check what a tool wrote, not what it printed"*, now from a different repository about a different
kind of tool. At three sightings it stops being an anecdote and belongs in the `Playbook` as a named
rule.

### 2.5 The rest, read and left

- **`systematic-debugging`** — one rule for Layer E's gate-failure path: **after 3 failed fixes, stop
  fixing and question the architecture** — *"Each fix reveals new shared state/coupling/problem in a
  different place… This is NOT a failed hypothesis — this is a wrong architecture."* In Scio that
  signal should propagate **back to Layer B**, not be retried in Layer E. We have no such back-edge.
- **`condition-based-waiting`** — poll the condition, not the clock; 10 ms; always time out with the
  condition named in the message; getter inside the loop; documented exception for genuinely timed
  behaviour. Layer E's sandbox needs this verbatim when waiting for a preview. Take as-is.
- **`dispatching-parallel-agents`** — mechanics are harness-specific and we have them. The
  transferable part is the four-part agent brief (scope · goal · explicit constraints · specified
  output shape); our Layer C package prompts carry two of the four.
- **`test-driven-development`**, **`using-git-worktrees`**, **`executing-plans`**,
  **`finishing-a-development-branch`**, **`requesting-code-review`**, **`receiving-code-review`**,
  **`using-superpowers`** — read; nothing for a layer. One policy worth echoing in Layer E:
  discarding work happens **only** on an explicit request, never as a cleanup step.
- **`writing-skills/persuasion-principles.md`** — 187 lines arguing skill prose should use authority,
  commitment, scarcity and social proof, citing Meincke et al. (2025), N = 28,000, compliance
  33% → 72%, p < .001. **The only sourced methodological claim in any of the eight repositories**, and
  it explains the imperative register visible across all of them. Read it before writing our
  `Playbook`, with the caveat they omit: the measured outcome is *compliance*, not correctness, so
  persuasive framing makes a wrong rule get followed exactly as reliably as a right one.

---

## 3 · claude-task-master against Layer C

*28,022★, pushed 2026-04-28 — the least maintained of the eight, four months stale. Cloned at
`c0c98d3`.*

**Licence first, because it changes what "mine" can mean here.** The API reports `NOASSERTION` and
the file says why: **MIT plus Commons Clause v1.0**, withholding the right to *"Sell the Software… as
part of a product or service whose value derives, entirely or substantially, from the functionality of
the Software."* Scio is a commercial app builder whose Layer C is task decomposition — vendoring their
code or prompt text is the shape of thing that clause exists to stop. **Take the ideas, write our own
text, copy nothing verbatim.**

`TOOLING-SCAN.md` called it "wrong granularity" for our build process. Correct — as a system it is
a to-do list for a human's editor. Read against Layer C instead, four mechanisms are worth having.

**1 · Two-stage decomposition: score, then expand.** `analyze-complexity` scores each task 1–10 and
emits three fields: `complexityScore`, **`recommendedSubtasks`** *(non-negative; **0 if no expansion
needed**)*, and **`expansionPrompt`** — a prompt written by the scoring pass and carried into the
expansion pass. Layer C decomposes architecture into packages in one step, so every branch gets the
same treatment. Two things here are better: the decomposer is explicitly allowed to **refuse to
decompose** (`0`), and the depth argument is *generated per node* rather than fixed. **Take: Layer C
scores each architecture component before splitting it, and a score below the threshold produces one
package, not a forced split.** The `expansionPrompt` idea — a per-node instruction produced by the
analysis and consumed by the generator — is the cheap way to make one Layer C prompt behave
differently per component without a prompt per component type.

**2 · Cycles made impossible by construction, then checked anyway.** The generation prompt carries
a structural invariant — *"a task can only depend on tasks with lower IDs"* — which makes a cycle
unrepresentable if the model obeys. `scripts/modules/dependency-manager.js` then assumes it will
not: `isCircularDependency` (DFS over the chain), `validateTaskDependencies`, `findCycles`,
`removeDuplicateDependencies`, `cleanupSubtaskDependencies`, and a `fixDependenciesCommand` that
repairs rather than only reports. Belt *and* braces, and the braces are the interesting half.
**Layer C emits packages with contracts; a contract graph with a cycle is a build that cannot
start.** I would take both halves: the monotone-ordering instruction in the generation prompt, and a
cycle check that does not trust it.

**3 · `ensureAtLeastOneIndependentSubtask`.** A decomposition in which every unit depends on another
unit is deadlocked even with no cycle at all — nothing is startable. One function, one invariant,
and it is a real failure mode of model-generated dependency graphs. **Layer C should assert at
least one package with an empty `Consumes`.** We do not have this rule and it is a one-liner.

**4 · The model is not allowed to write fields it does not own.** From `src/schemas/base-schemas.js`:

> *"The `metadata` field (user-defined task metadata) is intentionally EXCLUDED from all AI schemas.
> This ensures AI operations cannot overwrite user metadata. When tasks are updated via AI, the
> spread operator preserves existing metadata since AI responses won't include a metadata field."*

**This is the strongest single idea in the repository and it belongs in Layer A.** Layer A records
provenance per field — who or what supplied each value. Provenance is only meaningful if a
model-authored update *cannot* silently overwrite a user-authored field, and the way to guarantee
that is not a rule in a prompt but the **absence of the field from the structured-output schema**.
The model cannot launder provenance for a field it has no way to emit. Apply it wherever Layer F's
directed change re-generates a spec: user-set fields leave the schema for that call.

**Also worth noting, and lesser:** every schema is `.strict()` (`additionalProperties: false`),
required by OpenAI structured outputs and harmlessly ignored by others — a portability note we will
want when Layer E is multi-provider. And `SubtaskSchema` enforces minimum *lengths*
(`title` ≥ 5, `description` ≥ 10, `details` ≥ 20) — a schema-level anti-placeholder check.
Twenty characters stops nothing real, but the idea of putting the placeholder guard in the **type**
rather than in the prose is right, and it is a mechanism superpowers' much better `No Placeholders`
list lacks. Do both: minimum-substance constraints in the Layer C contract type, and the rejection
list in the prompt.

**The prompt registry, for our build process rather than a layer.** `src/prompts/` holds nine
prompts as versioned JSON assets governed by three JSON Schemas (`prompt-template`, `parameter`,
`variant`): every prompt has a semver, a description, **typed named parameters** with descriptions,
and **variants selected by condition** (`expand-task` ships `default`, `research` and
`complexity-report`, chosen by what context exists). We ship a `Playbook` into every build prompt
and our prompts are string literals in code. A schema-validated prompt registry with semver and
conditional variants is the mechanism that makes a `Playbook` versionable, diffable and testable.
Take the shape; write our own schema.

**Read and left:** the MCP server, the tag/branch task-set model, `tm-profiles`' per-editor slash
commands, `apps/extension`. All are surface for a human-driven to-do list. Nothing there for a
layer.

---

## 4 · claude-context against Layer D

*MIT, 12,446★, pushed 2026-07-14, cloned at `6fc318b`. Read: `packages/core/src/splitter/`
(AST + langchain fallback), `sync/merkle.ts` + `synchronizer.ts`, `vectordb/` including the hybrid
dense+BM25 path, the MCP handlers, and `evaluation/`.*

The brief asks a precise question: **what does semantic/vector retrieval offer that a graph does
not, specifically for Layer D's component library, where matching is by `Contract`
subset-and-equality and the catalog is loaded whole per package?**

**The answer for matching is: nothing, and it would be worse.** `Contract` subset-and-equality is a
set-containment predicate. It is exact, cheap, explainable and total — for a given `Contract` there
is a determinate set of components that satisfy it. An approximate nearest-neighbour index returns a
ranked list with no notion of satisfaction, so using it to *decide* a match replaces a correct
answer with a plausible one. gstack's own note (§1.5) names this failure in the wild: an unscoped
similarity search returning results from the wrong corpus, presented as if from the right one. For
Layer D that is a component returned as a `Contract` match because its prose was similar. **Do not
put a vector index on the matching path.**

**The answer for the catalog is: something real, and it is not the vectors.** "The catalog is
loaded whole per package" is a *recall* problem, not a matching problem, and it has a standard
shape that claude-context implements the first half of and stops:

> **cheap recall over the whole catalog → top-k candidates → exact `Contract` verification of each
> candidate → match or generate.**

Only the verification step decides. The recall step exists solely so that the exact step runs on k
candidates instead of on the whole catalog. That decomposition is what Layer D needs, and it is
**independent of what implements the recall step**. Three things could: a `Contract`-shape index
(a signature over required capability names — an inverted index, no embeddings, exactly and
deterministically over-inclusive); the graph, via graphify's `query --budget`; or embeddings. The
first is the smallest and the only one that is guaranteed not to drop a true match. **Take the
recall-then-verify decomposition and implement the recall step as an inverted index over `Contract`
capability names, not as a vector search.** That is the finding, and claude-context is what made it
visible: their whole product is the recall step with no verification step, and the consequence
shows up in their own numbers.

**Their own evaluation is the strongest evidence for the original skip, and it is worth quoting
rather than paraphrasing.** 30 SWE-bench Verified instances (15–60 minute difficulty, exactly 2 file
modifications), 3 runs each, GPT-4o-mini, against a grep-only baseline:

| Metric | Grep baseline | With claude-context | Change |
|---|---|---|---|
| Average F1 | 0.40 | 0.40 | **comparable** |
| Average tokens | 73,373 | 44,449 | −39.4% |
| Average tool calls | 8.3 | 5.3 | −36.3% |

They publish this as a win, and as a cost result it is one. But read it against what we already
measured: **semantic search buys 1.65× fewer tokens and no retrieval quality; graphify's own
`benchmark` reports 26.1× on our graph** (`GRAPHIFY-SURFACE.md`). Different corpora and different
tasks, so the ratio is not a like-for-like comparison — but the *quality* column is the one that
settles it. Their mechanism, on their benchmark, does not retrieve better; it retrieves the same
and cheaper. An F1 of 0.40 is also low in absolute terms and they do not comment on it. **Adding a
vector database to buy 1.65× is not a trade Layer D should make**, and this is now a sourced
statement rather than an assumption.

**One mechanism I would take, and it is not about search at all.** `sync/merkle.ts` +
`synchronizer.ts`: per-file SHA-256 content hashes rolled into a Merkle DAG, with the snapshot
persisted at `~/.context/merkle/<md5-of-absolute-path>.json`, so re-indexing computes a hash diff and
touches only changed files. graphify already does incremental `update` and `check-update`, so we
gain nothing for the code graph. **Where it does apply is Layer D's catalog itself:** if a
`Contract` index is derived from the component library, it needs a cheap, exact staleness test —
"has anything changed, and what" — and a content-hash tree keyed by absolute path is the right one.
Small, boring, correct.

**Read and left:** `ast-splitter.ts` (270 lines, tree-sitter chunking with a langchain
character-splitter fallback) — Layer D's unit is a component with a declared `Contract`, so it is
never chunked; the whole problem this file solves does not exist for us. The Milvus dense+BM25
hybrid path — real work, and the BM25 half is the lexical recall that an inverted `Contract` index
would do better and without a service. The MCP handlers and the two editor extensions — surface.
The README's opening line now advertises a *different* Zilliz product (`memsearch`) for memory,
which alongside a four-month-stale push is worth noting for anyone tempted later.

---

## 5 · supermemory — the model, not the service

*MIT, 29,083★, pushed 2026-08-26 (today), cloned at `9652478`. The skip stands: it is a hosted
memory engine, our memory is a git repo with ADRs, and graphify's `save-result` / `reflect` already
gives us half-life decay and a corroboration threshold deterministically
(`GRAPHIFY-SURFACE.md`). Read: `packages/validation/schemas.ts`, `packages/memory-graph/`
(`api-types.ts`, `canvas/version-chain.ts`, `canvas/renderer.ts`), `packages/tools/`.*

**The model is a schema, and the schema is worth reading in full.** `MemoryEntrySchema` says what
they think a memory is, and four of its fields are things Scio's Layer A needs and does not have.

**Memory is versioned, never mutated.** `version`, `isLatest`, `parentMemoryId`, `rootMemoryId` —
a chain per fact, with `VersionChainIndex` walking parent→children to reconstruct it. Same
conclusion gstack reached independently for decisions (§1.2: an append-only event log where "active"
is *computed*, because a mutable `status` field would contradict append-only). **Two unrelated
projects arrived at the same answer for stored assertions that change over time, and Layer A's spec
fields are exactly that**: a value the user gives, then revises in Layer F, then revises again. A
`Spec` whose fields are overwritten cannot answer "what did they originally say, and when did that
change" — which is the question every "why does my app do this?" support conversation starts with.

**`isInference: boolean`.** A flag distinguishing a fact the user stated from a fact the system
derived. **This is provenance reduced to one bit and put in the type.** Layer A records provenance
per field; this is the minimum viable version of it and it is the discriminator that matters most,
because the two kinds have different authority — an inferred value may be silently re-derived when
inputs change, a stated one may not. Pair it with task-master's rule (§3.4) that the model's output
schema must omit user-owned fields, and you have provenance that is enforced by construction rather
than by convention.

**`forgetAfter` + `forgetReason` + `isForgotten`.** *(Corrected by `PASS2-FOUR-REPOS.md` §3: this
mechanism **does not exist**. `forgetAfter` is read in exactly one place — a border-colour
function — nothing writes `isForgotten`, and their own test asserts an elapsed `forgetAfter`
renders as normal. Take the vocabulary, especially `forgetReason`; the engine is graphify's
half-life decay, which we already have.)* Expiry carries a **reason**, and forgetting is a
*state*, not a delete: `canvas/renderer.ts` draws superseded memories dimmed with a diagonal
strikethrough. Our decay story is graphify's half-life, which is silence — a thing simply stops
being surfaced. A reason field converts "this no longer applies" from a decay artefact into an
auditable statement, and the visual treatment is the honest presentation of it. **For Layer F:
directed change should supersede, dim and record a reason — not overwrite.** An app builder whose
user says "actually, no dark mode" should be able to show them what that undid.

**A closed relation ontology, three values wide.** `type MemoryRelation = "updates" | "extends" |
"derives"`. Not a free-form knowledge graph — three edge kinds, enumerated, and a
`memoryRelations: Record<string, MemoryRelation>` map. Restraint of this order is what makes an
ontology usable; ours (spec field → architecture element → package → component) would benefit from
being enumerated the same way rather than left implicit in the code that walks it.

**`sourceCount` and the `MemoryDocumentSource` join.** Corroboration as an integer, and a
many-to-many link from each memory back to the documents it came from with a `relevanceScore`.
graphify's `reflect` already implements a corroboration threshold, so this is confirmation rather
than a new idea — but the *join back to sources* is the part graphify does not have and Layer A
does need: a spec field should point at the conversation turns that produced it, not merely record
that a model produced it.

**One practical detail worth stealing outright:** `memoryEmbedding` / `memoryEmbeddingModel`
alongside `memoryEmbeddingNew` / `memoryEmbeddingNewModel` — two live embedding columns so the
corpus can be re-embedded under a new model while the old index still serves. We have the identical
problem shape in Layer G every time a stored artefact is derived by a model version: **store the
producing model id beside the derived value, and keep room for a second generation while migrating.**
gstack's `context-bill` reaches the same conclusion from the cost side ("these divisors are
tokenizer-specific… on later models use `--exact`").

**Not taken, and why.** The service, the container/space model, the connectors, the MCP server, the
benchmark leaderboard claims (LongMemEval / LoCoMo / ConvoMem — asserted in the README, not
reproduced in the repo, and I did not verify them). Nothing in `skills/supermemory` beyond
installation guidance.

---

## 6 · The three that stay skipped

### 6.1 repomix — the verdict is right, and one file complicates it slightly

*MIT, 28,070★, pushed 2026-08-23, cloned at `f465ad9`. Read: `src/core/` — `packager.ts`, `file/`,
`treeSitter/parseStrategies/`, `metrics/`, `security/`, `output/outputStyles/`.*

`TOOLING-SCAN.md` called it *"packing — the anti-pattern with a CLI"* and that is exactly what it is.
`docs/next/` names retrieval-versus-packing as a cross-cutting axis, and every layer of Scio is on the
retrieval side — Layer B validates a typed architecture, Layer C emits per-package contracts, Layer D
matches by `Contract`, Layer E gives each package agent only its own brief. There is no point at which
Scio wants the whole corpus in one buffer. The verdict stands unchanged.

One file complicates it without changing it: `treeSitter/parseStrategies/` implements `--compress`,
keeping names, comments, imports and signatures while discarding bodies, across six language
strategies. That is not packing; **it is a signature-only view of a corpus, which is conceptually what
Layer D's catalog is** — a `Contract` is a signature without a body. They arrive at it as a compression
ratio rather than as an interface, and graphify's AST extraction already gives us symbol-level
structure without the packing frame, so there is nothing to install. It is the second sighting of the
same idea (§4's recall-then-verify is the first): **the useful artefact is the signature layer; the
mistake is concatenating it rather than indexing it.** Noted in passing: a worker-pool token counter
with a cache, and `security/` (secretlint plus `filterOutUntrustedFiles.ts`) — the same pre-send scan
gstack does better, and at the sink.

### 6.2 andrej-karpathy-skills — verified, and thinner than reported

*207,634★, pushed 2026-04-20, cloned at `2c60614`. **No `LICENSE` file in the repository**; the
plugin manifest claims MIT. Not authored or endorsed by Andrej Karpathy — the manifest owner is
`forrestchang` and the description says "derived from Andrej Karpathy's observations".*

The report was that it is a single `CLAUDE.md`. **Confirmed, and it is smaller than that:** nine files
total, two of which are content — `CLAUDE.md` at 65 lines and `skills/karpathy-guidelines/SKILL.md` at
67 saying substantially the same thing — plus `EXAMPLES.md` (522 lines of before/after), two README
translations, and manifests. Four rules: Think Before Coding · Simplicity First · Surgical Changes ·
Goal-Driven Execution. No sources, no limits section, no eval — the objection is accurate and the skip
stands.

**Being blunt in the other direction, as the brief asks:** the file is better than its dismissal
implies, on two points we do not currently do.

- **Rule 3, Surgical Changes, is Layer F's problem stated precisely.** *"Don't 'improve' adjacent
  code, comments, or formatting… If you notice unrelated dead code, mention it — don't delete it…
  Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead
  code unless asked."* And the test: ***"Every changed line should trace directly to the user's
  request."*** Layer F takes a marking on a preview and produces a directed change; the failure mode
  is a model that rewrites the surrounding screen. That sentence is the acceptance criterion for
  directed change, and it is checkable against a diff.
- **The document's *form*.** It opens with its own tradeoff — *"These guidelines bias toward caution
  over speed. For trivial tasks, use judgment"* — and closes with an observable success criterion:
  *"These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to
  overcomplication, and clarifying questions come before implementation rather than after
  mistakes."* **Of the eight repositories, this 65-line file is the only rules document that states
  how you would know it worked.** Our `Playbook` ships into every build prompt and has neither a
  declared tradeoff nor a success criterion. Take both, for the `Playbook` as a whole and per
  section.

That two good ideas sit in a 65-line file with 207,634 stars and no eval is the whole argument of
`docs/next/SKILLS.md` in one artefact: provenance and evals are the gap, and popularity measures
neither.

### 6.3 get-shit-done — archived, and now only a redirect

*64,638★, **archived: true** (confirmed at the GitHub API today), last push 2026-05-31, MIT, cloned
at `bdcaab2`.* The `README.md` is no longer documentation; it is nine lines saying the project moved
to `open-gsd/gsd-core`. The repository still contains the machinery — 29 `gsd-*` agent definitions,
hooks, phase files, a changeset history — but it is a competing pipeline to `PIPELINE.md`, adopting
it means adopting its phase decomposition wholesale, and that is the same objection that disqualified
ECC. Archived plus superseded plus competing: the skip needs no further defence. **One correction to
record:** `TOOLING-SCAN.md` lists this as archived and it is, but the successor repository exists and
is not the same artefact — if anyone revisits this, they should look at `open-gsd/gsd-core`, not at
64,638 stars pointing at a redirect page.

---

## 7 · Verdict table — item by item, with the layer each serves

| # | Finding | Source | Layer | Verdict |
|---|---|---|---|---|
| 1 | `datamark()` at the render boundary — neutralize stored user text before it enters any prompt | gstack `lib/gstack-decision.ts` | **A, F, B** | **take.** ~10 lines; closes the gap a write-time denylist cannot |
| 2 | Scan-at-sink on the exact bytes, from the file that is passed downstream | gstack `spec` 4.5b | **A, E** | **take** |
| 3 | Three-tier gate (block / per-finding confirm / FYI); top tier unskippable by any flag | gstack `spec` 4.5b | **A** | **take** |
| 4 | Audit-sink invariant as a named test: a refused spec is in no store, no log, no prompt | gstack `spec-quality-gate-secret-sink.test.ts` | **A** | **take** |
| 5 | One-way / two-way `door_type` question registry; stable option keys, not labels | gstack `scripts/question-registry.ts` | **A** | **take** |
| 6 | Registry primary, keyword patterns as fallback, default to asking | gstack `scripts/one-way-doors.ts` | **A** | **take** |
| 7 | Catalog token budget + per-entry byte cap + same-commit ratchet on the derivation | gstack `test/catalog-budget.test.ts` | **D** | **take — the highest-value item for Layer D** |
| 8 | Cost estimator publishes its error band, its calibration corpus and its expiry condition | gstack `lib/context-bill.ts` | **E** | **take** |
| 9 | Optional-provider contract: required/optional capabilities, ops classed read/write, fail-closed default, `local` as a provider property, consent covers *search* | gstack `lib/code-intelligence/contract.ts` | **D, G** | **take when the library outgrows a file** |
| 10 | `null` (didn't run) vs `[]` (ran, found nothing) as distinct results; never search unscoped | gstack `gstack-decision-semantic.ts` | **D** | **take** |
| 11 | Event-sourced decisions; "active" computed, never a mutable status field | gstack + supermemory, independently | **A, G** | **take** |
| 12 | Tiered tests: free structural per-PR, paid behavioural periodic, env-scoped to the changed unit | gstack `test/helpers/e2e-gate.ts` | build process | **take** |
| 13 | Registry membership *is* the test — the registered set must equal the filesystem set | gstack `test/helpers/carve-guards.ts` | build process | **take** |
| 14 | Claimed limitations need evidence: verbatim error, documented statement, or a live probe | gstack preamble | **Playbook** | **take** |
| 15 | "No envelope" ≠ "zero results" — a failed pipeline is not an empty one | gstack `spec` 1b | **Playbook** | **take** |
| 16 | `Consumes` / `Produces` block on every package, justified by executor isolation | superpowers `writing-plans` | **C** | **take**, plus the bipartite completeness check as a validation rule |
| 17 | `## Global Constraints` — spec-wide requirements copied verbatim into every package prompt | superpowers `writing-plans` | **B, C** | **take** |
| 18 | The spec binds, the plan argues; a build with no reachable spec is marked provisional | superpowers `subagent-driven-development` | **A, C** | **take** |
| 19 | Package boundary = the smallest unit a gate could independently reject | superpowers `writing-plans` | **C** | **take** as a validation rule |
| 20 | `No Placeholders` rejection list, incl. cross-task references and undefined types | superpowers `writing-plans` | **C** | **take** |
| 21 | Classify the request (spike/bounded/architectural) before the first question, out loud | superpowers `brainstorming` | **A** | **take** |
| 22 | One-way ratchet: hidden complexity upgrades the path; nothing downgrades mid-task | superpowers `brainstorming` | **A** | **take** |
| 23 | "What scales with simplicity is the artifact, never the approval" | superpowers `brainstorming` | **A** | **take** |
| 24 | Decompose-before-interrogating when the request names several subsystems | superpowers `brainstorming` | **A → C** | **take** |
| 25 | Ambiguity check that *resolves* rather than flags: pick one, make it explicit, record it | superpowers `brainstorming` | **A** | **take** |
| 26 | Red-flag / rationalization tables — excuses paired with rebuttals, not rules | 4 independent instances | **Playbook** | **take the form** |
| 27 | Visual mode offered just-in-time, as its own message; per-question show-vs-tell test | superpowers `brainstorming` | **F** | **take** |
| 28 | Per-build ledger: identity first line, append-only completion lines, resume from the file not the conversation | superpowers `subagent-driven-development` | **E** | **take — prevents re-running completed packages** |
| 29 | Rulings not stalls: closed 4-item stop list + `Ruling: what — why — cost if wrong` | superpowers `subagent-driven-development` | **E, F** | **take**; the cost-if-wrong field is what makes Layer F's undo meaningful |
| 30 | Fix-round circuit breaker: 5 rounds, escalate model+context at R≥4, defined terminal state | superpowers `subagent-driven-development` | **E** | **take the whole ladder** |
| 31 | Model selection as a routing table by role; review model scaled to diff risk | superpowers `subagent-driven-development` | **E** | **take** |
| 32 | Validators emit an evidence table, one row per checked pair; no rows = not a scan | superpowers `subagent-driven-development` | **B, C** | **take — best single sentence in the eight repos** |
| 33 | An agent's success report is not evidence; verify the artefacts it produced | superpowers `verification-before-completion` | **E** | **take** |
| 34 | 3 failed fixes = wrong architecture, not a failed hypothesis | superpowers `systematic-debugging` | **E → B** | **take**; we have no back-edge from build failure to architecture |
| 35 | Condition-based waiting: poll the condition, name it in the timeout, getter inside the loop | superpowers `condition-based-waiting` | **E** | **take as-is** for sandbox/preview waits |
| 36 | Four-part agent brief: scope · goal · explicit constraints · specified output shape | superpowers `dispatching-parallel-agents` | **C, E** | **take**; ours carry two of four |
| 37 | Score-then-expand decomposition; the scorer may return "do not decompose" | task-master `analyze-complexity` | **C** | **take** |
| 38 | Monotone dependency ordering in the prompt **and** a cycle check that doesn't trust it | task-master `dependency-manager.js` | **C** | **take both halves** |
| 39 | At least one package with an empty `Consumes`, or the plan is deadlocked | task-master `ensureAtLeastOneIndependentSubtask` | **C** | **take** — one line, real failure mode |
| 40 | User-owned fields are **absent from the model's output schema**, not merely protected by a rule | task-master `base-schemas.js` | **A, F** | **take — strongest idea in that repo** |
| 41 | Minimum-substance constraints in the type, alongside the placeholder list in the prompt | task-master `SubtaskSchema` | **C** | **take** |
| 42 | Prompts as versioned JSON assets: semver, typed named parameters, conditional variants, schema-validated | task-master `src/prompts/` | build process, **B** | **take the shape**, write our own (Commons Clause) |
| 43 | Recall-then-verify: cheap over-inclusive recall → top-k → exact `Contract` verification | derived against claude-context | **D** | **take the decomposition; implement recall as an inverted `Contract` index, not vectors** |
| 44 | Vector similarity on the matching path | claude-context | **D** | **leave.** Their own eval: F1 0.40 → 0.40, tokens −39.4% (1.65×) vs graphify's measured 26.1×. **Read `PASS2-FOUR-REPOS.md` §2 before citing that F1**: `hits` are the files the agent *edited*, not what retrieval returned, so it measures end-to-end localisation, not retrieval quality |
| 45 | Content-hash staleness test keyed by absolute path | claude-context `sync/` | **D** | **take the 24-line three-way set diff only.** *(Corrected by `PASS2-FOUR-REPOS.md` §2: this row credited a Merkle DAG that does no work — root plus flat leaves, no intermediate nodes, and `checkForChanges()` reads and hashes every file before comparing. There is no logarithmic diff to take.)* |
| 46 | Versioned memory with `isLatest` + parent/root chain; never mutate a stored assertion | supermemory `MemoryEntrySchema` | **A** | **take** |
| 47 | `isInference` — provenance reduced to one enforced bit | supermemory | **A** | **take** |
| 48 | `forgetAfter` + `forgetReason` + `isForgotten`; superseded is shown dimmed, not deleted | supermemory | **F, A** | **take** |
| 49 | Closed relation ontology, three values wide | supermemory | **G** | **take the restraint**; enumerate ours |
| 50 | Store the producing model id beside a derived value; room for a second generation while migrating | supermemory embedding columns | **G** | **take** |
| 51 | Signature-only view of a corpus is the useful artefact; concatenating it is the mistake | repomix `--compress` | **D** | **leave the tool**, keep the observation |
| 52 | "Every changed line should trace directly to the user's request" | karpathy-skills rule 3 | **F** | **take** as the acceptance criterion for directed change |
| 53 | A rules document declares its own tradeoff and its own success criterion | karpathy-skills | **Playbook** | **take the form** |
| 54 | gstack `plan-*-review` persona family; `gbrain:` declarative context queries; the 865-line generated preamble | gstack | — | **leave.** `OPERATING-MODEL.md` §2.1 was right about this sixth of the repo |
| 55 | repomix as a tool; get-shit-done's pipeline; supermemory the service; claude-context the MCP | all four | — | **leave**, as originally decided |

### Three things to correct in `TOOLING-SCAN.md`

1. **gstack's row.** "23 tools… personas, not decision procedures" — it is 61 skills, and the
   persona framing covers roughly six of them. Keep the `skip`; replace the reason with *"a
   competing harness we will not adopt wholesale, mined separately."*
2. **claude-task-master's licence.** The row records none. It is **MIT + Commons Clause v1.0**,
   which withholds the right to sell — material for a commercial builder, and the reason the API
   reports `NOASSERTION`.
3. **`multica-ai/andrej-karpathy-skills` has no `LICENSE` file**, only a plugin manifest asserting
   MIT, and it is not authored by Andrej Karpathy. Both worth stating where the repo is named.

### What this pass cost, and what it says about method

Eight repositories, cloned and read on 2026-08-26. Three verdicts confirmed in a paragraph each
(§6), one confirmed and deepened (§5), one confirmed while yielding the section's actual finding by
contrast (§4), one re-aimed at the layer it fits (§3), one whose 1/14th reading hid its three most
useful files (§2), and one whose stated reason was a summary of the README (§1). The adoption calls
were 8 for 8. **The mineable content was 0 for 8, because nobody opened the files** — and the
single most useful item in the whole pass, §1.4's catalog budget, sits in a test file of a
repository dismissed for its marketing copy.

