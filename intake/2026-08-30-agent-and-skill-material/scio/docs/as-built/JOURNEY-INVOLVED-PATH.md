# The Involved Path

One user, one project, end to end — through the design window and out the other side.

This is **Level 2**: the user chooses to shape the design before the expensive build. The user
in this walkthrough is *impatient and untidy*, which is the realistic case and the more useful
one to trace: they do not use every tool, they do not iterate until satisfied, and they approve
early.

Two views of the same journey. **Part 1** is what the person experiences, in their language.
**Part 2** is what the backend does, keyed to the same step numbers. **Part 3** is where
*intended* and *today* come apart.

Sources: `docs/UX-FLOW.md` (intent), `LAYER-A` / `LAYER-E` / `LAYER-F` / `LAYER-G` (reality),
verified against code 2026-08-26.

---

# Part 1 · What the person experiences

### 1. They open Scio and start a project
They pick **application** from three routes. A near-instant screen — nothing has cost anything
yet.

### 2. They talk
A conversation, not a form. The agent asks one thing at a time and gives an example with every
question. Our user answers the first three fully, then gets bored and writes a long paragraph
covering several things at once.

They are asked about non-goals ("anything you deliberately want to skip?"). They say "no idea"
— which is recorded as *nothing excluded* rather than left blank.

### 3. They are shown themselves, better
The conversation stops. They are handed a written account of their own project — organised,
connected, more coherent than anything they said. Some sentences carry an **"assumed"** tag:
the platform, the look, who owns the data.

They skim it. It is right enough. They approve.

### 4. They are asked one question: how involved?
Two cards. *Shape the design first* is recommended, with a reason given: a change against a
preview costs one package to regenerate; the same change after a full build costs the build.

They pick it. They want to see it.

### 5. They wait, and are told it is only a preview
A short generation with calm text setting expectations. Then a preview of their app opens, with
a prompt field on the right and marking tools.

### 6. They mark three things and type one sentence
They click a heading — it becomes **1**. A button — **2**. A whole section — **3**. Next to
each number they write what they want: *"too big"*, *"move this up"*, *"this should be blue"*.

They ignore the drawing and note tools entirely. Then, in the free prompt field, they add:
*"and make the whole thing feel calmer."*

They press **Update** once. Everything goes at once — this is a batch, not a live conversation.

### 7. One of their markings argues with what they agreed
Marking 3 would remove something the spec says the app does. It is not silently applied. They
are asked: **keep it as it is**, or **change the plan** — which amends the approved spec and
freezes a new version.

They pick *change the plan*, without reading closely.

### 8. Some changes land, one does not
The result is per-marking, not one verdict. Markings 1 and 2 are applied. Marking 3 became the
spec amendment. The free-prompt "calmer" request touched two packages, one of which was
**rejected and rolled back** — the preview did not silently half-change.

They see what happened to each numbered item. They do not do a second round. It is fine.

### 9. They press build
The real build. They are told it takes a while and they can leave. They leave.

### 10. It is ready, and it tells them the truth
The running app is front and centre — clickable, not a mockup. Beside it, a plain-language
receipt: what was built, what was checked, and — honestly — **what still needs a look**.
Nothing is hidden.

Three ways onward: **try it**, **open & refine**, **get the code**.

### 11. They try to get the code — and this is where the journey stops
The screen is real. Version, commit sha, build time, honest status. Then a block titled
**"Not built yet"**, naming three things individually: downloading the repository, pushing to
your own remote, publishing.

None of them exist. The screen is honest rather than functional.

**Publish** says the same. And **five routes are placeholders**, not one — `/live` ("Refine"),
`/versions`, `/settings`, `/states`, `/notifications` — each rendering *"This screen is being
ported from the prototype next."*

So the journey ends with a working application the user can look at and click — and no way to
take it with them, which is the thing the product's differentiator promised.

---

# Part 2 · What the backend does, step by step

