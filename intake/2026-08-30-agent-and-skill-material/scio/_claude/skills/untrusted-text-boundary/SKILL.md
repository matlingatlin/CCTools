---
name: untrusted-text-boundary
layer: A
phase: build-time
status: written
description: Decide where text a person wrote gets neutralised on its way into a prompt, and what a gate does with what it refuses. Use when user prose is stored and later re-rendered into a prompt, when reviewing prompt-injection defences, when a denylist or validation runs at write time, when deciding what a blocking gate may log or persist, when a secret or credential could be pasted into an answer, when adding a pattern scanner, or when asked whether some text is trusted. Carries the execution-capable-destination test, render-boundary neutralisation and why write-time checking cannot replace it, scan-at-sink on the exact bytes, secret-matching rules with their published blind spots, and the rule that oversized input fails closed before any pattern runs.
---

# untrusted-text-boundary

Scio stores prose a person wrote and later renders it into prompts — in Layer A's spec fields, in
Layer B's `Playbook` interpolation, in Layer F's free-text markings on a preview. Its defence today
is validation at write time.

**Write-time validation is a denylist, and a denylist does not cover records written before the
pattern existed.** This skill is about the boundary that does, and where the other boundaries go.

---

## 1 · The question to ask first: is the destination execution-capable?

The useful framing is not *"is this text trusted?"* — almost no text is, and the answer changes
nothing. It is:

> **Is the destination execution-capable?**

Text landing in a log line and the same text landing in a prompt that produces code are the same
bytes and completely different risks. Scio's case is the sharp one: **the build prompt produces
code that runs, against a spend ceiling.** The classification is per *destination*, and one piece
of stored text usually has several.

The chain, as `docs/next/LAYER-A-INTAKE.md` §1.1a records it after reading the code, is a worked
example of why the destination and not the source is the unit:

| Point | Fenced? |
|---|---|
| `intake/extraction.py:285` wraps the transcript in `fence(...)`, with the untrusted-input instruction in the system prompt | **yes** |
| `intake/questions.py:130` and `:143` paste `conversation.as_prompt()` raw; the question system prompt has no such instruction | **no** |
| `_merge_list` (`extraction.py:142`) keeps *"the user's own wording"* by design; `layerb/whole.py:95` interpolates those values into a prompt | **no** |

Same text, same turn, same layer — fenced on one path and not the other. One test covers the
fenced half (`tests/test_prompt_injection.py:65`); the other half has none.

---

## 2 · Neutralise at the render boundary, not only at write

The mechanism, from `gstack lib/gstack-decision.ts`, is about ten lines. Stored free text is passed
through `datamark()` **on every read, before it reaches a model**:

| Transformation | What it defeats |
|---|---|
| strip C0/C1 control characters and U+0085 / U+2028 / U+2029 | invisible characters that break out of a quoted region |
| neutralise markdown code fences | text that closes the fence it was put inside |
| neutralise `---` banner sentinels | text that impersonates a document or frontmatter break |
| insert a zero-width space inside `<|` and `|>` | special-token impersonation |
| insert a zero-width space inside `system` / `user` / `assistant` / `tool` tag forms, and inside `Human:` / `Assistant:` / `System:` / `User:` | role impersonation in both the tag and the chat-transcript dialects |

The commentary is the finding:

> *"Write-time `hasInjection` is a denylist; this is the render-boundary defense-in-depth that also
> covers `--all` / snapshot reads and records written before a pattern existed."*

**Both boundaries, not one.** Write-time keeps obvious garbage out of the store and is where a
pasted credential should be caught and refused (§5). Render-time is what protects records that were
already stored — including every record written before today's pattern list existed, which is a set
that only grows.

**What this does not do:** it does not make the text safe. It makes the text *unable to impersonate
structure*. A sentence that simply asks the model to do something else is untouched, and no
transformation on this list would catch it.

---

## 3 · Scan the bytes that will actually be sent

> *"Scan-at-sink on the EXACT bytes that will be sent: write to a temp file, scan that file, pass
> the SAME file downstream. Never scan a string then re-render it."*

Scio's gate validates a `Spec` **object**; a later stage renders a prompt from it. **The
serialisation between them is unchecked**, and every check performed before a re-render is a check
of something other than what ships. One temp file, scanned and passed, closes that by construction
rather than by review.

The general rule: **a check and the thing it certifies must be the same bytes.** If a transformation
sits between them, the check certifies the input to the transformation and nothing else.

---

## 4 · What a gate does with what it refuses

A blocking gate that logs its rejected input has leaked. The invariant, stated as the name of a
test in the source repository:

> **When the scan blocks, the raw text must not be persisted anywhere downstream — no archive
> write, no transcript log, no onward dispatch.**

This is the half that gets forgotten, because the refusal *feels* like the end of the story and
because the debugging instinct is to log what was refused. Three specific sinks to check by name
whenever a gate is added: the audit log, the error message returned to the caller, and any
telemetry or metrics payload that carries a sample of the input.

Scio has written this rule and not the test — see `docs/triage/LAYER-A-TRIAGE.md` #37.

