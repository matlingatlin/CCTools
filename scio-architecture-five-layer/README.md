# `claude/scio-architecture-five-layer-t8t9mp`, parked 2026-09-12

| | |
|---|---|
| branch head | `30e197b3861be7ee2f5e4b390614ea0d900f79df` |
| last commit on it | 2026-09-11 14:49:03 +0000 |
| forked from | `0b0bdf588d57db80e26c67bcbfdc853efe126a49` (2026-09-03), the same point as three other session branches |
| commits | 25 |

## What is here

| | |
|---|---|
| `notes/` | **10 notes `main` does not have**, ~800 lines: agent-harness-principles-2026 · app-builder-prior-art-and-library-standards-2026-09 · build-evidence-tooling-2026 · claude-agent-sdk-hosting-and-limits-2026-09 · evidence-artefact-schemas-2026-09 · inter-rater-agreement-kappa-2026-09 · otel-genai-semantic-conventions-2026-09 · preview-and-sandbox-egress-boundary-2026-09 · supabase-row-level-security-2026-09 · typescript-stack-scan-2026-09 |
| `raw/` | **44 held source files** in four dated directories, each with its own `MANIFEST.md` |
| `changes-to-existing.patch` | 850 lines: everything the branch CHANGED in files `main` also has (25 notes, `knowledge/INDEX.md`, `knowledge/sources/SOURCES.md`, `pipeline/LESSONS.md`, `pipeline/STATUS.md`) |

## Why the changes are a patch and not files

The 25 shared notes are the reason this could not simply be merged. Measured against the fork point:
the branch's edits to them are **1 to 13 lines each**, while `main`'s edits to the same notes are
**140, 188, 149 lines**. So `main` holds the newer and far richer version of every shared note, and
copying the branch's files over them would have reverted a day of verified work.

A patch loses nothing and asserts nothing. It says exactly what the branch added, against a base
both sides share, and leaves the judgement for whoever applies it.

**A trial merge was run and then aborted, and it is worth recording what it found**, because it is
the map for applying the patch: **28 conflicts**. A resolver that keeps `main`'s `raw:` block and
takes the **union** of the `related:` lists cleared **11** of them mechanically and **refused 13** —
correctly, because those 13 are not frontmatter at all but **two different paragraphs written in the
same place**. Four more files (`skill-authoring-eval-methodology`, `third-party-landscape`,
`pipeline/STATUS.md`, `knowledge/sources/SOURCES.md`) need judgement of their own. So the work
remaining is **13 prose hunks plus 4 files, read one at a time** — not a merge command.

## The notes have their evidence; what they lack is the pointer

**None of the 10 notes carries a `raw:` key**, which `kb.py lint` now requires unconditionally, and
that is the single reason they are parked rather than placed. But they are **not unverifiable**: the
bytes are all here, and each `MANIFEST.md` carries per-file URL, fetch date, sha256, size and a
**`Feeds` column naming the note the file supports**.

So the join key exists — **in the other direction.** This base writes it note → raw in frontmatter;
this branch wrote it raw → note in a manifest. Same information, opposite arrow, which is exactly
the "asserted from only one end" shape. **That makes the `raw:` keys reconstructible mechanically
from the `Feeds` columns rather than by re-reading 10 notes**, and it is the first step for whoever
promotes these.

## Re-entry condition, per item, so this is recoverable and not merely stored

1. **`raw/` → `knowledge/raw/`**: each directory needs its files either baselined in
   `knowledge/raw/WATCH.tsv` or declared in `watch.py`'s `NEVER_WATCHED` with a reason, or
   `watch.py --offline` fails on the unaccounted files. The MANIFESTs already hold every URL and
   sha256 needed to write those rows.
2. **`notes/` → `knowledge/notes/`**: add the `raw:` key from the `Feeds` columns, then
   `kb.py lint` must come back with no new errors. Expect the reciprocity check to speak up — these
   notes name neighbours in `main` that do not name them back yet, which is the one-way-link debt
   parallel authoring produces structurally.
3. **`changes-to-existing.patch`**: 13 prose hunks and 4 files, read individually. `main`'s version
   is newer in every shared note; that is a reason to read the branch's paragraph as a possible
   *addition*, never a reason to assume it is a worse duplicate.

Until all three are done, nothing in this folder is part of the knowledge base, and
`kb.py`/`watch.py` will not see it.
