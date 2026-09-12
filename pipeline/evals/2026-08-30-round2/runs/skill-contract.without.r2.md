## Q1

The probe says the baseline already *lists* changes competently and already *reads* the plan. What it does not do is (a) separate destroys/replaces from the rest of the noise, and (b) commit to a verdict. So the skill must be narrow: extraction of the destructive subset + a mandatory verdict line. Everything else is padding that will make it mis-trigger.

`.claude/skills/terraform-plan-gate/SKILL.md`:

````markdown
---
name: terraform-plan-gate
description: Use when reviewing a Terraform/OpenTofu plan before apply — terraform plan output, tfplan, plan JSON, a plan posted in a PR or CI log, "is this plan safe to apply", "what does this destroy", "review this plan", "can I apply this". Extracts every resource that will be DESTROYED or REPLACED, names each one, and ends with a required GO / NO-GO / GO-WITH-CONDITIONS verdict line. Not for authoring or refactoring Terraform code, not for state-drift investigation, not for module or provider-version review.
---

# Terraform plan gate

A plan review is not a summary. It is a decision with a named blast radius. A review that
does not name every destroyed resource and does not end in a verdict has not been done.

## Inputs

Work from machine-readable output when it exists. If you were given only pasted human
output, say so in the report — the counts below are then read, not parsed.

- `terraform show -json tfplan > plan.json` (preferred), or
- `terraform plan -no-color` text.

## Procedure

**1. Parse the destructive subset first — before reading anything else.**

From `plan.json`, classify every element of `.resource_changes[]` by its
`.change.actions` array:

| `actions` | Class |
|---|---|
| `["no-op"]` | ignore |
| `["read"]` | ignore |
| `["create"]` | create |
| `["update"]` | update |
| `["delete"]` | **DESTROY** |
| `["delete","create"]` | **REPLACE** (destroy-then-create) |
| `["create","delete"]` | **REPLACE** (create-then-destroy) |

```bash
jq -r '.resource_changes[]
       | select(.change.actions | index("delete"))
       | [(.change.actions|join("+")), .address, (.change.before.id // "-")]
       | @tsv' plan.json
```

Also check `.output_changes` for removed outputs, and note any `moved`/`removed` blocks or
`-target` / `-replace` flags in the invoking command — a plan produced with `-target` is a
partial plan and must be flagged as such.

For text output, count the `# … will be destroyed` and `# … must be replaced` headers and
reconcile against the `Plan: X to add, Y to change, Z to destroy` line. **If your named list
is shorter than Z, you have missed resources — go back.** Do not report until the two agree.

**2. Grade each destroy/replace for recoverability.** For every entry from step 1, state in
one clause what is lost and whether it comes back:

- **Stateful / irrecoverable** — databases, disks/volumes, buckets and their objects, PVs,
  secret/KMS material, snapshots, stateful sets. Check `prevent_destroy`, deletion protection,
  final-snapshot settings, and `skip_final_snapshot = true` in particular.
- **Externally-referenced** — anything whose identity others depend on: DNS records, load
  balancer/IP addresses, ARNs and IDs consumed outside this state, IAM roles/policies.
- **Disruptive but recoverable** — instances, tasks, nodes: replaced with downtime.
- **Cheap** — null resources, local files, tags-only churn.

For each replacement, name the attribute that forces it — from `.change.replace_paths` in
JSON, or the `# forces replacement` marker in text. A replacement whose trigger you cannot
name is an unexplained replacement and is by itself grounds for NO-GO.

**3. Sanity-check the context.** Workspace/backend actually selected; the plan file is the
one that will be applied (a re-plan at apply time is a different plan); no unexplained
provider or module version movement.

**4. Write the report.** Required shape, in this order:

```
## Plan review — <workspace/env>, <plan source>

Counts: N to add, N to change, N to destroy   (parsed from plan.json | read from text)

### Will be DESTROYED (N)
- <address> — <what is lost> — <recoverable? how>
### Will be REPLACED (N)
- <address> — forced by <attribute> — <downtime / data impact>
### Other changes (N add, N update)
- one line, grouped; no per-resource detail unless it bears on the destroys

### Conditions / unknowns
- <anything you could not determine, each as an explicit unknown>

VERDICT: GO | GO-WITH-CONDITIONS | NO-GO — <one sentence of reason>
```

## Rules

- **The verdict line is mandatory and is the last line.** Exactly one of `GO`,
  `GO-WITH-CONDITIONS`, `NO-GO`. "Looks fine", "should be safe", "seems reasonable" are not
  verdicts and must not appear anywhere in the report.
- **Every destroy and every replace is named individually, by full resource address.** A
  count without addresses is a failed review. Never write "some resources are replaced".
- **Zero destroys is a finding, not a silence.** Write `### Will be DESTROYED (0)` explicitly
  so the reader can tell the section was checked rather than skipped.
