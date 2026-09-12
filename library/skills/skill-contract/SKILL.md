---
name: skill-contract
description: Use when writing or rewriting the fields of a Claude Code skill - SKILL.md frontmatter, name, description, body, pointers, references, assets - against a field contract that states what each field must contain. Covers the order fields are written in, why description is written last, and how a code check and an independent reader are applied to each field before it is accepted.
license: internal
---

# Writing a skill field by field

A skill is not written top to bottom. Each field depends on fields that come later in
the file and earlier in the work, so writing them in file order means guessing at
things you are about to decide.

Two rules govern the whole phase:

1. **A field is written, then checked by code, then checked by a reader who cannot see
   how it was written.** Code first — there is no point asking anyone whether a
   1,400-character description reads well when the cap is 1,024.
2. **A red field never proceeds.** Fixing it later means the fields written after it
   were written against something that changed.

## Important — the contract is the source, this file is the method

Never restate a field's rules here or in your head. Read them from the contract file
at the moment you write the field. A rule quoted from memory is a rule that has
already drifted, and the whole point of holding rules as data is that the code checker
and the writer are reading the same sentence.

What this file governs is the *order*, the *inputs*, and the *evidence* each field
needs — none of which the contract states.

## Steps

**4.0 · The bill of materials, before any file exists.** One row per planned file:
what kind it is, why it is needed, and one of `exists` / `needed` / `not needed
because …`. No row may be blank. Nothing proceeds with an unclassified row: a gap
found here is a task, and the same gap found halfway through writing is an
improvisation. Check it in both directions at the end — planned files that never
appeared, and files that appeared unplanned.

**4.1 references, 4.2 assets.** Bundled knowledge is written before the body, because
the body points at it and cannot point at what is not decided. Every claim carries its
source and the date it was fetched; bundled knowledge goes stale and nothing in the
runtime will tell you when. Assets carry fields to fill in — a template with no slots
is prose.

**4.3 name.** Constrained enough that the contract decides it. Reserved words and the
directory match are checkable; nothing here is a judgement call.

**4.4 body: what this is, and when to use it.** Written from the candidate sentence and
the observed failures, not from the topic.

**4.5 body: the steps.** *Only observed failures may become rules.* A rule with no
observation behind it is an opinion, and it costs context on every invocation. If you
cannot name the run where the failure happened, the rule does not go in. Every step
ends in something checkable — a number, a file and line, a named artefact, a table
row. "Consider whether…" is not a step.

**4.6 pointers.** Every bundled file the reader is meant to open gets a pointer in the
body saying what is in it and when to open it. A bundled file must not point at
another bundled file: a nested reference is previewed rather than read, so the
information goes silently incomplete.

**4.7 description — last, and for a reason.** It needs three things that do not exist
earlier: the finished body's actual scope, the trigger vocabulary, and the descriptions
of the neighbouring skills it must not collide with. Write it from the words a person
types when they *have* the problem — symptoms, error strings, tool names — not the
vocabulary of the solution. Then read it beside its nearest sibling and ask which one a
router would pick for each other's job; if the answer is unclear either way, one of the
two descriptions is wrong.

**4.8 frontmatter policy.** The invocation policy follows from what kind of content the
skill carries, and only the contract decides which fields survive packaging.

## After each field

Run the code checker on the whole artefact, not just the field — a field can only break
rules that span fields once it exists. Then hand the field, the contract rule, and
nothing else to a reader who did not write it. Record for each field which code rules
went red, which reader questions went red, and how many rewrites it took. That record
is what tells you later which field costs the most rework, and therefore which part of
this method to fix.

See `references/field-writing.md` for the per-field inputs and the reader's question
for each one.

## In this repo (one instance)

The contract is `pipeline/contracts/skill.contract.json`; the code checker is
`pipeline/validate/skill_contract.py`; the per-field record goes to
`pipeline/ledgers/fields.jsonl` through `pipeline/build/record.py`.
