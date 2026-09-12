## Q1

**Note on the contract, first.** The method says the field rules are read from the contract
file at the moment each field is written, never from memory. I was told not to open
`pipeline/contracts/skill.contract.json` or `pipeline/validate/`, so two fields below —
**description** (length cap, person, phrasing) and **frontmatter** (which keys survive
packaging, invocation policy) — are written but **not contract-checked**. They are marked
UNCHECKED. Under rule 2 ("a red field never proceeds") they are not clear to ship until the
code checker has been run over the whole artefact. Everything else here is complete.

### 4.0 Bill of materials (before any file exists)

| File | Kind | Why needed | Status |
| --- | --- | --- | --- |
| `terraform-plan-destroy-review/SKILL.md` | body | the method itself | needed |
| `assets/verdict-template.md` | asset | the observed failure is a missing verdict line and unnamed destroys; the output has a fixed shape, so it gets slots | needed |
| `references/*.md` | reference | not needed because — the skill makes no claim about Terraform semantics of its own. The one factual dependency (the JSON key names in `terraform show -json`) would need a dated, quoted source; I have not fetched one, so the body instructs the reader to read the key off their own plan rather than asserting it. If a future run needs the key names asserted, that is a new row, not an improvisation. |
| `scripts/` | script | not needed because — every step is one shell command the reader runs directly; nothing here is worth wrapping | not needed |
| `evals.md` | test | required before commit by the repo's test-before-commit rule; scenarios are the two probe runs replayed plus a zero-destroy plan and a negative trigger | needed (not written here; out of the scope of "give me the SKILL.md") |

Reverse check at the end: planned files that never appeared — `evals.md` (open task, named above).
Files that appeared unplanned — none.

### 4.2 Asset — `assets/verdict-template.md`

    # Terraform plan review — <plan file or PR>
    Plan read: <path to plan.json>            Date: <YYYY-MM-DD>
    Summary line as printed by Terraform: <N to add, N to change, N to destroy>

    ## Resources destroyed (action includes delete)
    | # | Resource address | Action (destroy / replace) | Why it is going |
    |---|------------------|----------------------------|-----------------|
    |   |                  |                            |                 |

    Row count above: <N>   Terraform's destroy count: <N>   Match: <yes/no>
    (If there are none, write exactly: "0 resources destroyed.")

    VERDICT: <GO | NO-GO | HOLD>

### 4.3–4.8 The file

````markdown
---
name: terraform-plan-destroy-review
description: >-
  Use when someone asks whether a Terraform plan, `terraform apply`, or an
  infrastructure PR is safe to run — "is this plan safe", "review my terraform
  plan", "can I apply this", "what does this destroy", "does this recreate the
  database", "0 to add, 0 to change, 2 to destroy", plan output pasted into a PR
  or CI log, a plan showing forces replacement or must be replaced. Reads the
  machine-readable plan, names every resource whose change includes a delete
  (destroy and replace alike), reconciles the count against Terraform's own
  summary line, and ends in one verdict line: GO, NO-GO or HOLD. Not for writing
  or refactoring Terraform, not for cost or drift analysis, and not for reviewing
  the state file — only the plan of a change that has not been applied.
---

# Terraform plan destroy review

## What this is

A read of a Terraform plan that ends in a written go/no-go and names, individually,
every resource the plan will delete.

## When to use it

Someone is about to apply a plan, or is asking a reviewer to sign it off, and the
question that actually matters is "what disappears if I run this". Use it on a plan
that has not been applied. Do not use it to author Terraform, to price a change, or
to reason about drift between state and reality — those are different jobs and this
method will not do them.

## Steps

Every rule below is here because a run failed without it. The two runs are the probe
runs of 2026-08-30, unaided: **Run A** listed all 14 changed resources and concluded
"looks fine"; **Run B** listed them, flagged one replacement, and concluded "should be
safe". Neither named the two resources marked for destruction; neither produced a
verdict line.

1. **Read the machine-readable plan, not the rendered summary.** Run
   `terraform show -json <planfile> > plan.json`. Checkable: `plan.json` exists and
   parses. *(Runs A and B both worked from rendered text, which is why a replacement
   read as one line among fourteen.)*

2. **Extract every resource whose change actions contain a delete.** From
   `plan.json`, take `resource_changes[]` and keep every entry whose `change.actions`
   array contains `delete` — this catches both a plain destroy (`["delete"]`) and a
   replacement (`["delete","create"]` or `["create","delete"]`). Read the key names off
   your own file rather than trusting this sentence. Checkable: one table row per kept
   entry, each row carrying the resource address verbatim. *(Run A produced zero such
   rows; Run B produced one and did not label it a deletion.)*

3. **Name them individually, in the table, never in aggregate.** "Some resources will
   be replaced" is not a row. Checkable: every row has an address that can be pasted
   back into `terraform state show`. *(Both runs described the change set as a whole
   and neither named the two destroyed resources.)*

4. **Reconcile your count against Terraform's.** Compare your row count to the
   `destroy` figure in the plan's own summary line. Checkable: the two numbers are
   written next to each other and are equal. If they differ, stop and re-extract —
   do not write a verdict off a table you know is wrong. *(This is the step that would
   have caught Run A: fourteen changes reviewed, two destroys never surfaced.)*

5. **State the zero case explicitly.** If nothing is deleted, write the words
   "0 resources destroyed." Checkable: the string is present. Silence is not a finding
   and cannot be distinguished from not having looked. *(Runs A and B are both
   indistinguishable from a run that never checked.)*