### 1. New project
`POST` a project row: `type`, `status=draft`. Loads the intake schema for `app`. **No engine
call, no model call, no cost.** Everything is scoped by `workspace_id` — one of the six tables
that actually carries the column.

### 2. Each message — `POST /projects/:id/intake/message` → engine `POST /intake/step`
One turn is four ordered operations (`intake/service.py`):

1. **Extract** — the conversation goes to the model, which returns typed fields with
   `source`, `confidence` and `provenance` (message ids). Anything claiming `stated` without a
   real message id is **discarded**, not kept. Rejections are returned rather than swallowed.
2. **Detect contradictions** — by rules, not judgement. A conflict holds the gate shut.
3. **Ask the gate** — `is_buildable()`: every core field answered *or* flagged as defaulted,
   every triggered conditional resolved, no open contradictions.
4. **Write the next question** — the gate decides *which* field, deterministically; only the
   *wording* goes to the model, with the schema's own phrasing as fallback.

The long unfocused paragraph in step 2 is handled by extraction filling several fields from one
turn — that is why one-field-per-turn was abandoned (recorded as B065).

"No idea" for non-goals writes an explicit *nothing excluded* rather than leaving a hole.

Metered per exchange: `cost_usd` on both the extraction and the question.

### 3. Spec gate — Layer B
`AppSpec → { whole, architecture, playbook, validation }`. Refuses a spec that has not passed
gate 1 (`NotBuildableError`).

Order is load-bearing: **the architecture is derived by rules and validated by eleven rule identifiers
before any model call**, so a design error costs a function call rather than a relay run. Then
the *whole* is written by the model, grounded — and the **"assumed" tags come from Layer A's
metadata, not from the model's claim about itself.**

Approval: `POST /projects/:id/spec/approve` freezes a `spec_version`.

### 4. The involvement question
`InvolvePage`. A route decision only — no backend work.

### 5. Preview — `POST /projects/:id/design/preview` (SSE)
Layer C decomposes the architecture into dependency-ordered, contract-bearing packages. Each
package's prompt carries its goal, its architecture slice, its dependencies' **interfaces and
not their code**, house rules, canonical vocabulary, scope guard and acceptance criteria.

Layer D matches every package against the library before generating. Layer E builds each
package and stamps every element with `data-scio-package` and a `scio_id` — **this stamping is
what makes step 6 possible at all.**

### 6. The batch — `POST /projects/:id/design/change`
A `ChangeBatch`: the markings plus one batch-wide prompt. Each marking carries `scio_id`,
`scio_package`, `tag`, `text`. The order is the design (`change.py:3-11`):

**resolve strictly → detect conflicts → ask the model → guard → commit.**

- **Resolve** — every marking maps to package/file/line via the manifest, and each gets *its
  own* outcome. Unaddressable markings are named, not dropped.
- The batch gets **one cost accumulator for the whole batch**, not per marking.
- **A rejected package does not stop the others**, and a rejection is rolled back rather than
  half-written.

Returns `DesignChangeResult`: `applied`, `conflicts[]`, per-package `edited_files` /
`rejection` / `rolled_back`, `unaddressable[]`, the moved-on manifest, `total_cost_usd`,
`compiles`, `git_sha`.

Two fields state their own honesty: `git_sha` — *"Empty means it could not be committed, and
therefore cannot be returned to."* `compiles` — *"None means nobody asked."*

### 7. The conflict
`detect_conflicts(batch, arch, allowances)` — regex plus canonical vocabulary, deliberately
model-free. Two answers only: keep as-is drops the marking; change the plan `POST`s
`/projects/:id/spec/amend` and freezes a new `spec_version`.

### 8. Commit
One commit per batch, `commit_change` returns the sha. A design version records the ref.

### 9. Build
`POST` a build. `ensureCanStart` checks the monthly cap ($50 default) and refuses with a 409
naming both figures. A `build_job` row is created before any work. A per-build spend ceiling is
computed as the approved estimate × 1.5 and travels into the relay.

