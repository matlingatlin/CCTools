---
name: memory-provenance-separation
description: "Use when durable agent memory holds something a user SAID as though the system had CHECKED it, or holds a fact with no date — a version, config, ownership, preference or environment claim asserted once in an old session and still steering decisions, an agent citing memory to rule an option out, memory that retrieves perfectly but is out of date. Stamps each row with origin (asserted / observed / derived), source, an as-of date, a re-check handle and a staleness horizon, then gates read-time trust on origin and age instead of on retrieval success, correcting by appending rather than editing. Triggers on 'the agent still thinks we use X', stale remembered facts, provenance or freshness of stored context, 'memory says…'. NOT for saving, searching or handing off memory itself (unified-memory — this governs the ORIGIN and FRESHNESS of a row, not its storage or retrieval), NOT for logging model calls, tokens, cost or replay (llm-call-ledger — that records calls, not knowledge provenance)."
---

# Memory Provenance Separation

Durable memory stores **claims** and returns **facts**. The gap between those two words is
where this fails, and it fails silently — retrieval works perfectly, so nobody looks.

Session 3 the user says *"we're on Postgres 14."* Session 40 the agent declines a PG15
feature the cluster has had for a year, and defends the refusal by citing memory. Every
component did its job. The row was saved correctly, retrieved correctly, and quoted
correctly. It was never true after month two, and nothing in it could say so.

**The rule, written against the outcome: a retrieved row is a dated claim, never a fact.**
A row may inform what you do. A row that is `asserted` or past its horizon may not be the
reason an option is ruled out, narrowed, deferred, downgraded, routed around, or quietly
not attempted — regardless of how the avoidance is phrased.

*Evidence:* MemSyco-Bench (arXiv 2607.01071, Jul 2026) benchmarks this directly: retrieved
memories "induce a critical issue of sycophancy, causing agents to over-align with the user
at the cost of factual accuracy or objective reasoning." Of its five tasks, three are ours —
rejecting memory as factual evidence, resolving conflicts between memory and objective
evidence, and tracking memory updates. The paper's framing is sycophancy; the mechanism is
unmarked origin. Its point about prior benchmarks is the one that matters here: they check
whether a memory was stored, retrieved and updated correctly, and that check passes on the
Postgres row.

## When to use
- Writing anything to durable/cross-session memory that a later session will act on.
- An agent justifies a decision with "memory says…", especially a decision NOT to do something.
- A remembered environment, version, config, owner, policy or preference is steering work and
  nobody has re-checked it this quarter.
- Auditing an existing store for undated or unattributed rows.

**When NOT to use:** you need the *mechanics* of saving, searching, handing off or resuming
(`unified-memory` — it stores; this governs what a stored row is allowed to mean). Those two
**compose, and both fire on a write:** *"remember that we're on Postgres 14"* is a
`unified-memory` save carrying the stamp this talent supplies — routing it away here is exactly
how the stamp never gets applied. Decline only when no row's origin or freshness is in question:
transport, scopes, handoff format, resume mechanics. Also not for: logging model calls, tokens
or spend (`llm-call-ledger`); a handoff brief going silent on a requirement
(`inherited-context-drift-audit`); incoming *data* drifting at a pipeline boundary
(`data-contract-assertions`).

## The stamp — five fields on every durable row

| Field | Form | Why it is not optional |
|---|---|---|
| `origin` | `asserted` (a person or another agent told us) · `observed` (this system checked, and the check is recorded) · `derived` (computed from named row ids) | Retrieval cannot tell these apart and neither can the text; if it is unmarked it will be read as observed |
| `source` | the person + session, the exact command, file+line, or API response | An assertion with no author is a rumour |
| `as_of` | UTC date the claim was **true**, not the date the row was written | Copying a claim forward with a fresh write date is worse than no date |
| `recheck` | the one-line check that would turn this into `observed` (`SELECT version();`) | A claim with no way to check it is a preference, not a fact |
| `horizon` | how long this class of claim stays credible, taken **from the class table below, not from judgement** | Age alone means nothing; age against a horizon means something |

Horizon bands: versions/config **weeks** · ownership/org **months** · a standing preference or
policy **months** · someone's stated intention **hours**. They are a `decided` default, not a
measurement — deviate where the domain warrants, but a horizon set **longer** than its class band
is itself a claim and goes in `source` with its reason. An unjustified long horizon is the `as_of`
refresh from the other end of the same inequality: both extend `now − as_of < horizon` with no new
evidence, and only one of the two looks like cheating.

