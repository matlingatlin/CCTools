# Eval: integration-contract-completeness

Functional regression test for the `integration-contract-completeness` talent. This is a
**technique** talent: given a patch that touches ONE side of a symmetric or multi-variant
contract, enumerate the contract's mirror sides and variant axes, grep the codebase for each
peer, and classify every axis as **covered** / **missing** / **deliberately-narrow-with-a-
reason** — then lead the report with the missing rows. Its sharpest, most-differentiated
behaviors are: (a) treating the *absence* of a peer (a decode next to a new encode, the other
providers' branches) as a finding rather than reviewing only the lines in the diff; (b) using
the codebase's OWN sibling branches as the authority on which variants a complete change must
cover; (c) refusing "not needed" as a justification and demanding a defensible reason for
every narrow; (d) counting a roundtrip test and a docs/changelog touch as axes, not
afterthoughts; and (e) NOT inventing axes a contract does not have — narrow, and "nothing to
sweep," are both allowed answers.

Method: for each scenario, reason through the likely output WITHOUT the talent (baseline
Claude reviewing the same diff) vs WITH the talent's method applied, and judge whether the
talent produces a materially better, criterion-meeting result. Adversarial, not a rubber
stamp. Traps are included in BOTH directions — the completeness failure the talent exists to
catch (one-sided patch shipped as "done"), a pressure case that tempts rubber-stamping a bad
reason, plus the talent's own negative triggers (a self-contained change with no mirror side;
a request that is really test-coverage or verification) that should make it decline to
manufacture axes.

Date: 2026-08-27 · Talent version: SKILL.md as of this commit.

---

## Scenario 1 — New encode path, no decode (application, core target)
**Input:** "I added `serialize_session_v2(session) -> bytes` to write our new on-disk session
format. Diff is +40 lines in `wire.py`, all in the new function. Is this change complete, or
did I miss anything?"
**Pass criterion:** Names the contract as a symmetric serialize/deserialize pair, identifies
that a `serialize` with no matching `deserialize` cannot be read back, and reports the decode
side as **missing** (a defect, not a nit). Must also flag the absent **roundtrip test**
(bytes → deserialize → equals input) and the **docs/format-version** obligation. Reviewing
only the 40 added lines for style = fail.

- **Baseline:** Reads the 40-line diff and reviews what is in front of it — naming, error
  handling, maybe a suggestion to add a docstring. Because the deserializer is *not in the
  diff*, baseline is prone to never asking "where is the reader?" It may say "looks good"
  about a function whose output nothing in the codebase can consume. The completeness gap is
  invisible precisely because the missing side is absent from the patch.
- **With talent:** Step 1 names the operation (`serialize_session_v2`) and its contract
  (session ↔ bytes, a paired encode/decode). Step 2 enumerates the mirror side (decode), the
  roundtrip obligation, and docs/version axes. Step 3 greps for a `deserialize_session`/
  `load_session_v2` peer and finds none present. Step 4 classifies: decode = **missing**,
  roundtrip test = **missing**, format-version doc = **missing**. Step 6 reports a table led
  by the missing rows: a v2 writer with no v2 reader is a half-contract.
- **Verdict:** PASS. The talent surfaces a defect that lives entirely *outside* the diff —
  exactly the blind spot a line-by-line review has. It converts "the added code looks fine"
  into "the added code is unreadable back until decode + roundtrip land." Decisive,
  differentiated win.

---

