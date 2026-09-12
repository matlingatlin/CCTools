#!/bin/sh
# Ensure this repo has a current code graph and a current corpus store.
#
# Runs on SessionStart, outside the model's context: zero tokens, no model calls.
# Silent on success. Never fails a session — every unmet precondition exits 0.
#
# The order matters and is not cosmetic. `graphify hook` rebuilds only the files in
# a commit, so installing it before a full build yields a graph of recent commits
# and nothing else — complete-looking and wrong. Full build first, hook second.
# Measured 2026-08-26: hook alone 3 nodes / 2 edges on a two-file repo; full build
# immediately after, 6 and 8.

set -u

command -v graphify >/dev/null 2>&1 || exit 0        # not installed: not our business
[ -d .git ] || exit 0                                 # not a repo: nothing to hook

LOG="${TMPDIR:-/tmp}/scio-ensure-graph.log"

# 1 · Full build, once. Backgrounded: a 6,000-file repo takes ~9.5s and a session
#     must not wait for it. Absent graph only — never rebuild what already exists,
#     or every session start pays for a repo it did not change.
if [ ! -f graphify-out/graph.json ]; then
  echo "[scio] no graph found, building in background -> $LOG" >&2
  nohup graphify update . >"$LOG" 2>&1 &
fi

# 2 · Then the commit hook, so it stays current without anyone remembering.
if ! grep -q graphify .git/hooks/post-commit 2>/dev/null; then
  graphify hook install >>"$LOG" 2>&1 || true
fi

# 3 · The corpus store. Rebuilt whenever a source file is newer than the database, so a
#     session never queries a stale index. Deterministic, no model call, well under a second.
if [ -d docs/triage ] || [ -d .claude/skills ]; then
  if [ ! -f scio.db ] || [ -n "$(find .claude/skills docs -name '*.md' -newer scio.db -print -quit 2>/dev/null)" ]; then
    python3 scripts/scio-db.py build >>"$LOG" 2>&1 || true
  fi
fi

exit 0
