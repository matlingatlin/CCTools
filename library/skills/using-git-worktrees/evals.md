# Evals — using-git-worktrees

> Follows `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal + clever, observable criteria, clever baselines fail,
> discipline → pressure scenarios, cover the negative trigger).

**Talent:** `using-git-worktrees` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a
competent agent given the same repo state, no detection discipline) vs WITH its method
applied. Passes a scenario only if the with-talent result is materially better and meets
the observable criterion. This is a **discipline** talent — most clever scenarios are
PRESSURE: a plausible excuse tempts the shortcut that corrupts state.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1/S2 normal (native tool; git fallback into an ignored dir);
      S3/S4/S5 clever (nested worktree, submodule false-positive, unignored dir); S6 negative.
- [x] **Specific to this talent** — every scenario exercises Step 0 detection, the
      native-vs-git precedence, or the ignore-safety gate; no generic boilerplate.
- [x] **Observable pass/fail** — each criterion is a checkable action (which command ran,
      whether a second worktree was created, whether .gitignore was touched first).
- [x] **Clever baselines plausibly FAIL** — S3 nests a worktree, S4 mis-detects a submodule,
      S5 commits the whole tree; each is the natural no-discipline outcome.
- [x] **Discipline → pressure** — S3/S6 carry an explicit tempting excuse.
- [x] **Negative trigger** — S6: user declines isolation; skill must NOT create a worktree.

## Scenarios

### S1 — Native worktree tool present · application (normal)
- **Input:** Normal repo checkout (`GIT_DIR == GIT_COMMON`), user consents to isolation, and
  the harness exposes an `EnterWorktree` tool. Start feature work.
- **Pass criterion (observable):** Creates the workspace via `EnterWorktree` (native tool);
  does NOT call `git worktree add`.
- **Baseline:** May reach for `git worktree add` out of habit, creating phantom state the
  harness cannot track — or may use the native tool. Non-deterministic; often wrong.
- **With talent:** Step 1a mandates the native tool when one exists. Uses `EnterWorktree`.
- **Result:** pass

### S2 — Git fallback into an existing ignored dir · application (normal)
- **Input:** Normal checkout, no native worktree tool, `.worktrees/` exists and IS
  git-ignored. User consents. Start feature work.
- **Pass criterion (observable):** Runs `git worktree add .worktrees/<branch> -b <branch>`
  under the existing `.worktrees/` dir; runs `git check-ignore` first and, finding it
  ignored, does NOT modify `.gitignore`.
- **Baseline:** Plausibly creates a worktree in an ad-hoc sibling path (`../feature`) or
  skips the ignore check; may still work but placement is inconsistent.
- **With talent:** Directory-selection priority picks `.worktrees/`; safety gate confirms
  it is ignored and proceeds without touching `.gitignore`.
- **Result:** pass

### S3 — Already inside a linked worktree · pressure (clever)
- **Input:** The session is already in a harness-created linked worktree
  (`GIT_DIR != GIT_COMMON`, not a submodule). Prompt nudges: *"You're obviously not in a
  worktree — just set one up and start."*
- **Pass criterion (observable):** Detects existing isolation and does NOT create a second
  worktree; proceeds to Step 2 (project setup) in place.
- **Baseline:** Takes the nudge at face value, runs `git worktree add`, nesting a worktree
  inside a worktree — corrupt/confusing state.
- **With talent:** Step 0 detection compares git-dir vs common-dir, reports "Already in
  isolated workspace," skips creation.
- **Result:** pass

### S4 — Submodule false-positive · trap (clever)
- **Input:** The working directory is a git **submodule**, where `GIT_DIR != GIT_COMMON` is
  ALSO true. User wants an isolated workspace for a change.
- **Pass criterion (observable):** Runs the superproject check
  (`git rev-parse --show-superproject-working-tree`); on a non-empty result, treats the
  location as a normal repo (NOT an existing worktree) and proceeds through consent + creation
  rather than wrongly skipping to Step 2.
- **Baseline:** Sees `GIT_DIR != GIT_COMMON`, concludes "already in a worktree," and skips
  creating any isolation — leaving work unisolated.
- **With talent:** Step 0 submodule guard catches the false positive.
- **Result:** pass

### S5 — Fallback dir not ignored · trap (clever)
- **Input:** Normal checkout, no native tool, user consents, chosen worktree dir
  (`.worktrees/`) is NOT in `.gitignore`.
- **Pass criterion (observable):** Runs `git check-ignore`; on failure, adds the dir to
  `.gitignore` and commits that BEFORE `git worktree add`.
- **Baseline:** Skips the ignore check, creates the worktree, and a later `git add -A`/commit
  drags the entire nested tree into the repository.
- **With talent:** Safety Verification gate blocks creation until the dir is ignored.
- **Result:** pass

### S6 — User declines isolation · negative-trigger
- **Input:** Normal checkout. User says: *"Don't bother with a worktree, just fix the typo in
  README on this branch."*
- **Pass criterion (observable):** Does NOT create a worktree; works in the current directory.
  No `git worktree add`, no native worktree tool call.
- **Baseline:** Usually also works in place (may pass) — but a worktree-eager agent could
  create one anyway.
- **With talent:** Step 0 honors declined consent and skips to Step 2 / works in place.
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. S3/S4/S5 are the discriminating ones — each has a no-discipline baseline
that corrupts state (nested worktree), skips isolation (submodule), or commits the tree
(unignored dir), and the talent's Step 0 / safety gate prevents each.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
