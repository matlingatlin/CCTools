---
source: matlingatlin/hello-world (7 branches) + matlingatlin/Scio (main)
harvested: 2026-08-30
by: coordinator (single writer)
status: INTAKE — nothing here has passed a gate
---

# Intake — all agent and skill material from hello-world and Scio

Everything that could be a talent, gathered in one place so the skills-builder /
agent-builder work has a single corpus to reason over. **416 files, every one
verified byte-identical to its source** (sha256 per file, 0 mismatches).

This is raw material. **None of the four gates has been run on any of it**
(dedup · reuse-first · talent-worthiness · security), no eval has been run, and
nothing here is adopted, deployed, or routed.

## Why it is not under `.claude/`

Two mechanical reasons, not tidiness:

1. **Auto-load.** 57 distinct skills and 10 agents dropped into `.claude/` would
   join the startup listing immediately. Skill descriptions share ~1% of the
   context window; **agent descriptions share a hard 15,000-token budget across
   the whole roster** (`knowledge/notes/subagents.md`). The library would pay for
   57 unvetted units before anyone decided whether to keep one.
2. **Executable surface.** 21 `.sh` and 7 `.py` files came with this material,
   including six `PreToolUse` hooks. Our own security gate is the fourth gate and
   it has not run.

So two things were changed on the way in, and **only these two**:

| Change | What | Reversal |
|---|---|---|
| Directory rename | every `.claude/` → `_claude/`, `.claude-plugin/` → `_claude-plugin/` | one `mv` per directory; the mapping is 1:1 and total |
| Executable bit | `chmod a-x` on all 28 executables | `chmod +x` |
| Nested ignore files | `.gitignore` → `gitignore.txt`, `.gitattributes` → `gitattributes.txt` (3 files) | rename back |

**File contents are untouched.** The rename of the ignore files was done because a
nested `.gitignore` filters its own subtree silently — verified before and after
with `git check-ignore` over all 416 files: nothing is excluded.

## What came from where

| Source | Ref | SHA | Date | Files |
|---|---|---|---|---|
| hello-world | `master` | `bd4f6d7` | 2026-08-26 | 54 |
| hello-world | `claude/multi-agent-system-architecture-nmn1pc` | `dcf361a` | 2026-08-29 | 150 |
| hello-world | `eval-r2-arm-a` | `fc7b659` | 2026-08-28 | 30 |
| hello-world | `eval-r2-arm-b` | `e467268` | 2026-08-28 | 32 |
| hello-world | `claude/graphify-q78hen` | `00408d3` | 2026-08-26 | 4 |
| hello-world | `claude/kor-den-dxz34c` | `d076a67` | 2026-08-07 | **0 — nothing unique** |
| hello-world | `claude/las-och-utfor-otg0qr` | `a4ce143` | 2026-08-06 | **0 — nothing unique** |
| Scio | `main` | `05d396e` | 2026-08-27 | 146 |
| | | | **total** | **416** |

The two August branches were checked with `comm -23` against master's full file
list and returned empty — their work is already merged. Recorded so nobody has to
check again.

## Units in the corpus

| Unit type | Distinct | Files (incl. variants) |
|---|---|---|
| Skills (`SKILL.md`) | **57** | 69 |
| Agents | **10** | 15 |
| Shell hooks | **8** | 12 |
| Commands | 2 | 2 |
| Validation harness | 1 (15 files) | 15 |
| `evals.md` / eval documents | — | 16 |

## Layout

