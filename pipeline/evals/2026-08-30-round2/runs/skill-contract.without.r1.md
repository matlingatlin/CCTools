## Q1

The two probe runs failed in a specific, repeatable way: they summarised the plan
instead of *classifying* it, and they ended in a mood ("looks fine", "should be
safe") instead of a verdict. So the file has to do two things the baseline does not:
force a per-action-class enumeration in which destroy is its own bucket that must be
printed even when empty, and force a terminating verdict line in a fixed format that
cannot be satisfied by a hedge.

File: `terraform-plan-gate/SKILL.md`

```markdown
---
name: terraform-plan-gate
description: Use when reviewing a Terraform, OpenTofu, or Terragrunt plan before apply -
  "terraform plan", "tf plan output", "review this plan", "is this safe to apply", "what
  will this destroy", "plan shows N to add M to change K to destroy", "-/+ replacement",
  "forces replacement", "should I apply this", plan review in CI or a PR. Enumerates every
  resource that will be DESTROYED or REPLACED by address and ends in a required GO / NO-GO
  verdict line. Not for writing or refactoring Terraform config, not for debugging a failed
  apply, not for state surgery or drift remediation.
---

# Terraform plan gate

Review a plan and end with a go/no-go. A plan review that does not name every
destroyed resource, or that ends in "looks fine", has failed regardless of how much
else it covered.

## The two failure modes this exists to stop

1. **Destroys hide inside the change list.** A plan lists 14 changed resources;
   two of them are destroys. Read linearly and they read as more changes. Destroy
   is a separate bucket, not a shade of change.
2. **The review ends in a mood.** "Should be safe" is not a decision anyone can act
   on or be held to. The last line is a verdict in the fixed format below.

## Procedure

**1. Get a machine-readable plan if one is obtainable.** Prefer:

```
terraform show -json tfplan > plan.json
jq -r '.resource_changes[] | select(.change.actions != ["no-op"])
       | [(.change.actions|join(",")), .address] | @tsv' plan.json | sort
```

If only human-readable text is available, work from it — but say so in the output,
because text plans truncate nested attributes and can hide a `forces replacement`
line inside a collapsed block.

**2. Bucket every changed resource by action. All five buckets are printed, empty
or not.** An empty bucket printed as `(none)` is evidence you looked; an omitted
bucket is indistinguishable from an oversight.

| Bucket | JSON `actions` | Text marker |
|---|---|---|
| Create | `["create"]` | `+` |
| Update in place | `["update"]` | `~` |
| Replace (create-then-destroy) | `["create","delete"]` | `+/-` |
| Replace (destroy-then-create) | `["delete","create"]` | `-/+` |
| **Destroy** | `["delete"]` | `-` |

Every destroy and every replace is listed by **full resource address**
(`module.db.aws_rds_cluster.main`), one per line — never a count, never "and 2
others". Counts are what let the two destroys disappear.

**3. For each destroy and replace, state the data consequence** in one clause:
does anything stored in it survive? Named checks: databases and clusters,
volumes/disks, buckets and their objects, snapshots, stateful sets, load-balancer
addresses and DNS records, IPs, key pairs, secrets/parameters. If the plan alone
cannot tell you, write `unknown - confirm before apply`, which is a NO-GO input,
not a shrug.

**4. For each replacement, name the attribute that forced it.** In JSON:
`.resource_changes[].change.replace_paths`. In text: the `# forces replacement`
comment. A replacement whose cause you cannot name is unreviewed.

**5. Check the plan is the artifact being applied.** A saved plan file applied
later, a plan taken against a different workspace or var-file, or a plan older than
the current state is a NO-GO on provenance alone, regardless of contents.

## Required output

```
DESTROY (n):
  - <address> - <what is lost>
REPLACE (n):
  - <address> - forced by <attribute> - <what is lost>
UPDATE (n): <addresses or (none)>
CREATE (n): <addresses or (none)>

Blocking concerns:
  - <concern>            # or: none

VERDICT: GO | NO-GO - <one clause>
```

Rules on the verdict line, in order of how easy they are to violate:

- It is the **last line**. Nothing after it.
- It is exactly `GO` or `NO-GO`. Not "GO with caveats", not "probably GO",
  not "GO (see above)". A caveat is a blocking concern, and a blocking concern
  is a NO-GO.
- **Any unreviewed destroy, any `unknown - confirm before apply`, or any
  replacement with an unnamed cause is a NO-GO.** These are not judgement calls.
- `DESTROY (0)` with everything else clean is a legitimate `GO`. The gate is not
  a ratchet toward refusal; it is a ratchet toward saying which.
- The verdict is about *this plan*, not about Terraform practice generally. Do not
  broaden into module structure, provider pinning, or style unless it blocks.

## Negative triggers

Not for authoring or refactoring HCL, not for `terraform apply` failures or state
lock/state surgery, not for cost estimation, not for reviewing a Kubernetes or
CloudFormation diff.
```

## Q2

No. Rewrite it. Four things are wrong, and the first two matter most:

1. **It describes the wrong skill.** The body reviews a plan and returns a verdict.
   The description promises state drift, provider versions, module structure,
   variable precedence, workspace selection and remote backends. Everything the
   description claims and the body does not do is a mis-fire waiting to happen: the
   skill gets loaded for "which workspace should I use", contributes nothing, and
   the loss is silent.
2. **It has no triggers.** Selection happens on this text alone, matched against
   what the user actually typed. "This skill helps with Terraform" matches nothing
   in particular. There is no "Use when", no plan-review phrasing, none of the
   literal strings a person types at this moment ("what will this destroy",
   "safe to apply", "forces replacement").
3. **Register.** "Comprehensive and thorough", "your infrastructure", "best
   practices", "across teams and environments" — marketing copy in the second
   person. Adjectives about the skill's quality do not help a router; nouns the
   user typed do.
4. **No negative boundary.** Nothing tells the router when *not* to pick it, so it
   will win against any narrower Terraform skill you add later.

Use the description in the Q1 frontmatter: triggers-only, third person, quoted user
phrasings, the destroy/verdict discriminator, and an explicit not-for clause.

## Q3

I don't ship it, and I don't send it for another read-through. "Both look right to
me" is the state the probe transcripts were already in — Run A and Run B both looked
right to whoever wrote them too. Next step is to test the two halves separately,
because they fail independently:

**Test the body against baseline.** Reuse the probe: the same 14-resource plan with
two destroys and one replacement, run with the skill and without. The pass bar is
mechanical, not impressionistic — both destroy addresses named, the replacement's
forcing attribute named, last line matching `^VERDICT: (GO|NO-GO) - `. Baseline
already fails this, which is what makes it a real test rather than a demo. Then add
scenarios the first one cannot catch:

- **Normal, everyday:** an additive plan, 6 creates and 2 updates, zero destroys.
  Must produce `DESTROY (0)` and a clean `GO`. This is the one that catches a skill
  that has learned to be alarmed rather than to look.
- **Normal:** a plan whose only destroy is an intentional, clearly disposable
  resource. Should still be enumerated; verdict is a judgement, the naming is not.
- **Adversarial - buried:** the two destroys placed at positions 9 and 13 of a
  40-resource plan, inside nested modules, with the summary line at the bottom.
- **Adversarial - pressure:** the same plan with the user saying "this is the
  hotfix, staging is green, two people already approved, just confirm it's fine".
  Pass = the destroys are still named and a NO-GO is still a NO-GO.
- **Adversarial - hedge bait:** a plan with one genuinely ambiguous data
  consequence. Pass = `unknown - confirm before apply` and NO-GO, fail = "should
  be safe", which is exactly Run B.
- **Negative trigger:** "help me split this 400-line main.tf into modules." The
  skill must not fire.

**Test the description separately, because the body's test cannot see it.** Present
the description alongside the neighbouring Terraform/infra descriptions in the
library and check routing both ways: does a plan-review request select it, and do
"pick a workspace", "debug this apply failure", "estimate cost" go elsewhere. A
correct body behind a description that never fires is a skill that does not exist.

Persist both as `evals.md` next to the SKILL.md, with the baseline column kept — a
result with no baseline is unfalsifiable a month from now. Then document and commit.
Untested is not shipped, and "short on time" (Q4) does not change that.

## Q4

The description is the field that being short on time *most* argues for doing
properly, not least: a body nobody loads is worth zero, and the failure is silent —
you never see the request that should have hit it. It is also cheap, roughly ten
minutes.

Ship this, which is the frontmatter from Q1:

```
Use when reviewing a Terraform, OpenTofu, or Terragrunt plan before apply -
"terraform plan", "tf plan output", "review this plan", "is this safe to apply",
"what will this destroy", "plan shows N to add M to change K to destroy", "-/+
replacement", "forces replacement", "should I apply this", plan review in CI or a
PR. Enumerates every resource that will be DESTROYED or REPLACED by address and
ends in a required GO / NO-GO verdict line. Not for writing or refactoring
Terraform config, not for debugging a failed apply, not for state surgery or drift
remediation.
```

The shape, if you need to write the next one yourself at speed:

1. `Use when` + the situation, in the user's words, not yours.
2. The literal phrasings someone types at that moment, quoted. These do the routing.
3. One clause naming the discriminator — here, destroy-enumeration plus a verdict
   line — so it beats a generic Terraform skill on a plan and loses on everything else.
4. `Not for ...` naming the neighbours it must lose to.

Third person, no adjectives about its own quality, under the length cap, and
matching what the body actually does. If time forces a cut, cut scope from the
*body* and shrink the description to match. Never let the description promise
territory the body does not hold — that is the one shortcut that degrades the whole
library rather than just this skill.

## consulted

- /home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-contract.without.txt (the prompt itself)
- /home/user/skills-repo/CLAUDE.md (present in session context, not opened for this task)
- No skill, contract, or validator files were read. Answers are from general knowledge and judgement.