## Steps

1. **Classify at write time, and default to doubt.** Every durable write carries all five
   fields. If you cannot establish origin, it is `asserted` — never `observed`. If the store
   has no fields for provenance, put a **fixed, greppable stamp line** in the body instead
   (`origin: asserted | source: … | as_of: … | recheck: … | horizon: …`); step 5 depends on
   that line being byte-identical everywhere.

2. **Keep the claim and the check as separate rows.** *"User states the cluster is PG 14"* is
   one row (`asserted`). *"`SELECT version()` → 15.4"* is a different row (`observed`). Never
   collapse them into one "fact" row: the merge destroys the only thing that lets a later
   session tell a report from a measurement.

   *Supersession propagates.* When a row is superseded, every `derived` row that names it is
   stale too, whatever its own `as_of` says — re-derive it, or mark it pending. A fresh
   derivation date must never launder a stale basis.

3. **Gate trust at READ time on origin and age — not on retrieval success.** Before a
   retrieved row changes what you do, require `origin == observed` — or `derived`, if every
   basis row it names currently passes this same gate — **and** `now − as_of < horizon`.
   Fails → run its `recheck` and use the answer. Cannot recheck →
   the doubt goes into the output where the user can see it: *"memory says PG 14 — asserted
   by you in session 3 (2026-03-04), never verified since; I have not confirmed it."*
   Never let a failing row silently produce a narrower plan.

   **Two classes of claim, one gate, different origins.** For a claim about the WORLD — a
   version, a config, an owner, an environment — `asserted` is a *proxy* for something
   checkable, and only `observed` may carry a decision. Expect the rationalization *"the user
   told me directly, that is stronger than a check"*: it is false, because authority names the
   **source**, it does not raise the **origin**, and the benchmark above is the measurement of
   what believing otherwise costs. For a claim about the PERSON OR ORG THAT MADE IT — a
   preference, a policy, a decision, an authorization, a stated intention — the assertion **is**
   the fact and there is nothing to observe: it passes on `asserted` by that party plus age
   against horizon alone, its `recheck` is a confirmation with that party, and inside its
   horizon you honour it silently instead of disclaiming it. The trap is a self-fact worded as
   a world-fact: a CTO saying *"we're off Kafka entirely"* is authoritative that the **decision**
   was taken and is no evidence whatever that the **migration completed**. Split it into the two
   rows of step 2 and gate each on its own class.

   **Leave a trace, or the gate is unfalsifiable.** A gate that passes silently is
   indistinguishable from a gate that never ran — this talent's own failure family, turned on
   itself. So the stamp travels with the claim: wherever a memory-derived claim reaches an
   output, a plan or a decision, it carries `id · origin · as_of` inline — *"Postgres 15.4
   (m-311, observed, 2026-08-28)"*. A bare memory-derived claim with no attribution is the one
   failure of this talent a reviewer can catch by reading the output.

4. **Correct by APPENDING and by precedence, never by mutation.** Write the observation as a
   NEW row with today's `as_of`, linked to the claim it corrects. At read time the newest
   `observed` row beats any older `asserted` one. Correctness comes from precedence, not from
   editing history — which is what makes step 6's gate cheap enough to actually obey: **you
   never need to destroy anything to fix a wrong fact.**

5. **Sweep for unstamped and expired rows — and prove the sweep can see.** Enumerate rows
   that are unstamped, `asserted` past horizon, or `observed` past horizon. **Before reporting
   a clean sweep, run a POSITIVE CONTROL:** name (or plant) a row you KNOW is present and
   stale, run the *identical* query, and confirm it comes back. A query returning nothing is
   indistinguishable from a wrong field name, the wrong scope (user vs project vs team), a
   matcher that never matched, or a store that silently omits superseded entries. This
   talent's own failure mode is silent, so an unproven sweep reproduces the bug it exists to
   catch. Report the control's result beside the finding count; a count with no control is
   not evidence of a clean store.

   **One control per scope, and one row outside normal recall.** A control proves only the path
   it travelled: a hit in one scope says nothing about the others, and nothing at all about the
   rows normal recall excludes *by design* (superseded, rejected, archived, low-trust) — which
   are precisely the rows a staleness sweep is hunting. Run the identical query once per scope
   the sweep claims to cover, add one row reachable only by direct id read, and name the scopes
   the control covered. An unnamed scope is an unswept scope, and a single-scope control
   reported as a clean store is this talent's own bug wearing a control's clothes.

