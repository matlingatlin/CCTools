---
name: steering-doc-pruning
description: "Use when a document an agent reads on EVERY turn has grown past what it earns — a CLAUDE.md, AGENTS.md, .cursorrules, a copilot-instructions file, a system prompt, or any always-on steering/rules file. Triggers on 'trim CLAUDE.md', 'our rules file is too long', 'the agent ignores our conventions', 'what belongs in AGENTS.md vs a skill', a steering doc grown by accretion where nobody remembers which lines still change behavior, a rules file edited so often the prompt cache never survives a session, or 'don't do X' lines that keep getting violated. Settled by running the doc, not reading it. NOT for measuring which loaded component eats tokens (context-budget ranks the components; this cuts inside one of them), NOT for authoring a new load-on-demand SKILL.md from scratch (writing-skills), NOT for tuning a skill's description so it auto-invokes correctly (skill-description-optimizer), NOT for finding lines a merged diff made FALSE (doc-claim-reconciliation — unearned is not false)."
---

# Steering Doc Pruning

A file an agent reads every turn is not documentation — it is part of the prompt. Every line
is paid for on every turn and competes for attention with the actual task. This talent decides,
line by line, what stays, what is rewritten, and what moves to a file loaded on demand, and it
settles each call by RUNNING the document rather than by reading it.

## When to use
- An always-loaded steering file (CLAUDE.md, AGENTS.md, a rules file, a system prompt) has grown by accretion and nobody can say which lines still change behavior.
- The agent ignores conventions the file states, or a rule keeps getting violated despite being written down.
- Deciding whether a procedure belongs in the always-on file or in an on-demand skill/doc.
- The steering file is edited constantly and sessions feel like they re-pay for it.

**When NOT to use:** you need to know WHICH loaded component (skills, MCP servers, agents, the
CLAUDE.md chain) is eating context — that inventory is `context-budget`, and it stops at the
ranking; this talent cuts inside one file. Authoring a load-on-demand SKILL.md from blank paper
is `writing-skills` (that file loads WHEN NEEDED; this one loads ALWAYS, and the whole method
turns on that difference). Making a skill auto-invoke on the right prompts is
`skill-description-optimizer`.

## Steps
1. **Scope and freeze policy.** Name the exact file(s) read every turn. Mark the protected
   lines (see the no-op test) before touching anything — they are off the table for removal.
2. **Baseline both metrics.** Token size of the whole always-loaded chain, AND compliance on a
   frozen set of real tasks. See "Measure before and after".
3. **Classify every line:** protected / duplicate / prose fat / negation / one-in-twenty detail
   / volatile status / true-but-unproven.
4. **Run the cheap passes** — no experiment needed: delete duplicates, cut prose fat, rewrite
   negations to positives, move one-in-twenty detail and volatile status out.
5. **No-op test what survives.** Only the true-but-unproven remainder earns an A/B.
6. **Re-layout and land ONE revision.** Stable top, volatile bottom or gone; trim + reorder in
   the same single edit (see "The cache test").
7. **Re-measure and verify behavior.** Shorter is not done. Compliance at or above baseline on
   the frozen task set is done.

## The no-op test (run it, don't read it)
A line is a no-op if removing it does not change what the agent DOES. That is a property of a
model-and-task pair, not of the sentence — which is why lines like "Be thorough when you review"
survive every read-through gallery. Settle it by running:

1. Pick 2–3 real tasks from your history where the line would bind if it binds at all.
2. Two arms: the doc as-is, and the doc with that ONE line removed, nothing else changed. One
   line per experiment — two removals at once tells you nothing about either.
3. Define the observable **P** before running: a binary an outsider could check from the result.
   "Tests were run before the commit." "The new file landed in `src/lib/`, not the repo root."
   "It asked before dropping the table." "The ADR exists." Tone, phrasing, and sounding careful
   are NOT P.
