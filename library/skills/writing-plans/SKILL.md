---
name: writing-plans
description: "Use when a spec or an approved set of requirements exists and the work needs to be turned into an ordered, executable plan document before any code is written — decomposing it into separately-rejectable tasks with file structure, interfaces, global constraints, and an observable success criterion per task. Triggers: 'write a plan for this', 'break this spec into tasks', 'plan before implementing', 'turn this into an implementation plan'. Scales DOWN as well as up: work with fewer than two separately-rejectable tasks AND confined to a single file, session, and executor needs an edit, not a plan document. NOT for deciding WHAT to build or exploring intent before a spec exists (use brainstorming), NOT for executing a plan that already exists (use subagent-driven-development), NOT for recovering what existing code already does (use behavioral-spec-mining). NOT for deciding what to cut when the budget will not cover the plan (use budget-cut-triage)."
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `using-git-worktrees` skill at execution time.

**Save plans to:** wherever the project keeps plan documents, named so they sort chronologically
(e.g. `<plans-dir>/YYYY-MM-DD-<feature-name>.md`). User or project preference always wins.

## Scope Check

**Scale down as well as up.** Write a plan when there are at least two separately-rejectable
tasks, or when the work spans multiple files, sessions, or executors. Below that, say so and make
the edit — a one-line change does not need a dated plan file, a mandatory header, and an executor
menu. **Requiring ceremony the work does not need is as much a plan failure as omitting a step**,
and it is the failure a planning skill is biased toward, because producing a plan always looks
like doing the job. (Its sibling `brainstorming` carries the same down-branch: "implement via
normal workflow, no plan doc".)

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Spec:** [path to the spec/design doc this plan implements — the plan
argues from the spec, so the spec travels with it; executors read both]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Sequencing a wide refactor (when vertical slices are not available)

**Precondition — check this before using the section.** This is for a refactor whose call sites you
can change in your own codebase and verify with your own build. If the old and new forms must be
valid *simultaneously in production* — a live schema, a deployed interface, other people's code or
persisted data still reading the old shape during a rollout window — stop and use
`expand-contract-migration` instead. The vocabulary below is deliberately the same, and that is the
trap: this section has no reader/writer-lag split, no dual-write gate, no backfill, and it uses a
caller search as the removal oracle, which is the wrong oracle when the callers are persisted rows
or a partner's client. It is a strict, less-safe subset for the live case.

Most plans decompose into vertical slices, each shippable on its own. Some do not: a change to a
widely-used form — a function signature, a type, a module boundary with many call sites — has a
blast radius that makes "one slice, end to end" impossible, because the first slice breaks
everything else.

Sequence those as **expand → migrate → contract**, and make each phase its own task:

1. **Add the new form beside the old one.** Both valid at once. Nothing is migrated yet, and the
   build stays green.
2. **Migrate call sites in blast-radius-sized batches**, each batch its own task with its own
   success criterion, and each leaving CI green. Size the batch by what you can review and revert
   as a unit, not by what is convenient to type.
3. **Delete the old form** — a separate, final task, once nothing references it. This is the only
   irreversible step, so it never shares a task with anything else.

The plan's task list should make it impossible to do step 3 early: give it an explicit success
criterion naming the evidence that no caller remains.

*(Distinct from the `expand-contract-migration` talent, which handles a LIVE schema or deployed
interface where old and new code run simultaneously against real data and a rollout window is in
play. This section is about how to ORDER the tasks of a wide refactor in a plan.)*

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Header and Global Constraints:** The header block is copied VERBATIM into every task's
context by the executor, so scan it with the same placeholder rules you applied to the steps —
a bracket placeholder left in the header propagates into every task instead of just one. Confirm
the Global Constraints block says what actually constrains this work, not a generic restatement.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

**Re-entry:** if the spec changes after the plan is written, this review is not one-shot — re-run
it against the NEW spec rather than patching the plan from memory. A plan silently diverging from
its spec is the failure this checklist exists to prevent, and it is invisible in the plan itself.

**Optional escalation:** for a long or high-stakes plan, `plan-document-reviewer-prompt.md` in
this skill's directory is a ready-made prompt for handing the finished plan to a fresh reviewer.
That is a deliberate extra pass, not a replacement for the checklist above — the checklist is
always run by you.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `<plans-dir>/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute the tasks in this session yourself, with a checkpoint after each task for review

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- Work the plan top to bottom in this session; stop at each task's checkpoint and confirm its
  success criterion before starting the next
- No sub-skill is required for this path

## In this repo (one instance of the general method)
- Plans live under `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`.
- Upstream chain: `brainstorming` produces the spec this consumes; `subagent-driven-development`
  executes the plan and copies this plan's Global Constraints block verbatim into every task
  reviewer's rubric — which is why constraint wording here is load-bearing downstream.
- The pytest/Python examples above are illustrations; the method is language-agnostic.
