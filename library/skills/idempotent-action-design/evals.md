# Evals — idempotent-action-design

**Talent:** `idempotent-action-design` · **Type:** technique · **Last eval:** 2026-08-28 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. The talent passes a scenario only if the with-talent result is materially
better and meets the pass criterion. Authored by an INDEPENDENT tester (not the skill author);
scenarios are written against the file's ACTUAL steps, tables and rules, not its self-description.

**Blend:** 11 scenarios — 5 `application (normal)`, 5 clever (4 `pressure`, 1 `edge`),
1 `negative-trigger`. ~50% normal, per CURATION-LESSONS ACTIVE DIRECTIVES.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 5 normal / 5 clever / 1 negative-trigger.
- [x] **Specific to this talent** — every scenario cites a concrete step, table row or rule.
- [x] **Observable pass/fail criterion** — each is a checkable line, no "looks good".
- [x] **Clever scenarios designed so baseline plausibly FAILS** — S6–S10.
- [x] **Matches talent type** — technique → APPLICATION scenarios for the normals.
- [x] **Negative trigger covered** — exactly one (S11).
- [x] **Dead cross-refs / invented commands / `name:` / portability** — checked, see Structural review.

## Scenarios

## S1 — Twelve-item pipeline dies after 7 · application (normal)
- **Input:** A nightly ingest processes 12 vendor files. Per item it (a) writes
  `out/<vendor>.parquet` with a full-content write, (b) posts a comment on the vendor's Jira
  issue linking the output, (c) runs `UPDATE vendor_stats SET files_ingested = files_ingested + 1`.
  It crashed after item 7 (items 1–7 fully done, item 8 unknown, 9–12 untouched).
  "How do we resume without double-posting?"
- **Pass criterion (observable):** The answer (i) lists all three side effects with system +
  verb + target identity (step 1); (ii) classifies the parquet write as idempotent and the Jira
  comment + counter increment as NOT (step 2 table rows "full-content write", "send", "increment");
  (iii) derives a key per action from `(operation, vendor id, content digest)` — not from the item
  index alone; (iv) prescribes plan-then-apply with a read of live state immediately before each
  apply (step 5); (v) puts item 8 in the intent-without-outcome bucket and sends it to
  reconciliation (step 8), rather than lumping it with 9–12. Fails if it answers "just re-run
  items 8–12" without distinguishing 8 from 9–12.
- **Baseline (without talent):** Likely correct on the easy half — "resume from item 8" — but
  usually treats item 8 as simply not-done and re-runs it whole, silently re-posting its Jira
  comment and re-bumping the counter if it had in fact completed.
- **With talent:** Step 1 enumerates 36 effects (3 × 12). Step 2 splits them. Step 3 marks the
  boundary after the parquet write. Step 6's ledger lookup returns `intent`-no-`outcome` for
  item 8 → step 8 queries Jira for the embedded marker before deciding; items 9–12 have no rows
  and apply cleanly. Counter is converted to a keyed set of `(vendor, run)` ids per the Rules
  ("increment → keyed set insert"), so its value is derived, not accumulated. **PASS. Beats baseline.**

## S2 — At-least-once webhook redelivery · application (normal)
- **Input:** A payments webhook endpoint receives `payment_succeeded` events. The provider
  documents at-least-once delivery; last month 1,140 events arrived, 1,163 HTTP deliveries were
  made (23 redeliveries after our 504s). Each handler run inserts a row into `payments_ledger`
  and emails a receipt. Finance reports 23 duplicate rows and 23 duplicate receipts.
- **Pass criterion (observable):** The answer keys off the provider's `event.id` (or a digest of
  the event body) rather than a locally generated value, puts a UNIQUE constraint on that column
  so the store rejects the duplicate insert (step 7 tier 2, named as tier 2), classifies the
  receipt email as a tier-1/2-impossible "send" and gates it on the insert winning, and describes
  the result as **effectively-once**, not exactly-once. Fails if the phrase "exactly-once" is used
  as an achieved property.
- **Baseline (without talent):** Usually gets the unique-constraint half right, but commonly
  describes the outcome as "exactly-once processing" and often leaves the email outside the
  transaction boundary, so a redelivery that loses the insert race still sends a second receipt.
- **With talent:** Step 2 classifies row-insert (not idempotent alone) and send (not idempotent).
  Step 7 ranks: tier 2 for the insert via the unique key we control; the email is sequenced after
  the insert commits and carries the same key, so a redelivery hits the constraint and never
  reaches the send. Intro rule "never claim exactly-once" is applied verbatim. **PASS.**

## S3 — Retry wrapper around an onboarding email · application (normal)
- **Input:** `@retry(attempts=5, backoff=exponential)` decorates
  `send_welcome_email(user_id)`. Nobody has looked inside since it was added 8 months ago.
  Support has 6 tickets this quarter about receiving the welcome email 2–4 times.
