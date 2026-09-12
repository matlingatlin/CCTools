---
title: The KERNEL prompt pattern — what it says, and what its numbers are worth
sources:
  - note: "Screenshot of the Reddit post by u/volodith in r/PromptEngineering, 'After 1000 hours of prompt engineering, I found the 6 patterns that actually matter' (only the K section visible). Received 2026-09-02."
  - url: https://x.com/MarcusMusashi/status/1998958759897383048
    note: "Verbatim repost of the same text; used to recover the other five letters. Not read in full — search snippet."
    fetched: 2026-09-02
  - url: https://www.threads.com/@power.ai/post/DRd-UtXjt_P/
    note: "Names all six letters. Secondary."
    fetched: 2026-09-02
tags: [prompting, patterns, claims-graded]
related: ["[[loop-engineering-and-fable-prompting]]", "[[skill-authoring-best-practices]]", "[[requirements-discovery]]", "[[third-party-landscape]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# KERNEL

A single practitioner's post, widely copied (X, Threads, at least four Medium rewrites).
It is a mnemonic, not a study: "tracking and analyzing over 1000 real work prompts" is
asserted, and no data, method or prompt set is published anywhere the copies point to.

## The six patterns (REPEATED — identical across copies)

| letter | rule | the post's example |
|---|---|---|
| **K** — Keep it simple | one clear goal, not 500 words of context | "Write a technical tutorial on Redis caching", not "I need help writing something about Redis" |
| **E** — Easy to verify | replace "make it engaging" with "include 3 code examples" | if you cannot verify success, the model cannot deliver it |
| **R** — Reproducible | no "current trends" / "latest"; pin versions and exact requirements | same prompt, same result |
| **N** — Narrow scope | one prompt = one goal; not code + docs + tests in one | |
| **E** — Explicit constraints | say what must not happen | |
| **L** — Logical structure | Context → Task → Constraints → Format | |

## The numbers (REPEATED, unsupported)

"70% less token usage, 3x faster responses" (K), "constraints reduce unwanted outputs by
91%" (E), "quietly doubled the team's AI-assisted output, cut token usage in half". No
denominator, no baseline, no prompt set. They are the kind of number this repo does not
carry into a decision (`pipeline/CONSTANTS.md`: measured against a threshold fixed before
the number existed, or not a measurement).

## Where it agrees with, and where it contradicts, sourced guidance

- **E (easy to verify)** and **L (structure)** match Anthropic's own pages and our
  `skill-contract` (a step is a check someone could run).
- **K (strip context)** is in direct tension with Anthropic's Fable 5 guidance "Give the
  reason, not only the request" — the model "tends to perform better when it understands
  the intent behind a request" (see [[loop-engineering-and-fable-prompting]]). The
  reconciliation is the one the Redis example itself shows: KERNEL strips *vague*
  context, not *purpose*. A sentence of why is not 500 words of preamble.
- **R (reproducible)** is a real constraint on eval prompts: our test prompts already ban
  temporal references for the same reason.

Nothing here is new to the library; `prompt-refinement` covers the same ground with
sources. Keep this note as the map from the meme to the evidence, so the next time the
acronym arrives it does not have to be re-graded.
