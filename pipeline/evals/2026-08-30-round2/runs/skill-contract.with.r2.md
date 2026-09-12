## Q1

Working in the method's order (4.0 BOM → 4.1/4.2 bundled → 4.3 name → 4.4/4.5/4.6 body → 4.7 description → 4.8 frontmatter).

**One flag before the file.** The method says the field rules are read from the contract *at the moment the field is written*, never from memory. I was instructed not to open the contract or the code checker for this exercise, so every field below is written against the method's ordering and evidence rules only. Nothing here has been through `skill_contract.py`. Treat the artefact as **written, not checked** — by rule 2 ("a red field never proceeds") it is not eligible to proceed until the checker has run on the whole file.

### 4.0 Bill of materials

| File | Kind | Why needed | Status |
| --- | --- | --- | --- |
| `terraform-plan-destroy-review/SKILL.md` | skill body | the method itself | needed — written below |
| `references/plan-json-fields.md` | reference | the body asserts the shape of `terraform show -json` (`resource_changes[].change.actions`, `replace_paths`); that is an external claim and needs a verbatim quote + fetch date | **needed, NOT WRITTEN** — I have not fetched the Terraform docs in this run, so I cannot date the quote. This is a task, not an improvisation: the body below is written so it *asserts* the field names at runtime (step 2 fails loudly if they are absent) rather than trusting them silently. |
| `assets/verdict-template.md` | asset | the skill emits a fixed-shape report; a template with slots is what makes the output checkable | needed — written below |
| `scripts/` | executable | — | not needed because the extraction is one `jq` filter that belongs in the step, and a script would hide the assertion the step depends on |
| `references/terraform-best-practices.md` | reference | — | not needed because no probe run failed on module structure, provider versions, backends or drift. There is no observation behind it, so it would be context cost with nothing failing without it. |

Back-check at the end (both directions): planned-and-missing = `references/plan-json-fields.md` (open task, above). Appeared-unplanned = none.

### 4.1/4.2 bundled knowledge

`references/` is deliberately empty pending the dated fetch above. `assets/verdict-template.md`:

```markdown
# Plan review — <plan file> — <date>

Plan counts as reported by terraform: <A> to add, <C> to change, <D> to destroy.
Resource changes parsed from JSON: <N>.  Reconciles: <yes/no>

## Will be destroyed (actions == ["delete"])
| # | address | type | replaced by nothing / superseded by | data at risk (y/n/unknown) |

## Will be replaced (actions == ["delete","create"] or ["create","delete"])
| # | address | type | order | what forced replacement (replace_paths) | downtime window |

## Everything else
<A> created, <C> updated in place — not enumerated here.

VERDICT: GO
VERDICT: NO-GO — <one clause naming the resource that decides it>
(delete whichever line does not apply; exactly one must remain)
```

### 4.3 name

`terraform-plan-destroy-review` — directory `terraform-plan-destroy-review/`, matching. Nothing reserved.

### The file

```markdown
---
name: terraform-plan-destroy-review
description: Use when a Terraform plan must be reviewed before apply and someone needs to know what will be DESTROYED — triggers on "review this plan", "is it safe to apply", "will this delete anything", "what does -/+ mean", "plan says N to destroy", "forces replacement", "sign off on this apply", "go/no-go on this plan". Parses terraform show -json, enumerates every resource change carrying a delete action by full address, separates outright destroy from replacement and create-before-destroy, reconciles the count against Terraform's own summary, and ends in one mandatory VERDICT: GO / NO-GO line. NOT for authoring or refactoring modules, NOT for state drift, provider upgrades, backend or workspace configuration, NOT for cost estimation, NOT for reviewing application source (use code-security-review).
---

# Terraform plan review: what gets destroyed, and a verdict

## What this is

A Terraform plan is reviewed and a written go/no-go is produced that names, by full
resource address, every resource the plan will destroy.

## When to use it

Use it when someone hands you plan output — text or JSON — and asks whether it is safe
to apply, or asks you to sign off on an apply.

Recognise the problem by what a plan review looks like when it goes wrong: the reviewer
lists all the changed resources, says something reassuring, and never names the
resources that are going away. Both probe runs did exactly that (run A: 14 resources
listed, "looks fine"; run B: same list, one replacement flagged, "should be safe").
Two resources were marked for destruction in both plans. Neither run named them.

## Steps

Every step ends in an artefact or a number you can point at.

1. **Get the machine-readable plan.** `terraform show -json <planfile> > plan.json`.
   If you were given only rendered text and cannot re-run `show`, say so and stop:
   the rest of this method reads fields that the rendered output does not carry.
   Checkable: `plan.json` exists and parses.

2. **Extract every change carrying a delete.**
   `jq '[.resource_changes[] | select(.change.actions | index("delete"))]' plan.json`
   If `.resource_changes` is absent or the filter errors, stop and report the plan-JSON
   shape you actually got — do not fall back to reading the rendered diff.
   Checkable: a JSON array of length N, and N is written down.

3. **Split the array into destroy vs replace.** `actions == ["delete"]` is a destroy.
   `["delete","create"]` is a replacement, and `["create","delete"]` is a replacement
   with create_before_destroy — the resource still dies, and the ordering changes the
   downtime story, so the two are not one category.
   Why the split is a rule: run B flagged "one replacement" and stopped there, which
   left both true destroys unnamed and left the reader unable to tell a rebuild from a
   deletion.
   Checkable: each of the N entries is in exactly one of the two lists.

4. **Fill the tables in `assets/verdict-template.md`, one row per entry, no blank
   cells.** Full address, type, and for replacements the `replace_paths` entry that
   forced it. If data-at-risk is unknowable from the plan, write `unknown` — the word
   `unknown` is an allowed answer; an empty cell is not.
   Checkable: row count equals N.

5. **Reconcile against Terraform's own summary.** The plan's "X to add, Y to change,
   Z to destroy" must agree with what you parsed; Z must equal the destroy count plus
   the replace count. If it does not, the plan you read is not the plan they are about
   to apply — stop and say so.
   Why the rule: run A listed 14 changed resources and drew a conclusion without ever
   checking its list against the plan's own totals, which is how two destroys stayed
   invisible inside a correct-looking list of 14.
   Checkable: the "Reconciles: yes/no" line is filled.

6. **Write exactly one verdict line**, in this form and as the last line of the report:
   `VERDICT: GO` or `VERDICT: NO-GO — <one clause naming the resource that decides it>`.
   Why the rule: neither probe run produced a verdict at all. "Looks fine" (run A) and
   "should be safe" (run B) are not verdicts — they carry no address, and a reader
   cannot act on them or be held to them. If N > 0 and no human has confirmed the
   destroys are intended, the verdict is NO-GO.
   Checkable: the report's last line matches `^VERDICT: (GO|NO-GO — .+)$`, and there
   is exactly one such line in the file.

## Pointers

- `assets/verdict-template.md` — the report shape, with the two tables and the verdict
  line. Open it at step 4, before writing any prose, and fill the slots in place.
```

