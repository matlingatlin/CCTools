# Eval: hybrid-parse-escalation

Functional regression test for the `hybrid-parse-escalation` talent. This is a **technique**
talent: parse a mostly-regular feed DETERMINISTICALLY first, score each record's parse
confidence, and escalate ONLY the low-confidence tail to a cheap LLM, keeping the
deterministic wins and merging both paths into one schema. Its sharpest, most-differentiated
behaviors are (a) refusing to send every record to an LLM when a parser handles the bulk for
free, (b) refusing to silently drop the tail a regex-only approach loses, (c) gating
escalation on a *measured* confidence signal rather than a guess, and (d) folding a recurring
outlier back into the parser instead of paying to escalate it forever.

Method: for each scenario, reason through the likely output WITHOUT the talent (baseline
Claude) vs WITH the talent's method applied, and judge whether the talent produces a
materially better, criterion-meeting result. Adversarial, not a rubber stamp. Traps are
included in BOTH directions — the two classic single-strategy failure modes (LLM-everything =
overpay; regex-only = silent drop), plus the talent's own negative triggers (one-off parse;
free-form prose with no structure) that should make it *decline* to build the pipeline.

Date: 2026-08-27 · Talent version: SKILL.md as of this commit.

---

## Scenario 1 — Bulk extraction from a mostly-regular feed (application, core target)
**Input:** "We ingest ~200k receipts/day, ~90% from one POS export format, the rest a long
tail of odd layouts. Extract `vendor`, `date`, `total`, `currency`, `line_items[]` from each.
An LLM call per receipt is blowing the budget. Fix it."
**Pass criterion:** Proposes a DETERMINISTIC parser (regex/grammar/format rules) for the
dominant format, a per-record confidence signal, and escalation of ONLY the low-confidence
rejects to a cheap LLM — then merges both paths into ONE schema with a source tag. Must NOT
recommend LLM-per-record, and must NOT propose regex-only that abandons the tail.

- **Baseline:** Tends to pick one of the two single-strategy failure modes. Either "use a
  cheap model and batch the receipts" — still an LLM call for all 200k, paying top price for
  the 90% a parser handles for free — or "write a regex for the POS format," which quietly
  drops or mis-parses the 10% tail with no accounting of what was lost. Rarely proposes the
  split deliberately, and rarely specifies a confidence gate.
- **With talent:** Step 1 samples and names the dominant format + outlier shapes and fixes the
  target schema. Step 2 writes a high-precision parser for the 90%. Step 3 defines a measured
  confidence signal (all required fields matched, `total`/`currency` type-valid, no unparsed
  residue). Step 4 accepts high-confidence parses free and routes only the ~10% rejects to a
  cheap LLM with the schema + raw record. Step 5 normalizes both into one schema, tagged by
  source. Result: ~90% of volume at zero LLM cost, model spend only on the hard tail, nothing
  dropped.
- **Verdict:** PASS. Directly attacks the cost driver (LLM calls × volume) while closing the
  silent-drop hole that the cheap regex alternative leaves open. Order-of-magnitude cost cut
  with equal-or-better coverage. Decisive, differentiated win.

---

## Scenario 2 — LLM-everything pressure (overpay trap)
**Input:** "Just pipe all the log lines through the cheap model to pull out `timestamp`,
`level`, `service`, `latency_ms`. Models are good at this now — why bother writing a parser?"
**Pass criterion:** Resists sending a highly-regular feed to an LLM at all. Establishes that a
structured log line is deterministically parseable, so the parser IS the default path and the
LLM is only the tail fallback. Agreeing to "cheap model for every line" = fail.
- **Baseline:** Susceptible to the framing. "The model is cheap and handles messiness" is a
  plausible-sounding answer, and baseline may endorse LLM-per-line, paying a recurring
  per-record tax on lines a single regex nails 99%+ of the time.
- **With talent:** Rule "Deterministic first, always — the LLM is the fallback for the tail,
  never the default path." A regular log format is the textbook case: one regex/grammar
  handles the overwhelming bulk at zero marginal cost; the LLM earns its keep only on
  malformed/novel lines. The talent reframes the request instead of complying with it.
- **Verdict:** PASS. The talent refuses the exact overpay pattern it exists to prevent, and
  gives a principled reason (marginal cost per record) rather than a habit. Clear win over a
  baseline that can be talked into the expensive default.

---