## Scenario 2 — New enum variant wired through one switch of several (fan-out trap)
**Input:** "Added a new `PaymentMethod.CRYPTO` value and handled it in `charge()`. The build
passes. Ship it?" Codebase context: `PaymentMethod` is also switched on in `refund()`,
`format_receipt()`, `estimate_fees()`, and a `PAYMENT_METHOD_LABELS` dict, each of which
enumerates the existing methods explicitly.
**Pass criterion:** Uses the existing sibling switch/dispatch sites as the authority on which
branches a complete `CRYPTO` addition must touch, greps them out, and reports `refund()`,
`format_receipt()`, `estimate_fees()`, and the labels dict as **missing** coverage for the
new variant. "Build passes, ship it" = fail (a non-exhaustive switch or a `.get()` with a
default compiles fine while silently mis-handling the new case).
- **Baseline:** Sees `charge()` handle `CRYPTO` correctly and that compilation succeeds.
  Without a reflex to enumerate every peer site, baseline tends to trust "it builds" — but in
  most languages a missing enum branch is a runtime `else`/default, not a compile error, so
  refunds silently fail or receipts render a blank method for crypto charges. Baseline reviews
  the one site it was shown.
- **With talent:** Rule "Prefer the codebase's own precedent: the sibling branches already
  present define which variants a complete change must cover." Step 3 greps for every site
  that switches on `PaymentMethod` and lists the four peers plus the labels dict. Step 4 marks
  each as **missing**. The report leads with them and flags that a green build does not prove
  exhaustiveness. Each new branch also implies a test axis.
- **Verdict:** PASS. This is the multi-variant fan-out the talent is built for: one branch
  updated, N-1 peers silently stale, and a passing build hiding it. Baseline is talked into
  "it compiles" far more easily. Strong, differentiated win.

---

## Scenario 3 — One-sided patch whose reverse path is generated (deliberately-narrow, boundary)
**Input:** "I added a `to_proto()` hand-written mapper for our `Order` type. There's no
matching `from_proto()` in my diff — but `from_proto` is code-generated from the `.proto` by
our build step. Is the patch incomplete?"
**Pass criterion:** Accepts the narrow as **deliberately-narrow with a defensible reason**
("the reverse path is generated") and does NOT demand a hand-written `from_proto`. Records the
reason and, at most, notes the residual obligation (a roundtrip test still validates that the
hand-written encode and the generated decode agree). Insisting the patch is incomplete and
must add `from_proto` = fail (over-widening).
- **Baseline:** Might reflexively say "you should add the inverse for symmetry," creating busy
  work that duplicates generated code — or might not engage with the symmetry question at all.
- **With talent:** Rule "Narrow can be the correct answer. The output is a justified decision,
  not a mandate to widen scope" and Step 5's list of acceptable reasons ("the reverse path is
  generated") apply directly. The talent classifies decode as **deliberately-narrow**, records
  the codegen reason, and — using the roundtrip rule — recommends a single roundtrip test
  (`order → to_proto → generated from_proto → equals order`) as the *real* completeness check,
  rather than a redundant hand-written mapper.
- **Verdict:** PASS (boundary). The talent does not beat baseline by widening — it beats a
  naive "always add the mirror" heuristic by making the correct *narrow* call with a recorded
  reason, and redirects effort to the roundtrip test that actually protects the contract.
  Correct restraint plus a sharper obligation.

---

## Scenario 4 — "The response side isn't needed, don't worry about it" (reason-demand pressure)
**Input:** "I added the outbound `POST /webhooks/subscribe` request builder. We don't need to
handle the provider's response — just fire and forget, it's not needed. Sign off on the diff?"
**Pass criterion:** Refuses "it's not needed" as a justification for skipping the response
side. Demands a *defensible* reason (e.g. the endpoint is truly 202-and-nothing-meaningful,
failures are surfaced elsewhere, a follow-up is tracked) and points out the specific
obligations the narrow waives — error/non-2xx handling, reton, at least a status check.
Rubber-stamping "not needed" = fail.
- **Baseline:** Under the user's confident "it's not needed" framing, baseline is prone to
  agree and sign off. "Fire and forget" sounds like a deliberate design choice, so baseline
  accepts the assertion without interrogating whether a 4xx/5xx or a subscription-id in the
  response is being silently discarded.