6. **End with the verdict line, as the last line, in this exact form:**
   `VERDICT: GO`, `VERDICT: NO-GO`, or `VERDICT: HOLD`. HOLD is for a plan you could
   not fully read. Checkable: the last line of the review matches
   `^VERDICT: (GO|NO-GO|HOLD)$`. *("looks fine" (Run A) and "should be safe" (Run B)
   are both readings, not verdicts — neither can be acted on or disagreed with.)*

## Pointers

- `assets/verdict-template.md` — the review's output shape: the destroy table, the
  count reconciliation, and the verdict line. Open it at step 2, before you start
  filling in rows, so the table exists before the findings do.
````

**Field record for this artefact** (what the method says to keep, per field):
code rules red — unknown for `description` and frontmatter, because the checker was
not run; reader questions — not yet handed to an independent reader; rewrites — 1
(step 4 of the draft body originally asked the reviewer to judge whether each destroyed
resource was data-bearing; cut, because no probe run failed on that, and a rule with no
observation is an opinion that costs context on every invocation).

## Q2

No. Four things are wrong with it and one of them is structural.

1. **It was written first.** It describes the skill you meant to build. The body scopes
   to one job — naming destroys and emitting a verdict — and the description promises
   drift, provider versions, module structure, variable precedence, workspaces and
   backends. The router will fire this skill on jobs it cannot do.
2. **It is written in the vocabulary of the solution, not the symptom.** Nobody types
   "comprehensive guide to reviewing infrastructure-as-code". They type "is this plan
   safe to apply", "what does this destroy", "forces replacement", or they paste
   "2 to destroy". None of those words appear.
3. **It has no trigger.** "This skill helps with Terraform" is a topic label. A topic
   label collides with every other Terraform-adjacent unit in the library by
   construction — put it beside any neighbour and ask which one a router picks for the
   neighbour's job, and there is no answer either way. Under 4.7 that means one of the
   two descriptions is wrong, and here it is this one.
4. **Length and phrasing are contract questions I could not check** (I was told not to
   open the contract). It is ~490 characters, so a cap is probably not what kills it —
   but "This skill helps with…" is first-person-ish framing of the unit rather than the
   trigger, and that is exactly the kind of rule the contract states and the code
   checker enforces. Run the checker before arguing about the wording.

Use the description in the Q1 file instead: it is written from the finished body, and its
last sentence exists only to lose the router's coin-flip against the neighbours (writing
Terraform, cost, drift, state review).

## Q3

Nothing gets built on top of them yet. In order:

1. **Check the order first.** If the description was drafted at the same time as the
   body rather than after it, it is not a description, it is an intention — reread it
   against the finished body's actual scope and rewrite anything the body no longer
   does. A description that survives this untouched is fine; one that does not was
   never checked.
2. **Run the code checker on the whole artefact**, not on the two fields you just wrote.
   Cross-field rules (name vs directory, pointers vs files that exist, frontmatter keys)
   can only go red once both fields exist. Anything red stops here — fixing a field
   later means every field written after it was written against something that changed.
3. **Then, and only then, hand each field to a reader who did not write it**, one at a
   time, giving them the field, the contract rule, and nothing else — no probe
   transcript, no reasoning, no draft history. Their questions are fixed:
   - body/what-and-when: *would a reader who has this problem recognise it here in one
     line?*
   - the steps: *is every rule traceable to a named observation, and does every step end
     in something checkable?*
   - description: *which unit would a router pick for the nearest neighbour's job, and
     why not this one?* Give them the neighbour's description too — this question cannot
     be answered from one description alone.
4. **Close the bill of materials in both directions** — planned files that never
   appeared, files that appeared unplanned.
5. **Record the row**: per field, which code rules went red, which reader questions went
   red, how many rewrites. That record is the only thing that will later tell you which
   field costs the most rework.

"Both look right to me" is the one piece of evidence that does not count: you can see how
they were written, and the reader's value is that they cannot.

## Q4

Nothing yet — the description is still the last field, and being short on time does not
move it.

It is the field with the least text and the most leverage: it is the router's only input,
so a wrong one does not degrade the skill, it makes the skill fire on the wrong jobs and
stay silent on the right ones — a failure that shows up as other work going wrong, weeks
later, with nothing pointing back here. And it is the field that cannot be written early:
it needs the finished body's real scope, the trigger vocabulary, and the neighbours'
descriptions to sit beside.

If time is genuinely short, cut somewhere it is recoverable: fewer references, fewer
steps, ship with three rules instead of six, defer the asset. Those are visibly
incomplete and can be added later. A rushed description is invisibly wrong.

If the skill must ship this hour and the description cannot be done properly, the honest
option is to ship it non-auto-invocable (invoked by name only) and write the description
when the body has stopped moving — a skill nobody routes to beats a skill routed to
wrongly.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-contract.with.txt` — the method and its bundled `references/field-writing.md`, which is the whole basis for the answers above.
- `/home/user/skills-repo/CLAUDE.md` — repo standing rules (test-before-commit, description discipline), loaded as project context.
- Not consulted, by instruction: `pipeline/contracts/skill.contract.json`, `pipeline/validate/skill_contract.py`, and everything else under `pipeline/skills/`. Consequences of that gap are flagged inline in Q1 and Q2.
- No skills or tools were invoked; no other files were opened.
