#!/usr/bin/env python3
"""context_surface.py — what every session in this repo pays BEFORE any work happens.

Why this exists. CLAUDE.md stated the talent listing "shares ~1% of the context window
across all talents". Measured 2026-09-08 it is 1.69% for the descriptions alone and 2.26%
counting CLAUDE.md itself — the stated figure understated by ~70%. The number was not
wrong when written; it is a RUNNING statistic pinned as if it were a constant, in the one
file every turn reads.

CONSTANTS.md already articulates the rule this violated, about a different value: "a value
that moves on its own must be recorded as a finding plus a pointer to its live computation,
never as a number. A pinned number that drifts is worse than no number, because it is cited
with the authority of this file." That rule had a pointer (`preflight.py`) for the over-cap
count and none for the context share. This is the missing pointer.

Deterministic, read-only, standard library only. The token figure is an ESTIMATE at 4 bytes
per token and is labelled as such wherever it prints — no tokenizer is available offline,
and a fake precision here would be worse than a stated approximation.

Usage:  python3 pipeline/queries/context_surface.py
        python3 pipeline/queries/context_surface.py --window 200000   # a smaller window
"""
import os
import re
import signal
import sys
import glob

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # let `| head` cut output without a traceback

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BYTES_PER_TOKEN = 4  # estimate; see the docstring
DEFAULT_WINDOW = 1_000_000  # Opus 5, per knowledge/notes/agent-design-template.md


def cap():
    """The authored cap, read from CONSTANTS.md rather than repeated here."""
    p = os.path.join(ROOT, 'pipeline/CONSTANTS.md')
    m = re.search(r'`DESCRIPTION_CAP_CHARS`\s*\|\s*\*\*(\d+)\*\*', open(p).read())
    return int(m.group(1)) if m else None


def descriptions(pattern, name_from):
    """(name, length) for every unit matching pattern that declares a description."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):
        m = re.search(r'^description:\s*(.+)$', open(f, encoding='utf-8').read(), re.M)
        if m:
            out.append((name_from(f), len(m.group(1).strip().strip('"').strip("'"))))
    return out


def main():
    window = DEFAULT_WINDOW
    if '--window' in sys.argv:
        window = int(sys.argv[sys.argv.index('--window') + 1])

    # Archived, not root: a root CLAUDE.md auto-loads, and this repository is deliberately
    # inert. The file is still what the figures below are ABOUT, so it is read where it lives.
    steering = os.path.join(ROOT, 'docs', 'steering', 'CLAUDE-md-archived.md')
    steering_b = len(open(steering, 'rb').read()) if os.path.exists(steering) else 0

    skills = descriptions('library/skills/*/SKILL.md', lambda f: os.path.basename(os.path.dirname(f)))
    agents = descriptions('library/agents/*.md', lambda f: os.path.splitext(os.path.basename(f))[0])
    listing_b = sum(n for _, n in skills + agents)
    total_b = steering_b + listing_b

    def row(label, b, n=None):
        tok = b // BYTES_PER_TOKEN
        count = f"{n:>3d}" if n is not None else "  -"
        return f"| {label:<26s} | {count} | {b:>8,d} | ~{tok:>7,d} | {b/BYTES_PER_TOKEN/window*100:>6.2f}% |"

    print(f"# Always-on context surface  (window {window:,d} tokens, ~{BYTES_PER_TOKEN} B/token ESTIMATE)\n")
    # In THIS repository the true always-on cost is zero: nothing sits under .claude/, so no
    # description is listed and no talent routes. The figures below are what the library would
    # cost the turn it is installed into a project - which is the number worth knowing before
    # installing it, and the reason this script moved across with the library rather than being
    # retired. Said here because a table headed "always-on" otherwise asserts the opposite.
    print("NOTE: nothing here is loaded. This is the cost the library WOULD carry once its\n"
          "      units are installed under a project's .claude/; measured, not estimated.\n")
    print("| component                  |   n |    bytes |  ~tokens | share |")
    print("|----------------------------|-----|----------|----------|-------|")
    print(row("CLAUDE.md", steering_b))
    print(row("skill descriptions", listing_b - sum(n for _, n in agents), len(skills)))
    print(row("agent descriptions", sum(n for _, n in agents), len(agents)))
    print(row("TOTAL always-on", total_b, len(skills) + len(agents)))

    # Inside the steering doc: which section costs what. Added 2026-09-08 after measuring
    # that ONE section was 68% of the file, and that the file's own claim about it was false.
    if steering_b:
        body = open(steering, encoding='utf-8').read()
        parts = re.split(r'^## ', body, flags=re.M)
        print(f"\nInside CLAUDE.md ({steering_b:,d} B):")
        for i, s in enumerate(parts):
            title = "(preamble)" if i == 0 else s.split("\n")[0][:40]
            b = len(s.encode('utf-8'))
            print(f"  {title:<42s} {b:>7,d} B  ~{b // BYTES_PER_TOKEN:>5,d} tok  {b / steering_b * 100:>5.1f}%")
        m = re.search(r'^## Capability map.*?(?=^## |\Z)', body, re.S | re.M)
        if m:
            named = set(re.findall(r'`([a-z][a-z0-9-]{3,})`', m.group(0)))
            have = {n for n, _ in skills + agents}
            print(f"  -> the capability map names {len(named & have)} of the {len(have)} loaded "
                  f"talents, whose own descriptions are already loaded above.")

    # The ON-DEMAND surface, for contrast. A body is paid only when its skill triggers;
    # a description is paid every turn. Added 2026-09-08 because the library's own body
    # lengths had never been measured against the four incompatible bars the sources give
    # (see knowledge/notes/anthropic-skill-authoring-contract.md, "Body length").
    bodies = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'library/skills/*/SKILL.md'))):
        txt = open(f, encoding='utf-8').read()
        body = txt.split('---', 2)[2] if txt.startswith('---') else txt
        bodies.append((os.path.basename(os.path.dirname(f)),
                       len(body.strip().splitlines()), len(body.split()),
                       len(body.encode('utf-8'))))
    if bodies:
        tb = sum(b[3] for b in bodies)
        med = sorted(b[1] for b in bodies)[len(bodies) // 2]
        over = [b for b in bodies if b[1] > 500]
        print(f"\nOn demand, not always-on: {len(bodies)} skill bodies, {tb:,d} B "
              f"(~{tb // BYTES_PER_TOKEN:,d} tok if every one triggered at once)")
        print(f"  median {med} lines; over the most-stated 500-line bar: "
              f"{len(over)} ({', '.join(b[0] for b in over) or 'none'})")

    c = cap()
    if c:
        over = sorted(((n, L) for n, L in skills + agents if L > c), key=lambda x: -x[1])
        print(f"\nOver the authored cap ({c}, DESCRIPTION_CAP_CHARS in CONSTANTS.md): "
              f"**{len(over)} of {len(skills) + len(agents)}**")
        for n, L in over:
            print(f"  {L:>5d}  {n}")
        if over:
            print("\nTrimming changes routing: each is an edit with a trigger check, never a\n"
                  "mechanical truncation (CONSTANTS.md, known-violation note).")
    print("\nEvery figure above is computed now. Do not copy one into a document as a "
          "constant —\ncite this script.")


if __name__ == '__main__':
    main()