## Scenario 3 — "Regex it and move on" (silent-drop trap + measured-gate trap)
**Input:** "Write me a regex to pull the order IDs out of these 2M support emails and dump
them to a table. If some don't match, whatever — the weird ones don't matter."
**Pass criterion:** Refuses to SILENTLY drop non-matching records — every record must end
parsed, escalated, or explicitly quarantined for review — AND gates on a measured signal
rather than trusting "it matched" blindly. A regex + implicit drop of the misses = fail.
- **Baseline:** Likely complies: writes the regex, and non-matches just don't appear in the
  output. The 2M-email scale hides the loss — nobody sees how many order IDs silently
  vanished, and "the weird ones don't matter" is accepted at face value even though a
  systematic non-match (e.g. a whole email template variant) could be dropping thousands of
  real orders.
- **With talent:** Rule "Never silently drop" forces the misses into an escalation queue or an
  explicit quarantine bucket with a count, not `/dev/null`. Rule "Confidence gates escalation
  — a record with unparsed residue or a failed check is a reject, not a pass" plus the
  escalation-rate health metric surface how big the tail actually is, converting an invisible
  data-loss bug into a measured, handled quantity.
- **Verdict:** PASS. The talent turns a silent, scale-hidden data-loss failure into an
  accounted-for split with a visible reject rate. This is precisely the failure regex-only
  pipelines ship to production, and baseline is prone to it under the user's framing.

---

## Scenario 4 — Escalation rate climbs after upstream change (tuning discipline)
**Input:** "Our hybrid extractor's escalation rate jumped from 3% to 17% last week and the LLM
bill with it. Nothing in our code changed. What do we do?"
**Pass criterion:** Reads rising escalation rate as the health signal it is (format drift /
new recurring outlier), diagnoses the newly-common shape, and FOLDS it back into the
deterministic parser — a permanent cost cut — rather than absorbing 17% escalation as the new
normal. Just "raise the budget" or "keep escalating" = fail.
- **Baseline:** Without the framing, may treat the symptom (higher bill) and suggest a cheaper
  model or a bigger budget, or shrug at "the data got messier," leaving a recurring, growing
  LLM tax in place and no diagnosis of *what* changed.
- **With talent:** "Escalation rate is the health metric — rising rate means the format
  drifted or the parser is stale." Step 6: "If escalation rate is high, widen the parser to
  absorb a recurring outlier (cheaper than escalating it forever)." The move is to sample the
  new rejects, find the recurring shape (e.g. a second date format from a new vendor), extend
  the parser to cover it, and watch the rate fall back toward 3%.
- **Verdict:** PASS. The talent converts a recurring, compounding cost into a one-time parser
  fix and names the exact metric that flags it. Baseline lacks the "escalation rate = drift
  signal → fold back" reflex. Strong, differentiated win.

---

## Scenario 5 — Single one-off parse (negative trigger; don't over-engineer)
**Input:** "Here's one gnarly invoice as a blob of text — can you pull the total and the due
date out of it for me?"
**Pass criterion:** Recognizes this is a ONE-OFF and does NOT stand up the whole
parser + confidence-gate + escalation + merge pipeline. Just extracts the two fields directly.
Building deterministic-parser machinery for a single record = fail (fails the talent's own
"NOT for a single one-off parse" boundary).
- **Baseline:** Naturally just reads the invoice and returns the total and due date. Correct
  and appropriately lightweight — baseline is *fine* here.
- **With talent:** "NOT for: a single one-off parse." A correct application of the talent is to
  NOT fire — no amortization exists over one record, so parser-writing overhead exceeds any
  saving. The talent should stay out of the way and let the direct extraction happen.
- **Verdict:** PASS (boundary). The talent does not beat baseline here — it *matches* it by
  correctly declining. Value is negative-precision: it names the boundary so it won't
  over-engineer a one-off. A talent that fired here would be worse than baseline; this one
  doesn't.

---

## Scenario 6 — Free-form prose + trusting the LLM path (negative trigger + gap probe)
**Input:** "Extract the customer's main complaint and their desired resolution from 40k
free-text survey responses — no template, people just wrote paragraphs. Set up the hybrid
parse to keep costs down."
**Pass criterion:** (a) Recognizes there is no exploitable deterministic structure, so the
regex-first split does NOT apply and it should decline the hybrid framing (route to LLM
extraction, or cost-aware-model-routing, not a parser). AND (b) if it DOES apply a hybrid step
anywhere, it must not trust the escalated LLM output unconditionally — the LLM path needs the
same schema/type validation the deterministic path gets.
- **Baseline:** May try to force regex/keyword rules onto genuinely unstructured prose
  ("complaint" keyword matching), producing brittle, low-precision extraction — the wrong tool
  — or may just send everything to a model with no cost thought.
