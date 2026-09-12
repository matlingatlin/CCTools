---
name: idempotent-action-design
description: "Use when an action with a real side effect could run more than once — a retried tool call, a resumed or restarted pipeline, a job that crashed halfway, an at-least-once queue redelivering, an agent repeating a step after a timeout — and nobody has made the second run safe. Triggers: 'is this safe to re-run', 'it posted the comment twice', 'duplicate rows / emails / PRs / tickets / charges', 'double-charged', 'the counter got bumped twice', 'the job died mid-write', 'resume from where it stopped', 'idempotency key', 'exactly-once', 'at-least-once', 'dedup the writes', 'replay the run', 'dry-run then apply', 'reconcile after a crash', partial writes, half-applied batches, unrecoverable send. Applies to any side effect: file writes, API calls, messages, DB mutations, payments. NOT classifying reversible vs irreversible or freezing an agent's scope BEFORE a run (agent-blast-radius-guard), NOT logging model calls for cost/replay accounting (llm-call-ledger), NOT whether a loop terminates or games its verifier (loop-design-check), NOT provoking tool failures to see how an agent reports them (agent-fault-injection)."
---

# Idempotent Action Design

Retries, resumes and crash-restarts are normal. The second run duplicating the first one's
effects is not: three identical comments, two emails, a counter bumped twice, a payment sent
again. This talent makes every real side effect safe to run again — keyed by its own content,
diffed against actual state, recorded before it happens, reconciled after an interruption.

**You cannot get exactly-once.** You get at-least-once delivery plus an idempotent apply,
which is *effectively once*. Say that; never claim exactly-once.

## When to use
- Anything with side effects will be retried, resumed, replayed, or restarted after a crash.
- A run died partway and you must decide what to re-run without duplicating what already ran.
- A step is wrapped in a retry/backoff and nobody checked whether the wrapped call is safe twice.
- Reviewing a pipeline, agent, worker, webhook handler, or migration that mutates external state.

**When NOT to use:** the run is read-only (nothing to make safe); you need to decide whether an
action is *permitted at all* or bound its damage — that is `agent-blast-radius-guard`, which
runs first and freezes scope; you want to *cause* failures to test honest reporting —
`agent-fault-injection` (complementary: it breaks things, this makes the re-run safe afterwards).

## Steps

1. **Enumerate the real side effects.** Walk the run end to end and list every step that
   changes state outside your process. For each record: system, operation verb, target
   identity, and one sentence — *what does the world look like if this runs twice?*
   Read-only steps drop out here. A side effect you cannot name, you cannot make safe.

2. **Classify each as naturally idempotent or not.** The verb decides, not the retry wrapper
   around it.

   | Operation | Safe to repeat? | Why |
   |---|---|---|
   | PUT / upsert on a stable key | **yes** | final state is defined by the key, not by call count |
   | Full-content write to a fixed path | **yes** | same bytes, same path |
   | DELETE by id | **yes** | second call is a no-op — treat "already gone"/404 as success |
   | Create-if-absent behind a unique constraint | **yes** | the store rejects the duplicate |
   | POST /create with a server-generated id | **no** | every call makes another one |
   | Append (log line, row insert, git commit, array push) | **no** | grows each run |
   | Increment / decrement / balance adjust | **no** | arithmetic accumulates |
   | Send (email, SMS, chat message, webhook, push) | **no** | delivery *is* the effect; it cannot be un-sent |
   | Charge / refund / transfer | **no** | money moves every time |

3. **Find the asymmetric pairs — this is where duplicates actually come from.** The failure is
   almost never a step everyone knows is dangerous. It is an idempotent-looking step sitting
   next to one that isn't, so the whole block gets declared "safe to re-run".

   > *Write `report.md` → post a PR comment linking it → bump a "reports generated" counter.*
   > Re-running gives one file (fine), **three comments**, and **three counter bumps**.

   **A sequence is only as re-runnable as its least idempotent member.** Do not prescribe
   "just re-run the step". Split the sequence at each boundary: the idempotent prefix may
   re-run freely, and every non-idempotent neighbour gets its own key (step 4) and its own
   ledger entry (step 6). Mark each boundary explicitly in the plan.

4. **Derive the idempotency key from the action's content.** Key = a stable digest of
   *(operation, target identity, semantic payload)*. It must be identical across attempts of
   the same action and different for genuinely different actions.
   - **Never** derive it from a fresh UUID, the attempt/retry number, a clock reading, or a
     PID — those make every retry look like a brand-new action, which is exactly the bug.
   - Exclude volatile fields that do not change meaning: timestamps, request ids, whitespace,
     re-serialization order.
   - Include everything that does change meaning, or two different actions collide and the
     second one is silently skipped — a dropped effect, the mirror-image bug.
   - Test both directions: re-planning the same input reproduces the same key; changing one
     meaningful field changes it.

5. **Plan, then apply — diffing against ACTUAL state.** Produce the full plan first (intended
   actions + their keys) with zero writes. Then, immediately before each apply, **read the
   current state of that target** and compare:
   - **already present and matching** → skip, record as satisfied;
   - **absent** → apply;
   - **present but different** → conflict: stop and escalate. Do not blind-overwrite;
     something else changed it, or your key is too coarse.

   Read at *apply* time, not at plan time: plan-time state is already stale, and the gap
   between planning and applying is exactly where the other writer lands.

