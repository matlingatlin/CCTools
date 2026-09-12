---
name: skill-builder
description: Use when turning an admitted build package into a tested skill - running the baseline probe, writing the skill field by field against the field contract, measuring it against the baseline, and deciding ship or iterate against a preregistered threshold. Expects a package that has already passed admission; it does not decide whether an idea is worth building.
---

# skill-builder — chain 4.0.0

Two modes, two prices. Read `pipeline/contracts/chain.contract.json` (`modes.candidate`,
`modes.promote`) before opening a record; `pipeline/build/run_phase.py` is the only way a
phase dispatches (one script per phase, writes and runs in one process).

## Candidate (default) — fill, check, one review, one rewrite. Under 15 minutes.
1. `record.py open <package> --mode candidate --coordinator-tier <tier>` — admission runs
   (package contract 1.3.0: every task carries `fixture_kind`, at least two kinds).
2. `run_phase.py probe <package> --k 1 --max-tasks 2` in the background — while it runs,
   write 1.1, 1.2, 4.0, 2.4, 2.5 and the artefact into `.claude/skills-candidates/<id>` in ONE
   authoring turn, description last. `skill_contract.py --context` after every field; log 5.1
   with `errors=<n>`.
3. `run_phase.py review <package>` — the description reader and the whole-artefact review in
   one fan-out. The review is ADVISORY: its findings are one rewrite (log the field rows), then
   5.1 again with `errors=<n>`. No second review, no cap, no abandon on the review.
4. `run_phase.py close <package>` — derives the coordinator turns from the run windows,
   decides (`candidate` when the last 5.1 has errors 0 and a review ran), writes the build row.
5. evals.md, the capability map line marked candidate, commit with `-F`, push.

## Promote — measure an existing candidate. This is where the cost is; say the budget first.
1. `record.py open <package> --mode promote ...` (a new id, e.g. `<id>-promote`).
2. `run_phase.py probe <package> --reuse-from <candidate build>` when prompt, fixtures, tier and
   effort are unchanged; otherwise `probe --k 1`.
3. `run_phase.py arms <package>` — with x k (k=1 when the baseline fails), without x1, incumbent
   only with `--incumbent <dir>`. Dispatch refuses a run past `budget.max_paired_runs`.
4. Expectations from the blinded copies in `blind/` (never from the labels); triggers (6.5);
   field trial (6.6) if the package names one; `close`.
5. `ship` -> move the directory to `.claude/skills/<id>`, `talent-deploy`, capability map,
   commit. `iterate` -> one rewrite, back to a candidate build. `abandon` -> the candidate stays.

## Rules that came from failures (all measured, all in the REVIEW document)
- The arm prompt names the CONTENT a reply must carry, never its shape.
- A dispatch never shares a shell command with a rewrite; the phase script is the dispatch.
- Coordinator turns are never typed in; `derive_coordinator_turns` reads the ledger.
- decide writes its own 8.1 event. A run that dies with no output is retried once by dispatch.
- The reviewer finds true defects in every text, adopted ones included (15 of 15 red). It is
  a critic. Fix what it says once; do not let it end a build.
