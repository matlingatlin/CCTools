---
name: loop-design-check
description: "Use when designing an autonomous agent loop, or worried an existing one will spin, burn tokens, game its verifier, or run a wrong answer to completion — gates whether to build, defines a decidable goal, reviews failure modes. NOT for choosing which plan items to drop when the budget is already short (use budget-cut-triage)."
metadata:
  origin: ECC
---

# Loop Design + Review

> **Premise.** An LLM is a feed-forward system: prompt in → tokens out, with no built-in "steer toward the goal" across turns. To make it *behave* like a goal-oriented system, you wrap a feedback loop around it. This skill helps you **write** that loop correctly and **review** it so it won't run away.

## When to use / not

**Use it when:**
- You want to hand a repeating task to an agent that runs over and over (write→test, test→fix, fix→verify…).
- You already have a loop and worry it spins, cheats, or runs a wrong answer to completion.

**Don't use it for:**
- A one-off task → just do it; don't wrap a loop around it.
- A plain timer / poll → use `/loop`; no design needed.
- *How to wire the loop architecture* (pipelines → DAGs, long-run recovery, the surrounding system) → that's the mechanism/ops layer, out of scope here: to **build** the surrounding system see `agentic-os`; to **operate** a long-running one see `enterprise-agent-ops`. **This skill only covers "is the goal right, and will it run away" — it does not re-explain mechanism.**

## Red-line premise: two levels of feedback

| Level | Who owns it | What it does |
|---|---|---|
| **Execution** (low) | machine / agent | Measures "how far from the literal goal" and grinds it to zero. The machine is strong here. |
| **Judgment** (high) | **human** | Decides "is this goal itself right, should it change, should it stop." The machine can't step outside its own loop to question the goal. |

> A thermostat can feed back "how far from 26°C," but when you have a fever and want 28°C it can't judge whether 26 is the *right* target — it just grinds toward 26. **"What to set today" is always the human's call.**
> Handing judgment / sign-off / the last switch to the machine = removing the high-level feedback = it sprints, fast and hard, toward a goal no one questioned → wrong output.

---

## Action 1 — Write a loop (5 steps)

### Step 0 · Subtract first: should you even build it? (4-condition gate, any miss = veto)

① the task repeats weekly or more　② verification can be automated　③ the token budget can take it　④ the agent has tools that actually *run and see the result*

Miss any one → **don't build a loop**; do it by hand or another way.
> What stops most people isn't "can I write a loop," it's "does my repo deserve one." A repo that deserves a loop has a reconciliation baseline (golden sample / upstream total) + tests + a lint guard. **A repo that doesn't deserve a loop will only have its errors amplified by one.**

### Step 1 · Define a *machine-decidable* goal (the hard part — the loop lives or dies here)

The whole loop rides on the comparator's "is it done yet?" **The comparator can only work if your exit condition can be judged yes/no by a machine.**

- Bad: Vague ("make it good," "write it sharper") → the comparator can't judge → either it never passes (stuck retrying) or it guesses (passes/blocks at random).
- Good: Decidable ("all 96 unit tests green AND a change-list is produced," "module-02 fields filled, pytest passes, business logic untouched") → one check settles it; the loop converges cleanly.

**Five-point goal framework:**
1. **Done-criterion is machine-verifiable.**
2. **Boundary conditions defined alongside the done-criterion** ("what it must NOT do") — anti-Goodhart; missing boundaries = a license to cheat.
3. **Has a failure fallback** — retry cap N + escalate to a human when exceeded.
4. **Goal is layered.**
5. **Prefer reconciliation over assertion for the done-criterion** — anchor to external fact (golden sample / upstream total / financial tie-out / platform back-office numbers) before your own assertions. "All tests pass" can be gamed (loosen asserts, fake mocks, swallow exceptions); "diff vs the reference < 0.01" can't.

> **Self-check:** read the goal to someone who doesn't know the domain — can they run one command and tell whether it's done? If not, it isn't decidable enough. Go back.

### Step 2 · Pick the loop type