6. **Write the ledger entry BEFORE the action, and check it before every action.** An
   append-only log, two records per action:
   - `intent` — key, operation, target, payload digest, timestamp — written **before** the call;
   - `outcome` — result, external id/reference, timestamp — written **after** it returns.

   Before executing anything, look the key up: an `outcome` means done (skip); nothing means
   not started (apply); **an `intent` with no `outcome` is the crash window — the action may or
   may not have happened**, and it goes to reconciliation (step 8), never straight to a retry.

   **The most common broken design is logging after success.** A crash between "the effect
   landed" and "the log was written" then leaves no trace at all, and the re-run duplicates it —
   silently, because nothing records that the first attempt existed. Ledger-after only works
   when the action is already naturally idempotent, in which case the ledger was barely needed.
   Writing before does not eliminate the unknown case; it makes the unknown case *visible*,
   which is the whole point. Never mutate or delete a past row — append a closing row instead.

7. **Handle external systems with no idempotency support — honestly.** In descending order of
   strength:
   1. **Native idempotency key** the API accepts (a header or field it dedups on server-side):
      a real guarantee. Send the step-4 key; reuse it on every retry of that action.
   2. **A natural unique key you control**: unique constraint, deterministic resource name or
      path, `create-if-absent`. The store enforces it — also a real guarantee.
   3. **Read-before-write on a natural key** (search for a marker, look the record up by an
      external reference you embedded). Embed the key visibly in the payload so the next run can
      recognise its own work — a trailer line, an HTML comment, a metadata field.

   Be explicit about the difference: **(3) is a race, not a guarantee.** Two runs can both read
   "absent" and both write. It narrows the window; it does not close it. If the effect is
   unrecoverable — money, mail, an outbound message — narrowing is not enough: serialize behind
   a lock/lease, or route it through a human gate (`agent-blast-radius-guard`). Write down which
   tier each side effect actually got; a tier-3 action documented as "idempotent" is a lie that
   will be believed later.

8. **Reconcile after any interruption, before resuming anything.**
   1. Read the ledger; list every key with an `intent` and no `outcome`.
   2. For each, query the target system by the key or embedded marker → **happened**,
      **did not happen**, or **unknown**.
   3. Append a closing row recording the finding (append-only: never edit the `intent`).
   4. Resume only the actions proven not to have happened; skip the ones proven done.
   5. **Unknown + non-idempotent effect → stop and ask a human.** Never guess, and never
      "retry to be safe" — that is the choice that sends the second email.
   Then hand the remaining work back to step 5.

9. **Verify by actually re-running.** Two tests, both required:
   - Run to completion, then run the identical input again. Assert the observable state is
     **unchanged**: one file, one comment, one row, the counter still at N, no second message.
   - Kill the run at its riskiest point (between the intent write and the outcome write of a
     non-idempotent action), then re-run. Assert the same.

   If you cannot state what "unchanged" means for a step, that step is not specified yet.

## Example
**Before:** a nightly agent writes a summary file, posts it as an issue comment, and increments
a "runs completed" field. It times out on the comment API weekly and the wrapper retries the whole
task, so the issue collects duplicate comments, the counter drifts high, and nobody can say which
runs actually finished.

**After:** three side effects enumerated and classified (write = idempotent, comment = not,
increment = not — an asymmetric triple). Key = digest of (`comment`, issue id, summary content).
The comment body carries a `<!-- idem:<key> -->` trailer; the run searches the issue's comments
for that marker before posting (tier 3 — documented as a narrowed race, not a guarantee). The
counter moves to a keyed set of completed-run ids, whose size is read as the count — turning an
increment into an idempotent set-insert. Intent rows are written before each call. The next
timeout resumes: the marker is found, the comment is skipped, the run id is already in the set,
and re-running the whole task changes nothing.

## Rules
- The key comes from the action's **content**. Never from a random value, an attempt number, or a clock.
- **Ledger before the action.** Append-only; never mutate or delete a past row.
- A sequence is only as re-runnable as its least idempotent step. Split at the boundary rather
  than declaring the whole block safe.
- Present-but-different is a **conflict**, not a write. Stop and escalate.
- Prefer converting a non-idempotent operation into an idempotent one (increment → keyed set
  insert; append → upsert by key; create → create-if-absent) over guarding it with logic.
- Never claim exactly-once. At-least-once + idempotent apply = effectively-once.
- Say which tier (native key / unique constraint / read-before-write) each effect got. Don't
  round a race up to a guarantee.
- Design method applied by hand: no auto-run hooks, no credentials, no external CLI installs.
- Complements, does not replace: `agent-blast-radius-guard` decides what may run at all,
  `agent-fault-injection` provokes the interruptions, `loop-design-check` bounds the loop,
  `verification-before-completion` demands the evidence for step 9.

## Common mistakes
| Mistake | What actually happens |
|---|---|
| Ledger written after the action succeeds | Crash in between leaves no record; the re-run duplicates it invisibly |
| Fresh UUID per attempt as the "idempotency key" | Every retry is a new action; the key dedups nothing |
| "The whole step is a file write, so it's safe to re-run" | The neighbouring post/increment/send in the same step is not |
| Diffing against the plan instead of live state | Skips work another writer undid; overwrites work another writer did |
| Retrying on `unknown` "to be safe" | Safe for reads; sends the second email for anything else |
| Key so coarse two distinct actions share it | The second real action is silently skipped — a dropped effect |
| Treating read-before-write as a guarantee | Two concurrent runs both read absent, both write |

## In this repo (one instance)
A wave writes `.claude/skills/<name>/SKILL.md` (full-content write — idempotent), appends a row
to `pipeline/metrics.jsonl` and `pipeline/ledgers/talents.jsonl` (**appends — not idempotent**),
and commits (**an append to history — a re-run creates a second commit**). That is the
asymmetric pair from step 3, in-house: re-running a wave leaves one skill file but duplicate
ledger rows and a duplicate commit. Key the jsonl rows by `(wave id, talent name)` and treat the
write as an upsert on that key, so a resumed wave reconciles instead of double-counting;
`pipeline/frontier.json` is state-by-key and already re-runnable.