4. Run **≥5 fresh sessions per arm**, same task, same starting state, no carryover.
5. Read the verdict off the two rates:
   - **Identical and unanimous** (5/5 vs 5/5, or 0/5 vs 0/5) → no observed effect on these tasks.
   - **P holds less often without the line** (5/5 vs 2/5) → load-bearing. Keep it; stop testing.
   - **Anything mixed or noisy** → undetermined.

**One A/B run decides nothing.** A 5-vs-4 split is what a coin looks like at n=5. You have
enough to cut when both arms are unanimous and identical across ≥5 reps on ≥2 different binding
tasks. Everything short of that is undetermined.

**Default on undetermined: KEEP — the burden of proof is on removal.** The errors are not
symmetric. A wrongly kept line costs a fixed handful of tokens per turn, sits visibly in the
file, and is reversible in one edit. A wrongly removed line costs behavior — diffusely, on the
tasks you did not sample, weeks later, with no error message and nothing pointing back at the
edit that caused it. "Undetermined" means *no evidence it changes behavior*, which licenses
making the line cheaper — compress it, merge it with a neighbor, or (if it is **not** protected
below) move it on-demand — never deleting it.

**Never eligible for no-op removal, whatever the A/B shows:**
- Policy and permission ("ask before deleting", "never push to main").
- Safety and irreversible actions: delete, force-push, deploy, spend money, message anyone external.
- Domain facts the model cannot derive: ports, deploy targets, "the migration runs before the seeder".
- Legal, licensing, and compliance constraints.
- Any rule whose violation **fails open** — silently wrong, caught by no test and no review.

Membership test: *if the agent ignored this line once, would a test or a human review catch it
before it landed?* If no, it is protected. "A capable model does it anyway most of the time" is
not evidence for removal — these lines exist for the tail, and an average-case A/B never samples
the tail. **This method is scoped to LOADING and CLARITY.** It may compress a protected line,
move it to a different place *within the always-loaded file*, or clarify its wording. It may
never weaken, narrow, or delete one. Softening a policy is a different decision and it belongs
to the human who set it.