- **Pass criterion (observable):** The answer states that the retry wrapper does not make the
  wrapped call safe (step 2: "the verb decides, not the retry wrapper around it"), classifies
  `send` as not idempotent because delivery IS the effect and cannot be un-sent, and — because the
  provider offers no dedup — declines to call read-before-write a fix, prescribing instead a
  ledger-gated send with the key stored before the call. Fails if the remedy is only "lower the
  retry count" or "add a try/except".
- **Baseline (without talent):** Plausibly reaches "emails aren't idempotent, gate the retry",
  which is right — this scenario confirms everyday behavior rather than discriminating.
- **With talent:** Steps 1–2 name the effect and its class; step 6 writes the `intent` before the
  SMTP call so a crash mid-send is visible; step 8.5 routes an `unknown` to a human instead of a
  sixth attempt. **PASS.**

## S4 — Cleanup worker alerting on 404 · application (normal)
- **Input:** A nightly worker deletes expired sessions: `DELETE /sessions/{id}` for each of ~800
  ids read from a snapshot. On the second pass after a partial failure, 612 of the calls return
  `404 Not Found`; the worker raises, pages on-call, and the remaining 188 deletions never run.
- **Pass criterion (observable):** The answer states that DELETE by id IS naturally idempotent and
  that `404` / "already gone" must be **treated as success**, not as an error (step 2 table row),
  and therefore the second pass needs no key or ledger for the delete itself — the fix is the
  worker's error handling, not a new idempotency layer. Fails if it proposes an idempotency key or
  ledger for a plain DELETE-by-id.
- **Baseline (without talent):** Often correct in principle but frequently over-engineers — adds a
  dedup ledger or "check existence before delete" for an operation that is already idempotent,
  and may still not say plainly that 404 is a success.
- **With talent:** The table row settles it in one line, and the "prefer converting a
  non-idempotent operation into an idempotent one" rule keeps the fix proportional: no machinery
  is added where the verb already carries the property. **PASS.**

## S5 — Proving the fix works · application (normal)
- **Input:** The team has implemented keys + a ledger for the S1 pipeline and asks: "how do we
  actually verify this before shipping?"
- **Pass criterion (observable):** The answer specifies BOTH of step 9's tests, not one:
  (1) run to completion, run the identical input again, assert observable state unchanged —
  named per effect (one parquet file, one Jira comment, counter still at N); and (2) kill the run
  specifically between the `intent` write and the `outcome` write of a non-idempotent action, then
  re-run and assert the same. Fails if only the happy re-run test is given.
- **Baseline (without talent):** Typically proposes the double-run test only. The crash-window
  injection — the one that exercises the reconciliation path — is the half that gets dropped.
- **With talent:** Step 9 requires both and adds the falsifiability check: "if you cannot state
  what unchanged means for a step, that step is not specified yet". **PASS. Beats baseline.**

## S6 — The asymmetric block behind a narrow question · pressure (clever, baseline fails)
- **Input:** "Our nightly `publish_report()` posts to Slack twice on about 3 nights a month —
  the job times out on the Slack API and our wrapper retries the task. **How do we stop the
  duplicate Slack messages?**" The function body, given: writes `reports/<date>.md` (full-content
  write), posts to `#eng`, then `UPDATE stats SET reports_generated = reports_generated + 1`.
  The team runbook says "publish_report is basically a file write — safe to re-run."
- **Pass criterion (observable):** The answer must flag the **counter** as also over-counted by
  the same 3 duplicate runs, even though the user asked only about Slack — and must explicitly
  reject the runbook line by stating that a sequence is only as re-runnable as its LEAST
  idempotent member, splitting the block at the boundary after the file write and giving the
  Slack post and the counter each their own key and ledger entry. Fails if it answers only the
  Slack question, or if it accepts "it's basically a file write".
- **Baseline (without talent):** Answers the question as asked. Proposes a Slack dedup marker or
  a shorter timeout, leaves the increment untouched — it was never mentioned and looks like
  bookkeeping — and does not contradict the runbook. The counter keeps drifting silently.
- **With talent:** Step 1 forces end-to-end enumeration BEFORE answering, so the increment enters
  the list regardless of what was asked. Step 3 is written for exactly this shape (its worked
  example is file → comment → counter) and names it an asymmetric triple; the Rules require
  splitting rather than declaring the block safe, and convert the increment to a keyed set of
  completed-run ids whose size is the count. **PASS. Beats baseline.**

## S7 — Ledger written after the send · pressure (clever, baseline fails)
- **Input:** A dunning job emails 500 overdue customers. Code:
  `send_invoice_email(c); db.insert("sent_log", c.id)`. The process was OOM-killed; `sent_log`
  holds 412 rows, and the customer list is stable and ordered. The on-call engineer asks:
  "safe to resume from row 413?"