- **With talent:** "NOT for: genuinely free-form prose with no exploitable structure." Step 1's
  "characterize the format" surfaces that there is no dominant machine-parseable format, so the
  deterministic-first premise fails and the talent should decline rather than manufacture a
  fake parser. It correctly steers away from (a). **GAP on (b):** the talent's confidence gate
  (Step 3) is defined only for the deterministic path. Step 5 says "normalize" the LLM output
  into the schema but the escalated records are then merged and trusted — the confidence gate
  is never re-applied to the LLM path. An LLM escalation that hallucinates a field, returns the
  wrong type, or emits malformed output is normalized-and-merged, not re-validated. The talent
  also relies on a purely STRUCTURAL confidence signal (fields present, types valid, no
  residue), which cannot catch a *structurally-valid-but-semantically-wrong* deterministic
  parse (e.g. subtotal captured into `total`); Step 6's labeled-slice accuracy check is the
  only backstop, and it is periodic sampling, not a per-record gate.
- **Verdict:** WEAK / PASS-with-gap. On (a) the talent decisively beats a baseline that would
  force regex onto prose — the negative trigger fires correctly. On (b) the talent has a real,
  specific gap: escalated LLM output is trusted rather than run back through a validation gate,
  and the confidence signal is structural-only. Identified GAP: no validation gate on the LLM
  path, and no acknowledgement that a high-confidence deterministic parse can still be
  semantically wrong.

---

## Summary
| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | 200k receipts, 90% one format | application (core) | PASS |
| 2 | "cheap model for every log line" | overpay trap | PASS |
| 3 | "regex it and drop the misses" | silent-drop trap | PASS |
| 4 | Escalation rate 3%→17% | tuning discipline | PASS |
| 5 | Single one-off invoice | negative trigger | PASS (boundary) |
| 6 | Free-form prose + trust LLM path | neg. trigger + gap | WEAK (gap) |

**Passed: 5 / 6.**

**Overall:** The talent decisively and materially beats baseline on its core target class and
on BOTH single-strategy failure modes. S1 shows the split (parser for the bulk, LLM for the
tail, one merged schema) against a baseline prone to LLM-per-record overpay or regex-only
silent drop. S2 resists the "models are cheap, skip the parser" framing that talks baseline
into paying a per-record tax on a trivially-parseable feed. S3 converts a scale-hidden,
silent data-loss bug into an accounted-for reject rate — the talent's "never silently drop" +
"confidence gates escalation" rules doing exactly their job. S4 names escalation rate as the
drift signal and folds a recurring outlier back into the parser, turning a compounding cost
into a one-time fix. S5 correctly DECLINES on a one-off, so it won't over-engineer. These are
behaviors baseline produces only sporadically and never with an auditable cost/coverage
rationale.

**Gap (Scenario 6):** Two related soft spots, neither touching the core claim. (1) The
confidence gate is defined only for the deterministic path; escalated LLM output is normalized
and merged but never re-validated against the schema, so a hallucinated field, wrong type, or
malformed LLM response can enter the output stream trusted. (2) The confidence signal is purely
structural (fields present, types valid, no residue), which cannot detect a
structurally-valid-but-semantically-wrong parse; Step 6's labeled-slice accuracy check is the
only backstop and it is periodic sampling, not a per-record gate. Both are refinements to a
sound method, not defects in its central "deterministic-first, escalate-the-tail" claim.

**Recommended fix (non-blocking):** Add to Step 5 / Rules — "Run the LLM output back through
the same schema/type validation as the deterministic path (required fields present, types and
ranges valid, well-formed); an escalation that fails validation is quarantined for review, not
merged. The confidence signal is structural — pair it with the Step 6 labeled-slice accuracy
check to catch high-confidence-but-wrong parses that the structural gate passes." This closes
the only place the talent trusts an unvalidated result.

**Verdict: PASSED** — decisive, differentiated wins on its core target and on both the overpay
and silent-drop traps, correct declines on both negative triggers, with one non-blocking
gap (validate the LLM path; structural confidence has a known blind spot) noted for a future
edit.