**And a protected line never leaves the always-loaded file.** Moving one to a load-on-demand file
is functionally a deletion for every turn that does not load it — the same outcome as removal,
reached through a verb this method permits, which is why the rule has to name it. A pointer does
not rescue the move: a pointer only helps a turn that already knows it needs the rule, and the
turn about to drop the table is precisely the turn that was not going to open the ops file.
Protected lines are cheap; the whole protected set is a handful of lines. Pay for them every turn.
So: compress in place, yes. Reposition in place, yes. Relocate out of the file, never — and this
holds however the move is framed (progressive exposure, an appendix, a linked playbook, "it's
still in the repo").

## The cache test
An always-loaded file sits in the cached prefix of every request, so editing it invalidates the
cache from the edit point onward and every remaining turn re-pays the prefix. Two consequences:

- **Cadence: batch.** Land the whole prune as ONE revision, not a trickle of small commits. Do
  not edit the steering file mid-session unless the session is being actively harmed by it —
  a mid-session edit charges the re-read to every turn that follows, so the payoff has to be
  "this run is going wrong now", not "I spotted a typo".
- **Layout: stable at the top, volatile at the bottom.** Rules and conventions change yearly;
  status, current phase, sprint state and TODO lists change weekly, and each such edit
  invalidates everything below it. Anything that changes weekly is usually also something not
  needed every turn — so the honest fix is to move it out, not to reorder it.
- **Reorder in the same revision as the trim.** A later cosmetic reshuffle of the top costs as
  much as a rewrite.

Exact cache mechanics differ by runtime and provider. The invariant: changes near the top cost
more than changes near the bottom, and never-changing content is cheapest of all. Do not quote
numbers you have not measured.

## Negation → positive instruction
"Don't do X" leaves the action space open — the model must invent the replacement, and under
pressure the nearest replacement is a neighbor of X. It keeps X salient, and it is not checkable:
you can observe a violation, never a compliance. "Do Y" is checkable and requires no invention.

Rewrite every "don't / never / avoid" line by asking **what should be done instead**:
- There is an answer → state it. "Don't write vague commit messages" → "Commit messages name the
  subsystem touched and the behavior that changed."
- The honest answer is "nothing — this must not happen" → **keep the prohibition** and sharpen it
  by naming the action and the route out: "Never force-push a shared branch; if history must
  change, ask first." Safety and irreversible actions live here permanently. A positive
  rephrasing of a hard prohibition weakens it.

When the failure is discipline (the agent knows the rule and breaks it under pressure) rather
than clarity, the form question is already answered in `writing-skills` ("Match the Form to the
Failure") — use that, don't re-derive it.

## Progressive exposure
The always-loaded file carries only what a typical turn needs. Observable rule: take your last
~20 real tasks and ask, per line, on how many the agent would have gone wrong without it.
- **Needed on most turns** (house conventions, how to run tests, standing policy) → stays.
- **Needed by about one task in twenty** (release procedure, migration playbook, one integration's
  quirks) **and not protected** → moves to a file loaded on demand, and the always-loaded file
  keeps ONE pointer line carrying the words a matching task would actually contain. Run the
  membership test before every move, not only before a deletion: a protected line used by one
  task in twenty still stays, because the cost of it being absent on the twentieth task is not
  paid in tokens.
- **Needed by none of the twenty, and not protected** → it is a no-op-test candidate, not an
  automatic move.

A move with no findable pointer is a deletion in disguise. The move is not done until you run one
task that needs the moved content and watch it get found and used. If the destination is a skill,
its pointer is its description — sharpening that is `skill-description-optimizer`'s job.

## Measure before and after
- **Before:** the token size of the whole always-loaded chain (`context-budget` does that
  inventory), AND a compliance baseline — for the 3–5 rules that matter most, the observable P
  from the no-op test, scored over a fixed set of real tasks. Freeze that task set.
- **After:** re-measure both, same tasks.

Tokens are the easy metric and the one that flatters you; rule compliance is the one that
matters. The uncomfortable case is real: **a trim can cut tokens and degrade behavior at the same
time.** That shows up as tokens down, compliance down, and it means the trim was wrong — not that
the tasks got harder. The prune is finished when the file is shorter AND compliance on the frozen
set is at or above baseline. If compliance dropped, restore the most recently cut lines and
re-check; whatever brings it back was, by definition, never a no-op.

Record what you cut and what each A/B showed, next to the file, so the next prune does not
re-litigate the same lines.

## Rules
- Removal carries the burden of proof. Undetermined → keep and rewrite, never keep-by-default-delete.
- Policy, safety, irreversible-action, domain-fact and fails-open lines are never no-op candidates.
  This method changes how a document LOADS and reads; it never changes what the project permits.
- One line per experiment, ≥5 reps per arm, an observable behavioral P fixed before running.
  Behavior, not tone.
- All edits land as one revision; no mid-session steering-file edits without a live reason.
- Not done at "shorter". Done at "shorter and compliance held".
- Method only: no hooks, no network calls, no external CLIs, no scripts that rewrite the file
  unattended. A human reviews the diff before it lands.

## In this repo (one instance)
The general method above applies to any always-on file; this repo's instance:
- The always-loaded file is `/home/user/skills-repo/CLAUDE.md` (standing rules + capability map).
  `pipeline/BRAIN.md` is read at loop start, not every turn — a different class, out of scope here.
- **Protected example:** "Never put backticks in a `git commit -m` string" is a domain fact that
  **fails open** — the commit lands quietly mangled, no test catches it, and it has already
  happened twice. A capable model would often get it right anyway. It is not a no-op candidate.
- **Layout:** the capability map grows every wave and sits mid-file, so each wave's append
  invalidates everything under it. Stable standing rules belong above it; the map, being the
  volatile part, belongs last or behind a pointer.
- **Progressive exposure done right, already present:** "For deterministic multi-step chaining see
  `pipeline/ROUTING.md`" — one pointer line instead of the routing table itself.
- **Frozen task set:** draw it from real wave tasks recorded in `pipeline/metrics.jsonl`, and score
  compliance with `eval-harness` rather than by eye.
