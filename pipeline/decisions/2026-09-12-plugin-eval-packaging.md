# Packaging the library for `claude plugin eval` — done, and the first run was meaningless

**The question, standing since 2026-09-11:** should this library be packaged as a plugin so
`claude plugin eval` can measure it? It was left open on two grounds: the with/without ablation
**doubles** the agent runs, and an `llm` grader *"sees the first 12 and the last 12"* messages of a
trace, so a long run is graded on its ends.

Both grounds were right about the mechanism and wrong about the conclusion, and the measurements are
below. Everything here was run with `--no-publish`: no report left this machine.

## What the tool requires, quoted from the held doc

`knowledge/raw/watch-2026-09-11b/code.claude.com_docs_en_plugin-evals@2026-09-11b.md`:

> To run plugin evals you need: **Claude Code v2.1.269 or later** … A plugin directory with a
> `plugin.json` or `.claude-plugin/plugin.json` manifest, or a skills-directory plugin.

Measured here: `claude --version` is **2.1.269** — exactly the floor, so this was unrunnable until
the version it now has.

And the fact that changes the cost argument:

> Of the six types, `regex`, `tool_used`, `tool_order`, and `file_exists` are computed from the
> transcript and files and **cost nothing**, while `llm` and `baseline` call a judge model.

## The cost objection, answered with numbers

The doubling is real; the **absolute** figure is what the objection never had.

| run | cases | arms × runs | cost |
|---|---|---|---|
| one free-grader case | 1 | 1 | **$0.04** |
| the whole suite, one run each, both arms | 5 | 2 × 1 | **$1.09** |

`--max-cost-usd` is a hard ceiling checked before each run launches, so a bounded run is a flag and
not a hope. A suite built only from free graders pays for the **agent runs** and nothing else — and
the `llm` grader's 12-and-12 window stops being a limitation when no grader is an `llm` grader. That
is what this suite does: **five cases, seven graders, every one of them free.**

## Packaging: a manifest, and one symlink that mattered more

`.claude-plugin/plugin.json` declares the name, version, author and `experimental.evals`.

**But the skills did not load, and finding out why is the whole story of this pass.** A plugin's
skills are read from **`skills/`**; this repo keeps them at **`.claude/skills/`**, which is the
project-local convention. `skills -> .claude/skills` fixes it, and the runtime follows it.
`claude plugin validate` does **not**, and says so:

> This directory is a symlink and nothing in it was read — component directories are read without
> following symlinks. A session loading this plugin does follow it, so validate the real directory
> separately.

So the two commands disagree on purpose: **`claude plugin validate .claude/skills` has to be run as
its own step**, because validating the plugin root now reads zero skills.

## The first run was a green-looking lie, and a positive control caught it

Before the symlink, the suite ran cleanly and reported scores: **4 cases, mean Δ 0.00, every
`tool_used: Skill` grader failing with `Skill called 0x` in BOTH arms.** No error. A report was
written. The doc's own troubleshooting entry says of exactly this shape:

> If the plugin did load and `Δ` is still near zero with your `tool_used: Skill` grader failing,
> that's **usually a real finding**, meaning the skill's `description` doesn't trigger on the
> prompt's phrasing.

Taking that at face value would have recorded **four false routing failures against this library**
and sent someone off to rewrite four descriptions that were never consulted. What settled it was a
**positive control**: one case whose prompt says *"Use the budget-cut-triage skill"* by name. A named
skill that does not fire cannot be a description problem. It scored **0.00** — so the skills were not
reaching the runs at all, and every score in that run was an artefact.

*The failure was not that it errored. It is that it parsed* — for the fourth time in this repo's
recorded history, and the second time today.

## The measurement, with the skills actually loaded

| case | with | without | Δ |
|---|---|---|---|
| `control-skill-named-explicitly` | 1.00 | 0.00 | **+1.00** |
| `routing-budget-will-not-cover-plan` | 1.00 | 0.00 | **+1.00** |
| `routing-green-after-loosening` | 1.00 | 0.00 | **+1.00** |
| `routing-edit-an-existing-skill` | 1.00 | 0.50 | **+0.50** |
| `negative-plain-factual-question` | 1.00 | 1.00 | 0.00 |

**5 of 5 pass, mean Δ +0.70, $1.09.** The negative trigger's Δ of 0.00 is the correct result, not a
weak one: a case asserting *no* skill fires must score the same in both arms, and it is the only
case in the suite that can catch a library that has become trigger-happy.

