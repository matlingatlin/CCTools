---
title: Raw layer — the four Claude Code doc pages that changed within hours of the first fetch
imported: 2026-09-04 (second fetch of the day, hence the `b`)
status: RAW — never edited; the first fetch in ../claude-code-docs-2026-09-04/ stays, because notes cite it
---

# Why a second dated fetch on the same day

`knowledge/watch.py` was written this afternoon to answer "have the bytes we read changed?" —
after measuring that the calendar-based `kb.py stale` was the wrong clock. Its first run, hours
after the morning fetch, reported **5 of 10 watched sources changed**. That was checked before
it was believed: the diffs are real content, not a nondeterministic header.

| Page | Changed lines | Substance |
|---|---|---|
| `skills` | 16 | nested `.claude/skills/` do NOT load at startup; `/add-dir` (v2.1.257+); `/skill-doctor`; Bash output ceiling returns a file path + preview |
| `sub-agents` | 4 | `--append-subagent-system-prompt-file` (v2.1.261+); reworded worktree refusal |
| `mcp` | 2 | removing a remote server also deletes its stored OAuth tokens and client registration |
| `hooks` | 2 | an `/add-dir` edge case |

Unchanged in the same run: `hooks-guide`, `plugins`, `plugin-marketplaces`, `features-overview`,
and the graphify `main` README.

The raw-layer rule holds: the morning's files are NOT overwritten. A source that moves on gets a
new dated directory and the old one stays, because notes cite it — and here the two together are
the evidence that the docs moved twice in one day.