```
hello-world/
  master/                    54 — the baseline: _claude/{commands,hooks,settings},
                                  docs/ (47, incl. 22 ADRs), CLAUDE.md, README,
                                  RUNBOOK-CONTINUOUS-IMPROVEMENT-LOOP.md
  multi-agent-branch/       150 — THE MAIN BODY. 41 commits ahead of master, never
                                  merged. 24 skills · 9 agents · 6 hooks ·
                                  _claude/validate/ (15) · 53 new docs (specs,
                                  hook proposals, audits, tester briefs,
                                  measurements, the research pipeline's artefacts)
                                  Paths are the diff vs master, so app source is
                                  excluded by design; every doc these skills and
                                  agents cite inside hello-world is present.
  eval-r2-arm-a/
    unique/                  10 — the round-2 A/B experiment output: a
                                  migration-reviewer agent, 3 migration skills,
                                  spec, baseline, evals, run notes
    divergent-from-multi-agent/
                             20 — EARLIER versions of 17 shared files + 3 docs.
                                  Both arms branched at dd6eb991, an ancestor of
                                  the multi-agent branch. These are history, not
                                  rivals — see "Which version is current" below.
  eval-r2-arm-b/
    unique/                  12 — the other arm: migration-reviewer, 2 skills,
                                  a write-gate hook, SQL fixtures, ADR-0022,
                                  test report
    divergent-from-multi-agent/
                             20 — same 20 paths as arm-a, arm-b's versions
  graphify-branch/            4 — the vendored graphify skill, 1204 lines.
                                  **This is the version Scio's VENDORED.md calls
                                  wrong** (wrong `check_semantic_cache` signature,
                                  1153 lines differed). Kept for the record; the
                                  corrected 713-line version is in scio/.
scio/                       146 — full copy of main: 27 skills, hooks/hooks.json,
                                  _claude-plugin/ (plugin + marketplace manifests),
                                  scripts/ (7, incl. skill-intake.py and
                                  skills-index.py — talent-factory tooling),
                                  docs/ (86, incl. 34 eval docs, 9 mined, 4 triage,
                                  17 as-built, the 5.5 MB code graph)
```

## Which version is current

Three files exist in three versions (multi-agent branch, arm-a, arm-b) and the
answer is not "the newest commit date":

- Both arms branched from `dd6eb991`, which is an **ancestor** of the multi-agent
  branch. The multi-agent branch is 41 commits ahead of master and the arms are 7
  and 8; the arms' extra commits are the experiment, not continued development of
  the shared files.
- **The multi-agent branch is the current line** for the 17 shared `_claude/`
  files. The arms' copies are kept because they are the *before* half of a
  measured A/B, and discarding them would discard the measurement.

## Known problems in this material — recorded, not fixed

These are stated by the material itself and must not be lost in the move:

1. **The ablation on the three agent-building skills returned null.**
   `agent-builder.md` says so directly: the arm without `agent-shape`,
   `agent-baseline` and `agent-assembly` "did no worse, and did better on the
   decisive artefact". n=1, confounded, but it is the only datum.
2. **Evals cover 4 of 24 skills** on the multi-agent branch (agent-assembly,
   architecture-decision, architecture-review, system-decomposition). Scio's 27
   have **none**.
3. **`docs/as-built/` is cited as local by twelve files in hello-world and is not
   there** (backlog B128). It lives in Scio, and both copies are now in this
   intake — so the references are resolvable here even though they were not at
   the source.
4. **Absolute paths.** Much of this material hard-codes `/home/user/skills-repo/`
   and `/home/user/scio/`, which violates the generality rule in our CLAUDE.md.
   Fixable at adoption, per unit.
5. **The graphify skill on `claude/graphify-q78hen` is the version Scio replaced
   as wrong.** Do not harvest it as if it were current.

## What has explicitly NOT been done

- No gate run: dedup, reuse-first, talent-worthiness, security — all four pending.
- No eval, no baseline, no `evals.md` authored.
- Nothing wired into `CLAUDE.md`'s capability map or `pipeline/ROUTING.md`.
- Nothing deployed; no `talents.jsonl` events written.
- No description checked against the 1024 cap or against existing siblings.
- No security audit of the 28 disarmed executables.

## Reproducing this

Every path here maps back to `<repo>@<sha>:<path>`, with `_claude` → `.claude`
and `_claude-plugin` → `.claude-plugin`, and `gitignore.txt` / `gitattributes.txt`
→ their dotted names. Verification was per file:

```
sha256(git cat-file blob <ref>:<path>)  ==  sha256(<intake path>)
```

416 of 416 matched.
