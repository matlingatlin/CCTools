# Ablation 01 · `as-built` — the first measurement of any skill in this project

**Date:** 2026-08-26
**Method:** manual with-versus-without arm, because `claude plugin eval` is early-access gated on
this account. This is the shape that command would have automated, and the shape
`obra/superpowers` prescribes anyway: *watch an agent fail without the skill first.*

## Setup

Two fresh subagents, identical prompts except one sentence. Both worked in `/home/user/scio` with
`/home/user/hello-world` also on disk and writable access to neither.

**Question:** *Layer C runs a plan validation before building. How many distinct validation rules
does it run, and does anything in the system read the result?*

**Arm A** got no mention of the skill. **Arm B** was told to read and follow
`.claude/skills/as-built/SKILL.md`.

Both were asked to report their answer, confidence, whether they opened the old repository, and
their tool-call count.

## Result

| | **A — no skill** | **B — with skill** |
|---|---|---|
| Rule count | **9 — correct** | **7 — wrong** |
| "Nothing reads it" | correct | correct |
| Opened `hello-world` | yes, 4 files | **no** |
| Tool calls | 8 | **10** |
| Confidence | high | high |

**Ground truth, counted at source:** `grep -o 'rule="[a-z_]*"' layerc/validate.py | sort -u` → **9**.
`grep -c '^def _check' ` → **7**. Both numbers are true of different things; a violation carries a
`rule` name, so nine is the count the question asks for.

## What actually happened

**The skill made the answer worse, and it cost more to get there.**

Arm A went to `docs/as-built/LAYER-C-BUILD-PLAN.md` **unprompted**, read its claim of nine, opened
`validate.py`, and counted. The document did the routing; the skill was not needed to find it.

Arm B obeyed the skill's central instruction — *do not open hello-world* — and then hit something
neither of us had accounted for: **our own two documents disagreed.** `00-INDEX` said seven,
`LAYER-C-BUILD-PLAN` said nine. Arm B resolved it the only way left to it, by counting outgoing
`calls` edges from `validate_plan` in the graph. That gives **seven**, because call edges count
*functions*. The answer is nine, because violations carry *rule names*.

**A graph query cannot settle a disagreement about units.** It answers precisely and about the
wrong thing.

## What the skill nevertheless did better

Arm B **found the contradiction**. Arm A read "nine" and confirmed it without ever noticing that
another document in the same repo said seven. One arm got the right answer and missed a live defect;
the other got the wrong answer and found it.

That is worth stating plainly: the skill's routing works. Its *stopping rule* does not.

## Three things fixed because of this

1. **The contradiction is gone.** `00-INDEX:119` and `LAYER-C-BUILD-PLAN:204` now both say seven
   check functions emitting nine rule identifiers, with the unit attached. The cross-document review
   flagged this and it had been fixed everywhere except the one file `CLAUDE.md` makes mandatory
   first reading.
2. **The skill has an escape hatch it lacked.** *When two documents disagree, stop and go to the
   code* — the one case where the no-cloning rule yields.
3. **And a sentence about what the skill is for.** *A retrieval budget is not an accuracy budget.*
   Cheap and wrong is the worst outcome available.

## What this says about the other sixteen

The skill we trusted most produced a confidently wrong answer on its first measurement, and would
have kept doing so indefinitely, because nothing was measuring. **Sixteen skills remain unmeasured.**

It also says something about how to read the result: a single case, run once per arm, is not an eval.
It is one observation, and it happened to land on a question where our documents were inconsistent —
which is precisely why it was informative. Repeat it on clean questions and the delta will likely
reverse; the point is that nobody knows yet.