6. **Human gate, anchored on the outcome.** Gated if, afterwards, **a row that normal recall
   used to return no longer comes back, its stored content differs, or any row becomes
   unrecoverable — including one normal recall had already excluded.** By any means and
   under any name: delete, overwrite, edit in place, merge, dedupe, prune, expire, compact,
   redact, archive, move to another scope, retag, mark superseded/rejected where that drops it
   from recall, purge the already-superseded set, set a retention or TTL policy that ages rows
   out, re-index or re-embed, or narrow the query so it is no longer reached. **The
   already-excluded set is the trap on this list:** purging it changes nothing normal recall
   returns, so a reachability-only test waves it straight through — and it is the audit trail
   step 4's precedence is computed from, which makes it the most destructive item here and the
   easiest to justify. All one outcome; all a
   **PROPOSAL to one named human**, never an act — stating row id, current content, its
   origin/source/as_of, the evidence it is wrong or expired, the proposed outcome, and what
   becomes unrecoverable. Appending a corrected row is **not** gated. Obvious staleness is not
   an exemption: obviousness is a property of your current context, and the row outlives it.

## Worked example

| # | Row | origin | source | as_of | horizon | Read-time verdict |
|---|---|---|---|---|---|---|
| m-104 | Cluster runs Postgres 14 | `asserted` | user, session 3 | 2026-03-04 | 30d | **fails on origin** — `asserted` never passed, and expired besides → recheck before use |
| m-311 | `SELECT version()` → 15.4 | `observed` | `psql -h prod-1 -c 'SELECT version()'` | 2026-08-28 | 30d | current → wins by precedence |

Session 40, without this skill: *"We're on PG 14, so I'll avoid that."* With it: m-104 fails
the step-3 gate on origin before age is even reached, `recheck` runs, m-311 is appended, the
PG15 feature is used and cited as *"Postgres 15.4 (m-311, observed, 2026-08-28)"*, and m-104 is
left standing — not deleted, because nothing needed deleting. Contrast a self-fact: *"m-208 —
user prefers terse answers, `asserted`, user session 3, 2026-03-04, horizon months"* is honoured
as written and never disclaimed, because there is no observation of a preference to go and make.

## Red flags
- "Memory says X" offered as evidence for X. It is evidence that someone said X, on a date.
- A row marked `observed` for a check you did not run yourself in this session.
- A claim repeated across many rows or many retrievals treated as corroborated. Repetition is
  not observation; copies of one assertion are still one assertion.
- Re-writing a row and refreshing its `as_of` because the content still looks right.
- Lengthening a `horizon` so a row stops failing the gate. Same inequality, other end.
- A sweep reported clean with no positive control beside it, or with a control that only ever
  travelled one scope.
- Reaching for delete/archive/merge to fix a wrong fact when appending would do — or reaching
  for the *superseded* pile, on the grounds that nothing reads it anyway.
- A memory-derived claim in an output or a plan with no `id · origin · as_of` beside it. You
  cannot tell that from a gate that never ran.

## In this repo (one instance)
The ECC Memory Vault behind `unified-memory` has no provenance fields — every entry is
`trust: unreviewed`, and normal recall already excludes superseded entries — so stamp in the
body and treat "superseded" as reachability-affecting under step 6. Positive control for
step 5, one per scope: normal search covers active `project` and `team` only, so run the same
`ecc memory search` in each, and again with `--scope user` — which is *never* included
implicitly, so a sweep that omits it reports a clean store it never looked at. Then read one
superseded entry by id with `ecc memory read`, which reaches non-active entries that search
excludes by design; that is the row outside normal recall. `ecc memory doctor` validates
structure, not provenance, so a green doctor says nothing about staleness. Note that writes
here are create-only and the MCP surface exposes no overwrite or delete, so most step-6 outcomes
in this instance are reached by scope moves, supersession and retention, not by deletion.
Step 6 proposals belong in this repo's human-gate proposals ledger under `pipeline/ledgers/`.