Two more properties of their gate worth knowing when designing one, both **decisions rather than
procedures**, so they are recorded here as context and not as recommendations: refusal outcomes
came in three tiers with the top tier unskippable by any flag, and an unknown repository visibility
was treated as public-strict — **unknown means strictest**. Adopting either in Scio's gate changes
its contract; that is an ADR (`LAYER-A-TRIAGE.md` #32).

---

## 5 · Matching a secret in the output, and admitting what you miss

If user prose can carry a pasted API key — and for an app builder it can — then the interesting
test is not whether the key was refused but whether it turns up in any output. The harness from
`gstack test/helpers/secret-sink-harness.ts` seeds a known secret and walks four channels, with
four match rules:

| Match rule | Why it exists |
|---|---|
| exact | the base case |
| **URL-decoded** | percent-encoded passwords inside connection strings |
| **first 12 characters**, for seeds ≥ 16 chars | the *"I only logged a portion"* pattern |
| **base64**, for seeds ≥ 12 chars | the value inside an auth header |

**Both length thresholds exist to bound false positives, and both are stated.** A threshold with no
stated reason gets tuned by whoever hits a false positive next.

Two further properties to copy:

- **The blind spots are published** — in their case a subprocess environment dump and the user's
  real shell history, each with a reason. A harness whose gaps are undocumented gets read as
  complete.
- **The assertion shows the right observable.** Their best line asserts that the output contains
  `len=43` — *the length of the secret is visible, the value is not.* That is the shape every log
  line touching a secret should have.

Scio's channels are different — sandbox filesystem, relay, preview, logs — so the channel list is
ours to write. The **match rules and the thresholds transfer unchanged.**

Every one of these tests asserts an absence, so every one needs a positive control: see `testing`
§3.5, which is the law that makes this section worth running at all.

---

## 6 · Size before patterns: fail closed, and never let a bad limit disable the guard

A pattern scanner is itself an attack surface. Three parts, in this order:

1. **A static lint for nested quantifiers** over the pattern set — a shape check on the regexes
   themselves, run in CI, not at request time.
2. **A runtime budget** per scan, generous enough that only a catastrophic pattern breaches it.
3. **A size cap checked *before* any pattern runs, failing closed.** Oversized input is refused, not
   scanned.

The third is the real backstop and it is the one usually written last: it is the only part that
holds when a pattern with a bad shape gets through the lint.

**And the detail that turns the guard off in production:** a malformed cap value must fall back to
the default, never disable the check. A `NaN` or a `≤ 0` read from configuration must not be
interpreted as *"no limit"*. This is a two-line branch and it is the difference between a guard and
a guard-shaped comment.

---

## 7 · Limits — what the sources show versus what we would be assuming

| The source shows | We would be assuming |
|---|---|
| Ten lines of string transformation shipped in a real tool | that it stops prompt injection. **It does not.** It stops text from impersonating *structure*. Plain instructional text passes through untouched, and the sources do not claim otherwise |
| Tests that a scanner catches seeded secrets in four channels | that it catches unseeded ones. A sink harness measures the channels you thought of. Its published blind spots are the honest part; a harness reported without them is a coverage claim it did not earn |
| A refusal invariant enforced by a test in **their** repo | that ours would hold. We have the rule and no test — the whole content of finding #37 |
| Scan-at-sink on a file passed downstream, in a **CLI** | that a temp file is the right mechanism in a Python service where the "sink" is an HTTP request body. The principle (*check the exact bytes that ship*) transfers; the file does not, necessarily |
| Prose mitigations widely deployed in prompts | that prose in a prompt is a mitigation at all. `ECC-MINED` §1.5 measured the opposite: a presence-of-boilerplate rule was **satisfied by a paste in 67 of 68 files.** Text instructing a model to ignore instructions is not a boundary |
| — | that any of this is verified against a real model. `docs/next/LAYER-A-INTAKE.md` §1.1a carries the review's own caveat: *no test proves that a real model resists a real injection.* Every mechanism here is structural, and structural is what we can actually assert |

**The honest summary:** these are boundaries that make a class of attack *structurally* harder and
that can be tested deterministically. None of them is evidence that a model behaves. Do not let a
green suite here be reported as injection resistance.

---

## 8 · Eval

| # | Case | Expected |
|---|---|---|
| E1 | A stored field containing `<|im_start|>`, then rendered into a prompt | Neutralised at render. Assert on **the bytes handed to the relay**, not on the stored value |
| E2 | The same field, written **before** the transformation existed | Same result. This is the case that write-time validation cannot cover, and the reason the boundary is at render |
| E3 | A field containing a closing code fence, rendered into a fenced region | The region still closes where it should |
| E4 | A field containing `Human:` at the start of a line | Neutralised in the chat-transcript dialect as well as the tag dialect |
| E5 | Text that politely asks the model to ignore its instructions | **Passes through unchanged, and that is correct.** This case exists so nobody reports the transformation as injection defence |
| E6 | Every path from a stored user value to a prompt, enumerated | Each is either fenced or explicitly listed as not needing it. Today `questions.py:130` and `:143` fail this |
| E7 | A gate refuses a spec containing a credential | The credential appears in no store, no log, no error payload, no telemetry. Four assertions, named separately |
| E8 | A seeded secret, per channel | Caught by each of the four match rules. **Plus a deliberate leak per channel** proving the harness can fail (`testing` §3.5) |
| E9 | Input one byte over the size cap | Refused before any pattern executes. Assert that the scanner did not run, not merely that the result was a refusal |
| E10 | Cap configured as `0`, `-1`, and a non-numeric string | Default cap applied in all three. **No configuration value disables the guard** |
| E11 | The pattern set, linted | No nested quantifiers; and a deliberately planted catastrophic pattern **is** flagged by the linter |

**E2 and E5 are the pair that keeps this honest.** E2 is the reason the boundary exists where it
does; E5 is the reason nobody should oversell it.

---

## 9 · When this skill is the wrong tool

- **Deciding whether a value is legitimately grounded in what the user said.** That is
  `ais-grounding`; this skill does not care what the text means.
- **Deciding what a gate's outcome vocabulary should be.** That is an ADR.
- **General test design.** `testing` — in particular §3.5, which every eval above depends on.