| Your task | Loop type (cybernetic) | How it stops |
|---|---|---|
| Has a clear "done" test (write to done / a batch of images processed) | **servo** (`/goal`-style closed-loop) | stops on reaching the goal |
| No endpoint, must keep maintaining a state (inventory alert / scheduled health check) | **regulator** (`/loop`-style thermostat) | never stops; acts only on change (dead-band suppresses noise) |
| Periodic sampling, stop on a condition (watch a PR until CI is green) | **regulator with an exit** | stops when the exit condition holds |
| Must "ensure something happens on time" | wrap the above in `/schedule` | cron fires it |

> Rule of thumb: clear "done" test → servo; must keep maintaining, no endpoint → regulator; must "happen on time" → wrap a regulator in schedule.

### Step 3 · Pick a skeleton

**Maintenance type (tend something that exists) → document-driven dispatch.**
The loop isn't "run a fixed check on a timer," it's **"read a doc on a timer, and dispatch only when the doc changed."** The doc is the task queue + state machine + human interface.
Three disciplines: ① the problem column is human-write-only, the result column is loop-write-only, **state advances one-way and never rolls back**; ② **the exit code is final** (if the script says exit 1, the script wins); ③ state advances only as far as "awaiting verification" — **the "done" cell is flipped by a human only.** The loop is the worker, not the acceptance officer.

**Greenfield type (build from scratch) → plan / build / judge, three roles.**

| Role | Does | Key |
|---|---|---|
| **Plan** | break the goal into a spec + **decidable acceptance conditions** | acceptance must be script-judgeable |
| **Build** | write to the spec | **must not change the acceptance conditions** |
| **Judge** | run acceptance **independently**; pass → stop, fail → return with the failure reason to Build | **independent + deterministic** |

Three iron rules (all bet on the judge): ① **the judge must be independent** — not the same agent as Build (grading your own homework always inflates); ② **deterministic rules** — pytest / reconciliation diff / type check / diff, never "looks right"; ③ **Build may not edit the acceptance conditions to pass**. Three failed retries → escalate to a human.

### Step 4 · Add damping (against oscillation / runaway)

Retry cap, hard stop, human flips the last switch = damping. **Negative feedback with no damping oscillates** (the Ralph-Wiggum loop: spinning in place, burning tokens).

**Quota damping — a loop that shares a resetting budget must know its own ceiling.** When the
loop runs under a quota that refills on a clock (an API rate-limit window, a spend cap), check
that quota at the ITERATION boundary, alongside the time budget. Four rules that turn a hard
crash into a clean pause (or a sustainable throttle):
1. **Approaching the ceiling is already the stop signal.** Don't start an iteration you can't
   finish — being cut off mid-iteration produces exactly the half-written state the graceful
   stop exists to prevent. "Still allowed" is not "enough left."
2. **A quota error is a stop, never a retry.** Retrying into a rate limit is the runaway this
   step exists to damp.
3. **Pause with a known wake-up.** Commit, record why it stopped and what backlog remains, and
   schedule ONE resume just after the reset. If an already-scheduled run lands soon after the
   reset, schedule nothing and let it take the work — two queued resumes is the same runaway
   in a different costume.
4. **Read the WINDOW LENGTH before choosing pause vs throttle — they are different quotas.**
   Most systems enforce several windows at once (e.g. a short rolling one and a long one); the
   binding quota is whichever is closest to its ceiling, and it CHANGES as windows reset. So
   check which window is warning, not just that something is:
   - **Short window** (minutes/hours) → **pause** and resume after reset, per rule 3. Waiting
     costs little.
   - **Long window** (days/a week) → **do NOT pause**: waiting days is a stop, not a pause, and
     it silently kills the loop. **Throttle instead** — smaller batches, less parallelism, a
     cheaper model for sub-work, or a longer interval between runs — so the loop keeps
     delivering within a budget that must now last until the distant reset.
   Getting this backwards is the trap: pausing on a weekly cap looks like graceful degradation
   and is actually an outage; throttling on a 5-minute cap wastes a reset that was seconds away.
   And a long-window warning is worth surfacing to the human — spending the rest of a weekly
   budget overnight is their call, not the loop's.

### Step 5 · Land in three stages (don't go fully automatic on day one)

① **Run it once by hand** (forces you to state exactly "how the judge decides") → ② harden into a skill / Claude Code sub-agents (a main Claude loops, dispatching plan/build/judge) → ③ hang it on cron for full automation.

---

