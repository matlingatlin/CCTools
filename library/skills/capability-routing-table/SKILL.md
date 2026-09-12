---
name: capability-routing-table
description: "Use when a library of skills, agents, or commands has grown until nobody can say WHICH unit owns a request — several descriptions claim the same job, no one can name the owner without re-reading the library, or a new unit is joining a crowded neighbourhood. Derives the library-wide job-to-owner table (job as typed, owner, the discriminator that picks it) and PROVES each row with negative triggers: per capability, the requests that must NOT route to it and the sibling they go to instead. Triggers: 'who owns this job', 'which skill should handle X', 'routing table', 'capability map', 'draw the boundaries'. NOT the periodic inventory grading each unit on quality, staleness, and tests (use skill-stocktake — it reports WHICH units overlap; this decides who OWNS each job and tests it). NOT the reactive fix of ONE description when the colliding siblings are already named (use skill-description-optimizer). NOT prior-art search before building (skill-scout), NOT authoring a unit (writing-skills)."
---

# Capability Routing Table

One table saying which unit owns each job across a whole library — and proof: every row
carries the requests that must NOT reach that unit and the sibling they go to instead.
A boundary nobody has tried to break is an assertion, not a boundary.

## When to use
- Several units claim overlapping trigger surface and no one can say who owns a request.
- A unit is joining a crowded neighbourhood and needs its lane cut before it ships.
- Work must be routable by someone who has not read the library.