### 4.8 frontmatter policy

Content kind is a technique the model should reach for unprompted when plan output appears, so it stays model-invocable — no `disable-model-invocation`. I have asserted only `name` and `description`; which fields survive packaging is the contract's call and must be confirmed by the checker, not by me.

**Per-field record (owed to `fields.jsonl`):** every row's `code_red` is currently `unrun`, not `0`. Do not let that be read later as a clean pass.

## Q2

No.

Six things wrong, in the order the method would catch them:

1. **It was written first.** It reads as a statement of intent for the skill you meant to build, not the router input for the body in Q1. That is the named failure mode in the method, and it is the root of the other five.
2. **It promises scope the body does not have** — state drift, provider versions, module structure, variable precedence, workspaces, remote backends. The body reviews a plan for destroys. Every one of those phrases is a request this skill will now win and then fail.
3. **Solution vocabulary, not symptom vocabulary.** "Infrastructure-as-code changes", "best practices", "maintainable" are words someone types when they already have the answer. The person with the problem types "will this delete my database", "what does `-/+` mean", "plan says 2 to destroy".
4. **It does not say what the skill actually produces.** The destroy enumeration and the mandatory verdict line — the only two things that distinguish it from a generic reviewer — are absent.
5. **No "Use when", no negative triggers.** Nothing tells a router where the boundary is, so no neighbour can be differentiated from it in either direction.
6. **Filler occupies the budget.** "Comprehensive and thorough", "helps with", "across teams and environments" cost characters and route nothing.

Use the description in Q1's frontmatter instead. And note the same caveat: neither of us has run the checker over it, so "good to go" is not a judgement either of us is entitled to make by eye — the length rule in particular is a code question, not a reading question.

## Q3

Not read them again. "Both look right to me" is the reading that measures worst, because you wrote them.

In order:

1. **Run the code checker on the whole artefact, not on the field you last touched.** Cross-field rules only become checkable once every field exists. Anything red is fixed and the checker is re-run before a reader ever sees it — there is no point spending a reader on a description that is over the cap.
2. **Then hand each field out separately** to a reader who did not write it, with the field and the contract rule and nothing else. Body → "would a reader who has this problem recognise it here in one line?" and "is every rule traceable to a named observation, and does every step end in something checkable?" Description → "which unit would a router pick for the neighbour's job, and why not this one?" Do not give them your reasoning; a critique of your own reasoning measures worse than no critique.
3. **Read the description beside its nearest sibling specifically** — for this skill, whatever else in the library claims plan/diff/change review or pre-ship gating. Ask it in both directions. If either direction is unclear, one of the two descriptions is wrong, and it is not automatically the new one.
4. **Back-check the bill of materials both ways.** Planned files that never appeared (here: `references/plan-json-fields.md` — still an open task), and files that appeared unplanned.
5. **Record the per-field result** — which code rules went red, which reader questions went red, how many rewrites each field took. Skipping this is silent: you lose the only signal that says which field of this method costs the most rework.

And one ordering point: if step 2 or 3 moves the body's scope, the description was written against a scope that no longer exists and is redrafted, not patched. That is the whole reason it is last.

## Q4

Nothing goes in it yet — and being short on time does not change that.

The description is last because it needs three inputs that do not exist earlier: the finished body's actual scope, the trigger vocabulary, and the neighbours it must not collide with. Writing it early under time pressure does not save the work, it moves it: you get a description of the skill you meant to build, and you pay for it on every future request that mis-routes, forever, silently. The unwritten skill costs one task; the mis-routed one costs every task that should have found it.

So the cheapest correct move, if you have ten minutes:

- Freeze the body first. Then write the description from it in one pass — symptoms, error strings, tool names, and the two things this skill uniquely emits (the destroy enumeration, the verdict line) — plus the explicit NOTs.
- Run the code checker. Seconds, and it settles length and format without a human.
- Do the one neighbour comparison, both directions. Skip the wider reader pass if you must; do not skip this one.

If you cannot even do that, ship the skill with the body and leave the description as the blocking task, rather than filling it with a guess. A red field never proceeds — and under time pressure the description is the field most likely to be red and least likely to be noticed.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-contract.with.txt` — the method and its bundled `field-writing.md` (the only source used for the answers)
- No other files were opened. In particular `pipeline/contracts/skill.contract.json`, `pipeline/validate/skill_contract.py` and `pipeline/skills/` were not read, per the instruction — which is why every field above is marked written-but-unchecked.
