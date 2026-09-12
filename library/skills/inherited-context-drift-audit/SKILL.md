---
name: inherited-context-drift-audit
description: "Use before acting on a handoff brief, status summary, task prompt or prefilled trajectory written by another agent or person, to catch requirements it has gone SILENT about rather than ones it contradicts. Triggers: 'continue from where the last agent left off', 'here's the handoff', 'remaining work is X', picking up a wave or shift someone else started, a brief that reads confident and internally consistent. Re-derives the requirement list from the original request first, then walks it row by row, so an omission has something to be measured against. NOT for storing or retrieving durable state (unified-memory), NOT for executing a plan with fresh context (subagent-driven-development), NOT for diagnosing a run that already visibly failed (agent-introspection-debugging), NOT for holding a stated position under social pressure (concession-audit)."
---

# Inherited Context Drift Audit

An inherited brief is evidence of what the last author **ended up doing**, not of what was **asked for**. Models resist direct adversarial pressure yet adopt an abandoned goal when conditioned on a confident prefilled trajectory from a weaker agent (arXiv 2603.03258); the companion failure is drift by *omission* — GD_inaction (arXiv 2505.02709). Nothing contradicts anything, every artifact is internally consistent, and the goal is quietly smaller.

**The rule, written against the outcome: a finding is a requirement from the origin that can no longer be traced in the brief.** Not a contradiction. Contradictions announce themselves; silence leaves no trace, so you must arrive with a list.

## When to use
- Handed a brief, summary, or continued trajectory, about to plan from it.
- A handoff reads complete and confident and you have not seen the original ask.
- Second or later hop in a chain — each hop verifies only against the hop before it.

**When NOT to use:** the run already failed visibly (`agent-introspection-debugging`); you are storing state rather than inheriting it (`unified-memory`); the request is merely vague with no prior author (`prompt-refinement`).

## Steps
1. **Name the origin.** The artifact predating the brief: the original request, ticket, spec, plan, linked issue, customer email. Find it before reading the brief closely. None → see *Origin unreachable*.
2. **Derive the requirement list from the origin, blind.** Enumerate atomic requirements R1…Rn from the origin alone, each with its verbatim phrase — before absorbing the brief's framing, or the brief decides what counts as a requirement and silence becomes unfindable. **Without a derived list there is nothing to be silent about.**
3. **Walk the list one row at a time**, three outcomes only: `mentioned + complete` / `mentioned + partial` / **`NOT MENTIONED`**. Search the brief for each requirement's synonyms, not just its words, before writing NOT MENTIONED. The third column is a CANDIDATE finding, not yet a finding — a handoff that says "remaining work is X" omits finished requirements by design, and that is the normal shape, not drift.
4. **Name the drift form** on every non-complete row: silent drop · weakened restatement ("handle errors" → "log errors") · scope shrunk to what got done · demoted to "future work" · a blocker described as finished.
5. **Anti-paranoia gate — done, decided, or silent?** A candidate row closes on EITHER of two
   kinds of evidence, and both may come from outside the brief — that is the usual place they live:

   - **Completion evidence** → `completed (evidence: <ref>)`. The requirement is absent because the
     work is finished: a merged change, a passing test, the artifact existing, a ticket closed.
     **Look for this outside the brief.** Accepting completion evidence only from inside the brief
     is the asymmetry that turns this method paranoid — a "remaining work is X" handoff names what
     is left, not what is done, so a finished requirement is silent by construction. Most candidate
     rows close here, and closing them is the normal outcome, not a concession.
   - **Decision evidence** → `descoped (decision: <ref>)`. Someone chose to drop it. Ideally a
     named decider, a place it is recorded, and a date; **decider-or-record plus a date is enough**
     to close it as `decision partially traced`. Demanding all three closes nothing in practice —
     verified against this repo's own proposals ledger, which records outcomes and dates but has no
     decider field at all, so a strict three-of-three would reopen every descope we have ever made.

   Only a row with neither is an `unresolved omission`. The brief's own silence is not evidence;
   "obviously out of scope" is not evidence; confident tone is not evidence; and the brief's author
   certifying their own descope when challenged is not evidence either — that is the same person's
   silence with a signature on it. Skip this gate and the method distrusts every handoff and becomes
   unusable.
6. **Emit, do not block.** **If every row closed, say so in one line and stop** — "12 requirements,
   all traced, no unresolved omissions" is the expected result on a healthy handoff, and producing a
   full table anyway trains people to skim it. The table earns its space when something is open.
   Publish the diff table plus one line per unresolved omission, addressed to the brief's author or the named decision-maker, then get on with the work. Make silence visible; do not hold the queue.

## Example
Origin ticket: *ship reporting — schema migration, backfill historical rows, wire the UI.* Brief: *"Schema migration complete; remaining work is wiring the UI."*

| # | Requirement (origin) | In brief | Form | Decision? | Verdict |
|---|---|---|---|---|---|
| R1 | Schema migration | mentioned + complete | — | — | ok |
| R2 | Backfill historical rows | **NOT MENTIONED** | silent drop; scope shrunk to what got done | none | **unresolved omission** |
| R3 | Wire the UI | mentioned + complete | — | — | ok |

→ *To the brief's author / ticket owner: R2 (backfill historical rows) is in the ticket and nowhere in the handoff, with no decision recorded. Completed, deferred, or abandoned? Proceeding with UI work meanwhile.* The two backfill errors are mentioned by nobody; only the derived list surfaces R2.

## Origin unreachable
State it in the output, above the table: **"Audit scope: brief only. No origin available; requirement coverage is unverified."** Never quietly promote the brief to the requirement list — that is the drift itself. Request the origin from the sender, and flag the structural risk: **a handoff chain that does not carry its origin forward compounds drift invisibly.** Fix forward by attaching the origin reference to every onward handoff.

## Red flags
- "It says the remaining work is X" — that is the claim under audit, not the scope.
- Planning from the brief without ever opening the ticket.
- A requirement you can only find in your memory of the origin — go read it.
- A row marked `descoped` or `completed` with no reference anyone else could open.

## In this repo (one instance)
Wave and fan-out briefs (`factory`, `/piano`, `subagent-driven-development` task prompts) are the origins to diff against; `pipeline/frontier.json` and `pipeline/ledgers/` hold the artifacts step 5 asks for — with the caveat that `proposals.jsonl` currently records outcome and date but no decider, which is exactly why step 5 accepts decider-or-record rather than both. Completion evidence here is usually a `talents.jsonl` event or the file existing on disk.