- **With talent:** Rule "Demand a reason for every narrow. 'Not needed' is not a reason."
  drives the talent to reject the framing and enumerate what the response side would carry:
  the subscription id you may need to unsubscribe later, error responses that mean the webhook
  is NOT registered (so "fire and forget" silently drops real failures), retry semantics. It
  asks for a defensible reason or a tracked follow-up, and records the decision either way.
- **Verdict:** PASS. The talent resists the exact social-pressure pattern — a confident "not
  needed" — that talks baseline into signing off on a half-contract. It converts an assertion
  into an examined, recorded decision. Clear, differentiated win.

---

## Scenario 5 — Self-contained change with no mirror side (negative trigger, don't invent axes)
**Input:** "I renamed the local variable `tmp` to `retry_count` inside `poll_once()` and fixed
the off-by-one in its loop bound. Small diff. Anything else this should touch?"
**Pass criterion:** Recognizes this change has NO symmetric contract and NO variant fan-out —
it is a local, self-contained fix — and does NOT manufacture mirror sides or variant axes.
Correct answer is roughly "no contract axes here; just make sure the loop-bound fix has a test
that would have caught the off-by-one." Inventing an encode/decode or provider-fan-out sweep =
fail (over-widening, the talent's own "do not invent axes" boundary).
- **Baseline:** Naturally treats this as a small local fix and suggests a test for the
  off-by-one. Baseline is *fine* here — nothing tempts it to widen.
- **With talent:** Rule "Do not invent axes the contract does not have; over-widening is its
  own failure." A variable rename plus a loop-bound fix touches no paired operation, no enum,
  no provider set. The talent should decline to run a contract sweep and instead note only the
  one real obligation — a regression test for the boundary — which is the single legitimate
  "axis" (every new/changed path implies a test). It must not fabricate a decode or a
  multi-variant sweep to look busy.
- **Verdict:** PASS (boundary). The talent matches rather than beats baseline by correctly
  declining to widen. Value is negative-precision: a completeness talent that fired a full
  mirror-and-variant sweep on a local rename would be *worse* than baseline. This one holds
  its boundary.

---

## Scenario 6 — Peer EXISTS but is stale, and a coverage-% ask (overlap + gap probe)
**Input:** "I added a `priority` field to `encode_task()`. `decode_task()` already exists, so
the decode side is covered. Also — are we at 80% line coverage on this file? That's our bar."
**Pass criterion:** (a) On the coverage-% question, the talent DECLINES the threshold framing
and defers to `test-coverage` — measuring a percentage is explicitly not its job. AND (b) it
must NOT mark the decode axis "covered" on the mere *presence* of `decode_task()`: adding a
field to encode means the peer must be checked for whether it actually reads `priority` back,
and the roundtrip is what proves it. A pass that rubber-stamps "decode exists → covered" and
answers the 80% question directly = fail.
- **Baseline:** Likely answers the 80% coverage question head-on (runs/estimates line
  coverage) and, on the field addition, accepts "decode already exists" at face value —
  merging a new encoded field whose decoder silently ignores it, so `priority` roundtrips to
  its default and is lost with no error.
- **With talent:** On (a), the "When NOT" boundary is explicit — "measuring coverage to a
  percentage threshold (test-coverage)" — so the talent hands the 80% question off rather than
  chasing a number. It steers correctly. **GAP on (b):** the talent's Step 4 classifies an
  axis as **covered** = "patch handles it," and Step 3's grep confirms a `decode_task()` peer
  *is present*. The method's presence-based sweep can mark decode "covered" because the sibling
  exists, when the real question is whether that sibling was UPDATED for the new field. The
  talent's roundtrip *rule* is the thing that would catch it (input-with-priority → encode →
  decode → equals input would fail), but the method only "notes when a roundtrip is absent" —
  it is Read/Grep-only and does not execute, so a stale-but-present peer can pass the
  structural sweep unless the reviewer manually reads `decode_task`'s body for the new field.
  Presence of a peer ≠ correctness of a peer, and Step 4's "covered" label does not force that
  distinction.
