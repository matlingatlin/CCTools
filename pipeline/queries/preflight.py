#!/usr/bin/env python3
"""Preflight: refuse a commit that damaged a talent's frontmatter.

Why this exists. Three times now a coordinator edit that meant to touch only
`description` has damaged the block around it: twice by swallowing the closing
`---` (three talents shipped unloadable, wave 28), once by dropping every key
that followed the description -- including `disable-model-invocation: true`,
which is a security gate, not a preference (wave 29). Every one of those was
SILENT: the file still looked like a skill, and the loose check in use at the
time (`content.split('---')[1]`) reported green on all of them because it
ignores line boundaries.

So this does not re-check the thing that was already believed true. It compares
each changed file's frontmatter against the version in HEAD and fails on any
key that disappeared. A key you meant to remove is declared, once, in
ALLOW_DROP -- an intentional removal costs one line, an accidental one fails.

It also gates STAGING SCOPE. Three coordinator defects in one wave had a single
shape: a rule I had written down, said aloud and intended never became a check
at the moment of acting. One of them was `git add -A` sweeping a still-running
agent's unreviewed, untested talent onto main, one message after I said I would
hold exactly those files. So: a staged talent with no `tested` event in the
ledger fails, unless it is named in ALLOW_UNTESTED. Committing untested work on
purpose costs one line; doing it by accident is refused.

Exit 1 on any finding. Run before every commit that touches library/.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Keys whose removal is intentional, as {(path, key)}. Keep this empty unless a
# removal is deliberate, and delete the entry once it is committed.
ALLOW_DROP = set()

# Talent names it is intentional to commit WITHOUT a passing test event, as
# {name}. An author's output committed before its tester has run belongs here,
# named, for exactly as long as that is true. Empty is the correct steady state.
ALLOW_UNTESTED = set()


def parse(text, where):
    """Line-anchored frontmatter parse. Returns (keys, description, error).

    Line 1 must be exactly `---`, and a LATER line must be exactly `---`.
    Anything looser reports green on an unterminated block, which is the bug
    that shipped three talents unloadable.
    """
    lines = text.split('\n')
    if not lines or lines[0] != '---':
        return None, None, f'{where}: line 1 is not exactly `---`'
    end = None
    for i, l in enumerate(lines[1:], 1):
        if l == '---':
            end = i
            break
    if end is None:
        return None, None, f'{where}: frontmatter is never closed by a line that is exactly `---`'
    keys, desc = set(), None
    for l in lines[1:end]:
        m = re.match(r'^([A-Za-z_][\w-]*):(.*)$', l)
        if m:
            keys.add(m.group(1))
            if m.group(1) == 'description':
                desc = m.group(2).strip().strip('"').strip("'")
    return keys, desc, None


def head_version(path):
    r = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def cap():
    p = os.path.join(ROOT, 'pipeline/CONSTANTS.md')
    m = re.search(r'`DESCRIPTION_CAP_CHARS`\s*\|\s*\*\*(\d+)\*\*', open(p).read())
    return int(m.group(1)) if m else None


def listing_truncation():
    """Where the HOST cuts, as opposed to where we author.

    `cap()` is the authored standard (1024, the agentskills.io spec limit). This is the
    different, larger number: Claude Code truncates `description` + `when_to_use` COMBINED at
    1,536 characters in the listing. Crossing it is not a style finding -- the tail is silently
    dropped, and by this library's house style the tail is where the NOT-clauses live, which are
    the lines that stop a mis-route. Measured 2026-09-08: 0 of 92 units use `when_to_use`, so the
    whole budget is the description's, and the largest description has **90 characters of
    headroom**. One added clarifying clause crosses it, and the clause just added is what
    disappears. Re-verified the same day against the docs bytes held at
    knowledge/raw/claude-code-docs-2026-09-04b/skills@2026-09-04b.md: still 1,536.
    """
    p = os.path.join(ROOT, 'pipeline/CONSTANTS.md')
    m = re.search(r'`DESCRIPTION_LISTING_TRUNCATION`\s*\|\s*\*\*(\d+)\*\*', open(p).read())
    return int(m.group(1)) if m else None


def tested_talents():
    """Talent names carrying a passing test event in the ledger."""
    out = set()
    path = os.path.join(ROOT, 'pipeline/ledgers/talents.jsonl')
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get('tested') and row.get('talent'):
                    out.add(row['talent'])
    except FileNotFoundError:
        pass
    return out


def staged_units():
    """Unit names whose files are STAGED for commit."""
    names = set()
    diff = subprocess.run(['git', 'diff', '--cached', '--name-only'],
                          cwd=ROOT, capture_output=True, text=True).stdout
    for p in diff.split('\n'):
        p = p.strip()
        if p.endswith('/SKILL.md'):
            names.add(os.path.basename(os.path.dirname(p)))
        elif (('/agents/' in p or '/commands/' in p) and p.endswith('.md')
              and not p.endswith('.evals.md')):
            names.add(os.path.splitext(os.path.basename(p))[0])
    return names


def main():
    changed = subprocess.run(
        ['git', 'status', '--porcelain', '--untracked-files=all'],
        cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
    paths = []
    for line in changed:
        if not line.strip():
            continue
        p = line[3:].strip()
        if p.endswith('/'):
            for dp, _, fs in os.walk(os.path.join(ROOT, p)):
                paths += [os.path.relpath(os.path.join(dp, f), ROOT)
                          for f in fs if f.endswith('.md')]
        elif p.startswith('library/') and p.endswith('.md'):
            paths.append(p)

    units = [p for p in sorted(set(paths))
             if (p.endswith('/SKILL.md') or
                 (('/agents/' in p or '/commands/' in p) and not p.endswith('.evals.md')))]

    findings, c, trunc = [], cap(), listing_truncation()
    for p in units:
        keys, desc, err = parse(open(os.path.join(ROOT, p)).read(), p)
        if err:
            findings.append(err)
            continue
        for req in ('name', 'description'):
            if req not in keys:
                findings.append(f'{p}: frontmatter has no `{req}`')
        if c and desc and len(desc) > c:
            findings.append(f'{p}: description is {len(desc)} chars, over the pinned cap of {c}')
        if trunc and desc and len(desc) >= trunc:
            findings.append(
                f'{p}: description is {len(desc)} chars, AT OR OVER the host listing truncation '
                f'of {trunc}. This is not a style finding: the tail is cut in the listing the '
                f'model sees, and the tail is where the NOT-clauses are. Shorten it.')
        elif trunc and desc and trunc - len(desc) < 100:
            findings.append(
                f'{p}: description is {len(desc)} chars, only {trunc - len(desc)} from the '
                f'{trunc}-char listing truncation. Nothing reports crossing it at runtime, so '
                f'the next clarifying clause added here is the one that vanishes.')
        old = head_version(p)
        if old is None:
            continue  # new file: nothing to have dropped
        old_keys, _, old_err = parse(old, p)
        if old_err:
            continue  # HEAD was already broken; not this edit's finding
        for k in sorted(old_keys - keys):
            if (p, k) in ALLOW_DROP:
                continue
            findings.append(
                f'{p}: frontmatter key `{k}` was present in HEAD and is gone. '
                f'Restore it, or declare it in ALLOW_DROP if the removal is intended.')

    # Frontier drift: a candidate still queued to be BUILT that already exists on
    # disk as a tested talent. frontier.json has now lied three times this way,
    # and it is silent -- a stale queue reads exactly like real work, so the next
    # wave either rebuilds a shipped talent or reports the queue non-empty when
    # there is nothing to do.
    try:
        with open(os.path.join(ROOT, 'pipeline/frontier.json')) as fh:
            # entries are a mix of bare strings (older) and dicts (newer)
            queued = [c if isinstance(c, str) else c.get('name')
                      for c in json.load(fh)['build_candidates']['queue']]
    except (OSError, KeyError, ValueError):
        queued = []
    shipped = set(os.listdir(os.path.join(ROOT, 'library/skills'))) if os.path.isdir(
        os.path.join(ROOT, 'library/skills')) else set()
    have = tested_talents()
    for name in queued:
        if name in shipped and name in have:
            findings.append(
                f'{name}: still in frontier.json build_candidates.queue, but it is already '
                f'on disk AND has a passing test event. Move it to done.')

    # Staging scope: an untested talent must not ride along in a commit unless
    # that is declared. This is the gate for the `git add -A` defect.
    have_tests = tested_talents()
    for name in sorted(staged_units() - have_tests - ALLOW_UNTESTED):
        findings.append(
            f'{name}: STAGED for commit with no passing test event in '
            f'pipeline/ledgers/talents.jsonl. An author never tests its own work here. '
            f'Unstage it, or name it in ALLOW_UNTESTED if committing it untested is deliberate.')

    if not units and not findings:
        print('preflight: no talent files changed')
        return 0
    for f in findings:
        print(f'FAIL  {f}')
    print(f'preflight: {len(units)} changed talent file(s), {len(findings)} finding(s)')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