- **Default to NO-GO** when: an irrecoverable resource is destroyed without a stated backup
  or snapshot; a replacement's forcing attribute cannot be named; the plan is stale, partial
  (`-target`), or from a different workspace than the apply will use; or the counts do not
  reconcile.
- **GO-WITH-CONDITIONS must list the conditions as checkable actions** ("take an RDS snapshot
  first", "lower the DNS TTL 24h ahead"), not as advice.
- Report unknowns as unknowns. `(known after apply)` on a destroy target's dependants is not
  evidence of safety.

## In this repo (one instance)

Nothing repo-specific. If your CI posts plans as PR comments, point the skill at the JSON
artifact rather than the comment text — text-only reviews cannot reconcile counts reliably.
````

## Q2

No. Rewrite it.

Three faults, in order of cost:

1. **It describes the topic, not the trigger.** "This skill helps with Terraform" and "comprehensive and thorough guide" tell the selector nothing about *when* to load it. Descriptions are matched against a request; write triggers ("Use when reviewing a terraform plan before apply…", "what does this destroy", "is this safe to apply") and the literal artifacts a user will paste (`terraform plan`, `tfplan`, `plan.json`, OpenTofu).
2. **It over-claims by a mile.** The body does one job: name destroys/replaces and issue a verdict. The description promises state drift, provider versions, module structure, variable precedence, workspace selection, remote backends and general best practice. Every one of those is a false trigger — it will load on "which provider version should I pin?" and then be no help. Description and body must claim the same scope; when they disagree, the description is the bug.
3. **No negative boundary.** Say what it is *not* for, so the neighbours are visible: not authoring Terraform, not drift investigation, not module/provider-version review.

Also: drop "This skill helps with" (wasted tokens, first-person-ish), drop the adjectives — "comprehensive and thorough" is not a trigger word, and it costs you keyword room inside the character cap that the real triggers need.

Use the description from the Q1 frontmatter.

## Q3

Neither of those is the thing that tells you it works, so: **test it before it goes anywhere near a commit.**

Concretely, next actions in order:

1. **Write the evals first, from the probe.** You already have the exact failure that justifies the skill — Runs A and B named zero of the two destroys and produced no verdict. That is scenario #1, and it is the one the baseline must fail.
2. **Build a blend of scenarios, not just traps.** Roughly half everyday: a plan with one clean destroy, a plan with a forced replacement, an adds-and-updates-only plan (must emit `DESTROYED (0)` and `GO`). Roughly half adversarial: a destroy buried at position 40 of 60; a `create+delete` ordering variant; a plan where `Plan: … 3 to destroy` disagrees with the visible blocks; a `-target` partial plan; `skip_final_snapshot = true` on an RDS destroy; pasted text with no JSON. Plus a **negative trigger**: "bump the AWS provider to 5.x across these modules" — the skill must *not* fire.
3. **Run baseline vs with-skill on every scenario.** Same prompts, same inputs, skill absent then present. Grade on the two contract points that the probe showed missing: every destroy/replace named by full address, and a verdict line present as the last line. Persist as `.claude/skills/terraform-plan-gate/evals.md` with the per-scenario result table.
4. **Read the deltas, then fix the file.** If baseline passes a scenario, that scenario is not evidence for the skill — replace it. If with-skill fails one, the body is under-specified, not the eval.
5. Only then: document and commit. Untested is not done, and "both look right to me" is exactly the state in which a skill that never fires, or fires on everything, feels finished.

## Q4

Short on time is not a reason to write the field badly — the description is the *only* part of the skill that runs on every request, and a wrong one costs you the skill entirely (it never loads, or it loads constantly). It is also thirty seconds of work. Paste this:

```yaml
description: Use when reviewing a Terraform/OpenTofu plan before apply — terraform plan output, tfplan, plan JSON, a plan posted in a PR or CI log, "is this plan safe to apply", "what does this destroy", "review this plan", "can I apply this". Extracts every resource that will be DESTROYED or REPLACED, names each one, and ends with a required GO / NO-GO / GO-WITH-CONDITIONS verdict line. Not for authoring or refactoring Terraform code, not for state-drift investigation, not for module or provider-version review.
```

The four parts, if you need to write your own under pressure: **Use when** + the concrete situation; the literal words and artifacts a user will type; what it produces; **Not for** + the two or three nearest neighbours. Third person, triggers only, under the character cap, no adjectives.

What you may not skip to save time is the testing (Q3). A description can be sharpened later from mis-fires you observe; an untested body ships a wrong verdict on a live apply.

## consulted

- /home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-contract.without.txt (the prompt itself)
- /home/user/skills-repo/CLAUDE.md (loaded automatically into context by the harness; not opened by me)
- No skill, contract, or validator files were read.
