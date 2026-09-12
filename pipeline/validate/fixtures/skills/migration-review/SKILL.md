---
name: migration-review
description: Use when reviewing a database migration before deploying it, or when asked whether a schema change is safe to ship. Covers drop column, table rename, backfill, index creation and lock escalation. SYNTHETIC FIXTURE, not a real skill.
allowed-tools: Read, Grep, Bash
---

# Migration review

SYNTHETIC FIXTURE. This directory exists so `pipeline/validate/selftest_skill.py` has
one artefact the skill checker accepts cleanly, which it can then break one thing at a
time. It is not installed, not adopted, and nothing in it is a finding.

## Important — read before the steps

A verdict is per statement, never per file. One safe file is a file whose every
statement is safe; a single irreversible statement decides the whole verdict.

## Steps

1. Split the migration into statements.
2. Mark each one reversible or irreversible.
3. For anything irreversible, name the reader that makes it so.
4. Emit the verdict on the shape in `assets/verdict-template.md`.

## Resources

- [Lock modes and what escalates them](references/lock-modes.md) — which statement
  takes which lock, and when a lock upgrades under load.
- `scripts/split_statements.py` — splits a migration file into numbered statements so
  step 1 is deterministic rather than eyeballed.
- `assets/verdict-template.md` — the shape the verdict is emitted on.