**When NOT to use:** grading units on quality, staleness, or tests (`skill-stocktake` — run it
first if you don't yet know what exists); one description mis-firing against a named sibling
(`skill-description-optimizer`); checking whether a capability already exists (`skill-scout`).

## What this rests on — state it, don't inflate it
Routing is an **untested structural argument**, and the argument is weaker than it first looks.
The claim is an information asymmetry: a model cannot name the owner of a job in a private
library it has never seen. That rests on a single negative-trigger miss (n=1), and the n=1 claim
standing beside it in the same sentence was pre-registered, re-run at n=12, and refuted.

**The asymmetry mostly evaporates when the library listing is in context** — which on a host that
puts every unit's name and description in front of the model is the normal condition, not the
exception. Given the listing, naming plausible owners and grouping the neighbourhoods is ordinary
reading, and it needs no method. Do not claim the method wins there.

What survives the listing is narrower, and it is the part worth doing: the listing shows
descriptions, so it cannot show what is NOT in them — a unit that cannot be invoked at all
(step 2), a unit that fell out of the table (step 6b), a boundary asserted from only one end
(step 7), or a collision nobody was required to report (step 6's negative control). Those are the
steps that earn their keep. Never present a routing table as an empirical result, as validated,
or as outperforming a general-purpose baseline that can see the same listing.

## Steps

1. **Enumerate every category, then positive-control the enumeration.** List each capability
   path separately (skills, agents, commands, hooks, plugins) and report counts per category — a
   category nobody enumerates is missing from the table while coverage still reads 100%. Then
   name one unit you KNOW is present *before* looking and confirm it comes back. If it doesn't,
   the enumeration is wrong; fix it before reading a single description. Until that control
   passes, a short result is indistinguishable from a correct negative.
   That control catches an under-count and is **blind to an over-count**, so also count UNITS,
   not files — one unit is one frontmatter block, and the tests, references and sub-docs sitting
   beside it in the same path are not units — and reconcile every category total against a count
   you can check by hand. An inventory that doubles a category reads exactly like a correct one.

2. **Extract the claimed job — and check the unit can be reached at all.** Read each unit's
   `description` — the text routing runs on — and write its job in the words a requester would
   type. Names and bodies lie about scope; descriptions decide. Then read the REST of the
   frontmatter for anything that disables invocation by the model or restricts who may call the
   unit. Such a unit never wins a prompt however good its description: mark it **not-routable**,
   and hand its jobs to the unit that actually receives them, naming that unit. A row whose owner
   cannot be invoked routes to nowhere, and nothing anywhere reports it.

3. **Cluster into contested jobs.** One claimant is a row you can write now. Two or more is
   contested and needs a discriminator.

4. **Write the discriminator, not a topic split.** Name the OBSERVABLE feature of the request
   that picks the owner: what the requester already has, has already done, or wants as output.
   "X is about tests, Y is about docs" does not route. Row shape, then one filled row so the
   shape is not the only instance you have seen:
   `| Job as typed | Owner | Discriminator | Must NOT route here → goes to |`
   `| "this run costs too much" | cost-router | the requester is SETTING a ceiling and has not | "we are already over and something must go" → plan-triage |`
   `|                           |             | yet decided what to give up                   |                                                          |`
   The discriminator names a state of the requester, not a topic. "Cost" is in both rows.

5. **Write negative triggers with destinations.** Per capability, at least one request per
   contested neighbour that must NOT route to it, each naming where it goes instead. A negative
   without a named destination is a complaint, not a test.

6. **Run the table, under two controls.** For every prompt, positive and negative, decide which
   description wins on the text as written, not on what you meant. Any ambiguous landing is a
   defect in BOTH descriptions.
   - *Positive control:* one uncontested prompt must route to its undisputed owner. If it does
     not, your judging procedure is broken, not the library.
   - *Negative control:* one pair you already know is ambiguous must be REPORTED ambiguous. The
     positive control only catches a procedure that routes nothing; it cannot catch a judge that
     favours the description it just wrote, and here the same reasoner writes and grades. Without
     a case it is required to fail, "no collisions found" is unfalsifiable.

6b. **Reconcile the table against the enumeration.** Every unit counted in step 1 appears as the
   owner of at least one row, or is listed as deliberately unrouted with a reason. Print both
   numbers. A unit dropped while clustering disappears from the library's routing while the table
   still reads complete — the same failure step 1 guards against for categories, one level down.

7. **Fix both ends — and budget the second end before you write it.** Sharpening one description
   while its rival still claims the prompt leaves the collision intact from the other side, so a
   boundary step 6 found CONTESTED appears in both units' descriptions, naming each other. This
   applies to contested boundaries, not to every pre-emptive NOT-clause: a reciprocal clause is
   not free, it is paid twice, and in a mature library there is no room left to pay. **Measure the
   headroom on both sides first** and say what you found. If only one side has room, the clause
   goes there and the other side is recorded as one-ended, not silently skipped. If neither side
   has room, do NOT buy the clause by truncating another clause in the same field, and do not move
   it to a host-specific field the portable spec does not carry — narrow the WINNER's trigger
   instead, or hand the row to a human as a proposal. Report before/after length for every
   description you touch. Re-run step 6 until each negative loses to its stated destination.

## Rules
- **Nothing leaves the library on your say-so.** If after your change a request that used to
  reach a unit can no longer reach it, you removed that unit — whatever it is called: delete,
  archive, retire, merge away, fold in, deprecate, demote to a reference doc, move it out of the
  scanned path, or narrow its description until no request arrives. That is a PROPOSAL to a
  human with evidence attached, never an act. Disuse, niche scope, rare triggering and library
  size are never grounds.
  **The table is a change.** Leaving a unit out of the standing routing artifact routes work away
  from it just as effectively as editing its description, and "a table is not a deletion" is the
  form this arrives in. Every enumerated unit is either an owner or an explicit, reasoned entry on
  the unrouted list (step 6b) — an omission is a removal and goes to the same human gate.
- Description edits are reversible and may be applied directly — then re-run steps 6–7.
- **Preserve the rest of the frontmatter.** An in-place description edit must drop no other key.
  Verify line-anchored: line 1 exactly `---`, a later line exactly `---`, `name` and
  `description` present. Never `split('---')` — it reports green on an unterminated file.
- Keep each rewritten description inside the cap your project pins, and **measure** it.
- Method only: reason over the text. No network calls, no auto-run hooks.

## In this repo (one instance)
Units live under `.claude/skills/<name>/SKILL.md` and `.claude/agents/` — enumerate both, and in
`.claude/agents/` count only the unit files: the `*.evals.md` beside them are tests, so a plain
`*.md` glob doubles that category. Some units carry `disable-model-invocation`, so step 2's
not-routable check has real work to do here. The standing routing artifact is the capability map
in `CLAUDE.md` — today a job-to-owner list with a discriminator on about half its rows and no
negative-trigger column, so it is step 4's input, not this method's output; say so when you run
here. The description cap is pinned in `pipeline/CONSTANTS.md`, and much of the library is
already at it, so step 7's headroom measurement is the binding constraint, not a formality.
`python3 pipeline/queries/preflight.py` runs the line-anchored frontmatter and dropped-key check.
Removal proposals go to the human gate and are logged in `pipeline/ledgers/proposals.jsonl`.