## Action 2 — Review a loop (checklist = five failure modes)

> Run the loop past each row. **Hitting any one = this loop will misfire; send it back.** These five are negative experience (gotchas) — worth more than positive rules.

| # | Failure mode (how it breaks) | Review question (a hit = red) | Antibody |
|---|---|---|---|
| 1 | Goal is a correct platitude → **spins, burns money** | Can the exit condition be machine-judged yes/no? Or is it "manage it well / make it good"? | Replace with a decidable result condition (Action 1·Step 1) |
| 2 | "Verification" written as "check if it looks ok" → **agent confidently says fine and stops** | Is the judge the defendant itself? Does verification rest on "looks right" or deterministic rules? | Reconcile + exit code rules + independent judge |
| 3 | (worst) Only gates on "all tests pass" → **agent deletes the tests** | Is there a boundary ("what it must NOT do")? Or only a done-criterion? | Done-criterion **+ boundary** together (the Goodhart antibody) |
| 4 | Counts on the agent asking mid-run → **it won't; it runs the wrong answer to the end** | Is there any "clarify only at runtime" point? | **Front-load every clarification**; settle it once before launch |
| 5 | Bloated CLAUDE.md + stale memory → **the faster it loops, the more it errs** | Are the docs/memory it depends on fresh? Who maintains them? | Layered memory + periodic lint |

**Plus three red lines (violate any = not allowed to go automatic):**
- **Keep judgment with the human.** Acceptance / the "done" cell is flipped by a human; the loop is not the acceptance officer.
- **Responsibility doesn't transfer.** Anything whose failure you can't afford (merge the wrong PR / publish the wrong thing / misallocate money) → **don't hand over the authority automatically.**
- **Counter-intuitive warning.** The more "self-improving / rewrites-its-own-rules" a loop is, the **stricter the human review it needs** (to see what it rewrote the rules into) — not looser. The machine is too fast to intercept after the fact, so the human's judgment must sit **before the action** (a hard gate), not as a post-hoc patch.

---

## Worked example — reviewing a "nightly green-keeper" loop

You want a loop that runs every night and fixes whatever tests are failing.

- **Naive goal:** "make all tests pass." → Step-1 self-check fails: this is the bait for failure mode #3.
- **Decidable goal (fixed):** "all tests green **AND** no test file deleted or weakened **AND** coverage not lowered **AND** a change-list produced." Boundary now defined alongside the done-criterion.
- **Type:** servo with a retry cap of 3 (Step 2 + Step 4).
- **Skeleton:** plan/build/judge — the **judge is CI run independently**, never the fixing agent (Step 3).

Now run the **review checklist**, and it catches what the naive version would have missed:
- **#3 hit** → the naive "all tests pass" lets the agent delete a failing test to "win." Fixed by the boundary "no test file deleted/weakened."
- **#2 hit** → if the fixing agent also judged its own fix, it would pass itself. Fixed by "judge = independent CI, deterministic."
- **#4 hit** → if a fix is ambiguous, the agent won't stop to ask at 2 a.m.; it'll commit a guess. Fixed by front-loading: ambiguous fixes are left for the human, not guessed.
- **Red line** → the loop opens a PR but **does not auto-merge**; the human flips the last switch (responsibility doesn't transfer).

The naive loop and the reviewed loop differ by four lines of constraint — and that's the difference between "wakes you to a deleted test suite" and "wakes you to a clean PR."

---

## One-line close

> The hard part of writing a loop isn't "can I write a loop," it's **defining a goal a machine can reconcile** — decidable, bounded, reconciliation-based. The controller must be deterministic and external; keep judgment and the standard with the human; the system tends toward entropy, so maintain it.
> **A loop only rewards someone who has already thought it through. Count on it to think for you, and it will happily think wrong, with you, at scale.**

---

> Lineage: Wiener's two-level feedback (*The Human Use of Human Beings*, 1950) for the judgment/execution split and red lines; the plan/build/judge pattern from Anatoli's *Loops explained* and Addy's *Loop Engineering*.
> Mechanism/ops layer (how to wire and run the surrounding system): `agentic-os` to build it, `enterprise-agent-ops` to operate a long-running one. This skill does not re-implement mechanism; it covers goal definition and runaway prevention only.