- **Pass criterion (observable):** The answer must (i) refuse a plain "resume at 413"; (ii) name
  the gap between the email being accepted by the provider and the log row committing as a
  **crash window**, and identify customer #413 specifically as the one action whose state is
  UNKNOWN; (iii) route #413 to reconciliation or a human rather than retrying it, invoking the
  rule that "retry to be safe" is what sends the second email; (iv) prescribe the structural fix —
  the `intent` row written BEFORE the send, `outcome` after. Fails if it recommends re-sending
  #413, or if it only reorders the log write without naming the unknown case.
- **Baseline (without talent):** "The log is the source of truth — resume from 413." That is the
  single most natural answer and it sends one duplicate invoice to a customer who already got one.
  A stronger baseline may notice the ordering bug and move the log before the send, but still
  treats the current #413 as un-sent.
- **With talent:** Step 6 states the failure mode by name ("the most common broken design is
  logging after success") and defines the three lookup outcomes; #413 has neither an `intent` nor
  an `outcome`, so nothing distinguishes "not sent" from "sent, unlogged" — step 8.5 makes that a
  stop-and-ask, and step 6's reordering makes the case *visible* next time rather than eliminating
  it. The answer also states honestly that writing-before does not remove the unknown case.
  **PASS. Beats baseline.**

## S8 — Search-then-create called idempotent · pressure (clever, baseline fails)
- **Input:** An alert-triage agent files tickets in an internal tool. `POST /tickets` returns a
  server-generated id; the API has no `Idempotency-Key` header and no unique constraint on title.
  `GET /tickets?search=<text>` exists. Two worker replicas consume the same alert stream, roughly
  40 alerts/hour. A design doc proposes: "search for the alert fingerprint first; if not found,
  create. This makes ticket creation idempotent."
- **Pass criterion (observable):** The answer must classify this as **tier 3** read-before-write
  and state in words that it is a **race, not a guarantee** — that both replicas can read "absent"
  and both create — and must therefore refuse to sign off the doc's word "idempotent"; it must
  prescribe serialization (lock/lease) or a human gate for the residual window, and require the
  fingerprint be embedded visibly in the ticket body so the next run recognises its own work.
  Fails if the answer endorses search-then-create as idempotent or safe without naming the race.
- **Baseline (without talent):** Endorses the doc. Search-before-create is the standard-issue
  answer, and with the two-replica detail present but unremarked, the concurrent double-read is
  usually not surfaced. The design ships labelled "idempotent" and duplicates appear under load.
- **With talent:** Step 7's tier list forces the label, and its closing line is decisive: "a
  tier-3 action documented as 'idempotent' is a lie that will be believed later." The Rules
  require writing down which tier each effect actually got and forbid rounding a race up to a
  guarantee. **PASS. Beats baseline.**

## S9 — A key that dedups nothing · pressure (clever, baseline fails)
- **Input:** A PR adds retries to a payouts worker:
  `idem_key = f"{job}-{attempt}-{uuid4().hex[:8]}"`, sent as the payment API's
  `Idempotency-Key` header. The PR description reads: "every call is uniquely keyed, so we can
  never double-charge." CI is green; the API accepts the header.
- **Pass criterion (observable):** The answer must state that this key **changes on every attempt
  of the same action** and therefore dedups nothing — the header is present but inert — and must
  replace it with a stable digest of `(operation, target identity, semantic payload)`, explicitly
  excluding attempt number, UUID and clock. It must state the two-direction test: re-planning the
  same payout reproduces the same key, and changing one meaningful field (amount, payee) changes
  it. Fails if the PR is approved, or if the fix is "reuse the UUID across retries" without
  grounding the key in content.
- **Baseline (without talent):** Sees a correctly-named header on a payments API and a
  confident description; "uniquely keyed" *sounds* like the right property. Approval is a very
  plausible outcome — the bug is that uniqueness is the exact opposite of what the header needs.
- **With talent:** Step 4's prohibition list names all three forbidden sources — fresh UUID,
  attempt number, clock — and the Common-mistakes table has the row verbatim ("fresh UUID per
  attempt … the key dedups nothing"). Step 4's two-direction test is the acceptance criterion.
  **PASS. Beats baseline.**

## S10 — A too-coarse key drops a real refund · edge (clever)
- **Input:** Refunds are deduped with `key = sha256(customer_id + "refund")`. Customer 9812 is
  legitimately refunded twice on the same day for two different orders — $40 (order A) and $75
  (order B). The second refund is skipped as "already satisfied" and the customer is $75 short.
  A junior engineer proposes appending `time.time()` to the key so the two refunds differ.
- **Pass criterion (observable):** The answer must (i) name this as the **mirror-image bug** — a
  dropped effect, not a duplicate — caused by a key missing a meaning-changing field; (ii) fix it
  by adding the **order id / amount** (content that changes meaning) to the key; and (iii)
  explicitly REJECT the timestamp proposal, on the ground that a clock reading makes every retry
  of the same refund look like a new action, reintroducing double-payment. Fails if the timestamp
  fix is accepted, or if only the dedup direction is discussed.
- **Baseline (without talent):** Diagnoses the collision correctly — that part is visible — but
  the offered remedy is usually "make the key unique per request", i.e. a timestamp, nonce or
  request id. That closes the reported bug and opens the far worse one, on a money path.
- **With talent:** Step 4 holds both halves at once: "include everything that does change meaning,
  or two different actions collide and the second is silently skipped", alongside the prohibition
  on clock readings and the instruction to exclude timestamps as volatile. Both Common-mistakes
  rows (too-coarse key; fresh value per attempt) apply, so the timestamp fix is rejected by the
  same rule set that diagnoses the collision. **PASS. Beats baseline.**

## S11 — "Is the agent allowed to delete this at all?" · negative-trigger
- **Input:** Before a new cleanup agent is enabled: "This agent will issue `DELETE /users/{id}`
  against production. Should it be permitted to delete user rows at all, what is the worst case
  if it goes wrong, and how do we cap the blast radius? It hasn't run yet."
- **Pass criterion (observable):** The talent does NOT fire. The answer must decline to produce an
  idempotency key, ledger, or plan-then-apply design, and must route to `agent-blast-radius-guard`
  as the talent that "runs first and freezes scope". Fails if it opens the step 2 verb table and
  starts designing keys because DELETE appears in the prompt.
- **Baseline (without talent):** Not applicable as a discriminator — this scenario tests
  over-triggering, not capability.
- **With talent:** The "When NOT to use" block names this case explicitly (permission and damage
  bounding → `agent-blast-radius-guard`, which runs first), and the description's NOT-clause lists
  the same routing. The DELETE verb in the prompt is deliberate bait — it is in the step 2 table —
  but the request contains no re-run, retry or resume: nothing has run yet, so there is no second
  run to make safe. **PASS.**

## Structural review (independent checks demanded by CURATION-LESSONS)
- **Frontmatter:** `name: idempotent-action-design` present, `description:` present. OK.
- **Dead cross-references:** all five named siblings exist under `.claude/skills/` —
  `agent-blast-radius-guard`, `llm-call-ledger`, `loop-design-check`, `agent-fault-injection`,
  `verification-before-completion`. No rot.
- **Invented slash-commands / built-ins:** none. (The only `/`-token is `POST /create` in the
  verb table — an HTTP path, not a command.)
- **Format drift:** tests live in this `evals.md`; no `evals/` directory. OK.
- **Portability:** the method is hand-applied — "no auto-run hooks, no credentials, no external
  CLI installs". The only repo-specific content is fenced in the "In this repo (one instance)"
  section, and the three paths it cites (`pipeline/metrics.jsonl`,
  `pipeline/ledgers/talents.jsonl`, `pipeline/frontier.json`) all exist. OK.
- **Verb table correctness (checked row by row):** PUT/upsert on a stable key — correct.
  Full-content write to a fixed path — correct, and properly conditioned on "same bytes".
  **DELETE by id — correct**: idempotent in final state, and the file carries the load-bearing
  rider that "already gone"/404 must be treated as success, without which callers get S4's bug.
  **Create-if-absent behind a unique constraint — correct**: the store rejects the duplicate, so
  final state is one row regardless of call count. POST /create with a server-generated id,
  append, increment, send, charge — all correctly marked not idempotent.
  *Minor, non-blocking:* the create-if-absent row does not carry the caller-side rider its DELETE
  neighbour does (treat the duplicate-key violation as success, not as a failed attempt). The
  idempotency claim itself is unaffected — no duplicate effect either way — and step 7 tier 2
  covers it in prose. Recorded as a polish note, not a defect.
- **"exactly-once" consistency (checked all 9 occurrences of the phrase family):** consistent
  throughout. The intro states "You cannot get exactly-once … never claim exactly-once"; the
  Rules restate it; nowhere in Steps, Example, Common mistakes or the repo section is
  exactly-once claimed as achieved. The one appearance in the `description:` is a user-uttered
  TRIGGER phrase, not an assertion — correct, since that is what people type. Step 7's "a real
  guarantee" for tiers 1–2 is not a contradiction: the guarantee claimed is on the *apply* side
  (server-side dedup / store-enforced uniqueness), which is precisely the "idempotent apply" half
  of "at-least-once + idempotent apply = effectively-once". No contradiction found.

## Failure triage (if any scenario failed)
No scenario failed; no triage required.

## Result summary
- Scenarios passed: 11/11 · failure_cause: none · verdict: passed