Layer E runs the gates in cost order: instrumentation (free) → seven deterministic validation
agents (free) → console classifier (a page load) → critique → app-wide typecheck.

### 10. Reveal
Honest status: `passed / needs_look / failed / blocked`, with `unjudged` a first-class value.
`build_version` carries `git_sha`, `honest_status`, `cost_usd`, `tokens`.

### 11. Get the code / publish
`ShipPage` reads the build version and renders it. **There is no download endpoint and no push
endpoint.** The deployment module is three files, 63 lines, both methods throwing
`NotImplementedException` — Nest's 501.

---

# Part 3 · Intended versus today

| # | Intended | Today |
|---|---|---|
| 2 | Conversation adapts to the kind of app | Fixed schema order, always the same six fields. Deliberate — the gate must be un-talk-past-able — but nothing detects *what kind* of app early |
| 3 | The whole, plus a sense of how well understood each area is | Prose plus a flat assumptions list. **No score.** Computable today from downstream tags × field `source` — not computed |
| 5 | Preview includes a **feasibility check** | Not found as a distinct step. Layer B's eleven rule identifiers are the nearest thing, and they run earlier |
| 6 | Tools: draw a line, mark, point, note | Marking and prompting are real. The rest of the promised toolset is not — `STRATEGY.md` §D names seven design-window tools; most are absent |
| 7 | A security-relevant allowance needs a second, distinct confirmation | **Only in the browser.** `AmendSpecDto` has three fields and no confirmation field — a direct POST records the allowance without it |
| 8 | `compiles` answers whether the change broke the build | A tri-state carried by hand through four hops with `?? null` at each, answered independently in two places, and **no test covers it** |
| 8 | The $2.00 per-change ceiling protects the design loop | Hard-coded in the API, and **entirely untested** — no `budget_usd` or ceiling reference in the design tests |
| 9 | Builds are jobs, queued and worked | Job row, cancellation and reaping are built. **The queue and worker are not** — `status = "queued"` is unreachable and the API still owns a forty-minute unit of work |
| 9 | The per-build ceiling caps the build | Checked *after* the call that crosses it, and the raise discards the whole `RelayResult` — so that attempt's completed passes go unbilled. Layers B and C and the library contribution run with **no spend tracking at all**; the reported cost is packages-only |
| 10 | The receipt shows checks passed | `checks_passed` is computed, typed, transmitted — and appears in **no** `.tsx` file. Never shown |
| 10 | "Does it work with real data" and "can a guest read another's row" | The two most valuable gates, **off by default** behind `SCIO_VERIFY_DATA=1` |
| 11 | You own the code — git, history included | **No download, no push, no publish.** The screen names all three as not built. This is honest, and it is also the differentiator's surface missing |
| 11 | Settings: spend, what is running, how to stop it | `PlaceholderPage` |

## What this journey reveals that the layer documents did not

Walking one user through end to end shows that **the product's honesty is complete and its
delivery is not.**

Every trust moment is built and built carefully — the grounded whole, the flagged assumption,
the conflict asked rather than resolved, the per-marking outcome, the honest status with
`unjudged`. A user is never lied to.

And then the journey ends at a screen that tells them, truthfully, that they cannot have the
thing they were promised.

The gap is not distributed evenly. **Nothing scores what was understood at the start**, and
**the entire post-reveal half is unbuilt** — five placeholder routes, not one.

`/live` — "Refine" — is the sharpest case. `UX-FLOW.md` says Level 1 *"does not remove control
— it moves shaping to AFTER the build… so Level 1 does not read as the lesser path."* That
shaping surface is a placeholder. **One of the two involvement levels has nowhere to land.**

Everything between the spec gate and the reveal works. See `REVIEWS-WHAT-WE-MISSED.md` §1.

---

*Written 2026-08-26 from the as-built documents and verified against code. The involvement
question is `InvolvePage.tsx`, covered by `design.test.tsx` and `projects.test.tsx`.*