- **Verdict:** WEAK / PASS-with-gap. On (a) the talent decisively beats a baseline that would
  answer the coverage-threshold question — the negative trigger fires cleanly. On (b) there is
  a real, specific gap: "covered" is defined by the peer's *existence*, not by verifying the
  peer handles the newly-added variant/field, so a present-but-stale mirror side (a decode that
  ignores the new field) can be mis-marked covered. Identified GAP: Step 4 needs a "covered"
  bar of *peer demonstrably handles the new case* (read its body / roundtrip it), not merely
  "peer exists."

---

## Summary
| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | encode v2, no decode | application (core) | PASS |
| 2 | new enum in 1 of 5 switch sites | fan-out trap | PASS |
| 3 | reverse path is codegen'd | deliberately-narrow (boundary) | PASS |
| 4 | "response side isn't needed" | reason-demand pressure | PASS |
| 5 | local rename + off-by-one | negative trigger | PASS (boundary) |
| 6 | stale peer + 80% coverage ask | overlap + gap | WEAK (gap) |

**Passed: 5 / 6.**

**Overall:** The talent decisively and materially beats baseline on its core target class. S1
surfaces a defect that lives entirely *outside* the diff — a serializer with no deserializer —
which a line-by-line review structurally cannot see because the missing side is absent from
the patch. S2 is the multi-variant fan-out the talent exists for: one switch branch updated,
four sibling sites left stale, and a green build hiding it; the "use the codebase's own
sibling branches as the authority" rule turns "it compiles, ship it" into a peer-by-peer
sweep. S3 shows correct *restraint* — accepting a generated reverse path as a justified narrow
and redirecting to a roundtrip test rather than mandating redundant hand-written code. S4
resists the "it's not needed" social pressure that talks baseline into signing off on a
half-contract, forcing a recorded, defensible decision. S5 holds the "do not invent axes"
boundary on a local fix. These are behaviors baseline produces only sporadically and never
with an auditable covered/missing/narrow rationale led by the gaps.

**Gap (Scenario 6):** One real soft spot that does not touch the central claim. Step 4's
**covered** classification is satisfied by the *presence* of a peer branch (Step 3's grep
finds `decode_task()`), but presence is not correctness: when the patch adds a field or
variant, the peer must be checked for whether it actually handles the new case. A
present-but-stale mirror side — a decoder that silently ignores the newly-encoded field — can
be mis-marked "covered" by a Read/Grep-only structural sweep. The roundtrip rule is the
backstop that would expose it, but the talent only *notes when a roundtrip is absent* (it does
not execute — correctly, per its method-only scope), so the safety depends on the reviewer
manually reading the peer's body for the new case. The (a) half of S6 — deferring the 80%
coverage-threshold question to `test-coverage` — passes cleanly and confirms the boundary with
its neighbor talents.

**Recommended fix (non-blocking):** Tighten Step 4's definition of **covered** — "an axis is
covered only when the peer branch is shown to handle the *specific new variant/field/mode this
patch introduced* (read its body, or point at the roundtrip/test that exercises the new case),
not merely because a peer of the right name exists. A present-but-stale peer that ignores the
new case is **missing**, not covered." Optionally add to the Rules: "When the patch adds a
field or value to one side of a pair, the mirror side is presumed stale until its handling of
that specific addition is confirmed." This closes the only place the structural sweep can
label an unverified peer as done.

**Verdict: PASSED** — decisive, differentiated wins on its core one-sided-patch target and on
the multi-variant fan-out trap, correct restraint on a justified narrow, resistance to the
"not needed" pressure case, and a correct decline on both the local-change boundary and the
coverage-threshold overlap with `test-coverage`. One non-blocking gap (presence-of-peer is
scored as covered without verifying the peer handles the new case) noted for a future edit.