`routing-edit-an-existing-skill` is a **regression test for a defect found hours earlier the same
day**: `CLAUDE.md`'s capability map had been routing *"edit a skill"* to `writing-skills`, whose own
description refuses the job. The case asserts `skill-description-optimizer` fires and
`writing-skills` does not. Both hold.

## Decision

**Packaged, suite committed, and run by hand — not in CI.** The eval run needs a credential and
spends money, and `kb-check.yml` is deliberately offline and dependency-free. Its own gate for a
skill change stays `desc_headroom`; this suite is what a routing pass runs.

**What this buys that nothing here had:** the library's descriptions have never been measured against
a baseline, only reasoned about. `capability-routing-table` names that gap in its own premise section
("not validated as beating a baseline that can see the same listing"), and a `tool_used: Skill`
grader in a two-arm run is precisely that baseline, for free.

**Next, when someone spends the budget:** the default is 3 runs per case, so this suite is ~$3.30 —
one non-deterministic run per case is a smoke test and not a measurement. The cases to add are the
collisions in the 36 map lines that assert a boundary, one case per pair, each with a
`did-not-fire` grader on the sibling.

## The real measurement, 2026-09-12 — 30 runs, and the three runs per case agree exactly

The section above was a **smoke test**: one run per case, which for a non-deterministic agent tells
you the plumbing works and nothing about stability. Run at the tool's default of 3 runs per case,
both arms — **30 agent runs, 893 s, $3.41**:

| case | with | without | Δ | spread across its 3 runs |
|---|---|---|---|---|
| `control-skill-named-explicitly` | 1.00 | 0.00 | **+1.00** | none |
| `routing-budget-will-not-cover-plan` | 1.00 | 0.00 | **+1.00** | none |
| `routing-green-after-loosening` | 1.00 | 0.00 | **+1.00** | none |
| `routing-edit-an-existing-skill` | 1.00 | 0.50 | **+0.50** | none |
| `negative-plain-factual-question` | 1.00 | 1.00 | 0.00 | none |

**5 of 5 pass, mean Δ +0.70, and not one case varied between its three runs** — every with-arm run
scored identically and every without-arm run scored identically, in both directions. For a suite
whose graders ask *which skill fired*, that is the useful result: **routing on these prompts is not
a coin flip**, so the smoke test's numbers were right for a reason and not by luck. It also means
three runs is more than this suite currently needs, and the honest conclusion is not "use one run"
but "this is what the variance is, measured, and it can be re-measured when a case is added."

Cost scaled as expected — $1.09 for 10 runs, $3.41 for 30 — so the per-run figure is stable at
roughly $0.11 and a budget for this suite is now arithmetic rather than a guess.

### One run hit the turn limit and still scored 1.00, which is a limitation and not a bug

`routing-edit-an-existing-skill` run 1 ended `exit 1: Reached maximum number of turns (8)`. It
scored **1.00 anyway**, because both its graders are `tool_used` checks on *which skill fired*, and
that happens in the first turns. The other two runs of the same case finished and scored the same.

**Recorded rather than patched, because the honest fix is not a turn limit.** A score that does not
depend on the run finishing is exactly what a routing suite measures, and saying so is more useful
than hiding the error line: raising `max_turns` would cost more for no extra signal, and lowering it
would make every run truncate. What it names is the suite's **ceiling** — these five cases can prove
*the right skill is selected* and nothing about whether the work was any good. **To claim more than
routing, a case needs an outcome grader (a `regex` over a produced file, or an `llm` on a short
answer), and only then does `max_turns` have to be high enough to reach an outcome.** That is the
next case's design problem, not this one's defect.

### And the harness could not seal its own scaffold, because it ran as root

The run printed a warning worth keeping, since it is a property of running this in a container as
root rather than of the suite:

> could NOT seal what the plugin under test wrote (the harness is running as root, which a directory
> mode does not bind) — everything in it except `out/` and `config/` may be agent-written … do not
> run git or anything that loads configuration from a working directory anywhere inside, and remove
> it

Removed with the exact command it gave, from outside the directory, without entering it and without
running git anywhere inside. **A sandbox that tells you it did not hold is doing its job**; one that
failed silently would have left an agent-writable tree in `/tmp` with a `config/` a later command
could have loaded. Worth knowing before anyone runs this suite unattended: as root, the OS-level
confinement the docs describe is not in force, and the scaffold has to be cleaned up by hand.

